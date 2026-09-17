# Idea 1188 (lane C, 2026-09-17) — how many committed SUB-TAPE FIGURES move once the LADDER is RESOLVED rather than FROZEN?

Script `2026-09-17_how-many-committed-SUB-TAPE-FIGURES-move-once-the-LADDER-is-RESOLVED-rather-than-FROZEN_C.py`.
Two tuned dials (CLAIM SET x LADDER = 15 cells, all published in `.grid.csv`). GATES 10 of 10.
Tape pinned at 2026-09-15. NO BOOTSTRAP, declared: a resample destroys a sub-tape object, so the
resolution measure is a jackknife.

## ANSWERED: 1,991 OF 8,479 (0.2348) — (A) BY THE DECLARED BAR, AND THE BAR IS MET BY WIDTH, NOT BY STABILITY

Of the record's re-derivable LADDER-DEPENDENT committed sub-tape figures, **1,991 of 8,479
(0.2348)** move by more than their own leave-one-rung-out jackknife SE when the ladder is resolved
from the one they were published on to L8. The pre-declared bar for **(A) THE RECORD IS ROBUST**
was < 0.25, so the scored verdict is (A) — by a margin of **0.0152**, and the three second
readings straddle the bar: J_GROUP @L_pub **0.1935**, J_GROUP @L **0.2374**, J_LADDER @L
**0.2658**. The verdict is reported as declared and not relabelled; what follows is why it should
not be read as "the record's sub-tape numbers are stable".

**The SE bar is enormous.** The median committed figure's OWN jackknife SE is **0.5463 of its
published value**; 0.8832 of figures have an SE above 10% of the value, 0.7088 above 25%, 0.5208
above 50%, and **0.3649 have an SE larger than the number itself**. A figure that does not move
beyond that bar has not been shown to be stable — it has been shown to be unresolved.

**On an SE-free reader's bar the same figures move a great deal.** At L8: **0.5683 move by more
than 10%**, 0.4049 by more than 25%, 0.2397 by more than 50%, 0.0947 by more than 100%. Median
relative move **0.1523**, p90 **0.9721**, max 226.4.

**The LADDER dial moves the answer; the CLAIM SET dial does not.** Share moved runs L2 **0.5435**,
L3 0.2769, L4 0.2630, L6 **0.2033**, L8 0.2348 — and going COARSER (L2) moves more than twice as
much as going finer. C_STRICT and C_WIDE give the identical numerator and denominator at every
ladder, because every re-derivable ladder-dependent figure in the record belongs to the
1140→1148→1157→1158 ratio lineage; the one other ladder-dependent source (1160's gross family,
972 figures) is 0 of 972 re-derivable, its mech/lam construction being outside this kernel.

## THE RECORD'S OWN HEADLINE FIGURE, TRACED

1148's committed SMALL / MAXDD / R_MATCHED, **published 0.794259**, on its own as-published repair:

| ladder | value | move vs published | own J_LADDER SE at that ladder |
|---|---|---|---|
| L2 | 1.4621 | +84.08% | n/a (one non-unit rung) |
| L3 (as published) | 0.794259 | 0.00% | **0.3683** |
| L4 | 0.5751 | −27.59% | 0.1688 |
| L6 | 0.5503 | −30.72% | **0.0311** |
| L8 | 0.4678 | **−41.10%** | 0.0543 |

Its 41% move does **not** clear its own L3 SE of 0.3683 — because that SE is 46% of the number.
The finer ladders are 7–12x better resolved. (1158 published 1.173714 for the same cell at L8
under the R_COUNT repair; 0.4678 is the same cell at L8 under the repair 1148 actually used. Both
are in `.surface.csv`; the gate replays both to 2.6e-08 and 1.5e-07.)

## COVERAGE — WHAT "WHOSE CITED SCRIPT CAN BE RE-RUN" ACTUALLY COSTS

68,526 committed sub-tape figures harvested from 6 committed CSVs. **65,373 (0.9540) re-derivable**
at replay tier T_EXACT/T_TIGHT; C_STRICT 13,015 of 15,066 (0.8639). Per source: 1158's `.grid.csv`
**9,720 of 9,720 bit-for-bit (all T_EXACT)**; 1157's `.subtapes.csv` 2,916 of 2,916; 1148's
`.subtapes.csv` 49,442 of 49,572; 1148's `.cells.csv` 699 of 972; 1148's `.perrung.csv` 2,596 of
4,374; 1160's `.ladder.csv` **0 of 972**. 55,598 re-derivable figures are ladder-INVARIANT
(per-fraction LEVELS): they cannot move, and their entire residual (max 9.9e-05) is the replay
tolerance — 1161's object-dependence from a third direction.

## THREE DEFECTS, TWO OF THEM THIS RUN'S OWN, ALL PRICED RATHER THAN HIDDEN

1. **This run's first cut read C_BOOK as "one group per book"** and replayed 197 of 4,860 of 1158's
   C_BOOK figures. 1158's C_BOOK is the ANCHOR book (ladder N, rung 20). Corrected: 9,720 of 9,720.
