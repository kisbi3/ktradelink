"""Public experimental fetch_ticker (ADR 0013) with mocked HTTPS only.

No socket, DNS, broker, account or order call is ever made. Every credential,
token and response below is synthetic. Quote bodies follow the documented
field names used by the existing decoder tests
(crates/ktradelink-decoders/tests/six_brokers.rs); they are not broker data.
The KIS expiry offset passed here is test context, not publisher evidence.
"""

import copy
import http.client
import json
import logging
import os
import pickle
import ssl
import subprocess
import sys
import threading
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from types import MappingProxyType
from unittest.mock import MagicMock

import pytest

import ktradelink
from ktradelink import _public_client
from ktradelink.errors import DeliveryState

KEY, SECRET, TOKEN = "SYNTHETIC_APP_KEY_123", "SYNTHETIC_APP_SECRET_456", "SYNTHETIC_BEARER_789"
UPSTREAM = "SYNTHETIC_UPSTREAM_TEXT"
SECRETS = (KEY, SECRET, TOKEN, UPSTREAM)
KST_TEST_OFFSET = timezone(timedelta(hours=9))
NOW_MS = int(datetime(2027, 1, 2, 0, 0, tzinfo=KST_TEST_OFFSET).timestamp() * 1000)
ABS_EXPIRY_MS = int(datetime(2027, 1, 2, 12, 1, 3, tzinfo=KST_TEST_OFFSET).timestamp() * 1000)
HOUR_MS = 3_600_000

TOKEN_BODIES = {
    "kis": {"access_token": TOKEN, "token_type": "Bearer",
            "access_token_token_expired": "2027-01-02 12:01:03"},
    "kiwoom": {"token": TOKEN, "token_type": "Bearer", "expires_dt": "20270102120103",
               "return_code": 0},
    "ls": {"access_token": TOKEN, "scope": "oob", "token_type": "Bearer", "expires_in": 86400},
}
QUOTE_BODIES = {
    "kis": {"rt_cd": "0", "output": {"stck_prpr": "72000", "stck_oprc": "71900",
                                     "stck_hgpr": "72400", "stck_lwpr": "71600",
                                     "acml_vol": "15"}},
    "kiwoom": {"return_code": 0, "stk_cd": "005930", "cur_prc": "72000", "open_pric": "71900",
               "high_pric": "72400", "low_pric": "71600", "trde_qty": "15"},
    "ls": {"rsp_cd": "00000", "t1102OutBlock": {"shcode": "005930", "price": 72000,
                                                "volume": 15}},
}
HOSTS = {
    ("kis", "live"): ("openapi.koreainvestment.com", 9443),
    ("kis", "paper"): ("openapivts.koreainvestment.com", 29443),
    ("kiwoom", "live"): ("api.kiwoom.com", None),
    ("kiwoom", "paper"): ("mockapi.kiwoom.com", None),
    ("ls", "live"): ("openapi.ls-sec.co.kr", 8080),
}
QUOTE_TARGETS = {
    "kis": ("GET", "/uapi/domestic-stock/v1/quotations/inquire-price"
                   "?fid_cond_mrkt_div_code=J&fid_input_iscd=005930"),
    "kiwoom": ("POST", "/api/dostk/stkinfo"),
    "ls": ("POST", "/stock/market-data"),
}
TOKEN_PATHS = {"kis": "/oauth2/tokenP", "kiwoom": "/oauth2/token", "ls": "/oauth2/token"}
BROKERS = ("kis", "kiwoom", "ls")


def body(data) -> bytes:
    return json.dumps(data).encode()


def token_body(broker):
    return body(TOKEN_BODIES[broker])


def quote_body(broker, **root):
    return body({**QUOTE_BODIES[broker], **root})


class Clock:
    def __init__(self, now):
        self.now = now

    def __call__(self):
        return self.now


@pytest.fixture
def clock(monkeypatch):
    fake = Clock(NOW_MS)
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", fake)
    return fake


@pytest.fixture
def no_network(monkeypatch):
    factory = MagicMock(side_effect=AssertionError("network must not be used"))
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    return factory


@pytest.fixture
def decoder_ready(monkeypatch):
    """Stands in for the native preflight on paths that fail before decoding,
    so they also run in the pure-Python CI job."""
    monkeypatch.setattr(_public_client, "_decoder_preflight", lambda broker: True)


@pytest.fixture
def native():
    pytest.importorskip("_ktradelink_native")


def connection(status=200, data=b"{}", **failures):
    conn = MagicMock()
    conn.getresponse.return_value.status = status
    conn.getresponse.return_value.read.return_value = data
    conn.getresponse.return_value.length = None
    for name, error in failures.items():
        getattr(conn, name).side_effect = error
    return conn


def serve(monkeypatch, *connections):
    factory = MagicMock(side_effect=list(connections))
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    return factory


