//! Offline order-book decoder contracts. Fixtures under tests/fixtures/order_book
//! are SYNTHETIC values in publisher-documented field layouts, not market data.

use ktradelink_core::{CoreOrderBook, Venue};
use ktradelink_decoders::{
    decode_order_book_candidate as decode, Broker, DecodeError, DecodeKind, ORDER_BOOK_DEPTH,
};
use serde_json::{json, Value};

const KIS: &str = include_str!("../../../tests/fixtures/order_book/kis-fhkst01010200-synthetic.json");
const KIWOOM: &str = include_str!("../../../tests/fixtures/order_book/kiwoom-ka10004-synthetic.json");
const LS: &str = include_str!("../../../tests/fixtures/order_book/ls-t1101-synthetic.json");

const BROKERS: [(Broker, &str); 3] = [(Broker::Kis, KIS), (Broker::Kiwoom, KIWOOM), (Broker::Ls, LS)];

/// Native (price, quantity) key pairs for level `n` (1-based) of a side.
fn keys(broker: Broker, ask: bool, n: usize) -> (String, String) {
    match (broker, ask) {
        (Broker::Kis, true) => (format!("askp{n}"), format!("askp_rsqn{n}")),
        (Broker::Kis, false) => (format!("bidp{n}"), format!("bidp_rsqn{n}")),
        (Broker::Kiwoom, true) if n == 1 => ("sel_fpr_bid".into(), "sel_fpr_req".into()),
        (Broker::Kiwoom, false) if n == 1 => ("buy_fpr_bid".into(), "buy_fpr_req".into()),
        (Broker::Kiwoom, true) => (format!("sel_{n}th_pre_bid"), format!("sel_{n}th_pre_req")),
        (Broker::Kiwoom, false) => (format!("buy_{n}th_pre_bid"), format!("buy_{n}th_pre_req")),
        (Broker::Ls, true) => (format!("offerho{n}"), format!("offerrem{n}")),
        (Broker::Ls, false) => (format!("bidho{n}"), format!("bidrem{n}")),
        _ => unreachable!(),
    }
}

/// Native JSON value for a number, in the type that broker documents.
fn native(broker: Broker, value: u64) -> Value {
    if broker == Broker::Ls { json!(value) } else { json!(value.to_string()) }
}

fn row(broker: Broker, doc: &mut Value) -> &mut serde_json::Map<String, Value> {
    let target = match broker {
        Broker::Kis => &mut doc["output1"],
        Broker::Ls => &mut doc["t1101OutBlock"],
        _ => doc,
    };
    target.as_object_mut().unwrap()
}

fn edited(broker: Broker, fixture: &str, edit: impl FnOnce(&mut serde_json::Map<String, Value>)) -> String {
    let mut doc: Value = serde_json::from_str(fixture).unwrap();
    edit(row(broker, &mut doc));
    doc.to_string()
}

fn ok(broker: Broker, payload: &str, limit: Option<usize>) -> CoreOrderBook {
    decode(broker, "005930", Venue::Krx, payload, limit).unwrap()
}

fn err(broker: Broker, payload: &str) -> DecodeError {
    decode(broker, "005930", Venue::Krx, payload, None).unwrap_err()
}

fn side(levels: &[ktradelink_core::BookLevel]) -> Vec<(String, u64)> {
    levels.iter().map(|l| (l.price().as_str().to_owned(), l.quantity())).collect()
}

#[test]
fn publisher_shaped_fixtures_decode_all_ten_levels_per_side() {
    let asks: Vec<_> = (0..10).map(|i| ((70100 + 100 * i).to_string(), [9, 20, 0, 31, 42, 53, 64, 75, 86, 97][i as usize])).collect();
    let bids: Vec<_> = (0..10).map(|i| ((70000 - 100 * i).to_string(), [12, 0, 23, 34, 45, 56, 67, 78, 89, 90][i as usize])).collect();
    assert_eq!(ORDER_BOOK_DEPTH, 10);
    for (broker, fixture) in BROKERS {
        let book = ok(broker, fixture, None);
        let input = book.input();
        assert_eq!(input.broker, broker.as_str());
        assert_eq!((input.symbol.as_str(), input.venue), ("005930", Venue::Krx));
        assert_eq!(side(&input.asks), asks, "{broker:?}");
        assert_eq!(side(&input.bids), bids, "{broker:?}");
        // Zero quantity at a quoted price is preserved (asks[2], bids[1]).
        assert_eq!(input.asks[2].quantity(), 0);
        assert_eq!(input.bids[1].quantity(), 0);
        assert_eq!((input.timestamp, input.retrieved_at), (None, None));
        assert!(input.scope_description.is_none());
    }
}

