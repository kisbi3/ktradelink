"""Private KIS/Kiwoom/LS/DB publisher-evidence token parsing, without network I/O.

No automatic token issuance or refresh, and no unsupported broker extrapolation.
Errors never reflect the upstream body. Parser success is NOT live validation.
"""

import hashlib
import json
import threading
from datetime import datetime, timedelta, timezone
from enum import Enum

from ktradelink._credential_runtime import (
    BearerLease,
    CredentialError,
    CredentialFailure,
    CredentialIdentity,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._https_transport import (
    MAX_RESPONSE_BYTES,
    TransportError,
    WireRequest,
    WireResponse,
    _token_send_attestation,
)
from ktradelink._request_plan import AuthRequirements

KST = timezone(timedelta(hours=9))
# Library sanity bound, NOT a publisher limit: the LS example shows 86400 s.
MAX_RELATIVE_LIFETIME_S = 7 * 24 * 60 * 60
# DB API guide token detail: valid for 24 hours from issue (개인/법인).
DB_MAX_LIFETIME_S = 24 * 60 * 60
# DB token response keys: the API guide example (`access_token`, `scope`,
# `token_type`, `expires_in`). The guide's field table names differ
# (`token`, `expire_in`); the example, the SDK and the testbed agree on these.
_DB_TOKEN_KEYS = frozenset(("access_token", "scope", "token_type", "expires_in"))
# The API guide example returns "oob" (the requested scope); the testbed
# example returns "login". Both are publisher-shown; no other value is.
_DB_TOKEN_SCOPES = ("oob", "login")


class TokenFailure(Enum):
    INVALID_RESPONSE = "token_response_invalid_or_unverified"
    EVIDENCE_MISSING = "token_expiry_timezone_not_supplied"
    STALE_CREDENTIAL = "credentials_changed_during_token_exchange"
    UNATTESTED = "token_response_not_received_by_transport"
    SUPERSEDED = "newer_token_already_cached"
    UNACKNOWLEDGED = "caller_acknowledgement_not_supplied"
    REISSUED = "token_reissued_with_unverifiable_expiry"


# DB re-issues the SAME token, with its ORIGINAL expiry, when a token is
# requested before the previous one expired, and the response cannot say which
# happened. Every DB token this process has received is remembered by digest
# (never the token itself) with the send that produced it, so a token returned
# again by a later send is recognised as re-issued (ADR 0015). Entries are
# dropped once their expiry is before a later send's attested start.
_DB_ISSUE_LOCK = threading.Lock()
_DB_ISSUED: dict[bytes, tuple[int, int]] = {}  # digest -> (send sequence, expires_at_ms)


def _db_reissued(access: str, sequence: int, send_start_ms: int, expires_at_ms: int) -> bool:
    digest = hashlib.sha256(access.encode("utf-8")).digest()
    with _DB_ISSUE_LOCK:
        for key in [k for k, (_, exp) in _DB_ISSUED.items() if exp <= send_start_ms]:
            del _DB_ISSUED[key]
        seen = _DB_ISSUED.get(digest)
        if seen is not None:
            return seen[0] != sequence
        _DB_ISSUED[digest] = (sequence, expires_at_ms)
        return False


def _json_int_seconds(value: object, maximum: int) -> int:
    """A JSON integer (never bool, float or string) between 1 and ``maximum``."""
    if type(value) is not int or not 1 <= value <= maximum:
        raise ValueError("invalid token lifetime")
    return value


def _ls_lifetime_seconds(field: str, value: object) -> int:
    """Example form: ``expires_in`` JSON int. Table form: ``expire_in`` String
    of at most 10 ASCII digits without sign, space or leading zero."""
    if field == "expires_in" and type(value) is int:
        seconds = value
    elif (field == "expire_in" and type(value) is str and 1 <= len(value) <= 10
            and value.isascii() and value.isdigit() and value[0] != "0"):
        seconds = int(value)
    else:
        raise ValueError("undocumented token lifetime representation")
    if not 1 <= seconds <= MAX_RELATIVE_LIFETIME_S:
        raise ValueError("invalid token lifetime")
    return seconds


class TokenError(RuntimeError):
    """Static error only, body and exception chain are intentionally discarded."""

    def __init__(self, kind: TokenFailure):
        self.kind = kind
        super().__init__(kind.value)


def save_example_token_response(
    response: WireResponse, identity: CredentialIdentity,
    provider: InMemoryCredentialProvider, cache: InMemoryTokenCache, *, now_ms: int,
    kis_expiry_timezone: timezone | None = None,
    db_production_key_acknowledged: bool = False,
    db_no_prior_token_acknowledged: bool = False,
) -> BearerLease:
    """Accept an explicit verified HTTP-200 response body; no network or retry.

    Uses publisher example expiration fields, not an inferred TTL. KIS's
    sample has a naive timestamp: a caller must explicitly supply its fixed
    timezone interpretation; synthetic fixture context is not live evidence.
    Only a response that ``HttpsTransport`` itself received is cached
    (``UNATTESTED`` otherwise). LS returns a relative lifetime in seconds; the
    lease expires that long after the transport's own clock reading taken
    just before the request write, never after the caller's ``now_ms``, so
    the lifetime cannot be stretched. ``now_ms`` only rejects an expiry that
    has already passed. A token from an earlier send never replaces one from a
    later send (``SUPERSEDED``).

    DB (ADR 0015) returns a relative ``expires_in`` too, but re-issues the
    same token with its original expiry when one is still valid, and live and
    demo app keys share one origin. Neither is visible in the response, so a
    DB lease needs both caller acknowledgements: ``db_production_key_
    acknowledged`` (the app key is a production key, matching the ``live``
    label) and ``db_no_prior_token_acknowledged`` (no unexpired token existed
    for this app key when the request was sent: a first issue, more than 24 h
    after the last one, or after a revoke). Otherwise ``UNACKNOWLEDGED``. A
    token this process already received from an earlier send is refused as
    ``REISSUED`` whatever the caller acknowledges. Other processes are not
    visible. Passing either acknowledgement for another broker is refused.
    A failed parse does not mutate the cache. Exchange-time credential rotation
    is rejected before writing the token. Future production support needs
    separately verified quote/source/status/expiry semantics.
    """
    if (type(response) is not WireResponse or type(identity) is not CredentialIdentity
            or type(provider) is not InMemoryCredentialProvider
            or type(cache) is not InMemoryTokenCache or type(now_ms) is not int
            or now_ms < 0):
        raise TokenError(TokenFailure.INVALID_RESPONSE)
    req = response.request
    if (type(req) is not WireRequest or type(req.source) is not AuthRequirements
            or req.purpose != "token" or type(response.status) is not int
            or req.source.broker != identity.broker
            or req.source.environment != identity.environment or response.status != 200):
        raise TokenError(TokenFailure.INVALID_RESPONSE)
    snap = req.credential_snapshot
    if snap is None or snap.identity != identity or snap.owner is not provider:
        raise TokenError(TokenFailure.STALE_CREDENTIAL)
    try:
        provider.require_current(snap)
    except CredentialError:
        stale = True
    else:
        stale = False
    if stale:
        raise TokenError(TokenFailure.STALE_CREDENTIAL)

    if type(response.body) is not bytes or len(response.body) > MAX_RESPONSE_BYTES:
        raise TokenError(TokenFailure.INVALID_RESPONSE)

    def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
        values: dict = {}
        for key, value in pairs:
            if key in values:
                raise ValueError("duplicate JSON field")
            values[key] = value
        return values

    def no_nonfinite(_value: str) -> None:
        raise ValueError("non-finite JSON token")

    expires = None
    lifetime_s = None
    date_format = None
    expiry_text = None
    try:
        payload = json.loads(
            response.json_text, object_pairs_hook=no_duplicate_keys, parse_constant=no_nonfinite
        )
        if type(payload) is not dict:
            raise ValueError("not a dict")
        if any(key in payload for key in ("error", "error_code", "error_description")):
            raise ValueError("explicit error response")
        kind = payload["token_type"]
        if type(kind) is not str or kind.lower() != "bearer":
            raise ValueError("unexpected token type")
        if identity.broker == "ls":
            # LS API guide token detail documents the lifetime two ways: the
            # field table says `expire_in`, type String, length 10; the response
            # example says `expires_in` as a JSON number. Each (name, type) pair
            # is accepted only as documented; mixed or both/neither fail closed.
            if any(key in payload for key in ("rsp_cd", "rsp_msg")):
                raise ValueError("gateway status envelope on token response")
            if payload["scope"] != "oob":
                raise ValueError("unexpected token scope")
            access = payload["access_token"]
            present = [key for key in ("expires_in", "expire_in") if key in payload]
            if len(present) != 1:
                raise ValueError("ambiguous token lifetime field")
            lifetime_s = _ls_lifetime_seconds(present[0], payload[present[0]])
        elif identity.broker == "db":
            # Exactly the API guide example's keys: an `rsp_cd`/`error`
            # envelope, the field table's `token`/`expire_in` names or any
            # other extra key fails closed. token_type is exactly "Bearer".
            if set(payload) != _DB_TOKEN_KEYS or kind != "Bearer":
                raise ValueError("undocumented DB token response shape")
            if type(payload["scope"]) is not str or payload["scope"] not in _DB_TOKEN_SCOPES:
                raise ValueError("unexpected token scope")
            access = payload["access_token"]
            lifetime_s = _json_int_seconds(payload["expires_in"], DB_MAX_LIFETIME_S)
        elif identity.broker == "kis":
            access = payload["access_token"]
            expiry_text = payload["access_token_token_expired"]
            if type(expiry_text) is not str:
                raise ValueError("invalid token expiry")
            date_format = "%Y-%m-%d %H:%M:%S"
            expires = datetime.strptime(expiry_text, date_format)
        elif identity.broker == "kiwoom":
            if type(payload.get("return_code")) is not int or payload["return_code"] != 0:
                raise ValueError("invalid token status")
            access = payload["token"]
            expiry_text = payload["expires_dt"]
            if type(expiry_text) is not str:
                raise ValueError("invalid token expiry")
            date_format = "%Y%m%d%H%M%S"
            expires = datetime.strptime(expiry_text, date_format)
        else:
            raise ValueError("unsupported broker")
        if (type(access) is not str or not 1 <= len(access) <= 8192
                or any(char in access for char in "\r\n\x00")):
            raise ValueError("invalid token")
        if expires is not None and expires.strftime(date_format) != expiry_text:
            raise ValueError("ambiguous date format")
        valid = True
    except (ValueError, TypeError, KeyError, OverflowError, AttributeError,
            RecursionError, TransportError):
        valid = False
    if not valid:
        raise TokenError(TokenFailure.INVALID_RESPONSE)
    if identity.broker == "kis":
        if kis_expiry_timezone is None:
            raise TokenError(TokenFailure.EVIDENCE_MISSING)
        if type(kis_expiry_timezone) is not timezone:
            raise TokenError(TokenFailure.INVALID_RESPONSE)
        expiry_timezone = kis_expiry_timezone
    else:
        if kis_expiry_timezone is not None:
            raise TokenError(TokenFailure.INVALID_RESPONSE)
        expiry_timezone = KST  # Explicitly assigned in the pinned Kiwoom auth source.
    db_acks = (db_production_key_acknowledged, db_no_prior_token_acknowledged)
    if any(type(ack) is not bool for ack in db_acks) or (
            identity.broker != "db" and any(db_acks)):
        raise TokenError(TokenFailure.INVALID_RESPONSE)
    attestation = _token_send_attestation(response)
    if attestation is None:
        raise TokenError(TokenFailure.UNATTESTED)
    if lifetime_s is not None:
        # Counted from just before the write: the server cannot have issued
        # the token earlier, so this never overstates the remaining lifetime
        # of a FRESHLY issued token (for DB see the re-issue check below).
        expires_at_ms = attestation.send_start_ms + lifetime_s * 1000
    else:
        try:
            expires_at_ms = int(expires.replace(tzinfo=expiry_timezone).timestamp() * 1000)
        except (ValueError, OverflowError, OSError):
            expires_at_ms = -1
    if identity.broker == "db":
        # Recorded before any refusal below: the gateway issued this token
        # whether or not this call caches it.
        if _db_reissued(access, attestation.sequence, attestation.send_start_ms,
                        expires_at_ms):
            raise TokenError(TokenFailure.REISSUED)
        if not all(db_acks):
            raise TokenError(TokenFailure.UNACKNOWLEDGED)
    if expires_at_ms <= now_ms:
        raise TokenError(TokenFailure.INVALID_RESPONSE)
    # Check again for rotated credentials before mutation; no automatic refresh.
    try:
        provider.require_current(snap)
    except CredentialError:
        stale = True
    else:
        stale = False
    if stale:
        raise TokenError(TokenFailure.STALE_CREDENTIAL)
    try:
        lease = cache.put(provider, snap, access_token=access, expires_at_ms=expires_at_ms,
                          now_ms=now_ms, issue_sequence=attestation.sequence)
        refused = None
    except CredentialError as error:
        refused = error.kind
    if refused is CredentialFailure.SUPERSEDED:
        raise TokenError(TokenFailure.SUPERSEDED)
    if refused is CredentialFailure.STALE:
        raise TokenError(TokenFailure.STALE_CREDENTIAL)
    if refused is not None:
        raise TokenError(TokenFailure.INVALID_RESPONSE)
    return lease
