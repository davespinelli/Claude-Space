# Idea 207 — clause-11b draw count BY ENUMERATION (cloud, 2026-09-05)

> **Collision notice, stated first.** A sibling cloud lane answered idea 207 the same day from a
> **400-rotation sampled pool** and committed it as
> `2026-09-05_how-many-draws-does-clause-11b-need_cloud.*` (commit `f709548`) while this run's
> enumeration was in flight. Both runs claimed the idea while it was open; neither knew of the
> other. This file is **not** a replacement for that one — it is the same question answered with
> the **complete** rotation population instead of a sample, and section (6) reconciles the two
> line by line. Where they agree, the agreement is an independent cross-check; where they
> differ, the difference is exactly the sampling error both runs exist to measure.

**ANSWERED, and the question dissolves before it can be answered: clause 11b as written has no
right draw count, because the draw count IS the significance level.** The incumbent form
("clears iff |d_real| > max of n draws") is a hypothesis test of size exactly `1/(n+1)`, so
raising n from 20 to 200 does not measure the same clause more precisely — it silently replaces
a 4.76% clause with a 0.50% one. Rewritten at a FIXED level as a Monte-Carlo permutation
p-value, the sweep becomes meaningful, and then the answer is **enumerate**: the rotation
population is finite and small (J−1 = 974 on U56/BROAD136, 869 on SMALL439), so the complete
population costs 4.9× a 200-draw band and removes draw noise entirely. **No book proposed;
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

## Corpus

Idea 201/191's **90 configurations** (3 panels × 3 overlay families × 5 thresholds × 2 depths)
× 2 cost rungs = **180 cells**, every one of them enumerated in full:
**84,600 genuine backtests → 169,020 null rows** in 1687 s on 4 cores. Base book fixed at idea
2/78's top-20 EW composite, no vol scaler, gross 0.75, weekly, t+1; 10 and 25 bps derived
exactly from a single 0 bps run through the engine's own turnover series. Idea 208 enumerated
one panel; this run enumerates all three, so every number below is a closed-form property of a
known finite population rather than itself a sample.

Tuned parameters, exactly 2, all 24 grid points reported: **n_draw ∈ {20, 50, 100, 200}** and
**ε ∈ {0.05, 0.10, 0.20}** (the undetermined band). Clause form (MAXN incumbent / PVAL
level-α), panel, family, threshold, depth, cost rung and statistic are carried axes.

## Reproduction, asserted before any new number was read

| check | result |
|---|---|
| [a] `fast_backtest` vs `engine.backtest`, 3 panels | max\|dret\| 1.4e-17 / 2.1e-17 / 2.8e-17 — PASS |
| [b] cost identity, 10 bps from the 0 bps run, 3 panels | 1.4e-17 / 2.1e-17 / 2.8e-17 — PASS |
| [c] base CAND-20 weights vs idea 78/171 `weights_cand` | **0.000e+00** on all 3 panels — PASS |
| [d] RULES v1 on U56 @10bps Sharpe | 0.66418 vs published 0.66418 — PASS |
| [e] idea 191's published `clause.csv`, **180 of 180 rows** | max\|d\| 9.7e-17 (dSharpe, dSharpe_IS), 1.0e-16 (dMaxDD), 1.1e-16 (on_share) — PASS |
| [f] idea 208's `exact.csv`, 60 U56 cells × 3 statistics | 176/180 (K,N) identical; the 4 disputed comparisons are all cells where the real effect is 0 to machine precision (\|d\| = 1.1e-16–2.2e-16) with 169–352 rotations tied on it, and the largest \|rotation − real\| over every disputed rotation is **2.220e-16** — a tie-breaking convention, not a different population — PASS |

By-product of [f]: **ties are not a corner case.** Mean tied rotations per cell 84.2 (dSharpe),
**129.2 (dMaxDD)**, 95.8 (IS-Sharpe) out of ~974, with 75 of 180 cells carrying ≥1 exact tie on
drawdown. For a large minority of these overlays the rotation genuinely does nothing to the
statistic being tested, which is the resolution floor of any clause built on it.

