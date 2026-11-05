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
  documentation pages and — for KIS only — one unauthenticated download of
  one public master file (§2.2) were fetched.
- **Retrieval, all on 2026-11-05 UTC:**
  - KIS: Git objects fetched 07:21–07:24 from `github.com` at the pinned
    SHA. The public KOSPI master zip was downloaded once at 07:29:11.
  - Kiwoom: Git objects fetched 07:25–07:27 at the pinned SHA, plus the
    earlier pin by SHA for the tree comparison in §3.1.
  - LS, DB, Toss, Meritz: pending (§4–§7).
- **Pin formats:**
  - Git: repository, full commit SHA and commit date; per file the Git blob
    SHA, i.e. `sha1("blob <len>\0" + bytes)`, what `git hash-object`
    prints, with a blob link at the commit.
  - Web pages have no immutable revision. Their sha256 prefix identifies
    only the copy retrieved at the stated time.
  - A downloaded master file is pinned by URL, retrieval time, byte size and
    sha256. **The file is not committed and no row, name or individual code
    from it is quoted**; only aggregate properties are recorded (§2.2).
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
  - `file observation`: aggregate-only properties of **one** downloaded copy
    (byte length, encoding, record count, distinct values of coded fields,
    code *shapes*). One snapshot; not a contract and not a cadence.
  - `not found`.
- Every inference is marked **Inference:**. "Not documented" means the pinned
  sources say nothing about it.
- **Data-rights caution:** no pinned source grants a right to store, cache
  or redistribute master content (§2.7, §3.7). Until the maintainer records
  a decision (G-R1), master content must not enter Git, fixtures, issues,
  logs or review material, and sample values in publisher examples are
  **not** authorized fixtures.

## 1. Broker × property summary

Evidence: `F` field table, `H` publisher layout header, `E` publisher
example, `C` publisher client code, `N` publisher repo note, `O` file
observation, `—` not found. `pending`: section not yet merged.

| Broker | Delivery | Venues / markets | Instrument types distinguished | Identifiers (short / standard / names) | Alphanumeric short codes | Trading attributes | NXT flag | Freshness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KIS | file: `kospi_code.mst.zip` / `kosdaq_code.mst.zip` / `konex_code.mst.zip` on `new.real.download.dws.co.kr`, zipped fixed-width cp949, no auth — H+C+O; publisher code disables TLS verification (unsafe) | one file per KRX market (유가증권 / 코스닥 / 코넥스); ELW in a separate file — H+C; NXT, K-OTC — | `scrt_grp_cls_code` (ST, EF, RT, DR, SW, …), `etp_prod_cls_code`, `prst_cls_code` — H; undocumented values `EN`, `PF` and others observed — O | 9-byte short code, 12-char standard code, 40-byte Korean name; no English name — H+C+O | **yes** — O (6-char mixed in `ST`, `EF`, `RT`, `PF`; 7- and 9-char codes in other groups) | 기준가, lot units, 거래정지, 정리매매, 관리, 시장경고, listing date, par value, listed shares (천주) — H; no tick size, no delisting date | — | not documented; one observation of HTTP `Last-Modified` (§2.6) — O; publisher MCP client refreshes once per calendar day — C |
| Kiwoom REST | REST `POST /api/dostk/stkinfo` `ka10099` (by `mrkt_tp`), `ka10100` (one code); `cont-yn`/`next-key` — F+E | 16 `mrkt_tp` codes incl. 코스피, 코스닥, 코넥스, K-OTC, 금현물 — F; response `marketCode`/`marketName` without code list — F | by request `mrkt_tp` only (ETF, ETN ×3, ELW, 리츠, 인프라, 뮤추얼, 신주인수권 …) — F; no preferred/SPAC field | `code` "단축코드" only; no standard code; no English name — F | not documented for these routes; other routes use `A`/`J`/`Q` + 6 digits — F | `listCount` (1주), `regDay`, `lastPrice`, free-text `state`/`auditInfo`, `orderWarning` codes — F; no tick, lot or delisting | `nxtEnable` "Y: 가능" — F | not documented |
| LS | pending | pending | pending | pending | pending | pending | pending | pending |
| DB | pending | pending | pending | pending | pending | pending | pending | pending |
| Toss | pending | pending | pending | pending | pending | pending | pending | pending |
| Meritz | pending | pending | pending | pending | pending | pending | pending | pending |

