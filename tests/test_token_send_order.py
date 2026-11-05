"""Token send-start anchoring, single-flight sends and send ordering.

Follow-ups to the ChatGPT reviews of PR #24/#25: the LS relative lifetime is
counted from a time the transport itself captured, and concurrent or
out-of-order token exchanges cannot cache an older token over a newer one.
Offline only: HTTPS connections are mocks and every value is synthetic.
"""

import http.client
import json
import threading
from dataclasses import replace
from unittest.mock import MagicMock

import pytest

from ktradelink._credential_runtime import (
    CredentialError,
    CredentialFailure,
    CredentialIdentity,
    CredentialPair,
    InMemoryCredentialProvider,
    InMemoryTokenCache,
)
from ktradelink._https_transport import (
    DeliveryState,
    HttpsTransport,
    TransportError,
    TransportFailure,
    WireResponse,
    _token_send_attestation,
    build_quote_request,
    build_token_request,
)
from ktradelink._request_plan import plan_ticker_request
from ktradelink._token_codec import TokenError, TokenFailure, save_example_token_response

LS_BODY = json.dumps({"access_token": "SYNTHETIC_LS", "scope": "oob",
                      "token_type": "Bearer", "expires_in": 86400}).encode()
KIWOOM_BODY = json.dumps({"token": "SYNTHETIC_KIWOOM", "token_type": "Bearer",
                          "return_code": 0, "expires_dt": "20991231235959"}).encode()


def _setup(broker="ls", profile="order"):
    identity = CredentialIdentity(broker, "live", profile)
    provider = InMemoryCredentialProvider()
    provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    return identity, provider


def _assert_cache_empty(cache, provider, identity):
    with pytest.raises(CredentialError) as missing:
        cache.get(provider, identity, now_ms=0)
    assert missing.value.kind is CredentialFailure.TOKEN_MISSING


# --- LS lifetime anchor ---------------------------------------------------

@pytest.mark.parametrize("caller_now_ms", [0, 1_500, 3_000_000])
def test_ls_lifetime_counts_from_the_transport_reading_before_the_write(
        caller_now_ms, receive_token_response):
    identity, provider = _setup()
    # Pre-connect reading 1_000, reading after TLS and before the write 1_500.
    response = receive_token_response(build_token_request(identity, provider), LS_BODY,
                                      clock=(1_000, 1_500))
    assert _token_send_attestation(response).send_start_ms == 1_500
    lease = save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                        now_ms=caller_now_ms)
    # Neither an earlier nor a later caller clock moves the expiry.
    assert lease.expires_at_ms == 1_500 + 86_400_000


def test_ls_expiry_already_past_by_caller_clock_is_not_cached(receive_token_response):
    identity, provider = _setup()
    response = receive_token_response(build_token_request(identity, provider), LS_BODY,
                                      clock=(1_000, 1_500))
    cache = InMemoryTokenCache()
    with pytest.raises(TokenError) as caught:
        save_example_token_response(response, identity, provider, cache,
                                    now_ms=1_500 + 86_400_000)
    assert caught.value.kind is TokenFailure.INVALID_RESPONSE
    _assert_cache_empty(cache, provider, identity)


# --- attestation ----------------------------------------------------------

