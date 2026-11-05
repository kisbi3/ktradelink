"""Offline order-book request templates: no network, no secrets, no live API."""

import dataclasses
import json
import socket
import subprocess
import sys

import pytest

from ktradelink._order_book_plan import (
    ORDER_BOOK_DEPTH,
    OrderBookRequestPlan,
    decode_offline_order_book_response,
    plan_order_book_request,
)
from ktradelink._request_plan import (
    OfflineResponseRejected,
    QuotePlanUnavailable,
    authentication_requirements,
    plan_ticker_request,
)

LIVE = {
    "kis": (
        "GET",
        "https://openapi.koreainvestment.com:9443",
        "/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn",
        (("FID_COND_MRKT_DIV_CODE", "J"), ("FID_INPUT_ISCD", "005930")),
        (("tr_id", "FHKST01010200"), ("custtype", "P"), ("tr_cont", "")),
        None,
    ),
    "kiwoom": (
        "POST",
        "https://api.kiwoom.com",
        "/api/dostk/mrkcond",
        (),
        (("api-id", "ka10004"), ("content-type", "application/json;charset=UTF-8")),
        '{"stk_cd":"005930"}',
    ),
}
PAPER_ORIGINS = {
    "kis": "https://openapivts.koreainvestment.com:29443",
    "kiwoom": "https://mockapi.kiwoom.com",
}


@pytest.fixture(autouse=True)
def _no_sockets(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("offline planning must not open sockets")

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)


@pytest.mark.parametrize("broker", list(LIVE))
def test_templates_match_the_pinned_publisher_examples(broker: str) -> None:
    plan = plan_order_book_request(broker, "005930", venue="KRX", environment="live")
    assert type(plan) is OrderBookRequestPlan
    assert (plan.method, plan.origin, plan.path, plan.query, plan.public_headers,
            plan.json_body) == LIVE[broker]
    assert (plan.broker, plan.symbol, plan.venue, plan.limit) == (broker, "005930", "KRX", None)
    assert plan.evidence_level == "publisher_order_book_example"
    assert plan.transport_implemented is False
    assert plan.auth == authentication_requirements(broker, environment="live")
    assert plan.auth.token_exchange_implemented is False
    with pytest.raises(dataclasses.FrozenInstanceError):
        plan.path = "/elsewhere"


@pytest.mark.parametrize("broker", list(LIVE))
def test_paper_uses_the_documented_paper_origin_and_same_route(broker: str) -> None:
    live = plan_order_book_request(broker, "005930", venue="KRX", environment="live")
    paper = plan_order_book_request(broker, "005930", venue="KRX", environment="paper")
    assert paper.origin == PAPER_ORIGINS[broker]
    assert (paper.method, paper.path, paper.query, paper.public_headers, paper.json_body) == (
        live.method, live.path, live.query, live.public_headers, live.json_body)


def test_order_book_route_differs_from_the_ticker_route() -> None:
    for broker in LIVE:
        book = plan_order_book_request(broker, "005930", venue="KRX", environment="live")
        quote = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
        assert (book.path, book.public_headers) != (quote.path, quote.public_headers)


@pytest.mark.parametrize("broker,environment,message", [
    ("ls", "live", "no exchange selector"),
    ("ls", "paper", "environment"),
    ("db", "live", "No evidenced order-book route"),
    ("toss", "live", "No evidenced order-book route"),
    ("meritz", "live", "No evidenced order-book route"),
    ("shinhan", "live", "Unknown"),
    ("kis", "demo", "environment"),
])
def test_unplanned_brokers_and_environments_fail_closed(broker, environment, message) -> None:
    with pytest.raises(QuotePlanUnavailable, match=message):
        plan_order_book_request(broker, "005930", venue="KRX", environment=environment)


@pytest.mark.parametrize("venue", ["NXT", "BROKER_COMPOSITE", "krx", "", None])
def test_only_explicit_krx_is_planned(venue) -> None:
    for broker in LIVE:
        with pytest.raises(QuotePlanUnavailable, match="Venue"):
            plan_order_book_request(broker, "005930", venue=venue, environment="live")


@pytest.mark.parametrize("symbol", ["5930", "0059300", "005930_NX", "００５９３０",
                                    5930, None, " 05930", "0000d0", "A005930",
                                    "Q500001", "0000Ｄ0"])
def test_symbols_reuse_the_quote_route_check(symbol) -> None:
    for broker in LIVE:
        with pytest.raises(QuotePlanUnavailable, match="Symbol"):
            plan_order_book_request(broker, symbol, venue="KRX", environment="live")


