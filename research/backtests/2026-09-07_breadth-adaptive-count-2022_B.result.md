# Idea 48 — breadth-adaptive-count-2022 (lane B, 2026-09-07) — **KILL**

Script: `research/backtests/2026-09-07_breadth-adaptive-count-2022_B.py`
Console: `research/backtests/2026-09-07_breadth-adaptive-count-2022_B.console.txt`
Grid: `research/backtests/2026-09-07_breadth-adaptive-count-2022_B.grid.csv`

## The question
Idea 46 killed the fixed-FRACTION rule as a general improvement over a fixed COUNT, but
noticed it won 2022 badly (f=0.35 −0.8%, f=0.45 −1.5% vs n=20's −9.0%, SPY −18.2%). Idea 48
asks whether that win can be bought without the bill: run fixed n=20 in broad markets and
switch to the fraction rule only when breadth `E_t` is in its own bottom quintile.

`HYB(q, f)`: narrow if `E_t <= Quantile_q(E_{<=t-1})` (**expanding**, min 252 obs, shifted —
causal), hold top `ceil(f·E_t)`; broad otherwise, hold top `min(20, E_t)`. Constant 75% gross
either way. Tuned: `q ∈ {0.10,0.20,0.30,0.40}` × `f ∈ {0.25,0.35,0.45,0.55}` = 16 points, all
reported. Fixed and not searched: n0=20, gross 75%, scorer without `/sqrt(vol20)`, 200d+vol20
eligibility, weekly, 10 bps, t+1. Controls: N20, NF20, F0.25/0.35/0.45/0.55/0.85/1.00, plus
three narrow-regime treatments at the pre-registered q=0.20 (CASH → flat, HALF → half gross,
FRAC → concentrate).

**Contamination declared up front:** 2022 is inside rule 8's OOS window, and the hypothesis
was generated from 2022. Every full-sample and stress-year number here is description. The
walk-forward is the evidence.

## Premise — the regime test does work
Causal narrow share at q=0.20: 13.3% of days overall, and **91% of 2022** (mean E_t 16.4 vs
37.5 full sample); 2015 38%, 2018 24%, 2020 21%. Agreement with a (non-tradable) full-sample
quantile: 93.4%. So the rule fires where the idea needs it; nothing below is a plumbing failure.

## Result
| book | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR/Sharpe/MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|
| N20 (idea 2's book) | 12.7% | 1.092 | −18.3% | 1.088/1.102 | 14.4% / 1.168 / −18.3% | no | **yes** |
| NF20 (the hybrid's broad leg) | 12.8% | 1.070 | −18.3% | 1.076/1.072 | 14.5% / 1.137 / −18.3% | no | yes |
| HYB q0.20 f0.35 | 13.7% | 1.070 | −21.5% | 1.011/1.127 | 16.2% / 1.183 / −21.5% | no | no (DD) |
| HYB q0.20 f0.45 | 13.5% | 1.073 | −19.7% | 0.991/1.148 | 16.3% / 1.204 / −19.7% | no | yes |
| RULES v2 (live) | 8.7% | 1.206 | −12.1% | 1.226/1.191 | 9.5% / 1.285 / −12.1% | — | — |
| SPY | 15.2% | 0.889 | −33.7% | 0.957/0.834 | 15.5% / 0.882 / −33.7% | — | — |

4b thresholds on this sample: MaxDD cap −20.2%, CAGR floor 10.7%.
Grid: **4a 0/27, 4b 14/27; of the 16 HYB points 4a 0/16, 4b 7/16** — and every 4b pass in the
grid is matched or beaten by a control the record already owns (N20, F0.45, F0.55, F0.85).

## The four things that kill it

**1. It loses to its own broad leg.** Against NF20 — the same rule with the conditional clause
deleted — HYB wins full-sample Sharpe at **4/16** points (mean **−0.011**) and has a **deeper**
drawdown at **16/16** (mean −3.2 pp). It beats its other parent F⟨f⟩ 16/16 (mean +0.042), but
that only restates idea 46: running the fraction rule sometimes beats running it always. The
clause's OOS Sharpe is better (11/16, mean +0.027) and CAGR is better (15/16, +0.67 pp/yr),
both bought entirely with drawdown.

**2. Rule 8 does not pick the 2022 defence.** With (q,f) chosen on 2009–2016 alone and
2017–2026 read once:

| family | rule | pick | OOS CAGR / Sharpe / MaxDD | 2022 | 4b |
|---|---|---|---|---|---|
| HYB | S1 IS-Sharpe | q0.40 f0.25 | 16.7% / 1.153 / **−25.0%** | +8.0% | **fail (DD)** |
| HYB | S2 4b-aware | q0.10 f0.25 | 16.3% / 1.185 / **−25.6%** | **−5.1%** | **fail (DD)** |
| F | S1 = S2 | F0.85 | 12.4% / 1.130 / −16.7% | −5.9% | pass |
| fixed n | S1 = S2 | N20 | 14.4% / 1.168 / −18.3% | −9.0% | pass |

Both hybrid picks blow through 4b's drawdown cap; both plain controls clear it. The in-sample
chooser lands on f=0.25 in both rules, and the S2 pick's 2022 is **−5.1%**, not the +1.5% the
idea was built on — the cell that delivers the 2022 defence is not the cell 2009–2016 selects.
No pick beats the live book on Sharpe (1.285 OOS).

**3. It does not survive a universe change.** On `universe_broad.json` (136 names): **HYB 4a
0/16, 4b 0/16, and 0/16 beat NF20 on Sharpe.** Every hybrid point fails H2, OOS *and* the
drawdown cap; NF20 fails on H2 alone and F0.85 still passes 4b. The clause is strictly harmful
there.

**4. The mechanism is concentration, not timing — and timing is what a bear defence needs.**
At the pre-registered q=0.20, holding the regime test fixed and varying only the treatment:

| narrow-regime treatment | CAGR | Sharpe | MaxDD | OOS Sharpe | 2022 |
|---|---|---|---|---|---|
| none (NF20) | 12.8% | 1.070 | −18.3% | 1.137 | −9.3% |
| CASH (flat) | 12.2% | **1.131** | **−12.7%** | **1.240** | −9.0% |
| HALF gross | 12.6% | 1.130 | −14.2% | 1.227 | −9.0% |
| FRAC (f=0.35) | 13.7% | 1.070 | −21.5% | 1.183 | **+1.5%** |

Only the concentration arm rescues 2022, and it is the only one of the three that makes the
book worse on drawdown. The two exposure arms return **−9.0%** in 2022, identical to no gate,
because the breadth flag is **lagging**: it fires in February 2022 (realised gross 0.52 in
January, 0.00 from February to November) so the book takes the January loss at full exposure
and then sits in cash through the Q4 recovery. Attribution agrees the concentration effect is
small: on the 591 narrow days the book earns −24.4%/yr under NF20 and −20.2%/yr under HYB — a
4.2 pp/yr rescue on 13.3% of days, i.e. ~0.6 pp/yr, bought with 3.2 pp of drawdown.

## Verdict — KILL
The conditional clause is not supportable. It loses to the simpler rule it wraps on
full-sample Sharpe and on drawdown, its walk-forward picks fail 4b on the drawdown cap while
both unconditional controls pass, and it reverses sign entirely on the broad universe. Idea
46's 2022 observation is real but is a concentration artefact of one narrow year, not a
timing edge, and it is not selectable ex ante. **No RULES change. No memo.**

## By-product for the queue (not a claim of this idea)
`DEC cash q0.20` — the pre-registered breadth flag used as a plain cash gate on top of NF20 —
is the highest-Sharpe non-live book on the grid: **12.2% / 1.131 / −12.7%**, halves 1.092/1.168,
OOS 13.8% / **1.240** / −12.7%, 9.7×/yr turnover, one parameter. It gives up 0.6 pp/yr of CAGR
against NF20 for 5.6 pp of drawdown and passes 4b (fails 4a: 1.131 < the live book's 1.206).
It is *not* a bear defence — its 2022 is −9.0% — so its Sharpe comes from the other narrow
episodes, and the lag it shows here is the thing to attack. Queued as idea 315.

## Caveats
`universe.json` is a 56-name current-constituent list, so absolute CAGRs are optimistic and
the hybrid holds most of it in the broad regime; the HYB-vs-parents comparison is the durable
part. The broad list (136 names) is also current-constituent. 2022 is the only year in the
sample where the narrow flag is on almost continuously, so every narrow-regime statistic here
rests on effectively one episode.
