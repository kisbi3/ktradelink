# ADR 0013: Experimental public `fetch_ticker` surface

- Date: 2026-11-05 (Asia/Seoul)
- Status: **proposed for independent review; offline implementation**. Merging
  this does not authorise any live run, by anyone. Every capability stays
  `documented_candidate`.
- Base: `main` `1a7b893f2f9fc205775314cd3ad51404442db046` (after PR #27).
- Related: Issue #17. Replaces the ADR 0006/0009/0011/0012 statements that a
  public `fetch_ticker` is unavailable. Everything else in ADR 0005–0012 stays
  binding.

## Context

After PR #27 every piece of a KIS, Kiwoom or LS quote exists in private
modules: the request planner, the in-memory credential provider and token
cache, the opt-in `HttpsTransport` with send attestation and single-flight
token sends, the token codec and the native decoders. The only way to use
them was to wire them by hand, as `tools/live_smoke_ls.py` does for LS. Hand
wiring is where a token gets printed or a retry gets added. The spec
(section 2) proposes `broker.fetch_ticker(symbol, *, venue="KRX", params=None)`.

## Decision

1. **Shape.**
   ```python
   client = ktradelink.connect(
       "ls", environment="live", credentials=ktradelink.Credentials(key, secret),
       allow_network=True, accept_unverified=True,
   )
   ticker = client.fetch_ticker("005930")  # venue="KRX", params=None
   ```
   - `connect()` sends nothing. It validates the whole configuration and
     returns a `BrokerClient` bound to one broker, one environment and one set
     of credentials. A `BrokerClient` cannot be constructed directly.
   - `fetch_ticker` returns the existing `ktradelink.models.Ticker`, never a
     dict. `timestamp` and `retrieved_at` stay `None`; `info` stays empty.
   - `symbol` must be exactly six ASCII digits (`InvalidSymbol`). `venue`
     must be `"KRX"`; `"NXT"`/`"BROKER_COMPOSITE"` raise
     `UnsupportedCapability`, anything else `InvalidVenue`. `params` must be
     `None` or an empty mapping; anything else is `InvalidParameter`.
   - All argument checks run before anything else, so a bad argument never
     reaches the network.
2. **Credentials.** `ktradelink.Credentials(app_key, app_secret)` wraps the
   private `CredentialPair`:
   - `repr`/`str` print `Credentials(<redacted>)`. It has `__slots__` and no
     `__dict__`, compares by identity, and refuses `pickle`, `copy` and
     `deepcopy` with a `TypeError` that names no value.
   - The library never reads credentials from the environment, files, a
     keychain or a device. The caller passes them explicitly.
   - Invalid input raises `InvalidParameter("invalid_credentials")` with no
     chained exception.
   - Each client holds its own `InMemoryCredentialProvider` and
     `InMemoryTokenCache`. `close()` (also on `with` exit) revokes the cached
     token and clears the credentials. That drops references only; Python
     cannot erase strings, and a token already issued stays valid at the
     broker until it expires.
3. **Explicit opt-in and acknowledgement.**
   - `allow_network` defaults to `False`. Without it `fetch_ticker` raises
     `NetworkDisabled` (`NOT_SENT`) after argument validation, before the
     decoder preflight and before any request is built. The underlying
     `HttpsTransport` is also created disabled.
   - `allow_network=True` requires `accept_unverified=True`, otherwise
     `connect()` raises `UnsupportedCapability`. This is the caller's
     acknowledgement that the capability is only `documented_candidate`.
   - `ktradelink.capabilities(broker)` and `client.capabilities` report a
     `Capability(broker, method, environment, venue, state, reason)` per
     environment for `fetch_ticker` on KRX. KIS live/paper, Kiwoom live/paper
     and LS live are `documented_candidate`; LS paper and all of DB, Toss and
     Meritz are `unsupported`. Nothing is `supported` (spec section 7).
     Anything not listed is unsupported.
4. **Allowlist.** `_public_client._FETCH_TICKER` holds one entry per enabled
   broker: its required root quote status field, the one accepted value and a
   synthetic preflight payload. Enabling DB or Toss later is one reviewed entry
   there, after its token and quote wire is enabled in `_https_transport`.
   `connect()` refuses every other broker with `UnsupportedCapability`.
5. **Errors** (`ktradelink.errors`, also exported at the top level).
   - Base `KTradeLinkError` with static `reason`, `stage` (`None`, `"token"`
     or `"quote"`) and `delivery` (`NOT_SENT`, `UNKNOWN`,
     `RESPONSE_RECEIVED`). `delivery` is on every error, including transport
     errors, because an `UNKNOWN` send is never safe to repeat.
   - No error contains a credential, token, header value, body or upstream
     message, and none chains its cause: every public error is raised outside
     the `except` block that caught the private one, so `__context__` and
     `__cause__` are `None`. Errors pickle back to the same fields.
   - Diagnostics (`collect_diagnostics`, ADR 0012) stay off on this path, so
     no gateway text is collected.
   - Mapping:

     | Private outcome | Public error |
     | --- | --- |
     | HTTP 401 | `AuthenticationError` |
     | HTTP 403 | `PermissionDenied` |
     | HTTP 429 | `RateLimitExceeded` |
     | HTTP 5xx | `BrokerUnavailable` |
     | redirect, other non-200 status, connect, TLS, write, response headers, body read, oversize, token in flight, token expired before send, clock unavailable | `TransportError` with the private kind as `reason` |
     | `NOT_ENABLED` | `NetworkDisabled` |
     | `EVIDENCE_MISSING` | `UnsupportedCapability` |
     | credential changed or missing (only `close()` does that) | `ClientClosed` |
     | token response rejected by the codec | `ResponseSchemaError` (`stage="token"`) |
     | quote body not UTF-8, not a JSON object, duplicate keys, non-finite numbers | `ResponseSchemaError` |
     | quote root status missing or of the wrong JSON type | `ResponseSchemaError` |
     | quote root status present with another value | `BrokerRejected` |
     | native decoder rejection | `ResponseSchemaError`, `detail` = the decoder's static `"<field>: <Kind>"` |

   - The HTTP classes follow the generic HTTP meaning of the status code.
     They are **not** verified broker semantics, and broker-native codes are
     not interpreted. `BrokerRejected` is an addition to the spec's proposed
     names: it says "the broker answered 200 with a non-success status"
     without claiming why.
6. **Quote status is required.** The KIS and Kiwoom decoders accept a missing
   root status because the offline synthetic examples omit it (ADR 0008).
   On the public path a missing upstream status is never success: KIS `rt_cd`
   must be the string `"0"`, Kiwoom `return_code` the integer `0` (not a
   boolean), LS `rsp_cd` the string `"00000"`. These are the success values the
   decoders already define (see
   [the decoder ledger](../brokers/six-broker-ticker-decoders.md)). Requiring
   their presence is library policy, not publisher evidence that the gateways
   always send them. The check reads the root field only; the native decoder
   still validates the whole body. If a real gateway omits the field, the
   call fails closed.
7. **Token lifecycle.**
   - A cached token is reused while more than `TOKEN_REUSE_MARGIN_MS`
     (60 s, library policy, not a publisher value) remains. Otherwise one new
     token request is sent in that call. Each call sends at most one token
     request and one quote request. There is no background refresh and no
     retry.
   - LS expiry counts from the transport's pre-write clock reading
     (ADR 0011); KIS and Kiwoom use the absolute expiry in the response.
   - **KIS requires `kis_expiry_timezone`**, a `datetime.timezone` passed to
     `connect()`. The KIS sample's expiry is naive and its time zone is not
     confirmed, so the library never assumes KST for KIS. `connect()` rejects
     a missing value, a `ZoneInfo`, a string or a `timedelta`, and rejects the
     argument for every other broker.
   - A token response that fails the codec is not cached, so the next call
     sends a new token request. A token send with `UNKNOWN` delivery may have
     issued a token the client never saw; the next call issues another.
   - A quote 401 removes exactly the token that was used, so the next call
     requests a new one. 403, 429 and 5xx leave the token in place.
8. **Threads.** A `BrokerClient` is safe to share between threads in one
   process.
   - Quotes run concurrently.
   - When no reusable token is cached, the first caller takes a client
     token lock without waiting. A concurrent caller that finds the lock taken
     fails at once with `TransportError("token_request_in_flight")`, `NOT_SENT`.
     It does not wait and then send its own request, because that would repeat
     a token request whose outcome may be unknown. The private single-flight
     guard (ADR 0011) stays underneath.
   - Nothing coordinates between clients or processes: two clients using one
     app key can invalidate each other's tokens. Create one client per key.
9. **Environments.** `environment` has no default. Only the planner's
   documented origins are used: KIS live/paper, Kiwoom live/paper, LS live.
   LS paper is refused; there is no fallback between live and paper.
10. **Native decoder preflight.** Before the first request, each client
    decodes a synthetic payload for its broker with the installed native
    module and checks the result (as in ADR 0012): broker, symbol, venue,
    last price and volume must all match, so a build that mislabels
    provenance is refused before any token request. If that fails, the call
    raises `UnsupportedCapability("native_decoder_unavailable")` and nothing
    is sent. Importing `ktradelink` still does not load the native module.
11. **Local clock failures** (`clock_unavailable`) name their stage and are
    `NOT_SENT` only before that stage's request is written. After a token
    response has arrived they are `RESPONSE_RECEIVED`, because the broker may
    already have issued a token.

## Consequences and limits

- **Tests:** `tests/test_public_fetch_ticker.py` uses mocked
  `http.client.HTTPSConnection` only. It covers success for KIS, Kiwoom and LS
  (and KIS/Kiwoom paper origins), disabled network refusing before any socket,
  argument and configuration refusals, every error mapping with its delivery
  state, token reuse and re-issue, the in-flight token race, `close()` during a
  handshake, and that no synthetic secret appears in `str`/`repr`/args,
  `__context__`, `__cause__` or captured logs. The quote bodies are synthetic
  and follow the documented field names used by the decoder tests;
  `tests/fixtures` has no publisher quote fixtures. Decoding tests skip when
  the native module is absent.
- **Unverified:** no gateway has seen any of these requests. Live and paper
  acceptance, KIS lowercase query keys and missing `custtype`/`tr_cont`
  headers, the KIS expiry time zone, status universes, rate limits, Kiwoom
  signed prices and quote venue provenance are open gates, as listed in
  [the 2026-11-05 ledger](../brokers/live-auth-transport-gates-2026-11-05.md).
  KIS responses do not echo the symbol, and Kiwoom's echo is optional; the
  response is bound to the request by the transport only.
- **Timeouts:** `timeout_ms` is a per-socket-operation timeout, not a
  deadline for the whole call (ADR 0009).
- **Not changed:** the private modules, the decoders, CI and
  `docs/specifications/capability-matrix-v0.1.json`, which remains the
  proposed design matrix (`implemented: false` there means "not a supported
  adapter"). Updating the matrix is a follow-up.
- **Evidence:** no credential, token, quote, account or order request was
  made while writing this.
