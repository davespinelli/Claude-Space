# Idea 571 — is-tpers-INFORMATION-or-TAUTOLOGY (lane B, 2026-09-11)

**Script:** `2026-09-11_is-tpers-INFORMATION-or-TAUTOLOGY_B.py`
**Verdict: KILL for capital. The R2 SURVIVES off-gate (so tpers is not an identity), but the
PANEL-ORDERING claim does not: the two persistence variables that are genuinely independent of
tpers order the three real panels BACKWARDS.**

## The question

Idea 569 found `tpers` (1 − daily flip rate of the name's own above-200d-MA state) is the first
characteristic to order the MA-gate selection premium monotonically: POOL slope +33.381187,
R2 0.847210, slope·span +0.707607 = 7.24x the published GAP, sign strengthening IS→OOS. But
tpers is the gate's own state variable, so "the gate pays where its state is persistent" may be
an identity. The queue asked: re-run the same kernel-draw ranking on the persistence of a
DIFFERENT signal (12-1 momentum rank persistence) and report whether the R2 survives.

Four persistence variables on idea 569's machinery (k=36 kernel draws, h=0.5·sd, 6 seeds,
pre-registered 10/30/50/70/90th-percentile rungs, gross {0.50,0.75,1.00} × cadence {W,M}
reported and averaged, 10 bps, t+1 fills):