## (1) The precondition the idea's wording hides — the draw count is the level

Every rotation in turn used as a pseudo-real and priced against the remaining N−1
(**169,020 pseudo-reals per row**):

| n_draw | nominal 1/(n+1) | measured size |
|---|---|---|
| 20 | 0.04762 | **0.04762** |
| 50 | 0.01961 | **0.01961** |
| 100 | 0.00990 | **0.00990** |
| 200 | 0.00498 | **0.00498** |

Exact to five decimals at every n. "How many draws does clause 11b need" therefore has no
answer in its own terms: n is not a precision dial, it is the α of the test.

## (2) Flip rate — 180 cells, expected disagreement with the enumerated truth (α = 0.05)

| rule | n=20 | n=50 | n=100 | n=200 |
|---|---|---|---|---|
| MAXN (incumbent), Sharpe | 0.0742 | 0.1009 | 0.1392 | **0.1739** |
| PVAL (level-α), Sharpe | 0.0742 | 0.0516 | 0.0312 | **0.0238** |
| PVAL, MaxDD | 0.0714 | 0.0533 | 0.0326 | 0.0187 |
| PVAL, IS-Sharpe | 0.0568 | 0.0349 | 0.0222 | 0.0159 |
| PVAL two-seed disagreement, Sharpe | 0.1003 | 0.0672 | 0.0416 | 0.0313 |

**Under the incumbent form more draws make the clause WORSE**: its expected error against the
truth more than doubles from n=20 to n=200, because the clause is walking away from the level
it is being scored at. Under the level-α form the error falls monotonically and the clearing
rate converges on the truth (E[clears] 0.1768 → 0.2120 against truth 0.2056). At n=20, 30.0% of
cells can never clear and 0.0% clear with certainty; at PVAL/200, 9.4% clear with certainty.

Against the verdicts actually committed to the LEADERBOARD — idea 191's published 20-draw
column — expected disagreement is **10.5% on Sharpe and 8.6% on drawdown**, and no draw count
reduces it (MAXN/200 raises it to 12.3%). That is the exact version of idea 201's sampled 17.8%
and idea 208's U56-only 10.0%.

## (3) Undetermined-zone width, in the units of the effect being tested

Mean |dSharpe| under test across the 180 cells = **0.0991**. Zone = the interval of true effect
sizes with P(clears) ∈ [ε, 1−ε], read off each cell's own population:

| rule | ε | n=20 | n=50 | n=100 | n=200 |
|---|---|---|---|---|---|
| MAXN width | 0.10 | 0.1031 | 0.1642 | 0.1861 | **0.1574** |
| PVAL width | 0.10 | 0.1031 | 0.0587 | 0.0319 | **0.0204** |
| PVAL width / mean effect | 0.10 | **104.0%** | 59.2% | 32.2% | **20.6%** |
| PVAL cells undetermined | 0.10 | 25.0% | 15.0% | 8.3% | 6.7% |
| PVAL width / mean effect | 0.05 | 163.3% | 82.3% | 41.8% | 26.8% |
| PVAL width / mean effect | 0.20 | 60.0% | 37.0% | 21.1% | 13.7% |

At the incumbent n=20 the clause cannot resolve a band **wider than the whole effect it is
testing**. Under MAXN the zone does not shrink at all — it widens, because the threshold
marches into a sparser and sparser tail.

## (4) Rule 8 — the clause as a selection gate, 18 cells × 200 draw regimes

Pick within (panel, family, cost rung) on IS ≤ 2016-12-31 by largest IS dSharpe among configs
whose IS effect clears the clause; abstain → hold the control book; read 2017–2026 once.

