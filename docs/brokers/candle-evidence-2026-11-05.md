# Six-broker candle (OHLCV) evidence — 2026-11-05

- **Scope:** domestic-equity candle routes for minute, day, week and month
  intervals, plus year where a broker documents it. Brokers: KIS, Kiwoom
  REST, LS, DB, Toss and Meritz. The Shinhan comparison stays separate.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No KTradeLink candle decoder or request plan exists, and
  this file does not authorize one.
- **No broker API request was sent.** No token, credential, account, MAC
  value or order was used. Only public documentation pages, publisher JSON
  documentation endpoints and public Git repositories were fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS and Kiwoom: fixed Git commits, fetched 06:39–06:45 from
    `raw.githubusercontent.com` at the pinned SHA.
  - LS and DB portal pages: 06:42–06:50. The DB SDK was fetched at a
    fixed commit.
  - Toss and Meritz portal pages: 06:43–06:49. The Meritz GitHub
    repository was fetched at a fixed commit.
- **Pin formats:**
  - Git blob SHAs are `sha1("blob <len>\0" + bytes)` of the retrieved
    bytes, i.e. what `git hash-object` prints.
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
  - `publisher repo note`: non-code text in a publisher repository that
    defers to the portal (§7.1).
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- Sample values in publisher examples are illustrative. They are **not**
  authorized response fixtures.

## 1. Broker × interval summary

Cell format: route — evidence; A = adjustment, P = pagination.

- Evidence: `F` field table, `E` publisher example, `C` publisher client
  code, `N` publisher repo note.
- A and P values:
  - `doc`: documented.
  - `partial`: documented with gaps, which the broker section explains.
  - `none`: not documented.
  - `no input`: the route has no such selector.
  - `contra.`: the sources contradict each other.

| Broker | Minute | Day | Week | Month | Year |
| --- | --- | --- | --- | --- | --- |
| KIS | `FHKST03010200` (today only) and `FHKST03010230` (by date) — E; size not documented; A no input; P partial (time cursor) | `FHKST03010100` `D` — E; A contra. (§2.8); P partial (date window, ≤100 rows) | same route `W` — E; A contra.; P partial | same route `M` — E; A contra.; P partial | same route `Y` — E; A contra.; P partial |
| Kiwoom REST | `ka10080` `tic_scope` 1–60 — F+E; A flag, meaning not stated; P doc | `ka10081` — F+E; A doc (`1` adjusted, `base_dt`-relative; `0` not stated); P doc | `ka10082` — F+E; A flag, meaning not stated; P doc | `ka10083` — F+E; A flag, meaning not stated; P doc | `ka10094` — F+E; A flag, meaning not stated; P doc |
| LS | `t8412` / `t8452` (`ncnt` n분) — F+E; A no input; P partial (`cts_*` + `tr_cont`) | `t8410` / `t8451` `gubun` 2, `t1305` — F+E; A doc (`sujung` Y/N; t1305 no input); P partial | `gubun` 3 (and t1305) — F only; A doc; P partial | `gubun` 4 (and t1305) — F only; A doc; P partial | `gubun` 5 — F only; A doc; P partial |
| DB | `CHARTMIN` (`InputDivXtick` seconds) — F+C+E (example inconsistent); A doc (`InputOrgAdjPrc` 0/1); P partial (`cont_yn`/`cont_key`) | `CHARTDAY` — F+C+E; A doc; P partial | `CHARTWEEK` — F+C+E; A doc; P partial | `CHARTMONTH` `M` — F+C+E; A doc; P partial | `CHARTMONTH` `Y` — F+C; A doc; P partial |
| Toss | `GET /api/v1/candles` `1m` — F+E; A doc (default `true`; effect on `1m` not stated); P doc (`before` inclusive) | same route `1d` — F+E; A doc (default `true`); P doc | not offered (400, allowed `1m`,`1d`) | not offered | not offered |
| Meritz | `GET /market/v1/candles/minutes` (`hour_cls_code` seconds) — F+E; A no input; P documented as none (latest 40) | `GET /market/v1/candles/days` — F+E+C; A doc (default `0` = adjusted); P partial (`from`+`to` ≤ 1 year, no cursor) | not found for equities (index only) | not found for equities | not found for equities |

## 2. KIS (Korea Investment & Securities)

### 2.1 Pinned sources

All sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362).
The full SHA is `3a9be59a3ed8745720dc3aa9d584bdf3b7830362` and the commit is
dated 2026-10-28T00:26:05+09:00. Paths are relative to the repository root.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | [`examples_llm/domestic_stock/inquire_daily_itemchartprice/inquire_daily_itemchartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_daily_itemchartprice/inquire_daily_itemchartprice.py) | `77f0eac28baba0c55a87ad05cc2aba67c12b73f6` | D/W/M/Y route, request fields, 100-row note |
| K2 | [`…/inquire_daily_itemchartprice/chk_inquire_daily_itemchartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_daily_itemchartprice/chk_inquire_daily_itemchartprice.py) | `e6ea734d0a938069a3bf58f3c530717564fcef2f` | `output1`/`output2` column names. This is the same blob ADR 0003 inspected. |
| K3 | [`…/inquire_daily_price/inquire_daily_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_daily_price/inquire_daily_price.py) | `2e68aa79ecba8407405843e51071346615c53414` | Recent-30 D/W/M route, its adjustment wording |
| K4 | [`…/inquire_daily_price/chk_inquire_daily_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_daily_price/chk_inquire_daily_price.py) | `003326208ac6bb74631bf24465ca64c057891f62` | `output` column names |
| K5 | [`…/inquire_time_itemchartprice/inquire_time_itemchartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_itemchartprice/inquire_time_itemchartprice.py) | `92385310e762d5ecd29fd984949b42a9e3933e6a` | Today-only minute route |
| K6 | [`…/inquire_time_itemchartprice/chk_inquire_time_itemchartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_itemchartprice/chk_inquire_time_itemchartprice.py) | `09d2b67dbb96024bf45d12ff7393aa83e141202f` | Minute column names |
| K7 | [`…/inquire_time_dailychartprice/inquire_time_dailychartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_dailychartprice/inquire_time_dailychartprice.py) | `aafa68e6f9cb8b06453f98ad63f954b096e3d7bb` | Minute-by-date route |
| K8 | [`…/inquire_time_dailychartprice/chk_inquire_time_dailychartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_dailychartprice/chk_inquire_time_dailychartprice.py) | `ad467c33e94f07a449a9376a3d41a05d59580413` | Minute-by-date column names |
| K9 | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) | `0e722d6f3253033efe3cf2b99845397b2b329655` | Transport: method, headers, origins, `rt_cd`. This blob is identical to the `examples_user/kis_auth.py` blob pinned in [live-auth-transport-gates](live-auth-transport-gates-2026-11-05.md). |
| K10 | [`MCP/Kis Trading MCP/configs/domestic_stock.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/configs/domestic_stock.json) | `e82a0829ef519c64dfecb3e966ed217b4fcd3805` | Publisher registry. Parameter descriptions are identical to K1, K3 and K5. |
| K11 | [`examples_user/domestic_stock/domestic_stock_functions.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_user/domestic_stock/domestic_stock_functions.py) | `e585487d112409af59a64ad135cfc9440b266e72` | L4473–4555 and L4628–4690 repeat K1/K3 verbatim |
| K12 | [`backtester/kis_backtest/providers/kis/data.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/kis_backtest/providers/kis/data.py) | `28bf9aca834e4abd7c0b4b63ab0b9be61678de13` | Publisher client code only. It shows paging habits and is **not** a contract. |

**Missing evidence:**

- None of K1–K12 contains a KIS field table: no JSON types, lengths or
  units.
- None contains a sample response body.
- The KIS developer-portal specification was **not** retrieved for this
  audit.
- Every response-side statement below is therefore limited to column
  *names*.

### 2.2 Routes by interval

All routes are `GET` with query parameters. K9 L472–476 uses `requests.get(url,
headers=headers, params=params)` unless `postFlag` is set, and none of K1/K3/K5/K7
sets it. The origins are the K9 L150–154 comments:
`https://openapi.koreainvestment.com:9443` (실전) and
`https://openapivts.koreainvestment.com:29443` (모의).

| Interval | Route (title in source) | Path | TR id | Separate route or period code? | Interval codes (verbatim) | Real / paper | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| minute (today only) | 주식당일분봉조회 [v1_국내주식-022] (K5 L19) | `/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice` | `FHKST03010200` for real and demo (K5 L80) | separate route | no minute-size field; size **not documented** | "실전계좌/모의계좌의 경우, 한 번의 호출에 최대 30건" (K5 L35) | publisher example |
| minute (by date) | 주식일별분봉조회 [국내주식-213] (K7 L19) | `/uapi/domestic-stock/v1/quotations/inquire-time-dailychartprice` | `FHKST03010230` (K7 L71, no real/demo switch) | separate route | no minute-size field; size **not documented** | "실전계좌의 경우, 한 번의 호출에 최대 120건" (K7 L36); paper **not stated** | publisher example |
| day / week / month / year | 국내주식기간별시세(일/주/월/년) [v1_국내주식-016] (K1 L19) | `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice` | `FHKST03010100` for real and demo (K1 L79–84) | one route, period code | `FID_PERIOD_DIV_CODE`: "D:일봉 W:주봉, M:월봉, Y:년봉" (K1 L44) | "실전계좌/모의계좌의 경우, 한 번의 호출에 최대 100건" (K1 L36) | publisher example |
| day / week / month (recent 30) | 주식현재가 일자별 [v1_국내주식-010] (K3 L18) | `/uapi/domestic-stock/v1/quotations/inquire-daily-price` | `FHKST01010400` for real and demo (K3 L69–74) | one route, period code | "D:(일)최근 30거래일, W:(주)최근 30주, M:(월)최근 30개월" (K3 L28) | not stated beyond identical TR id | publisher example |

Request headers (names only, K9 L61–66, L266–268, L457–459):

- `Content-Type`, `Accept`, `charset`, `User-Agent`;
- `authorization`, `appkey`, `appsecret`;
- `tr_id`, `custtype`, `tr_cont`.

For TR ids starting with `T`, `J` or `C`, K9 L453–455 rewrites the first
letter to `V` in paper mode. All four candle TR ids start with `F`, so the
sample sends the same id in both environments.

### 2.3 Request fields

| Concern | `inquire-daily-itemchartprice` (K1) | `inquire-daily-price` (K3) | `inquire-time-itemchartprice` (K5) | `inquire-time-dailychartprice` (K7) |
| --- | --- | --- | --- | --- |
| Symbol | `FID_INPUT_ISCD`, "종목코드 (ex 005930 삼성전자)" | same | `FID_INPUT_ISCD` "(ex. 123456)" | same |
| Venue | `FID_COND_MRKT_DIV_CODE` "J:KRX, NX:NXT, UN:통합" (K1 L40) | same codes (K3 L36) | same codes (K5) | "J:주식,NX:NXT,UN:통합" (K7) — `J` labelled 주식, not KRX |
| Range | `FID_INPUT_DATE_1` "조회 시작일자", `FID_INPUT_DATE_2` "조회 종료일자 (최대 100개)" (K1 L42–43). Example `"20220101"`, `"20220809"` (K1 L51): 8-digit `YYYYMMDD` (**Inference** from the example) | none; recent 30 periods only | `FID_INPUT_HOUR_1` "입력 시간1 (ex. 입력시간)"; chk example `"093000"` (K6) | `FID_INPUT_DATE_1` "(ex. 20241023)", `FID_INPUT_HOUR_1` "(ex. 130000)" |
| Period | `FID_PERIOD_DIV_CODE` D/W/M/Y | `FID_PERIOD_DIV_CODE` D/W/M | n/a | n/a |
| Adjustment | `FID_ORG_ADJ_PRC` "수정주가 원주가 가격 여부 (ex. 0:수정주가 1:원주가)" (K1 L45) | `FID_ORG_ADJ_PRC` "수정주가 원주가 가격 (ex. 0:수정주가미반영, 1:수정주가반영, *수정주가는 액면분할/액면병합 등 권리 발생 시 과거 시세를 현재 주가에 맞게 보정한 가격)" (K3 L29) — **opposite mapping**, see §2.8 | **no adjustment field** | **no adjustment field** |
| Other | — | — | `FID_PW_DATA_INCU_YN` "과거 데이터 포함 여부" (meaning of values not documented); `FID_ETC_CLS_CODE` "기타 구분 코드" (values not documented; sample sends `""`) | `FID_PW_DATA_INCU_YN` default `"N"`; `FID_FAKE_TICK_INCU_YN` "허봉 포함 여부" (default `""`, values not documented) |
| Page size | none; "최대 100건" per call | none; 30 periods | none; 30 per call | none; 120 per call (real) |
| Continuation | Sample sends `tr_cont=""` (K1 L95). No continuation key is documented for this route. The documented range control is the date pair. | none documented | Sample sends `tr_cont=""`. The time cursor is `FID_INPUT_HOUR_1`. | same as K5, plus `FID_INPUT_DATE_1` |

`tr_cont` header semantics are not documented in K1–K11 for these routes.
K12 L374–427 uses response-header `tr_cont` values `M`/`F` and request `N`
only for an *overseas* daily route. That shows nothing about domestic
candles.

### 2.4 Response

| Concern | Day/week/month/year (K1/K2) | Recent-30 (K3/K4) | Minute (K5/K6, K7/K8) |
| --- | --- | --- | --- |
| Envelope | `rt_cd`; K9 L351–357 treats `rt_cd == "0"` as OK. `msg_cd`, `msg1` (K9 L322–323). HTTP status other than 200 is an error (K9 L478–485). | same | same |
| Candle array | `output2` ("array 타입", K1 L101–102); `output1` is a summary object | `output` ("array 자료형", K3 L86–87) | `output2` array, `output1` object (K5, K7) |
| Date / time | `stck_bsop_date` "주식 영업 일자" (K2 L52) | `stck_bsop_date` (K4 L22) | `stck_bsop_date` "주식 영업일자", `stck_cntg_hour` "주식 체결시간" (K6 L30–31; K8 L31–32) |
| OHLC | `stck_oprc` "주식 시가2", `stck_hgpr`, `stck_lwpr`, `stck_clpr` "주식 종가" (K2 L53–56) | same four (K4 L23–26) | `stck_oprc`, `stck_hgpr`, `stck_lwpr`, and `stck_prpr` "주식 현재가" as the bar's last price. There is **no** `stck_clpr` in the minute mapping. |
| Volume / value | `acml_vol` "누적 거래량", `acml_tr_pbmn` "누적 거래 대금" (K2 L57–58) | `acml_vol` | `cntg_vol` "체결 거래량", `acml_tr_pbmn` "누적 거래대금" |
| Adjustment metadata | `flng_cls_code` "락 구분 코드", `prtt_rate` "분할 비율", `mod_yn` "변경 여부", `revl_issu_reas` "재평가사유코드" (K2 L59–64) | `flng_cls_code`, `acml_prtt_rate` "누적 분할 비율" | — |
| Direction | `prdy_vrss`, `prdy_vrss_sign` "전일 대비 부호" | same | same in `output1` |
| JSON types / units | **not documented** | **not documented** | **not documented** |
| Price sign | not documented | not documented | not documented |
| Ordering | not documented | not documented | not documented (see inference below) |

**Inferences (KIS ordering):**

- **Inference (day route):** K12 L119–126 pages backwards. It treats
  `data[-1].stck_bsop_date` as the earliest date returned and moves
  `FID_INPUT_DATE_2` to the day before it. It then sorts ascending (L147).
  This suggests newest-first `output2` rows.
  - Evidence level: publisher client code, not documentation.
- **Inference (today-only minute route):** K5 L42–43 explains that the
  "첫번째 배열" holds the bar in which trades are currently arriving. That
  points to the in-progress minute being first, i.e. newest-first.

### 2.5 Time and session semantics

- **Day/week/month/year label:**
  - `stck_bsop_date` "주식 영업 일자". Its format is not documented.
  - **Inference:** the field is `YYYYMMDD`, like the request dates.
  - Which day labels a W, M or Y bar (first trading day, last trading day or
    calendar start) is **not documented**.
- **Minute time:**
  - `stck_cntg_hour` "주식 체결시간". Its format is not documented.
  - **Inference:** the field is `HHMMSS`, like `FID_INPUT_HOUR_1` examples
    `093000` and `130000`.
  - Whether it marks the start or the end of the bar is **not documented**.
  - K12 L206 builds `datetime(date + stck_cntg_hour)` as the bar time.
    That is a client choice, not a contract.
- **Time zone:** not documented in any KIS source.
- **Current incomplete bar:**
  - Day route: not documented.
  - Today-only minute route: the in-progress minute **is** returned. K5
    L42–43 says: "output2의 첫번째 배열의 체결량(cntg_vol)은 첫체결이 발생되기
    전까지는 이전 분봉의 체결량이 해당 위치에 표시됩니다. 해당 분봉의 첫 체결이
    발생되면 해당 이전분 체결량이 두번째 배열로 이동되면서 새로운 체결량으로
    업데이트됩니다."
  - So before the first trade of a new minute, the first row carries the
    **previous** minute's volume.
- **Future cursor on the today-only route** (K5 L39–40): "FID_INPUT_HOUR_1 에
  미래일시 입력 시에 현재가로 조회됩니다. ex) 오전 10시에 113000 입력 시에 오전
  10시~11시30분 사이의 데이터가 오전 10시 값으로 조회됨".
