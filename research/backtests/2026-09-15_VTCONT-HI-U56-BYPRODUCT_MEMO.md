# By-product memo — U56 continuous vol target (VTCONT-HI), idea 870, 2026-09-15. NOT PROPOSED.

1. **What it is.** Hold the RULES-v1-eligible equal-weight book at gross 1.00, scaled every week
   by a continuous realised-vol target: `m_t = clip(σ*_t / σ_t, 0.50, 1.00)` where σ_t is the
   20-day annualised volatility of the equal-weight book's own returns and σ*_t is that series'
   83rd percentile over a rolling 252-day window. Never levers. Weekly cadence, 10 bps, t+1,
   U56 panel. This is the textbook vol target, and it had **never been priced in this record** —
   every prior gate family is a binary de-gross, not a continuous scaler.
2. **Full sample (2009-02→2026-09):** CAGR **13.66%**, Sharpe **1.098**, MaxDD **−18.79%**,
   halves **1.107 / 1.089**.
3. **Out of sample (rule 8, (q,w) chosen on 2009-2016 IS Sharpe only, read on 2017+ once):**
   CAGR **14.73%**, Sharpe **1.178**, MaxDD **−18.79%**.
4. **Comparands:** SPY 15.13% / 0.885 / −33.72% (H 0.959/0.824; OOS 15.27% / 0.874);
   RULES v2 (live) 8.64% / 1.208 / −11.90% (OOS 9.49% / 1.286 / −11.90%).
5. **PROTOCOL path 4b:** PASSES — Sharpe > SPY in both halves (1.107 > 0.959, 1.089 > 0.824) and
   out of sample (1.178 > 0.874); MaxDD −18.79% inside the −20.23% cap (60% of SPY's); CAGR
   13.66% above the 10.59% floor (70% of SPY's). Holds at **0 / 10 / 25 bps**
   (Sharpe 1.104 / 1.098 / 1.089; CAGR 13.75% / 13.66% / 13.54%). **Path 4a FAILS** — RULES v2's
   Sharpe is higher in both halves and its −11.90% drawdown is shallower.
6. **Exact RULES wording if it were ever promoted:** *"Clause N (continuous vol target): at the
   close of each weekly rebalance day t, compute σ_t = the 20-day annualised standard deviation
   of the equal-weight eligible panel's daily return, and σ\*_t = the 83rd percentile of σ over
   the trailing 252 trading days. Set the book's gross to `min(1.00, max(0.50, σ\*_t / σ_t))` of
   NAV, held equal-weight across the eligible names from day t+1 until the next rebalance; the
   un-invested remainder is held in cash and is never re-spread. Never lever above gross 1.00."*
7. **Why it is genuinely interesting.** It is the **cheapest** book on the 4b shelf: gate
   turnover **0.71/yr** against CORR-HI's 2.16 for a comparable Sharpe, because a continuous
   scaler trades small and often instead of all-or-nothing. Its cost decay over the whole
   0→25 bps ladder is **0.015 of Sharpe**, the smallest in this run's 3,456 arms.
8. **Why it is NOT proposed.** **352 of 3,456** arms in this grid clear 4b on the full sample
   *and* out of sample, and **every one of them is HI-side**. This is the best of a large field
   read off a grid built for a different question — selection, not evidence. Its own family is
   90 / 432 on full-sample 4b, and on B136 only 5 of 144 arms pass both ways, 0 of 144 on SMALL,
   so the result does not travel off U56.
9. **And it is the opposite tail from the idea that produced it.** Idea 870 was asked whether
   CORR-LO is a vol target in disguise. It is not: the two gates share 0.533 of their firing days
   but the excess decomposes the opposite way, and the vol-target family that *does* clear 4b
   (HI) overlaps CORR-LO at **Jaccard 0.000**. Nothing here validates the low tail.
10. **Survivorship.** U56 is a current-constituent list, so the CAGR and drawdown levels above are
    optimistic; the comparands share the bias, the matched contrasts do not. **No RULES change is
    proposed** — rule 6 reserves that for Sunday review, and this memo exists so the number is on
    the record, not so it is promoted.
