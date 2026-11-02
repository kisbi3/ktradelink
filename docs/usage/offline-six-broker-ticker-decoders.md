# Offline six-broker current-price Decoder candidates

This is **not a production brokerage API client**. No real quote fetching,
HTTP, WebSocket, auth, accounts, order placement, rate-limit enforcement, or
verified source venue. It is an internal research foundation that processes
synthetic JSON response shapes documented by publishers.

## Why separate crates?

```text
Publisher response-shaped JSON (six native envelopes)
    |
    v
crates/ktradelink-decoders/
    - JSON syntax and duplicate-key validation
    - broker-specific field extraction
    - no guess about native signs or venue
    |
    v
crates/ktradelink-core/         <-- still dependency-free
    - venue/value provenance and decimal text
    |
    v
bindings/python/               <-- PyO3, thin translation
    |
    v
EXISTING Python ktradelink.models.Ticker
```

The optional private `ktradelink._native.decode_ticker_candidate` is **not**
a user-facing `fetch_ticker`. You must install the separate native wheel
locally to exercise it. The plain Python SDK and its public typed models still
work without the native extension.

## Example with a synthetic KIS-shaped response

```python
from decimal import Decimal
from ktradelink._native import decode_ticker_candidate
from ktradelink.models import Ticker

source = '{"rt_cd":"0","output":{"stck_prpr":"72000.00","acml_vol":"0"}}'
quote = decode_ticker_candidate("kis", "005930", "KRX", source)

assert type(quote) is Ticker
assert quote.last == Decimal("72000.00")
assert quote.volume == 0
assert quote.timestamp is None
assert quote.info == {}
```

The KRX value is supplied by the caller and **does not authenticate the
response's venue**. A future transport/request layer must bind symbol,
market/session, account environment and native response metadata before
claiming a working adapter. Providing JSON alone is not evidence that any
broker sent it.

## Scope and limitations

- Six broker *candidate* profiles are `kis`, `kiwoom`, `ls`, `db`,
  `toss`, `meritz`. For `ls`, this is **only the official onboarding flat
  `price` example**, not a confirmed production t1102OutBlock decoder.
- Price parsing is exact unsigned fixed-decimal text; only the LS onboarding
  demo also accepts a JSON unsigned **integer** for `price`.
- Broker output fields and wrappers are **not interchangeable**. DB `Sdpr`
  is never assigned to `previous_close`. Signed Kiwoom `cur_prc` strings
  fail until its native semantics are documented; no `abs()`.
- Toss `result` is a *list*: select the exact symbol, reject duplicates or
  wrong currency. ISO source timestamp is not converted at this phase; it is
  `None` in the normalized model until a separately validated time mapping.
- If no evidenced field is present, the corresponding value is `None`.
  A valid literal zero stays 0. Empty or malformed present fields fail rather
  than being silently replaced. Never infer bid/ask from separate endpoints.
- JSON duplicate keys anywhere, malformed response envelopes, unsupported
  venue and non-success documented status codes cause explicit field-named
  errors. Native payloads are never logged or passed through `info`.
- Rust Core is still transport-independent and Python-free; the separate
  decoder crate depends on serde/serde_json, not the other way around.
- No capability matrix item becomes `implemented`, `supported` or
  `normalized_contract_verified` based on synthetic offline tests.
- The first six *comparison* scope does not silently include Shinhan (draft PR
  #6), which has different Windows ActiveX integration questions.

See [the source/evidence ledger](../brokers/six-broker-ticker-decoders.md).
