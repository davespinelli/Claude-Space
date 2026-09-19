# Idea 1694 (lane cloud, 2026-09-19) — is the KEEP-4b pass a REBALANCE-CALENDAR-PHASE artefact?

**VERDICT: ANSWERED, and it is the largest unpriced dial the record owns. The standing U56
WEEKLY 4b pass is NOT a weekday artefact (5 of 5 phases pass at G = 1.00). But moving only the
day you LOOK — latency held fixed at t+1 — moves Sharpe by a mean of 0.0737 (max 0.1639) and
MaxDD by a mean of 4.33 pp (max 10.03 pp), against a standing candidate whose entire 4b
drawdown margin is 1.10 pp and whose Sharpe edge over its matched twin is 0.0089. B136's 4b
pass IS phase-dependent (2 of 5 weekly, 2 of 6 monthly) and U56's MONTHLY pass fails at one
phase of six. KILL as a new book (4a 0 of 66; every 4b passer is the already-committed G = 1.00
band book). PROTOCOL note proposed, no RULES change.**

Script: `2026-09-19_rebalance-calendar-phase_cloud.py`.
Outputs: `.console.txt .grid.csv .keeppaths.csv .walkforward.csv`.

## The defect this closes

Every book in this record rebalances on the **last trading day of the period**, because that is
what `engine.rebalance_mask` does. Nobody chose that anchor and no run has priced it. Idea 1590
found that ONE trading day of execution **latency** (trade at t+2) kills the standing 4b pass.
This run asks the neighbouring question nobody had: hold latency fixed at t+1 and move **the day
you look**.

## Construction

Two dials and no more:

1. **CADENCE** {W, M}
2. **PHASE** — W: the weekday anchor, the last trading day of the week whose weekday <= p, for
   p in MON..FRI (**p = FRI is exactly `engine.rebalance_mask(idx, 'W')`**). M: the k-th trading
   day of the month, k in {1, 5, 10, 15, 20, L} (**k = L is exactly `rebalance_mask(idx, 'M')`**).

Not dials, published at every cell: **PANEL {U56, B136, SMALL}** and **GROSS {0.75, 1.00}**.
Both gross values are PRE-REGISTERED FROM THE COMMITTED RECORD, not chosen by this run's results:
0.75 is live RULES v2, and 1.00 is the only gross at which the band book clears 4b FULL-and-OOS
in the record (ideas 1498 / 1649). **66 cells, every one published** in `.grid.csv`.

Book: live RULES v2 band 0.03, gross/N equal weight over in-band priced names, gated-out weight
to 0%-yielding cash, t+1, 10 bps. The ONLY thing that moves across cells is which day the
weights are recomputed and traded on.

## Gates — run before any new number is read

| Gate | What | Result |
|---|---|---|
| G1 | `phase_mask(W, FRI) == engine.rebalance_mask(idx,'W')` | **True** |
| G2 | `phase_mask(M, L) == engine.rebalance_mask(idx,'M')` | **True** |
| G3 | the local `bt()` replays `engine.backtest` at freq='W' | max \|d\| **0.000e+00** |
| G4 | the local `bt()` replays `engine.backtest` at freq='M' | max \|d\| **0.000e+00** |
| G5 | rebalance-day counts equal within a cadence | W: **977** every phase; M: **225** every phase |

## (1) The weekly anchor is robust. The monthly anchor is not.

Cross-phase spread within one (panel, gross, cadence) group — the book is otherwise identical:

| cadence | mean Sharpe spread | mean MaxDD spread | mean OOS Sharpe spread |
|---|---|---|---|
| **W (5 phases)** | **0.0416** | **1.69 pp** | **0.0374** |
| **M (6 phases)** | **0.1060** | **6.97 pp** | **0.1635** |

Pooled over all 12 groups: **mean Sharpe spread 0.0737 (max 0.1639), mean MaxDD spread 4.33 pp
(max 10.03 pp), mean CAGR spread 0.55 pp/yr, mean OOS Sharpe spread 0.1005.**

Put beside the yardsticks the record already owns: the standing 4b candidate's Sharpe edge over
its own matched-exposure twin is **0.0089** (idea 1617) and its entire 4b drawdown margin is
**1.10 pp** (idea 1511), against a paired DD-contrast SE of **2.93 pp**. **An unpriced calendar
choice moves the book by 8x-18x the Sharpe edge and ~4x the drawdown margin of every device the
record has ever certified.** The monthly cadence alone spans 6.95 pp of MaxDD.

