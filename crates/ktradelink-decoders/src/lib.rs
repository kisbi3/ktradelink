//! Accountless, evidence-limited, SIX-broker offline ticker decoder candidates.
//! No HTTP, auth, orders, venue inference, timestamps or raw info forwarding.
#![forbid(unsafe_code)]

use ktradelink_core::{CoreError, CoreTicker, Price, Prices, TickerInput, Venue};
use serde::de::{self, MapAccess, SeqAccess, Visitor};
use serde::{Deserialize, Deserializer};
use serde_json::{Map, Value};
use std::fmt;

const MAX_JSON_BYTES: usize = 1_048_576;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DecodeKind {
    UnknownBroker,
    UnsupportedVenue,
    InvalidJson,
    InvalidEnvelope,
    MissingRequired,
    InvalidField,
    InvalidPrice,
    SourceStatus,
    AmbiguousSymbol,
    OversizedInput,
    CoreValidation,
}

/// Errors never include raw input, token fields, account numbers or JSON excerpts.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DecodeError {
    pub field: &'static str,
    pub kind: DecodeKind,
}

impl fmt::Display for DecodeError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}: {:?}", self.field, self.kind)
    }
}
impl std::error::Error for DecodeError {}

impl From<CoreError> for DecodeError {
    fn from(error: CoreError) -> Self {
        Self { field: error.field, kind: DecodeKind::CoreValidation }
    }
}

fn error(field: &'static str, kind: DecodeKind) -> DecodeError {
    DecodeError { field, kind }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Broker {
    Kis,
    Kiwoom,
    Ls,
    Db,
    Toss,
    Meritz,
}

impl Broker {
    pub const ALL: [Self; 6] = [
        Self::Kis, Self::Kiwoom, Self::Ls, Self::Db, Self::Toss, Self::Meritz,
    ];

    pub fn parse(name: &str) -> Result<Self, DecodeError> {
        match name {
            "kis" => Ok(Self::Kis),
            "kiwoom" => Ok(Self::Kiwoom),
            "ls" => Ok(Self::Ls),
            "db" => Ok(Self::Db),
            "toss" => Ok(Self::Toss),
            "meritz" => Ok(Self::Meritz),
            _ => Err(error("broker", DecodeKind::UnknownBroker)),
        }
    }

    pub fn as_str(self) -> &'static str {
        match self {
            Self::Kis => "kis",
            Self::Kiwoom => "kiwoom",
            Self::Ls => "ls",
            Self::Db => "db",
            Self::Toss => "toss",
            Self::Meritz => "meritz",
        }
    }
}

/// Deserialize JSON recursively and reject duplicate keys at EVERY depth.
/// serde_json::Value alone silently keeps a last duplicate value.
struct StrictJson(Value);
struct StrictVisitor;
impl<'de> Deserialize<'de> for StrictJson {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        deserializer.deserialize_any(StrictVisitor)
    }
}
impl<'de> Visitor<'de> for StrictVisitor {
    type Value = StrictJson;

    fn expecting(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str("valid JSON with unique keys at every level")
    }

    fn visit_bool<E: de::Error>(self, value: bool) -> Result<Self::Value, E> {
        Ok(StrictJson(Value::Bool(value)))
    }
    fn visit_i64<E: de::Error>(self, value: i64) -> Result<Self::Value, E> {
        Ok(StrictJson(Value::from(value)))
    }
    fn visit_u64<E: de::Error>(self, value: u64) -> Result<Self::Value, E> {
        Ok(StrictJson(Value::from(value)))
    }
    fn visit_f64<E: de::Error>(self, value: f64) -> Result<Self::Value, E> {
        serde_json::Number::from_f64(value)
            .map(|number| StrictJson(Value::Number(number)))
            .ok_or_else(|| E::custom("nonfinite JSON number"))
    }
    fn visit_str<E: de::Error>(self, value: &str) -> Result<Self::Value, E> {
        Ok(StrictJson(Value::String(value.to_owned())))
    }
    fn visit_string<E: de::Error>(self, value: String) -> Result<Self::Value, E> {
        Ok(StrictJson(Value::String(value)))
    }
    fn visit_none<E: de::Error>(self) -> Result<Self::Value, E> {
        Ok(StrictJson(Value::Null))
    }
    fn visit_unit<E: de::Error>(self) -> Result<Self::Value, E> {
        Ok(StrictJson(Value::Null))
    }
    fn visit_some<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        StrictJson::deserialize(deserializer)
    }
    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<Self::Value, A::Error> {
        let mut elements = Vec::new();
        while let Some(StrictJson(value)) = seq.next_element::<StrictJson>()? {
            elements.push(value);
        }
        Ok(StrictJson(Value::Array(elements)))
    }
    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let mut values = Map::new();
        while let Some((key, StrictJson(value))) = map.next_entry::<String, StrictJson>()? {
            if values.insert(key, value).is_some() {
                return Err(de::Error::custom("duplicate JSON key"));
            }
        }
        Ok(StrictJson(Value::Object(values)))
    }
}

