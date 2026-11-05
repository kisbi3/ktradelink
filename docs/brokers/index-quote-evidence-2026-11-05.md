# Six-broker index and sector quote (지수·업종 시세) evidence — 2026-11-05

- **Scope:** domestic REST routes that return the current value or candles
  of KOSPI, KOSDAQ, KOSPI200 and sector (업종) indices, plus the routes
  or files that list index codes. Brokers: KIS, Kiwoom REST, LS, DB, Toss
  and Meritz. WebSocket index feeds are **named only**. Constituent lists,
  expected (예상) indices, investor flows and program trading are named
  only where they share a code list. The Shinhan comparison stays
  separate.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No KTradeLink index decoder, request plan, index
  symbol rule or public index method exists, and this file does not
  authorize one.
- **No broker API request was sent.** No token, credential, account, MAC
  value or order was used. Only public Git repositories, public
  documentation pages and publisher JSON documentation endpoints were
  fetched. No index master *data file* was downloaded; the KIS
  `idxcode.mst` name and layout come from publisher code and a header
  file only (§2.3).
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS: files of a fixed commit, fetched 07:56:05–07:56:09 and
    08:03:43–08:03:44 from `raw.githubusercontent.com` (§2.1).
  - Kiwoom: files of a fixed commit, fetched 07:57:47–07:57:51 (§3.1).
  - LS portal guide JSON, catalog page and TR detail endpoints:
    07:59:52–08:01:29 (§4.1).
  - DB, Toss, Meritz: **pending** (§5–§7 are written in parallel and will
    be merged into this file).
- **Re-hash:** every Git blob SHA in §2.1 and §3.1 was computed from the
  retrieved bytes and matched the `git ls-tree` entry of the pinned
  commit. Every sha256 prefix in §4.1 identifies the retrieved copy.
- **Pin formats:**
  - Git blob SHAs are `sha1("blob <len>\0" + bytes)` of the retrieved
    bytes, i.e. what `git hash-object` and `git ls-tree` print.
  - Line numbers are written "(K3 L63–66)": source K3, lines 63–66 of that
    blob or copy.
  - Web pages have no immutable revision. Their sha256 prefix identifies
    only the copy retrieved at the stated time.
  - Raw copies were kept outside the repository. Sample tokens, app keys,
    account values, MAC values and staff contact data in publisher
    material are deliberately not copied.
- **Evidence levels:**
  - `field table`: a publisher field or spec table.
  - `publisher example`: a sample request/response or sample code.
  - `publisher client code`: SDK, helper or backtester behaviour. It shows
    how the publisher calls the route; it is **not** a contract.
  - `legacy publisher example`: sample code or Postman items under a
    publisher repository's `legacy/` directory. Lower weight than the
    current examples.
  - `publisher repo note`: non-code text in a publisher repository
    (including C header comments).
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- Sample values in publisher examples are illustrative. They are **not**
  authorized response fixtures. Several examples below are internally
  inconsistent (§3.7), which is itself recorded as evidence.

## 1. Broker × concern summary

Cell format: short verdict — evidence. `F` field table, `E` publisher
example, `L` legacy publisher example, `C` publisher client code, `N`
publisher repo note, `—` not found. DB, Toss and Meritz cells are
**pending** (§5–§7).

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Current value route | `FHPUP02100000` GET `…/quotations/inquire-index-price` 국내업종 현재지수 — E | `ka20001` 업종현재가요청 POST `/api/dostk/sect`; all-sector list `ka20003` — F+E | `t1511` 업종현재가 POST `/indtp/market-data`, TPS 10 — F+E | pending | pending | pending |
| Daily/weekly/monthly candles | `FHKUP03500100` `…/inquire-daily-indexchartprice` D/W/M/Y; `FHPUP02120000` `…/inquire-index-daily-price` D/W/M — E; `FHKUP03500100` also L | `ka20006`/`ka20007`/`ka20008`/`ka20019` 일/주/월/년봉 POST `/api/dostk/chart`; `ka20009` daily list — F+E | `t8429` 업종차트(일주월) POST `/indtp/chart`; `t1514` 업종기간별추이 (일/주/월) — F+E | pending | pending | pending |
| Intraday candles / series | `FHKUP03500200` `…/inquire-time-indexchartprice` (`FID_INPUT_HOUR_1` seconds) — E+L; value series `FHPUP02110100` (초), `FHPUP02110200` (분) — E | `ka20005` 분봉 (1–60분), `ka20004` 틱 (1–30틱) — F+E | `t8409` N분 (`0:30초`, n분), `t8408` 틱/n틱 — F+E | pending | pending | pending |
| Index code format | 4 chars, `FID_COND_MRKT_DIV_CODE` `U`; "코스피(0001), 코스닥(1001), 코스피200(2001)" — E | 3 chars `inds_cd` + `mrkt_tp` "0:코스피, 1:코스닥, 2:코스피200"; "001:종합(KOSPI) … 101:종합(KOSDAQ), 201:KOSPI200 …" — F | 3 chars `upcode`/`shcode`; "코스피@001 코스피200@101 KRX100@501 코스닥@301" — F | pending | pending | pending |
| Code list route / file | file `idxcode.mst.zip` (name + layout only) — C+N; no REST list found | `ka10101` 업종코드 리스트 POST `/api/dostk/stkinfo` — F+E | `t8424` 전체업종 POST `/indtp/market-data` — F+E | pending | pending | pending |
| Value scale / type | column names only; no type or decimals documented | current: decimal string "단위: 지수, 부호가 포함된 숫자"; charts: "소수점 제거 된 100배 값" — F | `Number(10.2)`; examples are JSON strings `"2610.62"` — F+E | pending | pending | pending |
| As-of time on current value | **none** in the column map — E | **none** at top level; `inds_cur_prc_tm[].tm_n` "HHmmss", no date — F | **none**; only `opentime`/`hightime`/`lowtime` String(6) — F | pending | pending | pending |
| Volume / value units | not documented | current "단위: 1000주", "단위: 백만원"; charts "단위: 1주" — F | not documented — F | pending | pending | pending |
| Venue / NXT | no venue parameter; `U` only — E | no venue parameter on index routes; `stex_tp` only on constituent route `ka20002` — F | no `exchgubun` on any 업종 TR — F | pending | pending | pending |
| Real / paper | legacy Postman marks `FHKUP0350*` "[실전투자/모의투자]", `FHPUP02110100` "[실전투자]" — L; others not stated | both domains in meta; PRD and MOCK Postman items; error `8104` possible — F | REST server list has no simulation URL — F | pending | pending | pending |
| WebSocket feed (name only) | `H0UPCNT0` 국내지수 실시간체결 — E | `0J` 업종지수 (also `0U` 업종등락) — F | `IJ_` 지수 (also `YJ_` 예상지수) — F | pending | pending | pending |

## 2. KIS (Korea Investment & Securities)

### 2.1 Pinned sources

All sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362).
The full SHA is `3a9be59a3ed8745720dc3aa9d584bdf3b7830362` and the commit is
dated 2026-10-28T00:26:05+09:00 (the same pin as the trade and candle
audits). Paths are relative to the repository root; `…/` stands for
`examples_llm/domestic_stock/`. Each `chk_*.py` file is the sibling
column-map script of the route file.

