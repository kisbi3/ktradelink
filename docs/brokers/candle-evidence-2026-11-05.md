# Six-broker candle (OHLCV) evidence — 2026-11-05

- **Scope:** domestic-equity candle routes for minute, day, week and month
  intervals, plus year where a broker documents it. Brokers: KIS, Kiwoom
  REST, LS, DB, Toss and Meritz. The Shinhan comparison stays separate.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No KTradeLink candle decoder or request plan exists, and
  this file does not authorize one.
- **No broker API request was sent.** No token, credential, account, MAC
  value or order was used.
  - KIS and Kiwoom sources are fixed Git commits. They were fetched on
    2026-11-05 between 06:39 and 06:45 UTC from `raw.githubusercontent.com`
    at the pinned SHA.
  - Raw copies were kept outside the repository.
  - Git blob SHAs below are `sha1("blob <len>\0" + bytes)` of the retrieved
    bytes, i.e. what `git hash-object` prints.
- **Section status:**
  - KIS and Kiwoom REST are complete in this revision.
  - LS, DB, Toss and Meritz are `pending`. Their sections are researched
    separately and will be merged into this file before review.
- **How to read the evidence levels:**
  - `field table`: a publisher field/spec table.
  - `publisher example`: sample request/response or sample code.
  - `publisher client code`: SDK or helper behaviour. It shows how the
    publisher calls the route, **not** a contract.
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- Sample values in publisher examples are illustrative. They are **not**
  authorized response fixtures.

## 1. Broker × interval summary

Cell format: route — evidence level. Adjustment (A) and pagination (P):
`doc` = documented, `partial` = documented with gaps described in the
broker section, `none` = not documented, `n/a` = the route has no such
selector.

| Broker | Minute | Day | Week | Month | Year |
| --- | --- | --- | --- | --- | --- |
| KIS | `FHKST03010200` today-only and `FHKST03010230` by date — publisher example; A n/a; P partial (time cursor, no continuation key documented) | `FHKST03010100` `D` — publisher example; A doc (see §2.7 contradiction); P partial (date window, max 100) | same route `W` — publisher example; A same flag; P partial | same route `M` — publisher example; A same flag; P partial | same route `Y` — publisher example; A same flag; P partial |
| Kiwoom REST | `ka10080` — field table + example; A flag present, meaning not stated; P doc (`cont-yn`/`next-key`) | `ka10081` — field table + example; A doc (base-date dependent); P doc | `ka10082` — field table + example; A flag present, meaning not stated; P doc | `ka10083` — field table + example; A flag present, meaning not stated; P doc | `ka10094` — field table + example; A flag present, meaning not stated; P doc |
| LS | pending | pending | pending | pending | pending |
| DB | pending | pending | pending | pending | pending |
| Toss | pending | pending | pending | pending | pending |
| Meritz | pending | pending | pending | pending | pending |

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
  - Gate G-K3 applies.

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

`pending` — researched separately; to be merged before review.

## 5. DB Securities

`pending` — researched separately; to be merged before review.

## 6. Toss Securities

`pending` — researched separately; to be merged before review.

## 7. Meritz Securities

`pending` — researched separately; to be merged before review.

## 8. Cross-broker comparison

### 8.1 Interval routes

Same content as §1, condensed. `F` = field table, `E` = publisher example,
`C` = publisher client code only, `—` = not found.

| Broker | 1m | Nm sizes | 1d | 1w | 1M | 1y |
| --- | --- | --- | --- | --- | --- | --- |
| KIS | E (size not documented) | — | E | E | E | E |
| Kiwoom REST | F+E | F+E: 1,3,5,10,15,30,45,60 | F+E | F+E | F+E | F+E |
| LS | pending | pending | pending | pending | pending | pending |
| DB | pending | pending | pending | pending | pending | pending |
| Toss | pending | pending | pending | pending | pending | pending |
| Meritz | pending | pending | pending | pending | pending | pending |

