# Idea 2125 (lane C, 2026-09-22) — IS THE 4b CAGR FLOOR REACHABLE AT ALL BELOW GROSS 1.00?

**ANSWERED = YES, DOWN TO GROSS 0.50 (the grid's own lower edge) ON BOTH PANELS IN ALL
THREE WINDOWS — BUT THE DEVICE THAT REACHES IT IS NOT A NON-EXPOSURE DEVICE, AND AN
INFORMATION-FREE PLACEBO REACHES IT AT THE SAME CELLS. KILL of the "concentration is a free
route to the floor" reading. NO NEW KEEP, no rules change.**

Script: `research/backtests/2026-09-22_4b-cagr-floor-below-gross-one_C.py`
Artifacts: `.log.txt`, `.grid.csv` (1,800 rows, every point), `.b1.csv`, `.b2.csv`,
`.b4.csv`, `.b8.csv`, `.walkforward.csv`, `.gates.csv`.
Gates: **4 of 4 PASS** — G1 local loop == `engine.backtest` max|d| **0.000e+00** over 4,706
rows; G2 mask == `rebalance_mask('W')` 0 differing rows; G3 the N=ALL column is
`baseline.rules_v2_weights` **bit-identical** (max|d| 0.000e+00); G4 no leverage (max row-sum
over nominal g = 4.441e-16).

## The book and the dials
RULES v2's own form with ONE new dial: band 0.03 fixed at the live value; among the names
whose band state is TRUE, hold the **top N** by the record's own no-vol-scaler composite
(`baseline.score(px, vol_scale=False)`) at **g/N** of NAV each; any shortfall goes to CASH,
never re-spread. N = ALL recovers the live book exactly. Weekly, t→t+1, 10 bps, long only.
**Exactly two tuned parameters — gross g ∈ {0.50,0.60,0.75,0.85,1.00} × holdings
N ∈ {5,10,20,40,ALL}** — and all 1,800 grid points (2 panels × 3 rankings × 25 cells ×
4 cost rungs × 3 windows) are published.

## B1/B2 — THE PUBLISHED NUMBER
At 10 bps, de-grossed cells (g ≤ 0.85) clearing the 4b CAGR floor (0.70 × SPY, same window):

| panel | window | floor | clear / 20 | best cell | best CAGR | margin |
|---|---|---|---|---|---|---|
| U56 | FULL | 10.60% | **13/20** | g=0.85 N=5 | 25.54% | +14.94 pp |
| U56 | IS | 10.47% | **10/20** | g=0.85 N=5 | 24.85% | +14.38 pp |
| U56 | OOS | 10.70% | **14/20** | g=0.85 N=5 | 26.11% | +15.41 pp |
| B136 | FULL | 10.59% | **13/20** | g=0.85 N=5 | 24.41% | +13.83 pp |
| B136 | IS | 10.47% | **14/20** | g=0.85 N=5 | 23.74% | +13.27 pp |
| B136 | OOS | 10.68% | **13/20** | g=0.85 N=5 | 24.97% | +14.29 pp |

**Lowest gross clearing the CAGR floor: 0.50 — the grid's own lower edge — on 6 of 6
panel×window blocks**, at N=5 and N=10. Lowest gross that is a FULL 4b PASS: **0.50** (U56
all three windows; B136 IS), 0.60 (B136 FULL), 0.75 (B136 OOS). So 2119's reading — that on
the band family the floor is a pure exposure bar — **does not survive the holding-count
dial**. The floor is a property of the FAMILY, not of the BAR.

## B3 — but the dial is not the non-exposure device it looks like
Realised mean gross, FULL, U56: at nominal g the N=ALL band book runs **0.355 / 0.426 /
0.533 / 0.604 / 0.710** (≈0.71 × nominal — the out-of-band names' weight is cash), while
every finite-N book runs ≈**1.00 × nominal** (N=5: 0.501/0.601/0.751/0.850/1.000), because
there are almost always ≥ N names in band (mean names held 5.0 / 9.9 / 19.3 / 35.2 vs the
live book's 38.4 of 56). **At the same nominal g=0.50 the concentrated book runs 41% more
realised exposure than the live book does.** Nominal gross and realised gross are different
dials on this family, and the idea's question was posed in the nominal one.

## B4 — MATCHED-REALISED-GROSS CONTROL: concentration buys CAGR with drawdown, at a Sharpe loss
Every floor-clearing cell with g ≤ 0.85 (77 of them) against the plain N=ALL band book
scaled to the SAME realised mean gross (max mismatch **1.8e-04** of gross):

* CAGR higher at **76 of 77** cells, median **+4.29 pp**
* Sharpe higher at only **25 of 77**, median **−0.0936**
* Shallower at only **2 of 77**, median **−5.51 pp of MaxDD**
* and it is monotone in the dial — median (dCAGR, dSharpe, dMaxDD) by N:
  **N=5 (+9.26, −0.104, −9.99) · N=10 (+4.65, −0.137, −6.01) · N=20 (+3.05, −0.092, −3.74) ·
  N=40 (+1.98, −0.005, −1.00) · N=ALL (−0.00, +0.000, +0.00)** (the last row is the identity
  check: the twin of the twin).

So at matched exposure the device is a **variance trade**, not an edge: it reaches the CAGR
floor by running a deeper book, which is exactly the trade the 4b DD cap exists to price.

## B8 — THE DECISIVE CONTROL: an information-free ranking reaches the floor at the same cells
Priced but never selected on: **BOTTOM** (reverse composite) and **ALPHA** (alphabetical by
ticker — zero information). De-grossed cells clearing the floor / full 4b passes of 120:

| ranking | clear the floor (g≤0.85, 6 blocks) | full 4b passes, g≤0.85 | triple-window (FULL∧IS∧OOS) 4b cells |
|---|---|---|---|
| TOP (the book) | 10–14 of 20 per block | **26 / 120** | **3 of 50** |
| ALPHA (placebo) | 9–13 of 20 per block | **31 / 120** | **7 of 50** |
| BOTTOM (reverse) | 0–3 of 20 per block | **5 / 120** | 1 of 50 |

**All three of TOP's triple-window 4b cells (U56 g=0.50/N=5, U56 g=0.85/N=40,
B136 g=0.75/N=40) are also ALPHA passers**, and ALPHA produces more of them than TOP does.
The chooser separates TOP from BOTTOM (that part is real — BOTTOM's best FULL CAGR is 13.39%
against TOP's 30.02%), but **what reaches the CAGR floor below gross 1.00 is CONCENTRATION
on a current-constituent tape, not the ranking**. On a survivorship-biased list any 5 of 56
names went up; the placebo says so directly.

## B5 — RULE 8 (parameters on IS only, 2017–2026 read ONCE): the floor is reachable but NOT by rule 8
The IS-Sharpe chooser goes straight to maximum gross and maximum concentration on both
panels and blows the DD cap:

| | U56 | B136 |
|---|---|---|
| IS pick | g=1.00, N=5 (IS Sharpe 1.2465) | g=1.00, N=10 (IS Sharpe 1.2083) |
| OOS | **30.56% / 1.0376 / −36.53%** (H 1.107/0.975) | **21.29% / 0.8601 / −32.95%** (0.924/0.803) |
| FULL | 30.02% / 1.1074 / −36.53% | 23.29% / 0.9891 / −32.95% |
| RULES v2 OOS | 9.46% / 1.2767 / −12.05% | 7.85% / 1.1017 / −12.24% |
| SPY OOS | 15.29% / 0.8751 / −33.72% | 15.26% / 0.8737 / −33.72% |
| 4b OOS | **FAIL** — DD **−16.30 pp**, CAGR +19.86 pp | **FAIL** — DD −12.72 pp, H1 −0.0668 |
| 4b FULL | FAIL — DD −16.30 pp | FAIL — DD −12.72 pp, H2 −0.0466 |
| 4a | **FAIL** both windows | **FAIL** both windows |

**PATH 4a: 0 of 25 at every panel × window.** The one cell that passes 4b in FULL **and** IS
**and** OOS on U56 (g=0.50, N=5: FULL 14.99%/1.1022/−19.70%, OOS 15.45%/1.0310/−19.70%,
IS 14.43%/1.2432/−13.01%, realised gross 0.501) is **not rule-8 reachable** — the IS chooser
does not pick it — and the ALPHA placebo passes at the same cell, so it is **not even a
PARK**: it is the artefact B8 was written to catch.

## B7 — cost ladder
De-grossed cells clearing the floor / lowest-gross full 4b pass, by cost:

| panel | window | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|---|
| U56 | FULL | 13/20 · 0.50 | 13/20 · 0.50 | 11/20 · 0.50 | 7/20 · 0.85 |
| U56 | IS | 12/20 · 0.50 | 10/20 · 0.50 | 9/20 · 1.00 | 4/20 · **NONE** |
| U56 | OOS | 15/20 · 0.50 | 14/20 · 0.50 | 12/20 · 0.50 | 9/20 · 0.75 |
| B136 | FULL | 15/20 · 0.50 | 13/20 · 0.60 | 11/20 · **NONE** | 4/20 · **NONE** |
| B136 | IS | 15/20 · 0.50 | 14/20 · 0.50 | 12/20 · 0.50 | 5/20 · **NONE** |
| B136 | OOS | 14/20 · 0.50 | 13/20 · 0.75 | 11/20 · 0.75 | 3/20 · **NONE** |

The reach survives 25 bps on U56 and dies at 50 bps on 4 of 6 blocks — the concentrated
books turn over 19–23×/yr against the live book's much lower rate, so the answer is
cost-sensitive in the direction the turnover predicts.

## VERDICT — **KILL** (of the hypothesis, not of a book)
The literal question has a YES answer and a published number (**lowest gross = 0.50, the
grid edge, 6 of 6 blocks**), so 2119's "pure exposure bar" reading is retired. But the route
is not the non-exposure route the idea hoped for: at matched realised exposure the device
loses Sharpe at 52 of 77 cells and runs 5.5 pp deeper, and an information-free alphabetical
ranking reaches the floor at the same cells and produces MORE triple-window 4b passes than
the real chooser. No KEEP, no PARK, no memo, RULES v2 untouched.

## CAVEATS
**Survivorship (PROTOCOL rule 9)** is load-bearing here in a way it usually is not: U56 and
B136 are current-constituent lists, and a holding-count device concentrates into exactly the
names the list was selected on, so every absolute CAGR at small N is optimistic by an
unknown and *increasing* amount as N falls. The B4 matched-gross contrast and the B8 placebo
are WITHIN-TAPE (same names, same dates) and are what the verdict rests on; neither repairs
the level. The band is held at the live 0.03 throughout (idea 2119 already laddered it), so
this run says nothing about band × N interaction. Offsets are not measured here, so idea
914's clause is not applied to any margin above — irrelevant to the verdict, which is a KILL.
