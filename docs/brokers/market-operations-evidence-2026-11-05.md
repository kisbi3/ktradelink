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
  value or order was used. Only public Git repositories, public
  documentation pages and publisher JSON documentation endpoints were
  fetched. No exchange (KRX/NXT) rulebook was fetched or cited: exchange
  rules are not broker evidence. Data-use and redistribution terms were
  out of scope by maintainer instruction.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS and Kiwoom: single files at fixed Git commits, fetched
    07:45:10–07:51:03 over HTTPS from
    `raw.githubusercontent.com/<owner>/<repo>/<full commit SHA>/<path>`.
    Git blob SHAs were computed locally from the retrieved bytes.
  - LS portal catalog and guide pages: 07:43:44–07:47:01; one t8453 copy
    reused from 07:11:28 (§4.1).
  - DB repository at a fixed commit, re-fetched 07:48:18; DB portal JSON
    endpoints 07:48:56–07:50:43 (§5.1).
  - Toss portal documents: 07:43:41–07:43:46 (§6.1).
  - Meritz portal: 07:45:15–07:45:18; Meritz repository at a fixed commit,
    cloned 07:45:19 (§7.1).
- **Cross-check with earlier audits:**
  - Fourteen KIS/Kiwoom blobs cited here were already pinned by the
    capability-inventory, order-book, candle, trade or symbol-master
    audits, and the copies retrieved for this file hash identically: K1,
    K7, K8, K21 (KRX file), K22–K25, K29; W1, W2, W7, W8 and Kiwoom
    `kiwoom/core/client.py` (§2.1, §3.1). The KIS and Kiwoom commit dates
    are quoted from the trade audit; this audit did not read those commit
    objects itself.
  - The LS catalog L1, the DB commit, the Toss documents and the Meritz
    spec export are byte- or content-identical to the copies pinned by the
    trade audit (§4.1, §5.1, §6.1, §7.1).
- **Spot re-check before merge:** for each of LS, DB, Toss and Meritz at
  least two pins were recomputed from the retrieved copies, and the cited
  lines were re-read; all matched (§8.4).
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
  - `publisher guide`: portal prose outside the API specification (for
    example the LS and Toss FAQs, the DB and Meritz API descriptions). It
    ranks below `field table`; the Toss FAQ itself defers to the API
    reference.
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
| Tick size (호가단위) | `aspr_unit` "호가단위" column on `inquire-price` only; no route, no type, no venue rule — E. A 7-band table "2023년 기준" in backtester / strategy-builder code — C (not a contract) | **not found** (no field, no route). `pri_sel_bid_unit` "우선매도호가단위" is a best-quote price, not a tick size (inference from E) | **not found**; `memedan` "수량단위" is a quantity unit — F | **not found**; reactive order code `2706` "주문가격의 호가단위를 확인하십시오."; a notebook comment "호가단위는 가격대별 상이" — C | no field; only `data.tickSize` in a rejected order (`400 invalid-request`); one band given as an example in `OrderCreateRequest.price` — F | `aspr_unit` "호가 단위입니다." (Number) on `/market/v1/prices`; guide: order price must match it — F+G. 6-row KRX table "2023-01-25 개편 기준" in repo code — C (not a contract) |
| Price limits | `stck_mxpr` "주식 상한가" / `stck_llam` "주식 하한가" on `inquire-price`, `inquire-price-2`, `capture-uplowprice`; `ovtm_untp_mxpr`/`ovtm_untp_llam` for 시간외 단일가 — E; types and signs not documented | `upl_pric` "상한가" / `lst_pric` "하한가", "단위: 원, 부호가 포함된 숫자", on `ka10001` and `ka10007` — F; `ka10001` example values misaligned (E) | `uplmtprice` / `dnlmtprice` (Number) on t1102, t1101, t8450, t8407, t8430, t8436; `highend`/`lowend` on charts; one pair per route — F+E | `Mxpr` "상한가" / `Llam` "하한가" (strings) on `PRICE` / `MULTIPRICE`; index rows return `""` — F+E | `GET /api/v1/price-limits`: `upperLimitPrice` / `lowerLimitPrice`, decimal string or `null`, "당일", no venue or date input — F | `mxpr` / `llam` "당일 주문 가능한 최고/최저 가격" on prices and orderbook; after-hours `ovtm_untp_*` may be (or always are) 0, "가격 범위 판단에 쓰지 마십시오" — F |
| 기준가 vs 전일종가 | separate columns `stck_sdpr` "주식 기준가" and `stck_prdy_clpr` "주식 전일 종가" on `inquire-price-2`; relation not documented — E | `base_pric` "기준가" (`ka10001`) vs `pred_close_pric` "전일종가" (`ka10007`), `lastPrice` "전일종가" (`ka10099`/`ka10100`); relation not documented — F | t8430/t8436 carry both `jnilclose` "전일가" and `recprice` "기준가"; t1102 `recprice` only; t8450 labels `jnilclose` "전일종가(기준가)" — F | `Sdpr` "기준가" only; no 전일종가 field — F | 기준가 only as `RankingPrice.basePrice` in rankings; FAQ: daily `closePrice` "등락률 계산 기준가와 다를 수 있습니다" — F+G | `sdpr` "당일 기준가(전일 종가)"; candle route: "전일 정규장 종가(기준가)" — F |
| Session hours | **no REST schedule**. Prose only: "장시간(09:00~15:30)" (REST docstring), "시간외 단일가(16:00~18:00)" (WebSocket docstrings) — E | **no REST schedule**. Clock times only in the WebSocket `0s` 장운영구분 code list — F (WS) | chart summary blocks `s_time`/`e_time` and KRX/NXT pre/after times (t8451–t8453), meaning undescribed; FAQ: paper fills only in "정규장 시간(09:00~15:30)" — F+E+G | KRX: **not found**. NXT order-acceptance windows in the `CSPAT00610` description (overlapping) — G | `GET /api/v1/market-calendar/KR`: per-session times, KRX+NXT union, KST; no per-venue times — F+G | `GET /reference/v1/market-hours` timetable per KRX segment (9-digit "HHMMSS"); `market-days` `sta_hour`/`fin_hour`; no NXT code — F |
| Market-phase code (REST) | `new_mkop_cls_code` "신 장운영 구분 코드", `antc_mkop_cls_code` "예상 장운영 구분 코드" on `inquire-asking-price-exp-ccn`; **no code list** — E | none in responses; request filters only (`ka10030` `mrkt_open_tp`, `ka10054` `bf_mkrt_tp`) — F | none; t1102 `janginfo` "장구분" is the market; `ho_status` "동시구분" has no code list; WS `JIF` only — F | none on quote routes; `DAYTRADE` `InputHourClsCode` is a request filter; WS `S00` `NewMkopclscode` (name) — F | none; timetable only — F | `mkop_cls_code` and five sibling codes on `market-hours`, `nw_mkop_cls_code` / `shrn_mkop_cls_code` on orderbook; **names "제공되지 않습니다"**; "000" is not a close signal — F |
| Holiday / calendar | `CTCA0903R` GET `…/quotations/chk-holiday`, `BASS_DT` YYYYMMDD → `bzdy_yn` 영업일, `tr_day_yn` 거래일, `opnd_yn` 개장일, `sttl_day_yn` 결제일; "가급적 1일 1회 호출" — E | **not found** (REST); WebSocket `0s` 장시작시간 only — F | **not found**; `t0167` is a server clock — F | **not found** (SDK API inventory, name search) — C+G | `market-calendar/KR`: previous, current and next business day only; `integrated: null` = holiday — F+G | `GET /reference/v1/market-days`: five business dates around "now", no date input, **no holiday flag** — F |
| VI | route `FHPST01390000` `inquire-vi-status` (static/dynamic, times, prices); `vi_cls_code` on quote routes; no code lists; no venue selector — E | route `ka10054` with `stex_tp` "1:KRX, 2:NXT 3.통합" and per-row `stex_tp`; `viaplc_tp` without code list — F+E | static-VI prices `svi_*` / `nxt_svi_*` on t1102; trigger only as text `shterm_text`; dynamic VI not found; WS `VI_`/`DVI`/`NVI`/`UVI` — F | **not found** (REST and WS field names) — F+C | `/stocks/{symbol}/warnings` `VI_STATIC` / `VI_DYNAMIC` / `VI_STATIC_AND_DYNAMIC`, with `exchange`, date granularity only — F | **not found** (domestic) — F |
| Halt / 관리 / warnings | `temp_stop_yn`, `trht_yn`, `tr_stop_yn`, `nxt_tr_stop_yn` "NXT 거래정지여부", `mang_issu_*`, `admn_item_yn`, `mrkt_warn_cls_code`, `invt_caful_yn`, `short_over_yn`, `sltr_yn` …; **no value encodings** — E | `orderWarning` code list "0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: …"; free-text `state`, `auditInfo`; `nxtEnable`; no halt field — F+E | t1102 display text `info1`–`info5`, `shterm_text` (no code lists); list TRs t1404/t1405 with `jongchk` codes; t9945 `nxt_chk` — F | **none on REST**; WS `S00` names `TrhtYn`, `MangIssuyn`, `WarnYn` — C | `krxTradingSuspended`, `nxtTradingSuspended`, `liquidationTrading`; warnings `OVERHEATED`, `INVESTMENT_WARNING`, `INVESTMENT_RISK`; 관리종목 and 투자주의 not found — F | `issu_stat_cls_code` (no list), `tmpr_susp_yn`, `sltr_yn`, free-text `invt_epmd_cntt`; order-response `warn_cls_code`; `oder_stop_yn` — F |

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

### 4.1 Pinned sources

All LS sources are public resources on `https://openapi.ls-sec.co.kr`
without an immutable revision; only L1 carries a publisher version marker.
Each sha256 prefix identifies only the copy retrieved at the stated UTC time
on 2026-11-05. Detail-page URLs are `…/guide/api/<data-tr>?type=rest&api=<data-api>`
with ids read from L2; the `api=` ids are `54a99b02-dbba-4057-8756-9ac759c9a2ed`
(`[주식] 시세`, `/stock/market-data`), `316495d3-6109-45a6-baaf-9e8a0261f30a`
(`[주식] 기타`, `/stock/etc`) and `3c452f0d-715e-43b5-a140-3e26f73dec76`
(`[기타] 시간조회`, `/etc/time-search`). L1 line numbers refer to the
pretty-printed catalog (89,446 lines). L1 is byte-identical to the catalog
pinned by the trade and candle audits (same sha256 prefix and version).

| # | Path / URL | Pin (sha256 prefix, UTC retrieval, revision) | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true | `9aaca437f1925115`, 07:43:44Z, 2,792,313 bytes; publisher `"version" : "20261026021444748"` (unchanged) | TR discovery and keyword sweep of every field; field tables, TPS, line numbers |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `732213d7561df1e4`, 07:44:48Z (page varies per request) | `data-api` / `data-tr` ids |
| L3 | `…/guide/api/wqs8bq62-huk0-wb6z-7x83-nt78d4ax2yb6?type=rest&api=54a99b02-…` (t1102) | `42712ce969a8a480`, 07:45:10Z | Field table, request example, response example |
| L4 | `…/guide/api/8tb7j8m8-5vb7-jzit-2284-1uc2rte784zb?type=rest&api=54a99b02-…` (t1101) | `e3bdd31adba31afb`, 07:45:07Z | Same |
| L5 | `…/guide/api/3691b2fa-67dc-49a5-aaaf-40aaf52c7bfb?type=rest&api=54a99b02-…` (t8450) | `0f663f3a7ab7095c`, 07:45:26Z | Same; NXT example |
| L6 | `…/guide/api/0xh85bca-blus-l8gm-685p-2tjnzb2k34pp?type=rest&api=54a99b02-…` (t8407) | `4b24594cd34020e3`, 07:45:24Z | Same; 3-symbol example |
| L7 | `…/guide/api/ir3h1jd3-6q1q-lrz6-51wl-88u4t8748hre?type=rest&api=316495d3-…` (t8430) | `5b017d334785e9fd`, 07:45:30Z | Same |
| L8 | `…/guide/api/10b608pg-043k-l8qc-587y-3hz6xy0c1b7r?type=rest&api=316495d3-…` (t8436) | `efbc50d023d9e06b`, 07:45:32Z | Same |
| L9 | `…/guide/api/u4hepin5-rfe4-3g3p-8yn3-7xko30x5hm5z?type=rest&api=54a99b02-…` (t9945) | `47a2ce86b41d3379`, 07:45:28Z | Same |
| L10 | `…/guide/api/7gc27jom-y6q6-fc24-q83c-l5t8ssxgwz13?type=rest&api=54a99b02-…` (t1404) | `4b23565549827a92`, 07:45:13Z | Same |
| L11 | `…/guide/api/rg2c22ji-2735-wfp8-4f47-x3a1j8f46865?type=rest&api=54a99b02-…` (t1405) | `d7e9df6ff5b80780`, 07:45:15Z | Same |
| L12 | `…/guide/api/zl807q83-e7b5-jb4p-5z4s-31b6148yiy6b?type=rest&api=54a99b02-…` (t1410) | `23e2a59658823278`, 07:45:17Z | Same |
| L13 | `…/guide/api/ifbnu5gu-g826-qa0s-tyl8-68854p8y34wb?type=rest&api=54a99b02-…` (t1422) | `5184e697784f5d06`, 07:45:19Z | Same |
| L14 | `…/guide/api/fxs7d671-z0s4-l4v3-1b8j-x416l2wc7t85?type=rest&api=54a99b02-…` (t1427) | `34d40f83db32cbbb`, 07:45:21Z | Same |
| L15 | `…/guide/api/d3yk1m28-slea-1sfn-0072-fjd1bu38p5h4?type=rest&api=3c452f0d-…` (t0167) | `0beef333e8733fe7`, 07:45:35Z | Same |
| L16 | `…/guide/api/9def2199-03ab-4a51-8275-e4db07ef35ce?type=rest&api=12320341-ad85-429a-90bd-5b3771c5e89f` (t8453) | `d2686195e356c5da`, retrieved 07:11:28Z for the trade audit (its L9); copy reused and re-hashed, not re-fetched | Session-time summary example values |
| L17 | https://openapi.ls-sec.co.kr/community-faq (302 → `/community/10000000-0000-0011-0000-000000000002`) | `418dff4e509da79f`, 07:47:01Z (differs from the trade/candle audit copies; page varies) | Paper-server hours prose (`publisher guide`) |

**Missing evidence:**

- No publisher Git repository or SDK for LS REST; every fact is from the
  portal (field table, publisher example or FAQ prose).
- Tick size: no route, field or publisher table (§4.3).
- Holiday / trading calendar: no route (§4.6).
- No code list for any REST status text field (`info1`–`info5`,
  `shterm_text`, `janginfo`) or for `ho_status` (§4.5, §4.7).
- No statement of the API's own service hours; paper hours appear only in
  FAQ prose.

### 4.2 Routes

