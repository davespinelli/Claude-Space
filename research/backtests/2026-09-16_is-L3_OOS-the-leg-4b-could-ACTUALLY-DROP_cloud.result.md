# Idea 1018 (cloud lane, 2026-09-16) — is `L3_OOS` the leg 4b could ACTUALLY DROP?

**ANSWERED = YES, EXACTLY, AND FOR A REASON 1014's CENSUS COULD NOT SEE. KILL the "widening"
framing: the 4b-minus-OOS conjunction is IDENTICAL to 4b on every population this record can
reach — 0 of 135 real rows and 0 of 13,500 gross-matched null draws change verdict, in all 9
claim-set x cost cells. KEEP a PROTOCOL rule 4 LEG-DROP clause (proposed, not applied — rule 6).
Nothing promoted, no RULES change; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
`baseline.py` untouched.**

Script: `2026-09-16_is-L3_OOS-the-leg-4b-could-ACTUALLY-DROP_cloud.py`

## The grid

45 books — the record's **9** committed memo-backed 4b passes (SHELF, rebuilt from lane C's own
`shelf_books` plus 1013's ninth) and the **36** never-memo-selected band x gross x QROLL ladder
(GRID) — each carried with **100** gross-matched ROT null draws (926's convention: at every
rebalance date a RANDOM subset of the SAME SIZE at the SAME GROSS from the names priced that
day), at **3** cost rungs x **2** panels. 135 real rows, **13,500** null rows. Two tuned axes
only, the queue line's own — CLAIM SET {REC, GRID, SHELF} x BINDING DEFINITION {SOLE, ANY} —
all 9 cells reported, none selected. Split fixed at PROTOCOL rule 8's own 2016-12-31 (idea 1013
priced moving it); bar convention the record's own REC_FULL.

## The answer is an integer and it is zero, twice

`d_real` and `d_null` — the widening of the PASS population when `L3_OOS` is dropped — are
**+0.0000 in all 9 cells**. Not "small": zero rows, real or null.

| claim | cost | real 4b | real 4b′ | **d_real** | null 4b | null 4b′ | **d_null** | DISC 4b | DISC 4b′ |
|---|---|---|---|---|---|---|---|---|---|
| REC | 0 | 0.6667 | 0.6667 | **+0.0000** | 0.3811 | 0.3811 | **+0.0000** | +0.2856 | +0.2856 |
| REC | **10** | **0.6222** | **0.6222** | **+0.0000** | **0.1344** | **0.1344** | **+0.0000** | **+0.4878** | **+0.4878** |
| REC | 25 | 0.5111 | 0.5111 | +0.0000 | 0.0007 | 0.0007 | +0.0000 | +0.5104 | +0.5104 |
| GRID | 10 | 0.5278 | 0.5278 | +0.0000 | 0.1336 | 0.1336 | +0.0000 | +0.3942 | +0.3942 |
| SHELF | 10 | 1.0000 | 1.0000 | +0.0000 | 0.1378 | 0.1378 | +0.0000 | +0.8622 | +0.8622 |

**H_BIND PASS** — `L3_OOS`'s SOLE-binder rate is **0.0000** in every one of the 9 cells,
reproducing 1014's 0.00013 record-wide figure on a fresh population from a different code path.
**H_WIDEN PASS** (max d_real +0.0000 vs a 0.10 bar). **H_NULL PASS**, the headline: the null
widens by no more than the real books, because neither widens at all. **H_DISC PASS**: the
real-minus-null discrimination gap is unchanged to the last digit — at REC/10 bps,
**DISC(4b) = DISC(4b′) = +0.4878**.

## The mechanism, and it is the part 1014 could not reach: DEPTH-3 CO-BINDING

"Never sole" is a weak statement if a leg is one co-binder away from deciding. It is not.
Among the null FAIL rows where `L3_OOS` itself fails, the **total** number of failing legs is
**never 1 and never 2** — the minimum observed co-fail depth is **3**, on all three rungs:

| source | cost | FAIL rows | of which `L3_OOS` fails | depth 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|---|
| REAL | 10 | 17 | **0** | 0 | 0 | 0 | 0 | 0 |
| NULL | 0 | 2,785 | 4 | 0 | 0 | 1 | 3 | 0 |
| NULL | **10** | 3,895 | **309** | **0** | **0** | 53 | 75 | 181 |
| NULL | 25 | 4,497 | **3,881** | **0** | **0** | 19 | 1,807 | 2,055 |

**H_DEPTH PASS.** The leg is not droppable because it is weak — it is droppable because by the
time a book's OOS Sharpe falls below SPY's, at least two other legs have already failed. On
real books `L3_OOS` never fails at all (real rate **1.000** vs null **0.9313**).

And it is emphatically not idle. Its ANY-binder rate on the null's FAIL rows runs **0.0014 /
0.0793 / 0.8630** at 0 / 10 / 25 bps (REC) — at 25 bps the leg is failing on **86%** of null
failures while still deciding **none** of them. A frequent co-binder that never decides, which
is the same shape idea 1014 found for `L2_H2` (54.3% co-binding, 0.29% sole) one leg further
out.

## What the leg is actually worth: the smallest discrimination lift of the five

Per-leg pass rates at REC / 10 bps over 4,500 null draws and 45 real books:

