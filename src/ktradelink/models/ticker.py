"""Broker-neutral, typed current-quote value model.

This is a value type only: no broker calls, parsing, or credential handling.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import Decimal
from types import MappingProxyType

InfoScalar = str | int | bool | Decimal | None

_SENSITIVE_KEYS = (
    "token", "secret", "password", "account", "authorization",
    "credential", "cookie", "api_key", "appkey",
)
_VENUES = frozenset({"KRX", "NXT", "BROKER_COMPOSITE"})
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
        for name in ("symbol", "broker"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value or value != value.strip():
                raise ValueError(f"{name} must be a nonempty, trimmed string")

        if not isinstance(self.venue, str) or self.venue not in _VENUES:
            raise ValueError(f"venue must be one of {sorted(_VENUES)!r}")
        if self.venue == "BROKER_COMPOSITE" and (
            not isinstance(self.scope_description, str)
            or not self.scope_description.strip()
        ):
            raise ValueError("composite quote requires scope_description")
        if self.scope_description is not None and (
            not isinstance(self.scope_description, str)
            or self.scope_description != self.scope_description.strip()
            or not self.scope_description
        ):
            raise ValueError("scope_description must be a nonempty, trimmed string")

        for name in _PRICES:
            value = getattr(self, name)
            if value is not None and (
                not isinstance(value, Decimal)
                or not value.is_finite()
                or value < 0
            ):
                raise ValueError(f"{name} must be a nonnegative finite Decimal or None")
        for name in (*_TIMESTAMPS, "volume"):
            value = getattr(self, name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value < 0
            ):
                raise ValueError(f"{name} must be a nonnegative integer or None")

        if not isinstance(self.info, Mapping):
            raise TypeError("info must be a mapping of safe scalar metadata")
        snapshot: dict[str, InfoScalar] = {}
        for key, value in self.info.items():
            if not isinstance(key, str):
                raise TypeError("info keys must be strings")
            normalized_key = key.casefold().replace("-", "_")
            if any(term in normalized_key for term in _SENSITIVE_KEYS):
                raise ValueError("info must not contain authentication/account fields")
            if not (value is None or isinstance(value, (str, int, bool, Decimal))):
                raise TypeError("info values must be immutable scalar metadata")
            if isinstance(value, Decimal) and not value.is_finite():
                raise ValueError("info decimals must be finite")
            snapshot[key] = value
        object.__setattr__(self, "info", MappingProxyType(snapshot))
