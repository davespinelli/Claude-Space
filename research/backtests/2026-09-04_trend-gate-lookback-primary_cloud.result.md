# Idea 55 — trend-gate-lookback-primary (cloud lane, 2026-09-04)

**Verdict: KILL for the trend gate as a source of edge on the primary universe** — at 200d
its effect is statistically indistinguishable from zero on both large-cap lists, and at
100d/50d it is significantly harmful. **Plus one 4b KEEP-candidate**: the same book with
the 200d gate removed dominates idea 2's candidate on `universe.json` and is the rule-8
walk-forward pick under both pre-registered selection rules. Memo:
`2026-09-04_trend-gate-lookback-primary_cloud.memo.md`.

Script: `research/backtests/2026-09-04_trend-gate-lookback-primary_cloud.py`
Console: `2026-09-04_trend-gate-lookback-primary_cloud.console.txt`

## Question and design

The 200d-MA gate is the load-bearing assumption of RULES v1 and of idea 2's KEEP-candidate.
Idea 39 measured it at -1.7pp CAGR on small caps and idea 27 at -6.4pp on QQQ, but nobody
had varied the **lookback on `universe.json`**, where it is supposed to be the edge.

Idea 2's construction, unchanged: top-n by the v1 composite **without** `/sqrt(vol20)`,
equal weight 0.75/n (75% gross), weekly, t+1, 10 bps, cash when fewer than n are eligible.
Two tuned parameters — **K ∈ {200d, 100d, 50d, none}** and **n ∈ {5,10,20,30}** — all 16
points reported. The `vol20 < 0.60` half of the gate is held at v1's value throughout
(varying it is queued as idea 56). Secondary robustness pass on `universe_broad.json`.

**Harness check: K=200d, n=20 reproduces idea 2's KEEP row to the decimal** —
12.7%/1.093/-18.3%, halves 1.088/1.103.

## Primary universe (universe.json, 56 names, 2009-01-13 → 2026-09-03)

SPY 15.3%/0.890/-33.7%, halves 0.957/0.837, OOS Sharpe 0.884. RULES v1 6.5%/0.666/-13.8%.

| K | n=5 | n=10 | n=20 | n=30 |
|---|---|---|---|---|
| 200d | 16.5%/0.952/-21.6% | 12.9%/0.929/-17.5% | **12.7%/1.093/-18.3%** ✔4b | 11.0%/1.099/-16.6% ✔4b |
| 100d | 15.7%/0.925/-22.6% | 12.4%/0.927/-18.0% ✔4b | 11.4%/1.050/-15.1% ✔4b | 9.5%/1.015/-12.9% ✔4a |
| 50d | 11.0%/0.730/-25.5% | 8.2%/0.690/-18.9% | 8.3%/0.824/-16.1% | 7.1%/0.821/-14.4% |
| none | 17.0%/0.971/-21.4% | 13.7%/0.969/-17.5% | **13.7%/1.123/-18.5%** ✔4b | 12.5%/1.099/-17.1% ✔4b |

6 of 16 pass 4b; 1 of 16 (K=100d n=30) passes 4a.

**K=none beats K=200d at every n, on CAGR and Sharpe both.** The trend gate excludes on
average 14.4 of 51.9 vol-eligible names per day and puts the book under 20 names on 11.0%
of days, for nothing.

## The number the idea asked for

Paired daily t-tests, same names and same days, K=none minus K:

| | universe.json | universe_broad.json |
|---|---|---|
| drop 200d | +0.35 to +1.47%/yr, **t +1.42 to +1.76** (positive at all 4 n) | -0.22 to +0.19%/yr, t -0.50 to +0.68 |
| drop 100d | +1.17 to +2.95%/yr, t +1.43 to +2.55 | -0.07 to +0.93%/yr, t -0.12 to +1.51 |
| drop 50d | +5.14 to +5.49%/yr, **t +3.06 to +3.85** | +3.03 to +4.38%/yr, **t +2.59 to +3.31** |

**Read it honestly in three parts.**
1. **200d contributes nothing measurable.** The point estimate is negative at every n on
   the primary universe and zero on the broad one; nothing reaches significance. The claim
   "the gate is the edge" is not supported on the universe where it was supposed to hold.
   Equally, "the gate destroys value here" is *not* established — only that it doesn't earn
   the ~6.5x/yr of extra turnover it costs the un-ranked book (see below).
2. **Faster is decisively worse.** The 50d gate is the only significant effect in the
   lookback dimension, costing 3–5.5%/yr on **both** universes at every n, monotone in K.
   Whipsaw is real; it just doesn't stop at 200d, it stops mattering by then.
