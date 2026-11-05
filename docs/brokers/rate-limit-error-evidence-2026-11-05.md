# Six-broker rate-limit and error-code (호출 한도·오류 코드) evidence — 2026-11-05

- **Scope:** request limits, token-issuance limits, throttle and
  token-expiry signals, success-status envelopes, HTTP status use and
  error catalogs of the domestic-equity REST APIs of KIS, Kiwoom REST, LS,
  DB, Toss and Meritz. WebSocket limits are mentioned only in passing. The
  Shinhan comparison stays separate. Data-use and redistribution terms are
  out of scope.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No rate limit was measured and no error response was
  observed. This file changes no code and authorizes no mapping change.
- **No broker API request was sent.** No token, quote, account, MAC value or
  order request was made and no credential was used. Only public Git
  repositories, public portal pages and the portals' public,
  unauthenticated documentation JSON (spec exports, guide detail, FAQ and
  notice posts) were fetched. No broker gateway origin was contacted.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS: `git fetch` of the pinned SHA from `github.com` at 07:44:49.
  - Kiwoom: `git fetch` of the pinned SHA at 07:44:59, and of the older pin
    `953e5dbf` at 07:52:22 to confirm the shared tree (§3.1).
  - `git ls-remote` at 07:45: both pinned SHAs were still the `main` heads.
  - LS portal pages and JSON: 07:44:06–07:52:17 (§4.1).
  - DB portal JSON/HTML: 07:48:21–07:51:01; the DB repository at a fixed
    commit (§5.1).
  - Toss portal documents: 07:43:44–07:43:45 (§6.1).
  - Meritz portal pages and JSON: 07:43:53–07:45:40; the Meritz repository
    at a fixed commit, `HEAD` per `git ls-remote` at 07:46:16 (§7.1).
- **Re-hash:** every KIS and Kiwoom blob SHA in §2.1 and §3.1 was recomputed
  from the retrieved bytes with a separate script; all matched the tree
  entries.
- **Spot-check at merge (08:00:38–08:01:28 UTC):** the merging author
  re-fetched two or more pins per merged broker from the public sources.
  - LS: L1 sha256 `9aaca437f1925115`, t1102 `"transactionPerSec" : "10"`
    and version `20261026021444748`; L4 sha256 `492a376455696d40`, revoke
    example "접근토큰 폐기에 성공하였습니다." All matched.
  - DB: commit `564b5100…` (date 2026-08-20T10:06:26+09:00); D1 blob
    `889d4557…` (L48, L74 `IGW00201`; L199; L210–211); D2 blob `6ce92fdc…`
    L82–83; D3 blob `6000fa44…` L65–67; DP1 sha256 `eeb775c8ecd70a5f`
    with "1분에 1건" and "동일한 토큰이 발급됩니다". All matched.
  - Toss: T1 sha256 `c5918961335ccd6b` (L91 "재발급 시 이전에 발급된 token 은
    즉시 무효화됩니다"); T2 sha256 `bef057d9babe9a38` (L236, L264, L276).
    All matched.
  - Meritz: commit `a93c6409…` still `HEAD`; M6 `60370924…` L67, M7
    `b4b2eac6…` L8–9, L75, L95, M8 `8351d534…` L120–121 and M10
    `7c68d3a4…` L487–494, L529 matched, as did the M5, M9 and M11 blob
    SHAs. The M4 notice text (six content lines) and `createdDate` matched,
    but the whole-file sha256 differed (`e099c364d3c691cd` vs
    `06570a95f862eb3a…`): the JSON carries a changing `viewCount`. Treat
    the M4 hash as identifying the 07:45:01 copy only.
- **Pin formats:**
  - Git blob SHAs are `sha1("blob <len>\0" + bytes)` of the retrieved
    bytes, i.e. what `git hash-object` and `git ls-tree` print.
  - Line numbers are written "(K2 L351–357)": source K2, lines 351–357 of
    that blob.
  - Web pages have no immutable revision. Their sha256 prefix identifies
    only the copy retrieved at the stated time.
  - Raw copies were kept outside the repository. Sample tokens, app keys,
    account values, MAC values, IPs and staff contact data in publisher
    material are deliberately not copied.
- **Evidence levels:**
  - `field table`: a publisher field, spec or error-code table.
  - `publisher example`: a sample request/response or sample code.
  - `publisher client code`: SDK or helper behaviour, including its
    comments. It shows how the publisher calls the API; it is **not** a
    contract.
  - `legacy publisher example`: material under a publisher repository's
    `legacy/` directory. Older than the current examples, lower weight.
  - `publisher guide`: portal prose outside the field tables, including
    portal FAQ and notice posts. Notices can change limits at short notice
    (§4.2, §5.2).
  - `publisher repo note`: non-code text in a publisher repository (README,
    `.env.example`, docstrings that describe server behaviour).
  - `not found`.
- **Retry code is not a safety signal.** Publisher retry, back-off and
  re-authentication code is recorded as publisher behaviour only. It is
  never evidence that a retry is safe: an UNKNOWN send, a timeout or an
  error response (including HTTP 5xx) is never proof that the broker did
  not accept the request (AGENTS.md).
- Every inference is marked **Inference:**. "Not found" means the pinned
  sources say nothing about it.

## 1. Broker × concern summary

Cell format: short verdict — evidence. `F` field table, `E` publisher
example, `L` legacy publisher example, `C` publisher client code, `N`
publisher repo note, `G` publisher guide, `—` not found.

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Request limit | **no number** in the current pin; "초당 거래건수 초과" names `EGW00201`, paper limit "낮습니다" (N); client pacing 0.05 s real / 0.5 s paper intended (C); "1초당 20건 제한" (L) | **no number** in the pin; per-API / total / group quotas exist by code `1700`/`1701`/`1702` (F) | per TR only: `transactionPerSec` (t1102 10, t1301 2, charts 1); no app-wide limit; scope key not stated (F) | app "20 TPS (1초당 20건)" per app (계좌) (G, N) plus per API (PRICE 5, charts 4) (F, N); temporary cuts by notice (G) | per client × group: `MARKET_DATA` 15/s, `MARKET_DATA_CHART` 20/s, adjustable without notice; read `X-RateLimit-Limit` (G, F) | 10/s, **scope conflicting**: per account, all REST summed (G) vs per API (N) |
| Token issuance limit | "토큰 재발급 - 1분당 1회 발급됩니다" (N); re-issue within 6 h returns the same token (C comment); `EGW00133` **not found** | **no documented number**; "초당 ~2회, 2026-08-18 demo 실측", rejected as `1700` (N) | `"-"`; **not found** (F) | "1분에 1건" (F, G, C); re-issue before expiry returns the **same** token (F) | `AUTH` group 5/s; no interval; re-issue **invalidates** the previous token (F) | **not found** (`tps "-"`) (N) |
| Throttle signal | `msg_cd` `EGW00201` (N, C); HTTP status, headers and back-off interval **not documented** | `return_code` `1700`–`1702` (F); HTTP status **not documented**; one repo note says "유량 제한(429)" (N, ambiguous, §3.6) | **not found** (no status, code or header) | `rsp_cd` `IGW00201` under HTTP **403 and 500**; no 429, no headers (N, C) | HTTP **429** `rate-limit-exceeded` + `X-RateLimit-*`, `Retry-After` (F, G) | HTTP **500** + `rsp_cd` `EGW00200` (F, N); FAQ names `EGW00201` (G); no headers |
| Token-expired signal | `msg_cd` `EGW00123` with HTTP 200 (L only); no current source | `8005` "Token이 유효하지 않습니다" (F); also HTTP 401, or top-level code 3 with "[8005:…]" in `return_msg` (C) | **not found** | `IGW00121`/`IGW00122`/`IGW00123` under 403 or 400 (N, C) | HTTP 401 `expired-token`, `invalid-token`, `token-revoked` (F) | `EGW00123` expired, `EGW00121` invalid, HTTP 500 (G, N) |
| Success-status field | `rt_cd` string `"0"` (C, E); failure example `"1"` (E) | `return_code` JSON number `0` in REST examples (E); **no REST field table**; client accepts int or numeric string (C) | `rsp_cd` `"00000"` in every TR example; in a field table only for `session/clear` (E, F) | `rsp_cd` `"00000"`, required even on HTTP 200 (E, C); not in field tables | HTTP 200 + `result`; no code field (F) | `rsp_cd`, value **per API family** (`"0000"` for quotes; `0001`, `5762`, `5766`, `5820`, …) (F, E, C) |
| HTTP status meaningful | client treats any non-200 as failure and does not parse the body (C); which statuses occur is **not documented** | business errors are HTTP 200 (C comment); 401 triggers re-auth (C); bodies of ≥400 parsed for `return_code` (C) | REST TRs **not documented**; OAuth failures come as HTTP 200 + body `code` (C, portal script) | partly: same code under 403 and 500; client errors under 500 (N, C) | **yes**: 400/401/403/404/409/422/429/500 per route (F, G) | mostly **no**: "오류는 종류와 관계없이 HTTP 500" with exceptions (G, N) |
| Error catalog available | **not found** in the repo (portal not retrieved); scattered codes only | **yes**: 37-row `error_codes` table (F) | **not found** (only `IGW40011` in portal script) | **yes**, in the repo (68 platform + 70 service + 6 WebSocket rows) (N); portal spreadsheet not read | **yes**: 53-row table, 49 codes (G); 44 codes in spec examples (F); they differ | no portal catalog; repo table of 21 error and 8 success codes (N) |

## 2. KIS (Korea Investment & Securities)

### 2.1 Pinned sources

All sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362).
The full SHA is `3a9be59a3ed8745720dc3aa9d584bdf3b7830362`, the commit is
dated 2026-10-28T00:26:05+09:00 (subject "fix: 토큰 관리 및 OS 간 호환성
오류 수정"), and it was the `main` head at retrieval. Every link below uses
the pinned SHA.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | [`README.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/README.md) | `182887151f1fb07e5789a029292ac3e43d3ba9bd` | Token reissue note (L390), `EGW00201` note (L414–417). Same blob as the capability inventory's K6. |
| K2 | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) | `0e722d6f3253033efe3cf2b99845397b2b329655` | Publisher client: token comments, pacing, `rt_cd`/`msg_cd`/`msg1`, non-200 handling. Same blob as `examples_user/kis_auth.py`, the [candle audit](candle-evidence-2026-11-05.md)'s K9 and the [trade audit](trade-evidence-2026-11-05.md)'s K7. |
| K3 | [`strategy_builder/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/strategy_builder/kis_auth.py) | `7388421fd3f5afc7561022b8b1d4d8c70e574269` | Serialised min-interval limiter (L63–67, L446–458). Same blob as `backtester/kis_auth.py`. |
| K4 | [`examples_llm/auth/auth_token/auth_token.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/auth/auth_token/auth_token.py) | `21b0465c230ebc19c072a4441c5fa18073fc2637` | Token route `/oauth2/tokenP` (L28), failure handling (L104–113) |
| K5 | [`examples_llm/auth/auth_token/chk_auth_token.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/auth/auth_token/chk_auth_token.py) | `52cda980ee866f250d06a5ab5227200b223dc1a8` | Token response column labels (L25–30) |
| K6 | [`backtester/README.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/README.md) | `f31e49dab3c947e0a7be0c888f198b1ac476fc9b` | "API 속도 제한" note (L625–629) |
| K7 | [`backtester/examples/README.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/examples/README.md) | `47660d77b2f4e57d17c6395243e884f4125c2504` | `EGW00201` message text (L364–372) |
| K8 | [`backtester/kis_backtest/providers/kis/data.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/kis_backtest/providers/kis/data.py) | `28bf9aca834e4abd7c0b4b63ab0b9be61678de13` | `EGW00201` wait-and-retry (L11–14, L93–107; again L495–507). Same blob as the [candle audit](candle-evidence-2026-11-05.md)'s K12. |
| K9 | [`backtester/kis_mcp/tools/backtest.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/kis_mcp/tools/backtest.py) | `da4725ae8d1f5c77a479ab5bd571b9df6c93fd74` | Error classification by message text (L170–183) |
| K10 | [`MCP/KIS Code Assistant MCP/src/prompts/prompt.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/KIS%20Code%20Assistant%20MCP/src/prompts/prompt.py) | `202dda44e719455e801f3fd77e9ca0c084be4d8a` | Pacing and WebSocket registration limit text (L62–64, L87, L109) |
| K11 | [`MCP/Kis Trading MCP/Readme.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/Readme.md) | `3069ae6fba2173165cc82c74c3a9f1aaec07486d` | "API 호출 제한" note (L552–555) |
| K12 | [`MCP/Kis Trading MCP/configs/auth.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/configs/auth.json) | `85734ff523757546bce16beb48926f1c4fdc7cc1` | Publisher MCP registry for the token API (L25–28); **no** limit or error text |
| K13 | [`examples_llm/domestic_stock/psearch_result/psearch_result.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/psearch_result/psearch_result.py) | `a60a0b48201e8ce794b8fd4ccc445f359fecb61e` | Verbatim failure envelope for an empty result (L39–40) |
| K14 | [`examples_llm/domestic_futureoption/display_board_callput/display_board_callput.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_futureoption/display_board_callput/display_board_callput.py) | `0c834fed4d53f1eab568091b9e26e4d22a49f4bb` | Per-route call recommendation (L37); futures/options, context only |
| K15 | [`examples_llm/etfetn/etf_nav_trend/chk_etf_nav_trend.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/etfetn/etf_nav_trend/chk_etf_nav_trend.py) | `57665dbcc248351f92bfc6017a981ed42e71dde5` | Korean labels of `rt_cd`/`msg_cd` (L24–25); a WebSocket TR, labels only |
| K16 | [`legacy/rest/get_interest_stocks_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/rest/get_interest_stocks_price.py) | `6dbfd3497eebb2c5b8c762f7d065964eb9e9ba23` | **Legacy** "1초당 20건 제한" (L35, L61, L87, L103) |
| K17 | [`legacy/rest/get_ovsstk_chart_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/rest/get_ovsstk_chart_price.py) | `c856191e99b35dfa0981f6ce717e019a042bfdf4` | **Legacy**, same comment (L42, L87); overseas |
| K18 | [`legacy/rest/get_ovsfut_chart_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/rest/get_ovsfut_chart_price.py) | `bd5166616dd53988322ac7229d60e79eb1dbc480` | **Legacy**, same comment (L83); overseas futures |
| K19 | [`legacy/rest/current_price_samle.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/rest/current_price_samle.py) | `41df6db034c8cca3c700ab127b7f688a8c05b3cc` | **Legacy** `EGW00123` token-expiry handling (L44–50) |
| K20 | [`legacy/Sample02/CSharp/KIS_OverseaStk.cs`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/Sample02/CSharp/KIS_OverseaStk.cs) | `a586111f158c7b1a9d360bab9eafa66094748f07` | **Legacy** "no data" check on a success envelope (L149); overseas |

Search scope: every text file in the 1,203-path tree was searched for
`유량`, `초당`, `1분당`, `호출 제한`, `rate limit`, `EGW`/`OPSQ`/`IGW`/`MCA`
codes, `msg_cd`, `rt_cd`, `오류코드`/`에러코드`, `tokenP`, `revokeP` and
`Retry-After`. Only the hits above bear on this audit.

**Missing evidence:**

- **No error-code catalog** exists anywhere in the pinned tree. The only
  codes found are `EGW00201` (K1, K7, K8, K9), `EGW00123` (K19, legacy) and
  `MCA05918` (K13). `EGW00133` (often cited as a token-issuance code) is
  **not found**.
- **No numeric request limit** in any current (non-legacy) file.
- No token-revoke route (`revokeP` or similar) in the tree.
- No KIS field table for the `rt_cd`/`msg_cd`/`msg1` envelope; only column
  labels (K15) and client code (K2).
- The KIS developer-portal specification and notices were **not**
  retrieved for this audit.

### 2.2 Rate limits

| Concern | Value (verbatim) | Scope / unit | Real vs paper | Evidence |
| --- | --- | --- | --- | --- |
| Per-second / per-minute request limit | **No number.** K1 L414: "초당 거래건수 초과 (`EGW00201`)"; K6 L627: "한국투자증권 API는 초당 호출 횟수 제한이 있습니다."; K11 L554: "분당 호출 횟수 제한이 있을 수 있습니다". Client pacing: K2 L174 `_smartSleep = 0.05` (prod), L179 `0.5` (vps); K10 L63 "실전 0.05초, 모의 0.5초 sleep 적용". | Scope (app key, account, IP, TR) **not documented** | K1 L416: "모의투자 계좌는 REST API 호출 제한이 낮습니다." No numbers for either. | publisher repo note (K1, K6, K11); publisher client code (K2, K10) |
| Same, legacy | "유량제한 예방 (REST: 1초당 20건 제한)" | not stated | not stated | legacy publisher example (K16 L35; K17 L42; K18 L83) |
| Per-route (TR) limits | Only a recommendation, on a futures/options route: "잦은 호출을 삼가해주시기 바랍니다. (1초당 최대 1건 권장)" | that route | not stated | publisher example (K14 L37) |
| Token issuance limit / interval | K1 L390: "토큰 재발급 - 1분당 1회 발급됩니다." Error code for a breach: **not found**. | per app key? **not stated** | not stated | publisher repo note (K1) |
| Token lifetime and re-issue | K2 L220: "Token 발급, 유효기간 1일, 6시간 이내 발급시 기존 token값 유지, 발급시 알림톡 무조건 발송" (also L69, L87). Response labels: `expires_in` "접근토큰유효기간_초", `access_token_token_expired` "접근토큰유효기간_일시표시" (K5 L28–29). The expiry string is parsed as `"%Y-%m-%d %H:%M:%S"` with no zone (K2 L78). | per app key? not stated | K2 selects separate real/paper app keys (L231–236) | publisher client code (comment; K2), publisher example (K5) |
| Does re-issue invalidate the old token? | Per K2 L220, a request within 6 h returns the **same** token ("기존 token값 유지"); no statement on later re-issue | — | — | publisher client code (comment) |
| WebSocket limits (mention only) | "1개 appkey당 최대 41건 등록 제한" | per app key | not stated | publisher client code (MCP prompt; K10 L64, L109) |
| Continuation/paging limits relevant to throttling | **not found** (no per-page pacing rule; K2's `smart_sleep()` is called between pages by many examples) | — | — | publisher client code |

**Inference:** the K2 pacing values do not take effect. `changeTREnv`
declares `global _isPaper` only (K2 L169), so `_smartSleep = 0.05` and
`= 0.5` (L174, L179) bind a local variable and the module value stays
`0.1` (L57). A static `symtable` check of K2 and K3 reports
`_smartSleep` as local in `changeTREnv`. K3's limiter (L450–458) reads the
same module value, so its comment "모의투자 0.5초, 실전 0.05초 최소 간격
보장" does not describe what runs. Not executed; scoping only.

### 2.3 Status envelope and HTTP status use

| Concern | Value | Evidence |
| --- | --- | --- |
| Success indicator | `rt_cd` equal to the **string** `"0"`: K2 L353 `if self.getBody().rt_cd == "0"`. Label "성공 실패 여부" (K15 L24). | publisher client code; publisher example (labels) |
| Failure indicator + message fields | `rt_cd` other than `"0"`; `msg_cd` (label "응답코드", K15 L25) and `msg1` (K2 L322–323). Verbatim failure body in a publisher docstring: `{"rt_cd":"1","msg_cd":"MCA05918","msg1":"종목코드 오류입니다."}` (K13 L39). | publisher client code; publisher example |
| Is HTTP status meaningful? | K2 L478–485: only HTTP 200 is parsed into `APIResp`; any other status becomes `APIRespError(status_code, res.text)` whose error code is the status number as text and whose body is not parsed. The token call likewise accepts only 200 (K2 L251, K4 L104–113). Which non-200 statuses KIS sends, and for what, is **not documented**. | publisher client code |
| Throttle signal | `msg_cd` `EGW00201`, message "초당 거래건수를 초과하였습니다." (K7 L367). HTTP status: **not documented**. `Retry-After` / rate-limit headers: **not found**. | publisher repo note (K7); publisher client code (K8 L11–12) |
| Token-expired / invalid-token signal | Legacy only: `res.status_code == 200 and res.json()["msg_cd"] == "EGW00123"` under the comment "토큰 만료 시" (K19 L46–47). No current source names a token-expiry code. | legacy publisher example |
| Error-response body schema | Same root keys as success (`rt_cd`, `msg_cd`, `msg1`) for HTTP-200 failures (K2, K13). The body of non-200 responses: **not documented**. Token-endpoint error body: **not found**. | publisher client code; publisher example |

**Inference:** K8 compares `resp.error_code == "EGW00201"` (L99), and
`error_code` is `msg_cd` only when K2/K3 built an `APIResp`, i.e. on HTTP
200 (K2 L478–485). The publisher's own retry code therefore expects
`EGW00201` inside an HTTP-200 body. K9 matches the text "EGW00201" anywhere
in a message (L172), which would also catch a non-200 body. Neither is a
contract; the HTTP status of `EGW00201` stays unverified.

### 2.4 Error catalog and mapping concerns

Catalog: **not found** in the pinned repository (no table, CSV, JSON or
Markdown list of `msg_cd` values). Three codes appear in passing.

| Concern | Code(s) + message verbatim | Evidence |
| --- | --- | --- |
| Rate limit exceeded | `EGW00201` "초당 거래건수를 초과하였습니다." | publisher repo note (K7 L367); K1 L414 heading |
| Token expired / invalid / revoked | `EGW00123` (no message text; comment "토큰 만료 시") | legacy publisher example (K19 L46–47) |
| Credential / app-key invalid | not found | — |
| Permission / entitlement / IP allow-list / service not subscribed | not found | — |
| Invalid symbol / no such instrument | not found for quote routes. `MCA05918` "종목코드 오류입니다." is documented as the answer to a condition search with **zero** results: "조건검색 결과 검색된 종목이 0개인 경우 위 응답값을 수신하게 됩니다." | publisher example (K13 L39–40) |
| Invalid parameter / malformed request | not found | — |
| Market closed / outside service hours | not found | — |
| Server busy / maintenance / internal error | not found | — |
| "No data" returned as success? | **Both forms appear.** K13: an empty condition search is a failure (`rt_cd "1"`, `MCA05918`). Legacy K20 L149 treats `rt_cd "0"` whose `msg1` contains "조회할 자료가 없습니다" as no data (overseas route). | publisher example; legacy publisher example |

### 2.5 Publisher retry / back-off behaviour (recorded, not adopted)

- **Fixed pacing:** `smart_sleep()` sleeps `_smartSleep` seconds (K2
  L289–293); examples call it between pages. K3 serialises every REST call
  behind a lock with a minimum interval (L63–67, L450–458). Effective value:
  §2.2 inference.
- **Rate-limit wait-and-retry:** K8 retries a daily-chart GET after
  `EGW00201`, sleeping `_RATE_LIMIT_WAIT = 61` seconds with the comment
  "KIS 한도 초기화 대기", up to `_RATE_LIMIT_MAX_RETRIES = 3` attempts
  (L11–14, L93–107; again L495–507). Read-only routes only.
- **Advice text:** K9 tells the caller "KIS API 한도 초과(EGW00201). 60초 후
  retry_backtest(job_id)를 호출하세요." (L183).
- **Re-authentication:** `reAuth()` re-issues when
  `(n2 - _last_auth_time).seconds >= 86400` (K2 L279–282), gated by
  `_autoReAuth = False` (L54). **Inference:** `timedelta.seconds` is always
  below 86400, so this condition never holds.
- **Legacy token-expiry retry:** on `EGW00123` the legacy sample calls
  `auth()` and repeats the quote call once (K19 L47–49).
- **WebSocket** (mention only): reconnects up to `max_retries = 3` with a 1 s
  sleep (K2 L691, L746–762).

None of this is adopted. In particular K8's 61-second wait is not evidence of
the KIS reset window, and none of it shows that repeating a request is safe.

### 2.6 Contradictions and gaps

1. **Per-second, per-minute or 61-second window?** K1/K7 name `EGW00201`
   "초당 거래건수", but K8 waits 61 s "KIS 한도 초기화 대기", K9 advises 60 s,
   and K11 says "분당 호출 횟수 제한이 있을 수 있습니다". The pinned sources do
   not resolve the window.
2. **Intended vs effective pacing:** comments say 0.05 s real / 0.5 s paper
   (K2 L174/179, K3 L450, K10 L63); the code keeps 0.1 s (§2.2 inference).
   The legacy "1초당 20건" (K16–K18) matches 0.05 s, not 0.1 s.
3. **"No data" envelope:** failure with a misleading "종목코드 오류입니다."
   (K13) vs success with "조회할 자료가 없습니다" (K20, legacy).
4. **Token re-issue:** "1분당 1회 발급" (K1) vs "6시간 이내 발급시 기존
   token값 유지" (K2). Both may hold (a rate limit on issuance; the same
   token returned inside 6 h), but neither says what a second request within
   one minute returns.
5. **Expiry fields:** K5 lists both `expires_in` (seconds) and
   `access_token_token_expired` (zone-less date-time); K2 uses only the
   latter. Their consistency is not documented.
6. **Gaps:** no catalog, no HTTP status for any code, no throttle headers,
   no token-error body, no revoke route, no maintenance or market-hours
   code.

### 2.7 Relation to KTradeLink error taxonomy (Inference only)

| Candidate class | KIS signal | **Inference:** status | Evidence that would confirm it |
| --- | --- | --- | --- |
| `RateLimitExceeded` | `msg_cd` `EGW00201` | **Inference:** only if the code is read from the body; nothing shows KIS answers 429. Today a 200 body would give `BrokerRejected`, a 5xx `BrokerUnavailable`. | Sanitised authorized `EGW00201` response with its HTTP status; portal error table |
| `AuthenticationError` | `EGW00123` (legacy, HTTP 200) | **Inference:** plausible for token expiry, but legacy-only and the status is from sample code | Current portal table; sanitised expired-token response |
| `PermissionDenied` | not found | — | Portal entitlement error rows |
| `BrokerUnavailable` | not found | — | Portal maintenance/internal codes and their HTTP status |
| `BrokerRejected` | any `rt_cd != "0"` in an HTTP-200 body (K2, K13) | **Inference:** matches the current generic class | — |
| `InvalidSymbol` | `MCA05918` is **not** usable: it signals an empty condition search (K13) | **Inference:** no KIS invalid-symbol code is evidenced | Portal table |
| `InvalidParameter` | not found | — | Portal table |
| `ResponseSchemaError` | missing `rt_cd`, wrong JSON type | **Inference:** library policy, not a KIS code | — |

### 2.8 Gates and not-verified items

- HTTP status, body and headers of `EGW00201`; the throttle window and
  scope (app key, account, IP, TR); real vs paper numbers.
- The token-issuance limit's error code and HTTP status; whether a second
  token request within one minute or within six hours returns the same
  token, a new one, or an error.
- A current KIS error catalog (portal), including token-expiry,
  entitlement, invalid-symbol and maintenance codes.
- The "no data" envelope for the quote routes KTradeLink uses.
- Whether `expires_in` and `access_token_token_expired` agree, and the
  latter's time zone (already a gate in ADR 0013).

## 3. Kiwoom REST

### 3.1 Pinned sources

All sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@c7a3d254`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/c7a3d25449ed4b4238bef378780c41103c67b9e9).
The full SHA is `c7a3d25449ed4b4238bef378780c41103c67b9e9`, the commit is
dated 2026-09-15T15:12:16+09:00, and it was the `main` head at retrieval.
Its tree is `4eb7d5497f4155ace73d8d37a03f3dc18abbe6fa`. The older pin
`953e5dbff123f437ab4d11a78a95191a685eb51f`, fetched by SHA for this audit,
names the **same tree**, so every blob below is identical under both pins
(as already recorded in the [trade audit](trade-evidence-2026-11-05.md) §3.1).

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field tables:** `error_codes` (L107018–107203); `au10001` 접근토큰 발급 (L3–164); `au10002` 접근토큰폐기 (L165–295); `ka10001` example (L1820); `returnCode` examples (L11461, L24751); WebSocket `return_code` rows (L29157, L29380, L95535) |
| W2 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | Searched; **no** limit, throttle or error-code text |
| W3 | [`kiwoom/core/errors.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/errors.py) | `dd7a8709bccd8a28601c49d26a298d3c92f34e5d` | Code classes (L169–189), embedded codes (L4–27), `return_code` type (L30–44), dispatch (L204–230) |
| W4 | [`kiwoom/core/client.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/client.py) | `52d915c9e2f38f21885efbc428d3b50593a452c9` | HTTP handling and auth retry (L61–109), page delay (L151–152, L184–185) |
| W5 | [`kiwoom/core/auth.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/auth.py) | `9026aae207b7e2963c40f06e5e9a2f287a589d28` | Token issue (L114–160), revoke (L171–206), KST expiry (L21, L325–327), error helper (L354–360) |
| W6 | [`kiwoom/core/ws_client.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/ws_client.py) | `3c47b80f9ccef211ef9323ce014f1ff710544fd1` | WebSocket login retry (L49–66), mention only |
| W7 | [`…/종목정보/get_domestic_stock_info.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_info.py) | `c39741c73f0f8bdbc47694de24abf3cbaaf1d402` | `ka10001` example client: paging constants (L20–21), status check (L186), delay (L207) |
| W8 | [`mcp_exec/src/kiwoom_exec_mcp/tokens.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/mcp_exec/src/kiwoom_exec_mcp/tokens.py) | `84ba998452a3f0f397eb559ad3aea3e2434c764d` | Docstring on `au10001` throttling, token lifetime and re-issue (L1–16), expiry margin (L36–38) |
| W9 | [`mcp_exec/.env.example`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/mcp_exec/.env.example) | `ff2bdb84204537cdbff75e8131da71dd3dcd05f4` | Same `au10001` note (L26–27); the MCP server's own limits are not Kiwoom's (L29–30) |
| W10 | [`mcp_exec/README.md`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/mcp_exec/README.md) | `a25c4c367fa8007521de6ee61549305f0e5fb766` | "알려진 제약" (L108–114), including "유량 제한(429)" |
| W11 | [`mcp_exec/src/kiwoom_exec_mcp/ratelimit.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/mcp_exec/src/kiwoom_exec_mcp/ratelimit.py) | `0d296c0d64a213a96773d4e366260a40f57e75b8` | The MCP server's **own** 429 with `retry-after` (L112–120) |
| W12 | [`README.md`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/README.md) | `018e50aad8156d18f057135a91ce2a15d09ce2d2` | "API 응답 코드/메시지가 보임" (L436–438) |

