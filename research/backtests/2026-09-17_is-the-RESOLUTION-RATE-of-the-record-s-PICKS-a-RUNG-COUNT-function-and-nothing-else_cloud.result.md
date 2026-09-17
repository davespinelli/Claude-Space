# Idea 1232 (lane cloud, 2026-09-17) — is the RESOLUTION RATE of the record's PICKS a rung-count function and nothing else?

**VERDICT: KILL (capital) — and the queue's premise is REFUTED. Neither rate is a k function;
1209's four-ladder ordering is the GROSS degeneracy wearing a rung count.** 10 of 10 gates pass.

Pre-declared outcome, read on RESOLVED (the queue's statistic): **(C) NEITHER SEPARABLE** —
both spreads sit under the 0.10 bar. Read on MONO by the same pre-declared arithmetic:
**(B) IT IS NOT k ALONE** (dial spread 0.9524 > k-spread 0.6825 and > 0.10). Both are printed
below; neither is chosen.

## Construction

Three TEN-RUNG base ladders, each containing the record's committed anchor rung, so every k is
drawn from a ladder of the same length by the same rule:
`N [5,8,10,12,15,20,25,30,35,40]`, `H [21,42,63,84,126,168,210,252,315,378]`,
`GROSS [0.30 … 0.75]` (the record's own). Sub-ladders preserve rung order: all C(10,k) when
that is ≤ 24, else a seeded sample of 24 (`default_rng(1232)`). **15,246 ladder-decisions**
(3 panels × 14 folds × 3 dials × 121 sub-ladders), 662 resolved, 4,704 distinct bootstrap pairs
at L=63 / B=400. At k=10 there is exactly one sub-ladder per (panel, fold, dial), so that row
has n=42 against n=1,008 elsewhere.

## The two rates at matched construction and matched k

| k | 2/k! | MONO N | MONO H | MONO GROSS | dial spread | RES N | RES H | RES GROSS | dial spread |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 1.000000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0228 | 0.1121 | 0.0774 | **0.0893** |
| 3 | 0.333333 | 0.4593 | 0.4385 | 0.9802 | 0.5417 | 0.0149 | 0.0496 | 0.0724 | 0.0575 |
| 4 | 0.083333 | 0.2391 | 0.1220 | 0.9692 | 0.8472 | 0.0159 | 0.0169 | 0.0714 | 0.0556 |
| 6 | 0.002778 | 0.0417 | 0.0099 | 0.9524 | 0.9425 | 0.0218 | 0.0089 | 0.0714 | 0.0625 |
| 8 | 0.000050 | 0.0010 | 0.0000 | 0.9524 | **0.9524** | 0.0258 | 0.0000 | 0.0714 | 0.0714 |
| 10 | 0.000001 | 0.0000 | 0.0000 | 0.9524 | 0.9524 | 0.0238 | 0.0000 | 0.0714 | 0.0714 |

Pooled over dials: MONO 1.0000 → 0.3175, RESOLVED 0.0708 → 0.0317.

**Both rates FALL with k. 1209's ordering RISES with k.** So the ordering it read
(N 0/42 < H 6/42 < GROSS 40/42 < CADENCE 42/42, rung counts 6, 4, 10, 2) cannot be a rung-count
effect — at matched construction, more rungs make a ladder *less* monotone and *less*
resolvable, which is what the combinatorics (2/k!) and a fixed bootstrap bar both predict.

**What the ordering actually is: GROSS is k-INVARIANT on both statistics.** Its MONO rate is
0.9524 at k = 4, 6, 8 and 10 alike and its RESOLVED rate is 0.0714 at every k ≥ 3, while N and
H collapse toward the null. Against 2/k! the GROSS excess runs 2.94x (k=3) → 11.63x (k=4) →
342.86x (k=6) → 19,200x (k=8) → 1,728,000x (k=10); N tops out at 20x and H never clears 3.6x.
GROSS is not a ladder of books, it is ONE book re-levered (1189's degeneracy, replayed here as
its IS Sharpe spread: median **0.0006 at k=2 rising only to 0.0018 at k=10**, against N's
0.0424 → 0.1655 and H's 0.0881 → 0.2926). A monotone leverage-cost gradient is monotone at
every k by construction, and the bootstrap reads that gradient's tiny, near-deterministic sign
as separation.

Gate G6 confirms the mechanism the queue assumed — median IS Sharpe spread is non-decreasing in
k on every dial — so the *spread* really does grow with k. The rates still fall, because the
combinatorial and sampling penalties of a longer ladder outrun it.

By panel (`.bypanel.csv`), the same shape holds on all three; SMALL's RESOLVED runs
0.1091 → 0.0238 and U56's and B136's likewise. No panel carries the headline.

## Why the pre-declared (C) is not a finding of equivalence

Read honestly: **(C) fires because the RESOLVED rate is near zero in every cell** (0.0434
overall, 662 of 15,246), which bounds both spreads under 0.10 mechanically. It is not evidence
that k and construction are the same thing — MONO, the statistic with room to move, lands on
(B) with a dial spread of 0.9524. The queue's question gets a clean NO from MONO and a
"the bar never fires" from RESOLVED.

## Rule 8 walk-forward and both KEEP paths

Benchmarks (10 bps, t+1, post warm-up): U56 SPY 15.06% / 0.8815 / -33.72% (halves
0.9600/0.8171), OOS 15.15% / 0.8686; U56 live RULES v2 8.60% / 1.1982 / -12.05%.

**90 rung books: 4a 0; 4b full 18; 4b OOS 17; BOTH 16** — all on U56 and B136, all in the
standing 2026-09-04 candidate's neighbourhood (best U56 N=15: 17.07% / 1.1675 / -20.14%, halves
1.2596/1.1091, OOS 18.87% / 1.1894 / -20.14%). Nothing new.

54 stitched OOS curves per policy (3 panels × 3 dials × 6 k, equal-weight over that cell's
sub-ladders), every choice made on the fold's IS window only:

| policy | mean stitched OOS Sharpe | 4b OOS passes | U56 | B136 | SMALL |
|---|---|---|---|---|---|
| T_ALWAYS (tune every fold) | 0.8437 | 16/54 | 1.1156 | 0.9447 | 0.4708 |
| T_ANCHOR (never tune) | 0.8845 | 18/54 | 1.1759 | 1.0240 | 0.4534 |
| **T_RESOLVED** (tune only when the bootstrap separates the pick) | **0.8848** | **22/54** | 1.1749 | **1.0252** | 0.4544 |

`T_RESOLVED - T_ALWAYS` by k: +0.0163, +0.0270, +0.0352, +0.0511, +0.0568, **+0.0604** — the
resolution bar is worth more the more rungs you tune over, which is the one place k does carry
information.

**But T_RESOLVED is T_ANCHOR.** It fires at 0.005 of folds on N, 0.022 on H and 0.101 on GROSS;
on U56/N it fires at 0.00 and the curve is bit-identical to the anchor's. Its +0.0003 mean
Sharpe over T_ANCHOR is the GROSS cell, i.e. a re-levering. The anchor book is already the
standing 2026-09-04 KEEP 4b candidate, so **nothing is promoted**.

## Caveats

Rule 9 survivorship: B136 and SMALL are CURRENT constituents (SMALL: 663 investable of 715
after dropping 52 names with `max_1d_move >= 1.0` from `data/small_meta.csv`), so their levels
are biased high; the headline is a within-panel rate comparison across k, which the bias does
not move. The N and H ten-rung base ladders EXTEND the record's committed 6- and 4-rung
ladders — a declared construction choice, made so that every k is drawn from a ladder of equal
length; GROSS is the record's own, unextended. The k=10 row rests on a single sub-ladder.
Sub-ladder sampling at k = 3, 4, 6 is 24 of C(10,k); the seed is fixed and published.

Files: `.py`, `.console.txt`, `.decisions.csv.gz`, `.grid.csv`, `.monotonicity.csv`,
`.bypanel.csv`, `.books.csv`, `.walkforward.csv`, `.gates.csv`.
