# ADR 0006: Implement ticker decoders by common feature across six brokers

- Date: 2026-11-02
- Status: **Accepted as a narrow accountless experiment**, **not production
  broker support**.
- Base: PR #13 Rust Core + Python typed-model foundation.

## Choice

Advance all six initial securities brokers together on the **same ticker
function** rather than completing all features of KIS, then Kiwoom, etc.
Keep broker-specific logic isolated while reusing the pure Rust
`ktradelink-core` contract and optional Python `Ticker` conversion.

Introduce a dedicated `ktradelink-decoders` Rust crate. Keep it separate from
the dependency-free `ktradelink-core` crate. It parses publisher-evidenced
JSON shapes into `CoreTicker` using strictly checked source fields. The
PyO3 boundary returns the existing `ktradelink.models.Ticker`, never a
dictionary. Python API remains **private** until six-broker semantics and
request/transport contracts are externally verified.

## Constraints

- Six targets: KIS, Kiwoom REST, LS, DB, Toss and Meritz. Shinhan i indi is
  discussed separately in PR #6 and Issue #5; no implicit seventh broker.
- All tests synthetic, no keys, no account, no auth/HTTP/WS/order.
- LS onboarding/demo response is not assumed equal to `t1102` output.
- Signed Kiwoom price semantics and other unknown fields cause explicit
  failures, not guessed transformations.
- No invalid KRX/NXT/BROKER_COMPOSITE fallback; caller's offline venue context
  is not proof of real-market quote provenance.
- Unknown fields cannot flow to `info` or errors.
- No promotion to `supported` in capabilities while accountless.
- Preserve small atomic commits and Gemini independent review before merger.

See [broker evidence ledger](../brokers/six-broker-ticker-decoders.md).
