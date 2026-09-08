# Idea 233 — does-turnover-level-predict-chooser-power (cloud lane, 2026-09-08)

**Verdict: KILL.** The cost ladder's chooser value is **not** publishable from one number.
Across the full 5 transforms x 4 rungs x 2 targets x 2 corpora grid (80 fits), turnover's best
single R^2 is **0.127** and its mean is **0.05**; at PROTOCOL's own 10 bps rung the fitted line
beats the trivial "quote the pooled mean" predictor in **0 of 10** grid points; leave-one-panel-
out is a coin flip (49 of 80). What survives is a *direction*, not a quantity: the slope is
positive in **4 of 4 folds at every transform for rungs >= 20 bps**. No RULES change, no new
book, no KEEP candidate. RULES.md, scan.py, bot.py and baseline.py untouched.

## Corpus and gate

Both parents rebuilt end to end from prices rather than cited: **idea 230's 33 cells** (TOPN /
V1C / EWALL x their dials on U56, B136, SMALL439) + **idea 228's 12 cells** (TOPN only, on U56,
B136 and the **unscreened SMALL484** that 228 actually used) = the **45 pooled rows** the queue
asks for. **8 of those rows are literal duplicates** (U56 and B136 TOPN, 4 dials each, appear in
both parents), so every headline is also quoted on the **37 distinct cells**. 2,016 grid points.

**Gate:** `net(c) = gross - turnover*c/1e4` against `engine.backtest` at 10 bps, max abs daily
difference **6.9e-18 / 2.4e-17 / 1.9e-17 / 2.4e-17** on U56 / B136 / SMALL439 / SMALL484.

Two targets, because "chooser power" has an in-sample and an out-of-sample reading and the
queue's y is the in-sample one: **y_IS** = `cost_of_0bps_pick_at_R` (Sharpe given up at rung R
by taking the 0-bps argmax) and **y_OOS** = rule-8 chooser power (OOS Sharpe of the IS-chosen
arm minus the do-nothing arm).

## (1) Turnover explains almost none of it

| corpus / target | mean R^2 | max R^2 | mean Spearman | max Spearman |
|---|---|---|---|---|
| dedup37 y_IS | 0.0649 | **0.1210** | 0.2755 | 0.3537 |
| dedup37 y_OOS | 0.0317 | 0.1121 | 0.1289 | 0.5050 |
| pooled45 y_IS | 0.0500 | 0.1032 | 0.2602 | 0.3568 |
| pooled45 y_OOS | 0.0375 | **0.1272** | 0.1530 | 0.5410 |

