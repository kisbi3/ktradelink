"""Deterministic synthetic messages; not exchange or broker data."""

import json


def generate_payloads(count: int) -> list[str]:
    if count < 1:
        raise ValueError("count must be positive")
    result = []
    for idx in range(count):
        value = 70_000 + idx % 30
        message = {
            "symbol": "005930" if idx % 2 == 0 else "0101N0",
            "venue": "KRX",
            "last": str(value),
            "open": str(value - 3),
            "high": str(value + 7),
            "low": str(value - 9),
            "previous_close": str(value - 2),
            "volume": idx % 10_000,
            "timestamp": None if idx % 3 == 0 else 1_793_113_200_000 + idx,
            "retrieved_at": 1_793_113_201_000 + idx,
        }
        result.append(json.dumps(message, separators=(",", ":")))
    return result
