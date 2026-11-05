# Six-broker auth/HTTPS contract gates — 2026-11-05 KST

This is a publisher-example audit plus **library design**, not proof of a
production endpoint, eligibility, rate limit, exchange venue or quote meaning.
No real token, HTTP request, account access or order was executed. Versioned
GitHub links below were inspected with their fixed SHA. The LS, DB, Toss and
Meritz pages were re-fetched on 2026-11-05 (see the recheck section); they are
still publisher documentation, not gateway verification. Current publisher
deployment and credential requirements can differ from examples.

| Broker | Current design state | Known evidence and unresolved gate |
| --- | --- | --- |
| **KIS** | Candidate JSON token POST and quote request assembly; disabled HTTPS sender only | Official pinned sample confirms `/oauth2/tokenP`, `client_credentials`, `appkey`, `appsecret`, `access_token`, `access_token_token_expired` (naive string; timezone **not confirmed** by the sample). Quote planner's lowercase `fid_*` differs from newer official uppercase `FID_*`; no actual gateway validation. **Header differences from the pinned sample (unverified, not copied):** the token request sends `content-type: application/json;charset=UTF-8` (the Kiwoom sample's value), whereas `kis_auth.py` L61-66 uses `Content-Type: application/json`, `Accept: text/plain`, `charset: UTF-8` and a `User-Agent`; the quote request omits `custtype` (sample L458 sets `"P"` for individuals, `"B"` for partners) and `tr_cont` (L459). Live/paper source/session still unverified. |
| **Kiwoom REST** | Candidate JSON token POST and quote assembly; disabled HTTPS sender only | Official pinned auth source confirms `/oauth2/token`, `grant_type`, `appkey`, `secretkey`, bearer/token and `expires_dt` parsed with KST. Actual `ka10001` status, signed quote prices, KRX/NXT/SOR and continuity remain unverified. |
| **LS** | Candidate form token POST and t1102 quote assembly (ADR 0010); disabled HTTPS sender only | Rechecked 2026-11-05 (see below): the current guide's token example uses a form body without disabling TLS, and the API guide now publishes a complete **t1102** REST contract (`POST /stock/market-data`, `tr_cd: t1102`, `t1102InBlock` with `shcode` and `exchgubun` K/N/U). Since PR #25 the planner sends that t1102 request with `exchgubun: K`, not the onboarding `GET` + `tr_id: STKCURR` route. Token lifetime is `expire_in` (type String, length 10) in the field table but `expires_in` (JSON number) in the example. |
| **DB** | Candidate form token POST and PRICE quote assembly (ADR 0015); disabled HTTPS sender only | `testbed-sample` still puts credentials in the URL query and disables TLS; **not copied**. The official SDK [`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb) and the API guide token detail send a form body with TLS verification on; that is the only shape built. The API guide limits token issuance to 1 per minute and returns the **same token and expiry** when re-issued before expiry. Live and demo share one REST origin (the app key decides). A lease therefore needs two caller acknowledgements (production key; no unexpired prior token), and a token seen again in-process fails `REISSUED`. The quote now sends the guide's bare `InputIscd1` and `cont_yn: N` (the testbed had `A005930` and blank). Gateway acceptance unverified. |
| **Toss** | Candidate form token POST and prices quote assembly (ADR 0015); disabled HTTPS sender only | OpenAPI `info.version` **1.2.28** (the earlier 1.2.13 view appears to have been stale). Form-encoded client-credentials token, `token_type: Bearer`, `expires_in` seconds; **one valid token per client — re-issuing invalidates the previous one immediately**. In-process: token sends are single-flight per client id, and only the lease from the latest send that started writing is usable for a quote. Other processes are not visible. 403 means the caller IP is not allow-listed; 429 carries `X-RateLimit-*`/`Retry-After` (not acted on, never retried). `GET /api/v1/prices` needs no `X-Tossinvest-Account` header and its rows carry **no venue field**. |
| **Meritz** | Credential identity only; token/quote WireRequests blocked | Rechecked 2026-11-05: form token with `scope=login`, `expires_in` seconds. **Every error is HTTP 500** with `rsp_cd`/`rsp_msg`; success `rsp_cd` differs by API family. Quote `mrkt_div_code` is `J` (KRX), `NJ` (NXT), `TJ` (integrated); quote `iscd` is 6 digits. `mac_address` (12 uppercase hex) is required; the publisher sample auto-detects it with `uuid.getnode()`, which must **not** be copied. |

## Pinned directly checked publisher inputs

- **KIS** official repository SHA
  `3a9be59a3ed8745720dc3aa9d584bdf3b7830362`,
  [`examples_user/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_user/kis_auth.py),
  Git blob `0e722d6f3253033efe3cf2b99845397b2b329655`;
  current price [`inquire_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_price/inquire_price.py),
  Git blob `bb6ab22df57b1a5d14fab861f6c1d29272872a84`.
- **Kiwoom REST** official repository SHA
  `953e5dbff123f437ab4d11a78a95191a685eb51f`,
  [`kiwoom/core/auth.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/kiwoom/core/auth.py),
  Git blob `9026aae207b7e2963c40f06e5e9a2f287a589d28`;
  [`ka10001 quote example`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_info.py),
  Git blob `c39741c73f0f8bdbc47694de24abf3cbaaf1d402`.

