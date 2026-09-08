# idea 205 — the-pool-mean-as-a-leaderboard-column (lane B, 2026-09-08)

**VERDICT: ANSWERED / SPLIT — ADOPT the column as REPORT-ONLY in its CAUSAL (IS-window) form;
KILL it as a gate, screen or KEEP bar. No promotion, no RULES change.**

Script: `2026-09-08_the-pool-mean-as-a-leaderboard-column_B.py`
Artefacts: `.grid.csv` (1,224 arm-rows) `.cells.csv` (144) `.picks.csv` (288) `.backfill.csv` (520)
`.backfill_files.csv` (21) `.backfill_unresolved.csv` (1,571) `.paired.csv` `.keeppaths.csv`
`.walkforward.csv` `.domination.csv` `.reproduction.csv` `.console.txt`

## Gates
* **(a) engine equivalence** — the modified runner reproduces `engine.backtest` on every ungated
  book, all three panels: **max|diff| = 0.000e+00 (EXACT)**.
* **(b) corpus reproduction** — 1,224 of 1,224 rows matched against idea 151's committed grid;
  max|diff| **≤ 2.22e-16** on every one of 14 columns on all three panels (**EXACT**).
* **(c) column reproduction** — this run's `pool_mean_dSharpe_OOS` matches idea 151's published
  `pool_mean_dSharpe` over all 144 cell×pool rows to **9.71e-17 (EXACT)**. The back-fill is
  measuring the same object the record already publishes.

## Q1 — the literal ask: how many selector claims stand over a negative-expectancy pool?
Of **1,592 committed CSVs**, only **21 are poolable** under the pre-registered rule
(1,264 have no `arm` column at all, 142 no do-nothing arm, 115 no OOS/Sharpe column, 50 no cell
with one do-nothing arm and ≥2 rivals). Those 21 files contribute **520 cells**.

* **414 of 520 cells (79.6%)** stand over a pool whose own mean dSharpe is **negative**;
  mean −0.0373, median −0.0275. **P1 CONFIRMED cell-weighted, NOT file-weighted** (below).
* **Concentration, reported not buried:** one file
  (`2026-09-05_cagr-floor-calibration_B.calibration.csv`) is 378 of 520 cells (72.7%).
  Excluding it: **78 of 142 (54.9%)** negative. File-weighted (one vote per file):
  **median 50.0%, mean 43.5%** — below half. The headline 79.6% is a cell count, not 21
  independent claims, and the file-weighted reading does **not** support P1.
* 2 of 21 files are negative in every cell; 7 of 21 in no cell.

**The load-bearing fact for the record is not the 79.6% — it is that the record cannot answer
its own question.** 98.7% of committed CSVs cannot be resolved into (cell, pool, do-nothing arm)
at all. A column that can be back-filled onto 1.3% of the corpus is a column the record must
start emitting going forward, not one it can recover.

## Q2 — is the published column causal? Partly. **P2 REJECTED.**
Both committed instances compute the column on the **OOS** window, so as published it is not
knowable when the selector fires. Its causal twin (same statistic, IS window only):

| | sign agreement IS vs OOS | pearson r | spearman |
|---|---|---|---|
| all 144 cells | **86.1%** | +0.648 | +0.625 |
| u56 (54) | 81.5% | +0.490 | |
| broad (54) | 87.0% | +0.504 | |
| small (36) | 91.7% | +0.917 | |

Regression OOS ~ IS: slope +0.419, **r² 0.420**, t 10.14. The column is **forecastable**, which
is what makes the report-only recommendation live rather than decorative.

## Q3 — is it decision-relevant? **No. P3 REJECTED, and this is the KILL.**
Slope of the incumbent selector's realised d(OOS Sharpe) on the column, paired over 72 cells:

| pool | selector | column | slope | r² | t | sign agreement |
|---|---|---|---|---|---|---|
| P_ALL | K_Sharpe | OOS form | −0.296 | 0.028 | −1.41 | 52.8% |
| P_ALL | K_Sharpe | IS form | **−0.613** | 0.213 | −4.35 | 50.0% |
| P_ALL | K_CAGR | OOS form | +0.180 | 0.054 | +1.99 | 22.2% |
| P_ALL | K_CAGR | IS form | **+0.260** | 0.200 | +4.19 | 22.2% |
| P_S1 | K_Sharpe | OOS form | **+0.639** | 0.162 | +3.68 | 80.6% |
| P_S1 | K_Sharpe | IS form | **−0.189** | 0.047 | −1.86 | 72.2% |
| P_S1 | K_CAGR | OOS form | +0.328 | 0.137 | +3.33 | 72.2% |
| P_S1 | K_CAGR | IS form | −0.205 | 0.176 | −3.86 | 65.2% |

The slope **changes sign across arms in both forms**, with |t| > 3.6 on both sides of zero, and
sign agreement spans 22.2%–80.6%. There is no stable direction to read the column in. It
describes the pool; it does not tell you what the selector will do.

## Q4 — priced as a GATE: KILL at every threshold
GATE(K, τ): take K's pick iff the cell's causal pool mean ≥ τ, else hold the cell's own ungated
book. 7 τ × 2 selectors × 2 pools = **28 grid points, all reported** in `.keeppaths.csv`.

