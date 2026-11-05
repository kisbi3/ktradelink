"""Private, value-free response diagnostics for an opt-in live smoke check.

Two helpers, both built to be safe to print and share:

- ``json_shape`` lists field paths and JSON types, never values.
- ``gateway_status`` extracts a short, sanitised status code and message from
  a small fixed set of envelope keys, with caller-supplied secrets redacted.

Neither is evidence of what a broker actually returns. Field names extracted
here are generic: ``rsp_cd``/``rsp_msg`` are the LS t1102 envelope (ADR 0010),
and ``error``/``error_description`` are the generic OAuth 2.0 error fields
(RFC 6749 section 5.2). Whether a given broker uses them on errors is unverified.
"""

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass

MAX_SHAPE_LINES = 200
MAX_SHAPE_DEPTH = 8
MAX_ARRAY_SAMPLE = 20
MAX_MESSAGE_CHARS = 200
_SAFE_KEY = re.compile(r"[A-Za-z0-9_]{1,64}")
_SAFE_CODE = re.compile(r"[A-Za-z0-9_.\-]{1,32}")
_DIGITS = re.compile(r"[0-9]+")
_DECIMAL = re.compile(r"[+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)")
_CODE_KEYS = ("rsp_cd", "error")
_MESSAGE_KEYS = ("rsp_msg", "error_description")
REDACTED = "<redacted>"


def _parse(body: object) -> tuple[object, str | None]:
    if type(body) is not bytes:
        return None, "<body is not bytes>"
    try:
        text = body.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return None, "<body is not UTF-8>"

    def no_constant(_value: str) -> None:
        raise ValueError("non-finite JSON number")

    try:
        return json.loads(text, parse_constant=no_constant), None
    except (ValueError, RecursionError):
        return None, "<body is not JSON>"


def _string_class(value: str) -> str:
    """A coarse class that helps a decoder fix without revealing the value."""
    if not value:
        return "string:empty"
    if value.isascii() and _DIGITS.fullmatch(value):
        return "string:digits"
    if value.isascii() and _DECIMAL.fullmatch(value):
        return "string:decimal"
    return "string:text"


def _scalar(value: object) -> str:
    if value is None:
        return "null"
    if type(value) is bool:
        return "boolean"
    if type(value) is int:
        return "integer"
    if type(value) is float:
        return "number"
    if type(value) is str:
        return _string_class(value)
    return "unknown"


def json_shape(body: bytes) -> tuple[str, ...]:
    """Sorted ``path: type`` lines for a JSON body, without any value.

    Object keys outside ``[A-Za-z0-9_]{1,64}`` are shown as ``<key>`` so an
    unexpected key cannot carry a value. Arrays are summarised as ``path[]``
    from their first elements. Depth and line count are bounded.
    """
    payload, problem = _parse(body)
    if problem is not None:
        return (problem,)
    lines: set[str] = set()

    def walk(value: object, path: str, depth: int) -> None:
        if len(lines) > MAX_SHAPE_LINES:
            return
        label = path or "$"
        if depth > MAX_SHAPE_DEPTH:
            lines.add(f"{label}: <depth limit>")
        elif type(value) is dict:
            lines.add(f"{label}: object")
            for key, child in value.items():
                name = key if _SAFE_KEY.fullmatch(key) else "<key>"
                walk(child, f"{path}.{name}" if path else name, depth + 1)
        elif type(value) is list:
            lines.add(f"{label}: array")
            for child in value[:MAX_ARRAY_SAMPLE]:
                walk(child, f"{path}[]", depth + 1)
        else:
            lines.add(f"{label}: {_scalar(value)}")

    walk(payload, "", 0)
    ordered = sorted(lines)
    if len(ordered) > MAX_SHAPE_LINES:
        ordered = ordered[:MAX_SHAPE_LINES] + ["<more fields omitted>"]
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class GatewayStatus:
    """Sanitised envelope status; ``None`` fields were absent."""

    code: str | None
    message: str | None


def _code(value: object) -> str | None:
    if value is None:
        return None
    if type(value) is int:  # bool is excluded: type(True) is bool
        value = str(value)
    if type(value) is str and _SAFE_CODE.fullmatch(value):
        return value
    return "<invalid code>"


def _message(value: object, secrets: tuple[str, ...]) -> str | None:
    if value is None:
        return None
    if type(value) is not str:
        return "<invalid message>"
    for secret in secrets:
        value = value.replace(secret, REDACTED)
    cleaned = "".join(char if char.isprintable() else "?" for char in value)
    if len(cleaned) > MAX_MESSAGE_CHARS:
        cleaned = cleaned[:MAX_MESSAGE_CHARS] + "…"
    # Redact again: truncation or replacement must not reassemble a secret.
    for secret in secrets:
        cleaned = cleaned.replace(secret, REDACTED)
    return cleaned


def gateway_status(body: bytes, *, redact: Iterable[str] = ()) -> GatewayStatus | None:
    """Return the root-level status envelope, or ``None`` if there is none.

    Only ``rsp_cd``/``error`` (code) and ``rsp_msg``/``error_description``
    (message) are read. Each string in ``redact`` (credentials, tokens) is
    replaced in the message; strings shorter than 4 characters are ignored so
    redaction cannot shred ordinary text.
    """
    secrets = tuple(sorted({s for s in redact if type(s) is str and len(s) >= 4},
                           key=len, reverse=True))
    payload, problem = _parse(body)
    if problem is not None or type(payload) is not dict:
        return None
    code_key = next((key for key in _CODE_KEYS if key in payload), None)
    message_key = next((key for key in _MESSAGE_KEYS if key in payload), None)
    if code_key is None and message_key is None:
        return None
    return GatewayStatus(
        _code(payload.get(code_key)) if code_key else None,
        _message(payload.get(message_key), secrets) if message_key else None,
    )
