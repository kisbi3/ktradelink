"""Publisher-example tokens are synthetic; no token is ever issued over the network."""

import json
from datetime import datetime, timedelta, timezone

import pytest

from ktradelink._credential_runtime import (
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._https_transport import WireResponse, build_token_request
from ktradelink._token_codec import TokenError, TokenFailure, save_example_token_response

KST = timezone(timedelta(hours=9))


def setup(broker):
    identity=CredentialIdentity(broker,'live','example')
    provider=InMemoryCredentialProvider()
    provider.put(identity,CredentialPair('NOT_REAL_APP_KEY','NOT_REAL_SECRET'))
    request=build_token_request(identity,provider)
    return identity,provider,request


@pytest.mark.parametrize('broker,fields',[
    ('kis', {'access_token':'SYNTHETIC_KIS','access_token_token_expired':'2027-01-02 12:01:03'}),
    ('kiwoom',{'token':'SYNTHETIC_KIWOOM','expires_dt':'20270102120103','return_code':0}),
])
def test_token_example_parses_exact_publisher_expiry_and_scoped_cache(broker,fields):
    identity,provider,req=setup(broker)
    cache=InMemoryTokenCache()
    response=WireResponse(req,200,json.dumps(fields).encode('utf-8'))
    issued=save_example_token_response(response,identity,provider,cache,now_ms=0)
    expected=int(datetime(2027,1,2,12,1,3,tzinfo=KST).timestamp()*1000)
    assert issued.expires_at_ms==expected
    assert cache.get(provider,identity,now_ms=expected-1) is issued
    with pytest.raises(Exception):
        cache.get(provider,identity,now_ms=expected)
    assert 'SYNTHETIC_KIS' not in repr(issued) and 'SYNTHETIC_KIWOOM' not in repr(issued)


@pytest.mark.parametrize('broker,fields',[
 ('kis',{}),('kis',{'access_token':'X','access_token_token_expired':'not time'}),
 ('kis',{'access_token':'X','access_token_token_expired':'2027-01-02 12:01:03','token_type':'MAC'}),
 ('kiwoom',{'token':'X','expires_dt':'invalid'}),
 ('kiwoom',{'token':'X','expires_dt':'20270102120103','return_code':1}),
 ('kiwoom',{'token':'X','expires_dt':'20270102120103','return_code':True}),
])
def test_invalid_response_never_cache_or_expose_body(broker,fields):
    identity,p,req=setup(broker)
    cache=InMemoryTokenCache()
    response=WireResponse(req,200,json.dumps(fields).encode('utf-8'))
    with pytest.raises(TokenError) as error:
        save_example_token_response(response,identity,p,cache,now_ms=0)
    assert error.value.kind is TokenFailure.INVALID_RESPONSE
    assert error.value.__context__ is None
    assert 'SYNTHETIC' not in str(error.value)
    with pytest.raises(Exception):cache.get(p,identity,now_ms=0)


def test_stale_credentials_cannot_bind_token_returned_after_rotation():
    identity,p,req=setup('kiwoom')
    p.put(identity,CredentialPair('ROTATED_KEY','ROTATED_SECRET'))
    response=WireResponse(req,200,b'{"token":"X","expires_dt":"20270102120103"}')
    with pytest.raises(TokenError) as error:
        save_example_token_response(response,identity,p,InMemoryTokenCache(),now_ms=0)
    assert error.value.kind is TokenFailure.STALE_CREDENTIAL


def test_malformed_utf8_and_non_dict_response_are_static():
    identity,p,req=setup('kis')
    for data in (b'\xff', b'[]', b'SYNTHETIC_BAD_PAYLOAD', b'{}'):
        with pytest.raises(TokenError) as error:
            save_example_token_response(WireResponse(req,200,data),identity,p,
                                        InMemoryTokenCache(),now_ms=0)
        assert error.value.kind is TokenFailure.INVALID_RESPONSE
        assert error.value.__context__ is None


def test_status_must_be_exactly_200_and_no_guess_on_missing_fields():
    identity,p,req=setup('kis')
    for status in (201,204,206,302,401,429):
        with pytest.raises(TokenError):
            save_example_token_response(WireResponse(req,status,b'{}'),identity,p,
                                        InMemoryTokenCache(),now_ms=0)


@pytest.mark.parametrize("body", [
    b'{"access_token":"A","access_token":"B","access_token_token_expired":"2027-01-02 12:01:03"}',
    b'{"access_token":"A","access_token_token_expired":"2027-01-02 12:01:03","meta":{"a":0,"a":1}}',
    b'{"access_token":"A","access_token_token_expired":"2027-01-02 12:01:03","extra":NaN}',
    b'{' + b' ' * (1_048_576 + 1) + b'}',
])
def test_duplicate_nonfinite_and_oversize_token_json_are_rejected(body):
    identity, provider, request = setup("kis")
    with pytest.raises(TokenError) as caught:
        save_example_token_response(WireResponse(request, 200, body), identity, provider,
                                    InMemoryTokenCache(), now_ms=0)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    assert caught.value.__context__ is None
