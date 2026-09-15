# Idea 970 (lane B, 2026-09-15) — does 4b SURVIVE a DISJOINT-HALVES SPLIT?

**ANSWERED = YES, IT SURVIVES — AND THAT IS THE PROBLEM. KILL for idea 942's clause (i) as a
repair to PROTOCOL 4b.** Making the halves disjoint from the rule-8 OOS window is a RESHUFFLE,
not a tightening: it destroys 2 and creates 2 of the rebuilt grid's 12 committed-style 4b passes
at 10 bps, leaves the coin flip's 4b base rate on the worst cell at **22.5%**, and leaves the OOS
leg exactly as redundant as 942 found it. Nothing promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched (rule 6). Script
`2026-09-15_does-4b-SURVIVE-a-DISJOINT-HALVES-SPLIT_B.py`, **GATES 8 of 8**.

## What was asked
Idea 942 found 4b's H2 window **100.0% contained inside** its rule-8 OOS window and proposed,
without applying, CLAUSE (i): take the 4b halves inside 2009–2016 and leave OOS untouched, or drop
the halves entirely. The queue asked which of the record's committed 4b passes clause (i) creates
and which it destroys.

## What was measured
- **THE GRID.** 3 panels (U56 / B136 / SMALL663) × 5 books (TOP5 / TOP10 / TOP20 / EWELIG /
  BAND03) × 4 gross (0.50 / 0.65 / 0.75 / 1.00) × 3 cadences × 5 cost rungs = **900 book rows**,
  each scored under **three split rules**: `REC` (the record's overlapping convention), `DISJ`
  (clause (i) form A) and `TWOLEG` (clause (i) form B). `L_DD` and `L_CAGR` are full-sample under
  all three, so every difference between the columns is a difference in the SHARPE legs alone.
- **THE CENSUS.** 918 eligible committed `.csv` artifacts, 339,204,825 bytes, 1,087,557 rows,
  sha `4d4cbbd`; **98,091 committed 4b PASS rows** after excluding the record's own coin-flip
  artifacts. STRICT re-prices 49 rows / 24 cells, WIDE 27,143 rows / 106 cells.
- **THE NULL.** 3 panels × 3 cadences × **200 gross-matched rotating coin flips** = 1,800 null
  books (idea 680/926/931/942's RANDROT unmodified), scored at 10 bps under all three split rules.
- **TUNED: 2.** SPLIT RULE (3 levels) and CADENCE (3 levels), every point reported, neither ever
  chosen. Panel, book, gross and cost rung are reported constants. CLAIM SET {STRICT, WIDE} is not
  a tuned dial — both are always printed and the honest answer is the interval between them.

## The answer
**On the whole rebuilt grid at 10 bps (180 book rows): REC 12 4b passes → DISJ 12 (2 destroyed,
2 created) → TWOLEG 14 (0 destroyed, 2 created).** Same shape at every rung except 50 bps. `H_SYM`
**PASS** — creation and destruction are balanced, which is what a reshuffle looks like.

**On the record, cell-weighted at 10 bps: STRICT 1 of 5 reproduced passing cells destroyed, 0
created; WIDE 2 of 8 destroyed, 2 created (net 0).** `H_DESTROY` **FAIL** at 0.062 against a
pre-registered 0.25 bar.

**ROW-weighted, WIDE destroys 4,335 of 6,412 (67.6%) — and 4,094 of those 4,335 rows are ONE
CELL.** The row-weighted number is a citation-count artefact, not a fact about the record; it is
reported here only so that nobody re-derives it as a headline. This is idea 951's file-weight /
row-weight lesson reproduced on a different object.

## The one cell clause (i) kills is the one cell 942 said was clean
The single STRICT committed pass destroyed at 10 bps is **`U56 / TOP20 / g0.75 / WEEKLY`** — the
standing candidate's weekly cell, which idea 942 named as *"the only pass on the grid that survives
its own null"* (0.0% weekly null base rate). Full sample 12.60% / 1.088 / −18.31%, halves under the
record's split **1.094 / 1.089**, OOS 14.24% / 1.160. Under a disjoint split its 2009–2012 half
reads **0.757** and it fails on `L_H1` alone. The pass that survived the null does not survive the
calendar.

## Clause (i) does not buy back discriminating power — both diagnostic hypotheses FAIL
- `H_NULL` **FAIL.** Gross-matched coin-flip 4b base rate, REC → DISJ → TWOLEG: **U56/M 0.405 →
  0.225 → 0.405**, B136/M 0.080 → 0.045 → 0.085, U56/Q 0.070 → 0.060 → 0.070, B136/Q 0.015 → 0.020
  → 0.025. Median ratio **0.710** against a 0.50 bar. Disjoint halves roughly halve the worst cell
  and leave a coin flip clearing 4b **more than one time in five**.
- `H_INDEP` **FAIL, 1 of 4 defined cells.** P(all 5 legs)/P(the other 4) under DISJ is **1.0000**
  on U56/M and U56/Q and 0.9000 on B136/M. Even with the windows made disjoint, **dropping the OOS
  leg still changes almost no verdicts** — 942's redundancy finding is not a window-overlap
  artefact, it is a property of the books that reach the other four legs.
- What the split *does* change is the correlation it was aimed at: over 900 book rows
  **corr(H2 Sharpe, OOS Sharpe) falls 0.9878 → 0.8022**, and per-cell leg agreement falls from
  0.83–1.00 to 0.33–1.00. The windows genuinely separate; the verdict does not move with them.

## Rule 8 (walk-forward) and both KEEP paths
(book, gross) chosen on **2009–2016 alone** by 3 IS-only choosers × 3 panels × 3 cadences = **27
picks**, 2017–2026 read once (G6: picks invariant to permuted OOS rows, 0 mismatches).
**OOS 4b 4 of 27 and OOS 4a 0 of 27 — identical under all three split rules.** Best pick
`U56/W/CH_SHARPE → BAND03 @ g1.00`: OOS **12.68% / 1.276 / −15.91%** against **SPY OOS 15.27% /
0.874 / −33.72%** and **RULES v2 OOS 9.46% / 1.277 / −12.05%**. It is the live book levered to
100% gross — full-sample Sharpe 1.2011 against the live 1.2013 — so it clears 4b and **fails 4a**
on drawdown (−15.91% vs −12.05%) and buys its CAGR with gross, not with skill. Full-sample 4a is
**1 of 180** rows at 10 bps (SMALL663/BAND03@0.50/M, Sharpe 0.731) under every split rule.
**Nothing here is a KEEP on either path.**

## Gates, 8 of 8 — and a correction the record can use
G1 closed-form runner ≡ `engine.backtest` 8.33e-17. G2 BAND03@0.75 ≡ `rules_v2_weights` 0.000e+00.
**G3a reproduces 942's window overlap exactly (H2 100.0% inside OOS, OOS 91.2% H2).
G3b/G3c reproduce BOTH committed U56/TOP20/M OOS triples on one tree: the DE-GROSS construction
reads 16.67% / 1.282 / −19.51% (idea 951's committed 16.67% / 1.283 / −19.51%) and its RE-SPREAD
twin reads 17.53% / 1.305 / −19.51% (idea 942's committed 17.53% / 1.305 / −19.51%). The record's
two committed triples for "the same cell" are idea 944's G3b de-gross / re-spread split and nothing
else — neither is a vintage drift.** G4 gross match Δ2.22e-16 / Δcount 0 / turnover 9.28x.
G5 determinism 0.000e+00. G6 IS-only choosers, 0 mismatches. G7 disjointness: under DISJ all three
window intersections are 0 rows on all three panels, while REC's H2∩OOS is 2,222 days (U56/B136)
and 1,969 (SMALL663). G8 census corpus stamped.

## What this proposes (for Sunday review; NOT written into PROTOCOL.md — rule 6)
Clause (i) is worth adopting for HONESTY and is worth nothing for POWER, so it should be adopted
as a labelling rule and not sold as a fix:

> *"PROTOCOL 4b — the halves are taken inside the in-sample window and the rule-8 OOS window is
> read once and separately. A 4b verdict is reported as THREE legs (IS-H1, IS-H2, OOS) and never
> as five, and the OOS Sharpe leg is reported as NON-CERTIFYING wherever its own cell's
> gross-matched null clears it above 0.90. Disjointness is a reporting requirement; it is not
> evidence, and a 4b pass under disjoint halves carries no more weight than one under the old
> convention."*

Cost of adoption as measured here: **1 of 5 re-priceable committed passing cells at 10 bps loses
its pass (the standing candidate's weekly cell), 2 of 8 under the generous claim set, and 2 cells
gain one.** No committed KILL becomes a KEEP.

## Survivorship (PROTOCOL 9)
U56 / B136 / SMALL663 are current-constituent lists, so every CAGR and drawdown LEVEL is optimistic
and every null base rate is an UPPER bound. The created/destroyed contrast is the SAME books on the
SAME tape under two window definitions and is untouched by it; the 4b LEVELS, read against SPY, are
not protected.
