"""Private KIS/Kiwoom publisher-example token parsing, without network I/O.

No automatic token issuance or refresh, and no unsupported broker extrapolation.
Errors never reflect the upstream body. Parser success is NOT live validation.
"""

import json
from datetime import datetime, timedelta, timezone
from enum import Enum

from ktradelink._credential_runtime import (
    BearerLease,
    CredentialError,
    CredentialIdentity,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._https_transport import (
    MAX_RESPONSE_BYTES,
    TransportError,
    WireRequest,
    WireResponse,
)
from ktradelink._request_plan import AuthRequirements

KST = timezone(timedelta(hours=9))


class TokenFailure(Enum):
    INVALID_RESPONSE = "token_response_invalid_or_unverified"
    EVIDENCE_MISSING = "token_expiry_timezone_not_supplied"
    STALE_CREDENTIAL = "credentials_changed_during_token_exchange"


class TokenError(RuntimeError):
    """Static error only, body and exception chain are intentionally discarded."""

    def __init__(self, kind: TokenFailure):
        self.kind = kind
        super().__init__(kind.value)


def save_example_token_response(
    response: WireResponse, identity: CredentialIdentity,
    provider: InMemoryCredentialProvider, cache: InMemoryTokenCache, *, now_ms: int,
    kis_expiry_timezone: timezone | None = None,
) -> BearerLease:
    """Accept an explicit verified HTTP-200 response body; no network or retry.

    Uses publisher example expiration fields, not an inferred TTL. KIS's
    sample has a naive timestamp: a caller must explicitly supply its fixed
    timezone interpretation; synthetic fixture context is not live evidence.
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
        if identity.broker == "kis":
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
        if expires.strftime(date_format) != expiry_text:
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
    try:
        expires_at_ms = int(expires.replace(tzinfo=expiry_timezone).timestamp() * 1000)
    except (ValueError, OverflowError, OSError):
        expires_at_ms = -1
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
    return cache.put(provider, snap, access_token=access, expires_at_ms=expires_at_ms,
                     now_ms=now_ms)
