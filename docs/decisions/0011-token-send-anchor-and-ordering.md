# ADR 0011: Transport-attested token send time, single-flight sends and send ordering

- Date: 2026-11-05 (Asia/Seoul)
- Status: **proposed for independent review; offline implementation**, not live API approval.
- Base: `main` `f4f966b47746ca1e6ad9c759ac5b14ee910ffa8d` (after PR #21/#24/#25).
- Related: Issue #17. Closes the "gate before any real token issuance" in
  ADR 0010, and replaces the ADR 0009 statement that concurrent use "requires
  a separate design" for one process. Everything else in ADR 0005–0010 stays
  binding.

## Context

Three gaps were open after PR #25. Each was reproduced on `main` `f4f966b`
with mocked HTTPS only:

1. **Lifetime stretching.** The LS lease expired `expires_in` seconds after
   the caller's `now_ms`. A caller passing a time taken after the response,
   or any later time, got a lease that outlived the real token. ChatGPT
   recorded this as a non-blocking gate in its PR #25 review.
2. **Out-of-order saves.** Two token exchanges for the same credentials could
   finish in either order. Saving the older response last replaced the newer
   lease. Where a broker invalidates the previous token on re-issue (Toss
   documents this; LS does not say), the cache would then hold a dead token.
3. **Concurrent sends.** Nothing stopped two token requests for the same
   credentials from being in flight at once. ChatGPT listed the missing
   concurrent token-rotation safety as a non-blocking limit in its PR #24
   re-review.

## Decision

1. **Attestation.** `HttpsTransport.send` records each token response it
   receives in a module-private, identity-keyed weak map:
   - the send's process-wide sequence number, taken when the send claims its
     in-flight slot;
   - the real-clock reading taken after the TLS handshake, immediately before
     the request write.

   `WireResponse` compares by identity (`eq=False`), so a copy or a
   field-for-field rebuild is never attested. `save_example_token_response`
   refuses an unattested response with `TokenFailure.UNATTESTED` and leaves
   the cache unchanged. The check runs after the body has been parsed, so
   malformed bodies still report `INVALID_RESPONSE`.
2. **LS lifetime anchor.** The LS lease expires `lifetime` seconds after the
   attested pre-write reading. The server cannot issue the token before the
   request is written, so this never overstates the lifetime. The caller's
   `now_ms` is used only to reject an expiry that has already passed.
3. **Single flight.** At most one token send per (provider object, credential
   identity) is in flight in the process, across all `HttpsTransport`
   instances. A second one fails with `TransportFailure.TOKEN_IN_FLIGHT` /
   `NOT_SENT` before connecting. The slot is released in `finally`, whatever
   the outcome. A send refused for being disabled, invalid, stale or
   unbound never takes the slot. Other identities and other providers are
   not blocked.
4. **Send ordering.** `BearerLease.issue_sequence` carries the attested
   sequence number. The cache also keeps, per (provider, identity), the
   highest sequence it has ever saved (a high-watermark):
   - The watermark **outlives the lease**: expiry eviction and `revoke` leave
     it in place.
   - `InMemoryTokenCache.put` refuses an attested save with
     `CredentialFailure.SUPERSEDED` (`TokenFailure.SUPERSEDED` in the codec)
     when its sequence is lower than the watermark.
   - It also refuses one that is equal to the watermark, unless that exact
     lease is still cached. Re-saving the live lease is the only allowed
     repeat.
   - So a response from an earlier send cannot be reinstated, even after the
     newer token expired or was revoked. After `revoke`, only a new send
     can repopulate the cache.
   - The watermark spans credential revisions. Sequences are process-wide
     and taken when a send starts, and a request for a newer revision can
     only be built after the rotation, so it always carries a higher
     sequence. Responses for an older revision fail `STALE_CREDENTIAL`.
   - Because sends for one identity never overlap (item 3), send-start order
     is the order in which the broker received them.
   - The watermark was added after the ChatGPT review of PR #26 (M1): the
     first version kept the order only in the cached lease, so expiry or
     revocation erased it.
5. **In-process locking.**
   - `InMemoryCredentialProvider` serialises its operations with an `RLock`.
   - `InMemoryTokenCache` serialises its operations with a `Lock`.
   - `put` holds the provider lock across the credential-currency check and
     the write, so a rotation cannot land in between.
   - Locks are always taken provider first, then cache.

## Consequences and limits

- **Callers:** `save_example_token_response` now accepts only a response that
  came from `HttpsTransport.send`. Offline tests reach that path through a
  mocked `http.client.HTTPSConnection`, using the shared
  `receive_token_response` fixture in `tests/conftest.py`.
- **Trust boundary:** the attestation is process-local Python state. Code
  that writes the private map or patches the module is outside the threat
  model, as before (ADR 0009).
- **Manual leases:** a lease put into the cache without `issue_sequence`
  (direct `cache.put`) is an explicit caller injection. It neither moves nor
  resets the watermark, so it cannot reopen the cache to an older attested
  response.
- **Memory:** the watermark is one integer per (provider, identity) for the
  cache's lifetime.
- **Processes:** nothing coordinates between processes or machines. Two
  processes sharing one app key can still invalidate each other's tokens.
- **Gateways:** none of this verifies any broker gateway. There is no
  automatic token issue, refresh or retry, no public `fetch_ticker`, and
  network stays disabled by default. No credential, token, quote, account or
  order request was made.
