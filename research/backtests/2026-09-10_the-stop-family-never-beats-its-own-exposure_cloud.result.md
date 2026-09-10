# Idea 396 — the stop family never beats its own exposure: LEVEL or INSTRUMENT?

**Run:** cloud, 2026-09-10 · `2026-09-10_the-stop-family-never-beats-its-own-exposure_cloud.py`
**Verdict: SPLIT — the queue's objection is LITERALLY RIGHT and SUBSTANTIVELY WRONG. Idea 135's
"0 of 59" is a level-set artefact (a wider ladder finds 61 of 594 wins, 10.3%), but every one of
those wins is either zero-cost-only or an arm where the stop barely fires. The instrument reading
stands: KILL upheld. 4a 0 of 594. No RULES/PROTOCOL/baseline edit.**

## Reproduction gates
| gate | result |
|---|---|
| G1 `run_stop(stop=None)` vs `engine.backtest`, all 9 panel × book | max\|dreturn\| **0.000e+00**, max\|dturnover\| **0.000e+00** — PASS everywhere |
| G2 idea 84 EWALL U56 g=0.85 @10bps | 11.8% / 1.05 / −17.9% / H 1.07/1.03 (committed 11.8/1.05/−17.9/1.07/1.04) |
| G3 derived cost rung `r(c) = r(0) − turnover·c/1e4` | max\|diff\| **0.000e+00** PASS |
| G4 de-gross interpolation on the 0.01 λ cache, 6 off-grid λ | max\|dSharpe\| **3.6e-08** |
| G5 BLOCK placebo matching identity (same mean invested fraction as its arm) | max\|diff\| **0.000e+00** |

## The grid
3 panels (U56 / B136 / SMALL 439 names) × 3 books (RULES v1 top-5, TOP20 = the 2026-09-04 KEEP
4b candidate, EWALL eligible-equal-weight at gross 0.75) × **11 stop levels 3%…50%** ×
2 cooldowns (0, 21d) × 3 cost rungs = **594 arms, every point reported**. The record has only
ever run the stop at 15% and 25%. Comparand inherited verbatim from ideas 66/94/135: the SAME
book de-grossed to the stop arm's own realised mean invested fraction.

## Q1 — is there ANY winning cell?
**61 of 594 (10.3%)**, so idea 135's 0-of-59 does not survive a wider ladder as a literal count.
By rung: 33/198 at 0 bps, **17/198 at 10 bps**, 11/198 at 25. But the wins sit at the two ENDS
of the ladder, and both ends are degenerate:

* **19 of the 61 (31.1%) are INERT** — λ ≥ 0.999, i.e. the stop de-grosses the book by less
  than 0.1% and fires 0–1 times a year. Their margin is +0.0003 to +0.0019 of Sharpe. That is
  numerically doing nothing, and it is where S = 0.40 gets its 12 "wins".
* Of the **42 non-inert wins, 26 are at 0 bps only**. The tight-stop wins that look real —
  U56 EWALL S=0.03 dSharpe +0.0762, B136 EWALL S=0.03 +0.0508 — do not survive the protocol
  rung.
* **16 non-inert wins survive at 10 or 25 bps**, and the largest is **+0.0255** of Sharpe
  (U56 / v1 / S=0.05 / 10 bps, λ 0.976). Every one of them has λ ≥ 0.90, i.e. the stop is
  de-grossing by at most 10%. **None of the 16 passes 4b, and none passes 4a.**

## Q2 — the shape of the curve
Median dSharpe vs stop level (10 bps, pooled over cooldown) is **monotone toward zero from
below** on all nine panel × book cells:

| S | 0.03 | 0.05 | 0.075 | 0.10 | 0.125 | **0.15** | 0.20 | **0.25** | 0.30 | 0.40 | 0.50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| median dSharpe | −0.285 | −0.194 | −0.099 | −0.042 | −0.032 | −0.013 | −0.011 | −0.010 | −0.002 | **0.000** | **0.000** |
| median λ | 0.798 | 0.902 | 0.962 | 0.980 | 0.989 | 0.994 | 0.998 | 1.000 | 1.000 | 1.000 | 1.000 |
| stops / yr | 233 | 151 | 87 | 52 | 31 | 17 | 6 | 2 | 1 | 0 | 0 |

