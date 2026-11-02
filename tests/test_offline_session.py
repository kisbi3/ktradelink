"""Synthetic authentication/transport contracts; no credentials or network."""

import dataclasses
import socket
import subprocess
import sys
import traceback
from decimal import Decimal

import pytest

from ktradelink import _offline_session as session
from ktradelink._offline_session import (
    CredentialScope,
    FailureKind,
    FakeCredentialProvider,
    FakeLease,
    FakeResponse,
    FakeTransport,
    FixtureOutcome,
    OfflineSessionError,
    TransportPolicy,
    execute_offline_quote,
)
from ktradelink._request_plan import plan_ticker_request
from ktradelink.models import Ticker

BROKERS = ("kis", "kiwoom", "ls", "db", "toss", "meritz")


def setup_fake(broker="kis", environment="live", *, lifetime_ms=1000):
    plan = plan_ticker_request(broker, "005930", venue="KRX", environment=environment)
    scope = CredentialScope(broker, environment, 0)
    provider = FakeCredentialProvider()
    lease = provider.issue(scope, now_ms=10, lifetime_ms=lifetime_ms)
    return plan, scope, provider, lease


@pytest.mark.parametrize("broker", BROKERS)
def test_six_broker_call_through_preserves_ticker_and_never_opens_socket(broker, monkeypatch):
    plan, scope, provider, lease = setup_fake(broker)
    expected = Ticker("005930", "KRX", broker, Decimal("72000.00"), volume=0)
    calls = []

    def decoder(p, *, http_status, json_text):
        calls.append((p, http_status, json_text))
        return expected

    def forbidden(*args, **kwargs):
        pytest.fail("offline execution must not open a socket")

    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(session, "decode_offline_quote_response", decoder)
    response = FakeResponse(plan, lease, 200, "{}", FixtureOutcome.SUCCESS, 1)
    transport = FakeTransport((response,))
    result = execute_offline_quote(plan, scope, provider, transport, now_ms=11)
    assert result is expected
    assert calls == [(plan, 200, "{}")]
    assert transport.calls == 1
    assert result.timestamp is None and result.retrieved_at is None
    assert plan.transport_implemented is False and not plan.auth.token_exchange_implemented


@pytest.mark.parametrize("broker", BROKERS)
@pytest.mark.parametrize("status,kind", [
    (199, FailureKind.HTTP), (204, FailureKind.PROVIDER_UNVERIFIED),
    (301, FailureKind.REDIRECT), (307, FailureKind.REDIRECT),
    (400, FailureKind.HTTP), (401, FailureKind.UNAUTHORIZED),
    (403, FailureKind.FORBIDDEN), (404, FailureKind.HTTP),
    (429, FailureKind.RATE_LIMITED), (500, FailureKind.SERVER), (599, FailureKind.SERVER),
])
def test_http_failure_is_static_and_never_retried(broker, status, kind, monkeypatch):
    plan, scope, provider, lease = setup_fake(broker)
    marker = "SYNTHETIC_DO_NOT_REFLECT"
    response = FakeResponse(plan, lease, status, marker)
    transport = FakeTransport((response, response))
    monkeypatch.setattr(session, "decode_offline_quote_response", lambda *a, **k: pytest.fail())
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, transport, now_ms=11)
    assert caught.value.kind is kind and transport.calls == 1
    assert marker not in repr(response) + str(caught.value)
    assert marker not in "".join(traceback.format_exception(caught.value))
    if status == 401:
        with pytest.raises(OfflineSessionError):
            provider.get(scope, now_ms=11)
    else:
        assert provider.get(scope, now_ms=11) is lease


def test_cache_key_separates_all_brokers_environments_and_fixture_identities():
    provider = FakeCredentialProvider()
    scopes = [CredentialScope(b, "live", i) for b in BROKERS for i in (0, 1)]
    scopes += [CredentialScope(b, "paper", i) for b in ("kis", "kiwoom") for i in (0, 1)]
    leases = [provider.issue(s, now_ms=0, lifetime_ms=100) for s in scopes]
    assert len(set(scopes)) == 16
    assert len({lease.generation for lease in leases}) == 16
    provider.revoke(scopes[0])
    for scope, lease in zip(scopes[1:], leases[1:], strict=True):
        assert provider.get(scope, now_ms=50) is lease
    with pytest.raises(OfflineSessionError):
        FakeCredentialProvider().get(scopes[1], now_ms=50)


