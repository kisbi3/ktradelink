# Order-book (호가) publisher evidence — 2026-11-05 KST

This ledger supports the **offline** order-book decoder and request-plan
candidates of [ADR 0014](../decisions/0014-offline-order-book-candidates.md).
It records publisher documentation and examples only. No credential, token,
quote, account or order request was sent to any broker; only public pages and
public GitHub files were fetched. Sample tokens, account values and contact
data that appear in some publisher material were not copied.

Evidence level for every row: **publisher example / offline code**. Nothing
here is paper- or live-verified, and nothing is publicly supported.

## Pinned sources

| Broker | Source | Pin | Identity of the retrieved copy |
| --- | --- | --- | --- |
| KIS | [`examples_llm/domestic_stock/inquire_asking_price_exp_ccn/inquire_asking_price_exp_ccn.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_asking_price_exp_ccn/inquire_asking_price_exp_ccn.py) | repo SHA `3a9be59a3ed8745720dc3aa9d584bdf3b7830362` | Git blob `956ce6779b48a8c2f8fd052ef1a0c4703357fa09` |
| KIS | [`…/chk_inquire_asking_price_exp_ccn.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/domestic_stock/inquire_asking_price_exp_ccn/chk_inquire_asking_price_exp_ccn.py) (column mapping) | same | Git blob `0e7385a2acbb431f2dc2ad6a66bf04146ca9f961` |
| KIS | [`examples_llm/kis_auth.py`](https://github.com/koreainvestment/open-trading-api/blob/3a9be59a3ed8745720dc3aa9d584bdf3b7830362/examples_llm/kis_auth.py) (`isOK`, `_url_fetch`) | same | Git blob `0e722d6f3253033efe3cf2b99845397b2b329655` (identical to `examples_user/kis_auth.py`) |
| Kiwoom REST | [`examples/국내주식/시세/get_domestic_stock_quote.py`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/examples/%EA%B5%AD%EB%82%B4%EC%A3%BC%EC%8B%9D/%EC%8B%9C%EC%84%B8/get_domestic_stock_quote.py) | repo SHA `953e5dbff123f437ab4d11a78a95191a685eb51f` | Git blob `77eb09356c8af6a98200cac55688027bba376bb1` (same blob ADR 0003 inspected) |
| Kiwoom REST | [`postman/kiwoom-openapi.postman_collection.json`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API/blob/953e5dbff123f437ab4d11a78a95191a685eb51f/postman/kiwoom-openapi.postman_collection.json), item `주식호가요청(ka10004)` (PRD and MOCK) | same | Git blob `88138bd9be24a6c39b2c8151fa6e465ce12319ce` |
| LS | API guide detail for **t1101** 주식현재가호가조회 (`GET /guide/api/8tb7j8m8-5vb7-jzit-2284-1uc2rte784zb?type=rest&api=54a99b02-dbba-4057-8756-9ac759c9a2ed`, linked from [apiservice](https://openapi.ls-sec.co.kr/apiservice)) | none published; retrieved **2026-11-05 06:16:09 UTC** | sha256 `e3bdd31adba31afb…` (42,632 bytes) |
| LS | API guide detail for **t8450** (통합)주식현재가호가조회2 (same family, `tr` id `3691b2fa-67dc-49a5-aaaf-40aaf52c7bfb`) | retrieved 2026-11-05 06:16:43 UTC | sha256 `0f663f3a7ab7095c…` (57,666 bytes) |

Git blob SHAs were computed with the Git object hash (`blob <len>\0<bytes>`)
over the raw files served for the pinned commit. The LS guide is a live JSON
endpoint without a revision marker, so its hash only identifies the copy
retrieved at that time.

## What each source confirms (and what it does not)

### KIS — `FHKST01010200`, 주식현재가 호가/예상체결

Confirmed by the pinned example:

- `GET /uapi/domestic-stock/v1/quotations/inquire-asking-price-exp-ccn`
  with `FID_COND_MRKT_DIV_CODE` (`J`=KRX, `NX`=NXT, `UN`=통합) and
  `FID_INPUT_ISCD` (6-digit code); `tr_id` `FHKST01010200` for **both**
  `real` and `demo`. `kis_auth._url_fetch` adds `custtype: P` and `tr_cont`.
- Success is `rt_cd == "0"` (string) in `kis_auth.py` `isOK()`.
- `output1` (object) is 호가정보; `output2` is 예상체결정보.
- Ten levels per side: `askp1..10` / `bidp1..10` (매도/매수호가) and
  `askp_rsqn1..10` / `bidp_rsqn1..10` (잔량).

Not documented / unverified (decoder fails closed or leaves out):

- **JSON value types are not shown.** The decoder accepts strings only, by
  precedent with the KIS ticker decoder; a JSON number is rejected.
- How an empty level is encoded is not shown (see policy below).
- No symbol echo in `output1` is documented (`stck_shrn_iscd` appears in the
  shared column mapping without saying which output carries it), so a KIS
  book is **not bound** to the requested symbol by the response.
- `aspr_acpt_hour` (호가 접수 시간) is time-of-day only: `timestamp=None`.
- Whether `J` returns a KRX-only book in every session is unverified.

### Kiwoom REST — `ka10004`, 주식호가요청

Confirmed by the pinned example and Postman field table:

- `POST /api/dostk/mrkcond`, header `api-id: ka10004`, body `{"stk_cd": …}`
  where a bare code is KRX (`039490`), `_NX` NXT and `_AL` SOR. Production
  origin `https://api.kiwoom.com`; mock `https://mockapi.kiwoom.com`.
- Book fields are on the **root** object. Level 1 is `sel_fpr_bid`/
  `sel_fpr_req` (매도최우선) and `buy_fpr_bid`/`buy_fpr_req` (매수최우선);
  levels 2–10 are `sel_{n}th_pre_bid`/`_req` and `buy_{n}th_pre_bid`/`_req`
  with the publisher's literal `2th`/`3th` spelling.
- All fields are `String` (length 20). Quantities: "단위: 1주". Prices:
  "단위: 원, **부호가 포함된 숫자**" (a number that includes a sign).
- The example client treats `return_code` absent or integer `0` as success.

Not documented / unverified:

- **The meaning of the price sign is not stated.** The decoder therefore
  rejects any signed price (`+`/`-`) as `InvalidPrice`; it never applies
  `abs()`. Real responses that carry a sign will fail closed until the sign
  semantics are documented. This is the most likely blocker for real use.
- The response has **no symbol echo** (`stk_cd` is not a response field).
- `bid_req_base_tm` is named "호가잔량기준시간" but described as `YYYYMMDD`;
  contradictory, so `timestamp=None`.
- Empty-level encoding, `return_code` universe and `cont-yn` paging for this
  API are not shown.

### LS — `t1101`, 주식현재가호가조회

Confirmed by the retrieved guide copy:

- `POST https://openapi.ls-sec.co.kr:8080/stock/market-data`,
  `tr_cd: t1101`, 10 TPS; body `{"t1101InBlock":{"shcode":"<6>"}}`.
- Response example: root `rsp_cd: "00000"`, `rsp_msg`, `t1101OutBlock`.
- `offerho1..10` / `bidho1..10` (매도/매수호가, `Number` length 8) and
  `offerrem1..10` / `bidrem1..10` (호가수량, `Number` length 12); the example
  carries them as JSON integers and echoes `shcode`.

Not documented / unverified:

- **`t1101InBlock` has no exchange selector** (unlike `t1102`/`t8450`,
  which take `exchgubun` K/N/U). Which venue's book t1101 returns is not
  stated. For this reason **no LS request plan is offered**; the decoder
  only parses caller-supplied JSON under caller-asserted KRX context.
- `hotime` (수신시간, 8 chars, e.g. `10061477`) is time-of-day only:
  `timestamp=None`.
- `t8450` (통합) does take `exchgubun`, but mixes shared price columns with
  separate `nxt_*`/`unx_*` quantity columns, and its example (requested with
  `N`) shows zero KRX quantities next to non-zero NXT ones. Which quantity
  belongs to which price for each `exchgubun` is not documented, so t8450 is
  **not adopted**.

## Decoder policies derived from the gaps (library policy, not evidence)

- **Status required with its native type:** KIS `rt_cd` `"0"`, Kiwoom
  `return_code` integer `0`, LS `rsp_cd` `"00000"`. Missing or `null` is
  `MissingRequired`; anything else is `SourceStatus`.
- **Every documented level field is required.** Missing, `null`, blank,
  signed, exponent, float or wrongly typed values fail; they are never
  read as "no quote".
- **Empty rank:** no source documents one, so a zero price is never
  interpreted (ADR 0003). A rank whose price **and** quantity are zero is
  `UnverifiedEmptyLevel`; a zero price with non-zero quantity is
  `InvalidPrice`. Neither is dropped or turned into a level, whatever
  `limit` is.
  Nothing is synthesized, sorted, merged or deduplicated.
- **Zero quantity at a quoted price is kept** (the LS t8450 example shows
  such levels).
- **Depth:** 10 per side for all three sources. `limit` is a per-side output
  cap in `1..=10`; `0` is `InvalidLimit`, more than 10 is `DepthExceeded`.
  Ordering is validated over the full book before the cap.
- **Crossed/locked books are preserved**; the model cannot infer auction or
  synchronization state.
- `timestamp`, `retrieved_at` and `scope_description` are `None`; `info` is
  empty.

## Open evidence questions

- KIS: field types; empty-level encoding; symbol echo; session coverage of `J`.
- Kiwoom: sign semantics of `*_bid` prices; empty-level encoding; paging.
- LS: venue of the t1101 book; t8450 price/quantity association per
  `exchgubun`; empty-level encoding.
- All: gateway acceptance, error-status universe and rate limits, verified
  only with explicit maintainer authorization and never in CI.
