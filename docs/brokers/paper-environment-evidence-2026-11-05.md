# Six-broker paper / mock environment (모의투자) evidence — 2026-11-05

- **Scope:** what the publishers document about their paper (모의투자,
  mock, VTS, demo) environments for domestic equity: how paper is selected,
  REST and WebSocket origins, token routes, TR-id / api-id differences,
  which market-data routes are offered in paper, and paper-only limits.
  Account and order differences are **named only**. Brokers: KIS, Kiwoom
  REST, LS, DB, Toss and Meritz. The Shinhan comparison stays separate.
- **Purpose:** to decide what a future, separately authorized smoke test
  could check against a paper environment first (§8), and what paper
  evidence can never prove about production.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** This file does not authorize any paper or live call,
  credential use, account access or order.
- **No broker API request was sent**, to a paper or a production gateway.
  No token, credential, account, MAC value or order was used. No portal
  account was registered or logged into. Only public Git repositories,
  public portal pages and publisher JSON documentation endpoints were
  fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS and Kiwoom: shallow clones of the pinned commits, 07:54–07:56;
    `git ls-remote` showed each pinned SHA as the remote `HEAD`.
  - DB and Meritz: the pinned commits fetched with `git fetch --depth 1`,
    07:54:53 and 07:54:54 (§5.1, §7.1).
  - KIS developer portal JSON and pages: 07:58:57–08:02:22 (§2.1).
  - DB portal JSON and pages: 07:55:50–07:58:11 (§5.1).
  - Toss public documents: 07:58:32–07:59:18 (§6.1).
  - Meritz portal pages and JSON: 07:59:54–08:01:12 (§7.1).
  - Kiwoom portal home page: 08:03 (§3.1).
  - LS portal pages and JSON guides: 08:05:40–08:07:26 (§4.1).
- **Not retrieved** (recorded, not worked around): Kiwoom portal guide and
  notice pages (connection reset / 404, §3.1); LS forum JSON (HTTP 302,
  §4.1); KIS and DB homepage pages outside the Open API portals (§2.1,
  §5.1).
- **Spot checks before merge:** for each of the six brokers at least two
  pins (Git blob SHA or sha256 prefix) and the quoted lines were
  recomputed from the retrieved copies; all matched, after one quotation
  attribution in §6.3 was corrected (T1, not T3 L9).
- **Pin formats:**
  - Git blob SHAs are `sha1("blob <len>\0" + bytes)` of the retrieved
    bytes, i.e. what `git hash-object` and `git ls-tree` print. They were
    computed from the cloned files.
  - Line numbers are written "(K2 L453–455)": source K2, lines 453–455.
  - Web pages and portal JSON have no immutable revision. Their sha256
    prefix identifies only the copy retrieved at the stated time. Where a
    portal record carries a publisher timestamp (`lastModifiedDate`,
    `createdDate`, a `version`), it is quoted.
  - Raw copies were kept outside the repository. Sample tokens, app keys,
    account numbers, HTS IDs, MAC values, IPs and staff identifiers in
    publisher material are deliberately not copied; key and variable
    **names** are quoted where they identify a mechanism.
- **Evidence levels:**
  - `field table`: a publisher field or spec table, including portal API
    records that carry per-API domain and TR-id fields.
  - `publisher guide`: portal prose outside the API specification (FAQ,
    notices, onboarding pages). It ranks below `field table`.
  - `publisher example`: sample request/response or sample code.
  - `publisher client code`: SDK or helper behaviour. It shows how the
    publisher calls the route; it is **not** a contract.
  - `legacy publisher example`: material under a publisher repository's
    `legacy/` directory; lower weight than current examples.
  - `publisher repo note`: non-code text in a publisher repository.
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.

## 1. Broker × concern summary

Cell format: short verdict — evidence. `F` field table, `G` publisher
guide, `E` publisher example, `C` publisher client code, `L` legacy
publisher example, `N` publisher repo note, `—` not found.

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Paper exists? | yes, "모의투자" (F+G+C) | yes, "모의투자" / `MOCK` / `demo` (F+C+N) | yes, "모의투자 OPEN API" applied for separately (G) | yes, "모의투자"; SDK mode `demo`, key prefix `vtl_` (G+N+C) | **not found** in any public document (F+G) | **no**: "현재 메리츠증권에서는 Open API 모의투자 기능을 제공하지 않습니다." (G); "모의계좌는 없습니다" (N) |
| Selection mechanism | separate origin **and** separate app key; trading TR ids switch to `V…` (F+G+C) | separate origin and separate app key; same api-id; wrong pairing → `8030`/`8031` (F+N) | separate app key (G); REST origin selection **not documented**; onboarding says "tr_id 값이 실전/모의를 구분해요" (G, non-authoritative) | same REST origin; "발급받은 앱 키의 속성으로 서버가 분기합니다." (N); separate paper app key "(모의투자 별도 발급)" (G); WS port differs | — (one production server) | — ; the portal "테스트베드" only replays guide examples and sends no request (G) |
| REST origin | `https://openapivts.koreainvestment.com:29443` vs `https://openapi.koreainvestment.com:9443` (F+G+C) | `https://mockapi.kiwoom.com` vs `https://api.kiwoom.com` (F+E+C) | **no paper REST origin documented**; guide lists only `https://openapi.ls-sec.co.kr:8080` (F); onboarding sends paper orders to `:8080` (G) | **same** `https://openapi.dbsec.co.kr:8443` for both; portal `simulatedDomain` null (F+N) | only `https://openapi.tossinvest.com` (F) | only `https://openapi.imeritz.com:9443`; `simulatedDomain` null for all 87 APIs (F) |
| WS origin | `ws://ops.koreainvestment.com:31000` vs `:21000`, plain `ws://` in both (F+C) | `wss://mockapi.kiwoom.com:10000` vs `wss://api.kiwoom.com:10000` (F+C) | `simulationUrl` `wss://openapi.ls-sec.co.kr:29443` vs `:9443` (F) | `wss://openapi.dbsec.co.kr:17070/websocket` vs `:7070` (F+N) | only `wss://openapi-ws.tossinvest.com/ws/v1`, server keyed `production` (F) | only `wss://openapi.imeritz.com:29443/websocket` (F) |
| TR-id change | market-data TR ids identical (F); trading TR ids `T…` → `V…` (F+G); sample client rewrites leading `T`/`J`/`C` (C); WS 체결통보 `H0STCNI0` → `H0STCNI9` (F) | none: same `api-id` in both (F+E) | not documented in the guide (F); onboarding uses a different order TR for paper (G, conflicts with the catalog) | none: identical TR codes (N) | n/a | n/a |
| Market-data availability | per-API "모의 Domain" / "모의 TR ID" fields; current price, order book, day candles, today's minute candles and trades **offered**; by-date minutes, symbol info, holidays, VI, NXT/통합 WS: "모의투자 미지원" (F) | no per-API column; all 337 spec entries list a 모의투자 domain (F); only `ka01690` says "해당 API는 모의투자를 지원하지 않습니다" (F); error `8104` "모의투자에서 지원하지 않는 API 입니다." (F) | **not found**: no per-TR paper flag in the guide (F) | repo matrix ⭕ for `PRICE`, `HOGA`, `CONCLUSION`, `CHARTMIN`/`CHARTDAY`, `JCODES`, `S00`/`S01` (N); since 2025-10-23 paper quote calls are served by the **production** quote system (G); portal phrase rule contradicts the matrix (§5.6) | no paper environment (—) | no paper environment (G) |
| Paper limits | REST "(모의투자) 1초당 1건" vs "(실전투자) 1초당 18건"; token 1/s (G); paper NXT unsupported for trading (G); paper run by a separate operator (G) | no paper number found; rate codes `1700`–`1702` without numbers (F) | no paper number found; per-TR `transactionPerSec` only (F); paper fills only "정규장 시간(09:00~15:30)" (G) | no paper-specific figures; per-app 20 TPS and token 1/min not split by environment; WS "모의투자 - 40세션" per port (G); paper-only `M001`/`M100` messages and success `00000` "모의투자 데이터가 없습니다." (N) | n/a; production only: token re-issue revokes the previous token (F+G), IP allow-list (G) | n/a; every call reaches a real account (G+N) |

## 2. KIS (Korea Investment & Securities)

### 2.1 Pinned sources

