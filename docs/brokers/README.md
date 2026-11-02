# Broker evidence and verification status

These files record **publisher documentation evidence**, not functional
KTradeLink broker support. Offline decoder candidates now exist in a Draft
PR, but no authenticated network fetch_ticker adapter is implemented or
live-tested.

- [KIS market-data evidence](kis-market-data.md)
- [Kiwoom REST market-data evidence](kiwoom-market-data.md)
- [Original six-broker comparison](six-broker-common-surface.md)
- [Six-broker offline ticker evidence ledger](six-broker-ticker-decoders.md)

The next step is to verify exact response schema/field-level semantics with
the current official specification and sanitized authorized responses. See
[Issue #2](https://github.com/kisbi3/ktradelink/issues/2).
