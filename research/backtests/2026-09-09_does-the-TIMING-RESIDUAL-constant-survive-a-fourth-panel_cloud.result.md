# Idea 555 — does-the-TIMING-RESIDUAL-constant-survive-a-fourth-panel (cloud, 2026-09-09)

**Verdict: ANSWERED / KILL of the "gate-form constant" reading.** `resid0` is **not** a
property of the gate form. Measured on 36 fresh ETF-share-controlled sub-panels drawn from
**one** parent panel (B136), the MA gate's timing residual spans **0.7913 pp/yr**
(−0.7399 … +0.0514) — **9.2×** the 0.0857 pp/yr spread across the three published anchors that
differ 8× in width. The three-panel agreement the record read as a constant is inside the
sampling noise of a single panel. Both pre-registered clauses fail; the effect tracks the
panel, and the characteristics that price it are named below.

Script: `2026-09-09_does-the-TIMING-RESIDUAL-constant-survive-a-fourth-panel_cloud.py`
Artefacts: `.grid.csv` (all 4,212 books) `.decomp.csv` `.panels.csv` `.constant.csv`
`.regressions.csv` `.walkforward.csv` `.keeppaths.csv` `.console.txt`

## Gates, read before the headline

| gate | result |
|---|---|
| G0 `fast_backtest` vs `engine.backtest` (returns AND turnover, 9 cells) | **PASS**, max 8.882e-16 |
| G1 DEGROSS/RESPREAD identity `r_dg = c_t · r_rs` | **PASS**, max 4.198e-16 |
| G2 \|mean QUANTILE-F resid0\| < 0.05 pp/yr per panel | **FAIL on 1 of 39** (B30q00s1, −0.0535) |
| G3 \|Δ mask fraction\| MA vs QUANTILE-F < 0.01 | **PASS**, max 0.00596 |
| R1 reproduce idea 305's published anchors | **PASS to 4 dp on all three** |

R1 is exact: U56 −0.3375, B136 −0.4231, SMALL439 −0.3817, |Δ| = 0.0000 against the published
values. The G2-failing panel is excluded from the headline clauses as pre-registered and
reported both ways; it changes neither clause.

## The headline

| population | n | mean R_p | sd | min | max | **range** |
|---|---|---|---|---|---|---|
| published anchors (U56 / B136 / SMALL439) | 3 | −0.3808 | 0.043 | −0.4231 | −0.3375 | **0.0857** |
| fresh cuts of B136 (headline set) | 35 | −0.3507 | 0.1971 | −0.7399 | +0.0514 | **0.7913** |
| fresh cuts (G2-failing panel included) | 36 | −0.3560 | 0.1969 | −0.7399 | +0.0514 | 0.7913 |

`R_p` = MA-THRESH `resid0`, FULL window, mean over 9 θ × 3 cadences, gross 0.75, 0 bps derived.

- **Clause 1 (range ≤ 2 × anchor span = 0.1712 pp/yr): FAIL**, 0.7913. Four cuts are more
  negative than any published panel and one is positive.
- **Clause 2 (no characteristic reaches R² 0.30): FAIL.** Best single regressor over all 38
  headline panels is **ETF share, R² 0.3598** (slope +0.539 pp/yr per unit ETF share — more
  ETFs, less negative residual). Within the 36 fresh cuts alone: `mean_vol` **0.4322**,
  `c_bar` **0.4133**, `etf_share` **0.4017**, `xs_disp` 0.3090, `width` 0.2575.

**⇒ H_CHARACTERISTIC.** The residual moves with the panel's own volatility / ETF content, not
with the gate.

Structure of the fresh cuts (6 seeds per cell, all reported):

| ETF share | W = 30 | W = 60 |
|---|---|---|
| 0.00 | −0.355 (sd 0.055) | **−0.645** (sd 0.117) |
| 0.25 | −0.223 (sd 0.157) | −0.456 (sd 0.091) |
| 0.50 | **−0.188** (sd 0.136) | −0.238 (sd 0.112) |

Both dials move it monotonically and in the same direction as panel volatility
(0.309 → 0.249 mean name vol across the ETF ladder).

## Rule 8 walk-forward (WF-B — does the constant walk forward?)

IS ≤ 2016-12-31 chooses, OOS ≥ 2017-01-01 read once, nothing fitted.

| estimator | OOS MAE, all 38 | anchors (3) | cuts (35) |
|---|---|---|---|
| per-panel IS mean | **0.3415** | **0.2785** | 0.3469 |
| pooled IS constant (−0.1702 for all panels) | 0.3446 | 0.3159 | 0.3470 |
| zero | 0.5062 | 0.4861 | 0.5079 |

Both estimators beat zero, and the per-panel one beats the pooled one by only **0.0031 pp/yr**
— so the *panel identity* adds almost nothing out of sample once you know the level. What does
not hold is the **level itself**: mean R_p drifts **−0.1702 (IS) → −0.5062 (OOS)**, corr(IS,OOS)
+0.45 over the cuts and **−0.75** over the three anchors. Any forward use of a number in
[−0.70, −0.20] is quoting an in-sample level that has already moved by 0.34 pp/yr.

## KEEP paths (both, on all 4,212 books)

`4a: 10 / 4212` · `4b: 139 / 4212`. Failing-bar counts: DD 2833, CAGR 1618, H2 1082, OOS 964,
H1 875. Every 4a passer is a θ = +0.30 QUANTILE-F DEGROSS book earning **1.5 %–2.2 % CAGR** —
it clears the drawdown leg by barely being invested, which is the failure mode PROTOCOL 4b was
added to catch. WF-A: no arm beats the live book out of sample on any panel
(0 of 468 arm-rows; mean OOS Sharpe 0.95–1.10 against RULES v2's **1.2840**).

Best U56 book on the grid (θ +0.06, monthly, QUANTILE-F RESPREAD): CAGR 15.79 %, Sharpe 1.231,
MaxDD −19.7 %, halves 1.298 / 1.183, OOS Sharpe 1.253 / CAGR 17.01 %. Comparands on the same
sample — RULES v2 (live) OOS Sharpe **1.2817**, CAGR 9.51 %, MaxDD −12.1 %; SPY OOS Sharpe
0.8786, CAGR 15.38 %, MaxDD −33.7 %. It clears 4b and loses 4a to the live book on drawdown.
**No book is promoted and no memo is written**: this is a decomposition study, its panels are
survivorship-inflated, and θ is one of the two tuned dials.

## What the record has to change

The reading "the MA gate's timing residual is ≈ −0.35 to −0.42 pp/yr" is a statement about
three particular panels, not about the gate. Any forward quote of it must carry (i) the panel
it was measured on, (ii) the ±0.4 pp/yr sampling spread of a single-panel redraw, and (iii) the
window, because the level itself moved 0.34 pp/yr across the rule-8 boundary.

**SURVIVORSHIP:** B136, SMALL439 and every fresh cut are current constituents only — no
delistings. CAGR levels and the 4a/4b columns are inflated by that; `resid0` is an
arm-minus-arm contrast on the same names, days and ranking, so it is very largely immune.
