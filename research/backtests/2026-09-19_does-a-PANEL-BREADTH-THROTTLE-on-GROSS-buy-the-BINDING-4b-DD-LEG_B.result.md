# Idea 1413 (lane B, 2026-09-19) — does a PANEL-BREADTH THROTTLE on GROSS buy the BINDING 4b DD LEG?

**ANSWER: NO. OUTCOME (C) DEGENERATE FIRED. KILL (capital), NO NEW BOOK, NO RULES CHANGE.**

## What was run
The frozen 2026-09-04 KEEP-4b incumbent (U56, N=20, H=126, gross 0.75, weekly, 10 bps, next-row)
with its gross scaled by `min(1, (b_s / b0) ** p)`, where `b_s` is the share of the PRICED,
INVESTABLE panel that is eligible (above 200d & vol20 < 0.60) at the segment's own **decision** row
`s`, applied from `s+1`. Two dials and no more: **p {0, 0.5, 1, 1.5, 2, 3} x b0 {0.30, 0.40, 0.50,
0.60, 0.70} = 30 cells per panel, 90 in all, every one published**, each with its **own
exposure-matched flat-gross control** (90 more books) and its own paired bootstrap. Panel
{U56, B136, SMALL} is a replication control, never selected on; the verdict is taken on U56.

## The premise is FACTUALLY TRUE and it still does not help
Breadth does move earlier and far more often than short fill. On U56's 923 post-warm-up decision
rows, breadth is below 0.50 at **162** rows and below 0.30 at **73**, against **98** short-fill rows,
and the low-breadth rows are exactly where the drawdown is made (2009: 14, 2022: 28, 2020: 5).
A throttle at b0 = 0.70 bites on **41.0%** of rows against short fill's 3.7%.

## The throttle DOES shallow the binding leg — and so does holding less equity for no reason
On U56 **every one of the 25 biting cells has a shallower MaxDD than the incumbent** (−19.13% →
−13.55% at p=3.0/b0=0.70) and **4b passes at 30 of 30 cells**. It buys the DD margin from +1.10 pp
to **+6.68 pp**. But the exposure-matched flat cut — the same weight frame at a CONSTANT gross equal
to the throttle's own realised mean target gross — **also passes 4b at 30 of 30** and gets from
−19.13% to −15.33% with no signal at all.

**THE CONTROL TEST IS A COMPLETE NULL.** Paired circular-block bootstrap (400 x 63 rows, seed
20260919, identical blocks): of the 25 biting U56 cells, **dSharpe is inside 2 SE at 25 and dMaxDD is
inside 2 SE at 25**. Across all three panels (75 biting cells) the largest |t| anywhere is
**1.59 on Sharpe and 1.93 on MaxDD** — not one cell reaches 2 SE. Mean throttle-minus-flat on U56:
dSharpe **−0.0003**, dMaxDD **+1.08 pp**, dCAGR **−0.57 pp**. This is idea 1189's fixed-Sharpe slide,
reproduced from a fifth direction: breadth timing sells CAGR to buy drawdown at unchanged Sharpe,
which is what the gross dial already does for free.

## What the throttle costs that the flat cut does not: TURNOVER
U56 annualised turnover runs **2.77 → 4.27 turns/yr** across the throttle grid while the matched flat
control runs **2.77 → 2.20**. At the most aggressive cell (p=3.0, b0=0.70) the throttle trades
**94% more than its own control** (4.27 vs 2.20) to reach a drawdown 1.78 pp shallower — a difference
inside 0.50 SE — and gives up 0.79 pp of CAGR and 0.024 of Sharpe doing it.

## B136 is the cleanest statement of the degeneracy: the control WINS
The throttle passes 4b at **6 of 30** B136 cells; its own exposure-matched flat cut passes at
**24 of 30**. On the second large-cap panel, de-grossing on a breadth signal is strictly worse than
de-grossing on nothing. SMALL is 0 of 30 both ways and fails on all five 4b legs.

## Rule 8 (parameters chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE)
Both declared choosers pick **p = 0 — the incumbent — on U56**, so the OOS delta is **+0.0000** and
the axis is null to an operator as well as to the bootstrap. On B136 the IS-Sharpe chooser moves to
p=0.5/b0=0.70 and **loses −0.0335 of OOS Sharpe**; on SMALL both choosers move and lose **−0.3195**
and **−0.2471**. The ex-post best OOS U56 cell (p=3.0, b0=0.60: OOS 14.54% / **1.2538** / −13.48%
against the incumbent's 17.34% / 1.1862 / −19.13%) is **reported, not claimed** — no declared chooser
reaches it, and its full-sample gap over its own matched flat is 0.09 SE.

**4a: 0 of 180 books** (the live RULES v2 book's −12.05% MaxDD is unreachable at any cell).
**Per-leg 4b failures over the 90 throttled books:** H2 49, H1 30, OOS 30, CAGR 30, DD 30 — U56 fails
**0 of 30 on every leg**, and every B136/SMALL DD failure is the panel, not the throttle.

## Gates
G1 p=0 is b0-invariant, worst spread **0.000e+00**. G2 the p=0 cell reproduces the committed
incumbent (CAGR 0.1582 vs 0.1579, Sharpe 1.1543 vs 1.1529, MaxDD −0.1913 vs −0.1913, OOS Sharpe
1.1862 vs 1.1837; worst |diff| **2.51e-03**, inside the tape-vintage floor, outside 5e-4 —
`data/prices.csv` is restated daily, idea 1272's finding). G3 at p=0 the matched flat control IS the
throttled book, **0.000e+00**. G5 mean target gross non-increasing in p at **15 of 15** ladders.
G4 the chooser reads no row ≥ 2017-01-01 (asserted in code). G6 exactly two tuned parameters.
Deterministic, offline, 28s.

## Survivorship (rule 9)
U56/B136 are CURRENT constituents; SMALL is the current sub-$2B screen less 54 tickers with
`max_1d_move >= 1.0`. Names that delisted, were acquired or went to zero are absent from every panel,
which flatters the books **and the breadth series itself** — a name that collapsed is not in
breadth's denominator, so this run measures the throttle on an optimistic signal and its null is if
anything generous. All 4b pass counts are upper bounds; throttle-minus-matched-flat is a difference
between two books on one panel and is first-order immune.

## What this adds to the record
A ninth consecutive mechanism (after 1253 phase, 1254 years, 1255 names, 1256 gate length, 1257
signal legs, 1369 cluster cap, 1377 rank hysteresis, 1395 entry throttle, 1399 short-fill handling)
that cannot move the incumbent's sole binding leg on its own account. The new content is the
**control**: this is the first run to price an exposure-timing mechanism against an exposure-MATCHED
flat cut rather than against the incumbent, and at matched exposure the timing is worth **nothing on
90 of 90 cells** while costing up to 94% more turnover. Any future 4b pass bought by de-grossing —
timed or not — should be reported against its own matched flat control before it is called a rule.
