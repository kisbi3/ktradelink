# ADR 0003: Daily Candle and typed OrderBook value contracts

- Date: 2026-11-02
- Status: Proposed implementation contract; independent review required
- Base: PR #7 merged at ec190643f549371b80c5f9e09a1a1318370f4f1a
- Scope: in-memory domestic-equity values only; no broker calls or decoders

## Evidence inspected before implementation

These are publisher documents/examples, NOT authenticated response fixtures.
Source field names establish candidates, not identical trading-session semantics.

| Publisher | Candle evidence | Book evidence | Limits of this check |
| --- | --- | --- | --- |
| KIS | Official daily-chart check sample lists stck_bsop_date, stck_oprc, stck_hgpr, stck_lwpr, stck_clpr, acml_vol | Previously mapped FHKST01010200; output-level decoding remains outside this change | Adjustment, missing values, sign and event-time behavior require fixtures |
| Kiwoom REST | ka10081 example lists dt, open_pric, high_pric, low_pric, cur_prc, trde_qty | ka10004 lists sel_fpr_bid/buy_fpr_bid and *_fpr_req; subsequent levels have different names | cur_prc's completed/incomplete candle meaning and signed values still need verification |
| LS | Catalog lists t8410 daily/weekly/monthly/yearly charts | Catalog lists t1101 book operation | Detailed response keys were not retrieved; do not invent mappings |
| DB | Indexed official catalog lists daily charts | Indexed official catalog lists books | Direct guide returned HTTP 502 during this check; detailed schema remains unverified |
| Toss | Canonical OpenAPI 1.2.28 documents daily OHLCV using openPrice/highPrice/lowPrice/closePrice, volume and timestamp | OrderbookResponse uses asks/bids price/volume objects | KR example asks are descending; example order is not a universal contract |
| Meritz | Python example lists date, oprc/hprc/lprc, stck_clpr and acml_vol | First level askp/bidp, later askp2/bidp2 etc.; sizes askp_rsqn1/bidp_rsqn1 | Time-only field prpr_hour does not establish an absolute event instant |

References (accessed 2026-11-02):
- KIS: https://github.com/koreainvestment/open-trading-api/blob/main/examples_llm/domestic_stock/inquire_daily_itemchartprice/chk_inquire_daily_itemchartprice.py (inspected blob e6ea734d0a938069a3bf58f3c530717564fcef2f)
- Kiwoom daily: https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_stock_daily_chart.py (blob c6ec6b33393b1f45e98e7cfbb2db5699e4239b53)
- Kiwoom book: https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%9C%EC%84%B8/get_domestic_stock_quote.py (blob 77eb09356c8af6a98200cac55688027bba376bb1)
- LS: https://openapi.ls-sec.co.kr/apiservice
- DB: https://openapi.db-fi.com/apiservice
- Toss index: https://developers.tossinvest.com/llms.txt
- Toss canonical specification: https://openapi.tossinvest.com/openapi-docs/latest/openapi.json (version 1.2.28 when checked)
- Meritz: https://openapi.imeritz.com/samplecode-py

## Local value-model decisions (NOT assertions about raw broker responses)

1. Retain the typed-only API: no dictionary/JSON conversion helpers, adapters,
   network clients, authentication or automatic normalization in constructors.
2. Reuse Ticker's primitive validation and defensive flat metadata snapshot in
   private helpers. Preserve Ticker field names, defaults and hash behavior.
3. Candle initially represents only 1d regular-session KR equity bars. Require
   an explicit raw/adjusted label and canonical YYYY-MM-DD session_date. Its
   timestamp must equal that date's Asia/Seoul midnight expressed in UTC epoch
   milliseconds. This is an interval label, NOT an exchange event time.
4. Validate unsigned finite Decimal OHLC prices and low <= open/close <= high.
   Do not coerce strings, floats or signed zero; do not invent missing prices.
   volume=None remains distinct from zero. complete is bool or None; it is
   never inferred from the clock. Do not reject weekends/holidays: a value
   model is not a verified exchange calendar.
5. Use frozen/slotted OrderBookLevel(price: Decimal, quantity: int). A normalized
   level has a strictly positive price and nonnegative integral share quantity;
   quantity=0 is retained. A provider's zero-price placeholder is NOT a level.
   Decoders must resolve placeholders using evidence, not silently drop data.
6. OrderBook contains immutable tuples of OrderBookLevel, bids strictly descending
   and asks strictly ascending. Reject unordered/duplicate same-side levels;
   do not sort, aggregate, clamp depth or impose a universal ten-level limit.
   Empty and one-sided books are representable; missing raw fields are NOT proof
   of an empty book. Crossed/locked books are preserved because this value layer
   cannot infer auction state, synchronization or aggregation rules.
7. Item 5 supersedes only the Phase 01 conceptual [price, shares] level container
   for the public Python API. Existing JSON fixtures remain test inputs, not a
   public serializer or a promise that constructors accept raw list pairs.
8. Preserve symbol/venue/broker/info provenance, composite scope requirements,
   optional event timestamp and independent retrieved_at. Missing source time
   stays None. Hashes include immutable scalar metadata and all equality fields.
9. Metadata key filtering is defense in depth, not redaction or an upstream field
   allowlist. Future adapters must explicitly allowlist safe values; info={} is
   preferred when provenance is unverified. No model can recognize arbitrary
   secret values under an innocent key.

## Completion / review boundary

Tests must cover construction, schema field parity, all fixture values, Decimal
edge cases, KST/UTC dates and leap days, invalid OHLC, complete flags, immutability,
hash/equality, book ordering/duplicates, empty sides, zero quantities, and absence
of hidden parsing or serialization. All data is synthetic. CI success proves
these contracts, not broker integration. Keep the PR unmerged for Gemini review
and explicit maintainer approval. PR #6 (Shinhan scope) is not modified here.
