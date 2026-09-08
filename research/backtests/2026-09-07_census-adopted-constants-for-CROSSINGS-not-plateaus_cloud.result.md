# Idea 401 — census the record's adopted constants for CROSSINGS, not plateaus (cloud, 2026-09-07)

Script: `2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.py`
Outputs: `.console.txt`, `.grid.csv` (620 arm-rows), `.shape.csv` (62 dial-cells), `.walkforward.csv`, `.keeppaths.csv`
Run launched 2026-09-07 UTC; finished just after the 09-08 UTC rollover.

## Verdict — ANSWERED, and the queue's framing needs splitting in two

**Plateau and crossing are not opposites, and 20 of the record's 29 plateau dial-cells are both.**
Of 62 (panel, book, cost, dial) cells over the six adopted constants: **29 are PLATEAUS** by idea
128's own statistic (plateau_frac ≥ 0.71), **35 are C1 crossings** (≥2 monotone 4b margins with
opposing trend signs), **21 are C2 crossings** (a strictly interior 4b window whose lower and upper
edges are set by *different* bars). The cross-tab is PLATEAU×C1 = 20 both / 9 plateau-only /
15 crossing-only / 18 neither. A flat Sharpe curve and a two-sided admissibility window are
compatible — indeed the `gross` dial is the extreme case, 12/12 plateau AND 12/12 C1, because
Sharpe is invariant in gross while CAGR rises and MaxDD deepens monotonically (idea 311).

**The thinness result is the smaller number, and it is the one that bites:** the adopted value's
binding 4b margin is thinner than one grid step of that same bar in **13 of 62 cells (21.0%)**, and
the full 4b verdict flips at an immediate neighbour in **9 of 62 (14.5%)**. Median thin_ratio 3.44,
so the typical adopted constant is *not* knife-edge — but the ones that are, are concentrated.

## Calibration (the gate on the whole census)

Idea 138's f dial is re-measured here and **reproduces exactly**: plateau_frac **0.167** on idea
138's published 6-point sweep (they published 0.167), **0.346** on the full 13-point dial including
the f=0 control (their own 'all' scope, 12 pts ex-control: 0.375). C1 8/8, C2 7/8, mono_S median
0.833, Sharpe argmax f≥0.50 in 8/8, worst-of-five-margin argmax f=0.25 in 4/8 and 0.15–0.25 in 7/8.
Idea 138's reading of its own dial is confirmed on an independent implementation.

