"""Unencodable credentials and tokens never surface inside an exception.

A lone surrogate is a valid Python ``str`` and passes ``CredentialPair``, but
it cannot be UTF-8 encoded. ``UnicodeEncodeError.object`` would then hold the
whole secret. Offline only; every value is synthetic.
"""

import json
import traceback

import pytest

from ktradelink._credential_runtime import (
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._https_transport import TransportError, TransportFailure, build_token_request
from ktradelink._token_codec import TokenError, TokenFailure, save_example_token_response

LONE = "\ud800"


@pytest.mark.parametrize("broker", ["ls", "db", "toss"])
@pytest.mark.parametrize("which", ["key", "secret"])
def test_unencodable_form_credentials_fail_with_a_static_error(broker, which):
    key, secret = "SYNTHETIC_KEY", "SYNTHETIC_SECRET"
    if which == "key":
        key += LONE
    else:
        secret += LONE
    identity = CredentialIdentity(broker, "live", "synthetic")
    provider = InMemoryCredentialProvider()
    provider.put(identity, CredentialPair(key, secret))
    with pytest.raises(TransportError) as caught:
        build_token_request(identity, provider)
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
    assert caught.value.__context__ is None and caught.value.__cause__ is None
    rendered = "".join(traceback.format_exception(caught.value))
    assert "SYNTHETIC_KEY" not in rendered and "SYNTHETIC_SECRET" not in rendered


DB = {"scope": "oob", "token_type": "Bearer", "expires_in": 86400}
TOSS = {"token_type": "Bearer", "expires_in": 86400}
ACKS = {"db_production_key_acknowledged": True, "db_no_prior_token_acknowledged": True}


@pytest.mark.parametrize("broker,fields,extra", [("db", DB, ACKS), ("toss", TOSS, {})])
@pytest.mark.parametrize("token", [
    "SYNTHETIC" + LONE,   # JSON "\ud800" escape
    "SYNTHETIC TOKEN",
    "SYNTHETIC\tTOKEN",
    "SYNTHETIC\x7fTOKEN",
    "SYNTHETIC토큰",
])
def test_db_and_toss_tokens_must_fit_a_bearer_header(
        broker, fields, extra, token, receive_token_response):
    identity = CredentialIdentity(broker, "live", "synthetic")
    provider = InMemoryCredentialProvider()
    provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    body = json.dumps(fields | {"access_token": token}).encode("ascii")
    response = receive_token_response(build_token_request(identity, provider), body)
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                    now_ms=0, **extra)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None
