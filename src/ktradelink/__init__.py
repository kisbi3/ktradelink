"""KTradeLink: a future unified Python interface for Korean securities brokers.

EXPERIMENTAL: ``connect(...).fetch_ticker(...)`` exists for KIS, Kiwoom and
LS only, built from publisher documentation and tested offline. It has never
been verified against a live or paper gateway (state ``documented_candidate``,
ADR 0013). Network access is off unless explicitly enabled. There are no
account, order or streaming operations.
"""

from ktradelink._public_client import (
    BrokerClient,
    Capability,
    Credentials,
    capabilities,
    connect,
)
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

__version__ = "0.0.0.dev0"

__all__ = [
    "AuthenticationError",
    "BrokerClient",
    "BrokerRejected",
    "BrokerUnavailable",
    "Capability",
    "ClientClosed",
    "Credentials",
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
    "__version__",
    "capabilities",
    "connect",
]
