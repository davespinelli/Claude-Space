# Idea 487 — is-a-draw-s-IS-SHARPE-the-wrong-thing-to-PREDICT (lane B, 2026-09-10)

**Verdict: ANSWERED/YES — the queue's own implication is CONFIRMED (nothing transfers even inside IS,
so sub-panel choice is a null); the competing REGIME explanation is FALSIFIED. KILL for capital.**
Script `2026-09-10_is-a-draw-s-IS-SHARPE-the-wrong-thing-to-PREDICT_B.py`, elapsed 866s, deterministic.

## The question and why the answer was not already in the record

Idea 484 found the name-additive ridge **wins the out-of-fold FIT** of a drawn sub-panel's IS Sharpe
and still **loses the rule-8 CHOICE** on both panels. Two readings produce that: the target is
unpredictable (selectors maximise noise), or the target is fine and 2017–2026 simply did not look
like 2009–2016 (regime). Every transfer test in the record scores IS-fitted predictions on the OOS
window, which cannot separate them. This run cuts the **IS window in half** and scores the IS1-fitted
models on **IS2** — both windows in-sample by rule 8's own definition — so the decisive leg reads no
OOS data at all.

Tuned parameters: exactly two, **TARGET** ∈ {Sharpe, CAGR, premium} × **PANEL** ∈ {B136, SMALL484}.
All 36 cells (target × panel × k × book size) reported at every point; k ∈ {20,40,80}, book ∈ {5,20},
D=500 draws/k cell, 10 folds, six penalties, seeds, 10 bps / weekly / next-day execution and the
2009-2016 / 2017-2026 split are idea 78/252/484's constants, imported verbatim.

## Gates (fired before any new number was read) — ALL PASS

| Gate | Check | Result |
|---|---|---|
| G1 | `fast_backtest` vs `engine.backtest`, 6 drawn books | **2.776e-17** |
| G2 | this run's 3,000 books vs idea 484's COMMITTED grid, **all 27 shared columns** | worst **7.105e-15** (`n_elig`); Sharpe/CAGR/MaxDD/halves/IS/OOS columns at **2.220e-16** |
| G3 | IS1/IS2 is a partition of IS — no overlap, no gap, ends before OOS | B136 1003+1004=**2007**; SMALL484 751+751=**1502**; overlap 0; IS2 ends 2016-12-30 < OOS 2017-01-03 |

G2 also re-derives idea 484's published KEEP counts exactly: B136/CAND20 **4a(v2) 12 / 4b 394 / BOTH 1**.
Windows (IS cut in half by trading-day count): B136 IS 2009-01-13..2016-12-31 = 2,007 days, IS1
2009-01-13..2013-01-07 (1,003 d) / IS2 2013-01-08..2016-12-31 (1,004 d); SMALL484 IS 2011-01-13..2016-12-31
= 1,502 days, IS1 2011-01-13..2014-01-08 (751 d) / IS2 2014-01-09..2016-12-31 (751 d).

## The three legs (medians over 36 cells; `.legs.csv` carries every one)

| Leg | Model | fit oofR2 | transfer ρ | centred transfer R2 | ρ≤0 cells | top-decile gain |
|---|---|---|---|---|---|---|
| **TRANSFER IS1→IS2** (no OOS read) | sd line | +0.0351 | **−0.0048** | −0.0452 | 18/36 | +0.0112 |
| | M (names, ridge) | **+0.7091** | **−0.0118** | **−0.7252** | 20/36 | +0.0051 |
| | M+sd | +0.7116 | −0.0156 | −0.7219 | 19/36 | +0.0068 |
| **OOS IS→2017-2026** | sd line | +0.0324 | +0.0605 | −0.0180 | 7/36 | +0.0077 |
| | M | +0.6987 | +0.0538 | −0.5918 | 12/36 | +0.0027 |
| | M+sd | +0.7018 | +0.0556 | −0.6082 | 12/36 | +0.0065 |

