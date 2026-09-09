# Idea 301 — is-the-gate-timing-residual-a-constant-in-pp-per-year (lane B, 2026-09-09)

**ANSWERED / KILL of the per-panel form; the constant exists but its unit is the GATE FAMILY, not the panel, and it is not actionable.**

Script: `2026-09-09_is-the-gate-timing-residual-a-constant-in-pp-per-year_B.py`
Outputs: `.grid.csv` (324 books) `.decomp.csv` (486 cell×window rows) `.estimator.csv` (245 estimator scores) `.walkforward.csv` `.console.txt`

Idea 298 killed the `share ~ c_bar` discount curve and replaced it with a **zero-parameter prescription**: *"subtract the gate's own timing residual (~0.0 pp/yr for a pure-exposure gate, 0.3–0.6 pp/yr for an MA gate), independent of c_bar."* That is a constancy claim resting on one **in-sample** intercept per panel (−0.619 / −0.267 / −0.352 pp, t −5.43/−3.16/−3.96, R² 0.04–0.19), never tested out of sample. This run tests it, and answers the queue's own head-to-head.

Grid **imported verbatim** from idea 298 (3 panels × 2 gate families × 9 strictness levels × 3 cadences = 162 decomposition cells / 324 books); `gate_mask`/`book`/`control_book`/`stat` are idea 298's code unchanged. Two tuned dials, reported at every point, selected at none outside rule 8: **POOLING LEVEL** (7: ZERO, GLOBAL, FAMILY, PANEL, PANELxFAM, CELL, CBAR-OLS) × **SHRINKAGE λ** toward the global IS mean (5: 0.00…1.00) = 35 estimator cells. IS ≤ 2016-12-31, OOS ≥ 2017-01-01. 10 bps, gross 0.75, next-day execution; the 0-bps rung is derived exactly (`r0 = r10 + turnover*bps/1e4`), never re-run.

---

## B3 REPRODUCTION GATE — **FAIL as written, 100% of it on U56**

Asserted before any new number was read, against idea 298's committed `.decomp.csv`, all 486 rows matched:

| panel | max \|Δresid0\| | max \|Δgap0\| | max \|Δpred0\| | max \|Δc_bar\| |
|---|---|---|---|---|
| SMALL439 | **0.00000000** | 0.00000000 | 0.00000000 | 0.00000000 |
| B136 | **0.00000000** | 0.00000000 | 0.00000000 | 0.00000000 |
| U56 | **0.01287497** | 0.53582014 | 0.52294518 | 0.00004218 |

Bar was `< 1e-2 pp`; the run misses it at **1.287e-02 pp**, on U56 only. 324 of 486 rows reproduce **exactly**. The bar is **not moved** — it fails. The cause is the known drift of `data/prices.csv` since 2026-09-06 (ideas 513, 515): `Δc_bar` is 4.2e-05 while `Δgap0` is 0.536 pp, i.e. the panel's *returns* moved, not the gate. Idea 515's proposed `|dSharpe| < 1e-3` bar would not save this either — the drift is 0.54 pp of CAGR. Every headline below is therefore **restated (B3b) on SMALL439 + B136 only**, the 108 cells that reproduce at 0.000e+00, and every conclusion survives that restatement.
Identity check re-asserted: `max |r_dg,t − c_t·r_rs,t| = 5.551e-17` over 486 cells (holds at 1e-12).

## B1 CONSTANCY — passes as written, and the bar is carried by a degenerate family

| panel | family | IS mean | IS sd | OOS mean | OOS sd | drift | IS slope t | OOS slope t | ρ(IS,OOS) |
|---|---|---|---|---|---|---|---|---|---|
| B136 | MA-THRESH | −0.2864 | 0.3261 | −0.5287 | 0.3737 | **−0.2423** | +2.93 | −0.36 | 0.489 |
| SMALL439 | MA-THRESH | −0.0201 | 0.2656 | −0.5918 | 0.4079 | **−0.5717** | −0.68 | −2.44 | 0.434 |
| U56 | MA-THRESH | −0.3162 | 0.3636 | −0.3377 | 0.3155 | −0.0216 | +0.88 | +0.47 | 0.542 |
| B136 | QUANTILE | −0.0401 | 0.0255 | −0.0454 | 0.0358 | −0.0053 | +2.83 | +3.57 | 0.903 |
| SMALL439 | QUANTILE | −0.0316 | 0.0278 | +0.0076 | 0.0295 | +0.0392 | +2.76 | +1.23 | 0.715 |
| U56 | QUANTILE | −0.0320 | 0.0288 | −0.0432 | 0.0390 | −0.0113 | +3.98 | +3.81 | 0.916 |

- **B1a PASS** — MA-THRESH OOS MAE: PANELxFAM 0.3900 < ZERO 0.4903 pp (on all 162: 0.2123 < 0.2641).
- **B1b PASS 4/6** at the 0.15 pp bar — **but the 4 passing arms are the 3 QUANTILE arms plus U56/MA-THRESH.** QUANTILE has `c_t ≡ x` by construction, so its ~0 residual is an *identity*, not evidence of constancy. **On MA-THRESH alone — the record's own gate form — the bar holds in 1 of 3 arms.** SMALL439's MA residual moves −0.02 → −0.59 pp/yr across the rule-8 boundary; idea 298's published −0.619 pp intercept for that panel is a *full-sample* number that its own IS window does not recover.

## B2 PER-PANEL vs GLOBAL — **REFUTED, and the direction is reversed**

| | OOS MAE (162 cells) | vs GLOBAL |
|---|---|---|
| GLOBAL (1 number) | 0.2458 | — |
| **PANEL (3 numbers)** | **0.2527** | **ratio 1.0281 — worse** |

