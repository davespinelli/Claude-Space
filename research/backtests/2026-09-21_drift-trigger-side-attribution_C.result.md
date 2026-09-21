# Idea 2030 (lane C, 2026-09-21) — DOES THE ASYMMETRY OF THE DRIFT TRIGGER CARRY THE WHOLE EFFECT?

**Verdict: ANSWERED — YES, AND CLEANLY. The DOWN side owns 104% of the OOS Sharpe credit and 96%
of the drawdown credit; the UP side owns 114% of the CAGR. But the half-rule is KILLED as a
REPLACEMENT (V3 not triggered: DOWN-only clears 4b at 121 of 270 cells against the two-sided 131,
and at 7 of 18 rule-8-reached arms against 11). It is PARKED as a CHEAPER, MORE COST-ROBUST
variant. NO NEW KEEP is put forward; the standing KEEP-4b candidate is not displaced.**
Script `2026-09-21_drift-trigger-side-attribution_C.py`, gates **11/11**, **6,000 scored rows**
(1,500 cells x 4 cost rungs) published in `.grid.csv.gz`.

## What was asked, and what makes this an attribution rather than a comparison

Idea 1799's drift trigger beat the turnover-matched calendar at 263 of 263 cells, mean **+0.0596**
OOS Sharpe / **+4.07 pp** OOS MaxDD for +0.31 pp CAGR — reproduced here to **8.9e-16** against the
committed grid (G5, 1,080 rows x 9 columns) and to the fourth decimal on the ruler itself (`SYM`
row below: +0.0596, win share 1.000). The trigger is SYMMETRIC, so it also delays RE-grossing, and
`L5_CAGR` was the binding leg at 38 of 420 cells. This run splits the trigger's sign condition:

    SYM      h_dn = h_up = h, trade day does NOT re-read     <- idea 1799's incumbent, verbatim
    SYM_TD   h_dn = h_up = h, trade day re-reads g_t         <- the matched two-sided control
    DOWN_TD  h_dn = h,  UP side deleted, trade day re-reads   <- intra-period DE-grossing only
    UP_TD    DOWN side deleted, h_up = h, trade day re-reads  <- intra-period RE-grossing only

The trade-day re-read is **PRE-STATED here** (idea 2075 added it post-hoc at a single `t`, and its
structural KILL is reproduced as a gate: a PURE down-only trigger never leaves zero gross, G8,
90 of 90 cells; a PURE up-only trigger never de-grosses in the 2020 crash, G9, min gross 0.784
against the two-sided 0.321). The re-read also buys an **exact zero point**: a threshold that never
fires IS the calendar book at the trade cadence, `TD-side (h -> inf) == CAL(R = T)`, gated to
**0.000e+00** at 90 cells (G6). So the attribution below is measured against one book that all
three sides collapse onto, and the interaction residual is published rather than assumed away.

## Headline 1 — the split is near-total and near-additive

Every side minus `CAL(R = T)`, 270 cells each, 10 bps (`.attribution.csv`):

| side | dOOS Sharpe | dOOS MaxDD | dOOS CAGR | dturn/yr | share of the two-sided credit |
|---|---|---|---|---|---|
| SYM (1799, no TD re-read) | +0.0571 | +4.47 pp | +0.26 pp | +0.50 | 117% / 103% / 120% |
| SYM_TD (two-sided control) | +0.0487 | +4.34 pp | +0.21 pp | +0.69 | 100% (the denominator) |
| **DOWN_TD** | **+0.0507** | **+4.15 pp** | **-0.01 pp** | +0.22 | **104% / 96% / -3%** |
| **UP_TD** | **+0.0025** | **+0.23 pp** | **+0.24 pp** | +0.28 | **5% / 5% / 114%** |

