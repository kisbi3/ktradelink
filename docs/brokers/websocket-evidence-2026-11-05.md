# Six-broker real-time WebSocket (실시간 시세) evidence — 2026-11-05

- **Scope:** domestic-equity real-time market data over WebSocket: trades
  (체결), quotes / order book (호가) and market-operation notices
  (장운영). Brokers: KIS, Kiwoom REST, LS, DB, Toss and Meritz. Account
  and order-fill feeds (체결통보, 주문체결, 잔고) are **named only**; their
  fields are not recorded. Index, ELW, ETF NAV, program-trading, member
  and condition-search streams are named only. The Shinhan comparison
  stays separate.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No KTradeLink WebSocket client, decoder, subscription
  plan or public `watch_*` method exists, and this file does not authorize
  one.
- **No broker API request or WebSocket connection was made.** No approval
  key, access token, credential, account, HTS ID, MAC value or order was
  used or requested. Only public Git repositories and public
  documentation were fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS: files of the pinned commit, fetched 07:56:08–07:56:50 from
    `raw.githubusercontent.com` by full commit SHA (§2.1).
  - Kiwoom: files of the pinned commit, fetched 07:58:54–07:59:22 the
    same way (§3.1).
  - Archive downloads and the GitHub API were not available in this
    session, so branch heads and commit dates were **not** re-read here;
    the commit dates are those recorded by the earlier audits for the same
    SHAs.
  - LS, DB, Toss, Meritz: **pending** (§4–§7).
- **Pin formats:**
  - Git blob SHAs are `sha1("blob <len>\0" + bytes)` of the retrieved
    bytes, i.e. what `git hash-object` and `git ls-tree` print. Blobs
    already pinned by earlier audits were recomputed and matched (noted
    per row).
  - Line numbers are written "(K5 L97–99)": source K5, lines 97–99 of
    that blob.
  - Web pages have no immutable revision. Their sha256 prefix identifies
    only the copy retrieved at the stated time.
  - Raw copies were kept outside the repository. Sample tokens, approval
    keys, AES key/IV values, account values, app keys, HTS IDs, IPs and
    staff contact data in publisher material are deliberately not copied.
- **Evidence levels:**
  - `field table`: a publisher field or spec table.
  - `publisher example`: a sample request/response or sample code.
  - `publisher client code`: SDK or helper behaviour. It shows how the
    publisher talks to the server; it is **not** a contract.
  - `legacy publisher example`: sample code under a publisher
    repository's `legacy/` directory. Older than the current examples, and
    lower weight than them.
  - `publisher guide`: portal prose outside the API specification or
    field tables.
  - `publisher repo note`: non-code text in a publisher repository.
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- Sample values in publisher examples are illustrative. They are **not**
  authorized fixtures.

## 1. Broker × concern summary

Cell format: short verdict — evidence. `F` field table, `E` publisher
example, `L` legacy publisher example, `C` publisher client code, `N`
publisher repo note, `G` publisher guide, `—` not found.

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Endpoint (real / paper) | `ws://ops.koreainvestment.com:21000` / `…:31000`, path `/tryitout` in current examples; **plain `ws://` only** — E+L | `wss://api.kiwoom.com:10000` / `wss://mockapi.kiwoom.com:10000`, path `/api/dostk/websocket` — F+C | pending | pending | pending | pending |
| Auth model | approval key from `POST /oauth2/Approval` (`appkey`, `secretkey`), sent as `approval_key` in **every** subscribe header; lifetime not documented — E+C | first packet `{"trnm":"LOGIN","token":…}` with the REST access token, then a LOGIN ack — C only; W1 tables show REST `authorization: Bearer` headers instead — F/C conflict | pending | pending | pending | pending |
| Subscription limit | server limit **not found**; client code refuses ">40" but counts subscribe *functions*, not symbols — C | **not found** | pending | pending | pending | pending |
| Trade channel | `H0STCNT0` 실시간체결가 (KRX); `H0NXCNT0` (NXT); `H0UNCNT0` (통합) — E | `0B` 주식체결 — F+E | pending | pending | pending | pending |
| Order-book channel | `H0STASP0` 실시간호가 (KRX); `H0NXASP0` (NXT); `H0UNASP0` (통합); 10 levels — E | `0D` 주식호가잔량, 10 levels; `0C` 주식우선호가 (best bid/ask only) — F+E | pending | pending | pending | pending |
| Market-operation channel | `H0STMKO0` 장운영정보 (KRX), `H0NXMKO0`, `H0UNMKO0`; per symbol, "VI 발동 시와 VI 해제 시" — E | `0s` 장시작시간 (market-wide, coded `215`); `1h` VI발동/해제 — F+E | pending | pending | pending | pending |
| Frame format | control: JSON; data: `flag\|tr_id\|count\|payload`, payload `^`-delimited, `count` records per frame — E | JSON text for control and data; data `trnm` `"REAL"`, `values` keyed by numeric field ids — F+E | pending | pending | pending | pending |
| Encryption | per-subscription AES-256 key and IV in the subscribe ack; data flag `1` = encrypted; which market-data channels are encrypted **not documented** — E+C | none documented (TLS only) — F | pending | pending | pending | pending |
| Heartbeat | server JSON `tr_id` `"PINGPONG"`; client answers with a WebSocket **pong control frame**; interval not documented — C+L | server `PING` (text or `trnm`); client **echoes the same packet**; interval not documented — C only | pending | pending | pending | pending |

## 2. KIS (Korea Investment & Securities)

### 2.1 Pinned sources

All sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362).
The full SHA is `3a9be59a3ed8745720dc3aa9d584bdf3b7830362`; the earlier
audits record the commit date 2026-10-28T00:26:05+09:00 (not re-read
here). Paths are relative to the repository root; `…/` stands for
`examples_llm/domestic_stock/`.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) | `0e722d6f3253033efe3cf2b99845397b2b329655` | WebSocket client: approval key, message shape, ack parsing, PINGPONG, AES decrypt, 40-limit, retry. Same blob as the trade audit's K7. |
| K2 | [`kis_devlp.yaml`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/kis_devlp.yaml) | `9d8615d34ef2135566186d0fee36474ed54de491` | WebSocket origins (L28, L30). Same blob as the capability inventory's K9. Only the origin lines were used. |
| K3 | [`examples_llm/auth/auth_ws_token/auth_ws_token.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/auth/auth_ws_token/auth_ws_token.py) | `543727d09b6d89608670d588d4493b39de8f2588` | "[인증] WebSocket 웹소켓 접속키 발급" request fields |
| K4 | [`…/ccnl_krx/ccnl_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/ccnl_krx/ccnl_krx.py) | `1767fa913d3807846f2d0e01d600b67ddcd589ac` | `H0STCNT0` TR id, `tr_type` docstring, columns (L70–83) |
| K5 | [`…/ccnl_krx/chk_ccnl_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/ccnl_krx/chk_ccnl_krx.py) | `603e540e1d9dd54a3e06b7a50ffb938fac12fb1f` | Column labels (L24–72); ack and frame description (L95–110). Same blob as the trade audit's K13. |
| K6 | [`…/ccnl_nxt/ccnl_nxt.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/ccnl_nxt/ccnl_nxt.py) | `664ce4b0e7924bc09fd93a90526d00a891d2f6e4` | `H0NXCNT0` (L49), columns (L59–73) |
| K7 | [`…/ccnl_nxt/chk_ccnl_nxt.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/ccnl_nxt/chk_ccnl_nxt.py) | `ba6c24ea763fbcb5ec594f2d4bc27b16332bb482` | `CNTG_CLS_CODE` label (L45) |
| K8 | [`…/ccnl_total/ccnl_total.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/ccnl_total/ccnl_total.py) | `3ee4c668fb23e1d8d232d8c07b394d1453802c8f` | `H0UNCNT0` (L52), columns (L62–110) |
| K9 | [`…/ccnl_total/chk_ccnl_total.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/ccnl_total/chk_ccnl_total.py) | `0a6151439fb0992942e1cc2640bda821ceb5ed00` | `CNTG_CLS_CODE` label (L44) |
| K10 | [`…/asking_price_krx/asking_price_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/asking_price_krx/asking_price_krx.py) | `ef306e40f733f71fecc50552781308baf1dc2819` | `H0STASP0` (L55–57), columns (L69–84) |
| K11 | [`…/asking_price_krx/chk_asking_price_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/asking_price_krx/chk_asking_price_krx.py) | `cbae1314e770bb1122984a24cb5d4e6b630e8253` | Column labels (L22–86); ack/frame text (L113–120) |
| K12 | [`…/asking_price_nxt/asking_price_nxt.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/asking_price_nxt/asking_price_nxt.py) | `9ca4ca549c5c9497c6d121fea18ac1f8f677d3de` | `H0NXASP0` (L52), columns (L62–128) |
| K13 | [`…/asking_price_total/asking_price_total.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/asking_price_total/asking_price_total.py) | `f8e97c0bfb6f0bb478ba8ce838f0159de971d399` | `H0UNASP0` (L51), columns (L61–128) |
| K14 | [`…/asking_price_total/chk_asking_price_total.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/asking_price_total/chk_asking_price_total.py) | `6110ea6f09106d39f9cea0e768ee97295ccfb05f` | `KMID_PRC`/`NMID_PRC`/`ANTC_EXCH_CLS_CODE` labels (L83, L86, L89) |
| K15 | [`…/market_status_krx/market_status_krx.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/market_status_krx/market_status_krx.py) | `d2c2f164a851059c542a4d2e4aff57a045969bd6` | `H0STMKO0` (L49), VI wording (L23–25), columns (L59–71) |
| K16 | [`…/market_status_nxt/market_status_nxt.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/market_status_nxt/market_status_nxt.py) | `db2057847bb53d41244b97a5967b158eed3fc312` | `H0NXMKO0` (L50), columns (L60–72) |
| K17 | [`…/market_status_total/market_status_total.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/market_status_total/market_status_total.py) | `ec7d8f9863ca68c825376cee97a1adeccff10799` | `H0UNMKO0` (L50), columns (L60–71) |
| K18 | [`…/ccnl_notice/ccnl_notice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/ccnl_notice/ccnl_notice.py) | `294967abb82167b545a7ba36596c3f253f36a677` | Account feed **name only**: "국내주식 주식체결통보" (L16), TR ids (L56, L58) |
| K19 | [`examples_user/domestic_stock/domestic_stock_functions_ws.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_user/domestic_stock/domestic_stock_functions_ws.py) | `5d3b7cb2edc4c5da9a366b790b5624ad4e1f4634` | Inventory: 25 domestic WS functions, 26 TR ids (titles at L12–2072) |
| K20 | [`README.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/README.md) | `182887151f1fb07e5789a029292ac3e43d3ba9bd` | WS usage snippet (L342–364); troubleshooting note (L398) |
| K21 | [`legacy/websocket/python/ws_domestic_stock.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/websocket/python/ws_domestic_stock.py) | `c292a115926876efc84193911fcf27b38bf1bcea` | **Legacy** message builder, `tr_type` 1/2, multi-record loop, PINGPONG |
| K22 | [`legacy/Sample01/kis_domstk_ws.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/Sample01/kis_domstk_ws.py) | `34b9c5ace597132a601d7b591e5a3534646535fd` | **Legacy** `CCLD_DVSN` code list (L137), URL (L484), date handling (L347) |
| K23 | [`backtester/kis_backtest/providers/kis/websocket.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/kis_backtest/providers/kis/websocket.py) | `27d3cd08fabc153cab0da822cb5fa7247f7c4928` | Second publisher client: sign codes (L114), message (L305–327), decrypt (L436–455), limit (L565–566), keepalive (L576) |

**Missing evidence:**

- No KIS WebSocket **field table**: no types, lengths, units, value
  formats or code lists for any channel. Column *names* and Korean labels
  come from example code only.
- No sample data frame beyond the abbreviated "ex) 0|H0STCNT0|004|…" in
  K5 L102 and L110; no sample ack body.
- No publisher statement of: approval-key lifetime, server-side
  subscription or connection limits, PINGPONG interval, close codes,
  reconnect policy, or which channels are encrypted.
- The KIS developer-portal WebSocket specification was **not** retrieved
  for this audit.

### 2.2 Connection

- **Endpoints.** K2 L28 `ops: "ws://ops.koreainvestment.com:21000" #
  웹소켓` and L30 `vops: "ws://ops.koreainvestment.com:31000" # 모의투자
  웹소켓`. K1 L208 selects `ops` for `prod` and `vops` otherwise; K1 L744
  appends the caller's path.
  - Current examples pass `api_url="/tryitout"` (K5 L123, K20 L361);
    legacy K22 L484 uses `ws://ops.koreainvestment.com:21000/tryitout`.
  - Legacy K21 L148–149 connects to the bare origin without a path.
- **Protocol.** Only `ws://` appears in any pinned KIS source; `wss://`
  is **not found**. **Inference:** the approval key, which travels in
  every subscribe message (below), crosses the network without TLS.
- **Auth model: approval key (웹소켓 접속키).**
  - Issued by `POST {REST origin}/oauth2/Approval` (K1 L518; K3 L29).
  - Body fields: `grant_type` "client_credentials", `appkey`,
    `secretkey` (K1 L507–516; K3 L98–100). The secret is sent under the
    name `secretkey`, not `appsecret`. K3 L105 adds an optional `token`.
  - Response field: `approval_key` (K1 L522). K1 L529 stores it in the
    WebSocket base header; it is **not** a bearer token and is not sent
    in an HTTP upgrade header.
  - **Lifetime: not documented.** K1 L538–541 re-issues when
    `(n2 - _last_auth_time).seconds >= 86400`; Python's
    `timedelta.seconds` is always below 86400, so that branch never runs.
    It is no evidence of a 24-hour lifetime.
- **Heartbeat.** The server sends a JSON message whose `header.tr_id` is
  `"PINGPONG"` (K1 L580, L592). K1 L729–732, K21 L256–259 and K23
  L425–427 answer with `ws.pong(raw)`: a WebSocket **pong control frame**
  carrying the received text, not a text-frame echo.
  - K23 L576 also enables the library's own pings
    (`ping_interval=30, ping_timeout=10`). K1 does not set them.
  - The PINGPONG interval and the penalty for not answering are **not
    documented**.
- **Reconnect.** Client code only: K1 L746–762 reconnects up to
  `max_retries` (default 3, K1 L691) with a 1 s pause and re-sends every
  registered subscription (L750–753). K23 uses 5 retries and 2 s
  (L245, L597–604). No publisher guidance was found.
- **Connections per key / account: not found.** K20 L398 (publisher
  repo note): if "No close frame received" occurs during 실시간 시세,
  check that the HTS ID in `kis_devlp.yaml` is correct. **Inference:** the
  server ties sessions to the HTS ID; the rule itself is not documented.

### 2.3 Subscription model

- **Message shape** (K1 L494–496, L544–565; same in legacy K21 L199–201):

  ```
  {"header": {"approval_key": <key>, "content-type": "utf-8",
              "tr_type": <"1"|"2">, "custtype": "P"},
   "body":   {"input": {"tr_id": <TR id>, "tr_key": <symbol>}}}
  ```

  `custtype` is hard-coded `"P"` in K1 L548.
- **`tr_type`:** `"1"` registers. Unregister is `"2"` in K1 L815
  (`unsubscribe`), legacy K21 L171–193 and K23 L311 ("1"=등록, "2"=해제).
  The example docstrings say instead "구독 등록("1") 또는 해제("0")"
  (K4 L31; same wording in K6 L29, K8 L29, K10 L31, K15 L29). §2.7.
- **`tr_key`:** the 6-digit symbol for market data (examples "005930",
  K5; K4 L32 "종목코드 (빈 문자열 불가)"). Account feeds use another key
  (legacy K22 L274, L299); not recorded here.
- **One symbol per message.** K1 L784–799 sends one message per item,
  pausing `smart_sleep()` after each (K1 L782; module default 0.1 s,
  K1 L57). The per-environment values at K1 L174 and L179 are assigned
  to a local name and do not change the module default.
- **Ack.** JSON. K1 `system_resp` (L569–620) reads `header.tr_id`,
  `header.tr_key`, `header.encrypt`, `body.rt_cd` (`"0"` = OK, L584),
  `body.msg1` and `body.output.iv` / `body.output.key` (L586–589).
  - K5 L97: "정상 응답 시, SUBSCRIBE SUCCESS".
  - An unsubscribe ack has `msg1` beginning with `"UNSUB"` (K1 L590).
  - Legacy K21 L244–246 treats `rt_cd == '1'` as an error. No error-code
    list was found.
- **Max subscriptions.** **No server-side limit was found.** "41건" does
  not occur in any pinned KIS source.
  - K1 L741–742 raises "Subscription's max is 40" when
    `len(open_map.keys()) > 40`, but `open_map` is keyed by the request
    function's name (K1 L635–652, L801–807), so it counts *channel kinds*,
    not symbols.
  - K23 L565–566 raises "최대 구독 수는 40개입니다." on its own
    subscription-name map (K23 L358–368), with the same effect.
- **Venue selection is by TR id**, not by a field: `H0ST…` KRX, `H0NX…`
  NXT, `H0UN…` 통합 (K4, K6, K8, K10, K12, K13, K15–K17).
- **Paper.** KRX functions use the same TR id for `real` and `demo`
  ("웹소켓은 동일한 TR ID 사용", K4 L55–58, K10 L55–57). The NXT and 통합
  functions have no `env_dv` and no demo branch; paper availability for
  them is **not documented**.

### 2.4 Market-data channels

Titles are verbatim from the source headers. Evidence for all rows:
`publisher example`.

| Channel (title verbatim) | TR id | Content | Venue | Frame format | Evidence |
| --- | --- | --- | --- | --- | --- |
| "국내주식 실시간체결가(KRX) [실시간-003]" (K4 L16) | `H0STCNT0` (K4 L55–58) | trade + day snapshot, 47 columns | KRX | `\|`/`^` text, `count` records | K4, K5 |
| "국내주식 실시간체결가 (NXT)" (K6 L16) | `H0NXCNT0` | same 47, `CNTG_CLS_CODE` replaces `CCLD_DVSN` | NXT | same | K6, K7 |
| "국내주식 실시간체결가 (통합)" (K8 L16) | `H0UNCNT0` | same as NXT | 통합 | same | K8, K9 |
| "국내주식 실시간호가 (KRX) [실시간-004]" (K10 L16) | `H0STASP0` | 10-level book + expected match, 63 columns | KRX | same | K10, K11 |
| "국내주식 실시간호가 (NXT)" (K12 L16) | `H0NXASP0` | 65 columns | NXT | same | K12 |
| "국내주식 실시간호가 (통합)" (K13 L16) | `H0UNASP0` | 66 columns | 통합 | same | K13, K14 |
| "국내주식 장운영정보 (KRX) [실시간-049]" (K15 L12) | `H0STMKO0` | per-symbol status, 11 columns | KRX | same | K15 |
| "국내주식 장운영정보(NXT)" (K16 L16) | `H0NXMKO0` | 11 columns | NXT | same | K16 |
| "국내주식 장운영정보(통합)" (K17 L16) | `H0UNMKO0` | 10 columns, **no symbol column** | 통합 | same | K17 |

Named only (K19): 실시간예상체결 `H0STANC0`/`H0NXANC0`/`H0UNANC0`;
실시간회원사 `H0STMBC0`/`H0NXMBC0`/`H0UNMBC0`; 실시간프로그램매매
`H0STPGM0`/`H0NXPGM0`/`H0UNPGM0`; 시간외 실시간호가 `H0STOAA0`,
시간외 실시간체결가 `H0STOUP0`, 시간외 실시간예상체결 `H0STOAC0` (KRX
only); 국내지수 `H0UPCNT0`/`H0UPANC0`/`H0UPPGM0`. Account feed, name
only: "국내주식 주식체결통보" `H0STCNI0` (real) / `H0STCNI9` (paper)
(K18 L16, L56–58).

**`H0STCNT0` trade columns** (K4 L70–83; labels K5 L24–72):

- Symbol `MKSC_SHRN_ISCD` "유가증권 단축 종목코드" — the frame binds
  itself to a symbol.
- Time `STCK_CNTG_HOUR` "주식 체결 시간". Format not documented; the
  abbreviated example `005930^123929^…` (K5 L102) suggests `HHMMSS`
  (**Inference**). Zone not stated.
- Date `BSOP_DATE` "영업 일자". Format not documented. This is the only
  date found in any KIS or Kiwoom trade frame.
- Price `STCK_PRPR` "주식 현재가"; quantity `CNTG_VOL` "체결 거래량";
  cumulative `ACML_VOL`, `ACML_TR_PBMN`.
- Change sign `PRDY_VRSS_SIGN` "전일 대비 부호". A code list appears only
  in client code: "1:상한, 2:상승, 3:보합, 4:하한, 5:하락" (K23 L114).
- Side `CCLD_DVSN` "체결구분" (K5 L46). A code list appears only in a
  legacy example: "1:매수(+), 3:장전, 5:매도(-)" (K22 L137). NXT and 통합
  carry `CNTG_CLS_CODE` "체결구분" instead (K7 L45, K9 L44), with no
  code list.
- Session-like codes: `HOUR_CLS_CODE` "시간 구분 코드" (legacy K22 L159
  gives only "0 : 장중"), `NEW_MKOP_CLS_CODE` "신 장운영 구분 코드",
  `MRKT_TRTM_CLS_CODE` "임의종료구분코드", `MARKET_CLS_CODE` "장 구분
  코드", `TRHT_YN` "거래정지 여부". No code lists.
- Also present: best bid/ask `ASKP1`/`BIDP1` and their sizes,
  day OHLC with their times, 체결강도 `CTTR`, cumulative buy/sell counts
  (`SELN_CNTG_CSNU`, `SHNU_CNTG_CSNU`), `VI_STND_PRC`.
- **No trade id or sequence field.**
- Legacy K21 L103 lists 46 names (no "장 구분 코드"). **Inference:** the
  column list grew; a decoder must not assume a fixed count without a
  versioned spec.

**`H0STASP0` book columns** (K10 L69–84; labels K11 L22–86):

- `MKSC_SHRN_ISCD` symbol; `BSOP_HOUR` "영업 시간" (no format);
  `HOUR_CLS_CODE` "시간 구분 코드". **No date field.**
- `ASKP1`–`ASKP10`, `BIDP1`–`BIDP10` prices; `ASKP_RSQN1`–`10`,
  `BIDP_RSQN1`–`10` sizes; `TOTAL_ASKP_RSQN`, `TOTAL_BIDP_RSQN`;
  after-hours totals `OVTM_TOTAL_*`.
- Expected match `ANTC_CNPR` "예상 체결가", `ANTC_CNQN`, `ANTC_VOL`,
  `ANTC_CNTG_VRSS(_SIGN)`, `ANTC_CNTG_PRDY_CTRT`.
- `STCK_DEAL_CLS_CODE` "주식 매매 구분 코드"; `MID_PRC` "중간가",
  `MIDP_TOTAL_RSQN`, `MIDP_CLS_CODE` "중간가 매수매도 구분";
  `MARKET_CLS_CODE`.
- NXT (`H0NXASP0`) and 통합 (`H0UNASP0`) drop `MID_PRC`, `MIDP_*` and
  `MARKET_CLS_CODE` and add `KMID_*` "KRX 중간가" and `NMID_*` "NXT
  중간가" (K14 L83, L86). 통합 also adds `ANTC_EXCH_CLS_CODE` "예상체결
  거래소구분" (K14 L89).
- Whether a frame is a full 10-level snapshot or a delta is **not
  documented**. **Inference:** a full snapshot, since every level has a
  fixed column.

**`H0STMKO0` market-operation columns** (K15 L59–71):

- `mksc_shrn_iscd`, `trht_yn` 거래정지여부, `tr_susp_reas_cntt`
  거래정지사유내용, `mkop_cls_code` 장운영구분코드, `antc_mkop_cls_code`,
  `mrkt_trtm_cls_code` 임의연장구분코드, `divi_app_cls_code`
  동시호가배분처리구분코드, `iscd_stat_cls_code`, `vi_cls_code`
  VI적용구분코드, `ovtm_vi_cls_code`, `EXCH_CLS_CODE` 거래소구분코드.
- Per symbol; K15 L23–25: "연결된 종목의 VI 발동 시와 VI 해제 시에
  데이터가 수신됩니다." It is **not documented** as a market-wide
  open/close notice.
- **No time field** and no code lists. `H0UNMKO0` has no symbol column
  (K17 L60–71), so a multi-symbol subscription cannot attribute its
  frames from the payload. **Inference:** the frame header carries no
  symbol either (only flag, TR id, count).

### 2.5 Frame encoding

- **Control frames** (acks, PINGPONG) are JSON text (K1 L569–592).
- **Data frames** are text: `<flag>|<tr_id>|<count>|<payload>` (K5
  L101–110; K11 L113–120).
  - flag: "0 암호화 되지 않은 데이터 / 1 암호화된 데이터" (K5 L103).
  - count: "001 인 경우 데이터 건수 1건, 004인 경우 데이터 건수 4건" (K5
    L105).
  - payload: fields separated by `^`. With `count > 1` the records are
    concatenated with `^` and no record separator: "※ 데이터가 많은 경우
    여러 건을 페이징 처리해서 데이터를 보내는 점 참고 부탁드립니다." (K5
    L108–110).
  - K1 L703 dispatches on `raw[0]` being `"0"` or `"1"`.