#[test]
fn limit_is_a_per_side_cap_within_documented_depth() {
    for (broker, fixture) in BROKERS {
        let book = ok(broker, fixture, Some(3));
        assert_eq!((book.input().bids.len(), book.input().asks.len()), (3, 3));
        assert_eq!(book.input().bids[0].price().as_str(), "70000");
        assert_eq!(ok(broker, fixture, Some(10)).input().bids.len(), 10);
        let e = decode(broker, "005930", Venue::Krx, fixture, Some(0)).unwrap_err();
        assert_eq!((e.field, e.kind), ("limit", DecodeKind::InvalidLimit));
        let e = decode(broker, "005930", Venue::Krx, fixture, Some(11)).unwrap_err();
        assert_eq!((e.field, e.kind), ("limit", DecodeKind::DepthExceeded));
        // The cap is checked before JSON parsing.
        let e = decode(broker, "005930", Venue::Krx, "not json", Some(11)).unwrap_err();
        assert_eq!(e.kind, DecodeKind::DepthExceeded);
    }
}

#[test]
fn unordered_or_duplicate_levels_are_rejected_not_sorted() {
    for (broker, fixture) in BROKERS {
        for (ask, n, value, field) in [
            (false, 2, 70100, "bids"), // bid 2 above bid 1
            (false, 2, 70000, "bids"), // duplicate bid price
            (true, 2, 70000, "asks"),  // ask 2 below ask 1
            (true, 2, 70100, "asks"),  // duplicate ask price
        ] {
            let (price_key, _) = keys(broker, ask, n);
            let payload = edited(broker, fixture, |r| { r.insert(price_key, native(broker, value)); });
            let e = err(broker, &payload);
            assert_eq!((e.field, e.kind), (field, DecodeKind::CoreValidation), "{broker:?}");
        }
        // A violation deeper than `limit` is still detected.
        let (price_key, _) = keys(broker, false, 10);
        let payload = edited(broker, fixture, |r| { r.insert(price_key, native(broker, 99000)); });
        let e = decode(broker, "005930", Venue::Krx, &payload, Some(2)).unwrap_err();
        assert_eq!((e.field, e.kind), ("bids", DecodeKind::CoreValidation));
    }
}

#[test]
fn crossed_and_locked_books_are_preserved() {
    for (broker, fixture) in BROKERS {
        // Best bid 70100 equals best ask (locked); asks start at 70100.
        let (bid1, _) = keys(broker, false, 1);
        let locked = edited(broker, fixture, |r| { r.insert(bid1.clone(), native(broker, 70100)); });
        assert_eq!(ok(broker, &locked, None).input().bids[0].price().as_str(), "70100");
        // Best bid 70150 above best ask 70100 (crossed).
        let crossed = edited(broker, fixture, |r| { r.insert(bid1, native(broker, 70150)); });
        assert_eq!(ok(broker, &crossed, None).input().bids[0].price().as_str(), "70150");
    }
}

#[test]
fn zero_zero_tail_is_no_quote_but_never_synthesized_or_gapped() {
    for (broker, fixture) in BROKERS {
        // Ranks 8..10 empty on the bid side -> exactly 7 bids, asks intact.
        let payload = edited(broker, fixture, |r| {
            for n in 8..=10 {
                let (p, q) = keys(broker, false, n);
                r.insert(p, native(broker, 0));
                r.insert(q, native(broker, 0));
            }
        });
        let book = ok(broker, &payload, None);
        assert_eq!((book.input().bids.len(), book.input().asks.len()), (7, 10));
        // limit larger than what the source quoted returns only real levels.
        assert_eq!(ok(broker, &payload, Some(9)).input().bids.len(), 7);

        // Entire ask side empty -> empty asks, not an error.
        let empty = edited(broker, fixture, |r| {
            for n in 1..=10 {
                let (p, q) = keys(broker, true, n);
                r.insert(p, native(broker, 0));
                r.insert(q, native(broker, 0));
            }
        });
        assert!(ok(broker, &empty, None).input().asks.is_empty());

        // An empty rank followed by a quoted rank is a gap, not a book.
        let (p5, q5) = keys(broker, true, 5);
        let (p6, _) = keys(broker, true, 6);
        let gap = edited(broker, fixture, |r| {
            r.insert(p5, native(broker, 0));
            r.insert(q5, native(broker, 0));
        });
        let e = err(broker, &gap);
        assert_eq!(e.kind, DecodeKind::LevelGap);
        assert_eq!(e.field, p6);

        // Zero price with resting quantity is malformed.
        let (p1, _) = keys(broker, false, 1);
        let bad = edited(broker, fixture, |r| { r.insert(p1.clone(), native(broker, 0)); });
        let e = err(broker, &bad);
        assert_eq!((e.field, e.kind), (p1.as_str(), DecodeKind::InvalidPrice));
    }
}

