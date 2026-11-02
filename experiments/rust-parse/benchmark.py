"""Compare Python versus Rust on the same in-memory synthetic payloads."""

import argparse
import gc
import json
import platform
import statistics
import sys
import time
from pathlib import Path

from data import generate_payloads
from reference import python_parse_batch, python_parse_one, row_to_ticker


def percentile(values: list[int], fraction: float) -> int:
    sorted_values = sorted(values)
    index = round((len(sorted_values) - 1) * fraction)
    return sorted_values[index]


def run(samples: int, repeats: int) -> dict:
    if samples < 1 or repeats < 5:
        raise ValueError("samples must be positive and repeats must be >= 5")
    import ktl_rust_parse_probe as rust

    payloads = generate_payloads(samples)
    py_batch = python_parse_batch(payloads)
    rust_batch = rust.parse_batch_json(payloads)
    assert py_batch == rust_batch
    assert [row_to_ticker(row) for row in py_batch] == [
        row_to_ticker(row) for row in rust_batch
    ]

    tasks = {
        "python_one_parse": lambda: [python_parse_one(p) for p in payloads],
        "rust_one_parse": lambda: [rust.parse_one_json(p) for p in payloads],
        "python_batch_parse": lambda: python_parse_batch(payloads),
        "rust_batch_parse": lambda: rust.parse_batch_json(payloads),
        "python_one_to_ticker": lambda: [row_to_ticker(python_parse_one(p)) for p in payloads],
        "rust_one_to_ticker": lambda: [row_to_ticker(rust.parse_one_json(p)) for p in payloads],
        "python_batch_to_ticker": lambda: [
            row_to_ticker(row) for row in python_parse_batch(payloads)
        ],
        "rust_batch_to_ticker": lambda: [
            row_to_ticker(row) for row in rust.parse_batch_json(payloads)
        ],
    }
    measurements: dict[str, list[int]] = {name: [] for name in tasks}
    for _ in range(2):
        for task in tasks.values():
            assert len(task()) == samples
    names = list(tasks)
    for iteration in range(repeats):
        for name in (names if iteration % 2 == 0 else reversed(names)):
            gc.collect()
            start = time.perf_counter_ns()
            result = tasks[name]()
            elapsed = time.perf_counter_ns() - start
            if len(result) != samples:
                raise AssertionError("benchmark result lost samples")
            measurements[name].append(elapsed)
    metrics = {
        name: {
            "p50_iteration_ms": round(statistics.median(times) / 1e6, 4),
            "p95_iteration_ms": round(percentile(times, 0.95) / 1e6, 4),
            "p50_microseconds_per_item": round(statistics.median(times) / samples / 1e3, 4),
            "p50_items_per_second": round(samples * 1e9 / statistics.median(times), 1),
        }
        for name, times in measurements.items()
    }
    return {
        "status": "synthetic_local_microbenchmark_not_broker_latency",
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "samples_per_iteration": samples,
        "repeats": repeats,
        "payload_mean_bytes": round(sum(len(x.encode()) for x in payloads) / samples, 2),
        "precision": "p95 is across full batch iterations, NOT per-event latency p95",
        "metrics": metrics,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=2000)
    parser.add_argument("--repeats", type=int, default=9)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = run(args.samples, args.repeats)
    content = json.dumps(data, ensure_ascii=False, indent=2)
    print(content)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
