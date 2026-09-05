# Idea 174 — the-sharpe-vs-4b-margin-sign-flip (lane C, 2026-09-05)

**VERDICT: ANSWERED — KILL of the idea's own hypothesis. 4b's CAGR floor and DD cap are
jointly satisfiable on this data, and the incumbent (0.70, 0.60) sits comfortably INSIDE the
non-empty region. 4b is a screen, not a wall. But the idea's *premise* is confirmed exactly,
and the reconciliation is the real finding: the CAGR floor is the most-violated bar because of
the LADDER the project sweeps, not because of the bar.** No RULES change, no new KEEP.

## Design
Two swept parameters, and they are the idea: **PHI** (CAGR-floor coefficient, 16 points
0.00–1.50) × **DELTA** (DD-cap coefficient, 20 points 0.10–2.00) = **320 grid cells, all
reported** (`.region.csv`). Pass/fail at any cell is a pure function of two numbers per point —
`c = CAGR/CAGR(SPY)` and `d = |MaxDD|/|MaxDD(SPY)|` — so the grid costs zero extra backtests and
nothing is re-fitted to pass.

Corpus (idea 171's, unchanged): 53 books (U56, B136, BSTK100, ETF36, SMALL484 + 48 sub-panels,
k∈{20,40,80}×16 draws, seed 171500+k) × 10 gross × 3 sleeve = **1590 points**, 10 bps, t+1,
weekly, book = idea 2's top-20 candidate. Book/gross/sleeve are corpus axes reported
exhaustively, not tuned.

## Reproduction, asserted before any new number was read
| check | result |
|---|---|
| [a] `fast_backtest` ≡ `engine.backtest` | max\|dret\| **2.776e-17**, max\|dturn\| 3.331e-16 — PASS |
| [b] idea 171's 530 committed GROSS-dial rows reproduced | **530 of 530**, max\|diff\| **2.220e-16** — PASS |
| [c] idea 171's premise re-counted on its own 1908 rows | CAGR **1223 of 1908** — matches the claim exactly |

## The answer

**Incumbent cell (0.70, 0.60):** `N_CD = 173` of 1590 points clear **both** coefficients
(31 of 53 distinct books); `N_4B = 151` clear all five bars of rule 4b. Best passer
`B136k40d04 @ g=0.90, f=0.30`: CAGR 11.75%, Sharpe 1.263, MaxDD −15.01%, halves 1.388/1.166,
OOS Sharpe 1.281 (SPY 15.23%/0.889/−33.72%, halves 0.957/0.834, OOS 0.882).

**Frontier.** `phi_max(delta)` = highest CAGR floor any point clears inside the DD cap:

| delta | 0.2 | 0.3 | 0.4 | 0.5 | **0.60** | 0.7 | 0.8 | ≥0.9 |
|---|---|---|---|---|---|---|---|---|
| phi_max (CD) | 0.411 | 0.575 | 0.731 | 0.892 | **0.957** | 1.076 | 1.200 | 1.200 |
| phi_max (full 4b) | 0.411 | 0.575 | 0.731 | 0.892 | **0.957** | 1.076 | 1.159 | 1.159 |

`phi_max(0.60) = 0.9569` against an incumbent phi of 0.70 — **headroom +0.2569 on both the
CD-only and the full-4b frontier.** The pair would have to be tightened to (0.96, 0.60) before
it became a wall. Grid-wide: `N_CD = 0` in 100 of 320 cells, `N_4B = 0` in 113 — the three
Sharpe bars close only **13** cells the two coefficients leave open.

**The closed form (Part 3B).** Because `c` and `d` scale together along the gross ladder, the
two coefficients collapse to one number: a point satisfies the pair iff its efficiency ratio
`k = c/d ≥ phi/delta`. The incumbent asks for **k ≥ 1.1667**. Observed: median k **1.376**,
max 2.187, **1340 of 1590 points** and **51 of 53 books** clear it. Idea 164 (cloud, same day)
derived the same constant from the other side — "non-empty iff rho/s ≤ delta/gamma = 0.857";
1/1.1667 = 0.8571. Independent agreement. k is near-invariant along gross (mean 1.233→1.286
across the whole 0.20–1.00 ladder) and is **moved by the sleeve** (1.270 → 1.392 → 1.509 at
f = 0.00/0.15/0.30), which is idea 139's point restated exactly. The one-number test predicts
cell non-emptiness in 267 of 320 cells (83.4%); its 53 failures are cells reachable only at a
gross outside [0.20, 1.00] — there the binding constraint is **PROTOCOL rule 2 (no leverage),
not rule 4b**.

