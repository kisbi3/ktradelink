"""Install both wheels in a clean venv and test outside the checkout (all OSes)."""

import argparse
import os
import subprocess
import tempfile
import venv
from pathlib import Path

MISSING_CHECK = '''
import ktradelink
from decimal import Decimal
from ktradelink.models import Ticker
from ktradelink._native import NativeCoreUnavailable, build_ticker
assert Ticker("005930", "KRX", "synthetic", Decimal(0)).last == 0
try:
    build_ticker("005930", "KRX", "synthetic")
except NativeCoreUnavailable:
    pass
else:
    raise AssertionError("native extension unexpectedly present in fresh venv")
'''

INSTALLED_CHECK = '''
import sys
from decimal import Decimal
from pathlib import Path
import _ktradelink_native
import ktradelink
from ktradelink._native import build_ticker, core_version
from ktradelink.models import Ticker
root = Path(sys.prefix).resolve()
for module in (ktradelink, _ktradelink_native):
    assert Path(module.__file__).resolve().is_relative_to(root), module.__file__
text = "9007199254740993.123456789012345678900"
result = build_ticker("005930", "KRX", "synthetic", last=text, volume=0)
assert type(result) is Ticker
assert result.last.as_tuple() == Decimal(text).as_tuple()
assert result.volume == 0 and result.timestamp is None
assert result.info == {} and core_version() == "0.1.0"
assert (Path(ktradelink.__file__).parent / "py.typed").is_file()
print("Isolated native wheel -> existing typed Ticker: passed")
'''


def only_wheel(directory: Path) -> Path:
    paths = list(directory.glob("*.whl"))
    if len(paths) != 1:
        raise ValueError(f"Expected exactly one wheel in {directory}")
    return paths[0].resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-dist", type=Path, required=True)
    parser.add_argument("--native-dist", type=Path, required=True)
    args = parser.parse_args()
    sdk = only_wheel(args.python_dist)
    native = only_wheel(args.native_dist)
    with tempfile.TemporaryDirectory(prefix="ktl-native-install-") as temp:
        root = Path(temp)
        env = root / "venv"
        venv.EnvBuilder(with_pip=True).create(env)
        python = env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        subprocess.run([str(python), "-m", "pip", "install", str(sdk)], check=True, cwd=root)
        subprocess.run([str(python), "-I", "-c", MISSING_CHECK], check=True, cwd=root)
        subprocess.run([str(python), "-m", "pip", "install", "--no-deps", str(native)], check=True, cwd=root)
        subprocess.run([str(python), "-I", "-c", INSTALLED_CHECK], check=True, cwd=root)


if __name__ == "__main__":
    main()
