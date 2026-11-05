# Six-broker auth/HTTPS contract gates — 2026-11-05 KST

This is a publisher-example audit plus **library design**, not proof of a
production endpoint, eligibility, rate limit, exchange venue or quote meaning.
No real token, HTTP request, account access or order was executed. Versioned
GitHub links below were inspected with their fixed SHA; the other references
are carried forward as **unverified pending** from previous audits. Current
publisher deployment and credential requirements can differ from examples.

| Broker | Current design state | Known evidence and unresolved gate |
| --- | --- | --- |
| **KIS** | Candidate JSON token POST and quote request assembly; disabled HTTPS sender only | Official pinned sample confirms `/oauth2/tokenP`, `client_credentials`, `appkey`, `appsecret`, `access_token`, `access_token_token_expired` (naive string; timezone **not confirmed** by the sample). Quote planner's lowercase `fid_*` differs from newer official uppercase `FID_*`; no actual gateway validation. Live/paper source/session still unverified. |
| **Kiwoom REST** | Candidate JSON token POST and quote assembly; disabled HTTPS sender only | Official pinned auth source confirms `/oauth2/token`, `grant_type`, `appkey`, `secretkey`, bearer/token and `expires_dt` parsed with KST. Actual `ka10001` status, signed quote prices, KRX/NXT/SOR and continuity remain unverified. |
| **LS** | Credential identity only; actual WireRequest blocked | Earlier official [guide](https://openapi.ls-sec.co.kr/howto-use) and [samples](https://openapi.ls-sec.co.kr/howto-sample) include an onboarding route, **not** a fully verified native t1102 token/quote contract. Do not inherit their TLS-disabled example. |
| **DB** | Credential identity only; token/quote WireRequests blocked | Earlier [official sample](https://openapi.dbsec.co.kr/testbed-sample) had URL-query credentials and disabled TLS. These behaviors are **not copied**; publisher-confirmed safe authentication is a gate. |
| **Toss** | Credential identity only; token/quote WireRequests blocked | Earlier [OpenAPI JSON](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) retrieval conflicted between info.version 1.2.13 and 1.2.28. Verify current version, token rotation/expiration, 429 and market/time provenance. No X-Tossinvest-Account header assumed for quotes. |
| **Meritz** | Credential identity only; token/quote WireRequests blocked | Earlier [official Python sample](https://openapi.imeritz.com/samplecode-py) search showed `mac_address`. Must be supplied by an approved user/device source, never auto-detected; quote-specific rsp_cd and J/NJ/TJ remain unknown. |

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
not copied. Every KIS/Kiwoom path remains candidate-only and HTTPS is disabled
by default. The other four still have no verified executable native token route.

## Before any public broker support

Confirm current endpoint and exact request fields for each broker and market,
allowed accounts, client token lifetimes/rotation, response status completeness,
TLS and error semantics, symbol/venue/environment provenance, session time,
rate limits and redistribution permissions. Require explicit user approval for
any credentials, broker network call, account or order; never run those in CI.
Preserve six-broker parallel capability tracking rather than pretending a
candidate backend is fully supported.