Git sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362).
The full SHA is `3a9be59a3ed8745720dc3aa9d584bdf3b7830362` (commit dated
2026-10-28T00:26:05+09:00 per [trade evidence](trade-evidence-2026-11-05.md) §2.1, same SHA). It
was the remote `HEAD` at retrieval. `…/` stands for
`examples_llm/domestic_stock/`.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | [`kis_devlp.yaml`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/kis_devlp.yaml) | `9d8615d34ef2135566186d0fee36474ed54de491` | Config key **names** (L2–17) and the four origins (L26–30). Same blob as the capability inventory's K9. |
| K2 | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) | `0e722d6f3253033efe3cf2b99845397b2b329655` | Publisher client: `prod`/`vps` switch, token files, TR-id rewrite, pacing. Identical blob at `examples_user/kis_auth.py`. |
| K3 | [`README.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/README.md) | `182887151f1fb07e5789a029292ac3e43d3ba9bd` | Separate paper keys (L222, L248–250); `EGW00201` note (L414–417) |
| K4 | [`MCP/Kis Trading MCP/Readme.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/Readme.md) | `3069ae6fba2173165cc82c74c3a9f1aaec07486d` | Paper credential variable names (L66–74) |
| K5 | [`MCP/Kis Trading MCP/tools/base.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/tools/base.py) | `33d0774cd1bc1f115d4e9e745c1c8eeaf28f0084` | MCP default environment (L18, L33–37, L289–295, L544) |
| K6 | [`MCP/Kis Trading MCP/configs/domestic_stock.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/configs/domestic_stock.json) | `e82a0829ef519c64dfecb3e966ed217b4fcd3805` | 18 of 74 entries carry an `env_dv` parameter |
| K7 | [`MCP/MCP AI 도구 연결 방법.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/MCP%20AI%20%EB%8F%84%EA%B5%AC%20%EC%97%B0%EA%B2%B0%20%EB%B0%A9%EB%B2%95.md) | `22531bff1bc2979b9ea4406d65ec17bb653bffee` | Contradicting key comment (L276–277) |
| K8 | [`…/inquire_price/inquire_price.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_price/inquire_price.py) | `bb6ab22df57b1a5d14fab861f6c1d29272872a84` | Same TR for `real` and `demo` (L58–64). Same blob as the gates ledger. |
| K9 | [`…/inquire_time_dailychartprice/inquire_time_dailychartprice.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_time_dailychartprice/inquire_time_dailychartprice.py) | `aafa68e6f9cb8b06453f98ad63f954b096e3d7bb` | No `env_dv`; "실전계좌의 경우" only (L36, L71) |
| K10 | [`legacy/postman/모의계좌_POSTMAN_샘플코드_v1.6.json`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/legacy/postman/%EB%AA%A8%EC%9D%98%EA%B3%84%EC%A2%8C_POSTMAN_%EC%83%98%ED%94%8C%EC%BD%94%EB%93%9C_v1.6.json) and `…_환경변수.json` | `03833e4af7258d1d85b76f298af3928be2748ea0`; `48f6793ff5fe0e84415563d85363ad6561ddd2f1` | **Legacy** paper collection "모의투자(모의Env)": `{{VTS}}` items (L64, L404, L646, L946, L1372); variable `VTS` = the paper origin |

KIS developer portal (`https://apiportal.koreainvestment.com`), public JSON
endpoints used by the portal pages. List URLs are
`/api/apis/public/api-list/<collection id>`; forum posts are
`/api/forums/<forum id>/posts/<post id>` with forum
`10000000-0000-0011-0000-000000000002` (자주 묻는 질문) or
`…-000000000001` (공지사항). API list records carry per-API fields
`realDomain`, `virtualDomain`, `realTrId`, `virtualTrId` and a
`lastModifiedDate`; the portal page labels them "실전 Domain", "모의
Domain", "실전 TR ID", "모의 TR ID".

| # | Source | Pin (sha256 prefix, bytes, UTC) | Used for |
| --- | --- | --- | --- |
| K11 | API list "OAuth인증" (`21ee37e4-dec1-4738-91ce-04f693a7ed29`) | `1294f82e6bf61088`, 40,855, 07:59:25 | token, revoke, WS approval-key domains; token description |
| K12 | API list "[국내주식] 기본시세" (`1031d032-6747-414b-bdf2-fd419c0c98ce`) | `4a05fabc060b88bb`, 939,107, 07:59:33 | 22 quote APIs: 11 with a paper domain, 11 "모의투자 미지원" |
| K13 | API list "[국내주식] 종목정보" (`996ddbef-140c-46da-9bfb-b1cdc1d9b81b`) | `bbb109e09e18ef1e`, 870,499, 07:59:37 | 19 APIs, none offered in paper |
| K14 | API list "[국내주식] 업종/기타" (`409bcd22-e5f5-40df-a839-372691060ce5`) | `6daf58ff04a816b1`, 669,119, 07:59:42 | 14 APIs, 1 offered in paper; includes 국내휴장일조회 |
| K15 | API list "[국내주식] 실시간시세" (`ba2a8f9b-b62e-4ffe-bbc9-d1d31552d0db`) | `969a738af0500082`, 885,868, 07:59:49 | 32 WS feeds, 3 offered in paper |
| K16 | API list "[국내주식] 주문/계좌" (`b0a44bfd-dfd5-47f1-9b06-758383e595db`) | `c7d297e9c4dc5812`, 873,689, 07:59:27 | Order/account TR-id pairs, **named only** |
| K17 | `/api/apis/public/detail?accessUrl=/uapi/domestic-stock/v1/quotations/inquire-price` | `ee385b7f24b532f0`, 53,179, 07:58:57 | Detail record for 주식현재가 시세; `lastModifiedDate` 2026-10-30T11:47:10+09:00 |
| K18 | FAQ list (forum `…0002`, `size=200`) | `95a1116ab155a274`, 174,520, 08:01:08 | 173 posts; titles and previews only |
| K19 | FAQ "실전계좌 / 모의계좌 간 호출 구분은 어떻게 되나요?" (`5c706351-631c-4276-b190-f2b52830a296`, created 2023-05-10 KST) | `23dbdffafd771b73`, 08:01:33 | Origin, TR-id prefix and key split |
| K20 | FAQ "모의투자 \"MCA00124 해당 서비스를 찾을 수 없습니다\" 오류 문의" (`7579a5e3-f157-4437-88e1-6f6a067eb6e2`, 2025-08-11) | `6911dcec7df7baec`, 08:01:32 | Error on the wrong origin |
| K21 | FAQ "모의투자 환경 403 인증 실패 또는 host name을 찾을 수 없음" (`695cfecd-4379-4ea3-bd24-d23f9400985a`, 2025-08-19) | `308f22d1834bc31f`, 08:01:31 | Paper host; method rule |
| K22 | FAQ "다계좌 이용 시 API 호출 최대 유량은 어떻게 측정되나요?" (`bcfb94ee-5aa3-4915-bca6-d63378c620c2`, 2022-11-14) | `a2cd223864eb13b3`, 08:01:35 | Older rate numbers |
| K23 | FAQ "EGW00201 에러가 뭔가요" (`8548106c-c7a8-4126-abb7-b8ec46a8cb5c`, 2022-08-10) | `02ed1c17a94ab24c`, 08:01:36 | Older rate numbers |
| K24 | FAQ "모의투자는 실전투자와 환경이 다른가요?" (`ca2cc700-5d48-4939-ae79-3043ccf9b6f6`, 2023-05-25) | `6b5e34eb285e9fb4`, 08:01:33 | Paper fill model (orders, context only) |
| K25 | FAQ "모의투자 주문 시에는 실전투자와 달리 부분체결될 수 있나요?" (`4bb7761e-e264-4f14-8c35-84f093e77728`, 2022-12-16) | `7c4819106b3f6ad1`, 08:01:34 | Paper fills follow real executions (context only) |
| K26 | Notice list (forum `…0001`, `size=300`) | `9fa0c04251c34a04`, 127,220, 08:01:58 | 121 notices; titles |
| K27 | Notice "API 호출 유량 안내 (REST, 웹소켓) (2026.04.20 기준)" (`d0d1a83f-6f8d-4437-9700-6d26702fd989`, created 2023-01-11; title carries the 2026-04-20 basis, no modification date in the record) | `2a209e35ab8271c1`, 08:02:06 | Current REST/WS/token limits |
| K28 | Notice "[중요] 모의투자 API 사용 안내" (`747384fe-f047-495c-8548-769c8e6f4c15`, 2026-08-25) | `49c0d926595c0a4f`, 08:02:07 | Paper-account errors (named only) |
| K29 | Notice "모의투자 신규 TR 전환 계획 (넥스트레이드 미지원)" (`dd2e7e20-51e8-45fd-b65a-24a128f6af34`, 2025-02-25) | `80e3ddda54e931b2`, 08:02:08 | No NXT in paper; trading TR pairs |
| K30 | Notice "[모의투자 필독] 모의투자 유량 제한 변경 안내 (REST 1초당 2건)" (`9858397d-351b-4eda-b6b5-c5ccbcaa64ce`, 2024-03-27) | `b1fb26a7d3289a72`, 08:02:09 | Older paper limit; separate paper operator |
| K31 | Notice "[중요] 한국투자증권 Open API 신규 고객 초당 호출 제한 안내" (`c1113824-17c7-47a7-b7b8-8880506a847c`, 2026-03-20) | `9e042899294417d2`, 08:02:10 | New-customer throttle excludes paper |
| K32 | Notice "[모의투자 필독] 모의투자 규정사항(주문, 매매제한종목, 수수료 등)" (`a995fa1c-39a1-4c0a-a99e-838400c7a7a2`, 2023-02-20) | `d9a2d4f8eb25d86f`, 08:02:22 | Paper rules (orders, named only) |

**Missing evidence:**

- The full per-API detail record was fetched for one route only (K17).
  Every other market-data statement uses the list records (K11–K16),
  which carry the same domain/TR-id fields.
- No source says whether paper market data is real-time, delayed or
  produced by the separate paper operator (§2.5).
- No paper service-hours statement for market-data routes was found.
- The portal's linked paper-rules page on `securities.koreainvestment.com`
  (K24, K32) was **not** retrieved; it concerns orders.

### 2.2 Does a paper environment exist?

Yes. The publisher calls it "모의투자" (portal, README) and `vps` / `demo`
in client code.

- **Selection is three-fold** (K19, publisher guide):
  - "모의계좌 - 도메인 URL: https://openapivts.koreainvestment.com:29443";
  - "TR_ID: V로 시작, ex) VTTT1234U" (real: "T 혹은 J로 시작");
  - "앱정보: 모의계좌번호, 모의계좌의 appkey, appsecret".
- **Separate app keys:** README L222 "**모의투자** 및 **실전투자** 앱키
  각각 준비"; K1 L6–8 key names `paper_app` / `paper_sec` beside
  `my_app` / `my_sec`; K4 L68–69 `KIS_PAPER_APP_KEY` /
  `KIS_PAPER_APP_SECRET`. K7 L276–277 contradicts this (§2.6).
- **Key registration (process only):** the API service is applied for on
  the KIS website with a paper account; K28: "반드시 모의투자 계좌를
  확인하신 후 API 신청하시기 바랍니다." K1 L16–17 holds the paper account
  under separate key names (`my_paper_stock`, `my_paper_future`). K28 adds
  that paper stock accounts start with `5` and futures/options accounts
  with `6`, and that the paper account screen is separate from the API
  application screen.
- **The TR id, not the origin, selects the ledger** (K19, verbatim): "TR
  기준으로 원장에 호출을 하기 때문에 TR이 보다 정확한 구분값이기에 간혹
  도메인을 변경해서 사용하시면 TR 기준으로 API 호출되어서 거래가 되는
  경우가 있습니다만 그렇지 않은 경우도 있기 때문에 구분에 맞춰서
  호출해주시길 부탁드립니다." **Inference:** the origin alone is not a
  safe isolation boundary for trading TRs; see G-P6.
- **Operator:** "모의투자는 별도 운영사(연합인포맥스)에서 시스템을 관리 하고
  있습니다." (K30). The K18 previews of two FAQ posts say the same
  ("모의투자는 모의투자 운영업체가 별도로 운영하기때문에 …", post
  `306ea338-…`; "(연합인포맥스(주))", post `e5eed951-…`); those posts were
  not fetched in full.

### 2.3 Origins and identifiers

| Concern | Production | Paper | Evidence |
| --- | --- | --- | --- |
| REST origin | `https://openapi.koreainvestment.com:9443` | `https://openapivts.koreainvestment.com:29443` | field table: `realDomain` / `virtualDomain` on every paper-offered API (K11–K16); publisher guide K19, K20, K21; publisher client code K1 L27, L29 (`prod`, `vps`), K2 L201 |
| WebSocket origin | `ws://ops.koreainvestment.com:21000` | `ws://ops.koreainvestment.com:31000` | field table K15 (values carry a leading space in some records); K1 L28, L30 (`ops`, `vops`); K2 L208. Plain `ws://` in **both** environments. |
| Token route | `POST /oauth2/tokenP` on the production origin | same path on the paper origin | field table K11 (`virtualDomain` set for 접근토큰발급(P), 접근토큰폐기(P) and 실시간 접속키 발급); K2 L246 `f"{_cfg[svr]}/oauth2/tokenP"`; legacy K10 L64 "V_토큰발급". The token description (K11) states no paper-specific lifetime or re-issue rule. |
| WS approval key | `POST /oauth2/Approval` on the production origin | same path on the paper origin | K11; K2 L506–518 |
| TR-id differences | market data: `F…` ids | market data: **identical** ids | field table K12: e.g. `realTrId` and `virtualTrId` both `FHKST01010100` (주식현재가 시세), both `FHKST01010200` (호가/예상체결). K8 L58–64 assigns the same id for `real` and `demo`. |
| TR-id differences (trading, named only) | `TTTC0011U` / `TTTC0012U`, `TTTC0013U`, `TTTC8434R` … | `VTTC0011U` / `VTTC0012U`, `VTTC0013U`, `VTTC8434R` … | field table K16; K29. 18 of 23 order/account APIs are "모의투자 미지원" (K16). |
| TR-id differences (WebSocket) | `H0STCNT0`, `H0STASP0`, `H0STCNI0` | `H0STCNT0`, `H0STASP0`, **`H0STCNI9`** | field table K15: "※ 모의투자는 H0STCNI9 로 변경하여 사용합니다" (체결통보, account-scoped, named only) |
| Client TR rewrite | — | leading `T`, `J` or `C` replaced by `V` | publisher client code K2 L453–455: `if ptr_id[0] in ("T", "J", "C"):` … `tr_id = "V" + ptr_id[1:]`. Market-data ids start with `F`, so they pass unchanged. |
| Required header differences | none found | none found | K2 L457–459 sends the same `tr_id`, `custtype`, `tr_cont` headers in both; only the values of `appkey`, `appsecret`, `authorization` and `tr_id` differ. |

### 2.4 Market-data route availability in paper

Verbatim "모의 Domain" / "모의 TR ID" values from the portal list records.
"VTS" abbreviates `https://openapivts.koreainvestment.com:29443`. The
`lastModifiedDate` is the record's publisher timestamp.

| Capability | Route (TR, portal name) | Paper supported? (verbatim) | Evidence |
| --- | --- | --- | --- |
| Ticker | `FHKST01010100` 주식현재가 시세[v1_국내주식-008], `GET …/quotations/inquire-price` | VTS / `FHKST01010100` | F: K12, K17 (2026-10-30T11:47:10+09:00); E: K8 L58–64; L: K10 L404 |
| Ticker (alternate) | `FHPST01010000` 주식현재가 시세2[v1_국내주식-054] | "모의투자 미지원" / "모의투자 미지원" | F: K12 (2026-10-30T11:46:39+09:00) |
| Order book | `FHKST01010200` 주식현재가 호가/예상체결[v1_국내주식-011] | VTS / `FHKST01010200` | F: K12 (2026-08-12T16:13:53+09:00); L: K10 L646 |
| Candles, day/week/month/year | `FHKST03010100` 국내주식기간별시세(일/주/월/년)[v1_국내주식-016] | VTS / `FHKST03010100`; summary "실전계좌/모의계좌의 경우, 한 번의 호출에 최대 100건까지 확인 가능합니다." | F: K12 (2026-03-27T13:01:20+09:00); L: K10 L946 |
| Candles, daily (recent) | `FHKST01010400` 주식현재가 일자별[v1_국내주식-010] | VTS / `FHKST01010400` | F: K12 |
| Candles, today's minutes | `FHKST03010200` 주식당일분봉조회[v1_국내주식-022] | VTS / `FHKST03010200`; "실전계좌/모의계좌의 경우, 한 번의 호출에 최대 30건까지 확인 가능합니다." | F: K12 (2026-03-27T12:59:31+09:00); L: K10 L1372 |
| Candles, minutes by date | `FHKST03010230` 주식일별분봉조회 [국내주식-213] | "모의투자 미지원" / "모의투자 미지원" | F: K12 (2026-08-12T15:53:16+09:00); E: K9 has no `env_dv` and says "실전계좌의 경우" (L36) |
| Trades | `FHKST01010300` 주식현재가 체결[v1_국내주식-009]; `FHPST01060000` 당일시간대별체결[v1_국내주식-023]; after-hours `FHPST02310000` [v1_국내주식-025] | VTS with the same TR id on all three | F: K12 |
| Symbol info | `CTPF1002R` 주식기본조회[v1_국내주식-067]; `CTPF1604R` 상품기본조회[v1_국내주식-029] | "모의투자 미지원" / "모의투자 미지원" (both) | F: K13 (2025-05-14) |
| Symbol master | master files (`stocks_info/`, download host) | not an API; no environment concept documented | see the symbol-master audit on its branch |
| Holidays | `CTCA0903R` 국내휴장일조회[국내주식-040] | "모의투자 미지원" / "모의투자 미지원" | F: K14 (2026-06-04T13:07:11+09:00) |
| VI status | `FHPST01390000` 변동성완화장치(VI) 현황 | "모의투자 미지원" / "모의투자 미지원" | F: K14 |
| WS trades / book (KRX) | `H0STCNT0` 실시간체결가 (KRX); `H0STASP0` 실시간호가 (KRX) | `ws://ops.koreainvestment.com:31000` / same TR | F: K15 |
| WS (NXT, 통합), market status, expected trades | `H0NX…`, `H0UN…`, `H0STMKO0`, `H0STANC0`, VI feeds | "모의투자 미지원" (all 26 + 3 records) | F: K15 |

Counts per list (K11–K16): OAuth 3 of 3 offered in paper; 기본시세 11 of
22; 종목정보 0 of 19; 업종/기타 1 of 14; 실시간시세 3 of 32; 주문/계좌 5
of 23. Non-offered records use one of four verbatim forms: "모의투자
미지원" in both fields, "미지원" + "모의투자 미지원", or "모의투자 미지원"
in one field with the other empty.

### 2.5 Limits and data quality in paper

- **Current rate limits** (K27, publisher guide, verbatim):
  "(실전투자) 1초당 18건 (기존 20건)", "(모의투자) 1초당 1건 (기존 2건)",
  "※ 계좌 단위로 유량 제한(실전투자의 경우, 1계좌당 1초당 18건)",
  "※ 접근토큰발급( /oauth2/tokenP)의 경우 1초당 1건(23.10.27 시행)".
  WebSocket: "1세션", "실시간 데이터 합산 41건까지 등록 가능", "※ 접속키
  발급의 경우, 초당 1건으로 발급 제한". The notice does not split the WS
  limits by environment.
- **History** (publisher guide): K30 lowered paper REST from "1초당 5건" to
  "1초당 2건" from "2024.03.29(금)", "(실전투자는 변동 없습니다)"; K22
  (2022) "실전투자 1초당 20건, 모의투자 1초당 2건"; K23 (2022) "1초당
  10건" without an environment split. K31: the 2026 three-day new-customer
  throttle "※ 모의투자 계좌는 해당되지 않습니다. (모의투자 기본 유량정책
  유지)". K3 L416: "모의투자 계좌는 REST API 호출 제한이 낮습니다."