@pytest.mark.parametrize("broker,body", [("ls", LS_BODY), ("kiwoom", KIWOOM_BODY)])
def test_response_not_received_by_the_transport_is_never_cached(broker, body):
    identity, provider = _setup(broker)
    cache = InMemoryTokenCache()
    fabricated = WireResponse(build_token_request(identity, provider), 200, body)
    with pytest.raises(TokenError) as caught:
        save_example_token_response(fabricated, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.UNATTESTED
    assert caught.value.__context__ is None
    _assert_cache_empty(cache, provider, identity)


def test_a_copy_of_an_attested_response_is_not_attested(receive_token_response):
    identity, provider = _setup()
    received = receive_token_response(build_token_request(identity, provider), LS_BODY)
    for copy in (replace(received), WireResponse(received.request, 200, received.body)):
        assert copy is not received and _token_send_attestation(copy) is None
        with pytest.raises(TokenError) as caught:
            save_example_token_response(copy, identity, provider, InMemoryTokenCache(),
                                        now_ms=0)
        assert caught.value.kind is TokenFailure.UNATTESTED


def test_quote_responses_carry_no_token_attestation(receive_token_response):
    identity, provider = _setup()
    cache = InMemoryTokenCache()
    cache.put(provider, provider.load(identity), access_token="SYNTHETIC_TOKEN",
              expires_at_ms=10_000, now_ms=0)
    plan = plan_ticker_request("ls", "005930", venue="KRX", environment="live")
    quote = build_quote_request(plan, identity, provider, cache, now_ms=1)
    assert _token_send_attestation(receive_token_response(quote, b"{}")) is None


# --- send ordering ---------------------------------------------------------

def _two_sequential_responses(receive_token_response, broker="ls"):
    identity, provider = _setup(broker)
    body = LS_BODY if broker == "ls" else KIWOOM_BODY
    first = receive_token_response(build_token_request(identity, provider), body)
    second = receive_token_response(build_token_request(identity, provider), body)
    assert (_token_send_attestation(first).sequence
            < _token_send_attestation(second).sequence)
    return identity, provider, first, second


@pytest.mark.parametrize("broker", ["ls", "kiwoom"])
def test_a_token_from_an_earlier_send_never_replaces_a_later_one(
        broker, receive_token_response):
    identity, provider, first, second = _two_sequential_responses(
        receive_token_response, broker)
    cache = InMemoryTokenCache()
    newer = save_example_token_response(second, identity, provider, cache, now_ms=0)
    with pytest.raises(TokenError) as caught:
        save_example_token_response(first, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.SUPERSEDED
    assert caught.value.__context__ is None
    assert cache.get(provider, identity, now_ms=0) is newer


def test_in_order_saves_and_a_repeated_save_are_accepted(receive_token_response):
    identity, provider, first, second = _two_sequential_responses(receive_token_response)
    cache = InMemoryTokenCache()
    save_example_token_response(first, identity, provider, cache, now_ms=0)
    newer = save_example_token_response(second, identity, provider, cache, now_ms=0)
    again = save_example_token_response(second, identity, provider, cache, now_ms=0)
    assert newer.issue_sequence == again.issue_sequence
    assert cache.get(provider, identity, now_ms=0) is again


def test_ordering_does_not_cross_a_credential_rotation(receive_token_response):
    identity, provider, first, second = _two_sequential_responses(receive_token_response)
    provider.put(identity, CredentialPair("ROTATED_KEY", "ROTATED_SECRET"))
    for response in (second, first):
        with pytest.raises(TokenError) as caught:
            save_example_token_response(response, identity, provider, InMemoryTokenCache(),
                                        now_ms=0)
        assert caught.value.kind is TokenFailure.STALE_CREDENTIAL


def _ls_body(lifetime_s):
    return json.dumps({"access_token": f"SYNTHETIC_LS_{lifetime_s}", "scope": "oob",
                       "token_type": "Bearer", "expires_in": lifetime_s}).encode()


def test_older_send_stays_out_after_the_newer_lease_expires(receive_token_response):
    # ChatGPT review of PR #26, M1: the order record must outlive the lease.
    identity, provider = _setup()
    older = receive_token_response(build_token_request(identity, provider), _ls_body(86400),
                                   clock=(1_000, 1_000))
    newer = receive_token_response(build_token_request(identity, provider), _ls_body(1),
                                   clock=(1_000, 1_000))
    cache = InMemoryTokenCache()
    save_example_token_response(newer, identity, provider, cache, now_ms=1_000)
    _assert_cache_empty_at(cache, provider, identity, 2_000)  # evicts the newer lease
    with pytest.raises(TokenError) as caught:
        save_example_token_response(older, identity, provider, cache, now_ms=2_001)
    assert caught.value.kind is TokenFailure.SUPERSEDED
    _assert_cache_empty_at(cache, provider, identity, 2_001)


def test_revoke_blocks_replay_until_a_new_send(receive_token_response):
    identity, provider, first, second = _two_sequential_responses(receive_token_response)
    cache = InMemoryTokenCache()
    save_example_token_response(second, identity, provider, cache, now_ms=0)
    cache.revoke(provider, identity)
    for replay in (second, first):  # the revoked response itself, and an older one
        with pytest.raises(TokenError) as caught:
            save_example_token_response(replay, identity, provider, cache, now_ms=0)
        assert caught.value.kind is TokenFailure.SUPERSEDED
    _assert_cache_empty(cache, provider, identity)
    fresh = receive_token_response(build_token_request(identity, provider), LS_BODY)
    lease = save_example_token_response(fresh, identity, provider, cache, now_ms=0)
    assert cache.get(provider, identity, now_ms=0) is lease


def test_a_manual_lease_does_not_reset_send_order(receive_token_response):
    identity, provider, first, second = _two_sequential_responses(receive_token_response)
    cache = InMemoryTokenCache()
    save_example_token_response(second, identity, provider, cache, now_ms=0)
    cache.revoke(provider, identity)
    cache.put(provider, provider.load(identity), access_token="SYNTHETIC_MANUAL",
              expires_at_ms=10_000, now_ms=0)
    with pytest.raises(TokenError) as caught:
        save_example_token_response(first, identity, provider, cache, now_ms=0)
    assert caught.value.kind is TokenFailure.SUPERSEDED


def test_rotation_keeps_old_responses_out_and_lets_new_sends_in(receive_token_response):
    identity, provider, first, second = _two_sequential_responses(receive_token_response)
    cache = InMemoryTokenCache()
    save_example_token_response(second, identity, provider, cache, now_ms=0)
    provider.put(identity, CredentialPair("ROTATED_KEY", "ROTATED_SECRET"))
    for old in (first, second):
        with pytest.raises(TokenError) as caught:
            save_example_token_response(old, identity, provider, cache, now_ms=0)
        assert caught.value.kind is TokenFailure.STALE_CREDENTIAL
    rotated = receive_token_response(build_token_request(identity, provider), LS_BODY)
    lease = save_example_token_response(rotated, identity, provider, cache, now_ms=0)
    assert cache.get(provider, identity, now_ms=0) is lease


def _assert_cache_empty_at(cache, provider, identity, now_ms):
    with pytest.raises(CredentialError) as missing:
        cache.get(provider, identity, now_ms=now_ms)
    assert missing.value.kind is CredentialFailure.TOKEN_MISSING


@pytest.mark.parametrize("sequence", [0, -1, True, 1.0, "1"])
def test_issue_sequence_must_be_a_positive_int(sequence):
    identity, provider = _setup()
    with pytest.raises(CredentialError) as caught:
        InMemoryTokenCache().put(provider, provider.load(identity), access_token="T",
                                 expires_at_ms=10, now_ms=0, issue_sequence=sequence)
    assert caught.value.kind is CredentialFailure.INVALID


# --- single flight -----------------------------------------------------------

class _BlockingConnection:
    """First connection blocks inside connect() until released."""

    def __init__(self):
        self.entered = threading.Event()
        self.release = threading.Event()
        self.created = 0

    def __call__(self, *args, **kwargs):
        self.created += 1
        conn = MagicMock()
        conn.getresponse.return_value.status = 200
        conn.getresponse.return_value.read.return_value = LS_BODY
        conn.getresponse.return_value.length = None
        if self.created == 1:
            def connect():
                self.entered.set()
                assert self.release.wait(5)
            conn.connect.side_effect = connect
        return conn


def test_second_concurrent_token_send_for_the_same_credentials_is_refused(monkeypatch):
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 1_000)
    factory = _BlockingConnection()
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    identity, provider = _setup()
    other_identity = CredentialIdentity("ls", "live", "other")
    provider.put(other_identity, CredentialPair("SYNTHETIC_KEY2", "SYNTHETIC_SECRET2"))
    transport = HttpsTransport(network_enabled=True)
    results = []
    worker = threading.Thread(target=lambda: results.append(
        transport.send(build_token_request(identity, provider))))
    worker.start()
    try:
        assert factory.entered.wait(5)
        # Same provider and identity, even through another transport: refused.
        with pytest.raises(TransportError) as caught:
            HttpsTransport(network_enabled=True).send(build_token_request(identity, provider))
        assert caught.value.kind is TransportFailure.TOKEN_IN_FLIGHT
        assert caught.value.delivery is DeliveryState.NOT_SENT
        assert factory.created == 1  # refused before any connection was made
        # A different identity is not blocked.
        assert transport.send(build_token_request(other_identity, provider)).status == 200
    finally:
        factory.release.set()
        worker.join(5)
    assert len(results) == 1 and results[0].status == 200
    # Released once the first send finished.
    assert transport.send(build_token_request(identity, provider)).status == 200


def test_another_provider_with_the_same_identity_is_not_blocked(monkeypatch):
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 1_000)
    factory = _BlockingConnection()
    monkeypatch.setattr(http.client, "HTTPSConnection", factory)
    identity, first_provider = _setup()
    second_provider = InMemoryCredentialProvider()
    second_provider.put(identity, CredentialPair("SYNTHETIC_KEY", "SYNTHETIC_SECRET"))
    worker = threading.Thread(target=lambda: HttpsTransport(network_enabled=True).send(
        build_token_request(identity, first_provider)))
    worker.start()
    try:
        assert factory.entered.wait(5)
        response = HttpsTransport(network_enabled=True).send(
            build_token_request(identity, second_provider))
        assert response.status == 200
    finally:
        factory.release.set()
        worker.join(5)


