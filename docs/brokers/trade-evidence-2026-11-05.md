# Six-broker trade-tick (체결) evidence — 2026-11-05

- **Scope:** domestic-equity REST routes that return recent executions
  (체결 내역, 시간대별 체결) for one symbol. Brokers: KIS, Kiwoom REST, LS,
  DB, Toss and Meritz. WebSocket execution feeds are out of scope; they are
  mentioned only where a WebSocket field table explains a REST field. The
  Shinhan comparison stays separate.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No KTradeLink trade decoder, request plan or public
  `fetch_trades` method exists, and this file does not authorize one.
- **No broker API request was sent.** No token, credential, account, MAC
  value or order was used. Only public Git repositories, public
  documentation pages and publisher JSON documentation endpoints were
  fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS and Kiwoom: fixed Git commits, fetched 07:00–07:17 with `git fetch`
    of the pinned SHA from `github.com`.
  - LS portal pages and JSON guides: 07:10:36–07:12:47 (§4.1).
  - DB portal JSON endpoints: 07:13:25–07:14:27; the DB SDK at a fixed
    commit (§5.1).
  - Toss portal documents: 07:10:32–07:11:21 (§6.1).
  - Meritz portal pages: 07:10:40–07:12:50; the Meritz repository at a
    fixed commit, cloned 07:13 (§7.1).
- **Re-hash before merge:** every sha256 prefix in §4–§7 and every Git
  blob SHA in §5.1 and §7.1 was recomputed from the retrieved copies
  before this file was assembled; all matched. Selected example
  arithmetic and quotations were re-checked against the same copies.
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
  - `publisher example`: a sample request/response or sample code.
  - `publisher client code`: SDK or helper behaviour. It shows how the
    publisher calls the route; it is **not** a contract.
  - `legacy publisher example`: sample code or Postman items under a
    publisher repository's `legacy/` directory. Older than the current
    examples, and lower weight than them.
  - `publisher guide`: portal prose outside the API specification or
    field tables (Toss overview and FAQ, §6.1; the LS FAQ, §4.3). It
    ranks below `field table`; the Toss FAQ itself defers to the API
    reference.
  - `publisher repo note`: non-code text in a publisher repository.
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- Sample values in publisher examples are illustrative. They are **not**
  authorized response fixtures.

## 1. Broker × property summary

Cell format: short verdict — evidence. `F` field table, `E` publisher
example, `L` legacy publisher example, `C` publisher client code, `N`
publisher repo note, `G` publisher guide, `—` not found.

| Property | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Route(s) | `FHKST01010300` GET `…/quotations/inquire-ccnl` 주식현재가 체결; `FHPST01060000` GET `…/quotations/inquire-time-itemconclusion` 당일시간대별체결; after-hours `FHPST02310000` `…/inquire-time-overtimeconclusion` — E | `ka10003` 체결정보요청; `ka10084` 당일전일체결요청; `ka10055` 당일전일체결량요청; all POST `/api/dostk/stkinfo` — F+E | `t8454` (통합) TPS 1; `t1301` TPS 2; `t1310` (분/틱, 당일/전일) TPS 2; all POST `/stock/market-data` — F+E | `CONCLUSION` POST `…/inquiry/hour-price`; `DAYTRADE` POST `…/inquiry/daily-price`; TPS 3 each — F+E+C | `GET /api/v1/trades` (`getTrades`) — F | `ohhts_1002_001r` GET `/market/v1/trades/ticks`; aggregate sibling `ohhts_1002_002r` `/trades/minutes` — F+E |
| Individual trade vs aggregate | **not documented** for any route. Legacy wording "체결 내역 30건" (L). Inference only. | `ka10003`: not stated; example cumulative deltas match each row's quantity (E, inference). `ka10084`: request selects `tic_min` "0:틱, 1:분" with **one** response table (F) — row type depends on the request. | not stated; t8454 example rows behave as single executions (E, inference); t1310 `timegb` "0:분 / 1:틱" selects the row type (F) | CONCLUSION: executions per publisher example-code prose (C), 19 of 20 example rows have `CntgVol` `"0"` (E); DAYTRADE: executions by example (E, inference) | individual (F field names; "체결 틱" only in G and WebSocket text) | ticks: individual, "해당 체결의 수량" (F+E); minutes: grouped, interval undocumented (F) |
| Timestamp / date in row | `stck_cntg_hour` "주식 체결 시간"; format not documented; **no date field** — E | `tm` / `cntr_tm` "HHmmss"; **no date field** — F | `chetime` String 10, `HHMMSS` in examples, **no date**; t1310 example has U+0000 inside (F+E) | `Hour` String 16, `HHMMSS` in examples, **no date** (F+E) | `timestamp` ISO-8601 date-time with offset, ms in examples; **date present** (F+E) | `prpr_hour` "체결 시각(HHMMSS)", **no date**, zone not stated (F) |
| Aggressor side | **none** on any route; `tday_rltv` "당일 체결강도" is a ratio, not a side — E | **not documented** for REST. Quantity is "부호가 포함된 숫자" (F) and examples carry `-` quantities (E); the meaning is documented **only** on WebSocket `0B` ("+는 매수체결,-는 매도체결", F). | **none per row**; day-cumulative `mdvolume`/`msvolume` "매도/매수체결수량" counters, assignment rule not documented (F); side only by differencing (inference) | CONCLUSION none; DAYTRADE per-row `ShnuCnqn` "매수체결량" / `SelnCnqn` "매도체결량", assignment rule not documented (F+E) | **none**; WebSocket text: "매수/매도 구분이 없고" (F, AsyncAPI) | **none**; `askp`/`bidp` "체결 시점의" quotes and `tday_rltv` only (F) |
| Trade id / sequence | none — E | none — F | none — F | none — F | none — F; WebSocket "sequence 필드는 제공되지 않습니다" | none — F |
| Pagination | `inquire-ccnl`: none. `itemconclusion`: time cursor `FID_INPUT_HOUR_1` "기준시간-이전체결처리" (L); boundary undocumented — E+L | `cont-yn` / `next-key` headers on all three (F); boundary undocumented. `ka10084` also `tm` HHMM (F). | body `cts_time` + headers `tr_cont`/`tr_cont_key` (F); FAQ on `cts_` keys (G); boundary undocumented | headers `cont_yn`/`cont_key` (F); body reused per page (C); boundary undocumented | **none**; `count` 1–50 (F); "과거 방향 페이지네이션 파라미터가 없어" (G) | **none**; "tr_cont_key)가 포함되지 않습니다" (F) |
| History depth / rows per call | `inquire-ccnl` "최근30건" (L); `itemconclusion` "당일" by title (E), "30건" (L) | rows per page not documented; `ka10084`/`ka10055` `tdy_pred` "당일 : 1, 전일 : 2" (F); `ka10003` not documented | t1310 "0:당일 / 1:전일" (F); t1301/t8454 not documented; page size not documented | not documented; page size not documented (examples 20 rows) | "당일 최근 체결", ≤50 (F+G) | latest ≤40, newest first (F); trading day not stated |
| Venue selector | `FID_COND_MRKT_DIV_CODE` "J:KRX, NX:NXT, UN:통합" on both regular routes (E); after-hours route "J:주식/ETF/ETN" only (E) | `stk_cd` suffix "KRX:039490,NXT:039490_NX,SOR:039490_AL" (F); per-row `stex_tp` "KRX , NXT , 통합" on `ka10003`/`ka10084` (F) | t8454/t1310 `exchgubun` "K: KRX / N: NXT / U:통합 / 그외 입력값은 KRX로 처리" (F); t1301 **none**; per-row `exchname` (F) | `InputCondMrktDivCode` `J`/`NJ`/`UJ` + `N-`/`U-` symbol prefix (F); no venue in rows | **none**; KRX + NXT 통합 시세, no per-row venue (G) | `mrkt_div_code` `J`/`NJ`/`TJ` (F); per-row `exch_code` only under `TJ` (F) |

## 2. KIS (Korea Investment & Securities)

### 2.1 Pinned sources

All sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362).
The full SHA is `3a9be59a3ed8745720dc3aa9d584bdf3b7830362` and the commit is
dated 2026-10-28T00:26:05+09:00. Paths are relative to the repository root;
`…/` stands for `examples_llm/domestic_stock/`.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | [`…/inquire_ccnl/inquire_ccnl.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_ccnl/inquire_ccnl.py) | `7d5ffdd673ce9da28a102fff4a0f8ec4a81b959f` | 주식현재가 체결 route, TR id, request fields. Same blob as the capability inventory's K2. |
| K2 | [`…/inquire_ccnl/chk_inquire_ccnl.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_ccnl/chk_inquire_ccnl.py) | `0f6592767d88eb57becbee18265967faf06f5482` | Response column names (L21–29) |
| K3 | [`…/inquire_time_itemconclusion/inquire_time_itemconclusion.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_itemconclusion/inquire_time_itemconclusion.py) | `7474386c075576d2f02e0fb86685be171eb43706` | 당일시간대별체결 route. Same blob as the capability inventory's K3. |
| K4 | [`…/inquire_time_itemconclusion/chk_inquire_time_itemconclusion.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_itemconclusion/chk_inquire_time_itemconclusion.py) | `52116f467bf61526b72f7d390eb972ba8847c397` | Response column names (L21–39), sample request (L65–70) |
| K5 | [`…/inquire_time_overtimeconclusion/inquire_time_overtimeconclusion.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_overtimeconclusion/inquire_time_overtimeconclusion.py) | `0dfdee115e260b3c6ef7850bf7e831654e3ac3a3` | 시간외시간별체결 route (after-hours single price) |
| K6 | [`…/inquire_time_overtimeconclusion/chk_inquire_time_overtimeconclusion.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_overtimeconclusion/chk_inquire_time_overtimeconclusion.py) | `04797ded24de2c13ba78a41c3a9e175aa264f063` | Its column names (L21–49) |
| K7 | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) | `0e722d6f3253033efe3cf2b99845397b2b329655` | Transport: method, headers, origins, `rt_cd`. Same blob as the candle audit's K9. |
| K8 | [`MCP/Kis Trading MCP/configs/domestic_stock.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/configs/domestic_stock.json) | `e82a0829ef519c64dfecb3e966ed217b4fcd3805` | Publisher registry, L301–366. Parameter descriptions repeat K1 and K3. K5 is not registered. |
| K9 | [`examples_user/domestic_stock/domestic_stock_functions.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_user/domestic_stock/domestic_stock_functions.py) | `e585487d112409af59a64ad135cfc9440b266e72` | L3973–4030 and L6821–6890 repeat K1 and K3 (same TR ids, params, outputs) |
| K10 | [`legacy/Sample01/kis_domstk.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/Sample01/kis_domstk.py) | `0090f06c540fadc0b87a1e9515ab4c098e3aa9c2` | **Legacy** comments on row count and the time cursor (L919, L1135–1136, L1159, L1176) |
| K11 | [`legacy/postman/실전계좌_POSTMAN_샘플코드_v2.6.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/postman/%EC%8B%A4%EC%A0%84%EA%B3%84%EC%A2%8C_POSTMAN_%EC%83%98%ED%94%8C%EC%BD%94%EB%93%9C_v2.6.json) | `a73d6bfab94ddfbf94af8db8de4c9e50ef040e58` | **Legacy** real-account Postman items (L3102, L3164, L3169, L3582, L3650–3660, L3668) |
| K12 | [`legacy/postman/모의계좌_POSTMAN_샘플코드_v1.6.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/postman/%EB%AA%A8%EC%9D%98%EA%B3%84%EC%A2%8C_POSTMAN_%EC%83%98%ED%94%8C%EC%BD%94%EB%93%9C_v1.6.json) | `03833e4af7258d1d85b76f298af3928be2748ea0` | **Legacy** paper-account Postman items (L486, L529, L1131, L1178) |
| K13 | [`…/ccnl_krx/chk_ccnl_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/ccnl_krx/chk_ccnl_krx.py) | `603e540e1d9dd54a3e06b7a50ffb938fac12fb1f` | WebSocket `H0STCNT0` column names, context only (§2.5) |

**Missing evidence:**

- None of K1–K13 contains a KIS field table: no JSON types, lengths,
  units or sign-code lists for these routes.
- None contains a sample response body (the legacy Postman items have no
  saved responses).
- The KIS developer-portal specification was **not** retrieved for this
  audit.
- Every response-side statement below is therefore limited to column
  *names* and their Korean labels.

### 2.2 Routes

All three routes are `GET` with query parameters: K7 L476 calls
`requests.get(url, headers=headers, params=params)` because none of K1, K3
or K5 sets `postFlag`. The origins are the K7 L152 and L154 comments:
`https://openapi.koreainvestment.com:9443` (실전) and
`https://openapivts.koreainvestment.com:29443` (모의).

| Route (title in source) | Path | TR id | Real / paper | Row = trade or aggregate? | Evidence |
| --- | --- | --- | --- | --- | --- |
| "[국내주식] 기본시세 > 주식현재가 체결[v1_국내주식-009]" (K1 L18) | `/uapi/domestic-stock/v1/quotations/inquire-ccnl` (K1 L22) | `FHKST01010300` for `real` and `demo` (K1 L56–59) | same TR id both; legacy paper Postman item exists (K12 L486, L529) | **not documented**; K1 L30 says only "종목의 체결 정보를 확인할 수 있습니다" | publisher example |
| "[국내주식] 기본시세 > 주식현재가 당일시간대별체결[v1_국내주식-023]" (K3 L19) | `/uapi/domestic-stock/v1/quotations/inquire-time-itemconclusion` (K3 L23) | `FHPST01060000` for `real` and `demo` (K3 L63–66) | same TR id both; legacy paper item (K12 L1131) | **not documented**; "시간대별" in the title vs "체결 내역 30건" in legacy K10 L1136 | publisher example |
| "[국내주식] 기본시세 > 주식현재가 시간외시간별체결[v1_국내주식-025]" (K5 L19) | `/uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion` (K5 L23) | `FHPST02310000` for `real` and `demo` (K5 L63–66) | same TR id both | **not documented** | publisher example |

Request headers (names only, K7 L61–66, L266–268, L457–459):

- `Content-Type`, `Accept`, `charset`, `User-Agent`;
- `authorization`, `appkey`, `appsecret`;
- `tr_id`, `custtype`, `tr_cont`.

K7 L453–455 rewrites a leading `T`, `J` or `C` to `V` in paper mode. All
three TR ids start with `F`, so the samples send the same id in both
environments.

The third route is limited to the after-hours single-price session (its
`FID_HOUR_CLS_CODE` is "1: 시간외", K5 L29). It is recorded for
completeness; it is not a general trade-tick route.

### 2.3 Request fields

| Concern | `inquire-ccnl` (K1) | `inquire-time-itemconclusion` (K3) | `inquire-time-overtimeconclusion` (K5) |
| --- | --- | --- | --- |
| Symbol | `FID_INPUT_ISCD` "[필수] 입력 종목코드 (ex. 123456)" (K1 L27); K2 L56 sends `"005930"` | `FID_INPUT_ISCD` "[필수] 입력 종목코드" (K3 L28); K4 L68 sends `"005930"` | `FID_INPUT_ISCD` "(ex. 123456(ETN의 경우 Q로 시작 Q500001))" (K5 L28) |
| Venue | `FID_COND_MRKT_DIV_CODE` "J:KRX, NX:NXT, UN:통합" (K1 L26) | same three codes (K3 L27) | "(ex. J:주식/ETF/ETN)" only (K5 L27); NX/UN **not documented** |
| Time cursor | none | `FID_INPUT_HOUR_1` "[필수] 입력 시간1" (K3 L29); no format in K3. Legacy: "기준시간-이전체결처리 (6자리)" (K11 L3660) and "기준시간 (6자리; HH:MM:SS) ex) 155000 입력시 15시 50분 00초 기준 이전 체결 내역이 조회됨" (K10 L1159) | none |
| Date | none | none | none |
| Session | none | none | `FID_HOUR_CLS_CODE` "[필수] 적립금구분코드 (ex. 1: 시간외)" (K5 L29); see §2.7 |
| Page size | none | none | none |
| Continuation | Sample sends `tr_cont=""` (K1 L68). No continuation key is documented. | Sample sends `tr_cont=""` (K3 L76). The only documented cursor is `FID_INPUT_HOUR_1`. | Sample sends `tr_cont=""` (K5) |

