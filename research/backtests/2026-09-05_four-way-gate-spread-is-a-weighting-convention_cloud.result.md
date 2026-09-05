# Idea 127 — four-way-gate-spread-is-a-weighting-convention (cloud, 2026-09-05)

**ANSWERED — KILL of the queue's premise.** The 0.356 → 0.080 collapse of the four-way gate
spread is **not** a weighting convention. It is the **ranking signal**. Holding the signal fixed
at ideas 38/56's raw 12-1 momentum, the matched-gross spread is **0.362** against the literal
**0.355** — the convention moves it by **+0.007 (−3% of the published gap, and in the wrong
direction)**. Idea 121's 0.080 is a *v1-composite* book, and the composite already contains a
0.5/1.0 trend factor and a /sqrt(vol20) scaler, i.e. it internalises the very gates being priced.

Grid: 3 panels × 3 signals × 4 gates × 3 conventions × (R10/R20/R40 + EWall) × 2 gross × 2 cost
rungs = **1440 rows, all reported** (`.grid.csv`). Exactly two tuned parameters (n, g).

## Reproduction (both exact, before anything new was read)
| row | none | 200d | vol60 | both | spread |
|---|---|---|---|---|---|
| ideas 38/56 published (small, mom, literal, g=0.75, 10bps) | 0.797 | 0.693 | 0.524 | 0.441 | 0.356 |
| this run | 0.799 | 0.694 | 0.527 | 0.444 | 0.355 (max\|diff\| 0.0034) |
| idea 121 published (small, v1c, matched) | 0.576 | 0.565 | 0.497 | 0.537 | 0.079 |
| this run | 0.576 | 0.565 | 0.497 | 0.537 | 0.079 (max\|diff\| 0.0000) |

Engine equivalence 6.9e-18 / 6.9e-18 / 1.4e-17 on u56 / broad / small. Idea 38's calendar-day
index warning re-checked: **0 weekend rows** on all three panels.

## 1. Attribution (small, n=40, g=0.75, 10 bps)
| | literal | matched | convention effect |
|---|---|---|---|
| **mom** (38/56's signal) | 0.355 | 0.362 | +0.007 |
| **v1u** (composite, no scaler) | 0.213 | 0.225 | +0.012 |
| **v1c** (composite, scaler — 121's signal) | 0.068 | 0.079 | +0.011 |
| signal effect at fixed convention | −0.287 | −0.283 | |

**Convention explains −3% of the gap; signal explains 103%.** Within the signal effect the split
is roughly half the composite blend (0.362 → 0.225) and half the vol scaler (0.225 → 0.079) —
idea 81's finding, now measured on the gate rows rather than the n-sweeps.

## 2. The convention is exposure TIMING, and it is small where the gate does not bind
For a ranked book the two conventions hold the **identical names**; literal is matched scaled by
f_t = k_t/n, so the whole effect is exposure. Splitting it (`sta` = matched at the literal book's
*constant* mean gross): over all 480 arms, |timing| median **0.0043** vs |level| median
**0.0000**; timing dominates in 86%. It is negligible on the ranked small-panel books (f = 0.99)
and large on the equal-weight books, where the gate actually de-grosses: small EWall+both
f = 0.419 (0.209 in SPY drawdowns > 10%), literal −2.0 pp CAGR and **+28.1 pp of MaxDD** vs
matched; u56 EWall+200d f = 0.710 (0.523 in crisis), timing **+0.080** Sharpe.

## 3. Which gate-indictment rows depend on the literal convention
Pre-registered flag (sign flip, or |matched| < half |literal|): **0 of 44 claim-cells**. Every
published gate indictment survives being re-weighted — including "vol60 is the larger destroyer"
(−0.272 literal → −0.285 matched) and ideas 49/51's equal-weight gate cost (−8.5 pp → −6.5 pp CAGR).

The census found the **reverse** exposure instead, and it is reported though it was not predicted:
in **8 of 44** cells the matched value is more than **twice** the literal one (max ratio 7.03), all
on **u56** — `d_both` −0.020 literal vs **−0.091** matched (n=40), −0.011 vs **−0.075** (EWall).
On large caps the literal convention **understates** the gate's Sharpe cost, because the cash the
gate raises pays for the names it excludes. The same thing inverts the OOS ordering: on u56 OOS at
n=40, literal gives tau **−0.67** (every gated book beats ungated) and matched gives **0.00**.
**A u56 gate row quoted under the literal convention is a statement about cash, not about the gate.**

## 4. Walk-forward (PROTOCOL rule 8) and KEEP paths
(n, g) chosen on IS Sharpe ≤ 2016-12-31 inside each (panel, signal, gate, convention, cost) cell,
OOS 2017-2026 read once: 216 picks, **102 beat SPY's OOS Sharpe 0.882**, 171 beat RULES v1, 17 pass
4b, **0 pass 4a**. Mean OOS Sharpe by panel: u56 1.112/1.076/1.076, broad 0.857/0.848/0.848, small
0.430/0.419/0.419 (lit/mat/sta) — the convention is worth ≤ 0.036 of mean OOS Sharpe anywhere.
Grid-wide: 140 rows pass 4a, 95 pass 4b, **0 of 480 small-panel rows pass 4b** (idea 121 reproduced).
Exactly **one** arm passes 4b in all four (u56/broad × 10/25 bps) cells: **EWall / vol60 / literal /
g=0.75** — the standing incumbent `EWall+vol60-dg`, confirmed here by a run that was not looking for it.

## 5. Predictions, scored (written before tests B–G)
P1 matched spread at fixed signal > 0.20 → **HELD** (0.362). P2 |lit−sta| < 0.05 in ≥ 2/3 of arms →
**HELD** (92%). P3 ordering inverts under matched on ≥ 1 panel → **HELD** (tau 0.67 on u56 and broad,
1.00 on small). P4 u56/broad spread < 0.15 → **HELD** (0.091 / 0.089). P5 nothing passes 4b on small
→ **HELD** (0/480).

## Caveats
Survivorship: all three panels are current-constituent lists; the small panel is a current sub-$2B
screen (483 names less the 44 with `max_1d_move ≥ 1.0` = 439), so every delisted, bankrupted or
acquired small cap of 2010-2025 is absent, the bias is one-directional, and it falls hardest on the
beaten-down cohort the 200d/vol20 gates exclude. **No level here is an achievable return**; the
spread itself does not fully escape the bias because the gates change which names are held. SPY is
selectable on u56/broad (ideas 94/95/121 convention) and benchmark-only on small. This run measures
a reporting convention; it promotes nothing.

## Proposed wording (for Sunday review; RULES.md untouched)
> A published gate/overlay row must state its weighting convention (`dg` literal / `rw` matched) and
> its mean admitted fraction f. Where f < 0.90 the row is a joint statement about the gate **and**
> about cash, and the matched-gross value must be quoted beside it.