| variable | what it is | gate's own? |
|---|---|---|
| `tpers` | 1 − flip rate of `px > 200d MA` | **YES** (REFERENCE) |
| `mompers` | 1 − flip rate of `rank_pct(12-1 mom) > 0.5` (the queue's variable) | no |
| `momsgn` | 1 − flip rate of `12-1 mom > 0` (name-local twin of tpers) | no |
| `momac` | lag-21 autocorrelation of `rank_pct(12-1 mom)` (continuous form) | no |

Tuned parameters: exactly two — the SIGNAL and the LEVEL. 324 draws × 2 arms × 3 gross ×
2 cadence = **3,888 books, every grid point in `.grid.csv`**.

## Gates

- **G1 PASS** — idea 569's committed tpers ladder reproduces **bit-for-bit**: 13/13 rungs,
  max |Δ| over (achieved, premium, sd, slope, R2, span, effect) = **1.11e-16**; POOL slope
  +33.381187, R2 0.847210, effect +0.707607 all to <1e-6 of the pre-registered values. (The
  per-name frame is built with idea 569's five original characteristics and `dropna()`'d exactly
  as it was, so the 573-name pool, the rung levels and the seeds are identical.)
- **G2 PASS** — `fast_backtest` == `engine.backtest`, max |Δreturn| 1.39e-17.
- **G3 PASS** — idea 569's committed tpers matched-level B−S origin gaps reproduce, 3/3,
  max |Δ| 8.33e-17.

## Result 1 — the R2 SURVIVES off-gate. tpers is NOT an identity.

POOL fits (premium vs the draw's achieved characteristic):

| char | slope | R2 | R2 / tpers | slope·span | /GAP | monotone | signOK |
|---|---|---|---|---|---|---|---|
| tpers (gate) | +33.3812 | **0.8472** | 1.000 | +0.7076 | 7.24 | up | True |
| mompers | +28.1431 | **0.7105** | 0.839 | +0.5406 | 5.53 | up | **False** |
| momsgn | +36.2251 | **0.7943** | 0.938 | +0.5934 | 6.07 | up | True |
| momac | +6.0707 | **0.7765** | 0.917 | +0.5958 | 6.09 | up | **False** |

Every non-gate persistence variable reproduces 0.84–0.94x of tpers's R2, clears the effect bar
(≥0.5·GAP) by 5–6x, is monotone up on POOL, and holds its slope sign IS→OOS in **12/12**
(char, flavour) cells. The premium rising with persistence is therefore a property of
**persistence in general**, not of the gate reading its own state. `H_TAUT` **FAILS**.
tpers does not even have the highest POOL R2 out of sample (OOS: momsgn 0.773, tpers 0.758,
momac 0.612, mompers 0.517).

## Result 2 — but the PANEL-ORDERING claim does not survive. This is the real finding.

The required slope sign is fixed in advance by the three real panels' own values of each
characteristic, so that a monotone fit would reproduce the published U56 > B136 > SMALL439
premium ordering (+0.0045 / −0.0465 / −0.1023, gap re-read +0.0978 = the published GAP):

| char | U56 | B136 | SMALL439 | required sign | measured POOL slope | agrees? |
|---|---|---|---|---|---|---|
| tpers | 0.9689 | 0.9682 | 0.9640 | **+1** | +33.38 | yes |
| mompers | 0.9691 | 0.9695 | **0.9696** | **−1** | +28.14 | **NO** |
| momsgn | 0.9758 | 0.9751 | 0.9703 | **+1** | +36.23 | yes |
| momac | 0.8481 | 0.8654 | **0.8666** | **−1** | +6.07 | **NO** |

All four panel orderings are monotone, but on `mompers` and `momac` the panel with the HIGHEST
premium (U56) has the LOWEST momentum-persistence, so the ladder's own direction predicts the
panel ordering backwards. And the one non-gate variable whose panel ordering does agree
(`momsgn`) is a near-copy of tpers: cross-name Spearman **+0.5208** (bar for independence
|ρ|<0.50 — it fails). The two variables that ARE independent of tpers (mompers ρ +0.3776,
momac ρ +0.3234) are exactly the two with the wrong sign.

**So: persistence orders the premium across kernel draws (robustly, off-gate, OOS), but
persistence does NOT explain why U56 > B136 > SMALL439.** Idea 569's H_PRED failure was not a
detail — the monotone ladder and the published panel gap are two different facts, and only the
gate's own variable (plus its near-copy) makes them look like one.

## Result 3 — H_CARRIER still fails for everything, but momac is the closest yet

| char | rungs inside seed sd | mean B−S | mean \|B−S\| | mean match resid |
|---|---|---|---|---|
| tpers | 0/3 | +0.1204 (0.61x idea 568) | 0.1204 | 0.0017 |
| mompers | 0/3 | +0.1012 (0.52x) | 0.1012 | 0.0014 |
| momsgn | 2/4 | +0.0393 (0.20x) | **0.1375** | 0.0012 |
| momac | 3/4 | +0.0426 (0.22x) | **0.0549** | 0.0152 |

No variable passes H_CARRIER (every one needs ALL rungs inside the floor). momsgn's small mean
is **cancellation** — its rungs run +0.2478, +0.1057, −0.0542, −0.1421, so mean |B−S| is 0.1375,
larger than tpers's. Only `momac` has a genuinely small matched-level origin gap
(mean |B−S| **0.0549 = 0.28x idea 568**, the smallest on this machinery to date; idea 569's best
was mrho +0.0801 = 0.41x) — but its match residual is 10x the others' (0.0152 on a 0.098 span),
so its rungs are the most loosely matched and the small gap is partly a matching artefact. That
is a lead for a follow-up, not a result.

## RULE 8 walk-forward (required) — and the KEEP paths

WF-A: slopes refit inside 2010-2016 and 2017-2026, read once. Sign holds **12/12** (char,
flavour) cells. POOL R2 IS → OOS: tpers 0.518→0.758, mompers 0.667→0.517, momsgn 0.427→0.773,
momac 0.635→0.612.

WF-B: (char, level) picked by **IS Sharpe alone** at g=0.75/W POOL, OOS read once. Pick
`tpers L=0.9780` (IS +0.9447) — which this time **was** the OOS winner (+1.0517); selection did
not lose, unlike idea 569's run.

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|
| WF-B pick (seed-pooled) | 14.53% | 1.134 | −23.56% | 1.260 / 1.058 | 16.51% | 1.194 | −23.56% |
| RULES v2 (B136) baseline | 7.62% | 1.082 | −12.24% | 1.126 / 1.040 | 7.98% | 1.119 | −12.24% |
| SPY | 14.13% | 0.862 | −33.72% | 0.891 / 0.858 | 15.45% | 0.882 | −33.72% |

- **4a FALSE** — the WF-B book out-Sharpes RULES v2 in both halves (1.260>1.126, 1.058>1.040)
  but its MaxDD is −23.56% against the baseline's −12.24%, so the MaxDD leg binds.
- **4b FAILS on DD only** — H1, H2, OOS and CAGR all clear SPY; MaxDD −23.56% vs the cap
  0.60 × −33.72% = **−20.23%**. It misses the drawdown cap by 3.3pp and nothing else.
- Over all 3,888 books: **4a 28, 4b 49, BOTH 0**. Binding 4b legs: DD 3404, H2 2841, OOS 2788,
  H1 2485, CAGR 2166. 4b passers by char: momsgn 19, momac 19, tpers 6, mompers 5 — another
  sign the effect is not the gate's variable's property.

No KEEP candidate, so no RULES wording is proposed.

## Caveats

Survivorship: B136 and the small panel are CURRENT constituents; every number is a statement
about surviving names, not a tradable 2010 universe. A kernel draw is not a tradable rule — the
4b passers above are diagnostics. `momac` is undefined for 2 names (AEBI, OMDA) and they are
excluded from its rungs only, so its pool is 571 vs 573. 2010-01-04..2026-09-04, one common
index; only 2020 and 2022 are real stress tests in it.
