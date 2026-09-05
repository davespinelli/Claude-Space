# Idea 113 — crisis-beta-as-the-pre-registrable-selector — **KILL** (2026-09-05, lane C)

Script: `2026-09-05_crisis-beta-as-the-pre-registrable-selector_C.py`
Console: `.console.txt` · grid: `.grid.csv` · betas: `.betas.csv` · picks: `.picks.csv` ·
diagnostics: `.diagnostics.csv` · paired: `.paired.csv`

## The proposal, made precise

Idea 99 measured a −1.03 slope of per-year overlay value on that year's SPY MaxDD. The queue's
follow-up: turn that into a selector that needs no OOS window. For each grid point *p*,

    beta_IS(p) = −OLS_slope( d_y(p) ~ SPY_MaxDD_y )  over the 7 IS years 2010–2016,
    d_y(p)     = Sharpe_y(p) − Sharpe_y(no-overlay control)
    S_crisis(B): argmax over the grid of [ IS_Sharpe(p) + beta_IS(p) · B ]

B is the stated drawdown budget in MaxDD units. **B = 0 is PROTOCOL rule 8 exactly**, so the
selectors nest and the question is one-sided: does any B > 0 beat B = 0?

Pre-registered before any number was computed: B ∈ {0.05, 0.10, 0.20}; a falsification control
`S_anti100` (the same dial turned the wrong way, B = −0.10); `S_null` (no overlay); `S_oracle`
(argmax OOS Sharpe — cheating, reported only to fix the ceiling). Tie-break everywhere: smallest
overlay parameter. Tuned parameters = 2 (budget × overlay parameter). 44 cells: 6 overlay grids
(sleeve, band, breadth, stop, crypto, gross) × 2 books (top20, ewall) × 2 universes (u56, broad)
× 2 cost rungs (10, 25 bps), weekly — the same cells as ideas 99 and 109. All 328 grid points
printed and in `.grid.csv`.

## Result: every budget is worse than rule 8, and worse than turning the dial backwards

44 cells, out-of-sample 2017-01-01 → 2026-09-04 (never touched by any selector but the oracle):

| selector | OOS Sharpe | OOS CAGR | OOS MaxDD | regret vs oracle | 4a | 4b | 4b(OOS-only) |
|---|---|---|---|---|---|---|---|
| **S_sharpe (rule 8, B=0)** | **1.048** | **13.3%** | −19.7% | **−0.015** | 17 | **20** | **22** |
| S_crisis050 (B=0.05) | 0.960 | 11.4% | −17.9% | −0.103 | 15 | 15 | 16 |
| S_crisis100 (B=0.10) | 0.960 | 11.2% | −17.5% | −0.103 | 16 | 14 | 16 |
| S_crisis200 (B=0.20) | 0.960 | 11.0% | −17.2% | −0.103 | 17 | 14 | 16 |
| S_anti100 (B=−0.10, control) | 1.023 | 14.1% | −21.5% | −0.040 | 15 | 10 | 12 |
| S_null (no overlay) | 0.993 | 12.4% | −19.2% | −0.070 | 18 | 19 | 19 |
| S_oracle (cheats) | 1.063 | 13.0% | −18.7% | 0.000 | 21 | 15 | 21 |

Reference: SPY OOS Sharpe 0.882, OOS CAGR 15.45%, OOS MaxDD −33.7%; RULES v1 OOS Sharpe 0.65.

Paired, cell by cell, against rule 8: **mean ΔOOS Sharpe −0.088 at every budget**, better in
3/5/6 cells and worse in 15/18/20 of the 18/23/26 cells where the pick differs. **The ceiling
rule 8 leaves is +0.0150** (mean regret vs the OOS oracle — an exact reproduction of idea 99's
+0.015 on independent code). The proposal does not eat into that ceiling; it burns **5.9× the
whole ceiling**. It also loses **5–6 of rule 8's 20 full-sample 4b passes** and 6 of its 22
OOS-only 4b passes. Excluding crypto (short IS window) and restricting to the defensive grids
both make it worse, not better (−0.113 and −0.141 regret).

The falsification control settles it: **the dial turned backwards (−0.088 → −0.025) beats the
dial turned the way idea 99's slope says it should go.** If crisis beta carried the claimed
information, +B would beat −B. Neither beats rule 8.

Robustness arm (declared, not tuned): re-estimating beta on the 28 IS **quarters** instead of the
7 IS years does not reverse anything — ΔOOS Sharpe −0.091 / −0.108 / −0.108, better in 1–4 cells,
worse in 17–23. Verdict is taken from the pre-registered annual estimator; the robustness arm
agrees.

