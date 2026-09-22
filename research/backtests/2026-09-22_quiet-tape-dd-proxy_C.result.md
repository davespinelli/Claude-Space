# Idea 2083 — does the NON-EPISODE DRAWDOWN have an EX-ANTE PROXY worth CAPITAL?

**Lane C, 2026-09-22.**  **ANSWERED — YES, ON U56 AND ONLY AT THE TIGHT END: an EX-ANTE
quiet-tape drawdown chooser closes idea 911's 1.95 pp DD miss and leaves a KEEP-4b CANDIDATE
(U56 MADIST top-40, gross 1.00, monthly — OOS 16.24% / 1.310 / −17.67%) that is robust to
0–50 bps AND to an extra day of signal staleness; + a KILL of the quiet-tape mask as a GENERAL
device** (it changes the pick at 72.2% of grid points but does not lower mean OOS drawdown, and
reaches 4b on 1 of 3 panels).  Script: `2026-09-22_quiet-tape-dd-proxy_C.py`.  Grid
`.grid.csv` (93 rows, **all published**), shelf `.shelf.csv`, cost × lag ladder `.ladder.csv`
(16 rows), gates `.gates.csv`, console `.log.txt`.

## What was priced
Idea 911's shelf verbatim — 80 books per panel (MOM/MOMVS/MADIST/LOWVOL × k∈{5,10,20,40,ALL} ×
gross∈{0.25,0.50,0.75,1.00}), monthly, fills t+1, 10 bps, gate close>200dMA & vol20<0.60 — on
U56 / B136 / SMALL665 (54 names dropped for max_1d_move ≥ 1.0), 18.7 / 18.7 / 16.7 y.
911's residual was measured on a series spliced against a **hindsight-labelled** crash calendar.
This run replaces that calendar with a **CAUSAL** SPY-only distress series and takes each book's
drawdown on the quiet days only.

**Two tuned dials, every value reported.**  DEFINITION ∈ {`NEARHI_EXP` (SPY drawdown from its
expanding high), `NEARHI_252` (from its 252-day high), `VOL60` (SPY 60-day realised vol)} ×
THRESHOLD q ∈ {0.40, 0.60, 0.80, 0.90, **1.00**}; a day is quiet iff d_t ≤ quantile_q(d over
2009–2016).  **q = 1.00 keeps every day, so 911's own plain-MaxDD chooser is a grid point of this
study, not an outside comparand.**  Reported, not tuned: PANEL, chooser FORM (`QRESID` = argmax
residual of quiet-DD on IS beta across the shelf — 911's construction with the statistic swapped
in; `QRAW` = argmin quiet-DD), the `IS_SHARPE` reference, and the cost × lag ladder.

**Gates 8 of 9 PASS.**  G1 the q=1.00 `QRESID` pick reproduces 911's `IS_RESID` pick on all three
panels; G1b it reproduces 911's U56 OOS numbers to **0.0e+00** (17.4473% / 1.2174 / −22.1818%);
G2 a 100% SPY book reads beta 1.0000; G3 no leverage (max shelf gross 1.0000); **G4 the distress
series is CAUSAL** — recomputed on a tape truncated at the midpoint it equals the full-tape series
on the overlap to **0.0e+00**; G5 93 of 93 grid points published; G7 the ladder's lag+0 @10 bps
cell reproduces its grid row to **0.0e+00**.
**G6 FAILS, and the failure is localised, not waived:** q=1.00 keeps 2007/2007 (U56, B136) and
1502/1502 (SMALL) days under both `NEARHI_*` definitions but only **1987/2007 and 1482/1502**
under `VOL60`, because the first 20 sessions of each book window have no 60-day vol read.  So
`VOL60`'s q=1.00 point is a 20-day-truncated control, not the exact 911 control; the `NEARHI_*`
q=1.00 points are exact, and G1b is measured on one of those.

## V1 — TRIGGERED.  The ex-ante statistic closes the 1.95 pp, at q = 0.40
**3 of 24** U56 grid points with q < 1.00 clear 4b FULL **and** OOS (3 of 93 overall):

