"""Private optional Rust seam, NOT a published brokerage client."""

from importlib import import_module
from types import ModuleType

from ktradelink.models import Ticker

_MODULE = "_ktradelink_native"
_CONTRACT_VERSION = 1


class NativeCoreUnavailable(ImportError):
    """The optional native module is absent or has an incompatible contract."""


def _load_native() -> ModuleType:
    try:
        module = import_module(_MODULE)
    except ModuleNotFoundError as exc:
        if exc.name != _MODULE:
            raise  # A broken transitive dependency is not an absent extension.
        raise NativeCoreUnavailable(
            "Optional Rust core is not installed. Build bindings/python first; "
            "ordinary ktradelink.models remain available."
        ) from exc
    contract = getattr(module, "CONTRACT_VERSION", None)
    if type(contract) is not int or contract != _CONTRACT_VERSION:
        raise NativeCoreUnavailable("Incompatible native core contract; rebuild bindings/python.")
    return module


def core_version() -> str:
    value = _load_native().CORE_VERSION
    if not isinstance(value, str):
        raise NativeCoreUnavailable("Invalid native core version metadata.")
    return value


def build_ticker(
    symbol: str, venue: str, broker: str, *, last: str | None = None,
    open: str | None = None, high: str | None = None, low: str | None = None,
    previous_close: str | None = None, bid: str | None = None, ask: str | None = None,
    volume: int | None = None, timestamp: int | None = None,
    retrieved_at: int | None = None, scope_description: str | None = None,
) -> Ticker:
    """Internal normalized-text construction probe, NOT fetch_ticker.

    No native fallback, network I/O, broker parsing or hidden metadata forwarding.
    Public users continue to consume the existing Ticker class.
    """
    result = _load_native()._build_ticker(
        symbol, venue, broker, last=last, open=open, high=high, low=low,
        previous_close=previous_close, bid=bid, ask=ask, volume=volume,
        timestamp=timestamp, retrieved_at=retrieved_at, scope_description=scope_description,
    )
    if not isinstance(result, Ticker):
        raise RuntimeError("Native core returned an incompatible model type.")
    return result


def decode_ticker_candidate(broker: str, symbol: str, venue: str, payload: str) -> Ticker:
    """PRIVATE offline publisher-evidence decoder; NO broker/network request.

    The caller's KRX/symbol context is not proof of an exchange-sourced price.
    Supports six restricted synthetic response shapes, with strict validation.
    Never expose this as a production/public fetch_ticker implementation.
    """
    result = _load_native()._decode_ticker_candidate(broker, symbol, venue, payload)
    if not isinstance(result, Ticker):
        raise RuntimeError("Native decoder returned an incompatible model type.")
    return result
