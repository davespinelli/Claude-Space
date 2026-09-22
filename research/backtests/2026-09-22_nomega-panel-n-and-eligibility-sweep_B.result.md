# Idea 941 — can any U56 book clear 4b on the 36-name NOMEGA panel at any n or gross?
**lane B, 2026-09-22.  VERDICT: KILL (of the hypothesis that idea 933 under-searched).  ANSWER: the panel is 4b-EMPTY.**

Script `2026-09-22_nomega-panel-n-and-eligibility-sweep_B.py`; outputs `.grid.csv` (1120 rows, every cell),
`.legs.csv`, `.controls.csv`, `.walkforward.csv`, `.log.txt`.  Offline, deterministic, committed caches only.

## What was asked
Idea 933 removed `universe.json:megacap` (the 2026 top-20 held from 2009 — the record's most obvious answer key)
and found 4b dies on 0 of 12 cells, with the best rule-8 OOS Sharpe on the 36-name remainder at 0.873 vs SPY's
0.874.  But 933 swept only 6 fixed book FORMS x 30 gross rungs — it never moved book SIZE or ELIGIBILITY.  So the
record could not say whether NOMEGA is 4b-EMPTY (a panel fact) or merely UNSEARCHED (a search fact).

## What was run
Two TUNED parameters, protocol rule 4: **n** (book size, 7 rungs {3,5,8,12,18,24,ALL}) x **band** (the 200d MA
eligibility threshold, 5 rungs {0.00,0.02,0.03,0.05,0.08}).  Read at committed conventions, not fitted here:
gross {0.75 = live RULES v2, 1.00 = where every committed 4b pass on this family sits}, cadence {W = live, M},
cost {0,10,25,50} bps (10 bps binds).  Book = RULES v2 generalised by size: top-n by the record's own composite
among names inside the band, gross/n each, remainder to CASH.  `n=ALL, band 0.03, gross 0.75, W` reproduces live
RULES v2 exactly, so the live book is a cell of the grid.  U56 (56 names) is run through the **identical** sweep as
a capability control.  Controls on NOMEGA: EW36 (0 params), RULES v2 re-run on NOMEGA, RAND8 x 10 md5 seeds.

## Results (all 1120 cells published in `.grid.csv`)
| | NOMEGA (36) | FULL / U56 (56) |
|---|---|---|
| cells clearing **4b** (FULL **and** OOS) | **0 of 560** | 141 of 560 |
| cells clearing **4a** | **0 of 560** | 16 of 560 |
| 4b passes at 0 / 10 / 25 / 50 bps | 0 / 0 / 0 / 0 | 69 / 46 / 21 / 5 |
| rule-8 instances clearing 4b (of 16) | **0** | 7 |
| best OOS Sharpe anywhere on the grid | 0.9547 | 1.2803 |
| best OOS Sharpe reachable by a legal IS-only chooser | 0.8067 | 1.2702 |

**The binding leg is CAGR, not drawdown.**  NOMEGA @10 bps, 140 cells: 77 clear the OOS DD cap, 24 clear the OOS
Sharpe leg, **only 3 clear the OOS CAGR floor, and Sharpe ∩ CAGR = 0**.  The grid's best OOS Sharpe, 0.9547
(n=ALL / band 0.02 / g1.00 / M), is **above** SPY's 0.8751 and above 933's reported 0.873 ceiling — so on the
Sharpe leg alone 933 *was* too pessimistic — but that cell earns 7.57%/yr against a 10.70% floor.  The panel is
not Sharpe-empty; it is CAGR-empty.

**Matched-cell cost of deleting the sleeve.**  Over all 140 (n, band, gross, freq) cells matched between panels at
10 bps: FULL beats NOMEGA on OOS CAGR in **140 of 140** (12.16% vs 6.78%, gap **−5.38 pp/yr**) and on OOS Sharpe in
**140 of 140** (0.9877 vs 0.6988, gap **−0.2889**), while OOS MaxDD is **worse** on NOMEGA in 71 of 140 (−19.79% vs
−18.17%).  The mega-cap sleeve is not buying risk — it is the return, at every book size and every threshold.

**Rule 8, 2017–2026 read ONCE.**  Headline NOMEGA pick (W, g1.00, 10 bps) = n18/b0.05 → OOS **9.11% / 0.7992 /
−20.17%** vs RULES v2 OOS 9.46% / 1.2767 / −12.05% and SPY OOS 15.29% / 0.8751 / −33.72%.  No instance passes.

**Controls.**  EW36 OOS 11.18% / 0.8572 / −28.88% (only control to clear the CAGR floor; fails the DD cap);
RULES v2 on NOMEGA OOS 5.37% / 0.9109 / −10.49% (clears the DD cap by 9.7 pp, misses the CAGR floor by 5.3 pp);
RAND8 0 of 10, mean OOS Sharpe 0.2946 (sd 0.0973).  Every route to the CAGR floor on this panel spends the
drawdown budget; every route that keeps the drawdown budget misses the floor.

## What this run cannot do (stated, not repaired)
One book FAMILY (band-eligible top-n, cash remainder) — a different selector could in principle reach further,
though the 140-of-140 sign consistency of the panel gap argues it is the NAMES and not the form.  Two cadences
(W, M), one weekday phase, one MEGA20 definition (the committed list, which is itself the answer key being
deleted).  **SURVIVORSHIP (rule 9):** U56 is a current-constituent list, so every level here is optimistic; the
mega-cap removal deletes the sleeve whose membership is most obviously look-ahead, so a NOMEGA 4b FAIL is a
LOWER bound on the damage, not an upper one.  **RESIDUE, not a rules change** (rule 6; RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched): no KEEP, no PARK, no memo — the answer is a documented emptiness.
