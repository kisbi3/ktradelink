# Offline six-broker quote request and authorization requirements

**Private developer research module**: `ktradelink._request_plan`. It is NOT
a live broker client. This page covers the same six initial domestic-market
brokers as PR #15: KIS, Kiwoom REST, LS, DB, Toss and Meritz.

## Why the new layer?

An API call has TWO different parts:

1. **What to ask**: which host and path, GET vs POST, parameters and
   public TR/API-ID header. These are documented and can be tested
   **without anyone's credentials**.
2. **Who is asking**: valid app credentials, bearer token, account/device
   context, token expiry, TLS server, entitlement and rate limiting.
   Those are *not* implemented or tested yet.

This change constructs (1) and describes the **names** of the requirements
for (2). It does NOT issue a token, discover a MAC, connect to the internet,
send any quote request, or imply verified per-market results.

## Private Python example — no actual API request

```python
from ktradelink._request_plan import (
    authentication_requirements,
    plan_ticker_request,
)

kis = plan_ticker_request(
    "kis", "005930", venue="KRX", environment="live"
)
assert kis.method == "GET"
assert kis.path == "/uapi/domestic-stock/v1/quotations/inquire-price"
assert ("tr_id", "FHKST01010100") in kis.public_headers
assert kis.query == (
    ("fid_cond_mrkt_div_code", "J"),
    ("fid_input_iscd", "005930"),
)
assert kis.transport_implemented is False

db = plan_ticker_request(
    "db", "005930", venue="KRX", environment="live"
)
assert db.method == "POST"
# db.json_body is the publisher-sample nested JSON body.

meritz_auth = authentication_requirements(
    "meritz", environment="live"
)
assert "mac_address" in meritz_auth.quote_header_names
assert meritz_auth.token_exchange_implemented is False
```

The `environment="live"` option selects the **documented production host
string**, not a live execution. These objects are immutable and only contain
nonsecret fields. You cannot set a token or arbitrary HTTP host through the
API. Symbols are validated locally to prevent request-line/header/JSON
injection. `venue="KRX"` is a caller constraint, not proof of the
broker-side exchange route.

## Provider-specific differences (source-evidence only)

| Broker | Offline quote request | Credential requirements description |
| --- | --- | --- |
| KIS | GET + KRX `J` + `fid_input_iscd`, `tr_id` | Bearer plus `appkey` / `appsecret` |
| Kiwoom | POST JSON `stk_cd`, `api-id` | Bearer, separate real/paper host labels |
| LS | POST t1102 `t1102InBlock` (`shcode`, `exchgubun=K`), `tr_cd` | Bearer; t1102 from the publisher API guide, gateway unverified |
| DB | POST nested `In` (`InputCondMrktDivCode=J`, bare six-digit `InputIscd1`), `cont_yn=N` | Bearer; form token body from the API guide and official SDK (ADR 0015); the testbed's URL-query sample is **unsafe**, do not replicate |
| Toss | GET `symbols` query | Bearer, **NO account header** for public market quote |
| Meritz | GET `mrkt_div_code=J`, `iscd` | Bearer plus required `mac_address` |

[Official-source endpoint and auth ledger](../brokers/six-broker-quote-request-auth.md).

For an illustrative **synthetic-only** response, a separate private function
can check a supplied HTTP status and then reuse the existing optional Rust
decoder. This makes the whole path executable under a fake response:

```python
from ktradelink._request_plan import (
    decode_offline_quote_response,
    plan_ticker_request,
)

plan = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
synthetic_json = '{"rt_cd":"0","output":{"stck_prpr":"72000.00"}}'
quote = decode_offline_quote_response(
    plan, http_status=200, json_text=synthetic_json
)
assert str(quote.last) == "72000.00"
```

The last snippet requires the separately installed native extension.
It does not prove either `http_status=200` or `synthetic_json` came from
KIS. If the extension is absent, no Python-only fallback decoder is
silently substituted. Response bodies, tokens and provider metadata are
never logged or inserted into `Ticker.info`.

## Security and production gates

- Never commit credentials or copy actual API keys/token values into tests,
  review packets, source code, URLs, exceptions or standard logs.
- No `requests.post`, `urllib`, Rust HTTP client, socket, `verify=False`,
  token refresh, automatic retry or public `fetch_ticker` is implemented.
- Only GET / quote-style POST templates appear; absolutely no orders.
- KIS/ Kiwoom paper host strings are documented; for other four providers
  paper mode fails loudly instead of falling back to a live host.
- Only KRX input is accepted. Special KRX symbols accepted by the public
  `Ticker` value model do not automatically become valid provider query
  symbols. Here only Toss's evidenced six-character alphanumeric style is
  accepted; all five others use the conservative six-ASCII-digit example.
- DB's older testbed token sample includes URL-query credential fields and
  disables TLS validation. It is never copied. The API guide token detail and
  the official SDK at a pinned commit send a form body with TLS verification
  on; that is the only DB token shape the private transport builds (ADR 0015).
  The testbed's `A`-prefixed quote code was also replaced by the guide's bare
  six-digit code.
- Meritz's mandatory `mac_address` header is a **requirement name only**.
  We never call `uuid.getnode` or probe the system to collect it.
- A fake successful HTTP status does not prove the broker's API-level
  success code, KRX/NXT provenance, time zone, live rate limits or entitlement.
- Separate future work: actual secret/provider storage, token validity and
  refresh, TLS transport, status/error taxonomy, per-broker source/venue
  validation, repeatable sanitized fixtures, and cautious live account
  verification. Explicit maintainer approval is needed before any broker
  requests are issued in an integration test.

This document is intentionally scoped to offline templates. Keep the
existing optional native Rust parser, public `Ticker` API, and capability
matrix untouched.
