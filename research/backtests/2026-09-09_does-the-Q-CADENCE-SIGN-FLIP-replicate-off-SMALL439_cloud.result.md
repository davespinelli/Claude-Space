# Idea 550 — does-the-Q-CADENCE-SIGN-FLIP-replicate-off-SMALL439 (cloud, 2026-09-09)

**Verdict: KILL of the premise.** The positive quarterly residual is a SMALL439 fact, it is
phase-locked to the calendar quarter, it is an OOS-half fact (the in-sample sign is negative),
and it is 1.1 bp/yr. Not a cadence property. No KEEP candidate on either path.

Script: `2026-09-09_does-the-Q-CADENCE-SIGN-FLIP-replicate-off-SMALL439_cloud.py`
(1,080 books = 3 panels × 9 θ × 5 cadences × 2 families × 2 constructions, plus the same grid
at a fixed 63-bar cadence × 5 phases; all grid points reported in `.headline.csv`, `.phase.csv`,
`.decomp.csv`, `.grid.csv`, `.walkforward.csv`, `.keeppaths.csv`, `.console.txt`).

## (a) Does the Q sign flip replicate off SMALL439? — NO

QUANTILE-M mean `resid0` (pp/yr) at cadence Q, all 9 θ, FULL window:

| panel | FULL | n_pos | IS | n_pos | OOS | n_pos | mean c_sd |
|---|---|---|---|---|---|---|---|
| U56 | **−0.0422** | 0/9 | −0.0317 | 0/9 | −0.0539 | 1/9 | 0.0074 |
| B136 | **−0.0442** | 0/9 | −0.0375 | 0/9 | −0.0494 | 0/9 | 0.0057 |
| SMALL439 | **+0.0114** | 9/9 | **−0.0237** | 1/9 | +0.0316 | 9/9 | 0.0097 |

U56 and B136 are negative at **every one of the 9 θ** at Q. The flip is SMALL439-only, so idea
307's headline must be stamped as a one-panel result. Note also that the 9/9 is a **FULL-window**
count only: on the in-sample half SMALL439's Q residual is −0.0237 with 1/9 positive. The whole
positive sign lives in the 2017+ half.

## (b) Calendar artefact or 63-bar holding period? — CALENDAR

Same decomposition at a fixed 63-bar cadence (rebalance count within 1 of calendar-Q, G7),
offsets {0, 13, 26, 39, 52}, QUANTILE-M mean `resid0` (pp/yr), FULL window:

| panel | 63bar+0 | +13 | +26 | +39 | +52 | calendar-Q | phases > 0 |
|---|---|---|---|---|---|---|---|
| U56 | −0.0539 | −0.0566 | −0.0585 | −0.0380 | −0.0299 | −0.0422 | 0/5 |
| B136 | −0.0534 | −0.0535 | −0.0601 | −0.0545 | −0.0273 | −0.0442 | 0/5 |
| SMALL439 | −0.0019 | −0.0370 | −0.0175 | −0.0690 | −0.0015 | **+0.0114** | **0/5** |

Zero of the fifteen off-calendar cells is positive. The ~63-bar holding period on its own never
produces the flip; only the quarter-end phase does. (In the OOS half alone SMALL439 turns
positive at 3 of 5 phases too, so the OOS-window phenomenon is not purely calendar — but the
published FULL-window number is.)

## Rule 8 walk-forward — the sign does not survive

Choose the cadence with the largest IS `resid0` per (family, panel); read the untouched OOS half:
**sign held in 0 of 6 cells.** SMALL439/QUANTILE-M picks D (IS +0.0005 → OOS −0.0007);
SMALL439/MA-THRESH picks M (IS +0.1138 → OOS −0.4507). Book-level walk-forward (choose by IS
Sharpe, read OOS): U56 OOS 41.5% / 1.34 / −33.7% (fails 4b on DD), B136 1.2% / 1.06 / −1.7%
(fails on CAGR), SMALL439 24.0% / 1.10 / −30.8% (fails on DD), against RULES v2 live OOS
9.5% / 1.28 / −12.1% and SPY OOS 15.5% / 0.88 / −33.7%.

## Magnitude

+0.0114 pp/yr is **1.1 bp/yr**, against a gap0 of −4.28 pp on the same cells: the residual is
0.27% of the quantity it decomposes, and 60× smaller than the MA-THRESH residual at the same
cadence and panel (−0.6871). Its sd across θ is 0.0043. A sign this size is a rounding fact.

## KEEP paths — none

Of 1,080 books: 5 pass 4a (all U56 QUANTILE-M/DEGROSS, all fail 4b on CAGR), 31 pass 4b (26 U56,
5 B136, **0 SMALL439**, all fail 4a), and **0 pass both**. The 4b fail-leg census is DD 755,
CAGR 537, H2 425, OOS 423, H1 396 — the drawdown cap remains the binding leg, as ideas 500/527
reported. None of the walk-forward picks passes 4b.

## Gates

G1 PASS (engine equivalence 0.0e0), G2 PASS (DEGROSS identity 6.7e−16), G3 PASS (idea 307
reproduces, 270/270 cells, worst |Δresid0| 2.2e−16), G4 PASS (idea 551 reproduces, 810/810,
2.2e−16), G7 PASS (rebalance-count parity, worst |Δ| = 1).
**G5 FAIL** (matching, worst |frac_q − frac_ma| = 0.01396 vs bar 0.01) and **G6 FAIL** (live
RULES v2 reads 8.64%/1.2037/−12.05% vs published 8.66%/1.2056/−12.05%) — both reproduce idea
551's failures to the digit and are pre-existing vintage/matching conditions of the current
caches, not this script; G3/G4 passing at 2e−16 is the evidence.

## Survivorship

SMALL439 and B136 are current constituents (`data/SMALL_PANEL_README.md`); 44 tickers with
`max_1d_move ≥ 1.0` were dropped before use. `resid0` is a difference of two books on the same
names, so the bias very largely cancels out of it; every CAGR/Sharpe/MaxDD/KEEP column above is
optimistic and is reported for completeness only.
