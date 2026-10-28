# Synthetic market-data design fixtures

These files are **invented values** for checking documented contract
invariants before any adapter exists. They are **not** captured or verified KIS
or Kiwoom responses. Do not reuse them as vendor field-mapping fixtures.

Prices are decimal strings so the tests can parse them with `Decimal`.
The daily date fixture shows KST session anchoring to previous UTC calendar
date; the order book tests show bid/ask order and zero quantity preservation.

Real provider-response contract tests must use authorized redacted samples,
reference the official field-level specification, and remain separate from
these conceptual examples.