- **Minute history depth:**
  - Today-only route: "당일 분봉 데이터만 제공됩니다. (전일자 분봉 미제공)"
    (K5 L37).
  - By-date route: "과거 분봉 조회 시, 당사 서버에서 보관하고 있는 만큼의 데이터만
    확인이 가능합니다. (최대 1년 분봉 보관)" (K7 L39).
- **Minute size:** not documented. Neither minute route has a size field.
- **Pre-market / after-hours / NXT minute bars:**
  - Venue codes J/NX/UN are accepted on both minute routes.
  - Which sessions each venue includes is **not documented**.
- **Holidays / suspended days:** not documented.

### 2.6 Limits

- 100 rows per call on the D/W/M/Y route (K1 L36), which says this holds for
  "실전계좌/모의계좌".
- 30 rows per call on the today-only minute route (K5 L35).
- 120 rows per call on the by-date minute route, stated for 실전계좌 only
  (K7 L36).
- `inquire-daily-price` is limited to the most recent 30 periods (K3 L32).
- Maximum D/W/M/Y lookback: not documented.
- Rate limits: not documented in K1–K11.
  - K12 L12–14 hard-codes `EGW00201` as a rate-limit error code and retries
    after 61 s.
  - That is publisher client code. It is **not** a documented quota, and
    KTradeLink does not adopt its retry policy.

### 2.7 Selector behaviour across intervals

- **Adjustment:**
  - Applies only to the D/W/M/Y and recent-30 routes. Neither minute route
    has an adjustment parameter.
  - K1 does not say whether the flag behaves the same for W/M/Y as for D.
- **Venue:** `J`/`NX`/`UN` is documented on every KIS candle route.
- **Session:** there is no session selector on any KIS candle route.

### 2.8 Contradictions and inferences

1. **Opposite adjustment wording on one parameter name.**
   - K1 (`inquire-daily-itemchartprice`) says `0:수정주가 1:원주가`, i.e.
     0 = adjusted, 1 = original.
   - K3 (`inquire-daily-price`) says `0:수정주가미반영, 1:수정주가반영`, i.e.
     0 = not adjusted, 1 = adjusted.
   - Both sources are at the same commit, and the K10 registry repeats both
     verbatim. At most one mapping can describe a shared server convention,
     and the sources cannot tell which.
   - A decoder must **not** map `adjustment="raw"` to a single global
     `FID_ORG_ADJ_PRC` value.
   - The sample calls are inconsistent too:
     - K1 L51 and K2 L98 send `"1"`, which per K1 is 원주가.
     - K12 L90 sends `"0"` with the comment "수정주가".
2. **Date range vs row cap.**
   - The K1 example asks for `20220101`–`20220809` (K1 L51).
   - **Inference:** that span has more than 100 KRX sessions, so the 100-row
     cap applies.
   - Which 100 rows are returned (newest or oldest end) is not documented.
3. **Paper availability of the by-date minute route.**
   - K7 mentions only 실전계좌 and has no `env_dv`, unlike K1, K3 and K5.
   - Paper support is therefore unknown.
4. **No field table or response example** exists in the pinned sources. JSON
   types, string vs number, signs and units are all unknown.

## 3. Kiwoom REST

### 3.1 Pinned sources

All sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@953e5dbf`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/953e5dbff123f437ab4d11a78a95191a685eb51f).
The full SHA is `953e5dbff123f437ab4d11a78a95191a685eb51f` and the commit is
dated 2026-09-15T15:12:16+09:00. In the links, `…/차트/` stands for
`examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/`
(`examples/국내주식/차트/`).

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | [`examples/국내주식/차트/get_domestic_stock_minute_chart.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_stock_minute_chart.py) | `e7cbf89464138162330e5e770991d5e4680fb122` | `ka10080` example |
| W2 | [`examples/국내주식/차트/get_domestic_stock_daily_chart.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_stock_daily_chart.py) | `c6ec6b33393b1f45e98e7cfbb2db5699e4239b53` | `ka10081` example. This is the same blob ADR 0003 inspected. |
| W3 | [`examples/국내주식/차트/get_domestic_stock_weekly_chart.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_stock_weekly_chart.py) | `4cab1386e5368d20ed5bbe2a7978cdb83f88dd6c` | `ka10082` example |
| W4 | [`examples/국내주식/차트/get_domestic_stock_monthly_chart.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_stock_monthly_chart.py) | `b6abf0e3c3ed65c297ff617b109b20f3b2f8deb0` | `ka10083` example |
| W5 | [`examples/국내주식/차트/get_domestic_stock_yearly_chart.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_stock_yearly_chart.py) | `1561e0540a0b37c63c45aacf35ae73101fd8770d` | `ka10094` example |
| W6 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field tables**: entries `apis["주식분봉차트조회요청(ka10080)"]`, `…(ka10081)`, `…(ka10082)`, `…(ka10083)`, `주식년봉차트조회요청(ka10094)`; `error_codes` |
| W7 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | Field tables (`PRD/국내주식/차트`, `MOCK(모의투자)/국내주식/차트`) |
| W8 | [`kiwoom/core/client.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/kiwoom/core/client.py) | `52d915c9e2f38f21885efbc428d3b50593a452c9` | Publisher client code: headers, `return_code`, continuation |

W6 and W7 carry the same field tables and wording for all five routes.
Where W7 differs from W6, §3.8 notes it.

### 3.2 Routes by interval

All five routes:

- `POST /api/dostk/chart`, `Format` `JSON`, `Content-Type`
  `application/json;charset=UTF-8` (W6 meta).
- Origins: "운영 도메인" `https://api.kiwoom.com` and "모의투자 도메인"
  `https://mockapi.kiwoom.com` (W6 meta; W7 variables `PRD` and `MOCK`).
- W7 lists every one of these routes under both `PRD` and `MOCK(모의투자)`.
  That shows the publisher *offers* them in both environments. It does not
  verify entitlement.

| Interval | API ID / name | Separate route or code? | Interval codes (verbatim) | Candle array key | Evidence |
| --- | --- | --- | --- | --- | --- |
| minute | `ka10080` 주식분봉차트조회요청 | separate API ID; size via `tic_scope` | `tic_scope` "1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분" | `stk_min_pole_chart_qry` | field table + example |
| day | `ka10081` 주식일봉차트조회요청 | separate API ID | — | `stk_dt_pole_chart_qry` | field table + example |
| week | `ka10082` 주식주봉차트조회요청 | separate API ID | — | `stk_stk_pole_chart_qry` | field table + example |
| month | `ka10083` 주식월봉차트조회요청 | separate API ID | — | `stk_mth_pole_chart_qry` | field table + example |
| year | `ka10094` 주식년봉차트조회요청 | separate API ID | — | `stk_yr_pole_chart_qry` | field table + example |

Required request headers (W6):

- `api-id` (Y): "7자리 TR코드".
- `authorization` (Y): "토큰 지정시 토큰타입("Bearer") 붙혀서 호출".

Optional request headers: `cont-yn` and `next-key`. W8 L44–48 also sends
`Content-Type`.

### 3.3 Request fields (W6; identical in W7)

| Concern | `ka10080` minute | `ka10081` day | `ka10082` / `ka10083` / `ka10094` |
| --- | --- | --- | --- |
| Symbol + venue | `stk_cd` String(20) Y: "거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)" | same | same |
| Date | `base_dt` String(8) **N**: "YYYYMMDD" | `base_dt` String(8) **Y** "YYYYMMDD" | `base_dt` String(8) Y "YYYYMMDD" |
| Interval | `tic_scope` String(2) Y (codes in §3.2) | — | — |
| Adjustment | `upd_stkpc_tp` String(1) Y: "0 or 1" | `upd_stkpc_tp` String(1) Y: "0 or 1 / 수정주가 적용을 원하시는 경우, 권리발생일 이후 일자를 base_dt에 넣어 조회 또는 연속조회해주시기 바랍니다. … 수정주가적용(1)로 조회하면 … 수정주가 적용된 … 가격이 나옵니다. … 권리 발생일 이전인 … 일자로 base_dt 조회 시 수정주가 적용되지 않아 …" (full text in W2 L100) | `upd_stkpc_tp` String(1) Y: "0 or 1" |
| Page size | none | none | none |
| Continuation | request headers `cont-yn` (len 1) and `next-key` (len 50): "응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 [next-key값] 세팅" | same | same |
| Range end / start | there is no start-date field; `base_dt` is the only date input | same | same |

- The body is JSON (W8 L52–58 sends `json=body`).
- The examples resend the **same body** on continuation and pass only the
  headers (W2 L143–178).

### 3.4 Response (W6 field tables; examples in W6 `response_example`)

| Concern | `ka10080` minute | `ka10081` day | `ka10082` week / `ka10083` month | `ka10094` year |
| --- | --- | --- | --- | --- |
| Envelope | `return_code` (example `0`, JSON number), `return_msg`. The field table does not list them; only the examples show them. W8 L104: "키움은 업무 오류도 HTTP 200으로 내려보내고 실패 여부는 본문 return_code에만 담는다." | same | same | same |
| Continuation (response headers) | `cont-yn`: "다음 데이터가 있을시 Y값 전달"; `next-key`: "다음 데이터가 있을시 다음 키값 전달" | same | same | same |
| Time | `cntr_tm` "체결시간" "YYYYMMDDHHmmss" | `dt` "일자" "YYYYMMDD" | `dt` "YYYYMMDD" | `dt` "YYYYMMDD" |
| OHLC | `open_pric`, `high_pric`, `low_pric`, `cur_prc` "현재가(종가)" — each "단위: 원, 부호가 포함된 숫자" | `open_pric`, `high_pric`, `low_pric`, `cur_prc` "현재가" — "단위: 원" | same as day | same as day |
| Volume | `trde_qty` "단위: 1주" | `trde_qty` "단위: 1주" | same | same |
| Value | not in field table | `trde_prica` "거래대금" "단위: **백만원**" | `trde_prica` "단위: **원**" | `trde_prica` "단위: **원**" |
| Direction | `pred_pre` "현재가 - 전일종가"; `pred_pre_sig` "1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락" | same + `trde_tern_rt` | same + `trde_tern_rt` | none |
| JSON types | all `String` (W6). The example values are JSON strings. | same | same | same |
| Price sign | field table says signed; example `"cur_prc": "-78800"` with `"pred_pre_sig": "5"` | field table silent; example prices unsigned (`"70100"`) | silent; example unsigned | silent; example unsigned |
| Ordering | example rows `cntr_tm` `20250917132000` then `20250917131900` | example `dt` `20250908` then `20250905` | week `20250901` then `20250825`; month `20250901` then `20250804` | `20250102` then `20240102` |

- **Ordering:** every example lists the newest row first. The field tables
  do not state an order. **Inference:** rows are newest-first.
- **Minute price sign:**
  - The field table states only that the number carries a sign. What the
    sign means is **not documented**.
  - **Inference:** in the example, absolute values satisfy low ≤ open/close
    ≤ high, and `pred_pre_sig` is `5` (하락). So the sign appears to be a
    direction marker relative to the previous close, not a negative price.
  - Gate G-U2 applies.

### 3.5 Time and session semantics

- **Minute time:**
  - `cntr_tm` "체결시간", `YYYYMMDDHHmmss`. It carries a date, unlike KIS.
  - Bar start vs end: **not documented**. Time zone: **not documented**.
- **Day/week/month/year label:** `dt` "일자" `YYYYMMDD`. Which day labels a
  week, month or year bar is **not documented**. The example labels are:
  - week: `20250901` and `20250825`, both Mondays;
  - month: `20250901` (Monday) and `20250804` (Monday).
    - 2025-08-01 was a Friday, so `20250804` is neither the calendar start
      of August nor its first weekday.
    - Whether 2025-08-01 was a KRX session is not established here.
  - year: `20250102` (Thursday) and `20240102` (Tuesday).
  - These labels must **not** be generalised into a rule.
- **Base date:** `base_dt` is the newest anchor of the request. Every route
  except minute requires it.
  - **Inference:** each later page continues further into the past, via
    `next-key`.
- **Current incomplete bar:** not documented for any interval.
- **Minute sessions:**
  - The venue is selected by symbol suffix (KRX, `_NX` NXT, `_AL` SOR).
  - Whether KRX minute data includes pre-market or after-hours
    single-price sessions is **not documented**.
- **Minute history depth:** not documented.
- **Holidays / suspended days:** not documented.

### 3.6 Limits

- Rows per page: not documented.
- Maximum lookback: not documented.
- Error codes (W6 `error_codes`) include the following, with documented
  messages:
  - `1700` "허용된 API 요청 개수를 초과하였습니다";
  - `1701` (총유량);
  - `1702` (그룹 요청);
  - `1687` "재귀 호출이 발생하여 API 호출을 제한합니다";
  - `1901`–`1903` (market code / symbol not found).
  - Numeric quotas are not in W1–W8.
  - The portal quota already recorded in
    [kiwoom-market-data.md](kiwoom-market-data.md) is outside this pin set.
- Example clients cap at `MAX_PAGES = 10` with a `REQUEST_DELAY_SECONDS = 0.2`
  delay (W2 L20–21; same in W1, W3–W5).
  - The W8 `iterate_pages` default is `max_pages=1`, `page_delay_seconds=0.2`.
  - These are **client policies**, not provider limits.

### 3.7 Selector behaviour across intervals

- **Venue:** the symbol-suffix scheme is documented identically on all five
  routes.
- **Adjustment:**
  - `upd_stkpc_tp` is required on all five routes.
  - Only `ka10081` documents that `1` = 수정주가 적용 and that the
    adjustment depends on `base_dt` being after the rights date.
  - The meaning of `0` is never stated. **Inference:** 0 = not applied.
  - For minute, week, month and year, the field reads only "0 or 1".
- **Session:** there is no session selector.

### 3.8 Contradictions and inferences

1. **Value units differ by route.** `trde_prica` is 백만원 on day and 원 on
   week, month and year (W6/W7). The examples agree in scale. A shared
   decoder must not reuse one unit.
2. **Sign documentation differs by route.**
   - Minute prices are documented as signed.
   - Day/week/month/year prices are documented as "단위: 원" only.
   - Elsewhere in the repo, `ka10001` quote prices are known to carry signs
     ([six-broker-ticker-decoders.md](six-broker-ticker-decoders.md)).
   - A daily decoder must therefore not assume unsigned input without a
     fixture.
3. **Field not in the table.** The `ka10080` example contains
   `acc_trde_qty`, which is absent from the field table.
4. **Example JSON is not valid JSON.** Every chart `response_example` has a
   trailing comma before `]`, so it cannot be used as a fixture verbatim.
5. **Example values are mutually inconsistent and partly implausible.**
   - The monthly example (base `20250905`) closes September at `78900`,
     while the weekly example for the same base closes the week of
     `20250901` at `69500`.
   - The 2024 yearly row has `"high_pric": "861000"`, an order of magnitude
     above every other price in that row.
   - The examples are illustrative only.
6. **Postman duplicates body fields into the query string**, e.g.
   `{{PRD}}/api/dostk/chart?stk_cd=005930&tic_scope=1&upd_stkpc_tp=1`.
   - W6 and W8 send JSON bodies only.
   - The query-string copy is **not** adopted as a contract.
7. **W8 tolerates a missing `return_code`.** It treats `None` like success
   (W8 L100, L105), and W2 L152 does the same.
   - KTradeLink's fail-closed policy (see
     [live-auth-transport-gates](live-auth-transport-gates-2026-11-05.md))
     does not copy this.
   - W8 L182 also substitutes `"Y"` when the response's `cont-yn` is empty
     but `has_next` was true. This client choice is not adopted either.

## 4. LS Securities

### 4.1 Pinned sources

All LS sources are public web resources without an immutable revision. Each
sha256 prefix identifies only the copy retrieved at that UTC time on
2026-11-05.

- The detail endpoints return JSON, not HTML. The path is the TR id and
  the `api=` query is the parent sub-menu id. This follows the publisher's
  `apiguide-52fb3f6955943fdee555972c5802f07e.js`.
- The chart sub-menu `[주식] 차트` (`/stock/chart`) has id `12320341-…`.
- t1305 sits under `[주식] 시세` (`/stock/market-data`), id `54a99b02-…`.

| # | Source | Pin (sha256 prefix, UTC retrieval) | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json (the `data-guide-json` attribute of the apiservice page; machine-readable catalog of every TR) | `9aaca437f1925115`, 06:43:57Z; publisher field `"version" : "20261026021444748"` | Chart TR discovery, field tables, TPS, REST server `https://openapi.ls-sec.co.kr:8080`, `contentType` |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `6f7c8d34053adf2c`, 06:43:37Z. An earlier copy at 06:42:47Z hashed `d953b3566410b0a1`; the page varies between requests. | Sub-menu ids (`data-api`) and TR ids (`data-tr`) |
| L3 | https://openapi.ls-sec.co.kr/guide/api/8ncj7d41-48w8-fv13-cj5y-4z8d6m811rbr?type=rest&api=12320341-ad85-429a-90bd-5b3771c5e89f (t8410) | `e45ad8da9fa0fb60`, 06:44:38Z (an identical copy was fetched at 06:42:58Z) | Field table, `required`, request/response example, code sample |
| L4 | `…/guide/api/57t2im3o-021x-1331-dln1-k244483t2m66?type=rest&api=12320341-…` (t8412) | `feefeb24704f16fa`, 06:44:41Z | Same; 500-row minute example |
| L5 | `…/guide/api/afda5e31-3414-4463-8f89-035b59cc170d?type=rest&api=12320341-…` (t8451) | `445482b6bdc1369d`, 06:44:43Z | Same; 10-row daily example |
| L6 | `…/guide/api/0aa3dd33-bada-4df7-bb85-eccc23bea6d9?type=rest&api=12320341-…` (t8452) | `3b4fbf7328ba63c5`, 06:44:45Z | Same; 10-row minute example |
| L7 | `…/guide/api/a7632b74-reqv-gx7q-7ni1-k15qb421az48?type=rest&api=54a99b02-dbba-4057-8756-9ac759c9a2ed` (t1305) | `21de7bd919451179`, 06:44:36Z | Same; 1-row example |
| L8 | https://openapi.ls-sec.co.kr/community-faq (302 → `/community/10000000-0000-0011-0000-000000000002`) | `af701a0003ca34bf`, 06:46:24Z | FAQ text on continuation |

### 4.2 Routes by interval

Every candidate below is in the L1 catalog with `"transactionPerSec" : "1"`.
Each is `POST`, with `domain` `https://openapi.ls-sec.co.kr:8080` and
`contentType` `application/json; charset=UTF-8` (L3–L7).

| Interval | Route / TR id (catalog name, verbatim) | Method + path | Separate route or period code? | Interval code values (verbatim) | Live / paper origin | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| minute | `t8412` "주식차트(N분)" and `t8452` "(통합)주식챠트(N분) API용" | `POST /stock/chart` | Separate TRs from day/week/month. The size is a field: `ncnt` "단위(n분)" (Number 4). | Only "단위(n분)"; no list of allowed sizes. The examples use `1`. | One REST server in L1. A separate paper REST origin is not documented; L1 lists `simulationUrl` only for WEBSOCKET. | field table, publisher example |
| day | `t8410` "API전용주식차트(일주월년)", `t8451` "(통합)주식챠트(일주월년) API용"; also `t1305` "기간별주가" | `POST /stock/chart` (t8410/t8451); `POST /stock/market-data` (t1305) | One TR with a period code | t8410/t8451 `gubun` "주기구분(2:일3:주4:월5:년)"; t1305 `dwmcode` "일주월구분", description "1@일, 2@주, 3@월" | as above | field table, publisher example (daily only) |
| week | same as day | same | period code | `gubun` `3`; t1305 `dwmcode` `2` | as above | field table only; no weekly example |
| month | same as day | same | period code | `gubun` `4`; t1305 `dwmcode` `3` | as above | field table only; no monthly example |
| year | `t8410`, `t8451` only | `POST /stock/chart` | period code | `gubun` `5`; t1305 has no year code | as above | field table only; no yearly example |

Present in the catalog but out of scope:

- tick charts `t8411` and `t8453`;
- `t1302` "주식분별주가조회";
- sector charts on `/indtp/chart`.

**Request headers** are the same for all five TRs (L3–L7
`requestHeaderFields`): `content-type`, `authorization`, `tr_cd`,
`tr_cont`, `tr_cont_key`, `mac_address`.

- The detail JSON marks all six `required: true`.
- The `mac_address` description reads "법인인 경우 필수 세팅", and the
  publisher code samples send it as `""`.

**Response headers:** `content-type`, `tr_cd`, `tr_cont`, `tr_cont_key`.

### 4.3 Request fields

The InBlock is a JSON object named `<tr>InBlock`, for example
`{"t8451InBlock": {...}}` (code samples L3–L7).

| Concern | t8410 (D/W/M/Y) | t8451 (integrated D/W/M/Y) | t8412 (minute) | t8452 (integrated minute) | t1305 (D/W/M) |
| --- | --- | --- | --- | --- | --- |
| Symbol | `shcode` "단축코드" String 6 | `shcode` String 6 | `shcode` String 6 | `shcode` String 6 | `shcode` String 6 |
| Venue selector + codes | **none** in the field table | `exchgubun` "거래소구분코드" String 1, no description in the table; example `"N"` | **none** | `exchgubun`: "K: KRX / N: NXT / U:통합 / 그외 입력값은 KRX로 처리"; example `"K"` | `exchgubun`, same wording as t8452; example `"U"` |
| Date / time range | `sdate` "시작일자" (description "조회구간종료일 / Space:기본값"); `edate` "종료일자", "처음조회기준일(LE) / 처음조회일 경우 이 값 기준으로 조회". String 8; examples use `YYYYMMDD` | `sdate`, `edate` String 8, no descriptions; example `edate` `"99999999"` | `sdate`: "기본값 : Space / (edate(필수입력) 기준으로 qrycnt 만큼 조회) / 조회구간을 설정하여 필터링 하고 싶은 경우 입력"; `edate`: "처음조회기준일(LE) / … / ("99999999" 혹은 '당일')"; `stime`/`etime` "(현재미사용)"; `nday` "조회영업일수(0:미사용1>=사용)" | same fields as t8412 | `date` "날짜": "처음 조회시는 Space / 연속 조회시에 이전 조회한 OutBlock의 date 값으로 설정"; no start/end range |
| Period / minute size | `gubun` | `gubun` | `ncnt` "단위(n분)" Number 4 | `ncnt` Number 4 | `dwmcode` Number 1 |
| Adjustment flag (verbatim) | `sujung` "수정주가여부(Y:적용N:비적용)"; example `"Y"` | `sujung` "수정주가여부(Y:적용N:비적용)"; example `"N"` | **none**: no request field. The response carries `jongchk` "수정구분" and `rate` "수정비율". | **none**, as t8412 | **none** |
| Session selector | not documented | not documented | `krx_mmk_gubun` "KRX정규장구분": "'Y' : 정규장 / 공백을 포함한 이외의 값 : 전체" | same wording | not documented |
| Count field | `qrycnt` "요청건수(최대-압축:2000비압축:500)" Number 4, "OPENAPI에서는 압축 미제공" | `qrycnt` same name, **String** 4 | `qrycnt` Number 4 | `qrycnt` Number 4 | `cnt` "건수" Number 4, "1 이상"; `idx` "사용안함(Space)" |
| Continuation | body `cts_date` "처음 조회시는 Space / 연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정"; header `tr_cont` "연속거래 여부 Y:연속○ N:연속×" and `tr_cont_key` (String 18) "연속일 경우 그전에 내려온 연속키 값 올림" | `cts_date` + same headers | `cts_date` and `cts_time` (String 10) + same headers | same as t8412 | body `date` + same headers |

