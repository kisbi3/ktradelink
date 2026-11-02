"""Six-broker OFFLINE source-shaped contract tests. No account or network calls."""

import json
from dataclasses import FrozenInstanceError
from decimal import Decimal

import _ktradelink_native as native
import pytest

from ktradelink._native import decode_ticker_candidate
from ktradelink.models import Ticker

SYNTHETIC = {
    "kis": {"rt_cd": "0", "output": {"stck_prpr": "72000.00", "stck_oprc": "71000",
                                   "stck_hgpr": "72500", "stck_lwpr": "70500",
                                   "acml_vol": "0"}},
    "kiwoom": {"return_code": 0, "stk_cd": "005930", "cur_prc": "72000.00",
               "open_pric": "71000", "high_pric": "72500", "low_pric": "70500",
               "trde_qty": "0"},
    "ls": {"shcode": "005930", "hname": "synthetic", "price": 72000},
    "db": {"rsp_cd": "00000", "Out": {"Prpr": "72000.00", "Oprc": "71000",
                                    "Hprc": "72500", "Lprc": "70500", "Sdpr": "70000"}},
    "toss": {"result": [{"symbol": "005930", "timestamp": "2026-03-25T09:30:00.123+09:00",
                         "lastPrice": "72000.00", "currency": "KRW"}]},
    "meritz": {"rsp_cd": "0000", "data": {"stck_prpr": "72000.00", "oprc": "71000",
                                         "hprc": "72500", "lprc": "70500",
                                         "acml_vol": "0"}},
}


@pytest.mark.parametrize("broker", list(SYNTHETIC))
def test_six_broker_candidates_return_exact_existing_ticker(broker: str) -> None:
    payload = json.dumps(SYNTHETIC[broker], ensure_ascii=False)
    quote = decode_ticker_candidate(broker, "005930", "KRX", payload)
    assert type(quote) is Ticker
    assert quote.broker == broker
    assert quote.symbol == "005930"
    assert quote.venue == "KRX"
    assert quote.last == Decimal("72000")
    assert quote.timestamp is None and quote.retrieved_at is None
    assert quote.previous_close is None and quote.bid is None and quote.ask is None
    assert quote.info == {}
    assert not hasattr(quote, "to_dict")
    assert not hasattr(quote, "__dict__")
    with pytest.raises(FrozenInstanceError):
        quote.last = Decimal("100")

    if broker in {"kis", "kiwoom", "meritz"}:
        assert quote.volume == 0
        assert quote.open == Decimal("71000")
        assert quote.high == Decimal("72500")
        assert quote.low == Decimal("70500")
    elif broker == "db":
        assert quote.volume is None  # DB example has NO volume field.
        assert quote.open == Decimal("71000")
    else:
        assert quote.volume is None  # Neither LS onboarding nor Toss PriceResponse.
        assert quote.open is None


@pytest.mark.parametrize("broker", ["kis", "kiwoom", "db", "toss", "meritz"])
def test_price_decimal_scale_preserved_across_rust_and_python(broker: str) -> None:
    original = "9007199254740993.1234567890123456789000"
    data = json.loads(json.dumps(SYNTHETIC[broker]))
    if broker == "kis":
        data["output"]["stck_prpr"] = original
    elif broker == "kiwoom":
        data["cur_prc"] = original
    elif broker == "db":
        data["Out"]["Prpr"] = original
    elif broker == "toss":
        data["result"][0]["lastPrice"] = original
    else:
        data["data"]["stck_prpr"] = original
    quote = decode_ticker_candidate(broker, "005930", "KRX", json.dumps(data))
    assert quote.last.as_tuple() == Decimal(original).as_tuple()


def test_no_implicit_venue_fallback_and_no_bad_signed_kiwoom_abs() -> None:
    payload = json.dumps(SYNTHETIC["kiwoom"])
    with pytest.raises(ValueError, match="venue"):
        decode_ticker_candidate("kiwoom", "005930", "NXT", payload)
    with pytest.raises(ValueError, match="venue"):
        decode_ticker_candidate("kiwoom", "005930", "BROKER_COMPOSITE", payload)
    with pytest.raises(ValueError, match="cur_prc"):
        decode_ticker_candidate("kiwoom", "005930", "KRX", '{"cur_prc":"-72000"}')


def test_toss_exact_match_required_and_currency_rejected() -> None:
    record = {
        "result": [
            {"symbol": "000660", "currency": "KRW", "lastPrice": "100"},
            {"symbol": "005930", "currency": "KRW", "lastPrice": "200.00"},
        ]
    }
    quote = decode_ticker_candidate("toss", "005930", "KRX", json.dumps(record))
    assert quote.last.as_tuple() == Decimal("200.00").as_tuple()
    record["result"][1]["currency"] = "USD"
    with pytest.raises(ValueError, match="currency"):
        decode_ticker_candidate("toss", "005930", "KRX", json.dumps(record))
    record["result"][1]["currency"] = "KRW"
    record["result"].append(dict(record["result"][1]))
    with pytest.raises(ValueError, match="symbol"):
        decode_ticker_candidate("toss", "005930", "KRX", json.dumps(record))


def test_duplicate_key_and_leaked_metadata_blocked() -> None:
    with pytest.raises(ValueError, match="payload"):
        decode_ticker_candidate(
            "kis", "005930", "KRX",
            '{"output":{"stck_prpr":"12","stck_prpr":"13"}}',
        )
    sample = json.loads(json.dumps(SYNTHETIC["kis"]))
    sample["output"]["access_token"] = "synthetic-marker-not-a-real-token"
    quote = decode_ticker_candidate("kis", "005930", "KRX", json.dumps(sample))
    assert quote.info == {}
    assert "synthetic-marker-not-a-real-token" not in repr(quote)


def test_missing_field_is_not_zero_and_wrong_status_rejected() -> None:
    with pytest.raises(ValueError, match="Prpr"):
        decode_ticker_candidate("db", "005930", "KRX", '{"rsp_cd":"00000","Out":{}}')
    with pytest.raises(ValueError, match="rsp_cd"):
        decode_ticker_candidate(
            "db", "005930", "KRX",
            '{"rsp_cd":"FORBIDDEN","Out":{"Prpr":"10"}}',
        )


def test_native_entry_point_and_private_wrapper_agree() -> None:
    payload = json.dumps(SYNTHETIC["meritz"])
    a = decode_ticker_candidate("meritz", "005930", "KRX", payload)
    b = native._decode_ticker_candidate("meritz", "005930", "KRX", payload)
    assert a == b and hash(a) == hash(b) and type(a) is Ticker
