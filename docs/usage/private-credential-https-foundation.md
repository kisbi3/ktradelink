# Private credential and HTTPS foundation (not a live broker client)

This is an **implementation candidate for Issue #17**. Python can hold explicitly
supplied credentials and bearer tokens, construct evidence-scoped KIS/Kiwoom
example requests and implement a TLS-verified HTTPS send. **Nothing here is a
functional or verified public `fetch_ticker` API**. No actual service is
contacted by importing the package or running its CI.

The safe default is a **disabled** transport. This example is fully offline and
uses intentionally synthetic values that will never authenticate anywhere:

```python
from ktradelink._credential_runtime import (
    CredentialIdentity, CredentialPair, InMemoryCredentialProvider, InMemoryTokenCache,
)
from ktradelink._https_transport import (
    HttpsTransport, TransportError, TransportFailure, build_token_request,
)

identity = CredentialIdentity("kis", "live", "demo")  # Non-secret alias.
provider = InMemoryCredentialProvider()
provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
request = build_token_request(identity, provider)  # Only creates an in-memory request.

try:
    HttpsTransport().send(request)  # Network disabled unless separately enabled.
except TransportError as exc:
    assert exc.kind is TransportFailure.NOT_ENABLED
```

Do not paste actual credentials into source code, test files or ChatGPT/Claude
review materials. The credential provider does not search local storage or
read environment variables. A real caller would be responsible for secure
secret acquisition outside this repository. The in-memory token cache expects
explicit expiry and credentials; it never refreshes automatically. The private
KIS/Kiwoom token parser can read a synthetic publisher-example response and
save an explicitly scoped, expiring lease, but it does not contact a broker.

A production real HTTPS client would need a **separate reviewed authorization**
and explicit opt-in. Even then, only two broker token request/response candidates
are currently encoded from publisher samples; their real/paper acceptance is
unverified. The other four brokers remain blocked for real WireRequests. KIS
quote planner still uses older lowercase query keys while newer sample shows
uppercase; no gateway acceptance has been demonstrated. Responses are raw and
untrusted; the SDK does not map them into a public Ticker or infer exchange/time.

### Failure semantics

The HTTPS transport uses a bounded timeout, certificate and hostname validation,
no redirect following, no ambient proxy and no automatic retry. Its delivery
state differentiates `NOT_SENT`, `UNKNOWN` and `RESPONSE_RECEIVED`. A write error
or missing HTTP status could mean the server has already seen the request;
**never automatically replay a non-idempotent operation**. HTTP 401/403/429,
5xx, other statuses and oversized response bodies have static error kinds, not
error strings containing network messages, headers or payload bytes.

Note that `network_enabled=True` exists in the private code as an explicit
runtime opt-in. Its existence is **not** permission for automated CI, this
assistant or contributors to contact real broker systems. It should never be
used in tests with real brokerage origins. The internal request/response objects
contain sensitive data in memory by necessity; their `repr` is redacted but
callers must never dump their `__dict__`, fields, tracebacks with locals, or
memory. Python's memory model cannot erase already-created immutable strings.

See [ADR 0009](../decisions/0009-opt-in-credential-https-foundation.md),
[dated evidence ledger](../brokers/live-auth-transport-gates-2026-11-05.md),
[ADR 0008](../decisions/0008-offline-auth-transport-contracts.md), and
[Issue #17](https://github.com/kisbi3/ktradelink/issues/17).
