# Idea 802 — is the MATCHED-LEVEL RESIDUAL a SEPARATION law, not a SIZE law?

**ANSWERED = YES. The separation law is CONFIRMED pre-registered, walked forward, and published as an
entitlement curve. KILL for capital (no 4a pass on 6,768 books; the 64 4b passes are not claimed, as
stated up front). No RULES change, no book promoted, no PROTOCOL edit applied (rule 6);
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script: `2026-09-12_is-the-MATCHED-LEVEL-RESIDUAL-a-SEPARATION-law-not-a-SIZE-law_cloud.py`
(263.6 s, deterministic, no network). Tuned: **characteristic (13) × arm pair (6) = 78 cells, all
reported** (74 have ≥1 feasible rung; 702 rung rows, 524 feasible). Frozen, not tuned: BW 0.500,
k 36, 6 seeds, 9 decile rungs, 6 re-rolls. Panel: B136 134 tradable + SMALL 663 tradable
(max_1d_move ≥ 1.0 dropped per PROTOCOL), 797 names, 2010-01-04..2026-09-04, MMC dropped for an
interior gap (G1).

## Gates — all PASS, including an exact reproduction of the parent
G0 determinism 0 differences · G1 1 of 798 names gapped (dropped) · G2 vectorised vs pandas momac
**3.664e-15** (bar 1e-12) · **G3: all six (pair, char) points of idea 800's `.overlap.csv` rebuilt
from scratch — max |ΔSMD| 6.245e-17, max |ΔOVL| 0.000e+00** · G4 fast_backtest vs engine.backtest
1.388e-17.

## The law
| test | bar | measured | verdict |
|---|---|---|---|
| **H_SMD** Spearman(SMD, cell-mean d) | ≥ +0.70 | **+0.747** over 74 cells | **PASS** |
| **H_LIN** pooled rung fit d on SMD | R² ≥ 0.50, slope > 0 | **R² 0.684**, slope **+0.2766**, icept 0.0251 | **PASS** |
| **H_DISP** rung-local displacement beats SMD | R²(DISP) > R²(SMD) | **0.013 vs 0.684** | **FAIL — the alternative is refuted** |
| **H_SIZE** idea 800's kill holds | \|Spearman(min_n, d)\| ≤ 0.30 in every SMD tertile | +0.124 / **−0.332** / −0.038 | **FAIL (marginal, mid tertile only)** |
| **H_NOISE** signal over draw noise | span ≥ 3× re-roll sd | span 0.2647 vs median re-roll sd 0.0301 = **8.80×** | **PASS** |
| **H_ENTITLE** rule 8 on the curve | OOS p90 within 1.5× of IS p90 per bin | worst **1.10×** (0.68/0.94/0.93/0.74/1.10) | **PASS** |

The separation reading is not a six-point coincidence: it survives 13 characteristics and 6 arm
pairs, the two same-distribution nulls (SS, BB) land 65% in the bottom d tertile, and the
**rung-local** alternative — which would have made entitlement a property of where you draw rather
than of who you draw from — is dead (R² 0.013, joint-fit DISP coefficient −0.0018). `1/OVL` is the
one predictor that rivals SMD (FULL R² 0.729 vs 0.684) but it loses the IS selection (0.484 vs
0.516) and loses OOS too (0.679 vs 0.710), so SMD stands. Size is **not** fully inert: in the middle
SMD tertile Spearman(min_n, d) = −0.332 with the expected sign, so idea 800's kill is confirmed in
the large but is not exactly zero once separation is controlled — stated, not smoothed.

## The entitlement curve (the deliverable)
| SMD bin | n rungs | chars | d p50 | **d p90** | d max |
|---|---|---|---|---|---|
| [0.0, 0.1) | 182 | 12 | 0.0410 | **0.1149** | 0.2860 |
| [0.1, 0.2) | 101 | 9 | 0.0395 | **0.1039** | 0.1542 |
| [0.2, 0.4) | 152 | 11 | 0.0914 | **0.1822** | 0.3630 |
| [0.4, 0.8) | 42 | 5 | 0.1518 | **0.2659** | 0.3536 |
| [0.8, 1.6) | 47 | 7 | 0.3622 | **0.4896** | 0.5884 |

A k=36 / BW=0.500 matched-level draw between two arms separated by SMD is entitled to
|resid| ≈ d_p90 × sd(char) in raw units at every reachable rung — computable **before** drawing.
Worked example, the record's own arms: BS/momac sits at SMD 0.328 → d_p90 0.1822 → entitlement
**0.0132 momac units** (sd 0.0724), against idea 796's committed 0.00271 and idea 800's 0.0056. Both
published residuals are therefore *better than entitled*, which is the mechanical reason they read as
tight matches. Closed form if a bin is too coarse: **d ≈ 0.025 + 0.277 × SMD** (FULL; IS 0.249, OOS
0.279 — the slope is stable out of sample).

## Rule 8
**WF-A** (characteristics re-estimated IS-only and OOS-only, rungs re-frozen per window, predictor
chosen on IS pooled R² alone): pick **SMD** (IS R² 0.516) → **OOS R² 0.710, slope +0.2787**, read
once. DISP 0.006→0.009, min_n 0.008→0.016, n_eff 0.022→0.040, 1/OVL 0.484→0.679.
**WF-B** (6,768 books, pick by IS Sharpe alone): SS/beta rung 0.5572, arm B, EWall, g=1.00, IS Sharpe
1.963 → **OOS CAGR 12.95% / Sharpe 0.735 / MaxDD −33.27%** against RULES v2 OOS 9.53% / 1.285 /
−12.05% and SPY OOS 15.45% / 0.882 / −33.72%. FULL 16.73% / 1.024 / −33.27%, halves 1.880/0.648 —
the IS-best book halves in the second half, the familiar shape.
**KEEP paths:** 4a **0** of 6,768; 4b **64** (0.9%); BOTH **0**. 14 books beat RULES v2 OOS Sharpe,
1,549 beat SPY's. As stated before any number was read, a kernel-weighted seeded draw is a
diagnostic panel, not a tradable rule, so no 4b pass here is claimed as a capital candidate.

## Caveats
* **SURVIVORSHIP:** both arms are current constituents of their screens; dead names are absent. The
  law's object is a difference of achieved characteristic *levels*, so the bias is second-order
  there; the WF-B/KEEP-path return legs carry the usual upward bias and are diagnostics only.
* The curve is measured on SMD ∈ [0.001, 1.443] and k=36 / BW=0.500 only. Three of the six arm pairs
  (VSPLIT/TSPLIT/MSPLIT) are *induced* splits whose job is to populate the high-SMD end; without
  them the record's own arms never exceed SMD 1.32.
* High-SMD cells lose rungs to common support (BS/ivol 2 rungs, VSPLIT/mdd 4), so the top bin rests
  on fewer, narrower reaches — p90 there is an entitlement, not a tight estimate.
* momac is the only pool-dependent characteristic; its rank re-normalisation channel (idea 800's
  H_REEST) is orthogonal to this law and is not re-litigated here.
