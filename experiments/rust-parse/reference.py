"""Python reference for a deliberately synthetic, broker-neutral quote payload.

This experiment is NOT a KIS/Kiwoom/LS/DB/Toss/Meritz response parser.
"""

import json
from decimal import Decimal

from ktradelink.models import Ticker

_PRICE_FIELDS = ("last", "open", "high", "low", "previous_close")
_INT_FIELDS = ("volume", "timestamp", "retrieved_at")
_KEYS = frozenset(("symbol", "venue", *_PRICE_FIELDS, *_INT_FIELDS))

# Tuple order matches the experimental Rust FFI return type, not a public API.
RawRow = tuple[
    str, str, str | None, str | None, str | None, str | None, str | None,
    int | None, int | None, int | None,
]


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    record: dict[str, object] = {}
    for key, value in pairs:
        if key in record:
            raise ValueError("duplicate JSON key")
        record[key] = value
    return record


def _non_json_constant(value: str) -> None:
    raise ValueError(f"non-JSON number {value}")


def python_parse_one(payload: str) -> RawRow:
    """Validate JSON shape and types without invoking the Ticker constructor."""
    record = json.loads(
        payload, object_pairs_hook=_unique_pairs, parse_constant=_non_json_constant
    )
    if not isinstance(record, dict) or not {"symbol", "venue"} <= record.keys():
        raise ValueError("synthetic JSON must be an object with symbol and venue")
    if not record.keys() <= _KEYS:
        raise ValueError("unknown synthetic quote fields")
    for key in ("symbol", "venue"):
        if not isinstance(record[key], str):
            raise ValueError(f"{key} must be a string")
    for key in _PRICE_FIELDS:
        value = record.get(key)
        if value is not None and not isinstance(value, str):
            raise ValueError(f"{key} must be a price string or null")
    for key in _INT_FIELDS:
        value = record.get(key)
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 2**64 - 1
        ):
            raise ValueError(f"{key} must be a nonnegative 64-bit integer or null")
    return (
        record["symbol"], record["venue"],
        *(record.get(key) for key in _PRICE_FIELDS),
        *(record.get(key) for key in _INT_FIELDS),
    )


def python_parse_batch(payloads: list[str]) -> list[RawRow]:
    return [python_parse_one(payload) for payload in payloads]


def row_to_ticker(row: RawRow) -> Ticker:
    """Build the exact existing public typed model, for either parsing backend."""
    symbol, venue, last, open_, high, low, previous_close, volume, timestamp, received = row

    def price(value: str | None) -> Decimal | None:
        return None if value is None else Decimal(value)

    return Ticker(
        symbol=symbol,
        venue=venue,
        broker="synthetic",
        last=price(last),
        open=price(open_),
        high=price(high),
        low=price(low),
        previous_close=price(previous_close),
        volume=volume,
        timestamp=timestamp,
        retrieved_at=received,
        info={},
    )
