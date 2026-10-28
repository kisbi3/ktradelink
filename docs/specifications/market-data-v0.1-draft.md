# Unified domestic-equity market-data API — v0.1 PROPOSAL

- **Status:** Proposed for independent Gemini Web review and maintainer decision
- **Last revised:** 2026-10-29
- **Not implemented. No live broker or paper account has been queried.**
- **First target:** KIS + Kiwoom **REST**; Korean listed common stocks, KRX
  read-only market data. NXT/SOR/composite scopes are documented as future
  conditional features, *not* an implicit KRX fallback.
- Source evidence: [KIS](../brokers/kis-market-data.md) and
  [Kiwoom REST](../brokers/kiwoom-market-data.md)

This proposal makes falsifiable choices so reviewers can reject them before
adapter development. A name matching a vendor endpoint is **not** a declaration
that KTradeLink supports it.

## 1. Design goals

1. A broker swap must preserve the **meaning** of the returned price, candle,
   quote book and session, or raise an explicit error.
2. User-facing `symbol` is a string with leading zeros intact, never an int.
3. Instrument identity, market-data source and order routing are distinct.
   **Order routing is outside v0.1**.
4. Model sources as potentially stale/partial; distinguish a missing value from
   a genuine zero; never invent a native exchange timestamp.
5. Brokerage capabilities are explicit and *per method, venue, environment,
   timeframe and asset class*, not an unconditional `has=True`.
6. Prefer read-only fixtures in CI; do not fetch live quotes or credentials.

## 2. Candidate public interface (signatures for review)

```python
# Conceptual contract; these functions do not exist yet.
broker.load_markets(*, reload=False)

broker.fetch_ticker(symbol: str, *, venue: str = "KRX", params=None)
broker.fetch_order_book(
    symbol: str, limit: int | None = None, *,
    venue: str = "KRX", params=None
)
broker.fetch_ohlcv(
    symbol: str, timeframe: str = "1d",
    since: int | None = None, limit: int | None = None, *,
    venue: str = "KRX", adjustment: str = "raw",
    session: str = "regular", params=None
)
```

`params` is reserved for **documented broker-native optional parameters**;
common choices such as `venue`, `adjustment`, and `session` must be explicit
rather than hidden. Unknown or conflicting options must raise an error.

The API names deliberately resemble CCXT, but the proposed data contract is
**Python-native**, not guaranteed byte-for-byte compatible with CCXT's list
return types. An eventual `to_ccxt_ohlcv()` or compatibility layer may be
offered separately after the normalized contract is stable. Do not implement
two conflicting representations now.

## 3. Symbol, venue and quote-source semantics

- **First-version stock symbol:** exactly six ASCII digits, e.g. `"005930"`.
  Do not strip leading zeros, accept integer symbols, or auto-guess ETFs/ETNs,
  indices, bonds or derivatives. Expand the instrument registry later.
- **Proposed `venue` values:** `KRX`, `NXT`, `BROKER_COMPOSITE`.
  `KRX` is the explicit **default** for v0.1 domestic-stock retrieval.
  Passing `NXT` or `BROKER_COMPOSITE` is an unsupported-capability error
  until that specific endpoint, account environment and behavior are verified.
- **Instrument vs market-data scope:** `venue="BROKER_COMPOSITE"` means a
  broker-defined multi-market quote, not a physical exchange and **never an
  order execution destination**. The result must record source semantics and
  source broker. Do not assume KIS `UN` and Kiwoom `_AL` SOR are identical.
- KIS example: `FID_INPUT_ISCD=005930` and
  `FID_COND_MRKT_DIV_CODE=J|NX|UN`.
- Kiwoom example: `stk_cd=005930|005930_NX|005930_AL` (the latter two
  are market-qualified *native* IDs). Query mapping must be endpoint-specific.
- **No fallback:** if the selected venue is unavailable, do not silently
  fetch KRX or an aggregated quote instead. Raise `UnsupportedCapability`
  or an explicit broker/data-access error.
- Each normalized object must contain both `symbol` and `venue` as well as
  `broker`; composite quotes also require a `scope_description` naming the
  native market source.

## 4. Proposed normalized data contract

For first-version pure-Python usage, model objects can be typed records
(`TypedDict`, dataclasses or equivalents **not chosen yet**). All payloads
below are proposals, not current `ktradelink` objects.

| Result | Required keys | Optional/nullable keys |
| --- | --- | --- |
| Ticker | `symbol`, `venue`, `broker`, `last`, `info` | `timestamp`, `retrieved_at`, `open`, `high`, `low`, `close`, `volume`, `bid`, `ask`, `scope_description` |
| Candle | `symbol`, `venue`, `broker`, `timeframe`, `timestamp`, `session_date`, `open`, `high`, `low`, `close`, `volume`, `adjustment`, `session` | `complete`, `source_timestamp` |
| OrderBook | `symbol`, `venue`, `broker`, `bids`, `asks`, `info` | `timestamp`, `retrieved_at`, `scope_description` |

- **Missing prices:** `last` is present as a key but can be `None`;
  `open/high/low/close/bid/ask` are `Decimal | None`. Distinct
  `None` vs `Decimal(0)` must be preserved based on field-level evidence.
  `volume` is an integer number of shares if supplied; otherwise `None`.
- **Precision (proposed):** parse currency prices as `Decimal`, not
  binary floats. For first-version domestic common stocks, currency is KRW
  and quantity unit is shares; do not infer the units of monetary **turnover**.
  JSON serialization of Decimal would require decimal *strings* and versioned
  schemas. Tick-size/order rules are separate concerns.
- **Source sign:** a leading `+`/`-` in a Kiwoom string may be directional
  metadata for a price *or* an actual signed delta, depending on field.
  Evidence for an `abs` transform is required per field. A missing field
  or non-numeric garbage should not be changed to zero silently.
