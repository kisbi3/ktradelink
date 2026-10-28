"""Static design-contract checks; NOT tests of any broker adapter.

Only synthetic data and documentary capability candidates are validated here.
"""

import datetime
import json
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs" / "specifications"
FIXTURES = ROOT / "tests" / "fixtures" / "spec"


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def test_matrix_never_reports_unimplemented_api_as_supported() -> None:
    matrix = read_json(SPEC / "capability-matrix-v0.1.json")

    assert matrix["review_status"] == "proposed_not_approved"
    assert matrix["live_tested"] is False
    assert matrix["schema_version"] == 1
    assert {broker["id"] for broker in matrix["brokers"]} == {"kis", "kiwoom"}
    allowed_states = set(matrix["capability_states"])
    required_methods = {
        "load_markets",
        "fetch_ticker",
        "fetch_ohlcv",
        "fetch_order_book",
    }
    for broker in matrix["brokers"]:
        assert broker["adapter_implemented"] is False
        assert (ROOT / broker["evidence_file"]).is_file()
        capabilities = broker["capabilities"]
        assert {cap["method"] for cap in capabilities} == required_methods
        for cap in capabilities:
            assert cap["state"] in allowed_states
            assert cap["state"] != "supported"
            assert cap["implemented"] is False
            assert cap["normalized_contract_verified"] is False
            assert cap["real_environment"] == "unverified"
            assert cap["paper_environment"] == "unverified"
            assert cap["evidence_url"].startswith("https://")
            assert cap["requested_venues"] == ["KRX"]
            assert isinstance(cap["requested_timeframes"], list)


def test_synthetic_daily_timestamp_is_anchored_to_kst_session_date() -> None:
    candle = read_json(FIXTURES / "candle-day-synthetic.json")
    assert candle["_synthetic"] is True
    assert candle["venue"] == "KRX"
    assert candle["session_date"] == "2026-10-28"

    kst_anchor = datetime.datetime.combine(
        datetime.datetime.fromisoformat(candle["session_date"]).date(),
        datetime.time.min,
        tzinfo=ZoneInfo("Asia/Seoul"),
    )
    assert candle["timestamp"] == int(kst_anchor.timestamp() * 1000)
    # KST midnight is 15:00 UTC on the *previous* calendar day.
    assert datetime.datetime.fromtimestamp(
        candle["timestamp"] / 1000, tz=datetime.UTC
    ).date().isoformat() == "2026-10-27"

    for key in ("open", "high", "low", "close"):
        assert Decimal(candle[key]) > 0
    assert candle["volume"] >= 0


@pytest.mark.parametrize(
    ("side", "reverse"),
    [("bids", True), ("asks", False)],
)
def test_synthetic_book_levels_follow_documented_price_order(
    side: str, reverse: bool
) -> None:
    book = read_json(FIXTURES / "order-book-synthetic.json")
    assert book["_synthetic"] is True
    assert book["timestamp"] is None  # No invented native event timestamp.
    prices = [Decimal(price) for price, quantity in book[side]]
    quantities = [quantity for price, quantity in book[side]]

    assert prices == sorted(prices, reverse=reverse)
    assert all(isinstance(quantity, int) and quantity >= 0 for quantity in quantities)
    # A genuinely documented zero-size level is distinct from missing data.
    if side == "bids":
        assert 0 in quantities
