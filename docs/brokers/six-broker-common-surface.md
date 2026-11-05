# Initial six-broker common surface — evidence before abstraction

- **Research date:** 2026-11-02
- **Scope:** domestic-equity read-only market data, initially KRX.
- **Status:** publisher documentation survey, **not** a broker integration test
- **Targets:** KIS, Kiwoom REST, LS Open API, DB Open API, Toss Securities,
  Meritz Securities
- **Constraints:** the maintainer currently holds no connected test account,
  API key, or authenticated response fixture for these providers.

This survey is used to identify a *small provable intersection* of advertised
capabilities, not to claim that any KTradeLink adapter is implemented.

## Official endpoint / operation discovery

| Broker | Current price | Daily candles | Order book | Documentation |
| --- | --- | --- | --- | --- |
| KIS | `inquire-price`, `FHKST01010100` | `inquire-daily-itemchartprice`, `FHKST03010100` | `inquire-asking-price-exp-ccn`, `FHKST01010200` | [Official examples](https://github.com/koreainvestment/open-trading-api) |
| Kiwoom REST | `ka10001`, `/api/dostk/stkinfo` | `ka10081`, `/api/dostk/chart` | `ka10004`, `/api/dostk/mrkcond` | [Official examples](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) |
| LS Open API | `t1102` | `t8410` | `t1101` | [Official TR catalog](https://openapi.ls-sec.co.kr/apiservice) |
| DB Open API | `국내주식시세 > 현재가조회` | `국내주식/선물차트 > 일차트조회` | `국내주식시세 > 호가조회` | [Official API guide](https://openapi.db-fi.com/apiservice) |
| Toss Securities | `GET /api/v1/prices` | `GET /api/v1/candles` | `GET /api/v1/orderbook` | [Official Open API spec](https://developers.tossinvest.com/llms.txt) |
| Meritz Securities | `GET /market/v1/prices` | `GET /market/v1/candles/days` | `GET /market/v1/orderbook` | [Official Python sample](https://openapi.imeritz.com/samplecode-py) |

**Important:** an official catalog entry confirms *feature discovery*, not
that it uses identical units, adjustment conventions, sessions, timestamps,
exchange scope, rate limits, data rights, or entitlements. DB method paths and
native TR codes are left **unverified** until the corresponding official detail
view is captured. No placeholder endpoint should be called in code.

## Native field names confirmed in publisher examples

| Meaning | KIS `inquire-price` | Kiwoom `ka10001` | Meritz `/market/v1/prices` |
| --- | --- | --- | --- |
| Last reported price | `stck_prpr` | `cur_prc` | `stck_prpr` |
| Open | `stck_oprc` | `open_pric` | `oprc` |
| High | `stck_hgpr` | `high_pric` | `hprc` |
| Low | `stck_lwpr` | `low_pric` | `lprc` |
| Volume | `acml_vol` | `trde_qty` | `acml_vol` |

Evidence:
- [KIS field mapping in publisher test sample](https://github.com/koreainvestment/open-trading-api/blob/main/examples_llm/domestic_stock/inquire_price/chk_inquire_price.py)
- [Kiwoom stock-information publisher example](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_info.py)
- [Meritz current-price publisher sample](https://openapi.imeritz.com/samplecode-py)

**Historical snapshot:** When this initial survey was written, LS, DB and
Toss field-level mappings were still unconfirmed. The [follow-up evidence
ledger](six-broker-ticker-decoders.md) now records publisher-sourced examples:
LS t1102OutBlock (ADR 0010; gateway unverified), DB Out.Prpr and
Toss result[].lastPrice. These are only offline decoder candidates,
not verified broker adapters. Market, session and volume scope remain
unverified.

## Intersection and initial implementation decision

1. All six publishers **advertise a domestic equity current-price operation**;
   it is the first candidate unified method.
2. Start with a Python-native immutable `Ticker` value type based on
   `symbol`, `venue`, `broker`, `last` and clearly optional quote fields.
   It is a **value model**, not a working six-broker adapter.
3. Use `Decimal` prices and optional fields to avoid inventing absent quote
   values. Do not imply that a quote must have a verified exchange event time.
4. Defer per-broker decoding, sign normalization and timestamp construction
   until official response samples for each source field exist.
5. A six-broker coverage matrix must distinguish `documented_candidate`
   from `implemented`, `verified`, and `supported`; currently only the
   first status is justified.
6. Defer `Candle` and `OrderBook` runtime models to additional common-field
   comparison before implementing decoders.

## Instrument identifier qualification

The Phase 01 first-scope draft proposed six **numeric** digits. Toss's
publisher reference allows a six-character KR symbol with ASCII alphanumeric
codes (for example, `0101N0`) in addition to all-numeric codes. As a result,
the general-purpose `Ticker` value model must **not** reject every
non-numeric symbol purely on the basis of that first two-broker draft.

Broker request validation will require a separate stock-master and asset-class
decision; accepting a symbol in a value model does **not** mean an adapter
supports querying or trading it.

## Accountless verification policy

- Official catalog and publisher examples: **documentary evidence only**.
- Generated values: explicitly **synthetic**, no actual financial data.
- Contract tests: check model typing, null-vs-zero, immutable provenance,
  source metadata and exclusion of unknown fields.
- Real/paper account integration and rate limit/paging assertions: **not run**.
- No broker API credentials must be committed, requested in chat, or copied to
  independent Gemini review packets.

## Follow-up source checks per broker

- LS, DB and Toss: identify *actual current-price response keys* and precise
  quote-market scope using downloadable source specifications, not analogies.
- KIS, Kiwoom and Meritz: verify signed numeric strings, empty fields, native
  time fields and market source with authorized sanitized examples.
- All six: verify session semantics, last trade vs reference price, effective
  limits, data caching/redistribution terms, and real vs paper availability.

For general project scope changes, coordinate with any other open roadmap PR
before editing or merging scope documents; this PR does not modify other PRs.
