# ADR 0004: Benchmark Rust before choosing the internal KTradeLink engine

- Date: 2026-11-02
- Status: **Experiment approved; language migration NOT approved**
- Current public SDK: Python-native `Ticker`, `Candle`, `OrderBook`, `OrderBookLevel`

## Decision

Compare an isolated Rust/PyO3/serde_json parser with a native Python/json
reference under **identical deterministic synthetic JSON input**. Both
must ultimately create the **same existing typed Python Ticker objects**;
the experiment may use internal tuples but MUST NOT expose a new
dictionary-returning API, alter the public package build, or call a broker.

Separate:
1. JSON decode/validation alone;
2. decoding plus construction of a full `Ticker`;
3. per-message Python-to-Rust boundary calls;
4. one batched Python-to-Rust call amortizing the boundary.

Do not equate synthetic parser throughput with native exchange event latency,
network RTT, permitted calls/second, order execution performance, or
a correctness proof for real KIS/Kiwoom/LS/DB/Toss/Meritz responses.
Include warmups, repeated measurements, input-byte size, exact tool versions,
p50 and p95 **of benchmark iterations**, and process-level noise caveats.
No fabricated speedup values.

## Consequences

- Rust remains an OPTIONAL experimental module under `experiments/`.
- `ktradelink` remains a pure Python wheel with no new native dependency.
- Existing data-model semantics and tests remain unchanged.
- Each benchmark result is a hypothesis about a specific workload and runner,
  not a universal Rust-vs-Python result; run more than once.
- A production Rust migration requires separate design review, real provider
  sanitized fixtures, measured end-to-end value, native Windows/macOS
  packaging feasibility, and explicit human approval.
- The user's preference remains **typed public models only**, not
  dictionary serialization helpers.

## Independent source references

- PyO3 modules: https://pyo3.rs/main/module
- Maturin tutorial: https://www.maturin.rs/tutorial.html
- Maturin local builds: https://www.maturin.rs/local_development
- Rust serde JSON: https://docs.rs/serde_json/latest/serde_json/

These references explain the *tooling*, not benchmark outcomes.
