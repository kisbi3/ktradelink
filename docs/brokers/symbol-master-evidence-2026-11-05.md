# Six-broker symbol-master evidence — 2026-11-05

- **Scope:** the source of a future `load_markets()` for domestic equities:
  the symbol master / instrument list (종목 마스터, 종목정보 리스트) of KIS,
  Kiwoom REST, LS, DB, Toss and Meritz. The Shinhan comparison stays
  separate.
- **Status:** publisher-documentation audit only. **Nothing here is live- or
  paper-verified.** No KTradeLink `load_markets` implementation, decoder or
  request plan exists, and this file does not authorize one.
- **No broker API request was sent.** No token, credential, account, MAC
  value or order was used. Only public Git repositories, public
  documentation pages and public master files were fetched. The master
  files were fetched once each without authentication: the KIS KOSPI file
  (§2.1) and the Meritz KOSPI and KOSDAQ files (§7.1).
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS: Git objects fetched 07:21–07:24 from `github.com` at the pinned
    SHA. The public KOSPI master zip was downloaded once at 07:29:11.
  - Kiwoom: Git objects fetched 07:25–07:27 at the pinned SHA, plus the
    earlier pin by SHA for the tree comparison in §3.1.
  - LS portal: 07:20:47–07:22:49. DB portal: 07:23:20–07:24:13; the DB Git
    repository at a fixed commit.
  - Toss documentation: 07:20:44–07:21:19. Meritz portal: 07:21:43–07:25:38;
    the Meritz Git repository at a fixed commit; master files 07:23:45–47.
  - **Spot check, 07:37–07:39:** pins re-fetched and confirmed for LS (L1,
    L3, L5), DB (DP3, DP4; Git blobs D1, D2, D5 and the commit date), Toss
    (T1, T3) and Meritz (M3 canonical hash; commit `a93c6409` still remote
    `HEAD`; blobs README, LICENSE, `llms.txt`). No master file was
    re-downloaded.
- **Pin formats:**
  - Git: repository, full commit SHA and commit date; per file the Git blob
    SHA, i.e. `sha1("blob <len>\0" + bytes)`, what `git hash-object`
    prints, with a blob link at the commit.
  - Web pages have no immutable revision. Their sha256 prefix identifies
    only the copy retrieved at the stated time.
  - A downloaded master file is pinned by URL, retrieval time, byte size and
    sha256. **No file is committed and no row, name or individual code
    from one is quoted**; only aggregate properties are recorded (§2.2,
    §7.2).
  - Line numbers (`L…`) on web pages refer to the retrieved copy.
  - Raw copies were kept outside the repository. Sample tokens, account
    values, app keys, MAC values and staff contact data in publisher
    material are deliberately not copied.
- **Evidence levels:**
  - `field table`: a publisher field or spec table.
  - `publisher layout header`: a publisher C struct with field comments that
    describes a file record layout.
  - `publisher example`: a sample request/response or sample code.
  - `publisher client code`: SDK, parser or helper behaviour. It shows how
    the publisher uses the source; it is **not** a contract.
  - `publisher repo note`: non-code text in a publisher repository.
  - `portal prose`: descriptive text on a publisher portal page or FAQ.
  - `file observation`: aggregate-only properties of **one** downloaded copy
    (byte length, encoding, record count, distinct values of coded fields,
    code *shapes*, response headers). One snapshot; not a contract and not
    a cadence.
  - `field table (REST)`: a field table of a per-symbol REST route, cited
    where a master lacks the attribute.
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- **Data-rights caution:** no pinned source grants a right to store, cache
  or redistribute master content (§N.7 of each broker). Until the maintainer records
  a decision (G-R1), master content must not enter Git, fixtures, issues,
  logs or review material, and sample values in publisher examples are
  **not** authorized fixtures.

## 1. Broker × property summary

Evidence: `F` field table, `H` publisher layout header, `E` publisher
example, `C` publisher client code, `N` publisher repo note, `P` portal
prose, `O` file observation, `—` not found.

| Broker | Delivery | Venues / markets | Instrument types distinguished | Identifiers (short / standard / names) | Alphanumeric short codes | Trading attributes | NXT flag | Freshness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KIS | file: `kospi_code.mst.zip` / `kosdaq_code.mst.zip` / `konex_code.mst.zip` on `new.real.download.dws.co.kr`, zipped fixed-width cp949, no auth — H+C+O; publisher code disables TLS verification (unsafe) | one file per KRX market (유가증권 / 코스닥 / 코넥스); ELW in a separate file — H+C; NXT, K-OTC — | `scrt_grp_cls_code` (ST, EF, RT, DR, SW, …), `etp_prod_cls_code`, `prst_cls_code` — H; undocumented values `EN`, `PF` and others observed — O | 9-byte short code, 12-char standard code, 40-byte Korean name; no English name — H+C+O | **yes** — O (6-char mixed in `ST`, `EF`, `RT`, `PF`; 7- and 9-char codes in other groups) | 기준가, lot units, 거래정지, 정리매매, 관리, 시장경고, listing date, par value, listed shares (천주) — H; no tick size, no delisting date | — | not documented; one observation of HTTP `Last-Modified` (§2.6) — O; publisher MCP client refreshes once per calendar day — C |
| Kiwoom REST | REST `POST /api/dostk/stkinfo` `ka10099` (by `mrkt_tp`), `ka10100` (one code); `cont-yn`/`next-key` — F+E | 16 `mrkt_tp` codes incl. 코스피, 코스닥, 코넥스, K-OTC, 금현물 — F; response `marketCode`/`marketName` without code list — F | by request `mrkt_tp` only (ETF, ETN ×3, ELW, 리츠, 인프라, 뮤추얼, 신주인수권 …) — F; no preferred/SPAC field | `code` "단축코드" only; no standard code; no English name — F | not documented for these routes; other routes use `A`/`J`/`Q` + 6 digits — F | `listCount` (1주), `regDay`, `lastPrice`, free-text `state`/`auditInfo`, `orderWarning` codes — F; no tick, lot or delisting | `nxtEnable` "Y: 가능" — F | not documented |
| LS | REST `POST /stock/etc` `t8436` (`gubun` 0/1/2; also `t8430`) and `POST /stock/market-data` `t9945`; `tr_cont`/`tr_cont_key` headers, whether the master pages is not documented; 2 TPS — F+E | KOSPI/KOSDAQ only; KONEX — | t8436 `etfgubun` (ETF/ETN), `bu12gubun` (REIT, DR, fund, infra, foreign ETF …), `spac_gubun` — F; preferred — | `shcode` String 6 / `expcode` String 12 / `hname` (20 or 40); no English name — F+E | not shown — | t8430/t8436 lot `memedan`, `recprice`, `jnilclose`, upper/lower limit — F+E; no tick, listing date or halt | t9945 `nxt_chk` 1/0 (absent from the example) — F | not documented |
| DB | REST `POST /api/v1/quote/kr-stock/inquiry/stock-ticker` `JCODES` (`J`/`NJ`/`UJ`/`E`/`EN`); `cont_yn`/`cont_key`; 3 TPS — F+E+C | `MrktClsCode` "1: 코스닥 / 4: 코스피", **contradicted by the example**; `MrktClsName` incl. 코넥스 — F vs E | ETF/ETN only (selector, `MrktClsName`); preferred/REIT/SPAC — | `Iscd` (length 9) / `StndIscd` 12 / `KorIsnm` 40; no English name — F+E | **yes** — E (`0000D0`) | none in the master — | venue selector `NJ`/`UJ` only; no per-row flag — F | not documented |
| Toss | REST `GET /api/v1/stocks/all?market=` (no paging, `STOCK_ALL` 1/s) + `GET /api/v1/stocks?symbols=` ≤200 (`STOCK` 5/s) — F | `KOSPI`/`KOSDAQ`/`KR_ETC` (undefined) + US; KONEX — | `securityType` (9 values) + `isCommonShare`; ELW/SPAC — — F | `symbol` / `isinCode` / `name`; `englishName` on the detail route only — F | **yes**, documented "숫자 또는 영문·숫자 조합" (`0101N0`) — F+E | `listDate`, `delistDate`, KRX/NXT halt, liquidation, `sharesOutstanding` (issued) — F; tick/lot not in the master | `nxtSupported` (detail route) — F | "일 배치로 갱신", cache daily recommended; no as-of field — F |
| Meritz | file: `openapi.imeritz.com/stock-info/download/{kospi,kosdaq}` → `mts_*_code.mst` (+ `all` zip); "전체 종목 조회 API는 제공되지 않으며" — P; fixed-width bytes, encoding undocumented — O | KOSPI, KOSDAQ files (+ overseas); KONEX — — P | not documented (column spec missing); FAQ order-code prefixes A/F/J — P | not documented; ISIN-shaped bytes 9–20 and a CP949 name region observed (inference) — O | **yes** — O (both files) | not in the master; per-symbol REST `ohhts_1001_001r` has tick, lot, halt, limits, listed shares — F (REST) | — | "매 영업일 자동으로 갱신"; as-of only on the HTML page; no `Last-Modified` — P+O |

## 2. KIS (한국투자증권)

### 2.1 Pinned sources

