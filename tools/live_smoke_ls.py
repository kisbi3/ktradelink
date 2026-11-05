"""Opt-in LS t1102 smoke check: one token request and one quote, nothing else.

Run it on your own computer with your own LS Open API app key. It is never run
in CI. Without ``--live`` it sends nothing and only shows what would be sent.

    python tools/live_smoke_ls.py                 # dry run, no network
    python tools/live_smoke_ls.py --live          # 2 HTTPS requests to LS

Credentials come from ``KTRADELINK_LS_APP_KEY`` / ``KTRADELINK_LS_APP_SECRET``
or a hidden prompt; there is deliberately no command-line option for them,
because arguments end up in shell history and process lists.

Everything printed is meant to be shareable: no app key, secret, token, raw
response body or header value is ever printed or written to disk. Failures
show a static kind, a redacted gateway status and a value-free JSON shape.
No orders, no account access, no retries, no automatic token refresh.
"""

import argparse
import getpass
import os
import re
import sys
import time
from collections.abc import Callable, Mapping
from typing import TextIO

from ktradelink._credential_runtime import (
    CredentialError,
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._diagnostics import gateway_status, json_shape
from ktradelink._https_transport import (
    HttpsTransport,
    TransportError,
    WireRequest,
    build_quote_request,
    build_token_request,
)
from ktradelink._request_plan import decode_offline_quote_response, plan_ticker_request
from ktradelink._token_codec import TokenError, save_example_token_response

KEY_ENV = "KTRADELINK_LS_APP_KEY"
SECRET_ENV = "KTRADELINK_LS_APP_SECRET"
CONFIRM_WORD = "send"
_SYMBOL = re.compile(r"[0-9]{6}")
_DECODER_ERROR = re.compile(r"[A-Za-z0-9_.]{1,64}: [A-Za-z]{1,32}")

EXIT_OK, EXIT_FAILED, EXIT_USAGE = 0, 1, 2


def _now_ms() -> int:
    return time.time_ns() // 1_000_000


def _native_available() -> bool:
    from ktradelink._native import NativeCoreUnavailable, core_version
    try:
        core_version()
    except NativeCoreUnavailable:
        return False
    return True


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="live_smoke_ls.py",
        description="Opt-in LS t1102 smoke check (1 token + 1 quote). Dry run by default.",
        allow_abbrev=False,
    )
    parser.add_argument("--symbol", default="005930",
                        help="6-digit KRX stock code (default: 005930)")
    parser.add_argument("--live", action="store_true",
                        help="actually send the two HTTPS requests to LS")
    parser.add_argument("--yes", action="store_true",
                        help="skip the interactive confirmation (only with --live)")
    return parser


def _describe(request: WireRequest, out: TextIO) -> None:
    """Method, origin, path and header *names* only; never values or body."""
    names = ", ".join(name for name, _ in request.headers)
    print(f"    {request.method} {request.origin}{request.path}", file=out)
    print(f"    header names: {names}", file=out)


def _report_shape(body: bytes, out: TextIO) -> None:
    print("    response shape (field paths and types only, no values):", file=out)
    for line in json_shape(body):
        print(f"      {line}", file=out)


def _report_transport_error(step: str, error: TransportError, out: TextIO) -> None:
    print(f"[{step}] FAILED: {error.kind.value} (delivery: {error.delivery.value})", file=out)
    if error.diagnostic is not None:
        print(f"    gateway code: {error.diagnostic.code}", file=out)
        print(f"    gateway message: {error.diagnostic.message}", file=out)


def _read_credentials(
    env: Mapping[str, str], ask_secret: Callable[[str], str], out: TextIO,
) -> CredentialPair | None:
    key = env.get(KEY_ENV) or ask_secret(f"LS app key ({KEY_ENV} not set): ")
    secret = env.get(SECRET_ENV) or ask_secret(f"LS app secret ({SECRET_ENV} not set): ")
    try:
        return CredentialPair(key.strip(), secret.strip())
    except (CredentialError, AttributeError):
        print("Credentials are empty or contain invalid characters.", file=out)
        return None


def _dry_run(symbol: str, out: TextIO) -> int:
    identity = CredentialIdentity("ls", "live", "smoke")
    provider = InMemoryCredentialProvider()
    provider.put(identity, CredentialPair("DRY_RUN_KEY", "DRY_RUN_SECRET"))
    cache = InMemoryTokenCache()
    cache.put(provider, provider.load(identity), access_token="DRY_RUN_TOKEN",
              expires_at_ms=2, now_ms=0)
    plan = plan_ticker_request("ls", symbol, venue="KRX", environment="live")
    print("Dry run: nothing is sent. With --live these 2 requests would be sent:", file=out)
    print("[1/2] token", file=out)
    _describe(build_token_request(identity, provider), out)
    print("[2/2] quote (t1102, KRX)", file=out)
    _describe(build_quote_request(plan, identity, provider, cache, now_ms=1), out)
    try:
        from ktradelink._native import NativeCoreUnavailable, core_version
        print(f"native decoder: available (core {core_version()})", file=out)
    except NativeCoreUnavailable:
        print("native decoder: NOT available - build it before --live "
              "(see docs/usage/live-smoke-ls.md)", file=out)
    print("No request sent.", file=out)
    return EXIT_OK


