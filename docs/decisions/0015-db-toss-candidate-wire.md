# ADR 0015: DB and Toss candidate token and quote wire

- Date: 2026-11-05 (Asia/Seoul)
- Status: **proposed for independent review; offline implementation**, not
  live API approval. It is a candidate only: nothing here was verified
  against a DB or Toss gateway. Merging it does not authorise any live run.
- Base: `main` `1a7b893f2f9fc205775314cd3ad51404442db046` (after PR #27).
- Related: Issue #17. Closes the DB and Toss design gates recorded in the
  [2026-11-05 ledger](../brokers/live-auth-transport-gates-2026-11-05.md).
  ADR 0005–0012 stay binding. Meritz stays blocked.

## Context

Until now `_SUPPORTED_CANDIDATES` was KIS, Kiwoom and LS. DB and Toss had
credential identities and quote plans, but no executable token or quote
`WireRequest`. The ledger recorded four gates:

1. **DB token request:** the only known DB example (the testbed sample)
   sends credentials in the URL query with `verify=False`.
2. **DB environment:** live and demo share one REST origin. The app key
   decides which one answers, so a mislabelled key cannot be detected.
3. **DB re-issue:** a token requested while one is still valid comes back
   unchanged, with its **original expiry**. The response carries only a
   relative `expires_in`, so `now + expires_in` can overstate a re-issued
   token.
4. **Toss shared token:** one valid token per client; issuing a new one
   invalidates the previous one at once. Tokens are provider-side shared
   state, which per-profile caches cannot see.

## Evidence (public documentation only, retrieved 2026-11-05 06:14–06:17 UTC)

No credential, token, quote, account or order request was sent to DB or
Toss. Sample tokens, staff contact data and account values in publisher
responses were not copied. Page hashes identify only the copy retrieved.

| Source | Pin | Used for |
| --- | --- | --- |
| DB official SDK [`DBsecurities/dbsec-open-api`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb) | commit `564b5100…`; [`dbsec_sdk/auth.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/auth.py) blob `b83addb2…`; [`examples/dbsec_helper.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/dbsec_helper.py) blob `a00db7a5…`; [`examples/kr_stock_quote/kr_stock_inquire_price.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_price.py) blob `f717db2b…`; [`dbsec_sdk/client.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/client.py) blob `6000fa44…`; [`config.yaml.example`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/config.yaml.example) blob `f6204f13…` | token: form body `grant_type`, `appkey`, `appsecretkey`, `scope=oob`, default TLS verification, "JSON 으로 보내면 IGW00133"; response docstring `access_token`, `token_type: Bearer`, `expires_in: 86400`; "24시간 이내 재발급 시 서버는 기존 토큰(만료시간 동일)을 반환"; quote headers `cont_yn: N`, `cont_key: ""`; PRICE body `InputIscd1: "005930"`; errors as HTTP 403 (token family) or 500 with `rsp_cd`; one REST origin for production and demo |
| DB API guide, OAuth list (`/api/apis/public/api-list/cc55b867-…`) | sha256 `eeb775c8ecd70a5f…` (unchanged from the earlier ledger copy); token API last modified 2026-02-25 | form content type; 1 issue per minute; 24 h validity from issue; "유효기간 만료 전 토큰을 발급을 하는경우, 동일한 토큰이 발급됩니다. (만료기간도 동일)" |
| DB API guide, token TR detail (`/api/apis/guide/tr/9e3097ab-…`, `/api/apis/guide/tr/property/cd5b4c37-…`) | sha256 `240e6462703d702a…` / `a7d184619b8d4e84…` | request example is a form string; response example `access_token`, `scope: "oob"`, `token_type: "Bearer"`, `expires_in: 86400`; field table names `token` and `expire_in` (length 10) instead |
| DB API guide, PRICE TR detail (`/api/apis/guide/tr/d7f6a691-…`, `/api/apis/guide/tr/property/3be5fa4b-…`) | sha256 `6017533ab47fefef…` / `a16222751d181c84…` | request example `InputIscd1: "005930"`; field text "J(KRX 주식): (ex. 005930)", NJ/UJ need `N-`/`U-`; `cont_yn` Y/N; `mac_address` "제휴사인 경우 필수 세팅, 개인은 세팅 X"; 5 TPS; response example with root `rsp_cd: "00000"` and `Out` |
| [DB testbed-sample](https://openapi.dbsec.co.kr/testbed-sample) | sha256 `98916511920f961a…` | still URL-query credentials and `verify=False` (**not copied**); token example shows `scope: "login"`; quote `InputIscd1: "A005930"`, blank `cont_yn` |
| [Toss OpenAPI JSON](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | `info.version` **1.2.28**, sha256 `c5918961335ccd6b…` (unchanged from the earlier ledger copy) | `OAuth2TokenRequest` form (`grant_type`, `client_id`, `client_secret`); `OAuth2TokenResponse` required `access_token`, `token_type` enum `Bearer`, `expires_in` integer "토큰 만료까지 남은 초"; "client 당 유효한 access token 은 1 개입니다. 재발급 시 이전에 발급된 token 은 즉시 무효화됩니다."; 400/401/403 `OAuth2ErrorResponse`, 403 = IP not allow-listed, 429 `RateLimitExceeded` with `X-RateLimit-*`/`Retry-After`; `/api/v1/prices` `symbols` query, `ApiResponse` `result` array of `PriceResponse` (`symbol`, `timestamp` nullable, `lastPrice` decimal string, `currency`), no venue field, no account header |

## Decision

### DB

1. **Token request:** `POST https://openapi.dbsec.co.kr:8443/oauth2/token`,
   `content-type: application/x-www-form-urlencoded`, form body
   `grant_type=client_credentials`, `appkey`, `appsecretkey`, `scope=oob`,
   with TLS verification on. `authentication_requirements("db")` now
   records `token_request_format="form"`. `WireRequest` refuses any other
   shape, including the testbed's URL query and a JSON body.
2. **Token response:** exactly the API guide example's keys:
   - `access_token`: printable ASCII without spaces;
   - `scope`: `"oob"` (API guide example) or `"login"` (testbed example);
   - `token_type`: exactly `"Bearer"`;
   - `expires_in`: a JSON integer from 1 to 86400 (the guide's 24 h).

   Any other key fails closed, including an `rsp_cd`/`error` envelope and
   the field table's `token`/`expire_in` names. The SDK, the testbed and
   the guide example agree on `access_token`/`expires_in`; the field table
   is the outlier. The lease expires `expires_in` seconds after the
   transport-attested pre-write clock reading (ADR 0011).
3. **Environment (gate 2):** only the `live` label exists, and it names the
   origin, not the account type. A DB lease additionally requires
   `db_production_key_acknowledged=True`: the caller states that the app
   key is a production key. Without it, `TokenFailure.UNACKNOWLEDGED`.
4. **Re-issue (gate 3):** no absolute expiry is documented, and a re-issued
   token's remaining lifetime has no lower bound the client can know. So:
   - A DB lease also requires `db_no_prior_token_acknowledged=True`. The
     caller states that no unexpired token existed for this app key when
     the request was sent: a first issue, more than 24 h since the last
     issue, or after a revoke. Without it, `UNACKNOWLEDGED`.
   - Independently, every DB token that the process receives is remembered
     by SHA-256 digest (never the token), together with the send sequence
     that produced it. The record is kept even when that save is refused.
     A token returned again by a later send fails `TokenFailure.REISSUED`,
     whatever the caller acknowledges, across providers and profiles.
     Re-saving the same response is allowed. A record is dropped once its
     expiry is before a later send's attested start.
   - Both acknowledgements must be exact booleans. Passing either one for
     another broker is refused (`INVALID_RESPONSE`), as is
     `kis_expiry_timezone` for DB.
5. **Quote (corrected plan):** `POST /api/v1/quote/kr-stock/inquiry/price`
   with headers `content-type: application/json; charset=utf-8`,
   `cont_yn: N`, `cont_key: ""` and the bearer token. The body is
   `{"In":{"InputCondMrktDivCode":"J","InputIscd1":"<6 digits>"}}`.
   - The guide's PRICE example, its field description and the SDK all use
     the bare code. The older testbed's `A005930` and blank `cont_yn` are
     replaced.
   - `mac_address` is for partner apps only, so it is not sent. Partner
     use is unsupported.
   - NXT and integrated quotes (`NJ`/`UJ`) are not offered.

### Toss

1. **Token request:** `POST https://openapi.tossinvest.com/oauth2/token`,
   form body `grant_type=client_credentials`, `client_id`, `client_secret`,
   and no scope.
2. **Token response:** exactly `access_token` (printable ASCII, no spaces),
   `token_type` exactly `"Bearer"` and `expires_in` as a JSON integer from
   1 s to the library's 7-day sanity bound. The schema does not forbid
   other keys, but rejecting them is library policy, so an OAuth error or
   BFF envelope cannot pass. The lifetime is anchored as in ADR 0011.
3. **One token per client (gate 4).** Within one process:
   - **Single flight per client:** Toss token sends are serialised per
     client id digest, not per (provider, identity). A second send for the
     same client, from any provider or profile, fails `TOKEN_IN_FLIGHT`
     before connecting.
   - **Latest send:** when a Toss token send starts writing, it becomes the
     latest for its client, even if it then fails. A write that may have
     reached Toss may have issued a new token. A send refused before the
     write (connect or TLS failure) changes nothing.
   - **Quote use:** only the lease from that latest send can build or send
     a Toss quote. This is checked in `build_quote_request`, before
     connecting and again after TLS, before the write. Otherwise
     `TOKEN_UNAVAILABLE`. A lease put into the cache by hand has no send
     sequence, so it can never be used for Toss.
   - **No quote write after a newer token write:** the final latest-send
     check and the claim of the quote write happen in one critical section
     of the process-wide token lock. While a Toss quote for a client is being
     written, a Toss token send for that client fails `QUOTE_IN_FLIGHT`
     before it writes anything (`NOT_SENT`); the claim is released when the
     quote write returns or fails. So no Toss quote starts writing after a
     newer token write started, in this process. No network I/O happens
     under the lock, nothing waits and nothing is retried (ChatGPT review of
     PR #30, M1). How Toss orders two requests that are both in flight is
     not documented.
   - **Saving:** a response from an older send cannot be saved
     (`TokenFailure.SUPERSEDED`).
   - **Not covered:** a refusal of a second provider or profile for the same
     client was considered and not chosen. It would not cover other
     processes either, and the latest-send rule already makes the conflict
     visible in-process as a static error rather than a silently dead token.
4. **Quote:** `GET /api/v1/prices?symbols=<code>` with only the bearer
   header: no account header and no body. 403 (IP not allow-listed) is
   `FORBIDDEN` and 429 is `RATE_LIMITED`. Neither is retried, and the
   rate-limit headers are not acted on.

### Both

- **Encoding guard:** a lone surrogate in a credential used to make the
  form builder raise `UnicodeEncodeError`, whose `.object` held the whole
  secret. This already affected LS. It now fails with a static
  `INVALID_REQUEST` that has no exception chain.
- **No new public API:** there is no `fetch_ticker`, no automatic token
  issue, refresh, revoke or retry, and network stays disabled by default.
  A `WireResponse` is never promoted to a `Ticker` automatically.
  `decode_offline_quote_response` stays the test-only seam.

## Consequences and limits

- **Not visible to the library:**
  - another process, machine or the official SDK sharing a DB app key or a
    Toss client;
  - whether a DB app key is production or demo;
  - whether DB reported a re-issued token's remaining time or its full
    lifetime.

  The acknowledgements make these assumptions explicit; they do not verify
  them. Two processes using one Toss client will still invalidate each
  other's tokens.
- **Unverified at the gateways:**
  - acceptance of the bare DB `InputIscd1` and `cont_yn: N`;
  - which DB token response form is real (scope value, field names);
  - DB's `rsp_cd` universe;
  - Toss acceptance from a given IP and Toss rate-limit buckets;
  - the meaning of `timestamp`, and redistribution rights for either
    broker's data.
- **DB errors:** DB reports errors as HTTP 403 or 500 with an `rsp_cd`
  (`IGW…`). The transport classifies them by status only. The SDK retries
  `IGW00201` (rate limit) and re-issues on `IGW00121/00123` (token
  rejected); neither is copied. DB issues at most one token per minute; the
  library never retries a token request.
- **Decoder findings** (crates are owned by another stream, so they are
  recorded here and were not changed):
  - The DB decoder treats a missing root `rsp_cd` as success
    (`StatusSpec` optional; the Rust test `{"Out":{"Prpr":"10"}}` decodes).
    The PRICE response example always carries `rsp_cd: "00000"`, and
    AGENTS.md forbids default success for a missing upstream status. The
    LS decoder already requires its `rsp_cd` (ADR 0010). Making DB's
    `rsp_cd` required is a **blocking gate before any public DB quote**
    (ChatGPT review of PR #30, L1); it is tracked as its own follow-up.
  - The DB decoder does not map the documented `AcmlVol` (volume). That is
    not a safety issue.
  - The Toss decoder does not reject a root `error` next to `result`. The
    spec says the two never co-occur, so this is low risk.
  - Otherwise the Toss decoder matches `PriceResponse`: exact symbol, no
    duplicates, `currency` KRW, `lastPrice` string, nullable string
    `timestamp`, no venue.
- **Diagnostics:** `_diagnostics.gateway_status` reads `error` as a string
  code. A Toss BFF error has `error` as an object, so its code is not
  extracted. `_diagnostics.py` is unchanged.
- **Meritz:** still blocked for token and quote (every error is HTTP 500, a
  MAC is mandatory), and covered by a test.
- **Tests:** `tests/test_db_wire.py`, `tests/test_toss_wire.py` and
  `tests/test_form_credential_encoding.py`. All use mocked HTTPS and
  synthetic credentials and tokens. The quote bodies are the publishers'
  example payloads, decoded end to end through the existing native decoder.