| arm | abstain | OOS CAGR | OOS Sharpe | OOS MaxDD | dOOS vs do-nothing | t |
|---|---|---|---|---|---|---|
| **S0 do-nothing (control book)** | 1.000 | **10.22%** | **0.7766** | −23.53% | — | — |
| NONE (IS argmax, no clause) | 0.000 | 9.37% | 0.7206 | −22.07% | −0.0560 | −1.66 |
| ENUM (exact population gate) | 0.556 | 9.16% | 0.7226 | −23.96% | −0.0540 | −2.50 |
| MAXN n=20 | 0.531 | 9.18% | 0.7222 | −24.13% | −0.0544 | −36.6 |
| MAXN n=200 | **0.851** | 10.05% | 0.7635 | −23.85% | −0.0131 | −14.0 |
| PVAL n=20 | 0.411 | 8.48% | 0.6743 | −22.24% | −0.1023 | −42.7 |
| PVAL n=200 | 0.457 | 8.61% | 0.6820 | −22.06% | −0.0946 | −40.3 |

References OOS: SPY 15.45% / 0.8820 / −33.72%; RULES v1 @10bps 7.73% / 0.7471 / −13.83% (U56),
5.94% / 0.5762 (BROAD136), 7.88% / 0.6617 (SMALL439).

**No gate at any draw count under either form beats doing nothing — the thirteenth consecutive
do-nothing win** (after ideas 110/132/151/166/171/174/177/181/186/191/194/201/208). And MAXN's
apparent improvement in n is entirely idea 194's dilution identity: its abstention rate rises
0.531 → 0.851 across the ladder, so it "improves" only by increasingly declining to act. The
draw alone moves the answer: per-seed mean OOS Sharpe ranges 0.0846 (MAXN/20) and 0.0950
(PVAL/20) across 200 seeds, still 0.052–0.057 at n=200.

## (5) KEEP paths (PROTOCOL 4)