#[test]
fn missing_or_null_level_fields_are_errors_not_empty_levels() {
    for (broker, fixture) in BROKERS {
        for (ask, n) in [(true, 1), (false, 10)] {
            let (p, q) = keys(broker, ask, n);
            for key in [p, q] {
                let missing = edited(broker, fixture, |r| { r.remove(&key); });
                let e = err(broker, &missing);
                assert_eq!((e.field, e.kind), (key.as_str(), DecodeKind::MissingRequired));
                let null = edited(broker, fixture, |r| { r.insert(key.clone(), Value::Null); });
                assert_eq!(err(broker, &null).kind, DecodeKind::MissingRequired);
            }
        }
    }
}

#[test]
fn level_values_accept_only_the_documented_unsigned_wire_type() {
    // KIS/Kiwoom: strings; LS: JSON integers. Signs are never stripped.
    let text_bad_prices = [json!("+70100"), json!("-70100"), json!(""), json!(" 70100"),
        json!("7e4"), json!("70100 "), json!(70100), json!(true), json!({})];
    let int_bad_prices = [json!("70100"), json!(-70100), json!(70100.5), json!(true), json!([])];
    let text_bad_qty = [json!("-1"), json!("+1"), json!("1.5"), json!(""), json!(" 1"),
        json!("18446744073709551616"), json!(1)];
    let int_bad_qty = [json!("1"), json!(-1), json!(1.5), json!(18446744073709551616.0_f64)];
    for (broker, fixture) in BROKERS {
        let (prices, qtys) = if broker == Broker::Ls {
            (&int_bad_prices[..], &int_bad_qty[..])
        } else {
            (&text_bad_prices[..], &text_bad_qty[..])
        };
        let (p, q) = keys(broker, true, 1);
        for value in prices {
            let payload = edited(broker, fixture, |r| { r.insert(p.clone(), value.clone()); });
            let e = err(broker, &payload);
            assert_eq!((e.field, e.kind), (p.as_str(), DecodeKind::InvalidPrice), "{broker:?} {value}");
        }
        for value in qtys {
            let payload = edited(broker, fixture, |r| { r.insert(q.clone(), value.clone()); });
            let e = err(broker, &payload);
            assert_eq!((e.field, e.kind), (q.as_str(), DecodeKind::InvalidField), "{broker:?} {value}");
        }
    }
    // Lossless decimal text and leading zeroes survive for text brokers.
    let payload = edited(Broker::Kiwoom, KIWOOM, |r| { r.insert("sel_fpr_bid".into(), json!("0070050.50")); });
    assert_eq!(ok(Broker::Kiwoom, &payload, None).input().asks[0].price().as_str(), "0070050.50");
}