- **Inference:** `FID_INPUT_HOUR_1` is `HHMMSS`, from the sample value
  `"115959"` (K4 L69) and the legacy description (K10 L1159).
- K3 L59–60 rejects an empty `FID_INPUT_HOUR_1`. The legacy helper fills
  the current client clock instead (K10 L1145–1154), and its comment says
  "시간 미지정시 현재시각 기준" (K10 L1136). Whether the server accepts an
  empty value is **not documented** in the current examples.

### 2.4 Response

| Concern | `inquire-ccnl` (K1/K2) | `inquire-time-itemconclusion` (K3/K4) | `inquire-time-overtimeconclusion` (K5/K6) |
| --- | --- | --- | --- |
| Envelope | `rt_cd`; K7 L353 treats `rt_cd == "0"` as OK. `msg_cd`, `msg1` (K7 L322–323). HTTP status other than 200 is an error (K7 L478–485). | same | same |
| Row array | `output`, passed straight to `pd.DataFrame` (K1 L71). Array-ness **inferred** from that call. | `output2` (K3 L83); `output1` is one object (K3 L80) | `output2` (K5 L83); `output1` object (K5 L80) |
| Time | `stck_cntg_hour` "주식 체결 시간" (K2 L22) | `stck_cntg_hour` "주식 체결 시간" (K4 L29) | `stck_cntg_hour` "주식 체결 시간" (K6 L40) |
| Date | **none** | **none** | **none** |
| Price | `stck_prpr` "주식 현재가" (K2 L23) | `stck_pbpr` labelled "주식 현재가" (K4 L30); `stck_prpr` also labelled "주식 현재가" (K4 L22). Which field is per row is **not documented** (§2.7). | `stck_prpr` "주식 현재가" (K6 L41) |
| Quantity | `cntg_vol` "체결 거래량" (K2 L26) | `cnqn` "체결량" (K4 L38) | `cntg_vol` "체결 거래량" (K6 L48) |
| Side / aggressor | **none** | **none** | **none** |
| 체결강도 | `tday_rltv` "당일 체결강도" (K2 L27) | `tday_rltv` "당일 체결강도" (K4 L36) | none |
| Best quotes | none | `askp` "매도호가", `bidp` "매수호가" (K4 L34–35) | `askp`, `bidp` (K6 L45–46) |
| Change / sign | `prdy_vrss` "전일 대비", `prdy_vrss_sign` "전일 대비 부호", `prdy_ctrt` "전일 대비율" (K2 L24–28) | same names (K4 L23–25, L31–33) | same names (K6 L42–44) |
| Cumulative volume | none | `acml_vol` "누적 거래량" (K4 L26, L37) | `acml_vol` (K6 L47) |
| Trade id / sequence | none | none | none |
| JSON types / units | **not documented** | **not documented** | **not documented** |
| Sign-code list | **not documented** for this route | **not documented** | **not documented** |
| Ordering | **not documented** | **not documented** | **not documented** |

The only `prdy_vrss_sign` code list found in the pin is a legacy comment on
a **different** route, 주식현재가 투자자 (`inquire-investor`): "1 : 상한,
2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락" (K10 L1025). It is not evidence for
the trade routes.

### 2.5 Semantics

- **Individual trade vs aggregate:** not documented for any of the three
  routes.
  - The current examples describe `inquire-ccnl` only as "체결 정보"
    (K1 L30).
  - The `itemconclusion` title says "시간대별체결" (by time band), while the
    legacy comment says "기준시각(HHMMSS) 이전 체결 내역 30건 조회됨"
    (K10 L1136) and calls the quantity column `cnqn` "체결량".
  - **Inference:** rows are probably individual executions with a
    one-second time label. This is not evidence; a fixture must prove it.
- **Time:** `stck_cntg_hour` has no documented format.
  - **Inference:** `HHMMSS`, like the cursor.
  - Time zone: **not documented**.
  - No row or envelope field carries a date on any route. The trading date
    must come from elsewhere (spec §5).
- **History depth:**
  - `inquire-ccnl`: the legacy Postman items are named
    "J_주식현재가 체결(최근30건)" (K11 L3102) and
    "V_주식현재가 체결(최근30건)" (K12 L486); the legacy helper says
    "(최근체결 건 30건만 조회)" (K10 L919). The current example (K1) states
    no count.
  - `itemconclusion`: "당일" in the title (K3 L19) points to today only.
    Legacy: "이전 체결 내역 30건" per call (K10 L1136).
  - Neither route has a documented date input, so neither is documented
    to return a previous session.
- **Ordering:** not documented. No sample response exists.
- **Sessions:**
  - `J`/`NX`/`UN` select KRX, NXT and 통합 on the two regular routes.
    Which sessions (pre-market, single-price auctions, after-hours) each
    code includes is **not documented**.
  - After-hours single-price executions have their own route (K5).
    Whether they also appear in `inquire-ccnl` or `itemconclusion` is
    **not documented**.
- **Aggressor side:** no REST route here has a side field.
  - For context only: the WebSocket feed `H0STCNT0` lists `CCLD_DVSN`
    "체결구분" (K13 L46), with no value list in K13. That field is **not**
    available on these REST routes and its codes are not documented here.
  - `tday_rltv` "당일 체결강도" is a day-level ratio. It must not be read as
    a per-trade side.

### 2.6 Limits

- Rows per call: no current source states one. Legacy sources say 30 for
  both regular routes (§2.5).
- Rate limits: not documented in K1–K13.
- Paper support: TR ids are identical for `real` and `demo` (K1 L56–59,
  K3 L63–66, K5 L63–66), and the legacy paper Postman collection lists the
  first two routes (K12). Entitlement is not verified.

### 2.7 Contradictions and inferences

1. **Docstring venue example outside the documented codes.** K3 L44 shows
   `inquire_time_itemconclusion("real", "U", "0001", "115959")`. `U` is not
   among "J:KRX, NX:NXT, UN:통합" (K3 L27), and `0001` is not a six-digit
   stock code. K9 repeats it. The runnable sample K4 L65–70 uses
   `J`/`005930`. **Inference:** the docstring is copied from an index
   route. It is not adopted.
2. **Ambiguous `output1`/`output2` split.** K4's `COLUMN_MAPPING`
   (L21–39) merges both outputs into one dict and repeats `prdy_vrss`,
   `prdy_vrss_sign`, `prdy_ctrt` and `acml_vol`.
   - **Inference:** the first block (L22–28: `stck_prpr` … `prdy_vol`,
     `rprs_mrkt_kor_name`) is `output1`, and the second block (L29–38:
     `stck_cntg_hour`, `stck_pbpr`, …, `cnqn`) is `output2`.
   - Under that inference the per-row price is `stck_pbpr`, labelled
     "주식 현재가" like `stck_prpr`. Its meaning is unconfirmed.
3. **Mislabelled session parameter.** K5 L29 labels `FID_HOUR_CLS_CODE` as
   "적립금구분코드" (reserve-fund code). The legacy Postman item calls it
   "시간구분코드 (1:시간외)" (K11, item at L3668). The value `1` agrees.
4. **Venue codes differ by source age.** The legacy Postman items document
   only "J : 주식, ETF, ETN / W: ELW" (K11 L3164, L3650). The current
   examples document `J`/`NX`/`UN` (K1 L26, K3 L27). The current examples
   are preferred; `W` (ELW) is out of scope.
5. **Optional vs required cursor.** Legacy K10 L1136 says an empty time
   means "현재시각 기준"; K3 L59–60 requires it (§2.3).
6. **Copy-pasted legacy comment.** K10 L1176 repeats the
   `itemconclusion` comment "기준시각(HHMMSS) 이전 체결 내역 30건 조회됨"
   above a different function (시간외일자별주가). Legacy comments are
   therefore weak evidence even for row counts.
7. **No field table or response example** exists in the pinned sources.
   JSON types, string vs number, signs and units are all unknown.

## 3. Kiwoom REST

### 3.1 Pinned sources

All sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@c7a3d254`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/c7a3d25449ed4b4238bef378780c41103c67b9e9).
The full SHA is `c7a3d25449ed4b4238bef378780c41103c67b9e9`, the commit is
dated 2026-09-15T15:12:16+09:00, and it was the only branch head
(`refs/heads/main`, also `HEAD`) in `git ls-remote` at retrieval.

**Re-pin from `953e5dbf`.** Earlier audits pinned
`953e5dbff123f437ab4d11a78a95191a685eb51f`. At retrieval:

- `953e5dbf` is not a branch head. It could still be fetched by SHA.
- Both commit objects name the **same tree**,
  `4eb7d5497f4155ace73d8d37a03f3dc18abbe6fa`, and carry the same commit
  date and subject. Their parents differ (`234560d2…` for `953e5dbf`,
  `66bebb00…` for `c7a3d254`), i.e. the history was rewritten.
- Identical trees mean every path has the same blob SHA under both
  commits. Blob pins from the earlier audits (for example the spec
  `15ee3a91…` and the Postman collection `88138bd9…`) therefore remain
  valid, and are re-anchored here on the reachable commit.

In the links, `…/종목정보/` stands for
`examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/`
(`examples/국내주식/종목정보/`).

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field tables** and examples: `apis["체결정보요청(ka10003)"]` (L2305–2546), `apis["당일전일체결량요청(ka10055)"]` (L17668–17879), `apis["당일전일체결요청(ka10084)"]` (L24480–24751), `apis["주식체결(0B)"]` (L96908; context only), `error_codes` (L107018) |
| W2 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | PRD items L3691 (`ka10003`), L5370 (`ka10055`), L5817 (`ka10084`); MOCK items L37228, L38907, L39354. Each PRD/MOCK description equals the W1 table. |
| W3 | [`…/종목정보/get_domestic_stock_execution_info.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_execution_info.py) | `434fbc6f8d618844c5540e67b7f9a8e25358f8ac` | `ka10003` example client |
| W4 | [`…/종목정보/get_domestic_today_prev_trades.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_today_prev_trades.py) | `2d65a1c65f60b562623e2fa740555dca0a270f4f` | `ka10084` example client |
| W5 | [`…/종목정보/get_domestic_today_prev_trade_volume.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_today_prev_trade_volume.py) | `63be5528e30e51b100515696d2f21a4c1a51d48a` | `ka10055` example client |
| W6 | [`kiwoom/core/client.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/client.py) | `52d915c9e2f38f21885efbc428d3b50593a452c9` | Publisher client code: headers, `return_code`, continuation |
| W7 | [`kiwoom/core/errors.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/errors.py) | `dd7a8709bccd8a28601c49d26a298d3c92f34e5d` | `normalize_return_code` (L30–36), `RATE_LIMIT_CODES` (L183) |

### 3.2 Routes

All three routes (W1 meta, identical in W2):

- `POST /api/dostk/stkinfo`, `Format` `JSON`, `Content-Type`
  `application/json;charset=UTF-8`; menu "국내주식 > 종목정보".
- Origins: "운영 도메인" `https://api.kiwoom.com` and "모의투자 도메인"
  `https://mockapi.kiwoom.com`. W2 lists each route under both `PRD` and
  `MOCK(모의투자)`. That shows the publisher *offers* them in both
  environments; error `8104` "모의투자에서 지원하지 않는 API 입니다." (W1
  `error_codes`) shows mock support is not guaranteed per API.
- Required request headers: `api-id` "7자리 TR코드", `authorization`
  "토큰 지정시 토큰타입("Bearer") 붙혀서 호출". Optional: `cont-yn`,
  `next-key`. W6 L46 also sends `Content-Type`.

| API ID / name | Overview (verbatim) | Row array | Row = trade or aggregate? | Evidence |
| --- | --- | --- | --- | --- |
| `ka10003` 체결정보요청 | "종목 코드로 체결 정보를 조회합니다." | `cntr_infr` "체결정보" LIST | **not documented**; example consistent with one execution per row (§3.5) | field table + example |
| `ka10084` 당일전일체결요청 | none in meta | `tdy_pred_cntr` "당일전일체결" LIST | **request-dependent**: `tic_min` "0:틱, 1:분"; the response table does not say how a minute row differs | field table + example |
| `ka10055` 당일전일체결량요청 | none in meta | `tdy_pred_cntr_qty` "당일전일체결량" LIST | **not documented**; example has two rows with the same second (§3.7) | field table + example |

### 3.3 Request fields (W1; identical in W2)

| Concern | `ka10003` | `ka10084` | `ka10055` |
| --- | --- | --- | --- |
| Symbol + venue | `stk_cd` String(20) Y: "거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)" | same | same |
| Day | none | `tdy_pred` String(1) Y: "당일 : 1, 전일 : 2" (L24553) | `tdy_pred` String(1) Y: "1:당일, 2:전일" (L17741) |
| Tick / minute | none | `tic_min` String(1) Y: "0:틱, 1:분" (L24563) | none |
| Time cursor | none | `tm` String(4) **N**: "조회시간 4자리, 오전 9시일 경우 0900, 오후 2시 30분일 경우 1430, 빈값('') 입력 시 현재시간으로 자동 설정" (L24573) | none |
| Page size | none | none | none |
| Continuation | request headers `cont-yn` (len 1) and `next-key` (len 50): "응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 [next-key값] 세팅" | same | same |

- The body is JSON (W6 L57 sends `json=body`).
- The examples resend the **same body** on continuation and pass only the
  two headers (W3 L128–161; W4 L145–178; W5 L127–160).
- Whether `tm` selects rows at, before or after `HHMM` is **not
  documented**, and so is its interaction with `next-key`.
- W2 copies body fields into the query string
  (`{{PRD}}/api/dostk/stkinfo?stk_cd=005930&tdy_pred=1&tic_min=0`). W1 and
  W6 send JSON bodies only; the query-string copy is not adopted.

### 3.4 Response (W1 field tables; examples in W1 `response_example`)

| Concern | `ka10003` (`cntr_infr`) | `ka10084` (`tdy_pred_cntr`) | `ka10055` (`tdy_pred_cntr_qty`) |
| --- | --- | --- | --- |
| Envelope | `return_code` (example `0`, JSON number), `return_msg`. Not in the field table. W6 L104: "키움은 업무 오류도 HTTP 200으로 내려보내고 실패 여부는 본문 return_code에만 담는다." | Example uses **`returnCode`** / **`returnMsg`** (L24751), not `return_code` | `return_code`, `return_msg` (example) |
| Continuation (response headers) | `cont-yn` "다음 데이터가 있을시 Y값 전달"; `next-key` "다음 데이터가 있을시 다음 키값 전달" | same | same |
| Time | `tm` "시간" "HHmmss" (L2424) | `tm` "시간" "HHmmss" (L24629) | `cntr_tm` "체결시간" "HHmmss" (L17797) |
| Date | **none** | **none** | **none** |
| Price | `cur_prc` "현재가" "단위: 원, 부호가 포함된 숫자" | same | `cntr_pric` "체결가" "단위: 원, 부호가 포함된 숫자" |
| Quantity | `cntr_trde_qty` "체결거래량" "단위: 1주, 부호가 포함된 숫자" (L2484) | same text (L24689) | `cntr_qty` "체결량" "단위: 1주" — **no sign stated** (L17847) |
| Side / aggressor | **not documented** (see quantity sign, §3.5) | same | same |
| 체결강도 | `cntr_str` "체결강도" "단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율" | same | none |
| Best quotes | `pri_sel_bid_unit` "우선매도호가단위", `pri_buy_bid_unit` "우선매수호가단위", both "단위: 원, 부호가 포함된 숫자" | same | none |
| Change / sign | `pred_pre` "전일대비" (원, signed), `pre_rt` "대비율" (%, signed), `sign` "1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락" | same; `sign` 한글명 "전일대비기호" | `pred_pre_sig` (same five codes), `pred_pre`, `flu_rt` "등락율" |
| Cumulative volume | `acc_trde_qty` "누적거래량" "단위: 1주" | same | same |
| Cumulative value | `acc_trde_prica` "누적거래대금" "단위: **원**" (L2514) | "단위: **백만원**" (L24719) | "단위: **백만원**" (L17867) |
| Venue per row | `stex_tp` "거래소구분" "KRX , NXT , 통합" (L2534) | same (L24739) | none |
| Trade id / sequence | none | none | none |
| JSON types | all `String` in the table; example values are JSON strings | same | same |
| Ordering | not documented; example `tm` 130429, 130153, …, 124507 (newest first) | not documented; example 112711, 111554 | not documented; example 171945, 154626, 154626, 154357 |