- **Raw data:** `info` defaults to an empty, allowlisted sanitized mapping.
  Never include tokens, account identifiers, authentication headers, keys or
  unconstrained upstream payloads in public models or logs.

## 5. Time and market session semantics

- All values named `timestamp` or `retrieved_at` are **UTC Unix epoch
  milliseconds**, typed `int | None`. A quote/order-book timestamp is
  `None` unless the publisher supplies a trustworthy event time.
  `retrieved_at` is a *client receive time*, never an exchange time.
- Day candles represent a **KST exchange session date**; the required
  `session_date` is an ISO date (`YYYY-MM-DD`). Proposed `timestamp`
  convention for `1d`: **00:00:00 Asia/Seoul of `session_date`**, converted
  to UTC Unix ms as a *session anchor*, not as a real trade time.
  Example: `2026-10-28` session anchors at
  `2026-10-27T15:00:00Z`, which is correct for KST midnight. Consumers must
  NOT compare its UTC date to `session_date` and call it a mismatch.
- Minute candles require an explicit source date + time in KST and a
  `timestamp` for the **start of the interval**; reject unknown end-vs-start
  conventions until verified. If the source gives only `HHMMSS`, require a
  verified trading date, not local-wall-clock inference.
- For weekly/monthly bars, the interval anchor/session label remains **TBD**;
  no `1w`/`1M` support may be advertised until defined.
- Keep `session="regular"` as v0.1 requested scope, not an assumption that
  all broker API responses exclude pre/post market and NXT trading. If the
  adapter cannot establish regular-session coverage, error instead of
  mislabeling mixed-session bars.
- Session timestamps, DST, holidays, and exchange schedule require
  explicit tests. Korea uses `Asia/Seoul` for current market data.

## 6. Candle and book ordering, pagination and adjustments

- `fetch_ohlcv()` returns candles **oldest to newest** by timestamp, without
  duplicate timestamps in a single `venue/timeframe/adjustment/session`
  series. Whether the source sorts newest-first is implementation detail.
- If `since` is provided, interpret it as UTC Unix ms **inclusive** and
  return up to `limit` earliest items at or after `since`. Without `since`,
  `limit` refers to the most recent `limit` available candles, still returned
  oldest-first. All limits must be validated as positive integers.
- No hidden truncation: if the requested range needs pagination the adapter
  must implement a proven continuation path or explicitly reject that request.
  Fewer items are acceptable only when a genuine end-of-history boundary
  is established, not merely because a provider response was capped.
- `fetch_order_book`: `bids` descending by price, `asks` ascending;
  levels are `[Decimal(price), int(shares)]`. An actual zero-size quoted
  level may be preserved when its price was provided; **missing** price and
  level information must not be synthesized. `limit` counts levels on
  *each side*; exceeding verified source depth must error rather than
  silently clamp.
- **Adjustment:** `raw` vs `adjusted` is a semantic input, not a generic
  `FID_ORG_ADJ_PRC` value. The KIS adjustment parameter meaning can vary
  across endpoints; Kiwoom's `upd_stkpc_tp` needs independent per-ID mapping.
  The proposed default `raw` must **not** be published until backed by
  authoritative response fixtures; otherwise fail with unsupported option.
- Incomplete current session bar and suspended trading must be distinguished
  from missing data. Define their exact status after test fixtures are available.

## 7. Capabilities and exceptions (names proposed)

**Capability states**: `documented_candidate`, `unverified`,
`supported`, `conditional`, `unsupported`. **Only `supported`**
means both implemented and passing broker-specific normalized contract tests.
No capabilities are `supported` today. Future discovery must allow
method, symbol asset class, environment, venue, timeframe and permission
restrictions (with documented evidence references).

**Proposed error taxonomy**:

- `InvalidSymbol`, `InvalidVenue`, `InvalidTimeframe`,
  `InvalidParameter`
- `UnsupportedCapability` (feature/option not implemented or proven)
- `AuthenticationError`, `PermissionDenied`
- `RateLimitExceeded`, `BrokerUnavailable`, `TransportError`
- `ResponseSchemaError`, `IncompleteMarketData`

An HTTP success with missing required fields is **not** a valid ticker/candle.
No broad `except: return []` or ungrounded automatic retries. Raw broker
error IDs map to common errors only when verified.

## 8. Unresolved design gates (must be reviewed before adapters)

- [ ] Confirm `Candle` typed-record representation vs strict CCXT six-value
      OHLCV arrays and possible dual convenience API.
- [ ] Check native KIS and Kiwoom field names, nullable semantics, signed-price
      rules and response timestamps against vendor specifications and legal
      sanitized account fixtures.
- [ ] Verify KIS daily adjustment behavior *per endpoint* and Kiwoom `ka10081`
      chart's adjustment, timestamps and continuation; add raw and adjusted
      examples, no guessing.
- [ ] Verify both providers' quote scope/mode, paper vs real entitlements and
      NXT/SOR rules; explicit KRX-only initial support is the safe option.
- [ ] Define `load_markets` master sources, cache invalidation, session/venue
      listing, and data rights before enabling it.
- [ ] Create contract fixtures for genuine vendor responses with sensitive
      information removed. Synthetic examples are only **design examples**.
- [ ] Confirm per-venue interval availability, `since`/paging completeness,
      empty order-book levels, out-of-session data and date boundaries.
- [ ] Record Gemini Web review pinned to a commit SHA, resolve findings, and
      obtain human approval. Until then this document is PROPOSED.

## 9. Non-goals

No functional KIS/Kiwoom adapter, no real data, no WebSocket streaming, no
orders/accounts, no broker credential processing, no backtesting, no MCP, no
hosted SaaS, and no market-data redistribution.
