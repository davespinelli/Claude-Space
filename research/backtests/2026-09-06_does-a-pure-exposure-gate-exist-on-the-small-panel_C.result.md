# Idea 300 — does-a-pure-exposure-gate-exist-on-the-small-panel (lane C, 2026-09-06)

**ANSWER: YES, and the MA gate's extra residual buys nothing.** A constant-depth QUANTILE gate
matched to the MA gate's own mean exposure carries **-0.0124 pp/yr** of timing residual (sd
0.0242, range -0.064..+0.017) against the MA gate's **-0.3817 pp/yr** (sd 0.3199, range
-1.160..+0.044) — and that extra 0.38 pp/yr of residual is worth **-0.0092 of Sharpe** full
sample (positive in only **9/27** cells) and **-0.0256 OOS** (8/27). `H_TIMING_PAYS` FAILS on
all three of its clauses; `H_PURE_DRAG` HOLDS. **4a 0/108, 4b 0/108** — no KEEP.

## Setup

SMALL439 (439 sub-$2B names, the 44 with `max_1d_move >= 1.0` dropped), 2011-01-13..2026-09-04
(15.61 yrs), 10 bps, 75% gross, next-day execution, no shorting/leverage. 0-bps rung derived
exactly as `r0 = r10 + turnover*bps/1e4`.

Both families order names by the same statistic `dist_t = px/ma200 - 1`. **MA-THRESH** holds
`{dist_t > theta}` — a prefix of that ranking whose LENGTH moves with the market (k sd 32–64
names). **QUANTILE-M** holds the top `ceil(x*n_t)` of the SAME ranking with `x` set to the MA
arm's own mean mask fraction — same prefix, CONSTANT length (k sd 7–63, and only 7–34 below
c_bar 0.5). Selection skill and mean exposure are therefore held fixed; the single remaining
difference is whether the depth is time-varying. Two dials: theta (9) × cadence (W/M/Q);
`x` is a deterministic function of theta, not a third dial. 9×3×2 families×2 constructions =
108 books, 54 decomposition cells, every one reported.

**B_MATCH (validity gate, read before the headline): PASS.** Identity
`max|r_dg,t - c_t·r_rs,t|` = **5.551e-17** over 54 cells; worst |Δ mask fraction| **0.00166**,
worst |Δ realised c_bar| **0.00643**; MA resid0 mean -0.3817 pp/yr lands inside idea 298's
pre-registered [-0.70, -0.20] band and QUANTILE resid0 -0.0124 inside ±0.05.

## Headline — MA-THRESH minus matched QUANTILE-M, DEGROSS, 27 cells

| statistic | mean | positive cells |
|---|---|---|
| dSharpe, full | **-0.0092** (median -0.0177, sd 0.0524) | **9/27** |
| dSharpe, H1 / H2 | -0.0187 / -0.0112 | 11/27 and 8/27 |
| dSharpe, OOS 2017-2026 | **-0.0256** | 8/27 |
| dCAGR | **-0.29 pp/yr** | 11/27 |
| dMaxDD | +1.22 pp (MA shallower) | 17/27 |
| turnover | 1.633/yr vs 1.652/yr (0.989×) | — |

The +1.22 pp of drawdown is the only thing the MA gate wins, and it is not robust: by cadence
it is **+4.47 pp (W), +1.89 (M), -2.69 (Q)**, and the quarterly arm loses Sharpe in **0/9**
cells (mean -0.056, OOS -0.084). The one place the MA form helps at all is the strict end,
c_bar ≤ 0.38 (dSharpe +0.02..+0.04) — i.e. exactly where the book is mostly cash and the
DEGROSS CAGR is 1.4–3.8%; from c_bar 0.5 up, where a real book would live, dSharpe is
-0.012..-0.047 and OOS -0.053..-0.076 at every rung.

## Exact attribution (an identity, closes to 1.78e-15 pp)

`dCAGR0_dg = SELECTION + LEVEL + TIMING`, means over 27 cells:

```
-0.2917 pp/yr  =  +1.2436 (selection)  -1.1660 (level)  -0.3693 (timing)
```

