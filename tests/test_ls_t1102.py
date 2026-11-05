"""LS t1102 candidate wire and token contracts, offline only.

Shapes follow the LS API guide t1102 and token REST details retrieved
2026-11-05 (see docs/brokers/live-auth-transport-gates-2026-11-05.md). Every
value is synthetic. No socket, DNS, broker, account or order call is made.
"""

import http.client
import json
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
from ktradelink._request_plan import plan_ticker_request
from ktradelink._token_codec import (
    MAX_RELATIVE_LIFETIME_S,
    TokenError,
    TokenFailure,
    save_example_token_response,
)

KEY = "SYNTHETIC_KEY"
SECRET = "SYNTH+SECRET&=/%"  # characters that must be form-encoded


def _setup():
    provider = InMemoryCredentialProvider()
    identity = CredentialIdentity("ls", "live", "synthetic")
    provider.put(identity, CredentialPair(KEY, SECRET))
    return identity, provider


def test_token_request_is_the_documented_form_body():
    identity, provider = _setup()
    req = build_token_request(identity, provider)
    assert (req.method, req.origin, req.path, req.query) == (
        "POST", "https://openapi.ls-sec.co.kr:8080", "/oauth2/token", ()
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


@pytest.mark.parametrize("change", ["json_body", "scope", "content_type", "query_secret"])
def test_token_request_shape_cannot_be_altered(change):
    identity, provider = _setup()
    req = build_token_request(identity, provider)
    changes = {
        "json_body": {"body": json.dumps({"grant_type": "client_credentials",
                                          "appkey": KEY, "appsecretkey": SECRET}).encode()},
        "scope": {"body": req.body.replace(b"scope=oob", b"scope=login")},
        "content_type": {"headers": (("content-type", "application/json;charset=UTF-8"),)},
        "query_secret": {"query": (("appkey", KEY),)},
    }
    with pytest.raises(TransportError) as caught:
        replace(req, **changes[change])
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
    assert caught.value.delivery is DeliveryState.NOT_SENT


def test_paper_is_still_unsupported():
    with pytest.raises(CredentialError) as caught:
        CredentialIdentity("ls", "paper", "synthetic")
    assert caught.value.kind is CredentialFailure.INVALID


def _lease(identity, provider, cache):
    return cache.put(provider, provider.load(identity), access_token="SYNTHETIC_TOKEN",
                     expires_at_ms=1_000, now_ms=0)


def test_quote_request_is_bearer_only_with_t1102_headers_and_body():
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    _lease(identity, provider, cache)
    plan = plan_ticker_request("ls", "005930", venue="KRX", environment="live")
    req = build_quote_request(plan, identity, provider, cache, now_ms=1)
    assert (req.method, req.path, req.query) == ("POST", "/stock/market-data", ())
    assert dict(req.headers) == {
        "content-type": "application/json; charset=utf-8",
        "tr_cd": "t1102",
        "tr_cont": "N",
        "tr_cont_key": "",
        "mac_address": "",
        "authorization": "Bearer SYNTHETIC_TOKEN",
    }
    # LS quotes do not carry the app key/secret (unlike KIS).
    assert all(KEY not in value and SECRET not in value for _, value in req.headers)
    assert json.loads(req.body) == {"t1102InBlock": {"shcode": "005930", "exchgubun": "K"}}
    with pytest.raises(TransportError):
        replace(req, body=b'{"t1102InBlock":{"shcode":"005930","exchgubun":"U"}}')
    with pytest.raises(TransportError):
        replace(req, headers=req.headers + (("tr_id", "STKCURR"),))


def test_quote_send_is_one_attempt_to_the_t1102_path(monkeypatch):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    _lease(identity, provider, cache)
    plan = plan_ticker_request("ls", "005930", venue="KRX", environment="live")
    req = build_quote_request(plan, identity, provider, cache, now_ms=1)
    conn = MagicMock()
    conn.getresponse.return_value.status = 200
    conn.getresponse.return_value.read.return_value = b"{}"
    conn.getresponse.return_value.length = None
    factory = MagicMock(return_value=conn)
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 2)
    HttpsTransport(network_enabled=True).send(req)
    factory.assert_called_once()
    assert factory.call_args.args[0] == "openapi.ls-sec.co.kr"
    assert factory.call_args.kwargs["port"] == 8080
    conn.request.assert_called_once()
    method, target = conn.request.call_args.args
    assert (method, target) == ("POST", "/stock/market-data")
    assert conn.request.call_args.kwargs["headers"]["tr_cd"] == "t1102"


