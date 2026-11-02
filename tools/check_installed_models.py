"""Run with an isolated wheel venv, from outside the source checkout."""

import sys
from decimal import Decimal
from importlib.metadata import version
from pathlib import Path
from zoneinfo import ZoneInfo, reset_tzpath

import ktradelink
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
    print(f"Installed typed-model and timezone checks passed: {installed}")


if __name__ == "__main__":
    main()
