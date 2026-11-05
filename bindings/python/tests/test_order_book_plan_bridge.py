"""Offline order-book plan -> REAL native decoder -> existing OrderBook.

The HTTP status and body are caller-supplied synthetic inputs; nothing is sent.
"""

from decimal import Decimal
from pathlib import Path

import pytest

from ktradelink._order_book_plan import (
    decode_offline_order_book_response,
    plan_order_book_request,
)
from ktradelink._request_plan import OfflineResponseRejected
from ktradelink.models import OrderBook

FIXTURES = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "order_book"
FILES = {"kis": "kis-fhkst01010200-synthetic.json", "kiwoom": "kiwoom-ka10004-synthetic.json"}


@pytest.mark.parametrize("broker", list(FILES))
@pytest.mark.parametrize("limit", [None, 1, 10])
def test_planned_route_decodes_synthetic_book(broker: str, limit) -> None:
    plan = plan_order_book_request(broker, "005930", venue="KRX", environment="live",
                                   limit=limit)
    text = (FIXTURES / FILES[broker]).read_text(encoding="utf-8")
    book = decode_offline_order_book_response(plan, http_status=200, json_text=text)
    assert type(book) is OrderBook
    assert (book.symbol, book.venue, book.broker) == ("005930", "KRX", broker)
    depth = limit or 10
    assert len(book.bids) == len(book.asks) == depth
    assert book.bids[0].price == Decimal("70000") and book.asks[0].price == Decimal("70100")
    assert book.timestamp is None and book.info == {}


def test_native_errors_surface_unchanged() -> None:
    plan = plan_order_book_request("kis", "005930", venue="KRX", environment="live")
    with pytest.raises(ValueError, match="rt_cd: MissingRequired"):
        decode_offline_order_book_response(plan, http_status=200, json_text='{"output1":{}}')
    with pytest.raises(OfflineResponseRejected):
        decode_offline_order_book_response(plan, http_status=500, json_text="{}")
