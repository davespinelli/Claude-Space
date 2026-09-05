# Idea 196 — does-the-leak-free-selector-edge-survive-a-third-corpus (cloud, 2026-09-05)

**VERDICT: KILL of the replication. Idea 193's S2LF edge is a two-panel accident. The
do-nothing streak is restored to nine, and idea 193's own "the streak ENDS" claim should be
read as ended only for the LEAKY keys.** Rules unchanged; no new KEEP; no memo.

## What was asked
Idea 193's rule-8 walk-forward found S2LF — the in-sample argmax over the three **leak-free**
keys MOM / R3 / REBASED — beating the do-nothing control by **+0.1370 mean OOS Sharpe
(t +2.19, 11W/1L)** on 6 cost-collapsed cells drawn from **two** panels (broad136, small483).
Six paired observations cannot separate a selector edge from a panel accident. Re-run the
identical keys, tilt construction (`comp + dir·m·rankpct(key)`), base book (idea 2's top-20
EW composite, gross 0.75, weekly, t+1) and selector protocol on a **third corpus**:
idea 175's **115 books** (SMALL439, U56, ETF36 + 112 seeded sub-draws; no broad136 anywhere).

## Reproduction, asserted before any new number was read
| check | value | target | err |
|---|---|---|---|
| RULES v1 on u56 @10bps | 6.45305% / 0.66418 / −13.82780% | published, to every digit | 4.0e-07 |
| `fast_backtest` == `engine.backtest` | — | 0 | **1.39e-17** |
| cost identity `r_c = r_0 − turnover·c/1e4` | — | 0 | **1.39e-17** |
| idea 175's U56 @ W ladder point | 12.8581% / **1.1075** / −18.2071% | 12.86 / 1.1075 / −18.21 | 2.4e-05 |
| corpus size | 115 books (SMALL 49 / U56 33 / ETF 33) | 115 | **0** |

Grid: 115 books × (1 control + 3 keys × 2 dirs × 3 m) × 2 cost rungs = **4370 rows, 4140 real
arms**, 2185 backtests. Exactly **two tuned parameters** (m ∈ {0.20, 0.50, 1.00}, dir ∈
{POS, NEG}), every grid point reported. The 25 bps rung is derived exactly from the single
0 bps run via the engine's own turnover series, not re-fitted.

## (1) The headline: it does not replicate — it inverts
Rule 8, key/dir chosen on ≤ 2016-12-31 only, 2017-2026 read once, **690 cells**:

| selector | mean OOS Sharpe | dOOS vs S0 | t | W/L (690) |
|---|---|---|---|---|
| ORACLE-OOS (ceiling, not implementable) | +0.6522 | **+0.0210** | +12.40 | 367/35 |
| C-MOM/POS (best constant) | +0.6361 | +0.0049 | +3.64 | 227/173 |
| **S0 do-nothing** | **+0.6312** | 0 | — | — |
| **S2LF IS-argmax (leak-free)** | +0.6280 | **−0.0032** | −1.79 | 172/228 |
| RANDOM (same pool) | +0.6171 | −0.0142 | −6.17 | 155/247 |
| C-MOM/NEG (worst constant) | +0.5961 | −0.0351 | −12.83 | 71/331 |

On idea 193's own cost-collapsed convention (345 cells): **−0.0032, t −1.28, 84W/116L**,
against its published **+0.1370, t +2.19, 11W/1L**. The point estimate moves by 0.140 of
OOS Sharpe and changes sign, on 58× the paired observations.

## (2) Why — and the one genuinely new thing this run establishes
The selector is **not** unskilled. S2LF agrees with the OOS oracle in **52.9%** of cells
against 16.7% by chance, and it **beats RANDOM drawn from its own pool by +0.0110
(t +3.78, 193W/147L)**. What kills it is the pool: the mean dSharpe of all 4140 real arms is
**negative**, monotonically in tilt strength (m=0.2 −0.001 → m=1.0 −0.015 @10bps, −0.023
@25bps) and worse at the higher cost rung. **Real picking skill inside a negative-expectancy
pool still loses to not trading the instrument at all.** That distinction — which idea 193's
6 cells could not draw — is the finding, and it reconciles this run with idea 189's premise:
the best *constant* (C-MOM/POS, +0.0049, t +3.64) is the only arm in the run that beats S0.