def client(broker="ls", environment="live", **overrides):
    options = {"credentials": ktradelink.Credentials(KEY, SECRET), "allow_network": True,
               "accept_unverified": True}
    if broker == "kis":
        options["kis_expiry_timezone"] = KST_TEST_OFFSET
    options.update(overrides)
    return ktradelink.connect(broker, environment=environment, **options)


def assert_clean(error):
    """Static text only, nothing chained, no secret anywhere we can render."""
    assert isinstance(error, ktradelink.KTradeLinkError)
    assert error.__context__ is None and error.__cause__ is None
    rendered = " ".join((str(error), repr(error), repr(error.args), str(error.reason),
                         str(error.detail), str(vars(error))))
    for secret in SECRETS:
        assert secret not in rendered


# --- public surface ---------------------------------------------------------

def test_public_all_is_exact_and_resolvable():
    assert sorted(ktradelink.__all__) == sorted([
        "AuthenticationError", "BrokerClient", "BrokerRejected", "BrokerUnavailable",
        "Capability", "ClientClosed", "Credentials", "DeliveryState", "InvalidParameter",
        "InvalidSymbol", "InvalidVenue", "KTradeLinkError", "NetworkDisabled",
        "PermissionDenied", "RateLimitExceeded", "ResponseSchemaError", "TransportError",
        "UnsupportedCapability", "__version__", "capabilities", "connect",
    ])
    for name in ktradelink.__all__:
        assert getattr(ktradelink, name) is not None
    for name in ktradelink.errors.__all__:
        assert getattr(ktradelink, name) is getattr(ktradelink.errors, name)
    # Private pieces are not re-exported.
    for private in ("HttpsTransport", "CredentialPair", "InMemoryTokenCache", "WireRequest"):
        assert not hasattr(ktradelink, private)
    for cls in (ktradelink.InvalidSymbol, ktradelink.TransportError, ktradelink.BrokerRejected):
        assert issubclass(cls, ktradelink.KTradeLinkError)


def test_importing_the_package_does_not_load_the_native_module():
    src = str(Path(ktradelink.__file__).resolve().parents[1])
    code = ("import sys, ktradelink\n"
            "assert hasattr(ktradelink, 'connect')\n"
            "assert 'ktradelink._native' not in sys.modules\n"
            "assert '_ktradelink_native' not in sys.modules\n")
    env = {**os.environ, "PYTHONPATH": src}
    subprocess.run([sys.executable, "-c", code], check=True, env=env, cwd=src)


def test_clients_are_only_created_by_connect():
    with pytest.raises(TypeError):
        ktradelink.BrokerClient(object(), "ls", "live", None, allow_network=False,
                                timeout_ms=1, kis_expiry_timezone=None)


# --- capabilities ------------------------------------------------------------

def test_capabilities_report_candidates_honestly_and_never_supported():
    expected = {
        "kis": ("documented_candidate", "documented_candidate"),
        "kiwoom": ("documented_candidate", "documented_candidate"),
        "ls": ("documented_candidate", "unsupported"),
        "db": ("unsupported", "unsupported"),
        "toss": ("unsupported", "unsupported"),
        "meritz": ("unsupported", "unsupported"),
    }
    for broker, states in expected.items():
        rows = ktradelink.capabilities(broker)
        assert tuple(row.environment for row in rows) == ("live", "paper")
        assert tuple(row.state for row in rows) == states
        for row in rows:
            assert type(row) is ktradelink.Capability
            assert (row.broker, row.method, row.venue) == (broker, "fetch_ticker", "KRX")
            assert row.state != "supported"
    assert client("kis", allow_network=False).capabilities == (
        ktradelink.capabilities("kis")[0],)


@pytest.mark.parametrize("broker", ["KIS", "shinhan", "", None, 1])
def test_capabilities_of_an_unknown_broker_is_an_error(broker):
    with pytest.raises(ktradelink.InvalidParameter) as caught:
        ktradelink.capabilities(broker)
    assert_clean(caught.value)


# --- connect -----------------------------------------------------------------

@pytest.mark.parametrize("broker", ["db", "toss", "meritz"])
def test_brokers_without_a_reviewed_route_are_unsupported(broker, no_network):
    with pytest.raises(ktradelink.UnsupportedCapability) as caught:
        client(broker)
    assert caught.value.reason == "broker_or_environment_not_enabled"
    assert_clean(caught.value)


def test_paper_is_never_replaced_by_live(no_network):
    with pytest.raises(ktradelink.UnsupportedCapability):
        client("ls", "paper")


