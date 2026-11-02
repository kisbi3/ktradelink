"""Real PyO3 binding tests for offline request planning + six synthetic quotes.

No API credentials, TLS sockets, HTTP requests, account numbers or orders.
A fake HTTP status is an explicitly caller-supplied test input.
"""

import dataclasses
import json
from decimal import Decimal

import pytest

from ktradelink._request_plan import (
    OfflineResponseRejected,
    QuotePlanUnavailable,
    authentication_requirements,
    decode_offline_quote_response,
    plan_ticker_request,
)
from ktradelink.models import Ticker

FIXTURES = {
    "kis": {"rt_cd": "0", "output": {"stck_prpr": "72000.00", "acml_vol": "0"}},
    "kiwoom": {
        "return_code": 0, "stk_cd": "005930", "cur_prc": "72000.00",
        "trde_qty": "0",
    },
    "ls": {"shcode": "005930", "price": "72000.00"},
    "db": {"rsp_cd": "00000", "Out": {"Prpr": "72000.00"}},
    "toss": {"result": [{
        "symbol": "005930", "currency": "KRW", "lastPrice": "72000.00"
    }]},
    "meritz": {"rsp_cd": "0000", "data": {
        "stck_prpr": "72000.00", "acml_vol": "0"
    }},
}


@pytest.mark.parametrize("broker", list(FIXTURES))
def test_prepared_offline_request_to_native_ticker_no_network(broker: str) -> None:
    plan = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
    response = json.dumps(FIXTURES[broker])
    quote = decode_offline_quote_response(plan, http_status=200, json_text=response)
    assert type(quote) is Ticker
    assert quote.last.as_tuple() == Decimal("72000.00").as_tuple()
    assert quote.symbol == "005930"
    assert quote.broker == broker
    assert quote.venue == "KRX"  # Caller-supplied offline context only.
    assert quote.info == {}
    assert quote.timestamp is None and quote.retrieved_at is None
    assert quote.previous_close is None and quote.bid is None and quote.ask is None
    assert not hasattr(quote, "to_dict")
    if broker in {"kis", "kiwoom", "meritz"}:
        assert quote.volume == 0
    else:
        assert quote.volume is None


@pytest.mark.parametrize("broker", list(FIXTURES))
@pytest.mark.parametrize("status", [401, 429, 500])
def test_non_2xx_is_rejected_before_reading_synthetic_source(
    broker: str, status: int
) -> None:
    plan = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
    raw = json.dumps(FIXTURES[broker])
    with pytest.raises(OfflineResponseRejected, match="not successful"):
        decode_offline_quote_response(plan, http_status=status, json_text=raw)


def test_offline_200_not_sufficient_for_bad_kis_payload() -> None:
    plan = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
    with pytest.raises(ValueError, match="rt_cd"):
        decode_offline_quote_response(
            plan, http_status=200,
            json_text='{"rt_cd":"not-0","output":{"stck_prpr":"72000"}}',
        )


def test_no_tampered_request_context_can_flow_to_native_decoder() -> None:
    plan = plan_ticker_request("toss", "005930", venue="KRX", environment="live")
    for altered in [
        dataclasses.replace(plan, symbol="000660"),
        dataclasses.replace(plan, origin="https://attacker.invalid"),
        dataclasses.replace(plan, venue="NXT"),
        dataclasses.replace(plan, query=(("symbols", "000660"),)),
    ]:
        with pytest.raises(QuotePlanUnavailable):
            decode_offline_quote_response(altered, http_status=200, json_text="{}")


def test_meritz_quote_requires_mac_header_name_but_does_not_generate_it() -> None:
    plan = plan_ticker_request("meritz", "005930", venue="KRX", environment="live")
    assert "mac_address" in plan.auth.quote_header_names
    assert plan.public_headers == ()
    assert plan.auth.token_exchange_implemented is False


def test_paper_plan_is_only_documented_template_not_broker_verification() -> None:
    plan = plan_ticker_request("kiwoom", "005930", venue="KRX", environment="paper")
    assert plan.origin == "https://mockapi.kiwoom.com"
    assert not plan.transport_implemented
    assert authentication_requirements("kiwoom", environment="paper").token_path == "/oauth2/token"
