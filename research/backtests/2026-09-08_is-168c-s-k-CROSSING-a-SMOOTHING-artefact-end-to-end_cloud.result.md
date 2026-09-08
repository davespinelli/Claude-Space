# Idea 440 — is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end (cloud, 2026-09-08)

**ANSWERED, and the answer is stronger than the queue's question: idea 168c's "k crossing" is not
a smoothing artefact — it is not a measurement at all. `dSharpe` is defined WITHIN cell as
`Sharpe(k) − Sharpe(k=0)`, so the curve passes through exactly 0.0 at k = 0 in all 32 cells with
ZERO variance. `crossing_of` requires a strictly positive value, so the reading it returns is
mechanically the smallest positive grid point the reader can emit — +0.10 — and the bootstrap
confirms it returns exactly that in 2000 of 2000 draws under all three block definitions. The
half-window then walks it up to +1.00 because a symmetric window at a positive centre reaches back
into the steep negative arm; at hmult 5 the "window at +0.10" is the whole grid. KILL of the
"k threshold" object.** No RULES change, no KEEP (0 of 6 arms pass 4a or 4b); `RULES.md`,
`scan.py`, `bot.py`, `baseline.py` untouched.

Script: `research/backtests/2026-09-08_is-168c-s-k-CROSSING-a-SMOOTHING-artefact-end-to-end_cloud.py`
Artefacts: `.console.txt`, `.grid.csv` (528 fresh books), `.exact.csv`, `.window.csv`, `.boot.csv`,
`.shape.csv`, `.walkforward.csv`, `.pooled.csv`, `.keeppaths.csv`.

## Reproduction gate — before any new number was read

| check | published | this run | |
|---|---|---|---|
| `fast_backtest` vs `engine.backtest`, u56 k=−0.5 n=10 @10 bps | — | max abs diff **0.000e+00** | MATCH |
| 168c's committed books | 352 | 352 matched | MATCH |
| **broad** half, all 7 metrics (weekly price cache, vintage unchanged) | — | max abs diff **≤ 2.2e-16** | MATCH |
| u56 half, CAGR / Sharpe (daily price cache, vintage gone — see below) | — | 3.64e-04 / 3.93e-03, tol 1e-03 / 1e-02 | MATCH |
| live k = −0.5 loses to k = 0 on Sharpe | 32/32 | 32/32 | MATCH |
| signed dCAGR at live k negative @10 bps | 16/16 | 16/16 | MATCH |
| Spearman(k, CAGR) positive in every cell | "monotone" | 32/32 (+0.782 … +1.000) | MATCH |
| idea 439's readings, hmult 1–5 | 0.10 / 0.10 / 0.50 / 0.75 / 1.00 | identical | MATCH |

**Why the u56 half is not bit-exact, stated rather than hidden.** `data/prices.csv` is refreshed by
the daily job scan and only entered git on 2026-09-08 (commit `dcaffa8`); the vintage 168c ran on
2026-09-05 no longer exists. `data/prices_broad.csv` is refreshed weekly (protocol rule 9) and its
vintage is unchanged — and it reproduces to 2.2e-16, which is what proves the code path here is
168c's verbatim (`score_k` / `weights_k` / `panel` / `eligible_mask` are imported from the committed
168c script, not retyped). **Every conclusion in sections 1–4 below is read off 168c's OWN COMMITTED
`.curve.csv`, so none of them depends on the re-run at all.** The re-run exists to price section 5.

