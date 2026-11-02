"""Pure-Python experimental reference tests (work without Rust extension)."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data import generate_payloads  # noqa: E402
from reference import python_parse_batch, python_parse_one, row_to_ticker  # noqa: E402


def test_reference_round_trip_to_real_typed_ticker() -> None:
    payloads = generate_payloads(23)
    result = [row_to_ticker(row) for row in python_parse_batch(payloads)]
    assert len(result) == 23
    assert result[0].last is not None
    assert result[0].info == {}
    assert result[1].symbol == "0101N0"
    assert result[2].timestamp is not None
    assert result[0].timestamp is None
    assert not hasattr(result[0], "to_dict")
    assert row_to_ticker(python_parse_one(payloads[0])) == result[0]


@pytest.mark.parametrize(
    "message",
    [
        "[]",
        "{}",
        '{"symbol":"005930","venue":"KRX","unknown":1}',
        '{"symbol":"005930","venue":"KRX","last":70500}',
        '{"symbol":"005930","venue":"KRX","volume":true}',
        '{"symbol":"005930","venue":"KRX","timestamp":-1}',
        '{"symbol":123,"venue":"KRX"}',
        '{"symbol":"005930","venue":"KRX","last":null,"last":"1"}',
        '{"symbol":"005930","venue":"KRX","volume":NaN}',
    ],
)
def test_reference_rejects_malformed_synthetic_schema(message: str) -> None:
    with pytest.raises(ValueError):
        python_parse_one(message)


def test_native_value_model_rejects_signed_and_nonfinite_prices() -> None:
    for invalid in ["-0", "-10", "NaN", "Infinity"]:
        raw = json.dumps({"symbol": "005930", "venue": "KRX", "last": invalid})
        with pytest.raises(ValueError):
            row_to_ticker(python_parse_one(raw))