**The mechanism, in one line: the model that wins the fit by +0.6741 out-of-fold R2 loses the transfer
by −0.6800 centred R2.** Centred transfer R2 ≤ 0 in **104 of 108** model-cells. On the RAW (uncentred)
transfer R2 the IS1→IS2 leg is **0 of 36 positive for every one of the three models (0/108 pooled)**,
median −1.9894 (M) / −1.2424 (sd); the IS→OOS leg is 1/108 positive, median −0.7580 (M).

## The ceiling — and what it falsifies

The queue's own implication is confirmed: nothing transfers even inside IS. What the ceiling adds is
which of the two *explanations* survives.

The ceiling on any selector that predicts window 1 to choose for window 2 is the target's own
persistence, ρ(y₁,y₂):

| Seam | median ρ | sig. negative | sig. positive | by target (median) |
|---|---|---|---|---|
| **IS1→IS2 (inside IS)** | **−0.0249** | **11/36** | 5/36 | Sharpe −0.0342, CAGR −0.0224, premium −0.0249 (**0/12 significant**) |
| IS→OOS | **+0.0546** | 4/36 | 16/36 | Sharpe +0.0997, CAGR +0.1634, premium +0.0496 |

**The OOS seam persists MORE than the seam inside IS, not less.** The regime reading is therefore
falsified: nothing specific breaks at 2017. A drawn sub-panel's next-window Sharpe is ~unpredictable
from its own previous-window Sharpe *everywhere*, and inside IS the sign is not even stable (range
−0.178..+0.241, 11 cells significantly negative = the best IS1 draws are the worst IS2 draws).

**The clean percentile.** S1/S3/S4/S5 pick on y_IS, which *contains* IS2, so their high IS2 percentiles
are mechanical and are NOT evidence of transfer. The only selector fitted on **IS1 alone** is S2, and its
pick lands at IS2 percentile **0.5015 pooled (t +0.028 vs the 0.50 null)** — B136 0.663, SMALL484 0.340 —
against **0.5213** for random draws. Selection on an IS1 fit is indistinguishable from drawing at random.

## Pre-registered reading: **NULL INSIDE IS**

All three conditions met: all three models' median transfer ρ < 0.10 (−0.005/−0.012/−0.016); centred
transfer R2 ≤ 0 in 104/108 (bar 72); |decile t| < 2 in **73/108 (bar 72)**. *Stated honestly: the third
condition cleared by one cell.* There is a small, real, unexplained within-cell top-decile effect —
dec_t ≥ 2 in 23/108 against ~5 expected at 5%, median gain **+0.0074 Sharpe**, positive 23 / negative 12 —
an order of magnitude below what a choice needs and it does not survive into a pick (0.5015 above).
Flagged for the queue, not claimed as a rule.

## Rule 8 walk-forward and both KEEP paths

All 3,000 books (PROTOCOL 4): **4a(v1) 1,785 / 4a(v2) 13 / 4b 424 / BOTH 1.**
All 216 selector picks: **4a(v2) 0 / 4a(v1) 61 / 4b 20 / BOTH 0.** **No KEEP, no memo, no RULES change.**

Mean OOS Sharpe over the 18 (target × k × book) cells per panel:

| Arm | B136 OOS Sharpe | beats live / SPY | SMALL484 OOS Sharpe | beats live / SPY |
|---|---|---|---|---|
| **RULES v2 (live book)** | **1.1185** (7.98% / −12.24%) | — | **0.6629** (4.55% / −12.09%) | — |
| SPY | 0.8820 (15.45% / −33.72%) | — | 0.8820 | — |
| S0 do-nothing (whole panel) | 0.8529 | 0/18 | 0.4324 | 0/18 |
| S1 IS-target argmax | 0.9875 | 3/18, 13/18 | 0.2951 | 2/18, 2/18 |
| **S2 IS2 argmax on IS1 fit** | 0.9096 | **0/18**, 12/18 | **0.1416** | **0/18, 0/18** |
| S3 sd line | 0.9016 | 4/18, 9/18 | 0.1487 | 0/18, 0/18 |
| S4 M ridge | 0.9797 | 1/18, 13/18 | 0.3964 | 2/18, 0/18 |
| S5 M+sd ridge | 0.9797 | 1/18, 13/18 | 0.3968 | 1/18, 0/18 |
| S6 random draw | 0.8292 | 0/18 | 0.4250 | 0/18 |

