# Experimental `fetch_ticker` (KIS, Kiwoom, LS)

> **Experimental and unverified.** `fetch_ticker` is built from publisher
> documentation and examples and tested only against mocked HTTPS. It has
> **never** been run against a live or paper gateway. Its capability state is
> `documented_candidate`, not `supported`. Merging it authorised no live run.
> Use your own app key, on your own machine, at your own risk.

Design and limits: [ADR 0013](../decisions/0013-public-fetch-ticker-surface.md).

## Offline: nothing is sent

```python
import ktradelink

creds = ktradelink.Credentials("SYNTHETIC_KEY", "SYNTHETIC_SECRET")
client = ktradelink.connect("ls", environment="live", credentials=creds)

print(client.capabilities)
try:
    client.fetch_ticker("005930")
except ktradelink.NetworkDisabled as error:
    print(error.reason, error.delivery)  # network_not_enabled DeliveryState.NOT_SENT
```

`connect()` never sends anything. Without `allow_network=True`,
`fetch_ticker` checks its arguments and stops before building any request.

## Opting in

```python
client = ktradelink.connect(
    "ls",                       # "kis", "kiwoom" or "ls"
    environment="live",         # required; "paper" only where documented
    credentials=creds,          # explicit; never read from the environment
    allow_network=True,         # explicit network opt-in
    accept_unverified=True,     # acknowledges "documented_candidate"
)
with client:
    ticker = client.fetch_ticker("005930")  # venue="KRX", params=None
    print(ticker.symbol, ticker.last, ticker.volume)
```

- **Brokers:** KIS (live and paper), Kiwoom (live and paper) and LS (live).
  DB, Toss and Meritz raise `UnsupportedCapability`; so does LS paper.
  `ktradelink.capabilities("kis")` lists the state per environment.
- **KIS needs `kis_expiry_timezone`.** KIS returns a token expiry without a
  time zone, and the publisher sample does not say which one. Pass a
  `datetime.timezone` you have confirmed yourself, for example
  `kis_expiry_timezone=timezone(timedelta(hours=9))` if you have established
  that KIS uses KST. The library will not guess.
- **Symbol and venue:** six ASCII characters in `[0-9A-Z]` (ADR 0016),
  `venue="KRX"` only. Lowercase, whitespace and native forms such as
  `A005930` or `005930_NX` raise `InvalidSymbol`; nothing is folded or
  stripped. A symbol with a letter (e.g. `0000D0`) is accepted for KIS but
  raises `UnsupportedCapability` for Kiwoom and LS, whose documents do not
  show such codes. Whether KIS's quote route accepts one is not verified.
  `NXT` and `BROKER_COMPOSITE` are unsupported; there is no fallback to KRX.
- **`params`:** must be `None` or empty for now. Unknown options are errors.
- **Result:** the same `ktradelink.models.Ticker` the decoders produce.
  `timestamp` and `retrieved_at` are `None`. LS fills only `last` and
  `volume`. `venue` is the venue you requested; no response proves it.
- **Native decoder:** the optional `ktradelink-native` extension must be
  installed (see [live-smoke-ls.md](live-smoke-ls.md), step 1). Otherwise the
  call raises `UnsupportedCapability("native_decoder_unavailable")` before
  sending anything.

## What one call sends

At most **one token request** (only when no token with more than 60 s left is
cached) and **one quote request**. Nothing is retried, and no token is
refreshed in the background. Each client keeps its own token cache. Two
clients, or two processes, using the same app key can invalidate each
other's tokens, so create one client per key and reuse it. `close()` drops
the credentials and cached token from the client; a token already issued
stays valid at the broker until it expires.

A client is safe to share between threads. If one thread is requesting a
token, a second thread that also needs one fails immediately with
`TransportError` (`reason="token_request_in_flight"`, `NOT_SENT`) instead of
sending a second token request.

## Errors

Every error is a `ktradelink.KTradeLinkError` with static fields only:
`reason`, `stage` (`None`, `"token"` or `"quote"`) and `delivery`. Credentials,
tokens, headers, bodies and broker messages never appear in an error, and no
error chains the internal exception.

| Error | Meaning |
| --- | --- |
| `InvalidSymbol`, `InvalidVenue`, `InvalidParameter` | Bad argument; nothing sent |
| `UnsupportedCapability` | Broker, environment, venue or decoder not available |
| `NetworkDisabled` | Client created without `allow_network=True` |
| `ClientClosed` | `close()` was called |
| `AuthenticationError` / `PermissionDenied` | HTTP 401 / 403 |
| `RateLimitExceeded` / `BrokerUnavailable` | HTTP 429 / 5xx |
| `TransportError` | Connect, TLS, write, read, redirect or other HTTP failure |
| `BrokerRejected` | HTTP 200 with a non-success broker status |
| `ResponseSchemaError` | HTTP 200 with a missing status or a malformed body |

The HTTP classes use the generic HTTP meaning of the status. Broker error
codes are not interpreted. A quote 401 drops the token that was used, so the
next call requests a new one.

**Check `delivery` before you call again.** `NOT_SENT` means nothing reached
the broker. `RESPONSE_RECEIVED` means the broker answered. `UNKNOWN` means the
request may have arrived: for a token request, a token may have been issued
that this client never saw. Quotes are read-only, but never build automatic
retry loops on top of this API; respect each broker's own rate limits, which
this library does not know.

## What is not verified

Everything about the real gateways: whether they accept these exact
requests, the KIS expiry time zone, the full set of status codes, rate
limits, Kiwoom's signed prices, and whether a quote really comes from KRX.
See the [2026-11-05 ledger](../brokers/live-auth-transport-gates-2026-11-05.md).
Quote data is broker market data; its redistribution terms are not
established here.
