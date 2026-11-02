"""Private value validation shared by market-data models; no native parsing."""

import re
from collections.abc import Mapping
from decimal import Decimal
from types import MappingProxyType

InfoScalar = str | int | bool | Decimal | None
_SENSITIVE_KEY_FRAGMENTS = (
    "token", "secret", "password", "account", "authorization",
    "credential", "cookie", "apikey", "appkey", "acnt", "acct", "seckey",
)
_VENUES = frozenset({"KRX", "NXT", "BROKER_COMPOSITE"})


def validate_provenance(
    symbol: str, venue: str, broker: str, scope_description: str | None
) -> None:
    """Retain Ticker's identifier and composite-source rules."""
    for name, value in (("symbol", symbol), ("broker", broker)):
        if (
            not isinstance(value, str)
            or not value
            or value != value.strip()
            or any(char.isspace() or not char.isprintable() for char in value)
        ):
            raise ValueError(f"{name} must be a printable string without whitespace")
    if not isinstance(venue, str) or venue not in _VENUES:
        raise ValueError(f"venue must be one of {sorted(_VENUES)!r}")
    if venue == "BROKER_COMPOSITE" and (
        not isinstance(scope_description, str) or not scope_description.strip()
    ):
        raise ValueError("composite quote requires scope_description")
    if scope_description is not None and (
        not isinstance(scope_description, str)
        or scope_description != scope_description.strip()
        or not scope_description
        or any(not char.isprintable() for char in scope_description)
    ):
        raise ValueError("scope_description must be printable and trimmed")


def validate_price(name: str, value: object, *, nullable: bool = True) -> None:
    """Do not normalize a broker's sign or create a Decimal from a float."""
    if value is None and nullable:
        return
    if not isinstance(value, Decimal) or not value.is_finite() or value.is_signed():
        suffix = " or None" if nullable else ""
        raise ValueError(f"{name} must be an unsigned finite Decimal{suffix}")


def validate_integer(name: str, value: object, *, nullable: bool = True) -> None:
    if value is None and nullable:
        return
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        suffix = " or None" if nullable else ""
        raise ValueError(f"{name} must be a nonnegative integer{suffix}")


def freeze_info(info: Mapping[str, InfoScalar]) -> Mapping[str, InfoScalar]:
    """Copy flat scalar metadata; denylist is NOT a provider allowlist/redactor."""
    if not isinstance(info, Mapping):
        raise TypeError("info must be a mapping of safe scalar metadata")
    snapshot: dict[str, InfoScalar] = {}
    for key, value in info.items():
        if not isinstance(key, str):
            raise TypeError("info keys must be strings")
        normalized_key = "".join(char for char in key.casefold() if char.isalnum())
        key_parts = re.split(r"[^a-z0-9]+", key.casefold())
        if (
            any(term in normalized_key for term in _SENSITIVE_KEY_FRAGMENTS)
            or "cano" in key_parts
        ):
            raise ValueError("info must not contain authentication/account fields")
        if not (value is None or isinstance(value, (str, int, bool, Decimal))):
            raise TypeError("info values must be immutable scalar metadata")
        if isinstance(value, Decimal) and not value.is_finite():
            raise ValueError("info decimals must be finite")
        snapshot[key] = value
    return MappingProxyType(snapshot)
