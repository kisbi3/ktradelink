//! Isolated synthetic JSON parsing probe: not a provider adapter or stable SDK.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct SyntheticQuote {
    symbol: String,
    venue: String,
    last: Option<String>,
    open: Option<String>,
    high: Option<String>,
    low: Option<String>,
    previous_close: Option<String>,
    volume: Option<u64>,
    timestamp: Option<u64>,
    retrieved_at: Option<u64>,
}

// Experimental FFI value: a tuple in known field order, not a public return type.
type RawRow = (
    String, String, Option<String>, Option<String>, Option<String>, Option<String>,
    Option<String>, Option<u64>, Option<u64>, Option<u64>,
);

fn decode(payload: &str) -> PyResult<RawRow> {
    let q: SyntheticQuote = serde_json::from_str(payload)
        .map_err(|err| PyValueError::new_err(format!("invalid synthetic quote JSON: {err}")))?;
    Ok((
        q.symbol,
        q.venue,
        q.last,
        q.open,
        q.high,
        q.low,
        q.previous_close,
        q.volume,
        q.timestamp,
        q.retrieved_at,
    ))
}

#[pyfunction]
fn parse_one_json(payload: &str) -> PyResult<RawRow> {
    decode(payload)
}

#[pyfunction]
fn parse_batch_json(payloads: Vec<String>) -> PyResult<Vec<RawRow>> {
    payloads.iter().map(|payload| decode(payload)).collect()
}

#[pymodule]
fn ktl_rust_parse_probe(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(parse_one_json, module)?)?;
    module.add_function(wrap_pyfunction!(parse_batch_json, module)?)?;
    Ok(())
}
