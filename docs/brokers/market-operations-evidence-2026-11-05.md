# Six-broker market-operations (장 운영 정보) evidence — 2026-11-05

- **Scope:** publisher documentation for domestic-equity market-operations
  information on six REST APIs: tick size (호가단위), price limits
  (상·하한가, 기준가), trading sessions and hours, the holiday / trading
  calendar, and instrument and market status (VI, 거래정지, 관리종목,
  투자경고 and similar). Brokers: KIS, Kiwoom REST, LS, DB, Toss and
  Meritz. WebSocket feeds (for example 장운영정보) are named by id only.
  The Shinhan comparison stays separate.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No KTradeLink calendar, tick-size, price-limit or
  status model, decoder or request plan exists, and this file does not
  authorize one.
- **No broker API request was sent.** No token, credential, account, MAC
  value or order was used. Only files in public Git repositories were
  fetched for §2 and §3. No exchange (KRX/NXT) rulebook was fetched or
  cited: exchange rules are not broker evidence. Data-use and
  redistribution terms were out of scope by maintainer instruction.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS and Kiwoom: single files at fixed Git commits, fetched
    07:45:10–07:51:03 over HTTPS from
    `raw.githubusercontent.com/<owner>/<repo>/<full commit SHA>/<path>`.
    Git blob SHAs were computed locally from the retrieved bytes.
  - LS and DB: **pending** (§4.1, §5.1).
  - Toss and Meritz: **pending** (§6.1, §7.1).
- **Cross-check with earlier audits:** fourteen blobs cited here were
  already pinned by the capability-inventory, order-book, candle, trade or
  symbol-master audits, and the copies retrieved for this file hash
  identically: K1, K7, K8, K21 (KRX file), K22–K25, K29; W1, W2, W7, W8
  and Kiwoom `kiwoom/core/client.py` (§2.1, §3.1). The commit dates in
  §2.1 and §3.1 are quoted from the trade audit; this audit did not read
  commit objects itself.
- **Pin formats:**
  - Git blob SHAs are `sha1("blob <len>\0" + bytes)` of the retrieved
    bytes, i.e. what `git hash-object` and `git ls-tree` print.
  - Line numbers are written "(K3 L63–66)": source K3, lines 63–66 of that
    blob.
  - Web pages have no immutable revision. Their sha256 prefix identifies
    only the copy retrieved at the stated time.
  - Raw copies were kept outside the repository. Sample tokens, account
    values, app keys, MAC values and staff contact data in publisher
    material are deliberately not copied.
- **Evidence levels:**
  - `field table`: a publisher field or spec table.
  - `publisher example`: a sample request/response or sample code,
    including the Korean column labels and docstrings in KIS sample code.
  - `publisher client code`: SDK, helper or tool behaviour (for example a
    tick table in a backtester). It shows what the publisher's own code
    does; it is **not** a contract.
  - `legacy publisher example`: sample code under a publisher repository's
    `legacy/` directory. Lower weight than current examples.
  - `publisher guide`: portal prose outside the API specification.
  - `publisher repo note`: non-code text in a publisher repository.
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- Sample values in publisher examples are illustrative. They are **not**
  authorized response fixtures.

## 1. Broker × concern summary

Cell format: short verdict — evidence. `F` field table, `E` publisher
example, `L` legacy publisher example, `C` publisher client code, `G`
publisher guide, `—` not found.

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Tick size (호가단위) | `aspr_unit` "호가단위" column on `inquire-price` only; no route, no type, no venue rule — E. A 7-band table "2023년 기준" in backtester / strategy-builder code — C (not a contract) | **not found** (no field, no route). `pri_sel_bid_unit` "우선매도호가단위" is a best-quote price, not a tick size (inference from E) | pending | pending | pending | pending |
| Price limits | `stck_mxpr` "주식 상한가" / `stck_llam` "주식 하한가" on `inquire-price`, `inquire-price-2`, `capture-uplowprice`; `ovtm_untp_mxpr`/`ovtm_untp_llam` for 시간외 단일가 — E; types and signs not documented | `upl_pric` "상한가" / `lst_pric` "하한가", "단위: 원, 부호가 포함된 숫자", on `ka10001` and `ka10007` — F; `ka10001` example values misaligned (E) | pending | pending | pending | pending |
| 기준가 vs 전일종가 | separate columns `stck_sdpr` "주식 기준가" and `stck_prdy_clpr` "주식 전일 종가" on `inquire-price-2`; relation not documented — E | `base_pric` "기준가" (`ka10001`) vs `pred_close_pric` "전일종가" (`ka10007`), `lastPrice` "전일종가" (`ka10099`/`ka10100`); relation not documented — F | pending | pending | pending | pending |
| Session hours | **no REST schedule**. Prose only: "장시간(09:00~15:30)" (REST docstring), "시간외 단일가(16:00~18:00)" (WebSocket docstrings) — E | **no REST schedule**. Clock times only in the WebSocket `0s` 장운영구분 code list — F (WS) | pending | pending | pending | pending |
| Market-phase code (REST) | `new_mkop_cls_code` "신 장운영 구분 코드", `antc_mkop_cls_code` "예상 장운영 구분 코드" on `inquire-asking-price-exp-ccn`; **no code list** — E | none in responses; request filters only (`ka10030` `mrkt_open_tp`, `ka10054` `bf_mkrt_tp`) — F | pending | pending | pending | pending |
| Holiday / calendar | `CTCA0903R` GET `…/quotations/chk-holiday`, `BASS_DT` YYYYMMDD → `bzdy_yn` 영업일, `tr_day_yn` 거래일, `opnd_yn` 개장일, `sttl_day_yn` 결제일; "가급적 1일 1회 호출" — E | **not found** (REST); WebSocket `0s` 장시작시간 only — F | pending | pending | pending | pending |
| VI | route `FHPST01390000` `inquire-vi-status` (static/dynamic, times, prices); `vi_cls_code` on quote routes; no code lists; no venue selector — E | route `ka10054` with `stex_tp` "1:KRX, 2:NXT 3.통합" and per-row `stex_tp`; `viaplc_tp` without code list — F+E | pending | pending | pending | pending |
| Halt / 관리 / warnings | `temp_stop_yn`, `trht_yn`, `tr_stop_yn`, `nxt_tr_stop_yn` "NXT 거래정지여부", `mang_issu_*`, `admn_item_yn`, `mrkt_warn_cls_code`, `invt_caful_yn`, `short_over_yn`, `sltr_yn` …; **no value encodings** — E | `orderWarning` code list "0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: …"; free-text `state`, `auditInfo`; `nxtEnable`; no halt field — F+E | pending | pending | pending | pending |

## 2. KIS (Korea Investment & Securities)

### 2.1 Pinned sources

All sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362).
The full SHA is `3a9be59a3ed8745720dc3aa9d584bdf3b7830362`; the trade audit
records the commit date as 2026-10-28T00:26:05+09:00. Paths are relative to
the repository root; `…/` stands for `examples_llm/domestic_stock/`. Every
file was fetched 07:45:10–07:47:35.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | [`…/chk_holiday/chk_holiday.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/chk_holiday/chk_holiday.py) | `24c2c33ced429c1446cf39c8cd4dda79bdd18ce3` | 국내휴장일조회 route, request, cadence note. Same blob as the capability inventory's K5. |
| K2 | [`…/chk_holiday/chk_chk_holiday.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/chk_holiday/chk_chk_holiday.py) | `baad0c91b6a701cf86467da6dcf06449542fd5d9` | Response column names (L21–28) |
| K3 | [`…/inquire_price/inquire_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_price/inquire_price.py) | `bb6ab22df57b1a5d14fab861f6c1d29272872a84` | 주식현재가 시세 route |
| K4 | [`…/inquire_price/chk_inquire_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_price/chk_inquire_price.py) | `ad79be53fe43e667db13748799458ca66e3ab9d7` | Its column names (L21–104) |
| K5 | [`…/inquire_price_2/inquire_price_2.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_price_2/inquire_price_2.py) | `1f87c3093ac992d7d94c5fb9c1ddf4599ab2726c` | 주식현재가 시세2 route |
| K6 | [`…/inquire_price_2/chk_inquire_price_2.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_price_2/chk_inquire_price_2.py) | `e79fa32fead2d526fc8f66b4b60159eec253c3e8` | Its column names (L21–76) |
| K7 | [`…/inquire_asking_price_exp_ccn/inquire_asking_price_exp_ccn.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_asking_price_exp_ccn/inquire_asking_price_exp_ccn.py) | `956ce6779b48a8c2f8fd052ef1a0c4703357fa09` | 호가/예상체결 route, output split (L73–77) |
| K8 | [`…/inquire_asking_price_exp_ccn/chk_inquire_asking_price_exp_ccn.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_asking_price_exp_ccn/chk_inquire_asking_price_exp_ccn.py) | `0e7385a2acbb431f2dc2ad6a66bf04146ca9f961` | 장운영 code column names (L92–93) |
| K9 | [`…/inquire_overtime_price/inquire_overtime_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_overtime_price/inquire_overtime_price.py) | `94b484734703b24bb8cde2382c8d20eadaf4b52e` | 시간외현재가 route |
| K10 | [`…/inquire_overtime_price/chk_inquire_overtime_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_overtime_price/chk_inquire_overtime_price.py) | `537674154e47829334ab528cd4026957b6597611` | Its column names (L21–57) |
| K11 | [`…/inquire_vi_status/inquire_vi_status.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_vi_status/inquire_vi_status.py) | `874b047cb07b91c561d524697cb0ba29712627e8` | VI 현황 route and request codes |
| K12 | [`…/inquire_vi_status/chk_inquire_vi_status.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_vi_status/chk_inquire_vi_status.py) | `30a867e0c182a4faca103e6615aae217e8dbf285` | Its column names (L25–40) |
| K13 | [`…/capture_uplowprice/capture_uplowprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/capture_uplowprice/capture_uplowprice.py) | `09fd310d08728b0af3bc90d0df70995324a9d70a` | 상하한가 포착 route |
| K14 | [`…/capture_uplowprice/chk_capture_uplowprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/capture_uplowprice/chk_capture_uplowprice.py) | `5cfe05cf211dda5e8070b6d7fe2287391d0ac345` | Its column names (L21–39) |
| K15 | [`…/search_stock_info/search_stock_info.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/search_stock_info/search_stock_info.py) | `67473d72bec848a594c33d18674230c030deb8ce` | 주식기본조회 route |
| K16 | [`…/search_stock_info/chk_search_stock_info.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/search_stock_info/chk_search_stock_info.py) | `25570cec2ecbdbf63640c5c6792b9b3a49de3bf7` | Halt / 관리 / NXT columns (L72–73, L84, L90–91) |
| K17 | [`…/market_time/market_time.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/market_time/market_time.py) | `9c5aee4708710e90ee8c7c44a9ee1fb99bfcb79b` | 국내선물 영업일조회 route (futures by title) |
| K18 | [`…/market_time/chk_market_time.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/market_time/chk_market_time.py) | `d1333dcfe0c24b0d2d558997b74059fc0717c3e7` | Its column names (L21–31) |
| K19 | [`…/comp_program_trade_today/comp_program_trade_today.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/comp_program_trade_today/comp_program_trade_today.py) | `1590335401b94af6fceab7e3a6f41b54d36ceec8` | Hours stated in a REST docstring (L35–36) |
| K20 | [`…/overtime_ccnl_krx/overtime_ccnl_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/overtime_ccnl_krx/overtime_ccnl_krx.py); [`…/overtime_asking_price_krx/overtime_asking_price_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/overtime_asking_price_krx/overtime_asking_price_krx.py) | `9e2e6dc6579e8a38cf05f9391bbc42cb576de17f`; `ce3d0d04f19055cbdd9c257a9219ee402fbb4f0e` | WebSocket docstrings with 시간외 단일가 hours (L26; L27). Context only. |
| K21 | [`…/market_status_krx/market_status_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/market_status_krx/market_status_krx.py); [`…/market_status_nxt/market_status_nxt.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/market_status_nxt/market_status_nxt.py); [`…/market_status_total/market_status_total.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/market_status_total/market_status_total.py) | `d2c2f164a851059c542a4d2e4aff57a045969bd6`; `db2057847bb53d41244b97a5967b158eed3fc312`; `ec7d8f9863ca68c825376cee97a1adeccff10799` | WebSocket 장운영정보 ids `H0STMKO0` / `H0NXMKO0` / `H0UNMKO0`, names only |
| K22 | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) | `0e722d6f3253033efe3cf2b99845397b2b329655` | Transport: GET (L476), paper TR rewrite (L453–455), `smart_sleep` (L289–293). Same blob as the trade audit's K7. |
| K23 | [`MCP/Kis Trading MCP/configs/domestic_stock.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/configs/domestic_stock.json) | `e82a0829ef519c64dfecb3e966ed217b4fcd3805` | Publisher tool registry: `chk_holiday` (L2217–2256) |
| K24 | [`examples_user/domestic_stock/domestic_stock_functions.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_user/domestic_stock/domestic_stock_functions.py) | `e585487d112409af59a64ad135cfc9440b266e72` | L418–451 repeat K1; L9605–9623 repeat K17 |
| K25 | [`legacy/Sample01/kis_domstk.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/Sample01/kis_domstk.py) | `0090f06c540fadc0b87a1e9515ab4c098e3aa9c2` | **Legacy** holiday helper (L1332–1357) |
| K26 | [`backtester/kis_backtest/utils/korean_market.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/kis_backtest/utils/korean_market.py) | `7f29357822d462077fa5aee8d52fae42e2c57f76` | **Client code** tick table (L10–47) |
| K27 | [`strategy_builder/core/order_executor.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/strategy_builder/core/order_executor.py) | `a58e8da3e97b9baba2008f9fc9313956cb559fba` | **Client code** tick table (L101–123) |
| K28 | [`backtester/kis_backtest/models/market_data.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/kis_backtest/models/market_data.py) | `b72cccfb545ec0c050ef15877c6fcbafb247d1f2` | **Client code** model with `price_limit_up` / `price_limit_down` (L88–90) |
| K29 | [`…/inquire_daily_itemchartprice/chk_inquire_daily_itemchartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_daily_itemchartprice/chk_inquire_daily_itemchartprice.py) | `e6ea734d0a938069a3bf58f3c530717564fcef2f` | `stck_mxpr`/`stck_llam` on the daily-chart route (L32–33) |
| K30 | [`MCP/KIS Code Assistant MCP/data.csv`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/KIS%20Code%20Assistant%20MCP/data.csv) | `8602ddd4c90811d21d4e997298c7a04a4c6f9b3d` | Search index only: a CSV copy of the `examples_llm` docstrings and column maps. Every hit used here is cited from the underlying example file. |

**Missing evidence:**

- None of K1–K30 is a KIS field table: there are no JSON types, lengths,
  units, value encodings (`Y`/`N`?) or code lists for any field below.
- None contains a sample response body.
- The KIS developer-portal specification was **not** retrieved.
- Every response-side statement is therefore limited to column *names*
  and their Korean labels in sample code (`publisher example`).
- Searched and **not found** in the files above: an equity session-schedule
  route, a tick-size route, NXT session hours, API service hours, and a
  code list for any status or 장운영 field.

### 2.2 Routes

All routes below are `GET` with query parameters: none passes `postFlag`
to K22 `_url_fetch`, which then calls `requests.get` (K22 L476).

| Route (title verbatim) | Method + path | TR id | Real / paper | Purpose | Evidence |
| --- | --- | --- | --- | --- | --- |
| "[국내주식] 업종/기타 > 국내휴장일조회[국내주식-040]" (K1 L19) | GET `/uapi/domestic-stock/v1/quotations/chk-holiday` (K1 L23) | `CTCA0903R` (K1 L70) | no environment switch in K1. K22 L453–455 rewrites a leading `C` to `V` in paper mode, so the sample would send `VTCA0903R`; paper support **not documented** | holiday flags per date | publisher example |
| "[국내주식] 기본시세 > 주식현재가 시세[v1_국내주식-008]" (K3 L18) | GET `…/quotations/inquire-price` (K3 L22) | `FHKST01010100` for `real` and `demo` (K3 L59–64) | same id both | limits, 기준가, `aspr_unit`, status flags | publisher example |
| "[국내주식] 기본시세 > 주식현재가 시세2[v1_국내주식-054]" (K5 L18) | GET `…/quotations/inquire-price-2` (K5 L22) | `FHPST01010000` (K5 L50) | no environment switch; **not documented** | limits, 기준가 and 전일종가, status flags | publisher example |
| "[국내주식] 기본시세 > 주식현재가 호가/예상체결[v1_국내주식-011]" (K7 L19) | GET `…/quotations/inquire-asking-price-exp-ccn` (K7 L23) | `FHKST01010200` for `real` and `demo` (K7 L58–63) | same id both | 장운영 code columns, 기준가, VI | publisher example |
| "[국내주식] 기본시세 > 국내주식 시간외현재가[국내주식-076]" (K9 L18) | GET `…/quotations/inquire-overtime-price` (K9 L22) | `FHPST02300000` (K9 L51) | **not documented** | 시간외 단일가 limits, 기준가, VI, status | publisher example |
| "[국내주식] 기본시세 > 변동성완화장치(VI) 현황[v1_국내주식-055]" (K11 L21) | GET `…/quotations/inquire-vi-status` (K11 L25) | `FHPST01390000` (K11 L106) | **not documented** | VI events by date | publisher example |
| "[국내주식] 시세분석 > 국내주식 상하한가 포착 [국내주식-190]" (K13 L17) | GET `…/quotations/capture-uplowprice` (K13 L21) | `FHKST130000C0` (K13 L77) | **not documented** | symbols at / near a limit | publisher example |
| "[국내주식] 종목정보 > 주식기본조회[v1_국내주식-067]" (K15 L24) | GET `…/quotations/search-stock-info` (K15 L28) | `CTPF1002R` (K15 L75) | K22 would send `VTPF1002R` in paper mode; **not documented** | 거래정지 / 관리 / NXT flags | publisher example |
| "[국내주식] 업종/기타 > 국내선물 영업일조회 [국내주식-160]" (K17 L18) | GET `…/quotations/market-time` (K17 L22) | `HHMCM000002C0` (K17 L37) | **not documented** | futures business days and times (by title); see §2.5 | publisher example |

WebSocket 장운영정보, names only: `H0STMKO0` "국내주식 장운영정보 (KRX)"
(K21 `market_status_krx.py` L24, L49), `H0NXMKO0` "(NXT)" (K21
`market_status_nxt.py` L24, L50) and `H0UNMKO0` "(통합)" (K21
`market_status_total.py` L24, L50). The KRX docstring says "연결된 종목의 VI
발동 시와 VI 해제 시에 데이터가 수신됩니다." (K21 `market_status_krx.py`
L26).

### 2.3 Tick size (호가단위)

- **Route:** none found.
- **Field:** `aspr_unit` "호가단위" is a column of `inquire-price` (K4 L61).
  It appears in no other route retrieved here.
  - Type, unit and whether it is the tick at the current price, the tick
    of the 기준가 band, or something else: **not documented**.
    `NUMERIC_COLUMNS` is empty (K4 L106).
  - `hts_deal_qty_unit_val` "HTS 매매 수량 단위 값" (K4 L62) is a quantity
    unit, not a price tick.
- **Venue:** `inquire-price` accepts `FID_COND_MRKT_DIV_CODE` "J:KRX, NX:NXT,
  UN:통합" (K3 L26). Whether `aspr_unit` differs by venue: **not
  documented**.
- **Publisher client code (not a contract):**
  - K26 L10–47 `get_tick_size(price)`, docstring "한국 주식시장 호가단위
    (2023년 기준)" (K26 L13), seven bands: "~2,000원: 1원",
    "2,000~5,000원: 5원", "5,000~20,000원: 10원", "20,000~50,000원: 50원",
    "50,000~200,000원: 100원", "200,000~500,000원: 500원",
    "500,000원~: 1,000원" (K26 L14–20).
  - K27 L101–117 repeats the same bands in `_get_tick_size`; K27 L120–123
    always rounds **down** ("가격을 호가단위로 내림 (매수 시 유리한 방향)").
  - Neither table distinguishes KOSPI / KOSDAQ, ETF / ETN, or KRX / NXT,
    and neither cites a source beyond "2023년 기준".
  - K26 L3 says the module handles "호가단위, 거래시간 등"; the 82-line file
    contains only the two tick functions. No trading-hours code exists in
    it.
  - **Inference:** the publisher's own tools do not read `aspr_unit`; they
    carry a local table. That is a hint that the field was not considered
    sufficient there, not evidence of its semantics.

### 2.4 Price limits (상한가 / 하한가 / 기준가)

| Route | 상한가 | 하한가 | 기준가 | 전일종가 | Other |
| --- | --- | --- | --- | --- | --- |
| `inquire-price` | `stck_mxpr` "주식 상한가" (K4 L43) | `stck_llam` "주식 하한가" (K4 L44) | `stck_sdpr` "주식 기준가" (K4 L45) | none | `rstc_wdth_prc` "제한 폭 가격" (K4 L58) |
| `inquire-price-2` | `stck_mxpr` (K6 L26) | `stck_llam` (K6 L51) | `stck_sdpr` (K6 L57) | `stck_prdy_clpr` "주식 전일 종가" (K6 L59) | `mxpr_llam_cls_code` "상하한가 구분 코드" (K6 L24), no code list |
| `inquire-asking-price-exp-ccn` | none | none | `stck_sdpr` (K8 L98) | none | — |
| `inquire-overtime-price` | `ovtm_untp_mxpr` "시간외 단일가 상한가" (K10 L30) | `ovtm_untp_llam` "시간외 단일가 하한가" (K10 L31) | `ovtm_untp_sdpr` "시간외 단일가 기준가" (K10 L48) | none | — |
| `capture-uplowprice` | `stck_mxpr` "주식상한가" (K14 L37) | `stck_llam` "주식하한가" (K14 L36) | none | none | request below |
| `inquire-daily-itemchartprice` | `stck_mxpr` (K29 L32) | `stck_llam` (K29 L33) | — | — | whether per day or a current snapshot is not stated |

- **Types, units and signs:** not documented for any of these columns
  (§2.1).
- **기준가 vs 전일종가:** `inquire-price-2` carries both as separate
  columns (K6 L57, L59). Their relationship (for example after a corporate
  action) is **not documented**.
- **Regular vs after-hours:** the 시간외 단일가 limits and 기준가 have
  their own columns (K10 L30–31, L48), distinct from the regular ones.
- **Venue:** `inquire-price` and `inquire-price-2` accept J / NX / UN
  (K3 L26; K5 L32). Whether limits or 기준가 differ by venue is **not
  documented**. `capture-uplowprice` takes only "J:주식" (K13 L25) and a
  market code "0000:전체, 0001:코스피, 1001:코스닥" (K13 L30).
- **`capture-uplowprice` request:** `FID_PRC_CLS_CODE` "0:상한가, 1:하한가"
  (K13 L27); `FID_DIV_CLS_CODE` "0:상하한가종목, 6:8%상하한가 근접,
  5:10%상하한가 근접, 1:15%상하한가 근접, 2:20%상하한가 근접, 3:25%상하한가
  근접" (K13 L29). The docstring ties it to an HTS screen: "한국투자
  HTS(eFriend Plus) > [0917] 실시간 상하한가 포착 화면 의 기능을 API로 개발한
  사항" (K13 L39).
- **Publisher client code:** the backtester model `StockInfo` has
  `prev_close` "전일종가", `price_limit_up` "상한가" and `price_limit_down`
  "하한가" (K28 L88–90). Which KIS field feeds them was not traced.

### 2.5 Trading sessions and hours

- **Session-schedule route for equities:** not found.
- **Hours stated in publisher prose** (docstrings, KRX only, not a
  contract):
  - REST 프로그램매매 종합현황(시간): "※ 장시간(09:00~15:30) 동안의 최근 30분간의
    데이터 확인이 가능하며, 다음조회가 불가합니다." and "※ 장시간(09:00~15:30)
    이후에는 bsop_hour 에 153000 ~ 170000 까지의 시간데이터가 출력되지만
    데이터는 모두 동일한 장마감 데이터인 점 유의 부탁드립니다." (K19 L35–36).
  - WebSocket 시간외 체결/호가: "국내주식 시간외 단일가(16:00~18:00) 시간대에
    실시간체결가 데이터 확인 가능합니다." (K20 `overtime_ccnl_krx.py` L26;
    the same hours in `overtime_asking_price_krx.py` L27).
  - Pre-market, 장전/장후 시간외 종가 and NXT pre/after-market hours:
    **not found**.
- **Market-phase codes on REST:**
  - `new_mkop_cls_code` "신 장운영 구분 코드" and `antc_mkop_cls_code`
    "예상 장운영 구분 코드" (K8 L92–93). K7 L73–77 returns `output1`
    (호가정보) and `output2` (예상체결정보); K8 maps both into one table, so
    which output carries these columns is **not documented**. Code list:
    **not found**.
  - Related phase-like columns, all without code lists:
    `iscd_stat_cls_code` "종목 상태 구분 코드" (K4 L22);
    `oprc_rang_cont_yn` "시가 범위 연장 여부" and `clpr_rang_cont_yn`
    "종가 범위 연장 여부" (K4 L28–29); `divi_app_cls_code`
    "동시호가배분처리코드" (K6 L42); `vlnt_fin_cls_code` "임의 종료 구분 코드"
    (K6 L73).
- **Session selection:** after-hours single-price data has its own routes
  (`inquire-overtime-price`, §2.2; `FHPST02310000` in the trade audit).
  Whether `J` / `NX` / `UN` quote routes include pre- or after-market
  values: **not documented**.
- **`market-time`:** its title is "국내선물 영업일조회" (K17 L18) and the
  docstring says "국내선물 영업일조회 API입니다. API호출 시 body 혹은
  params로 입력하는 사항이 없습니다." (K17 L26–27). Columns `date1`–`date5`
  "영업일1"–"영업일5", `today` "오늘일자", `time` "현재시간", `s_time`
  "장시작시간", `e_time` "장마감시간" (K18 L22–30). **Inference:** by its
  title this is a futures route; it is not equity session evidence. The
  capability inventory reached the same conclusion.
- **API service hours:** not found.

### 2.6 Holiday / trading calendar

- **Route:** 국내휴장일조회, `CTCA0903R`, GET `…/quotations/chk-holiday`
  (§2.2). The publisher registry K23 L2217–2256 and K24 L418–451 repeat it.
- **Request** (K1 L26–33, L72–76):
  - `BASS_DT` "[필수] 기준일자 (ex. YYYYMMDD)" (K1 L44);
  - `CTX_AREA_FK` "연속조회검색조건" and `CTX_AREA_NK` "연속조회키"
    (K1 L28–29, L74–75);
  - header `tr_cont` "연속거래여부".
  - No date range, venue or market selector exists.
- **Response columns** (K2 L21–28):

  | Column | Label |
  | --- | --- |
  | `bass_dt` | "기준일자" |
  | `wday_dvsn_cd` | "요일구분코드" |
  | `bzdy_yn` | "영업일여부" |
  | `tr_day_yn` | "거래일여부" |
  | `opnd_yn` | "개장일여부" |
  | `sttl_day_yn` | "결제일여부" |

  Value encodings (`Y`/`N` or other) and the `wday_dvsn_cd` code list:
  **not documented**.
- **Publisher semantics** (K1 L39–41): "국내휴장일조회 API입니다. 영업일,
  거래일, 개장일, 결제일 여부를 조회할 수 있습니다. 주문을 넣을 수 있는지
  확인하고자 하실 경우 개장일여부(opnd_yn)을 사용하시면 됩니다."
  - What distinguishes 영업일, 거래일 and 개장일, and which venue or
    session 개장일 refers to: **not documented**.
- **Range and paging:**
  - K1 treats `output` as a list (K1 L81–85) and follows `tr_cont` "M" or
    "F" with `ctx_area_fk` / `ctx_area_nk` from the body (K1 L94–103).
  - How many dates one response covers, and in which direction from
    `BASS_DT`: **not documented**. **Inference:** a response may hold
    several dates.
  - The legacy helper keeps only the first row: "첫 번째 값만 선택하여 반환"
    (K25 L1354–1357).
- **Cadence:** "(★중요) 국내휴장일조회(TCA0903R) 서비스는 당사 원장서비스와
  연관되어 있어 단시간 내 다수 호출시 서비스에 영향을 줄 수 있어 가급적 1일
  1회 호출 부탁드립니다." (K1 L36–37). Update time of the underlying
  calendar: **not documented**.
- **Real / paper:** not documented (§2.2).

### 2.7 Instrument / market status

No status column below has a documented code list or value encoding.

| Concern | Column and label (verbatim) | Route (source) |
| --- | --- | --- |
| VI | `vi_cls_code` "VI적용구분코드" | `inquire-price` (K4 L96), `inquire-price-2` (K6 L49), `inquire-asking-price-exp-ccn` (K8 L105) |
| VI | `vi_cls_code` "VI발동상태" | `inquire-vi-status` (K12 L29) |
| VI (after-hours) | `ovtm_vi_cls_code` "시간외단일가VI적용구분코드" | `inquire-price` (K4 L97), `inquire-overtime-price` (K10 L54) |
| Temporary stop | `temp_stop_yn` "임시 정지 여부" | `inquire-price` (K4 L27) |
| Trading halt | `trht_yn` "거래정지 여부" | `inquire-price-2` (K6 L71), `inquire-overtime-price` (K10 L46) |
| Trading halt | `tr_stop_yn` "거래정지여부" | `search-stock-info` (K16 L72) |
| NXT halt / eligibility | `nxt_tr_stop_yn` "NXT 거래정지여부"; `cptt_trad_tr_psbl_yn` "NXT 거래종목여부" | `search-stock-info` (K16 L91, L90) |
| 관리종목 | `mang_issu_cls_code` "관리종목여부" | `inquire-price` (K4 L103) |
| 관리종목 | `mang_issu_yn` "관리 종목 여부"; `mang_issu_cls_name` "관리 종목 구분 명" | `inquire-price-2` (K6 L41); `inquire-overtime-price` (K10 L44, L23) |
| 관리종목 | `admn_item_yn` "관리종목여부" | `search-stock-info` (K16 L73) |
| Market warning | `mrkt_warn_cls_code` "시장경고코드" | `inquire-price` (K4 L100), `inquire-price-2` (K6 L44) |
| Market warning | `mrkt_warn_cls_code` "시장 경고 구분 코드"; `mrkt_warn_cls_name` "시장 경구 구분 명" | `inquire-overtime-price` (K10 L45, L49) |
| Market warning | `mrkt_warn_cls_name` "시장 경고 구분 명" | `inquire-price-2` (K6 L56) |
| 투자유의 | `invt_caful_yn` "투자유의여부" | `inquire-price` (K4 L99), `inquire-price-2` (K6 L45) |
| 투자유의 (ETF/ETN) | `etf_etn_ivst_heed_item_yn` "ETFETN투자유의종목여부" | `search-stock-info` (K16 L84) |
| 단기과열 | `short_over_yn` "단기과열여부"; `short_over_cls_code` "단기과열구분코드" | `inquire-price` (K4 L101), `inquire-price-2` (K6 L43, L50) |
| 정리매매 | `sltr_yn` "정리매매여부" / "정리매매 여부" | `inquire-price` (K4 L102), `inquire-price-2` (K6 L70), `inquire-overtime-price` (K10 L43) |
| Other flags | `stange_runup_yn` "이상급등여부", `ssts_hot_yn` "공매도과열 여부", `low_current_yn` "저유동성 종목 여부", `insn_pbnt_yn` "불성실 공시 여부" | `inquire-price-2` (K6 L46–48, L60) |
| Instrument state | `iscd_stat_cls_code` "종목 상태 구분 코드" | `inquire-price` (K4 L22) |

**`inquire-vi-status` (K11, K12):**

- Request codes (K11 L47–54): `fid_div_cls_code` "0:전체 1:상승 2:하락";
  `fid_cond_scr_div_code` "20139"; `fid_mrkt_cls_code` "0:전체 K:거래소
  Q:코스닥"; `fid_input_iscd` "종목코드"; `fid_rank_sort_cls_code`
  "0:전체 1:정적 2:동적 3:정적&동적"; `fid_input_date_1` "영업일".
- Response columns (K12 L27–39): `bsop_date` "영업 일자",
  `cntg_vi_hour` "VI발동시간", `vi_cncl_hour` "VI해제시간",
  `vi_kind_code` "VI종류코드", `vi_prc` "VI발동가격", `vi_stnd_prc`
  "정적VI발동기준가격", `vi_dprt` "정적VI발동괴리율", `vi_dmc_stnd_prc`
  "동적VI발동기준가격", `vi_dmc_dprt` "동적VI발동괴리율", `vi_count`
  "VI발동횟수".
- **No venue selector:** `fid_mrkt_cls_code` selects a market (거래소 /
  코스닥), not KRX vs NXT. Whether NXT VIs are included: **not
  documented**.
- Paging follows `tr_cont` "M" only (K11 L138), whereas K1 follows "M"
  and "F" (K1 L98).

### 2.8 Contradictions and gaps

1. **Same column, different labels:** `vi_cls_code` is "VI적용구분코드" on
   the quote routes (K4 L96) but "VI발동상태" on `inquire-vi-status`
   (K12 L29).
2. **관리종목 encodings disagree by name:** `mang_issu_cls_code` (a code)
   is labelled "관리종목여부" (K4 L103); `inquire-price-2` uses
   `mang_issu_yn` (K6 L41); `inquire-overtime-price` has both a `_yn` and a
   `_cls_name` (K10 L44, L23).
3. **Two halt flags:** `temp_stop_yn` "임시 정지 여부" on `inquire-price`
   (K4 L27) vs `trht_yn` "거래정지 여부" on `inquire-price-2` (K6 L71).
   Whether they are the same condition: **not documented**.
4. **TR id spelling:** the cadence note says "TCA0903R" (K1 L36); the code
   sends "CTCA0903R" (K1 L70).
5. **Legacy copy-paste:** the legacy comment on `BASS_DT` reads "시장 분류
   코드 J : 주식/ETF/ETN, W: ELW" (K25 L1342), a market-code text on a
   date field.
6. **`market-time` path vs title:** an equity path
   (`/uapi/domestic-stock/…`, K17 L22) and an equity category
   "[국내주식] 업종/기타" carry the title "국내선물 영업일조회" (K17 L18).
7. **VI route category:** the header says "[국내주식] 기본시세" (K11 L21);
   the docstring says "[국내주식] 업종/기타" (K11 L42).
8. **Typo:** "시장 경구 구분 명" (K10 L49) for `mrkt_warn_cls_name`.
9. **Hours appear only in docstrings** of two unrelated route families
   (K19, K20), KRX only. No NXT hours.
10. **Paper TR rewrite:** K22 L453–455 turns `CTCA0903R` / `CTPF1002R`
    into `VTCA0903R` / `VTPF1002R` in paper mode. No source says these
    paper ids exist.
11. **Publisher tick tables are undated beyond "2023년 기준"** and
    venue-blind (K26, K27); they are client code, not a published rule.

### 2.9 Gates and not-verified items

See §10 and §11. KIS-specific: every response statement above rests on
sample-code column maps only; the KIS portal field tables must be
retrieved and pinned before any decoder reads these columns.

## 3. Kiwoom REST

### 3.1 Pinned sources

All sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@c7a3d254`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/c7a3d25449ed4b4238bef378780c41103c67b9e9).
The full SHA is `c7a3d25449ed4b4238bef378780c41103c67b9e9`; the trade audit
records the commit date 2026-09-15T15:12:16+09:00 and that the earlier pin
`953e5dbff123f437ab4d11a78a95191a685eb51f` names the same tree
`4eb7d5497f4155ace73d8d37a03f3dc18abbe6fa`, so blob pins are identical
under both. Files were fetched 07:47:59–07:51:03.

