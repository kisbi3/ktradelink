# Rust Core foundation: what now works

The native component is an optional local build. It does not implement any
broker API. Existing `from ktradelink.models import Ticker` usage and the pure
Python package build remain unchanged.

## Layout

```text
crates/ktradelink-core/  Exact decimal text and normalized quote values, pure Rust
bindings/python/        PyO3 conversion into the existing Python Ticker
src/ktradelink/_native.py  Private lazy loader, not a stable public API
experiments/rust-parse/  Prior benchmark, excluded from the new Cargo workspace
```

The Rust core knows nothing about Python. The binding is a translator: it accepts
normalized decimal strings, validates them in Rust, and constructs Python Decimal
and Ticker objects without passing through float. There is no dictionary-returning
public API and no duplicated replacement for the existing Python dataclass.

## Build locally (repository checkout; NOT a PyPI install instruction)

```bash
python -m pip install -e ".[dev]" "maturin==1.16.0" build
cargo test -p ktradelink-core
python -m maturin develop --release --manifest-path bindings/python/Cargo.toml
python -m pytest -q tests bindings/python/tests
```

`maturin develop` requires an activated virtual environment. For a distributable
local artifact, use `maturin build --release --manifest-path bindings/python/Cargo.toml`
and install the resulting wheel. The native distribution is `ktradelink-native`,
its extension module is `_ktradelink_native`. It is not published by this PR.

## Executable offline example (private development seam)

```python
from decimal import Decimal
from ktradelink._native import build_ticker
from ktradelink.models import Ticker

quote = build_ticker(
    "005930", "KRX", "synthetic",
    last="70500.00", volume=0, timestamp=None,
)
assert type(quote) is Ticker
assert quote.last == Decimal("70500.00")
assert quote.volume == 0
assert quote.timestamp is None
```

This only constructs a value from supplied synthetic data; it does not fetch
Samsung's price. The public broker `fetch_ticker` method is not implemented.

## Important boundaries

- Current native price grammar is unsigned digits plus optional fraction. Values
  like `-0`, `+1`, `1e3`, whitespace and nonfinite strings are rejected, not fixed.
  Precise digits and trailing zeros survive; the core is not a rounding engine.
- The private native seam accepts ASCII graphic symbol/broker identifiers and
  u64 nonnegative integer metadata. Existing Python models retain their own
  broader input contract. bool is never silently interpreted as integer 0/1.
- No raw `info` mapping is accepted at the native seam; output info is empty.
- Composite venue provenance is mandatory. Rust rejects absent/empty/control
  scope text; Python's final Ticker validation may reject additional Unicode
  nonprintables. Accepting a venue here does not declare broker support.
- Absence of the native wheel raises NativeCoreUnavailable on explicit native
  calls. Ordinary Python model construction still works. Broken transitive
  imports and contract-version mismatches are not hidden behind a fallback.
- Unit tests use invented normalized values. Real broker decoding, sign rules,
  auth, HTTP/WebSocket, rate limits, stream processing and credentials are outside
  this change. Rust build success is not evidence of live broker compatibility.
- CI targets ordinary CPython 3.11-3.13 on Ubuntu and 3.13 on native Windows/macOS.
  Coverage claims depend on actual job results, not merely the matrix definition.
  Release packaging/ABI3/free-threaded interpreters are not yet promised.