### 3.5 Semantics

- **Individual trade vs aggregate:**
  - None of the three tables says whether a row is one execution.
  - `ka10003` example: for each pair of adjacent rows, the newer
    `acc_trde_qty` minus the older one equals the newer row's
    `cntr_trde_qty` (8735−7725 = 1010, 7725−7269 = 456, 7269−6269 = 1000,
    6269−6267 = 2, 6267−6265 = 2). The same holds for `acc_trde_prica` and
    price × quantity (e.g. 524269500−470234500 = 1010 × 53500).
    **Inference:** example rows are consecutive single executions. Example
    values are illustrative, so this is not a contract.
  - `ka10084` with `tic_min=1` ("분") returns minute rows under the same
    field names. Whether `tm`, `cur_prc` and `cntr_trde_qty` then mean the
    minute's label, last price and summed volume is **not documented**.
- **Time:** `HHmmss` without a date on all three routes. Time zone:
  **not documented**. For `ka10084`/`ka10055` with `tdy_pred=2`, the rows
  belong to the previous trading day, but no row carries that date.
- **History depth:**
  - `ka10084` and `ka10055`: today or the previous day (`tdy_pred`). No
    other date can be requested.
  - `ka10003`: no day input; depth **not documented**.
  - How far continuation reaches within a day is **not documented**.
- **Ordering:** every example lists the newest row first. The tables do
  not state an order. **Inference:** newest first.
- **Sessions:**
  - The venue is chosen by symbol suffix (KRX, `_NX` NXT, `_AL` SOR).
  - `stex_tp` per row can be "KRX", "NXT" or "통합". Whether a `_AL`
    request returns rows labelled with the executing venue or "통합" is
    **not documented**.
  - The `ka10055` example (`tdy_pred=2`) contains a `171945` row. The
    table does not say whether after-hours or NXT executions are included.
- **Aggressor side:**
  - REST `cntr_trde_qty` is documented only as "부호가 포함된 숫자".
    Examples carry `-5` (`ka10003`) and `-1` (`ka10084`) quantities.
  - The **WebSocket** `0B` 주식체결 field `15` "거래량" is documented as
    "+는 매수체결,-는 매도체결" (W1 L97214). No REST trade table in the pin
    carries that sentence.
  - **Inference:** the REST quantity sign follows the WebSocket convention.
    This is **not** documented for REST and must not be used to set a
    side (G-S1).
- **Quantity magnitude:** in every example the absolute value of the
  signed quantity is what increases `acc_trde_qty` (e.g. `ka10084` rows
  `-1` with cumulative 1 → 2). **Inference:** magnitude = shares, sign =
  something else.

### 3.6 Limits

- Rows per page: not documented.
- History depth: §3.5.
- Error codes (W1 `error_codes`), with documented messages:
  - `1700` "허용된 API 요청 개수를 초과하였습니다. 유량={?}, API ID={?}";
  - `1701` "허용된 전체 요청 개수를 초과하였습니다. 총유량={?}";
  - `1702` "허용된 그룹 요청 개수를 초과하였습니다. 총유량={?}, API_ID={?}";
  - `1687` "재귀 호출이 발생하여 API 호출을 제한합니다, API ID={?}";
  - `1901`–`1903` (market code / symbol / 거래소구분 not found);
  - `8104` (API not supported in mock).
  - Numeric quotas are not in W1–W7. The portal quota recorded in
    [kiwoom-market-data.md](kiwoom-market-data.md) is outside this pin set.
- Example clients cap at `MAX_PAGES = 10` with
  `REQUEST_DELAY_SECONDS = 0.2` (W3 L20–21, W4 L20–21, W5 L20–21). These
  are **client policies**, not provider limits.

### 3.7 Contradictions and inferences

1. **Envelope key differs in one example.** The `ka10084` example uses
   `returnCode`/`returnMsg` (W1 L24751); every other trade route uses
   `return_code`/`return_msg`.
   - W4 L154 checks `response_body.get("return_code") not in (None, 0)`,
     so a `returnCode` body is treated as success **whatever its value**.
   - W6 L84 reads only `return_code`; W7 L30–36 says `None` means "no
     code present", and W6 L100/L105 then raise nothing.
   - KTradeLink's fail-closed rule rejects a missing or unreadable status
     (G-E1).
2. **Quantity sign: table vs example.** `ka10055` documents `cntr_qty` as
   "단위: 1주" without a sign, yet its example values are `-1793`, `-1`,
   `-1`, `-100` (W1 L17879).
3. **Identical rows.** The `ka10055` example has two `154626` rows with the
   same price, change and quantity (`-1`); only `acc_trde_qty` (444400 vs
   444401) differs. `(time, price, quantity)` is therefore **not** a unique
   key (G-D1).
4. **Cumulative gap.** In the same example, 444401 → 446203 is +1802, but
   the newer row's quantity is 1793. Either rows are missing between them or
   the example is inconsistent. Do not assume continuity.
5. **Field in table, missing from example.** `stex_tp` is in the `ka10084`
   table (L24739) but absent from its example rows.
6. **Value units differ by route.** `acc_trde_prica` is 원 on `ka10003` but
   백만원 on `ka10084` and `ka10055`. The examples agree in scale
   (`ka10084` `"0"` for 2 shares at 128300).
7. **Implausible example prices.** The `ka10003` example alternates
   between 53500 and the 상한가 68900 within minutes, and its last row has
   `pri_buy_bid_unit` 67500 above the trade price 67100. The examples are
   illustrative only.
8. **Signed zero.** `ka10084` shows `"pri_sel_bid_unit": "-0"`. A parser
   must accept or reject `-0` explicitly.
9. **Same table, different `sign` label.** `ka10003` labels `sign` as
   "sign"; `ka10084` as "전일대비기호". The code list is identical.

## 4. LS Securities

### 4.1 Pinned sources

All LS sources are public web resources on `https://openapi.ls-sec.co.kr`
without an immutable revision; only L1 carries a publisher version marker.
Each sha256 prefix identifies only the copy retrieved at the stated UTC time
on 2026-11-05 (window 07:10:36–07:12:47Z). The detail endpoints return JSON:
the path is the TR's `data-tr` id and `api=` is the parent sub-menu id
`54a99b02-dbba-4057-8756-9ac759c9a2ed` (`[주식] 시세`, `/stock/market-data`)
or `12320341-ad85-429a-90bd-5b3771c5e89f` (`[주식] 차트`, `/stock/chart`),
both read from L2. L1 and the L3/L4 hashes are byte-identical to the copies
pinned by the capability inventory (its L1/L2).

| # | Path / URL | Pin (sha256 prefix, UTC retrieval, revision) | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true | `9aaca437f1925115`, 07:10:36Z, 2,792,313 bytes; publisher `"version" : "20261026021444748"` | TR discovery (all REST TRs whose name contains 체결/시간대/틱), field tables, `transactionPerSec`, REST server `https://openapi.ls-sec.co.kr:8080`, `contentType` |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `f9110ffd00a01b89`, 07:11:06Z (page varies per request) | `data-api` / `data-tr` ids |
| L3 | `…/guide/api/f1408ze5-83ug-s557-4mc1-x51w48aoxvd8?type=rest&api=54a99b02-…` (t1301) | `768799e97d57c8d5`, 07:11:18Z | Field table, `required`, code sample, 1-row response example |
| L4 | `…/guide/api/1455a055-68ad-4830-88d2-98e8b15ed8f2?type=rest&api=54a99b02-…` (t8454) | `d28ac2914a236eb9`, 07:11:20Z | Same; 20-row NXT response example |
| L5 | `…/guide/api/m5385w1v-6qqk-4mp7-v4u2-47574734x8g2?type=rest&api=54a99b02-…` (t1310) | `7e894907544488ca`, 07:11:21Z | Same; 2-row minute-mode example |
| L6 | `…/guide/api/80fs5s20-0zdv-pwy6-fuvc-i145b873aw1a?type=rest&api=54a99b02-…` (t1308) | `b0887f8e26e88b80`, 07:11:23Z | Neighbouring aggregate route (out of scope, §4.2) |
| L7 | `…/guide/api/f005a3h7-7en1-61ng-2t1c-w78a2g4b8lv4?type=rest&api=54a99b02-…` (t1109) | `ccc49aaaad66dfaf`, 07:11:25Z | After-hours single-price executions (§4.2) |
| L8 | `…/guide/api/d572j5bw-aswb-mcjo-72x8-s726julol0y7?type=rest&api=12320341-…` (t8411) | `a6e3395d3e5b05c8`, 07:11:27Z | Tick chart; "no data" example under `00000` |
| L9 | `…/guide/api/9def2199-03ab-4a51-8275-e4db07ef35ce?type=rest&api=12320341-…` (t8453) | `d2686195e356c5da`, 07:11:28Z | Integrated tick chart; session-time summary fields |
| L10 | https://openapi.ls-sec.co.kr/community-faq (302 → `/community/10000000-0000-0011-0000-000000000002`) | `ea4a5a1943e5ee6b`, 07:12:32Z (differs from the candle ledger copy; page varies) | Symbol format; `cts_` continuation prose |

**Missing evidence:**

- No publisher Git repository or SDK for LS REST; every fact is from the
  portal (field table or publisher example).
- No tick-mode (`timegb` `1`) example for t1310; no t1301/t8454 example
  with a falling price, an integrated (`U`) venue, or a continuation call.
- No time-zone, history-depth or session-coverage statement for any
  candidate route.
- No over-limit response code was found in L1/L3–L5.

### 4.2 Routes

Common transport (L1, L3–L5):

- `POST`, origin `https://openapi.ls-sec.co.kr:8080`, `contentType`
  `application/json; charset=UTF-8`. L1 lists one REST server; a
  `simulationUrl` exists only for WEBSOCKET, so a separate paper REST origin
  is **not documented**.
- Request headers (all `required: true` in L3–L5): `content-type`,
  `authorization`, `tr_cd`, `tr_cont`, `tr_cont_key`, `mac_address`
  ("법인인 경우 필수 세팅"; the code samples send `""`).
- Response headers: `content-type`, `tr_cd`, `tr_cont`, `tr_cont_key`.
- Body: `{"<tr>InBlock": {...}}` (code samples).

| Route (title verbatim) | Method + path | TR id | Real / paper | Row = individual trade or time aggregate? | Evidence |
| --- | --- | --- | --- | --- | --- |
| "주식시간대별체결조회" | `POST /stock/market-data` | `t1301` (TPS `2`) | one REST origin; paper not documented | Not stated. **Inference:** individual executions (§4.5). | field table (L1, L3), publisher example (1 row) |
| "(통합)주식시간대별체결2 API용" | `POST /stock/market-data` | `t8454` (TPS `1`) | as above | Not stated. **Inference:** individual executions; strongest example evidence (§4.5). | field table (L1, L4), publisher example (20 rows) |
| "주식당일전일분틱조회" | `POST /stock/market-data` | `t1310` (TPS `2`) | as above | Selectable: `timegb` "0:분 / 1:틱". Tick mode is **not exemplified**; the example is minute mode. | field table (L1, L5), publisher example (minute mode, 2 rows) |

Related routes found in L1 but **not** recommended as the trade-tick route:

- `t1308` "주식시간대별체결조회챠트" (TPS `1`, L6): rows carry `open`/`high`/
  `low` and the request has `bun_term` "분간격" — a per-interval aggregate.
- `t1109` "시간외체결량" (TPS `1`, L7): `dan_*` fields; example rows at
  10-minute marks between 16:10 and 18:00. **Inference:** after-hours single-price
  (시간외단일가) prints only. Its own continuation keys (`dan_chetime`,
  `idx`).
- `t8411` "주식차트(틱/n틱)" and `t8453` "(통합)주식챠트(틱/N틱) API용"
  (`/stock/chart`, TPS `1`, L8/L9): `ncnt` "단위(n틱)" bars with `date`,
  `time`, OHLC, `jdiff_vol`. With `ncnt` 1 the t8453 example rows look like
  single prints (O=H=L=C), but they are chart bars with no side fields, and
  the effect of `ncnt` 1 is not documented.
- Real-time WebSocket trade feeds (`S3_`, `NS3`, `US3`) are out of scope.

### 4.3 Request fields

| Concern | t1301 | t8454 | t1310 |
| --- | --- | --- | --- |
| Symbol format | `shcode` "단축코드" String 6; example `"001200"` | `shcode` String 6; example `"010950"` | `shcode` String 6; example `"001200"` |
| Venue selector + codes verbatim | **none**. Venue not documented. | `exchgubun` "거래소구분코드" String 1, **no description** in L1/L4; example `"N"` | `exchgubun`: "K: KRX / N: NXT / U:통합 / 그외 입력값은 KRX로 처리"; example `"U"` |
| Time / date filter + format | `starttime` "시작시간" String 4, "장시작시간 이후"; `endtime` "종료시간" String 4, "장종료시간 이전"; examples `""`. No date field. | `starttime`, `endtime` String 4, no descriptions; examples `""`. No date field. | `daygb` "당일전일구분": "0:당일 / 1:전일"; `endtime` String 4: "처음 조회시 시간 입력값. / t1310OutBlock1.chetime <= endtime 인 데이터 조회됨."; no start time |
| Other filter | `cvolume` "특이거래량" Number 12, "거래량 > 특이거래량"; example `0` | `cvolume` "특이거래량" Number 12, no description; omitted from the code sample | `timegb` "분틱구분": "0:분 / 1:틱"; example `"0"` |
| Count / page size | **none** | **none** | **none** |
| Continuation | body `cts_time` "시간CTS" String 10, "연속조회시 OutBlock의 동일필드 입력"; headers `tr_cont` "연속거래 여부 Y:연속○ N:연속×" and `tr_cont_key` String 18 "연속일 경우 그전에 내려온 연속키 값 올림" | body `cts_time` String 10 (no description) + same headers | body `cts_time`: "처음 조회시 Space / 다음 조회시 t1310OutBlock.cts_time 값 입력" + same headers |
| Other required fields | all body fields and headers marked `required: true` | same; see §4.7 item 3 | same |

- The `HHMM` format of `starttime`/`endtime` is stated only on t1308
  ("장시작시간 이후(hhmm)", L6). **Inference:** the same format applies to
  t1301/t8454/t1310.
- FAQ (L10, publisher prose): "'A'를 제외한 6자리 단축코드 만 사용합니다.
  예: A005930 → 005930" and "응답의 연속 키( cts_ 필드)가 비어있지 않으면 다음
  데이터가 더 있다는 의미입니다. 해당 키를 다음 요청의 입력에 그대로 넣고, 연속 조회
  플래그를 true 로 설정해 반복 호출합니다." How the body `cts_time` relates to
  the `tr_cont_key` header is **not documented**.

### 4.4 Response

