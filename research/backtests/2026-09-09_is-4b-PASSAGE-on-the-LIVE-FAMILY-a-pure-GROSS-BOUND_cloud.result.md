# Idea 544 — is 4b passage on the LIVE family a pure GROSS BOUND? (cloud, 2026-09-09)

**VERDICT: ANSWERED — YES, and the answer is a KILL for capital. On the live DEGROSS family
4b passage is exactly a one-sided gross bound: the drawdown bar NEVER binds (0 of 1,728
DEGROSS grid points fail it), so the admissible set is always `[g*, 1.00]` and passage is
literally the single number g*. But g* sits at 0.9179–0.9694 (U56) and 0.9292–0.9936 (B136)
— 17–24 pp above the live 0.75 — the window is 0.6–8.2 pp of gross wide (median 5.0 pp), and
the IS→OOS drift of that same threshold is 7.9–10.0 pp, i.e. LARGER than the window it has to
land in. A number you cannot estimate to better than the width of its own target is not a
number you can size a book with. RULES v2 unchanged; no new KEEP. RULES.md, scan.py, bot.py,
baseline.py untouched.**

Script: `research/backtests/2026-09-09_is-4b-PASSAGE-on-the-LIVE-FAMILY-a-pure-GROSS-BOUND_cloud.py`
Artefacts: `.grid.csv` (3,456 books), `.thresholds.csv` (36 cells), `.walkforward.csv`, `.console.txt`.

## What was priced

The live book is `unit_book(band) × gross`, so the family has exactly one scalar dial once the
band is fixed. Two pre-registered parameters, every point reported, none selected on:

| dial | values |
|---|---|
| GROSS RESOLUTION | coarse 0.05 (20 pts), fine 0.01 (96 pts), bisection to 1e-4 |
| BAND | 0.00, 0.01, 0.02, **0.03 (live)**, 0.05, 0.08 |

Fixed: weekly cadence, 10 bps, next-day execution, gross capped at 1.00 (PROTOCOL rule 2, no
leverage), IS ≤ 2016-12-31 / OOS ≥ 2017-01-01. DEGROSS is the live construction and the only
one a KEEP may come from; RESPREAD is reported as a control. 96 × 6 × 2 × 3 panels = 3,456 books.

### Gates (all passed before any verdict was read)

- **G1** vectorised runner vs `engine.backtest`, live U56 v2 book: max abs diff **1.735e-17**.
- **G2** `unit_book(0.03, DEGROSS) × 0.75` vs `baseline.rules_v2_weights`: **0.000e+00**.
- **G3** idea 542's premise reproduces **12/12** required cells: at gross 0.75, DEGROSS, on both
  U56 and B136 and on every band, `fail4b == "CAGR"` and nothing else.

### The premise, measured

- **C1 Sharpe invariance.** Max span of full-sample Sharpe over the whole 96-point gross grid is
  **0.0022** across all 36 (panel, band, construction) cells (DEGROSS max 0.0010, OOS span max
  0.0045). Consistent with idea 542. It is *not* exactly zero, and the reason is mechanical:
  de-grossing parks the residual in cash at 0%, and the sleeve drifts between weekly rebalances,
  so the mix is not a pure scalar.
- **C2 Monotonicity.** CAGR and |MaxDD| are monotone in gross at **0/3,420** adjacent violations
  each. The interval characterisation is therefore exact, not approximate.

## The answer

**4b passage on this family is one-sided, on every non-empty cell, on every panel.**

| panel | shape (DEGROSS, 6 bands) | g\* range | window width | 4b points / 96 |
|---|---|---|---|---|
| U56 | one-sided 6/6, two-sided 0/6, empty 0/6 | 0.9179 – 0.9694 | 0.031 – 0.082 | 4 – 9 |
| B136 | one-sided 4/6, two-sided 0/6, **empty 2/6** | 0.9292 – 0.9936 | 0.006 – 0.071 | 0 – 8 |
| SMALL439 | empty 6/6 | — | 0 | 0 |

The DD bar fails on **0 of 1,728** DEGROSS grid points across all three panels, so `g_DD = 1.00`
everywhere and the upper edge of the admissible set is always the no-leverage cap, never a
drawdown constraint. The queue's framing is correct: on this family 4b is one number wide.

On the **live band 0.03** the number is **g\* = 0.9179 (U56)** and **0.9935 (B136)** — the live
gross of 0.75 misses by **16.8 pp and 24.4 pp** respectively. B136 at the live band clears 4b at
exactly **1 of 96** grid points.