In the W7 link, `…/종목정보/` stands for
`examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/`
(`examples/국내주식/종목정보/`).

**Missing evidence:**

- No numeric quota (per second, per minute, per app key, per account) in
  any file of the pinned tree. The `1700`–`1702` messages carry the quota
  only as a runtime placeholder ("유량={?}").
- No HTTP status for any error code; no throttle response headers.
- No REST field table for `return_code` / `return_msg`; they appear in
  REST response *examples* only.
- The Kiwoom developer portal (including the quota page cited in
  [kiwoom-market-data.md](kiwoom-market-data.md)) was **not** retrieved
  for this audit.

### 3.2 Rate limits

| Concern | Value (verbatim) | Scope / unit | Real vs paper | Evidence |
| --- | --- | --- | --- | --- |
| Per-second / per-minute request limit | **No number.** Error rows: `1700` "허용된 API 요청 개수를 초과하였습니다. 유량={?}, API ID={?}"; `1701` "허용된 전체 요청 개수를 초과하였습니다. 총유량={?}"; `1702` "허용된 그룹 요청 개수를 초과하였습니다. 총유량={?}, API_ID={?}" | per API ID, overall, and per **group** of APIs (group membership **not documented**); unit and holder (app key, account, IP) **not documented** | not documented | field table (W1 L107076–107087) |
| Per-route (TR) limits | Per-API quotas exist by `1700`; values **not documented** | per API ID | not documented | field table (W1) |
| Recursive-call limit | `1687` "재귀 호출이 발생하여 API 호출을 제한합니다, API ID={?}" | per API ID | not documented | field table (W1 L107071–107072) |
| Token issuance limit / interval | **No documented number.** W8 L3–5: "요청마다 subprocess가 `/oauth2/token`을 부르면 키움 `au10001` 유량 제한(초당 ~2회, 2026-08-18 demo 실측)에 걸려 같은 키로 조회를 3~5개만 연달아/동시에 보내도 절반이 `1700`으로 거절된다." Repeated in W9 L27. | per key (by the note) | measured on **demo** only, by the publisher's note | publisher repo note (W8, W9) |
| Token lifetime and re-issue | `expires_dt` "만료일" (W1 au10001 field table), example `"20241107083713"` (W1 L163); W5 parses it as `%Y%m%d%H%M%S` in KST (L21, L325–327). W8 L10: "키움 토큰 자체는 ~24h 유효하지만". | per app key | both origins listed in the table | field table; publisher example; publisher client code; publisher repo note |
| Does re-issue invalidate the old token? | W8 L13–14: "키움은 유효 토큰이 있으면 같은 토큰을 돌려주므로 TTL마다의 재발급은 사실상 \"현재 토큰 조회\"이고 다른 클라이언트의 토큰을 끊지 않는다." Explicit revoke: `au10002` POST `/oauth2/revoke` with `appkey`, `secretkey`, `token` (W1 L165–295). | per key | both origins listed | publisher repo note; field table |
| Token bound to IP | `8010` "Token을 발급받은 IP와 서비스를 요청한 IP가 동일하지 않습니다" | per token | not documented | field table (W1 L107141–107142) |
| WebSocket limits (mention only) | not found | — | — | — |
| Continuation/paging limits relevant to throttling | Client policy only: `iterate_pages(max_pages=1, page_delay_seconds=0.2)` "서버 요청 간격 정책을 지킵니다" (W4 L151–158); examples `MAX_PAGES = 10`, `REQUEST_DELAY_SECONDS = 0.2` (W7 L20–21; the same two constants appear in 304 example files) | client | — | publisher client code; publisher example |

### 3.3 Status envelope and HTTP status use

| Concern | Value | Evidence |
| --- | --- | --- |
| Success indicator | `return_code` `0` with `return_msg` "정상적으로 처리되었습니다" in REST examples, e.g. `ka10001` (W1 L1820). 331 of 337 W1 `response_example` strings contain `return_code`, every value written as the JSON number `0`; 2 REST examples use **`returnCode`** instead (`ka10030` L11461, `ka10084` L24751); 4 US WebSocket examples carry neither. | publisher example |
| Field-table type | **No REST field table lists `return_code`.** Only WebSocket tables do, as `String`: "정상 : 0" (`ka10171`, W1 L29157), "정상:0 나머지:에러" (`ka10172`, L29380), "등록,해지요청시에만 값 전송 0:정상,1:오류" (L95535). | field table (WebSocket only) |
| Client view of the type | W3 L33–35: "The server emits the code as an int or a numeric string (\"0\", \"0000\", \"8005\") depending on the endpoint." W4 L84 normalizes before comparing; W4 L105 and W7 L186 treat a **missing** `return_code` as success. | publisher client code |
| Failure indicator + message fields | non-zero `return_code` plus `return_msg`. W3 L8–10: "Kiwoom often reports a generic top-level ``return_code`` (e.g. 3 = \"인증에 실패했습니다\") and puts the specific code inside ``return_msg`` as ``[8005:Token이 유효하지 않습니다]`` (REST) or ``CODE=8005`` (WebSocket)." | publisher client code |
| Is HTTP status meaningful? | W4 L104: "키움은 업무 오류도 HTTP 200으로 내려보내고 실패 여부는 본문 return_code에만 담는다." W4 L61–72 treats HTTP **401** as an auth failure; L98–102 raises for any status ≥ 400 after reading `return_code`/`return_msg` from the body. Which codes come with which status is **not documented**. | publisher client code |
| Throttle signal | `return_code` `1700`/`1701`/`1702` (W1). HTTP status **not documented**; headers (`Retry-After`, `X-RateLimit-*`) **not found**. W10 L114 says "너무 짧은 간격으로 `kiwoom_query`를 반복 호출하면 유량 제한(429) 오류가 날 수 있습니다." (ambiguous, §3.6). | field table; publisher repo note |
| Token-expired / invalid-token signal | `8005` "Token이 유효하지 않습니다" (W1 L107126–107127). Per W4 L85–86 it arrives as top-level `8005` or as `3` with "[8005:...]" in `return_msg`; W4 L61 also handles HTTP 401. No separate "expired" code exists in W1. | field table; publisher client code |
| Error-response body schema | Same root keys as success (`return_code`, `return_msg`) per W3/W4. No field table or example of an error body. W4 L79–82 copes with a non-JSON 200 body. | publisher client code |

### 3.4 Error catalog and mapping concerns

Catalog: W1 `error_codes`, L107018–107203, **37 rows** with columns `No.`,
`오류코드`, `오류메시지`. All codes are four digits. Categories (counts):
request/header validation `1501`–`1517` (10); call control `1687`,
`1700`–`1702` (4); instrument `1901`–`1903` (3); unexpected `1999` (1);
app key and token `8001`–`8020` (12); real/paper mismatch `8030`–`8031`
(2); device authentication `8040`, `8050`, `8103` (3); service availability
`8104`, `8200` (2). The catalog gives **no HTTP status** per code.

| Concern | Code(s) + message verbatim | Evidence |
| --- | --- | --- |
| Rate limit exceeded | `1700` "허용된 API 요청 개수를 초과하였습니다. 유량={?}, API ID={?}"; `1701` "허용된 전체 요청 개수를 초과하였습니다. 총유량={?}"; `1702` "허용된 그룹 요청 개수를 초과하였습니다. 총유량={?}, API_ID={?}"; related `1687` "재귀 호출이 발생하여 API 호출을 제한합니다, API ID={?}" | field table (W1 L107071–107087) |
| Token expired / invalid / revoked | `8005` "Token이 유효하지 않습니다"; `8003` "Access Token을 조회하는데 실패했습니다. 실패사유={?}"; `8031` "투자구분(실전/모의)이 달라서 Token를 사용할수가 없습니다"; revoke failures `8015` "Access Token을 폐기하는데 실패했습니다. 실패사유={?}", `8016` "Access Token을 폐기하는데 실패했습니다. 입력값에 Token이 들어오지 않았습니다"; header errors `1513`–`1516` (missing/malformed `authorization`) | field table (W1) |
| Credential / app-key invalid | `8001` "App Key와 Secret Key 검증에 실패했습니다"; `8002` "App Key와 Secret Key 검증에 실패했습니다. 실패사유={?}"; `8020` "입력파라미터로 appkey 또는 secretkey가 들어오지 않았습니다."; `8030` "투자구분(실전/모의)이 달라서 Appkey를 사용할수가 없습니다"; issuance `8006`, `8009`, `8011`, `8012` | field table (W1) |
| Permission / entitlement / IP allow-list / service not subscribed | `8010` "Token을 발급받은 IP와 서비스를 요청한 IP가 동일하지 않습니다"; `8040` "단말기 인증에 실패했습니다"; `8050` "지정단말기 인증에 실패했습니다"; `8103` "토큰 인증 또는 단말기인증에 실패했습니다. 실패사유={?}"; `8104` "모의투자에서 지원하지 않는 API 입니다."; `8200` "법인 고객은 해당 API를 지원하지 않습니다. API ID={?}, URI={?}" | field table (W1) |
| Invalid symbol / no such instrument | `1901` "시장 코드값이 존재하지 않습니다. 종목코드={?}"; `1902` "종목 정보가 없습니다. 입력한 종목코드 값을 확인바랍니다. 종목코드={?}"; `1903` "종목 정보가 없습니다. 입력한 종목코드, 거래소구분 값을 확인바랍니다. 거래소구분={?}, 종목코드={?}" | field table (W1 L107091–107102) |
| Invalid parameter / malformed request | `1511` "필수 입력 값에 값이 존재하지 않습니다. 필수입력 파라미터={?}"; `1517` "입력 값 형식이 올바르지 않습니다. 파라미터={?} 실패사유= {?}"; API-ID errors `1501`, `1504`, `1505`; header `1512` | field table (W1) |
| Market closed / outside service hours | not found (W12 L438 only advises checking "장 운영 시간") | publisher repo note |
| Server busy / maintenance / internal error | `1999` "예기치 못한 에러가 발생했습니다. 실패사유={?}"; no busy or maintenance code | field table (W1 L107106–107107) |
| "No data" returned as success? | not found | — |

### 3.5 Publisher retry / back-off behaviour (recorded, not adopted)

- **Re-authenticate and resend once:** on HTTP 401 (W4 L61–70), and on
  `return_code` or embedded code in `AUTH_RETRY_RETURN_CODES = {8005, 8031,
  8103}` (W3 L6; W4 L87–96), the client clears its token, issues a new one
  and resends **the same request** once. This applies to every method,
  including POST order routes; nothing in W4 limits it to reads.
- **Rate limit:** no automatic retry. `1700`–`1702` raise `RateLimitError`
  whose text says "요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요."
  (W3 L120–124, L214–215).
- **Paging delay:** 0.2 s between pages (W4 L151–152, L184–185; W7 L21,
  L207).
- **Token reuse:** a cached token is reused until 600 s before expiry
  (`refresh_buffer_seconds: int = 600`, W5 L93); the MCP server issues once
  per key ("single-flight") and caches it for 900 s to stay under the
  `au10001` throttle (W8 L9–16, L36–38).
- **WebSocket** (mention only): one login retry after an auth code (W6
  L49–66).

None of this is adopted. W4's resend after `8005` is a publisher choice; it
is not evidence that the first request was not executed.

### 3.6 Contradictions and gaps

1. **`return_code` type:** JSON number `0` in every REST example; `String`
   in the (WebSocket-only) field tables; "int or a numeric string" per the
   client (W3 L33–34). Two REST examples use `returnCode` (W1 L11461,
   L24751).
2. **Codes outside the catalog:** W3 L8–10 describes generic top-level
   codes such as `3` (and W3 L205 "3, 5, ...") that are not among the 37 W1
   rows.
3. **Token response:** the `au10001` field table lists only `expires_dt`,
   `token_type`, `token`; the example adds `return_code` and `return_msg`
   (W1 L163), and that example is not valid JSON (no comma after the
   `token` value).
4. **Throttle HTTP status:** W4 L104 says business errors are HTTP 200;
   W10 L114 speaks of "유량 제한(429)". W10 L110 says the listed limits are
   "키움 API 자체의 제약", but the same MCP server answers its **own** 429
   with `retry-after` (W11 L112–120), so the 429 may be the server's, not
   Kiwoom's.
5. **Missing status = success?** W4 L105, W5 L137 and W7 L186 accept a
   missing `return_code` as success; W5 L197–198 rejects a revoke response
   without it.
6. **Token issuance throttle shares `1700`** with per-API request limits
   (W8 L5), so `1700` alone does not say which budget was exhausted.
7. **Gaps:** no numbers, no HTTP status per code, no headers, no
   market-hours or maintenance code.

### 3.7 Relation to KTradeLink error taxonomy (Inference only)

