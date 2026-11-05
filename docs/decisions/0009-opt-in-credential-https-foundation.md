# ADR 0009: Explicit credentials and opt-in HTTPS transport foundation

- Date: 2026-11-05 (Asia/Seoul)
- Status: **proposed for independent review; offline implementation**, not live API approval.
- Base: `b83b5b28c0024120164e6ee2b858f1a02a24897a` (merged PR #20).
- Related: Issue #17; ADR 0005–0008 remain binding.

## Decision and boundaries

Add private Python components separate from Rust Core, broker decoders, PyO3 and
public value models. This implements runtime mechanisms but does **not** authorize
the assistant to access accounts, fetch tokens or make any real network request.

- `CredentialIdentity` is broker + explicitly supported live/paper environment +
  user-chosen *non-secret* profile alias. Real account numbers must never be
  used as the alias. Missing/unsupported environments are rejected.
- `InMemoryCredentialProvider` only accepts keys/secrets intentionally supplied
  by a caller; there is no environment, keychain, filesystem, MAC or account
  discovery. Secret-bearing objects have redacted representations, but Python
  memory remains introspectable; do not log them or use `vars`/`asdict`.
- `InMemoryTokenCache` is instance-local. It binds each bearer lease to the
  exact provider object, broker/environment/profile and current credential
  generation. Expiry is exclusive; optional safety margin is fail-closed.
  Rotation/revocation invalidate; no automatic token issue, refresh or retry.
- `_https_transport.HttpsTransport` has `network_enabled=False` by default.
  Only an explicit opt-in instance can connect. It uses `http.client` over
  verified TLS with `SSLContext(PROTOCOL_TLS_CLIENT)`, hostname verification
  and system roots; never disables certificate checks. It deliberately avoids
  `create_default_context()` because that helper can honor `SSLKEYLOGFILE` and
  enable TLS session-key logging from the ambient environment. It does not consult proxy
  environment variables, follow redirects, reuse cookies, persist secrets or
  auto-retry. System-level proxy interception or hostile monkeypatching is
  not a threat model this component can enforce.
- DNS/TLS connection failures before writing have `NOT_SENT` delivery state.
  A write failure or failure to obtain response headers has `UNKNOWN` state:
  it may already have reached the server. Status/response-body errors have
  `RESPONSE_RECEIVED` state. **No caller may assume an UNKNOWN failure is safe
  to retry**, particularly for future orders. There are no order paths here.
- HTTP quote and token requests are assembled using canonical fixed-origin
  existing request plans and publisher-example evidence, not arbitrary URLs.
  The entire body and header tuple must match the builder's canonical shape,
  including the exact credential snapshot and bearer lease. Host/framing header
  overrides and altered quote symbols in request bodies are rejected.
  Credential and token revocation/rotation/expiry are rechecked before connecting
  and again after TLS, before the HTTP write. This is not atomic coordination
  with other threads/processes; concurrent use requires a separate design.
  Exact 200 is the only provisional success status; all other status families
  fail with static classification. One network attempt at most; response bodies
  are bounded at 1,048,576 bytes and treated as **untrusted**. A body that
  ends before its declared `Content-Length` is a `READ` failure with
  `RESPONSE_RECEIVED` state, because `http.client`'s bounded `read(amt)` does
  not raise `IncompleteRead` on an early close (including a TLS close without
  `close_notify`). The send clock is fixed at transport construction and read
  twice; there is no per-call clock override (follow-up to the PR #22 review).
- Token request construction/response parsing is **candidate-only for KIS and
  Kiwoom** based on pinned official example source files. A token response must
  explicitly declare bearer `token_type`; Kiwoom must also have integer
  `return_code == 0`. Missing fields are never treated as success, even where
  upstream example code is permissive. Explicit error envelopes are rejected.
  KIS `access_token_token_expired` (`%Y-%m-%d %H:%M:%S`) is naive in the pinned
  sample: the parser requires a caller-supplied `kis_expiry_timezone` (a fixed
  `datetime.timezone`) and otherwise fails with `EVIDENCE_MISSING`. Tests supply
  a synthetic offset; that does not confirm the production time basis. Kiwoom
  `expires_dt` (`%Y%m%d%H%M%S`) uses KST explicitly in the pinned publisher code.
  No guessed TTL or transitive secret fallback. Duplicate JSON keys, non-finite
  constants, malformed/deeply nested input and noncanonical date text fail.
- LS, DB, Toss and Meritz can have distinct in-memory credential identities
  but **cannot** create real token/quote WireRequests until their relevant
  publisher-confirmed contracts are fully verified. DB's unsafe query-secret
  sample is deliberately *not implemented*. No MAC auto-detection.
- Native decoder, typed `Ticker`, quote provenance and public `fetch_ticker`
  remain **unchanged / unavailable**. No `WireResponse` is automatically
  promoted to a `Ticker`: provider response status, venue, environment and
  session/source assertions are still not fully evidenced.

## Timeout and TLS implementation limits

`timeout_ms` sets the standard-library socket blocking-operation timeout. It is
**not** an end-to-end wall-clock deadline, DNS deadline or cancellable operation;
a peer making incremental progress can keep a request alive beyond that value.
A response byte cap is not a duration bound. Before production integration,
choose and independently test an absolute deadline/cancellation strategy.
No live TLS handshake, DNS query or timeout behavior is validated by mock tests.

Python 3.13 primary references, checked 2026-11-05:
[HTTPConnection timeout](https://docs.python.org/3.13/library/http.client.html#http.client.HTTPConnection),
[SSLContext](https://docs.python.org/3.13/library/ssl.html#ssl.SSLContext), and
[create_default_context / SSLKEYLOGFILE](https://docs.python.org/3.13/library/ssl.html#ssl.create_default_context).

## Verification and next gates

Only synthetic fixtures and fake HTTPSConnection objects are exercised in CI.
Tests verify TLS settings, no actual socket from disabled transport, path and
host binding, expiring/rotated credentials, strict token examples, bounded
payloads, no redirect or retry and NOT_SENT/UNKNOWN/RESPONSE_RECEIVED.

Actual use requires separately approved and reviewed work: confirmed current
broker endpoint/headers/body/status/token semantics, secure credential source,
verified real/paper and market/session provenance, and opt-in sanitised network
integration. This ADR is a proposed internal foundation, **not an official
published broker support statement**. In particular KIS request key case,
Kiwoom signed quote prices, LS t1102, safe DB authentication, Toss revision
and token semantics, and Meritz MAC/quote evidence remain Issue #17 gates.