The single best cell of the entire 80-fit grid is `dedup37 / span / 30 bps` at R^2 **0.1210**
for y_IS and `pooled45 / span / 30 bps` at **0.1272** for y_OOS. The `span` transform (the
cell's turnover range across the dial) beats the do-nothing turnover LEVEL the queue named, at
every rung, on both corpora — but only from 0.108 to 0.121.

## (2) The replacement test — the line does not beat the mean

The claim is a *replacement* claim ("publishable from one number instead of a census"), so the
test is leave-one-out RMSE of the fitted line against leave-one-out RMSE of the pooled mean.

| | beats the mean |
|---|---|
| dedup37 y_IS | 12 of 20 |
| pooled45 y_IS | 9 of 20 |
| dedup37 y_OOS | 6 of 20 |
| pooled45 y_OOS | 6 of 20 |

Mean RMSE ratio by transform (y_IS): span **0.989**, log 1.000, level 1.002, rank 1.003,
span/level 1.011 — i.e. the best transform in the grid buys **1.1% of RMSE**. By rung it is
worse where it matters: at **10 bps, PROTOCOL's binding rung, the line beats the mean in 0 of
10 grid points** (mean ratio 1.016). The relation only appears at 25 and 30 bps (8 of 10 each),
which are rungs PROTOCOL does not cost at.

## (3) Leave-one-panel-out is a coin flip

The 37 cells are 4 panels, not 37 independent draws, so the only honest generalisation is
leave-one-panel-out: **49 of 80 folds** (dedup37, y_IS) and 46 of 80 (pooled45). On the
`level` transform the U56 fold **never** beats the mean, at any rung (RMSE 0.0141 vs 0.0137 at
10 bps, 0.0537 vs 0.0518 at 30), and the SMALL439 fold beats it at 0 of 4 rungs on dedup37.
B136 and SMALL484 beat it at 3 and 4 of 4 — the sign of the answer depends on which panel is
held out.

**What does survive:** the slope is stable. Across all 4 folds and all 5 transforms, it is
positive in **4 of 4 folds at every rung >= 20 bps** (level 30 bps: mean +0.0034, min +0.0022,
max +0.0044), and only at 10 bps does it wobble (0.75-0.88 positive). Higher turnover *does*
mean a more re-rankable cost ladder — as a direction, not a number.

## (4) Why: y is a spike at zero

`y_IS = 0` exactly iff the ladder never re-ranks, so `y = P(re-rank) x E[cost | re-rank]` and
any "clean function of turnover" must first be a clean function of P(re-rank). It is not:

* **25 of 37 distinct cells (67.6%) have y_IS(30) exactly 0**; at 10 bps, **28 of 37 (75.7%)**.
* Mean y_IS(30) is 0.0347 overall but **0.1070 among the 12 nonzero cells** (max 0.2913).
* Do-nothing turnover of re-ranking vs non-re-ranking cells: **22.5 vs 18.9 turns/yr**, over
  *identical* ranges (10.9 to 32.4 both). Turnover span: 16.7 vs 10.3, ranges 0.6-32.8 vs
  0.1-30.6. Turnover does not separate the two populations.

## (5) The in-sample target does not predict the out-of-sample one

Regressing y_OOS on y_IS over the 37 distinct cells: R^2 **0.005 / 0.000 / 0.020 / 0.056** and
Spearman **-0.119 / +0.085 / +0.151 / +0.216** at 10 / 20 / 25 / 30 bps. At PROTOCOL's binding
rung the sign is *negative*. Even if turnover predicted `cost_of_0bps_pick_at_30` cleanly, it
would not be predicting anything the walk-forward cares about.

## (6) Rule 8 walk-forward and both KEEP paths

Rule 8 at 10 bps (params 2009-2016, 2017-2026 read once), 37 cells: mean d(pick - do-nothing)
**+0.0011**, pick wins **51.4%** — a coin flip, the record's standing result reproduced again.

| OOS at 10 bps, mean over cells | Sharpe | CAGR | MaxDD |
|---|---|---|---|
| rule-8 pick | 0.7599 | 12.95% | -32.55% |
| do-nothing | 0.7587 | 11.73% | -29.72% |
| RULES v2 (live) | **0.9551** | 6.84% | **-12.90%** |
| RULES v1 (continuity) | 0.5997 | — | — |
| SPY | 0.8820 | 15.45% | -33.72% |

By panel, pick OOS Sharpe **U56 1.0788 / B136 0.8416 / SMALL484 0.5641 / SMALL439 0.4304** vs
SPY 0.8820 and RULES v2 1.2851 / 1.1185 / 0.6629 / 0.5680.

**KEEP paths on all 2,016 grid points: 4a 0/2,016** against the live RULES v2 (251/2,016 against
the retired v1) — every failure is drawdown; **4b 49/2,016**, of which **8 at PROTOCOL's 10
bps**, all U56 and all already-published shapes: EWALL band 0.01/0.02/**0.03** (best: 15.05%,
**1.1348**, -19.95%, H1 1.1131 / H2 1.1576, **OOS 1.2314**, 6.41 turns/yr), EWALL V=0.40,
EWALL K=2, TOPN N=40 (12.95%, 1.1236, OOS 1.2656), TOPN V=0.30, V1C N=40. Nothing new; no memo.

## What to do with the queue's proposal

Do not replace the cost-ladder census with a turnover number. The defensible one-line
statement, offered to Sunday review as reporting language only, is directional:
*"a cell's cost ladder re-ranks more often when its dial spans more turnover; the effect is
positive in 4 of 4 panel folds at 20-30 bps and indistinguishable from the pooled mean at
PROTOCOL's 10 bps."*

## Caveats

SURVIVORSHIP: B136, SMALL439 and SMALL484 are current constituents of their screens only
(data/SMALL_PANEL_README.md, idea 54) — the bias runs in favour of every long book quoted here.
SMALL439 drops the 44 tickers with `max_1d_move >= 1.0`; SMALL484 is deliberately unscreened
because that is the panel idea 228 used, and it is the one place the two parents genuinely
differ. 37 cells over 4 panels and 3 books is a small, dependent sample: the three books share
one eligible set, so the LOPO folds are the binding evidence and they are the weakest.
