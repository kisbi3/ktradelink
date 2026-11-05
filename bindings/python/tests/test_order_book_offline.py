"""Offline KIS/Kiwoom/LS order-book candidates through the REAL extension.

Fixtures are synthetic values in publisher-documented layouts (see
tests/fixtures/order_book/README.md). No account, token or network call.
"""

import json
from dataclasses import FrozenInstanceError
from decimal import Decimal
from pathlib import Path

import _ktradelink_native as native
import pytest

from ktradelink._native import decode_order_book_candidate
from ktradelink.models import OrderBook, OrderBookLevel

FIXTURES = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "order_book"
FILES = {
    "kis": "kis-fhkst01010200-synthetic.json",
    "kiwoom": "kiwoom-ka10004-synthetic.json",
    "ls": "ls-t1101-synthetic.json",
}
ASKS = tuple(OrderBookLevel(Decimal(70100 + 100 * i), q)
             for i, q in enumerate((9, 20, 0, 31, 42, 53, 64, 75, 86, 97)))
BIDS = tuple(OrderBookLevel(Decimal(70000 - 100 * i), q)
             for i, q in enumerate((12, 0, 23, 34, 45, 56, 67, 78, 89, 90)))


def payload(broker: str) -> str:
    return (FIXTURES / FILES[broker]).read_text(encoding="utf-8")


def book_row(broker: str, doc: dict) -> dict:
    return {"kis": lambda: doc["output1"], "kiwoom": lambda: doc,
            "ls": lambda: doc["t1101OutBlock"]}[broker]()


@pytest.mark.parametrize("broker", list(FILES))
def test_publisher_shapes_return_the_existing_order_book(broker: str) -> None:
    book = decode_order_book_candidate(broker, "005930", "KRX", payload(broker))
    assert type(book) is OrderBook
    assert (book.symbol, book.venue, book.broker) == ("005930", "KRX", broker)
    assert book.asks == ASKS and book.bids == BIDS
    assert all(type(level) is OrderBookLevel for level in book.asks + book.bids)
    assert all(type(level.price) is Decimal and type(level.quantity) is int
               for level in book.asks + book.bids)
    assert book.timestamp is None and book.retrieved_at is None
    assert book.scope_description is None and book.info == {}
    assert book == OrderBook("005930", "KRX", broker, BIDS, ASKS)
    with pytest.raises(FrozenInstanceError):
        book.bids = ()


@pytest.mark.parametrize("broker", list(FILES))
def test_limit_is_per_side_and_never_clamped(broker: str) -> None:
    book = decode_order_book_candidate(broker, "005930", "KRX", payload(broker), limit=2)
    assert book.asks == ASKS[:2] and book.bids == BIDS[:2]
    for limit, message in [(0, "limit: InvalidLimit"), (11, "limit: DepthExceeded"),
                           (2**64 - 1, "limit: DepthExceeded")]:
        with pytest.raises(ValueError, match=message):
            decode_order_book_candidate(broker, "005930", "KRX", payload(broker), limit=limit)
    with pytest.raises(TypeError):
        decode_order_book_candidate(broker, "005930", "KRX", payload(broker), limit=True)
    with pytest.raises(TypeError):
        decode_order_book_candidate(broker, "005930", "KRX", payload(broker), limit=2.0)
    with pytest.raises(ValueError):
        decode_order_book_candidate(broker, "005930", "KRX", payload(broker), limit=-1)


def test_native_function_requires_keyword_limit() -> None:
    with pytest.raises(TypeError):
        native._decode_order_book_candidate("kis", "005930", "KRX", payload("kis"), 3)


