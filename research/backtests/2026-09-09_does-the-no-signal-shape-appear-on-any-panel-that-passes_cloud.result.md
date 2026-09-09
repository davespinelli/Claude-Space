# Idea 283 — does the no-signal shape appear on any panel that passes? (cloud, 2026-09-09)

**KILL of the saturation diagnostic as a screening column — and it fails in the WRONG DIRECTION.**
The question was whether the arms that clear 4b are exactly the ones whose band-recovery curve
saturates. They are not; on the published grid they are exactly the ones whose curve does NOT.

**Part A, the literal back-fill (idea 61's 168 published BAND arms over 24 cells, no re-run).**
R = (CAGR(0.20) − CAGR(0.03)) / (CAGR(0.03) − CAGR(0.00)). Only 2 of 24 cells saturate at the
pre-registered bar R ≤ 1 (both U56 / ew-all / dg) and **neither contains a 4b passer. All 28
published 4b-passing BAND arms sit in NO-SIGNAL cells** (R 3.87 to 22.41). Contingency at
R* ∈ {0.25, 0.5, 1.0}: precision 0.000, recall 0.000, phi −0.135 (arm level) and −0.174 (cell
level); at R* = 2 phi −0.287. **AUC of R for a 4b pass 0.260** — the diagnostic separates, with
the sign reversed: high R (the "gate loses on every crossing" shape) is what predicts a pass.

**Part B, the independent replication (432 fresh arms: 3 panels × 3 books × 2 conventions × 3
rungs × 8 band widths, against 27 ungated controls).** Same answer, weaker: at R* ≤ 1 precision
0.179 against a base rate of 0.164 (phi +0.023 — nothing), **AUC 0.401**, still the wrong side of
0.5. Cells split NO-SIGNAL 24 / NO-RECOVERY 16 / SATURATES 14, and 4b passers appear in all three
classes (8 / 2 / 3 cells).

**Why it inverts (mechanism, not a fudge).** On these panels 4b binds on the CAGR floor (70% of
SPY = 10.63% on U56, 10.66% on B136). The band's recovery IS the CAGR the gate gave up: a cell
whose curve is still rising at b = 0.20 is one still climbing toward the floor. The diagnostic
and the 4b bar read the same CAGR increment with opposite signs, so a saturated curve means the
gate's damage is small AND permanent — the arm sits wherever the gate left it. Idea 60 read
non-saturation as evidence of no signal; that reading is right about the GATE and says nothing
about whether the BOOK clears 4b.

**The diagnostic is not even construction-stable.** U56 / top20 / dg at 10 bps is R = **+8.68**
on idea 61's grid and **−5.09** on this one, while both harnesses agree the cell passes 4b (5 of
7 arms there, 7 of 8 here). The cause is what "de-gross" means: idea 61 ranks its top-20 WITHIN
the gated set, so widening the band admits new names; the price-list convention used here ranks
on the ungated book and zeroes gated-out names, so widening restores the ungated top-20. Two
defensible conventions, opposite signs of inc2, same 4b verdict.

**Rule 8 (i), band chosen per cell on IS 2009-2016 Sharpe, 2017-2026 read once at 10 bps:** the
IS-chosen band beats SPY's OOS Sharpe in 9 of 18 cells and the live RULES v2 book in 5 of 18;
b* = 0.20 in 5 cells and 0.00 in 2. **Rule 8 (ii), the diagnostic itself walked forward:** R
recomputed from IS-only CAGRs is a *stable measurement* (Spearman 0.923 with the full-sample R
over the 28 cells where both are defined) and still does not screen — AUC **0.322** for an
OOS-only 4b-style pass, precision 0.208 against a 0.178 base rate, phi +0.042. So the failure is
not sampling noise in R. R is reproducible and simply uninformative about 4b.

**KEEP paths at 10 bps: 4a 0/144, 4b 25/144** (U56 20, B136 5, SMALL439 0). Every passer is a
top-20-plus-band or EWall-plus-band book already in the record. **Idea 61's PARKed by-product
replicates: U56 / EWall / rw / b = 0.12 gives 14.00% / 1.2250 / −19.42%, halves 1.265/1.199, OOS
1.2637** — 4b on every leg, still short of the live book's 1.2817 OOS Sharpe and 7.4 pp deeper in
drawdown, so it stays a PARK, not a KEEP. Idea 60's SMALL439 reading also replicates: the curve
never saturates there (R 3.63 dg / 3.21 rw at 10 bps) and 0 of 48 small-panel arms clear 4b.

**No RULES change, no new book, no KEEP candidate.** The saturation ratio should not be added to
the leaderboard as a screening column; if it is published at all it belongs beside the gate's own
damage, as a description of the gate, never as a predictor of the book.

SURVIVORSHIP: universe.json / universe_broad.json are current-constituent lists; SMALL439 is a
current screen with the 44 max_1d_move ≥ 1.0 names dropped. Levels are optimistic; R is a ratio
of two same-cell, same-days CAGR increments.

Files: `..._cloud.py`, `.console.txt`, `.partA.csv` (24 published cells), `.grid.csv` (432 arms),
`.curves.csv` (54 cells), `.walkforward.csv` (18 cells), `.walkdiag.csv`.
