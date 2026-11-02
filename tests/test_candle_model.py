"""Daily Candle edge cases on synthetic values; no authenticated market data."""

import datetime as dt
import json
from dataclasses import FrozenInstanceError, fields, replace
from decimal import Decimal
from pathlib import Path

import pytest

from ktradelink.models import Candle

ROOT = Path(__file__).resolve().parents[1]


def example_candle(**changes: object) -> Candle:
    args = dict(
        symbol="005930", venue="KRX", broker="synthetic", timeframe="1d",
        timestamp=1793113200000, session_date="2026-10-28",
        open=Decimal("70000"), high=Decimal("71000"), low=Decimal("69000"),
        close=Decimal("70500"), volume=12345, adjustment="raw", session="regular",
        info={},
    )
    args.update(changes)
    return Candle(**args)


def test_all_fixture_fields_and_schema_match_runtime_model() -> None:
    raw = json.loads((ROOT / "tests/fixtures/spec/candle-day-synthetic.json").read_text())
    assert raw.pop("_synthetic") is True
    raw.pop("_note")
    for name in ("open", "high", "low", "close"):
        raw[name] = Decimal(raw[name])
    candle = Candle(**raw)
    for name, expected in raw.items():
        assert getattr(candle, name) == expected
    schema = json.loads((ROOT / "docs/specifications/normalized-models-v0.1.json").read_text())
    spec = schema["models"]["Candle"]
    assert {f.name for f in fields(Candle)} == set(spec["required"] + spec["optional"])
    assert candle.source_timestamp is None
    assert not hasattr(candle, "to_dict")
    assert not hasattr(candle, "to_json")


@pytest.mark.parametrize("name", ["open", "high", "low", "close"])
@pytest.mark.parametrize(
    "bad", [None, True, 1, 1.5, "1", Decimal("NaN"), Decimal("sNaN"),
            Decimal("Infinity"), Decimal("-1"), Decimal("-0")],
)
def test_invalid_prices_are_not_coerced(name: str, bad: object) -> None:
    with pytest.raises(ValueError):
        example_candle(**{name: bad})


@pytest.mark.parametrize(
    "change", [{"open": Decimal("72000")}, {"close": Decimal("68000")},
               {"low": Decimal("72000")}, {"high": Decimal("68000")}],
)
def test_invalid_ohlc_relations(change: dict) -> None:
    with pytest.raises(ValueError, match="OHLC"):
        example_candle(**change)


def test_equal_prices_zero_and_nullable_volume() -> None:
    zero = example_candle(open=Decimal(0), high=Decimal(0), low=Decimal(0), close=Decimal(0))
    assert zero.close == 0
    assert example_candle(volume=None).volume is None
    assert example_candle(volume=0).volume == 0


@pytest.mark.parametrize("name", ["volume", "source_timestamp", "retrieved_at"])
@pytest.mark.parametrize("bad", [True, -1, 1.2, "1"])
def test_invalid_integer_metadata(name: str, bad: object) -> None:
    with pytest.raises(ValueError):
        example_candle(**{name: bad})


@pytest.mark.parametrize("bad", [None, True, -1, "1793113200000", 1793113200000.0])
def test_anchor_requires_integer_not_bool(bad: object) -> None:
    with pytest.raises(ValueError):
        example_candle(timestamp=bad)


@pytest.mark.parametrize(
    "bad", [None, 20261028, "20261028", "2026-2-01", "2026-02-29",
            "2026-10-28T00:00:00", "2026-10-28\n", "2026-13-01", "0001-01-01"],
)
def test_invalid_session_date(bad: object) -> None:
    with pytest.raises(ValueError):
        example_candle(session_date=bad)


def test_anchor_is_kst_midnight_not_utc_midnight() -> None:
    candle = example_candle()
    moment = dt.datetime.fromtimestamp(candle.timestamp / 1000, tz=dt.UTC)
    assert moment.isoformat() == "2026-10-27T15:00:00+00:00"
    with pytest.raises(ValueError, match="anchor"):
        example_candle(timestamp=1793145600000)


def test_leap_day_and_weekend_are_calendar_dates_not_entitlements() -> None:
    leap = dt.datetime(2024, 2, 28, 15, tzinfo=dt.UTC)
    candle = example_candle(session_date="2024-02-29", timestamp=int(leap.timestamp()) * 1000)
    assert candle.session_date == "2024-02-29"
    saturday = dt.datetime(2026, 10, 30, 15, tzinfo=dt.UTC)
    example_candle(session_date="2026-10-31", timestamp=int(saturday.timestamp()) * 1000)


@pytest.mark.parametrize("value", [True, False, None])
def test_complete_is_explicit_tristate(value: bool | None) -> None:
    assert example_candle(complete=value).complete is value


@pytest.mark.parametrize("bad", [0, 1, "true", [], Decimal(1)])
def test_complete_does_not_accept_truthy_non_booleans(bad: object) -> None:
    with pytest.raises(ValueError):
        example_candle(complete=bad)


@pytest.mark.parametrize(
    "change", [{"timeframe": "1m"}, {"timeframe": "1w"}, {"timeframe": None},
               {"session": "all"}, {"session": None}, {"adjustment": "unknown"},
               {"adjustment": True}],
)
def test_unimplemented_scope_is_rejected(change: dict) -> None:
    with pytest.raises(ValueError):
        example_candle(**change)


def test_provenance_immutability_hash_and_completion_not_inferred() -> None:
    metadata = {"source": "synthetic", "counter": 0}
    candle = example_candle(info=metadata)
    same = example_candle(info=dict(reversed(metadata.items())))
    assert candle == same and hash(candle) == hash(same)
    assert {candle: "ok"}[same] == "ok"
    metadata["source"] = "mutated"
    assert candle.info["source"] == "synthetic"
    with pytest.raises(TypeError):
        candle.info["x"] = 1
    with pytest.raises(FrozenInstanceError):
        candle.close = Decimal(0)
    assert candle.complete is None
    assert candle != replace(candle, adjustment="adjusted")
    assert candle != replace(candle, source_timestamp=0)
    assert not hasattr(candle, "__dict__")


def test_composite_needs_scope_and_credentials_cannot_be_metadata() -> None:
    with pytest.raises(ValueError):
        example_candle(venue="BROKER_COMPOSITE")
    candle = example_candle(venue="BROKER_COMPOSITE", scope_description="synthetic scope")
    assert candle.scope_description == "synthetic scope"
    with pytest.raises(ValueError):
        example_candle(info={"app-key": "synthetic"})