- **Multi-record handling differs between publisher clients.**
  - Legacy K21 L101–111 walks `count × columns` fields.
  - K1 L715–716 parses the payload as **one** CSV row (`sep="^"`,
    `names=columns`). **Inference:** with `count > 1`, K1 mis-parses the
    frame.
  - K23 L445 leaves the count commented out.
- **Encryption.** AES-256-CBC over base64 text, PKCS#7 unpadding (K1
  L623–628; K5 L98–99 "AES256 IV", "AES256 Key").
  - Key and IV arrive in the subscribe ack `body.output` (K1 L586–589),
    i.e. per subscription. Values are not reproduced here.
  - K1 decrypts when the ack header `encrypt` is `"Y"` (K1 L712–713);
    K23 decrypts when the frame flag is `"1"` (K23 L443–450). §2.7.
  - Legacy K21 decrypts only the account feed (L232–235); its KRX trade
    and book handlers expect flag `0` (L216–228). **Inference:** the
    market-data channels are unencrypted; not documented.
- **Character encoding.** Header `"content-type": "utf-8"` (K1 L495). The
  payload charset is not documented; `tr_susp_reas_cntt` may carry Korean
  text.
- **Unsafe publisher patterns (not to be copied):** K1 logs every sent
  message, including the `approval_key` header, at INFO (L779) and every
  received frame (L698). Legacy K21 prints the approval key (L152) and
  the AES key and IV (L254).

