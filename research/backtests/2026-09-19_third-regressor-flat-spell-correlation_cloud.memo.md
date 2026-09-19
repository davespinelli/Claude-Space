# KEEP-4b CANDIDATE MEMO — idea 1558, lane cloud, 2026-09-19 (10 lines). NOT proposed for enactment.

1. **CELL.** `L_M blend None|200 @ lambda = 0.50` on **B136** (and, as hindsight, on U56) — the
   frozen 2026-09-04 incumbent (N = 20, H = 126, gross 0.75, MAXVOL 0.60, 200d MA gate, weekly
   Fri-decide / Mon-trade, 10 bps, t+1) blended 50:50 with its own SPY-200d-gated twin. Both
   sleeves share ONE selection frame, so the blend is a **two-state gross** — 0.75 above SPY's 200d
   MA, **0.375** below — and not a two-book portfolio. Idea 1538 verified that identity as its gate
   G12 (max |dSharpe| 0.0002 as a single book) on this same construction at lambda 0.75.
2. **WHAT IS NEW HERE, AND WHAT IS NOT.** Nothing about the DEVICE is new: this is idea 1538's
   Clause M one lambda deeper (low-state gross 0.375 instead of 0.5625). What is new is that at
   lambda 0.50 the cell clears 4b on **B136** on both windows while the frozen anchor **fails both**
   — so the candidate is not U56-only.
3. **REACHED BY.** On B136, ARGMAX-IS-Sharpe restricted to the three flat-bearing ladders, fitted on
   warm-up..2016-12-31 ONLY (IS Sharpe **1.1651** vs the anchor's 1.1391); 2017-2026 read ONCE.
4. **B136 FULL SAMPLE.** CAGR 14.23% / Sharpe **1.0798** / MaxDD **-16.73%**, halves 1.3276 /
   0.8824. Frozen anchor: 16.06% / 1.0654 / -20.74%, halves 1.2815 / 0.8968. **4b PASS on all four
   legs, where the anchor FAILS the DD leg** (cap -20.23%).
5. **B136 OOS 2017-2026.** CAGR 14.29% / Sharpe **1.0250** / MaxDD **-16.73%**. Anchor OOS 16.19% /
   1.0180 / -20.74%; SPY OOS 15.26% / 0.8738 / -33.72%; RULES v2 OOS 7.85% / 1.1019 / -12.24%.
   **4b PASS.** Turnover 4.00x/yr, charged at 10 bps.
6. **U56, SAME CELL.** FULL 13.99% / **1.1828** / **-17.01%** (halves 1.2114 / 1.1654) and OOS
   15.58% / **1.2438** / -17.01%, both 4b PASS, beating the frozen anchor (15.80%/1.1537/-19.13%;
   OOS 17.32%/1.1857/-19.13%) on both Sharpes with 2.12 pp less drawdown.
7. **HONEST LIMIT (i) — the U56 cell is HINDSIGHT.** Its IS Sharpe is **1.1042, BELOW the anchor's
   1.1158**, so no IS-only chooser in this run reaches it on U56. Only the B136 reading is rule-8
   clean, and the chooser that reaches it restricts the pool to the three flat ladders (it reads no
   OOS row, but the restriction is itself a choice).
8. **HONEST LIMIT (ii) — not significant.** OOS dSharpe against the frozen anchor is **+0.0071,
   t = +0.10** on B136 and **+0.0581, t = +0.74** on U56 (paired circular-block bootstrap, L = 63,
   400 reps). **Path 4a is FALSE at all 189 cells** (0 full, 0 OOS), and on SMALL the cell fails 4b
   on both windows (0.5105 full / 0.4058 OOS).
9. **SURVIVORSHIP (rule 9).** U56 and B136 are CURRENT-constituent lists carried back to 2008, so
   every level above is an UPPER BOUND; what survives the bias is the CONTRAST against the
   incumbent over the same names on the same days.
10. **EXACT RULES WORDING, if the Sunday review (PROTOCOL rule 6) ever enacts it.** Identical to
    idea 1538's Clause M except for the low-state number, so the two must be raced, not stacked:
    > **Clause M (macro de-gross).** Let `MKT_t` be TRUE when SPY's close on the prior trading day
    > is above its own 200-day simple moving average, and FALSE otherwise (FALSE before 200 closes
    > exist). At each weekly rebalance, after the book's names and equal weights are fixed by the
    > standing clauses, set total gross to **0.75 when `MKT_t` is TRUE and to 0.375 when `MKT_t` is
    > FALSE**. The de-grossed weight goes to CASH and is never re-spread. Names, ranking, the
    > per-name 200d MA gate and the MAXVOL ceiling are unchanged.
