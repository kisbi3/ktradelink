//! Accountless, evidence-limited OFFLINE order-book (호가) decoder candidates
//! for KIS (FHKST01010200), Kiwoom REST (ka10004) and LS (t1101) only.
//! Evidence: docs/brokers/order-book-evidence-2026-11-05.md. No HTTP, auth,
//! venue inference, timestamps, sorting, clamping or raw info forwarding.

use ktradelink_core::{BookLevel, CoreOrderBook, OrderBookInput, Price, Venue};
use serde_json::{Map, Value};

use super::{
    child_object, error, object, required_identifier, required_status, Broker, DecodeError,
    DecodeKind, StrictJson, MAX_JSON_BYTES,
};

/// Documented depth per side in every supported publisher source.
pub const ORDER_BOOK_DEPTH: usize = 10;

/// Native JSON value type of the level fields, as each publisher documents it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Wire {
    /// JSON string of unsigned ASCII digits (price may carry one '.').
    Text,
    /// Unsigned JSON integer.
    Integer,
}

type Side = [(&'static str, &'static str); ORDER_BOOK_DEPTH];

struct Layout {
    asks: Side,
    bids: Side,
    wire: Wire,
}

// KIS FHKST01010200 output1: askp{n}/askp_rsqn{n}, bidp{n}/bidp_rsqn{n}.
const KIS: Layout = Layout {
    asks: [
        ("askp1", "askp_rsqn1"), ("askp2", "askp_rsqn2"), ("askp3", "askp_rsqn3"),
        ("askp4", "askp_rsqn4"), ("askp5", "askp_rsqn5"), ("askp6", "askp_rsqn6"),
        ("askp7", "askp_rsqn7"), ("askp8", "askp_rsqn8"), ("askp9", "askp_rsqn9"),
        ("askp10", "askp_rsqn10"),
    ],
    bids: [
        ("bidp1", "bidp_rsqn1"), ("bidp2", "bidp_rsqn2"), ("bidp3", "bidp_rsqn3"),
        ("bidp4", "bidp_rsqn4"), ("bidp5", "bidp_rsqn5"), ("bidp6", "bidp_rsqn6"),
        ("bidp7", "bidp_rsqn7"), ("bidp8", "bidp_rsqn8"), ("bidp9", "bidp_rsqn9"),
        ("bidp10", "bidp_rsqn10"),
    ],
    wire: Wire::Text,
};

// Kiwoom ka10004 root: level 1 is the `fpr` (최우선) pair; levels 2..10 use
// the publisher's literal `{n}th_pre` spelling (including "2th"/"3th").
const KIWOOM: Layout = Layout {
    asks: [
        ("sel_fpr_bid", "sel_fpr_req"), ("sel_2th_pre_bid", "sel_2th_pre_req"),
        ("sel_3th_pre_bid", "sel_3th_pre_req"), ("sel_4th_pre_bid", "sel_4th_pre_req"),
        ("sel_5th_pre_bid", "sel_5th_pre_req"), ("sel_6th_pre_bid", "sel_6th_pre_req"),
        ("sel_7th_pre_bid", "sel_7th_pre_req"), ("sel_8th_pre_bid", "sel_8th_pre_req"),
        ("sel_9th_pre_bid", "sel_9th_pre_req"), ("sel_10th_pre_bid", "sel_10th_pre_req"),
    ],
    bids: [
        ("buy_fpr_bid", "buy_fpr_req"), ("buy_2th_pre_bid", "buy_2th_pre_req"),
        ("buy_3th_pre_bid", "buy_3th_pre_req"), ("buy_4th_pre_bid", "buy_4th_pre_req"),
        ("buy_5th_pre_bid", "buy_5th_pre_req"), ("buy_6th_pre_bid", "buy_6th_pre_req"),
        ("buy_7th_pre_bid", "buy_7th_pre_req"), ("buy_8th_pre_bid", "buy_8th_pre_req"),
        ("buy_9th_pre_bid", "buy_9th_pre_req"), ("buy_10th_pre_bid", "buy_10th_pre_req"),
    ],
    wire: Wire::Text,
};

