"""Opt-in LS t1102 smoke check: one token request and one quote, nothing else.

Run it on your own computer with your own LS Open API app key. It is never run
in CI. Without ``--live`` it sends nothing and only shows what would be sent.

    python tools/live_smoke_ls.py                 # dry run, no network
    python tools/live_smoke_ls.py --live          # 2 HTTPS requests to LS

Credentials come from ``KTRADELINK_LS_APP_KEY`` / ``KTRADELINK_LS_APP_SECRET``
or a hidden prompt; there is deliberately no command-line option for them,
because arguments end up in shell history and process lists.

Output never contains the app key, secret, token, a raw response body or a
header value, and nothing is written to disk. Failures show a static kind,
the gateway status code with your credentials redacted, and a value-free
JSON shape that names only documented LS fields. Review the output before
sharing it anyway:
- a successful quote is LS market data, whose redistribution terms are not
  established here;
- the gateway *message* is arbitrary upstream text, so it is hidden unless
  you pass ``--show-gateway-message``, and even then only your credentials
  and token are redacted from it.
No orders, no account access, no retries, no automatic token refresh.
"""

import argparse
import getpass
import os
import re
import sys
import time
from collections.abc import Callable, Mapping
from decimal import Decimal
from typing import TextIO

from ktradelink._credential_runtime import (
    CredentialError,
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._diagnostics import GatewayStatus, gateway_status, json_shape
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
# Library safety threshold, NOT an LS rule: shorter strings cannot be
# redacted from output without shredding ordinary text.
MIN_CREDENTIAL_CHARS = 8

# Field names the shape report may print. Everything else prints as <key>.
# t1102OutBlock fields: LS API guide t1102 REST detail, retrieved 2026-11-05,
# sha256 42712ce969a8a480... (docs/brokers/live-auth-transport-gates-2026-11-05.md).
_T1102_OUT_FIELDS = frozenset("""
    hname price sign change diff volume recprice avg uplmtprice dnlmtprice jnilvolume
    volumediff open opentime high hightime low lowtime high52w high52wdate low52w
    low52wdate exhratio per pbrx listing jkrate memedan offernocd1 bidnocd1 offerno1
    bidno1 dvol1 svol1 dcha1 scha1 ddiff1 sdiff1 offernocd2 bidnocd2 offerno2 bidno2
    dvol2 svol2 dcha2 scha2 ddiff2 sdiff2 offernocd3 bidnocd3 offerno3 bidno3 dvol3
    svol3 dcha3 scha3 ddiff3 sdiff3 offernocd4 bidnocd4 offerno4 bidno4 dvol4 svol4
    dcha4 scha4 ddiff4 sdiff4 offernocd5 bidnocd5 offerno5 bidno5 dvol5 svol5 dcha5
    scha5 ddiff5 sdiff5 fwdvl ftradmdcha ftradmddiff fwsvl ftradmscha ftradmsdiff vol
    shcode value jvolume highyear highyeardate lowyear lowyeardate target capital abscnt
    parprice gsmm subprice total listdate name bfsales bfoperatingincome
    bfordinaryincome bfnetincome bfeps name2 bfsales2 bfoperatingincome2
    bfordinaryincome2 bfnetincome2 bfeps2 salert opert ordrt netrt epsrt info1 info2
    info3 info4 janginfo t_per tonghwa dval1 sval1 dval2 sval2 dval3 sval3 dval4 sval4
    dval5 sval5 davg1 savg1 davg2 savg2 davg3 savg3 davg4 savg4 davg5 savg5 ftradmdval
    ftradmsval ftradmdvag ftradmsvag info5 spac_gubun issueprice alloc_gubun alloc_text
    shterm_text svi_uplmtprice svi_dnlmtprice low_lqdt_gu abnormal_rise_gu lend_text
    ty_text nxt_janginfo nxt_shterm_text nxt_svi_uplmtprice nxt_svi_dnlmtprice ex_shcode
    krx_mcls_price
""".split())
# Token fields: LS token REST detail (sha256 4acff92cdcdfd551...) table and
# example; plus the generic envelope keys that gateway_status reads.
_ENVELOPE_FIELDS = frozenset(("rsp_cd", "rsp_msg", "error", "error_description"))
TOKEN_FIELDS = frozenset(("access_token", "expire_in", "expires_in", "scope",
                          "token_type")) | _ENVELOPE_FIELDS
QUOTE_FIELDS = frozenset(("t1102OutBlock",)) | _T1102_OUT_FIELDS | _ENVELOPE_FIELDS

# Synthetic t1102 payload for the preflight decode; not broker data.
_PREFLIGHT_PAYLOAD = (
    '{"rsp_cd":"00000","t1102OutBlock":{"shcode":"005930","price":72000,"volume":0}}'
)


def _now_ms() -> int:
    return time.time_ns() // 1_000_000


def _native_available() -> bool:
    """Decode a synthetic t1102 payload with the installed native module.

    A version check alone is not enough: an older or partial build can report
    a compatible core and still lack a working LS decoder (ChatGPT review of
    PR #27, M2). Any failure means "not available".
    """
    try:
        from ktradelink._native import decode_ticker_candidate
        ticker = decode_ticker_candidate("ls", "005930", "KRX", _PREFLIGHT_PAYLOAD)
        return ticker.last == Decimal("72000") and ticker.volume == 0
    except Exception:
        return False


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
    parser.add_argument("--show-gateway-message", action="store_true",
                        help="also print the gateway's error message (upstream text; "
                             "only your credentials and token are redacted from it)")
    return parser


def _describe(request: WireRequest, out: TextIO) -> None:
    """Method, origin, path and header *names* only; never values or body."""
    names = ", ".join(name for name, _ in request.headers)
    print(f"    {request.method} {request.origin}{request.path}", file=out)
    print(f"    header names: {names}", file=out)


def _report_shape(body: bytes, known: frozenset[str], out: TextIO) -> None:
    print("    response shape (documented field names and types only; "
          "other keys show as <key>):", file=out)
    for line in json_shape(body, known_keys=known):
        print(f"      {line}", file=out)


def _report_status(status: GatewayStatus | None, show_message: bool, out: TextIO) -> None:
    if status is None:
        return
    print(f"    gateway code: {status.code}", file=out)
    if status.message is None:
        return
    if show_message:
        print(f"    gateway message (upstream text, review before sharing): "
              f"{status.message}", file=out)
    else:
        print("    gateway message: hidden (rerun with --show-gateway-message to see it)",
              file=out)


def _report_transport_error(
    step: str, error: TransportError, show_message: bool, out: TextIO,
) -> None:
    print(f"[{step}] FAILED: {error.kind.value} (delivery: {error.delivery.value})", file=out)
    _report_status(error.diagnostic, show_message, out)


def _read_credentials(
    env: Mapping[str, str], ask_secret: Callable[[str], str], out: TextIO,
) -> CredentialPair | None:
    key = env.get(KEY_ENV) or ask_secret(f"LS app key ({KEY_ENV} not set): ")
    secret = env.get(SECRET_ENV) or ask_secret(f"LS app secret ({SECRET_ENV} not set): ")
    try:
        key, secret = key.strip(), secret.strip()
        pair = CredentialPair(key, secret)
    except (CredentialError, AttributeError):
        print("Credentials are empty or contain invalid characters.", file=out)
        return None
    if min(len(key), len(secret)) < MIN_CREDENTIAL_CHARS:
        print(f"Credentials shorter than {MIN_CREDENTIAL_CHARS} characters cannot be "
              "reliably redacted from output; refusing.", file=out)
        return None
    return pair


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
    if _native_available():
        print("native decoder: available (synthetic t1102 decode passed)", file=out)
    else:
        print("native decoder: NOT available - build it before --live "
              "(see docs/usage/live-smoke-ls.md)", file=out)
    print("No request sent.", file=out)
    return EXIT_OK


def _live(symbol: str, pair: CredentialPair, show_message: bool, out: TextIO) -> int:
    identity = CredentialIdentity("ls", "live", "smoke")
    provider = InMemoryCredentialProvider()
    provider.put(identity, pair)
    cache = InMemoryTokenCache()
    transport = HttpsTransport(network_enabled=True, collect_diagnostics=True)
    secrets = [pair.client_key, pair.client_secret]

    try:
        token_response = transport.send(build_token_request(identity, provider))
    except TransportError as error:
        _report_transport_error("1/2 token", error, show_message, out)
        return EXIT_FAILED
    try:
        lease = save_example_token_response(token_response, identity, provider, cache,
                                            now_ms=_now_ms())
    except TokenError as error:
        print(f"[1/2 token] FAILED: {error.kind.value}", file=out)
        _report_status(gateway_status(token_response.body, redact=secrets), show_message, out)
        _report_shape(token_response.body, TOKEN_FIELDS, out)
        return EXIT_FAILED
    remaining_s = max(0, (lease.expires_at_ms - _now_ms()) // 1000)
    print(f"[1/2 token] OK: bearer token received, valid for about {remaining_s} s", file=out)
    secrets.append(lease.access_token)

    plan = plan_ticker_request("ls", symbol, venue="KRX", environment="live")
    try:
        quote_response = transport.send(
            build_quote_request(plan, identity, provider, cache, now_ms=_now_ms()))
    except TransportError as error:
        _report_transport_error("2/2 quote", error, show_message, out)
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
        _report_status(gateway_status(quote_response.body, redact=secrets), show_message, out)
        _report_shape(quote_response.body, QUOTE_FIELDS, out)
        return EXIT_FAILED
    print(f"[2/2 quote] OK: {ticker.symbol} last={ticker.last} volume={ticker.volume}",
          file=out)
    print("    venue is the requested KRX; the t1102 response has no venue field.", file=out)
    print("    This is LS market data: check LS's terms before sharing it.", file=out)
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
        if args.yes or args.show_gateway_message:
            print("--yes and --show-gateway-message only apply together with --live.",
                  file=out)
            return EXIT_USAGE
        return _dry_run(args.symbol, out)
    if not _native_available():
        # Otherwise a token would be issued and the quote could not be decoded.
        print("The native LS decoder is missing or not working; build it first "
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
    return _live(args.symbol, pair, args.show_gateway_message, out)


if __name__ == "__main__":
    sys.exit(main())
