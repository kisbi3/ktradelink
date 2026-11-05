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
| **DB** | Credential identity only; token/quote WireRequests blocked | `testbed-sample` still puts credentials in the URL query and disables TLS; **not copied**. Rechecked 2026-11-05: the official SDK [`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb) sends them in a form body with TLS verification on. The API guide limits token issuance to 1 per minute and returns the **same token and expiry** when re-issued before expiry. Live and demo share one REST origin (the app key decides). Gateway acceptance unverified. |
| **Toss** | Credential identity only; token/quote WireRequests blocked | Rechecked 2026-11-05: OpenAPI `info.version` **1.2.28** (the earlier 1.2.13 view appears to have been stale). Form-encoded client-credentials token, `token_type: Bearer`, `expires_in` seconds; **one valid token per client — re-issuing invalidates the previous one immediately**; 403 means the caller IP is not allow-listed; 429 carries `X-RateLimit-*`/`Retry-After`. `GET /api/v1/prices` needs no `X-Tossinvest-Account` header and its rows carry **no venue field**. |
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
not copied. Every KIS/Kiwoom/LS path remains candidate-only and HTTPS is
disabled by default. DB, Toss and Meritz still have no executable token route.

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

Design gates these observations add before any of the four is enabled:

- **Toss:** a client's tokens are shared state on the provider side. Two
  profiles, providers or processes holding the same client credentials will
  invalidate each other's tokens; per-profile cache separation cannot prevent it.
- **DB:** environment cannot be checked from the origin, so a mislabelled
  live/demo app key is undetectable by the transport. A re-issued token keeps
  its original expiry, so `now + expires_in` must not be assumed for it.
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