Two tuned parameters: **P1** half-window `hmult ∈ {0 (EXACT), 1, 2, 3, 4, 5}` × median grid step
0.25 (idea 439's own P1 with the exact reading prepended); **P2** bootstrap block ∈
{cell, panel×cost, panel}. All 6 × 3 grid points reported.

## (1) The curve is pinned to zero at k = 0, so the "crossing" is definitional

`dSharpe(k) = Sharpe(k) − Sharpe(k = 0)` within each (panel, cost, share) cell. Exact per-k means
over 168c's 32 cells, **no window at all**:

| k | mean dSharpe | sd | >0 in | t |
|---|---|---|---|---|
| −1.00 | −0.35419 | 0.25702 | 0/32 | −7.80 |
| −0.75 | −0.29403 | 0.23167 | 0/32 | −7.18 |
| −0.50 | −0.20276 | 0.16225 | 0/32 | −7.07 |
| −0.25 | −0.09826 | 0.09406 | 2/32 | −5.91 |
| −0.10 | −0.02558 | 0.02973 | 1/32 | −4.87 |
| **0.00** | **0.00000** | **0.00000** | **0/32** | — |
| +0.10 | +0.04596 | 0.05280 | 28/32 | +4.92 |
| +0.25 | +0.05142 | 0.05723 | 28/32 | +5.08 |
| +0.50 | +0.05254 | 0.06644 | 26/32 | +4.47 |
| +0.75 | +0.05513 | 0.06296 | 27/32 | +4.95 |
| +1.00 | +0.06066 | 0.07407 | 25/32 | +4.63 |

**EXACT `crossing_of` = +0.10, last non-positive centre 0.00.** The zero it "crosses" is the
control's own definitional zero, with sd exactly 0.0 in 32 of 32 cells. `crossing_of` needs a
*strictly* positive value, so k = 0 can never be returned and **+0.10, the next grid point up, is
the smallest number the reader is capable of emitting.** A statistic whose minimum attainable value
is also its realised value is not a location.

## (2) The bootstrap does not rescue it — it confirms the degeneracy

B = 2000, exact per-k means, three block definitions (P2):

| block | blocks resampled | crossing distribution | P(= 0.10) | P(≥ 0.50) |
|---|---|---|---|---|
| cell | 32 | +0.10: 2000 | **100.0%** | 0.0% |
| panel×cost | 4 | +0.10: 2000 | **100.0%** | 0.0% |
| panel | 2 | +0.10: 2000 | **100.0%** | 0.0% |

Perfectly stable — and stable at the reader's floor. The informative contrast is the one the
crossing hides: **is the k > 0 arm a ramp or a plateau?**

| block | mean dSharpe(+1.00) − mean dSharpe(+0.10) | 95% CI | separable? |
|---|---|---|---|
| cell | +0.01455 | [−0.01615, +0.04019] | **NO** |
| panel×cost | +0.01458 | [−0.01396, +0.04336] | **NO** |
| panel | +0.01483 | [−0.01396, +0.04336] | **NO** |

Across k ∈ (0, 1] the mean moves by **0.0147, i.e. 0.23 of the cross-cell sd (0.0627)**; across
k ∈ [−1, 0) it moves by **0.3286, i.e. 5.24 sd**. All the signal is in the negative arm. The
bootstrap argmax lands on +1.00 in 70.9% of draws and on +0.10 in 7.0% — a grid-edge argmax on a
flat arm, which is idea 168B's finding on the other lane, not an optimum.

## (3) The half-window cannot inform the reading, only relocate it

The design is balanced (32 cells at every k), so a windowed local mean is the *unweighted mean of
the per-k means inside the window*. Checked over all 55 grid points of all 5 windows:
**max |windowed − re-average of the exact per-k means| = 5.55e-17.** The smoothed curve is an exact
linear functional of the exact curve; it carries no information the exact curve does not.

| hmult | half-w | crossing | steps vs EXACT | grid points inside the window at centre +0.10 | window mean there |
|---|---|---|---|---|---|
| **0 (exact)** | 0.00 | **+0.10** | 0 | 1 (+0.10 alone) | **+0.04596** |
| 1 | 0.25 | +0.10 | 0 | 4, 1 negative | +0.01795 |
| 2 | 0.50 | +0.10 | 0 | 6, 2 negative | +0.00435 |
| 3 | 0.75 | +0.50 | 2 | 8, 3 negative | −0.01520 |
| 4 | 1.00 | +0.75 | 3 | 10, 4 negative | −0.03549 |
| 5 | 1.25 | +1.00 | 4 | **11 of 11 — the whole grid**, 5 negative | −0.06447 |

That is the whole mechanism of idea 439's 4-step march: a symmetric window at a positive centre
reaches back across the kink into the steep negative arm, and drags the local mean below zero. It
is not heterogeneity, not composition, and not noise — it is arithmetic, and it is one-directional
(a crossing on a curve with a steep negative arm can only be pushed *up* by widening the window).

## (4) Threshold or slope? Neither — a kink at the control point, then a plateau

Same 352 points, four shapes (knot searched over the 9 interior grid values, +1 parameter charged
for the search):

| model | params | τ̂ | RSS | R² | ΔAIC |
|---|---|---|---|---|---|
| linear | 2 | — | 6.74882 | 0.4755 | 69.12 |
| step @ τ | 3 | −0.50 | 6.52409 | 0.4929 | 59.20 |
| **hinge @ τ (free knot)** | 4 | **+0.10** | 5.48297 | 0.5738 | **0.00** |
| hinge @ 0 (pinned) | 3 | 0.00 | 5.54370 | 0.5691 | 1.88 |

Bootstrap (B = 1000, block = cell): τ̂ = +0.10 in **97.1%** of draws, +0.25 in 2.9%, 0.00 in 0.0%;
the free hinge wins AIC in 94.6%. **A step (a genuine threshold) is beaten by 59 AIC and is never
the winner; a pure slope by 69.** The best description is a kink between k = 0.00 and k = +0.10 —
the control point and its immediate neighbour, one grid step apart, with no grid point in between to
resolve them (hinge@0 is only 1.88 AIC behind). So: **the record has not been reading a slope and
has not been reading a threshold. It has been reading the corner where a within-cell difference
curve leaves its own definitional zero.**

## (5) It is not even a sign constant across panels — SMALL439 reverses it

Fresh 528-book corpus (3 panels × 2 costs × 11 k × 8 shares), dSharpe rebuilt the same way:

| panel | mean dSharpe @ −0.50 | @ +0.10 | @ +1.00 | >0 at +1.00 | EXACT crossing |
|---|---|---|---|---|---|
| u56 (56) | −0.2326 | +0.0599 | +0.0459 | 11/16 | +0.10 |
| broad (136) | −0.1728 | +0.0320 | +0.0754 | 14/16 | +0.10 |
| **SMALL439** | **+0.0119** | **−0.0326** (t −11.75) | **−0.2401** (t −11.26) | **0/16** | **none (nan)** |
| pooled 48 cells | −0.1312 | +0.0198 | −0.0396 | 25/48 | **none (nan)** |

On the sub-$2B panel the curve is monotone **decreasing**: every positive exponent hurts in 16 of 16
cells and the live k = −0.5 sits on the *right* side of zero. Adding one panel deletes the crossing
from the pooled corpus entirely. *(SMALL439 = current constituents of the screen, tickers with
`max_1d_move ≥ 1.0` dropped, 439 names; **survivorship bias** — reported as a shape check, never as
a tradable return.)*

## (6) Rule 8, live prices: k chosen on IS ≤ 2016-12-31, evaluated untouched on 2017–2026

Pooled equal-weight-of-cells book, 48 cells, 10 bps and 25 bps, weekly, t+1:

| arm | k | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| A_IS (IS-Sharpe argmax, per cell) | 10 distinct | 11.20% | 0.907 | −22.61% | 1.029 / 0.812 | 11.16% | 0.858 | −22.61% |
| **A_EXACT (k = +0.10)** | +0.10 | 10.86% | 0.828 | −22.92% | 0.874 / 0.797 | **11.89%** | **0.846** | −22.92% |
| A_HM3 (k = +0.50, 439's headline) | +0.50 | 10.68% | 0.788 | −23.28% | 0.809 / 0.777 | 11.90% | 0.819 | −23.28% |
| A_HM5 (k = +1.00, widest window) | +1.00 | 10.36% | 0.759 | −23.38% | 0.756 / 0.767 | 11.65% | 0.797 | −23.38% |
| A_ZERO (k = 0, no vol scaler) | 0.00 | 10.16% | 0.799 | −22.59% | 0.866 / 0.752 | 10.94% | 0.805 | −22.59% |
| A_LIVE (k = −0.50, RULES v1's) | −0.50 | 5.90% | 0.647 | −20.65% | 0.793 / 0.534 | 5.71% | 0.596 | −20.65% |
| **SPY** (equal-weight of the 3 panels) | — | 14.36% | 0.883 | −33.72% | 0.965 / 0.834 | 15.45% | 0.882 | −33.72% |
| **RULES v2 (live) @10 bps** | — | 6.69% | 1.032 | −10.90% | 1.086 / 0.987 | 7.13% | 1.063 | −10.90% |
| RULES v1 @10 bps | — | 6.93% | 0.756 | −18.24% | 0.840 / 0.691 | 7.48% | 0.768 | −18.24% |

**Which reading you adopt has a price, and it is negative.** Against A_EXACT, pooled OOS:
A_HM3 **−0.0276** Sharpe, A_HM5 **−0.0494** Sharpe and +0.46 pp of drawdown, A_ZERO −0.0408 Sharpe
and −0.95 pp CAGR, A_LIVE **−0.2504** Sharpe and **−6.18 pp** CAGR. Widening the window costs real
OOS Sharpe — the same direction and roughly the same size as the 0.054 idea 439 measured for
adopting the demeaned reading.

**Selection loses again.** The IS-Sharpe chooser beats the k = 0 control on OOS Sharpe in **25 of 48
cells, mean margin −0.0078 (sd 0.1446)** — a sixth coin flip after ideas 110/151/132/166/155/168.
Its chosen k is spread across all 10 non-edge values (−1.00: 6, −0.75: 7, −0.50: 3, −0.25: 4,
−0.10: 1, 0.00: 2, +0.10: 6, +0.25: 7, +0.50: 5, +0.75: 7) — it is choosing noise.

Per panel @10 bps (OOS CAGR / Sharpe / MaxDD): u56 A_EXACT 18.62% / 1.114 / −19.84% vs RULES v2
9.53% / 1.285 / −12.05% and SPY 15.45% / 0.882 / −33.72%; broad A_EXACT 13.94% / 0.955 / −20.90%
vs RULES v2 7.98% / 1.119 / −12.24%; SMALL439 A_EXACT 6.96% / 0.485 / −33.12% vs RULES v2
3.84% / 0.566 / −14.70%.

## (7) KEEP paths — none

Pooled 48-cell book, 4b bars off the pooled SPY (H1 > 0.965, H2 > 0.834, OOS > 0.882,
|MaxDD| ≤ 20.23%, CAGR ≥ 10.05%):

| arm | 4a vs RULES v2 | 4a vs RULES v1 | 4b | failing |
|---|---|---|---|---|
| A_IS | False | False | False | H2 \| OOS \| DD |
| A_EXACT | False | False | False | H1 \| H2 \| OOS \| DD |
| A_HM3 | False | False | False | H1 \| H2 \| OOS \| DD |
| A_HM5 | False | False | False | H1 \| H2 \| OOS \| DD |
| A_ZERO | False | False | False | H1 \| H2 \| OOS \| DD |
| A_LIVE | False | False | False | H1 \| H2 \| OOS \| DD \| CAGR |

**0 of 6 on both paths.** Every k-ladder arm clears the 4b CAGR floor but fails the drawdown bar
(−20.6% to −23.4% against a −20.23% cap) and loses SPY's halves; none beats RULES v2's Sharpe in
either half. The k dial does not produce a capital-worthy book at any exponent.

## Verdict

**KILL** — of the object, not of a rule. Idea 168c's k crossing is a reader floor sitting one grid
step above a definitional zero; idea 439's 4-step window sensitivity is the arithmetic of a
symmetric window straddling a kink; and the underlying shape is a hinge at the control point
followed by a plateau whose extent is not separable from zero. The k > 0 arm has no interior
optimum and no threshold, and on SMALL439 its sign reverses outright, so no k constant is publishable
across panels. What survives from idea 168 is the *negative* arm and only that: on both large-cap
panels the live k = −0.5 costs 0.250 of OOS Sharpe and 6.18 pp of OOS CAGR against k = +0.10, and
0.209 against k = 0 — the vol scaler's sign, not its magnitude, is the live question, and it is
already answered.

## What this run proposes (for the queue, not adopted here)

Two candidates, added to QUEUE.md rather than written into PROTOCOL.md, because a protocol clause is
a Sunday-review decision:

1. **A within-cell difference curve may not carry a published sign threshold.** When `y` is defined
   as `f(x) − f(x₀)`, `y(x₀) ≡ 0` with zero variance, and any sign reading is pinned to `x₀` by
   construction. Such a curve may publish a *magnitude* (a plateau level, a slope, a hinge) but the
   crossing is not a measurement. Back-fillable: the record's other difference curves are
   enumerable from the committed `*.curve*.csv` set.
2. **A local-mean reading on a balanced grid must publish its exact (unsmoothed) per-cell means
   beside it**, since the smoothed curve is provably an exact re-average of them and cannot add
   information. This is the sharpened form of idea 441's half-window column: the half-window is not
   just under-reported, it is uninformative by construction on a balanced design.
