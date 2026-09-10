# PARK memo — B136 BREADTH-QUANT gate, idea 400 by-product (2026-09-10, cloud)

**PARKED, NOT PROPOSED FOR ADOPTION.**  It is filed because it is a rule-8-selected 4b passer and
the record's convention is to publish those, not because this run recommends it.

1. **The book.**  B136 panel, equal weight across every priced name at gross 1.00/N, weekly, t+1,
   10 bps.  On a day when panel BREADTH (share of names above their own 200d MA) is below the
   trailing 1260-day (min 504) **q = 0.159 quantile of its own history**, the whole book goes to
   CASH; gated weight is never re-spread.  Fires on **12.44% of scored days over 37 episodes**.
2. **Numbers.**  Full 2009-2026: **15.79% CAGR / 1.1630 Sharpe / −20.02% MaxDD**, halves
   **1.2104 / 1.1276**.  OOS 2017-2026 (read once): **14.17% / 1.2583 / −14.80%**.
3. **Comparands.**  B136 RULES v2 8.03% / 1.1058 / −12.24%, OOS Sharpe 1.1185.  B136 SPY 15.23% /
   0.8890 / −33.72%, halves 0.9566 / 0.8340, OOS Sharpe 0.8820.  Ungated EW parent at the same
   gross 18.92% / 1.1220 / −32.72% — it **fails** 4b on the DD cap, so this pass is not inherited.
4. **KEEP path.**  **4b PASS** (H1 1.2104 > 0.9566, H2 1.1276 > 0.8340, OOS 1.2583 > 0.8820,
   MaxDD −20.02% ≥ −20.23%, CAGR 15.79% ≥ 10.66%).  **4a FAIL** on both legs (H1 1.2104 < v2's
   1.2291; MaxDD −20.02% worse than v2's −12.24%).
5. **Rule 8.**  (threshold, gross) chosen on 2009-2016 Sharpe alone; 2017-2026 read once.  It is
   the chooser's own pick for (B136, BREADTH, QUANT), so it is not an in-sample-only winner.
6. **Why PARK and not KEEP — reason 1.**  It clears the 4b drawdown cap by **0.21 pp** (−20.019%
   against −20.234%).  Ideas 527/530/531 established the DD cap as the binding leg of 4b and its
   0.60 constant as the single tuned number in the rule; a 0.21 pp margin is inside that.
7. **Reason 2.**  B136 is a CURRENT-CONSTITUENT list.  Survivorship inflates the CAGR leg this
   book also passes, and the leg is passed with room, so the margin cannot be audited from here.
8. **Reason 3.**  Idea 336 priced this exact family (the causal rolling-quantile re-cut of an
   absolute breadth gate) and found the quantile form **worse** than the absolute form under the
   identical chooser on both large panels, with its whole small-panel advantage bought by not
   firing.  This run reproduces the mechanics, not a new edge.
9. **Exact RULES wording IF a Sunday review ever promoted it** (not proposed here): *"Hold every
   priced instrument at 1.00/N of NAV, rebalanced weekly. On any rebalance day where the share of
   instruments trading above their own 200-day moving average is below the 0.159 quantile of that
   share's own trailing 1260-day history (minimum 504 observations), hold 100% cash instead;
   gated weight goes to cash and is never re-spread."*
10. **What would have to be true first.**  (a) The DD margin survives a 25 bps cost rung and the
    0.60 cap constant being moved to 0.55; (b) the pass replicates on U56, which is
    survivorship-free — it does not today (U56 BREADTH-QUANT's rule-8 pick fails 4b); (c) the
    firing quantile 0.159 is shown to be a plateau, not a point, per idea 407's test.  Until all
    three, this is a PARK.
