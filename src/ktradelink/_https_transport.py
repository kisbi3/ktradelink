"""Private, explicit opt-in HTTPS wire transport; no automatic broker access.

This module can assemble KIS/Kiwoom/LS/DB/Toss *candidate* token/quote
requests from publisher evidence, but actual broker contract/provenance is
NOT verified.
Meritz stays blocked.
Network I/O is disabled by default and never exercised in CI. No redirects,
proxies, retries, account calls or orders. Not a public fetch_ticker adapter.
"""

import hashlib
import http.client
import itertools
import json
import ssl
import threading
import time
import weakref
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
from ktradelink._diagnostics import GatewayStatus, gateway_status
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
    TOKEN_IN_FLIGHT = "token_exchange_already_in_flight"
    QUOTE_IN_FLIGHT = "toss_quote_write_in_flight"
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
    """Only static classifications; no URL, headers, body, or origin exception.

    ``diagnostic`` is ``None`` unless the sender opted in with
    ``collect_diagnostics=True`` and an HTTP error response carried a status
    envelope. It holds only the sanitised, redacted code and message from
    ``_diagnostics.gateway_status`` and never appears in ``str``/``repr``.
    """

    def __init__(self, kind: TransportFailure, delivery: DeliveryState,
                 diagnostic: GatewayStatus | None = None):
        self.kind = kind
        self.delivery = delivery
        self.diagnostic = diagnostic
        super().__init__(kind.value)


def _reject(kind: TransportFailure, delivery: DeliveryState = DeliveryState.NOT_SENT) -> None:
    raise TransportError(kind, delivery)


# Meritz stays out: every Meritz error is HTTP 500 and its quote needs a MAC.
_SUPPORTED_CANDIDATES = frozenset(("kis", "kiwoom", "ls", "db", "toss"))


