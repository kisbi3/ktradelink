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
  value or order was used. Only public Git repositories (and, for the
  brokers in §4–§7, public documentation pages) were fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS and Kiwoom: fixed Git commits, fetched 07:00–07:17 with `git fetch`
    of the pinned SHA from `github.com`.
  - LS, DB, Toss and Meritz: see §4.1, §5.1, §6.1 and §7.1 (pending).
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
  - `publisher repo note`: non-code text in a publisher repository.
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- Sample values in publisher examples are illustrative. They are **not**
  authorized response fixtures.

## 1. Broker × property summary

Cell format: short verdict — evidence. `F` field table, `E` publisher
example, `L` legacy publisher example, `C` publisher client code, `N`
publisher repo note, `—` not found. "pending" = section not yet merged.

| Property | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Route(s) | `FHKST01010300` GET `…/quotations/inquire-ccnl` 주식현재가 체결; `FHPST01060000` GET `…/quotations/inquire-time-itemconclusion` 당일시간대별체결; after-hours `FHPST02310000` `…/inquire-time-overtimeconclusion` — E | `ka10003` 체결정보요청; `ka10084` 당일전일체결요청; `ka10055` 당일전일체결량요청; all POST `/api/dostk/stkinfo` — F+E | pending | pending | pending | pending |
| Individual trade vs aggregate | **not documented** for any route. Legacy wording "체결 내역 30건" (L). Inference only. | `ka10003`: not stated; example cumulative deltas match each row's quantity (E, inference). `ka10084`: request selects `tic_min` "0:틱, 1:분" with **one** response table (F) — row type depends on the request. | pending | pending | pending | pending |
| Timestamp / date in row | `stck_cntg_hour` "주식 체결 시간"; format not documented; **no date field** — E | `tm` / `cntr_tm` "HHmmss"; **no date field** — F | pending | pending | pending | pending |
| Aggressor side | **none** on any route; `tday_rltv` "당일 체결강도" is a ratio, not a side — E | **not documented** for REST. Quantity is "부호가 포함된 숫자" (F) and examples carry `-` quantities (E); the meaning is documented **only** on WebSocket `0B` ("+는 매수체결,-는 매도체결", F). | pending | pending | pending | pending |
| Trade id / sequence | none — E | none — F | pending | pending | pending | pending |
| Pagination | `inquire-ccnl`: none. `itemconclusion`: time cursor `FID_INPUT_HOUR_1` "기준시간-이전체결처리" (L); boundary undocumented — E+L | `cont-yn` / `next-key` headers on all three (F); boundary undocumented. `ka10084` also `tm` HHMM (F). | pending | pending | pending | pending |
| History depth / rows per call | `inquire-ccnl` "최근30건" (L); `itemconclusion` "당일" by title (E), "30건" (L) | rows per page not documented; `ka10084`/`ka10055` `tdy_pred` "당일 : 1, 전일 : 2" (F); `ka10003` not documented | pending | pending | pending | pending |
| Venue selector | `FID_COND_MRKT_DIV_CODE` "J:KRX, NX:NXT, UN:통합" on both regular routes (E); after-hours route "J:주식/ETF/ETN" only (E) | `stk_cd` suffix "KRX:039490,NXT:039490_NX,SOR:039490_AL" (F); per-row `stex_tp` "KRX , NXT , 통합" on `ka10003`/`ka10084` (F) | pending | pending | pending | pending |

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

*Pending: section to be merged from the LS/DB research.*

## 5. DB Securities

*Pending: section to be merged from the LS/DB research.*

## 6. Toss Securities

*Pending: section to be merged from the Toss/Meritz research.*

## 7. Meritz Securities

*Pending: section to be merged from the Toss/Meritz research.*

## 8. Cross-broker comparison

### 8.1 Trade-row fields

`F` = field table, `E` = publisher example, `L` = legacy publisher example,
`—` = not found.

| Broker / route | Time field (format) | Date in row | Price | Quantity (signed?) | Side field | Cumulative vol | Venue per row | Trade id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KIS `inquire-ccnl` | `stck_cntg_hour` (not documented) — E | — | `stck_prpr` — E | `cntg_vol` (not documented) — E | — | — | — | — |
| KIS `itemconclusion` | `stck_cntg_hour` (not documented) — E | — | `stck_pbpr`? (§2.7) — E | `cnqn` (not documented) — E | — | `acml_vol` — E | — | — |
| Kiwoom `ka10003` | `tm` `HHmmss` — F | — | `cur_prc` signed — F | `cntr_trde_qty`, signed, meaning not stated — F+E | — | `acc_trde_qty` — F | `stex_tp` — F | — |
| Kiwoom `ka10084` | `tm` `HHmmss` — F | — | `cur_prc` signed — F | same as `ka10003` — F+E | — | `acc_trde_qty` — F | `stex_tp` — F (not in E) | — |
| Kiwoom `ka10055` | `cntr_tm` `HHmmss` — F | — | `cntr_pric` signed — F | `cntr_qty` unsigned in F, signed in E | — | `acc_trde_qty` — F | — | — |
| LS | pending | pending | pending | pending | pending | pending | pending | pending |
| DB | pending | pending | pending | pending | pending | pending | pending | pending |
| Toss | pending | pending | pending | pending | pending | pending | pending | pending |
| Meritz | pending | pending | pending | pending | pending | pending | pending | pending |