In the links, `…/종목정보/` stands for
`examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/`
(`examples/국내주식/종목정보/`) and `…/시세/` for
`examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%9C%EC%84%B8/`.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field tables** and examples: `ka10001` (L1259–1821), `ka10003` (L2305–2547), `ka10007` (L3857–5209), `ka10017` (L7261–7593), `ka10030` (L11040–11462), `ka10054` (L17285–17667), `ka10087` (L25409–25981), `ka10099` (L27524–27786), `ka10100` (L27787–28039), `kt10000` (L52180–52362); WebSocket names `0B` (L97347), `0D` (L99093), `0g` (L102548), `0s` (L103234), `1h` (L104222) |
| W2 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | PRD items L3505 (`ka10001`), L7205 (`ka10007`), L4118 (`ka10017`), L5216 (`ka10054`), L6019 (`ka10099`), L6112 (`ka10100`), L11196 (`ka10030`); MOCK items L37042, L40742, L37655, L38753, L39556, L39649, L44733. Spot-checked: the `orderWarning` text repeats at L6071, L6164, L39608, L39701. |
| W3 | [`…/종목정보/get_domestic_stock_info.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_info.py) | `c39741c73f0f8bdbc47694de24abf3cbaaf1d402` | `ka10001` example client (L2, L18–19) |
| W4 | [`…/시세/get_domestic_stock_market_condition_info.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%9C%EC%84%B8/get_domestic_stock_market_condition_info.py) | `45aabe5e32d49eeab93cc4314e12015167893b19` | `ka10007` example client (L2, L18–19) |
| W5 | [`…/종목정보/get_domestic_upper_lower_limit_stocks.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_upper_lower_limit_stocks.py) | `d35f02f090219cbc4832927fcd6eaed27e86737c` | `ka10017` example client (L2, L18–19, L108) |
| W6 | [`…/종목정보/get_domestic_vi_triggered_stocks.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_vi_triggered_stocks.py) | `5487a7a411f8b2032e986c3e9ec660ac87f1d72a` | `ka10054` example client (L2, L18–19, L118) |
| W7 | [`…/종목정보/list_domestic_stocks.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/list_domestic_stocks.py) | `3197c003b534dc9804fc83d41805055b9b74b783` | `ka10099` example client (L2, L18–19) |
| W8 | [`…/종목정보/get_domestic_stock_detail.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_detail.py) | `b112ec61821a15e4c8ffe447a140a73dfbbba737` | `ka10100` example client (L2, L18–19) |