On the 180 real overlay rows: **4a 37/180, 4b 28/180** (U56 27 — DDCTL 11, BUDGET 9, SLEEVE 7;
BROAD136 1; SMALL439 0 — idea 136's small-panel wall, fourth confirm). Of the 28 4b passes,
**0 clear their own null with probability 1 at n ≤ 50 under either form**, 3 do at PVAL/200, and
22–23 can never clear at any seed. No 4b pass on this grid is defensible as an overlay effect —
an independent third confirmation of ideas 191/208 on twice their corpus. This idea proposes no
book and claims neither KEEP path.

## (6) Reconciliation with the sibling 400-draw run

**Agreements, independently arrived at (different pools, different estimators):**

| quantity | this run (enumerated) | sibling run (400-draw pool) |
|---|---|---|
| the max-of-n band's size | **exactly 1/(n+1)**, measured on 169,020 pseudo-reals | same conclusion, inferred from band drift +65.9% and clear rate 15.6% → 2.2% |
| 4a / 4b passes on the 180 real rows | **37 / 28** | **37 / 28** |
| 4b passes clearing their own null | 0 with P=1 at n ≤ 50 | "all 28 inside their own band at K=200" |
| rule 8, do-nothing control S0 | **10.22% / 0.7766 / −23.53%** | **0.7766** |
| every clause-gated selector | loses to S0 (best −0.0131) | loses to S0 (best −0.0145) |
| SMALL439 4b passes | **0 / 60** | **0 / 60** |
| idea 201's published bands | reproduce at 9.7e-17 (180/180 real rows) | reproduce at 9.7e-17, flip count 32/180 exact |

**Two corrections this run's exact population supplies.**

1. **The rotation population is larger than the sibling run states.** Its caveat gives
   "J ≈ 670 on U56/BROAD136, ≈ 600 on SMALL439"; the enumeration counts **J − 1 = 974 (U56),
   974 (BROAD136), 869 (SMALL439)** — the same N idea 208 enumerated on U56. A 400-draw pool is
   therefore **41–46%** of the population, not the 60–67% claimed, which makes its
   block-resampling estimates noisier than its own caveat allows and strengthens rather than
   weakens its conclusions about the max form.
2. **"K = 200 doubles the cost for no measured gain" is a limit of the estimator, not of the
   draw count.** That reading rests on **one disjoint block pair per configuration** at K = 200,
   which the sibling run flags itself (its P5 miss). Under the exact law there is no block
   count: at a fixed level the error keeps falling — flip vs the truth **0.0312 (n=100) →
   0.0238 (n=200)** and the undetermined zone **0.0319 → 0.0204**, a further 24% and 36%. So the
   sibling's "the number is 100" is a floor, not an optimum; 200 is measurably better, and the
   complete population — 974 draws, **2.4× a 400-draw pool and 4.9× a 200-draw band** — is
   exact.

**One disagreement that is itself the finding.** The sibling run's realised clear rates at
K = 20 are 15.6% (Sharpe) and 6.1% (drawdown); the exact expectations over all 20-subsets of the
full population are **17.7% and 11.9%**. A single 20-draw realisation misses its own clause's
expectation by 2–6 percentage points — which is precisely the instability both runs were
commissioned to measure, showing up in the measurement of the measurement.

## Proposed PROTOCOL clause (for Sunday review; not applied here)

> **11b.** A null band is a hypothesis test and must be stated at a level, never as a draw
> count. Report `p = (#{|d_null| ≥ |d_real|} + 1) / (n + 1)` and clear at `p ≤ α` with α stated
> (α = 0.05 reproduces the incumbent max-of-20 exactly, and is the exact-inference form of the
> sibling run's Q95 proposal). Where the null population is finite and smaller than ~2000 —
> **every rotation null in this project is: J − 1 = 869–974** — **enumerate it in full** and
> report the exact p-value with the population size; the enumeration costs 2.4× a 400-draw pool
> and removes draw noise entirely. Where it must be sampled, **n ≥ 200** is the floor (2.4%
> expected verdict error, undetermined zone 21% of the mean effect); n = 100 is the sibling
> run's recommendation and is 31% worse on both (3.1%, 32%); n = 20 is not reportable (7.4%
> error, zone 104% of the effect). Publish the count of rotations tied with the real effect
> alongside the p-value — the median cell has **129 of 974** rotations tied on drawdown, which
> is the clause's resolution floor. The clause stays report-only: it may not gate or select.

## Pre-registered predictions: 3 of 5 hit

- **HIT** P1 — incumbent size = 1/(n+1) at every n: 0.04762 / 0.01961 / 0.00990 / 0.00498, exact.
- **HIT** P2 — level-α flip rate falls in n but stays ≥ 2% at n=200: 0.0742 → 0.0238.
- **MISS** P3 — zone shrinks ≥3× (5.05×, hit) but is 20.6% of the effect at n=200, not ≥50%.
  The level-α form is more effective at n=200 than predicted.
- **HIT** P4 — no clause-gated selector beats do-nothing OOS (best −0.0131).
- **MISS** P5 — 25.0% of the 180 cells undetermined at n=20/ε=0.10, not ≥80%. Idea 208's 83.3%
  was U56-only *and* measured against the max-of-20 band's own draw distribution; on the
  three-panel corpus with the zone defined by P(clears) the figure is four times smaller, so
  idea 208's headline overstates the general case.

## Caveats

Survivorship: BROAD136 and SMALL439 are current constituents only; SMALL439 is the 483-name
sub-$2B panel with the 44 `max_1d_move ≥ 1.0` tickers dropped per `data/small_meta.csv`, and its
bias is one-directional and falls hardest on beaten-down names. Idea 38's calendar-day index
after 2014-09-17 and idea 126's t+1 convention are inherited unchanged from the parents. The
result is about the CLAUSE, not about any book: it says nothing about whether an overlay works,
only that the published verdicts on 180 of them rest on a statistic that changes its own
meaning with its sample size.