Common transport is as recorded in the trade audit §4.2: `POST`, one REST
origin `https://openapi.ls-sec.co.kr:8080` (L1 `servers`), headers
`content-type`, `authorization`, `tr_cd`, `tr_cont`, `tr_cont_key`,
`mac_address`; body `{"<tr>InBlock": {...}}`. L1 lists a `simulationUrl`
only for WEBSOCKET, so a separate paper REST origin is **not documented**.
Envelope `rsp_cd`/`rsp_msg` with success `"00000"` in every example below.

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Purpose | Evidence |
| --- | --- | --- | --- | --- | --- |
| "주식현재가(시세)조회" | `POST /stock/market-data` | `t1102` (TPS `10`, L1 L18309) | one REST origin; paper REST not documented | 상/하한가, 기준가, 정적VI 가격, status text fields, `janginfo` | field table (L1, L3), publisher example (L3) |
| "주식현재가호가조회" | `POST /stock/market-data` | `t1101` (TPS `10`, L1 L17767) | as above | 상/하한가, 전일종가, `ho_status` | field table, publisher example (L4) |
| "(통합)주식현재가호가조회2 API용" | `POST /stock/market-data` | `t8450` (TPS `10`, L1 L23118) | as above | 상/하한가 with venue selector; `ho_status` / `nxt_ho_status` | field table, publisher example (L5) |
| "API용주식멀티현재가조회" | `POST /stock/market-data` | `t8407` (TPS `5`, L1 L22914) | as above | 상/하한가 for several symbols | field table, publisher example (L6) |
| "주식종목조회" | `POST /stock/etc` | `t8430` (TPS `2`, L1 L15327) | as above | Master list with 상/하한가, 전일가, 기준가 | field table, publisher example (L7) |
| "주식종목조회 API용" | `POST /stock/etc` | `t8436` (TPS `2`, L1 L15464) | as above | Same plus `bu12gubun`, `spac_gubun` | field table, publisher example (L8) |
| "주식마스터조회API용" | `POST /stock/market-data` | `t9945` (TPS `2`, L1 L24038) | as above | Master list; only status-like field is `nxt_chk` | field table, publisher example (L9) |
| "관리/불성실/투자유의조회" | `POST /stock/market-data` | `t1404` (TPS `1`, L1 L20795) | as above | List of designated symbols by category | field table, publisher example (L10) |
| "투자경고/매매정지/정리매매조회" | `POST /stock/market-data` | `t1405` (TPS `1`, L1 L20970) | as above | Same, other categories | field table, publisher example (L11) |
| "초저유동성조회" | `POST /stock/market-data` | `t1410` (TPS `1`, L1 L21125) | as above | Low-liquidity / low-PBR list | field table, publisher example (L12) |
| "상/하한" | `POST /stock/market-data` | `t1422` (TPS `2`, L1 L21270) | as above | Symbols at 상한/하한 | field table, publisher example (L13) |
| "상/하한가직전" | `POST /stock/market-data` | `t1427` (TPS `2`, L1 L21497) | as above | Symbols near 상한/하한 | field table, publisher example (L14) |
| "서버시간조회" | `POST /etc/time-search` | `t0167` (TPS `10`, L1 L88569) | as above | Server date and time | field table, publisher example (L15) |
| Chart TRs (titles in the candle audit) | `POST /stock/chart` | `t8410`–`t8412`, `t8451`–`t8453` | as above | Summary-block 상/하한가, 정적VI, session start/end times | field table (L1), publisher example (L16) |

WebSocket feeds, name and id only (not detailed): `JIF` "장운영정보"
(L1 L88633; its table has `jangubun` "장구분" and `jstatus` "장상태" code
lists), `VI_` "VI발동해제" (L1 L31224), `DVI` "시간외단일가VI발동해제"
(L1 L25400), `NVI` "(NXT)VI 발동 해제" (L1 L33598), `UVI` "(통합)VI발동해제"
(L1 L38042).

### 4.3 Tick size (호가단위)

**Not found.**

- No dedicated route. A sweep of every L1 field (element, name, description)
  for `호가단위|틱단위|호가 단위|tick|unit` under `/stock` and `/etc` hits
  only ELW `t1969` (`onetickgubun` "LP갭1틱", `tickvalue` "1틱환산") and
  `t1449` `tickdiff` "등락율" — none is an equity tick size.
- No unit field in quote responses. `memedan` is "수량단위" (t1102, L1
  L18535) / "주문수량단위" (t8430, L1 L15446), String 5, example `"00001"`
  (L3, L7). By its label it is an order-quantity unit, not a price tick.
- KRX vs NXT tick difference: not documented.
- No publisher client code exists for LS REST, so there is no hard-coded
  tick table either.

### 4.4 Price limits (상한가 / 하한가 / 기준가)

| TR | 상한 / 하한 field (verbatim name) | Base field(s) | Venue selector | Example (L3–L8) |
| --- | --- | --- | --- | --- |
| t1102 | `uplmtprice` "상한가(최고호가가격)", `dnlmtprice` "하한가(최저호가가격)", Number 8 (L1 L18440, L18445) | `recprice` "기준가(평가가격)" Number 8 (L18430); `krx_mcls_price` "KRX정규종가" (L19225, `required: false`); **no** `jnilclose` | `exchgubun` optional: "K: KRX / N: NXT / U:통합 / 그외 입력값은 KRX로 처리" (L18360) | `"078020"`, `U`: recprice 6710, 8720 / 4700 |
| t1101 | `uplmtprice` "상한가", `dnlmtprice` "하한가" (L18256, L18261) | `jnilclose` "전일종가" (L17881) | **none** | `"078020"`: 4525, 5880 / 3170 |
| t8450 | `uplmtprice` "상한가", `dnlmtprice` "하한가" (L23503, L23508) | `jnilclose` "전일종가(기준가)" (L23238) | `exchgubun` **required**, same code text (L23169) | `"010950"`, `N`, `ex_shcode` `"N010950"`: 60200, 78200 / 42200 |
| t8407 | `uplmtprice`, `dnlmtprice` (L23105, L23110) | `jnilclose` "전일종가" (L23100) | **none** | 3 rows, e.g. `"005930"`: 72200, 93800 / 50600 |
| t8430 | `uplmtprice` "상한가", `dnlmtprice` "하한가" (L15431, L15436) | `jnilclose` "전일가" (L15441) **and** `recprice` "기준가" (L15451) | **none**; request `gubun` "구분(0:전체1:코스피2:코스닥)" | `"000020"`: 전일가 10550, 기준가 10550, 13710 / 7390 |
| t8436 | same fields (L15569 …) | `jnilclose` "전일가" and `recprice` "기준가" (L15589) | **none** | `"005385"`: 107900 / 107900, 140200 / 75600 |
| t1427 | `lmtprice` "상한가/하한가" (L21686) | — | none | `"328380"`: 1574 |
| Charts | `highend` "상한가", `lowend` "하한가": Number in t8410–t8412, **String** in t8451–t8453 (t8410 L43542/L43547; t8453 L45139/L45144) | t8453 `jiclose` "전일종가" | `exchgubun` | t8453 (L16): jiclose 154500, 201000 / 108500 |

- **JSON types:** the field tables say Number; every quote-route example
  carries JSON integers.
- **Per venue:** each route returns one pair of limit fields. Unlike static
  VI (t1102 has separate `nxt_svi_*` fields), there are no NXT-specific limit
  fields. The t8450 NXT example returns one pair. Whether NXT limits equal
  KRX limits, and what `U` returns, is **not documented**.
- **기준가 vs 전일종가:** t8430/t8436 publish them as two fields (equal in
  every example). t1102 has only `recprice` "기준가(평가가격)"; t8450 labels
  `jnilclose` "전일종가(기준가)". **Inference:** LS treats them as distinct
  values that coincided in the examples; the t8450 label merges them. When
  they differ is not documented.
- **Arithmetic on examples only.** **Inference:** across the 10 quote-route
  example rows (t1102, t1101, t8450, t8407 ×3, t8430 ×2, t8436 ×2):
  - upper / base is 1.2989–1.2996;
  - lower / base is 0.7004–0.7011.

  LS publishes no limit or rounding rule. The chart example does not fit
  this pattern (§4.8 item 7).
- 정적VI prices: t1102 `svi_uplmtprice` "정적VI상한가" / `svi_dnlmtprice`
  "정적VI하한가" (L19170–19175), example 7390 / 6030 against recprice 6710.
  The VI base price is not documented.

### 4.5 Trading sessions and hours

- **Session times (chart summary blocks only):**
  - t8410–t8412 carry `s_time` "장시작시간(HHMMSS)", `e_time`
    "장종료시간(HHMMSS)" and `dshmin` "동시호가처리시간(MM:분)" (t8410
    L43557, L43562).
  - t8451–t8453 add `nxt_fm_s_time` "NXT프리마켓장시작시간(HHMMSS)",
    `nxt_fm_e_time`, `nxt_am_s_time` "NXT에프터마켓장시작시간(HHMMSS)",
    `nxt_am_e_time`, `krx_fm_s_time` "KRX프리마켓장시작시간(HHMMSS)",
    `krx_fm_e_time`, `krx_am_s_time` "KRX에프터마켓장시작시간(HHMMSS)",
    `krx_am_e_time`, plus `*_dshmin` (t8451 L44428–44508).
  - t8453 example (L16, `exchgubun` `"N"`): `s_time` `"090000"`, `e_time`
    `"152000"`, NXT pre `"080000"`–`"085000"`, NXT after
    `"154000"`–`"200000"`, KRX pre `""`–`""`, KRX after
    `"160000"`–`"200000"`, every `*_dshmin` `"00"`.
  - Meaning is **not described**: e.g. whether `e_time` excludes the closing
    call, whether values change per day or venue, time zone.
- **No REST session-phase field:**
  - t1102 `janginfo` "장구분" String 10 (L19005) has example `"KOSDAQ"`
    (L3). It names the listing market, **not** a session phase.
    `nxt_janginfo` "NXT장구분" (L19200) has example `""`.
  - t1101 / t8450 `ho_status` "동시구분" String 1 (L18246, L23493) and t8450
    `nxt_ho_status` "NXT동시구분" (L23663) have **no code list**. Examples:
    t1101 `"1"` with `hotime` `"10061477"`; t8450 `ho_status` `""` and
    `nxt_ho_status` `"1"` with `hotime` `"14162900"`. Meaning not
    determinable from the sources.
- **Request-side session selectors:**
  - t1489 `jgubun` "장구분": "0:장전\n1:장후" (L16855).
  - t1488 `jgubun` "장구분": "1:장전\n2:장후\n3:직전대비" (L22756).
  - t8412/t8452 `krx_mmk_gubun` "KRX정규장구분": "'Y' : 정규장 / 공백을
    포함한 이외의 값 : 전체" (t8452 L44695).
  - t1301/t1308 `starttime` "장시작시간 이후" (trade audit §4.3).
- **Real-time phase:** WebSocket `JIF` "장운영정보" only (§4.2; not
  detailed).
- **API service hours:** not found in L1 or L17.
- **Paper hours (publisher guide, L17):** question ""모의투자 주문처리가 안되었습니다.
  재시도 바랍니다." 메시지가 나옵니다. 왜 그런가요?", answer "모의투자 서버는
  정규장 시간(09:00~15:30)에만 주문이 체결되며, 장 시작 전·점심 정산 시간·서버
  점검 중에는 해당 메시지가 발생할 수 있습니다." The same answer advises "응답
  코드를 확인한 뒤 일정 간격을 두고 재시도하도록 구현하세요" for an order
  message; see §4.9.

### 4.6 Holiday / trading calendar

**Not found.**

- No L1 TR name or field matches `휴장|영업일|개장일|거래일|달력|calendar|holiday`
  for domestic equity. The only hits are:
  - chart request `nday` "조회영업일수(0:미사용1>=사용)" (t8453 L45009);
  - ELW/ETN `lastdate` "최종거래일";
  - account `TrdDt` fields;
  - overseas `bymd` / `chedate` "영업일자".
- t0167 "서버시간조회" (L15) returns `dt` "일자(YYYYMMDD)" and `time`
  "시간(HHMMSSssssss)" (L1 L88591, L88596); example `"20230605"` /
  `"102652926435"`. Its input `id` String 8 has no description. It is a
  server clock, not a calendar or business-day flag.
