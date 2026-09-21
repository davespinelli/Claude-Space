# Idea 2075 (lane C, 2026-09-21) — DOES THE 4:1 ASYMMETRY RATIO MATTER, OR IS ANY TIGHT DOWN-TRIGGER THE SAME?

**Verdict: ANSWERED — THE ASYMMETRY MATTERS, THE RATIO DOES NOT.  Plus two KILLs: DOWN-ONLY is
not a strategy on this construction, and `C_ISDD` is not a legal chooser.  NO NEW KEEP: the
standing KEEP-4b candidate is not displaced.**  Script
`2026-09-21_asymmetry-ratio-ladder_C.py`, gates **13/13**, 13,344 scored rows (3,336 cells x 4
cost rungs) published in `.grid.csv.gz`.

## What was asked

Idea 2026 PRE-STATED the drift trigger's down/up ratio at 4:1 and found it worth +1.01 / +0.61 pp
of OOS MaxDD for -0.33 / -0.16 pp of OOS CAGR at +0.26 / +0.23 turns/yr — but never laddered the
ratio.  This run walks `A` over {1, 2, 4, 8, 16, DOWNONLY, UPONLY} at BOTH bases the record owns
(FIXH `b = h`; FRACG `b = f * g_t`), sets `h_up = b`, `h_dn = b / A`, and asks where the drawdown
credit saturates, where the CAGR cost binds, and whether a down-only trigger dominates.

EXACTLY TWO tuned dials: `A` x the family's own BASE rung.  `t` is PRE-STATED at the inherited
0.16 and no chooser ever reads the `t` ladder; TRADE cadence, PANEL and COST are reported, not
tuned.  Both KEEP paths scored at every cell; rule 8 read once.

## Headline 1 — the asymmetry is worth ~7 of 60 cells; the RATIO between 2 and 16 is worth ~1

Paired against each base's OWN symmetric twin, `t* = 0.16`, 10 bps, 60 (arm x base) pairs
(U56/B136 x W/M x 8 `h` + 7 `f` rungs).  Full table in `.profile.csv`:

| A | dOOS MaxDD | dOOS CAGR | dOOS Sharpe | dturn/yr | 4b passes (of 60) | pp DD per pp CAGR |
|---|---|---|---|---|---|---|
| 1 (symmetric) | — | — | — | — | **52** | — |
| 2  | **+0.708 pp** | -0.201 pp | +0.0094 | +0.103 | **59** | **3.52** |
| 4 (pre-stated) | +0.810 pp | -0.292 pp | +0.0100 | +0.156 | **59** | 2.77 |
| 8  | **+0.938 pp** | -0.315 pp | +0.0110 | +0.181 | 58 | 2.98 |
| 16 | +0.818 pp | -0.349 pp | +0.0091 | +0.192 | 58 | 2.35 |

The whole 4b pass-count move is the FIRST step: 52 -> 59 going from symmetric to ANY asymmetric
rung, then 59 / 59 / 58 / 58 across a factor of EIGHT in `A` — a spread of 1.7% inside the
asymmetric ladder against 11.9% for the ladder including `A = 1`.  **V4 TRIGGERED on the ladder as
a whole and NOT on its interior: the pre-stated 4 carries no information over 2, 8 or 16.**

## Headline 2 — V1 NOT TRIGGERED: the credit does not saturate monotonically, it PEAKS and REVERSES

The pre-stated saturation clause required the OOS MaxDD credit to be non-decreasing in `A`.  It is
not: it runs +0.708 -> +0.810 -> +0.938 -> **+0.818**, peaking at `A = 8` and giving back 0.120 pp
at 16 (-14.6% of the whole 1 -> 16 move).  87% of the peak credit is already collected at
**A = 2**, the first rung off symmetric.

## Headline 3 — V2 TRIGGERED: the CAGR cost is MONOTONE, so the ladder keeps paying after it has stopped buying

