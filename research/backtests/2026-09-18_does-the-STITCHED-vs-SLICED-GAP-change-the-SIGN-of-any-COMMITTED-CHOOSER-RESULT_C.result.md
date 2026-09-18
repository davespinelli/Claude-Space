# Idea 1276 (lane C, 2026-09-18) — does the STITCHED vs SLICED gap change the SIGN of any COMMITTED CHOOSER RESULT?

**VERDICT: KILL (capital), NO NEW BOOK. ANSWERED NO — OUTCOME (C) THE SWITCH IS IMMATERIAL.
At PROTOCOL rule 2's rung, 0 of 18 committed chooser cells change SIGN once the switch is
charged and 0 cross their own SE. Across all 144 grid points (both pick conventions x four
cost rungs): 0 switch sign changes, 4 switch SE crossings, every one of them on the
degenerate GROSS ladder.** 13 of 13 gates, including exact replays of 1224's sliced table,
1236's ARM D and 1236's §5. Runtime 29s, offline, deterministic.

Script: `2026-09-18_does-the-STITCHED-vs-SLICED-GAP-change-the-SIGN-of-any-COMMITTED-CHOOSER-RESULT_C.py`
Dials (2, PROTOCOL rule 4): **VERDICT SET** {V_AXIS 12 cells, V_WIDE 3, V_POOL 3} x
**COST RUNG** {0, 10, 25, 50} bps. 72 grid points, each computed under BOTH pick conventions
(144 rows), every one published in `.cells.csv`. Nothing is selected on the convention and the
two are identical at the reference rung (gate G8c).

---

## 1. What 1236 left conflated, and what this run separates