| Concern | t1301 | t8454 | t1310 |
| --- | --- | --- | --- |
| Envelope / status + success value | Root `rsp_cd`, `rsp_msg`, not in the field table; example `"00000"` / "정상적으로 조회가 완료되었습니다." | same | same |
| Row array path | `t1301OutBlock1` ("Object Array"); summary `t1301OutBlock` (`cts_time`) | `t8454OutBlock1`; summary `t8454OutBlock` (`cts_time`, `ex_shcode` "거래소별단축코드" String 10, example `"N010950"`) | `t1310OutBlock1`; summary `t1310OutBlock` (`cts_time`) |
| Trade time | `chetime` "시간" String 10; example `"102626"` (`HHMMSS`) | `chetime` String 10; examples 6 characters `HHMMSS` | `chetime` String 10; examples `"102700"` and `"100800\u0000000"` (embedded NUL, §4.7) |
| Date present in row? | **no** | **no** | **no** (`daygb` selects 당일/전일 instead) |
| Price | `price` "현재가" Number 8; example `3685` (KRW unit not stated) | `price` Number 8; examples 60600/60700 | `price` Number 8 |
| Quantity | `cvolume` "체결수량" Number 12 | `cvolume` "체결수량" Number 12 | `cvolume` "체결수량" Number 12; meaning in minute mode not documented |
| Side / aggressor | No per-row side field. Cumulative counters: `mdvolume` "매도체결수량", `mdchecnt` "매도체결건수", `msvolume` "매수체결수량", `mschecnt` "매수체결건수", `revolume` "순체결량", `rechecnt` "순체결건수". How a trade is assigned to 매도/매수 is **not documented**. | same fields | same fields |
| 체결강도 | `chdegree` "체결강도" Number 8.2 | same | same |
| Change / sign | `sign` "전일대비구분" String 1 (**no code list** on these TRs); `change` "전일대비" Number 8; `diff` "등락율" Number 6.2 | same | same |
| Cumulative volume / value | `volume` "거래량" Number 12 (cumulative per example arithmetic, §4.5); no value/turnover field | same | same |
| Trade id / sequence | **none** | **none**; `exchname` "거래소명" String 3 (example `"NXT"`) | **none**; `exchname` in table but absent from the example |
| JSON types | Table: Number for numerics. Example: integers for `price`, `change`, `cvolume`, `volume`, `md*`, `ms*`, `re*`; **strings** for `diff` (`"000.68"`) and `chdegree` (`"00163.65"`) | Example: integers as t1301; `diff` `"0.66"`, `chdegree` `"62.76"` (unpadded) | Example as t1301 (padded strings) |
| Ordering | Not determinable (1 row) | Not documented. Example is **newest first** (141715 → 135820). | Not documented. Example newest first (102700 → 100800). |

Sign-code list: the t1301/t8454/t1310 tables give none. The only nearby
list is on chart TRs (t8410 "1:상한2:상승3:보합4:하한5:하락", per the candle
ledger), which is not evidence for these TRs.

### 4.5 Semantics

- **Individual trade vs aggregate:** not stated by the publisher.
  - **Inference (t8454, L4 example, 19 of 19 consecutive pairs):** the
    newer row's `volume` exceeds the older row's by exactly the newer row's
    `cvolume`, and exactly one of `mdvolume`/`msvolume` rises by that
    amount while its `*checnt` rises by 1. Each row therefore looks like one
    execution carrying day-cumulative counters.
  - In the same example, `revolume` = `msvolume` − `mdvolume`,
    `rechecnt` = `mschecnt` − `mdchecnt`, and `chdegree` =
    `msvolume` / `mdvolume` × 100 to two decimals on every row (also true
    for the t1301 and t1310 rows).
  - t1301 has only one example row; the inference is carried over from the
    identical field set and is **unverified** for t1301.
  - t1310 `timegb` `0` rows (example) are per-minute; in that example
    `cvolume` 5 does not equal the change in `volume` between the minute
    rows, so `cvolume` in minute mode is not a per-minute volume.
- **Aggressor side:** not documented.
  - **Inference:** in the t8454 example, every row whose `mdvolume` rose
    printed at 60600 and every row whose `msvolume` rose printed at 60700,
    which fits a seller-initiated / buyer-initiated split. This reading
    uses outside market-microstructure knowledge; the publisher does not
    define "매도체결"/"매수체결".
  - Per-row side can only be derived by differencing cumulative counters
    between adjacent rows, which needs both rows in hand (a page boundary
    or a filtered row breaks it).
  - In the t1301 and t1310 examples `volume` − `mdvolume` − `msvolume` =
    6,062 / 6,063, i.e. some volume is in neither bucket. **Inference:**
    auction prints may be unclassified. Not documented.
- **Time format:** `chetime` String 10; examples are `HHMMSS` (6 chars) for
  t1301/t8454. `cts_time` examples are 10 chars: t8454 `"1358200001"` =
  oldest row `135820` + `0001`; t1301 `"1013130002"`. The meaning of the
  last 4 characters is **not documented**. Time zone: **not documented**.
- **Date / history depth:**
  - t1310: "0:당일 / 1:전일" — today or the previous day only.
  - t1301, t8454: no date input or output; depth **not documented**.
    **Inference:** current day only.
- **Ordering / paging direction:** t8454 example is newest first and its
  `cts_time` points at the oldest returned row's second.
  **Inference:** continuation pages go back in time. Whether the row at
  `cts_time` is repeated on the next page is not documented. t1310's
  "chetime <= endtime" also implies a backward walk from `endtime`.
- **Session coverage:**
  - t8454 example rows are NXT (`exchname` `"NXT"`, `ex_shcode`
    `"N010950"`) at 13:58–14:17.
  - Whether t1301 includes KRX pre-market/after-hours or NXT prints is not
    documented. **Inference:** t1301 may be KRX only (no `exchgubun`;
    contrast with "(통합)" t8454) and may exclude after-hours single-price
    prints, which have their own route t1109. Unverified.
  - What `exchgubun` `U` returns (interleaved KRX + NXT rows, or a merged
    tape) and what `exchname` then holds is **not documented**.
  - The t8453 summary block (L9) carries NXT pre-market `080000`–`085000`,
    NXT after-market `154000`–`200000` and KRX after-market start/end
    fields (example values). These are not present on t8454/t1310.

### 4.6 Limits

- **Rows per call:** no count field; page size **not documented**. Example
  sizes: t1301 1, t8454 20, t1310 2 rows.
- **Rate:** `transactionPerSec` t1301 `2`, t8454 `1`, t1310 `2` (L1, L3–L5).
  No account- or app-level limit and no over-limit code found in these
  sources.

### 4.7 Contradictions and inferences

1. **`cts_time` vs rows (t1301, L3):** the only row is `102626` but
   `cts_time` is `"1013130002"`, i.e. earlier than and not matching the
   returned row. In t8454 the key matches the oldest row. The t1301 example
   is probably truncated; do not derive paging rules from it.
2. **Embedded NUL (t1310, L5):** `cts_time` `"100700\u0000000"` and
   `chetime` `"100800\u0000000"` contain U+0000. A decoder must not treat
   `chetime` as clean ASCII digits.
3. **t8454 code sample vs field table (L4):** the sample body sends
   `bun_term` (a t1308 field, absent from the t8454 table) and omits
   `cvolume` and `cts_time`, which the table marks `required: true`.
4. **t1310 example vs table:** the request uses `exchgubun` `"U"`, but the
   rows have no `exchname`, which the table lists.
5. **Types:** `diff` (Number 6.2) and `chdegree` (Number 8.2) are JSON
   strings in every example, in two styles: zero-padded (`"000.68"`,
   `"00163.65"`, t1301/t1310) and unpadded (`"0.66"`, `"62.76"`, t8454).
6. **`chetime` length:** String 10 in the table, 6 characters in the
   t1301/t8454 examples, 10 characters with a NUL in t1310.
7. **Change sign:** every t1301/t8454/t1310 example row has `sign` `"2"` and
   positive `change`, so whether `change` is signed when the price falls is
   not determinable. In the t1109 example (L7) a falling row has
   `dan_sign` `"5"`, `dan_change` `15` (unsigned) and `diff` `"-00.41"`
   (signed): `change` and `diff` may follow different sign conventions.
8. **t1301 vs t1310 examples:** both show symbol `001200` near 10:27, but
   the t1310 minute row `102700` has `msvolume` 195607 / `mschecnt` 238,
   lower than the t1301 trade row `102626` (195608 / 239). The examples
   were presumably captured at different times; they cannot be used to
   reason about minute-label start/end.
9. **Success with no data (L8):** the t8411 example returns
   `"rsp_cd": "00000"` with "해당자료가 없습니다." and no OutBlock. An empty
   or missing row array under `00000` is therefore possible.
10. **t1301 `cvolume` filter:** "거래량 > 특이거래량" does not say which
    quantity (row `cvolume` or cumulative `volume`) is compared, nor what
    `0` does. **Inference:** `0` disables the filter.

## 5. DB Securities

### 5.1 Pinned sources

