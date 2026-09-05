# Memo — idea 102, pruned macro sleeve (NOT ADOPTABLE THIS WEEK)

1. **Finding.** S4's diversification is carried by **GLD (53% of sleeve return)**, not TLT (9.1%);
   TLT-only as a sleeve has dSharpe < 0 in 8/8 cells and 0/48 4b passes, and deleting TLT retains
   81-103% of the benefit — so idea 100's result is **not** a falling-rate artefact.
2. **Best book produced:** `top20 + 50% sleeve(TLT,GLD,UUP)` at 100% gross — u56 11.5%/**1.167**/
   **-13.3%** (H1 1.169 / H2 1.167, OOS 1.215); broad 12.0%/1.073/-14.6% (1.245/0.917, OOS 0.985).
3. Clears **4a in 8/8** cells and **4b on both universes** to 15 bps; beats SPY (0.889/-33.7%) and
   RULES v1 (0.664/0.635) on every bar; rule 8 picks this exact composition in 6/8 cells.
4. **Why not adopt:** it inherits idea 100's un-pre-registered g=1.00 dial AND selects the
   composition across six variants. Two un-pre-registered dials is PROTOCOL rule 7 territory.
5. **Route to adoption:** idea 101 is already re-running `top20 + 50% S4` with g fixed ex ante at
   1.00, the full cost ladder and idea 65's cadence bar. Add the `(TLT,GLD,UUP)` composition as a
   *second pre-registered arm* of that run (idea 104) rather than opening a third study.
6. Only if idea 101/104 clears on its own pre-registration should the Sunday review see wording.
7. **Exact RULES wording to hold in reserve** (do not adopt until 104 reports):

> **RULES v2 — candidate, not adopted.** Hold two sleeves at all times, rebalanced Friday at the
> close, executed at the next close, fully invested (100% gross, no leverage, no shorting).
> **Equity sleeve (50% of capital):** equal-weight the 20 highest-composite names among those
> trading above their 200-day moving average with 20-day annualised volatility below 0.60, where
> composite = mean of the percentile ranks of 12-1 month, 6-month and 3-month return (no
> volatility scaler). If fewer than 20 are eligible, hold those that are and let the macro sleeve
> take the remainder. **Macro sleeve (50% of capital):** hold TLT, GLD and UUP, each weighted by
> (fraction of {12-1, 6-month, 3-month} returns that are positive) x (inverse 60-day volatility),
> normalised across the three. Rescale the combined book to 100% gross each Friday.

8. **Numbers the review must see if it ever votes on this:** 12.4-15.2x annual turnover (vs RULES
   v1's much lower book), 4b lost by 20 bps, and a 4.7-year rising-rate sample behind the whole
   regime argument.
9. **Known weakness to state out loud:** the sleeve's edge is gold. That is a narrower claim than
   "multi-asset diversification" and has not been tested against SLV/IAU or a gold-free variant
   (idea 105).
10. **This week: no rules change.** RULES.md, scan.py, bot.py and baseline.py untouched by this run.
