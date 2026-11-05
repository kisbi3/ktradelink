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
  - DB: the SDK at a fixed commit, fetched by SHA at 07:54 (`git
    ls-remote` at 07:54:56 showed it still at the default-branch HEAD);
    portal JSON endpoints 07:55:37–07:56:34 (§5.1).
  - Toss portal documents: 07:57:35–07:57:38 (§6.1).
  - Meritz: portal spec export 07:58:47; the repository at a fixed
    commit, fetched by SHA at 07:54 (§7.1).
- **Re-hash:** every Git blob SHA in §2.1 and §3.1 was computed from the
  retrieved bytes and matched the `git ls-tree` entry of the pinned
  commit. Every sha256 prefix in §4.1 identifies the retrieved copy.
  When §5–§7 were merged, these pins were re-fetched at 08:12:23–08:12:27
  and matched: DB D1 and D9 blobs and the DP1 sha256 prefix; Toss T1 and
  T2 sha256 prefixes; Meritz M2 and M3 blobs. Quoted lines D1 L176, D9
  L59, M2 L9398/L9562/L9854/L16297/L16461/L16753 and M3 L6–9 were
  re-read in those copies.
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
  - `publisher guide`: portal prose outside the API specification or
    field tables (Toss overview and FAQ, §6.1). It ranks below `field
    table`.
  - `publisher repo note`: non-code text in a publisher repository
    (including C header comments and the DB/Meritz repository docs).
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- Sample values in publisher examples are illustrative. They are **not**
  authorized response fixtures. Several examples below are internally
  inconsistent (§3.7, §5.7, §7.7), which is itself recorded as evidence.

## 1. Broker × concern summary

Cell format: short verdict — evidence. `F` field table, `E` publisher
example, `L` legacy publisher example, `C` publisher client code, `N`
publisher repo note, `G` publisher guide, `—` not found. Source ids in
cells (D…, M…) refer to §5.1 and §7.1.

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Current value route | `FHPUP02100000` GET `…/quotations/inquire-index-price` 국내업종 현재지수 — E | `ka20001` 업종현재가요청 POST `/api/dostk/sect`; all-sector list `ka20003` — F+E | `t1511` 업종현재가 POST `/indtp/market-data`, TPS 10 — F+E | `PRICE` POST `/api/v1/quote/kr-stock/inquiry/price` with `InputCondMrktDivCode` `U`, 5 TPS — F; `MULTIPRICE` 1–50 symbols, index row in example — F+E | `GET /api/v1/market-indicators/prices` (`getMarketIndicatorPrices`, ≤200 symbols) — F+E | `ohhts_1514_001r` GET `/market/v1/index/prices`, `x-tps` 10 — F+E |
| Daily/weekly/monthly candles | `FHKUP03500100` `…/inquire-daily-indexchartprice` D/W/M/Y; `FHPUP02120000` `…/inquire-index-daily-price` D/W/M — E; `FHKUP03500100` also L | `ka20006`/`ka20007`/`ka20008`/`ka20019` 일/주/월/년봉 POST `/api/dostk/chart`; `ka20009` daily list — F+E | `t8429` 업종차트(일주월) POST `/indtp/chart`; `t1514` 업종기간별추이 (일/주/월) — F+E | `CHARTDAY`/`CHARTWEEK`/`CHARTMONTH` (`M`/`Y`) POST `/api/v1/quote/kr-chart/*`, `U` listed, **no index example** — F; `UPTJJDAY` daily close, index only in its example — E | `GET /api/v1/market-indicators/{symbol}/candles` `interval` `1d` only (no week/month/year), ≤200 bars — F+E | `ohhts_1514_101r` GET `/market/v1/index/candles/days` D/W/M/Y, no date range or count — F+E |
| Intraday candles / series | `FHKUP03500200` `…/inquire-time-indexchartprice` (`FID_INPUT_HOUR_1` seconds) — E+L; value series `FHPUP02110100` (초), `FHPUP02110200` (분) — E | `ka20005` 분봉 (1–60분), `ka20004` 틱 (1–30틱) — F+E | `t8409` N분 (`0:30초`, n분), `t8408` 틱/n틱 — F+E | `CHARTMIN` `InputDivXtick` seconds ("30: 30초 / 60: 1분 …"), `CHARTTICK` N-tick; no index example — F | same route, `1m` (indices only); no `1m` example — F | `ohhts_8001_002r` GET `/market/v1/index/candles/minutes`, `hour_cls_code` seconds; `888888`/`999999` non-time rows — F+E+C |
| Index code format | 4 chars, `FID_COND_MRKT_DIV_CODE` `U`; "코스피(0001), 코스닥(1001), 코스피200(2001)" — E | 3 chars `inds_cd` + `mrkt_tp` "0:코스피, 1:코스닥, 2:코스피200"; "001:종합(KOSPI) … 101:종합(KOSDAQ), 201:KOSPI200 …" — F | 3 chars `upcode`/`shcode`; "코스피@001 코스피200@101 KRX100@501 코스닥@301" — F | `U` + 4 chars; "1001" KOSPI, "2001" KOSDAQ, "3001" KOSPI200, "0100" KRX100 (16-code list) — F | symbol names `KOSPI`, `KOSDAQ` only, in an 8-symbol catalog with six `KR_BOND_*` — F | 6 chars `iscd`: `KGG01P` (F); `QGG01P`, `K2G01P`, `XGG01P` (C only) |
| Code list route / file | file `idxcode.mst.zip` (name + layout only) — C+N; no REST list found | `ka10101` 업종코드 리스트 POST `/api/dostk/stkinfo` — F+E | `t8424` 전체업종 POST `/indtp/market-data` — F+E | `USTOCKCOND` 업종분류코드 조회 POST `…/inquiry/industry-cls`; parameter placement contradictory — F+E | none; static catalog in T1 `tags[5]` — F | — (not found) |
| Value scale / type | column names only; no type or decimals documented | current: decimal string "단위: 지수, 부호가 포함된 숫자"; charts: "소수점 제거 된 100배 값" — F | `Number(10.2)`; examples are JSON strings `"2610.62"` — F+E | `Prpr` String 16, no description; index examples `"2588.72"` — F+E | `lastPrice` decimal string, unit "포인트"; example `"2812.45"` — F+E | `stck_prpr` Number 13; example JSON number `2487.15`; decimals not documented — F+E |
| Previous close | **none** (only `prdy_clpr_vrss_lwpr`) — E | **none** — F | `jniljisu` 전일지수 — F+E | `Sdpr` "기준가" (= previous close by example arithmetic, inference) — F+E | **none** — F | `prdy_clpr` "전일종가" — F+E |
| As-of time on current value | **none** in the column map — E | **none** at top level; `inds_cur_prc_tm[].tm_n` "HHmmss", no date — F | **none**; only `opentime`/`hightime`/`lowtime` String(6) — F | **none** on PRICE/MULTIPRICE — F | `timestamp` date-time with offset, "데이터 미제공 시 null" — F | **no time**; `stck_last_tr_date` YYYYMMDD only — F |
| Volume / value units | not documented | current "단위: 1000주", "단위: 백만원"; charts "단위: 1주" — F | not documented — F | not documented — F | candle `volume` decimal string, unit not documented; no 거래대금 — F | `acml_vol` "체결된 주식 수" (shares); `acml_tr_pbmn` unit not stated — F |
| Venue / NXT | no venue parameter; `U` only — E | no venue parameter on index routes; `stex_tp` only on constituent route `ka20002` — F | no `exchgubun` on any 업종 TR — F | `U` only; `NJ`/`UJ` and `N-`/`U-` are stock-only — F | not stated for indices (the KRX+NXT FAQ answer concerns stocks) — — | no venue selector on index routes — F |
| Real / paper | legacy Postman marks `FHKUP0350*` "[실전투자/모의투자]", `FHPUP02110100` "[실전투자]" — L; others not stated | both domains in meta; PRD and MOCK Postman items; error `8104` possible — F | REST server list has no simulation URL — F | "REST API URL은 운영/모의 동일" (D12); ⭕ per route (D4); demo index data not stated — N | real origin only; no paper origin in T1 — F | real only; "모의계좌는 없습니다" (M7 L125) — N |
| WebSocket feed (name only) | `H0UPCNT0` 국내지수 실시간체결 — E | `0J` 업종지수 (also `0U` 업종등락) — F | `IJ_` 지수 (also `YJ_` 예상지수) — F | `U00` [실시간]업종지수체결가 (also `U03`, `U05`) — C | **not found** (no index channel in T3) — F | **not found** — F |

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
(L2343) and `inquire_index_daily_price` (L2515), all under "[국내주식]
업종/기타". K9–K11 are not registered.

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

### 5.1 Pinned sources