@pytest.mark.parametrize("kwargs,error,reason", [
    ({"broker": "Kiwoom"}, ktradelink.InvalidParameter, "unknown_broker"),
    ({"broker": None}, ktradelink.InvalidParameter, "unknown_broker"),
    ({"environment": "LIVE"}, ktradelink.InvalidParameter, "unknown_environment"),
    ({"environment": "prod"}, ktradelink.InvalidParameter, "unknown_environment"),
    ({"credentials": (KEY, SECRET)}, ktradelink.InvalidParameter, "credentials_required"),
    ({"credentials": None}, ktradelink.InvalidParameter, "credentials_required"),
    ({"allow_network": 1}, ktradelink.InvalidParameter, "flags_must_be_bool"),
    ({"accept_unverified": "yes"}, ktradelink.InvalidParameter, "flags_must_be_bool"),
    ({"accept_unverified": False}, ktradelink.UnsupportedCapability,
     "unverified_capability_not_acknowledged"),
    ({"timeout_ms": 0}, ktradelink.InvalidParameter, "invalid_timeout_ms"),
    ({"timeout_ms": 60_001}, ktradelink.InvalidParameter, "invalid_timeout_ms"),
    ({"timeout_ms": True}, ktradelink.InvalidParameter, "invalid_timeout_ms"),
    ({"timeout_ms": 5.0}, ktradelink.InvalidParameter, "invalid_timeout_ms"),
    ({"kis_expiry_timezone": KST_TEST_OFFSET}, ktradelink.InvalidParameter,
     "kis_expiry_timezone_only_for_kis"),
])
def test_connect_rejects_invalid_configuration(kwargs, error, reason, no_network):
    options = {"broker": "ls", "environment": "live",
               "credentials": ktradelink.Credentials(KEY, SECRET),
               "allow_network": True, "accept_unverified": True, **kwargs}
    broker = options.pop("broker")
    environment = options.pop("environment")
    with pytest.raises(error) as caught:
        ktradelink.connect(broker, environment=environment, **options)
    assert caught.value.reason == reason
    assert_clean(caught.value)


def test_environment_has_no_default():
    with pytest.raises(TypeError):
        ktradelink.connect("ls", credentials=ktradelink.Credentials(KEY, SECRET))


@pytest.mark.parametrize("tz,reason", [
    (None, "kis_expiry_timezone_required"),
    ("+09:00", "kis_expiry_timezone_must_be_datetime_timezone"),
    (timedelta(hours=9), "kis_expiry_timezone_must_be_datetime_timezone"),
])
def test_kis_never_assumes_an_expiry_timezone(tz, reason, no_network):
    with pytest.raises(ktradelink.InvalidParameter) as caught:
        client("kis", kis_expiry_timezone=tz)
    assert caught.value.reason == reason


def test_kis_rejects_a_zoneinfo_because_only_fixed_offsets_are_accepted(no_network):
    from zoneinfo import ZoneInfo

    with pytest.raises(ktradelink.InvalidParameter):
        client("kis", kis_expiry_timezone=ZoneInfo("Asia/Seoul"))


# --- credentials -------------------------------------------------------------

def test_credentials_are_redacted_and_cannot_be_pickled_or_copied():
    creds = ktradelink.Credentials(KEY, SECRET)
    for text in (repr(creds), str(creds), f"{creds}", f"{creds!r}"):
        assert text == "Credentials(<redacted>)"
    assert not hasattr(creds, "__dict__")
    for attempt in (lambda: pickle.dumps(creds), lambda: copy.copy(creds),
                    lambda: copy.deepcopy(creds)):
        with pytest.raises(TypeError) as caught:
            attempt()
        assert KEY not in str(caught.value) and SECRET not in str(caught.value)
    assert creds != ktradelink.Credentials(KEY, SECRET)  # identity, never value compare


@pytest.mark.parametrize("key,secret", [
    ("", SECRET), (KEY, ""), (KEY + "\r\n", SECRET), (KEY, SECRET + "\x00"),
    (None, SECRET), (KEY, b"bytes"), ("x" * 4097, SECRET),
])
def test_invalid_credentials_fail_without_echo_or_chain(key, secret):
    with pytest.raises(ktradelink.InvalidParameter) as caught:
        ktradelink.Credentials(key, secret)
    assert caught.value.reason == "invalid_credentials"
    assert_clean(caught.value)


def test_client_repr_and_pickling_never_expose_secrets(no_network):
    c = client("kis")
    assert repr(c) == "BrokerClient(broker='kis', environment='live', network=enabled)"
    assert str(c) == repr(c)
    for attempt in (lambda: pickle.dumps(c), lambda: copy.copy(c)):
        with pytest.raises(TypeError):
            attempt()


# --- network opt-in and argument validation (nothing sent) -------------------

@pytest.mark.parametrize("broker", BROKERS)
def test_network_is_disabled_by_default_and_refused_before_any_socket(
        broker, no_network, monkeypatch):
    preflight = MagicMock(return_value=True)
    monkeypatch.setattr(_public_client, "_decoder_preflight", preflight)
    options = {"credentials": ktradelink.Credentials(KEY, SECRET)}
    if broker == "kis":
        options["kis_expiry_timezone"] = KST_TEST_OFFSET
    c = ktradelink.connect(broker, environment="live", **options)
    assert c.network_enabled is False
    with pytest.raises(ktradelink.NetworkDisabled) as caught:
        c.fetch_ticker("005930")
    assert caught.value.delivery is DeliveryState.NOT_SENT
    assert_clean(caught.value)
    no_network.assert_not_called()
    preflight.assert_not_called()


