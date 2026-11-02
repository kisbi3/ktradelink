# ADR 0005: Rust core with a separate Python binding

- Date: 2026-11-02
- Status: Direction accepted by the maintainer; implementation awaits PR review
- Base: e865e73d3023e908a26ad88610f09b56fc8cfaec (PR #11 merged)
- Scope: foundation and offline construction, NOT a brokerage adapter

## Decision and authorization boundary

The maintainer selected Rust Core + Python SDK as the target architecture and
asked to implement the foundation. This supersedes ADR 0004's undecided language
direction, NOT its cautions about synthetic benchmarks or production readiness.
The first native path only constructs existing Python Ticker values. It does not
fetch prices, parse a named broker response, authenticate, or execute orders.
No production speed claim follows from this PR.

## Separation

- crates/ktradelink-core: ordinary Rust library, no PyO3, Python, network, JSON,
  broker credentials, or external runtime dependencies. It owns exact decimal
  text validation, typed quote fields, venue identity, and structured errors.
- bindings/python: thin PyO3 extension. It translates Python arguments into Rust
  values and converts the result into the EXISTING ktradelink.models.Ticker.
- src/ktradelink/_native.py: private, lazy-loading integration seam. Absence of
  the optional extension produces an explicit error, not a silent Python fallback.
- Existing Python dataclasses, their public imports, and the root setuptools
  build remain unchanged. Public results are typed models, not dictionaries.
- experiments/rust-parse remains isolated from the new Cargo workspace. It is
  not copied wholesale into production-facing code.

## Deliberately narrow normalized input contract

This is not a broker wire decoder. Price input is already normalized unsigned
ASCII decimal text: one or more digits, optionally followed by a dot and one or
more digits. No signs (including -0), whitespace, exponent syntax, NaN/Infinity,
float conversion, or guessed sign removal. Exact text is carried to Python
Decimal, preserving arbitrary precision and trailing zeros. This transport type
is not a Rust arithmetic/rounding engine. Python's direct Ticker constructor is
unchanged and can still accept its existing Decimal inputs.

Symbol and broker identifiers in this initial native seam must be nonempty ASCII
graphic strings (no whitespace/control characters). This is a private boundary
restriction, not a claim about every supported security identifier or a change
to the broader Python model constructor. Six-digit numeric-only rules are NOT
introduced. Venue is KRX, NXT, or BROKER_COMPOSITE; accepting a venue in a value
object does not imply that a broker supports it. Composite scope is explicit.

Native integer metadata uses u64. Python bool is explicitly rejected before
integer conversion; out-of-range and negative integers are errors. Missing values
remain None, not zero. The binding sends no upstream info payload: info defaults
to an empty mapping. The final Python Ticker constructor still enforces its own
public invariants. Neither boundary changes partial data into plausible values.

## Packaging and compatibility

Build the extension as an optional, separately installed local wheel named
ktradelink-native with module _ktradelink_native. It is not published by this PR,
and no root dependency on an unavailable PyPI package is added. Ordinary
installation of ktradelink remains usable without Rust or the native wheel.
The private loader checks a contract version and surfaces incompatible modules
explicitly. Rust source, Python wheel, and source distribution builds are tested
separately; a green Linux build alone is not Windows/macOS validation.

Use pinned Rust/PyO3/Maturin versions and a workspace Cargo.lock when generated.
No ABI3/free-threaded-Python support is promised by this foundation. Current
validation targets ordinary CPython 3.11-3.13. No public native decode_* API is
frozen yet; the first real broker decoder is a subsequent independently reviewed
change grounded in official payload evidence.

## Acceptance and review

Core-only Rust tests must run without a Python binding dependency. Native tests
must prove exact Decimal round trips, null/zero distinctions, bool/u64 errors,
unchanged Ticker equality/hash, missing-extension behavior, and construction from
an installed wheel outside the checkout. Existing Python tests must still pass.
Use a focused original-source TXT for Gemini. Do not merge without explicit
maintainer approval. PR #6 and Issues #9/#12 are not silently closed or rewritten.

References consulted for tooling (2026-11-02):
- https://pyo3.rs/v0.29.0/module.html
- https://www.maturin.rs/tutorial
- https://www.maturin.rs/project_layout
- https://doc.rust-lang.org/cargo/reference/workspaces.html

These are build/tooling references, not evidence of broker behavior.