def test_expiry_is_exclusive_no_resurrection_or_automatic_refresh():
    _, scope, provider, lease = setup_fake(lifetime_ms=10)
    assert provider.get(scope, now_ms=19) is lease
    for now in (20, 21, 11):
        with pytest.raises(OfflineSessionError) as caught:
            provider.get(scope, now_ms=now)
        assert caught.value.kind is FailureKind.CREDENTIAL_UNAVAILABLE
    new = provider.issue(scope, now_ms=30, lifetime_ms=10)
    assert new.generation > lease.generation
    with pytest.raises(OfflineSessionError):
        provider.get(scope, now_ms=29)
    assert provider.get(scope, now_ms=30) is new


@pytest.mark.parametrize("change", ["rotate", "provider", "copy", "identity", "symbol", "paper"])
def test_response_binding_rejects_stale_or_unrelated_context(change):
    plan, scope, provider, lease = setup_fake()
    response_plan, response_lease = plan, lease
    if change == "rotate":
        provider.issue(scope, now_ms=10, lifetime_ms=1000)
    elif change == "provider":
        response_lease = FakeCredentialProvider().issue(scope, now_ms=10, lifetime_ms=1000)
    elif change == "copy":
        response_lease = dataclasses.replace(lease)
    elif change == "identity":
        response_lease = provider.issue(CredentialScope("kis", "live", 1),
                                        now_ms=10, lifetime_ms=1000)
    else:
        response_plan = plan_ticker_request(
            "kis", "000660" if change == "symbol" else "005930", venue="KRX",
            environment="paper" if change == "paper" else "live",
        )
    response = FakeResponse(response_plan, response_lease, 200, "{}", FixtureOutcome.SUCCESS)
    transport = FakeTransport((response,))
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, transport, now_ms=11)
    assert caught.value.kind is FailureKind.CONTEXT_MISMATCH
    assert transport.calls == 1


@pytest.mark.parametrize("scope", [CredentialScope("kiwoom", "live", 0),
                                   CredentialScope("kis", "paper", 0)])
def test_scope_mismatch_fails_before_fake_exchange(scope):
    plan, _, provider, _ = setup_fake()
    transport = FakeTransport(())
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, transport, now_ms=11)
    assert caught.value.kind is FailureKind.CONTEXT_MISMATCH and transport.calls == 0


@pytest.mark.parametrize("changes", [
    {"origin": "https://invalid.example"}, {"path": "/orders"}, {"method": "DELETE"},
    {"symbol": "000660"}, {"venue": "NXT"}, {"transport_implemented": True},
])
def test_tampered_plan_fails_before_credentials_or_transport(changes):
    plan, scope, provider, _ = setup_fake()
    transport = FakeTransport(())
    with pytest.raises(OfflineSessionError):
        execute_offline_quote(dataclasses.replace(plan, **changes), scope,
                              provider, transport, now_ms=11)
    assert transport.calls == 0


@pytest.mark.parametrize("elapsed,kind", [(9, FailureKind.PROVIDER_UNVERIFIED),
                                         (10, FailureKind.TIMEOUT), (11, FailureKind.TIMEOUT)])
def test_simulated_deadline_boundary(elapsed, kind):
    plan, scope, provider, lease = setup_fake()
    transport = FakeTransport((FakeResponse(plan, lease, 200, "{}", elapsed_ms=elapsed),))
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, transport, now_ms=11,
                              policy=TransportPolicy(timeout_ms=10))
    assert caught.value.kind is kind and transport.calls == 1


def test_token_expiring_during_fake_exchange_is_not_accepted():
    plan, scope, provider, lease = setup_fake(lifetime_ms=5)
    response = FakeResponse(plan, lease, 200, "{}", FixtureOutcome.SUCCESS, elapsed_ms=4)
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, FakeTransport((response,)), now_ms=11)
    assert caught.value.kind is FailureKind.CREDENTIAL_UNAVAILABLE


@pytest.mark.parametrize("policy", [
    {"timeout_ms": 0}, {"timeout_ms": True}, {"timeout_ms": 1.0}, {"timeout_ms": 60_001},
    {"verify_tls": False}, {"verify_tls": 1}, {"follow_redirects": True},
    {"follow_redirects": 0}, {"retries": 1}, {"retries": True}, {"retries": -1},
])
def test_unsafe_policy_is_rejected(policy):
    with pytest.raises(OfflineSessionError):
        TransportPolicy(**policy)