def _live(symbol: str, pair: CredentialPair, out: TextIO) -> int:
    identity = CredentialIdentity("ls", "live", "smoke")
    provider = InMemoryCredentialProvider()
    provider.put(identity, pair)
    cache = InMemoryTokenCache()
    transport = HttpsTransport(network_enabled=True, collect_diagnostics=True)
    secrets = [pair.client_key, pair.client_secret]

    try:
        token_response = transport.send(build_token_request(identity, provider))
    except TransportError as error:
        _report_transport_error("1/2 token", error, out)
        return EXIT_FAILED
    try:
        lease = save_example_token_response(token_response, identity, provider, cache,
                                            now_ms=_now_ms())
    except TokenError as error:
        print(f"[1/2 token] FAILED: {error.kind.value}", file=out)
        status = gateway_status(token_response.body, redact=secrets)
        if status is not None:
            print(f"    gateway code: {status.code}", file=out)
            print(f"    gateway message: {status.message}", file=out)
        _report_shape(token_response.body, out)
        return EXIT_FAILED
    remaining_s = max(0, (lease.expires_at_ms - _now_ms()) // 1000)
    print(f"[1/2 token] OK: bearer token received, valid for about {remaining_s} s", file=out)
    secrets.append(lease.access_token)

    plan = plan_ticker_request("ls", symbol, venue="KRX", environment="live")
    try:
        quote_response = transport.send(
            build_quote_request(plan, identity, provider, cache, now_ms=_now_ms()))
    except TransportError as error:
        _report_transport_error("2/2 quote", error, out)
        return EXIT_FAILED
    except CredentialError as error:
        print(f"[2/2 quote] FAILED before sending: {error.kind.value}", file=out)
        return EXIT_FAILED

    try:
        ticker = decode_offline_quote_response(
            plan, http_status=quote_response.status, json_text=quote_response.json_text)
    except Exception as error:  # report a static reason only, never the body
        # The Rust decoder's ValueError text is "<field>: <Kind>"; anything
        # else is reduced to its exception class name.
        text = str(error)
        if type(error) is ValueError and _DECODER_ERROR.fullmatch(text):
            reason = text
        else:
            reason = type(error).__name__
        print(f"[2/2 quote] FAILED to decode: {reason}", file=out)
        status = gateway_status(quote_response.body, redact=secrets)
        if status is not None:
            print(f"    gateway code: {status.code}", file=out)
            print(f"    gateway message: {status.message}", file=out)
        _report_shape(quote_response.body, out)
        return EXIT_FAILED
    print(f"[2/2 quote] OK: {ticker.symbol} last={ticker.last} volume={ticker.volume}",
          file=out)
    print("    venue is the requested KRX; the t1102 response has no venue field.", file=out)
    print("Done. The token stays valid at LS until it expires; it was not stored.", file=out)
    return EXIT_OK


def main(
    argv: list[str] | None = None, *, env: Mapping[str, str] | None = None,
    ask: Callable[[str], str] = input, ask_secret: Callable[[str], str] = getpass.getpass,
    out: TextIO | None = None,
) -> int:
    out = sys.stdout if out is None else out
    env = os.environ if env is None else env
    try:
        args = _parser().parse_args(argv)
    except SystemExit as exit_:
        return EXIT_USAGE if exit_.code else EXIT_OK
    if not _SYMBOL.fullmatch(args.symbol):
        print("--symbol must be a 6-digit KRX stock code.", file=out)
        return EXIT_USAGE
    if not args.live:
        if args.yes:
            print("--yes only applies together with --live.", file=out)
            return EXIT_USAGE
        return _dry_run(args.symbol, out)
    if not _native_available():
        # Otherwise a token would be issued and the quote could not be decoded.
        print("The native decoder is not installed; build it first "
              "(see docs/usage/live-smoke-ls.md). No request sent.", file=out)
        return EXIT_USAGE

    print("This sends exactly 2 HTTPS requests to openapi.ls-sec.co.kr:8080:", file=out)
    print("  1) POST /oauth2/token        (issues one bearer token for your app key)", file=out)
    print(f"  2) POST /stock/market-data   (t1102 quote for {args.symbol}, KRX)", file=out)
    print("No orders, no account access, no retries.", file=out)
    if not args.yes:
        try:
            answer = ask(f"Type '{CONFIRM_WORD}' to continue: ")
        except EOFError:
            answer = ""
        if answer.strip() != CONFIRM_WORD:
            print("Cancelled. No request sent.", file=out)
            return EXIT_USAGE
    try:
        pair = _read_credentials(env, ask_secret, out)
    except EOFError:
        pair = None
    if pair is None:
        print("No credentials. No request sent.", file=out)
        return EXIT_USAGE
    return _live(args.symbol, pair, out)


if __name__ == "__main__":
    sys.exit(main())
