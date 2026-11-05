"""Real optional Rust decoder through fake auth/transport; all data synthetic."""

from decimal import Decimal

import pytest

from ktradelink._offline_session import (
    CredentialScope,
    FailureKind,
    FakeCredentialProvider,
    FakeResponse,
    FakeTransport,
    FixtureOutcome,
    OfflineSessionError,
    execute_offline_quote,
)
from ktradelink._request_plan import plan_ticker_request
from ktradelink.models import Ticker

PAYLOADS = {
    "kis": '{"rt_cd":"0","output":{"stck_prpr":"72000.00","acml_vol":"0"}}',
    "kiwoom": '{"return_code":0,"stk_cd":"005930","cur_prc":"72000.00"}',
    "ls": '{"rsp_cd":"00000","t1102OutBlock":{"shcode":"005930","price":"72000.00"}}',
    "db": '{"rsp_cd":"00000","Out":{"Prpr":"72000.00"}}',
    "toss": '{"result":[{"symbol":"005930","currency":"KRW","lastPrice":"72000.00"}]}',
    "meritz": '{"rsp_cd":"0000","data":{"stck_prpr":"72000.00"}}',
}


@pytest.mark.parametrize("broker,environment", [(b, "live") for b in PAYLOADS]
                         + [("kis", "paper"), ("kiwoom", "paper")])
def test_fake_session_uses_native_decoder_and_existing_ticker(broker, environment):
    plan = plan_ticker_request(broker, "005930", venue="KRX", environment=environment)
    scope = CredentialScope(broker, environment, 0)
    provider = FakeCredentialProvider()
    lease = provider.issue(scope, now_ms=0, lifetime_ms=100)
    transport = FakeTransport((FakeResponse(plan, lease, 200, PAYLOADS[broker],
                                            FixtureOutcome.SUCCESS),))
    quote = execute_offline_quote(plan, scope, provider, transport, now_ms=1)
    assert type(quote) is Ticker
    assert quote.last.as_tuple() == Decimal("72000.00").as_tuple()
    assert (quote.broker, quote.symbol, quote.venue) == (broker, "005930", "KRX")
    assert quote.timestamp is None and quote.retrieved_at is None
    assert quote.info == {} and not hasattr(quote, "to_dict")
    assert transport.calls == 1 and not plan.transport_implemented


@pytest.mark.parametrize("broker", PAYLOADS)
def test_synthetic_success_does_not_bypass_native_json_rejection(broker):
    plan = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
    scope = CredentialScope(broker, "live", 0)
    provider = FakeCredentialProvider()
    lease = provider.issue(scope, now_ms=0, lifetime_ms=100)
    response = FakeResponse(plan, lease, 200, "{broken", FixtureOutcome.SUCCESS)
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, FakeTransport((response,)), now_ms=1)
    assert caught.value.kind is FailureKind.DECODER


@pytest.mark.parametrize("payload", [
    '{"rt_cd":"1","output":{"stck_prpr":"72000"}}',
    '{"rt_cd":null,"output":{"stck_prpr":"72000"}}',
])
def test_synthetic_success_cannot_override_present_bad_broker_status(payload):
    plan = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
    scope = CredentialScope("kis", "live", 0)
    provider = FakeCredentialProvider()
    lease = provider.issue(scope, now_ms=0, lifetime_ms=100)
    response = FakeResponse(plan, lease, 200, payload, FixtureOutcome.SUCCESS)
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, FakeTransport((response,)), now_ms=1)
    assert caught.value.kind is FailureKind.DECODER
