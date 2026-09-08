# Idea 216R — a-flip-rate-estimator-that-is-not-confounded-by-block-count
### INDEPENDENT REPLICATION, lane B, 2026-09-08 (the cloud lane reached Done first; the two runs AGREE)

**ANSWERED / the queue's premise CONFIRMED / the estimator BUILT and then SUPERSEDED by a
closed form. No RULES change, no PROTOCOL edit, no KEEP, no new book. RULES.md, scan.py,
bot.py and baseline.py untouched.**

## What was asked

Idea 207 fixed clause 11b's draw count at K = 100 on a flip rate measured by cutting a
400-rotation pool into `floor(400/K)` DISJOINT blocks — 20 blocks at K=20 and **two** at
K=200, i.e. 190 pairwise comparisons per configuration falling to **one**. Idea 216 asked for
an estimator holding the comparison count fixed across K, so the recommendation rests on
something whose variance does not itself depend on K.

## What was built

The whole rotation **population** was enumerated rather than sampled: every one of the J−1
circular rotations for each of idea 207's own 90 configurations × 2 cost rungs = 180 rows,
N = 974 / 974 / 869 on U56 / BROAD136 / SMALL439 — **84,510 null backtests**. That gives an
exact population band and an exact population verdict, against which any K-draw can be scored.
Three estimators on the same pool, each replicated R = 8 times:

| | comparisons per configuration | what it measures |
|---|---|---|
| **D** disjoint (idea 207's) | 1128 at K=20 → **1** at K=400 | pairwise verdict disagreement |
| **P** paired fixed-B (the ask) | **200 at every K** | the same disagreement |
| **E** error vs the population | 200 draws at every K | `p_K`, the estimand |

## The answer

**1. The queue's premise is confirmed, and the artefact reappears at the new noisiest rung.**
D's replicate sd rises with K exactly as its comparison count falls — MAX 0.0015 → 0.0073
(4.8×), Q95 0.0017 → 0.0114 (6.7×) — and on Q95 it makes the ladder **non-monotone**
(0.0437 → 0.0359 → **0.0403** at K = 100/200/400). Under the fixed-B estimator the same
ladder is monotone (0.0424 → 0.0365 → 0.0348) and its sd is **0.0004 against D's 0.0114 at
K = 400, a factor of 28**. Idea 207's "Q95 disagreement rises 2.50% → 3.33% from K=100 to
K=200, zone widens 0.0097 → 0.0163" was its estimator, not the clause.

**2. The estimator has a closed form, so the Monte Carlo is not needed at all.** A K-draw's
verdict depends on the draw only through `X` = how many of the K sampled |dSharpe| reach the
real |dSharpe|; with an order-statistic band at level q it clears iff `X <= K − ceil(qK)`, and
`X ~ Hypergeom(N, M, K)` in the population's own exceedance count `M`. So

```
P(clear at K) = P(X <= c)      P(flip) = 2 P(A clears) P(B not clear | A clears)
```

is exact, has **zero** sampling error, and needs **one integer per configuration**. On the MAX
band, where the form is exact, it matches the B=200 Monte Carlo to **0.0009** across the whole
ladder (the Monte-Carlo se is 0.0026). This is the queue's estimator at B → ∞.

**3. The MAX band never fires at its own limit — 0 of 180.** With the population enumerated,
**not one configuration clears the MAX band** (Q95 clears 20.6%). Every MAX "clear" in the
record is therefore a finite-K false positive, and MAX's whole error ladder (17.68% at K=20
down to 1.03% at K=400) is its **size**, nothing else. Idea 207 called the max "a moving
target"; the population says the target is *unreachable*.