// LS t1101 t1101OutBlock: offerho{n}/offerrem{n}, bidho{n}/bidrem{n}.
const LS: Layout = Layout {
    asks: [
        ("offerho1", "offerrem1"), ("offerho2", "offerrem2"), ("offerho3", "offerrem3"),
        ("offerho4", "offerrem4"), ("offerho5", "offerrem5"), ("offerho6", "offerrem6"),
        ("offerho7", "offerrem7"), ("offerho8", "offerrem8"), ("offerho9", "offerrem9"),
        ("offerho10", "offerrem10"),
    ],
    bids: [
        ("bidho1", "bidrem1"), ("bidho2", "bidrem2"), ("bidho3", "bidrem3"),
        ("bidho4", "bidrem4"), ("bidho5", "bidrem5"), ("bidho6", "bidrem6"),
        ("bidho7", "bidrem7"), ("bidho8", "bidrem8"), ("bidho9", "bidrem9"),
        ("bidho10", "bidrem10"),
    ],
    wire: Wire::Integer,
};

/// Unsigned decimal text only. A sign ('+'/'-'), blank, space, exponent or
/// float is rejected: Kiwoom documents its prices as "부호가 포함된 숫자"
/// without stating what the sign means, so it is never stripped (no abs()).
type Row = Map<String, Value>;

fn level_price(row: &Row, key: &'static str, wire: Wire) -> Result<Price, DecodeError> {
    let text = match (row.get(key), wire) {
        (None | Some(Value::Null), _) => return Err(error(key, DecodeKind::MissingRequired)),
        (Some(Value::String(raw)), Wire::Text) => raw.clone(),
        (Some(Value::Number(n)), Wire::Integer) if n.is_u64() => n.to_string(),
        _ => return Err(error(key, DecodeKind::InvalidPrice)),
    };
    Price::parse(&text, key).map_err(|_| error(key, DecodeKind::InvalidPrice))
}

/// Integral share quantity; documented as unsigned ("단위: 1주" / Number).
fn level_quantity(row: &Row, key: &'static str, wire: Wire) -> Result<u64, DecodeError> {
    match (row.get(key), wire) {
        (None | Some(Value::Null), _) => Err(error(key, DecodeKind::MissingRequired)),
        (Some(Value::String(raw)), Wire::Text)
            if !raw.is_empty() && raw.bytes().all(|b| b.is_ascii_digit()) =>
        {
            raw.parse::<u64>().map_err(|_| error(key, DecodeKind::InvalidField))
        }
        (Some(Value::Number(n)), Wire::Integer) => {
            n.as_u64().ok_or_else(|| error(key, DecodeKind::InvalidField))
        }
        _ => Err(error(key, DecodeKind::InvalidField)),
    }
}

/// Reads all documented levels of one side, best first.
///
/// No publisher documents how an empty rank is encoded, so a zero price is
/// never interpreted (ADR 0003: placeholders are resolved with evidence, not
/// silently dropped). Zero price with zero quantity is `UnverifiedEmptyLevel`;
/// zero price with a nonzero quantity is `InvalidPrice`. Missing, null, blank
/// or wrongly typed fields always fail. A positive price with zero quantity is
/// a real level and is kept.
fn side(row: &Row, layout: &Side, wire: Wire) -> Result<Vec<BookLevel>, DecodeError> {
    let mut levels = Vec::with_capacity(ORDER_BOOK_DEPTH);
    for &(price_key, quantity_key) in layout {
        let price = level_price(row, price_key, wire)?;
        let quantity = level_quantity(row, quantity_key, wire)?;
        if price.is_zero() {
            let kind = if quantity == 0 {
                DecodeKind::UnverifiedEmptyLevel
            } else {
                DecodeKind::InvalidPrice
            };
            return Err(error(price_key, kind));
        }
        levels.push(BookLevel::new(price, quantity, price_key)?);
    }
    Ok(levels)
}