fn object<'a>(value: &'a Value, field: &'static str) -> Result<&'a Map<String, Value>, DecodeError> {
    value.as_object().ok_or_else(|| error(field, DecodeKind::InvalidEnvelope))
}

fn child_object<'a>(
    record: &'a Map<String, Value>,
    key: &'static str,
) -> Result<&'a Map<String, Value>, DecodeError> {
    object(record.get(key).ok_or_else(|| error(key, DecodeKind::MissingRequired))?, key)
}

fn price(
    record: &Map<String, Value>,
    key: &'static str,
    required: bool,
    allow_unsigned_integer: bool,
) -> Result<Option<Price>, DecodeError> {
    let source = match record.get(key) {
        None | Some(Value::Null) if !required => return Ok(None),
        None | Some(Value::Null) => return Err(error(key, DecodeKind::MissingRequired)),
        Some(Value::String(raw)) => raw.as_str().to_owned(),
        Some(Value::Number(n)) if allow_unsigned_integer && n.is_u64() => n.to_string(),
        _ => return Err(error(key, DecodeKind::InvalidPrice)),
    };
    Price::parse(&source, key)
        .map(Some)
        .map_err(|_| error(key, DecodeKind::InvalidPrice))
}

fn volume(record: &Map<String, Value>, key: &'static str) -> Result<Option<u64>, DecodeError> {
    let value = match record.get(key) {
        None | Some(Value::Null) => return Ok(None),
        Some(Value::Number(n)) => n
            .as_u64()
            .ok_or_else(|| error(key, DecodeKind::InvalidField))?,
        Some(Value::String(raw)) if !raw.is_empty() && raw.bytes().all(|b| b.is_ascii_digit()) => {
            raw.parse::<u64>().map_err(|_| error(key, DecodeKind::InvalidField))?
        }
        _ => return Err(error(key, DecodeKind::InvalidField)),
    };
    Ok(Some(value))
}

// Status success code TYPES are native to each provider. In particular,
// Kiwoom's integer 0 cannot become KIS's string "0" accidentally.
#[derive(Debug, Clone, Copy)]
enum StatusSpec {
    ExactText(&'static str),
    IntegerZero,
}

fn status(
    record: &Map<String, Value>,
    key: &'static str,
    accepted: StatusSpec,
) -> Result<(), DecodeError> {
    match (record.get(key), accepted) {
        (None, _) => Ok(()), // Optional in example, not authorization to ignore HTTP errors.
        (Some(Value::String(value)), StatusSpec::ExactText(expected))
            if value == expected => Ok(()),
        (Some(Value::Number(n)), StatusSpec::IntegerZero)
            if n.as_u64() == Some(0) => Ok(()),
        _ => Err(error(key, DecodeKind::SourceStatus)),
    }
}

fn matching_identifier(
    record: &Map<String, Value>,
    key: &'static str,
    requested: &str,
) -> Result<(), DecodeError> {
    match record.get(key) {
        None => Ok(()), // Optional field absent in some publisher examples.
        Some(Value::String(actual)) if actual == requested => Ok(()),
        Some(Value::String(_)) => Err(error(key, DecodeKind::AmbiguousSymbol)),
        Some(_) => Err(error(key, DecodeKind::InvalidField)),
    }
}

fn required_str<'a>(
    record: &'a Map<String, Value>,
    key: &'static str,
) -> Result<&'a str, DecodeError> {
    match record.get(key) {
        None | Some(Value::Null) => Err(error(key, DecodeKind::MissingRequired)),
        Some(Value::String(value)) => Ok(value.as_str()),
        Some(_) => Err(error(key, DecodeKind::InvalidField)),
    }
}