W3–W8 restate the W1 route, path and request descriptions; they add no
market-operations semantics. The repository `README.md`
(`018e50aad8156d18f057135a91ce2a15d09ce2d2`) and `kiwoom/core/client.py`
(`52d915c9e2f38f21885efbc428d3b50593a452c9`) were searched for
휴장 / 영업일 / 운영시간 / 호가단위 / 상한가 / clock times; no relevant hit
(README L338 "장시간 실행" means a long-running process).

**Missing evidence:**

- No REST holiday / calendar route, tick-size field or session-schedule
  route was found in W1 (searched: 휴장, 영업일, 개장일, 장운영, 호가단위,
  틱단위, 장시작, 장마감, 정규장, 프리마켓, 애프터마켓, clock-time patterns).
- No code list for `viaplc_tp`, `state`, `auditInfo` or the VI row
  `stex_tp`.
- The Kiwoom developer portal was **not** retrieved for this audit.
- The full Kiwoom repository was **not** searched for client-side tick or
  calendar tables; only the files above were retrieved.

### 3.2 Routes

Every route is `POST` with a JSON body; the API id goes in the `api-id`
header. Each W1 `meta` lists "운영 도메인" `https://api.kiwoom.com` and
"모의투자 도메인" `https://mockapi.kiwoom.com` (e.g. W1 L1270). Whether mock
data equals production data: **not documented**.

