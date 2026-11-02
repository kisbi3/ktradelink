"""Private in-memory auth/transport rehearsal, NEVER a live broker client.

Only synthetic identity slots and leases are accepted. No credential values,
OAuth, HTTP, files, environment lookup, MAC discovery or automatic retries.
Fixture context and outcome are NOT evidence of actual market provenance.
"""

from dataclasses import dataclass, field
from enum import Enum

from ktradelink._request_plan import (
    QuoteRequestPlan,
    authentication_requirements,
    decode_offline_quote_response,
    plan_ticker_request,
)
from ktradelink.models import Ticker

MAX_BODY_BYTES = 1_048_576  # Library-owned limit, not a provider limit.


class FailureKind(Enum):
    INVALID_INPUT = "invalid_offline_input"
    CREDENTIAL_UNAVAILABLE = "fake_credential_unavailable"
    CONTEXT_MISMATCH = "fake_response_context_mismatch"
    SCRIPT_EXHAUSTED = "fake_transport_script_exhausted"
    TIMEOUT = "simulated_timeout"
    REDIRECT = "redirect_refused"
    UNAUTHORIZED = "http_unauthorized"
    FORBIDDEN = "http_forbidden"
    RATE_LIMITED = "http_rate_limited"
    SERVER = "http_server_error"
    HTTP = "http_response_rejected"
    PROVIDER_UNVERIFIED = "fixture_outcome_not_success"
    DECODER = "offline_decoder_rejected"
    NATIVE_UNAVAILABLE = "native_decoder_unavailable"


class OfflineSessionError(RuntimeError):
    """Static classification only; no payload or arbitrary exception text."""

    def __init__(self, kind: FailureKind) -> None:
        self.kind = kind if type(kind) is FailureKind else FailureKind.INVALID_INPUT
        super().__init__(self.kind.value)


def _integer(value: int, *, positive: bool = False) -> None:
    if type(value) is not int or value < int(positive):
        raise OfflineSessionError(FailureKind.INVALID_INPUT)


def _plan(plan: QuoteRequestPlan) -> None:
    if type(plan) is not QuoteRequestPlan:
        raise OfflineSessionError(FailureKind.INVALID_INPUT)
    try:
        expected = plan_ticker_request(
            plan.broker, plan.symbol, venue=plan.venue, environment=plan.environment
        )
    except (TypeError, ValueError):
        raise OfflineSessionError(FailureKind.INVALID_INPUT) from None
    if plan != expected:
        raise OfflineSessionError(FailureKind.CONTEXT_MISMATCH)


@dataclass(frozen=True, slots=True)
class CredentialScope:
    """Integer identity_slot is a fixture label, NEVER an account or app key."""

    broker: str
    environment: str
    identity_slot: int

    def __post_init__(self) -> None:
        _integer(self.identity_slot)
        if type(self.broker) is not str or type(self.environment) is not str:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        try:
            authentication_requirements(self.broker, environment=self.environment)
        except (TypeError, ValueError):
            raise OfflineSessionError(FailureKind.INVALID_INPUT) from None


@dataclass(frozen=True, slots=True)
class FakeLease:
    """Not a bearer token: object identity binds a fixture to one issuance."""

    scope: CredentialScope = field(repr=False)
    generation: int
    issued_at_ms: int
    expires_at_ms: int

    def __post_init__(self) -> None:
        if type(self.scope) is not CredentialScope:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        _integer(self.generation, positive=True)
        _integer(self.issued_at_ms)
        _integer(self.expires_at_ms, positive=True)
        if self.expires_at_ms <= self.issued_at_ms:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)


class FakeCredentialProvider:
    """Instance-local synthetic cache. Explicit issue/revoke; no refresh or IO."""

    __slots__ = ("_leases", "_generation")

    def __init__(self) -> None:
        self._leases: dict[CredentialScope, FakeLease] = {}
        self._generation = 0

    def issue(self, scope: CredentialScope, *, now_ms: int, lifetime_ms: int) -> FakeLease:
        if type(scope) is not CredentialScope:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        _integer(now_ms)
        _integer(lifetime_ms, positive=True)
        self._generation += 1
        lease = FakeLease(scope, self._generation, now_ms, now_ms + lifetime_ms)
        self._leases[scope] = lease
        return lease

    def get(self, scope: CredentialScope, *, now_ms: int) -> FakeLease:
        if type(scope) is not CredentialScope:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        _integer(now_ms)
        lease = self._leases.get(scope)
        if lease is not None and now_ms >= lease.expires_at_ms:
            del self._leases[scope]
        elif lease is not None and lease.issued_at_ms <= now_ms:
            return lease
        raise OfflineSessionError(FailureKind.CREDENTIAL_UNAVAILABLE)

    def revoke(self, scope: CredentialScope) -> None:
        if type(scope) is not CredentialScope:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        self._leases.pop(scope, None)


