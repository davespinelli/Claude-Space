# Idea 431 — is K_MEDIAN a real abstention rule or a 36-cell accident? (lane C, 2026-09-08)

**Verdict: ANSWERED / SPLIT — the queue's PREMISE is CONFIRMED and its INSTRUMENT is KILLED.**
K_MEDIAN's positive OOS lift **replicates** on a corpus that shares no cell with idea 204's
(+0.0232, t +2.20, 26/36 — idea 204 had +0.0205, t +2.73, 28/36), so it was not a 36-cell
accident. It is also **not a rule**: the lift is measured against the pool mean, an object nobody
can hold, and it is *smaller than the do-nothing arm's own lift* (+0.0675, t +4.13). Every one of
the 13 grid points across both tuned parameters loses to do-nothing. **Idea 241's minimum-margin
rule is degenerate on this corpus** — 100% of pools have a top-2 IS gap under 0.15, so every
m ≥ 0.10 *is* do-nothing by construction. No book promoted, no KEEP candidate, no memo. PROTOCOL,
RULES.md, scan.py, bot.py and baseline.py untouched.

## Gate G0 — the premise, re-derived from idea 204's own committed grid (no re-simulation)
| selector | mean lift | t | wins | vs do-nothing | t | = DIALMID |
|---|---|---|---|---|---|---|
| **K_MED204** | **+0.0205** | **+2.73** | **28/36** | **−0.0182** | −2.53 | 52.8% |
| K_DIALMID (no performance data) | +0.0094 | +1.19 | 26/36 | −0.0293 | −2.98 | 100.0% |
| K_ARGMAX | +0.0075 | +0.52 | 19/36 | −0.0312 | −1.53 | 16.7% |
| K_ANTI | −0.0471 | −2.65 | 17/36 | −0.0858 | −4.11 | 5.6% |

Queue quotes +0.0205 / t +2.73 / 28-36 / −0.0182. Re-derivation matches at **|d| 6.25e-06** on the
lift and **5.99e-06** on the do-nothing delta. **G0 PASS.** G1 fast-vs-engine ≤ 1.04e-17 on returns
and 1.80e-16 on turnover; G5 rung identity 0.000e+00, all three panels.

## Corpus C — fresh, disjoint from idea 204's 36 cells on the family axis
3 panels (u56 56, broad 136, small 439) × 4 dial families × 3 rungs = **36 cells, 216 arm-rows,
12 simulated books**. Idea 204's families were GROSS / WIDTH / CADENCE / GATE-KIND; none of
BAND (band half-width, 7 arms) / MALEN (MA lookback, 6) / VOLCAP (extra vol20 cap, 6) /
MOMLOOK (top-20 signal-window scale, 5) turns any of those dials. The families necessarily meet
idea 204's corpus at **one arm each — the do-nothing control** — because "vs do-nothing" is the
comparison the queue asks about; stated, not hidden. No cell is shared.