| Route (title verbatim) | Method + path | API id | Real / paper | Purpose | Evidence |
| --- | --- | --- | --- | --- | --- |
| "주식기본정보요청" — "종목 코드로 주식 기본 정보를 조회한다." (W1 L1259–1276) | POST `/api/dostk/stkinfo` (W1 L1271) | `ka10001` | both domains listed | 상한가 / 하한가 / 기준가 | field table + example |
| "시세표성정보요청" — "종목 코드로 시세표성 정보를 조회합니다." (W1 L3857–3874) | POST `/api/dostk/mrkcond` (W1 L3869) | `ka10007` | both | 상한가 / 하한가 / 전일종가 | field table + example |
| "상하한가요청" — "상하한가 종목 정보를 조회합니다." (W1 L7261–7278) | POST `/api/dostk/stkinfo` (W1 L7273) | `ka10017` | both | symbols at / moving toward a limit | field table + example |
| "당일거래량상위요청" (W1 L11040–11057) | POST `/api/dostk/rkinfo` (W1 L11052) | `ka10030` | both | only its `mrkt_open_tp` session vocabulary is used here | field table |
| "변동성완화장치발동종목요청" — "변동성 완화 장치가 발동한 종목 정보를 조회합니다." (W1 L17285–17302) | POST `/api/dostk/stkinfo` (W1 L17297) | `ka10054` | both | VI events | field table + example |
| "종목정보 리스트" — "시장을 선택하여 종목 리스트를 조회합니다." (W1 L27524–27541) | POST `/api/dostk/stkinfo` (W1 L27536) | `ka10099` | both | per-symbol `state`, `orderWarning`, `nxtEnable` | field table + example |
| "종목정보 조회" — "종목 코드로 종목 정보를 조회합니다." (W1 L27787–27804) | POST `/api/dostk/stkinfo` (W1 L27799) | `ka10100` | both | same fields for one code | field table + example |

