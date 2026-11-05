"""Six-broker offline HTTP templates: no network, no secrets, no fake live API."""

import dataclasses
import json
import subprocess
import sys

import pytest

from ktradelink._request_plan import (
    AuthRequirements,
    OfflineResponseRejected,
    QuotePlanUnavailable,
    QuoteRequestPlan,
    authentication_requirements,
    decode_offline_quote_response,
    plan_ticker_request,
)

BROKERS = ("kis", "kiwoom", "ls", "db", "toss", "meritz")
EXPECTED = {
    "kis": (
        "GET",
        "https://openapi.koreainvestment.com:9443",
        "/uapi/domestic-stock/v1/quotations/inquire-price",
        (("fid_cond_mrkt_div_code", "J"), ("fid_input_iscd", "005930")),
    ),
    "kiwoom": ("POST", "https://api.kiwoom.com", "/api/dostk/stkinfo", ()),
    "ls": (
        "POST",
        "https://openapi.ls-sec.co.kr:8080",
        "/stock/market-data",
        (),
    ),
    "db": (
        "POST",
        "https://openapi.dbsec.co.kr:8443",
        "/api/v1/quote/kr-stock/inquiry/price",
        (),
    ),
    "toss": (
        "GET",
        "https://openapi.tossinvest.com",
        "/api/v1/prices",
        (("symbols", "005930"),),
    ),
    "meritz": (
        "GET",
        "https://openapi.imeritz.com:9443",
        "/market/v1/prices",
        (("mrkt_div_code", "J"), ("iscd", "005930")),
    ),
}



def test_offline_quote_return_type_resolves_without_loading_native() -> None:
    """A runtime-resolvable Ticker hint must not eagerly load the optional Rust module."""
    code = (
        "import sys\n"
        "from typing import get_type_hints\n"
        "from ktradelink._request_plan import decode_offline_quote_response\n"
        "from ktradelink.models import Ticker\n"
        "assert get_type_hints(decode_offline_quote_response)['return'] is Ticker\n"
        "assert 'ktradelink._native' not in sys.modules\n"
        "assert '_ktradelink_native' not in sys.modules\n"
    )
    subprocess.run([sys.executable, "-I", "-c", code], check=True)

@pytest.mark.parametrize("broker", BROKERS)
def test_all_six_provider_quote_templates_have_exact_documented_shapes(
    broker: str,
) -> None:
    plan = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
    assert isinstance(plan, QuoteRequestPlan)
    assert (plan.method, plan.origin, plan.path, plan.query) == EXPECTED[broker]
    assert plan.broker == broker and plan.symbol == "005930"
    assert plan.transport_implemented is False
    assert plan.auth.token_exchange_implemented is False
    assert plan.origin.startswith("https://")
    assert plan.venue == "KRX"
    assert plan.evidence_level == "publisher_quote_example"


def test_native_quote_specific_fixed_headers_are_not_credentials() -> None:
    kis = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
    kiwoom = plan_ticker_request("kiwoom", "005930", venue="KRX", environment="live")
    ls = plan_ticker_request("ls", "005930", venue="KRX", environment="live")
    db = plan_ticker_request("db", "005930", venue="KRX", environment="live")
    toss = plan_ticker_request("toss", "005930", venue="KRX", environment="live")
    meritz = plan_ticker_request("meritz", "005930", venue="KRX", environment="live")
    assert ("tr_id", "FHKST01010100") in kis.public_headers
    assert ("api-id", "ka10001") in kiwoom.public_headers
    assert ("tr_cd", "t1102") in ls.public_headers
    assert all(name != "tr_id" for name, _ in ls.public_headers)  # not the onboarding demo
    assert dict(db.public_headers) == {
        "content-type": "application/json; charset=utf-8", "cont_yn": "N", "cont_key": "",
    }  # no partner-only mac_address
    assert toss.public_headers == () and meritz.public_headers == ()
    assert kis.auth.quote_header_names == ("authorization", "appkey", "appsecret")
    assert meritz.auth.quote_header_names == ("authorization", "mac_address")
    assert toss.auth.quote_header_names == ("authorization",)
    assert "X-Tossinvest-Account" not in repr(toss)


@pytest.mark.parametrize("broker", BROKERS)
def test_auth_requirement_types_only_no_secrets_or_exchange(broker: str) -> None:
    a = authentication_requirements(broker, environment="live")
    assert isinstance(a, AuthRequirements)
    assert a.token_origin == EXPECTED[broker][1]
    assert a.token_exchange_implemented is False
    assert a.token_path in {"/oauth2/token", "/oauth2/tokenP"}
    assert not hasattr(a, "access_token")
    assert not hasattr(a, "appkey")
    assert not hasattr(a, "secretkey")
    assert not hasattr(a, "__dict__")
    assert "client_credentials" not in a.credential_field_names
    assert all("secret" in key or "key" in key or "client" in key
               for key in a.credential_field_names)


