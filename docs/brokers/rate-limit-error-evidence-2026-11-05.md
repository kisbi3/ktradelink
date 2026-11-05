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
  repositories (and, for §4–§7, public documentation pages) were fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS: `git fetch` of the pinned SHA from `github.com` at 07:44:49.
  - Kiwoom: `git fetch` of the pinned SHA at 07:44:59, and of the older pin
    `953e5dbf` at 07:52:22 to confirm the shared tree (§3.1).
  - `git ls-remote` at 07:45: both pinned SHAs were still the `main` heads.
  - LS and DB (§4, §5): *pending*.
  - Toss and Meritz (§6, §7): *pending*.
- **Re-hash:** every KIS and Kiwoom blob SHA in §2.1 and §3.1 was recomputed
  from the retrieved bytes with a separate script before this file was
  written; all matched the tree entries.
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
  - `publisher guide`: portal prose outside the field tables.
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
| Request limit | **no number** in the current pin; "초당 거래건수 초과" names `EGW00201`, paper limit "낮습니다" (N); client pacing 0.05 s real / 0.5 s paper intended (C); "1초당 20건 제한" (L) | **no number** in the pin; per-API / total / group quotas exist by code `1700`/`1701`/`1702` (F) | *pending* | *pending* | *pending* | *pending* |
| Token issuance limit | "토큰 재발급 - 1분당 1회 발급됩니다" (N); re-issue within 6 h returns the same token (C comment); `EGW00133` **not found** | **no documented number**; "초당 ~2회, 2026-08-18 demo 실측", rejected as `1700` (N) | *pending* | *pending* | *pending* | *pending* |
| Throttle signal | `msg_cd` `EGW00201` (N, C); HTTP status, headers and back-off interval **not documented** | `return_code` `1700`–`1702` (F); HTTP status **not documented**; one repo note says "유량 제한(429)" (N, ambiguous, §3.6) | *pending* | *pending* | *pending* | *pending* |
| Token-expired signal | `msg_cd` `EGW00123` with HTTP 200 (L only); no current source | `8005` "Token이 유효하지 않습니다" (F); also HTTP 401, or top-level code 3 with "[8005:…]" in `return_msg` (C) | *pending* | *pending* | *pending* | *pending* |
| Success-status field | `rt_cd` string `"0"` (C, E); failure example `"1"` (E) | `return_code` JSON number `0` in REST examples (E); **no REST field table**; client accepts int or numeric string (C) | *pending* | *pending* | *pending* | *pending* |
| HTTP status meaningful | client treats any non-200 as failure and does not parse the body (C); which statuses occur is **not documented** | business errors are HTTP 200 (C comment); 401 triggers re-auth (C); bodies of ≥400 parsed for `return_code` (C) | *pending* | *pending* | *pending* | *pending* |
| Error catalog available | **not found** in the repo (portal not retrieved); scattered codes only | **yes**: 37-row `error_codes` table (F) | *pending* | *pending* | *pending* | *pending* |

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

*pending — written in a separate section file (§4.1–§4.8) and merged later.*

## 5. DB Securities

*pending — written in a separate section file (§5.1–§5.8) and merged later.*

## 6. Toss Securities

*pending — written in a separate section file (§6.1–§6.8) and merged later.*

## 7. Meritz Securities

*pending — written in a separate section file (§7.1–§7.8) and merged later.*

## 8. Cross-broker comparison

### 8.1 Signals side by side

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Numeric request quota in the pinned sources | none (legacy "1초당 20건") | none | *pending* | *pending* | *pending* | *pending* |
| Throttle carried in | body `msg_cd` `EGW00201`; status unknown | body `return_code` `1700`–`1702`; status unknown | *pending* | *pending* | *pending* | *pending* |
| Throttle headers | not found | not found | *pending* | *pending* | *pending* | *pending* |
| Token-issuance budget | 1/min (repo note) | ~2/s demo, measured by publisher (repo note) | *pending* | *pending* | *pending* | *pending* |
| Token-invalid signal | `EGW00123` (legacy, HTTP 200) | `8005` (table); HTTP 401 (client) | *pending* | *pending* | *pending* | *pending* |
| Re-issue returns same token? | within 6 h (client comment) | while valid (repo note) | *pending* | *pending* | *pending* | *pending* |
| Success value and type | `rt_cd` `"0"` string | `return_code` `0` number (examples) | *pending* | *pending* | *pending* | *pending* |
| Business errors on HTTP 200? | yes for `rt_cd != "0"` bodies (client) | yes (client comment) | *pending* | *pending* | *pending* | *pending* |
| Error catalog | not found | 37 rows | *pending* | *pending* | *pending* | *pending* |

### 8.2 What a common mapping could and could not rely on

All points are **Inference:** from the KIS and Kiwoom evidence only; the
other four brokers are pending.