| Candidate class | Kiwoom signal | **Inference:** status | Evidence that would confirm it |
| --- | --- | --- | --- |
| `RateLimitExceeded` | `1700`, `1701`, `1702` (and possibly `1687`) | **Inference:** strong by code text; but if they arrive in an HTTP-200 body the current code gives `BrokerRejected`. | Sanitised authorized `1700` response with HTTP status |
| `AuthenticationError` | HTTP 401 (W4); `8005`, `8003`, `8031`, `8103`; credential codes `8001`, `8002`, `8020`, `8030`; embedded "[8005:…]" | **Inference:** strong by code text; HTTP status unknown | Sanitised expired/invalid-token response |
| `PermissionDenied` | `8010`, `8040`, `8050`, `8104`, `8200` | **Inference:** by text; `8104` and `8200` might instead be `UnsupportedCapability` | Maintainer decision; sanitised responses |
| `BrokerUnavailable` | `1999` only | **Inference:** weak; "예기치 못한 에러" is not a busy signal | Portal maintenance notice format |
| `BrokerRejected` | any other non-zero `return_code` | **Inference:** matches the current generic class | — |
| `InvalidSymbol` | `1901`, `1902`, `1903` | **Inference:** strong by text | Sanitised response |
| `InvalidParameter` | `1501`–`1517`, `8011`, `8012` | **Inference:** by text | — |
| `ResponseSchemaError` | missing or non-int `return_code` | **Inference:** library policy; note the client's int-or-string claim (§3.6) | Sanitised success response for each route used |

### 3.8 Gates and not-verified items

- Numeric quotas, their holder (app key, account, IP) and the API groups
  behind `1702`; real vs paper.
- HTTP status of `1700`–`1702`, `8005` and every other code; any
  rate-limit headers.
- The JSON type of `return_code` on `ka10001`, `ka10004` and the chart
  routes, and the `returnCode` variants.
- Whether generic codes such as `3` occur, and the embedded-code format.
- The `au10001` throttle (repo note "초당 ~2회", demo) and its real-origin
  value; whether a re-issue returns the same token on the real origin.
- The `8010` IP binding for clients behind changing egress IPs.

## 4. LS Securities

### 4.1 Pinned sources

All LS sources are public pages or JSON on `https://openapi.ls-sec.co.kr`
with no immutable revision. L1 is the only one with a publisher version
marker. Each sha256 prefix identifies only the copy retrieved on 2026-11-05
at the stated UTC time (window 07:44:06–07:52:17Z). Detail endpoints are
`/guide/api/<data-tr>?type=rest&api=<data-api>`; the ids are from L2. Line
numbers in L1 and L7 are 1-based lines of the retrieved copy.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true | `9aaca437f1925115`, 07:44:06Z, 2,792,313 bytes; publisher `"version" : "20261026021444748"` (L2). This is the same version and hash as the trade/candle ledgers. | `transactionPerSec` per TR (369 TRs); token L41, revoke L123, t8430 L15327, t8436 L15464, t1101 L17767, t1102 L18309, t1301 L19684, t9945 L24038, t8410 L43368, t8412 L43941, t8451 L44238, t8452 L44587 (lines of `"code"`) |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `2d55b7b0044232ba`, 07:45:03Z (the page varies per request) | `data-tr` / `data-api` ids |
| L3 | `…/guide/api/07112bqm-8133-8wf2-ckd2-o8o7210v5m6o?type=rest&api=33bd887a-6652-4209-88cd-5324bc7c5e36` (token) | `4acff92cdcdfd551`, 07:46:31Z (same hash as the live-auth-transport-gates copy) | Token field table and example, `transactionPerSec` `"-"` |
| L4 | `…/guide/api/7tso3860-d2r6-7m2d-b431-yle82vfngam8?type=rest&api=2d923333-f816-4df9-932d-ad390437b66f` (revoke) | `492a376455696d40`, 07:46:33Z | Revoke envelope `code` / `message` |
| L5 | Detail JSON for the market-data TRs: t1102 `wqs8bq62-…`, t1101 `8tb7j8m8-…`, t1301 `f1408ze5-…`, t9945 `u4hepin5-…` (api `54a99b02-…`); t8410 `8ncj7d41-…`, t8412 `57t2im3o-…`, t8451 `afda5e31-…`, t8452 `0aa3dd33-…` (api `12320341-…`); t8430 `ir3h1jd3-…`, t8436 `10b608pg-…` (api `316495d3-6109-45a6-baaf-9e8a0261f30a`) | t1102 `42712ce969a8a480`, t1101 `e3bdd31adba31afb`, t1301 `768799e97d57c8d5`, t9945 `47a2ce86b41d3379`, t8410 `e45ad8da9fa0fb60`, t8412 `feefeb24704f16fa`, t8451 `445482b6bdc1369d`, t8452 `3b4fbf7328ba63c5`, t8430 `5b017d334785e9fd`, t8436 `efbc50d023d9e06b`; 07:46:35–07:46:52Z. t1102/t1301/t8410–t8452 match earlier pinned copies. | `transactionPerSec`, response header table, `responseExample` envelope, `qrycnt` |
| L6 | `…/guide/api/67c4aa4c-19e2-45d0-9f76-b83a70bd4ad9?type=rest&api=d80b2a7c-ea3d-49d9-a065-9c40c1c89174` (`/websocket/session/clear`) | `0b09a1d143f5dc51`, 07:46:54Z | The only REST field table that lists `rsp_cd` / `rsp_msg` |
| L7 | https://openapi.ls-sec.co.kr/renewal/js/apiguide-52fb3f6955943fdee555972c5802f07e.js (the API-guide page script) | `a46b0b4e534868e6`, 07:46:02Z, 1,583 lines | **publisher client code** (portal tester): L811–812, L1059–1064, L1270, L1350–1362, L1375–1378 |
| L8 | https://openapi.ls-sec.co.kr/howto-use | `c3c3677608bef22b`, 07:44:49Z | Token example `expires_in` 86400 "// 24시간"; app-key 사용해지 note |
| L9 | https://openapi.ls-sec.co.kr/community-faq (302 → `/community/10000000-0000-0011-0000-000000000002`) | `95618113d53e496d`, 07:44:53Z (9 FAQ rows) | Paper-order retry advice; continuation loop |
| L10 | https://openapi.ls-sec.co.kr/community-notice (302 → `/community/10000000-0000-0011-0000-000000000001`) and `?page=1…5` | `404a886274e025b3`, 07:45:16Z (page 0) | Notice titles ("총 57 건") |
| L11 | Notice posts `…/community/10000000-0000-0011-0000-000000000001/posts/<id>?page=0&tab=`: `043f99f1-271c-4d00-93e4-21b1fbff8de0` (2026-09-23), `03f7e4d4-cdb3-4276-a7b6-0f27ca5ebfb5` (2026-10-16), `57513975-963b-4e00-b78c-9dba14f02a3f` (2025-11-05), `096796f5-f50a-48dd-8a9d-0a8afebeabcf` (2023-10-25) | `b5937c98d36c3f19` (07:51:52Z), `976299afbcb51a5e` (07:51:50Z), `a0f9bff9e0deedae` (07:52:16Z), `0539af4789a76b0a` (07:52:17Z) | WebSocket session/subscription limits; history of TR TPS changes |
| L12 | t8411 detail (trade ledger L8 copy) | `a6e3395d3e5b05c8`, 07:11:27Z | `"rsp_cd": "00000"` with "해당자료가 없습니다." |

**Missing evidence:**

- **No REST error-code / 응답코드 catalog** was found on the portal: not in
  L1, the detail JSON (L3–L6), howto-use, FAQ, notice titles, or the
  portal scripts. `xing-help` lists an "xingAPI 에러코드표"; that is the
  legacy xingAPI (COM) manual. It was not opened and is not REST evidence.
- **No over-limit response** (HTTP status, `rsp_cd`, message or header) for
  REST TRs is documented anywhere found.
- No statement of the TPS scope (app key, account, IP or TR), the window
  (rolling or fixed second), or whether paper has separate limits.
- No token-issuance rate limit and no statement on whether re-issuing a
  token invalidates the previous one.
- The TR lists for two TPS-change notices (L11, 2023-10-25 and 2025-11-05)
  are image attachments ("LS증권_OPEN API 유량변경.png"); they were not
  downloaded or read.
- No publisher SDK or Git repository for LS REST.

### 4.2 Rate limits

| Concern | Value (verbatim) | Scope / unit | Real vs paper | Evidence |
| --- | --- | --- | --- | --- |
| Per-second / per-minute request limit | Per TR only: `"transactionPerSec"`. No app-, account- or IP-wide REST limit found. | Per TR; the counter's key (app key / account / IP) is **not documented** | L1 has one REST server; paper is not a separate REST origin (L1 `simulationUrl` exists only for WEBSOCKET). Paper limits not documented. | field table (L1, L5) |
| Per-route (TR) limits | Target TRs: t1102 `"10"`, t1101 `"10"`, t8450 `"10"`, t1301 `"2"`, t9945 `"2"`, t8430 `"2"`, t8436 `"2"`, t8407 `"5"`; chart t8410, t8411, t8412, t8451, t8452, t8453 all `"1"`. Detail JSON (L5) agrees with L1 for every target TR. | Per TR per second | as above | field table (L1, L5) |
| — distribution | 253 REST TRs: `"1"` ×160, `"2"` ×52, `"3"` ×5, `"5"` ×7, `"10"` ×27, `"-"` ×2 (token, revoke). `/stock/market-data` (25 TRs): `10` ×3, `5` ×1, `3` ×2, `2` ×8, `1` ×11. `/stock/chart` (7): all `1`. `/stock/etc` (10): `2` ×2, `1` ×8. | — | — | field table (L1) |
| Token issuance limit / interval | `/oauth2/token` and `/oauth2/revoke`: `"transactionPerSec" : "-"`. No per-minute or per-day statement. | — | — | field table (L1 L41, L123; L3, L4); limit **not found** |
| Token lifetime and reissue | Field table: `expire_in` "접근토큰 유효기간" String 10, "유효기간(초)". Example: `"expires_in": 86400` (JSON number). L8: `"expires_in" : 86400 // 24시간`. Reissue behaviour: **not found**. L8 only says that after "'사용해지'후 재등록 … 기존 발금된 토큰은 만료돼요." | Seconds | not documented | field table (L3), publisher example (L3, L8) |
| WebSocket limits (mention only) | Before: "세션 : 계좌(앱키) 무제한 및 IP당 20개", "구독제한 : 무제한". 1차 (from "2026년 10월 31일 08:00~"): "세션 : 계좌(앱키)당 3개", "※ 향후 구독갯수 제한 예정입니다." Announced final: "세션 : 계좌(앱키)당 3개", "구독제한 : 세션당 200개", "※ 동일 종목의 다른 실시간 구독 경우 개별 구독 적용". | Per app key | not stated | publisher guide (L11) |
| Continuation / paging | Chart `qrycnt` "요청건수(최대-압축:2000비압축:500)", "OPENAPI에서는 압축 미제공" (t8410). Continuation via headers `tr_cont` "연속거래 여부 Y:연속○ N:연속×" / `tr_cont_key` plus body `cts_*`. No inter-page delay is stated. The FAQ loop (`t1305`) calls back-to-back with no sleep. | Rows per call | — | field table (L5), publisher example (L9) |

**Limits change over time (publisher notices, L11):**

- 2023-10-25: "주식 시세 및 실시간체결잔고 TR 의 잦은 호출로 인한 서버과부하
  관계로 다음과 같이 초당 전송횟수를 일시적으로 변경" (effective "2023년
  11월 27일(월) 17시(예정)").
- 2025-11-05: "2차례에 걸쳐 일부tr 유량 확대", round 2 (2025-11-12)
  covering "국내주식".

The TR lists in both notices are images that were not read. L1 values are
valid for catalog version `20261026021444748` only.

### 4.3 Status envelope and HTTP status use

| Concern | Value | Evidence |
| --- | --- | --- |
| Success indicator | Root `rsp_cd` `"00000"` (JSON string) with `rsp_msg` "정상적으로 조회가 완료되었습니다." in every target TR example. `rsp_cd`/`rsp_msg` are **not** in the market-data or chart field tables. They appear in a field table only for `/websocket/session/clear` (`rsp_cd` "응답코드" String 100; example `"00000"` / "정상처리되었습니다"). | publisher example (L5), field table (L6) |
| Failure indicator + message fields | Not documented for REST TRs. Portal script (WebSocket subscribe ACK): `var code = h.rsp_cd \|\| j.rsp_cd \|\| "";` and `if (!code \|\| code === "00000") return null;`, i.e. a non-`00000` `rsp_cd` is a rejection, shown with `rsp_msg`. | publisher client code (L7 L1059–1064) |
| Is HTTP status meaningful? | REST TRs: not documented. OAuth TRs: L7 L1350–1351: "OAuth TR(발급·폐기)은 실패도 HTTP 200 으로 내려보내고 바디의 code 로만 알린다 (폐기 실패 = 200 {"code":403})." The portal tester treats any 2xx REST response as "OK" without reading `rsp_cd` (L1357–1359). | publisher client code (L7) |
| Throttle signal | **not found** (no HTTP status, code, message or `Retry-After` / `X-RateLimit-*` header documented). Response headers documented: `content-type`, `tr_cd`, `tr_cont`, `tr_cont_key` only. | field table (L5) |
| Token-expired / invalid-token signal | **not found** | — |
| Error-response body schema | Not documented for REST TRs. Revoke success: `{"code": 200, "message": "접근토큰 폐기에 성공하였습니다."}`. Revoke field table: `code` "응답코드" String 3, `message` String 100. So the OAuth envelope (`code`/`message`) differs from the TR envelope (`rsp_cd`/`rsp_msg`). | field table + publisher example (L4) |

### 4.4 Error catalog and mapping concerns

**No LS REST error catalog was found** (§4.1). The only codes or messages
seen are below; there is no count and no category list.

| Concern | Code(s) + message verbatim | Evidence |
| --- | --- | --- |
| Rate limit exceeded | not found | — |
| Token expired / invalid / revoked | not found. Revoke failure is described only as HTTP 200 + body `{"code":403}` (no message). | publisher client code (L7 L1350–1351) |
| Credential / app-key invalid | not found | — |
| Permission / entitlement / IP allow-list | not found | — |
| Invalid symbol | not found | — |
| Invalid parameter / malformed request | `IGW40011`, no message text: "게이트웨이는 바디 필드의 JSON 타입을 검증한다 — String이 아닌 필드에 문자열을 보내면 IGW40011이다. 빈 문자열도 타입 오류라 값이 비면 키째 뺀다(생략은 통과한다)." Also L1270: "빈칸을 그대로 보내면 문자열은 ""로, 숫자는 키가 빠진 채 나가 게이트웨이 오류로만 돌아온다." HTTP status not stated. | publisher client code (L7 L811–812, L1270) |
| Market closed / outside service hours | FAQ, for paper orders only: ""모의투자 주문처리가 안되었습니다. 재시도 바랍니다." 메시지" occurs "장 시작 전·점심 정산 시간·서버 점검 중에는". No code given. | publisher guide (L9) |
| Server busy / maintenance / internal error | not found (same FAQ row mentions "서버 점검 중") | publisher guide (L9) |
| "No data" returned as success? | **Yes**: t8411 example `"rsp_cd": "00000"`, `"rsp_msg": "해당자료가 없습니다."`, no OutBlock. | publisher example (L12) |

### 4.5 Publisher retry / back-off behaviour (recorded, not adopted)

- No publisher REST client, SDK or retry code exists for LS.
- FAQ (L9), on the paper-order message: "모의투자는 실거래 대비 체결 처리에
  지연이 있을 수 있으니, 응답 코드를 확인한 뒤 일정 간격을 두고 재시도하도록
  구현하세요." This is publisher advice for **orders**. It is recorded only.
  It conflicts with AGENTS.md (no automatic retry of orders or other
  non-idempotent operations without a proven duplicate-order safeguard) and
  is **not** evidence that a retry is safe.
- FAQ continuation example (L9) loops on `cts_date` with no delay and no
  status check.
- The portal tester disables its run button for 1,500 ms after each call
  (L7 L1375–1378). This is a UI cooldown, not a published limit.

### 4.6 Contradictions and gaps

1. **Token lifetime field:** table `expire_in` (String 10) vs example
   `expires_in` (JSON number 86400) (L3). Already recorded in
   live-auth-transport-gates.
2. **Revoke `code` type:** table String 3 vs example JSON number `200`
   (L4).
3. **OAuth failure on HTTP 200** comes only from a portal-script comment
   (L7). The field tables and examples do not show it.
4. **`rsp_cd` status:** a field only in the session/clear table (L6). Every
   TR example carries it, but no TR table lists it. Its presence and value
   set on errors are not documented.
5. **TPS values are mutable:** the 2023-10-25 and 2025-11-05 notices
   changed them, and their TR lists were not read. L1's value is a snapshot
   at version `20261026021444748`.
6. **WebSocket limits** come only from notices. The 2026-09-23 notice
   gives a final "구독제한 : 세션당 200개"; the 2026-10-16 notice applies
   sessions only, with subscription limits "향후 … 예정".
7. L1 gives `"transactionPerSec" : "1"` to four WEBSOCKET order-event
   entries (SC2, SC3, SC4, O01) and to REST `session/clear`. The meaning
   of a TPS on push events is not documented.
8. **Cross-broker overlap (Inference):** LS and DB share the `IGW40011`
   code family (L7; DB §5.4), an identical revoke example
   (`"code": 200`, "접근토큰 폐기에 성공하였습니다."), OAuth field names
   (`appsecretkey`, `token_type_hint`), and the message "모의투자 주문처리가
   안되었습니다" (LS FAQ; DB `M100`). This suggests a shared gateway
   product. DB's catalog must **not** be applied to LS without LS evidence.

### 4.7 Relation to KTradeLink error taxonomy (Inference only)

Code references: `main` @ `a5d2639e1b555b54c7a96652432cc2c3bf141fb7` (its `src/`
and `crates/` are identical to `f254ae87…`).

- `_https_transport.py` (blob `747138bc…`) L412–425 maps HTTP 401/403/429/5xx
  to the transport failure kinds behind `AuthenticationError`,
  `PermissionDenied`, `RateLimitExceeded` and `BrokerUnavailable`.
- The LS decoder requires `rsp_cd` `"00000"` (`lib.rs` blob `d4b6ad4f…`
  L361–364).

| LS signal | Candidate class | Evidence that would confirm |
| --- | --- | --- |
| HTTP 200 + `rsp_cd` ≠ `00000` | **Inference:** `BrokerRejected` (current) | A publisher REST error list or authorised paper capture |
| HTTP 200 + `rsp_cd` `00000` + no OutBlock ("해당자료가 없습니다.") | **Inference:** `ResponseSchemaError` for t1102 (missing `t1102OutBlock`); a typed empty result would need a contract decision | Publisher statement that `00000` + no block means "no data" for each TR |
| Over-TPS rejection | **Inference:** `RateLimitExceeded` only if LS uses HTTP 429. Unknown, so it may surface as `BrokerRejected`, `PermissionDenied` or `BrokerUnavailable`. | Documented over-limit code/status |
| Token invalid/expired | **Inference:** `AuthenticationError` if HTTP 401; otherwise unknown | Documented token-error code/status |
| OAuth HTTP 200 + body `code` ≠ 200 | **Inference:** token path must fail closed as `ResponseSchemaError`/`AuthenticationError`, never as success | Token-failure example in the field table |
| `IGW40011` | **Inference:** `InvalidParameter`-like, but it arrives as a broker response, so `BrokerRejected` today. `InvalidSymbol`/`InvalidParameter` are local validation classes. | Publisher code list with HTTP status |

### 4.8 Gates and not-verified items

- **Rate:** treat L1 `transactionPerSec` as a per-TR ceiling snapshot only.
  The scope key, window, paper limits and over-limit response are
  unverified. Any client pacing is our own policy, not a publisher
  contract.
- **No retry on an unknown LS rejection.** The FAQ's retry advice for paper
  orders is not adopted.
- **Token:** issuance rate limit, reissue/invalidation behaviour and the
  authoritative expiry field remain unverified. Token-failure bodies may
  arrive on HTTP 200.
- **Errors:** an LS REST error catalog, the HTTP status used for TR errors,
  and the meaning of a missing `rsp_cd` are not found. Keep the t1102
  decoder's required `rsp_cd` gate.
- **WebSocket:** session/subscription limits are from notices only. They
  are not used.

## 5. DB Securities

### 5.1 Pinned sources

