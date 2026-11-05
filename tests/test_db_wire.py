"""DB candidate token and PRICE quote wire, offline only (ADR 0015).

Shapes follow the DB API guide token/PRICE details and the official SDK at
DBsecurities/dbsec-open-api@564b5100 (see
docs/brokers/live-auth-transport-gates-2026-11-05.md). Every credential and
token is synthetic; the quote body is the API guide's published example.
No socket, DNS, broker, account or order call is made.
"""

import http.client
import json
import ssl
from dataclasses import replace
from datetime import timedelta, timezone
from unittest.mock import MagicMock
from urllib.parse import parse_qsl

import pytest

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
from ktradelink._request_plan import (
    authentication_requirements,
    decode_offline_quote_response,
    plan_ticker_request,
)
from ktradelink._token_codec import (
    DB_MAX_LIFETIME_S,
    TokenError,
    TokenFailure,
    save_example_token_response,
)

KEY = "SYNTHETIC_DB_KEY"
SECRET = "SYNTH+DB&SECRET=/%"  # characters that must be form-encoded
ACKS = {"db_production_key_acknowledged": True, "db_no_prior_token_acknowledged": True}
GOOD = {"access_token": "SYNTHETIC_DB_TOKEN", "scope": "oob", "token_type": "Bearer",
        "expires_in": 86400}
# API guide PRICE detail, response example (published sample market values).
PRICE_EXAMPLE = {
    "Out": {
        "Sdpr": "53900", "Prpr": "55550", "Mxpr": "70000", "Llam": "37800",
        "Oprc": "54300", "SdprVrssMrktRate": "0.74", "PrprVrssOprcRate": "-2.25",
        "Hprc": "55900", "SdprVrssHgprRate": "3.71", "PrprVrssHgprRate": "0.63",
        "Lprc": "54200", "SdprVrssLwprRate": "0.56", "PrprVrssLwprRate": "-2.43",
        "PrdyVrss": "1650", "PrdyCtrt": "3.06", "Per": "10.89", "Pbr": "0.93",
        "AcmlTrPbmn": "400303637800", "AcmlVol": "7240324", "PrdyVol": "13439520",
        "Bidp1": "55500", "Askp1": "55600", "HtsOtstStplQty": "", "OtstStplQtyIcdc": "",
    },
    "rsp_cd": "00000",
    "rsp_msg": "정상 처리 되었습니다.",
}


def _setup(profile="synthetic"):
    provider = InMemoryCredentialProvider()
    identity = CredentialIdentity("db", "live", profile)
    provider.put(identity, CredentialPair(KEY, SECRET))
    return identity, provider


def _body(payload):
    return json.dumps(payload).encode()


def _assert_cache_empty(cache, provider, identity, now_ms=0):
    with pytest.raises(CredentialError) as missing:
        cache.get(provider, identity, now_ms=now_ms)
    assert missing.value.kind is CredentialFailure.TOKEN_MISSING


# --- token request ----------------------------------------------------------

def test_token_request_is_the_documented_form_body_never_the_query_sample():
    identity, provider = _setup()
    req = build_token_request(identity, provider)
    assert authentication_requirements("db", environment="live").token_request_format == "form"
    assert (req.method, req.origin, req.path, req.query) == (
        "POST", "https://openapi.dbsec.co.kr:8443", "/oauth2/token", ()
    )
    assert req.headers == (("content-type", "application/x-www-form-urlencoded"),)
    assert parse_qsl(req.body.decode("ascii"), strict_parsing=True) == [
        ("grant_type", "client_credentials"),
        ("appkey", KEY),
        ("appsecretkey", SECRET),
        ("scope", "oob"),
    ]
    assert SECRET not in req.body.decode("ascii")  # percent-encoded, not raw
    assert KEY not in repr(req) and "SYNTH" not in repr(req)


@pytest.mark.parametrize("change", [
    "json_body", "scope", "content_type", "query_secret", "query_all", "extra_header",
])
def test_token_request_shape_cannot_be_altered(change):
    identity, provider = _setup()
    req = build_token_request(identity, provider)
    changes = {
        # The SDK notes JSON is refused by the gateway (IGW00133).
        "json_body": {"body": json.dumps({"grant_type": "client_credentials",
                                          "appkey": KEY, "appsecretkey": SECRET,
                                          "scope": "oob"}).encode()},
        "scope": {"body": req.body.replace(b"scope=oob", b"scope=login")},
        "content_type": {"headers": (("content-type", "application/json;charset=UTF-8"),)},
        # The testbed sample's URL-query credentials.
        "query_secret": {"query": (("appsecretkey", SECRET),)},
        "query_all": {"query": tuple(parse_qsl(req.body.decode("ascii"))), "body": b""},
        "extra_header": {"headers": req.headers + (("mac_address", "0123456789AB"),)},
    }
    with pytest.raises(TransportError) as caught:
        replace(req, **changes[change])
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
    assert caught.value.delivery is DeliveryState.NOT_SENT


