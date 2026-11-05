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
  used or requested, and DB's state-changing `DisconnectSession` was not
  called. Only public Git repositories and public
  documentation were fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS: files of the pinned commit, fetched 07:56:08–07:56:50 from
    `raw.githubusercontent.com` by full commit SHA (§2.1).
  - Kiwoom: files of the pinned commit, fetched 07:58:54–07:59:22 the
    same way (§3.1).
  - Archive downloads and the GitHub API were not available for the KIS
    and Kiwoom retrieval, so their branch heads and commit dates were
    **not** re-read; the dates are those recorded by the earlier audits
    for the same SHAs.
  - LS portal pages, JSON guides and console script: 07:54:49–07:59:51
    (§4.1).
  - DB repository at a fixed commit, fetched 08:00:39; DB portal JSON
    08:01:37–08:03:11 (§5.1).
  - Toss portal documents: 07:54:46–07:55:27 (§6.1).
  - Meritz portal pages and notice: 07:57:09–07:59:00; the Meritz
    repository at a fixed commit, re-cloned 07:55:53 (§7.1).
- **Re-hash before merge:** the section authors recomputed every pin from
  their retrieved copies. At merge, 14 pins were independently recomputed
  (LS L1, L5, L12, L16; DB D1, D6, DP4-S00; Toss T2, T3, T4; Meritz M1,
  M4, M7, M11) and all matched; selected quotations (LS `tr_type` and
  session/subscription notices, DB limits and `10011`, Toss limits and
  FAQ L9, Meritz `WSC00110` and the 2026-09-14 note) were re-read at the
  cited lines.
- **Pin formats:**
  - Git blob SHAs are `sha1("blob <len>\0" + bytes)` of the retrieved
    bytes, i.e. what `git hash-object` and `git ls-tree` print. Blobs
    already pinned by earlier audits were recomputed and matched (noted
    per row).
  - Line numbers are written "(K5 L97–99)": source K5, lines 97–99 of
    that blob or retrieved copy. Single-line JSON documents (Toss T3, the
    Meritz and LS JSON exports) are cited by JSON path instead.
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
| Endpoint (real / paper) | `ws://ops.koreainvestment.com:21000` / `…:31000`, path `/tryitout` in current examples; **plain `ws://` only** — E+L | `wss://api.kiwoom.com:10000` / `wss://mockapi.kiwoom.com:10000`, path `/api/dostk/websocket` — F+C | `wss://openapi.ls-sec.co.kr:9443/websocket` / `:29443` (L1 only); portal `accessUrl` `/websocket/stock`·`/etc` conflicts — F+E | `wss://openapi.dbsec.co.kr:7070/websocket` / `:17070` — F+C+N | `wss://openapi-ws.tossinvest.com/ws/v1`; **real only** — F | `wss://openapi.imeritz.com:29443/websocket`; **real only** — F+E |
| Auth model | approval key from `POST /oauth2/Approval` (`appkey`, `secretkey`), sent as `approval_key` in **every** subscribe header; lifetime not documented — E+C | first packet `{"trnm":"LOGIN","token":…}` with the REST access token, then a LOGIN ack — C only; W1 tables show REST `authorization: Bearer` headers instead — F/C conflict | REST access token in `header.token` of every message — F+E | REST access token in `header.token` of every message — F | `Authorization: Bearer` on the HTTP handshake; a token reissue revokes the old one and closes the socket — F+G | `header.token` "Bearer …" in every subscribe message; whether `mac_address` is needed is unresolved — F+E |
| Subscription limit | server limit **not found**; client code refuses ">40" but counts subscribe *functions*, not symbols — C | **not found** | planned "세션당 200개" (TR × symbol), not yet applied — G | "50종목/세션" — N | 100 per connection (channel × symbol); 5 declarations/s — F+G | "실시간주식체결가 + 실시간주식호가 20건 등" (ambiguous) — G |
| Connection limit | **not found** | **not found** | "계좌(앱키)당 3개" from 2026-10-31 — G | 2 per app (account); 6 connects/min — N | 2 per account; a third is accepted and the oldest closed — F+G | 2 per HTS ID — G |
| Trade channel | `H0STCNT0` 실시간체결가 (KRX); `H0NXCNT0` (NXT); `H0UNCNT0` (통합) — E | `0B` 주식체결 — F+E | `S3_`/`K3_` (KRX), `NS3` (NXT), `US3` (통합) — F+E | `S00`, one TR for all venues — F+E | `realtime-trade`, `trade:kr` (integrated only) — F | `ohhts_stck_cntg` (KRX), `ohhts_nxt_cntg` (NXT), `ohhts_unt_cntg` (SOR 통합) — F+E |
| Order-book channel | `H0STASP0` 실시간호가 (KRX); `H0NXASP0` (NXT); `H0UNASP0` (통합); 10 levels — E | `0D` 주식호가잔량, 10 levels; `0C` 주식우선호가 (best bid/ask only) — F+E | `H1_`/`HA_` (KRX), `NH1`, `UH1`; 10 levels — F+E | `S01`, 10 levels, **no venue field** — F+E | `realtime-orderbook`, `orderbook:kr`; full snapshot; depth not documented — F+G | `ohhts_stck_aspr`, 10 levels, **KRX only** — F |
| Market-operation channel | `H0STMKO0` 장운영정보 (KRX), `H0NXMKO0`, `H0UNMKO0`; per symbol, "VI 발동 시와 VI 해제 시" — E | `0s` 장시작시간 (market-wide, coded `215`); `1h` VI발동/해제 — F+E | `JIF` 장운영정보 (market-wide) — F+E | **not found** | **not found** | **not found**; `mkop_clcd`/`trht_yn` in trade body only |
| Frame format | control: JSON; data: `flag\|tr_id\|count\|payload`, payload `^`-delimited, `count` records per frame — E | JSON text for control and data; data `trnm` `"REAL"`, `values` keyed by numeric field ids — F+E | JSON `{header, body}`; all values strings — E | JSON `{header, body}`; all values strings; field-name case differs between table and example — F+E | JSON `{type, topic, data}`, one record per frame; **lossy** — F | JSON `{header, body}`; all values strings — F+E |
| Encryption | per-subscription AES-256 key and IV in the subscribe ack; data flag `1` = encrypted; which market-data channels are encrypted **not documented** — E+C | none documented (TLS only) — F | none documented | none documented | none (TLS required) — F | none documented |
| Heartbeat | server JSON `tr_id` `"PINGPONG"`; client answers with a WebSocket **pong control frame**; interval not documented — C+L | server `PING` (text or `trnm`); client **echoes the same packet**; interval not documented — C only | **not found** | not found; "연결 후 Send … 10초 이내" or disconnect — N | client sends text `PING` within 180 s ("60초 간격 권장"); server `{"type":"pong"}` — F | **not found** |

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
  every subscribe message (below), crosses the network without TLS. This
  blocks any KIS connection under gate G-W2 (§10.1).
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

### 4.1 Pinned sources

All LS sources are public web resources on `https://openapi.ls-sec.co.kr`
with no immutable revision; only L1 carries a publisher version. Each sha256
prefix identifies only the copy retrieved at the stated time on 2026-11-05.

- L1 is byte-identical to the copy pinned by the trade evidence (its L1).
- L3–L11 are the portal's TR-detail JSON (`/guide/api/<data-tr>?type=rest&api=<data-api>`).
  The ids come from L2. The `api=` value is `9a2800c3-9bf2-4d67-8d83-905074f06646`
  ("[주식] 실시간 시세") or `eddd61f7-d595-4370-b9c3-49c4c6178096` ("[기타] 실시간 시세").

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true | `9aaca437f1925115`, 07:54:49–07:54:59Z, 2,792,313 bytes; publisher `"version" : "20261026021444748"` | `servers` (WEBSOCKET `url`, `simulationUrl`, `contentType`); WebSocket groups `apis[13]` "[주식] 실시간 시세" (65 TRs) and `apis[39]` "[기타] 실시간 시세"; request/response field tables; `transactionPerSec`; OAuth `expire_in` |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `d3417664b0637f28`, 07:55:42Z (page varies per request) | `data-api` / `data-tr` ids; `data-realtime="true"` |
| L3 | `…/guide/api/1v82075e-xo68-55y8-0if3-h7053s85441q?…` (S3_) | `feefc8800c4cfcda`, 07:56:39Z | `domain`, `accessUrl`, code samples, response example |
| L4 | `…/guide/api/w384266h-m7ss-4vw2-g71j-a1h28rw228fr?…` (K3_) | `16ca3a55d1fed3b4`, 07:56:36Z | same |
| L5 | `…/guide/api/6109bede-ef88-45b2-bf8b-0e5a00ccfdf7?…` (NS3) | `ec7073bda67c6960`, 07:56:42Z | same |
| L6 | `…/guide/api/b26bf1b2-9662-469c-8b2c-a7241a3bf05c?…` (US3) | `4e3783bf84764d55`, 07:56:46Z | same |
| L7 | `…/guide/api/1x6v03nd-8q12-500i-ip58-7x0272qv1wzm?…` (H1_) | `64b535fdeb6e4c63`, 07:56:31Z | same |
| L8 | `…/guide/api/z25317m7-61g4-6k88-27p5-tab0k6146w1p?…` (HA_) | `c9ea70e0a9641461`, 07:56:34Z | same |
| L9 | `…/guide/api/cb01a6c6-242f-456d-a7fe-7a0dccad0ce8?…` (NH1) | `5701056f2b203fe5`, 07:56:44Z | same |
| L10 | `…/guide/api/09f45862-49e8-4220-b2f8-09f7cfb72c99?…` (UH1) | `f0ad2eeced3ae7db`, 07:56:49Z | same |
| L11 | `…/guide/api/148z73fs-4n7x-0ot8-46t8-63jg7w181y21?type=rest&api=eddd61f7-…` (JIF) | `201a21c2c84eee27`, 07:56:51Z | same |
| L12 | https://openapi.ls-sec.co.kr/renewal/js/apiguide-52fb3f6955943fdee555972c5802f07e.js (loaded by L2) | `a46b0b4e534868e6`, 07:56:06Z, 68,433 bytes, 1,583 lines; the content hash is in the file name | Portal console WebSocket client: L40, L207, L1007–1031, L1046–1066, L1090–1166, L1168–1186 |
| L13 | https://openapi.ls-sec.co.kr/howto-use | `fc5a454085f50dcf`, 07:58:14Z | Step "3-4 WebSocket 연결 및 구독 등록" (NWS sample) |
| L14 | https://openapi.ls-sec.co.kr/community-faq (→ `/community/10000000-0000-0011-0000-000000000002`) | `c805082d0996c04d`, 07:58:16Z; 9 FAQ entries | Community FAQ (no WebSocket entry; §4.7) |
| L15 | Notice "[공지] OPEN API 유량제어 시행 안내", 2026-09-23: `…/community/10000000-0000-0011-0000-000000000001/posts/043f99f1-271c-4d00-93e4-21b1fbff8de0` | `6462299c3d8768a3`, 07:59:51Z | Planned final session/subscription limits |
| L16 | Notice "[공지] OPEN API 시스템작업 및 1차 유량제어 시행 안내", 2026-10-16: `…/posts/03f7e4d4-cdb3-4276-a7b6-0f27ca5ebfb5` | `add99aaffedebd28`, 07:59:31Z | Phase-1 session limit from 2026-10-31 |
| L17 | https://openapi.ls-sec.co.kr/intro | `c4eedea3dfac4d38`, 07:58:31Z | Marketing prose only ("WebSocket · 10ms"); not relied on |

Notices L15/L16 were found via the notice list
(`/community-notice`, `a4f0ed56d8bbfa67`, 07:59:17Z; 57 entries, first
page read). Of the other notices read, only `eba635bf…` touches this
topic: a 2026-09-12 outage "KRX 애프터마켓 개설 및 NXT 제도 반영" (sha256
`7fd411e5139f9554`). It contains a support phone number, which is not
copied.

**Missing evidence:**

- There is no publisher Git repository or SDK for LS WebSocket. Behaviour
  is from L1 field tables, L3–L11 examples, L12 portal console code and
  L13/L15/L16 prose.
- There is no heartbeat/ping, reconnect, server-close or WebSocket error-code
  documentation. The subscribe-ack frame shape is also undocumented; only
  L12 code reads it.
- No sign-code list on any WebSocket TR. L1 has "1:상한 2:상승 3:보합
  4:하한 5:하락" on REST TRs only (t1961, t2111, t8410, …), which is not
  evidence for `sign` on S3_/K3_/NS3/US3.
- No time-zone statement, no sequence or trade id, and no date field in
  any trade or order-book frame.
- No paper-environment statement beyond L1 `simulationUrl`.

### 4.2 Connection

- **Endpoints (L1 `servers`):**
  - WEBSOCKET `url` `wss://openapi.ls-sec.co.kr:9443`.
  - `simulationUrl` `wss://openapi.ls-sec.co.kr:29443`.
  - `contentType` `application/json; charset=UTF-8`.
  - L1 `path` is `/websocket` for every WebSocket group.
  - Code samples connect to `wss://openapi.ls-sec.co.kr:9443/websocket`
    (L3–L11 `codeSamples`; L13 step 3-4). L12 L1121 connects to
    `d.domain + "/websocket"`.
  - L3–L11 carry `accessUrl` `/websocket/stock` or `/websocket/etc`,
    which contradicts the other sources (§4.7).
  - Only port 9443 appears in L3–L13. Port 29443 appears only in L1.
