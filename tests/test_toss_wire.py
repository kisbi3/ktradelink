"""Toss candidate token and prices wire, offline only (ADR 0015).

Shapes follow the Toss OpenAPI document, info.version 1.2.28 (see
docs/brokers/live-auth-transport-gates-2026-11-05.md). Every credential and
token is synthetic; the quote body is the OpenAPI krStock example. No
socket, DNS, broker, account or order call is made.
"""

import http.client
import json
import threading
from dataclasses import replace
from datetime import timedelta, timezone
from unittest.mock import MagicMock
from urllib.parse import parse_qsl

import pytest

from ktradelink import _https_transport
from ktradelink._credential_runtime import (
    CredentialError,
    CredentialFailure,
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
from ktradelink._request_plan import decode_offline_quote_response, plan_ticker_request
from ktradelink._token_codec import (
    MAX_RELATIVE_LIFETIME_S,
    TokenError,
    TokenFailure,
    save_example_token_response,
)

CLIENT = "SYNTHETIC_TOSS_CLIENT"
SECRET = "SYNTH+TOSS&SECRET=/%"  # characters that must be form-encoded
GOOD = {"access_token": "SYNTHETIC_TOSS_TOKEN", "token_type": "Bearer", "expires_in": 86400}
# OpenAPI 1.2.28 /api/v1/prices 200 example "krStock".
PRICES_EXAMPLE = {"result": [{"symbol": "005930", "timestamp": "2026-03-25T09:30:00.123+09:00",
                              "lastPrice": "72000", "currency": "KRW"}]}


def _setup(profile="synthetic", client=CLIENT, provider=None):
    provider = provider or InMemoryCredentialProvider()
    identity = CredentialIdentity("toss", "live", profile)
    provider.put(identity, CredentialPair(client, SECRET))
    return identity, provider


def _body(payload):
    return json.dumps(payload).encode()


def _token(n):
    return _body(GOOD | {"access_token": f"SYNTHETIC_TOSS_TOKEN_{n}"})


def _assert_cache_empty(cache, provider, identity, now_ms=0):
    with pytest.raises(CredentialError) as missing:
        cache.get(provider, identity, now_ms=now_ms)
    assert missing.value.kind is CredentialFailure.TOKEN_MISSING


def _plan():
    return plan_ticker_request("toss", "005930", venue="KRX", environment="live")


def _issue(receive, identity, provider, cache, n=1, clock=(1_000, 1_000)):
    response = receive(build_token_request(identity, provider), _token(n), clock=clock)
    return save_example_token_response(response, identity, provider, cache, now_ms=clock[1])


# --- token request ------------------------------------------------------------

def test_token_request_is_the_documented_client_credentials_form():
    identity, provider = _setup()
    req = build_token_request(identity, provider)
    assert (req.method, req.origin, req.path, req.query) == (
        "POST", "https://openapi.tossinvest.com", "/oauth2/token", ()
    )
    assert req.headers == (("content-type", "application/x-www-form-urlencoded"),)
    assert parse_qsl(req.body.decode("ascii"), strict_parsing=True) == [
        ("grant_type", "client_credentials"),
        ("client_id", CLIENT),
        ("client_secret", SECRET),
    ]
    assert SECRET not in req.body.decode("ascii")
    assert CLIENT not in repr(req) and "SYNTH" not in repr(req)


@pytest.mark.parametrize("change", [
    "json_body", "scope", "content_type", "query_secret", "basic_auth",
])
def test_token_request_shape_cannot_be_altered(change):
    identity, provider = _setup()
    req = build_token_request(identity, provider)
    changes = {
        "json_body": {"body": json.dumps({"grant_type": "client_credentials",
                                          "client_id": CLIENT,
                                          "client_secret": SECRET}).encode()},
        "scope": {"body": req.body + b"&scope=oob"},
        "content_type": {"headers": (("content-type", "application/json;charset=UTF-8"),)},
        "query_secret": {"query": (("client_secret", SECRET),)},
        "basic_auth": {"headers": req.headers + (("authorization", "Basic SYNTHETIC"),)},
    }
    with pytest.raises(TransportError) as caught:
        replace(req, **changes[change])
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
    assert caught.value.delivery is DeliveryState.NOT_SENT


def test_token_send_target_has_no_credentials(monkeypatch):
    identity, provider = _setup()
    conn = MagicMock()
    conn.getresponse.return_value.status = 200
    conn.getresponse.return_value.read.return_value = _body(GOOD)
    conn.getresponse.return_value.length = None
    factory = MagicMock(return_value=conn)
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 1_000)
    HttpsTransport(network_enabled=True).send(build_token_request(identity, provider))
    assert factory.call_args.args[0] == "openapi.tossinvest.com"
    assert factory.call_args.kwargs["port"] is None  # default 443
    assert conn.request.call_args.args == ("POST", "/oauth2/token")


