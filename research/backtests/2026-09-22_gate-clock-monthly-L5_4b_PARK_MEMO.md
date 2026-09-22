# KEEP-4b candidate — U56 / monthly gate clock L = 5 / c = 0.00 / monthly cadence
**RECORDED AND NOT RECOMMENDED. Idea 2276, lane B, 2026-09-22.
Script `2026-09-22_gate-clock-monthly-cadence_B.py`; row in `.grid.csv` and `.ddcells.csv`.**

1. **The book.** Idea 182's frozen R6 top-20 monthly hypothesis with ONE clause changed: the MA
   membership gate is computed on **monthly bars** with a 5-bar average, not on daily closes with a
   200-day one. Gross 0.75, n = 20 equal weight, vol20 < 0.60 ceiling, 1/vol20^0.5 scaler, monthly
   cadence, next-day execution, 10 bps — every one of those inherited, none tuned here.
2. **The numbers (U56, 10 bps).** FULL **13.16% / 1.1850 / −14.61%** (halves 1.3312 / 1.0616),
   OOS 2017–2026 **13.15% / 1.1434 / −14.61%**, realised turnover 5.38x/yr.
3. **Against the gate it replaces** (idea 182 as it trades, daily 200d, 14.03% / 1.1828 / −18.81%,
   OOS 14.52% / 1.1683): **+4.20 pp of drawdown, +0.0022 of Sharpe, −0.87 pp of CAGR** full sample.
4. **4b is cleared on all five legs.** CAGR **+2.46 pp** over the 10.70% floor, MaxDD **+5.62 pp**
   under the −20.23% cap, Sharpe over SPY **+0.2646** full and **+0.2683** OOS, both halves above
   SPY (1.3312 / 1.0616 vs 1.0703 / 0.8166); OOS margins +2.45 pp and +5.62 pp. 4b path, not 4a.
5. **4a fails**, as it does at 0 of 480 cells on this grid: live RULES v2's −12.05% MaxDD is
   unreachable by any cell of this book, whose shallowest is −13.46%.
6. **Rule 8 cannot reach it — this is why it is PARK and not KEEP.** Dials chosen on 2009–2016
   only: **0 of 4 legal IS-only choosers pick this cell at any cost rung on U56/M**, and at the
   live 10 bps rung all of them pick cells that are WORSE out of sample than the shipped gate
   (C_SHARPE L=13 c=0.05 → OOS 1.1237 / −21.69%; C_4B L=7 c=0.05 → 1.1228 / −21.42%).
7. **Its own OOS Sharpe is worse than the incumbent's**, −0.0249. The drawdown gain is a
   full-sample fact; the Sharpe edge is not repeated out of sample.
8. **It is a ladder EDGE, not a plateau.** L = 5 months is the fastest rung tested and the far end
   from the live gate's 200-day analogue (L = 10); its neighbours L = 7/10/13/16 buy nothing at
   c = 0.00 on U56/M, and the pooled clock effect across the grid is negative (−0.0113 Sharpe).
9. **Survivorship (PROTOCOL rule 9):** U56 is a current-constituent list held from 2008, so the
   13.16% CAGR is optimistic and the 4b floor is easier than it would be on a point-in-time panel.
10. **Proposed RULES wording, recorded for completeness and NOT proposed for adoption** — it would
    replace RULES v2 clause 2 wholesale, since this is a different book from the live one, not a
    tweak: *"**2. Membership gate:** a 5-bar moving average of MONTHLY closes, per name. A name is
    **IN** when its latest monthly close is above that average and **OUT** otherwise; the state is
    set at each month's last close and is not re-read intra-month. A name with fewer than 5 monthly
    closes is OUT."* — together with clause 3 becoming *"hold the top 20 names by R6 / vol20^0.5
    among IN names with vol20 < 0.60"*, clause 4 sizing at `0.75 / 20`, and clause 5 rebalancing on
    the last trading day of each month. **Not adopted: rule 8 does not reach this cell.**