| # | Path | Pin (Git blob) | Used for |
| --- | --- | --- | --- |
| K1 | [`…/inquire_index_price/inquire_index_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_index_price/inquire_index_price.py) | `8301317180bf88a062b37b6d7b5c18323e3b90e5` | 국내업종 현재지수: path, TR id, params, code examples (L21–25, L41–42, L73–79, L101–108) |
| K2 | `…/inquire_index_price/chk_inquire_index_price.py` | `7966c02d430d657a4d3bb323dd69378ddf3c1ad1` | Its column map (L24–61) |
| K3 | [`…/inquire_index_daily_price/inquire_index_daily_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_index_daily_price/inquire_index_daily_price.py) | `c9fdebb9980531a5a41c3f46bada4867168a0395` | 국내업종 일자별지수 (L22–26, L45–48, L86–92, L118–126) |
| K4 | `…/inquire_index_daily_price/chk_inquire_index_daily_price.py` | `ff819bd46f5758840aea67dbcab9bd27c365ebf5` | Its column map (L25–58) |
| K5 | [`…/inquire_daily_indexchartprice/inquire_daily_indexchartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_daily_indexchartprice/inquire_daily_indexchartprice.py) | `0e8856c13f790b5112d0f8f1c8e53c15cb0aa0aa` | 국내주식업종기간별시세(일/주/월/년) (L1, L24–28, L36, L49–54, L118–129, L162) |
| K6 | `…/inquire_daily_indexchartprice/chk_inquire_daily_indexchartprice.py` | `8bd568e077178ac0958bbe04f607de0250bf6b41` | Its column map (L25–49) |
| K7 | [`…/inquire_time_indexchartprice/inquire_time_indexchartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_indexchartprice/inquire_time_indexchartprice.py) | `7327b519ec8b413852b0bd22e57caee49da18f4e` | 업종 분봉조회 (L24–28, L36–38, L48–52, L103–110, L160–169) |
| K8 | `…/inquire_time_indexchartprice/chk_inquire_time_indexchartprice.py` | `1d553d850455bdd7f08ef9d7dac16d9d8f523b95` | Its column map (L25–51; `Output1` marker L26, `Output2` marker L43) |
| K9 | `…/inquire_index_tickprice/inquire_index_tickprice.py`; `chk_…` | `e8fba43abe12a511428fc707d1a66f6615378d6f`; `cba60485b425086ffa28bbe3d82bf3947dd1410b` | 국내업종 시간별지수(초) (L21–25, L41–42, L70); columns (chk L25–32) |
| K10 | `…/inquire_index_timeprice/inquire_index_timeprice.py`; `chk_…` | `f43eb5d22d476b0ef1b4c363c875763ad90341b5`; `0b6593041f10d70664fc7e2a1569acde42471bb1` | 국내업종 시간별지수(분) (L21–25, L42–44, L76); columns (chk L25–32) |
| K11 | `…/inquire_index_category_price/inquire_index_category_price.py` | `41c2355c942b0cf31d33b1d0c8d9541f7d92775e` | 국내업종 구분별전체시세 (L21–25, L45–49, L100, L145); named only |
| K12 | `…/index_ccnl/index_ccnl.py` | `44cb428c79ebfedcef0fb09bdd31d272999956c9` | WebSocket name only (L17, L51) |
| K13 | [`stocks_info/sector_code.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/stocks_info/sector_code.py) | `3c34fce92f7fd913c529e3f8adee5f00953ced78` | `idxcode.mst` name and parse offsets (L11–12, L19–26) |
| K14 | [`stocks_info/업종코드정보.h`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/stocks_info/%EC%97%85%EC%A2%85%EC%BD%94%EB%93%9C%EC%A0%95%EB%B3%B4.h) | `508b2d6567951ab197050a47cdc8d94350bdcb89` | `IDX_CODE` record layout (L1–9) |
| K15 | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) | `0e722d6f3253033efe3cf2b99845397b2b329655` | Transport: origins (L152, L154), paper TR remap (L453–455), `tr_cont` header (L459), GET (L476), `rt_cd` (L353) |
| K16 | [`MCP/Kis Trading MCP/configs/domestic_stock.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/configs/domestic_stock.json) | `e82a0829ef519c64dfecb3e966ed217b4fcd3805` | Publisher registry: L2166–2186, L2257–2304, L2343+, L2515+ |
| K17 | `backtester/kis_backtest/providers/kis/data.py` | `28bf9aca834e4abd7c0b4b63ab0b9be61678de13` | Publisher client code for index daily history (L454–551) |
| K18 | `legacy/Sample01/kis_domstk.py` | `0090f06c540fadc0b87a1e9515ab4c098e3aa9c2` | **Legacy** `U` comments on a stock minute route (L1231–1237) |
| K19 | [`legacy/postman/실전계좌_POSTMAN_샘플코드_v2.6.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/postman/%EC%8B%A4%EC%A0%84%EA%B3%84%EC%A2%8C_POSTMAN_%EC%83%98%ED%94%8C%EC%BD%94%EB%93%9C_v2.6.json) | `a73d6bfab94ddfbf94af8db8de4c9e50ef040e58` | **Legacy** real-account items (L3934–3981, L4519, L7205–7252, L7375–7463, L7582–7642, L7670–7730, L7836) |
| K20 | [`legacy/postman/모의계좌_POSTMAN_샘플코드_v1.6.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/postman/%EB%AA%A8%EC%9D%98%EA%B3%84%EC%A2%8C_POSTMAN_%EC%83%98%ED%94%8C%EC%BD%94%EB%93%9C_v1.6.json) | `03833e4af7258d1d85b76f298af3928be2748ea0` | **Legacy** paper-account item (L1041–1108) |

**Missing evidence:**

- No KIS field table for any index route: no JSON types, lengths,
  decimals, units or sign-code lists.
- No sample response body (current examples print DataFrames; the legacy
  Postman items have no saved responses).
- The KIS developer-portal specification and the portal FAQ that K1 L42
  points to ("포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)") were
  **not** retrieved.
- No REST route that lists index codes was found; only the `idxcode.mst`
  file (§2.3).
- All response statements below are limited to column *names* and their
  Korean labels.

### 2.2 Routes

All routes are `GET` with query parameters: K15 L476 calls
`requests.get(url, headers=headers, params=params)` because no index route
sets `postFlag`. Origins are the K15 L152 and L154 comments:
`https://openapi.koreainvestment.com:9443` (실전) and
`https://openapivts.koreainvestment.com:29443` (모의). `…` stands for
`/uapi/domestic-stock/v1/quotations`.

| Route (title verbatim) | Method + path | TR id | Real / paper | Current / candles / list | Evidence |
| --- | --- | --- | --- | --- | --- |
| "[국내주식] 업종/기타 > 국내업종 현재지수 [v1_국내주식-063]" (K1 L21) | GET `…/inquire-index-price` | `FHPUP02100000` (K1 L73) | not stated; no legacy item | current value (one object, `output`) | publisher example |
| "국내업종 일자별지수[v1_국내주식-065]" (K3 L22) | GET `…/inquire-index-daily-price` | `FHPUP02120000` (K3 L86) | not stated | `output1` summary + `output2` rows; period "D:일별 , W:주별, M:월별" (K3 L45) | publisher example |
| "국내주식업종기간별시세(일_주_월_년)[v1_국내주식-021]" (K5 L24) | GET `…/inquire-daily-indexchartprice` | `FHKUP03500100` (K5 L120) | K5: `env_dv` "real"/"demo" both use the same TR id (L118–120); K19 L7247 and K20 L1084: "[실전투자/모의투자]" | candles "D:일봉 W:주봉, M:월봉, Y:년봉" (K5 L53) | publisher example + legacy |
| "업종 분봉조회[v1_국내주식-045]" (K7 L24) | GET `…/inquire-time-indexchartprice` | `FHKUP03500200` (K7 L103) | K19 L7417: "[실전투자/모의투자]" | intraday candles (`output2` rows) | publisher example + legacy |
| "국내업종 시간별지수(초)[국내주식-064]" (K9 L21) | GET `…/inquire-index-tickprice` | `FHPUP02110100` (K9 L70) | K19 L7628: "[실전투자]" | value series, **not OHLC** | publisher example + legacy |
| "국내업종 시간별지수(분)[국내주식-119]" (K10 L21) | GET `…/inquire-index-timeprice` | `FHPUP02110200` (K10 L76) | K19 L7715–7716: value `FHPUP02110200`, description "[실전투자/모의투자]\nFHKST01010100 : 주식현재가 시세" (mismatch, §2.7) | value series, **not OHLC** | publisher example + legacy |
| "국내업종 구분별전체시세[v1_국내주식-066]" (K11 L21) | GET `…/inquire-index-category-price` | `FHPUP02140000` (K11 L100) | not stated | all sectors of one market (named only) | publisher example |

Registry (K16) lists `inquire_index_price` (L2166),
`inquire_daily_indexchartprice` (L2257), `inquire_time_indexchartprice`
(L2343) and `inquire_index_daily_price` (L2515), all under "[국내주식] 업종/기타". K9–K11 are not registered.

Paper environment: K15 L453–455 rewrites a TR id to `V…` only when it
starts with `T`, `J` or `C`. Every index TR id here starts with `F`, so the
publisher client sends the same id to the paper origin. **Inference:** the
helper therefore neither proves nor rules out paper support.

WebSocket (name only): "[국내주식] 실시간시세 > 국내지수 실시간체결
[실시간-026]", `tr_id = "H0UPCNT0"` (K12 L17, L51).

### 2.3 Index identifiers

