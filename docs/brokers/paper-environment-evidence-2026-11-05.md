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
- **Draft state:** §2–§4 (KIS, Kiwoom, LS) are complete. §5–§7 (DB, Toss,
  Meritz) are written separately and are `pending` in this draft; the
  DB/Toss/Meritz columns of §1 and §8 are `pending` until then.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS and Kiwoom: shallow clones of the pinned commits, 07:54–07:56;
    `git ls-remote` showed each pinned SHA as the remote `HEAD`.
  - KIS developer portal JSON and pages: 07:58:57–08:02:22 (§2.1).
  - Kiwoom portal home page: 08:03 (§3.1).
  - LS portal pages and JSON guides: 08:05:40–08:07:26 (§4.1).
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
| Paper exists? | yes, "모의투자" (F+G+C) | yes, "모의투자" / `MOCK` / `demo` (F+C+N) | yes, "모의투자 OPEN API" applied for separately (G) | pending (§5) | pending (§6) | pending (§7) |
| Selection mechanism | separate origin **and** separate app key; trading TR ids switch to `V…` (F+G+C) | separate origin and separate app key; same api-id; wrong pairing → `8030`/`8031` (F+N) | separate app key (G); REST origin selection **not documented**; onboarding says "tr_id 값이 실전/모의를 구분해요" (G, non-authoritative) | pending | pending | pending |
| REST origin | `https://openapivts.koreainvestment.com:29443` vs `https://openapi.koreainvestment.com:9443` (F+G+C) | `https://mockapi.kiwoom.com` vs `https://api.kiwoom.com` (F+E+C) | **no paper REST origin documented**; guide lists only `https://openapi.ls-sec.co.kr:8080` (F); onboarding sends paper orders to `:8080` (G) | pending | pending | pending |
| WS origin | `ws://ops.koreainvestment.com:31000` vs `:21000`, plain `ws://` in both (F+C) | `wss://mockapi.kiwoom.com:10000` vs `wss://api.kiwoom.com:10000` (F+C) | `simulationUrl` `wss://openapi.ls-sec.co.kr:29443` vs `:9443` (F) | pending | pending | pending |
| TR-id change | market-data TR ids identical (F); trading TR ids `T…` → `V…` (F+G); sample client rewrites leading `T`/`J`/`C` (C); WS 체결통보 `H0STCNI0` → `H0STCNI9` (F) | none: same `api-id` in both (F+E) | not documented in the guide (F); onboarding uses a different order TR for paper (G, conflicts with the catalog) | pending | pending | pending |
| Market-data availability | per-API "모의 Domain" / "모의 TR ID" fields; current price, order book, day candles, today's minute candles and trades **offered**; by-date minutes, symbol info, holidays, VI, NXT/통합 WS: "모의투자 미지원" (F) | no per-API column; all 337 spec entries list a 모의투자 domain (F); only `ka01690` says "해당 API는 모의투자를 지원하지 않습니다" (F); error `8104` "모의투자에서 지원하지 않는 API 입니다." (F) | **not found**: no per-TR paper flag in the guide (F) | pending | pending | pending |
| Paper limits | REST "(모의투자) 1초당 1건" vs "(실전투자) 1초당 18건"; token 1/s (G); paper NXT unsupported for trading (G); paper run by a separate operator (G) | no paper number found; rate codes `1700`–`1702` without numbers (F) | no paper number found; per-TR `transactionPerSec` only (F); paper fills only "정규장 시간(09:00~15:30)" (G) | pending | pending | pending |

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

`pending` — written separately; to be merged before review.

## 6. Toss Securities

`pending` — written separately; to be merged before review.

## 7. Meritz Securities

`pending` — written separately; to be merged before review.

## 8. Cross-broker comparison and paper-first smoke-test scope

### 8.1 Comparison

| Property | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Paper REST origin distinct from production | yes | yes | not documented | pending | pending | pending |
| Paper WS origin distinct | yes (port only, plain `ws://`) | yes | yes (`simulationUrl`) | pending | pending | pending |
| Separate paper app key | yes | yes | yes | pending | pending | pending |
| Machine-readable per-route paper availability | **yes** (portal `virtualDomain` / `virtualTrId`) | no (one prose note + `8104`) | no | pending | pending | pending |
| Market-data TR / api id changes in paper | no | no | not documented | pending | pending | pending |
| Documented paper rate limit | 1 req/s REST, token 1/s | not found | not found | pending | pending | pending |
| Documented env-mismatch error | `MCA00124` (paper key on production origin) | `8030`, `8031` | not found | pending | pending | pending |
| Paper data quality / hours documented | no (fills follow real executions) | no | fills only 09:00–15:30 | pending | pending | pending |

### 8.2 Proposed paper-first smoke-test scope (Inference)

This is a proposal for the maintainer, not an authorization. Every item
needs an explicit, separate authorization naming the broker, environment,
credentials owner, routes and request count.

