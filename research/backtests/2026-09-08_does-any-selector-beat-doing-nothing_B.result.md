# idea 151 — does-any-selector-beat-doing-nothing (lane B, 2026-09-08)

**ANSWERED, and it is a SPLIT: KILL of the incumbent rule-8 default, KEEP of one alternative.**
The record's ~20 scattered "do-nothing wins" anecdotes are now a census, and it says the
incumbent **argmax-IS-Sharpe loses to inaction**, while **argmax-IS-CAGR beats it** — the same
selector gap idea 142 found on 48 cells, replicated here on a differently-composed 72.

## Corpus and gates

1,224 arm-rows = 3 panels (u56 / broad136 / small439) x 9 books at matched 0.75 gross
(6 on small) x **3 cost rungs {0, 10, 25 bps}** x idea 94's 17 arms = 72 cells. The **0-bps rung
is new** and is a reported axis, added because idea 235 asks whether "selection beats do-nothing"
is a rung artefact and the committed 10/25 corpus cannot answer that.

* Gate (a) — `H.run` vs `engine.backtest` on every ungated book: **0.000e+00 on all three panels.**
* Gate (b) — idea 142's committed 816-row grid, all 14 metric columns: **max |diff| 3.6e-15**
  (turnover; every return column at 1e-16), **BIT-EXACT on u56, broad and small.** Idea 401's
  restatement no longer bites, both grids being on today's `data/prices.csv`.
* Gate (b2) — **0 of 192 argmaxes** move when re-run on idea 142's committed columns.

## The answer (72 paired cells; `d` = the default's pick minus the do-nothing control)

| default (unscreened pool) | no-op | helps | hurts | win rate | mean d(OOS Sharpe) | t | sign p |
|---|---|---|---|---|---|---|---|
| **K_Sharpe (the incumbent)** | 17 | **18** | **37** | **0.327** | **-0.0241** | -3.34 | 0.014 |
| K_CAGR | 26 | **33** | 13 | **0.717** | **+0.0100** | +3.17 | 0.0045 |
| K_Calmar | 10 | 17 | 45 | 0.274 | -0.0200 | -2.89 | 0.0005 |
| K_MaxDD | 0 | 17 | 55 | 0.236 | -0.0740 | -4.98 | 0.0000 |
| K_Random (control) | 8 | 20 | 44 | 0.312 | -0.0196 | -2.60 | 0.0037 |

At **PROTOCOL's own 10-bps rung** the incumbent helps in **5 of 18** non-tied cells
(mean -0.0347, t -2.45, sign p 0.096). **P1 HIT, P2 HIT.**

**K_CAGR minus K_Sharpe, paired on identical cells: +0.0342 of OOS Sharpe (t +3.96, wins 36/43).**
Idea 142 published +0.0415 on 48 cells; this is +0.0342 on 72 with a rung it never saw — a
replication, not a re-read. It survives Bonferroni over the six defaults (0.0045 x 6 = 0.027).
The trade is explicit: K_CAGR buys **+1.36 pp** of OOS CAGR and gives back **1.61 pp** of OOS
drawdown against K_Sharpe.

## Three things this kills

1. **Idea 235's rung-artefact explanation — KILLED (P4 MISS, and the miss is the finding).**
   K_Sharpe's mean d is **-0.0126 (0 bps) / -0.0347 (10) / -0.0252 (25)** — non-monotone,
   `rho(d, cost) = +0.020`, and **negative at every rung including zero**. Selection does not lose
   to inaction because of costs; it loses on the merits.
2. **"The selector earns the drawdown" — KILLED (P5 HIT, but for the pool, not the selector).**
   Every default wins on OOS MaxDD: K_Sharpe 42/48 non-tied (+2.19 pp, t +5.00), K_CAGR 35/40,
   K_MaxDD 69/71. **So does the RANDOM control (40/55, +2.11 pp)** — and K_Sharpe minus K_Random
   on OOS MaxDD is **+0.0008 (t +0.13), not separable.** The de-risking belongs to the arm menu
   (gates, stops, DD controls, entry budgets), which is defensive by construction; any draw from
   it is shallower than the control. Idea 163's hypothesis is true of the **menu** and false of
   the **chooser**.