3. **The sign is unstable between the two large-cap lists** at 200d (-1.0%/yr on primary at
   n=20, +0.2%/yr on broad), which is itself evidence the gate is noise, not structure.

## Gate-only control — equal-weight every eligible name, no ranking (75% gross)

| K | universe.json | turn | universe_broad.json | turn |
|---|---|---|---|---|
| 200d | 10.4%/1.050/-15.9% | 8.2x | 10.7%/1.027/-17.7% | 8.3x |
| 100d | 9.9%/1.008/-20.0% | 12.1x | 10.2%/0.986/-18.2% | 12.3x |
| 50d | 7.4%/0.786/-22.3% | 18.1x | 8.4%/0.849/-22.9% | 18.1x |
| **none** | **12.2%/1.127/-18.4%** | **1.9x** | **12.9%/1.121/-20.8%** | **1.8x** |

This is the cleanest statement in the run, and it is **consistent in sign on both
universes**: for the un-ranked book the 200d gate costs ~1.8–2.2pp of CAGR and ~0.09 of
Sharpe (t +1.47 primary, **t +2.13 broad**) and adds **6.4x/yr of turnover**, to buy
2.5–3.1pp of drawdown. The turnover cost is certain; the drawdown benefit is the only thing
it reliably delivers. That trade may still be worth making for a live book — but it should
be recorded as drawdown insurance, not as alpha.

The K=none control passes 4b outright on `universe.json` (halves 1.141/1.116, OOS 1.183,
CAGR 12.2%, MaxDD -18.4%) and misses on `universe_broad.json` by 0.6pp of drawdown alone
(-20.8% vs the -20.2% cap) — more portable than any ranked book here. **It is also ~52 of
56 current constituents equal-weighted, i.e. close to an equal-weight index of a list
chosen in 2026.** Survivorship is the leading explanation for its 1.13 Sharpe against SPY's
0.89 and it is recorded as a diagnostic, not a candidate.

## Rule-8 walk-forward (IS ≤ 2016-12-31, OOS ≥ 2017-01-01)

- **universe.json — both selection rules pick K=none, n=20** (IS Sharpe 1.071, IS MaxDD
  -11.9%, the only point clearing the in-sample 4b bars with the best in-sample Sharpe).
  OOS **14.9%/1.164/-18.5%** vs SPY 15.5%/0.884/-33.7% and RULES v1 7.8%/0.751/-13.8%; it
  clears every OOS 4b bar. OOS Sharpe > IS Sharpe, so no overfitting signature.
- **universe_broad.json — both rules pick K=200d, n=30.** OOS 11.6%/0.904/-20.3%: beats
  SPY's OOS Sharpe but misses the OOS 4b bars, and **0 of 16 broad points pass 4b**.

The two universes pick opposite arms. That is the honest headline about the gate.

## Calendar-year check at n=20 (does the gate earn its keep in bear years?)

2018 K=200d +5.9% vs K=none +7.3% (SPY -4.6%); 2020 +15.4% vs +13.8% (SPY +18.3%);
2022 **-9.0% vs -8.9%** (SPY -18.2%). The gate helped only in 2020, by 1.6pp, and was a
dead heat in 2022 — the drawdown protection in the aggregate table comes from the vol20
filter and the cash sleeve, not from the trend gate.

## Caveats

- **Survivorship**, one-directional: both universes are current-constituent lists; a
  20-name book holds over a third of the 56-name list. Absolute figures are optimistic; the
  K-vs-K comparisons are much less exposed since every arm draws the same names.
- The `vol20 < 0.60` threshold is held fixed at v1's value and is **not** tested here; idea
  38 found it is the more damaging half of the gate on small caps. Queued as idea 56.
- Costs are 10 bps flat. The un-ranked K=none book at 1.9x turnover is the only arm here
  that would be materially cheaper in practice than modelled.

## Consequence for the Sunday review

1. Do **not** describe the 200d filter as the source of the live book's edge. On the
   universe it was fitted to, its measured contribution is zero within noise.
2. If idea 2's candidate is adopted, adopt it **without** the 200d gate (memo has exact
   wording): same construction, one fewer filter, +1.0pp CAGR, +0.030 Sharpe, -0.2pp
   drawdown, identical turnover, and it is the walk-forward pick under both rules.
3. Neither version survives the broad list, so any adoption still needs the explicit
   large-cap-universe clause ideas 39/49 called for.
4. Keep a 200d-class lookback if the gate is kept at all: 50d is significantly worse on
   both universes and 100d is worse on the primary one. Ideas 56 and 57 queued.