## 2. KIS (Korea Investment & Securities)

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
| ELW | separate file `elw_code.mst.zip` (K8 L237; not analysed here). In the KOSPI file `elw_pblc_yn` "ELW 발행여부 (Y/N)" (K4 L34). **Inference:** this flags an ELW *underlying*, not an ELW row. | K4, K8 | layout header / client code |
| Index membership | KOSPI100/50/200 sector, KRX100/300, KOSDAQ150, `kospi_issu_yn` "KOSPI여부" (K4 L87) — meaning of "KOSPI여부" not documented | K4, K5 | layout header |

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

## 3. Kiwoom REST

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
- W6 governs "본 소프트웨어 및 관련 문서 파일" (§1), limits use "키움증권
  OpenAPI 서비스를 이용하기 위한 목적에 한하여" (§2), and forbids, "회사의 사전
  서면 동의 없이", "본 소프트웨어의 복제, 배포, 전송, 출판" and "수정, 2차적
  저작물 작성" (§3).
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

## 4. LS Securities

_Pending — section to be merged from the LS/DB research._

## 5. DB Securities

_Pending — section to be merged from the LS/DB research._

## 6. Toss Securities

_Pending — section to be merged from the Toss/Meritz research._

## 7. Meritz Securities

_Pending — section to be merged from the Toss/Meritz research._

## 8. Cross-broker comparison

LS, DB, Toss and Meritz columns are pending.

### 8.1 Delivery and access

| Broker | Mechanism | Auth | Paging | Encoding / format | Evidence |
| --- | --- | --- | --- | --- | --- |
| KIS | public zip file per market | none (K7, K8) | whole file | cp949 fixed-width, 288-byte KOSPI records | H+C+O |
| Kiwoom REST | REST per `mrkt_tp` | bearer token | `cont-yn`/`next-key`; size not documented | JSON | F+E |

### 8.2 Identifier and type mapping

| Concern | KIS | Kiwoom REST |
| --- | --- | --- |
| Short code | 9-byte field; 6-, 7- and 9-char codes observed | `code` "단축코드"; format not documented |
| Standard code | 12-char `stnd_iscd` | none |
| English name | none | none |
| Market | file per market | request `mrkt_tp`; response `marketCode` without code list |
| ETF / ETN | `scrt_grp_cls_code` `EF` + `etp_prod_cls_code` | `mrkt_tp` `8` / `60` / `70` / `90` |
| Preferred | `prst_cls_code` 0/1/2 (+ undocumented 9) | none |
| SPAC | `etpr_undt_objt_co_yn` | none |
| Halt / admin / warning | `trht_yn`, `mang_issu_yn`, `mrkt_alrm_cls_code` | free-text `state`/`auditInfo`; `orderWarning` |
| NXT eligibility | none | `nxtEnable` |
| Listed shares unit | thousands (`lstn_stcn` "(천)") | 1주 (`listCount`) |
| Tick / lot | lot units only; no tick | neither |

**Reading 8.2:** the two brokers share no identifier beyond the short code.
They use different type taxonomies (security-group code vs request market
code), different listed-share units, and one has an NXT flag while the other
has none. A cross-broker merge would need an explicit join rule (G-M1).

## 9. Relation to existing repository documents

None of the files below is edited by this change.