**The curve's maximum is the point where the instrument switches off.** The argmax per
panel × book is S = 0.40 or 0.50 (dSharpe exactly 0.0000) in 4 of 9 cells, and in the other 5
it is a +0.002…+0.012 blip at S = 0.10–0.15. There is no interior optimum anywhere.

And the record's two levels were **not** the worst points: 15%/25% sit **above** the ladder
median in 6 of 9 panel × book cells. Idea 135 did not happen to pick the ladder's floor — it
picked two points that flatter the stop.

## Q3 — what the stop pays and what it buys (10 bps, median)
| S | dCAGR | dMaxDD | dCalmar | turnover/yr |
|---|---|---|---|---|
| 0.03 | **−2.25 pp** | +1.57 pp | −0.117 | 27.0× |
| 0.05 | −2.19 pp | +2.28 pp | −0.075 | 22.3× |
| 0.10 | −0.96 pp | +0.75 pp | −0.023 | 17.4× |
| 0.15 | −0.39 pp | +0.03 pp | −0.012 | 14.7× |
| 0.50 | 0.00 | 0.00 | 0.000 | 13.8× (= un-stopped) |

The stop does buy drawdown — up to +2.3 pp at S = 0.05 — but it pays 2.2 pp of CAGR and
doubles turnover to get it, and **Calmar is negative at every level**: de-grossing buys the
same drawdown more cheaply. That is idea 74's "dearest menu entry", re-derived across the whole
range rather than at two points.

## Q4 — the BLOCK placebo (carried over from idea 604, same day)
Each arm's own invested-fraction path, circularly shifted: the same cash, the same day-count,
the same run-length distribution, **no information about when to hold it**.

| rung | REAL win | BLOCK placebo win | diff |
|---|---|---|---|
| 0 bps | 0.167 | 0.342 | **−0.175** |
| **10 bps** | **0.086** | **0.134** | **−0.048** |
| 25 bps | 0.056 | 0.055 | +0.001 |

**The stop loses to a no-information cash path of its own shape.** REAL beats BLOCK in **1 of 9**
panel × book cells and is reversed in **8**. This is the sharpest form of the result: the stop's
timing is not merely worth less than de-grossing, it is worth less than shuffling its own exits.

## Q5 — KEEP paths and rule 8
**4a: 0 of 594 at every rung.** 4b: 65 / **22** / 8 at 0 / 10 / 25 bps — but **13 of the 22 at
10 bps are inert arms** (the stop never fires, so the book is its un-stopped self) and only
**1 of the 22 also beats its own matched-gross twin**. **0 arms pass both paths.**

Rule 8 (choose stop and cooldown on 2009–2016 IS Sharpe, read 2017+ once), 9 panel × book cells:

| | beats matched-gross control | beats un-stopped book | beats RULES v2 | beats SPY |
|---|---|---|---|---|
| OOS | **1 / 9** | **1 / 9** | **0 / 9** | 4 / 9 |

**IS dSharpe vs the control is positive in 7 of 9 cells and OOS positive in 1 of 9** — the
in-sample stop edge is the classic non-transferring one. Worst case, U56 / TOP20: the IS pick
(S=0.15, cooldown 21) reads OOS 12.43% / 1.116 / −14.55% against its matched-gross control's
13.86% / 1.168 / −17.72% and the un-stopped book's 14.36% / 1.168 / −18.31%.

## What the record should now say
1. **Idea 135's "stop 0.0%, 0 of 59" should be restated as a two-level reading.** The correct
   general statement is: *the stop's advantage over its own de-grossed control is negative at
   every level where the stop materially fires, and reaches zero only by switching off.*
2. **Idea 74's "the stop is the dearest menu entry" is upheld across the whole range**, not just
   at 15%/25%, and now has a Calmar-negative-everywhere form.
3. **Any future stop arm needs an inertness column** (λ, and stops/yr). 31% of this run's "wins"
   are arms that do nothing; without λ published beside dSharpe they would read as evidence.
4. **The BLOCK placebo belongs on the stop family too** (idea 604's finding, confirmed here at
   the sharper reading: reversed in 8 of 9 cells).

**Survivorship:** all three panels are current-constituent lists, so CAGR and drawdown *levels*
are optimistic; the stop-vs-control *contrast* is the durable part. The small panel drops the
44 tickers with `max_1d_move >= 1.0` in `data/small_meta.csv` before anything is computed and
starts 2010-01-04, so its halves are not U56/B136's calendar halves.
