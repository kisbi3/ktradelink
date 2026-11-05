"""Run with an isolated wheel venv, from outside the source checkout."""

import sys
from decimal import Decimal
from importlib.metadata import version
from pathlib import Path
from zoneinfo import ZoneInfo, reset_tzpath

import ktradelink
from ktradelink._credential_runtime import (
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
)
from ktradelink._https_transport import (
    HttpsTransport,
    TransportError,
    TransportFailure,
    build_token_request,
)
from ktradelink._offline_session import (
    CredentialScope,
    FailureKind,
    FakeCredentialProvider,
    FakeResponse,
    FakeTransport,
    OfflineSessionError,
    execute_offline_quote,
)
from ktradelink._request_plan import authentication_requirements, plan_ticker_request
from ktradelink.models import Candle, OrderBook, OrderBookLevel, Ticker


def main() -> None:
    installed = Path(ktradelink.__file__).resolve()
    assert installed.is_relative_to(Path(sys.prefix).resolve())
    assert version("ktradelink") == ktradelink.__version__
    assert (installed.parent / "py.typed").is_file()
    assert version("tzdata")
    # Emulate a machine with no OS IANA database, without changing the host.
    reset_tzpath(())
    ZoneInfo.clear_cache()
    candle = Candle(
        symbol="005930", venue="KRX", broker="synthetic", timeframe="1d",
        timestamp=1793113200000, session_date="2026-10-28",
        open=Decimal(1), high=Decimal(1), low=Decimal(1), close=Decimal(1),
        volume=0, adjustment="raw", session="regular",
    )
    quote = Ticker("005930", "KRX", "synthetic", Decimal(1))
    book = OrderBook("005930", "KRX", "synthetic", (OrderBookLevel(Decimal(1), 0),), ())
    assert candle.complete is None and candle.source_timestamp is None
    assert book.timestamp is None and quote.timestamp is None
    assert len({candle, quote, book}) == 3
    assert not hasattr(candle, "to_dict")
    assert not hasattr(book, "to_json")
    for broker in ("kis", "kiwoom", "ls", "db", "toss", "meritz"):
        plan = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
        assert not plan.transport_implemented and plan.origin.startswith("https://")
        assert not authentication_requirements(
            broker, environment="live"
        ).token_exchange_implemented
        scope = CredentialScope(broker, "live", 0)
        provider = FakeCredentialProvider()
        lease = provider.issue(scope, now_ms=0, lifetime_ms=100)
        transport = FakeTransport((FakeResponse(plan, lease, 403, "{}"),))
        try:
            execute_offline_quote(plan, scope, provider, transport, now_ms=1)
        except OfflineSessionError as exc:
            assert exc.kind is FailureKind.FORBIDDEN
        else:
            raise AssertionError("fake forbidden response accepted")
        assert transport.calls == 1
    identity = CredentialIdentity("kis", "live", "installed-smoke")
    explicit = InMemoryCredentialProvider()
    explicit.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    request = build_token_request(identity, explicit)
    assert "SYNTHETIC_SECRET" not in repr(request)
    try:
        HttpsTransport().send(request)
    except TransportError as exc:
        assert exc.kind is TransportFailure.NOT_ENABLED
    else:
        raise AssertionError("disabled HTTPS transport accidentally permitted network")
    assert "ktradelink._native" not in sys.modules
    assert "_ktradelink_native" not in sys.modules
    print(f"Installed typed-model and offline request-plan checks passed: {installed}")


if __name__ == "__main__":
    main()
