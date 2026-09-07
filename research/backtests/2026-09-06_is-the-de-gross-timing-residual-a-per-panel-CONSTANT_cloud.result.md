# Idea 303 — is-the-de-gross-timing-residual-a-per-panel-CONSTANT (cloud, 2026-09-06)

**SPLIT.** A negative constant beats the naive zero and transfers to cells it was never fitted
on (+26.4% pooled OOS MAE, 3/3 panels, 102 of 108 cells). But it is **not per-panel**: a single
GLOBAL constant does as well pooled (MAE 0.4721 vs PANEL's 0.4768) and beats PANEL outright on
SMALL439 (0.4696 vs 0.5601, −19.3%). And the constant is **not constant in time**: every
estimator is biased +0.45 pp/yr because the OOS residual is far more negative than any IS fit.

## Design

The claim under test is idea 297's walk-forward number (IS panel mean beats the zero on OOS MAE
by 17–31%), which was measured **in-corpus** — fitted on the IS half of the same 108 cells it
was then scored on. This run makes the corpus disjoint:

| | cells | window |
|---|---|---|
| FIT | idea 297's 108 cells, bands 0.00/0.02/0.03/0.05/0.08/0.12 | IS ≤ 2016-12-31 |
| TEST | 108 cells at bands 0.01/0.04/0.06/0.10/0.15/0.20 | OOS 2017-01-01+ |

Same 3 panels × 2 gates (MA, MAVOL) × 3 cadences (W/M/Q) × 2 constructions, 75% gross, 10 bps
(0 bps for the decomposition), next-day execution. Overlap on (panel, gate, cadence, band) = 0.
Tuned parameters: band and cadence, reported at every value.

**Validity gates, asserted first.** B0: all **432 of 432** recomputed OLD-band rows reproduce
idea 297's committed `decomp.csv` — max |Δ| c_bar 5.6e-17, gap0 8.9e-16, pred0 8.9e-16, resid0
2.2e-16 (bar 1e-6). P1: the leverage identity max |r_dg,t − c_t·r_rs,t| = **3.5e-17** over all
216 pairs (bar 1e-12).

## The contest — OOS MAE (pp/yr) on the disjoint TEST corpus

| panel | ZERO | GLOBAL | **PANEL** | PANELGATE | CELLIS | ORACLE |
|---|---|---|---|---|---|---|
| SMALL439 | 0.6633 | **0.4696** | 0.5601 | 0.5639 | 0.5079 | 0.3192 |
| U56 | 0.4895 | 0.3517 | **0.3366** | 0.3300 | 0.4993 | 0.2773 |
| B136 | 0.7901 | 0.5950 | **0.5338** | 0.5332 | 0.6376 | 0.3061 |
| POOLED | 0.6477 | **0.4721** | 0.4768 | 0.4757 | 0.5483 | 0.3009 |

Fitted constants (pp/yr): GLOBAL −0.1952; PANEL SMALL439 −0.1032, U56 −0.2251, B136 −0.2572.
Realised TEST-corpus OOS means: SMALL439 −0.6633, U56 −0.4845, B136 −0.7901 (sd 0.35–0.39).

## Pre-registered verdicts

- **H1 HOLDS (3/3).** PANEL beats ZERO on every panel: +15.6% / +31.2% / +32.4%; paired
  cell-by-cell 36/36, 30/36, 36/36 (pooled 102/108, p 1e-21).
- **H2 FAILS (2/3).** PANEL loses to GLOBAL on SMALL439 by 19.3% (paired 0/36, p 3e-11), wins on
  U56 (+4.3%, 27/36) and B136 (+10.3%, 36/36). Pooled, GLOBAL is marginally ahead.
- **H3 HOLDS.** Pooled MAE gain over ZERO +26.4% (bar ≥ 10%).
- **H4 FAILS.** Spearman(fitted constant, realised OOS mean) over the three panels = **+0.50**.
  The fit ranks SMALL439 least negative (−0.103); it realises second (−0.663).

## What the numbers actually say

1. **The discount is real, its per-panel form is not.** All of PANEL's transferable content is
   the shared sign and rough size (~−0.2 pp/yr). Splitting that one number three ways adds
   nothing pooled and actively hurts on the panel whose IS estimate is the outlier.
2. **The estimator's real error is a time shift, not a panel shift.** Bias is +0.45 pp/yr for
   both GLOBAL and PANEL: 2017–2026 residuals are 2–4× more negative than 2009–2016 ones on
   every panel. Sign agreement is 98% but magnitude is systematically short.
3. **Cell noise dominates.** ORACLE — the realised OOS panel mean, unknowable in advance —
   still leaves MAE 0.3009 against PANEL's 0.4768. Two thirds of the achievable error is
   within-panel dispersion no constant of any kind can reach.
4. **CELLIS is the worst usable estimator** (MAE 0.5483, sign agreement 66%), confirming idea
   297's per-cell reading on a corpus it never saw.

## KEEP paths (PROTOCOL requires both on every cell)

216 NEW cells at 10 bps: **4a 0/216**, **4b 20/216** — every passer a U56/B136 RESPREAD narrow-band
MA or MAVOL book, i.e. the already-published band family (ideas 291/298), none of them the
rule-8 pick. Rule-8 walk-forward over 12 arms: 5/12 beat the matched EWall control, 8/12 beat
SPY, **0/12 beat the live RULES v2 book, 0/12 clear 4a, 0/12 clear 4b**. No candidate.

Best 4b cell for the record: U56 / RESPREAD / MA / W / b=0.10 — 13.62% / **1.2309** / −18.19%
(halves 1.2695 / 1.2083, OOS 1.2681, 2.19×/yr turnover) vs SPY 15.23% / 0.8890 / −33.72% and
the live book 8.79% / 1.2141 / −12.05%. It fails 4a on drawdown and is not what rule 8 selects.

## Caveats

SURVIVORSHIP: all three panels are current constituents (no delistings). Every estimator column
is an arm-minus-arm contrast on the same names and days, so the bias largely cancels there; it
does **not** cancel out of the 4a/4b levels.

Script `2026-09-06_is-the-de-gross-timing-residual-a-per-panel-CONSTANT_cloud.py`; console,
`decomp.csv` (864 rows), `estimators.csv`, `paired.csv`, `grid.csv`, `walkforward.csv` committed.
