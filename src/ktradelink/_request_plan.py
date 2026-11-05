"""Private, entirely offline, six-broker quote request planning.

No OAuth exchange, secrets, token management, HTTP client or live fetch_ticker.
Data are immutable public request TEMPLATE VALUES only. Do not execute a plan
without a separately reviewed transport, credential provider, and response
provenance/venue contract. The existing Python Ticker API is untouched.
"""

import json
from dataclasses import dataclass

from ktradelink.models import Ticker


class QuotePlanUnavailable(ValueError):
    """A provider route, market, identifier or environment is not evidenced."""


class OfflineResponseRejected(ValueError):
    """An offline HTTP response cannot be safely passed to the Rust decoder."""


@dataclass(frozen=True, slots=True)
class AuthRequirements:
    """Credential FIELD NAMES only; NEVER hold actual credentials or access tokens."""

    broker: str
    environment: str
    token_origin: str
    token_path: str
    token_request_format: str
    credential_field_names: tuple[str, ...]
    quote_header_names: tuple[str, ...]
    scope: str | None = None
    token_exchange_implemented: bool = False


@dataclass(frozen=True, slots=True)
class QuoteRequestPlan:
    """Immutable fixed-origin request metadata, never a network request object.

    All values are non-secret. The caller's venue is NOT proof of source
    exchange; the source status is documentation-only.
    """

    broker: str
    environment: str
    symbol: str
    venue: str
    method: str
    origin: str
    path: str
    query: tuple[tuple[str, str], ...]
    public_headers: tuple[tuple[str, str], ...]
    json_body: str | None
    auth: AuthRequirements
    evidence_level: str
    transport_implemented: bool = False


# Deliberately pinned to official publisher examples. Never accept arbitrary
# origins from callers (avoids credential forwarding / SSRF on future work).
_LIVE_ORIGINS = {
    "kis": "https://openapi.koreainvestment.com:9443",
    "kiwoom": "https://api.kiwoom.com",
    "ls": "https://openapi.ls-sec.co.kr:8080",
    "db": "https://openapi.dbsec.co.kr:8443",
    "toss": "https://openapi.tossinvest.com",
    "meritz": "https://openapi.imeritz.com:9443",
}
_PAPER_ORIGINS = {
    "kis": "https://openapivts.koreainvestment.com:29443",
    "kiwoom": "https://mockapi.kiwoom.com",
}


def _origin(broker: str, environment: str) -> str:
    if type(broker) is not str or broker not in _LIVE_ORIGINS:
        raise QuotePlanUnavailable("Unknown or undocumented broker")
    if environment == "live":
        return _LIVE_ORIGINS[broker]
    if environment == "paper" and broker in _PAPER_ORIGINS:
        return _PAPER_ORIGINS[broker]
    raise QuotePlanUnavailable("Unsupported or undocumented broker environment")


def _checked_symbol(broker: str, symbol: str) -> str:
    if type(symbol) is not str or len(symbol) != 6 or not symbol.isascii():
        raise QuotePlanUnavailable("Symbol format not established for this route")
    # The official Toss KR symbol schema includes alphanumeric six-character
    # identifiers. Other current quote request examples show six digits only.
    # Do not confuse public Ticker identifiers with broker request formats.
    if broker == "toss":
        if not symbol.isalnum():
            raise QuotePlanUnavailable("Symbol format not established for this route")
    elif not symbol.isdecimal():
        raise QuotePlanUnavailable("Symbol format not established for this route")
    return symbol


def authentication_requirements(broker: str, *, environment: str) -> AuthRequirements:
    """Describe six provider-specific auth requirements without ANY secrets.

    This does not request a token. DB's provider sample sends credentials in
    URL query and disables TLS verification; DO NOT replicate that flow.
    """
    origin = _origin(broker, environment)

    if broker == "kis":
        token_path = "/oauth2/tokenP"
        request_format = "json"
        names = ("appkey", "appsecret")
        header_names = ("authorization", "appkey", "appsecret")
        scope = None
    elif broker == "kiwoom":
        token_path = "/oauth2/token"
        request_format = "json"
        names = ("appkey", "secretkey")
        header_names = ("authorization",)
        scope = None
    elif broker == "ls":
        token_path = "/oauth2/token"
        request_format = "form"
        names = ("appkey", "appsecretkey")
        header_names = ("authorization",)
        scope = "oob"
    elif broker == "db":
        token_path = "/oauth2/token"
        request_format = "unsafe_query_sample_only"
        names = ("appkey", "appsecretkey")
        header_names = ("authorization",)
        scope = "oob"
    elif broker == "toss":
        token_path = "/oauth2/token"
        request_format = "form"
        names = ("client_id", "client_secret")
        header_names = ("authorization",)
        scope = None
    else:
        token_path = "/oauth2/token"
        request_format = "form"
        names = ("client_id", "client_secret")
        header_names = ("authorization", "mac_address")
        scope = "login"

    return AuthRequirements(
        broker=broker,
        environment=environment,
        token_origin=origin,
        token_path=token_path,
        token_request_format=request_format,
        credential_field_names=names,
        quote_header_names=header_names,
        scope=scope,
    )