GitHub sources are at
[`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb)
(`564b5100b80a3a785468b77ee8c0557f6edcfdeb`, committer date
2026-08-20T10:06:26+09:00), the commit already pinned by the candle and
capability ledgers; blob SHAs are from `git ls-tree` of that commit. Guide
JSON endpoints on `https://openapi.dbsec.co.kr` were retrieved 2026-11-05
07:13:25–07:14:27Z. The portal API ids are the ones the SDK docstrings link
(`…/apiservice?group_id=80005fb0-…&api_id=…`).

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| D1 | [`dbsec_sdk/apis/kr_stock_quote/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_quote/endpoints.py#L320-L402) | blob `5930af396f4a74ff04c7e780fcec87660399bec3`; L35–36, L53–54 paths/TR codes; L320–358 CONCLUSION; L360–402 DAYTRADE | Routes, "유량제어: 3 TPS", field docstrings, `InputHourClsCode` list |
| D2 | [`examples/kr_stock_quote/README.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/README.md#L25-L43) | blob `8041ac5a03b1cdd1d7227c48901b6017755426a7`; L25–26, L36–43 | Route titles; CONCLUSION is the paging example |
| D3 | [`examples/kr_stock_quote/kr_stock_inquire_time_execution.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_time_execution.py) | blob `ad190cccaefb2dfa0eab2580257fff0c3ad3f13d`; L18–28, L37–46 | Example body; `Out (오브젝트)` |
| D4 | [`examples/kr_stock_quote/kr_stock_inquire_time_execution_paged.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_time_execution_paged.py#L14-L36) | blob `eece643c3faf82f4e856db709701bd831c278426`; L14–23, L33–36, L81–83, L93–94 | Publisher prose on per-trade rows and header paging |
| D5 | [`examples/kr_stock_quote/kr_stock_inquire_daily_executions.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_daily_executions.py) | blob `8c97b4a332915b275d8ffe84c813f49fa7afd798`; L18–29, L38–48 | Example body (`InputHourClsCode` `"4"`) |
| D6 | [`dbsec_sdk/response.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/response.py#L27-L85) | blob `6ce92fdc7fca3e34dda4c25b2797e153de29f7a5`; L27–32, L42–45, L78–85 | `cont_yn`/`cont_key` are response headers; success `rsp_cd == '00000'` even on HTTP 200 |
| D7 | [`dbsec_sdk/client.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/client.py#L231-L283) | blob `6000fa447765e6fc5822e6c8fe09ef92ead8d462`; L65–76, L231–283 | SDK paging loop, 100-page safety cap, `IGW00201` back-off retry — SDK behaviour, **not** adopted |
| D8 | [`docs/errors_and_rate_limits.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/errors_and_rate_limits.md#L197-L212) | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L48, L74, L104–109, L197–212 | `00000` message variants; `IGW00201`; app 20 TPS |
| D9 | [`docs/api_support_matrix.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/api_support_matrix.md#L58-L59) | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c`; L3–5, L58–59 | Both routes ⭕ ("모의투자 + 실전투자 모두 호출 가능"), TPS 3 |
| D10 | [`config.yaml.example`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/config.yaml.example#L13-L14) | blob `f6204f1399f2f080c11f28364444b40b7868ef96`; L13–14 | "REST API URL은 운영/모의 동일 (앱 속성으로 내부 분기)" |
| D11 | [`dbsec_sdk/auth.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/auth.py) | blob `b83addb2b8007ae12946eab1ae0395ceb3eca7de`; L250–253 | SDK base headers: `content-type`, `authorization` only |
| DP1 | https://openapi.dbsec.co.kr/api/apis/public/api-list/80005fb0-6feb-4b8b-904a-605c59e29b4f (국내주식시세) | sha256 `f4f56996c26c33b3`, 07:13:25Z (identical to the inventory's D7 copy) | Per-API `accessUrl`, `httpMethod`, `contentType`, `domain`, `simulatedDomain`, `extraParam` |
| DP2 | `https://openapi.dbsec.co.kr/api/apis/public/<api_id>`: CONCLUSION `01b99bab-7f12-4098-97e1-99fdda029ca2`, DAYTRADE `6738128a-9cc7-46ce-b59f-dda6162a12b8` | sha256 CONCLUSION `87fc2e98b056fd97` (07:13:27Z), DAYTRADE `6c91a035165e9fbe` (07:13:28Z); `lastModifiedDate` 2024-03-28 (both) | Same metadata per API (contains staff contact data; not copied) |
| DP3 | `https://openapi.dbsec.co.kr/api/apis/guide/tr/<api_id>` | sha256 CONCLUSION `9f173a6f5907af57` (07:13:29Z), DAYTRADE `6516ac7c46f221f4` (07:13:30Z) | `trCode`, `transactionPerSec` `"3"`, `reqExample`, `resExample` (20 rows each) |
| DP4 | `https://openapi.dbsec.co.kr/api/apis/guide/tr/property/<tr_id>`: CONCLUSION `2d5b6685-7cc5-4c28-9391-e20d4979f40f`, DAYTRADE `73e2be64-29e3-4180-971e-63131b282b37` | sha256 CONCLUSION `7a0d6af0055c5fce` (07:13:43Z), DAYTRADE `9047cf546e005642` (07:13:44Z) | Header/body field tables |
| DP5 | `…/guide/tr/efe731f7-0f2a-45d1-81da-335ebeacd552` (CHARTTICK) | sha256 `df8397f078cb1b8e`, 07:14:27Z | Neighbouring N-tick chart (out of scope) |

**Missing evidence:**

- No field descriptions for any response field (DP4 `description` is null
  for `Hour`, `Prpr`, `PrdyVrssSign`, `PrdyCtrt`, `PrdyVrss`, `CntgVol`,
  `ShnuCnqn`, `SelnCnqn`).
- No sign-code list for `PrdyVrssSign` in these sources.
- No example with a continuation call, an NXT/`UJ` venue, or a
  session code other than DAYTRADE `4`.
- No time-zone, history-depth or page-size statement.

### 5.2 Routes

Common transport (DP1–DP4, D6, D10):

- `POST`, `contentType` `application/json;charset=utf-8`, domain
  `https://openapi.dbsec.co.kr:8443`, `simulatedDomain` null; D10: one
  REST origin for production and demo ("앱 속성으로 내부 분기").
- Request headers (DP4 `req_h`, all `requireYn` `Y`): `content-type`,
  `authorization`, `cont_yn` "연속거래 여부(Y:연속거래 사용 N:연속거래
  사용안함)", `cont_key` (String 70) "연속일 경우 그전에 내려온 연속키 값 올림",
  `mac_address` "제휴사인 경우 필수 세팅, 개인은 세팅 X". No `tr_cd` header; the
  path selects the TR. The SDK base headers are `content-type` and
  `authorization` only (D11).
- Response headers: `content-type`, `cont_yn`, `cont_key` (String **18**,
  `requireYn` `N`).
- Body `{"In": {...}}`.

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Row = individual trade or time aggregate? | Evidence |
| --- | --- | --- | --- | --- | --- |
| "시간대별체결조회" ("국내주식 시간대별 체결 조회 API입니다.") | `POST /api/v1/quote/kr-stock/inquiry/hour-price` | `CONCLUSION`; api `01b99bab-…`; `svc_id` `CONCLUSION` | same origin; SDK matrix ⭕ (D9 L58) | Field tables silent. Publisher example-code prose (D4 L14–15): "시간대별 체결은 장중 체결 한 건 한 건이 시간 순으로 쌓이는 데이터라" — individual executions. | field table (DP4), publisher example (DP3), publisher client code (D1, D3, D4) |
| "일별체결조회" ("국내주식 일별체결 조회 API입니다.") | `POST /api/v1/quote/kr-stock/inquiry/daily-price` | `DAYTRADE`; api `6738128a-…`; `svc_id` `DAYTRADE` | same; ⭕ (D9 L59) | Not stated. Despite the title, rows carry `Hour` and one quantity each. **Inference:** individual executions of one day with a side split (§5.5). | field table (DP4), publisher example (DP3), publisher client code (D1, D5) |

The capability inventory lists only CONCLUSION for DB; DAYTRADE is a second
candidate and the only DB REST route with a buy/sell quantity split and a
session filter.

Out of scope: `CHARTTICK` `POST /api/v1/quote/kr-chart/tick` (TPS 4, DP5)
returns N-tick bars (`InputDivXtick` "N Tick 입력 ex. 100") with `Date`,
`Hour`, OHLC and `CntgVol`; it is a chart, has no side field, and whether
`1` is accepted is not documented. Real-time `S00` 체결 is WebSocket.

### 5.3 Request fields

| Concern | CONCLUSION | DAYTRADE |
| --- | --- | --- |
| Symbol format | `InputIscd1` "입력종목코드1" String 12: "종목코드 입력 - J(KRX 주식): (ex. 005930) - NJ(NXT 주식): (ex. N-005930) - UJ(통합): (ex. U-005930) ※ NXT/통합시세로 종목 조회 시 반드시 종목 앞에 구분자 (N-, U-)를 붙여서 호출 부탁드리겠습니다." | same |
| Venue selector + codes verbatim | `InputCondMrktDivCode` "입력조건시장분류코드" String 2: "주식:J / 주식(NXT): NJ / 주식(통합): UJ / ETN: EN / ELW: W / ※ ETF종목의 경우 J 코드를 사용해 조회 부탁드립니다." | same |
| Time / date filter + format | **none** (no date, no time) | **none** for date/time. Session filter `InputHourClsCode` "입력시간구분코드" String 9: "1: 시간외단일가체결 / 2: 장전+장중+장후 / 3: 장전+장후 / 4: 장중 / 5: 장전+장중+장후+장종료(예상포함) / 6: 예상제외 모두 / 7: 장전+장중+장후+장종료(예상불포함) / 8: 예상 / 9: 장전+장중+장후+장종료 (예상,대량, 바스켓, 정리매매 제외) / 10: 시간외단일가 예상" |
| Count / page size | **none** | **none** |
| Continuation | Headers only: request `cont_yn`/`cont_key`, response `cont_yn`/`cont_key`. D6 L42–43: "DB증권 서버는 응답에 cont_yn(다음 페이지 존재 'Y'/'N')·cont_key(다음 키) 헤더를 내려준다". D4 L19–23 table: first `cont_yn=N, cont_key=""`; then `cont_yn=Y` with the previous key; stop when the response `cont_yn` is `N`. D4 L32: body "페이지마다 동일하게 재사용됨 (cont_key 는 헤더로만 변함)". | same headers; no route-specific paging example |
| Other required fields | all marked `requireYn` `Y` | all `Y` |

### 5.4 Response

| Concern | CONCLUSION | DAYTRADE |
| --- | --- | --- |
| Envelope / status + success value | Root `rsp_cd`, `rsp_msg` (not in DP4); example `"00000"` / "정상 처리 되었습니다.". D6 L82–83: "업무 성공은 rsp_cd == '00000' 으로 확인한다 (서버가 HTTP 200 과 함께 업무오류코드 M100/IGW… 를 내려주는 경우가 있음)". | same |
| Row array path | `Out`; DP4 type `A0003` (the same type as the `In` object); D3/D4 "Out (오브젝트)"; example is a JSON **array** | same |
| Trade time | `Hour` "시간" String 16, no description; examples `HHMMSS` | same |
| Date present in row? | **no** | **no** |
| Price | `Prpr` "현재가" String 16; examples unsigned digit strings (`"73000"`) | same (`"73000"`, `"73200"`, `"73100"`) |
| Quantity | `CntgVol` "체결거래량" String 16 | none named as such; see side row |
| Side / aggressor indicator | **none** | `ShnuCnqn` "매수체결량" String 10, `SelnCnqn` "매도체결량" String 10; no descriptions. In every example row exactly one of the two is non-zero. |
| 체결강도 / buy-sell totals | none | none (per-row quantities only) |
| Change / sign | `PrdyVrssSign` "전일대비부호" String 1 (no code list); `PrdyCtrt` "전일대비율" String 16, example `"-1.35"` (signed) | `PrdyVrssSign`; `PrdyVrss` "전일대비" String 16, example `"-1000"` (**signed**) |
| Cumulative volume / value | **none** | **none** |
| Trade id / sequence | **none** | **none** |
| JSON types | DP4 `A0001` for every field; every example value is a JSON string | same |
| Ordering | Not documented. Example newest first (`153007` → `153005`). D4 L14 prose says rows accumulate "시간 순으로". | Not documented. Example newest first (`153007` → `151958`). |

### 5.5 Semantics

- **Individual trade vs aggregate:**
  - CONCLUSION: publisher example-code prose (D4 L14–15, L81–82) says
    "장중 체결 한 건 한 건이 시간 순으로 쌓이는 데이터" — **publisher client
    code**, not a contract. The field table does not say.
  - DAYTRADE: **Inference** from the example — 13 rows share `151959`,
    each with a small single quantity; these are executions, not a
    per-second aggregate.
  - **Inference:** `CntgVol` is a per-row quantity, not cumulative: the
    CONCLUSION example's `153007` row has `CntgVol` `"1321868"`, equal to
    the DAYTRADE example's `153007` `SelnCnqn` `"1321868"` (same symbol,
    price and change in both examples).
- **Zero-quantity rows (CONCLUSION example):** 19 of 20 rows
  (`153007`…`153005`) have `CntgVol` `"0"` at an unchanged price.
  Not documented. **Inference:** these may be expected-price (예상체결)
  updates around the closing auction, which DAYTRADE can exclude via
  `InputHourClsCode`; CONCLUSION has no such filter. Weak; rests on outside
  knowledge of the KRX closing call auction.
- **Aggressor side:** DAYTRADE splits each row into "매수체결량" /
  "매도체결량". The rule assigning a trade to either side is **not
  documented**.
  - **Inference:** in the example, buy-side rows print at 73200 and the one
    sell-side intraday row at 73100, which fits an aggressor
    classification.
  - The `153007` closing print (1,321,868 shares, code `4` "장중") is
    booked entirely as `SelnCnqn`. **Inference:** auction prints receive a
    side that is not an aggressor side.
- **Time format:** `Hour` String 16 with `HHMMSS` examples; no sub-second
  part. Time zone **not documented**.
- **History depth:** no date input or output on either route; **not
  documented**. **Inference:** current (or latest) trading day only. The
  DAYTRADE title "일별체결조회" does not mean per-day rows.
- **Session coverage:**
  - Venue by `J`/`NJ`/`UJ` plus `N-`/`U-` symbol prefix. Rows carry no
    venue field, so `UJ` rows cannot be attributed to KRX or NXT.
  - DAYTRADE session codes are verbatim above. "장전", "장후", "장종료",
    "예상" are not defined; NXT pre/after-market is not mentioned.
  - The DAYTRADE example with `4` "장중" contains the `153007` closing print
    and no rows between `151959` and `153007`.
  - CONCLUSION coverage is not documented.

### 5.6 Limits

- **Rows per call:** not documented; both examples have 20 rows.
- **Rate:** 3 TPS per route (DP3 `transactionPerSec` `"3"`; DP1/DP2
  `ThroughputQuotaRule` and `CorpThroughputQuotaRule` `requestLimit` `"3"`;
  D1 L333, L374; D9). App level "20 TPS" (D8 L210, SDK documentation).
  Over the limit: `IGW00201` "호출 거래건수를 초과하였습니다." (D8 L48 under
  HTTP 403 and L74 under HTTP 500).
- **SDK client policy (not adopted):** automatic `IGW00201` exponential
  back-off retry up to 4 times (D7 L65–71); paging stops on response
  `cont_yn` ≠ `Y`, on an empty or unchanged `cont_key`, or at a 100-page
  safety cap (D7 L73–76, L258–282). D4 L93 sleeps 0.5 s between pages.

### 5.7 Contradictions and inferences

1. **`Out` type:** DP4 types `Out` as `A0003` (the type of the `In`
   object) and D3/D4 call it "(오브젝트)", but both examples return an
   array. (The candle ledger's chart routes type `Out` as `A0002`.)
2. **Route title vs content:** "일별체결조회" has no date field and returns
   intraday `Hour` rows.
3. **CONCLUSION zero-volume rows:** 19 rows with `CntgVol` `"0"` are not
   explained (§5.5).
4. **Closing print side:** the DAYTRADE `153007` print is reported as
   `SelnCnqn` (§5.5).
5. **`cont_key` length:** 70 in the request header table, 18 in the
   response header table.
6. **`mac_address`:** `requireYn` `Y`, but "개인은 세팅 X"; the SDK does not
   send it (D11).
7. **Sign conventions:** `PrdyVrss` and `PrdyCtrt` are signed strings
   (`"-1000"`, `"-1.35"`) alongside `PrdyVrssSign` `"5"`; the code list for
   `PrdyVrssSign` is not in these sources.
8. **Success with no data:** D8 L104–109 lists four `00000` messages,
   including "모의투자 데이터가 없습니다.", so an empty `Out` under `00000` is
   possible (paper).
9. **Duplicates:** the DAYTRADE example has byte-identical rows (e.g.
   `151959`, `73200`, `ShnuCnqn` `"1"` occurs four times). Without a sequence id,
   identical rows are distinct trades and must not be deduplicated by
   content.

## 6. Toss Securities

### 6.1 Pinned sources

Public Toss portal documents under `https://openapi.tossinvest.com` and
`https://developers.tossinvest.com`, retrieved 2026-11-05 07:10–07:12 UTC.
No broker API request was sent. T1–T3 have the same sha256 and version as
the copies pinned in the candle evidence (§6.1 there), so the spec did not
change between 06:43 and 07:10 UTC.

Evidence level `publisher guide` is used here for portal prose outside the
OpenAPI/AsyncAPI documents (T2 overview, T4 FAQ). T4 L3 itself defers to the
API reference: "각 API 의 정확한 요청·응답 형식은 API 문서의 해당 엔드포인트
항목이 기준입니다." `publisher guide` therefore ranks below T1 `field table`.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | sha256 `c5918961335ccd6b…`, 07:10:32Z; `openapi 3.1.0`, `info.version 1.2.28` | `paths./api/v1/trades.get` (`operationId getTrades`), `components.parameters.SymbolQuery`, `components.schemas.{Trade,ApiResponse,ErrorResponse,Currency}`, `components.responses.{NotFound,RateLimitExceeded,InternalErrorMarketData}`, `components.securitySchemes.oauth2ClientCredentials`, `tags[Market Data]`, `servers` |
| T2 | [overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md) | sha256 `bef057d9babe9a38…`, 07:10:35Z | L95 endpoint list; L236–238, L250, L264, L273–282 rate limits; L379, L384 WebSocket trade channel |
| T3 | [asyncapi.json](https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json) | sha256 `46669a360d4c5c64…`, 07:10:34Z; `asyncapi 3.0.0`, `info.version 1.2.3` | `channels.realtime-trade.description` and `messages.tradeStream` — WebSocket only, used as a cross-reference because it states the frame `data` has the REST trade item's shape |
| T4 | [faq.md](https://openapi.tossinvest.com/openapi-docs/faq.md) | sha256 `6ad4c02b8e785f7d…`, 07:11:21Z | L3 (precedence), L14 (rate headers), L22 (venue), L27 (1m-candle session scope, cross-check only), L37 (row cap, no paging), L67 (own-order fills; not this route) |
| T5 | [developers.tossinvest.com/llms.txt](https://developers.tossinvest.com/llms.txt) | sha256 `bbff77eaa55df248…`, 07:10:36Z | L16: T1 is "the source of truth for endpoints, schemas, … and rate limits" |

**Missing evidence:**

- No separate field table beyond T1's schema; no publisher client code for
  this route was retrieved.
- No paper/sandbox origin in T1.

### 6.2 Routes

Transport: `GET` with a query string; origin `https://openapi.tossinvest.com`
(T1 `servers[0].url`); response `application/json`. Required header:
`Authorization` (`Bearer` access token from `POST /oauth2/token`, scheme
`oauth2ClientCredentials`, T1). No `X-Tossinvest-Account` parameter on this
route; T1 tag `Market Data`: "계좌 정보 없이 액세스 토큰만으로 호출할 수
있습니다."

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Row = individual trade or time aggregate? | Evidence |
| --- | --- | --- | --- | --- | --- |
| "최근 체결 내역 조회" — description "당일 최근 체결 내역을 조회합니다." | `GET /api/v1/trades` | `operationId getTrades` | Real origin only; no paper origin in T1 | Individual trade. `Trade` fields are "체결가", "체결 수량", "체결 시각"; T2 L379 calls the same-shape WebSocket item "체결 틱(체결가·체결량)". **Inference** for REST: the REST text itself never says "틱". | field table + publisher guide |

Out of scope, same portal: `GET /api/v1/stocks/{symbol}/program-trades` and
`/credit-trades` (daily program/credit trading trends, not ticks). T4 L67
"체결 내역이 건별로 나오나요? … 주문 1건이 1행입니다" concerns the user's
own order fills, **not** this market-data route.

### 6.3 Request fields (`GET /api/v1/trades`, T1)

| Concern | `GET /api/v1/trades` |
| --- | --- |
| Symbol format | `symbol` (query, required, `SymbolQuery`): "종목 심볼. KRX: 6자리 종목코드 (숫자 또는 영문·숫자 조합; 예: 005930, 0101N0), US: 영문 티커 (예: AAPL). 영문 대/소문자, 숫자, '.', '-' 만 허용한다." Pattern `^[A-Za-z0-9.\-]+$`. |
| Venue selector | **None.** T4 L22: "거래소를 지정해 조회하는 파라미터나 거래소를 식별하는 응답 필드는 없습니다." (publisher guide) |
| Time / date filter + format | **None.** No time, date or `before` parameter. |
| Count / page size | `count` (query, optional, integer, default 50, minimum 1, maximum 50): "조회 건수 (최대 50)" |
| Continuation mechanism | **None.** No cursor in request or response. T4 L37: "최근 체결은 과거 방향 페이지네이션 파라미터가 없어 당일 전체 체결을 조회할 수 없습니다." |
| Other required fields | none |

### 6.4 Response (T1)

| Concern | `GET /api/v1/trades` |
| --- | --- |
| Envelope / status field + success value | HTTP 200 → `ApiResponse` (`result` required); "`result` 와 `error` 는 동시에 나타나지 않습니다." Errors → `ErrorResponse` `{error:{requestId,code,message,data?}}`. Route lists 404 (`stock-not-found`, "종목을 찾을 수 없습니다."), 429 (`rate-limit-exceeded`) and 500 (`InternalErrorMarketData`, `internal-error`). **No 400 is listed** although `count` is bounded. |
| Row array path | `result` itself is the array (`type: array`, items `Trade`) — unlike candles (`result.candles`). |
| Trade time | `timestamp` (`string`, `format: date-time`) "체결 시각". Examples carry milliseconds and an offset: `"2026-03-25T09:30:42.000+09:00"`, `"…09:30:41.500+09:00"`. |
| Date present in row? | Yes, inside the ISO-8601 `timestamp`. |
| Price | `price` (`string`, `format: decimal`, `maxLength 30`) "체결가". Sign not documented; examples unsigned. Currency via `currency`. |
| Quantity | `volume` (`string`, `decimal`, `maxLength 30`) "체결 수량" — per trade. Unit not stated. |
| Side / aggressor indicator | **None in `Trade`.** T3 (WebSocket, same item shape per T3 `tradeStream.payload.description` "`data` 는 REST 체결 조회(`GET /api/v1/trades`)의 체결 항목과 동일한 모양입니다"): "프레임에는 누적 거래량·매수/매도 구분이 없고". |
| 체결강도 / buy-sell volume | none |
| Change / sign | none (no 전일대비 fields) |
| Cumulative volume / value | none |
| Trade id / sequence | **None.** T3 (WebSocket): "유실 감지용 sequence 필드는 제공되지 않습니다." |
| Other | `currency` (`Currency` enum `KRW`, `USD`; "클라이언트는 unknown enum 값을 허용하도록 구현해야 합니다.") All four `Trade` fields are `required`. |
| JSON types | price/volume decimal **strings**; timestamp string; currency string enum. |
| Ordering | **Not documented.** Both T1 examples list rows with descending `timestamp` (publisher example). |

### 6.5 Semantics

- **Individual vs aggregate:** individual trades (§6.2; field names plus T2
  L379 / T3 same-shape statement). Whether simultaneous fills of one
  aggressive order are split or merged is not documented.
- **Time format:** ISO-8601 with offset; KRX examples use `+09:00` with
  millisecond precision. The US example is also rendered in `+09:00`
  (`"2026-03-25T22:30:42.100+09:00"`). Zone is carried in the offset; no
  separate statement of the zone.
- **History depth:** "당일 최근 체결 내역" (T1), at most 50 rows, no
  pagination (T4 L37). Past dates are not available on this route. What is
  returned before the day's first trade, on holidays, or overnight is
  **not documented**.
- **Venue:** T4 L22 "국내 캔들·체결은 KRX 만 집계하나요?" → "KRX + NXT 통합
  시세입니다. … NXT 에서 거래되지 않는 종목은 KRX 시세로 자동 제공됩니다."
  No per-row venue field (publisher guide).
- **Session coverage for REST trades:** not stated for this route.
  - T3 (WebSocket only): "푸시는 모든 세션에서 제공됩니다. … 국내는 KRX
    정규장과 NXT 프리·정규·애프터마켓 합산입니다."
  - **Inference:** REST `trades` likely draws on the same integrated feed,
    but the documents do not say so; KRX after-market inclusion is
    unresolved (see §6.7 #2).
- **Aggressor side:** not provided and not derivable from documented
  fields (no bid/ask at trade time).

### 6.6 Limits

- **Rows per call:** `count` 1–50, default 50 (T1); T4 L37 "최근 체결은 최대
  50 건입니다."
- **Rate:** T1 description "**Rate Limits Group**: `MARKET_DATA`"; T2 L250
  "`MARKET_DATA` | 초당 최대 15회". The group is shared with quotes,
  orderbook and price limits (T1 tag text: "호가·현재가·체결·상하한가는
  `MARKET_DATA` Rate Limits Group 에 속하고"). Limits are per "클라이언트 ×
  API 그룹" (T2 L236) and "운영 상황에 따라 사전 공지 없이 조정될 수"
  (T2 L238, L264).
- **Headers:** `X-RateLimit-Limit/Remaining/Reset` (T2 L273–275); T4 L14
  says success responses always include `X-RateLimit-*`. `Retry-After`
  only on 429 (T2 L276). T2 L280–281 recommends waiting `Retry-After` and
  exponential back-off with jitter on 429 (publisher guide; this route is a
  read-only GET).

### 6.7 Contradictions and inferences

1. **Ordering is example-only.** Unlike candles (explicit "최신순"), the
   trades route states no order; only the examples are newest-first.
2. **Session scope of integrated trades.** T3 lists "KRX 정규장과 NXT 프리·
   정규·애프터마켓" for WebSocket pushes, omitting the KRX after-market,
   while T4 L27 (1-minute candles) lists "KRX 애프터마켓" among included
   trades. Neither states the REST trades scope; unresolved.
3. **Example rate-limit header value.** T1 `RateLimitExceeded` example
   `X-RateLimit-Limit: 10` differs from T2's `MARKET_DATA` 15/s.
   **Inference:** the example is generic; read the live header.
4. **No dedup key.** No id/sequence; two trades with the same millisecond
   timestamp, price and volume are indistinguishable. Overlapping polls
   cannot be deduplicated exactly.
5. **OpenAPI version label.** T5 L16 calls T1 "OpenAPI 3.0"; T1 declares
   `3.1.0` (also noted in the candle evidence §6.8 #4).
6. **Candle-evidence cross-check.** Candle evidence §6.5 says REST candle
   venue is "not documented"; T4 L22 (not cited there) states candles and
   trades are KRX+NXT integrated. The candle doc may want this citation.

## 7. Meritz Securities

### 7.1 Pinned sources

Portal `https://openapi.imeritz.com`, retrieved 2026-11-05 07:10–07:13 UTC,
and GitHub repository
[`meritz-securities/open-api@a93c6409db73ea97ad15f7b7186f36c9f32ecd89`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89)
(commit 2026-10-28T22:32:03+09:00; still the default-branch head when
cloned at 07:13Z). Repo README L11: "API 목록과 파라미터·응답 필드의 정본은
개발자 포털입니다." — repo content is `publisher repo note` (prose/data) or
`publisher client code`, ranked below M1.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| M1 | Portal API spec export [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json) (`title` "메리츠증권 Open API 명세") | 07:10:40Z sha256 `0332db07236052df…`, 1,136,519 bytes, `generatedAt "2026-11-05 16:10:38"`. With `generatedAt` removed and `json.dumps(sort_keys=True, ensure_ascii=False)`: `2fff4f3e02d20cd5…` — **identical** to both candle-evidence copies (06:44Z, 06:46Z). | `groups[2]` "국내주식": `apis[24]` "체결추이 조회(틱)" (`ohhts_1002_001r`), `apis[23]` "체결추이 조회(분)" (`ohhts_1002_002r`) — field tables and examples |
| M2 | [samplecode-py](https://openapi.imeritz.com/samplecode-py) | 07:12:48Z sha256 `0e6a5582d2d2dbb3…` (varies per request) | "오류도 HTTP 500 + JSON 본문으로 오므로, 상태코드가 아니라 rsp_cd 로 판정합니다"; `rsp_cd` printability check; "초당 호출 한도는 공지사항에 기재하였습니다."; origin `https://openapi.imeritz.com:9443`. **No trades example** (0 matches for `trades/ticks`, `ohhts_1002_001r`). |
| M3 | [howto-use](https://openapi.imeritz.com/howto-use) | 07:12:50Z sha256 `d319369d8776e5e1…` | "조회 API 는 GET + 쿼리스트링 … 오류는 종류와 관계없이 HTTP 500 으로 오며, 원인은 응답 본문의 rsp_cd·rsp_msg·rsp_sub_msg 에 담깁니다." |
| M5 | repo `openapi.json` | blob `93e900e66b965607d7fd8b8e14c6088d710e6fce` | L10 server `https://openapi.imeritz.com:9443`; L8450–8632 `/market/v1/trades/minutes` (`x-tr-id` L8631, `x-tps "10"` L8632); L8635–8840 `/market/v1/trades/ticks` (`x-tr-id` L8839, `x-tps "10"` L8840) |
| M6 | repo `meritz/data/corrections.json` | blob `60370924e13233bbd2cccb517bfffee002dad915` | [L4–20](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/data/corrections.json#L4-L20) `rsp_cd` correction (keys include `market_trades_ticks`, `market_trades_minutes`); L150 after-market change |
| M7 | repo `docs/errors.md` | blob `b4b2eac6541bd2b886071c1caad17fa0c57ba3e6` | L7–8 (all errors HTTP 500), L89 `IGW50006`, L95 `EGW00200` |
| M8 | repo `llms.txt` | blob `8351d5343d785b61107179d19197c59a08e1edff` | L120–121 rate limit |
| M9 | repo `README.md` | blob `61aa5f7f2c1059a29a99175a5cdf573996d81479` | L11 portal canonical; L125 no paper account |
| M10 | repo `meritz/core/client.py` | blob `7c68d3a4006730c09b18acb90ddcf2d478a40c16` | L3–4, L565–566, L635–663 handling of unreadable `rsp_cd` (publisher client code) |

For both routes every M1 request/response field description appears
verbatim in M5, **except**: M5 has no description for `data` (so the
"40건", newest-first and no-`tr_cont_key` statements are **portal-only**),
and M5 models `authorization` as `bearerAuth` instead of a header field.

**Missing evidence:**

- The notice board that M2 cites for rate limits was not retrieved for
  this audit (the candle evidence found it script-loaded with no static
  text). The capability inventory (PR #32, its M4) did retrieve a notice
  "API 호출 유량 제어 안내(REST, WEBSOCKET)" at 06:57:52Z and summarises it
  as REST 10 calls/s **per account**, whereas M7/M8 say 10 per second
  **per API**. That notice is not re-verified here.
- M4 is not used in this section; the source IDs follow the draft
  numbering.
- No publisher sample code calls either trades route.

### 7.2 Routes

Transport (M1, M3, M5): `GET` with query string; origin
`https://openapi.imeritz.com:9443`; `contentType` "application/json;
charset=utf-8". Required headers: `authorization` (Bearer access token) and
`mac_address` ("호출 단말의 MAC 주소입니다. 12자리로 넣습니다. 넣지 않으시면
요청이 거부됩니다."). M1 files `mrkt_div_code`/`iscd` under request
"body", but its `requestExample` and M5 use `in: query`. No paper
environment: M9 L125 "앱키에 연결된 계좌는 실계좌입니다. 모의계좌는 없습니다".

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Row = individual trade or time aggregate? | Evidence |
| --- | --- | --- | --- | --- | --- |
| "체결추이 조회(틱)" / "주식 체결추이 조회 (틱)" | `GET /market/v1/trades/ticks` | `ohhts_1002_001r` | real only | **Individual trade:** `data` "체결 내역 배열입니다"; `cntg_vol` "해당 체결의 수량입니다." | field table + publisher example |
| "체결추이 조회(분)" / "주식 체결추이 조회 (분)" | `GET /market/v1/trades/minutes` | `ohhts_1002_002r` | real only | **Aggregate, grouping undocumented:** `data` "체결 내역을 일정 구간으로 묶은 배열입니다. … 한 행이 1분 구간이라고 보지 마십시오. 묶는 간격은 체결시간(cntg_hour)으로 확인하십시오." `cntg_vol` "해당 구간의 체결 수량". | field table + publisher example |

The minutes route is listed for completeness; it is **not** a tick source.

### 7.3 Request fields (M1)

| Concern | `/market/v1/trades/ticks` | `/market/v1/trades/minutes` |
| --- | --- | --- |
| Symbol format | `iscd` (Y, len 12): "종목 코드입니다. 6자리(005930)로 넣으십시오. 등록되지 않은 종목코드는 오류 없이 빈 목록이 정상 응답코드로 내려오며 자료가 없는 경우와 구분되지 않으므로, 빈 목록을 받으면 종목코드부터 확인하십시오." | same wording |
| Venue selector + codes | `mrkt_div_code` (Y, len 2): "어느 시장의 체결을 볼지 정합니다. "J": KRX "NJ": 대체거래소(NXT) "TJ": KRX + NXT 통합 같은 종목이라도 시장마다 누적거래량이 다릅니다." | same wording |
| Time / date filter | **None** | **None** |
| Count / page size | none (server returns up to 40) | none (up to 40) |
| Continuation | none in request; response `data`: "응답 본문에는 다음 페이지를 이어받는 키(tr_cont_key)가 포함되지 않습니다." | none documented; see §7.7 #4 |
| Other required fields | headers only (§7.2) | same |

### 7.4 Response (M1)

| Concern | `/market/v1/trades/ticks` | `/market/v1/trades/minutes` |
| --- | --- | --- |
| Envelope / status + success value | Top-level `data`, `rsp_cd`, `rsp_msg`, `rsp_sub_msg` (N). `rsp_cd`: ""0000": 정상 처리 조회 결과가 없을 때도 "0000" 이 내려옵니다. … 오류는 종류와 무관하게 HTTP 500 으로 반환됩니다. 성공·실패는 HTTP 상태가 아니라 이 값으로 판정하시고" — **but see §7.7 #1.** `rsp_msg`: "오류 응답에는 data·tr_cont 가 없으므로 data 를 읽기 전에 HTTP 상태와 rsp_cd 를 먼저 확인하십시오." | same |
| Row array path | `data` (Object Array): "최신 체결이 먼저 옵니다. 한 번에 40건까지 내려오며" | `data`: "최신 구간이 먼저 오고 한 번에 40건까지 내려옵니다." |
| Trade time | `prpr_hour` String len 6 "현재가시간": "체결 시각(HHMMSS)입니다. 같은 뜻의 값이 체결추이 조회(분)(/market/v1/trades/minutes)에서는 cntg_hour 라는 이름으로 내려옵니다." | `cntg_hour` String len 6: "체결 시각(HHMMSS). 집계 구간의 시각입니다." |
| Date present in row? | **No** | **No** |
| Price | `stck_prpr` Number len 13 "주식현재가": "가장 최근 체결된 가격입니다." Sign not stated; example values unsigned. Unit not stated. | `stck_prpr`, same wording |
| Quantity | `cntg_vol` Number len 13 "체결거래량": "해당 체결의 수량입니다." | `cntg_vol`: "해당 구간의 체결 수량" |
| Side / aggressor | **None.** Nearest fields: `askp` "체결 시점의 매도호가입니다.", `bidp` "체결 시점의 매수호가입니다." (Number len 13). How to classify side from them is not documented. | same `askp`/`bidp`; no side |
| 체결강도 / buy-sell volume | `tday_rltv` String len 9 "당일체결강도": "당일 체결강도(%)입니다." Formula not given. No buy/sell volume fields. | same |
| Change / sign | `prdy_vrss_sign` String len 2: "전일 대비 부호 "1": 상한 "2": 상승 "3": 보합 "4": 하한 "5": 하락"; `prdy_vrss` Number "전일 종가 대비 등락 금액" (signed in example: `-1136000` with sign `"5"`); `prdy_ctrt` String "전일 종가 대비 등락률(%)" (example `"-11.93"`) | same three fields |
| Cumulative volume / value | `acml_vol` Number len 19: "장 시작부터 지금까지 체결된 주식 수를 모두 더한 값입니다. 개별 체결 수량이 아닙니다."; `acml_tr_pbmn` Number len 19: "장 시작부터 지금까지 체결된 거래대금을 모두 더한 값입니다." Currency not stated. | same |
| Venue per row | `exch_code` String len 1 "거래소코드": "체결이 이루어진 거래소 코드입니다. "1": KRX "2": 대체거래소(NXT) 통합("TJ")으로 조회하실 때만 채워지고, KRX("J")와 대체거래소("NJ")로 조회하실 때는 빈 값입니다." `altn_exch_ssn_id` len 2: "KRX 체결에는 "40", 대체거래소(NXT) 체결에는 "42" 가 내려옵니다. KRX("J")만 조회하시면 빈 값이고, 통합("TJ")으로 조회하시면 KRX 체결에도 값이 채워집니다. 값이 있다는 것만으로 대체거래소 체결이라고 보지 마시고 거래소코드(exch_code)로 가르십시오." `altn_exch_board_id` len 2: "대체거래소(NXT) 체결에는 "G1", KRX 체결에는 "G4"" + the same caveat. | **absent** (no `exch_code`, `altn_*`) |
| Trade id / sequence | **None** | None |
| JSON types | `prpr_hour`, `prdy_vrss_sign`, `prdy_ctrt`, `tday_rltv`, `exch_code`, `altn_*` String; prices, volumes, values Number (JSON integers in the example). M5 types: `string`/`number`. | same pattern |
| Ordering | newest first (field table) | newest first (field table) |

### 7.5 Semantics

- **Individual vs aggregate:** `/trades/ticks` rows are individual trades
  (field table). The example agrees: row-to-row `acml_vol` rises by 1 and
  `acml_tr_pbmn` by 8,389,000 = newer row's `stck_prpr` × `cntg_vol`
  (publisher example; values illustrative).
- **Time:** `HHMMSS`, second resolution, **no date** in the row and **no
  date/time input**; time zone **not documented**. Two example rows share
  `"195958"`.
- **Which trading day:** not stated (the ticks route, unlike Toss, does not
  say "당일"). **Inference:** the current or most recent trading day.
- **History depth:** the latest ≤40 trades only; no continuation key and no
  time filter, so earlier trades of the day are unreachable via this route.
- **Venue:** `J` / `NJ` / `TJ` selector; per-row exchange only with `TJ`
  (`exch_code` "1"/"2"). Cumulative fields are per selected market ("같은
  종목이라도 시장마다 누적거래량이 다릅니다").
- **Session coverage:** not documented. `altn_exch_ssn_id` distinguishes
  KRX ("40") vs NXT ("42"), not pre/regular/after sessions.
  - The example (`mrkt_div_code=J`) has trades at `195958`.
    **Inference:** KRX after-market trades appear under `J`; consistent with
    M6 L150 (publisher repo note): "2026-09-14 부터 KRX 시간외 단일가
    (16:00~18:00)가 애프터마켓(16:00~20:00, 실시간 체결)으로 바뀌어".
  - NXT pre-market under `NJ`/`TJ`: not documented.
- **Aggressor side:** not documented. `askp`/`bidp` at trade time are
  provided, but the example shows both as `0` at `195958` under `J`;
  when they are zero is not documented.

### 7.6 Limits

- **Rows per call:** up to 40 (portal-only statement, M1).
- **Rate:** M2 defers to notices (not retrieved). M5 `x-tps: "10"` on both
  routes (L8632, L8840); M7 L95 "`EGW00200` | 초당 호출 한도 초과 | API 당
  초당 10건입니다. 재시도 가능합니다"; M8 L120–121 adds that it arrives as
  HTTP 500 with `rsp_cd` `EGW00200` (publisher repo note). M8 L121 also says
  the publisher client throttles automatically (client policy, not a limit).

### 7.7 Contradictions and inferences

1. **`rsp_cd` success value does not hold for these routes.** M1 says
   `"0000"` = success. M6 L4–20 (publisher repo note) lists
   `market_trades_ticks` and `market_trades_minutes` under kind "응답 rsp_cd
   손상": "HTTP 200 과 정상 data 를 주면서 rsp_cd 에 널바이트가 섞여 옵니다.
   rsp_msg 는 빈 문자열입니다." Workaround: "data 가 있으면 정상으로
   보십시오. 이 API 들은 rsp_cd 로 성공을 판정할 수 없습니다." M10
   (publisher client code): an unprintable/blank `rsp_cd` on a listed API
   with empty `data` → `EMPTY_RESULT` failure (L652–658); with data →
   success flagged `verified=False` (L660–663). **Unverified** here.
2. **Empty list is ambiguous three ways.** Unregistered `iscd` → empty list
   with success code (M1); "no data" → `"0000"` + `[]` (M1); and with the
   `rsp_cd` corruption, the status code cannot separate them either.
   `IGW50006` (M7 L89) covers a wrong `mrkt_div_code` for an API, but the
   exact behaviour for `NJ` on a non-NXT symbol is not documented for this
   route (the candle route documents an empty array).
3. **Symbol format differs from candles.** Ticks/minutes: "6자리(005930)로
   넣으십시오"; candle routes accept "6자리(005930) 또는 A 를 붙인
   7자리(A005930)". `A`-prefixed input is undocumented here.
4. **`tr_cont` in the minutes example.** The minutes response example ends
   with `"tr_cont": "0"`, which its field table does not declare; the ticks
   example has none. M1 `rsp_msg` also mentions `tr_cont` generically.
5. **Minutes grouping.** The minutes example rows are at `180745` and
   `174755` (~10 minutes apart, not minute-aligned); combined with "한 행이
   1분 구간이라고 보지 마십시오", row interval and boundary convention are
   unknown. **Inference:** grouping varies or skips empty intervals.
6. **Same-second ties.** No sequence id and second-resolution time; equal
   `prpr_hour`/price/qty rows cannot be deduplicated across polls except,
   **inference**, via `acml_vol` (monotone per market in the example) —
   not documented as a key.
7. **`mac_address`.** Required header. M2's sample derives it from host
   interface discovery; that is **not** a pattern to copy (AGENTS.md).

## 8. Cross-broker comparison

### 8.1 Trade-row fields

`F` = field table, `E` = publisher example, `L` = legacy publisher example,
`C` = publisher client code, `G` = publisher guide, `—` = not found.

| Broker / route | Time field (format) | Date in row | Price | Quantity (signed?) | Side field | Cumulative vol | Venue per row | Trade id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KIS `inquire-ccnl` | `stck_cntg_hour` (not documented) — E | — | `stck_prpr` — E | `cntg_vol` (not documented) — E | — | — | — | — |
| KIS `itemconclusion` | `stck_cntg_hour` (not documented) — E | — | `stck_pbpr`? (§2.7) — E | `cnqn` (not documented) — E | — | `acml_vol` — E | — | — |
| Kiwoom `ka10003` | `tm` `HHmmss` — F | — | `cur_prc` signed — F | `cntr_trde_qty`, signed, meaning not stated — F+E | — | `acc_trde_qty` — F | `stex_tp` — F | — |
| Kiwoom `ka10084` | `tm` `HHmmss` — F | — | `cur_prc` signed — F | same as `ka10003` — F+E | — | `acc_trde_qty` — F | `stex_tp` — F (not in E) | — |
| Kiwoom `ka10055` | `cntr_tm` `HHmmss` — F | — | `cntr_pric` signed — F | `cntr_qty` unsigned in F, signed in E | — | `acc_trde_qty` — F | — | — |
| LS `t1301` | `chetime` String 10, `HHMMSS` in E — F+E | — | `price` Number 8 — F | `cvolume` Number 12 — F | — (day-cumulative `mdvolume`/`msvolume`, F) | `volume` — F | — | — |
| LS `t8454` | `chetime` String 10, `HHMMSS` in E — F+E | — | `price` — F | `cvolume` — F | — (same counters) | `volume` — F | `exchname` — F+E | — |
| LS `t1310` | `chetime`; U+0000 inside in E — F+E | — (`daygb` in request) | `price` — F | `cvolume`; minute-mode meaning not documented — F | — (same counters) | `volume` — F | `exchname` — F (not in E) | — |
| DB `CONCLUSION` | `Hour` String 16, `HHMMSS` in E — F+E | — | `Prpr` String 16 — F | `CntgVol` String 16; 19 of 20 E rows `"0"` — F+E | — | — | — | — |
| DB `DAYTRADE` | `Hour` — F+E | — | `Prpr` — F | `ShnuCnqn` / `SelnCnqn` String 10 — F | same two fields; assignment rule not documented — F | — | — | — |
| Toss `GET /api/v1/trades` | `timestamp` date-time with offset — F+E | yes | `price` decimal string — F | `volume` decimal string — F | — | — | — (integrated, G) | — |
| Meritz `/trades/ticks` | `prpr_hour` `HHMMSS` — F | — | `stck_prpr` Number — F | `cntg_vol` Number — F | — (`askp`/`bidp` at trade, F) | `acml_vol` — F | `exch_code` under `TJ` only — F | — |
| Meritz `/trades/minutes` (aggregate) | `cntg_hour` "집계 구간의 시각" — F | — | `stck_prpr` — F | `cntg_vol` "해당 구간의 체결 수량" — F | — | `acml_vol` — F | — | — |

### 8.2 Request controls

| Broker / route | Venue selector | Day selector | Time cursor / filter | Continuation | Rows per call |
| --- | --- | --- | --- | --- | --- |
| KIS `inquire-ccnl` | `J`/`NX`/`UN` — E | — (today, inferred) | — | — | 30 — L |
| KIS `itemconclusion` | `J`/`NX`/`UN` — E | — ("당일") | `FID_INPUT_HOUR_1` (before-time, L) | — | 30 — L |
| Kiwoom `ka10003` | `stk_cd` suffix — F | — | — | `cont-yn`/`next-key` — F | not documented |
| Kiwoom `ka10084` | `stk_cd` suffix — F | `tdy_pred` 1/2 — F | `tm` HHMM — F | `cont-yn`/`next-key` — F | not documented |
| Kiwoom `ka10055` | `stk_cd` suffix — F | `tdy_pred` 1/2 — F | — | `cont-yn`/`next-key` — F | not documented |
| LS `t1301` | **none** | — | `starttime`/`endtime` (format inferred `HHMM`) — F | `cts_time` + `tr_cont`/`tr_cont_key` — F | not documented |
| LS `t8454` | `exchgubun` (no description; E `"N"`) — F+E | — | `starttime`/`endtime` — F | same — F | not documented |
| LS `t1310` | `exchgubun` K/N/U — F | `daygb` 0/1 — F | `endtime` "chetime <= endtime" — F | same — F | not documented |
| DB `CONCLUSION` | `J`/`NJ`/`UJ` + `N-`/`U-` prefix — F | — | — | `cont_yn`/`cont_key` headers — F | not documented |
| DB `DAYTRADE` | same — F | — | session filter `InputHourClsCode` 1–10 — F | same — F | not documented |
| Toss `trades` | **none** (integrated, G) | — ("당일") | — | **none** — F+G | `count` 1–50, default 50 — F |
| Meritz `/trades/ticks` | `J`/`NJ`/`TJ` — F | — | — | **none** — F | ≤40 — F |
| Meritz `/trades/minutes` | `J`/`NJ`/`TJ` — F | — | — | none documented — F | ≤40 groups — F |

**Reading 8.1/8.2:**

- **Trade id:** none of the six brokers documents a trade id or sequence
  on any REST trade route. Toss explicitly says its WebSocket frames have
  no sequence field.
- **Aggressor side:** none of the six documents a per-trade aggressor
  side.
  - DB `DAYTRADE` reports per-row "매수체결량"/"매도체결량" with no
    assignment rule.
  - LS reports day-cumulative "매도/매수체결수량" counters, from which a
    side can only be inferred by differencing adjacent rows.
  - Kiwoom's REST quantity sign is undocumented; its meaning is documented
    only for the WebSocket feed.
  - KIS, Toss and Meritz have no side field.
- **Date and zone:** only Toss carries a date and an offset in each row.
  Every other route has `HHMMSS` only.
- **Ordering:** only Meritz documents row order (newest first) in a field
  table. Kiwoom, LS, DB and Toss examples are newest first; KIS has no
  example.
- **Depth:** Toss (≤50) and Meritz (≤40) return a latest-rows snapshot
  without continuation. KIS has a one-second time cursor. Kiwoom, LS and
  DB have continuation keys with undocumented boundaries.
- **Same field names, different row types:** Kiwoom `ka10084`
  (`tic_min`) and LS `t1310` (`timegb`) return minute rows under the
  trade field names. Meritz uses a separate `/trades/minutes` route.
- **Venue:** Toss has no selector and is KRX + NXT integrated. LS `t1301`
  has no selector and an undocumented venue. Per-row venue exists only on
  Kiwoom (`stex_tp`), LS `t8454`/`t1310` (`exchname`) and Meritz under
  `TJ` (`exch_code`).

## 9. Relation to existing repository documents

None of the files below is edited by this change. The differences are
recorded here only.

| Document and claim | This audit |
| --- | --- |
| [market-data spec](../specifications/market-data-v0.1-draft.md) §2: candidate interface lists `fetch_ticker`, `fetch_order_book`, `fetch_ohlcv` | No trade method is proposed there. Any `fetch_trades` needs a spec change and maintainer decision first (§10). |
| market-data spec §1 goal 4: "never invent a native exchange timestamp"; §5: "If the source gives only `HHMMSS`, require a verified trading date" (stated for minute candles) | Applies to every KIS, Kiwoom, LS, DB and Meritz trade route: all carry only `HHMMSS`. Toss rows carry a full timestamp. |
| [six-broker-ticker-decoders.md](six-broker-ticker-decoders.md) L9: individual trades are out of the ticker scope | Consistent. This file is evidence only and does not widen the ticker decoder. |
| [kis-market-data.md](kis-market-data.md) L42–44: real-time feeds should use WebSocket, so `fetch_ticker` must not promise tick-by-tick streaming | Consistent. The KIS REST trade routes found here are capped snapshots (30 rows per legacy sources), not a stream. |
| [kiwoom-market-data.md](kiwoom-market-data.md): portal quota "inquiries 5/s" | Not in this pin set; not re-verified here. |
| Capability inventory ([PR #32](https://github.com/kisbi3/ktradelink/pull/32), branch `claude/issue-17-capability-inventory` @ `cc761cd89a9fe15d179105381e4b1918b2f8765e`, not merged) row 4, KIS: `FHKST01010300` + `FHPST01060000` · EX | **Confirmed** at the same blobs. **Missing:** the after-hours route `FHPST02310000` `inquire-time-overtimeconclusion` (§2.2). |
| Same row, Kiwoom: `ka10003` 체결정보요청 · FT | **Confirmed**. `ka10084` 당일전일체결요청 (tick/minute, today/previous day, time cursor) and `ka10055` were also found (§3.2). |
| Same row, LS: `t1301` (2 TPS); `t8454` (통합, `exchgubun`) · FT | **Confirmed** (TPS 2 and 1). `t1310` 주식당일전일분틱조회 (tick/minute, today/previous day) was also found (§4.2). |
| Same row, DB: `CONCLUSION` `…/inquiry/hour-price` · SDK+FT | **Confirmed**. **Missing:** `DAYTRADE` 일별체결조회 `POST /api/v1/quote/kr-stock/inquiry/daily-price`, the only DB route with a buy/sell split and a session filter (§5.2). |
| Same row, Toss: `GET /api/v1/trades` (당일 최근 체결) · OAS | **Confirmed**; ≤50 rows, no pagination (§6). |
| Same row, Meritz: `ohhts_1002_001r` `GET /market/v1/trades/ticks` · FT | **Confirmed**. The aggregate sibling `ohhts_1002_002r` `/trades/minutes` is not a tick source (§7.2). |
| Same inventory, Meritz notes: "M4: REST 10 calls/s per account" (its M4, notice retrieved 06:57:52Z) | **Differs** from the Meritz repo's "API 당 초당 10건" (M7 L95, M8 L120). Not re-verified here (§7.1). |
| Same inventory: Kiwoom pin `953e5db…` "no longer reachable from any branch"; `c7a3d25…` identical tree `4eb7d549…` | **Confirmed** (§3.1); this file pins `c7a3d25…`. |
| Candle evidence ([PR #31](https://github.com/kisbi3/ktradelink/pull/31), branch `claude/issue-17-candle-evidence` @ `108e2b6b0226f9e67a4854e58c03789a3141df6e`, not merged): Kiwoom pin `953e5dbf` | Its Kiwoom blob pins stay valid under `c7a3d254` (same tree). |
| Candle evidence §6.5 / §8.2: Toss REST candle venue "not documented" | Toss FAQ (T4 L22, publisher guide), not cited there: "국내 캔들·체결은 KRX 만 집계하나요? … KRX + NXT 통합 시세입니다." That file could cite it; not changed here. |
| Candle evidence §7.8 / G-S2: Meritz `rsp_cd` NUL corruption on candle routes | The same publisher note (M6 L10–11) also lists `market_trades_ticks` and `market_trades_minutes` (§7.7). |
| [live-auth-transport-gates](live-auth-transport-gates-2026-11-05.md): Toss OpenAPI `1.2.28`, sha256 `c5918961335ccd6b…` | **Unchanged** at this retrieval (§6.1). |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any trade decoder, request plan or public
`fetch_trades` is written. Broker tags are in brackets.

### 10.1 Individual trades vs aggregates

- **G-I1:** a public trade object means **one execution**. Rows that may be
  per-time or per-minute aggregates must not be returned as trades.
  - [KIS] neither regular route documents the row type; legacy wording
    suggests executions. Blocked until a fixture shows it.
  - [Kiwoom] `ka10084` `tic_min=1` and [LS] `t1310` `timegb=0` return
    minute rows under the trade field names. Only the tick modes may be
    considered, and only after a fixture. LS `t1310` tick mode has no
    example at all.
  - [Kiwoom] `ka10003`/`ka10055`, [LS] `t1301`/`t8454` and [DB]
    `DAYTRADE` row types are inferred from examples only. [DB]
    `CONCLUSION` rests on publisher example-code prose. [Toss] and
    [Meritz] `/trades/ticks` are documented as individual trades.
  - [Meritz] `/trades/minutes` must never be decoded as ticks or as
    1-minute bars ("한 행이 1분 구간이라고 보지 마십시오").
  - [LS] `t1308` and the `t8411`/`t8453` tick charts, and [DB]
    `CHARTTICK`, are chart routes, not trade routes.
- **G-I2:** never merge a trade route with a candle route, and never
  synthesize trades from candles or cumulative-volume differences.
- **G-I3 Zero-quantity rows:** [DB] `CONCLUSION` rows with `CntgVol` `"0"`
  (19 of 20 example rows) must not become trades. Drop or flag them only
  under a rule a fixture or the publisher establishes. Never coerce a
  missing quantity to zero, or a zero row to a trade.

### 10.2 Aggressor side

- **G-S1 No inferred side:** no broker documents a per-trade aggressor
  side. Expose `side=None` unless a documented REST field gives it.
  - [KIS], [Toss], [Meritz] have no side field. `tday_rltv` / `chdegree`
    (체결강도) are ratios and must not be mapped to a side.
  - [Kiwoom] the `+`/`-` meaning is documented only for WebSocket `0B`.
    Do not transfer it to REST `cntr_trde_qty` without a REST field table
    or an authorized fixture compared against a known feed.
  - Never derive side from price vs best bid/ask ([KIS] `askp`/`bidp`,
    [Kiwoom] `pri_*_bid_unit`, [Meritz] `askp`/`bidp` "체결 시점의"): no
    publisher documents such a rule, and [Meritz] shows both as `0` in its
    example.
- **G-S2:** keep quantity magnitude and its sign separate. `abs()` on
  quantity is allowed only after the sign meaning is proven; until then a
  negative quantity must be kept signed or rejected, never silently
  dropped or flipped.
- **G-S3 [DB] `DAYTRADE` split:** `ShnuCnqn`/`SelnCnqn` may be exposed
  only as **broker-reported** "매수체결량"/"매도체결량", not as a verified
  aggressor side; the assignment rule is undocumented. A row where both or
  neither is non-zero fails closed. The example books the 15:30 closing
  print (1,321,868 shares) entirely as `SelnCnqn`, so auction prints carry
  a label that is not an aggressor side.
- **G-S4 [LS] side by differencing only:** LS rows carry day-cumulative
  `mdvolume`/`msvolume` counters, not a side. A side may be derived only by
  differencing two adjacent rows **within one response**. Across a page
  boundary, after a filtered row (`cvolume` filter) or where neither
  counter moves, the side is unknown. Volume in neither bucket
  (`volume` − `mdvolume` − `msvolume` > 0 in the `t1301`/`t1310`
  examples) means some prints are unclassified.

### 10.3 Trade id, dedup and ordering

- **G-D1 No synthesized id:** none of the six brokers documents a trade
  id. Never synthesize one (no hash of time+price+qty, no row index).
  - Identical rows are real: [Kiwoom] `ka10055` has two rows identical
    except for `acc_trde_qty`; [DB] `DAYTRADE` has four byte-identical
    `151959`/`73200`/`ShnuCnqn "1"` rows; [Meritz] has two `195958` rows.
- **G-D2 Dedup across pages or polls:** with no id, overlap can only be
  resolved by a verified monotonic field. Cumulative volume is a candidate
  where it exists ([KIS] `itemconclusion` `acml_vol`, [Kiwoom]
  `acc_trde_qty`, [LS] `volume`, [Meritz] `acml_vol`) but is unverified as
  strictly increasing per execution, and [Meritz] documents it as
  per-market. [DB] and [Toss] rows have no cumulative field, so overlap
  cannot be resolved at all. Until verified, overlapping pages raise
  `IncompleteMarketData`; do not drop "duplicates".
- **G-D3 Ordering:** row order is documented only by [Meritz] (newest
  first). [Kiwoom], [LS], [DB] and [Toss] examples are newest first; [KIS]
  has none. Sort by a verified key, never by example order, and never sort
  only on `HHMMSS` (ties within a second).
- **G-D4 Gaps:** the [Kiwoom] `ka10055` example has a cumulative gap.
  Detect gaps via cumulative volume where verified, and report
  incompleteness rather than interpolate.

### 10.4 Paging and completeness

- **G-P1:** finite page budget; raise `IncompleteMarketData` instead of
  truncating.
  - [KIS] `inquire-ccnl` has no cursor (30 rows, legacy).
    `itemconclusion` has only a one-second time cursor "이전체결" whose
    boundary (inclusive/exclusive) is undocumented; trades sharing the
    boundary second can be lost or repeated.
  - [Kiwoom] `cont-yn`/`next-key` boundaries and page size are
    undocumented; the examples' `MAX_PAGES = 10` is a client policy. The
    `ka10084` `tm` cursor direction is undocumented.
  - [LS] `cts_time` points at the oldest row's second plus an undocumented
    4-character suffix; whether that row repeats is undocumented. The
    `t1301` example's `cts_time` does not match its row.
  - [DB] header-only `cont_key` (request length 70, response 18); page
    size undocumented. The SDK's 100-page cap is a client policy.
  - [Toss] ≤50 and [Meritz] ≤40 latest rows with no continuation: never
    claim a complete day.
- **G-P2 Success with no data:** an empty row list is neither
  end-of-history nor proof that the symbol is valid.
  - [LS] `rsp_cd` `"00000"` with "해당자료가 없습니다." and no OutBlock
    (`t8411` example).
  - [DB] `00000` also carries "모의투자 데이터가 없습니다.".
  - [Meritz] an unregistered `iscd` returns an empty list with the success
    code, indistinguishable from "no data" (M1).
  - Stop only at a documented boundary.

### 10.5 Time, date and zone

- **G-T1 Date:** every [KIS], [Kiwoom], [LS], [DB] and [Meritz] trade row
  has time only (`HHMMSS`). A trade timestamp needs a trading date proven
  from the request and a verified exchange calendar, never the client
  clock.
  - [Kiwoom] `tdy_pred=2` and [LS] `t1310` `daygb=1` rows belong to the
    previous trading day, not "yesterday" by calendar.
  - [Meritz] does not even say which trading day `/trades/ticks` returns;
    expose time-of-day only, or require an explicit verified trading date.
  - [Toss] rows carry a full ISO-8601 timestamp with offset; parse it with
    its offset and keep milliseconds.
- **G-T2 Zone:** only [Toss] carries an offset. Asia/Seoul is an
  assumption to verify everywhere else (spec §5).
- **G-T3:** [KIS] do not fill an empty `FID_INPUT_HOUR_1` from the client
  clock (legacy K10 does); send only verified values.
- **G-T4 NUL characters:** the [LS] `t1310` example has U+0000 inside
  `chetime` and `cts_time` (`"100800\u0000000"`). Reject or strip it by an
  explicit, tested rule; never treat those fields as clean ASCII digits.

### 10.6 Venue and session

- **G-V1:** ship KRX only first; venue must be explicit.
  - [KIS] `J`/`NX`/`UN`; [Kiwoom] `_NX`/`_AL` suffix; [LS] `exchgubun`
    K/N/U; [DB] `J`/`NJ`/`UJ` plus the matching `N-`/`U-` prefix;
    [Meritz] `J`/`NJ`/`TJ`. These are not equivalent without evidence.
  - [Kiwoom] for a KRX or `_NX` request, a row whose `stex_tp` differs
    from the requested venue must raise, not be relabelled. `_AL` (SOR)
    rows stay unsupported until the meaning of "통합" is documented.
  - [LS] `t1301` has no venue selector and an undocumented venue: do not
    label it KRX. `exchgubun` silently maps invalid values to KRX
    ("그외 입력값은 KRX로 처리"), so validate before sending. Under `U`,
    require the per-row `exchname` (missing from the `t1310` example).
  - [DB] `UJ` rows carry no venue and cannot be attributed.
  - [Meritz] per-row `exch_code` exists only under `TJ`; do not infer NXT
    from `altn_exch_*` values (publisher warning).
- **G-V2 [Toss] integrated only:** Toss trades are "KRX + NXT 통합 시세"
  with no selector and no per-row venue (T4 L22). Its rows must never be
  labelled KRX; they need an integrated-scope label with that caveat, or
  the venue is unsupported.
- **G-V3 Session:** session coverage (pre-market, auctions, after-hours,
  NXT) is undocumented for most routes. `session="regular"` must error
  rather than mislabel.
  - [KIS] after-hours single-price trades have a separate route
    (`FHPST02310000`); do not mix its rows into a regular series.
  - [DB] `DAYTRADE` `InputHourClsCode` labels ("장전", "장후", "장종료",
    "예상") are undefined; send no default code without a maintainer
    decision.
  - [Meritz] the `J` example contains a `195958` trade; [LS] `t8454`
    example rows are NXT.

### 10.7 Status, types, units and signs

- **G-E1:** a missing or unreadable status is never success.
  - [KIS] `rt_cd == "0"`.
  - [Kiwoom] `return_code == 0`, but the `ka10084` example uses
    `returnCode`; the publisher examples and SDK treat a missing code as
    success. Do not copy that; decide the accepted key(s) from fixtures.
  - [LS] `rsp_cd` `"00000"` (examples only; not in the field tables).
  - [DB] `rsp_cd == "00000"` even on HTTP 200.
  - [Toss] HTTP status plus `ErrorResponse.error.code`; `result` and
    `error` never appear together. A 400 for a bad `count` is not listed.
- **G-E2 [Meritz] `rsp_cd` corruption:** the publisher repo note (M6
  L10–18) lists both trades routes among APIs whose HTTP 200 responses
  carry NUL bytes in `rsp_cd`, with an empty `rsp_msg`, and says to treat
  `data` as success. Errors arrive as HTTP 500. A corrupted `rsp_cd` with
  empty `data` must never become an empty success. Choose between the
  portal rule (`"0000"`) and the repo rule only after authorized fixtures.
- **G-U1 Decimals:** parse strictly; never use floats.
  - [Toss] `price`/`volume` are decimal **strings** (`format: decimal`);
    `currency` must tolerate unknown enum values.
  - [Kiwoom] all `String`, signed prices, signed `-0`.
  - [DB] every field is a string; `PrdyVrss`/`PrdyCtrt` are signed.
  - [LS] tables say Number, but `diff`/`chdegree` are strings in two
    formats (zero-padded and unpadded).
  - [Meritz] prices and volumes are JSON numbers.
  - [KIS] types are undocumented.
- **G-U2 Price and change signs:** decide per field whether `abs()` is
  permitted. [Kiwoom] `cur_prc`/`cntr_pric` are signed. [LS] `change` sign
  on a falling price is not exemplified, and `t1109` suggests `change` and
  `diff` differ. [DB]/[Meritz] change fields are signed. No sign-code list
  is documented for [KIS], [LS] or [DB] trade routes.
- **G-U3 Value units:** [Kiwoom] `acc_trde_prica` is 원 on `ka10003` and
  백만원 on `ka10084`/`ka10055`. [Meritz] `acml_tr_pbmn` currency is not
  stated. Do not share a unit.

### 10.8 Rate limits, retries, headers and environment

- **G-R1 Budgets:** [LS] `t8454` 1 TPS, `t1301`/`t1310` 2 TPS; [DB] 3 TPS
  per route plus an SDK-documented app-level 20 TPS; [Toss] `MARKET_DATA`
  15/s, shared with quotes and order book, adjustable (read
  `X-RateLimit-*`); [Meritz] 10/s per API (repo only); [Kiwoom] error codes
  `1700`–`1702` without numbers; [KIS] none in the pin.
- **G-R2 No automatic retries:** surface `RateLimitExceeded`. The [DB] SDK
  retries `IGW00201` automatically with back-off (D7 L65–71) and the
  [Meritz] client throttles itself; neither behaviour is adopted. Toss's
  429 back-off advice is not a licence for retry loops.
- **G-H1 `mac_address`:** [LS] and [DB] list it as required while saying
  it is for 법인/제휴사 only; [Meritz] requires it on both trades routes
  and rejects requests without it. It must come from explicit
  configuration, never from host discovery (the Meritz sample page derives
  it from the host; that is not copied), and must never be logged.
- **G-H2 Environment:** any call, paper or live, needs separate explicit
  authorization.
  - Paper availability is publisher-stated only: identical [KIS] TR ids;
    [Kiwoom] MOCK items, with `8104` possible; [DB] ⭕ in the SDK matrix
    on one shared origin.
  - [LS] documents no paper REST origin; [Toss] none.
  - [Meritz] has **no paper environment** ("모의계좌는 없습니다", M9
    L125), so even a read-only trade call needs explicit live
    authorization.

## 11. Not verified

- Any live or paper response for any route above. No broker API request
  was sent.
- Entitlements, real/paper parity and redistribution rights for all six
  brokers.
- Actual rate limits. The Meritz notice was not retrieved for this audit;
  the capability inventory's summary of it (10/s per account) differs
  from the Meritz repo (10/s per API), §7.1.
- KIS:
  - row type (execution vs time aggregate) on all three routes;
  - JSON types, units, sign codes, ordering and the envelope beyond
    `rt_cd` (the portal specification was not retrieved);
  - the `output1`/`output2` split of `itemconclusion` and the meaning of
    `stck_pbpr`;
  - the 30-row cap (legacy only) and `FID_INPUT_HOUR_1` boundary
    semantics;
  - session coverage of `J`/`NX`/`UN`, and whether after-hours trades
    appear in the regular routes.
- Kiwoom:
  - meaning of the REST quantity sign;
  - row type for `ka10003`/`ka10055`, and `ka10084` minute-row semantics;
  - page size, continuation boundaries, `tm` direction and intraday depth;
  - `stex_tp` behaviour for `_AL` (SOR) requests;
  - which envelope key (`return_code` vs `returnCode`) `ka10084` returns.
- LS:
  - row type of `t1301` (one example row) and `t1310` tick mode (no
    example);
  - the 매도/매수 assignment rule and the unclassified volume;
  - what `exchgubun` `U` returns and `t1301`'s venue and session coverage;
  - the `cts_time` suffix, page overlap and page size;
  - history depth of `t1301`/`t8454`; time zone;
  - the `change` sign on a falling price.
- DB:
  - page size and ordering beyond the examples;
  - the zero-quantity `CONCLUSION` rows;
  - the `ShnuCnqn`/`SelnCnqn` assignment rule, including auction prints;
  - `NJ`/`UJ` behaviour and the meaning of the `InputHourClsCode` labels;
  - history depth, time zone and paper data availability.
- Toss:
  - row ordering (examples only);
  - REST session coverage, including the KRX after-market;
  - behaviour before the first trade and on holidays;
  - a 400 for an out-of-range `count`;
  - whether `volume` can be fractional for KRX.
- Meritz:
  - the `rsp_cd` NUL-byte behaviour on the trades routes (repo note only);
  - which trading day is returned, and the time zone;
  - NXT pre-market rows; `NJ` on a non-NXT symbol;
  - the meaning of `askp`/`bidp` = 0;
  - the `/trades/minutes` grouping interval.
- Holiday, suspended-trading, VI and partial-session behaviour on every
  route.
