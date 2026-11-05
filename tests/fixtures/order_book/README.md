# Synthetic order-book (호가) decoder fixtures

Every value in these files is **invented**. Only the field **names** and
outer JSON layout follow publisher documentation pinned in
[`docs/brokers/order-book-evidence-2026-11-05.md`](../../../docs/brokers/order-book-evidence-2026-11-05.md):

| File | Publisher shape |
| --- | --- |
| `kis-fhkst01010200-synthetic.json` | KIS `inquire-asking-price-exp-ccn` (`FHKST01010200`): root `rt_cd`, `output1` book object, `output2` |
| `kiwoom-ka10004-synthetic.json` | Kiwoom REST `ka10004` root object with `return_code` |
| `ls-t1101-synthetic.json` | LS `t1101` REST: root `rsp_cd`, `t1101OutBlock` |

They are **not** captured, authorized or verified broker responses and must
not be cited as evidence of live behavior. The `_note` key is a marker that
no publisher sends; decoders ignore unmapped fields. No token, account,
MAC or other credential value appears here.

All three files encode the same synthetic book: asks 70100..71000 and bids
70000..69100 in 100 KRW steps, with one zero-quantity level per side
(`asks[2]`, `bids[1]`) to exercise "zero size kept when a price is given".
