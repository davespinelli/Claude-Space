# idea 2506 (lane C, run 63, 2026-09-23) — result memo

**IS THE CANDIDATE'S 2% NAME CAP A CONCENTRATION CONTROL, OR A DISGUISED BREADTH-LINKED GROSS
SCHEDULE?  ANSWERED = IT IS A GROSS SCHEDULE, PROVED AS AN IDENTITY.  CONFIRM of CAP2 on 4b
(0 of 168 arms dominate it; it carries the most 4b of any shape).  KILL of the smooth
generalisation (every gain is re-grossing).  NO NEW KEEP CANDIDATE, NO RULES CHANGE.**

Script `research/backtests/2026-09-23_cap-as-breadth-linked-gross-schedule_C.py`, 192 published
rows (2 panels x 8 shapes x 3 gross x 4 rungs), 48 distinct realised weight paths, **17 of 17
gates pass**.

## 1. The identity, asserted rather than claimed (G7 / G10 / G11)
`min(g/N_in, c)` is the SAME number for every held name, so **a cap on an already-equal-weight
book can never de-concentrate it**: the max-minus-min held weight is **0.000e+00** on all 48
paths.  What the cap does instead is pin target risk gross to **`min(g, c x N_in)`**
(max|d| **2.9e-15**, float summation precision), i.e. constant GROSS above `N_in = g/c` names and
constant WEIGHT-PER-NAME (`= c`) below it (max|w - c| over binding rows **0.000e+00**).

## 2. The ladder spans the record's own two headline books (G14 — not expected)
Writing the family as `G_t = g x p_t^alpha`, `p_t = N_in/N_priced`:
* **alpha = 0 IS CAND**, the uncapped candidate (constant gross) — max|d| **0.000e+00** (G8).
* **alpha = 1 IS `baseline.rules_v2_weights`, THE LIVE BOOK** — max|d| **3.47e-18**, every panel
  and gross (G14).
So **the standing candidate's cap is a KINKED INTERPOLATION BETWEEN THE LIVE BOOK AND THE
UNCAPPED CANDIDATE**, and the A1.00 arm priced here differs from the 4a baseline by the SHY sweep
ALONE.  Measured, not assumed: that sweep is worth **+0.50 pp CAGR / +0.0667 Sharpe / +0.57 pp
MaxDD on U56 and +0.52 / +0.0697 / +0.59 on B136** — an independent reproduction of idea 2227's
+0.50 pp.

## 3. The kink is panel-size dependent — the one wording defect this run found
The kink sits at a fixed NAME COUNT `g/c`, not a fixed breadth.  The IDENTICAL "2% cap at gross
0.75" therefore binds **29.7% of U56 days and 5.2% of B136 days**, and at gross 1.00 on U56 it
binds **93.8%** of days — at which point the book is the live book's schedule wearing a gross-1.00
label.  Any memo taking CAP2 to a Sunday review should say what the clause does.  **PROPOSED
wording, NOT applied here (rule 6 — RULES.md, scan.py, bot.py and baseline.py are untouched):**

> Size each in-band name at `min(gross / N_in, 0.02)` of NAV, where `N_in` is the number of names
> inside the band that day.  Equivalently and preferably stated: hold every in-band name at the
> same weight and set portfolio risk gross to `min(gross, 0.02 x N_in)`.  This is a BREADTH-LINKED
> GROSS SCHEDULE, not a per-name concentration limit: because every in-band name already carries
> the same weight, the 2% clause never binds on one name relative to another.  Its kink sits at
> `N_in = gross / 0.02` names, so its effect depends on the size of the traded panel and must be
> re-stated (or re-expressed as a breadth fraction) if the panel changes.

## 4. What the generalisation actually bought: nothing that was not exposure
**0 of 168** arms dominate the committed CAP2 cell on all five of (CAGR, Sharpe, MaxDD, OOS
Sharpe, turnover).  Of the 96 smooth arms, **all 64 with dSharpe > 0, all 74 with dOOS_Sharpe > 0
and all 84 with dTurn < 0 carry dGross < 0** (median -0.119 / -0.137 / -0.135); rank
corr(dCAGR, dGross) = **+0.982**.  Restricted to the **40 gross-neutral arms** (|dGross| <= 0.02)
the median dSharpe is **-0.0109** and only 12 of 40 improve.  This is the thirteenth instance of
idea 2477's finding: on this book the deltas track realised risk gross, not device design.

## 5. Both KEEP paths, and the first 4a passes in the capped family's record
**4b 43 of 192, 4a 41 of 192, joint 4a AND 4b 0 of 192.**  By shape (24 rows each) 4b runs
**CAP0.020 10**, A0.50 8, CAP0.030 6, CAND 6, A0.25 5, A1.00 5, CAP0.015 3, A2.00 0 — **the
committed kink carries the most 4b of any shape on the ladder**.  Cross-panel (same cell on U56
AND B136): 4b **16 of 96**, including CAP0.020 / g0.75 at 0, 10 and 25 bps.  4a is **15 of 96**
cross-panel and is ENTIRELY a de-grossing phenomenon: 33 of the 41 4a rows sit at gross 0.50,
their mean CAGR is **7.57% = 49.8% of SPY's**, and **L_CAGR fails on 0 of 41** — i.e. every 4a
pass here is a book PROTOCOL 4b was written to reject.  4a's binding leg elsewhere is MaxDD
(127 of 151 failures).

## 6. Rule 8 — and the chooser's defection
Two dials (shape, gross) fitted on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE, 16 picks across
2 pre-stated IS-only choosers.  **16 of 16 beat SPY's OOS Sharpe, 12 of 16 beat the LIVE book's,
12 of 16 carry a full-sample 4a, 0 of 16 carry a full-sample 4b.**  **All 16 picks land on gross
0.50**: given a shape dial, the IS chooser defects to the lowest gross on the ladder and therefore
selects a 4a book every time.  Shape is near-indifferent (KINK 7 / SMOOTH 9), exactly as
pre-stated before compute.  Benchmarks read once — U56: SPY OOS 15.45% / 0.8831 / -33.72%, live
RULES v2 OOS 9.51% / 1.2839 / -12.05%.  B136: SPY OOS 15.26% / 0.8737 / -33.72%, live RULES v2
OOS 7.85% / 1.1017 / -12.24%.

## 7. Survivorship (rule 9)
U56 / B136 are CURRENT constituents of their screens held from 2008, so absolute levels are biased
upward and 4b's `L_CAGR` floor is the most contaminated leg.  The shape-vs-shape contrast is
same-tape, same-day, same-names and first-order immune; the absolute 4b and 4a verdicts are not.