WebSocket, names only (W1 `meta`, POST `/api/dostk/websocket`):
`0s` "장시작시간" — "장 시작 전, 장 종료 후, 시간 외 등에 알림" (W1 L103250);
`1h` "VI발동/해제" — "VI발동 및 해제 정보를 수신합니다." (W1 L104238);
`0g` "주식종목정보" — "임의연장, 관리종목 변경, VI발동, 조기 종료등 시장 조치가
있을 때 발생하는 실시간 타입" (W1 L102564).

### 3.3 Tick size (호가단위)

- **Route / field:** not found.
- **Names that contain "호가단위" but are prices:** `ka10003`
  `pri_sel_bid_unit` "우선매도호가단위" and `pri_buy_bid_unit`
  "우선매수호가단위", both "단위: 원, 부호가 포함된 숫자" (W1 L2464, L2474).
  In the example they hold price levels equal to traded prices, e.g.
  `"cur_prc": "+68900"` next to `"pri_sel_bid_unit": "+68900"` (W1 L2546).
  **Inference:** these are best quotes, not tick sizes. The trade audit
  reads them the same way.
- `tic_scope` "틱범위" on chart routes is a bar size, not a price tick.
- **Venue:** not applicable (no field).

### 3.4 Price limits (상한가 / 하한가 / 기준가)

| Route | 상한가 | 하한가 | 기준가 | 전일종가 |
| --- | --- | --- | --- | --- |
| `ka10001` | `upl_pric` "상한가", String 20, "단위: 원, 부호가 포함된 숫자" (W1 L1638) | `lst_pric` "하한가", same (W1 L1648) | `base_pric` "기준가", String 20, "단위: 원" (W1 L1658) | none |
| `ka10007` | `upl_pric` (W1 L4026) | `lst_pric` (W1 L4036) | none | `pred_close_pric` "전일종가", "단위: 원" (W1 L4006) |
| `ka10099` / `ka10100` | none | none | none | `lastPrice` "전일종가", "단위: 원, 좌측 0-padding 처리된 부호 포함 8자리 숫자" (W1 L27693; L27946) |

- **Signed limits:** both limit fields are documented as signed numbers;
  `base_pric` and `pred_close_pric` are not. What the sign means: **not
  documented**.
- **`ka10007` example** (W1 L5208): `"pred_close_pric": "135300"`,
  `"upl_pric": "+175800"`, `"lst_pric": "-94800"`.
  **Inference:** 175800 / 135300 ≈ 1.2993 and 94800 / 135300 ≈ 0.7007, so
  the `-` on `lst_pric` is a direction marker relative to the reference,
  not a negative price. This matches the candle audit's reading of signed
  Kiwoom prices. It is not documented.
- **`ka10001` example is misaligned** (W1 L1820): `"upl_pric": "20241016"`,
  `"lst_pric": "-47.41"`, `"base_pric": "20231024"`,
  `"250hgst_pric_dt": "3"`, `"cur_prc": "0.00"`. **Inference:** the sample
  values are shifted against the field list. This example cannot support
  any limit or 기준가 semantics.
- **Limit-state markers:** `pre_sig` "대비기호" (`ka10001`, W1 L1738),
  `smbol` "부호" (`ka10007`, W1 L4076) and `pred_pre_sig` (`ka10017`,
  W1 L7490): "1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락".
- **`ka10017` 상하한가요청 request:** `mrkt_tp` "000:전체, 001:코스피,
  101:코스닥" (W1 L7324); `updown_tp` "1:상한, 2:상승, 3:보합, 4: 하한,
  5:하락, 6:전일상한, 7:전일하한" (W1 L7334); `stex_tp` "1:KRX, 2:NXT
  3.통합" (W1 L7394). The response list `updown_pric` (W1 L7440) has no
  limit-price field, only `cur_prc`, `pred_pre_sig`, quotes and `cnt`
  "횟수" (W1 L7480–7580).
- **Venue:** `ka10001` / `ka10007` select the venue by `stk_cd` "거래소별
  종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)" (W1 L1322; L3920).
  Whether limits or 기준가 differ per venue: **not documented**.
- **After-hours:** `ka10087` 시간외단일가요청 has no limit or 기준가 field
  (W1 L25409–25981): **not found**.
- **기준가 vs 전일종가:** distinct fields on different routes
  (`base_pric` vs `pred_close_pric` / `lastPrice`). Relationship: **not
  documented**.

### 3.5 Trading sessions and hours

- **REST session schedule:** not found.
- **REST session vocabulary** (request filters, no clock times):
  - `ka10030` `mrkt_open_tp` "장운영구분": "0:전체조회, 1:장중, 2:장전시간외,
    3:장후시간외" (W1 L11173).
  - `ka10054` `bf_mkrt_tp` "장전구분": "0:전체, 1:정규시장,2:시간외단일가"
    (W1 L17358).
  - Order type `trde_tp` on `kt10000` lists "81:장마감후시간외 ,
    61:장시작전시간외, 62:시간외단일가" among others (W1 L52283). Orders are
    out of scope; recorded only as vocabulary.