- **Protocol:** `wss` only.
- **Auth model:**
  - Every subscribe message carries the access token in the JSON
    `header.token` ("접근토큰", String 1000, "Access Token을 설정하기 위한
    Header Parameter"; L1, L3–L11). There is no separate approval-key
    route.
  - The token is the REST OAuth token from `POST /oauth2/token`
    (form-urlencoded: `grant_type` "client_credentials", `appkey`,
    `appsecretkey`, `scope` "oob"). The response has `access_token` and
    `expire_in` "유효기간(초)" (L1 `apis[0]`); no lifetime value is stated.
  - No URL-query token appears in any LS WebSocket sample.
  - Whether a paper (모의) token is required on 29443, or accepted on 9443,
    is **not documented**. **Inference:** paper sessions need a paper-app
    token on 29443. Unverified.
- **Heartbeat/ping:** **not found** in L1, L3–L16 (no "ping", "heartbeat",
  "keepalive" or "PINGPONG" in any copy).
- **Reconnect guidance:** **not found.**
- **Max connections (L15, L16; publisher guide):**
  - Before 2026-10-31: "세션 : 계좌(앱키) 무제한 및 IP당 20개".
  - From "2026년 10월 31일 08:00~": "세션 : 계좌(앱키)당 3개", with
    "※ 향후 구독갯수 제한 예정입니다." (L16).
  - The notices say "세션", not "WebSocket". **Inference:** a session is
    one WebSocket connection; the word "구독" in the same notices
    supports this.

### 4.3 Subscription model

- **Message (L1 field tables; L3–L11 code samples; L12 L1049–1054):**

  ```json
  {"header": {"token": "<ACCESS_TOKEN>", "tr_type": "3"},
   "body": {"tr_cd": "S3_", "tr_key": "005930"}}
  ```

- **`tr_type` (L1, verbatim):** "1: 계좌등록, 2: 계좌해제, 3: 실시간 시세 등록,
  4: 실시간 시세 해제". L12 L40: `LIVE_SUBSCRIBE = "3", LIVE_UNSUBSCRIBE =
  "4"`. Codes 1/2 serve the account feeds (named only: SC0 "주식주문접수",
  SC1 "주식주문체결", SC2 "주식주문정정", SC3 "주식주문취소", SC4
  "주식주문거부").
- **`tr_cd`:** body, String 3 "LS증권 거래코드".
- **`tr_key` (body):**

  | TR family | Spec (verbatim) | Required | Example |
  | --- | --- | --- | --- |
  | KRX TRs (S3_, K3_, H1_, HA_) and JIF | String 8: "단축코드 6자리 또는 8자리 (단건, 연속), (계좌등록/해제 일 경우 필수값 아님)" | `required: false` | `"005930"`, `"122870"`, `"086520"`; JIF `"0"` |
  | NXT TRs (NS3, NH1) | String 10: "단축코드 7자리 + 공백 3자리" | `required: false` | `"N010950   "`, `"N000880   "` |
  | Integrated TRs (US3, UH1) | same text as NXT | US3 has no `required` key, so L1 `defaults.fieldRequired: true` applies (L6 shows `true`); UH1 `false` | `"U005930   "` |

  - Portal client code (L12 L1007–1031) treats the key as fixed width:
    "게이트웨이는 tr_key를 고정 길이로 받고 그 폭은 TR마다 다르다". The
    console pads the key with trailing spaces up to the example's length
    (or the spec `length`).
  - What "연속" means (several keys in one message?) is **not documented**.
  - JIF `tr_key` `"0"` is unexplained.
- **Per-symbol vs batch:** examples are one key per message. Batch syntax
  is **not documented**.
- **Max subscriptions:** none enforced as of the L16 phase.
  - L15 states the planned final rule: "구독제한 : 세션당 200개" and "※ 동일
    종목의 다른 실시간 구독 경우 개별 구독 적용 ex) US3(통합체결) 삼성전자 구독 +
    UH1(통합호가잔량) 삼성전자 구독 의 경우 2건의 구독이 됩니다."
  - L16 (later) applies only the session limit and defers the
    subscription cap.
- **Ack (publisher client code only, L12 L1088–1093, L1057–1066,
  L1145–1153):**
  - "데이터보다 ACK가 먼저 한 번 온다."
  - The console treats the first frame containing `rsp_cd` as the ack. It
    reports a rejection when `header.rsp_cd` (or root `rsp_cd`) is
    non-empty and not `"00000"`, using `rsp_msg` as the reason.
  - Ack field tables, success text and error codes are **not found** in L1
    or L3–L11.
- **Unsubscribe:** the same message with `tr_type` `"4"` (L12 L1182). L12
  sends it before closing.
- **Venue selection is by TR code, not by a field:**
  - KRX: `S3_`, `K3_`, `H1_`, `HA_`.
  - NXT: `NS3` "(NXT)체결", `NH1` "(NXT)호가잔량".
  - Integrated: `US3` "(통합)체결", `UH1` "(통합)호가잔량".
  - There are no codes `NS3_`/`US3_` (with underscore). The NXT and
    integrated codes are three letters (L1, L2).

### 4.4 Market-data channels

| Channel (title verbatim) | TR / channel id | Content | Venue | Frame format | Evidence |
| --- | --- | --- | --- | --- | --- |
| "KOSPI체결" | `S3_` | Trade print + day OHLC + cumulative counters + best bid/ask | KRX (example `exchname` `"KRX"`) | JSON; all values strings | field table (L1), publisher example (L3) |
| "KOSDAQ체결" | `K3_` | same fields | KRX | same | field table, example (L4) |
| "(NXT)체결" | `NS3` | same + `ex_shcode`; L1 has **no `high`** | NXT (`"NXT"`) | same; L1 types numerics `Number`, example has strings | field table, example (L5) |
| "(통합)체결" | `US3` | same + `ex_shcode` | Integrated; `exchname` "KRX, NXT" | same | field table, example (L6) |
| "KOSPI호가잔량" | `H1_` | 10-level book + totals + mid-price block | KRX; no venue field | JSON strings | field table, example (L7) |
| "KOSDAQ호가잔량" | `HA_` | same | KRX | same | field table, example (L8) |
| "(NXT)호가잔량" | `NH1` | same + `ex_shcode` | NXT | same | field table, example (L9) |
| "(통합)호가잔량" | `UH1` | One price ladder; `krx_`/`nxt_`/`unt_` quantities per level and totals; per-venue `donsigubun`, mid-price | Integrated | same | field table, example (L10) |
| "장운영정보" | `JIF` | `jangubun`, `jstatus` | All markets ("1:코스피 … 6:NXT전용 … F:일본주식오후") | JSON strings | field table, example (L11) |

Other domestic-equity market-data TRs in L1 (named only):

- Pre-match and after-hours: YS3/YK3/NYS/UYS (예상체결); DS3/DK3
  (시간외단일가체결); DH1/DHA; H2_/HB_ (장전시간외호가잔량).
- S2_/KS_/NS2/US2 (우선호가) and S4_ "KOSPI기세".
- VI_/DVI/NVI/UVI (VI발동해제) and SHC/SHD/SHI/SHO (상/하한가).
- K1_/OK_/NK1/UK1 (거래원) and program-trading TRs.

**Trade channels (S3_/K3_/NS3/US3; L1, L3–L6):**

- **Time:** `chetime` "체결시간" String 6; examples are `HHMMSS`
  (`"090851"`). `opentime`/`hightime`/`lowtime` are also `HHMMSS`. There is
  **no date field**. Zone **not documented**.
- **Price/quantity:**
  - `price` "현재가", `cvolume` "체결량".
  - `volume` "누적거래량", `value` "누적거래대금" (unit not stated).
  - `w_avrg` "가중평균가".
  - `offerho`/`bidho` "매도호가"/"매수호가".
- **Side:** `cgubun` "체결구분": "+ : 매수 / - : 매도" (S3_, K3_, US3; no
  description on NS3).
  - Cumulative `mdvolume` "매도누적체결량", `mdchecnt`, `msvolume`,
    `mschecnt`, and `cpower` "체결강도".
  - In all four examples, `cpower` = `msvolume` / `mdvolume` × 100 to two
    decimals.
- **Change/sign:**
  - `sign` "전일대비구분" String 1 has **no code list**.
  - `change` "전일대비" and `drate` "등락율".
  - Every example has `sign` `"2"` with unsigned positive `change`, so the
    sign convention for falls is not determinable.
- **Session:** `status` "장정보" String 2. On S3_ only: "' 0':장중 / ' 4':장후시간외
  / ' 3':장마감 / '10':장전시간외". The example value is `"00"` (§4.7).
- **Venue:** `exchname` "거래소명" String 3. On NS3/US3 also `ex_shcode`
  "거래소별단축코드" (example `"N010950"`, `"U005930"`). `shcode` stays the
  6-digit code.
- **Sequence/trade id:** **none.**
- **Other fields:** `jnilvolume` "전일동시간대거래량".

**Order-book channels (H1_/HA_/NH1/UH1; L1, L7–L10):**

- `hotime` "호가시간" String 6 (`HHMMSS`); no date.
- Levels 1–10: `offerho1..10`, `bidho1..10`, `offerrem1..10`,
  `bidrem1..10`, plus `totofferrem`/`totbidrem` and `volume`.
- `donsigubun` "동시호가구분": "1:장중 / 2:시간외 / 3:장전/장중/장마감".
- `alloc_gubun` "배분적용구분": "기본값 : space / 1: 배분개시 / 2: 배분해제".
- `midprice`, `offermidsumrem`, `bidmidsumrem`, `midsumrem`, and
  `midsumremgubun` "' '없음 '1'매도 '2'매수".
- UH1 duplicates every quantity as `krx_`, `nxt_` and `unt_`, and splits
  `donsigubun` into `krx_`/`nxt_`.
- No sequence field. No venue field on H1_/HA_.
- Arithmetic checks (examples):
  - NH1: level sums equal `totofferrem` 4761 and `totbidrem` 7116, and
    `midprice` 46700 is the mean of the best quotes.
  - UH1: `krx_` level sums equal `krx_totofferrem` 4245162 and
    `krx_totbidrem` 1623247.

**JIF (L1, L11):**

- `jangubun` "장구분": "1:코스피 / 2:코스닥 / 3:KRX / 5:선물/옵션 / 6:NXT전용 /
  8:KRX야간파생 / 9:미국주식". Codes A–F cover Chinese, Hong Kong and
  Japanese morning/afternoon sessions (e.g. "C:홍콩주식오전").
- `jstatus` "장상태": a long verbatim list, including "11:장전동시호가개시",
  "21:장시작", "31:장후동시호가개시", "41:장마감", "51:시간외종가매매개시",
  "54:시간외단일가매매종료", "55:프리마켓 개시", "56:에프터마켓 개시",
  "57:프리마켓 마감" and "58:에프터마켓 마감".
  - It also lists KOSPI/KOSDAQ circuit-breaker and sidecar codes 61–71,
    which apply when `jangubun` is 1 or 2.
  - Codes 61–77 are re-used with different meanings for `jangubun` 5.
  - A decoder must therefore read `jstatus` together with `jangubun`.
- No time field. The example is `{"jangubun": "C", "jstatus": "21"}`.

### 4.5 Frame encoding

- **Format:** JSON text, `{"header": {"tr_cd", "tr_key"}, "body": {...}}`
  (L3–L11 examples). L1 response headers list only `tr_cd`. The examples
  also echo `tr_key`, with its padding (`"N010950   "`).
- **Types:** every body value in every example is a JSON **string**, even
  where L1/L5/L6/L9/L10 type the field `Number`. Integers appear as plain
  digits; decimals unpadded (`"1.93"`, `"332.56"`). Empty strings and a
  lone space occur (§4.7).
- **Multi-record frames:** **not documented**. Every example is one record
  with no count field.
- **Encryption:** **none documented.** No key/iv field appears in any LS
  WebSocket TR.
- **Character encoding:** L1 `contentType` `application/json;
  charset=UTF-8`.
- **Value unit (Inference):** in S3_/K3_/NS3/US3 examples, `value` ≈
  `volume` × `w_avrg` / 10^6 (603.66→`604`, 15083.48→`15083`,
  1655.62→`1656`, 926809.52→`926807`). This suggests millions of KRW. The
  unit is not documented.

### 4.6 Limits and errors

- **Connections:** 3 sessions per app key from 2026-10-31 08:00 (L16).
  The previous limit was "IP당 20개".
- **Subscriptions:** planned "세션당 200개", counting each TR × symbol
  separately (L15). It is not yet applied as of L16.
- **`transactionPerSec`:**
  - `"-"` for every market-data WebSocket TR in L1 and L3–L11.
  - `"1"` for the account TRs SC2/SC3/SC4 (named only).
- **Error/close codes:** **not found.** L12 shows only that a non-`"00000"`
  `rsp_cd` in the ack means rejection.
- **Over-limit behaviour** (session or subscription) and server-initiated
  disconnects: **not documented.**
- **Community FAQ (L14):** its 9 entries do not cover WebSocket
  connection, limits or errors. The only real-time mention is the NWS news
  answer ("실시간 수신이 필요하면 실시간 TR NWS를 구독하세요"). The FAQ about
  "모의투자 주문처리가 안되었습니다" is about orders and is out of scope.

### 4.7 Contradictions and gaps

1. **Path:**
   - `/websocket` appears in L1 `path`, all code samples, L13 and L12
     L207/L1121.
   - L3–L11 `accessUrl` is `/websocket/stock` or `/websocket/etc`.
   - **Inference:** `accessUrl` is a portal grouping label; connect to
     `/websocket`. Unverified.
2. **Paper endpoint:** `simulationUrl` `:29443` is only in L1. The portal
   detail `domain`, samples and how-to show `:9443` only.
3. **NS3 field table vs example:**
   - L1/L5 omit `high`, but the L5 example contains `"high": "62700"`.
   - NS3 `hightime` is typed `Number` 8, while other TRs type it String 6.
4. **Declared vs actual types:** NS3/US3/NH1/UH1 declare `Number` for
   prices and quantities, and US3 declares `ex_shcode` `Number` 10. All
   examples are strings, including `ex_shcode` `"U005930"`.
5. **`status` codes:** S3_ lists space-padded codes (`' 0'`, `' 4'`,
   `' 3'`, `'10'`). Every example sends `"00"`. K3_/NS3/US3 give no list.
6. **H1_/HA_ examples (08:42–08:43, `donsigubun` `"3"`):**
   - `totofferrem`/`totbidrem` are `"0"` while levels 1–3 are non-zero.
   - The mid-price fields in the table are absent.
   - `alloc_gubun` is `""`, although the table says "기본값 : space".
7. **UH1 example:**
   - `volume` is `" "` (a single space).
   - `nxt_donsigubun` is `"0"`, outside "1/2/3".
   - `krx_midsumremgubun` is typed `Number` but sent as `""`.
8. **Integrated trades (L6):** at `chetime` `162202` the US3 example has
   `exchname` `"NXT"` and `opentime`/`hightime`/`lowtime` `080000`.
   - **Inference:** `exchname` gives the venue of each integrated print.
     It is not a fixed feed label.
   - In the same example, `volume` − `mdvolume` − `msvolume` = 1,644,881.
     Gaps also appear for S3_ (6,795) and K3_ (37,456), but not for NS3
     (0). **Inference:** auction prints are unclassified (cf. trade
     evidence §4.5). Not documented.
9. **`tr_key` width:** KRX keys are "6자리 또는 8자리" in a field of length
   8, but examples are 6 characters. NXT/integrated keys need exactly 10
   characters with trailing spaces. Padding is a portal-console behaviour
   (L12), not a stated server rule.
10. **Sign:** there is no WebSocket sign list. Examples cover only `"2"`.

### 4.8 Gates and not-verified items

See §10 (gates tagged [LS]) and §11.

## 5. DB Securities

### 5.1 Pinned sources

Git sources:

- Commit [`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb)
  (`564b5100b80a3a785468b77ee8c0557f6edcfdeb`, committer date
  2026-08-20T10:06:26+09:00). It is the commit pinned by the trade,
  candle and capability evidence documents.
