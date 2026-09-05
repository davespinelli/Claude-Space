# Idea 162 — where-does-the-POS-tilt-stop-transferring (lane C, 2026-09-05)

**ANSWERED, and the answer kills the clause it was meant to write. The vol premium's sign
flip is BRACKETED (between `broad78` and the most liquid sub-$2B quintile) but it is not a
BOUNDARY: four consecutive rungs of the ladder sit inside a statistical dead zone, the
premium is NOT monotone in size at the top (`mega20` +0.00220 < `broad98` +0.00251, P2
FAILED), and a selector that trades on the sign LOSES out-of-sample to plain IS-Sharpe and
to doing nothing at all (P7 HELD). There is no cut point PROTOCOL can honestly state.**

Script `2026-09-05_where-does-the-POS-tilt-stop-transferring_C.py`; outputs `.console.txt`,
`.grid.csv`, `.premium.csv`, `.adv.csv`, `.walkforward.csv`, `.signmatch.csv`.

## The one thing this run could not do, stated first

**There is no market-capitalisation series in this repo** — no shares outstanding anywhere in
`data/`. So "the market-cap boundary" the idea asks for cannot be quoted in dollars, and any
such number would have been fabricated. Two orderings the committed data *does* support were
used and labelled: **(A)** an ordinal MEMBERSHIP ladder from the universe files
(`mega20` > `broad98` > `broad78` > sub-$2B) and **(B)** a MEASURED liquidity ladder inside the
small panel — median daily dollar volume, the only continuous size-like variable the repo
holds (median **$3.44M/day**, 10th pct $0.30M, 90th pct $19.9M).

## Reproduction, before any new number was read

| check | target | this run |
|---|---|---|
| [a] `INV / n=5 / w=0.15` vs `baseline.rules_v1_weights`, u56 and broad | 0 | **0.000e+00 (EXACT)** |
| [b] idea 80's `fama_macbeth`, imported verbatim, on idea 81's three panels | u56 +0.00450 (t +3.90) / broad +0.00294 (t +3.19) / small −0.00084 (t −0.95); IC −0.0428 / −0.0332 / +0.0195 | **all six MATCH to the published digit** |
| [c] new panels are exact subsets of their parents, ETF-free / mega-free as claimed | — | **True**; the 5 ADV quintiles partition all 439 small-panel names, 0 dropped |

## (1) THE ANSWER: the flip is bracketed, and the bracket is a dead zone

Bivariate weekly Fama-MacBeth slope of next-week return on the vol20 percentile rank among
eligible names, **COMMON window (2011-01-13 →)** so the ladder is not a sample artefact:

| rung (ladder A, largest first) | names | slope | t | low-vol IC (t) | reading |
|---|---|---|---|---|---|
| u56 (anchor, 36 ETFs) | 56 | **+0.00455** | **+3.81** | −0.0458 (−4.10) | high vol pays, significant |
| mega20 | 20 | +0.00220 | +1.29 | −0.0122 (−0.94) | **out of order — P2 fails here** |
| broad98 (broad minus ETFs) | 100 | **+0.00251** | **+2.45** | −0.0216 (−2.28) | last SIGNIFICANT positive rung |
| broad78 (large, not mega) | 80 | +0.00157 | +1.59 | −0.0175 (−1.83) | dead zone |
| smADV5 (most liquid sub-$2B) | 88 | **−0.00025** | −0.17 | +0.0059 (+0.68) | **sign flips here**, dead zone |
| smADV4 | 88 | −0.00124 | −0.76 | +0.0087 (+1.05) | dead zone |
| smADV3 | 87 | −0.00213 | −1.38 | +0.0265 (+3.16) | negative, IC significant |
| smADV2 | 88 | −0.00157 | −0.96 | +0.0298 (+3.54) | negative, IC significant |
| smADV1 (least liquid) | 88 | −0.00189 | −1.29 | +0.0282 (+3.78) | negative, IC significant |

* **Where it flips:** between `broad78` (+0.00157) and `smADV5` (−0.00025) — i.e. at the
  boundary of the sub-$2B screen itself, not inside it.