These are official examples, **not** authorized response fixtures. Rechecking
KIS `save_token` / `_read_token_file` shows naive `datetime.strptime` and local
`datetime.today()` comparisons, not a timezone declaration. The parser no
longer assumes KST for KIS: explicit caller-provided fixed-offset context is
required, and the true provider time basis remains unverified. Kiwoom's pinned
auth source explicitly assigns KST when parsing expiry. Neither observation
proves actual live/paper behavior. Strict token_type and Kiwoom return_code
requirements are fail-closed library policy; permissive upstream defaults are
not copied. Every KIS/Kiwoom/LS/DB/Toss path remains candidate-only and HTTPS
is disabled by default. Meritz still has no executable token or quote route.

## Recheck of the four non-GitHub publishers — 2026-11-05 02:31–02:36 UTC

These pages were re-fetched after the environment's network policy was
widened. Public pages have no immutable revision, so the SHA-256 prefixes only
identify the copy retrieved at that time; Meritz pages vary by a few bytes per
request. Only public documentation was fetched: no credential, token, quote,
account or order request was sent. Sample tokens, account values and staff
contact data present in some publisher responses are deliberately not copied.

| Source | Retrieved copy | Observations used above |
| --- | --- | --- |
| [Toss OpenAPI JSON](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | sha256 `c5918961335ccd6b…` | `openapi 3.1.0`, `info.version 1.2.28`; `/oauth2/token` and `/api/v1/prices` schemas, `RateLimitExceeded` response |
| [LS howto-use](https://openapi.ls-sec.co.kr/howto-use) | sha256 `1ac67684c850e15a…` | token example: `data=` form body, no `verify=False`; onboarding `GET /stock/market-data` with `tr_id: STKCURR` |
| LS API guide detail for t1102 (`/guide/api/<tr-id>?type=rest`, linked from [apiservice](https://openapi.ls-sec.co.kr/apiservice)) | sha256 `42712ce969a8a480…` | `POST :8080/stock/market-data`, JSON, `transactionPerSec 10`; headers `content-type`, `authorization`, `tr_cd`, `tr_cont`, `tr_cont_key`, `mac_address` ("법인인 경우 필수"); `exchgubun` K/N/U, "그외 입력값은 KRX로 처리"; `t1102OutBlock` |
| LS API guide detail for token | sha256 `4acff92cdcdfd551…` | `POST :8080/oauth2/token`, form, `grant_type`, `appkey`, `appsecretkey`, `scope=oob`; field table `expire_in` (String, length 10) vs example `expires_in` (number) |
| [DB testbed-sample](https://openapi.dbsec.co.kr/testbed-sample) | sha256 `e793a892d99c3697…` | token still via URL query with `verify=False`; quote `POST /api/v1/quote/kr-stock/inquiry/price`, `{"In":{...}}`, `rsp_cd "00000"` |
| DB API guide list (`/api/apis/public/api-list/<group>`) | sha256 `eeb775c8ecd70a5f…` | token: form content type, 1 issue per minute, 24-hour validity, same token if re-issued before expiry (last modified 2026-02-25) |
| [DB official SDK](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb) | commit `564b5100…` (2026-08-20); `dbsec_sdk/auth.py` blob `b83addb2b8007ae12946eab1ae0395ceb3eca7de`; `examples/dbsec_helper.py` blob `a00db7a5a6104f7b4029c0b206231ff389b97f6b` | form body, default TLS verification, "JSON 으로 보내면 IGW00133"; `config.yaml.example`: one REST origin for production and demo |
| [Meritz samplecode-py](https://openapi.imeritz.com/samplecode-py) / [howto-use](https://openapi.imeritz.com/howto-use) | sha256 `f04eda2bf5149532…` / `09697fb15c771de5…` | form token with `scope=login`; all errors HTTP 500 + `rsp_cd`; sample `OK_CODES`; J/NJ/TJ; `mac_address` via `uuid.getnode()` |

## DB and Toss recheck for ADR 0015 — 2026-11-05 06:14–06:17 UTC

Public documentation only; nothing was sent to either gateway. Sample tokens,
the masked example credentials and staff contact data in the DB API guide
responses were not copied. The DB testbed page hash differs from the
02:31 UTC copy; the token and quote observations on it are unchanged.

| Source | Retrieved copy | Observations used by ADR 0015 |
| --- | --- | --- |
| DB API guide OAuth list (`/api/apis/public/api-list/cc55b867-…`) | sha256 `eeb775c8ecd70a5f…` (same as above) | token API last modified 2026-02-25; re-issue before expiry returns the same token "(만료기간도 동일)"; revoke first for a new one |
| DB API guide token TR detail (`/api/apis/guide/tr/9e3097ab-…`) and field table (`/api/apis/guide/tr/property/cd5b4c37-…`) | sha256 `240e6462703d702a…` / `a7d184619b8d4e84…` | form request example; response example `access_token`, `scope: "oob"`, `token_type: "Bearer"`, `expires_in: 86400`; field table instead names `token`, `expire_in` (length 10), `scope`, `token_type` |
| DB API guide PRICE TR detail (`/api/apis/guide/tr/d7f6a691-…`) and field table (`/api/apis/guide/tr/property/3be5fa4b-…`) | sha256 `6017533ab47fefef…` / `a16222751d181c84…` | request example `InputIscd1: "005930"`; "J(KRX 주식): (ex. 005930)", NJ `N-005930`, UJ `U-005930`; `cont_yn` Y/N; `mac_address` partner-only ("개인은 세팅 X"); 5 TPS; response example root `rsp_cd: "00000"` + `Out` |
| [DB testbed-sample](https://openapi.dbsec.co.kr/testbed-sample) | sha256 `98916511920f961a…` | URL-query token with `verify=False` (not copied); token example `scope: "login"`; quote `A005930`, blank `cont_yn` |
| DB SDK at `564b5100…`: [`examples/kr_stock_quote/kr_stock_inquire_price.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_price.py), [`dbsec_sdk/client.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/client.py), [`config.yaml.example`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/config.yaml.example) | blobs `f717db2b3ce2322d898785f850ca6f7c77afcc03`, `6000fa447765e6fc5822e6c8fe09ef92ead8d462`, `f6204f1399f2f080c11f28364444b40b7868ef96`; `auth.py` and `dbsec_helper.py` re-fetched with the blobs listed above | quote body `InputIscd1: "005930"`; headers `cont_yn: "N"`, `cont_key: ""`; errors arrive as HTTP 403 (token family) or 500 with `IGW…` `rsp_cd`; the SDK retries `IGW00201` and re-issues on `IGW00121/00123` (neither copied) |
| [Toss OpenAPI JSON](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | `info.version` 1.2.28, sha256 `c5918961335ccd6b…` (same as above) | `OAuth2TokenRequest`/`OAuth2TokenResponse`/`OAuth2ErrorResponse` schemas; `PriceResponse`; `ApiResponse` "`result` 와 `error` 는 동시에 나타나지 않습니다" |

Design gates these observations add before any of the four is enabled. DB and
Toss are addressed by ADR 0015 within one process; the cross-process parts
remain open:

- **Toss:** a client's tokens are shared state on the provider side. Two
  profiles, providers or processes holding the same client credentials will
  invalidate each other's tokens; per-profile cache separation cannot prevent
  it. *ADR 0015:* single-flight per client id and "latest send only" leases
  in-process; other processes remain invisible.
- **DB:** environment cannot be checked from the origin, so a mislabelled
  live/demo app key is undetectable by the transport. A re-issued token keeps
  its original expiry, so `now + expires_in` must not be assumed for it.
  *ADR 0015:* explicit caller acknowledgements for both, and an in-process
  `REISSUED` refusal; neither is verification.
- **Meritz:** the transport's status-only classification (500 → `SERVER`)
  cannot tell authentication, request and server errors apart; broker-specific
  `rsp_cd` interpretation is required, especially before any order path.
- **LS:** do not infer which token expiry field name is authoritative; an
  invalid `exchgubun` silently becomes KRX, so the venue must always be sent
  explicitly. The relative lifetime is counted from the transport-attested
  pre-write time (ADR 0011). Whether re-issuing invalidates the previous token
  is undocumented; single-flight sends and send ordering keep the newest one.

## Before any public broker support

Confirm current endpoint and exact request fields for each broker and market,
allowed accounts, client token lifetimes/rotation, response status completeness,
TLS and error semantics, symbol/venue/environment provenance, session time,
rate limits and redistribution permissions. Require explicit user approval for
any credentials, broker network call, account or order; never run those in CI.
Preserve six-broker parallel capability tracking rather than pretending a
candidate backend is fully supported.
