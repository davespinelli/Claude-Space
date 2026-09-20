# Idea 1785 (lane cloud, 2026-09-20) — DOES THE VOLTGT DIAL'S MATCHED-TWIN WIN SURVIVE A PAIRED CIRCULAR-BLOCK BOOTSTRAP?

**ANSWERED. SPLIT VERDICT — KILL THE SHARPE HALF, the drawdown half survives only at ~2 sigma and
only under one of the two standard CI conventions. NOT A KEEP. NO RULES CHANGE.**

Script: `research/backtests/2026-09-20_voltgt-twin-win-block-bootstrap_cloud.py`
(`.books.csv` 540 rows, `.bootstrap.csv` 540 rows x 2,000 draws, `.surface.csv` 200 rows,
`.walkforward.csv` 33 picks, `.gates.csv`, `.log.txt`). **GATES 12 of 12.** Deterministic, offline.
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched (rule 6).

## What was priced

Idea 1771's surviving claim — *"the vol target is the record's FIRST device to beat its own
realised-mean-gross-matched constant-gross twin: OOS +0.0587 Sharpe / +6.16 pp MaxDD on U56, win
share 0.810"* — was a POINT ESTIMATE with no standard error, and its "n" was quoted as 100 cells
that are 20 conventions x 5 targets on ONE 2,400-day tape. This run gives both differences their
own **paired circular-block bootstrap** SE (same block offsets applied to book and twin, so the
pairing survives; 2,000 draws per cell from a fixed md5 seed stream).

TUNED (2, protocol maximum, every grid point reported): block length `B` {5, 10, 21, 63} and the
twin's gross-matching window `M` {IS, FULL, OOS}. PUBLISHED, NOT TUNED: target `t` {0.08, 0.10,
0.12, 0.16, 0.20}, panel {U56, B136, SMALL665}, cost {0, 10, 25, 50} bps, sigma cell `(L=20, d=0)`,
weekly cadence, next-day execution, gross capped at 1.00.

**Replication first.** G1 the fast runner `== engine.backtest` at **1.4e-17 / 2.1e-17 / 3.5e-17**
(10 and 25 bps, three panels). G2 reproduces the standing memo's sections 2-4 at max |d| **2.76e-04**.
**G3 reproduces idea 1771's pooled headline exactly: U56 dSharpe +0.0587, dMaxDD +0.0616, win share
0.810; B136 +0.0503 / +0.0944 / 0.790.** G4 twins bisected to **2.2e-16**. G5 SMALL665 clears 4b at
**0 of 45** rows (memo addendum A2, fourth confirmation).

## V1 — THE SHARPE LEG IS NOT RESOLVABLE ON THIS TAPE