* **Why that is not a boundary you can trade:** the last rung with t ≥ +2 is `broad98`
  (+2.45) and, in slope space, no quintile of the small panel reaches t ≤ −2 (best −1.38);
  the first significantly-negative cohort is the **2nd ADV decile** (−0.00496, t −2.53). Four
  consecutive rungs — `broad78`, `smADV5`, `smADV4`, `smADV2` — are indistinguishable from
  zero. The sign flip happens *inside a region where the sign carries no information.*
* **P3 HELD (the flip is at/above the sub-$2B ceiling):** **0 of 10** ADV deciles of the small
  panel has a significantly positive slope; **1 of 10** is even positive-signed, and it is the
  TOP decile (`smDEC10`, +0.00253, t +1.09, the ≥$20M/day names). The premium does not turn
  positive again anywhere inside the panel; it just runs out of significance at its ceiling.
* **P5 HELD:** u56 +0.00455 (t +3.81) and broad +0.00275 (t +2.95) on the common window, so
  the large-cap premium is not a sample-window artefact of the longer price history.

## (2) P2 FAILED — the premium is not monotone in size, and `mega20` is why

`mega20` +0.00220 sits BELOW `broad98` +0.00251 (5 of 7 ladder pairs in order, not 7). Size is
therefore not the axis at the top of the ladder. The mechanism is idea 81's, sharpened:
**at n=20 on a 20-name panel the scaler cannot change the book at all** — `mega20`'s INV, NONE
and POS arms at n=20 are numerically IDENTICAL (12.05% / 1.337 / −12.1% in all three). A
cross-sectional tilt pays only where the book is a small slice of the cross-section, and
`mega20` is the degenerate end of that: the slice is the whole panel.

## (3) P4 HELD, 8 of 11 panels (35 of 44 cells, 79.5%) — and the misses are the dead zone

Idea 81's "winning tilt sign matches the panel's own premium sign" survives the widening from
3 panels to 11. The two clean misses are exactly the cells where it should miss:
**`smADV5` 0 of 4** — the panel the sign flips ON, where the slope is −0.00025 (t −0.17) and
NONE wins — and **`mega20` 2 of 4**, the degenerate cell above. `smADV3` splits 2/2.

## (4) Both KEEP paths at every one of the 132 grid points

**4a 24 of 132** (all on broad/broad98/broad78/mega20, 6 each). **4b 10 of 132.**
**4b on the OOS window alone 13 of 132.** **P6 HELD: 0 of 12 arms pass 4b on every equity
panel** — cross-universe 4b is still zero, for the ninth time.

Every 4b pass, and **none of them is proposed** (reasons below):

| panel | arm | cost | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | 4a |
|---|---|---|---|---|---|---|---|---|
| mega20 | INV n=20 ≡ NONE ≡ POS | 10 | 12.05% | **1.337** | −12.1% | 1.341 / 1.341 | **1.446** | yes |
| mega20 | INV n=20 ≡ NONE ≡ POS | 25 | 11.46% | 1.277 | −12.2% | 1.278 / 1.284 | 1.390 | yes |
| mega20 | INV n=5 | 10 | 18.00% | 1.121 | −19.4% | 1.095 / 1.150 | 1.166 | no (it *is* RULES v1 here) |
| mega20 | NONE n=5 | 10 | 18.51% | 1.049 | −18.4% | 0.974 / 1.118 | 1.085 | no |
| u56 | NONE n=20 | 10 | 12.66% | 1.092 | −18.3% | 1.088 / 1.102 | 1.168 | no |
| u56 | POS n=20 | 10 | 13.15% | 1.082 | −19.0% | 1.010 / 1.150 | 1.198 | no |

SPY on this sample: 15.23% / 0.889 / −33.72%, halves 0.957 / 0.834, OOS 15.45% / 0.882 / −33.72%.