| leg | null rate | real rate | **lift** |
|---|---|---|---|
| `L4_DD` | 0.5396 | 0.8667 | **+0.3271** |
| `L1_H1` | 0.7187 | 0.9556 | +0.2369 |
| `L2_H2` | 0.7864 | 1.0000 | +0.2136 |
| `L5_CAGR` | 0.6189 | 0.8000 | +0.1811 |
| **`L3_OOS`** | **0.9313** | 1.0000 | **+0.0687** |

`L3_OOS` is the leg the coin flip clears most easily (0.9313, the highest of five) and the leg
that separates a book from a coin flip least (+0.0687, the smallest of five, **4.8x** below
`L4_DD`). The two readings agree: the leg carries the least information in the conjunction.

## Rule 8 and both KEEP paths

The walk-forward is PROTOCOL rule 8's own: 3 IS-only choosers x 2 panels x 3 rungs = **18
picks** from the GRID pool made on 2009-01-13..2016-12-31 **alone**, 2017–2026 read once.
**H_RULE8 PASS — 0 of 18 picks change verdict**, and **no committed 4b FAIL becomes a rule-8
pass under 4b′** (0 FAIL→PASS flips over all 45 books at every rung). The picks and their OOS
triples at 10 bps:

- U56 `band0.08@1.00` (IS_SHARPE and IS_LEGS) **11.99% / 1.162 / −19.05%**
- U56 `qroll-q0.17-w1008-d0.50` (IS_CAGR) **15.60% / 1.293 / −15.59%**
- B136 `band0.08@1.00` (IS_SHARPE and IS_LEGS) **11.05% / 1.097 / −19.50%**
- B136 `qroll-q0.12-w1008-d0.50` (IS_CAGR) **14.30% / 1.157 / −17.31%**

Comparands: **SPY OOS 15.21% / 0.871 / −33.72%** (U56) and **15.33% / 0.877 / −33.72%** (B136);
**RULES v2 (live, 10 bps) full 8.62% / 1.201 / −12.05%** (H1 1.232 / H2 1.176) on U56 and
**7.98% / 1.099 / −12.24%** (H1 1.235 / H2 0.966) on B136. All 18 picks pass 4b and 4b′ alike.
**4a is 2 of 135** over the whole real ladder and **0 of 18** among the picks — gross against the
live book's −12.05% drawdown is not close on any cell. **Nothing is promoted.**

## Gates 7 of 7 PASS, printed before any result number

G1 `fast_run` == `engine.backtest` on returns AND turnover **6.939e-18 / 1.665e-16**. G2 band
book == `baseline.rules_v2_weights` **0.000e+00**. **G3 CROSS-RUN** SPY's OOS triple at
2016-12-31 reads **15.2102% / 0.8711 / −33.7173%** against the record's committed 15.21% /
0.8713 / −33.72%, max|d| **1.702e-04**. **G4** all 9 SHELF books reproduce their committed memo
triples, **9 of 9**. **G5 GROSS MATCH** every one of the 13,500 null draws matches its book's
realised gross to **4.441e-16** and its holding count to **0**. G6 determinism **0.000e+00**.
G7 leg identity, independent recomputation, **0** disagreeing rows.

## Limits, stated

The null is **gross**-matched, not turnover-matched (926's convention), so it inherits the
book's timing of when to be invested and randomises only WHICH names — it is a test of security
selection, not of the gate. 100 draws per book resolves a pass rate to about ±0.05 at 2 SE, so
`d_null = 0.0000` bounds the widening below roughly 1 in 13,500, not to literal impossibility.
The cost ladder stops at 25 bps; the ANY-binder rate's climb to 0.8630 there says the leg's
redundancy is a function of where the other four bars sit, and this run does not establish it at
rungs the record does not carry. The split is fixed at 2016-12-31 — idea 1013 priced moving it,
and its 16-end band is not re-run here.

## Survivorship (rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL above is optimistic
and every 4b/4b′ count an UPPER bound. The measured object is a DIFFERENCE between a book and a
coin flip drawn from the SAME panel on the SAME tape at the SAME gross. A coin flip drawn from a
survivor panel is a BETTER book than one drawn in real time, so every NULL pass rate here is an
UPPER bound and every DISC a LOWER bound — which cuts **against** this run's own H_NULL, i.e.
the hypothesis that the leg is free was the EASIER one to pass and it passed anyway. SPY is a
real index series and is not inflated.

## Proposed, not applied (rule 6)

`2026-09-16_leg-drop-clause_cloud.memo.md` proposes a PROTOCOL rule 4 clause: *no leg is dropped
from the 4b conjunction on a SOLE-BINDER rate alone; a proposed drop is published with the leg's
CO-FAIL DEPTH distribution on the book population AND on a gross-matched null, and with its null
DISCRIMINATION LIFT at every cost rung the record carries. A leg whose minimum co-fail depth is
2 on any population is NOT droppable.* On this run the clause clears `L3_OOS` (min depth 3, lift
+0.0687) and would have refused the drop on the evidence 1014 alone supplied, which established
only the sole rate.

Follow-ups filed: 1027, 1028, 1029 (renumbered from 1024-1026: lane C claimed those numbers in the same hour — idea 932's numbering defect again).