The MA gate's threshold form does buy something — but in the **RESPREAD** arm, where exposure
is pinned at 1: dSharpe **+0.0476** (17/27), dCAGR **+1.09 pp/yr**. Taking a deeper slice of the
ranking in strong markets and a shallower one in weak markets is a real cross-sectional effect.
It is destroyed by the de-grossing: the level term (-1.17 pp) is mechanically tied to the
selection term (scaling a higher-CAGR respread book by c_bar costs more in absolute pp), and
the timing term (-0.37 pp) then takes the rest. Net, de-grossing on the MA threshold gives back
everything the threshold earned.

## Rule 8 walk-forward (IS ≤ 2016-12-31 selects, 2017-2026 read once)

**WF-A** — (theta, cadence) by IS Sharpe inside each family × construction arm:

| arm | IS pick | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|
| MA-THRESH / DEGROSS | theta -0.40, Q | 7.98% | 0.5874 | -32.47% |
| MA-THRESH / RESPREAD | theta +0.30, M | 24.02% | 1.1042 | -30.78% |
| QUANTILE-M / DEGROSS | theta -0.12, Q | 7.03% | 0.6365 | -25.43% |
| QUANTILE-M / RESPREAD | theta -0.12, Q | 9.35% | 0.6307 | -34.83% |
| SPY | — | 15.45% | 0.8820 | -33.72% |
| RULES v2 (live) | — | 9.53% | 1.2851 | -12.05% |
| EWall no-gate control W/M/Q | — | 10.10/9.71/10.16% | 0.6372/0.6235/0.6467 | -36.16/-34.75/-33.94% |

Every DEGROSS pick loses to SPY on Sharpe and to the no-gate control on CAGR. The one arm that
beats SPY OOS (MA/RESPREAD, 1.1042) is a 10%-of-names concentrated momentum book at -30.8% DD;
it fails 4b on the drawdown cap and is not what this idea is about.

**WF-B (family choice)** — IS prefers MA-THRESH in 15/27 cells; OOS Sharpe of the pick **0.6221**
vs always-MA 0.6011 vs **always-QUANTILE-M 0.6268**. IS→OOS sign agreement of dSharpe **16/27
(0.593)**. Picking the gate form in sample does not beat simply always taking the pure-exposure
gate.

**WF-C (a KILL, and a qualifier on idea 298)** — idea 298 replaced its share-vs-c_bar curve with
a zero-parameter "subtract the gate's own constant residual". On SMALL439 that constant does
**not** walk forward for the MA gate: IS mean resid0 **-0.0201** pp/yr against OOS mean
**-0.5918**, and the IS-mean-constant predictor cuts OOS MAE only from 0.5975 (predict zero) to
0.5789 — a 3% improvement on an error five times the quantity being predicted. Predicting each
cell from its own IS value is worse still (0.5966). For the QUANTILE gate the zero-residual
property *does* walk forward: OOS mean -0.0002 pp/yr, MAE vs zero **0.0216**, and the IS-mean
constant makes it *worse* (0.0348). **The pure-exposure gate's zero is the discount that
survives; the MA gate's constant is a full-sample average, not a forecastable one.**

## KEEP paths

**4a 0/108** (nothing comes near RULES v2's -12.05% drawdown). **4b 0/108**; failure census:
all five clauses 65, H1/H2/OOS/CAGR 31, H1/H2/OOS/DD 6, H1/OOS/DD 3, H1/DD 2, DD alone 1.
The single book failing on DD alone is MA/RESPREAD theta +0.30 M (20.86% CAGR, Sharpe 1.0264,
halves 0.9383/1.1089, OOS 1.1042) at MaxDD -30.78% against a -20.2% cap — the same concentrated
momentum book WF-A picked, and it is idea 291's already-killed form, not a new candidate.

## Caveats

SURVIVORSHIP: `data/prices_small.csv.gz` is current constituents of the screen, no delistings,
so every CAGR **level** here is inflated and the 4a/4b columns inherit that bias whole. The
headline is an arm-minus-arm contrast on the same names, the same ranking and the same days, so
the bias very largely cancels out of dSharpe / dCAGR / resid0. One panel only, per the queue —
idea 298 measured the same residual gap on U56 and B136 but this pricing was not repeated there.

Script: `research/backtests/2026-09-06_does-a-pure-exposure-gate-exist-on-the-small-panel_C.py`
Outputs: `.grid.csv` `.decomp.csv` `.matched.csv` `.walkforward.csv` `.console.txt`