@pytest.mark.parametrize("symbol", [
    "5930", "0059300", "00593A", "005 30", "００５９３０", "", " 005930", 5930, None, True,
    b"005930",
])
def test_invalid_symbols_are_rejected_before_anything_else(symbol, no_network):
    with pytest.raises(ktradelink.InvalidSymbol) as caught:
        client().fetch_ticker(symbol)
    assert caught.value.delivery is DeliveryState.NOT_SENT
    no_network.assert_not_called()


@pytest.mark.parametrize("venue,error", [
    ("NXT", ktradelink.UnsupportedCapability),
    ("BROKER_COMPOSITE", ktradelink.UnsupportedCapability),
    ("krx", ktradelink.InvalidVenue), ("", ktradelink.InvalidVenue),
    ("KOSPI", ktradelink.InvalidVenue), (None, ktradelink.InvalidVenue),
])
def test_only_krx_is_accepted_with_no_venue_fallback(venue, error, no_network):
    with pytest.raises(error):
        client().fetch_ticker("005930", venue=venue)
    no_network.assert_not_called()


@pytest.mark.parametrize("params,reason", [
    ({"FID_COND_MRKT_DIV_CODE": "UN"}, "params_not_supported"),
    ({"": None}, "params_not_supported"),
    ([("a", 1)], "params_must_be_a_mapping"),
    ("a", "params_must_be_a_mapping"),
    (0, "params_must_be_a_mapping"),
])
def test_any_non_empty_params_are_rejected(params, reason, no_network):
    with pytest.raises(ktradelink.InvalidParameter) as caught:
        client().fetch_ticker("005930", params=params)
    assert caught.value.reason == reason
    no_network.assert_not_called()


@pytest.mark.parametrize("params", [None, {}, MappingProxyType({})])
def test_empty_params_pass_validation(params, no_network):
    disabled = ktradelink.connect("ls", environment="live",
                                  credentials=ktradelink.Credentials(KEY, SECRET))
    with pytest.raises(ktradelink.NetworkDisabled):
        disabled.fetch_ticker("005930", params=params)


def test_missing_native_decoder_refuses_before_sending(monkeypatch, no_network):
    from ktradelink import _native

    def missing(name):
        raise ModuleNotFoundError("synthetic absent", name=name)

    monkeypatch.setattr(_native, "import_module", missing)
    with pytest.raises(ktradelink.UnsupportedCapability) as caught:
        client().fetch_ticker("005930")
    assert caught.value.reason == "native_decoder_unavailable"
    assert caught.value.delivery is DeliveryState.NOT_SENT
    assert_clean(caught.value)
    no_network.assert_not_called()


def test_closed_client_sends_nothing_and_drops_its_secrets(no_network, decoder_ready):
    with client() as c:
        assert c.closed is False
    assert c.closed is True and "closed" in repr(c)
    with pytest.raises(ktradelink.ClientClosed) as caught:
        c.fetch_ticker("005930")
    assert_clean(caught.value)
    c.close()  # idempotent
    no_network.assert_not_called()


# --- success, per broker -----------------------------------------------------

@pytest.mark.parametrize("broker,environment", sorted(HOSTS))
def test_success_sends_one_token_and_one_quote(broker, environment, clock, monkeypatch,
                                               native, caplog):
    caplog.set_level(logging.DEBUG)
    token_conn = connection(data=token_body(broker))
    quote_conn = connection(data=quote_body(broker))
    factory = serve(monkeypatch, token_conn, quote_conn)
    ticker = client(broker, environment).fetch_ticker("005930")

    assert type(ticker) is ktradelink.models.Ticker
    assert (ticker.symbol, ticker.venue, ticker.broker) == ("005930", "KRX", broker)
    assert ticker.last == Decimal("72000") and ticker.volume == 15
    assert ticker.timestamp is None and ticker.retrieved_at is None
    assert ticker.bid is None and ticker.ask is None and ticker.previous_close is None
    assert ticker.info == {}
    if broker == "ls":  # t1102 open/high/low are deliberately not mapped (ADR 0010)
        assert ticker.open is None and ticker.high is None
    else:
        assert (ticker.open, ticker.high, ticker.low) == (
            Decimal("71900"), Decimal("72400"), Decimal("71600"))

    host, port = HOSTS[(broker, environment)]
    assert factory.call_count == 2
    for call in factory.call_args_list:
        assert call.args == (host,) and call.kwargs["port"] == port
        assert call.kwargs["context"].verify_mode is ssl.CERT_REQUIRED
    assert token_conn.request.call_args.args == ("POST", TOKEN_PATHS[broker])
    assert quote_conn.request.call_args.args == QUOTE_TARGETS[broker]
    headers = quote_conn.request.call_args.kwargs["headers"]
    assert headers["authorization"] == f"Bearer {TOKEN}"
    if broker == "kis":
        assert (headers["appkey"], headers["appsecret"]) == (KEY, SECRET)
    for secret in SECRETS:
        assert secret not in repr(ticker) and secret not in caplog.text


