"""Regression counterexamples use synthetic secrets and patched HTTPS only."""

import http.client
import json
import ssl
from dataclasses import replace
from datetime import UTC, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ktradelink._credential_runtime import (
    CredentialError,
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._https_transport import (
    DeliveryState,
    HttpsTransport,
    TransportError,
    TransportFailure,
    WireResponse,
    build_quote_request,
    build_token_request,
)
from ktradelink._request_plan import plan_ticker_request
from ktradelink._token_codec import TokenError, TokenFailure, save_example_token_response


def setup(broker="kiwoom", environment="live"):
    identity = CredentialIdentity(broker, environment, "synthetic")
    provider = InMemoryCredentialProvider()
    snapshot = provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    cache = InMemoryTokenCache()
    cache.put(provider, snapshot, access_token="SYNTHETIC_TOKEN", now_ms=0, expires_at_ms=100)
    return identity, provider, cache


def request_for(purpose, identity, provider, cache):
    if purpose == "token":
        return build_token_request(identity, provider)
    plan = plan_ticker_request(
        identity.broker, "005930", venue="KRX", environment=identity.environment
    )
    return build_quote_request(plan, identity, provider, cache, now_ms=1)


def send_at(monkeypatch, req, now_ms):
    """Test-only: patch the module clock; the sender itself accepts no clock."""
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: now_ms)
    return HttpsTransport(network_enabled=True).send(req)


def no_network(monkeypatch):
    factory = MagicMock(side_effect=AssertionError("must fail before connecting"))
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    return factory


def fake_network(monkeypatch):
    conn = MagicMock()
    conn.getresponse.return_value.status = 200
    conn.getresponse.return_value.read.return_value = b"{}"
    conn.getresponse.return_value.length = None
    factory = MagicMock(return_value=conn)
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    return factory, conn


@pytest.mark.parametrize("broker", ["kis", "kiwoom"])
@pytest.mark.parametrize("purpose", ["token", "quote"])
@pytest.mark.parametrize("change", ["host", "length", "body", "header_shape"])
def test_whole_wire_shape_is_bound_to_credential_and_plan(broker, purpose, change):
    identity, provider, cache = setup(broker)
    req = request_for(purpose, identity, provider, cache)
    changes = {
        "host": {"headers": req.headers + (("Host", "unrelated.example"),)},
        "length": {"headers": req.headers + (("Content-Length", "0"),)},
        "body": {"body": b'{"stk_cd":"000660"}'},
        "header_shape": {"headers": ("SYNTHETIC_MALFORMED",)},
    }
    with pytest.raises(TransportError) as caught:
        replace(req, **changes[change])
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
    assert caught.value.delivery is DeliveryState.NOT_SENT


@pytest.mark.parametrize("broker", ["kis", "kiwoom"])
@pytest.mark.parametrize("purpose", ["token", "quote"])
@pytest.mark.parametrize("change", ["rotate", "revoke"])
def test_stale_credentials_never_open_connection(broker, purpose, change, monkeypatch):
    identity, provider, cache = setup(broker)
    req = request_for(purpose, identity, provider, cache)
    if change == "rotate":
        provider.put(identity, CredentialPair("NEW_KEY", "NEW_SECRET"))
    else:
        provider.clear(identity)
    factory = no_network(monkeypatch)
    with pytest.raises(TransportError) as caught:
        send_at(monkeypatch, req, 2)
    assert caught.value.kind is TransportFailure.STALE_CREDENTIAL
    assert caught.value.delivery is DeliveryState.NOT_SENT
    assert caught.value.__context__ is None
    factory.assert_not_called()


@pytest.mark.parametrize("broker", ["kis", "kiwoom"])
@pytest.mark.parametrize("change", ["expired", "rotate", "revoke"])
def test_prepared_quote_rechecks_current_token(broker, change, monkeypatch):
    identity, provider, cache = setup(broker)
    req = request_for("quote", identity, provider, cache)
    now_ms = 100 if change == "expired" else 2
    if change == "revoke":
        cache.revoke(provider, identity)
    elif change == "rotate":
        cache.put(provider, provider.load(identity), access_token="NEW_TOKEN",
                  now_ms=1, expires_at_ms=200)
    factory = no_network(monkeypatch)
    with pytest.raises(TransportError) as caught:
        send_at(monkeypatch, req, now_ms)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE
    assert caught.value.delivery is DeliveryState.NOT_SENT
    assert caught.value.__context__ is None
    factory.assert_not_called()


@pytest.mark.parametrize("broker", ["kis", "kiwoom"])
@pytest.mark.parametrize("environment", ["live", "paper"])
def test_quote_send_stays_single_attempt_with_bound_token(broker, environment, monkeypatch):
    identity, provider, cache = setup(broker, environment)
    req = request_for("quote", identity, provider, cache)
    factory, conn = fake_network(monkeypatch)
    result = send_at(monkeypatch, req, 2)
    assert result.request is req and result.status == 200
    factory.assert_called_once()
    conn.request.assert_called_once()
    conn.close.assert_called_once()


