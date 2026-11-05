"""Experimental public ``fetch_ticker`` surface (ADR 0013); not verified live.

This module only composes the existing private pieces:

    request planner -> in-memory credential provider and token cache
    -> HttpsTransport token send -> save_example_token_response
    -> HttpsTransport quote send -> root status check -> native decoder -> Ticker

Nothing is sent unless the caller created the client with
``allow_network=True`` and ``accept_unverified=True``. Each ``fetch_ticker``
call sends at most one token request and at most one quote request. Nothing
is retried or refreshed in the background. Errors carry static reasons only
(see ``ktradelink.errors``).
"""

import json
import re
import threading
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import timezone
from decimal import Decimal

from ktradelink import _https_transport as _transport
from ktradelink._credential_runtime import (
    CredentialError,
    CredentialFailure,
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._https_transport import (
    HttpsTransport,
    TransportFailure,
    build_quote_request,
    build_token_request,
)
from ktradelink._request_plan import (
    authentication_requirements,
    decode_offline_quote_response,
    plan_ticker_request,
)
from ktradelink._token_codec import TokenError, TokenFailure, save_example_token_response
from ktradelink.errors import (
    AuthenticationError,
    BrokerRejected,
    BrokerUnavailable,
    ClientClosed,
    DeliveryState,
    InvalidParameter,
    InvalidSymbol,
    InvalidVenue,
    KTradeLinkError,
    NetworkDisabled,
    PermissionDenied,
    RateLimitExceeded,
    ResponseSchemaError,
    TransportError,
    UnsupportedCapability,
)
from ktradelink.models import Ticker

KNOWN_BROKERS = ("kis", "kiwoom", "ls", "db", "toss", "meritz")
ENVIRONMENTS = ("live", "paper")
DOCUMENTED_CANDIDATE = "documented_candidate"
UNSUPPORTED = "unsupported"
# Library policy, not publisher evidence: a cached token with this little
# lifetime left is not reused, so it does not expire while a quote is in flight.
TOKEN_REUSE_MARGIN_MS = 60_000
_PROFILE_ALIAS = "public"
_SPEC_VENUES = ("KRX", "NXT", "BROKER_COMPOSITE")
_DECODER_DETAIL = re.compile(r"[A-Za-z0-9_.]{1,64}: [A-Za-z]{1,32}")


@dataclass(frozen=True, slots=True)
class _FetchTickerProfile:
    status_field: str  # root quote status field that MUST be present
    status_ok: str | int  # its only accepted value (and exact JSON type)
    preflight: str  # synthetic payload decoded before anything is sent


# Brokers whose public fetch_ticker is enabled. Adding one is a reviewed
# one-entry change here; its token/quote wire must already be enabled in
# _https_transport. Requiring the root status is library policy: the native
# decoders accept a missing status for synthetic examples (ADR 0008), but a
# missing upstream status is never treated as success on this public path.
_FETCH_TICKER = {
    "kis": _FetchTickerProfile(
        "rt_cd", "0", '{"rt_cd":"0","output":{"stck_prpr":"72000","acml_vol":"0"}}'),
    "kiwoom": _FetchTickerProfile(
        "return_code", 0,
        '{"return_code":0,"stk_cd":"005930","cur_prc":"72000","trde_qty":"0"}'),
    "ls": _FetchTickerProfile(
        "rsp_cd", "00000",
        '{"rsp_cd":"00000","t1102OutBlock":{"shcode":"005930","price":72000,"volume":0}}'),
}

_DELIVERY = {
    _transport.DeliveryState.NOT_SENT: DeliveryState.NOT_SENT,
    _transport.DeliveryState.UNKNOWN: DeliveryState.UNKNOWN,
    _transport.DeliveryState.RESPONSE_RECEIVED: DeliveryState.RESPONSE_RECEIVED,
}
_TRANSPORT_CLASSES: dict[TransportFailure, type[KTradeLinkError]] = {
    TransportFailure.UNAUTHORIZED: AuthenticationError,
    TransportFailure.FORBIDDEN: PermissionDenied,
    TransportFailure.RATE_LIMITED: RateLimitExceeded,
    TransportFailure.SERVER: BrokerUnavailable,
    TransportFailure.NOT_ENABLED: NetworkDisabled,
    TransportFailure.EVIDENCE_MISSING: UnsupportedCapability,
    # Only close() changes this client's credentials.
    TransportFailure.STALE_CREDENTIAL: ClientClosed,
}


@dataclass(frozen=True, slots=True)
class Capability:
    """Honest per-environment state of one method. Nothing is ``supported``.

    ``documented_candidate`` means: implemented from publisher documentation
    and examples, tested offline only, never verified against a live or paper
    gateway (spec section 7).
    """

    broker: str
    method: str
    environment: str
    venue: str
    state: str
    reason: str


def _capability(broker: str, environment: str) -> Capability:
    try:
        authentication_requirements(broker, environment=environment)
        documented = True
    except (TypeError, ValueError):
        documented = False
    if not documented:
        state, reason = UNSUPPORTED, "environment_not_documented"
    elif broker not in _FETCH_TICKER:
        state, reason = UNSUPPORTED, "no_reviewed_token_and_quote_route"
    else:
        state, reason = DOCUMENTED_CANDIDATE, "publisher_documented_not_gateway_verified"
    return Capability(broker, "fetch_ticker", environment, "KRX", state, reason)


def capabilities(broker: str) -> tuple[Capability, ...]:
    """``fetch_ticker`` state for ``broker`` per environment (KRX only).

    Anything not listed (other methods, NXT, BROKER_COMPOSITE) is unsupported.
    """
    if type(broker) is not str or broker not in KNOWN_BROKERS:
        raise InvalidParameter("unknown_broker")
    return tuple(_capability(broker, environment) for environment in ENVIRONMENTS)


class Credentials:
    """App key and secret, supplied explicitly by the caller.

    The library never reads them from the environment, files or a keychain.
    ``repr``/``str`` are redacted and the object cannot be pickled or copied.
    Python memory stays introspectable: do not dump private attributes.
    """

    __slots__ = ("_pair",)

    def __init__(self, app_key: str, app_secret: str):
        try:
            pair = CredentialPair(app_key, app_secret)
        except CredentialError:
            pair = None
        if pair is None:  # raised outside the handler: no chained context
            raise InvalidParameter("invalid_credentials")
        self._pair = pair

    def __repr__(self) -> str:
        return "Credentials(<redacted>)"

    __str__ = __repr__

    def __reduce_ex__(self, protocol):
        raise TypeError("Credentials cannot be pickled or copied")


def _now_ms(stage: str, delivery: DeliveryState = DeliveryState.NOT_SENT) -> int:
    """The transport's real UTC clock, so tests patch a single function.

    A failure is reported for the request named by ``stage``: ``NOT_SENT``
    only before that request is written, ``RESPONSE_RECEIVED`` after its
    response arrived (a token may already have been issued).
    """
    try:
        value = _transport._wall_clock_ms()
    except Exception:
        value = None
    if type(value) is not int or value < 0:
        raise TransportError("clock_unavailable", delivery=delivery, stage=stage)
    return value


def _check_symbol(symbol: object) -> None:
    if (type(symbol) is not str or len(symbol) != 6 or not symbol.isascii()
            or not symbol.isdigit()):
        raise InvalidSymbol("symbol_must_be_six_ascii_digits")


def _check_venue(venue: object) -> None:
    if type(venue) is not str or venue not in _SPEC_VENUES:
        raise InvalidVenue("unknown_venue")
    if venue != "KRX":
        raise UnsupportedCapability("venue_not_supported")


def _check_params(params: object) -> None:
    if params is None:
        return
    if not isinstance(params, Mapping):
        raise InvalidParameter("params_must_be_a_mapping")
    if len(params) != 0:
        raise InvalidParameter("params_not_supported")


def _from_transport(error: _transport.TransportError, stage: str) -> KTradeLinkError:
    cls = _TRANSPORT_CLASSES.get(error.kind, TransportError)
    return cls(error.kind.value, delivery=_DELIVERY[error.delivery], stage=stage)


def _from_credential(error: CredentialError, stage: str) -> KTradeLinkError:
    if error.kind in (CredentialFailure.MISSING, CredentialFailure.STALE):
        return ClientClosed("client_closed", stage=stage)
    return TransportError(error.kind.value, stage=stage)


def _from_token(error: TokenError) -> KTradeLinkError:
    received = DeliveryState.RESPONSE_RECEIVED
    if error.kind is TokenFailure.STALE_CREDENTIAL:
        return ClientClosed("client_closed", delivery=received, stage="token")
    if error.kind is TokenFailure.EVIDENCE_MISSING:
        return InvalidParameter(error.kind.value, delivery=received, stage="token")
    return ResponseSchemaError(error.kind.value, delivery=received, stage="token")


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    values: dict = {}
    for key, value in pairs:
        if key in values:
            raise ValueError("duplicate JSON field")
        values[key] = value
    return values


def _no_constant(_value: str) -> None:
    raise ValueError("non-finite JSON number")


def _status_failure(profile: _FetchTickerProfile, text: str) -> KTradeLinkError | None:
    """Root status presence and value only; the native decoder checks the rest."""
    try:
        root = json.loads(text, object_pairs_hook=_no_duplicate_keys,
                          parse_constant=_no_constant)
    except (ValueError, TypeError, RecursionError):
        root = None
        malformed = True
    else:
        malformed = False
    received = DeliveryState.RESPONSE_RECEIVED
    if malformed or type(root) is not dict:
        return ResponseSchemaError("quote_response_not_a_json_object",
                                   delivery=received, stage="quote")
    if profile.status_field not in root:
        return ResponseSchemaError("quote_status_missing", delivery=received, stage="quote")
    value = root[profile.status_field]
    if type(value) is not type(profile.status_ok):  # includes an explicit null
        return ResponseSchemaError("quote_status_invalid", delivery=received, stage="quote")
    if value != profile.status_ok:
        return BrokerRejected("quote_status_not_success", delivery=received, stage="quote")
    return None


def _decoder_preflight(broker: str) -> bool:
    """Decode a synthetic payload with the installed native module.

    A version check alone can pass an old or partial build (ADR 0012).
    """
    try:
        from ktradelink._native import decode_ticker_candidate

        ticker = decode_ticker_candidate(broker, "005930", "KRX", _FETCH_TICKER[broker].preflight)
        # Provenance too: a build that mislabels symbol or venue must fail
        # here, before any token is requested (ChatGPT review of PR #28, M2).
        return (type(ticker) is Ticker and ticker.broker == broker
                and ticker.symbol == "005930" and ticker.venue == "KRX"
                and ticker.last == Decimal("72000") and ticker.volume == 0)
    except Exception:
        return False


_CONSTRUCT = object()


class BrokerClient:
    """One broker, one environment, one set of credentials. Use ``connect()``.

    Experimental: the capability is ``documented_candidate`` only. Thread
    safe within one process. Not coordinated across processes: two clients or
    processes using the same app key can invalidate each other's tokens.
    """

    __slots__ = ("_broker", "_environment", "_identity", "_provider", "_cache",
                 "_transport", "_network", "_kis_tz", "_token_lock", "_state_lock",
                 "_closed", "_decoder_ready")

    def __init__(self, key: object, broker: str, environment: str, pair: CredentialPair,
                 *, allow_network: bool, timeout_ms: int,
                 kis_expiry_timezone: timezone | None):
        if key is not _CONSTRUCT:
            raise TypeError("create clients with ktradelink.connect()")
        self._broker = broker
        self._environment = environment
        self._identity = CredentialIdentity(broker, environment, _PROFILE_ALIAS)
        self._provider = InMemoryCredentialProvider()
        self._provider.put(self._identity, pair)
        self._cache = InMemoryTokenCache()
        self._transport = HttpsTransport(network_enabled=allow_network, timeout_ms=timeout_ms)
        self._network = allow_network
        self._kis_tz = kis_expiry_timezone
        self._token_lock = threading.Lock()
        self._state_lock = threading.Lock()
        self._closed = False
        self._decoder_ready = False

    @property
    def broker(self) -> str:
        return self._broker

    @property
    def environment(self) -> str:
        return self._environment

    @property
    def network_enabled(self) -> bool:
        return self._network

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def capabilities(self) -> tuple[Capability, ...]:
        return (_capability(self._broker, self._environment),)

    def __repr__(self) -> str:
        network = "enabled" if self._network else "disabled"
        state = ", closed" if self._closed else ""
        return (f"BrokerClient(broker={self._broker!r}, environment={self._environment!r}, "
                f"network={network}{state})")

    __str__ = __repr__

    def __reduce_ex__(self, protocol):
        raise TypeError("BrokerClient cannot be pickled or copied")

    def __enter__(self) -> "BrokerClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def close(self) -> None:
        """Drop the credentials and any cached token from this client.

        This removes references only; Python cannot erase strings from memory.
        A token already issued stays valid at the broker until it expires.
        """
        with self._state_lock:
            if self._closed:
                return
            self._closed = True
            self._cache.revoke(self._provider, self._identity)
            self._provider.clear(self._identity)

    def fetch_ticker(self, symbol: str, *, venue: str = "KRX",
                     params: Mapping[str, object] | None = None) -> Ticker:
        """Current quote for one six-digit KRX stock code, as a ``Ticker``.

        Sends at most one token request (only when no reusable token is
        cached) and one quote request. Never retries. ``params`` must be
        ``None`` or empty. ``retrieved_at``/``timestamp`` are ``None``.
        """
        _check_symbol(symbol)
        _check_venue(venue)
        _check_params(params)
        if self._closed:
            raise ClientClosed("client_closed")
        if not self._network:
            raise NetworkDisabled("network_not_enabled")
        if not self._decoder_ready:
            if not _decoder_preflight(self._broker):
                raise UnsupportedCapability("native_decoder_unavailable")
            self._decoder_ready = True
        plan = plan_ticker_request(self._broker, symbol, venue=venue,
                                   environment=self._environment)
        self._ensure_token()
        return self._fetch_quote(plan)

    def _reusable_token(self) -> bool:
        now = _now_ms("token")
        try:
            lease = self._cache.get(self._provider, self._identity, now_ms=now)
        except CredentialError:
            return False
        return lease.expires_at_ms - now > TOKEN_REUSE_MARGIN_MS

    def _ensure_token(self) -> None:
        if self._reusable_token():
            return
        # Never wait for another thread's token request and then send our own:
        # that would repeat a possibly delivered request. Fail fast instead.
        if not self._token_lock.acquire(blocking=False):
            raise TransportError("token_request_in_flight", stage="token")
        try:
            if not self._reusable_token():
                self._issue_token()
        finally:
            self._token_lock.release()

    def _issue_token(self) -> None:
        failure: KTradeLinkError | None = None
        try:
            request = build_token_request(self._identity, self._provider)
        except CredentialError as error:
            failure = _from_credential(error, "token")
        except _transport.TransportError as error:
            failure = _from_transport(error, "token")
        if failure is not None:
            raise failure
        try:
            response = self._transport.send(request)
        except _transport.TransportError as error:
            failure = _from_transport(error, "token")
        if failure is not None:
            raise failure
        # The token response has arrived: a clock failure here must not claim
        # the token request was never sent (ChatGPT review of PR #28, M1).
        now = _now_ms("token", DeliveryState.RESPONSE_RECEIVED)
        try:
            save_example_token_response(
                response, self._identity, self._provider, self._cache, now_ms=now,
                kis_expiry_timezone=self._kis_tz)
        except TokenError as error:
            failure = _from_token(error)
        if failure is not None:
            raise failure

    def _drop_token(self, rejected: object) -> None:
        """After a quote 401, stop reusing exactly that token (no re-send)."""
        try:
            current = self._cache.get(self._provider, self._identity,
                                      now_ms=_now_ms("quote", DeliveryState.RESPONSE_RECEIVED))
        except (CredentialError, KTradeLinkError):
            return
        if current is rejected:
            self._cache.revoke(self._provider, self._identity)

    def _fetch_quote(self, plan) -> Ticker:
        failure: KTradeLinkError | None = None
        now = _now_ms("quote")
        try:
            request = build_quote_request(plan, self._identity, self._provider, self._cache,
                                          now_ms=now)
        except CredentialError as error:
            if error.kind is CredentialFailure.TOKEN_MISSING:
                failure = TransportError(error.kind.value, stage="quote")
            else:
                failure = _from_credential(error, "quote")
        except _transport.TransportError as error:
            failure = _from_transport(error, "quote")
        if failure is not None:
            raise failure
        unauthorized = False
        try:
            response = self._transport.send(request)
        except _transport.TransportError as error:
            failure = _from_transport(error, "quote")
            unauthorized = error.kind is TransportFailure.UNAUTHORIZED
        if failure is not None:
            if unauthorized:
                self._drop_token(request.bearer_lease)
            raise failure
        return self._decode(plan, request, response)

    def _decode(self, plan, request, response) -> Ticker:
        received = DeliveryState.RESPONSE_RECEIVED
        if response.request is not request or response.status != 200:
            raise ResponseSchemaError("quote_response_unbound", delivery=received, stage="quote")
        try:
            text = response.json_text
        except _transport.TransportError:
            text = None
        if text is None:
            raise ResponseSchemaError("quote_response_not_utf8", delivery=received,
                                      stage="quote")
        failure = _status_failure(_FETCH_TICKER[self._broker], text)
        if failure is not None:
            raise failure
        ticker = None
        detail = None
        try:
            ticker = decode_offline_quote_response(plan, http_status=response.status,
                                                   json_text=text)
        except Exception as error:
            # The Rust decoder's ValueError text is a static "<field>: <Kind>".
            message = str(error) if type(error) is ValueError else ""
            detail = message if _DECODER_DETAIL.fullmatch(message) else None
        if ticker is None:
            raise ResponseSchemaError("quote_rejected_by_decoder", delivery=received,
                                      stage="quote", detail=detail)
        if (type(ticker) is not Ticker or ticker.symbol != plan.symbol
                or ticker.venue != "KRX" or ticker.broker != self._broker):
            raise ResponseSchemaError("quote_provenance_mismatch", delivery=received,
                                      stage="quote")
        return ticker


def connect(
    broker: str, *, environment: str, credentials: Credentials,
    allow_network: bool = False, accept_unverified: bool = False,
    kis_expiry_timezone: timezone | None = None, timeout_ms: int = 5_000,
) -> BrokerClient:
    """Create an experimental client. Nothing is sent by this call.

    - ``environment`` is required (``"live"`` or ``"paper"``); there is no
      fallback between them.
    - ``allow_network=True`` is required before ``fetch_ticker`` sends
      anything, and then ``accept_unverified=True`` must acknowledge that the
      capability is only ``documented_candidate``.
    - KIS requires ``kis_expiry_timezone`` (a ``datetime.timezone``): the KIS
      token expiry is a naive timestamp whose time zone the publisher sample
      does not confirm. Other brokers reject it.
    - ``timeout_ms`` is a per-socket-operation timeout (1-60000), not a
      deadline for the whole call.
    """
    if type(broker) is not str or broker not in KNOWN_BROKERS:
        raise InvalidParameter("unknown_broker")
    if type(environment) is not str or environment not in ENVIRONMENTS:
        raise InvalidParameter("unknown_environment")
    if _capability(broker, environment).state != DOCUMENTED_CANDIDATE:
        raise UnsupportedCapability("broker_or_environment_not_enabled")
    if type(credentials) is not Credentials:
        raise InvalidParameter("credentials_required")
    if type(allow_network) is not bool or type(accept_unverified) is not bool:
        raise InvalidParameter("flags_must_be_bool")
    if allow_network and not accept_unverified:
        raise UnsupportedCapability("unverified_capability_not_acknowledged")
    if type(timeout_ms) is not int or not 1 <= timeout_ms <= 60_000:
        raise InvalidParameter("invalid_timeout_ms")
    if broker == "kis":
        if kis_expiry_timezone is None:
            raise InvalidParameter("kis_expiry_timezone_required")
        if type(kis_expiry_timezone) is not timezone:
            raise InvalidParameter("kis_expiry_timezone_must_be_datetime_timezone")
    elif kis_expiry_timezone is not None:
        raise InvalidParameter("kis_expiry_timezone_only_for_kis")
    return BrokerClient(
        _CONSTRUCT, broker, environment, credentials._pair, allow_network=allow_network,
        timeout_ms=timeout_ms, kis_expiry_timezone=kis_expiry_timezone,
    )
