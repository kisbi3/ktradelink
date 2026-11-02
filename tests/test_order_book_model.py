"""Book contracts on synthetic quotes, not captured brokerage responses."""

import json
from dataclasses import FrozenInstanceError, fields, replace
from decimal import Decimal
from pathlib import Path

import pytest

from ktradelink.models import OrderBook, OrderBookLevel

ROOT = Path(__file__).resolve().parents[1]


def level(price: str = "70000", quantity: int = 1) -> OrderBookLevel:
    return OrderBookLevel(Decimal(price), quantity)


def example_book(**changes: object) -> OrderBook:
    args = dict(
        symbol="005930", venue="KRX", broker="synthetic",
        bids=(level("70000", 12), level("69900", 0)),
        asks=(level("70100", 9), level("70200", 20)), info={},
    )
    args.update(changes)
    return OrderBook(**args)


def test_fixture_fields_and_schema_match_model() -> None:
    path = ROOT / "tests/fixtures/spec/order-book-synthetic.json"
    raw = json.loads(path.read_text())
    assert raw.pop("_synthetic") is True
    raw.pop("_note")
    for side in ("bids", "asks"):
        raw[side] = tuple(OrderBookLevel(Decimal(price), size) for price, size in raw[side])
    book = OrderBook(**raw)
    for key, value in raw.items():
        assert getattr(book, key) == value
    assert book.bids[1].quantity == 0
    schema = json.loads((ROOT / "docs/specifications/normalized-models-v0.1.json").read_text())
    spec = schema["models"]["OrderBook"]
    assert {f.name for f in fields(OrderBook)} == set(spec["required"] + spec["optional"])
    assert not hasattr(book, "to_dict")
    assert not hasattr(book, "to_json")


@pytest.mark.parametrize(
    "bad", [None, True, 1, 1.0, "70000", Decimal("NaN"), Decimal("sNaN"),
            Decimal("Infinity"), Decimal("-1"), Decimal("-0"), Decimal(0)],
)
def test_invalid_level_prices(bad: object) -> None:
    with pytest.raises(ValueError):
        OrderBookLevel(bad, 1)


@pytest.mark.parametrize("bad", [None, True, -1, 1.5, "1", Decimal(1)])
def test_invalid_level_quantities(bad: object) -> None:
    with pytest.raises(ValueError):
        OrderBookLevel(Decimal(1), bad)


@pytest.mark.parametrize("side", ["bids", "asks"])
@pytest.mark.parametrize("bad", [None, [], {}, "", ((Decimal(1), 1),), (None,)])
def test_sides_require_typed_immutable_tuples(side: str, bad: object) -> None:
    with pytest.raises(TypeError):
        example_book(**{side: bad})


@pytest.mark.parametrize(
    "side,prices", [("bids", ("1", "2")), ("asks", ("2", "1")),
                    ("bids", ("1", "1.0")), ("asks", ("1.0", "1"))],
)
def test_unsorted_or_duplicate_levels_are_not_silently_repaired(
    side: str, prices: tuple[str, ...]
) -> None:
    with pytest.raises(ValueError, match="price-ordered"):
        example_book(**{side: tuple(level(price) for price in prices)})


@pytest.mark.parametrize("side", ["bids", "asks"])
def test_empty_or_one_sided_books_can_be_explicit(side: str) -> None:
    assert getattr(example_book(**{side: ()}), side) == ()
    assert example_book(bids=(), asks=()).bids == ()


def test_crossed_and_locked_books_not_misclassified_as_invalid_values() -> None:
    crossed = example_book(bids=(level("70200"),), asks=(level("70100"),))
    assert crossed.bids[0].price > crossed.asks[0].price
    locked = example_book(bids=(level(),), asks=(level(),))
    assert locked.bids[0].price == locked.asks[0].price


def test_no_universal_depth_limit_and_zero_quantity_preserved() -> None:
    bids = tuple(level(str(100 - i), i) for i in range(12))
    book = example_book(bids=bids, asks=())
    assert len(book.bids) == 12
    assert book.bids[0].quantity == 0


@pytest.mark.parametrize("name", ["timestamp", "retrieved_at"])
@pytest.mark.parametrize("bad", [True, -1, 1.0, "1"])
def test_invalid_times_not_replaced_by_local_clock(name: str, bad: object) -> None:
    with pytest.raises(ValueError):
        example_book(**{name: bad})


def test_frozen_nested_values_and_hash_equality() -> None:
    metadata = {"source": "synthetic", "counter": 0}
    book = example_book(info=metadata)
    same = example_book(info=dict(reversed(metadata.items())))
    assert book == same and hash(book) == hash(same)
    assert {book: "ok"}[same] == "ok"
    metadata["source"] = "changed"
    assert book.info["source"] == "synthetic"
    with pytest.raises(TypeError):
        book.info["source"] = "changed"
    with pytest.raises(FrozenInstanceError):
        book.bids = ()
    with pytest.raises(FrozenInstanceError):
        book.bids[0].quantity = 2
    assert not hasattr(book, "__dict__")
    assert not hasattr(book.bids[0], "__dict__")
    assert book != replace(book, timestamp=0)
    assert hash(level("1.0", 0)) == hash(level("1", 0))


@pytest.mark.parametrize("broker", ["kis", "kiwoom", "ls", "db", "toss", "meritz"])
def test_provider_name_is_provenance_not_a_functional_support_claim(broker: str) -> None:
    assert example_book(broker=broker).broker == broker


def test_metadata_and_composite_scope_checks() -> None:
    with pytest.raises(ValueError):
        example_book(venue="BROKER_COMPOSITE")
    with pytest.raises(ValueError):
        example_book(info={"personalseckey": "synthetic"})
    with pytest.raises(TypeError):
        example_book(info={"source": {"nested": 1}})
    assert example_book(timestamp=None, retrieved_at=0).timestamp is None
    assert example_book(venue="BROKER_COMPOSITE", scope_description="synthetic scope")
