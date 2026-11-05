"""Optional loader tests need no Rust installation and never contact brokers."""

from types import ModuleType

import pytest

from ktradelink import _native
from ktradelink.models import Ticker


def test_missing_extension_is_explicit_and_python_models_still_work(monkeypatch) -> None:
    def missing(name: str):
        raise ModuleNotFoundError("synthetic missing extension", name=name)
    monkeypatch.setattr(_native, "import_module", missing)
    with pytest.raises(_native.NativeCoreUnavailable, match="not installed"):
        _native.build_ticker("005930", "KRX", "synthetic", last=None)
    assert Ticker("005930", "KRX", "synthetic", None).last is None


def test_broken_transitive_import_is_not_hidden(monkeypatch) -> None:
    def broken(name: str):
        raise ModuleNotFoundError("synthetic broken dependency", name="another_dependency")
    monkeypatch.setattr(_native, "import_module", broken)
    with pytest.raises(ModuleNotFoundError) as caught:
        _native.core_version()
    assert type(caught.value) is ModuleNotFoundError
    assert caught.value.name == "another_dependency"


@pytest.mark.parametrize("contract", [None, True, 0, 1, 3, "2", 2.0])
def test_contract_mismatch_rejected(monkeypatch, contract: object) -> None:
    module = ModuleType("fake_native")
    module.CONTRACT_VERSION = contract
    monkeypatch.setattr(_native, "import_module", lambda name: module)
    with pytest.raises(_native.NativeCoreUnavailable, match="Incompatible"):
        _native.core_version()


def test_wrong_return_type_is_not_a_dictionary_api(monkeypatch) -> None:
    module = ModuleType("fake_native")
    module.CONTRACT_VERSION = _native._CONTRACT_VERSION
    module._build_ticker = lambda *args, **kwargs: {"last": "1"}
    monkeypatch.setattr(_native, "import_module", lambda name: module)
    with pytest.raises(RuntimeError, match="model type"):
        _native.build_ticker("005930", "KRX", "synthetic")