#[test]
fn status_fields_are_required_with_native_type_and_value() {
    type Variants = Vec<(Option<Value>, DecodeKind)>;
    let cases: [(Broker, &str, &str, Variants); 3] = [
        (Broker::Kis, KIS, "rt_cd", vec![
            (None, DecodeKind::MissingRequired), (Some(Value::Null), DecodeKind::MissingRequired),
            (Some(json!(0)), DecodeKind::SourceStatus), (Some(json!("1")), DecodeKind::SourceStatus),
            (Some(json!("00")), DecodeKind::SourceStatus),
        ]),
        (Broker::Kiwoom, KIWOOM, "return_code", vec![
            (None, DecodeKind::MissingRequired), (Some(Value::Null), DecodeKind::MissingRequired),
            (Some(json!("0")), DecodeKind::SourceStatus), (Some(json!(-1)), DecodeKind::SourceStatus),
            (Some(json!(0.0)), DecodeKind::SourceStatus), (Some(json!(false)), DecodeKind::SourceStatus),
        ]),
        (Broker::Ls, LS, "rsp_cd", vec![
            (None, DecodeKind::MissingRequired), (Some(Value::Null), DecodeKind::MissingRequired),
            (Some(json!(0)), DecodeKind::SourceStatus), (Some(json!("00001")), DecodeKind::SourceStatus),
        ]),
    ];
    for (broker, fixture, key, variants) in cases {
        for (value, kind) in variants {
            let mut doc: Value = serde_json::from_str(fixture).unwrap();
            let root = doc.as_object_mut().unwrap();
            match &value {
                None => { root.remove(key); }
                Some(v) => { root.insert(key.into(), v.clone()); }
            }
            let e = err(broker, &doc.to_string());
            assert_eq!((e.field, e.kind), (key, kind), "{broker:?} {value:?}");
        }
    }
    // Status values are never echoed.
    let doc = KIS.replace(r#""rt_cd": "0""#, r#""rt_cd": "secret-response""#);
    assert!(!err(Broker::Kis, &doc).to_string().contains("secret-response"));
}

#[test]
fn envelopes_and_ls_symbol_echo_are_strict() {
    let kis_missing = KIS.replace(r#""output1""#, r#""output9""#);
    assert_eq!(err(Broker::Kis, &kis_missing).field, "output1");
    let kis_array = r#"{"rt_cd":"0","output1":[]}"#;
    assert_eq!(err(Broker::Kis, kis_array).kind, DecodeKind::InvalidEnvelope);
    // The ticker output block is not the book block.
    assert_eq!(err(Broker::Kis, r#"{"rt_cd":"0","output":{}}"#).kind, DecodeKind::MissingRequired);
    let ls_t1102 = LS.replace("t1101OutBlock", "t1102OutBlock");
    assert_eq!(err(Broker::Ls, &ls_t1102).field, "t1101OutBlock");
    for (value, kind) in [
        (None, DecodeKind::MissingRequired),
        (Some(json!(5930)), DecodeKind::InvalidField),
        (Some(json!("000660")), DecodeKind::AmbiguousSymbol),
    ] {
        let payload = edited(Broker::Ls, LS, |r| match value {
            None => { r.remove("shcode"); }
            Some(v) => { r.insert("shcode".into(), v); }
        });
        let e = err(Broker::Ls, &payload);
        assert_eq!((e.field, e.kind), ("shcode", kind));
    }
    for payload in ["[]", "null", "\"x\"", "1"] {
        assert_eq!(err(Broker::Kiwoom, payload).kind, DecodeKind::InvalidEnvelope);
    }
}

#[test]
fn invalid_json_duplicate_keys_and_oversize_are_rejected() {
    for (broker, fixture) in BROKERS {
        assert_eq!(err(broker, "{").kind, DecodeKind::InvalidJson);
        assert_eq!(err(broker, r#"{"a": NaN}"#).kind, DecodeKind::InvalidJson);
        // Duplicate key at the root and inside the level block.
        let (p, _) = keys(broker, false, 1);
        let dup_root = fixture.replacen('{', r#"{"_note": "dup","#, 1);
        assert_eq!(err(broker, &dup_root).kind, DecodeKind::InvalidJson);
        let needle = format!(r#""{p}":"#);
        let dup_level = fixture.replacen(&needle, &format!("{needle} \"1\", {needle}"), 1);
        assert_ne!(dup_level, fixture);
        assert_eq!(err(broker, &dup_level).kind, DecodeKind::InvalidJson);

        let exact = format!("{fixture}{}", " ".repeat(1_048_576 - fixture.len()));
        assert_eq!(ok(broker, &exact, None).input().bids.len(), 10);
        let e = err(broker, &format!("{exact} "));
        assert_eq!((e.field, e.kind), ("payload", DecodeKind::OversizedInput));
    }
}

#[test]
fn caller_context_is_checked_before_parsing() {
    for (broker, fixture) in BROKERS {
        for venue in [Venue::Nxt, Venue::BrokerComposite] {
            let e = decode(broker, "005930", venue, fixture, None).unwrap_err();
            assert_eq!((e.field, e.kind), ("venue", DecodeKind::UnsupportedVenue));
        }
        for bad in ["", "005 930", "종목", "005930\n", "\u{200b}005930"] {
            let e = decode(broker, bad, Venue::Krx, "not-json", None).unwrap_err();
            assert_eq!(e.to_string(), "symbol: CoreValidation");
        }
    }
    for broker in [Broker::Db, Broker::Toss, Broker::Meritz] {
        let e = decode(broker, "005930", Venue::Krx, "{}", None).unwrap_err();
        assert_eq!((e.field, e.kind), ("broker", DecodeKind::UnsupportedBroker));
    }
}

#[test]
fn unmapped_fields_never_enter_the_book_or_errors() {
    for (broker, fixture) in BROKERS {
        let payload = edited(broker, fixture, |r| {
            r.insert("access_token".into(), json!("not-for-model"));
            r.insert("account".into(), json!("not-for-model"));
        });
        let book = ok(broker, &payload, None);
        assert_eq!(book.input().bids.len(), 10);
        let (p, _) = keys(broker, true, 1);
        let bad = edited(broker, fixture, |r| { r.insert(p, json!("secret-value")); });
        assert!(!err(broker, &bad).to_string().contains("secret-value"));
    }
}