@pytest.mark.parametrize("broker", BROKERS)
def test_plans_are_immutable_and_have_no_sensitive_fields(broker: str) -> None:
    plan = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
    with pytest.raises(dataclasses.FrozenInstanceError):
        plan.origin = "https://attacker.invalid"
    with pytest.raises(dataclasses.FrozenInstanceError):
        plan.query = (("redirect", "https://attacker.invalid"),)
    assert plan.auth.credential_field_names
    assert plan.json_body is None or "secret" not in plan.json_body
    assert "Bearer " not in repr(plan)
    assert not hasattr(plan, "headers")  # Prevent misreading as authenticated wire headers.


def test_post_bodies_are_exactly_evidenced_and_not_unauthorized_order_calls() -> None:
    k = plan_ticker_request("kiwoom", "005930", venue="KRX", environment="live")
    d = plan_ticker_request("db", "005930", venue="KRX", environment="live")
    assert json.loads(k.json_body) == {"stk_cd": "005930"}
    assert json.loads(d.json_body) == {
        "In": {"InputCondMrktDivCode": "J", "InputIscd1": "005930"}
    }  # API guide PRICE example and SDK: bare code for J, not the testbed's "A005930"
    for broker in ("kis", "toss", "meritz"):
        plan = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
        assert plan.json_body is None and plan.method == "GET"
    assert all("/order" not in EXPECTED[b][2] for b in BROKERS)


@pytest.mark.parametrize("broker", BROKERS)
@pytest.mark.parametrize("venue", ["NXT", "BROKER_COMPOSITE", "SOR", "", None, True])
def test_unverified_market_never_falls_back(broker: str, venue: object) -> None:
    with pytest.raises(QuotePlanUnavailable, match="Venue"):
        plan_ticker_request(broker, "005930", venue=venue, environment="live")


@pytest.mark.parametrize("broker", BROKERS)
@pytest.mark.parametrize(
    "symbol",
    ["", "00593", "0059300", "005 930", "005930\n", "005930\t",
     "005930/extra", "005930?token=abc", "000660,005930", "종목", True, 5930],
)
def test_bad_or_injected_symbol_rejected_without_reflection(
    broker: str, symbol: object
) -> None:
    with pytest.raises(QuotePlanUnavailable) as exc:
        plan_ticker_request(broker, symbol, venue="KRX", environment="live")
    assert "token=abc" not in str(exc.value)


@pytest.mark.parametrize("broker", ["kiwoom", "ls"])
@pytest.mark.parametrize("symbol", ["0000D0", "0101N0", "00593A", "ABCDEF"])
def test_alphanumeric_symbol_is_not_planned_without_broker_evidence(
    broker: str, symbol: str
) -> None:
    # ADR 0016: Kiwoom and LS documents neither show nor exclude such codes.
    with pytest.raises(QuotePlanUnavailable, match="Symbol"):
        plan_ticker_request(broker, symbol, venue="KRX", environment="live")


ALPHANUMERIC_SYMBOL_IN_REQUEST = {
    "kis": lambda plan: plan.query == (("fid_cond_mrkt_div_code", "J"),
                                       ("fid_input_iscd", plan.symbol)),
    "db": lambda plan: json.loads(plan.json_body) == {
        "In": {"InputCondMrktDivCode": "J", "InputIscd1": plan.symbol}},
    "toss": lambda plan: plan.query == (("symbols", plan.symbol),),
    "meritz": lambda plan: plan.query == (("mrkt_div_code", "J"), ("iscd", plan.symbol)),
}


@pytest.mark.parametrize("broker", sorted(ALPHANUMERIC_SYMBOL_IN_REQUEST))
@pytest.mark.parametrize("symbol", ["0000D0", "0101N0", "005930"])
def test_alphanumeric_symbol_is_planned_verbatim_where_evidenced(
    broker: str, symbol: str
) -> None:
    # ADR 0016: KIS/Meritz master observation, DB example, Toss documented.
    # Gateway acceptance of an alphanumeric code is NOT verified.
    plan = plan_ticker_request(broker, symbol, venue="KRX", environment="live")
    assert plan.symbol == symbol
    assert ALPHANUMERIC_SYMBOL_IN_REQUEST[broker](plan)


@pytest.mark.parametrize("broker", BROKERS)
@pytest.mark.parametrize(
    "symbol",
    ["0000d0", "0101n0", "A005930", "Q500001", "J005930", "005930_NX", "005930_AL",
     "N-005930", "U-005930", "0000D", "0000D00", "0000Ｄ0", "00593é", " 0000D0",
     "0000D0 ", "0000 D"],
)
def test_public_symbol_grammar_is_enforced_for_every_broker(
    broker: str, symbol: str
) -> None:
    # No case folding, trimming or prefix/suffix stripping, even for Toss whose
    # request pattern admits lower case (ADR 0016).
    with pytest.raises(QuotePlanUnavailable, match="Symbol"):
        plan_ticker_request(broker, symbol, venue="KRX", environment="live")


