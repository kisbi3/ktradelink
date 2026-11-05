# Six-broker capability inventory (domestic equity, REST) — 2026-11-05

- **Scope:** KIS, Kiwoom REST, LS, DB, Toss, Meritz; domestic equity; REST
  routes (WebSocket only as an availability flag).
- **Retrieved:** 2026-11-05, 06:50–07:00 UTC (exact times per source below).
  GitHub sources are pinned by commit SHA and Git blob SHA (`git ls-tree`).
- **Status: shallow inventory, not field-level verified, nothing
  live-verified, no broker API request sent.** Only public documentation
  pages, public JSON documents and public Git repositories were fetched. No
  credential, token, quote, account or order request was made. Sample
  tokens, account values, staff contacts and `writer` fields present in some
  publisher responses were not copied.
- A listed route is **feature discovery** only. It does not establish
  entitlement, venue, session, units, response status semantics, rate limit
  in practice, paper/live behaviour or redistribution rights, and it does not
  change any `capability-matrix-v0.1.json` state.
- Candles are being audited separately; this file only points to that audit.

**Evidence levels:** `EX` publisher example code · `FT` publisher field
table / machine-readable API guide · `SDK` official SDK code or SDK docs ·
`OAS` OpenAPI/AsyncAPI schema · `PR` publisher prose (guide text, notice)
without a field table · `NF` not found (where looked is stated).
Source IDs (`K1`, `W1`, `L1`, …) resolve in the per-broker source tables.

## Capability × broker table

