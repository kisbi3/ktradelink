# KTradeLink

**One API. Every Korean Broker.**

KTradeLink is an open-source, Python-native project to provide one consistent
interface to the Open APIs of Korean securities brokers. It takes inspiration
from the [CCXT](https://github.com/ccxt/ccxt) unified API approach.

> **Status: pre-alpha / foundation only.** The package is importable, but no
> broker adapters, market-data methods, or trading operations are implemented.
> Example broker calls described in design discussions are not functional yet.

## Mission

Users should be able to change broker adapters without rewriting their
application's market-data and account workflows, provided that the capability
is actually supported by both brokers.

The first intended integrations are **Korea Investment & Securities (KIS)** and
**Kiwoom Securities**. Additional brokers, real-time data, and trading APIs are
planned but not promised for a particular release.

## Principles

- **Unified, not misleading:** expose common semantics; never silently emulate
  an unsupported broker capability.
- **Native escape hatch:** retain a documented route to broker-specific features.
- **Safe by default:** do not place real orders implicitly; keep credentials out
  of logs, source control, and LLM review materials.
- **Evidence-driven:** map each broker adapter to official API documentation and
  contract tests; mark undocumented assumptions explicitly.
- **Traceability:** make small, meaningful, tested commits and preserve their
  history through non-squash pull-request merges.

## Scope

**Near term:** Python package foundation, unified domestic-equity market-data
specification, KIS and Kiwoom adapters with tests.

**Later:** accounts, paper-trading-verified order workflows, WebSocket event
streams, additional brokers, and other asset classes.

**Not in scope for the core library:** strategy hosting, portfolio management
UI, backtesting engine, centralized brokerage credentials, or custody.

## Development installation

Python 3.11 or newer is required.

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m ruff check .
```

The commands above verify the *bootstrap only*; they do not test connectivity to
any securities broker. Production and live-account use is **not supported**.

## Collaboration

GitHub is the source of truth. ChatGPT Chat prepares implementations and pull
requests; Gemini Web is used for an independent review. The human maintainer
approves merges. See [AGENTS.md](AGENTS.md) and
[CONTRIBUTING.md](CONTRIBUTING.md).

## Safety and licensing

KTradeLink is software infrastructure, not investment advice. Future users are
responsible for complying with broker API contracts, exchange market-data terms,
and applicable regulations. No broker credentials should appear in public
issues or pull requests.

MIT licensed. See [LICENSE](LICENSE).
