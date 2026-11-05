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
| `ls` | [LS API guide t1102 REST detail](https://openapi.ls-sec.co.kr/apiservice) (retrieved 2026-11-05, see [ledger](live-auth-transport-gates-2026-11-05.md)) | `t1102OutBlock` object; **required** root `rsp_cd` `00000` and echoed `shcode` | `price` (unsigned; direction in `sign`) | `volume` | `open`/`high`/`low` are `0` before the first trade in the publisher example, so they are **not mapped**; no venue field in the response |
| `db` | [Official DB domestic quote Python sample](https://openapi.dbsec.co.kr/testbed-sample), `PRICE` | `Out` object; **required** root `rsp_cd`, exactly `00000` ([SDK `response.py` L78–85](https://github.com/DBsecurities/dbsec-open-api/blob/564b5100b80a3a785468b77ee8c0557f6edcfdeb/dbsec_sdk/response.py#L78-L85), ADR 0015) | `Prpr` | `Oprc`, `Hprc`, `Lprc` | `Sdpr` is a **reference/base price**, not proven previous session close; no volume in publisher example |
| `toss` | [Server-owned canonical OpenAPI 3.1 v1.2.28](https://openapi.tossinvest.com/openapi-docs/latest/openapi.json), `GET /api/v1/prices` | `result` array, match **exact requested symbol**, `currency=KRW` | `lastPrice` | `symbol`, `currency` | PriceResponse has **no volume/OHLC**; `timestamp` is ISO offset text; conversion deferred until semantics/coverage verified |
| `meritz` | [Official current-price Python sample](https://openapi.imeritz.com/samplecode-py), `GET /market/v1/prices` | `data` object | `stck_prpr` | `oprc`, `hprc`, `lprc`, `acml_vol` | Native event clock, `previous_close`, market-wide aggregation, validated response-code taxonomy beyond published example |

The six **documented candidate** profiles do not mean six production-ready
adapters. LS now follows the published t1102 REST block (ADR 0010), but its
gateway behaviour is still unverified. Unverified endpoints must never be
claimed as working.

## Meritz status-code evidence and endpoint-specific guard

Source: [Official Meritz Python sample](https://openapi.imeritz.com/samplecode-py),
accessed 2026-11-02. Its general-purpose helper lists codes
0000, 0001, 5762, 5766, 5820 and 5822 as acceptable across different
API families. This list does NOT assert that those values signify
success for the specific current-price GET /market/v1/prices endpoint.

The same official page identifies 0001 as an order receipt, 5762 as
order-history continuation, 5766 as completion of account/order history
queries, and 5820 as empty order history. It does NOT establish a
current-price meaning for 5822. These codes cannot be blindly
accepted in the ticker decoder.

For the constrained, synthetic current-price decoder, only the
conservative TEXTUAL candidate rsp_cd="0000" is accepted if present.
The publisher's market-data order-book example reports this code.
However, the current-price sample does not present a raw success
envelope proving that 0000 is the ONLY current-price success code.
Exact GET /market/v1/prices status semantics remain UNVERIFIED.
A production adapter must verify its own endpoint-specific contract.
A missing Meritz status is still accepted, for synthetic examples
only. That is not permission to ignore an actual HTTP or provider error
status. LS and DB no longer accept a missing status: their root `rsp_cd`
is **required** (ADR 0010, ADR 0015).

## Shared input and error boundaries after Gemini review

- Caller symbol is checked for nonempty ASCII graphic characters
  before parsing ANY JSON for every one of the six broker candidates.
  The error is field symbol, kind CoreValidation in every case.
- Missing/null required Toss symbol/currency string fields are
  MissingRequired; present number or boolean is InvalidField.
- Optional Kiwoom stk_cd and LS shcode may be absent in an offline
  sample. If present, null/number/bool are InvalidField; a well-formed
  mismatched string is AmbiguousSymbol.
- Status values are broker-specific: KIS rt_cd string "0", Kiwoom
  return_code numeric integer 0, LS and DB rsp_cd string "00000",
  Meritz rsp_cd string "0000" as limited above.
- KIS, Kiwoom and Meritz still accept a missing status, for synthetic
  examples only. A present null or wrong JSON type fails SourceStatus.
- LS and DB require the root rsp_cd (ADR 0010, ADR 0015). A missing or
  null rsp_cd fails MissingRequired. Any other value or type fails
  SourceStatus.
- Toss has no status field in the decoder. Toss is listed with the
  brokers that tolerate a missing status in ADR 0015.
- The upper input-size bound is inclusive: 1,048,576 UTF-8 bytes
  can decode; 1,048,577 bytes rejects before JSON parsing. This
  is an application safety limit, NOT a broker publisher limit.
- LS t1102 `price` accepts an unsigned JSON integer or unsigned
  fixed-decimal string; a negative JSON integer fails. The flat onboarding
  demo shape is no longer accepted.
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
- LS: the t1102 output block is now documented (ADR 0010); verify gateway
  acceptance, `rsp_cd` universe, the meaning of `0` OHLC values and NXT/
  integrated (`exchgubun` N/U) semantics before any wider support.
- DB: verify `rsp_cd` universe, market-specific response semantics,
  reference/base vs closing price and daily volume availability.
- Toss: confirm whether `GET /api/v1/prices` for Korean symbols is KRX-only
  vs consolidated; implement validated offset-aware `timestamp` conversion
  in a separate change, and confirm multi-symbol return uniqueness.
- Meritz: confirm success code families, price field optionality and
  market-specific KRX/NXT/composite flags for each real call.

This document tracks **research and offline parsing** only, not live
market-data compatibility. Related: Issues #2, #5, #9, #12, #14.
