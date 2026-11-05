"""Value-free JSON shapes and redacted gateway status; offline only."""

import http.client
import json
from unittest.mock import MagicMock

import pytest

from ktradelink._credential_runtime import (
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._diagnostics import (
    MAX_MESSAGE_CHARS,
    MAX_SHAPE_LINES,
    REDACTED,
    GatewayStatus,
    gateway_status,
    json_shape,
)
from ktradelink._https_transport import (
    HttpsTransport,
    TransportError,
    TransportFailure,
    build_quote_request,
    build_token_request,
)
from ktradelink._request_plan import plan_ticker_request

SECRET_VALUES = ("SYNTHETIC_PRICE_72000", "SYNTH-NAME", "SYNTHETIC_TOKEN")
KNOWN = frozenset(("rsp_cd", "rsp_msg", "t1102OutBlock", "price", "rate", "volume", "diff",
                   "hname", "empty", "flag", "none", "rows", "a", "b"))


def test_shape_lists_paths_and_types_without_values():
    body = json.dumps({
        "rsp_cd": "00000", "rsp_msg": "SYNTH-NAME",
        "t1102OutBlock": {"price": "72000", "rate": "-1.5", "volume": 12, "diff": 1.5,
                          "hname": "SYNTH-NAME", "empty": "", "flag": True, "none": None},
        "rows": [{"a": 1}, {"a": "x", "b": "SYNTHETIC_PRICE_72000"}],
    }).encode()
    shape = json_shape(body, known_keys=KNOWN)
    assert shape == tuple(sorted(shape))
    assert set(shape) == {
        "$: object", "rsp_cd: string:digits", "rsp_msg: string:text",
        "t1102OutBlock: object", "t1102OutBlock.price: string:digits",
        "t1102OutBlock.rate: string:decimal", "t1102OutBlock.volume: integer",
        "t1102OutBlock.diff: number", "t1102OutBlock.hname: string:text",
        "t1102OutBlock.empty: string:empty", "t1102OutBlock.flag: boolean",
        "t1102OutBlock.none: null", "rows: array", "rows[]: object",
        "rows[].a: integer", "rows[].a: string:text", "rows[].b: string:text",
    }
    text = "\n".join(shape)
    assert all(value not in text for value in SECRET_VALUES)
    assert "72000" not in text and "-1.5" not in text


def test_keys_outside_the_allowlist_are_masked():
    # ChatGPT review of PR #27, H1-B: a well-formed key can itself be a secret.
    body = json.dumps({"SYNTHETIC_APP_SECRET": "x", "SYNTHETIC KEY=VALUE": 1,
                       "price": {"SYNTHETIC_NESTED_KEY": 2}}).encode()
    shape = json_shape(body, known_keys=frozenset(("price",)))
    assert shape == ("$: object", "<key>: integer", "<key>: string:text",
                     "price.<key>: integer", "price: object")
    assert json_shape(body, known_keys=frozenset()) == (
        "$: object", "<key>.<key>: integer", "<key>: integer", "<key>: object",
        "<key>: string:text")


@pytest.mark.parametrize("known", [None, {"price"}, ("price",), ["price"]])
def test_an_allowlist_frozenset_is_required(known):
    with pytest.raises(TypeError):
        json_shape(b"{}", known_keys=known)


@pytest.mark.parametrize("body,expected", [
    (b"\xff", "<body is not UTF-8>"),
    (b"<html>SYNTHETIC_TOKEN</html>", "<body is not JSON>"),
    (b'{"a": NaN}', "<body is not JSON>"),
    ("not bytes", "<body is not bytes>"),
])
def test_unparseable_bodies_are_reported_without_content(body, expected):
    assert json_shape(body, known_keys=KNOWN) == (expected,)
    assert gateway_status(body) is None


def test_shape_is_bounded_in_depth_and_lines():
    deep: dict = {}
    node = deep
    for _ in range(20):
        node["n"] = {}
        node = node["n"]
    shape = json_shape(json.dumps(deep).encode(), known_keys=frozenset(("n",)))
    assert any(line.endswith("<depth limit>") for line in shape)
    wide = json_shape(json.dumps({f"k{n}": f"{n}" * (n % 7) for n in range(500)}).encode(),
                      known_keys=frozenset(f"k{n}" for n in range(500)))
    assert len(wide) == MAX_SHAPE_LINES + 1 and wide[-1] == "<more fields omitted>"


def test_gateway_status_reads_only_the_fixed_envelope_and_redacts():
    body = json.dumps({
        "rsp_cd": "SYNTH01",
        "rsp_msg": "bad key SYNTHETIC_KEY / SYNTHETIC_SECRET\r\nline2\x00",
        "other": "SYNTHETIC_OTHER",
    }).encode()
    status = gateway_status(body, redact=["SYNTHETIC_KEY", "SYNTHETIC_SECRET", "abc"])
    assert status == GatewayStatus("SYNTH01", f"bad key {REDACTED} / {REDACTED}??line2?")
    assert "SYNTHETIC_OTHER" not in repr(status)


@pytest.mark.parametrize("payload,expected", [
    ({"error": "invalid_client", "error_description": "SYNTH desc"},
     GatewayStatus("invalid_client", "SYNTH desc")),
    ({"rsp_cd": 12}, GatewayStatus("12", None)),
    ({"rsp_msg": "only message"}, GatewayStatus(None, "only message")),
    ({"rsp_cd": "has space"}, GatewayStatus("<invalid code>", None)),
    ({"rsp_cd": True}, GatewayStatus("<invalid code>", None)),
    ({"rsp_cd": "x" * 33}, GatewayStatus("<invalid code>", None)),
    ({"rsp_cd": "1", "rsp_msg": {"nested": "SYNTH"}}, GatewayStatus("1", "<invalid message>")),
    ({"t1102OutBlock": {"rsp_cd": "1"}}, None),
    ([{"rsp_cd": "1"}], None),
])
def test_gateway_status_variants(payload, expected):
    assert gateway_status(json.dumps(payload).encode()) == expected


@pytest.mark.parametrize("field", ["rsp_cd", "error"])
@pytest.mark.parametrize("code", ["SYNTHETIC_APP_KEY", "synthetic_app_key", "X-SYNTHETIC_APP_KEY"])
def test_a_code_containing_a_secret_is_redacted(field, code):
    # ChatGPT review of PR #27, H1-A: the code is upstream text as well.
    status = gateway_status(json.dumps({field: code}).encode(), redact=["SYNTHETIC_APP_KEY"])
    assert status.code == REDACTED


@pytest.mark.parametrize("secret", ["abc", "Z", "SyNtH"])
def test_secrets_of_any_length_are_redacted_case_insensitively(secret):
    # ChatGPT review of PR #27, H1-C: no minimum redaction length.
    body = json.dumps({"rsp_cd": f"E{secret}1", "rsp_msg": f"bad {secret.upper()} x"}).encode()
    status = gateway_status(body, redact=[secret])
    assert status.code == REDACTED
    assert secret.casefold() not in status.message.casefold().replace(REDACTED, "")


def test_gateway_message_is_truncated_and_cannot_reassemble_a_secret():
    secret = "SYNTHETIC_SECRET_VALUE"
    message = "a" * (MAX_MESSAGE_CHARS - 5) + secret
    status = gateway_status(json.dumps({"rsp_msg": message}).encode(), redact=[secret])
    assert secret not in status.message and len(status.message) <= MAX_MESSAGE_CHARS + 1
    korean = gateway_status(json.dumps({"rsp_msg": "조회할 자료가 없습니다"}).encode())
    assert korean.message == "조회할 자료가 없습니다"


# --- transport integration ---------------------------------------------------

def _quote_request():
    identity = CredentialIdentity("ls", "live", "diag")
    provider = InMemoryCredentialProvider()
    provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    cache = InMemoryTokenCache()
    cache.put(provider, provider.load(identity), access_token="SYNTHETIC_TOKEN",
              expires_at_ms=10_000, now_ms=0)
    plan = plan_ticker_request("ls", "005930", venue="KRX", environment="live")
    return build_quote_request(plan, identity, provider, cache, now_ms=1)


def _serve_error(monkeypatch, status, body):
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 2)
    conn = MagicMock()
    conn.getresponse.return_value.status = status
    conn.getresponse.return_value.read.return_value = body
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=conn))
    return conn