def test_token_send_uses_verified_tls_and_puts_nothing_in_the_url(monkeypatch):
    identity, provider = _setup()
    conn = MagicMock()
    conn.getresponse.return_value.status = 200
    conn.getresponse.return_value.read.return_value = _body(GOOD)
    conn.getresponse.return_value.length = None
    factory = MagicMock(return_value=conn)
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 1_000)
    HttpsTransport(network_enabled=True).send(build_token_request(identity, provider))
    factory.assert_called_once()
    assert factory.call_args.args[0] == "openapi.dbsec.co.kr"
    assert factory.call_args.kwargs["port"] == 8443
    context = factory.call_args.kwargs["context"]
    assert context.verify_mode is ssl.CERT_REQUIRED and context.check_hostname is True
    method, target = conn.request.call_args.args
    assert (method, target) == ("POST", "/oauth2/token")
    assert KEY not in target and "?" not in target
    assert conn.request.call_args.kwargs["headers"] == {
        "content-type": "application/x-www-form-urlencoded"}


@pytest.mark.parametrize("environment", ["paper", "demo"])
def test_only_the_live_label_exists(environment):
    with pytest.raises(CredentialError) as caught:
        CredentialIdentity("db", environment, "synthetic")
    assert caught.value.kind is CredentialFailure.INVALID


# --- token response -----------------------------------------------------------

@pytest.mark.parametrize("scope", ["oob", "login"])  # API guide example / testbed example
def test_documented_response_yields_a_lease_anchored_before_the_write(
        scope, receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    response = receive_token_response(build_token_request(identity, provider),
                                      _body(GOOD | {"scope": scope}), clock=(4_000, 5_000))
    lease = save_example_token_response(response, identity, provider, cache, now_ms=9_000,
                                        **ACKS)
    assert lease.expires_at_ms == 5_000 + 86_400_000
    assert cache.get(provider, identity, now_ms=9_000) is lease
    assert "SYNTHETIC_DB_TOKEN" not in repr(lease)


WITHOUT = {key: {k: v for k, v in GOOD.items() if k != key} for key in GOOD}


@pytest.mark.parametrize("payload", [
    WITHOUT["access_token"], WITHOUT["scope"], WITHOUT["token_type"], WITHOUT["expires_in"],
    # field-table names, alone or next to the example's
    WITHOUT["access_token"] | {"token": "SYNTHETIC_DB_TOKEN"},
    GOOD | {"token": "SYNTHETIC_DB_TOKEN"},
    WITHOUT["expires_in"] | {"expire_in": "86400"},
    GOOD | {"expire_in": "86400"},
    # envelopes and other extra keys
    GOOD | {"rsp_cd": "00000"},
    GOOD | {"rsp_msg": "SYNTHETIC"},
    GOOD | {"error": "invalid_client"},
    GOOD | {"error_description": "SYNTHETIC"},
    GOOD | {"refresh_token": "SYNTHETIC"},
    GOOD | {"expires_at": "20991231235959"},
    # token_type
    GOOD | {"token_type": "bearer"},
    GOOD | {"token_type": "BEARER"},
    GOOD | {"token_type": "MAC"},
    GOOD | {"token_type": None},
    # scope
    GOOD | {"scope": "OOB"},
    GOOD | {"scope": "oob login"},
    GOOD | {"scope": ""},
    GOOD | {"scope": None},
    GOOD | {"scope": ["oob"]},
    # lifetime: JSON integer 1..86400 only
    GOOD | {"expires_in": True},
    GOOD | {"expires_in": 86400.0},
    GOOD | {"expires_in": "86400"},
    GOOD | {"expires_in": 0},
    GOOD | {"expires_in": -1},
    GOOD | {"expires_in": DB_MAX_LIFETIME_S + 1},
    GOOD | {"expires_in": None},
    # token value
    GOOD | {"access_token": ""},
    GOOD | {"access_token": "A\r\nB"},
    GOOD | {"access_token": 12345},
    GOOD | {"access_token": "A" * 8193},
])
def test_undocumented_or_malformed_token_responses_never_cache(payload, receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    response = receive_token_response(build_token_request(identity, provider), _body(payload))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=1, **ACKS)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None
    assert "SYNTHETIC" not in str(caught.value)
    _assert_cache_empty(cache, provider, identity)


@pytest.mark.parametrize("body", [
    b'{"access_token":"A","access_token":"B","scope":"oob","token_type":"Bearer",'
    b'"expires_in":86400}',
    b'{"access_token":"A","scope":"oob","token_type":"Bearer","expires_in":NaN}',
    b'{"access_token":"A","scope":"oob","token_type":"Bearer","expires_in":Infinity}',
    b'["SYNTHETIC"]',
    b'\xff',
])
def test_duplicate_nonfinite_and_non_object_bodies_are_rejected(body, receive_token_response):
    identity, provider = _setup()
    response = receive_token_response(build_token_request(identity, provider), body)
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=1, **ACKS)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None


