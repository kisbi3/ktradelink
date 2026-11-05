# LS live smoke check (opt-in, your own machine only)

`tools/live_smoke_ls.py` makes the first contact with the real LS gateway. It
sends **one token request and one t1102 quote**, prints a shareable result and
exits. It never places orders, reads accounts, retries or stores anything.
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

- **Success:** `[2/2 quote] OK: 005930 last=… volume=…`.
- **Failure:** the step, a static kind such as `http_unauthorized`, the
  delivery state, and, when the gateway sent one, its status code and
  message with your key, secret and token replaced by `<redacted>`.
- **Unexpected shape:** field paths and types only, for example
  `t1102OutBlock.price: string:digits`. Values are never printed.

The output is designed to be pasted into an Issue or a review. Still, read
the gateway message before sharing it: it is upstream text, and only your
key, secret and token are redacted from it.

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
