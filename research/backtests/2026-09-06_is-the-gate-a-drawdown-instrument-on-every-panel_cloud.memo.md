# MEMO to the Sunday review — `EWall + vol60-dg` re-confirmed under matched gross (4b), and the band's panel limit

1. **What passes 4b here.** `EWall + vol60-dg` — equal-weight every panel name whose 20-day
   annualised vol is below 0.60, gross 75%, weekly, excluded names in CASH — clears 4b on the
   **full sample AND the rule-8 OOS window, on U56 and B136, at 10 and 25 bps** (4 of the 13
   surviving cells). U56 @10bps: **12.08% / 1.1333 / −17.56%**, halves 1.156/1.113, **OOS 12.59% /
   1.1858 / −17.44%**, turnover **1.44×/yr**; B136 @10bps: 12.83% / 1.1400 / −19.34%, halves
   1.258/1.028, OOS 12.43% / 1.1240. SPY: 15.23% / 0.8890 / −33.72% (OOS 15.45% / 0.8820 / −33.72%).
2. **This is a third independent re-confirmation**, not a new candidate: idea 94's lane-B memo
   proposed the same book, and it survives here on a different harness that additionally matches
   realised gross and adds the OOS 4b legs the earlier run did not compute.
3. **`ddctl8` (book DD > 8% → halve) passes the same four cells** at even lower turnover
   (1.25–1.28×/yr), U56 OOS 13.52% / 1.1852. It is a genuine alternative, not a runner-up.
4. **The live band passes 4b on U56 only** (11.59% / 1.2054 / −15.91%, OOS 12.78% / 1.2844) and
   fails B136's CAGR floor. It is the highest-Sharpe arm on the board, and the narrowest.
5. **The blocker, unchanged from idea 94: 0.60 is inherited from RULES v1** and has never been
   re-derived. Queued idea 95 owns that sweep. Do not adopt before it reports.
6. **Second blocker, new here: every 4b pass sits on the top gross rung.** At G = 0.40/0.50/0.60
   all four instruments fail 4b's CAGR floor (128 of 144 treated cells). The pass is as much a
   statement about gross as about the gate — idea 274's knife-edge finding, reproduced.
7. **Third: a gate is not an exposure dial.** At G=0.75 band3/g200/abs12/v1gate cannot reach the
   target gross at m=1.0 (band3 tops out at realised 0.7102 on U56). 40 of 168 cells are
   unpriceable for that reason. vol60 and ddctl8 reach every rung; the trend gates do not.
8. **Selection is weak.** Rule 8's IS chooser picks the OOS-cheapest instrument in 8 of 24 cells;
   mean Spearman(IS, OOS price) is +0.267 and is *negative* on SMALL439. Any price list this
   project publishes should carry that number beside it.
9. **Proposed RULES wording (adoptable only if idea 95 confirms 0.60):**
   > *Eligibility.* A name is eligible in week t if its 20-day annualised volatility, measured at
   > the close of the last trading day of week t−1, is below 0.60. No trend filter is applied.
   > *Sizing.* Hold every eligible name at equal weight, total gross 75% of NAV; the weight of any
   > excluded name is held in cash and is never redistributed. *Cadence.* Decide at the weekly
   > close, execute at the next close.
10. **Proposed RULES wording, instrument-choice clause (adoptable now, it is a measurement):**
    > *Drawdown instruments.* When a drawdown budget is set, the instrument is chosen per panel,
    > not globally: the 200-day band is the cheapest instrument on universe.json only; on the
    > broad list the volatility gate is cheaper at every gross level and both cost rungs, and on
    > the sub-$2B panel the book-level drawdown control is. No instrument may be quoted at a gross
    > level it cannot reach at m = 1.0.