@pytest.mark.parametrize("broker", list(FILES))
def test_zero_price_levels_fail_closed_instead_of_shortening_a_side(broker: str) -> None:
    """No publisher documents an empty-rank encoding, so a 0/0 level is never
    dropped (ADR 0003; ChatGPT review of PR #29, M1)."""
    zero = 0 if broker == "ls" else "0"
    keys = {"kis": ("bidp{}", "bidp_rsqn{}"), "ls": ("bidho{}", "bidrem{}"),
            "kiwoom": ("buy_{}th_pre_bid", "buy_{}th_pre_req")}[broker]
    doc = json.loads(payload(broker))
    for n in (9, 10):
        book_row(broker, doc)[keys[0].format(n)] = zero
        book_row(broker, doc)[keys[1].format(n)] = zero
    with pytest.raises(ValueError) as caught:
        decode_order_book_candidate(broker, "005930", "KRX", json.dumps(doc))
    assert str(caught.value) == f"{keys[0].format(9)}: UnverifiedEmptyLevel"
    # A limit that hides the 0/0 ranks does not turn it into a valid book.
    with pytest.raises(ValueError, match="UnverifiedEmptyLevel"):
        decode_order_book_candidate(broker, "005930", "KRX", json.dumps(doc), limit=2)
    book_row(broker, doc)[keys[1].format(9)] = 1 if broker == "ls" else "1"
    with pytest.raises(ValueError, match="InvalidPrice"):
        decode_order_book_candidate(broker, "005930", "KRX", json.dumps(doc))


@pytest.mark.parametrize("broker,status", [
    ("kis", {"rt_cd": "1"}), ("kiwoom", {"return_code": "0"}), ("ls", {"rsp_cd": "00001"}),
])
def test_wrong_status_is_rejected_without_echo(broker: str, status: dict) -> None:
    doc = json.loads(payload(broker)) | status
    with pytest.raises(ValueError, match="SourceStatus") as caught:
        decode_order_book_candidate(broker, "005930", "KRX", json.dumps(doc))
    assert str(caught.value) == f"{next(iter(status))}: SourceStatus"


@pytest.mark.parametrize("broker", list(FILES))
def test_missing_status_is_rejected(broker: str) -> None:
    key = {"kis": "rt_cd", "kiwoom": "return_code", "ls": "rsp_cd"}[broker]
    doc = json.loads(payload(broker))
    del doc[key]
    with pytest.raises(ValueError, match=f"{key}: MissingRequired"):
        decode_order_book_candidate(broker, "005930", "KRX", json.dumps(doc))


def test_signed_kiwoom_price_is_rejected_not_abs() -> None:
    doc = json.loads(payload("kiwoom"))
    doc["buy_fpr_bid"] = "-70000"
    with pytest.raises(ValueError, match="buy_fpr_bid: InvalidPrice") as caught:
        decode_order_book_candidate("kiwoom", "005930", "KRX", json.dumps(doc))
    assert "70000" not in str(caught.value)


@pytest.mark.parametrize("broker,venue,symbol,message", [
    ("kis", "NXT", "005930", "venue: UnsupportedVenue"),
    ("kis", "BROKER_COMPOSITE", "005930", "venue: UnsupportedVenue"),
    ("ls", "KRX", "005 930", "symbol: CoreValidation"),
    ("db", "KRX", "005930", "broker: UnsupportedBroker"),
    ("toss", "KRX", "005930", "broker: UnsupportedBroker"),
    ("meritz", "KRX", "005930", "broker: UnsupportedBroker"),
    ("shinhan", "KRX", "005930", "broker: UnknownBroker"),
])
def test_invalid_context_fails_before_parsing(broker, venue, symbol, message) -> None:
    with pytest.raises(ValueError, match=message):
        decode_order_book_candidate(broker, symbol, venue, "not-json")


def test_ls_symbol_echo_must_match() -> None:
    with pytest.raises(ValueError, match="shcode: AmbiguousSymbol"):
        decode_order_book_candidate("ls", "000660", "KRX", payload("ls"))


@pytest.mark.parametrize("broker", list(FILES))
def test_strict_json_and_size_bound(broker: str) -> None:
    text = payload(broker)
    for bad in ["{", text.replace("{", '{"_note": 1,', 1), text + " " * (1_048_577 - len(text))]:
        with pytest.raises(ValueError):
            decode_order_book_candidate(broker, "005930", "KRX", bad)