def test_concurrent_first_calls_send_one_token_and_fail_fast(clock, monkeypatch, native):
    entered, release = threading.Event(), threading.Event()
    token_conn = connection(data=token_body("ls"))

    def slow_connect():
        entered.set()
        assert release.wait(5)

    token_conn.connect.side_effect = slow_connect
    factory = serve(monkeypatch, token_conn, connection(data=quote_body("ls")),
                    connection(data=quote_body("ls")))
    c = client()
    results = []
    worker = threading.Thread(target=lambda: results.append(c.fetch_ticker("005930")))
    worker.start()
    assert entered.wait(5)
    with pytest.raises(ktradelink.TransportError) as caught:
        c.fetch_ticker("005930")
    assert caught.value.reason == "token_request_in_flight"
    assert caught.value.delivery is DeliveryState.NOT_SENT
    assert factory.call_count == 1
    release.set()
    worker.join(5)
    assert results and results[0].last == Decimal("72000")
    assert c.fetch_ticker("005930").last == Decimal("72000")  # reuses the token
    assert factory.call_count == 3


def test_close_during_a_token_handshake_stops_the_write(clock, monkeypatch, decoder_ready):
    entered, release = threading.Event(), threading.Event()
    token_conn = connection(data=token_body("ls"))

    def slow_connect():
        entered.set()
        assert release.wait(5)

    token_conn.connect.side_effect = slow_connect
    serve(monkeypatch, token_conn)
    c = client()
    errors = []

    def call():
        try:
            c.fetch_ticker("005930")
        except ktradelink.KTradeLinkError as error:
            errors.append(error)

    worker = threading.Thread(target=call)
    worker.start()
    assert entered.wait(5)
    c.close()
    release.set()
    worker.join(5)
    assert type(errors[0]) is ktradelink.ClientClosed
    assert (errors[0].stage, errors[0].delivery) == ("token", DeliveryState.NOT_SENT)
    token_conn.request.assert_not_called()  # rechecked after TLS, before the write
    assert_clean(errors[0])


# --- token lifecycle ---------------------------------------------------------

def test_ls_token_is_reused_until_the_margin_then_reissued_once(clock, monkeypatch, native):
    conns = [connection(data=token_body("ls")), connection(data=quote_body("ls")),
             connection(data=quote_body("ls")),
             connection(data=token_body("ls")), connection(data=quote_body("ls"))]
    factory = serve(monkeypatch, *conns)
    c = client()
    c.fetch_ticker("005930")
    clock.now = NOW_MS + HOUR_MS
    c.fetch_ticker("005930")
    assert factory.call_count == 3  # second call: quote only
    # LS lifetime counts from the transport's pre-write reading (ADR 0011).
    clock.now = NOW_MS + 86_400_000 - _public_client.TOKEN_REUSE_MARGIN_MS
    c.fetch_ticker("005930")
    assert factory.call_count == 5
    assert [conn.request.call_args.args[1] for conn in conns] == [
        "/oauth2/token", "/stock/market-data", "/stock/market-data",
        "/oauth2/token", "/stock/market-data"]


@pytest.mark.parametrize("broker", ["kis", "kiwoom"])
def test_absolute_expiry_token_is_reissued_after_expiry(broker, clock, monkeypatch, native):
    conns = [connection(data=token_body(broker)), connection(data=quote_body(broker)),
             connection(data=quote_body(broker)),
             connection(data=token_body(broker)), connection(data=quote_body(broker))]
    factory = serve(monkeypatch, *conns)
    c = client(broker)
    c.fetch_ticker("005930")
    clock.now = ABS_EXPIRY_MS - _public_client.TOKEN_REUSE_MARGIN_MS - 1
    c.fetch_ticker("005930")
    assert factory.call_count == 3
    # Synthetic re-issue with a later expiry text.
    later = {**TOKEN_BODIES[broker]}
    later["access_token_token_expired" if broker == "kis" else "expires_dt"] = (
        "2027-01-03 12:01:03" if broker == "kis" else "20270103120103")
    conns[3].getresponse.return_value.read.return_value = body(later)
    clock.now = ABS_EXPIRY_MS
    c.fetch_ticker("005930")
    assert factory.call_count == 5
    assert conns[3].request.call_args.args[1] == TOKEN_PATHS[broker]


def test_kis_token_already_expired_by_its_timezone_is_never_cached(clock, monkeypatch,
                                                                    decoder_ready):
    factory = serve(monkeypatch, connection(data=token_body("kis")))
    # The same naive expiry text read at UTC+14 lies before the current clock.
    clock.now = ABS_EXPIRY_MS
    c = client("kis", kis_expiry_timezone=timezone(timedelta(hours=14)))
    with pytest.raises(ktradelink.ResponseSchemaError) as caught:
        c.fetch_ticker("005930")
    assert caught.value.stage == "token"
    assert factory.call_count == 1