1. **Order:** KIS paper, then Kiwoom paper. LS has no documented paper REST
   path (§4.7). DB/Toss/Meritz: pending.
2. **Per broker, at most:** one token request; one ticker request for one
   KRX symbol; optionally one order-book and one day-candle request on
   routes the publisher marks as paper-offered (KIS) or observes as served
   (Kiwoom). No WebSocket, no account, no order route.
3. **Pacing:** at least one second between KIS paper requests (K27). No
   automatic retry of any request, including after `EGW00201`, `1700`
   series, HTTP 5xx or a timeout.
4. **Record:** HEAD SHA, environment, origin, route, HTTP status, root
   status field and value, error code if any, and the delivery state —
   never the token, keys, account values or raw body (only sanitized,
   reviewed fixtures).
5. **Paper can show:** the paper host's TLS chain and reachability; the
   token request/response shape and expiry field format in that
   environment; header names accepted; that the TR / api id is served in
   paper; the status envelope (`rt_cd`, `return_code`) and decoder field
   names on a real paper response; the error code for an unsupported
   route (`8104`) or mismatched key (`MCA00124`, `8030`/`8031`).
6. **Paper cannot show:** production origin, TLS and availability;
   production entitlements; production rate limits (KIS 18/s vs 1/s);
   production-only routes (KIS by-date minutes, symbol info, holidays,
   VI); NXT / 통합 / SOR venues; whether paper quotes equal production
   quotes in value, timing or sign; production token lifetime and
   re-issue behaviour; production error universes; anything about
   accounts or orders (KIS paper fills are simulated by a separate
   operator, K25/K30). A paper success therefore leaves every
   `documented_candidate` capability at that state for production.

## 9. Relation to existing code and documents

None of the files below is edited by this change. Matches and differences
are recorded only.

| Code or document and claim | This audit |
| --- | --- |
| `src/ktradelink/_request_plan.py` `_LIVE_ORIGINS` / `_PAPER_ORIGINS`: KIS paper `https://openapivts.koreainvestment.com:29443`, Kiwoom paper `https://mockapi.kiwoom.com`; no LS/DB/Toss/Meritz paper origin | **Matches** K11–K17, K19–K21 (KIS) and W1/W2 (Kiwoom). LS has no documented paper REST origin (§4.3), so its absence matches. DB/Toss/Meritz: pending. |
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
| Symbol-master evidence (branch `claude/issue-17-symbol-master-evidence` @ `b127724ee73fac239d987a2fa2a5b889c5f92bfb`, not merged): LS "No REST paper origin is documented" | **Confirmed**. KIS `CTPF1002R` / `CTPF1604R` are "모의투자 미지원" (K13). |

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
- **G-P2 Paper success is not production evidence.** A paper response
  does not change any production capability state, fixture provenance,
  rate-limit assumption, venue claim or decoder contract (§8.2 item 6).
  Paper fixtures must be labelled with their environment and never used
  as production fixtures.
- **G-P3 Environment-mismatch errors are configuration errors.**
  [KIS] `MCA00124` (K20), [Kiwoom] `8030` / `8031` (W1): surface them, do
  not retry and do not switch environments.
- **G-P4 Paper-unsupported routes fail closed.** [KIS] routes marked
  "모의투자 미지원" (K12–K16) must be refused offline for `paper` before
  anything is sent, if they are ever planned. [Kiwoom] `8104` surfaces as
  an unsupported capability, not as a reason to try production.
- **G-P5 No automatic retries, in paper too.** Publisher advice to retry
  ([KIS] K27 "즉시 재호출", [LS] L8 "재시도하도록 구현하세요") is not
  adopted. [KIS] paper is 1 REST request per second and 1 token request
  per second (K27); any smoke test paces manually.
- **G-P6 Trading TRs and ledger selection.** [KIS] the TR id can select
  the ledger regardless of origin (K19), and trading TR ids differ
  (`T…`/`V…`). No KTradeLink code may rewrite TR ids automatically.
  Account and order routes stay out of scope and need their own
  authorization in every environment.
- **G-P7 Venue in paper.** [KIS] paper trading is KRX only and NXT is not
  supported (K29); NXT/통합 paper feeds are "모의투자 미지원" (K15). Paper
  quote requests stay KRX-only; NXT/SOR/통합 behaviour can only be
  learned in production under separate authorization.
- **G-P8 Transport.** [KIS] paper and production WebSocket origins are
  plain `ws://`; WebSocket is out of scope until a transport-security
  decision exists. [LS] paper WS has only a server-level `simulationUrl`.
- **G-P9 Authorization.** Real authentication, any network call (paper
  included), account access and orders each need explicit, separate
  maintainer authorization. Nothing runs in CI. No secret discovery.

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
- DB, Toss, Meritz: pending (§5–§7).
- Entitlements, paper/production data parity and redistribution rights for
  all brokers (not researched).
