"""Normalized daily equity bars, not a broker response parser."""

import datetime as dt
from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import Decimal
from zoneinfo import ZoneInfo

from ktradelink.models._validation import (
    InfoScalar,
    freeze_info,
    validate_integer,
    validate_price,
    validate_provenance,
)


def _session_anchor(session_date: str) -> int:
    """Return the Asia/Seoul midnight label as integer UTC milliseconds."""
    if not isinstance(session_date, str) or len(session_date) != 10:
        raise ValueError("session_date must be canonical YYYY-MM-DD")
    try:
        day = dt.date.fromisoformat(session_date)
        if day.isoformat() != session_date:
            raise ValueError("noncanonical date")
        midnight = dt.datetime.combine(day, dt.time.min, tzinfo=ZoneInfo("Asia/Seoul"))
        delta = midnight.astimezone(dt.UTC) - dt.datetime(1970, 1, 1, tzinfo=dt.UTC)
    except (ValueError, OverflowError) as exc:
        raise ValueError("session_date must be a valid representable ISO date") from exc
    return delta // dt.timedelta(milliseconds=1)


@dataclass(frozen=True, slots=True)
class Candle:
    """A daily regular-session value with explicit adjustment provenance.

    timestamp is a session anchor, not an execution time. This class does not
    infer holidays, completion, signs, adjustment factors or source coverage.
    Only 1d/regular is implemented at this stage; unknown scopes must not be
    relabeled to make construction pass. No public serialization helpers.
    """

    symbol: str
    venue: str
    broker: str
    timeframe: str
    timestamp: int
    session_date: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int | None
    adjustment: str
    session: str
    info: Mapping[str, InfoScalar] = field(default_factory=dict, repr=False)
    complete: bool | None = None
    source_timestamp: int | None = None
    retrieved_at: int | None = None
    scope_description: str | None = None

    def __post_init__(self) -> None:
        validate_provenance(self.symbol, self.venue, self.broker, self.scope_description)
        if self.timeframe != "1d":
            raise ValueError("only 1d Candle values are implemented")
        if self.session != "regular":
            raise ValueError("only explicit regular-session Candle values are implemented")
        if self.adjustment not in ("raw", "adjusted"):
            raise ValueError("adjustment must be raw or adjusted")
        validate_integer("timestamp", self.timestamp, nullable=False)
        if self.timestamp != _session_anchor(self.session_date):
            raise ValueError("timestamp must match session_date's Asia/Seoul midnight anchor")
        for name in ("open", "high", "low", "close"):
            validate_price(name, getattr(self, name), nullable=False)
        if not (self.low <= self.open <= self.high and self.low <= self.close <= self.high):
            raise ValueError("OHLC must satisfy low <= open/close <= high")
        validate_integer("volume", self.volume)
        validate_integer("source_timestamp", self.source_timestamp)
        validate_integer("retrieved_at", self.retrieved_at)
        if self.complete is not None and type(self.complete) is not bool:
            raise ValueError("complete must be bool or None")
        object.__setattr__(self, "info", freeze_info(self.info))

    def __hash__(self) -> int:
        return hash((
            self.symbol, self.venue, self.broker, self.timeframe, self.timestamp,
            self.session_date, self.open, self.high, self.low, self.close, self.volume,
            self.adjustment, self.session, tuple(sorted(self.info.items())),
            self.complete, self.source_timestamp, self.retrieved_at, self.scope_description,
        ))
