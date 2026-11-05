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
  `toss`, `meritz`. For `ls`, this is the published t1102 `t1102OutBlock`
  shape (ADR 0010), not a gateway-verified decoder.
- Price parsing is exact unsigned fixed-decimal text; only LS t1102 also
  accepts a JSON unsigned **integer** for `price`.
- Broker output fields and wrappers are **not interchangeable**. DB `Sdpr`
  is never assigned to `previous_close`. Signed Kiwoom `cur_prc` strings
  fail until its native semantics are documented; no `abs()`.
- Toss `result` is a *list*: select the exact symbol, reject duplicates or
  wrong currency. ISO source timestamp is not converted at this phase; it is
  `None` in the normalized model until a separately validated time mapping.
- If no evidenced field is present, the corresponding value is `None`.
  A valid literal zero stays 0. Empty or malformed present fields fail rather
  than being silently replaced. Never infer bid/ask from separate endpoints.
- Caller symbol is validated before JSON parsing in ALL six profiles.
  Toss required symbol/currency fields distinguish missing/null from
  malformed type; optional Kiwoom/LS identifiers distinguish wrong type
  from an actual string mismatch. The one-megabyte JSON limit is
  inclusive, with an explicit exact-boundary test.
- JSON duplicate keys anywhere, malformed response envelopes, unsupported
  venue and non-success documented status codes cause explicit field-named
  errors. When a status is present, its JSON type and success value must
  match that broker: KIS text "0", Kiwoom integer 0, DB text "00000",
  Meritz text "0000" only (limited offline candidate, actual quote
  success status needs real-provider verification). The official Meritz
  general OK_CODES list mixes order/history/market API families and must
  NOT be used wholesale as ticker success. Native payloads are never
  logged or passed through `info`.
- Rust Core is still transport-independent and Python-free; the separate
  decoder crate depends on serde/serde_json, not the other way around.
- No capability matrix item becomes `implemented`, `supported` or
  `normalized_contract_verified` based on synthetic offline tests.
- The first six *comparison* scope does not silently include Shinhan (draft PR
  #6), which has different Windows ActiveX integration questions.

See [the source/evidence ledger](../brokers/six-broker-ticker-decoders.md).
