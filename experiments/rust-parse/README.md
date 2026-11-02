# Rust vs Python current-quote parser probe

**Experiment only.** This is not a broker adapter, not an API credential
client, and not a published part of the `ktradelink` package.
All payloads are invented, deterministic, synthetic quote-shaped JSON.
The keys do NOT claim to be the wire schema of any named broker.

The Rust extension `ktl_rust_parse_probe` uses PyO3 + serde_json and
returns a private 10-element tuple. The Python reference uses `json.loads`
and returns the identical private tuple. Both paths then use the **same**
Python `row_to_ticker` function to build a public `Ticker` model.
This keeps the existing typed-only SDK contract intact.

## Reproduce

From repository root, with Rust stable / cargo and Python 3.11+:

```bash
python -m pip install -e .
python -m pip install "maturin>=1.9,<2" "pytest>=8"
python -m maturin build --release --manifest-path experiments/rust-parse/Cargo.toml --interpreter python --out /tmp/ktl-probe-wheels
python -m pip install /tmp/ktl-probe-wheels/ktl_rust_parse_probe-*.whl
python -m pytest -q experiments/rust-parse/tests
python experiments/rust-parse/benchmark.py --samples 2000 --repeats 9
```

The existing regular repository CI is unchanged. A **separate** experimental
GitHub Actions workflow builds and tests the Rust extension without making
it an installation requirement for `ktradelink`.

## Workload and reporting rules

Compare all eight variants: Python/Rust single-message parse, Python/Rust
batch parse, and the same four variants after constructing the public typed
`Ticker`. The workload is identical and pre-generated before timing.
Each Rust result is compared to Python both as a raw tuple and a Ticker.

Use release-optimized Rust, time only in-process parsing/construction,
alternate measurement order, and use the same Python interpreter, runner and
input set. Report iterations, sample size, environment, p50/p95
**per iteration**, normalized throughput and estimated microseconds/item.
These p95 values do **not** represent the latency distribution of individual
exchange messages or orders. Full snapshots of broker data and network calls
are specifically excluded.

The results are diagnostic; the benchmark does not assert that Rust must win.
The Python↔Rust boundary and Python object allocation may dominate individual
calls. A batched fast path is not necessarily usable by an existing broker.
No benchmark alone decides a production language migration.

## Safety and reproducibility limits

- No credentials, auth headers, accounts, orders, or live market data.
- This is a controlled synthetic schema, not the six brokers' actual payloads.
- The extension has its own build backend; root `pyproject.toml` remains
  setuptools and does not compile Rust.
- Version constraints are not a pinned dependency lockfile; follow-up
  reproducibility hardening will be required for a long-lived Rust package.
- GitHub shared runners have noisy CPUs; re-run, do not overfit one result.
