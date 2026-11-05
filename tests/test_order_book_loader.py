"""The order-book decoding seam is optional, not a fake Python fallback."""

from types import ModuleType

import pytest

from ktradelink import _native
from ktradelink.models import OrderBook


def test_missing_extension_fails_explicitly(monkeypatch) -> None:
    def missing(name: str):
        raise ModuleNotFoundError("synthetic absent", name=name)

    monkeypatch.setattr(_native, "import_module", missing)
    with pytest.raises(_native.NativeCoreUnavailable, match="not installed"):
        _native.decode_order_book_candidate("kis", "005930", "KRX", "{}")


def test_an_old_contract_build_is_rejected_before_the_call(monkeypatch) -> None:
    module = ModuleType("fake_native")
    module.CONTRACT_VERSION = 1  # pre-order-book contract

    def must_not_run(*args, **kwargs):
        raise AssertionError("an incompatible native build must not be called")

    module._decode_order_book_candidate = must_not_run
    monkeypatch.setattr(_native, "import_module", lambda name: module)
    with pytest.raises(_native.NativeCoreUnavailable, match="Incompatible"):
        _native.decode_order_book_candidate("kis", "005930", "KRX", "{}")


@pytest.mark.parametrize("returned", [{"bids": [], "asks": []}, [], None, "book"])
def test_malformed_native_return_is_rejected(monkeypatch, returned) -> None:
    module = ModuleType("fake_native")
    module.CONTRACT_VERSION = _native._CONTRACT_VERSION
    module._decode_order_book_candidate = lambda *args, **kwargs: returned
    monkeypatch.setattr(_native, "import_module", lambda name: module)
    with pytest.raises(RuntimeError, match="model type"):
        _native.decode_order_book_candidate("kis", "005930", "KRX", "{}")


def test_limit_is_forwarded_as_keyword(monkeypatch) -> None:
    seen = {}
    book = OrderBook("005930", "KRX", "kis", (), ())

    def fake(*args, **kwargs):
        seen.update(args=args, kwargs=kwargs)
        return book

    module = ModuleType("fake_native")
    module.CONTRACT_VERSION = _native._CONTRACT_VERSION
    module._decode_order_book_candidate = fake
    monkeypatch.setattr(_native, "import_module", lambda name: module)
    assert _native.decode_order_book_candidate("kis", "005930", "KRX", "{}", limit=3) is book
    assert seen == {"args": ("kis", "005930", "KRX", "{}"), "kwargs": {"limit": 3}}
