# Six-broker multi-symbol quote (여러 종목 일괄 시세) evidence — 2026-11-05

- **Scope:** domestic-equity REST routes that return the current price of
  several symbols in one call, as the basis for a future `fetch_tickers`.
  Brokers: KIS, Kiwoom REST, LS, DB, Toss and Meritz. WebSocket
  subscriptions, theme/ranking lists and watchlist-group management routes
  are out of scope. The Shinhan comparison stays separate.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No KTradeLink batch request plan, decoder or public
  `fetch_tickers` method exists, and this file does not authorize one.
- **No broker API request was sent.** No token, credential, account, MAC
  value or order was used. Only public Git repositories, public
  documentation pages and publisher JSON documentation endpoints were
  fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS, Kiwoom, DB and Meritz repositories: shallow clones of the default
    branch at 07:55:48–07:56:03. Each clone's head equals the pinned SHA.
  - LS portal: 07:58:51–07:59:48 (§4.1).
  - DB portal JSON endpoints: 08:00:28–08:00:41 (§5.1).
  - Toss portal documents: 08:01:09–08:01:11 (§6.1).
  - Meritz portal specification: 08:01:51 (§7.1).
- **Unchanged since the earlier 2026-11-05 audits:** the LS `tr-guides.json`,
  the DB group list, the three Toss documents and the normalised Meritz
  specification are byte-identical (Meritz: identical after removing
  `generatedAt`) to the copies pinned by the trade-tick audit
  ([trade-evidence-2026-11-05.md](trade-evidence-2026-11-05.md) §4.1–§7.1),
  retrieved about 50 minutes earlier.
- **Pin formats:**
  - Git blob SHAs are `sha1("blob <len>\0" + bytes)`, i.e. what
    `git ls-tree` prints. Lines are written "(K1 L91)": source K1, line 91.
  - Web pages have no immutable revision. Their sha256 prefix identifies
    only the copy retrieved at the stated time.
  - Raw copies were kept outside the repository. Sample tokens, account
    values, app keys, MAC values and staff contact data in publisher
    material are deliberately not copied.