**No selector beats the live book in the mean on either panel**, and this run's own persistence selector
(S2) is the worst arm on SMALL484 — below random (0.1416 vs 0.4250). Best single pick anywhere: B136
S1, k=20 / n=20 / draw 253, OOS **9.63% / 1.3063 / −13.86%** vs the live book 7.98% / 1.1185 / −12.24%
and SPY 15.45% / 0.8820 / −33.72% — one cell out of 108, chosen after the fact, and it still fails 4a(v2)
on drawdown.

## What the record should take from this

1. Idea 484's "wins the fit, loses the choice" is **not** a regime fact and **not** a selection-rule fact.
   It is a **target** fact: the fit is to window-specific noise (+0.71 R2 in-window, −0.73 out-of-window),
   and the quantity has no persistence to convert at any seam.
2. Sub-panel choice on any IS-side book statistic is a **null on its own training data**. Ideas that
   rank drawn sub-panels by an IS statistic should stop being run — including the IS-Sharpe argmax the
   record uses as its rule-8 incumbent, whose IS2 percentiles are contaminated by construction.
3. `premium` is the most clearly dead target: **0 of 12 cells** show significant persistence across the
   IS seam.

SURVIVORSHIP: both panels are current constituents only (PROTOCOL rule 9 / `data/SMALL_PANEL_README.md`);
the ceiling measured here is if anything flattered by it.

Artefacts: `.console.txt`, `.grid.csv.gz` (3,000 books, every window), `.legs.csv` (216 model-cells),
`.scoring.csv`, `.keeppaths.csv`, `.walkforward.csv` (324 rows).

## Reconciliation with the same-day cloud sibling (both designed and run before either landed on main)

`2026-09-10_is-a-draw-s-IS-SHARPE-the-wrong-thing-to-PREDICT_cloud.py` (commit 4fdd8fb) ran the same
idea independently. **The verdicts agree, the decisive numbers agree to the second digit, and one
reading is ADDED rather than contested.**

| Quantity | cloud | lane B (this run) |
|---|---|---|
| G1 fast backtest | 2.776e-17 | **2.776e-17** |
| G2 vs idea 484's committed grid | 7.105e-15 (1,500 B136 rows, 25 cols) | **7.105e-15** (3,000 rows, 27 cols) |
| fit oofR2, name-additive ridge | +0.796 (24 Sharpe cells) | +0.7091 (36 cells incl. CAGR/premium) |
| IS1→IS2 raw transfer R2 positive | **0 of 72** (median −2.87) | **0 of 108** (median −1.9894 M / −1.2424 sd) |
| IS1→IS2 transfer ρ | −0.03 | **−0.0118** (M) |
| ρ(y₁,y₂) IS1/IS2 | **−0.023** | **−0.0249** |
| ρ(y₁,y₂) IS/OOS | **+0.045** | **+0.0546** |
| upper-tail qualifier (real, unusable) | argmax above cell median in 5 of 6 (panel,k) clusters | top-decile gain +0.0074 Sharpe, sig. in 23/108 vs ~5 expected |
| KEEP paths on picks | 4a 0/120, 4b 13/120, BOTH 0/120 | **4a(v2) 0/216, 4b 20/216, BOTH 0/216** |

Both runs reach ANSWERED/YES and KILL for capital, and both flag the same real-but-unusable upper tail.
This run's addition: it reports the two seam ceilings **side by side and draws the directional
conclusion** — the IS/OOS seam persists MORE (+0.055) than the seam wholly inside IS (−0.025), on the
sibling's numbers as well as this run's — which kills the regime explanation of idea 484's result, and
it supplies the clean percentile (S2, the only IS1-only selector, at **0.5015**, t +0.028) showing that
the record's IS-argmax incumbent's apparent IS2 skill is contamination, not transfer. The sibling's
stronger framing, "winning the fit and losing the choice are the same fact", is the same conclusion.
