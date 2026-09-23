# idea 2343 (lane C, 2026-09-23) — IS THE KEEP-4b CANDIDATE A 200d ARTEFACT? THE MA-LENGTH LADDER

**ANSWERED = NO. THE 4b PASS IS A PLATEAU, NOT A RIDGE. NO NEW KEEP CANDIDATE, NO RULES CHANGE.**

## The object and the grid
Idea 2300's standing 4b candidate `RG100 + phi = 1.00` — every name INSIDE the 200d +/-3% band
(clause 2, with hysteresis) held at `gross / N_in`, idle NAV swept to SHY — priced with the MA
length as a dial. **Two tuned dials and no more: L {100, 150, 200, 250, 300} and gross
{0.75, 1.00}.** Panels (U56 / B136 / SMALL), rungs {0, 10, 25, 50} bps, band c = 0.03, the weekly
cadence, t+1 execution and the sweep instrument are REPORTED, never selected on.
**30 books x 4 rungs = 120 published rows**, every one in `.grid.csv`.

## The answer: 4 of the 5 rungs pass on each large-cap panel
U56, gross 0.75, 10 bps — the live cell and its neighbours:

| L | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | 4b | turn/yr |
|---|---|---|---|---|---|---|---|---|
| 100 | 11.54% | 1.0878 | −22.01% | 1.29 / 0.91 | 10.63% | 0.9891 | **.** (L_DD) | 6.96 |
| 150 | 12.07% | 1.1557 | −17.77% | 1.31 / 1.03 | 12.02% | 1.1101 | **Y** | 5.23 |
| **200 (live)** | **12.59%** | **1.1934** | **−17.39%** | 1.24 / 1.17 | **13.85%** | **1.2397** | **Y** | 4.39 |
| 250 | 12.59% | 1.1861 | −17.50% | 1.27 / 1.13 | 13.52% | 1.1981 | **Y** | 3.91 |
| 300 | 12.24% | 1.1341 | −17.91% | 1.21 / 1.08 | 13.10% | 1.1510 | **Y** | 3.81 |

SPY over the same window: 15.23% / 0.8897 / −33.72% (so the 4b DD cap is −20.23% and the CAGR
floor 10.66%). B136 is the mirror image: L = 100/150/200/250 all pass at 0.75/10 bps and **L = 300
fails by 12 bps of drawdown** (−20.35% against the −20.23% cap). Only **L = 100 on U56** and
**L = 300 on B136** fail, both on `L_DD` alone, at the two ends of the ladder. **The pass set is a
contiguous interior plateau, not a knife edge at 200.**

## L = 200 is not the ladder's optimum, and the ladder's cost is second-order
Against the live cell (U56, 0.75, 10 bps): `dOOS_Sharpe` is −0.2506 at L = 100, −0.1296 at 150,
**−0.0416 at 250**, −0.0887 at 300. L = 200 is the OOS Sharpe *maximum on U56* but **not on B136**,
where L = 250 wins (12.66% / 1.1204 against 12.29% / 1.0994). Turnover falls monotonically with L
on all three panels (U56 6.96 -> 3.81 turns/yr), and max per-name weight falls with it too
(25.00% -> 12.50% at L = 250). **U56 / L = 250 / 0.75 is the only cell in all 120 rows that clears
4b at 50 bps** (10.84% / 1.0345 / −17.96%, OOS 11.72% / 1.0518) — reported, not selected on: the
50 bps rung is a reported axis, so switching the book onto it would be tuning on a reported dial.

## Rule 8 — (L, gross) fitted on <= 2016-12-31, 2017–2026 read ONCE. **0 of 24 picks land on L = 200.**
24 picks (3 panels x 4 rungs x {C_ISSHARPE, C_ISCALMAR}). Distribution: **L150 15, L300 5, L100 3,
L250 1, L200 0.** The IS choosers systematically prefer a SHORTER lookback than the committed one
and pay for it out of sample: on U56 at 10 bps the pick (L = 150) reads OOS **12.02% / 1.1101**
against the incumbent L = 200's **13.85% / 1.2397** — **−1.83 pp of OOS CAGR and −0.130 of OOS
Sharpe**. Picks beat SPY's OOS Sharpe at **15 of 24** and the live RULES v2 book's at **4 of 24**;
13 of 24 also pass 4b full-sample. **This is the honest caution of the run: the plateau means the
incumbent length is not fragile, but it does NOT mean an out-of-sample chooser would have found
it.** The committed L = 200 is a frozen convention that happens to sit near the top of its own
ladder, and that is a fact about the ladder, not evidence the chooser works.