- t3202 "종목별증시일정" lists per-symbol corporate events (`upgu` "01:유상증자
  …14:스톡옵션행사"), not trading days.
- **Inference:** `nday` implies the server counts business days, but no
  calendar is exposed.

### 4.7 Instrument / market status

**t1102 fields** (L1 L18985–19215, no descriptions, no code lists):

| Field | Name (verbatim) | Type | Example (L3) |
| --- | --- | --- | --- |
| `info1` | "락구분" | String 10 | `""` |
| `info2` | "관리/급등구분" | String 10 | `""` |
| `info3` | "정지/연장구분" | String 10 | `""` |
| `info4` | "투자/불성실구분" | String 12 | `""` |
| `info5` | "투자주의환기" | String 8 | `""` |
| `shterm_text` | "단기과열/VI발동" | String 10 | `""` |
| `svi_uplmtprice` / `svi_dnlmtprice` | "정적VI상한가" / "정적VI하한가" | Number 8 | 7390 / 6030 |
| `low_lqdt_gu` | "저유동성종목여부" | String 1 | `"0"` |
| `abnormal_rise_gu` | "이상급등종목여부" | String 1 | `"0"` |
| `ty_text` | "ETF/ETN투자유의" | String 8 | `""` |
| `nxt_shterm_text` | "NXT단기과열/VI발동" | String 10 | `""` |
| `nxt_svi_uplmtprice` / `nxt_svi_dnlmtprice` | "NXT정적VI상한가" / "NXT정적VI하한가" | Number 8 | 0 / 0 |

**Inference:** the String 8–12 fields are display text, not enumerated
codes. They cannot be mapped to typed states from these sources.

**List routes and filters:**

- t1404 `jongchk` "종목체크": "1:관리\n2:불성실공시\n3:투자유의\n4.투자환기"
  (L20847). Rows carry `date` "지정일", `edate` "해제일", `reason` "사유"
  String 4 (no code list; examples `"5102"`, `"6024"`). Paging uses
  `cts_shcode`.
- t1405 `jongchk`: "1 : 투자경고\n2 : 매매정지\n3 : 정리매매\n4 : 투자주의\n5 :
  투자위험\n6 : 위험예고\n7 : 단기과열지정\n8 : 이상급등종목\n9 : 상장주식수 부족"
  (L21022). Rows carry `date` "지정일" and `edate` "해제일".
- t1410 `jong_gbn`: "'0' : 초저유동성 종목 / '1' : 저PBR 종목" (L21183).
- t1404/t1405/t1410 take `gubun` "0:전체\n1:코스피\n2:코스닥" and have **no**
  `exchgubun`; NXT coverage is not documented.
- t1422/t1427 `jc_num` "대상제외" bit flags (L21340, L21567), e.g. t1427:
  "000000000128(0x00000080):관리종목", "000000000256(0x00000100):시장경보",
  "000000000512(0x00000200):거래정지", "000016777216(0x01000000):정리매매",
  "000067108864(0x04000000):투자유의", "002147483648(0x80000000):불성실공시".
  The description opens with "대상제외값(설정시 저장됨)". **Inference:** the
  server may persist the filter. t1422 also has `lmtdaycnt` "연속" (L21474).
- t8430 / t8436 / t9945 have **no** 거래정지 / 관리 / 투자경고 field.
  - t9945 has only `nxt_chk` "NXT상장구분": "1:NXT 거래소 제공\n0:NXT 거래소
    미제공" (L24142) and `etfchk`.
  - t8436 adds `bu12gubun` "증권그룹" and `spac_gubun`.
- `t3320` "FNG_요약" has `notice1` "위험고지구분1_정리매매", `notice2`
  "위험고지구분2_투자위험", `notice3` "위험고지구분3_단기과열", String 1, no code
  list (L48919–48929).

**VI:**

- Static VI prices: t1102 and the charts (t8410 L43577; t8451 L44448).
- Dynamic-VI price: **not found**.
- VI trigger state: only the text field `shterm_text` on REST. Real-time
  VI is WebSocket only (`VI_`, `DVI`, `NVI`, `UVI`; §4.2).

### 4.8 Contradictions and gaps

1. **"장구분" means different things.**
   - t1102 `janginfo`: market (example `"KOSDAQ"`).
   - t1489: "0:장전\n1:장후".
   - t1488: "1:장전\n2:장후\n3:직전대비".
   - JIF `jangubun`: market list.

   Do not map fields by Korean name.
2. **t1427 `diff` description** repeats the same condition for both
   directions: "signgubun 이 '1'(상한직전)인 경우 diff 이상\nsigngubun 이
   '1'(상한직전)인 경우 -diff 이하" (L21561).
3. **기준가 labels:** t8450 "전일종가(기준가)" vs separate `jnilclose` /
   `recprice` in t8430/t8436 (§4.4).
4. **t9945 example omits `nxt_chk`**, although the field table lists it.
5. **ETF/ETN flags differ:**
   - t8430 `etfgubun` "ETF구분(1:ETF)";
   - t8436 "ETF구분(1:ETF2:ETN)" with "1:ETF\n2:ETN".
   - The FAQ (L17) says "OPEN API는 t8430(주식 종목 조회), xingAPI는
     t8436(주식 종목 마스터)을 사용합니다", yet L1 lists t8436 as a REST TR
     "주식종목조회 API용".
6. **t1404 code text** uses "4.투자환기" (period, not colon). t1102 names
   the related field "투자주의환기".
7. **Chart limits vs quote limits:** in t8453 (L16), `highend`/`jiclose` =
   1.3010 and `lowend`/`jiclose` = 0.7023. Both are outside the
   quote-example range in §4.4. **Inference:** chart limits use another
   base (or a different day); not documented.
8. **t1102 example** requests `exchgubun` `"U"`, but every `nxt_*` field is
   `""`/0 and `ex_shcode` is `"078020"`. Whether that symbol trades on NXT
   is not stated.
9. **t1422 `jc_num` example `"8"`** is not one of the listed flag values.
10. **`exchgubun` requiredness:** `"required" : false` only in t1102
    (L18360). In t1310, t1422 and t8450 it inherits the catalog default
    `"fieldRequired" : true`, and the t1422/t8450 guides (L13, L5) show it
    as required.

### 4.9 Gates and not-verified items

See §10 and §11 (items tagged [LS]). LS-specific: nothing was sent to
LS; the FAQ retry advice (§4.5) is recorded but **not adopted**, and the
t1422 / t1427 `jc_num` "설정시 저장됨" server-side state needs maintainer
review before any use (G-X5).

## 5. DB Securities

### 5.1 Pinned sources

GitHub sources are at
[`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb)
(`564b5100b80a3a785468b77ee8c0557f6edcfdeb`, committer date
2026-08-20T10:06:26+09:00). This is the commit pinned by the trade, candle
and capability-inventory audits; it was re-fetched at 07:48:18Z. Blob SHAs are from
`git ls-tree` of that commit. Portal JSON endpoints on
`https://openapi.dbsec.co.kr` were retrieved 2026-11-05 07:48:56–07:50:43Z.
Portal records carry `lastModifiedDate` (the visible publisher revision);
some also contain staff contact data, which is not copied.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| D1 | [`dbsec_sdk/apis/kr_stock_quote/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_quote/endpoints.py) | blob `5930af396f4a74ff04c7e780fcec87660399bec3`; L28–64 paths/TR codes, L68–97 JCODES, L143–199 MULTIPRICE, L218–258 PRICE, L269–310 HOGA, L380 `InputHourClsCode` | Route list, docstrings (truncated, "(이하 생략 — 가이드 참조)" L197, L257) |
| D2 | [`dbsec_sdk/apis/kr_stock_order/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_order/endpoints.py#L250-L259) | blob `a6e13e46fafb3eedb801f023b6dcd73ecd708105`; L100, L104, L250–259 | `TrchNo`, `OrdprcPtnCode`, NXT 접수시간 (docstring copy of DP1 text) |
| D3 | [`docs/errors_and_rate_limits.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/errors_and_rate_limits.md#L100-L178) | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L100–102, L120, L123, L139–140, L143–147, L149–150, L167–168 | Service message codes tied to tick, limits and sessions |
| D4 | [`docs/api_support_matrix.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/api_support_matrix.md) | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c`; L3–6, L20–25, L49–67, L69–81, L149–157, L268–272 | Complete domestic API inventory, ⭕/❌ paper support, TPS |
| D5 | [`examples/kr_stock_quote/kr_stock_inquire_price.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_price.py#L18-L35) | blob `f717db2b3ce2322d898785f850ca6f7c77afcc03`; L18–20, L32–35 | `Out (오브젝트)`; `Sdpr`/`Mxpr`/`Llam` "(문자)" |
| D6 | [`examples/kr_stock_realtime/kr_stock_realtime_execution_price.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_realtime/kr_stock_realtime_execution_price.py#L38-L60) | blob `7bb1a89ff71116d50e300755d69e1a1874e03832`; L38–41, L56–60 | WebSocket `S00` field names only |
| D7 | [`config.yaml.example`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/config.yaml.example#L13-L14) | blob `f6204f1399f2f080c11f28364444b40b7868ef96`; L13–14 | "REST API URL은 운영/모의 동일 (앱 속성으로 내부 분기)" |
| D8 | [`dbsec_sdk/client_examples/kr-stock-trading-basic.ipynb`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/client_examples/kr-stock-trading-basic.ipynb) | blob `e6ae55d3561ea780da8e3cf0ab635aeb34834566`; L419 (raw JSON line) | Example limit-price rounding with a tick remark (`publisher client code`) |
| DP0 | https://openapi.dbsec.co.kr/apiservice | sha256 `9e18e5d8725cbff5`, 07:48:56Z | Group ids; JSON endpoints incl. `/api/apis/public/search` |
| DP1 | `https://openapi.dbsec.co.kr/api/apis/public/api-list/<group_id>` | 국내주식시세 `80005fb0-…` `f4f56996c26c33b3` (07:49:18Z, identical to the trade audit's DP1); 국내주식주문 `05ac28b8-…` `4f2578523296c2ec` (07:49:24Z); 공통 `b5b58c45-…` `4d5aad054da5b107` (07:49:16Z); 국내주식시세(실시간) `94b5fddc-…` `f48090f104faa614` (07:49:20Z); 국내주식/선물차트 `0bc09824-…` `f10207c4b22890cb` (07:49:22Z, identical to the candle audit's DP1) | Per-API name, path, `svc_id`, description, `lastModifiedDate` |
| DP2 | `https://openapi.dbsec.co.kr/api/apis/guide/tr/<api_id>` | PRICE `d7f6a691-…` `6017533ab47fefef` (07:50:09Z); MULTIPRICE `3abd4f11-…` `b4e64123ae390dfd` (07:50:13Z); HOGA `14be0244-…` `f1bc6c5611010369` (07:50:16Z); JCODES `d8621b8b-…` `4c6329458f9036de` (07:50:20Z); RANKLIST `668de023-…` `1b2b9ba2a98268d4` (07:50:23Z) | `transactionPerSec`, `reqExample`, `resExample` |
| DP3 | `https://openapi.dbsec.co.kr/api/apis/guide/tr/property/<tr_id>` | PRICE `3be5fa4b-…` `a16222751d181c84` (07:50:36Z); MULTIPRICE `b1a8a157-…` `94360bc187c75c90` (07:50:38Z); HOGA `12248529-…` `3dc7e84f6d3cedca` (07:50:40Z); JCODES `de65de78-…` `372c44c2077f9cc1` (07:50:42Z); RANKLIST `ff9b979f-…` `08fe60420ec7a0ab` (07:50:43Z) | Complete request/response field tables |
| DP4 | `https://openapi.dbsec.co.kr/api/apis/public/search?searchText=<term>` | Terms 휴장, 영업일, 장운영, 개장, VI, 상한가, 호가단위, 거래정지, 관리종목, 장구분, 기준가 (07:49:33–07:49:50Z): every body `[]`, sha256 `4f53cda18c2baa0c`. Controls 현재가 `d95fe5e0e17ad565`, 차트 `ee5015285dc62db7` (07:49:56–58Z) returned API lists. | Negative search for market-ops APIs |

Publisher revisions (`lastModifiedDate`, DP1):

| API | `lastModifiedDate` |
| --- | --- |
| PRICE | 2024-06-05 |
| MULTIPRICE | 2026-03-13 |
| HOGA, JCODES, RANKLIST | 2024-03-28 |
| CSPAT00600 | 2026-06-15 |
| CSPAT00610 | 2026-08-21 |

**Missing evidence:**

- No tick-size, holiday, 장운영 or VI route, and no REST status field
  (§5.3, §5.6, §5.7).
- PRICE/MULTIPRICE response fields have no descriptions (DP3 `description`
  null).
- No example with `NJ`/`UJ`, a falling price, or a halted or limit-locked
  symbol.
- **Inference:** DP4 matches API names only. Controls hit names, and
  "기준가" — a PRICE field name — returned nothing. A field-level negative
  therefore rests on DP3/D1–D4, not on DP4.

### 5.2 Routes

Common transport is as in the trade audit §5.2:

- `POST` to `https://openapi.dbsec.co.kr:8443`. One origin serves
  production and demo (D7).
- Headers: `content-type`, `authorization`, `cont_yn`, `cont_key`,
  `mac_address`.
- Body `{"In": {...}}`; envelope `rsp_cd`/`rsp_msg`.

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Purpose | Evidence |
| --- | --- | --- | --- | --- | --- |
| "현재가조회" | `POST /api/v1/quote/kr-stock/inquiry/price` | `PRICE`; api `d7f6a691-…`; TPS 5 | ⭕ (D4 L56) | 기준가 / 상한가 / 하한가 | field table (DP3), publisher example (DP2), publisher client code (D1, D5) |
| "국내주식 멀티현재가조회" | `POST /api/v1/quote/kr-stock/inquiry/multiprice` | `MULTIPRICE`; api `3abd4f11-…`; TPS 2 | ⭕ (D4 L55) | Same per row, "1~50" symbols | field table, publisher example |
| "호가조회" | `POST /api/v1/quote/kr-stock/inquiry/orderbook` | `HOGA`; api `14be0244-…`; TPS 3 | ⭕ (D4 L57) | Checked: no limit, tick or status field | field table (DP3) |
| "주식종목 조회" | `POST /api/v1/quote/kr-stock/inquiry/stock-ticker` | `JCODES`; api `d8621b8b-…`; TPS 3 | ⭕ (D4 L53) | Checked: market only, no status | field table (DP3) |
| "일별체결조회" | `POST /api/v1/quote/kr-stock/inquiry/daily-price` | `DAYTRADE`; TPS 3 | ⭕ (D4 L59) | Session filter `InputHourClsCode` (§5.5) | field table, publisher client code (D1 L380; trade audit §5.3) |
| "주식종합주문- NXT거래소" | `POST /api/v1/trading/kr-stock/order-nxt` | `CSPAT00610`; api `13143c06-…`; TPS 10 | ❌ (D4 L34) | **Description only:** NXT 접수시간 (§5.5). Order route; nothing was called. | publisher guide (DP1), publisher client code (D2) |

WebSocket, name and id only: `S00` "[실시간]주식체결가" (D4 L76). Its example
field list names `StckSdpr` "기준가", `StckMxpr` "상한가", `StckLlam` "하한가",
`TrhtYn` "거래정지 여부", `MangIssuyn` "관리종목 여부", `WarnYn` "투자주의 여부"
and `NewMkopclscode` "신장운영구분코드" (D6 L38–41, L56–60). Not detailed.

D4 is the SDK's full API list. Its 공통 group (L20–25) has only interest-group
APIs (`MCJDD88841`, `MCJDD88840`), confirmed by DP1.

### 5.3 Tick size (호가단위)

**Not found.**

- No route and no field in the PRICE, MULTIPRICE, HOGA, JCODES or RANKLIST
  field tables (DP3).
- No tick table in SDK or example code. A repository-wide `git grep` for
  `호가단위|틱단위|tick_size` (including notebooks) hits only D3 L123 and
  D8 L419.
- D8 (`publisher client code`, an order-practice notebook) rounds an example
  limit price with `int(last_price * 0.95) // 100 * 100` and the comment "100원
  단위 절사 (호가단위는 가격대별 상이)". The publisher thus states that the tick
  varies by price band, but gives no table. The 100 KRW truncation is a
  notebook shortcut, not a tick rule.
- Order-side evidence is reactive: service code `2706` "주문가격의 호가단위를
  확인하십시오." (D3 L123).
- KRX vs NXT difference: not documented.

### 5.4 Price limits (상한가 / 하한가 / 기준가)

| Route | Fields (DP3, verbatim) | Type | Venue | Example (DP2) |
| --- | --- | --- | --- | --- |
| PRICE | `Sdpr` "기준가", `Mxpr` "상한가", `Llam` "하한가" (`Out` A0003 object) | `A0001`, length 16; JSON strings (D5 "(문자)") | `InputCondMrktDivCode` "주식:J<br/>주식(NXT): NJ<br/>주식(통합): UJ<br/>ETN: EN<br/>ELW: W<br/>업종&지수: U…" with `N-`/`U-` symbol prefix | `J` `005930`: `"53900"`, `"70000"` / `"37800"`; `Prpr` `"55550"`, `PrdyVrss` `"1650"` |
| MULTIPRICE | Same three per row (`Out` A0002 array) | same | per-row `InputCondMrktDivCode<n>` | `000660` `"184900"` → `"240000"` / `"129500"`; `005930` `"61000"` → `"79300"` / `"42700"`; index `1001` `Mxpr` `""`, `Llam` `""` |

- **기준가 vs 전일종가:** there is no 전일종가 field on PRICE or MULTIPRICE,
  so the distinction is **not documented**.
  - **Inference:** in the PRICE example `PrdyVrss` (`"1650"`) equals `Prpr`
    − `Sdpr`, so there 전일대비 is measured from 기준가.
- **Per venue:** one `Mxpr`/`Llam` pair per response. No `NJ`/`UJ` example
  exists. Whether `UJ` limits are KRX limits is **not documented**.
- **Not applicable → empty string:** the index row returns `""` for `Mxpr`
  and `Llam`, not `"0"` or an absent key.
- **Arithmetic on examples only.** **Inference:** the three stock rows give
  upper / base 1.2980–1.3000 and lower / base 0.7000–0.7013. DB publishes no
  rule.
- **Order-side codes (D3):**
  - `3180` "주문가격이 상한가 초과입니다." (L139);
  - `3181` "주문가격이 하한가 미달입니다." (L140);
  - paper `M100` "모의투자 상하한가 오류" (L167).

### 5.5 Trading sessions and hours

- **NXT order-acceptance hours (publisher guide, DP1 CSPAT00610
  description, `lastModifiedDate` 2026-08-21; same text in D2 L256–259):**
  "※ NXT 거래소 접수시간 <br> 프리마켓 : 08:00 ~ 08:50, [주문가능구분] :
  지정가,최유리,최우선 <br> 메인마켓 : 09:00:30 ~ 15:20, [주문가능구분] :
  모든주문구분 가능 <br> 애프터마켓 : 15:30 ~ 20:00, [주문가능구분] :
  지정가,최유리,최우선 (15:30~40: 지정가만 가능) <br> 종가매매 : 15:00 ~ 16:00,
  [주문가능구분] : 시간외종가 <br>". These are acceptance windows for DB's NXT
  order route, not quote-session data. Time zone not stated.
- **KRX session hours:** **not found** in D1–D7 or DP1–DP3. The CSPAT00600
  description only links "주식매매 거래제도 안내"
  (`https://www.dbsec.co.kr/custcenter/jobservice/cu_TradeStock_viw.do`),
  a customer-centre page outside the API docs. It was **not retrieved**.
- **Session-linked order types:** `OrdprcPtnCode` "00:지정가 03:시장가
  05:조건부지정가 06:최유리지정가 07:최우선지정가 14: 중간가호가 61:장개시전시간외
  81:시간외종가 82:시간외단일가" (D2 L104).
  - `TrchNo`: "주문시 거래소 구분용도로 사용 1 : KRX ※ 1로 고정하셔서 사용
    부탁드립니다. (SOR 주문 구분은 추후 제공 예정)" (D2 L100).
- **Session filter on a quote route:** DAYTRADE `InputHourClsCode` "1:
  시간외단일가체결 / 2: 장전+장중+장후 / … / 10: 시간외단일가 예상" (D1 L380;
  full list in the trade audit §5.3). It filters rows only; no phase is
  returned.
- **Session-phase field:** none on PRICE, MULTIPRICE, HOGA or JCODES (DP3).
  WebSocket `S00` names `NewMkopclscode` "신장운영구분코드" (D6 L60); its code
  list is not in D6.
- **Session-related service codes (D3):**
  - `2611` "장시작 전 또는 장마감 되었습니다." (L120);
  - `3446` "접속매매에서만 가능한 호가구분입니다." (L143);
  - `3563` "정규매매장이 종료되었습니다. 시간외 호가구분을 입력하십시요." (L144);
  - `3589` "장개시 전이므로 주문 불가합니다." (L146);
  - `3590` "장마감 후이므로 주문 불가합니다." (L147);
  - `3665` "해당 서비스 일시정지중입니다." (L149);
  - paper `M100` "모의투자 장시작전 입니다." (L168).
- **API service hours / paper hours:** not found.

### 5.6 Holiday / trading calendar

**Not found.**

- D4 (the SDK's full API inventory) lists no holiday, business-day or
  calendar API.
- `git grep -i '휴장|공휴|holiday|영업일|거래일|개장일|calendar'` over the
  commit hits only:
  - overseas and futures modules (`영업일자`, a futures 거래제도 note);
  - account `TrdDt` "거래일자" (D2 L941).
- DP4 name search for 휴장, 영업일, 개장 returned `[]`.

### 5.7 Instrument / market status

- **REST: none.** The DP3 tables for PRICE, MULTIPRICE, HOGA, JCODES and
  RANKLIST contain no 거래정지, 관리, 투자경고/주의, 정리매매, 단기과열 or VI
  field.
  - JCODES gives only `MrktClsName` "시장구분명" ("구분자 목록: "ETF",
    "ETN","코넥스","코스닥","거래소(코스피)"") and `MrktClsCode` "1: 코스닥<br/>4:
    코스피".
- **WebSocket only (names, D6 L56–59):** `TrhtYn` "거래정지 여부",
  `MangIssuyn` "관리종목 여부", `WarnYn` "투자주의 여부". Not detailed.
- **VI:** not found in any REST or WebSocket field name in D1, D6 or DP3.
  DP4 "VI" returned `[]`.
- **Order-side code:** `3735` "해당종목 NXT거래  불가합니다." (D3 L150). The
  same code also carries "자전거래 의심주문으로 해당 종목은 주문이 불가합니다."

### 5.8 Contradictions and gaps

1. **SDK docstrings are truncated:** "(이하 생략 — 가이드 참조)" (D1 L197,
   L257). D1 is not a complete field list; DP3 is.
2. **Empty-string limits:** the MULTIPRICE index row returns `Mxpr`/`Llam`
   `""`. A decoder must not coerce `""` to 0.
3. **NXT hours text** lists 종가매매 "15:00 ~ 16:00" inside the other
   windows: it overlaps 메인마켓 (to 15:20) and the 애프터마켓 start (15:30).
   Window boundaries (inclusive/exclusive) and time zone are not stated.
4. **`M100`** is one code for many paper messages, e.g. "모의투자
   상하한가 오류" and "모의투자 장시작전 입니다." (D3 L162–173). Only the
   message text distinguishes them. `3735` likewise has two meanings.
5. **No sign field on PRICE:** DP3 has `PrdyVrss` but no `PrdyVrssSign`
   (RANKLIST has one). The PRICE example rises (`"1650"`), so the
   falling-price convention is not shown on this route.
6. **Tick and limit enforcement is reactive only:** codes
   `2706`/`3180`/`3181` exist, but no tick source does (§5.3).
7. **Status is WebSocket-only:** status flags appear only in `S00` field
   names. The REST snapshot routes expose none.

### 5.9 Gates and not-verified items

See §10 and §11 (items tagged [DB]). DB-specific: nothing was sent to
DB, and the NXT order route was read as documentation only. `""` limits
on index rows must never be read as 0 (G-L5).

## 6. Toss Securities

### 6.1 Pinned sources

Public Toss portal documents, retrieved 2026-11-05 07:43:41–07:43:46 UTC.
No broker API request was sent. All five files are byte-identical (same
sha256) to the copies pinned in the trade audit (§6.1 there, 07:10 UTC),
so the spec did not change between the two retrievals.

Evidence ranking is the same as in the trade audit:

- T1 is the `field table`.
- T2 and T4 are `publisher guide`. T4 L3 says the API reference wins: "각
  API 의 정확한 요청·응답 형식은 API 문서의 해당 엔드포인트 항목이
  기준입니다."
- T5 L16 calls T1 the source of truth.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | sha256 `c5918961335ccd6b…`, 07:43:41Z; `openapi 3.1.0`, `info.version 1.2.28`; `servers[0].url` `https://openapi.tossinvest.com` | `paths./api/v1/price-limits.get` (`getPriceLimit`), `/api/v1/market-calendar/KR` (`getKrMarketCalendar`), `/api/v1/market-calendar/US` (`getUsMarketCalendar`), `/api/v1/stocks` (`getStocks`), `/api/v1/stocks/all` (`listStocks`), `/api/v1/stocks/{symbol}/warnings` (`getStockWarnings`), `/api/v1/prices`, `/api/v1/rankings`; `POST /api/v1/orders` and `/api/v1/conditional-orders` error examples; `components.schemas.{PriceLimitResponse, KrMarketCalendarResponse, KrMarketDay, IntegratedHour, PreMarketSession, RegularMarketSession, AfterMarketSession, UsMarketDay, StockInfo, KrMarketDetail, StockWarning, PriceResponse, RankingPrice, ApiError, OrderCreateRequest, ConditionRequest}`; `tags[Market Data, Stock Info, Market Info]` |
| T2 | [overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md) | sha256 `bef057d9babe9a38…`, 07:43:44Z | L26, L28, L31 feature list; L96, L104, L111–117 endpoint list; L236–238, L246–250 rate limits; L305 error-code example; L343–345, L349, L363 error table |
| T3 | [asyncapi.json](https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json) | sha256 `46669a360d4c5c64…`, 07:43:43Z; `asyncapi 3.0.0`, `info.version 1.2.3` | Channel names only: `connection`, `realtime-trade`, `realtime-orderbook`, `realtime-order`, `realtime-conditional-order` |
| T4 | [faq.md](https://openapi.tossinvest.com/openapi-docs/faq.md) | sha256 `6ad4c02b8e785f7d…`, 07:43:46Z | L24–27 (auction / session coverage of candles), L40, L42 (no per-symbol 기준가), L50 (order hours), L64, L75 (SOR only), L77–84 (장 운영 시간 · 휴장) |
| T5 | [developers.tossinvest.com/llms.txt](https://developers.tossinvest.com/llms.txt) | sha256 `bbff77eaa55df248…`, 07:43:46Z | L5, L32 (market calendars listed) |

**Missing evidence:**

- No paper or sandbox origin in T1 (`servers` has one entry).
- No publisher client code or SDK was retrieved for these routes.
- No document states the service hours of the API itself (see §6.5).

### 6.2 Routes

Every route is a `GET` with a query string on `https://openapi.tossinvest.com`,
and every route needs an `Authorization` Bearer token (scheme
`oauth2ClientCredentials`). None of them takes an account header.

- T1 tag `Market Data`: "계좌 정보 없이 액세스 토큰만으로 호출할 수
  있습니다."
- T1 tag `Market Info`: "계좌와 무관한 정보로 토큰만으로 호출 가능합니다."

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Purpose | Evidence |
| --- | --- | --- | --- | --- | --- |
| "상/하한가 조회" — "종목의 당일 상한가 및 하한가를 조회합니다." | `GET /api/v1/price-limits?symbol=` | `getPriceLimit`; group `MARKET_DATA` | real only | Daily upper/lower limit | field table |
| "국내 장 운영 정보 조회" | `GET /api/v1/market-calendar/KR[?date=]` | `getKrMarketCalendar`; group `MARKET_INFO` | real only | Previous/today/next business day with KRX+NXT integrated session times; holiday = `null` | field table + publisher guide (T4 L81) |
| "해외 장 운영 정보 조회" | `GET /api/v1/market-calendar/US[?date=]` | `getUsMarketCalendar`; group `MARKET_INFO` | real only | US day/pre/regular/after sessions, in KST | field table |
| "종목 기본 정보 조회" | `GET /api/v1/stocks?symbols=` (≤200) | `getStocks`; group `STOCK` | real only | `status`, `koreanMarketDetail` (정리매매, NXT support, KRX/NXT 거래정지) | field table + publisher guide (T4 L84) |
| "마켓별 전체 종목 조회" | `GET /api/v1/stocks/all?market=` | `listStocks`; group `STOCK_ALL` | real only | Universe filter by `status` (`SCHEDULED`/`ACTIVE`/`DELISTED`); no halt or warning fields | field table |
| "매수 유의사항 조회" — "종목의 매수 유의사항 및 변동성 완화(VI) 발동 정보를 조회합니다." | `GET /api/v1/stocks/{symbol}/warnings` | `getStockWarnings`; group `STOCK` | real only | 정리매매, 단기과열, 투자경고, 투자위험, VI, 신주인수권 | field table |
| "현재가 조회" | `GET /api/v1/prices?symbols=` | `getPrices`; group `MARKET_DATA` | real only | Checked for limit, 기준가 and tick fields: **none** (only `symbol`, `timestamp`, `lastPrice`, `currency`) | field table |
| "주식 랭킹 조회" | `GET /api/v1/rankings` | `getRankings`; group `RANKING` | real only | Only route with `basePrice` (기준가); see §6.4 | field table + publisher guide (T4 L42) |

Order routes are cited only for their tick and hours error contracts
(§6.3, §6.5); no order call was made. AsyncAPI (T3) has no market-status,
VI or session channel; the five channel names are listed in §6.1.

### 6.3 Tick size (호가단위)

- **No dedicated route and no tick field** in `PriceResponse`,
  `OrderbookEntry`, `StockInfo` or `ListedStock` (T1). `OrderbookEntry` has
  only `price` "호가" and `volume` "잔량".
- **Reactive only, via order errors.** `ApiError.data` (T1) lists the
  standard keys `tickSize` (string) "호가 단위." and `nearestPrices`
  (string[]) "근접 유효 가격 (`[lower, upper]`)."
  - `POST /api/v1/orders` and `/orders/{orderId}/modify`, 400 example
    `invalidTickSize`: `code` `"invalid-request"`, message "주문 가격이 호가
    단위에 맞지 않습니다.", `data` `{"field":"price","tickSize":"100",
    "nearestPrices":["50100","50200"]}`.
  - `POST /api/v1/conditional-orders` and `…/modify` give the same message,
    with `field` `"first.orderPrice"` and `tickSize` `"50"`.
- **Rule text inside a field description, given as an example, not a
  table.** `OrderCreateRequest.price` (T1):
  - "KR: 정수 (원 단위). 호가 단위에 맞아야 합니다 (예: 50,000~200,000원
    구간은 100원 단위). 맞지 않으면 `400 invalid-request` 에러와 함께
    올바른 호가 단위가 `data`에 포함됩니다."
  - US: "$1 미만: 소수점 넷째 자리까지 (그 이하 자릿수는 절삭). $1 이상:
    소수점 둘째 자리까지 (그 이하 자릿수는 절삭)."
  - `ConditionRequest.orderPrice` repeats the KR example.
- **Venue:** no KRX/NXT tick distinction is documented. Orders are SOR only:
  T4 L75 "Open API 주문은 통합(SOR) 모드만 지원해 거래소를 지정한 주문 자체가
  불가능하며". 422 `investor-exchange-not-integrated` also applies (T1;
  T2 L349).
- **Publisher-code tick table:** not found.
- **Inference:** a read-only client cannot get the tick size before
  ordering. It only learns the value from a rejected order's
  `data.tickSize`.

### 6.4 Price limits (상한가 / 하한가 / 기준가)

`GET /api/v1/price-limits` → `result: PriceLimitResponse` (T1):

| Field | Type | Required | Description (verbatim) |
| --- | --- | --- | --- |
| `timestamp` | string `date-time` | Y | "데이터 시각" (example `"2026-03-25T09:30:00.123+09:00"`) |
| `upperLimitPrice` | `string` or `null`, `format: decimal`, `maxLength 30` | N | "상한가. 미국 주식 등 가격제한이 없는 시장에서는 null" |
| `lowerLimitPrice` | `string` or `null`, `decimal`, `maxLength 30` | N | "하한가. 미국 주식 등 가격제한이 없는 시장에서는 null" |
| `currency` | `Currency` enum (`KRW`, `USD`) | Y | — |

- **Examples:** KR `"93000"`/`"50400"` `KRW`; US `null`/`null` `USD` (summary
  "해외 주식 (Apple, 가격제한 없음)").
- **Errors:** 404 `NotFound`, 429, 500 `InternalErrorMarketData`. No 400 is
  listed.
- **Request:** `symbol` only (`SymbolQuery`). There is no venue or date
  parameter.
- **Venue:** not stated for limits. The FAQ says domestic quotes are
  KRX+NXT integrated (T4 L22, L40), but it does not mention limits.
  **Inference:** one limit pair per symbol.
- **Which trading day:** "당일" only. What the route returns before the open,
  after the close or on a holiday is not documented.
- **기준가:**
  - **Not returned** by `price-limits`, `prices` or `orderbook`.
  - T4 L42: "종목별 전일 기준가나 등락률을 조회할 수 있나요? | 종목별로
    조회하는 API 는 제공하지 않습니다. 기준가(`basePrice`)와 등락률은 랭킹
    조회(`GET /api/v1/rankings`) 응답 항목에만 포함됩니다. 국내 일봉의 전일
    `closePrice` 는 KRX·NXT 통합 마지막 체결가라 등락률 계산 기준가와 다를
    수 있습니다."
  - So Toss documents that 기준가 ≠ previous daily `closePrice`.
- **`RankingPrice.basePrice`** (T1): "기준가. `TOP_GAINERS` / `TOP_LOSERS`
  는 `duration` 시작 시점 기준가, 나머지 타입은 `duration` 과 무관하게 항상
  전일 기준가." It is per ranking row, not per arbitrary symbol.
- **Order-side link:**
  - 422 `price-out-of-range` "주문 가격이 허용 범위를 벗어났습니다." (T1).
  - T2 L345 glosses it as "주문 가격이 허용 범위(상/하한가)를 벗어났습니다."
- **Rate:** `MARKET_DATA` 15/s, shared with quotes, orderbook and trades
  (T2 L250; T1 tag text).

### 6.5 Trading sessions and hours

**KR calendar session model** (`GET /api/v1/market-calendar/KR`, T1). The
route description reads: "국내 시장의 거래 가능 시간을 조회합니다. 통합 모드
(KRX+NXT) 기준이며, 장전/장후 시간외종가는 제외됩니다. 전일/당일/익일
3영업일 정보를 반환합니다. 모든 시간은 KST(+09:00) 기준."

| Object.field | Type | Description (verbatim) |
| --- | --- | --- |
| `IntegratedHour` | object | "거래 가능 시간. 장전/장후 시간외종가 제외, 통합 모드 (KRX+NXT) 기준. 세 세션(`preMarket`, `regularMarket`, `afterMarket`) 각각 nullable. 해당 세션이 KRX·NXT 모두 휴장이면 null, 세 세션 모두 null 이면 상위 `integrated` 자체가 null." |
| `.preMarket` | `PreMarketSession` or `null` | "프리마켓 (NXT 접속매매). NXT 프리마켓이 휴장이면 null" |
| `PreMarketSession.singlePriceAuctionStartTime` | date-time or `null` | "프리마켓 내 시가단일가 구간 시작 (NXT 프리마켓 접속매매 종료). 단일가 정보 결손 시 null" |
| `PreMarketSession.endTime` | date-time | "프리마켓 종료 (시가단일가 종료)" |
| `.regularMarket` | `RegularMarketSession` or `null` | "정규장. KRX·NXT 정규장의 합집합. 둘 다 휴장이면 null"; schema: "(가장 이른 시작 ~ 가장 늦은 종료). 종가단일가 구간을 포함" |
| `RegularMarketSession.singlePriceAuctionStartTime` | date-time or `null` | "정규장 내 종가단일가 구간 시작 (KRX 기준). KRX 휴장이면 null" |
| `.afterMarket` | `AfterMarketSession` or `null` | "애프터마켓. KRX·NXT 애프터마켓의 합집합. 둘 다 휴장이면 null" |
| `AfterMarketSession.singlePriceAuctionEndTime` | date-time or `null` | "애프터마켓 내 시가단일가 구간 종료 (NXT 기준). NXT 애프터마켓이 휴장이면 null" |
| `AfterMarketSession.endTime` | date-time | "애프터마켓 전체 종료. 가장 늦은 KRX/NXT 애프터마켓 종료 시각" |

- **Example values** (`businessDay`, publisher example):
  - pre-market 08:00 / auction 08:50 / end 09:00;
  - regular 09:00 / closing auction 15:20 / end 15:30;
  - after-market 15:30 / auction end 15:40 / end 20:00.
  - All values carry a `+09:00` offset.
- **Per-venue times are not available.** T4 L82: "KRX 와 NXT 의 개장·폐장
  시간을 각각 확인할 수 있나요? | 거래소별로 구분된 시간은 제공하지 않습니다.
  통합 모드 기준 시간만 제공합니다." T4 L83 confirms the union rule for the
  after-market and regular sessions.
- **No market-phase / 장운영구분 code field** on any REST route. There is no
  "current phase" output; only the timetable.
- **Excluded sessions:** 장전/장후 시간외종가 (T1). T4 L64 says Open API does
  not support those order types ("장전/장후 시간외종가 등 Open API 가 지원하지
  않는 호가 유형").
- **Order-hours behaviour:**
  - T4 L50: "Open API 가 별도로 제한하지 않고 매매 시스템의 주문 가능 시간을
    그대로 따릅니다. 애프터마켓도 동일하게 적용되며, 주문 불가 시간에는
    `422 order-hours-closed` 로 응답합니다."
  - Example `data` `{"retryAfterAt":"2026-01-02T09:00:00+09:00"}` on order
    create; T1.
  - `timeInForce` `OPG`: "세션 시간(장전 사전접수) 외 접수는 원장에서 거절될
    수 있습니다."
  - Conditional orders (T1): "국내 주식: KRX 정규장에서만 발동됩니다."
- **US calendar:** four sessions (`dayMarket` "데이마켓 세션 (토스증권)",
  `preMarket`, `regularMarket`, `afterMarket`), all in KST. `date` is
  "조회 기준일 (YYYY-MM-DD, 미국 현지 날짜)". Example: day 09:00–16:50,
  pre 17:00–22:30, regular 22:30–05:00, after 05:00–07:00 KST.
- **API service hours / maintenance:** not documented. The only related
  item is error `maintenance` "시스템 점검 중입니다." (T2 L363), with an
  order example of `retryAfterSeconds: 600` (T1).
- **Rate:** `MARKET_INFO` 3/s (T2 L249).

### 6.6 Holiday / trading calendar

- **Route:** `GET /api/v1/market-calendar/KR` (and `/US`).
- **Request:** optional `date` (query, `format: date`, "조회 기준일
  (YYYY-MM-DD)"). There is no range parameter.
- **Response:** exactly three days, `today`, `previousBusinessDay` and
  `nextBusinessDay` (all required, `KrMarketDay`). There are no
  multi-day lists and no year calendar.
- **`KrMarketDay` fields:**
  - `date` (string `date`, required): "영업일 (KST 기준)".
  - `integrated` (`IntegratedHour` or `null`): "거래 가능 시간 (통합 모드
    (KRX+NXT) 기준). 둘 다 휴장이면 null".
- **Holiday flag:** there is **no boolean** 영업일/휴장 flag. A holiday is
  signalled by `null`. T4 L81: "국내 장 운영 정보 조회에서 해당 일자의 통합
  장 정보(`integrated`) 가 `null` 이면 휴장일입니다. 세션 단위로도
  `preMarket`·`regularMarket`·`afterMarket` 각각 휴장이면 `null` 입니다."
- **Examples:**
  - `holidayToday`: `today.date` `"2026-05-05"`, `integrated: null`; previous
    business day `2026-05-04`, next `2026-05-06`.
  - `nxtPreMarketHoliday`: `preMarket: null`, other sessions present
    ("부분 휴장").
- **Range limits:** not documented. KR lists 400 `unsupported-date` "요청한
  조회 일자를 지원하지 않습니다." with `data {"field":"date"}`, but which
  dates are supported is not stated. The US route lists **no 400**.
- **Update cadence, and how far ahead holidays are known:** not documented.
- **Paper:** none.

### 6.7 Instrument / market status

| Status | Route + field | Values / description (verbatim) | Timeliness |
| --- | --- | --- | --- |
| Listing status | `GET /api/v1/stocks` `status` (required) | enum `SCHEDULED`, `ACTIVE`, `DELISTED`; "상장 상태" | Tag `Stock Info`: "영업일 단위(또는 그 이상)로 갱신" |
| 거래정지 (KRX) | `koreanMarketDetail.krxTradingSuspended` (boolean, required in `KrMarketDetail`) | "KRX 거래정지 여부" | T4 L84: "현재 거래정지 여부 … 과거 거래정지 이력은 제공하지 않습니다." |
| 거래정지 (NXT) | `koreanMarketDetail.nxtTradingSuspended` (`boolean` or `null`) | "NXT 거래정지 여부. NXT 미지원 종목(nxtSupported=false)은 null" | same |
| NXT eligibility | `koreanMarketDetail.nxtSupported` (boolean) | "NXT 대체거래소 지원 여부" | — |
| 정리매매 | `koreanMarketDetail.liquidationTrading` (boolean) **and** warnings `LIQUIDATION_TRADING` | "정리매매 여부 (상장폐지 절차 진행 중)." | see §6.8 item 4 |
| VI | `GET /api/v1/stocks/{symbol}/warnings` `warningType` ∈ `VI_STATIC_AND_DYNAMIC`, `VI_STATIC`, `VI_DYNAMIC` | "변동성 완화장치(VI) 정적 + 동적 동시 발동" / "… 정적 발동" / "… 동적 발동" | "VI 발동/해제는 거래소 이벤트 발생 후 수 초 내 반영됩니다." |
| 단기과열 / 투자경고 / 투자위험 | warnings `OVERHEATED`, `INVESTMENT_WARNING`, `INVESTMENT_RISK` | "단기과열종목 지정" / "투자경고종목 지정" / "투자위험종목 지정" | "거래소 공시 기준 일배치로 반영됩니다." |
| 신주인수권 | warnings `STOCK_WARRANTS` | "신주인수권증서/증권" | — |
| 관리종목 | — | **not found** | — |
| 투자주의 | — | **not found** (no `INVESTMENT_CAUTION`-style value) | — |
| Order-time restriction | `POST /api/v1/orders` 422 `stock-restricted` | "해당 종목은 현재 주문이 제한되어 있습니다." (T2 L344: "해당 종목이 거래 제한 상태입니다.") | — |

`StockWarning` fields (T1):

- `warningType` (required). "클라이언트는 unknown code 를 허용하도록
  구현해야 합니다."
- `exchange` (`string` or `null`): "거래소 코드 (KRX, NXT 등 물리적 거래소
  단위) … 거래소 무관 경고는 null".
- `startDate` / `endDate` (`date` or `null`, inclusive, KST).
  - `endDate` `null` = "진행 중이거나 미정".
  - Active means "`startDate <= 오늘 <= endDate` … (또는 `endDate` 가 `null`
    인 진행 중 항목)".
  - Sorted by `startDate` descending; ties have no guaranteed order.
- Unknown symbol → `404 stock-not-found`; no active warnings → `200` with
  `result: []`.

VI is reported at **date** granularity only. There is no trigger time, no
trigger or reference price and no release time. Example:
`{"warningType":"VI_STATIC","exchange":"KRX","startDate":"2026-03-26",
"endDate":null}`.

### 6.8 Contradictions and gaps

1. **Tick error code name.** T2 L305 gives `invalid-tick-size` as an example
   error code. T1's order and conditional-order examples use
   `invalid-request` plus `data.tickSize`. No `invalid-tick-size` appears
   in T1. **Inference:** match on `data.tickSize`, not on the code string.
2. **`KrMarketDay.date` "영업일".** The field is described as "영업일 (KST
   기준)", but in the `holidayToday` example `today.date` is a holiday
   (`2026-05-05`, `integrated: null`). The US example does the same
   (`2026-07-03`). `today.date` is therefore not always a business day.
3. **Warnings timeliness vs tag text.** Tag `Stock Info` says the
   reference data and 매수 유의사항 are updated "영업일 단위(또는 그 이상)"
   and advises against short polling. The warnings route says VI changes
   are reflected "수 초 내". The tag advice does not fit VI.
4. **Two 정리매매 sources.** `KrMarketDetail.liquidationTrading` and warnings
   `LIQUIDATION_TRADING` are both documented. Their update cadence and
   whether they always agree are not stated.
5. **No per-venue limits, ticks or hours.** The limits, calendar and
   orderbook are integrated or SOR. The KRX/NXT split exists only for
   거래정지 and for warning `exchange`.
6. **Price-limit day boundary.** "당일" is undefined for pre-open, the
   after-market (to 20:00) and holidays.
7. **Calendar `date` range.** 400 `unsupported-date` exists (KR) but the
   supported window is undocumented. The US route has no 400.
8. **No status code for the current phase.** Clients must compare the
   clock with the timetable. The VI/halt state is not tied to a session.

### 6.9 Gates and not-verified items

See §10 and §11 (items tagged [Toss]). Toss-specific: every field above
is `field table` or `publisher guide`; the tick size is only observable
through a rejected order, so no tick probe may be designed (G-T4).
Unknown `warningType` and `Currency` values must be tolerated (T1).

## 7. Meritz Securities

### 7.1 Pinned sources

Sources:

- Portal `https://openapi.imeritz.com`, retrieved 2026-11-05 07:45:15–07:45:18
  UTC.
- GitHub repository
  [`meritz-securities/open-api@a93c6409db73ea97ad15f7b7186f36c9f32ecd89`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89)
  (commit 2026-10-28T22:32:03+09:00). It was still the default-branch head
  when cloned at 07:45:19Z.

Repo README L11 says the portal is canonical: "API 목록과 파라미터·응답 필드의
정본은 [개발자 포털](https://openapi.imeritz.com)입니다." Repo content is
therefore `publisher repo note` or `publisher client code` and ranks below
M1. No broker API request was sent. The portal sample's `mac_address`
handling is deliberately not reproduced or described here.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| M1 | Portal spec export [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json), `title` "메리츠증권 Open API 명세" | 07:45:15Z, raw sha256 `afc8983dbc6507ee…`, 1,136,519 bytes, `generatedAt "2026-11-05 16:43:51"`. With `generatedAt` removed and `json.dumps(sort_keys=True, ensure_ascii=False)`: `2fff4f3e02d20cd5…`, **identical** to the trade-audit copy (07:10Z). | `groups[2]` "국내주식": `apis[19]` 현재가 조회, `[20]` 시간외 단일가 조회, `[21]` 호가 조회, `[22]` 시간외 단일가 호가 조회, `[25]` 국내 영업일 조회, `[26]` 국내 장운영 조회, `[15]` 시세추이 조회(일봉) (기준가 wording), `[8]` 예약주문 매수 (`warn_cls_code` list), `[0]` 일반주문 매수 (`warn_cls_code` set); `groups[3]` `[20]`–`[22]`, `[30]` (overseas, out of scope); `groups[4]` (WebSocket, names only) |
| M2 | [samplecode-py](https://openapi.imeritz.com/samplecode-py) | 07:45:18Z, raw sha256 `9a67829eac3f9969…` (varies per request). Visible text (script and style elements stripped): sha256 `9ee90e874d493a7c…`, identical to the 07:12Z copy. | Text L157 (`J`/`NJ`/`TJ`), L162 (`mxpr`/`llam` printed), L217 (tick = `aspr_unit`), L276–278 (after-close orderbook) |
| M3 | [howto-use](https://openapi.imeritz.com/howto-use) | 07:45:17Z, raw sha256 `2de1fe898939991b…` (varies). Visible text sha256 `1d088d95b66c210a…`, identical to the 07:12Z copy. | Searched for service hours, 장운영, 휴장: **not found** (only a `J` sample at text L201) |
| M5 | repo [`openapi.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/openapi.json) | blob `93e900e66b965607d7fd8b8e14c6088d710e6fce` | `/market/v1/prices` L6607–7157 (`issu_stat_cls_code` L6684, `tmpr_susp_yn` L6714, `mxpr` L6804, `llam` L6809, `sdpr` L6814, `aspr_unit` L6893, `sltr_yn` L7032, `x-tps "10"` L7157); `/prices/after` L7160–7550 (`ovtm_untp_mxpr` L7319); `/orderbook` L7553–8223 (`shrn_mkop_cls_code` L8021, `nw_mkop_cls_code` L8096, `mxpr` L8102); `/orderbook/after` L8226–8447; `/reference/v1/market-days` L8843–8960; `/reference/v1/market-hours` L8963–9247 (`mkpl_cls_code` L8985, `mkop_cls_code` L9039, `pgm_aspr_fin_time` L9087, `oder_stop_yn` L9159) |
| M6 | repo [`meritz/data/corrections.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/data/corrections.json) | blob `60370924e13233bbd2cccb517bfffee002dad915` | [L4–20](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/data/corrections.json#L4-L20) `rsp_cd` corruption (keys include `market_prices`, `market_prices_after`, `market_orderbook`, `market_orderbook_after`); L21–30 (`orders_estimate` uses `mxpr`); L142–155 (KRX 애프터마켓 change) |
| M7 | repo [`docs/errors.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/docs/errors.md) | blob `b4b2eac6541bd2b886071c1caad17fa0c57ba3e6` | L7–9 (errors are HTTP 500); L77–100 error table (**no tick-size or order-hours code listed**) |
| M8 | repo [`llms.txt`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/llms.txt) | blob `8351d5343d785b61107179d19197c59a08e1edff` | L120–121 rate limit |
| M9 | repo [`README.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/README.md) | blob `61aa5f7f2c1059a29a99175a5cdf573996d81479` | L11 portal canonical; L125 no paper account |
| M10 | repo [`meritz/core/client.py`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/core/client.py) | blob `7c68d3a4006730c09b18acb90ddcf2d478a40c16` | L58–68 (constant `tmpr_susp_yn="N"` on missed lookups); L127–131 (`rsp_sub_msg` "8337 의 호가 단위") |
| M11 | repo [`position_sizing/money.py`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/position_sizing/money.py) | blob `31c651193d7c0df463d155f18858a0eaa8d65ea8` | L10–21 hard-coded KRX tick table (publisher client code) |
| M12 | repo [`indicators/candles.py`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/indicators/candles.py) | blob `edef8b4e22aa9474f4e595ab520e837cd24b2f25` | L79–83 daily close after the 9/14 after-market change |
| M13 | repo [`asyncapi.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/asyncapi.json) | blob `c108c3c52288d5296b2871582ff856d532073242`; `asyncapi 3.0.0`, `info.version 2026-10-22` | Names only: `trht_yn` "거래정지여부", `mkop_clcd` "신장운영구분코드" in `ohhts_stck_cntg`/`ohhts_nxt_cntg`/`ohhts_unt_cntg`; `frml_ovtm_cls_code` in order notices `ohhts_cntg_infr`/`ohhts_cntg_rslt` (L2408–2409, L2644–2645) |

M4 is not used; the source IDs follow the trade audit's numbering.

**Missing evidence:**

- The portal notice board (rate limits; the trade audit's M2) was
  not retrieved.
- No portal page states API service hours or maintenance windows.
- There is no code list for `issu_stat_cls_code`, the `*_mkop_cls_code`
  fields, `frml_ovtm_cls_code`, `oder_trnm_stat_code` or
  `shrn_mkop_cls_code`. M1 says outright that names are not provided.
- There is no VI field in any domestic REST or WebSocket route.

### 7.2 Routes

Transport (M1, M5): `GET` with a query string on
`https://openapi.imeritz.com:9443`, `contentType` "application/json;
charset=utf-8". Two headers are required:

- `authorization` (Bearer);
- `mac_address`: "호출 단말의 MAC 주소입니다. 12자리로 넣습니다. 넣지
  않으시면 요청이 거부됩니다."

M1 files query inputs under request "body", but the `requestExample` and
M5 use a query string. There is no paper environment: M9 L125 "앱키에
연결된 계좌는 실계좌입니다. 모의계좌는 없습니다". M5 gives `x-tps "10"` for
every route below.

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Purpose | Evidence |
| --- | --- | --- | --- | --- | --- |
| "현재가 조회" / "주식 현재가 조회" | `GET /market/v1/prices?mrkt_div_code=&iscd=` | `ohhts_1001_001r` | real only | `mxpr`, `llam`, `sdpr`, `aspr_unit`, `deal_qty_unit`, `issu_stat_cls_code`, `tmpr_susp_yn`, `sltr_yn`, `invt_epmd_cntt`, `oprc_rang_exts_yn`, `clpr_rang_exts_yn` | field table + publisher example |
| "호가 조회" / "주식 호가 조회" | `GET /market/v1/orderbook?mrkt_div_code=&iscd=` | `ohhts_1001_005r` | real only | `mxpr`, `llam`, `sdpr`, `shrn_mkop_cls_code`, `nw_mkop_cls_code` | field table + publisher example |
| "시간외 단일가 조회" / "주식 시간외 현재가 조회" | `GET /market/v1/prices/after` | `ohhts_1181_002r` | real only | `ovtm_untp_mxpr`, `ovtm_untp_llam`, `ovtm_untp_sdpr` | field table |
| "시간외 단일가 호가 조회" / "주식 시간외 호가 조회" | `GET /market/v1/orderbook/after` | `ohhts_1181_001r` | real only | same `ovtm_untp_*` limit fields | field table |
| "국내 영업일 조회" — "영업일 여부와 전전·전·익·익익 영업일" | `GET /reference/v1/market-days` (no input) | `obcpp_bsdy_021r` | real only | five business dates + regular-session start/end | field table + publisher example |
| "국내 장운영 조회" — "국내 시장의 장운영 상태와 시간표를 조회합니다." | `GET /reference/v1/market-hours?mkpl_cls_code=` | `obtrs_sstm_506r` | real only | current phase codes + today's timetable per KRX market segment | field table + publisher example |

Out of scope (overseas), listed by name only:

- `GET /reference/v1/overseas/market-hours` (`obtro_comn_010r`,
  `ovrs_mkop_cls_code` "\"004\": 정규장 개시 · \"012\": 시장이 닫혀 있는
  동안");
- `/reference/v1/overseas/market-days` (`obtro_comn_006r`, `bsop_date`);
- `/market/v1/overseas/prices` (`shnu_aspr_unit`, `seln_aspr_unit`,
  `vcm_stat_cls_code` "변동성 완화장치(VCM) 상태입니다." with no code list,
  and `mxpr`/`llam`, which are 0 for US/HK examples).

WebSocket (names only, M1 `groups[4]`, M13): "(실시간) 국내주식 현재가
(SOR 통합/KRX/NXT/시간외단일가)" carry `trht_yn` and `mkop_clcd`. There is no
dedicated 장운영 or VI channel.

**Venue selector** (`mrkt_div_code`, String len 2, required; prices and
orderbook): "어느 시장의 시세를 볼지 정합니다. "J": KRX "NJ": 대체거래소(NXT)
"TJ": KRX + NXT 통합 위 세 값만 넣으십시오. 그 밖의 값도 오류 없이 정상
응답코드로 내려올 수 있으므로 보내는 값을 먼저 확인하십시오." For the
`…/after` routes: "시간외 단일가는 "J" 로 조회하십시오."

### 7.3 Tick size (호가단위)

- **Field:** `/market/v1/prices` `aspr_unit` (Number, len 13, required)
  "호가단위" — "호가 단위입니다." Example `1000` alongside `stck_prpr`
  `1263000` (publisher example; values illustrative).
- **Related field:** `deal_qty_unit` (Number) "매매수량단위" — "매매 수량
  단위. 주문 수량은 이 단위의 배수여야 합니다."
- **Guide:** M2 text L217: "주문 단가는 종목의 호가단위(현재가 조회의
  aspr_unit)에 맞아야 합니다." (publisher guide)
- **Not on** `orderbook`, `prices/after`, `orderbook/after` or the
  market-hours route.
- **Venue:** `aspr_unit` is returned for whatever `mrkt_div_code` is
  requested (`J`/`NJ`/`TJ`). Whether it differs by venue, and what `TJ`
  returns, is **not documented**. M2's order example uses
  `exch_kind_code` "01 KRX, 02 NXT, 03 SOR" (text L196); which venue's tick
  applies to an SOR order is not stated.
- **Publisher client code (not a contract):** M11 L10–21 hard-codes a table
  with the comment "국내 주식의 호가 가격단위 (2023-01-25 개편 기준,
  유가증권·코스닥 주식). ETF·ETN·ELW·채권은 표가 다르다. 그쪽에 쓰지 말
  것."
  - `_KRX_STOCK_TICKS = ((2_000, 1), (5_000, 5), (20_000, 10), (50_000,
    50), (200_000, 100), (500_000, 500))`, upper bound exclusive, else
    `1_000`.
  - `tick_floor`/`tick_ceil` accept an explicit `tick` and fall back to
    this table only when none is given (L24–37). The repo never wires
    `aspr_unit` into it.
  - Not a contract and not authoritative for NXT, ETFs or other products.
- **Rejection code:** M10 L130 mentions "8337 의 호가 단위" as an
  `rsp_sub_msg` example. M7's error table has **no** `8337` entry, so the
  tick-rejection code is unconfirmed.

### 7.4 Price limits (상한가 / 하한가 / 기준가)

| Route | Field | Type, len | Description (verbatim) |
| --- | --- | --- | --- |
| `/market/v1/prices`, `/market/v1/orderbook` | `mxpr` | Number, 13 | "당일 주문 가능한 최고 가격(상한가)입니다." |
| same | `llam` | Number, 13 | "당일 주문 가능한 최저 가격(하한가)입니다." |
| same | `sdpr` | Number, 13 | "당일 기준가(전일 종가)" |
| `/market/v1/prices/after` | `ovtm_untp_mxpr` / `ovtm_untp_llam` | Number, 13 | "시간외 단일가 상한가입니다. 0 으로 내려올 수 있으므로 가격 범위 판단에 쓰지 마십시오." (하한가 same) |
| same | `ovtm_untp_sdpr` | Number, 13 | "시간외 단일가의 기준가입니다. 정규장 현재가(stck_prpr)와 다른 값이 내려올 수 있습니다." |
| `/market/v1/orderbook/after` | `ovtm_untp_mxpr` / `ovtm_untp_llam` | Number, 13 | "시간외 단일가로 낼 수 있는 가장 높은 가격 자리입니다. 이 조회에서는 같은 응답의 시간외단일가현재가와 기준가가 채워져 있을 때에도 0 으로 내려옵니다. 이 항목을 가격 범위 판단에 쓰지 마십시오." |
| same | `ovtm_untp_sdpr` | Number, 13 | "… 정규장 기준가(sdpr)와 다른 값이 내려올 수 있으므로 서로 바꿔 쓰지 마십시오." |
| `/market/v1/prices`, `orderbook`, ticks, candles | `prdy_vrss_sign` | String, 2 | "전일 대비 부호 "1": 상한 "2": 상승 "3": 보합 "4": 하한 "5": 하락" |

- **JSON types:** prices are JSON integers in the examples (`"mxpr":
  1640000`, `"llam": 884000`, `"sdpr": 1262000`).
- **Per venue:** limits come back for the requested `mrkt_div_code`.
  Whether `J`, `NJ` and `TJ` can differ is **not documented**. Every
  example uses `J`.
- **기준가 vs 전일종가:**
  - `sdpr` is described as "당일 기준가(전일 종가)", i.e. as the previous
    close.
  - The daily-candle route (M1 `apis[15]`) says `prdy_vrss` is measured
    against "전일 정규장 종가(기준가)".
  - `exch_use_yn`: "정규장 종가는 mrkt_div_code "TJ" 와 "Y" 를 함께 넣을
    때만 내려옵니다. "J"·"NJ" 에서는 "Y" 와 "N" 의 결과가 같아서, "J" 에
    "Y" 를 넣어도 애프터마켓까지 포함한 값이 내려옵니다."
  - Conclusion: 기준가 = previous **regular-session** close, which is not
    the `J`/`NJ` daily-candle close (see §7.8 item 4).
- **Order-side link:** M6 L29 (publisher repo note) says
  `orders/estimate` with `oder_unpr=0` sizes market orders "당일
  상한가(mxpr) 기준으로".
- **Success code caveat:** M6 L4–20 lists `market_prices`,
  `market_prices_after`, `market_orderbook` and `market_orderbook_after`
  under "응답 rsp_cd 손상": "HTTP 200 과 정상 data 를 주면서 rsp_cd 에
  널바이트가 섞여 옵니다." Workaround: "data 가 있으면 정상으로 보십시오."
  M1 also says an unknown `iscd` returns `"0000"` with zero or empty
  values. So `mxpr = 0` can mean "symbol not found" rather than "no limit".

### 7.5 Trading sessions and hours

`GET /reference/v1/market-hours` (M1 `apis[26]`, M5 L8963–9247).

**Request:** `mkpl_cls_code` (String 2, required): "조회할 매매시장
코드입니다. 두 자리로 넣으십시오. "01" 유가증권 · "02" 코넥스 · "03" 코스닥
· "24" 소액채권 (query string)". There is **no NXT code**. `data` is
"요청한 매매시장의 당일 장운영 정보입니다."

**Phase / status codes** (all String). Each says its code names are not
provided:

| Field | Len | Description (verbatim, abridged only where marked …) | Example |
| --- | --- | --- | --- |
| `mkop_cls_code` 장운영구분코드 | 3 | "현재 시점의 장운영 상태를 나타내는 세 자리 코드입니다. 시장마다 값이 다르고 시각에 따라 바뀌며, 코드에 대응하는 이름은 제공되지 않습니다. 장이 끝난 뒤에도 "000" 이 되지 않는 시장이 있으므로 "000" 여부로 장 종료를 판정하지 마십시오." | `"000"` |
| `frml_ovtm_cls_code` 정규시간외구분코드 | 1 | "한 자리 구분 코드입니다. 값에 대응하는 이름은 제공되지 않습니다." | `"0"` |
| `mkob_mkop_cls_code` 장개시전장운영구분코드 | 3 | "장 개시 전 구간의 장운영 상태 코드입니다. … 코드에 대응하는 이름은 제공되지 않습니다." | `"000"` |
| `pgtr_` / `cptn_bltr_` / `trst_` / `buyin_mkop_cls_code` | 3 | 프로그램매매 / 경쟁대량매매 / 자사주 / BUYIN 장운영 상태; names "제공되지 않습니다" / "응답에 함께 오지 않습니다" | `"000"` |
| `oder_stop_yn` 주문중지여부 | 1 | "주문 중지 여부입니다." (value set not given) | `"0"` |
| `oder_trnm_stat_code` 주문전송상태코드 | 1 | "… 값에 대응하는 이름은 응답에 함께 오지 않습니다." | `"2"` |
| `pros_date` 처리일자 | 8 | "이 장운영 정보가 적용되는 일자입니다. YYYYMMDD 8자리." | `"20260911"` |

**Timetable fields:** String, declared length 9, each described as
"HHMMSS 형식". These are the publisher example values:

| Field (name) | Example |
| --- | --- |
| `oprc_untp_begn_time` / `oprc_untp_clsn_time` (시가단일가) | `083000000` / `090000000` |
| `clpr_untp_begn_time` / `clpr_untp_fin_time` (종가단일가) | `152000000` / `153000000` |
| `mkob_ovtm_begn_time` / `mkob_ovtm_fin_time` (장개시전시간외) | `083000000` / `084000000` |
| `mkfa_ovtm_begn_time` / `mkfa_ovtm_cntg_indc_time` / `mkfa_ovtm_fin_time` (장종료후시간외) | `153000000` / `154000000` / `160000000` |
| `ovtm_untp_begn_time` / `ovtm_untp_fin_time` (시간외단일가) | `160000000` / `200000000` |
| `pgm_aspr_fin_time` (프로그램호가종료) — "HHMMSS 6자리로 내려옵니다." | `152000` |
| `trst_tr_fin_time`, `itmt_cptn_bltr_fin_time` ("앞 6자리(HHMMSS)만 잘라 쓰십시오. 소액채권(24)은 빈 문자열이 내려옵니다.") | `150000000` |
| `gnrl_` / `tday_byng_trns_tr_begn/fin_time` (BUYIN) | `153500000`–`154500000` / `175000000`–`180000000` |

- **No regular-session start/end field** in market-hours. Those come from
  `/reference/v1/market-days` `sta_hour` / `fin_hour` (String 6,
  "정규장이 시작되는/끝나는 시각(HHMMSS 6자리)… 시장별 시각은 국내 장운영
  조회(/reference/v1/market-hours)를 쓰십시오."; example `090000` /
  `153000`).
- **Orderbook phase codes:**
  - `shrn_mkop_cls_code` (String 3) "장 운영 구분입니다. 시장
    (mrkt_div_code)마다 값이 다르며 빈 값으로 내려올 수 있습니다." —
    example `"AC2"`.
  - `nw_mkop_cls_code` (String 2) "장 운영 상태 코드입니다(2자리, 빈 값
    가능). 같은 항목이 실시간 구독에서는 mkop_clcd 라는 이름으로
    내려옵니다." — example `"20"`.
  - No code list for either.
- **After-market change (publisher repo note, M6 L142–155):**
  - "2026-09-14 부터 KRX 시간외 단일가(16:00~18:00)가 애프터마켓
    (16:00~20:00, 실시간 체결)으로 바뀌어 "81" 은 더 쓰지 않습니다.
    애프터마켓 주문에 쓰는 별도 oder_cls_code 는 포털 명세에 없습니다. …
    대상은 코스피·코스닥 주식과 DR 이고 ETF·ETN 은 제외입니다."
  - Workaround: "16:00~20:00 에는 oder_cls_code 에 "01"·"12"·"13" 을 사용할
    수 있습니다."
  - M1 field names still say "시간외단일가" (see §7.8 item 2).
- **NXT sessions** (pre/after market, 08:00–20:00): **not documented** by
  any Meritz REST route. `mkpl_cls_code` has no NXT value.
- **After-close quote behaviour (publisher guide, M2 text L278):** "장
  마감 후에 조회하면 shrn_iscd 와 stck_prpr 는 0 으로 옵니다." (orderbook)
- **API service hours:** not found in M2, M3 or the repo.
- **Rate:** `x-tps "10"` (M5). M7 L95 / M8 L120 say 10 per second per API,
  and an exceeded limit arrives as HTTP 500 `EGW00200`.

### 7.6 Holiday / trading calendar

`GET /reference/v1/market-days` (`obcpp_bsdy_021r`, M1 `apis[25]`, M5
L8843–8960):

- **Request:** no parameters besides the headers. There is **no date
  input**; the route always answers for "조회 시점".
- **Response `data`** (Object): "조회 기준일의 영업일 정보입니다. 직전·당일·
  다음 영업일과 정규장 개시·종료 시각이 한 건으로 들어 있습니다. 앞뒤로 각각
  두 영업일이 내려옵니다."

| Field | Type, len | Description (verbatim) | Example |
| --- | --- | --- | --- |
| `tday_bsdy` 당일영업일 | String, 8 | "조회 시점의 영업일입니다. YYYYMMDD 8자리." | `"20260911"` |
| `bef_bsdy` 전영업일 | String, 8 | "직전 영업일입니다. YYYYMMDD 8자리." | `"20260910"` |
| `bef_bef_bsdy` 전전영업일 | String, 8 | "직전 영업일의 그 앞 영업일입니다." | `"20260909"` |
| `nx_bsdy` 익영업일 | String, 8 | "다음 영업일입니다. YYYYMMDD 8자리." | `"20260914"` |
| `nx_nx_bsdy` 익익영업일 | String, 8 | "다음 영업일의 그 다음 영업일입니다. YYYYMMDD 8자리." | `"20260915"` |
| `sta_hour` / `fin_hour` | String, 6 | regular-session start/end (§7.5) | `"090000"` / `"153000"` |
| `tr_cont` | String, 1 | "항상 "0"으로 내려옵니다. 이 API는 연속조회를 지원하지 않습니다." | `"0"` |
| `rsp_cd` | String, 8 | "이 API 의 성공 응답 코드는 "0000"(정상 처리)입니다. 성공 코드는 API 마다 다릅니다. 다른 API 에서는 "5766"·"5762"·"5820" 등이 성공 코드입니다." | `"0000"` |

- **Holiday flag:** **none.** The API description promises "영업일 여부",
  but no 영업일/휴장 field exists. What `tday_bsdy` holds when called on a
  holiday or weekend is not documented. **Inference:** compare
  `tday_bsdy` with the local KST date. This is unverified.
- **Range:** five dates centred on "now"; there is no year calendar or
  look-ahead beyond two business days.
- **Market scope:** no market selector. Whether the dates are KRX-only or
  also NXT is not stated.
- **Related holiday behaviour on another route:** `/trading/v1/orders/history`
  `oder_date` says "휴장일은 오류가 아니라 "5820" 과 0건이 내려옵니다."
- **Update cadence:** not documented. **Paper:** none (M9 L125).

### 7.7 Instrument / market status

| Status | Route + field | Values / description (verbatim) |
| --- | --- | --- |
| Instrument status code | `/market/v1/prices` `issu_stat_cls_code` (String 2) | "종목 상태 구분 코드입니다(2자리)." **No code list.** Example `"55"`; its meaning is not documented. |
| Temporary halt | `/market/v1/prices` `tmpr_susp_yn` (String 2) | "임시 정지 여부 "Y": 정지 "N": 정상". M10 L65 (publisher client code): the gateway can return constant fields such as `tmpr_susp_yn="N"` even when the lookup missed. |
| 거래정지 (WebSocket only) | `trht_yn` (String 1) in 현재가 SOR/KRX/NXT/시간외 feeds | "거래정지 여부입니다. "Y": 거래정지 "N": 정상 거래" (name only; WebSocket out of scope) |
| 정리매매 | `/market/v1/prices` `sltr_yn` (String 2) | "정리매매 여부 "Y": 해당 "N": 비해당" |
| 투자유의 text | `/market/v1/prices` `invt_epmd_cntt` (String 50) | "투자 유의 안내 문구입니다." Free text; example `""`. |
| Price-range extension | `oprc_rang_exts_yn`, `clpr_rang_exts_yn` (String 2) | "시가/종가 결정 시 가격 범위가 연장되었는지 여부입니다. "Y": 연장 "N": 미연장 빈 값으로 내려올 수 있으므로 빈 값을 함께 처리하십시오." |
| Credit / short-sell eligibility | `crdt_able_yn`, `ssts_yn` | "신용 거래 가능 여부 "Y": 가능 "N": 불가"; "공매도 가능 여부 "Y": 가능 "N": 불가" |
| Order-time designation (reserved orders) | `/trading/v1/reserved-orders/{buy,sell,cancel}` response `warn_cls_code` (String 1) | ""0": 정상 접수 "1": 경고 "2": 보류 "3": 투자유의 "4": 경고 + 투자유의 "5": 보류 + 투자유의 "6": 단기과열 "7": 경고 + 단기과열 "8": 보류 + 단기과열 "9": 투자경고 "a": 경고 + 투자경고 "b": 보류 + 투자경고 "c": 투자위험 "d": 경고 + 투자위험 "e": 보류 + 투자위험 "f": 정리매매 "g": 경고 + 정리매매 "h": 보류 + 정리매매" |
| Order-time designation (regular orders) | `/trading/v1/orders/{buy,sell,modify,cancel}` and credit orders, `warn_cls_code` | ""0": 정상 접수 경고 ― "1" "3" "4" "6" "7" "9" "a" "c" "d" "f" "g" … 보류 ― "2" "5" "8" "b" "e" "h"" — the same letters, without names |
| VI | — | **not found** in domestic REST or WebSocket. Overseas `vcm_stat_cls_code` only, with no code list. |
| 관리종목, 투자경고 (as a quote field) | — | **not found** as dedicated fields. **Inference:** possibly encoded in `issu_stat_cls_code`, but no code list exists. |
| Market-level order stop | `/reference/v1/market-hours` `oder_stop_yn` | "주문 중지 여부입니다." Values not listed; example `"0"`. |

### 7.8 Contradictions and gaps

1. **Time format in market-hours.** Fields say "HHMMSS 형식" but are
   declared length 9, and the example values are nine digits
   (`083000000`). `pgm_aspr_fin_time` alone is six digits ("HHMMSS
   6자리로 내려옵니다"), and `itmt_cptn_bltr_fin_time` says "앞 6자리만
   잘라 쓰십시오". **Inference:** the trailing three digits are sub-second
   or padding. That meaning is not documented.
2. **Outdated "시간외단일가" naming.** M1 still names `ovtm_untp_*` fields
   and routes "시간외 단일가". M6 L150 says that session became the
   애프터마켓 (16:00~20:00) on 2026-09-14. The market-hours example has
   `pros_date` `20260911`, which is **before** the change, yet shows
   `ovtm_untp_fin_time` `200000000` (20:00) rather than 18:00. The example
   values cannot be relied on as historical.
3. **"영업일 여부" promised, not delivered.** The `market-days` description
   mentions 영업일 여부, but no flag field exists. The `data` text says
   "조회 기준일", yet no reference-date input exists.
4. **기준가 vs 전일 종가.** `sdpr` is described as "기준가(전일 종가)". The
   candle route defines 기준가 as "전일 정규장 종가", and after
   2026-09-14 the `J`/`NJ` daily close includes after-market trades (M1
   `exch_use_yn`; M12 L79–83). A client that computes 기준가 from the
   `J` daily close would be wrong. **Inference:** use `sdpr`.
5. **Unnamed phase codes.** `mkop_cls_code`, `nw_mkop_cls_code`,
   `shrn_mkop_cls_code` (e.g. `"AC2"`) and `issu_stat_cls_code` (e.g.
   `"55"`) have no published code lists. The publisher explicitly warns
   against treating `"000"` as "closed". `frml_ovtm_cls_code` has a code
   list only in the WebSocket order-notice schema (M13 L2409: ""0": 해당
   없음 "1": 정규장 "2": 장 개시 전 시간외 종가"). Whether that list
   applies to the REST market-hours field is **not documented**.
6. **After-hours limits unusable.** `ovtm_untp_mxpr`/`llam` may be 0
   (prices/after) or are always 0 (orderbook/after) "이 항목을 가격 범위
   판단에 쓰지 마십시오". No other after-market limit source is
   documented.
7. **Success-code divergence.** The success code is `"0000"` for
   market-days, prices and orderbook, but `"5766"` for market-hours. On top
   of that, M6 L4–20 says the quote routes' `rsp_cd` arrives corrupted.
   Unknown `iscd` / `mrkt_div_code` values return success with zeros, so
   `mxpr`/`llam`/`aspr_unit` = 0 is ambiguous.
8. **NXT coverage.** Quotes accept `NJ`/`TJ`, but there is no NXT
   market-hours code, no NXT holiday statement and no documented
   per-venue tick or limit.
9. **Tick-rejection code.** `8337` appears only in client-code prose (M10
   L130), not in M7's error table.
10. **Example data are internally inconsistent** (e.g. `prices/after`:
    `stck_prpr 8389000` vs `ovtm_untp_sdpr 1681000` for one symbol), as
    M2 text L278 warns: "숫자는 임의의 값입니다." Do not derive rules from
    example values.

### 7.9 Gates and not-verified items

See §10 and §11 (items tagged [Meritz]). Meritz-specific: there is no
paper environment, so any verification needs separate authorization for
**real** read-only calls plus a sanctioned `mac_address` source; the
publisher sample's auto-detection is not an acceptable pattern (G-E2).
Treat `mxpr` / `llam` / `sdpr` = 0 or empty as unknown (G-L6).

## 8. Cross-broker comparison

### 8.1 Evidence by concern

Short form; details and pins are in §2–§7.

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| **Price limits** (per symbol) | `stck_mxpr` / `stck_llam`; names only, no types (E) | `upl_pric` / `lst_pric`, **signed** strings (F) | `uplmtprice` / `dnlmtprice`, Number (F+E) | `Mxpr` / `Llam`, strings; `""` on index rows (F+E) | dedicated route `/price-limits`; decimal string or `null` (F) | `mxpr` / `llam`, Number; 0 for unknown symbols with a success code (F) |
| After-hours limits | separate `ovtm_untp_*` columns (E) | not found | not found | not found | not found | `ovtm_untp_*`, documented as 0 / unusable (F) |
| Limit venue scope | J / NX / UN selector; per-venue values not documented | `stk_cd` suffix; not documented | `exchgubun` on t1102/t8450 only; not documented | `J` / `NJ` / `UJ`; not documented | integrated; no selector | `J` / `NJ` / `TJ`; not documented |
| **기준가 vs 전일종가** | two columns, relation undocumented (E) | `base_pric` vs `pred_close_pric` / `lastPrice`, different routes (F) | t8430/t8436: two fields; t8450: "전일종가(기준가)" (F) | `Sdpr` only (F) | `basePrice` only in rankings; daily `closePrice` may differ (F+G) | `sdpr` "당일 기준가(전일 종가)"; = previous **regular-session** close (F) |
| **Tick size** | `aspr_unit` label only (E); client table (C) | not found | not found | not found; reactive code `2706` | only after a rejected order (`data.tickSize`) (F) | `aspr_unit` on `/prices`, documented for order prices (F+G); client table (C) |
| **Calendar** | per-date flags `bzdy_yn` / `tr_day_yn` / `opnd_yn` / `sttl_day_yn`; 1 call/day (E) | not found | not found (`t0167` = server clock) | not found | prev / today / next business day; `integrated: null` = holiday (F+G) | five business dates around now; no date input, no holiday flag (F) |
| **Session hours** | docstrings only, KRX (E) | WS `0s` code list only | chart summaries (KRX + NXT pre/after), meaning undescribed (F+E) | NXT order-acceptance windows only, overlapping (G) | KRX+NXT **union** timetable, KST (F) | KRX segment timetable, no NXT (F) |
| **Session phase (REST)** | `new_mkop_cls_code`, no list (E) | none (filters only) | none; `ho_status` no list | none | none | `mkop_cls_code` etc., names "제공되지 않습니다" (F) |
| **Halt** | `temp_stop_yn`, `trht_yn`, `tr_stop_yn`, `nxt_tr_stop_yn` (E) | none | text `info3` "정지/연장구분"; list TR t1405 (F) | none on REST (WS names) | `krxTradingSuspended`, `nxtTradingSuspended` (F) | `tmpr_susp_yn` (REST); `trht_yn` WS only (F) |
| 관리 / warnings | many flags, no encodings (E) | `orderWarning` list (incomplete), `state` text (F) | text fields; list TRs t1404/t1405 (F) | none on REST | warnings enum; 관리 and 투자주의 not found (F) | `issu_stat_cls_code` (no list), `sltr_yn`, text; order `warn_cls_code` list (F) |
| **VI** | route + flags; times and prices; no venue selector (E) | route `ka10054` with venue; times, no date (F+E) | static-VI prices; trigger as text (F) | not found | warnings enum, **date** granularity, `exchange` (F) | not found |
| Real / paper documented | no | mock domain listed | no paper REST origin documented | ⭕ in SDK matrix, same origin | none | none ("모의계좌는 없습니다") |

### 8.2 Contradictions between broker sections

1. **KRX after-hours single-price window.** KIS docstrings say "국내주식 시간외
   단일가(16:00~18:00)" (§2.5, K20) and Kiwoom's WebSocket `0s` code list
   ends 시간외 단일가 at 18:00 (§3.5). Meritz's repo note says that from
   2026-09-14 this session became an 애프터마켓 "16:00~20:00" (§7.5, M6),
   the Meritz market-hours example shows a 20:00 end (§7.8 item 2), and
   the LS `t8453` example gives a KRX after-market `"160000"`–`"200000"`
   (§4.5). These are all publisher texts; this audit does not establish
   which is current. **Inference:** the KIS and Kiwoom texts may predate
   the change.
2. **Start of the NXT after-market.** DB says "애프터마켓 : 15:30 ~ 20:00 …
   (15:30~40: 지정가만 가능)" (§5.5) and the Toss example starts the
   after-market at 15:30 with a single-price auction to 15:40 (§6.5); the
   LS `t8453` example gives NXT after-market `"154000"`–`"200000"` (§4.5).
   **Inference:** LS may report only the continuous part; not documented.
3. **Is 기준가 the previous close?** Meritz (`sdpr` "당일 기준가(전일
   종가)") and LS `t8450` ("전일종가(기준가)") equate them in labels. Toss
   says the daily `closePrice` "등락률 계산 기준가와 다를 수 있습니다";
   Meritz itself narrows 기준가 to the previous *regular-session* close.
   KIS, Kiwoom and LS `t8430`/`t8436` keep two separate fields.
4. **Tick tables agree, but only as client code.** KIS (K26, K27, "2023년
   기준") and Meritz (M11, "2023-01-25 개편 기준") hard-code the same seven
   bands; Toss's one example band ("50,000~200,000원 구간은 100원 단위")
   matches both. Meritz's comment limits its table to 유가증권·코스닥 stocks
   ("ETF·ETN·ELW·채권은 표가 다르다"); KIS's does not. None is a contract.
5. **Same field name, different documentation.** KIS and Meritz both use
   `aspr_unit` "호가단위", `ovtm_untp_*`, `prdy_vrss_sign` and an "임시 정지
   여부" flag (`temp_stop_yn` / `tmpr_susp_yn`). Meritz documents
   `aspr_unit` as the order tick; KIS gives only a label. **Inference:**
   similar names do not transfer semantics between brokers.
6. **"장구분" / "장운영구분" mean different things across brokers too.** LS
   `janginfo` "장구분" is a market (§4.8 item 1); Kiwoom `mrkt_open_tp`
   "장운영구분" is a request filter; KIS `new_mkop_cls_code` and Meritz
   `nw_mkop_cls_code` / `mkop_cls_code` are phase codes of different
   lengths without code lists. No field may be mapped by its Korean name.
7. **"No value" has six encodings.** Kiwoom signs limits; DB returns `""`;
   Meritz returns 0 for unknown symbols and for after-hours limits; Toss
   returns `null` where there is no limit; LS and KIS give no rule.
8. **Calendar shapes are incompatible.** KIS returns four per-date flags;
   Toss three neighbouring business days with `null` for a holiday;
   Meritz five neighbouring business dates and no flag. Toss calls
   `KrMarketDay.date` "영업일" yet returns a holiday there (§6.8 item 2);
   Meritz promises "영업일 여부" without a field (§7.8 item 3).
9. **VI granularity.** KIS and Kiwoom give trigger / release times and
   prices; Toss gives dates only; LS gives static-VI price bands; DB and
   Meritz give nothing on REST.

### 8.3 What a common surface could and could not rely on

All statements in this subsection are **Inference:**; the maintainer
decides.

- **Price limits** are the only concern all six brokers expose per symbol.
  A nullable, broker-qualified limit pair is the most plausible common
  element. It could not rely on a common encoding (§8.2 item 7), on a
  venue rule (Toss is integrated; the rest are undocumented per venue), on
  a defined trading day ("당일" is undefined outside regular hours), or on
  after-hours limits. "Unknown" would have to stay distinct from "no
  limit".
- **기준가** is per symbol at five brokers (Toss only in rankings). It could
  not be equated with `previous_close` (§8.2 item 3).
- **Tick size:** only Meritz documents a per-symbol tick field for order
  prices; KIS has an undocumented column; Toss reveals it only after a
  rejected order; LS, DB and Kiwoom have nothing. A common tick size could
  not rely on broker evidence.
- **Calendar:** three brokers (KIS, Toss, Meritz) with incompatible shapes;
  three with none. A common calendar would need a per-broker capability
  flag and an "unsupported" error. "Is today a trading day" is answerable
  directly only from KIS flags (semantics undefined) and Toss `null`.
- **Session hours:** Toss (KRX+NXT union) and Meritz (KRX segments only)
  publish timetables on REST; no broker gives a complete per-venue
  timetable. A common session schedule could not rely on broker data.
- **Phase and status:** codes without names (KIS, Meritz), free text (LS,
  Kiwoom `state`) and enums (Toss) cannot share an enum. Only a raw,
  broker-qualified status would be faithful.

### 8.4 Spot re-check of merged pins

Recomputed from the retrieved copies before merge; all matched.

| Broker | Pin re-checked | Result |
| --- | --- | --- |
| LS | L1 sha256 `9aaca437f1925115` (2,792,313 bytes); L1 L18440 / L18445 `uplmtprice` / `dnlmtprice`, L19005 `janginfo`, L16855 / L22756 `jgubun`, L21567–21571 t1427 `jc_num` "대상제외값(설정시 저장됨)" | match |
| LS | L3 (t1102) sha256 `42712ce969a8a480`; L5 (t8450) sha256 `0f663f3a7ab7095c` | match |
| DB | D1 blob `5930af396f4a74ff…` (L197, L257 "(이하 생략 — 가이드 참조)", L380 `InputHourClsCode`); D2 blob `a6e13e46fafb3eed…` (L256–259 NXT 접수시간) | match |
| DB | D3 blob `889d4557b9a60d79…` (L123 `2706`, L139–140 `3180`/`3181`, L167–168 `M100`); DP3 PRICE sha256 `a16222751d181c84`, MULTIPRICE `94360bc187c75c90`; DP2 MULTIPRICE example has `"Mxpr": ""`, `"Llam": ""` | match |
| Toss | T1 sha256 `c5918961335ccd6b`, `info.version` `1.2.28`, `getPriceLimit` "상/하한가 조회", `KrMarketDay.date` "영업일 (KST 기준)"; T2 sha256 `bef057d9babe9a38` L249–250 | match |
| Toss | T4 sha256 `6ad4c02b8e785f7d`, L42 (기준가 only in rankings), L81 (`integrated` `null` = 휴장일), L82 (no per-venue hours) | match |
| Meritz | M1 raw sha256 `afc8983dbc6507ee`; M5 blob `93e900e66b965607…` (L6804 `mxpr`, L6893 `aspr_unit`, L8985 `mkpl_cls_code`, L9039 `mkop_cls_code`) | match |
| Meritz | M6 blob `60370924e13233bb…` L150; M11 blob `31c651193d7c0df4…` L10–12; M7, M8, M9, M10, M12, M13 blobs; M9 L11, L125; M10 L65, L130; M13 L2409 | match |

## 9. Relation to existing repository documents and models

None of the files below is edited by this change. Paths are on `main` at
`a5d2639` unless a branch is named.

| Document / model and claim | This audit |
| --- | --- |
| [`Ticker`](../../src/ktradelink/models/ticker.py) (L18, L23–45): price fields `last`, `open`, `high`, `low`, `previous_close`, `bid`, `ask`, plus `volume`, timestamps, `scope_description` and a scalar `info` mapping | **No** field for upper / lower limit, 기준가, tick size, session / market phase, or instrument status. The Rust core `Prices` (`crates/ktradelink-core/src/lib.rs` L112–117) likewise ends at `previous_close`. See the model implication below. |
| [market-data spec](../specifications/market-data-v0.1-draft.md) L99–104: `previous_close` is the "completed regular-session official closing price" only if the native response reliably identifies it | KIS `stck_sdpr`, Kiwoom `base_pric`, LS `recprice`, DB `Sdpr`, Meritz `sdpr` and Toss `basePrice` are **기준가**. Only Meritz describes 기준가 as the previous regular-session close, and it is still labelled 기준가. None should fill `previous_close` without a maintainer decision (§8.2 item 3). |
| [offline decoder usage](../usage/offline-six-broker-ticker-decoders.md) L65–67: "DB `Sdpr` is never assigned to `previous_close`. Signed Kiwoom `cur_prc` strings fail until its native semantics are documented" | Consistent, and the same rule extends to the other five brokers' 기준가 fields. Kiwoom's signed `upl_pric` / `lst_pric` and DB's `""` limits would fail the same parser. |
| [six-broker-ticker-decoders.md](six-broker-ticker-decoders.md) L95–100: a reported zero may mean halt or sentinel (unverified); no hidden request for a "calendar or reference price" | Consistent. Meritz documents zeros for unknown symbols with a success code and for after-hours limits (§7.4, §7.8); halt flags elsewhere have undocumented or partial encodings. |
| market-data spec L159–164: `session="regular"` must error rather than mislabel; "Session timestamps, DST, holidays, and exchange schedule require explicit tests" | No broker documents the session coverage of its quote routes. Three brokers document a calendar route, with incompatible shapes (§8.2 item 8). |
| market-data spec L214–215: "suspended trading must be distinguished from missing data" | Candidate inputs: KIS `trht_yn` / `tr_stop_yn` / `temp_stop_yn`, Toss `krxTradingSuspended` / `nxtTradingSuspended`, Meritz `tmpr_susp_yn`, LS text `info3`; Kiwoom and DB have none on REST. |
| market-data spec L250–251: verify NXT/SOR rules; "explicit KRX-only initial support is the safe option" | Consistent. Per-venue halt or eligibility exists at KIS (`nxt_tr_stop_yn`), Kiwoom (`nxtEnable`), LS (`nxt_chk`) and Toss (`nxtTradingSuspended`); no broker documents per-venue limits or ticks. |
| [capability inventory](capability-inventory-2026-11-05.md) row 6 (L34) and notes L166, L172, L179 | **Confirmed** for all six: KIS `CTCA0903R` (same blob `24c2c33c…`); Kiwoom and LS REST not found (WS `0s` / `JIF` only for phase); DB not found; Toss `market-calendar/KR` (prev/today/next, KRX+NXT, KST); Meritz `market-days` + `market-hours`. **Refinement:** LS chart summaries carry session times (§4.5). Not in its scope but found here: KIS `inquire-vi-status`, Kiwoom `ka10054`, Toss `/price-limits` and `/warnings`. |
| capability inventory L178: Toss "numeric quotas are not published (only header examples)" | **Differs:** T2 L246–250 publishes per-group limits (e.g. `MARKET_INFO` "초당 최대 3회", `MARKET_DATA` "초당 최대 15회"), while T2 L238 says they may change without notice (§6.4, §6.5). Not changed here. |
| capability inventory L151: `market_time` is 국내선물 영업일조회 and was not used | **Confirmed** (§2.5); also the path / title contradiction (§2.8 item 6). |
| [order-book evidence](order-book-evidence-2026-11-05.md) and its synthetic fixture `tests/fixtures/order_book/kis-fhkst01010200-synthetic.json` L77, L92 (`"new_mkop_cls_code": "00"`, `"vi_cls_code": "N"`) | Those values are **invented** (fixture README L3–4) and decoders ignore them. They are not evidence of a code list; none is documented (§2.5, §2.7). |
| Symbol-master evidence (branch `claude/issue-17-symbol-master-evidence` @ `b127724ee73fac239d987a2fa2a5b889c5f92bfb`, not merged): Kiwoom `state` / `auditInfo` / `orderWarning` / `nxtEnable`; KIS master file has `trht_yn`, `mang_issu_yn`, `mrkt_alrm_cls_code` with a code list; LS t9945 `nxt_chk` | Kiwoom and LS text **identical** (§3.7, §4.7). For KIS, the REST `search-stock-info` route has NXT flags (`nxt_tr_stop_yn`, `cptt_trad_tr_psbl_yn`, §2.7) that the master file lacks. |
| [Candle evidence](candle-evidence-2026-11-05.md) L207, L377: "Holidays / suspended days: not documented" for KIS and Kiwoom candles; L346–350: Kiwoom signed prices read as direction markers (inference) | Consistent; the KIS holiday route exists but candle routes do not reference it. The same sign reading applies to `lst_pric` (§3.4, inference). Meritz's change of the `J`/`NJ` daily close after 2026-09-14 (§7.8 item 4) also affects candles. |
| [Trade evidence](trade-evidence-2026-11-05.md) L1418–1427 (G-V3): session coverage undocumented; KIS after-hours trades on a separate route; L355: Kiwoom `pri_*_bid_unit` read as best quotes | Consistent (§2.5, §3.3). |

**Ticker-model implication across the six brokers (description only; the
maintainer decides):**

- An upper / lower price limit is the only market-operations value that
  all six brokers return per symbol. Its encodings differ: signed strings,
  empty strings, zeros, `null` or plain numbers. Its venue and trading-day
  scope are undocumented everywhere.
- 기준가 is per symbol at five brokers and is not `previous_close` under
  the current spec.
- Tick size, the calendar, session phase and status are either absent,
  undocumented, or delivered by separate routes with incompatible shapes.
- **Inference:** these facts fit the current `Ticker` best if it stays
  unchanged. A future limit pair would have to be optional, keep "unknown"
  separate from "no limit", and carry no venue claim. Calendar, session,
  tick and status data would sit outside `Ticker` if modelled at all. This
  audit proposes no model change.

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any calendar, tick-size, price-limit or
status model, decoder or request plan is written. Broker tags are in
brackets.

### 10.1 Model scope

- **G-M1:** `Ticker` has no limit, 기준가, tick, session or status field
  (§9). Whether to add typed optional fields, a separate value type, or
  nothing is a maintainer decision; this audit does not propose one.
- **G-M2:** no public dict/JSON status surface. Raw status codes may only
  be exposed in a typed, broker-qualified form once their encodings are
  documented.
- **G-M3:** never map fields across or within brokers by their Korean name
  ("장구분", "장운영구분", "기준가"; §4.8 item 1, §8.2 items 3 and 6).

### 10.2 Calendar

- **G-C1 [KIS]:** do not map `opnd_yn`, `tr_day_yn` or `bzdy_yn` to
  "exchange open" until their meanings, value encoding and venue are
  documented or verified (§2.6).
- **G-C2 [KIS]:** respect "가급적 1일 1회 호출" (K1 L36–37): cache, no
  per-request calls, no automatic retry loop.
- **G-C3 [Kiwoom] [LS] [DB]:** no REST calendar; report the capability as
  unsupported. Do not infer trading days from empty responses, candles,
  LS `t0167`, LS chart `nday`, or DB `M100` / `2611` messages.
- **G-C4 [Toss]:** the calendar covers only the previous, current and next
  business day; `integrated: null` means a holiday, and `today.date` can
  itself be a holiday. The supported `date` range (400 `unsupported-date`)
  is undocumented.
- **G-C5 [Meritz]:** `market-days` has no holiday flag and no date input;
  comparing `tday_bsdy` with the KST date is an unverified inference.
- **G-C6:** do not hard-code an exchange holiday list from any source in
  this file; none is broker evidence.

### 10.3 Sessions

- **G-S1:** session hours from docstrings (KIS K19, K20), WebSocket code
  lists (Kiwoom `0s`), chart examples (LS) or order-route prose (DB) are
  not contracts; do not ship them as constants. The KRX after-hours
  window is contradictory across publishers (§8.2 item 1).
- **G-S2 [KIS] [Meritz]:** phase codes without code lists
  (`new_mkop_cls_code`, `antc_mkop_cls_code`, `mkop_cls_code`,
  `nw_mkop_cls_code`, `shrn_mkop_cls_code`); do not interpret them.
  [Meritz] "000" is explicitly **not** a market-closed signal.
- **G-S3 [LS]:** `ho_status` / `nxt_ho_status` have no code list; do not
  decode them.
- **G-S4 [DB]:** the NXT acceptance windows overlap (종가매매 15:00~16:00
  inside 메인마켓 and 애프터마켓); boundaries and time zone are not stated.
- **G-S5 [Toss]:** times are the KRX+NXT union; never label them as KRX or
  NXT hours.
- **G-S6 [Meritz]:** market-hours times are 9-digit strings described as
  "HHMMSS"; the extra digits are undocumented. No NXT market code exists.
- **G-S7:** NXT session hours per venue are documented by no broker; any
  NXT scope stays unsupported (market-data spec L250–251).

### 10.4 Tick size

- **G-T1:** no broker publishes a tick table as a contract. Do not round or
  validate order prices from the client tables (KIS K26, K27; Meritz M11)
  without a maintainer decision and an authoritative source.
- **G-T2:** no automatic price adjustment on the order path; the KIS client
  floors prices (K27 L120–123), which silently changes order intent.
- **G-T3 [Meritz]:** `aspr_unit` is the documented candidate; verify it,
  including `J` / `NJ` / `TJ` differences and zero on unknown symbols,
  before use. [KIS] `aspr_unit` has a label only.
- **G-T4 [Toss]:** the tick is only observable through a rejected order;
  do not design a tick probe (it would need order authorization). Match on
  `data.tickSize`, not on the error code string (§6.8 item 1).
- **G-T5 [DB]:** code `2706` is reactive evidence only.

### 10.5 Price limits

- **G-L1 [Kiwoom]:** `upl_pric` / `lst_pric` are signed strings; reject or
  map the sign explicitly, never `abs()`.
- **G-L2 [Kiwoom]:** do not use the `ka10001` example as a fixture (§3.4).
- **G-L3:** 기준가 ≠ 전일종가 ≠ `previous_close` (§9).
- **G-L4 [KIS]:** regular and 시간외 단일가 limits are separate columns;
  never merge them. [Meritz] after-hours `ovtm_untp_mxpr` / `llam` must
  not be used ("가격 범위 판단에 쓰지 마십시오").
- **G-L5 [DB]:** index rows return `""` limits; never read `""` as 0.
- **G-L6 [Meritz]:** `mxpr` / `llam` / `sdpr` = 0 can mean an unknown
  symbol answered with a success code; treat 0 or empty as unknown, never
  as "no limit". Success codes vary by route (`"0000"`, `"5766"`, …) and
  the quote routes' `rsp_cd` may arrive corrupted (§7.8 item 7).
- **G-L7 [Toss]:** `null` limits mean "no price limit" only for markets
  without limits (US); behaviour before the open, after hours and on
  holidays is undocumented.
- **G-L8:** venue: KRX first; limits for NXT, integrated or SOR requests
  stay unsupported until per-venue behaviour is documented.
- **G-L9:** the ±30 % ratios computed from examples (Kiwoom, LS, DB) are
  example arithmetic, not a rule.

### 10.6 Status

- **G-X1:** no common status enum. KIS and Meritz flags lack encodings;
  Kiwoom's `orderWarning` list is incomplete; LS fields are display text;
  Toss has an enum but no 관리종목 or 투자주의. Do not map an absent flag
  to "normal".
- **G-X2 [KIS]:** three halt-like flags (`temp_stop_yn`, `trht_yn`,
  `tr_stop_yn`) plus `nxt_tr_stop_yn`; do not merge them without evidence.
- **G-X3 [KIS]:** `inquire-vi-status` has no venue selector; do not label
  its rows KRX or NXT.
- **G-X4 [Kiwoom]:** VI rows carry HHmmss times without a date; require a
  verified trading date (market-data spec §5).
- **G-X5 [LS]:** the t1422 / t1427 `jc_num` description says "대상제외값
  (설정시 저장됨)". **Inference:** the server may persist the filter. This
  server-side state needs maintainer review before any use.
- **G-X6 [Toss]:** VI is date-granular; warnings are batch-updated except
  VI; tolerate unknown `warningType` values. Two 정리매매 sources may
  disagree.
- **G-X7 [Meritz]:** `tmpr_susp_yn = "N"` can be a constant on a missed
  lookup (M10 L65); `issu_stat_cls_code` has no code list.
- **G-X8 [DB]:** status exists only as WebSocket field names; not usable
  for REST snapshots.

### 10.7 Environment, requests and retries

- **G-E1:** real/paper availability: KIS undocumented; Kiwoom mock domain
  listed; LS no paper REST origin documented; DB ⭕ in the SDK matrix with
  one origin; Toss and Meritz none. No silent LIVE/PAPER fallback; the
  KIS `C…`→`V…` paper rewrite (K22 L453–455) must not be assumed to name a
  real paper TR.
- **G-E2:** every route here needs authentication; [Meritz] also a
  `mac_address` header, which needs a sanctioned source (no MAC discovery,
  no MAC values in Git or logs). Any real request needs a separate
  explicit authorization (AGENTS.md); none was made.
- **G-E3 [LS]:** the FAQ advice to retry an order message "일정 간격을 두고"
  is recorded, **not adopted**. [DB] the SDK's automatic back-off is not
  adopted. No order retry without a proven duplicate-order safeguard.

## 11. Not verified

- Any live or paper response for any route above. No broker API request
  was sent.
- Entitlements and real/paper parity for all six brokers.
- Which KRX after-hours window is current (§8.2 item 1).
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
- LS:
  - NXT and `U` limit semantics; when `recprice` differs from `jnilclose`;
  - meaning of the chart session times and `ho_status`;
  - code lists for the t1102 status text fields;
  - venue coverage of t1404 / t1405; `jc_num` persistence.
- DB:
  - `NJ` / `UJ` limit semantics; the falling-price convention on `PRICE`;
  - KRX session hours (the linked customer-centre page was not
    retrieved); NXT window boundaries and time zone;
  - the `S00` WebSocket status flags.
- Toss:
  - `price-limits` outside regular hours and on holidays;
  - the supported calendar `date` range and `today.date` on holidays;
  - VI latency and halt-flag freshness.
- Meritz:
  - `issu_stat_cls_code` and `*_mkop_cls_code` meanings; `oder_stop_yn`
    values;
  - `tday_bsdy` on holidays; the 9-digit time format;
  - whether `aspr_unit` / `mxpr` / `llam` differ between `J`, `NJ` and
    `TJ`;
  - the tick-rejection `rsp_cd` (`8337` appears only in client prose).
- Exchange rules (tick tables, limit widths, session hours, holidays) were
  deliberately not consulted; nothing here states them.