## Q1 — the rank-quantile dial q (tuned parameter 1, all 5 grid points, 36 cells each)
| selector | mean lift | t | wins | sign p | vs do-nothing | t | wins |
|---|---|---|---|---|---|---|---|
| K_Q0.00 (argmin, power check) | −0.0688 | −4.78 | 6/36 | 0.000 | −0.1363 | −4.89 | 3/36 |
| K_Q0.25 | −0.0183 | −1.62 | 20/36 | 0.618 | −0.0858 | −4.05 | 7/36 |
| **K_Q0.50 (= K_MEDIAN)** | **+0.0232** | **+2.20** | 26/36 | 0.011 | **−0.0443** | −2.32 | 10/36 |
| K_Q0.75 | +0.0262 | +2.72 | 25/36 | 0.029 | −0.0413 | −3.22 | 5/36 |
| K_Q1.00 (incumbent argmax) | +0.0163 | +1.02 | 17/36 | 0.868 | −0.0512 | −2.56 | 7/36 |
| K_MED204 (idea 204's even-n convention) | +0.0320 | +2.39 | 27/36 | 0.004 | −0.0355 | −1.64 | 10/36 |
| K_DIALMID (reads no performance data) | +0.0371 | +4.77 | 30/36 | 0.000 | −0.0304 | −2.06 | 0/36 |

**The median is not a peak.** The positive-lift region is the whole top half of the IS ranking
(q=0.75 **+0.0262 ≥** q=0.50 +0.0232), and the shape that produces it is the bottom half being
bad (q=0.00 −0.0688, q=0.25 −0.0183), not the centre being good. "Pick the median" is one
arbitrary point on a flat plateau, and the convention alone (`round(q(n−1))` vs idea 204's
`index[len//2]`) moves the headline from +0.0232 to +0.0320.

## Q2 — idea 241's minimum-margin abstention rule (tuned parameter 2, all 7 grid points)
| m | abstain | mean lift | t | vs do-nothing | t | wins | mean OOS Sharpe |
|---|---|---|---|---|---|---|---|
| 0.00 (raw argmax) | 0.0% | +0.0163 | +1.02 | −0.0512 | −2.56 | 7/36 | 0.9268 |
| 0.05 | 83.3% | +0.0591 | +3.72 | −0.0084 | −0.62 | 3/36 | 0.9696 |
| 0.10 / 0.15 / 0.25 / 0.50 / ∞ | 100.0% | +0.0675 | +4.13 | **+0.0000** | n/a | 0/36 | 0.9780 |

Top-2 IS-Sharpe gap over the 36 pools: median **0.0242**, mean 0.0267, max **0.0786**;
**83.3% under 0.05 and 100% under 0.15**. So the margin rule has no operating range on a dial
corpus: any threshold a person would pre-register abstains always and *is* the do-nothing arm,
delta exactly 0.0000. The one threshold that ever trades (0.05) still loses. **The margin rule is
damage control on the argmax (−0.0512 → −0.0084 → 0.0000), never expectancy** — which is a real
finding for idea 241, just not the one it hoped for.

## Q3 — where the lift actually comes from (two decompositions, both exact)
`lift = TRANSFER + POSITION`, POSITION being the arm at the middle of the *printed dial order*
(zero parameters, no performance data):

| K_Q0.50 | mean | t | wins |
|---|---|---|---|
| lift | +0.0232 | +2.20 | 26/36 |
| POSITION (no selector content) | **+0.0371** | **+4.77** | 30/36 |
| TRANSFER (the only part that can be skill) | **−0.0138** | **−0.96** | 11/36 |

spearman(IS_Sharpe, dial position) +0.443; spearman(IS_Sharpe, OOS_Sharpe) +0.278 (23/36 positive).
**CONFOUND, disclosed:** the dial middle *is* the control arm in BAND/MALEN/MOMLOOK (100%) and not
in VOLCAP (0%) — overall 75% — because the adopted value sits at the centre of three of the four
grids by construction. K_DIALMID is therefore **not an independent rule**; it is "hold the adopted
arm" restated, and VOLCAP, the one family where the two differ, is the family where it loses to
do-nothing (−0.1218). That makes the second decomposition the load-bearing one:

`lift ≡ d_vs_ctl + CONTROL_LIFT`, closing at **0.00e+00 / 5.55e-17** on every selector, where
`CONTROL_LIFT = OOS(control) − pool mean` is the **pool deficit** — a property of the pool that
needs no selector at all.

| corpus | CONTROL_LIFT | K_MEDIAN lift | = | d_vs_ctl | + | CONTROL_LIFT |
|---|---|---|---|---|---|---|
| C (fresh) | **+0.0675** (t +4.13, 30/36) | +0.0232 | = | −0.0443 | + | +0.0675 |
| B (idea 204's) | **+0.0387** (t +3.56, 22/36; idea 204 published it as −0.0387, sign flipped) | +0.0205 | = | −0.0182 | + | +0.0387 |

**This is the answer.** Every "reliably positive lift" in the selector literature, K_MEDIAN's
included, is the pool deficit minus the selector's own loss. The do-nothing arm earns the whole
deficit for free; K_MEDIAN hands back 0.0443 of the 0.0675 (t −2.32) for the privilege of choosing.
Idea 204 had already published the corpus-B version of this number as **−0.0387** — the queue's
+0.0205 and that −0.0387 were never two facts, they were one.

## Clustering, printed rather than asserted (mean lift / mean vs-do-nothing)
K_Q0.50 by panel: broad +0.0227/−0.0042, small +0.0061/−0.1213, u56 +0.0409/−0.0073 (n=12 each).
By family: BAND +0.0071/−0.0015, MALEN +0.0179/−0.0500, MOMLOOK +0.0211/−0.0292, VOLCAP
+0.0469/−0.0964 (n=9). By rung: 0 bps +0.0362/−0.0231, 10 bps +0.0160/−0.0504, 25 bps
+0.0175/−0.0594. The lift is positive in 3/3 panels, 4/4 families and 3/3 rungs; the loss to
do-nothing is negative in 3/3, 4/4 and 3/3. **The sign is stable; 36 cells is still 36 cells.**

## Rule 8 walk-forward and both KEEP paths (scored because PROTOCOL 4 requires it)
Every selector reads IS ≤ 2016-12-31 only and 2017–2026 is read once. At the 10 bps rung, averaged
over the 12 cells:

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | dS vs RULES v2 | dS vs SPY | dS vs do-nothing |
|---|---|---|---|---|---|---|
| K_Q1.00 (argmax) | 8.77% | 0.9149 | −15.36% | −0.0751 | +0.0329 | −0.0702 |
| K_Q0.50 (K_MEDIAN) | 8.37% | 0.9347 | −14.82% | −0.0553 | +0.0527 | −0.0504 |
| K_MED204 | 8.74% | 0.9783 | −15.20% | −0.0117 | +0.0963 | −0.0068 |
| K_DIALMID | 8.90% | 0.9551 | −15.24% | −0.0349 | +0.0731 | −0.0300 |
| **do-nothing (= K_M≥0.10)** | **9.25%** | **0.9851** | **−15.59%** | −0.0049 | **+0.1031** | 0.0000 |

SPY OOS 15.45% / 0.8820 / −33.72%; RULES v2 @10bps OOS 9.53%/1.285 (u56), 7.98%/1.119 (broad),
3.84%/0.566 (small). **Every chooser lands below the arm it started from, and the do-nothing arm
is the only one that beats SPY's OOS Sharpe by more than 0.10.**

| scope | rung | n | 4a vs v2 | 4b full | 4b OOS | BOTH |
|---|---|---|---|---|---|---|
| corpus-C arms | 0 / 10 / 25 bps | 72 | 2 / 2 / 2 | 7 / 7 / 3 | 7 / 7 / 5 | **0 / 0 / 0** |
| walk-forward picks | 0 / 10 / 25 bps | 168 | 1 / 2 / 2 | 18 / 18 / 11 | 18 / 18 / 14 | **0 / 0 / 0** |

17 of 216 arm-rows clear 4b full *and* OOS; **all 17 are MOMLOOK top-20 books on u56/broad**, i.e.
restatements of the record's standing top-20 pass (idea 423's book form), and the signal-window
scale k is flat across them — 4b does not discriminate the dial. The 6 4a passes are all
small-panel (BAND b=0.05, MALEN L=250) and fail 4b on CAGR by a wide margin (4.1%/0.617 vs SPY
14.1%/0.862). **0 of 216 arms and 0 of 504 picks clear both paths at any rung.** 4b binding bar
over the arm-rows: full CAGR 109, H2 57, H1 28, DD 22; OOS CAGR 105, H2 85, DD 24, H1 2.

## Prediction scorecard (pre-registered)
- **P1** K_MEDIAN's lift < +0.0205 and |t| ≤ 2 — **REJECTED**: +0.0232, t +2.20. The premise
  replicates; the effect is if anything slightly larger on the disjoint corpus.
- **P2** K_DIALMID indistinguishable AND agrees > 50% — **REJECTED as a conjunction, and the split
  is the finding**: the paired difference is not significant (−0.0138, t −0.96), which is the half
  that matters, while the agreement half fails because K_DIALMID picks a *different* arm 86.1% of
  the time and still scores **higher** (+0.0371 vs +0.0232). Stronger than predicted, not weaker.
- **P3** no q and no m beats do-nothing OOS — **CONFIRMED**, 0 of 13 grid points.
- **P4** K_MARGIN monotone to 0 in m, no interior optimum — **CONFIRMED**
  (−0.0512, −0.0084, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000).
- **P5** q=0.00 reliably negative (power check) — **CONFIRMED**: −0.0688, t −4.78.

## What the record should take from this (proposal only; no clause changed here)
A selector claim quoting `lift` is quoting `d_vs_ctl + CONTROL_LIFT`, and only the first term is
the selector's. Idea 204 proposed publishing `lift`; this run says publish **`d_vs_ctl` and
`CONTROL_LIFT` separately**, because their sum is exactly the statistic that made a rule which
loses to do-nothing look "reliably positive". K_MEDIAN should not enter PROTOCOL as an abstention
rule, and idea 241's minimum-margin rule should be recorded as **inapplicable to dial pools**: its
threshold has no operating range where the top-2 IS gap never exceeds 0.08.

## Caveats carried
SURVIVORSHIP (idea 54) on all three panels: current constituents only, every CAGR flattered. Every
statistic quoted is a paired within-pool contrast, which the level bias cannot move. 36 cells is
36 cells and arms overlap heavily inside a panel — per-panel, per-family and per-rung breakdowns
are printed above and in the CSVs rather than hidden behind the t-statistics; this run claims the
same clustering idea 204 had, on disjoint dials, which is what a replication needs and no more.
The K_DIALMID/control confound (75%) is disclosed above and is why the CONTROL_LIFT decomposition,
not the POSITION one, carries the conclusion. t+1 execution; PROTOCOL's rung is 10 bps with 0 and
25 reported alongside.

Files: `.console.txt`, `.grid.csv` (216 arm-rows), `.picks.csv` (504), `.selectors.csv`,
`.decomp.csv`, `.keeppaths.csv`, `.premise204.csv` (144).
