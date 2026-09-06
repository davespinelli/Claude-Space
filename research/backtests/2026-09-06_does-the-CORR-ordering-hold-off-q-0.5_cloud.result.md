# Idea 293 — does-the-CORR-ordering-hold-off-q-0.5 (cloud, 2026-09-06)

**Verdict: ANSWERED — the negative within-stratum `corr` → OOS-Sharpe ordering is NOT a
q = 0.5 / k = 40 artefact. It is negative in 27 of 27 (q × k × book) points, mean ρ −0.2680,
and the Simpson reversal against the pooled reading is reproduced in all three books.**
**But its SIZE is a function of the cap mix, and it dies at high small-cap share: ρ −0.343 at
q = 0.25, −0.315 at q = 0.50, and only −0.146 at q = 0.75 (1 of 9 significant, seed halves
disagree in 5 of 9). Idea 284's PARK is upgraded from one stratum to a nine-stratum
regularity, and its walk-forward selector replicates in 15 of 18 cells. Still no KEEP:
4a 2/2725, 4b 52/2725, and the two cells where S_CORR's pick clears 4b are cells where that
panel's un-ranked EWall book and RULES v2 clear it too — the pass is the panel's, not the rule's.**

Script: `research/backtests/2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.py`
Console: `….console.txt` · CSVs: `.panels` (545) `.cells` (2,725) `.strata` (108 ρ points) `.walkforward`

## Construction

Idea 284's construction re-run verbatim over the full cross of the two dials the queue named.

| dial | values | status |
|---|---|---|
| q — share of the k names drawn from SMALL439, rest from BSTK100 | 0.25, 0.50, 0.75 | **tuned (1 of 2)** |
| k — panel width | 20, 40, 80 | **tuned (2 of 2)** |

**9 strata × 60 seeded draws = 540 constructed panels + 5 NAMED = 545 panels × 5 arms
(EWall, CAND10, CAND20, RULES v1, RULES v2) = 2,725 cells, every one reported.** Common
calendar 2010-01-04 → 2026-09-04 (4,194 days); constructed-panel SPY 14.13% / 0.8616 / −33.72%,
halves 0.8907 / 0.8577, OOS 0.8820. Gate = above-200d AND vol20 < 0.60; composite score without
the vol scaler as ranking key; 75% gross; weekly; 10 bps; next-day execution. IS ≤ 2016-12-31,
2017-2026 read once.

Seeds are replication, never selection. The seed key is idea 284's verbatim — `STRAT|{q}|{sd}`,
with **k deliberately absent** — which buys the reproduction gate below and makes strata that
differ only in k seed-paired rather than freshly drawn.

**Reproduction gates, asserted before any new stratum was read.**
The (q = 0.500, k = 40) stratum is idea 284's stratum bit-identically:

| corr ρ_within | EWall | CAND10 | CAND20 |
|---|---|---|---|
| this run | −0.4708 | −0.3648 | −0.4815 |
| idea 284 published | −0.4708 | −0.3648 | −0.4815 |
| \|diff\| | 0.00000 | 0.00002 | 0.00002 |

Named panels also reproduce: U56/CAND20 **13.04% / 1.0821 / −18.30%, OOS 1.1458** (idea 284's
figure exactly), SMALL439 breadth 0.3048 against 0.6442–0.6665 for every large-cap panel,
dispersion 0.1507 vs 0.057–0.096, corr 0.1710 vs 0.309–0.378. **Gate PASS.**

## Q1 — the answer. corr ρ_within, all 27 grid points

| k | q | EWall | CAND10 | CAND20 | p (E/10/20) | both seed halves same sign |
|---|---|---|---|---|---|---|
| 20 | 0.25 | −0.4495 | −0.4593 | −0.4495 | .0003/.0003/.0003 | 3/3 |
| 20 | 0.50 | −0.2787 | −0.2551 | −0.2836 | .030/.049/.026 | 3/3 |
| 20 | 0.75 | −0.0572 | −0.0775 | −0.0532 | .670/.560/.689 | 1/3 |
| 40 | 0.25 | −0.3267 | −0.4216 | −0.2922 | .0098/.0009/.022 | 3/3 |
| 40 | 0.50 | **−0.4708** | **−0.3648** | **−0.4815** | .0005/.0046/.0003 | 3/3 |
| 40 | 0.75 | −0.1329 | −0.1389 | −0.1299 | .314/.288/.324 | 0/3 |
| 80 | 0.25 | −0.1718 | −0.2486 | −0.2646 | .191/.055/.042 | 3/3 |
| 80 | 0.50 | −0.2729 | −0.1792 | −0.2500 | .035/.175/.056 | 3/3 |
| 80 | 0.75 | −0.2714 | −0.2451 | −0.2096 | .037/.060/.108 | 3/3 |

**P1 (pre-registered: negative in ≥ 7 of 9 strata on CAND20) → 9/9. PASSES**, and 9/9 on the
other two books as well: **27/27 negative, 15/27 at p < 0.05, mean ρ −0.2680**, range
−0.4815 … −0.0532. Rank-partial ρ controlling the other three characteristics: mean **−0.2180**,
negative at every one of the 27 points.

**The dial that matters is q, not k.** Mean ρ by cap mix: **−0.3426 (q=0.25) → −0.3152 (q=0.50)
→ −0.1462 (q=0.75)**, with 7 / 7 / **1** of 9 significant and both-seed-halves agreement 9 / 9 /
**4** of 9. By width: −0.2626 (k=20), −0.3066 (k=40), −0.2348 (k=80) — no monotone trend, and
k=80 is the only width where the q=0.75 stratum survives (−0.21…−0.27, 1 significant). So the
ordering is **general in sign and reproducible in size at low-to-mid small-cap share, and
indistinguishable from zero on predominantly small-cap panels of ordinary width.**