Per-panel wins in **1 of 3** panels (SMALL439 0.3051 vs 0.3108; U56 0.1873 vs 0.1687; B136 0.2658 vs 0.2580). Restated on the 108 exactly-reproducing cells: PANEL 0.2854 vs GLOBAL 0.2817, **ratio 1.0132 — still worse**. Splitting the constant by panel costs accuracy; it does not buy it.

## THE ANSWER — the unit is the **FAMILY**, and it is idea 298's own prescription

OOS MAE (pp/yr) at λ=1, all 162 cells / 81 MA-THRESH / 81 QUANTILE, with R² against predicting zero:

| pooling | ALL | MA-THRESH | QUANTILE | R²_vs_zero (ALL) |
|---|---|---|---|---|
| ZERO | 0.2641 | 0.4903 | 0.0380 | 0.0000 |
| GLOBAL | 0.2458 | 0.3973 | 0.0944 | 0.2494 |
| **FAMILY (2 numbers)** | **0.1936** | **0.3517** | **0.0354** | **0.4187** |
| PANEL | 0.2527 | 0.4104 | 0.0951 | 0.2059 |
| PANELxFAM | 0.2123 | 0.3900 | 0.0346 | 0.3154 |
| CELL (162 numbers) | 0.2088 | 0.3966 | 0.0211 | 0.3415 |
| CBAR-OLS | 0.2180 | 0.4056 | 0.0303 | 0.2885 |

**FAMILY at λ=1 is the lowest-MAE estimator of all 35 grid points, on ALL and on MA-THRESH, and it replicates on the 108 exact cells (0.2407 / 0.4437, best pooling FAMILY on both).** Its two numbers are the IS means **MA-THRESH −0.2076, QUANTILE −0.0346 pp/yr** — which is, to the digit, what idea 298 wrote down without testing it ("~0.0 for a pure-exposure gate, 0.3–0.6 for an MA gate"). **Idea 298's prescription is vindicated in form; the queue's per-panel refinement of it is refuted.**

Three by-products:
1. **Pooling coarser than family is worse than saying nothing.** On the QUANTILE cells GLOBAL and PANEL score R²_vs_zero **−3.23 / −3.74** — they smear the MA family's −0.21 onto cells whose truth is −0.03.
2. **CBAR-OLS loses to the FAMILY constant at every λ** — a second, independent kill of idea 298's `c_bar` dependence. Its IS slope is "significant" on 3 of 6 arms (t +2.76…+3.98) and the OOS slope flips sign on 2 of the 3 MA arms.
3. **The mechanism behind "family" is how much `c_t` moves.** `corr(c_sd, |resid0|) = 0.7765` pooled and 0.57 / 0.56 *within* each family (`c_sd` mean 0.118 MA vs 0.006 QUANTILE). The family label is a proxy for gate-exposure volatility.

**But the constant is weak.** Best MA-THRESH MAE 0.3517 pp/yr against an OOS family mean of −0.4861 pp/yr — the prediction error is **72% of the level being predicted** — and every pooled estimator carries a **+0.1355 pp bias** (the residual got *more* negative out of sample on 2 of 3 MA arms). ρ(IS resid, OOS resid) across the 162 cells is 0.461, and 0.336 on MA-THRESH alone.

## Rule 8

**WF-A (the book).** (level, cadence) chosen on IS Sharpe inside each panel × family × construction arm, OOS read once: 12 picks. Beat **SPY OOS 8/12**, the cadence-matched no-filter control **5/12**, **RULES v2 OOS 0/12** (live book OOS CAGR 9.51% / Sharpe 1.2817 / MaxDD −12.05%). Mean regret vs the OOS oracle **−0.1258**.

**WF-B (the deliverable).** The whole estimator ladder is the walk-forward — every predictor fitted on IS cells only, scored once on OOS cells. Results above.

**WF-C — the estimator is NOT actionable.** Letting the IS-predicted gap pick the construction per cell gives the **identical** result for all 35 estimators (mean OOS Sharpe 0.9365, n_DEGROSS 0/162) because **the realised gap is negative in 162 of 162 OOS cells**: the sign is constant, so no residual estimator can earn on it. Always-RESPREAD 0.9365, always-DEGROSS 0.9052, OOS oracle 0.9426 — the whole decision is worth 0.006 of Sharpe and the estimator captures none of it. **This is a reporting discipline, not a book.**

## KEEP paths

**4a 0/324. 4b 16/324. Both 0/324.** 4b failure signatures: DD 121, all-five 70, CAGR 52, H1/H2/OOS/CAGR 33, pass 16, remainder ≤8 each. The 16 passers are idea 298's 16, same cells (13 U56, 3 B136, 0 SMALL439). Idea 298's one WF-clean 4b passer — U56 QUANTILE x=0.50 monthly RESPREAD — reproduces at **CAGR 15.51% / Sharpe 1.2385 / MaxDD −19.80% / halves 1.3501 / 1.1517 / OOS 1.2210** against its published 15.53% / 1.2400 / −19.80% / 1.3459 / 1.1581 / 1.2237; the |Δ| is the same U56 vintage drift that failed B3. It is a third un-pre-registered dial with no cross-panel replication and DD on the bar. **PARK re-affirmed, not promoted. No KEEP, no memo.**

## Survivorship

All three panels are **current constituents** — no delistings — so every CAGR level is inflated and the 4a/4b columns inherit that whole. The headline object is an arm-minus-arm contrast on the *same* names and days (DEGROSS and RESPREAD share one gate mask), so the bias very largely cancels out of `gap0`/`pred0`/`resid0`; it does **not** cancel out of the KEEP columns.

## Not touched

`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` unchanged. No rules change proposed.

Follow-ups filed: 535, 536, 537.
