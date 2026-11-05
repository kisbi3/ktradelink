"""Install both wheels in a clean venv and test outside the checkout (all OSes)."""

import argparse
import os
import subprocess
import tempfile
import venv
from pathlib import Path

MISSING_CHECK = '''
import ktradelink
from decimal import Decimal
from ktradelink._offline_session import (
    CredentialScope,
    FailureKind,
    FakeCredentialProvider,
    FakeResponse,
    FakeTransport,
    FixtureOutcome,
    OfflineSessionError,
    execute_offline_quote,
)
from ktradelink.models import Ticker
from ktradelink._native import NativeCoreUnavailable, build_ticker, decode_ticker_candidate
from ktradelink._request_plan import (
    authentication_requirements, decode_offline_quote_response, plan_ticker_request
)
from ktradelink._credential_runtime import (
    CredentialIdentity, CredentialPair, InMemoryCredentialProvider,
)
from ktradelink._https_transport import (
    HttpsTransport, TransportError, TransportFailure, build_token_request,
)
identity = CredentialIdentity("kiwoom", "live", "wheel-smoke")
p = InMemoryCredentialProvider()
p.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
req = build_token_request(identity, p)
assert "SYNTHETIC_SECRET" not in repr(req)
try:
    HttpsTransport().send(req)
except TransportError as exc:
    assert exc.kind is TransportFailure.NOT_ENABLED
else:
    raise AssertionError("network-enabled default on installed wheel")
assert Ticker("005930", "KRX", "synthetic", Decimal(0)).last == 0
plan = plan_ticker_request("kis", "005930", venue="KRX", environment="live")
assert plan.method == "GET" and plan.transport_implemented is False
assert authentication_requirements("kis", environment="live").token_exchange_implemented is False
try:
    decode_offline_quote_response(plan, http_status=200, json_text="{}")
except NativeCoreUnavailable:
    pass
else:
    raise AssertionError("offline native decoder unexpectedly available")
scope = CredentialScope("kis", "live", 0)
provider = FakeCredentialProvider()
lease = provider.issue(scope, now_ms=0, lifetime_ms=100)
transport = FakeTransport((FakeResponse(plan, lease, 200, "{}", FixtureOutcome.SUCCESS),))
try:
    execute_offline_quote(plan, scope, provider, transport, now_ms=1)
except OfflineSessionError as exc:
    assert exc.kind is FailureKind.NATIVE_UNAVAILABLE
else:
    raise AssertionError("fake session silently replaced missing Rust decoder")
for operation in (
    lambda: build_ticker("005930", "KRX", "synthetic"),
    lambda: decode_ticker_candidate("kis", "005930", "KRX", "{}"),
):
    try:
        operation()
    except NativeCoreUnavailable:
        pass
    else:
        raise AssertionError("native extension unexpectedly present in fresh venv")
'''

INSTALLED_CHECK = '''
import sys
from decimal import Decimal
from pathlib import Path
import _ktradelink_native
import ktradelink
from ktradelink._native import build_ticker, core_version, decode_ticker_candidate
from ktradelink._request_plan import decode_offline_quote_response, plan_ticker_request
from ktradelink._offline_session import (
    CredentialScope,
    FailureKind,
    FakeCredentialProvider,
    FakeResponse,
    FakeTransport,
    FixtureOutcome,
    OfflineSessionError,
    execute_offline_quote,
)
from ktradelink.models import Ticker
from ktradelink._credential_runtime import (
    CredentialIdentity, CredentialPair, InMemoryCredentialProvider,
)
from ktradelink._https_transport import (
    HttpsTransport, TransportError, TransportFailure, build_token_request,
)
identity = CredentialIdentity("kiwoom", "live", "wheel-smoke")
p = InMemoryCredentialProvider()
p.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
req = build_token_request(identity, p)
assert "SYNTHETIC_SECRET" not in repr(req)
try:
    HttpsTransport().send(req)
except TransportError as exc:
    assert exc.kind is TransportFailure.NOT_ENABLED
else:
    raise AssertionError("network-enabled default on installed wheel")
root = Path(sys.prefix).resolve()
for module in (ktradelink, _ktradelink_native):
    assert Path(module.__file__).resolve().is_relative_to(root), module.__file__
text = "9007199254740993.123456789012345678900"
result = build_ticker("005930", "KRX", "synthetic", last=text, volume=0)
assert type(result) is Ticker
assert result.last.as_tuple() == Decimal(text).as_tuple()
assert result.volume == 0 and result.timestamp is None
assert result.info == {} and core_version() == "0.1.0"
examples = {
    "kis": '{"output":{"stck_prpr":"72000","acml_vol":"0"}}',
    "kiwoom": '{"cur_prc":"72000","trde_qty":"0"}',
    "ls": '{"rsp_cd":"00000","t1102OutBlock":{"shcode":"005930","price":72000,"volume":0}}',
    "db": '{"Out":{"Prpr":"72000"}}',
    "toss": '{"result":[{"symbol":"005930","currency":"KRW","lastPrice":"72000"}]}',
    "meritz": '{"data":{"stck_prpr":"72000","acml_vol":"0"}}',
}
for broker, payload in examples.items():
    quote = decode_ticker_candidate(broker, "005930", "KRX", payload)
    assert type(quote) is Ticker and quote.last == Decimal("72000")
    assert quote.broker == broker and quote.info == {}
    plan = plan_ticker_request(broker, "005930", venue="KRX", environment="live")
    new_quote = decode_offline_quote_response(plan, http_status=200, json_text=payload)
    assert type(new_quote) is Ticker and new_quote == quote
    assert plan.transport_implemented is False
    scope = CredentialScope(broker, "live", 0)
    provider = FakeCredentialProvider()
    lease = provider.issue(scope, now_ms=0, lifetime_ms=100)
    response = FakeResponse(plan, lease, 200, payload, FixtureOutcome.SUCCESS)
    transport = FakeTransport((response,))
    session_quote = execute_offline_quote(plan, scope, provider, transport, now_ms=1)
    assert type(session_quote) is Ticker and session_quote == quote
    assert transport.calls == 1
assert (Path(ktradelink.__file__).parent / "py.typed").is_file()
print("Isolated native wheel -> six offline decoder candidates -> existing Ticker: passed")
print("Isolated fake auth/transport -> six Rust decoders -> existing Ticker: passed")
'''


def only_wheel(directory: Path) -> Path:
    paths = list(directory.glob("*.whl"))
    if len(paths) != 1:
        raise ValueError(f"Expected exactly one wheel in {directory}")
    return paths[0].resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-dist", type=Path, required=True)
    parser.add_argument("--native-dist", type=Path, required=True)
    args = parser.parse_args()
    sdk = only_wheel(args.python_dist)
    native = only_wheel(args.native_dist)
    with tempfile.TemporaryDirectory(prefix="ktl-native-install-") as temp:
        root = Path(temp)
        env = root / "venv"
        venv.EnvBuilder(with_pip=True).create(env)
        python = env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        subprocess.run([str(python), "-m", "pip", "install", str(sdk)], check=True, cwd=root)
        subprocess.run([str(python), "-I", "-c", MISSING_CHECK], check=True, cwd=root)
        subprocess.run([str(python), "-m", "pip", "install", "--no-deps", str(native)], check=True, cwd=root)
        subprocess.run([str(python), "-I", "-c", INSTALLED_CHECK], check=True, cwd=root)


if __name__ == "__main__":
    main()
