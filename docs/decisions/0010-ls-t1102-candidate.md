# ADR 0010: Move LS from the onboarding demo to the published t1102 contract

- Date: 2026-11-05 (Asia/Seoul)
- Status: **proposed for independent review; offline implementation**, not live API approval.
- Base: PR #24 (`claude/issue-17-transport-hardening`) on top of `main` `2d1f416f7e689c38ebf1ac056773a4c84a76c6da`.
- Related: Issue #17. Supersedes the LS-specific statements in ADR 0006 ("LS onboarding/demo response is not assumed equal to `t1102`"), ADR 0007 (onboarding walkthrough path) and ADR 0008 ("LS remains an onboarding candidate"). Everything else in ADR 0005–0009 stays binding.

## Context

Until now the LS planner used the onboarding `GET /stock/market-data` with
`tr_id: STKCURR` from the getting-started guide, and the decoder accepted that
demo's flat JSON. Earlier audits could not find a complete t1102 REST
contract. On 2026-11-05 the LS API guide served full TR details for t1102 and
for the token endpoint. The retrieved copies are identified by hash in
[the ledger](../brokers/live-auth-transport-gates-2026-11-05.md).

## Decision

1. **Quote request (planner):**
   - `POST https://openapi.ls-sec.co.kr:8080/stock/market-data`
   - Headers: `content-type: application/json; charset=utf-8`, `tr_cd: t1102`,
     `tr_cont: N`, empty `tr_cont_key` and empty `mac_address`, as in the
     publisher sample.
   - Body: `{"t1102InBlock":{"shcode":"<6 digits>","exchgubun":"K"}}`.
   - LS treats any unknown `exchgubun` as KRX. The KRX code `K` is therefore
     always sent explicitly; `N` (NXT) and `U` (integrated) are not offered.
   - `mac_address` is mandatory only for corporate customers. Corporate use is
     unsupported, and a MAC is never auto-detected.
   - Paper stays unsupported: the guide does not establish a separate paper
     origin, and its order example distinguishes live from paper by `tr_id`.
2. **Decoder (Rust):**
   - Requires root `rsp_cd == "00000"`. A missing or `null` status is
     `MissingRequired`, unlike the older optional-status brokers.
   - Requires the `t1102OutBlock` object and an echoed `shcode` equal to the
     request.
   - Maps `price` (unsigned; direction lives in `sign`) and `volume`.
   - `open`/`high`/`low` are `0` before the first trade in the publisher
     example. Whether `0` is a sentinel is undocumented, so they are not mapped.
   - The response has no venue field. Provenance is limited to "requested KRX".
3. **Token (Python):**
   - Request: form body `grant_type=client_credentials`, `appkey`,
     `appsecretkey`, `scope=oob`, with TLS verification on. The canonical shape
     is enforced by `WireRequest`.
   - Response: explicit Bearer `token_type`; `scope == "oob"`; no
     `rsp_cd`/`rsp_msg` envelope.
   - Lifetime: the guide's field table says `expire_in`, but its example says
     `expires_in`. Exactly one of the two must be present, as an integer
     between 1 and a library sanity bound of 7 days. Both or neither fail
     closed.
   - The lease expires that many seconds after the caller's `now_ms`. Callers
     should pass the time before sending, so the round trip is not counted as
     lifetime.

## Consequences and limits

- These are publisher documentation and samples, not gateway verification.
  Live acceptance, the `rsp_cd` universe, rate limits (the guide lists
  10 TPS for t1102) and the meaning of zero OHLC values remain unverified.
- No public `fetch_ticker`. Network stays disabled by default. No credential,
  token, quote, account or order request was made to LS.
- DB, Toss and Meritz remain blocked for real `WireRequest`s. The gates for
  them are listed in the ledger.
