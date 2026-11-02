use ktradelink_core::{CoreTicker, ErrorKind, Price, Prices, TickerInput, Venue};

fn quote() -> TickerInput {
    TickerInput {
        symbol: "005930".into(), venue: Venue::Krx, broker: "synthetic".into(),
        prices: Prices { last: Some(Price::parse("70500.00", "last").unwrap()), ..Prices::default() },
        volume: None, timestamp: None, retrieved_at: None, scope_description: None,
    }
}

#[test]
fn price_text_is_lossless_without_binary_floats() {
    for value in ["0", "0.00", "00070.5000", "9007199254740993.12345678901234567890123456789"] {
        assert_eq!(Price::parse(value, "last").unwrap().as_str(), value);
    }
}

#[test]
fn invalid_prices_are_rejected_not_coerced() {
    for value in ["", "-0", "-1", "+1", "NaN", "Infinity", "1e3", "1.", ".1", "1.2.3", " 1", "1\n", "１"] {
        let error = Price::parse(value, "last").unwrap_err();
        assert_eq!(error.kind, ErrorKind::InvalidPrice);
        assert_eq!(error.field, "last");
    }
}

#[test]
fn errors_do_not_echo_input() {
    let error = Price::parse("secret-test-value", "last").unwrap_err();
    assert!(!error.to_string().contains("secret-test-value"));
    assert_eq!(error.to_string(), "last: InvalidPrice");
}

#[test]
fn missing_and_zero_are_different_values() {
    let absent = CoreTicker::new(quote()).unwrap();
    assert_eq!(absent.input().volume, None);
    let mut input = quote();
    input.prices.last = None;
    input.volume = Some(0);
    input.timestamp = Some(0);
    let zero = CoreTicker::new(input).unwrap();
    assert!(zero.input().prices.last.is_none());
    assert_eq!(zero.input().volume, Some(0));
    assert_eq!(zero.input().timestamp, Some(0));
}

#[test]
fn identifiers_are_not_numeric_only() {
    let mut input = quote();
    input.symbol = "0101N0".into();
    assert!(CoreTicker::new(input).is_ok());
    for bad in ["", "005 930", "005930\n", "\u{200b}005930", "종목"] {
        let mut input = quote();
        input.symbol = bad.into();
        assert_eq!(CoreTicker::new(input).unwrap_err().kind, ErrorKind::InvalidIdentifier);
    }
}

#[test]
fn broker_identifier_uses_same_boundary_rule() {
    let mut input = quote();
    input.broker = "kis\0".into();
    assert_eq!(CoreTicker::new(input).unwrap_err().field, "broker");
}

#[test]
fn venue_is_explicit_not_a_support_declaration() {
    for name in ["KRX", "NXT", "BROKER_COMPOSITE"] {
        assert_eq!(Venue::parse(name).unwrap().as_str(), name);
    }
    assert!(Venue::parse("krx").is_err());
    assert!(Venue::parse("unknown").is_err());
}

#[test]
fn composite_scope_is_mandatory_and_no_hidden_fallback() {
    let mut input = quote();
    input.venue = Venue::BrokerComposite;
    assert!(CoreTicker::new(input.clone()).is_err());
    for bad in ["", " ", "scope\nvalue", " scope"] {
        input.scope_description = Some(bad.into());
        assert!(CoreTicker::new(input.clone()).is_err());
    }
    input.scope_description = Some("synthetic scope".into());
    assert_eq!(CoreTicker::new(input).unwrap().input().venue, Venue::BrokerComposite);
}

#[test]
fn integer_boundary_is_u64_not_float() {
    let mut input = quote();
    input.volume = Some(u64::MAX);
    assert_eq!(CoreTicker::new(input).unwrap().input().volume, Some(u64::MAX));
}
