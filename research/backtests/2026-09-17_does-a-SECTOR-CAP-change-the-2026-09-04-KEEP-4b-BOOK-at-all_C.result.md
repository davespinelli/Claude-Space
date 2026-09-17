# Idea 1258 (lane C, 2026-09-17) — does a SECTOR CAP change the 2026-09-04 KEEP 4b book at all?

**VERDICT: KILL (capital). ANSWERED = YES IT CHANGES IT, AND EVERY CHANGE IS A LOSS ON THE PANEL
THE CANDIDATE LIVES ON.** No new book, no memo, no RULES change. Pre-declared outcome (C) lands.

Script: `research/backtests/2026-09-17_does-a-SECTOR-CAP-change-the-2026-09-04-KEEP-4b-BOOK-at-all_C.py`
Console: `..._C.console.txt`  Grid: `..._C.grid.csv` (56 rows, every one published)
Walk-forward: `..._C.walkforward.csv`  Maps: `..._C.maps.csv`  Gates: `..._C.gates.csv` (1 of 1 PASS)

## Dials (rule 4) and what was frozen
CAP {1,2,3,4,5,6,8,20} x MAP {PIT, FROZEN} = 16 cells per panel on U56 / B136 / SMALL663, plus a
UJSON control arm on U56 (universe.json's own four declared groups, reported never chosen).
CAP = 20 is unreachable at N = 20 and is the UNCAPPED ANCHOR. PIT = point-in-time argmax of the
252d trailing correlation to one of the 11 sector SPDRs (below 0.50 the name is UNMAPPED and
uncapped); FROZEN = the same argmax computed once on warm-up..2016-12-31 and held fixed. Frozen
constants, not dials: CORR_MIN 0.50, CORR_LOOK 252, the 11-SPDR sector set. The book itself is
untouched: RAW composite (21/252, 0/126, 0/63), no vol scaler, above-200d AND vol20 < 0.60,
N = 20, H = 126, gross 0.75, weekly, 10 bps, t+1, warm-up 260. **Gate G1: the uncapped anchor
replays the committed U56 triple 15.71% / 1.1480 / -19.13% to 0.0000.**

## The headline
1. **THE BOOK IS CONCENTRATED AND THE CAP REALLY BITES.** The uncapped book's largest co-movement
   group holds a mean 6.7 of 20 slots on U56 (worst week 13 of 20) and 7.0 of 20 on B136. A cap is
   therefore not a clause about nothing: at CAP = 1 it displaces 12.2 candidates per rebalance on
   U56 and the resulting book shares only **0.457** of the anchor's names.
2. **AND IT LOSES ON BOTH AXES.** On U56 the cap costs CAGR at **14 of 14** capped cells
   (-0.17 to -4.37 pp/yr) and makes MaxDD **WORSE at 13 of 14** (-0.36 to +0.08 pp). It is worse on
   BOTH at 13 of 14. The single cell that improves drawdown does so by 0.08 pp while costing
   0.17 pp/yr. The cheapest risk clause in the record buys no risk reduction on the panel the
   standing candidate is defined on.
3. **4a 0 of 56.** Every cell's drawdown is worse than live RULES v2's -12.05%.
4. **4b 13 of 56 (U56 7 of 16 dial cells, B136 3 of 16, SMALL663 0 of 16).** Two of U56's seven
   are the anchor itself; the five capped passes are all strictly worse than the anchor. **Every
   U56 and B136 failure is the DRAWDOWN leg alone** (9 and 13 cells), consistent with ideas
   1253/1256/1257.
5. **THE CAP IS NOT ENFORCEABLE ON THIS BOOK.** With H = 126 and point-in-time groups, held names
   drift into over-full groups: the cap is VIOLATED on **0.597 / 0.148 / 0.026** of weeks at
   CAP = 1 / 5 / 8 on U56. A RULES line saying "at most k per sector" would be false about the
   book it governs unless it also overrides the minimum hold — i.e. it is a different book.
6. **THE GROUP MAP IS THE BIGGER DIAL.** The UJSON control (4 hand-written groups) binds on
   **100%** of rebalances at CAP <= 4, displacing 23-33 candidates a week, drops name overlap to
   0.162 and takes MaxDD to **-28.74%** at CAP = 1. Coarser groups change the book more and hurt
   it more. Whoever writes the clause chooses the answer by choosing the map.
7. **B136 IS THE ONE PLACE A CAP FLIPS A VERDICT, AND IT IS INSIDE THE TAPE'S PRECISION.** The
   B136 anchor FAILS 4b on DD (-20.74% vs a -20.23% cap); FROZEN/1 passes at **-20.1760%, a
   margin of 0.056 pp**, and PIT/1 with the same cap rung under the other map still FAILS. Filed
   as a live instance of idea 1259's precision question, NOT as a candidate.
8. **SMALL663 HAS NOTHING TO CAP.** Mean max-group share 0.132, 0.71 of name-days UNMAPPED, bind
   rate <= 0.026 at every rung; at CAP >= 8 the capped book is bit-identical to the anchor.

## Rule 8 (walk-forward) — (CAP, MAP) chosen on warm-up..2016-12-31 by IS Sharpe only, 2017-2026 read ONCE
| panel | IS pick | IS Sharpe | OOS Sharpe | uncapped anchor OOS | grid mean | worst | IS/OOS rank corr |
|---|---|---|---|---|---|---|---|
| U56 | FROZEN/1 | 1.3341 | 1.1805 | 1.1759 (**+0.0045**) | 1.1403 | 1.0301 | -0.0368 |
| B136 | FROZEN/1 | 1.3620 | 1.1359 | 1.0240 (**+0.1119**) | 1.0459 | 0.9696 | -0.0368 |
| SMALL663 | FROZEN/1 | 0.7237 | 0.4417 | 0.4534 (**-0.0118**) | 0.4583 | 0.4417 | -0.3015 |

Pooled IS-chosen OOS Sharpe **0.9193** vs do-nothing anchor **0.8845** (+0.0349) vs grid mean
0.8815. This is the record's first dial whose IS chooser does not lose to doing nothing — **but
the IS/OOS rank correlation is NEGATIVE on all three panels**, so it is not selection working:
the chooser lands on the SAME extreme rung (CAP = 1, FROZEN) on every panel, and CAP = 1 is
maximal diversification rather than a chosen cell. The Sharpe it buys is paid for in CAGR
(U56 13.82% OOS vs the anchor's 17.16%), which is why it does not rescue a single 4b verdict.

## Survivorship (rule 9) and one caveat on the map
U56 / B136 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen (52 of 715 dropped
for max_1d_move >= 1.0). Levels are optimistic. A current-constituent panel is KIND TO
CONCENTRATION — the names a momentum screen piles into are disproportionately the ones that
survived into the list — so the UNCAPPED arm is the more flattered of the two and the cap's
losses reported here are an **UPPER bound** on its losses, its wins a **LOWER** bound. Separately,
a correlation-argmax group is a CO-MOVEMENT group, not a GICS sector; it is the only sector-like
map derivable offline from committed data, and the UJSON arm is the independent hand-written read.

## Why no memo
A KEEP memo needs a cell that beats the incumbent on a KEEP path. None does: the five capped U56
4b passes are all lower-CAGR, mostly deeper-drawdown versions of the anchor, and the only
verdict-flipping cell (B136 FROZEN/1) clears its bar by 0.056 pp and is contradicted by the same
rung under the other map.
