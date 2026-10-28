# KIS domestic equity market-data evidence

- Research date: **2026-10-29 KST**
- Status: **documentary endpoint discovery**, not live integration verification
- Vendor: Korea Investment & Securities (KIS), Open Trading API
- Intended transport: KIS Open API; no credentials or requests used in this research

## Publisher-owned references

- [KIS official examples repository](https://github.com/koreainvestment/open-trading-api)
- [Current quote example — `inquire_price`](https://github.com/koreainvestment/open-trading-api/blob/main/examples_llm/domestic_stock/inquire_price/inquire_price.py)
- [Daily/weekly/monthly/yearly bars — `inquire_daily_itemchartprice`](https://github.com/koreainvestment/open-trading-api/blob/main/examples_llm/domestic_stock/inquire_daily_itemchartprice/inquire_daily_itemchartprice.py)
- [Official publisher endpoint registry](https://github.com/koreainvestment/open-trading-api/blob/main/MCP/Kis%20Trading%20MCP/configs/domestic_stock.json)
- [Publisher's use-case examples](https://github.com/koreainvestment/open-trading-api/blob/main/examples_user/domestic_stock/domestic_stock_examples.py)

These sources are publisher-owned *examples and registry*, not an authenticated
account test. Verify the vendor portal's latest specification before writing
parsers or releasing a support claim.

## Confirmed endpoint candidates

| Unified candidate | Publisher function | Endpoint path | Auth/TR ID where found | Evidence |
| --- | --- | --- | --- | --- |
| `fetch_ticker` | `inquire_price` | `/uapi/domestic-stock/v1/quotations/inquire-price` | `FHKST01010100` | current quote example |
| `fetch_order_book` | `inquire_asking_price_exp_ccn` | `/uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn` | verify exact TR ID against current example before implementation | publisher registry |
| `fetch_ohlcv` (D/W/M/Y) | `inquire_daily_itemchartprice` | `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice` | `FHKST03010100` | period-bar example |
| `fetch_ohlcv` (intraday candidate) | `inquire_time_itemchartprice` / `inquire_time_dailychartprice` | `/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice` / `inquire-time-dailychartprice` | not yet mapped | publisher registry |
| `load_markets` | publisher's `stocks_info` reference | no confirmed REST contract | n/a | current quote example points to master files |

**Existence of a publisher example does not establish** supported account
entitlements, current market-data rights, real/paper parity, a normalized result,
or correctness of a KTradeLink implementation.

## Request detail supported by publisher examples

For `inquire_price`, examples show:

- `FID_INPUT_ISCD="005930"` for Samsung Electronics.
- `FID_COND_MRKT_DIV_CODE` values `J` (KRX), `NX` (NXT),
  `UN` (통합 / publisher-described integrated quote).
- ETN codes may follow another format; **ETN is outside first-version scope**.
- KIS states to use WebSocket rather than the REST current-quote endpoint for
  real-time feeds; therefore `fetch_ticker` must not promise tick-by-tick
  streaming or a guaranteed fresh exchange timestamp.

For `inquire_daily_itemchartprice`, examples show:

- `FID_INPUT_DATE_1` and `FID_INPUT_DATE_2` are request dates.
- `FID_PERIOD_DIV_CODE`: `D`, `W`, `M`, `Y`.
- `FID_ORG_ADJ_PRC` is required; this endpoint's example documents
  `0` adjusted, `1` original.
- The example states **up to 100 rows per call**. Verify any continuation,
  response ordering and boundary behavior before promising arbitrary
  `since`/`limit` coverage.

## Outstanding source-level checks (not verified yet)

1. Which exact quote fields are present, optional, delayed, numeric-string, or
   dependent on the exchange selection? Confirm native output schemas.
2. `output1` order book level mappings and timestamp source/precision.
3. Minutes vs daily: session coverage, data quality and cross-venue meaning.
4. `FID_ORG_ADJ_PRC` semantics **per endpoint**, not globally. Different KIS
   sample endpoints have used differing descriptions; do not silently unify.
5. Real/paper availability and KIS per-TR rate limits must be checked in the
   up-to-date vendor portal; never assume a generic per-second limit.
6. Market master coverage, refresh cadence, permitted local caching and
   redistribution license are still unverified.
7. No tokens/accounts/real exchange data were fetched here.