def _token_wire(
    auth: AuthRequirements, pair: CredentialPair,
) -> tuple[bytes, tuple[tuple[str, str], ...]]:
    """The one canonical token body/header shape per evidenced broker.

    KIS/Kiwoom: JSON from their pinned publisher samples. LS: form body from
    its API guide token detail. DB: the same form fields, from its API guide
    token detail and the official SDK at 564b5100 (ADR 0015); the testbed's
    URL-query sample is never built. TLS verification is never disabled.
    Every other broker fails closed.
    """
    key_name, secret_name = auth.credential_field_names
    if auth.broker in ("kis", "kiwoom") and auth.token_request_format == "json":
        body = json.dumps({
            "grant_type": "client_credentials",
            key_name: pair.client_key,
            secret_name: pair.client_secret,
        }, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        return body, (("content-type", "application/json;charset=UTF-8"),)
    if (auth.broker in ("ls", "db") and auth.token_request_format == "form"
            and auth.scope == "oob"):
        fields = (
            ("grant_type", "client_credentials"),
            (key_name, pair.client_key),
            (secret_name, pair.client_secret),
            ("scope", auth.scope),
        )
    elif (auth.broker == "toss" and auth.token_request_format == "form" and auth.scope is None
            and (key_name, secret_name) == ("client_id", "client_secret")):
        # OpenAPI 1.2.28 OAuth2TokenRequest: exactly these three form fields.
        fields = (
            ("grant_type", "client_credentials"),
            (key_name, pair.client_key),
            (secret_name, pair.client_secret),
        )
    else:
        _reject(TransportFailure.EVIDENCE_MISSING)
    # A lone surrogate cannot be UTF-8 percent-encoded. The UnicodeEncodeError
    # would carry the whole secret in ``.object``, so it is replaced by a
    # static error raised outside the handler (no __context__ chain).
    try:
        body = urlencode(fields).encode("ascii")
    except UnicodeError:
        body = None
    if body is None:
        _reject(TransportFailure.INVALID_REQUEST)
    return body, (("content-type", "application/x-www-form-urlencoded"),)


# Toss keeps ONE valid token per client: issuing a new one invalidates the
# previous one at once (OpenAPI 1.2.28, /oauth2/token). Per-profile caches
# cannot see that, so this process records, per client id digest, the
# sequence of the most recent Toss token send that began writing. Only a
# lease from that send can be used for a Toss quote (ADR 0015). Another
# process using the same client is NOT visible.
_TOSS_TOKEN_WRITES: dict[bytes, int] = {}
# Toss quote writes in progress per client id digest. A quote claims its slot
# in the same critical section as its final latest-token check, and a Toss
# token send may not start writing while any slot is held, so no quote write
# can begin after a newer token write began (ChatGPT review of PR #30, M1).
_TOSS_QUOTE_WRITES: dict[bytes, int] = {}


def _toss_client(pair: CredentialPair) -> bytes:
    """Digest of the Toss client id; the id itself is never kept here."""
    # surrogatepass: never raises, so the id cannot leak through an exception.
    return hashlib.sha256(pair.client_key.encode("utf-8", "surrogatepass")).digest()


def _toss_token_write_is_latest(pair: CredentialPair, sequence: object) -> bool:
    """True only for the latest Toss token send to this client in the process."""
    if type(sequence) is not int:
        return False
    with _TOKEN_STATE_LOCK:
        return _TOSS_TOKEN_WRITES.get(_toss_client(pair)) == sequence


def _claim_toss_quote_write(client: bytes, sequence: object) -> bool:
    """Atomically re-check that ``sequence`` is still the latest Toss token send
    and register a quote write for ``client``. Release with
    ``_release_toss_quote_write``. No I/O happens under the lock."""
    if type(sequence) is not int:
        return False
    with _TOKEN_STATE_LOCK:
        if _TOSS_TOKEN_WRITES.get(client) != sequence:
            return False
        _TOSS_QUOTE_WRITES[client] = _TOSS_QUOTE_WRITES.get(client, 0) + 1
        return True


def _release_toss_quote_write(client: bytes) -> None:
    with _TOKEN_STATE_LOCK:
        remaining = _TOSS_QUOTE_WRITES.get(client, 0) - 1
        if remaining > 0:
            _TOSS_QUOTE_WRITES[client] = remaining
        else:
            _TOSS_QUOTE_WRITES.pop(client, None)


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
            expected_body, expected_headers = _token_wire(self.source, pair)
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


@dataclass(frozen=True, slots=True, repr=False, eq=False, weakref_slot=True)
class WireResponse:
    """Untrusted HTTP bytes, not authenticated quote/exchange provenance.

    Identity-compared on purpose: a response received by ``HttpsTransport``
    is attested by object identity (see ``_token_send_attestation``), so an
    equal-looking object built elsewhere never inherits that attestation.
    """

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
    """Candidate token POST from publisher evidence, no sending."""
    if type(identity) is not CredentialIdentity or type(provider) is not InMemoryCredentialProvider:
        _reject(TransportFailure.INVALID_REQUEST)
    _candidate_broker(identity)
    creds = provider.load(identity)
    provider.require_current(creds)
    auth = authentication_requirements(identity.broker, environment=identity.environment)
    # Never clone DB's unsafe URL credential testbed example or infer other
    # brokers' token body semantics: _token_wire fails closed for them.
    body, headers = _token_wire(auth, creds.pair)
    return WireRequest(
        auth, "POST", auth.token_origin, auth.token_path, (), headers, body, "token",
        credential_snapshot=creds,
    )


def build_quote_request(
    plan: QuoteRequestPlan, identity: CredentialIdentity,
    provider: InMemoryCredentialProvider, tokens: InMemoryTokenCache,
    *, now_ms: int,
) -> WireRequest:
    """Candidate HTTP quote request, never an attested broker or market adapter.

    A Toss quote needs the lease from the latest Toss token send to that
    client in this process; anything else, including a lease put into the
    cache by hand, fails ``TOKEN_UNAVAILABLE`` (ADR 0015).
    """
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
    if plan.broker == "toss" and not _toss_token_write_is_latest(
            credential.pair, lease.issue_sequence):
        _reject(TransportFailure.TOKEN_UNAVAILABLE)
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


@dataclass(frozen=True, slots=True)
class _TokenSendAttestation:
    """What the transport itself observed about one token send."""

    sequence: int  # process-wide order in which token sends started
    send_start_ms: int  # real clock read after TLS, immediately before the write


_TOKEN_STATE_LOCK = threading.Lock()
_TOKEN_SEQUENCE = itertools.count(1)
# (id(provider), identity), or ("toss", client digest) for Toss.
_TOKENS_IN_FLIGHT: set[tuple[object, object]] = set()
_TOKEN_ATTESTATIONS: "weakref.WeakKeyDictionary[WireResponse, _TokenSendAttestation]" = (
    weakref.WeakKeyDictionary()
)


def _token_send_attestation(response: object) -> _TokenSendAttestation | None:
    """The transport's record for a token response it received, else None.

    A ``WireResponse`` built anywhere else, including a field-for-field copy,
    has no record.
    """
    if type(response) is not WireResponse:
        return None
    with _TOKEN_STATE_LOCK:
        return _TOKEN_ATTESTATIONS.get(response)


def _error_diagnostic(response: object, request: WireRequest) -> GatewayStatus | None:
    """Redacted status envelope of an HTTP error body; the body is discarded."""
    try:
        body = response.read(MAX_RESPONSE_BYTES + 1)
    except Exception:
        return None
    if type(body) is not bytes or len(body) > MAX_RESPONSE_BYTES:
        return None
    pair = request.credential_snapshot.pair
    secrets = [pair.client_key, pair.client_secret]
    if request.bearer_lease is not None:
        secrets.append(request.bearer_lease.access_token)
    try:
        return gateway_status(body, redact=secrets)
    except Exception:
        return None


def _wall_clock_ms() -> int:
    """The only send-time clock. Tests may monkeypatch this module function;
    there is deliberately no constructor or per-call clock parameter, so a
    network-enabled sender cannot be handed a frozen or rolled-back time."""
    return time.time_ns() // 1_000_000


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
        if request.source.broker == "toss" and not _toss_token_write_is_latest(
                snapshot.pair, current_lease.issue_sequence):
            return TransportFailure.TOKEN_UNAVAILABLE
    return None


class HttpsTransport:
    """Zero-retry TLS-verified sender; disabled until explicitly opted in.

    Uses http.client directly: it does not read HTTP(S)_PROXY, copy environment
    credentials, follow redirects, keep a cookie jar or reuse connections.
    Never call with real keys without the maintainer's separate live approval.

    Token expiry is always checked against the real UTC clock, read before
    connecting and again after the TLS handshake. No caller-supplied clock is
    accepted (follow-up to the ChatGPT review of PR #24).

    At most one token request per provider and credential identity is in
    flight in this process (for Toss: per client id, across providers and
    profiles); a second concurrent one fails ``TOKEN_IN_FLIGHT`` before
    connecting. A received token response is attested with its send order
    and the clock reading taken just before the write. A Toss token send that
    starts writing retires every earlier Toss lease for that client in this
    process, even if the send then fails (ADR 0015). The final latest-token
    check of a Toss quote and the claim of its write are one atomic step, and
    a Toss token send fails ``QUOTE_IN_FLIGHT`` (nothing written) while a
    Toss quote for the same client is being written, so no quote write starts
    after a newer token write started. Nothing waits or retries.

    With ``collect_diagnostics=True`` (default off), an HTTP error response
    body is read within the usual bound only to extract a redacted status
    envelope into ``TransportError.diagnostic``; the body is then discarded.
    """

    __slots__ = ("_enabled", "_timeout_ms", "_diagnostics")

    def __init__(self, *, network_enabled: bool = False, timeout_ms: int = 5_000,
                 collect_diagnostics: bool = False):
        if (type(network_enabled) is not bool or type(timeout_ms) is not int
                or not 1 <= timeout_ms <= 60_000 or type(collect_diagnostics) is not bool):
            _reject(TransportFailure.INVALID_REQUEST)
        self._enabled = network_enabled
        self._timeout_ms = timeout_ms
        self._diagnostics = collect_diagnostics

    @staticmethod
    def _now_ms() -> int | None:
        try:
            value = _wall_clock_ms()  # looked up at call time
        except Exception:
            return None
        if type(value) is not int or value < 0:
            return None
        return value

    def __repr__(self) -> str:
        return "HttpsTransport(<redacted>)"

    def send(self, request: WireRequest) -> WireResponse:
        """One HTTPS attempt; no reconnect, refresh, retry, or downstream decode."""
        if type(request) is not WireRequest:
            _reject(TransportFailure.INVALID_REQUEST)
        # Defend against mutated/fabricated request objects, not hostile Python.
        request.__post_init__()
        if not self._enabled:
            _reject(TransportFailure.NOT_ENABLED)
        now_ms = self._now_ms()
        if now_ms is None:
            _reject(TransportFailure.INVALID_REQUEST)
        binding_failure = _binding_failure(request, now_ms)
        if binding_failure is not None:
            _reject(binding_failure)
        parsed = urlsplit(request.origin)
        target = request.path
        if request.query:
            target += "?" + urlencode(request.query)

        flight_key = None
        sequence = None
        toss_client = None
        quote_claimed = False
        toss_quote_client = None
        if request.purpose == "quote" and request.source.broker == "toss":
            toss_quote_client = _toss_client(request.credential_snapshot.pair)
        if request.purpose == "token":
            snapshot = request.credential_snapshot
            if request.source.broker == "toss":
                # One token per client on the Toss side: serialise on the
                # client itself, across providers and profiles.
                toss_client = _toss_client(snapshot.pair)
                key = ("toss", toss_client)
            else:
                key = (id(snapshot.owner), snapshot.identity)
            with _TOKEN_STATE_LOCK:
                if key not in _TOKENS_IN_FLIGHT:
                    _TOKENS_IN_FLIGHT.add(key)
                    flight_key = key
                    sequence = next(_TOKEN_SEQUENCE)
            if flight_key is None:
                _reject(TransportFailure.TOKEN_IN_FLIGHT)

        conn = None
        response_status: int | None = None
        response_body: bytes | None = None
        before_write_ms: int | None = None
        diagnostic: GatewayStatus | None = None
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
                before_write_ms = self._now_ms()
                if before_write_ms is None:
                    failure = TransportFailure.INVALID_REQUEST
                else:
                    failure = _binding_failure(request, before_write_ms)
            if failure is None and toss_client is not None:
                # From here Toss may issue a new token and invalidate the
                # previous one, whatever this send's outcome turns out to be.
                # Never start while a quote with the current token is writing.
                with _TOKEN_STATE_LOCK:
                    if _TOSS_QUOTE_WRITES.get(toss_client, 0) > 0:
                        failure = TransportFailure.QUOTE_IN_FLIGHT
                    else:
                        _TOSS_TOKEN_WRITES[toss_client] = sequence
            if failure is None and toss_quote_client is not None:
                if _claim_toss_quote_write(toss_quote_client,
                                           request.bearer_lease.issue_sequence):
                    quote_claimed = True
                else:
                    failure = TransportFailure.TOKEN_UNAVAILABLE
            if failure is None:
                state = DeliveryState.UNKNOWN  # any write failure may be partial
                try:
                    conn.request(
                        request.method, target, body=request.body,
                        headers=dict(request.headers),
                    )
                except Exception:
                    failure = TransportFailure.WRITE
                finally:
                    if quote_claimed:
                        quote_claimed = False
                        _release_toss_quote_write(toss_quote_client)

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
                    if failure is not None and self._diagnostics:
                        diagnostic = _error_diagnostic(response, request)

            if failure is None:
                try:
                    response_body = response.read(MAX_RESPONSE_BYTES + 1)
                    # read(amt) does not raise IncompleteRead when the peer
                    # closes before the declared Content-Length; http.client
                    # leaves the unread remainder in ``length`` (None when the
                    # body is chunked or close-delimited).
                    remaining = getattr(response, "length", None)
                    if type(response_body) is not bytes:
                        failure = TransportFailure.READ
                    elif len(response_body) > MAX_RESPONSE_BYTES:
                        failure = TransportFailure.OVERSIZED
                    elif remaining is not None and (type(remaining) is not int or remaining != 0):
                        failure = TransportFailure.READ
                except Exception:
                    failure = TransportFailure.READ
        finally:
            if quote_claimed:
                _release_toss_quote_write(toss_quote_client)
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    # close failure must never disguise the original send outcome
                    pass
            if flight_key is not None:
                with _TOKEN_STATE_LOCK:
                    _TOKENS_IN_FLIGHT.discard(flight_key)

        # Outside except handlers: prevent original URL/header/payload exceptions
        # from being retained by the public error via __context__.
        if failure is not None:
            raise TransportError(failure, state, diagnostic)
        assert response_status is not None and response_body is not None
        received = WireResponse(request, response_status, response_body)
        if sequence is not None:
            assert before_write_ms is not None
            with _TOKEN_STATE_LOCK:
                _TOKEN_ATTESTATIONS[received] = _TokenSendAttestation(sequence, before_write_ms)
        return received
