# Six-broker ticker decoder evidence ledger (offline candidates)

- Collected/accessed: **2026-11-02**.
- Scope: first read-only **ticker decoding** pass for **KIS, Kiwoom REST, LS, DB,
  Toss, Meritz** together.
- Stage: **offline_documented_candidate**, **NOT** implemented/verified brokerage
  `fetch_ticker`. No credentials or authorized raw brokerage response fixtures.
- Transport, HTTP request building, authentication, order placement, live
  entitlement, source venue verification, individual trades and WebSocket are
  **not included**.
- We implement only field names/outer structures substantiated by the publisher
  examples below. Missing source facts remain missing, not guessed.

## Broker-owned evidence and deliberately narrow conversion

| Broker ID | Publisher current-price evidence | Candidate response shape | Exact last field | Other evidenced fields | Deliberately NOT inferred |
| --- | --- | --- | --- | --- | --- |
| `kis` | [KIS domestic stock quote example](https://github.com/koreainvestment/open-trading-api/blob/main/examples_llm/domestic_stock/inquire_price/chk_inquire_price.py) (FHKST01010100) | `output` object | `stck_prpr` | `stck_oprc`, `stck_hgpr`, `stck_lwpr`, `acml_vol` | Event timestamp; KIS response may not specify confirmed venue for every TR |
| `kiwoom` | [Kiwoom REST ka10001 publisher example](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_info.py) | Root object | `cur_prc` | `open_pric`, `high_pric`, `low_pric`, `trde_qty`, optional `stk_cd` | **Signed price semantics** — reject signs until documented at field level |
| `ls` | [Official LS onboarding `GET /stock/market-data` example](https://openapi.ls-sec.co.kr/howto-use) | **Flat onboarding demo only** | `price` | optional `shcode` if supplied | Does **NOT** establish actual `t1102OutBlock` wire envelope, depth, unit, time or volume |
| `db` | [Official DB domestic quote Python sample](https://openapi.dbsec.co.kr/testbed-sample), `PRICE` | `Out` object and `rsp_cd` success code `00000` | `Prpr` | `Oprc`, `Hprc`, `Lprc` | `Sdpr` is a **reference/base price**, not proven previous session close; no volume in publisher example |
| `toss` | [Server-owned canonical OpenAPI 3.1 v1.2.28](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json), `GET /api/v1/prices` | `result` array, match **exact requested symbol**, `currency=KRW` | `lastPrice` | `symbol`, `currency` | PriceResponse has **no volume/OHLC**; `timestamp` is ISO offset text; conversion deferred until semantics/coverage verified |
| `meritz` | [Official current-price Python sample](https://openapi.imeritz.com/samplecode-py), `GET /market/v1/prices` | `data` object | `stck_prpr` | `oprc`, `hprc`, `lprc`, `acml_vol` | Native event clock, `previous_close`, market-wide aggregation, validated response-code taxonomy beyond published example |

The six **documented candidate** profiles do not mean six production-ready
adapters. LS is specifically **onboarding-demo-only**. A production LS `t1102`
profile requires verifying the official TR-specific response block. Unverified
endpoints must never be claimed as working.

## Decoder semantics and provenance policy

1. **The caller explicitly supplies** `symbol` and `venue="KRX"`; the offline
   decoder does **not establish** those from native responses except Toss
   `result[].symbol` (and optional Kiwoom/LS native identifiers) which are
   matched to the caller to avoid silent misassociation. The eventual request
   layer MUST validate actual market/venue scope and bind the response to the
   exact submitted request before making a real `fetch_ticker` claim.
2. Only `KRX` is permitted for these candidate tests. Do **not** silently
   fallback from NXT or broker composite. `KRX` here is the caller's
   **offline context**, **not an independently authenticated exchange label**.
3. Input is a JSON **string** supplied by tests or future trusted transport.
   Duplicate JSON keys anywhere in the payload, invalid JSON, ambiguous match,
   malformed envelopes, incompatible status and malformed field types raise
   explicit errors. **No exception means that a price was actually fetched.**
4. Price fields become exact **unsigned fixed-decimal text** via
   `ktradelink_core::Price::parse`, and finally Python `Decimal`, never
   `f64`. Native signed price or directional metadata is **not**
   converted using `abs` without provider-verified meaning.
5. `None` means field absent/null; **empty string**, negative quantities,
   floating-point quantities and malformed data are **errors**, never 0.
   A reported zero is kept literal; whether it means halt or sentinel is
   **unverified** and must be examined with provider evidence before production.
6. `bid`, `ask`, `previous_close`, `timestamp`, `retrieved_at` and
   `scope_description` are **None** unless separately supported by evidence.
   There is no hidden request for a bid/ask, guessed UTC time, request-receive
   time, calendar or reference price.
7. `info` is always **empty**. Never propagate raw provider JSON (which
   could contain tokens, account details, headers or unusual metadata). No
   unknown input fields are serialized into public models, errors or logs.
8. Reject oversized input and non-unique requested stock responses; do not
   quietly select the first result in a batch.
9. Validation is based on deterministic, invented **synthetic** examples matching
   the documented **field names**. No real-data sample has been recorded.
10. `Supported` capability flags and published `fetch_ticker` API remain
   **false/unimplemented**. A declared decoder *candidate* is not a verified
   broker adapter. Link supporting official URLs and access date on each
   provider when evidence changes.

## Explicit next evidence questions

- KIS: response status, field formats, zero prices under trading halts,
  per-venue and per-session provenance, optional previous close existence.
- Kiwoom: verify the *native* `cur_prc` sign convention, market-qualified
  `stk_cd`, volume meaning and exchange/session coverage before allowing
  signed prices; do not apply unconditional absolute value.
- LS: fetch publisher's current **t1102 TR output block** and verify its real
  wrapper; onboarding demo is **not** sufficient for real-t1102 adapters.
- DB: verify `rsp_cd` universe, market-specific response semantics,
  reference/base vs closing price and daily volume availability.
- Toss: confirm whether `GET /api/v1/prices` for Korean symbols is KRX-only
  vs consolidated; implement validated offset-aware `timestamp` conversion
  in a separate change, and confirm multi-symbol return uniqueness.
- Meritz: confirm success code families, price field optionality and
  market-specific KRX/NXT/composite flags for each real call.

This document tracks **research and offline parsing** only, not live
market-data compatibility. Related: Issues #2, #5, #9, #12, #14.
