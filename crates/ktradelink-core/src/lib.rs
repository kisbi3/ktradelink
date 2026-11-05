//! Python-independent foundation. No broker decoder, networking or price arithmetic.
#![forbid(unsafe_code)]

use std::cmp::Ordering;
use std::fmt;

mod order_book;
pub use order_book::{BookLevel, CoreOrderBook, OrderBookInput};

pub const CORE_VERSION: &str = env!("CARGO_PKG_VERSION");
pub const CONTRACT_VERSION: u32 = 1;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ErrorKind {
    InvalidIdentifier,
    InvalidVenue,
    InvalidPrice,
    InvalidScope,
    /// A book level whose price is zero; a placeholder is never a level.
    InvalidLevel,
    /// Same-side book levels not strictly ordered best-to-worst.
    UnorderedLevels,
}

/// Contains field names and error kinds only, never input values or secrets.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CoreError {
    pub field: &'static str,
    pub kind: ErrorKind,
}

impl fmt::Display for CoreError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}: {:?}", self.field, self.kind)
    }
}

impl std::error::Error for CoreError {}

/// Lossless unsigned fixed-decimal TEXT, not a floating-point/arithmetic type.
/// Leading and trailing zeroes are retained; no numeric equality is promised here.
#[derive(Debug, Clone)]
pub struct Price(String);

impl Price {
    pub fn parse(text: &str, field: &'static str) -> Result<Self, CoreError> {
        let mut parts = text.split('.');
        let whole = parts.next().unwrap_or_default();
        let fraction = parts.next();
        let digits = |s: &str| !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit());
        if !digits(whole) || fraction.is_some_and(|p| !digits(p)) || parts.next().is_some() {
            return Err(CoreError { field, kind: ErrorKind::InvalidPrice });
        }
        Ok(Self(text.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }

    /// True when every digit is zero (e.g. `0`, `000`, `0.00`).
    pub fn is_zero(&self) -> bool {
        self.0.bytes().all(|b| b == b'0' || b == b'.')
    }

    /// Exact numeric ordering of two validated decimal texts, without any
    /// float conversion. Leading/trailing zeroes do not affect the result,
    /// so `70500` and `070500.00` compare Equal while their text differs.
    pub fn numeric_cmp(&self, other: &Self) -> Ordering {
        fn split(text: &str) -> (&str, &str) {
            let (whole, fraction) = text.split_once('.').unwrap_or((text, ""));
            (whole.trim_start_matches('0'), fraction.trim_end_matches('0'))
        }
        let (left_whole, left_fraction) = split(&self.0);
        let (right_whole, right_fraction) = split(&other.0);
        left_whole
            .len()
            .cmp(&right_whole.len())
            .then_with(|| left_whole.cmp(right_whole))
            .then_with(|| left_fraction.cmp(right_fraction))
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Venue {
    Krx,
    Nxt,
    BrokerComposite,
}

impl Venue {
    pub fn parse(value: &str) -> Result<Self, CoreError> {
        match value {
            "KRX" => Ok(Self::Krx),
            "NXT" => Ok(Self::Nxt),
            "BROKER_COMPOSITE" => Ok(Self::BrokerComposite),
            _ => Err(CoreError { field: "venue", kind: ErrorKind::InvalidVenue }),
        }
    }

    pub fn as_str(self) -> &'static str {
        match self {
            Self::Krx => "KRX",
            Self::Nxt => "NXT",
            Self::BrokerComposite => "BROKER_COMPOSITE",
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct Prices {
    pub last: Option<Price>,
    pub open: Option<Price>,
    pub high: Option<Price>,
    pub low: Option<Price>,
    pub previous_close: Option<Price>,
    pub bid: Option<Price>,
    pub ask: Option<Price>,
}

/// Internal normalized values. Units: prices in KRW, quantities in shares,
/// timestamps in UTC epoch milliseconds. No raw upstream info is carried.
#[derive(Debug, Clone)]
pub struct TickerInput {
    pub symbol: String,
    pub venue: Venue,
    pub broker: String,
    pub prices: Prices,
    pub volume: Option<u64>,
    pub timestamp: Option<u64>,
    pub retrieved_at: Option<u64>,
    pub scope_description: Option<String>,
}

#[derive(Debug, Clone)]
pub struct CoreTicker(TickerInput);

/// Shared symbol/broker/venue/scope rules for every normalized value.
fn validate_provenance(
    symbol: &str,
    broker: &str,
    venue: Venue,
    scope_description: Option<&str>,
) -> Result<(), CoreError> {
    for (field, value) in [("symbol", symbol), ("broker", broker)] {
        if value.is_empty() || !value.bytes().all(|b| b.is_ascii_graphic()) {
            return Err(CoreError { field, kind: ErrorKind::InvalidIdentifier });
        }
    }
    if venue == Venue::BrokerComposite && scope_description.is_none() {
        return Err(CoreError { field: "scope_description", kind: ErrorKind::InvalidScope });
    }
    if let Some(scope) = scope_description {
        if scope.is_empty() || scope.trim() != scope || scope.chars().any(char::is_control) {
            return Err(CoreError { field: "scope_description", kind: ErrorKind::InvalidScope });
        }
    }
    Ok(())
}

impl CoreTicker {
    pub fn new(input: TickerInput) -> Result<Self, CoreError> {
        validate_provenance(
            &input.symbol,
            &input.broker,
            input.venue,
            input.scope_description.as_deref(),
        )?;
        Ok(Self(input))
    }

    pub fn input(&self) -> &TickerInput {
        &self.0
    }
}
