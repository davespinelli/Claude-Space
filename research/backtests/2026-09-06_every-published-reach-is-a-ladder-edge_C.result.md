# idea 256 — every published reach is a ladder edge until proven otherwise (lane C, 2026-09-06)

**VERDICT: ANSWERED — the queue's worry is CONFIRMED as a description of the record and KILLED as a
source of return.** 87.4% of the record's 22,443 readable argmaxes sit at a grid END (2/L null
34.4%, excess **+52.9pp**), and only **42.2%** of the edge grids have ever been re-run wider by a
later script. But widening the grid moves the ANSWER without moving the OUTCOME: across 30
walk-forward cells the argmax leaves the record grid in 43.3% of them for a mean OOS Sharpe of
**+0.018 (t +0.91, 8/30 wins)**. No new book, no KEEP candidate, no RULES change; RULES.md,
scan.py, bot.py and baseline.py untouched. One REPORT-ONLY PROTOCOL clause is proposed.

## Part A — the census (mechanical, over the committed corpus)

723 committed `research/backtests/*.csv[.gz]` → 715 after de-duplication by content hash → **22,443
readable cells** over 87 artefacts, 61 scripts, 21 distinct dial names, 100 (file, dial) grids. A
cell is a fully-crossed group holding exactly one row per grid level; ragged designs contribute
nothing. Higher is better for all three outcome families (MaxDD is stored negative), so an argmax
covers the idea's "argmax **or argmin**" — a floor on a loss is an argmax of MaxDD.

| statistic | Sharpe | CAGR | MaxDD | ALL |
|---|---|---|---|---|
| cells | 8338 | 6642 | 7463 | 22443 |
| argmax at a grid END | 0.822 | 0.890 | 0.917 | **0.874** |
| 2/L null (a random argmax) | 0.356 | 0.337 | 0.337 | 0.344 |
| excess over null | +0.466 | +0.553 | +0.580 | **+0.529** |
| response MONOTONE (never turned over) | 0.618 | 0.722 | 0.678 | 0.669 |

Decomposition of the 87.4%: **66.9% monotone** (the ladder never turned over — the published number
is the ladder end and nothing else), **20.5% edge-but-turning** (the response has an interior
turn, the best value is still at an end), **12.6% interior argmax**. Unit-weighted (one unit =
script stem × dial × outcome family, so a 1485-row artefact cannot outvote thirty small ones):
234 units, mean edge **0.828** vs null 0.398 (+0.430); **127/234 units (54.3%) are at an edge in
EVERY cell they publish**, 10 units (4.3%) never.

The rate is not an artefact of cost rungs, where an edge is expected because more cost is always
worse: those (`cost`/`cost_bps`/`bps`, 5012 cells) run 0.974, and **every other dial still runs
0.845 against a 0.298 null**.

By dial name (unit-weighted; `m` is 51 units over 17 scripts at edge 0.794 vs a 0.180 null — the
single largest block; `n` 22 units 0.696 vs 0.526; `g` 18 units 0.963 vs 0.353; `k` 15 units 0.726
vs 0.578; `share` is the one clean exception at 0.180 vs 0.151). Full table in `.census.csv`.

**Has anyone ever re-run the grid wider?** Of the 100 (file, dial) grids, **90 are edge grids**
(argmax at an end in >50% of their cells). Matching on dial name across scripts:

| | ever wider (any date) | wider by a LATER script | strict superset |
|---|---|---|---|
| all 100 grids | 72.0% | 41.0% | 62.0% |
| the 90 EDGE grids | **73.3%** | **42.2%** | 65.6% |

So the answer to the queue's question is **42.2%**: fewer than half of the record's edge-argmax
grids have ever been re-swept wider by a later run, and **26.7% have never been swept wider by
anybody, in either direction, at any date**.

## Part B — does widening change the answer, and is the change worth anything?

