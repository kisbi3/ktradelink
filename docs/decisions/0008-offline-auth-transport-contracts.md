# ADR 0008: Fake authentication and transport before live integration

- Date: 2026-11-03 (Asia/Seoul)
- Status: Offline implementation requested by maintainer; independent PR review pending.
- Base: 2009e9c7bc456fcb2ef8a2fbce585e04d31634ba (PR #19 merged).
- Related: Issue #17; ADR 0005, 0006 and 0007 remain in force.

## Scope

Exercise the missing orchestration between the existing six-broker RequestPlan
and Rust decoder using **only in-memory fakes**. This is not a credential store,
OAuth client, HTTPS implementation, sandbox account, or public fetch_ticker.
Issue #17 remains open after this incremental PR; no live-access approval follows.

## Decision

Add a private Python module, separate from Core/Decoder/PyO3 and public models.
It accepts only the concrete fake provider and fake transport, not arbitrary
callbacks or duck-typed HTTP clients. A future real provider/transport requires
a separately reviewed design; the fake API is not a frozen public protocol.

- Credential scope is broker + environment + an integer fixture identity slot.
  There is no free-form credential, account, MAC, token, file or environment input.
- Fake token leases contain scope, a generation, and explicitly injected clock
  bounds, never a bearer value. Cache state is instance-local. Issuance/rotation
  is explicit, expiry is exclusive, revocation is explicit, and a missing or
  expired lease fails rather than issuing/refreshing automatically.
- Request plans are reconstructed and compared before any fake operation.
  Unsupported paper environments still fail, never fall back to live.
- A frozen policy requires TLS verification, disallows redirects, and allows
  zero retries. Its positive bounded timeout is tested against **simulated**
  elapsed milliseconds; it does not implement or prove real TLS/timeouts.
- A scripted response is tied to the entire request plan and the exact issued
  lease. A mismatched symbol/venue/origin/environment/identity/generation fails.
  All such metadata is fixture context, **not authenticated market provenance**.
- HTTP 401, 403, 429, 5xx, redirects and other failures have distinct static
  errors. A 401 invalidates only the matching fake scope. Nothing is replayed.
- A separate explicit fixture outcome must say success before decoding.
  Missing/unverified outcome fails. This outcome is not a broker response field
  and must NEVER substitute for provider-specific status validation in live code.
- Response bodies stay out of repr and error text. UTF-8 size is bounded before
  native dispatch. Decoder errors are replaced with a static error without a
  displayed exception chain. This is not memory erasure or a hostile-code sandbox.
- The existing native decoder still parses JSON and constructs the same Ticker.
  It remains lazy and optional. No Python JSON decoder/fallback is introduced.
  No guessed prices, market labels, retrieved_at or exchange timestamps are added.

## Deliberately unresolved

Wire status-field completeness, quote symbol/market/environment attestation,
exchange/session clocks, real token expiry/rotation/revocation, process concurrency,
credential storage, account entitlement and redistribution rights remain gates.
Existing optional status fields in offline decoders are NOT a live success policy.
LS remains an onboarding candidate, not t1102. DB unsafe samples are not executed.
Meritz MAC values are never discovered. Public support/capability flags stay false.
See the [dated evidence audit](../brokers/auth-transport-evidence-2026-11-03.md).

## Verification and merge

Synthetic fixtures cover all six brokers, scope separation, expiry/rotation,
no retry, timeout, response mismatch, redacted errors, and lazy native import.
Test the fake-to-native path and installed wheels, not just monkeypatched returns.
Keep CI credential-free on Python 3.11-3.13 and Linux/Windows/macOS. Preserve
semantic commits, pin the full-source review packet to HEAD, and require Gemini
review plus explicit maintainer merge approval. No actual broker calls in CI.
