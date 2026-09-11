# Idea 573 — is-the-4b-PASS-RATE-a-PANEL-OF-ORIGIN-statistic-everywhere (cloud, 2026-09-11)

**VERDICT: ANSWERED — the ORDERING is a panel-of-origin fact everywhere (U56 holds the top 4b
rate in 9 of 9 cells, SMALL439 is 0 of 360), but the ORIGIN EFFECT IS NOT SEPARABLE FROM BOOK
FAMILY at this resolution (panel spread 0.161 vs family spread 0.167, both at the ~0.16 bar 40
draws can resolve). KILL for capital: the rule-8 pick fails both KEEP paths, and the IS
objective picks the cell whose OOS 4b rate is 0.025 while the best OOS cell (0.450) reads
0.025 in-sample.**

## Scope, stated honestly
The queue asks for a CENSUS of committed runs reporting 4b passes over draws. Those counts are
prose and per-file CSV schemas, not runnable objects, and a census of them carries no price
leg — it can satisfy neither rule 8 nor either KEEP path. This run instead REBUILDS the object
the census was meant to adjudicate, on a construction idea 569 never used: **3 source panels ×
3 widths k × 3 book families × 40 draws = 1,080 draw books**, gross 0.75, weekly, 10 bps, t+1,
warm-up `px.index[260]`, IS ≤ 2016-12-31, OOS ≥ 2017-01-01. It replicates the origin effect; it
does not restate any committed count, and nothing published is retired here.

Draws: k names without replacement from the panel's investable columns (SPY excluded from every
draw, used only as the benchmark), seed 573 + (k, draw), so each draw set is a pure function of
its coordinates. Families, built on the drawn names alone: **BAND** (RULES v2 form on the draw),
**TOP10** (composite, no vol scaler, above-200d and vol20 < 0.60, gross/10 — the 2026-09-04
KEEP-4b family), **EWALL** (equal weight, no gate). Tuned parameters: k and family. The panel is
the question, not a dial.

## Gates (pre-registered, all PASS)
G1 `fast_backtest` == `engine.backtest` on a probe draw **6.939e-18** · G2 `band_book(0.03,0.75)`
== `rules_v2_weights` **0.000e+00** · G3 SMALL dropped the **44** `max_1d_move >= 1.0` names →
440 cols · G4 draws reproducible at seed, SPY-free, exactly k distinct in-panel names · G5 IS
statistics on a frame TRUNCATED at IS_END **0.000e+00**.

## 4b pass rate by panel of origin — every (family, k) cell

| family | k | U56 | B136 | SMALL439 | winner | spread |
|---|---|---|---|---|---|---|
| BAND | 12 | 0.125 | 0.100 | 0.000 | U56 | 0.125 |
| BAND | 24 | 0.000 | 0.000 | 0.000 | tie(0) | 0.000 |
| BAND | 36 | 0.000 | 0.000 | 0.000 | tie(0) | 0.000 |
| EWALL | 12 | 0.125 | 0.000 | 0.000 | U56 | 0.125 |
| EWALL | 24 | 0.175 | 0.000 | 0.000 | U56 | 0.175 |
| EWALL | 36 | 0.025 | 0.000 | 0.000 | U56 | 0.025 |
| TOP10 | 12 | 0.150 | 0.075 | 0.000 | U56 | 0.150 |
| TOP10 | 24 | 0.400 | 0.375 | 0.000 | U56 | 0.400 |
| TOP10 | 36 | **0.450** | 0.150 | 0.000 | U56 | 0.450 |

Pooled: **U56 0.161 (58/360), B136 0.078 (28/360), SMALL439 0.000 (0/360)**; by family BAND
0.025 / TOP10 **0.178** / EWALL 0.036; by width k=12 0.064, k=24 0.106, k=36 0.069.
4a pooled: U56 0.033, B136 0.019, SMALL439 0.003 (max cell 0.125, BAND k=24).

**B1 PASS** — U56 is the top panel in 9 of 9 cells (two of them 0–0 ties at the floor), and
SMALL439 passes 4b in **0 of its 360 draw books** at every family and width. The origin
ordering U56 ≥ B136 > SMALL439 is exceptionless on this construction.

**B2 — but origin does not out-rank construction.** Mean 4b spread across panels at fixed
(family, k) = **0.161**; across families at fixed (panel, k) = **0.167**. At 40 draws the
pass-rate SE is ~0.08, so a difference below ~0.16 is not resolvable (idea 528): both spreads
sit *at* that bar and neither is separable from the other. The honest reading is that
**"the panel of origin decides the 4b count" and "the book family decides it" are the same
size of claim here** — the only unambiguous origin fact is SMALL439's zero.

## Rule 8 — cell chosen on IS alone, OOS read once (27 cells, all published in `.walkforward.csv`)

| | panel | family | k | IS 4b rate | OOS 4b rate |
|---|---|---|---|---|---|
| IS pick | U56 | EWALL | 36 | **0.500** | **0.025** |
| best OOS cell | U56 | TOP10 | 36 | 0.025 | **0.450** |
| runner-up IS | U56 | EWALL | 24 | 0.325 | 0.175 |

Acted book (declared tie-break, fixed before the run: the **median IS Sharpe** draw of the
picked cell, draw #10): full CAGR **13.52%**, Sharpe **1.1073**, MaxDD **−24.09%**, halves
1.1883 / 1.0378; **OOS CAGR 13.67%, Sharpe 1.1039, MaxDD −24.09%** against **RULES v2 OOS
9.45% / 1.2747 / −12.05%** and **SPY OOS 15.24% / 0.8721 / −33.72%**. **4a FALSE, 4b FALSE.**

IS→OOS rank transport of the 4b rate over the 27 cells is Spearman **+0.7009** — the ordering
largely survives, but the *argmax* does not: the IS objective loads on EWALL (gateless, k=36),
whose OOS rate collapses 0.500 → 0.025, while TOP10 at k=24/36 goes the other way (IS 0.025–0.100
→ OOS 0.375–0.450). A selector that picks the cell to hunt in by IS 4b rate therefore picks the
wrong family, which is the same failure mode idea 712 flagged for PICK-4b-IS.

## Why this is a KILL for capital
Every 4b pass in the run is a *draw*, not a rule: the passing draw sets are chosen by the seed,
not by anything knowable in advance, and the one pre-registered selector that turns the census
into a decision lands on a book that fails both paths and loses 0.17 of OOS Sharpe and 12 pp of
drawdown to the incumbent while buying 4.2 pp of CAGR. Nothing here is promotable.

## Caveats
SURVIVORSHIP (idea 54): all three panels are current constituents with no delistings, so every
CAGR level is inflated and both KEEP columns inherit it; SMALL439 is the current sub-$2B screen
less the 44 `max_1d_move >= 1.0` names. OVERLAP (idea 719): U56 and B136 share 55 of 56 names, so
"U56 wins 9 of 9" is really *one* large-cap reading beating the disjoint small panel, not two
independent confirmations. 40 draws per cell ⇒ SE ≈ 0.08 at 50%. One OOS window, read once.
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Artefacts: `.draws.csv` (1,080 draw books), `.bypanel.csv`, `.walkforward.csv` (27 cells),
`.console.txt`.
