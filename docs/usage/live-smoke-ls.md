# LS live smoke check (opt-in, your own machine only)

`tools/live_smoke_ls.py` makes the first contact with the real LS gateway. It
sends **one token request and one t1102 quote**, prints a result that never
contains your credentials or token, and exits. It never places orders, reads accounts, retries or stores anything.
CI never runs it. See ADR 0012 for the design.

## Before you start

- The maintainer has separately approved a live run, naming the broker
  (LS), the environment (live; LS paper is unsupported) and the scope
  (quote only).
- An LS Open API app is registered and you have its app key and secret.
  Check the LS portal for app or IP registration conditions. This repository
  has not pinned evidence for them.
- t1102 needs no account number. Never type one into anything here.

## 1. Build the package and the native decoder

From a clone of the repository, in a virtual environment (a Rust toolchain
is required):

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
python -m pip install -e ".[dev]" "maturin==1.16.0"
```

```bash
python -m maturin develop --release --manifest-path bindings/python/Cargo.toml
```

On Windows, activate with `.venv\Scripts\activate` instead.

## 2. Dry run (sends nothing)

```bash
python tools/live_smoke_ls.py
```

It should end with `native decoder: available` and `No request sent.`

## 3. Live run

Provide the credentials through the environment, or let the tool ask for
them with a hidden prompt. Never pass them as arguments, and never commit or
paste them anywhere.

```bash
python tools/live_smoke_ls.py --live --symbol 005930
```

Type `send` when asked. The tool prompts for the key and secret if
`KTRADELINK_LS_APP_KEY` / `KTRADELINK_LS_APP_SECRET` are not set.

## What it prints and what to share

The tool never prints your key, secret or token, a raw response body or a
header value. Even so, **read the output before sharing it**:

- **Success:** `[2/2 quote] OK: 005930 last=… volume=…`. This is LS market
  data. Check LS's terms before posting it anywhere public.
- **Failure:** the step, a static kind such as `http_unauthorized`, the
  delivery state, and the gateway's status code. If the code contains your
  key, secret or token, it prints as `<redacted>`.
- **Gateway message:** hidden by default. `--show-gateway-message` prints it
  with your key, secret and token redacted. It is still arbitrary upstream
  text and may contain other details you would not want to share.
- **Unexpected shape:** field paths and types only, for example
  `t1102OutBlock.price: string:digits`. Only field names documented by LS
  are printed; any other key prints as `<key>`.

A key or secret shorter than 8 characters is refused, because it could not
be reliably redacted from output. Before `--live` sends anything, the tool
also checks that the native decoder can decode a synthetic t1102 response.

## Things to know

- Each live run issues a new token. It stays valid at LS until it expires,
  because the tool has no revoke call. Avoid running it in a tight loop.
- The guide lists 10 transactions per second for t1102. One run sends one
  quote.
- The printed venue is the requested KRX: the t1102 response has no venue
  field.
- If the token step fails with `TOKEN_IN_FLIGHT`, another token request with
  the same credentials is still running in the same process. Wait for it to
  finish.