GitHub sources are at
[`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb)
(`564b5100b80a3a785468b77ee8c0557f6edcfdeb`, committer date
2026-08-20T10:06:26+09:00). On 2026-11-05 this was still the upstream
default-branch HEAD. Blob SHAs are from that commit. Portal JSON/HTML on
`https://openapi.dbsec.co.kr` was retrieved 2026-11-05 07:48:21–07:51:01Z.
The portal's AI-service guide (DP8) and a 2026-07-31 notice (DP10) name
this repository as the official source for "오류코드·호출 한도(TPS)".

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| D1 | [`docs/errors_and_rate_limits.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/errors_and_rate_limits.md) | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L10–50 (403), L52–56 (200), L58–68 (400), L70–96 (500), L100–175 (service), L179–188 (WebSocket), L192–193, L197–222 | Error catalog; app 20 TPS; token 1 TPM; WebSocket limits |
| D2 | [`dbsec_sdk/response.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/response.py#L73-L85) | blob `6ce92fdc7fca3e34dda4c25b2797e153de29f7a5`; L24, L32, L73–85 | `is_ok` = HTTP 2xx; business success `rsp_cd == '00000'` even on HTTP 200 |
| D3 | [`dbsec_sdk/client.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/client.py#L62-L218) | blob `6000fa447765e6fc5822e6c8fe09ef92ead8d462`; L62–76, L156–218, L285–286 | **publisher client code**: `IGW00201` back-off retry; token auto-reissue; page cap. **Not adopted.** |
| D4 | [`dbsec_sdk/rate_limiter.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/rate_limiter.py#L1-L45) | blob `c51e3f06685375457b6dbc3d103dcd833f8b1d50`; L1–32, L44–45 | SDK pacing; publisher claim about the server's 1-second window |
| D5 | [`dbsec_sdk/auth.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/auth.py) | blob `b83addb2b8007ae12946eab1ae0395ceb3eca7de`; L20–21, L56–57, L95, L202–235, L271, L330–339 | Token 1-per-minute (`IGW00201`); same-token reissue; revoke-then-issue |
| D6 | [`docs/api_support_matrix.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/api_support_matrix.md) | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c`; L3–5, L17–18, L31, L53–59, L153–157 | Per-API TPS column, ⭕/❌ paper support |
| D7 | [`dbsec_sdk/apis/kr_stock_quote/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_quote/endpoints.py) | blob `5930af396f4a74ff04c7e780fcec87660399bec3`; "유량제어:" at L80 (JCODES), L170 (MULTIPRICE), L231 (PRICE), L282 (HOGA), L333 (CONCLUSION), L374 (DAYTRADE) | Docstring TPS |
| D8 | [`dbsec_sdk/apis/kr_chart/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_chart/endpoints.py) | blob `0b80a958e7c97e73bf2f4430b1550625fe3ab204`; L65 (tick), L120 (min), L174 (day) | Docstring "유량제어: 4 TPS" |
| D9 | [`dbsec_sdk/apis/kr_stock_order/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_order/endpoints.py#L95-L138) | blob `a6e13e46fafb3eedb801f023b6dcd73ecd708105`; L95, L138 | Order calls go through the same `client.post` → `request` loop |
| D10 | [`README.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/README.md#L712-L725) and [`docs/sdk_usage.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/sdk_usage.md#L131-L134) | blobs `377b5b9e0e3bcdfa54edad23507860798fa91143` (L712–725), `af4995d87434cc2b9bb7ca07cab55ddf56cf7878` (L131–134) | "자주 만나는 오류" summary; token 1/min |
| D11 | [`examples/dbsec_helper.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/dbsec_helper.py#L437-L521) | blob `a00db7a5a6104f7b4029c0b206231ff389b97f6b`; L440–453, L521, L619–635 | Helper paging `page_sleep` 0.5; status display reads `rsp_cd` or `code` |
| DP1 | https://openapi.dbsec.co.kr/api/apis/public/api-list/cc55b867-e049-421b-a798-be016370ff44 (OAuth 인증) | `eeb775c8ecd70a5f`, 07:50:17Z (same as gates copy); token `lastModifiedDate` 2026-02-25, revoke 2024-02-26 | Token description (rate, lifetime, reissue) |
| DP2 | `…/api/apis/public/api-list/80005fb0-6feb-4b8b-904a-605c59e29b4f` (국내주식시세) and `…/0bc09824-e8c2-491a-8c9d-b99e64b4b907` (국내주식/선물차트) | `f4f56996c26c33b3` (07:50:18Z), `f10207c4b22890cb` (07:50:19Z); both same as earlier ledgers | `extraParam` `ThroughputQuotaRule` / `CorpThroughputQuotaRule` `requestLimit`; `errorText` null on all 22 APIs |
| DP3 | `…/api/apis/guide/tr/<api_id>`: token `9e3097ab-7d39-4433-8002-00649604f0de`, revoke `3395b34c-f48c-436f-a5fa-dbae6b224af8`, PRICE `d7f6a691-8fe6-4733-901f-c2535417dc46`, CHARTMIN `f8581e1f-5621-4be6-a4e7-7cc8088d603f` | token `240e6462703d702a` (07:50:46Z), revoke `db1eb6b67b9b384a` (07:50:47Z), PRICE `6017533ab47fefef` (07:50:49Z), CHARTMIN `c34b20ae4c818bc1` (07:50:50Z) | `transactionPerSec`; examples with root `rsp_cd` |
| DP4 | `…/api/apis/guide/tr/property/<tr_id>`: revoke `59e897e8-a609-4305-b41d-6e3906ffca08`, PRICE `3be5fa4b-e576-4e5d-903b-7ff70d39d42b` | `b9616b35c22d8c74` (07:51:00Z), `a16222751d181c84` (07:51:01Z) | Revoke `code`/`msg` table; PRICE table has no `rsp_cd` |
| DP5 | https://openapi.dbsec.co.kr/apiservice | `9d67a597ce325d9f`, 07:48:21Z | Group ids; no error-code group in the menu |
| DP6 | https://openapi.dbsec.co.kr/howto-use | `04709494b0245f81`, 07:48:45Z | "신청일시로부터 24시간까지" |
| DP7 | https://openapi.dbsec.co.kr/about-openapi | `78fe31dfa1654c3f`, 07:48:52Z | "신청일로부터 익일 07시까지" |
| DP8 | https://openapi.dbsec.co.kr/aiservice-guide | `e9e378da1d03d078`, 07:48:58Z | Points to repo `docs/` for "오류코드·호출 한도(TPS)" and to `docs/api_support_matrix.md` for TPS |
| DP9 | FAQ via `https://openapi.dbsec.co.kr/api/forums/10000000-0000-0011-0000-000000000002/posts` (list `9b9027ff7672e390`, 07:49:27Z) and `/posts/<id>`: `109ff5ce-f155-4ad2-8692-b04804dab36f` "Open API 메세지 & 오류코드 안내 (26.6.15)", `8a596b8d-07e6-4a61-ae24-bcd04ac671e6` "Open API 호출 유량 안내 (Rest API, Websocket) - 2026.9.14 기준" | `de9c4e2427e20611` (07:49:44Z), `28372f51fffef86e` (07:49:45Z) | Official rate-limit statement; error-code spreadsheet attachment (not downloaded) |
| DP10 | Notices via `…/api/forums/10000000-0000-0011-0000-000000000001/posts` (list `0bbc3f096c1f8aef`, 07:49:28Z; 65 posts) and `/posts/<id>`: `1d422848-18e3-4f84-9f45-8f137342cff2` (2026-08-12), `405f1656-bba7-4cf1-aebb-ddcb32581848` (2024-09-25), `881ac1b4-b79a-4b6e-b5b2-4f82bb437dba` (2025-08-18), `e1517530-34e6-41a3-aeb5-3738f9608bc0` (2026-07-31) | `0d0b982c4822d9a4`, `449f869bf33d5f39`, `f553db3c628afffb`, `e8ce04c8c602c811`; 07:49:46–07:49:50Z | Temporary throttles; TPS history; GitHub endorsement |

Staff names, emails and sample tokens in DP1–DP10 were not copied.

**Missing evidence:**

- The portal's own error list is the FAQ attachment "DB증권 OpenAPI
  메세지코드_260615.xlsx" (DP9). It was **not downloaded**, so whether D1
  (2026-08-20) matches it is unverified.
- No `Retry-After` / `X-RateLimit-*` header and no HTTP 429 anywhere.
- No per-route statement of which error codes a quote or chart route can
  return.
- `rsp_cd` / `rsp_msg` are absent from every DP4 field table checked; the
  success value comes from examples and SDK prose.

### 5.2 Rate limits

| Concern | Value (verbatim) | Scope / unit | Real vs paper | Evidence |
| --- | --- | --- | --- | --- |
| Per-second request limit | FAQ: "앱(계좌)별 유량제어 : 20 TPS (1초당 20건)" (the "20" is split across HTML tags) and "※ 앱 유량제어 범위 내에서는 다른 API 즉시 호출에 대한 제한은 없습니다." D1 L210: "**앱(계좌)별** \| 20 TPS \| 초당 20건". | Per app; an app is issued per account ("앱(계좌)") | Paper apps are issued separately (DP6 "(모의투자 별도 발급)"); whether paper has its own limits is not documented | publisher guide (DP9), publisher repo note (D1) |
| Per-route limits | FAQ: "API 별 유량제어 : 각 API 별 확인 필요 (ex. 주식종합주문 10TPS, 주식 잔고조회 2TPS 등)". Target routes (DP2 `ThroughputQuotaRule` = `CorpThroughputQuotaRule` = DP3 `transactionPerSec` = D6 = D7/D8 docstrings): PRICE `5`, HOGA `3`, JCODES `3`, MULTIPRICE `2`, CONCLUSION `3`, DAYTRADE `3`, CHARTTICK/MIN/DAY/WEEK/MONTH `4`. | Per API per app | D6 ⭕ = "모의투자 + 실전투자 모두 호출 가능"; one TPS column for both | field table (DP2, DP3), publisher repo note (D6), publisher client code (D7, D8) |
| — distribution | D6: 166 methods; TPS `2` ×58, `3` ×13, `10` ×13, `1` ×10, `4` ×10, `5` ×7, `-` ×55 (real-time and OAuth). D7/D8/other docstrings (111 methods) match D6 for every numeric TPS. | — | — | publisher repo note (D6) |
| Token issuance limit | DP1: "※ API호출 유량은 1분에 1건 입니다." FAQ: "※ 접근토큰 발급 (/oauth2/token) 의 경우 1분에 1건 호출 가능 합니다." D1 L211: "**토큰 발급/폐기** \| 1 TPM \| 1분에 1건". D5 L56: "토큰 발급/폐기는 DB증권 정책상 1분 1건(IGW00201) 제한". | Per app (**Inference**) | — | field table (DP1), publisher guide (DP9), publisher client code (D5) |
| Token lifetime and reissue | DP1: "※ 접근토큰 유효기간 개인/법인 : 신청일시로부터 24시간" and "※ 유효기간 만료 전 토큰을 발급을 하는경우, 동일한 토큰이 발급됩니다. (만료기간도 동일) 유효기간 만료 전 새 토큰이 필요한 경우 접근토큰 폐기 후  발급 부탁드립니다." Example `"expires_in": 86400`. **But** DP7: "개인/법인 : 신청일로부터 익일 07시까지". Reissue does not invalidate; it returns the same token. | Seconds | — | field table + publisher example (DP1, DP3), publisher guide (DP6, DP7) |
| WebSocket limits (mention only) | FAQ: "앱(계좌)별 : 2 세션", "각 세션당 5 0종목 (2세션 전부 사용기준 100 종목 )", "웹소켓 연결: 6TPM", "한 IP당 웹소켓 각 포트별 40세션 연결 가능 (실전투자 - 40세션, 모의투자 - 40세션, 해외선물옵션 - 40세션)", "Connect 후, 10초 이내에 Send를 하지 않을 시 Connect가 해제 됩니다." D1 L218–222 agrees (adds "송수신 딜레이 100ms" as an SDK delay). | Per app / per IP | separate ports per environment | publisher guide (DP9), publisher repo note (D1) |
| Continuation / paging | No server page-rate rule. **Inference:** each page is one call against the API's TPS. SDK: 100-page safety cap `_PAGED_SAFETY_CAP = 100` (D3 L76); helper `page_sleep: float = 0.5` "0.5초 = 2 TPS 안전선. 1 TPS API 는 1.0 권장." (D11 L440–453). Chart `IGW40018` "datacnt 값이 최대 요청 가능한 건 수를 초과하였습니다." (D1 L96). | — | — | publisher client code (D3, D11), publisher repo note (D1) |

**Limits change at short notice (DP10):**

- 2026-08-12 notice: "공모주 상장일시: 2026년 8월 25일 (화) 08:00 ~ … 10:14
  (원상복구 완료)" (the planned "14:00 (총 6시간)" is struck through).
  "유량제어 내용: 앱별 유량제어 초당 1TPS 로 제한 (기존 20TPS)". "※ 주문 API
  (ex. 주식종합주문, 선옵종합주문 등) 는 유량제어가 적용되지 않습니다."
  Similar notices exist for 2024-06-11, 2024-11-18, 2025-01-13, 2025-07-10
  and "[긴급공지] 금융시장상황 급변 예상에 따른 일시 유량제어 안내
  [24.12.04]" (titles only).
- 2025-08-18: chart APIs "기존) 3TPS 변경) 4TPS". This matches the current
  `4`.
- 2024-09-25: PRICE "현재 : 5 TPS 변경 : 1 TPS (멀티 현재가조회 API 오픈 후
  2주 뒤 반영 예정)", and MULTIPRICE "API 유량: 1TPS". Current sources say
  PRICE `5` and MULTIPRICE `2` (§5.6 #5).

### 5.3 Status envelope and HTTP status use

| Concern | Value | Evidence |
| --- | --- | --- |
| Success indicator | Root `rsp_cd` `"00000"` (string). Examples: PRICE and CHARTMIN `"rsp_cd": "00000"`, `"rsp_msg": "정상 처리 되었습니다."` (DP3). D1 L56 lists `00000` "거래를 성공하였습니다." under "HTTP 200 (OK)". D1 L106–109 list four more `00000` messages. D2 L82–83: "is_ok 는 HTTP 2xx 만 보므로, 업무 성공은 rsp_cd == '00000' 으로 확인한다 (서버가 HTTP 200 과 함께 업무오류코드 M100/IGW… 를 내려주는 경우가 있음)." **So success requires `rsp_cd` `"00000"` even on HTTP 200.** `rsp_cd` is not in the PRICE field table (DP4). | publisher example (DP3), publisher repo note (D1), publisher client code (D2) |
| Failure indicator + message fields | `rsp_cd` (code) + `rsp_msg` (message). D1 L192–193: "같은 응답코드가 상황에 따라 여러 메시지로 재사용될 수 있습니다(예: `3139`, `3735`, `M100`). 오류 원인 판단은 항상 서버가 함께 내려주는 `rsp_msg` 원문을 기준으로 하세요." D2 L55 falls back to `msg`. | publisher repo note (D1), publisher client code (D2) |
| Is HTTP status meaningful? | Partly. D1 groups platform codes by HTTP 403 / 200 / 400 / 500. D3 L65–67: "HTTP 상태는 403(토큰발급계열)·500(그 외) 둘 다로 오며, 500 에는 진짜 서버오류(IGW50xxx)도 섞이므로, 상태코드가 아니라 반드시 이 rsp_cd 로만 트리거한다." Client errors (`IGW40012`, `IGW40017`, `IGW40018`) are listed under 500. Server errors (`IGW00001`, `IGW00002`) are listed under 403. Service codes (D1 §2) have **no** HTTP status. | publisher repo note (D1), publisher client code (D3) |
| Throttle signal | `IGW00201` "호출 거래건수를 초과하였습니다." under **HTTP 403** (D1 L48) **and HTTP 500** (D1 L74). D1 L199: "초과 시 `IGW00201`(호출 거래건수 초과)이 반환됩니다." D5 says token over-limit also returns `IGW00201`. No HTTP 429; no `Retry-After` / `X-RateLimit-*`. D4 L20–22 (publisher claim): "서버는 자체 1초 카운팅 윈도로 집계" and "실측에서 동시 12콜 중 2콜이 이렇게 누수됐다." | publisher repo note (D1), publisher client code (D3–D5) |
| Token-expired / invalid-token signal | `IGW00121` "유효하지 않은 token 입니다." and `IGW00123` "기간이 만료된 token 입니다." (403 L37/L39 and 400 L62/L63); `IGW00122` "token을 찾을 수 없습니다." (403 L38); `IGW00205` "credentials_type이 유효하지 않습니다.(Bearer)" (400 L66). The SDK treats `{"IGW00121", "IGW00122", "IGW00123"}` as token errors (D3 L63). | publisher repo note (D1), publisher client code (D3) |
| Error-response body schema | Same root keys `rsp_cd`/`rsp_msg` as success (D1 tables, D3 L178 reads `rsp_cd` from the error body). No error example JSON was published. OAuth revoke uses `{"code": 200, "message": …}` (DP3), but the field table says `code` "응답코드" A0001 length 8 and `msg` "응답메세지" (DP4). D11 L621 reads "`rsp_cd` or `code`". | publisher example (DP3), field table (DP4), publisher client code (D3, D11) |

### 5.4 Error catalog and mapping concerns

**Catalog:** D1. The portal endorses `docs/` for error codes (DP8) and has
its own spreadsheet (DP9, not read). Size:

- §1 platform codes: 68 rows (403 ×37, 200 ×1, 400 ×7, 500 ×23); 62
  distinct `IGW` codes plus `00000`.
- §2 service codes: 70 rows, 50 distinct codes including `00000`.
- §3 WebSocket: 6 rows.

Categories: OAuth/credential/content-type (`IGW001xx`), rate (`IGW00201`),
permission/IP (`IGW40342`, `IGW00303`), request validation (`IGW400xx`),
gateway/MCI internals and timeouts (`IGW500xx`), order/account business
codes (4-digit), paper-system codes (`M001`, `M100`, `M205`, `M216`),
WebSocket (`100xx`).

Duplicates: `IGW00121`, `IGW00123`, `IGW00133` and `IGW00201` each appear
under two HTTP statuses. `IGW00132` has two meanings: 403 "Content-Type이
유효하지 않습니다." (L29) and 400 "MAC주소(mac_address)는 필수입니다." (L64).
`M100` carries 12 messages, `3139` five and `3735` two.

| Concern | Code(s) + message verbatim | Evidence |
| --- | --- | --- |
| Rate limit exceeded | `IGW00201` "호출 거래건수를 초과하였습니다." (403 L48; 500 L74) | D1 |
| Token expired / invalid / revoked | `IGW00121` "유효하지 않은 token 입니다."; `IGW00122` "token을 찾을 수 없습니다."; `IGW00123` "기간이 만료된 token 입니다."; `IGW00205` "credentials_type이 유효하지 않습니다.(Bearer)" | D1 L37–39, L62–63, L66 |
| Credential / app-key invalid | `IGW00102` "AppKey는 필수입니다."; `IGW00103` "유효하지 않은 AppKey입니다."; `IGW00104` "AppSecret은 필수입니다."; `IGW00105` "유효하지 않은 AppSecret입니다."; `IGW00133` "Content-Type이 유효하지 않습니다." (D5 L271: "JSON 으로 보내면 IGW00133") | D1 L17–20, L47, L65; D5 |
| Permission / entitlement / IP allow-list | `IGW40342` "API 사용 권한이 없습니다."; `IGW00303` "법인고객에게 허용되지 않은 IP접근입니다."; `M100` "모의투자에서는 해당업무가 제공되지 않습니다."; `IGW00132` "MAC주소(mac_address)는 필수입니다." (400) | D1 L49–50, L64, L162 |
| Invalid symbol | `1887` "상장 종목번호를 확인하여 입력하십시오."; `3053` "해당 종목번호가 없습니다."; `IGW40011` "단축코드(shcode) 길이 확인이 필요합니다. & 단축코드(shcode) data type을 확인하세요." (400). DB quote fields are named `InputIscd1`, not `shcode`. | D1 L68, L114, L131 |
| Invalid parameter / malformed request | `IGW00101` "유효하지 않은 요청입니다." (403); `IGW40010` "연속구분 (cont)은 필수입니다." (400); `IGW40012` "요청데이터(json) 형식 오류 입니다." (500); `IGW40017` "datacnt 값과 요청 데이터 개수가 일치하지 않습니다." (500); `IGW40018` (500, §5.2); `IGW50002` "요청전문 유효성 체크 중 오류가 발생하였습니다." (500); `2028` "시작일이 종료일보다 큽니다." | D1 L16, L67, L76, L93, L95–96, L115 |
| Market closed / outside service hours | `2218` "온라인 중에만 가능합니다."; `2611` "장시작 전 또는 장마감 되었습니다."; `M100` "모의투자 장시작전 입니다." (`3589`/`3590` are order-only) | D1 L117, L120, L168 |
| Server busy / maintenance / internal error | `IGW00001` "일시적 오류가 발생했습니다." and `IGW00002` "서버 에러가 발생했습니다." (both **403**); `IGW50001`–`IGW50018` (500), incl. `IGW50005` "MCI 통신 중 오류가 발생하였습니다.", `IGW50011` "Connection 타임아웃 오류입니다.", `IGW50012` "Socket 타임아웃이 발생했습니다."; `IGW40013` "데이터 조회에 실패 했습니다."; `3665` "해당 서비스 일시정지중입니다."; `8000` "처리중 오류가 발생했습니다. (DB)"; `8001`; `M001` "서비스가 지연처리되고 있습니다. 잠시후 사용하시기 바랍니다."; `M205` / `M216` "서비스 지연중입니다. 처리결과 확인후 사용하시기 바랍니다." (TPENOENT / TPECLOSE) | D1 L14–15, L75–94, L149, L153–154, L161, L174–175 |
| "No data" returned as success? | **Both ways.** `00000` "모의투자 데이터가 없습니다." (success code, L108) **and** `2679` "조회내역이 없습니다" (non-success code, L121). Which routes use which is not documented. | D1 |

`M205`/`M216` ("처리결과 확인후"), `IGW50011`/`IGW50012` (timeouts) and
`IGW50005` (back-end communication) are outcome-UNKNOWN signals in the
AGENTS.md sense. **Inference:** the broker may have processed the request.

### 5.5 Publisher retry / back-off behaviour (recorded, not adopted)

These items are recorded as publisher behaviour only. None of them is
evidence that a retry is safe.

- **Proactive pacing** (D4 L7–31, D1 L201–204): the SDK paces each call at
  a minimum interval. It applies app `APP_TPS = 20` plus the per-endpoint
  TPS from D6 (`DEFAULT_TPS = 1` if missing), with `rate_limit_safety` 0.9.
- **Reactive `IGW00201` back-off** (D3 L68–71, L192–209), on by default:
  - Up to `_BACKOFF_RETRIES = 4` resends.
  - Delays of 1, 2, 4, 8 s (`_BACKOFF_MAX = 8.0`) plus 0–25 % jitter:
    "1+2+4+8 ≈ 최악 15s+jitter".
  - The trigger is the body `rsp_cd`, not the HTTP status (L65–67).
  - The loop is path-agnostic. Order methods call the same `client.post` →
    `request` loop (D9 L138; D3 L285–286). **The SDK therefore also
    resends orders on `IGW00201`.**
  - Whether an `IGW00201` order was rejected before any processing is
    **not documented**. Per AGENTS.md this is not adoptable. The 2026-08-12
    notice says the temporary throttle does not apply to order APIs.
- **Token auto-reissue** (D3 L62–63, L180–190; D5 L202–235): on `IGW00121`,
  `IGW00122` or `IGW00123` the SDK revokes, re-issues (up to
  `token_retry_limit` 5) and resends the **same request**, including orders.
  Revoke-then-issue is needed because "24시간 이내 재발급 시 서버가 기존
  토큰을 반환" (D5 L20–21). The token endpoint allows one call per minute.
- **2xx short-circuit** (D3 L174–176): the SDK returns any HTTP 2xx as-is
  without checking `rsp_cd`. Callers must check `rsp_cd` themselves (D2
  L82–83). D2 L85 returns `""` when `rsp_cd` is missing.
- **Paging:** 100-page cap (D3 L76, L277); helper `time.sleep(page_sleep)`
  0.5 s (D11 L521).

### 5.6 Contradictions and gaps

1. **HTTP 200 with an error code:** D2 L82–83 says HTTP 200 can carry
   `M100`/`IGW…`. D1 lists only `00000` under HTTP 200 and puts every `IGW`
   code under 403/400/500.
2. **Throttle status:** `IGW00201` appears under both 403 and 500 (D1).
   D3 says 403 is the "토큰발급계열". The HTTP status alone cannot
   classify a DB error (§5.3).
3. **`IGW00132`** has two meanings (D1 L29 vs L64).
4. **Token/revoke limit:** DP1 and DP9 give 1 per minute for **issuance**.
   D1 L211 and D5 L56 extend it to "발급/폐기". The SDK's revoke-then-issue
   on token errors therefore uses two rate-limited calls.
5. **PRICE / MULTIPRICE TPS:** the 2024-09-25 notice announced PRICE
   5 → 1 and MULTIPRICE 1. The current DP2 (PRICE `lastModifiedDate`
   2024-06-05; MULTIPRICE 2026-03-13), DP3, D6 and D7 say PRICE `5` and
   MULTIPRICE `2`. Whether the PRICE change was applied, reverted or
   cancelled is not documented. **Inference:** the current portal values
   govern, unverified.
6. **Token lifetime:** "신청일시로부터 24시간" (DP1, DP6; example 86400) vs
   "신청일로부터 익일 07시까지" (DP7).
7. **No data:** `00000` "모의투자 데이터가 없습니다." vs `2679` "조회내역이
   없습니다" (D1).
8. **Revoke envelope:** table `code` (A0001, length 8) / `msg`; example
   JSON number `200` / `message` (DP3, DP4).
9. **howto-use token snippet** (DP6): `"content-type":"application/json"`,
   `data=json.dumps(body)` and body key `appsecret`. The SDK uses a form
   body and says JSON yields `IGW00133` (D5 L271). The DP4 revoke table
   uses `appsecretkey`.
10. **FAQ dating:** "… - 2026.9.14 기준" in the title vs `createdDate`
    2024-08-08 (DP9). The post was edited, but no modification date is
    exposed.
11. **Cross-broker:** see §4.6 #8. The `IGW40011` message names
    `shcode`, a field DB quote routes do not use.

### 5.7 Relation to KTradeLink error taxonomy (Inference only)

**Current behaviour** (`main` @ `a5d2639e…`; same `src/` and `crates/` as
`f254ae87…`):

- Transport: `_https_transport.py` L412–425 classifies by HTTP status only
  (401/403/429/5xx). `errors.py` (blob `fea32222…`) L113–144 documents
  `AuthenticationError`=401, `PermissionDenied`=403,
  `RateLimitExceeded`=429, `BrokerUnavailable`=5xx,
  `BrokerRejected`=200 + non-success status.
- **Open gate:** the DB decoder uses
  `status(root, "rsp_cd", StatusSpec::ExactText("00000"))` (`lib.rs` blob
  `d4b6ad4f…` L374). `status()` returns `Ok(())` when the key is absent
  (L224). Sources supporting a *required* root `rsp_cd` `"00000"`:
  - every DB guide example (PRICE, CHARTMIN, CONCLUSION, DAYTRADE) carries
    it (DP3);
  - D2 L82–83 says business success is `rsp_cd == '00000'` even on HTTP
    200;
  - D1 L56/L106–109 define `00000` as the only success code.
  
  No source says a successful quote may omit it.

| DB signal | Candidate class | Evidence that would confirm |
| --- | --- | --- |
| `IGW00201` (HTTP 403 or 500) | **Inference:** semantically `RateLimitExceeded`. Today it surfaces as `PermissionDenied` (403) or `BrokerUnavailable` (500). Code-based mapping would need `rsp_cd` from the error body (`_diagnostics.gateway_status` already reads `rsp_cd`). Never retried. | Authorised paper capture of the over-limit status/body |
| `IGW00121`/`IGW00122`/`IGW00123`/`IGW00205` | **Inference:** `AuthenticationError`. Today they are `PermissionDenied` (403) or a generic HTTP failure (400). | Same |
| `IGW00102`–`IGW00105`, `IGW00133` (token path) | **Inference:** `AuthenticationError` (credential) | Same |
| `IGW40342`, `IGW00303`, `M100` "모의투자에서는 해당업무가 제공되지 않습니다." | **Inference:** `PermissionDenied` | Same; `M100` would need message matching (D1 L192–193) |
| `1887`, `3053`, `IGW40011` | **Inference:** broker-side "no such instrument" → `BrokerRejected`. `InvalidSymbol` is a local six-digit validation class (errors.py L89–90) and should not be reused without a decision. | Route-specific code list |
| `IGW40010`/`IGW40012`/`IGW40017`/`IGW40018`/`IGW50002`/`2028` | **Inference:** `BrokerRejected` (request rejected). Some arrive as HTTP 500 → `BrokerUnavailable` today, which is misleading. | Same |
| `IGW500xx`, `IGW00001`/`IGW00002`, `IGW40013`, `3665`, `8000`/`8001`, `M001`, `M205`/`M216` | **Inference:** `BrokerUnavailable` with delivery UNKNOWN where the code implies a timeout or "처리결과 확인" | Same |
| HTTP 200 + `rsp_cd` ≠ `00000` (incl. `2679`, `2611`, `2218`) | **Inference:** `BrokerRejected` (current) | — |
| HTTP 200 + `rsp_cd` missing | **Inference:** must become `ResponseSchemaError` (missing required status), closing the open gate | DB decoder change + test |
| HTTP 200 + `00000` + empty `Out` ("모의투자 데이터가 없습니다.") | **Inference:** `ResponseSchemaError` for a single-quote route; needs a contract decision for list routes | — |

### 5.8 Gates and not-verified items

- **Decoder gate (open):** make the DB root `rsp_cd` required with exact
  value `"00000"` (as LS t1102 already does), and add a regression test for
  a body without `rsp_cd`.
- **Rate:** app 20 TPS plus per-API TPS are publisher statements that can
  change at short notice (temporary 1 TPS app-wide on IPO days). They are
  not verified by any call. Any pacing is our policy. A hard-coded table
  must carry its source pin.
- **No automatic retry** of `IGW00201`, token errors, timeouts or 5xx. This
  applies to orders above all. The SDK back-off and token-reissue loops
  (§5.5) are not adopted.
- **Error classification:** the HTTP status is not a reliable class for DB
  (§5.3, §5.6 #1–2). Mapping by `rsp_cd` needs an authorised paper capture
  and a maintainer decision. `M100`/`3139`/`3735` need `rsp_msg` to
  disambiguate.
- **Token:** the 1/min issuance limit and same-token reissue are documented.
  The revoke limit, the lifetime (24 h vs "익일 07시") and the over-limit
  token response remain unverified.
- Not read: the DP9 spreadsheet; notice bodies other than the four in DP10.

## 6. Toss Securities

### 6.1 Pinned sources

Public Toss portal documents, retrieved 2026-11-05 07:43:44–07:43:45 UTC.
Nothing was sent to any Toss API: no token, quote or account request. All
four files have the same sha256 as the copies pinned in the trade evidence
(07:10 UTC) and in the transport-gates recheck, so the spec has not changed
since `info.version 1.2.28` was first pinned. T1 is a pretty-printed JSON
file (13,525 lines), so line numbers are given for that copy. T3
(AsyncAPI) is not used here; the ID is kept free so the numbering matches
the trade evidence.

T5 L16 calls T1 the "source of truth for endpoints, schemas, … errors, and
rate limits". T4 L3 defers to the API document. However, the numeric
per-group limits appear **only** in T2 (see §6.6 #5). Evidence levels:
`field table` for T1; `publisher guide` for T2, T4 and T5.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | 07:43:44Z, sha256 `c5918961335ccd6b…`, `openapi 3.1.0`, `info.version 1.2.28`, 534,361 bytes | L85–210 `/oauth2/token` (description L91; 400/401/403/429); L336ff `/api/v1/prices`; `components.responses` `Unauthorized` L8884 (`token-revoked` L8926), `Forbidden` L8945, `NotFound` L8962, `RateLimitExceeded` L8979–9025, `ServiceUnavailable` L9026, `InternalErrorMarketData` L9077; `components.schemas` `ErrorResponse` L9315, `ApiError` L9327, `OAuth2ErrorResponse` L9435; `components.headers` `XRequestId`/`WWWAuthenticate`; `maintenance` example L6969–6977 |
| T2 | [overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md) | 07:43:45Z, sha256 `bef057d9babe9a38…` | L210 allow-listed IP onboarding; L234–282 rate limits, headers and 429 advice; L286–363 error envelope and error table; L444–452, L465–488 WebSocket limits and errors (mentioned only) |
| T4 | [faq.md](https://openapi.tossinvest.com/openapi-docs/faq.md) | 07:43:45Z, sha256 `6ad4c02b8e785f7d…` | L9 (one token per client), L10–12 (401/`invalid_client`/403), L14 (rate headers), L15 (`403 edge-blocked` on token), L16 (`requestId`), L51 (`ORDER` group) |
| T5 | [developers.tossinvest.com/llms.txt](https://developers.tossinvest.com/llms.txt) | 07:43:45Z, sha256 `bbff77eaa55df248…` | L14–17 (source-of-truth ranking) |

**Missing evidence:**

- `https://openapi.tossinvest.com/openapi-docs/llms.txt` returned HTTP 404
  at 07:43:46Z. The `llms.txt` used here is the `developers.tossinvest.com`
  copy (T5).
- No paper/sandbox origin: T1 `servers` has only
  `https://openapi.tossinvest.com`.
- No publisher client code or SDK was found that shows retry or
  token-handling behaviour.
- No documented limit on how often a token may be issued, other than the
  `AUTH` group rate (§6.2).

### 6.2 Rate limits

| Concern | Value (verbatim) | Scope / unit | Real vs paper | Evidence |
| --- | --- | --- | --- | --- |
| Per-second / per-minute request limit | T2 L236: "모든 API 는 **클라이언트 × API 그룹** 단위로 초당 요청 수(TPS)가 제한됩니다." Each operation's description ends with "**Rate Limits Group**: `…`" (T1). T2 L238/L264: "운영 상황에 따라 사전 공지 없이 조정될 수 있으며, 현재 허용 한도는 응답 헤더 `X-RateLimit-Limit` 으로 확인할 수 있습니다." T2 L265: "비정상 사용이 의심되는 일부 IP 대역에서는 요청 한도를 초당 최대 1회로 제한합니다." | Per client (`client_id`) × group; per second; token bucket (T1 `X-RateLimit-Remaining` "현재 버킷에 남은 토큰 수") | Real only | publisher guide (numbers) + field table (group names) |
| Per-route (group) limits | `MARKET_DATA` "초당 최대 15회" covers `/api/v1/prices`, `/orderbook`, `/trades`, `/price-limits`. `MARKET_DATA_CHART` "초당 최대 20회" covers `/candles`. Others: `AUTH` 5, `ACCOUNT` 1, `ASSET` 5, `TRANSACTION` 5, `STOCK` 5, `STOCK_ALL` 1, `STOCK_TRADING_TREND` 10, `MARKET_INFO` 3, `RANKING` 5, `MARKET_INDICATOR_PRICE` 10, `MARKET_INDICATOR` 10, `MARKET_INDICATOR_CHART` 5, `SECTOR` 5, `SECTOR_RANKING` 5, `ORDER` 10 (peak "09:00 ~ 09:10 KST: **초당 최대 10회**"), `ORDER_HISTORY` 5, `ORDER_INFO` 6 (peak 3), `CONDITIONAL_ORDER` 5, `CONDITIONAL_ORDER_HISTORY` 10 (T2 L240–262). T1 Market Data tag: "두 그룹의 한도 응답 헤더를 각각 확인하는 것을 권장합니다." `/api/v1/prices` accepts up to 200 symbols per call ("최대 200건 까지 다건 조회", T1). | per client × group | Real only | publisher guide + field table |
| Token issuance limit / interval | No separate issuance interval is documented. `/oauth2/token` belongs to "**Rate Limits Group**: `AUTH`" (T1 L91) = "초당 최대 5회" (T2). | per client × `AUTH` group | Real only | field table + publisher guide; interval **not found** |
| Token lifetime and reissue behaviour | T1 L91: "refresh token 은 제공되지 않습니다. 만료 시 동일 엔드포인트로 재발급합니다." and "client 당 유효한 access token 은 1 개입니다. 재발급 시 이전에 발급된 token 은 즉시 무효화됩니다." `expires_in` "토큰 만료까지 남은 초." (`integer`/`int64`; example `86400`). T4 L9: "새로 발급하면 직전 토큰은 즉시 무효화되어 `401 token-revoked` 로 거부됩니다. … 프로세스마다 토큰을 따로 발급하면 서로를 무효화합니다." | per client | Real only | field table + publisher guide |
| WebSocket limits (mention only) | T2 L446–450: "동시 연결 \| **계정당 2개**" (the oldest connection is closed), "연결당 구독 수 \| **100건**", "선언(요청) 빈도 \| **5회/초**" → `rate-limit-exceeded`. T2 L452: "REST 와 달리 `Retry-After` 헤더는 제공되지 않습니다". | per account / connection | — | publisher guide |
| Continuation/paging limits relevant to throttling | No cursor on `prices`/`trades`. `candles` returns up to 200 bars per call (T1). Each call counts once against its group. **Inference:** batching ≤200 symbols per `prices` call is the main lever against `MARKET_DATA` 15/s. | — | — | field table; batching effect is Inference |

### 6.3 Status envelope and HTTP status use

| Concern | Value | Evidence |
| --- | --- | --- |
| Success indicator | HTTP 200 + `ApiResponse` with required `result`: "`result` 와 `error` 는 동시에 나타나지 않습니다." There is no success code field. `/oauth2/token` 200 is the OAuth2 standard body instead ("BFF 공통 envelope 이 아닌 OAuth2 표준 형식"). | T1 `ApiResponse`, L91 |
| Failure indicator + message fields | `ErrorResponse` `{error: ApiError}` "4xx/5xx 응답에 사용됩니다". `ApiError` requires `requestId`, `code`, `message`; `data` (hint object) is optional. `code`: "클라이언트는 unknown code 를 허용하도록 구현해야 합니다." `message`: "내부 정책상 노출이 제한되는 경우 빈 문자열로 내려갈 수 있으므로 클라이언트는 `code` 기반으로 메시지를 자체 매핑할 것을 권장합니다." Token endpoint uses `OAuth2ErrorResponse` `{error, error_description?, error_uri?}`: "클라이언트는 `code` 가 아닌 `error` 필드로 에러를 식별해야 합니다." | T1 L9315, L9327, L9435 |
| Is HTTP status meaningful? | Yes. 400/401/403/404/409/422/429/500 are used per route (T1). T2 L309–363 maps each code to a status. No "200 with error body" pattern is documented. | field table + publisher guide |
| Throttle signal | HTTP **429**, `error.code` `rate-limit-exceeded`, message "요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요." (T1 `RateLimitExceeded`). T2 L360 also lists 429 `edge-rate-limit-exceeded`. Headers (T1 L8982–9010): `X-RateLimit-Limit` "현재 허용된 초당 요청 수 (burst capacity)" (example `10`); `X-RateLimit-Remaining` "429 시 0."; `X-RateLimit-Reset` "토큰 1 개가 재충전될 때까지 예상 초"; `Retry-After` "재시도 권장 초" (integer). T2 L269: "정상 응답과 429 응답 모두에 다음 헤더가 포함됩니다"; T2 L276: `Retry-After` "429 응답에만 포함". | field table + publisher guide |
| Token-expired / invalid-token signal | HTTP 401 + `WWW-Authenticate: Bearer realm="openapi", error="invalid_token", …`. Codes: `invalid-token`, `expired-token`, `token-revoked`, `login-user-not-found` (T1 `Unauthorized`). T2 L319 adds 401 `edge-blocked` "`Authorization` 헤더가 전달되지 않았습니다." Token endpoint: 401 `invalid_client` "Client authentication failed." with `WWW-Authenticate: Basic realm="openapi"`. | field table + publisher guide |
| Error-response body schema | JSON. It is a **different** envelope from success (`error` vs `result`). `requestId` equals the `X-Request-Id` header. T2 L304: "일부 응답에서 requestId 가 누락된 경우, 응답 헤더의 `referenceId` 또는 `x-amz-cf-id` 값을 첨부해주세요." So `requestId` can be missing even though T1 marks it required. | field table + publisher guide |

### 6.4 Error catalog and mapping concerns

Catalog locations:

- **T2 L309–363:** one table with 53 rows and 49 distinct codes, covering
  HTTP 400/401/403/404/409/414/415/422/429/500.
- **T1:** has no catalog. Codes appear only as response examples. 44
  distinct `ApiError.code` values are used there, plus 4 OAuth2 `error`
  values (`invalid_request`, `invalid_client`, `unsupported_grant_type`,
  `access_denied`). The `OAuth2ErrorResponse.error` enum has 6 values
  (adding `invalid_grant` and `unauthorized_client`).

Categories: authentication (401), edge/IP/permission (403), not-found
(404), order-state conflicts (409), order business rules (422), throttle
(429), server/maintenance (500).

The two catalogs do not match exactly:

- In T2 only: `edge-blocked`, `ip-not-allowed`,
  `edge-rate-limit-exceeded`, `unsupported-content-type`,
  `insufficient-sellable-quantity`, `order-limit-exceeded`,
  `duplicate-conditional-order`, `condition-already-met`.
- In T1 only: `fractional-quantity-outside-regular-hours`,
  `unsupported-date`, `us-modify-quantity-not-supported`.

| Concern | Code(s) + message verbatim | Evidence |
| --- | --- | --- |
| Rate limit exceeded | 429 `rate-limit-exceeded` "요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요." (T1). 429 `edge-rate-limit-exceeded` "Rate limit 초당 요청 수를 초과했습니다." (T2 L360; not in T1). | field table + publisher guide |
| Token expired / invalid / revoked | 401 `expired-token` "토큰이 만료되었습니다."; `invalid-token` "유효하지 않은 토큰입니다."; `token-revoked` "새로 발급된 토큰으로 대체되어 더 이상 유효하지 않은 토큰입니다. 최신 토큰으로 다시 시도해 주세요."; `login-user-not-found` "로그인 정보를 찾을 수 없습니다." (T1 L8884–8944) | field table |
| Credential / app-key invalid | Token endpoint 401 `invalid_client` "Client authentication failed." ("`client_id` / `client_secret` 가 잘못되었거나 클라이언트가 비활성 상태인 경우"). 400 `invalid_request` "OAuth 2.0 Parameter: {name}" or "Malformed client authentication: …" (T1 L85–210). T4 L15: token request "`403 edge-blocked`" = "서버 앞단에서 허용되지 않은 형식의 요청을 차단한 것입니다." | field table + publisher guide |
| Permission / entitlement / IP allow-list | Token endpoint 403 `access_denied` "IP address not allowed" — "클라이언트에 등록된 허용 IP 목록에 없는 IP 에서 호출한 경우 차단됩니다." (T1 L196–204). Other APIs: T2 L324 403 `ip-not-allowed` "허용되지 않은 IP 주소입니다." (not in T1). T2 L325 / T1 `Forbidden` 403 `forbidden` "요청에 필요한 권한이 부족합니다." T2 L323 403 `edge-blocked` "허용되지 않은 요청입니다." | field table + publisher guide |
| Invalid symbol / no such instrument | 404 `stock-not-found` "종목을 찾을 수 없습니다." (T1 `NotFound`, used by `/api/v1/prices`). 400 `unsupported-market` / `unsupported-symbol` on other groups. | field table |
| Invalid parameter / malformed request | 400 `invalid-request`. `/api/v1/prices` example: "요청이 올바르지 않습니다." with `data` `{"field":"symbols","constraint":{"min":1,"max":200}}` (T1). T2 L341: 415 `unsupported-content-type`; T2 L340: 414 `edge-blocked`. | field table + publisher guide |
| Market closed / outside service hours | Market data: **not found**. Order-only codes: 422 `order-hours-closed` "현재 해당 주문을 접수할 수 없는 시간입니다." | field table |
| Server busy / maintenance / internal error | 500 `internal-error` "처리 중 문제가 생겼어요. 잠시 후 다시 시도해주세요." (T1 `InternalErrorMarketData`, "시세 조회 중 일시적 오류"). 500 `maintenance` "점검 중입니다. 잠시 후 다시 시도해 주세요." with `data.retryAfterSeconds` `600`, shown only on an order route (T1 L6969–6977); T2 L363 lists it generally. `ServiceUnavailable` ("서비스 일시 불가") is referenced only as the **500** of `/api/v1/accounts` (T1 L5056); no REST 503 is documented. | field table + publisher guide |
| "No data" returned as success? | Not documented for `prices`. A missing symbol is a 404 (above). How a batch with one unknown symbol is handled is **not documented**. | not found |

### 6.5 Publisher retry / back-off behaviour (recorded, not adopted)

These items record what the publisher recommends. None of them is evidence
that a retry is safe.

- **429 advice (T2 L278–282):**
  - "429 수신 시 `Retry-After` 헤더 값만큼 대기 후 재시도합니다."
  - "지수 백오프(1s → 2s → 4s ...) 와 jitter 를 함께 적용합니다."
  - "`X-RateLimit-Remaining` 이 낮아질 때 클라이언트 측에서 요청 속도를
    선제적으로 완화할 수 있습니다."
- **`retryAfterAt` / `retryAfterSeconds` (`ApiError.data`, T1 L9356):**
  hint keys. Examples show them on `maintenance` (600) and on order 409
  `already-processing` (1, L7414/L7638).
- **"잠시 후 다시 시도해 주세요":** this wording appears in the 429,
  `internal-error`, `maintenance` and order-conflict messages. It is
  user-facing text, not a contract.
- **Token reissue:** the 401 `token-revoked` message says "최신 토큰으로
  다시 시도해 주세요". T4 L10 says to make "모든 프로세스가 그 토큰만
  쓰도록 맞춰 주세요". Reissuing invalidates every other holder (§6.2).
  **Inference:** an automatic reissue on 401 in one process would break
  every other process sharing the client.
- **No publisher retry code.** The FAQ does not exempt order routes from
  this advice. KTradeLink policy (AGENTS.md) still forbids automatic retry
  of non-idempotent operations, whatever the publisher advice says.

### 6.6 Contradictions and gaps

1. **What 403 means on non-token routes.**
   - T2 L210: "등록된 허용 IP 목록에 없는 IP 에서의 호출은 403 으로
     차단됩니다". T2 L324 gives the code `ip-not-allowed`.
   - T1's shared `Forbidden` response (L8945) shows only `forbidden`
     "권한 부족". `ip-not-allowed` appears nowhere in T1.
   - The Market Data routes, including `/api/v1/prices`, list **no 403**
     (and no 401) in T1, only 200/400/404/429/500.
   - So "403 = IP not allow-listed" is documented as a T1 contract only
     for `/oauth2/token` (`access_denied`, OAuth2 envelope). For
     `/api/v1/prices` it is publisher-guide prose only.
2. **401 is undeclared on Market Data routes.** Every route requires the
   bearer token (T1 `security`), but T1 declares 401 only on Stock Info,
   Account, Asset, Order and Transaction routes. **Inference:**
   `/api/v1/prices` can also return 401 `expired-token` / `token-revoked`.
   Read it from the response, not from T1.
3. **Rate headers on success.** T1 attaches `X-RateLimit-*` only to the 429
   response object. T2 L269 and T4 L14 say success responses always carry
   them ("성공 응답에도 `X-RateLimit-*` 헤더가 항상 포함되며 클라이언트
   단위로 매초 갱신됩니다").
4. **Example header value.** The T1 `X-RateLimit-Limit` example `10` does
   not match `MARKET_DATA` 15/s (T2). **Inference:** the example is
   generic.
5. **Source-of-truth claim versus content.** T5 L16 names T1 as the source
   of truth "for … rate limits", but T1 carries only group names. All
   numbers are in T2. T5 also calls T1 "OpenAPI 3.0", while T1 declares
   `3.1.0`.
6. **Group-name drift.** T2 lists `MARKET_INDICATOR_PRICE` (10/s), but no
   T1 operation is tagged with it. `/api/v1/market-indicators/prices` is
   tagged `MARKET_INDICATOR`.
7. **Catalog drift.** T1 and T2 error codes differ (§6.4). The `edge-*`
   codes (401/403/404/414/429) come from the front layer and exist only in
   T2.
8. **`requestId` required but sometimes absent** (T2 L304; see §6.3).
9. **`ORDER` peak limit equals its normal limit.** It is 10/s at both
   times (T2), which may be a documentation slip. This item is
   order-related only.

### 6.7 Relation to KTradeLink error taxonomy (Inference only)

Reference: `src/ktradelink/errors.py` on `main` @ `a5d2639e…` (unchanged since `7b7aa074…`)
(blob `fea3222272023105dc77bf200ef9795cf38d8643`). L17–19 map classes by
generic HTTP status. Native codes are not interpreted (ADR 0013).

| Upstream signal | Candidate class | Status | What would confirm it |
| --- | --- | --- | --- |
| 429 `rate-limit-exceeded` / `edge-rate-limit-exceeded` | `RateLimitExceeded` | **Inference:** status-only mapping already matches | Captured 429 with headers, under an explicit authorization |
| 401 `expired-token` / `invalid-token` / `login-user-not-found` | `AuthenticationError` | **Inference** | Same |
| 401 `token-revoked` | `AuthenticationError` | **Inference:** this one means "another holder reissued" and is a cross-process hazard. A distinct internal reason may be useful; reissuing must not be automatic. | ADR decision; authorized capture |
| Token 403 `access_denied` / 403 `ip-not-allowed` / `forbidden` / `edge-blocked` | `PermissionDenied` | **Inference:** the same status covers both IP allow-listing and entitlement | Authorized capture of the body on `prices` |
| Token 401 `invalid_client`, 400 `invalid_request` | `AuthenticationError` / `InvalidParameter` | **Inference:** the OAuth2 envelope is not `ErrorResponse` | — |
| 404 `stock-not-found` | `InvalidSymbol` (today: status-only path; 404 is not mapped specifically) | **Inference** | Decoder/transport decision |
| 400 `invalid-request` with `data.field` | `InvalidParameter` or `BrokerRejected` | **Inference** | — |
| 500 `internal-error` / `maintenance` | `BrokerUnavailable` | **Inference:** status-only mapping already matches; no automatic retry | — |
| Body without `result`, or both `result` and `error` | `ResponseSchemaError` | **Inference** | — |

### 6.8 Gates and not-verified items

- **Rate limits are not a contract.** The T2 numbers "사전 공지 없이 조정될
  수" and are not in T1. A limiter must not hard-code them as a guarantee.
  Reading `X-RateLimit-*` at runtime is the publisher's stated source, and
  it is unverified.
- **No automatic retry.** Do not adopt the 429 back-off advice for
  non-idempotent routes. For read-only `prices`, any retry policy needs its
  own maintainer decision; publisher advice is not a safety signal.
- **Token sharing.** One valid token per client is documented (T1, T4).
  Cross-process invalidation stays an open gate (see
  `live-auth-transport-gates-2026-11-05.md`). Do not add automatic reissue
  on `token-revoked`.
- **Not verified:**
  - the actual 403 body on `/api/v1/prices` from a non-allow-listed IP;
  - whether a 401 on Market Data routes uses the T1 `Unauthorized` shape;
  - whether success responses carry `X-RateLimit-*`;
  - how a batch with an unknown symbol is handled;
  - the `edge-*` code bodies;
  - the `requestId`-missing case.

  Each of these needs an explicitly authorized live check. None was
  performed.

## 7. Meritz Securities

### 7.1 Pinned sources

Sources are the portal `https://openapi.imeritz.com`, retrieved 2026-11-05
07:43:53–07:45:40 UTC, and the GitHub repository
[`meritz-securities/open-api@a93c6409db73ea97ad15f7b7186f36c9f32ecd89`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89)
(commit 2026-10-28T22:32:03+09:00). `git ls-remote` at 07:46:16Z showed
this commit is still `HEAD`. The repo README L11 says "API 목록과 파라미터·
응답 필드의 정본은 개발자 포털입니다." Repo content therefore ranks below
the portal: it is `publisher repo note` or `publisher client code`.
errors.md L3 claims "실제 호출로 확인된 값만 담았습니다". That is a
publisher claim and was not verified here.

The portal notice (M4) and FAQ (M12) bodies are loaded by the portal page
script from public, unauthenticated JSON endpoints:
`/api/forums/{forumId}/posts` and `/api/forums/{forumId}/posts/{postId}`.
These were fetched as public documentation. No broker gateway (`:9443`)
request was made. Staff names and contacts in the post metadata were not
copied.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| M1 | Portal spec export [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json) (`title` "메리츠증권 Open API 명세") | 07:43:53Z, sha256 `afc8983dbc6507ee…`, 1,136,519 bytes, `generatedAt "2026-11-05 16:43:51"`. With `generatedAt` removed and `sort_keys`, the canonical hash is `2fff4f3e02d20cd5…`, **identical** to the trade/candle evidence copies. | `groups[0]` OAuth: `token` (`expires_in` String len 10; example `604800`), `revoke` (response `code`/`message`); `rsp_cd` field descriptions: `groups[2].apis[19]` `/market/v1/prices`, `[2].apis[14]` profit-loss/summary, `[3].apis[21]` overseas market-hours, `[3].apis[22]` overseas market-days, `[3].apis[26]` `/forex/v1/rates` (EGW00200 text) |
| M2 | [samplecode-py](https://openapi.imeritz.com/samplecode-py) | 07:43:56Z, sha256 `4f59caafce3e6a70…` (this page varies per request) | sample `OK_CODES`; "오류도 HTTP 500 + JSON 본문으로 오므로, 상태코드가 아니라 rsp_cd 로 판정합니다"; "초당 호출 한도는 공지사항에 기재하였습니다." |
| M3 | [howto-use](https://openapi.imeritz.com/howto-use) | 07:43:55Z, sha256 `912809adf5bbb244…` | token example, `EGW00103`, `EGW00123`/`EGW00121`, revoke text, "오류는 종류와 관계없이 HTTP 500" |
| M4 | Portal notice "API 호출 유량 제어 안내(REST, WEBSOCKET)": [`/api/forums/10000000-0000-0011-0000-000000000001/posts/3dc11098-4ce4-4695-abf5-4c7aa194cb9d`](https://openapi.imeritz.com/api/forums/10000000-0000-0011-0000-000000000001/posts/3dc11098-4ce4-4695-abf5-4c7aa194cb9d) (board page [`/community-notice`](https://openapi.imeritz.com/community-notice) → `/community/…0001`) | 07:45:01Z, sha256 `06570a95f862eb3a…`, `createdDate 2026-09-23T10:12:28+09:00`, no `lastModifiedDate`. The notice list (2 posts) was retrieved at 07:44:49Z, sha256 `7572eab660f71a46…`. | REST/WebSocket rate limits (content lines 1–6) |
| M5 | [`openapi.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/openapi.json) | blob `93e900e66b965607d7fd8b8e14c6088d710e6fce`; `info.version "2026-10-28"` | `x-tps`: `"10"` on 71 of 73 operations; `"-"` on `token` (L131) and `revoke` (L222). Only `200` responses are modelled; there is no error schema. |
| M6 | [`meritz/data/corrections.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/data/corrections.json) | blob `60370924e13233bbd2cccb517bfffee002dad915` | L4–20 `rsp_cd` corruption on 8 domestic market-data APIs; L61–70 `oauth2_revoke` (one token per app key) |
| M7 | [`docs/errors.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/docs/errors.md) | blob `b4b2eac6541bd2b886071c1caad17fa0c57ba3e6` | L7–9, L25–31, L35–47, L75–99 (error table), L117–132 (decision order), L138–146 (client labels) |
| M8 | [`llms.txt`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/llms.txt) | blob `8351d5343d785b61107179d19197c59a08e1edff` | L59–60 token reuse; L81–82; L114–118; L120–126 rate limit and no auto-retry |
| M9 | [`README.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/README.md) | blob `61aa5f7f2c1059a29a99175a5cdf573996d81479` | L11 portal canonical; L125 no paper account |
| M10 | [`meritz/core/client.py`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/core/client.py) | blob `7c68d3a4006730c09b18acb90ddcf2d478a40c16` | L23–27 code sets; L217–278 `TokenManager`; L296–320 `_Throttle`; L452–456; L487–494 token-dead re-call; L527–537 `RATE_LIMITED` (publisher client code) |
| M11 | [`meritz/data/catalog.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/data/catalog.json) | blob `000c2dbc636ad46077d4f46d67a04e0cd6fe1319` | `tps` `"10"` on 85 of 87 APIs, `"-"` on 2 |
| M12 | Portal FAQ board, forum `10000000-0000-0011-0000-000000000002` ([`/community/…0002`](https://openapi.imeritz.com/community/10000000-0000-0011-0000-000000000002)) | list at 07:45:12Z, sha256 `54a894ec38442d90…`, `X-Total-Count: 50`; posts retrieved 07:45:26–07:45:40Z; see the sub-table below | throttle code, IP policy, token/app-key invalidation, error FAQs |

M12 posts used. Each is pinned by post-id prefix, `createdDate` and
sha256 prefix; all are under `/api/forums/…0002/posts/<id>`:

| Post | Title (verbatim, abridged) | createdDate | sha256 |
| --- | --- | --- | --- |
| `5e6c2b36` | "Max retries exceeded with url 오류가 발생했어요" | 2026-09-17 | `6ff3294baaf60c93…` |
| `604f4641` | "EGW00201 에러가 발생했습니다." | 2026-09-17 | `6d2ffc6fdb0b8b58…` |
| `3ce2726f` | "API 호출 유량 제어 안내(REST, WEBSOCKET)" (points to M4) | 2026-09-17 | `f8de871c0cf377c7…` |
| `582875d3` | "EGW00002 서버 에러가 발생했습니다." | 2026-09-17 | `bec3cdc219397929…` |
| `e91ad610` | "EGW00202 에러가 발생했어요." | 2026-09-17 | `bdf46e89c694489d…` |
| `e0a0d56c` | "EGW00205 에러: credentials_type이 유효하지 않습니다" | 2026-09-17 | `24b4c7ee38617a5b…` |
| `2b676a2c` | "IGW50004 \"MCI 전문바디 구성 중 오류\" …" | 2026-09-17 | `9c4d648279dfcce5…` |
| `dbed6402` | "MCI 전문바디 구성 중 오류가 발생하였습니다. …" | 2026-09-17 | `4d884c39818197ed…` |
| `7e0ebaf1` | "MCI 통신 중 오류가 발생하였습니다 …" | 2026-09-17 | `95cc027f11d71552…` |
| `799f0367` | "화이트리스트(White List) IP 등록 정책이 있나요?" | 2026-09-17 | `7e1829e78c106123…` |
| `12b6388a` | "Open API 이용 시 특정 IP로만 사용 가능한가요?" | 2026-09-17 | `8e924fb92e7f9d35…` |
| `035e045c` | "메리츠증권 오픈API는 유동 IP 환경에서도 이용할 수 있나요?" | 2026-09-17 | `1ed381566210ea86…` |
| `a40ed3f5` | "Open API 운영 시간은 어떻게 되나요?" | 2026-09-17 | `4bd48710d8a79975…` |
| `c0849a6c` | "계좌 비밀번호를 변경하면 기존 App Key를 계속 사용할 수 있나요?" | 2026-09-23 | `50247d14f3369723…` |
| `edcfd260` | "ID를 등록/변경 하면 기존 App Key를 계속 사용할 수 있나요?" | 2026-10-16 | `b9791b3594d348b3…` |
| `91b2bcf6` | "… '계정당 최대 세션 수 초과' 시 개인 세션 초기화 방법" | 2026-10-29 | `0ebb2a76bb0841c4…` |
| `5f27d9b8` | "IGW50024 \"mac_address 헤더값은 필수입니다.\" 에러가 발생했어요." (title from the list only; body not fetched) | 2026-09-17 | list hash above |

**Missing evidence:**

- **Token issuance limit:** none is documented. The portal (M1/M3) states
  no issuance-frequency limit, and M5/M11 give `tps "-"` for `token` and
  `revoke`. **Not found.**
- **No error catalog in the portal.** Only M7 (repo) has a code table.
  Portal codes are scattered across field descriptions, M3 and FAQ posts.
- **No throttle header or `Retry-After`.** None is documented anywhere.
- **The second notice was not used.** "메리츠증권 Open API 서비스 오픈 일정
  및 이용 안내" (2026-10-12, sha256 `6b1f55f7787c18d1…`) only says the beta
  period may be unstable. It is not used beyond that.
- **No paper environment.** M9 L125: "앱키에 연결된 계좌는 실계좌입니다.
  모의계좌는 없습니다".

### 7.2 Rate limits

| Concern | Value (verbatim) | Scope / unit | Real vs paper | Evidence |
| --- | --- | --- | --- | --- |
| Per-second / per-minute request limit | M4 content L1–3: "API 초당 호출 가능 유량에 대해 안내드립니다." / "- REST API: 1초당 10건" / "* 계좌 단위로 유량 제한 (1계좌당 10건/초)". M12 `5e6c2b36`: "모든 REST API(주문, 잔고조회, 시세조회 등) 합산하여 1초당 10건 호출 유량 제한이 됩니다." M7 L95: "`EGW00200` \| 초당 호출 한도 초과 \| API 당 초당 10건입니다. 재시도 가능합니다". M8 L120: "**초당 호출 한도는 API마다 10건입니다.**" M2: "초당 호출 한도는 공지사항에 기재하였습니다." | **Conflicting:** per account, all REST summed (M4, M12) versus per API (M7, M8, M5/M11 `x-tps`). See §7.6 #1. | Real only (M9 L125) | publisher guide (M4, M12) vs publisher repo note (M7, M8) |
| Per-route (TR) limits | M5 `x-tps "10"` on 71/73 operations; M11 `tps "10"` on 85/87 APIs; `"-"` on `token`/`revoke`. No route has a value other than 10. M1 (portal spec) has **no** per-API TPS field. | per API (repo) | Real only | publisher repo note |
| Token issuance limit / interval | **Not found** (`tps "-"` for `token`, M5 L131). | — | — | not found |
| Token lifetime and reissue behaviour | M1 `expires_in` "유효기간 (초)" (String, len 10); example `604800`. M3: "발급 응답의 expires_in(초) 동안 유효합니다. 만료 전까지 재사용하고, 만료(rsp_cd EGW00123)·무효(EGW00121) 응답을 받으면 APP KEY·APP SECRET 으로 재발급한 뒤 이용합니다." M3 revoke: "토큰 폐기 API(POST /oauth2/revoke)를 호출하면 해당 APP KEY 로 발급된 토큰이 즉시 무효화됩니다." M6 L67 (repo): "같은 앱키로 발급받은 토큰은 하나이므로, 다른 프로세스·세션이 쓰고 있던 토큰도 함께 끊깁니다." Whether a **new `/oauth2/token` call** invalidates the previous token is **not stated** by the portal. M12 `c0849a6c`/`edcfd260`: after an account password change or ID registration/change, "기존 App Key로 API를 호출할 때 오류가 발생합니다". | per app key | Real only | publisher guide + publisher repo note; reissue-invalidation **not found** |
| WebSocket limits (mention only) | M4 L4–6: "- WEBSOCKET : 2세션" / "실시간주식체결가 + 실시간주식호가 20건 등" / "*HTS ID 단위로 유량 제한(1개의 HTS ID당 2세션)". M7 L99 `WSC00110` "계정당 최대 세션 수 초과". M12 `91b2bcf6` documents a session-reset endpoint (`POST …/websocket/clearSession`); recorded only and not called. | per HTS ID | — | publisher guide |
| Continuation/paging limits relevant to throttling | `rsp_cd` `5762` "다음 페이지 있음" + `tr_cont`/`tr_cont_key` (M7 L43). M7 L110–112: continuation actually works on only six APIs (account/order families). Market data has none (trade evidence §7.3). **Inference:** each page is one call against the 10/s budget. | — | — | publisher repo note; Inference |

### 7.3 Status envelope and HTTP status use

| Concern | Value | Evidence |
| --- | --- | --- |
| Success indicator | `rsp_cd` (String). **The success value differs by API family.** For `/market/v1/prices`: "이 API 의 성공 응답 코드입니다. "0000": 정상 처리 조회 결과가 없을 때도 "0000" 이 내려옵니다." Other families use `5766`/`5762`/`5820`/`0001`. M2: "성공 응답 코드(rsp_cd)는 계열마다 다릅니다. 자료가 있는지 없는지는 rsp_cd 가 아니라 data로 판단하시길 바랍니다." M2 sample `OK_CODES = {"0000", "0001", "5762", "5766", "5820", "5822"}`; M10 L27 adds `5620`. | field table (M1) + publisher example (M2) + client code (M10) |
| Failure indicator + message fields | `rsp_cd`, `rsp_msg`, `rsp_sub_msg`. M2: "원인은 rsp_cd 와 rsp_msg 에, 구체적인 조치 사항은 rsp_sub_msg 에 담겨 옵니다." M7 L21–23: `rsp_msg` is often vague; the actionable detail is in `rsp_sub_msg`. | publisher example + repo note |
| Is HTTP status meaningful? | Mostly no. M3: "오류는 종류와 관계없이 HTTP 500 으로 오며". M7 L8–9: "권한이 없어도 500, 날짜 형식이 틀려도 500, 필수값이 빠져도 500 입니다. 403·400·404 는 오지 않습니다." Exceptions are below. | publisher guide + repo note |
| Exceptions | M7 L75: "전부 HTTP 500 으로 옵니다(`EGW00103` 만 403 으로 올 때가 있습니다)." M10 L242 comment: "HTTP 403 {"rsp_cd":"EGW00103",…}". M1 `[3].apis[21]`: "범위 밖의 두 자리 값(예: "33")을 넣으면 HTTP 500 과 함께 data 가 없는 본문이 내려오며, 이때 rsp_cd 는 "0000" 입니다." and "일부 오류는 rsp_cd 가 "0000" 으로 내려오므로, 성공 여부는 HTTP 상태와 rsp_cd "5766" 을 함께 확인하십시오." M6 L15–16: 8 domestic market-data APIs return "HTTP 200 과 정상 data 를 주면서 rsp_cd 에 널바이트가 섞여 옵니다." | field table + repo note |
| Throttle signal | HTTP **500** + `rsp_cd` **`EGW00200`** (M1 on four APIs, e.g. `/forex/v1/rates`: "초당 호출 건수를 넘기면 "EGW00200" 이 내려오며, 잠시 뒤 같은 요청을 다시 보내십시오."; M7 L95; M8 L120–121). **The FAQ names a different code:** M12 `604f4641`: "EGW00201는 초당 거래건수를 초과하였을 때 표시되는 오류 코드입니다." No `Retry-After` or `X-RateLimit-*` is documented. M10 L529: "초당 거래건수 초과가 429 가 아니라 500 으로 온다." | field table + guide + repo; code **conflicting** (§7.6 #2) |
| Token-expired / invalid-token signal | M3: "만료(rsp_cd EGW00123)·무효(EGW00121)". M7 L93–94: `EGW00121` "유효하지 않은 token"; `EGW00123` "기간이 만료된 token" — "캐시의 만료 시각이 남아 있어도 서버가 거절합니다". HTTP status is 500 (M7 L75; not shown verbatim for these codes). | publisher guide + repo note |
| Error-response body schema | JSON with `rsp_cd`/`rsp_msg`/`rsp_sub_msg`. The trade evidence (§7.4) cites M1: "오류 응답에는 data·tr_cont 가 없으므로". The token endpoint error uses the same keys (M3 example: `{"rsp_cd": "EGW00103", "rsp_msg": "유효하지 않은 client_id입니다."}`). Revoke success uses a **different** shape, `{code, message}` (M1). M7 L143: a non-200 without `rsp_cd` = "프록시·업스트림 장애". | field table + publisher example + repo note |

### 7.4 Error catalog and mapping concerns

There is no portal catalog. The repo table in M7 has **21 error codes**
(L79–99) and **8 success codes** (L40–47). Its categories:

- business/request: numeric codes such as `0760`, `3174`, `5018`, `7936`;
- gateway request validation: `IGW5000x`;
- gateway auth/throttle/server: `EGW…`;
- WebSocket: `WSC…`.

Portal-side codes are scattered:

- M3: `EGW00103`, `EGW00121`, `EGW00123`;
- M1: `EGW00200`, `IGW50002`, `EGW00202`, and family codes;
- M12 FAQ: `EGW00002`, `EGW00201`, `EGW00202`, `EGW00205`, `IGW50004`,
  `IGW50024`.

`EGW00201` and `EGW00205` are **not** in M7.

| Concern | Code(s) + message verbatim | Evidence |
| --- | --- | --- |
| Rate limit exceeded | `EGW00200` "초당 호출 한도 초과" (M7 L95; M1 four APIs). `EGW00201` "초당 거래건수를 초과하였을 때 표시되는 오류 코드" (M12 `604f4641`). M12 `5e6c2b36` attributes the client-side message "Max retries exceeded with url" "주로 API 유량제한된 경우" (**Inference:** that text comes from the Python HTTP library, not from the gateway). | field table + guide + repo note |
| Token expired / invalid / revoked | `EGW00123` "기간이 만료된 token"; `EGW00121` "유효하지 않은 token" (M3, M7 L93–94). There is no distinct "revoked by reissue" code; revoke makes tokens "즉시 무효화" (M3). | publisher guide + repo note |
| Credential / app-key invalid | `EGW00103` "유효하지 않은 client_id입니다." M3: "APP KEY 오타이거나 비밀번호 변경, ID변경 또는 ID등록의 경우에 발생할 수 있습니다." (sometimes HTTP 403, M7 L75). `EGW00205` "credentials_type이 유효하지 않습니다" → M12: "토큰 지정시 토큰 타입 지정 부탁드립니다." `EGW00202` → M12: "요청 시 헤더에 authorization: Bearer {Token} 입력이 필요합니다." (M7 L96 instead says "권한 없음 (게이트웨이 단계)"). | publisher guide + FAQ + repo note |
| Permission / entitlement / IP allow-list | `0760` "권한이 없습니다." M7 L79: "**재시도·토큰 재발급으로 풀리지 않습니다.**" M8 L116–117 agrees. IP: M12 `12b6388a`: "별도의 허용 IP 목록을 운영하거나 특정 IP를 차단하지 않습니다." M12 `035e045c`: "접속 IP와 무관하게 인증이 이루어지기 때문에 고정 IP가 필요하지 않습니다." There is **no IP allow-list signal**. | repo note + FAQ |
| Invalid symbol / no such instrument | **No error code.** M1 `/market/v1/prices` `iscd`: "표준코드(KR7005930003)·소문자 a(a005930)·등록되지 않은 코드는 오류 없이 정상 응답코드 "0000" 으로 내려오되 값이 비거나 0 입니다. … 응답의 단축종목코드(shrn_iscd)가 채워져 있는지 확인하십시오." | field table |
| Invalid parameter / malformed request | `IGW50004` "전문 길이 초과 · 필수 누락" (M7 L88; M12: "요청 시의 Body 입력값 및 포맷을 확인"). `IGW50006` "시장구분코드가 그 API 에 맞지 않음" (M7 L89). `IGW50024` "mac_address 헤더값은 필수입니다." (M12 title; M7 L90 "필수 헤더 누락"). `IGW50002` on over-precise prices (M1). `7936`: `rsp_msg` "해당데이터가 없습니다." but actually "**필수값 누락**" (M7 L87). | field table + FAQ + repo note |
| Market closed / outside service hours | **Not found** as an error code. M12 `a40ed3f5`: "점검일 등 예외 사항이 없을 시, 24시간 조회 가능합니다." | FAQ |
| Server busy / maintenance / internal error | `EGW00002`: M7 L91 "서버측 오류 \| 자격증명 문제가 아닙니다". M12 `582875d3` instead: "요청 전문에 오류가 있는 것으로 … body를 json으로 담아서 호출하셨는지 확인". FAQ "MCI 통신 중 오류가 발생하였습니다" → "요청전문이 정확한지 확인". No maintenance code was found. | repo note vs FAQ (conflict, §7.6 #3) |
| "No data" returned as success? | **Yes.** `0000` + empty/zero for `prices` (M1). `5820`/`5822` "조회할 자료 없음" are success codes, and "**자료를 담은 채로도 `5820` 을 보냅니다.**" (M7 L49–58). M7 L101–107: wrong date formats return data with the period ignored "정상 코드와 함께". | field table + repo note |

### 7.5 Publisher retry / back-off behaviour (recorded, not adopted)

These items record what the publisher does or recommends. None of them is
evidence that a retry is safe.

- **"Retry" wording on `EGW00200`:**
  - M1 (four APIs): "잠시 뒤 다시 보내십시오" / "잠시 뒤 같은 요청을 다시
    보내십시오".
  - M7 L95: "재시도 가능합니다".
  - M7 L123: "간격을 두고 재시도할 수 있다".
  - M7 L141: "`RATE_LIMITED` … 간격을 두고 재시도하면 됩니다
    (`retryable=True`)".
- **Pre-emptive per-API throttle.** M8 L121 and M10 L296–320 (`_Throttle`)
  apply a sliding one-second window **per API key**, using `tps` from M11.
  M8 L125–126: "응답에 `retryable`만 표시하고 다시 보내지는 않습니다. 자동
  재시도·백오프와 웹소켓 재연결은 예제 범위 밖이니, 언제 다시 보낼지는
  호출하시는 쪽에서 정하셔야 합니다."
- **Automatic re-send after a dead token.**
  - M10 L487–494: on `EGW00121`/`EGW00123` the client invalidates the
    token, fetches a new one and **calls the same request again once**.
    `call()` does not restrict this by API type.
  - **Inference:** this would re-send state-changing requests too. A
    token-rejection code is not proof that the first request had no
    effect, so KTradeLink must not copy this pattern.
- **Token reuse and early refresh.**
  - M2/M3 examples refresh the token at `expires_in - 60` s.
  - M10 L269 falls back to `expires_in` 43200 when the field is absent.
    The comment at L489 says "최대 12시간".
- **Timeout guidance.** M10 timeout text: "상태변경 요청이었다면 재전송 전에
  조회 API 로 실제 처리 여부를 먼저 확인하십시오." This is consistent with
  AGENTS.md.
- **FAQ advice.** M12 `799f0367` suggests "예외처리(try-except)로 일시적 오류
  회피 시도" for 500 errors. This is generic advice, not a contract.

### 7.6 Contradictions and gaps

1. **Rate-limit scope is unresolved.**

   The 10/s scope is stated three different ways:

   - **Per account, all REST summed (portal):**
     - M4 notice ("API 호출 유량 제어 안내(REST, WEBSOCKET)",
       [`/api/forums/10000000-0000-0011-0000-000000000001/posts/3dc11098-4ce4-4695-abf5-4c7aa194cb9d`](https://openapi.imeritz.com/api/forums/10000000-0000-0011-0000-000000000001/posts/3dc11098-4ce4-4695-abf5-4c7aa194cb9d),
       retrieved 2026-11-05 07:45:01Z, sha256 `06570a95f862eb3a…`, created
       2026-09-23): "- REST API: 1초당 10건" / "* 계좌 단위로 유량 제한
       (1계좌당 10건/초)".
     - M12 `5e6c2b36` (2026-09-17) agrees: "모든 REST API(주문, 잔고조회,
       시세조회 등) 합산하여 1초당 10건".
   - **Per API (repo):**
     - `meritz-securities/open-api@a93c6409db73ea97ad15f7b7186f36c9f32ecd89`
       `docs/errors.md` (blob `b4b2eac6541bd2b886071c1caad17fa0c57ba3e6`)
       L95: "`EGW00200` | 초당 호출 한도 초과 | API 당 초당 10건입니다.
       재시도 가능합니다".
     - `llms.txt` L120 (blob `8351d5343d785b61107179d19197c59a08e1edff`):
       "초당 호출 한도는 API마다 10건입니다."
     - M5/M11 `x-tps "10"` per operation. M10 throttles per API key.

   Under the portal reading, ten APIs at 10/s each would exceed the
   account budget tenfold. It is **unverified** whether both limits apply
   at once (per API **and** per account) or whether the documents simply
   conflict. The portal ranks above the repo (M9 L11), but the repo is
   newer (2026-10-28 versus the 2026-09-23 notice).

2. **Throttle code.** `EGW00200` is used by M1 (portal field table, four
   APIs), M7, M8 and M10. M12 `604f4641` (portal FAQ) says `EGW00201` is
   "초당 거래건수 초과". M10 L24 labels `EGW00200` with the same wording,
   "초당 거래건수 초과". `EGW00201` is absent from M7. **Inference:**
   either both codes exist (for example per-API versus per-account) or the
   FAQ is stale. Neither is verified.
3. **`EGW00002` meaning.** M7 L91 says "서버측 오류 … 자격증명 문제가
   아닙니다". M12 `582875d3` says it means the request text is malformed
   (non-JSON body, missing commas). Server-side versus client-side cannot
   be settled from the documents.
4. **"Every error is HTTP 500" has exceptions.** These are `EGW00103` as
   HTTP 403 (M7 L75, M10 L242), an HTTP 500 with `rsp_cd "0000"` (M1
   overseas market-hours), and HTTP 200 with a corrupted `rsp_cd` (M6
   L4–20). Neither status nor `rsp_cd` alone classifies a response.
5. **`EGW00202` meaning.** M7 L96 says "권한 없음 (게이트웨이 단계)". The
   M12 FAQ and the M1 WebSocket text say it is the missing `Bearer`
   prefix or missing `authorization` header.
6. **Token lifetime.** The M1 example has `expires_in` `604800` (7 days)
   while its field type is String len 10. M10 assumes 43200 when the field
   is absent and comments "최대 12시간". The real lifetime is unverified.
7. **One token per app key** is a repo note (M6 L67). The portal says only
   that revoke invalidates "해당 APP KEY 로 발급된 토큰". Whether issuing a
   new token invalidates the previous one is **not stated** by the portal.
8. **Success-code sets differ.** The M2 sample `OK_CODES` lacks `5620`;
   M7 L42 and M10 L27 include it ("예약 주문 접수").
9. **No throttle headers.** Unlike Toss there is no `Retry-After` or
   remaining-budget signal, so the client cannot learn its budget at
   runtime.

### 7.7 Relation to KTradeLink error taxonomy (Inference only)

Reference: `src/ktradelink/errors.py` on `main` @ `a5d2639e…` (unchanged since `7b7aa074…`)
(blob `fea3222272023105dc77bf200ef9795cf38d8643`). L17–19 say the classes
are chosen by generic HTTP status and that broker-native codes are not
interpreted. For Meritz, **status-only mapping would put every error,
including throttle, token and permission errors, into
`BrokerUnavailable`** (5xx). That would hide the actionable cause. The
same concern is recorded in `live-auth-transport-gates-2026-11-05.md` as
"500 → `SERVER`".

| Upstream signal | Candidate class | Status | What would confirm it |
| --- | --- | --- | --- |
| HTTP 500 + `EGW00200` (and possibly `EGW00201`) | `RateLimitExceeded` | **Inference:** requires `rsp_cd` interpretation, a change to ADR 0013 | Maintainer ADR; authorized capture of the throttle body |
| HTTP 500 + `EGW00121` / `EGW00123` | `AuthenticationError` | **Inference** | Same |
| HTTP 500/403 + `EGW00103`, `EGW00205` | `AuthenticationError` | **Inference** | Same |
| HTTP 500 + `0760` / `EGW00202` | `PermissionDenied` | **Inference:** `EGW00202` is ambiguous (§7.6 #5) | Same |
| HTTP 500 + `IGW5000x`, `7936`, `3174`, `6102`, `5018` | `InvalidParameter` or `BrokerRejected` | **Inference** | Same |
| HTTP 500 + `EGW00002` | `BrokerUnavailable` or `InvalidParameter` | **Inference:** sources conflict (§7.6 #3) | Same |
| `0000` with empty `shrn_iscd` / zero values on `prices` | `InvalidSymbol` | **Inference:** not distinguishable from "no data" by code | Decoder rule plus authorized fixture |
| HTTP 200 with unreadable `rsp_cd` | `ResponseSchemaError`, or success only with data (M6 workaround) | **Inference:** library policy choice; fail-closed is the default | Maintainer decision |
| Non-200 without `rsp_cd` (proxy HTML etc.) | `TransportError` / `BrokerUnavailable` | **Inference** | — |

### 7.8 Gates and not-verified items

- **Rate-limit scope gate.** Neither "계좌당 10/s" (M4) nor "API당 10/s"
  (M7 L95) may become a fixed, global limiter contract on its own. A
  limiter design must record the conflict (§7.6 #1), cite both pins, and
  get a maintainer decision before it is relied on. Whether both limits
  apply at once is unverified.
- **Throttle code gate.** Do not treat a single code as the only throttle
  signal until `EGW00200` versus `EGW00201` is resolved (§7.6 #2).
- **No automatic retry.** Publisher "재시도 가능" wording, `retryable=True`
  and the M10 token-dead re-send are behaviour records, not safety
  evidence. An HTTP 500 from this gateway is never proof that a request
  was not processed (AGENTS.md).
- **Status-only classification is insufficient.** Any enablement needs
  broker-specific `rsp_cd` interpretation (ADR change), in particular
  before any order path.
- **Token gates.** The real lifetime, whether reissue invalidates the
  previous token, and the issuance frequency limit are all undocumented or
  unverified. Revoke invalidates all tokens of the app key (M3); never call
  it as a test.
- **`mac_address`.** The header is required (`IGW50024`). Publisher
  auto-detection is not described or copied here, and it must not be
  adopted.
- **Not verified:**
  - the throttle code and body;
  - the scope of the 10/s limit;
  - `EGW00103` 403 versus 500;
  - token lifetime;
  - the `rsp_cd` null-byte corruption;
  - `EGW00002` semantics.

  Each needs an explicitly authorized live check. None was performed.

## 8. Cross-broker comparison

### 8.1 Signals side by side

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Numeric request quota in the pinned sources | none (legacy "1초당 20건") | none | per TR, 1–10 TPS (§4.2) | app 20 TPS + per API 2–10 TPS (§5.2) | per client × group, e.g. `MARKET_DATA` 15/s (§6.2) | 10/s (§7.2) |
| Quota holder | not stated | not stated | not stated | app (= account) | `client_id` × group | **conflicting**: account, all REST summed (portal) vs per API (repo) |
| Limits can change without a new pin | — | — | yes, by notice (2023, 2025) | yes, by notice (IPO-day 1 TPS) | yes, "사전 공지 없이" | not stated |
| Throttle carried in | body `msg_cd` `EGW00201`; status unknown | body `return_code` `1700`–`1702`; status unknown | **not found** | body `rsp_cd` `IGW00201` on HTTP 403 **or** 500 | HTTP 429 + `error.code` `rate-limit-exceeded` | HTTP 500 + `rsp_cd` `EGW00200` (FAQ: `EGW00201`) |
| Throttle headers | not found | not found | not found | not found | `X-RateLimit-*`; `Retry-After` on 429 | not found |
| Token-issuance budget | 1/min (repo note) | ~2/s, demo, publisher-measured (repo note) | not found | 1/min (field table) | `AUTH` 5/s | not found |
| Token-invalid signal | `EGW00123` (legacy, HTTP 200) | `8005` (table); HTTP 401 (client) | not found | `IGW00121`/`IGW00122`/`IGW00123` on 403 or 400 | HTTP 401 `expired-token` / `invalid-token` / `token-revoked` | `EGW00121` / `EGW00123` on HTTP 500 |
| Re-issue returns the same token? | yes within 6 h (client comment) | yes while valid (repo note) | not found | yes before expiry (field table) | **no**: previous token "즉시 무효화" | portal silent; repo: one token per app key, revoke kills all |
| Success value and type | `rt_cd` `"0"` string | `return_code` `0` number (examples) | `rsp_cd` `"00000"` string | `rsp_cd` `"00000"` string | no code; `result` present | `rsp_cd` string, value per API family |
| Business errors on HTTP 200? | yes (client) | yes (client comment) | OAuth yes (portal script); TRs not documented | "sometimes" (D2) vs only `00000` under 200 (D1) | no (4xx/5xx documented) | no; but HTTP 500 can carry `"0000"` and HTTP 200 a corrupted `rsp_cd` |
| "No data" as success? | both forms (§2.4) | not found | yes (`00000` + "해당자료가 없습니다.") | both (`00000` / `2679`) | not documented; unknown symbol is 404 | yes (`0000` with empty values; `5820` even with data) |
| Error catalog | not found | 37 rows (field table) | not found | repo tables (68 + 70 + 6 rows) | 53-row guide table; spec examples differ | repo table only (21 + 8) |

### 8.2 What a common mapping could and could not rely on

All points are **Inference:** from the six sections above.

- **`RateLimitExceeded` by HTTP 429 covers Toss only.** KIS and Kiwoom put
  the throttle in the body with an undocumented status; DB sends
  `IGW00201` on 403 or 500; Meritz sends `EGW00200` on 500; LS documents
  nothing. A common class would need per-broker native-code tables, which
  ADR 0013 does not interpret today.
- **`AuthenticationError` by HTTP 401 covers Toss and part of Kiwoom.**
  Kiwoom also signals `8005` in an HTTP-200 body; DB uses 403/400 with
  `IGW0012x`; Meritz uses 500 with `EGW00121`/`EGW00123`; KIS evidence is
  a legacy HTTP-200 sample; LS has none.
- **HTTP 403 does not mean "permission" across brokers.** On Toss it is IP
  allow-listing or entitlement. On DB, 403 also carries throttling
  (`IGW00201`), token errors and server errors (`IGW00001`, `IGW00002`).
  On Meritz it appears only for the credential code `EGW00103`.
- **HTTP 5xx does not mean "unavailable" across brokers.** Every Meritz
  error, including throttle, token, permission and parameter errors, is
  HTTP 500. DB 500 includes throttling and request-validation codes. Only
  for Toss does 500 match `internal-error` / `maintenance`.
- **`BrokerRejected` (HTTP 200 + non-success status)** fits KIS, Kiwoom
  and LS bodies and DB's HTTP-200 errors. It hides throttling and token
  expiry from the caller.
- **Shared code families must not be transferred.** KIS (`EGW00201`,
  `EGW00123`), Meritz (`EGW00121`, `EGW00123`, `EGW00200`, FAQ
  `EGW00201`), DB (`IGW00121`, `IGW00123`, `IGW00201`) and LS (`IGW40011`)
  use similar prefixes and wording: KIS `EGW00201` "초당 거래건수를
  초과하였습니다." vs the Meritz FAQ "EGW00201는 초당 거래건수를 초과하였을
  때"; DB `IGW00123` "기간이 만료된 token 입니다." vs Meritz `EGW00123`
  "기간이 만료된 token". This suggests a common gateway product, but the
  codes already diverge (Meritz `EGW00200` vs `EGW00201`). No code may be
  applied to a broker without that broker's own evidence.
- **No common "retry after" value.** Only Toss sends headers. KIS sources
  disagree on the window (1 s vs 60–61 s); the others give nothing.
- **Token re-issue semantics split.** Toss invalidates the previous token;
  KIS, Kiwoom and DB return the same token while it is valid; LS is
  silent; Meritz's portal is silent on issuance, and its revoke kills
  every token of the app key. A common token cache cannot assume either
  behaviour.
- **Delivery is never implied by a code.** Every body-coded error is
  `RESPONSE_RECEIVED`, and DB `M205`/`M216`, `IGW50005`, `IGW50011`,
  `IGW50012` explicitly leave the outcome open. No class can imply that a
  resend is safe.
- **"No data" has no common shape**, even within one broker (KIS, DB).

## 9. Relation to existing code and docs

Description only; nothing below is changed by this file. Code references
are to `main` at `a5d2639e1b555b54c7a96652432cc2c3bf141fb7`. Its `src/`
and `crates/` are identical to `f254ae87…` and `7b7aa074…`, which some
section drafts cited; blob prefixes: `errors.py` `fea32222…`,
`_https_transport.py` `747138bc…`, `crates/ktradelink-decoders/src/lib.rs`
`d4b6ad4f…`.

### 9.1 Code and documents, claim by claim

| Code / document and its current assumption | This audit |
| --- | --- |
| `src/ktradelink/_public_client.py` L89–90: KIS quote status `rt_cd` must be the string `"0"` | **Matches** K2 L353 and K13 (`"1"` for failure, a string). |
| `_public_client.py` L91–93 and ADR 0013 decision 6: Kiwoom `return_code` must be the integer `0` (not a boolean) | **Matches** every REST example (W1, e.g. L1820). **Differs** from the publisher client's statement that the server sends an int **or a numeric string** (W3 L33–34) and from the WebSocket field tables' `String` type. A string `"0"` would fail closed as `ResponseSchemaError("quote_status_invalid")`. Two REST TRs use `returnCode` (not `ka10001`). |
| `_public_client.py` L94–96 and `lib.rs` L361–364: LS t1102 `rsp_cd` `"00000"` required | **Matches** every LS TR example (L5). LS returns `"00000"` with "해당자료가 없습니다." and no OutBlock on another TR (L12); for t1102 that would fail closed as a decoder rejection. |
| `_public_client.py` L257–278: any other status value → `BrokerRejected`; message and code not exposed | **Consistent** with KIS, Kiwoom and LS sending business errors on HTTP 200. It also means a KIS `EGW00201` or Kiwoom `1700` on HTTP 200 surfaces as `BrokerRejected`, **not** `RateLimitExceeded`, and a Kiwoom `8005` (or `3` + "[8005:…]") on HTTP 200 surfaces as `BrokerRejected`, **not** `AuthenticationError`. |
| `src/ktradelink/errors.py` L17–20, L113–126 and `_https_transport.py` `_http_kind` L412–425: 401/403/429/5xx carry generic HTTP meaning; other non-200 statuses become the generic `HTTP` kind | **Matches Toss only** (§6.3). Not documented for KIS, Kiwoom or LS; contradicted by DB (403/500 carry throttle, token and validation codes, §5.3) and Meritz (all errors 500, §7.3). Toss 404 `stock-not-found` and 400/409/422 fall into the generic kind, i.e. `TransportError`, not `InvalidSymbol`/`InvalidParameter`. |
| `_public_client.py` `_drop_token` L456–464 and ADR 0013 decision 7: only a quote **401** drops the cached token | **Gap** for in-body token failures: Kiwoom `8005`/`8031`/`8103` (W4 L84–96) and KIS `EGW00123` if on HTTP 200 (legacy K19). The cached token stays until its expiry margin. (DB 403/400 and Meritz 500 token codes would not drop it either, if those brokers were enabled.) |
| `src/ktradelink/_token_codec.py` L248–256: Kiwoom token response must carry `return_code` int `0` | **Stricter than the evidence.** The `au10001` field table does not list `return_code`; only the (invalid-JSON) example has it (W1 L163), and the publisher client accepts its absence (W5 L137). A real response without it would fail closed (`ResponseSchemaError`, stage `token`). |
| `_token_codec.py` L241–247: KIS token uses `access_token_token_expired` only; zone supplied by `kis_expiry_timezone` | **Matches** K2 L78. K5 also lists `expires_in` (seconds), which the library does not use; their agreement is unverified. |
| `_token_codec.py` L279: Kiwoom expiry in KST | **Matches** W5 L21, L325–327. |
| `_token_codec.py` L212–224: LS token rejects `rsp_cd`/`rsp_msg` and requires `scope` and one lifetime field | **Consistent** with L7 L1350–1351: an OAuth failure on HTTP 200 with a `code`/`message` body lacks those keys and fails closed (`ResponseSchemaError`, stage `token`). |
| `_public_client.py` L413–426, ADR 0013 decision 7: at most one token request per call; after a rejected token response the next call sends another | **No pacing between calls.** Documented budgets: KIS 1/min (K1 L390), DB 1/min (DP1), Toss `AUTH` 5/s; Kiwoom ~2/s on demo (W8, repo note). Repeated calls after a token failure could hit them. |
| `BrokerClient` docstring L305–308 and ADR 0013 decision 8: "two clients using one app key can invalidate each other's tokens" | **Holds for Toss** (T1 L91, T4 L9) and for Meritz revoke (M3, M6 L67). **Not supported for KIS, Kiwoom or DB**, which return the same token while valid (K2 L220, W8 L13–14, DP1). Kiwoom `8010` adds an IP binding the docstring does not mention. |
| `lib.rs` L374 with L224: the DB decoder accepts a **missing** root `rsp_cd` | **Differs** from every DB source: all guide examples carry it (DP3), D2 L82–83 requires `rsp_cd == '00000'` even on HTTP 200, and D1 L56 / L106–109 define `00000` as the only success code. No source says a quote may omit it. DB is not a public `fetch_ticker` broker today (`_capability`, L141–142). |
| `lib.rs` L392 with L224: the Meritz decoder accepts `rsp_cd` `"0000"` or a missing `rsp_cd`; it does not check `shrn_iscd` | **Gap:** M1 says unregistered codes return `"0000"` with empty or zero values and tells clients to check `shrn_iscd`; M6 reports HTTP 200 with a NUL-corrupted `rsp_cd` on 8 market-data APIs (that case fails closed as a status error). Meritz stays blocked in the transport (`_https_transport.py` L92–93). |
| `lib.rs` `toss_record` L283–308 reads `result` only | T1 says `result` and `error` never co-occur; the decoder does not reject a root `error` beside `result` (already recorded in ADR 0015). |
| `src/ktradelink/_diagnostics.py` L36–37: diagnostics read only `rsp_cd`/`error` and `rsp_msg`/`error_description` | Covers LS, DB and Meritz `rsp_cd`/`rsp_msg` and OAuth `error`. **Does not cover** KIS `msg_cd`/`msg1`, Kiwoom `return_code`/`return_msg`, Meritz `rsp_sub_msg`, or Toss `error` as an object (ADR 0015). Diagnostics are off on the public path (ADR 0013). |
| No retry anywhere (`errors.py` L121–126; `_https_transport.py` L503–506, L555) | **Consistent** with AGENTS.md. Publisher retries are not adopted: KIS 61 s × 3 (§2.5); Kiwoom resend after re-auth (§3.5); DB back-off and token re-issue including orders (§5.5); Toss 429 advice (§6.5); Meritz token-dead resend (§7.5); LS FAQ paper-order advice (§4.5). |
| [ADR 0015](../decisions/0015-db-toss-candidate-wire.md) L172–176: DB errors are HTTP 403 or 500 with `rsp_cd` `IGW…`, classified by status only; the SDK retries `IGW00201` and re-issues on `IGW00121/00123` | **Confirmed** (D1, D3); the SDK token set also includes `IGW00122` (D3 L63). |
| ADR 0015 L163: two processes using one Toss client invalidate each other | **Confirmed** (T1 L91, T4 L9). |
| [live-auth-transport-gates-2026-11-05.md](live-auth-transport-gates-2026-11-05.md) L18: Meritz "Every error is HTTP 5…" | **Confirmed** with exceptions: `EGW00103` sometimes 403, HTTP 500 with `"0000"`, HTTP 200 with a corrupted `rsp_cd` (§7.6 #4). |
| [kiwoom-market-data.md](kiwoom-market-data.md) L50–53: portal quota "orders 5/s and inquiries 5/s"; paper "additional per-TR restrictions" | **Not in this pin set**; not re-verified. The same paragraph ends "must not be copied as a universal KIS quota", which reads as if it meant Kiwoom. |
| [kis-market-data.md](kis-market-data.md) L65–66: "KIS per-TR rate limits must be checked in the up-to-date vendor portal; never assume a generic per-second limit" | **Consistent**: the repo has no per-TR numbers; the portal was not retrieved here. |
| [capability-inventory-2026-11-05.md](capability-inventory-2026-11-05.md) row 7 (L35) | KIS, Kiwoom, LS and DB: **confirmed**. Added here: Kiwoom's measured `au10001` throttle (W8) and the KIS 60/61-second retry wait (K8, K9). Toss "no numeric quota": **differs**, the overview gives per-group numbers (T2 L240–262; the OAS T1 has group names only). Meritz "REST 10/s per account": the portal reading only; the repo says per API (§7.6 #1). |
| Same inventory, row 8 (L36) | KIS "NF as a table", Kiwoom "37-entry `error_codes` table", DB "full platform/service/WS code tables": **confirmed**. Toss: the overview has a 53-row table (T2 L309–363). Meritz "no consolidated table": true for the portal; the repo has one (M7). |
| [candle-evidence-2026-11-05.md](candle-evidence-2026-11-05.md) L218–222 and G-R1 (L1331–1333): KIS rate limits "not documented"; K12 retries `EGW00201` after 61 s; Kiwoom `1700`–`1702` without numbers | **Confirmed** (same K8 blob). |
| Candle G-R2 (L1336–1338): "On 429, `IGW00201`, `EGW00200` or the Kiwoom `1700`-series, surface `RateLimitExceeded`"; [trade-evidence-2026-11-05.md](trade-evidence-2026-11-05.md) G-R2 (L1471): "surface `RateLimitExceeded`" | **Not what current code does** for body codes: KIS `EGW00201` or Kiwoom `1700` on HTTP 200 → `BrokerRejected`; DB `IGW00201` on 403 → `PermissionDenied`, on 500 → `BrokerUnavailable`; Meritz `EGW00200` on 500 → `BrokerUnavailable`. Only Toss 429 → `RateLimitExceeded`. Meeting those gates needs native-code interpretation (G-E1). |
| Trade G-R1 (L1466–1470): [Meritz] "10/s per API (repo only)" | Recorded with the portal's per-account reading as an unresolved conflict (§7.6 #1, G-E13). |

### 9.2 Where current code differs from the evidence, by broker

Public `fetch_ticker` is enabled only for KIS, Kiwoom and LS
(`_FETCH_TICKER`, `_public_client.py` L88–97). DB and Toss have private
candidate wires only (ADR 0015); Meritz is blocked. The "if enabled" rows
describe what the existing status-only mapping would do.

| Broker | What the code assumes | What the evidence says | Effect today (description only) |
| --- | --- | --- | --- |
| KIS | Throttle = 429, auth failure = 401; `rt_cd` `"0"` | Throttle `EGW00201` in the body, status undocumented; token expiry `EGW00123` on HTTP 200 (legacy); token 1/min | Throttling and token expiry on HTTP 200 surface as `BrokerRejected`; the expired token is not dropped; no token-request pacing |
| Kiwoom | `return_code` integer `0` on quote **and** token; only 401 drops the token | `return_code` may be int or numeric string (client); not in the token field table; `8005` (or `3` + "[8005:…]") on HTTP 200; `1700`–`1702` in the body | A string `"0"` or a token response without `return_code` fails closed; throttle and invalid-token bodies surface as `BrokerRejected`; the rejected token is kept |
| LS | `rsp_cd` `"00000"` required; 429 = throttle | Per-TR TPS only; no over-limit response documented; OAuth failures on HTTP 200 | Matches what is documented; an LS throttle signal is unknown, so its class is unknown |
| DB (if enabled) | Status-only classes; decoder accepts a missing `rsp_cd` | `IGW00201` under **403 or 500**; token codes under 403/400; client-validation codes under 500; `rsp_cd` `"00000"` required (D2 L82–83) | `IGW00201` would surface as `PermissionDenied` (403) or `BrokerUnavailable` (500), not `RateLimitExceeded`; token errors as `PermissionDenied`; a body without `rsp_cd` would decode as success |
| Toss (if enabled) | Status-only classes | 429/401/403/404/500 with documented meanings; one valid token per client | 429, 401, 403 and 500 match; 404 `stock-not-found` and 400 become `TransportError`; `token-revoked` is not distinguished from expiry |
| Meritz (if enabled) | Status-only classes; decoder `rsp_cd` `"0000"` optional; no `shrn_iscd` check | Every error HTTP 500 (with exceptions); throttle `EGW00200`/`EGW00201`; unknown symbol returns `"0000"` with empty values | Every error, including throttle, token and permission, would surface as `BrokerUnavailable`; an unknown symbol might not be detected |

## 10. Gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any native error code is interpreted, the
public error mapping changes, or a further broker is enabled. Broker tags
are in brackets.

### 10.1 Cross-broker

- **G-E1 Native-code interpretation:** whether `BrokerRejected`,
  `PermissionDenied` and `BrokerUnavailable` should be refined from body
  codes into `RateLimitExceeded`, `AuthenticationError`, `InvalidSymbol`,
  etc.: [KIS] `EGW00201`; [Kiwoom] `1700`–`1702`, `8005`, `1901`–`1903`;
  [DB] `IGW00201`, `IGW0012x`; [Meritz] `EGW00200`, `EGW00121`,
  `EGW00123`. ADR 0013 forbids interpreting them today. Needs a maintainer
  decision and a reviewed, pinned code table per broker. Codes must never
  be transferred between brokers (§8.2).
- **G-E2 Throttle transport:** the HTTP status and headers of [KIS]
  `EGW00201`, [Kiwoom] `1700`–`1702` and any [LS] over-limit response.
  Only a sanitized authorized response can show them.
- **G-E3 Token-invalid handling:** whether an in-body token failure
  ([Kiwoom] `8005`, `3` + "[8005:…]"; [KIS] `EGW00123`; [DB] `IGW0012x`
  on 403/400; [Meritz] `EGW00121`/`EGW00123` on 500) should drop the
  cached token as a 401 does today. Dropping it must never trigger an
  automatic resend of the rejected request.
- **G-E4 Token budgets:** [KIS] and [DB] 1 issuance per minute; [Toss]
  `AUTH` 5/s; [Kiwoom] ~2/s (demo, repo note); [LS] and [Meritz] not
  found. [DB] revoke-then-issue spends two 1/min calls. Decide whether the
  library needs a cross-call issuance floor; any pacing is library policy,
  not a publisher limit.
- **G-E5 No automatic retries:** unchanged. Publisher retry, back-off,
  "재시도 가능", `retryable=True` and resend-after-reauth code ([KIS],
  [Kiwoom], [DB], [Toss], [Meritz]; [LS] FAQ advice for paper orders) is
  not a licence to retry. Rate-limit and token errors are returned to the
  caller.
- **G-E6 "No data":** [KIS] an empty result may be a failure envelope with
  a misleading message (K13); [LS] `00000` + no block; [DB] `00000` or
  `2679`; [Meritz] `0000` or `5820`/`5822`, and unknown symbols as `0000`
  with empty values. No decoder may map these to `InvalidSymbol` without
  route-specific evidence.
- **G-E7 Limits as data:** [LS] TPS values changed by notice (2023-10-25,
  2025-11-05); [DB] app limit cut to 1 TPS on IPO days by notice; [Toss]
  "사전 공지 없이 조정". Any hard-coded table must carry its source pin and
  version, and must not be presented as a guarantee.
- **G-E8 Outcome-unknown codes:** [DB] `M205`/`M216` ("처리결과
  확인후"), `IGW50005`, `IGW50011`, `IGW50012`; [Meritz] timeouts per M10.
  Delivery stays UNKNOWN; never retried.

### 10.2 Broker-specific

- **G-E9 [Kiwoom] status type:** confirm `return_code` type (number vs
  string) and key (`return_code` vs `returnCode`) on every route used, for
  quote and token responses.
- **G-E10 [Kiwoom] IP binding:** `8010` means a token may fail when the
  egress IP changes; document before any multi-host use.
- **G-E11 [DB] throttle under 403/500:** `IGW00201` arrives as HTTP 403 or
  500 (D1 L48, L74; D3 L65–67). The current status-only mapping would
  surface it as `PermissionDenied` or `BrokerUnavailable`, never
  `RateLimitExceeded`. Classifying it needs `rsp_cd` from the error body
  (G-E1).
- **G-E12 [Meritz] all-500 errors:** every Meritz error, including
  throttle, token, permission and parameter errors, is HTTP 500 (M3; M7
  L8–9), so status-only mapping turns all of them into
  `BrokerUnavailable`. Any enablement needs broker-specific `rsp_cd`
  interpretation (an ADR change) first, above all before any order path.
- **G-E13 [Meritz] rate-limit scope:** neither "1계좌당 10건/초", all REST
  summed (M4 notice; M12 FAQ), nor "API 당 초당 10건" (M7 L95; M8 L120;
  M5/M11 `x-tps`) may become a fixed global limiter on its own. A limiter
  design must cite both pins, record the conflict (§7.6 #1) and get a
  maintainer decision. Whether both limits apply at once is unverified.
  Likewise, do not treat one code as the only throttle signal until
  `EGW00200` vs `EGW00201` is resolved (§7.6 #2).
- **G-E14 [DB] required `rsp_cd`:** make the DB root `rsp_cd` required
  with exact value `"00000"`, as LS t1102 already is. Evidence: D2
  (`dbsec_sdk/response.py`) L82–83, DP3 examples, D1 L56 / L106–109. Add a
  regression test for a body without `rsp_cd`.
- **G-E15 [Toss] token sharing and limits:** one valid token per client;
  re-issue invalidates every other holder (`token-revoked`). Do not add
  automatic re-issue on `token-revoked`. Do not hard-code the T2 numbers;
  `X-RateLimit-*` at runtime is the publisher's stated source and is
  unverified.
- **G-E16 [LS] TPS and OAuth:** treat `transactionPerSec` as a per-TR
  snapshot; scope key, window, paper limits and over-limit response are
  unknown. OAuth failures may arrive on HTTP 200 with a `code` body; keep
  the token codec's fail-closed shape check. The FAQ's paper-order retry
  advice is not adopted.
- **G-E17 [Meritz] token and headers:** revoke invalidates every token of
  the app key (M3); never call it as a test. The real lifetime (`604800`
  example vs client fallback 43200), issuance limit and re-issue
  invalidation are undocumented. `mac_address` is required (`IGW50024`);
  it must come from explicit configuration, never host discovery (see the
  trade evidence G-H1).

## 11. Not verified

- Any live or paper response, success or error, for any route. No broker
  API request was sent and no limit was measured.
- KIS:
  - every numeric limit (request and token), its window and its holder;
  - the HTTP status, body and headers of `EGW00201`, `EGW00123` and the
    token-issuance limit; whether `EGW00133` exists;
  - any current error catalog (the portal was not retrieved);
  - the "no data" envelope of the routes KTradeLink uses;
  - token re-issue behaviour within one minute and within six hours;
  - the effective client pacing (inferred from scoping, not executed).
- Kiwoom:
  - every numeric quota, the `1702` API groups, real vs paper;
  - the HTTP status and headers of every code, including whether
    "유량 제한(429)" (W10) refers to Kiwoom or to the MCP server;
  - `return_code` type and key per route; generic codes such as `3`;
  - the `au10001` throttle beyond the publisher's demo measurement;
  - same-token re-issue and `8010` IP binding on the real origin.
- LS:
  - the TPS scope key, window and paper limits; the over-limit response;
  - any REST error catalog, the HTTP status of TR errors, and the meaning
    of a missing `rsp_cd`;
  - token issuance limits and re-issue behaviour; the authoritative
    lifetime field (`expire_in` vs `expires_in`);
  - the TR lists in the 2023-10-25 and 2025-11-05 TPS notices (images,
    not read); WebSocket limits (notices only).
- DB:
  - whether the repo catalog (D1, 2026-08-20) matches the portal
    spreadsheet (DP9, not downloaded);
  - which HTTP status each code uses in practice, including `IGW00201`;
  - the revoke limit, the token lifetime (24 h vs "익일 07시") and the
    over-limit token response;
  - the PRICE/MULTIPRICE TPS history (§5.6 #5); which routes return
    `00000` vs `2679` for no data.
- Toss:
  - the actual 403 body on `/api/v1/prices` from a non-allow-listed IP;
  - whether a 401 on Market Data routes uses the T1 `Unauthorized` shape;
  - whether success responses carry `X-RateLimit-*`;
  - how a batch with an unknown symbol is handled; the `edge-*` bodies;
    the `requestId`-missing case.
- Meritz:
  - the throttle code and body (`EGW00200` vs `EGW00201`);
  - the scope of the 10/s limit;
  - `EGW00103` 403 vs 500; `EGW00002` semantics;
  - token lifetime, issuance limit and re-issue invalidation;
  - the `rsp_cd` null-byte corruption.
