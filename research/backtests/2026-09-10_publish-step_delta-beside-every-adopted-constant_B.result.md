# Idea 408R — publish step_delta beside every adopted constant (lane B, 2026-09-10) — SPLIT

**Filed as an INDEPENDENT CONCURRENT REPLICATION (record convention 320R).** A cloud run answered
idea 408 while this one was in flight; the two were written independently and agree on the
headline (step_delta is not density-free; the unit must be margin per unit of dial). Points 1, 2,
4 and 6 below are new here. Cross-check of their PARKed 4b candidate at the end.

**Not a KEEP.** 4a 0/273, 4b 9/273 at 10 bps, both paths 0/273. Nothing is promoted; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are untouched. What follows is a **report-only
proposal for the Sunday review**, in the exact wording it would take.

1. **The back-fill idea 408 asks for cannot be done.** Of 572 committed KEEP rows, **0 (0.0%)**
   can supply all three columns from the row itself and **8 (1.4%)** from the row plus its
   sidecar CSVs; only 58.9% of KEEP rows have a sidecar CSV at all. The proposal is prospective.
2. **BAR is not well-defined without a scale — idea 408's premise, confirmed in its strongest
   form.** The binding bar read as argmin over raw margins and as argmin over margin/step
   **disagree on 41.3% of 150 points**. Publishing BAR alone publishes an artefact of mixing
   Sharpe units with return units in one `min`.
3. **STEP as published is a property of the grid, not of the dial.** Halving every spacing moves
   step_delta by a median factor **1.94** and flips the THIN verdict on **4.4%** of points;
   `UNIT_STEP` (margin per unit of the dial) is invariant at **1.00**.
4. **STEP does not earn a third column at the protocol rung.** Predicting a real neighbour flip:
   AUC 0.861 (margin/step) vs **0.863 (margin alone)**, delta **−0.002** at 10 bps. It only pays
   at 0 bps (+0.071). Rule 8: it changes **0 of 27** walk-forward picks at tau=1, 3 of 27 at tau=2.
5. **PROTOCOL clause proposed (report-only, no verdict may turn on it):** *every LEADERBOARD row
   whose verdict rests on a swept constant must publish two columns — the BINDING BAR and its
   MARGIN — and, where a sweep is published, MARGIN PER UNIT OF THE DIAL (not per grid step).
   The binding bar must be the argmin of the step-normalised margins, not of the raw ones.*
6. **Cross-check of the same-day cloud run's PART E 4b candidate (RULES v2 at gross 1.00, U56).**
   It reproduces here exactly — 11.5791% / 1.2090 / −15.70% / H 1.2365/1.1878 — and idea 408's own
   statistic prices it: binding bar **CAGR +0.0097 = +1.67 grid steps** on the record's published
   gross grid (step 0.05; STEP 0.00580, UNIT_STEP 0.11606); the 4b window is `gross ≥ 0.95`, a pass
   at the top edge with no interior optimum. Two conventions move it: warm-up index[260]→[300] cuts
   the margin **4.8× to +0.0020**, and the record's own adopted vol cap 0.60 **flips its sign
   (−0.0021) at their own start**. That is the input this proposal was meant to produce; it argues
   for PARK, not adoption. Cheapest back-fill today: the 8 KEEP rows that already carry all three
   columns, plus idea 401's six adopted constants.