FAQ (L8, publisher prose): "응답의 연속 키( cts_ 필드)가 비어있지 않으면 다음
데이터가 더 있다는 의미입니다. 해당 키를 다음 요청의 입력에 그대로 넣고, 연속 조회
플래그를 true 로 설정해 반복 호출합니다." The guide does **not document** how the
body `cts_*` keys relate to the `tr_cont_key` header.

### 4.4 Response

| Concern | t8410 / t8451 | t8412 / t8452 | t1305 |
| --- | --- | --- | --- |
| Status / envelope | Root `rsp_cd`, `rsp_msg`; examples `"rsp_cd": "00000"`, `"rsp_msg": "정상적으로 조회가 완료되었습니다."`. Neither field is in the chart TR field tables, so the success code is from the publisher example only. | same | same |
| Candle array path | `t8410OutBlock1` / `t8451OutBlock1`; summary object `…OutBlock` | `t8412OutBlock1` / `t8452OutBlock1`; summary `…OutBlock` | `t1305OutBlock1`; summary `t1305OutBlock` |
| Date / time | `date` "날짜" String 8 | `date` String 8; `time` "시간" String **10** (examples are 6 characters, `HHMMSS`) | `date` String 8 |
| OHLC | `open`, `high`, `low`, `close` | same | same |
| Volume / value | `jdiff_vol` "거래량"; `value` "거래대금" (unit **not documented**); `ratevalue` "수정비율반영거래대금" | `jdiff_vol`, `value` (unit not documented) | `volume` "누적거래량"; `value` "누적거래대금(단위:백만)" |
| Adjustment metadata | `jongchk` "수정구분", `rate` "수정비율" (6.2), `pricechk` "수정주가반영항목" | `jongchk`, `rate` | none |
| JSON types | Table: t8410 Number, **t8451 String** for every OHLCV field. Both examples send JSON integers for OHLCV and `rate` as a JSON string (`"000.00"`, `"0.00"`). | Table: t8412 Number, **t8452 String**. Examples: integers; `rate` string `"0.00"` or `"0"`. | Table Number; example integers, decimal fields as strings |
| Price sign | Example prices are positive. `sign` "종가등락구분(1:상한2:상승3:보합4:하한5:하락주식일만사용)" is a separate field. | `sign` "종가등락구분(1:상한2:상승3:보합4:하한5:하락)" | `sign` "전일대비구분" is separate; `change` "전일대비" is signed in the example |
| Ordering | Not documented. The t8451 example (10 rows) is ascending by `date`, 20260831 → 20260911. | Not documented. Both examples are ascending; t8412 has 500 rows over 20240906 → 20240909. | Not determinable (one-row example) |

### 4.5 Time and session semantics

- **Date / time format:**
  - `date` is 8 characters; examples use `YYYYMMDD`.
  - Minute `time` is declared String 10, but the examples use `HHMMSS` (6
    characters).
- **Bar time = start or end:** not documented.
  - **Inference** from the t8412 example (L4): the first bar of the
    20240909 session is `090100`, with no `090000` bar.
  - The 20240906 bars run `…151900, 152000, 153000`, with no rows for
    152100–152900. t8452 (L6) shows the same `152000 → 153000` jump.
  - This fits **end-of-interval** labels. The reading rests on outside
    knowledge of the KRX 09:00 open and closing call auction; the publisher
    does not state it.
- **Time zone:** not documented.
- **Current incomplete bar:** not documented.
- **Zero-volume minute bars:** not documented.
  - **Example fact:** 348 of the 500 t8412 rows have `jdiff_vol` 0, with
    O=H=L=C.
  - "No trade" and "missing data" therefore cannot be told apart from bar
    presence.
- **Week / month / year label:** not documented. There is no weekly, monthly
  or yearly example.
- **Holidays / suspension:** not documented. The t8412 example has no rows
  for the weekend between 20240906 (Fri) and 20240909 (Mon).
- **Pre-market / after-hours / NXT in minute data:**
  - The default (blank, as in every example) for `krx_mmk_gubun` is
    "전체". What "전체" contains is not documented.
  - The t8451/t8452 summary blocks carry NXT and KRX pre/after-market
    start and end times (`nxt_fm_*`, `nxt_am_*`, `krx_fm_*`, `krx_am_*`).
  - How `exchgubun` `U` combines KRX and NXT bars is not documented.
- **Minute history depth:** not documented.

### 4.6 Limits

- **Rows per call:**
  - `qrycnt` max "비압축:500", and compression is not offered on the open
    API. The documented maximum is therefore 500.
  - The t8412 example requests 500 and returns `rec_count` 500.
  - The t1305 `cnt` maximum is not documented.
- **Rate:** `transactionPerSec` `1` for t8410, t8412, t8451, t8452 and t1305
  (L1, L3–L7).
- **Lookback:** not documented.

### 4.7 Selector behaviour across intervals

- **Adjustment:**
  - `sujung` exists only on the D/W/M/Y TRs.
  - The minute TRs have no adjustment input but return `jongchk`/`rate`.
    Whether minute bars are adjusted is not documented.
  - t1305 has no adjustment input.
- **Venue:**
  - Only t8451, t8452 and t1305 take `exchgubun`. t8410 and t8412 have no
    venue field, and their venue is **not documented**.
  - **Inference** from the "(통합)" name contrast: they may be KRX only.
    This is unverified.
  - On the TRs that have the field, an invalid value silently becomes KRX
    ("그외 입력값은 KRX로 처리").
- **Session:** `krx_mmk_gubun` exists only on the minute TRs.

### 4.8 Contradictions and inferences

1. **t8410 `sdate`:** the label is "시작일자" but the description says
   "조회구간종료일".
2. **Field types:**
   - t8451/t8452 tables type OHLCV as String, but the examples send JSON
     integers.
   - t8410/t8412 type `rate` as Number 6.2, but the examples send strings.
     Two formats occur within one t8412 example: `"0.00"` and `"0"`.
3. **`time` length:** String 10 in the table, 6 characters in the examples.
4. **`required` flags:** every request field and header is marked
   required. That includes `stime`/`etime` "(현재미사용)", `idx`
   "사용안함(Space)" and `mac_address` "법인인 경우 필수 세팅". The code samples
   send empty strings for them.
5. **`sign` vs prices:** in the t8451 example, 20260903 `close` is 150900,
   after 149800 on 20260902, yet `sign` is `"3"` (보합). The basis of `sign`
   is not documented, so do not derive direction from it.
6. **Continuation direction:** the examples' `cts_date`/`cts_time` point to
   just **before** the oldest returned row:
   - t8412: `cts` is 20240906 `111200`; the first row is `111300`.
   - t8452: `cts` is 20260911 `151100`; the first row is `151200`.
   - t8451: `cts_date` is 20260828; the first row is 20260831.
   - **Inference:** pages go backward in time. Whether the `cts` row is
     included in the next page is not documented.
7. **FAQ vs field table:** the FAQ pseudo-code passes `"cts_date"` to t1305.
   The t1305 field table names the key `date`, and its OutBlock has no
   `cts_date`.
8. **t8410 example:** it sends `qrycnt` 200 with blank `sdate`/`edate`, and
   the response has one row and empty `cts_date`. The other examples send
   `edate` `"99999999"`. The effect of a blank `edate` is not documented.
9. **`value` unit:** not documented for t84xx.
   - **Inference:** the examples fit millions of KRW. For t8451 20260831,
     152,922 shares × ~151,000 ≈ 23.1 billion, and `value` is 23163.
   - t1305 states "(단위:백만)" explicitly.

## 5. DB Securities

### 5.1 Pinned sources

