# Memo — idea 871 lane B by-product: a 4b KEEP-CANDIDATE (BREADTH-HI de-gross, U56). NOT PROPOSED.

1. **What it is.** Hold the RULES-v2-eligible equal-weight book at gross 1.00, and de-gross it to
   CASH entirely whenever market breadth is in its top 12% over a trailing 2016-day window.
2. **Exact RULES wording if ever adopted (rule 6 — Sunday review decides, nothing is changed here):**
   *"Clause 3 (breadth de-gross). Let BREADTH_t be the share of priced instruments above their own
   200-day average. Let T_t be the 88th percentile of BREADTH over the trailing 2016 trading days
   (undefined until 504 closes exist; treat as not-firing). At each weekly rebalance, if
   BREADTH_t > T_t, hold 0% gross (all cash) for the coming week; otherwise hold the clause-2 book
   at 100% gross. Two parameters, q = 0.12 and w = 2016; no others."*
3. **Numbers, U56, 10 bps, weekly, next-day execution.** CAGR **14.18%**, Sharpe **1.123**,
   MaxDD **−19.91%**, halves **1.144 / 1.107**. SPY 15.13% / 0.885 / −33.72%, halves 0.959 / 0.824.
   RULES v2 live 8.64% / 1.208 / −11.90%.
4. **Rule 8.** Parameters chosen on 2009–2016 by IS Sharpe alone over all 1,152 U56 arms; read
   untouched on 2017–2026: OOS CAGR **14.81%**, Sharpe **1.150**, MaxDD **−19.91%** (SPY OOS
   15.27% / 0.874 / −33.72%; RULES v2 OOS 9.49% / 1.286 / −11.90%).
5. **Path.** **4b PASS** on all five legs — H1 1.144 > 0.959, H2 1.107 > 0.824, OOS 1.150 > 0.874,
   MaxDD −19.91% inside the −20.23% cap (0.6 × SPY), CAGR 14.18% above the 10.59% floor (0.7 × SPY).
   **4a FAILS**: it is below RULES v2's Sharpe in both halves and runs 8 pp more drawdown.
6. **Cost sensitivity.** Sharpe 1.242 at 0 bps, 1.123 at 10 bps, 0.944 at 25 bps. It fires on
   14.18% of days in 41 runs averaging 15.4 days, so it is a low-turnover clause, not a trader.
7. **Why it is NOT proposed.** The DD-cap margin is 0.32 pp. 239 of this panel's 1,152 arms
   (20.7%) also pass 4b, so passing is the base rate of this grid, not a distinction; on B136 the
   same family's IS-pick fails 4b outright (H2 0.660) and on SMALL nothing passes at all.
8. **The sharper objection.** BREADTH-HI has the SMALLEST placebo excess of the eight families
   measured in this very run (+0.0128 against an information-free BLOCK null, share>0 0.592). The
   arm the IS selector likes is drawn from the family with almost no edge over a matched coin flip,
   which reproduces idea 815's finding that the statistic and the 4b bar are decoupled.
9. **Standing objections that also apply.** Idea 787 killed the record's whole standing 4b shelf
   (0 of 82) against an equal-weight basket of the book's own panel; that bar has not been run here.
   SURVIVORSHIP: U56 is a current-constituent list, so the CAGR and drawdown LEVELS are optimistic.
   The binding drawdown is 2020 and the window is a QQQ-favourable regime.
10. **Recommendation.** Log it, do not adopt it, and do not put capital behind it. If the Sunday
    review wants it, run it against idea 787's equal-weight bar and idea 502's gross-matched
    coin-flip base rate first; a 0.32 pp DD margin will not survive either.
