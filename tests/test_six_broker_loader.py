"""The six-broker decoding seam is optional, not a fake Python fallback."""

from types import ModuleType

import pytest

from ktradelink import _native


def test_offline_candidate_missing_extension_fails_explicitly(monkeypatch) -> None:
    def missing(name: str):
        raise ModuleNotFoundError("synthetic absent", name=name)

    monkeypatch.setattr(_native, "import_module", missing)
    with pytest.raises(_native.NativeCoreUnavailable, match="not installed"):
        _native.decode_ticker_candidate("kis", "005930", "KRX", "{}")


def test_offline_candidate_malformed_native_return_is_rejected(monkeypatch) -> None:
    module = ModuleType("fake_native")
    module.CONTRACT_VERSION = 1
    module._decode_ticker_candidate = lambda *args, **kwargs: {"last": "1"}
    monkeypatch.setattr(_native, "import_module", lambda name: module)
    with pytest.raises(RuntimeError, match="model type"):
        _native.decode_ticker_candidate("kis", "005930", "KRX", "{}")


def test_offline_candidate_broken_native_import_not_hidden(monkeypatch) -> None:
    def broken(name: str):
        raise ModuleNotFoundError("synthetic missing underlying dependency", name="another_module")

    monkeypatch.setattr(_native, "import_module", broken)
    with pytest.raises(ModuleNotFoundError) as caught:
        _native.decode_ticker_candidate("kis", "005930", "KRX", "{}")
    assert caught.value.name == "another_module"