@pytest.mark.parametrize("change,expected", [
    ("credential", TransportFailure.STALE_CREDENTIAL),
    ("token", TransportFailure.TOKEN_UNAVAILABLE),
])
def test_handshake_change_stops_before_any_http_write(change, expected, monkeypatch):
    identity, provider, cache = setup()
    req = request_for("quote", identity, provider, cache)
    _, conn = fake_network(monkeypatch)
    def revoke_during_handshake():
        if change == "credential":
            provider.clear(identity)
        else:
            cache.revoke(provider, identity)
    conn.connect.side_effect = revoke_during_handshake
    with pytest.raises(TransportError) as caught:
        send_at(monkeypatch, req, 2)
    assert caught.value.kind is expected and caught.value.delivery is DeliveryState.NOT_SENT
    conn.request.assert_not_called()
    conn.close.assert_called_once()


def test_default_clock_is_checked_again_after_handshake(monkeypatch):
    identity, provider, cache = setup()
    req = request_for("quote", identity, provider, cache)
    _, conn = fake_network(monkeypatch)
    clock = MagicMock(side_effect=[1_000_000, 100_000_000])
    monkeypatch.setattr("ktradelink._https_transport.time.time_ns", clock)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(req)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE
    assert caught.value.delivery is DeliveryState.NOT_SENT
    conn.request.assert_not_called()


def test_tls_never_enables_ambient_session_key_logging(monkeypatch, tmp_path):
    identity, provider, _ = setup()
    req = build_token_request(identity, provider)
    keylog = tmp_path / "unexpected-key-log"
    monkeypatch.setenv("SSLKEYLOGFILE", str(keylog))
    factory, _ = fake_network(monkeypatch)
    HttpsTransport(network_enabled=True).send(req)
    context = factory.call_args.kwargs["context"]
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
    assert context.keylog_filename is None
    assert not keylog.exists()


def test_invalid_tls_context_fails_before_connection(monkeypatch):
    identity, provider, _ = setup()
    context = SimpleNamespace(verify_mode=ssl.CERT_NONE, check_hostname=False,
                              load_default_certs=lambda *_: None)
    monkeypatch.setattr(ssl, "SSLContext", lambda *_: context)
    factory = no_network(monkeypatch)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(build_token_request(identity, provider))
    assert caught.value.kind is TransportFailure.TLS
    assert caught.value.delivery is DeliveryState.NOT_SENT
    factory.assert_not_called()


def token_fields(broker):
    if broker == "kiwoom":
        return {"token": "SYNTHETIC_TOKEN", "token_type": "Bearer", "return_code": 0,
                "expires_dt": "20270102120103"}
    return {"access_token": "SYNTHETIC_TOKEN", "token_type": "Bearer",
            "access_token_token_expired": "2027-01-02 12:01:03"}


@pytest.mark.parametrize("field", ["token_type", "return_code"])
def test_missing_token_success_fields_are_not_inferred(field):
    identity, provider, _ = setup()
    fields = token_fields("kiwoom")
    fields.pop(field)
    cache = InMemoryTokenCache()
    response = WireResponse(build_token_request(identity, provider), 200, json.dumps(fields).encode())
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None
    with pytest.raises(CredentialError):
        cache.get(provider, identity, now_ms=0)


@pytest.mark.parametrize("status", [200.0, "200", True, None])
def test_token_parser_rejects_noninteger_http_status(status):
    identity, provider, cache = setup()
    response = WireResponse(build_token_request(identity, provider), status,
                            json.dumps(token_fields("kiwoom")).encode())
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


@pytest.mark.parametrize("bad", [b"[" * 2000 + b"]" * 2000, b"\xff"])
def test_malformed_token_payload_does_not_retain_parser_context(bad):
    identity, provider, cache = setup()
    response = WireResponse(build_token_request(identity, provider), 200, bad)
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None


@pytest.mark.parametrize("field", ["error", "error_code", "error_description"])
def test_explicit_error_with_token_fields_is_not_success(field):
    identity, provider, cache = setup()
    fields = {**token_fields("kiwoom"), field: "SYNTHETIC_ERROR"}
    response = WireResponse(build_token_request(identity, provider), 200, json.dumps(fields).encode())
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None


def test_kis_naive_expiry_does_not_silently_assume_kst(receive_token_response):
    identity, provider, cache = setup("kis")
    response = receive_token_response(build_token_request(identity, provider),
                                      json.dumps(token_fields("kis")).encode())
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.EVIDENCE_MISSING
    # The offset is explicit synthetic fixture context, not broker verification.
    utc = save_example_token_response(response, identity, provider, cache, now_ms=0,
                                     kis_expiry_timezone=UTC)
    kst = save_example_token_response(response, identity, provider, cache, now_ms=0,
                                     kis_expiry_timezone=timezone(timedelta(hours=9)))
    assert utc.expires_at_ms - kst.expires_at_ms == 9 * 60 * 60 * 1000


@pytest.mark.parametrize("value", ["KST", 9, True])
def test_kis_requires_explicit_fixed_timezone_object(value):
    identity, provider, cache = setup("kis")
    response = WireResponse(build_token_request(identity, provider), 200,
                            json.dumps(token_fields("kis")).encode())
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=0,
                                    kis_expiry_timezone=value)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


def test_kiwoom_expiry_source_cannot_be_overridden_by_kis_offset():
    identity, provider, cache = setup()
    response = WireResponse(build_token_request(identity, provider), 200,
                            json.dumps(token_fields("kiwoom")).encode())
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=0,
                                    kis_expiry_timezone=UTC)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
