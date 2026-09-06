# Idea 298 — does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level (cloud, 2026-09-06)

**Verdict: ANSWERED — and the answer is NEITHER of the two things the title offers.**
**The exposure share is a property of the GATE'S FORM (partial R² 0.374), not of the panel
(partial R² 0.0020, three panels indistinguishable). The level does matter (partial R² 0.271)
but in the OPPOSITE direction to the queue's stated intuition: a gate that de-grosses LIGHTLY
looks LESS like pure cash drag, not more.**
**KILL of the share-vs-c_bar discount curve as a usable rule (it does not walk forward);
REPLACED by a zero-parameter constant-residual discount that does. No rules change.
One 4b BY-PRODUCT, PARKed — it needs a dial this run did not pre-register.**

Script: `research/backtests/2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud.py`
Console: `….console.txt` · CSVs: `.grid` (324 books) `.decomp` (486 = 162 cells × FULL/IS/OOS) `.walkforward`

## Construction

3 panels × 2 gate FAMILIES × 9 strictness levels × 3 cadences × 2 constructions = **324 books**,
162 decomposition cells, every one reported. 10 bps, 75% gross, next-day execution, weekly/
monthly/quarterly. The 0-bps rung is *derived exactly* (`r0 = r10 + turnover·bps/1e4`), not re-run.

| dial | values | status |
|---|---|---|
| strictness level | QUANTILE x ∈ {.20 .30 .40 .50 .60 .70 .80 .90 .95}; MA-THRESH θ ∈ {+.30 +.20 +.12 +.06 .00 −.06 −.12 −.25 −.40} | **tuned (1 of 2)** |
| cadence | W, M, Q | **tuned (2 of 2)** |
| panel | SMALL439, U56, B136 | reported |
| gate family | QUANTILE (c_t ≡ x by construction), MA-THRESH (px > ma200·(1+θ)) | reported |
| construction | RESPREAD (w=g/k_t·G), DEGROSS (w=g/n_t·G) | reported |

