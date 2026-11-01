"""Construction-time contracts for the typed-only, broker-neutral Ticker."""

import json
from dataclasses import FrozenInstanceError
from decimal import Decimal
from pathlib import Path

import pytest

from ktradelink.models import Ticker


def example_ticker(**overrides: object) -> Ticker:
    kwargs = {
        "symbol": "005930",
        "venue": "KRX",
        "broker": "kis",
        "last": Decimal("70500"),
        "previous_close": Decimal("70000"),
        "volume": 0,
        "info": {"source_api_id": "example"},
    }
    kwargs.update(overrides)
    return Ticker(**kwargs)


def test_fixture_builds_typed_ticker_with_nullable_bid_and_ask() -> None:
    path = Path(__file__).parent / "fixtures" / "spec" / "ticker-synthetic.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["_synthetic"] is True
    ticker = Ticker(
        symbol=data["symbol"],
        venue=data["venue"],
        broker=data["broker"],
        last=Decimal(data["last"]),
        previous_close=Decimal(data["previous_close"]),
        bid=data["bid"],
        ask=data["ask"],
        info=data["info"],
    )
    assert ticker.last == Decimal("70500")
    assert ticker.previous_close == Decimal("70000")
    assert ticker.bid is None and ticker.ask is None
    assert ticker.symbol == "005930"
    assert not hasattr(ticker, "to_dict")
    assert not hasattr(ticker, "to_json")
    assert not hasattr(ticker, "close")


def test_frozen_model_and_independent_info_snapshot() -> None:
    native = {"source_api_id": "ka10001"}
    ticker = example_ticker(info=native)
    native["source_api_id"] = "mutated"
    assert ticker.info["source_api_id"] == "ka10001"
    with pytest.raises(TypeError):
        ticker.info["source_api_id"] = "not allowed"
    with pytest.raises(FrozenInstanceError):
        ticker.last = Decimal("10")
    assert not hasattr(ticker, "__dict__")


@pytest.mark.parametrize(
    "bad",
    ["70500", 70500, 70500.0, Decimal("NaN"), Decimal("Infinity"), Decimal("-1")],
)
def test_reject_unparsed_or_invalid_prices(bad: object) -> None:
    with pytest.raises(ValueError):
        example_ticker(last=bad)


@pytest.mark.parametrize("bad", [True, 1.5, -1, "42"])
def test_reject_invalid_volume(bad: object) -> None:
    with pytest.raises(ValueError):
        example_ticker(volume=bad)


def test_zero_price_and_missing_price_are_distinct() -> None:
    assert example_ticker(last=Decimal(0)).last == Decimal(0)
    assert example_ticker(last=None).last is None


@pytest.mark.parametrize("bad", [True, "123", -1])
def test_reject_invalid_timestamps(bad: object) -> None:
    with pytest.raises(ValueError):
        example_ticker(timestamp=bad)


def test_non_numeric_korean_symbol_is_not_rejected_by_value_model() -> None:
    assert example_ticker(symbol="0101N0").symbol == "0101N0"
    assert example_ticker(symbol="005930").symbol == "005930"


@pytest.mark.parametrize("value", ["", " 005930", 123456])
def test_invalid_symbol(value: object) -> None:
    with pytest.raises(ValueError):
        example_ticker(symbol=value)


def test_composite_scope_required() -> None:
    with pytest.raises(ValueError):
        example_ticker(venue="BROKER_COMPOSITE")
    ticker = example_ticker(
        venue="BROKER_COMPOSITE", scope_description="broker-defined quote aggregation"
    )
    assert ticker.scope_description == "broker-defined quote aggregation"
    with pytest.raises(ValueError):
        example_ticker(venue="NONEXISTENT")


@pytest.mark.parametrize(
    "info",
    [{"access_token": "secret"}, {"account_id": "123"}, {"nested": {"value": 1}}],
)
def test_sensitive_or_mutable_info_is_rejected(info: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        example_ticker(info=info)


def test_equal_tickers_with_metadata_are_hashable() -> None:
    left = example_ticker(info={"source_api_id": "ka10001", "source": "test"})
    right = example_ticker(info={"source": "test", "source_api_id": "ka10001"})
    assert left == right
    assert hash(left) == hash(right)
    assert {left, right} == {left}
    assert {left: "price"}[right] == "price"


def test_hash_includes_metadata_value_semantics() -> None:
    left = example_ticker(info={"source_api_id": "ka10001"})
    right = example_ticker(info={"source_api_id": "FHKST01010100"})
    assert left != right
    assert hash(left) == hash(left)  # Stable within a process.
    assert {left: "kiwoom", right: "kis"}[right] == "kis"


@pytest.mark.parametrize(
    "field_name",
    [
        "app-key",
        "app_key",
        "AppKey",
        "api-key",
        "api_key",
        "apiKey",
        "CANO",
        "cust-CANO",
        "acnt_no",
        "ACNT_PRDT_CD",
        "acct_no",
        "personalseckey",
        "PERSONALSECKEY",
        "refresh_token",
    ],
)
def test_broker_specific_credential_metadata_names_are_rejected(field_name: str) -> None:
    with pytest.raises(ValueError, match="authentication/account"):
        example_ticker(info={field_name: "redacted-for-test"})


def test_benign_metadata_keys_are_not_blocked_by_short_cano_name() -> None:
    ticker = example_ticker(
        info={"source_api_id": "FHKST01010100", "canonical_symbol": "005930"}
    )
    assert ticker.info["canonical_symbol"] == "005930"

