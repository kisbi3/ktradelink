//! Normalized equity book snapshot. Mirrors `ktradelink.models.OrderBook`:
//! bids strictly descending, asks strictly ascending, positive prices,
//! integral share quantities (zero kept), no sorting/merging/clamping.

use std::cmp::Ordering;

use crate::{validate_provenance, CoreError, ErrorKind, Price, Venue};

/// One quoted price (strictly positive decimal text) and share quantity.
/// A quantity of zero is a real value; a zero PRICE is never a level.
#[derive(Debug, Clone)]
pub struct BookLevel {
    price: Price,
    quantity: u64,
}

impl BookLevel {
    /// `field` names the native price field for errors; no value is echoed.
    pub fn new(price: Price, quantity: u64, field: &'static str) -> Result<Self, CoreError> {
        if price.is_zero() {
            return Err(CoreError { field, kind: ErrorKind::InvalidLevel });
        }
        Ok(Self { price, quantity })
    }

    pub fn price(&self) -> &Price {
        &self.price
    }

    pub fn quantity(&self) -> u64 {
        self.quantity
    }
}

/// Internal normalized values. Units: prices in KRW, quantities in shares,
/// timestamps in UTC epoch milliseconds. No raw upstream info is carried.
#[derive(Debug, Clone)]
pub struct OrderBookInput {
    pub symbol: String,
    pub venue: Venue,
    pub broker: String,
    pub bids: Vec<BookLevel>,
    pub asks: Vec<BookLevel>,
    pub timestamp: Option<u64>,
    pub retrieved_at: Option<u64>,
    pub scope_description: Option<String>,
}

#[derive(Debug, Clone)]
pub struct CoreOrderBook(OrderBookInput);

/// Strict best-to-worst order on one side; equal prices are duplicates.
fn validate_side(
    field: &'static str,
    levels: &[BookLevel],
    best_first: Ordering,
) -> Result<(), CoreError> {
    for pair in levels.windows(2) {
        if pair[0].price.numeric_cmp(&pair[1].price) != best_first {
            return Err(CoreError { field, kind: ErrorKind::UnorderedLevels });
        }
    }
    Ok(())
}

impl CoreOrderBook {
    /// Empty/one-sided and crossed/locked books are representable: this value
    /// layer cannot infer auction state or source synchronization.
    pub fn new(input: OrderBookInput) -> Result<Self, CoreError> {
        validate_provenance(
            &input.symbol,
            &input.broker,
            input.venue,
            input.scope_description.as_deref(),
        )?;
        validate_side("bids", &input.bids, Ordering::Greater)?;
        validate_side("asks", &input.asks, Ordering::Less)?;
        Ok(Self(input))
    }

    pub fn input(&self) -> &OrderBookInput {
        &self.0
    }
}