### 8.2 Request controls

| Broker / route | Venue selector | Day selector | Time cursor | Continuation | Rows per call |
| --- | --- | --- | --- | --- | --- |
| KIS `inquire-ccnl` | `J`/`NX`/`UN` — E | — (today, inferred) | — | — | 30 — L |
| KIS `itemconclusion` | `J`/`NX`/`UN` — E | — ("당일") | `FID_INPUT_HOUR_1` (before-time, L) | — | 30 — L |
| Kiwoom `ka10003` | `stk_cd` suffix — F | — | — | `cont-yn`/`next-key` — F | not documented |
| Kiwoom `ka10084` | `stk_cd` suffix — F | `tdy_pred` 1/2 — F | `tm` HHMM — F | `cont-yn`/`next-key` — F | not documented |
| Kiwoom `ka10055` | `stk_cd` suffix — F | `tdy_pred` 1/2 — F | — | `cont-yn`/`next-key` — F | not documented |
| LS / DB / Toss / Meritz | pending | pending | pending | pending | pending |

**Reading 8.1/8.2 (KIS and Kiwoom only, pending the other four):**

- Neither broker documents a trade id, a per-row date, a time zone, row
  order or an aggressor side for its REST trade routes.
- Kiwoom has field tables; KIS has column names only.
- Kiwoom's quantity sign is documented as present but not explained on
  REST; KIS has no side information at all.

## 9. Relation to existing repository documents

None of the files below is edited by this change.

| Document and claim | This audit |
| --- | --- |
| [market-data spec](../specifications/market-data-v0.1-draft.md) §2: candidate interface lists `fetch_ticker`, `fetch_order_book`, `fetch_ohlcv` | No trade method is proposed there. Any `fetch_trades` needs a spec change and maintainer decision first (§10). |
| market-data spec §1 goal 4: "never invent a native exchange timestamp"; §5: "If the source gives only `HHMMSS`, require a verified trading date" (stated for minute candles) | Applies to every KIS and Kiwoom trade route: all carry only `HHMMSS` (§2.5, §3.5). |
| [six-broker-ticker-decoders.md](six-broker-ticker-decoders.md) L9: individual trades are out of the ticker scope | Consistent. This file is evidence only and does not widen the ticker decoder. |
| [kis-market-data.md](kis-market-data.md) L42–44: real-time feeds should use WebSocket, so `fetch_ticker` must not promise tick-by-tick streaming | Consistent. The REST trade routes found here are capped snapshots (30 rows per legacy sources), not a stream. |
| [kiwoom-market-data.md](kiwoom-market-data.md): portal quota "inquiries 5/s" | Not in this pin set; not re-verified here. |
| Capability inventory (branch `claude/issue-17-capability-inventory` @ `cc761cd89a9fe15d179105381e4b1918b2f8765e`, not merged) row 4: KIS `FHKST01010300` + `FHPST01060000` · EX | **Confirmed** at the same blobs. A third, after-hours route `FHPST02310000` exists (§2.2). |
| Same row: Kiwoom `ka10003` 체결정보요청 · FT | **Confirmed**. `ka10084` 당일전일체결요청 (tick/minute, today/previous day, time cursor) and `ka10055` were also found. |
| Same inventory: Kiwoom pin `953e5db…` "no longer reachable from any branch"; `c7a3d25…` identical tree `4eb7d549…` | **Confirmed** (§3.1); this file pins `c7a3d25…`. |
| Candle evidence (branch `claude/issue-17-candle-evidence` @ `108e2b6b0226f9e67a4854e58c03789a3141df6e`, not merged): Kiwoom pin `953e5dbf` | Its Kiwoom blob pins stay valid under `c7a3d254` (same tree). That file is not changed here. |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any trade decoder, request plan or public
`fetch_trades` is written. Broker tags are in brackets.

### 10.1 Individual trades vs aggregates

- **G-I1:** a public trade object means **one execution**. Rows that may be
  per-time or per-minute aggregates must not be returned as trades.
  - [KIS] neither regular route documents the row type; legacy wording
    suggests executions. Blocked until a fixture shows it.
  - [Kiwoom] `ka10084` `tic_min=1` returns minute rows with the trade field
    names. Only `tic_min=0` may be considered, and only after a fixture.
    `ka10003` and `ka10055` row type is inferred from examples only.
- **G-I2:** never merge a trade route with a minute-candle route, and never
  synthesize trades from candles or cumulative-volume differences.

### 10.2 Aggressor side

- **G-S1:** no inferred side. Expose `side=None` unless a documented REST
  field gives it.
  - [KIS] no side field on any REST trade route. `tday_rltv` (체결강도)
    is a ratio and must not be mapped to a side.
  - [Kiwoom] the `+`/`-` meaning is documented only for WebSocket `0B`.
    Do not transfer it to REST `cntr_trde_qty` without a REST field table
    or an authorized fixture compared against a known feed.
  - Never derive side from price vs best bid/ask (`askp`/`bidp`,
    `pri_*_bid_unit`): their timing relative to the trade is undocumented.