- Fetched 08:00:39Z. Blob SHAs are from `git ls-tree` of that commit.

Portal JSON (`https://openapi.dbsec.co.kr`) was retrieved 08:01:37–08:03:11Z.
The ids are the ones the SDK docstrings link:

- group `94b5fddc-b819-451b-9619-13ee42468798` "국내주식시세(실시간)";
- group `0140b583-0f93-4aff-897b-e350b3652b40` "웹소켓(공통)".

The portal metadata contains staff contact data and IP ranges, and
DP4/DP5 contain a sample account number. None of these are copied.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| D1 | [`dbsec_sdk/websocket/stream.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/websocket/stream.py) | blob `3e16937c651e67b03fbcaa000964119b0e8c196b`; L6–18, L64–90, L121–125, L157–165, L403–452, L465–510 | SDK client: URLs, message shape, `tr_type`, error hints, limits, control/keepalive handling, reconnect |
| D2 | [`dbsec_sdk/apis/kr_stock_realtime/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/kr_stock_realtime/endpoints.py#L29-L51) | blob `4a230c35ef8732722ddd23a73f84c8fd0effb919`; L29–51, L106–154 | TR list (9), `/pub/<tr>` paths, "TPS: 2", portal api ids |
| D3 | [`examples/kr_stock_realtime/kr_stock_realtime_execution_price.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_realtime/kr_stock_realtime_execution_price.py#L18-L97) | blob `7bb1a89ff71116d50e300755d69e1a1874e03832`; L18–84, L94–97 | S00 field list (docstring), `tr_key` prose |
| D4 | [`examples/kr_stock_realtime/kr_stock_realtime_orderbook.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/kr_stock_realtime/kr_stock_realtime_orderbook.py) | blob `6d2b5295c541bc2a08622fc1265d74786a391d65`; L18–209, L232 | S01 field list; `tr_key="UJU-005930"` |
| D5 | [`examples/dbsec_helper.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/examples/dbsec_helper.py#L525-L590) | blob `a00db7a5a6104f7b4029c0b206231ff389b97f6b`; L50–56, L525–590 | Example WS loop (0.5 s blocking sleep per frame), unsubscribe on exit |
| D6 | [`docs/errors_and_rate_limits.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/errors_and_rate_limits.md#L179-L222) | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L179–188, L214–222 | WebSocket message codes; WebSocket limits |
| D7 | [`docs/api_support_matrix.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/api_support_matrix.md#L69-L81) | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c`; L3–5, L69–81, L268–272 | S00/S01 ⭕ paper + real, TPS `-`; DisconnectSession ⭕, TPS 1 |
| D8 | [`docs/sdk_usage.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/sdk_usage.md#L140-L155) | blob `af4995d87434cc2b9bb7ca07cab55ddf56cf7878`; L140–155 | `tr_key="J 005930"`; `tr_type` usage |
| D9 | [`README.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/README.md#L686-L695) | blob `377b5b9e0e3bcdfa54edad23507860798fa91143`; L686–695, L732, L740 | Real/paper URLs; "WebSocket 포트만 다릅니다"; paper support |
| D10 | [`dbsec_sdk/config.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/config.py#L25-L35) and [`config.yaml.example`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/config.yaml.example#L16-L25) | blobs `8fab32d061fa9b483247915b2a37159831a0eeee` (L25–35), `f6204f1399f2f080c11f28364444b40b7868ef96` (L16–25) | URL constants by mode |
| D11 | [`dbsec_sdk/apis/ws_common/endpoints.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/apis/ws_common/endpoints.py#L40-L63) | blob `d1fa624f52159ab7979879518e381de2b171c894`; L29–35, L40–63 | Session-reset REST API |
| DP1 | `https://openapi.dbsec.co.kr/api/apis/public/api-list/94b5fddc-b819-451b-9619-13ee42468798` | sha256 `f48090f104faa614`, 08:01:37Z | Per-TR `accessUrl`, `domain`, `simulatedDomain`, `protocolType`, `contentType`, `extraParam` (`requestLimit`), `lastModifiedDate` |
| DP2 | `…/api/apis/public/<api_id>`: S00 `7c257cdc-5807-46ca-8d86-666a2bfd6798`, S01 `973365c6-91fd-4ca8-ac66-fa1a65017c0e` | S00 `e90eead519a0ee6f` (08:02:01Z), S01 `89fb33ffe9255bcf` (08:02:04Z); `lastModifiedDate` 2024-02-26 (both) | Same metadata per TR |
| DP3 | `…/api/apis/guide/tr/<api_id>` (S00, S01) | S00 `beb73f3c6ad07255` (08:01:59Z), S01 `9d0f752bcc284d42` (08:02:02Z) | `transactionPerSec` `"-"`, `reqExample`, `resExample` |
| DP4 | `…/api/apis/guide/tr/property/<tr_id>`: S00 `7a7b6e1d-74b5-454d-9826-327afd598eab`, S01 `f67b8d3e-3fdc-427e-8b3b-aec6a240bcb6` | S00 `a353f2cc163227c5` (08:02:23Z, 68 rows), S01 `b63dbf8fb9479123` (08:02:25Z, 203 rows) | `req_h`/`req_b`/`res_h`/`res_b` field tables |
| DP5 | DisconnectSession: `…/public/api-list/0140b583-…` (`d02264f963dda0bb`, 08:01:39Z); `…/public/cc424a15-7d38-46d6-ab6e-5d46b2b386fc` (`e0f96dbe95546969`, 08:02:08Z); `…/guide/tr/cc424a15-…` (`3221c32d92fc5394`, 08:02:06Z) | `lastModifiedDate` 2025-08-27 | Session-reset description, 1 TPS |
| DP6 | https://openapi.dbsec.co.kr/testbed-sample | sha256 `a7a9ef6f037489a5`, 08:03:11Z | Older WS sample (overseas `V60` only): ports, message, first-frame example |

**Missing evidence:**

- There is no portal page on WebSocket heartbeat, reconnect, ack format,
  session or subscription limits, or error codes. Those come only from the
  SDK repository (D1, D6, D9).
- DP4 gives **no code list** for `HourClscode`, `PrdyVrsssign`,
  `CntgClscode`, `NewMkopclscode`, `PrprCntgclscode`, `CnccAsprclscode` or
  `CompClscode`. Only `AntcNmixclscode` and `ExmrClsCode` have lists.
- There is no dedicated market-operation (장운영) or VI channel in the
  domestic-stock real-time group (D2 L29–51; DP1 lists 9 TRs).
- No NXT or integrated example frame. No falling-price, pre-open or
  after-hours example. No time-zone statement.

### 5.2 Connection

- **Endpoints:**
  - Real: `wss://openapi.dbsec.co.kr:7070/websocket`. Paper:
    `wss://openapi.dbsec.co.kr:17070/websocket` (D1 L6–8, D9 L689, D10).
  - The portal metadata agrees on host and port: `domain`
    `wss://openapi.dbsec.co.kr:7070`, `simulatedDomain`
    `wss://openapi.dbsec.co.kr:17070`, `protocolType` `WEBSOCKET` (DP1,
    DP2). Its `accessUrl` is `/pub/S00` / `/pub/S01` (§5.7).
  - DP6: "접속포트는 운영-7070, 모의투자-17070 을 사용합니다."
  - D9 L693: "**WebSocket 포트만 다릅니다**". REST is one origin for both
    environments.
- **Protocol:** `wss`.
- **Auth model:**
  - The JSON `header.token`: "G/W 에서 발급하는 접근토큰", String 1000,
    `requireYn` `Y` (DP4 `req_h`). It is the REST access token.
  - There is no approval-key route.
  - D1 L385–388 obtains the token per message from the SDK token manager.
  - DP3 `reqExample` uses a template placeholder (not copied).
  - Code `10009` "token 계좌정보와 서버정보가 일치하지 않습니다." (D6 L186).
  - Lifetime: D6 L211 mentions "24h 토큰 재사용" in the SDK cache
    (publisher repo note). The WebSocket-specific lifetime or expiry
    behaviour is **not documented**.
- **Keep-alive:**
  - D6 L221 (publisher repo note) lists "연결 후 Send | 10초 이내 | 미전송
    시 연결 해제". D1 L165 says the same.
  - A ping/pong or `PINGPONG` frame is **not found**.
  - D1 L449–452 (client code) drops frames whose `header` and `body` are
    both empty "(keepalive 등)". This is not a documented server frame.
- **Reconnect:**
  - The SDK policy (D1 L465–510) is exponential back-off 2/4/8/16/32 s,
    up to 5 attempts, and it re-sends all stored subscriptions. **Not a
    contract; not adopted.**
  - For `10011`, D1 L84–88 advises calling the session-reset API and then
    reconnecting.
- **Max connections:**
  - "세션 수 | 2세션 | 앱(계좌)당 최대 2개" (D6 L218). D9 L732 says the
    same.
  - Over-limit code `10011` "계좌별 허용 세션 수를 초과하였습니다." (D6 L187).
  - Connection rate: "연결 빈도 | 6 TPM | 1분당 6건 (서버 정책)" (D6 L220).
    D1 L125 and L140–142 pace connects to 10 s.
- **Session reset:** `POST /api/v1/websocket/disconnectSession`
  (`DisconnectSession`), a REST call on `https://openapi.dbsec.co.kr:8443`
  with `simulatedDomain` null (DP5).
  - Description: "접속중인 모든 웹소켓 세션을 초기화 하는 API 입니다. ※
    발급받은 토큰정보와 일치하는 계좌의 세션이 초기화 됩니다."
  - Rate: `requestLimit` 1 (DP5, D11 L46–52).
  - The response carries an account number (named only; DP5 example not
    copied).

### 5.3 Subscription model

- **Message (DP3 S00 `reqExample`; D1 L10–13, L389–398; DP6):**

  ```json
  {"header": {"token": "<ACCESS_TOKEN>", "tr_type": "1"},
   "body": {"tr_cd": "S00", "tr_key": "J 005930"}}
  ```

- **`tr_type` (DP4 `req_h`, verbatim):** "1: 실시간 시세 등록, 2: 실시간 시세
  해제, 3: 계좌 등록". DP6 has the same text.
  - D1 L18 / D8 L153: account registration (`IS0`, `IS1`, named only) has
    "해제 메시지 없음 (세션 종료가 곧 해제)" (publisher repo note).
  - The numbering is the reverse of LS (§4.3).
- **`tr_cd`:** body, String 3, "TR코드입력: S00" / "S01".
- **`tr_key` (DP4 `req_b`, String 20, `requireYn` `Y`; verbatim, HTML
  breaks removed):**
  - "[KRX] 주식&ETF:J ETN: EN ※ 종목분류코드 + 주식종목코드 입력 (ex. J
    005930) ※ 종목분류코드는 두자리 입력이 필요하므로, J + " " (공백) 문자를
    넣어 2바이트를 맞춰 입력 부탁드리겠습니다."
  - "[NXT] NXT주식: NJ+ 종목코드 (ex. 삼성전자 종목조회시 NJN-005930,
    종목코드: N- + 기존종목코드)"
  - "[통합시세] 통합시세 주식: UJ+ 종목코드 (ex. 삼성전자 종목조회시
    UJU-005930, 종목코드: U- + 기존종목코드) ※ KRX거래소 단독 상장 종목의
    경우, 통합시세 코드가아닌 KRX 거래소 코드(J) 사용부탁드립니다"
  - So the formats are `"J 005930"` (KRX), `"NJN-005930"` (NXT) and
    `"UJU-005930"` (integrated). D4 L232 uses `"UJU-005930"` and D8 L147
    uses `"J 005930"`.
- **Venue selection:** the `tr_key` prefix selects the venue; one `tr_cd`
  (S00/S01) serves all three venues.
- **Max subscriptions:** "종목 수 | 50종목/세션 | 세션당 50종목 — 초과 시 SDK
  가 `RateLimitError` 발생" (D6 L219; D1 L123, L207–213).
  - This is a publisher repo note; no portal source states it.
  - Whether S00 and S01 on the same symbol count as one subscription or
    two is **not documented**.
- **Per-symbol vs batch:** one `tr_key` per message in every source. Batch
  is **not documented**.
- **Ack:**
  - The portal documents no ack.
  - DP6's sample output (overseas `V60`) prints the body of the first
    frame as `{"tr_key": ["FNTSLA"]}` before data.
  - **Inference:** a successful subscribe returns a frame whose body
    echoes the subscribed key(s) as an array. This is unverified for S00
    and S01.
  - D1 L403–447 (client code) treats any frame with `rsp_cd`/`rsp_msg` in
    `header` or `body` as a control or error response. It treats `""`,
    `"0"` or `"00000"` as normal, and notes that `header`/`body` "null 이거나
    rsp_cd/rsp_msg 만 담겨 온다".

### 5.4 Market-data channels

| Channel (title verbatim) | TR / channel id | Content | Venue | Frame format | Evidence |
| --- | --- | --- | --- | --- | --- |
| "[실시간]주식체결가" ("국내주식 실시간 체결가 API 입니다.") | `S00` | Trade print + day OHLC + limits + best quote + cumulative counters + status flags | By `tr_key` prefix; `ExmrClsCode` "1: KRX, 통합시세 / 2: NXT 거래소" | JSON; all values strings; `A0001` for every field | field table (DP4), publisher example (DP3), publisher client code (D2, D3) |
| "[실시간]주식호가" ("국내주식 실시간 호가 API 입니다.") | `S01` | 10-level book + changes + LP quantities + totals + expected price + mid-price | By `tr_key` prefix; **no venue field** | same | field table (DP4), publisher example (DP3), publisher client code (D2, D4) |

Also listed in the group (DP1, D2): "[실시간]ELW호가" `W01` and
"[실시간]ELW체결" `W00`, plus index TRs `U00`, `U03` and `U05`. Account
TRs are named only: `IS0` "[실시간]주식주문접수 조회" and `IS1`
"[실시간]주식주문체결 조회".

**S00 (DP4 `res_b`, 63 rows; DP3 example):**

- **Date/time:** `BsopDate` "실시간일자" String 8 (example `"20250827"`)
  and `StckCntghour` "체결시간" String 6 (`"142230"`). Zone **not
  documented**.
- **Price/quantity:**
  - `StckPrpr` "현재가", `CntgVol` "체결거래량".
  - `AcmlVol` "누적거래량", `AcmlTrpbmn` "누적거래대금".
  - `WghnAvrgprpr` "가중평균가격".
  - Day `StckOprc`/`StckHgpr`/`StckLwpr`, `StckSdpr` "기준가",
    `StckMxpr` "상한가", `StckLlam` "하한가".
  - In the example, `AcmlTrpbmn` ≈ `AcmlVol` × `WghnAvrgprpr` in KRW
    (39,198,911,700 vs 39,198,864,342). **Inference:** the unit is KRW.
- **Side:**
  - `CntgClscode` "체결구분코드" and `RgbfCntgclscode` "직전체결구분코드"
    (no code lists; example `"1"`).
  - Cumulative counters: `SelnCntgcsnu`/`ShnuCntgcsnu`
    "매도/매수체결건수", `SelnCntgsmtn`/`ShnuCntgsmtn` "매도/매수체결합계",
    `rltv` "체결강도".
  - A second scheme, "현재가비교방식": `PrprCntgclscode`,
    `PrprSelncntgsmtn`, `PrprShnucntgsmtn`, `PrprCttr`.
  - Example arithmetic: both schemes' sell + buy sums equal `AcmlVol`
    405039. `Rltv` 101.73 = 204254/200785×100, and `PrprCttr` 62.01 =
    155029/250010×100.
  - How a print is classified under either scheme is **not documented**.
- **Change/sign:**
  - `PrdyVrsssign` "전일대비부호" (no list; example `"1"` at
    `StckPrpr` = `StckMxpr`), `PrdyVrss` "전일대비", `PrdyCtrt`
    "전일대비율".
  - Each price field has a `…clr` "색참조(+상승, -하락)" companion.
- **Session/status:**
  - `HourClscode` "시간구분코드" (no list; `"0"`).
  - `AntcNmixclscode` "예상지수구분코드": "0:예상 / 1:정규".
  - `NewMkopclscode` "신장운영구분코드" (no list; `"20"`).
  - `TrhtYn` "거래정지 여부", `MangIssuyn`, `WarnYn`, `PrstClscode`.
- **Other fields:** `CntgPrgs` "체결틱추이" String 10 (example
  `"0040430000"`; meaning not documented).
- **Venue:** `ExmrClsCode` "1: KRX, 통합시세 / 2: NXT 거래소". KRX and
  integrated frames therefore share code `1`.
- **Sequence/trade id:** **none.**

**S01 (DP4 `res_b`, 198 rows; DP3 example):**

- **Time:** `BsopHour` "호가시간" String 6 (`"100647"`); **no date
  field**.
- **Levels:**
  - `askp1..10` "N매도호가", `bidp1..10`.
  - `AskpRsqn1..10`/`BidpRsqn1..10` quantities.
  - `AskpRsqnicdc1..10`/`BidpRsqnicdc1..10` changes.
- **Totals:**
  - `TotalAskprsqn`/`TotalBidprsqn` and their `…icdc` changes.
  - `OvtmTotalaskprsqn`/`OvtmTotalbidprsqn` "시간외총매도/매수호가잔량".
- **LP:** `LpAskprsqn1..10`, `LpBidprsqn1..10`, LP totals and changes.
- **Auction/expected price:**
  - `AntcCnpr` "예상체결가", `AntcCnqn` "예상체결량", `AntcIssyn` "예상
    활성 여부".
  - `CnccAsprclscode` "동시호가구분코드" and `CompClscode` "경쟁대량
    방향구분" (no lists).
  - `HourClscode` "시간구분" and `NewMkopclscode` "신 장운영 구분 코드".
- **Mid-price:** `MidPrc` "중간가" and the `MidpTotal…` fields.
- **Example arithmetic:** level sums equal `TotalAskprsqn` 809630 and
  `TotalBidprsqn` 2193305. `MidPrc` 54450 is the mean of the best quotes.
- **Not present:** venue field, sequence field.

### 5.5 Frame encoding

- **Format:** JSON text `{"header": {"tr_cd", "tr_key"}, "body": {...}}`
  (DP3). DP4 `res_h` lists only `tr_cd`. Both examples have `"tr_key":
  null`, so a decoder cannot rely on `header.tr_key` to route frames.
- **Types:** every DP4 field is `A0001` (string). Every example value is a
  JSON string; empty strings occur in `…clr` fields.
- **Field-name case:** DP4 names `askp1`, `bidp1` and `rltv` in lower
  case. The examples use `Askp1`, `Bidp1` and `Rltv` (§5.7).
- **Multi-record frames:** **not documented**; the examples are single
  records.
- **Encryption:** **none documented.**
- **Character encoding:** DP1/DP2 `contentType`
  `application/json;charset=utf-8`.
- **Control/error frames:** the portal documents none. D1 L424–434 (client
  code) says `header`/`body` may be JSON `null`, and `rsp_cd`/`rsp_msg` may
  be in either object.

### 5.6 Limits and errors

- **WebSocket message codes (D6 L179–188, publisher repo note; verbatim):**

  | Code | Message |
  | --- | --- |
  | `10004` | "tr_cd가 존재하지 않습니다. 확인 후 거래 하세요." |
  | `10005` | "허용되지 않는 tr_cd 입니다. 확인 후 거래 하세요." |
  | `10006` | "tr_key가 존재하지 않습니다. 확인 후 거래 하세요." |
  | `10009` | "token 계좌정보와 서버정보가 일치하지 않습니다. 확인 후 거래 하세요." |
  | `10011` | "계좌별 허용 세션 수를 초과하였습니다." |
  | `10017` | "종목코드를 찾을 수 없습니다. 거래코드 및 종목코드를 확인하세요.[% %]" |

  The SDK's interpretations (D1 L79–90) are client hints, not contract.
  For example, `10005` is said to cover paper-unsupported TRs, and the
  `10006` hint repeats the "J + 공백" key rule.
- **Limits (D6 L214–222, publisher repo note):**
  - 2 sessions per app (account).
  - 50 symbols per session.
  - 6 connections per minute.
  - The first send must happen within 10 s.
  - "송수신 딜레이 100ms" is an SDK pacing choice.
- **Per-TR `requestLimit`:** `"2"` for S00/S01 and `"10"` for W00/W01
  (DP1 `extraParam` `ThroughputQuotaRule`/`CorpThroughputQuotaRule`).
  D2 docstrings agree ("TPS: 2"). DP3 `transactionPerSec` and the D7 TPS
  column are `"-"`. What a per-second limit means for a WebSocket TR is
  **not documented**. **Inference:** it may cap subscribe/unsubscribe
  messages.
- **Over-subscription:** the server response is **not documented**. The
  SDK refuses the 51st subscription client-side (D1 L207–213).
- **Server-initiated disconnects:** only the 10-second no-send rule (D6
  L221). No close codes are documented.
- **Paper:**
  - S00/S01 are marked ⭕ "모의투자(`mode: "demo"`) + 실전투자 모두 호출
    가능" (D7 L3–5, L75–76).
  - D9 L740: "시세 · 실시간 · 차트 그룹은 전부 사용 가능".
  - Paper symbol coverage and data source are **not documented**.

### 5.7 Contradictions and gaps

1. **Path:**
   - DP1/DP2 `accessUrl` is `/pub/S00` / `/pub/S01`, and D2 `PATHS` copies
     it.
   - D1, D5, D9, D10 and DP6 all connect to `/websocket`.
   - **Inference:** `/pub/<tr>` is a gateway routing id, not the
     connection path. Unverified.
2. **S00 example vs request:** the request `tr_key` is `"J 005930"` (KRX),
   but the response `ShrnIscd` is `"U-005930"` (an integrated-style code,
   length 9 field) with `ExmrClsCode` `"1"`.
   - **Inference:** the example was captured from a `UJ` subscription, or
     `ShrnIscd` can carry the `U-` prefix. Either way, `ShrnIscd` cannot be
     assumed to be 6 digits.
3. **S00 example internal consistency:** `Askp1` 140200 < `Bidp1` 143300
   (crossed). `StckHgpr` = `StckMxpr` and `StckLwpr` = `StckLlam`. The
   example is illustrative only; do not use it as a fixture.
4. **Field-name case:** table `askp1`/`bidp1`/`rltv` versus example
   `Askp1`/`Bidp1`/`Rltv`. S01 has the same split for all 20 price levels.
   D3/D4 docstrings follow the table. A case-sensitive decoder built from
   either source would miss the other.
5. **S01 table vs example:**
   - The example has `TotalRsqnGap` and `TotalRsqnGapcclr`, which are not
     in DP4. The example value is the bid total minus the ask total
     (1383675).
   - DP4 names `MidpTotalAskpRsqncclr ` with a trailing space.
   - The S01 `reqExample` is a JSON-encoded string with raw CR/LF, so it
     does not parse as an object.
6. **Venue code `1`:** `ExmrClsCode` "1: KRX, 통합시세" does not separate
   KRX from integrated frames. S01 has no venue field at all.
7. **`tr_key` NXT format:** the field table example `"NJN-005930"` and the
   prose "NJ+ 종목코드" (D3 L97) differ in form. They are consistent only if
   "종목코드" already includes `N-`. REST CONCLUSION instead uses a separate
   market code plus `N-005930` (trade evidence §5.3).
8. **Limits sources:**
   - Session, subscription, connection-rate and 10-second rules appear
     only in the SDK repository, not on the portal.
   - Their wording differs: "앱(계좌)당 최대 2개" (D6) versus "계좌별 허용
     세션 수" (`10011`).
   - The per-TR `requestLimit` 2 conflicts with TPS `-` in DP3 and D7.
9. **Ack:** the only evidence is an overseas-TR sample output (DP6).
10. **Client pacing:** D1 sleeps 100 ms after every received frame (L306–
    307). D5 L574 and DP6 sleep 0.5 s per frame. **Inference:** a busy
    symbol could back up the socket under those clients. Do not copy.

### 5.8 Gates and not-verified items

See §10 (gates tagged [DB]) and §11.

## 6. Toss Securities

### 6.1 Pinned sources

Public Toss portal documents, retrieved 2026-11-05 07:54–07:56 UTC. No
token was issued, no WebSocket connection was opened and no API request was
sent. T1–T5 have the same sha256 as the copies pinned in the trade evidence
(§6.1 there, 07:10–07:12 UTC), so none changed between the two retrievals.
T2–T4 carry `last-modified: Wed, 04 Nov 2026 01:48:38 GMT`.

T5 L17 names T3 the "Canonical AsyncAPI 3.0 document for the realtime
WebSocket API. Use this as the source of truth for WebSocket channels,
subscription declarations, message schemas and examples, connection limits,
keepalive, and reconnect semantics." T3 is therefore `field table`. T2, T4
and T5 are `publisher guide`, and T4 L3 defers to the API documents.

T3 is a single-line JSON file, so it is cited by JSON path, not by line.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | sha256 `c5918961335ccd6b…`, 07:55:27Z; `openapi 3.1.0`, `info.version 1.2.28` | `paths./api/v1/orderbook.get`, `components.schemas.{OrderbookResponse,OAuth2TokenResponse}`: the REST shapes that T3 says its frames reuse |
| T2 | [overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md) | sha256 `bef057d9babe9a38…`, 07:54:47Z | L8, L64–69, L199–203 (WS listed as a product); L367–493 "웹소켓 연동": L371 topic rule, L379–384 channel list and venue, L388–408 connection steps, L434–442 delivery guarantees, L444–452 limits, L454–463 frames, L465–493 errors |
| T3 | [asyncapi.json](https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json) | sha256 `46669a360d4c5c64…`, 07:54:46Z; `asyncapi 3.0.0`, `info.version 1.2.3` ("REST 스펙(openapi.json)과 독립적으로 관리") | `servers.production`; `channels.connection` (auth, declare model, dispatch, limits, keepalive, close/reconnect, ack/error/ping/pong messages); `channels.realtime-trade`; `channels.realtime-orderbook`; `operations`; `components.securitySchemes.bearerToken` |
| T4 | [faq.md](https://openapi.tossinvest.com/openapi-docs/faq.md) | sha256 `6ad4c02b8e785f7d…`, 07:54:48Z | L3 (precedence), L9 (one valid token per client), L22 (venue), L27 (1m-candle session scope, cross-check only), L38–41 (integrated book, full snapshot, no venue per level, timestamp semantics) |
| T5 | [developers.tossinvest.com/llms.txt](https://developers.tossinvest.com/llms.txt) | sha256 `bbff77eaa55df248…`, 07:54:49Z (`etag "07da9e01…"`, `last-modified` 2026-10-08) | L5, L7, L10, L17, L35 |

**Missing evidence:**

- No publisher client code or SDK for the WebSocket was found. T2
  L412–432 is a `wscat` walk-through (`publisher example`; its sample
  client id and token are not copied).
- No paper/sandbox WebSocket server: T3 `servers` has only `production`.
- No market-operation or VI/halt channel. T3 has exactly five channels:
  `connection`, `realtime-trade`, `realtime-orderbook`, `realtime-order`,
  `realtime-conditional-order`.
- Order-book depth (number of levels) is not stated in T1, T3 or T4.

### 6.2 Connection

- **Endpoint:** `wss://openapi-ws.tossinvest.com/ws/v1`. T3
  `servers.production` gives host `openapi-ws.tossinvest.com`, protocol
  `wss` and pathname `/ws/v1`; T2 L369 and T5 L10 give the same URL. There
  is one endpoint for all channels and **real only**. T3: "TLS 필수".
- **Auth:** the HTTP handshake carries the header
  `Authorization: Bearer {access_token}`. The token is the REST token from
  `POST /oauth2/token` (Client Credentials Grant; T3
  `components.securitySchemes.bearerToken`, T5 L7). There is no separate
  approval key and no auth field in the subscribe message.
  - Handshake results (T3 `channels.connection.description`; T2
    L469–473): `101` success; `401` "토큰 없음·무효·만료"; `403` "허용 IP
    미등록"; `503` "서버 내부 오류". The REST allow-list ("WTS 설정 > Open
    API > 허용 IP 관리") also applies to the WebSocket.
  - No account header is documented for the WebSocket (T5 L7 requires
    `X-Tossinvest-Account` only for REST account/asset/order APIs). Account
    identifiers appear only in `personal:*` declarations.
- **Key lifetime / reuse:**
  - The token is re-validated **during** the connection. On expiry,
    reissue or deletion, removal of the IP from the allow-list, or an
    unsupported subscribed account, the server sends an `auth-revoked`
    error frame and closes. T3: "**토큰이 만료되면 연결도 종료되므로**,
    만료 전에 새 토큰을 발급받아 재연결하세요."
  - T4 L9: "클라이언트당 유효한 토큰은 1개입니다. 새로 발급하면 직전 토큰은
    즉시 무효화되어 `401 token-revoked` 로 거부됩니다."
  - T1 `OAuth2TokenResponse.expires_in` is "토큰 만료까지 남은 초."; 86400
    appears only as an example value.
  - **Inference:** issuing a new token, including for REST, revokes the
    token the open WebSocket uses. A token handover therefore always costs
    a reconnect and a gap in data (see §6.7 #3).
- **Heartbeat:** client-driven.
  - The server closes the connection after "**클라이언트로부터의 수신이
    180초간 없으면**"; data the server sends does not reset this timer.
  - The client sends the plain text frame `PING` (uppercase, not JSON) at
    an interval under 180 s, "**60초 간격 권장**". The server answers
    `{"type":"pong"}`.
  - "웹소켓 표준 ping/pong 프레임도 지원됩니다."
  - Sources: T3 `channels.connection.description` and `messages.ping` /
    `messages.pong`; T2 L407.
- **Reconnect guidance (T3 `channels.connection.description`):**
  - On `server-shutdown`, reconnect and re-declare. On `auth-revoked`, get
    a new token first.
  - Other closes may come "별도 close code 없이" and look like abnormal
    closure: idle timeout, backpressure on the order channels, or being the
    oldest connection over the limit.
  - Back off "지수 백오프(1s → 2s → 4s ..., jitter 포함 — REST `429` 대응과
    동일)" and re-declare the subscriptions.
  - "재연결하기 전에 쓰던 연결을 먼저 닫아 주세요".
- **Max connections:** "계정당 **2개**". A third connection is accepted
  and the oldest is closed (T3 limits table; T2 L388, L448).

### 6.3 Subscription model

- **Declarative full replace.** The client sends one JSON array as a text
  frame; that array **is** the complete current subscription set.
  - Items left out are unsubscribed, and `[]` unsubscribes everything.
  - There is no subscribe/unsubscribe action and no `tr_type`.
  - Sources: T3 `channels.realtime-trade.messages.declare.payload`; T2
    L389.
- **Array element shapes** (T3 `declare.payload.items.oneOf`):
  - `{"type": "trade:kr", "codes": [...]}` and `{"type": "orderbook:kr",
    "codes": [...]}`. `codes` holds "6자리 종목코드(숫자 또는 영문·숫자;
    예: `005930`·`0101N0`)", `minItems 1`.
  - `trade:us` / `orderbook:us` take US tickers (out of scope).
  - `personal:order` and `personal:conditional-order` are account feeds,
    **named only**.
  - An optional `{"id": "…"}` element is echoed in the ack or error.
- **Batching:** many symbols and channels go in one array. Per T2 L371,
  topic = `type` + `:` + code, e.g. `trade:kr:005930`.
- **Limits:**
  - "연결당 구독 수 | **100건** (`codes` 합산)"; T2 L449 adds "주문
    `accountSeq` 포함".
  - It is counted per channel × symbol: "같은 종목이라도 채널이 다르면 각각
    1건입니다".
  - Declaration rate: "**5회/초**".
- **Ack** (`type: "subscriptions"`, T3 `messages.subscriptionsAck`):
  - Required fields: `subscribed` (full keys) and `rejected[]` of
    `{target, code, message}`.
  - The ack arrives "데이터보다 먼저".
  - Per-item reject codes: `stock-not-found`, `symbol-market-mismatch`,
    `account-not-found`. A symbol that is lower-case or missing from the
    stock master gets `stock-not-found` (T3 `codes` description).
  - With a partial reject, "`subscribed` 항목은 정상 구독되고 연결은
    유지됩니다". A rejected item is rejected again on every re-declaration
    until it is fixed.
- **Whole-declaration error:** a `type: "error"` frame; "기존 구독 유지"
  (§6.6).
- **No initial snapshot.** "구독 직후 초기 스냅샷은 전송되지 않으며 다음
  체결부터 푸시됩니다". The same holds for "다음 호가 갱신부터" (T3
  `realtime-trade.description` / `realtime-orderbook.description`). T3
  points to REST `GET /api/v1/trades` / `GET /api/v1/orderbook` for the
  state at connect time.
- **Venue selection: none.**
  - `kr` is the integrated feed only. T2 L384: "`{시장}` 은 미국 `us`,
    국내(통합) `kr` 입니다. 국내는 통합 시세(KRX+NXT)만 노출합니다."
  - T3 declare item: "국내(통합 시세, KRX+NXT)는 `trade:kr`".
  - T4 L40 (order book): "REST·웹소켓 모두 국내 호가는 통합 호가로만
    제공되며". There are no KRX-only or NXT-only types.

### 6.4 Market-data channels

| Channel (title verbatim) | TR / channel id | Content | Venue | Frame format (JSON / delimited text / encrypted?) | Evidence |
| --- | --- | --- | --- | --- | --- |
| "Trade" — "[수신] 체결 프레임" | `realtime-trade`; declare `type` `trade:kr`; topic `trade:kr:{symbol}` | One trade per frame: "체결이 발생할 때마다" | KRX+NXT integrated; no venue field | JSON text, plain | field table (T3) |
| "Orderbook" — "[수신] 호가 프레임" | `realtime-orderbook`; `orderbook:kr`; topic `orderbook:kr:{symbol}` | Full book snapshot on each update (T4 L39 "전체 스냅샷입니다 … 증분 갱신은 제공하지 않습니다") | KRX+NXT integrated, merged by price (T4 L38) | JSON text, plain | field table (T3) + publisher guide (T4) |
| "Order Event", "Conditional Order Event" | `realtime-order`, `realtime-conditional-order` | Account feeds; **named only** | — | JSON | T3 |

**Trade frame** (T3 `messages.tradeStream`): `{type: "message", topic,
data}`. T3: "`data` 는 REST 체결 조회(`GET /api/v1/trades`)의 체결 항목과
동일한 모양입니다."

- `data` has four required fields: `price` (string, `format: decimal`,
  `maxLength 30`) "체결가"; `volume` (decimal string) "체결 수량";
  `timestamp` (string, `date-time`) "체결 시각"; `currency` (enum `KRW`,
  `USD`, "unknown enum 값을 허용하도록 구현해야 합니다").
- **Time:** ISO-8601 with offset. The field example is
  `"2026-03-25T09:30:42.000+09:00"`, i.e. millisecond precision and a
  `+09:00` offset. No separate zone statement.
- **Sign:** no change or sign fields. `price` examples are unsigned.
- **Side:** none. T3: "프레임에는 누적 거래량·매수/매도 구분이 없고".
- **Sequence / id:** none. T3: "유실 감지용 sequence 필드는 제공되지
  않습니다."
- **Cumulative values:** none. T3: "수신 프레임 합산으로 누적 거래량을
  재구성할 수 없습니다 — 누적값이 필요하면 REST 캔들·현재가를 사용하세요."
- **Session:** T3: "푸시는 모든 세션에서 제공됩니다. … 국내는 KRX 정규장과
  NXT 프리·정규·애프터마켓 합산입니다." No per-frame session field.

**Order-book frame** (T3 `messages.orderbookStream`): `data` has "REST 호가
조회(`GET /api/v1/orderbook`)의 응답과 동일한 모양". It matches T1
`OrderbookResponse`.

- `timestamp` is `["string","null"]`, `date-time`, "데이터 시각. 데이터
  미제공 시 null", and **not required**.
- `currency` is required.
- `asks[]` "매도호가 목록 (낮은 가격순)" and `bids[]` "매수호가 목록 (높은
  가격순)". Each entry is `{price, volume}` as decimal strings ("호가",
  "잔량").