All Git sources are in
[`koreainvestment/open-trading-api@3a9be59a`](https://github.com/koreainvestment/open-trading-api/tree/3a9be59a3ed8745720dc3aa9d584bdf3b7830362).
The full SHA is `3a9be59a3ed8745720dc3aa9d584bdf3b7830362` and the commit is
dated 2026-10-28T00:26:05+09:00 (the same pin as the candle audit). Paths
are relative to the repository root; `…/stocks_info/` stands for
`stocks_info/`.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| K1 | [`stocks_info/kis_kospi_code_mst.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/stocks_info/kis_kospi_code_mst.py) | `989278b7850d1899aa87db544f8d4a08404831f2` | KOSPI URL, TLS handling, encoding, parse widths and column names |
| K2 | [`stocks_info/kis_kosdaq_code_mst.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/stocks_info/kis_kosdaq_code_mst.py) | `9d04b1d6f6ab31b9b9d9e0014f43690c1571c2c9` | KOSDAQ equivalent |
| K3 | [`stocks_info/kis_konex_code_mst.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/stocks_info/kis_konex_code_mst.py) | `96439073d55b1ada544e33c66c5981a74fa3e4a4` | KONEX equivalent |
| K4 | [`stocks_info/종목마스터정보(코스피).h`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%BD%94%EC%8A%A4%ED%94%BC%29.h) | `61692a9c810c45748d48b3b51427da4350888967` | KOSPI record layout `ST_KSP_CODE` with code lists |
| K5 | [`stocks_info/종목마스터정보(코스닥).h`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%BD%94%EC%8A%A4%EB%8B%A5%29.h) | `6a58359f5045ea2a00371c8acc61ccbcc5cbf721` | KOSDAQ record layout `ST_KSQ_CODE` |
| K6 | [`stocks_info/종목마스터정보(코넥스).h`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/stocks_info/%EC%A2%85%EB%AA%A9%EB%A7%88%EC%8A%A4%ED%84%B0%EC%A0%95%EB%B3%B4%28%EC%BD%94%EB%84%A5%EC%8A%A4%29.h) | `9c816e536b6388b0a2da44601f965ed22e2b5e49` | KONEX record layout `ST_KNX_CODE` |
| K7 | [`backtester/scripts/download_master.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/backtester/scripts/download_master.py) | `6770e7c0db5a2fef4c34f2bf73eb80b1c48874f6` | Publisher client code: "인증 없이 공개 URL", byte-based layout note |
| K8 | [`MCP/Kis Trading MCP/module/plugin/master_file.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/MCP/Kis%20Trading%20MCP/module/plugin/master_file.py) | `a45f2bfa8ff7766f767341e9a0a8fae4cbc080d0` | Publisher client code: URL registry, refresh policy, TLS handling |
| K9 | [`README.md`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/README.md) | `182887151f1fb07e5789a029292ac3e43d3ba9bd` | Repo notes: disclaimer (L8–10), `stocks_info/` "종목정보파일 참고 데이터" (L100) |

**Downloaded file (aggregate observation only):**

| Item | Value |
| --- | --- |
| URL | `https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip` (the K1 L16 URL) |
| Retrieved | 2026-11-05T07:29:11Z, one unauthenticated `GET`, TLS verification **on**, through this session's egress proxy |
| HTTP | `200`, `content-type: application/zip`, `content-length: 119846`, `last-modified: Thu, 05 Nov 2026 01:55:03 GMT` |
| Zip | 119,846 bytes, sha256 `a954a927a16b4f1203744a745d8f3aeb5076b36c028cfe3eb93d69ee3a270074` |
| Member | one member `kospi_code.mst`, 742,441 bytes, deflate, zip timestamp 2026-11-05 07:35:04 (zip time has no zone), sha256 `96bb6d1facbcc1b60d7b20f7af29916db305c6274b7304361660beb0c9c1eff0` |

The KOSDAQ and KONEX files were **not** downloaded.

**Missing evidence:**

- No KIS developer-portal page describing the master files was retrieved.
- `SZ_SHRNCODE`, `SZ_STNDCODE` and `SZ_KORNAME` (K4–K6 L6–8) are not
  defined in any pinned file.
- No update schedule, as-of field, NXT master, K-OTC master or
  redistribution statement was found in K1–K9.
- The TLS verification observed above was against the session proxy's CA.
  The origin's own certificate chain was **not** examined.

### 2.2 Delivery

| Concern | Value (verbatim where possible) | Source | Evidence |
| --- | --- | --- | --- |
| Mechanism | static file download, no REST route. K8 L52: `"auth": []  # 인증은 마스터파일 불필요`; K7 L10: "인증 없이 공개 URL에서 다운로드합니다." | K7, K8 | publisher client code |
| URLs | `https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip` (K1 L16), `…/kosdaq_code.mst.zip` (K2 L17), `…/konex_code.mst.zip` (K3 L100); same three in K8 L59, L68, L77. ELW: `…/elw_code.mst.zip` (K8 L237) | K1–K3, K8 | publisher example |
| Host | `new.real.download.dws.co.kr`. This is **not** a KIS API origin (`openapi.koreainvestment.com`). **Inference:** a download host the publisher uses; ownership not documented. | K1–K3 | publisher example |
| Method / scheme | HTTPS `GET` (`urllib.request.urlretrieve`, K1 L16; `requests.get`, K8 L593) | K1, K8 | publisher example |
| **TLS** | K1 L14, K2 L15, K3 L14: `ssl._create_default_https_context = ssl._create_unverified_context`. K8 L590–591 does the same with the comment "SSL 컨텍스트 설정 (한국투자증권 서버용)". **Unsafe; must not be copied.** K7 L37 uses `urllib.request.urlopen(url, timeout=60)` without disabling verification. | K1–K3, K7, K8 | publisher example / client code |
| Compression | zip; K1 L21–22 extracts all members. Observed: one member `kospi_code.mst` | K1, file | publisher example + file observation |
| Encoding | K1 L35–38 and K2 L35–38 open as `cp949`; K7 L54: "EUC-KR 인코딩". K8 L669 tries `cp949`, `euc-kr`, `utf-8`, … in turn. Observed: all 2,569 records decode as cp949 | K1, K2, K7, K8, file | publisher example + file observation |
| Line terminator | not documented. Observed: LF only, no CR, file ends with LF | file | file observation |
| Header row | none documented; K1 reads every line as data. Observed: every record has the same byte length | K1, file | publisher example + file observation |
| Record layout | fixed width. Prefix = short code (K1 L41 `row[0:9]`), standard code (L42 `row[9:21]`), Korean name (L43 `row[21:len(row)-228]`). Tail = fixed fields of K4 (227 bytes; K1 L45 `row[-228:]` includes the newline) | K1, K4 | publisher example + layout header |
| Tail widths | Sum of K4 field widths = 227 (70 fields); K5 = 221 (64 fields, K2 `row[-222:]`); K6 = 184 (38 fields, K3 `row[-184:]` after `strip()`). K1/K2 width lists match K4/K5 exactly. | K1–K6 | layout header |
| Byte vs character | K7 L54: "고정 폭 필드 (바이트 기준)" with name "21-60 (40바이트)" (L57). K1/K2 slice **decoded characters** from the end. Observed: every KOSPI record is 288 bytes = 9 + 12 + **40** + 227; name region 40 bytes in every record; no non-ASCII byte in the first 21 or last 227 bytes. | K1, K7, file | client code + file observation |
| Size | KOSPI: 119,846-byte zip, 742,441-byte member, 2,569 records (2026-11-05 copy) | file | file observation |
| Pagination | n/a (whole-file download) | — | — |

**Inference:** K1/K2 character slicing gives the same result as byte slicing
only because the prefix and tail are ASCII. A KTradeLink parser should slice
**bytes** at the K4 widths and decode only the name region (G-F2).

### 2.3 Coverage: markets, venues, instrument types

| Market / type | Covered? | Discriminating field + documented codes | Source | Evidence |
| --- | --- | --- | --- | --- |
| 유가증권시장 (KOSPI market) | `kospi_code.mst` | file identity; K4 L2 "코스피 종목 코드 파일 구조" | K1, K4 | layout header |
| KOSDAQ | `kosdaq_code.mst` | file identity; K5 L2 | K2, K5 | layout header |
| KONEX | `konex_code.mst` | file identity; `scrt_grp_cls_code` "KN:코넥스" (K6 L10) | K3, K6 | layout header |
| NXT | **not found** | no NXT file and no NXT field in K4–K6 | — | not found |
| K-OTC | **not found** | — | — | not found |
| Security group | yes | `scrt_grp_cls_code[2]` "ST:주권 MF:증권투자회사 RT:부동산투자회사 SC:선박투자회사 IF:사회간접자본투융자회사 DR:주식예탁증서 EW:ELW EF:ETF SW:신주인수권증권 SR:신주인수권증서 BC:수익증권 FE:해외ETF FS:외국주권" (K4 L9–14; K5 L9–14 identical) | K4, K5 | layout header |
| ETF / ETN | yes | `etp_prod_cls_code[1]` KOSPI: "0:해당없음 1:투자회사형 2:수익증권형 3:ETN 4:손실제한ETN 5:상장형수익증권" (K4 L31–33); KOSDAQ: "0:해당없음 1:투자회사형 2:수익증권형 3:ETN 4:손실제한ETN" (K5 L23–25) | K4, K5 | layout header |
| Preferred | yes | `prst_cls_code[1]` "0:해당없음(보통주) 1:구형우선주 2:신형우선주" (K4 L82–83; K5 L73–74; K6 L41–42) | K4–K6 | layout header |
| SPAC | yes | `etpr_undt_objt_co_yn[1]` "기업인수목적회사여부" (K4 L40; K5 L31); not in K6 | K4, K5 | layout header |
| REIT | yes | `scrt_grp_cls_code` `RT` | K4 | layout header |
| ELW | separate file | `elw_code.mst.zip` (K8 L237; not analysed here). In the KOSPI file `elw_pblc_yn` "ELW 발행여부 (Y/N)" (K4 L34). **Inference:** this flags an ELW *underlying*, not an ELW row. | K4, K8 | layout header / client code |
| Index membership | flags | KOSPI100/50/200 sector, KRX100/300, KOSDAQ150, `kospi_issu_yn` "KOSPI여부" (K4 L87) — meaning of "KOSPI여부" not documented | K4, K5 | layout header |

**File observations (KOSPI copy of 2026-11-05; value sets only):**

- `scrt_grp_cls_code` values present: `BC`, `DR`, `EF`, `EN`, `FS`, `IF`,
  `MF`, `PF`, `RT`, `SR`, `ST`, `SW`. **`EN` and `PF` are not in the K4
  list.** **Inference:** `EN` holds ETNs (all `EN` rows have the 7-character
  short-code shape below); `PF` is unknown.
- `etp_prod_cls_code` values present: space, `2`, `3`, `4`, `5`, `8`, `9`.
  **Space, `8` and `9` are undocumented**, and the documented `0` does not
  occur.
- `prst_cls_code` values present: `0`, `1`, `2`, `9`. **`9` is
  undocumented.**
- The "KOSPI" file therefore lists ETFs, ETNs, 수익증권 and warrants as well
  as shares. It is a market-segment file, not a common-stock list.
- `kospi_issu_yn` = `Y` on fewer rows than `scrt_grp_cls_code` = `ST`.
  **Inference:** it is an index-membership flag, not "listed on KOSPI".

### 2.4 Identifier fields

| Concern | Field | Documented type/length/format | Source | Evidence |
| --- | --- | --- | --- | --- |
| Short code | `mksc_shrn_iscd` "단축코드" | width `SZ_SHRNCODE` (undefined); K1 L41 slices 9 and `rstrip()`s | K1, K4 L6 | layout header + publisher example |
| Standard code | `stnd_iscd` "표준코드" | width `SZ_STNDCODE` (undefined); K1 L42 slices 12 | K1, K4 L7 | layout header + publisher example |
| Korean name | `hts_kor_isnm` "한글종목명" | width `SZ_KORNAME` (undefined); K7 L57 "40바이트"; observed 40 bytes, space-padded **Inference** from K1 `strip()` | K4 L8, K7 | layout header + client code + file observation |
| English name | — | not in K4–K6 | — | not found |
| Venue-qualified id | — | none in the file; venue is chosen by the REST field `FID_COND_MRKT_DIV_CODE` (candle audit §2.3) | — | not found |

**Alphanumeric short codes — yes (file observation, KOSPI copy):**

- The short-code field is 9 bytes wide. Shapes present, by group:
  - 6 ASCII digits + 3 spaces: `ST`, `EF`, `RT`, `DR`, `FS`, `IF`, `MF`.
  - 6 characters mixing digits and **one or more uppercase letters** + 3
    spaces: present in `ST` (both `prst_cls_code` `0` common shares and
    preferred classes), `EF`, `RT` and `PF`.
  - 7 characters = one uppercase letter + 6 digits: all `EN` rows.
  - 9 characters (letters and digits): all `BC`, `SR` and `SW` rows.
- Standard codes are 12 characters starting with two or three letters;
  some contain further letters. **Inference:** ISIN-like; no check-digit
  rule is documented.
- K7 L70–75 truncates codes longer than 6 to their last 6 characters and
  keeps only all-digit codes: "숫자로만 이루어진 코드만". That publisher
  client code silently drops alphanumeric instruments. **Must not be
  copied** (G-I2).
- Consequence for the v0.1 spec (§3: "exactly six ASCII digits"): at least
  some KRX common shares in the KIS master are not representable (G-I1).

### 2.5 Trading attributes (as documented in K4; K5/K6 identical unless noted)

| Attribute | Field + documented meaning/codes | Source | Evidence |
| --- | --- | --- | --- |
| Tick size / price unit | **not in the layout** | — | not found |
| Lot size | `frml_mrkt_deal_qty_unit[5]` "정규 시장 매매 수량 단위", `ovtm_mrkt_deal_qty_unit[5]` "시간외 시장 매매 수량 단위" | K4 L54–55 | layout header |
| Base price | `stck_sdpr[9]` "주식 기준가" (unit not documented) | K4 L53 | layout header |
| Listing date | `stck_lstn_date[8]` "주식 상장 일자" (format not documented; observed 8 digits in every record) | K4 L77 | layout header + file observation |
| Delisting date | **not in the layout** | — | not found |
| Trading halt | `trht_yn[1]` "거래정지 여부" | K4 L56 | layout header |
| Liquidation trading | `sltr_yn[1]` "정리매매 여부" | K4 L57 | layout header |
| Administrative issue | `mang_issu_yn[1]` "관리 종목 여부" | K4 L58 | layout header |
| Market warning | `mrkt_alrm_cls_code[2]` "00:해당없음 01:투자주의 02:투자경고 03:투자위험"; `mrkt_alrm_risk_adnt_yn[1]` "시장 경고위험 예고 여부" | K4 L59–61 | layout header |
| Short-term overheating | `short_over_cls_code[1]` "0:해당없음 1:지정예고 2:지정 3:지정연장(해제연기)" | K4 L43–44 | layout header |
| KOSDAQ caution | `invt_alrm_yn[1]` "(코스닥)투자주의환기종목여부" (KOSDAQ only) | K5 L38 | layout header |
| Other flags | 불성실공시, 우회상장, 락구분, 액면가 변경, 증자, 증거금 비율, 신용가능/기간, 공매도과열, 이상급등, 담보대출/대주 가능 | K4 L62–98 | layout header |
| NXT eligibility | **not in the layout** | — | not found |
| Par value | `stck_fcam[12]` "주식 액면가" (unit not documented) | K4 L76 | layout header |
| Listed shares | `lstn_stcn[15]` "상장 주수(천)" — **thousands of shares** | K4 L78 | layout header |
| Financials | 매출액, 영업이익, 경상이익, 당기순이익, ROE, `base_date[8]` "기준년월", 시가총액 (억) | K4 L88–94 | layout header |

Numeric fields are fixed-width text. Their sign, padding and units are
**not documented**, except where the comment names a unit.

### 2.6 Freshness and staleness

- **Update cadence:** not documented in K1–K9.
- **Publisher client policy:** K8 L475–478 re-downloads when the stored
  update time's date is before today's local date
  (`last_update.date() < datetime.now().date()`). This is client code, not
  a publication schedule.
- **As-of field:** none in the layout. `base_date[8]` "기준년월" is not a
  file as-of date: in the 2026-11-05 copy it is blank in most records and
  takes several different 8-digit values elsewhere. **Inference:** a
  financial-statement base date.
- **Observed once:** HTTP `Last-Modified: Thu, 05 Nov 2026 01:55:03 GMT`; zip
  member timestamp 2026-11-05 07:35:04 (no zone). These do not agree
  without a zone assumption, and one observation is not a cadence.
- **Staleness detection:** not documented. **Inference:** a client could
  record `Last-Modified`/`ETag`, size and sha256 per download; the meaning
  of those headers for this host is undocumented (G-C2).
- `전일 거래량` (`prdy_vol`) and `전일기준 시가총액` suggest a once-per-day
  snapshot. **Inference** only.

### 2.7 Data rights and redistribution

- Not documented in the pinned sources. K9 L8–10 covers sample code only:
  "샘플 코드는 … 참고용으로 제공되고 있습니다." and "샘플 코드를 활용하여 제작한
  고객님의 프로그램으로 인한 손해에 대해서는 당사에서 책임지지 않습니다."
- The repository root has no licence file at the pin.
- Public, unauthenticated availability (K7 L10, K8 L52) is **not** a grant
  of storage or redistribution rights.

### 2.8 Contradictions and inferences

1. **Undocumented code values.** The file contains `scrt_grp_cls_code`
   `EN`/`PF`, `etp_prod_cls_code` space/`8`/`9` and `prst_cls_code` `9`,
   none of which K4 lists. A decoder must keep unknown codes as unknown
   (`UNKNOWN(<raw>)`), never map them to a default type (G-T2).
2. **Layout widths undefined.** K4–K6 leave the three prefix widths
   symbolic. K1 (9/12), K7 (9/12/40) and the observed 288-byte records
   agree for KOSPI only. KOSDAQ and KONEX prefix widths are unobserved.
3. **Byte vs character slicing.** K7 is byte-based; K1/K2 slice characters.
   Equivalent today only because prefix and tail are ASCII (§2.2).
4. **KONEX parser fragility.** K3 L32 calls `row.strip()` before slicing
   from the end. **Inference:** a record whose last fields are spaces would
   shift every tail field. The KONEX file was not downloaded.
5. **TLS.** Three `stocks_info` scripts and K8 disable verification; K7 does
   not. The publisher comment in K8 L590 implies a certificate problem, but
   none was observed here through the proxy. The origin chain is
   unverified (G-S1).
6. **ETN typing.** K4 lists no ETN group code, yet ETNs appear under `EN`
   with `etp_prod_cls_code` `3`/`4`. Typing must use both fields and must
   not infer type from code shape alone.
7. **`base_date` "기준년월"** is 8 characters wide, and observed values are
   8 digits, not `YYYYMM`.
8. **Listed-share unit** is thousands (K4 L78), unlike Kiwoom's 1주 (§3.5).

## 3. Kiwoom REST (키움증권)

### 3.1 Pinned sources and re-pin

All sources are in
[`Kiwoom-Securities/Kiwoom-REST-API@c7a3d254`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/tree/c7a3d25449ed4b4238bef378780c41103c67b9e9).
The full SHA is `c7a3d25449ed4b4238bef378780c41103c67b9e9`, commit dated
2026-09-15T15:12:16+09:00. In the links, `…/종목정보/` stands for
`examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/`.

**Re-pin from `953e5dbf`.** The earlier audits pinned
`953e5dbff123f437ab4d11a78a95191a685eb51f`. On 2026-11-05:

- `git ls-remote` lists only `HEAD` and `refs/heads/main`, both
  `c7a3d254…`. No branch or tag reaches `953e5dbf`.
- `953e5dbf` was still fetchable from GitHub by SHA.
- Both commits have **tree `4eb7d5497f4155ace73d8d37a03f3dc18abbe6fa`**, the
  same author/committer dates (2026-09-15T15:12:16+09:00) and message, and
  different parents (`234560d2…` vs `66bebb00…`).
- Identical trees mean every file and blob SHA is identical. The blobs
  pinned by the candle audit (`kiwoom_api_spec.json` `15ee3a91…`, postman
  `88138bd9…`, `client.py` `52d915c9…`) are therefore valid at
  `c7a3d254`. **Inference:** the publisher rewrote history below the commit.

| # | Path | Git blob | Used for |
| --- | --- | --- | --- |
| W1 | [`kiwoom/_data/kiwoom_api_spec.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/_data/kiwoom_api_spec.json) | `15ee3a916d266a0e4c0a4f77e286e4ec9017ca84` | **Field tables**: `apis["종목정보 리스트(ka10099)"]`, `apis["종목정보 조회(ka10100)"]`; prefixed-code fields of other routes |
| W2 | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/postman/kiwoom-openapi.postman_collection.json) | `88138bd9be24a6c39b2c8151fa6e465ce12319ce` | Field tables under `PRD/국내주식/종목정보/…` and `MOCK(모의투자)/국내주식/종목정보/…` |
| W3 | [`examples/국내주식/종목정보/list_domestic_stocks.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/list_domestic_stocks.py) | `3197c003b534dc9804fc83d41805055b9b74b783` | `ka10099` example and paging loop |
| W4 | [`…/종목정보/get_domestic_stock_detail.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_detail.py) | `b112ec61821a15e4c8ffe447a140a73dfbbba737` | `ka10100` example |
| W5 | [`kiwoom/core/client.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/kiwoom/core/client.py) | `52d915c9e2f38f21885efbc428d3b50593a452c9` | Publisher client code: headers, `return_code`, continuation |
| W6 | [`LICENSE.md`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/c7a3d25449ed4b4238bef378780c41103c67b9e9/LICENSE.md) | `556ae8b60ece2439d691cebc4df4676ae9e6fbdd` | Software/documentation licence (§3.7) |

W1 and W2 carry the same field wording for both routes. Differences are
noted in §3.8.

**Missing evidence:** page size, row order, update cadence, the response
`marketCode` code list, the `state`/`auditInfo` vocabularies and any data
redistribution terms.

### 3.2 Delivery

| Concern | `ka10099` 종목정보 리스트 | `ka10100` 종목정보 조회 | Evidence |
| --- | --- | --- | --- |
| Purpose (verbatim) | "시장을 선택하여 종목 리스트를 조회합니다." | "종목 코드로 종목 정보를 조회합니다." | field table |
| Method / path | `POST /api/dostk/stkinfo` | `POST /api/dostk/stkinfo` (same path; selected by `api-id`) | field table |
| Origins | "운영 도메인" `https://api.kiwoom.com`, "모의투자 도메인" `https://mockapi.kiwoom.com` (W1 meta). W2 lists both routes under `PRD` and `MOCK(모의투자)`. | same | field table |
| Format | `JSON`, `Content-Type` `application/json;charset=UTF-8` | same | field table |
| Required request headers | `api-id` (Y), `authorization` (Y, "Bearer" token) | same | field table |
| Optional request headers | `cont-yn` (len 1), `next-key` (len 50) | same | field table |
| Request body | `mrkt_tp` String(2) Y "시장구분" (§3.3) | `stk_cd` String(6) Y "종목코드 6자리" | field table |
| Response array | `list` "종목리스트" LIST | none; fields at top level | field table + example |
| Envelope | `return_code` (example `0`, JSON number), `return_msg`; not in the field table. W5 L104: "키움은 업무 오류도 HTTP 200으로 내려보내고 실패 여부는 본문 return_code에만 담는다." | same | example + client code |
| Continuation | response headers `cont-yn` "다음 데이터가 있을시 Y값 전달", `next-key` "다음 데이터가 있을시 다음 키값 전달" | headers listed, but a single-code lookup | field table |
| Page size | not documented | n/a | not found |
| Auth needed | yes (`authorization` required). Unlike KIS, the master is **not** public. | yes | field table |

**Publisher example paging (W3):** `MAX_PAGES = 10 # 최대 조회 페이지 수`
(L20), `REQUEST_DELAY_SECONDS = 0.2` (L21), and a loop that stops at
`MAX_PAGES` even when `cont-yn` is still `Y` (L139–172). That is client code.
Copying it would silently truncate the master (G-C3).

### 3.3 Coverage: markets, venues, instrument types

`mrkt_tp` (W1 `ka10099` request body; W2 identical; W3 L90–105 identical),
verbatim: "0 : 코스피, 10 : 코스닥, 30 : K-OTC, 50 : 코넥스, 60 : ETN, 70 :
손실제한 ETN, 80 : 금현물, 90 : 변동성 ETN, 2 : 인프라투융자, 3 : ELW, 4 :
뮤추얼펀드, 5 : 신주인수권, 6 : 리츠종목, 7 : 신주인수권증서, 8 : ETF, 9 :
하이일드펀드".

| Market / type | Covered? | Discriminating field + documented codes | Evidence |
| --- | --- | --- | --- |
| KOSPI / KOSDAQ / KONEX | yes | request `mrkt_tp` `0` / `10` / `50` | field table |
| K-OTC | yes — **not a KRX market** | `mrkt_tp` `30` | field table |
| 금현물 (gold spot) | yes — not an equity | `mrkt_tp` `80` | field table |
| ETF / ETN / 손실제한 ETN / 변동성 ETN | yes | `mrkt_tp` `8` / `60` / `70` / `90` | field table |
| ELW, 신주인수권, 신주인수권증서, 리츠, 인프라투융자, 뮤추얼펀드, 하이일드펀드 | yes | `mrkt_tp` `3`, `5`, `7`, `6`, `2`, `4`, `9` | field table |
| NXT | no market code; per-row flag `nxtEnable` (§3.5) | — | field table |
| Preferred shares | **no field** | — | not found |
| SPAC | **no field or market code** | — | not found |
| Foreign companies (KOSDAQ) | `companyClassName` "회사분류" "코스닥만 존재함"; values not listed (example: "외국기업") | — | field table + example |
| Response market | `marketCode` "시장구분코드", `marketName` "시장명": **no code list documented** | — | field table |

- Whether a code can appear under more than one `mrkt_tp` (for example an
  ETF under both `0` and `8`) is **not documented**.
- The `ka10100` example returns `marketCode` `"0"` with `marketName`
  "거래소", while the `mrkt_tp` label for `0` is "코스피". The `ka10099`
  example returns `marketCode` `"10"` with "코스닥". **Inference:** response
  `marketCode` reuses the `mrkt_tp` numbering. Not documented.

### 3.4 Identifier fields

| Concern | Field | Documented type/length/format | Evidence |
| --- | --- | --- | --- |
| Short code | `code` "종목코드" "단축코드" | String, length `20` (`ka10099`) / blank (`ka10100`); format not documented | field table |
| Request code (`ka10100`) | `stk_cd` | String(6) "종목코드 6자리" — no `_NX`/`_AL` suffix | field table |
| Standard code (ISIN-like) | — | none in either route | not found |
| Korean name | `name` "종목명" | String(40) | field table |
| English name | — | none | not found |
| Venue-qualified native id | — | none in these routes. Chart/quote routes use `stk_cd` "KRX:039490,NXT:039490_NX,SOR:039490_AL" (candle audit §3.3) | field table (other routes) |

**Alphanumeric short codes:** not documented for `ka10099`/`ka10100`. The
examples show only `005930`. Elsewhere in W1, nine routes (`ka10172`,
`ka10173`, `kt00004`, `kt00005`, `kt00007`, `kt00008`, `kt00009`,
`kt00015`, `kt00018`) describe their code field as "접두어 1자리 + 종목코드
6자리, 접두어(A: 주식 / J: ELW / Q: ETN)". So Kiwoom uses at least three
identifier forms: plain 6-character, venue-suffixed (`_NX`, `_AL`) and
prefixed (`A`/`J`/`Q`). A canonical identifier must strip none of these
implicitly (G-I3).

### 3.5 Trading attributes (W1 field tables)

| Attribute | Field + documented meaning/codes | Evidence |
| --- | --- | --- |
| Tick size | **not in either route** | not found |
| Lot size | **not in either route** | not found |
| Listing date | `regDay` "상장일" "YYYYMMDD" | field table |
| Delisting date | — | not found |
| Previous close | `lastPrice` "전일종가" "단위: 원, 좌측 0-padding 처리된 부호 포함 8자리 숫자" | field table |
| Listed shares | `listCount` "상장주식수" "단위: 1주, 좌측 0-padding 처리된 부호 포함 16자리 숫자" | field table |
| Audit status | `auditInfo` "감리구분": no value list. Examples: "정상", "투자주의환기종목" | field table + example |
| Instrument state | `state` "종목상태": no value list. Examples: "관리종목", "증거금100%", "증거금20%\|담보대출\|신용가능" (pipe-joined) | field table + example |
| Investment warning | `orderWarning` "투자유의종목여부": "0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달" (verbatim, including the unclosed parenthesis) | field table |
| Trading halt | no dedicated field. **Inference:** may appear in free-text `state`; not documented | not found |
| NXT eligibility | `nxtEnable` "NXT가능여부" "Y: 가능". Other values not documented | field table |
| Sector / size | `upName` "업종명", `upSizeName` "회사크기분류" (example "대형주") | field table + example |
| Par value | — | not found |

### 3.6 Freshness and staleness

- Update cadence: not documented.
- As-of field: none. `lastPrice` "전일종가" implies a previous-session
  reference. **Inference** only.
- Staleness detection: not documented.

### 3.7 Data rights and redistribution

- No statement about master/market-data storage or redistribution was found
  in W1–W5.
- W6 governs "본 소프트웨어 및 관련 문서 파일" (its article 1), limits use
  "키움증권 OpenAPI 서비스를 이용하기 위한 목적에 한하여" (article 2), and
  forbids, "회사의 사전 서면 동의 없이", "본 소프트웨어의 복제, 배포, 전송,
  출판" and "수정, 2차적 저작물 작성" (article 3).
- Consequence: KTradeLink cites W1/W2 field names and short wording only.
  It must not vendor Kiwoom code, the spec JSON or the postman collection
  (G-R2). W6 says nothing about the returned data.

### 3.8 Contradictions and inferences

1. **Synthetic list example.** The `ka10099` request example sends
   `mrkt_tp` `"0"` (코스피), yet every one of its five rows has
   `marketCode` `"10"` / "코스닥" and the same `code`/`name` with different
   listing dates and share counts. The example is not a usable fixture.
2. **Field lengths differ between the routes.** `ka10099` gives `20` for
   nearly every field. `ka10100` gives `listCount` 16, `regDay` 8,
   `lastPrice` 8 and blanks elsewhere. Lengths must not drive parsing.
3. **Body vs query.** W1 documents `mrkt_tp`/`stk_cd` as body fields, and
   W3/W4 send them in the JSON body. W2 sends them **both** as URL query
   (`{{PRD}}/api/dostk/stkinfo?mrkt_tp=0`) and body. Only the body form is
   field-table-backed.
4. **`orderWarning` gaps.** No code for 투자주의 or 투자경고 on non-ETF
   rows. "5: 투자경과" is verbatim. **Inference:** a typo for 투자경고. It
   must not be mapped as such without evidence (G-T3).
5. **Signed counts.** `listCount` and `lastPrice` are documented as "부호
   포함" zero-padded strings, but the examples are unsigned. The sign
   meaning is not documented.
6. **Label mismatch.** `mrkt_tp` `0` = "코스피" vs example `marketName`
   "거래소" (§3.3).
7. **W3 marks `NXT가능여부` as a numeric display column (L48–51).** That is
   cosmetic client code and does not change the documented `Y` value.

## 4. LS Securities (LS증권)

### 4.1 Pinned sources

All LS sources are public portal resources on `https://openapi.ls-sec.co.kr`
with **no immutable revision**. Each sha256 prefix identifies only the copy
retrieved at the stated UTC time on 2026-11-05. Retrieval window:
07:20:47Z–07:22:49Z.

- The guide detail endpoints return JSON. The path is the TR id from the
  apiservice page's `data-tr` attribute; `api=` is the parent sub-menu id
  (`data-api`). This is the same method the candle audit used.
- `[주식] 기타` (`/stock/etc`) sub-menu id: `316495d3-6109-45a6-baaf-9e8a0261f30a`.
- `[주식] 시세` (`/stock/market-data`) sub-menu id: `54a99b02-dbba-4057-8756-9ac759c9a2ed`.

| # | Path / URL | sha256 prefix (+ publisher revision), retrieval UTC | Used for |
| --- | --- | --- | --- |
| L1 | https://openapi.ls-sec.co.kr/api/apis/public/tr-guides.json | `9aaca437f1925115`, 07:20:47–58Z, 2,792,313 bytes; publisher `"version" : "20261026021444748"`. The same bytes as the capability-inventory copy (06:53:57Z) and the candle-audit copy (06:43:57Z). | TR discovery; field tables for t8430, t8436, t9945, t1403; `transactionPerSec`; REST server `https://openapi.ls-sec.co.kr:8080`; `defaults.fieldRequired: true` |
| L2 | https://openapi.ls-sec.co.kr/apiservice | `7869ee4196d7ee94`, 07:21:21Z. The page varies between requests. | `data-api` / `data-tr` ids (lines 603–609, 1035–1065 of the retrieved copy) |
| L3 | https://openapi.ls-sec.co.kr/guide/api/10b608pg-043k-l8qc-587y-3hz6xy0c1b7r?type=rest&api=316495d3-6109-45a6-baaf-9e8a0261f30a (t8436) | `efbc50d023d9e06b`, 07:21:32Z. The same bytes as the inventory copy (06:52Z). | `requestHeaderFields`, `requestBlocks`, `responseBlocks`, `codeSamples`, `responseExample` |
| L4 | `…/guide/api/ir3h1jd3-6q1q-lrz6-51wl-88u4t8748hre?type=rest&api=316495d3-…` (t8430) | `5b017d334785e9fd`, 07:21:34Z | same keys |
| L5 | `…/guide/api/u4hepin5-rfe4-3g3p-8yn3-7xko30x5hm5z?type=rest&api=54a99b02-dbba-4057-8756-9ac759c9a2ed` (t9945) | `47a2ce86b41d3379`, 07:21:35Z. The same bytes as the inventory copy. | same keys |
| L6 | `…/guide/api/1p7tu38d-jj3j-b2ic-s4sm-r3c08o27z7ij?type=rest&api=316495d3-…` (t1403, an auxiliary source) | `f383172d144bd86c`, 07:21:36Z | Listing-date source (§4.5) |
| L7 | https://openapi.ls-sec.co.kr/community-faq (302 → `/community/10000000-0000-0011-0000-000000000002`) | `f17898553e4237dc`, 07:22:23Z. The candle-audit copy at 06:46:24Z hashed `af701a0003ca34bf`, so the page varies. | FAQ row `data-id="17180a67-8a0e-44d2-ae2d-2b44a9efebb7"`, `data-title="종목검색은 어떻게 하나요?"` (lines 548–563) |
| L8 | https://openapi.ls-sec.co.kr/howto-use; `/about-openapi`; `/community-notice` (→ `/community/10000000-0000-0011-0000-000000000001`) | `64789b75a7a72062` 07:22:25Z; `89eb85b0bbd48d03` 07:22:27Z; `2e46566ce40586b4` 07:22:49Z | Data-rights and notice search only; nothing relevant found (§4.7) |

**Missing evidence:**

- There is no LS master **file** download. L1–L8 document only REST TRs.
- No integrated or NXT variant of the stock master exists.
  - L1 has `(통합)`/`(NXT)` names only for quote, chart and WebSocket TRs.
  - Examples: `t8450`, `t8451`–`t8453`, `t8454`, `NS3`, `US3`.
  - None of them lists symbols.
- The **terms of use** were not retrieved. L8 links them only through a
  footer popup (`data-footer-popup="LSFooterTerms"`).
- There is no public LS Git repository to pin. The publisher code is the
  `codeSamples` inside L3–L5.

### 4.2 Delivery

Three REST TRs list domestic stock symbols. **t8436** is the inventory's
route. **t9945** is the only LS route with an NXT flag. **t8430** is the
FAQ's route (§4.8 item 1).

| Concern | t8436 "주식종목조회 API용" | t8430 "주식종목조회" | t9945 "주식마스터조회API용" | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| Method + path | `POST /stock/etc` | `POST /stock/etc` | `POST /stock/market-data` | L1 group `path`; L3–L5 `httpMethod`, `accessUrl` | field table |
| Origin | `https://openapi.ls-sec.co.kr:8080` (L3–L5 `domain`) | same | same | L1 `servers[protocol=REST]`, L3–L5 | field table |
| Paper origin | L1 gives a `simulationUrl` only for `WEBSOCKET`. No REST paper origin is documented. | same | same | L1 `servers` | not found |
| `tr_cd` | `t8436` | `t8430` | `t9945` | L3–L5 `trCode`, `codeSamples.python` | field table, publisher example |
| Request headers (names) | `content-type`, `authorization`, `tr_cd`, `tr_cont`, `tr_cont_key`, `mac_address`; all `required: true` | same | same | L3–L5 `requestHeaderFields` | field table |
| `mac_address` | "법인인 경우 필수 세팅"; the code samples send `""` | same | same | L3–L5 | field table, publisher example |
| Body | `{"t8436InBlock": {"gubun": "1"}}` | `{"t8430InBlock": {"gubun": "1"}}` | `{"t9945InBlock": {"gubun": "1"}}` | L3–L5 `codeSamples.python` | publisher example |
| Selector | `gubun` String 1, "구분(0:전체1:코스피2:코스닥)" | same wording | `gubun` String 1, "구분(KSP:1KSD:2)". There is **no "all" code**. | L3–L5 `requestBlocks` | field table |
| Response array | `t8436OutBlock` "Object Array" | `t8430OutBlock` | `t9945OutBlock` | L1, L3–L5 `responseBlocks` | field table |
| Envelope / success | Root `rsp_cd`, `rsp_msg`. The example shows `"rsp_cd": "00000"`, `"rsp_msg": "정상적으로 조회가 완료되었습니다."`. These fields are not in the TR field table. | same | same | L3–L5 `responseExample` | publisher example only |
| Pagination | Request and response headers `tr_cont` "연속거래 여부 Y:연속○ N:연속×" and `tr_cont_key` String 18 "연속일 경우 그전에 내려온 연속키 값 올림". The InBlock has **no** body continuation field. Whether the list is ever split across pages is **not documented**. | same | same | L3–L5 `requestHeaderFields`, `responseHeaderFields`, `requestBlocks` | field table |
| Page size / row count | Not documented. Each example shows 2–3 rows, so the examples are excerpts. | same | same | L3–L5 | not found |
| Rate | `transactionPerSec` `"2"` | `"2"` | `"2"` | L1, L3–L5 | field table |

The L3–L5 detail `description` is the parent sub-menu's text, not the TR's:

- t8430 and t8436: "신용잔고 및 신규상장종목 등 종목별 기타정보를 확인할 수 있는 서비스입니다."
- t9945: "개별종목 현재가 및 기간별 시세 등 종목별 시세를 확인할 수 있습니다."

It says nothing about the master's content.

### 4.3 Coverage: markets, venues, instrument types

| Market / type | Covered? | Discriminating field + documented codes | Source | Evidence |
| --- | --- | --- | --- | --- |
| KOSPI | yes | Request `gubun` `1`. Response `gubun` "구분(1:코스피2:코스닥)" (t8430/t8436). t9945 has **no response market field**; the market is known only from the request `gubun` (`1` = KSP). | L3–L5 | field table, publisher example (`"gubun": "1"`) |
| KOSDAQ | yes | `gubun` `2` (all three TRs) | L3–L5 | field table |
| KONEX | **not documented** | No KONEX code appears in any master selector or response field. L1 names 코넥스 only in `t0424` (balance) and `SC0` (order event) code lists. | L1 | not found |
| NXT | Partly: as a **flag**, not a venue list | t9945 `nxt_chk` "NXT상장구분": "1:NXT 거래소 제공 / 0:NXT 거래소 미제공". t8430/t8436 have no NXT field. | L5, L1 | field table only (the field is absent from the example, §4.8 item 4) |
| ETF | yes | t8436 `etfgubun` "ETF구분(1:ETF2:ETN)" plus `bu12gubun` `08`. t8430 `etfgubun` "ETF구분(1:ETF)". t9945 `etfchk` "ETF구분" has **no documented codes**. | L3–L5 | field table; the t9945 example shows `"1"` on an ETF row |
| ETN | t8436 only | `etfgubun` `2`; `bu12gubun` `15` "ETN" | L3 | field table |
| ELW | **not in the stock masters** | Separate TRs: `t9942` "ELW마스터조회API용" and `t8431` "ELW종목조회" (`/stock/elw`, tps 2). Not inspected in detail. | L1 | field table (catalog listing only) |
| REIT | t8436 | `bu12gubun` `06` "Reits종목" | L3 | field table |
| SPAC | t8436 | `spac_gubun` "기업인수목적회사여부(Y/N)", description "Y or N" | L3 | field table |
| Preferred shares | **no discriminator** | None documented. The t8436 example row `005385` "현대차우" has `bu12gubun` `"01"` (주식). | L3 | publisher example |
| DR / mutual fund / ship / infra / foreign ETF / foreign original share | t8436 | `bu12gubun`: `03` "예탁증서(DR)", `04` "증권투자회사(뮤추얼펀드)", `10` "선박투자회사", `12` "인프라투융자회사", `13` "해외ETF", `14` "해외원주" | L3 | field table |
| Common stock | t8436 | `bu12gubun` `01` "주식" | L3 | field table |
| K-OTC, indices, futures | not in these TRs | Futures/options masters are separate (`t8401`, `t8433`, `t8435`, `t9943`, `t9944`, …) | L1 | out of scope |

The full t8436 `bu12gubun` code list is: `01`, `03`, `04`, `06`, `08`,
`10`, `12`, `13`, `14`, `15`. Codes `02`, `05`, `07`, `09` and `11` are
**not documented**.

### 4.4 Identifier fields

| Concern | Field | Documented type/length/format | Source | Evidence |
| --- | --- | --- | --- | --- |
| Short code | `shcode` "단축코드" | String 6 (all three TRs). Format beyond the length is not documented. | L3–L5 | field table |
| Standard code (12 chars) | `expcode` "확장코드" | String 12. The examples are ISIN-shaped, e.g. `KR7000020008`. | L3–L5 | field table, publisher example |
| Korean name | `hname` "종목명" | String **20** (t8430/t8436); String **40** (t9945) | L3–L5 | field table |
| English name | — | not documented in any of the three TRs | L1 | not found |
| Venue-qualified native id | — | none; NXT is a flag (`nxt_chk`), not an id | L5 | not found |

**Alphanumeric short codes:** not documented.

- `shcode` is declared String 6, which does not by itself exclude letters.
- Every `shcode` in the L3–L5 examples is six digits.
- **Inference:** if a listed code contains letters (§5.4 shows such codes
  exist on the KRX list), the master would carry it in this field. The
  current v0.1 rule is "exactly six ASCII digits" ([market-data spec §3](../specifications/market-data-v0.1-draft.md)).
  A `load_markets` built on it would then reject or drop those rows. LS
  evidence alone cannot settle this.

### 4.5 Trading attributes (only as documented)

| Attribute | Field + documented meaning/codes | Source | Evidence |
| --- | --- | --- | --- |
| Tick size | not documented in t8430/t8436/t9945 | L1 | not found |
| Lot size | t8430/t8436 `memedan` "주문수량단위" String 5; example `"00001"` | L3, L4 | field table, publisher example |
| Listing date | Not in the master TRs. A separate TR, `t1403` "신규상장종목조회", returns `date` "등록일" String 8 for listings in a `styymm`–`enyymm` "YYYYMM" range (`/stock/etc`, tps 1). Its example has an empty `t1403OutBlock1`. `t1102` (quote) has `listdate` "상장일". | L6, L1 | field table |
| Delisting date | not documented | — | not found |
| Trading halt | not in the master TRs | L1 | not found |
| Administrative issue | not in the master TRs | L1 | not found |
| Investment caution / warning | Not in the master TRs. The per-symbol quote `t1102` has `info5` "투자주의환기", `shterm_text` "단기과열/VI발동" and `nxt_shterm_text` "NXT단기과열/VI발동". These are not inspected here. | L1 | field table (t1102 only) |
| NXT eligibility | t9945 `nxt_chk`: "1:NXT 거래소 제공 / 0:NXT 거래소 미제공" | L5 | field table |
| Par value | not documented | — | not found |
| Listed shares | not in the master TRs (`t1102` `listing` "상장주식수(천)") | L1 | field table (t1102 only) |
| Base / reference price | t8430/t8436 `recprice` "기준가" Number 8; `jnilclose` "전일가" Number 8 | L3, L4 | field table |
| Upper / lower limit | t8430/t8436 `uplmtprice` "상한가", `dnlmtprice` "하한가", Number 8 | L3, L4 | field table |
| Other | `filler` (t8436 "filler(미사용)" String 32; t9945 String 4) | L3, L5 | field table |

The **venue** of `recprice`, `jnilclose`, `uplmtprice` and `dnlmtprice` (KRX
vs NXT) is not documented.

### 4.6 Freshness and staleness

- **Update cadence:** not documented.
- **As-of / base-date field:** none in any of the three OutBlocks. The
  request has no date input.
- **Staleness detection:** not documented.
  - **Inference:** t8430/t8436 carry same-day reference and limit prices.
    The list therefore reflects some trading-day state, but that day is not
    stated in the payload.

### 4.7 Data rights and redistribution

Not documented in the pinned sources. No redistribution statement was
found in L1–L8; the terms of use (footer popup `LSFooterTerms`) were not
retrieved.

### 4.8 Contradictions and inferences

1. **Which TR is "the" OPEN API master (FAQ vs catalog):**
   - The FAQ (L7) says "OPEN API는 `t8430`(주식 종목 조회), xingAPI는
     `t8436`(주식 종목 마스터)을 사용합니다."
   - The OPEN API catalog (L1, L2) lists **both** t8430 and t8436 as REST
     TRs on `/stock/etc`. It names t8436 "주식종목조회 **API용**".
   - The FAQ code `api.request("t8430", {"gubun": "0"})` omits the
     `t8430InBlock` wrapper that the field table and code samples use.
   - Safe consequence: choose the TR on field content, not on the FAQ.
     Treat both as candidates until a fixture exists.
2. **t8430 vs t8436 content:**
   - t8436 is a superset of t8430: it adds `bu12gubun` and `spac_gubun`,
     and `etfgubun` gains `2:ETN`.
   - In t8430, `etfgubun` documents only "1:ETF". How ETNs appear there is
     not documented.
3. **`etfgubun` / `etfchk` value `"0"`:** every non-ETF example row (t8430,
   t8436, t9945) has `"0"`, which no field table documents. **Inference:**
   "neither ETF nor ETN". Do not map an undocumented code to a type.
4. **`nxt_chk` absent from the example:** t9945's field table lists
   `nxt_chk`, but none of the three example rows contains the key.
   - Missing ≠ `0`. A missing flag must be "unknown", not "not
     NXT-eligible".
5. **No market field in t9945:** the response has no `gubun`. The market
   must come from the request selector, and t9945 has no "all" code.
6. **Name length differs:** `hname` is String 20 in t8430/t8436 and String
   40 in t9945.
   - **Inference:** long names (e.g. ETF names) may be truncated in
     t8430/t8436. Do not use `hname` as an identity key.
7. **Preferred shares indistinguishable:** `bu12gubun` `01` covers the
   example preferred row (`005385` "현대차우"). Any preferred/common
   classification would be outside inference, not documentation.
8. **`required` flags:**
   - Every request header is `required: true`, including `tr_cont_key` and
     `mac_address` "법인인 경우 필수 세팅".
   - The code samples send both as `""` (same pattern as the candle audit
     §4.8 item 4).
9. **Pagination unknown:**
   - The headers support `tr_cont`/`tr_cont_key`, but no body
     continuation key exists.
   - Whether a full-market response can be split is not documented.
   - A `load_markets` must not assume one call is complete unless the
     response `tr_cont` says so.

## 5. DB Securities (DB증권)

### 5.1 Pinned sources

GitHub sources are at
[`DBsecurities/dbsec-open-api@564b5100`](https://github.com/DBsecurities/dbsec-open-api/tree/564b5100b80a3a785468b77ee8c0557f6edcfdeb):

- Full SHA `564b5100b80a3a785468b77ee8c0557f6edcfdeb`.
- Committer date 2026-08-20T10:06:26+09:00.
- The same commit as the capability inventory and the candle audit.

Blob links below are relative to
`https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/`.

Portal JSON was retrieved 07:23:20Z–07:24:13Z on 2026-11-05 from
`https://openapi.dbsec.co.kr`. It has no immutable revision.

DB metadata JSON (DP2) contains creator and contact records and IP ranges.
None of these is copied here.

| # | Path / URL | Git blob or sha256 prefix (+ publisher revision) | Used for |
| --- | --- | --- | --- |
| D1 | `dbsec_sdk/apis/kr_stock_quote/endpoints.py` | blob `5930af396f4a74ff04c7e780fcec87660399bec3`; L29–30 (`PATHS`), L47–48 (`TR_CODES`), L68–104 (`kr_stock_search_stocks`) | Path, TR `JCODES`, "유량제어: 3 TPS" (L80), selector codes (L84), response field notes (L89–95) |
| D2 | `examples/kr_stock_quote/kr_stock_search_stocks.py` | blob `4b9a5a0e221c85513d4d76816b5a8f6b3a200a9c`; L1–46 | Example body `{"In": {"InputCondMrktDivCode": "J"}}` (L39–43); response field notes (L18–28) |
| D3 | `docs/api_support_matrix.md` | blob `f63c7746d947ac1c3d704489b18ad5d62657f65c`; L5–6, L53 | Legend "⭕ — 모의투자(`mode: "demo"`) + 실전투자 모두 호출 가능"; JCODES row ⭕, TPS 3 |
| D4 | `dbsec_sdk/response.py` | blob `6ce92fdc7fca3e34dda4c25b2797e153de29f7a5`; L27–28, L42–47, L66–70, L78–83 | `cont_yn`/`cont_key` are response headers; success is `rsp_cd == '00000'` |
| D5 | `dbsec_sdk/client.py` | blob `6000fa447765e6fc5822e6c8fe09ef92ead8d462`; L76, L220–282 | SDK paging loop and the `_PAGED_SAFETY_CAP = 100` truncation (SDK behaviour, **not** a contract) |
| D6 | `docs/errors_and_rate_limits.md` | blob `889d4557b9a60d7965eca02673455ec4373c43e9`; L48, L104–108, L208–212 | `IGW00201`; the three `00000` messages including "모의투자 데이터가 없습니다."; app 20 TPS |
| D7 | `config.yaml.example` | blob `f6204f1399f2f080c11f28364444b40b7868ef96`; L13–14 | "REST API URL은 운영/모의 동일 (앱 속성으로 내부 분기)"; `https://openapi.dbsec.co.kr:8443` |
| D8 | `README.md` | blob `377b5b9e0e3bcdfa54edad23507860798fa91143`; L499–503 | "응답이 여러 페이지로 나뉘는 조회(순위·종목조회·…)" |
| DP1 | https://openapi.dbsec.co.kr/api/apis/public/api-list/80005fb0-6feb-4b8b-904a-605c59e29b4f (group 국내주식시세) | `f4f56996c26c33b3`, 07:23:20Z. The same bytes as the inventory copy (06:55:17Z). | JCODES/WCODES entries: `accessUrl`, `extraParam`, `lastModifiedDate` |
| DP2 | https://openapi.dbsec.co.kr/api/apis/public/d8621b8b-11fd-4d01-b175-e6e3f6285215 | `c437e95c135e9651`, 07:23:21Z | `name` "주식종목 조회"; `httpMethod` `POST`; `contentType` `application/json;charset=utf-8`; `domain` `https://openapi.dbsec.co.kr:8443`; `simulatedDomain` null; `extraParam` `svc_id` "JCODES", `requestLimit` "3" (personal and `CorpThroughputQuotaRule`); `termsOfUse.name` "약관1"; `billingPolicy.name` "무과금"; `createdDate` 2024-02-26T16:34:15+09:00; `lastModifiedDate` 2024-03-28T10:28:28+09:00 |
| DP3 | https://openapi.dbsec.co.kr/api/apis/guide/tr/d8621b8b-11fd-4d01-b175-e6e3f6285215 | `4c6329458f9036de`, 07:23:23Z | `[0].id` `de65de78-52fa-4e6e-88b0-54b182eccd57`, `trCode` "JCODES", `transactionPerSec` "3", `reqExample`, `resExample` |
| DP4 | https://openapi.dbsec.co.kr/api/apis/guide/tr/property/de65de78-52fa-4e6e-88b0-54b182eccd57 | `372c44c2077f9cc1`, 07:23:41Z | Header/body field tables (`bodyType` `req_h`, `req_b`, `res_h`, `res_b`) |
| DP5 | https://openapi.dbsec.co.kr/apiservice | `11d236298f41353e`, 07:24:04Z | Endpoint discovery (the page script calls `/api/apis/public/`, `/api/apis/guide/tr/`, `/api/apis/guide/tr/property/`) |

**Missing evidence:**

- There is no DB master **file** download in the SDK or the portal JSON.
- `termsOfUse` is only an id and the name "약관1"; its text was not
  retrieved.
- The DB FAQ and notice pages (`/community-faq` → `…-000000000002`
  `de46dc17480b4959`; `/community-notice` → `…-000000000001`
  `605d50ae1b3c57b8`, 07:24:12–13Z) load their content via
  `/api/forums/public`. That content was not retrieved or inspected.
- The ELW list `WCODES` (`/api/v1/quote/kr-stock/inquiry/elw-ticker`, tps
  3; D1 L106–141) was noted but not audited.

### 5.2 Delivery

| Concern | Value (verbatim where possible) | Source | Evidence |
| --- | --- | --- | --- |
| Method + path | `POST /api/v1/quote/kr-stock/inquiry/stock-ticker` | DP2 `accessUrl`, `httpMethod`; D1 L30, L79 | field table, publisher client code |
| TR id | `JCODES` ("주식종목 조회") | DP2 `extraParam.svc_id`, DP3 `trCode`, D1 L48 | field table |
| Origin | `https://openapi.dbsec.co.kr:8443`; `simulatedDomain` null | DP2; D7 L13–14 | field table, publisher repo note |
| Paper availability | D3 L53 marks JCODES ⭕, i.e. callable in demo and production. D7 says the URL is the same for both ("앱 속성으로 내부 분기"). | D3, D7 | publisher repo note |
| Request headers (names) | `content-type`, `authorization`, `cont_yn`, `cont_key`, `mac_address`; all `requireYn` `Y`. There is no `tr_cd` header. | DP4 `req_h` | field table |
| `mac_address` | "제휴사인 경우 필수 세팅, 개인은 세팅 X" | DP4 | field table |
| Body | `{"In": {"InputCondMrktDivCode": "J"}}` | DP3 `reqExample`; D2 L39–43 | publisher example |
| Selector | `InputCondMrktDivCode` String(`A0001`) 2: "J : 주식 (KRX) / NJ : 주식(NXT) / UJ : 주식(통합) / E : ETF / EN : ETN" | DP4 `req_b` 001.001; D1 L84 | field table |
| Response array | `Out` (type `A0002`) | DP4 `res_b` 001; DP3 `resExample` | field table, publisher example |
| Envelope / success | Root `rsp_cd`, `rsp_msg`; the example shows `"00000"`, "정상 처리 되었습니다.". D4 L78–83: "업무 성공은 rsp_cd == '00000' 으로 확인한다 (서버가 HTTP 200 과 함께 업무오류코드 M100/IGW… 를 내려주는 경우가 있음)". D6 L104–108 lists `00000` with "조회가 완료되었습니다.", "정상 처리 되었습니다." and "모의투자 데이터가 없습니다." | DP3, D4, D6 | publisher example, publisher client code, publisher repo note |
| Pagination | DP2 `description` and D1 L77: "※ 연속키 조회를 통해 종목을 추가로 조회 할 수 있습니다." Request headers `cont_yn` "연속거래 여부(Y:연속거래 사용 N:연속거래 사용안함)" and `cont_key` (length **70**) "연속일 경우 그전에 내려온 연속키 값 올림". Response headers `cont_yn` "연속거래 여부" and `cont_key` (length **18**, `requireYn` `N`). | DP2, DP4, D1 | field table, portal prose |
| Paging protocol (SDK) | D5 L233–236: "첫 요청: cont_key='' → cont_yn='N'(처음부터) … 이후 요청: 직전 응답의 cont_key 를 cont_yn='Y' 로 패스스루 · 종료: 응답 헤더 cont_yn != 'Y'". The SDK also stops on an empty or unchanged key (L260–269). It stops at 100 pages by default and only logs a warning (L76, L277–282). | D5 | publisher client code (**not** a contract) |
| Page size | not documented (no count field) | DP4 | not found |
| Rate | 3 TPS for JCODES (DP2 `requestLimit` "3", DP3 `transactionPerSec` "3", D1 L80, D3 L53). App level "20 TPS" (D6 L210). Over the limit: `IGW00201` "호출 거래건수를 초과하였습니다." (D6 L48). | DP2, DP3, D1, D3, D6 | field table, publisher repo note |

### 5.3 Coverage: markets, venues, instrument types

| Market / type | Covered? | Discriminating field + documented codes | Source | Evidence |
| --- | --- | --- | --- | --- |
| KOSPI | yes | `MrktClsCode` "시장분류구분코드": "1: 코스닥 / 4: 코스피". `MrktClsName` "시장구분명": "구분자 목록: "ETF", "ETN","코넥스","코스닥","거래소(코스피)"". **The example contradicts both** (§5.8 item 1). | DP4 `res_b`, D1 L91–95, D2 L21–25 | field table vs publisher example |
| KOSDAQ | yes | `MrktClsCode` `1`; `MrktClsName` "코스닥" | DP4 | field table |
| KONEX | Listed as a `MrktClsName` value | `MrktClsName` "코넥스". No selector code targets KONEX alone, and which selector returns KONEX rows is not documented. | DP4 | field table |
| NXT | As a **request venue**, not a per-row flag | Selector `NJ` "주식(NXT)", `UJ` "주식(통합)". There is no per-row NXT-eligibility field, and what `NJ`/`UJ` return (NXT-traded subset? prefixed codes?) is not documented. | DP4 `req_b` | field table |
| ETF | yes | Selector `E` "ETF"; `MrktClsName` "ETF". The `J` example also returns rows with `MrktClsName` "ETF" (7 of 22 rows). | DP4, DP3 | field table, publisher example |
| ETN | yes | Selector `EN` "ETN"; `MrktClsName` "ETN" | DP4 | field table |
| ELW | separate TR | `WCODES` with selector "W" (D1 L106–122) | D1 | publisher client code |
| REIT / SPAC / DR / infra / mutual fund | **no discriminator** | none documented | DP4 | not found |
| Preferred shares | **no discriminator** | None documented. The `J` example contains preferred rows, e.g. `000105` "유한양행우", with the same `MrktClsCode`/`MrktClsName` as common stock. | DP3 | publisher example |

### 5.4 Identifier fields

| Concern | Field | Documented type/length/format | Source | Evidence |
| --- | --- | --- | --- | --- |
| Short code | `Iscd` "종목코드" | String(`A0001`) length **9**; the examples are six characters | DP4, DP3 | field table, publisher example |
| Standard code (12 chars) | `StndIscd` "표준종목코드" | length 12; the examples are ISIN-shaped, e.g. `KR7000020008` | DP4, DP3 | field table, publisher example |
| Korean name | `KorIsnm` "한글종목명" | length 40 | DP4 | field table |
| English name | — | not documented | DP4 | not found |
| Venue-qualified native id | — | Not documented in the master. Quote and chart TRs take `N-`/`U-` prefixed codes ("NJ(NXT 주식): (ex. N-005930) - UJ(통합): (ex. U-005930)", D1 L176, L236). Whether `NJ`/`UJ` master rows carry such prefixes is not documented. | D1 | publisher client code |

**Alphanumeric short codes: shown in a publisher example.**

- The DP3 `resExample` for selector `J` contains 7 rows whose `Iscd` mixes
  digits and letters. Example: `"Iscd": "0000D0"`,
  `"StndIscd": "KR70000D0009"`, `MrktClsName` "ETF".
- The field table gives no format rule beyond length 9.
- This conflicts with the v0.1 "exactly six ASCII digits" rule
  ([market-data spec §3](../specifications/market-data-v0.1-draft.md)).
- **Inference:** the 9-character length may fit prefixed codes such as
  `N-005930` (8 characters). This is not documented.

### 5.5 Trading attributes (only as documented)

JCODES `Out` has exactly five documented fields: `MrktClsName`, `Iscd`,
`StndIscd`, `KorIsnm` and `MrktClsCode` (DP4 `res_b`; D1 L89–95).
**None** of the attributes in the template table is present:

- tick size;
- lot size;
- listing or delisting date;
- halt, administrative or caution flags;
- NXT eligibility;
- par value;
- listed shares;
- base price;
- limits.

Each is **not documented / not found** in the master. Per-symbol quote
routes (e.g. `PRICE`, `/api/v1/quote/kr-stock/inquiry/price`) were not
audited for these attributes.

### 5.6 Freshness and staleness

- **Update cadence:** not documented.
- **As-of field:** none in `Out`; the request has no date input.
- DP2 `lastModifiedDate` 2024-03-28T10:28:28+09:00 dates the **API
  definition**, not the data.
- **Staleness detection:** not documented.

### 5.7 Data rights and redistribution

Not documented in the pinned sources. No redistribution statement was
found in D1–D8 or DP1–DP5; DP2 names only `termsOfUse` "약관1", whose text
was not retrieved.

### 5.8 Contradictions and inferences

1. **`MrktClsCode` / `MrktClsName` vs example:**
   - The field table (DP4) and the SDK docstrings (D1 L91–95, D2 L21–25)
     say `MrktClsCode` "1: 코스닥 / 4: 코스피". They give `MrktClsName`
     values "ETF", "ETN", "코넥스", "코스닥", "거래소(코스피)".
   - The DP3 example (selector `J`) returns `"MrktClsCode": "1"` with
     `"MrktClsName": "거래소"` for 15 rows, e.g. `000020` "동화약품"
     (`StndIscd` `KR7000020008`).
   - **Inference (outside knowledge, not publisher text):** those issuers
     are KOSPI-listed. LS's own example lists the same `000020` row with
     `gubun` `"1"` (코스피) (L3, L4), which supports this reading.
   - The example name "거래소" is not the documented "거래소(코스피)".
   - All 7 ETF rows also have `MrktClsCode` `"1"`.
   - **Inference:** the documented `1`/`4` mapping is unreliable, or code
     `1` means something else (e.g. "listed/exchange").
   - Safe consequence: **do not map `MrktClsCode` to KOSPI/KOSDAQ**, and do
     not map `MrktClsName` strings beyond verbatim values, until a sanitised
     live fixture resolves this.
2. **Selector `J` vs `E`:**
   - `E` "ETF" is a separate selector, yet the `J` "주식 (KRX)" example
     returns ETF rows.
   - Whether `J` is a superset of `E`/`EN`, and whether it includes KONEX,
     is not documented.
   - De-duplicate by `StndIscd`, not by selector.
3. **`cont_key` length:** 70 in the request header table, 18 in the
   response header table. This is the same discrepancy as the chart routes
   (candle audit §5.8 item 6).
4. **Duplicate `propertyOrder`:** in DP4 `res_b`, `MrktClsName` and `Iscd`
   both carry `propertyOrder` `001.001`. Field order in the documentation
   is therefore not authoritative. Decode by key.
5. **`mac_address`:** marked `requireYn` `Y`, but described as "개인은 세팅
   X".
6. **Success with no data:** D6 L108 lists `00000` "모의투자 데이터가
   없습니다.".
   - An empty `Out` under the success code is possible in paper.
   - An empty or short list must never replace a cached master.
7. **SDK truncation:**
   - D5 stops paging at 100 pages by default (`_PAGED_SAFETY_CAP`). It also
     stops on an empty or unchanged `cont_key` while `cont_yn` is `Y`.
   - In both cases it only logs a warning and returns the pages it has.
   - KTradeLink must not copy this silent-partial behaviour; a truncated
     master must be an error.
8. **NJ/UJ semantics:** not documented. **Inference:** `NJ` may return only
   NXT-tradable symbols, which would act as an eligibility list. This is
   unverified and must not be used as an NXT flag without a fixture.

## 6. Toss Securities (토스증권)

### 6.1 Pinned sources

All Toss sources are public documentation files on `openapi.tossinvest.com` /
`developers.tossinvest.com`, retrieved 2026-11-05 07:20:44–07:21:19 UTC. Web
files have no immutable revision; the sha256 prefix identifies only the copy
retrieved at that time. T1 carries a publisher version (`info.version`).
T1's hash is identical to the copy pinned in the candle audit (06:43:32Z) and
the capability inventory (06:55:39Z), so the same document was in force all
morning. Line numbers (`L…`) refer to the retrieved copies (T1 is
pretty-printed JSON).

| # | Path / URL | sha256 prefix (+ publisher revision) | Used for |
| --- | --- | --- | --- |
| T1 | [openapi.json](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json), 07:20:44–07:20:46Z, 534,361 bytes | `c5918961335ccd6b…`; `openapi 3.1.0`, `info.version 1.2.28` | `paths./api/v1/stocks/all.get` (`listStocks`, L1073–1265); `paths./api/v1/stocks.get` (`getStocks`, L853–1072); `paths./api/v1/stocks/{symbol}/warnings.get` (L1266–); `paths./api/v1/price-limits.get` (L571–); `components.parameters.{Symbol,SymbolQuery,KrSymbol}` (L8805–8880); `components.schemas.{ListedStock (L9925), StockInfo (L9712), KrMarketDetail (L9843), StockWarning (L9876), PriceLimitResponse (L9593), Currency, ApiResponse}`; `servers[0].url` (L10); `ErrorResponse.error.data` (L9356) |
| T2 | [overview.md](https://openapi.tossinvest.com/openapi-docs/overview.md), 07:21:13Z, 31,279 bytes | `bef057d9babe9a38…` (same hash as the candle-audit copy); no visible revision | L24, L27 (종목 마스터 scope), L103, L236–247 (rate-limit groups `STOCK`, `STOCK_ALL`) |
| T3 | [faq.md](https://openapi.tossinvest.com/openapi-docs/faq.md), 07:21:19Z, 19,799 bytes | `6ad4c02b8e785f7d…`; no visible revision | L33 (delisted → 404), L84 (halt flags), L86–88 (데이터 이용 정책) |
| T4 | [llms.txt](https://developers.tossinvest.com/llms.txt), 07:21:15Z, 2,847 bytes | `bbff77eaa55df248…` | L16: the OpenAPI JSON is "the source of truth for endpoints, schemas, … and rate limits"; L18 links T3 |

**Missing evidence:**

- No definition of the `KR_ETC` market value in T1, T2 or T3. The value
  appears only in enums and in the 400 example (T1 L1100, L1231).
- No KONEX, ELW, SPAC, 관리종목 or 투자주의 value anywhere in T1, T2 or T3
  (searched).
- No tick-size, lot-size or par-value field in any instrument schema.
- No as-of / base-date field in either stock-info response.
- No paper/sandbox origin (as in the inventory).
- The Markdown API reference (`/openapi-docs/latest/api-reference/README.md`,
  linked from T4 L15) was **not** retrieved. T4 marks T1 as canonical.

### 6.2 Delivery

Toss delivers the instrument list over **REST only**; there is no file.
Two routes are needed for a full master (T1 L1079: "**관련 API**: 여기서 얻은
`symbol` 로 [`GET /api/v1/stocks`] … 를 호출해 종목명·통화·상장상태 등 상세
정보를 채울 수 있습니다.").

| Concern | Value (verbatim where possible) | Source | Evidence |
| --- | --- | --- | --- |
| Universe route | `GET /api/v1/stocks/all`, operationId `listStocks`, summary "마켓별 전체 종목 조회" | T1 L1073–1080 | field table |
| Purpose | "마켓(거래소)별 종목 리스트를 조회합니다. 종목 유니버스 구성 용도이며, 토스증권에서 거래 가능한 종목만 제공합니다." | T1 L1079 | field table |
| Detail route | `GET /api/v1/stocks`, operationId `getStocks`, "종목 기본 정보 조회", "`symbols` 를 콤마로 구분하여 최대 200건 까지 다건 조회를 지원합니다." | T1 L853–867 | field table |
| Origin | `servers[0].url` `https://openapi.tossinvest.com`. No paper origin. | T1 L8–10 | field table |
| Auth / headers | `security: oauth2ClientCredentials` (Bearer token; `tokenUrl` `/oauth2/token`, T1 L8782). **No** `X-Tossinvest-Account` parameter on either route. | T1 L1080–1086, L860–866 | field table |
| Query (`/stocks/all`) | `market` (required; enum `KOSPI`, `KOSDAQ`, `NYSE`, `NASDAQ`, `AMEX`, `KR_ETC`, `US_ETC`); `status` (optional; `SCHEDULED`/`ACTIVE`/`DELISTED`; "미지정 시 ACTIVE"); `securityType` (optional; "미지정 시 전체 유형"); `commonShare` (optional boolean; "true=보통주만, false=우선주만, 미지정 시 전체") | T1 L1088–1150 | field table |
| Query (`/stocks`) | `symbols` (required): "콤마로 구분하여 최대 200건. 예: 005930 또는 005930,AAPL. 영문 대/소문자, 숫자, '.', '-' 만 허용한다." pattern `^[A-Za-z0-9.,\-]+$` | T1 L868–878 | field table |
| Pagination | `/stocks/all`: "**정렬**: `symbol` 오름차순. 필터 조건에 해당하는 종목을 페이지네이션 없이 한 번에 반환합니다." No cursor. `/stocks`: ≤200 symbols per call; 400 `invalid-request` with `data.constraint {min:1,max:200}` above that. | T1 L1079; L1037–1060 (`tooManySymbols`) | field table + publisher example |
| Size | "마켓당 최대 수천 건(예: NASDAQ 약 2,800건, gzip 응답 약 30KB)" | T1 L1079 | field table (prose in description) |
| Envelope | 200: `ApiResponse` with `result` = array of `ListedStock` (`/stocks/all`) or `StockInfo` (`/stocks`). Errors: `ErrorResponse`; "`result` 와 `error` 는 동시에 나타나지 않습니다." Listed statuses: 400, 401, 403, 429, 500 (`InternalErrorStock` "종목 정보 조회 중 일시적 오류"). | T1 `components.schemas.ApiResponse`; L1150–1265 | field table |
| Rate | `/stocks/all`: Rate Limits Group `STOCK_ALL`; T2 L247 "`STOCK_ALL` \| 초당 최대 1회". `/stocks`: `STOCK`; T2 L246 "초당 최대 5회". T2 L238: "구체적인 한도 수치는 운영 상황에 따라 사전 공지 없이 조정될 수 있으며, 현재 허용 한도는 응답 헤더로 확인할 수 있습니다." | T1 L1079, L860; T2 | field table + portal prose |

### 6.3 Coverage: markets, venues, instrument types

| Market / type | Covered? | Discriminating field + documented codes | Source | Evidence |
| --- | --- | --- | --- | --- |
| KOSPI | yes | request `market=KOSPI`; `StockInfo.market` "상장 시장" enum incl. `KOSPI` | T1 L1088–1104, L9749 | field table |
| KOSDAQ | yes | `market=KOSDAQ` | same | field table |
| KONEX | **not documented** | No `KONEX` value. `KR_ETC` exists but is undefined. **Inference:** KONEX may fall under `KR_ETC`; unverified. | T1 enums | not found |
| `KR_ETC` | yes (value exists) | Meaning not documented. `koreanMarketDetail` "국내 종목(KOSPI, KOSDAQ, KR_ETC)에만 제공" confirms it is domestic. | T1 L9831 | field table |
| NXT (venue) | flag only | No NXT market value. `StockInfo.koreanMarketDetail.nxtSupported` "NXT 대체거래소 지원 여부". **Not in `ListedStock`**, so `/stocks/all` alone cannot tell. | T1 L9858 | field table |
| Foreign markets | yes, out of scope | `NYSE`, `NASDAQ`, `AMEX`, `US_ETC`; `koreanMarketDetail` is null for them | T1 L1088–1104, L9831 | field table |
| Common vs preferred | yes | `isCommonShare` (`StockInfo`: "보통주 여부. 우선주인 경우 false"; `ListedStock`: "보통주 여부"); filter `commonShare` | T1 L9779, L9963, L1144 | field table |
| Common stock | yes | `securityType` `STOCK` | T1 `ListedStock.securityType` enum (L9948) | field table |
| ETF | yes | `ETF` (example `069500` KODEX 200 with `securityType: "ETF"`) | T1 L9948; L998–1022 | field table + publisher example |
| ETN | yes | `ETN` | T1 L9948 | field table |
| REIT | yes | `REIT` | T1 L9948 | field table |
| Infrastructure fund | yes | `INFRASTRUCTURE_FUND` | T1 L9948 | field table |
| Depositary receipt | yes | `DEPOSITARY_RECEIPT` | T1 L9948 | field table |
| Foreign stock / foreign ETF | yes (value exists) | `FOREIGN_STOCK`, `FOREIGN_ETF`; whether these occur in KR markets is not documented | T1 L9948 | field table |
| Rights (신주인수권) | yes | `STOCK_WARRANTS`; T1 `StockWarning` table defines the same code as "신주인수권증서/증권" | T1 L9948, L9884 | field table |
| ELW | **not documented** | No ELW value | — | not found |
| SPAC | **not documented** | No SPAC value or flag. **Inference:** SPACs would be `STOCK`; unverified. | — | not found |
| Delisted / scheduled | yes | `status` `SCHEDULED`/`ACTIVE`/`DELISTED` (filter on `/stocks/all`, field on `StockInfo`) | T1 L1107–1122, L9784 | field table |
| Leverage / inverse | yes | `leverageFactor` "레버리지 배수. ETF/ETN에만 적용 (1.0, 2.0, -1.0 등)"; `string` decimal, nullable | T1 L9827 | field table |

`ListedStock` has **no `market` and no `status` field** (required:
`symbol`, `name`, `securityType`, `isCommonShare`, `isinCode`; T1 L9925–9972).
The market is only known from the request parameter.

### 6.4 Identifier fields

| Concern | Field | Documented type/length/format | Source | Evidence |
| --- | --- | --- | --- | --- |
| Short code | `symbol` | `ListedStock`/`StockInfo`: `string`, "종목 심볼.", no pattern or length on the response field | T1 L9729, L9937 | field table |
| Short code (request) | path/query `symbol` | "KRX: 6자리 종목코드 (숫자 또는 영문·숫자 조합; 예: 005930, 0101N0), US: 영문 티커 (예: AAPL). 영문 대/소문자, 숫자, '.', '-' 만 허용한다." pattern `^[A-Za-z0-9.\-]+$` | T1 `components.parameters.Symbol` L8805–8824, `SymbolQuery` L8825–8845 | field table |
| KR-only request symbol | `KrSymbol` | "국내(KR) 종목 심볼. KRX 6자리 종목코드 (숫자 또는 영문·숫자 조합; 예: 005930, 0101N0)." pattern `^[A-Za-z0-9.\-]+$` | T1 L8866–8880 | field table |
| Standard code | `isinCode` | `ListedStock`: "ISIN 코드"; `StockInfo`: "국제증권식별번호 (ISO 6166)"; `string`, no pattern; examples `KR7005930003`, `KR7069500007` | T1 L9744, L9968 | field table + publisher example |
| Korean name | `name` | "종목명 (한글)"; US symbols also carry a Korean name ("NASDAQ 종목 (미국 종목도 한글 name 제공)") | T1 L9734, L9942; L1200 | field table |
| English name | `englishName` | `StockInfo` only, "영문 종목명", required. Not in `ListedStock`. | T1 L9739 | field table |
| Venue-qualified id | none | No venue suffix or prefix; one symbol per instrument. T3 L22: domestic data is "KRX + NXT 통합 시세". | T1; T3 | field table + portal prose |

**Alphanumeric short codes.** T1 documents them explicitly. Every KRX symbol
description says "6자리 종목코드 (숫자 또는 영문·숫자 조합)". Examples are
`0101N0` (`Symbol`, `SymbolQuery`, `KrSymbol`) and `0167A0` (ranking item
schemas, e.g. `NetBuyRankingItem.symbol`, T1 L11258).

- The **pattern does not enforce six characters**: `^[A-Za-z0-9.\-]+$` also
  admits `.`, `-`, lower case and any length. "6자리" is prose only.
- **No** Q-prefixed ETN or J-prefixed ELW code form is documented.
- The KTradeLink v0.1 rule "exactly six ASCII digits" ([market-data spec §3](../specifications/market-data-v0.1-draft.md);
  [ADR 0013](../decisions/0013-public-fetch-ticker-surface.md) L37 at
  `main` `03680cd6e36afd3b85f80e080fb9e6259c0c20e2`) would reject the
  publisher's own example `0101N0`.

### 6.5 Trading attributes (only as documented)

| Attribute | Field + documented meaning/codes | Source | Evidence |
| --- | --- | --- | --- |
| Tick size / price unit | **Not in the master.** Order prose only: "KR: 정수 (원 단위). 호가 단위에 맞아야 합니다 (예: 50,000~200,000원 구간은 100원 단위)". A mismatch returns 400 with `data.tickSize` ("호가 단위") and `nearestPrices`. | T1 L12380 (`OrderCreateRequest` `price`), L9356, L6624–6640 (`invalidTickSize` example) | field table + publisher example |
| Lot size | **Not in the master.** For KR orders, quantity must be a positive integer ("기본: 양의 정수만 가능합니다"; `OrderModifyRequest.quantity` "KR 주식: 필수. 양의 정수만 허용합니다"). No 매매수량단위 field. | T1 L12372, L12469 | field table |
| Listing date | `StockInfo.listDate` `["string","null"]` date, "상장일 (YYYY-MM-DD, KST 기준). 정보 미제공 시 null" | T1 L9801 | field table |
| Delisting date | `StockInfo.delistDate` "상장폐지일 (YYYY-MM-DD, KST 기준). 활성 종목은 null" | T1 L9810 | field table |
| Trading halt | `koreanMarketDetail.krxTradingSuspended` (required boolean) "KRX 거래정지 여부"; `nxtTradingSuspended` `["boolean","null"]` "NXT 미지원 종목(nxtSupported=false)은 null". T3 L84: "과거 거래정지 이력은 제공하지 않습니다." | T1 L9863, L9871; T3 L84 | field table + portal prose |
| Administrative issue (관리종목) | **not found** | — | not found |
| Caution / warning / risk | Separate per-symbol route `GET /api/v1/stocks/{symbol}/warnings` (group `STOCK`). `warningType` enum: `LIQUIDATION_TRADING`, `OVERHEATED` 단기과열, `INVESTMENT_WARNING` 투자경고, `INVESTMENT_RISK` 투자위험, `VI_STATIC_AND_DYNAMIC`, `VI_STATIC`, `VI_DYNAMIC`, `STOCK_WARRANTS`. "클라이언트는 unknown code 를 허용하도록 구현해야 합니다." **No 투자주의 (caution) code.** `exchange` "KRX, NXT 등 물리적 거래소 단위". | T1 L1266–, L9876–9924 | field table |
| NXT eligibility | `koreanMarketDetail.nxtSupported` (required boolean) "NXT 대체거래소 지원 여부" | T1 L9858 | field table |
| Par value | **not found** | — | not found |
| Listed shares | `StockInfo.sharesOutstanding` (required, `string` decimal, maxLength 30) "발행주식수", i.e. *issued* shares; "listed" is not stated | T1 L9817 | field table |
| Base / reference price | **Not offered per symbol.** T3 L42: "종목별로 조회하는 API 는 제공하지 않습니다. 기준가(`basePrice`)와 등락률은 랭킹 조회(`GET /api/v1/rankings`) 응답 항목에만 포함됩니다." | T3 L42 | portal prose |
| Price limits | Separate per-symbol route `GET /api/v1/price-limits` (group `MARKET_DATA`): `upperLimitPrice`/`lowerLimitPrice` "상한가"/"하한가" (nullable for markets without limits), `timestamp` | T1 L571–, L9593 | field table |
| Liquidation trading | `koreanMarketDetail.liquidationTrading` (required) "정리매매 여부 (상장폐지 절차 진행 중)." | T1 L9853 | field table |
| Currency | `StockInfo.currency` (`Currency` enum `KRW`, `USD`; "클라이언트는 unknown enum 값을 허용하도록 구현해야 합니다.") | T1 `components.schemas.Currency` | field table |

### 6.6 Freshness and staleness

- **Cadence (documented):** `/stocks/all` (T1 L1079): "일 배치로 갱신되는
  저변동 데이터이므로 하루 1회 조회 후 로컬 캐싱을 권장합니다."
- **Warnings (documented, T1 warnings description):** "VI 발동/해제는 거래소
  이벤트 발생 후 수 초 내 반영됩니다. 정리매매·단기과열·투자경고/위험 지정은
  거래소 공시 기준 일배치로 반영됩니다." Activity is defined as
  "`startDate <= 오늘 <= endDate` 인 항목 (또는 `endDate` 가 `null` 인 진행 중
  항목)".
- **Batch time:** the time of day of the batch is **not documented**.
- **As-of field:** none in `ListedStock` or `StockInfo`. The response carries
  no batch date.
- **Freshness of `/api/v1/stocks`:** the halt/NXT flags are not documented
  (real-time vs batch).
- **Staleness detection:** not documented. **Inference:** a client can only
  record its own fetch time.

### 6.7 Data rights and redistribution

T3 L86–88 ("데이터 이용 정책"): "상업적 이용이 제외될 뿐만 아니라 비상업적인
용도라 하더라도 제 3자에게 배포하는 행위는 엄격히 금지됩니다." Fetched lists are
therefore never committed or used as fixtures (header caution; G-R1).

### 6.8 Contradictions and inferences

1. **Tradable-only vs `DELISTED` filter.** T1 L1079 says `/stocks/all`
   returns "토스증권에서 거래 가능한 종목만". The same route accepts
   `status=DELISTED` and `SCHEDULED`. T3 L33 says delisted symbols' history
   returns `404 stock-not-found`.
   - Whether `DELISTED` rows are actually returned, and how far back, cannot
     be resolved from the documentation.
   - Consequence: `load_markets` must request `ACTIVE` explicitly. It must
     not treat absence from the list as delisting.
2. **`englishName` required but missing in an example.** `StockInfo.required`
   includes `englishName` (T1 L9714). The `etf` example (KODEX 200, T1
   L998–1022) omits the key; the other examples include it.
   - Consequence: the decoder must treat a missing `englishName` as
     *unknown*, not as a hard error, until a fixture settles it. It must not
     substitute an empty string silently.
3. **"6자리" prose vs pattern.** See §6.4. The response `symbol` has no
   pattern at all.
   - Consequence: Toss KR symbols must be validated as opaque ASCII
     alphanumerics. A future six-char alphanumeric rule must come from an
     ADR, not from this pattern.
4. **`isCommonShare` for non-equity types.** The ETF example has
   `isCommonShare: true`. The filter `commonShare=false` is described as
   "우선주만".
   - Whether ETF/ETN/REIT rows are excluded by `commonShare=false`, and what
     `isCommonShare` means for them, is not documented.
   - Consequence: preferred = `securityType == STOCK && !isCommonShare` is
     an **Inference**, not a mapping.
5. **`market` (segment) vs `exchange` (venue).** `StockInfo.market` "warnings
   API의 exchange(거래소 단위)와 달리 시장 세그먼트 단위로 구분". NXT is
   therefore a capability flag (`nxtSupported`), not a market.
   - Consequence: KTradeLink must not map `market` to a venue. In
     particular, `KOSPI`/`KOSDAQ` ≠ `KRX` venue identity.
6. **`KR_ETC` undefined.** It is domestic (it gets `koreanMarketDetail`), but
   its membership is undocumented. Consequence: exclude it from
   `load_markets` until documented or fixture-verified.
7. **Two-step master.** `ListedStock` lacks NXT, halt, listing date, English
   name and market fields.
   - A complete domestic master needs `/stocks/all` per market (1 rps),
     then `/stocks` in ≤200-symbol batches (5 rps).
   - **Inference:** about 13 detail calls for ~2,500 KOSPI rows. The
     publisher gives only NASDAQ (~2,800) as a size example.
8. **OpenAPI version label.** T4 L16 calls T1 an "OpenAPI 3.0 document". T1
   declares `openapi: 3.1.0` and uses 3.1 type arrays (`["string","null"]`)
   for `listDate`, `delistDate`, `leverageFactor` and
   `nxtTradingSuspended`. (Same finding as candle audit §6.8 #4.)
9. **`sharesOutstanding` = issued, not listed.** It is labelled "발행주식수".
   Equating it with 상장주식수 is an inference.

## 7. Meritz Securities (메리츠증권)

### 7.1 Pinned sources

- **Portal:** `https://openapi.imeritz.com`, retrieved 2026-11-05
  07:21:43–07:25:38 UTC. Portal HTML embeds per-request script blobs and CSRF
  tokens, so page hashes differ per copy and identify only the retrieved
  bytes.
- **Repository:**
  [`meritz-securities/open-api@a93c6409`](https://github.com/meritz-securities/open-api/tree/a93c6409db73ea97ad15f7b7186f36c9f32ecd89)
  (`a93c6409db73ea97ad15f7b7186f36c9f32ecd89`, commit
  2026-10-28T22:32:03+09:00). It was still the remote `HEAD` at ~07:25Z.
  - README L11 makes the portal canonical: "API 목록과 파라미터·응답 필드의
    정본은 [개발자 포털](https://openapi.imeritz.com)입니다." Repo notes
    therefore rank below the portal.

| # | Path / URL | Git blob or sha256 prefix (+ publisher revision) | Used for |
| --- | --- | --- | --- |
| M1 | [stock-info](https://openapi.imeritz.com/stock-info) "종목정보 파일 다운로드", 07:21:43Z, 159,184 bytes | sha256 `43b377a664d0c5cc…` (inventory copy at 06:57:19Z was `c44ed281…`; dynamic page) | L11 (meta description), L2142–2255 (download cards, file names, "최종 업데이트", sizes, footnote) |
| M2 | FAQ board [`/community/10000000-0000-0011-0000-000000000002`](https://openapi.imeritz.com/community/10000000-0000-0011-0000-000000000002), 07:23:12Z, 229,558 bytes | sha256 `c9ed81f50b49373f…` | Embedded JSON-LD `FAQPage.mainEntity` on L35: "국내/해외 종목들의 리스트를 받을 수 있는 API는 없을까요?", "…시세데이터를 이용해 웹페이지를 공개해도 되나요", "…종목코드 앞의 문자는 무엇을 의미하나요?" |
| M3 | API spec JSON export [`/api-spec/download/json`](https://openapi.imeritz.com/api-spec/download/json), 07:21:58Z, 1,136,519 bytes | sha256 `56628855ef33ae1d…`; `generatedAt "2026-11-05 16:19:00"`. With `generatedAt` removed and `json.dumps(sort_keys=True, ensure_ascii=False)`, it hashes to `2fff4f3e02d20cd5…`, **identical** to the candle-audit canonical hash. | Negative check for a master route or column spec; `groups[name="국내주식"].apis[url="/market/v1/prices"].trs[code="ohhts_1001_001r"]` request/response fields |
| M4 | API spec Excel export [`/api-spec/download/excel`](https://openapi.imeritz.com/api-spec/download/excel), 07:22:55Z, 333,447 bytes | sha256 `a2cde8cb4980edd5…`; `Content-Disposition` filename `meritz_openapi_spec_20261105.xlsx`; 88 sheets | Negative check: no sheet or string about `.mst` / 종목정보 file layout |
| M5 | [apiservice](https://openapi.imeritz.com/apiservice) 07:22:27Z `653b7a5838c998f5…`; [samplecode-py](https://openapi.imeritz.com/samplecode-py) 07:25:38Z `7c4ab7bba9286210…`; [howto-use](https://openapi.imeritz.com/howto-use) `6009747542243d85…`; [intro](https://openapi.imeritz.com/intro) `507fbc7a94ab12fa…` | — | Negative checks: the only `종목정보` hit is the nav link (`href="/stock-info"`). No master download or parser code. |
| M6 | Repo `a93c6409…` files | blobs: `README.md` `61aa5f7f2c1059a29a99175a5cdf573996d81479`; `llms.txt` `8351d5343d785b61107179d19197c59a08e1edff`; `DISCLAIMER.md` `1ecb0ebd63232e1de6b33a11ce55728655627f84`; `LICENSE` `be744417a05876aeaaf8a6e99632fe81e42cd074`; `openapi.json` `93e900e66b965607d7fd8b8e14c6088d710e6fce`; `meritz/data/catalog.json` `000c2dbc636ad46077d4f46d67a04e0cd6fe1319` | README L11; [`llms.txt` L55–57](https://github.com/meritz-securities/open-api/blob/a93c6409db73ea97ad15f7b7186f36c9f32ecd89/llms.txt#L55-L57); DISCLAIMER L12–13. `git grep` for `.mst`, `stock-info`, `종목정보`, `마스터` over the tree finds only unrelated `oder_rsev_mst_*` fields. |
| M7 | Downloaded master files (once each, by the Meritz research, scratchpad only, **not committed, no row quoted**): [`/stock-info/download/kospi`](https://openapi.imeritz.com/stock-info/download/kospi) 07:23:45Z; [`/stock-info/download/kosdaq`](https://openapi.imeritz.com/stock-info/download/kosdaq) 07:23:47Z | KOSPI 304,640 bytes, sha256 `738eacacad67f73d5904096d8adbb29cb962fb7bda4b48115369821d0fd2e22b`; KOSDAQ 214,227 bytes, sha256 `5f76461520947480dc6080d0d91999e44bb3f84305765a5639902cfdafee7eda` | Format, encoding, record length, code shapes (counts only) |

**Missing evidence:**

- **The column specification of the `.mst` files was not found.**
  - M1 L2254–2255 says "파일 형식과 컬럼 명세는 API 문서를 참고해주세요."
  - It is absent from: the JSON spec (M3), the Excel spec (M4, all 88
    sheets), the static apiservice/howto-use/intro/samplecode pages (M5),
    and the repo (M6).
  - The apiservice page loads API detail by script
    (`/api/apis/public/api-list/<group>`). Its group list (OAuth, 계좌,
    국내주식, 해외주식, 실시간 ×2) has no 종목정보 entry.
- `/stock-info/download/all` (zip) and `/stock-info/download/exst`
  (overseas) were **not** downloaded.
- The Open API terms of use (`/api/terms/public?termsType=…`) were not
  retrieved.
- No publisher client code downloads or parses the master.

### 7.2 Delivery

Meritz delivers the domestic master as **files only**. M2 FAQ: "국내/해외 전체
종목 조회 API는 제공되지 않으며, Open API 포털 > API 가이드 > 종목정보를 통해
종목정보 확인이 가능합니다." (portal prose). The M3 catalogue has no list
route.

| Concern | Value (verbatim where possible) | Source | Evidence |
| --- | --- | --- | --- |
| URLs | `https://openapi.imeritz.com/stock-info/download/kospi` → `mts_kospi_code.mst`; `…/download/kosdaq` → `mts_kosdaq_code.mst`; `…/download/exst` → `mts_exst_code.mst` (해외주식, out of scope); `…/download/all` "종목정보 파일을 하나의 zip 파일로 내려받으세요." | M1 L2150–2246 | portal prose |
| Host / scheme | `openapi.imeritz.com`, HTTPS default port 443 (portal host). This is **not** the REST origin `https://openapi.imeritz.com:9443`. | M1; M7 | portal prose + file observation |
| Authentication | None documented. **Observed:** an anonymous `GET` (no auth header, no cookie) returned HTTP 200. That is one retrieval, not a contract. | M7 | file observation |
| TLS | The download went through this session's HTTPS proxy. curl verification succeeded against the proxy CA bundle (`ssl_verify_result=0`). **The origin certificate chain was not independently inspected.** No publisher code for this download exists, so there is no TLS-disabling pattern to flag (contrast KIS K1–K3 and K8, §2.2). | M7; M5/M6 negative | file observation |
| Response headers (observed) | `Content-Type: application/octet-stream`; `Content-Disposition: attachment; filename="mts_kospi_code.mst"` (resp. `mts_kosdaq_code.mst`); `Content-Length` equals the bytes received; `Cache-Control: no-cache, no-store, max-age=0, must-revalidate`; **no** `Last-Modified`, `ETag` or `Content-Encoding` | M7 | file observation |
| Compression | Individual `.mst`: none (no zip/gzip magic; observed). `all`: zip per M1 (not downloaded). | M7; M1 L2151 | file observation + portal prose |
| Encoding | **Not documented.** Observed: both files fail UTF-8 decoding (KOSPI at byte 27, KOSDAQ at byte 258) and decode without error as CP949 and as EUC-KR. **Inference:** EUC-KR family (CP949); unverified. | M7 | file observation / inference |
| Record layout | **Not documented** (§7.1 Missing evidence). See the inference block below the table. | M7 | file observation / inference |
| Line terminator / header | Observed: LF only (no CR), trailing LF, no NUL/TAB/`\|`/`,`/`^` bytes. No header row: every record has the same length and an alphanumeric bytes 0–5. | M7 | file observation |
| Size | Page: KOSPI "297.5 KB", KOSDAQ "209.2 KB" (M1 L2182, L2212). Downloaded: 304,640 and 214,227 bytes, i.e. 297.5 KiB and 209.2 KiB. The page "KB" is therefore KiB. | M1; M7 | portal prose + file observation |
| Rate limit for downloads | not documented | — | not found |

**Record layout inferred from one copy of each file (not a publisher
contract; must not drive a decoder):**

- **Fixed byte-width records.**
  - KOSPI: 118 bytes + LF, 2,560 records (2,560 × 119 = 304,640).
  - KOSDAQ: 116 bytes + LF, 1,831 records (1,831 × 117 = 214,227).
  - **The two files have different widths.** Character counts vary under
    CP949, so the width is in bytes.
- **Bytes 0–8:** an ASCII code region, left-aligned and space-padded.
- **Bytes 9–20:** a 12-character token with a two-letter country-like
  prefix.
  - `KR` + 10 alphanumerics in 2,559/2,560 KOSPI and 1,820/1,831 KOSDAQ
    records.
  - The rest begin `KY`, `HK` or `US`.
  - **Inference:** ISIN.
- **Bytes 21–60 (KOSPI) / 21–50 (KOSDAQ):** the only bytes > 0x7F occur
  here. **Inference:** a Korean name field.
- **Remaining tail:** ASCII digits, letters and spaces. Meaning unknown.

### 7.3 Coverage: markets, venues, instrument types

| Market / type | Covered? | Discriminating field + documented codes | Source | Evidence |
| --- | --- | --- | --- | --- |
| KOSPI | yes | separate file `mts_kospi_code.mst`, "국내주식(코스피) 종목코드 및 기본정보" | M1 L2166–2174 | portal prose |
| KOSDAQ | yes | separate file `mts_kosdaq_code.mst`, "국내주식(코스닥) 종목코드 및 기본정보" | M1 L2196–2204 | portal prose |
| KONEX | **not documented** | no KONEX file | M1 | not found |
| NXT | **not documented in the master** | No file or column documented. Per-symbol REST `mrkt_div_code` `"J"` KRX / `"NJ"` 대체거래소(NXT) / `"TJ"` KRX + NXT 통합 exists on quote routes, and NJ for a non-NXT symbol returns an empty array "오류 없이" (candle audit §7.3). No eligibility flag was found in M3. | M3 `…/market/v1/prices` `mrkt_div_code` | field table (REST, not master) |
| Overseas | yes, out of scope | `mts_exst_code.mst` "해외주식 종목코드 및 기본정보" | M1 L2226–2234 | portal prose |
| Instrument types | **no documented discriminator** | Column spec missing. M2 FAQ documents code **prefixes** used "주식 주문 등에서": "1. 주식: 'A' + 숫자, ex) A138040 / 2. 수익증권: 'F' + 숫자, ex) F00000000 / 3. ELW: J' + 숫자, ex) J754609" (verbatim, including the unbalanced quote). | M2 L35 | portal prose |
| Observed code shapes (counts only; M7) | — | **KOSPI file:** 6 digits 1,767; `Q`+6 digits 357; 4 digits+letter+digit 334; `F`+8 chars 75; 5 digits+letter 22; `J`+8 chars 4; 4 digits+2 letters 1. **KOSDAQ file:** 6 digits 1,764; 4 digits+letter+digit 66; 5 digits+letter 1. **Inference:** the KOSPI file mixes non-equity products (`F` 수익증권 and `J` ELW per M2's prefix list; `Q` meaning not documented), so it is not an equity-only universe. | M7 | file observation / inference |
| ETF / ETN / REIT / SPAC / preferred | **not documented** | No type column documented. Per-symbol REST `ohhts_1001_001r` has `elw_pblc_yn` "ELW 발행 여부" and `rprs_mrkt_kor_name` (e.g. "KOSPI200"), but no ETF/ETN/REIT/SPAC/preferred discriminator. | M3 | field table (REST) / not found |

### 7.4 Identifier fields

| Concern | Field | Documented type/length/format | Source | Evidence |
| --- | --- | --- | --- | --- |
| Short code (master) | undocumented | **Inference:** bytes 0–8, space-padded (§7.2) | M7 | file observation / inference |
| Short code (REST input) | `iscd` (String, len 12, Y) | "6자리(005930) 또는 대문자 A 를 붙인 7자리(A005930)로 넣으십시오. … 표준코드(KR7005930003)·소문자 a(a005930)·등록되지 않은 코드는 오류 없이 정상 응답코드 "0000" 으로 내려오되 값이 비거나 0 입니다. 뒤에 문자가 더 붙은 값(예: A005930ZZZZZ)은 앞 7자리만 읽습니다. 응답의 단축종목코드(shrn_iscd)가 채워져 있는지 확인하십시오." | M3 `/market/v1/prices` `request.body[iscd]` | field table |
| Short code (REST output) | `shrn_iscd` (String, **len 9**) | "단축 종목코드(6자리)" | M3 `ohhts_1001_001r` `response.body` | field table |
| Code notation | — | M6 `llms.txt` L55–57: "**종목코드 표기가 API마다 다릅니다.** 시세 조회는 `005930`, 주문은 `A005930`처럼 앞에 `A`가 붙습니다. … 형식을 추측해 채우지 마십시오." | M6 | publisher repo note |
| Standard code (ISIN) | undocumented in master | **Inference:** bytes 9–20 (§7.2) | M7 | file observation / inference |
| Korean name | undocumented in master | **Inference:** CP949 region from byte 21 | M7 | file observation / inference |
| English name | **not found** | no documented column | — | not found |
| Venue-qualified id | none | Venue is the separate `mrkt_div_code` request field, not a code suffix | M3 | field table (REST) |

**Alphanumeric short codes.** No Meritz source documents the six-character
alphanumeric form, and the portal FAQ prefix list (A/F/J + 숫자) is
digits-only. Yet M7 shows non-digit codes in both files: 334 + 22 + 1
(KOSPI) and 66 + 1 (KOSDAQ) six-character codes containing letters, plus
`Q`/`F`/`J`-prefixed codes of 7–9 characters (KOSPI).

- **Inference:** the domestic universe contains codes that the KTradeLink
  v0.1 six-digit rule rejects. Whether REST `iscd` accepts them is not
  documented.

### 7.5 Trading attributes (only as documented)

The master file's columns are undocumented, so **every row below is "not
documented" for the master**. The per-symbol REST quote route
`GET /market/v1/prices` (`ohhts_1001_001r`; headers `authorization`,
`mac_address`; 10/s per the capability inventory's source M4) documents these fields instead (M3,
field table). It needs a token and MAC header and was **not called**.

| Attribute | Field + documented meaning/codes (REST `ohhts_1001_001r`) | Source | Evidence |
| --- | --- | --- | --- |
| Tick size | `aspr_unit` Number(13) "호가 단위입니다." | M3 | field table (REST) |
| Lot size | `deal_qty_unit` Number(13) "매매 수량 단위. 주문 수량은 이 단위의 배수여야 합니다." | M3 | field table (REST) |
| Listing / delisting date | **not found** | — | not found |
| Trading halt | `tmpr_susp_yn` String(2) "임시 정지 여부 / "Y": 정지 / "N": 정상" | M3 | field table (REST) |
| Status code | `issu_stat_cls_code` String(2) "종목 상태 구분 코드입니다(2자리)." **Values not enumerated.** | M3 | field table (REST) |
| Administrative issue (관리종목) | not found as a named field (may be inside `issu_stat_cls_code`; undocumented) | — | not found |
| Caution / warning / risk | `invt_epmd_cntt` String(50) "투자 유의 안내 문구입니다." (free text, no codes) | M3 | field table (REST) |
| NXT eligibility | **not found** (only the `mrkt_div_code` NJ empty-array behaviour) | — | not found |
| Par value | `fcam` **String**(14) "1주의 액면가입니다." | M3 | field table (REST) |
| Listed shares | `lstn_stcn` Number(19) "이 종목이 발행해 상장된 총 주식 수입니다." | M3 | field table (REST) |
| Base price | `sdpr` Number(13) "당일 기준가(전일 종가)" | M3 | field table (REST) |
| Price limits | `mxpr` "당일 주문 가능한 최고 가격(상한가)입니다." / `llam` "…최저 가격(하한가)입니다." | M3 | field table (REST) |
| Other | `sltr_yn` 정리매매여부 "Y"/"N"; `crdt_able_yn` 신용가능여부; `ssts_yn` 공매도여부; `marg_rate` 증거금비율 (String 9); `elw_pblc_yn` (may be empty) | M3 | field table (REST) |

### 7.6 Freshness and staleness

- **Cadence (documented):** M1 L11 "종목정보 파일은 매 영업일 자동으로
  갱신됩니다."; L2254 "종목정보 파일은 매 영업일 자동 갱신되며, 최종 업데이트
  일시는 서버 파일 기준으로 표시됩니다."
- **As-of shown on the page only:**
  - "최종 업데이트" KOSPI "2026.11.05 08:53", KOSDAQ "2026.11.05 08:53",
    해외 "2026.11.05 10:15" (M1 L2177–2179, L2207–2209, L2237–2239). The zone is not stated.
    **Inference:** KST, because 08:53 UTC was still in the future at the
    07:21Z retrieval.
  - The update time of day is not documented as a schedule.
- **As-of in the file or headers:** none documented. The file name carries no
  date. The download response has no `Last-Modified`/`ETag` and is `no-store`
  (observed).
- **Staleness detection:** not documented. **Inference:** the only signals are
  the page's HTML "최종 업데이트" text and the client's own fetch time. A
  content hash detects change, not staleness.

### 7.7 Data rights and redistribution

M2 FAQ (L35) says "시세 데이터를 활용한 비즈니스 서비스 제공 또는 외부
서비스(앱) 배포는 불가능합니다"; whether the symbol master counts as 시세 데이터
is not documented. M6 `LICENSE` (MIT) covers the repository only, and the
`.mst` files are not in it. The files are never committed or quoted (header
caution; G-R1).

### 7.8 Contradictions and inferences

1. **"Column spec in API 문서" vs no spec anywhere.** M1 L2255 defers to the
   API documentation, but M3, M4, M5 and M6 contain none (§7.1).
   - Consequence: **no decoder** until a publisher column spec is found and
     pinned. The byte observations in §7.2 must not become a layout.
2. **Inventory under-reported the file set.** The capability inventory lists
   only `kospi`/`kosdaq`. M1 also offers `exst` (overseas) and an `all` zip.
   Neither is in domestic scope.
3. **Mixed universes in the KOSPI file.** The file is labelled "국내주식(코스피)
   종목코드 및 기본정보". It contains `F`-prefixed (M2: 수익증권), `J`-prefixed
   (M2: ELW) and `Q`-prefixed codes (meaning undocumented). The KOSDAQ file
   has none of these.
   - **Inference:** the KOSPI file is a broader product list.
   - Consequence: equity filtering needs a documented type column. It must
     not rely on code-shape heuristics.
4. **`shrn_iscd` "6자리" vs length 9.** The REST output is declared String(9)
   while described as six digits. The file code region is also 9 bytes
   (inference).
   - **Inference:** 9 bytes accommodate the `F`/`J` 9-character codes.
5. **Unregistered codes succeed.** REST `iscd` returns `"0000"` with empty or
   zero values for unknown, ISIN or lower-case codes (M3).
   - Consequence: a REST probe cannot validate master membership. Absence of
     `shrn_iscd` is the documented check.
6. **Encoding.** The encoding is undocumented. CP949 and EUC-KR both decode
   these copies; they differ for extension characters.
   - Consequence: the encoding must be pinned by the publisher before names
     are decoded. A wrong choice risks silent mojibake.
7. **Rate-limit wording conflicts** (REST, not the file). The FAQ says
   "모든 REST API(주문, 잔고조회, 시세조회 등) 합산하여 1초당 10건". The repo
   (`docs/errors.md` L95, candle audit §7.6) says "API 당 초당 10건". This
   matters for any REST enrichment of ~4,400 rows.
8. **Different record widths.** KOSPI is 118 bytes and KOSDAQ 116 bytes
   (observed). One fixed layout for both files must not be assumed.

## 8. Cross-broker comparison

### 8.1 Delivery and access

| Broker | Mechanism | Auth | Completeness / paging | Encoding / format | Evidence |
| --- | --- | --- | --- | --- | --- |
| KIS | public zip file per market | none (K7, K8) | whole file | cp949, fixed width; 288-byte KOSPI records | H+C+O |
| Kiwoom REST | REST per `mrkt_tp` | bearer token | `cont-yn`/`next-key`; page size not documented | JSON | F+E |
| LS | REST per `gubun` (t8436, t8430, t9945) | bearer token; `mac_address` header listed | `tr_cont`/`tr_cont_key` exist; whether the master pages is not documented | JSON | F+E |
| DB | REST `JCODES` per selector | bearer token; `mac_address` header listed | `cont_yn`/`cont_key`; "연속키 조회를 통해 종목을 추가로 조회" | JSON | F+E+P+C |
| Toss | REST `/stocks/all` per market + `/stocks` detail | bearer token | "페이지네이션 없이 한 번에"; detail ≤200 per call | JSON | F |
| Meritz | public `.mst` file per market | none documented; one anonymous 200 observed | whole file | fixed-width bytes; encoding and columns **not documented** | P+O |

### 8.2 Identifier and type mapping

| Concern | KIS | Kiwoom REST | LS | DB | Toss | Meritz |
| --- | --- | --- | --- | --- | --- | --- |
| Short code | 9-byte field; 6-, 7- and 9-char codes observed | `code` "단축코드" | `shcode` String 6 | `Iscd` length 9 | `symbol`, no response pattern | undocumented (9-byte region observed) |
| Standard code | `stnd_iscd` 12 | none | `expcode` 12 | `StndIscd` 12 | `isinCode` | undocumented (ISIN-shaped bytes observed) |
| English name | none | none | none | none | `englishName` (detail only) | none documented |
| Alphanumeric short codes | observed | not documented | not shown | publisher example | documented | observed |
| Market | file per market | `mrkt_tp`; response code list missing | `gubun` 1/2 (t9945: request only) | `MrktClsCode` contradicted by example | request `market` only | file per market |
| ETF / ETN | `scrt_grp_cls_code` + `etp_prod_cls_code` | `mrkt_tp` 8 / 60 / 70 / 90 | t8436 `etfgubun`, `bu12gubun` | selector `E` / `EN`, `MrktClsName` | `securityType` | not documented |
| Preferred | `prst_cls_code` | none | none (example preferred row is `01`) | none | `isCommonShare` (meaning for non-stock undocumented) | not documented |
| SPAC | `etpr_undt_objt_co_yn` | none | `spac_gubun` | none | none | not documented |
| Halt / admin / warning | `trht_yn`, `mang_issu_yn`, `mrkt_alrm_cls_code` | free-text `state`; `orderWarning` | not in the master | not in the master | halt flags (detail); warnings route | not in the master (REST only) |
| NXT eligibility | none | `nxtEnable` | t9945 `nxt_chk` | selector `NJ`/`UJ` only | `nxtSupported` (detail) | none |
| Listing date | `stck_lstn_date` | `regDay` | separate TR t1403 | none | `listDate`, `delistDate` | none |
| Shares | `lstn_stcn` (천주) | `listCount` (1주) | not in the master | none | `sharesOutstanding` "발행주식수" | not in the master |
| Tick / lot | lot only | neither | lot (`memedan`) only | neither | neither | not in the master (REST only) |
| Freshness | not documented | not documented | not documented | not documented | "일 배치" | "매 영업일 자동으로 갱신" |

**Reading 8.2:**

- The short code is the only identifier every broker exposes, and even its
  form differs (6 to 9 characters, prefixed or suffixed native variants).
- A 12-character standard code is documented by KIS, LS, DB and Toss.
  Kiwoom has none, and Meritz has none documented.
- Only Toss documents an English name.
- No two brokers share a type taxonomy.
- NXT eligibility exists in four different forms (Kiwoom flag, LS flag,
  DB selector, Toss detail flag) and not at all in KIS or Meritz.
- Only Toss and Meritz document an update cadence, and neither gives an
  as-of field in the payload or file.

### 8.3 Agreements and contradictions between broker sections

1. **Alphanumeric six-character codes are real.** They are observed in the
   KIS and Meritz files, shown in a DB example and documented by Toss. LS
   and Kiwoom master docs neither show nor exclude them. All four positive
   sources conflict with the v0.1 six-digit rule (G-I1).
2. **ETN codes.** KIS (`EN` group) and Meritz (KOSPI file) both contain
   7-character "letter + 6 digits" codes. Kiwoom documents `Q` + 6 digits
   for ETNs on account routes. Toss documents **no** `Q`-prefixed form.
   **Inference:** the KIS and Meritz 7-character codes are the same
   prefixed ETN form; not documented by either.
3. **"KOSPI" files are not equity-only.** Both the KIS and the Meritz KOSPI
   files contain ETF, ETN and other product codes. Toss and DB instead
   split ETF/ETN by type or selector. A market label alone never implies
   "stock".
4. **Record counts differ.** The KIS KOSPI file had 2,569 records and the
   Meritz KOSPI file 2,560 on the same day. **Inference:** different
   inclusion rules or snapshot times; not documented by either.
5. **Prefix conventions conflict.** Kiwoom documents `A`/`J`/`Q` prefixes
   (stock/ELW/ETN) on account routes. Meritz documents `A`/`F`/`J`
   (stock/수익증권/ELW) for orders. DB uses `N-`/`U-` for venues on quote
   routes. None of these prefixes may enter the canonical symbol (G-I3).
6. **DB market code vs LS.** DB's field table says `MrktClsCode` `1` =
   코스닥; its own example puts `000020` under `1`/"거래소", and LS's
   example lists the same code under `gubun` `1` = 코스피 (§5.8 item 1).
7. **Listed vs issued shares.** KIS counts listed shares in thousands,
   Kiwoom in shares, and Toss gives issued shares ("발행주식수"). These are
   not interchangeable.
8. **Capability inventory routes.** LS's FAQ names `t8430`, the inventory
   names `t8436` (§4.8 item 1). Meritz offers `exst` and `all` files beyond
   the inventory's two (§7.8 item 2).

## 9. Relation to existing repository documents

None of the files below is edited by this change.

| Document and claim | This audit |
| --- | --- |
| [kis-market-data.md](kis-market-data.md) L29: `load_markets` "publisher's `stocks_info` reference; no confirmed REST contract" | **Confirmed**: file download only, layouts K4–K6, no REST route found |
| kis-market-data.md L67: "Market master coverage, refresh cadence, permitted local caching and redistribution license are still unverified" | Coverage now documented (§2.3). Cadence, caching and licence remain **not documented** (§2.6, §2.7) |
| [kiwoom-market-data.md](kiwoom-market-data.md) L29: `load_markets` "no selected authoritative endpoint/master mechanism yet" | Candidates found: `ka10099`/`ka10100` `POST /api/dostk/stkinfo` (§3.2). Selection is still a maintainer decision |
| kiwoom-market-data.md L70: "Market master list API/licensing and any data redistribution conditions" | API documented; data terms **not documented**; W6 restricts the software/docs (§3.7) |
| [capability-matrix-v0.1.json](../specifications/capability-matrix-v0.1.json) KIS `load_markets` evidence URL on `main`; Kiwoom `load_markets` evidence = portal guide | Superseded for master work by the pinned sources here |
| [six-broker-common-surface.md](six-broker-common-surface.md) L72–80: six-digit numeric draft must not be universal; `0101N0`-style codes exist (Toss) | **Consistent** and extended: KIS, DB and Meritz also carry alphanumeric codes (§8.3 item 1) |
| [market-data spec §3](../specifications/market-data-v0.1-draft.md) L60: v1 symbol "exactly six ASCII digits" | Excludes codes documented or observed at four brokers (§8.3 item 1; G-I1) |
| [ADR 0013](../decisions/0013-public-fetch-ticker-surface.md) L37 (on `main` `03680cd6`): `fetch_ticker` `symbol` "must be exactly six ASCII digits (`InvalidSymbol`)" | The same constraint now exists in public code. A `load_markets` result containing alphanumeric codes would list symbols that `fetch_ticker` rejects (G-I1) |
| market-data spec §8: "Define `load_markets` master sources, cache invalidation, session/venue listing, and data rights" | Sources recorded for all six brokers; cache, venue and rights remain open (§10) |
| Capability inventory (branch `claude/issue-17-capability-inventory`, unmerged) row 5: KIS `kospi`/`kosdaq` files; Kiwoom `ka10099`; LS `t8436`; DB `JCODES`; Toss `/stocks/all`; Meritz `kospi`/`kosdaq` files | **Confirmed**, plus KIS `konex`, Kiwoom `ka10100`, LS `t8430`/`t9945`, Toss `/stocks` detail and Meritz `exst`/`all` |
| Candle audit (branch `claude/issue-17-candle-evidence`, unmerged): Kiwoom pin `953e5dbf` | Equivalent tree to `c7a3d254` (§3.1); its Kiwoom blobs remain valid |

## 10. Implementation gates for `load_markets`

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any `load_markets` code is written. Broker
tags are in brackets.

### 10.1 Canonical identifier

- **G-I1 Symbol grammar:** v0.1 (spec §3, ADR 0013) accepts only six ASCII
  digits. Alphanumeric six-character codes are observed in [KIS] (including
  common shares) and [Meritz], shown in a [DB] example and documented by
  [Toss]. Decide, by ADR, between widening to six ASCII upper-alphanumerics
  or keeping digits and **reporting** the rest as unsupported. Never drop,
  pad, lower-case or truncate silently.
- **G-I2 No lossy normalisation:** never apply [KIS] K7's `code[-6:]`
  truncation or digit-only filter. Keep the native short code verbatim
  next to the canonical symbol.
- **G-I3 Native forms:** [Kiwoom] `_NX`/`_AL` suffixes and `A`/`J`/`Q`
  prefixes, [DB] `N-`/`U-` prefixes and [Meritz] `A` order prefix are
  route-specific encodings. Map them per endpoint and never treat them as
  part of the symbol.
- **G-I4 Standard code:** documented by [KIS], [LS], [DB] and [Toss]; absent
  in [Kiwoom]; undocumented in [Meritz]. Do not make it mandatory in the
  cross-broker model or synthesise it.
- **G-I5 Names are not keys:** [LS] `hname` is String 20 in t8430/t8436 and
  40 in t9945; [Toss] `englishName` can be missing from an example despite
  being required. Treat names as display data; a missing name is unknown,
  never `""`.

### 10.2 Venue and market mapping

- **G-V1 Market segment ≠ execution venue:** KOSPI/KOSDAQ/KONEX are listing
  segments; KRX/NXT are venues (spec §3). [Toss] `market` is explicitly a
  segment. Store both and do not derive one from the other.
- **G-V2 Out-of-scope or undefined markets:** [Kiwoom] `mrkt_tp` `30`
  K-OTC and `80` 금현물, and [Toss] `KR_ETC`, stay excluded from v0.1. Never
  coerce them into `KRX`.
- **G-V3 Market codes needing fixtures:** [DB] `MrktClsCode`/`MrktClsName`
  must not be mapped to KOSPI/KOSDAQ until a fixture resolves §5.8 item 1;
  [Kiwoom] response `marketCode` has no code list; [LS] t9945 carries the
  market only through the request.
- **G-V4 NXT eligibility:** documented as [Kiwoom] `nxtEnable` ("Y: 가능"
  only), [LS] t9945 `nxt_chk` 1/0 and [Toss] `nxtSupported` (detail route).
  [DB] `NJ`/`UJ` is a selector with undocumented semantics. [KIS] and
  [Meritz] have none. A missing flag is "unknown", never "not eligible",
  and never permission to route to NXT. [Toss] `nxtTradingSuspended: null`
  means "NXT not supported", not "not suspended".

### 10.3 Instrument-type taxonomy

- **G-T1 Taxonomy:** define a closed KTradeLink type set (common, preferred,
  ETF, ETN, ELW, REIT, SPAC, fund, warrant, DR, foreign, other) with an
  explicit `UNKNOWN(raw)` member.
- **G-T2 Undocumented codes stay unknown:** [KIS] `EN`, `PF`,
  `etp_prod_cls_code` space/`8`/`9`, `prst_cls_code` `9`; [LS]
  `etfgubun`/`etfchk` `"0"` and unlisted `bu12gubun` values; [Toss]
  unknown `securityType`, `Currency` or `warningType` values (the publisher
  says to tolerate them) map to `UNKNOWN(raw)`.
- **G-T3 Free text:** [Kiwoom] `state`, `auditInfo` and `orderWarning` `5`,
  and [Meritz] REST `invt_epmd_cntt`, must not be parsed into halt/warning
  booleans without a documented vocabulary.
- **G-T4 Overlap and dedup:** [Kiwoom] codes under several `mrkt_tp` values
  and [DB] `J` vs `E`/`EN` (the `J` example contains ETFs) are undocumented
  overlaps. De-duplicate by a documented key and fail loudly on conflicts.
- **G-T5 Preferred shares:** documented only by [KIS] `prst_cls_code` and
  [Toss] `isCommonShare` (its meaning for non-stock types is undocumented).
  [Kiwoom], [LS] and [DB] have no discriminator; never infer preferred from
  the name or code shape.
- **G-T6 No shape heuristics:** [KIS] and [Meritz] KOSPI files mix ETF,
  ETN, 수익증권 and warrants with shares. Filtering by code shape is
  forbidden; use documented type fields only.

### 10.4 File parsing (file-delivered masters)

- **G-F1 TLS:** never disable TLS verification and never copy
  `ssl._create_unverified_context` ([KIS] K1–K3, K8). If verification fails
  at the origin, the source is unavailable; there is no fallback.
- **G-F2 Bytes, not characters:** slice fixed-width records in bytes at the
  published widths; decode only text fields with the documented encoding.
  Reject records of unexpected length.
- **G-F3 Layout versioning:** pin layouts to a publisher blob SHA. Fail on
  a width mismatch instead of shifting fields. [Meritz] KOSPI and KOSDAQ
  record widths differ (118 vs 116 bytes, observed).
- **G-F4 Untrusted archive:** treat downloaded files and zips as untrusted
  (member names, member count, size limits; no extraction outside a temp
  directory).
- **G-F5 [Meritz] blocked:** no `.mst` decoder until the publisher column
  specification and encoding are found and pinned. The byte observations in
  §7.2 are leads, not a layout.

### 10.5 Caching and invalidation

- **G-C1 Snapshot identity:** record source URL or route, retrieval time,
  size and sha256 (file) or page count (REST) with each master snapshot.
- **G-C2 Freshness:** [Toss] "일 배치로 갱신 … 하루 1회 조회 후 로컬 캐싱을
  권장" and [Meritz] "매 영업일 자동으로 갱신" give a cadence but no as-of
  field; [KIS], [Kiwoom], [LS] and [DB] document neither. Any refresh
  policy is a KTradeLink choice and must be labelled as such.
- **G-C3 Completeness:** [Kiwoom] page until `cont-yn` ≠ `Y`; [LS] treat
  the master as complete only when `tr_cont` is `N` or empty; [DB] loop on
  `cont_yn` = `Y`. A page cap, an empty or repeated continuation key must
  raise, not truncate (unlike [Kiwoom] W3 `MAX_PAGES = 10` and [DB] D5
  `_PAGED_SAFETY_CAP = 100`, which warn and return partial data).
- **G-C4 Empty or short results never replace a cache:** [DB] documents
  success code `00000` with "모의투자 데이터가 없습니다."; [LS] documents its
  success code only in examples. A sharply shorter list is an error.
- **G-C5 Units:** [KIS] listed shares are thousands; [Kiwoom] are shares;
  [Toss] gives issued shares. Normalise explicitly and keep the semantic.
- **G-C6 Daily-varying values:** [LS] `recprice`, `uplmtprice`,
  `dnlmtprice` and `jnilclose` have no as-of date or documented venue; do
  not expose them from a cached master as current values.
- **G-C7 Status filters:** [Toss] request `status=ACTIVE` explicitly; the
  `DELISTED`/`SCHEDULED` behaviour is undocumented.

### 10.6 No silent merging across brokers

- **G-M1:** each master is per broker. A cross-broker view needs an explicit,
  reviewed join rule (at least short code + market segment) and must report
  conflicts, never pick one broker's value silently.
- **G-M2:** a symbol absent from one broker's master is "not listed by that
  broker" (for example [Toss] "토스증권에서 거래 가능한 종목만"), not
  "delisted".
- **G-M3:** the six-broker common subset is short code + market segment
  only. ISIN, names and types cannot be common fields while [Kiwoom] lacks
  ISIN and [Meritz] has no column specification.

### 10.7 Data rights

- **G-R1:** no source grants storage or redistribution rights, and [Toss]
  and [Meritz] FAQs restrict distribution (§6.7, §7.7). Master content stays
  out of Git, fixtures and review material; fixtures are synthetic. Whether
  a local cache is permitted is a maintainer decision.
- **G-R2:** [Kiwoom] W6 forbids copying and distributing its software and
  documentation without consent. Do not vendor its spec JSON, postman
  collection or examples.

### 10.8 Network and credentials

- **G-N1 Authenticated masters:** [Kiwoom], [LS], [DB] and [Toss] masters
  need a bearer token. Even a read-only master load is an authenticated
  request requiring separate explicit authorization.
- **G-N2 Unauthenticated files:** [KIS] and [Meritz] downloads are still
  network access: never in CI, never implicit on import, explicit opt-in.
- **G-N3 `mac_address`:** listed by [LS] and [DB] (and [Meritz] REST). It
  must come from explicit configuration, never from host discovery, and
  must never be logged.
- **G-N4 Rates and retries:** [LS] 2 TPS, [DB] 3 TPS (app 20), [Toss]
  `STOCK_ALL` 1/s and `STOCK` 5/s with 429 headers, [Kiwoom] not documented
  for these routes. These are read-only `GET`/`POST` queries, but any
  retry policy is a separate, reviewed decision.
- **G-N5 [Meritz] REST enrichment is separate:** tick, lot, halt and limits
  exist only per symbol via `ohhts_1001_001r`, which needs a token and
  `mac_address`, and returns `"0000"` with empty values for unknown codes.
  It is not part of a v1 `load_markets`.

## 11. Not verified

- Any live or paper response for any master route. No broker API request
  was sent.
- [KIS] KOSDAQ, KONEX and ELW file contents (only the KOSPI file was
  downloaded, once); the origin TLS certificate of
  `new.real.download.dws.co.kr` (verified only through the session proxy);
  ownership of that host.
- [KIS] meaning of `EN`, `PF`, `etp_prod_cls_code` space/`8`/`9`,
  `prst_cls_code` `9`, `kospi_issu_yn` and `elw_pblc_yn`; units and signs of
  numeric tail fields.
- [Kiwoom] page size, row order, `marketCode` code list, `nxtEnable` values
  other than `Y`, `state`/`auditInfo` vocabularies, duplicate rows across
  `mrkt_tp`, whether alphanumeric codes are returned, and real/paper parity
  beyond the W2 listing.
- [LS] row counts, paging, KONEX presence, `nxt_chk` presence and the
  meaning of `etfchk`/`etfgubun` `0`; ELW masters (`t9942`, `t8431`) and
  t1102 per-symbol flags.
- [DB] actual `MrktClsCode`/`MrktClsName` values; the content of `NJ`, `UJ`,
  `E` and `EN`; KONEX rows; page size; whether `Iscd` ever carries
  prefixes; FAQ and notice content; `WCODES`.
- [Toss] any `/stocks/all` or `/stocks` response; `KR_ETC` membership;
  whether `DELISTED`/`SCHEDULED` rows are returned; batch time of day;
  freshness of the halt/NXT flags; whether ELW/SPAC/KONEX appear at all.
- [Meritz] column layout, encoding and record semantics of `.mst`; the
  `all` zip contents; whether the files ever need authentication; the time
  zone of "최종 업데이트" and whether the files change intraday; whether
  REST `iscd` accepts the alphanumeric or `Q`/`F`/`J` codes; the origin TLS
  certificate.
- Update cadence and as-of semantics wherever not quoted above; caching
  and redistribution rights for every broker (not researched further, by
  maintainer instruction).