### 8.2 KRX daily raw vs adjusted — documented semantics

| Broker | KRX selector | Raw daily documented? | Adjusted daily documented? | Field types documented? | Order documented? |
| --- | --- | --- | --- | --- | --- |
| KIS | `FID_COND_MRKT_DIV_CODE=J` | Contradictory: `1:원주가` (K1) vs `0:수정주가미반영` (K3) | Contradictory: `0:수정주가` (K1) vs `1:수정주가반영` (K3) | no | no (inference only) |
| Kiwoom REST | unsuffixed `stk_cd` (KRX) | `0` meaning not stated | `1` = 수정주가 적용, valid only for rights events before `base_dt` | yes (String) | no (examples newest-first) |
| LS | pending | pending | pending | pending | pending |
| DB | pending | pending | pending | pending | pending |
| Toss | pending | pending | pending | pending | pending |
| Meritz | pending | pending | pending | pending | pending |

At this revision **neither KIS nor Kiwoom documents an unambiguous "raw"
daily mode**. Following the
[market-data spec §6](../specifications/market-data-v0.1-draft.md), the
`adjustment="raw"` default must not be published for either without
authorized fixtures.

## 9. Relation to existing repository documents

| Document and claim | This audit |
| --- | --- |
| [kis-market-data.md](kis-market-data.md): "`FID_ORG_ADJ_PRC` … this endpoint's example documents `0` adjusted, `1` original" | **Confirmed** for `inquire-daily-itemchartprice` at the pin. K3 documents the **opposite** for `inquire-daily-price`, which confirms that file's warning not to unify per endpoint. |
| kis-market-data.md: intraday TR "not yet mapped" | Now pinned: `FHKST03010200` (today only), `FHKST03010230` (by date) |
| kis-market-data.md: "up to 100 rows per call" | **Confirmed** (K1 L36), real and paper |
| [kiwoom-market-data.md](kiwoom-market-data.md): `ka10082`/`ka10083` "confirm per-ID paths and outputs" | **Confirmed**: both `POST /api/dostk/chart`, keys `stk_stk_pole_chart_qry` / `stk_mth_pole_chart_qry`. Yearly `ka10094` was also found. |
| kiwoom-market-data.md: `upd_stkpc_tp='1'` adjusted, depends on `base_dt` | **Confirmed** in the W6 field table (day route only) |
| kiwoom-market-data.md: `ka10080` `tic_scope` "e.g. 1, 3, … 60" | **Confirmed** as the complete documented list |
| [ADR 0003](../decisions/0003-candle-orderbook-value-contract.md): Kiwoom `cur_prc` "signed values still need verification" | Partly answered. Minute prices are documented as signed; day/week/month/year are not, and their examples are unsigned. Sign meaning is still undocumented. |
| [market-data spec §6](../specifications/market-data-v0.1-draft.md): KIS and Kiwoom "can surface newest-first slices" | Kiwoom: every example is newest-first, but no documented order. KIS: no documented order; only publisher client code (K12) implies newest-first. |
| [capability-matrix-v0.1.json](../specifications/capability-matrix-v0.1.json) KIS/Kiwoom `fetch_ohlcv` evidence URLs point at `main` | Superseded for candle work by the SHA-pinned blobs above. The JSON is not edited here. |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any candle decoder or request plan is
written.

**General:**

- **G1 Adjustment mapping per route.**
  - KIS: resolve the K1/K3 contradiction with the current portal field
    table plus raw and adjusted fixtures across a known split.
  - Kiwoom: confirm that `0` means unadjusted, and decide how the
    `base_dt` dependency is exposed.
  - Until then, raise `UnsupportedCapability` for `adjustment` rather than
    defaulting.
- **G2 Ordering and dedup.**
  - Neither broker documents row order.
  - The decoder must sort by the native date/time, reject duplicates and
    gaps it cannot explain, and not trust example order.