### 2.6 Limits and errors

- Subscription limit: §2.3. No server-side number found.
- Send pacing: client pauses only (K1 0.1 s; K23 L553 0.1 s "rate
  limit"). No WebSocket rate limit was found.
- Errors: `rt_cd` `"0"` OK / `"1"` error with `msg1` text (K1 L584; K21
  L244–246). No WebSocket error-code list, close-code list or
  over-subscription behaviour was found.
- Server-initiated disconnects: not documented. K20 L398 ties "No close
  frame received" to a wrong HTS ID (publisher repo note).

### 2.7 Contradictions and gaps

1. **Unregister code.** `tr_type` `"2"` in client code (K1 L815, K23
   L311) and legacy (K21 L171–193) vs `"0"` in the example docstrings
   (K4 L31 and siblings).
2. **"Subscription's max is 40"** counts channel kinds, not symbols
   (§2.3). The expected "41건" was not found.
3. **Encryption trigger:** ack header `encrypt == "Y"` (K1) vs frame flag
   `1` (K23, K5 L103).
4. **Multi-record parsing:** K1 treats a frame as one row, contradicting
   the K5 L108–110 description (§2.5).
5. **Plain `ws://`** for both environments (K2 L28, L30); no TLS
   endpoint documented.
6. **Path:** `/tryitout` in current examples (K5 L123, K20 L361) vs no
   path in legacy K21 L149.
7. **Side code naming:** `CCLD_DVSN` (KRX) vs `CNTG_CLS_CODE` (NXT,
   통합); codes only in legacy K22 L137.
8. **Market-operation feed:** `H0UNMKO0` lacks a symbol column; none of
   the three has a time field; K15 describes VI events only.
9. **Client defects** (publisher client code, not contracts): the
   approval-key renewal never triggers (K1 L540); `unsubscribe` calls the
   async `send_multiple` without `await` (K1 L815), so no unregister
   message is sent.
10. **Timestamp guess in a legacy example:** K22 L347 prepends the
    local date to the trade time. `BSOP_DATE` exists in the frame; the
    pattern is not acceptable for KTradeLink (§10).

### 2.8 Gates and not-verified items

See §10 (gates tagged [KIS]) and §11.

## 3. Kiwoom REST

### 3.1 Pinned sources

All sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@c7a3d254`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/c7a3d25449ed4b4238bef378780c41103c67b9e9).
The full SHA is `c7a3d25449ed4b4238bef378780c41103c67b9e9`; the trade
audit records the commit date 2026-09-15T15:12:16+09:00 and the re-pin
from `953e5dbf` (same tree). Neither was re-read here.

In the links, `…/실시간시세/` stands for
`examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%A4%EC%8B%9C%EA%B0%84%EC%8B%9C%EC%84%B8/`
(`examples/국내주식/실시간시세/`).

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field tables** and examples: `0B` (L96908–97579), `0C` (L97581–97842), `0D` (L97844–99715), `0s` (L103234–103505), `1h` (L104222–104653), condition search (L29041–), error table (L107018–). Same blob as the trade audit's W1. |
| W2 | [`kiwoom/core/ws_client.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/ws_client.py) | `3c47b80f9ccef211ef9323ce014f1ff710544fd1` | Publisher client: LOGIN, PING echo, framing, keepalive setting |
| W3 | [`kiwoom/core/auth.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/auth.py) | `9026aae207b7e2963c40f06e5e9a2f287a589d28` | WS origins and their environment-variable override (L28–49) |
| W4 | [`kiwoom/core/errors.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/errors.py) | `dd7a8709bccd8a28601c49d26a298d3c92f34e5d` | Auth-retry codes and the WebSocket `CODE=` note (L4–11). Same blob as the trade audit's W7. |
| W5 | [`kiwoom/realtime/packets.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/realtime/packets.py) | `db63bed74f1d8a10be276397a0ee3c47917d0e32` | REG / REMOVE builders (L14–65) |
| W6 | [`kiwoom/realtime/decoders.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/realtime/decoders.py) | `8bcaba9be5ee0f7c8ddea519093b805572f492fb` | REAL decoding; mentions `SYSTEM` frames (L120–123) |
| W7 | [`kiwoom/realtime/stream.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/realtime/stream.py) | `50efaade63fc32ad081ad49eb7560fad9a4e069a` | Several REG packets on one connection (L118); `REG/SYSTEM` frames (L173–174) |
| W8 | [`…/실시간시세/subscribe_domestic_stock_trade_async.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%A4%EC%8B%9C%EA%B0%84%EC%8B%9C%EC%84%B8/subscribe_domestic_stock_trade_async.py) | `d2a0aa37115936c0e4659d1e79d02129dcd0d682` | `0B` REG example (L72–78), LOGIN/PING note (L18) |
| W9 | [`…/실시간시세/subscribe_domestic_stock_order_book_depth_async.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%A4%EC%8B%9C%EA%B0%84%EC%8B%9C%EC%84%B8/subscribe_domestic_stock_order_book_depth_async.py) | `d3a6b5a48b6dbc10f80e6978888c935d22c706b5` | `0D` REG example (L193) |
| W10 | [`…/실시간시세/subscribe_domestic_market_open_time_async.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%A4%EC%8B%9C%EA%B0%84%EC%8B%9C%EC%84%B8/subscribe_domestic_market_open_time_async.py) | `f2a2a62be6b9a2d6bb4fe8b85e68f67e6ea1cf72` | `0s` REG with empty item list (L33–37) |
| W11 | [`README.md`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/README.md) | `018e50aad8156d18f057135a91ce2a15d09ce2d2` | WS example patterns (L338); "WebSocket API는 포함되지 않으며" in Postman (L351) |
| W12 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | Contains no `wss://` or `/websocket` string (0 matches). Same blob as the trade audit's W2. |