fn toss_record<'a>(
    root: &'a Map<String, Value>,
    requested: &str,
) -> Result<&'a Map<String, Value>, DecodeError> {
    let rows = root.get("result")
        .and_then(Value::as_array)
        .ok_or_else(|| error("result", DecodeKind::InvalidEnvelope))?;
    let mut selected = None;
    for row in rows {
        let entry = object(row, "result")?;
        if required_str(entry, "symbol")? == requested
            && selected.replace(entry).is_some()
        {
            return Err(error("symbol", DecodeKind::AmbiguousSymbol));
        }
    }
    let selected = selected.ok_or_else(|| error("symbol", DecodeKind::MissingRequired))?;
    if required_str(selected, "currency")? != "KRW" {
        return Err(error("currency", DecodeKind::InvalidField));
    }
    if let Some(timestamp) = selected.get("timestamp") {
        if !timestamp.is_null() && !timestamp.is_string() {
            return Err(error("timestamp", DecodeKind::InvalidField));
        }
    }
    Ok(selected)
}

fn blank_prices() -> Prices {
    Prices::default()
}

/// Offline candidate on authenticated-context-assumed KRX only.
/// This does not validate network request provenance or claim a broker works.
pub fn decode_ticker_candidate(
    broker: Broker,
    symbol: &str,
    venue: Venue,
    payload: &str,
) -> Result<CoreTicker, DecodeError> {
    if venue != Venue::Krx {
        return Err(error("venue", DecodeKind::UnsupportedVenue));
    }
    // Reject invalid caller context before any JSON parsing or symbol lookup.
    // Mirror ktradelink-core's ASCII-graphic identifier contract.
    if symbol.is_empty() || !symbol.bytes().all(|b| b.is_ascii_graphic()) {
        return Err(error("symbol", DecodeKind::CoreValidation));
    }
    if payload.len() > MAX_JSON_BYTES {
        return Err(error("payload", DecodeKind::OversizedInput));
    }
    let StrictJson(raw) = serde_json::from_str::<StrictJson>(payload)
        .map_err(|_| error("payload", DecodeKind::InvalidJson))?;
    let root = object(&raw, "payload")?;
    let mut prices = blank_prices();
    let mut qty = None;

    match broker {
        Broker::Kis => {
            status(root, "rt_cd", StatusSpec::ExactText("0"))?;
            let row = child_object(root, "output")?;
            prices.last = price(row, "stck_prpr", true, false)?;
            prices.open = price(row, "stck_oprc", false, false)?;
            prices.high = price(row, "stck_hgpr", false, false)?;
            prices.low = price(row, "stck_lwpr", false, false)?;
            qty = volume(row, "acml_vol")?;
        }
        Broker::Kiwoom => {
            status(root, "return_code", StatusSpec::IntegerZero)?;
            matching_identifier(root, "stk_cd", symbol)?;
            // DO NOT abs() signed Kiwoom price strings until source rules are verified.
            prices.last = price(root, "cur_prc", true, false)?;
            prices.open = price(root, "open_pric", false, false)?;
            prices.high = price(root, "high_pric", false, false)?;
            prices.low = price(root, "low_pric", false, false)?;
            qty = volume(root, "trde_qty")?;
        }
        Broker::Ls => {
            // LS publisher onboarding demo flat JSON, NOT confirmed t1102OutBlock.
            matching_identifier(root, "shcode", symbol)?;
            prices.last = price(root, "price", true, true)?;
        }
        Broker::Db => {
            status(root, "rsp_cd", StatusSpec::ExactText("00000"))?;
            let row = child_object(root, "Out")?;
            prices.last = price(row, "Prpr", true, false)?;
            prices.open = price(row, "Oprc", false, false)?;
            prices.high = price(row, "Hprc", false, false)?;
            prices.low = price(row, "Lprc", false, false)?;
            // Sdpr is a base/reference price; not a proven previous close.
        }
        Broker::Toss => {
            let row = toss_record(root, symbol)?;
            prices.last = price(row, "lastPrice", true, false)?;
            // ISO date-time is present in publisher schema but not parsed yet.
            // PriceResponse has no volume or OHLC.
        }
        Broker::Meritz => {
            // General Meritz success codes belong to DIFFERENT endpoint families.
            // 0001 is an order ACK, 5762 is order history continuation, etc.
            // Only the conservative quote-shaped 0000 candidate is accepted.
            status(root, "rsp_cd", StatusSpec::ExactText("0000"))?;
            let row = child_object(root, "data")?;
            prices.last = price(row, "stck_prpr", true, false)?;
            prices.open = price(row, "oprc", false, false)?;
            prices.high = price(row, "hprc", false, false)?;
            prices.low = price(row, "lprc", false, false)?;
            qty = volume(row, "acml_vol")?;
        }
    }
    let input = TickerInput {
        symbol: symbol.to_owned(),
        venue,
        broker: broker.as_str().to_owned(),
        prices,
        volume: qty,
        timestamp: None,
        retrieved_at: None,
        scope_description: None,
    };
    CoreTicker::new(input).map_err(Into::into)
}
