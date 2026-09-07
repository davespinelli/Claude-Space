# Idea 386 — does the U56 band-m20 book beat its PARENT at matched cadence?  **NO. PARK, not KEEP.**

**Verdict: the owed test is discharged AGAINST the band.** The candidate loses to its own
plain (m=0) parent at matched turnover on all three pre-registered readings, on U56, at every
cost rung. Idea 280's finding survives; the memo
`2026-09-07_u56-top20-band-m20_4b_B_MEMO.md` stays a comparison and must not be promoted.

## What was run
Fine cadence ladder `{W, 2W, 3W, 4W, 5W, 6W, 8W, M, Q}` x `m in {0, 20}` (the two tuned
parameters) on three panels x three cost rungs = 54 books, every point printed and written to
`<slug>.grid.csv`. Book fixed as idea 384's: U56 top-20 by the v1 composite (vol scaler OFF),
v1 eligibility, NORM weights g/k_t at g = 0.75, next-day execution, 10 bps.
The new rungs (3W, 4W, 5W, 8W) exist only to bracket the candidate's 5.265x/yr turnover, which
idea 331's coarse ladder straddled 2.6x wide (2W 7.38x .. M 4.82x).

## Reproduction gates (all before any new number)
`fast_backtest == engine.backtest` at 0.000e+00 on returns and turnover; the derived rung
r(25) == `backtest(cost_bps=25)` at 0.000e+00; `sel_band(m=0)` nests `sel_hard(n=20)` with
**0 disagreements on all 9 cadences**; and idea 331's five published U56 rungs (W m=0, W m=20,
2W m=0, M m=0, 6W m=20) reproduce to a worst rounded discrepancy of **0.0005** — exact at the
3–4 s.f. the record published.

## The head-to-head (U56, 10 bps). Candidate: W m=20, T* = 5.265x/yr, Sharpe 1.112
| reading | comparand | parent Sharpe | band − parent |
|---|---|---|---|
| **B1** nearest m=0 twin | **4W**, 4.898x (\|dturn\| 0.367) | 1.142 | **−0.030** |
| **B2** bracket, linear in turnover | 4W 4.898x .. 3W 5.836x, w = 0.391 | **1.148** | **−0.036** (CAGR −1.63 pp, OOS −0.081) |
| **B3** best m=0 cell trading **no more** than the candidate | **M**, 4.816x | **1.213** | **−0.101** (CAGR −2.43 pp, OOS −0.120) |

Not a rung artefact: B1/B2/B3 are −0.024/−0.032/−0.094 at 0 bps, −0.030/−0.036/−0.101 at 10,
−0.040/−0.041/−0.112 at 25. **The margin against the band WIDENS with cost**, which is the
opposite of the band's own selling point (its 47-bps breakeven), because the M m=0 parent
already trades less than the banded weekly book does.

The pre-registered decision rule required the candidate to win B1 **and** B2 **and** B3 and
hold 4b at all three rungs. It holds 4b at 0/10/25 and loses all three comparisons. **PARK.**

## Rule 8 walk-forward ((cadence, m) on 2008–2016 IS Sharpe @10 bps, 2017–2026 read once)
| panel | menu | pick | OOS Sharpe | OOS CAGR | OOS MaxDD | regret |
|---|---|---|---|---|---|---|
| U56 | with band | 8W m=20 | **0.971** | 12.89% | −20.09% | −0.392 |
| U56 | band removed | **M m=0** | **1.307** | 17.57% | −19.51% | −0.056 |
| B136 | with band | 8W m=20 | 0.888 | 14.17% | −26.89% | −0.204 |
| B136 | band removed | M m=0 | 1.041 | 16.41% | −26.10% | −0.001 |
| SMALL439 | with band | 3W m=20 | 0.448 | 6.71% | −33.22% | −0.116 |
| SMALL439 | band removed | 5W m=0 | 0.376 | 5.31% | −34.93% | −0.188 |

SPY OOS 0.882; RULES v2 (live) OOS 1.285 / 1.119 / 0.568. **Putting the band on the chooser's
menu costs −0.336 OOS Sharpe on U56 and −0.153 on B136** (+0.073 on SMALL439) — a sharper
version of idea 331's −0.183, measured on the finer ladder. The honest chooser that is allowed
the band does not even pick the candidate: it picks 8W m=20, whose OOS 0.971 is below the
anchor's 1.131 and the candidate's own 1.187. **No chooser reaches the candidate cell**, which
is the second, independent reason it is PARK.

## KEEP-path census (54 books)
4b **10/54 @0 bps, 9/54 @10, 8/54 @25 — all but one on U56**; 4a **0/54 at every rung** (RULES
v2's −12.05% MaxDD dominates every cell). Breakeven c* on U56, m=0 / m=20: W 21/47, 2W —/—,
3W —/—, 4W —/67, 5W 34/77, 6W —/104, 8W —/37, M 68/95, Q —/—. B136 has exactly one cell with
any breakeven (W m=0 at 6 bps, below PROTOCOL's own cost assumption); SMALL439 has none.

## What survives
Nothing new is proposed. The strongest U56 object on this grid remains the **M m=0** parent
(15.30% / 1.213 / −19.51%, halves 1.200/1.232, OOS 1.307, c* 68, 4.82x/yr) — idea 329's
by-product, already PARKed for failing 4b on B136 (−26.10% MaxDD) and 4a on drawdown. This run
adds that it is also the band-free rule-8 chooser's own pick with regret −0.056, and that it
beats the banded candidate on every axis while trading less.

## Caveats
All three panels are current-constituent lists — **survivorship** — so CAGR levels are
optimistic (the CAGR floor is the bar this flatters most); the cadence- and m-differences this
run is about are much less affected. SMALL439 starts 2010-01-04 (44 tickers with
`max_1d_move >= 1.0` dropped), so its halves are not the same calendar halves. The kW rungs are
phase-anchored to each panel's first complete week; weekday-phase sensitivity is still owed.
