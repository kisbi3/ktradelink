# Contributing to KTradeLink

Thank you for helping unify Korean securities broker APIs.

## Workflow

1. Discuss a user-facing interface change in an issue or specification draft.
2. Create a focused branch (`feat/...`, `fix/...`, or `docs/...`).
3. Implement one complete, testable change at a time and **commit immediately**.
4. Run `python -m pytest -q` and `python -m ruff check .` locally or in an
   equivalent cloud environment.
5. Open a PR that describes the behavior, tests, official broker-doc evidence,
   and changes to the capability matrix.
6. Obtain independent review for broker-specific parsing and all order paths.
7. The maintainer merges after CI and reviews pass; preserve atomic commits.

Use Conventional Commits:

```text
feat(kis): normalize domestic-equity ticker
fix(core): reject unsupported venues
test(kiwoom): cover missing market price
docs(spec): clarify ticker timestamps
ci: enforce Python lint and tests
```

## New broker adapters

Broker contributions should provide the official documentation links, supported
capability declaration, sanitized response fixtures, normalization examples,
and failure-mode tests. Do not commit credentials or personal financial data.

## Current state

The package is pre-alpha and deliberately exposes no functional broker API yet.
See `docs/specifications/` for draft designs before coding to them.
