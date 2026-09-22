# idea 2326 (lane cloud, 2026-09-22) — does a MINIMUM BREADTH FLOOR on N_in beat the PER-NAME CAP?

**ANSWERED = NO. KILL of the idea's own premise ("a floor keeps the candidate's full re-gross on
the 99% of days where breadth is healthy and spends nothing there, so if it holds the 4b pass it
is the cheaper of the two fixes"). The floor DOES hold the 4b pass — and it is NOT cheaper. It
raises turnover where the cap lowers it, it buys less Sharpe per point of CAGR spent, and under
rule 8 its picks beat idea 2322's committed cap book on OOS CAGR *and* OOS Sharpe at 0 of 24.
NO NEW KEEP-CANDIDATE; the cap stands as the better fix.**

## The two devices, on the same candidate
`FLOOR(m, g)`: `if N_in < m: w_i = g / N_t` (fall back to the de-grossed live book) `else:
w_i = g / N_in` (idea 2300's full re-gross); idle NAV -> SHY at phi = 1.00 either way.
Two tuned dials and no more: **m {1, 3, 5, 8, 12, 20, INF} and gross {0.75, 1.00}**. m = 1 IS the
candidate (gate G2, 4.4e-16), m = INF is the de-grossed live book + sweep (gate G3, 7.8e-16).
Reference books computed and reported but **never selected on and never counted as a dial**:
`CAP2` = idea 2322's committed `min(g / N_in, 2.0%)` device, and `FLOORCAP` = the floor with that
same inherited cap attached. Panels (U56 / B136 / SMALL), rungs {0, 10, 25, 50} bps, weekly
cadence, t+1, band 0.03 and the sweep instrument are reported, never selected on.
**90 books x 4 rungs = 360 published rows.**

## The head-to-head (U56, gross 0.75, 10 bps — the live gross)
| book | CAGR | Sharpe | MaxDD | OOS CAGR / Sharpe | 4b | max name w | binds | turn/yr |
|---|---|---|---|---|---|---|---|---|
| candidate m=1 | 12.59% | 1.1934 | -17.39% | 13.85% / 1.2397 | Y | **15.00%** | 0.00% | 4.39 |
| floor m=8 | 12.30% | 1.1762 | -17.39% | 13.26% / 1.2040 | Y | 9.38% | 1.01% | 4.58 |
| floor m=12 | 12.35% | 1.2132 | -17.39% | 13.26% / 1.2507 | Y | 6.25% | 3.73% | 4.50 |
| floor m=20 | 11.91% | 1.2389 | -15.36% | 12.93% / 1.2967 | Y | 3.75% | 10.09% | 4.49 |
| **cap 2.0% (idea 2322)** | 11.62% | **1.2687** | **-14.81%** | 12.77% / **1.3318** | Y | **2.00%** | always | **3.51** |
| de-grossed m=INF | 9.15% | 1.2719 | -11.48% | 10.21% / 1.3636 | . (L_CAGR) | 1.50% | 100% | 2.79 |

Deltas against the candidate: the cap spends **0.97 pp of CAGR** and returns **+0.0753 Sharpe,
+2.58 pp of MaxDD, +0.0921 OOS Sharpe** and a max per-name weight of 2.00%. The best floor rung
(m=20) spends **0.69 pp** and returns **+0.0456 Sharpe, +2.03 pp, +0.0570 OOS Sharpe** at 3.75%.
Per point of CAGR given up that is **0.078 Sharpe for the cap against 0.066 for the floor**, and
the cap ends with half the concentration.

## Why the "spends nothing in normal breadth" argument fails
It is true and it is the problem. On U56 the floor **never binds at all** at m <= 5 (min N_in over
the scored window is 5), and binds on 1.01% / 3.73% / 10.09% of days at m = 8 / 12 / 20. On B136
m=20 binds 1.93% of days, on SMALL 0.13%. So the dial is inert exactly where the candidate's
concentration lives — the 15% single-name weight survives every rung up to m=5 unchanged — and it
only starts to bite by turning itself into the de-gross switch. Worse, **switching weighting
scheme on a minority of days ADDS trading**: turnover goes 4.39 -> 4.49-4.58 turns/yr under the
floor, while the cap takes it DOWN to 3.51. The floor is the more expensive fix on its own stated
mechanism.

## The floor is redundant once the cap is on
`FLOORCAP` at m = 1 / 3 / 5 is bit-equal to `CAP2`; at m = 8 / 12 / 20 the whole family moves by
**<= 0.13 pp of OOS CAGR and <= 0.003 of Sharpe** (12.77% / 1.3318 -> 12.64% / 1.3315). Adding a
breadth floor to a capped book changes nothing worth a parameter.

## Rule 8 (m, gross fitted on <= 2016-12-31, 2017-2026 read ONCE)
24 picks = 3 panels x 4 rungs x {C_ISSHARPE, C_ISCALMAR}. **0 of 24 land on m = 1.** The picks
beat CAP2's OOS Sharpe at 9 of 24 and its OOS CAGR at 6 of 24 — and **beat it on BOTH at 0 of
24**. 9 of 24 sit on a ladder ENDPOINT (m = INF, i.e. the chooser walks back to the de-grossed
book), including every SMALL pick at every rung. 12 of 24 picks also pass 4b on the full sample.

## Both KEEP paths, all 360 rows
4b **116**, 4a **12** of 360 (every 4a pass is the m=INF de-grossed book, and 4a is **0 of 180**
at 25 and 50 bps). By family: FLOOR 41/168, FLOORCAP 65/168, CAP2 10/24. By panel: U56 73/120,
B136 43/120, **SMALL 0 of 120** — the sub-$2B panel clears nothing on either path at any rung,
the same result 2322 published for the cap. The dominant binding leg on 4b failures is `L_DD`
(45 of the failures at every rung), then `L_CAGR` (21 -> 64 as costs rise).

## Gates — 14 of 14 pass
G0 >= 10y per panel (17.7 / 17.7 / 15.7y). G1 the per-column replica equals `engine.backtest`
(0.00e+00). G2 m=1 == idea 2300's RG100 + phi=1 (4.4e-16). G3 m=INF == the de-grossed live book +
sweep (7.8e-16). G4 no leverage (max row sum 1.000000000). G5 the binding-day share is
non-decreasing along the ladder at 6 of 6 (panel, gross) cells. G6 SHY priced on every held row.
G7 SMALL dropped 54 tickers at `max_1d_move >= 1.0` (665 investable). G8 exactly two tuned
parameters. **G9 reproduces idea 2300's committed U56 headline** (12.55%/1.1896/-17.39%, OOS
13.77%/1.2332) to 8.25e-04. **G10 reproduces idea 2322's committed U56 cap-2.0% headline**
(11.58%/1.2643/-14.81%, 1.3042/1.2363, OOS 12.70%/1.3243) to 9.44e-04.

## Caveats, stated not buried
- **Survivorship.** U56 and B136 are current-constituent lists; SMALL is a current screen of
  sub-$2B names (665 after the drop rule). Every absolute CAGR here, and therefore every 4b
  verdict, is survivorship-optimistic. The floor-vs-cap comparison is same-names, same-days.
- The two G9/G10 residuals (8e-04, 9e-04) are the price-cache vintage, not a construction
  difference: the committed cells were priced on an earlier `data/prices.csv` blob.
- SHY exists on the panel from the start, so the sweep carries no instrument-availability bias
  here; the sleeve's own rate-regime exposure was priced separately by idea 2290.

Script: `research/backtests/2026-09-22_minimum-breadth-floor-vs-per-name-cap_cloud.py`
Outputs: `.grid.csv` (360 rows) `.shape.csv` (90 books) `.walkforward.csv` `.gates.csv` `.log.txt`