- **Market division:** every index route takes `FID_COND_MRKT_DIV_CODE`
  with "업종(U)" (K1 L41), "시장구분코드 (업종 U)" (K3 L46), "업종 : U"
  (K5 L49).
- **Index code** (`FID_INPUT_ISCD`), four characters in every example:
  - K1 L42, K3 L47, K11 L46: "코스피(0001), 코스닥(1001), 코스피200(2001)
    ... 포탈 (FAQ : 종목정보 다운로드(국내) - 업종코드 참조)".
  - K5 L50: "0001 : 종합 0002 : 대형주 ... 포탈 (FAQ : 종목정보 다운로드(국내)
    - 업종코드 참조)"; K7 L50: "'0001' 종합, '0002' 대형주".
  - K9 L41, K10 L43: "0001:거래소, 1001:코스닥, 2001:코스피200, 3003:KSQ150".
  - Legacy (other routes, context only): K19 L4519 "'0000':전체, '0001':코스피,
    '1001':코스닥, '2001':코스피200, '4001':KRX100"; K19 L7836 "'0001':코스피,
    '1001':코스닥, '2001':코스피200, '3003':코스닥150, '4001':KRX100".
  - **KRX100:** only the legacy `4001` above. No current example names it.
- **K11 market codes** (category route, context): `FID_MRKT_CLS_CODE`
  "시장구분코드(K:거래소, Q:코스닥, K2:코스피200)" (K11 L48).
- **Index master file (name and layout only; not downloaded):**
  - K13 L12 downloads `idxcode.mst.zip` from the publisher's master-file
    host and reads `idxcode.mst` as `cp949` (L19–23). K13 L11 disables TLS
    verification (`ssl._create_unverified_context`); this is **not** a
    safe implementation pattern.
  - K13 L25: `tcode = row[1:5]` "업종코드 4자리 (맨 앞 1자리 제거)"; L26:
    `tname = row[3:43].rstrip()` "업종명".
  - K14 L4–9: `IDX_CODE` = `idx_div[1]` "시장구분값 ex) 00002(대형주)일 경우
    맨 앞자리 0", `idx_code[4]` "업종코드 ex) 00002(대형주)일 경우 맨 앞자리를
    제외한 0002", `idx_name[40]` "업종명".
  - The two disagree on the name offset (§2.7).
  - No REST code-list route was found in the pinned files.

### 2.4 Current value response

`FHPUP02100000` returns one `output` object (K1 L86–90). Column names and
labels (K2 L24–61), grouped:

| Concern | Columns (label verbatim) |
| --- | --- |
| Value | `bstp_nmix_prpr` "업종 지수 현재가" |
| Change | `bstp_nmix_prdy_vrss` "업종 지수 전일 대비"; `prdy_vrss_sign` "전일 대비 부호"; `bstp_nmix_prdy_ctrt` "업종 지수 전일 대비율" |
| OHL | `bstp_nmix_oprc` "업종 지수 시가2", `bstp_nmix_hgpr` "업종 지수 최고가", `bstp_nmix_lwpr` "업종 지수 최저가" (+ per-field sign and rate columns) |
| Previous close | **no column**; `prdy_clpr_vrss_lwpr` "전일 종가 대비 최저가" only |
| Volume / value | `acml_vol` "누적 거래량", `prdy_vol` "전일 거래량", `acml_tr_pbmn` "누적 거래 대금", `prdy_tr_pbmn` "전일 거래 대금" |
| Breadth | `ascn_issu_cnt` "상승 종목 수", `uplm_issu_cnt` "상한 종목 수", `stnr_issu_cnt` "보합 종목 수", `down_issu_cnt` "하락 종목 수", `lslm_issu_cnt` "하한 종목 수" |
| Year range | `dryy_bstp_nmix_hgpr`, `dryy_bstp_nmix_hgpr_date`, `dryy_bstp_nmix_lwpr`, `dryy_bstp_nmix_lwpr_date` |
| Book totals | `total_askp_rsqn`, `total_bidp_rsqn`, `seln_rsqn_rate`, `shnu_rsqn_rate` "매수2 잔량 비율", `ntby_rsqn` |
| Time | **none** |

- Types, decimals, units and the `prdy_vrss_sign` code list: **not
  documented** (K2 has `NUMERIC_COLUMNS = []`, L63).
- Envelope: K15 L353 treats `rt_cd == "0"` as success. Index-specific
  error codes: not found.
- Paging: K1 L101–108 re-calls on response header `tr_cont == "M"` with
  `"N"` and the same params. **Inference:** a single object is not
  expected to page; the generic helper does this for every route.

### 2.5 Index candles

| Concern | `FHKUP03500100` daily+ (K5, K6) | `FHPUP02120000` 일자별 (K3, K4) | `FHKUP03500200` intraday (K7, K8) |
| --- | --- | --- | --- |
| Intervals | "D:일봉 W:주봉, M:월봉, Y:년봉" (K5 L53) | "D:일별 , W:주별, M:월별" (K3 L45) | `FID_INPUT_HOUR_1` "(예: '30', '60', '600', '3600')" (K7 L51); legacy "입력 시간(초) ex) 30: 30초, 60: 1분, 600:10분, 3600:1시간" (K19 L7453) |
| Range input | `FID_INPUT_DATE_1` "조회 시작일자", `FID_INPUT_DATE_2` "조회 종료일자" (K5 L51–52) | `FID_INPUT_DATE_1` "입력 날짜(ex. 20240223)" (K3 L48) | none; `FID_PW_DATA_INCU_YN` "(예: 'Y' 과거, 'N' 당일)" (K7 L52) |
| Session filter | none | none | `FID_ETC_CLS_CODE` "(예: '0' 기본, '1' 장마감, 시간외 제외)" (K7 L49) |
| Row date/time | `stck_bsop_date` "영업 일자" (K6 L42) | `stck_bsop_date` "주식 영업 일자" (K4 L46) | `stck_bsop_date` + `stck_cntg_hour` "주식 체결 시간" (K8 L44–45) |
| OHLC | `bstp_nmix_oprc` "업종 지수 시가", `…_hgpr`, `…_lwpr`, `bstp_nmix_prpr` "업종 지수 현재가" | same (+ change columns) | same, `oprc` labelled "시가2" |
| Volume | `acml_vol`, `acml_tr_pbmn` | `acml_vol`, `acml_tr_pbmn` | `cntg_vol` "체결 거래량", `acml_tr_pbmn` |
| Other | `mod_yn` "변경 여부" (K6 L49) | `acml_vol_rlim`, `invt_new_psdg`, `d20_dsrt` | `output1` has `futs_prdy_*` "선물 전일 …" labels (K8 L40–42) |

- **Adjustment:** no 수정주가 parameter on any index route. `mod_yn` is
  labelled only "변경 여부". **Inference:** adjustment is not applicable
  to an index, but no KIS text says so.
- **Row order and depth:** not documented. K17 (publisher client code)
  says its result is "오래된 순 정렬" only after it sorts (L549–550), pages
  by moving `FID_INPUT_DATE_2` to the last row's date minus one day
  (L539–546) and stops after "최대 10 페이지" (L486). **Inference:** K17
  expects `output2` newest first; not a contract.
- **Page size:** not documented for any index route.
- **Continuation:** K3, K5, K7 re-call on `tr_cont` "M" or "F" with the
  **same** parameters (K5 L162; K3 L118–126; K7 L160–169); no body cursor
  is shown.
- **Value series (not candles):** K9 columns `stck_cntg_hour`,
  `bstp_nmix_prpr`, `cntg_vol`, …; K10 `bsop_hour` "영업 시간", same
  values, `fid_input_hour_1` "초단위, 60(1분), 300(5분), 600(10분)" (K10
  L42). No open/high/low columns.

### 2.6 Venue / calculation scope

- No index route has a venue parameter or a venue column. The equity
  venue codes `J`/`NX`/`UN` do not appear in K1–K11.
- No KIS text states who calculates the index or whether NXT trades are
  included. **Not documented.**
- `FID_ETC_CLS_CODE` "'1' 장마감, 시간외 제외" (K7 L49) is the only
  session-related input; its exact effect is not documented.

### 2.7 Contradictions and gaps

1. **Master layout vs parser.** K14 places `idx_name` after a 1-byte
   `idx_div` and a 4-byte `idx_code` (offset 5). K13 reads the code as
   `row[1:5]` (consistent) but the name as `row[3:43]` (offset 3), which
   would overlap the code. Neither is a field table; no sample row.
