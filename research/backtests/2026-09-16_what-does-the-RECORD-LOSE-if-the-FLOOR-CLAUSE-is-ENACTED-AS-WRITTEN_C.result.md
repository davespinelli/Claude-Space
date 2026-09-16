# Idea 1110 (lane C, 2026-09-16) — what does the RECORD LOSE if the FLOOR CLAUSE is ENACTED AS WRITTEN?

**ANSWERED. The clause as written costs the record 64% of its argmax content at q=0.90 — and
both alternatives the queue asked to price against it are WORSE, one of them dominated
outright. AS_WRITTEN STANDS as the best ENACTABLE form. It remains PROPOSED, not enacted
(PROTOCOL rule 6). Nothing promoted, no RULES change, no PROTOCOL edit.**

Script `research/backtests/2026-09-16_what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN_C.py`,
14 CSVs, console log, 4 LEADERBOARD rows. Gates 9 of 9.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

CLAUSE FORM {AS_WRITTEN, ANNOTATED, WIDER_RUNGS, LONGER_TAPE} x CONFIDENCE q {0.80, 0.90, 0.95}
= 12 combinations, ALL published, plus two variants reported beside their headline and never
selected on (WIDER_RUNGS_ENDS, LONGER_TAPE at M = 4 and 8). PANEL, LADDER and STATISTIC are not
dials: all 2 x 4 x 4 = 32 CORE cells are reported everywhere. BLOCK LENGTH is not a dial (L=63
throughout, 1098/1102/1108's headline). Everything else frozen at 1082/1094/1098/1102/1108's
construction. Seeds are `zlib.crc32` — 1108's repair of 1102's process-random `hash()` seeds.

## HOW EVERY FORM IS SCORED — pre-registered, before any number

A published argmax claim on a k-rung ladder is an ASSERTION SET: it names a set S that may hold
the optimum and EXCLUDES the other k - |S| rungs. Two numbers per cell, and no others:

- **DECIDED** = k - |S|, the rungs actually ruled out. CONTENT = DECIDED / (k - 1).
- **EXP_FALSE** = sum over excluded j of (1 - A_peak,j), A from the block bootstrap — the
  expected number of WRONG exclusions the clause publishes.

ERR = EXP_FALSE / DECIDED; **PRICE = DECIDED / EXP_FALSE** is "decidable claims per unit of
honesty" read literally. DECISION RULE, fixed in advance: among the forms CALIBRATED at q
(ERR <= 1 - q), the answer is the one with the most DECIDED rungs.

## THE ANSWER (q = 0.90, 32 CORE cells, 184 decidable rungs)

| form | DECIDED | CONTENT | EXP_FALSE | ERR | PRICE | contentless cells | calibrated |
|---|---|---|---|---|---|---|---|
| ANNOTATED (point argmax + gap + floor) | 184 | 1.000 | **34.34** | 0.1866 | **5.4** | 0 | **NO** |
| LONGER_TAPE M=2 (**PROJECTED**) | 90 | 0.489 | 1.60 | 0.0178 | 56.1 | 10 | yes |
| **AS_WRITTEN (the clause)** | **66** | **0.359** | **1.41** | **0.0213** | **46.9** | **18** | **yes** |
| WIDER_RUNGS (every 2nd rung) | 39 | 0.212 | 0.96 | 0.0245 | 40.8 | 19 | yes |

At q = 0.80 / 0.95 the clause retains 0.516 / 0.293 of the content and leaves 8 / 23 cells
contentless. **The literal decision rule answers LONGER_TAPE at q = 0.90 and 0.95 — and that
answer is unattainable:** M = 2 is 34 years of tape on panels that start in 2008, the
projection's bias runs TOWARD resolution, and the tape multiple a cell actually needs for its
own committed gap to clear its own floor has median **12.5x = 220 years**, with 8 of 32 cells
not clearing at M <= 500. Among ENACTABLE forms, AS_WRITTEN wins on content AND on price.

## BOTH QUEUE ALTERNATIVES, KILLED ON THEIR OWN TERMS

- **H_ANNOT_PRICE FAILS, and its failure is the result.** Publishing the argmax as a point with
  its gap and floor beside it was expected to buy content at a defensible rate. It does not: it
  buys 2.8x the content at **24x the wrong exclusions** (34.34 against 1.41), PRICE 5.4 against
  46.9. It is not a trade, it is dominated. Per cell it is calibrated at NO confidence — 24 / 26
  / 26 of 32 cells exceed their own bar at q = 0.80 / 0.90 / 0.95.
- **H_COARSE_LOSES PASSES.** Widening the rungs decides 39 against 66: what coarsening gains in
  gap it loses in the mean 2.50 rungs per cell it can no longer speak about (ENDS-only: 10).
- **H_TAPE_HALF PASSES.** The floor's tape scaling is MEASURED on disjoint sub-tapes, not
  assumed: median fitted beta over the 24 non-DD cells **-0.4540** against 1/sqrt(T)'s -0.50.
  DD is exempt by declaration and runs the other way (+0.2093) — a path functional's own level
  grows with the tape.

## D1 — A CORRECTION TO 1102, AND IT RUNS AGAINST THE CLAUSE

1102's committed `tie_set` column is `mass_set(counts, rungs, 0.90)`: the smallest CONTIGUOUS
set of rungs carrying 0.90 of the bootstrap ARGMAX MASS, computed once at a fixed 0.90 and
written into every q row. That is not the set the clause publishes, and it never consults q —
**it moves between q = 0.80 and 0.95 in 0 of 32 cells while 1102's own capped floor moves in
15.** The premise's "4.88 rungs / 0.851 of its ladder / 12 WHOLE-LADDER" reproduces EXACTLY as
that mass-set figure over the 26 TIE cells only. The clause's own FLOOR set, over all 32 cells
at q = 0.90: mean **4.69 of 6.75 rungs (0.787)**, **18 of 32 CONTENTLESS**, and it does move
with q (17 of 32 cells; 3.78 / 4.69 / 5.06 rungs). Enacted as written the clause costs MORE
than 1102 published.

## D2 — A CORRECTION TO THIS RUN'S OWN DECISION RULE

The rule declared in (f) tests the AGGREGATE error share, which is weaker than a per-cell test:
a long ladder's far rungs resolve almost surely and dilute the near ones. ANNOTATED is
aggregate-calibrated at q = 0.80 (0.1866 <= 0.20) and per-cell calibrated at no q. Under the
per-cell reading the q = 0.80 answer changes from ANNOTATED to AS_WRITTEN; q = 0.90 and 0.95 do
not change. Both readings are published; the per-cell one is the honest bar.

## THE CORPUS LAYER (inherited harvest, rates re-derived here)

Re-weighted onto 1102's 200 harvested VALUED argmax claims: content retained at q = 0.90 is
**46.9 of 200 (0.234)** under AS_WRITTEN, 29.5 (0.147) under WIDER_RUNGS, 70.8 (0.354) under the
PROJECTED LONGER_TAPE, 200 (1.000) under the uncalibrated ANNOTATED. 134 claims are scored by
their own (family, statistic) cell; 24 + 42 carry a TRANSFERRED rate, declared in advance as an
EXTRAPOLATION and not a re-derivation of those claims (1048/1102's convention).

## THE DECLARED APPROXIMATION, AND ITS DIRECTION

LONGER_TAPE is a PROJECTION: A' = Phi(sqrt(M) Phi^-1(A)) assumes a fixed population gap and an
SE falling as 1/sqrt(T). Both assumptions run TOWARD resolution — a longer tape moves the gaps
too, and a regime it has not seen can only widen the null — so **every LONGER_TAPE count here is
an UPPER bound** on what lengthening the tape would buy, and it still loses to the one form that
can actually be enacted once its infeasibility is priced. The sub-tape fit is the check on the
exponent; 118 of 224 window-cells (18 of 32 on the full tape) have a floor CAPPED at the ladder
spread, where beta describes the spread's scaling rather than the floor's, and is declared so.

## GATES 9 of 9, printed before any result number

G1 fast runner == `engine.backtest` 1.39e-17; G2 CROSS-RUN 936/1071/1082/1094/1102/1108's
committed U56 W/H126/N=20 triple 3.18e-07; G3 SPY OOS triple 1.70e-04; G4 1098/1102's committed
U56 n=12 triple 4.97e-05 and G4b its B136 n=15 triple 2.13e-05; G5 live RULES v2 MaxDD ==
committed -12.05% at 4.95e-05; G6 determinism 0.00e+00; G7 the ladders are live (Sharpe spread
0.1916); **G8 CROSS-RUN 1102's committed tie-set verdicts 32 of 32 and its committed peaks
32 of 32** — 1102's conclusions reproduce under repaired seeds, exactly as 1108 found.

## RULE 8 AND BOTH KEEP PATHS — NOTHING PROPOSED

No clause form can move a book: the BOOK at every cell is byte-identical across all four forms,
only the PROSE changes, so 4a and 4b are invariant to dial 1 by construction. Scored anyway
because rule 4 requires it. Rung chosen on IS 2009-2016 ALONE, per ladder, three choosers, OOS
read ONCE: **4 of 24 picks clear 4b full AND OOS; 0 of 24 clear 4a.** Whole grid of 54 cells:
4b full **16**, 4b OOS **17**, **4a 0** — independently reproducing 1108's counts. Every passing
pick is the standing anchor U56 / W / H=126 / N=20 / gross 0.75 (full 15.58% / 1.1397 / -19.13%,
halves 1.2037/1.0971, OOS 16.97% / 1.1643 / -19.13%), a cell the record already holds and has
already PARKED. Benchmarks: U56 SPY full 15.10% / 0.8829 / -33.72% (halves 0.9588/0.8207), OOS
15.21% / 0.8711 / -33.72%; U56 RULES v2 live 8.62% / 1.2007 / -12.05%, OOS 9.45% / 1.2762 /
-12.05%; B136 SPY full 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767 / -33.72%; B136 RULES v2
7.98% / 1.0993 / -12.24%, OOS 7.88% / 1.1059 / -12.24%. **Nothing new, nothing promoted.**

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels, so every level is optimistic. A GAP between two
rungs and an AGREEMENT between two rungs both contrast two books over the same inflated tape and
the bias very largely cancels out of them and out of the floor; it does NOT cancel out of the 4b
legs, measured against SPY, a real index, so the 16 full-sample 4b passes are an UPPER bound.

## FOLLOW-UPS FILED

1114 (is the clause's own confidence q itself a free parameter the record never priced — its
content runs 0.516 / 0.359 / 0.293 across q = 0.80 / 0.90 / 0.95 and nothing in the record says
which bar is the record's), 1115 (does the per-cell calibration bar of D2 change any committed
DECISIVENESS claim, not just this run's own rule), 1116 (the 8 of 32 cells that never resolve at
M <= 500 — are they the same cells across statistics, i.e. is un-resolvability a LADDER property
or a STATISTIC property). Filed as 1111-1113 and renumbered on push after a lane collision —
idea 932's defect again; the concurrent lane had already taken 1111-1113.
