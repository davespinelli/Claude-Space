# Idea 602 — is-the-MATCHED-GROSS-TWIN-win-rate-a-FIRING-RATE-function (lane C, 2026-09-10)

**Verdict: SPLIT.** The queue's hypothesis is **KILLED as pre-registered** — the matched-gross twin
win rate is *not* a monotone function of the realised firing rate in any useful sense, and it is
**REVERSED** in ABS. But the worry underneath it ("then the record's *a gate is only a gross dial*
claims are rate-conditional") is **REFUTED, not confirmed**: a rate-matched, information-free
placebo's twin win rate *falls* with the rate, so the twin leg measures information, not exposure.
Two dials the record has not been quoting do move it: **cost** and **depth**. No book promoted, no
RULES change, no PARK. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.

Script `2026-09-10_is-the-MATCHED-GROSS-TWIN-win-rate-a-FIRING-RATE-function_C.py`;
console `.console.txt`; artefacts `.cells.csv` (1 989 rows), `.placebo.csv.gz` (12 960),
`.walkforward.csv`, `.claim.csv`, `.curves.csv`, `.monotone.csv`, `.predictors.csv`,
`.sufficiency.csv`, `.excess.csv`, `.gates.csv`, `.g3.csv`.

---

## 0. Gates — five, all pre-registered, all printed before any new number was read

| Gate | Result |
|---|---|
| **G1** derived cost rung `r(c) = r(0) − turnover·c/1e4` vs live `engine.backtest(c)` | **0.000e+00** (bar 1e-12) → PASS |
| **G2** idea 84's ungated EWALL U56 g=0.85 @10bps | 11.755% / 1.046 / −17.894% / H 1.073 / 1.025 vs committed 11.8% / 1.05 / −17.9% / 1.07 / 1.04 → PASS |
| **G3** idea 399's committed `.matched.csv`, **all 270 rows joined**, re-run under its own 2dp twin convention | **2.220e-16** (B136 2.220e-16, U56 2.220e-16, SMALL439 9.714e-17) and it reproduces idea 399's headline **exactly: QROLL 208 of 216, QEXP 31 of 54** → PASS |
| **G4** twin gross interpolation (0.01 cache → exact g) vs a true backtest, 6 off-grid g per panel | max \|dSharpe\| **3.743e-07**, max \|dr\| 5.748e-07 (bar 1e-3) → PASS |
| **G5** placebo matching identity (RAND/BLOCK share the real arm's on_share, gap and g_eff) | **0.000e+00** on all three panels × 2 160 cells → PASS (exact by construction) |

G3 matters: idea 399's twin numbers are reproducible to machine precision on **all three panels**,
including U56, which idea 399's own G3 could not reproduce against idea 336. So everything below is
a re-reading of the *same* numbers, not of a different vintage. G4 also disposes of confound (iii):
idea 399's 2dp twin-gross rounding is worth ≤ 4e-07 of Sharpe, so it changed nothing.

## 1. Population — 1 944 gated cells, and the rate/depth axes are orthogonal

3 panels × 18 level-arms (ABS 3 / QEXP 3 / QROLL 12) × 3 depths × 2 cadences × 2 gross × 3 cost
rungs. `on_share` (the fraction of eval days the book is actually de-grossed, post-cadence,
post-shift) is a function of family × level × w × cadence only — **max spread over depths
0.00e+00** — so rate and depth are orthogonal here by construction and Q3 is a real test.
Ties (|dSharpe| ≤ 1e-12, ideas 594/595): **54 of 1 944**.

| panel | family | n | rate min / med / max | twin win rate | median dSharpe |
|---|---|---|---|---|---|
| B136 | ABS | 108 | 0.062 / 0.110 / 0.153 | 0.315 | −0.0086 |
| B136 | QEXP | 108 | 0.000 / 0.025 / 0.047 | 0.574 | +0.0056 |
| B136 | QROLL | 432 | 0.041 / 0.113 / 0.222 | **0.917** | +0.0398 |
| SMALL439 | ABS | 108 | **0.243 / 0.491 / 0.825** | **0.250** | −0.0373 |
| SMALL439 | QEXP | 108 | 0.000 / 0.019 / 0.051 | 0.426 | 0.0000 |
| SMALL439 | QROLL | 432 | 0.031 / 0.105 / 0.216 | 0.884 | +0.0194 |
| U56 | ABS | 108 | 0.070 / 0.124 / 0.173 | 0.778 | +0.0206 |
| U56 | QEXP | 108 | 0.002 / 0.032 / 0.052 | 0.667 | +0.0268 |
| U56 | QROLL | 432 | 0.042 / 0.109 / 0.198 | **0.986** | +0.0570 |

The single cleanest refutation is in this table: **SMALL439 ABS carries the highest firing rates in
the whole run (median 0.491, up to 0.825) and the LOWEST twin win rate (0.250)**, while U56 ABS, at
a quarter of the rate, wins 0.778. Idea 42's ABS family — the highest-rate family on every panel,
and the one idea 399 never gave a twin — is where the monotone story breaks.

## 2. Q1 — the pre-registered monotonicity bar FAILS

Bar: every adjacent bucket step non-decreasing **and** per-family Spearman ≥ +0.80, at every
K ∈ {3,4,5,6,8}, in both units (equal-count / equal-width) and on both rulers (buckets cut on the
pooled population / inside each family). Result over the 60 family × K × unit × ruler cells:

- only **32 of 60 are RESOLVABLE at all** — on the pooled ruler QEXP occupies **1 of 3** buckets, so
  **idea 399's between-family rate contrast was never a within-rate one** (pooled ruler: 8 of 30
  resolvable);
- **monotone_up in 4 of 60**; **rho ≥ +0.80 in 12 of 60**; min rho **−1.000**, median **+0.068**;
- the four monotone cells are all QEXP or QROLL on the within-family ruler at K=3.

Continuous reading, no buckets, at the PROTOCOL rung (10 bps, both gross, 648 cells):

| family | n | rho(rate, dSharpe) | AUC(rate → win) | win rate |
|---|---|---|---|---|
| ABS | 108 | **−0.4035** | **0.3310** (reversed) | 0.481 |
| QEXP | 108 | **+0.7041** | **0.9481** (the queue's direction) | 0.574 |
| QROLL | 432 | +0.2960 | 0.5234 (saturated at 0.963) | 0.963 |
| POOLED | 648 | +0.2043 | **0.5592** | 0.818 |

So the relation is **positive in QEXP, negative in ABS and inert in QROLL** — three signs on three
families. "Monotone across all three families" is false in the strongest available way.

## 3. Q2 — at matched rate the family effect does NOT vanish

Over the 35 rate buckets that carry two or more families with n ≥ 8, the between-family win-rate
gap is **median 0.417, max 0.800**. QROLL wins 0.89–0.98 in *every* bucket, including the lowest;
ABS wanders 0.17–1.00 with no order in the rate. Rate is not a sufficient statistic for the twin
win rate — the family label survives conditioning on it.

## 4. Q3 — rate is not the best predictor either, and two other dials are

Pooled AUC for the win label: **on_share 0.5592 | g_eff 0.5374 | gap (= rate × depth) 0.4759 |
depth 0.3480 | rate_inst 0.5604**. Nothing orders it well pooled; within ABS the best predictor is
**g_eff (0.7102)**, i.e. the *level* of exposure rather than its variation.

Two dials that *do* move it, neither of which the record quotes beside a twin claim:

- **COST.** QROLL 0.991 → 0.963 → 0.833 and ABS 0.574 → 0.481 → 0.278 at 0 / 10 / 25 bps. The twin
  win rate is largely a switching-cost statistic.
- **GROSS-INVARIANCE.** The same numbers at g = 0.75 and g = 1.00 (identical to 3dp in 5 of 6
  family × rung cells). A twin comparison is a *shape* statement, so the gross dial that decides
  most of the record's 4b verdicts cannot move it.
- **DEPTH**, monotone *downward* at every rate bucket (K=4, pooled): 0.25 / 0.50 / 1.00 →
  0.778/0.741/0.593, 0.963/0.926/0.815, 1.000/0.963/0.778, 0.852/0.815/0.593. Rate is hump-shaped
  in the same table; depth is monotone. The queue named the wrong dial.

## 5. Q4 — the placebo, and why the record's twin leg is NOT a rate artefact

Two nulls at the *identical* g_eff and therefore the *identical* twin (G5): **RAND** (iid days,
exact matched count) and **BLOCK** (circular shift of the real multiplier — exact rate *and* exact
run-length distribution, zero information). 12 960 cells, 10 seeds.

| K=5 rate bucket | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| bucket median rate | 0.031 | 0.062 | 0.101 | 0.131 | 0.198 |
| **REAL** | 0.636 | 0.894 | 0.937 | 0.879 | 0.746 |
| **BLOCK** | 0.264 | 0.297 | 0.258 | 0.236 | 0.239 |
| **RAND** | 0.051 | 0.001 | 0.000 | 0.000 | 0.000 |

Overall REAL **0.818** vs BLOCK **0.259** vs RAND **0.010**. The placebo curve is **flat to
falling** in the rate at every K (BLOCK rho −0.683 … −1.000; RAND −0.764 … −0.894). **If the twin
win rate were a firing-rate function, the placebo would show it — it shows the opposite sign.**
Real arms beat their own matched placebo mean: vs RAND 100% / 66.7% / 100%, vs BLOCK
**76.9% / 64.8% / 98.4%** (ABS / QEXP / QROLL).

And here is the one place the queue's intuition is right, on the *differenced* statistic rather than
the raw one — median excess of REAL over its own BLOCK placebo, by rate bucket:

| family | bk0 | bk1 | bk2 | bk3 | bk4 |
|---|---|---|---|---|---|
| QROLL | +0.0259 | +0.0446 | +0.0705 | +0.0695 | **+0.1017** |
| ABS | — | +0.0248 | +0.0241 | +0.0371 | +0.0171 |
| QEXP | +0.0069 | +0.0438 | — | — | — |

Inside QROLL the excess is monotone in the rate and its share > 0 rises 0.925 → 0.966 → 0.992 →
1.000 → 1.000. **A gate that fires more often carries more information per unit of exposure it
gives up — but that is a statement about the placebo-differenced excess inside one family, not
about the raw twin win rate, and it does not hold in ABS.**

## 6. Q5 — PROTOCOL KEEP paths and rule 8

Both paths on all 1 944 gated points: **4a 3, 4b 492, BOTH 1**. The 4a passes are all at **rung 0**
(zero cost), all B136 QROLL q=0.17 — the same shape as idea 399's 3-of-1296-all-at-zero-cost. At 10
and 25 bps: **4a zero**. 4b 492 splits 306 / 141 / 45 across 0 / 10 / 25 bps and is a
cost-and-gross artefact: at the PROTOCOL rung with g = 0.75 it is **24 of 324**, and B136's *ungated
parent already passes 4b there*, so 22 of those 24 are inherited.

Rule 8 (chooser over level × w × depth on IS ≤ 2016-12-31 Sharpe, OOS 2017+ read once, g = 0.75),
54 cells: beats do-nothing OOS **33 of 54** (QROLL **18 of 18**, mean +0.097…+0.122; ABS 12/18,
mean −0.024…−0.075; QEXP 3/18), beats SPY OOS 36/54, beats **RULES v2 OOS 5 of 54** (all QROLL, 4 of
them off the protocol rung), mean regret −0.118. At the protocol rung with g = 0.75 only **2 of 18
picks clear 4b, both B136 QEXP q=0.07 whose realised rate is EXACTLY 0.0000** — the gate never
fires, the book is bit-identical to its parent, and the parent passes 4b on its own. **Uninherited,
non-degenerate protocol-rung rule-8 4b passes: 0.** Nothing to promote.

**Rule 8 on the claim itself** (fit the rate → win relation on IS only, read OOS once) is the
sharpest result in the run: the sign **flips between halves in every family**.

| | ABS | QEXP | QROLL | POOLED |
|---|---|---|---|---|
| IS rho(rate, dSharpe) | +0.1848 | −0.3737 | −0.0819 | −0.1276 |
| OOS rho | **−0.6223** | **+0.7124** | **+0.4205** | **+0.3481** |
| IS AUC | 0.6410 | 0.2857 | 0.3204 | 0.3263 |
| OOS AUC | 0.0574 | 0.9656 | 0.8263 | 0.5951 |
| win-label agreement IS vs OOS | 0.269 | 0.509 | 0.542 | 0.491 |

IS-fitted buckets applied unchanged to OOS: monotone_up **False**, rho 0.400, span **+0.008**.
Label agreement is a coin flip. Even where the relation is strong in one window it does not walk
forward, so "the twin win rate is a firing-rate function" is **not a stable relation** and cannot
be used to re-price anything in the record.

## 7. Corrections and follow-ups

- **CORRECTION to the queue's framing of idea 399.** "The only difference being the realised firing
  rate" is wrong twice: QROLL and QEXP also differ in arm count (216 vs 54) and in a second dial
  (w), and on the pooled rate ruler the two families **share only 1 of 3 buckets**, so the published
  contrast was never a rate-matched one. Idea 399's numbers themselves reproduce at 2.220e-16.
- The record's "a gate is only a gross dial" claims are **not** rate-conditional. They are
  **cost-conditional** (0.991 → 0.833 over 0–25 bps) and **depth-conditional** (monotone downward),
  and they are **gross-invariant**, which is the opposite of what "a gross dial" implies.
- Any future twin comparison should publish a **BLOCK-placebo column** beside it: the twin win rate
  alone reads 0.818, and its information content is the 0.818 − 0.259 = 0.559 above the
  clustering-matched null, which is the number a reader wants.
- Follow-ups filed: 604 (census the record's twin/matched-gross claims for a placebo column),
  605 (is the twin win rate a SWITCHING-COST statistic — sweep bps on a fixed twin population),
  606 (does the QROLL placebo-excess rate slope survive outside the breadth family).

_Survivorship: all three panels are current-constituent lists, so CAGR and drawdown levels are
optimistic; the gate-minus-twin and real-minus-placebo contrasts are the durable part. SMALL439
starts 2010-01-04, so its halves are not U56/B136's calendar halves, and w=2016 spends half its
sample unarmed. Research, not investment advice._