- **Error code:** `EGW00201` = "초당 거래건수를 초과하였을 때 표시되는 오류
  코드" (K23). Not stated to differ by environment.
- **Retry advice not adopted:** K27 says "서버 내 분산 정책에 따라 일부
  유량이 통과되지 않는 경우, 즉시 재호출 수행 부탁드립니다." This
  conflicts with the repository's no-automatic-retry rule (G-P5).
- **Paper-only errors** (publisher guide):
  - `MCA00124` "해당 서비스를 찾을 수 없습니다" when paper credentials are
    sent to the production origin: "실전 도메인으로 호출할 경우 MCA00124
    오류가 발생합니다." (K20)
  - HTTP 403 or "host name을 찾을 수 없음" on a mistyped paper host or a
    wrong method: "접근토큰발급과 주문은 POST 방식, 그 외 조회는 GET
    방식으로 호출해야 정상 처리됩니다." (K21)
  - Account-related, **named only:** `90070000` (K28), `40910000` (K28).
- **Venue:** "모의투자는 대체거래소(넥스트레이드) 거래를 지원하지 않으며,
  실전투자에서만 대체거래소 거래가 가능합니다." and "※ 모의투자는 거래소
  지정 불가, KRX(한국거래소) 주문만 가능" (K29, about trading). Whether
  quote routes accept `NX` / `UN` in paper is **not documented**; the NXT
  and 통합 WebSocket feeds are "모의투자 미지원" (K15).
