# Idea 376 — does a breadth-SPEED signal beat a breadth-LEVEL signal on the same 54 books?

**KILL (2026-09-07, lane C). The queue's TIMING premise is CONFIRMED and large — a speed
trigger reaches most of the loss a level trigger misses — but the DECISION does not move:
earlier arming buys drawdown at a WORSE exchange rate, loses the paired Sharpe head-to-head,
and clears 4b at 10 bps on fewer books than the level trigger it was meant to replace.
Lateness was not the binding constraint. No RULES change. One by-product 4b cell is PARKed
with a memo. RULES.md, scan.py, bot.py and baseline.py untouched.**

## Reproduction gates (all PASS, before any new number was read)
* derived rung identity `r(c) = r(0) - turnover*c/1e4` vs `engine.backtest(cost_bps=25)`: **0.000e+00**
* idea 40/41 U56 controls: NONE n=3 **21.9% / 1.04 / -25.8%** (H1 1.01 / H2 1.06), n=5 **16.5% / 0.95 / -21.6%**
* LIVE RULES v2 U56: **8.66% / 1.2056 / -12.05%** (halves 1.2259 / 1.1908)
* idea 350's committed `windows.csv`, all 54 books: peak/trough date mismatches **0**, max
  |neg_share difference| at B = 0.30/0.40/0.50 **8.3e-17**. The two runs are on the same books.

## Design
Idea 350's 54 books (EWALL / TOP3 / TOP10 / TOP20 / MAEW / RULES v2 x U56 / B136 / SMALL439 x
0/10/25 bps), rebuilt from source. Two trigger families armed by the **same** rule on their own
signal, so armed-day frequency is matched by construction rather than by a hand-picked
threshold: `armed_t = 1[S_{t-1} < Q_q(S_{..t-1})]`, Q_q a CAUSAL expanding quantile (min 252
obs), with `S = E_t` (LEVEL) or `S = E_t - mean_L(E)` (SPEED-L). Two tuned parameters: **L in
{10, 20, 40}** and **q in {0.10, 0.20, 0.30}**. Reported axes, every point printed: family,
depth {0.50, 1.00}, 6 forms, 3 panels, 3 rungs = **1296 overlay points**.

## [1] The premise is CONFIRMED — the speed trigger is EARLY, by a lot
Median `off_share` (share of the control book's binding-window down-day loss booked while the
gate is OFF; 1.0 = unreachable), at matched q:

| arm | q=0.10 | q=0.20 | q=0.30 |
|---|---|---|---|
| LEVEL | **0.784** | 0.490 | 0.326 |
| SPEED10 | **0.327** | 0.230 | 0.189 |
| SPEED20 | **0.286** | 0.283 | 0.189 |
| SPEED40 | **0.286** | 0.283 | 0.189 |

LEVEL at q=0.10 reproduces idea 350's fixed-B reading (0.784 vs 0.793 at B=0.30). At the same
armed-day budget the speed trigger is armed through **70.6%** of the binding window's days on
U56 and B136 versus LEVEL's 11.8% / 17.6%. Paired at (book, rung, q), SPEED's off_share is
below LEVEL's in **110-112 of 162** points, median difference **-0.116**. The two triggers are
genuinely different instruments: LEVEL-vs-SPEED20 armed-day Jaccard overlap is only
**0.18 / 0.26 / 0.33** at q = 0.10 / 0.20 / 0.30.

**Exception — SMALL439.** The speed trigger does NOT move the statistic there (0.767 -> 0.715
at q=0.10; window armed share 0.158 -> 0.147) and it arms FEWER days than LEVEL (0.079 vs
0.101). Whatever the small-cap binding episode is, it is not a breadth-deceleration event.

## [2] The decision does NOT move — being early is not worth anything here
Paired at matched (book, rung, q, depth), 324 points per lookback:

| arm | dDD better than LEVEL | median dDD diff | dSharpe better | median dSharpe diff | median dCAGR diff |
|---|---|---|---|---|---|
| SPEED10 | 178/324 | +0.296 pp | **87/324** | -0.0794 | -1.254 pp |
| SPEED20 | 161/324 | -0.008 pp | **82/324** | -0.0548 | -1.043 pp |
| SPEED40 | 156/324 | -0.147 pp | **109/324** | -0.0253 | -0.701 pp |

Drawdown is a coin flip; Sharpe and CAGR are worse. Exposure-normalised (idea 351's numeraire
form: pp of drawdown bought per pp of CAGR given up), the median exchange rate is **LEVEL 1.19,
SPEED10 0.92, SPEED20 0.86, SPEED40 0.79**, against a free-numeraire bar of **1.72** — the
speed family is not only worse than the level family, both are worse than simply holding less.
Beats-numeraire counts are flat across families (114 / 109 / 104 / 114 of 324).

