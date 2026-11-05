"""Private opt-in in-memory credential and bearer lease contracts.

Never read the environment, disk, OS keychain, accounts or device identifiers.
No token exchange happens here. This is not a public broker client.

Thread safety is limited to one process: the provider and cache serialise
their own operations with locks, and the cache checks credential currency and
writes a lease as one step. Nothing here coordinates across processes.
"""

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

from ktradelink._request_plan import authentication_requirements


class CredentialFailure(Enum):
    INVALID = "invalid_credential_contract"
    MISSING = "credential_not_supplied"
    STALE = "credential_revision_changed"
    TOKEN_MISSING = "token_not_supplied_or_expired"
    SUPERSEDED = "newer_token_already_cached"


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

    __slots__ = ("_entries", "_revision", "_lock")

    def __init__(self) -> None:
        self._entries: dict[CredentialIdentity, CredentialSnapshot] = {}
        self._revision = 0
        # Re-entrant: InMemoryTokenCache.put holds it across require_current().
        self._lock = threading.RLock()

    def put(self, identity: CredentialIdentity, pair: CredentialPair) -> CredentialSnapshot:
        if type(identity) is not CredentialIdentity or type(pair) is not CredentialPair:
            raise CredentialError(CredentialFailure.INVALID)
        with self._lock:
            self._revision += 1
            snapshot = CredentialSnapshot(identity, self._revision, pair, self)
            self._entries[identity] = snapshot
        return snapshot

    def load(self, identity: CredentialIdentity) -> CredentialSnapshot:
        if type(identity) is not CredentialIdentity:
            raise CredentialError(CredentialFailure.INVALID)
        with self._lock:
            snapshot = self._entries.get(identity)
        if snapshot is None:
            raise CredentialError(CredentialFailure.MISSING)
        return snapshot

    def require_current(self, snapshot: CredentialSnapshot) -> None:
        if type(snapshot) is not CredentialSnapshot or snapshot.owner is not self:
            raise CredentialError(CredentialFailure.STALE)
        with self._lock:
            current = self._entries.get(snapshot.identity)
        if current is not snapshot:
            raise CredentialError(CredentialFailure.STALE)

    def clear(self, identity: CredentialIdentity) -> None:
        if type(identity) is not CredentialIdentity:
            raise CredentialError(CredentialFailure.INVALID)
        with self._lock:
            self._entries.pop(identity, None)

    def __repr__(self) -> str:
        return "InMemoryCredentialProvider(<redacted>)"


@dataclass(frozen=True, slots=True, repr=False)
class BearerLease:
    """Sensitive in-memory token, never persisted or automatically refreshed."""

    snapshot: CredentialSnapshot = field(repr=False, compare=False)
    access_token: str = field(repr=False, compare=False)
    expires_at_ms: int
    # Process-wide order of the token send that produced this lease, attested
    # by the HTTPS transport. None for a lease the caller put in directly.
    issue_sequence: int | None = None

    def __post_init__(self) -> None:
        if type(self.snapshot) is not CredentialSnapshot:
            raise CredentialError(CredentialFailure.INVALID)
        if (type(self.access_token) is not str or not 1 <= len(self.access_token) <= 8192
                or any(char in self.access_token for char in "\r\n\x00")):
            raise CredentialError(CredentialFailure.INVALID)
        _nonnegative(self.expires_at_ms)
        if self.issue_sequence is not None and (
                type(self.issue_sequence) is not int or self.issue_sequence < 1):
            raise CredentialError(CredentialFailure.INVALID)

    def __repr__(self) -> str:
        return "BearerLease(<redacted>)"


class InMemoryTokenCache:
    """Strict broker/environment/profile/provider/revision binding; no refresh.

    A lease from a later attested token send is never replaced by one from an
    earlier send, so a slow, out-of-order exchange cannot reinstate an older
    token. Lock order is always provider, then cache.
    """

    __slots__ = ("_entries", "_lock")

    def __init__(self) -> None:
        self._entries: dict[tuple[InMemoryCredentialProvider, CredentialIdentity], BearerLease] = {}
        self._lock = threading.Lock()

    def put(
        self, provider: InMemoryCredentialProvider, snapshot: CredentialSnapshot,
        *, access_token: str, expires_at_ms: int, now_ms: int,
        issue_sequence: int | None = None,
    ) -> BearerLease:
        if type(provider) is not InMemoryCredentialProvider:
            raise CredentialError(CredentialFailure.INVALID)
        _nonnegative(now_ms)
        if type(expires_at_ms) is not int or expires_at_ms <= now_ms:
            raise CredentialError(CredentialFailure.INVALID)
        # Hold the provider lock so a rotation cannot land between the
        # currency check and the write.
        with provider._lock:
            provider.require_current(snapshot)
            lease = BearerLease(snapshot, access_token, expires_at_ms, issue_sequence)
            cache_key = (provider, snapshot.identity)
            with self._lock:
                existing = self._entries.get(cache_key)
                if (issue_sequence is not None and existing is not None
                        and existing.snapshot is snapshot
                        and existing.issue_sequence is not None
                        and existing.issue_sequence > issue_sequence):
                    raise CredentialError(CredentialFailure.SUPERSEDED)
                self._entries[cache_key] = lease
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
        with self._lock:
            lease = self._entries.get(cache_key)
            if lease is None:
                missing = True
            elif (lease.snapshot is not snapshot
                    or now_ms + min_remaining_ms >= lease.expires_at_ms):
                del self._entries[cache_key]  # same lock: this is the judged lease
                missing = True
            else:
                missing = False
        if missing:
            raise CredentialError(CredentialFailure.TOKEN_MISSING)
        return lease

    def revoke(self, provider: InMemoryCredentialProvider, identity: CredentialIdentity) -> None:
        if type(provider) is not InMemoryCredentialProvider or type(identity) is not CredentialIdentity:
            raise CredentialError(CredentialFailure.INVALID)
        with self._lock:
            self._entries.pop((provider, identity), None)

    def __repr__(self) -> str:
        return "InMemoryTokenCache(<redacted>)"