Three dial families on the committed composite book (constant-gross top-n, gross/count — idea
244's NORM channel, so an `n` sweep is not a disguised gross ladder), weekly, t+1, engine-executed.
**Exactly one tuned parameter**: the dial's level, chosen by IS Sharpe on ≤ 2016-12-31. Carried
axes, never selected on, every level reported: panel {u56, broad136, small484}, cost rung {10, 25}
bps, and n ∈ {5, 20} when n is not the swept dial. 228 grid points, 30 walk-forward cells.

| family | record grid | extended grid | narrow pick at an edge | pick MOVES out | mean ΔOOS Sharpe | ext. OOS spread |
|---|---|---|---|---|---|---|
| `n` | {5,10,20} | 2…56 / 136 / 484 | 6/6 | **6/6** | **+0.181** | 0.558 (max 0.881) |
| `max_vol` | {0.4,0.6,0.8} | 0.20…1.50, off | 10/12 | 6/12 | −0.046 | 0.241 (max 0.525) |
| `gross` | {0.5,0.75,1.0} | 0.20…1.00 | 11/12 | 1/12 | 0.000 | 0.009 (max 0.034) |

**The three rates the idea is about** (30 cells): record-grid IS argmax at a grid END **90.0%
(27/30)**; widening moves it outside the record grid **43.3% (13/30)**; and the widened argmax is
**itself** at the extended grid's end in **46.7% (14/30)** — widening relocates the edge about as
often as it resolves it.

**The price of the move.** OOS Sharpe (wide pick − narrow pick): mean **+0.0178**, median 0.000,
sd 0.107, **t +0.91**, wins 8/30. Restricted to the 13 cells where the pick actually moved: mean
+0.041, median +0.003, wins 8/13. The `n` family pays (+0.181, 6/6 moved, and u56 n: 20 → 56 takes
OOS Sharpe 0.993 → 1.113); `max_vol` costs (−0.046); `gross` is decision-irrelevant — its whole
extended ladder spans **0.034 of OOS Sharpe at most**, so its 11/12 edge argmaxes are real,
monotone and worth nothing.

**Rule 8 / KEEP paths.** Baselines on the OOS window: RULES v1 @10bps OOS Sharpe 0.747 (u56) /
0.576 (broad136); SPY OOS CAGR 15.5%, Sharpe 0.882, MaxDD −33.7%. **4b passes: 0/30 narrow picks
and 0/30 wide picks.** 4a: 7/30 narrow, 4/30 wide. At the grid-point level 3 of 228 points pass 4b
and **all three lie outside the record grid**:

| point | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe |
|---|---|---|---|---|---|
| u56 · n=20 · max_vol=1.50 @10bps | 10.7% | 0.991 | −19.5% | 1.039 / 0.961 | 1.029 |
| u56 · n=20 · max_vol=off @10bps | 10.7% | 0.993 | −19.5% | 1.039 / 0.966 | 1.033 |
| broad136 · n=136 (EWall) @10bps | 10.7% | 1.025 | −17.7% | 1.143 / 0.915 | 1.019 |

Inside the record grids: 90 points, **0 pass 4b**, best OOS Sharpe 0.993. Outside: 138 points, 3
pass, best OOS Sharpe 1.114. That gap is the strongest form of the idea's claim — but **none of
the three is a new object**: n=136 on broad136 *is* EWall, and "no vol gate at n=20" is ideas
38/49/232. They reproduce known record objects that the record's own sweep grids happen to
exclude, and the IS chooser does not select any of them, so **no KEEP is claimed from this run.**

## Pre-registered predictions, scored
* **P1 ✓** reproduction: cost identity 0 bps + turnover → 10 bps vs a genuine engine 10 bps run,
  max|d| **0.000e+00**; realised gross at n=5, g=0.75 exactly 0.7500.
* **P2 ✓** the `n` record grid's IS argmax is the top level (20) in 6/6 cells and the extended
  argmax is above 20 in 6/6 (28, 136, 40, 40, 56, 56).
* **P3 ✓** the gross ladder's extended OOS-Sharpe spread is < 0.15 in every cell (max 0.034).
* **P4 ✗ / ✓** the first clause is WRONG: `max_vol`'s IS argmax sits at the loose end in only 2/8
  large-cap cells (the n=5 books pick the TIGHT end, 0.40, on both large-cap panels). The second
  clause holds: 0.80 → off moves OOS Sharpe by ≤ 0.046 everywhere.
* **P5 ✓** the decisive one: widening moves the answer (43.3%) far more often than the outcome
  (mean +0.018, t +0.91, not significant).
* **P6 ✓** no new 4b KEEP from any widened pick, on any panel.

## What this means for the protocol (report-only, for Sunday review — not a rules change)
A grid-end argmax is a **reportable defect in a published number**, not a discarded profit. The
census shows the record cannot tell the two apart today, and the cheap fix is a column, not a
re-run: **beside every published argmax, print `edge=lo|hi|interior` and the outcome spread across
the whole ladder.** An edge with a 0.03 spread (`gross`) is noise; an edge with a 0.88 spread
(`n`) is an unfinished sweep. The second half of the fix is a floor on re-runs: the 26.7% of edge
grids that nobody has ever widened are the ones whose published ceilings are unaudited.

## Caveats carried, not buried
* SURVIVORSHIP: u56, broad136 and small484 are current-constituent lists (idea 54). Every LEVEL
  inherits it; the narrow-vs-wide COMPARISON is matched and does not.
* The census matches dials **by name** across scripts. `n` means book size throughout this record;
  `k`, `m` and `g` need not, so a name-matched "wider re-run" can be a different dial with the same
  letter. Per-dial file and script counts are printed so the reader can discount, and Part B's
  three families were chosen from the unambiguous names.
* Only dials that reached a committed CSV are visible. Ladders printed to console or discussed in
  a memo are invisible: every count is a floor, not a ceiling.
* The dial detector is name-blind except for one printed diagnostic blacklist; near-duplicate
  artefacts differing by one column survive de-duplication as two units, which is why every rate
  is also reported unit-weighted.
* `gross` is capped at 1.00 by PROTOCOL rule 2 (no leverage). That end is **unwidenable by
  protocol** — a third category the idea's dichotomy misses, and the reason 11/12 of its cells are
  edge picks that no re-run can move.
* On small484 SPY is dropped from the selectable set (it is a joined benchmark there, not a
  constituent); on u56 and broad136 it is left eligible exactly as the incumbent has it.
* Idea 38 (calendar-day index after 2014-09-17) and idea 126 (t+1 execution only) carry over.

Artefacts: `.py`, `.console.txt`, `.census.csv`, `.cells.csv.gz`, `.widen.csv`, `.grid.csv`,
`.walkforward.csv`, `.keep.csv`. Runtime 206s, deterministic, no seed anywhere.