- T4 L41: `timestamp` "마지막으로 호가가 갱신된 시각이라, 호가 변동이 없으면
  이전 시각이 그대로 유지됩니다." There is no sequence field.
- T4 L40: there is no per-level venue field and no separate ask/bid update
  time.
- T4 L38: crossed or locked integrated books are possible ("매도 1호가가 매수
  1호가보다 낮거나 같게 나올 수 있나요? | 나올 수 있습니다").
- Depth is **not documented**. The T1 `krStock` example has 3 levels a
  side; the T3 example has 1 (publisher examples).

### 6.5 Frame encoding

- **JSON text frames only.** Every server frame is a JSON object with a
  top-level `type`: `subscriptions`, `message`, `error` or `pong` (T3
  `channels.connection.description` dispatch table; T2 L456–463).
- The only non-JSON frame is the client's `PING` (T3 `messages.ping`
  `contentType: text/plain`).
- **One record per frame:** `data` is a single object (T3 schemas). No
  count field and no multi-record frames.
- **Encryption:** none documented. All channels are plain JSON over TLS.
- **Numbers:** prices and quantities are decimal **strings**.
- **Character encoding:** not stated. **Inference:** UTF-8, as for any
  WebSocket text frame.

### 6.6 Limits and errors

- **Limits** (T3 `channels.connection.description`; T2 L446–452):

  | Item | Limit | Over limit |
  | --- | --- | --- |
  | Concurrent connections | 2 per account | New one accepted, oldest closed |
  | Subscriptions per connection | 100 (`codes` total) | `too-many-topics` |
  | Declaration rate | 5/s | `rate-limit-exceeded`; "약 1초 대기 후 재선언" — no `Retry-After` |

  T2 L452: "한도를 넘은 선언은 거부되고 기존 구독은 그대로 유지됩니다."
