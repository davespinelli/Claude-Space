# Idea 47 — fraction-rule-cost-and-lag (cloud, 2026-09-07)

**KILL — but the queue's prediction is falsified: F085 does not die sooner than n=20, it dies
LATER. What actually dies is the whole family, between 10 and 25 bps.**

The brief: idea 46's fraction book **F085** (top `ceil(0.85 * E_t)` eligible at 0.75/k) is a 4b
candidate whose CAGR margin is only ~0.6 pp, so it "should die sooner" than idea 2's KEEP **N20**
under costs and a slower fill. This run sweeps `cost ∈ {0,5,10,25,50} bps × lag ∈ {1d,2d,1w}` = 15
cells per book, on four fixed books (F085, N20, NF20, F100) across U56 / B136 / SMALL439 — **180
cells, all reported**. Costs come analytically from one zero-cost run per (book, lag, panel),
checked against `engine.backtest` at 10 bps to `max|diff| < 1e-12` on every panel.

## 1. The prediction is wrong on the mechanism

F085 holds ~1.6x (U56) to ~4x (B136) as many names as N20, but it **turns over less**, because a
fractional count moves smoothly with E_t while a hard `top 20` churns the boundary:

| panel | F085 names / turnover | N20 names / turnover | cost slope F085 | cost slope N20 |
|---|---|---|---|---|
| U56 | 32.2 / 9.60x | 19.1 / 9.63x | −1.05 pp CAGR per +10 bps | −1.07 |
| B136 | 78.1 / **9.52x** | 19.7 / **13.77x** | **−1.04** | **−1.53** |
| SMALL439 | 120.6 / 14.35x | 19.9 / 20.20x | −1.47 | −2.06 |

Pooled: F085 −1.19 pp per 10 bps vs N20 −1.57. F085 passes 4b in **15/45** cells against N20's
**11/45**. The fraction rule is the *cheaper* book, not the more fragile one.

## 2. What is fragile is F085's CAGR margin — and the 1-week fill

The two books fail on **different bars**, which is why "margin" and "slope" point opposite ways.
At 10 bps / 1d: F085's 4b CAGR margin is +0.66 pp (U56) and +0.51 pp (B136) with drawdown to spare
(+3.56 / +1.65 pp); N20's CAGR margin is +2.00 / +2.43 pp but its first failing bar is a half
Sharpe (H1 on U56, H2 on B136) and its DD margin on B136 is +0.18 pp. So costs take F085 out
through CAGR and N20 out through the halves, at almost the same rung.

The **execution lag** is where the queue's instinct was right, on B136 only: the 1-week fill costs
F085 −0.80 pp/yr of CAGR and −0.089 of Sharpe there and moves it from 3/3 passing cells to **0/3**
(fails DD, CAGR, H2). On U56 the same lag is free for both books (F085 1w @10 bps still 11.4% /
1.048 / −17.3%, 4b PASS). Pooled by lag, F085 passes 6 / 6 / 3 cells at 1d / 2d / 1w and N20
5 / 3 / 3 — the lag hurts the wide book on the wide panel and nobody else.

## 3. The finding that matters: 0 of 180 cells pass 4b at 25 or 50 bps

| bps | F085 | N20 | NF20 | F100 |
|---|---|---|---|---|
| 0 | 5/9 | 4/9 | 4/9 | 6/9 |
| 5 | 5/9 | 4/9 | 4/9 | 6/9 |
| 10 | 5/9 | 3/9 | 3/9 | 3/9 |
| **25** | **0/9** | **0/9** | **0/9** | **0/9** |
| **50** | **0/9** | **0/9** | **0/9** | **0/9** |

**Every 4b pass in this family sits at ≤10 bps**, i.e. exactly at PROTOCOL's anchor and below.
4a: **0/180**. SMALL439: **0/60** — nothing passes anything at any cost or lag (best cell 6.6% /
0.463 / −27.4% for N20 at 10 bps against SPY's 14.1% / 0.862). Whatever "capital-worthy" means in
this record, it is currently a claim about a 10 bps world, and it does not survive a doubling of
the cost assumption on any book, panel or fill. Queued as idea 323.

## 4. Rule 8: the in-sample chooser is not informative here

At every (panel, cost, lag) the book was chosen on ≤2016 alone under two pre-fixed rules (S1 = best
IS Sharpe; S2 = best IS Sharpe among books clearing the IS 4b bars) and 2017– read once. The
chooser picks the OOS-best of the four books in **27/90** cells — barely above the 22.5 a coin
would give — and **0/30 on SMALL439**. It is worst exactly where it is most confident: on B136 it
picks F085 in **0/30** cells while F085 in fact beats N20 on OOS Sharpe in **30/30** there; on
SMALL439 it picks F085 in 26/30 while F085 loses to N20 in 30/30. Mean OOS Sharpe regret 0.033
(U56) / 0.055 (B136) / 0.166 (SMALL439).

## 5. Head-to-head at the anchor and the stress points

| panel | book | lag | bps | CAGR / Sharpe / MaxDD | H1 / H2 | OOS Sharpe | 4b |
|---|---|---|---|---|---|---|---|
| U56 | F085 | 1d | 10 | 11.3% / 1.071 / −16.7% | 1.092 / 1.056 | 1.130 | **PASS** |
| U56 | N20 | 1d | 10 | 12.7% / 1.092 / −18.3% | 1.088 / 1.102 | 1.168 | **PASS** |
| U56 | F085 | 1d | 25 | 9.7% / 0.934 / −16.8% | 0.953 / 0.920 | 0.995 | fail H1,CAGR |
| U56 | N20 | 1d | 25 | 11.0% / 0.967 / −18.4% | 0.954 / 0.984 | 1.050 | fail H1 |
| U56 | F085 | 1w | 10 | 11.4% / 1.048 / −17.3% | 1.075 / 1.029 | 1.097 | **PASS** |
| B136 | F085 | 1d | 10 | 11.2% / 1.023 / −18.6% | 1.128 / 0.927 | 1.024 | **PASS** |
| B136 | N20 | 1d | 10 | 13.1% / 0.957 / −20.1% | 1.125 / 0.811 | 0.892 | fail H2 |
| B136 | F085 | 1w | 10 | 10.4% / 0.934 / −20.7% | 1.096 / 0.792 | 0.899 | fail H2,DD,CAGR |
| SMALL439 | F085 | 1d | 10 | 4.3% / 0.373 / −40.9% | 0.466 / 0.305 | 0.321 | fail ×5 |
| SMALL439 | N20 | 1d | 10 | 6.6% / 0.463 / −27.4% | 0.603 / 0.348 | 0.487 | fail ×5 |

References: SPY 15.2% / 0.889 / −33.7% (OOS 0.882); RULES v2 (live) 8.7% / 1.206 / −12.1% on U56,
8.0% / 1.106 / −12.2% on B136, 3.8% / 0.572 / −14.7% on SMALL439.

**Survivorship:** three current-constituent panels (SMALL439 drops the 1 name with `max_1d_move ≥
1.0`); absolute CAGRs are optimistic everywhere. The cost and lag comparisons hold names, days,
filter, gross and cadence fixed and are far less exposed than the levels — they are the durable
part of this run.

**Rules unchanged. No KEEP.** F085 stays a 10-bps-only candidate and is not proposed; nothing in
this family is capital-worthy at 25 bps.
Script: `2026-09-07_fraction-rule-cost-and-lag_cloud.py`