**SMALL439 cannot pass at any gross.** All three Sharpe legs fail on all 576 DEGROSS points
(H1 576/576, H2 576/576, OOS 576/576) — the small-cap panel's problem is not sizing.

**Resolution matters.** A 0.05 grid overstates g\* by up to **0.0471**; the 0.01 grid by up to
**0.0099**. Both errors are of the same order as the window itself, so any threshold in the
record quoted off a coarse gross ladder is a rounding, not a number.

## Rule 8 — the threshold is not estimable, and that is the verdict

Gross chosen on IS (≤ 2016) alone as the smallest value clearing the IS CAGR bar subject to the
IS DD bar; OOS read once.

| cell | g\*_IS | g\*_OOS | drift | OOS CAGR (SPY / live v2) | OOS Sharpe (SPY / live) | OOS MaxDD (SPY / live) | full 4b |
|---|---|---|---|---|---|---|---|
| U56 b0.08 | 0.9855 | 0.8855 | **−0.1000** | 12.00% (15.38 / 9.51) | 1.1811 (0.8786 / 1.2817) | −18.65% (−33.72 / −12.05) | **PASS** |
| B136 b0.02 | 0.9741 | none | > +0.026 | 10.50% (15.45 / 9.53) | 1.1400 (0.8820 / 1.2851) | −15.69% (−33.72 / −12.05) | FAIL (CAGR) |
| B136 b0.03 | 0.9684 | none | > +0.032 | 10.32% (15.45 / 9.53) | 1.1196 (0.8820 / 1.2851) | −15.59% (−33.72 / −12.05) | FAIL (CAGR) |
| B136 b0.05 | 0.9647 | none | > +0.035 | 10.25% (15.45 / 9.53) | 1.0963 (0.8820 / 1.2851) | −16.67% (−33.72 / −12.05) | FAIL (CAGR) |
| B136 b0.08 | 0.8872 | 0.9659 | **+0.0787** | 9.93% (15.45 / 9.53) | 1.1131 (0.8820 / 1.2851) | −17.35% (−33.72 / −12.05) | FAIL (CAGR) |
| U56 b0.00/0.01/0.02/0.03/0.05, SMALL439 ×6 | — | — | — | no gross ≤ 1.00 clears the IS bars | | | no pick |

**1 of 12** required band-cells has an IS-chosen gross that clears full 4b, and it is not the
live band. Median |drift| **0.0894** against a median window width of **0.0503** — the
estimation error is 1.8× the target. On B136 three of the four cells with an IS pick have **no
admissible gross at all** in the OOS window, so the IS threshold points at an empty set.
The one passer (U56 b0.08) overshot its own OOS threshold by 10 pp and cleared anyway; that is
luck inside a one-sided interval, not estimation.

## Both KEEP paths, and the exclusion gap

| panel | construction | n | pass 4a | pass 4b | pass BOTH |
|---|---|---|---|---|---|
| U56 | DEGROSS | 576 | 72 | 39 | **0** |
| U56 | RESPREAD | 576 | 0 | 110 | **0** |
| B136 | DEGROSS | 576 | 0 | 11 | **0** |
| B136 | RESPREAD | 576 | 0 | 67 | **0** |
| SMALL439 | DEGROSS / RESPREAD | 1,152 | 0 | 0 | **0** |

**0 of 3,456** points clear both paths, extending idea 404's census. On the live U56 band 0.03
DEGROSS cell the exclusion now has an exact width: 4a passes for gross **0.05–0.76**, 4b for
gross **≥ 0.9179** — a bare gap of **0.158 in gross (1.21×)** with nothing admissible inside it.

## Survivorship

All three panels are current constituents — universe.json, universe_broad.json, and
`prices_small.csv.gz` less the 44 tickers with `max_1d_move ≥ 1.0`. No delistings. Because the
only binding 4b bar here is CAGR, and survivorship inflates CAGR, **every g\* above is a lower
bound on the gross a real book would have needed**, and the windows above are upper bounds on
their true width. The finding gets worse, never better, with honest data.

## What this changes

Nothing in RULES v2. It closes the question idea 542 opened: the live family's distance from 4b
is a single scalar, it is roughly "be fully invested", and it cannot be estimated out of sample
to the precision passage demands. Raising live gross from 0.75 toward 0.92–0.99 to chase 4b
would be fitting one number to the in-sample CAGR level of a survivorship-inflated panel.