- **Inference:** a common `RateLimitExceeded` **cannot** rely on HTTP 429
  for KIS or Kiwoom. Neither pin documents 429; both name a body code
  (`EGW00201`, `1700`–`1702`). A mapping would need per-broker native-code
  tables, which ADR 0013 deliberately does not interpret today.
- **Inference:** a common `AuthenticationError` **cannot** rely on HTTP 401
  alone. Kiwoom's own client handles both 401 and in-body `8005` (also
  wrapped in a generic code 3); KIS evidence is a legacy HTTP-200 sample.
- **Inference:** `BrokerRejected` ("HTTP 200 with a non-success status")
  is the only class whose trigger both brokers' evidence supports, and it
  hides throttling and token expiry from the caller.
- **Inference:** a common "retry after" value **cannot** be derived: no
  headers, and KIS sources disagree on the window (1 s vs 60–61 s).
- **Inference:** a native code would not change the delivery question.
  Every body-coded error is `RESPONSE_RECEIVED`; whether the broker acted on
  the request is still not shown by the code, so no class can imply that a
  resend is safe.
- **Inference:** "no data" cannot be mapped uniformly even within KIS
  (failure in K13, success in legacy K20).

## 9. Relation to existing code and docs

Description only; nothing below is changed by this file. Code references
are to `main` at `a5d2639e1b555b54c7a96652432cc2c3bf141fb7`.

| Code / document and its current assumption | This audit |
| --- | --- |
| `src/ktradelink/_public_client.py` L89–90: KIS quote status `rt_cd` must be the string `"0"` | **Matches** K2 L353 and K13 (`"1"` for failure, a string). |
| `_public_client.py` L91–93 and ADR 0013 decision 6: Kiwoom `return_code` must be the integer `0` (not a boolean) | **Matches** every REST example (W1, e.g. L1820). **Differs** from the publisher client's statement that the server sends an int **or a numeric string** (W3 L33–34) and from the WebSocket field tables' `String` type. A string `"0"` would fail closed as `ResponseSchemaError("quote_status_invalid")`. Two REST TRs use `returnCode` (not `ka10001`). |
| `_public_client.py` L257–278: any other status value → `BrokerRejected`; message and code not exposed | **Consistent** with both brokers sending business errors on HTTP 200 (K2, W4 L104). It also means a KIS `EGW00201` or Kiwoom `1700` delivered on HTTP 200 surfaces as `BrokerRejected`, **not** `RateLimitExceeded`, and a Kiwoom `8005` (or `3` + "[8005:…]") on HTTP 200 surfaces as `BrokerRejected`, **not** `AuthenticationError`. |
| `src/ktradelink/errors.py` L17–20, L113–126 and `_https_transport.py` `_http_kind` L412–425: 401/403/429/5xx carry generic HTTP meaning | **Consistent** with the docstring's own caveat. Neither KIS nor Kiwoom documents 429 for throttling; only the Kiwoom client documents 401 for auth. |
| `_public_client.py` `_drop_token` L456–464 and ADR 0013 decision 7: only a quote **401** drops the cached token | **Gap:** Kiwoom's client re-authenticates on in-body `8005`/`8031`/`8103` as well (W4 L84–96). An in-body token failure would leave KTradeLink's cached token in place until its expiry margin, so later calls repeat the same rejection. The same applies to KIS `EGW00123` if it arrives on HTTP 200 (legacy K19). |
| `src/ktradelink/_token_codec.py` L248–256: Kiwoom token response must carry `return_code` int `0` | **Stricter than the evidence.** The `au10001` field table does not list `return_code`; only the (invalid-JSON) example has it (W1 L163), and the publisher client accepts its absence (W5 L137). A real response without it would fail closed (`ResponseSchemaError`, stage `token`). |
| `_token_codec.py` L241–247: KIS token uses `access_token_token_expired` only; zone supplied by `kis_expiry_timezone` | **Matches** K2 L78. K5 also lists `expires_in` (seconds), which the library does not use; their agreement is unverified. |
| `_token_codec.py` L279: Kiwoom expiry in KST | **Matches** W5 L21, L325–327. |
| `_public_client.py` L413–426, ADR 0013 decision 7: at most one token request per call; after a rejected token response the next call sends another | **No pacing between calls.** KIS documents 1 token per minute (K1 L390); the Kiwoom repo note measured ~2/s on demo (W8). Repeated calls after a token failure could hit those budgets; the library would surface the result only by HTTP status. |
| `BrokerClient` docstring L305–308 and ADR 0013 decision 8: "two clients using one app key can invalidate each other's tokens" | **Not supported for KIS or Kiwoom by these pins**: K2 says a request within 6 h keeps the existing token; W8 says Kiwoom returns the same token while one is valid. The caution is conservative and harmless; the evidence for it lies with other brokers (ADR 0015 for DB/Toss). Kiwoom `8010` adds an IP binding that the docstring does not mention. |
| `src/ktradelink/_diagnostics.py` L36–37: diagnostics read only `rsp_cd`/`error` and `rsp_msg`/`error_description` | **Does not cover** KIS `msg_cd`/`msg1` or Kiwoom `return_code`/`return_msg`. (Diagnostics are off on the public path, ADR 0013.) |
| No retry anywhere (`errors.py` L121–126; `_https_transport.py` L503–506, L555) | **Consistent** with AGENTS.md. Publisher retries (K8 61 s × 3; W4 resend-after-reauth including POST) are not adopted (§2.5, §3.5). |
| [kiwoom-market-data.md](kiwoom-market-data.md) L50–53: portal quota "orders 5/s and inquiries 5/s"; paper "additional per-TR restrictions" | **Not in this pin set**; not re-verified. The same paragraph ends "must not be copied as a universal KIS quota", which reads as if it meant Kiwoom. |
| [kis-market-data.md](kis-market-data.md) L65–66: "KIS per-TR rate limits must be checked in the up-to-date vendor portal; never assume a generic per-second limit" | **Consistent**: the repo has no per-TR numbers; the portal was not retrieved here. |
| [capability-inventory-2026-11-05.md](capability-inventory-2026-11-05.md) row 7 (L35), KIS "token 1/min; `EGW00201` = TPS exceeded; paper \"lower\", no numbers"; Kiwoom "codes `1700`/`1701`/`1702` … no numbers" | **Confirmed** at the same blobs. Added here: the Kiwoom repo note's measured `au10001` throttle (~2/s, demo, W8), and the KIS 60/61-second retry wait (K8, K9). |
| Same inventory, row 8 (L36): KIS catalog "NF as a table"; Kiwoom "37-entry `error_codes` table" | **Confirmed** (§2.4, §3.4). |
| [candle-evidence-2026-11-05.md](candle-evidence-2026-11-05.md) L218–222 and G-R1 (L1331–1333): KIS rate limits "not documented"; K12 retries `EGW00201` after 61 s; Kiwoom `1700`–`1702` without numbers | **Confirmed** (same K8 blob). |
| Candle G-R2 (L1336–1338): "On 429, `IGW00201`, `EGW00200` or the Kiwoom `1700`-series, surface `RateLimitExceeded`"; [trade-evidence-2026-11-05.md](trade-evidence-2026-11-05.md) G-R2 (L1471): "surface `RateLimitExceeded`" | **Not what current code does** for body codes: a KIS `EGW00201` or Kiwoom `1700` on HTTP 200 becomes `BrokerRejected`, and a body code on HTTP 5xx becomes `BrokerUnavailable`. Meeting those gates needs native-code interpretation (G-E1), which ADR 0013 excludes today. |
| ADR 0015 (DB/Toss) and the LS/DB/Toss/Meritz rows | *pending* (§4–§7). |