**Missing evidence:**

- The `LOGIN` packet, `PING` handling and the LOGIN ack appear **only**
  in publisher client code (W2) and example comments (W8 L18). W1 has no
  LOGIN or PING entry.
- No subscription, group (`grp_no`) or connection limit anywhere in W1,
  W2, W5–W11.
- No WebSocket-specific error or close-code table; W1's 37-entry table
  (L107018–) is shared with REST.
- No code lists for `0B` `9081` 거래소구분, `0D` `215` 장운영구분 (its
  description is empty there), `1h` `9068` VI발동구분 / `9069`
  발동방향구분.

### 3.2 Connection

- **Endpoints.** W1 meta for every 실시간시세 entry: "운영 도메인"
  `wss://api.kiwoom.com:10000`, "모의투자 도메인"
  `wss://mockapi.kiwoom.com:10000`, "URL" `/api/dostk/websocket` (W1
  L96918–96920). W3 L36–39 holds the same defaults.
  - W3 L28–31 and L47–49 let environment variables `W_PRD` / `W_MOCK`
    override the WebSocket origin silently (publisher client code).
- **Protocol:** `wss://` (TLS) in both environments.
- **W1 meta is REST-shaped:** "Method" `POST` and "Format" `JSON` on a
  WebSocket entry; request header rows `api-id`, `authorization`
  ("Bearer" prefix, W1 L96939), `cont-yn`, `next-key`. §3.7.
- **Auth model (client code only).** After connecting, W2 L151–161 sends
  `{"trnm": "LOGIN", "token": <access token>}`, where the token is the
  REST OAuth access token (`self.auth.get_access_token()`, W2 L157).
  - W2 L168–180 then requires a LOGIN ack before any other message; a
    non-zero `return_code` is a login failure.
  - W2 L49–66 retries the login once after refreshing the token when the
    code is in `{8005, 8031, 8103}` (W4 L6). W4 L8–10 notes that the
    WebSocket reports such codes embedded as `CODE=8005` in `return_msg`.
  - Token lifetime and whether a live connection survives token expiry
    are **not documented**.
- **Heartbeat (client code only).** W2 L182–193: a message that is the
  text `PING` or a JSON object with `trnm` `"PING"` (W2 L244–249) is sent
  back unchanged. W2 L206 disables the library keepalive
  (`ping_interval=None`). Interval and timeout: not documented.
- **Reconnect:** none in W2. `iter_messages` ends quietly on a
  `ConnectionClosed*` exception (W2 L105–116, L258–260). No publisher
  guidance found.
- **Connections per token / account: not found.**

### 3.3 Subscription model

- **Request body** (W1 field table; identical rows in `0B`, `0C`, `0D`,
  `0s`, `1h`):

  | Field | 한글명 | Type / length | Description (verbatim) |
  | --- | --- | --- | --- |
  | `trnm` | 서비스명 | String 10, required | "REG : 등록 , REMOVE : 해지" (W1 L96978) |
  | `grp_no` | 그룹번호 | String 4, required | empty (W1 L96984) |
  | `refresh` | 기존등록유지여부 | String 1, required | "등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요" (W1 L96994) |
  | `data` | 실시간 등록 리스트 | LIST | — |
  | `data[].item` | 실시간 등록 요소 | String 100 | "거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)" (W1 L97018) |
  | `data[].type` | 실시간 항목 | String 2, required | "TR 명(0A,0B....)" |