| Document and claim | This audit |
| --- | --- |
| [kis-market-data.md](kis-market-data.md) L29: `load_markets` "publisher's `stocks_info` reference; no confirmed REST contract" | **Confirmed**: file download only, layouts K4–K6, no REST route found |
| kis-market-data.md L67: "Market master coverage, refresh cadence, permitted local caching and redistribution license are still unverified" | Coverage now documented (§2.3). Cadence, caching and licence remain **not documented** (§2.6, §2.7) |
| [kiwoom-market-data.md](kiwoom-market-data.md) L29: `load_markets` "no selected authoritative endpoint/master mechanism yet" | Candidates found: `ka10099`/`ka10100` `POST /api/dostk/stkinfo` (§3.2). Selection is still a maintainer decision |
| kiwoom-market-data.md L70: "Market master list API/licensing and any data redistribution conditions" | API documented; data terms **not documented**; W6 restricts the software/docs (§3.7) |
| [capability-matrix-v0.1.json](../specifications/capability-matrix-v0.1.json) KIS `load_markets` evidence URL on `main`; Kiwoom `load_markets` evidence = portal guide | Superseded for master work by the SHA-pinned sources here |
| [six-broker-common-surface.md](six-broker-common-surface.md) L72–80: six-digit numeric draft must not be universal; `0101N0`-style codes exist (Toss) | **Consistent.** The KIS master contains alphanumeric 6-character `ST` codes (§2.4) |
| [market-data spec §3](../specifications/market-data-v0.1-draft.md): v1 symbol "exactly six ASCII digits" | Excludes some KRX common shares observed in the KIS master (§2.4; G-I1) |
| market-data spec §8: "Define `load_markets` master sources, cache invalidation, session/venue listing, and data rights" | Sources recorded for KIS and Kiwoom; cache, venue and rights remain open (§10) |
| Capability inventory (branch `claude/issue-17-capability-inventory`, unmerged): KIS file `kospi_code.mst.zip` / `kosdaq_code.mst.zip`; Kiwoom `ka10099` `POST /api/dostk/stkinfo` | **Confirmed**, plus `konex_code.mst.zip` and `ka10100` |
| Candle audit (branch `claude/issue-17-candle-evidence`, unmerged): Kiwoom pin `953e5dbf` | Equivalent tree to `c7a3d254` (§3.1); its Kiwoom blobs remain valid |

## 10. Implementation gates for `load_markets`

These must be decided by the maintainer, or verified with authorized and
sanitized fixtures, **before** any `load_markets` code is written. Broker
tags are in brackets.

### 10.1 Canonical identifier

- **G-I1 Symbol grammar:** v0.1 accepts only six ASCII digits. [KIS] lists
  common and preferred shares with alphanumeric six-character codes. Decide
  between widening to six ASCII upper-alphanumerics or keeping digits and
  raising an explicit `UnsupportedCapability` for the rest. Never drop,
  pad or truncate silently.
- **G-I2 No lossy normalisation:** never apply K7's `code[-6:]` truncation
  or digit-only filter. Keep the native short code verbatim next to the
  canonical symbol.
- **G-I3 Native forms:** [Kiwoom] plain, `_NX`/`_AL`-suffixed and
  `A`/`J`/`Q`-prefixed forms are route-specific encodings. Map them per
  endpoint and never treat a suffix or prefix as part of the symbol.
- **G-I4 Standard code:** only [KIS] supplies a 12-character standard code.
  Do not make it mandatory in the cross-broker model or synthesise it.

### 10.2 Venue and market mapping

- **G-V1 Market segment ≠ execution venue:** KOSPI/KOSDAQ/KONEX are listing
  segments; KRX/NXT are venues (spec §3). Store both and do not derive one
  from the other.
- **G-V2 Out of scope markets:** [Kiwoom] `mrkt_tp` `30` K-OTC and `80`
  금현물 are not KRX equities. Exclude them from v0.1, never coerce them
  into `KRX`.
- **G-V3 NXT eligibility:** only [Kiwoom] documents a flag (`nxtEnable`,
  "Y: 가능" only). [KIS] has none. Absence of a flag is "unknown", never
  "not eligible", and never permission to route to NXT.

### 10.3 Instrument-type taxonomy

- **G-T1 Taxonomy:** define a closed KTradeLink type set (common, preferred,
  ETF, ETN, ELW, REIT, SPAC, fund, warrant, DR, foreign, other) with an
  explicit `UNKNOWN(raw)` member.
