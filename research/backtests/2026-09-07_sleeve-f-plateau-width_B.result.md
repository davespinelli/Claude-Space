# Idea 138 — sleeve-f-plateau-width (lane B, 2026-09-07)

**Verdict: SPLIT. The queue's PREMISE is KILLED — the sleeve fraction is not a plateau dial, it
is a monotone ramp on which the no-sleeve control is DOMINATED (control above the whole sweep in
0 of 16 cells, below all of it in 13; idea 128's general case is above in 34 of 54, median control
percentile 0.86 vs 0.00 here). And the standing KEEP-candidate's f = 0.25 SURVIVES the test, but
for a reason idea 139's memo does not state: 0.25 is nowhere near the Sharpe argmax (0.60), it is
the argmax of the 4b MARGIN. No new book, no new KEEP, no RULES change; one memo correction.**

## What was run

208 arm-rows: 13 f-points × 2 panels (u56, broad) × 2 base books (EWall, TOP20) × 2 sleeve sets
(S3 = TLT/GLD/UUP, S4 = TLT/GLD/DBC/UUP) × 2 cost rungs (10, 25 bps), weekly, t+1, 0.75 gross,
all net. f = the queue's published sweep {0.05…0.25, 0.50} + {0.30, 0.35, 0.40} + an edge probe
{0.60, 0.75, 1.00}; **f = 1.00 is the pure sleeve, so the dial is bounded by construction and
ideas 240/256/328's grid-edge flag cannot apply to the reported argmax.** f = 0.00 is the
no-sleeve control. Tuned parameters: **two** — f (all 13 reported) and the sleeve set (both
reported). Panels, books, rungs, selectors and both KEEP paths are reported axes, never selected on.