ERROR_BODY = json.dumps({
    "rsp_cd": "SYNTH99",
    "rsp_msg": "echo SYNTHETIC_TOKEN SYNTHETIC_KEY SYNTHETIC_SECRET",
}).encode()


def test_diagnostics_are_off_by_default_and_the_error_body_is_not_read(monkeypatch):
    conn = _serve_error(monkeypatch, 500, ERROR_BODY)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(_quote_request())
    assert caught.value.kind is TransportFailure.SERVER
    assert caught.value.diagnostic is None
    conn.getresponse.return_value.read.assert_not_called()


@pytest.mark.parametrize("status,kind", [(500, TransportFailure.SERVER),
                                         (401, TransportFailure.UNAUTHORIZED),
                                         (429, TransportFailure.RATE_LIMITED)])
def test_opt_in_diagnostic_is_redacted_and_kept_out_of_the_message(status, kind, monkeypatch):
    _serve_error(monkeypatch, status, ERROR_BODY)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True, collect_diagnostics=True).send(_quote_request())
    error = caught.value
    assert error.kind is kind
    assert error.diagnostic == GatewayStatus("SYNTH99", f"echo {REDACTED} {REDACTED} {REDACTED}")
    assert str(error) == kind.value and "SYNTH99" not in repr(error)
    assert error.__context__ is None


def test_unreadable_error_body_gives_no_diagnostic(monkeypatch):
    conn = _serve_error(monkeypatch, 500, b"")
    conn.getresponse.return_value.read.side_effect = OSError("SYNTHETIC_READ_FAILURE")
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True, collect_diagnostics=True).send(_quote_request())
    assert caught.value.kind is TransportFailure.SERVER and caught.value.diagnostic is None
    assert caught.value.__context__ is None


def test_token_error_redacts_the_credentials(monkeypatch):
    identity = CredentialIdentity("ls", "live", "diag")
    provider = InMemoryCredentialProvider()
    provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    _serve_error(monkeypatch, 403, json.dumps(
        {"error": "SYNTH_denied", "error_description": "SYNTHETIC_SECRET rejected"}).encode())
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True, collect_diagnostics=True).send(
            build_token_request(identity, provider))
    assert caught.value.diagnostic == GatewayStatus("SYNTH_denied", f"{REDACTED} rejected")


@pytest.mark.parametrize("value", [1, "yes", None])
def test_collect_diagnostics_must_be_a_bool(value):
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True, collect_diagnostics=value)
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