Mean d(OOS Sharpe) vs do-nothing, and the two degenerate endpoints of every arm:

| pool | selector | τ=−∞ (ungated) | τ=+∞ (do nothing) | best interior τ | interior dominates both? |
|---|---|---|---|---|---|
| P_ALL | K_Sharpe | −0.0241 | 0.0000 | −0.0038 (τ=+0.02) | **No** |
| P_ALL | K_CAGR | **+0.0100** (t 3.17) | 0.0000 | +0.0047 (τ=−0.02) | **No** |
| P_S1 | K_Sharpe | −0.0045 | 0.0000 | −0.0003 (τ=+0.02) | **No** |
| P_S1 | K_CAGR | **+0.0040** (t 2.35) | 0.0000 | +0.0007 (τ=−0.02) | **No** |

**The interior gate dominates both of its own endpoints in 0 of 4 arms.** Nine of twenty interior
points do beat do-nothing, but every one of them does so by walking *toward* an endpoint and
never past it: where the selector helps, the gate subtracts from it; where the selector hurts,
the gate merely does less of it (take_rate collapses to 0.014–0.083 on P_ALL).

**KEEP paths.** Arm-rows: 4a-vs-v2 28/1,224, 4a-vs-v1 465/1,224, 4b(full) 198/1,224,
4b(OOS) 222/1,224, both 8/1,224. On gated selections, **4a-vs-v2 falls from 4 (ungated K_CAGR)
to 0 at every interior τ, and both-paths from 4 to 0**. Do-nothing's own baseline over the same
72 cells is 4a_v2 0, 4b 9, 4b_oos 9, both 0. **No KEEP on either path at any of the 28 grid
points.** Mean OOS book across cells: gated 0.9245–0.9293 Sharpe / 13.6–13.8% CAGR / −24.4 to
−24.7% MaxDD, against do-nothing 0.9246 / 13.68% / −24.75%, SPY 0.8820 / 15.45% / −33.72%,
RULES v2 1.0379, RULES v1 0.6001 (10-bps rung, OOS window).

## Rule 8 — nested walk-forward for τ (arms on A ≤2012, τ* on B 2013–2016, read once on C 2017–2026)
| pool | selector | τ* chosen on B | C mean_d | C OOS Sharpe / CAGR / MaxDD |
|---|---|---|---|---|
| P_ALL | K_Sharpe | **+0.01** (interior) | **−0.0119** (t −1.76, 0 wins of 3) | 0.9127 / 13.47% / −24.63% |
| P_ALL | K_CAGR | **+∞ (do nothing)** | 0.0000 | 0.9246 / 13.68% / −24.75% |
| P_S1 | K_Sharpe | **−∞ (gate off)** | −0.0052 (t −1.91) | 0.9194 / 13.36% / −24.09% |
| P_S1 | K_CAGR | **−∞ (gate off)** | +0.0029 (t 1.75) | 0.9275 / 13.64% / −24.01% |

Comparands on C: do-nothing 0.9246 / 13.68% / −24.75%; RULES v2 1.0379; RULES v1 0.6001;
SPY 0.8820 / 15.45% / −33.72%.

**P4 is REJECTED as literally coded and CONFIRMED in substance.** The honest window chose a
degenerate endpoint in 3 of 4 arms, so the one positive number (+0.0029) is the *ungated*
K_CAGR selector, not the gate. Forcing an interior τ and reading it once on C gives
[−0.0119, +0.0045, −0.0031, +0.0005]; the single arm where an interior gate dominates both
endpoints out of sample (P_ALL/K_CAGR, +0.0045, 3 wins of 4 moves, sign p 0.625) is one the
walk-forward **chose do-nothing for**. The gate never wins a decision it was actually allowed
to make.

## Recommendation to the Sunday review
1. **ADOPT** `pool_mean_dSharpe` as a REPORT-ONLY column beside any published selector claim,
   in its **CAUSAL (IS-window)** form, with `n_pool` beside it. It is free (both numbers are
   already computed inside every selector run), it is forecastable (r² 0.42 onto the OOS form),
   and 79.6% of back-fillable cells (though only half of poolable files) stand over a pool
   that could not have helped.
2. **DO NOT** make it a gate, a screen, an admission rule or a KEEP bar. Priced as one it loses
   at every threshold, on both selectors, on both pools, and on the nested walk-forward.
3. **The back-fill is 1.3% of the corpus.** If the record wants this column it has to emit
   `arm` + a do-nothing row + cell keys going forward; it cannot recover them.

## Caveats
Survivorship (idea 54) on all three panels — every CAGR is flattered and no level here is an
achievable return; both sides of every pair come from the same flattered panel, so the paired
signs stand. 72 cells are not 72 independent observations (books and arms overlap heavily inside
a panel) — per-panel breakdowns are in the console. The back-fill reads committed CSVs at face
value and reports the *poolable population*, not a verified list of published selector sentences;
`.backfill_files.csv` makes the mapping auditable. Idea 126: t+1 execution throughout.