GitHub sources are at
[`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb)
(`564b5100b80a3a785468b77ee8c0557f6edcfdeb`, committer date
2026-08-20T10:06:26+09:00). This is the same commit the
[live-auth-transport-gates](live-auth-transport-gates-2026-11-05.md) ledger
pins. Guide JSON pages were retrieved on 2026-11-05 at the UTC times shown.

| # | Source | Pin | Used for |
| --- | --- | --- | --- |
| D1 | [`dbsec_sdk/apis/kr_chart/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_chart/endpoints.py) | blob `0b80a958e7c97e73bf2f4430b1550625fe3ab204`; L29–43 paths/TR codes, L103–157 min, L158–209 day, L210–264 week, L265–318 month | Routes, TR codes, field docstrings, "유량제어: 4 TPS" |
| D2 | [`examples/kr_chart/README.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_chart/README.md#L46-L64) | blob `70257442f0b6788a3c7218e528ab9e69fac1c97b`, L46–64 | `dataCnt` range/default; day/week/month use dates |
| D3 | `examples/kr_chart/kr_chart_chart_{day,min,week,month}.py` | blobs: day `cebb87c73f31924bf7e4896a067e87355cd626e2`, min `895f5cc6b44c9561cf4d6d486e101794500505c5`, week `cacc14427aa162b9de05f9e9ea681802766cf19f`, month `32de308d85d97b5a46c963fda906039f2a018209`; L42–48 | Example request bodies |
| D4 | [`dbsec_sdk/response.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/response.py#L27-L85) | blob `6ce92fdc7fca3e34dda4c25b2797e153de29f7a5`; L27–32, L42–49, L74–85 | `cont_yn`/`cont_key` are **response headers**; success is `rsp_cd == '00000'`, even on HTTP 200 |
| D5 | [`dbsec_sdk/client.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/client.py#L63-L76) | blob `6000fa447765e6fc5822e6c8fe09ef92ead8d462`; L63–76, L229–280 | SDK paging loop; automatic `IGW00201` back-off retry (`_BACKOFF_RETRIES = 4`, L71). This is SDK behaviour and is **not** adopted. |
| D6 | [`examples/dbsec_helper.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/dbsec_helper.py#L437-L521) | blob `a00db7a5a6104f7b4029c0b206231ff389b97f6b`; L437–521 | Same paging protocol in the helper |
| D7 | [`docs/errors_and_rate_limits.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/errors_and_rate_limits.md) | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L48, L74, L96, L104–115, L197–212 | `00000` variants including "모의투자 데이터가 없습니다." (L108); `IGW00201`; `IGW40018`; `2028`; app-level 20 TPS (L210) |
| D8 | [`dbsec_sdk/auth.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/auth.py#L250-L253) | blob `b83addb2b8007ae12946eab1ae0395ceb3eca7de`; L250–253 | SDK base headers: `content-type` and `authorization` only |
| D9 | [`config.yaml.example`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/config.yaml.example#L13-L14) | blob `f6204f1399f2f080c11f28364444b40b7868ef96`; L13–14 | "REST API URL은 운영/모의 동일"; `https://openapi.dbsec.co.kr:8443` |
| DP0 | https://openapi.dbsec.co.kr/apiservice | sha256 `85f2960784174b9d`, 06:47:31Z | Endpoint discovery (the JSON endpoints below are the ones its script calls) |
| DP1 | https://openapi.dbsec.co.kr/api/apis/public/api-list/0bc09824-e8c2-491a-8c9d-b99e64b4b907 (group 국내주식/선물차트) | sha256 `f10207c4b22890cb`, 06:47:24Z | Per-API `accessUrl`, `httpMethod` `POST`, `contentType` `application/json;charset=utf-8`, `domain` `https://openapi.dbsec.co.kr:8443`, `simulatedDomain` null, `ThroughputQuotaRule` `requestLimit` "4"; `lastModifiedDate` 2025-08-27 |
| DP2 | `https://openapi.dbsec.co.kr/api/apis/public/<api_id>` (min `f8581e1f-5621-4be6-a4e7-7cc8088d603f`, day `85fa3c5f-c317-43ab-8590-f57a28f2f8e9`, week `2a108f78-c73f-409f-82fa-d81befc899f8`, month `e34ed58e-6f91-4faa-8112-b9206395f2f0`) | sha256: min `934e7117d8643f31`, day `7536ac65cd74ff68`, week `9b7c52bfb3ed1580`, month `e9280acafdd96cd7`; 06:47:42–45Z | Same metadata per API |
| DP3 | `https://openapi.dbsec.co.kr/api/apis/guide/tr/<api_id>` | sha256: min `c34b20ae4c818bc1`, day `0e04795df4cf5496`, week `7545a04ea0b4a23f`, month `f39dc9948fd403ab`; 06:47:56–58Z | `trCode`, `transactionPerSec` "4", `reqExample`, `resExample` |
| DP4 | `https://openapi.dbsec.co.kr/api/apis/guide/tr/property/<tr_id>` (min `70560350-289e-497c-8710-19eba09f84ee`, day `5d393437-fb83-4602-9f1c-570d0ec0b6ce`, week `b8e9e67d-421c-48b9-abe4-6a99b6072117`, month `057f6634-a3b2-4296-ab30-e4cbcd045882`) | sha256: min `0b5b3ad2fc756aa0`, day `16251b6327e67f6a`, week `d13b6e29487432cc`, month `f599b23f45d88bf6`; 06:48:05–08Z | Header/body field tables |

### 5.2 Routes by interval

| Interval | Route / TR id | Method + path | Separate route or period code? | Interval code values (verbatim) | Live / paper origin | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| minute | 분차트조회 `CHARTMIN` | `POST /api/v1/quote/kr-chart/min` | Own route; size is `InputDivXtick` | "30: 30초 / 60: 1분 / 600: 10분 / 3600: 60분 / [60*N: N분]" (String 9) | One origin `https://openapi.dbsec.co.kr:8443`; DP1 `simulatedDomain` null; D9 "운영/모의 동일 (앱 속성으로 내부 분기)" | field table (DP4), SDK (D1 L129), publisher example |
| day | 일차트조회 `CHARTDAY` | `POST /api/v1/quote/kr-chart/day` | Own route, no period field | — | same | field table, example |
| week | 주차트조회 `CHARTWEEK` | `POST /api/v1/quote/kr-chart/week` | Own route **plus** `InputPeriodDivCode` | `InputPeriodDivCode` "입력주", description `"W"` (String 32) | same | field table, example |
| month | 월차트조회 `CHARTMONTH` | `POST /api/v1/quote/kr-chart/month` | Own route plus `InputPeriodDivCode` | "입력일 - 월/년": "M:월 / Y:년" (String 1) | same | field table, SDK, example (`M` only) |
| year | `CHARTMONTH` with `InputPeriodDivCode` `Y` | `POST /api/v1/quote/kr-chart/month` | Period code on the month route | `Y` "년" | same | field table + SDK only; no yearly example |

Tick (`CHARTTICK`) is out of scope.

**Request headers** (DP4 `req_h`), all marked `requireYn` `Y`:

- `content-type`, `authorization`;
- `cont_yn` "연속거래 여부(Y:연속거래 사용 N:연속거래 사용안함)";
- `cont_key` (String 70) "연속일 경우 그전에 내려온 연속키 값 올림";
- `mac_address` "제휴사인 경우 필수 세팅, 개인은 세팅 X".

There is no `tr_cd` header; the route selects the TR.

**Response headers:** `content-type`, `cont_yn`, `cont_key` (String **18**).

### 5.3 Request fields (body `{"In": {...}}`)

| Concern | CHARTMIN | CHARTDAY | CHARTWEEK | CHARTMONTH |
| --- | --- | --- | --- | --- |
| Symbol | `InputIscd1` "입력종목코드1" String 12: "- J(KRX 주식): (ex. 005930) - NJ(NXT 주식): (ex. N-005930) - UJ(통합): (ex. U-005930) ※ NXT/통합시세로 종목 조회 시 반드시 종목 앞에 구분자 (N-, U-)를 붙여서 호출 부탁드리겠습니다." | same | same | same |
| Venue | `InputCondMrktDivCode` String 2: "주식:J / 주식(NXT): NJ / 주식(통합): UJ / … ※ ETF종목의 경우 J 코드를 사용해 조회 부탁드립니다." (also futures/options/index codes) | same | same | same |
| Date / time range | `InputDate1` "조회 시작일을 YYYYMMDD 형식으로 입력 ex. 20241204". **No end date or time field.** | `InputDate1` "YYYYMMDD (조회 시작일)", `InputDate2` "YYYYMMDD (조회 종료일)" | same as day | same as day |
| Period / size | `InputDivXtick` (above) | — | `InputPeriodDivCode` `"W"` | `InputPeriodDivCode` `M` / `Y` |
| Adjustment flag (verbatim) | `InputOrgAdjPrc` "수정주가사용여부": "0:수정주가 미사용 / 1: 수정주가 사용" | same | same | same |
| Count | `dataCnt` "호출건수" String 4: "입력범위: "1" ~ "2000" ""(공백입력) 또는 "0" 입력시 기본개수(400개)조회" | **none**. D2 L64: "일/주/월차트(`day`, `week`, `month`)는 `dataCnt` 대신 `InputDate1`/`InputDate2` 로 조회 구간을 지정합니다." | none | none |
| Continuation | Request headers `cont_yn`/`cont_key` and response headers `cont_yn`/`cont_key` (DP4). D4 L42–43: "DB증권 서버는 응답에 cont_yn(다음 페이지 존재 'Y'/'N')·cont_key(다음 키) 헤더를 내려준다". The SDK loop (D5/D6) starts with `cont_yn` N and an empty key, repeats with `cont_yn` Y and the previous `cont_key` while the response `cont_yn` is `Y`, and stops on an empty or unchanged key. Chart-specific paging is shown only for tick. | same | same | same |

### 5.4 Response

| Concern | All four routes |
| --- | --- |
| Status / envelope | Root `rsp_cd`, `rsp_msg`; examples `"rsp_cd": "00000"`, `"rsp_msg": "정상 처리 되었습니다."`. D4 L82–83: "업무 성공은 rsp_cd == '00000' 으로 확인한다 (서버가 HTTP 200 과 함께 업무오류코드 M100/IGW… 를 내려주는 경우가 있음)". D7 L104–108 lists `00000` with four messages, including "모의투자 데이터가 없습니다." (no data under a success code). |
| Candle array path | `Out` (DP4 type `A0002`; the examples show a JSON array) |
| Date / time | `Date` "일자" String 8 (examples `YYYYMMDD`); `Hour` "시간" String 6 (minute example `HHMMSS`; day/week examples `""`; **absent** in the month example) |
| OHLC | `Oprc` "시가", `Hprc` "고가", `Lprc` "저가", `Prpr` "현재가" (used as close). The day/week/month `Prpr` description reads: "UJ 통합시세 조회시 종가(현재가)는 KRX 거래소 종가가 아닌, NXT 거래소 종가를 사용합니다." |
| Volume / value | min/day/week tables: `CntgVol` "체결거래량"; month table: `AcmlVol` "누적체결거래량". **No turnover/value field.** Units not documented. |
| JSON types | Table type `A0001` for every field. **Inference:** a string, because every example value is a JSON string (`"63700"`). |
| Price sign | Not documented; no sign field. Example values are unsigned digit strings. |
| Ordering | Not documented. All four examples are **newest first**: day 2 rows, week 5, month 4, minute 20. |

### 5.5 Time and session semantics

- **Date / time format:** `YYYYMMDD` is documented for the inputs. The
  output `Date`/`Hour` formats come only from examples (`YYYYMMDD`,
  `HHMMSS`).
- **Bar time = start or end:** not documented.
  - The minute example's 20 one-minute bars run `154000` … `155900`
    (20240205) at one price.
  - **Inference (weak):** this fits start-of-interval labels covering
    15:40–16:00. It rests on outside knowledge of the KRX after-hours
    session.
  - The example does not match its own request (§5.8), so the inference is
    unreliable.
- **Time zone:** not documented.
- **Current incomplete bar:** not documented.
- **Week / month / year label:** not documented.
  - **Inference from examples:** weekly `Date` values are 20240102 (Tue)
    followed by Mondays, and monthly values are 20240102, 20240201,
    20240304 and 20240401. Both look like the **first trading day of the
    period**.
  - There is no yearly example.
- **Range inclusiveness:** not documented.
  - **Inference from the day example:** `InputDate1` 20250714 with
    `InputDate2` 20250715 returns both dates.
  - The weekly example (`InputDate2` 20240201) returns the bar labelled
    20240129, whose week runs past 20240201.
- **Holidays / suspension:** not documented.
- **Pre-market / after-hours / NXT in minute data:**
  - There is no session selector; the venue is chosen by `J`/`NJ`/`UJ`.
  - **Inference:** the 15:40–15:59 example bars suggest after-hours prints
    can appear. Not documented.
- **UJ (integrated) close:** documented as the **NXT** close for day, week
  and month. The note is absent from the minute table.
- **Minute history depth / direction:** not documented.

### 5.6 Limits

- **Rows per call:**
  - Minute: `dataCnt` 1–2000, default 400 (DP4, D1, D2). `IGW40018`
    "datacnt 값이 최대 요청 가능한 건 수를 초과하였습니다." (D7 L96).
  - Day, week and month: page size not documented.
- **Rate:**
  - 4 TPS per chart API (DP3 `transactionPerSec`, DP1 `requestLimit`, D1).
  - App level "20 TPS" (D7 L210), from SDK documentation.
  - Over the limit the response is `IGW00201` "호출 거래건수를 초과하였습니다."
    (D7 L48, L74).
- **Lookback:** not documented.
- **Date-order error:** `2028` "시작일이 종료일보다 큽니다." (D7 L115).

### 5.7 Selector behaviour across intervals

- `InputOrgAdjPrc`, `InputCondMrktDivCode` and `InputIscd1` (with the
  `N-`/`U-` prefix rule) are worded identically on all four routes,
  including minute.
- The UJ "NXT 종가" note appears on day, week and month only.
- No session selector is documented.

### 5.8 Contradictions and inferences

1. **Day volume field:** the CHARTDAY table and D1 say `CntgVol`
   "체결거래량", but the CHARTDAY example returns `AcmlVol`. The month table
   says `AcmlVol`.
2. **Weekly example volume:** every row has `"CntgVol": ""` (empty). An
   empty volume must not become 0.
3. **Month example:** `Hour` is absent, although the table marks it
   `requireYn` `Y`.
4. **Example requests vs required fields:**
   - The week, month and minute `reqExample`s omit `InputOrgAdjPrc`.
   - The week example also omits `InputPeriodDivCode`.
   - The minute example sends `dataCnt` as `""`, which means the default
     of 400.
   - The day example and the SDK examples (D3) send every field.
5. **Minute example vs its request:** the request asks for `InputDate1`
   20241202 with `InputDivXtick` "600" (10-minute). The response shows
   **1-minute** bars on **20240205**.
6. **`cont_key` length:** 70 in the request header table, 18 in the
   response header table.
7. **`mac_address`:** marked `requireYn` `Y`, but the description says
   "개인은 세팅 X". The SDK does not send it (D8).
8. **Success with no data:** D7 lists `00000` "모의투자 데이터가 없습니다.", so an
   empty `Out` under the success code is possible (paper). Live behaviour
   is not documented.

## 6. Toss Securities

### 6.1 Pinned sources

| # | Source | Pin | Used for |
| --- | --- | --- | --- |
| T1 | [Toss OpenAPI JSON](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | sha256 `c5918961335ccd6b…`, retrieved 06:43:32Z; `openapi 3.1.0`, `info.version 1.2.28`. Same hash and version as the copy pinned in [live-auth-transport-gates](live-auth-transport-gates-2026-11-05.md). | `paths./api/v1/candles.get`, `components.schemas.{CandlePageResponse,Candle,ApiResponse,ErrorResponse,Currency}`, `components.responses.RateLimitExceeded`, `tags[Market Data]` |
| T2 | [Toss overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md) | sha256 `bef057d9babe9a38…`, 06:48:59Z | "Rate Limits" table (`MARKET_DATA_CHART` at L251 of the retrieved copy) |
| T3 | [Toss AsyncAPI JSON](https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json) | sha256 `46669a360d4c5c64…`, 06:43–06:44Z; `asyncapi 3.0.0`, `info.version 1.2.3` | Negative check only: no candle channel |
| T4 | [developers.tossinvest.com/llms.txt](https://developers.tossinvest.com/llms.txt) | sha256 `bbff77eaa55df248…`, 06:48:54Z | Says the OpenAPI JSON is "the source of truth for endpoints, schemas, … and rate limits" and links T2 |

### 6.2 Routes by interval

| Interval | Route / operationId | Method + path | Separate route or period code? | Interval code values (verbatim) | Live / paper origin | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| minute | `getCandles` "캔들 차트 조회" | `GET /api/v1/candles` | One route; `interval` query enum | `"1m"` only | `servers[0].url` `https://openapi.tossinvest.com`; no paper origin in T1 | field table |
| day | `getCandles` | `GET /api/v1/candles` | same route | `"1d"` | same | field table |
| week / month / year | none | — | — | Not in the enum. The 400 example `unsupportedCandleInterval` returns "지원하지 않는 캔들 주기입니다." with `data.allowedValues: ["1m","1d"]`. | — | field table + publisher example (negative) |

- The T1 tag text for `Market Data` reads: "캔들 차트(1분봉·일봉)를 제공합니다. 계좌
  정보 없이 액세스 토큰만으로 호출할 수 있습니다."
- **Request:** GET with a query string. Required header:
  `Authorization: Bearer <access token>` (scheme `oauth2ClientCredentials`).
  There is no `X-Tossinvest-Account` parameter on this route.
- **Response:** `application/json`.
- **Out of equity scope:** `GET /api/v1/market-indicators/{symbol}/candles`
  (index/bond). Its timestamp convention differs; see §6.8.

### 6.3 Request fields (`GET /api/v1/candles`, T1)

| Concern | Documented |
| --- | --- |
| Symbol | `symbol` (query, required): "종목 심볼. KRX: 6자리 종목코드 (숫자 또는 영문·숫자 조합; 예: 005930, 0101N0), US: 영문 티커 (예: AAPL)." |
| Venue selector | **none**: the route has no venue, market or exchange parameter |
| Range | Upper bound only. `before` (query, optional, `date-time`): "페이지네이션 상한 (inclusive, ISO 8601). 이 시각과 같거나 이전인 봉만 반환합니다. 미지정 시 가장 최신 봉부터 반환." The `+` of an offset must be sent as `%2B`. There is no lower-bound field. |
| Interval | `interval` (query, required) "봉 단위", enum `["1m","1d"]` |
| Adjustment | `adjusted` (query, optional, boolean, **default `true`**): "수정주가 적용 여부. `true` 면 수정주가 적용, `false` 면 미적용." |
| Count | `count` (query, optional, integer, default 100, minimum 1, maximum 200): "조회 봉 수 (최대 200)" |
| Continuation | Response `nextBefore`: "다음 페이지 조회 시 `before` 쿼리 파라미터에 그대로 전달. 마지막 페이지면 null." |

### 6.4 Response (T1)

| Concern | Documented |
| --- | --- |
| Status / envelope | HTTP 200 carries the `ApiResponse` envelope (`result` required). 4xx/5xx carry `ErrorResponse` `{error:{requestId,code,message,data?}}`; "`result` 와 `error` 는 동시에 나타나지 않습니다." The candle route lists 400, 404, 429 and 500. |
| Candle array path | `result.candles` (required array); `result.nextBefore` (`["string","null"]`, date-time, not in `required`) |
| Date / time | `timestamp` (`string`, `date-time`); see §6.5 |
| OHLC | `openPrice` "시가", `highPrice` "고가", `lowPrice` "저가", `closePrice` "종가" |
| Volume / value | `volume` "거래량"; unit not stated. **No turnover/value field.** |
| Other | `currency` (`Currency` enum `KRW`, `USD`; "클라이언트는 unknown enum 값을 허용하도록 구현해야 합니다.") |
| JSON types | OHLC and volume: `string`, `format: decimal`, `maxLength: 30`. All seven `Candle` fields are `required`. |
| Price sign | Not documented |
| Ordering | **Documented:** "봉은 최신순(`timestamp` 내림차순)으로 정렬됩니다 — 배열의 첫 요소가 가장 최근 봉, 마지막 요소가 가장 오래된 봉입니다." "최대 200개 봉을 반환합니다." |

### 6.5 Time and session semantics

- **Format:** ISO-8601 date-time with offset. All examples use `+09:00`.
- **`1m` bar time = interval END.** `Candle.timestamp`: "봉 기준 시각 - `1m`: 봉
  종료 시각. 해당 봉은 `[timestamp - 1분, timestamp)` 구간의 체결을 집계합니다."
  - The spec's interval-start timestamp is therefore `timestamp − 60 s`,
    by the documented formula.
- **`1d` bar time:** "`1d`: 해당 거래일 (시각은 현지 자정 고정)". The example is
  `2026-03-25T00:00:00+09:00`.
  - **Inference:** for KRX symbols, "현지" means KST.
- **Time zone:** carried in the offset.
- **Current incomplete bar:** not documented.
- **Week / month / year label:** not applicable; those intervals are not
  offered.
- **Holidays / suspended days:** not documented for candles.
- **Pre-market / after-hours / NXT, and which venue the bars aggregate:**
  not documented for REST candles.
  - T2 says "국내는 통합 시세(KRX+NXT)만 노출합니다", but only in its
    WebSocket section. It is **not** applied to REST candles here.
- **Minute history depth / lookback:** not documented.

### 6.6 Limits

- **Rows per call:** `count` 1–200, default 100.
- **Rate:**
  - The route belongs to Rate Limits Group `MARKET_DATA_CHART` (T1). T2
    gives "`MARKET_DATA_CHART` | 초당 최대 20회".
  - T2 also states: "구체적인 한도 수치는 운영 상황에 따라 사전 공지 없이 조정될 수
    있으며, 현재 허용 한도는 응답 헤더로 확인할 수 있습니다."
  - A 429 response carries `X-RateLimit-*` and `Retry-After` (T1).
- **Lookback:** not documented.

### 6.7 Selector behaviour across intervals

- `adjusted` is a route-wide parameter, and T1 does not restrict it to
  `1d`. Its effect on `1m` is **not documented**.
- No interval has a venue or session selector.

### 6.8 Contradictions and inferences

1. **Inclusive `before` plus `nextBefore` equal to the oldest bar.**
   - `before` is inclusive, and the client is told to pass `nextBefore`
     unchanged.
   - In both examples `nextBefore` equals the oldest returned bar's
     `timestamp`.
   - **Inference:** each follow-up page repeats the previous page's oldest
     bar unless the server excludes it. The documentation does not resolve
     this.
2. **Equity vs indicator timestamps.** The equity `1m` timestamp is the bar
   end. `MarketIndicatorCandle.timestamp` is "봉 시작 시각". The two need
   separate decoders.
3. **Last page and empty pages.** `nextBefore: null` marks the last page.
   Whether an empty `candles` array can come with a non-null `nextBefore`
   is not documented.
4. **OpenAPI version.** T4 calls the file a "Canonical server-owned OpenAPI
   3.0 document", but T1 declares `openapi: 3.1.0`. T1 uses 3.1 type arrays
   such as `["string","null"]`, so a 3.0-only parser mis-reads the
   nullability of `nextBefore`.

## 7. Meritz Securities

### 7.1 Pinned sources

Evidence level `publisher repo note` means a statement in Meritz's GitHub
repository that is not code. That repository's README L11 names the portal
as canonical: "API 목록과 파라미터·응답 필드의 정본은 개발자 포털입니다." Repo notes
therefore rank below the portal (M1).

| # | Source | Pin | Used for |
| --- | --- | --- | --- |
| M1 | Portal API spec JSON export [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json) | Two copies: 06:44:34Z sha256 `deb1285fdf5bd8ef…` and 06:46:17Z sha256 `54a9d5b8b78934cb…`. They differ only in the top-level `generatedAt`. With `generatedAt` removed and keys sorted (`json.dumps(sort_keys=True, ensure_ascii=False)`), both hash to `2fff4f3e02d20cd5…`. | Field tables and examples for `ohhts_1002_003r` (daily) and `ohhts_kapi_005r` (minute) |
| M2 | [samplecode-py](https://openapi.imeritz.com/samplecode-py) | 06:44:28Z sha256 `16500f66fdbf5ec1…`; 06:48:27Z sha256 `e4dbdfb42c4aa3db…`. The copies differ only in an embedded script blob and a CSRF token; both are 183,857 bytes. | Daily sample ("02. 주식 현재가, 일봉 조회"), `rsp_cd` readability check, origin `https://openapi.imeritz.com:9443`, "초당 호출 한도는 공지사항에 기재하였습니다." |
| M3 | [howto-use](https://openapi.imeritz.com/howto-use) | 06:44:27Z sha256 `e710269042e7e27f…` | "조회 API 는 GET + 쿼리스트링 …"; all errors are HTTP 500 |
| M4 | [intro](https://openapi.imeritz.com/intro) | 06:44:25Z sha256 `d7948a13362832b7…` | Provenance: the JSON-LD `WebAPI.sameAs` lists `https://github.com/meritz-securities/open-api` |
| M5 | [`meritz-securities/open-api@a93c6409`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89) (`a93c6409db73ea97ad15f7b7186f36c9f32ecd89`, commit 2026-10-28T22:32:03+09:00) | blobs: `openapi.json` `93e900e66b965607d7fd8b8e14c6088d710e6fce`; `meritz/data/corrections.json` `60370924e13233bbd2cccb517bfffee002dad915`; `docs/errors.md` `b4b2eac6541bd2b886071c1caad17fa0c57ba3e6`; `llms.txt` `8351d5343d785b61107179d19197c59a08e1edff`; `README.md` `61aa5f7f2c1059a29a99175a5cdf573996d81479`; `examples/09_index.py` `778252ff923d47b1d7c0372ae0e82cf92ed757c6` | `openapi.json` `x-tps` (L5421, L5596) and index sentinel rows (L9508); [`corrections.json` L4–20](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/data/corrections.json#L4-L20) and L150; `docs/errors.md` L85, L90, L95; `llms.txt` L120; `README.md` L11, L125; `examples/09_index.py` L17 |
| — | Notice board (`/community-notice`), 06:45:57Z sha256 `efde3ce076549db1…` | The list loads by script, and the static HTML contained no notice text. | **not found**: the rate-limit notice that M2 refers to was not retrieved |

For both candle routes, M1 wording is identical to M5 `openapi.json`. M5
adds `x-tr-id` and `x-tps` and omits M1's `required` column.

### 7.2 Routes by interval (domestic equity)

| Interval | Route / TR id | Method + path | Separate route or period code? | Interval code values (verbatim) | Live / paper origin | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| minute (also seconds/hours) | `ohhts_kapi_005r` "주식 시세추이 조회 (분봉)" | `GET /market/v1/candles/minutes` | Own route; size via `hour_cls_code` | `hour_cls_code` "봉 간격을 초 단위로 입력합니다. 15는 15초, 60은 1분, 3600은 1시간입니다. 반드시 넣으십시오." No list of allowed values. | `https://openapi.imeritz.com:9443` (M2/M4). No paper environment: M5 README L125 "앱키에 연결된 계좌는 실계좌입니다. 모의계좌는 없습니다" (publisher repo note) | field table |
| day | `ohhts_1002_003r` "주식 시세추이 조회 (일봉)" | `GET /market/v1/candles/days` | Own route; no period code | — | same | field table + publisher example (M2) |
| week / month / year | **not found for equities** | — | — | — | — | not found (the full M1 catalogue was searched for `주봉`/`월봉`/`연봉`/`period_cls_code`) |

- **Index-only weekly/monthly/yearly route (out of equity scope):**
  `GET /market/v1/index/candles/days` (`ohhts_1514_101r`) takes
  `period_cls_code` "일봉 D · 주봉 W · 월봉 M · 연봉 Y". It is not an equity
  route.
- **Content type:** M1 `contentType` "application/json; charset=utf-8".
- **Parameter placement:** parameters go in the query string (M3). The M1
  table files them under "request body", but its `requestExample` and M5
  use `in: query`.
- **Required headers (M1):**
  - `authorization` (Bearer access token).
  - `mac_address`: "호출 단말의 MAC 주소입니다. 12자리로 넣습니다. 넣지 않으시면
    요청이 거부됩니다."

### 7.3 Request fields

| Concern | `/market/v1/candles/days` | `/market/v1/candles/minutes` |
| --- | --- | --- |
| Symbol | `iscd` (Y, len 12): "6자리(005930) 또는 A 를 붙인 7자리(A005930)로 넣습니다." | `iscd` (Y, len 12): the same wording, plus "형식이 맞지 않는 코드는 오류 없이 정상 응답코드로 처리될 수 있으며, 예를 들어 뒤에 문자가 붙은 "A005930ZZZZZ" 는 봉이 한 건만 내려옵니다." |
| Venue | `mrkt_div_code` (Y, len 2): `"J": KRX`, `"NJ": 대체거래소(NXT)`, `"TJ": KRX + NXT 통합`; "위 세 값만 넣으십시오. NXT 에 상장되지 않은 종목을 "NJ" 로 조회하면 오류 없이 빈 배열이 내려옵니다." | `mrkt_div_code` (Y): the same three codes, with no further note |
| Session / close basis | `exch_use_yn` (N, len 1): "넣지 않으면 "Y" 로 조회합니다. "Y": KRX 정규장 종가 "N": 애프터마켓(~20:00)까지 포함한 그날의 마지막 체결가 정규장 종가는 mrkt_div_code "TJ" 와 "Y" 를 함께 넣을 때만 내려옵니다. "J"·"NJ" 에서는 "Y" 와 "N" 의 결과가 같아서, "J" 에 "Y" 를 넣어도 애프터마켓까지 포함한 값이 내려옵니다. "TJ" 에서 "Y" 와 "N" 은 시가·고가·저가·종가·전일대비가 달라지고 거래량·거래대금은 같습니다." | not documented |
| Date range | `from` (N, len 8): "YYYYMMDD 8자리이며 to 와 함께 넣으면 그 기간의 일봉이 내려오고, 기간은 최대 1년입니다. 기간 조회는 from 과 to 를 함께 넣어야 합니다. from 만 넣으면 그 날짜부터 과거 방향으로 40건, 둘 다 없으면 최신 40건이 내려옵니다." `to` (N, len 8): "from 과 함께 넣습니다. to 만 넣으면 무시되고 최신 40건이 내려옵니다." Whether the bounds are inclusive is **not documented**. | **None.** No date or time input. |
| Interval | n/a | `hour_cls_code` (Y, len 6), in seconds |
| Adjustment | `mod_stpr_cls_code` (N, len 3): "수정주가 구분입니다. "0" 또는 "1" 을 넣습니다. 0:수정종각 (기본값) / 1:원종가" (verbatim; "수정종각" appears to be a typo for 수정종가). **Default = adjusted.** | **none** |
| Count | none; 40 rows unless both `from` and `to` are sent | none; "한 번에 40건까지 내려오고" |
| Continuation | **not documented** (no `tr_cont`/`tr_cont_key` in the field table) | Explicitly none: "응답에 연속조회 키(tr_cont_key)는 담기지 않습니다." The response example nevertheless contains `"tr_cont": "0"`. |

### 7.4 Response (M1)

| Concern | `/market/v1/candles/days` | `/market/v1/candles/minutes` |
| --- | --- | --- |
| Status / envelope | Top-level `data`, `rsp_cd`, `rsp_msg`, `rsp_sub_msg`. The portal says: ""0000" 이 정상입니다. 결과가 없을 때도 "0000" 과 빈 배열이 내려옵니다. 오류는 HTTP 500 으로 반환되므로 성공·실패는 이 값으로 판정하십시오." **But see §7.8 #1.** | Same shape and wording |
| Array path | `data`: "일봉 배열입니다. 최신 일자가 먼저 오며, from·to 를 넣지 않으면 최신 40건이 내려옵니다." | `data`: "분봉 배열입니다. 최신 봉이 먼저 오며 한 번에 40건까지 내려오고, … 장 마감 뒤 과거 구간은 시세추이 조회(일봉)(/market/v1/candles/days)을 쓰십시오." |
| Date / time | `date` String len 8 "일자(YYYYMMDD)" | `cntg_hour` String len 6, "그 봉 구간의 시각입니다. HHMMSS 여섯 자리로 내려옵니다." **No date field.** |
| Open / high / low | `oprc`, `hprc`, `lprc` (day first trade, high, low) | `oprc`, `hprc`, `lprc` (first, highest and lowest trade within the bar) |
| Close | `stck_clpr` "요청한 시장 구분과 종가 기준에 따른 종가입니다. 정규장 종가는 mrkt_div_code "TJ" 이고 exch_use_yn 이 "Y"(기본)일 때입니다." | **No close field.** `stck_prpr` "가장 최근 체결된 가격입니다." **Inference:** this is the bar's last trade. Not stated. |
| Volume / value | `acml_vol` (cumulative shares for the day); `acml_tr_pbmn` (cumulative traded value; currency not stated) | `cntg_vol` "해당 구간의 체결 수량"; `acml_vol` (cumulative since the open). No per-bar value field. |
| JSON types | Prices and volumes `Number`, and the examples are JSON integers. `date` and `prdy_vrss_sign` are String. | `cntg_hour` String; prices and volumes `Number` |
| Price sign | `prdy_vrss_sign` "1": 상한 … "5": 하락. `prdy_vrss` is signed in the example (`-1136000` with sign `"5"`). OHLC values are unsigned in the examples. | no sign fields |
| Ordering | newest first (documented) | newest first (documented) |

### 7.5 Time and session semantics

- **Daily:** `date` is `YYYYMMDD`. Time zone **not documented**.
- **Minute:** `cntg_hour` is `HHMMSS`, and the row carries **no trading
  date**.
  - Bar start vs end: **not documented** ("그 봉 구간의 시각").
  - Time zone: **not documented**.
- **Current incomplete bar:**
  - M1 does not document it.
  - The M2 daily sample's comment reads "최근 일자부터 내려오며, 장 마감 후에는
    당일 봉도 포함됩니다" (publisher example).
  - Behaviour before the close is unstated.
- **Week / month / year label:** not applicable for equities.
- **Holidays / suspended days:** not documented.
- **Sessions in daily bars:** documented through `exch_use_yn` (§7.3).
  - Only `TJ` with `Y` yields the KRX regular-session close.
  - `J` returns after-market-inclusive values whatever `exch_use_yn` is.
  - For `TJ`, volume and value are the same under `Y` and `N`.
  - M5 `corrections.json` L150 (publisher repo note) records that the KRX
    16:00–18:00 single-price session became the 16:00–20:00 after-market
    from 2026-09-14.
- **Sessions in minute bars:** not documented.
  - The M1 example (`mrkt_div_code=J`) has bars at `180800` and `174800`.
  - **Inference:** after-market bars appear in `J` minute data.
- **Non-time rows:**
  - These are documented for the index minute route only. M5
    `openapi.json` L9508 says "888888, 999999 처럼 시각이 아닌 값이 내려오는
    행이 있습니다", and `examples/09_index.py` L17 calls them 장마감 and
    시간외 rows.
  - Whether the equity minute route can return such rows is not documented.
- **Minute history depth:** the 40 most recent bars per call, with no
  continuation and no date input. M1: "장 마감 뒤 과거 구간은 시세추이
  조회(일봉)… 을 쓰십시오."

### 7.6 Limits

- **Rows:**
  - Daily: 40 rows unless both `from` and `to` are sent. With both, "그
    기간의 일봉" for at most one year; the row cap for that case is not
    stated.
  - Minute: up to 40.
- **Rate:**
  - M2 says the limit is in the notices, which were not retrieved.
  - M5 `openapi.json` gives `x-tps: "10"` on both candle routes.
  - M5 `docs/errors.md` L95: "`EGW00200` | 초당 호출 한도 초과 | API 당 초당
    10건입니다."
  - M5 `llms.txt` L120 says the same, adding that the error arrives as HTTP
    500.
  - Evidence: publisher repo note, not portal.
- **Date format error:** M5 `docs/errors.md` L85 `6102` "일자 형식 오류"
  (sometimes `IGW50004`).

### 7.7 Selector behaviour across intervals

- **Adjustment:** daily only (`mod_stpr_cls_code`). Whether minute bars are
  adjusted is **not documented**.
- **Venue:** `mrkt_div_code` J/NJ/TJ on both routes. The NJ empty-array note
  appears only on the daily route.
- **Session:** `exch_use_yn` is daily only.

### 7.8 Contradictions and inferences

1. **`rsp_cd` success value.**
   - M1 says `"0000"` means success for both candle routes.
   - M5 `corrections.json` L4–20 says otherwise. Its keys include
     `market_candles_minutes` and `market_candles_days`, and its kind is
     "응답 rsp_cd 손상": "HTTP 200 과 정상 data 를 주면서 rsp_cd 에 널바이트가
     섞여 옵니다. rsp_msg 는 빈 문자열입니다."
   - Its workaround is "data 가 있으면 정상으로 보십시오. 이 API 들은 rsp_cd 로
     성공을 판정할 수 없습니다."
   - The M2 sample's response handler checks whether `rsp_cd` is printable.
   - Evidence: publisher repo note plus publisher client code. Unverified.
2. **Empty results are ambiguous.**
   - `"0000"` with `[]` means no result.
   - NJ for a non-NXT symbol returns `[]` "오류 없이".
   - A malformed `iscd` can return one bar with a success code.
3. **Minute example vs request.** The M1 example asks for `hour_cls_code=15`
   (15 s) but returns rows at `180800` and `174800`, 20 minutes apart.
   **Inference:** intervals without trades are omitted.
4. **Minute `tr_cont`.** The field table has no continuation key, but the
   example contains `"tr_cont": "0"`.
5. **Example values are synthetic and inconsistent.** Daily example row 1
   implies a previous close different from row 2's close. M2's own output
   says "숫자는 임의의 값입니다".
6. **`mac_address`.**
   - M1 lists it as a required request header. M5 `docs/errors.md` L90 adds
     "12자리 대문자 16진수".
   - The M2 sample derives it from host network-interface discovery. That
     is **not** a pattern to copy (AGENTS.md).

## 8. Cross-broker comparison

### 8.1 Interval routes

`F` = field table, `E` = publisher example, `C` = publisher client code,
`—` = not found or not offered.

| Broker | 1m | Other minute sizes (verbatim) | 1d | 1w | 1M | 1y |
| --- | --- | --- | --- | --- | --- | --- |
| KIS | E (size not documented) | — | E | E | E | E |
| Kiwoom REST | F+E | F+E: 1, 3, 5, 10, 15, 30, 45, 60 | F+E | F+E | F+E | F+E |
| LS | F+E (`ncnt` 1 in examples) | F: "단위(n분)", no list | F+E | F | F | F |
| DB | F+C+E | F+C: "30: 30초 / 60: 1분 / 600: 10분 / 3600: 60분 / [60*N: N분]" | F+C+E | F+C+E | F+C+E | F+C |
| Toss | F+E | — (enum `1m`, `1d` only) | F+E | — | — | — |
| Meritz | F+E (seconds; example inconsistent) | F: "15는 15초, 60은 1분, 3600은 1시간", no list | F+E | — | — | — |

### 8.2 KRX daily raw vs adjusted — documented semantics

| Broker | KRX selector | Raw daily (verbatim) | Adjusted daily (verbatim) | Default | Field types | Order |
| --- | --- | --- | --- | --- | --- | --- |
| KIS | `FID_COND_MRKT_DIV_CODE=J` (E) | **Contradictory:** `1:원주가` (K1) vs `0:수정주가미반영` (K3) | **Contradictory:** `0:수정주가` (K1) vs `1:수정주가반영` (K3) | required, no default | not documented | not documented (C implies newest first) |
| Kiwoom REST | unsuffixed `stk_cd` (F) | `0` meaning not stated | `1` 수정주가 적용, valid only for rights events before `base_dt` (F) | required, no default | F: String | not documented (E newest first) |
| LS | t8451 `exchgubun` `K` (F); t8410 has **no venue field** | `sujung` `N` "비적용" (F) | `sujung` `Y` "적용" (F) | required, no default | F vs E conflict (Number/String) | not documented (E ascending) |
| DB | `InputCondMrktDivCode` `J` + plain symbol (F) | `InputOrgAdjPrc` `0` "수정주가 미사용" (F) | `1` "수정주가 사용" (F) | marked required; omitted in some examples | F `A0001`; E strings | not documented (E newest first) |
| Toss | **no venue selector**; venue of REST candles not documented | `adjusted=false` "미적용" (F) | `adjusted=true` "적용" (F) | **`true` (adjusted)** | F: decimal strings | **documented** newest first |
| Meritz | `mrkt_div_code` `J` is after-market-inclusive. A KRX regular close needs `TJ` + `exch_use_yn=Y`, and its volume still includes the after-market (F). | `mod_stpr_cls_code` `1` "원종가" (F) | `0` "수정종각 (기본값)" (F) | **`0` (adjusted)** | F: Number | **documented** newest first |

**Reading 8.2:**

- **Documented raw/adjusted pair:** LS, DB, Toss and Meritz each document an
  unambiguous pair of values. KIS contradicts itself. Kiwoom documents only
  the adjusted value.
- **Documented KRX regular-session daily series:**
  - None of the six documents both a clean venue and a regular-session
    daily series.
  - LS t8451 `K` and DB `J` select KRX but say nothing about session.
  - Toss has no venue selector.
  - Meritz `J` is after-market-inclusive by its own documentation.
- **Defaults:** Toss and Meritz default to **adjusted**. A request plan must
  always send the flag explicitly (G-A1).

## 9. Relation to existing repository documents

None of the files below is edited by this change. The contradictions are
recorded here only.

| Document and claim | This audit |
| --- | --- |
| [kis-market-data.md](kis-market-data.md): "`FID_ORG_ADJ_PRC` … this endpoint's example documents `0` adjusted, `1` original" | **Confirmed** for `inquire-daily-itemchartprice` at the pin. K3 documents the **opposite** for `inquire-daily-price`, which confirms that file's warning not to unify across endpoints. |
| kis-market-data.md: intraday TR "not yet mapped" | Now pinned: `FHKST03010200` (today only), `FHKST03010230` (by date) |
| kis-market-data.md: "up to 100 rows per call" | **Confirmed** (K1 L36), real and paper |
| [kiwoom-market-data.md](kiwoom-market-data.md): `ka10082`/`ka10083` "confirm per-ID paths and outputs" | **Confirmed**: both `POST /api/dostk/chart`. Yearly `ka10094` was also found. |
| kiwoom-market-data.md: `upd_stkpc_tp='1'` adjusted, depends on `base_dt` | **Confirmed** in the W6 field table (day route only) |
| kiwoom-market-data.md: `ka10080` `tic_scope` "e.g. 1, 3, … 60" | **Confirmed** as the complete documented list |
| [six-broker-common-surface.md](six-broker-common-surface.md) L20: LS daily candles = `t8410` | **Incomplete.** t8410 has **no venue field**, and its venue is undocumented. The integrated TR with `exchgubun` K/N/U is `t8451` (§4.3). |
| six-broker-common-surface.md L21: DB guide at `https://openapi.db-fi.com/apiservice` | **Host unchecked.** This audit, the DB SDK (D9) and [live-auth-transport-gates](live-auth-transport-gates-2026-11-05.md) all use `openapi.dbsec.co.kr`. The `db-fi.com` host was not fetched, so which host is canonical is unverified. |
| six-broker-common-surface.md L27–29: "DB method paths and native TR codes are left **unverified** until the corresponding official detail view is captured" | **Now captured** for candles: `POST /api/v1/quote/kr-chart/{min,day,week,month}`, `CHARTMIN`/`CHARTDAY`/`CHARTWEEK`/`CHARTMONTH` (§5.2). Other DB routes are not covered here. |
| six-broker-common-surface.md L22: Toss candles cite `developers.tossinvest.com/llms.txt` | Route consistent. llms.txt (T4) calls the spec "Canonical server-owned OpenAPI **3.0** document", but the file declares `openapi: 3.1.0` (T1). Cite T1 directly. |
| six-broker-common-surface.md L23: Meritz `GET /market/v1/candles/days` from the sample page | Consistent. M1 is the field-table source. |
| [ADR 0003](../decisions/0003-candle-orderbook-value-contract.md): LS "Detailed response keys were not retrieved"; DB "Direct guide returned HTTP 502" | Both are now retrieved (§4, §5). |
| ADR 0003: Kiwoom `cur_prc` "signed values still need verification" | Partly answered. Minute prices are documented as signed. Day/week/month/year prices are not, and their examples are unsigned. The meaning of the sign is still undocumented. |
| [live-auth-transport-gates](live-auth-transport-gates-2026-11-05.md): Meritz "success `rsp_cd` differs by API family" | M1 gives `"0000"` for both candle routes. The Meritz repo note says candle `rsp_cd` can be NUL-corrupted (§7.8). |
| live-auth-transport-gates: Toss OpenAPI `1.2.28`, sha256 `c5918961335ccd6b…` | **Unchanged** at this retrieval |
| [market-data spec §5](../specifications/market-data-v0.1-draft.md): minute `timestamp` = interval start | Toss `1m` is documented as **end**-labelled (convertible). LS examples suggest end labels (inference). KIS, Kiwoom, DB and Meritz do not document it. |
| market-data spec §6: proposed default `adjustment="raw"` | Conflicts with the documented Toss (`true`) and Meritz (`0`) defaults, which are adjusted. The flag must always be sent. |
| market-data spec §6: KIS and Kiwoom "can surface newest-first slices" | Not documented for either: Kiwoom examples only; KIS client code only. Order **is** documented for Toss and Meritz (newest first). LS examples are ascending. |
| [capability-matrix-v0.1.json](../specifications/capability-matrix-v0.1.json): KIS/Kiwoom `fetch_ohlcv` evidence URLs point at `main` | Superseded for candle work by the SHA-pinned blobs above |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any candle decoder or request plan is
written. Broker tags are in brackets.

### 10.1 Adjustment default

- **G-A1:** never inherit a broker default; always send the flag
  explicitly.
  - [Toss] `adjusted` defaults to `true`.
  - [Meritz] `mod_stpr_cls_code` defaults to `0` = adjusted.
  - Raise `UnsupportedCapability` for `adjustment` wherever the mapping is
    not proven.
- **G-A2 Contradictory or partial mappings:**
  - [KIS] `FID_ORG_ADJ_PRC` has opposite meanings on K1 and K3. Resolve it
    with the current portal field table plus raw and adjusted fixtures
    across a known split.
  - [Kiwoom] The meaning of `0` is never stated, and `1` is relative to
    `base_dt`.
- **G-A3 No adjustment input:** [KIS minute, LS t8412/t8452/t1305, Meritz
  minute]. Do not label these bars raw or adjusted. Whether [Toss]
  `adjusted` affects `1m` is undocumented.
- **G-A4 Volume and value under adjustment:** not documented for any
  broker. LS returns `ratevalue` separately.

### 10.2 Ordering, paging and overlap

- **G-P1:** the decoder sorts by native date/time and rejects duplicates.
  - Order is documented only for [Toss] and [Meritz] (newest first).
  - [Kiwoom] and [DB] examples are newest first; [LS] examples are
    ascending; [KIS] is undocumented.
  - Never rely on example order.
- **G-P2 Boundary overlap:**
  - [Toss] `before` is **inclusive**, and `nextBefore` equals the oldest
    returned bar, so pages can repeat one bar.
  - [LS] `cts_*` points just before the oldest row; inclusion is
    undocumented.
  - [Kiwoom] and [DB] use header cursors with undocumented boundaries.
  - Deduplicate by timestamp and detect gaps.
- **G-P3 Completeness:** use a finite page budget and raise
  `IncompleteMarketData` rather than truncate.
  - [KIS] D/W/M/Y has no continuation key; which end of an over-100 window
    returns is undocumented.
  - [Meritz] minute returns the latest 40 rows only. Meritz daily needs
    `from`+`to` windows of at most one year, with bound inclusivity and the
    row cap undocumented.
  - [DB] day/week/month page size is undocumented.
  - The publisher examples' page caps (Kiwoom 10, DB SDK 100) are client
    policies, not limits.
- **G-P4 Empty page is not end-of-history:**
  - [Meritz] `NJ` for a non-NXT symbol returns `[]` with success, and a
    malformed `iscd` can return one row.
  - [DB] `00000` can mean "no data".
  - Stop only at a proved boundary.

### 10.3 Minute bar time: start vs end, date, zone, in-progress bar

- **G-T1 Bar anchor:** the spec wants interval-start timestamps.
  - [Toss] documents the **end** (`[timestamp − 1분, timestamp)`). Convert
    by subtracting 60 s, and never share the decoder with the
    start-labelled market-indicator route.
  - [LS] examples suggest end labels (inference). [DB] examples weakly
    suggest start labels (inference, from an inconsistent example).
  - [KIS], [Kiwoom] and [Meritz] are undocumented.
  - Minute support stays blocked per broker until a fixture across a
    known minute boundary proves the convention. No broker-agnostic rule.
- **G-T2 Trading date and time zone:**
  - [Meritz] minute rows carry **no date** (`cntg_hour` only), so they
    cannot satisfy spec §5 on their own.
  - [KIS] uses `stck_bsop_date` + `stck_cntg_hour`; [Kiwoom] a 14-digit
    `cntr_tm`; [LS] `date` + `time` (declared length 10, 6 in examples);
    [DB] `Date` + `Hour`.
  - Only [Toss] carries an explicit offset. Asia/Seoul is an assumption to
    verify everywhere else.
- **G-T3 In-progress bar:**
  - [KIS] documents that the first `output2` row is the live minute, and
    that it can show the **previous** minute's `cntg_vol` until the first
    trade.
  - [Meritz] daily includes today after the close (sample comment);
    behaviour before the close is unstated.
  - The other brokers do not document it.
  - Mark such bars `complete=False` or drop them. Never infer completeness
    from the client clock.
- **G-T4 Minute size:**
  - [KIS] has no size field, so the native granularity must be proven.
  - [LS] `ncnt`, [DB] `InputDivXtick` and [Meritz] `hour_cls_code` have no
    allowed-value list. [Kiwoom] lists its sizes.
  - [Toss] offers `1m` only.
  - Do not advertise resampled sizes as broker data.
- **G-T5 History depth:**
  - [KIS] today-only route: today; by-date route: "최대 1년".
  - [Meritz] minute: the latest 40 rows.
  - All other brokers: undocumented.
- **G-T6 Future cursor:** [KIS] a future `FID_INPUT_HOUR_1` returns data
  labelled with the current time. Never send a cursor later than a
  verified server clock.

### 10.4 Venue and session

- **G-V1 Venue must be explicit and proven:**
  - [LS] t8410 and t8412 have no venue field. `exchgubun` silently maps
    invalid values to KRX, so send it explicitly via t8451/t8452.
  - [DB] needs `InputCondMrktDivCode` **and** the matching `N-`/`U-`
    symbol prefix.
  - [Toss] has no selector, and its REST candle venue is undocumented.
  - [Kiwoom] `_NX`/`_AL` and [KIS] `NX`/`UN` are not equivalent without
    evidence.
  - Ship KRX only first.
- **G-V2 Integrated closes are not KRX closes:**
  - [DB] UJ day/week/month `Prpr` is documented as the **NXT** close.
  - [Meritz] `TJ` + `Y` gives the KRX regular close, but its volume and
    value are the same as under `N` (after-market-inclusive).
  - Never label these KRX or present them as a merged-venue close without
    the caveat.
- **G-V3 No clean KRX regular-session daily series at [Meritz]:** `J`
  includes the after-market by documentation. Mark
  `venue=KRX, session=regular` as unsupported or conditional for Meritz.
- **G-V4 Minute session coverage:**
  - [LS] defaults to "전체"; send `krx_mmk_gubun=Y` for regular, and still
    verify.
  - The [DB] and [Meritz] examples contain post-15:30 bars.
  - [KIS], [Kiwoom] and [Toss] are undocumented.
  - `session="regular"` must error rather than mislabel.

### 10.5 Week / month / year labels

- **G-W1:** no broker documents the label day of a W/M/Y bar.
  - [Kiwoom] example labels are Mondays, and its monthly `20250804` is
    unexplained.
  - [DB] examples look like the first trading day (inference).
  - [KIS] and [LS] have no example.
  - [Toss] and [Meritz] equities do not offer these intervals. Do not map
    the Meritz **index** route onto equities.
  - No `1w`/`1M`/`1y` until the spec defines the anchor and fixtures prove
    it.

### 10.6 Empty, zero-volume and placeholder rows

- **G-E1:**
  - [LS] fills no-trade minutes with flat zero-volume bars (348 of the 500
    rows in the t8412 example).
  - [DB] weekly example volume is `""`.
  - [Meritz] omits no-trade intervals (inference), and its index route has
    `888888`/`999999` sentinel rows.
  - Never coerce `""` or absence to 0. Keep "no trade", "no data" and
    "missing field" distinct.

### 10.7 Status-code reliability

- **G-S1:** a missing or unreadable status is never success.
  - [KIS] `rt_cd == "0"`.
  - [Kiwoom] body `return_code == 0`, even on HTTP 200. The SDK tolerates
    a missing code; do not copy that.
  - [LS] `rsp_cd` `"00000"` is from examples only.
  - [DB] `rsp_cd` `"00000"` is required (HTTP 200 can carry errors), but
    `00000` can also mean "모의투자 데이터가 없습니다.".
  - [Toss] `result` and `error` are mutually exclusive.
- **G-S2 [Meritz]:**
  - Every error is HTTP 500 with `rsp_cd`.
  - The publisher repo says candle `rsp_cd` can contain **NUL bytes**,
    with an empty `rsp_msg`, on HTTP 200.
  - Choose between the portal rule (`"0000"`) and the repo rule ("data
    present") only after authorized fixtures. Do not classify by HTTP
    status alone.

### 10.8 Rate limits and retries

- **G-R1:** budget pages against the documented limits.
  - [LS] **1 TPS** per chart TR.
  - [DB] **4 TPS** per chart API, plus an SDK-documented app-level 20 TPS.
  - [Toss] **20/s** for `MARKET_DATA_CHART`; adjustable, so read
    `X-RateLimit-*`.
  - [Meritz] **10/s** per API (repo note; the portal notice was not
    retrieved).
  - [Kiwoom] error codes `1700`–`1702` exist, but no numeric quota is in
    the pin set.
  - [KIS] not documented.
- **G-R2 No retry loops:**
  - The [DB] SDK auto-retries `IGW00201` with back-off, and the [KIS]
    backtester retries `EGW00201` after 61 s. **Neither is copied.**
  - On 429, `IGW00201`, `EGW00200` or the Kiwoom `1700`-series, surface
    `RateLimitExceeded`.

### 10.9 Types, units and signs

- **G-U1:** parse decimals strictly from whichever JSON type the field
  actually uses. Never use floats.
  - [LS] tables disagree with examples (String vs Number; `rate` in two
    string formats).
  - [DB] values are strings; [Toss] decimal strings; [Meritz] numbers.
  - [KIS] types are undocumented.
- **G-U2 Signed prices:** decide whether `abs()` is permitted per field.
  - [Kiwoom] minute prices are documented as signed; the meaning is
    inferred, not documented.
  - [LS] `sign` disagrees with consecutive closes in its own example.
- **G-U3 Value units:**
  - [Kiwoom] `trde_prica` is 백만원 on day and 원 on week/month/year.
  - [LS] `value` unit is undocumented for t84xx (t1305: 백만).
  - [DB] and [Toss] have no value field.

### 10.10 Headers, environment and credentials

- **G-H1 `mac_address`:** listed by [LS], [DB] and [Meritz] (Meritz:
  mandatory, 12 uppercase hex). It must come from explicit configuration,
  never from host discovery, and must never be logged.
- **G-H2 Environment:**
  - [DB] live and demo share one origin.
  - [Meritz] has no paper environment (repo note), so even a read-only
    candle call needs explicit live authorization.
  - [KIS] by-date minute paper availability is undocumented.
- **G-H3 Undocumented parameter values:**
  - [KIS] `FID_PW_DATA_INCU_YN`, `FID_ETC_CLS_CODE` and
    `FID_FAKE_TICK_INCU_YN`.
  - [LS] blank `edate` behaviour.
  - Send only documented values.

## 11. Not verified

- Any live or paper response for any route above. No broker API request
  was sent.
- Entitlements, real/paper parity and redistribution rights for all six
  brokers.
- Actual rate limits. The Meritz rate-limit notice was not retrieved.
- KIS JSON types, units, signs, ordering and the envelope beyond `rt_cd`.
  The KIS portal specification was not retrieved.
- Kiwoom row order, page size, the meaning of adjustment `0`, the W/M/Y
  label day, and minute session coverage.
- LS:
  - minute bar start vs end (inference only);
  - venue of t8410/t8412;
  - the contents of `krx_mmk_gubun` "전체";
  - page-boundary inclusion;
  - the `value` unit;
  - weekly/monthly/yearly output (no examples).
- DB:
  - ordering;
  - minute bar convention (the example is inconsistent with its request);
  - range inclusiveness;
  - day/week/month page size;
  - live empty-result behaviour;
  - whether `openapi.db-fi.com` is an alias of `openapi.dbsec.co.kr`.
- Toss:
  - whether pages overlap at `before`;
  - venue and session coverage of REST candles;
  - the effect of `adjusted` on `1m`;
  - the in-progress bar.
- Meritz:
  - the `rsp_cd` NUL-corruption note;
  - minute bar convention and trading date;
  - row cap for one-year windows;
  - bound inclusivity;
  - whether equity minute rows can be sentinels.
- Holiday, suspended-trading and partial-session behaviour on every route.
