# Typed market-data values (offline)

This change provides in-memory value objects. It does not implement
`fetch_ticker`, `fetch_ohlcv`, `fetch_order_book`, authentication, native parsing,
or any brokerage connection. All values below are synthetic.

```python
from decimal import Decimal
from ktradelink.models import Candle, OrderBook, OrderBookLevel

bar = Candle(
    symbol="005930", venue="KRX", broker="synthetic", timeframe="1d",
    timestamp=1793113200000, session_date="2026-10-28",
    open=Decimal("70000"), high=Decimal("71000"),
    low=Decimal("69000"), close=Decimal("70500"),
    volume=12345, adjustment="raw", session="regular",
)
book = OrderBook(
    symbol="005930", venue="KRX", broker="synthetic",
    bids=(OrderBookLevel(Decimal("70000"), 12),),
    asks=(OrderBookLevel(Decimal("70100"), 0),),
)
assert bar.complete is None
assert book.asks[0].quantity == 0
```

## Meaning and limitations

- Candle initially accepts only `1d` / `regular`, with explicit `raw` or
  `adjusted` provenance. That label does not itself adjust prices or establish
  that a provider supplied regular-session-only data.
- The required `timestamp` is the `session_date` Asia/Seoul midnight anchor,
  as a nonnegative integer Unix millisecond value, not an exchange event time.
  The example's UTC date is the preceding day. No weekday/holiday validation
  or current-time inference is performed.
- `tzdata` is a runtime dependency so `ZoneInfo("Asia/Seoul")` works even without
  a system timezone database. This follows the Python zoneinfo guidance:
  https://docs.python.org/3.11/library/zoneinfo.html#data-sources
- Missing source event time stays `None`; `retrieved_at` is separate. Candle
  volume may be `None`, zero, or a nonnegative integer; `complete` is explicitly
  `True`, `False`, or `None` (unknown).
- Prices must already be finite unsigned Decimal values. No string/float/sign
  coercion takes place. Signed negative zero is rejected, consistent with Ticker.
- Book sides must be tuples of typed levels. Prices are strictly positive;
  quantities are nonnegative integer shares, not arbitrary lots or turnover.
  No automatic sorting, deduplication, depth truncation or spread repair occurs.
  Bids descend and asks ascend. Explicit empty/one-sided books are permitted.
  A decoder must not treat a missing upstream field as an empty side.
- Crossed/locked books are representable; no claim about auction state or source
  synchronization is made. Models do not define an executable order route.
- `info` is a defensive flat, read-only scalar snapshot. Its name filter is not
  a full secret scanner. Future decoders must allowlist native fields and values.
- Frozen/slotted values are hashable with the same equality fields; hash values
  are not guaranteed stable across interpreter processes. No serialization,
  dictionary conversion, pickle portability or stable wire format is promised.

See ADR 0003 for publisher evidence, initial restrictions, and the typed
`OrderBookLevel` refinement of the older conceptual `[price, shares]` notation.
Synthetic fixtures validate model contracts, not real/paper account responses.