**Why the mega20 rows are recorded and NOT proposed** (three independent reasons, any one
sufficient): (i) `universe.json['megacap']` is the list of the 20 largest US companies **as of
2026** — backtesting it from 2009 is close to pure look-ahead selection, a far worse bias than
the small panel's, and `RULES v1` itself scores 18.00% / 1.121 / −19.36% on it, which is what
that bias looks like; (ii) the n=20 book is **scaler-degenerate** (all three arms identical)
and runs at mean gross **0.492**, not 0.75 — per ideas 144/152 its −12.1% drawdown is bought
by de-grossing, not by signal; (iii) it does not transfer (P6).

## (5) PROTOCOL rule 8 — the capital-relevant KILL

Parameters chosen on the IS window only, read once on 2017-01-01→. 22 panel × cost cells:

| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | beats RULES v1 | beats SPY |
|---|---|---|---|---|---|
| S1 plain IS-Sharpe argmax | **0.5914** | 7.51% | −32.4% | 12/22 | 6/22 |
| **S2 SIGN selector (idea 162's rule)** | **0.5818** | 8.14% | −33.1% | 10/22 | 7/22 |
| S3 do-nothing INV/n=5 (the live tilt) | **0.3982** | 5.17% | −34.1% | 0/22 | 3/22 |
| S4 do-nothing NONE/n=20 | 0.5827 | 6.88% | **−29.8%** | **14/22** | 8/22 |

**P7 HELD: the sign selector does not beat plain IS-Sharpe — mean ΔOOS Sharpe −0.0096, wins
3 of 22.** It does not beat *doing nothing* either (S4, 0.5827, with 2.6pp less drawdown). So
even where the boundary is real (the two ends of the ladder), knowing which side you are on
is worth **less than nothing** out of sample. Every selector loses to SPY's OOS Sharpe of
**0.882**. The live tilt S3 is last by 0.18–0.19 of Sharpe — a **fourth** independent
confirmation that `/sqrt(vol20)` should be deleted rather than inverted (ideas 2/80/81/160).

## Prediction scorecard — 5 of 7

| | prediction | outcome |
|---|---|---|
| P1 | reproduction [a] [b] [c] | **HELD** (all exact) |
| P2 | slope monotone down the membership ladder | **FAILED** — mega20 out of order, 5/7 pairs |
| P3 | flip at/above the sub-$2B ceiling | **HELD** — 0 of 10 deciles significantly positive |
| P4 | sign match ≥ 6 of 11 panels | **HELD** — 8 of 11, 35 of 44 cells |
| P5 | large-cap premia survive the common window | **HELD** |
| P6 | cross-universe 4b stays 0 | **HELD** — 0 of 12 arms |
| P7 | sign selector does not beat IS-Sharpe | **HELD** — −0.0096, wins 3/22 |

## What PROTOCOL should take from this (and what it should not)

**Not** a cap threshold — none is derivable here, and even the ordinal bracket sits in a dead
zone. What is supportable is a **two-regime statement with an explicit no-man's-land**: the
vol premium is significantly positive only on the ETF-bearing and large-cap-equity panels
(u56, broad, broad98), significantly *low-vol-paying* only in IC space on the bottom ADV
deciles of the sub-$2B panel, and indistinguishable from zero on everything between
`broad78` and `smADV4`. Any universe clause written from it must name the two ends and admit
the middle, and — per rule 8 above — must not be traded on, because acting on the sign costs
0.01 of OOS Sharpe against doing nothing.

## Caveats carried

No market-cap data (above). ADV is a liquidity proxy and adjusted-close × raw share volume
misstates dollar volume across splits — used only to ORDER names, never as a level.
Survivorship on all four panel families (idea 54), worst on `mega20` (see §4) and on the small
panel (its 44 max_1d_move ≥ 1.0 names dropped). The new equity panels hold no ETFs, so no
cash-like sleeve, and their drawdowns are not comparable with u56/broad. SPY benchmarks the
small panels (no IWM cached). Ideas 49/39 (the gate is inverted on small), 128 (the IS window's
SPY drawdown is shallower), 144 (a de-grossed book is the same book), 38 and 126 carry over.
