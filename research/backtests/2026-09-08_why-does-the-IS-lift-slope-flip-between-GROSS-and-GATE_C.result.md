# idea 432 — why-does-the-IS-lift-slope-flip-between-GROSS-and-GATE (lane C, 2026-09-08)

**Verdict: ANSWERED / SPLIT — the queue's PREMISE is CONFIRMED and its proposed INSTRUMENT is
KILLED. The flip is a real family fact; the regression the queue proposes to explain it returns
nothing; the identified form of the same question returns a strong answer with the sign the queue
did not predict; and the GROSS slope that started this is 193x too small to matter.**
No KEEP-candidate (both paths 0 in every scope), no memo, no RULES change.

Script `2026-09-08_why-does-the-IS-lift-slope-flip-between-GROSS-and-GATE_C.py`; corpus 3 panels x
7 dial families x 3 cost rungs = 63 pools, 41 arms/panel, 369 arm-rows, 504 pick-rows.
2 tuned params: `tau` (11 points) x `stat` (sd | span). All 22 grid points reported.

## G0 — the number, reproduced before it is explained
From idea 204's own committed `.walkforward.csv` (324 rows, 36 cells, 9 selectors), OLS(OOS_lift ~
IS_lift) per family excluding K_ANTI:

| family | n | slope | t | R2 |
|---|---|---|---|---|
| GROSS | 72 | **−0.5803** | −12.63 | 0.6951 |
| WIDTH | 72 | −0.5637 | −3.04 | 0.1166 |
| CADENCE | 72 | +0.5682 | +4.17 | 0.1991 |
| GATE | 72 | **+0.9836** | +10.75 | 0.6226 |

Queue quotes −0.580 / +0.984; reproduced to 0.0003 / 0.0004. **G0 PASS.** Note the framing
correction that falls out immediately: this is not a GROSS-vs-GATE binary — **WIDTH is negative
too**, so the record has two negative and two positive families, and the queue's title names one
of each.

Gates: G1 fast_backtest vs `engine.backtest` returns ≤1.04e-17 / turnover ≤1.80e-16 on all three
panels; G5 rung identity 0.000e+00; G2 the decomposition `slope = rho * sd(O)/sd(I)` closes at
1.776e-15 over 63 cells.

## The flip is real (Q3)
Cluster bootstrap over each family's own 9 (panel, rung) cells, 2,000 draws, seed 4321:

| family | point | boot mean | boot sd | 95% CI | P(slope>0) |
|---|---|---|---|---|---|
| GROSS | −0.5803 | −0.5986 | 0.1237 | [−0.8954, −0.3963] | 0.000 |
| WIDTH | −0.5637 | −0.5534 | 0.3963 | [−1.2302, +0.2638] | 0.090 |
| CADENCE | +0.5682 | +0.6748 | 0.3606 | [+0.4031, +2.1183] | 1.000 |
| GATE | +0.9836 | +0.9142 | 0.2684 | [+0.0959, +1.2219] | 0.982 |
| MALEN | +0.4391 | +0.3997 | 0.1496 | [−0.0051, +0.5892] | 0.972 |
| VOLCAP | +1.7650 | +1.7777 | 0.3489 | [+1.2275, +2.5233] | 1.000 |
| LOOKBACK | +0.2985 | +0.2920 | 0.0675 | [+0.1361, +0.4015] | 1.000 |

GROSS − GATE = −1.5639 (boot mean −1.5128, 95% CI [−1.961, −0.665], **P(diff<0) = 1.000**).
Spread of the 7 family slopes 0.8299 vs mean bootstrap se 0.2450 → **ratio 3.39**. The queue's
"family fact, not record fact" is **CONFIRMED**.

## The asked regression returns nothing (Q1)
Per-family slope regressed on the family's own IS-Sharpe dispersion, exactly as asked:

| unit | y ~ x | n | b | t | R2 |
|---|---|---|---|---|---|
| family (idea 204's unit, 7 families) | slope ~ sd | 7 | +3.4156 | +0.490 | 0.0458 |
| family | slope ~ span | 7 | +1.3754 | +0.533 | 0.0537 |
| cell, ARMS | slope ~ sd | 63 | +1.8212 | +0.682 | 0.0076 |
| cell, PICKS | slope ~ sd | 63 | +3.9825 | +1.236 | 0.0244 |
| cell, CORE only | ARM slope ~ sd | 36 | +6.6812 | +1.104 | 0.0346 |
| cell, EXT only | ARM slope ~ sd | 27 | **−4.2163** | −1.283 | 0.0618 |
| cell, excl. CADENCE | ARM slope ~ sd | 54 | +4.9023 | +2.100 | 0.0782 |

The hypothesis predicts a reliably **negative** coefficient (low dispersion → noise → negative
slope). What comes back is **positive, insignificant, and sign-unstable between the CORE and EXT
halves of the same corpus**. **P1 CONFIRMED (no reliable signed relation).**

## Why: the queue regressed a ratio on its own denominator (Q2)
`slope = rho * sd(OOS lift) / sd(IS lift)` and `disp = sd(IS lift)`. The scale-free leg answers
the queue's question cleanly:

| scope | y ~ disp_sd | n | b | intercept | t | R2 |
|---|---|---|---|---|---|---|
| ALL | ARM rho | 63 | **+5.5815** | −0.2095 | **+4.518** | **0.2507** |
| CORE | ARM rho | 36 | +12.0574 | −0.6326 | +4.490 | 0.3722 |
| EXT | ARM rho | 27 | +0.9300 | +0.4591 | +0.761 | 0.0226 |

and it is monotone in terciles of pool dispersion:

| tercile | n | disp_sd | mean ARM rho | t | cells rho>0 | sign p |
|---|---|---|---|---|---|---|
| low | 21 | 0.0003–0.0495 | −0.1245 | −0.70 | 9/21 | 0.664 |
| mid | 21 | 0.0526–0.0912 | +0.2227 | +1.71 | 14/21 | 0.189 |
| high | 21 | 0.0913–0.2666 | **+0.6336** | **+8.11** | 20/21 | 0.0000 |

**So dispersion governs HOW MUCH IS lift ranks out of sample, not WHICH SIGN it ranks with.**
`|t|` on rho is 4.518 against 0.682 on slope, R2 0.2507 against 0.0076 — **P3 REJECTED**, the
scale-free form is 6.6x the t and 33x the R2 of the form the queue proposed.

The obvious alternative explanation is also **killed**: this is not a divide-by-small-number.
`|ARM slope| ~ 1/disp` gives t +0.976 and `se(ARM slope) ~ 1/disp` gives t **−1.585** (se *falls*
as dispersion shrinks). **P2 REJECTED.** GROSS's slope is not a noisy ratio: its mean within-cell
rho is **−0.9586** and **0 of 9 cells** have a positive slope (sign p 0.0039). On a Sharpe-invariant
dial the IS-best arm is *reliably* the OOS-worst — near-deterministic anti-persistence, not noise
being extrapolated. (The low-dispersion tercile as a whole is still indistinguishable from zero,
t −0.70; the negativity in it is GROSS's.)

## The number that ends the question: scale (Q2d)

| family | sd(IS lift) | sd(OOS lift) | mean abs OOS lift | slope | rho |
|---|---|---|---|---|---|
| GROSS | 0.0016 | **0.0011** | **0.0010** | −0.5803 | −0.8337 |
| WIDTH | 0.0694 | 0.1146 | 0.1054 | −0.5637 | −0.3414 |
| CADENCE | 0.0590 | 0.0751 | 0.0653 | +0.5682 | +0.4462 |
| GATE | 0.0921 | 0.1149 | 0.0855 | +0.9836 | +0.7890 |
| MALEN | 0.0935 | 0.0695 | 0.0600 | +0.4391 | +0.5907 |
| VOLCAP | 0.0881 | **0.2143** | 0.1675 | +1.7650 | +0.7252 |
| LOOKBACK | 0.1651 | 0.0831 | 0.0583 | +0.2985 | +0.5930 |

Largest / smallest family sd(OOS lift) = **193.3x**. Pooled over all 504 pick rows the "record
fact" slope is **+0.5053** (t +10.79); **deleting GROSS's 72 rows entirely moves it to +0.5147, a
change of +0.0093**, because OLS weights by x-variance and GROSS's IS-lift variance is ~0.
**The −0.580 is loud and weightless.** Idea 408's rule for margins applies verbatim to slopes: a
slope quoted without `sd(OOS lift)` beside it is uninterpretable.

## Idea 311's premise, measured not cited (Q4)
GROSS IS-Sharpe span over its 9 cells: **0.0009 … 0.0049, mean 0.0032 — ≤ 0.006 in 9 of 9 cells.**
GROSS ranks **1 of 7** families by span; the next-narrowest (CADENCE, 0.1241) is **39x wider**.
**P4 CONFIRMED**, at the quoted level as well as in sign.

## Rule 8 — and the instrument the answer implies (Q5)
Pre-registered rule R(tau, stat): in a pool whose IS dispersion exceeds `tau`, take the K_Sharpe
argmax pick; otherwise take the pool's own do-nothing control. `tau` chosen on an **inner IS split**
(fit ≤2013-12-31, evaluated 2014–2016); outer OOS 2017–2026 read **once**. All 22 grid points in
`.walkforward.csv`.

Inner split picks **tau\* = 0.0000 on `sd`** (mean inner lift +0.0565, t +3.43, picks in 63/63
pools) — the in-sample evidence says *never abstain*. Read once:

| rule | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | d vs control | t | wins | sign p |
|---|---|---|---|---|---|---|---|
| **R(tau\*)** = always-pick | 0.9410 | 10.63% | −19.37% | **−0.0206** | −1.43 | 22/59 | 0.067 |
| best grid point (sd > 0.0835) | 0.9700 | 9.19% | −16.95% | +0.0084 | +0.90 | 14/25 | 0.690 |
| always-abstain (do-nothing) | **0.9616** | 8.04% | −14.30% | 0.0000 | — | — | — |

**P5 CONFIRMED**: gating the chooser by dispersion does not rescue it. Even the best-of-22 grid
point is +0.0084 at t +0.90 — inside noise, and it was not the point the inner split chose. This is
the 4th independent reproduction in the record (ideas 151, 204, 430) of *no chooser beats
do-nothing*, now with the "but only where the dial actually moves Sharpe" escape hatch closed.

OOS benchmarks (2017–2026, 10 bps): SPY 15.45% / 0.8820 / −33.72%; RULES v2 u56 9.53% / 1.2851 /
−12.05%, broad 7.98% / 1.1185 / −12.24%, small 3.84% / 0.5665 / −14.70%.

## KEEP paths (Q6, PROTOCOL 4a and 4b)
| scope | n | 4a (v2) | 4b full | 4b OOS | **BOTH** |
|---|---|---|---|---|---|
| arms, all rungs | 369 | 3 | 38 | 41 | **0** |
| arms, 10 bps | 123 | 1 | 14 | 14 | **0** |
| arms, CORE | 207 | 3 | 18 | 20 | **0** |
| arms, EXT | 162 | 0 | 20 | 21 | **0** |
| R(tau\*) selected books | 63 | 0 | 13 | 12 | **0** |
| R(tau\*), 10 bps only | 21 | 0 | 5 | 4 | **0** |

Binding 4b bar on the 10-bps arms that fail: CAGR 51, H2 25, H1 23, DD 10. **No book promoted.**

## Pre-registered predictions, scored
P1 CONFIRMED · P2 **REJECTED** · P3 **REJECTED** · P4 CONFIRMED · P5 CONFIRMED. Two of five wrong,
and both wrong in the direction that makes the GROSS slope *more* real rather than less: it is
neither a sampling artefact (P2) nor noise (the −0.96 rho), it is simply nil in size.

## Recommendation to the record (report-only, no RULES change)
1. Any published `slope(OOS lift ~ IS lift)` must carry **`sd(OOS lift)`** beside it. Without the
   scale, a slope comparison across families is uninterpretable — this run's whole result.
2. When comparing families, quote **rho, not slope**. Slope carries the comparand family's own
   IS dispersion in its denominator; rho is bounded, scale-free, and 33x the R2 here.
3. Do **not** adopt a dispersion-gated selector. It fails rule 8 (P5) at the threshold its own
   in-sample evidence chooses.

## Caveats
SURVIVORSHIP (idea 54): all three panels are current constituents; every CAGR is flattered and no
level is achievable. All statistics are within-pool or paired contrasts, which the level bias does
not move. 63 pools are not 63 independent observations — arms and panels overlap heavily; the
bootstrap resamples cells, not rows, and every t is quoted with its n. CADENCE has only 4 arms and
its cells are flagged; the regressions are re-run without it (the excl.-CADENCE row is the only
cell-level slope-on-dispersion result that clears |t| = 2, at +2.100, and it is positive — the
opposite of the queue's hypothesis). Idea 401's restatement: `data/prices.csv` was rewritten after
some committed grids, so G0 is quoted per number rather than asserted bit-exact. PROTOCOL rung is
10 bps; 0 and 25 reported. Every book is t+1 execution (idea 126).