## Why it fails — two measured mechanisms, not bad luck

**T1 — crisis beta shrinks ~6× out of sample.** Across the 164 non-null points, beta_IS does
rank-predict the same point's beta_OOS (Spearman **+0.744**), but the OLS slope is only **+0.172**:
mean beta_IS 2.80 → mean beta_OOS 0.378. The selector adds an **unshrunk** beta, over-crediting
crisis protection by about a factor of six. The IS fit itself is barely identified — mean Pearson r
of the per-point annual regression is −0.06 to −0.22 (R² ≈ 0.5–5%) on n = 7 points.

**T2 — crisis beta does not predict OOS payoff.** Cross-sectional regression of realised d_OOS on
beta_IS: slope −0.008, Pearson **−0.604**, Spearman **+0.159**. The sign disagreement means no
reliable monotone relation — the linear fit is dragged by the extreme sleeve points. The control
rule 8 already uses, plain IS value d_IS, predicts d_OOS far better: Pearson **+0.850**, Spearman
**+0.703**. Rule 8's input is the better input.

**The structural defect (this is the real finding).** beta_IS is not a bounded correction term;
it is an unbounded, superlinear function of overlay *dose*. On `u56 / sleeve / top20`:

| f (sleeve fraction) | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---|---|---|---|---|
| IS Sharpe | 1.012 | 1.060 | **1.077** | 0.938 | 0.271 |
| beta_IS | 0.0 | 2.6 | 7.1 | 14.3 | **31.8** |
| OOS Sharpe | 1.156 | 1.208 | **1.261** | 1.243 | **0.728** |

At B = 0.05 the objective is 1.077 + 7.08·0.05 = 1.43 for f = 0.50 against 0.271 + 31.8·0.05 =
1.86 for f = 1.00. **Any B > 0 saturates the dial at the grid endpoint**, which here is the pure
macro sleeve — the worst arm on the grid. That is where the damage lives: per-grid mean ΔOOS
Sharpe is **−0.460 on `sleeve`** against −0.03..+0.01 on band/breadth/stop/gross/crypto. The
selector is not mistuned; it is degenerate on any grid where beta scales with dose, which is
every defensive grid.

**And the honest budget is ~0.005, not 0.05.** The OOS window's mean annual SPY MaxDD is −13.8%
against the IS window's −11.1%, so the *realised* budget was **B\* = +0.027** — already below the
smallest budget tested. Composed with T1's 0.172 shrinkage, the correctly-specified coefficient
on beta_IS is 0.172 × 0.027 ≈ **0.005**, an order of magnitude below the pre-registered grid's
smallest value. Rule 8's B = 0 is within a rounding error of the right answer.

## What this does and does not settle

- **Does not** overturn idea 99's T2 regression: the pooled per-year slope is real. It shows that
  the slope is a *pooled, window-level* fact and does not survive being estimated *per grid point*
  and used as a selector — pooled crisis sensitivity ≠ estimable per-arm crisis beta.
- Rule 8 beats no-selection by +0.055 of mean OOS Sharpe (1.048 vs 0.993), reproducing idea 109's
  headline on independent code. Idea 110's pre-registration test of that +0.055 is unaffected.
- Third selector proposal in a row to lose to plain argmax IS Sharpe (idea 109's CAGR floor
  −0.010; this run's crisis beta −0.088). The accumulating evidence is that **rule 8 as written
  is close to the frontier on this project's grids**, and the +0.015 ceiling is small enough that
  no selector-side idea is worth more runs.

**No RULES change. No PROTOCOL change.** Recommend closing the selector line: ideas 111 and 113
were the two follow-ups from idea 99 aimed at the selector; this one is dead and 111 is a
documentation change, not an edge.

## Caveats

- SURVIVORSHIP: both equity panels are current constituents of their lists; levels are biased up.
  The bias is identical across selectors, which is what this run compares.
- Idea 38's calendar-day index caveat applies to every grid point, every beta and every selector
  identically.
- CRYPTO: BTC-USD starts 2014-09-17, so that grid's beta_IS is fitted on ~2 usable years; results
  are reported in and out of every pooled statistic and the verdict does not depend on it.
- 2026 is a partial calendar year in the OOS beta and B\* figures (kept for consistency with idea 99).
- S_oracle sees the OOS window by construction and is a ceiling, never a rule. Its lower
  full-sample 4b count (15 vs 20) is expected: maximising OOS Sharpe is not maximising 4b.
- The "corrected budget ≈ 0.005" figure is arithmetic composed from T1's slope and the realised
  B\*, not a selector that was run; it is stated as a scale check, not a result.