| # | Capability | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Current price / ticker | `FHKST01010100` GET `/uapi/domestic-stock/v1/quotations/inquire-price` · EX · see [quote ledger](six-broker-quote-request-auth.md) | `ka10001` POST `/api/dostk/stkinfo` · EX · see [quote ledger](six-broker-quote-request-auth.md) | `t1102` POST `/stock/market-data` · FT · see [quote ledger](six-broker-quote-request-auth.md), ADR 0010 | `PRICE` POST `/api/v1/quote/kr-stock/inquiry/price` · EX+SDK · [quote ledger](six-broker-quote-request-auth.md), D3 | GET `/api/v1/prices` · OAS · [quote ledger](six-broker-quote-request-auth.md), T1 | `ohhts_1001_001r` GET `/market/v1/prices` · EX+FT · [quote ledger](six-broker-quote-request-auth.md), M1 |
| 2 | Order book (호가) | `FHKST01010200` GET `…/quotations/inquire-asking-price-exp-ccn` · EX · see OB | `ka10004` POST `/api/dostk/mrkcond` · EX+FT · see OB | `t1101` POST `/stock/market-data` (no venue selector) · FT · see OB | `HOGA` POST `/api/v1/quote/kr-stock/inquiry/orderbook` · SDK+FT · D3, D7 | GET `/api/v1/orderbook` · OAS · T1 | `ohhts_1001_005r` GET `/market/v1/orderbook` · FT · M1, M2 |
| 3 | Candles (OHLCV) | see `candle-evidence-2026-11-05.md` (in progress) | see `candle-evidence-2026-11-05.md` (in progress) | see `candle-evidence-2026-11-05.md` (in progress) | see `candle-evidence-2026-11-05.md` (in progress) | see `candle-evidence-2026-11-05.md` (in progress) | see `candle-evidence-2026-11-05.md` (in progress) |
| 4 | Trade ticks / recent executions (체결) | `FHKST01010300` GET `…/quotations/inquire-ccnl`; `FHPST01060000` GET `…/quotations/inquire-time-itemconclusion` · EX · K2, K3 | `ka10003` 체결정보요청 POST `/api/dostk/stkinfo` · FT · W1 | `t1301` POST `/stock/market-data` (2 TPS); `t8454` (통합, `exchgubun`) · FT · L1, L2 | `CONCLUSION` POST `/api/v1/quote/kr-stock/inquiry/hour-price` · SDK+FT · D3, D7 | GET `/api/v1/trades` (당일 최근 체결) · OAS · T1 | `ohhts_1002_001r` GET `/market/v1/trades/ticks` · FT · M1, M2 |
| 5 | Symbol master (`load_markets`) | file download `kospi_code.mst.zip` / `kosdaq_code.mst.zip` (zipped `.mst`) · EX · K4 | `ka10099` 종목정보 리스트 POST `/api/dostk/stkinfo` (`mrkt_tp`) · FT · W1 | `t8436` 주식종목조회 API용 POST `/stock/etc` (`gubun`) · FT · L1, L2 | `JCODES` POST `/api/v1/quote/kr-stock/inquiry/stock-ticker` · SDK+FT · D3, D7 | GET `/api/v1/stocks/all?market=…` (JSON, no paging) · OAS · T1 | file download `mts_kospi_code.mst` / `mts_kosdaq_code.mst` via `/stock-info/download/{kospi,kosdaq}` · PR · M3 |
| 6 | Market session / holidays | `CTCA0903R` 국내휴장일조회 GET `…/quotations/chk-holiday` · EX · K5 | REST NF (spec searched for 휴장/영업일/장운영); WS only `0s` 장시작시간 · FT · W1 | REST NF (catalog; `t0167` is server time only); WS only `JIF` 장운영정보 · FT · L1 | NF (SDK, support matrix, quote-group guide list) · D1, D3, D7 | GET `/api/v1/market-calendar/KR` · OAS · T1 | `obcpp_bsdy_021r` GET `/reference/v1/market-days`; `obtrs_sstm_506r` GET `/reference/v1/market-hours` · FT · M1, M2 |
| 7 | Rate limits (as documented) | token 1/min; `EGW00201` = TPS exceeded; paper "lower", no numbers · PR · K6 | codes `1700`/`1701`/`1702` (per-API/total/group exceeded), no numbers · FT · W1, W3 | per-TR `transactionPerSec` (e.g. t1102 10, t1301 2, CSPAT00601 10); token limit NF · FT · L1 | app 20 TPS; token 1/min; per-API TPS; WS 2 sessions × 50 symbols · SDK · D2, D1 | named groups + `X-RateLimit-*`/`Retry-After` on 429; no numeric quota; one live token per client · OAS · T1 | REST 10/s per account; WS 2 sessions per HTS ID · PR · M4 |
| 8 | Error / status code reference | NF as a table; README names only `EGW00201`; `rt_cd`/`msg_cd` envelope in `kis_auth.py` · PR · K6, K1 | 37-entry `error_codes` table in SDK spec · FT · W1 | NF (tr-guides.json, apiservice, about-openapi, howto-use; FAQ redirected) · L1, L4, L5 | full platform/service/WS code tables · SDK · D2 | `ErrorResponse.code` flat strings, per-op examples, "accept unknown codes"; no list · OAS · T1 | per-API `rsp_cd` field; all errors HTTP 500; no consolidated table found · FT+PR · M1, M5 |
| 9 | Account balance (잔고) — inventory only | `TTTC8434R`/`VTTC8434R` GET `…/trading/inquire-balance`; needs `CANO`+`ACNT_PRDT_CD` · EX · K7 | `kt00018` POST `/api/dostk/acnt`; no account-number field in request table · FT · W1 | `t0424` 주식잔고2 POST `/stock/accno`; no account-number field in InBlock · FT · L1, L2 | `CSPAQ03420` POST `/api/v1/trading/kr-stock/inquiry/balance`; no account-number field in body · SDK+FT · D4, D8 | GET `/api/v1/holdings`; header `X-Tossinvest-Account` required · OAS · T1 | `obacb_balc_114r` GET `/accounts/v1/me/holdings`; no account-number param (`me`) · FT · M1, M2 |
| 10 | Order place / modify / cancel — inventory only | `TTTC0012U`/`TTTC0011U` (buy/sell) POST `…/trading/order-cash`; `TTTC0013U` POST `…/trading/order-rvsecncl`; `CANO` field · EX · K8 · paper: ✓ `VTTC…` + paper origin (K9) | `kt10000`/`kt10001`/`kt10002`/`kt10003` POST `/api/dostk/ordr` · FT · W1, W2 · paper: ✓ `mockapi.kiwoom.com` per spec meta | `CSPAT00601`/`00701`/`00801` POST `/stock/order` · FT · L1, L2 · paper: ~ 모의투자 app type exists (L5), REST mock origin not listed | `CSPAT00600`/`00700`/`00800` POST `/api/v1/trading/kr-stock/order{,-revision,-cancel}` · SDK+FT · D4, D1, D8 · paper: ✓ ⭕ (NXT variants ❌) | POST `/api/v1/orders`, `/{orderId}/modify`, `/{orderId}/cancel`; `X-Tossinvest-Account` · OAS · T1 · paper: NF | `obtrs_oder_101a` POST `/trading/v1/orders/{buy,sell,modify,cancel}` · FT · M1, M2 · paper: ✗ publisher states the linked account is real (M5) |
| 11 | Real-time WebSocket (quotes) | yes: `H0STCNT0` 체결, `H0STASP0` 호가; `ws://ops.koreainvestment.com:21000` (paper :31000) · EX · K9, K10 | yes: `0B` 주식체결, `0D` 호가잔량; `wss://api.kiwoom.com:10000` `/api/dostk/websocket` (mock host listed) · FT · W1 | yes: `S3_`/`H1_` (KRX), `NS3`/`NH1` (NXT), `US3`/`UH1` (통합); `wss://openapi.ls-sec.co.kr:9443` (simulation :29443) · FT · L1 | yes: `S00` 체결, `S01` 호가; `wss://openapi.dbsec.co.kr:7070/websocket` (demo :17070) · SDK · D5, D6 | yes: `realtime-trade`, `realtime-orderbook`; `wss://openapi-ws.tossinvest.com/ws/v1` · OAS · T2 | yes: `ohhts_stck_cntg`, `ohhts_stck_aspr` (+NXT/SOR); `wss://openapi.imeritz.com:29443` · FT · M1, M2 |