**4. The K recommendation.** On Q95 at fixed B, error against the population runs
6.76 / 4.30 / 3.41 / 2.67 / 2.02 % at K = 20 / 50 / 100 / 200 / 400 and the undetermined share
(configurations erring above the clause's own 5% size) runs 22.8 / 15.0 / **9.4** / 7.2 / 6.7 %.
There is **no interior optimum** — the ladder is monotone with diminishing returns, K=100 is a
floor and not an optimum, and past K≈200 the marginal gain is under half a percentage point
for double the compute. With the closed form available the draw count stops being a
statistical question at all: `M` can be computed once and `P(error at K)` read off exactly.

**5. Two pre-registrations were rejected and are reported as such.** P4 predicted MAX's error
would stay above 5% at K=400; it is **1.03%**, because a 400-draw from a 974-member population
is 41% of it and the sample max nearly is the population max — the bias argument was right
about the direction and wrong about the finite-population scale. P5 predicted Q95 below MAX at
every K ≥ 50; true at K = 50/100/200 and **false at K = 400** (2.02% vs 1.03%), for the same
reason. P2's second clause ("P's sd flat within 2×") is rejected on its literal ratio test
(3.2–3.3×) — the ratio was the wrong scale; the level at the noisy end is the 28× above.

**6. Rule 8 (PROTOCOL clause 8).** Clause read on the IS window only (≤ 2016-12-31), overlay
point chosen there, 2017-2026 read once, 18 cells. **Every one of the 12 clause-gated arms
loses to do-nothing** — best −0.0029, worst −0.0742, mean OOS Sharpe 0.7024-0.7737 against the
control's 0.7766 — while ORACLE-OOS buys +0.0431, so the ladder does have headroom and the
gate simply fails to find it. The IS-Sharpe argmax control also loses (−0.0361). This is the
**fourteenth consecutive** do-nothing win in this project.

**7. Both KEEP paths** on the 180 real rows: 4a (vs the panel's own RULES v1 at the row's own
cost rung) 37/180, 4b (vs SPY) 28/180, **BOTH 2/180**. 27 of the 28 4b passes are U56, and the
best-Sharpe 4b row (U56 DDCTL 0.15/0.5 @10bps, 1.1075 / −18.21% / OOS 1.1775) is **numerically
identical to its own untreated control** — the overlay never fires. Idea 435's point again:
the 4b passes are the carrier, not the instrument.

## Caveats carried

SURVIVORSHIP (idea 54): current constituents only; levels are biased upward and not tradable —
the clause reading is unaffected because real and rotated draws inherit it identically. The
rotation population is finite and neighbouring offsets are correlated: enumerating it removes
the pool-sampling layer but not the within-draw dependence, so every number is a statement
about clause 11b's own sampling scheme. BUDGET-skip's turnover infidelity (ideas 186/191/203)
is inherited, not fixed. Reproduction: `bt_np` equals `p191.fast_backtest` at **0.0e+00** on
returns and turnover; idea 201's published bands reproduce **bit-exactly on BROAD136 and
SMALL439 (median 8e-17)** and drift up to 1.49e-2 on **U56 only** — the one panel whose price
file has been re-cached since idea 201 ran, which is what a vintage drift should look like.

## Relation to the cloud lane

When this run started, a cloud-lane script for the same idea sat in the repo with no console,
no CSVs, no leaderboard rows and the idea still under `## Open`. The cloud lane's results
landed while this run's enumeration was going, so the two are a **replication pair** (as ideas
203 / 203R were), reached by different constructions — this run enumerates the population and
measures by Monte Carlo, the cloud run reads the closed form first.

**They agree on every shared count.** KEEP 4a 37/180, 4b 28/180, BOTH 2/180 — identical. The
hypergeometric identity, derived independently on both sides. 12 of 12 clause-gated arms losing
to do-nothing. K=100 a floor and not an optimum. And idea 207's estimator unbiased in its
**centre** — this run's disjoint estimator gives 0.1022 against the fixed-B 0.1011 at K=20 —
with only its **confidence** wrong, which is the cloud lane's phrasing too.

**One difference, and it is the estimand, not the answer.** The cloud lane scores error against
the record's nominal 0.05 permutation target and reads MAX's error as *rising* 0.0741 → 0.1596
in K. This run scores error against the *enumerated population verdict* and reads it as
*falling* 0.1768 → 0.0103. Both are the same fact — MAX's clear rate collapses as K grows — and
this run supplies the limit point the cloud series is heading toward: **the population MAX clear
rate is exactly 0 of 180.**

## Recommendation (proposed only; PROTOCOL.md untouched)

Replace clause 11b's draw-count sentence with the exceedance count. Exact wording, for the
Sunday review to accept or reject:

> **11b.** A clause's effect clears its null when `M`, the number of null draws whose
> |dSharpe| reaches the real |dSharpe|, satisfies `M <= N − ceil(0.95 N)` over the enumerated
> rotation population; where enumeration is too expensive, draw K rotations and report
> `P(error at K) = P(Hypergeom(N, M̂, K) <= K − ceil(0.95 K))` beside the verdict. **Never
> report a MAX band**: over the enumerated population it clears 0 of 180 configurations, so at
> finite K it is a pure size dial.
