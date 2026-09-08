# Idea 405 — price the levered sleeve against its own TURNOVER (lane C, 2026-09-08)

**Verdict: KILL (fee story).** The levered arm's Sharpe edge over the standing candidate does
not survive moving *either* fee tap one rung above the record's own convention.

Pre-registered question, decision rule, predictions and caveats are in the script docstring,
written before any number here was read. 896 arm-rows from 32 simulated paths; both fee taps
are exactly linear in the paths (cost identity asserted at `max|d| < 1e-15`), which is what
makes the surface solvable rather than re-simulated. Idea 402's committed grid reproduces on
128 shared rows × 8 columns at `max|d| 1.03e-05` (u56 price-cache drift, idea 401's DEFECT).

## Q1 — the premise is half right

The queue's "triples the incumbent's turnover (2.3× → 7.9×/yr)" is an **EWall** fact, not a
book fact. Turnover multiple LEV/INC by cell:

| base book | u56 S3 | u56 S4 | broad S3 | broad S4 | median |
|---|---|---|---|---|---|
| EWall | 3.447 | 3.517 | 3.414 | 3.479 | **3.463** |
| TOP20 | 1.605 | 1.611 | 1.438 | 1.445 | **1.525** |

Pure gross ratio is 1.667. So on EWall the lever roughly doubles turnover *beyond* what the
gross ratio explains (the sleeve rebalances against a near-static equal-weight base); on
TOP20, whose base book already turns over 9–12×/yr, the multiple is *below* the gross ratio.
P1 CONFIRMED. Cell median over all 8 is **2.51×**, not 3.4×.

## Q2 — the joint region

Cells (of 8) where LEV beats INC on Sharpe, rows = trading cost bps, cols = borrow bps/yr:

| c \ φ | 0 | 100 | 200 | 300 | 400 | 500 | 600 |
|---|---|---|---|---|---|---|---|
| **0** | 8 | 8 | 8 | 8 | 7 | 6 | 6 |
| **10** | 8 | 8 | 8 | **6** | 6 | 3 | 1 |
| **25** | 6 | 5 | 1 | **1** | 0 | 0 | 0 |
| **50** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

LEV wins at 104 of 224 (cell, rung) points, and the win set is a **prefix in financing inside
every cost row in 8 of 8 cells** — the region is a staircase, exactly P2. At the record's own
rung (c=10, φ=300) LEV beats INC in **6/8** cells (mean dSharpe **+0.0326**) and passes 4b in
**8/8** — P4 CONFIRMED. One rung up on cost (25/300) it wins **1/8**; one dial to the top on
borrow (10/600) it wins **1/8**. That is the pre-defined fee-story condition, met on both taps.
Note the comparand is not fee-immune either: INC's own 4b passes fall 8 → 8 → 6 → 2 across the
cost rungs, so at 50 bps neither book is a candidate.

## Q3 — the break-even frontier, and a correction to idea 402's headline

φ*(c), bps of borrow the Sharpe edge absorbs (NaN = never crosses inside 0–600):

| cell | c=0 | c=10 | c=25 | c=50 |
|---|---|---|---|---|
| broad/EWall/S3 | >600 | >600 | 319 | <0 |
| broad/EWall/S4 | >600 | 537 | 199 | <0 |
| broad/TOP20/S3 | >600 | 470 | 197 | <0 |
| broad/TOP20/S4 | >600 | 462 | 197 | <0 |
| u56/EWall/S3 | >600 | 513 | 181 | <0 |
| u56/EWall/S4 | >600 | 404 | 71 | <0 |
| u56/TOP20/S3 | 416 | 236 | never | <0 |
| u56/TOP20/S4 | 380 | 207 | never | <0 |

These reproduce idea 402's `be_sharpe` column to the digit on every shared cell. **But idea
402's published "median break-even 277 bps" is a median POOLED ACROSS ITS TWO COST RUNGS.**
Split by rung it is **466 bps at c=10** and **189 bps at c=25**. The single pooled number
understates the arm at the PROTOCOL rung by ~190 bps and overstates it at 25 bps by ~90 — a
number that decides an allocation should never be pooled over the dial it is most sensitive to.

Paired exchange rate (cells interior at both ends of a cost step, 7 paired cell-steps):
**median dφ*/dc = −18.2 bps of borrow per bp of trading cost** (range −22.6..−17.3). P3
CONFIRMED. The unpaired median-by-rung reads 398 → 462 → 197 and is *non-monotone*, a pure
composition artefact of which cells are interior at which rung; it is printed with that warning.

## Q4 — decomposition: which tap does the killing

Cell-mean dSharpe(LEV−INC) = zero-fee gap **+0.1469** (positive in 8/8, range +0.080..+0.228),
plus a trading increment invariant in φ (−0.0461 at c=10, −0.1155 at 25, −0.2316 at 50) plus a
financing increment invariant in c (−0.0227 per 100 bps). Additivity in Sharpe is not exact
but is tiny: max|resid| **6.6e-04**. At c=10/φ=300 the split is
**+0.0326 = +0.1469 − 0.0461 − 0.0682**, i.e. financing carries **59.7%** of the fee drag and
trading **40.3%**. The lever's own tap is the bigger one, but the turnover tap is not far
behind and it is the one that scales fastest: at c=50 trading alone (−0.2316) exceeds the whole
zero-fee edge.

## Q5 — rule 8 (walk-forward, arm chosen on 2009–2016 only, 2017–2026 read once)

The IS chooser tracks the fee surface: S0 picks LEV in 8/8 cells at (0,0), 4/8 at (10,300),
1/8 at (25,300) and 0/8 at c=50. **IS/OOS agreement on the LEV>INC call is 81.2%** of 224
points, and the OOS win region is *LARGER* than the IS one (111 vs 89) — **P5 REJECTED**: the
fee surface is estimated the same way in both windows, so the disagreement is edge noise, not
fee optimism, and it runs in the levered arm's favour out of sample.

At c=10/φ=300, cell means over 8 cells:

| | OOS CAGR | OOS Sharpe | OOS MaxDD | clears 3 OOS 4b bars |
|---|---|---|---|---|
| S0 (IS-Sharpe) | 12.92% | 1.1741 | −17.88% | 8/8 |
| S1 (IS-4b screened) | 12.84% | 1.1728 | −17.99% | 8/8 |
| INC (do-nothing) | 12.41% | 1.1498 | −18.15% | 8/8 |
| LEV (always) | 13.56% | **1.1866** | −18.02% | 8/8 |
| SPY | 15.45% | 0.8820 | −33.72% | — |
| RULES v2 (live) u56 | 9.53% | **1.2851** | −12.05% | — |
| RULES v2 (live) broad | 7.98% | 1.1185 | −12.24% | — |

**Both choosers LOSE to holding LEV unconditionally** (1.1741 / 1.1728 vs 1.1866): the IS
screen's only effect is to sell the arm in cells where it went on to win. And the live book
still beats every arm here on u56 OOS Sharpe at a third of the drawdown.

## KEEP paths

Over 896 rows: **4b 320, 4a (vs the LIVE RULES v2 book, cost-matched) 0, BOTH 0**; 4a against
v1 at a fixed 10 bps is 196 — the 4a comparand gap open idea 398 owns, here ∞× rather than
8×. No new KEEP, no RULES change. 4b by arm: INC 168/224, LEV 152/224, CTL 0/224, CTLg 0/224 —
the no-sleeve controls clear 4b **nowhere on this surface**, at any fee rung.

## What this settles, and what it does not

Settled: the levered f=0.60 arm is a **fee story** under the queue's own definition. Its edge
is real and large before fees (+0.147 of Sharpe, 8/8 cells), survives at exactly the record's
conventional rung, and is gone by 25 bps of trading cost or 600 bps of borrow. A real account
paying 25 bps all-in and 500 bps on margin — not an exotic account in 2023–24 — holds the
incumbent. Idea 402's PARK stands, and the reason is now priced rather than counted.

Not settled: **the cash-at-zero convention (open idea 406) is worth the entire frontier here.**
INC holds mean cash 0.250 and LEV borrows mean 0.250, so crediting cash at k bps moves φ*
against LEV at ~1.00 bps per bp. Idea 406's first rung (150 bps) would cut every φ* above by
~150 bps, taking the c=10 median from 462 to ~312 and putting the record's own rung on the
frontier. Every φ* in this file is an **upper bound**. That correction is idea 406's to make,
and it should be made before any levered sleeve is priced again.