GitHub sources are at
[`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb)
(`564b5100b80a3a785468b77ee8c0557f6edcfdeb`, committer date
2026-08-20T10:06:26+09:00), the commit already pinned by the trade and candle
evidence. Blob SHAs are from `git ls-tree` of that commit. Portal JSON
endpoints on `https://openapi.dbsec.co.kr` were retrieved 2026-11-05
07:55:37–07:56:34Z. DP1 has the same sha256 as the trade-evidence copy
(07:13:25Z).

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| D1 | [`dbsec_sdk/apis/kr_stock_quote/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_quote/endpoints.py) | blob `5930af396f4a74ff04c7e780fcec87660399bec3`; L29–64 paths/TR codes; L143–216 MULTIPRICE (L170, L175–176); L218–267 PRICE (L231, L235–236); L425–426 RANKLIST; L453–508 UPTJJDAY (L468, L472–473); L696–732 USTOCKCOND (L709, L713–714); L734–781 USTOCKCONDLIST | Routes, TPS docstrings, truncated code-list docstrings (§5.7 item 4) |
| D2 | [`dbsec_sdk/apis/kr_chart/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_chart/endpoints.py) | blob `0b80a958e7c97e73bf2f4430b1550625fe3ab204`; L28–43; L65–74 tick; L120–129 min; L174–191 day; L227–245 week; L282–300 month | Chart routes, "4 TPS", interval codes |
| D3 | [`dbsec_sdk/apis/kr_stock_realtime/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_realtime/endpoints.py#L206-L254) | blob `4a230c35ef8732722ddd23a73f84c8fd0effb919`; L36–37, L48–49, L206–229, L231–254 | WebSocket `U00`/`U03` names only |
| D4 | [`docs/api_support_matrix.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/api_support_matrix.md) | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c`; L3–5, L55–56, L61, L66–67, L79–81, L153–157 | ⭕ "모의투자(`mode: "demo"`) + 실전투자 모두 호출 가능"; TPS |
| D5 | [`examples/kr_stock_quote/kr_stock_inquire_price_multi.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_price_multi.py#L52-L64) | blob `c8fdf801aac864822670a7b2215cc351eb639e4f`; L54–55, L62–63 | Example sends `U` / `1001` |
| D6 | [`examples/kr_stock_quote/kr_stock_inquire_daily_industry_investor.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_daily_industry_investor.py#L55-L56) | blob `a6d3e504fce28a9dcd5566dc85a33f05e5642bb3`; L55–56 | Example sends `U` / `1001` |
| D7 | [`examples/kr_stock_quote/kr_stock_inquire_industry_codes.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_industry_codes.py#L38-L39) | blob `57fb776a474d168c3ef9e26dcaeac17b8c10cc8c`; L38–39 | Example parameter values (§5.7 item 2) |
| D8 | [`examples/kr_stock_quote/kr_stock_inquire_condition_rise_fall.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_condition_rise_fall.py#L46) | blob `f9a55efcde8cc026afe5e6123ea9a647c63c8ceb`; L46 | "코스피:1001 코스닥:2001" (corroboration) |
| D9 | [`examples/kr_stock_quote/kr_stock_inquire_price.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_price.py#L59) | blob `f717db2b3ce2322d898785f850ca6f7c77afcc03`; L59–60 | Untruncated code list in an SDK comment |
| D10 | [`dbsec_sdk/response.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/response.py#L42-L83) | blob `6ce92fdc7fca3e34dda4c25b2797e153de29f7a5`; L42, L82–83 | `cont_yn`/`cont_key` headers; success `rsp_cd == '00000'` |
| D11 | [`docs/errors_and_rate_limits.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/errors_and_rate_limits.md) | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L48, L74, L106–109, L199–210 | `IGW00201`; `00000` message variants; app 20 TPS |
| D12 | [`config.yaml.example`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/config.yaml.example#L13-L14) | blob `f6204f1399f2f080c11f28364444b40b7868ef96`; L13–14 | "REST API URL은 운영/모의 동일 (앱 속성으로 내부 분기)" |
| DP1 | `https://openapi.dbsec.co.kr/api/apis/public/api-list/80005fb0-6feb-4b8b-904a-605c59e29b4f` (국내주식시세) | sha256 `f4f56996c26c33b3`, 07:55:37Z | Per-API `accessUrl`, `httpMethod`, `domain`, `simulatedDomain`, `extraParam` (`svc_id`, `requestLimit`), `lastModifiedDate` |
| DP2 | `…/api/apis/public/api-list/0bc09824-e8c2-491a-8c9d-b99e64b4b907` (국내주식/선물차트) | sha256 `f10207c4b22890cb`, 07:55:38Z | Same, for CHARTTICK/MIN/DAY/WEEK/MONTH |
| DP3 | `…/api/apis/public/<api_id>` | sha256 PRICE `beb86a75f39e448d`, MULTIPRICE `8cf7763a99b9238a`, CHARTTICK `3030724e0d291ff3`, CHARTMIN `934e7117d8643f31`, CHARTDAY `7536ac65cd74ff68`, CHARTWEEK `9b7c52bfb3ed1580`, CHARTMONTH `e9280acafdd96cd7`, USTOCKCOND `b32906c83c47172b`, USTOCKCONDLIST `5c6a1c142e998e29`, UPTJJDAY `7a690e94cacb23bf` (07:55:55–07:56:11Z) | Route descriptions; `lastModifiedDate` (§5.2). Contains staff contact data; not copied. |
| DP4 | `…/api/apis/guide/tr/<api_id>` | sha256 PRICE `6017533ab47fefef`, MULTIPRICE `b4e64123ae390dfd`, CHARTTICK `df8397f078cb1b8e` (identical to the trade-evidence copy), CHARTMIN `c34b20ae4c818bc1`, CHARTDAY `0e04795df4cf5496`, CHARTWEEK `7545a04ea0b4a23f`, CHARTMONTH `f39dc9948fd403ab`, USTOCKCOND `33224afa0fcb6941`, USTOCKCONDLIST `d0db210bd04260d4`, UPTJJDAY `f83c943b959ec456`, SECTORCOND `afa09b498bc23dc6` (07:55:54–07:56:10Z) | `trCode`, `transactionPerSec`, `reqExample`, `resExample` |
| DP5 | `…/api/apis/guide/tr/property/<tr_id>` | sha256 PRICE `a16222751d181c84`, MULTIPRICE `94360bc187c75c90`, CHARTTICK `6fd477a819e6b4e5`, CHARTMIN `0b5b3ad2fc756aa0`, CHARTDAY `16251b6327e67f6a`, CHARTWEEK `d13b6e29487432cc`, CHARTMONTH `f599b23f45d88bf6`, USTOCKCOND `a65cbe811312b93a`, USTOCKCONDLIST `ce36ece4480aec93`, UPTJJDAY `932e930d6c553da3`, SECTORCOND `e33139858f4aeed2` (07:56:26–07:56:34Z) | Header/body field tables, including the index code list |

API ids (DP1/DP2): PRICE `d7f6a691-8fe6-4733-901f-c2535417dc46`, MULTIPRICE
`3abd4f11-4a92-48f3-bc3e-726a97a47905`, CHARTTICK
`efe731f7-0f2a-45d1-81da-335ebeacd552`, CHARTMIN
`f8581e1f-5621-4be6-a4e7-7cc8088d603f`, CHARTDAY
`85fa3c5f-c317-43ab-8590-f57a28f2f8e9`, CHARTWEEK
`2a108f78-c73f-409f-82fa-d81befc899f8`, CHARTMONTH
`e34ed58e-6f91-4faa-8112-b9206395f2f0`, USTOCKCOND
`d373d73b-9d99-474e-a990-048132353d61`, USTOCKCONDLIST
`e75a5938-c6bb-4bb4-b424-06a021f6f560`, UPTJJDAY
`a4dc3cb3-ee90-4b40-a833-835a8bc2ac15`.

**Missing evidence:**

- No index (`U`) example for PRICE or for any chart route. The only index
  response examples are MULTIPRICE (row 5, `U`/`1001`) and UPTJJDAY
  (`U`/`1001`), both DP4.
- Every value field in DP5 has `description` null: no decimal places, unit,
  sign-code list or time zone for PRICE, MULTIPRICE or the chart rows.
- No code list for KOSDAQ, KOSPI200 or KRX sector indices (the USTOCKCOND
  example covers `K` only).
- No statement that demo (모의) apps receive index data.
- WebSocket `U00`/`U03` field tables were not reviewed (named only).

### 5.2 Routes

Common transport (DP1–DP5, D10, D12): `POST`, `contentType`
`application/json;charset=utf-8`, domain `https://openapi.dbsec.co.kr:8443`,
`simulatedDomain` null; D12 L13: "REST API URL은 운영/모의 동일 (앱 속성으로
내부 분기)". Request headers (DP5 `req_h`, all `requireYn` `Y`):
`content-type`, `authorization`, `cont_yn`, `cont_key` (String 70),
`mac_address` "제휴사인 경우 필수 세팅, 개인은 세팅 X". Response headers
`content-type`, `cont_yn`, `cont_key` (String 18). Body `{"In": {...}}`.

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Current value / candles / constituents | Evidence |
| --- | --- | --- | --- | --- | --- |
| "현재가조회" ("국내주식 현재가 조회 API입니다.") | `POST /api/v1/quote/kr-stock/inquiry/price` | `PRICE`; `d7f6a691-…`; `lastModifiedDate` 2024-06-05 | same origin (D12); ⭕ (D4 L56) | Current value. `InputCondMrktDivCode` lists "업종&지수: U". | field table (DP5); publisher example is `J` only (DP4); publisher client code (D1 L218–267) |
| "국내주식 멀티현재가조회" (`trName` "국내 멀티현재가조회") | `POST /api/v1/quote/kr-stock/inquiry/multiprice` | `MULTIPRICE`; `3abd4f11-…`; 2026-03-13 | same; ⭕ (D4 L55) | Current value, 1–50 symbols per call with a market code per symbol; mixing `U` with `J`, `F`, `JO` in one call is shown | field table + publisher example with an index row (DP4) + publisher client code (D1, D5 L62–63) |
| "틱차트조회" | `POST /api/v1/quote/kr-chart/tick` | `CHARTTICK`; `efe731f7-…`; 2025-08-27 | same; ⭕ (D4 L153) | N-tick candles; `U` listed | field table (DP5); example `J` only |
| "분차트조회" | `POST /api/v1/quote/kr-chart/min` | `CHARTMIN`; `f8581e1f-…`; 2025-08-27 | same; ⭕ (D4 L154) | Minute candles; `U` listed | field table (DP5); example `J` only |
| "일차트조회" | `POST /api/v1/quote/kr-chart/day` | `CHARTDAY`; `85fa3c5f-…`; 2025-08-27 | same; ⭕ (D4 L155) | Daily candles; `U` listed | field table (DP5); example `J` only |
| "주차트조회" | `POST /api/v1/quote/kr-chart/week` | `CHARTWEEK`; `2a108f78-…`; 2025-08-27 | same; ⭕ (D4 L156) | Weekly candles; `U` listed | field table (DP5); example `J` only |
| "월차트조회" | `POST /api/v1/quote/kr-chart/month` | `CHARTMONTH`; `e34ed58e-…`; 2025-08-27 | same; ⭕ (D4 L157) | Monthly/yearly candles; `U` listed | field table (DP5); example `J` only |
| "일별업종별투자자조회" ("국내 일별업종별투자자조회 API입니다.") | `POST /api/v1/quote/kr-stock/inquiry/daily-investor-u` | `UPTJJDAY`; `a4dc3cb3-…`; 2025-04-30 | same; ⭕ (D4 L61) | Daily index close + change + investor buy/sell per date range. The field table does **not** list `U` (§5.7 item 1). | publisher example (DP4, D6 L55–56); field table contradicts |
| "업종분류코드 조회" ("국내  업종분류코드를 조회 할 수 있는 API 입니다.") | `POST /api/v1/quote/kr-stock/inquiry/industry-cls` | `USTOCKCOND`; `d373d73b-…`; 2025-12-11 | same; ⭕ (D4 L66) | Index/sector code master (code + name only) | field table + publisher example (DP4/DP5) |
| "업종구성종목 조회" ("국내 업종구성종목을 조회 할 수 있는 API 입니다.") | `POST /api/v1/quote/kr-stock/inquiry/industry-components` | `USTOCKCONDLIST`; `e75a5938-…`; 2025-12-11 | same; ⭕ (D4 L67) | Constituents of one 업종 code, with stock quotes | field table (DP5) |

Rates (DP1/DP2 `extraParam` `ThroughputQuotaRule`/`CorpThroughputQuotaRule`
`requestLimit`; DP4 `transactionPerSec`; D1/D2 docstrings; D4): PRICE "5",
MULTIPRICE "2", CHART* "4", UPTJJDAY/USTOCKCOND/USTOCKCONDLIST "2" per
second. App level "20 TPS" (D11 L210). Over the limit: `IGW00201` (D11 L48,
L74).

Not index routes: SECTORCOND "섹터분류코드 조회" / SECTORCONDLIST return
thematic groups (DP4 example codes such as `9012` "반도체 장비", `9016`
"구제역/광우병 수혜"), not index values. RANKLIST filters stocks by
`InputBstpIscd`. WebSocket, named only (D3, D4 L79–81): `U00`
"[실시간]업종지수체결가", `U03` "[실시간]업종지수등락", `U05`
"[실시간]업종별투자자".

### 5.3 Index identifiers

- **Market-division code:** `U`, "업종&지수: U" in `InputCondMrktDivCode`
  (PRICE, CHART*) and `InputCondMrktDivCode1..50` (MULTIPRICE) (DP5). There
  is no separate index route; the stock routes switch on `U`.
- **Index code list** (DP5 `InputIscd1`, String 12, text identical across
  PRICE, MULTIPRICE and the five chart TRs apart from whitespace; also D9
  L59). Lead-in: "업종(U) 선택시 지수코드:".

  | Code | Name (verbatim) |
  | --- | --- |
  | `1001` | "KOSPI" |
  | `2001` | "KOSDAQ" |
  | `3001` | "KOSPI200" |
  | `1002` | "코스피(대형주)" |
  | `1004` | "코스피(소형주)" |
  | `1053` | "KOSPI50종합지수" |
  | `1054` | "KOSPI100종합지수" |
  | `1163` | "코스피고배당50" |
  | `2002` | "코스닥(대형주)" |
  | `2004` | "코스닥(소형주)" |
  | `2203` | "코스닥 150" |
  | `3903` | "KP200레버리지지수" |
  | `3907` | "변동성지수" |
  | `0100` | "KRX100" |
  | `0600` | "KTOP 30" |
  | `K001` | "KOVIXI00" |

- **Format:** four characters, digits except `K001`; no prefix (the `N-`/
  `U-` prefixes apply to "주식(J, NJ, UJ)" only). Corroboration: RANKLIST
  `InputBstpIscd` "코스피:1001 코스닥:2001" (D1 L426, D8 L46).
- **Index master route — USTOCKCOND (DP5):** request `InputMrktClsCode`
  "입력시장 구분코드로, 입력값은 "U" 고정입니다." and `InputCondMrktDivCode`
  "K: 코스피 Q: 코스닥 K2: Kospi200 KR: KRX" — but the example swaps them
  (§5.7 item 2). Response rows `Iscd` "종목코드" String 9, `KorIsnm` "한글종목명"
  String 40. The `K` example (DP4, 32 rows) lists: `1001` "코스피종합",
  `1002` "대형주", `1003` "중형주", `1004` "소형주", sectors `1005` "음식료·담배"
  … `1021` "금융", `1024` "증권", `1025` "보험", `1026` "일반서비스", `1027`
  "제조", `1045` "부동산", `1046` "IT서비스", `1047` "오락·문화", and `1053`,
  `1054`, `1163`, `1164` "코스피배당성장50".
- **Sector indices:** KOSPI sector codes appear only in the USTOCKCOND `K`
  example. KOSDAQ (`Q`), KOSPI200 (`K2`) and KRX (`KR`) sector lists are
  **not found** in these sources.
- **Constituents:** USTOCKCONDLIST `InputBstpIscd` "업종분류코드조회 API에서
  조회된 값 사용 ex. "1024"입력시 증권 업종 구성종목 조회", `InputCondMrktDivCode`
  ""UJ" 고정", sort `InputRankSortClsCode1` "2: 시가총액 DESC / 4: 현재가 DESC /
  12: 등락율 DESC / 13: 거래량 DESC / 42: 거래대금 DESC".

### 5.4 Current value response

| Concern | PRICE (DP5) | MULTIPRICE (DP5, DP4 index row) |
| --- | --- | --- |
| Value field | `Prpr` "현재가" String 16, no description | `Prpr`, same. Index example `"2588.72"` |
| Type / decimals | JSON string (`A0001`); decimals **not documented** | Example two decimals as a string |
| Previous close | `Sdpr` "기준가" | `Sdpr` `"2610.38"`. **Inference:** for an index, 기준가 = previous close: `2588.72 − 2610.38 = −21.66` = `PrdyVrss`. |
| Change / sign | `PrdyVrss` "전일대비", `PrdyCtrt` "전일대비율"; **no sign field** | Same; example `PrdyVrss` `"-21.66"` (signed), `PrdyCtrt` `"-0.83"` (= −21.66/2610.38, rounded) |
| OHLC | `Oprc`, `Hprc`, `Lprc`; `Mxpr`/`Llam` 상/하한가 | Same; index example `Mxpr` `""`, `Llam` `""` and `PrprVrss*Rate` `""` |
| Volume / value | `AcmlVol` "거래량", `AcmlTrPbmn` "거래대금" String 25; **units not documented** | **absent** |
| Name | none | `KorIsnm`; index example "코스피지수" |
| Time field | **none** (no date or time) | **none** |
| Envelope | `Out` typed `A0003` (object); example object | `Out` `A0002` (array) |

- **Envelope status:** root `rsp_cd`/`rsp_msg` (not in DP5); examples
  `"00000"` / "정상 처리 되었습니다.". D10 L82: "업무 성공은 rsp_cd ==
  '00000' 으로 확인한다". D11 L106–109 lists four `00000` messages,
  including "모의투자 데이터가 없습니다.".
- **UPTJJDAY rows** (daily, DP5/DP4): `Date`, `Prpr` (index example
  `"2548.86"`), `PrdyVrssSign` "전일대비부호" (no code list; example `"2"`),
  `PrdyVrss` `"2.56"`, `PrdyCtrt` `"0.10"`, `AcmlVol` `"454102"`,
  `AcmlTrPbmn` `"7803355"`, then 기관/외국인/개인 buy/sell quantity and amount.
  Units not documented. **Inference:** 천주 and 백만원 for the index row
  (magnitude only; weak).
- The only sign-code list near these routes is USTOCKCONDLIST (stock rows):
  "2: 상승 / 3: 보합 / 5: 하락".

### 5.5 Index candles

- **Routes:** CHARTTICK, CHARTMIN, CHARTDAY, CHARTWEEK, CHARTMONTH accept
  `U` per field table. **No index example exists**; every chart example is
  `J`/`005930`.
- **Intervals (DP5):** tick `InputDivXtick` "N Tick 입력 ex. 100"; minute
  `InputDivXtick` "30: 30초 / 60: 1분 / 600: 10분 / 3600: 60분 / [60*N:
  N분]"; day; week `InputPeriodDivCode` ""W""; month `InputPeriodDivCode`
  "M:월 / Y:년".
- **Range and count:** tick/minute `InputDate1` "조회 시작일을 YYYYMMDD 형식으로
  입력" and `dataCnt` "입력범위: "1" ~ "2000" ""(공백입력) 또는 "0" 입력시
  기본개수(400개)조회"; day/week/month `InputDate1`/`InputDate2` "YYYYMMDD
  (조회 시작일)" / "(조회 종료일)", no count.
- **Adjustment:** `InputOrgAdjPrc` "0:수정주가 미사용 / 1: 수정주가 사용",
  required on all five; effect on an index **not documented**.
- **Row fields:** `Hour` String 6, `Date` String 8, `Prpr`, `Oprc`,
  `Hprc`, `Lprc`, `CntgVol` "체결거래량" (tick/min/day/week); month has
  `AcmlVol` "누적체결거래량". No 거래대금, no change fields. Bar time
  convention (start/end) not documented.
- **Paging:** request/response headers `cont_yn`/`cont_key` (DP5; D10 L42).
  Rows per page beyond `dataCnt` not documented.
- **Row order:** not documented; all (stock) examples newest first.
- **History depth:** not documented.
- **Daily alternative:** UPTJJDAY gives a dated daily close and change for
  `U`/`1001` (example only; §5.7 item 1). No OHLC there.

### 5.6 Venue / calculation scope

- Index rows use market code `U` only. `NJ`/`UJ` and the `N-`/`U-` symbol
  prefixes are documented for stocks ("주식(J, NJ, UJ) 선택시"); no NXT or
  integrated index code is listed.
- The CHARTDAY/WEEK/MONTH `Prpr` note "UJ 통합시세 조회시 종가(현재가)는 KRX
  거래소 종가가 아닌, NXT 거래소 종가를 사용합니다." concerns stocks under `UJ`.
- Calculation source or publisher of the index values: **not found**.

### 5.7 Contradictions and gaps

1. **UPTJJDAY scope:** the field table lists `InputCondMrktDivCode`
   "주식&ETF:J / 주식(NXT): NJ / 주식(통합): UJ / ETN: EN / ELW: W" and stock
   codes only (also D1 L472–473), yet its own example and D6 L55–56 send
   `U`/`1001` and return index levels.
2. **USTOCKCOND parameter swap:** DP5 and D1 L713–714 put `"U"` in
   `InputMrktClsCode` and `K/Q/K2/KR` in `InputCondMrktDivCode`; the DP4
   example and D7 L38–39 send `"InputCondMrktDivCode": "U"`,
   `"InputMrktClsCode": "K"`. Unresolved.
3. **USTOCKCOND array name:** DP5 names the response array
   "입력조건시장분류코드"; the example uses `Out`.
4. **Truncated SDK docstrings:** D1 L176, L236 and D2 L72, L127, L180,
   L234, L288 end "업종(U) 선택시 지수코드: 1001: KOSPI 200..." — a cut of
   "1001: KOSPI / 2001: KOSDAQ". It reads as if `1001` were KOSPI 200. DP5 and
   D9 L59 give `1001` KOSPI and `3001` KOSPI200.
5. **Index name differs by route:** `1001` is "KOSPI" (DP5 list),
   "코스피지수" (MULTIPRICE example) and "코스피종합" (USTOCKCOND example).
6. **No timestamp** on PRICE or MULTIPRICE; a polled index value cannot be
   dated from the response.
7. **Stock chart examples disagree with their tables** (route-level, not
   index-specific): CHARTDAY table has `CntgVol`, its example `AcmlVol`;
   CHARTMIN example sends `InputDivXtick` `"600"` (10분) and `InputDate1`
   `20241202` but returns one-minute rows dated `20240205`; the required
   `InputOrgAdjPrc` is missing from the CHARTTICK/MIN/WEEK/MONTH examples.
8. **Code names:** `K001` "KOVIXI00" and `3907` "변동성지수" are verbatim;
   whether every route accepts them is not documented.

### 5.8 Gates and not-verified items

- Nothing live- or paper-verified. Whether PRICE and the chart routes really
  return index data for `U` has no publisher example.
- Not documented: decimals, volume/value units, time zone, bar-time
  convention, history depth, rows per page, `InputOrgAdjPrc` meaning for
  indices, the `PrdyVrssSign` code list on UPTJJDAY.
- The correct USTOCKCOND parameter placement (§5.7 item 2) needs a sanctioned
  check before a decoder or request plan relies on it.
- Demo support for index data is not stated (D4 ⭕ is per route).
- SDK `IGW00201` back-off retry (D11) is client policy, not adopted.

## 6. Toss Securities

### 6.1 Pinned sources

Public Toss portal documents, retrieved 2026-11-05 07:57:35–07:57:38 UTC.
All five copies have the same sha256 as the trade-evidence copies
(07:10–07:11Z). No broker API request was sent. `publisher guide` (T2, T4)
ranks below T1 `field table`; T4 L3 and T5 L16, L27 defer to T1.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | sha256 `c5918961335ccd6b`, 07:57:35Z; `openapi 3.1.0`, `info.version 1.2.28` | `tags[5]` "Market Indicators" (symbol catalog); `paths./api/v1/market-indicators/prices.get` (`getMarketIndicatorPrices`); `paths./api/v1/market-indicators/{symbol}/candles.get` (`getMarketIndicatorCandles`); `components.schemas.{MarketIndicatorPriceResponse,MarketIndicatorCandlePageResponse,MarketIndicatorCandle,Candle,ApiResponse,ErrorResponse}`; `components.responses.{RateLimitExceeded,InternalErrorMarketIndicators}`; `tags[6]` "Sector" |
| T2 | [overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md) | sha256 `bef057d9babe9a38`, 07:57:37Z | L4, L33 category text; L125–131 endpoint list; L236–238, L253–255, L264, L269 rate limits; L315–316 `unsupported-symbol` |
| T3 | [asyncapi.json](https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json) | sha256 `46669a360d4c5c64`, 07:57:36Z; `asyncapi 3.0.0`, `info.version 1.2.3` | Channel list (no index channel) |
| T4 | [faq.md](https://openapi.tossinvest.com/openapi-docs/faq.md) | sha256 `6ad4c02b8e785f7d`, 07:57:38Z | L3 precedence; no index Q&A (0 matches for "지수", "코스피", "KOSPI", "시장 지표"); L22 stock venue (not applied here) |
| T5 | [developers.tossinvest.com/llms.txt](https://developers.tossinvest.com/llms.txt) | sha256 `bbff77eaa55df248`, 07:57:38Z | L16, L27: T1 is the source of truth |

**Missing evidence:**

- No `1m` index candle example; only `1d` examples.
- No publisher client code for these routes.
- No paper/sandbox origin in T1.

### 6.2 Routes

Transport: `GET`, origin `https://openapi.tossinvest.com` (T1 `servers`),
`Authorization` Bearer token (`oauth2ClientCredentials`). No account header;
T1 `tags[5]`: "계좌와 무관한 정보로 토큰만으로 호출 가능합니다."

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Current value / candles / constituents | Evidence |
| --- | --- | --- | --- | --- | --- |
| "시장 지표 현재가 조회" — "시장 지표(국내 지수·국채)의 현재가를 조회합니다. 최대 200건 까지 다건 조회를 지원하며 콤마(`,`)로 구분합니다." | `GET /api/v1/market-indicators/prices` | `operationId getMarketIndicatorPrices` | Real origin only; no paper origin in T1 | Current value, batch | field table + publisher example (T1); publisher guide (T2 L129) |
| "시장 지표 캔들 차트 조회" — "시장 지표(국내 지수·국채)의 캔들(OHLCV) 차트 데이터를 조회합니다. 최대 200개 봉을 반환합니다." | `GET /api/v1/market-indicators/{symbol}/candles` | `operationId getMarketIndicatorCandles` | same | Candles (`1m`, `1d`) | field table + publisher example (T1); publisher guide (T2 L130) |

Constituents: **not found** for any index. Out of scope:

- `GET /api/v1/market-indicators/{symbol}/investor-trading`
  "투자자별 매매대금 조회" returns investor flows for "KRX 시장(코스피·코스닥)",
  not index values.
- The Sector group is "토스증권 자체 산업 분류인 섹터" (T1 `tags[6]`). It has
  constituents and period change rates (`changeRates`), but no index level
  or candles. It is not a 업종 index.
- WebSocket: **not found.** T3 channels are `realtime-trade`,
  `realtime-orderbook`, `realtime-order` and `realtime-conditional-order`.

### 6.3 Index identifiers

T1 `tags[5]` "심볼 카탈로그" (verbatim). "이 그룹의 모든 엔드포인트는 아래 **심볼
카탈로그**의 8종 심볼만 지원하며, 카탈로그에 없는 심볼은 400
`unsupported-symbol` 로 응답합니다."

| 심볼 | 명칭 | 자산 유형 | 표시 단위 | 비고 |
| --- | --- | --- | --- | --- |
| `KOSPI` | 코스피 | `INDEX` | 포인트 | 투자자별 매매대금 지원 |
| `KOSDAQ` | 코스닥 | `INDEX` | 포인트 | 투자자별 매매대금 지원 |
| `KR_BOND_2Y` | 한국 국채 2년 | `BOND` | % | 수익률(금리), 예: `3.25` = 3.25% |
| `KR_BOND_3Y` | 한국 국채 3년 | `BOND` | % | |
| `KR_BOND_5Y` | 한국 국채 5년 | `BOND` | % | |
| `KR_BOND_10Y` | 한국 국채 10년 | `BOND` | % | |
| `KR_BOND_20Y` | 한국 국채 20년 | `BOND` | % | |
| `KR_BOND_30Y` | 한국 국채 30년 | `BOND` | % | |

- KOSPI200, KRX100 and sector indices: **not found.**
- Format: plain names, not numeric codes. Pattern `^[A-Za-z0-9_,]+$`
  (`symbols`, prices) and `^[A-Za-z0-9_]+$` (`symbol`, candles).
- No market-division code and no list route. The catalog is static text;
  the 400 example's `data.allowedValues` lists the same eight symbols.
- T1 `tags[5]` says individual stocks use Market Data (`GET
  /api/v1/prices`, `/candles`).

### 6.4 Current value response

`result` is an array of `MarketIndicatorPriceResponse` (T1):

| Field | Type | Description (verbatim) | Example |
| --- | --- | --- | --- |
| `symbol` (required) | string | "시장 지표 심볼. `GET /api/v1/market-indicators/prices` 의 심볼 카탈로그 참조" | `"KOSPI"` |
| `timestamp` | string \| null, `date-time` | "데이터 시각. 데이터 미제공 시 null" | `"2026-06-11T15:30:00+09:00"` |
| `lastPrice` (required) | string, `decimal`, maxLength 30 | "현재가. 시장 호가 그대로이며, 통화·단위는 심볼 카탈로그를 따릅니다" | `"2812.45"`, KOSDAQ `"845.32"` |

- **Decimals:** not documented; examples two decimals. Unit "포인트" (T1
  catalog).
- **Change / sign / previous close / OHLC / volume / value:** **none.**
- **Envelope:** HTTP 200 `ApiResponse` (`result` required; "`result` 와
  `error` 는 동시에 나타나지 않습니다."). Errors `ErrorResponse`: 400
  `unsupported-symbol` "지원하지 않는 심볼입니다." and `invalid-request`
  (`symbols` count `min` 1, `max` 200); 429 `rate-limit-exceeded`; 500
  `InternalErrorMarketIndicators` `internal-error`.
- Response order relative to `symbols`, and duplicate handling: **not
  documented.**

### 6.5 Index candles

- `interval` (required) enum `1m`, `1d`: "`1m`(분봉)은 지수(`KOSPI`·
  `KOSDAQ`)만 지원하고, 국채(`KR_BOND_*`)는 `1d`(일봉)만 지원합니다." Bond
  `1m` → 400 `invalid-request`.
- `count` 1–200, default 100: "조회 봉 수 (최대 200)".
- **Paging:** `before` "페이지네이션 상한 (inclusive, ISO 8601). 이 시각과 같거나
  이전인 봉만 반환합니다. 미지정 시 가장 최신 봉부터 반환." with "`+` 는
  쿼리스트링에서 `%2B` 로 URL 인코딩해야 합니다". Response `nextBefore`
  "다음 페이지 조회 시 `before` 쿼리 파라미터에 그대로 전달. 마지막 페이지면
  null."
- **Order:** "최신순(`timestamp` 내림차순) 정렬 — 배열 첫 요소가 가장 최근 봉,
  마지막 요소가 가장 오래된 봉입니다." (field table).
- **Row:** `timestamp` "봉 시작 시각"; `openPrice`, `highPrice`, `lowPrice`,
  `closePrice` and `volume` "거래량", all decimal strings and required. No
  거래대금. `1d` examples are stamped `T09:00:00+09:00`
  (`"2026-06-11T09:00:00+09:00"`, close `"2812.45"`, volume
  `"542000000"`).
- **Volume unit:** not documented. **Inference:** shares, not 천주, from
  magnitude (weak).
- **Adjustment:** none mentioned (n/a for indices).
- **History depth and 1m session coverage:** not documented.

### 6.6 Venue / calculation scope

- No venue or calculation-source statement for index values. T4 L22
  ("KRX + NXT 통합 시세") answers "국내 캔들·체결" for stocks. It is not
  applied to indices here.
- The investor-trading route says "KRX 시장(코스피·코스닥)"; this concerns
  investor flows, not index calculation.

### 6.7 Contradictions and gaps

1. **Rate-limit group:** T2 L253–255 lists `MARKET_INDICATOR_PRICE` (10/s),
   `MARKET_INDICATOR` (10/s) and `MARKET_INDICATOR_CHART` (5/s). T1 tags
   the prices route `MARKET_INDICATOR` (shared with investor-trading) and the
   candle route `MARKET_INDICATOR_CHART`. No T1 route uses
   `MARKET_INDICATOR_PRICE`.
2. **Candle timestamp convention differs from stock candles:**
   `MarketIndicatorCandle.timestamp` is "봉 시작 시각", with daily bars at
   `09:00+09:00`. Stock `Candle.timestamp` says "`1m`: 봉 종료 시각. 해당 봉은
   `[timestamp - 1분, timestamp)` 구간의 체결을 집계합니다." and "`1d`: 해당
   거래일 (시각은 현지 자정 고정)". A shared decoder would mis-bucket one of
   them.
3. **Batch size vs catalog:** up to 200 `symbols` accepted, but only eight
   exist.
4. **Wording:** `lastPrice` "시장 호가 그대로" for an index, which has no
   order book.
5. **Example limit header:** `RateLimitExceeded` example
   `X-RateLimit-Limit: 10` vs `MARKET_INDICATOR_CHART` 5/s (T2 L255).
   **Inference:** generic example.
6. **OpenAPI version label:** T5 L16 says "OpenAPI 3.0"; T1 declares
   `3.1.0` (already noted in earlier evidence).

### 6.8 Gates and not-verified items

- Nothing live- or paper-verified. No `1m` example; bar boundary for `1m`
  index bars (start vs end, open/close auction placement) is unverified.
- Not documented: decimals, volume unit, history depth, behaviour outside
  trading hours (`timestamp` null case), response order in batch calls.
- Only KOSPI and KOSDAQ are offered. KOSPI200, KRX100 and sector indices
  need another source; there is none here.
- Rate limits are "운영 상황에 따라 사전 공지 없이 조정될 수" (T2 L238, L264);
  read `X-RateLimit-*` (T2 L269). The 429 back-off advice applies to these
  read-only GETs only.

## 7. Meritz Securities

### 7.1 Pinned sources

Portal export retrieved 2026-11-05 07:58:47Z. GitHub repository
[`meritz-securities/open-api@a93c6409db73ea97ad15f7b7186f36c9f32ecd89`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89)
(commit 2026-10-28T22:32:03+09:00; default-branch HEAD at 07:54:56Z). README
L11: "API 목록과 파라미터·응답 필드의 정본은 개발자 포털입니다." Repo content is
`publisher repo note` or `publisher client code`, ranked below M1.
Source ids are numbered M1–M8 in this file only; the trade and candle
evidence number the same repository files differently.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| M1 | Portal spec export [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json) (`title` "메리츠증권 Open API 명세") | 07:58:47Z sha256 `f36ecb02ee31730e`, 1,136,519 bytes, `generatedAt "2026-11-05 16:58:46"`. With `generatedAt` removed and `json.dumps(sort_keys=True, ensure_ascii=False)`: `2fff4f3e02d20cd5`, **identical** to the trade- and candle-evidence copies. | `groups[2]` "국내주식": `apis[27]` "국내지수 시세추이 조회", `apis[28]` "국내지수 시세추이 조회 (분봉)", `apis[29]` "국내지수 현재가 조회"; `groups[4]`/`groups[5]` WebSocket lists |
| M2 | [repo `openapi.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/openapi.json#L9250-L9855) | blob `93e900e66b965607d7fd8b8e14c6088d710e6fce` | L10 server; L9250–9399 days (`x-tr-id` L9398, `x-tps "10"` L9399); L9402–9563 minutes (L9562–9563); L9566–9855 prices (L9854–9855); overseas `x-tr-id` L16297, L16461, L16753 |
| M3 | [repo `examples/09_index.py`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/examples/09_index.py#L1-L19) | blob `778252ff923d47b1d7c0372ae0e82cf92ed757c6` | L6–7 unknown-code behaviour; L9 domestic code list; L14–15 seconds; L17–18 `888888`/`999999`; L49 `from`/`to` comment (publisher client code) |
| M4 | repo `meritz/data/catalog.json` | blob `000c2dbc636ad46077d4f46d67a04e0cd6fe1319` | L13636–13637, L13827–13828, L14029–14030 path + `tr_id` |
| M5 | [repo `docs/errors.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/docs/errors.md#L7-L9) | blob `b4b2eac6541bd2b886071c1caad17fa0c57ba3e6` | L7–9 all errors HTTP 500; L40 `0000` "정상 / 시세 계열"; L43 `5762` paging; L95 `EGW00200` |
| M6 | repo `llms.txt` | blob `8351d5343d785b61107179d19197c59a08e1edff` | L29 example index; L71–74 success codes; L120–121 rate limit |
| M7 | repo `README.md` | blob `61aa5f7f2c1059a29a99175a5cdf573996d81479` | L11 portal canonical; L125 "모의계좌는 없습니다" |
| M8 | repo `meritz/data/corrections.json` | blob `60370924e13233bbd2cccb517bfffee002dad915` | 0 entries for `market_index_*` |

Every M1 field description for the three routes appears verbatim in M2,
except `data` (absent in M2). So "최신 일자가 먼저 옵니다" is **portal-only**.
M2 also models `authorization` as `bearerAuth`.

**Missing evidence:**

- Only the KOSPI code `KGG01P` is in M1/M2; other codes are only in M3
  (publisher client code).
- No sector index codes, and no index master or constituents route.
- No paging statement for the index routes.
- The rate-limit notice board was not retrieved (see trade evidence §7.1).

### 7.2 Routes

Transport (M1, M2): `GET`, query string, origin
`https://openapi.imeritz.com:9443`; `contentType` "application/json;
charset=utf-8". Required headers: `authorization` and `mac_address`
("호출 단말의 MAC 주소입니다. 12자리로 넣습니다. 넣지 않으시면 요청이
거부됩니다."). The publisher sample fills this header automatically; that
code is deliberately not described or copied. M1 files request parameters
under "body"; its request examples and M2 use `in: query`. No paper
environment (M7 L125).

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Current value / candles / constituents | Evidence |
| --- | --- | --- | --- | --- | --- |
| "국내지수 현재가 조회" / TR "지수 현재가 조회 (국내)" | `GET /market/v1/index/prices` | `ohhts_1514_001r` | real only | Current value (one index per call) | field table + publisher example (M1); M2 |
| "국내지수 시세추이 조회" / TR "지수 시세추이 조회 (국내, 일-주-월-년봉)" | `GET /market/v1/index/candles/days` | `ohhts_1514_101r` | real only | Day/week/month/year candles | field table + publisher example (M1); M2 |
| "국내지수 시세추이 조회 (분봉)" / TR "지수 시세추이 조회 (국내, 분봉)" | `GET /market/v1/index/candles/minutes` | `ohhts_8001_002r` | real only | Intraday candles (seconds-based interval) | field table + publisher example (M1); M2 |

Constituents: **not found.** WebSocket index feed: **not found.** M1
`groups[4]` (domestic real-time) has stock price, order book, expected-price
and order-notice channels only. Its `antc_nmix_cls_code` "예상지수구분코드" is
a stock-feed field, not an index feed.

Rate: M2 `x-tps "10"` on all three; M5 L95 "`EGW00200` | 초당 호출 한도 초과 |
API 당 초당 10건입니다. 재시도 가능합니다"; M6 L120–121 (HTTP 500 +
`EGW00200`).

### 7.3 Index identifiers

- `iscd` (Y, String 12) on all three: "조회할 지수의 코드입니다. (예: 코스피
  KGG01P)" (M1, M2 example `KGG01P`).
- M3 L9 (publisher client code): "국내  KGG01P 코스피 · QGG01P 코스닥 · K2G01P
  코스피 200 · XGG01P KRX 100".

  | Index | Code | Source |
  | --- | --- | --- |
  | KOSPI | `KGG01P` | M1 field table, M2, M3 |
  | KOSDAQ | `QGG01P` | M3 only |
  | KOSPI200 | `K2G01P` | M3 only |
  | KRX100 | `XGG01P` | M3 only |
  | Sector indices | **not found** | — |

- Format: six alphanumerics, not the four-digit KRX-style codes used by DB.
  No market-division parameter on these routes.
- Index list/master route: **not found.**
- Unknown codes, M3 L6–7: "지수 코드는 종목코드와 다르다. 없는 코드를 넣어도
  오류가 나지 않고, 정상 응답(200 · rsp_cd 0000)에 모든 필드가 0 이거나 빈
  값으로 온다 — 이름이 비어 있으면 코드를 의심한다." (publisher client code).
  Not stated in M1.

### 7.4 Current value response

`data` (Object): "지수 현재가 정보입니다. 현재지수와 전일 대비 등락, 시가·고가·저가,
상승·하락 종목 수, 52주 최고·최저 지수가 한 건으로 내려옵니다." (M1).

| Concern | Field (M1) |
| --- | --- |
| Value | `stck_prpr` "현재지수" Number 13: "가장 최근 체결된 가격입니다." Example `2487.15` (JSON number). Decimals not documented. |
| Previous close | `prdy_clpr` "전일종가" Number 10: "전일 종가(전일 지수)입니다." Example `2471.50`. |
| Change | `prdy_vrss` Number 13: "전일 대비 변화량입니다. 부호는 prdy_vrss_sign으로 판단합니다." Example `15.65` (= 2487.15 − 2471.50). |
| Sign | `prdy_vrss_sign` String 2: "전일 대비 방향입니다. "2": 상승 "5": 하락 "3": 보합" |
| Rate | `prdy_ctrt` **String** 9 "전일 대비 등락률(%)입니다."; example JSON number `0.63` |
| OHLC + times | `oprc`/`oprc_hour`, `hprc`/`hgpr_hour`, `lprc`/`lwpr_hour` (times `HHMMSS`), plus `prdy_clpr_vrss_*` differences and `*_rate` (String) |
| Volume / value | `acml_vol` Number 19: "장 시작부터 지금까지 체결된 주식 수를 모두 더한 값입니다. 개별 체결 수량이 아닙니다."; `acml_tr_pbmn` Number 19: "장 시작부터 지금까지 체결된 거래대금을 모두 더한 값입니다." Example `512345678` / `8123456789000`. Value unit not stated; **Inference:** won (weak, magnitude). |
| Breadth | `tr_frmt_issu_cnt`, `ascn_issu_cnt`, `down_issu_cnt`, `stnr_issu_cnt`, `uplm_issu_cnt`, `lslm_issu_cnt` |
| 52-week | `52_week_hghs_nmix`, `52_week_hgpr_date`, `52_week_hgpr_rate`, `52_week_lwst_nmix`, `52_week_lwpr_date`, `52_week_lwpr_rate` |
| Date / time | `stck_last_tr_date` "가장 최근 거래가 있었던 일자(YYYYMMDD)입니다."; **no time of the current value** |
| Other | `kor_isnm` "지수의 한글 명칭입니다." (example "코스피"); `mtrt_date` "만기일" (example `""`) |
| Envelope | Not in the field table. Example: `"rsp_cd": "0000"`, `"rsp_msg": "정상 처리 되었습니다."`, `"tr_cont": "0"`. M5 L7–9: errors of any kind arrive as HTTP 500; "상태코드가 아니라 `rsp_cd` 로 가르십시오." M5 L40: `0000` "정상 / 시세 계열". |

### 7.5 Index candles

**Days route (`ohhts_1514_101r`):**

- `period_cls_code` (Y, String 2): "일봉 D · 주봉 W · 월봉 M · 연봉 Y 를
  넣습니다."
- **No date range or count parameter** in M1/M2 (§7.7 item 3).
- Rows (`data` "봉 배열입니다. 최신 일자가 먼저 옵니다."): `date`
  "해당 봉의 일자(YYYYMMDD)입니다. 월봉 조회에서는 마지막 행이 00000000 이고
  값이 모두 0인 빈 행으로 올 수 있습니다. 자료가 아니므로 제외하고 쓰십시오.";
  `prpr` "해당 봉의 종가(지수)입니다. 일봉은 그날의 마지막 지수이고, 주봉·월봉은
  그 기간의 마지막 거래일 지수입니다."; `oprc`/`hprc`/`lprc` (period first
  open, period max/min); `prdy_vrss_sign`, `prdy_ctrt`; `acml_vol`,
  `acml_tr_pbmn` "해당 봉 기간 동안 …".
- Example rows `20260928` (close `2487.15`) and `20260925` (close
  `2471.50`). These agree with the prices example's `prdy_clpr`.
  `tr_cont` `"0"`.

**Minutes route (`ohhts_8001_002r`):**

- `hour_cls_code` (Y, String 7) "봉 간격을 초 단위로 입력합니다. 60은 1분봉,
  300은 5분봉입니다. 반드시 넣으셔야 합니다."
- `from` / `to` (N, YYYYMMDD) "from과 함께 사용합니다."
- `past_data_incu_yn` (N) "과거 데이터 포함 여부입니다. "Y" 또는 "N" 을
  넣습니다." Its effect is not documented.
- Rows: `date`, `cntg_hour` "해당 봉의 체결 시각(HHMMSS)입니다. 888888,
  999999 처럼 시각이 아닌 값이 내려오는 행이 있습니다.", `prpr` "현재가입니다.",
  `oprc`, `hprc`, `lprc`, `cntg_vol` "해당 봉 구간의 체결 거래량입니다." No
  거래대금.
- M3 L17–18 (client code): "cntg_hour 가 888888 이면 장마감 행, 999999 이면
  시간외 행이다. 분봉이 아니므로 봉 계산에서는 뺀다." M3 L14–15: "1 이나 5 를
  넣으면 1초·5초 간격으로 읽혀 거의 비어 온다."
- Order: **not documented** ("분봉 배열입니다."; the example has one row).
  Whether `cntg_hour` is the bar start or end: not documented.

**Both routes:** rows per call and history depth not documented. Paging is
not documented for these routes. The generic code `5762` "다음 페이지 있음 …
`tr_cont`·`tr_cont_key` 로 이어 조회" (M5 L43, M6 L72–73) exists, but no
`tr_cont_key` parameter is listed here. Adjustment: n/a, not mentioned.

### 7.6 Venue / calculation scope

- No venue selector on the index routes (stock routes use `mrkt_div_code`
  J/NJ/TJ). No NXT-inclusive or integrated index is offered or mentioned.
- Calculation source: **not found.**
- `acml_vol` / `acml_tr_pbmn` scope (KRX only or including NXT): not
  documented.

### 7.7 Contradictions and gaps

1. **Type vs example:** `prdy_ctrt`, `tr_frmt_ctrt` and all `*_rate`
   fields are typed String, but the examples carry JSON numbers (`0.63`,
   `-4.43`). Decoders must accept both until verified.
2. **Envelope undeclared:** `rsp_cd`, `rsp_msg`, `tr_cont` appear only in
   examples, not in the index field tables.
3. **`from`/`to` on the days route:** M3 L49 says "from·to 는 선택이다. 기간으로
   조회할 때는 둘을 함께 넣는다." for the daily call, but M1/M2 define no
   `from`/`to` for `/market/v1/index/candles/days`. The overseas index days
   route has them.
4. **Shared TR ids with overseas routes:** domestic and overseas index
   prices both use `ohhts_1514_001r`, and both minute routes use
   `ohhts_8001_002r` (M2 L9562/L16461, L9854/L16753). Domestic days uses
   `ohhts_1514_101r`, overseas days `ohhts_8001_001r` (L16297).
   **Inference:** the backend tells domestic from overseas by code format.
5. **Example breadth inconsistency:** prices example `tr_frmt_issu_cnt` 820
   while `ascn_issu_cnt` + `down_issu_cnt` + `stnr_issu_cnt` = 540 + 310 +
   70 = 920. The values are illustrative.
6. **Stock-style wording:** `stck_prpr` "현재지수" is described as "가장 최근
   체결된 가격입니다."; `mtrt_date` "만기일" has no meaning for an index.
7. **Sign handling:** `prdy_vrss` description says the sign comes from
   `prdy_vrss_sign`. The trade-tick route's example carried a signed
   `prdy_vrss` (trade evidence §7.4). Whether index `prdy_vrss` is unsigned
   is unverified (the example is positive).
8. **Unknown codes return success** (M3 L6–7), so an empty `kor_isnm` is the
   only documented hint. This is client-code evidence, not M1.

### 7.8 Gates and not-verified items

- Nothing live-verified; no paper environment exists (M7 L125).
- Index codes other than `KGG01P` rest on publisher client code (M3).
  Sector index codes are absent.
- Not documented: decimals, volume/value units, time zone, minute-bar
  order and boundary, `past_data_incu_yn` effect, rows per call, paging,
  history depth.
- `mac_address` is a required header. Its value is a device identifier
  under AGENTS.md; automatic discovery is not an approved pattern.
- `EGW00200` is described as retryable (M5 L95); for these read-only GETs
  that is acceptable only under a bounded policy. The client throttling in
  M6 L121 is not adopted as a limit.

## 8. Cross-broker comparison

Cells cite the broker sections; evidence levels as in §1. "C only" means
the value rests on publisher client code alone.

### 8.1 Identifiers and code lists

| Concern | KIS | Kiwoom | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Code format | `U` + 4 digits (`FID_INPUT_ISCD`) | 3 digits `inds_cd` (+ `mrkt_tp` on `ka20001`/`ka20009`) | 3 digits `upcode`/`shcode` | `U` + 4 chars (`InputIscd1`; `K001` has a letter) | symbol name (`^[A-Za-z0-9_]+$`) | 6 chars `iscd` |
| KOSPI | `0001` | `001` | `001` | `1001` | `KOSPI` | `KGG01P` |
| KOSDAQ | `1001` | `101` | `301` | `2001` | `KOSDAQ` | `QGG01P` (C only) |
| KOSPI200 | `2001` | `201` | `101` | `3001` | not offered | `K2G01P` (C only) |
| KRX100 | `4001` (legacy only) | `701` | `501` | `0100` | not offered | `XGG01P` (C only) |
| Sector indices | via `idxcode.mst` | `ka10101` list (KOSPI example) | `t8424` list | KOSPI sectors in the `USTOCKCOND` example only | not offered | not found |
| Code-list route / file | `idxcode.mst` file (no REST list) | `ka10101` | `t8424` | `USTOCKCOND` | static 8-symbol catalog in T1 | not found |

**Code collisions.** The same string means different indices:

- `1001` is KOSDAQ at KIS but KOSPI at DB; `2001` is KOSPI200 at KIS but
  KOSDAQ at DB. Both brokers use `U` plus four digits, so the two formats
  look interchangeable and are not.
- `101` is KOSDAQ at Kiwoom but KOSPI200 at LS; `201` is KOSPI200 at
  Kiwoom, and LS uses `301` for KOSDAQ.
- `001` (Kiwoom, LS) and `0001` (KIS) both mean KOSPI.

A broker-native code is therefore not a portable identifier.

### 8.2 Values, time and change

| Concern | KIS | Kiwoom | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Current value type | not documented | decimal string with direction sign, e.g. `"-2394.49"` | `Number(10.2)` sent as JSON string | `Prpr` String 16, no description; example `"2588.72"` | `lastPrice` decimal string | `stck_prpr` Number 13 sent as JSON number |
| Chart value type / scale | not documented | **100× integer** strings ("소수점 제거 된 100배 값") | `Number(10.2)` as JSON string | `Prpr` etc. String; no index example | decimal strings | Number; JSON numbers in examples |
| Change sign | `prdy_vrss_sign` (codes undocumented) | `pred_pre_sig` 1–5; value also signed | `sign` (codes undocumented) | signed `PrdyVrss` on PRICE/MULTIPRICE, no sign field; `PrdyVrssSign` on UPTJJDAY (codes undocumented) | no change field | `prdy_vrss_sign` "2"/"5"/"3"; `prdy_vrss` sign "판단" from it |
| Previous close | none | none | `jniljisu` | `Sdpr` "기준가" (inference) | none | `prdy_clpr` |
| As-of time (current) | none | none (list `tm_n` "HHmmss", no date) | none (`opentime` etc. only) | none | `timestamp` ISO date-time with offset, nullable | none; `stck_last_tr_date` date only |
| Volume unit (current) | not documented | 1000주 | not documented | not documented | no volume on current | `acml_vol` shares ("주식 수") |
| Time zone stated | no | no | no | no | yes, offsets in values (`+09:00`) | no |

### 8.3 Candles

| Concern | KIS | Kiwoom | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Intraday | `FHKUP03500200`, `FID_INPUT_HOUR_1` seconds (30/60/600/3600) | `ka20005` 1–60분; `ka20004` 1–30틱 | `t8409` 30초 / n분; `t8408` n틱 | `CHARTMIN` seconds (30, 60, 600, 3600, 60×N); `CHARTTICK` N-tick | `1m` only (indices) | `hour_cls_code` seconds |
| Day / week / month / year | D/W/M/Y (`FHKUP03500100`) | `ka20006`/`07`/`08`/`19` | D/W/M (`t8429`); no year | D, W, M/Y | `1d` only | D/W/M/Y |
| Bar time field | `stck_bsop_date` (+ `stck_cntg_hour` intraday) | `dt`; `cntr_tm` "YYYYMMDDHHmmss" (tick), no format (minute) | `date` + `time` HHMMSS | `Date` + `Hour` | `timestamp` "봉 시작 시각"; `1d` stamped `09:00+09:00` | `date` + `cntg_hour` HHMMSS, with `888888`/`999999` rows |
| Start vs end of bar | not documented | not documented | not documented | not documented | **start** (field table) | not documented |
| Row order | newest first (C, inference) | newest first (E) | oldest first (E) | not documented; stock examples newest first | newest first (F) | days newest first (F, portal only); minutes not documented |
| Count / paging | `tr_cont` header; page size not documented | `cont-yn`/`next-key`; page size not documented | `qrycnt` ≤500 (≤2000 compressed) + `cts_date`/`cts_time` | `dataCnt` 1–2000 (default 400) for tick/min + `cont_yn`/`cont_key` | `count` ≤200 + `before`/`nextBefore` | not documented (days: no range or count input) |
| Adjustment input | none | none | none | `InputOrgAdjPrc` required; effect on an index not documented | none | none |

### 8.4 Fit with the existing models (Inference only)

The models in `src/ktradelink/models/` were read at `main`
`a5d2639e1b555b54c7a96652432cc2c3bf141fb7`; they are unchanged since
`7b7aa07`.

- **Inference — venue.** `Ticker` and `Candle` require `venue` in
  `{"KRX", "NXT", "BROKER_COMPOSITE"}` (`_validation.py` `_VENUES`). No
  index route at any of the six brokers takes or returns a venue, and no
  source states the calculating party or NXT inclusion (§2.6–§7.6).
  Labelling an index `KRX` would assert a scope the brokers do not
  document; `BROKER_COMPOSITE` would misdescribe an exchange-published
  index. A venue-free or "not-applicable" scope would be a model change.
- **Inference — symbol.** `validate_provenance` accepts `"0001"`,
  `"001"`, `"KOSPI"` or `"KGG01P"` (printable, no whitespace), but the
  same string means different indices at different brokers (§8.1), and
  ADR 0013 rejects any non-six-digit symbol (§9). Meritz's six-character
  codes are not digits either. A canonical index identifier and a
  per-broker mapping would be needed.
- **Inference — value and sign.** `validate_price` requires an unsigned
  finite `Decimal`. Two-decimal index values fit `Decimal`, but:
  Kiwoom current values carry a direction sign and its chart values are
  100× integers; DB `PrdyVrss` is signed with no sign field on PRICE;
  LS sends index values as JSON strings and Meritz as JSON numbers.
  Each needs a documented per-route rule, never a silent sign strip or a
  float parse (a JSON number must be read as `Decimal` from its text).
- **Inference — timestamp.** Only Toss gives a dated as-of time with an
  offset (`timestamp`, nullable). KIS, Kiwoom, LS, DB and Meritz give no
  dated time for the current value, so `Ticker.timestamp` must stay
  `None` for them; Kiwoom `tm_n`, LS `opentime` and Meritz `oprc_hour`
  are times without a date, and Meritz `stck_last_tr_date` is a date
  without a time.
- **Inference — volume.** `Ticker.volume`/`Candle.volume` are plain
  integers with no unit. Kiwoom's 1000주 vs 1주 split, Toss's decimal
  string, Meritz's shares and the undocumented KIS/LS/DB units mean an
  index volume cannot be stored without a unit decision.
- **Inference — fields without a home.** `Ticker.previous_close` can be
  filled only from LS `jniljisu`, Meritz `prdy_clpr` and (by inference)
  DB `Sdpr`. Breadth counts, 52-week/yearly ranges and sub-index values
  would go to `info` or a new type. `bid`/`ask` do not apply.
- **Inference — candles.** `Candle` accepts only `timeframe="1d"`,
  `session="regular"` and `adjustment` in `{"raw", "adjusted"}`.
  - Five brokers have no adjustment input on index charts; DB's
    `InputOrgAdjPrc` exists but its effect on an index is not documented.
    Neither label is documented for an index.
  - Weekly, monthly, yearly, minute, 30-second and tick bars are rejected
    by design.
  - `Candle.timestamp` must equal the Asia/Seoul midnight anchor of
    `session_date`. Toss daily index bars are stamped at `09:00+09:00`
    (bar start), so a Toss index bar would need its date mapped to the
    anchor and its native stamp kept separately (`source_timestamp`).
    Toss stock daily bars are already at local midnight (§6.7 item 2).
  - Meritz `00000000` monthly filler rows and `888888`/`999999` minute
    rows must be dropped before construction, per the publisher's own
    text, and would otherwise fail the OHLC or date checks.
- **Inference — overall.** Reusing `Ticker`/`Candle` for indices would
  require relabelling at least venue and adjustment, and a cross-broker
  identifier. A separate typed index value (or an explicit model
  extension) is a maintainer decision (§10.1).

## 9. Relation to existing repository documents

None of the files below is edited by this change. The differences are
recorded here only. Line numbers refer to `main`
`a5d2639e1b555b54c7a96652432cc2c3bf141fb7`.

| Document and claim | This audit |
| --- | --- |
| [ADR 0013](../decisions/0013-public-fetch-ticker-surface.md) L37: "`symbol` must be exactly six ASCII digits (`InvalidSymbol`)" | **Cannot express index codes.** KIS and DB use four characters (`0001`, `1001`), Kiwoom and LS three (`001`), Toss names (`KOSPI`), Meritz six alphanumerics (`KGG01P`). Any index method needs a new symbol rule or a separate identifier type (§10.1). |
| Same ADR L37–39: `venue` must be `"KRX"`; `NXT`/`BROKER_COMPOSITE` raise `UnsupportedCapability` | No index route at any of the six brokers has a venue (§2.6–§7.6); the ADR's venue rule has no index meaning. |
| [market-data spec](../specifications/market-data-v0.1-draft.md) §3 L60–62: six-digit stock symbol; do not "auto-guess ETFs/ETNs, indices, bonds or derivatives. Expand the instrument registry later." | **Consistent.** Index support needs that registry expansion first. Toss shows why: its index route also serves bond yields (`KR_BOND_*`, unit "%"), which the same registry decision must exclude or model (§6.3). |
| `src/ktradelink/models/_validation.py` `_VENUES` = `KRX`, `NXT`, `BROKER_COMPOSITE` | No value fits an index (§8.4). |
| [Capability inventory](capability-inventory-2026-11-05.md) rows 1–11 | **No index/sector row.** Index quotes are not inventoried there; this file is the first audit of them. |
| [Candle evidence](candle-evidence-2026-11-05.md) L816: Toss `GET /api/v1/market-indicators/{symbol}/candles` is "Out of equity scope … Its timestamp convention differs" | **Consistent** and made explicit here: index bars are stamped at bar start, `1d` at `09:00+09:00` (§6.5, §6.7 item 2). |
| Candle evidence L947–950: Meritz `GET /market/v1/index/candles/days` (`ohhts_1514_101r`) with `period_cls_code` D/W/M/Y is "not an equity route"; L1012–1015: `888888`/`999999` rows are documented for the index minute route only | **Consistent** with §7.5. The candle evidence does not cover the KIS, Kiwoom, LS or DB index chart routes (§2.5, §3.5, §4.5, §5.5). |
| [Trade evidence](trade-evidence-2026-11-05.md) §3.1 (Kiwoom re-pin to `c7a3d254`), §4.1 (LS L1 `9aaca437f1925115`), §5.1 (DB `564b5100`), §6.1 (Toss T1 `c5918961335ccd6b`), §7.1 (Meritz `a93c6409`, export digest `2fff4f3e02d20cd5`) | **Same pins** at this retrieval. Meritz source ids are numbered differently here (§7.1). |
| Symbol-master evidence (branch `claude/issue-17-symbol-master-evidence` @ `b127724ee73fac239d987a2fa2a5b889c5f92bfb`, not merged) L415: `upName` "업종명" as a stock attribute | No index master is covered there; KIS `idxcode.mst`, Kiwoom `ka10101`, LS `t8424` and DB `USTOCKCOND` are recorded here (§2.3, §3.3, §4.3, §5.3). |
| [six-broker-ticker-decoders.md](six-broker-ticker-decoders.md) | Equity ticker scope; this file does not widen it. |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any index decoder, request plan or public
index method is written. Broker tags are in brackets. Per-broker detail is
in §2.8, §3.8, §4.8, §5.8, §6.8 and §7.8.

### 10.1 Identity and model

- G-I1: choose a canonical index identifier and a per-broker mapping;
  ADR 0013's six-digit rule does not apply (§9). Broker-native codes
  collide, including KIS vs DB inside the same `U` + four-digit format
  (§8.1).
- G-I2: decide between a new typed index model and an extension of
  `Ticker`/`Candle`; venue and adjustment have no documented index value
  (§8.4). No dict/JSON public surface.
- G-I3: [Toss] decide whether bond-yield indicators (`KR_BOND_*`) that
  share the index routes are in scope; they must not be decoded as index
  points.

### 10.2 Value scale, type and sign

- G-I4: [Kiwoom] separate decoders for decimal current values and 100×
  chart values; [LS] read `Number(10.2)` from JSON strings; [Meritz] read
  JSON numbers as `Decimal` from their text, and accept both strings and
  numbers for String-typed `*_rate` fields until verified (§7.7 item 1);
  [KIS, DB] obtain types and decimals first. No float parsing.
- G-I5: [Kiwoom, LS, KIS, DB, Meritz] sign/direction codes are
  undocumented or partially documented; unknown codes (e.g. Kiwoom `43`)
  must fail closed, and no signed value may be silently made unsigned.
  [DB] PRICE has a signed `PrdyVrss` and no sign field. [Meritz]
  `prdy_vrss` takes its sign from `prdy_vrss_sign`; whether the value
  itself can be negative is unverified.

### 10.3 Codes and lists

- G-I6: [KIS] `idxcode.mst` offsets conflict (§2.7); [Kiwoom]
  `mrkt_tp`/`inds_cd` pairing undocumented for some codes; [LS]
  code-list source not stated per TR; [DB] `USTOCKCOND` parameter
  placement contradictory (§5.7 item 2) and the truncated SDK docstring
  reads as "1001: KOSPI 200" (§5.7 item 4); [Meritz] only `KGG01P` is in
  the portal, other codes are client code only, and unknown codes return
  success with empty fields (§7.3). Code lists must not be hard-coded
  from examples.

### 10.4 Time

- G-I7: [KIS, Kiwoom, LS, DB, Meritz] no dated as-of time on current
  values; `timestamp` stays `None` unless a dated field is documented.
  [Toss] `timestamp` is nullable ("데이터 미제공 시 null"). Only Toss
  states a zone (offsets in values).
- G-I8: bar time semantics: [Toss] index bars are bar **start** while
  Toss stock bars are bar **end** (`1m`) or local midnight (`1d`); a
  shared Toss candle decoder would mis-bucket one of them (§6.7 item 2).
  [KIS, Kiwoom, LS, DB, Meritz] start vs end not documented. [Meritz]
  `888888`/`999999` minute rows and `00000000` monthly filler rows must
  be excluded.

### 10.5 Candles and paging

- G-I9: row order differs by broker and is documented in a field table
  only by Toss and (portal-only) Meritz days (§8.3); page size and depth
  are not documented [KIS, Kiwoom, Meritz]; LS caps 500/2000, DB
  `dataCnt` ≤2000 (tick/min), Toss `count` ≤200. Continuation boundaries
  need fixtures. The KIS example continuation bug (§2.7 item 6) must not
  be copied. [Meritz] the days route has no range or count input, and the
  `from`/`to` in the publisher example is not in the spec (§7.7 item 3).
- G-I10: units of index volume/value [KIS, LS, DB, Toss] and the Kiwoom
  1000주/1주 split must be decided before any volume field is populated.
- G-I11: [DB] `InputOrgAdjPrc` is required on chart routes but its effect
  on an index is not documented; [DB] no index example exists for PRICE
  or any chart route, so `U` support there rests on the field table only.

### 10.6 Environment, venue and limits

- G-I12: paper support per route is not established [KIS, Kiwoom, LS,
  DB]; [Toss] no paper origin; [Meritz] real only ("모의계좌는 없습니다").
  No silent LIVE/PAPER fallback.
- G-I13: no NXT-inclusive or venue-specific index route was found at any
  broker; do not infer one from equity venue codes (DB `UJ`, Kiwoom
  `_NX`/`_AL`, LS `exchgubun`, Meritz `NJ`/`TJ`, Toss's KRX+NXT stock
  FAQ).
- G-I14: documented limits only [LS `t1511` 10, other 업종 TRs 1; DB
  PRICE 5, MULTIPRICE 2, CHART* 4, app 20; Toss 10/s prices, 5/s
  candles; Meritz 10/s per API]; the Toss rate-limit group names
  disagree (§6.7 item 1). No automatic retry beyond what a reviewed
  transport policy allows; the KIS backtester's automatic `EGW00201`
  retry (K17 L495–509), the DB SDK `IGW00201` back-off and Meritz's
  "재시도 가능" `EGW00200` note are publisher statements, not policy.
- G-I15: [Meritz] `mac_address` is a required header and a device
  identifier; automatic discovery is not an approved pattern (AGENTS.md).
- G-I16: [Meritz] domestic and overseas index routes share TR ids
  (`ohhts_1514_001r`, `ohhts_8001_002r`); a request plan must key on the
  path, not the TR id alone (§7.7 item 4).

## 11. Not verified

- Any live or paper response for any route above. No broker API request
  was sent.
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
- DB: whether PRICE and the chart routes return index data for `U` (no
  index example); decimals and units; `InputOrgAdjPrc` for indices;
  `PrdyVrssSign` codes; correct `USTOCKCOND` parameter placement; KOSDAQ,
  KOSPI200 and KRX sector lists; demo index data; bar-time convention,
  rows per page and depth.
- Toss: any `1m` index bar (no example) and its boundary; decimals and
  volume unit; history depth; behaviour outside trading hours (null
  `timestamp`); response order in batch calls.
- Meritz: index codes other than `KGG01P` (client code only); decimals
  and units; minute-bar order and boundary; `past_data_incu_yn`; rows per
  call, paging and depth; whether `prdy_vrss` can be negative; whether
  unknown codes really return success.
- Time zone, holiday, half-day and pre-open behaviour on every route
  (only Toss carries offsets).
- Whether any broker's index value or volume includes NXT trades.
- WebSocket feeds `H0UPCNT0` (KIS), `0J` (Kiwoom), `IJ_` (LS) and `U00`
  (DB) beyond their names; Toss and Meritz have no index feed in the
  pinned sources.
