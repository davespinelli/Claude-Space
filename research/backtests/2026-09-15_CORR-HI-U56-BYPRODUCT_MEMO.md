# By-product memo — U56 CORR-HI de-grossing gate (idea 815, 2026-09-15). NOT PROPOSED.

1. **What it is.** Hold the RULES-v1-eligible equal-weight book at gross 1.00; de-gross to cash
   entirely on days when 20d average pairwise correlation is in its top 17% over a rolling 504d
   window. Daily cadence, 10 bps, t+1. U56 panel.
2. **Full sample (2009-02→2026-09):** CAGR **14.04%**, Sharpe **1.240**, MaxDD **−15.93%**,
   halves 1.169 / 1.310.
3. **Out of sample (rule 8, (q,w) chosen on 2009-2016 IS Sharpe only, read on 2017+ once):**
   CAGR **15.66%**, Sharpe **1.402**, MaxDD **−11.31%**.
4. **Comparands:** SPY 15.13% / 0.885 / −33.72% (H 0.959/0.824; OOS 15.27% / 0.874);
   RULES v2 (live) 8.64% / 1.208 / −11.90% (H 1.237/1.186; OOS 1.286).
5. **PROTOCOL path 4b:** PASSES — Sharpe > SPY in both halves and OOS; MaxDD −15.93% inside the
   −20.23% cap (60% of SPY); CAGR 14.04% above the 10.59% floor (70% of SPY). Holds at 0, 10 and
   25 bps. **Path 4a FAILS** (MaxDD worse than RULES v2's −11.90%).
6. **Exact RULES wording if it were ever promoted:** *"Clause N (correlation de-gross): compute
   c_t = the 20-day average pairwise correlation of the eligible panel via the equal-weight
   index-vs-name variance identity. Let T_t = the 17th-percentile-from-the-top of c over the
   trailing 504 trading days. If c_t > T_t at the close of day t, hold 100% cash on day t+1;
   otherwise hold the eligible names equal-weight at gross 1.00. Evaluate daily."*
7. **Why it is NOT proposed.** It is the best of **35** rule-8 picks that clear 4b on both
   windows, read off a **3,456-cell** grid built for a different question. That is selection, not
   evidence.
8. **And the run's own headline is against it.** Idea 815 found that CORR-HI's placebo-differenced
   excess (+0.0554 over its BLOCK null) goes to **−0.0062** under an episode-preserving null: the
   family's measured edge over an information-free gate is the 2020/2022 alignment, not the
   signal. 18.6% of this book's de-grossed days sit inside those two episodes.
9. **Replication note.** Its B136 twin (q=0.17, w=252, depth 0.50, daily, g=1.00) reads
   14.04% / 1.156 / −15.04%, OOS 14.30% / 1.210 — reproducing idea 606's committed by-product
   (14.02% / 1.154 / −15.11%, OOS 14.29% / 1.208) on a different tape vintage.
10. **Survivorship.** U56 is a current-constituent list; the CAGR and drawdown levels are
    optimistic, and the binding drawdown is 2020 — the same episode point 8 is about. Status:
    **PARK**, pending a clean pre-registered run on a panel whose 4b bar is not a single episode.
