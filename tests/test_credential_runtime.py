"""Offline synthetic tokens and caller-supplied placeholder secrets only."""

import pytest

from ktradelink._credential_runtime import (
    BearerLease,
    CredentialError,
    CredentialFailure,
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)

BROKERS = ("kis", "kiwoom", "ls", "db", "toss", "meritz")


def identity(broker="kis", environment="live", profile="example"):
    return CredentialIdentity(broker, environment, profile)


def test_secrets_are_explicit_and_redacted():
    c = CredentialPair("NOT_REAL_CLIENT_KEY", "NOT_REAL_SECRET")
    p = InMemoryCredentialProvider()
    s = p.put(identity(), c)
    cache = InMemoryTokenCache()
    lease = cache.put(p, s, access_token="SYNTHETIC_BEARER", expires_at_ms=25, now_ms=10)
    assert c.client_key == "NOT_REAL_CLIENT_KEY"
    assert c.client_secret == "NOT_REAL_SECRET"
    assert lease.access_token == "SYNTHETIC_BEARER"
    for obj in (c, p, s, cache, lease):
        dump = str(obj) + repr(obj)
        assert "NOT_REAL" not in dump and "SYNTHETIC_BEARER" not in dump


@pytest.mark.parametrize("broker", BROKERS)
def test_each_supported_broker_has_an_independent_key(broker):
    provider = InMemoryCredentialProvider()
    scope = identity(broker)
    snapshot = provider.put(scope, CredentialPair("key", "secret"))
    cache = InMemoryTokenCache()
    cache.put(provider, snapshot, access_token="fake", expires_at_ms=100, now_ms=0)
    assert cache.get(provider, scope, now_ms=10).snapshot is snapshot
    if broker in ("kis", "kiwoom"):
        other = identity(broker, "paper")
        with pytest.raises(CredentialError) as exc:
            provider.load(other)
        assert exc.value.kind is CredentialFailure.MISSING


def test_missing_or_expired_token_never_refreshes():
    provider = InMemoryCredentialProvider()
    cache = InMemoryTokenCache()
    scope = identity()
    snapshot = provider.put(scope, CredentialPair("key", "secret"))
    with pytest.raises(CredentialError) as exc:
        cache.get(provider, scope, now_ms=0)
    assert exc.value.kind is CredentialFailure.TOKEN_MISSING
    cache.put(provider, snapshot, access_token="synthetic", expires_at_ms=10, now_ms=0)
    assert cache.get(provider, scope, now_ms=9).access_token == "synthetic"
    for now in (10, 0):
        with pytest.raises(CredentialError) as exc:
            cache.get(provider, scope, now_ms=now)
        assert exc.value.kind is CredentialFailure.TOKEN_MISSING


def test_token_margin_is_fail_closed_and_drops_stale_entry():
    p = InMemoryCredentialProvider()
    ident = identity()
    snapshot = p.put(ident, CredentialPair("x", "y"))
    cache = InMemoryTokenCache()
    cache.put(p, snapshot, access_token="fake", expires_at_ms=200, now_ms=0)
    with pytest.raises(CredentialError):
        cache.get(p, ident, now_ms=190, min_remaining_ms=10)
    with pytest.raises(CredentialError):
        cache.get(p, ident, now_ms=1)


def test_rotation_revocation_and_provider_identity_are_separate():
    p1, p2 = InMemoryCredentialProvider(), InMemoryCredentialProvider()
    i = identity()
    s1 = p1.put(i, CredentialPair("k1", "s1"))
    s2 = p2.put(i, CredentialPair("k2", "s2"))
    cache = InMemoryTokenCache()
    cache.put(p1, s1, access_token="t1", expires_at_ms=100, now_ms=1)
    cache.put(p2, s2, access_token="t2", expires_at_ms=100, now_ms=1)
    assert cache.get(p2, i, now_ms=2).access_token == "t2"
    rotated = p1.put(i, CredentialPair("k3", "s3"))
    assert rotated.revision > s1.revision
    with pytest.raises(CredentialError) as exc:
        p1.require_current(s1)
    assert exc.value.kind is CredentialFailure.STALE
    with pytest.raises(CredentialError):
        cache.get(p1, i, now_ms=2)
    assert cache.get(p2, i, now_ms=2).access_token == "t2"
    cache.revoke(p2, i)
    with pytest.raises(CredentialError):
        cache.get(p2, i, now_ms=3)
    p1.clear(i)
    with pytest.raises(CredentialError):
        p1.load(i)


@pytest.mark.parametrize("profile", ["", "abc def", "a/b", "한글", "a"*65, None, 12, True])
def test_identity_profile_validation(profile):
    with pytest.raises(CredentialError):
        identity(profile=profile)


@pytest.mark.parametrize("broker,environment", [("unknown","live"),("db","paper"),("toss","paper"),("ls","paper"),("meritz","paper"),("kis","simulation")])
def test_unverified_environment_is_not_automatically_live(broker, environment):
    with pytest.raises(CredentialError):
        identity(broker, environment)


@pytest.mark.parametrize("key,secret", [('', 'ok'), ('ok',''), (True,'secret'),('a\nb','secret'),('a\x00b','secret'),('a'*4097,'s')])
def test_credential_values_reject_invalid_types_or_control_chars(key,secret):
    with pytest.raises(CredentialError):
        CredentialPair(key,secret)


@pytest.mark.parametrize("now,expires",[(0,0), (10,10),(-1,12),(10,True),(True,10),(10,-1)])
def test_token_expiry_is_strictly_future_time(now,expires):
    p=InMemoryCredentialProvider()
    s=p.put(identity(),CredentialPair('key','secret'))
    with pytest.raises(CredentialError):
        InMemoryTokenCache().put(p,s,access_token='fake',now_ms=now,expires_at_ms=expires)


def test_cross_provider_snapshot_and_stale_revision_refused():
    a,b=InMemoryCredentialProvider(),InMemoryCredentialProvider()
    scope=identity()
    snap=a.put(scope,CredentialPair('a','b'))
    with pytest.raises(CredentialError) as e:
        InMemoryTokenCache().put(b,snap,access_token='token',now_ms=1,expires_at_ms=10)
    assert e.value.kind is CredentialFailure.STALE
    a.put(scope,CredentialPair('a2','b2'))
    with pytest.raises(CredentialError):
        InMemoryTokenCache().put(a,snap,access_token='token',now_ms=1,expires_at_ms=10)


def test_bearer_lease_direct_construction_has_no_leak_or_invalid_clock():
    p=InMemoryCredentialProvider(); snap=p.put(identity(),CredentialPair('x','y'))
    with pytest.raises(CredentialError):
        BearerLease(snap,'bad\nheader',100)
    with pytest.raises(CredentialError):
        BearerLease(snap,'ok',True)