U56, memo rung `t = 0.16`, twin matched OOS (idea 1771's own comparand). Observed
**dSharpe +0.0930**, **dMaxDD +0.0760**.

| B | dSharpe SE | t | p | pct CI | pivotal CI | boot mean |
|---|---|---|---|---|---|---|
| 5 | 0.1156 | **+0.80** | 0.398 | [−0.119, +0.331] | [−0.145, +0.305] | +0.0869 |
| 10 | 0.1198 | **+0.78** | 0.450 | [−0.122, +0.338] | [−0.152, +0.308] | +0.0819 |
| 21 | 0.1072 | **+0.87** | 0.400 | [−0.112, +0.295] | [−0.109, +0.298] | +0.0761 |
| 63 | 0.0899 | **+1.04** | 0.307 | [−0.088, +0.259] | [−0.073, +0.274] | +0.0713 |

| B | dMaxDD SE | t | p | pct CI | pivotal CI | boot mean |
|---|---|---|---|---|---|---|
| 5 | 0.0356 | +2.13 | 0.010 | [−0.021, +0.114] | [+0.037, +0.173] | +0.0333 |
| 10 | 0.0451 | +1.68 | 0.022 | [−0.023, +0.139] | [+0.013, +0.175] | +0.0390 |
| 21 | 0.0417 | +1.82 | 0.010 | [−0.016, +0.131] | [+0.021, +0.167] | +0.0445 |
| 63 | 0.0389 | +1.95 | 0.007 | [−0.013, +0.103] | [+0.049, +0.165] | +0.0466 |

**V1 TRIGGERED at 4 of 4 block lengths.** The Sharpe difference is under one standard error at every
block length, its two-sided bootstrap p never drops below 0.307, and **both** CI conventions cover
zero. Across the whole OOS grid (180 cells = 3 panels x 5 targets x 3 M x 4 B) only **0.033** reach
|t| >= 2 on dSharpe, and on U56 and B136 the 95% CI covers zero in **1.000** of cells under both
conventions. The claim "the vol target beats its matched twin on Sharpe" is **below this tape's
resolution**, and so, symmetrically, is idea 1771's *opposite* claim on SMALL665: the −0.1929 mean
loss there reaches |t| >= 2 in only **0.100** of cells. **KILL both readings of the Sharpe leg.**

## V2 — THE TWO LEGS DISAGREE, AND THE DRAWDOWN LEG IS THE ONE THAT CARRIES SIGNAL

OOS, 10 bps, all panels x targets x M x B:

* **dSharpe:** mean obs +0.0207, share obs > 0 **0.667**, share |t| >= 2 **0.033**.
* **dMaxDD:** mean obs +0.0928, share obs > 0 **1.000**, share t >= 2 **0.522** (U56 0.567,
  B136 **1.000**, SMALL665 0.000), share t <= −2 **0.000**.

The book's drawdown beats its matched twin's at **180 of 180** cells and does so resolvably at half
of them. The two legs are never averaged and must not be quoted as one "twin win".

## V3 — THE dMaxDD SE IS STABLE, BUT THE TWO CI CONVENTIONS DISAGREE AND THAT IS THE REAL LIMIT

The dMaxDD SE moves only **1.27x** from B=5 (0.0356) to B=63 (0.0389) — V3 PASS, the block bootstrap
is a usable instrument for this leg. But the **percentile CI covers zero at 1.000 of 180 cells while
the pivotal CI excludes it at 1.000 of U56 and B136 cells.** The two disagree because the bootstrap
draw distribution of dMaxDD is **downward-biased**: its mean runs +0.033 to +0.047 against an
observed +0.076, because circular block resampling shreds the long declines that make a drawdown.
Neither convention is wrong; the honest statement is the range. **The drawdown win is supportable at
roughly 1.7-2.1 sigma and no further, and any wording that leans on it must say which CI it used.**

## V4 — RULE 8 (parameters on 2009-2016 only; 2017-2026 read ONCE)

Adding the bootstrap-t as a chooser statistic is legal (the IS bootstrap reads nothing after
2016-12-31). 33 legal picks: **4b OOS 17 of 33, 4a OOS 3 of 33** (U56 11/11 and 0/11, B136 6/11 and
3/11, SMALL665 0/11 and 0/11).

| chooser | 4b OOS | 4b FULL | picks |
|---|---|---|---|
| `C_ISSHARPE` | 2/3 | 2/3 | 0.16, 0.20 |
| `C_GXS_IS` (twin-corrected Sharpe) | 2/3 | 2/3 | 0.16, 0.20 |
| `C_GXDD_IS` (twin-corrected MaxDD) | 2/3 | 1/3 | 0.08, 0.10, 0.12 |
| `C_BOOTT_S` (bootstrap t of dSharpe) | 4/12 | 4/12 | 0.16, 0.20 |
| `C_BOOTT_D` (bootstrap t of dMaxDD) | **7/12** | **0/12** | 0.08, 0.16, 0.20 |

* **`C_BOOTT_S` is a provable no-op**, exactly like idea 1793's `C_GXS`: it makes the IDENTICAL pick
  to plain `C_ISSHARPE` at 4 of 4 block lengths on all three panels. Dividing an unresolvable
  difference by its own SE does not make it informative.
* **`C_BOOTT_D` reproduces `C_GXDD_IS` on U56** (`t = 0.08`, OOS **11.38% / 1.2999 / −12.28%**,
  4b OOS PASS) at all four block lengths — but that cell **fails 4b FULL on the CAGR floor**
  (10.22% against 0.70 x SPY = 10.58%), which is why its 4b FULL count is 0 of 12. A chooser that
  passes OOS and fails FULL is not a capital recommendation.
* **And it is block-length fragile on B136:** `B = 5` picks `t = 0.20` (OOS 1.1726 / −20.46%,
  **4b OOS FAIL**) while `B >= 10` picks `t = 0.08` (1.2447 / −10.86%, PASS). The tuned dial moves
  the verdict.

## Capital arm — every grid point, 10 bps, M = IS

U56 FULL: SPY 15.12% / 0.8844 / −33.72%; live RULES v2 8.62% / 1.2011 / −12.05%.
U56 OOS: SPY 15.26% / 0.8738 / −33.72%; live RULES v2 9.46% / 1.2769 / −12.05%.

| t | U56 FULL | 4b | U56 OOS | 4b |
|---|---|---|---|---|
| 0.08 | 10.22% / 1.1803 / −12.28% | . | 11.38% / 1.2999 / −12.28% | P |
| 0.10 | 12.24% / 1.2032 / −14.55% | P | 13.23% / 1.2922 / −14.55% | P |
| 0.12 | 13.74% / 1.2103 / −16.44% | P | 14.56% / 1.2728 / −16.44% | P |
| 0.16 | 15.61% / 1.2028 / −19.86% | P | 15.94% / 1.2196 / −19.86% | P |
| 0.20 | 16.49% / 1.1789 / −20.82% | . | 16.92% / 1.1967 / −20.82% | . |

B136 OOS runs 10.97%-16.46% / 1.1726-1.2447 / −10.86% to −20.46% against SPY 15.26% / 0.8739;
**SMALL665 OOS runs 2.90%-7.45% / 0.3700-0.4901 / −21.87% to −33.78%, 4b 0 of 45 at every cost
rung.** Cost ladder (15 M=IS books): 4b FULL **8 / 6 / 6 / 5** and 4b OOS **8 / 8 / 7 / 5** of 15 at
0 / 10 / 25 / 50 bps; 4a FULL 1 / 1 / 0 / 0 and 4a OOS 1 / 1 / 1 / 0. Binding 4b legs OOS at 10 bps:
`L4_DD` 7 of 15, the other three 5 each.

**PATH 4a: KILL.** 3 of 33 legal picks, all B136 at `t = 0.08`, and only against the live book
restated on B136 (1.1019) rather than the real live U56 comparand (1.2769) — the same
panel-restatement artefact ideas 1763 and 1793 recorded.

## What this changes in the record

1. **Idea 1771's headline sentence must lose its Sharpe half.** "The first device in the record to
   beat its matched twin" is true only of the DRAWDOWN leg, and only at ~2 sigma under the pivotal
   CI. The +0.0587 is reproduced exactly (G3) and is **not distinguishable from zero**.
2. **Idea 1537's paired circular-block bootstrap of this dMaxDD is now run.** The instrument works
   for the drawdown leg (SE stable to 1.27x across the ladder) and the answer is "marginal", not
   "significant".
3. **The 0.810 win share is not independent evidence** and should not be quoted as if it were: those
   100 cells share one tape, and the bootstrap of the very same difference cannot reject zero.
4. **No new KEEP-candidate.** The standing VOLTGT memo's status stays **PARK** (ideas 1771 / 1767 /
   1793); nothing here restores it. Idea 1793's `C_GXDD` KEEP-4b candidate is untouched — note only
   that its U56 pick (`t = 0.08`) is the same cell this run finds failing 4b FULL on the CAGR floor.

## Caveats, stated

**SURVIVORSHIP:** U56, B136 and SMALL665 are CURRENT constituents of their screens; delisted names
are absent, so every number above is the optimistic read. SMALL drops 54 tickers with
`max_1d_move >= 1.0` per `data/small_meta.csv` before anything is computed. The bootstrap treats the
2,400-day OOS tape as the population; it prices sampling noise on THIS tape and says nothing about
regime change. MaxDD is a path statistic and block resampling biases it downward — quantified above,
not assumed away.
