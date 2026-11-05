"""Public, experimental error taxonomy for ``ktradelink.connect`` clients.

Every error carries only static text: a ``reason`` code chosen by this
library, the request ``stage`` it concerns and a ``delivery`` state. No error
contains a credential, token, header value, URL query, response body or
upstream message, and none chains the private exception that caused it
(``__cause__`` and ``__context__`` are ``None``).

``delivery`` describes the request named by ``stage``:

- ``NOT_SENT``: nothing of that request was written to the network.
- ``UNKNOWN``: the request may have reached the broker. **Never treat it as
  safe to repeat** for a non-idempotent operation; for a token request it may
  have issued a token that this client did not keep.
- ``RESPONSE_RECEIVED``: the broker answered; the answer was rejected.

HTTP-status-based classes (``AuthenticationError`` for 401, ``PermissionDenied``
for 403, ``RateLimitExceeded`` for 429, ``BrokerUnavailable`` for 5xx) follow
the generic HTTP meaning of the status. They are **not** verified broker error
semantics, and broker-native error codes are not interpreted (ADR 0013).
"""

from enum import Enum

__all__ = [
    "AuthenticationError",
    "BrokerRejected",
    "BrokerUnavailable",
    "ClientClosed",
    "DeliveryState",
    "InvalidParameter",
    "InvalidSymbol",
    "InvalidVenue",
    "KTradeLinkError",
    "NetworkDisabled",
    "PermissionDenied",
    "RateLimitExceeded",
    "ResponseSchemaError",
    "TransportError",
    "UnsupportedCapability",
]


class DeliveryState(Enum):
    """Whether the request named by an error's ``stage`` reached the broker."""

    NOT_SENT = "not_sent"
    UNKNOWN = "may_have_been_sent"
    RESPONSE_RECEIVED = "response_received"


_STAGES = (None, "token", "quote")


def _rebuild(cls, reason, delivery, stage, detail):
    return cls(reason, delivery=delivery, stage=stage, detail=detail)


class KTradeLinkError(Exception):
    """Base class. ``reason``/``stage``/``detail`` are static library strings.

    ``detail`` is set only for a native decoder rejection and then holds the
    decoder's static ``"<field>: <Kind>"`` text, never a value.
    """

    def __init__(self, reason: str, *, delivery: DeliveryState = DeliveryState.NOT_SENT,
                 stage: str | None = None, detail: str | None = None):
        if type(reason) is not str or not reason:
            raise TypeError("reason must be a non-empty str")
        if type(delivery) is not DeliveryState:
            raise TypeError("delivery must be a DeliveryState")
        if stage not in _STAGES:
            raise TypeError("stage must be None, 'token' or 'quote'")
        if detail is not None and type(detail) is not str:
            raise TypeError("detail must be a str or None")
        self.reason = reason
        self.delivery = delivery
        self.stage = stage
        self.detail = detail
        text = f"{reason} (stage={stage or 'request'}, delivery={delivery.value})"
        if detail is not None:
            text += f" [{detail}]"
        super().__init__(text)

    def __reduce__(self):
        return (_rebuild, (type(self), self.reason, self.delivery, self.stage, self.detail))


class InvalidSymbol(KTradeLinkError):
    """The symbol is not exactly six ASCII ``[0-9A-Z]`` characters (ADR 0016).

    Nothing is case-folded, trimmed or stripped: lowercase, whitespace and
    native prefixes or suffixes (``A005930``, ``005930_NX``) are rejected. A
    well-formed alphanumeric symbol for a broker without evidence of such
    codes raises ``UnsupportedCapability`` instead.
    """


class InvalidVenue(KTradeLinkError):
    """The venue is not one of the spec's venue names."""


class InvalidParameter(KTradeLinkError):
    """An argument is malformed, unknown or not accepted yet (e.g. ``params``)."""


class UnsupportedCapability(KTradeLinkError):
    """The broker, environment, venue or capability is not enabled here."""


class NetworkDisabled(KTradeLinkError):
    """The client was created without ``allow_network=True``; nothing was sent."""


class ClientClosed(KTradeLinkError):
    """The client was closed; its credentials and token were dropped."""


class AuthenticationError(KTradeLinkError):
    """HTTP 401 from the broker (generic HTTP meaning, not a verified code)."""


class PermissionDenied(KTradeLinkError):
    """HTTP 403 from the broker (generic HTTP meaning, not a verified code)."""


class RateLimitExceeded(KTradeLinkError):
    """HTTP 429 from the broker. Nothing is retried automatically."""


class BrokerUnavailable(KTradeLinkError):
    """HTTP 5xx from the broker. Nothing is retried automatically."""


class TransportError(KTradeLinkError):
    """Connection, TLS, write, read, redirect or other non-success HTTP failure.

    Check ``delivery``: ``UNKNOWN`` means the request may have been received.
    """


class BrokerRejected(KTradeLinkError):
    """HTTP 200 whose body carries a non-success broker status.

    The broker's code and message are not interpreted or exposed.
    """


class ResponseSchemaError(KTradeLinkError):
    """HTTP 200 whose body is missing, malformed or fails the strict decoder."""