def test_unknown_token_send_is_not_retried_in_the_same_call(clock, monkeypatch, decoder_ready):
    factory = serve(monkeypatch, connection(request=OSError(f"reset {SECRET}")),
                    connection(status=503))
    c = client()
    with pytest.raises(ktradelink.TransportError) as caught:
        c.fetch_ticker("005930")
    assert caught.value.delivery is DeliveryState.UNKNOWN
    assert caught.value.stage == "token"
    assert_clean(caught.value)
    assert factory.call_count == 1
    # A later call is a new caller decision; it sends one new token request.
    with pytest.raises(ktradelink.BrokerUnavailable):
        c.fetch_ticker("005930")
    assert factory.call_count == 2


def test_invalid_token_response_is_not_cached(clock, monkeypatch, decoder_ready):
    factory = serve(monkeypatch,
                    connection(data=body({"error": UPSTREAM, "error_description": SECRET})),
                    connection(status=500))
    c = client()
    with pytest.raises(ktradelink.ResponseSchemaError) as caught:
        c.fetch_ticker("005930")
    error = caught.value
    assert (error.stage, error.delivery) == ("token", DeliveryState.RESPONSE_RECEIVED)
    assert error.reason == "token_response_invalid_or_unverified"
    assert_clean(error)
    assert factory.call_count == 1
    with pytest.raises(ktradelink.BrokerUnavailable) as again:
        c.fetch_ticker("005930")
    assert again.value.stage == "token"  # no token was cached


# --- error mapping -----------------------------------------------------------

HTTP_ERRORS = [
    (401, ktradelink.AuthenticationError, "http_unauthorized"),
    (403, ktradelink.PermissionDenied, "http_forbidden"),
    (429, ktradelink.RateLimitExceeded, "http_rate_limited"),
    (500, ktradelink.BrokerUnavailable, "http_server_error"),
    (503, ktradelink.BrokerUnavailable, "http_server_error"),
    (302, ktradelink.TransportError, "redirect_refused"),
    (400, ktradelink.TransportError, "http_status_rejected"),
    (404, ktradelink.TransportError, "http_status_rejected"),
    (201, ktradelink.TransportError, "http_status_rejected"),
]


@pytest.mark.parametrize("status,error,reason", HTTP_ERRORS)
def test_token_http_errors_map_statically_and_send_no_quote(
        status, error, reason, clock, monkeypatch, decoder_ready):
    factory = serve(monkeypatch, connection(status=status, data=body({"msg": UPSTREAM})))
    with pytest.raises(error) as caught:
        client().fetch_ticker("005930")
    assert type(caught.value) is error
    assert (caught.value.reason, caught.value.stage) == (reason, "token")
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED
    assert_clean(caught.value)
    assert factory.call_count == 1


@pytest.mark.parametrize("status,error,reason", HTTP_ERRORS)
def test_quote_http_errors_map_statically_and_are_not_retried(
        status, error, reason, clock, monkeypatch, decoder_ready):
    factory = serve(monkeypatch, connection(data=token_body("ls")),
                    connection(status=status, data=body({"rsp_msg": UPSTREAM})))
    with pytest.raises(error) as caught:
        client().fetch_ticker("005930")
    assert type(caught.value) is error
    assert (caught.value.reason, caught.value.stage) == (reason, "quote")
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED
    assert_clean(caught.value)
    assert factory.call_count == 2


def test_quote_401_drops_the_token_but_429_keeps_it(clock, monkeypatch, decoder_ready):
    factory = serve(monkeypatch, connection(data=token_body("ls")), connection(status=429),
                    connection(status=401), connection(data=token_body("ls")),
                    connection(status=503))
    c = client()
    with pytest.raises(ktradelink.RateLimitExceeded):
        c.fetch_ticker("005930")
    with pytest.raises(ktradelink.AuthenticationError):
        c.fetch_ticker("005930")  # token kept after 429: quote only
    assert factory.call_count == 3
    with pytest.raises(ktradelink.BrokerUnavailable) as caught:
        c.fetch_ticker("005930")  # token dropped after 401: one new token, then quote
    assert caught.value.stage == "quote"
    assert factory.call_count == 5


@pytest.mark.parametrize("stage", ["token", "quote"])
@pytest.mark.parametrize("failure,reason,delivery", [
    ({"connect": OSError(f"refused {SECRET}")}, "https_connect_failed", DeliveryState.NOT_SENT),
    ({"connect": ssl.SSLError(f"bad cert {KEY}")}, "tls_handshake_failed",
     DeliveryState.NOT_SENT),
    ({"request": OSError(f"broken pipe {TOKEN}")}, "request_write_failed_or_unknown",
     DeliveryState.UNKNOWN),
    ({"getresponse": TimeoutError(UPSTREAM)}, "response_headers_unavailable",
     DeliveryState.UNKNOWN),
])
def test_transport_failures_keep_their_delivery_state(
        stage, failure, reason, delivery, clock, monkeypatch, decoder_ready):
    conns = [connection(**failure)] if stage == "token" else [
        connection(data=token_body("ls")), connection(**failure)]
    factory = serve(monkeypatch, *conns)
    with pytest.raises(ktradelink.TransportError) as caught:
        client().fetch_ticker("005930")
    assert (caught.value.reason, caught.value.stage, caught.value.delivery) == (
        reason, stage, delivery)
    assert_clean(caught.value)
    assert factory.call_count == len(conns)