- **Data quality:** **not documented.** K24/K25/K32 say only that paper
  *fills* follow real exchange executions ("모의투자시스템의 가상체결은
  실제 거래소 체결 기준으로 처리됩니다.", K25). Whether paper quotes are
  real-time, delayed, or produced by the separate operator (K30) is not
  stated.
- **Service hours of paper market data:** not found.
- **Client pacing (publisher client code, not a quota):** K2 L57 sets a
  module default `_smartSleep = 0.1`; `changeTREnv` assigns `0.05`
  (`prod`) and `0.5` (`vps`) at L174/L179, but declares only
  `global _isPaper` (L169). **Inference** (Python scoping): those two
  assignments are local, so `smart_sleep()` (L288–293) keeps sleeping
  0.1 s in both environments.

### 2.6 Contradictions and gaps

1. **Rate numbers.** K27 (paper 1/s, real 18/s, "2026.04.20 기준") is the
   newest-dated statement. K30 (2/s), K22 (20/2) and K23 (10/s) are older
   and conflict with it. The K27 record has no modification timestamp, so
   its "기준" date comes from the title only.
2. **TR-id prefix.** K19 says paper TR ids start with `V` and real ones
   with "T 혹은 J". The client rewrites `T`, `J` **and** `C` (K2
   L453–455). The portal records show that market-data `F…` ids are
   identical in both (K12), and that many `C…` ids are "모의투자 미지원"
   (K13, K16). **Inference:** the `V` rule applies to the trading TRs
   offered in paper, not to market data.
3. **Paper keys.** K7 L276–277 annotates `paper_app` / `paper_sec` with
   "모의투자용 APP KEY (실전과 동일)" / "(실전과 동일)". K3 L222, K4
   L68–69, K19 and K28 all describe separate paper keys. K7 is the outlier.
4. **Cross-environment token reuse in the sample client.** K2 L88–104:
   when no server is given and `auth()` has not run, `read_token()` tries
   "가장 최근 저장된 실전/모의 토큰 파일 → 기존 단일 토큰 파일 순으로".
   A token from the other environment can therefore be returned. Not a
   contract; not adopted (G-P1).
5. **Publisher MCP defaults to paper.** K5 L289 `pop("env_dv", "demo")`
   and L544 "기본값은 'demo'이므로 사용자가 투자환경을 명시하지 않으면
   모의투자로 실행". The runner then authenticates with `ka.auth("vps")`
   (L33–35) even for routes the portal marks "모의투자 미지원" (K6: 56 of
   74 entries have no `env_dv`, e.g. `inquire_time_dailychartprice`).
   KTradeLink has no default environment (§9).
6. **Pacing.** See §2.5 (scoping inference).

### 2.7 Implications for a first authorized smoke test (Inference only)

- **Could be checked in paper first** (after separate authorization): the
  token route on the paper origin (`/oauth2/tokenP`, at most one request);
  one `FHKST01010100` quote with `FID_COND_MRKT_DIV_CODE=J`; optionally
  `FHKST01010200`, `FHKST03010100`, `FHKST03010200` and `FHKST01010300`.
  This would exercise TLS to the paper host, JSON token request shape,
  header names, the `rt_cd` envelope and decoder field names.
- **Must stay at ≤ 1 REST request per second** (K27), with the token
  request counted separately at 1/s. A single `fetch_ticker` sends a token
  request and a quote request back to back; pacing between them is not
  documented.
- **Cannot be checked in paper at all:** by-date minute candles
  (`FHKST03010230`), symbol info (`CTPF1002R`, `CTPF1604R`), holidays
  (`CTCA0903R`), VI status, NXT / 통합 venues, NXT and 통합 WebSocket
  feeds. Each needs a separately authorized production check, or must
  stay unsupported.
- **What paper cannot prove:** production TLS/host behaviour, production
  rate limits (18/s vs 1/s), production entitlements, whether paper
  quotes equal production quotes, production error universes, or anything
  about `NX` / `UN` quotes.

### 2.8 Gates and not-verified items

- Paper keys are separate; a paper credential sent to the production
  origin yields `MCA00124` (K20). The library must never re-send the
  request to the other origin on that error (G-P1, G-P3).
- The TR id, not only the origin, can select the ledger (K19). Trading
  TRs are out of scope and need separate order authorization (G-P6).
- Not verified: any paper response; paper quote data quality and hours;
  whether `NX` / `UN` are rejected on paper quote routes; whether a paper
  token is rejected by the production origin (only the reverse case is
  documented, K20); the 6-hour same-token rule (K11) in paper.

## 3. Kiwoom REST

### 3.1 Pinned sources

Git sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@c7a3d254`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/c7a3d25449ed4b4238bef378780c41103c67b9e9).
The full SHA is `c7a3d25449ed4b4238bef378780c41103c67b9e9`; it was the only
branch head (`refs/heads/main`, also `HEAD`) in `git ls-remote` at
retrieval. Earlier audits pinned `953e5dbf…`; both commits name the same
tree (see [trade evidence](trade-evidence-2026-11-05.md) §3.1), and the blob SHAs below match
the earlier pins where they overlap.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field tables**: per-API `meta` with "운영 도메인" and "모의투자 도메인" (e.g. au10001 L3–17, ka10001 L1259–1273, 0B L96908–96921); `ka01690` note (L972); `error_codes` (L107018; `8030` L107171, `8031` L107176, `8104` L107196; `1700`–`1702` L107076–107086) |
| W2 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | `PRD` folder (L8) and `MOCK(모의투자)` folder (L33545), 306 items each; variables `PRD`, `MOCK`, `APP_KEY`, `APP_SECRET`, `APP_KEY_MOCK`, `APP_SECRET_MOCK` (L67084–67091) |
| W3 | [`kiwoom/core/auth.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/auth.py) | `9026aae207b7e2963c40f06e5e9a2f287a589d28` | Default REST/WS origins per mode (L21–39); environment-variable override (L42–59). Same blob as the gates ledger. |
| W4 | [`kiwoom/core/errors.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/errors.py) | `dd7a8709bccd8a28601c49d26a298d3c92f34e5d` | `ModeMismatchError` (L148–152), `DemoUnsupportedError` (L162–166), code sets (L183, L187, L189) |
| W5 | [`kiwoom/core/types.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/types.py) | `5bb46c91eb53325152948891b775128fbebd6dd0` | `Mode = Literal["real", "demo"]`; unknown mode raises (L6–18) |
| W6 | [`kiwoom/core/secrets.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/secrets.py) | `002031b77823845b77bb46da579c4369c8a883df` | Credential variable names per mode (L241–246) |
| W7 | [`README.md`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/README.md) | `018e50aad8156d18f057135a91ce2a15d09ce2d2` | PRD/MOCK mirror (L15); separate keys (L92, L95–100, L107); setup default (L248); Postman (L349–350); `.env` (L378–380) |
| W8 | [`SETUP-MCP.md`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/SETUP-MCP.md) | `56d479cc628662304c0cd588254ecf3f1e7d8822` | MCP default mode (L52); key pairing (L546, L874) |
| W9 | [`mcp_exec/README.md`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/mcp_exec/README.md) | `a25c4c367fa8007521de6ee61549305f0e5fb766` | Known demo-mode refusals (L115) |
| W10 | Portal home https://openapi.kiwoom.com/main/home | sha256 `e7b00f82d5d65b72`, 51,849 bytes, 08:03 UTC | Menu item "모의투자 이용안내" (`data-mid="01030000"`) only |

**Missing evidence:**

- The portal's "모의투자 이용안내", "API 가이드" and notice pages were
  **not retrieved**: their routes are resolved by page script, and direct
  GETs of `/guide/apiguide` and `/board/notice` were reset by the server
  at 08:03 UTC (`/guide/faq` returned 404). No further attempt was made.
- Consequently no paper rate limit, paper service hours, paper data
  quality statement or paper venue restriction (for example a
  "KRX만 지원" statement) was found in the pinned sources.
- W1 carries no per-API paper-availability column.

### 3.2 Does a paper environment exist?

Yes: "모의투자 도메인" on every W1 entry, the `MOCK(모의투자)` Postman
folder (W2) and `demo` mode in the client (W5).

- **Selection:** a separate origin (§3.3) and a separate app key. W7 L92:
  "**운영(real)** 과 **모의투자(demo)** 는 키가 **서로 다릅니다.**"; W8
  L52 "두 모드는 **서로 다른 앱 키**를 씁니다."
- **Mismatch errors** (field table W1): `8030` "투자구분(실전/모의)이 달라서
  Appkey를 사용할수가 없습니다", `8031` "투자구분(실전/모의)이 달라서
  Token를 사용할수가 없습니다". The client maps both to
  `ModeMismatchError` (W4 L148–152, L187).
- **Key registration (process only):** W7 L95–100 — log into the Kiwoom
  OpenAPI portal, apply for OpenAPI use and register an app, read the App
  Key/Secret, and "운영과 모의투자를 모두 사용할 경우, 각 환경의 키를 따로
  발급받습니다."
- No header, api-id or body field selects the environment.

### 3.3 Origins and identifiers

| Concern | Production | Paper | Evidence |
| --- | --- | --- | --- |
| REST origin | `https://api.kiwoom.com` | `https://mockapi.kiwoom.com` | field table W1 meta on all 306 REST entries; W2 variables L67084–67091; client code W3 L32–35 |
| WebSocket origin | `wss://api.kiwoom.com:10000` | `wss://mockapi.kiwoom.com:10000` | field table W1 meta on all 31 WS entries (e.g. 0B L96918–96919); W3 L36–39 |
| Token route | `POST /oauth2/token` (au10001) | same path on the paper origin | field table W1 L3–17; W2 MOCK item L33554 |
| api-id differences | — | none: the MOCK items send the same `api-id` as PRD | W2 (e.g. ka10001 PRD L3505, MOCK L37042) |
| Required header differences | `api-id`, `authorization`, `cont-yn`, `next-key` | same | W1 ka10001 request header table |
| Origin override | — | the client reads `PRD`, `MOCK`, `W_PRD`, `W_MOCK` from the process environment and uses them instead of the defaults when set | publisher client code W3 L24–31, L42–59; W7 L380 |

### 3.4 Market-data route availability in paper

W1 has **no per-API availability column**. Every one of its 337 entries
lists a "모의투자 도메인", and W2 has a MOCK item for every one of its 306
REST requests, including the one API that W1 says is not offered in paper.
**Inference:** the presence of a mock domain or a MOCK Postman item is not
evidence that a route is served in paper.

| Capability | Route | Paper supported? (verbatim) | Evidence |
| --- | --- | --- | --- |
| Ticker | `ka10001` 주식기본정보요청, `POST /api/dostk/stkinfo` | not stated; mock domain listed | W1 L1259–1273; W2 MOCK L37042 |
| Order book | `ka10004` 주식호가요청, `POST /api/dostk/mrkcond` | not stated; mock domain listed | W1 L2548; W2 MOCK L40463 |
| Candles, minute | `ka10080` 주식분봉차트조회요청, `POST /api/dostk/chart` | not stated; mock domain listed | W1 L23478; W2 MOCK L48120 |
| Candles, day | `ka10081` 주식일봉차트조회요청, `POST /api/dostk/chart` | not stated; mock domain listed | W1 L23721; W2 MOCK L48229 |
| Trades | `ka10003` 체결정보요청, `POST /api/dostk/stkinfo` | not stated; mock domain listed | W1 (trade audit W1 L2305–2546); W2 MOCK item (trade audit L37228) |
| Symbol master | `ka10099` 종목정보 리스트, `POST /api/dostk/stkinfo` | not stated; mock domain listed | W1 L27524; W2 MOCK L39556 |
| WS trades | `0B` 주식체결 | not stated; mock WS domain listed | W1 L96908–96921 |
| (account, named only) | `ka01690` 일별잔고수익률 | "해당 API는 모의투자를 지원하지 않습니다" | W1 L972; yet W2 MOCK L33731 exists |
| Any route | — | error `8104` "모의투자에서 지원하지 않는 API 입니다." | field table W1 L107196; client `DemoUnsupportedError` W4 L162–166 |

Repo note W9 L115: "모의투자(demo) 모드에서는 환율 조회, 주문가능금액 조회가
거절됩니다." (non-market-data, named only).

### 3.5 Limits and data quality in paper

- Rate-limit codes `1700` "허용된 API 요청 개수를 초과하였습니다. 유량={?},
  API ID={?}", `1701` (전체) and `1702` (그룹) carry no numbers and no
  environment split (W1 L107076–107086).
- No paper-specific number, service hours, data-quality (real-time vs
  delayed) or venue statement was found (see Missing evidence).
- `kiwoom-market-data.md` cites the portal for "paper accounts have
  additional per-TR restrictions"; that page is not in this pin set
  (§9).

### 3.6 Contradictions and gaps

1. W7 L15 "HTTP API 306개를 PRD/MOCK 환경별로 제공" vs W1 L972 (ka01690
   not offered in paper) and W9 L115 (two refused routes): the MOCK
   collection mirrors PRD and does not express availability.
2. **Defaults to paper in publisher tools:** W7 L248 "Enter는 안전을 위해
   demo가 기본입니다" (CLI setup); W8 L52 "기본값은 `demo`로 설치합니다"
   (MCP). KTradeLink has no default (§9).
3. **Origin override from the process environment** (W3 L42–59) lets any
   `MOCK` value replace the paper origin. Not a contract; not adopted.
4. W9 L87: the exec MCP server takes `APP_KEY` / `APP_SECRET` in both
   modes and maps them to the `_MOCK` names for `demo`; the library
   itself uses `APP_KEY_MOCK` / `APP_SECRET_MOCK` (W6 L244–245).

### 3.7 Implications for a first authorized smoke test (Inference only)

- **Could be checked in paper first:** one token request to
  `https://mockapi.kiwoom.com/oauth2/token` and one `ka10001` request.
  This would show whether the route is served in paper at all (success vs
  `8104`), the `return_code` envelope, the token's `expires_dt` and the
  decoder field names.
- A paper key sent to production (or the reverse) should produce `8030`
  or `8031`; observing that is optional and needs its own authorization.
- **Cannot be planned without first observing paper:** whether `ka10004`,
  `ka10080`, `ka10081`, `ka10003` and `ka10099` are served in paper, and
  whether `_NX` / `_AL` symbols work there.
- **What paper cannot prove:** production rate limits, production
  entitlements and data quality, NXT/SOR behaviour, and whether paper and
  production return the same fields and signs.

### 3.8 Gates and not-verified items

- `8104` must surface as an unsupported capability, never as a retry
  against production (G-P4). `8030`/`8031` must surface as a
  configuration error, never as a switch of environment (G-P3).
- Not verified: which routes are served in paper; paper rate limits,
  hours and data quality; paper venue coverage; the portal's paper guide.

## 4. LS Securities

### 4.1 Pinned sources

All LS sources are public web resources on `https://openapi.ls-sec.co.kr`
without an immutable revision; only L1 carries a publisher version marker.
Each sha256 prefix identifies only the copy retrieved at the stated UTC
time on 2026-11-05. Detail endpoints are
`/guide/api/<data-tr id>?type=<rest|websocket>&api=<data-api id>` with ids
read from L2.

| # | Path / URL | Pin (sha256 prefix, UTC, revision) | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json?download=true | `9aaca437f1925115`, 2,792,313 bytes, 08:05:40; publisher `"version" : "20261026021444748"` (byte-identical to the copies pinned by the capability inventory and trade audits) | `servers` (L7–16): REST `url` only; WEBSOCKET `url` and `simulationUrl` (L14); t1852 `sservergb` (L41543–41547); order `shcode` text (L42294, L42595, L42864) |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `9f6acf250acdb42a`, 08:07:00 (page varies per request) | `data-api` / `data-tr` ids |
| L3 | `…/guide/api/07112bqm-8133-8wf2-ckd2-o8o7210v5m6o?type=rest&api=33bd887a-6652-4209-88cd-5324bc7c5e36` (token) | `4acff92cdcdfd551`, 08:07:23 (same hash as the gates ledger copy) | single `domain` `https://openapi.ls-sec.co.kr:8080` |
| L4 | `…/guide/api/wqs8bq62-huk0-wb6z-7x83-nt78d4ax2yb6?type=rest&api=54a99b02-dbba-4057-8756-9ac759c9a2ed` (t1102) | `42712ce969a8a480`, 08:07:25 (same hash as the gates ledger copy) | single `domain` `:8080`; `transactionPerSec` `10` |
| L5 | `…/guide/api/1v82075e-xo68-55y8-0if3-h7053s85441q?type=websocket&api=9a2800c3-9bf2-4d67-8d83-905074f06646` (S3_ KOSPI체결) | `feefc8800c4cfcda`, 08:07:26 | single `domain` `wss://openapi.ls-sec.co.kr:9443` |
| L6 | https://openapi.ls-sec.co.kr/about-openapi | `157e6d68134ff5e1`, 08:06:10 (differs from the capability inventory copy `0faac4ed…`) | Paper application and separate keys |
| L7 | https://openapi.ls-sec.co.kr/howto-use | `236e735fef842744`, 08:06:12 | Onboarding paper order example (non-authoritative) |
| L8 | https://openapi.ls-sec.co.kr/community-faq (→ `/community/10000000-0000-0011-0000-000000000002`) | `b3f0b6aeda5eca6a`, 08:06:24 | FAQ entry on paper fills (`data-id` `7841c58a-93f5-4601-b466-46b5effabcb8`) |

**Missing evidence:**

- No publisher Git repository or SDK for LS REST.
- No per-TR paper flag, no paper REST origin and no paper rate limit in
  L1, L3–L5.
- The public forum JSON endpoints used by the KIS portal pattern
  (`/api/forums/<forum>/posts`) answered HTTP 302 at 08:06:14–15 UTC and
  were not followed; LS notices were therefore not searched.

### 4.2 Does a paper environment exist?

Yes, as a separately requested service with its own keys (L6, publisher
guide): "API 신청은 실전투자와 모의투자 2가지로 구분되며 처음 시작하는
경우 모의투자로 먼저 테스트하는 것을 권장해요."; step 06 "모의투자 OPEN
API 신청 (선택)" — "실제 거래 전 테스트하려면 모의투자 OPEN API(①)도
별도로 신청해야해요. ※ 모의투자는 App Key·Secret Key가 실계좌와 다르게
발급돼요." Registration happens on the LS website after certificate
login (process only).

How a REST call is routed to paper is **not documented in the guide**:

- L1 `servers` gives REST only `"url" : "https://openapi.ls-sec.co.kr:8080"`;
  only the WEBSOCKET server has `"simulationUrl" :
  "wss://openapi.ls-sec.co.kr:29443"` (L1 L14).
- Every detail record has a single `domain` (L3, L4, L5); there is no
  simulated-domain field.
- Onboarding (L7, publisher guide, non-authoritative): "실제 자금이
  사용되므로 처음에는 반드시 모의투자 토큰으로 테스트하세요. tr_id 값이
  실전/모의를 구분해요." with "CSPAT00101 (모의) / CSPAT00601 (실전)", and
  the paper order is posted to `https://openapi.ls-sec.co.kr:8080/stock/order`.
  `CSPAT00101` is absent from the L1 catalog (as the capability inventory
  noted), and the same page's market-data example uses the non-catalog
  `STKCURR` route that ADR 0010 already rejected. **Inference:** paper REST
  may share the production origin and be selected by the paper app key's
  token, but no authoritative source says so.

### 4.3 Origins and identifiers

| Concern | Production | Paper | Evidence |
| --- | --- | --- | --- |
| REST origin | `https://openapi.ls-sec.co.kr:8080` | **not documented** (onboarding uses `:8080`) | field table L1 L7–10, L3, L4; publisher guide L7 |
| WebSocket origin | `wss://openapi.ls-sec.co.kr:9443` | `wss://openapi.ls-sec.co.kr:29443` (`simulationUrl`) | field table L1 L11–15; L5 shows only `:9443` |
| Token route | `POST /oauth2/token`, form body | not documented; onboarding implies the same route with paper keys | L3; L7 |
| TR-id differences | — | not documented in the guide; onboarding claims a different order TR (named only) | L1; L7 |
| Field-level markers | — | t1852 (파일저장종목 실시간검색, not market data) `sservergb` "서버구분" = "I : 운영\nS : 모의투자"; order `shcode` "(모의투자는 A+종목코드)" (orders, named only) | field table L1 L41543–41547, L42294 |
| Required header differences | — | none documented | L3, L4 |

### 4.4 Market-data route availability in paper

**Not found.** L1 has 42 API groups and no per-TR paper flag; the detail
records (L3–L5) carry one `domain` and `transactionPerSec` only. No
statement says whether `t1102` (ticker), `t1101` (order book),
`t8410`/`t8412` (candles), `t1301`/`t8454` (trades) or `t8436` (symbol
master) are served in paper.

| Capability | Route | Paper supported? (verbatim) | Evidence |
| --- | --- | --- | --- |
| All market-data TRs | `POST /stock/market-data`, `/stock/chart`, `/stock/etc` | not found | L1, L3, L4 |
| WebSocket feeds | `/websocket`, `/websocket/stock` | only a server-level `simulationUrl` | L1 L14; L5 |

### 4.5 Limits and data quality in paper

- Rate limits: per-TR `transactionPerSec` (e.g. `t1102` `10`, L4); no
  environment split and no paper number found.
- Paper fills (FAQ, publisher guide, about orders): Q "\"모의투자 주문처리가
  안되었습니다. 재시도 바랍니다.\" 메시지가 나옵니다. 왜 그런가요?" A
  "모의투자 서버는 정규장 시간(09:00~15:30)에만 주문이 체결되며, 장 시작
  전·점심 정산 시간·서버 점검 중에는 해당 메시지가 발생할 수 있습니다.
  또한 모의투자는 실거래 대비 체결 처리에 지연이 있을 수 있으니, 응답
  코드를 확인한 뒤 일정 간격을 두고 재시도하도록 구현하세요." (L8). The
  retry advice concerns orders and is not adopted (G-P5).
- Paper market-data hours and data quality: not found.

### 4.6 Contradictions and gaps

1. Onboarding (L7) vs guide (L1): a paper order TR `CSPAT00101` that the
   catalog does not list, and a claim that `tr_id` separates paper from
   production, while the guide documents no TR-id difference.
2. Paper WebSocket has an origin (L1 L14) but paper REST does not.
3. L6 hash changed since the capability inventory retrieval; the paper
   statements quoted here are consistent with that audit's summary
   ("API keys are issued for 실전 or 모의").

### 4.7 Implications for a first authorized smoke test (Inference only)

- **No paper REST smoke test can be planned for LS** from public
  evidence: sending a paper key to `:8080` would rely on an undocumented
  routing rule. KTradeLink correctly refuses LS paper (§9).
- If the maintainer wants LS paper evidence, the first step is a
  publisher-documentation request (or a portal page, once retrievable)
  that names the paper REST origin, not a network probe.
- Any LS smoke test would therefore have to be a separately authorized
  **production** read (as ADR 0012 already frames it).

### 4.8 Gates and not-verified items

- LS paper stays refused until a paper REST origin is documented (G-P1).
- Not verified: paper REST routing; which market-data TRs exist in paper;
  paper limits, hours and data quality; whether paper tokens are rejected
  by production routes.

## 5. DB Securities

### 5.1 Pinned sources

GitHub sources are at
[`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb)
(`564b5100b80a3a785468b77ee8c0557f6edcfdeb`, committer date
2026-08-20T10:06:26+09:00), the commit already pinned by the trade, candle
and capability ledgers; fetched 07:54:53Z. Blob SHAs are from
`git rev-parse <commit>:<path>`. Portal JSON on `https://openapi.dbsec.co.kr`
was retrieved 07:55:50–07:58:11Z; the portal has no document version, so
each API's `lastModifiedDate` is given where it matters. The three group
lists DP2–DP4 and DP5 have the **same sha256** as the copies pinned in the
trade/candle/capability ledgers (06:47–07:14Z), so they did not change.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| D1 | [`config.yaml.example`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/config.yaml.example#L4-L26) | blob `f6204f1399f2f080c11f28364444b40b7868ef96`; L4–26 | `prd_*`/`vtl_*` key pairs; "REST API URL은 운영/모의 동일 (앱 속성으로 내부 분기)"; WS ports; `mode` |
| D2 | [`README.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/README.md#L684-L741) | blob `377b5b9e0e3bcdfa54edad23507860798fa91143`; L104, L280, L286–314, L427–446, L684–705, L736–741 | Paper application process; "운영 vs 모의투자" table; paper-support rule |
| D3 | [`docs/api_support_matrix.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/api_support_matrix.md#L1-L59) | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c`; L3–6, L17, L31, L34, L53–59, L75–76, L153–157 | Per-API ⭕/❌ and TPS |
| D4 | [`docs/errors_and_rate_limits.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/docs/errors_and_rate_limits.md#L104-L222) | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L106–109, L161–173, L184–187, L197–222 | Paper messages; REST/WS limits (not split by environment) |
| D5 | [`dbsec_sdk/config.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/config.py#L24-L162) | blob `8fab32d061fa9b483247915b2a37159831a0eeee`; L24–35, L81–100, L112–130, L143–162 | SDK environment selection (publisher client code) |
| D6 | [`dbsec_sdk/auth.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/auth.py#L96-L150) | blob `b83addb2b8007ae12946eab1ae0395ceb3eca7de`; L96–106, L131, L150, L250–253 | Token cache tagged with `mode`; base headers identical in both modes |
| D7 | [`dbsec_sdk/websocket/stream.py`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/websocket/stream.py#L81) | blob `3e16937c651e67b03fbcaa000964119b0e8c196b`; L81 | SDK hint for WS `10005` |
| D8 | [`web_test/README.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/web_test/README.md#L24-L33) | blob `2aecf79c76d1874ef1db4a479682ffe1b5d8dd73`; L24–33 | "어느 토큰을 쓰는지가 환경을 결정" |
| D9 | [`HOWTOUSE.md`](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/HOWTOUSE.md#L33-L34) | blob `f9452d057fe3962610b17f168674cccbff7dd7b4`; L33–34, L82–86 | Separate real/paper app keys |
| DP1 | [apiservice](https://openapi.dbsec.co.kr/apiservice) (HTML) | sha256 `fc1105771d2c0de8`, 07:56:19Z | Row "모의투자 도메인" (`simulatedDomain`); shown only when `!!data.simulatedDomain` |
| DP2 | `/api/apis/public/api-list/80005fb0-6feb-4b8b-904a-605c59e29b4f` (국내주식시세, 15 APIs) | sha256 `f4f56996c26c33b3`, 07:55:50Z; `lastModifiedDate` PRICE 2024-06-05, HOGA/CONCLUSION/JCODES 2024-03-28 | `domain`, `simulatedDomain`, `description`, `extraParam` |
| DP3 | `…/api-list/0bc09824-e8c2-491a-8c9d-b99e64b4b907` (국내주식/선물차트, 5 APIs) | sha256 `f10207c4b22890cb`, 07:55:52Z; CHARTMIN/CHARTDAY 2025-08-27 | same |
| DP4 | `…/api-list/05ac28b8-624f-4115-8aed-cf55f24279dd` (국내주식주문, 17 APIs) | sha256 `4f2578523296c2ec`, 07:55:51Z; CSPAT00600 2026-06-15 | Paper phrase on order/account APIs (named only) |
| DP5 | `…/api-list/cc55b867-e049-421b-a798-be016370ff44` (OAuth 인증) | sha256 `eeb775c8ecd70a5f`, 07:56:44Z; token 2026-02-25 | Token description |
| DP6 | `…/api-list/94b5fddc-b819-451b-9619-13ee42468798` (국내주식시세(실시간), 9 APIs) | sha256 `f48090f104faa614`, 07:56:44Z | WS `domain` vs `simulatedDomain` |
| DP7 | `…/api-list/f1819725-95e6-4445-ad7f-aa1908b20b03` (해외선물옵션시세(실시간)) | sha256 `83e5833f4d7389d3`, 07:56:46Z | Control: `simulatedDomain` null |
| DP8 | `/api/apis/guide/tr/property/cd5b4c37-609c-4b8c-995f-f4f7a594a16c` (token field table) | sha256 `a7d184619b8d4e84`, 07:57:10Z | No environment field in the token request |
| DP9 | [howto-use](https://openapi.dbsec.co.kr/howto-use) | sha256 `391a634b1d63cf6d`, 07:57:25Z | "(모의투자 별도 발급)" |
| DP10 | Notice "[공지] 모의투자 관련 변경사항 (25.10.23)" — `/api/forums/10000000-0000-0011-0000-000000000001/posts/d65120c3-f972-4f4a-90e1-e2333a59c80c` | sha256 `109edd7955121c02`, 07:58:05Z; `createdDate` 2025-10-23T08:59+09:00 | Paper app may call quote APIs from 2025-10-23 08:00 |
| DP11 | Notice "[공지] 모의투자 시스템 정상화 공지" — same forum, post `10a58364-97b6-4a41-a4d9-9bb0fe517693` | sha256 `1dd7263396b45fed`, 07:58:06Z; `createdDate` 2025-10-23T10:43+09:00 | Paper quotes are routed to the production quote system; paper-only outage |
| DP12 | FAQ "OpenAPI 모의투자 앱 신청방법" — `/api/forums/10000000-0000-0011-0000-000000000002/posts/09835da7-309c-4327-8127-c63d53b9bb2e` | sha256 `8fac2a3530432343`, 07:58:07Z; `createdDate` 2026-08-05 | Registration process; product scope |
| DP13 | FAQ "Open API 호출 유량 안내 (Rest API, Websocket) - 2026.9.14 기준" — same forum, post `8a596b8d-07e6-4a61-ae24-bcd04ac671e6` | sha256 `d7b08453a0435039`, 07:58:08Z; `createdDate` 2024-08-08 (title says "2026.9.14 기준") | Per-port WS session count incl. 모의투자 |

Evidence levels: DP2–DP8 `field table`; DP9–DP13 `publisher guide`; D2–D4,
D8–D9 `publisher repo note`; D1, D5–D7 `publisher client code` (D1 is a
sample config read by that code).

**Missing evidence:**

- No paper service-hours statement, no paper-specific rate limit, and no
  statement on whether paper **WebSocket** market data comes from the
  production feed.
- No public change log on whether the 2025-10-23 routing (DP10/DP11) covers
  the 국내주식/선물차트 group (DP10 names only the three "시세 API" groups).
- The DB homepage pages for 상시모의투자 (`www.dbsec.co.kr/custcenter/vts/…`,
  linked from D2 L104) were not retrieved; they are outside the Open API
  portal.

### 5.2 Does a paper environment exist?

**Yes** — "모의투자" (repo and portal); the SDK calls it `demo` and the key
prefix `vtl_` (D1 L8–10, D5 L81–100). Selection:

- **REST:** same origin; the server decides by the app key. D1 L13 "REST
  API URL은 운영/모의 동일 (앱 속성으로 내부 분기)"; D2 L693 "발급받은 앱
  키의 속성으로 서버가 분기합니다."; D8 L29 "REST 는 운영/모의 URL 이 동일해
  **어느 토큰을 쓰는지가 환경을 결정**합니다." Portal REST APIs have
  `simulatedDomain` null (DP2–DP5), so DP1 shows no "모의투자 도메인" row for
  them.
- **WebSocket:** separate port, "**WebSocket 포트만 다릅니다** (운영: 7070,
  모의: 17070)" (D2 L693); DP6 gives `simulatedDomain` for every domestic
  real-time API.
- **No TR-id prefix or header switch:** D3 lists one TR code per API for
  both environments (field table + repo note).
- **Separate app key:** DP9 "계좌별 개인 고유 토큰(APP_KEY, APP_SECRET)이
  발급됩니다.(모의투자 별도 발급)"; D9 L33 "**실전투자용**(`prd_*`) 과
  **모의투자용**(`vtl_*`) 앱키를 발급받습니다."
- **Registration (process only):** DP12 / D2 L290 "신청 순서: 상시모의투자
  참가신청(홈페이지/MTS) → 모의투자 계좌 발급 → OpenAPI 모의투자 서비스 신청";
  D2 L314 "상시모의투자 계좌가 없으면 OpenAPI 모의투자 서비스를 신청할 수
  없습니다." Scope: "국내주식, 해외주식, 국내선물옵션 (해외선물옵션의 경우
  모의투자 지원 X)" (DP12; D2 L292–296).

### 5.3 Origins and identifiers

| Concern | Production | Paper | Evidence |
| --- | --- | --- | --- |
| REST origin | `https://openapi.dbsec.co.kr:8443` | **same** origin; environment chosen by the app key | D1 L13–14; D2 L688; DP2–DP5 `domain`, `simulatedDomain` null (field table) |
| WebSocket origin | `wss://openapi.dbsec.co.kr:7070/websocket` (해외선물옵션: `:7071`) | `wss://openapi.dbsec.co.kr:17070/websocket`; none for 해외선물옵션 | D1 L17–21; D2 L689–690; DP6 `domain` `…:7070`, `simulatedDomain` `…:17070`; DP7 `simulatedDomain` null |
| Token route / behaviour | `POST /oauth2/token` (form; `appkey`, `appsecretkey`, `grant_type`, `scope` "oob") | same route and fields with the 모의투자 app key; no environment field | DP5, DP8 (field table); D5 L81–100 (client code). DP5: "API호출 유량은 1분에 1건", 24 h validity, "유효기간 만료 전 토큰을 발급을 하는경우, 동일한 토큰이 발급됩니다. (만료기간도 동일)" — **not stated per environment** |
| TR-id / api-id differences | e.g. `PRICE`, `HOGA`, `CONCLUSION`, `CHARTMIN`, `JCODES`, `S00` | **identical** TR codes | D3 (single TR column) |
| Required header differences | `content-type`, `authorization` (SDK) | **none documented**; SDK sends the same two headers in both modes | D6 L250–253 (client code); DP2–DP8 have no environment header |

SDK-only guards (client code, not a contract): the token cache records the
`mode` and is discarded on mismatch (D6 L96–106, L131, L150); `mode` must be
exactly `"demo"` or `"production"`, defaulting to `"demo"` (D5 L122), and
D5 L119–120 explains why: "오타 시 REST 는 실전(prd) 앱키로, WebSocket 은
demo 로 엇갈려 폴백돼 '모의라고 믿고 실주문'이 나갈 수 있어 명시적으로
차단한다."

### 5.4 Market-data route availability in paper

D3 legend (L4): "⭕ — 모의투자(`mode: "demo"`) + 실전투자 모두 호출 가능";
D2 L740: "시세 · 실시간 · 차트 그룹은 전부 사용 가능". DP10: "모의투자 앱에
시세 API 사용가능하도록 시스템 개선 (아래 서비스그룹의 API 사용가능)" —
"국내주식 시세 API", "해외주식 시세 API", "국내선물옵션 시세 API";
"사용가능일시 : 25.10.23 (08:00)". None of the market-data descriptions in DP2/DP3/DP6
carries the phrase "※ 모의투자 계좌로 사용가능한 API입니다." (see §5.6 #1).

| Capability | Route | Paper supported? (verbatim) | Evidence |
| --- | --- | --- | --- |
| Current price (ticker) | `PRICE` `POST /api/v1/quote/kr-stock/inquiry/price`; `MULTIPRICE` `…/multiprice` | ⭕ (both) | D3 L55–56; DP10 group "국내주식 시세 API" |
| Order book | `HOGA` `POST /api/v1/quote/kr-stock/inquiry/orderbook` | ⭕ | D3 L57; DP10 |
| Candles — minute | `CHARTMIN` `POST /api/v1/quote/kr-chart/min` (tick `CHARTTICK`) | ⭕ | D3 L153–154 only; **not** named in DP10 (chart group) |
| Candles — day | `CHARTDAY` `POST /api/v1/quote/kr-chart/day` | ⭕ | D3 L155 only; not named in DP10 |
| Trades | `CONCLUSION` `…/inquiry/hour-price`; `DAYTRADE` `…/inquiry/daily-price` | ⭕ | D3 L58–59; DP10 |
| Symbol master | `JCODES` `POST /api/v1/quote/kr-stock/inquiry/stock-ticker` | ⭕ | D3 L53; DP10 |
| WS trades / order book | `S00` 주식체결가, `S01` 주식호가 | ⭕; paper port 17070 | D3 L75–76; DP6 |
| Token | `token` | ⭕ | D3 L17 |

Account/order differences (named only): paper orders accept only "지정가,
시장가, 최유리지정가, 최우선지정가" (DP4 주식종합주문 description); D4 L171
"모의투자 FOK, IOC는 제공하지 않습니다."; NXT order TRs `CSPAT00610/00710/00810`
are ❌ (D3 L34–36); several account queries are ❌ (e.g. 당일매매손익 조회,
D3 L40); 해외선물옵션 has no paper at all (D3 L6).

### 5.5 Limits and data quality in paper

- **Data source (REST):** DP11: "모의투자 앱에서도 투자정보 서비스 API
  사용가능하도록 API 라우팅 작업을 진행하였으나 (당사 모의투자 시스템에서는
  시세를 제공하지 않아, 운영 시스템 시세 API호출하도록 개선)". REST paper
  market data is therefore served by the **production quote system**, not a
  simulator (publisher guide). Delay is not stated.
- **Data source (WebSocket):** **not documented** for port 17070.
- **Rate limits:** no paper-specific figures. REST "앱(계좌)별 20 TPS" and
  per-API TPS (D4 L210, L212; DP13), token "1분에 1건" (DP5, DP13). D3 has a
  single TPS column used for both modes. DP13 is the only environment split:
  "한 IP당 웹소켓 각 포트별 40세션 연결 가능 (실전투자 - 40세션, 모의투자 -
  40세션, 해외선물옵션 - 40세션)". **Inference:** because limits are per app
  (account) and the paper app has its own key and account, paper calls
  probably count against a separate bucket; not stated.
- **Service hours:** not found for paper. D4 L168 "모의투자 장시작전 입니다."
  (an `M100` order-side message) implies paper order hours exist.
- **Paper-only messages (D4):** `00000` "모의투자 데이터가 없습니다." and
  "모의투자 조회가 완료되었습니다." (L108–109, success code);
  `M001` "서비스가 지연처리되고 있습니다. …" with note "모의투자 시스템 관련
  메시지" (L161); twelve `M100` messages (L162–173), e.g. "모의투자에서는
  해당업무가 제공되지 않습니다.". WS `10005` "허용되지 않는 tr_cd 입니다."
  (L184) — the SDK hint (D7 L81, client code) reads it as "현재 모드(운영/
  모의)에서 허용되지 않습니다".
- **Paper-only incident (DP11):** on 2025-10-23 the routing change broke
  paper business APIs with `rsp_cd` `M024` "Interface ID(QID)를 찾을수
  없습니다."; "운영 서비스는 이상이 없었으며, 모의투자 서비스만 현상이
  발생하였습니다." `M024` is not in D4.

### 5.6 Contradictions and gaps

1. **Paper-support rule vs matrix.** D2 L738: an API is paper-capable if its
   portal description contains "※ 모의투자 계좌로 사용가능한 API입니다.";
   "그 외는 실전투자 환경에서만 호출됩니다." The phrase appears only on
   order/account APIs (DP4); **no** quote, chart or real-time description
   carries it (DP2, DP3, DP6), yet D2 L740 and D3 mark them all ⭕. DP10/DP11
   (2025-10-23) support ⭕ for the three quote groups; the chart group rests
   on D3/D2 alone.
2. **Success code with no paper data.** `00000` "모의투자 데이터가 없습니다."
   (D4 L108) is a success code; after DP11's routing, whether market-data
   routes can still return it is not documented. An empty result under
   `00000` must not be read as "no trades/quotes" without that check.
3. **Edited FAQ.** DP13's title says "2026.9.14 기준" while `createdDate` is
   2024-08-08; the portal exposes no revision history.
4. **SDK default is paper.** D5 L122 defaults `mode` to `"demo"`; the web
   tester auto-issues from the 실전 key (D2 L280). Both are client
   conveniences, not server behaviour.
5. **Mismatch detection.** No documented error for "production token on the
   paper WS port" or the reverse. `10009` "token 계좌정보와 서버정보가 일치하지
   않습니다." (D4 L186) is a candidate. **Inference** only.

### 5.7 Implications for a first authorized smoke test (Inference only)

- Paper is the natural first target for: paper-key token issuance and its
  re-issue rule (same token, same expiry), REST envelope/`rsp_cd` handling,
  and decoding of `PRICE`, `HOGA`, `CONCLUSION`, `CHARTMIN`/`CHARTDAY` and
  `JCODES` payloads — DP11 says these come from the production quote system,
  so field shapes are plausibly the same as production.
- Paper **cannot** prove: production app-key acceptance or entitlement
  (`IGW40342`); production per-app TPS behaviour; port 7070 behaviour; NXT
  order paths; that the 2025-10-23 routing still applies on the test day;
  or that chart routes are routed the same way.
- The origin cannot reveal the environment. A production key labelled as
  paper would silently reach production (also recorded in
  `live-auth-transport-gates-2026-11-05.md` on `main` @ `a5d2639e`, L91–95,
  where ADR 0015 adds explicit caller acknowledgements). KTradeLink
  must carry environment provenance from configuration, never infer it, and
  never fall back.
- A WS test must pair the paper token with port 17070; mismatches are not
  documented (§5.6 #5).

### 5.8 Gates and not-verified items

- Not verified: any paper or live response; paper market-data latency or
  timestamps vs production; paper WS feed source; paper hours; paper TPS.
- Gate: explicit separate authorization for paper credentials and for each
  paper network call; orders (even paper) need their own authorization.
- Gate: environment is a declared, recorded property of the credential
  profile; mixing a paper token with production WS (or the reverse) must be
  rejected before sending.
- Gate: treat `00000` + "모의투자 데이터가 없습니다." as "no data from paper",
  distinct from an empty production result.

## 6. Toss Securities

### 6.1 Pinned sources

Public Toss documents retrieved 2026-11-05 07:58:32–07:59:18 UTC. T1–T5 have
the **same sha256** as the trade-evidence copies (07:10–07:11Z) and the
inventory copies (06:55Z), so nothing changed during the day.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json) | sha256 `c5918961335ccd6b`, 07:58:32Z; `openapi 3.1.0`, `info.version 1.2.28` | L8–12 `servers` (one entry); `components.securitySchemes.oauth2ClientCredentials`; `paths./oauth2/token`; `components.schemas.OAuth2TokenRequest` |
| T2 | [overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md) | sha256 `bef057d9babe9a38`, 07:58:34Z | L18, L36, L62, L89–97, L209–210, L236–264 |
| T3 | [faq.md](https://openapi.tossinvest.com/openapi-docs/faq.md) | sha256 `6ad4c02b8e785f7d`, 07:58:35Z | L3, L9, L50 |
| T4 | [developers.tossinvest.com/llms.txt](https://developers.tossinvest.com/llms.txt) | sha256 `bbff77eaa55df248`, 07:58:35Z | L9–10 servers; L16 T1 is source of truth |
| T5 | [asyncapi.json](https://openapi.tossinvest.com/openapi-docs/latest/asyncapi.json) | sha256 `46669a360d4c5c64`, 07:58:35Z; `asyncapi 3.0.0`, `info.version 1.2.3` | `servers` has one key, `production` |
| T6 | [api-reference/README.md](https://openapi.tossinvest.com/openapi-docs/latest/api-reference/README.md) | sha256 `39bc07740f869dbc`, 07:59:16Z | Search only |

Search terms run over T1–T6 (case-insensitive): "모의", "sandbox",
"샌드박스", "paper", "mock", "staging", "demo", "simulat", "테스트 환경",
"dry run", "validateOnly". **No match** in any of them. The browser pages
`developers.tossinvest.com/` and `/docs` (sha256 `c6c355fc66070915`,
`23edd501b20d1587`, 07:59:17–18Z) are script shells with no static text on
the topic.

**Missing evidence:** any paper, sandbox, test-key or test-origin
statement — **not found**.

### 6.2 Does a paper environment exist?

**Not found.** T1 has one server, `https://openapi.tossinvest.com`
(L8–12); T5 has one WS server keyed `production`; T4 L9–10 lists one REST
and one WS server. No document names 모의투자, sandbox or test mode.

Key registration (process only, production): T2 L209 "토스증권 WTS에 로그인
후 설정 > Open API 메뉴에 진입하여 `client_id` 와 `client_secret` 을
발급받습니다."; L210 allow-listed IP registration is required ("등록된 허용
IP 목록에 없는 IP 에서의 호출은 403 으로 차단됩니다").

### 6.3 Origins and identifiers

| Concern | Production | Paper | Evidence |
| --- | --- | --- | --- |
| REST origin | `https://openapi.tossinvest.com` | not found | T1 L8–12; T4 L9 (field table) |
| WebSocket origin | `wss://openapi-ws.tossinvest.com/ws/v1` | not found | T5 `servers.production`; T4 L10 |
| Token route / behaviour | `POST /oauth2/token`, form, `client_credentials`; "client 당 유효한 access token 은 1 개입니다. 재발급 시 이전에 발급된 token 은 즉시 무효화됩니다." (T1); FAQ: "새로 발급하면 직전 토큰은 즉시 무효화되어 `401 token-revoked` 로 거부됩니다." (T3 L9) | not found | T1 `paths./oauth2/token` description (field table); T3 L9 (publisher guide) |
| TR-id / api-id differences | n/a (REST paths + `operationId`) | not found | T1 |
| Required header differences | `Authorization: Bearer`; `X-Tossinvest-Account` for account, order and conditional-order groups only | not found | T2 L18, L36, L62 |

The placeholder `client_id` in T1/T2 examples contains a `live` segment and
no other variant is shown. **Inference:** this may hint at a key-type
prefix, but no test key type is documented.

### 6.4 Market-data route availability in paper

No paper environment, so no route is paper-capable. Production routes, for
reference: T2 L89–97 "Market Data — 시세".

| Capability | Route | Paper supported? (verbatim) | Evidence |
| --- | --- | --- | --- |
| Current price | `GET /api/v1/prices` | not found (no paper environment) | T1, T2 L94 |
| Order book | `GET /api/v1/orderbook` | not found | T1, T2 L93 |
| Candles (1m, 1d) | `GET /api/v1/candles` | not found | T1, T2 L97 |
| Trades | `GET /api/v1/trades` | not found | T1, T2 L95 |
| Symbol master | `GET /api/v1/stocks`, `GET /api/v1/stocks/all` | not found | T1 |

Account/order differences: none to name; account, order and
conditional-order groups exist only against the single production server.

### 6.5 Limits and data quality in paper

Not applicable — no paper environment documented. Production limits for
context only: "클라이언트 × API 그룹" TPS (T2 L236), e.g. `MARKET_DATA` "초당
최대 15회" and `MARKET_DATA_CHART` "초당 최대 20회" (T2 L250–251), adjustable
"사전 공지 없이" (T2 L238, L264). T3 L50 says Open API order hours follow
the trading system ("매매 시스템의 주문 가능 시간을 그대로 따릅니다").

### 6.6 Contradictions and gaps

1. **OpenAPI version label.** T4 L16 calls T1 "OpenAPI 3.0"; T1 declares
   `3.1.0` (already noted in the trade/candle ledgers).
2. **Server naming.** T5 keys its only server `production`. **Inference:**
   the name alone does not imply that another environment exists.
3. No contradiction found about paper; absence is consistent across T1–T6.

### 6.7 Implications for a first authorized smoke test (Inference only)

- There is no non-production rehearsal. Before any live call, the only
  evidence is offline: T1 schemas and examples as synthetic fixtures.
- A first authorized test could only be production, read-only market data
  (token only, no `X-Tossinvest-Account`), from an allow-listed IP.
- Issuing a token revokes the client's previous token (T3 L9), so a smoke
  test can disrupt any other process using the same client; this needs to
  be part of the authorization.
- Orders cannot be rehearsed anywhere; they stay out of scope.

### 6.8 Gates and not-verified items

- Not verified: absence of an undocumented sandbox (only documents were
  read); any live behaviour.
- Gate: no `PAPER` environment value may be offered for Toss; a request for
  paper must fail closed rather than fall back to production.
- Gate: explicit authorization for the production client, IP allow-list
  entry and each live call; token issuance treated as a state-changing act.

## 7. Meritz Securities

### 7.1 Pinned sources

GitHub repository
[`meritz-securities/open-api@a93c6409`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89)
(`a93c6409db73ea97ad15f7b7186f36c9f32ecd89`, committer date
2026-10-28T22:32:03+09:00), fetched 07:54:54Z; blob SHAs from
`git rev-parse`. Portal `https://openapi.imeritz.com` retrieved
07:59:54–08:01:12Z. Repo README L11 makes the portal canonical, so repo text
ranks below MP2/MP4.

| # | Path / URL | Pin | Used for |
| --- | --- | --- | --- |
| M1 | [`README.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/README.md#L125) | blob `61aa5f7f2c1059a29a99175a5cdf573996d81479`; L125 | "모의계좌는 없습니다" |
| M2 | [`llms.txt`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/llms.txt#L101-L120) | blob `8351d5343d785b61107179d19197c59a08e1edff`; L101, L109–118, L120 | Default server, real account, app key bound to its server, `mac_address` required |
| M3 | [`DISCLAIMER.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/DISCLAIMER.md#L27) | blob `1ecb0ebd63232e1de6b33a11ce55728655627f84`; L4, L27 | Real account |
| M4 | [`SECURITY.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/SECURITY.md#L23-L25) | blob `3ef48de49497587f4fc299a48af9a9a92660216c`; L23–25 | "모든 요청이 실계좌로 나간다고 전제하십시오." |
| M5 | [`meritz/core/config.py`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/meritz/core/config.py#L1-L148) | blob `50f2c7f93bf329655afec252670a82018f45f976`; L3–4, L14–15, L72–74, L132–148 | Only `PROD`/`PROD_WS`; override → env "custom" (client code) |
| M6 | repo `openapi.json` | blob `93e900e66b965607d7fd8b8e14c6088d710e6fce`; L8–11; `info.version` `2026-10-28` | Single server, description "운영" |
| M7 | repo `asyncapi.json` | blob `c108c3c52288d5296b2871582ff856d532073242`; L8–10; `info.version` `2026-10-22` | Single WS server `prod` |
| M8 | repo `meritz/data/catalog.json` | blob `000c2dbc636ad46077d4f46d67a04e0cd6fe1319` | Every API's `domain` has only a `prod` key (73 REST `…:9443`, 14 WS `…:29443/websocket`) |
| M9 | [`docs/errors.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/docs/errors.md#L75-L92) | blob `b4b2eac6541bd2b886071c1caad17fa0c57ba3e6`; L75, L92 | `EGW00103` "개발 앱키를 운영 서버에 쓴 경우" |
| M10 | [`CONTRIBUTING.md`](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/CONTRIBUTING.md#L66-L67) | blob `aaecaa006ce9654f85c016de4bc9839197c62de9`; L66–67 | "테스트를 위해 실제 API 를 호출하지 말아 주십시오." |
| MP1 | FAQ "Open API 모의투자 기능 있나요?" — `/api/forums/10000000-0000-0011-0000-000000000002/posts/356f5fc1-5db0-45c6-a0c1-53cdbaed104a` | sha256 `d9c3665bc59448e5`, 08:01:09Z; `createdDate` 2026-09-17T19:34+09:00 | Explicit "no paper" |
| MP2 | [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json) | sha256 `ce7c85787916484d`, 07:59:55Z, 1,136,519 bytes, `generatedAt "2026-11-05 16:55:11"`; normalised (without `generatedAt`, sorted keys) `2fff4f3e02d20cd5` — **identical** to the trade/candle copies | 0 matches for "모의", "mock", "demo", "paper", "sandbox", "simulat", "실계좌"; REST `domain` "" (72), WS `wss://openapi.imeritz.com:29443` (14) |
| MP3 | [apiservice](https://openapi.imeritz.com/apiservice) (HTML) | sha256 `18fb34d1def00212`, 08:00:15Z | Row "모의투자 Domain" is `style="display: none;"` and the page script never shows it |
| MP4 | `/api/apis/public/api-list/<group>` for all six groups (OAuth `1c647f61-…`, 계좌 `5bde10c9-…`, 국내주식 `441da3d2-…`, 해외주식 `7f77b304-…`, 실시간 국내 `6fdcbbbe-…`, 실시간 해외 `6e20c010-…`) | sha256 `e7b956b48f266bfa`, `6989ca0fea7f0184`, `8c33857167d5936b`, `e52b5391e440d4e0`, `75441f6745bc7d0a`, `5da357e2a2542546`; 08:00:28–08:00:33Z | 87 APIs; `simulatedDomain` **null for all 87** |
| MP5 | [testbed-lab](https://openapi.imeritz.com/testbed-lab) | sha256 `87bcdc6b679b0ceb`, 08:00:48Z | "테스트베드" sends no request |
| MP6 | [samplecode-py](https://openapi.imeritz.com/samplecode-py) | sha256 `77f8489abbfb238e`, 08:00:47Z (varies per request) | "모의계좌가 아니라 실제 계좌"; one WS endpoint |
| MP7 | FAQ "Open API 운영 시간은 어떻게 되나요?" — same forum, post `a40ed3f5-c115-45c4-979e-a9b5db7abbf0` | sha256 `2b075a23450609b3`, 08:01:10Z; `createdDate` 2026-09-17 | Production query hours |
| MP8 | [about-openapi](https://openapi.imeritz.com/about-openapi) | sha256 `9379807871280d02`, 08:00:42Z | "테스트베드 메뉴에서 테스트가 가능합니다." |

Evidence levels: MP2, MP4 `field table`; MP1, MP3, MP5–MP8 `publisher
guide`; M1–M4, M9–M10 `publisher repo note`; M5–M8 `publisher client code`
or machine-readable repo data below MP2.

**Missing evidence:** no development/test origin is published, although M9
and M2 refer to app keys of other servers (§7.6 #1).

### 7.2 Does a paper environment exist?

**No (explicitly).** MP1: "현재 메리츠증권에서는 Open API 모의투자 기능을
제공하지 않습니다. 양해 부탁드리며, 향후 서비스 제공 계획이 있을 경우 별도
안내드리도록 하겠습니다." Consistent repo notes: M1 L125 "앱키에 연결된
계좌는 실계좌입니다. 모의계좌는 없습니다"; M3 L27; M4 L23–24; M10 L66–67;
MP6 "APP KEY 에 연결된 계좌는 모의계좌가 아니라 실제 계좌입니다."

The portal "테스트베드" is **not** a paper environment. MP5: "※ 본 화면은
개발 참고용 예시 화면으로, 실제 API 호출 및 실행 기능은 제공되지 않습니다."
and "모의 테스트입니다. 실제 API로 요청을 보내지 않고, API 가이드의 요청,
응답 예시를 보여 드립니다."

### 7.3 Origins and identifiers

| Concern | Production | Paper | Evidence |
| --- | --- | --- | --- |
| REST origin | `https://openapi.imeritz.com:9443` | not found (portal `simulatedDomain` null for all APIs) | MP4 (field table); M6 L8–11 ("운영"); M8; M5 L14 |
| WebSocket origin | `wss://openapi.imeritz.com:29443/websocket` | not found | MP4; M7 L8–10; MP6 "접속점은 이것 하나입니다" |
| Token route / behaviour | `POST /oauth2/token` (form, `scope=login`, per the auth gates doc on `main` @ `a5d2639e` L18) | not found | MP4 OAuth group; M8 |
| TR-id / api-id differences | n/a | not found | — |
| Required header differences | `mac_address` required: "**`mac_address` 헤더가 필수입니다.** 빠지면 요청이 거부됩니다." | not found | M2 L101 (repo note); how it is produced is out of scope and not described here |

### 7.4 Market-data route availability in paper

No paper environment, so no route is paper-capable ("현재 … 모의투자 기능을
제공하지 않습니다", MP1).

| Capability | Route | Paper supported? (verbatim) | Evidence |
| --- | --- | --- | --- |
| Current price, order book, candles, trades | 국내주식 group (30 REST APIs, e.g. `/market/v1/trades/ticks`) | "모의투자 기능을 제공하지 않습니다" | MP1; MP4 `simulatedDomain` null |
| Symbol master | `.mst` files (stock-info page; not paper-related) | same | MP1 |
| Real-time | 실시간 국내주식 (9 WS APIs) | same | MP1; MP4 |

Account/order differences: none to name — every order goes to the real
account bound to the app key (M2 L111–112; M3 L24–27).

### 7.5 Limits and data quality in paper

Not applicable. Production context only: MP7 "점검일 등 예외 사항이 없을 시,
24시간 조회 가능합니다."; M2 L120 "초당 호출 한도는 API마다 10건입니다."
(the capability inventory records a per-account reading of a portal notice;
not re-checked here).

### 7.6 Contradictions and gaps

1. **Other servers are implied but not published.** M9 L92: `EGW00103`
   "앱키 오타, 또는 **개발 앱키를 운영 서버에 쓴 경우**"; M2 L114 "앱키는
   발급받은 서버에서만 통합니다."; M5 L4 "앱키는 발급받은 환경에서만 통한다."
   No such server appears in MP2, MP4, M6–M8. **Inference:** a non-public
   development environment may exist; it is not offered as a paper
   environment (MP1) and must not be treated as one.
2. **"테스트" wording.** MP8 "테스트베드 메뉴에서 테스트가 가능합니다." reads
   like a test environment, but MP5 shows it only replays guide examples.
3. **Hidden portal row.** MP3 has a "모의투자 Domain" row that is never
   displayed. **Inference:** a portal-template remnant (the DB portal uses the
   same row and `simulatedDomain` field, DP1), not a feature.
4. **Spec export has no REST origin.** MP2 REST `domain` is "" for 72 APIs;
   the origin must come from MP4 or M6, not from MP2.
5. **Client override.** M5 L132–148 lets `MERITZ_BASE_URL` point elsewhere
   ("custom") and then requires an explicit `MERITZ_WS_URL`; client code
   only, no documented target.

### 7.7 Implications for a first authorized smoke test (Inference only)

- Every authorized call is production against a **real account**. The first
  test, if any, should be one read-only market-data call; account and order
  routes stay out of scope.
- The mandatory `mac_address` header (M2 L101) means even a read-only test
  needs a separately authorized decision on what value is sent; automatic
  device discovery is not an acceptable default.
- All errors arrive as HTTP 500 with `rsp_cd` (auth gates doc on `main` @
  `a5d2639e`, L18, L96–98), so a smoke test proves little unless `rsp_cd` is interpreted.
- Paper cannot be used to de-risk anything; offline fixtures from MP2
  examples are the only pre-live evidence.

### 7.8 Gates and not-verified items

- Not verified: existence or behaviour of any development server (§7.6 #1);
  any live behaviour.
- Gate: no `PAPER` environment for Meritz; a paper request must fail closed.
- Gate: explicit authorization for production credentials, the
  `mac_address` value and each live call; no order path without its own
  authorization and a duplicate-order safeguard.

## 8. Cross-broker comparison and paper-first smoke-test scope

### 8.1 Comparison

| Property | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Paper REST origin distinct from production | yes | yes | not documented | **no**: same origin, the app key selects | no paper | no paper |
| Paper WS origin distinct | yes (port only, plain `ws://`) | yes | yes (`simulationUrl`) | yes (port 17070) | no paper | no paper |
| Separate paper app key | yes | yes | yes | yes | — | — |
| Machine-readable per-route paper availability | **yes** (portal `virtualDomain` / `virtualTrId`) | no (one prose note + `8104`) | no | repo matrix ⭕/❌ (D3); portal `simulatedDomain` null for REST; the portal phrase rule contradicts the matrix | n/a | `simulatedDomain` null for all 87 APIs |
| Market-data TR / api id changes in paper | no | no | not documented | no | n/a | n/a |
| Documented paper rate limit | 1 req/s REST, token 1/s | not found | not found | none paper-specific; WS 40 sessions per port incl. paper | n/a | n/a |
| Documented env-mismatch error | `MCA00124` (paper key on production origin) | `8030`, `8031` | not found | none documented; WS `10009` is a candidate (inference) | n/a | `EGW00103` "개발 앱키를 운영 서버에 쓴 경우" (not paper) |
| Paper data quality / hours documented | no (fills follow real executions) | no | fills only 09:00–15:30 | REST quotes come from the production quote system (DP11); WS source and hours not documented | n/a | n/a |

### 8.2 Proposed paper-first smoke-test scope (Inference)

This is a proposal for the maintainer, not an authorization. Every item
needs an explicit, separate authorization naming the broker, environment,
credentials owner, routes and request count.

1. **Order and per-broker verdict:**

   | Broker | Paper smoke? | Why |
   | --- | --- | --- |
   | KIS | **first** | distinct paper origin and keys; per-route field table marks the ticker, order book, day and today's-minute candles and trades as paper-offered (§2.4) |
   | Kiwoom REST | **second** | distinct paper origin and keys; per-route service unknown, so the first call also shows whether `ka10001` is served or `8104` (§3.7) |
   | DB | **possible, with a caveat** | paper keys exist, but paper and production share one REST origin and the key alone selects the environment, and since 2025-10-23 paper REST quotes are served by the production quote system (DP11). A DB paper call therefore tests paper auth plus **production** market data, and a mislabelled production key would silently reach production (§5.7). KTradeLink currently refuses DB paper (§9). |
   | LS | **none** | no documented paper REST origin (§4.7) |
   | Toss | **none** | no paper environment found (§6.2) |
   | Meritz | **none** | explicitly no paper (MP1); the testbed sends no requests (MP5); any other server implied by `EGW00103` is an inference and is **not** a paper environment (§7.6 #1) |

   For LS, Toss and Meritz the only pre-live evidence is offline; any
   first network check would be a separately authorized **production**
   read.
2. **Per broker, at most:** one token request; one ticker request for one
   KRX symbol; optionally one order-book and one day-candle request on
   routes the publisher marks as paper-offered (KIS, DB matrix) or observes
   as served (Kiwoom). No WebSocket, no account, no order route.
3. **Pacing:** at least one second between KIS paper requests (K27); DB
   token issuance is "1분에 1건" (DP5). No automatic retry of any request,
   including after `EGW00201`, the `1700` series, `IGW00201`, `M001`,
   HTTP 5xx or a timeout.
4. **Record:** HEAD SHA, environment, origin, route, HTTP status, root
   status field and value, error code if any, and the delivery state —
   never the token, keys, account values or raw body (only sanitized,
   reviewed fixtures).
5. **Paper can show:** the paper host's TLS chain and reachability; the
   token request/response shape and expiry field format in that
   environment; header names accepted; that the TR / api id is served in
   paper; the status envelope (`rt_cd`, `return_code`) and decoder field
   names on a real paper response; the error code for an unsupported
   route (`8104`) or mismatched key (`MCA00124`, `8030`/`8031`); for DB,
   the decoding of production-sourced quote payloads under a paper key
   and the paper-only `rsp_cd` messages.
6. **Paper cannot show:** production origin, TLS and availability (except
   that DB's paper REST origin *is* the production origin); production app
   keys, entitlements and acceptance (e.g. DB `IGW40342`); production rate
   limits (KIS 18/s vs 1/s; DB per-app buckets); production-only routes
   (KIS by-date minutes, symbol info, holidays, VI); NXT / 통합 / SOR
   venues; whether paper quotes equal production quotes in value, timing
   or sign (for DB only the REST source is stated, not latency; the paper
   WS source is undocumented); that DB's 2025-10-23 routing still applies
   on the test day or covers the chart group; production token lifetime
   and re-issue behaviour; production error universes; anything about
   accounts or orders (KIS paper fills are simulated by a separate
   operator, K25/K30; DB paper offers fewer order types). Nothing about
   LS, Toss or Meritz production can be learned from any paper call. A
   paper success therefore leaves every `documented_candidate` capability
   at that state for production.

## 9. Relation to existing code and documents

None of the files below is edited by this change. Matches and differences
are recorded only.

| Code or document and claim | This audit |
| --- | --- |
| `src/ktradelink/_request_plan.py` `_LIVE_ORIGINS` / `_PAPER_ORIGINS`: KIS paper `https://openapivts.koreainvestment.com:29443`, Kiwoom paper `https://mockapi.kiwoom.com`; no LS/DB/Toss/Meritz paper origin | **Matches** K11–K17, K19–K21 (KIS) and W1/W2 (Kiwoom). LS has no documented paper REST origin (§4.3); Toss (§6.2) and Meritz (§7.2) have no paper environment; their absence matches. **DB differs:** DB documents paper on the **same** REST origin `https://openapi.dbsec.co.kr:8443` (D1 L13–14, D2 L693), so DB paper is refused by the planner (`environment_not_documented`) although the publisher offers it. |
| DB `live` path (ADR 0015 gate 2; `_token_codec` `db_production_key_acknowledged`) | **Consistent** with §5.2/§5.7: the origin cannot tell paper from production, so a paper (`vtl_`) key used under `live` would reach the paper system, and a production key labelled as paper would reach production. The acknowledgement records the caller's claim; it does not verify it. ADR 0015's "only the `live` label exists" stands. |
| `_https_transport` / `_public_client`: Toss and Meritz offer `live` only | **Matches** §6 and §7 (no paper). |
| `_request_plan._origin`: only `"live"` / `"paper"`; unknown or undocumented environment raises `QuotePlanUnavailable`; origins are never taken from callers | Consistent with G-P1. Differs from the publisher clients' environment-variable origin override (Kiwoom W3 L42–59; KIS MCP `KIS_URL_REST_PAPER`), which is not adopted. |
| `authentication_requirements`: KIS token path `/oauth2/tokenP`, Kiwoom `/oauth2/token`, on the environment's origin | **Matches** K11 (token offered on VTS) and W1 au10001 (mock domain listed). |
| `plan_ticker_request` KIS: `tr_id` `FHKST01010100` in both environments, `fid_cond_mrkt_div_code=J` | **Matches** K12/K17 (`virtualTrId` `FHKST01010100`). KRX-only matches the paper venue limitation (K29). The planner does not rewrite TR ids; no rewrite is needed for `F…` ids (K2 L453–455 rewrites only `T`/`J`/`C`). |
| `_order_book_plan` KIS `FHKST01010200` "same tr_id for real and demo" | **Matches** K12. |
| `plan_ticker_request` Kiwoom `api-id` `ka10001`, same in both environments | Matches W2 (same api-id in MOCK). Paper service of `ka10001` is **not documented** (§3.4); only `8104` would reveal it. |
| `_public_client.ENVIRONMENTS = ("live", "paper")`; `connect()` requires `environment`, "there is no fallback between them" | Consistent with G-P1. Differs from publisher tools that default to paper when none is given (K5 L289, L544; W7 L248; W8 L52) and from the KIS sample's cross-environment token-file fallback (K2 L88–104). |
| `_public_client._capability` / `capabilities()`: KIS live/paper, Kiwoom live/paper and LS live are `documented_candidate`; LS paper `unsupported` (`environment_not_documented`) | KIS paper: supported by a per-route field table (K12). Kiwoom paper: rests on the generic mock domain only (W1), weaker evidence than KIS. LS paper refusal matches §4. |
| `CredentialIdentity(broker, environment, …)` binds credentials to one environment (`_credential_runtime.py`) | Matches the separate paper keys at KIS, Kiwoom and LS (§2.2, §3.2, §4.2). Environment-mismatch error codes (`MCA00124`, `8030`, `8031`) are not mapped specifically; the transport classifies by HTTP status only. |
| `_public_client` sends ≤ 1 token + ≤ 1 quote per `fetch_ticker`, no retry, no pacing | No retry matches G-P5. No pacing: two KIS paper requests back to back may exceed "(모의투자) 1초당 1건" (K27); the token limit is stated separately (1/s), and whether the two share one budget is not documented. |
| [ADR 0013](../decisions/0013-public-fetch-ticker-surface.md) item 9: "Only the planner's documented origins are used: KIS live/paper, Kiwoom live/paper, LS live. LS paper is refused; there is no fallback between live and paper." | Consistent with §2–§4. |
| ADR 0013 "Unverified: … Live and paper acceptance …" | Unchanged; nothing here is paper-verified. |
| [live-auth-transport-gates](live-auth-transport-gates-2026-11-05.md), KIS row: "Live/paper source/session still unverified" | Unchanged. This audit adds the per-route paper matrix and paper limits, not verification. |
| Same ledger, KIS header gaps (`custtype`, `tr_cont` omitted; content-type differs from the sample) | Not paper-specific; the sample sends the same header names in both environments (K2 L457–459). |
| [Capability inventory](capability-inventory-2026-11-05.md) row 7, KIS: "paper 'lower', no numbers · PR · K6" | **Superseded by numbers:** "(모의투자) 1초당 1건", token 1/s (K27). |
| Same inventory, KIS notes: "K1 paces 0.05 s (prod) / 0.5 s (paper) between calls" | **Differs:** those assignments are local to `changeTREnv`; the effective pause stays 0.1 s (K2 L57, L169–179, L288–293; scoping inference, §2.5). |
| Same inventory, KIS notes: "Market-data TRs use the same `tr_id` for real and demo; account/order TRs switch `T…`→`V…`" | **Confirmed** by the portal field table (K12, K16); 18 of 23 order/account APIs are not offered in paper at all. |
| Same inventory, Kiwoom notes: every entry lists both domains; `8104` shows per-API support is not guaranteed | **Confirmed**; `ka01690` is the one explicit "모의투자를 지원하지 않습니다" (W1 L972). |
| Same inventory, LS notes: keys issued for 실전 or 모의; WS `simulationUrl` only; no REST mock origin | **Confirmed** (L1, L6). |
| Same inventory row "Orders: documented paper env" (KIS ✓, Kiwoom ✓, LS ~) | Not re-examined (orders named only). |
| [kiwoom-market-data.md](kiwoom-market-data.md): portal "paper accounts have additional per-TR restrictions" | Not in this pin set; portal guide pages could not be retrieved (§3.1). |
| [order-book evidence](order-book-evidence-2026-11-05.md): KIS `FHKST01010200` for `real` and `demo` | **Confirmed** (K12). |
| [Candle evidence](candle-evidence-2026-11-05.md) (on `main` since PR #31) §2.7 item 3 (L253–255): by-date minute route `FHKST03010230` "Paper support is therefore unknown"; G-gate L1366 "[KIS] by-date minute paper availability is undocumented" | **Resolved by field table:** "모의투자 미지원" / "모의투자 미지원" (K12, record dated 2026-08-12T15:53:16+09:00). That file could cite K12; not changed here. |
| [Trade evidence](trade-evidence-2026-11-05.md) (on `main` since PR #33) G-H2 (L1482–1485): "identical [KIS] TR ids"; "[LS] documents no paper REST origin" | **Confirmed**; all three KIS trade routes are paper-offered (K12). |
| Symbol-master evidence (branch `claude/issue-17-symbol-master-evidence` @ `b127724ee73fac239d987a2fa2a5b889c5f92bfb`, not merged): LS "No REST paper origin is documented" | **Confirmed**. KIS `CTPF1002R` / `CTPF1604R` are "모의투자 미지원" (K13). Its DB legend "⭕ — 모의투자(`mode: "demo"`) + 실전투자 모두 호출 가능" (D3) is the same source as §5.4. |
| live-auth-transport-gates, DB row and DB gate (L91–95): "Live and demo share one REST origin (the app key decides)"; "a mislabelled live/demo app key is undetectable by the transport" | **Confirmed** (D1 L13, D2 L693, D8 L29). New: since 2025-10-23 paper REST quotes are served by the production quote system (DP11). |
| Same ledger, Meritz row and gate (L18, L96–98): every error is HTTP 500 with `rsp_cd` | Not paper-specific; Meritz has no paper (MP1). |
| Capability inventory row "Orders: documented paper env" (DB ✓, Toss ✗, Meritz ✗) and notes ("D1 … 모의투자 ⭕/❌"; Meritz "real account, not a mock account") | **Consistent** with §5–§7 (orders named only). |
| Capability inventory, Meritz notes: "M2 has no 모의투자 domain for any API" | **Confirmed** for all 87 APIs (MP4) and now backed by an explicit FAQ (MP1). |
| Candle evidence §5 (DB): `00000` can also mean "모의투자 데이터가 없습니다." | **Consistent** (D4 L108); §5.6 #2 adds that the DP11 routing leaves open whether market-data routes can still return it. |
| Trade evidence G-H2: "[DB] ⭕ in the SDK matrix on one shared origin"; "[Toss] none"; "[Meritz] has **no paper environment**" | **Confirmed**; DB chart-group paper support rests on D2/D3 only (§5.6 #1). |

## 10. Gates

These must be satisfied, or decided by the maintainer, before any paper
or live call. Broker tags are in brackets.

- **G-P1 No silent LIVE/PAPER fallback.**
  - The environment is always explicit; there is no default. Publisher
    tools that default to paper ([KIS] MCP, [Kiwoom] CLI/MCP) are not a
    model.
  - Origins come only from the reviewed allowlist, never from process
    environment variables ([Kiwoom] W3, [KIS] MCP) or caller input.
  - A token, cache entry or credential issued for one environment is
    never used for the other ([KIS] K2 L88–104 is the counter-example).
  - An error in one environment never triggers a request to the other.
  - [LS] paper stays refused until a paper REST origin is documented.
  - [DB] the origin cannot reveal the environment; it is a declared,
    recorded property of the credential profile (ADR 0015
    acknowledgements), never inferred, and a paper token is never paired
    with the production WS port 7070 or a production token with 17070.
    The DB SDK's default `mode` `"demo"` (D5 L122) is not a model.
  - [Toss] [Meritz] no `paper` value is offered; a paper request fails
    closed and never falls back to production. A [Meritz] development
    server implied by `EGW00103` (M9 L92) is not a paper environment.
- **G-P2 Paper success is not production evidence.** A paper response
  does not change any production capability state, fixture provenance,
  rate-limit assumption, venue claim or decoder contract (§8.2 item 6).
  Paper fixtures must be labelled with their environment and never used
  as production fixtures. [DB] Even though paper REST quotes come from the
  production quote system (DP11), a DB paper success does not prove
  production keys, entitlements, limits or the WS feed.
- **G-P3 Environment-mismatch errors are configuration errors.**
  [KIS] `MCA00124` (K20), [Kiwoom] `8030` / `8031` (W1), [DB] WS `10009`
  and `10005` (D4, candidates only), [Meritz] `EGW00103` (M9): surface
  them, do not retry and do not switch environments.
- **G-P4 Paper-unsupported routes fail closed.** [KIS] routes marked
  "모의투자 미지원" (K12–K16) must be refused offline for `paper` before
  anything is sent, if they are ever planned. [Kiwoom] `8104` surfaces as
  an unsupported capability, not as a reason to try production. [DB]
  `M100` "모의투자에서는 해당업무가 제공되지 않습니다." likewise. [DB]
  Success `00000` with "모의투자 데이터가 없습니다." means "no data from
  paper", never an empty production result (§5.6 #2).
- **G-P5 No automatic retries, in paper too.** Publisher advice to retry
  ([KIS] K27 "즉시 재호출", [LS] L8 "재시도하도록 구현하세요") is not
  adopted. [KIS] paper is 1 REST request per second and 1 token request
  per second (K27); [DB] token "1분에 1건" (DP5) and `M001` "서비스가
  지연처리되고 있습니다" (D4 L161) are not retry triggers; any smoke test
  paces manually.
- **G-P6 Trading TRs and ledger selection.** [KIS] the TR id can select
  the ledger regardless of origin (K19), and trading TR ids differ
  (`T…`/`V…`). No KTradeLink code may rewrite TR ids automatically.
  Account and order routes stay out of scope and need their own
  authorization in every environment. [Meritz] every order reaches a
  real account (M2, M3) and needs a duplicate-order safeguard as well.
- **G-P7 Venue in paper.** [KIS] paper trading is KRX only and NXT is not
  supported (K29); NXT/통합 paper feeds are "모의투자 미지원" (K15). Paper
  quote requests stay KRX-only; NXT/SOR/통합 behaviour can only be
  learned in production under separate authorization. [DB] NXT order
  TRs `CSPAT00610/00710/00810` are ❌ in paper (D3; named only).
- **G-P8 Transport.** [KIS] paper and production WebSocket origins are
  plain `ws://`; WebSocket is out of scope until a transport-security
  decision exists. [LS] paper WS has only a server-level `simulationUrl`.
  [DB] paper WS is a separate port (17070) whose data source is not
  documented.
- **G-P9 Authorization.** Real authentication, any network call (paper
  included), account access and orders each need explicit, separate
  maintainer authorization. Nothing runs in CI. No secret discovery.
  [Toss] token issuance revokes the client's previous token (T1, T3 L9)
  and is a state-changing act; calls come only from an allow-listed IP
  (T2 L210). [Meritz] the required `mac_address` value (M2 L101) needs
  its own decision; no device discovery.

## 11. Not verified

- Any paper or production response for any route. No broker API request
  was sent.
- KIS:
  - paper market-data quality (real-time, delayed or operator-generated)
    and paper market-data hours;
  - whether `NX` / `UN` are accepted on paper quote routes;
  - whether the token and REST budgets in K27 are shared or separate, and
    which statement is current where K22, K23, K27 and K30 differ;
  - whether a paper token is rejected by production routes (only the
    reverse case is documented);
  - the 6-hour same-token rule (K11) in paper;
  - the effective pacing of the sample client (scoping inference only).
- Kiwoom:
  - which market-data routes are served in paper (no per-API matrix);
  - paper rate limits, hours, data quality and venue coverage (`_NX`,
    `_AL`);
  - the portal's 모의투자 이용안내 and API guide pages (not retrieved).
- LS:
  - how a paper REST request is routed (origin, token, TR id);
  - which market-data TRs exist in paper; paper limits and data quality;
  - LS notices (forum endpoints answered 302).
- DB:
  - paper market-data latency and timestamps versus production; the
    paper WebSocket feed source; paper hours and paper TPS;
  - whether the 2025-10-23 routing (DP10/DP11) still applies and covers
    the chart group (`CHARTMIN`, `CHARTDAY`);
  - whether market-data routes can still return `00000` "모의투자 데이터가
    없습니다.";
  - the error, if any, for a paper token on port 7070 or the reverse.
- Toss: absence of an undocumented sandbox (only documents were read).
- Meritz: existence or behaviour of any development server (§7.6 #1).
- Entitlements, paper/production data parity and redistribution rights for
  all brokers (not researched).