2. **`env_dv` default.** K5 L36 defaults `env_dv="real"`; the registry
   K16 L2303–2304 says `"default_value": "demo"` "기본값: 'demo'". Both
   map to `FHKUP03500100` (K5 L118–120).
3. **`K2` label.** K11 L48 says "K2:코스피200"; K11 L49 continues
   "시장구분코드(K2:코스닥) 0:전업종".
4. **Minute interval values.** Current K7 L51 and legacy K19 L7453 accept
   second counts `30`/`60`/`600`/`3600`. Legacy K18 L1231 (stock minute
   route `FHKST03010200` with `U`) says "업종(U)일 경우, 조회간격(초) (60 or
   120 만 입력 가능)". K19 L7428 sends `FID_INPUT_HOUR_1=120` to
   `FHKUP03500200`.
5. **Legacy Postman mismatches.** K19 L3934–3981 "J_주식당일분봉조회(업종)"
   sends TR `FHKST03010200` to `…/inquire-daily-indexchartprice` with
   minute parameters. K19 L7716 describes `FHPUP02110200` as
   "FHKST01010100 : 주식현재가 시세".
6. **Recursive paging bug (client code).** K3 L126, K7 L169 and K11 L145
   pass `"N", dataframe1, dataframe2, …` positionally, but the signatures
   order `dataframe1, dataframe2, tr_cont` (K3 L33–35, K7 L36–38). The
   continuation call therefore sends a DataFrame-or-`None` as `tr_cont`.
   This is publisher example code, not a contract.
7. **Category label.** K5 L1 says "[국내주식] 업종/기타"; K5 L24 says
   "[국내주식] 기본시세".
8. **Gaps:** types, decimals, units, sign codes, row order, page size,
   history depth, behaviour of `FID_PW_DATA_INCU_YN`, paper support of
   `FHPUP02100000`/`FHPUP02120000`, and time zone.

### 2.8 Gates and not-verified items

- G-K1: obtain the KIS portal field tables (types, decimals, units, sign
  codes) for `FHPUP02100000`, `FHKUP03500100` and `FHKUP03500200` before
  any decoder.
- G-K2: decide whether `idxcode.mst` or a documented list is the code
  source; resolve the K13/K14 offset conflict with a sanitized sample.
- G-K3: no as-of time on the current value; a decoder must not invent
  one (§10.4).
- G-K4: confirm row order and paging of `output2` with authorized fixtures;
  the example continuation (§2.7 item 6) must not be copied.
- Not verified: any response, paper support, units, `FID_INPUT_HOUR_1`
  accepted values, `FID_ETC_CLS_CODE` effect, history depth.

## 3. Kiwoom REST

### 3.1 Pinned sources

All sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@c7a3d254`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/c7a3d25449ed4b4238bef378780c41103c67b9e9).
The full SHA is `c7a3d25449ed4b4238bef378780c41103c67b9e9`, dated
2026-09-15T15:12:16+09:00. It names the same tree as the earlier pin
`953e5dbf…`, so blob pins from earlier audits remain valid (see §3.1 of
the trade evidence on branch `claude/issue-17-trade-evidence` for the re-pin
record).

| # | Path | Pin (Git blob) | Used for |
| --- | --- | --- | --- |
| W1 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field tables** and examples: `ka10101` (L28040–28202), `ka20001` (L30033–30455), `ka20002` (L30456–30718, named only), `ka20003` (L30719–30991), `ka20004` (L30992–31214), `ka20005` (L31215–31457), `ka20006` (L31458–31670), `ka20007` (L31671–31883), `ka20008` (L31884–32096), `ka20009` (L32097–32509), `ka20019` (L32510–32722), `0J` (L101802), `0U` (L102165), `error_codes` (L107018; `8104` at L107196–107197) |
| W2 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | PRD items L6205 (`ka10101`), L9941, L10142, L10235, L15104–15600; MOCK items L39742, L43478, L43679, L43772, L48641–49137 |
| W3 | [`…/업종/get_domestic_sector_price.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%97%85%EC%A2%85/get_domestic_sector_price.py) | `bf8efe30b078baa8bb1eaca0111de6337ae60f5e` | `ka20001` example client (L18, L125–126) |
| W4 | [`…/차트/get_domestic_sector_daily_chart.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_sector_daily_chart.py) | `c6cab18c7ff02ea6e076c6f960fea5effe1ac065` | `ka20006` client: `MAX_PAGES = 10` (L20), row key (L28), continuation loop (L132–166) |
| W5 | [`…/차트/get_domestic_sector_minute_chart.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_sector_minute_chart.py) | `eaf00cd04f5a21501e2254af800381100664b85d` | `ka20005` client: row key `inds_min_pole_qry` (L28) |
| W6 | [`…/종목정보/list_domestic_sector_codes.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/list_domestic_sector_codes.py) | `f832c4f0d85b9395c6cb9526409e511834759d4d` | `ka10101` client (L18, L77) |
| W7 | [`kiwoom/core/client.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/client.py) | `52d915c9e2f38f21885efbc428d3b50593a452c9` | `return_code` handling (L84, L104–105), `cont-yn` header (L128) |

`…/` stands for `examples/국내주식/`.

**Missing evidence:**

- No row-count limit, history depth or row-order statement for any chart
  route.
- No time-zone statement.
- Several examples contradict their own field tables (§3.7); no
  consistent sample exists for `ka20005`.

### 3.2 Routes

Common (W1 meta, repeated in W2): `Method` `POST`, `Format` `JSON`,
`Content-Type` `application/json;charset=UTF-8`, "운영 도메인"
`https://api.kiwoom.com`, "모의투자 도메인" `https://mockapi.kiwoom.com`.
Headers `api-id` (required), `authorization` (required), `cont-yn` and
`next-key` (optional) on every route below.

| Route (title verbatim) | Method + path | API id | Real / paper | Current / candles / list | Evidence |
| --- | --- | --- | --- | --- | --- |
| 업종현재가요청: "업종 현재가 정보를 조회합니다." | POST `/api/dostk/sect` | `ka20001` | PRD + MOCK items (W2) | current value + intraday list `inds_cur_prc_tm` | field table + example |
| 전업종지수요청: "전 업종 지수 정보를 조회합니다." | POST `/api/dostk/sect` | `ka20003` | PRD + MOCK | current values of all sectors (`all_inds_idex`) | field table + example |
| 업종현재가일별요청: "업종 현재가 일별 정보를 조회합니다." | POST `/api/dostk/sect` | `ka20009` | PRD + MOCK | current value + daily close list `inds_cur_prc_daly_rept` (no OHL per row) | field table + example |
| 업종틱차트조회요청 | POST `/api/dostk/chart` | `ka20004` | PRD + MOCK | tick candles `inds_tic_chart_qry` | field table + example |
| 업종분봉조회요청 | POST `/api/dostk/chart` | `ka20005` | PRD + MOCK | minute candles `inds_min_pole_qry` | field table; example mismatched (§3.7) |
| 업종일봉조회요청 | POST `/api/dostk/chart` | `ka20006` | PRD + MOCK | daily `inds_dt_pole_qry` | field table + example |
| 업종주봉조회요청 | POST `/api/dostk/chart` | `ka20007` | PRD + MOCK | weekly `inds_stk_pole_qry` | field table + example |
| 업종월봉조회요청 | POST `/api/dostk/chart` | `ka20008` | PRD + MOCK | monthly `inds_mth_pole_qry` | field table + example |
| 업종년봉조회요청 | POST `/api/dostk/chart` | `ka20019` | PRD + MOCK | yearly `inds_yr_pole_qry` | field table + example |
| 업종코드 리스트: "업종 코드 리스트를 조회합니다." | POST `/api/dostk/stkinfo` | `ka10101` | PRD + MOCK | code list | field table + example |
| 업종별주가요청 | POST `/api/dostk/sect` | `ka20002` | PRD + MOCK | constituents (named only) | field table |

- A MOCK Postman item shows the publisher *offers* the route in the mock
  environment. W1 error `8104` "모의투자에서 지원하지 않는 API 입니다."
  (L107196–107197) shows mock support is not guaranteed per API.
- W7 L104: "키움은 업무 오류도 HTTP 200으로 내려보내고 실패 여부는 본문
  return_code에만 담는다." (publisher client code). Examples carry
  `return_code: 0` and `return_msg` "정상적으로 처리되었습니다".
