"""Regression cases for the shared primitives; no broker data is used."""

from decimal import Decimal

import pytest

from ktradelink.models import Ticker
from ktradelink.models._validation import freeze_info, validate_integer, validate_price


@pytest.mark.parametrize("bad", [True, -1, 1.5, "1", Decimal(1)])
def test_integer_validation_does_not_coerce(bad: object) -> None:
    with pytest.raises(ValueError):
        validate_integer("quantity", bad, nullable=False)


@pytest.mark.parametrize("bad", [None, True, 0, 1.0, "1", Decimal("sNaN"), Decimal("-0")])
def test_required_price_validation(bad: object) -> None:
    with pytest.raises(ValueError):
        validate_price("price", bad, nullable=False)


def test_optional_values_and_zero_remain_distinct() -> None:
    validate_price("last", None)
    validate_price("last", Decimal(0))
    validate_integer("volume", None)
    validate_integer("volume", 0)
    with pytest.raises(ValueError):
        validate_integer("volume", None, nullable=False)


@pytest.mark.parametrize("key", ["app.key", "APP_KEY", "api-key", "CANO", "ACNT_PRDT_CD"])
def test_known_secret_aliases_rejected(key: str) -> None:
    with pytest.raises(ValueError):
        freeze_info({key: "synthetic-test-value"})


def test_ticker_regression_signature_hash_and_metadata() -> None:
    metadata = {"source_api_id": "synthetic", "canonical_symbol": "0101N0"}
    quote = Ticker("0101N0", "KRX", "synthetic", Decimal(0), metadata)
    equal = Ticker("0101N0", "KRX", "synthetic", Decimal(0), dict(reversed(metadata.items())))
    assert quote == equal
    assert hash(quote) == hash(equal)
    metadata["source_api_id"] = "changed"
    assert quote.info["source_api_id"] == "synthetic"
    assert quote.timestamp is None
    assert quote.volume is None
    assert not hasattr(quote, "to_dict")
    assert not hasattr(quote, "__dict__")