**Reproduction gates, asserted before any new number was read.**
`max_t |r_dg,t − c_t·r_rs,t|` = **5.55e-17** over all 162 cells (idea 290's P1 identity, bar 1e-12).
SMALL439 / MA-THRESH θ=0.00 reproduces idea 290's published cells: c_bar 0.5039/0.5087/0.5106 vs
0.5040/0.5087/0.5106 (|Δ| ≤ 7e-5) and share 0.9760/0.9481/0.8270 vs 0.9760/0.9480/0.8262
(|Δ| ≤ 8.5e-4) at W/M/Q. **B4 PASS.**
No-filter control reproductions: SMALL439 weekly 10.20% / 0.6792 / −36.16% (idea 49/52 published
10.2% / 0.677–0.679 / −36.2%).

## The answer: the share is the gate's FORM, and the level pushes the wrong way

**QUANTILE — a gate with no market-timing content.** Its timing residual is essentially zero at
*every* level, so it is pure cash drag from c_bar 0.14 to 0.96:

| U56 / QUANTILE / weekly | x=.20 | .40 | .60 | .80 | .90 | .95 |
|---|---|---|---|---|---|---|
| c_bar | 0.2059 | 0.4059 | 0.6065 | 0.8062 | 0.9065 | 0.9623 |
| gap0 pp/yr | −14.34 | −9.32 | −5.98 | −2.63 | −1.27 | −0.52 |
| **resid0 pp/yr** | **−0.017** | **−0.017** | **−0.014** | **−0.006** | **+0.003** | **−0.003** |
| **share** | **0.9988** | **0.9982** | **0.9976** | **0.9976** | **1.0025** | **0.9936** |

**MA-THRESH — the record's own gate form.** Its residual is a level-independent lump of bad
exposure timing that does *not* shrink with the gap, so the share collapses exactly where the
queue expected it to go to 1:

| U56 / MA-THRESH / weekly | θ=+.30 | +.12 | .00 | −.06 | −.12 | −.40 |
|---|---|---|---|---|---|---|
| c_bar | 0.0424 | 0.2318 | 0.7074 | 0.8571 | 0.9212 | 0.9893 |
| gap0 pp/yr | −28.58 | −17.21 | −3.91 | −2.20 | −1.48 | −0.27 |
| **resid0 pp/yr** | −0.147 | −1.282 | −0.231 | −0.443 | −0.484 | −0.132 |
| **share** | 0.9949 | 0.9255 | 0.9409 | **0.7989** | **0.6720** | **0.5188** |

Collapsed over all 162 cells (the "discount table" the queue asked for):

| c_bar rung | ≤.25 | .25–.35 | .35–.45 | .45–.55 | .55–.65 | .65–.75 | .75–.85 | .85–.92 | >.92 |
|---|---|---|---|---|---|---|---|---|---|
| n | 30 | 15 | 15 | 15 | 12 | 18 | 11 | 18 | 28 |
| mean share | 0.988 | 0.980 | 0.973 | 0.959 | 0.961 | 0.923 | 0.955 | **0.877** | **0.799** |
| sd | 0.016 | 0.027 | 0.032 | 0.054 | 0.073 | 0.093 | 0.088 | **0.138** | **0.180** |
| mean resid0 pp | −0.21 | −0.22 | −0.22 | −0.27 | −0.16 | −0.29 | −0.12 | −0.23 | −0.13 |

The share **falls** as c_bar → 1 and its spread **quadruples**, because `resid0` is flat in c_bar
while `gap0` shrinks to zero. **Both pre-registered hypotheses FAIL as written:**

* **H_QUEUE** (share → 1 as c_bar → 1; within 0.03 of 1.000 at c_bar ≥ 0.85 in ≥5/6 arms) → **3/6, FAILS.** It holds in all three QUANTILE arms and in none of the MA-THRESH arms (0.639 / 0.749 / 0.736).
* **H_RATIO** (share invariant to c_bar; |t(slope)| < 2 and sd ≤ 0.10 in a majority) → **1/6 and 3/6, FAILS.** The eps does *not* cancel: `resid0 ~ 1 + (1−c_bar)` fits with a significant **intercept** on all three MA-THRESH arms (−0.619 t −5.43 / −0.267 t −3.16 / −0.352 t −3.96) and R² of only 0.04–0.19, against R² 0.92–0.98 for `gap0` and `pred0`. The timing cost is a **constant in pp/yr**, not a share.

**B3 — panel or level?** `share ~ 1 + c_bar + panel + family + cadence`, n=162, R² 0.610. Partial R²:
**family 0.3739 > c_bar 0.2708 ≫ panel 0.0020 ≈ cadence 0.0018.** Family t **+12.19**, c_bar t
**−10.37**, both panel dummies **t +0.24 / +0.86**. Mean share by panel is 0.846 / 0.859 / 0.869
(B136 / SMALL439 / U56) — a 2.4pp spread against a 14pp family spread. **The panel is not the
variable.** Idea 290's 0.914 was therefore *not* a SMALL439 fact; it was an MA-gate-at-c_bar≈0.5 fact,
and it would have read ≈0.999 with a quantile gate at the same c_bar, or ≈0.52–0.69 with the same
MA gate loosened.

## Rule 8 — the deliverable gets its own walk-forward, and fails it

**WF-B.** `share ~ 1 + c_bar` fitted on IS (2011/2009–2016) cells only, then used to predict each
cell's OOS share: IS fit `share = 1.0103 − 0.0706·c_bar` (t −2.86, **R² 0.0487**).

| OOS predictor | mean abs err | RMSE | bias |
|---|---|---|---|
| curve fitted on IS | **0.0957** | 0.1647 | −0.0651 |
| IS mean share (constant) | 0.0994 | 0.1733 | −0.0650 |
| idea 290's 0.914 (constant) | 0.1179 | **0.1609** | **−0.0097** |

The curve beats a constant by 0.004 of mean absolute error and *loses* to idea 290's flat 0.914
on RMSE and on bias. IS→OOS share rank stability is only **0.3485**. Per arm the curve's edge over
the constant is +0.010/+0.004/+0.012 on the MA arms and **negative** on all three QUANTILE arms.
**A share-vs-c_bar curve is not a usable discount rule.** What survives is the finding underneath
it: discount a de-gross claim by *subtracting the gate's own timing residual*, ≈0.0 pp/yr for a
pure-exposure gate and ≈0.3–0.6 pp/yr for an MA gate, independent of c_bar — a zero-parameter
correction, and the only form of this deliverable that walked forward.

**WF-A** (the book; (level, cadence) chosen on IS Sharpe inside each of 12 arms, OOS read once):
regret 0.000 to −0.718; the DEGROSS arms pick badly (SMALL439/MA-THRESH −0.247, U56/MA-THRESH
−0.718) while the QUANTILE arms pick within 0.026 of the OOS best in 4 of 6.

## KEEP paths — all 324 books

**4a: 0 / 324.** RULES v2 (live) is Sharpe 1.2056 at MaxDD −12.05% on this window; nothing here
comes near that drawdown. **4b: 16 / 324** (13 U56, 3 B136, **0 SMALL439**); failures are
DD 120, `H1,H2,OOS,DD,CAGR` 70, CAGR 52.

**The one by-product worth a line, and why it is PARK not KEEP.** WF-A's IS-only pick in the
U56 / QUANTILE / RESPREAD arm — **top 50% of live names by distance above the 200d MA, equal
weight, 75% gross, MONTHLY** — clears 4b outright: **15.53% CAGR / Sharpe 1.2400 / MaxDD −19.80%,
halves 1.3459 / 1.1581, OOS Sharpe 1.2237**, against SPY 15.23% / 0.8890 / −33.72% (halves
0.9566 / 0.8340, OOS 0.8820) and bars H1>0.957, H2>0.834, OOS>0.882, MaxDD ≥ −20.2%, CAGR ≥ 10.66%.
Regret vs the OOS-best cell in its own arm is only −0.0256 (x=0.60 gives 1.2493). It is **PARK**
because: (i) the QUANTILE family was declared a *reported* dimension, so picking it is a third,
un-pre-registered dial; (ii) it does **not** replicate across panels — B136/QUANTILE/RESPREAD's
own IS pick fails 4b on the DD cap and SMALL439's fails on all five bars; and (iii) its MaxDD
clears the cap by 0.4pp, i.e. it sits on the bar. Follow-ups 299–301.

## Survivorship

`prices_small.csv.gz`, `universe.json` and `universe_broad.json` are **current constituents, no
delistings**, so every CAGR level here is inflated and the 4a/4b columns inherit that whole — the
PARKed by-product especially, since it is a level claim on U56. The headline is an arm-minus-arm
contrast on the *same* names and days (DEGROSS and RESPREAD share one gate mask g), so the bias
very largely cancels out of gap0 / pred0 / resid0 and out of the share; it does not cancel out of
anything in the KEEP section.