- **G3 Pagination completeness.**
  - KIS D/W/M/Y has no documented continuation key; date windows are the
    only lever. Decide how to prove which end of an over-100 window is
    returned.
  - Kiwoom: document the `cont-yn`/`next-key` loop as a finite budget,
    distinct from the example's 10-page cap.
  - Raise `IncompleteMarketData` rather than truncate.
- **G4 Interval labels.**
  - Decide how W/M/Y bars are anchored. Neither broker documents the label
    day, and Kiwoom's example monthly label is unexplained (§3.5).
  - No `1w`/`1M`/`1y` until this is resolved (spec §5).
- **G5 Units and types.**
  - Kiwoom `trde_prica` is 백만원 on day vs 원 on week/month/year.
  - KIS types and units are entirely undocumented in the pin set; retrieve
    the portal field tables.
- **G6 Status envelope.**
  - KIS: `rt_cd == "0"`.
  - Kiwoom: `return_code == 0` in the body, even on HTTP 200.
  - A missing status field must not be treated as success.

**Intraday time semantics:**

- **G-I1 Bar anchor.**
  - KIS `stck_cntg_hour` and Kiwoom `cntr_tm` are both called "체결시간".
  - Start vs end of the bar is undocumented for both.
  - The spec requires interval-start timestamps, so minute support is
    blocked until fixtures across a known minute boundary show the
    convention.
- **G-I2 Time zone and date.**
  - Neither broker states a time zone.
  - KIS minute rows carry `stck_bsop_date` + `stck_cntg_hour`; Kiwoom
    carries a 14-digit `cntr_tm`.
  - Asia/Seoul is an assumption to verify, not a documented fact.
- **G-I3 In-progress bar.**
  - KIS documents that the first `output2` row is the live minute and can
    show the *previous* minute's `cntg_vol` until the first trade.
  - Mark such a bar `complete=False`, or drop it. Never publish its volume
    as final.
  - Kiwoom does not document this.
- **G-I4 Session boundaries.**
  - Pre-market, after-hours, closing auction and NXT inclusion are
    undocumented on every minute route.
  - `session="regular"` cannot be guaranteed. Error, do not mislabel.
- **G-I5 Minute size.**
  - KIS has no size parameter, so the native granularity must be proven.
  - Kiwoom's sizes are documented, but its `45` and `60` buckets need
    session-boundary fixtures.
- **G-I6 History depth.**
  - KIS today-only route: today only.
  - KIS by-date route: "최대 1년".
  - Kiwoom: undocumented.
  - The scheduler must stop at a proved boundary, not at an empty page
    alone.
- **G-I7 KIS future-time cursor.** Per K5 L39–40, a future
  `FID_INPUT_HOUR_1` returns data labelled with the current time. Never
  send a cursor later than the verified server clock.

**Broker-specific:**

- **G-K1** KIS by-date minute route paper availability is undocumented.
- **G-K2** KIS `FID_PW_DATA_INCU_YN`, `FID_ETC_CLS_CODE` and
  `FID_FAKE_TICK_INCU_YN` value meanings are undocumented. Do not send
  values other than the publisher sample's until they are documented.
- **G-K3** Kiwoom signed minute prices: decide whether `abs()` is
  permitted. The current evidence is an inference, not documentation.
- **G-K4** Kiwoom venue suffixes `_NX`/`_AL` are not equivalent to KIS
  `NX`/`UN` without evidence. KRX only first.

## 11. Not verified

- Any live or paper response for any route above.
- Entitlements, real/paper parity and redistribution rights.
- Actual rate limits for these routes.
- KIS JSON types, units, signs, ordering and response envelope beyond
  `rt_cd`. The KIS portal specification was not retrieved.
- Kiwoom row order, page size, the `0` adjustment meaning, the label day of
  W/M/Y bars, and minute session coverage.
- Holiday, suspended-trading and partial-session behaviour on any route.
- Every LS, DB, Toss and Meritz statement (sections pending).