- **Evidence levels:** `field table` (publisher field/spec table),
  `publisher example` (sample request/response or sample code),
  `publisher client code` (SDK behaviour, **not** a contract),
  `legacy publisher example` (under a repository's `legacy/` directory),
  `publisher guide` (portal prose outside the field tables),
  `publisher repo note` and `not found`.
- Every inference is marked **Inference:**. "Not documented" means the
  pinned sources say nothing about it. Sample values in publisher examples
  are illustrative and are **not** authorized response fixtures.

## 1. Broker × concern summary

Cell format: short verdict — evidence. `F` field table, `E` publisher
example, `L` legacy publisher example, `C` publisher client code, `G`
publisher guide, `—` not found.

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Batch route | `FHKST11300006` GET `/uapi/domestic-stock/v1/quotations/intstock-multprice` "관심종목(멀티종목) 시세조회" — E | `ka10095` POST `/api/dostk/stkinfo` "지정종목 정보요청" — F+E | `t8407` POST `/stock/market-data` "API용주식멀티현재가조회" — F+E | `MULTIPRICE` POST `/api/v1/quote/kr-stock/inquiry/multiprice` "국내주식 멀티현재가조회" — F+E+C | `getPrices` GET `/api/v1/prices` "현재가 조회" (the single-symbol route itself) — F | **not found**; `/market/v1/prices` is "한 종목" only — F |
| Max symbols per call | 30 — E, L | **not documented**; `stk_cd` length 20 (F) | 50 (`nrec` "최대 50개까지") — F | 50, `dataCnt` 1–50 — F | 200 — F | n/a |
| Symbol list format | numbered pairs `FID_COND_MRKT_DIV_CODE_n` + `FID_INPUT_ISCD_n`, n = 1..30 — E | one string, "\| 로 구분" — F | one string, no separator, plus count `nrec` — F | numbered pairs `InputCondMrktDivCoden` + `InputIscdn` plus count `dataCnt` — F | one query string, comma-separated — F | n/a |
| Venue selector | per symbol: "J:KRX, NX:NXT" — E | per symbol: code suffix `_NX` / `_AL` — F | **none** — F | per symbol: `J`/`NJ`/`UJ` + `N-`/`U-` prefix — F | **none** — F | n/a |
| Echoed code per row | `inter_shrn_iscd` "관심 단축 종목코드" — E (names only) | `stk_cd`, `required` N — F | `shcode` String 6 — F | `Iscd`, `required` Y — F | `symbol`, required — F | n/a |
| Row order documented? | no | no | no; example rows follow request order — E | no; example rows follow request order — E | no | n/a |
| Missing / invalid symbol | not documented | not documented per row; generic codes `1902`/`1903` — F | not documented | not documented | not documented per row; route has 404 "종목을 찾을 수 없음" — F | n/a |
| Row time field | **none** (only `hour_cls_code`) — E | `cntr_tm` "HHmmss" + `dt` "YYYYMMDD" — F | **none** — F | **none** — F | `timestamp` ISO date-time, nullable — F | n/a |
| Volume in row | `acml_vol` — E | `trde_qty` — F | `volume` — F | **none** — F | **none** — F | n/a |
| Rate: batch vs single | not documented in current sources; legacy "1초당 20건" — L | not documented | `t8407` TPS 5 vs `t1102` TPS 10 — F | `MULTIPRICE` 2 vs `PRICE` 5 — F, C | same route, group `MARKET_DATA` 15/s — F, G | n/a |
| Paper | legacy READMEs: not offered in 모의 — L | mock domain listed — F | no paper REST origin — F | ⭕ (모의 + 실전) — C | no paper origin — F | n/a |

## 2. KIS (Korea Investment & Securities)

### 2.1 Pinned sources

All sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362)
(`3a9be59a3ed8745720dc3aa9d584bdf3b7830362`, committed
2026-10-28T00:26:05+09:00). `…/` stands for `examples_llm/domestic_stock/`.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | [`…/intstock_multprice/intstock_multprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/intstock_multprice/intstock_multprice.py) | `8da776840d8e3194167f87cc0d3680d84d5f6c5e` | Title (L19), path (L23), params (L25–85), docstring (L88–98, L101), TR id (L176), query (L178–299), call (L301–309) |
| K2 | [`…/intstock_multprice/chk_intstock_multprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/intstock_multprice/chk_intstock_multprice.py) | `d2e5fba4ee8e88910652086dce528aaefe8f54c2` | Response column names (L21–51); sample call with two symbols (L78–83) |
| K3 | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) | `0e722d6f3253033efe3cf2b99845397b2b329655` | Origins (L152, L154), `_url_fetch` GET (L444–476), `rt_cd == "0"` (L584) |
| K4 | [`MCP/Kis Trading MCP/configs/domestic_stock.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/configs/domestic_stock.json) | `e82a0829ef519c64dfecb3e966ed217b4fcd3805` | Registry entry L1015–1027; repeats K1 |
| K5 | [`examples_user/domestic_stock/domestic_stock_functions.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_user/domestic_stock/domestic_stock_functions.py) | `e585487d112409af59a64ad135cfc9440b266e72` | L7229–7384 repeat K1 (path, TR id) |
| K6 | [`legacy/rest/get_interest_stocks_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/rest/get_interest_stocks_price.py) | `6dbfd3497eebb2c5b8c762f7d065964eb9e9ba23` | **Legacy** flow (L1–3), rate comments (L35, L61, L87, L103), multi call (L91–107), parameter loop (L129–135), `output` (L140–141) |
| K7 | [`legacy/postman/실전계좌_POSTMAN_샘플코드_v2.6.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/postman/%EC%8B%A4%EC%A0%84%EA%B3%84%EC%A2%8C_POSTMAN_%EC%83%98%ED%94%8C%EC%BD%94%EB%93%9C_v2.6.json) | `a73d6bfab94ddfbf94af8db8de4c9e50ef040e58` | **Legacy** item L12329–12639: `tr_id` (L12370), URL with 30 pairs (L12381), param notes (L12396, L12401), no saved response (L12639) |
| K8 | [`legacy/postman/README.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/postman/README.md) | `8ae02454877ff6eb0d824e374f3d4d59f5c90d17` | Table header L81 (모의/실전 제공 여부), row L210 |
| K9 | [`legacy/README.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/README.md) | `580876a545d21846645e8747c56c923d759f0594` | Table header L102 (모의투자 제공 여부), row L235 |
| K10 | [`…/inquire_price/inquire_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_price/inquire_price.py) | `bb6ab22df57b1a5d14fab861f6c1d29272872a84` | Single-symbol comparison: venue codes (L26), real/demo TR ids (L59–61) |

**Missing evidence:**

- No KIS field table, JSON types, lengths or sample response body for this
  route in K1–K10. Response statements are limited to column names and their
  Korean labels (K2).
- The KIS developer-portal specification was **not** retrieved.

### 2.2 Routes

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Max symbols per call | Evidence |
| --- | --- | --- | --- | --- | --- |
| "[국내주식] 시세분석 > 관심종목(멀티종목) 시세조회 [국내주식-205]" (K1 L19) | GET `/uapi/domestic-stock/v1/quotations/intstock-multprice` (K1 L23; GET because K1 L301 sets no `postFlag`, K3 L472–476) | `FHKST11300006` (K1 L176); K7 L12370 labels it "[실전투자]" | K1 has **no** `env_dv` and one TR id, unlike K10 L59–61. K8 L210 marks it 실전 ⭕ and 모의 blank; K9 L235 leaves 모의 blank. **Inference:** real only. | 30: "※ 한 번의 호출에 최대 30종목의 시세 확인 가능합니다." (K1 L91); K6 L91 "(30종목까지 조회 가능)" | publisher example, legacy publisher example |

### 2.3 Request

- **List format:** numbered query pairs. `FID_COND_MRKT_DIV_CODE_1` and
  `FID_INPUT_ISCD_1` are required (K1 L26–27, L170–174); pairs 2–30 are
  optional and only sent when given (K1 L183–299). K7 L12381 sends all 30
  pairs.
- **Venue:** per symbol, "조건 시장 분류 코드1 (J:KRX, NX:NXT)" (K1 L101;
  K4 repeats it). There is **no** `UN:통합` on this route, unlike the
  single-symbol route "J:KRX, NX:NXT, UN:통합" (K10 L26).
- **Where the pairs come from:** the docstring describes "① 관심종목
  그룹조회 → ② 관심종목 그룹별 종목조회 → ③ 관심종목(멀티종목) 시세조회"
  and maps "fid_mrkt_cls_code(시장구분) → FID_COND_MRKT_DIV_CODE_1",
  "jong_code(종목코드) 1 → FID_INPUT_ISCD_1" (K1 L89–94). K2 L78–83 and
  K7 call the route directly with literal codes. **Inference:** the
  watchlist steps are a convenience, not a prerequisite.
- Mixing other asset types, duplicate symbols, gaps in numbering and
  invalid symbols: **not documented**.

### 2.4 Response

- **Row array:** `output`, read as a list of rows (K1 L304,
  `pd.DataFrame(res.getBody().output)`; K6 L140). Envelope success is
  `rt_cd == "0"` in the shared helper (K3 L584). Publisher client code only.
- **Echoed code:** `inter_shrn_iscd` "관심 단축 종목코드" and
  `inter_kor_isnm` "관심 한글 종목명" (K2 L25–26). Whether an `NX` request
  echoes a plain six-digit code is not documented.
- **Row order and missing symbols:** not documented; no sample response
  exists (K7 L12639 `"response": []`).
- **Fields vs single symbol** (K2 L21–50; the single-symbol decoder fields
  are in §9):

  | Concept | Batch (K2) | Single `FHKST01010100` |
  | --- | --- | --- |
  | last | `inter2_prpr` "관심2 현재가" | `stck_prpr` |
  | open / high / low | `inter2_oprc` / `inter2_hgpr` / `inter2_lwpr` | `stck_oprc` / `stck_hgpr` / `stck_lwpr` |
  | volume | `acml_vol` "누적 거래량" | `acml_vol` |
  | change, sign, rate | `inter2_prdy_vrss`, `prdy_vrss_sign`, `prdy_ctrt` | — (not decoded) |
  | previous close | `inter2_prdy_clpr` "관심2 전일 종가" | — |
  | time | **none**; only `hour_cls_code` "시간 구분 코드", no code list | none |

  Only `acml_vol` shares a name with a decoded single-symbol field.

### 2.5 Limits

- 30 symbols per call (§2.2). No paging fields; K1 passes `tr_cont` `""`
  (K1 L301).
- Rate limit for this route: **not documented** in current sources. Legacy
  K6 comments "유량제한 예방 (REST: 1초당 20건 제한)" (L35, L61, L87,
  L103) and sleeps 0.05 s; that is a general, legacy statement.

### 2.6 Contradictions and gaps

1. **Legacy parameter numbering starts at 0.** K6 L131–133 builds
   `FID_COND_MRKT_DIV_CODE_{i}` / `FID_INPUT_ISCD_{i}` for
   `i in range(...)`, i.e. `_0` … `_29`. K1, K4 and K7 number 1–30. The
   current numbering is preferred; `_0` is undocumented.
2. **Dead link.** K1 L98 points to `rest/interest_stocks_price.py` on
   `main`; at the pinned commit the sample is
   `legacy/rest/get_interest_stocks_price.py` (K6).
3. **Venue set narrower than the single route** (§2.3): `UN` is absent.
4. **No field table or response example** for the route.

### 2.7 Gates and not-verified items

- Bind each row to its symbol by `inter_shrn_iscd`, never by position; the
  publisher does not document row order.
- A separate KIS batch decoder is required: the price fields are
  `inter2_*`, not `stck_*`.
- Not verified: real/paper availability, row order, echo format for `NX`,
  behaviour for unknown or duplicate codes, gaps in numbering, JSON types and
  signs, the rate limit, and `hour_cls_code` values.

## 3. Kiwoom REST

### 3.1 Pinned sources

All sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@c7a3d254`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/c7a3d25449ed4b4238bef378780c41103c67b9e9)
(`c7a3d25449ed4b4238bef378780c41103c67b9e9`, committed
2026-09-15T15:12:16+09:00). `…/종목정보/` stands for
`examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/`.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field table**: `apis["지정종목 정보요청(ka10095)"]` L26468–27220 (meta L26473–26480, `stk_cd` L26531–26538, `atn_stk_infr` L26577, row `stk_cd` L26587, `cur_prc` L26607, `cntr_tm` L26887, `dt` L26967, examples L27218–27219); `apis["주식기본정보요청(ka10001)"]` L1259 (comparison); `error_codes` L107018 |
| W2 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | PRD item L5926 (URL L5961, body L5981); MOCK item L39463 (URL L39498, body L39518); descriptions repeat W1 |
| W3 | [`…/종목정보/get_domestic_watchlist_stock_info.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_watchlist_stock_info.py) | `f76c4737d7393c914f6316d045a39a7c432cef7c` | Example client: header (L1–9), page cap (L20–21), `stk_cd` doc (L169–172), body (L190–192), paging loop (L206–239) |

**Missing evidence:** no example with more than one code (W1 L27218, W2
L5981 and W3 L264 all send `"005930"`); no stated maximum.

### 3.2 Routes

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Max symbols per call | Evidence |
| --- | --- | --- | --- | --- | --- |
| "지정종목 정보요청" ("국내주식 > 종목정보 > 지정종목 정보요청(ka10095)", W1 meta) | POST `/api/dostk/stkinfo` (same path as `ka10001`) | `ka10095` in header `api-id` | "운영 도메인" `https://api.kiwoom.com`, "모의투자 도메인" `https://mockapi.kiwoom.com` (W1 L26478–26479); W2 has PRD and MOCK items | **not documented** | field table, publisher example |

### 3.3 Request

- **List format:** one body field, `stk_cd` String, length `20`, required:
  "거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) 여러개의
  종목코드 입력시 | 로 구분" (W1 L26531–26538).
- **Venue:** per symbol, by suffix (`_NX`, `_AL`); none = KRX.
- **Inference:** if the length `20` is enforced, at most three six-digit
  KRX codes fit ("aaaaaa|bbbbbb|cccccc" is 20 characters), fewer with
  suffixes. The publisher states no maximum.
- Mixing venues, duplicates and invalid codes: **not documented**.
  W1 `error_codes` has generic "1902" "종목 정보가 없습니다. 입력한
  종목코드 값을 확인바랍니다. 종목코드={?}" and "1903" (with 거래소구분);
  whether one bad code fails the whole call is not documented.

### 3.4 Response

- **Row array:** `atn_stk_infr` "관심종목정보", LIST, `required` N
  (W1 L26577). Envelope `return_code` / `return_msg` (W1 L27219 example:
  `0`).
- **Echoed code:** `stk_cd` String 20, `required` N (W1 L26587). Whether a
  `_NX`/`_AL` request is echoed with its suffix is not documented.
- **Row order and missing symbols:** not documented; the only example has
  one row.
- **Fields vs single symbol (`ka10001`, W1 L1259):** `cur_prc`,
  `open_pric`, `high_pric`, `low_pric`, `trde_qty`, `stk_cd`, `pred_pre`,
  `flu_rt` have the **same names** in both. Differences:
  - direction code: `pred_pre_sig` "전일대비기호" "1: 상한가, 2:상승,
    3:보합, 4:하한가, 5:하락" in `ka10095` vs `pre_sig` in `ka10001`;
  - `ka10095` adds `cntr_tm` "체결시간" "HHmmss" (L26887) and `dt` "일자"
    "YYYYMMDD" (L26967); `ka10001` has neither;
  - `cur_prc` is "단위: 원, 부호가 포함된 숫자" (L26607). The example
    sends `"+156600"` with `pred_pre_sig` `"2"`; `lst_pric` is `"-85200"`.

### 3.5 Limits

- `cont-yn` / `next-key` request and response headers are documented for
  `ka10095` (W1 request/response headers). Whether a batch can span pages
  is not documented. W3 loops up to `MAX_PAGES = 10` with
  `REQUEST_DELAY_SECONDS = 0.2` (L20–21) — client policy only.
- Rate limit: not in W1–W3. Generic codes "1700" (API), "1701" (전체) and
  "1702" (그룹) exist in `error_codes`.

### 3.6 Contradictions and gaps

1. **Multi-code support vs field length.** "여러개의 종목코드 입력시 | 로
   구분" sits on a field of length `20` (§3.3).
2. **Name.** The API is "지정종목 정보요청"; the response list is
   "관심종목정보" (`atn_stk_infr`), and W3 is named
   `get_domestic_watchlist_stock_info`. It is not a watchlist-group route.
3. **Sign field renamed** between `ka10001` (`pre_sig`) and `ka10095`
   (`pred_pre_sig`).
4. W2 PRD/MOCK put `?stk_cd=005930` in the URL of a POST that also sends it
   in the body (L5961, L5981). W1 documents only the body.

### 3.7 Gates and not-verified items

- Bind rows by `stk_cd`, never by position. Because `stk_cd` is
  `required` N, a row without it cannot be bound and must be rejected.
- Signed price strings follow the existing `ka10001` rule (no `abs()`
  until the sign meaning is verified).
- Not verified: the real maximum count, length enforcement, mock
  availability, suffix echo, paging of a batch, per-row errors.

## 4. LS Securities

### 4.1 Pinned sources

Portal `https://openapi.ls-sec.co.kr`, no immutable revision; only L1
carries a publisher version.

| # | Path / URL | Pin (sha256 prefix, UTC retrieval, revision) | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true | `9aaca437f1925115`, 07:58:51Z, 2,792,313 bytes; `"version" : "20261026021444748"` (identical to the trade-tick audit copy) | `apis[12]` "[주식] 시세" (`/stock/market-data`); `t8407` L22914–23117 (TPS L22916, `nrec` L22960–22964, `shcode` L22966–22970, `t8407OutBlock1` L23001); `t1102` TPS L18311; REST server |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `d32121ed58f29357`, 07:59:21Z (page varies) | `data-tr` id of t8407 (L597–598) |
| L3 | `https://openapi.ls-sec.co.kr/guide/api/0xh85bca-blus-l8gm-685p-2tjnzb2k34pp?type=rest&api=54a99b02-dbba-4057-8756-9ac759c9a2ed` (t8407) | `4b24594cd34020e3`, 07:59:48Z | TPS (L11), request fields with examples (L14–27), `responseBlocks` (L310), code samples (L494), 3-row `responseExample` (L500) |

**Missing evidence:** no publisher repository or SDK for LS REST; no example
with an unknown code, a duplicate code or a continuation call.

### 4.2 Routes

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Max symbols per call | Evidence |
| --- | --- | --- | --- | --- | --- |
| "API용주식멀티현재가조회" | POST `/stock/market-data`, origin `https://openapi.ls-sec.co.kr:8080` | `t8407` in header `tr_cd`; `transactionPerSec` `"5"` | one REST origin; L1 lists a `simulationUrl` only for WEBSOCKET, so paper REST is **not documented** | 50: `nrec` "최대 50개까지" | field table, publisher example |

The other "[주식] 시세" TRs whose names contain 현재가/시세 (`t1101`,
`t1102`, `t1104`, `t8450`) each take one code of length 6 (`shcode`, or
`code` for `t1104`) in L1; `t1537` "테마종목별시세조회" (`/stock/sector`)
lists a theme, not caller-chosen symbols.

### 4.3 Request

- **Block:** `{"t8407InBlock": {"nrec": …, "shcode": …}}` (L3 code sample).
- `nrec` "건수" Number 3, "최대 50개까지"; example `3` (L1, L3).
- `shcode` "종목코드" String **300**: "구분자 없이 종목코드를 붙여서 입력
  078020, 000660, 005930 을 전송시 '078020000660005930' 을 입력"
  (L1 L22966–22970). 300 = 50 × 6.
- **Venue:** **no** `exchgubun` field, unlike `t1102` (K/N/U). Which venue
  the prices come from is not documented.
- Headers as for other LS TRs: `content-type`, `authorization`, `tr_cd`,
  `tr_cont`, `tr_cont_key`, `mac_address` ("법인인 경우 필수 세팅"; the
  code samples send `""`).
- A mismatch between `nrec` and the number of codes, duplicates and unknown
  codes: **not documented**.

### 4.4 Response

- **Row array:** `t8407OutBlock1`, "Object Array" (L1 L23001); envelope
  `rsp_cd` `"00000"` / `rsp_msg` in the example (L3 L500), not in the
  field table.
- **Echoed code:** `shcode` "종목코드" String 6.
- **Row order:** not documented. The example returns `078020`, `000660`,
  `005930` — the request order.
- **Fields vs single symbol (`t1102OutBlock`):** `price` "현재가",
  `volume` "누적거래량", `sign` "전일대비구분", `change`, `diff`,
  `open`, `high`, `low` have the **same names** as `t1102`. `t8407` adds
  `jnilclose` "전일종가" and has no time field.
- **Types in the example vs the table:** `diff` (Number 6.2) is sent as
  `"-01.45"`, `chdegree` (Number 9.2) as `"000020.91"`; `change` is
  unsigned (`1600` with `sign` `"5"`), `diff` is signed.

### 4.5 Limits

- `t8407` TPS `5` vs single `t1102` TPS `10` (L1 L22916, L18311).
  **Inference:** up to 250 symbols/s through `t8407` against 10 through
  `t1102`, if the gateway counts one batch as one transaction.
- Paging: `tr_cont` / `tr_cont_key` headers exist; whether a 50-code batch
  ever continues is not documented.

### 4.6 Contradictions and gaps

1. Type drift: `diff` and `chdegree` are Number in L1/L3 but strings in
   the example (§4.4).
2. `rsp_cd` appears only in the example.
3. No venue selector or per-row venue (§4.3).

### 4.7 Gates and not-verified items

- Bind rows by `shcode`, never by position, even though the example
  preserves order.
- Treat the venue as **unknown**; do not label `t8407` prices `KRX`
  without evidence.
- Not verified: venue, `nrec` mismatch handling, unknown codes, duplicate
  codes, continuation, paper.

## 5. DB Securities

### 5.1 Pinned sources

[`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb)
(`564b5100b80a3a785468b77ee8c0557f6edcfdeb`, committed
2026-08-20T10:06:26+09:00) and portal JSON endpoints on
`https://openapi.dbsec.co.kr`. The portal API id is the one the SDK links
(`…/apiservice?group_id=80005fb0-…&api_id=3abd4f11-…`).

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| D1 | [`dbsec_sdk/apis/kr_stock_quote/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_quote/endpoints.py#L143-L216) | blob `5930af396f4a74ff04c7e780fcec87660399bec3`; L32, L50, L143–216 (TPS L170), PRICE TPS L231 | Path, TR code, SDK signature |
| D2 | [`examples/kr_stock_quote/kr_stock_inquire_price_multi.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_quote/kr_stock_inquire_price_multi.py) | blob `c8fdf801aac864822670a7b2215cc351eb639e4f`; L5, L18–39, L49–67 | Out field list; example body |
| D3 | [`dbsec_sdk/client_examples/quickstart.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/client_examples/quickstart.py#L82-L95) | blob `8434f056cc6e8e5f69db03747386d5dbefcb48cd`; L82–95 | Five-symbol SDK call |
| D4 | [`docs/api_support_matrix.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/api_support_matrix.md#L55-L56) | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c`; L3–5, L55–56 | ⭕ (모의 + 실전); TPS 2 vs 5 |
| D5 | [`docs/errors_and_rate_limits.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/errors_and_rate_limits.md#L202-L212) | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L202–212 | App 20 TPS + per-API TPS |
| DP1 | https://openapi.dbsec.co.kr/api/apis/public/api-list/80005fb0-6feb-4b8b-904a-605c59e29b4f | sha256 `f4f56996c26c33b3`, 08:00:28Z (identical to the trade-tick audit copy) | `extraParam` `requestLimit` `"2"` (MULTIPRICE) and `"5"` (PRICE) |
| DP2 | `https://openapi.dbsec.co.kr/api/apis/public/3abd4f11-4a92-48f3-bc3e-726a97a47905` | sha256 `8cf7763a99b9238a`, 08:00:29Z; `lastModifiedDate` 2026-03-13 | `name`, `description`, `accessUrl`, `httpMethod`, `domain`, `simulatedDomain` `null` (contains staff/organisation metadata; not copied) |
| DP3 | `https://openapi.dbsec.co.kr/api/apis/guide/tr/3abd4f11-4a92-48f3-bc3e-726a97a47905` | sha256 `b4e64123ae390dfd`, 08:00:30Z | `trName` "국내 멀티현재가조회", `trCode` `MULTIPRICE`, `transactionPerSec` `"2"`, `reqExample`, `resExample` (5 rows) |
| DP4 | `https://openapi.dbsec.co.kr/api/apis/guide/tr/property/b1a8a157-d4f7-4c61-93b1-0f26d4f5603b` | sha256 `94360bc187c75c90`, 08:00:41Z | Header/body field tables |

**Missing evidence:** no response-field descriptions (DP4 `description` is
empty for every `Out` field); no example with `NJ`/`UJ`, an unknown code or
a count mismatch.

### 5.2 Routes

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Max symbols per call | Evidence |
| --- | --- | --- | --- | --- | --- |
| "국내주식 멀티현재가조회" (DP2 `name`; DP3 `trName` "국내 멀티현재가조회") | POST `/api/v1/quote/kr-stock/inquiry/multiprice`, `https://openapi.dbsec.co.kr:8443` | `MULTIPRICE`; TPS `2` (DP1, DP3, D1 L170, D4 L55) | D4 L55 ⭕ ("모의투자(`mode: "demo"`) + 실전투자 모두 호출 가능", L4); DP2 `simulatedDomain` `null` | 50: "※ 1회 호출에 최대 50종목의 시세를 확인 가능합니다." (DP2) | field table, publisher example, publisher client code |

### 5.3 Request

- **Body:** `{"In": {"dataCnt": …, "InputCondMrktDivCode1": …,
  "InputIscd1": …, …}}` (DP3 `reqExample`).
- `dataCnt` "호출건수", length 2, required, "1~50사이의 값 입력" (DP4).
  DP2: "※ "dataCnt" 필드의 값과 입력 데이터의 개수가 일치하지 않으면
  호출이 불가합니다." and "※ 아래와 같이시장구분필드와 종목코드가 1:1
  쌍을 이뤄야 호출이 정상적으로 이뤄집니다." (verbatim, including the
  missing space).
- **Venue / asset per symbol:** `InputCondMrktDivCoden` lists "주식:J",
  "주식(NXT): NJ", "주식(통합): UJ", "ETN: EN", "ELW: W", "업종&지수: U"
  and futures/options codes; `InputIscdn` length 12: "NXT/통합시세로 종목
  조회 시 반드시 종목 앞에 구분자 (N-, U-)를 붙여서 호출" (DP4).
- **Mixing:** the publisher example mixes asset types in one call: index
  future `F`, stock option `JO`, two stocks `J` and index `U` (DP3
  `reqExample`, D2 L49–67).
- Duplicates and unknown codes: **not documented**.

### 5.4 Response

- **Row array:** `Out` (DP4 type `A0002`; `In` is `A0003`, every other
  field `A0001`), an array in the example; envelope `rsp_cd` `"00000"`,
  `rsp_msg` (DP3 `resExample`). D2 L20 labels it "Out  (배열)".
- **Echoed code:** `Iscd` "종목코드", required Y (DP4). Echo format for
  `N-`/`U-` requests is not documented.
- **Row order:** not documented. The example returns the five rows in
  request order.
- **Fields vs single symbol (`PRICE`):** `Prpr` "현재가", `Oprc`, `Hprc`,
  `Lprc`, `Sdpr` "기준가", `PrdyVrss` "전일대비", `PrdyCtrt`
  "전일대비율" share the single-route names. The batch row has **no
  volume** (`PRICE` has `AcmlVol` per D1), **no sign code** and **no time**.
  `PrdyVrss` is signed in the example (`"-5100"`). Index rows have empty
  `Mxpr`/`Llam`.

### 5.5 Limits

- `MULTIPRICE` 2 TPS vs `PRICE` 5 TPS (DP1 `requestLimit`, D4 L55–56);
  app-wide 20 TPS (D5 L210). **Inference:** up to 100 symbols/s through
  `MULTIPRICE` against 5 through `PRICE`.
- Paging: `cont_yn` (required) / `cont_key` headers exist (DP4); whether a
  batch continues is not documented.

### 5.6 Contradictions and gaps

1. **SDK accepts exactly five symbols.** D1 L143–158 declares
   `InputCondMrktDivCode1`…`InputIscd5` as required keyword arguments and
   no others, while DP2 allows 1–50 and requires `dataCnt` to match.
   Publisher client code, not a contract.
2. **`dataCnt` type.** DP4 gives it type `A0001` length 2, the same type
   as the string fields `Iscd` and `Prpr`, whose example values are JSON
   strings; DP3 sends the JSON integer `5`; D2 L53 comments "(str)" next to
   the integer; D1 types it `int`.
3. **Missing volume** compared with `PRICE` (§5.4).

### 5.7 Gates and not-verified items

- Bind rows by `Iscd`, never by position.
- Send only `J` pairs; reject non-stock market codes, so a batch cannot mix
  futures, options or indices into equity tickers.
- Not verified: count mismatch behaviour, unknown or duplicate codes,
  `N-`/`U-` echo, paper entitlement, continuation.

## 6. Toss Securities

### 6.1 Pinned sources

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | sha256 `c5918961335ccd6b`, 08:01:09Z; `openapi 3.1.0`, `info.version 1.2.28` | `paths./api/v1/prices.get` L336–456 (summary L341–342, `symbols` L351–357, `krStock` example L386–398, 400 `invalidBatchSize` L417–444, 404/429/500 L445–451); `components.responses.NotFound` L8962; `components.schemas.PriceResponse` L9525; `Currency`; `servers` |
| T2 | [overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md) | sha256 `bef057d9babe9a38`, 08:01:10Z | L94 endpoint list; L236–238, L250, L264 rate limits |
| T3 | [faq.md](https://openapi.tossinvest.com/openapi-docs/faq.md) | sha256 `6ad4c02b8e785f7d`, 08:01:11Z | L22 venue (candles and trades only) |

**Missing evidence:** no example with more than one symbol in `result`, an
unknown symbol, or a mix of KR and US symbols.

### 6.2 Routes

| Route (title verbatim) | Method + path | TR / API id | Real / paper | Max symbols per call | Evidence |
| --- | --- | --- | --- | --- | --- |
| "현재가 조회" | GET `/api/v1/prices`, server `https://openapi.tossinvest.com` | `operationId` `getPrices`; group `MARKET_DATA` | one server; no paper origin in T1 | 200: "최대 200건 까지 다건 조회를 지원하며 콤마(`,`)로 구분합니다." (T1 L342) | field table |

This is the same route the private single-symbol planner already uses with
one symbol (§9).

### 6.3 Request

- `symbols` (query, required): "종목 심볼. 최대 200 개를 콤마(`,`)로 구분.
  예: `005930,000660` 또는 `AAPL,MSFT`. 영문 대/소문자, 숫자, '.', '-'
  만 허용한다."; pattern `^[A-Za-z0-9.,\-]+$` (T1 L351–357).
- 400 example `invalidBatchSize`: "symbols 개수가 허용 범위(1~200) 를
  벗어남" with `constraint` `min` 1, `max` 200 (T1 L424–444).
- **Venue:** no selector. T3 L22 says "KRX + NXT 통합 시세입니다" but
  answers a question about "캔들·체결", not prices.
- Mixing KR and US symbols, duplicates, empty items (`a,,b`): **not
  documented**.

### 6.4 Response

- **Row array:** `result`, array of `PriceResponse` (T1 L370–378).
- **Echoed code:** `symbol`, required (T1 L9525–9529).
- **Row order:** not documented.
- **Missing symbols:** the route lists 404 `NotFound`, "종목을 찾을 수
  없음", code `stock-not-found` (T1 L445, L8962). Whether one unknown
  symbol fails the whole batch or is omitted is **not documented**.
- **Fields:** `symbol`, `timestamp` (date-time or `null`, "데이터 시각.
  체결 미발생 등으로 시각이 없을 경우 null"), `lastPrice` (string,
  `decimal`, maxLength 30), `currency` (`KRW`/`USD`, "클라이언트는 unknown
  enum 값을 허용하도록 구현해야 합니다."). No volume, OHLC or change.

### 6.5 Limits

- `MARKET_DATA` "초당 최대 15회" per "클라이언트 × API 그룹" (T2 L236,
  L250); "사전 공지 없이 조정될 수 있으며" (T2 L238, L264). Whether a
  200-symbol call counts as one request is not documented.
- No paging.

### 6.6 Contradictions and gaps

1. Batch failure semantics for a partly unknown list are undocumented
   (§6.4).
2. The FAQ venue statement does not name the prices route (§6.3).

### 6.7 Gates and not-verified items

- Bind rows by `symbol`, never by position; the existing decoder already
  matches exactly and rejects duplicates (§9).
- Require `currency` `KRW` per row for KR symbols; reject unknown enums.
- Not verified: partial-failure behaviour, duplicate handling, row order,
  venue, whether US and KR symbols can be mixed, rate-limit accounting.

## 7. Meritz Securities

### 7.1 Pinned sources

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| M1 | Portal API spec export [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json) ("메리츠증권 Open API 명세") | 08:01:51Z, sha256 `a22d5041775b9ce7`, 1,136,519 bytes, `generatedAt "2026-11-05 17:01:49"`. Without `generatedAt` and with `json.dumps(sort_keys=True, ensure_ascii=False)`: `2fff4f3e02d20cd5`, identical to the trade-tick audit copy | Every group and API (scan below); `groups[2].apis[19]` "현재가 조회" L6974–7013 (description L6977, `ohhts_1001_001r` L6980, `mrkt_div_code` L7000–7005, `iscd` L7008–7013) |
| M2 | Repo [`meritz-securities/open-api@a93c6409`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89) (`a93c6409db73ea97ad15f7b7186f36c9f32ecd89`, 2026-10-28T22:32:03+09:00) `openapi.json` | blob `93e900e66b965607d7fd8b8e14c6088d710e6fce`; L6607–7157 (description L6614, `iscd` L6642–6649, `x-tr-id` L7156, `x-tps` `"10"` L7157) | Same route, repository copy |

The repository README states "API 목록과 파라미터·응답 필드의 정본은
개발자 포털입니다." (README L11, blob
`61aa5f7f2c1059a29a99175a5cdf573996d81479`), so M1 ranks first.

### 7.2 Routes

**Not found.** M1 has six groups; group 2 "국내주식" has 30 REST APIs, and
none of their names or descriptions offers a multi-symbol quote (the quote
routes are 현재가, 시간외 단일가, 호가, 체결추이, 시세추이 and 지수 routes,
plus orders, accounts and reference data). Keyword scans of M1 and of the
repository
(멀티, 복수, 다건, 여러 종목, multi, batch, bulk) match only WebSocket
subscription text ("한 접속에서 여러 종목·여러 서비스를 구독") and
non-quote prose. The current-price route says "국내주식 한 종목의 현재가와
당일 시세를 조회합니다." (M1 L6977, M2 L6614).

### 7.3 Request

Single-symbol route only. Its `iscd` description matters for any attempt to
pass a list: "뒤에 문자가 더 붙은 값(예: A005930ZZZZZ)은 앞 7자리만
읽습니다." and unregistered codes "오류 없이 정상 응답코드 "0000" 으로
내려오되 값이 비거나 0 입니다." (M1 L7013).

### 7.4 Response

n/a (no batch route).

### 7.5 Limits

Single route `x-tps` `"10"` (M2 L7157). A batch of N symbols needs N calls.

### 7.6 Contradictions and gaps

None for the batch topic.

### 7.7 Gates and not-verified items

- Never pass a concatenated or delimited list in `iscd`: per M1 L7013 it
  would be truncated to the first code and could still answer `"0000"`.
- A Meritz `fetch_tickers` can only be N single-symbol requests, each bound
  by its own `shrn_iscd` echo; not verified.

## 8. Cross-broker comparison

| Property | KIS | Kiwoom | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Max per call | 30 | not documented (length 20) | 50 | 50 | 200 | 1 |
| Count field | none | none | `nrec` | `dataCnt` (must match) | none | — |
| Venue control | per symbol J/NX | per symbol suffix | none | per symbol J/NJ/UJ | none | per call J/NJ/TJ (single) |
| Echo field | `inter_shrn_iscd` | `stk_cd` (optional) | `shcode` | `Iscd` | `symbol` | `shrn_iscd` (single) |
| Same last-price name as single route | no (`inter2_prpr`) | yes (`cur_prc`) | yes (`price`) | yes (`Prpr`) | same route | — |
| Volume | `acml_vol` | `trde_qty` | `volume` | none | none | — |
| Row time | none | `cntr_tm` + `dt` | none | none | `timestamp` | — |
| Batch TPS vs single | not documented | not documented | 5 vs 10 | 2 vs 5 | 15/s, same route | 10 (single) |

What a common `fetch_tickers` could rely on — **Inference:** only:

- **Inference:** a per-row echoed code exists everywhere a batch route
  exists, so binding by code is possible for all five; it is optional only
  at Kiwoom.
- **Inference:** a last price is the only field present in every batch row.
  Volume is absent at DB and Toss, OHLC at Toss, and a row timestamp at KIS,
  LS and DB. A common `fetch_tickers` could promise `last` only; other
  `Ticker` fields would be per-broker and often `None`.
- **Inference:** no publisher documents row order, partial results or
  duplicate handling, so a common contract must treat a batch as
  "all requested symbols bound by echo, or fail".
- **Inference:** the cap must be per broker (30/50/50/200) and requests must
  be chunked; Kiwoom has no usable cap, and Meritz has no batch.
- **Inference:** venue cannot be common. LS and Toss have no selector, KIS
  lacks `UN` on the batch route, and DB/Kiwoom encode venue in the code.
  `KRX`-only, as in ADR 0013, can be expressed at KIS (`J`), Kiwoom (no
  suffix) and DB (`J`), but not at LS or Toss.
- **Inference:** the batch routes have lower per-call TPS than their
  single routes at LS and DB, but more symbols per second.

## 9. Relation to existing repository code and documents

- **Request planner** (`src/ktradelink/_request_plan.py`):
  `plan_ticker_request` plans one symbol per broker. KIS uses
  `inquire-price` with `FHKST01010100` (L182–185), Kiwoom `ka10001`
  (L186–193), LS `t1102` with `exchgubun` `K` (L194–212), DB `PRICE` with
  `J` (L213–230), Toss `GET /api/v1/prices` with `symbols` = one code
  (L231–233), Meritz `/market/v1/prices` (L234–236). None of the batch
  routes in §2–§5 is planned. `_checked_symbol` (L87–98) requires one
  six-character code; there is no list type.
- **Decoders** (`crates/ktradelink-decoders/src/lib.rs`, summarised in
  `six-broker-ticker-decoders.md`): KIS reads `output` as an **object**
  with `stck_prpr`/`stck_oprc`/`stck_hgpr`/`stck_lwpr`/`acml_vol`; Kiwoom
  reads root `cur_prc`/`open_pric`/`high_pric`/`low_pric`/`trde_qty` and an
  optional matching `stk_cd`; LS reads `t1102OutBlock` with required
  `shcode`, `price`, `volume`; DB reads `Out` as an **object** with `Prpr`,
  `Oprc`, `Hprc`, `Lprc`; Toss scans `result[]` for exactly one row whose
  `symbol` equals the request and rejects a second match
  (`AmbiguousSymbol`); Meritz reads `data`.
- **Do batch rows share the single-symbol names?**
  - KIS: **no** for prices (`inter2_prpr`, `inter2_oprc`, `inter2_hgpr`,
    `inter2_lwpr`); only `acml_vol` matches. The array is `output` in both,
    but as a list here. A KIS batch needs its own field mapping.
  - Kiwoom: **yes** for `cur_prc`, `open_pric`, `high_pric`, `low_pric`,
    `trde_qty`, `stk_cd`, but rows sit in `atn_stk_infr[]`, not at the
    root, and the sign code is `pred_pre_sig`, not `pre_sig`.
  - LS: **yes** for `shcode`, `price`, `volume` (and `open`/`high`/`low`,
    which the LS decoder does not map); rows sit in `t8407OutBlock1[]`.
  - DB: **yes** for `Prpr`, `Oprc`, `Hprc`, `Lprc`; `Out` becomes an array
    and there is no volume (the single decoder maps none either).
  - Toss: identical route and schema; the decoder already selects one row
    out of many by exact `symbol`.
  - Meritz: no batch route.
- **ADR 0013:** the public `fetch_ticker` sends one quote request per call
  and accepts `venue="KRX"` only; it notes that "KIS responses do not echo
  the symbol". The KIS batch route does echo (`inter_shrn_iscd`), which a
  batch path could use. ADR 0013 also forbids retries; the same would apply
  to every chunk.
- **`six-broker-quote-request-auth.md`** already records that Toss
  "Supports up to 200 comma-separated requested symbols; only one in this
  private planner"; T1 at 1.2.28 still says 200.
- No code was changed by this audit.

## 10. Implementation gates

1. **Bind by echoed code, never by position**, unless the publisher
   documents the order. None of the six does. Echo fields: KIS
   `inter_shrn_iscd`, Kiwoom `stk_cd`, LS `shcode`, DB `Iscd`, Toss
   `symbol`. A row without a parseable echo is an error, not "the next
   requested symbol".
2. **Exact set match:** every requested code must appear exactly once.
   A missing row, an extra row or a duplicate echo fails the call; no
   silent partial result and no first-match selection.
3. **Venue:** batch requests are `KRX`-only until each route's venue is
   verified. Send KIS `J`, DB `J` (no prefix), Kiwoom codes without
   suffix; do not offer LS `t8407` or Toss as `KRX` without venue evidence.
   Echo formats for `NX`/`_NX`/`N-` requests are unknown.
4. **Asset class:** accept six-digit stock codes only; never forward DB
   futures/options/index market codes or Toss US symbols into a KR
   `fetch_tickers`.
5. **Caps and counts:** enforce 30 (KIS), 50 (LS, DB), 200 (Toss) before
   sending; set `nrec`/`dataCnt` equal to the code count. Kiwoom stays
   unsupported for batches until a maximum is evidenced. Meritz batches are
   N single calls and must never put a list into `iscd`.
6. **No retries,** including no automatic re-send of a failed chunk; an
   `UNKNOWN` delivery for one chunk leaves the others unaffected but is not
   repeated (ADR 0013).
7. **Status:** each batch has one envelope status (`rt_cd`, `return_code`,
   `rsp_cd`, HTTP for Toss); no route documents per-row status. A missing
   status is never success.
8. **Field mapping per broker:** KIS needs `inter2_*`; Kiwoom keeps the
   signed-price rule; DB and Toss rows have no volume; only a row's own
   documented timestamp may fill `Ticker.timestamp` (Kiwoom `dt`+`cntr_tm`,
   Toss `timestamp`), and only after the time zone is verified.

## 11. Not verified

- Any gateway behaviour: acceptance, real/paper availability, entitlement.
- Row order, duplicate handling and missing/invalid-symbol behaviour at
  every broker; Toss 404 scope for a partly unknown batch.
- Echo format for venue-qualified codes (KIS `NX`, Kiwoom `_NX`/`_AL`, DB
  `N-`/`U-`).
- Kiwoom maximum count and enforcement of the 20-character `stk_cd`.
- LS `t8407` venue, and `nrec` mismatch handling; DB `dataCnt` mismatch
  handling and JSON type.
- KIS field types, signs, `hour_cls_code` values and the rate limit.
- Whether a batch call counts as one request in each broker's rate
  limiter; whether any batch route can return a continuation.
- Time zone of Kiwoom `cntr_tm`/`dt`; Toss `timestamp` source.
- Whether Toss accepts mixed KR/US symbol lists.