def test_truncated_quote_body_is_a_read_failure_after_response(clock, monkeypatch,
                                                                decoder_ready):
    truncated = connection(data=b'{"rsp_cd":')
    truncated.getresponse.return_value.length = 10
    serve(monkeypatch, connection(data=token_body("ls")), truncated)
    with pytest.raises(ktradelink.TransportError) as caught:
        client().fetch_ticker("005930")
    assert caught.value.reason == "response_body_read_failed"
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED


@pytest.mark.parametrize("broker,root,error,reason", [
    # Missing status is never success, although the decoders tolerate it.
    ("kis", {"rt_cd": None}, ktradelink.ResponseSchemaError, "quote_status_missing"),
    ("kiwoom", {"return_code": None}, ktradelink.ResponseSchemaError, "quote_status_missing"),
    ("ls", {"rsp_cd": None}, ktradelink.ResponseSchemaError, "quote_status_missing"),
    ("kis", {"rt_cd": 0}, ktradelink.ResponseSchemaError, "quote_status_invalid"),
    ("kiwoom", {"return_code": "0"}, ktradelink.ResponseSchemaError, "quote_status_invalid"),
    ("kiwoom", {"return_code": False}, ktradelink.ResponseSchemaError, "quote_status_invalid"),
    ("ls", {"rsp_cd": 0}, ktradelink.ResponseSchemaError, "quote_status_invalid"),
    ("kis", {"rt_cd": "1"}, ktradelink.BrokerRejected, "quote_status_not_success"),
    ("kiwoom", {"return_code": 1}, ktradelink.BrokerRejected, "quote_status_not_success"),
    ("ls", {"rsp_cd": UPSTREAM}, ktradelink.BrokerRejected, "quote_status_not_success"),
])
def test_quote_root_status_must_be_present_and_successful(
        broker, root, error, reason, clock, monkeypatch, decoder_ready):
    data = dict(QUOTE_BODIES[broker])
    for key, value in root.items():
        if value is None:
            data.pop(key)
        else:
            data[key] = value
    serve(monkeypatch, connection(data=token_body(broker)), connection(data=body(data)))
    with pytest.raises(error) as caught:
        client(broker).fetch_ticker("005930")
    assert type(caught.value) is error
    assert (caught.value.reason, caught.value.stage) == (reason, "quote")
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED
    assert_clean(caught.value)


def test_the_decoders_alone_would_accept_a_missing_status(native):
    """Why the public path checks status itself (regression guard)."""
    from ktradelink._native import decode_ticker_candidate

    for broker in ("kis", "kiwoom"):
        data = dict(QUOTE_BODIES[broker])
        data.pop("rt_cd" if broker == "kis" else "return_code")
        assert decode_ticker_candidate(broker, "005930", "KRX", json.dumps(data)).last


@pytest.mark.parametrize("data,reason", [
    (b"\xff\xfe", "quote_response_not_utf8"),
    (UPSTREAM.encode(), "quote_response_not_a_json_object"),
    (b"[]", "quote_response_not_a_json_object"),
    (b'{"rsp_cd":"00000","rsp_cd":"00000","t1102OutBlock":{}}',
     "quote_response_not_a_json_object"),
    (b'{"rsp_cd":"00000","x":NaN}', "quote_response_not_a_json_object"),
    (b"[" * 100_000, "quote_response_not_a_json_object"),
])
def test_malformed_quote_bodies_are_schema_errors(data, reason, clock, monkeypatch,
                                                  decoder_ready):
    serve(monkeypatch, connection(data=token_body("ls")), connection(data=data))
    with pytest.raises(ktradelink.ResponseSchemaError) as caught:
        client().fetch_ticker("005930")
    assert caught.value.reason == reason
    assert_clean(caught.value)


@pytest.mark.parametrize("broker,data,detail", [
    ("ls", {"rsp_cd": "00000", "t1102OutBlock": {"shcode": "000660", "price": 1}},
     "shcode: AmbiguousSymbol"),
    ("ls", {"rsp_cd": "00000", "t1102OutBlock": {"shcode": "005930", "price": -1}},
     "price: InvalidPrice"),
    ("kiwoom", {"return_code": 0, "cur_prc": "-72000"}, "cur_prc: InvalidPrice"),
    ("kis", {"rt_cd": "0", "output": {"stck_prpr": UPSTREAM}}, "stck_prpr: InvalidPrice"),
    ("kis", {"rt_cd": "0", "output": []}, "output: InvalidEnvelope"),
])
def test_decoder_rejections_expose_only_the_static_field_and_kind(
        broker, data, detail, clock, monkeypatch, native):
    serve(monkeypatch, connection(data=token_body(broker)), connection(data=body(data)))
    with pytest.raises(ktradelink.ResponseSchemaError) as caught:
        client(broker).fetch_ticker("005930")
    assert caught.value.reason == "quote_rejected_by_decoder"
    assert caught.value.detail == detail
    assert_clean(caught.value)