| definition | q | form | pick | FULL CAGR/Sharpe/MaxDD | OOS CAGR/Sharpe/MaxDD | DD margin |
|---|---|---|---|---|---|---|
| NEARHI_EXP | 0.40 | QRESID | **MADIST/40/g1.00** | 14.57% / 1.1965 / −17.67% | **16.24% / 1.3099 / −17.67%** | **+2.56 pp** |
| NEARHI_252 | 0.40 | QRESID | **MADIST/40/g1.00** | 14.57% / 1.1965 / −17.67% | **16.24% / 1.3099 / −17.67%** | **+2.56 pp** |
| VOL60 | 0.80 | QRESID | **MOMVS/40/g1.00** | 14.29% / 1.1946 / −18.17% | 15.51% / 1.2760 / −18.17% | +2.06 pp |

Against SPY (FULL 15.14% / 0.8851 / −33.72%, halves 0.9570 / 0.8264; OOS 15.29% / 0.8751 /
−33.72%) the MADIST pick clears every 4b leg: halves **1.1834 / 1.2098** both above SPY's, FULL
MaxDD −17.67% inside the −20.23% cap, FULL CAGR 14.57% above the 10.60% floor, OOS Sharpe 1.3099
above 0.8751, OOS MaxDD −17.67% inside −20.23%, OOS CAGR 16.24% above 10.70%.
**Both near-high definitions agree at q = 0.40** — the two are interchangeable on U56, picking the
same book at all five q. `VOL60` reaches a different but comparable book at q = 0.80.

**The dial matters and the failure mode is legible.**  At q ≥ 0.60 the near-high chooser falls
back to 911's own pick (`MADIST/ALL/g1.00`, OOS −22.18%, the −1.95 pp miss) at 8 of 24 points.
The whole gain is in the tight end: keeping only the calmest **803 of 2007** IS days (SPY within
0.91% of its running high) moves the pick from `k = ALL` to `k = 40`.  `QRAW` (no beta step)
degenerates at every point — it always picks a gross-0.25 LOWVOL book running 1.0–2.6% CAGR that
fails the 4b CAGR floor by 8+ pp.  **The beta-residual step is doing essential work.**

## V2 — NOT TRIGGERED.  The mask is not a no-op, but it is not a general improvement
Across the 72 (panel × form × definition × q<1.00) comparisons the quiet-tape chooser picks a
book **different from its own q=1.00 control at 52 of 72 points (72.2%)** — so the mask is
demonstrably not inert — but its **mean OOS MaxDD is −19.89% against the control's −19.69%, i.e.
0.20 pp DEEPER**.  The second clause of the pre-registered rule therefore fails.  Distinct books
reached across the 30 q<1.00 points per panel: U56 9, B136 9, SMALL 7.  **Reading: the quiet-tape
statistic does not make drawdown-at-matched-beta a better chooser in general; it makes it better
in one corner, and that corner has to be named in advance.**

## V3 — NOT TRIGGERED.  It is a U56 fact
4b FULL+OOS clears at **3 of 93** grid points and all three are U56; **0 of 62** non-U56 points
clear.  B136 misses the OOS DD leg by **7.96 to 10.50 pp** at every `QRESID` point (its best,
`MADIST/ALL/g1.00`, runs OOS 15.99% / 1.068 / −28.19%); SMALL665 misses by **15.03 to 27.79 pp**
and also fails the CAGR floor (best `LOWVOL/40/g1.00` OOS 5.92% against a 10.70% floor).
**4a: 0 of 93** — no pick beats live RULES v2's −12.05% drawdown, so nothing here touches the
live book on path 4a.

