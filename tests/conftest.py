"""Shared offline helpers. No socket, DNS, broker, account or order call."""

import http.client
from unittest.mock import MagicMock

import pytest

from ktradelink._https_transport import HttpsTransport


@pytest.fixture(autouse=True)
def _fresh_process_token_registries(monkeypatch):
    """Each test starts with empty process-wide token registries.

    Tests reuse synthetic token strings and clock readings, so a registry
    entry from one test must not leak into another.
    """
    monkeypatch.setattr("ktradelink._token_codec._DB_ISSUED", {})
    monkeypatch.setattr("ktradelink._https_transport._TOSS_TOKEN_WRITES", {})
    monkeypatch.setattr("ktradelink._https_transport._TOSS_QUOTE_WRITES", {})


@pytest.fixture
def receive_token_response(monkeypatch):
    """Return ``receive(request, body, clock=(pre_connect_ms, before_write_ms))``.

    It sends ``request`` once through a network-enabled ``HttpsTransport``
    whose HTTPS connection is a mock answering HTTP 200 with ``body``, so the
    result is a transport-attested response. The clock readings are test
    scaffolding for the module-private ``_wall_clock_ms``.
    """

    def receive(request, body: bytes, *, clock=(1_000, 1_000)):
        readings = iter(clock)
        monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms",
                            lambda: next(readings))
        conn = MagicMock()
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read.return_value = body
        conn.getresponse.return_value.length = None
        monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=conn))
        return HttpsTransport(network_enabled=True).send(request)

    return receive
