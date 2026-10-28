# ADR 0001: Core scope and source-of-truth policy

- **Status:** Accepted for project bootstrap; subject to later review
- **Date:** 2026-10-28

## Context

Korean securities brokers expose distinct API shapes. KTradeLink aims to offer
one Python interface without pretending that all brokers have identical
features or market-data rights.

## Decision

1. Build an **importable Python SDK** as the primary product, not a hosted
   multi-broker platform or API gateway.
2. Start from **KIS and Kiwoom** and focus on domestic-equity market-data
   methods before account/order operations.
3. Keep broker-specific adapters separate from common models and transports.
4. Use explicit capability discovery and an escape hatch for broker-specific
   functionality once the API contract is defined.
5. Treat GitHub source, decisions, issues, and tests as the canonical record.
6. Do not implement real order routing before a dedicated safety review.

## Consequences

- Broker support can grow without centralizing credentials.
- Cross-broker equivalence depends on documented semantics and tests, not
  identical method names alone.
- Interface details (such as symbol encoding, venue selection and time units)
  remain open until an independent specification review.