@pytest.mark.parametrize("status", [201, 401, 403, 500])
def test_only_http_200_is_parsed(status):
    identity, provider = _setup()
    response = WireResponse(build_token_request(identity, provider), status, _body(GOOD))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=1, **ACKS)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


def test_unattested_response_is_never_cached():
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    fabricated = WireResponse(build_token_request(identity, provider), 200, _body(GOOD))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(fabricated, identity, provider, cache, now_ms=0, **ACKS)
    assert caught.value.kind is TokenFailure.UNATTESTED
    _assert_cache_empty(cache, provider, identity)


def test_rotation_during_exchange_is_stale(receive_token_response):
    identity, provider = _setup()
    response = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    provider.put(identity, CredentialPair("ROTATED_KEY", "ROTATED_SECRET"))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=0, **ACKS)
    assert caught.value.kind is TokenFailure.STALE_CREDENTIAL


def test_expiry_already_past_by_caller_clock_is_not_cached(receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    response = receive_token_response(build_token_request(identity, provider), _body(GOOD),
                                      clock=(1_000, 1_000))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache,
                                    now_ms=1_000 + 86_400_000, **ACKS)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    _assert_cache_empty(cache, provider, identity, now_ms=0)


# --- caller acknowledgements (environment label and re-issue) -----------------

@pytest.mark.parametrize("acks", [
    {},
    {"db_production_key_acknowledged": True},
    {"db_no_prior_token_acknowledged": True},
    {"db_production_key_acknowledged": True, "db_no_prior_token_acknowledged": False},
])
def test_db_lease_needs_both_acknowledgements(acks, receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    response = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache, now_ms=0, **acks)
    assert caught.value.kind is TokenFailure.UNACKNOWLEDGED
    assert caught.value.__context__ is None
    _assert_cache_empty(cache, provider, identity)


@pytest.mark.parametrize("value", [1, "yes", None, 1.0])
def test_acknowledgements_must_be_exact_booleans(value, receive_token_response):
    identity, provider = _setup()
    response = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=0, **(ACKS | {"db_no_prior_token_acknowledged": value}))
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


def test_kis_timezone_is_refused_for_db(receive_token_response):
    identity, provider = _setup()
    response = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=0, kis_expiry_timezone=timezone(timedelta(hours=9)),
                                    **ACKS)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


@pytest.mark.parametrize("broker,body", [
    ("ls", {"access_token": "SYNTHETIC_LS", "scope": "oob", "token_type": "Bearer",
            "expires_in": 86400}),
    ("kiwoom", {"token": "SYNTHETIC_KIWOOM", "token_type": "Bearer", "return_code": 0,
                "expires_dt": "20991231235959"}),
])
@pytest.mark.parametrize("ack", ["db_production_key_acknowledged",
                                 "db_no_prior_token_acknowledged"])
def test_db_acknowledgements_are_refused_for_other_brokers(
        broker, body, ack, receive_token_response):
    identity = CredentialIdentity(broker, "live", "synthetic")
    provider = InMemoryCredentialProvider()
    provider.put(identity, CredentialPair(KEY, SECRET))
    response = receive_token_response(build_token_request(identity, provider), _body(body))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=0, **{ack: True})
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


def test_a_token_returned_again_by_a_later_send_is_reissued(receive_token_response):
    # DB returns the same token with its ORIGINAL expiry when re-issued before
    # expiry; counting 86400 s from the second send would overstate it.
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    first = receive_token_response(build_token_request(identity, provider), _body(GOOD),
                                   clock=(1_000, 1_000))
    lease = save_example_token_response(first, identity, provider, cache, now_ms=1_000, **ACKS)
    second = receive_token_response(build_token_request(identity, provider), _body(GOOD),
                                    clock=(600_000, 600_000))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(second, identity, provider, cache, now_ms=600_000, **ACKS)
    assert caught.value.kind is TokenFailure.REISSUED
    assert caught.value.__context__ is None
    # The first lease, with the first send's expiry, is untouched.
    assert cache.get(provider, identity, now_ms=600_000) is lease
    assert lease.expires_at_ms == 1_000 + 86_400_000


