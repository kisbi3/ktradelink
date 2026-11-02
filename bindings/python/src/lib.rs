//! Thin Python boundary. Existing Python Ticker remains the final public model.
use ktradelink_core::{CoreError, CoreTicker, Price, Prices, TickerInput, Venue};
use ktradelink_decoders::{decode_ticker_candidate, Broker, DecodeError};
use pyo3::exceptions::{PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyInt};

fn core_error(error: CoreError) -> PyErr {
    PyValueError::new_err(error.to_string())
}

fn decoder_error(error: DecodeError) -> PyErr {
    PyValueError::new_err(error.to_string())
}

fn price(value: Option<&str>, field: &'static str) -> PyResult<Option<Price>> {
    value.map(|text| Price::parse(text, field).map_err(core_error)).transpose()
}

fn integer(value: Option<&Bound<'_, PyAny>>, field: &'static str) -> PyResult<Option<u64>> {
    match value {
        None => Ok(None),
        Some(value) => {
            if value.is_instance_of::<PyBool>() || !value.is_instance_of::<PyInt>() {
                return Err(PyTypeError::new_err(format!("{field} must be int or None, not bool")));
            }
            value.extract::<u64>().map(Some).map_err(|_| {
                PyValueError::new_err(format!("{field} must fit an unsigned 64-bit integer"))
            })
        }
    }
}

/// One conversion implementation for the old normalized-value seam and ALL
/// six publisher-evidence offline candidates; do not make a replacement Ticker.
fn into_python_ticker(py: Python<'_>, quote: &CoreTicker) -> PyResult<Py<PyAny>> {
    let q = quote.input();
    let kwargs = PyDict::new(py);
    kwargs.set_item("symbol", &q.symbol)?;
    kwargs.set_item("venue", q.venue.as_str())?;
    kwargs.set_item("broker", &q.broker)?;
    kwargs.set_item("volume", q.volume)?;
    kwargs.set_item("timestamp", q.timestamp)?;
    kwargs.set_item("retrieved_at", q.retrieved_at)?;
    kwargs.set_item("scope_description", q.scope_description.as_deref())?;
    kwargs.set_item("info", PyDict::new(py))?; // No upstream JSON metadata.
    let decimal = py.import("decimal")?.getattr("Decimal")?;
    for (field, value) in [
        ("last", &q.prices.last), ("open", &q.prices.open), ("high", &q.prices.high),
        ("low", &q.prices.low), ("previous_close", &q.prices.previous_close),
        ("bid", &q.prices.bid), ("ask", &q.prices.ask),
    ] {
        match value {
            Some(value) => kwargs.set_item(field, decimal.call1((value.as_str(),))?)?,
            None => kwargs.set_item(field, py.None())?,
        }
    }
    // Python Ticker is the sole public value contract authority.
    let ticker = py.import("ktradelink.models")?.getattr("Ticker")?;
    Ok(ticker.call((), Some(&kwargs))?.unbind())
}

#[allow(clippy::too_many_arguments)]
#[pyfunction]
#[pyo3(signature = (symbol, venue, broker, *, last=None, open=None, high=None, low=None,
    previous_close=None, bid=None, ask=None, volume=None, timestamp=None,
    retrieved_at=None, scope_description=None))]
fn _build_ticker(
    py: Python<'_>, symbol: &str, venue: &str, broker: &str,
    last: Option<&str>, open: Option<&str>, high: Option<&str>, low: Option<&str>,
    previous_close: Option<&str>, bid: Option<&str>, ask: Option<&str>,
    volume: Option<&Bound<'_, PyAny>>, timestamp: Option<&Bound<'_, PyAny>>,
    retrieved_at: Option<&Bound<'_, PyAny>>, scope_description: Option<&str>,
) -> PyResult<Py<PyAny>> {
    let input = TickerInput {
        symbol: symbol.into(), venue: Venue::parse(venue).map_err(core_error)?,
        broker: broker.into(),
        prices: Prices {
            last: price(last, "last")?, open: price(open, "open")?,
            high: price(high, "high")?, low: price(low, "low")?,
            previous_close: price(previous_close, "previous_close")?,
            bid: price(bid, "bid")?, ask: price(ask, "ask")?,
        },
        volume: integer(volume, "volume")?, timestamp: integer(timestamp, "timestamp")?,
        retrieved_at: integer(retrieved_at, "retrieved_at")?,
        scope_description: scope_description.map(str::to_owned),
    };
    let quote = CoreTicker::new(input).map_err(core_error)?;
    into_python_ticker(py, &quote)
}

/// PRIVATE research tool: parse a source-shaped JSON document supplied by a
/// caller, with no evidence that the caller actually queried that broker.
/// It is NOT a published fetch_ticker adapter.
#[pyfunction]
fn _decode_ticker_candidate(
    py: Python<'_>, broker: &str, symbol: &str, venue: &str, payload: &str,
) -> PyResult<Py<PyAny>> {
    let selected = Broker::parse(broker).map_err(decoder_error)?;
    let venue = Venue::parse(venue).map_err(core_error)?;
    let quote = decode_ticker_candidate(selected, symbol, venue, payload)
        .map_err(decoder_error)?;
    into_python_ticker(py, &quote)
}

#[pymodule]
fn _ktradelink_native(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add("CORE_VERSION", ktradelink_core::CORE_VERSION)?;
    module.add("CONTRACT_VERSION", ktradelink_core::CONTRACT_VERSION)?;
    module.add_function(wrap_pyfunction!(_build_ticker, module)?)?;
    module.add_function(wrap_pyfunction!(_decode_ticker_candidate, module)?)?;
    Ok(())
}
