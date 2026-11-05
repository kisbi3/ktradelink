# Six-broker quote request and authentication evidence ledger

**Researched 2026-11-02. Status: publisher-documented OFFLINE templates,
not a working authenticated broker integration.** None of the six has been
called using a real account, token, TLS session or recorded live fixture.
Do not equate an API guide/example with confirmed account entitlement.

## Side-by-side quote request templates

| Broker | Quote verb, path | Public request fields, **not secret credentials** | Auth prerequisite | Environment and evidence |
| --- | --- | --- | --- | --- |
| KIS | GET `/uapi/domestic-stock/v1/quotations/inquire-price` | `fid_cond_mrkt_div_code=J`, `fid_input_iscd=005930`; header `tr_id=FHKST01010100` | Bearer, `appkey`, `appsecret` (quote headers) | Official [KIS current-price sample](https://github.com/koreainvestment/open-trading-api/blob/main/legacy/rest/current_price_samle.py) and [config](https://github.com/koreainvestment/open-trading-api/blob/main/kis_devlp.yaml). Live `https://openapi.koreainvestment.com:9443`; paper `https://openapivts.koreainvestment.com:29443`. |
| Kiwoom REST | POST `/api/dostk/stkinfo` | JSON `{"stk_cd":"005930"}`; header `api-id=ka10001` | Bearer | Official [ka10001 publisher example](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_info.py) and [auth client](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/kiwoom/core/auth.py): live `https://api.kiwoom.com`, demo `https://mockapi.kiwoom.com`. |
| LS | POST `/stock/market-data` (**t1102**) | JSON `{"t1102InBlock":{"shcode":"005930","exchgubun":"K"}}`; headers `tr_cd=t1102`, `tr_cont=N`, blank `tr_cont_key` and `mac_address` | Bearer | [LS API guide t1102 REST detail](https://openapi.ls-sec.co.kr/apiservice) (retrieved 2026-11-05, see [ledger](live-auth-transport-gates-2026-11-05.md)): `https://openapi.ls-sec.co.kr:8080`. Replaced the onboarding `GET`/`tr_id=STKCURR` demo (ADR 0010). Unknown `exchgubun` becomes KRX on the LS side, so `K` is always explicit. Gateway acceptance unverified. |
| DB | POST `/api/v1/quote/kr-stock/inquiry/price` | JSON `{"In":{"InputCondMrktDivCode":"J","InputIscd1":"A005930"}}`; sample `cont_yn` and `cont_key` blank | Bearer | [Official DB PRICE sample](https://openapi.dbsec.co.kr/testbed-sample): `https://openapi.dbsec.co.kr:8443`. Its `verify=False` is **unsafe and MUST NOT be copied**. |
| Toss | GET `/api/v1/prices` | Query `symbols=005930` (single-symbol here) | Bearer, **no account header** for market data | [Canonical OpenAPI 3.1 v1.2.28](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json), server `https://openapi.tossinvest.com`. Supports up to 200 comma-separated requested symbols; only one in this private planner. |
| Meritz | GET `/market/v1/prices` | `mrkt_div_code=J`, `iscd=005930` | Bearer + `mac_address` header, required in official sample | [Official Meritz Python sample](https://openapi.imeritz.com/samplecode-py): `https://openapi.imeritz.com:9443`. `mac_address` value must be supplied by a future credential context, not probed or logged. |

All examples and paths above are **publisher-source evidence**, not tested
contracts for live entitlement, market venue, TR applicability, or quote time.
The `KRX` argument is **caller-provided context**, never a promise the broker
returned a KRX-only price. Alphanumeric symbols are a general value-model
feature, not proof every provider query accepts them.

### Authentication source taxonomy (metadata only)

| Broker | Token endpoint | Publisher documented token request | Implementation here |
| --- | --- | --- | --- |
| KIS | POST `/oauth2/tokenP` | JSON `grant_type=client_credentials`, `appkey`, `appsecret` ([KIS](https://github.com/koreainvestment/open-trading-api/blob/main/examples_user/kis_auth.py)) | **Not executed.** Required credential field names only. |
| Kiwoom | POST `/oauth2/token` | JSON `grant_type`, `appkey`, `secretkey` ([official auth.py](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/kiwoom/core/auth.py)) | Not executed |
| LS | POST `/oauth2/token` | Form `grant_type`, `appkey`, `appsecretkey`, `scope=oob` ([guide](https://openapi.ls-sec.co.kr/howto-use)) | Not executed |
| DB | POST `/oauth2/token` | Official sample passes `appkey`, `appsecretkey`, `scope=oob` **in URL query** ([example](https://openapi.dbsec.co.kr/testbed-sample)); sample disables TLS verification | **Intentionally blocked:** safe, standards-verified credential transfer not established |
| Toss | POST `/oauth2/token` | Form `grant_type`, `client_id`, `client_secret` ([canonical OpenAPI](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json)) | Not executed; documented OAuth token replacement invalidates earlier token |
| Meritz | POST `/oauth2/token` | Form `grant_type`, `client_id`, `client_secret`, `scope=login` ([official sample](https://openapi.imeritz.com/samplecode-py)) | Not executed |

Auth token lifecycle, cache/refresh/revocation, account entitlement,
credential persistence, TLS client, retries, and real-time WebSocket are
**unimplemented**. No private keys or token samples are stored in this repo.
Do not blindly follow provider sample snippets that print tokens, disable TLS
validation or put passwords in URLs.

## Status of work after PR #15

- Rust `ktradelink-decoders` has six **offline response-shaped candidates**.
- This work adds a matching six-provider **nonsecret request planner** plus
  **auth requirements metadata**; it does not change Rust decoder behavior.
- Never say `fetch_ticker` is implemented. No real/paper account,
  authenticated call, actual ticker prices, broker sign conversion, timestamps,
  rate-limit measurements or order execution has been verified.
- Specific remaining questions: KIS/other venue-specific quote provenance,
  Kiwoom signed price strings, LS t1102 gateway acceptance, DB safe OAuth
  transport and TLS, Toss per-market session/source timestamp, Meritz exact
  success codes and mandatory device/MAC policy.
- Related review/roadmap: [Issue #2](https://github.com/kisbi3/ktradelink/issues/2),
  [Issue #5](https://github.com/kisbi3/ktradelink/issues/5),
  [Issue #12](https://github.com/kisbi3/ktradelink/issues/12),
  [Issue #14](https://github.com/kisbi3/ktradelink/issues/14).
- Shinhan i indi remains a separate question in draft PR #6, not seventh
  executable HTTP planner.
