# Idea 45 — position-count COST AND LIQUIDITY: what survives around idea 2's 4b KEEP?

**Script:** `2026-09-07_position-count-cost-and-liquidity_cloud.py`
**Book under test (verbatim, not re-tuned):** idea 2's KEEP — top-20 eligible by the v1 composite with the
`/sqrt(vol20)` scaler OFF, equal-weighted at a constant 75% gross (3.75% each), v1 eligibility (above 200d
MA, vol20 < 0.60), weekly, next-day execution. n held at the pre-registered 20.
**Two tuned parameters:** `cost_bps` ∈ {5,10,25,50} and `lag` ∈ {1,2,3,5,10} trading days. Panels U56 and
B136 are a structural variant, both reported. **40 cells, all reported** (`.grid.csv`, `.console.txt`).
**SURVIVORSHIP:** both universes are current-constituent lists; CAGR levels are optimistic, the cost/lag
*differences* much less so.

## Verdict: **KILL of the claim at PROTOCOL-plus cost rungs; the LAG worry is FALSIFIED.**
**4b 9/40, 4a 0/40.** Reproduction check: U56 @10 bps, lag 1 gives 12.66% / 1.092 / −18.31%
(H1/H2 1.088/1.102) — idea 2's published KEEP, reproduced.

### 1. Execution lag is not the threat. This is the queue's premise, refuted.
U56 @10 bps, lag 1 → 5 trading days (the "1-week execution lag" the idea asks for):
Sharpe 1.092 → 1.080 (−0.012), CAGR 12.66% → 12.98% (**+0.32pp**), DD −18.31% → −18.34%, and **4b still
PASSES at every lag from 1 to 5 days**. It breaks only at lag=10d, and then on DD (−22.87%), not on return.
The signal is slow: nothing about the edge is decision-day-specific. On B136 the same is true of the return
(CAGR *rises* with lag, +0.62pp at 10d) while DD widens monotonically (−20.05% → −26.51%), so lag costs risk
there, not return.

### 2. The cost rung is the threat, and the book's DD margin is not where it dies.
U56 anchor (lag=1) down the ladder — DD margin is essentially **flat** at +1.9pp (+0.0197 → +0.0157 from 5
to 50 bps), so the queue's "only 1.9pp of drawdown margin" is stable, not fragile:

| panel | 5 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|
| U56 | **PASS** (13.20%/1.134) | **PASS** (12.66%/1.092) | fail: **H1** (11.04%/0.967) | fail: H1+H2+OOS+CAGR (8.40%/0.757) |
| B136 | **PASS** (13.87%/1.007) | fail: **H2** (13.09%/0.957) | fail: H2+OOS (10.77%/0.808) | fail: H1+H2+OOS+DD+CAGR (7.02%/0.559) |

Interpolated breakeven of each 4b bar (lag=1):

| bar | U56 crosses zero at | B136 crosses zero at |
|---|---|---|
| H1 Sharpe vs SPY | 24.7 bps | 26.5 bps |
| H2 Sharpe vs SPY | 44.0 bps | **7.7 bps** |
| OOS Sharpe vs SPY | 46.2 bps | 11.0 bps |
| CAGR floor | 28.6 bps | 25.8 bps |
| DD cap | never in [5,50] | 26.0 bps |

**The book is a ≲25 bps claim on U56 and a ≲8 bps claim on B136.** At 9.63x/yr turnover (U56) and 13.77x/yr
(B136), each 5 bps of cost is 0.48pp / 0.69pp of CAGR per year; the cost gradient is −0.0417 / −0.0497 of
Sharpe per 5 bps, exactly the mechanical drag. This corroborates idea 47's 0/180 at 25 and 50 bps on the
fraction family, on a different book form.

### 3. 4a is 0/40 at every rung
RULES v2 on U56 runs 8.66% / 1.206 / −12.05% at 10 bps; the candidate never beats it in both halves with
no worse drawdown, at any cost or lag. Nothing here disturbs the live book.

### 4. Rule 8 walk-forward — lag chosen on 2008–2016, 2017–2026 read once
| panel, cost | chooser | OOS CAGR/Sharpe/DD | vs lag=1 anchor | regret | RULES v2 OOS | SPY OOS |
|---|---|---|---|---|---|---|
| U56 5 | lag=1 | 14.91% / 1.207 / −18.26% | +0.000 | 0.021 | 1.297 | 0.882 |
| U56 10 | lag=1 | 14.36% / 1.168 / −18.31% | +0.000 | 0.022 | 1.285 | 0.882 |
| U56 25 | lag=1 | 12.73% / 1.050 / −18.44% | +0.000 | 0.026 | 1.248 | 0.882 |
| U56 50 | lag=1 | 10.06% / 0.852 / −18.66% | +0.000 | 0.033 | 1.187 | 0.882 |
| B136 5 | lag=5 | 12.84% / 0.876 / −22.81% | −0.066 | 0.068 | 1.133 | 0.882 |
| B136 10 | lag=5 | 12.04% / 0.829 / −22.93% | −0.063 | 0.067 | 1.119 | 0.882 |
| B136 25 | lag=5 | 9.69% / 0.688 / −23.29% | −0.056 | 0.063 | 1.074 | 0.882 |
| B136 50 | lag=5 | 5.87% / 0.453 / −23.89% | −0.043 | 0.056 | 1.000 | 0.882 |

The IS chooser **never beats the lag=1 anchor OOS (0/8, mean −0.028)**, beats SPY OOS in 3/8 (the three
cheapest U56 cells) and RULES v2 OOS in **0/8**. It is the eleventh-plus instance in the record of an
in-sample chooser losing to doing nothing — here it costs 0.063 of OOS Sharpe on B136 by preferring lag=5.

## What this is owed as
No RULES change and no new KEEP. The honest re-statement of idea 2's standing 4b pass:
> *"idea 2's top-20 EQW@75% book clears 4b on U56 at 5 and 10 bps and at any execution lag up to one week,
> and on B136 at 5 bps only. Its binding bar under cost is H1 Sharpe vs SPY (U56, 24.7 bps) and H2 Sharpe
> vs SPY (B136, 7.7 bps), not its 1.9pp drawdown margin, which is flat in cost. At 9.6–13.8x/yr turnover
> the pass does not survive a 25 bps rung on either panel."*