## Both KEEP paths over all 120 rows
**4b 24, 4a 0.** By panel: U56 13/40, B136 11/40, **SMALL 0 of 40 on both paths at every rung** —
the same null 2322 and 2326 published for the cap and the floor. By rung: 8 / 8 / 7 / 1 at
0 / 10 / 25 / 50 bps. **Every 4b pass in the run is at gross 0.75**; gross 1.00 fails on `L_DD` at
all 5 lengths on all 3 panels. Dominant binding leg on 4b failures is `L_DD` (22–24 of the ~22–29
failures at every rung), then `L_CAGR` (5 -> 19 as costs rise). 4a being 0 of 120 repeats every
prior run on this family.

## The warm-in question, handled in the open
`band_state` is OUT before L closes exist, so L = 300 spends 39 days of the headline window forced
all-out. Section F re-scores the SAME return series on an equal-state window (index[360:], by which
L = 300 has 60 days of live band state): **4b passes go 24 -> 26 of 120**, L = 200 goes 6 -> 7 and
L = 250 7 -> 8, and no cell's verdict flips against the long lengths. **The ordering is not a
warm-in artefact** — if anything the headline window understates the long end.

## Gates — 13 of 13 pass
G0 >= 10y on all three panels (17.7 / 17.7 / 15.7 y). G1 per-column replica == `engine.backtest`
at **0.00e+00**. **G2 `band_state_L(200)` == `baseline.band_state` at 0 differing cells** (the
ladder's centre IS the live clause-2 object). G3 the L = 200 book == an independently constructed
`RG100 + phi = 1` at 4.44e-16. G4 no leverage (max row sum 1.000000000 over all 30 books).
G5 the dial bites (mean time-IN 0.659 -> 0.713 on U56, 6 of 6 cells move). G6 SHY priced on every
held row. G7 SMALL dropped 54 tickers at `max_1d_move >= 1.0`. G8 exactly two tuned parameters.
**G9 EXTERNAL REPRODUCTION of idea 2300's committed U56 headline** (12.55% / 1.1896 / −17.39%,
OOS 13.77% / 1.2332) read as 12.59% / 1.1934 / −17.39%, OOS 13.85% / 1.2397 — **max\|d\| 8.25e-04**,
the same price-cache vintage residual idea 2326 published, not a construction difference.

## Honest limits
U56 and B136 are current-constituent lists and SMALL is a current-screen panel, so **survivorship
(rule 9) flatters the CAGR side of every row here**; it applies equally along the ladder, so the
L-comparison is cleaner than any level. One band width (c = 0.03 — idea 2318 sweeps that), one
cadence (W), one phase, one delay (t+1), one sweep instrument (SHY), one re-gross exponent
(phi = 1.00). Costs are flat per unit turnover with no spread, impact or borrow, which matters
most at the high-turnover short-L end. Five lengths on a 50-point spacing: the plateau is
established at that resolution, not finer.

## Verdict
**ANSWERED = NO, THE PASS IS NOT A 200d ARTEFACT — PLATEAU, NOT RIDGE. No new KEEP candidate and
no RULES change:** nothing on the ladder beats the incumbent cell on the headline rung, rule 8
lands on L = 200 at 0 of 24, and the one rung that is more cost-robust (L = 250) is worse on OOS
Sharpe and is reachable only by selecting on a reported axis. **The standing candidate survives
its lookback dial; keep L = 200 frozen.**

Script: `research/backtests/2026-09-23_ma-length-ladder-on-the-4b-candidate_C.py`
Artefacts: `.grid.csv` (120 rows) / `.exposure.csv` / `.equalstate.csv` / `.walkforward.csv` /
`.gates.csv` / `.log.txt`