## 10. Gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any native error code is interpreted or the
public error mapping changes. Broker tags are in brackets.

- **G-E1 Native-code interpretation:** whether `BrokerRejected` should be
  refined into `RateLimitExceeded`, `AuthenticationError`, `InvalidSymbol`
  etc. from body codes ([KIS] `EGW00201`; [Kiwoom] `1700`–`1702`, `8005`,
  `1901`–`1903`). ADR 0013 currently forbids interpreting them. Needs a
  maintainer decision and a reviewed code table per broker.
- **G-E2 Throttle transport:** the HTTP status and headers of [KIS]
  `EGW00201` and [Kiwoom] `1700`–`1702`. Only a sanitized authorized
  response can show it.
- **G-E3 Token-invalid handling:** whether an in-body token failure
  ([Kiwoom] `8005`, `3` + "[8005:…]"; [KIS] `EGW00123`) should drop the
  cached token as a 401 does today. Dropping it must never trigger an
  automatic resend of the rejected request.
- **G-E4 Kiwoom status type:** confirm `return_code` type (number vs
  string) and key (`return_code` vs `returnCode`) on every route KTradeLink
  uses, for both quote and token responses.
- **G-E5 Token budgets:** [KIS] 1 issuance per minute; [Kiwoom] ~2/s
  (demo, repo note). Decide whether the library needs a cross-call issuance
  floor; any such pacing is library policy, not a publisher limit.
- **G-E6 No automatic retries:** unchanged. Publisher retry, back-off and
  resend-after-reauth code is not a licence to retry. A rate-limit or
  token error is returned to the caller.
- **G-E7 "No data":** [KIS] an empty result may be a failure envelope with
  a misleading message (K13). Any decoder must not map it to
  `InvalidSymbol` without route-specific evidence.
- **G-E8 IP binding:** [Kiwoom] `8010` means a token may fail when the
  egress IP changes; document before any multi-host use.
- LS, DB, Toss and Meritz gates: *pending*.

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
- LS, DB, Toss, Meritz: *pending*.
