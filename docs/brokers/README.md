# Broker evidence and verification status

These files record **publisher documentation evidence**, not functional
KTradeLink broker support. Six-provider offline decoder candidates were
merged in PR #15. An offline request/auth-plan foundation is proposed next,
but NO authenticated network fetch_ticker adapter is implemented or
live-tested.

- [KIS market-data evidence](kis-market-data.md)
- [Kiwoom REST market-data evidence](kiwoom-market-data.md)
- [Original six-broker comparison](six-broker-common-surface.md)
- [Six-broker offline ticker evidence ledger](six-broker-ticker-decoders.md)
- [Six-broker quote request and authentication evidence](six-broker-quote-request-auth.md)
- [Six-broker candle (minute/day/week/month/year) evidence, 2026-11-05](candle-evidence-2026-11-05.md)
- [Six-broker market-operations (tick size, price limits, sessions, holidays, status) evidence, 2026-11-05](market-operations-evidence-2026-11-05.md)
- [Private offline request planner usage](../usage/offline-six-broker-request-plans.md)

The next step is to verify exact response schema/field-level semantics with
the current official specification and sanitized authorized responses. See
[Issue #2](https://github.com/kisbi3/ktradelink/issues/2).