The mechanism is visible: **M/D15 is the worst phase at 6 of 6 monthly panel-gross groups** (U56 G=1.00
Sharpe 1.1125 and MaxDD -24.36% against M/L's 1.1734 / -18.81%; SMALL G=0.75 0.5689 vs 0.7263).
Mid-month rebalancing of a 200d-band book is materially worse than month-end, and no run had
ever said so.

## (2) The 4b verdict flips on the phase at 3 of 12 groups

| panel | G | cadence | phases passing 4b FULL-and-OOS | anchor passes? |
|---|---|---|---|---|
| **U56** | 1.00 | **W** | **5 of 5** | yes |
| **U56** | 1.00 | M | **5 of 6** (M/D15 fails) | yes |
| **B136** | 1.00 | W | **2 of 5** (TUE, WED only) | **no** |
| **B136** | 1.00 | M | **2 of 6** (D1, D5 only) | **no** |
| all 8 other groups | | | 0 of n | no |

So: **the standing U56 weekly pass survives every weekday** — that is the reassuring half, and
it is the first time anyone has checked. **B136's 4b pass exists only at 2 of its 5 weekdays and
at neither of the two anchors the record actually quotes**, so any B136 4b claim that does not
name its phase is unadjudicable. **4a: 0 of 66 cells, on every phase and every cadence.**

## (3) The committed anchor is not a neutral draw

Ranking the anchor (FRI for W, L for M) by Sharpe inside its own phase set: **mean rank 2.00 of
a mean 5.5 phases, against a uniform expectation of 3.25; rank 1 or 2 in 8 of 12 groups**
(rank 1 at all four monthly groups on B136 and SMALL). The record's inherited last-trading-day
anchor is **systematically one of the better phases**, so every Sharpe the record has published
is quoted at a mildly favourable point of a dial nobody declared. This is a small upward bias in
every committed number, not a large one — but it is a bias, and it is free to state.

## (4) Rule 8 — phase chosen on 2010-2016 rows ONLY, 2017-2026 read ONCE

18 (panel, gross, chooser) picks, three legal IS-only choosers (argmax IS Sharpe, argmax IS
CAGR, argmax IS MaxDD):

- **0 of 18 picks land back on the committed anchor (W/FRI).**
- Mean OOS Sharpe of the picks **0.9188 vs the anchor's 0.9744 on the same cells (-0.0555)**.
- **3 of 18 picks clear 4b OOS; 0 of 18 clear 4a.**
- **C_SHARPE picks M/D15 on all four U56 and B136 cells**, and C_CAGR picks it on both B136
  cells — the phase that is *worst* out of sample (U56 G=1.00 OOS Sharpe 1.1121 against the
  anchor's 1.2759, **-0.1639**). On SMALL both choosers pick M/L, the anchor's own monthly
  phase, and gain (+0.0333).

**The IS-fitted phase is actively harmful**, which is the same end-seeking failure the record
has now found on N (idea 1639), gross (idea 1590) and cadence (idea 1586). The correct handling
of an unresolvable calendar dial is to leave it where it is and widen the error bar around every
number read off it.

## What the record should do

1. **Quote the rebalance PHASE beside every committed cadence or device verdict.** A verdict
   read at one phase of five or six is a verdict quoted at one draw of a dial with a 0.074
   Sharpe / 4.33 pp MaxDD spread.
2. **Use the cross-phase spread as the noise floor for cadence claims.** A cadence contrast is
   a contrast between two dials at once — the period AND the anchor inside it — and this run
   measures the anchor's own contribution at **0.0416 of Sharpe within the weekly cadence and
   0.1060 within the monthly one**. Any cadence verdict smaller than that is reporting its
   anchor, not its period.
3. **Do not re-tune the phase.** 0 of 18 IS-only choosers reach the anchor and the mean reach
   costs -0.0555 of OOS Sharpe.
4. **No RULES change proposed.** The live weekly book is phase-robust at its own panel; nothing
   here is a new book.

## Survivorship (rule 9)

U56 and B136 are current-constituent lists; SMALL is a current sub-$2B screen carried back to
2010, with 54 tickers dropped for `max_1d_move >= 1.0` (665 names remain). All three flatter the
long book. The phase contrast is *within* each panel, so the bias cancels out of the spread —
but not out of any level quoted here.