/// The pinned Kiwoom example treats an integer `return_code` of 0 (or its
/// absence) as success. Here it is REQUIRED (fail-closed library policy).
fn required_integer_zero(record: &Row, key: &'static str) -> Result<(), DecodeError> {
    match record.get(key) {
        None | Some(Value::Null) => Err(error(key, DecodeKind::MissingRequired)),
        Some(Value::Number(n)) if n.as_u64() == Some(0) => Ok(()),
        Some(_) => Err(error(key, DecodeKind::SourceStatus)),
    }
}

/// Offline order-book candidate for caller-asserted KRX context only.
///
/// `limit` caps the levels returned on EACH side after the full documented
/// depth has been validated. `None` returns every non-empty documented level.
/// `Some(0)` is `InvalidLimit`; more than the documented depth is
/// `DepthExceeded` (never silently clamped). Every documented level must be a
/// real quote, so each side always has exactly the documented depth.
pub fn decode_order_book_candidate(
    broker: Broker,
    symbol: &str,
    venue: Venue,
    payload: &str,
    limit: Option<usize>,
) -> Result<CoreOrderBook, DecodeError> {
    let layout = match broker {
        Broker::Kis => &KIS,
        Broker::Kiwoom => &KIWOOM,
        Broker::Ls => &LS,
        Broker::Db | Broker::Toss | Broker::Meritz => {
            return Err(error("broker", DecodeKind::UnsupportedBroker));
        }
    };
    if venue != Venue::Krx {
        return Err(error("venue", DecodeKind::UnsupportedVenue));
    }
    if symbol.is_empty() || !symbol.bytes().all(|b| b.is_ascii_graphic()) {
        return Err(error("symbol", DecodeKind::CoreValidation));
    }
    let depth = match limit {
        None => ORDER_BOOK_DEPTH,
        Some(0) => return Err(error("limit", DecodeKind::InvalidLimit)),
        Some(n) if n > ORDER_BOOK_DEPTH => return Err(error("limit", DecodeKind::DepthExceeded)),
        Some(n) => n,
    };
    if payload.len() > MAX_JSON_BYTES {
        return Err(error("payload", DecodeKind::OversizedInput));
    }
    let StrictJson(raw) = serde_json::from_str::<StrictJson>(payload)
        .map_err(|_| error("payload", DecodeKind::InvalidJson))?;
    let root = object(&raw, "payload")?;

    let row = match broker {
        Broker::Kis => {
            // kis_auth.py isOK(): rt_cd == "0" (string). output1 = 호가정보.
            required_status(root, "rt_cd", "0")?;
            child_object(root, "output1")?
        }
        Broker::Kiwoom => {
            // ka10004 response has no echoed stk_cd: symbol cannot be bound.
            required_integer_zero(root, "return_code")?;
            root
        }
        _ => {
            required_status(root, "rsp_cd", "00000")?;
            let row = child_object(root, "t1101OutBlock")?;
            required_identifier(row, "shcode", symbol)?;
            row
        }
    };
    let asks = side(row, &layout.asks, layout.wire)?;
    let bids = side(row, &layout.bids, layout.wire)?;

    let full = OrderBookInput {
        symbol: symbol.to_owned(),
        venue,
        broker: broker.as_str().to_owned(),
        bids,
        asks,
        // aspr_acpt_hour / bid_req_base_tm / hotime are time-only or
        // contradictory; none documents an absolute instant or timezone.
        timestamp: None,
        retrieved_at: None,
        scope_description: None,
    };
    // Validate ordering over the WHOLE documented book before applying the
    // output cap, so a violation deeper than `limit` is never hidden.
    let mut capped = CoreOrderBook::new(full)?.input().clone();
    capped.bids.truncate(depth);
    capped.asks.truncate(depth);
    CoreOrderBook::new(capped).map_err(Into::into)
}
