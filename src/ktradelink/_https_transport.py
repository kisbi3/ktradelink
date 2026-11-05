"""Private, explicit opt-in HTTPS wire transport; no automatic broker access.

This module can assemble KIS/Kiwoom *candidate* token/quote requests from
publisher examples, but actual broker contract/provenance is NOT verified.
Network I/O is disabled by default and never exercised in CI. No redirects,
proxies, retries, account calls or orders. Not a public fetch_ticker adapter.
"""

import http.client
import json
import ssl
import time
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlencode, urlsplit

from ktradelink._credential_runtime import (
    BearerLease,
    CredentialError,
    CredentialIdentity,
    CredentialPair,
    CredentialSnapshot,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._request_plan import (
    AuthRequirements,
    QuoteRequestPlan,
    authentication_requirements,
    plan_ticker_request,
)

MAX_RESPONSE_BYTES = 1_048_576  # Our own cap; NOT a publisher limit.


class DeliveryState(Enum):
    NOT_SENT = "not_sent"
    UNKNOWN = "may_have_been_sent"
    RESPONSE_RECEIVED = "response_received"


class TransportFailure(Enum):
    INVALID_REQUEST = "invalid_http_request"
    NOT_ENABLED = "real_network_disabled"
    STALE_CREDENTIAL = "credential_changed_before_send"
    TOKEN_UNAVAILABLE = "token_invalid_before_send"
    EVIDENCE_MISSING = "broker_wire_contract_not_verified"
    CONNECT = "https_connect_failed"
    TLS = "tls_handshake_failed"
    WRITE = "request_write_failed_or_unknown"
    RESPONSE = "response_headers_unavailable"
    READ = "response_body_read_failed"
    OVERSIZED = "response_body_exceeds_library_limit"
    REDIRECT = "redirect_refused"
    UNAUTHORIZED = "http_unauthorized"
    FORBIDDEN = "http_forbidden"
    RATE_LIMITED = "http_rate_limited"
    SERVER = "http_server_error"
    HTTP = "http_status_rejected"


class TransportError(RuntimeError):
    """Only static classifications; no URL, headers, body, or origin exception."""

    def __init__(self, kind: TransportFailure, delivery: DeliveryState):
        self.kind = kind
        self.delivery = delivery
        super().__init__(kind.value)


def _reject(kind: TransportFailure, delivery: DeliveryState = DeliveryState.NOT_SENT) -> None:
    raise TransportError(kind, delivery)


_SUPPORTED_CANDIDATES = frozenset(("kis", "kiwoom"))


@dataclass(frozen=True, slots=True, repr=False)
class WireRequest:
    """Transient private request: body/headers can contain secrets; NEVER log."""

    source: AuthRequirements | QuoteRequestPlan = field(repr=False, compare=False)
    method: str
    origin: str
    path: str
    query: tuple[tuple[str, str], ...]
    headers: tuple[tuple[str, str], ...] = field(repr=False)
    body: bytes | None = field(repr=False)
    purpose: str
    credential_snapshot: CredentialSnapshot | None = field(default=None, repr=False, compare=False)

    bearer_lease: BearerLease | None = field(default=None, repr=False, compare=False)
    token_cache: InMemoryTokenCache | None = field(default=None, repr=False, compare=False)

    def __repr__(self) -> str:
        return "WireRequest(<redacted>)"

    def __post_init__(self) -> None:
        if type(self.source) is QuoteRequestPlan:
            try:
                canonical = plan_ticker_request(
                    self.source.broker, self.source.symbol,
                    venue=self.source.venue, environment=self.source.environment,
                )
            except (TypeError, ValueError):
                _reject(TransportFailure.INVALID_REQUEST)
            if self.source != canonical or self.purpose != "quote":
                _reject(TransportFailure.INVALID_REQUEST)
            if (self.method, self.origin, self.path, self.query) != (
                canonical.method, canonical.origin, canonical.path, canonical.query
            ):
                _reject(TransportFailure.INVALID_REQUEST)
        elif type(self.source) is AuthRequirements:
            try:
                canonical = authentication_requirements(
                    self.source.broker, environment=self.source.environment
                )
            except (TypeError, ValueError):
                _reject(TransportFailure.INVALID_REQUEST)
            if self.source != canonical or self.purpose != "token":
                _reject(TransportFailure.INVALID_REQUEST)
            if (self.method, self.origin, self.path, self.query) != (
                "POST", canonical.token_origin, canonical.token_path, ()
            ):
                _reject(TransportFailure.INVALID_REQUEST)
        else:
            _reject(TransportFailure.INVALID_REQUEST)

        if (type(self.credential_snapshot) is not CredentialSnapshot
                or type(self.credential_snapshot.identity) is not CredentialIdentity
                or type(self.credential_snapshot.pair) is not CredentialPair
                or type(self.credential_snapshot.owner) is not InMemoryCredentialProvider
                or self.credential_snapshot.identity.broker != self.source.broker
                or self.credential_snapshot.identity.environment != self.source.environment):
            _reject(TransportFailure.INVALID_REQUEST)
        if self.source.broker not in _SUPPORTED_CANDIDATES:
            _reject(TransportFailure.EVIDENCE_MISSING)
        parsed = urlsplit(self.origin)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
                or parsed.password is not None or parsed.path or parsed.query or parsed.fragment
                or parsed.hostname not in self.origin):
            _reject(TransportFailure.INVALID_REQUEST)
        if type(self.method) is not str or self.method not in ("GET", "POST"):
            _reject(TransportFailure.INVALID_REQUEST)
        if (type(self.body) not in (bytes, type(None)) or type(self.headers) is not tuple
                or type(self.query) is not tuple):
            _reject(TransportFailure.INVALID_REQUEST)
        if type(self.path) is not str or not self.path.startswith("/") or self.path.startswith("//"):
            _reject(TransportFailure.INVALID_REQUEST)
        if ("?" in self.path or "#" in self.path or "\r" in self.path
                or "\n" in self.path or "\\" in self.path):
            _reject(TransportFailure.INVALID_REQUEST)
        sensitive = {"appkey", "appsecret", "appsecretkey", "secretkey", "client_secret",
                     "client_id", "authorization", "token", "access_token", "password"}
        for item in self.query:
            if type(item) is not tuple or len(item) != 2:
                _reject(TransportFailure.INVALID_REQUEST)
            key, value = item
            if (type(key) is not str or type(value) is not str or key.lower() in sensitive
                    or any(c in key + value for c in "\r\n\x00")):
                _reject(TransportFailure.INVALID_REQUEST)
        if len(self.headers) > 32:
            _reject(TransportFailure.INVALID_REQUEST)
        seen: set[str] = set()
        for item in self.headers:
            if type(item) is not tuple or len(item) != 2:
                _reject(TransportFailure.INVALID_REQUEST)
            name, value = item
            if (type(name) is not str or type(value) is not str
                    or not name or not name.isascii() or not all(
                        c.isalnum() or c in "-_" for c in name
                    ) or any(c in value for c in "\r\n\x00")):
                _reject(TransportFailure.INVALID_REQUEST)
            if name.lower() in seen:
                _reject(TransportFailure.INVALID_REQUEST)
            seen.add(name.lower())
        if len(self.body or b"") > MAX_RESPONSE_BYTES:
            _reject(TransportFailure.INVALID_REQUEST)
        if self.method == "GET" and self.body is not None:
            _reject(TransportFailure.INVALID_REQUEST)

        # Validate the entire wire shape, not only its destination. No arbitrary
        # Host/framing headers, alternate symbols, or unrelated secret payloads.
        pair = self.credential_snapshot.pair
        if self.purpose == "token":
            if self.bearer_lease is not None or self.token_cache is not None:
                _reject(TransportFailure.INVALID_REQUEST)
            key_name, secret_name = self.source.credential_field_names
            expected_body = json.dumps({
                "grant_type": "client_credentials",
                key_name: pair.client_key,
                secret_name: pair.client_secret,
            }, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
            expected_headers = (("content-type", "application/json;charset=UTF-8"),)
        else:
            if (type(self.bearer_lease) is not BearerLease
                    or type(self.token_cache) is not InMemoryTokenCache
                    or self.bearer_lease.snapshot is not self.credential_snapshot):
                _reject(TransportFailure.INVALID_REQUEST)
            expected_headers = self.source.public_headers + (
                ("authorization", f"Bearer {self.bearer_lease.access_token}"),
            )
            if self.source.broker == "kis":
                expected_headers += (("appkey", pair.client_key), ("appsecret", pair.client_secret))
            expected_body = (self.source.json_body.encode("utf-8")
                             if self.source.json_body is not None else None)
        if self.body != expected_body or self.headers != expected_headers:
            _reject(TransportFailure.INVALID_REQUEST)


@dataclass(frozen=True, slots=True, repr=False)
class WireResponse:
    """Untrusted HTTP bytes, not authenticated quote/exchange provenance."""

    request: WireRequest = field(repr=False, compare=False)
    status: int
    body: bytes = field(repr=False)

    def __repr__(self) -> str:
        return "WireResponse(<redacted>)"

    @property
    def json_text(self) -> str:
        try:
            text = self.body.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            text = None
        if text is None:
            _reject(TransportFailure.READ, DeliveryState.RESPONSE_RECEIVED)
        return text


def _candidate_broker(identity: CredentialIdentity) -> None:
    if identity.broker not in _SUPPORTED_CANDIDATES:
        _reject(TransportFailure.EVIDENCE_MISSING)


def build_token_request(
    identity: CredentialIdentity, provider: InMemoryCredentialProvider,
) -> WireRequest:
    """KIS/Kiwoom candidate token POST based on publisher examples, no sending."""
    if type(identity) is not CredentialIdentity or type(provider) is not InMemoryCredentialProvider:
        _reject(TransportFailure.INVALID_REQUEST)
    _candidate_broker(identity)
    creds = provider.load(identity)
    provider.require_current(creds)
    auth = authentication_requirements(identity.broker, environment=identity.environment)
    key_name, secret_name = auth.credential_field_names
    # Only the verified JSON sample shapes are implemented here. Never clone DB's
    # unsafe URL credential example or infer other brokers' token body semantics.
    if auth.token_request_format != "json":
        _reject(TransportFailure.EVIDENCE_MISSING)
    body = json.dumps({
        "grant_type": "client_credentials",
        key_name: creds.pair.client_key,
        secret_name: creds.pair.client_secret,
    }, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return WireRequest(
        auth, "POST", auth.token_origin, auth.token_path, (),
        (("content-type", "application/json;charset=UTF-8"),), body, "token",
        credential_snapshot=creds,
    )


def build_quote_request(
    plan: QuoteRequestPlan, identity: CredentialIdentity,
    provider: InMemoryCredentialProvider, tokens: InMemoryTokenCache,
    *, now_ms: int,
) -> WireRequest:
    """Candidate HTTP quote request, never an attested broker or market adapter."""
    if (type(plan) is not QuoteRequestPlan or type(identity) is not CredentialIdentity
            or type(provider) is not InMemoryCredentialProvider
            or type(tokens) is not InMemoryTokenCache):
        _reject(TransportFailure.INVALID_REQUEST)
    _candidate_broker(identity)
    if (identity.broker, identity.environment) != (plan.broker, plan.environment):
        _reject(TransportFailure.INVALID_REQUEST)
    credential = provider.load(identity)
    lease = tokens.get(provider, identity, now_ms=now_ms)
    if lease.snapshot is not credential:
        _reject(TransportFailure.INVALID_REQUEST)
    headers = list(plan.public_headers)
    headers.append(("authorization", f"Bearer {lease.access_token}"))
    if plan.broker == "kis":
        headers.extend((
            ("appkey", credential.pair.client_key),
            ("appsecret", credential.pair.client_secret),
        ))
    return WireRequest(
        plan, plan.method, plan.origin, plan.path, plan.query,
        tuple(headers), plan.json_body.encode("utf-8") if plan.json_body is not None else None,
        "quote", credential_snapshot=credential, bearer_lease=lease, token_cache=tokens,
    )


def _http_kind(status: int) -> TransportFailure | None:
    if status == 200:
        return None
    if 300 <= status < 400:
        return TransportFailure.REDIRECT
    if status == 401:
        return TransportFailure.UNAUTHORIZED
    if status == 403:
        return TransportFailure.FORBIDDEN
    if status == 429:
        return TransportFailure.RATE_LIMITED
    if 500 <= status <= 599:
        return TransportFailure.SERVER
    return TransportFailure.HTTP


def _binding_failure(request: WireRequest, now_ms: int) -> TransportFailure | None:
    snapshot = request.credential_snapshot
    provider = snapshot.owner
    try:
        provider.require_current(snapshot)
    except CredentialError:
        return TransportFailure.STALE_CREDENTIAL
    if request.purpose == "quote":
        try:
            current_lease = request.token_cache.get(provider, snapshot.identity, now_ms=now_ms)
        except CredentialError:
            return TransportFailure.TOKEN_UNAVAILABLE
        if current_lease is not request.bearer_lease:
            return TransportFailure.TOKEN_UNAVAILABLE
    return None


class HttpsTransport:
    """Zero-retry TLS-verified sender; disabled until explicitly opted in.

    Uses http.client directly: it does not read HTTP(S)_PROXY, copy environment
    credentials, follow redirects, keep a cookie jar or reuse connections.
    Never call with real keys without the maintainer's separate live approval.
    """

    __slots__ = ("_enabled", "_timeout_ms")

    def __init__(self, *, network_enabled: bool = False, timeout_ms: int = 5_000):
        if (type(network_enabled) is not bool or type(timeout_ms) is not int
                or not 1 <= timeout_ms <= 60_000):
            _reject(TransportFailure.INVALID_REQUEST)
        self._enabled = network_enabled
        self._timeout_ms = timeout_ms

    def __repr__(self) -> str:
        return "HttpsTransport(<redacted>)"

    def send(self, request: WireRequest, *, now_ms: int | None = None) -> WireResponse:
        """One HTTPS attempt; no reconnect, refresh, retry, or downstream decode."""
        if type(request) is not WireRequest:
            _reject(TransportFailure.INVALID_REQUEST)
        # Defend against mutated/fabricated request objects, not hostile Python.
        request.__post_init__()
        if not self._enabled:
            _reject(TransportFailure.NOT_ENABLED)
        injected_clock = now_ms is not None
        if now_ms is None:
            now_ms = time.time_ns() // 1_000_000
        if type(now_ms) is not int or now_ms < 0:
            _reject(TransportFailure.INVALID_REQUEST)
        binding_failure = _binding_failure(request, now_ms)
        if binding_failure is not None:
            _reject(binding_failure)
        parsed = urlsplit(request.origin)
        target = request.path
        if request.query:
            target += "?" + urlencode(request.query)

        conn = None
        response_status: int | None = None
        response_body: bytes | None = None
        failure: TransportFailure | None = None
        state = DeliveryState.NOT_SENT
        try:
            try:
                # Unlike create_default_context(), this does not inspect
                # SSLKEYLOGFILE and cannot start ambient TLS session-key logging.
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.load_default_certs(ssl.Purpose.SERVER_AUTH)
                # The SDK never disables system CA verification or hostname checking.
                if context.verify_mode != ssl.CERT_REQUIRED or not context.check_hostname:
                    failure = TransportFailure.TLS
                else:
                    conn = http.client.HTTPSConnection(
                        parsed.hostname, port=parsed.port, timeout=self._timeout_ms / 1_000,
                        context=context,
                    )
                    conn.connect()  # handshake completed BEFORE request write
            except ssl.SSLError:
                failure = TransportFailure.TLS
            except Exception:
                failure = TransportFailure.CONNECT

            if failure is None:
                # A slow handshake must not make a revoked/expired lease usable.
                before_write_ms = now_ms if injected_clock else time.time_ns() // 1_000_000
                failure = _binding_failure(request, before_write_ms)
            if failure is None:
                state = DeliveryState.UNKNOWN  # any write failure may be partial
                try:
                    conn.request(
                        request.method, target, body=request.body,
                        headers=dict(request.headers),
                    )
                except Exception:
                    failure = TransportFailure.WRITE

            if failure is None:
                try:
                    response = conn.getresponse()
                    response_status = response.status
                    state = DeliveryState.RESPONSE_RECEIVED
                except Exception:
                    failure = TransportFailure.RESPONSE

            if failure is None:
                if type(response_status) is not int or not 100 <= response_status <= 599:
                    failure = TransportFailure.RESPONSE
                else:
                    failure = _http_kind(response_status)

            if failure is None:
                try:
                    response_body = response.read(MAX_RESPONSE_BYTES + 1)
                    if type(response_body) is not bytes:
                        failure = TransportFailure.READ
                    elif len(response_body) > MAX_RESPONSE_BYTES:
                        failure = TransportFailure.OVERSIZED
                except Exception:
                    failure = TransportFailure.READ
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    # close failure must never disguise the original send outcome
                    pass

        # Outside except handlers: prevent original URL/header/payload exceptions
        # from being retained by the public error via __context__.
        if failure is not None:
            raise TransportError(failure, state)
        assert response_status is not None and response_body is not None
        return WireResponse(request, response_status, response_body)