- **Client shape.** W5 L34–44 and W8 L72–78 send `item` and `type` as
  **arrays**: `{"trnm": "REG", "grp_no": "1", "refresh": "1", "data":
  [{"item": ["005930"], "type": ["0B"]}]}`. REMOVE omits `refresh`
  (W5 L56–65). **Inference:** one entry may register several symbols
  and types; W1 types them as single strings.
- **Market-wide types** use an empty item: W1 request examples for `0s`
  and `1h` show `"- item": ""`; W10 L37 sends `"item": []`.
- **Ack.** `trnm` echoes the request; `return_code` "통신결과에대한 코드
  (등록,해지요청시에만 값 전송 0:정상,1:오류 , 데이터 실시간 수신시
  미전송)" (W1 L97074); `return_msg`. The example ack has
  `'return_code': 0` as a number (W1 L97579) while the table types it
  String.
- **Data frames:** `trnm` "등록,해지요청시 요청값 반환 , 실시간수신시 REAL
  반환" (W1 L97094); `data[]` entries with `type`, `name`, `item`,
  `values`.
- **Several REG packets per connection:** W7 L118 "One ``REG`` packet,
  or a list to combine several on one" connection (client code).
- **`grp_no`:** required, 4 characters, meaning and range **not
  documented**; examples always use `"1"`.
- **Venue selection is by item suffix:** bare code KRX, `_NX` NXT, `_AL`
  SOR (W1 L97018). The response `item` is described only as "종목코드".
- **Max subscriptions: not found.**
- **Condition-search streams, named only** (same URL; `trnm` values from
  W1): 조건검색 목록조회 `ka10171` (`CNSRLST`, W1 L29111), 조건검색 요청
  일반 `ka10172`, 조건검색 요청 실시간 `ka10173` (`CNSRREQ`, `search_type`
  "1: 조건검색+실시간조건검색", `stex_tp` "K:KRX", W1 L29637–29647),
  조건검색 실시간 해제 `ka10174`.

### 3.4 Market-data channels

All are `/api/dostk/websocket`, JSON text frames. Evidence: `field table`
+ `publisher example` (W1).

| Channel (title verbatim) | Type id | Content | Venue | Frame format | Evidence |
| --- | --- | --- | --- | --- | --- |
| "주식체결" | `0B` | trade + day snapshot, 43 value fields | item suffix; `9081` "거래소구분" per frame (no code list) | JSON `REAL` | F+E (W1 L96908–97579) |
| "주식우선호가" | `0C` | best ask `27` / best bid `28` only; **no time field** | item suffix | JSON `REAL` | F+E (W1 L97581–97842) |
| "주식호가잔량" | `0D` | 10-level book + expected match + LP sizes + per-venue sizes, 163 value fields | item suffix; KRX/NXT split fields | JSON `REAL` | F+E (W1 L97844–99715) |
| "장시작시간" | `0s` | market-operation code `215`, time `20`, `214` | market-wide (empty item) | JSON `REAL` | F+E (W1 L103234–103505) |
| "VI발동/해제" | `1h` | VI events; item `9001` in values | example registers market-wide | JSON `REAL` | F+E (W1 L104222–104653) |

Named only (W1): 주식기세 `0A`, 주식시간외호가 `0E`, 주식당일거래원 `0F`,
ETF NAV `0G`, 주식예상체결 `0H`, 국제금환산가격 `0I`, 업종지수 `0J`,
업종등락 `0U`, 주식종목정보 `0g`, ELW 이론가 `0m`, ELW 지표 `0u`,
종목프로그램매매 `0w`. Account feeds, name only: 주문체결 `00`, 잔고 `04`.

**`0B` 주식체결 values** (W1 L97140–97577):

- `20` 체결시간 "HHmmss" (W1 L97154). **No date field.** Zone not stated.
- `10` 현재가, `16`/`17`/`18` 시가/고가/저가, `27`/`28` (최우선)매도/매수호가:
  "단위: 원, 부호가 포함된 숫자".
- `15` 거래량 "+는 매수체결,-는 매도체결" (W1 L97214) — the only
  documented per-trade side among KIS and Kiwoom.
- `13` 누적거래량 "단위: 1주"; `14` 누적거래대금 "단위: 백만원".
- `25` 전일대비기호 "1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락" (W1
  L97274).
- `290` 장구분 "1: 장전 시간외 , 2: 장중 , 3: 장후 시간외" (W1 L97354).
- `1315`/`1316` 매도/매수체결량_단건, `1030`/`1031` 매도/매수체결량 (no
  descriptions); `228` 체결강도; `9081` 거래소구분 (W1 L97570, no code
  list; example `'1'`).
- **No trade id or sequence field.** All values are typed String.
- **Inference (examples only):** prices are signed relative to the
  previous close. `10` `'-20800'` with `11` 전일대비 `'-50'` implies a
  reference of 20,850, and `0D` levels flip from `-20800` to `+20900`
  across it. Not documented.

**`0D` 주식호가잔량 values** (W1 L97844–99715):