**Gates before any new number.** (a) `H.run` (idea 94's simulator) vs `engine.backtest` on both
panels: max|d| **0.000e+00**. (b) Idea 134's committed `.grid.csv` re-derived on its 52 shared
rows: max|dSharpe| **2.2e-16**, max|dCAGR| **9.7e-17**, max|dMaxDD| **8.3e-17**. (c) Idea 139's
KEEP-candidate reproduced independently: u56 **11.22% / 1.2331 / −16.67%**, halves 1.327/1.160,
OOS **1.221**; broad **11.93% / 1.2370 / −18.50%**, halves 1.372/1.118, OOS **1.196** — the memo's
numbers to every published digit.

## Q1 — the queue's literal question (published sweep, Sharpe axis, 16 cells)

| statistic | this dial | idea 128's five other dials |
|---|---|---|
| control ABOVE the whole sweep | **0 / 16** | 34 / 54 |
| control strictly INSIDE | 3 / 16 | 15 / 54 |
| control BELOW the whole sweep | **13 / 16** | 5 / 54 |
| median control percentile | **0.00** | 0.86 |
| median Sharpe range | 0.1092 (min 0.0357, max 0.2311) | 0.091 |
| median `plateau_frac` (points within 0.05 of the cell's best) | **0.17** | 0.71 |
| f = 0.25 beats the control | **16 / 16** | (n/a) |

By book: EWall below-all **8/8**, TOP20 below-all 5/8 (inside 3). So **the answer to the queue is
that the plateau test does not apply here**: the range is ordinary but the shape is not flat —
`plateau_frac` 0.17 against idea 128's 0.71 — and the control is not somewhere inside the range,
it is the worst point of the dial. This is the first dial in the record whose no-instrument
control is dominated on Sharpe in every cell.

## Q2 — but the ramp does not stop at 0.25, and Sharpe is the wrong axis

Sharpe is **monotone increasing in f across the entire published sweep in 16 of 16 cells** (every
one of the 5 steps up in every cell; 14/16 still monotone once 0.30–0.40 are inserted), so on the
queue's own grid the Sharpe argmax is the edge f = 0.50 in **16/16**. With the
edge probe the true interior argmax is **f = 0.60 in 9/16**, 0.50 in 5, 0.40 in 2 — and MaxDD is
shallowest at **f = 0.75 in 16/16**. Cell-mean curve (all 16 cells):

| f | 0.00 | 0.10 | 0.20 | **0.25** | 0.30 | 0.40 | 0.50 | 0.60 | 0.75 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 1.066 | 1.089 | 1.117 | 1.131 | 1.145 | 1.172 | 1.194 | **1.196** | 1.098 | 0.342 |
| MaxDD | −24.1% | −21.7% | −19.3% | −18.2% | −17.1% | −14.9% | −13.0% | −11.1% | **−8.4%** | −21.1% |
| CAGR | 13.9% | 13.0% | 12.1% | 11.7% | 11.2% | 10.2% | 9.1% | 8.0% | 6.1% | 1.9% |
| worst 4b margin | −0.044 | −0.022 | −0.004 | **+0.0001** | −0.002 | −0.008 | −0.017 | −0.027 | −0.056 | −0.802 |

**Idea 128's finding 3 is confirmed on a new dial, in the opposite direction.** The 4b-margin axis
— the bar this constant is actually adopted for — is the only one with an interior optimum at the
adopted value: its argmax is **0.15–0.30 in 14/16 cells (0.25 in 6/16)**, and the cell-mean worst
margin is positive **only at f = 0.25**. Choosing f on Sharpe picks f ≥ 0.50, which **fails 4b in
16/16 cells** (the CAGR floor). 4b passes: 0 at f ≤ 0.05, 3/16 at 0.10, 8 at 0.15, 10 at 0.20,
**14 at 0.25**, 12 at 0.30, 6 at 0.35, 4 at 0.40, **0 at f ≥ 0.50** — idea 134's interior peak
reproduces on a different book set, shifted to 0.25.

## Q3 — rule 8 (f dialled on 2009–2016, 2017–2026 read once)

| selector (published sweep) | picks | mean OOS Sharpe | vs control | vs SPY | all three OOS 4b bars |
|---|---|---|---|---|---|
| S0 argmax IS Sharpe | 0.50 (15), 0.25 (1) | 1.1683 | **+0.1144**, positive 16/16 | 0.8820 | **2 / 16** |
| S1 IS-4b-screened | **0.25 (13), 0.20 (2)**, abstains 1 | 1.1255 | +0.0551, positive 15/15 | 0.8820 | **14 / 15** |

The f dial's IS→OOS rank ordering is **perfectly stable — median Spearman 1.000 across f in every
cell** — which is why S0's OOS-best f is its own pick in 15/16. Stability is not the same as
usefulness: S0 rides the ramp to the value that fails the CAGR floor. The one abstention and the
one S1 failure are both `broad / TOP20 @ 25 bps`, the two cells whose 4b window is **empty**.

## Materiality and the qualification the standing memo needs

The 4b window is interior and several grid points wide (median 4 points, range 0–7; empty in the
two broad/TOP20 @25bps cells), so idea 139's "not knife-edged in f" is **upheld as a window
statement**. It is **thin as a margin statement**: at f = 0.25 the binding bar clears by > 0.005 in
only **12/16** cells and by > 0.01 in **4/16**; on u56/EWall @25 bps the margin is **+0.0018**
(0.18 pp/yr of CAGR). The window exists because two monotone curves cross — Sharpe and drawdown
improve in f while CAGR falls — not because anything is flat. One grid step of f moves the binding
margin by 0.004–0.011, i.e. by more than the margin itself in most cells.

## KEEP paths

**4b:** 57 of 208 rows, all at 0.10 ≤ f ≤ 0.40. **4a (vs the LIVE RULES v2, cost-matched, per
PROTOCOL 3):** **11 of 208**, every one at f ≥ 0.50 and every one failing 4b. **Both: 0 of 208.**
Against RULES v1 at a fixed 10 bps — the record's older convention — the 4a count is **88 of 208**,
an **8×** gap on the same rows: more evidence for open idea 398, which owns the comparand.

## Caveats, stated not buried

Survivorship (idea 54): both panels are current constituents, which inflates the equity leg more
than the ETF sleeve — so it biases *toward* the control, and this run's finding that the control is
dominated is therefore understated, not flattered. Idea 128's IS-window caveat (the IS window's SPY
MaxDD is shallower than the OOS window's) biases S1 toward admitting too much. The sleeve is three
or four ETFs over one macro regime (idea 139 risk (a)); nothing here speaks to a sample with all
legs dead at once. t+1 only (idea 126); calendar-day index (idea 38); mean realised gross printed on
every row and flat at 0.7502–0.7503 throughout, so **none of this dial is an exposure effect**
(idea 127). MaxDD is one number off one path (idea 321).

## Follow-ups proposed

- **401** — the 4b window is a CROSSING, not a plateau: census the record's other adopted constants
  for the same shape (two monotone curves crossing) and report how many "windows" are crossings.
- **402** — f = 0.60 is the Sharpe argmax and fails only the CAGR floor: is the 4b-defensive class
  at high f just the sleeve's own low return, and does a levered f = 0.60 book clear the floor?
- **403** — the two empty-window cells are both broad/TOP20 @ 25 bps: is the window's existence a
  turnover-cost fact about the ranked book rather than a sleeve fact?

Files: `2026-09-07_sleeve-f-plateau-width_B.py` + `.grid.csv` (208 rows) `.plateaus.csv` (144 rows)
`.walkforward.csv` (96 rows) `.keeppaths.csv` (57 rows) `.console.txt`, and
`2026-09-07_sleeve-f-plateau-width_B_MEMO.md` (the correction to idea 139's memo point 6).