**P3 (breadth stays ≈ 0 everywhere) → PASSES**: mean |ρ| 0.0611, max 0.1283, **0 of 27 at
p < 0.05**, seed halves agree in only 5 of 27 — which is what a zero looks like. Idea 284's KILL
of breadth as a panel property now holds at three cap mixes and three widths, not one cell.

**P4 (the pooled reversal is reproduced) → PASSES.** Pooling the 540 panels across strata flips
every sign: corr **+0.5004 / +0.3511 / +0.4578** (EWall / CAND10 / CAND20) against within-stratum
means of **−0.2702 / −0.2656 / −0.2682**; breadth pools to +0.63/+0.49/+0.59, disp to −0.32/−0.26/−0.30,
evol to −0.47/−0.33/−0.42. All three books: **REVERSAL REPRODUCED.** The other two survivors also
replicate: disp **+0.2514** mean (0/27 negative, 12/27 significant) but its partial collapses to
**+0.0046**; evol **+0.2732** (0/27 negative) with partial **+0.1551** — so at three cap mixes it is
evol, not disp, that survives the control, the opposite of idea 284's single-stratum reading.

## Rule 8 — the walk-forward, in every stratum

Selectors and directions were fixed before any OOS number was read; each picks ONE panel of 60
on its IS characteristic and that panel's OOS book is read once. Anchor = mean OOS Sharpe of all
60 draws (seed sd 0.107–0.218), i.e. drawing a panel at random.

| selector (pre-registered direction) | mean edge vs anchor, CAND10 / CAND20 | strata won (of 9) |
|---|---|---|
| **S_CORR** (lowest IS corr) | **+0.1456 / +0.1430** | **8 / 7** |
| S_DISP (highest IS dispersion) | +0.0358 / +0.0826 | 6 / 5 |
| S_BREADTH (highest IS breadth) | −0.0191 / −0.0005 | 5 / 5 |
| S_ISS (highest IS Sharpe of the book) | −0.0007 / −0.0699 | 6 / 2 |
| S_EWALL (highest IS EWall Sharpe) | −0.0667 / −0.0720 | 4 / 2 |
| S_EVOL (lowest IS eligible-set vol) | −0.1502 / −0.1704 | 3 / 2 |

**S_CORR is the only selector with a positive mean edge in both books, and it beats doing
nothing in 15 of 18 stratum × book cells** — idea 284's single-stratum finding replicated at
eight further (q, k) points. Its three losses are the two q=0.75 cells at k=40 (−0.132/−0.175,
the stratum where ρ itself is dead) and k=20/q=0.50/CAND20 (−0.031). The reverse-extreme sign
check is ordinally right (worse than anchor) in 6 of 9 strata on CAND10 and 6 of 9 on CAND20.

## KEEP paths — all 2,725 cells

**4a: 2 / 2725** (both at k=20/q=0.75, CAND20 and EWall — the stratum where RULES v2 is weakest,
OOS 0.5820). **4b: 52 / 2725**, and the footprint is a cap-mix gradient, not a rule: by q,
**4b passes 42 (q=0.25) / 7 (q=0.50) / 1 (q=0.75)**. Failure census (CAND20): all-five 241,
`H2,OOS,DD` 102, `H2,OOS,DD,CAGR` 59, DD alone 30.

**Where S_CORR's pick clears 4b, and why it is still PARK.** At k=20/q=0.25 the pick
(`k20~q0.250~s48`) clears all five bars in both books — CAND20 **14.61% / 1.1505 / −18.99%,
halves 1.2499 / 1.0691, OOS Sharpe 1.1727** and CAND10 15.03% / 1.0974 / −19.85%, OOS 1.0723,
against SPY 14.13% / 0.8616 / −33.72% (halves 0.8907 / 0.8577, OOS 0.8820). Idea 284's pick
failed on the DD cap alone; this one clears it by 1.2pp. **It is nonetheless not a rule that
earned anything**: on the same panel the *un-ranked* EWall book (1.1711, OOS 1.1952) and
RULES v2 (1.1793, OOS 1.2460) also clear 4b, and v2 does so with a −14.92% drawdown. S_CORR
found a good *panel*, and everything you could hold on that panel passes. The stratum in which
this happens is also one of nine grid points chosen after the fact.

Consistent with that: the "are 4b passers distinguished by their IS corr?" check goes the
predicted way in only 3 of the 5 strata that have passers — lower mean IS corr among passers at
k20/q0.25 (0.3003 vs 0.3255), k40/q0.25 (0.3193 vs 0.3307) and k40/q0.50 (0.2504 vs 0.2749), but
**higher** at k80/q0.25 (0.3473 vs 0.3268) and k80/q0.50 (0.2804 vs 0.2709).

**Net:** the corr ordering is a real, reproducible, cross-strata regularity with the sign the
pooled record gets backwards, and it is the record's best panel selector. It is still not a
tradable rule, and it is not measurable on predominantly small-cap panels. PARK, with the
q-dependence now quantified. Follow-ups 308–310.

## Survivorship

SMALL439 and BSTK100 are **current constituents of their screens, no delistings**, so every panel
inherits the bias whole and the LEVEL of every CAGR here — including every 4b column — is inflated.
The object under test is whether a characteristic ORDERS panels within a fixed cap mix; the bias is
common to all 60 panels of a stratum and inflates between-panel spread in level, which is what a
characteristic would have to order, so it runs **against** a "nothing separates" finding and does
**not** protect the "the ordering is general" finding this run reaches. That finding is therefore
stated as a within-corpus regularity over current-constituent panels, never as a tradable edge; and
the 44 SMALL439 tickers with `max_1d_move ≥ 1.0` were dropped before any draw.