def plan_ticker_request(
    broker: str, symbol: str, *, venue: str, environment: str
) -> QuoteRequestPlan:
    """Construct an offline official-example quote TEMPLATE for one KR symbol.

    No network sending or authentication is performed. LS uses the t1102
    REST contract from the publisher's API guide (not the onboarding GET demo).
    The caller must not assume a real exchange-specific response follows.
    """
    origin = _origin(broker, environment)
    if venue != "KRX":
        raise QuotePlanUnavailable("Venue not verified for this offline route")
    code = _checked_symbol(broker, symbol)
    auth = authentication_requirements(broker, environment=environment)

    method = "GET"
    query: tuple[tuple[str, str], ...] = ()
    public_headers: tuple[tuple[str, str], ...] = ()
    json_body: str | None = None
    evidence = "publisher_quote_example"

    if broker == "kis":
        path = "/uapi/domestic-stock/v1/quotations/inquire-price"
        query = (("fid_cond_mrkt_div_code", "J"), ("fid_input_iscd", code))
        public_headers = (("tr_id", "FHKST01010100"),)
    elif broker == "kiwoom":
        method = "POST"
        path = "/api/dostk/stkinfo"
        public_headers = (
            ("api-id", "ka10001"),
            ("content-type", "application/json;charset=UTF-8"),
        )
        json_body = json.dumps({"stk_cd": code}, separators=(",", ":"))
    elif broker == "ls":
        # LS API guide, t1102 REST detail (retrieved 2026-11-05; see
        # docs/brokers/live-auth-transport-gates-2026-11-05.md). LS treats an
        # unknown exchgubun as KRX, so the KRX code "K" is always sent
        # explicitly. mac_address is mandatory only for corporate customers;
        # the publisher sample sends it empty and corporate use is unsupported.
        method = "POST"
        path = "/stock/market-data"
        public_headers = (
            ("content-type", "application/json; charset=utf-8"),
            ("tr_cd", "t1102"),
            ("tr_cont", "N"),
            ("tr_cont_key", ""),
            ("mac_address", ""),
        )
        json_body = json.dumps(
            {"t1102InBlock": {"shcode": code, "exchgubun": "K"}},
            separators=(",", ":"),
        )
    elif broker == "db":
        method = "POST"
        path = "/api/v1/quote/kr-stock/inquiry/price"
        public_headers = (
            ("content-type", "application/json; charset=utf-8"),
            ("cont_yn", ""),
            ("cont_key", ""),
        )
        json_body = json.dumps(
            {"In": {"InputCondMrktDivCode": "J", "InputIscd1": "A" + code}},
            separators=(",", ":"),
        )
    elif broker == "toss":
        path = "/api/v1/prices"
        query = (("symbols", code),)
    else:
        path = "/market/v1/prices"
        query = (("mrkt_div_code", "J"), ("iscd", code))

    return QuoteRequestPlan(
        broker=broker,
        environment=environment,
        symbol=code,
        venue=venue,
        method=method,
        origin=origin,
        path=path,
        query=query,
        public_headers=public_headers,
        json_body=json_body,
        auth=auth,
        evidence_level=evidence,
    )


def decode_offline_quote_response(
    plan: QuoteRequestPlan, *, http_status: int, json_text: str
) -> Ticker:
    """Test-only status gate -> existing native parser -> existing Python Ticker.

    This does not send anything. The HTTP status and JSON were supplied by
    the caller, NOT vouched for as a real broker response. Never log
    the response body; even malformed JSON could contain sensitive fields.
    """
    if type(plan) is not QuoteRequestPlan:
        raise QuotePlanUnavailable("Invalid offline quote plan")
    expected = plan_ticker_request(
        plan.broker, plan.symbol, venue=plan.venue, environment=plan.environment
    )
    if plan != expected:
        raise QuotePlanUnavailable("Unrecognized or modified offline quote plan")
    if type(http_status) is not int or not 200 <= http_status < 300:
        raise OfflineResponseRejected("Offline HTTP response is not successful")
    if type(json_text) is not str:
        raise OfflineResponseRejected("Offline response body must be JSON text")
    from ktradelink._native import decode_ticker_candidate

    return decode_ticker_candidate(plan.broker, plan.symbol, plan.venue, json_text)