Interaction residual `SYM_TD - (DOWN_TD + UP_TD)`: **-0.0046** Sharpe (9.4% of the two-sided
move), **-0.04 pp** MaxDD (0.9%), **-0.02 pp** CAGR (11.2%). The two halves are close to additive
and each owns one axis outright. **The +0.0596 is a DOWN-side object; the CAGR is an UP-side
object.** V1 and V2 both TRIGGERED, on pre-stated thresholds.

On idea 1799's own ruler (turnover-matched calendar, 10 bps, `.matched.csv`), per panel:

| panel | SYM | SYM_TD | DOWN_TD | UP_TD |
|---|---|---|---|---|
| U56 | +0.0628 | +0.0262 | **+0.0527** | **-0.0144** |
| B136 | +0.0647 | +0.0299 | **+0.0507** | **-0.0109** |
| SMALL665 | +0.0516 | +0.0245 | **+0.0280** | +0.0075 |

The UP-only book is *worse than the calendar it replaces* on the two large panels. Three panels,
same sign.

## Headline 2 — V2's mechanism: the UP side is what keeps the CAGR floor off the book

4b CAGR margin `L5_CAGR`, 10 bps, 270 cells per side: **UP_TD +1.72 pp > SYM_TD +1.30 > SYM +1.26
> DOWN_TD +1.14**, and the leg BINDS at 90 / 101 / 98 / **113** cells respectively. Deleting the
up side costs 0.16 pp of CAGR margin and 12 more binding cells; deleting the down side buys 0.42 pp
and removes 11. Exactly the trade the idea predicted, and it is the reason V3 fails.

## Headline 3 — V3 NOT TRIGGERED: the half-rule does not replace the whole one at 10 bps

4b FULL+OOS pass counts (270 cells per side) and 4a, by cost rung:

| cost | SYM | SYM_TD | DOWN_TD | UP_TD |
|---|---|---|---|---|
| 0 bps | 159 / 4a 31 | 152 / 31 | 130 / 35 | 108 / 11 |
| **10 bps** | **136 / 30** | **131 / 30** | **121 / 34** | 89 / 9 |
| 25 bps | 119 / 22 | 118 / 22 | 117 / 24 | 85 / 9 |
| **50 bps** | 99 / 6 | 95 / 4 | **101 / 17** | 63 / 0 |

Paired DOWN_TD vs SYM_TD at the same cell: at 10 bps mean dOOS Sharpe **+0.0020** (win 48.5%),
weak dominance on all four of {OOS Sharpe, OOS MaxDD, OOS CAGR, turnover} at **14 of 270**; at
50 bps **+0.0179** (win 68.1%), weak dominance at **77 of 270**. The half-rule trades **0.471
fewer turns/yr** throughout. **It is not a replacement at the protocol's 10 bps, and it becomes
one only at a cost rung the protocol does not use — so it is PARKED, not promoted.**

`UP_TD` is the clearer KILL: `L4_DD` is its single binding leg at 73 of its 4b failures, its OOS
MaxDD averages **-23.41%** against the two-sided **-19.31%**, and it clears 4a at 9 cells against
30. Deleting the down side deletes the book's drawdown case.

## Headline 4 — rule 8: 2009-2016 chooses, 2017-2026 read exactly once

18 legal (panel x trade cadence x chooser) picks per family; `C_ISDD` is reported but excluded as
illegal per idea 2075. 4b FULL+OOS at the reached cell: **SYM_TD 11/18, UP_TD 9/18, SYM 7/18,
DOWN_TD 7/18, CALENDAR 1/18** (the calendar chooser lands on `R = M` at 18 of 18 and carries a
-30.36% mean OOS MaxDD — the third run this month to find the IS window preferring a slow gross
clock). **0 of 72 side picks clear 4a at any cost rung.** `SMALL665` clears 4b at **0 of 90** cells
on every side — the tenth confirmation that this family is a large-panel object.

The best reached cells (10 bps, all three legal choosers agree on U56 / T=W):

