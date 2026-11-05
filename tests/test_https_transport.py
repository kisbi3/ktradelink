"""No socket, DNS, broker, account or token exchange is executed in these tests."""

import http.client
import ssl
import traceback
from types import SimpleNamespace

import pytest

from ktradelink._credential_runtime import (
    CredentialError,
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._https_transport import (
    MAX_RESPONSE_BYTES,
    DeliveryState,
    HttpsTransport,
    TransportError,
    TransportFailure,
    WireRequest,
    build_quote_request,
    build_token_request,
)
from ktradelink._request_plan import plan_ticker_request


def setup(broker="kis", environment="live"):
    p=InMemoryCredentialProvider()
    ident=CredentialIdentity(broker,environment,"test")
    s=p.put(ident,CredentialPair("SYNTHETIC-KEY","SYNTHETIC-SECRET"))
    return p,ident,s


@pytest.mark.parametrize("broker", ("kis","kiwoom"))
def test_token_request_is_publisher_example_json_not_query(broker):
    provider,ident,_=setup(broker)
    req=build_token_request(ident,provider)
    assert req.origin.startswith("https://") and not req.query
    assert req.method=="POST" and req.purpose=="token"
    assert b'"grant_type":"client_credentials"' in req.body
    assert b'SYNTHETIC-KEY' in req.body
    assert not any(s in repr(req) for s in ("SYNTHETIC-KEY","SYNTHETIC-SECRET"))
    assert req.path==("/oauth2/tokenP" if broker=="kis" else "/oauth2/token")


@pytest.mark.parametrize("broker",("db","toss","meritz"))
def test_brokers_with_unverified_token_wire_format_fail_closed(broker):
    p,ident,_=setup(broker)
    with pytest.raises(TransportError) as ex:
        build_token_request(ident,p)
    assert ex.value.kind is TransportFailure.EVIDENCE_MISSING


@pytest.mark.parametrize("broker",("kis","kiwoom"))
@pytest.mark.parametrize("environment",("live","paper"))
def test_quote_request_requires_current_token_and_matching_environment(broker,environment):
    p,ident,s=setup(broker,environment)
    tokens=InMemoryTokenCache()
    tokens.put(p,s,access_token="SYNTHETIC-TOKEN",expires_at_ms=200,now_ms=1)
    plan=plan_ticker_request(broker,"005930",venue="KRX",environment=environment)
    req=build_quote_request(plan,ident,p,tokens,now_ms=2)
    assert "SYNTHETIC-TOKEN" not in repr(req)
    auth=dict(req.headers)
    assert auth["authorization"]=="Bearer SYNTHETIC-TOKEN"
    assert bool("appkey" in auth)==(broker=="kis")
    assert req.purpose=="quote"
    with pytest.raises(TransportError):
        build_quote_request(plan,CredentialIdentity(broker, "paper" if environment=="live" else "live", "test"),p,tokens,now_ms=2)
    p.put(ident,CredentialPair("ROTATED", "ROTATED"))
    with pytest.raises(CredentialError):
        build_quote_request(plan,ident,p,tokens,now_ms=2)


def test_network_is_disabled_before_any_socket_or_dns(monkeypatch):
    p,ident,_=setup()
    req=build_token_request(ident,p)
    monkeypatch.setattr(http.client,"HTTPSConnection",lambda *args,**kw: pytest.fail("network created"))
    with pytest.raises(TransportError) as exc:
        HttpsTransport().send(req)
    assert exc.value.kind is TransportFailure.NOT_ENABLED
    assert exc.value.delivery is DeliveryState.NOT_SENT


class _StubResponse:
    def __init__(self, status=200, data=b'{}', read_failure=False):
        self.status=status
        self.data=data
        self.read_failure=read_failure
    def read(self, limit):
        if self.read_failure:
            raise RuntimeError('SECRET_SERVER_CONTENT')
        return self.data[:limit]


class _StubConnection:
    instances=[]
    def __init__(self, host,port,timeout,context):
        self.host=host
        self.port=port
        self.timeout=timeout
        self.context=context
        self.calls=[]
        self.closed=False
        self.behavior=SimpleNamespace(connect=None,write=None,headers=None,response=_StubResponse())
        self.__class__.instances.append(self)
    def connect(self):
        self.calls.append('connect')
        if self.behavior.connect:
            raise self.behavior.connect
    def request(self,method,target,body=None,headers=None):
        self.calls.append(('request',method,target,body,headers))
        if self.behavior.write:
            raise self.behavior.write
    def getresponse(self):
        self.calls.append('getresponse')
        if self.behavior.headers:
            raise self.behavior.headers
        return self.behavior.response
    def close(self):
        self.closed=True


def fake_network(monkeypatch):
    _StubConnection.instances.clear()
    monkeypatch.setattr(http.client,'HTTPSConnection',_StubConnection)
    return _StubConnection.instances


@pytest.mark.parametrize('broker',('kis','kiwoom'))
def test_explicit_opt_in_uses_system_tls_verify_hostname_no_proxy_no_retry(broker,monkeypatch):
    p,ident,_=setup(broker)
    req=build_token_request(ident,p)
    connections=fake_network(monkeypatch)
    response=HttpsTransport(network_enabled=True,timeout_ms=750).send(req)
    assert response.status==200 and response.body==b'{}'
    assert "SYNTHETIC" not in repr(response)
    assert len(connections)==1
    conn=connections[0]
    assert conn.context.verify_mode is ssl.CERT_REQUIRED
    assert conn.context.check_hostname is True
    assert conn.host==req.origin.split('://')[1].split(':')[0]
    assert conn.timeout==.75 and conn.closed
    assert conn.calls[0]=='connect'
    assert conn.calls[1][0]=='request'
    assert conn.calls.count('getresponse')==1
    assert conn.calls[1][2]==req.path
    assert conn.calls[1][4]['content-type'].startswith('application/json')


@pytest.mark.parametrize('status,kind',[
(201,TransportFailure.HTTP),(204,TransportFailure.HTTP),(206,TransportFailure.HTTP),
(301,TransportFailure.REDIRECT),(302,TransportFailure.REDIRECT),
(401,TransportFailure.UNAUTHORIZED),(403,TransportFailure.FORBIDDEN),
(429,TransportFailure.RATE_LIMITED),(500,TransportFailure.SERVER),(503,TransportFailure.SERVER)
])
def test_http_status_classification_is_received_never_retry(status,kind,monkeypatch):
    p,ident,_=setup()
    req=build_token_request(ident,p)
    instances=fake_network(monkeypatch)
    previous=_StubConnection.__init__
    def configured(self,*a,**kw):
        previous(self,*a,**kw)
        self.behavior.response=_StubResponse(status,b'SECRET_SERVER_CONTENT')
    monkeypatch.setattr(_StubConnection,'__init__',configured)
    with pytest.raises(TransportError) as exc:
        HttpsTransport(network_enabled=True).send(req)
    assert exc.value.kind is kind and exc.value.delivery is DeliveryState.RESPONSE_RECEIVED
    assert len(instances)==1 and instances[0].closed
    assert 'SECRET' not in repr(exc.value)


@pytest.mark.parametrize('phase,kind,state',[
('connect',TransportFailure.CONNECT,DeliveryState.NOT_SENT),
('write',TransportFailure.WRITE,DeliveryState.UNKNOWN),
('headers',TransportFailure.RESPONSE,DeliveryState.UNKNOWN),
('read',TransportFailure.READ,DeliveryState.RESPONSE_RECEIVED),
])
def test_network_phase_classifies_send_ambiguity_without_leak(phase,kind,state,monkeypatch):
    p,ident,_=setup()
    req=build_token_request(ident,p)
    instances=fake_network(monkeypatch)
    old=_StubConnection.__init__
    def setup_stub(self,*args,**kwargs):
        old(self,*args,**kwargs)
        if phase == 'read':
            self.behavior.response = _StubResponse(read_failure=True)
        else:
            setattr(self.behavior, phase, ValueError('SYNTHETIC-SECRET'))
    monkeypatch.setattr(_StubConnection,'__init__',setup_stub)
    with pytest.raises(TransportError) as exc:
        HttpsTransport(network_enabled=True).send(req)
    assert exc.value.kind is kind and exc.value.delivery is state
    assert exc.value.__context__ is None and exc.value.__cause__ is None
    assert 'SYNTHETIC-SECRET' not in ''.join(traceback.format_exception(exc.value))
    assert len(instances)==1 and instances[0].closed


def test_explicit_tls_failure_does_not_degrade_to_no_verification(monkeypatch):
    p,ident,_=setup()
    req=build_token_request(ident,p)
    instances=fake_network(monkeypatch)
    old=_StubConnection.__init__
    def setup_stub(self,*args,**kwargs):
        old(self,*args,**kwargs)
        self.behavior.connect=ssl.SSLError('SYNTHETIC-SECRET')
    monkeypatch.setattr(_StubConnection,'__init__',setup_stub)
    with pytest.raises(TransportError) as exc:
        HttpsTransport(network_enabled=True).send(req)
    assert exc.value.kind is TransportFailure.TLS and exc.value.delivery is DeliveryState.NOT_SENT
    assert instances[0].closed


def test_response_size_cap_and_encoding_are_static(monkeypatch):
    p,ident,_=setup()
    req=build_token_request(ident,p)
    fake_network(monkeypatch)
    old=_StubConnection.__init__
    def setup_stub(self,*args,**kwargs):
        old(self,*args,**kwargs)
        self.behavior.response=_StubResponse(data=b'X'*(MAX_RESPONSE_BYTES+2))
    monkeypatch.setattr(_StubConnection,'__init__',setup_stub)
    with pytest.raises(TransportError) as ex:
        HttpsTransport(network_enabled=True).send(req)
    assert ex.value.kind is TransportFailure.OVERSIZED


def test_no_arbitrary_host_or_path_from_a_forged_plan():
    p,ident,_=setup()
    req=build_token_request(ident,p)
    with pytest.raises(TransportError):
        WireRequest(req.source,'POST','https://another.example',req.path,(),req.headers,req.body,'token',credential_snapshot=req.credential_snapshot)
    with pytest.raises(TransportError):
        WireRequest(req.source,'POST',req.origin,'/orders',(),req.headers,req.body,'token',credential_snapshot=req.credential_snapshot)


@pytest.mark.parametrize('ms',[0,-1,True,60001,1.5,'60'])
def test_bad_timeouts_and_network_flags_rejected(ms):
    with pytest.raises(TransportError):
        HttpsTransport(timeout_ms=ms)


def test_proxy_environment_does_not_provide_destinations_or_credential(monkeypatch):
    monkeypatch.setenv('HTTPS_PROXY','https://SYNTHETIC-SECRET@somewhere.invalid')
    p,ident,_=setup()
    req=build_token_request(ident,p)
    fake_network(monkeypatch)
    result=HttpsTransport(network_enabled=True).send(req)
    assert result.status==200
    assert all('SYNTHETIC-SECRET@somewhere' not in repr(x) for x in _StubConnection.instances)
