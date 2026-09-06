# Idea 245 — arm-the-cheap-instruments-in-crashes-instead (cloud, 2026-09-06)

**Verdict: KILL of the queue's premise, generalised. NO slow instrument is cheaper in crashes.
The one family that is (constant de-gross) is not an arming candidate at all — it is unconditional
by definition. No new KEEP; RULES.md, scan.py, bot.py and baseline.py untouched.**

Script `research/backtests/2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud.py`.
2 panels (u56 56 names, broad 136) x 2 instrument-free base books (EWALL0 equal-weight-all,
CAND20 top-20-by-composite-no-gates, both gross 0.75) x 6 instrument families x 4 strength levels
x 2 cost rungs = **200 backtests, all reported**; exactly TWO tuned dimensions (family, strength).
SURVIVORSHIP: both panels are current constituents, so every *level* is biased upward; the
verdict statistic is a within-cell difference (arm minus its own control, same panel/book/cost),
which the bias largely cancels out of.

Harness gates, asserted before any number was read: **[A]** `run()` with no instrument equals
`engine.backtest` at max|diff| = **0.000e+00** on returns and turnover; **[C]** `run(stop=S)`
reproduces idea 94's published `run_stop` at max|diff| = **0.000e+00** over all four depths
(idea 94's module is imported, not re-implemented). **[B]** is a reported gap, not an assertion:
weight-scaling a book by g is *not* idea 66's lever in this engine (the drift step re-normalises
against the cash line), so `dg` is priced with the lever convention throughout; the two conventions
differ by 0.0002 CAGR / 0.0016 Sharpe at g = 0.60.

## 1. The pre-registered test (arm − own control, annualised within regime, pp/yr, 10 bps)

| family | cells | cheaper in crashes | median crash | median trend | median gap | min gap | max gap |
|---|---|---|---|---|---|---|---|
| 200d gate | 16 | **2/16** | −5.08 | −0.51 | **−4.87** | −9.43 | +1.04 |
| 3% band | 16 | **0/16** | −4.20 | −0.01 | **−4.44** | −7.56 | −0.29 |
| abs momentum | 16 | **0/16** | −4.85 | −0.54 | **−4.23** | −8.87 | −0.01 |
| ddctl (idea 40) | 16 | **2/16** | −4.06 | −0.31 | **−3.76** | −8.60 | +5.63 |
| stop (idea 75 ref) | 16 | **1/16** | −2.79 | −0.51 | **−2.21** | −3.92 | +0.17 |
| **de-gross (dg)** | 16 | **16/16** | **+4.92** | −6.48 | **+11.54** | +4.71 | +23.16 |

Every *conditional* instrument the project owns is **dearer in the crash regime than in trends**,
by 2.2–4.9 pp/yr of median gap, and the ordering is the flip-rate ordering ideas 55/57/4 predicted
(200d gate 10.8x/yr turnover, worst gap; ddctl 5.6x/yr, mildest of the gates). Idea 75's sign
reversal was therefore **not a stop property** — it is a property of arming anything on a regime.

The single YES is `dg`, and it is a YES by arithmetic rather than by timing: holding less is
mechanically profitable whenever the market falls and mechanically costly when it rises, so its
crash/trend gap is forced (+11.5 pp/yr median, 16/16). It cannot be "armed in crashes", because
arming it *is* the ddctl row above — and ddctl is dearer in crashes in 14/16 cells.

Robustness, never selected on: under idea 75's `breadth20` regime instead of `spy200`, the gaps
shrink (the regime is rarer: 8.1–8.6% of days vs 17.1%) but no ordering changes — 200d −1.78,
abs −0.59, ddctl −3.70, stop −2.16, band +0.03 (8/16, the one family that reaches a coin flip),
dg +14.80 (16/16). At 25 bps the gates get *worse*, not better: 200d −5.69, band −4.99, abs −4.64,
ddctl −3.83, stop −2.60, dg +11.59.

## 2. Both KEEP paths (10 bps, all 96 instrument arms + 4 controls)

4a passes 23/96, 4b passes 25/96; **all four no-instrument controls fail both paths on DD**, which
is the whole point — the instruments do buy drawdown. Best 4b arms are the project's already-known
books rediscovered, not new candidates: `u56/EWALL0/band 3%` 12.3% / 1.168 / −17.6%, halves
1.217/1.136, OOS 1.211, 4.3x turnover (this is idea 57's `ew-band3`); `u56/CAND20/ddctl 12%`
14.7% / 1.164 / −17.8%, halves 1.279/1.071, OOS 1.138. SPY over the same window: 15.2% / 0.889 /
−33.7%, halves 0.957/0.834, OOS 0.882. RULES v1: 6.5% / 0.664 / −13.8% (u56).

**No new KEEP is proposed**, because these full-sample passes are not what rule 8 picks:

## 3. Rule 8 walk-forward — (family, strength) on 2009–2016, 2017–2026 read once

| panel/book/cost | IS pick | OOS Sharpe | control OOS | regret | best available OOS |
|---|---|---|---|---|---|
| broad/CAND20/10 | abs/378 | 0.925 | 0.936 | −0.011 | 200d/200 (0.950) |
| broad/CAND20/25 | abs/378 | 0.793 | 0.813 | −0.020 | 200d/200 (0.822) |
| broad/EWALL0/10 | ddctl/0.20 | 1.088 | 1.104 | −0.016 | ddctl/0.08 (1.178) |
| broad/EWALL0/25 | ddctl/0.20 | 1.073 | 1.093 | −0.020 | ddctl/0.08 (1.144) |
| u56/CAND20/10 | 200d/150 | 1.046 | 1.175 | **−0.129** | band/0.08 (1.178) |
| u56/CAND20/25 | dg/0.45 | 1.081 | 1.081 | 0.000 | band/0.08 (1.085) |
| u56/EWALL0/10 | 200d/150 | 1.015 | 1.140 | **−0.126** | ddctl/0.08 (1.256) |
| u56/EWALL0/25 | band/0.08 | 1.156 | 1.130 | **+0.027** | ddctl/0.08 (1.229) |

Mean OOS regret vs doing nothing **−0.0368**, median −0.0178, **wins 1/8**. Restricting the
chooser to the queue's slow set only gives the identical table (the stop is never picked).
OOS benchmarks: RULES v1 7.7% / 0.747 / −13.8% (u56) and 5.9% / 0.576 / −21.2% (broad);
SPY 15.5% / 0.882 / −33.7%. This is another do-nothing win for the record.

## 4. What this settles

1. The queue's premise — "the slow instruments might be the ones that are cheap in crashes" —
   is **refuted for all five of them**. The regime split does not rescue any gate.
2. The mechanism is confirmed as flip rate, not regime: gap magnitude orders with turnover
   (200d 10.8x → −4.87; band 7.3x → −4.44; ddctl 5.6x → −3.76; dg 2.4x → +11.54).
3. Any future "arm X only in crashes" proposal should be presumed dead on arrival unless X is
   unconditional de-grossing, in which case arming it *is* ddctl and ddctl is priced above.
