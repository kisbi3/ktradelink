# ADR 0016: KR equity symbol grammar — six uppercase ASCII alphanumerics

- Date: 2026-11-05 (Asia/Seoul)
- Status: **proposed for independent review; offline implementation**. Not
  live- or paper-verified. Merging this authorises no broker call,
  credential use, account access or order.
- Base: `main` `a5d2639e1b555b54c7a96652432cc2c3bf141fb7`.
- Related: Issue #17. Maintainer decision on gate G-I1 ("①로 하자": widen to
  six ASCII upper-alphanumerics). Supersedes the six-digit symbol sentence
  in ADR 0013 decision item 1 and in
  [market-data spec §3](../specifications/market-data-v0.1-draft.md), and the
  per-broker symbol statements in ADR 0007 ("Provider boundaries", first
  bullet) and ADR 0015 item 5 (`"<6 digits>"`). Everything else in ADR
  0002–0015 stays binding; ADR 0002's rule that value models do not enforce
  a numeric-only symbol is unchanged.
- Evidence: `docs/brokers/symbol-master-evidence-2026-11-05.md` §2.4, §5.4,
  §6.4, §7.4, §8.3 item 1 and §10.1 G-I1–G-I3, on branch
  `claude/issue-17-symbol-master-evidence` at
  `b127724ee73fac239d987a2fa2a5b889c5f92bfb` (not merged when this was
  written).

## Context

ADR 0013 made `fetch_ticker` reject every symbol that is not exactly six
ASCII digits, following spec §3. The symbol-master audit found
six-character codes that mix digits and uppercase letters at four of the six
brokers:

| Broker | Evidence | Level |
| --- | --- | --- |
| KIS | KOSPI master file: six-character codes with letters in `ST` (common and preferred), `EF`, `RT`, `PF` (§2.4) | file observation, one copy |
| DB | `JCODES` response example: `"Iscd": "0000D0"` (§5.4) | publisher example |
| Toss | `Symbol`/`SymbolQuery`/`KrSymbol`: "6자리 종목코드 (숫자 또는 영문·숫자 조합; 예: 005930, 0101N0)" (§6.4) | field table |
| Meritz | KOSPI and KOSDAQ master files: six-character codes with letters (§7.4) | file observation, one copy |
| Kiwoom | `ka10099`/`ka10100` examples show only digits; nothing excludes letters (§3.4) | not documented |
| LS | `shcode` String 6; examples show only digits; nothing excludes letters (§4.4) | not documented |

The six-digit rule therefore rejects listed instruments, including some KRX
common shares in the KIS master (G-I1).

## Decision

1. **Public grammar.** A KR equity symbol passed to the public API is
   exactly six ASCII characters, each in `[0-9A-Z]`. Anything else raises
   `InvalidSymbol("symbol_must_be_six_uppercase_alphanumerics")`, `NOT_SENT`:
   lowercase (`0000d0`), whitespace anywhere, native prefixes and suffixes
   (`A005930`, `Q500001`, `J005930`, `005930_NX`, `005930_AL`, `N-005930`,
   `U-005930`), any other length (5, 7, 9 …), non-ASCII characters
   (including full-width `０`–`９`, `Ａ`–`Ｚ`), and non-`str` values.
2. **No normalisation.** No case folding, trimming, padding, truncation or
   prefix/suffix stripping (G-I2, G-I3). The symbol is sent and returned
   verbatim.
3. **Per-broker request acceptance is separate from the grammar.** A digit-only
   symbol is accepted for every broker as before. A symbol containing a
   letter is accepted only for a broker whose publisher evidence shows such
   codes: **KIS, DB, Toss and Meritz** (table above).
4. **Kiwoom and LS** neither show nor exclude alphanumeric codes. A
   well-formed alphanumeric symbol for them is a capability gap, not a bad
   symbol: `fetch_ticker` raises
   `UnsupportedCapability("alphanumeric_symbol_not_evidenced_for_broker")`,
   `NOT_SENT`, and the offline planners (`plan_ticker_request`,
   `plan_order_book_request`) raise `QuotePlanUnavailable`.
5. **Order of checks.** The grammar and the per-broker rule run in
   `_check_symbol`, the first of `fetch_ticker`'s argument checks (ADR 0013
   item 1), so a refused symbol never reaches the closed-client,
   network-enabled or native-decoder checks, the token request or the
   transport. `_check_symbol` requires the broker argument, so a new caller
   cannot skip the per-broker rule.
6. **Digit-only behaviour is unchanged** for all six brokers, in the public
   client and in the planners.
7. **Toss lower case.** Toss's request pattern `^[A-Za-z0-9.\-]+$` admits
   lower case, `.` and `-`; the previous Toss-only planner check accepted
   lowercase ASCII letters. The public grammar does not, so a lowercase
   Toss symbol is now refused. This is a deliberate tightening.

The single source of truth is `ktradelink._request_plan`
(`_is_public_symbol`, `_symbol_evidenced_for`,
`_ALPHANUMERIC_SYMBOL_BROKERS`); `_public_client._check_symbol` and the
order-book planner reuse it. The Rust core and decoders are unchanged: they
already accept any non-empty ASCII-graphic symbol and the LS decoder still
compares the `shcode` echo exactly.

## Not verified (stated limits)

- **Nothing here is live- or paper-verified.** No gateway has received an
  alphanumeric symbol from KTradeLink.
- **KIS:** the evidence is one copy of a master file. Whether the
  `inquire-price` (`FHKST01010100`) or `inquire-asking-price-exp-ccn`
  (`FHKST01010200`) route accepts an alphanumeric `fid_input_iscd` is not
  documented and not verified.
- **DB:** the example is from the `JCODES` master route. Whether the PRICE
  route accepts an alphanumeric `InputIscd1` is not documented.
- **Meritz:** the evidence is a master-file observation. The REST `iscd`
  description names only `005930`/`A005930` forms; whether it accepts an
  alphanumeric code is not documented (§7.4, §11). Meritz returns `"0000"`
  with empty values for unknown codes, so a refused code may look like
  success. Meritz has no public `fetch_ticker`.
- **Toss:** documented in the request schema only; no response observed.
  DB and Toss have no public `fetch_ticker` either (ADR 0013, ADR 0015).
- **Kiwoom and LS:** whether their masters or quote routes carry
  alphanumeric codes is unknown. Accepting them needs publisher evidence or
  an authorised, sanitised fixture and a new reviewed decision.
- The grammar does not decide instrument type (G-T6): an accepted symbol may
  be a share, ETF, REIT or other product. ETN (`Q` + 6), ELW and 9-character
  codes stay outside the grammar until a `load_markets` decision.

## Consequences

- Error reason `symbol_must_be_six_uppercase_alphanumerics` replaces
  `symbol_must_be_six_ascii_digits`. Callers matching the old reason string
  must update; the exception class is unchanged.
- `tools/live_smoke_ls.py` keeps its `[0-9]{6}` symbol check: it is an LS-only
  tool and LS stays digit-only under item 4.
- ADR 0013 is left as written; this ADR records the change.