def test_errors_pickle_without_gaining_text(clock, monkeypatch, decoder_ready):
    serve(monkeypatch, connection(request=OSError(SECRET)))
    with pytest.raises(ktradelink.TransportError) as caught:
        client().fetch_ticker("005930")
    restored = pickle.loads(pickle.dumps(caught.value))
    assert type(restored) is ktradelink.TransportError
    assert (restored.reason, restored.delivery, restored.stage, restored.detail) == (
        caught.value.reason, DeliveryState.UNKNOWN, "token", None)
    assert str(restored) == str(caught.value)


def test_error_constructor_refuses_non_static_shapes():
    with pytest.raises(TypeError):
        ktradelink.TransportError("x", stage="body")
    with pytest.raises(TypeError):
        ktradelink.TransportError("x", delivery="not_sent")
    with pytest.raises(TypeError):
        ktradelink.TransportError("")


# --- ChatGPT review of PR #28 (M1, M2, L1) ----------------------------------

def test_clock_failure_after_the_token_response_is_not_reported_as_not_sent(
        clock, monkeypatch, decoder_ready):
    """M1: once the token response has arrived, a token may already exist at
    the broker. A later local clock failure must say so, never NOT_SENT."""
    token_conn = connection(data=token_body("ls"))
    quote_conn = connection(data=quote_body("ls"))
    serve(monkeypatch, token_conn, quote_conn)

    def failing_after_response():
        if token_conn.getresponse.called:
            raise OSError("synthetic clock failure")
        return NOW_MS

    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", failing_after_response)
    with pytest.raises(ktradelink.KTradeLinkError) as caught:
        client("ls").fetch_ticker("005930")
    assert caught.value.stage == "token"
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED
    assert caught.value.delivery is not DeliveryState.NOT_SENT
    assert token_conn.request.call_count == 1
    quote_conn.request.assert_not_called()
    assert_clean(caught.value)


def test_clock_failure_before_any_write_is_not_sent_with_its_stage(monkeypatch, no_network,
                                                                   decoder_ready):
    def broken():
        raise OSError("synthetic clock failure")

    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", broken)
    with pytest.raises(ktradelink.TransportError) as caught:
        client("ls").fetch_ticker("005930")
    assert (caught.value.reason, caught.value.stage) == ("clock_unavailable", "token")
    assert caught.value.delivery is DeliveryState.NOT_SENT
    no_network.assert_not_called()
    assert_clean(caught.value)


@pytest.mark.parametrize("symbol,venue", [("000660", "KRX"), ("005930", "NXT")])
def test_preflight_rejects_a_decoder_that_mislabels_provenance(symbol, venue, monkeypatch,
                                                               no_network):
    """M2: a build returning the right price but the wrong symbol or venue
    must be refused before any connection or token request."""
    from ktradelink import _native

    def mislabelled(broker, _symbol, _venue, _payload):
        return ktradelink.models.Ticker(symbol=symbol, venue=venue, broker=broker,
                                        last=Decimal("72000"), volume=0)

    monkeypatch.setattr(_native, "decode_ticker_candidate", mislabelled)
    assert _public_client._decoder_preflight("ls") is False
    with pytest.raises(ktradelink.UnsupportedCapability) as caught:
        client("ls").fetch_ticker("005930")
    assert caught.value.reason == "native_decoder_unavailable"
    assert caught.value.delivery is DeliveryState.NOT_SENT
    no_network.assert_not_called()


def test_preflight_accepts_a_correctly_labelled_decoder(monkeypatch):
    from ktradelink import _native

    def correct(broker, symbol, venue, _payload):
        return ktradelink.models.Ticker(symbol=symbol, venue=venue, broker=broker,
                                        last=Decimal("72000"), volume=0)

    monkeypatch.setattr(_native, "decode_ticker_candidate", correct)
    assert _public_client._decoder_preflight("ls") is True


@pytest.mark.parametrize("broker,field", [("kis", "rt_cd"), ("kiwoom", "return_code"),
                                          ("ls", "rsp_cd")])
def test_explicit_null_status_is_malformed_not_missing(broker, field, clock, monkeypatch,
                                                       decoder_ready):
    """L1: an explicit JSON null is present but malformed."""
    data = {**QUOTE_BODIES[broker], field: None}
    serve(monkeypatch, connection(data=token_body(broker)), connection(data=body(data)))
    with pytest.raises(ktradelink.ResponseSchemaError) as caught:
        client(broker).fetch_ticker("005930")
    assert (caught.value.reason, caught.value.stage) == ("quote_status_invalid", "quote")
    assert caught.value.delivery is DeliveryState.RESPONSE_RECEIVED