## (3) No family carries it — the two-panel accident is localised
| family | books | S0 | S2LF dOOS | t | W/L |
|---|---|---|---|---|---|
| SMALL | 49 | +0.1501 | **−0.0004** | −0.11 | 91/105 |
| U56 | 33 | +1.1783 | −0.0053 | −2.35 | 49/53 |
| ETF | 33 | +0.7986 | −0.0051 | −4.31 | 32/70 |

Idea 193's edge came from broad136 + small483. The SMALL family here — sub-draws of the same
483-name panel — reads **−0.0004**, i.e. exactly zero. Nothing survives the corpus change.

## (4) Both KEEP paths, all 4140 real arms
**4a 1665/4140, 4b 208/4140** (controls 94/230 and 14/230). 4b passes are **U56 208, SMALL 0,
ETF 0** — the twelfth reproduction of idea 136 (the small panel has no 4b-passing book) and the
first time ETF36's family is shown to have none either. Among 3932 failing rows the bar
violation counts are **CAGR 3893 / OOS-Sharpe 2632 / DD 1211**: the CAGR floor is what kills
almost everything, as ideas 152/161 predicted.

**By-product, PARKed, NOT proposed.** `U56 + REBASED/POS` clears 4b at **all three m and both
cost rungs** (m=1.0 @10bps: **13.30% / 1.1327 / −18.44%**, halves 1.189/1.107, **OOS 1.2007 /
15.60% CAGR**, 7.9×/yr turnover — vs the untilted control's 12.86% / 1.1075 / −18.21%,
OOS 1.1775). It is the only arm in the run that improves the standing 4b candidate on Sharpe,
CAGR, drawdown *and* turnover simultaneously. It is not proposed because (a) per idea 144 it is
idea 2's existing book with an instrument on it, not a new book; (b) it **fails the universe
change outright** — the same arm reads 0.2408 Sharpe on SMALL439 and 0.8657 on ETF36, against
SPY's 0.8615/0.8890, i.e. 0 of 1188 ETF rows and 0 of 1764 SMALL rows pass 4b; (c) 4a fails in
all six cells; (d) it is 1 of 4140 unpriced grid points, and idea 181 already showed a
zero-information key clears 4b *more* often than a real one.

## Predictions: 3 of 5 hit
- **P1 MISS** — S2LF is not positive-but-smaller; it is **negative** (−0.0032).
- **P2 MISS** — S2LF *does* significantly beat RANDOM (+0.0110, t +3.78). Reported as the
  run's real content, see (2).
- P3 HIT — best constant (+0.0049) beats S2LF (−0.0032).
- P4 HIT — SMALL (−0.0004) > U56 (−0.0053), though "carries the edge" is vacuous at zero.
- P5 HIT — 4b is U56 208 / SMALL 0 / ETF 0.

## Caveats carried, not buried
- **SURVIVORSHIP (idea 54):** SMALL439 is current constituents of a sub-$2B screen with no
  delistings; U56 and ETF36 are current lists. Control and arms inherit the bias identically,
  so the **paired** selector reading is unaffected; every **level** (CAGR, Sharpe, 4b counts)
  on the small family is biased upward and is not a tradable estimate.
- Books inside a family are overlapping draws from one pool, so the pooled t **overstates**
  significance. Per-family numbers are given for that reason; the conclusion (no positive
  effect anywhere) does not depend on the pooled t.
- Idea 38: calendar-day index on U56/ETF36 after 2014-09-17, so a weekly bar there is a
  calendar week. Idea 126: t+1 execution only.
- REBASED's "entry" is the first bar of the panel sample, not a listing date — same
  construction as idea 193, re-priced rather than improved.

## What this changes
Nothing in RULES, `scan.py`, `bot.py` or `baseline.py` (all untouched). The record should now
read: **an IS-fitted selector has lost to doing nothing in nine of nine project runs**
(110/132/151/166/171/174/175/186/196), and idea 193's apparent exception was carried entirely
by keys that read the level of an auto-adjusted price series. Ideas 198–200 queued.