@pytest.mark.parametrize("environment", ["paper", "demo"])
def test_only_the_live_origin_exists(environment):
    with pytest.raises(CredentialError):
        CredentialIdentity("toss", environment, "synthetic")


# --- token response -------------------------------------------------------------

def test_documented_response_yields_a_lease_anchored_before_the_write(receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    response = receive_token_response(build_token_request(identity, provider), _body(GOOD),
                                      clock=(4_000, 5_000))
    lease = save_example_token_response(response, identity, provider, cache, now_ms=9_000)
    assert lease.expires_at_ms == 5_000 + 86_400_000
    assert cache.get(provider, identity, now_ms=9_000) is lease
    assert "SYNTHETIC_TOSS_TOKEN" not in repr(lease)


WITHOUT = {key: {k: v for k, v in GOOD.items() if k != key} for key in GOOD}


@pytest.mark.parametrize("payload", [
    WITHOUT["access_token"], WITHOUT["token_type"], WITHOUT["expires_in"],
    GOOD | {"scope": "oob"},
    GOOD | {"refresh_token": "SYNTHETIC"},
    GOOD | {"result": {}},
    GOOD | {"error": "invalid_client"},
    GOOD | {"error_description": "SYNTHETIC"},
    GOOD | {"error_uri": "https://example.invalid"},
    {"error": "access_denied", "error_description": "IP address not allowed"},
    {"error": {"requestId": "SYNTHETIC", "code": "rate-limit-exceeded", "message": "x"}},
    {"result": GOOD},  # the BFF envelope is not used by /oauth2/token
    GOOD | {"token_type": "bearer"},
    GOOD | {"token_type": "MAC"},
    GOOD | {"expires_in": True},
    GOOD | {"expires_in": 86400.0},
    GOOD | {"expires_in": "86400"},
    GOOD | {"expires_in": 0},
    GOOD | {"expires_in": -1},
    GOOD | {"expires_in": MAX_RELATIVE_LIFETIME_S + 1},
    GOOD | {"expires_in": None},
    GOOD | {"access_token": ""},
    GOOD | {"access_token": "A\r\nB"},
    GOOD | {"access_token": None},
])
def test_undocumented_or_malformed_token_responses_never_cache(payload, receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    response = receive_token_response(build_token_request(identity, provider), _body(payload))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=1)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None
    assert "SYNTHETIC" not in str(caught.value)
    _assert_cache_empty(cache, provider, identity)


@pytest.mark.parametrize("body", [
    b'{"access_token":"A","access_token":"B","token_type":"Bearer","expires_in":86400}',
    b'{"access_token":"A","token_type":"Bearer","expires_in":NaN}',
    b'[]',
    b'\xff',
])
def test_duplicate_nonfinite_and_non_object_bodies_are_rejected(body, receive_token_response):
    identity, provider = _setup()
    response = receive_token_response(build_token_request(identity, provider), body)
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=1)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


@pytest.mark.parametrize("extra", [
    {"kis_expiry_timezone": timezone(timedelta(hours=9))},
    {"db_production_key_acknowledged": True},
    {"db_no_prior_token_acknowledged": True},
])
def test_other_brokers_context_is_refused(extra, receive_token_response):
    identity, provider = _setup()
    response = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=0, **extra)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


def test_unattested_and_stale_responses_are_refused(receive_token_response):
    identity, provider = _setup()
    fabricated = WireResponse(build_token_request(identity, provider), 200, _body(GOOD))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(fabricated, identity, provider, InMemoryTokenCache(),
                                    now_ms=0)
    assert caught.value.kind is TokenFailure.UNATTESTED
    response = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    provider.put(identity, CredentialPair(CLIENT, "ROTATED_SECRET"))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=0)
    assert caught.value.kind is TokenFailure.STALE_CREDENTIAL


# --- one valid token per client ----------------------------------------------------

def test_a_second_profile_on_the_same_client_retires_the_first_lease(receive_token_response):
    provider = InMemoryCredentialProvider()
    first, _ = _setup("first", provider=provider)
    second, _ = _setup("second", provider=provider)
    cache = InMemoryTokenCache()
    _issue(receive_token_response, first, provider, cache, 1)
    build_quote_request(_plan(), first, provider, cache, now_ms=1_000)  # usable now
    _issue(receive_token_response, second, provider, cache, 2)
    # Still cached and unexpired, but Toss has invalidated it.
    assert cache.get(provider, first, now_ms=1_000).issue_sequence is not None
    with pytest.raises(TransportError) as caught:
        build_quote_request(_plan(), first, provider, cache, now_ms=1_000)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE
    assert caught.value.delivery is DeliveryState.NOT_SENT
    build_quote_request(_plan(), second, provider, cache, now_ms=1_000)


