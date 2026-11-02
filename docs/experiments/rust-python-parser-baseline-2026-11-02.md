# Rust vs Python parser experiment — first CI measurement

- **Measured on:** 2026-11-02 (GitHub-hosted Ubuntu runner)
- **PR:** #11, code HEAD `43edf21d300ede28673601115ab03bbc9a9608ef`
- **Source:** [GitHub Actions Rust experiment run #41394580369](https://github.com/kisbi3/ktradelink/actions/runs/41394580369)
- **Status:** one **synthetic** microbenchmark run; **NOT** an approved Rust migration
- **Tests:** experimental Python/Rust equivalence suite: **29 passed** on
  Python 3.11.17 and Python 3.13.17; regular Python CI 3.11/3.12/3.13 green
- **Versions:** Rust/Cargo 1.99.1; Maturin 1.16.0; experiment references PyO3
  0.29-compatible dependency specification (full Cargo dependency resolution
  not locked in this commit)

## Controlled setup

- **Input:** 2,000 identical deterministic synthetic quote-shaped JSON
  strings per iteration; average payload **182.44 UTF-8 bytes**.
- **Sampling:** two warmup passes and nine measured repetitions per variant.
- **Metrics below:** median (`p50`) total milliseconds to process **all
  2,000 messages once**. Both implementations use the same input and make
  **no network calls**.
- **Final public output:** for `to_ticker` variants, both Python and Rust paths
  run the same Python `row_to_ticker` constructor to yield the existing,
  frozen typed `Ticker`; no new public dictionary API.
- **Noise:** shared hosted CPU / Python runtime / compiler versions mean numbers
  will vary. The `p95` produced by the script is across whole benchmark
  iterations, **not** the per-event latency distribution.

## Result: 2,000 messages / batch, median elapsed milliseconds

| Workload | Python 3.11 Python | 3.11 Rust | Rust speedup | Python 3.13 Python | 3.13 Rust | Rust speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| One-message calls, parse only | 15.8091 | 2.0275 | 7.80× | 18.9684 | 2.3667 | 8.01× |
| One bulk call, parse only | 15.7461 | 2.8683 | 5.49× | 18.9664 | 2.6488 | 7.16× |
| One-message calls, parse + `Ticker` | 35.3974 | 18.8078 | 1.88× | 44.0690 | 23.4364 | 1.88× |
| One bulk call, parse + `Ticker` | 32.9779 | 19.4823 | 1.69× | 40.3493 | 23.7545 | 1.70× |

Additional `p95` (entire 2,000-item iteration, ms):

| Workload | Py3.11 Python / Rust | Py3.13 Python / Rust |
| --- | --- | --- |
| Single parse | 18.4241 / 2.0696 | 19.1790 / 2.4392 |
| Batch parse | 16.0819 / 3.0240 | 19.2227 / 3.0115 |
| Single parse + `Ticker` | 36.2038 / 19.3279 | 45.5710 / 25.6375 |
| Batch parse + `Ticker` | 33.3852 / 19.7657 | 43.3340 / 23.9638 |

## Interpretation and risk of overclaiming

1. Rust's raw JSON parsing is substantially faster on **this controlled
   shape**. This does **not** show that a brokerage REST request (network
   RTT and provider rate limit) would improve by those factors.
2. Creating the same public Python `Ticker` objects reduces the observed
   advantage to roughly **1.7–1.9×**. Python object construction is part of
   the real user-facing cost. Therefore do NOT quote the 5–8× parsing-only
   figure as expected end-to-end SDK performance.
3. Bulk-call Rust is not automatically the fastest variant; Python↔Rust
   allocations, list/tuple creation and synthetic payload size matter.
   Real WebSocket message sizes, event rates, streams and memory pressure
   remain unmeasured.
4. The Python oracle rejects duplicate JSON keys and nonstandard numeric
   constants and does strict value type checks; the Rust serde parser
   uses deny-unknown-fields and type-safe deserialization. Benchmark
   differences depend partly on the chosen safety work and exact libraries,
   not only language implementation speed.
5. No HTTP/JSON auth, TLS, retries, source timestamp validation,
   cancellation, asynchronous scheduling, NXT/SOR handling, or broker-specific
   sign conventions are tested. The first six brokerage adapters remain
   **unimplemented**.

## Decision

**Do not migrate the production SDK yet.** Maintain Python public typed
models and a separate Rust experiment. Before proposing a production engine:
repeat on representative sanitized vendor messages when available, benchmark
high-rate event ingestion and order-book updates, evaluate memory and single
event tail latency separately, test Windows/macOS packaging, constrain or
lock tool dependencies, and have independent Gemini review of benchmark
methodology plus human architecture approval.