- **`error.code` values** (T3 `messages.errorFrame`; T2 L479–488):
  `wrong-format`, `no-type`, `invalid-type`, `no-codes`,
  `too-many-topics`, `too-many` ("해석 후 구독 수 100건 초과(안전망)"),
  `rate-limit-exceeded`, `internal-error`, `auth-revoked`,
  `server-shutdown`.
- **Reject codes:** `rejected[].code` values are listed in §6.3.
- **Server-initiated disconnects:**
  - `server-shutdown` ("서버 배포 시") and `auth-revoked` (no `id`) are
    each followed immediately by a close.
  - Idle timeout after 180 s, and eviction when over the connection
    limit, come without a close code.
  - Order-channel backpressure: "수신이 2초 이상 계속 막히면 연결이
    종료됩니다" (T2 L439–440).
- **Loss model:** market data is "LOSSY — 수신이 밀리면 중간 프레임이 유실될
  수 있습니다" and "항상 최신 상태 우선" (T3 channel summaries; T2 L438).
  The order channels are LOSSLESS, but only within one connection.

### 6.7 Contradictions and gaps

1. **KRX after-market in the push scope.** T3 (trade and order book) says
   "KRX 정규장과 NXT 프리·정규·애프터마켓 합산", omitting KRX
   after-market. T4 L27 (1-minute candles) includes "KRX 애프터마켓".
   Whether KRX after-market trades are pushed is unresolved; this matches
   trade evidence §6.7 #2.
2. **Venue statement location.** The phrase "국내는 통합 시세(KRX+NXT)만
   노출합니다" is in T2 L384, **not** in T3. T3 says the same thing in other
   words in its declare item descriptions. There is no contradiction.
3. **Token rotation vs. a live connection.** T3 says to "만료 전에 새 토큰을
   발급받아 재연결". T4 L9 says a new token immediately revokes the old
   one, and T3 says revocation closes the connection with `auth-revoked`.
   **Inference:** a seamless overlap (new connection up before the old
   one drops) is impossible, and any REST-side reissue also drops the
   socket.
4. **Order channels share the connection budget.** A stalled `personal:order`
   reader closes the whole connection after 2 s (T2 L439). The 2-connection
   cap (T3) limits how far market data can be isolated from account feeds.
   **Inference**, not a documented recommendation.
5. **Example timestamp outside domestic hours.** The T3 `orderbookMessage`
   example for `orderbook:kr:005930` has `"2026-06-18T23:30:00.000+09:00"`,
   outside every KRX/NXT session that T3 lists. **Inference:** the
   example is illustrative only.
6. **T5 channel list.** T5 L5 and L35 mention trade ticks, order book and
   "personal order events" but not conditional-order events, which T3 and
   T2 L382 document. T5 defers to T3, so this is an omission only.
7. **Two "too many" codes.** `too-many-topics` (request total over 100) and
   `too-many` (resolved total over 100, "안전망") are both documented. When
   the second can occur without the first is not explained.

### 6.8 Gates and not-verified items

See §10 (gates tagged [Toss]) and §11.

## 7. Meritz Securities

### 7.1 Pinned sources

Portal `https://openapi.imeritz.com`, retrieved 2026-11-05 07:57–07:59 UTC.
GitHub repository
[`meritz-securities/open-api@a93c6409db73ea97ad15f7b7186f36c9f32ecd89`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89)
(commit 2026-10-28T22:32:03+09:00; still the default-branch head when
re-cloned at 07:55:53Z). No token, credential, account or MAC value was used,
and no WebSocket connection was opened.

