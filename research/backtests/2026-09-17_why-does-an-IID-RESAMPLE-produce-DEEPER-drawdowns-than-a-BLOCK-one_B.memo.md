# Memo — idea 1162 (lane B, 2026-09-17): the C_GATEOFF 4b band. **RECOMMENDATION: PARK.**

Written because PROTOCOL rule 4 path 4b passed, not because anything here should be enacted.
`C_GATEOFF` was built as a MECHANISM CONTROL for idea 1162's bootstrap question and is proposed
as a book by nobody, this memo included.

1. **Exact RULES wording, if it were ever enacted:** *"each Friday, rank every priced name by
   the CAND20 composite (12-1 momentum, 6-month and 3-month total return, equal-weighted
   percentile ranks), hold the top 20 at 0.75/N of NAV with a 126-trading-day minimum holding
   period, and apply NO 200-day trend filter and NO realised-volatility ceiling."* It is the
   live RULES v2 selection machinery with clause 2 (the 200d ±3% band) and the `max_vol 0.60`
   ceiling deleted.
2. **What passes.** U56 gross 0.55–0.75 clears 4b full AND 4b OOS; B136 gross 0.50–0.65 does.
   At U56/0.75: full 15.76% / 1.1445 / −20.11% (halves 1.2731/1.0520), OOS 16.85% / 1.1461.
3. **It is strictly dominated by the incumbent.** U56 C_BOOK at the same gross 0.75 posts
   15.55% / 1.1381 / −19.13%, OOS **1.1615** against C_GATEOFF's **1.1461**, with a SHALLOWER
   drawdown (−19.13% vs −20.11%) and a much better second half (1.0932 vs 1.0520).
4. **Rule 8 does not reach it.** All three IS-only choosers pick something else (C_GATEOFF 0.95,
   C_NOREBAL 1.00, C_GATEOFF 0.30 on U56); **0 of 9 picks clear 4b full or 4b OOS** on any panel.
5. **Path 4a is 0 of 180 books** and 0 of 60 on U56 — it never beats the live book's Sharpe in
   both halves at a drawdown no worse.
6. **Honest discount.** Removing the trend gate raises gross exposure through every drawdown, so
   the 4b pass is bought with beta in a tape whose two crashes both recovered inside the sample.
7. **Survivorship (rule 9).** U56 and B136 are current-constituent panels; the CAGR floor and
   the drawdown cap are both measured against an inflated book and the bias does NOT cancel.
8. **The cheapest counter-test** before anyone revisits this: re-run the band on a tape that
   contains a crash with no in-sample recovery, and on a delisting-aware panel.
9. **Nothing is proposed for the Sunday review** (rule 6). RULES.md, PROTOCOL.md, scan.py,
   bot.py and baseline.py are untouched by this run.
10. **PARK.** A control that happens to clear a bar is not a candidate; it is a control.