def test_another_provider_with_the_same_client_retires_the_lease(receive_token_response):
    identity, provider = _setup()
    other_identity, other_provider = _setup()
    cache, other_cache = InMemoryTokenCache(), InMemoryTokenCache()
    _issue(receive_token_response, identity, provider, cache, 1)
    _issue(receive_token_response, other_identity, other_provider, other_cache, 2)
    with pytest.raises(TransportError) as caught:
        build_quote_request(_plan(), identity, provider, cache, now_ms=1_000)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE


def test_a_different_client_is_independent(receive_token_response):
    identity, provider = _setup("first")
    other_identity, other_provider = _setup("second", client="SYNTHETIC_OTHER_CLIENT")
    cache = InMemoryTokenCache()
    _issue(receive_token_response, identity, provider, cache, 1)
    _issue(receive_token_response, other_identity, other_provider, InMemoryTokenCache(), 2)
    build_quote_request(_plan(), identity, provider, cache, now_ms=1_000)


def test_a_response_from_a_retired_send_cannot_be_saved(receive_token_response):
    provider = InMemoryCredentialProvider()
    first, _ = _setup("first", provider=provider)
    second, _ = _setup("second", provider=provider)
    older = receive_token_response(build_token_request(first, provider), _token(1))
    receive_token_response(build_token_request(second, provider), _token(2))
    cache = InMemoryTokenCache()
    with pytest.raises(TokenError) as caught:
        save_example_token_response(older, first, provider, cache, now_ms=1_000)
    assert caught.value.kind is TokenFailure.SUPERSEDED
    assert caught.value.__context__ is None
    _assert_cache_empty(cache, provider, first)


def test_a_prepared_quote_is_refused_after_a_newer_token_write(
        receive_token_response, monkeypatch):
    provider = InMemoryCredentialProvider()
    first, _ = _setup("first", provider=provider)
    second, _ = _setup("second", provider=provider)
    cache = InMemoryTokenCache()
    _issue(receive_token_response, first, provider, cache, 1)
    quote = build_quote_request(_plan(), first, provider, cache, now_ms=1_000)
    _issue(receive_token_response, second, provider, cache, 2)
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 2_000)
    factory = MagicMock(side_effect=lambda *a, **k: pytest.fail("connected"))
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(quote)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE
    assert caught.value.delivery is DeliveryState.NOT_SENT


def test_a_token_write_during_the_quote_handshake_is_caught_before_the_write(
        receive_token_response, monkeypatch):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    _issue(receive_token_response, identity, provider, cache, 1)
    quote = build_quote_request(_plan(), identity, provider, cache, now_ms=1_000)
    conn = MagicMock()

    def connect():
        # Stand-in for another thread's Toss token send writing meanwhile.
        client = _https_transport._toss_client(provider.load(identity).pair)
        _https_transport._TOSS_TOKEN_WRITES[client] += 1_000

    conn.connect.side_effect = connect
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 2_000)
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=conn))
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(quote)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE
    assert caught.value.delivery is DeliveryState.NOT_SENT
    conn.request.assert_not_called()


@pytest.mark.parametrize("outcome,retires", [
    ("http_500", True),         # written: Toss may have issued and invalidated
    ("write_error", True),      # UNKNOWN delivery: may have reached Toss
    ("connect_error", False),   # NOT_SENT: nothing reached Toss
])
def test_a_failed_token_send_retires_the_lease_once_it_started_writing(
        outcome, retires, receive_token_response, monkeypatch):
    provider = InMemoryCredentialProvider()
    first, _ = _setup("first", provider=provider)
    second, _ = _setup("second", provider=provider)
    cache = InMemoryTokenCache()
    _issue(receive_token_response, first, provider, cache, 1)
    conn = MagicMock()
    conn.getresponse.return_value.status = 500
    conn.getresponse.return_value.length = None
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 2_000)
    if outcome == "write_error":
        conn.request.side_effect = OSError("SYNTHETIC")
    if outcome == "connect_error":
        conn.connect.side_effect = OSError("SYNTHETIC")
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=conn))
    with pytest.raises(TransportError):
        HttpsTransport(network_enabled=True).send(build_token_request(second, provider))
    if retires:
        with pytest.raises(TransportError) as caught:
            build_quote_request(_plan(), first, provider, cache, now_ms=1_000)
        assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE
    else:
        build_quote_request(_plan(), first, provider, cache, now_ms=1_000)


def test_a_manual_lease_cannot_be_used_for_a_toss_quote():
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    cache.put(provider, provider.load(identity), access_token="SYNTHETIC_MANUAL",
              expires_at_ms=10_000, now_ms=0)
    with pytest.raises(TransportError) as caught:
        build_quote_request(_plan(), identity, provider, cache, now_ms=1)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE


class _BlockingConnection:
    def __init__(self):
        self.entered = threading.Event()
        self.release = threading.Event()
        self.created = 0

    def __call__(self, *args, **kwargs):
        self.created += 1
        conn = MagicMock()
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read.return_value = _body(GOOD)
        conn.getresponse.return_value.length = None
        if self.created == 1:
            def connect():
                self.entered.set()
                assert self.release.wait(5)
            conn.connect.side_effect = connect
        return conn


@pytest.mark.parametrize("other", ["profile", "provider"])
def test_concurrent_token_sends_for_one_client_are_refused(other, monkeypatch):
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 1_000)
    factory = _BlockingConnection()
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    identity, provider = _setup("first")
    if other == "profile":
        other_identity, other_provider = _setup("second", provider=provider)
    else:
        other_identity, other_provider = _setup("first")
    worker = threading.Thread(target=lambda: HttpsTransport(network_enabled=True).send(
        build_token_request(identity, provider)))
    worker.start()
    try:
        assert factory.entered.wait(5)
        with pytest.raises(TransportError) as caught:
            HttpsTransport(network_enabled=True).send(
                build_token_request(other_identity, other_provider))
        assert caught.value.kind is TransportFailure.TOKEN_IN_FLIGHT
        assert caught.value.delivery is DeliveryState.NOT_SENT
        assert factory.created == 1
        # A different client is not blocked.
        third_identity, third_provider = _setup("third", client="SYNTHETIC_OTHER_CLIENT")
        assert HttpsTransport(network_enabled=True).send(
            build_token_request(third_identity, third_provider)).status == 200
    finally:
        factory.release.set()
        worker.join(5)


# --- quote ------------------------------------------------------------------------------

def test_quote_request_is_a_bearer_get_without_an_account_header(receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    _issue(receive_token_response, identity, provider, cache, 1)
    req = build_quote_request(_plan(), identity, provider, cache, now_ms=1_000)
    assert (req.method, req.origin, req.path, req.query, req.body) == (
        "GET", "https://openapi.tossinvest.com", "/api/v1/prices", (("symbols", "005930"),), None)
    assert req.headers == (("authorization", "Bearer SYNTHETIC_TOSS_TOKEN_1"),)
    for change in (
        {"query": (("symbols", "005930,000660"),)},
        {"query": (("symbols", "005930"), ("client_id", CLIENT))},
        {"headers": req.headers + (("X-Tossinvest-Account", "SYNTHETIC"),)},
        {"body": b"{}"},
    ):
        with pytest.raises(TransportError):
            replace(req, **change)


def _serve(monkeypatch, status, body):
    conn = MagicMock()
    conn.getresponse.return_value.status = status
    conn.getresponse.return_value.read.return_value = body
    conn.getresponse.return_value.length = None
    factory = MagicMock(return_value=conn)
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 2_000)
    return factory, conn


@pytest.mark.parametrize("status,kind", [
    (401, TransportFailure.UNAUTHORIZED),
    (403, TransportFailure.FORBIDDEN),     # caller IP not allow-listed
    (429, TransportFailure.RATE_LIMITED),  # X-RateLimit-*/Retry-After are not acted on
    (500, TransportFailure.SERVER),
])
def test_quote_errors_are_one_attempt_and_never_retried(
        status, kind, receive_token_response, monkeypatch):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    _issue(receive_token_response, identity, provider, cache, 1)
    req = build_quote_request(_plan(), identity, provider, cache, now_ms=1_000)
    factory, _ = _serve(monkeypatch, status, b'{"error":{"code":"SYNTHETIC"}}')
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(req)
    assert caught.value.kind is kind
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED
    assert factory.call_count == 1


def test_token_then_quote_end_to_end_through_the_existing_decoder(
        receive_token_response, monkeypatch):
    pytest.importorskip("_ktradelink_native")
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    _issue(receive_token_response, identity, provider, cache, 1)
    req = build_quote_request(_plan(), identity, provider, cache, now_ms=1_500)
    factory, conn = _serve(monkeypatch, 200, _body(PRICES_EXAMPLE))
    response = HttpsTransport(network_enabled=True).send(req)
    assert factory.call_count == 1
    assert conn.request.call_args.args == ("GET", "/api/v1/prices?symbols=005930")
    assert conn.request.call_args.kwargs["body"] is None
    assert conn.request.call_args.kwargs["headers"] == {
        "authorization": "Bearer SYNTHETIC_TOSS_TOKEN_1"}
    ticker = decode_offline_quote_response(_plan(), http_status=response.status,
                                           json_text=response.json_text)
    assert (ticker.symbol, ticker.venue, ticker.broker) == ("005930", "KRX", "toss")
    assert str(ticker.last) == "72000"
    assert ticker.volume is None and ticker.open is None  # PriceResponse has neither
