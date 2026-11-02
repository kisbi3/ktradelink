"""Broker-neutral, typed current-quote value model.

This is a value type only: no broker calls, parsing, or credential handling.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import Decimal

from ktradelink.models._validation import (
    InfoScalar,
    freeze_info,
    validate_integer,
    validate_price,
    validate_provenance,
)

_PRICES = ("last", "open", "high", "low", "previous_close", "bid", "ask")
_TIMESTAMPS = ("timestamp", "retrieved_at")


@dataclass(frozen=True, slots=True)
class Ticker:
    """Normalized quote metadata with an explicit source and nullable prices.

    Prices must already be normalized to Decimal by a broker-specific decoder.
    This constructor never guesses a broker-native field's sign or timestamp.
    The object intentionally has no public dictionary/JSON conversion method.
    """

    symbol: str
    venue: str
    broker: str
    last: Decimal | None
    info: Mapping[str, InfoScalar] = field(default_factory=dict, repr=False)
    timestamp: int | None = None
    retrieved_at: int | None = None
    open: Decimal | None = None
    high: Decimal | None = None
    low: Decimal | None = None
    previous_close: Decimal | None = None
    volume: int | None = None
    bid: Decimal | None = None
    ask: Decimal | None = None
    scope_description: str | None = None

    def __post_init__(self) -> None:
        validate_provenance(self.symbol, self.venue, self.broker, self.scope_description)
        for name in _PRICES:
            validate_price(name, getattr(self, name))
        for name in (*_TIMESTAMPS, "volume"):
            validate_integer(name, getattr(self, name))
        object.__setattr__(self, "info", freeze_info(self.info))

    def __hash__(self) -> int:
        """Hash all equality fields, including sanitized scalar metadata.

        A MappingProxyType is immutable but not hashable. Its contents are
        deliberately restricted to hashable scalars during construction.
        Sorting items makes the hash independent of source mapping order.
        """
        return hash((
            self.symbol,
            self.venue,
            self.broker,
            self.last,
            tuple(sorted(self.info.items())),
            self.timestamp,
            self.retrieved_at,
            self.open,
            self.high,
            self.low,
            self.previous_close,
            self.volume,
            self.bid,
            self.ask,
            self.scope_description,
        ))