- **G-T2 Undocumented codes:** [KIS] `EN`, `PF`, `etp_prod_cls_code`
  space/`8`/`9`, `prst_cls_code` `9` map to `UNKNOWN(raw)` until a source
  documents them.
- **G-T3 Free text:** [Kiwoom] `state`, `auditInfo` and `orderWarning` `5`
  must not be parsed into halt/warning booleans without a documented
  vocabulary.
- **G-T4 Overlap:** [Kiwoom] whether one code appears under several
  `mrkt_tp` values is undocumented. Detect duplicates and fail loudly rather
  than keep the first.

### 10.4 File parsing (file-delivered masters)

- **G-F1 TLS:** never disable TLS verification and never copy
  `ssl._create_unverified_context`. If verification fails at the origin,
  the source is unavailable; there is no fallback.
- **G-F2 Bytes, not characters:** slice fixed-width records in bytes at the
  published widths; decode only text fields with the documented encoding.
  Reject records of unexpected length.
- **G-F3 Layout versioning:** pin layouts to a publisher blob SHA. Fail on
  a width mismatch instead of shifting fields.
- **G-F4 Untrusted archive:** treat downloaded zips as untrusted (member
  names, member count, size limits; no extraction outside a temp directory).

### 10.5 Caching and invalidation

- **G-C1 Snapshot identity:** record source URL or route, retrieval time,
  size and sha256 (file) or page count (REST) with each master snapshot.
- **G-C2 Freshness:** no broker here documents a cadence or as-of field.
  Any refresh policy (for example daily) is a KTradeLink choice and must be
  labelled as such, not as broker behaviour.
- **G-C3 Completeness:** [Kiwoom] page until `cont-yn` ≠ `Y`; a page cap
  must raise, not truncate (unlike W3 `MAX_PAGES = 10`).
- **G-C4 Units:** [KIS] listed shares are thousands; [Kiwoom] are shares.
  Normalise explicitly.

### 10.6 No silent merging across brokers

- **G-M1:** each master is per broker. A cross-broker view needs an explicit,
  reviewed join rule (at least short code + market segment) and must report
  conflicts, never pick one broker's value silently.
- **G-M2:** a symbol absent from one broker's master is "not listed by that
  broker", not "delisted".

### 10.7 Data rights

- **G-R1:** no source grants storage or redistribution rights. Decide
  whether a local cache is permitted, where it lives (never Git), and
  whether master content may appear in fixtures (default: no; synthetic
  rows only).
- **G-R2:** [Kiwoom] W6 forbids copying and distributing its software and
  documentation without consent. Do not vendor its spec JSON, postman
  collection or examples.

### 10.8 Network and credentials

- **G-N1:** [Kiwoom] `ka10099` needs a bearer token, so even a read-only
  master load is an authenticated request requiring separate authorization.
- **G-N2:** [KIS] downloads are unauthenticated but still network access:
  never in CI, never implicit on import. They require explicit opt-in.

## 11. Not verified

- Any live or paper response for `ka10099`/`ka10100`. No broker API request
  was sent.
- KIS KOSDAQ, KONEX and ELW file contents. Only the KOSPI file was
  downloaded, once.
- The origin TLS certificate of `new.real.download.dws.co.kr`. Verification
  succeeded only against the session proxy CA.
- Ownership of the download host and whether it is an official KIS
  distribution point beyond its use in publisher code.
- Update cadence, publication time and as-of semantics for every source.
- Meaning of KIS `EN`, `PF`, `etp_prod_cls_code` space/`8`/`9`,
  `prst_cls_code` `9`, `kospi_issu_yn` and `elw_pblc_yn`.
- Units and signs of KIS numeric tail fields (기준가, 액면가, 자본금, financials).
- Kiwoom page size, row order, `marketCode` code list, `nxtEnable` values
  other than `Y`, `state`/`auditInfo` vocabularies, duplicate rows across
  `mrkt_tp`, and whether alphanumeric codes are returned.
- Real/paper parity of both Kiwoom routes beyond their listing in W2.
- Redistribution, caching and display rights for every broker.
- LS, DB, Toss and Meritz: pending (§4–§7).
