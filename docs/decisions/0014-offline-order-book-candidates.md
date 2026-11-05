# ADR 0014: Offline KIS/Kiwoom/LS order-book candidates

- Date: 2026-11-05 (Asia/Seoul)
- Status: **proposed for independent review; offline implementation only.**
  Not a public API and not live-verified. Merging this authorizes no broker
  call, credential use, account access or order.
- Base: `main` `1a7b893f2f9fc205775314cd3ad51404442db046`.
- Related: Issue #17; ADR 0003 (OrderBook value contract), ADR 0005/0006
  (Rust core and decoder candidates), ADR 0010 (LS t1102). They stay binding.
- Evidence: [order-book ledger](../brokers/order-book-evidence-2026-11-05.md).

## Context

`ktradelink.models.OrderBook` exists (ADR 0003), and the market-data spec
(section 6) fixes the `fetch_order_book` meaning: bids descending, asks
ascending, `[Decimal price, int shares]` levels, a zero-size level kept only
when its price was given, no synthesized levels, and `limit` per side that
errors beyond verified depth. No decoder produced an `OrderBook` yet.

The pinned KIS and Kiwoom examples and the LS API guide document 10-level
books, but with different envelopes, value types and gaps: Kiwoom prices
carry an undocumented sign, KIS value types are not shown, and LS `t1101`
has no exchange selector.

## Decision

1. **Rust core** gets `BookLevel` (strictly positive decimal-text price, `u64`
   quantity, zero kept) and `CoreOrderBook` with strict best-to-worst order
   per side, compared exactly on decimal text without floats. Empty,
   one-sided, crossed and locked books are representable. The core stays
   free of JSON, network and Python.
2. **Decoder** `decode_order_book_candidate(broker, symbol, venue, payload,
   limit)` in `crates/ktradelink-decoders/src/order_book.rs`:
   - KIS `FHKST01010200` (`output1`), Kiwoom `ka10004` (root), LS `t1101`
     (`t1101OutBlock`); KRX caller context only; DB/Toss/Meritz are
     `UnsupportedBroker`.
   - Status is required with its native type (KIS `"0"`, Kiwoom integer `0`,
     LS `"00000"`); the LS `shcode` echo must match the request.
   - All 10 documented levels per side are required. KIS/Kiwoom accept
     unsigned digit strings and LS unsigned JSON integers. Signed Kiwoom
     prices are rejected, never `abs()`-ed.
   - A zero-price **and** zero-quantity rank means "no quote" and may only
     form a contiguous tail (`LevelGap` otherwise); a zero price with
     quantity is `InvalidPrice`. This interpretation is library policy: no
     publisher documents an empty rank.
   - Ordering is checked over the full book, then `limit` caps each side
     (`0` → `InvalidLimit`, `>10` → `DepthExceeded`).
   - Same strict JSON (duplicate keys at any depth), 1 MiB bound and
     symbol-before-parse rules as the ticker decoder. Timestamps stay
     `None`: every source time field is time-of-day only or contradictory.
3. **PyO3/Python:** private `_decode_order_book_candidate` and
   `ktradelink._native.decode_order_book_candidate` return the existing
   `OrderBook`/`OrderBookLevel`; `info` is empty. The native
   `CONTRACT_VERSION` becomes **2**, so an older build is rejected as
   incompatible rather than failing on a missing function.
4. **Offline request plans** in the new private `_order_book_plan` module
   (reusing `_request_plan` origins, symbol check and auth field names):
   - KIS: `GET …/inquire-asking-price-exp-ccn`, `FID_COND_MRKT_DIV_CODE=J`,
     `tr_id FHKST01010200`, `custtype P`, empty `tr_cont`; live and paper.
   - Kiwoom: `POST /api/dostk/mrkcond`, `api-id ka10004`, bare 6-digit
     `stk_cd` (KRX); live and mock.
   - **LS is not planned:** `t1101` cannot select a venue, so a KRX book
     cannot be requested. `t8450` takes `exchgubun`, but its per-venue
     quantity columns are not explained well enough to map. It is not
     adopted.
   - No transport wiring. `HttpsTransport` and the live smoke tool are
     unchanged.

## Consequences and limits

- Kiwoom real responses are expected to carry signed prices and will fail
  closed until the sign meaning is documented. LS can be decoded but not
  planned. KIS JSON types and empty-rank encoding are assumptions that
  fail closed if wrong.
- KIS and Kiwoom books are not bound to the requested symbol by their
  responses. Only the LS echo is checked.
- No public `fetch_order_book`, no capability flag and no `supported`
  state. Gateway behaviour, rate limits, session coverage and
  redistribution rights are unverified.
- Tests are offline. They use synthetic fixtures under
  `tests/fixtures/order_book` that follow publisher field names.