"OB" = [`order-book-evidence-2026-11-05.md`](https://github.com/kisbi3/ktradelink/blob/91bc30d7540814e7d5a6355a51904172a5e4073f/docs/brokers/order-book-evidence-2026-11-05.md)
on the open branch `claude/issue-17-order-book` at commit
`91bc30d7540814e7d5a6355a51904172a5e4073f` (not merged; its KIS, Kiwoom and
LS pins are reused here unchanged).

Account rows (9, 10) are recorded so the maintainer can see the surface; they
were **not** called and nothing here authorizes calling them. KIS and Toss
document an explicit account identifier in the request; for Kiwoom, LS, DB
and Meritz the inspected request tables show **no** account-number field, so
the account context appears to be bound to the credential. That binding is an
inference from absence and is **unverified**.

### Compact grid

`✓` documented REST route (or documented file for row 5) · `~` partial
(WebSocket-only, or prose without numbers/table) · `✗` not found.

| Capability | KIS | Kiwoom | LS | DB | Toss | Meritz | ✓ count |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Current price | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6 |
| Order book | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6 |
| Candles | (separate audit) | | | | | | – |
| Trade ticks | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6 |
| Symbol master | ✓ file | ✓ | ✓ | ✓ | ✓ | ✓ file | 6 (4 REST + 2 file) |
| Market session / holidays | ✓ | ~ WS | ~ WS | ✗ | ✓ | ✓ | 3 |
| Rate limits | ~ | ~ | ✓ | ✓ | ~ | ✓ | 3 |
| Error code reference | ~ | ✓ | ✗ | ✓ | ~ | ~ | 2 |
| Balance (inventory) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6 |
| Orders (inventory) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6 |
| Orders: documented paper env | ✓ | ✓ | ~ | ✓ | ✗ | ✗ | 3 |
| WebSocket quotes | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6 |

## Sources

### KIS — `koreainvestment/open-trading-api` @ `3a9be59a3ed8745720dc3aa9d584bdf3b7830362`

Paths are relative to `https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/`.

| ID | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | `examples_llm/kis_auth.py` | `0e722d6f3253033efe3cf2b99845397b2b329655` (already pinned in the gates ledger) | `rt_cd`/`msg_cd` envelope; client pacing |
| K2 | `examples_llm/domestic_stock/inquire_ccnl/inquire_ccnl.py` | `7d5ffdd673ce9da28a102fff4a0f8ec4a81b959f` | 주식현재가 체결 `FHKST01010300` (real = demo id) |
| K3 | `examples_llm/domestic_stock/inquire_time_itemconclusion/inquire_time_itemconclusion.py` | `7474386c075576d2f02e0fb86685be171eb43706` | 당일시간대별체결 `FHPST01060000` |
| K4 | `stocks_info/kis_kospi_code_mst.py`; `stocks_info/kis_kosdaq_code_mst.py` | `989278b7850d1899aa87db544f8d4a08404831f2`; `9d04b1d6f6ab31b9b9d9e0014f43690c1571c2c9` | master-file URLs on `new.real.download.dws.co.kr` |
| K5 | `examples_llm/domestic_stock/chk_holiday/chk_holiday.py` | `24c2c33ced429c1446cf39c8cd4dda79bdd18ce3` | 국내휴장일조회 `CTCA0903R` |
| K6 | `README.md` | `182887151f1fb07e5789a029292ac3e43d3ba9bd` | token 1/min; `EGW00201` |
| K7 | `examples_llm/domestic_stock/inquire_balance/inquire_balance.py` | `ddd9392d847dca5a0e0675c0b1905800b364d380` | 주식잔고조회 |
| K8 | `examples_llm/domestic_stock/order_cash/order_cash.py`; `…/order_rvsecncl/order_rvsecncl.py` | `f422cf4ebb3029f580eb10294883a82fded610f6`; `1c927e108db8d30e330a592bd1936bdec8c23bdf` | 주식주문(현금), 정정취소 |
| K9 | `kis_devlp.yaml` | `9d8615d34ef2135566186d0fee36474ed54de491` | prod/paper REST and WebSocket origins |
| K10 | `examples_llm/domestic_stock/ccnl_krx/ccnl_krx.py`; `…/asking_price_krx/asking_price_krx.py`; `…/market_status_krx/market_status_krx.py` | `1767fa913d3807846f2d0e01d600b67ddcd589ac`; `ef306e40f733f71fecc50552781308baf1dc2819`; `d2c2f164a851059c542a4d2e4aff57a045969bd6` | WS `H0STCNT0`, `H0STASP0`, 장운영정보 `H0STMKO0` |

### Kiwoom REST — `Kiwoom-Securities/Kiwoom-REST-API` @ `953e5dbff123f437ab4d11a78a95191a685eb51f`

Paths are relative to `https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/`.

| ID | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | `kiwoom/_data/kiwoom_api_spec.json` | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | 337 API entries (menu, method, URL, 운영/모의 domain, field tables) and 37 `error_codes` |
| W2 | `postman/kiwoom-openapi.postman_collection.json` | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` (same blob as OB) | PRD and MOCK items for ka10003, ka10099, kt00018, kt10000, kt10002, kt10003 |
| W3 | `kiwoom/core/errors.py` | `dd7a8709bccd8a28601c49d26a298d3c92f34e5d` | `RATE_LIMIT_CODES = {1700, 1701, 1702}` |

### LS — public API guide (no Git source)

| ID | Source | Retrieved (UTC) | Identity of the retrieved copy |
| --- | --- | --- | --- |
| L1 | [`/api/apis/public/tr-guides.json?download=true`](https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true) (linked from howto-use), `"version": "20261026021444748"` | 2026-11-05 06:53:57 | sha256 `9aaca437f1925115…`, 2,792,313 bytes; 369 TRs, `servers` REST `:8080`, WEBSOCKET `:9443` with `simulationUrl` `:29443` |
| L2 | Guide detail JSON `/guide/api/<tr-id>?type=rest&api=<sub-menu id>` (IDs from [apiservice](https://openapi.ls-sec.co.kr/apiservice)) | 06:52:20–06:52:59 | t1301 `768799e97d57c8d5…`; t8454 `d28ac2914a236eb9…`; t8436 `efbc50d023d9e06b…`; t9945 `47a2ce86b41d3379…`; t0424 `d9f491edc050d360…`; CSPAQ12200 `d4a5b336b85ab53d…`; CSPAT00601 `cd0ecf53f5659ed5…`; CSPAT00701 `39daec21beb2cc46…`; CSPAT00801 `26b451800cc15862…`; S3_ `feefc8800c4cfcda…`; H1_ `64b535fdeb6e4c63…`; JIF `201a21c2c84eee27…`; t0167 `0beef333e8733fe7…` (t1101 `e3bdd31adba31afb…`, t1102 `42712ce969a8a480…`, token `4acff92cdcdfd551…` match the earlier ledgers byte-for-byte) |
| L3 | [apiservice](https://openapi.ls-sec.co.kr/apiservice) catalog (369 `tr-item` buttons) | 06:59:43 | sha256 `d287f5fcc2079275…`; varies per request (CSRF token only; catalog identical to an earlier copy) |
| L4 | [howto-use](https://openapi.ls-sec.co.kr/howto-use) | 06:53:28 | sha256 `8d07034a134f1baa…` (differs from the 02:3x ledger copy `1ac67684…`) |
| L5 | [about-openapi](https://openapi.ls-sec.co.kr/about-openapi) | 06:53:58 | sha256 `0faac4ed094de0a2…` |

### DB — SDK `DBsecurities/dbsec-open-api` @ `564b5100b80a3a785468b77ee8c0557f6edcfdeb` + API guide

SDK paths are relative to `https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/`.

| ID | Source | Pin | Used for |
| --- | --- | --- | --- |
| D1 | `docs/api_support_matrix.md` | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c` | per-API TR code, 모의투자 ⭕/❌, TPS |
| D2 | `docs/errors_and_rate_limits.md` | blob `889d4557b9a60d7965eca02673455ec4373c43e9` | platform/service/WS code tables; REST and WS limits |
| D3 | `dbsec_sdk/apis/kr_stock_quote/endpoints.py` | blob `5930af396f4a74ff04c7e780fcec87660399bec3` | `PATHS`/`TR_CODES` for PRICE, HOGA, CONCLUSION, JCODES |
| D4 | `dbsec_sdk/apis/kr_stock_order/endpoints.py` | blob `a6e13e46fafb3eedb801f023b6dcd73ecd708105` | order, revision, cancel, balance paths |
| D5 | `dbsec_sdk/apis/kr_stock_realtime/endpoints.py` | blob `4a230c35ef8732722ddd23a73f84c8fd0effb919` | WS `S00`, `S01` |
| D6 | `dbsec_sdk/config.py` | blob `8fab32d061fa9b483247915b2a37159831a0eeee` | REST `:8443`; WS production `:7070`, demo `:17070` |
| D7 | API guide list `https://openapi.dbsec.co.kr/api/apis/public/api-list/80005fb0-6feb-4b8b-904a-605c59e29b4f` (국내주식시세) | retrieved 06:55:17, sha256 `f4f56996c26c33b3…` | path, `svc_id`, `requestLimit` cross-check |
| D8 | API guide list `…/api-list/05ac28b8-624f-4115-8aed-cf55f24279dd` (국내주식주문) | retrieved 06:55:29, sha256 `4f2578523296c2ec…` | order/balance path and `requestLimit` cross-check; `simulatedDomain` null |

### Toss — public OpenAPI

| ID | Source | Retrieved (UTC) | Identity |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | 06:55:39 | `openapi 3.1.0`, `info.version 1.2.28`, sha256 `c5918961335ccd6b…` (identical to the 02:3x ledger copy) |
| T2 | [asyncapi.json](https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json) (referenced by T1 `externalDocs`) | 06:56:04 | `asyncapi 3.0.0`, `info.version 1.2.3`, sha256 `46669a360d4c5c64…` |

### Meritz — public portal pages

| ID | Source | Retrieved (UTC) | Identity |
| --- | --- | --- | --- |
| M1 | API 명세 JSON [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json) (linked from apiservice) | 06:56:31 | sha256 `12574c9e9006a606…`, 1,136,519 bytes, `generatedAt "2026-11-05 15:56:29"` (regenerated per download, so the hash identifies this copy only) |
| M2 | API guide lists `https://openapi.imeritz.com/api/apis/public/api-list/<group>`: 국내주식 `441da3d2-…-198cfffef047`; 계좌 `5bde10c9-…-4fefea58994d`; 실시간 국내주식 `6fdcbbbe-…-78f83301d53d` | 06:56:56–06:56:58 | sha256 `8c33857167d5936b…`; `6989ca0fea7f0184…`; `75441f6745bc7d0a…`; REST domain `https://openapi.imeritz.com:9443`, `simulatedDomain` null for every entry |
| M3 | [stock-info](https://openapi.imeritz.com/stock-info) | 06:57:19 | sha256 `c44ed281d7841e17…`; files themselves **not** downloaded |
| M4 | Notice "API 호출 유량 제어 안내(REST, WEBSOCKET)", created 2026-09-23, via `/api/forums/10000000-0000-0011-0000-000000000001/posts/3dc11098-4ce4-4695-abf5-4c7aa194cb9d` | 06:57:52 | sha256 `06570a95f862eb3a…` |
| M5 | [samplecode-py](https://openapi.imeritz.com/samplecode-py) | ≤06:56:14 | sha256 `661c016af6d72790…` (varies per request; earlier ledger copy `f04eda2b…`) |

## Per-broker notes

**KIS**
- Market-data TRs use the same `tr_id` for real and demo; account/order TRs switch `T…`→`V…` for demo (K7, K8).
- K4 master downloaders call `ssl._create_unverified_context` — **unsafe, must not be copied**; only the file names/host are inventoried.
- K9 lists WebSocket origins as plain `ws://` (ports 21000/31000), not `wss://` — a transport-security gate before any WS work.
- K5 asks callers to keep 국내휴장일조회 to about once per day (원장 load); caching design input.
- `market_time` (`HHMCM000002C0`) is 국내선물 영업일조회 (futures) and was not used for equity sessions.
- K1 paces 0.05 s (prod) / 0.5 s (paper) between calls; that is SDK behaviour, not a documented quota.

**Kiwoom REST**
- W1 is a machine-readable spec shipped in the SDK; every inspected entry lists both 운영 and 모의투자 domains, but error `8104` ("모의투자에서 지원하지 않는 API") shows per-API mock support is not guaranteed.
- No REST market-calendar/holiday API in W1; only WS `0s` 장시작시간.
- Rate-limit errors `1700`/`1701`/`1702` exist without published numbers in the pinned repo.
- `ka10003` takes `_NX`/`_AL` suffixed codes like other Kiwoom quote APIs (venue handling deferred).
- The pinned commit `953e5db…` is **no longer reachable from any branch** of the publisher repo; current `main` `c7a3d25…` has the identical tree (`4eb7d549…`). Pinned links may rot if GitHub prunes it.

**LS**
- L1 (`tr-guides.json`, version `20261026021444748`) is the only LS source with a publisher revision marker; prefer it over HTML pages for future pins.
- L4 onboarding again conflicts with the guide: it shows mock order `tr_id: CSPAT00101` (absent from the 369-TR catalog), a `CANO` body and `GET /stock/balance` with `CSPAQ12300` (catalog: BEP단가조회). Treat as non-authoritative, as with STKCURR (ADR 0010).
- Paper: L5 says API keys are issued for 실전 or 모의; L1 lists a WS `simulationUrl` only; order field text mentions "모의투자는 A+종목코드". No REST mock origin documented.
- WS path differs between L1 (`/websocket`) and L2 (`/websocket/stock`, `/websocket/etc`).
- `t1301` has no `exchgubun`; `t8454` (통합) has one. Market session is WS `JIF` only.

**DB**
- D1 TPS values match D7/D8 `requestLimit` for every TR checked (PRICE 5, HOGA 3, CONCLUSION 3, JCODES 3, CSPAT00600 10, 00700 3, 00800 3, CSPAQ03420 2).
- NXT order TRs (`CSPAT00610`/`00710`/`00810`) are marked ❌ for demo in D1.
- D2 describes REST limits "앱(계좌)별" and WS limits per app/account; consistent with the absent account field (unverified).
- No market-session or holiday API found in the SDK, D1 or the quote group list.
- D3 docstrings give KRX codes as `005930` and NXT/통합 as `N-`/`U-` prefixed, while the testbed sample used `A005930`; field-level, left to the ticker audit.

**Toss**
- T1 market-data operations need no account header; holdings and order operations require `X-Tossinvest-Account`.
- No paper/sandbox environment is described in T1 or T2 (searched "sandbox", "모의", "paper").
- Rate limits are grouped (`MARKET_DATA`, `MARKET_DATA_CHART`, `MARKET_INFO`, `ASSET`, …) and reported via headers; numeric quotas are not published (only header examples).
- `market-calendar/KR` is described as integrated KRX+NXT mode, excluding pre/post closing-price sessions, returning previous/current/next business day in KST.
- `stocks/all` returns only symbols tradable at Toss, refreshed by a daily batch.

**Meritz**
- M5 states the account linked to the app key is a **real account, not a mock account**; M2 has no 모의투자 domain for any API. Order paths therefore have no documented paper environment.
- Account APIs are `/accounts/v1/me/...` with no account parameter; `mac_address` is a required header on market-data and account calls (M1).
- M4: REST 10 calls/s per account; WebSocket 2 sessions per HTS ID.
- Errors: HTTP 500 for every error with `rsp_cd`/`rsp_msg` (`rsp_sub_msg` on some APIs); success codes differ by API family (order receipt `0001`). No consolidated code table found.
- Symbol master is a set of `.mst` files refreshed each business day; the column spec is said to be in the API 문서 (not inspected).
- WS path differs between M1 (`/websocket`) and M2 (`/websocket/<tr>`).

## Suggested next deep audits (data-driven)

Ranked by how many of the six publishers document a REST route (✓) in the
grid above. This is a documentation count only; it claims no support.

1. **Trade ticks / recent executions — 6/6 REST.** Read-only, no account
   context, venue selectors visible on most routes. Best next market-data audit.
2. **Symbol master — 6/6, but 4 REST + 2 file.** Needs a format/provenance
   decision (REST pages vs fixed-width `.mst` files) before field mapping.
3. **Market session / holidays — 3/6 REST (+2 WS-only, 1 not found).**
   Cannot become a six-broker common method without a WS or external source.
4. **Rate limits — 3/6 with numbers; error codes — 2/6 with tables.**
   Cross-cutting transport inputs; audit together, per broker.
5. **Balance and orders — 6/6 documented, but account-bound.** Only 3/6
   document a paper environment (KIS, Kiwoom, DB; LS partial). Any deeper
   audit needs explicit maintainer scoping, and any call needs separate
   authorization; Toss and Meritz offer no documented paper path.

WebSocket quotes are documented by all six but are out of the REST scope.
Order book and current price already have evidence ledgers; candles are
covered by the separate in-progress audit.
