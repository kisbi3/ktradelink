# ADR 0012: Opt-in LS smoke tool and value-free diagnostics

- Date: 2026-11-05 (Asia/Seoul)
- Status: **proposed for independent review; offline implementation**. Merging this does
  not authorise any live run. A maintainer runs it with their own key, on
  their own machine, after separate approval.
- Base: PR #26 (`claude/issue-17-token-send-anchor`, ADR 0011).
- Related: Issue #17. ADR 0005–0011 stay binding, except as noted in item 2.

## Context

The first run against the real LS gateway is the first time any of the
LS contracts from ADR 0010 meets real data. Before that run, three problems
had to be solved:

- **No safe entry point.** Without a tool, a person would wire the private
  components together by hand, and could easily print a token or a raw body.
- **Opaque failures.** A failure carries only a static kind such as
  `http_server_error`. The gateway's own status code and message are thrown
  away, so the first failure would be impossible to diagnose.
- **No way to share a response.** If the real response differs from the
  documented one (for example `price` as a string), there is no safe way to
  show how it differs.

## Decision

1. **`tools/live_smoke_ls.py`**
   - **What it sends:** one LS token request and one t1102 quote (KRX).
     Nothing else: no orders, no account access, no retries, no refresh.
     Nothing is written to disk.
   - **Dry run by default:** without `--live` it sends nothing. It prints the
     two planned requests (method, origin, path, header names) and whether
     the native decoder is installed.
   - **Live run:** `--live` also requires typing `send`; `--yes` skips that
     prompt.
   - **Decoder preflight:** before `--live` sends anything, the tool decodes a
     synthetic t1102 payload with the installed native module and checks the
     result. A version check alone let an old or partial build through
     (ChatGPT review of PR #27, M2).
   - **Credentials:** read from `KTRADELINK_LS_APP_KEY` /
     `KTRADELINK_LS_APP_SECRET`, or from a hidden `getpass` prompt. There is
     no command-line option for them, because shell history and process
     lists would keep them. A key or secret shorter than 8 characters is
     refused before sending. That is a library threshold, not an LS rule:
     shorter strings cannot be redacted reliably.
   - **Output:**
     - The token, credentials, header values and raw body are never printed.
     - Success prints symbol, last price and volume. That is LS market data,
       and the tool says so: its redistribution terms are not established.
     - Failure prints the static kind, the delivery state, the gateway code
       with credentials redacted (item 2), and the value-free shape (item 3).
     - The gateway **message** is hidden unless `--show-gateway-message` is
       given, and then it is labelled as upstream text to review before
       sharing.
     - Decoder errors print only the Rust decoder's `<field>: <Kind>` text.
       Any other exception prints only its class name.
     - The output is **not** claimed to be safe to share unreviewed (ChatGPT
       review of PR #27, H1).
2. **`HttpsTransport(collect_diagnostics=True)`** (default off)
   - For an HTTP error status, the transport reads the error body within the
     usual 1 MiB bound. It extracts a `GatewayStatus` into
     `TransportError.diagnostic` and then discards the body.
   - `GatewayStatus` takes only the root `rsp_cd` or `error` as the code, and
     `rsp_msg` or `error_description` as the message:
     - Redaction covers the app key, the secret and (for quotes) the bearer
       token. It is case-insensitive and has no minimum length.
     - The code must match `[A-Za-z0-9_.-]{1,32}`, otherwise it becomes
       `<invalid code>`. A code that contains any secret becomes
       `<redacted>`.
     - In the message, each secret is replaced with `<redacted>`.
       Non-printable characters become `?`. It is cut at 200 characters, then
       redacted again. If a secret still appears, the whole message becomes
       `<redacted>`.
   - The diagnostic never appears in `str`/`repr` of the error, and the
     error's `__context__` stays empty.
   - **This partly relaxes "errors never reflect the upstream body"**
     (ADR 0008/0009), and only when the caller opts in.
   - `rsp_cd`/`rsp_msg` is the LS t1102 envelope (ADR 0010).
     `error`/`error_description` are the generic OAuth 2.0 error fields
     (RFC 6749 §5.2). Which of them LS uses on errors is unverified, and no
     error code value is assumed.
3. **`_diagnostics.json_shape`**
   - Prints sorted `path: type` lines and never a value.
   - Types: `object`, `array`, `integer`, `number`, `boolean`, `null`, and
     strings classed as `string:empty|digits|decimal|text`.
   - It takes a required allowlist of **documented field names**; every
     other key prints as `<key>`. A key name is upstream text too, and a
     syntax check alone let a secret-shaped key through (H1).
   - The tool's allowlists are:
     - quote: the 166 `t1102OutBlock` fields from the LS t1102 REST detail
       (sha256 `42712ce969a8a480…`), plus `t1102OutBlock`;
     - token: the token REST detail's table and example fields (sha256
       `4acff92cdcdfd551…`);
     - both: the envelope keys from item 2.
   - Arrays are summarised from their first 20 elements. Depth is capped at
     8 and output at 200 lines.

## Consequences and limits

- **Tests:** `tests/test_live_smoke_ls.py` covers dry run, argument and
  confirmation refusals, success, token/quote HTTP errors, an unexpected
  token shape, an undecodable quote and a connect failure. It uses mocked
  HTTPS and checks that no synthetic secret appears in the output.
  `tests/test_diagnostics.py` covers the helpers and the transport opt-in.
- **Gateway messages and codes:** both are upstream text. Redaction removes
  only the values the tool knows (key, secret, token). It cannot prove that
  nothing else confidential is present. That is why the message is opt-in,
  and why output should be read before it is shared.
- **Token lifetime:** each live run issues a new token. It stays valid at LS
  until it expires: there is no revoke call, because no LS revoke contract
  is pinned. Whether a re-issue invalidates the previous token is
  undocumented (ADR 0011).
- **Scope:** this is not a public `fetch_ticker`, and it is not part of CI.
  Network stays disabled by default everywhere else.
- **Evidence:** no credential, token, quote, account or order request was
  made while writing this.
