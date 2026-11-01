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

The Ticker fixture intentionally has `bid=null` and `ask=null`: no implicit
second book request is allowed. It distinguishes `last` from
`previous_close`, and does not include an ambiguous `Ticker.close` field.
All three model fixtures are checked against
`docs/specifications/normalized-models-v0.1.json`, which in turn is checked
against the required/optional-key table in the Markdown proposal.
