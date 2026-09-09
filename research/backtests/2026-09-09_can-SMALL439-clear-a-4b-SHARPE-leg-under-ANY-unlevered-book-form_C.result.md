# Idea 575 — can SMALL439 clear a 4b SHARPE leg under ANY unlevered book form? (lane C, 2026-09-09)

**VERDICT: KILL.** 0 of 100 grid points clears the three 4b Sharpe legs; 0 of 100 clears 4a.
Idea 311's SMALL439 result generalises: the small panel's 4b failure is **form-invariant**, not
just gross-invariant.

## Setup
- Panel: 439 tradable sub-$2B names + SPY, 2010-01-04 .. 2026-09-04 (4,194 rows), names with
  `max_1d_move >= 1.0` dropped first. **SURVIVORSHIP: current constituents only — every level
  below is biased UP.**
- Tuned parameters (exactly 2): book FORM family x size dial n. Gross fixed at 0.75 for the
  screen; cadence (W/M) is a reported axis. 10 bps costs, t+1 fills, no shorting, no leverage.
- Menu (50 books): `EWall`, `MA-RS`, `MA-DG` (idea 311 anchors) + `TOP`, `MA`, `LOWVOL`,
  `IVOL`, `TRIM` (trend+trim), `SECT` (<=3 names per SIC major group) at n in {5,10,15,20,30,40,60}
  + `VT` (MA-RS vol-targeted, scales gross DOWN only) at targets {8,10,12,15,20}%.

## Gates
| gate | result |
|---|---|
| G1 `fast_backtest == engine.backtest` (MA20/W, returns and turnover) | PASS, max abs diff 2.50e-16 |
| G2 idea 311's 12 committed SMALL439 g=0.75 rows reproduce | PASS, max abs diff 8.33e-17 |
| G3 Sharpe span over g in [0.20,1.00], five families | max **0.0046** vs bar 0.0100 — H_GINVAR PASS |

G3 licenses the single-g screen: with the Sharpe legs g-invariant on this panel too, no
placement of gross can manufacture a Sharpe-leg passer.

## The bar and the result
SPY on this panel's days: CAGR 14.13%, Sharpe 0.8615, MaxDD -33.72%, H1 0.8907, H2 0.8577,
OOS Sharpe 0.8820. RULES v2 on the same panel: 3.80% / 0.571 (W), 4.64% / 0.663 (M).

| hypothesis | result |
|---|---|
| **H_MAIN** no book clears H1, H2 and OOS | **HOLDS — 0/100.** Leg failures: H1 87/100, H2 97/100, **OOS 100/100** |
| **H_NARROW** >=2 distinct legs are somewhere the sole blocker | **FAIL** — no cell fails only one Sharpe leg; the minimum is two (16 cells) |
| **H_DEFENS** a defensive form gets closest | **FAIL, and backwards** — best closest-leg margin by family: TOP -0.158 > MA -0.166 > SECT -0.174 > EWall -0.245 > MA-RS -0.249 > MA-DG -0.294 > IVOL -0.337 > LOWVOL -0.350 > TRIM -0.409 > **VT -0.419** |
| **H_4A** no book clears 4a vs RULES v2 on this panel | **HOLDS — 0/100** |

Best cells: highest full-sample Sharpe TOP15/W 0.7798 (CAGR 16.01%, MaxDD -31.12%, H1 0.9911,
H2 0.6628); highest OOS Sharpe **0.8465** (TOP5 = MA5 = SECT5, monthly) against SPY's 0.8820 —
the panel's ceiling on the binding leg sits **below the bar**. The DD leg passes in only 2/100
cells (MA-DG at both cadences, MaxDD -14.3%/-16.6%) and both of those fail the CAGR floor.

Vol-targeting works mechanically and does not help: VT8/W reaches the menu's best MaxDD
(-21.70%) but its CAGR falls to 1.97% and its added turnover leaves Sharpe at 0.3372.

## Rule 8 walk-forward (2010-2016 chooses, 2017-2026 read once)
| cadence | selector | pick | IS Sharpe | OOS CAGR / Sharpe / MaxDD | baseline OOS Sharpe | SPY OOS Sharpe |
|---|---|---|---|---|---|---|
| W | IS-Sharpe-max | LOWVOL5 | 1.1228 | 0.26% / **0.0789** / -30.57% | 0.5665 | 0.8820 |
| W | IS-Sharpe-max, IS half-legs | LOWVOL5 | 1.1228 | 0.26% / 0.0789 / -30.57% | 0.5665 | 0.8820 |
| M | IS-Sharpe-max | LOWVOL10 | 1.1136 | 2.86% / **0.3097** / -23.35% | 0.6194 | 0.8820 |
| M | IS-Sharpe-max, IS half-legs | LOWVOL10 | 1.1136 | 2.86% / 0.3097 / -23.35% | 0.6194 | 0.8820 |

The IS-best small-panel book is a low-vol trap: IS Sharpe 1.12 with a -9% IS drawdown becomes
OOS Sharpe 0.08 with a -31% OOS drawdown. Both selectors pick it; it loses to the panel's own
RULES v2 baseline and to SPY on every OOS metric.

## Reading
The queue asked whether idea 311's SMALL439 result was a property of its six-form menu. It is
not. Across ten families, seven sizes and two cadences the **OOS Sharpe leg fails everywhere**
and no book gets within one leg of passing. Because Sharpe is g-invariant here (G3), there is
no dial left to turn: on this panel, over this sample, an unlevered long-only small-cap book
does not clear PROTOCOL 4b, and the reason is the panel's risk-adjusted return level, not the
book's construction. No capital candidate, no memo, no rules change.

Artefacts: `.grid.csv` (all 100 points), `.ginvar.csv`, `.wf_W.csv`, `.wf_M.csv`,
`.walkforward.csv`, `.sicmap.csv` (the SIC snapshot the SECT form used — idea 565 showed the
source file is rewritten nightly), `.console.txt`.