| cell | OOS CAGR / Sharpe / MaxDD | full | turns/yr |
|---|---|---|---|
| U56 T=W `SYM_TD` t=0.12 h=0.16 (C_ISLEGS) | 14.79% / **1.2971** / -16.44% | 13.85% / 1.2243 / -16.44% | 2.48 |
| U56 T=W `DOWN_TD` t=0.12 h=0.20 (C_ISLEGS) | 14.78% / **1.2975** / -16.44% | 13.80% / 1.2211 / -16.44% | **2.44** |

against live RULES v2 OOS 9.46% / 1.2766 / -12.05% and SPY OOS 15.26% / 0.8737 / -33.72%. Both
clear 4b FULL and OOS; **neither clears 4a**, and neither displaces the standing KEEP-4b candidate
(U56 FRACG f=0.10 t=0.16 M: full 15.81% / 1.2470 / -19.12%) — lower CAGR and lower full-sample
Sharpe for a better drawdown. **V4 is triggered but NO NEW BOOK IS PUT FORWARD**, and no memo is
written: minting one for `DOWN_TD` would contradict this run's own pre-stated V3.

## Headline 5 — the mechanism table, and why the two-sided trigger looked necessary

Gross through the 2020 window (U56, T=M, t=0.16, h=0.12; `.crash.csv`):

| side | pre-crash | trough | re-entry |
|---|---|---|---|
| SYM (1799) | 0.970 | 0.253 | **0.448** |
| SYM_TD | 1.000 | 0.197 | 0.356 |
| DOWN_TD | 1.000 | 0.197 | **0.222** |
| UP_TD | 1.000 | 0.197 | 0.356 |

All three de-gross identically — and `UP_TD` de-grosses too, because with the trade-day re-read the
**scheduled trade day** is already a de-grossing channel. What separates them is RE-ENTRY: the
down-only book comes out at 0.222 against 0.356, and that 13-point exposure gap over the recovery
is the whole of the CAGR cost in Headline 2. Once the trade day re-reads the scalar, the up-side
*threshold* has almost nothing left to do (it is worth +0.0025 Sharpe), which is why `DOWN_TD` and
`SYM_TD` sit within 0.002 of each other and why the original no-TD `SYM` — which defers the
re-gross to the trigger — is the best of the three at +0.0571.

## Gates (11/11)

G0 sample 18.7y; G1 calendar diagonal == `engine.backtest` 0.0; G2 cost identity 0.0; G3 standing
VOLTGT memo 4.6e-05; G4 `SYM h=0 == CAL R=D` 0.0 at 30 cells; **G5 `SYM` reproduces idea 1799's
committed DRIFT grid, 1,080 rows x 9 columns, max|d| 8.9e-16**; **G6 `TD-side (h -> inf) ==
CAL(R=T)` 0.0 at 90 cells**; G7 gross never levered (max 1.000000); **G8 / G9 replicate idea
2075's two structural KILLs**; G10 the h ladder moves refresh 0.8 .. 150.3 /yr.

## Limits

SURVIVORSHIP: U56 / B136 are current-constituent lists, SMALL a current sub-$2B screen (54 tickers
with `max_1d_move >= 1.0` dropped). Levels are optimistic and both 4b bars are easier here than on
a point-in-time panel; the SIDE contrast is same-tape / same-names / same-grid with only the
trigger's sign condition moved, so it is first-order immune, but the PASS COUNTS are not. The
attribution is conditional on the trade-day re-read: without it the down-only book is undefined
(G8), so "the DOWN side owns the effect" is a statement about a book that still re-reads its scalar
on its own trade calendar, not about a trigger in isolation. `SMALL665` contributes 0 of 360 4b
passes and its rows are diagnostic only.

Artifacts: `.grid.csv.gz` (6,000 rows), `.attribution.csv`, `.matched.csv`, `.walkforward.csv`,
`.crash.csv`, `.gates.csv`, `.log.txt`.
