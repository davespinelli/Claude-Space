# Idea 82 — ranking-subtracts-value (lane B, 2026-09-06)

**ANSWERED. The queue's MEASUREMENT reproduces; its RECOMMENDATION is REFUTED. KILL of
"drop ranking from the candidate book entirely."** The composite ranking subtracts
*Sharpe* and adds *CAGR*, both at t > 4, so "does ranking subtract value" has no answer
until the metric is named — and 4b, the path that matters for real capital, has a CAGR
floor. No RULES change, no new KEEP-candidate, no memo. Nothing in `RULES.md`, `scan.py`,
`bot.py` or `baseline.py` touched.

Script: `2026-09-06_ranking-subtracts-value_B.py` · console
`…_B.console.txt` · grids `…_B.{grid,comparisons,fwd_vs_rand_seeds,cagr,bands,walkforward}.csv`

## Design

10 bps, weekly, next-day execution. Gate, cadence and ranking key are idea 73/240's,
imported verbatim. **Gross matched at 0.75 on every arm including EWall** (idea 73's
`CANDg` / idea 240's NORM); idea 73's literal `GROSS/n` is a gross ladder (ideas 240/244)
and is used only for the reproduction gate. Panels U56 / B136 / BSTK100, n ∈ {20,30,40,60}.
Two tuned parameters: **panel** and **n**. 126 points, all reported.

The queue's design conflates two things, stated before any number was read: `EWall` holds
every eligible name and `CANDg-n` holds n of them, so `EWall − FWD` is **concentration +
ranking**. This run adds the arm that separates them — `RAND`, n eligible names by a
per-name uniform score drawn once per seed and held constant through time (so its
persistence, and hence its turnover, is generated the way FWD's and REV's are), 8 seeds,
every seed reported.

Reproduction gate: `U56/CAND20 FIXED` **12.7% / 1.092 / −18.3%, halves 1.088/1.102**
against published 12.7%/1.093/−18.3%, 1.088/1.103 (the last-digit gap idea 81 logged);
`U56/RULES v1` 6.5%/0.664/−13.8% against 6.5%/0.666/−13.8%.
`B136/EWall` reproduces idea 10's 4b pass: **10.7% / 1.026 / −17.7%, halves 1.146/0.914,
OOS 1.019** against published 10.7%/1.027/−17.7%, 1.146/0.917, OOS 1.021.

## 1. The queue's statistic reproduces — on Sharpe

Over the 8 unsaturated cells (`sat_share ≤ 0.25`; a cell whose panel cannot supply n
names IS EWall and is not evidence about ranking — 4 of 12 cells excluded):

| comparison | mean ΔSharpe | t | positive |
|---|---|---|---|
| `EWall − FWD` (the queue's statistic) | **+0.0467** | +4.03 | 7/8 |
| `FWD − RAND` (what the ranking adds) | **−0.0213** | −1.73 | 1/8 |
| `FWD − REV` (is the key signed) | **+0.1803** | +5.66 | 8/8 |
| `EWall − RAND` (concentration alone) | **+0.0254** | +4.26 | 8/8 |

Per (cell, seed): `FWD − RAND` = **−0.0213, t −2.72, positive in 21/64**.
So the gap splits roughly in half: **+0.025 concentration, +0.021 ranking**. The single
cell that goes the other way is **U56 n=20 (−0.0145)** — the project's own universe at the
incumbent count.

## 2. The key is monotone, and informative

`FWD > REV` at t +5.66 is not consistent with a worthless key, so the 5 disjoint 20-name
rank bands were read directly. **Band 1–20 is the argmax on 3 of 3 panels** and Sharpe
falls across the bands (B136 0.943 → 0.779 → 0.605 → 0.711 → **0.384**; BSTK100 0.946 →
0.839 → 0.851 → 0.550 → **−0.007**). There is no interior optimum. The composite orders
names correctly.

## 3. Why both hold: the ranking buys return with drawdown

Re-read on CAGR and MaxDD over the same 8 cells:

| | mean | t | positive |
|---|---|---|---|
| CAGR: `FWD − EWall` | **+1.28 pp/yr** | +4.93 | 8/8 |
| CAGR: `FWD − RAND` | **+1.25 pp/yr** | +4.30 | 8/8 |
| \|MaxDD\|: `FWD − EWall` | +1.49 pp | +4.70 | 8/8 |
| \|MaxDD\|: `FWD − RAND` | +1.06 pp | +4.55 | 8/8 |

At n=20: U56 12.79% vs 10.40% (EWall) vs 10.14% (RAND); B136 12.99 / 10.72 / 10.88;
BSTK100 13.88 / 12.74 / 12.63. The ranking pays **0.86 pp of CAGR per pp of MaxDD** against
EWall and 1.18 against RAND. That is a risk-budget trade, not a destroyed edge — and it is
priced on the axis 4b bars.

The Sharpe gap is also not stationary: `EWall − FWD` is +0.035 (t +6.69, 8/8) in H1 and
+0.052 (t +2.74, 7/8) in H2, +0.067 OOS (7/8).

## 4. Rule 8 walk-forward (IS 2009–2016 chooses, OOS 2017–2026 read once)

Pooled equal-weight over the 3 panels:

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|
| ALL_ISARGMAX | 11.4% | **1.048** | −19.8% |
| **EWALL** | 11.4% | 1.047 | −19.9% |
| RAND20 | 11.3% | 1.007 | −20.4% |
| FWD_ISARGMAX | 13.0% | 0.972 | −22.0% |
| FWD20 | **13.3%** | 0.968 | −21.9% |
| SPY | 15.5% | 0.882 | −33.7% |
| RULES v1 | 6.5% | 0.609 | −18.7% |

`EWALL − FWD20` OOS Sharpe **+0.078, wins 2/3** (U56 −0.019, B136 +0.135, BSTK100 +0.119);
`EWALL − RAND20` +0.040, 3/3. The IS chooser over all 12 arms picked a RAND arm on 3/3
panels — i.e. it chose *not the composite*, and only tied EWALL (−0.002). **The same split
survives OOS**: every selector that keeps the ranking wins CAGR and loses Sharpe.

## 5. KEEP paths

4b passes **25 of 126** points: **EWall 1/3, FWD 5/12, REV 0/12, RAND 19/96, v1 0/3**. The
no-ranking book does not pass 4b more often than the ranked one (0.33 vs 0.42).

- `B136/EWall` — 4a **and** 4b, 10.7%/1.026/−17.7%, halves 1.146/0.914, OOS 1.019. This is
  idea 10's published book, reproduced, not a new candidate.
- `U56/FWD20` (= gross-matched CANDg-20) — 4b clean, 12.8%/1.064/−18.3%, halves
  1.068/1.066, OOS 1.131. **`U56/EWall` fails 4b on the CAGR floor alone** (10.4% vs 70% of
  SPY's 15.2% = 10.66%) — the bar the ranking exists to clear.
- `BSTK100` — nothing passes 4b at any arm or n; the whole panel fails on DD.
- REV passes 4b in 0 of 12 and 4a in 4 of 12.

## Verdict

**KILL of the strong recommendation.** Pre-registered condition (a) held (7/8), (b) held
(FWD−RAND is not reliably positive on Sharpe), (c) held (EWALL is not beaten OOS by the FWD
selectors) — so the rule *as I wrote it* would uphold "drop ranking". That pre-registration
is itself the defect the run exposes: **it was Sharpe-only**, and on CAGR the same eight
cells reverse at t +4.30, 8/8. A recommendation to delete the ranking from the candidate
book would surrender 1.25–1.28 pp/yr of CAGR to buy 0.02 of Sharpe, and would push
`U56/EWall` below 4b's CAGR floor. Idea 73's headline is real, correctly measured, and
**misnamed**: it is a statement about a risk-budget preference, not about whether the
composite key works. Half of it is not about ranking at all.

**SURVIVORSHIP.** B136 / BSTK100 are current constituents, one-directional, and the bias
runs *toward* this run's Sharpe result: on a list of known survivors, holding everything
inherits the full survivorship premium while any selection rule can only redistribute it.
The pro-EWall half of the finding is therefore partly manufactured by the panel; the
pro-ranking CAGR half is measured against that headwind.

**Follow-ups queued:** 258 (price the trade on idea 74's exchange-rate menu), 259 (does the
Sharpe/CAGR reversal appear at every published EWall-vs-ranked claim), 260 (re-run with the
RAND arm re-drawn weekly to separate persistence from pick).
