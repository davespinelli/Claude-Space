# Idea 569 — name-the-CARRIER-that-survives-a-CHARACTERISTIC-MATCH (cloud, 2026-09-09)

**VERDICT: KILL of the carrier read for all four new candidates. NO CANDIDATE closes the
matched-level B-S gap.** One real by-product: `tpers` is the first characteristic in this line
that orders the premium monotonically with a high R² and a sign that survives rule 8 — but it
is the gate's OWN variable, it still leaves 0.61x of idea 568's origin gap standing, and it
produces no tradable book.

Script `research/backtests/2026-09-09_name-the-CARRIER-that-survives-a-CHARACTERISTIC-MATCH_cloud.py`
(229 s, 372 kernel draws, 4,464 draw books + 36 real books = 4,500).

## Gates

* **G1 PASS** — idea 312's committed 36 REAL rows reproduce at **2.2e-16 / 2.2e-16 / 4.4e-16**
  (B136 / SMALL439 / U56) over 13 columns; 4a and 4b flags 36/36. Published premium re-read
  U56 −0.0045 > B136 −0.0465 > SMALL439 −0.1023, **GAP +0.0978** exactly as pre-registered.
* **G2 PASS** — `fast_backtest` vs `engine.backtest` max |dreturn| **1.39e-17**.
* **G3 PASS** — idea 568's committed `origin.csv` mean matched B-S gap **+0.1961**, the
  pre-registered anchor.

## Design

Idea 568's machinery verbatim: pooled B136 (134 tradables) + SMALL439 on the common index
2010-01-04 .. 2026-09-04 (4,194 bars, 573 names); k = 36 kernel draws, bandwidth 0.5·sd (NOT
re-tuned); 6 seeds; POOL / BONLY / SONLY flavours; arms EWall (control) and MA-RS (200d gate,
re-spread at fixed gross); premium = Sharpe(MA-RS) − Sharpe(EWall) averaged over gross
{0.50, 0.75, 1.00} × cadence {W, M}. 10 bps, t+1 fills, no leverage/shorting. Two tuned
parameters only: **characteristic** and **target level**; levels pre-registered as the pooled
10/30/50/70/90th percentiles. 75 rungs planned, **62 feasible**, 13 infeasible and reported.

