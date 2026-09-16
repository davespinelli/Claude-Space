# Idea 1047 (cloud, 2026-09-16) — proposed PROTOCOL clause: NULL FLOORS ARE QUOTED AS A CELL p95

1. **Verdict.** KILL the global `0.012` dispersion-floor bar; KILL the queue's premise that the
   bar can be restated per cell on the same statistic. KEEP the clause below (proposed, NOT
   applied — PROTOCOL rule 6 reserves rule changes to a Sunday review).
2. **Why.** `sqrt(max(D2_hat, 0))` sits ON its own truncation point: only 0.462–0.552 of reps
   give a positive intercept, so the median reads exactly 0.0000 in 55 of 192 cells and ~0.03 in
   the rest. Its value is a coin flip, not a bias with a scaling law.
3. `D2_hat` is in fact slightly **negative** (mean −0.000176..−0.001154, t −0.43..−2.69 in the
   six headline cells): on nested tail windows `sd²` falls a little faster than `C/L`.
4. **Exact wording proposed for PROTOCOL rule 8 (append):** "Any dispersion floor, sd floor or
   `D` reported off a fitted `sd² = D² + C/L` curve must be quoted as the **p95 of its own
   cell's zero-dispersion null**, together with that cell's `(pool size N, tape length T, ladder
   rungs, panel, cost rung)`. A point estimate of such a floor is not a finding; a global
   threshold across cells is not admissible."
5. **What the clause costs.** Per-cell p95 at the record's own cells: U56 0.1165 (10 bps) /
   0.1163 (25 bps), B136 0.1237 / 0.1239 — about **10x** the retired 0.012 bar.
6. **What it changes.** Of 1044's 24 committed floors, 8 clear the global 0.012 and **0** clear
   their own cell's p95; 8 of 24 verdicts move. Every dispersion floor in the record is noise.
7. **The queue's either/or, answered on the only statistic that resolves it** (section B2,
   reported, NOT pre-registered): **TAPE LENGTH**, slope −0.566 on the shape-held-fixed ladder
   against an a-priori −0.50. Pool size over the record's three real pools: −0.040, flat.
8. **Pool size cannot be bought.** Independent-idio N ladder reaches only −0.197; with the
   pool's real cross-book idio correlation it collapses to +0.090. A band × gross ladder is
   near-collinear, so nominal N ≫ effective N.
9. **Rule 8 (2016-12-31 split, OOS read once).** Best pick U56 `qroll-q0.17-w1008-d0.50`:
   OOS 15.60% / 1.293 / −15.59% vs RULES v2 9.45% / 1.276 / −12.05% and SPY 15.21% / 0.871 /
   −33.72%. OOS 4b 36/36, 4a 0/36. Pool has no OOS effect (mean OOS Sharpe 1.133 / 1.115 /
   1.117 for GRID / SHELF / WIDE). **SURVIVORSHIP:** U56/B136 are current-constituent panels,
   so every CAGR and drawdown level here is optimistic and the 4b counts are an upper bound.
10. Gates 10 of 10; hypotheses 1 of 6, and four of the five failures are the same failure —
    every bar was pre-registered on the median floor, which the run then showed cannot resolve
    anything. Reported as written, not re-scored. Script:
    `2026-09-16_is-the-0.012-FLOOR-BIAS-a-TAPE-LENGTH-object-or-a-POOL-SIZE-object_cloud.py`.
