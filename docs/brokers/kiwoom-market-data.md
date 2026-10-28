# Kiwoom REST domestic equity market-data evidence

- Research date: **2026-10-29 KST**
- Status: **documentary endpoint discovery**, not live integration verification
- Target: **Kiwoom REST API** (HTTP), **not** legacy Windows COM/OCX OpenAPI+

## Publisher-owned references

- [Kiwoom REST API developer portal](https://openapi.kiwoom.com/guide/apiguide)
- [Kiwoom REST API service details and documented quotas](https://openapi.kiwoom.com/intro?dummyVal=0)
- [Official Kiwoom REST API GitHub repository](https://github.com/Kiwoom-Securities/Kiwoom-REST-API)
- [Official stock information example (`ka10001`)](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%A2%85%EB%AA%A9%EC%A0%95%EB%B3%B4/get_domestic_stock_info.py)
- [Official quote-depth example (`ka10004`)](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%9C%EC%84%B8/get_domestic_stock_quote.py)
- [Official minute-chart example (`ka10080`)](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/main/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%B0%A8%ED%8A%B8/get_domestic_stock_minute_chart.py)

These are publisher-controlled sources; code examples should still be checked
against the current downloadable API specification. No token was used.

## Confirmed endpoint candidates

| Unified candidate | Kiwoom API ID | REST path | Evidence |
| --- | --- | --- | --- |
| `fetch_ticker` | `ka10001` (`주식기본정보요청`) | `POST /api/dostk/stkinfo` | publisher-owned stock information example |
| `fetch_order_book` | `ka10004` (`주식호가요청`) | `POST /api/dostk/mrkcond` | publisher-owned quote-depth example |
| `fetch_ohlcv` (minute) | `ka10080` (`주식분봉차트조회요청`) | `POST /api/dostk/chart` | publisher-owned minute-chart example |
| `fetch_ohlcv` (day) | `ka10081` (`주식일봉차트조회요청`) | `/api/dostk/chart` path **still requires endpoint-specific confirmation** | publisher portal API guide lists `ka10081`; chart path established for `ka10080` |
| `fetch_ohlcv` (week/month) | `ka10082`, `ka10083` | confirm per-ID paths and outputs | publisher portal lists names |
| `load_markets` | no selected authoritative endpoint/master mechanism yet | unknown | unresolved |

The official examples use `api-id` to select a Kiwoom TR. Merely finding an
API ID does **not** prove its availability in a paper account or for every venue.

## Documented request and response clues

- `stk_cd` can be market-qualified in the Kiwoom REST examples:
  `039490` (KRX), `039490_NX` (NXT), `039490_AL` (SOR).
  These are **broker-native identifiers**, not KTradeLink symbols.
- `ka10001` exposes fields such as `cur_prc`, `open_pric`,
  `high_pric`, `low_pric`, `trde_qty`, and `pred_pre`. Sign-bearing
  strings must be interpreted **field by field**; do not call `abs` on every
  value (a signed day-over-day change has different semantics from a price).
- `ka10004` includes quote-depth and level-size fields; check the complete
  response schema for level ordering and any source timestamp.
- `ka10080` uses `tic_scope` (e.g. 1, 3, 5, 10, 15, 30, 45, 60-minute
  intervals shown in official sample), `upd_stkpc_tp` and `base_dt`.
  The example identifies response keys including `cntr_tm` and
  `stk_min_pole_chart_qry`. Daily/weekly/monthly bar date labels and
  calendar boundaries need their own verification.
- The official portal states domestic-equity REST request throttling for real
  accounts: account/token **orders 5/s and inquiries 5/s**; paper accounts
  have additional per-TR restrictions. This is *documentation*, not live
  rate-limit testing, and must not be copied as a universal KIS quota.
- Official portal lists `https://api.kiwoom.com` and
  `https://mockapi.kiwoom.com` as respective environments, with distinct
  entitlements. The initial normalized client remains read-only.

## Outstanding checks (not verified yet)

1. The exact official `ka10081` per-ID request/response specification,
   date/adjustment semantics and pagination headers (`cont-yn`, `next-key`).
2. Whether `_AL` SOR quotes are equivalent to KIS `UN` integrated quotes;
   **do not map them to the same normalized scope without evidence**.
3. Order-book timestamp source, empty levels, signed field semantics and whether
   quote fields are same-session vs delayed across environments.
4. Client clock handling, daily candle timestamp source, and intraday session
   time conventions require sanitized reference fixtures.
5. Market master list API/licensing and any data redistribution conditions.
6. No real brokerage responses, credentials, order activity, or credentials
   were used during this research.