**SCOPE CAVEAT the census has to carry:** `plateau_frac` is a property of the GRID, not of the
function — the same f dial reads 0.167 on 6 points and 0.346 on 13. Every cross-dial plateau_frac
comparison in the record (including idea 128's 0.71 median, which this census uses as its cut) is
only meaningful with the point set stated.

## Per dial (12 cells each; f 8, n 6)

| dial | adopted | plateau_frac med | PLATEAU | mono_S med | C1 | C2 | 4b window width med | THIN | FLIP1 | adopted passes 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| band | 3% | 1.000 | 7/12 | 0.750 | 0/12 | 0/12 | 0 | 0/12 | 0 | 2/12 |
| gross | 0.75 | 1.000 | 12/12 | 1.000 | 12/12 | 5/12 | 0 | 4/12 | 2 | 2/12 |
| K | 200d | 0.643 | 6/12 | 0.800 | 5/12 | 2/12 | 0 | 2/12 | 1 | 2/12 |
| vol | 0.60 | 0.438 | 3/12 | 0.857 | 7/12 | 7/12 | 1.5 | 3/12 | 4 | 6/12 |
| f | 0.25 | 0.346 | 1/8 | 0.833 | 8/8 | 7/8 | 4 | 2/8 | 2 | 7/8 |
| n | 20 | 0.250 | 0/6 | 0.750 | 3/6 | 0/6 | 0 | 2/6 | 0 | 0/6 |

Three readings the record should carry forward:

1. **The `band` dial is the one clean plateau** — 7/12 plateau, C1 **0/12**, C2 **0/12**, THIN
   **0/12**, FLIP1 **0**. RULES v2's adopted 3% band is the only adopted constant in this census
   whose neighbourhood is flat in Sharpe *and* not squeezed by opposing bars. It is also the one
   with the smallest step_delta (median 9.37 ratio), i.e. the dial where a grid step barely moves
   the binding bar.
2. **`gross` is a plateau AND a crossing, and that is the whole point of idea 311** — Sharpe
   invariant (mono_S 1.000 with a tiny range), CAGR and MaxDD moving monotonically in opposite
   admissibility directions. Its 4b "window" is a dial placement, not an edge. 4/12 THIN.
3. **The only dials with non-degenerate 4b windows are `f` (median width 4) and `vol` (1.5).**
   Every other dial's median window width is **0** — the adopted constant does not sit inside a 4b
   interval at all on most cells.

## Where the thinness sits

Per panel: u56 **7/22** THIN (ratio median 1.27), broad **6/22** (2.81), small **0/18** (12.96 —
the small panel fails every bar by a wide margin, so nothing there is close). Per dial, thinness
concentrates on `gross` (4/12), `vol` (3/12), `n` (2/6), `f` (2/8), `K` (2/12), `band` (0/12).

Of the 19 cells where the adopted value clears all five 4b bars: **12** clear by more than one grid
step, **6** by more than two, **4** by less than half a step. The thinnest passing margin in the
whole census is **+0.0018 of CAGR (0.18 pp/yr)** — u56/EWall/25 bps at f=0.25, thin_ratio 0.36 —
which is idea 139's own standing KEEP candidate. Idea 138 already flagged that number; this census
confirms it is the thinnest published pass among all six adopted constants.

## Rule 8 (PROTOCOL 8) — dial chosen on 2009-2016 only, 2017-2026 read once

Three selectors over all 62 dial-cells. S0 = argmax IS Sharpe. S1 = argmax IS Sharpe among IS-4b
passers (abstain → control). S2 = S1 further restricted to values whose IS binding margin exceeds
one IS grid step — the THIN diagnostic used as a screening column, which is the natural follow-on
question and the reason this census is worth running at all.

| | OOS CAGR | OOS Sharpe | OOS MaxDD | vs control | vs RULES v2 | vs SPY | regret | abstains |
|---|---|---|---|---|---|---|---|---|
| S0 (IS Sharpe) | 12.09% | 0.9415 | −22.34% | −0.0087 (17/62) | −0.0525 | +0.0595 | 0.0365 | 0/62 |
| S1 (IS 4b-screened) | 13.10% | 0.9591 | −25.30% | +0.0088 (14/62) | −0.0350 | +0.0771 | 0.0189 | 35/62 |
| S2 (S1 + THICK) | 13.16% | 0.9581 | −25.61% | +0.0078 (12/62) | −0.0360 | +0.0760 | 0.0200 | 41/62 |
| control (no instrument) | 13.73% | 0.9503 | −26.91% | — | — | +0.0683 | — | — |
| adopted constant | — | 0.9285 | — | −0.0218 | — | +0.0465 | — | — |
| RULES v2 (live) | 7.15% | 0.9941 | −12.99% | — | — | +0.1121 | — | — |
| SPY | 15.45% | 0.8820 | −33.72% | — | — | — | — | — |

**The THIN screen is inert as a selector.** S2 vs S1: 15 of 62 picks move, paired mean ΔOOS Sharpe
**−0.0011**, and it buys 6 extra abstentions. It is a *description* of how much evidence a published
constant rests on, not a way to pick better constants. Report it; do not select on it.

Two further readings, both against the project's own interest:
- **The adopted constants underperform their own no-instrument controls out of sample** (0.9285 vs
  0.9503 mean OOS Sharpe), and S0 does too (0.9415). Only the 4b-screened selectors edge past the
  control, by +0.009, on 14 of 62 cells. This is idea 151's "does any selector beat doing nothing"
  finding reproduced on a sixth corpus.
- **RULES v2 (live) beats every selector and every control on OOS Sharpe** (0.9941) at a third of
  the drawdown, on a third of the CAGR. Nothing in this census threatens or improves it.

## KEEP paths

620 arm-rows. **4b: 75.** **4a against the LIVE RULES v2 book, cost-matched: 44.** **BOTH: 0.**
(4a against v1 at the same rung: 393 — an 8.9x comparand gap, the same defect open idea 398 names.)
No new book, no new KEEP, no RULES change. By dial: f 31/104 4b, vol 19/96, gross 10/228, band 9/72,
K 6/84, n 0/36. By panel at 4b: u56 58/224, broad 17/224, small 0/172.

## Reproduction gates (run before any new statistic)

- `H.run` vs `engine.backtest`, EWall, u56: **0.000e+00**. Parameterised band3/g200/vol60 gates vs
  idea 94's fixed gates: **0 differing cells** each.
- Idea 128's committed grid, 516 shared rows: **broad 2.220e-16, small 9.714e-17, u56 1.415e-05.**
- Idea 138's committed grid, 104 shared rows: **broad 2.220e-16, u56 9.797e-06.**

**A finding for the record, not a footnote:** the u56 rows reproduce only to ~1e-5 while broad and
small reproduce EXACTLY. `data/prices.csv` (the u56 panel's source) was rewritten by the
`Daily close 2026-09-07 [actions]` commit and the vendor restated its adjusted closes;
`data/prices_broad.csv` and `data/prices_small.csv` were not touched. Every cross-run
"max|d| 0.000e+00" claim in the record measured on u56 *before* a daily-close refresh is reproducible
only to that restatement. It is 50x smaller than the thinnest binding margin measured here (7.0e-04)
so it changes no verdict — but it is the same order as the record's thinnest published 4b margins,
and a census re-run against a refreshed cache would have to state it.

## Caveats

- **SURVIVORSHIP (idea 54):** three current-constituent panels; the small panel is a sub-$2B screen
  run today and back-filled to 2010 (tickers with `max_1d_move >= 1.0` in `data/small_meta.csv`
  dropped first, idea 118). It flatters the ungated/full-gross/wide end of every dial — the CONTROL
  end — and flatters every CAGR-floor margin, so **thinness is understated here, not overstated.**
- A "grid step" is a property of the PUBLISHED grid: a constant published on a coarse grid looks
  thin. THIN is a statement about the published evidence, not about the underlying function.
- Idea 38 (u56/broad calendar-day index) and idea 126 (t+1 only, no lag band) carry forward.

## Follow-ups proposed

407. `is-the-BAND-the-only-clean-constant-in-RULES` — the band dial is the census's only cell that is
     plateau, non-crossing, non-thin and non-flipping in 12/12. Test whether that survives finer band
     grids and other panels, since RULES v2's single adopted constant rests on it.
408. `publish-step_delta-beside-every-adopted-constant` — PROTOCOL currently quotes a margin with no
     scale. Propose the binding bar, its margin and its one-step motion as three required columns,
     and back-fill them over the record's committed KEEP rows.
409. `why-do-4b-windows-have-width-0-on-four-of-six-dials` — the adopted value sits inside a 4b
     interval only on `f` and `vol`. Test whether the other four dials have empty windows because the
     book fails 4b everywhere along them (an exposure fact) or because the window is off-grid.
