"""Typed, already-normalized equity book snapshots; no native parsing."""

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


@dataclass(frozen=True, slots=True)
class OrderBookLevel:
    """One quoted price and integral share quantity, including zero quantity."""

    price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        validate_price("price", self.price, nullable=False)
        if self.price.is_zero():
            raise ValueError("book level price must be strictly positive")
        validate_integer("quantity", self.quantity, nullable=False)


def _validate_side(name: str, levels: tuple[OrderBookLevel, ...]) -> None:
    if not isinstance(levels, tuple):
        raise TypeError(f"{name} must be a tuple of OrderBookLevel values")
    if any(not isinstance(level, OrderBookLevel) for level in levels):
        raise TypeError(f"{name} must contain only OrderBookLevel values")
    for left, right in zip(levels, levels[1:], strict=False):
        ordered = left.price > right.price if name == "bids" else left.price < right.price
        if not ordered:
            raise ValueError(f"{name} must be strictly price-ordered without duplicates")


@dataclass(frozen=True, slots=True)
class OrderBook:
    """Normalized snapshot with best-to-worst price ordering on each side.

    Bids descend and asks ascend. Empty/one-sided and crossed/locked books are
    representable; the model cannot infer auction or source synchronization.
    Constructors neither sort/merge levels nor decide whether a native zero is
    a missing quote. An absent provider field must not be converted to ().
    """

    symbol: str
    venue: str
    broker: str
    bids: tuple[OrderBookLevel, ...]
    asks: tuple[OrderBookLevel, ...]
    info: Mapping[str, InfoScalar] = field(default_factory=dict, repr=False)
    timestamp: int | None = None
    retrieved_at: int | None = None
    scope_description: str | None = None

    def __post_init__(self) -> None:
        validate_provenance(self.symbol, self.venue, self.broker, self.scope_description)
        _validate_side("bids", self.bids)
        _validate_side("asks", self.asks)
        validate_integer("timestamp", self.timestamp)
        validate_integer("retrieved_at", self.retrieved_at)
        object.__setattr__(self, "info", freeze_info(self.info))

    def __hash__(self) -> int:
        return hash((
            self.symbol, self.venue, self.broker, self.bids, self.asks,
            tuple(sorted(self.info.items())), self.timestamp, self.retrieved_at,
            self.scope_description,
        ))