- **No market-phase field in any REST response** retrieved here.
- **WebSocket, by name only:** `0s` 장시작시간 carries field `215`
  "장운영구분" whose description is a code list annotated with KRX clock
  times (for example "3 : 장시작(09:00)") and NXT phase codes ("P : NXT
  프리마켓 시작 알림" …) **without** clock times (W1 L103473–103480). `0B`
  has `290` "장구분" (W1 L97347) and `0D` has `215` "장운영구분"
  (W1 L99093). These are the only Kiwoom publisher statements with session
  times found; they are WebSocket field tables and are not detailed here.
- **API service hours:** not found.

### 3.6 Holiday / trading calendar

- **REST route:** not found (W1 descriptions and meta searched for 휴장,
  영업일, 개장일; W2 searched for 휴장 and 영업일).
- WebSocket `0s` signals phase changes (§3.5); it is not a calendar.
- The capability inventory records the same result.

### 3.7 Instrument / market status

**VI — `ka10054`:**

- Request (W1 L17348–17468): `mrkt_tp` "000:전체, 001: 코스피,
  101:코스닥"; `bf_mkrt_tp` (§3.5); `stk_cd` (venue suffix, "공백입력시
  시장구분으로 설정한 전체종목조회"); `motn_tp` "0:전체, 1:정적VI, 2:동적VI,
  3:동적VI + 정적VI"; `motn_drc` "0:전체, 1:상승, 2:하락"; `stex_tp`
  "1:KRX, 2:NXT 3.통합"; `skip_stk`, a 9-flag mask whose order is
  "우선주,관리종목,투자경고/위험,투자주의,환기종목,단기과열종목,증거금100%,ETF,ETN"
  (W1 L17388).
- Response list `motn_stk` (W1 L17514–17654): `motn_pric` "발동가격";
  `dynm_dispty_rt` "동적괴리율"; `trde_cntr_proc_time` "매매체결처리시각"
  HHmmss; `virelis_time` "VI해제시각" HHmmss; `viaplc_tp` "VI적용구분" (no
  code list); `dynm_stdpc` "동적기준가격"; `static_stdpc` "정적기준가격";
  `static_dispty_rt` "정적괴리율"; `open_pric_pre_flu_rt` "시가대비등락률";
  `vimotn_cnt` "VI발동횟수"; `stex_tp` "거래소구분" (no code list).
- Example (W1 L17666): `viaplc_tp` values "동적" and "동적+정적";
  `stex_tp` values "KRX" and "NXT"; times such as "172311" and "163030".
  The rows carry **no date** field.

**Instrument state — `ka10099` / `ka10100`:**

| Field | Description (verbatim) | Source |
| --- | --- | --- |
| `orderWarning` "투자유의종목여부" | "0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달" | W1 L27753; L28016 |
| `state` "종목상태" | no description. Examples: "관리종목", "증거금100%" (W1 L27785); "증거금20%\|담보대출\|신용가능" (W1 L28038) | W1 L27703; L27956 |
| `auditInfo` "감리구분" | no description. Examples: "정상", "투자주의환기종목" (W1 L27785) | W1 L27673; L27926 |
| `nxtEnable` "NXT가능여부" | "Y: 가능"; other values not documented | W1 L27773; L28026 |

- **Trading halt:** no dedicated REST field found. **Inference:** a halt
  may surface only inside free-text `state`; not documented.
- `ka10100` takes `stk_cd` "종목코드 6자리", length 6 (W1 L27850): no
  venue suffix, so these fields are not per venue except `nxtEnable`.
- Ranking routes accept status **filters** such as `stk_cnd`
  "1:관리종목제외 … 10:우선주+관리종목+환기종목제외" (`ka10017`, W1 L7354).
  Filters are not per-symbol status output.

### 3.8 Contradictions and gaps

1. **`ka10001` example misaligned** (W1 L1820): date-like values in
   `upl_pric` / `base_pric` and a percentage in `lst_pric` (§3.4).
2. **`orderWarning` "5: 투자경과":** **Inference:** probably 투자경고. The
   list has no 투자주의 code for non-ETF symbols, and the parenthesis after
   "ETF인 경우만 전달" is never closed. The symbol-master audit records the
   same text.
3. **`bf_mkrt_tp` is labelled "장전구분"** but its values are
   "1:정규시장,2:시간외단일가" (W1 L17358).
4. **`ka10017` example** sends `"trde_qty_tp": "0000"` (W1 L7591); the
   table lists five-digit codes such as "00000:전체조회" (W1 L7364).
5. **Signed vs unsigned reference prices** (§3.4): sign meaning
   undocumented.
6. **"호가단위" in field names of price levels** (§3.3).
7. **`skip_stk` description** contains stray doubled quotes around its
   examples (`"011111111""`, W1 L17388).
8. **No code lists** for `viaplc_tp`, the VI row `stex_tp`, `state` or
   `auditInfo`; values are Korean free text in the examples.

### 3.9 Gates and not-verified items

See §10 and §11. Kiwoom-specific: price-limit fields are signed strings;
any decoder must reject or explicitly map the sign, never apply `abs()`.

## 4. LS Securities

**pending** — written in parallel (`sections/ls-db.md`); to be merged.

## 5. DB Securities

**pending** — written in parallel (`sections/ls-db.md`); to be merged.

## 6. Toss Securities

**pending** — written in parallel (`sections/toss-meritz.md`); to be
merged.

## 7. Meritz Securities

**pending** — written in parallel (`sections/toss-meritz.md`); to be
merged.

## 8. Cross-broker comparison

### 8.1 Evidence by concern

LS, DB, Toss and Meritz columns are **pending**.

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Holiday route | yes, REST, per-date flags, no venue | no | pending | pending | pending | pending |
| Session schedule route | no | no | pending | pending | pending | pending |
| Session times anywhere | REST/WS docstrings, KRX only | WS `0s` code list (KRX times; NXT phases without times) | pending | pending | pending | pending |
| Market-phase field in REST response | yes, no code list | no | pending | pending | pending | pending |
| Tick size | one undocumented column + client-code table | none | pending | pending | pending | pending |
| Upper / lower limit | yes (names only) | yes (field table, signed) | pending | pending | pending | pending |
| After-hours limits | separate `ovtm_untp_*` columns | not found | pending | pending | pending | pending |
| 기준가 distinct from 전일종가 | yes (two columns) | yes (two fields, two routes) | pending | pending | pending | pending |
| VI list route | yes, no venue selector | yes, with `stex_tp` | pending | pending | pending | pending |
| Halt flag | three (`temp_stop_yn`, `trht_yn`, `tr_stop_yn`) + NXT halt | none | pending | pending | pending | pending |
| Warning code list | none | `orderWarning` (incomplete) | pending | pending | pending | pending |
| Real / paper documented | no | domains only | pending | pending | pending | pending |

### 8.2 What a common surface could and could not rely on

All statements in this subsection are **Inference:** from KIS and
Kiwoom only; they must be revisited when §4–§7 are merged.

- **Market calendar:** KIS has a per-date flag route and Kiwoom has none.
  A common calendar could not rely on every broker offering one; it would
  need a per-broker capability flag and an explicit "unsupported" error.
  KIS's four flags (영업일, 거래일, 개장일, 결제일) are undefined relative
  to each other and to venues, so mapping any of them to "the exchange is
  open" would be a guess.
- **Session schedule:** neither broker publishes one on REST. Hard-coded
  hours from docstrings or WebSocket code lists would be publisher text,
  not a contract, and NXT hours are absent. A common surface could not
  rely on broker-supplied session times.
- **Tick size:** no broker so far documents a tick-size contract. KIS's
  `aspr_unit` is an undocumented column and its own tools use a local,
  venue-blind table. A common `tick_size` could not rely on broker
  evidence yet.
- **Price limits:** both brokers expose an upper / lower limit per symbol,
  so a nullable per-quote limit pair is the most plausible common element.
  It could not rely on a common sign convention (Kiwoom signs them), on a
  common venue rule, or on after-hours limits (KIS only).
- **기준가:** both brokers keep 기준가 separate from 전일종가. A common
  surface could not equate them.
- **Status:** VI exists on both, but with different selectors and no code
  lists. Halt, 관리 and warning flags differ in name, granularity and
  encoding; only a raw, broker-qualified status would be faithful today.

## 9. Relation to existing repository documents and models

None of the files below is edited by this change. Paths are on `main` at
`a5d2639` unless a branch is named.

| Document / model and claim | This audit |
| --- | --- |
| [`Ticker`](../../src/ktradelink/models/ticker.py) (L18, L23–45): price fields `last`, `open`, `high`, `low`, `previous_close`, `bid`, `ask`, plus `volume`, timestamps, `scope_description` and a scalar `info` mapping | **No** field for upper / lower limit, 기준가, tick size, session / market phase, or instrument status. The Rust core `Prices` (`crates/ktradelink-core/src/lib.rs` L112–117) likewise ends at `previous_close`. Adding any of them is a model change for the maintainer (§10). |
| [market-data spec](../specifications/market-data-v0.1-draft.md) L99–104: `previous_close` is the "completed regular-session official closing price" only if the native response reliably identifies it | KIS `stck_sdpr` and Kiwoom `base_pric` are **기준가**, documented separately from 전일종가 (§2.4, §3.4). They must not fill `previous_close`. |
| [offline decoder usage](../usage/offline-six-broker-ticker-decoders.md) L65–67: "DB `Sdpr` is never assigned to `previous_close`. Signed Kiwoom `cur_prc` strings fail until its native semantics are documented" | Consistent. The same applies to KIS `stck_sdpr` / Kiwoom `base_pric`, and Kiwoom's signed `upl_pric` / `lst_pric` would fail the same unsigned parser. |
| [six-broker-ticker-decoders.md](six-broker-ticker-decoders.md) L95–100: a reported zero may mean halt or sentinel (unverified); no hidden request for a "calendar or reference price" | Consistent. KIS and Kiwoom expose halt-related flags (§2.7, §3.7) whose encodings are undocumented, so zero-vs-halt stays unverified. |
| market-data spec L159–164: `session="regular"` must error rather than mislabel; "Session timestamps, DST, holidays, and exchange schedule require explicit tests" | Neither broker documents session coverage of its quote routes; KIS documents a holiday route, Kiwoom none (§8). |
| market-data spec L214–215: "suspended trading must be distinguished from missing data" | Candidate inputs exist (KIS `trht_yn` / `tr_stop_yn` / `temp_stop_yn`, Kiwoom `state`), none with a documented encoding. |
| market-data spec L250–251: verify NXT/SOR rules; "explicit KRX-only initial support is the safe option" | Consistent. KIS `nxt_tr_stop_yn` and Kiwoom `nxtEnable` show that halt / eligibility can differ per venue (§2.7, §3.7). |
| [capability inventory](capability-inventory-2026-11-05.md) row 6 (L34): KIS `CTCA0903R` · EX · K5; Kiwoom "REST NF … WS only `0s`" | **Confirmed**, same KIS blob `24c2c33c…`. Not in its scope but found here: KIS `inquire-vi-status`, `capture-uplowprice`, `search-stock-info`; Kiwoom `ka10054`, `ka10017`. |
| capability inventory L151: `market_time` is 국내선물 영업일조회 and was not used | **Confirmed** (§2.5); also the path / title contradiction (§2.8 item 6). |
| [order-book evidence](order-book-evidence-2026-11-05.md) and its synthetic fixture `tests/fixtures/order_book/kis-fhkst01010200-synthetic.json` L77, L92 (`"new_mkop_cls_code": "00"`, `"vi_cls_code": "N"`) | Those values are **invented** (fixture README L3–4) and decoders ignore them. They are not evidence of a code list; none is documented (§2.5, §2.7). |
| Symbol-master evidence (branch `claude/issue-17-symbol-master-evidence` @ `b127724ee73fac239d987a2fa2a5b889c5f92bfb`, not merged): Kiwoom `state` / `auditInfo` / `orderWarning` / `nxtEnable`; KIS master file has `trht_yn`, `mang_issu_yn`, `mrkt_alrm_cls_code` with a code list, and "NXT … not found" in the master | Kiwoom text **identical** (§3.7). For KIS, the REST `search-stock-info` route has NXT flags (`nxt_tr_stop_yn`, `cptt_trad_tr_psbl_yn`, §2.7) that the master file lacks. The master's `mrkt_alrm_cls_code` code list is not repeated by any REST column found here. |
| [Candle evidence](candle-evidence-2026-11-05.md) L207, L377: "Holidays / suspended days: not documented" for KIS and Kiwoom candles; L346–350: Kiwoom signed prices read as direction markers (inference) | Consistent; the KIS holiday route exists but candle routes do not reference it. The same sign reading applies to `lst_pric` (§3.4, inference). |
| [Trade evidence](trade-evidence-2026-11-05.md) L1418–1427 (G-V3): session coverage undocumented; KIS after-hours trades on a separate route; L355: Kiwoom `pri_*_bid_unit` read as best quotes | Consistent (§2.5, §3.3). |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any calendar, tick-size, price-limit or
status model, decoder or request plan is written. Broker tags are in
brackets. LS, DB, Toss and Meritz gates are **pending**.

### 10.1 Model scope

- **G-M1:** `Ticker` has no limit, 기준가, tick, session or status field
  (§9). Whether to add typed optional fields, a separate value type, or
  nothing is a maintainer decision; this audit does not propose one.
- **G-M2:** no public dict/JSON status surface. Raw status codes may only
  be exposed in a typed, broker-qualified form once their encodings are
  documented.

### 10.2 Calendar

- **G-C1 [KIS]:** do not map `opnd_yn`, `tr_day_yn` or `bzdy_yn` to
  "exchange open" until their meanings, value encoding and venue are
  documented or verified (§2.6).
- **G-C2 [KIS]:** respect "가급적 1일 1회 호출" (K1 L36–37): cache, no
  per-request calls, no automatic retry loop.
- **G-C3 [Kiwoom]:** no REST calendar; report the capability as
  unsupported rather than deriving holidays from empty candles.
- **G-C4:** do not hard-code an exchange holiday list from any source in
  this file; none is broker evidence.

### 10.3 Sessions

- **G-S1:** session hours from docstrings (KIS K19, K20) or WebSocket code
  lists (Kiwoom `0s`) are not contracts; do not ship them as constants.
- **G-S2 [KIS]:** `new_mkop_cls_code` / `antc_mkop_cls_code` have no code
  list; do not interpret them.
- **G-S3:** NXT session hours are not documented by either broker; any
  NXT scope stays unsupported (market-data spec L250–251).

### 10.4 Tick size

- **G-T1:** no tick-size contract exists for KIS or Kiwoom. Do not round
  or validate order prices from `aspr_unit` or from the publisher client
  tables (K26, K27) without a maintainer decision and an authoritative
  source.
- **G-T2:** no automatic price adjustment on the order path; the
  publisher's own client floors prices (K27 L120–123), which silently
  changes order intent.

### 10.5 Price limits

- **G-L1 [Kiwoom]:** `upl_pric` / `lst_pric` are signed strings; reject or
  map the sign explicitly, never `abs()`.
- **G-L2 [Kiwoom]:** do not use the `ka10001` example as a fixture (§3.4).
- **G-L3:** 기준가 ≠ 전일종가 ≠ `previous_close` (§9).
- **G-L4 [KIS]:** regular and 시간외 단일가 limits are separate columns;
  never merge them.
- **G-L5:** venue: KRX first; limits for `NX` / `UN` / `_NX` / `_AL`
  requests stay unsupported until per-venue behaviour is documented.

### 10.6 Status

- **G-X1:** no status code list is documented for KIS; Kiwoom has only the
  incomplete `orderWarning` list. Do not translate flags into a common
  enum.
- **G-X2 [KIS]:** three halt-like flags (`temp_stop_yn`, `trht_yn`,
  `tr_stop_yn`) plus `nxt_tr_stop_yn`; do not merge them without evidence.
- **G-X3 [KIS]:** `inquire-vi-status` has no venue selector; do not label
  its rows KRX or NXT.
- **G-X4 [Kiwoom]:** VI rows carry HHmmss times without a date; require a
  verified trading date (market-data spec §5).

### 10.7 Environment and requests

- **G-E1:** real/paper availability of every route here is undocumented
  for KIS and only domain-listed for Kiwoom. No silent LIVE/PAPER
  fallback; the KIS `C…`→`V…` paper rewrite (K22 L453–455) must not be
  assumed to name a real paper TR.
- **G-E2:** every route here needs authentication. Any real request needs a
  separate explicit authorization (AGENTS.md); none was made.

## 11. Not verified

- Any live or paper response for any route above. No broker API request
  was sent.
- Entitlements and real/paper parity for both brokers.
- KIS:
  - JSON types, units, signs and value encodings of every column in
    §2.3–§2.7 (the portal specification was not retrieved);
  - code lists for `new_mkop_cls_code`, `antc_mkop_cls_code`,
    `iscd_stat_cls_code`, `vi_cls_code`, `vi_kind_code`,
    `mrkt_warn_cls_code`, `mang_issu_cls_code`, `short_over_cls_code`,
    `mxpr_llam_cls_code`, `wday_dvsn_cd`;
  - meaning of `aspr_unit` and of `rstc_wdth_prc`;
  - how many dates `chk-holiday` returns and its venue scope; paper
    support of `CTCA0903R` / `CTPF1002R`;
  - per-venue (`J` / `NX` / `UN`) behaviour of limits, 기준가 and status;
  - whether `inquire-vi-status` includes NXT VIs;
  - the relationship between `temp_stop_yn`, `trht_yn` and `tr_stop_yn`.
- Kiwoom:
  - meaning of the sign on `upl_pric` / `lst_pric`;
  - per-venue limits for `_NX` / `_AL` codes;
  - code lists for `viaplc_tp`, `state`, `auditInfo`, VI-row `stex_tp`;
  - the intended `orderWarning` code 5 label and any missing codes;
  - whether a halt appears in `state`;
  - whether mock-domain data matches production.
- LS, DB, Toss and Meritz: **pending** (§4–§7).
- Exchange rules (tick tables, limit widths, session hours, holidays) were
  deliberately not consulted; nothing here states them.