- `21` 호가시간 "HHmmss" (W1 L98086). **No date field.**
- `41`–`50` 매도호가1–10, `51`–`60` 매수호가1–10 ("단위: 원, 부호가
  포함된 숫자", W1 L98096); `61`–`70` / `71`–`80` 수량 ("단위: 1주");
  `81`–`100` 직전대비; `121`/`125` 총잔량 and `122`/`126` 직전대비.
- Expected match `23`/`24`, `200`/`201`/`238`, `291` "예상체결 시간동안에만
  유효한 값", `292`–`295`, `299`.
- `621`–`640` LP 매도/매수호가수량1–10; `128`/`138` 순매수/순매도잔량;
  `215` 장운영구분 (no description); `216` 투자자별ticker.
- Per-venue sizes: `6044`–`6065` "KRX …잔량", `6066`–`6087` "NXT …잔량"
  (W1 L99116–99546); `6100`–`6115` KRX/NXT 중간가 fields.
- No symbol in `values`; the entry's `item` carries it. No sequence.
  Snapshot vs delta: **not documented**.

**`0s` 장시작시간 values** (W1 L103234–103505):

- `215` 장운영구분, verbatim (W1 L103480): "0 : 장시작전 알림(8:40~), 3 :
  장시작(09:00), 2 : 장마감 알림(15:20~), 4 : 장마감(15:30), 8 :
  정규장마감(거래소 수신시 15:30 이후), 9 : 전체장마감(거래소 수신시 18:00
  이후), a : 시간외 종가매매 시작(15:40), b : 시간외 종가매매 종료(16:00), c
  : 시간외 단일가 시작(16:00), d : 시간외 단일가 종료(18:00), e : 선옵
  장마감전 동시호가 종료, f : 선물옵션 장운영시간 알림(조기개장 상품), o :
  선옵 장시작, s : 선옵 장마감전 동시호가 시작, P : NXT 프리마켓 시작 알림,
  Q : NXT 프리마켓 종료 알림, R : NXT 메인마켓 시작 알림, S : NXT 메인마켓
  종료 알림, T : NXT 에프터마켓 단일가 시작 알림, U : NXT 에프터마켓 시작
  알림, V : NXT 에프터마켓 종료 알림".
- `20` 체결시간 "HHmmss"; `214` 장시작예상잔여시간 "HHmmss".
- Codes are case-sensitive single characters mixing equity, derivatives
  and NXT events. No date.

**`1h` VI발동/해제 values:** `9001` 종목코드, `302` 종목명, `9068`
VI발동구분, `1225` VI적용구분 "정적/동적/동적+정적", `1221` VI발동가격,
`1223` 매매체결처리시각 / `1224` VI해제시각 "HHmmss", `9069`
발동방향구분, `1279` "Extra Item" (W1 L104222–104653). Code lists for
`9068`/`9069`: not documented.

### 3.5 Frame encoding

- **JSON text** for LOGIN, PING (JSON or plain text), acks and data (W1
  "Format" `JSON`; W2 L224–237 parses text as JSON and falls back to the
  raw string).
- `data` is a list (W1); W6 L95–113 decodes every entry. **Inference:** a
  frame may carry several entries; every W1 example shows one.
- `values` is a JSON **object** keyed by numeric field-id strings in every
  example, while W1 types it "LIST" (W1 L97140). §3.7.
- Absent values are empty strings in the examples (`'851': ''`).
- **Encryption:** none documented. TLS only.
- **Character encoding:** W2 L225–226 decodes bytes as UTF-8 and L255
  sends with `ensure_ascii=False`. Not stated in W1.
- Frames named `SYSTEM` are mentioned only in client code (W6 L122–123,
  W7 L174). Their fields are not documented.

### 3.6 Limits and errors

- Subscription and connection limits: **not found**.
- Rate limit: W1 error codes `1700` "허용된 API 요청 개수를 초과하였습니다.
  유량={?}, API ID={?}", `1701`, `1702` are shared with REST; whether
  they apply to REG packets is **not documented**.
- Ack errors: `return_code` `1` with `return_msg` (W1 L97074). Auth codes
  inside WS messages: client comment only (W4 L10).
- Over-subscription behaviour, server-initiated close codes and idle
  timeouts: **not documented**.

### 3.7 Contradictions and gaps

1. **Auth:** W1 header rows (`authorization: Bearer …`, `api-id`,
   `cont-yn`, `next-key`) vs the client's LOGIN packet (W2 L155–158).
   LOGIN is not in W1.
2. **Unregister:** W1 says `REMOVE`; the example comments say
   `등록("0"이면 해제)` (W8 L73, W9 L193, W10 L33).
3. **`item`/`type`:** String in W1; arrays in W5 and W8.
4. **`values`:** "LIST" in W1; an object in every example.
5. **`return_code`:** String in W1; number `0` in the example ack.
6. **Malformed request examples:** W1 L97578 shows `"data": null`
   followed by `"- item"` / `"- type"` keys (a flattened table, not
   valid request JSON).
7. **Example time vs code:** `0s` example `'215': 'b'` (시간외 종가매매
   종료, 16:00) with `'20': '170000'`; `0B` example `'20': '165208'` with
   `'290': '2'` (장중). **Inference:** example values are illustrative
   only.
8. **Field-description gaps:** `0D` `215` has no description while `0s`
   `215` has a list; `9081` has no code list.

### 3.8 Gates and not-verified items

See §10 (gates tagged [Kiwoom]) and §11.

## 4. LS Securities

<!-- pending: merged from sections/ls-db.md -->

**Pending.** Written separately; to be merged.

## 5. DB Securities

<!-- pending: merged from sections/ls-db.md -->

**Pending.** Written separately; to be merged.

## 6. Toss Securities

<!-- pending: merged from sections/toss-meritz.md -->

**Pending.** Written separately; to be merged.

## 7. Meritz Securities

<!-- pending: merged from sections/toss-meritz.md -->

**Pending.** Written separately; to be merged.

## 8. Cross-broker comparison

LS, DB, Toss and Meritz columns are **pending**.

### 8.1 Transport and session

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| TLS | no (`ws://`) | yes (`wss://`) | pending | pending | pending | pending |
| Credential on the socket | approval key in every subscribe header | REST access token in a LOGIN packet | pending | pending | pending | pending |
| Separate key issuance | yes, `/oauth2/Approval` | no (REST token reused) | pending | pending | pending | pending |
| Heartbeat answer | pong control frame | echo text packet | pending | pending | pending | pending |
| Venue selection | TR id per venue | item suffix | pending | pending | pending | pending |
| Documented subscription limit | none (client 40, miscounted) | none | pending | pending | pending | pending |

### 8.2 Data fields

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Trade time | `STCK_CNTG_HOUR`, format undocumented | `20` "HHmmss" | pending | pending | pending | pending |
| Date in trade frame | `BSOP_DATE` 영업 일자 | none | pending | pending | pending | pending |
| Aggressor side | `CCLD_DVSN` / `CNTG_CLS_CODE`; codes legacy only | sign of `15` (documented) | pending | pending | pending | pending |
| Trade id / sequence | none | none | pending | pending | pending | pending |
| Book depth | 10 | 10 | pending | pending | pending | pending |
| Book time / date | `BSOP_HOUR` / none | `21` "HHmmss" / none | pending | pending | pending | pending |
| Symbol in payload | yes (except `H0UNMKO0`) | entry `item` | pending | pending | pending | pending |
| Multi-record frames | yes, `count` field | `data` list (inference) | pending | pending | pending | pending |

### 8.3 What a common `watch_*` surface could rely on

Everything in this subsection is **Inference:** from KIS and Kiwoom only;
it must be revisited when §4–§7 are merged. No `watch_*` method is
proposed.

- **Common shape.** Both brokers follow connect → authenticate →
  subscribe (symbol, channel) → server push → unsubscribe, with a
  server-initiated heartbeat that the client must answer. The answer
  mechanism differs (pong control frame vs echoed text), so heartbeat
  handling must be broker-specific.
- **`watch_trades`.** Both feeds carry one price and one quantity per
  record, so a per-record trade is plausible, but neither source says a
  record is exactly one execution. Neither has a trade id or sequence:
  duplicates and gaps (including across reconnects) cannot be detected.
  A common surface could not promise completeness or de-duplication.
- **Side.** Only Kiwoom documents a per-trade side (sign of `15`). KIS
  side codes exist only in legacy code. A common `side` would have to be
  optional and `None` for KIS until verified.
- **Time.** Both give time of day only. KIS adds `BSOP_DATE`; Kiwoom
  gives no date and neither states a zone. A common `timestamp` would
  have to stay `None` unless a verified trading date is supplied, per the
  market-data spec's rule against inventing timestamps.
- **`watch_order_book`.** Both expose 10 levels per side with sizes and
  totals in fixed fields. **Inference:** frames are full snapshots, not
  deltas; this is undocumented for both. Kiwoom prices carry signs whose
  meaning is undocumented.
- **`watch_ticker`.** Both trade feeds carry day OHLC, cumulative volume
  and best bid/ask, so a ticker could be derived from the trade feed;
  field semantics (signs, units) differ.
- **Venue.** KIS selects venue by TR id; Kiwoom by symbol suffix, with
  KRX/NXT split fields inside `0D`. A common surface must keep venue
  explicit and never merge KRX, NXT and integrated streams.
- **Market operation.** KIS `H0STMKO0` is per-symbol and VI-oriented;
  Kiwoom `0s` is market-wide with a coded event list. They are not the
  same concept.

## 9. Relation to existing repository documents

None of the files below is edited by this change. Differences are
recorded here only.

| Document and claim | This audit |
| --- | --- |
| [capability inventory](capability-inventory-2026-11-05.md) row 11, KIS: `H0STCNT0` 체결, `H0STASP0` 호가; `ws://ops.koreainvestment.com:21000` (paper :31000) · EX · K9, K10 | **Confirmed** at the same blobs (K2, K4, K10). Adds NXT/통합 variants, `H0STMKO0`/`H0NXMKO0`/`H0UNMKO0` and the `/tryitout` path (§2.2, §2.4). |
| Same file, note: "K9 lists WebSocket origins as plain `ws://` … a transport-security gate before any WS work" | **Confirmed**; adds that the approval key is sent in every subscribe message (§2.2, G-W3). |
| Same row, Kiwoom: `0B`, `0D`; `wss://api.kiwoom.com:10000` `/api/dostk/websocket` · FT | **Confirmed** (W1 L96918–96920). Adds `0C`, `0s`, `1h` and the client-only LOGIN packet (§3.2). |
| Same file, Kiwoom note: no REST market-calendar API; "only WS `0s` 장시작시간" | **Confirmed**; the `215` code list is recorded verbatim in §3.4. |
| [trade evidence](trade-evidence-2026-11-05.md) §2.5: `H0STCNT0` `CCLD_DVSN` "체결구분" with "no value list in K13" | **Confirmed** for that blob (K5). A legacy list exists: "1:매수(+), 3:장전, 5:매도(-)" (K22 L137, legacy); NXT/통합 use `CNTG_CLS_CODE` (§2.4). |
| Same file §3.5: `0B` field `15` "+는 매수체결,-는 매도체결" (W1 L97214) | **Confirmed** at the same line. |
| [order-book evidence](order-book-evidence-2026-11-05.md): no WebSocket channel cited; Kiwoom REST price sign meaning "not stated"; KIS REST book has no symbol echo | `0D` prices are also "부호가 포함된 숫자" with no stated meaning (§3.4). The KIS WS book **does** carry `MKSC_SHRN_ISCD`, unlike the REST route. |
| [kis-market-data.md](kis-market-data.md) L43–45: KIS says to use WebSocket for real-time feeds | Consistent; the underlying KIS statement was not re-verified here. |
| [market-data spec](../specifications/market-data-v0.1-draft.md) L266: "no WebSocket streaming" | Unchanged. Any `watch_*` method needs a spec change and a maintainer decision first (§10). |
| [candle evidence](candle-evidence-2026-11-05.md) L872: Toss WebSocket text "국내는 통합 시세(KRX+NXT)만 노출합니다" | Toss: pending (§6). |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any WebSocket client, decoder,
subscription plan or public `watch_*` method is written. Broker tags are
in brackets; untagged gates apply to all six.

- **G-W1 — No connection without authorization.** No WebSocket
  connection, approval-key issuance or LOGIN to any broker, real or
  paper, without a **separate explicit authorization** naming the broker,
  environment and purpose. No WebSocket connections in CI.
- **G-W2 — Approval keys are credentials: never logged.** KIS approval
  keys, Kiwoom LOGIN tokens, KIS AES keys and IVs, and whole subscribe
  messages that contain them must never appear in logs, errors, panics,
  fixtures, screenshots or review material. Publisher examples that log
  them (K1 L698, L779; K21 L152, L254) are not safe patterns.
- **G-W3 — Transport security [KIS].** KIS documents only plain `ws://`.
  Whether to connect without TLS is a maintainer decision; KTradeLink
  must not silently try `wss://`, nor silently fall back to `ws://`.
- **G-W4 — Decryption [KIS].** Decrypt only on a documented trigger. The
  ack `encrypt` flag and the frame flag disagree in publisher code; an
  unknown or inconsistent flag fails closed.
- **G-W5 — Explicit environment.** No silent LIVE/PAPER fallback and no
  environment-variable endpoint override (Kiwoom W3 L28–49).
- **G-W6 — Timestamps.** Time-of-day fields (`HHMMSS`) are not
  timestamps. No date guessing from the local clock (as legacy K22 L347
  does); KIS `BSOP_DATE` format and both brokers' zones are unverified.
- **G-W7 — Ordering and gaps.** No trade id or sequence [KIS, Kiwoom]:
  a reconnect is a gap and must be surfaced. No automatic REST backfill
  merged into a stream without a maintainer decision.
- **G-W8 — Framing [KIS].** Honour the `count` field; a field count that
  is not `count × columns` fails closed. Column lists differ by venue and
  have changed over time; pin them to a versioned source.
- **G-W9 — Signs and side.** [Kiwoom] the sign of `15` is the only
  documented side; price signs are undocumented and must not be dropped
  or `abs()`-ed silently. [KIS] side codes are legacy-only.
- **G-W10 — Limits.** Client-side caps (KIS "40") are not server limits.
  Over-subscription behaviour is unknown; do not probe it live.
- **G-W11 — Reconnect and re-auth.** Reconnect and re-subscribe only
  market-data channels, with bounded back-off; never re-issue keys in a
  tight loop, and never re-send anything order-related. Account and
  order-fill feeds (KIS `H0STCNI0`/`H0STCNI9`, Kiwoom `00`/`04`) are out
  of scope and need their own authorization.
- **G-W12 — Venue.** KRX, NXT and 통합/SOR streams stay separate and
  labelled; no merging.
- **G-W13 — Unknown frames.** Unknown message kinds (e.g. Kiwoom
  `SYSTEM`, unknown KIS `tr_id`) are reported without payload and never
  treated as success.

## 11. Not verified

- Any live or paper WebSocket frame, ack, heartbeat or close for any
  broker. No connection was made.
- Entitlements, real/paper parity and redistribution rights.
- KIS:
  - approval-key lifetime, reuse across connections, and issuance limits;
  - server-side subscription and connection limits; whether "41" or "40"
    is a server rule;
  - PINGPONG interval and timeout; close codes; reconnect rules;
  - which channels are encrypted;
  - formats of `STCK_CNTG_HOUR`, `BSOP_DATE`, `BSOP_HOUR`; time zone;
  - code lists for `CCLD_DVSN`, `CNTG_CLS_CODE`, `PRDY_VRSS_SIGN`,
    `HOUR_CLS_CODE`, `MARKET_CLS_CODE` and all `H0STMKO0` codes;
  - whether a trade record is exactly one execution; snapshot vs delta
    for the book;
  - paper availability of NXT and 통합 TR ids;
  - the role of the HTS ID in WebSocket sessions.
- Kiwoom:
  - the LOGIN packet and ack (client code only), token lifetime on a live
    socket, and PING interval;
  - subscription, group and connection limits; `grp_no` semantics;
  - array vs string `item`/`type`; multi-entry `data` frames;
  - meaning of price signs; code lists for `9081`, `0D` `215`, `9068`,
    `9069`; time zone;
  - whether `1700`–`1702` apply to REG packets; close codes;
  - `_AL` (SOR) frames and how `9081` labels them.
- LS, DB, Toss, Meritz: pending (§4–§7).