@pytest.mark.parametrize("value", [True, -1, "secret", None, 0.0])
def test_identity_and_clock_accept_exact_nonnegative_integers_only(value):
    with pytest.raises(OfflineSessionError):
        CredentialScope("kis", "live", value)
    _, scope, provider, _ = setup_fake()
    with pytest.raises(OfflineSessionError):
        provider.issue(scope, now_ms=value, lifetime_ms=10)
    with pytest.raises(OfflineSessionError):
        provider.issue(scope, now_ms=10, lifetime_ms=value)


@pytest.mark.parametrize("broker", ["ls", "db", "toss", "meritz"])
def test_unverified_paper_is_not_live(broker):
    with pytest.raises(OfflineSessionError):
        CredentialScope(broker, "paper", 0)


@pytest.mark.parametrize("changes", [
    {"http_status": True}, {"http_status": "200"}, {"http_status": 99},
    {"http_status": 600}, {"outcome": "success"}, {"outcome": True},
    {"elapsed_ms": -1}, {"elapsed_ms": True}, {"json_text": None},
    {"json_text": "\ud800"}, {"json_text": "a" * (session.MAX_BODY_BYTES + 1)},
    {"json_text": "\u00e9" * (session.MAX_BODY_BYTES // 2 + 1)},
])
def test_response_rejects_invalid_types_encoding_and_size(changes):
    plan, _, _, lease = setup_fake()
    fields = dict(request=plan, lease=lease, http_status=200, json_text="{}")
    fields.update(changes)
    with pytest.raises(OfflineSessionError):
        FakeResponse(**fields)


def test_exact_utf8_boundary_and_frozen_records():
    plan, scope, _, lease = setup_fake()
    response = FakeResponse(plan, lease, 200, "\u00e9" * (session.MAX_BODY_BYTES // 2))
    assert len(response.json_text.encode()) == session.MAX_BODY_BYTES
    for value, key in [(response, "http_status"), (lease, "generation"),
                       (scope, "identity_slot"), (TransportPolicy(), "retries")]:
        assert not hasattr(value, "__dict__")
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(value, key, 1)


@pytest.mark.parametrize("error,kind", [(ValueError, FailureKind.DECODER),
                                       (ImportError, FailureKind.NATIVE_UNAVAILABLE)])
def test_decoder_exceptions_do_not_reflect_body_or_display_chain(error, kind, monkeypatch):
    plan, scope, provider, lease = setup_fake()
    marker = "SYNTHETIC_PAYLOAD_SENTINEL"

    def reject(*args, **kwargs):
        raise error(marker)

    monkeypatch.setattr(session, "decode_offline_quote_response", reject)
    transport = FakeTransport((FakeResponse(plan, lease, 200, marker, FixtureOutcome.SUCCESS),))
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, transport, now_ms=11)
    assert caught.value.kind is kind
    assert marker not in "".join(traceback.format_exception(caught.value))


def test_only_concrete_fakes_allowed_and_script_exhaustion_is_explicit():
    plan, scope, provider, _ = setup_fake()
    transport = FakeTransport(())
    for args in [(object(), transport), (provider, object())]:
        with pytest.raises(OfflineSessionError) as caught:
            execute_offline_quote(plan, scope, *args, now_ms=11)
        assert caught.value.kind is FailureKind.INVALID_INPUT
    with pytest.raises(OfflineSessionError) as caught:
        execute_offline_quote(plan, scope, provider, transport, now_ms=11)
    assert caught.value.kind is FailureKind.SCRIPT_EXHAUSTED and transport.calls == 1


def test_module_import_and_rejected_call_do_not_load_native():
    code = """
import sys
from ktradelink._offline_session import *
from ktradelink._request_plan import plan_ticker_request
plan = plan_ticker_request('kis', '005930', venue='KRX', environment='live')
scope = CredentialScope('kis', 'live', 0)
try:
    execute_offline_quote(plan, scope, FakeCredentialProvider(), FakeTransport(()), now_ms=0)
except OfflineSessionError as exc:
    assert exc.kind is FailureKind.CREDENTIAL_UNAVAILABLE
else:
    raise AssertionError('missing lease accepted')
assert 'ktradelink._native' not in sys.modules
assert '_ktradelink_native' not in sys.modules
"""
    subprocess.run([sys.executable, "-I", "-c", code], check=True, timeout=30)


def test_lease_is_not_a_secret_container():
    _, scope, provider, lease = setup_fake()
    assert dataclasses.fields(FakeLease)[0].name == "scope"
    assert "identity_slot" not in repr(lease)
    for obj in (scope, provider, lease):
        for name in ("access_token", "appkey", "appsecret", "mac_address", "account"):
            assert not hasattr(obj, name)