def test_a_token_first_seen_without_acknowledgement_still_counts_as_issued(
        receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    first = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(first, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.UNACKNOWLEDGED
    second = receive_token_response(build_token_request(identity, provider), _body(GOOD),
                                    clock=(60_000, 60_000))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(second, identity, provider, cache, now_ms=60_000, **ACKS)
    assert caught.value.kind is TokenFailure.REISSUED
    _assert_cache_empty(cache, provider, identity)
    # The first send's own response can still be saved once acknowledged.
    lease = save_example_token_response(first, identity, provider, cache, now_ms=60_000, **ACKS)
    assert lease.expires_at_ms == 1_000 + 86_400_000


def test_reissue_is_detected_across_profiles_and_providers(receive_token_response):
    identity, provider = _setup("first")
    other_identity, other_provider = _setup("second")
    save_example_token_response(
        receive_token_response(build_token_request(identity, provider), _body(GOOD)),
        identity, provider, InMemoryTokenCache(), now_ms=0, **ACKS)
    again = receive_token_response(build_token_request(other_identity, other_provider),
                                   _body(GOOD), clock=(2_000, 2_000))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(again, other_identity, other_provider,
                                    InMemoryTokenCache(), now_ms=2_000, **ACKS)
    assert caught.value.kind is TokenFailure.REISSUED


def test_resaving_the_same_response_and_a_new_token_are_accepted(receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    first = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    save_example_token_response(first, identity, provider, cache, now_ms=0, **ACKS)
    again = save_example_token_response(first, identity, provider, cache, now_ms=0, **ACKS)
    assert cache.get(provider, identity, now_ms=0) is again
    fresh = receive_token_response(build_token_request(identity, provider),
                                   _body(GOOD | {"access_token": "SYNTHETIC_DB_TOKEN_2"}))
    newer = save_example_token_response(fresh, identity, provider, cache, now_ms=0, **ACKS)
    assert cache.get(provider, identity, now_ms=0) is newer


def test_an_expired_token_record_is_dropped(receive_token_response):
    identity, provider = _setup()
    first = receive_token_response(build_token_request(identity, provider),
                                   _body(GOOD | {"expires_in": 1}), clock=(1_000, 1_000))
    save_example_token_response(first, identity, provider, InMemoryTokenCache(), now_ms=1_000,
                                **ACKS)
    # A send that starts after that token's expiry cannot have re-issued it.
    later = receive_token_response(build_token_request(identity, provider),
                                   _body(GOOD | {"expires_in": 1}), clock=(2_000, 2_000))
    lease = save_example_token_response(later, identity, provider, InMemoryTokenCache(),
                                        now_ms=2_000, **ACKS)
    assert lease.expires_at_ms == 3_000


def test_older_send_never_replaces_a_newer_db_token(receive_token_response):
    identity, provider = _setup()
    first = receive_token_response(build_token_request(identity, provider), _body(GOOD))
    second = receive_token_response(build_token_request(identity, provider),
                                    _body(GOOD | {"access_token": "SYNTHETIC_DB_TOKEN_2"}))
    cache = InMemoryTokenCache()
    newer = save_example_token_response(second, identity, provider, cache, now_ms=0, **ACKS)
    with pytest.raises(TokenError) as caught:
        save_example_token_response(first, identity, provider, cache, now_ms=0, **ACKS)
    assert caught.value.kind is TokenFailure.SUPERSEDED
    assert cache.get(provider, identity, now_ms=0) is newer


# --- quote ----------------------------------------------------------------------

def _quote_request(identity, provider, cache):
    cache.put(provider, provider.load(identity), access_token="SYNTHETIC_TOKEN",
              expires_at_ms=10_000, now_ms=0)
    plan = plan_ticker_request("db", "005930", venue="KRX", environment="live")
    return plan, build_quote_request(plan, identity, provider, cache, now_ms=1)


def test_quote_request_is_bearer_only_with_the_price_headers_and_body():
    identity, provider = _setup()
    _, req = _quote_request(identity, provider, InMemoryTokenCache())
    assert (req.method, req.origin, req.path, req.query) == (
        "POST", "https://openapi.dbsec.co.kr:8443", "/api/v1/quote/kr-stock/inquiry/price", ())
    assert req.headers == (
        ("content-type", "application/json; charset=utf-8"),
        ("cont_yn", "N"),
        ("cont_key", ""),
        ("authorization", "Bearer SYNTHETIC_TOKEN"),
    )
    assert all(KEY not in value and SECRET not in value for _, value in req.headers)
    assert json.loads(req.body) == {"In": {"InputCondMrktDivCode": "J", "InputIscd1": "005930"}}
    assert "SYNTHETIC_TOKEN" not in repr(req)


@pytest.mark.parametrize("change", [
    {"body": b'{"In":{"InputCondMrktDivCode":"J","InputIscd1":"A005930"}}'},
    {"body": b'{"In":{"InputCondMrktDivCode":"UJ","InputIscd1":"U-005930"}}'},
    {"body": b'{"In":{"InputCondMrktDivCode":"J","InputIscd1":"000660"}}'},
    {"headers": (("content-type", "application/json; charset=utf-8"), ("cont_yn", "Y"),
                 ("cont_key", "SYNTHETIC"), ("authorization", "Bearer SYNTHETIC_TOKEN"))},
    {"headers": (("content-type", "application/json; charset=utf-8"), ("cont_yn", "N"),
                 ("cont_key", ""), ("authorization", "Bearer SYNTHETIC_TOKEN"),
                 ("mac_address", "0123456789AB"))},
    {"headers": (("content-type", "application/json; charset=utf-8"), ("cont_yn", "N"),
                 ("cont_key", ""), ("authorization", "Bearer SYNTHETIC_TOKEN"),
                 ("appkey", KEY))},
    {"path": "/api/v1/trading/kr-stock/order"},
])
def test_quote_request_cannot_be_altered(change):
    identity, provider = _setup()
    _, req = _quote_request(identity, provider, InMemoryTokenCache())
    with pytest.raises(TransportError) as caught:
        replace(req, **change)
    assert caught.value.kind is TransportFailure.INVALID_REQUEST


def _serve(monkeypatch, *responses):
    connections = []

    def factory(*args, **kwargs):
        status, body = responses[len(connections)]
        conn = MagicMock()
        conn.getresponse.return_value.status = status
        conn.getresponse.return_value.read.return_value = body
        conn.getresponse.return_value.length = None
        connections.append(conn)
        return conn

    spy = MagicMock(side_effect=factory)
    monkeypatch.setattr(http.client, "HTTPSConnection", spy)
    return spy, connections


@pytest.mark.parametrize("status,kind", [
    (403, TransportFailure.FORBIDDEN),  # SDK: token-family IGW errors arrive as 403
    (500, TransportFailure.SERVER),     # SDK: other IGW errors arrive as 500
])
def test_quote_gateway_errors_are_one_attempt_and_never_retried(status, kind, monkeypatch):
    identity, provider = _setup()
    _, req = _quote_request(identity, provider, InMemoryTokenCache())
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 2)
    spy, _ = _serve(monkeypatch, (status, b'{"rsp_cd":"SYNTHETIC","rsp_msg":"x"}'))
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(req)
    assert caught.value.kind is kind
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED
    assert spy.call_count == 1


def test_token_then_quote_end_to_end_through_the_existing_decoder(
        monkeypatch, receive_token_response):
    pytest.importorskip("_ktradelink_native")
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    token = receive_token_response(build_token_request(identity, provider), _body(GOOD),
                                   clock=(1_000, 1_000))
    save_example_token_response(token, identity, provider, cache, now_ms=1_000, **ACKS)
    plan = plan_ticker_request("db", "005930", venue="KRX", environment="live")
    req = build_quote_request(plan, identity, provider, cache, now_ms=2_000)
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 2_000)
    spy, connections = _serve(monkeypatch, (200, _body(PRICE_EXAMPLE)))
    response = HttpsTransport(network_enabled=True).send(req)
    assert spy.call_count == 1
    method, target = connections[0].request.call_args.args
    assert (method, target) == ("POST", "/api/v1/quote/kr-stock/inquiry/price")
    sent = connections[0].request.call_args.kwargs
    assert sent["headers"]["authorization"] == "Bearer SYNTHETIC_DB_TOKEN"
    assert json.loads(sent["body"]) == {"In": {"InputCondMrktDivCode": "J",
                                               "InputIscd1": "005930"}}
    ticker = decode_offline_quote_response(plan, http_status=response.status,
                                           json_text=response.json_text)
    assert (ticker.symbol, ticker.venue, ticker.broker) == ("005930", "KRX", "db")
    assert str(ticker.last) == "55550"
    assert (str(ticker.open), str(ticker.high), str(ticker.low)) == ("54300", "55900", "54200")