## [3] KEEP paths, all 1296 points reported
**4a 39/1296** (LEVEL 14, SPEED 25 — every one at 0 bps, none survive a cost). **4b 128/1296**
(LEVEL 21/10/3 and SPEED 67/23/4 at 0/10/25 bps). At the protocol's 10 bps rung the per-cell
picture is the opposite of the queue's hypothesis: the best LEVEL cell (q=0.20, depth 0.50)
clears 4b on **4 of 18** books, the best SPEED cell (SPEED40, q=0.10, depth 0.50) on **3 of 18**.
4b failing bars across the grid: CAGR 998, H1 870, H2 795, OOS 778, DD 572.

## [4] Rule 8 walk-forward (menu chosen on IS <= 2016 Sharpe at 10 bps, 2017-2026 read once)
Three choosers on the same 18 books: OFF+LEVEL, OFF+SPEED, OFF+both.

| chooser | takes a gate | OOS Sharpe > own control | OOS MaxDD better | > SPY (0.882) | > RULES v2 OOS | median regret | median OOS CAGR |
|---|---|---|---|---|---|---|---|
| LEVEL | 12/18 | **3/18** (median -0.0065) | 11/18 (+0.945 pp) | 9/18 | 2/18 | 0.0262 | 8.59% |
| SPEED | 11/18 | **5/18** (median +0.0000) | 11/18 (+1.627 pp) | 9/18 | 3/18 | 0.0668 | 9.88% |
| ALL | 16/18 | **6/18** (median -0.0178) | 15/18 (+2.406 pp) | 8/18 | 2/18 | 0.0855 | 8.61% |

Head to head, the SPEED chooser beats the LEVEL chooser out of sample in **11 of 18** books
(median **+0.0169** Sharpe) with OOS MaxDD better in 9/18 — a real but small edge, and it is an
edge inside a family that still loses to doing nothing in 13 of 18 books.

## [5] Is the loss-share statistic still a pre-screen? (idea 350's -0.53 / -0.55 / -0.40)
Spearman(off_share, dDD_pp) stays negative in all 12 arm x q cells, but is weaker and noisier
for the speed family: LEVEL -0.545 / -0.249 / -0.330 at q = 0.10/0.20/0.30, SPEED10 -0.156 /
-0.365 / -0.125, SPEED20 -0.159 / -0.384 / -0.257, SPEED40 -0.331 / -0.375 / -0.500. The
statistic survives as a direction, not as a calibrated screen — consistent with idea 375's
brief, and with the fact that off_share explains which books a gate *can* touch, not what
touching them is worth.

## Verdict
**KILL.** Replacing the level trigger with breadth's own rate of change does exactly what the
queue predicted to the timing statistic (off_share 0.784 -> 0.286 at matched arming frequency)
and nothing at all to the outcome: the drawdown head-to-head is a coin flip, Sharpe and CAGR
are worse, the exchange rate is worse, and 4b at 10 bps is 3/18 against LEVEL's 4/18. The
breadth-gate family's problem is therefore **not** that a 200d-MA breadth signal is late — the
early version of the same instrument is no better. That closes the "de-lag it" branch the queue
has carried since idea 315, and leaves idea 350's own conclusion (negative median dSharpe, a
5-in-18 out-of-sample record against do-nothing) as the reason to retire the family.

One by-product cell is a genuine 4b pass and IS-selectable — **SPEED40, q=0.10, depth 0.50 on
equal-weight books** (U56 EWALL, U56 TOP20, B136 EWALL at 10 bps, rule-8 picked on all three) —
filed as **PARK** in the memo, not as a proposed rule, because it does not beat the LEVEL cell
it was built to replace.

## Caveats
All three panels are current-constituent lists (**SURVIVORSHIP**), so drawdown LEVELS are
optimistic and the 4b DD cap is a level test; the off_share decomposition is within-window and
unaffected. SMALL439 drops the 44 tickers with max_1d_move >= 1.0 and starts 2010-01-04, so its
halves are not the same calendar halves. The sample starts 2009-01-13 (260-day warm-up) so the
GFC is only partly inside it. **Realised armed-day frequency is matched only to ~2 pp**: the
causal expanding quantile gives LEVEL 0.080 / 0.176 / 0.289 and SPEED20 0.099 / 0.199 / 0.297
at q = 0.10 / 0.20 / 0.30 (and the reverse on SMALL439), so SPEED is arming slightly MORE on
the two large-cap panels — which flatters its drawdown column and is already charged against it
in the exposure-normalised exchange rate. A speed signal built on a 200d-MA breadth series is
still a slow statistic; this is the strongest de-lagged form the record's breadth definition
admits, not a lag-free one.
