"""Smoke tests for the installable KTradeLink package."""

import importlib
from importlib.metadata import version


def test_package_imports() -> None:
    module = importlib.import_module("ktradelink")
    assert module.__name__ == "ktradelink"


def test_distribution_version_matches_package_version() -> None:
    from ktradelink import __version__

    assert version("ktradelink") == __version__


def test_no_unimplemented_brokers_are_exposed() -> None:
    import ktradelink

    assert not hasattr(ktradelink, "kis")
    assert not hasattr(ktradelink, "kiwoom")