@pytest.mark.parametrize("symbol", ["0000D0", "0101N0", "00593A"])
def test_alphanumeric_symbols_follow_the_per_broker_rule(symbol) -> None:
    # ADR 0016: KIS master files carry such codes; Kiwoom documents neither
    # show nor exclude them. Gateway acceptance is NOT verified.
    with pytest.raises(QuotePlanUnavailable, match="Symbol"):
        plan_order_book_request("kiwoom", symbol, venue="KRX", environment="live")
    kis = plan_order_book_request("kis", symbol, venue="KRX", environment="live")
    assert kis.symbol == symbol
    assert kis.query == (("FID_COND_MRKT_DIV_CODE", "J"), ("FID_INPUT_ISCD", symbol))


def test_limit_is_a_documented_per_side_cap() -> None:
    assert ORDER_BOOK_DEPTH == 10
    for limit in (1, 5, 10):
        assert plan_order_book_request("kis", "005930", venue="KRX", environment="live",
                                       limit=limit).limit == limit
    with pytest.raises(QuotePlanUnavailable, match="exceeds the documented"):
        plan_order_book_request("kis", "005930", venue="KRX", environment="live", limit=11)
    for bad in (0, -1, True, 2.0, "3"):
        with pytest.raises(QuotePlanUnavailable, match="positive int"):
            plan_order_book_request("kiwoom", "005930", venue="KRX", environment="live",
                                    limit=bad)


def test_plans_hold_no_secret_values() -> None:
    plan = plan_order_book_request("kis", "005930", venue="KRX", environment="live")
    names = {name.lower() for name, _ in plan.public_headers}
    assert not names & {"authorization", "appkey", "appsecret", "secretkey"}
    assert "Bearer" not in repr(plan)


def _plan(broker="kiwoom", **kwargs):
    return plan_order_book_request(broker, "005930", venue="KRX", environment="live", **kwargs)


@pytest.mark.parametrize("change", [
    {"path": "/api/dostk/stkinfo"},
    {"origin": "https://example.invalid"},
    {"json_body": '{"stk_cd":"005930_NX"}'},
    {"public_headers": (("api-id", "ka10001"),)},
    {"venue": "NXT"},
    {"limit": 11},
    {"limit": True},
    {"transport_implemented": True},
])
def test_modified_plans_are_rejected_before_decoding(change) -> None:
    tampered = dataclasses.replace(_plan(), **change)
    with pytest.raises(QuotePlanUnavailable):
        decode_offline_order_book_response(tampered, http_status=200, json_text="{}")


def test_non_plans_are_rejected() -> None:
    quote = plan_ticker_request("kiwoom", "005930", venue="KRX", environment="live")
    for bad in (quote, None, {"broker": "kiwoom"}):
        with pytest.raises(QuotePlanUnavailable, match="Invalid"):
            decode_offline_order_book_response(bad, http_status=200, json_text="{}")


@pytest.mark.parametrize("status", [199, 201, 204, 299, 300, 404, 500, True, "200", 200.0,
                                    None])
def test_unsuccessful_or_untyped_http_status_never_reaches_the_decoder(
    status, monkeypatch
) -> None:
    import ktradelink._native as native

    monkeypatch.setattr(native, "decode_order_book_candidate",
                        lambda *a, **k: pytest.fail("decoder must not run"))
    with pytest.raises(OfflineResponseRejected):
        decode_offline_order_book_response(_plan(), http_status=status, json_text="{}")


@pytest.mark.parametrize("body", [b"{}", None, {}, 1])
def test_body_must_be_text(body) -> None:
    with pytest.raises(OfflineResponseRejected, match="JSON text"):
        decode_offline_order_book_response(_plan(), http_status=200, json_text=body)


def test_plan_limit_is_forwarded_to_the_decoder(monkeypatch) -> None:
    import ktradelink._native as native

    seen = {}

    def fake(*args, **kwargs):
        seen.update(args=args, kwargs=kwargs)
        return "sentinel"

    monkeypatch.setattr(native, "decode_order_book_candidate", fake)
    result = decode_offline_order_book_response(_plan("kis", limit=4), http_status=200,
                                                json_text=json.dumps({}))
    assert result == "sentinel"
    assert seen == {"args": ("kis", "005930", "KRX", "{}"), "kwargs": {"limit": 4}}


def test_module_import_does_not_load_the_native_extension() -> None:
    code = (
        "import sys\n"
        "from typing import get_type_hints\n"
        "from ktradelink._order_book_plan import decode_offline_order_book_response\n"
        "from ktradelink.models import OrderBook\n"
        "assert get_type_hints(decode_offline_order_book_response)['return'] is OrderBook\n"
        "assert 'ktradelink._native' not in sys.modules\n"
        "assert '_ktradelink_native' not in sys.modules\n"
    )
    subprocess.run([sys.executable, "-I", "-c", code], check=True)
