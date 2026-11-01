# Initial broker comparison scope (seven brokers)

- **Status:** Scope decision / research targets, **not implemented broker support**
- **Date:** 2026-11-02
- **Tracking:** [Issue #5](https://github.com/kisbi3/ktradelink/issues/5)
- **Prior specification:** [Issue #2](https://github.com/kisbi3/ktradelink/issues/2)
  and [Phase 01 proposal](../specifications/market-data-v0.1-draft.md)

## Scope decision

KTradeLink's initial broker **comparison set** contains seven firms. The
objective is to discover semantically equivalent market-data behavior from
publisher evidence before generalizing the Python interface.

| Broker | First evidence track | Initial classification |
| --- | --- | --- |
| Korea Investment & Securities (KIS) | REST examples and API documentation | Publisher-documented market-data candidates; adapter not implemented |
| Kiwoom Securities | REST developer API (not legacy OpenAPI+) | Publisher-documented market-data candidates; adapter not implemented |
| LS Securities | Published Open API / REST | Research target; adapter not implemented; field-level review pending |
| DB Securities | Published Open API / REST | Research target; adapter not implemented; field-level review pending |
| Toss Securities | Published trading Open API | Research target; adapter not implemented; field-level review pending |
| Meritz Securities | Published trading Open API | Research target; adapter not implemented; field-level review pending |
| **Shinhan Securities** | **Shinhan i indi — Windows ActiveX component**; Shinhan Financial Group Open API Market is a *separate* channel | **Included in comparisons; Windows-specific adapter feasibility pending. Public personal-use REST stock trading interface unverified.** |

These are proposed comparison/integration targets, **not seven supported
brokers**. There is no production-ready KTradeLink adapter today. No quote,
order-book, history, balance or order capability may be marked supported until
its native field mappings and contract tests are completed.

## Shinhan source evidence and limitations

Publisher-owned sources (checked 2026-11-02):

- [Shinhan Securities — Shinhan i indi product, usage and downloads](https://www.shinhansec.com/siw/customer-center/channel/channel_homeTrading-indi/contents.do)
- [Shinhan Securities — Shinhan i indi FAQ](https://www.shinhansec.com/siw/customer-center/channel/channel_homeTrading-indi_faq/contents.do)
- [Shinhan Financial Group Open API Market — service directory](https://openapi.shinhan.com/service)
- [Shinhan Financial Group Open API Market — partnership procedure](https://openapi.shinhan.com/portal-info)

The securities publisher describes i indi as an **ActiveX component based**
system exposing real-time and historical securities data with application
examples (including Python). Use requires the prescribed account/ID,
agreement and installed software. This is a **Windows-oriented installed
component**, not an ordinary REST service that a Linux cloud CI job can call.

The Shinhan Financial Group Open API Market advertises securities-related
investment information and partnership APIs. **Do not equate these listings**
with a documented individual developer stock quote/order REST interface.
Such an API may exist behind a separate eligibility/partnership process,
but it was **not verified from public documentation** in this review.

Shinhan candidate capability state (documentary research only):
- `transport.i_indi = windows_activex_documented_candidate`
- `transport.public_personal_rest_trading = unverified`
- `fetch_ticker`, `fetch_ohlcv`, `fetch_order_book` = `unverified`
  within KTradeLink (even if vendor product pages mention corresponding data)
- `balance` and `order` = out of the initial read-only phase; permissions,
  native interfaces and safety must be independently verified.

If an i indi implementation is pursued, keep it in an **optional,
Windows-specific adapter** with OS-gated tests and explicit dependencies.
No Windows ActiveX requirement may leak into the importable platform-neutral
core. A cloud-hosted Python SDK cannot transparently operate a local ActiveX
component without an explicitly designed, separately secured bridge; **do not
promise such a bridge or construct a hidden service**.

## Common-ground-first implementation protocol

1. Build a **seven-broker capability/evidence matrix** from official sources,
   with broker transport, eligibility and market-data usage rights. Distinguish
   `documented_candidate`, `unverified`, `conditional`, `unsupported`,
   and `implemented_and_contract_tested`.
2. Compare **meaning** of native current-price, day-bar and order-book fields:
   instrument/venue/source, trading session, event time vs retrieval time,
   Decimal sign/missing handling, adjustment, pagination and quote depth.
3. Extract the smallest semantically sound common interface; preserve
   vendor-only features behind an explicit native extension, and raise clear
   exceptions where features cannot be mapped reliably.
4. Implement independent adapter modules and tests in small meaningful
   commits, not phase-end batches. Portable REST adapters and a possible
   optional Windows adapter have separate integration acceptance gates.
5. Run isolated contract tests, have Gemini Web independently review a pinned
   commit and its official references, and require human approval before
   non-squash merge.

## Initial implementation priority

**Comparison:** all seven brokers from day one.

**First code:** a transport-neutral common ticker contract, followed by
daily OHLCV and order book, each with a real broker-by-broker capability
declaration. Build the REST integrations where documented and verifiable.
Shinhan stays in scope for API discovery and future conditional adapter
implementation, but it must **not block** portable integrations when
Windows/partnership restrictions are unresolved.

**Account/orders:** later phases, following explicit safety and entitlement
verification.

This scope document does **not** rewrite the already-merged KIS/Kiwoom
`capability-matrix-v0.1.json`. That machine-readable matrix intentionally
tracks only its original two documented candidates and still lists **no
implemented capabilities**. Expand the matrix format once seven-broker
source mappings and transport requirements have been independently reviewed.
