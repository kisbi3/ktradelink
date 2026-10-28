# Market-data Unified API v0.1 — DRAFT

- **Status:** Proposed, not approved or implemented
- **Created:** 2026-10-28
- **Target brokers:** Korea Investment & Securities (KIS), Kiwoom Securities
- **Initial scope:** domestic equities, read-only

## Motivation

Applications should call the same methods and receive normalized fields when
the underlying brokers actually support equivalent functionality.

## Proposed public methods

| Method | Intended result | Notes |
| --- | --- | --- |
| `load_markets()` | supported instruments and metadata | shape TBD |
| `fetch_ticker(symbol, params=None)` | current price and quote summary | fields TBD |
| `fetch_ohlcv(symbol, timeframe="1d", since=None, limit=None, params=None)` | list of candles | only broker-supported intervals |
| `fetch_order_book(symbol, limit=None, params=None)` | normalized bids and asks | only when broker exposes the necessary depth |

All methods are **proposals**. The actual broker capability list must be
verified against current official documentation before implementing any of
them. A declared unsupported method should fail explicitly, not silently
substitute a different dataset.

## Proposed normalized fields

Ticker candidate: `symbol`, `timestamp`, `datetime`, `last`, `open`, `high`,
`low`, `close`, `volume`, `bid`, `ask`, `info`.

OHLCV candidate: `[timestamp, open, high, low, close, volume]` with a UTC Unix
millisecond timestamp (same basic approach as CCXT).

Order-book candidate: `symbol`, `timestamp`, `bids`, `asks`, `info`; bid/ask
levels would include price and size.

`info` should preserve a sanitized broker-native payload where permitted.
Missing values must be distinguishable from genuine zeros.

## Open questions requiring formal decisions

1. **Symbols:** canonical instrument identifier (e.g. domestic six-digit code)
   versus market-qualified identifier; avoid confusing trading venue with the
   instrument itself.
2. **Venues:** KRX/NXT selection and broker-specific market codes; never infer
   an executable venue from a quote without an explicit rule.
3. **Numeric representation:** `Decimal` versus `float`, including serialization
   and unit handling.
4. **Timestamps:** native timestamps, session boundaries, KST-to-UTC conversion,
   and daily-bar timestamp conventions.
5. **Price semantics:** adjusted/unadjusted OHLCV, auction/closing price,
   trading-session qualification, market suspensions and missing data.
6. **Market-data availability:** broker entitlements and endpoint limits; no
   assumption that each broker offers a full order book or arbitrary intervals.
7. **Rate limits and caching:** quotas are broker-specific and must be validated.
8. **Exception taxonomy:** distinguish invalid input, authorization, quota,
   temporarily unavailable endpoint, unsupported capability and parse mismatch.
9. **Sync/async API:** public naming and behavior across Python execution modes.

## Verification checklist before approval

- [ ] KIS official API endpoints and fields mapped to each proposed method
- [ ] Kiwoom official API endpoints and fields mapped to each proposed method
- [ ] Capability matrix includes unsupported and conditional cases
- [ ] Timestamp, symbol, numeric and venue decisions documented
- [ ] Sanitized samples and contract tests specified
- [ ] Gemini Web independent review recorded with a target commit SHA
- [ ] Human maintainer approval documented

## Explicit non-goals for this spec

No orders, live credentials, automatic execution, backtesting, MCP or hosted
service. These require later separate designs and reviews.
