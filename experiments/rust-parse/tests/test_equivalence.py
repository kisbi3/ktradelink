"""End-to-end equality when the opt-in native extension is installed."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ktl_rust_parse_probe as rust_probe  # noqa: E402
from data import generate_payloads  # noqa: E402
from reference import python_parse_batch, python_parse_one, row_to_ticker  # noqa: E402


@pytest.mark.parametrize("count", [1, 2, 17, 257])
def test_raw_and_public_typed_results_equal_for_batch(count: int) -> None:
    payloads = generate_payloads(count)
    rust = rust_probe.parse_batch_json(payloads)
    python = python_parse_batch(payloads)
    assert rust == python
    assert [row_to_ticker(row) for row in rust] == [row_to_ticker(row) for row in python]
    assert rust_probe.parse_one_json(payloads[0]) == python_parse_one(payloads[0])


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
def test_both_parsers_reject_malformed_wire_types(message: str) -> None:
    with pytest.raises(ValueError):
        python_parse_one(message)
    with pytest.raises(ValueError):
        rust_probe.parse_one_json(message)


@pytest.mark.parametrize("value", ["-1", "-0", "NaN", "Infinity"])
def test_both_reject_unsafe_price_when_constructing_typed_model(value: str) -> None:
    message = json.dumps({"symbol": "005930", "venue": "KRX", "last": value})
    for raw in (python_parse_one(message), rust_probe.parse_one_json(message)):
        with pytest.raises(ValueError):
            row_to_ticker(raw)


def test_null_and_missing_fields_have_same_typed_semantics() -> None:
    for message in (
        '{"symbol":"005930","venue":"KRX"}',
        '{"symbol":"005930","venue":"KRX","last":null,"volume":0}',
    ):
        assert row_to_ticker(python_parse_one(message)) == row_to_ticker(
            rust_probe.parse_one_json(message)
        )