def _token_response(identity, provider, payload):
    req = build_token_request(identity, provider)
    return WireResponse(req, 200, json.dumps(payload).encode())


GOOD = {"access_token": "SYNTHETIC_TOKEN", "scope": "oob", "token_type": "Bearer",
        "expires_in": 86400}


WITHOUT_LIFETIME = {k: v for k, v in GOOD.items() if k != "expires_in"}


# (name, value) pairs exactly as the LS guide documents them: the response
# example (`expires_in` JSON number) and the field table (`expire_in`, String,
# length 10).
@pytest.mark.parametrize("field,value", [("expires_in", 86400), ("expire_in", "86400")])
def test_either_documented_lifetime_form_yields_a_relative_lease(field, value):
    identity, provider = _setup()
    payload = WITHOUT_LIFETIME | {field: value}
    cache = InMemoryTokenCache()
    lease = save_example_token_response(
        _token_response(identity, provider, payload), identity, provider, cache, now_ms=5_000,
    )
    assert lease.expires_at_ms == 5_000 + 86_400_000
    assert cache.get(provider, identity, now_ms=5_000) is lease
    assert "SYNTHETIC_TOKEN" not in repr(lease)


@pytest.mark.parametrize("payload", [
    GOOD | {"expire_in": 86400},                                      # both spellings
    {k: v for k, v in GOOD.items() if k != "expires_in"},             # neither
    {k: v for k, v in GOOD.items() if k != "scope"},                  # scope missing
    GOOD | {"scope": "login"},
    GOOD | {"token_type": "mac"},
    {k: v for k, v in GOOD.items() if k != "token_type"},
    GOOD | {"expires_in": True},
    GOOD | {"expires_in": 86400.0},
    GOOD | {"expires_in": "86400"},
    GOOD | {"expires_in": 0},
    GOOD | {"expires_in": -1},
    GOOD | {"expires_in": MAX_RELATIVE_LIFETIME_S + 1},
    WITHOUT_LIFETIME | {"expire_in": 86400},    # table name with the example's type
    WITHOUT_LIFETIME | {"expire_in": "086400"},
    WITHOUT_LIFETIME | {"expire_in": "+86400"},
    WITHOUT_LIFETIME | {"expire_in": " 86400"},
    WITHOUT_LIFETIME | {"expire_in": "86400.0"},
    WITHOUT_LIFETIME | {"expire_in": "\uff18\uff16\uff14\uff10\uff10"},  # full-width digits
    WITHOUT_LIFETIME | {"expire_in": "12345678901"},                # over the 10-char table length
    WITHOUT_LIFETIME | {"expire_in": "0"},
    WITHOUT_LIFETIME | {"expire_in": ""},
    WITHOUT_LIFETIME | {"expire_in": str(MAX_RELATIVE_LIFETIME_S + 1)},
    WITHOUT_LIFETIME | {"expire_in": None},
    GOOD | {"expire_in": "86400"},                                  # both forms at once
    GOOD | {"rsp_cd": "00000"},                                       # gateway envelope
    GOOD | {"error": "invalid_client"},
    GOOD | {"access_token": ""},
    GOOD | {"access_token": "A\r\nB"},
])
def test_ambiguous_or_malformed_token_responses_never_cache(payload):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    with pytest.raises(TokenError) as caught:
        save_example_token_response(
            _token_response(identity, provider, payload), identity, provider, cache, now_ms=1,
        )
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None
    with pytest.raises(CredentialError) as missing:
        cache.get(provider, identity, now_ms=1)
    assert missing.value.kind is CredentialFailure.TOKEN_MISSING


def test_kis_timezone_argument_is_rejected_for_ls():
    identity, provider = _setup()
    with pytest.raises(TokenError) as caught:
        save_example_token_response(
            _token_response(identity, provider, GOOD), identity, provider,
            InMemoryTokenCache(), now_ms=1, kis_expiry_timezone=timezone(timedelta(hours=9)),
        )
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE


def test_rotation_during_exchange_is_stale():
    identity, provider = _setup()
    response = _token_response(identity, provider, GOOD)
    provider.put(identity, CredentialPair("ROTATED", "ROTATED"))
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(), now_ms=1)
    assert caught.value.kind is TokenFailure.STALE_CREDENTIAL