3. **"The IS-4b screen changes the pick" — the change is ABSTENTION, not re-selection.**
   The screen alters K_Sharpe's pick in 38 of 72 cells, but **33 of those 38 are the screen
   admitting nothing and forcing the control**; on the 32 cells where it admits something it
   re-picks **5 times (15.6%)**. P6 as I worded it MISSED because I forgot the fallbacks; its
   substance — near-inert on picks — is the fourth reproduction of ideas 132/140 and agrees with
   yesterday's cloud result that abstention is the whole screen.

## What separates a good pick from a bad one

Spearman over K_Sharpe's 72 cells, reported not selected on:

* `rho(d, IS_argmax_margin) = **-0.383**` — **the more decisive the in-sample argmax, the worse
  it does out of sample.** IS confidence is negatively informative. This is the sharpest
  mechanism the record has for why the incumbent default fails.
* `rho(d, TO_ratio) = **+0.544**` — selection pays only when it moves to a *higher*-turnover arm
  than the control; the modal failure is picking a cheap, gated, low-turnover arm.
* `rho(d, pool_mean_dSharpe) = +0.066` — **idea 204's pool-sign explanation does not carry here.**
* `rho(d, cost) = +0.020`.

Clustering, made visible rather than hidden: K_Sharpe helps 9/27 (broad), 5/18 (small), 4/27
(u56); by book it helps 9/9 on R40 and **1/9 on V1u (mean -0.1039)**. 72 cells are not 72
independent observations.

## Rule 8 / benchmarks (OOS 2017-01-01.., read once)

Mean OOS Sharpe over all 72 cells: **do-nothing 0.9246** (CAGR 13.68%, MaxDD -24.75%) vs
K_CAGR **0.9346** / K_Sharpe 0.9004 / K_Calmar 0.9045 / K_Random 0.9050 / K_MaxDD 0.8506.
Reference: **RULES v2 (live) 1.0379, RULES v1 0.6001, SPY 0.8820 / 15.45% / -33.72%.**
No default's mean pick beats the live book out of sample.

**P3 SPLIT:** on the unscreened pool K_Sharpe (-0.0241) IS separable from the random expectation
(-0.0438, 400 draws/cell) at 1 se — the incumbent has real skill *relative to chance*. It is
still worse than not choosing. Selection beats random and loses to abstention.

## KEEP paths — 1,224 rows, nothing proposed

4a vs live RULES v2 **28/1224** (0 bps 23, 10 bps 5, **25 bps 0**; small panel **0/306** — 17th
reproduction of idea 136). 4b full-sample **198/1224**, OOS-window 4b 222. **BOTH paths: 8 rows**,
7 of them at 0 bps. The single 10-bps both-paths row is
`u56 / S3-50 / band3-rw`: **CAGR 11.3% / Sharpe 1.262 / MaxDD -11.6%, halves 1.279/1.249,
OOS Sharpe 1.289, 8.17x turnover** — an exact independent re-derivation of idea 142's standing
candidate, whose memo already blocks it at 25 bps. **No new KEEP-candidate, no memo, no RULES
change.** This run's finding is about PROTOCOL rule 8's machinery, not about a book.

## Caveats

Survivorship (idea 54) on all three panels: it inflates every CAGR level and the 4b counts, but
cannot flip a paired sign — both sides of every pair are drawn from the same flattered panel.
Idea 128: the IS window's shallower SPY drawdown biases the P_S1 screen toward admitting too
much. Idea 126: t+1 execution only. And the K_CAGR result is one corpus: it should be
pre-registered and re-run before PROTOCOL names a selector.

## Proposed PROTOCOL consequence (for the Sunday review; RULES/PROTOCOL untouched here)

Rule 8 currently says "parameters chosen on 2009-2016" without naming how. Every run in this
record has read that as argmax IS Sharpe. On this census that default is **worse than writing
down the ungated book and not choosing at all** (-0.0241, sign p 0.014), and a run that reports
"the IS chooser picked X" is reporting a step with negative expectancy. Minimum honest change:
**rule 8 must report the do-nothing control beside every chosen arm** so the reader can price the
selection. Stronger change, if idea 415 clears: **name argmax-IS-CAGR as the default.**

Script: `research/backtests/2026-09-08_does-any-selector-beat-doing-nothing_B.py`;
`.console.txt`, `.grid.csv` (1,224 rows), `.picks.csv`/`.walkforward.csv` (864 picks),
`.paired.csv`, `.keeppaths.csv`, `.restatement.csv` alongside.