2. **This run's first cut used 1158's between term everywhere** and replayed **0 of 1,458** of
   1148's per-rung R_SD figures. 1157's `ratio_from` — the one 1148 was written with — uses the SD
   of the fraction medians for R_SD's between term, not the endpoint range. Corrected.
3. **Not this run's: 1148's per-rung R_MATCHED replays at 6 of 1,458.** R_MATCHED is the family's
   HEADLINE within term and it carries a 200-pair Monte-Carlo draw. A Monte-Carlo statistic
   published without its draw order is not reproducible from the committed artefact. The pooled
   cell is replayable (G5, bit for bit at 0.794259) only because 1158 recovered the loop order.

## CENSUS

**30 committed `frac`/`fracs`/`frac_ladder` columns across 28 CSVs, and exactly 15 (0.5000) are
SUB-TAPE denominators** (42,483 rows). The other 15 (2,423 rows) use the same column name for an
entirely different object — window fraction, share of names, ADV fraction, within-family pass
share. Any census that counts `frac` columns without checking their semantics double-counts the
files. PROSE: **212 sub-tape sentence-rows carrying 96 numbers; 0.2075 of rows state a ladder**
and 0.7604 of the numbers are locatable on this run's surface. The prose census excludes this
run's own write-up, QUEUE entry and LEADERBOARD rows by name; the three follow-up ideas it filed
(1190-1192) are the only self-reference left in it and are worth 2 rows.

## RULE 8 + BOTH KEEP PATHS — 81 rung books, every one published

Benchmarks (pinned): U56 SPY 15.10% / 0.8829 / −33.72% (OOS 15.21% / 0.8711), v2 8.62% / 1.2008
(1.2322 / 1.1760) / −12.05%; B136 SPY 15.16% / 0.8861, v2 7.98% / 1.0993 / −12.24%; SMALL SPY
14.06% / 0.8581, v2 4.30% / 0.6637 / −13.89%.

**4b full 16 of 81, 4b OOS 17, 4b BOTH 15, 4a 0 of 81** (U56 10 / 11 / 0, B136 6 / 6 / 0,
**SMALL 0 / 0 / 0 on every path**) — an independent reproduction of 1158's 16 / 17 / 0 on the same
grid. 4a fails on A_H2 at 79 of 81 and on A_DD at 74 of 81.

**NO NEW CANDIDATE, AND THE REASON IS ARITHMETIC AGAIN:** 10 of U56's 16 passing reads are one
book. CADENCE=W, H=126, GROSS=0.75 and N=20 are the SAME anchor book by construction, and the
GROSS ladder 0.50 → 0.75 moves its Sharpe **1.1389 → 1.1397, a spread of 8e-04 over a 1.5x change
in gross** — idea 1189's degeneracy reproduced from a fourth direction. The genuinely distinct
passers are U56/N=12, U56/CADENCE=Q, B136/N=15 and B136/N=10; none clears 4a. Best 4b (full AND
OOS) U56/N=12: full 17.71% / 1.1692 / −20.17% (H1 1.2753 / H2 1.0885), OOS 18.89% / 1.1759 /
−20.17%.

**RESOLVING THE LADDER MOVES THE PICK AT 2 OF 3 PANELS AND NEVER FOR THE BETTER.** IS-only
choosers, OOS read once: U56 CH_PUB N=8 → CH_RES N=10 (OOS Sharpe 1.0797 → 1.0954); B136 unmoved;
SMALL CH_PUB CADENCE=D → CH_RES N=5, and the resolved pick is strictly **worse** — OOS Sharpe
0.3633 → 0.1972, OOS MaxDD −38.31% → −50.70%. **0 of 9 picks clear 4a; 0 of 9 clear 4b full AND
OOS.**

## VERDICT

**KILL as a capital finding.** The free parameter has documented reach over the record's published
numbers and no capital content: no pick it moves clears either KEEP path, and the run's only 4b
reads are the standing incumbent and its degenerate gross rungs. Nothing enacted (rule 6); no memo.

A PROTOCOL clause is **PROPOSED, NOT ENACTED**: *a published sub-tape figure must state its
fraction ladder and its own resolution, and a Monte-Carlo sub-tape statistic must state its draw
order or be published in its exact-pair form.* On this run's numbers the first half costs nothing
(the ladder is already in the CSV for 15 of 30 columns) and the second half is what separates 6 of
1,458 reproducible per-rung headline figures from 1,458.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are current-constituent lists; SMALL is the current output of a sub-$2B screen less
the documented `max_1d_move >= 1.0` exclusion (715 listed, 52 dropped, 663 served). Every LEVEL is
optimistic and every 4a/4b count is an UPPER bound. The run's own object is a ratio of two spreads
in the statistic's own units and is far less exposed, but MAXDD is the family's headline statistic
and a survivorship-flattered panel has a shallower drawdown path, so the levels are published
beside every ratio in `.surface.csv` and `.levels.csv`.