@pytest.mark.parametrize("broker", BROKERS)
def test_unsupported_environment_is_explicit(broker: str) -> None:
    with pytest.raises(QuotePlanUnavailable):
        plan_ticker_request(broker, "005930", venue="KRX", environment="demo")
    if broker not in {"kis", "kiwoom"}:
        with pytest.raises(QuotePlanUnavailable):
            authentication_requirements(broker, environment="paper")


def test_only_official_paper_hosts_and_no_live_fallback() -> None:
    kis = plan_ticker_request("kis", "005930", venue="KRX", environment="paper")
    kiwi = plan_ticker_request("kiwoom", "005930", venue="KRX", environment="paper")
    assert kis.origin == "https://openapivts.koreainvestment.com:29443"
    assert kiwi.origin == "https://mockapi.kiwoom.com"
    assert kis.auth.token_origin == kis.origin
    assert kiwi.auth.token_origin == kiwi.origin


@pytest.mark.parametrize("broker", ["", "shinan", "Shinhan", "unknown", None, 42, True])
def test_unknown_broker_never_gets_fallback_origin(broker: object) -> None:
    with pytest.raises(QuotePlanUnavailable):
        plan_ticker_request(broker, "005930", venue="KRX", environment="live")


def test_db_token_metadata_is_the_form_body_not_the_unsafe_query_sample() -> None:
    auth = authentication_requirements("db", environment="live")
    assert auth.token_request_format == "form"
    assert auth.scope == "oob"
    assert auth.token_exchange_implemented is False
    assert "appkey" in auth.credential_field_names
    assert "appsecretkey" in auth.credential_field_names
    assert "?" not in auth.token_path and "?" not in auth.token_origin
    assert "verify=False" not in repr(auth)


def test_meritz_mac_requirement_is_metadata_not_automatic_collection() -> None:
    auth = authentication_requirements("meritz", environment="live")
    assert "mac_address" in auth.quote_header_names
    plan = plan_ticker_request("meritz", "005930", venue="KRX", environment="live")
    assert "mac_address" not in dict(plan.public_headers)
    assert "mac_address" not in plan.json_body if plan.json_body is not None else True


@pytest.mark.parametrize("status", [None, True, False, 0, 199, 300, 401, 429, 500, "200"])
def test_non_success_mock_status_fails_before_native_import(status: object, monkeypatch) -> None:
    from ktradelink import _native

    monkeypatch.setattr(
        _native,
        "decode_ticker_candidate",
        lambda *_args: pytest.fail("must reject before invoking Rust"),
    )
    plan = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
    with pytest.raises(OfflineResponseRejected):
        decode_offline_quote_response(plan, http_status=status, json_text='{"output":{}}')


def test_modified_request_plan_is_rejected_before_native_import(monkeypatch) -> None:
    from ktradelink import _native

    monkeypatch.setattr(
        _native, "decode_ticker_candidate",
        lambda *_args: pytest.fail("must reject tampering"),
    )
    plan = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
    changed = dataclasses.replace(plan, origin="https://attacker.invalid")
    with pytest.raises(QuotePlanUnavailable, match="Unrecognized"):
        decode_offline_quote_response(changed, http_status=200, json_text="{}")


def test_offline_mock_valid_status_invokes_native_once(monkeypatch) -> None:
    from ktradelink import _native

    calls = []

    def fake_decode(*args):
        calls.append(args)
        return object()

    monkeypatch.setattr(_native, "decode_ticker_candidate", fake_decode)
    plan = plan_ticker_request("toss", "005930", venue="KRX", environment="live")
    result = decode_offline_quote_response(plan, http_status=200, json_text="{}")
    assert result is not None and len(calls) == 1
    assert calls[0] == ("toss", "005930", "KRX", "{}")


def test_mock_http_success_is_not_evidence_of_broker_venue_or_source() -> None:
    plan = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
    assert plan.venue == "KRX"
    assert plan.transport_implemented is False
    assert plan.evidence_level == "publisher_quote_example"


def test_ls_t1102_body_always_names_krx_explicitly() -> None:
    # LS treats an unknown exchgubun as KRX; never leave the venue implicit.
    ls = plan_ticker_request("ls", "005930", venue="KRX", environment="live")
    assert json.loads(ls.json_body) == {
        "t1102InBlock": {"shcode": "005930", "exchgubun": "K"}
    }
    assert dict(ls.public_headers) == {
        "content-type": "application/json; charset=utf-8",
        "tr_cd": "t1102",
        "tr_cont": "N",
        "tr_cont_key": "",
        "mac_address": "",
    }
    for venue in ("NXT", "SOR", "COMPOSITE"):
        with pytest.raises(QuotePlanUnavailable):
            plan_ticker_request("ls", "005930", venue=venue, environment="live")
    with pytest.raises(QuotePlanUnavailable):
        plan_ticker_request("ls", "005930", venue="KRX", environment="paper")