## Reconciling the premise with the answer
Idea 171 was right that the CAGR floor is the most-violated bar, and it reproduces here:
violations at the incumbent are **CAGR 1280, H2 243, DD 153, H1 127, OOS 116** of 1590, and CAGR
is the *sole* binding bar for **1021** points (DD 87, H2 10, H1 3, multi 318, pass 151). But
"most violated" is not "unsatisfiable". Mean `c ≈ 0.856 × gross`, so the floor mechanically
requires `g ≳ 0.82`, and **8 of the 10 rungs of the ladder the project sweeps sit below that**:
the 4b pass rate is 0.0% at every gross ≤ 0.60 and 10.7–23.9% at g ≥ 0.70. The CAGR-floor count
is a fact about the *ladder*, not about the bar. `Spearman(c, d) = +0.9340` full sample,
+0.9166 OOS — return and drawdown are bought together, which is exactly the mechanism behind
idea 171's Sharpe-vs-margin sign flip, now measured.

## Rule 8 walk-forward
**W1 (region stability).** The map recomputed on the IS window alone and the OOS window alone:
at the incumbent, 172 points pass IS, 172 pass OOS, 80 pass both. Emptiness agrees in **306 of
320 cells**; `Spearman(n_IS, n_OOS) = +0.9942`. The region is a stable object, not a
window artefact.

**W2 (the pick).** At each cell, best IS Sharpe among IS-passers, read once on OOS.
Do-nothing control (best IS Sharpe, no screen): `B136k80d13 g=0.40 f=0.30`, OOS
5.36%/**1.0553**/−8.96%. Incumbent-cell pick `B136k80d13 g=0.70 f=0.30`: OOS
8.03%/**0.9804**/−12.93% — **−0.0749 vs the control**, +0.0984 vs SPY (0.8820), +0.4041 vs
RULES v1 (B136 OOS 5.94%/0.5763/−21.19%). Across the 240 non-empty cells: mean OOS Sharpe
0.9885 vs the control's 1.0553, and only **3 of 240 cells beat the control**. The (phi, delta)
screen is one more IS-fitted selector that loses to doing nothing — ideas 110/132/151/166/171,
fifth instance.

## Both KEEP paths (incumbent coefficients, all 1590 points, `.keep.csv`)
4a passes **1430** of 1590 (de-grossing makes MaxDD trivially better than the low-return live
book — PROTOCOL's own stated reason for adding 4b); 4b passes **151**; both **142**. Passers are
B136 141 / U56 10 / **SMALL484 zero**, consistent with idea 170. Per idea 144 these are
re-grossed/re-sleeved views of idea 171's already-committed books, so **this run proposes no new
KEEP candidate.**

## Pre-registered predictions, scored
P1 HIT/HIT/HIT · P2 **HIT** (region non-empty) · P3 **MISS** — I predicted a Sharpe bar would
bind; the CAGR floor binds, 1280 vs 243 · P4 HIT · P5 HIT (+0.934) · P6 HIT (−0.0749) ·
P7 HIT.

## Caveats carried
Survivorship (idea 54) biases every `c` up and every `d` down, so the region looks *more*
reachable than it is — "satisfiable" is the conservative direction here, "a wall" would have
been the strong claim. Idea 38 (calendar-day index) and idea 126 (t+1 only) carry over. The
1590 points are 53 books at 30 exposures, not 1590 independent trials (idea 144). One data set.

Artefacts: `.console.txt`, `.points.csv` (1590), `.region.csv` (320), `.frontier.csv` (20),
`.walkforward.csv` (320), `.keep.csv` (1590), `.memo.md`.
