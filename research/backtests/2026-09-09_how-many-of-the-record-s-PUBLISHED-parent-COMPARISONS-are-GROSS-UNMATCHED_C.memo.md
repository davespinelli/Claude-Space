# PARK memo — U56 BREADTH-DG q=0.20 g=1.00 (idea 581 by-product, NOT a promotion)

1. **What it is.** Equal-weight every priced name in `research/universe.json` at gross 1.00/N;
   when market breadth is in its bad tail, send the whole book to CASH. Weekly, t+1, 10 bps.
2. **Rule 8 was run properly:** (dial, g) chosen on 2009–2016 only, evaluated on 2017–2026
   untouched, and the pick is identical under both the unmatched and the matched-gross
   selection rule.
3. **Full sample** CAGR 16.01% / Sharpe 1.258 / MaxDD −16.48%, halves 1.187 / 1.357.
   **OOS 2017–2026** CAGR 16.39% / Sharpe 1.456 / MaxDD −14.16%.
4. **vs SPY** (CAGR 15.19% / Sharpe 0.887 / MaxDD −33.72%, halves 0.959 / 0.829, OOS Sharpe 0.879)
   and **vs RULES v2** (CAGR 8.64% / Sharpe 1.204 / MaxDD −12.05%, OOS Sharpe 1.282).
5. **KEEP path 4b passes on all five legs:** Sharpe > SPY in both halves (1.187 > 0.959,
   1.357 > 0.829) and OOS (1.456 > 0.879); MaxDD −16.48% ≤ 60% of SPY's −20.23%; CAGR 16.01%
   ≥ 70% of SPY's 10.63%.  **4a fails** (MaxDD −16.48% worse than RULES v2's −12.05%).
6. **It survives this run's own criticism:** at matched gross its edge over its own control is
   dSharpe +0.135 (vs +0.135 unmatched) and dMaxDD +0.091 (vs +0.127 unmatched, so 29% of the
   drawdown edge was exposure and 71% was not); dCAGR is +0.75 pp at matched gross.
7. **Why it is PARKed, not proposed.** It re-discovers a family the record priced on 2026-09-09
   ("the gate is a volatility discount, not a bear defence", six rule-8 picks failing on the
   CAGR floor).  The reconciliation is one number: that run held the gate at gross 0.75, where
   the CAGR floor bites; this one clears the floor only at gross 1.00.  A KEEP that depends on
   the gross dial is idea 311's g-band loophole, and this run did not test it as such.
8. **Second reason to PARK:** the two tuned parameters here were spent on the CENSUS grid
   (dial, g), not chosen to make this book work; treating a by-product of an audit grid as a
   capital candidate is exactly the selection the protocol's rule 8 exists to stop.
9. **Survivorship:** `research/universe.json` is a current-constituent list, so the LEVEL is
   biased up; the matched-gross deltas in §6 are differences on a fixed panel and are not.
10. **Exact RULES wording if a Sunday review ever promotes it** (do NOT apply now):
    *"Hold every name priced today at gross 1.00 / N of NAV, N = names priced that day. Compute
    breadth as the fraction of those names trading above their own 200-day moving average. If
    breadth is below its trailing 5-year 20th percentile (1260 trading days, minimum 504) at
    today's close, hold no equities and stay in cash; otherwise hold the equal-weight book.
    Rebalance weekly on the last trading day of the week, executed at the next close."*
