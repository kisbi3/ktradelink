# ADR 0002: Native typed models and evidence-first shared contracts

- **Status:** Accepted for the first Core Library implementation
- **Date:** 2026-11-02
- **Scope:** Public Python data contract, not broker adapter support

## Context

KTradeLink aims to unify the *actual shared semantics* of Korean broker APIs,
not invent a framework and force broker outputs to fit it. The first comparison
set is KIS, Kiwoom REST, LS, DB, Toss, and Meritz. See
[`docs/brokers/six-broker-common-surface.md`](../brokers/six-broker-common-surface.md)
for source evidence and unresolved fields.

The maintainer has no API-enabled account/credentials for the six providers.
Publisher specifications and clearly synthetic fixtures are available; live
and mock-account contract tests are **not** available yet.

## Decision

1. **Public API returns typed Python models only**, using frozen/slotted
   dataclasses for core market-data values. Do not add public `to_dict()`,
   `as_dict()`, `to_json()` or a second dictionary-returning API in v0.x.
2. Broker HTTP/JSON parsing may use Python dictionaries **internally**.
   Internal protocol representation is not the same as a public return type.
3. Keep supported common information small: symbol, selected quote venue,
   source broker, price and optional session/quote metadata. Support
   provider-specific information only after identifying its meaning.
4. A field discovered in a publisher example is a **documented candidate**,
   not proof of its actual presence in all account environments or sessions.
5. Preserve missing-versus-zero distinction and never invent timestamps.
6. Default any `info` metadata to a small, sanitized, read-only mapping.
   Exposing arbitrary raw HTTP payloads with account identifiers is forbidden.
7. No account, token, live quotation, or order transmission is required in
   the initial Core Library tests; test solely with synthetic values.
8. New contract features are added after cross-broker comparisons or
   documented conditional capabilities. Keep CCXT naming where useful, but
   do not prioritize byte-for-byte CCXT serialization.

## Limitations and revisit criteria

- A `frozen=True` dataclass protects attribute reassignment, **not**
  automatically a mutable nested object. Treat `info` specially and test it.
- Do not convert every numeric string to a positive absolute value. Broker
  field-level sign meaning must be verified separately.
- Do not enforce numeric-only six-digit stock symbols in general-purpose
  data-model constructors solely because the first two broker examples used
  them. At least one publisher documents alphanumeric KR symbols. Define
  strict instrument validation with a market master/asset-class policy later.
- No serialization promise yet. When integration needs it, propose a
  dedicated serialization contract in a separate issue/PR with reasons and
  tests, rather than adding convenience methods preemptively.
- The Phase 01 contract documents remain PROPOSED until actual field-level
  broker mapping and review evidence justify changing their status.

## Consequences

The first implementation unit can be a `Ticker` model with strict
construction-time types and independent tests. `Candle` and `OrderBook`
follow when their meaning is compared across the initial broker set.
