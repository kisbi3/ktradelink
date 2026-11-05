"""Regression tests for the PR #22 review findings L1/L2 and PR #24 review M1.

No socket, DNS, broker, account or token exchange is executed: responses are
parsed by the real ``http.client.HTTPResponse`` from in-memory bytes.
"""

import http.client
import io
import traceback
from unittest.mock import MagicMock

import pytest

from ktradelink._credential_runtime import (
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
    build_quote_request,
    build_token_request,
)
from ktradelink._request_plan import plan_ticker_request


class _BytesSocket:
    """Just enough of a socket for ``http.client.HTTPResponse`` to parse."""

    def __init__(self, raw: bytes):
        self._raw = raw

    def makefile(self, _mode):
        return io.BytesIO(self._raw)


class _RecordedConnection:
    """Replaces HTTPSConnection; replies with real HTTPResponse parsing."""

    instances: list["_RecordedConnection"] = []
    raw_response = b""

    def __init__(self, host, port=None, timeout=None, context=None):
        self.calls = []
        self.closed = False
        self.instances.append(self)

    def connect(self):
        self.calls.append("connect")

    def request(self, method, target, body=None, headers=None):
        self.calls.append("request")

    def getresponse(self):
        self.calls.append("getresponse")
        response = http.client.HTTPResponse(_BytesSocket(self.raw_response), method="POST")
        response.begin()
        return response

    def close(self):
        self.closed = True


def _token_request(broker="kiwoom"):
    provider = InMemoryCredentialProvider()
    identity = CredentialIdentity(broker, "live", "hardening")
    provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    return build_token_request(identity, provider)


def _serve(monkeypatch, raw: bytes):
    _RecordedConnection.instances.clear()
    monkeypatch.setattr(_RecordedConnection, "raw_response", raw)
    monkeypatch.setattr(http.client, "HTTPSConnection", _RecordedConnection)
    return _RecordedConnection.instances


_COMPLETE_TOKEN = (
    b'{"token_type":"bearer","return_code":0,"token":"SYNTHETIC_TOKEN",'
    b'"expires_dt":"20991231235959"}'
)


def test_body_shorter_than_content_length_is_read_failure(monkeypatch):
    # A complete JSON document followed by an early close: http.client's
    # read(amt) returns the short body without raising IncompleteRead.
    raw = (b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n" % (len(_COMPLETE_TOKEN) + 50)
           + _COMPLETE_TOKEN)
    connections = _serve(monkeypatch, raw)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(_token_request())
    assert caught.value.kind is TransportFailure.READ
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED
    assert caught.value.__context__ is None
    assert len(connections) == 1 and connections[0].closed


def test_exact_content_length_body_is_accepted(monkeypatch):
    raw = b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n" % len(_COMPLETE_TOKEN) + _COMPLETE_TOKEN
    _serve(monkeypatch, raw)
    response = HttpsTransport(network_enabled=True).send(_token_request())
    assert response.status == 200 and response.body == _COMPLETE_TOKEN


def test_chunked_and_close_delimited_bodies_still_work(monkeypatch):
    chunked = (b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n"
               + b"%x\r\n" % len(_COMPLETE_TOKEN) + _COMPLETE_TOKEN + b"\r\n0\r\n\r\n")
    _serve(monkeypatch, chunked)
    assert HttpsTransport(network_enabled=True).send(_token_request()).body == _COMPLETE_TOKEN
    close_delimited = b"HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n" + _COMPLETE_TOKEN
    _serve(monkeypatch, close_delimited)
    assert HttpsTransport(network_enabled=True).send(_token_request()).body == _COMPLETE_TOKEN


def test_truncated_chunked_body_is_read_failure(monkeypatch):
    raw = b'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n40\r\n{"a":1}'
    _serve(monkeypatch, raw)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(_token_request())
    assert caught.value.kind is TransportFailure.READ
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED


@pytest.mark.parametrize("remaining", [1, "0", 0.0, MagicMock()])
def test_unrecognised_remaining_length_fails_closed(remaining, monkeypatch):
    conn = MagicMock()
    conn.getresponse.return_value.status = 200
    conn.getresponse.return_value.read.return_value = b"{}"
    conn.getresponse.return_value.length = remaining
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=conn))
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(_token_request())
    assert caught.value.kind is TransportFailure.READ


def test_send_has_no_per_call_clock_override():
    with pytest.raises(TypeError):
        HttpsTransport(network_enabled=True).send(_token_request(), now_ms=1)


@pytest.mark.parametrize("enabled", [True, False])
def test_sender_accepts_no_caller_clock(enabled):
    # A network-capable sender must never be handed a frozen/rolled-back clock.
    with pytest.raises(TypeError):
        HttpsTransport(network_enabled=enabled, clock=lambda: 2)


def _quote_request(expires_at_ms):
    provider = InMemoryCredentialProvider()
    identity = CredentialIdentity("kiwoom", "live", "hardening")
    snapshot = provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    cache = InMemoryTokenCache()
    cache.put(provider, snapshot, access_token="SYNTHETIC_TOKEN",
              expires_at_ms=expires_at_ms, now_ms=0)
    plan = plan_ticker_request("kiwoom", "005930", venue="KRX", environment="live")
    return build_quote_request(plan, identity, provider, cache, now_ms=1)


def test_token_expired_by_real_clock_is_never_written(monkeypatch):
    # ChatGPT review of PR #24, M1: the lease was valid at build time (now_ms=1)
    # but the real epoch is far past expires_at_ms=100.
    request = _quote_request(expires_at_ms=100)
    conn = MagicMock()
    factory = MagicMock(return_value=conn)
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(request)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE
    assert caught.value.delivery is DeliveryState.NOT_SENT
    factory.assert_not_called()
    conn.request.assert_not_called()


def _patch_clock(monkeypatch, clock):
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", clock)


def test_clock_is_read_again_after_handshake(monkeypatch):
    request = _quote_request(expires_at_ms=100)
    readings = iter([10, 100])  # valid before connect, expired after the handshake
    _patch_clock(monkeypatch, lambda: next(readings))
    conn = MagicMock()
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=conn))
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(request)
    assert caught.value.kind is TransportFailure.TOKEN_UNAVAILABLE
    assert caught.value.delivery is DeliveryState.NOT_SENT
    conn.connect.assert_called_once()
    conn.request.assert_not_called()


def _raising_clock():
    raise RuntimeError("SYNTHETIC_CLOCK_SECRET")


@pytest.mark.parametrize("clock", [lambda: -1, lambda: 1.5, lambda: True, lambda: None,
                                   _raising_clock])
def test_bad_clock_reading_fails_before_connecting(clock, monkeypatch):
    _patch_clock(monkeypatch, clock)
    factory = MagicMock(side_effect=AssertionError("must not connect"))
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(_token_request())
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
    assert caught.value.delivery is DeliveryState.NOT_SENT
    assert caught.value.__context__ is None
    assert "SYNTHETIC_CLOCK_SECRET" not in "".join(traceback.format_exception(caught.value))
    factory.assert_not_called()


def test_bad_clock_reading_after_handshake_stops_before_write(monkeypatch):
    readings = iter([10, -1])
    _patch_clock(monkeypatch, lambda: next(readings))
    conn = MagicMock()
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=conn))
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(_token_request())
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
    assert caught.value.delivery is DeliveryState.NOT_SENT
    conn.request.assert_not_called()
    conn.close.assert_called_once()
