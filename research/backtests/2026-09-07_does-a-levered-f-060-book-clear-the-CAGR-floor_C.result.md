# Idea 402 — does-a-levered-f-060-book-clear-the-CAGR-floor (lane C, 2026-09-07)

**Verdict: ANSWERED / PARK. YES — the f = 0.60 book clears the 4b CAGR floor as soon as the
gross is put back, and it does so while paying 300 bps/yr to borrow: 4b passes in 14 of 16
cells at g = 1.25, the SAME 14 cells the standing f = 0.25 candidate passes, missing the SAME
two (broad/TOP20 @ 25 bps, idea 138's empty-window cells). But the queue's second sentence is
only half right. The floor failure at high f IS just a return deficit — and yet the book is
NOT reducible to an exposure dial: the no-sleeve control clears 4b in only 4 of 16 cells (one
gross setting, g = 0.60, and only on u56/TOP20), and de-grossed to the incumbent's own CAGR it
LOSES by −0.069 Sharpe and −2.43 pp of drawdown in 16/16. What the levered arm does not survive is the
pre-registered KEEP bar: no single g passes 4b in all 16 cells, rule 8's IS-4b chooser clears
all three OOS bars in 12/16 (< 14), and the whole Sharpe edge over the incumbent has a
break-even borrow rate of a median 277 bps. No new KEEP, no RULES change.**

## What was run

1,728 arm-rows = 3 f-points × 12 g-points × 2 panels (u56, broad) × 2 base books (EWall,
TOP20) × 2 sleeve sets (S3 = TLT/GLD/UUP, S4 = +DBC) × 2 cost rungs (10, 25 bps) × 3 financing
rungs (0, 150, 300 bps/yr on borrowed notional), from 576 backtests — financing is a
deterministic daily charge on the realised drifted gross, so the three rungs are exact, not
re-simulated. Weekly, t+1, all net. **Two tuned parameters — f ∈ {0.00, 0.25, 0.60} and
g ∈ {0.40 … 2.00}; every point of both is reported.** Panels, books, sleeve sets, cost rungs,
financing rungs, selectors and both KEEP paths are reported axes, never selected on.

**Leverage convention, stated not buried.** PROTOCOL 2 permits leverage when the idea says so;
idea 402 does. Borrowing costs fin bps/yr on max(gross − 1, 0); cash earns **zero** at g < 1
(the record's standing convention, kept so these rows stay comparable with idea 138's). That
pairing is deliberately unkind to the levered arm — it pays to borrow but is never paid to
lend. Sharpe is rf = 0 throughout, as everywhere in this record.

**Gates before any new number.** (a) `run_lev` (H.run with every instrument removed and its
`s > 1.0` gross CAP removed — that cap is why the record could not price leverage at all) vs
`H.run` vs `engine.backtest` on both panels: max|d| **0.000e+00** on both comparisons.
(b) Idea 138's committed `.grid.csv` re-derived on its 48 shared rows: on the 40-row exact
subset (all f > 0, plus EWall at f = 0) max|dSharpe| **4.4e-16**. The 8 remaining rows differ
by construction and the difference is published, not hidden: idea 138's f = 0 TOP20 control is
the raw book (mean gross 0.747), this run renormalises every arm to exactly g because Q3 is a
matched-gross comparison — mean dSharpe **−0.0084**, i.e. **this run's TOP20 control is the
weaker one**, and every "sleeve beats control" count on a TOP20 cell is flattered by that much
and no more.

## Q1 — does f = 0.60 clear the floor at some gross? (yes, and the window's ends name themselves)

4b pass counts over 16 cells, at the headline 300 bps financing rung:

| g | 0.40 | 0.50 | 0.60 | 0.75 | 0.85 | 0.90 | 1.00 | 1.10 | **1.25** | 1.50 | 1.75 | 2.00 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f = 0.00 (control) | 0 | 0 | **4** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| f = 0.25 (incumbent) | 0 | 0 | 0 | **14** | 8 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| f = 0.60 | 0 | 0 | 0 | 0 | 0 | 2 | 7 | 11 | **14** | 3 | 0 | 0 |

Cell-mean curve at f = 0.60 (300 bps financing): CAGR 7.98% → 12.54% → 17.98% and MaxDD
−11.10% → −18.10% → −28.02% as g goes 0.75 → 1.25 → 2.00, against bars of CAGR ≥ 10.66% and
MaxDD ≥ −20.23%. **P2 confirmed exactly: the g-window is bounded BELOW by the CAGR floor in
16/16 cells and ABOVE by the DD cap in 16/16** — idea 401's crossing shape on a second dial,
found here by construction rather than by census. Median window width 2.5 of 12 g-points at
f = 0.60 (1.5 for the incumbent); 15/16 cells have a window with free money, 14/16 at 150 and
at 300 bps.

**P1 confirmed:** with free money Sharpe is flat in g (cell-mean range 0.0010 over 0.75→2.00,
slope +0.0008/unit g). Financing is the only thing that bends it: slope −0.078/unit g at
150 bps, −0.156 at 300. So the levered book's whole risk of ruin here is the borrow rate, not
the leverage.

## Q2 — the queue's second sentence, split in two

**On the return axis, yes.** At MATCHED CAGR with the incumbent (g* interpolated per cell,
mean 1.09–1.14), levered f = 0.60 beats f = 0.25 @ 0.75 on Sharpe in **14/16 cells (mean
+0.0659)** with free money, 13/16 (+0.0495) at 150 bps, **9/16 (+0.0261)** at 300 bps, and is
shallower on MaxDD in **16/16 at every rung** (mean +2.29 / +2.04 / +1.67 pp). Idea 138's
"f = 0.60 fails only the CAGR floor" is therefore a statement about how much risk the book
holds, not about what it earns per unit of risk.

**On the identity axis, no — and this is the finding that survives.** The same test run on the
NO-SLEEVE control is a clean loss: de-grossed to the incumbent's CAGR (mean g* **0.631**) it is
worse on Sharpe in **16/16** (mean **−0.0693**) and worse on MaxDD in **16/16** (mean
**−2.43 pp**). The gross dial alone is not *entirely* empty — the control does clear 4b in
**4 of 16 cells**, at exactly one gross (g = 0.60) and only on u56/TOP20 (12.30% / 1.1596 /
−18.40% @ 10 bps; note that at f = 0 the S3 and S4 rows are the same book, so those 4 cells are
2 distinct books) — but that is against **14/16** for the incumbent and **14/16** for the
levered f = 0.60 arm, and the DD cap binds at every other gross in every other cell. At matched
gross, gross by gross (max |Δ mean realised gross| 1.1e-3, so this is never an exposure
comparison), f = 0.60 beats the control on Sharpe in **16/16 at all 12 g-points** with free
money (mean +0.134) and in 16/16 up to g = 1.10 even at 300 bps (15/16 at 1.25, 13/16 at 2.00),
and is shallower on MaxDD in **16/16 at all 12 g-points at every financing rung** (mean
+13.1 pp at g = 0.75, +19.8 pp at 1.25). **A de-grossed equity book reaches the 4b class only
in one corner of the panel space; the sleeve reaches it nearly everywhere, so the sleeve is not
a de-grossing in disguise.**

## Q3 — rule 8 (parameters on 2009–2016, 2017–2026 read once)

| selector | picks | mean OOS Sharpe | OOS CAGR | OOS MaxDD | all 3 OOS bars |
|---|---|---|---|---|---|
| CTL f = 0.00, g = 0.75 | fixed | 1.0497 | 14.26% | −24.16% | 0/16 |
| INC f = 0.25, g = 0.75 (idea 139) | fixed | 1.1092 | 11.89% | −18.20% | **14/16** |
| S0 IS-Sharpe argmax, f = 0.60 | g = 1.00 (16) | **1.1833** | 10.76% | −14.62% | 7/16 |
| S1 IS-4b screened, f = 0.60 | g = 1.25 (9), 1.00 (2), 1.10 (1), abstains 4 | 1.1771 | 12.51% | −17.14% | **12/16** |
| S2 joint (f, g) IS-margin argmax | 0.90 (7), 1.25 (5), 0.85 (2), … | 1.1176 | 13.61% | −20.17% | 8/16 |

(300 bps rung; with free money S1 is 1.2261 / 13.33% / −17.43% and 14/16, abstaining twice.)
S1 beats the incumbent's OOS Sharpe in 8/12 non-abstaining cells (mean +0.0278) at 300 bps,
13/14 (+0.0781) with free money. **P5 was wrong in direction**: the chooser's OOS is *better*
than the incumbent's, not merely close — but it abstains in 4 cells at the headline rung, and
an abstention is a failure to produce a book, not a neutral result.

## Q4 — the financing break-even (the number the answer actually turns on)

Solved per cell by bisection on the borrow rate:

| arm | break-even for the SHARPE edge over the incumbent | break-even for 4b itself |
|---|---|---|
| best-margin g per cell | median **277 bps** (range 0 … 1183) | median **831 bps** (range 0 … 2527) |
| fixed g = 1.25 (S1's modal pick) | median **221 bps** (0 … 658) | median **831 bps** (0 … 1507) |

So: the levered book keeps *passing 4b* until borrowing costs ~8.3%/yr, but stops being *better
than the book we already have* at ~2.8%/yr — inside the range a real account pays. Four cells
(all at 25 bps trading costs) have a break-even of **0 bps**: there the incumbent is already
ahead before any financing is charged.

## KEEP paths

**4b:** 199 of 1,728 arm-rows (65 at 300 bps), all at f = 0.25 with g ≤ 0.90, f = 0.60 with
0.90 ≤ g ≤ 1.50, or f = 0.00 at g = 0.60 (4 cells, 2 distinct books, both u56/TOP20). **4a (vs the LIVE RULES v2, cost-matched,
PROTOCOL 3):** 135 of 1,728 (45 at 300 bps), every one at f = 0.60 with g ≤ 0.85 or f = 0.25
with g = 0.40. **BOTH: 0 of 1,728.** Idea 138 found the two paths disjoint on the f dial; this
run shows **the gross dial does not merge them either, and says why**: 4a needs drawdown no
worse than the live book's −12%, which wants LOW gross; 4b needs 70% of SPY's CAGR, which wants
HIGH gross. They pull the same dial in opposite directions. Against RULES v1 at a fixed 10 bps
(the record's older convention) the 4a count is 615 of 1,728 — a **4.6×** comparand gap on
identical rows, more evidence for open idea 398.

## The two headline books, side by side (EWall / S3 / 10 bps, 300 bps financing)

| panel | book | CAGR | Sharpe | MaxDD | halves | OOS Sharpe | OOS CAGR | turnover | 4b |
|---|---|---|---|---|---|---|---|---|---|
| u56 | INC f = 0.25, g = 0.75 | 11.22% | 1.2331 | −16.67% | 1.327/1.160 | 1.2211 | 11.51% | 2.29× | ✓ |
| u56 | **f = 0.60, g = 1.25** | **12.45%** | **1.2894** | −16.81% | 1.361/1.229 | **1.2577** | 12.37% | **7.90×** | ✓ |
| broad | INC f = 0.25, g = 0.75 | 11.93% | 1.2370 | −18.50% | 1.372/1.118 | 1.1959 | 11.62% | 2.33× | ✓ |
| broad | **f = 0.60, g = 1.25** | **13.19%** | **1.3294** | −17.55% | 1.461/1.210 | **1.2598** | 12.50% | **7.97×** | ✓ |

SPY over the same slice: 15.23% / 0.889 / −33.72%, halves 0.957/0.834, OOS 0.882 / 15.45%.
Live RULES v2 (u56 @ 10 bps): 8.66% / 1.206 / −12.05%. The levered arm is better than the
incumbent on every column here **except turnover, which it triples** (2.3× → 7.9×/yr) — the
cost rung is already charged, but a 3.4× turnover multiple is where a 10-bps assumption would
hurt most if it is wrong.

## Verdict against the PRE-REGISTERED decision rule

(i) a single (f = 0.60, g) passing 4b in all 16 cells at 300 bps: **NONE** (best is g = 1.25 at
14/16 — the same 14/16 the incumbent itself manages, missing the identical two cells, so this
bar was one the standing candidate never met either; the rule stands as written).
(ii) S1 clears all three OOS bars in **12/16** (< 14). (iii) S1 mean OOS Sharpe − incumbent's:
**+0.0679** ✓. Two of three ⇒ **PARK**.

## Caveats, stated not buried

Survivorship (idea 54): current constituents on both panels inflate the equity leg more than
the ETF sleeve, so the control is flattered and Q2's control result is *understated*.
Financing is a FLAT rate over 2009–2026, not a path — no funding series is cached and the
sandbox has no network — so it overcharges 2009–2015 and undercharges parts of 2022–2026; the
0/150/300 bracket is a range, not a curve, and the break-even numbers above are the honest way
to read it. MaxDD is one number off one path (idea 321) and the window's upper end is set by
exactly that number, so a single episode moves the ceiling of the g-window. The sleeve is 3–4
ETFs over one macro regime (idea 139 risk (a)); leverage does not make that sample larger, it
makes a bad draw from it cost 1.67× more. Idea 128's IS-window caveat biases S1 toward
admitting too much gross. t+1 only (idea 126); calendar-day index (idea 38); realised mean
gross printed on every row and matched to 1.1e-3 across arms (idea 127).

## Follow-ups proposed

- **404** — the 4a/4b paths pull the gross dial in opposite directions (0 of 1,728 rows pass
  both, with the DD-vs-live-book bar wanting low gross and the CAGR-vs-SPY bar wanting high):
  census the record for any book that has EVER passed both, and if none exists, PROTOCOL 4
  should say so rather than implying the paths are alternatives.
- **405** — the levered arm triples turnover (2.3× → 7.9×/yr) for a Sharpe edge whose
  break-even borrow rate is 277 bps: price the same g-window at 0/10/25/50 bps trading cost
  and report the joint (financing, trading-cost) region where it beats the incumbent.
- **406** — cash earns 0 in this record while borrowing costs 300 bps; every de-grossed book in
  the LEADERBOARD is therefore priced with a free option foregone. Re-price the standing 4b
  candidates crediting cash at a flat 150 bps and report how many 4b margins change sign.

Files: `2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C.py` + `.grid.csv` (1,728
rows) `.window.csv` (144) `.matched.csv` (48) `.walkforward.csv` (288) `.breakeven.csv` (32)
`.keeppaths.csv` (334) `.console.txt`.
