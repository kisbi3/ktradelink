"""Private opt-in in-memory credential and bearer lease contracts.

Never read the environment, disk, OS keychain, accounts or device identifiers.
No token exchange happens here. This is not a public broker client.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

from ktradelink._request_plan import authentication_requirements


class CredentialFailure(Enum):
    INVALID = "invalid_credential_contract"
    MISSING = "credential_not_supplied"
    STALE = "credential_revision_changed"
    TOKEN_MISSING = "token_not_supplied_or_expired"


class CredentialError(RuntimeError):
    """Sanitised error, never incorporates credential or token values."""

    def __init__(self, kind: CredentialFailure):
        self.kind = kind
        super().__init__(kind.value)


def _nonnegative(value: int) -> None:
    if type(value) is not int or value < 0:
        raise CredentialError(CredentialFailure.INVALID)


@dataclass(frozen=True, slots=True)
class CredentialIdentity:
    broker: str
    environment: str
    profile: str  # Caller-chosen non-secret alias; not an account identifier.

    def __post_init__(self) -> None:
        if type(self.broker) is not str or type(self.environment) is not str:
            raise CredentialError(CredentialFailure.INVALID)
        if (type(self.profile) is not str or not 1 <= len(self.profile) <= 64
                or not self.profile.isascii() or not all(
                    char.isalnum() or char in "_-" for char in self.profile
                )):
            raise CredentialError(CredentialFailure.INVALID)
        try:
            authentication_requirements(self.broker, environment=self.environment)
        except (TypeError, ValueError):
            raise CredentialError(CredentialFailure.INVALID) from None


class CredentialPair:
    """Explicit caller-supplied secrets, never printed by library repr/str."""

    __slots__ = ("_client_key", "_client_secret")

    def __init__(self, client_key: str, client_secret: str):
        for value in (client_key, client_secret):
            if (type(value) is not str or not 1 <= len(value) <= 4096
                    or any(char in value for char in "\r\n\x00")):
                raise CredentialError(CredentialFailure.INVALID)
        self._client_key = client_key
        self._client_secret = client_secret

    @property
    def client_key(self) -> str:
        return self._client_key

    @property
    def client_secret(self) -> str:
        return self._client_secret

    def __repr__(self) -> str:
        return "CredentialPair(<redacted>)"

    __str__ = __repr__


@dataclass(frozen=True, slots=True, repr=False)
class CredentialSnapshot:
    """One provider-specific generation. Deliberately not a serialisable DTO."""

    identity: CredentialIdentity
    revision: int
    pair: CredentialPair = field(repr=False, compare=False)
    owner: object = field(repr=False, compare=False)

    def __repr__(self) -> str:
        return "CredentialSnapshot(<redacted>)"


class CredentialProvider(Protocol):
    def load(self, identity: CredentialIdentity) -> CredentialSnapshot: ...


class InMemoryCredentialProvider:
    """Instance-local store; callers opt in to supplying every secret explicitly."""

    __slots__ = ("_entries", "_revision")

    def __init__(self) -> None:
        self._entries: dict[CredentialIdentity, CredentialSnapshot] = {}
        self._revision = 0

    def put(self, identity: CredentialIdentity, pair: CredentialPair) -> CredentialSnapshot:
        if type(identity) is not CredentialIdentity or type(pair) is not CredentialPair:
            raise CredentialError(CredentialFailure.INVALID)
        self._revision += 1
        snapshot = CredentialSnapshot(identity, self._revision, pair, self)
        self._entries[identity] = snapshot
        return snapshot

    def load(self, identity: CredentialIdentity) -> CredentialSnapshot:
        if type(identity) is not CredentialIdentity:
            raise CredentialError(CredentialFailure.INVALID)
        snapshot = self._entries.get(identity)
        if snapshot is None:
            raise CredentialError(CredentialFailure.MISSING)
        return snapshot

    def require_current(self, snapshot: CredentialSnapshot) -> None:
        if type(snapshot) is not CredentialSnapshot or snapshot.owner is not self:
            raise CredentialError(CredentialFailure.STALE)
        if self._entries.get(snapshot.identity) is not snapshot:
            raise CredentialError(CredentialFailure.STALE)

    def clear(self, identity: CredentialIdentity) -> None:
        if type(identity) is not CredentialIdentity:
            raise CredentialError(CredentialFailure.INVALID)
        self._entries.pop(identity, None)

    def __repr__(self) -> str:
        return "InMemoryCredentialProvider(<redacted>)"


@dataclass(frozen=True, slots=True, repr=False)
class BearerLease:
    """Sensitive in-memory token, never persisted or automatically refreshed."""

    snapshot: CredentialSnapshot = field(repr=False, compare=False)
    access_token: str = field(repr=False, compare=False)
    expires_at_ms: int

    def __post_init__(self) -> None:
        if type(self.snapshot) is not CredentialSnapshot:
            raise CredentialError(CredentialFailure.INVALID)
        if (type(self.access_token) is not str or not 1 <= len(self.access_token) <= 8192
                or any(char in self.access_token for char in "\r\n\x00")):
            raise CredentialError(CredentialFailure.INVALID)
        _nonnegative(self.expires_at_ms)

    def __repr__(self) -> str:
        return "BearerLease(<redacted>)"


class InMemoryTokenCache:
    """Strict broker/environment/profile/provider/revision binding; no refresh."""

    __slots__ = ("_entries",)

    def __init__(self) -> None:
        self._entries: dict[tuple[InMemoryCredentialProvider, CredentialIdentity], BearerLease] = {}

    def put(
        self, provider: InMemoryCredentialProvider, snapshot: CredentialSnapshot,
        *, access_token: str, expires_at_ms: int, now_ms: int,
    ) -> BearerLease:
        if type(provider) is not InMemoryCredentialProvider:
            raise CredentialError(CredentialFailure.INVALID)
        provider.require_current(snapshot)
        _nonnegative(now_ms)
        if type(expires_at_ms) is not int or expires_at_ms <= now_ms:
            raise CredentialError(CredentialFailure.INVALID)
        lease = BearerLease(snapshot, access_token, expires_at_ms)
        self._entries[(provider, snapshot.identity)] = lease
        return lease

    def get(
        self, provider: InMemoryCredentialProvider, identity: CredentialIdentity,
        *, now_ms: int, min_remaining_ms: int = 0,
    ) -> BearerLease:
        if type(provider) is not InMemoryCredentialProvider:
            raise CredentialError(CredentialFailure.INVALID)
        _nonnegative(now_ms)
        _nonnegative(min_remaining_ms)
        snapshot = provider.load(identity)
        cache_key = (provider, identity)
        lease = self._entries.get(cache_key)
        if lease is None:
            raise CredentialError(CredentialFailure.TOKEN_MISSING)
        if lease.snapshot is not snapshot or now_ms + min_remaining_ms >= lease.expires_at_ms:
            self._entries.pop(cache_key, None)
            raise CredentialError(CredentialFailure.TOKEN_MISSING)
        return lease

    def revoke(self, provider: InMemoryCredentialProvider, identity: CredentialIdentity) -> None:
        if type(provider) is not InMemoryCredentialProvider or type(identity) is not CredentialIdentity:
            raise CredentialError(CredentialFailure.INVALID)
        self._entries.pop((provider, identity), None)

    def __repr__(self) -> str:
        return "InMemoryTokenCache(<redacted>)"
