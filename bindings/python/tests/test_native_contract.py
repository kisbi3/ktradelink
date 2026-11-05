"""Real extension tests. A missing native module MUST fail, never silently skip."""

from dataclasses import FrozenInstanceError, fields
from decimal import Decimal, localcontext

import _ktradelink_native as native
import pytest

from ktradelink._native import build_ticker, core_version
from ktradelink.models import Ticker

PRICE_FIELDS = ("last", "open", "high", "low", "previous_close", "bid", "ask")


def quote(**kwargs) -> Ticker:
    return build_ticker("005930", "KRX", "synthetic", **kwargs)


def test_versions_and_exact_return_type() -> None:
    assert native.CONTRACT_VERSION == 2
    assert core_version() == "0.1.0"
    assert type(quote()) is Ticker
    assert not hasattr(quote(), "to_dict")
    assert not hasattr(quote(), "__dict__")


def test_all_fields_equal_existing_python_constructor() -> None:
    values = dict(last="70500.00", open="70000", high="71000", low="69000",
                  previous_close="69800", bid="70400", ask="70600")
    actual = quote(**values, volume=0, timestamp=None, retrieved_at=1793113200000)
    expected = Ticker(
        "005930", "KRX", "synthetic", **{k: Decimal(v) for k, v in values.items()},
        volume=0, timestamp=None, retrieved_at=1793113200000,
    )
    assert actual == expected and hash(actual) == hash(expected)
    for field in fields(Ticker):
        assert getattr(actual, field.name) == getattr(expected, field.name)
    assert actual.info == {}
    with pytest.raises(FrozenInstanceError):
        actual.last = Decimal(1)


@pytest.mark.parametrize("field", PRICE_FIELDS)
def test_price_precision_and_scale_preserved(field: str) -> None:
    text = "9007199254740993.1234567890123456789012345678900"
    with localcontext() as ctx:
        ctx.prec = 6
        value = getattr(quote(**{field: text}), field)
        assert value.as_tuple() == Decimal(text).as_tuple()


@pytest.mark.parametrize("field", PRICE_FIELDS)
@pytest.mark.parametrize("bad", ["-0", "-1", "+1", "NaN", "sNaN", "Infinity", "1e3", "1.", ".1", " 1", "１", "\ud800"])
def test_bad_price_text_rejected(field: str, bad: str) -> None:
    with pytest.raises((ValueError, UnicodeError)):
        quote(**{field: bad})


@pytest.mark.parametrize("bad", [True, 1, 1.5, Decimal("1"), b"1"])
def test_price_wire_types_not_coerced(bad: object) -> None:
    with pytest.raises(TypeError):
        quote(last=bad)


@pytest.mark.parametrize("field", ["volume", "timestamp", "retrieved_at"])
@pytest.mark.parametrize("bad", [True, -1, 2**64, 1.0, "1"])
def test_integer_type_and_bounds(field: str, bad: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        quote(**{field: bad})


@pytest.mark.parametrize("field", ["volume", "timestamp", "retrieved_at"])
def test_zero_none_and_u64_max_are_distinct(field: str) -> None:
    for value in [None, 0, 2**64 - 1]:
        assert getattr(quote(**{field: value}), field) == value


@pytest.mark.parametrize("symbol", ["", "005 930", "005930\n", "\u200b005930", "종목"])
def test_private_ascii_identifier_boundary(symbol: str) -> None:
    with pytest.raises(ValueError):
        build_ticker(symbol, "KRX", "synthetic")


def test_alphanumeric_symbol_and_composite_provenance() -> None:
    assert build_ticker("0101N0", "KRX", "synthetic").symbol == "0101N0"
    with pytest.raises(ValueError):
        build_ticker("005930", "BROKER_COMPOSITE", "synthetic")
    ticker = build_ticker("005930", "BROKER_COMPOSITE", "synthetic", scope_description="synthetic scope")
    assert ticker.scope_description == "synthetic scope"
    with pytest.raises(ValueError):
        build_ticker("005930", "BROKER_COMPOSITE", "synthetic", scope_description="hidden\u200bscope")


def test_errors_do_not_echo_price_or_accept_upstream_metadata() -> None:
    with pytest.raises(ValueError) as error:
        quote(last="secret-synthetic-value")
    assert "secret-synthetic-value" not in str(error.value)
    with pytest.raises(TypeError):
        native._build_ticker("005930", "KRX", "synthetic", info={"access_token": "x"})


def test_native_entry_point_cannot_bypass_integer_checks() -> None:
    with pytest.raises(TypeError):
        native._build_ticker("005930", "KRX", "synthetic", volume=True)
