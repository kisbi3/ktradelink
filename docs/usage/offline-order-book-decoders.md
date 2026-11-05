# Offline order-book (호가) decoder candidates

This is **not** `fetch_order_book`. Nothing here sends a request, reads a
credential or touches an account. It parses JSON **you** supply, shaped like
the publisher examples pinned in
[the evidence ledger](../brokers/order-book-evidence-2026-11-05.md), into the
existing `ktradelink.models.OrderBook`. Design: [ADR 0014](../decisions/0014-offline-order-book-candidates.md).

| Broker | Source shape | Decoder | Offline plan |
| --- | --- | --- | --- |
| `kis` | `FHKST01010200` `output1`, string values | yes | yes (live/paper) |
| `kiwoom` | `ka10004` root, string values, **unsigned prices only** | yes | yes (live/mock) |
| `ls` | `t1101` `t1101OutBlock`, JSON integers, `shcode` echo | yes | **no**: t1101 has no venue selector |
| `db`, `toss`, `meritz` | — | `UnsupportedBroker` | no |

## Requirements

The decoder lives in the optional native extension (contract version 2):

```bash
python -m pip install -e ".[dev]" "maturin==1.16.0"
python -m maturin develop --release --manifest-path bindings/python/Cargo.toml
```

## Decode a synthetic payload

```python
from pathlib import Path
from ktradelink._native import decode_order_book_candidate

text = Path("tests/fixtures/order_book/kis-fhkst01010200-synthetic.json").read_text()
book = decode_order_book_candidate("kis", "005930", "KRX", text, limit=5)
book.bids[0]        # OrderBookLevel(price=Decimal('70000'), quantity=12)
len(book.asks)      # 5
book.timestamp      # None: no source documents an absolute event time
```

## Plan, then decode a caller-supplied response

```python
from ktradelink._order_book_plan import (
    decode_offline_order_book_response, plan_order_book_request,
)

plan = plan_order_book_request("kiwoom", "005930", venue="KRX", environment="live")
plan.path, plan.json_body   # ('/api/dostk/mrkcond', '{"stk_cd":"005930"}')
book = decode_offline_order_book_response(plan, http_status=200, json_text=text)
```

`plan_order_book_request("ls", ...)` raises `QuotePlanUnavailable`.
A tampered plan, a non-2xx status or a non-text body is rejected before the
decoder runs.

## What the decoder guarantees

- Bids are strictly descending and asks strictly ascending, exactly as the
  source sent them. Unordered or duplicate levels are errors and are never
  sorted. Crossed and locked books are kept.
- A level with a positive price keeps its quantity, even `0`.
- A zero price is never interpreted, because no publisher documents how an
  empty rank is encoded. Price `0` with quantity `0` is
  `UnverifiedEmptyLevel`; a zero price with a quantity is `InvalidPrice`.
  Neither is dropped, so a thin book with fewer than 10 quoted ranks per
  side currently fails, even with a smaller `limit`.
- Missing, `null`, blank, signed or wrongly typed fields are errors. They
  are never read as an empty level.
- `limit` is per side, `1..10`. Above 10 it raises `DepthExceeded` and is
  never clamped. Ordering is checked on the full book first.
- A status is required: KIS `rt_cd "0"`, Kiwoom `return_code 0`, LS
  `rsp_cd "00000"`.
- Error messages name a field and a kind only. They never include values.

## What it does not tell you

- That the JSON came from a broker, or which venue's book it is. `KRX` is
  the caller's context. KIS and Kiwoom responses do not echo the symbol.
- Real gateway types, empty-rank encoding or Kiwoom sign semantics. All are
  open questions in the ledger.
