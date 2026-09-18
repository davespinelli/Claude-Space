# Idea 1079 (lane cloud, 2026-09-18) — is RELIABILITY the statistic the record should have been publishing for rho?

**ANSWERED — NO, not as proposed. KILL (capital) + KILL of the proposed correction.**
Bycatch (positive, capital): the standing 2026-09-04 KEEP-4b book **survives 25 and 50 bps**.

Monthly, next-day execution, warm-up 260 rows, panels U56 / B136 / SMALL (663 names after
dropping the 52 with `max_1d_move >= 1.0` from `data/small_meta.csv`). 54 books
(3 panels x 9 N x 2 gross) read at 10 / 25 / 50 bps = 162 cells. Two tuned parameters only:
N and gross; cost is a reported scenario. Script:
`research/backtests/2026-09-18_is-RELIABILITY-the-statistic-the-record-should-have-been-publishing-for-rho_cloud.py`

## Gates
- **G1** cost enters `engine.backtest` strictly as `− turnover·bps/1e4` and never feeds the drift,
  so every cost rung is derived exactly from one zero-cost run: max|Δ| vs `engine.backtest`
  **6.94e-18 at 10, 25 and 50 bps**.
- **G2** the standing 2026-09-04 candidate reproduces: **0.1269 / 1.2019 / −0.1711 / OOS 1.2824**
  against idea 879's committed 0.1269 / 1.201 / −0.1711 / 1.281.

## Capital leg — all 162 grid points (`.grid.csv`)
**4a: 0 of 162.** **4b: 16 of 162** — all on U56; B136 0/54, SMALL 0/54.
By cost rung: **7 of 54 @ 10 bps, 6 of 54 @ 25 bps, 3 of 54 @ 50 bps.**

The standing candidate (U56, top-20 by the v1 composite without the vol scaler, gross 0.65,
monthly) across the cost ladder — it clears 4b at **all three** rungs:

| bps | CAGR | Sharpe | MaxDD | OOS Sharpe | 4b |
|---|---|---|---|---|---|
| 10 | 12.69% | 1.2019 | −17.11% | 1.2824 | PASS |
| 25 | 12.06% | 1.1480 | −17.19% | 1.2315 | PASS |
| 50 | 11.01% | 1.0574 | −17.32% | 1.1459 | PASS |

(U56 SPY 15.13% / 0.8848 / −33.72%, OOS 0.8745; live RULES v2 8.62% / 1.2017 / −12.05%, OOS 1.2778.)
The three survivors at 50 bps are N=15 g=0.65, **N=20 g=0.65**, N=40 g=1.00. Turnover 3.75x/yr at
the candidate. **Nothing is promoted** — 4a is 0 everywhere and no cell is a new book.

## Reliability leg — split-half (interleaved 63-day blocks, Spearman-Brown), 9-rung cells
| panel | mean rel_OOS | mean rel_IS | mean \|rho_obs\| | mean SD(OOS Sharpe) |
|---|---|---|---|---|
| U56 | **0.9679** | 0.0167 | 0.9333 | 0.1645 |
| B136 | 0.4428 | 0.3663 | 0.1639 | 0.0610 |
| SMALL | **0.0000** (raw split-half r = **−0.79**, clipped) | 0.7669 | 0.4056 | 0.0705 |

### Four reasons the proposal fails as stated
1. **The correction is undefined exactly where the idea says it is needed.** SMALL's split-half r is
   **negative** (−0.7889 to −0.8046 across all six cells), so reliability is 0 and
   `rho / sqrt(rel)` is **NaN in all 6 SMALL cells**. Disattenuation cannot be published for the
   small-cap panel at all.
2. **It does not reorder anything.** Rank on |rho| differs at 18 of 18 cells only because observed
   |rho| is heavily tied (all six U56 cells read 0.9333) and disattenuation breaks the ties;
   Spearman(rank_obs, rank_disatt) = **0.9063**. Mean |rho| 0.5009 → 0.5988. No cell crosses
   another materially, and 0 of 12 defined cells overshoot |rho| > 1.
3. **Reliability is not available ex ante.** rho(rel_IS, rel_OOS) across cells = **−0.9255**. The
   in-sample reading of the very statistic being proposed *anti*-predicts its out-of-sample reading.
4. **High reliability does not mean the choice transfers.** U56 has the highest OOS reliability
   (0.9679) and the **worst** picks (−0.3404 OOS Sharpe against the do-nothing anchor). Reliability
   here is high because between-book dispersion is large (SD 0.1645 vs 0.0610 / 0.0705), not
   because the in-sample ordering survives.

## Rule 8 — N chosen on 2009–2016 IS Sharpe alone, 2017–2026 read ONCE
| policy | fires | mean OOS Sharpe |
|---|---|---|
| always take the IS-max pick | 18/18 | **0.6690** |
| gate rel_IS ≥ 0.25 | 10/18 | 0.7905 |
| gate rel_IS ≥ 0.50 | 8/18 | 0.7966 |
| gate rel_IS ≥ 0.75 | 4/18 | **0.8007** |
| do nothing (hold the 9 rungs) | 0/18 | 0.7965 |
| panel SPY OOS, cell-weighted | — | 0.8760 |

rho(rel_IS, OOS gain of the pick) = +0.8846 looks decisive and **is not**: the 18 cells are 3
panels x 6 near-identical (gross, cost) readings, so the effective n is **3**, and the best gate
beats the do-nothing anchor by **+0.0042**. As in idea 1283 the same day, the gate's entire value
is in refusing to fire — it is a veto, not a selector, and nothing here beats SPY OOS.

## Census leg (mechanical; regexes in the console log)
163 files, 12,518 non-blank lines. **74** lines carry a rho/correlation claim about an OOS Sharpe;
**1 of them (1.4%)** also names reliability or attenuation. The record's practice is as idea 1079
alleges — but on this grid, correcting it changes no ordering and no verdict.

## What is NOT claimed
That idea 1073's 0.0915 / 0.5126 figures are reproduced or refuted — a different construction
(one book across composition draws) is measured there and is not re-run here. That reliability is
never worth publishing — only that *disattenuating rho by it* is undefined on SMALL, non-reordering
elsewhere, and unavailable ex ante. That the rel_IS gate works (effective n = 3). That any committed
verdict flips. That clipping a negative split-half r to 0 is the only defensible convention; the raw
r is reported beside it.

## Survivorship (rule 9)
U56 / B136 / SMALL are current constituents only, so every LEVEL is an upper bound; the quoted
results are within-grid differences on identical panels and dates and are first-order immune.