New per-name candidates (the queue's list): `mrho` (marginal pairwise rho), `beta` (to SPY),
`tpers` (1 − daily flip rate of the name's own above-200d-MA state = trend persistence of the
200d signal), `plevel` (log10 median close). `cvol` re-run as the idea 568 reference.

**SURVIVORSHIP:** B136 and the small panel are today's constituents. Everything below is a
statement about surviving names, not about a tradable 2010 universe.

## H_CARRIER — the answer

At a matched level, does the panel of origin stop mattering? Bar: every overlapping rung's
|premium(BONLY) − premium(SONLY)| inside the seed sd, **and** mean gap < 0.5 × idea 568's
+0.1961.

| char | rungs inside sd | mean B-S | × GAP | × idea 568 | H_CARRIER |
|---|---|---|---|---|---|
| mrho | 2/3 | **+0.0801** | +0.82 | +0.41 | **False** |
| beta | 2/4 | +0.0839 | +0.86 | +0.43 | **False** |
| tpers | 0/3 | +0.1204 | +1.23 | +0.61 | **False** |
| cvol (ref) | 0/1 | +0.1350 | +1.38 | +0.69 | **False** |
| plevel | 0/1 | +0.1420 | +1.45 | +0.72 | **False** |

**H_ANY FAIL.** Every candidate leaves a positive B-sourced-minus-S-sourced premium at matched
level, in the same direction, and every mean gap is at least 0.82× the entire published
three-panel gap the whole literature rests on. The sign never once reverses across 12
overlapping rungs. The closest thing to an absorber is `mrho` (2 of 3 rungs inside their own
seed sd, gap cut to 0.41× idea 568) — that is a *shrinkage*, not a closure, and it is measured
on the narrowest overlap in the run (BONLY reach [0.125, 0.337] vs SONLY [0.079, 0.274]).

Six characteristics have now been tried (ETF share, cvol, breadth, mrho, beta, tpers, plevel).
**The panel-of-origin effect is still unnamed.**

## H_CHAR / H_NOISE / H_PRED — one candidate does order the premium

POOL fits, required slope sign fixed in advance by the three real panels' own values:

| char | slope | R² | slope·span | ×GAP | sign OK | monotone | H_CHAR | H_NOISE | H_PRED |
|---|---|---|---|---|---|---|---|---|---|
| **tpers** | **+33.38** | **0.847** | **+0.7076** | **7.24** | yes | **up** | **True** | **True** | False (resid 0.0736) |
| mrho | −0.4867 | 0.149 | −0.1311 | 1.34 | no | – | False | True | False |
| cvol | −0.1442 | 0.057 | −0.0660 | 0.68 | yes | – | True | False | False |
| plevel | +0.0350 | 0.015 | +0.0350 | 0.36 | yes | – | False | False | False |
| beta | −0.0097 | 0.0004 | −0.0069 | **0.07** | yes | – | False | False | False |

`tpers` is monotone up on **all three** flavours (POOL +33.4 R² 0.847, SONLY +30.9 R² 0.793,
BONLY +16.4 R² 0.539) and spans −0.4059 to +0.2327 across five rungs — the premium changes
SIGN across the range. Nothing else in the record has done that. **But**: `tpers` is the
persistence of the 200d gate's own state, so "the MA gate pays where the MA state is
persistent" is close to a tautology, not an independent explanation; and it still fails
H_PRED (max |resid| 0.0736 vs the 0.03 bar) and H_CARRIER. `beta` is the flattest variable
ever measured here (R² 0.0004, effect 0.07× GAP) — beta is not it, at all.

Noise floor recomputed here: **within-rung seed sd 0.0798 = 0.82× the published GAP** (idea
312 got 0.0745), so the published three-panel ordering remains inside one draw's worth of
composition luck.

## Rule 8 walk-forward (IS ≤ 2016-12-31, OOS ≥ 2017-01-01, read once)

**WF-A** — slope sign holds IS → OOS in **9/13** (char, flavour) cells. `tpers` holds on all
three flavours and *strengthens* out of sample (POOL IS +21.37 R² 0.518 → OOS +39.08 R²
0.758); `beta` flips sign on 2 of 3 flavours; `mrho` flips on BONLY; `plevel` flips on SONLY.

**WF-B** — pick (char, level) by IS Sharpe alone at g=0.75/W POOL, then read OOS once. The
IS pick is **beta L=0.6021** (IS +0.9551); the OOS winner was **tpers L=0.9780** (OOS +1.0517,
IS rank 2). Selection loses again.

| book | CAGR | Sharpe | MaxDD | H1 | H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| WF-B pick (seed-pooled) | 9.12% | 0.895 | −26.77% | 1.082 | 0.781 | **8.79%** | **0.815** | **−26.77%** |
| RULES v2 (B136) | 7.62% | 1.082 | −12.24% | 1.126 | 1.040 | 7.98% | 1.119 | −12.24% |
| SPY | 14.13% | 0.862 | −33.72% | 0.891 | 0.858 | 15.45% | 0.882 | −33.72% |

WF-B **4a False**; **4b fails H2, OOS, DD and CAGR** — it loses to the live book on Sharpe and
to SPY on return, out of sample, on four legs at once.

## KEEP paths over all 4,500 books

**4a 23/4500 (0.51%) · 4b 63/4500 (1.40%) · BOTH 0/4500.** Binding 4b legs: DD 3,964 · H2
3,351 · OOS 3,312 · H1 2,879 · CAGR 2,607. 17 of the 23 4a passers are `EWall`, the *ungated*
control. Of the 60 draw-level 4b passers, **57 are BONLY** (large-cap-sourced) draws — the
origin effect shows up in the KEEP counts too, on a completely different statistic. Best 4b
passer `mrho~BONLY~L0.163402~4` EWall g=0.75/M (CAGR 14.54%, Sharpe 1.337, DD −20.15%, OOS
1.350) is a kernel draw, not a rule, and is not promoted. **No capital candidate, no memo.**

## Artefacts

`.grid.csv` (4,464 rows, every grid point) · `.rungs.csv` · `.origin.csv` · `.predict.csv` ·
`.walkforward.csv` · `.keeppaths.csv` (4,500 rows) · `.chars.csv` · `.namechars.csv` ·
`.console.txt`.

## Follow-ups proposed

1. `tpers` is the gate's own variable — price the premium against a persistence measure of a
   DIFFERENT signal (e.g. 12-1 momentum rank persistence) to test whether the R² 0.847 is
   information or tautology.
2. `mrho` halves the origin gap on the narrowest overlap in the run — widen the overlap by
   dropping k to 20 and re-measure whether the shrinkage is real or a reach artefact.
3. 57 of 60 draw-level 4b passers are BONLY at every characteristic — census whether the
   record's 4b pass rate is, everywhere, a panel-of-origin statistic.