@pytest.mark.parametrize("failure", ["connect", "status"])
def test_in_flight_slot_is_released_after_a_failed_send(failure, monkeypatch):
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 1_000)
    identity, provider = _setup()
    conn = MagicMock()
    if failure == "connect":
        conn.connect.side_effect = OSError("SYNTHETIC_CONNECT_FAILURE")
    else:
        conn.getresponse.return_value.status = 500
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=conn))
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(build_token_request(identity, provider))
    assert caught.value.kind is not TransportFailure.TOKEN_IN_FLIGHT
    ok = MagicMock()
    ok.getresponse.return_value.status = 200
    ok.getresponse.return_value.read.return_value = LS_BODY
    ok.getresponse.return_value.length = None
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=ok))
    assert HttpsTransport(network_enabled=True).send(
        build_token_request(identity, provider)).status == 200


def test_disabled_or_invalid_sends_never_take_the_in_flight_slot(monkeypatch):
    identity, provider = _setup()
    request = build_token_request(identity, provider)
    with pytest.raises(TransportError) as caught:
        HttpsTransport().send(request)
    assert caught.value.kind is TransportFailure.NOT_ENABLED
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: -1)
    with pytest.raises(TransportError) as caught:
        HttpsTransport(network_enabled=True).send(request)
    assert caught.value.kind is TransportFailure.INVALID_REQUEST
    monkeypatch.setattr("ktradelink._https_transport._wall_clock_ms", lambda: 1_000)
    ok = MagicMock()
    ok.getresponse.return_value.status = 200
    ok.getresponse.return_value.read.return_value = LS_BODY
    ok.getresponse.return_value.length = None
    monkeypatch.setattr(http.client, "HTTPSConnection", MagicMock(return_value=ok))
    assert HttpsTransport(network_enabled=True).send(request).status == 200


# --- in-process locking -------------------------------------------------------

def test_concurrent_credential_puts_get_distinct_revisions():
    provider = InMemoryCredentialProvider()
    identities = [CredentialIdentity("ls", "live", f"p{n}") for n in range(8)]
    revisions: list[int] = []
    lock = threading.Lock()

    def rotate(identity):
        local = [provider.put(identity, CredentialPair("K", "S")).revision
                 for _ in range(200)]
        with lock:
            revisions.extend(local)

    threads = [threading.Thread(target=rotate, args=(i,)) for i in identities]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(10)
    assert len(revisions) == len(set(revisions)) == 8 * 200