@dataclass(frozen=True, slots=True)
class TransportPolicy:
    """Simulated deadline only. Flags constrain design, not real TLS or IO."""

    timeout_ms: int = 5_000
    verify_tls: bool = True
    follow_redirects: bool = False
    retries: int = 0

    def __post_init__(self) -> None:
        _integer(self.timeout_ms, positive=True)
        if (self.timeout_ms > 60_000 or self.verify_tls is not True
                or self.follow_redirects is not False
                or type(self.retries) is not int or self.retries != 0):
            raise OfflineSessionError(FailureKind.INVALID_INPUT)


_DEFAULT_POLICY = TransportPolicy()


class FixtureOutcome(Enum):
    """Test author's assertion, NOT a parsed provider status or live attestation."""

    UNVERIFIED = "unverified"
    SUCCESS = "synthetic_success"
    ERROR = "synthetic_error"


@dataclass(frozen=True, slots=True)
class FakeResponse:
    request: QuoteRequestPlan = field(repr=False)
    lease: FakeLease = field(repr=False)
    http_status: int
    json_text: str = field(repr=False)
    outcome: FixtureOutcome = FixtureOutcome.UNVERIFIED
    elapsed_ms: int = 0

    def __post_init__(self) -> None:
        _plan(self.request)
        if type(self.lease) is not FakeLease or type(self.outcome) is not FixtureOutcome:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        if type(self.http_status) is not int or not 100 <= self.http_status <= 599:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        _integer(self.elapsed_ms)
        if type(self.json_text) is not str or len(self.json_text) > MAX_BODY_BYTES:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        try:
            size = len(self.json_text.encode("utf-8"))
        except UnicodeEncodeError:
            raise OfflineSessionError(FailureKind.INVALID_INPUT) from None
        if size > MAX_BODY_BYTES:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)


class FakeTransport:
    """Consume scripted responses exactly once; never send, sleep or retry."""

    __slots__ = ("_responses", "_calls")

    def __init__(self, responses: tuple[FakeResponse, ...]) -> None:
        if type(responses) is not tuple or any(type(r) is not FakeResponse for r in responses):
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        self._responses = responses
        self._calls = 0

    @property
    def calls(self) -> int:
        return self._calls

    def exchange(self, plan: QuoteRequestPlan, lease: FakeLease) -> FakeResponse:
        _plan(plan)
        if type(lease) is not FakeLease:
            raise OfflineSessionError(FailureKind.INVALID_INPUT)
        index = self._calls
        self._calls += 1
        if index >= len(self._responses):
            raise OfflineSessionError(FailureKind.SCRIPT_EXHAUSTED)
        response = self._responses[index]
        if response.request != plan or response.lease is not lease:
            raise OfflineSessionError(FailureKind.CONTEXT_MISMATCH)
        return response


def _http_failure(status: int) -> FailureKind | None:
    if 200 <= status < 300:
        return None
    if 300 <= status < 400:
        return FailureKind.REDIRECT
    if status in (401, 403, 429):
        return {401: FailureKind.UNAUTHORIZED, 403: FailureKind.FORBIDDEN,
                429: FailureKind.RATE_LIMITED}[status]
    return FailureKind.SERVER if 500 <= status <= 599 else FailureKind.HTTP


def execute_offline_quote(
    plan: QuoteRequestPlan, scope: CredentialScope,
    provider: FakeCredentialProvider, transport: FakeTransport, *, now_ms: int,
    policy: TransportPolicy = _DEFAULT_POLICY,
) -> Ticker:
    """Rehearse one synthetic request; never a public fetch_ticker implementation."""
    if (type(provider) is not FakeCredentialProvider or type(transport) is not FakeTransport
            or type(scope) is not CredentialScope or type(policy) is not TransportPolicy):
        raise OfflineSessionError(FailureKind.INVALID_INPUT)
    _plan(plan)
    if (scope.broker, scope.environment) != (plan.broker, plan.environment):
        raise OfflineSessionError(FailureKind.CONTEXT_MISMATCH)
    lease = provider.get(scope, now_ms=now_ms)
    response = transport.exchange(plan, lease)
    if response.elapsed_ms >= policy.timeout_ms:
        raise OfflineSessionError(FailureKind.TIMEOUT)
    failure = _http_failure(response.http_status)
    if failure is not None:
        if failure is FailureKind.UNAUTHORIZED:
            provider.revoke(scope)
        raise OfflineSessionError(failure)
    provider.get(scope, now_ms=now_ms + response.elapsed_ms)
    if response.outcome is not FixtureOutcome.SUCCESS:
        raise OfflineSessionError(FailureKind.PROVIDER_UNVERIFIED)
    try:
        return decode_offline_quote_response(
            plan, http_status=response.http_status, json_text=response.json_text
        )
    except ImportError:
        raise OfflineSessionError(FailureKind.NATIVE_UNAVAILABLE) from None
    except (TypeError, ValueError, RuntimeError):
        raise OfflineSessionError(FailureKind.DECODER) from None
