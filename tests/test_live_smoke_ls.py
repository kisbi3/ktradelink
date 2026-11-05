"""tools/live_smoke_ls.py with mocked HTTPS only; no real network, ever.

Every credential, token and response is synthetic. The checks focus on what
must hold before anyone runs it with a real key: nothing is sent without
--live and confirmation, secrets never reach the output, and failures are
reported with value-free diagnostics.
"""

import http.client
import importlib.util
import io
import json
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "live_smoke_ls.py"
KEY, SECRET, TOKEN = "SYNTHETIC_APP_KEY", "SYNTHETIC_APP_SECRET", "SYNTHETIC_BEARER"
ENV = {"KTRADELINK_LS_APP_KEY": KEY, "KTRADELINK_LS_APP_SECRET": SECRET}
TOKEN_BODY = json.dumps({"access_token": TOKEN, "scope": "oob", "token_type": "Bearer",
                         "expires_in": 86400}).encode()
QUOTE_BODY = json.dumps({"rsp_cd": "00000", "rsp_msg": "SYNTHETIC_OK",
                         "t1102OutBlock": {"shcode": "005930", "hname": "SYNTHETIC_NAME",
                                           "price": 72000, "volume": 15}}).encode()


@pytest.fixture(scope="module")
def tool():
    spec = importlib.util.spec_from_file_location("live_smoke_ls", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _no_secret_prompt(prompt):
    raise AssertionError("must not ask for a secret")


def _run(tool, argv, *, env=None, answer="send", secrets=_no_secret_prompt, native=True):
    """``native`` True/False stands in for the decoder preflight, so paths that
    never decode also run in the pure-Python CI job; ``None`` runs the real
    preflight. Decoding tests skip without the native module."""
    out = io.StringIO()
    real_check = tool._native_available
    if native is not None:
        tool._native_available = lambda: native
    try:
        code = tool.main(argv, env={} if env is None else env, ask=lambda _p: answer,
                         ask_secret=secrets, out=out)
    finally:
        tool._native_available = real_check
    return code, out.getvalue()


def _forbid_network(monkeypatch):
    factory = MagicMock(side_effect=AssertionError("network must not be used"))
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    return factory


def _serve(monkeypatch, *responses):
    """Each response is (status, body); one HTTPS connection per response.

    The transport keeps its real clock: the tool compares the token expiry
    with the real time, as it would in a live run.
    """
    connections = []
    for status, body in responses:
        conn = MagicMock()
        conn.getresponse.return_value.status = status
        conn.getresponse.return_value.read.return_value = body
        conn.getresponse.return_value.length = None
        connections.append(conn)
    factory = MagicMock(side_effect=connections)
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    return factory, connections


def _assert_clean(output):
    for secret in (KEY, SECRET, TOKEN, "SYNTHETIC_NAME", "SYNTHETIC_OK"):
        assert secret not in output


def test_dry_run_sends_nothing_and_shows_only_names(tool, monkeypatch):
    factory = _forbid_network(monkeypatch)
    code, output = _run(tool, [], env=ENV)
    assert code == tool.EXIT_OK
    assert "No request sent." in output
    assert "POST https://openapi.ls-sec.co.kr:8080/stock/market-data" in output
    header_lines = [line for line in output.splitlines() if "header names:" in line]
    assert "tr_cd" in header_lines[-1] and "t1102" not in "".join(header_lines)
    assert "DRY_RUN" not in output
    _assert_clean(output)
    factory.assert_not_called()


@pytest.mark.parametrize("argv", [
    ["--app-key", KEY], ["--secret", SECRET], ["--symbol", "5930"], ["--symbol", "00593A"],
    ["--yes"], ["--liv"], ["--show-gateway-message"],
])
def test_bad_arguments_never_send(tool, argv, monkeypatch):
    factory = _forbid_network(monkeypatch)
    code, output = _run(tool, argv, env=ENV)
    assert code == tool.EXIT_USAGE
    factory.assert_not_called()


def test_live_without_the_native_decoder_sends_nothing(tool, monkeypatch):
    factory = _forbid_network(monkeypatch)
    code, output = _run(tool, ["--live", "--yes"], env=ENV, native=False)
    assert code == tool.EXIT_USAGE
    assert "native LS decoder is missing or not working" in output and "No request sent." in output
    factory.assert_not_called()


@pytest.mark.parametrize("answer", ["", "yes", "SEND", "no"])
def test_live_needs_the_exact_confirmation_word(tool, answer, monkeypatch):
    factory = _forbid_network(monkeypatch)
    code, output = _run(tool, ["--live"], env=ENV, answer=answer)
    assert code == tool.EXIT_USAGE and "Cancelled. No request sent." in output
    factory.assert_not_called()


def test_missing_credentials_are_prompted_hidden_and_empty_ones_send_nothing(tool, monkeypatch):
    factory = _forbid_network(monkeypatch)
    prompts = []

    def hidden(prompt):
        prompts.append(prompt)
        return "   "

    code, output = _run(tool, ["--live", "--yes"], secrets=hidden)
    assert code == tool.EXIT_USAGE and "No request sent." in output
    assert len(prompts) == 2
    factory.assert_not_called()


def test_live_success_sends_exactly_two_requests_and_prints_no_secret(tool, monkeypatch):
    pytest.importorskip("_ktradelink_native")
    factory, connections = _serve(monkeypatch, (200, TOKEN_BODY), (200, QUOTE_BODY))
    code, output = _run(tool, ["--live", "--yes"], env=ENV)
    assert code == tool.EXIT_OK, output
    assert factory.call_count == 2
    assert [c.request.call_args.args for c in connections] == [
        ("POST", "/oauth2/token"), ("POST", "/stock/market-data")]
    assert "[1/2 token] OK" in output
    assert "[2/2 quote] OK: 005930 last=72000 volume=15" in output
    _assert_clean(output)


def test_token_http_error_stops_before_the_quote(tool, monkeypatch):
    body = json.dumps({"error": "invalid_client",
                       "error_description": f"unknown appkey {KEY}"}).encode()
    factory, _ = _serve(monkeypatch, (401, body))
    code, output = _run(tool, ["--live", "--yes"], env=ENV)
    assert code == tool.EXIT_FAILED
    assert factory.call_count == 1
    assert "[1/2 token] FAILED: http_unauthorized" in output
    assert "gateway code: invalid_client" in output
    # Upstream text is hidden unless asked for, and then still redacted.
    assert "gateway message: hidden" in output and "unknown appkey" not in output
    _serve(monkeypatch, (401, body))
    code, output = _run(tool, ["--live", "--yes", "--show-gateway-message"], env=ENV)
    assert "unknown appkey <redacted>" in output
    _assert_clean(output)


def test_unexpected_token_shape_reports_types_not_values(tool, monkeypatch):
    body = json.dumps({"access_token": TOKEN, "scope": "oob", "token_type": "Bearer",
                       "expires_in": "86400"}).encode()
    factory, _ = _serve(monkeypatch, (200, body))
    code, output = _run(tool, ["--live", "--yes"], env=ENV)
    assert code == tool.EXIT_FAILED and factory.call_count == 1
    assert "token_response_invalid_or_unverified" in output
    assert "expires_in: string:digits" in output
    assert "access_token: string:text" in output
    _assert_clean(output)


def test_quote_gateway_error_is_redacted(tool, monkeypatch):
    body = json.dumps({"rsp_cd": "SYNTH1", "rsp_msg": f"bad token {TOKEN}"}).encode()
    factory, _ = _serve(monkeypatch, (200, TOKEN_BODY), (500, body))
    code, output = _run(tool, ["--live", "--yes", "--show-gateway-message"], env=ENV)
    assert code == tool.EXIT_FAILED and factory.call_count == 2
    assert "[2/2 quote] FAILED: http_server_error (delivery: response_received)" in output
    assert "gateway code: SYNTH1" in output and "bad token <redacted>" in output
    _assert_clean(output)


def test_undecodable_quote_reports_field_kind_status_and_shape(tool, monkeypatch):
    pytest.importorskip("_ktradelink_native")
    body = json.dumps({"rsp_cd": "SYNTH2", "rsp_msg": "SYNTHETIC_OK",
                       "t1102OutBlock": {"shcode": "005930", "price": "SYNTHETIC_NAME"}}).encode()
    _serve(monkeypatch, (200, TOKEN_BODY), (200, body))
    code, output = _run(tool, ["--live", "--yes"], env=ENV)
    assert code == tool.EXIT_FAILED
    assert "[2/2 quote] FAILED to decode: rsp_cd: SourceStatus" in output
    assert "gateway code: SYNTH2" in output
    assert "t1102OutBlock.price: string:text" in output
    assert "gateway message: hidden" in output and "SYNTHETIC_OK" not in output
    assert "SYNTHETIC_NAME" not in output and TOKEN not in output and KEY not in output


def test_quote_connect_failure_is_static(tool, monkeypatch):
    factory, connections = _serve(monkeypatch, (200, TOKEN_BODY), (200, b""))
    connections[1].connect.side_effect = OSError(f"SYNTHETIC {TOKEN}")
    code, output = _run(tool, ["--live", "--yes"], env=ENV)
    assert code == tool.EXIT_FAILED
    assert "[2/2 quote] FAILED: https_connect_failed (delivery: not_sent)" in output
    _assert_clean(output)


# --- ChatGPT review of PR #27, H1: secrets reflected by the gateway ---------

def test_a_gateway_code_echoing_the_key_is_redacted(tool, monkeypatch):
    body = json.dumps({"error": KEY, "error_description": "synthetic error"}).encode()
    _serve(monkeypatch, (401, body))
    code, output = _run(tool, ["--live", "--yes", "--show-gateway-message"], env=ENV)
    assert code == tool.EXIT_FAILED
    assert "gateway code: <redacted>" in output
    _assert_clean(output)


def test_a_response_key_named_like_a_secret_is_masked(tool, monkeypatch):
    body = json.dumps({"token_type": "Bearer", SECRET: "unexpected field",
                       "nested": {KEY: 1}}).encode()
    _serve(monkeypatch, (200, body))
    code, output = _run(tool, ["--live", "--yes"], env=ENV)
    assert code == tool.EXIT_FAILED
    assert "<key>: string:text" in output and "token_type: string:text" in output
    _assert_clean(output)


@pytest.mark.parametrize("key,secret", [("abc", "SYNTHETIC_LONG_SECRET"),
                                        ("SYNTHETIC_LONG_KEY", "def"),
                                        ("1234567", "SYNTHETIC_LONG_SECRET")])
def test_credentials_too_short_to_redact_are_refused_before_sending(tool, key, secret,
                                                                      monkeypatch):
    factory = _forbid_network(monkeypatch)
    env = {"KTRADELINK_LS_APP_KEY": key, "KTRADELINK_LS_APP_SECRET": secret}
    code, output = _run(tool, ["--live", "--yes"], env=env)
    assert code == tool.EXIT_USAGE and "No request sent." in output
    assert key not in output and secret not in output
    factory.assert_not_called()


# --- ChatGPT review of PR #27, M2: decoder preflight ------------------------

def _fake_native(**attributes):
    module = types.ModuleType("_ktradelink_native")
    module.CONTRACT_VERSION = 1
    module.CORE_VERSION = "synthetic-old-build"
    for name, value in attributes.items():
        setattr(module, name, value)
    return module


@pytest.mark.parametrize("module", [
    _fake_native(),                                                   # no decoder at all
    _fake_native(_decode_ticker_candidate=lambda *a: None),           # wrong return type
    _fake_native(_decode_ticker_candidate=MagicMock(side_effect=ValueError("price: X"))),
])
def test_a_build_without_a_working_ls_decoder_opens_no_connection(tool, module, monkeypatch):
    monkeypatch.setitem(sys.modules, "_ktradelink_native", module)
    factory = _forbid_network(monkeypatch)
    code, output = _run(tool, ["--live", "--yes"], env=ENV, native=None)
    assert code == tool.EXIT_USAGE
    assert "native LS decoder is missing or not working" in output
    assert "No request sent." in output
    factory.assert_not_called()
    code, output = _run(tool, [], env=ENV, native=None)
    assert code == tool.EXIT_OK and "native decoder: NOT available" in output


def test_the_real_native_decoder_passes_the_preflight(tool):
    pytest.importorskip("_ktradelink_native")
    assert tool._native_available() is True