OOS CAGR runs -0.201 / -0.292 / -0.315 / -0.349 pp, strictly worsening at every rung, as does
turnover (+0.103 -> +0.192 turns/yr) and refresh rate (+3.7 -> +12.9 /yr).  Credit saturates;
cost does not.  The exchange rate (pp of OOS MaxDD bought per pp of OOS CAGR surrendered) is
therefore **best at A = 2 (3.52)**, and 4 is the WORST rung but one (2.77 against 2.98 at 8 and
2.35 at 16).  **If the record ever wants the asymmetry, the defensible rung is 2, not 4.**  No
rung drives `L5_CAGR` negative at a pre-stated base (2 of 60 cells at `A = 1`, 0 at `A = 2/4/16`,
1 at `A = 8`), so the CAGR FLOOR never actually binds here — the cost is real but sub-critical.

## Headline 4 — KILL: a PURE DOWN-ONLY trigger is not a strategy, it is a one-way ratchet

**V3-pure NOT TRIGGERED BY CONSTRUCTION, and this is the run's sharpest structural fact.**  In
ideas 1799 / 2026 the drift trigger is the book's ONLY channel for re-reading `g_t`: the scheduled
trade day re-spreads the NAMES at the scalar already in force but never re-reads it.  Deleting the
up-side threshold therefore deletes the book's only RE-ENTRY channel.  Measured, not argued: mean
gross 0 and turnover 0 on **60 of 60** cells (gate G10: **360 of 360** over the whole `t` ladder),
failing 4b on four legs at once everywhere.  The question "does down-only dominate?" has no
return-based answer on this construction.

**POST-HOC REPAIR, DECLARED AS SUCH.**  The two `_TD` rungs — which restore re-entry by letting the
scheduled trade day re-read `g_t` — were added AFTER the first run of this script, once the pure
rung came back degenerate.  They are the nearest WELL-DEFINED "no up-side threshold" book and V3 is
re-read on the MATCHED pair `DOWNONLY_TD` vs `A1_TD`.  It still fails: weak dominance on all four
of {OOS Sharpe, OOS MaxDD, OOS CAGR, turnover} on **1 of 60 pairs (1.7%)**, pooled dCAGR **-0.198
pp** and 4b on **55 vs 58** of 60.  It buys OOS Sharpe (+0.0035) and turnover (-0.185/yr) and pays
for both in return.  **DOWN-ONLY DOES NOT DOMINATE.  The up-side threshold is earning something.**

The mirror control says the same thing from the other side: `UPONLY` (down trigger deleted) never
de-grosses — crash-window gross 0.94-1.00 against 0.22 for every two-sided rung — runs OOS MaxDD
-29.4% against -17.3%, and clears 4b on **0 of 60**, binding on `L4_DD` at every cell.  The
drawdown credit is entirely a DOWN-side object, and the UP side is what makes it investable.

## Headline 5 — incidental KILL: `C_ISDD` is not a legal chooser on any corpus admitting a cash cell

The rule-8 block exposes it mechanically.  `C_ISDD` maximises in-sample MaxDD, and a book holding
NOTHING has MaxDD exactly 0, so it picked the absorbing `DOWNONLY` book on **12 of 12** of its own
cells (100%) and on 12 of the 48 chooser cells overall.  Any corpus containing a zero-gross cell
turns `C_ISDD` into "hold cash".  The record has used `C_ISDD` as one of four legal IS-only
choosers since idea 2026; it should not be used where a de-grossing dial can reach zero.

## Rule 8 and capital (V5)

`(A, base)` chosen on 2009-2016 only, 2017-2026 read exactly once, 48 cells (3 panels x 2 cadences
x 2 bases x 4 choosers): **18 of 48 clear 4b FULL+OOS, 0 of 48 clear 4a.**  Excluding the 12
degenerate `C_ISDD` picks, 18 of 36.  The choosers land on `A = 4` 11 times, `A = 1` 8, `A = 2` 8,
`DOWNONLY_TD` 5, `A1_TD` 2, `A = 8` 2 — i.e. no rung of the ratio dial is reliably reachable, which
is the same ladder-fragility idea 2026 documented for the threshold itself.

**The PRE-STATED `A* = 4` cells clear 4b FULL+OOS on 8 of 12 large-panel cells, exactly as its
symmetric twin `A = 1` does (8 of 12).**  At the standing KEEP cell (U56, FRACG `f = 0.10`,
`t = 0.16`, monthly, 10 bps) the ratio makes the book WORSE on four of five legs:

| A | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | turns/yr |
|---|---|---|---|---|
| **1 (the standing KEEP)** | **15.81% / 1.2470 / -19.12%** | 1.2937 / 1.2055 | **16.55% / 1.2928 / -19.12%** | 1.42 |
| 2 | 15.28% / 1.2260 / -19.13% | 1.2681 / 1.1891 | 15.97% / 1.2684 / -19.13% | 1.53 |
| 4 (pre-stated) | 15.08% / 1.2177 / -18.96% | 1.2682 / 1.1726 | 15.62% / 1.2538 / -18.96% | 1.60 |
| 16 | 15.08% / 1.2206 / -18.85% | 1.2696 / 1.1769 | 15.64% / 1.2583 / -18.85% | 1.64 |

against SPY 15.12% / 0.8843 / -33.72% (OOS 15.26% / 0.8737 / -33.72%) and live RULES v2
8.62% / 1.2010 / -12.05% (OOS 9.46% / 1.2766 / -12.05%).  **NO NEW KEEP-4b CANDIDATE IS PUT
FORWARD: the standing `A = 1` book is not displaced by any rung of the ratio dial.**  Path 4a is a
KILL at every one of the 420 large-panel cells at `t*`, 10 bps, on every rung and both bases.

The pre-stated `A* = 4` book at the FIXH base (U56, `h = 0.12`, monthly) clears 4b at 0 and 10 bps
and FAILS at 25 and 50 on `L4_DD` — a narrower cost band than the standing `A = 1` KEEP, which
clears all four rungs.  The ratio makes the book MORE cost-fragile, not less.

## Caveats, stated

1. **Survivorship.** U56 / B136 are CURRENT-constituent lists; SMALL665 is a current sub-$2B
   screen (54 tickers with `max_1d_move >= 1.0` dropped first).  Every LEVEL is optimistic.  The
   RATIO contrast is same-tape / same-names / same-grid with only the trigger's two sides moved and
   is first-order immune; the PASS COUNTS are not.
2. **The `_TD` rungs are POST-HOC** and labelled so everywhere.  V1, V2 and V4 are pre-stated and
   unchanged; only V3's second reading is after the fact.
3. **No standard errors.**  Point estimates only.  Idea 2042 owns the 4b-leg SE question, and idea
   2060 has since found the CAGR-floor margin unresolvable at 95% on a paired block bootstrap — so
   the ~0.1-0.9 pp drawdown deltas tabulated above are almost certainly inside their own noise, and
   the DIRECTIONAL and STRUCTURAL findings (Headlines 1, 4, 5) are the ones this run stands behind.
4. `t* = 0.16` is INHERITED (idea 2026's caveat 3), not chosen here; the full `t` ladder
   {0.10, 0.12, 0.16, 0.20} is published in `.grid.csv.gz` so the inheritance can be audited.
5. The sigma convention is FIXED at (L=20, d=0); idea 1771 owns that surface.
6. SMALL665 clears nothing: 0 of 28 pre-stated cells on 4b and on 4a alike — sixth confirmation of
   the VOLTGT memo's A2.

## Gates (13/13)

G0 15.6y min; G1 idea 1799's U56 cell reproduced to 4.042e-07; G2 idea 2026's standing KEEP-4b cell
to 3.354e-05; G3 refresh rate non-decreasing in `A` on 360 of 360; G4 cost identity 0.000e+00;
G5 zero base (`b=0`, A=1) == CAL `R=D` at 0.000e+00; G6 gross never levered (max 1.000000);
G7 DOWNONLY refreshes <= A=1 on 360 of 360; G8 UPONLY likewise; G9 the 4:1 trigger refreshes >= its
symmetric twin on 360 of 360 (idea 2026's G8 restated); G10 pure DOWNONLY absorbing on 360 of 360;
G11 DOWNONLY_TD <= A1_TD on 360 of 360; G12 the trade-day re-read only ADDS refreshes on 360 of 360.

Artifacts: `.grid.csv.gz` (all 13,344 rows), `.profile.csv`, `.dominance.csv`, `.ratio_counts.csv`,
`.prestated.csv`, `.choosers.csv`, `.gates.csv`, `.log.txt`.
