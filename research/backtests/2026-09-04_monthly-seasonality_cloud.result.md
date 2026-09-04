# Idea 16 — `monthly-seasonality`: **KILL** (cloud lane, 2026-09-04)

Script `research/backtests/2026-09-04_monthly-seasonality_cloud.py` ·
console `…_cloud.console.txt` · grid `…_cloud.grid.csv` (150 rows).
10 bps, weekly, weights at close *t* applied *t+1*, 75 % gross (v1 keeps its 15 %/name).
Harness reproduces idea 2's standing KEEP row **12.7 % / 1.093 / −18.3 %, halves 1.088 / 1.103**
and the live v1 row **6.5 % / 0.666 / −13.8 %** to the decimal before any new number is read.

**Grid:** 2 universes × 3 books (`v1`, idea 2's `top20`, `EWall`) × 6 masks
(`sellinmay`, `sep`, `worst1/2/3/6` fitted on 2009-2016 only) × f ∈ {0.00, 0.25, 0.50, 0.75}
= **144 points, every one printed**, plus 6 f = 1.00 controls. Two tuned parameters (mask, f).

---

## 1. There is no month ordering to trade — the effect does not survive to the second half

Spearman correlation between each series' **H1** mean-daily-return-by-month ranking and its
**H2** ranking, the number the whole idea rests on:

| | SPY | v1 | top20 | EWall |
|---|---|---|---|---|
| universe.json | **+0.000** | **−0.182** | **−0.364** | **−0.021** |
| universe_broad.json | **+0.000** | **−0.049** | **−0.322** | **+0.028** |

Six of eight are negative; the largest is +0.028. Knowing which months were weak in 2009-2017
tells you nothing — slightly worse than nothing — about which will be weak in 2017-2026.
Corroborating the same point directly: September is the worst full-sample month in **all four**
series, yet it appears in only **1 of the 24** in-sample-fitted `worst-k` masks and in **0 of 6**
`worst1` picks (in-sample worst-1 is Jan or Aug everywhere). *September is a full-sample artefact.*

Individual month t-stats are consistent with no effect: SPY's worst full-sample month (Sep)
is **t −0.22**; the only |t| > 2 months are the *positive* ones (Jul +3.54, Nov +3.05).

## 2. The literal idea loses, and loses more the more it is applied

| | points | dSharpe > 0 | mean dSharpe | best dSharpe | worst |
|---|---|---|---|---|---|
| all | 144 | 24 (16.7 %) | **−0.080** | +0.063 | −0.582 |
| v1 | 48 | — | −0.042 | +0.063 | −0.234 |
| top20 (the KEEP) | 48 | — | **−0.113** | **+0.003** | −0.582 |
| EWall | 48 | — | −0.085 | +0.010 | −0.508 |

Monotone in f in every book: the more exposure the mask removes, the worse it gets
(`top20`/u56 `sellinmay`: f = 0.75/0.50/0.25/0.00 → dSharpe −0.032 / −0.095 / −0.214 / −0.391).
The mask is also a *trade*: `v1` turnover rises from 23.6× to 29-ish inside the mask arms it
does not cut, and the exposure it removes costs CAGR at roughly the gross-lever rate ideas 66/83
already measured — this idea buys nothing that de-grossing does not buy more cheaply.

## 3. Rule 8: the in-sample fit is anti-predictive, 6 of 6

(mask, f) chosen on 2009-2016 IS Sharpe, evaluated untouched on 2017-2026:

| universe | book | IS pick | IS Sharpe | OOS Sharpe | control OOS | Δ |
|---|---|---|---|---|---|---|
| u56 | v1 | worst6 f = 0.00 | 0.818 | 0.182 | 0.751 | **−0.570** |
| u56 | top20 | worst6 f = 0.50 | 1.050 | 0.842 | 1.170 | **−0.327** |
| u56 | EWall | worst6 f = 0.50 | 1.036 | 0.822 | 1.114 | **−0.292** |
| broad | v1 | worst6 f = 0.00 | 1.135 | 0.081 | 0.581 | **−0.500** |
| broad | top20 | worst6 f = 0.25 | 1.223 | 0.371 | 0.894 | **−0.523** |
| broad | EWall | worst6 f = 0.25 | 1.297 | 0.604 | 1.021 | **−0.417** |

**0 of 6.** In every case the selector picks `worst6` — the mask with the most fitting freedom —
which is the signature of pure in-sample fitting, and it destroys 0.29-0.57 of OOS Sharpe.

## 4. The two apparent cross-universe 4b passes are not a result

14 of 144 scaled arms pass 4b somewhere; exactly two pass on **both** universes —
`top20`/`sep` at f = 0.00 and f = 0.25. Both are *worse than their own control on Sharpe*
(broad 0.935 / 0.947 vs 0.958). They clear the bar only because zeroing September lifts broad
H2 from 0.814 to 0.846 past SPY's 0.837 — the exact 0.02 gap idea 44 flagged — and, per §1,
September is a mask nothing but full-sample hindsight would have chosen.
Rule 8 never selects it. This is what a lucky grid cell looks like; it is not a candidate.

## Verdict — **KILL**, as the QUEUE predicted, with a stronger reason than expected

Not "the weak-month rule underperforms" but "**calendar month is not a persistent property of
these series**": the H1→H2 rank correlation of month means is ≈0 or negative in 8 of 8 cells, so
no month mask is estimable, and the one that looks best full-sample is precisely the one the
in-sample fit refuses to pick. Rules unchanged. Standing candidates unaffected —
idea 2's `top20` is *hurt* most by this idea (mean dSharpe −0.113).

**Carry-forward:** this is the first run to state PROTOCOL's rule-8 failure mode as an explicit
diagnostic — *cross-half rank correlation of the conditioning variable* — computable before any
book is built and costing one line. Any future conditioning idea (regime, breadth quintile,
day-of-week, VIX bucket) should report it first; if it is ≈0, no grid can rescue the idea.

**Caveats.** Both lists are current constituents (SURVIVORSHIP — absolute CAGRs optimistic;
the month-vs-month comparison is far less exposed since every arm holds the same names on the
same days). 17.7 years is 17-18 observations per calendar month, so even a real month effect of
plausible size would be unmeasurable here — which is itself part of the KILL.
