# Idea 528 — how-many-DRAWS-does-a-PASS-RATE-CURVE-need-before-MONOTONICITY-is-testable (cloud, 2026-09-12)

**ANSWERED = IT DEPENDS ON ONE THING THE RECORD NEVER STATES, AND IT IS NOT THE DRAW COUNT.
A PAIRED sweep (the same books priced at every rung) needs D = 5. An INDEPENDENT sweep (fresh
books per rung, which is what a binomial standard error assumes) needs D = 80 on a 7-rung ladder
and D = 10 on a 4-rung ladder. KILL as a capital idea; no KEEP claimed, no memo, no book promoted,
no PROTOCOL edit applied (rule 6); RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.**

Three earlier cloud runs skipped this idea for having no price leg. This run gives it one: instead
of bootstrapping committed markdown rows it rebuilds the object — **3,360 real books** (160 random
k=20 equal-weight draws x 7 gross rungs x 3 panels), each priced through the engine at 10 bps, t+1,
weekly, seed 528. Params: DRAWS D ∈ {5,10,20,40,80,160} and RUNG SET (FINE 7 / COARSE 4); 72
bootstrap cells x 6 D-rungs, all reported. Resampling mode and panel are REPORTED, NEVER SELECTED.
SURVIVORSHIP: B136 and SMALL664 are current constituents only; SMALL664 = small panel minus the 52
tickers with `max_1d_move >= 1.0`; eligible pools (>=90% coverage) 51 / 124 / 394 names.

## GATES — 4 of 4 PASS
G1 engine vs runner max|dret| **2.776e-17** (bar 1e-12) · G2 max gross **1.000000** · G3
determinism · G4 the N=160 reference curve is monotone with **0 wrong-way steps in all 6
(panel, leg) FULL cells**, so both single legs are usable monotone nulls.

## THE MECHANISM (SECTION 1b) — the result behind the result
**100.00% of books have a monotone pass vector** along the gross ladder for `leg_cagr` (increasing)
and `leg_dd` (decreasing), on all three panels and all three windows. A paired subsample of
monotone books cannot produce a wrong-way step *at any D* — which is why the paired wrong-way rate
is **0.000 at D=5**, and why D* is 5 wherever books are re-used. The conjunction is different: only
**0.4875–0.8500** of books have a monotone **4b** vector on U56/B136 (1.0000 on SMALL664, where
nothing passes). **Non-monotonicity in a paired 4b pass-rate curve is therefore a real object (the
gross window), not resolution — but non-monotonicity in an independent one, at 20 draws, is noise.**

## THE NUMBERS
| | max D* (FINE, 7 rungs) | max D* (COARSE, 4 rungs) | worst P(>=1 wrong-way step) at idea 285's D=20 |
|---|---|---|---|
| PAIRED | **5** | **5** | **0.000** |
| INDEPENDENT | **80** | **10** | **0.260** |

Independent-mode detail, FULL window: U56 `leg_cagr` D*=40 (P20 0.076), SMALL664 `leg_cagr` D*=80
(P20 0.134), everything else D*=5. Reference curves are in `.curves.csv`; e.g. U56 `leg_cagr`
0.0000/0.0000/0.0125/0.4125/0.8688/0.9625/1.0000 over gross 0.25→1.00.

## PRE-REGISTERED HYPOTHESES — 3 of 5 PASS
- **H_20 FAILS** (worst-leg P20 = 0.076 U56, **0.002 B136**, 0.134 SMALL664): idea 285's 20 draws
  is inadequate on two panels and adequate on the third, so "20 is too few" is a panel-dependent
  statement, not a universal one.
- **H_D PASSES** — D* is reached on the ladder in 12 of 12 FULL cells.
- **H_PAIR PASSES, 216 of 216** (cell, D) comparisons: pairing is never worse and often free.
- **H_COARSE PASSES, 36 of 36**: D*(COARSE) <= D*(FINE) everywhere — halving the ladder buys 8x the
  draws (80 → 10 in independent mode).
- **H_OOS FAILS, 22 of 23** (rule 8): the IS-calibrated D* clears the 1-in-20 bar out of sample
  everywhere except **SMALL664/COARSE/cagr/INDEPENDENT (D*_IS = 5 → P_OOS = 0.069)**. The small
  panel's CAGR-leg curve is much flatter OOS (0.0000/0.0000/0.0125/0.0750/0.2313/0.5000/0.6312)
  than IS (0.0000/0.0187/0.3937/0.7312/0.9437/0.9750/0.9938), so a D calibrated in sample is not
  automatically enough out of sample.

## THE PRICE LEG (rule 8, OOS 2017-01-01 … 2026-09-11)
3,360 books, both KEEP paths at 10 bps: **4b passes 80/1,120 (U56), 39/1,120 (B136), 0/1,120
(SMALL664); 4a passes 0 / 41 / 33.** The 4b pass rate against gross is a hump peaking at
**g = 0.625** (U56 51/160, B136 27/160) and falling to 0 at both ends — idea 670/677's gross window,
reproduced here on random books. Best single draw, B136 #117 at g=0.50: full CAGR +11.08%, Sharpe
1.278, MaxDD −16.86%; OOS +11.47% / 1.262 / −16.86% vs SPY OOS +15.33% / 0.877 / −33.72%.
**No KEEP is claimed from it**: it is the best of 1,120 unselected coin flips on one panel, which
is exactly the multiplicity the record's own idea 680 warns about, and 0 of 1,120 small-cap books
clear 4b at any gross.

## WHAT THIS BUYS THE RECORD
Any future admissibility claim on a pass-rate ladder must state **whether the rungs share their
draws**. Paired: 5 draws per rung suffices. Independent: 80 at 7 rungs, 10 at 4. And a wrong-way
step in a paired single-leg curve is impossible by construction — if one is published, the bug is
in the sweep, not the sample.
