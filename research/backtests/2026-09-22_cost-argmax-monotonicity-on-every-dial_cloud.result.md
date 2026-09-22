# Idea 1621 (lane cloud, 2026-09-22) — does the SLOWER-ONLY direction of COST INVERSION hold on the OTHER DIALS?

**ANSWERED = YES, UNANIMOUSLY — AND THE LAW IS WEAKER THAN IT LOOKS, BECAUSE THE ARGMAX BARELY MOVES AND IS BARELY RESOLVED.**

## What was priced
Four turnover-bearing dials, each a fresh ladder of real books, on three panels x two cadences =
**24 instances / 156 rungs / 7,956 grid points** (`*.grid.csv`), every one published.
`TOPN` N in {5,10,20,30,40,ALL} · `MINHOLD` H in {1,5,10,21,42,63,126} trading days ·
`HYST` exit-rank slack h in {0,5,10,20,40,80} on a top-20 book · `BAND` c in
{0.00,0.02,0.03,0.05,0.08,0.12,0.16}.  Gross 0.75 everywhere, t+1 fills, gate = above the 200d
MA & vol20 < 0.60.  Each book was priced ONCE at cost 0 and reconstructed at all 51 cost rungs
from its own turnover series; **gate G_COST: max |err| vs a direct 25 bps engine run = 0.000e+00**,
so the ladder is exact, not a two-rung interpolation.

Tuned dials (2): DIAL SET, COST LADDER.  Reported, not tuned: panel, cadence, gross, N=20 inside
MINHOLD/HYST.

## Headline
| gate | result |
|---|---|
| **V1a DIRECTION (listed slowness order)** | **18 of 18** adjacent-cost argmax moves are SLOWER, **0 faster** — share 1.0000 |
| **V1b DIRECTION (empirical turnover order)** | **18 of 18** slower, **0 faster** — the law is not an artefact of how the record labels a dial |
| **V2a / V2b MONOTONE** | **24 of 24** argmax paths monotone non-decreasing in slowness, on BOTH indices |
| **V3a / V3b 1586 REPLICATION** | 6 of 24 instances move between 10 and 25 bps; **6 slower, 0 faster** |
| **V4 CAPITAL** | 6 of 24 argmax cells clear 4b FULL+OOS at 10 bps (all U56); **4a = 0 of 24** |
| **V5 RESOLUTION** | **FAIL** — median Sharpe margin holding an argmax **0.0183** (target > 0.02); **13 of 24 instances sit below 0.02** |

So 1586's slower-only finding is **not a cadence fact**: it is a property of the cost axis that
reproduces on every other turnover-bearing dial the record owns, in 18 of 18 moves, under two
independently-defined slowness orderings.  **No dial's argmax ever wandered backwards.**

## The three qualifications that matter more than the headline
1. **The argmax hardly moves.**  10 of 24 instances have **zero** moves over the whole
   0-50 bps ladder, and the committed 10 bps argmax equals the 0 bps argmax on **20 of 24** and the
   50 bps argmax on **13 of 24**.  All 18 moves come from three dials — HYST 10, MINHOLD 5,
   TOPN 3.  **BAND contributes 0 of 18**: the band dial's best rung is cost-INVARIANT on all six
   panel x cadence instances, so the directional law is vacuous there.
2. **The argmax is poorly resolved.**  Median best-minus-runner-up Sharpe margin is 0.0183 and
   **54% of instances hold their argmax by less than 0.02** — U56/W HYST holds it by **exactly
   0.0000**.  A unanimous DIRECTION does not make the committed best rung a resolved number.
3. **Ladders saturate.**  **8 of 156 rungs are DEGENERATE** — bit-identical books to a lower rung
   (e.g. on a 56-name panel HYST h >= 36 puts the exit rank beyond the panel, so h=40 and h=80 are
   the same book; MINHOLD H=63 and H=126 coincide at monthly cadence).  5 of 24 instances are
   affected.  Argmax ties were broken toward the FASTER rung — the conservative direction for a
   slower-only claim.

## Rule 8 — 2017-2026 read ONCE
Rung chosen on 2009-2016 IS Sharpe at 10 bps, OOS read once.  The IS pick equals the full-sample
argmax on **12 of 24** instances; **mean OOS rank 3.54 of 6.5** rungs — an in-sample chooser on
these dials is barely better than the middle of its own ladder.  4b OOS is reached on **6 of 24**
(all U56); 4a FULL on **0 of 24**.  On SMALL every IS pick lands at the slow end of its ladder and
**every one fails 4b** (OOS Sharpe 0.319-0.717 against SPY OOS 0.875).

## Capital
One 4b KEEP-candidate falls out and is **recorded, not recommended** — U56 / weekly / BAND c=0.12
at gross 0.75, chosen by the legal IS-only chooser and identical to the full-sample argmax:
FULL 13.95% / 1.2218 / -19.42% (H1 1.2617 / H2 1.1959), OOS 15.03% / 1.2581 / -19.42%, turnover
1.93x/yr, against SPY FULL 15.14% / 0.8851 / -33.72% and OOS 15.29% / 0.8751 / -33.72%.  It clears
4b in FULL and OOS.  It is **not** proposed for adoption: it fails 4a (0 of 24 everywhere), it
does **not** replicate on B136 (4b FULL False) or SMALL (0 of 810-cell equivalents), and it is a
re-discovery of the band x gross family the record already priced under ideas 2119 / 923.

## Survivorship (rule 9)
U56, B136 and SMALL are all CURRENT-CONSTITUENT panels (SMALL = the sub-$2B screen as cached,
719 names, of which the **54 with max_1d_move >= 1.0 were dropped**, leaving 665 investable names;
SPY is a benchmark column there, not a constituent).  All CAGR and MaxDD LEVELS are optimistic and
both 4b bars are easier than on a point-in-time panel.  The measured object — where an argmax sits
along a cost axis on one and the same tape — is first-order immune; the 4b pass counts are not.

## Verdict
**ANSWERED = YES / KILL of the "committed best rung is a cost-rung artefact" worry, PARK of the
resolution problem.**  The direction is a law (18/18, both indices, 24/24 monotone paths), but the
practical content is small: on 20 of 24 instances the 10 bps rung and the 0 bps rung name the same
winner, and on 54% of instances that winner is held by less than 0.02 of Sharpe.  The record's
committed best rungs are not mislocated BY COST; they are under-resolved FULL STOP.

Files: `*.grid.csv` (7,956 rows) · `*.argmax.csv` (1,224 rows) · `*.instances.csv` (24) ·
`*.walkforward.csv` (24) · `*.gates.csv` · `*.log.txt`