## Robustness at the clearing books — 16 of 16 cells hold
Cost {0,10,25,50} bps × signal lag {0, +1 day}, at both U56 books (`.ladder.csv`).  **All 16
cells clear 4b FULL+OOS.**  MADIST/40: OOS Sharpe **1.336 / 1.310 / 1.270 / 1.202** at
0/10/25/50 bps at lag+0 and **1.340 / 1.314 / 1.274 / 1.208** at lag+1; OOS MaxDD −17.62% →
−17.90% across the cost ladder and −19.56% → −19.83% at lag+1 (still inside the −20.23% cap, but
**the +1-day lag spends 1.9 pp of the 2.56 pp DD margin**).  MOMVS/40 behaves the same.
Turnover **3.09x/yr** (MOMVS 3.08x) against live RULES v2's **1.77x** — for contrast, the
2026-09-20 Sunday review's candidate turned 8.18x and lost its pass above 10 bps; **this one does
not**, which is the one respect in which it is a better object than the incumbent candidate.
Average gross 0.865, minimum 0.100 (the 200d-MA gate de-grosses to cash on its own; no leverage).

## Independent convergence with idea 2079 (lane cloud, same day, different chooser)
Discovered on the rebase, not by design: lane cloud's idea 2079 run reached a KEEP-4b candidate
of the **same family, width, panel and cadence** — U56 MADIST top-40, monthly, de-gross to cash —
at the **adjacent gross rung 0.75** (FULL 10.86% / 1.194 / −13.55%, OOS **12.08% / 1.308** /
−13.55%), via a completely different chooser (its residual *label-only* selector).  Two
independent IS-only choosers landing on the same (panel, family, k, cadence) cell at neighbouring
gross rungs, with OOS Sharpe **1.308 vs 1.3099**, is the strongest cross-run evidence this cell
has.  The two differ where it matters for 4b: at gross 0.75 the FULL CAGR margin is **0.26 pp**
(10.86% vs the 10.60% floor), which is why 2079 parked it; at **gross 1.00 the margin is 3.97 pp**
(14.57%) and the drawdown is still inside the cap (−17.67% vs −20.23%).  So the gross rung is the
live question for the Sunday review, and the two runs bracket it.

## Honest limits
1. **3 of 24 is a dial-dependent pass.**  Two of the three clearing points are the SAME cell
   reached by two near-interchangeable definitions, so the independent count is closer to **2**.
   This is a KEEP-*candidate*, not a promotion, and the Sunday review should treat the (definition,
   q) pair as a tuned choice that a real deployment has to fix in advance.
2. **No confidence interval was computed on the margin.**  Idea 2042 established that a 4b pass in
   a grid of this shape is a point estimate whose binding leg is usually unresolvable at 95%; the
   +2.56 pp DD margin here is wider than most it examined but **was not bootstrapped**, and the
   lag+1 cell shows 1.9 pp of it is spendable. **Filed as idea 2090**, not claimed here.
3. **The reached book is plain.**  Top-40 of a 56-name panel at equal weight is most of the panel;
   the chooser's content is "own nearly everything above its 200d MA, ranked by distance from it,
   at gross ≤ 1.00" — not an exotic object, and its 4b pass may be mostly the 200d-MA gate. **Filed as idea 2094.**
4. **Splicing still changes the statistic** (911's limit 1 survives in weaker form): a drawdown
   computed on quiet days only is not a drawdown any investor experienced.  What is new is that
   the MASK is causal, so the statistic is computable at the decision close — which is exactly
   what idea 2083 asked for and what 911's episode calendar was not.
5. **Survivorship (rule 9).**  U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT
   sub-$2B screen, so every CAGR and MaxDD LEVEL above is optimistic and both 4b bars are easier
   than on a point-in-time panel.  The chooser CONTRAST (quiet-tape vs plain IS MaxDD) is
   same-shelf / same-tape with only the day mask changed and is first-order immune; **the 3-of-93
   pass count is not.**
6. **Rule 8 was honoured:** both dials and the pick are functions of 2009–2016 only; 2017–2026 was
   read once, after the grid was fixed.  The `t+2` arm of an earlier draft of this script was
   discarded as mis-specified — shifting a MONTH-STEPPED weight frame by one day moves the trade to
   the next month-end, not the next day — and replaced by the signal-lag construction gated by G7.
