# ADR 0007 — Six-broker quote request planning before live transport

- Date: 2026-11-02
- Status: **Accepted as a private offline request-planning foundation**.
- Parent decisions: ADR 0005 (Rust Core + Python bindings) and ADR 0006
  (six brokers together by feature, never "KIS fully then Kiwoom fully").
- No production adapter is implemented or verified by this ADR.

## Decision

Implement one **private Python request planner** covering domestic read-only
quote request shapes of KIS, Kiwoom REST, LS onboarding, DB, Toss and Meritz.
Keep JSON/quote normalization in the already merged **pure Rust decoder**
library and immutable Python `Ticker` contract. HTTP/network latency is a
separate consideration and does **not** justify prematurely introducing
native TLS/HTTP dependencies into `ktradelink-core`.

The planner describes **only nonsecret, evidence-backed request inputs**
such as HTTP method, fixed official origin, path, safe query/body values,
public TR IDs and required authentication HEADER NAMES. It carries **no**
App Keys, App Secrets, OAuth bearer tokens, account numbers, machine MAC
values, mutable credential dictionaries or loggable credential material.
Credential exchange, token lifecycle, refresh, injection and HTTP sending
are **not included**. No GET/POST is executed in this change.

The future flow is deliberately separated:

```text
user broker + symbol + venue -> offline RequestPlan (this PR)
    -> validated account-bound CredentialProvider (NOT implemented)
    -> guarded authenticated TLS transport (NOT implemented)
    -> HTTP/provider error validation (only mock guard now)
    -> Rust decoder candidate (already merged)
    -> the SAME frozen/slotted Python Ticker (already merged)
```

## Provider boundaries

- A public `Ticker` accepts alphanumeric six-character symbols as a **value
  object**. That does not establish broker route compatibility. Route
  construction uses source-evidenced local identifier formats: the five
  numeric-only quote examples use six ASCII digits; Toss KR examples can
  use ASCII alphanumeric six characters (`0101N0`).
- Only explicitly supplied `venue="KRX"` is supported by these **offline
  examples**, not proof of an actual exchange-specific response. Reject NXT
  and BROKER_COMPOSITE instead of fallback.
- Production and simulation environments must never silently mix. Official
  live/paper base URLs are used only where independently documented (KIS,
  Kiwoom); others **reject paper** rather than inventing an endpoint.
- KIS and Kiwoom quote requests differ in verb, path, body, public headers.
  DB adds the evidenced `A` symbol prefix inside a nested `In` body.
  Toss has a `symbols` query even for one symbol. Meritz uses
  `mrkt_div_code=J` plus `iscd`. LS uses **only** an official beginner
  walkthrough path, **NOT** verified t1102.
- Never take an arbitrary origin/host, URL path, query mapping, public
  header, auth token or body fragment from user input. The planner constructs
  fixed publisher-derived templates only; symbol validation precedes all
  string interpolation and JSON encoding.
- Quote-specific HTTP status and broker error classification needs an
  authoritative, sanitized authenticated fixture. A **mock-only guard**
  rejects non-2xx statuses and invalid status types without returning raw
  error response text. We do not auto retry 401/429, refresh or replay
  orders, guess rate limits, or silently map broker errors.
- Do not copy the DB provider's documented legacy sample that places
  app credentials in an URL query and sets `verify=False`. Before any DB
  live token flow, obtain a validated TLS-checked, non-leaking contract.
- Do not auto-discover the host's MAC address for Meritz. Its documented
  `mac_address` header is recorded as a missing credential-context
  prerequisite; no value is generated, stored or forwarded here.
- Market-data requests do not add Toss `X-Tossinvest-Account`: official
  spec requires it for account/order operations, **not prices**.
- No credentials in repositories, test snapshots, CI logs or Gemini review.
- All output is private immutable typed plan records, never public dict
  serializers; `ktradelink.models.Ticker` remains unchanged.

## Release gate

1. Confirm all six source templates/credential metadata against current
   **official source** and review ambiguities independently.
2. Offline tests, Ruff, CPython 3.11/3.12/3.13, clean installed-wheel check.
3. Gemini fixed-SHA review and explicit human authorization before merge.
4. A *separate* future PR may introduce a credential provider and real HTTPS
   transport after account, paper/real access, TLS and response semantics are
   independently verified. No network tests or live orders in CI.

See [request/auth evidence ledger](../brokers/six-broker-quote-request-auth.md).
