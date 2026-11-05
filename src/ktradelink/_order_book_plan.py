"""Private, entirely offline order-book (호가) request planning.

Only KIS (``FHKST01010200``) and Kiwoom REST (``ka10004``) are planned: both
publisher examples select the KRX book explicitly. LS ``t1101`` can be decoded
offline but is NOT planned, because its request documents no exchange
selector (see docs/brokers/order-book-evidence-2026-11-05.md). DB, Toss and
Meritz have no evidenced order-book decoder.

No OAuth exchange, secrets, token management, HTTP client, transport wiring
or public ``fetch_order_book``. A plan is an immutable TEMPLATE of public,
non-secret values; executing it needs a separately reviewed transport.
"""

import json
from dataclasses import dataclass

from ktradelink._request_plan import (
    AuthRequirements,
    OfflineResponseRejected,
    QuotePlanUnavailable,
    _checked_symbol,
    _origin,
    authentication_requirements,
)
from ktradelink.models import OrderBook

#: Levels per side documented by every planned publisher route.
ORDER_BOOK_DEPTH = 10

_PLANNED = ("kis", "kiwoom")


@dataclass(frozen=True, slots=True)
class OrderBookRequestPlan:
    """Immutable fixed-origin order-book request metadata, never a request.

    ``limit`` is the per-side output cap applied by the offline decoder
    (``None`` = all documented levels). The caller's venue is the selector
    sent to the publisher, NOT proof of the venue of the returned book.
    """

    broker: str
    environment: str
    symbol: str
    venue: str
    limit: int | None
    method: str
    origin: str
    path: str
    query: tuple[tuple[str, str], ...]
    public_headers: tuple[tuple[str, str], ...]
    json_body: str | None
    auth: AuthRequirements
    evidence_level: str
    transport_implemented: bool = False


def _checked_limit(limit: object) -> int | None:
    if limit is None:
        return None
    if type(limit) is not int or limit < 1:
        raise QuotePlanUnavailable("Order-book limit must be a positive int or None")
    if limit > ORDER_BOOK_DEPTH:
        raise QuotePlanUnavailable("Order-book limit exceeds the documented source depth")
    return limit


def plan_order_book_request(
    broker: str, symbol: str, *, venue: str, environment: str, limit: int | None = None
) -> OrderBookRequestPlan:
    """Construct an offline publisher-example order-book TEMPLATE for one KR symbol.

    No network sending or authentication is performed. ``limit`` beyond the
    documented ten levels per side is rejected, never clamped.
    """
    origin = _origin(broker, environment)
    if broker == "ls":
        raise QuotePlanUnavailable(
            "LS t1101 documents no exchange selector; a KRX book cannot be requested"
        )
    if broker not in _PLANNED:
        raise QuotePlanUnavailable("No evidenced order-book route for this broker")
    if venue != "KRX":
        raise QuotePlanUnavailable("Venue not verified for this offline route")
    code = _checked_symbol(broker, symbol)
    checked_limit = _checked_limit(limit)
    auth = authentication_requirements(broker, environment=environment)

    query: tuple[tuple[str, str], ...] = ()
    json_body: str | None = None
    if broker == "kis":
        # KIS open-trading-api 3a9be59 inquire_asking_price_exp_ccn.py: the
        # same tr_id for real and demo; J = KRX. kis_auth._url_fetch adds
        # custtype "P" (individual/corporate customer) and an empty tr_cont.
        method = "GET"
        path = "/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn"
        query = (("FID_COND_MRKT_DIV_CODE", "J"), ("FID_INPUT_ISCD", code))
        public_headers: tuple[tuple[str, str], ...] = (
            ("tr_id", "FHKST01010200"),
            ("custtype", "P"),
            ("tr_cont", ""),
        )
    else:
        # Kiwoom REST-API 953e5db ka10004: a bare 6-digit stk_cd is the KRX
        # code (NXT is "_NX", SOR "_AL"; neither is offered here).
        method = "POST"
        path = "/api/dostk/mrkcond"
        public_headers = (
            ("api-id", "ka10004"),
            ("content-type", "application/json;charset=UTF-8"),
        )
        json_body = json.dumps({"stk_cd": code}, separators=(",", ":"))

    return OrderBookRequestPlan(
        broker=broker,
        environment=environment,
        symbol=code,
        venue=venue,
        limit=checked_limit,
        method=method,
        origin=origin,
        path=path,
        query=query,
        public_headers=public_headers,
        json_body=json_body,
        auth=auth,
        evidence_level="publisher_order_book_example",
    )


def decode_offline_order_book_response(
    plan: OrderBookRequestPlan, *, http_status: int, json_text: str
) -> OrderBook:
    """Test-only status gate -> native order-book decoder -> Python OrderBook.

    Nothing is sent. The HTTP status and JSON are caller-supplied, NOT a
    vouched broker response. Never log the body; it may hold sensitive data.
    """
    if type(plan) is not OrderBookRequestPlan:
        raise QuotePlanUnavailable("Invalid offline order-book plan")
    expected = plan_order_book_request(
        plan.broker, plan.symbol, venue=plan.venue, environment=plan.environment,
        limit=plan.limit,
    )
    if plan != expected:
        raise QuotePlanUnavailable("Unrecognized or modified offline order-book plan")
    if type(http_status) is not int or not 200 <= http_status < 300:
        raise OfflineResponseRejected("Offline HTTP response is not successful")
    if type(json_text) is not str:
        raise OfflineResponseRejected("Offline response body must be JSON text")
    from ktradelink._native import decode_order_book_candidate

    return decode_order_book_candidate(
        plan.broker, plan.symbol, plan.venue, json_text, limit=plan.limit
    )
