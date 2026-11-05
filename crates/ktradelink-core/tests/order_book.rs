//! Synthetic book values only; mirrors ktradelink.models.OrderBook invariants.

use ktradelink_core::{BookLevel, CoreOrderBook, ErrorKind, OrderBookInput, Price, Venue};
use std::cmp::Ordering;

fn level(price: &str, quantity: u64) -> BookLevel {
    BookLevel::new(Price::parse(price, "price").unwrap(), quantity, "price").unwrap()
}

fn book(bids: Vec<BookLevel>, asks: Vec<BookLevel>) -> OrderBookInput {
    OrderBookInput {
        symbol: "005930".into(), venue: Venue::Krx, broker: "synthetic".into(),
        bids, asks, timestamp: None, retrieved_at: None, scope_description: None,
    }
}

#[test]
fn numeric_comparison_is_exact_and_ignores_padding() {
    let cmp = |a: &str, b: &str| {
        Price::parse(a, "a").unwrap().numeric_cmp(&Price::parse(b, "b").unwrap())
    };
    assert_eq!(cmp("70500", "070500.00"), Ordering::Equal);
    assert_eq!(cmp("70500", "70499.999"), Ordering::Greater);
    assert_eq!(cmp("9", "10"), Ordering::Less);
    assert_eq!(cmp("0.5", "0.45"), Ordering::Greater);
    assert_eq!(cmp("0.4", "0.45"), Ordering::Less);
    assert_eq!(cmp("9007199254740993", "9007199254740992.9"), Ordering::Greater);
    assert_eq!(cmp("0", "0.000"), Ordering::Equal);
    for zero in ["0", "000", "0.00"] {
        assert!(Price::parse(zero, "p").unwrap().is_zero());
    }
    assert!(!Price::parse("0.01", "p").unwrap().is_zero());
}

#[test]
fn zero_price_is_never_a_level_but_zero_quantity_is() {
    let err = BookLevel::new(Price::parse("0.00", "bidp3").unwrap(), 0, "bidp3").unwrap_err();
    assert_eq!((err.field, err.kind), ("bidp3", ErrorKind::InvalidLevel));
    let kept = level("70000", 0);
    assert_eq!(kept.quantity(), 0);
    assert_eq!(kept.price().as_str(), "70000");
    assert_eq!(level("1", u64::MAX).quantity(), u64::MAX);
}

#[test]
fn sides_are_strictly_best_to_worst_without_sorting() {
    let ok = CoreOrderBook::new(book(
        vec![level("70000", 12), level("69900", 0)],
        vec![level("70100", 9), level("70200", 20)],
    ))
    .unwrap();
    let prices: Vec<_> = ok.input().bids.iter().map(|l| l.price().as_str()).collect();
    assert_eq!(prices, ["70000", "69900"]);

    for (bids, asks, field) in [
        (vec![level("69900", 1), level("70000", 1)], vec![], "bids"),
        (vec![level("70000", 1), level("70000.0", 1)], vec![], "bids"),
        (vec![], vec![level("70200", 1), level("70100", 1)], "asks"),
        (vec![], vec![level("70100", 1), level("070100", 1)], "asks"),
    ] {
        let err = CoreOrderBook::new(book(bids, asks)).unwrap_err();
        assert_eq!((err.field, err.kind), (field, ErrorKind::UnorderedLevels));
    }
}

#[test]
fn empty_one_sided_crossed_and_locked_books_are_representable() {
    assert!(CoreOrderBook::new(book(vec![], vec![])).is_ok());
    assert!(CoreOrderBook::new(book(vec![level("1", 1)], vec![])).is_ok());
    // Crossed (best bid > best ask) and locked (equal) are preserved, not fixed.
    assert!(CoreOrderBook::new(book(vec![level("70200", 1)], vec![level("70100", 1)])).is_ok());
    assert!(CoreOrderBook::new(book(vec![level("70100", 1)], vec![level("70100", 1)])).is_ok());
}

#[test]
fn provenance_rules_match_ticker() {
    let mut input = book(vec![], vec![]);
    input.symbol = "005 930".into();
    assert_eq!(CoreOrderBook::new(input).unwrap_err().kind, ErrorKind::InvalidIdentifier);
    let mut input = book(vec![], vec![]);
    input.broker = String::new();
    assert_eq!(CoreOrderBook::new(input).unwrap_err().field, "broker");
    let mut input = book(vec![], vec![]);
    input.venue = Venue::BrokerComposite;
    assert_eq!(CoreOrderBook::new(input.clone()).unwrap_err().kind, ErrorKind::InvalidScope);
    input.scope_description = Some("synthetic scope".into());
    assert!(CoreOrderBook::new(input).is_ok());
}

#[test]
fn errors_do_not_echo_values() {
    let input = book(vec![level("12345", 1), level("23456", 1)], vec![]);
    assert_eq!(CoreOrderBook::new(input).unwrap_err().to_string(), "bids: UnorderedLevels");
}