- **G-S2:** keep quantity magnitude and its sign separate. `abs()` on
  quantity is allowed only after the sign meaning is proven; until then a
  negative quantity must be kept signed or rejected, never silently
  dropped or flipped.

### 10.3 Trade id, dedup and ordering

- **G-D1:** never synthesize a trade id (no hash of time+price+qty, no row
  index). No route documents one.
  - [Kiwoom] the `ka10055` example has two rows identical except for
    `acc_trde_qty` — a `(time, price, qty)` key would merge real trades.
- **G-D2 Dedup across pages:** with no id, overlap can only be resolved by
  a verified monotonic field. `acc_trde_qty` is a candidate [KIS
  `itemconclusion`, Kiwoom all three] but is unverified as strictly
  increasing per execution. Until verified, overlapping pages raise
  `IncompleteMarketData`; do not drop "duplicates".
- **G-D3 Ordering:** row order is undocumented for every route; examples
  [Kiwoom] are newest first, [KIS] has none. Sort by a verified key, never
  by example order, and never sort only on `HHMMSS` (ties within a second).
- **G-D4 Gaps:** the `ka10055` example has a cumulative gap. Detect gaps
  via cumulative volume where verified, and report incompleteness rather
  than interpolate.

### 10.4 Paging and completeness

- **G-P1:** finite page budget; raise `IncompleteMarketData` instead of
  truncating.
  - [KIS] `inquire-ccnl` has no cursor (30 rows, legacy). `itemconclusion`
    has only a one-second time cursor "이전체결" whose boundary
    (inclusive/exclusive) is undocumented; trades sharing the boundary
    second can be lost or repeated.
  - [Kiwoom] `cont-yn`/`next-key` boundaries and page size are
    undocumented; the examples' `MAX_PAGES = 10` is a client policy. The
    `ka10084` `tm` cursor direction is undocumented.
- **G-P2:** an empty page is not end-of-history unless a documented
  boundary says so.

### 10.5 Time, date and zone

- **G-T1:** every KIS and Kiwoom trade row has time only (`HHMMSS`). A
  trade timestamp needs a trading date proven from the request
  (`tdy_pred`, "당일") and a verified exchange calendar, never the client
  clock. [Kiwoom] `tdy_pred=2` rows belong to the previous trading day,
  not "yesterday" by calendar.
- **G-T2:** time zone is undocumented for all routes; Asia/Seoul is an
  assumption to verify (spec §5).
- **G-T3:** [KIS] do not fill an empty `FID_INPUT_HOUR_1` from the client
  clock (legacy K10 does); send only verified values.

### 10.6 Venue and session

- **G-V1:** ship KRX only first; venue must be explicit.
  - [KIS] `J`/`NX`/`UN`; [Kiwoom] `_NX`/`_AL` suffix. These are not
    equivalent without evidence.
  - [Kiwoom] for a KRX or `_NX` request, a row whose `stex_tp` differs
    from the requested venue must raise, not be relabelled. `_AL` (SOR)
    rows stay unsupported until the meaning of "통합" is documented.
- **G-V2:** session coverage (pre-market, auctions, after-hours, NXT) is
  undocumented for all routes. [KIS] after-hours single-price trades have a
  separate route (`FHPST02310000`); do not mix its rows into a regular
  series. `session="regular"` must error rather than mislabel.

### 10.7 Status, types, units and signs

- **G-E1:** a missing or unreadable status is never success. [KIS]
  `rt_cd == "0"`. [Kiwoom] `return_code == 0`, but the `ka10084` example
  uses `returnCode`; the publisher examples and SDK treat a missing code as
  success. Do not copy that; decide the accepted key(s) from fixtures.
- **G-U1:** parse decimals strictly; no floats. [KIS] JSON types are
  undocumented. [Kiwoom] all `String`, signed prices, signed `-0`.
- **G-U2:** price sign — [Kiwoom] `cur_prc`/`cntr_pric` are signed numbers;
  the example signs match the change direction. Decide per field whether
  `abs()` is permitted (as for candles).
- **G-U3:** cumulative value — [Kiwoom] `acc_trde_prica` is 원 on
  `ka10003` and 백만원 on `ka10084`/`ka10055`. Do not share a unit.

### 10.8 Rate limits, retries and environment

- **G-R1:** [KIS] no documented quota in the pin; [Kiwoom] error codes
  `1700`–`1702` without numbers. Surface `RateLimitExceeded`; no retry
  loops.
- **G-H1:** paper availability is publisher-stated only (identical KIS TR
  ids; Kiwoom MOCK items, with `8104` possible). Any call, paper or live,
  needs separate explicit authorization.

## 11. Not verified

- Any live or paper response for any route above. No broker API request
  was sent.
- Entitlements, real/paper parity and redistribution rights.
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
- LS, DB, Toss, Meritz: pending (§4–§7).
- Holiday, suspended-trading, VI and partial-session behaviour on every
  route.
