//! Synthetic fixtures following field names from official publisher documents.
//! These are NOT real authenticated brokerage responses.

use ktradelink_core::Venue;
use ktradelink_decoders::{decode_ticker_candidate as decode, Broker, DecodeKind};

fn offline(id: &str, json: &str) -> ktradelink_core::CoreTicker {
    let broker = Broker::parse(id).unwrap();
    decode(broker, "005930", Venue::Krx, json).unwrap()
}
fn last(id: &str, json: &str) -> String {
    offline(id, json).input().prices.last.as_ref().unwrap().as_str().to_owned()
}

#[test]
fn six_brokers_have_distinct_documented_candidate_fields() {
    assert_eq!(Broker::ALL.len(), 6);
    let samples = [
        ("kis", r#"{"rt_cd":"0","output":{"stck_prpr":"72000.00","stck_oprc":"71900","stck_hgpr":"72400","stck_lwpr":"71600","acml_vol":"0"}}"#),
        ("kiwoom", r#"{"return_code":0,"stk_cd":"005930","cur_prc":"72000.00","open_pric":"71900","high_pric":"72400","low_pric":"71600","trde_qty":"0"}"#),
        ("ls", r#"{"shcode":"005930","hname":"synthetic","price":72000}"#),
        ("db", r#"{"rsp_cd":"00000","Out":{"Prpr":"72000.00","Oprc":"71900","Hprc":"72400","Lprc":"71600","Sdpr":"70100"}}"#),
        ("toss", r#"{"result":[{"symbol":"005930","timestamp":"2026-03-25T09:30:00.123+09:00","lastPrice":"72000.00","currency":"KRW"}]}"#),
        ("meritz", r#"{"rsp_cd":"0000","data":{"stck_prpr":"72000.00","oprc":"71900","hprc":"72400","lprc":"71600","acml_vol":"0"}}"#),
    ];
    for (id, payload) in samples {
        let quote = offline(id, payload);
        assert_eq!(quote.input().broker, id);
        assert_eq!(quote.input().venue, Venue::Krx);
        assert_eq!(quote.input().timestamp, None);
        assert_eq!(quote.input().retrieved_at, None);
        assert_eq!(quote.input().prices.previous_close.as_ref().map(|p| p.as_str()), None);
        assert_eq!(quote.input().prices.bid.as_ref().map(|p| p.as_str()), None);
        assert_eq!(quote.input().prices.ask.as_ref().map(|p| p.as_str()), None);
        assert!(["72000.00", "72000"].contains(&last(id, payload).as_str()));
    }
}

#[test]
fn volume_null_and_zero_maintain_distinct_meanings() {
    let zero = offline("kis", r#"{"output":{"stck_prpr":"10","acml_vol":"0"}}"#);
    let absent = offline("kis", r#"{"output":{"stck_prpr":"10"}}"#);
    assert_eq!(zero.input().volume, Some(0));
    assert_eq!(absent.input().volume, None);
    let zero_int = offline("kiwoom", r#"{"cur_prc":"10","trde_qty":0}"#);
    assert_eq!(zero_int.input().volume, Some(0));
    assert_eq!(offline("db", r#"{"Out":{"Prpr":"10"}}"#).input().volume, None);
    assert_eq!(offline("toss", r#"{"result":[{"symbol":"005930","currency":"KRW","lastPrice":"10"}]}"#).input().volume, None);
}

#[test]
fn missing_optional_and_invalid_present_field_are_not_confused() {
    assert!(offline("kis", r#"{"output":{"stck_prpr":"10"}}"#).input().prices.open.is_none());
    let bad = decode(Broker::Kis, "005930", Venue::Krx, r#"{"output":{"stck_prpr":"10","stck_oprc":""}}"#).unwrap_err();
    assert_eq!(bad.field, "stck_oprc");
    assert_eq!(bad.kind, DecodeKind::InvalidPrice);
    let null = offline("meritz", r#"{"data":{"stck_prpr":"10","acml_vol":null}}"#);
    assert_eq!(null.input().volume, None);
}

#[test]
fn signed_kiwoom_prices_and_floating_point_inputs_are_not_guessed() {
    for val in ["-72000", "+72000", "1e3", "-0", "NaN"] {
        let payload = format!(r#"{{"cur_prc":"{val}"}}"#);
        let e = decode(Broker::Kiwoom, "005930", Venue::Krx, &payload).unwrap_err();
        assert_eq!(e.kind, DecodeKind::InvalidPrice);
        assert!(!e.to_string().contains(val));
    }
    for (id, payload) in [
        ("kis", r#"{"output":{"stck_prpr":72000.25}}"#),
        ("ls", r#"{"price":72000.25}"#),
        ("db", r#"{"Out":{"Prpr":72000.25}}"#),
    ] {
        let e = decode(Broker::parse(id).unwrap(), "005930", Venue::Krx, payload).unwrap_err();
        assert_eq!(e.kind, DecodeKind::InvalidPrice);
    }
}

#[test]
fn nested_duplicate_keys_and_malformed_envelopes_are_rejected() {
    for payload in [
        r#"{"output":{"stck_prpr":"10","stck_prpr":"11"}}"#,
        r#"{"output":{"stck_prpr":"10"},"output":{"stck_prpr":"11"}}"#,
        r#"{"output":{"stck_prpr":"10","extra":{"a":1,"a":2}}}"#,
        r#"{"output":{"stck_prpr": NaN}}"#,
        r#"{"output":[{"stck_prpr":"10"}]}"#,
        r#"[]"#,
        r#"{"output":null}"#,
    ] {
        assert!(decode(Broker::Kis, "005930", Venue::Krx, payload).is_err());
    }
}

#[test]
fn source_status_failures_do_not_leak_native_values() {
    for (id, payload) in [
        ("kis", r#"{"rt_cd":"secret-response","output":{"stck_prpr":"10"}}"#),
        ("kiwoom", r#"{"return_code":-1,"cur_prc":"10"}"#),
        ("db", r#"{"rsp_cd":"secret-response","Out":{"Prpr":"10"}}"#),
        ("meritz", r#"{"rsp_cd":"secret-response","data":{"stck_prpr":"10"}}"#),
    ] {
        let e = decode(Broker::parse(id).unwrap(), "005930", Venue::Krx, payload).unwrap_err();
        assert_eq!(e.kind, DecodeKind::SourceStatus);
        assert!(!e.to_string().contains("secret-response"));
    }
}

#[test]
fn toss_symbol_selection_is_exact_and_unambiguous() {
    let payload = r#"{"result":[{"symbol":"000660","currency":"KRW","lastPrice":"5"},{"symbol":"005930","currency":"KRW","lastPrice":"72.00"}]}"#;
    assert_eq!(last("toss", payload), "72.00");
    for payload in [
        r#"{"result":[{"symbol":"000660","currency":"KRW","lastPrice":"5"}]}"#,
        r#"{"result":[{"symbol":"005930","currency":"KRW","lastPrice":"2"},{"symbol":"005930","currency":"KRW","lastPrice":"3"}]}"#,
        r#"{"result":[{"symbol":"005930","currency":"USD","lastPrice":"2"}]}"#,
        r#"{"result":[{"symbol":"005930","currency":"KRW","lastPrice":"2","timestamp":12}]}"#,
        r#"{"result":{"symbol":"005930","currency":"KRW","lastPrice":"2"}}"#,
    ] {
        assert!(decode(Broker::Toss, "005930", Venue::Krx, payload).is_err());
    }
}

#[test]
fn request_symbol_mismatch_and_invalid_market_context_are_errors() {
    for (id, payload) in [
        ("kiwoom", r#"{"stk_cd":"000660","cur_prc":"10"}"#),
        ("ls", r#"{"shcode":"000660","price":"10"}"#),
    ] {
        let e = decode(Broker::parse(id).unwrap(), "005930", Venue::Krx, payload).unwrap_err();
        assert_eq!(e.kind, DecodeKind::AmbiguousSymbol);
    }
    let e = decode(Broker::Kis, "005930", Venue::Nxt, r#"{"output":{"stck_prpr":"10"}}"#).unwrap_err();
    assert_eq!(e.kind, DecodeKind::UnsupportedVenue);
    let e = decode(Broker::Kis, "005930", Venue::BrokerComposite, r#"{"output":{"stck_prpr":"10"}}"#).unwrap_err();
    assert_eq!(e.kind, DecodeKind::UnsupportedVenue);
    assert!(Broker::parse("shinan").is_err());
}

#[test]
fn malformed_quantities_are_not_silently_coerced() {
    for value in [r#""-1""#, r#""1.5""#, r#"" 0""#, "true", "1.25", "-1"] {
        let payload = format!(r#"{{"output":{{"stck_prpr":"10","acml_vol":{value}}}}}"#);
        assert!(decode(Broker::Kis, "005930", Venue::Krx, &payload).is_err());
    }
    let overflow = r#"{"output":{"stck_prpr":"10","acml_vol":"18446744073709551616"}}"#;
    assert!(decode(Broker::Kis, "005930", Venue::Krx, overflow).is_err());
}

#[test]
fn oversized_input_and_untrusted_unknown_fields_do_not_enter_ticker() {
    let huge = " ".repeat(1_048_577);
    let e = decode(Broker::Kis, "005930", Venue::Krx, &huge).unwrap_err();
    assert_eq!(e.kind, DecodeKind::OversizedInput);
    let q = offline("kis", r#"{"output":{"stck_prpr":"10","access_token":"not-for-model"},"other":{"account":"not-for-model"}}"#);
    assert_eq!(q.input().prices.last.as_ref().unwrap().as_str(), "10");
    assert_eq!(q.input().prices.previous_close.as_ref().map(|p| p.as_str()), None);
}

#[test]
fn inputs_have_no_timestamp_inference_even_if_payload_has_one() {
    let quote = offline("toss", r#"{"result":[{"symbol":"005930","currency":"KRW","lastPrice":"10","timestamp":"2026-03-25T09:30:00.123+09:00"}]}"#);
    assert_eq!(quote.input().timestamp, None);
    assert_eq!(quote.input().retrieved_at, None);
}