- WebSocket (name only): `0J` "업종지수" and `0U` "업종등락", menu "국내주식
  > 실시간시세", domain `wss://api.kiwoom.com:10000` (W1 L101802,
  L102165).

### 3.3 Index identifiers

- `inds_cd` String(3) Y on `ka20001`/`ka20002`/`ka20004`–`ka20006`/
  `ka20008`/`ka20009`/`ka20019` (e.g. W1 L30106): "001:종합(KOSPI),
  002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200,
  302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고". `ka20007` declares it
  String(8) (§3.7).
- `ka20003` `inds_cd` (W1 L30782): "001:종합(KOSPI), 101:종합(KOSDAQ)".
- `mrkt_tp` String(1) Y on `ka20001`, `ka20002`, `ka20009` (W1 L30096,
  L30519, L32160): "0:코스피, 1:코스닥, 2:코스피200". The chart routes
  take **no** `mrkt_tp`.
- `ka10101` 업종코드 리스트 `mrkt_tp` (W1 L28103): "0:코스피(거래소),1:코스닥,
  2:KOSPI200,4:KOSPI100,7:KRX100(통합지수)". Response `list[]` has
  `marketCode` "시장구분코드", `code` "코드", `name` "업종명", `group` "그룹",
  all `String()` with no length (L28149–28189). Example (`mrkt_tp` `0`):
  11 rows from `{"marketCode": "0", "code": "001", "name": "종합(KOSPI)",
  "group": "1"}` to `"011"` "철강금속" (L28201).
- How `mrkt_tp` and `inds_cd` must agree (e.g. `1` + `101`) is **not
  documented**. No `mrkt_tp` value on `ka20001` corresponds to `ka10101`'s
  `4` or `7` (§3.7).

### 3.4 Current value response (`ka20001`, W1 L30152–30442)

| Field | Label | Type(len) | Description (verbatim) |
| --- | --- | --- | --- |
| `cur_prc` | 현재가 | String(20) | "단위: 지수, 부호가 포함된 숫자" |
| `pred_pre_sig` | 전일대비기호 | String(20) | "1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락" |
| `pred_pre` | 전일대비 | String(20) | "단위: 지수, 부호가 포함된 숫자" |
| `flu_rt` | 등락률 | String(20) | "단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율" |
| `trde_qty` | 거래량 | String(20) | "단위: 1000주" |
| `trde_prica` | 거래대금 | String(20) | "단위: 백만원" |
| `open_pric` / `high_pric` / `low_pric` | 시가 / 고가 / 저가 | String(20) | "단위: 지수, 부호가 포함된 숫자" |
| `upl`, `rising`, `stdns`, `fall`, `lst` | 상한, 상승, 보합, 하락, 하한 | String(20) | "단위: 종목수" |
| `52wk_hgst_pric`, `52wk_lwst_pric` (+ `_dt` "YYYYMMDD", `_pre_rt`) | 52주최고가 / 최저가 | String(20) | value "단위: 지수, 부호가 포함된 숫자" |
| `inds_cur_prc_tm[]` | 업종현재가_시간별 | LIST | rows `tm_n` "HHmmss", `cur_prc_n`, `pred_pre_sig_n`, `pred_pre_n`, `flu_rt_n`, `trde_qty_n` "단위: 1000주", `acc_trde_qty_n` "단위: 1000주" |

- **No previous-close field** and **no as-of date or time** at top level.
  The only time is `tm_n` "HHmmss" inside the list, with no date.
- **Signed value.** The example (W1 L30454) has `"cur_prc": "-2394.49"`
  with `"pred_pre_sig": "5"`, `"open_pric": "-2669.53"`,
  `"52wk_hgst_pric": "+3001.91"`. **Inference:** the sign marks the
  direction against the previous close, not a negative index; the field
  table says only "부호가 포함된 숫자".
- **Decimals:** the example has two decimals; the field table does not
  state a scale for this route.
- Example list rows are newest first (`143000`, `142950`, `142940`,
  `142930`) at 10-second spacing; the interval is not documented.
- `ka20009` (W1 L32216–32496) repeats the same top-level fields and adds
  `inds_cur_prc_daly_rept[]` with `dt_n` "YYYYMMDD", `cur_prc_n`,
  `pred_pre_sig_n`, `pred_pre_n`, `flu_rt_n`, `acc_trde_qty_n` "단위:
  1000주". No per-row open/high/low.
- `ka20003` rows (W1 L30838–30978): `stk_cd`, `stk_nm`, `cur_prc`
  "단위: 지수, 부호가 포함된 숫자", `pre_sig`, `pred_pre`, `flu_rt`,
  `trde_qty` "단위: 1000주", `wght` "비중", `trde_prica` "단위: 백만원",
  breadth counts, `flo_stk_num` "상장종목수". Example index codes are
  returned in a field named `stk_cd` (`"001"`, `"002"`, `"003"`).

### 3.5 Index candles

| Concern | `ka20004` tick | `ka20005` minute | `ka20006`/`07`/`08`/`19` day/week/month/year |
| --- | --- | --- | --- |
| Interval input | `tic_scope` String(2) "1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱" (L31065) | `tic_scope` "1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분" (L31288) | fixed per API |
| Date input | none | `base_dt` String(8) **N** "YYYYMMDD" (L31298) | `base_dt` String(8) Y "YYYYMMDD" (L31531, L31957, L32583; `ka20007` String(3), L31744) |
| Value fields | `cur_prc`, `open_pric`, `high_pric`, `low_pric`: "단위: 지수\n\n※ 지수 값은 소수점 제거 된 100배 값으로 제공됩니다." (L31131–31181) | same (L31364–31414) | same (e.g. L31597–31647) |
| Time field | `cntr_tm` "YYYYMMDDHHmmss" (L31151) | `cntr_tm` "체결시간", **no format** (L31384) | `dt` "YYYYMMDD" |
| Volume | `trde_qty` "단위: 1주" | `trde_qty` (no unit), `acc_trde_qty` "단위: 1주" | `trde_qty` "단위: 1주"; `trde_prica` "단위: 백만원" (`ka20008`: no unit, L32083) |
| Change | `pred_pre` "현재가 - 전일종가", `pred_pre_sig` 1–5 | same | none |

- **Scale:** chart values are integers at 100× (field table). Example
  `ka20006` row `"cur_prc": "252127"` (L31669). **Inference:** 2521.27.
- **Adjustment:** no 수정주가 input on any index chart route (stock chart
  routes take `upd_stkpc_tp`, e.g. W1 L23318). **Inference:** not
  applicable.
