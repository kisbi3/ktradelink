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

def test_synthetic_model_fixtures_match_spec_required_fields() -> None:
    """Compare the machine-readable proposal, its Markdown table and fixtures."""
    import re

    schema = read_json(SPEC / "normalized-models-v0.1.json")
    assert schema["status"] == "proposed_not_approved"
    assert schema["conditional_required"]["venue=BROKER_COMPOSITE"] == [
        "scope_description"
    ]
    assert set(schema["models"]) == {"Ticker", "Candle", "OrderBook"}
    markdown = (SPEC / "market-data-v0.1-draft.md").read_text(encoding="utf-8")

    for model_name, model in schema["models"].items():
        fixture = read_json(FIXTURES / model["fixture"])
        assert fixture["_synthetic"] is True

        required, optional = set(model["required"]), set(model["optional"])
        assert not (required & optional)
        assert {"symbol", "venue", "broker", "info"} <= required
        assert "scope_description" in optional

        actual = set(fixture) - {"_synthetic", "_note"}
        assert required <= actual, f"{model_name} missing: {required - actual}"
        assert actual <= (required | optional), f"{model_name} unexpected: {actual - required - optional}"
        assert isinstance(fixture["info"], dict)

        table_row = next(
            row for row in markdown.splitlines() if row.startswith(f"| {model_name} |")
        )
        cells = [cell.strip() for cell in table_row.strip("|").split("|")]
        assert len(cells) == 3
        md_required = set(re.findall(r"`([^`]+)`", cells[1]))
        md_optional = set(re.findall(r"`([^`]+)`", cells[2]))
        assert required == md_required, f"{model_name} required keys differ from Markdown"
        assert optional == md_optional, f"{model_name} optional keys differ from Markdown"


def test_synthetic_ticker_distinguishes_last_and_previous_close() -> None:
    ticker = read_json(FIXTURES / "ticker-synthetic.json")

    assert ticker["_synthetic"] is True
    assert ticker["venue"] == "KRX"
    assert ticker["timestamp"] is None
    assert ticker["retrieved_at"] is not None
    assert ticker["info"] == {}
    assert Decimal(ticker["last"]) != Decimal(ticker["previous_close"])
    assert ticker["bid"] is None
    assert ticker["ask"] is None
    assert "close" not in ticker


def test_synthetic_candle_provenance_is_explicit() -> None:
    candle = read_json(FIXTURES / "candle-day-synthetic.json")
    assert candle["info"] == {}
    assert candle["adjustment"] == "raw"
    assert candle["session"] == "regular"


def test_proposed_history_query_policy_has_finite_scope() -> None:
    policy = read_json(SPEC / "history-query-v0.1.json")
    assert policy["status"] == "proposed_not_approved"
    assert policy["since_requires_until"] is True
    assert policy["until_exclusive"] is True
    assert policy["output_order"] == "oldest_first"
    assert policy["provider_request_budget"] == "finite_per_adapter"
    assert policy["on_incomplete_range"] == "raise_incomplete_market_data"