1236's ARM D compared a WHOLE-SPAN Sharpe (the realised stitched book) against a
MEAN-OF-FOLD-SHARPES (the record's sliced accounting). Those differ for two unrelated
reasons and only one of them is the switch:

    S1 SLICED        mean over folds of [S_oos(anchor, f, c) - S_oos(pick_f, f, c)], continuous books
    S2 STITCHED_FREE whole-span Sharpe of the REALISED moving book, anchor minus book, with the
                     INCREMENTAL re-booking turnover at each switch row rebated
    S3 STITCHED_PAID the same book paying its own switch turnover                   (1236's ARM D)

    AGGREGATION = S2 - S1     SWITCH CHARGE = S3 - S2     TOTAL = S3 - S1

The rebate in S2 is `t_stitched(o0) - t_continuous_new(o0)`, so the moving book is charged
everything a continuously-run book of the same rung would have paid and not one basis point
more. SWITCH CHARGE is therefore EXACTLY 0 at 0 bps (G5) and EXACTLY 0 for a cell that never
switches (G6) — two facts the decomposition must satisfy and does, to 0.0.

## 2. The answer — the census at every rung, under both pick conventions (`.census.csv`)

| picks | cost | cells | FLIP(switch) | FLIP(total) | SEcross(switch) | SEcross(total) | mean SWITCH | mean AGGREG |
|---|---|---|---|---|---|---|---|---|
| CA | 0 | 18 | 0 | 2 | 0 | 4 | +0.0000 | +0.0202 |
| **CA** | **10** | **18** | **0** | **2** | **0** | **4** | **+0.0017** | **+0.0155** |
| CA | 25 | 18 | 0 | 3 | 0 | 3 | +0.0041 | +0.0052 |
| CA | 50 | 18 | 0 | 3 | 1 | 3 | +0.0071 | +0.0000 |
| FZ | 0 | 18 | 0 | 2 | 0 | 4 | +0.0000 | +0.0155 |
| **FZ** | **10** | **18** | **0** | **2** | **0** | **4** | **+0.0017** | **+0.0155** |
| FZ | 25 | 18 | 0 | 2 | 1 | 4 | +0.0043 | +0.0154 |
| FZ | 50 | 18 | 0 | 2 | 2 | 5 | +0.0087 | +0.0154 |

CA = the chooser sees the rung it pays (the realised object, PRIMARY). FZ = picks made once at
10 bps and re-priced, which is 1224's / 1236's main-grid convention. **No sign change is
attributable to the switch at any rung under either convention: 0 of 144.**

## 3. Why — the gap 1236 published is 89% ACCOUNTING SHAPE, not cost

At the reference rung the mean SWITCH CHARGE is **+0.0017** of Sharpe against a mean
AGGREGATION gap of **+0.0155** — a ratio of **0.1117**. The switch charge is bounded at
**+0.0000 / +0.0017 / +0.0041 / +0.0071** (max over any single cell +0.0041 / +0.0117 /
+0.0163) across the whole 0-50 bps ladder, while at **0 bps — where the switch costs exactly
nothing — the stitched-minus-sliced gap is still +0.0202.**

So 1236's ARM D headline ("+0.0331 -> +0.0417 across 0-50 bps, so every committed
chooser-minus-anchor figure is a FLOOR") is **directionally right and mechanistically
misattributed**: +0.0331 of the +0.0417 is present with costs switched off and is the
difference between averaging 14 fold Sharpes and computing one span Sharpe. **The re-booking
cost itself is worth +0.0017 at PROTOCOL's rung and moves no verdict.** This is the third
arrival on this record at the same shape of answer (1236 §1 found 98.1% of 1224's gain
survives at 0 bps; §3 found the N-vs-H sign disagreement cost-invariant): **on this tape, cost
rungs inside 0-50 bps are not where chooser verdicts live.**

## 4. By family at the reference rung (`.byfamily.csv`)

| family | cells | switches | S1 sliced | S3 paid | switch | aggregation | anchor wins sliced -> paid | flips sw/tot | SE x sw/tot |
|---|---|---|---|---|---|---|---|---|---|
| V_AXIS | 12 | 43 | +0.0213 | +0.0348 | +0.0013 | +0.0122 | 10/12 -> 10/12 | 0 / 2 | 0 / 3 |
| V_WIDE | 3 | 20 | +0.0690 | +0.0996 | +0.0030 | +0.0276 | 3/3 -> 3/3 | 0 / 0 | 0 / 1 |
| V_POOL | 3 | 14 | -0.0023 | +0.0165 | +0.0023 | +0.0165 | 2/3 -> 2/3 | 0 / 0 | 0 / 0 |

**Not one of the 18 cells changes which side wins because of the switch.** V_POOL is the one
family whose POOLED sign moves (-0.0023 sliced to +0.0165 paid) and all of that move is
aggregation; no individual V_POOL cell flips and none crosses its own SE.

## 5. The verdicts that DO move are the degenerate ladder again (`.cells.csv`)

Both TOTAL sign changes at 10 bps, and 3 of the 4 TOTAL SE crossings, are the GROSS ladder:

| cell | S1 sliced | its own SE | S3 paid | aggregation | switch |
|---|---|---|---|---|---|
| B136 V_AXIS GROSS | **+0.000000** | **0.000000** | +0.000375 | +0.000375 | 0.000000 |
| SMALL V_AXIS GROSS | +0.002599 | 0.001299 | **-0.024636** | -0.027681 | +0.000446 |
| U56 V_AXIS GROSS | +0.000535 | 0.000399 | +0.064392 | +0.063600 | +0.000257 |
| U56 V_WIDE | +0.044607 | 0.073603 | +0.133177 | +0.084597 | +0.003973 |

B136's sliced delta is **exactly 0.000000 with an SE of exactly 0.000000** — the chooser never
leaves the anchor, so a sign "change" of +0.000375 is arithmetic on a null object, not a
verdict. All 4 SWITCH SE crossings anywhere in the 144 (U56 GROSS @25/@50 FZ, SMALL GROSS @50
CA and FZ) are cells whose own SE is 4.7e-4 to 1.5e-3 — i.e. **the crossings are the
denominator collapsing, not the numerator moving.** This is the fifth run to land on the
GROSS ladder's degeneracy (1189 / 1214 / 1224 / 1236 / here) and the operational reading is
unchanged: **a GROSS-ladder t-statistic or SE crossing on this record is never economic.**

## 6. Both KEEP paths on every realised book (PROTOCOL rule 4)

| cost | stitched 4a | stitched 4b | anchor 4a | anchor 4b |
|---|---|---|---|---|
| 0 | 0 of 18 | 2 of 18 | 0 | 6 of 18 |
| **10** | **0 of 18** | **1 of 18** | **0** | **6 of 18** |
| 25 | 0 of 18 | 1 of 18 | 0 | 6 of 18 |
| 50 | 0 of 18 | 1 of 18 | 0 | 6 of 18 |

**4a is 0 everywhere, as at every previous attempt** — live RULES v2's -12.05% MaxDD is
shallower than every growth book on this tree. The single stitched book that clears 4b at
10 bps is U56 / V_AXIS / GROSS: **15.43% CAGR / 1.1609 Sharpe / -19.13% MaxDD (halves
1.1234 / 1.2178)** over the 2013-2026 fold span, against span SPY **14.97% / 0.9163 /
-33.72% (H 1.0849 / 0.8405)** and live RULES v2 **9.23% / 1.3033 / -12.05% (H 1.2813 /
1.3355)**. Its own pick sequence gives it away: `2013:GROSS=0.3 | 2014:GROSS=0.5 |
2015..2026:GROSS=0.75` — **two switches, after which it IS the committed 2026-09-04 anchor.**
It is prior art reached by a longer road, not a new book, and is NOT promoted (rule 6).

## 7. Rule 8 — 2017-2026 read once (`.walkforward.csv`)

432 rows (3 panels x 6 cells x 4 cost rungs x 2 pick conventions x 3 arms). STITCH_OOS
re-picks at each OOS fold from data strictly before it; FROZEN picks once on
warm-up..2016-12-31 and holds; ANCHOR never moves.

| arm | rows (CA) | 4a OOS | 4b OOS | mean OOS CAGR / Sharpe / MaxDD | mean turnover |
|---|---|---|---|---|---|
| STITCH_OOS | 72 | 0 | 5 | 12.20% / 0.8141 / -26.80% | 3.695 |
| FROZEN | 72 | 0 | 8 | 12.90% / 0.8393 / -27.81% | 3.327 |
| **ANCHOR** | 72 | 0 | **24** | **13.10% / 0.8624 / -25.38%** | 3.574 |

OOS anchor-minus-stitched Sharpe **+0.0516 / +0.0637 / +0.0501 / +0.0279** at 0/10/25/50, of
which **the switch cost alone is +0.0000 / +0.0015 / +0.0034 / +0.0058** — the same 1-to-10
ratio the full-sample census gives, out of sample and untouched. Note the OOS gap SHRINKS as
cost rises while the switch charge grows: the chooser becomes the anchor faster than the
switch gets expensive.

Benchmarks (OOS 2017-2026): U56 SPY **15.28% / 0.8747 / -33.72%** (H 0.9915/0.7488), live
RULES v2 **9.47% / 1.2781 / -12.05%**; B136 SPY 15.33% / 0.8769, live 7.88% / 1.1061; SMALL
SPY 15.33% / 0.8769, live 4.47% / 0.6518.

Every OOS 4b pass resolves to **5 distinct realised books across 37 passing rows**, and the
24 ANCHOR passes are one book — the standing 2026-09-04 U56 N=20 / H=126 / gross 0.75 /
weekly incumbent, whose OOS 17.28% / 1.1832 / -19.13% at 10 bps replays 1236 exactly.
**CONFIRMATORY, NOT GENERATIVE — NOTHING PROMOTED, NO RULES CHANGE (rule 6).**

## 8. Survivorship (rule 9)

U56 (55 names) and B136 (135) are CURRENT constituents; SMALL is the sub-$2B screen, 664
investable of 715 after dropping every ticker with max_1d_move >= 1.0, and starts 2010. SPY is
excluded from every eligible set and used as benchmark only. The bias does not cancel out of
the OOS levels or the 4b legs, so every pass above is an upper bound. It DOES largely cancel
out of the anchor-minus-chooser DELTAS, which are differences of two books on one panel — the
census in §2 is the more trustworthy half of this run.

## 9. Gates — 13 of 13

G1 fast runner == engine.backtest at EVERY cost rung 2.08e-17 · G2 the 0 bps rung is the gross
book exactly 0.0 · G3 live RULES v2 U56 MaxDD -12.0549% == committed -12.05% · G4 the anchor
rung of all four ladders is ONE book, returns AND turnover, 0.0 · G5 SWITCH CHARGE exactly 0
at 0 bps, 0.0 · G6 a never-switching cell has SWITCH CHARGE 0 at every rung, 0.0 · G6b
incremental switch turnover never negative, 0 of 144 · G8c the two pick conventions are
identical at the reference rung, 0.0 · G9 folds tile all three panels (14 each) ·
**G7 1236's ARM D replays on the 12 V_AXIS books (FZ) 3.23e-05** · **G7b 1236's 43
fold-boundary switches replay exactly** · **G7c 1236's §5 cost-aware chooser row replays on
the CA arm 3.85e-05** · **G8 1224/1236's P_AXIS SLICED delta replays (FZ) 3.39e-05.**

A first pass of this run compared its cost-aware grid against 1236's FROZEN-pick table and
failed G7/G8 at 2.7e-2 / 1.8e-2. **The bar was NOT widened.** The mismatch was diagnosed: the
CA arm reproduces 1236's §5 cost-aware row (+0.0157 / +0.0213 / +0.0159 / +0.0052) to 3.8e-05
at all four rungs, and the FZ arm reproduces its main grid to 3.4e-05. Both conventions are
now computed and published in full, which is why the grid is 144 rows rather than 72.

## 10. What this leaves for the queue

Three sentences worth a header. **(i) The stitched-vs-sliced gap the record has been treating
as a re-booking cost is 89% an AGGREGATION artefact — mean-of-fold-Sharpes against a whole-span
Sharpe — and is +0.0202 at 0 bps where the switch is free by construction.** **(ii) The
re-booking cost proper is worth +0.0017 of Sharpe at PROTOCOL's rung and changes the sign of
0 of 18 committed chooser verdicts and crosses 0 of their own SEs; 1236's claim that every
committed chooser-minus-anchor figure is a FLOOR survives as a statement about the LEVEL and
dies as a statement about any VERDICT.** **(iii) Every SE crossing the switch does produce
sits on the GROSS ladder, whose own cell SEs are 4.7e-4 to 1.5e-3 — the denominator, not the
numerator, and the fifth arrival at that sentence.** A schema line follows from (i): **a
committed chooser comparison must state whether its statistic is a POOLED FOLD MEAN or a
WHOLE-SPAN READING, because on this tape the two differ by an order of magnitude more than
the cost rung does.** Three follow-ups filed, all price-only.