Repo README L11 makes the portal canonical ("API 목록과 파라미터·응답
필드의 정본은 개발자 포털입니다", trade evidence §7.1). M1 is therefore
`field table`. Repo files are `publisher repo note`, `publisher example`
(sample code) or `publisher client code`.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| M1 | Portal spec export [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json) (`title` "메리츠증권 Open API 명세") | 07:57:09Z sha256 `ce7c85787916484d…`, 1,136,519 bytes, `generatedAt "2026-11-05 16:55:11"`. With `generatedAt` removed and `json.dumps(sort_keys=True, ensure_ascii=False)`: `2fff4f3e02d20cd5…`, **identical** to the trade/candle-evidence copies | `groups[4]` "(실시간) 국내주식" (9 APIs): `apis[0]` SOR 통합 `ohhts_unt_cntg`, `[1]` KRX `ohhts_stck_cntg`, `[2]` NXT `ohhts_nxt_cntg`, `[3]` `ohhts_ovtp_cntg`, `[4]` `ohhts_stck_aspr`, `[5]` `ohhts_ovtp_aspr`, `[6]` `ohhts_ovan_cntg`, `[7]`–`[8]` account feeds (named only). Fields `protocol`, `domain`, `url`, `description`, `trs[0].{request,response,requestExample,responseExample}` |
| M2 | [samplecode-py](https://openapi.imeritz.com/samplecode-py) | 07:57:12Z sha256 `5fabbe7775de5f1f…` (varies per request) | Section "06. 실시간 시세 (WebSocket)": endpoint, token-in-message, subscribe/ACK sample, tr_cd list, unknown-symbol behaviour |
| M3 | [howto-use](https://openapi.imeritz.com/howto-use) | 07:57:11Z sha256 `81fe5ed49d3f2eeb…` | Searched; **no WebSocket text** (0 matches for 웹소켓/실시간/websocket/wss:/29443 in the raw HTML) |
| M4 | Notice "API 호출 유량 제어 안내(REST, WEBSOCKET)", JSON at `/api/forums/10000000-0000-0011-0000-000000000001/posts/3dc11098-4ce4-4695-abf5-4c7aa194cb9d` | 07:59:00Z sha256 `9d27d191994f6052…`, `createdDate` 2026-09-23T10:12:28+09:00 | WebSocket session/registration limit (publisher guide). Hash differs from the capability inventory's 06:57:52Z copy (`06570a95…`); **Inference:** its `viewCount` field changes per view. The text was not compared. |
| M6 | repo [`meritz/data/corrections.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/data/corrections.json) | blob `60370924e13233bbd2cccb517bfffee002dad915` | L110–131 "웹소켓 path 는 주소가 아니다"; L150 KRX after-market change |
| M7 | repo [`docs/errors.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/docs/errors.md) | blob `b4b2eac6541bd2b886071c1caad17fa0c57ba3e6` | L47 `00000`; L91 `EGW00002`; L93–94 token errors; L96 `EGW00202`; L97–99 `WSC00106/108/110` |
| M8 | repo [`llms.txt`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/llms.txt) | blob `8351d5343d785b61107179d19197c59a08e1edff` | L95–99 single endpoint, auth in message, ACK; L100 `mac_address` requirement (stated generally); L109–111; L126 reconnect out of scope |
| M9 | repo [`README.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/README.md) | blob `61aa5f7f2c1059a29a99175a5cdf573996d81479` | L86 "실시간 14건 — AsyncAPI 3.0"; L98 `MERITZ_WS_URL` default; L104–105; L125 no paper account |
| M11 | repo [`asyncapi.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/asyncapi.json) | blob `c108c3c52288d5296b2871582ff856d532073242`; `asyncapi 3.0.0`, `info.version "2026-10-22"` | L3–6 info; L7–12 `servers.prod`; channels L15–38 (`ohhts_stck_cntg`), L39 (`nxt`), L63 (`ovtp_cntg`), L87 (`stck_aspr`), L111 (`ovtp_aspr`), L135 (`ovan_cntg`), L205–228 (`unt_cntg`); components L451–693 (`stck_cntg`), L694, L937, L1173–1639 (`stck_aspr`), L1640, L2107, L2815–3064 (`unt_cntg`; `exch_code` L3010–3015) |
| M12 | repo [`examples/07_realtime.py`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/examples/07_realtime.py) | blob `4556366615f91846f08c64b5a31e286afb33af13` | L6–17 connection model; L39 connect; L48–51 subscribe; L63–70 ACK; L77–78 unknown symbols |
| M13 | repo [`meritz/data/catalog.json`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/data/catalog.json) | blob `000c2dbc636ad46077d4f46d67a04e0cd6fe1319`; `generated "2026-10-28"` | L25926–25935 `ws_stck_cntg` (`method "SUBSCRIBE"`, `path "/websocket/ohhts-stck-cntg"`, `tps "10"`); other domestic WS keys at L26354, L26782, L27199, L27979, L28759, L29968 |

**Cross-check:** for all nine M1 `groups[4]` TRs, every body field name,
title, description and length in M11 equals M1 (comparison script
kept outside the repository). M11 differs only in its examples: they are
placeholders (`tr_key "sample"`, `shrn_iscd "1000"`), whereas M1 has
realistic-looking values.

M5 and M10 (trade-evidence IDs) are not used here.

**Missing evidence:**

- No subscribe-ACK or error-frame **schema**. M11 defines only `receive`
  operations. The ACK shape comes from M2 and M12 examples.
- No heartbeat/PINGPONG, reconnect, encryption or close-code text in any
  source.
- No NXT or integrated **order-book** channel. No market-operation or
  VI/halt channel; `trht_yn` and `mkop_clcd` in the trade body are the
  only status fields.
- Token lifetime is not stated in the WebSocket documents.

### 7.2 Connection

- **Endpoint:** `wss://openapi.imeritz.com:29443/websocket`, one endpoint
  for all channels, **real only**.
  - M1 gives `domain` `"wss://openapi.imeritz.com:29443"` + `url`
    `"/websocket"` for every WS API.
  - M2: "실시간 시세는 wss://openapi.imeritz.com:29443/websocket 접속점
    하나로 받고".
  - M11 L10 has host `openapi.imeritz.com:29443/websocket`; M9 L98 gives
    the same default.
  - No paper environment: M9 L125 "모의계좌는 없습니다".
- **Auth: inside each subscribe message, not at the handshake.**
  - M2: "인증도 접속할 때가 아니라 구독 메시지에 넣는 token 으로 합니다."
    M12 L17 and M8 L96 say the same.
  - The M2 and M12 L39 samples open the socket with no headers.
  - The field `token` (String, len 1000) sits in the message `header`: "발급받은
    접근토큰에 "Bearer " 를 붙여 넣습니다. 세션 한도를 넘기면 WSC00110 이
    내려옵니다." M1 description: "접두어가 없으면 EGW00202 로 거절됩니다."
  - The token is the REST access token; there is no separate approval key.
- **`mac_address`:** M8 L100 states the REST requirement generally. No
  WebSocket field table, example or AsyncAPI channel includes a
  `mac_address` field or handshake header. Whether the WebSocket needs it
  is **not documented** (§7.7 #5).
- **Key lifetime / reuse:** not documented for the WebSocket. M7 L93–94
  cover invalid/expired tokens (`EGW00121`, `EGW00123`) in general. What
  happens to live subscriptions when the token expires is **not found**.
- **Heartbeat:** **not found** in M1, M2, M8, M11 or M12.
- **Reconnect:** **not found**. M8 L126: "자동 재시도·백오프와 웹소켓
  재연결은 예제 범위 밖이니".
- **Max connections:**
  - M4: "WEBSOCKET : 2세션" and "*HTS ID 단위로 유량 제한(1개의 HTS ID당
    2세션)" (publisher guide).
  - M7 L99: "`WSC00110` | 계정당 최대 세션 수 초과 | 같은 앱키로 열어 둔
    웹소켓을 먼저 닫으십시오".
  - M12 L9–15 (publisher example): open **one** connection and subscribe
    many times on it. A connection per symbol can leave server sessions
    piling up, "결국 새 구독마다 EGW00002(서버 에러)로 거절되는 상태에 빠질
    수 있다".

### 7.3 Subscription model

- **Message shape** (M1 `requestExample`; M2; M11 `x-subscribe.example`):
  `{"header": {"token": "Bearer <token>", "tr_type": "1"}, "body":
  {"tr_cd": "<tr_cd>", "tr_key": "<6-digit code>"}}`.
- **Fields:**
  - `tr_type` (len 1): ""1" 구독 등록 / "2" 구독 해지. 해지는 등록과 같은
    tr_cd·tr_key 로 보냅니다."
  - `tr_cd` (len 20) selects the channel.
  - `tr_key` (len 9): "구독할 종목의 단축코드 6자리입니다. 예) 005930".
- **Per symbol:** one message per (`tr_cd`, `tr_key`). There is no batch
  form; M12 L47–51 loops one message per symbol on a single connection.
  Many symbols and channels can share one connection.
- **Subscription limits:** M4 "실시간주식체결가 + 실시간주식호가 20건 등",
  verbatim and ambiguous. **Inference:** about 20 registrations per
  session, counted across trade and quote TRs. Not confirmed elsewhere.
  M13 `tps "10"` on WS entries is unexplained.
- **ACK** (M2 example, publisher example):
  - `{"header": {"tr_type": "1", "tr_cd": "ohhts_stck_cntg", "rsp_cd":
    "00000", "rsp_msg": "정상처리되었습니다"}, "body": {}}`. The ACK carries
    no `tr_key`.
  - M7 L47: "`00000` | 실시간 구독 성공 | 관측된 값은 다섯 자리입니다". M2
    and M12 L63–67 accept both `"00000"` and `"0000"`.
- **Error codes on subscribe** (M1 `tr_cd` description): "허용되지 않는
  tr_cd 는 WSC00106, tr_key 를 빼면 WSC00108, 빈 값이면 WSC00107 로
  거절됩니다." The full error list is in §7.6.
- **Unknown symbols are not rejected.**
  - M1 `ohhts_stck_cntg` `tr_key`: "없는 코드나 자릿수가 다른 값을
    넣으셔도 구독 응답은 정상(00000)으로 옵니다."
  - M2: "없는 종목코드를 구독해도 구독 응답은 정상으로 오고 체결 통보만
    오지 않으므로".
  - M12 L77: "서버는 종목코드를 검사하지 않는다."
- **Venue selection by `tr_cd`:**
  - `ohhts_stck_cntg` is KRX.
  - `ohhts_nxt_cntg` is NXT: "같은 종목이라도 정규시장(KRX) 체결은 이
    서비스로 오지 않으므로, 두 시장을 함께 보시려면 각각 구독하십시오".
  - `ohhts_unt_cntg` is "SOR 통합": "정규시장(KRX)과 대체거래소(NXT)의
    체결을 하나로 합쳐".
  - The order book is KRX only (`ohhts_stck_aspr`, "정규시장"), plus the
    시간외단일가 book.
- **Demultiplexing:** data frames echo `header.tr_cd` / `header.tr_key`.
  M1: "한 접속에서 여러 종목·여러 서비스를 구독하셨다면 header 의
  tr_cd·tr_key 로 어느 구독의 데이터인지 가려내십시오."

### 7.4 Market-data channels

All channels below come from M1 `groups[4]`, mirrored in M11. Every body
field is `String`.

| Channel (title verbatim) | TR / channel id | Content | Venue | Frame format (JSON / delimited text / encrypted?) | Evidence |
| --- | --- | --- | --- | --- | --- |
| "(실시간) 국내주식 현재가 (KRX)" — TR name "실시간 주식 현재가 (정규)" | `ohhts_stck_cntg` | One trade per message ("체결이 일어날 때마다 … 한 건씩"), with best bid/ask | KRX ("정규시장(KRX)") | JSON `{header, body}`, plain | field table + publisher example (M2) |
| "(실시간) 국내주식 현재가 (NXT)" | `ohhts_nxt_cntg` | Same 28 fields; "누적거래량 acml_vol 은 이 시장에서 체결된 수량만 더한 값" | NXT | JSON | field table |
| "(실시간) 국내주식 현재가 (SOR 통합)" | `ohhts_unt_cntg` | Same + `exch_code` (29 fields) | KRX+NXT merged, per-trade `exch_code` | JSON | field table |
| "(실시간) 국내주식 호가" — TR "실시간 주식 호가 (정규)" | `ohhts_stck_aspr` | 10-level book + expected-match fields (60 fields) | KRX ("정규시장") | JSON | field table |
| "(실시간) 국내주식 현재가 (시간외단일가)" | `ohhts_ovtp_cntg` | 시간외단일가 trades (27 fields; no `mkop_clcd`) | KRX single-price after-hours | JSON | field table (sparse descriptions) |
| "(실시간) 국내주식 호가 (시간외단일가)" | `ohhts_ovtp_aspr` | 시간외단일가 book (60 fields) | same | JSON | field table |
| "(실시간) 국내주식 시간외예상체결가" | `ohhts_ovan_cntg` | Expected price, "아직 체결된 값이 아니라" | same | JSON | field table |
| "(실시간) 주문 접수 통보", "(실시간) 주문 체결 통보" | `ohhts_cntg_infr`, `ohhts_cntg_rslt` | Account feeds; **named only** | — | JSON | M1 `[7]`–`[8]` |

**Trade body** (`ohhts_stck_cntg`, M1 `apis[1]`; M11 L451–650):

- `shrn_iscd` (9).
- `bsop_hour` (6) "체결이 일어난 시각입니다. HHMMSS 6자리이며 한국시간
  기준입니다." It has **no date** and second resolution.
- `hour_cls_code` (1) "장 구분입니다." Codes: ""0": 장중", ""B": 장 개시 전
  예상", ""C": 09시 이후 예상", ""A": 장 종료 후 예상", ""D": 시간외 단일가
  예상".
- `antc_nmix_cls_code` (1) "예상체결 여부를 나타내는 구분값입니다." No
  code list.
- `prpr` (11) "가장 최근 체결된 가격입니다. 이 메시지가 알리는 체결의
  가격입니다."
- `prdy_vrss_sign` (1): ""1": 상한 "2": 상승 "3": 보합 "4": 하한 "5": 하락".
  `prdy_vrss` (11) is **unsigned**. M1 description: "전일 대비 금액
  prdy_vrss 에는 부호가 붙지 않으므로 방향은 prdy_vrss_sign 으로
  판단하십시오"; M2 says the same. `prdy_ctrt` (9) is "(%)".
- `oprc`, `hprc` and `lprc` are day open/high/low.
- **Side:** `cntg_cls_code` (1): "체결 유형입니다. "1": 매수 체결 · "2": 매도
  체결. 값에 대응하는 이름은 통보에 함께 오지 않으므로 알 수 없는 값도
  오류로 다루지 마십시오." **Inference:** this is an aggressor
  (buyer-/seller-initiated) flag. The documents do not say so.
- `cntg_vol` (11) "이번 체결의 수량입니다. 누적이 아니라 건별 수량입니다."
  `acml_vol` (13) and `acml_tr_pbmn` (13) are cumulative.
  `wghn_avrg_stck_prc` (11) is "누적거래대금을 누적거래량으로 나눈 평균
  단가".
- `askp1`, `bidp1`, `askp_rsqn1`, `bidp_rsqn1` are "체결 시점의 최우선"
  quotes. `total_askp_rsqn` / `total_bidp_rsqn` are also present.
- `rltv` (9) "체결강도입니다." (formula not given). `shnu_rate` (9) "전체
  체결 중 매수 체결이 차지하는 비율(%)".
- `trht_yn` (1): ""Y": 거래정지 / "N": 정상 거래".
- `prdy_vrss_vol_rate` and `prdy_smns_hour_vol_rate` are present.
- `mkop_clcd` (2) "장 운영 상태를 나타내는 코드입니다. 값에 대응하는 이름은
  통보에 함께 오지 않으므로 알 수 없는 값도 오류로 다루지 마십시오." There
  is no code list; the examples show `"20"`.
- **Sequence / trade id:** none.

**Unified feed** (`ohhts_unt_cntg`, M1 `apis[0]`; M11 L3010–3015): body
description "어느 거래소의 체결인지는 함께 오는 거래소코드(exch_code)로
가르십시오".

- `exch_code` (String, **len 2**): "이번 체결이 이루어진 거래소입니다. 값에
  대응하는 이름은 통보에 함께 오지 않습니다." There is **no code list**;
  the M1 example has `"2"`.
- **Inference:** `"1"` = KRX and `"2"` = NXT, as on the REST ticks route
  (trade evidence §7.4, len 1 there). Not documented for the WebSocket.

**Order book** (`ohhts_stck_aspr`, M1 `apis[4]`; M11 L1173–1639):

- `bsop_hour` "호가가 갱신된 시각입니다. HHMMSS 6자리, 한국시간입니다."
- `askp1..10` / `bidp1..10`: "askp1 이 최우선(가장 낮은) 매도호가",
  "bidp1 이 최우선(가장 높은) 매수호가".
- `askp_rsqn1..10` / `bidp_rsqn1..10`. `total_*_rsqn` is "10단계 … 잔량의
  합". There are `*_icdc` deltas "직전 호가 대비" and `ovtm_total_*`
  after-hours totals.
- Expected-match fields: `antc_cnpr` "지금 체결된다면 형성될 가격입니다.
  실제 체결가가 아닙니다.", `antc_cntg_vrss_sign` (same 1–5 codes),
  `antc_cntg_vrss`, `antc_cntg_prdy_ctrt`, `antc_cnqn` and `antc_vol`. M1:
  "단일가 시간대에는 예상체결 항목(antc_cnpr·antc_cnqn·antc_vol)에 값이
  담깁니다."
- `acml_vol`, `wghn_avrg_stck_prc`, and `stck_deal_cls_code` "매매
  구분입니다." (no code list).
- Each message is a full 10-level snapshot (field set). **Inference:**
  not a delta stream, but M1 does not say so explicitly.

### 7.5 Frame encoding

- **JSON** messages `{"header": {...}, "body": {...}}` (M1 `format
  "JSON"`, `contentType "application/json"`; M11 payload schemas; M2
  examples).
  - Data frames: the header has `tr_cd` and `tr_key`.
  - ACK frames: the header has `tr_type`, `tr_cd`, `rsp_cd` and `rsp_msg`;
    the body is `{}`.
  - M2 and M12 L63 tell ACKs apart by the presence of `header.rsp_cd`.
- **Not** `|`/`^`-delimited text. There is no record count field; one
  `body` object per message.
- All numeric values are JSON **strings**. The REST ticks route uses JSON
  numbers (trade evidence §7.4).
- **Encryption:** none documented. 0 matches for 암호/AES in M1 `groups[4]`
  or M11.
- **Character encoding:** not stated. **Inference:** UTF-8 (JSON text).

### 7.6 Limits and errors

- **Sessions:** 2 per HTS ID (M4). Over the limit → `WSC00110` (M1
  `token`; M7 L99).
- **Registrations:** "실시간주식체결가 + 실시간주식호가 20건 등" (M4,
  ambiguous; see §7.3).
- **Codes verbatim** (M7 table; M1):

  | Code | Meaning |
  | --- | --- |
  | `00000` | "실시간 구독 성공" |
  | `WSC00106` | "실시간 미개방 \| 그 서버에서 해당 구독이 열려 있지 않습니다"; M1: disallowed `tr_cd` |
  | `WSC00107` | M1 only: empty value; **absent from M7** |
  | `WSC00108` | "구독 요청 오류 \| `tr_cd`·`tr_key` 형식을 확인하십시오"; M1: missing `tr_key` |
  | `WSC00110` | "계정당 최대 세션 수 초과" |
  | `EGW00202` | missing `Bearer ` prefix (M1); M7 L96 "권한 없음 (게이트웨이 단계)" |
  | `EGW00002` | "서버측 오류" (M7 L91); M12 L15 links it to accumulated sessions |

- **Over-subscription behaviour:** beyond `WSC00110`, not documented.
- **Server-initiated disconnects** and close codes: **not found**.
- **No retry is safe by default** for these read-only subscriptions
  either. Re-subscribing after `EGW00002` is not documented as safe.
  **Inference:** treat it as a session-cleanup problem, not as a
  transient error to retry.

### 7.7 Contradictions and gaps

1. **`prdy_vrss` sign: WebSocket vs REST.** The WebSocket `prdy_vrss` is
   documented unsigned (M1, M2). The REST ticks example has a signed
   `prdy_vrss` (`-1136000` with sign `"5"`, trade evidence §7.4). A shared
   decoder must apply `prdy_vrss_sign` for the WebSocket and must not
   assume one convention for both.
2. **After-hours regime change vs. 시간외단일가 channels.** M6 L150 (repo
   note): "2026-09-14 부터 KRX 시간외 단일가(16:00~18:00)가
   애프터마켓(16:00~20:00, 실시간 체결)으로 바뀌어". Yet M1 still lists
   `ohhts_ovtp_cntg`, `ohhts_ovtp_aspr` and `ohhts_ovan_cntg` as 시간외
   단일가, and `hour_cls_code` keeps `"D": 시간외 단일가 예상`. Which
   channel carries KRX after-market (16:00–20:00) trades is **not
   documented**.
3. **Per-channel "path" is not an address.**
   - M13 L25931 lists `path "/websocket/ohhts-stck-cntg"` (and similar
     paths for the others), plus `method "SUBSCRIBE"`.
   - M1 has `url "/websocket"` and `method "POST"` for every WS API.
   - M6 L126–129: "웹소켓 path 는 주소가 아니다 … 접속점은 domain 하나뿐입니다
     (wss://openapi.imeritz.com:29443/websocket) … path 는 포털 화면 구분용
     슬롯이며 주소가 아닙니다."
   - M6 L129 also says "asyncapi.json 은 13채널 모두 address 가 "/"
     입니다", but M11 has **14** channels (M9 L86 "14건"). The M6 key list
     omits `ws_cntg_exst`.
4. **ACK success code digits.** `00000` (5 digits) per M1, M2 and M7, vs
   REST `0000`. M7 L47 says the publisher could not confirm the digits
   are always different, and the samples accept both.
5. **`mac_address` for the WebSocket.** M8 L100 says the header is
   mandatory, but every WebSocket sample (M2, M12 L39, L48–51) and field
   table omits it. This is unresolved. (The publisher's MAC-derivation
   helper is deliberately not described.)
6. **Field-table placement of `token`/`tr_type`.** M1 lists them right
   after the `header` element (nested by order). M13 tags them `"location":
   "body"`, while all examples put them in `header`. Follow the examples
   plus M1.
7. **`exch_code` length/codes differ from REST.** The WebSocket has len 2
   and no code list. REST has len 1 with `"1"` KRX and `"2"` NXT.
8. **Unified cumulative volume.** Whether `ohhts_unt_cntg.acml_vol` sums
   KRX+NXT is not stated. **Inference** from M1 examples: unified
   `15219368` ≈ KRX `7190656` + NXT `8028606` = `15219262`. The values
   are close but not equal, so the snapshots are not simultaneous;
   illustrative only.
9. **Example inconsistencies (illustrative values):**
   - In M1 `ohhts_stck_aspr`, the levels are around 100,200 while
     `antc_cnpr` is `270000`. Level residuals sum to 12,035 ask vs
     `total_askp_rsqn` `1199507`, and `antc_cnqn` is `"-50"`.
   - M1 `ohhts_ovtp_*` examples have `bsop_hour` `110925` / `134219`
     with `hour_cls_code` `"0"`, i.e. regular-session times on
     after-hours channels.
   - Every trade example has `shnu_rate` `"0.00"` beside `rltv` of about
     80.
   - Consistent: `wghn_avrg_stck_prc` = ⌊`acml_tr_pbmn` / `acml_vol`⌋ in
     all three trade examples, e.g. 1,920,226,409,250 / 7,190,656 →
     267,044.
10. **Repo examples are placeholders.** M11 examples (`tr_key "sample"`,
    `shrn_iscd "1000"`) differ from M1's. Use neither as a fixture.
11. **AsyncAPI host includes a path.** M11 `servers.prod.host` is
    `openapi.imeritz.com:29443/websocket` instead of using `pathname`, and
    channel `address` is `"/"`. Tools may build the URL wrongly.

### 7.8 Gates and not-verified items

See §10 (gates tagged [Meritz]) and §11.

## 8. Cross-broker comparison

### 8.1 Cross-broker table

Facts only; each cell is backed by the broker's section. "n/d" means not
documented in the pinned sources.

| Concern | KIS (§2) | Kiwoom REST (§3) | LS (§4) | DB (§5) | Toss (§6) | Meritz (§7) |
| --- | --- | --- | --- | --- | --- | --- |
| Endpoint / TLS | `ws://` only, **no TLS** | `wss://` | `wss://` | `wss://` | `wss://`, "TLS 필수" | `wss://` |
| Paper endpoint | `:31000` (`ws://`) | `mockapi` host | `:29443` (L1 only) | `:17070` | none | none |
| Auth carrier | separate approval key in every subscribe header | REST token in a LOGIN packet (client code) | REST token in every message `header.token` | REST token in every message `header.token` | REST token as `Authorization: Bearer` on the handshake | REST token "Bearer …" in every message `header.token` |
| Subscribe shape | `header{approval_key, tr_type, custtype}` + `body.input{tr_id, tr_key}` | `{trnm, grp_no, refresh, data[{item, type}]}` | `header{token, tr_type}` + `body{tr_cd, tr_key}` | `header{token, tr_type}` + `body{tr_cd, tr_key}` | one JSON array = the **whole** subscription set | `header{token, tr_type}` + `body{tr_cd, tr_key}` |
| Register / unregister | `tr_type` `1` / `2` (docstrings say `0`) | `trnm` `REG` / `REMOVE` | `tr_type` `3` / `4` (`1`/`2` = account) | `tr_type` `1` / `2` (`3` = account) | re-declare without the item; `[]` clears all | `tr_type` `1` / `2` |
| Symbol key | 6-digit code | code, `_NX`, `_AL` suffix | 6-digit (KRX); 10 chars, space-padded (`N…`/`U…`) | `"J 005930"`, `"NJN-005930"`, `"UJU-005930"` | 6-character code in `codes[]` | 6-digit code |
| Venue selection | TR id per venue | item suffix | TR code per venue | `tr_key` prefix; one TR | none: integrated only | `tr_cd` per venue (trades); book KRX only |
| Frame format | `flag\|tr_id\|count\|payload`, `^` fields | JSON, `values` by field id | JSON, string values | JSON, string values | JSON, `type`-dispatched | JSON, string values |
| Records per frame | `count` field | `data` list (one in examples) | one (n/d) | one (n/d) | one | one |
| Encryption | AES-256-CBC on some channels (which: n/d) | none | none | none | none | none |
| Heartbeat | server `PINGPONG` → pong control frame | server `PING` → echo (client code) | n/d | n/d; first send within 10 s (repo note) | client `PING` < 180 s → `{"type":"pong"}` | n/d |
| Connection limit | n/d | n/d | 3 per app key | 2 per app (repo note) | 2 per account, oldest evicted | 2 per HTS ID |
| Subscription limit | n/d (client "40" miscounts) | n/d | 200 per session (planned) | 50 symbols per session (repo note) | 100 per connection | "20건 등" (ambiguous) |
| Subscribe ack | JSON, `rt_cd`, "SUBSCRIBE SUCCESS" | `return_code` `0`/`1` | `rsp_cd` (console code only) | n/d (overseas sample only) | `type: "subscriptions"`, `rejected[]` | `rsp_cd` `00000`, also for **unknown symbols** |
| Per-trade side | `CCLD_DVSN`/`CNTG_CLS_CODE`; codes legacy only | sign of `15` "+는 매수체결,-는 매도체결" | `cgubun` "+ : 매수 / - : 매도" | `CntgClscode`, no code list | **none** | `cntg_cls_code` "1": 매수 체결 · "2": 매도 체결 |
| Date in trade frame | `BSOP_DATE` | none | none | `BsopDate` (S00 only) | full ISO-8601 with `+09:00` | none |
| Time zone stated | no | no | no | no | offset in value | "한국시간" |
| Trade id / sequence | none | none | none | none | none ("sequence 필드는 제공되지 않습니다") | none |
| Book depth | 10 | 10 | 10 | 10 | n/d (examples 1–3) | 10 |
| Book time / date | `BSOP_HOUR` / none | `21` "HHmmss" / none | `hotime` / none | `BsopHour` / none | nullable `timestamp` | `bsop_hour` / none |
| Market-operation feed | per-symbol `H0STMKO0` family | `0s`, `1h` | `JIF` | none | none | none |

### 8.2 What a common `watch_*` surface could rely on

Everything in this subsection is **Inference:** from the six sections. No
`watch_*` method is proposed.

- **Common lifecycle only.** All six follow connect → authenticate →
  subscribe → server push → unsubscribe or close. Everything else differs:
  credential carrier (four models), heartbeat direction (server-initiated
  for KIS and Kiwoom, client-initiated for Toss, undocumented for LS, DB
  and Meritz), and subscription semantics (incremental for five,
  declarative full replace for Toss). A common layer would have to hold
  the desired subscription set itself and translate it per broker.
- **No shared protocol constants.** `tr_type` `1` means "subscribe market
  data" for KIS, DB and Meritz but "register account" for LS. Codes must
  be per broker, never shared.
- **`watch_trades`.** Only Toss ("체결이 발생할 때마다") and Meritz
  ("건별 수량") say one record is one execution. **No broker has a trade id
  or sequence**, and Toss states its market data is lossy. A common
  surface could not promise completeness, de-duplication or gap
  detection, and a reconnect is always a gap.
- **Side.** Documented for Kiwoom, LS and Meritz; code list missing for
  DB; legacy-only for KIS; absent for Toss. A common `side` must be
  optional.
- **Time.** Only Toss gives a full timestamp. KIS and DB `S00` add a date
  field whose format is not specified as a contract; Kiwoom, LS and
  Meritz give time of day only. Only Meritz states the zone in words.
  Under the market-data spec's rule against invented timestamps, most
  `timestamp` values would have to stay `None` without a verified trading
  date.
- **`watch_order_book`.** Five brokers expose 10 fixed levels; Toss depth
  is undocumented. Only Toss documents full snapshots; for the others,
  snapshot rather than delta is an inference from fixed fields.
- **Venue.** Venue selection uses four mechanisms (TR id, suffix,
  prefix, none). Toss is integrated-only; Meritz has no NXT or SOR book;
  DB `ExmrClsCode` `1` covers both KRX and integrated. Venue must stay
  explicit and streams must never be merged.
- **Subscription health.** Meritz acknowledges unknown symbols with
  `00000`, and Toss sends no initial snapshot. An ack alone does not prove
  data will arrive.
- **Market operation.** Only KIS (per-symbol, VI-oriented), Kiwoom
  (market-wide coded events) and LS (`JIF`, market-wide) have a feed, and
  they are different concepts. No common `watch_market_status` is
  supported by the evidence.

## 9. Relation to existing repository documents

None of the files below is edited by this change. Differences are
recorded here only.

| Document and claim | This audit |
| --- | --- |
| [capability inventory](capability-inventory-2026-11-05.md) row 11, KIS: `H0STCNT0` 체결, `H0STASP0` 호가; `ws://ops.koreainvestment.com:21000` (paper :31000) · EX · K9, K10 | **Confirmed** at the same blobs (K2, K4, K10). Adds NXT/통합 variants, `H0STMKO0`/`H0NXMKO0`/`H0UNMKO0` and the `/tryitout` path (§2.2, §2.4). |
| Same file, note: "K9 lists WebSocket origins as plain `ws://` … a transport-security gate before any WS work" | **Confirmed**; adds that the approval key is sent in every subscribe message (§2.2); this is now gate G-W2 (§10.1). |
| Same row, Kiwoom: `0B`, `0D`; `wss://api.kiwoom.com:10000` `/api/dostk/websocket` · FT | **Confirmed** (W1 L96918–96920). Adds `0C`, `0s`, `1h` and the client-only LOGIN packet (§3.2). |
| Same file, Kiwoom note: no REST market-calendar API; "only WS `0s` 장시작시간" | **Confirmed**; the `215` code list is recorded verbatim in §3.4. |
| [trade evidence](trade-evidence-2026-11-05.md) §2.5: `H0STCNT0` `CCLD_DVSN` "체결구분" with "no value list in K13" | **Confirmed** for that blob (K5). A legacy list exists: "1:매수(+), 3:장전, 5:매도(-)" (K22 L137, legacy); NXT/통합 use `CNTG_CLS_CODE` (§2.4). |
| Same file §3.5: `0B` field `15` "+는 매수체결,-는 매도체결" (W1 L97214) | **Confirmed** at the same line. |
| [order-book evidence](order-book-evidence-2026-11-05.md): no WebSocket channel cited; Kiwoom REST price sign meaning "not stated"; KIS REST book has no symbol echo | `0D` prices are also "부호가 포함된 숫자" with no stated meaning (§3.4). The KIS WS book **does** carry `MKSC_SHRN_ISCD`, unlike the REST route. |
| [kis-market-data.md](kis-market-data.md) L43–45: KIS says to use WebSocket for real-time feeds | Consistent; the underlying KIS statement was not re-verified here. |
| [market-data spec](../specifications/market-data-v0.1-draft.md) L266: "no WebSocket streaming" | Unchanged. Any `watch_*` method needs a spec change and a maintainer decision first (§10). |
| [candle evidence](candle-evidence-2026-11-05.md) L872: Toss WebSocket text "국내는 통합 시세(KRX+NXT)만 노출합니다" | **Confirmed** at T2 L384 (same sha256 as the trade-evidence copy); T3 says the same in other words (§6.3, §6.7 #2). |
| Capability inventory row 11, LS: `S3_`/`H1_` (KRX), `NS3`/`NH1` (NXT), `US3`/`UH1` (통합); `wss://openapi.ls-sec.co.kr:9443` (simulation :29443) · FT · L1 | **Confirmed** (§4.2–§4.4). Adds `K3_`/`HA_` and `JIF`, and the 3-sessions-per-app-key notice (§4.6). |
| Same file, LS note: "WS path differs between L1 (`/websocket`) and L2 (`/websocket/stock`, `/websocket/etc`)" | **Confirmed** (§4.7 #1); **Inference:** `accessUrl` is a portal grouping label. |
| Same row, DB: `S00` 체결, `S01` 호가; `wss://openapi.dbsec.co.kr:7070/websocket` (demo :17070) · SDK · D5, D6 | **Confirmed** (§5.2). Adds the session, symbol and connect-rate limits (repo notes) and the state-changing `DisconnectSession` (§5.2, §10.2). |
| Same row, Toss: `realtime-trade`, `realtime-orderbook`; `wss://openapi-ws.tossinvest.com/ws/v1` · OAS · T2 | **Confirmed** (§6.2–§6.4) with T1–T5 unchanged since the trade audit. |
| Same row, Meritz: `ohhts_stck_cntg`, `ohhts_stck_aspr` (+NXT/SOR); `wss://openapi.imeritz.com:29443` | **Partly confirmed:** NXT and SOR variants exist for **trades only**; the book is KRX only (§7.3–§7.4). |
| Same file, Meritz notes: "M4: … WebSocket 2 sessions per HTS ID"; "WS path differs between M1 (`/websocket`) and M2 (`/websocket/<tr>`)" | **Confirmed** (§7.2). The publisher's own note says the per-channel path "는 주소가 아니다" (§7.7 #3). |
| [trade evidence](trade-evidence-2026-11-05.md) §6.7 #2: Toss WebSocket push scope omits KRX after-market | **Unchanged** and still unresolved (§6.7 #1). |
| Same file §6.4: Toss WebSocket "sequence 필드는 제공되지 않습니다" | **Confirmed** (§6.4). |
| Same file §7: Meritz notice summarised by the capability inventory, "not re-verified" | Retrieved here (M4, 07:59:00Z): "WEBSOCKET : 2세션", HTS-ID based (§7.2). Its REST wording was not compared. |

## 10. Implementation gates

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any WebSocket client, decoder,
subscription plan or public `watch_*` method is written. Broker tags are
in brackets.

### 10.1 Common gates (all six brokers)

- **G-W1 — No connection without authorization.** No WebSocket
  connection, approval-key issuance, LOGIN or token issuance for
  WebSocket use, real or paper, without a **separate explicit
  authorization** naming the broker, environment and purpose. No
  WebSocket connections in CI.
- **G-W2 — Never send a credential over plaintext.** No approval key,
  access token or other credential may be sent over an unencrypted
  connection. **[KIS]** documents only `ws://` (K2 L28, L30), and its
  approval key travels in every subscribe message (§2.2, §2.3), so a KIS
  WebSocket connection is **blocked** until a TLS endpoint is documented
  by KIS or the maintainer records an explicit decision. KTradeLink must
  not silently try `wss://`, nor silently fall back to `ws://`. The same
  rule applies to any future broker or environment.
- **G-W3 — Approval keys and tokens are credentials: never logged.**
  Approval keys, access tokens, LOGIN packets, subscribe messages that
  embed a token, and KIS AES keys and IVs must never appear in logs,
  errors, panics, fixtures, screenshots or review material. Publisher
  examples that log them (K1 L698, L779; K21 L152, L254) are not safe
  patterns.
- **G-W4 — Explicit environment.** No silent LIVE/PAPER fallback and no
  environment-variable endpoint override (Kiwoom W3 L28–49). Toss and
  Meritz have no paper WebSocket at all.
- **G-W5 — Timestamps.** Time-of-day fields are not timestamps. No date
  guessing from the local clock (as legacy K22 L347 does). Date fields
  (KIS `BSOP_DATE`, DB `BsopDate`) and zones are unverified except where a
  broker states them (Toss offset, Meritz "한국시간").
- **G-W6 — Ordering, loss and gaps.** No broker has a trade id or
  sequence. A reconnect, an eviction or a lossy drop is a gap and must be
  surfaced. No automatic REST backfill merged into a stream without a
  maintainer decision.
- **G-W7 — Signs and side.** Never drop a sign or apply `abs()` silently;
  never infer a side that is not documented; keep unknown codes visible
  instead of mapping them to a default.
- **G-W8 — Limits.** Client-side caps are not server limits.
  Over-subscription and over-connection behaviour must not be probed
  live. Back-off must respect each broker's documented connect rate.
- **G-W9 — Reconnect and re-auth.** Reconnect and re-subscribe only
  market-data channels, with bounded back-off; never issue keys or tokens
  in a loop, and never re-send anything order-related. An error or close
  is not evidence that a retry is safe.
- **G-W10 — Account feeds out of scope.** Account and order-fill feeds
  (KIS `H0STCNI0`/`H0STCNI9`; Kiwoom `00`/`04`; LS `SC0`–`SC4`; DB
  `IS0`/`IS1`; Toss `personal:*`; Meritz `ohhts_cntg_infr`/
  `ohhts_cntg_rslt`) need their own authorization.
- **G-W11 — Venue.** KRX, NXT and integrated/SOR streams stay separate
  and labelled; no client-side merging.
- **G-W12 — Unknown frames.** Unknown message kinds and codes are
  reported without payload and never treated as success.

### 10.2 Broker-specific gates

- **[KIS]**
  - Plaintext transport: G-W2 blocks connection.
  - Decrypt only on a documented trigger; the ack `encrypt` flag and the
    frame flag disagree in publisher code, so an unknown or inconsistent
    flag fails closed.
  - Honour the frame `count`; a field count that is not
    `count × columns` fails closed. Column lists differ by venue and have
    changed over time; pin them to a versioned source.
  - Side codes are legacy-only; `H0UNMKO0` frames cannot be attributed to
    a symbol from the payload.
- **[Kiwoom]**
  - LOGIN and PING exist only in client code; capture them with
    authorization before relying on them.
  - The sign of `15` is the only documented side; price signs are
    undocumented.
  - Do not trust `W_PRD`/`W_MOCK` overrides.
- **[LS]**
  - Market data uses `tr_type` `3`/`4`; `1`/`2` register **account**
    feeds. Never reuse DB, KIS or Meritz codes.
  - NXT and integrated TRs are `NS3`/`NH1` and `US3`/`UH1` (three
    letters, no underscore); their `tr_key` is 10 characters with trailing
    spaces. Padding is portal-console behaviour, not a stated server
    rule.
  - Honour 3 sessions per app key; plan for the announced 200
    subscriptions per session (TR × symbol). Both are publisher guidance,
    not server-verified.
  - Obtain authorized sanitized captures of the ack, an error frame, an
    over-limit response, a falling-price trade (`sign`, `change`) and a
    pre-open book before any decoder. Do not infer the ack shape from
    portal JavaScript.
  - Treat numerics as strings; tolerate `""` and `" "`; fail closed on
    unknown `status`, `donsigubun` or `jstatus` codes, and read `jstatus`
    together with `jangubun`.
  - Keep `krx_`/`nxt_`/`unt_` quantities apart; read US3 `exchname` per
    frame.
- **[DB]**
  - `tr_type` numbering is the reverse of LS: `1` subscribe, `2`
    unsubscribe, `3` account. Sending LS codes to DB would register an
    account feed.
  - KRX and integrated frames share `ExmrClsCode` `1`, and `S01` has no
    venue field: keep `J`, `NJ` and `UJ` subscriptions distinct and never
    read `1` as "KRX".
  - **`DisconnectSession` (REST session reset) changes server state** for
    every session of the account. It must never be called implicitly,
    automatically or as part of reconnect; it needs separate explicit
    authorization.
  - Honour 2 sessions, 50 symbols per session, 6 connects per minute and
    the 10-second first send (repo notes; enforcement unverified).
  - Match field names case-insensitively or against both observed forms;
    never default unknown `CntgClscode`, `PrdyVrsssign`, `HourClscode` or
    `NewMkopclscode`; treat `…clr` fields as display hints, not signs.
  - Capture one KRX, one `NJ` and one `UJ` frame for `S00` and `S01`, the
    ack and the error/session-limit frames before any decoder.
- **[Toss]**
  - The subscription message **replaces the whole set**; a partial
    declaration silently unsubscribes everything left out.
  - 2 connections per account; a third connection evicts the **oldest**
    without a close code. Any second client on the same account can
    silently kill a KTradeLink stream.
  - 100 subscriptions per connection and 5 declarations per second.
  - Market data is **lossy**; never derive cumulative volume or claim
    completeness.
  - **A token reissue revokes the old token and drops the live socket**
    (`auth-revoked`), including a reissue made for REST. Token handling
    needs a design decision first.
  - No aggressor side and no per-trade venue: keep venue `INTEGRATED`,
    never map it to KRX. The order-book `timestamp` may be `null`; do not
    substitute receive time. Do not hard-code a book depth.
- **[Meritz]**
  - Unknown symbols are still acknowledged with `00000`; subscription
    health cannot be inferred from the ack.
  - Whether `mac_address` is required on the WebSocket is **unresolved**.
    No MAC value or discovery may be added without explicit maintainer
    authorization.
  - KRX after-hours changed on 2026-09-14 (single price 16:00–18:00 →
    after-market 16:00–20:00), but the 시간외단일가 channel names and
    codes are unchanged; which channel carries after-market trades is
    undocumented.
  - The WebSocket `prdy_vrss` is unsigned; reconstruct the signed change
    from `prdy_vrss_sign` and do not share the REST convention.
  - `cntg_cls_code` "1"/"2" as an aggressor side is an inference; keep
    unknown values. `exch_code` decoding is unverified. There is no NXT or
    SOR order book.
  - Treat `EGW00002` as a session-cleanup problem, not a transient error.

## 11. Not verified

- Any live or paper WebSocket frame, ack, heartbeat or close for any
  broker. No connection was made.
- Entitlements, real/paper parity and redistribution rights.
- **[KIS]**
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
- **[Kiwoom]**
  - the LOGIN packet and ack (client code only), token lifetime on a live
    socket, and PING interval;
  - subscription, group and connection limits; `grp_no` semantics;
  - array vs string `item`/`type`; multi-entry `data` frames;
  - meaning of price signs; code lists for `9081`, `0D` `215`, `9068`,
    `9069`; time zone;
  - whether `1700`–`1702` apply to REG packets; close codes;
  - `_AL` (SOR) frames and how `9081` labels them.
- **[LS]**
  - the ack and error frame shapes and codes (portal console code only);
  - heartbeat, reconnect and close behaviour;
  - the connect path (`/websocket` vs `accessUrl`), and paper (`:29443`)
    behaviour, token type and symbol coverage;
  - server enforcement of 3 sessions and the planned 200 subscriptions;
  - `tr_key` padding as a server rule, and what "연속" means;
  - the WebSocket `sign` code list and falling-price `change`;
  - `status` codes (examples `"00"` vs listed `' 0'`), the `value` unit,
    time zone;
  - whether unclassified volume in US3/S3_/K3_ is auction prints.
- **[DB]**
  - the ack shape for `S00`/`S01` (only an overseas sample exists);
  - server enforcement of the session, symbol, connect-rate and
    10-second rules (repo notes only), and over-limit responses;
  - the meaning of per-TR `requestLimit` `2` on a WebSocket TR;
  - code lists for `CntgClscode`, `PrdyVrsssign`, `HourClscode`,
    `NewMkopclscode`, `CnccAsprclscode`, `CompClscode`;
  - `ShrnIscd` format, `ExmrClsCode` for `NJ`/`UJ`, `header.tr_key`, and
    field-name case in real frames;
  - the connect path (`/websocket` vs `/pub/<tr>`); paper coverage; time
    zone; token expiry on a live socket.
- **[Toss]**
  - whether KRX after-market trades are pushed;
  - order-book depth;
  - how often frames are dropped under load;
  - when `too-many` occurs without `too-many-topics`;
  - behaviour of a token reissue on a live socket beyond the documented
    `auth-revoked` close.
- **[Meritz]**
  - the ack and error-frame schemas (examples only);
  - heartbeat, reconnect, close codes and token expiry on a live socket;
  - whether `mac_address` is required;
  - the meaning of "20건 등" and of catalog `tps "10"`;
  - which channel carries KRX after-market trades since 2026-09-14;
  - `exch_code` values, `mkop_clcd` and `stck_deal_cls_code` codes, and
    whether `ohhts_unt_cntg.acml_vol` sums KRX and NXT.
