# Fake authentication and transport (private, offline only)

This rehearses Issue #17 without real keys, tokens, accounts, MAC addresses,
HTTP clients or broker requests. It is NOT public fetch_ticker. A native wheel
is required for successful decoding; missing native code fails explicitly.
Importing the fake module or rejecting a request does not load native code.

```python
from ktradelink._offline_session import (
    CredentialScope, FakeCredentialProvider, FakeResponse, FakeTransport,
    FixtureOutcome, execute_offline_quote,
)
from ktradelink._request_plan import plan_ticker_request

plan = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
scope = CredentialScope("kis", "live", 0)  # Fixture slot, not an account number.
provider = FakeCredentialProvider()
lease = provider.issue(scope, now_ms=0, lifetime_ms=100)
response = FakeResponse(
    plan, lease, 200,
    '{"rt_cd":"0","output":{"stck_prpr":"72000.00","acml_vol":"0"}}',
    FixtureOutcome.SUCCESS,
)
transport = FakeTransport((response,))
ticker = execute_offline_quote(plan, scope, provider, transport, now_ms=1)
assert ticker.last is not None and ticker.volume == 0
assert transport.calls == 1
```

The environment string selects a request template only. No live or paper server
is contacted. All six offline candidates can use this flow; LS uses the
published t1102 REST shape (ADR 0010). Only the previously evidenced KIS/Kiwoom
paper templates are available. No native or Python model contract is changed.

## Synthetic state and failures

A lease contains no bearer value. Its scope separates brokers, environments and
integer fixture identity slots. Each provider owns its cache. `issue()` explicitly
replaces a lease; old response scripts fail object-identity matching. `revoke()`
removes one scope. `get()` rejects missing, future-issued and expired leases;
expiry is exclusive. No cache is persisted and nothing auto-refreshes.

Each response belongs to a whole request plan and one issued lease; the plan's
broker/environment must match the lease scope. Scripts are consumed once even
on errors. A missing lease **before** exchange yields CREDENTIAL_UNAVAILABLE,
whereas a lease that becomes invalid **after** the scripted exchange yields
LEASE_INVALID_AFTER_EXCHANGE. A post-exchange error never means "request not sent"
and must not trigger a replay of a non-idempotent operation. This fake has no
order support. Timeout is simulated elapsed_ms >= timeout_ms;
the allowed 1..60,000 ms bound is a library policy, not a broker limit. TLS must
be enabled in the policy, redirects disabled, retries zero. These flags do NOT
implement TLS, network cancellation or elapsed-time measurement.

Only exact HTTP 200 can proceed; 204, 206 and other 2xx responses are rejected
by this library-owned fake-quote policy. 401 invalidates the matching scope
without replay. 403, 429, 5xx and redirects have distinct FailureKind values;
no error body is reflected. Bodies are hidden from repr and UTF-8 bounded to
1,048,576 bytes (library limit). Mapped decoder rejection becomes a static error
with no retained exception context. A broken transitive native import propagates,
rather than being disguised as a missing extension. This is not secret-memory
erasure; Python callers/debuggers still have access to their fixture objects.

## Important gap: fixture assertion is not provider attestation

FixtureOutcome defaults to UNVERIFIED and must be explicitly SUCCESS to decode.
It is a test author's assertion, not a parsed broker status or market proof.
A success fixture still passes through the existing Rust JSON/status validation;
present invalid status fields are rejected. Existing optional status omissions
(KIS, Kiwoom and Meritz; LS and DB require their status, ADR 0010/0015)
remain offline-only behavior. Do NOT copy this flow into a live adapter: actual
status completeness, requested symbol/market/environment and session clock must
be verified from publisher-evidenced wire responses. No timestamp is inferred
from the fake clock, and no KRX-only provenance is established by this test.

See [ADR 0008](../decisions/0008-offline-auth-transport-contracts.md) and the
[dated source audit](../brokers/auth-transport-evidence-2026-11-03.md).

## Reproduce

Install the Python package first (`pip install -e ".[dev]"`), then run
`python -m pytest -q` and `python -m ruff check .`. The isolated subprocess test
uses the installed package rather than PYTHONPATH. With the optional native
wheel installed, run `python -m pytest -q tests bindings/python/tests`.
CI also executes fake-session checks from installed Python/native wheels outside
the checkout. None of these tests calls a broker. Independent fixed-SHA review
and separate maintainer approval are required before merge.
