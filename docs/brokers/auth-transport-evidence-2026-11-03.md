# Issue #17: authentication/transport evidence audit

Checked 2026-11-03 (Asia/Seoul). This is a **public-document retrieval audit**,
not real-account/paper-account verification. No credential, OAuth, quote or order
request was executed. The existing offline planner and decoder mappings are not
changed by this audit. The new fake layer cannot establish live API correctness.

## Retrieval quality

GitHub sources below are commit-pinned. Other pages have no immutable revision;
the browser returned cached/indexed views, sometimes older than search snippets.
Do not equate retrieval date with publisher revision date or label these views
as the latest deployed contract. Conflicts/failures are retained below rather
than silently replacing earlier evidence. No third-party implementation is used
as authority. No publisher token examples or sample account values are copied.

## KIS

Pinned publisher repository: `3a9be59a3ed8745720dc3aa9d584bdf3b7830362`.
[Current-price sample](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_price/inquire_price.py)
(blob `bb6ab22df57b1a5d14fab861f6c1d29272872a84`) uses uppercase
`FID_COND_MRKT_DIV_CODE` and `FID_INPUT_ISCD`, with `FHKST01010100` for real/demo.
Its parameter comments distinguish J/KRX, NX/NXT and UN/integrated.
This is source evidence only, not permission to enable new venues. The existing
legacy-derived lowercase planner is unchanged. Gateway case equivalence,
real/paper behavior, session provenance and token lifecycle still need evidence.

## Kiwoom REST

Pinned publisher repository: `953e5dbff123f437ab4d11a78a95191a685eb51f`.
[Auth source](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/kiwoom/core/auth.py)
(blob `9026aae207b7e2963c40f06e5e9a2f287a589d28`) separates real/demo origins;
POST token JSON uses grant_type/appkey/secretkey. Its cache considers profile,
credential identity and expiry. These observations motivate scope separation,
NOT copying automatic refresh, source logging, defaults or credential storage.
The [official quote example](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_info.py)
(blob `c39741c73f0f8bdbc47694de24abf3cbaaf1d402`) was confirmed at the same
publisher commit (ka10001, /api/dostk/stkinfo). This pins the sample content,
not the deployed API behavior.
Signed prices, KRX/NXT/SOR symbol semantics and full status/continuation validation
remain unverified by this change.

## LS

[Guide](https://openapi.ls-sec.co.kr/howto-use) retrieved as an older cached view:
separate paper credentials select the environment; its token snippet combines
a form content-type with `params=` and disables TLS verification. Do not copy it
or infer safe body encoding from the content-type alone. Its expiry wording is
not implemented as a universal token lifetime.
[Publisher samples](https://openapi.ls-sec.co.kr/howto-sample) show POST
/stock/market-data with tr_cd and named input/output blocks for t1301/t1101.
These do not establish t1102. The retrieved [guide index](https://openapi.ls-sec.co.kr/apiservice)
did not expose a usable complete t1102 contract; a newer search view and the
older retrieved page differ. Existing GET/STKCURR onboarding data must not be
promoted to a live adapter. Real t1102 and safe token exchange remain blocked.

## DB

[Official sample](https://openapi.dbsec.co.kr/testbed-sample) still contains token
credentials in the URL query and TLS verification disabled in the retrieved view.
The [API guide](https://openapi.dbsec.co.kr/apiservice) returned a navigation shell
without populated endpoint details. This does not prove no safe contract exists;
it means this audit did not verify one. Obtain a complete publisher-confirmed
non-URL credential contract and TLS-verified exchange before live implementation.
Keep the old unsafe_query_sample_only metadata and unsupported paper gate.

## Toss

[Canonical JSON](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json)
was retrieved with OpenAPI 3.1.0 / info.version **1.2.13**, whereas the earlier
ledger recorded **1.2.28**. Treat this as a cache/revision discrepancy, NOT a
publisher downgrade or a reason to overwrite the prior mapping. Retrieved
content documents OAuth2 client credentials, bearer-only market data without
X-Tossinvest-Account, GET /api/v1/prices with symbols, and a 429 response.
No new numeric rate limit, single-token invalidation policy, market provenance
or timestamp conversion is asserted. Reconcile a fresh complete version and
client token rotation rules before any real adapter is enabled.

## Meritz

[Python sample](https://openapi.imeritz.com/samplecode-py) and
[guide](https://openapi.imeritz.com/howto-use) were found in the official search
index; snippets identify authorization and mac_address. Full page retrieval
failed in this audit. Preserve earlier evidence as historical rather than claim
all fields were reverified. Never auto-detect a MAC. Obtain readable current
quote-specific rsp_cd, token lifecycle, approved device context and J/NJ/TJ
semantics before live work. Order response codes are not quote success codes.

## What the fake implementation proves / does not prove

It tests library-owned scope keys, explicit synthetic leases, context matching,
HTTP failure classes, simulated deadlines, zero replay, and safe error text.
A fixture outcome is caller-supplied simulation metadata, not wire-status
attestation. The existing Rust decoder remains the JSON validation boundary;
its optional statuses are intentionally not promoted to a live success rule.
All six brokers remain unverified for actual authenticated ticker use.

Issue #17 stays open for complete official contracts, safe real credential
providers/transports, source/session validation and separately authorized tests.
This PR neither changes capability flags nor implements public fetch_ticker.