- **Paging:** `cont-yn` / `next-key` headers ("다음 데이터가 있을시 Y값
  전달"). W4 (client code) loops on them up to `MAX_PAGES = 10` (L20).
  Rows per page and boundary semantics are **not documented**.
- **Row order:** every chart example lists the newest row first
  (`ka20004` `20250917142630` then `20250917142350`; `ka20006` `20250210`
  then `20250207`; `ka20019` `20250102` then `20241105`). Not stated in a
  field table.
- **History depth:** not documented.

### 3.6 Venue / calculation scope

- No index route takes a venue input; `stk_cd` suffixes `_NX`/`_AL` are
  not used. `stex_tp` "거래소구분" "1:KRX, 2:NXT, 3:통합" appears **only** on
  the constituent route `ka20002` (W1 L30539), for member stock prices.
- The `ka20001` example rows carry `"stex_tp": ""` (W1 L30454), a key not
  in its field table.
- `ka10101` labels code `7` "KRX100(통합지수)". **Inference:** "통합" here
  names an index family, not an NXT-inclusive calculation.
- Calculation source and NXT inclusion: **not documented**.

### 3.7 Contradictions and gaps

1. **Two value scales.** `ka20001`/`ka20003`/`ka20009` give decimal
   strings ("-2394.49"); `ka20004`–`ka20008`/`ka20019` give "소수점 제거
   된 100배 값" ("252127"). A shared decoder would be wrong for one set.
2. **`ka20005` example is a daily example.** Field table rows are
   `inds_min_pole_qry` with `cntr_tm`/`acc_trde_qty`/`pred_pre`; the
   response example (L31456) is `inds_dt_pole_qry` with `dt` and
   `trde_prica`, byte-identical to the `ka20006` rows. W5 L28 follows the
   field table.
3. **Undocumented sign code.** `ka20004` example `"pred_pre_sig": "43"`
   (L31213), outside "1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"; its
   `pred_pre` `"18031"` is unsigned.
4. **Swapped lengths.** `ka20007` `inds_cd` String(8) and `base_dt`
   String(3) (L31734, L31744); every sibling has String(3) and String(8).
5. **Examples are not strict JSON.** `ka20004`–`ka20008` examples end
   their arrays with a trailing comma (`},\n    ],`).
6. **Volume units differ** between current (1000주) and chart (1주)
   routes; `ka20005` `trde_qty` and `ka20008` `trde_prica` have no unit.
7. **`mrkt_tp` coverage.** `ka10101` lists `4:KOSPI100` and
   `7:KRX100(통합지수)`; `ka20001` accepts only `0`/`1`/`2`, while its
   `inds_cd` list includes `701: KRX100` and `302:KOSTAR`. Which `mrkt_tp`
   goes with `701` or `302` is not documented.
8. **Illustrative dates.** `ka20006` requests `base_dt` `20250905` but
   the example rows are February 2025; `ka20008` example (`base_dt`
   `20250905`) has a row dated `20250917`.
9. **Undocumented key.** `stex_tp` in the `ka20001` example (§3.6).
10. **Gaps:** time zone, page size, depth, tick interval semantics,
    `inds_cur_prc_tm` spacing, whether `cur_prc` can be empty before the
    open.

### 3.8 Gates and not-verified items

- G-W1: one decoder per scale family; the 100× rule applies only where
  the field table states it.
- G-W2: sign handling must use `pred_pre_sig` and the documented "부호가
  포함된 숫자" rule only after an authorized fixture shows the sign
  semantics; unknown codes such as `43` must fail closed.
- G-W3: `ka20005` row key, `cntr_tm` format and volume unit need an
  authorized fixture (the example is unusable).
- G-W4: `mrkt_tp` × `inds_cd` pairing for KRX100/KOSTAR needs publisher
  confirmation.
- Not verified: any response; mock support per route; paging; row order;
  time zone; scale of `ka20003`/`ka20009` beyond the example.

## 4. LS Securities

### 4.1 Pinned sources

All LS sources are public web resources on `https://openapi.ls-sec.co.kr`
without an immutable revision; only L1 carries a publisher version marker.
Detail endpoints return JSON; the path is the TR's `data-tr` id and `api=`
is the parent sub-menu id from L2: `88a7c0d3-fb4f-48ef-bc9b-4c47ac72a87b`
(`[업종] 시세`, `/indtp/market-data`) or
`5b483d74-407c-4760-8452-1b2b1dc1dcde` (`[업종] 차트`, `/indtp/chart`).
Each sha256 prefix identifies only the copy retrieved at the stated time.

| # | Path / URL | Pin (sha256 prefix, UTC retrieval, revision) | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true | `9aaca437f1925115`, 07:59:52Z, 2,792,313 bytes; `"version" : "20261026021444748"` (L2) | TR discovery, field tables, `transactionPerSec`, `servers` (L7–15). Byte-identical prefix to the copy pinned by the trade audit. |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `815ea2f522673904`, 07:59:54Z (page varies per request) | `data-api` / `data-tr` ids (L440–506, L1189) |
| L3 | `…/guide/api/8ll424vf-400s-6yy2-kc17-rq0s3z16q53b?type=rest&api=88a7c0d3-…` (t1511) | `5d0d16dbfe5d1796`, 08:01:23Z | Field table, code sample, response example |
| L4 | `…/guide/api/6elw1gsv-2ddm-27t2-an4o-6q1s5v18x78n?type=rest&api=88a7c0d3-…` (t1514) | `29f5799de78e80eb`, 08:01:24Z | Same |
| L5 | `…/guide/api/xknl5740-7upu-zukv-7tpa-153466dx54r3?type=rest&api=88a7c0d3-…` (t8424) | `75d57073f3f34471`, 08:01:25Z | Same |
| L6 | `…/guide/api/87477b5n-06j7-j553-67gb-2u6ix76fy6fx?type=rest&api=5b483d74-…` (t8408) | `86ae30bd8b5ee511`, 08:01:26Z | Same |
| L7 | `…/guide/api/wv87v3rg-6ru5-4ibe-z53e-25h83b24pm5c?type=rest&api=5b483d74-…` (t8409) | `0454f4300d0f8bcc`, 08:01:28Z | Same |
| L8 | `…/guide/api/03vo4mle-l8q8-1r45-u224-5bo27y1c8t54?type=rest&api=5b483d74-…` (t8429) | `1f70911f819e3374`, 08:01:29Z | Same |

`…` stands for `https://openapi.ls-sec.co.kr`.

**TR id check.** The requested ids `t8417`, `t8418`, `t8419` occur **zero**
times in L1 and L2. The `[업종] 차트` sub-menu (L1 api[4], L2 L470–490)
lists exactly `t8408` 업종차트(틱/n틱), `t8409` 업종차트(N분) and `t8429`
업종차트(일주월). `t1511`, `t1514` and `t8424` are confirmed.

**Missing evidence:**

- No publisher Git repository or SDK for LS REST; every fact is from the
  portal (field table or example).
- No sign-code list, unit or time-zone statement for any 업종 TR.
- No example with a falling index, a continuation call, `comp_yn` `Y` or
  `t1514` minute mode.

### 4.2 Routes

Common transport (L1, L3–L8): `POST`, `https://openapi.ls-sec.co.kr:8080`,
body `{"<tr>InBlock": {...}}`, headers `content-type`, `authorization`,
`tr_cd`, `tr_cont`, `tr_cont_key`, `mac_address` "법인인 경우 필수 세팅";
responses carry `rsp_cd` (`"00000"`) and `rsp_msg` in the examples.

| Route (title verbatim) | Method + path | TR | Real / paper | Current / candles / list | Evidence |
| --- | --- | --- | --- | --- | --- |
| 업종현재가 | POST `/indtp/market-data` | `t1511`, TPS "10" (L1 L705) | not stated | current value (`t1511OutBlock`) | field table + example |
| 업종기간별추이 | POST `/indtp/market-data` | `t1514`, TPS "1" | not stated | 일/주/월 (and "분") rows with OHLC | field table + example |
| 전체업종 | POST `/indtp/market-data` | `t8424`, TPS "1" | not stated | code list | field table + example |
| 업종차트(틱/n틱) | POST `/indtp/chart` | `t8408`, TPS "1" | not stated | tick candles | field table + example |
| 업종차트(N분) | POST `/indtp/chart` | `t8409`, TPS "1" | not stated | 30-second / n-minute candles | field table + example |
| 업종차트(일주월) | POST `/indtp/chart` | `t8429`, TPS "1" | not stated | daily / weekly / monthly candles | field table + example |
| 예상지수 / 업종별종목시세 | POST `/indtp/market-data` | `t1485` / `t1516` | not stated | named only | field table |

- L1 `servers` (L7–15): REST has only `url`
  `https://openapi.ls-sec.co.kr:8080`; only the WebSocket server lists a
  `simulationUrl`. Paper REST behaviour for these TRs: **not documented**.
- WebSocket (name only): `IJ_` "지수" and `YJ_` "예상지수" under "[주식]
  실시간 시세" (L1 L26352, L31307); `BM_` 업종별투자자별매매현황 under
  "[업종] 실시간 시세" (L1 L1364).

### 4.3 Index identifiers

- `t1511InBlock.upcode` String(3) (L1 L749): "코스피@001\r\n코스피200@101\r\n
  KRX100@501\r\n코스닥@301".
- `t1485InBlock.upcode` (L1 L569, context): "코스피@001\n코스닥@301\n
  KRX100@501\nKP200@101\nSRI@515\n코스닥프리미어@404\nKRX 보험@516\nKRX
  운송@517".
- `t1514InBlock.upcode` String(3) (L1 L221): no description. Chart TRs
  use `shcode` "단축코드" String(3) with no description (L1 L1498, L1724,
  L1961); examples use `"001"`.
- `t8424` 전체업종 (L1 L422–511): input `gubun1` "구분1" String(1), **no
  description**; output array `hname` "업종명" String(20), `upcode`
  "업종코드" String(3). Example (L5) `gubun1` `""`; rows `001` "종       합",
  `002` "대   형  주", `820` "KQ150 L KP200 0.5 S".
- **Inference:** `t8424` is the list for `upcode`/`shcode`; no LS text
  links the two explicitly.

### 4.4 Current value response (`t1511OutBlock`, L1 L784–1108)

| Concern | Fields (label, type) |
| --- | --- |
| Value | `pricejisu` 현재지수 Number(10.2); `jniljisu` 전일지수 Number(10.2) |
| Change | `sign` 전일대비구분 String(1) (**no code list**); `change` 전일대비 Number(10.2); `diffjisu` 지수등락율 Number(6.2) |
| OHL + times | `openjisu`/`highjisu`/`lowjisu` Number(10.2); `opentime`/`hightime`/`lowtime` String(6) |
| Volume / value | `volume` 당일거래량, `jnilvolume` 전일거래량, `value` 당일거래대금, `jnilvalue` 전일거래대금, all Number(12), **no unit** |
| Ranges | `whjisu` 52주최고지수 Number(10.2), `wljisu` 52주최저지수 **Number(7.2)**, `yhjisu`/`yljisu` Number(10.2), dates String(8) |
| Sub-indices | `firstjcode` … `fourthjcode` String(3) with name, value, sign, change, rate |
| Breadth | `highjo` 상승, `upjo` 상한, `unchgjo` 보합, `lowjo` 하락, `downjo` 하한, Number(4) |
| Header | `gubun` 업종구분 String(1) (no code list), `hname` 업종명 String(20) |
| As-of time | **none** |

- Example (L3): `"pricejisu": "2610.62"`, `"jniljisu": "2601.36"`,
  `"sign": "2"`, `"change": "9.26"` — `Number` fields are JSON
  **strings**; `"volume": 263165`, `"value": 3884240`, breadth counts are
  JSON **numbers**. `hname` is space-padded ("종       합").
- `jniljisu` gives a previous-close index value, which KIS (§2.4) and
  Kiwoom (§3.4) do not.

### 4.5 Index candles

| Concern | `t8408` tick | `t8409` N분 | `t8429` 일주월 | `t1514` 기간별추이 |
| --- | --- | --- | --- | --- |
| Interval | `ncnt` "단위(n틱)" Number(4) | `ncnt` "0:30초\n1: 1분\n2: 2분\n.....\nn: n분" (L1 L1729) | `gubun` "주기구분(2:일3:주4:월)" (L1 L1966) | `gubun2` "일@1\n주@2\n월@3\n분" (L1 L232) |
| Count | `qrycnt` "요청건수(최대-압축:2000비압축:500)" | same | same (L1 L1971) | `cnt` 조회건수 Number(4), no maximum |
| Range | `sdate` "기본값 : Space (edate(필수입력) 기준으로 qrycnt 만큼 조회)"; `edate` "처음조회기준일(LE) … ("99999999" 혹은 '당일')"; `stime`/`etime` "(현재미사용)" | same | `sdate`, `edate` | none; `cts_date` |
| Continuation | `cts_date` "처음 조회시는 Space 연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정"; `cts_time` (no description) | same | `cts_date` | `cts_date` "연속조회기준일(LT)" (L1 L238) |
| Row fields | `date` String(8), `time` String(6), OHLC Number(10.2), `jdiff_vol` Number(12) | + `value` 거래대금 | `date`, OHLC, `jdiff_vol`, `value` | `date`, `jisu`/`openjisu`/`highjisu`/`lowjisu` Number(12.2), `volume`, `value1`, `value2`, breadth, `frgsvolume`, `orgsvolume` |
| Header block | prior/today OHLC, `s_time` "장시작시간(HHMMSS)", `e_time`, `dshmin` "동시호가처리시간(MM:분)", `rec_count` | `s_time` "업종시작시간(HHMMSS)" | same (no `cts_time`) | `cts_date` only |
| Compression | `comp_yn` "N:비압축 모듈\nY: 압 축 모듈" (L1 L1553) | same | same | none |

- **Adjustment:** no 수정주가 input on any 업종 chart TR (the stock chart
  TRs `t8410` and `t8451` have `sujung`, L1 L43454, L44320).
  **Inference:** not applicable.
- **Row order:** examples are oldest first (`t8409` `102400` → `102800`;
  `t8429` `20230530` → `20230605`). Not stated in a field table.
- **Bar time:** whether `time` labels the bar start or end is not
  documented. The `t8409` example's last row (`102800`) has `jdiff_vol` 0
  and `value` 0. **Inference:** possibly a forming bar.
- **Example header values** (L6–L8): `s_time` `"090000"`, `e_time`
  `"153000"`, `dshmin` `"10"`.
- **History depth:** not documented; `nday` "조회영업일수(0:미사용1>=사용)".
- **Compression format** for `comp_yn` `Y` over REST: not documented.

### 4.6 Venue / calculation scope

- No 업종 TR has `exchgubun` or any NXT/통합 field (searched L1
  L175–2160). `exchgubun` occurs 44 times elsewhere in L1 (stock TRs).
- Calculation source and NXT inclusion: **not documented**.

### 4.7 Contradictions and gaps

1. **Requested TR ids absent.** `t8417`/`t8418`/`t8419` are not in L1 or
   L2; the 업종 chart TRs are `t8408`/`t8409`/`t8429` (§4.1).
2. **`t1514` continuation text.** OutBlock `cts_date` (L1 L288) says "이
   필드의 데이터를 다음 조회시 InBlock의 date 필드에 넣어준다", but the
   InBlock field is `cts_date`; the InBlock text says "(cont:1일때)" and
   there is no `cont` field.
3. **`t1514` minute mode** "분" has no code value (L1 L232).
4. **`Number` vs JSON type.** Index `Number(10.2)` fields are JSON
   strings in every example; `Number(12)` counts are JSON numbers.
5. **`wljisu` width.** `Number(7.2)` (L1 L923) while the other index
   values are `Number(10.2)`.
6. **Code lists differ by TR.** `t1511` lists 4 codes, `t1485` lists 8,
   and the `t8424` example includes `820`; `t1514` and the chart TRs list
   none.
7. **Gaps:** `sign` and `gubun` code lists, volume/value units, time
   zone, `nday` behaviour, `cts_time` format, paper REST support.

### 4.8 Gates and not-verified items

- G-L1: the index decoder must read `Number(10.2)` values from JSON
  strings and integer counts from JSON numbers without float conversion,
  and reject other shapes until authorized fixtures show otherwise.
- G-L2: `sign` code list and `upcode` list source (`t8424`) need
  publisher confirmation.
- G-L3: bar-time semantics and the forming last bar (§4.5) need
  authorized fixtures before any intraday candle.
- Not verified: any response; paper REST; `comp_yn` `Y`; continuation;
  TPS enforcement.

## 5. DB Securities

**Pending.** Written in parallel; to be merged from the DB/Toss/Meritz
section file.

## 6. Toss Securities

**Pending.** Written in parallel; to be merged.

## 7. Meritz Securities

**Pending.** Written in parallel; to be merged.

## 8. Cross-broker comparison

DB, Toss and Meritz columns are pending.

### 8.1 Identifiers and values

| Concern | KIS | Kiwoom | LS |
| --- | --- | --- | --- |
| KOSPI | `U` + `0001` | `mrkt_tp` `0` + `001` | `001` |
| KOSDAQ | `U` + `1001` | `mrkt_tp` `1` + `101` | `301` |
| KOSPI200 | `U` + `2001` | `mrkt_tp` `2` + `201` | `101` |
| KRX100 | `4001` (legacy only) | `701` | `501` |
| Code list | `idxcode.mst` file | `ka10101` | `t8424` |
| Current value type | not documented | signed decimal string | `Number(10.2)` as JSON string |
| Chart value type | not documented | 100× integer string | `Number(10.2)` as JSON string |
| Previous close | none (derive?) | none | `jniljisu` |
| As-of time (current) | none | none (list `tm_n` only) | none (`opentime` etc. only) |
| Volume unit | not documented | 1000주 (current) / 1주 (charts) | not documented |
| Sub-minute bars | value series only (`FHPUP02110100`) | ticks (`ka20004`) | 30초 (`t8409` `ncnt` 0), ticks (`t8408`) |
| Yearly bars | `Y` (`FHKUP03500100`) | `ka20019` | none |
| Row order (examples / client code) | newest first (C, inference) | newest first (E) | oldest first (E) |

**Code collision:** `101` is KOSDAQ at Kiwoom and KOSPI200 at LS; `001`
(Kiwoom, LS) and `0001` (KIS) both mean KOSPI. A broker-native code is
therefore not a portable identifier.

### 8.2 Fit with the existing models (Inference only)

The models in `src/ktradelink/models/` were read at `main`
`7b7aa074045115103e18dce2558612f1e48394cf`.

- **Inference — venue.** `Ticker` and `Candle` require `venue` in
  `{"KRX", "NXT", "BROKER_COMPOSITE"}` (`_validation.py` `_VENUES`). No
  index route here takes or returns a venue, and no source states the
  calculating party or NXT inclusion. Labelling an index `KRX` would
  assert a scope the brokers do not document; `BROKER_COMPOSITE` would
  misdescribe an exchange-published index. A venue-free or
  "not-applicable" scope would be a model change.
- **Inference — symbol.** `validate_provenance` accepts `"0001"` or
  `"001"` (printable, no whitespace), but the same string means different
  indices at different brokers (§8.1), and ADR 0013 rejects any
  non-six-digit symbol (§9). A canonical index identifier and per-broker
  mapping would be needed.
- **Inference — value and sign.** `validate_price` requires an unsigned
  finite `Decimal`. Two-decimal index values fit `Decimal`. Kiwoom
  current values are signed strings and chart values are 100× integers;
  converting either needs a documented, per-route rule (§3.7 item 1),
  never a silent sign strip or float parse.
- **Inference — timestamp.** None of the current-value routes gives an
  as-of time with a date, so `Ticker.timestamp` must stay `None`; Kiwoom
  `tm_n` and LS `opentime` are times without a date.
- **Inference — volume.** `Ticker.volume`/`Candle.volume` are plain
  integers with no unit. Kiwoom's 1000주 vs 1주 split and the undocumented
  KIS/LS units mean an index volume cannot be stored without a unit
  decision.
- **Inference — fields without a home.** previous close (`Ticker` has
  `previous_close`, only LS supplies it), breadth counts, 52-week/yearly
  ranges and sub-index values would go to `info` or a new type. `bid`/
  `ask` do not apply.
- **Inference — candles.** `Candle` accepts only `timeframe="1d"`,
  `session="regular"` and `adjustment` in `{"raw", "adjusted"}`. Index
  routes have no adjustment input, so neither label is documented; weekly,
  monthly, yearly, minute, 30-second and tick bars are rejected by
  design. The Asia/Seoul midnight anchor and the OHLC ordering check
  would apply to daily index bars.
- **Inference — overall.** Reusing `Ticker`/`Candle` for indices would
  require relabelling at least venue and adjustment. A separate typed
  index value (or an explicit model extension) is a maintainer decision
  (§10.1).

## 9. Relation to existing repository documents

None of the files below is edited by this change. The differences are
recorded here only.

| Document and claim | This audit |
| --- | --- |
| [ADR 0013](../decisions/0013-public-fetch-ticker-surface.md) L37: "`symbol` must be exactly six ASCII digits (`InvalidSymbol`)" | **Cannot express index codes.** KIS uses four characters (`0001`), Kiwoom and LS three (`001`). Any index method needs a new symbol rule or a separate identifier type (§10.1). |
| Same ADR L37–39: `venue` must be `"KRX"`; `NXT`/`BROKER_COMPOSITE` raise `UnsupportedCapability` | No index route here has a venue (§2.6, §3.6, §4.6); the ADR's venue rule has no index meaning. |
| [market-data spec](../specifications/market-data-v0.1-draft.md) §3 L60–62: six-digit stock symbol; do not "auto-guess ETFs/ETNs, indices, bonds or derivatives. Expand the instrument registry later." | **Consistent.** Index support needs that registry expansion first; this file supplies evidence only. |
| `src/ktradelink/models/_validation.py` `_VENUES` = `KRX`, `NXT`, `BROKER_COMPOSITE` | No value fits an index (§8.2). |
| [Capability inventory](capability-inventory-2026-11-05.md) rows 1–11 | **No index/sector row.** Index quotes are not inventoried there; this file is the first audit of them. |
| Candle evidence (branch `claude/issue-17-candle-evidence` @ `3cae42624ee5aae9c2bae214efc411bf7d9f96d9`, not merged) | Covers equity candles. It mentions a Meritz index-only route as out of scope; it does not cover the KIS/Kiwoom/LS index chart routes of §2.5, §3.5, §4.5. |
| Symbol-master evidence (branch `claude/issue-17-symbol-master-evidence` @ `b127724ee73fac239d987a2fa2a5b889c5f92bfb`, not merged) L415: `upName` "업종명" as a stock attribute | No index master is covered there; KIS `idxcode.mst`, Kiwoom `ka10101` and LS `t8424` are recorded here (§2.3, §3.3, §4.3). |
| Trade evidence (branch `claude/issue-17-trade-evidence` @ `bed8a9cb2d58687bc86ff29bab5dc3cc5fe74fdc`, not merged) §3.1 | Same Kiwoom pin `c7a3d254`; LS L1 sha256 prefix `9aaca437f1925115` identical. |
| [six-broker-ticker-decoders.md](six-broker-ticker-decoders.md) | Equity ticker scope; this file does not widen it. |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any index decoder, request plan or public
index method is written. Broker tags are in brackets; DB/Toss/Meritz
gates are pending.

### 10.1 Identity and model

- G-I1: choose a canonical index identifier and a per-broker mapping;
  ADR 0013's six-digit rule does not apply (§9). Broker-native codes
  collide (§8.1).
- G-I2: decide between a new typed index model and an extension of
  `Ticker`/`Candle`; venue and adjustment have no documented index value
  (§8.2). No dict/JSON public surface.

### 10.2 Value scale, type and sign

- G-I3: [Kiwoom] separate decoders for decimal current values and 100×
  chart values; [LS] read `Number(10.2)` from JSON strings; [KIS] obtain
  types first (G-K1). No float parsing.
- G-I4: [Kiwoom, LS, KIS] sign/direction codes are undocumented or
  partially documented; unknown codes (e.g. Kiwoom `43`) must fail
  closed, and no signed value may be silently made unsigned.

### 10.3 Codes and lists

- G-I5: [KIS] `idxcode.mst` offsets conflict (§2.7); [Kiwoom]
  `mrkt_tp`/`inds_cd` pairing undocumented for some codes; [LS] code-list
  source not stated per TR. Code lists must not be hard-coded from
  examples.

### 10.4 Time

- G-I6: [all three] no as-of timestamp with a date on current values;
  `timestamp` stays `None` unless a dated field is documented. Time zone
  is not documented anywhere. Intraday bar time semantics (start vs end)
  are not documented [KIS, Kiwoom, LS].

### 10.5 Candles and paging

- G-I7: row order differs by broker (§8.1) and is documented only by
  examples or client code; page size and depth are not documented
  [KIS, Kiwoom]; LS caps 500/2000 per request. Continuation boundaries
  need fixtures. The KIS example continuation bug (§2.7 item 6) must not
  be copied.
- G-I8: units of index volume/value [KIS, LS] and the Kiwoom 1000주/1주
  split must be decided before any volume field is populated.

### 10.6 Environment, venue and limits

- G-I9: paper support per route is not established [KIS, Kiwoom, LS];
  no silent LIVE/PAPER fallback.
- G-I10: no NXT-inclusive or venue-specific index route was found; do
  not infer one from equity venue codes.
- G-I11: documented TPS [LS `t1511` 10, others 1] only; other limits not
  re-verified here. No automatic retry beyond what a reviewed transport
  policy allows (the KIS backtester's automatic `EGW00201` retry, K17
  L495–509, is client code, not a policy).

## 11. Not verified

- Any live or paper response for any route above. No broker API request
  was sent.
- DB, Toss and Meritz: **pending** (§5–§7).
- Entitlements, real/paper parity and redistribution rights.
- KIS: field types, decimals, units and sign codes; the `idxcode.mst`
  layout; paper support of `FHPUP02100000`/`FHPUP02120000`;
  `FID_INPUT_HOUR_1` accepted values; `FID_PW_DATA_INCU_YN` and
  `FID_ETC_CLS_CODE` effects; `output2` order and depth.
- Kiwoom: sign semantics of `cur_prc`; `pred_pre_sig` values beyond 1–5;
  `ka20005` response shape; page size, depth and order; mock support per
  route; `mrkt_tp` pairing for `701`/`302`.
- LS: `sign`/`gubun` codes; volume/value units; bar-time semantics;
  `comp_yn` `Y`; continuation; `t1514` minute mode; paper REST.
- Time zone, holiday, half-day and pre-open behaviour on every route.
- Whether any broker's index value includes NXT trades.
- WebSocket feeds `H0UPCNT0`, `0J`, `IJ_` beyond their names.
