# Idea 207 — how-many-draws-does-clause-11b-need (cloud, 2026-09-05)

**ANSWERED, and the queue's premise is half wrong. For clause 11b's statistic AS WRITTEN
(band = max |dSharpe| over K rotations) there is NO number: K does not set the band's
precision, it sets the test's SIZE. Replace the max with a fixed quantile and the number
exists and is 100. No RULES change, no new book, no KEEP candidate.**

Script `2026-09-05_how-many-draws-does-clause-11b-need_cloud.py`; artefacts `.console.txt`,
`.band.csv`, `.flip.csv`, `.zone.csv`, `.walkforward.csv`, `.keep.csv`.

## Corpus and reproduction

Idea 191's machinery imported verbatim (panels, base book, overlay families, `apply_overlay`,
the rotation construction, the 4a/4b evaluators). 3 panels (U56, BROAD136, SMALL439 = the
483-name sub-$2B panel less the 44 tickers with `max_1d_move >= 1.0`) × 3 families
(DDCTL/BUDGET/SLEEVE) × 5 thresholds × 2 depths = **90 configurations**, × 2 cost rungs
(10/25 bps, both derived exactly from one 0 bps run) = **180 real rows**, each against a pool
of **400 circular rotations** = **72,000 null evaluations**. 2643 s.

Reproduction asserted before any new number was read: engine equivalence, the cost identity
and the CAND-20 weights on all three panels; RULES v1 on u56 at 6.45305% / 0.66418 /
−13.82780% exactly; and — the point of the run — **idea 201's three published bands reproduce
at 9.7e-17 on all 180 rows and its 3-block flip count reproduces exactly at 32/180 = 17.8%.**
Idea 201 sorted its 60 offsets before blocking; that ordering is reconstructed rather than
assumed. Seeded with `zlib.crc32`, so unlike idea 191 this run is reproducible across
processes (PROTOCOL 5).

## Q1 — the band DRIFTS, so K is not a precision dial

| stat | K | nominal size | mean band | mean margin | clear rate (Sharpe) | clear rate (MaxDD) |
|---|---|---|---|---|---|---|
| MAX | 20 | 1/21 = 4.76% | 0.1686 | −0.0694 | **15.6%** (28/180) | 6.1% |
| MAX | 50 | 1/51 = 1.96% | 0.2100 | −0.1109 | 9.4% (17) | 2.8% |
| MAX | 100 | 1/101 = 0.99% | 0.2465 | −0.1473 | 3.9% (7) | 2.2% |
| MAX | 200 | 1/201 = 0.50% | **0.2797** | −0.1805 | **2.2%** (4) | 1.7% |
| Q95 | 20 | 5% | 0.1374 | −0.0383 | 23.9% (43) | 18.3% |
| Q95 | 50 | 5% | 0.1420 | −0.0429 | 21.1% (38) | 17.2% |
| Q95 | 100 | 5% | 0.1449 | −0.0458 | 22.8% (41) | 17.2% |
| Q95 | 200 | 5% | **0.1466** | −0.0475 | **23.3%** (42) | 16.7% |

The MAX band rises **+65.9%** from K=20 to K=200 and its clear rate falls **15.6% → 2.2%**,
monotonically in both. That is not noise reduction — it is the estimand moving. A one-sided
test whose critical value is the maximum of K draws has nominal size 1/(K+1), so "how many
draws" is the same question as "what size should the test be", and idea 186's K=20 is a 4.8%
test while K=200 is a 0.5% one. The Q95 band moves **+6.7%** and its clear rate is flat.
The K ladder is nested (each K uses pool positions 0:K), so the drift is not a re-draw artefact.

## Q2 — flip rate, and why the MAX band's "stability" at K=200 is degenerate

Disjoint blocks of size K from the 400-draw pool (20 / 8 / 4 / 2 blocks); a configuration
flips when two disjoint blocks disagree on `clears`.

| stat | K | blocks | configs that flip | pairwise disagreement | band sd across blocks | range / band |
|---|---|---|---|---|---|---|
| MAX | 20 | 20 | **31.7%** (57/180) | 10.8% | 0.0502 | **115.3%** |
| MAX | 50 | 8 | 22.8% (41) | 9.4% | 0.0569 | 77.6% |
| MAX | 100 | 4 | 13.3% (24) | 7.6% | 0.0606 | 55.3% |
| MAX | 200 | 2 | 2.8% (5) | 2.8% | 0.0492 | 25.4% |
| Q95 | 20 | 20 | 26.7% (48) | 7.7% | **0.0242** | 68.6% |
| Q95 | 50 | 8 | 15.0% (27) | 5.8% | 0.0153 | 31.2% |
| Q95 | 100 | 4 | **4.4%** (8) | **2.5%** | 0.0115 | 17.6% |
| Q95 | 200 | 2 | 3.3% (6) | 3.3% | **0.0076** | 7.2% |

**The MAX band's absolute sampling sd does not fall with K at all** — 0.0502 → 0.0492 while
the band itself grows 66%. Its flip rate falls only because by K=200 just 4 of 180 rows clear
anything, so there is almost nothing left to disagree about: the test stabilises by ceasing to
fire. **The Q95 band's sd falls 0.0242 → 0.0076, a factor of 3.18 against sqrt(200/20) = 3.16
— textbook 1/sqrt(K)**, which is the property that makes a draw count meaningful in the first
place.

Idea 201's headline reproduces and is if anything understated: measured on 20 disjoint blocks
rather than 3, **31.7% of configurations flip at K=20**, against its 17.8% on 3 blocks.

## Q3 — the undetermined zone

95th percentile of |margin| among flipping configurations, and the share of the corpus inside it:

| stat | K | zone p95 | zone median | corpus inside |
|---|---|---|---|---|
| MAX | 20 | 0.1248 | 0.0269 | 72.8% |
| MAX | 50 | 0.0787 | 0.0186 | 52.8% |
| MAX | 100 | 0.1068 | 0.0141 | 49.4% |
| MAX | 200 | 0.0141 | 0.0095 | 16.1% |
| Q95 | 20 | 0.0921 | 0.0164 | 72.8% |
| Q95 | 50 | 0.0327 | 0.0099 | 41.1% |
| Q95 | 100 | **0.0097** | 0.0027 | **16.1%** |
| Q95 | 200 | 0.0163 | 0.0016 | 25.0% |

Idea 201's rule of thumb — read any `clears` with |margin| < 0.05 as undetermined — is
**correct at K=20 and too loose at both ends elsewhere**: the 95th percentile of flipper
|margin| is 0.0921 (Q95) / 0.1248 (MAX) at K=20 and 0.0097 at Q95 K=100.
The K=200 rows rest on ONE block pair per configuration and are the noisiest estimates in the
table; that is why Q95's zone widens from K=100 to K=200 rather than narrowing, and it is a
property of the estimator, not of the band (whose sd keeps falling).

## Q4 — rule 8: nothing here moves a decision, and the clause still loses to doing nothing

Clause read on the IS window only (≤ 2016-12-31), overlay point chosen there, 2017-01-01 →
read once. 18 cells = 3 panels × 3 families × 2 cost rungs; pool = 10 points per cell.

| selector | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | dOOS | t | W/L | abstains |
|---|---|---|---|---|---|---|---|
| ORACLE-OOS | 0.8197 | 11.04% | −23.16% | +0.0431 | +3.86 | 12/0 | 0 |
| **S0 do-nothing** | **0.7766** | 10.22% | −23.53% | — | — | — | — |
| S2 clause-gated MAX K=200 | 0.7621 | 10.07% | −24.13% | −0.0145 | −1.89 | 0/4 | 14 |
| S2 clause-gated MAX K=50 | 0.7496 | 9.73% | −23.41% | −0.0270 | −2.41 | 0/6 | 12 |
| S2 clause-gated MAX K=20 | 0.7471 | 9.73% | −24.32% | −0.0295 | −2.35 | 0/6 | 12 |
| S2 clause-gated Q95 K=100 | 0.7471 | 9.73% | −24.32% | −0.0295 | −2.35 | 0/6 | 12 |
| S2 clause-gated Q95 K=200 | 0.7418 | 9.39% | −23.68% | −0.0348 | −2.77 | 0/8 | 10 |
| S1 IS-Sharpe argmax (control) | 0.7405 | 9.55% | −25.52% | −0.0361 | −1.68 | 5/9 | 0 |
| S2 clause-gated MAX K=100 | 0.7383 | 9.75% | −23.98% | −0.0383 | −1.50 | 0/5 | 13 |
| S2 clause-gated Q95 K=20 | 0.7125 | 9.12% | −25.46% | −0.0641 | −3.14 | 1/9 | 8 |
| S2 clause-gated Q95 K=50 | 0.7114 | 9.06% | −23.61% | −0.0652 | −2.35 | 0/8 | 10 |

Benchmarks over the same OOS window: **SPY 15.45% / 0.8820 / −33.72%**; RULES v1 @10 bps
7.73% / 0.7471 / −13.83% (u56), 5.94% / 0.5762 / −21.19% (broad), 7.88% / 0.6617 / −32.37%
(small). **Every one of the eight clause-gated selectors loses to the do-nothing control at
every K and both statistics** — the twelfth consecutive instance in this project of an
IS-fitted selector failing to earn its complexity, and the third of this null clause failing as
a gate (after ideas 181, 186 and 192). The best of them (MAX K=200, −0.0145) is best only
because it abstains in 14 of 18 cells.

## Q5 — both KEEP paths

180 real rows: **4a 37/180, 4b 28/180.** By panel and rung: U56 1/19 @10, 6/8 @25;
BROAD136 6/1 @10, 23/0 @25; **SMALL439 0/0 @10 and 1/0 @25 — the twelfth reproduction of
idea 136.** **All 28 of the 4b passes are INSIDE their own 200-draw MAX band**, up from
idea 186's "18 of 18" at K=20: raising the draw count does not rescue a single one.

## Predictions

4 of 6 hit. **P1** (reproduction) HIT — 9.7e-17, 32/180 exactly. **P2** (MAX drifts >20%,
monotone) HIT — +65.9%. **P3** (Q95 stable) HIT — +6.7%. **P6** (no gated selector beats
do-nothing) HIT — best −0.0145.
**P4 MISS**: the MAX flip rate at K=200 is 2.8%, below the predicted 5% — but for the reason
that inverts the prediction's meaning: by K=200 only 4 of 180 rows clear at all, so the test
is nearly empty rather than nearly stable, and the band's absolute sd is unchanged.
**P5 MISS**: the Q95 flip rate is not monotone (2.5% at K=100, 3.3% at K=200) and is not below
MAX at K=200 (3.3% vs 2.8%). Both comparisons at K=200 rest on a single block pair per
configuration; the monotone quantity that does not depend on the block count — the band's
across-block sd — falls exactly as 1/sqrt(K) for Q95 and not at all for MAX.

## The answer to the queue, in the form it asked for

1. **For the band as written (max of K), no draw count is correct**, because K is the test's
   size, not its precision: 4.8% at K=20, 0.5% at K=200, band level +66%, clear rate
   15.6% → 2.2%, absolute sd unchanged.
2. **Fix the statistic first.** With a fixed Q95 band the level is stable (+6.7%) and the
   noise falls as 1/sqrt(K), so a draw count becomes meaningful.
3. **Then the number is 100.** At Q95/K=100 the pairwise flip rate is 2.5% (from 7.7% at
   K=20), the undetermined zone is |margin| < 0.010 (from 0.092), and 16.1% of the corpus
   sits inside it. K=200 doubles the cost for no measured improvement on this corpus.
4. **Publish the band's own sd beside it**, whatever K is chosen: at Q95/K=100 it is 0.0115
   and 17.6% of the band's value.
5. **None of this makes the clause a gate.** It remains report-only: every gated selector
   loses to do-nothing, and all 28 of the corpus's 4b passes are inside their own band at
   K=200 as they were at K=20.

## Caveats carried

Current-constituent survivorship on all three panels (idea 54) — inherited identically by real
and rotated draws, so the clause reading is unaffected and every level is biased upward and is
not a tradable estimate. Only J−1 distinct rotations exist per configuration (J ≈ 670 on
U56/BROAD136, ≈ 600 on SMALL439), so a 400-draw pool is 60–67% of the whole rotation
population and neighbouring offsets are correlated: blocks are disjoint in offset but not
independent, the K=200 flip rate is a lower bound, and the MAX band at large K approaches the
population maximum, which is why its drift flattens at the top and must not be read as
convergence to a critical value. BUDGET-skip's turnover mismatch (idea 186: 25.4%; idea 191:
1782.7% on the widened grid) is inherited and stated, not fixed — idea 203's subject. 2 of 180
rows (SMALL439 / BUDGET τ=0.05 / skip) have an undefined IS Sharpe and are carried as
non-clearing with the surviving n printed; nothing imputed. Idea 38's calendar-day index and
idea 126's t+1-only execution carry over.

## Follow-ups queued

214 (does the Q95 band's size hold at its nominal 5% under a known-null overlay), 215
(back-fill the Q95/K=100 band over every committed rotation-null claim and count moved
verdicts), 212 (a paired null that removes the block-count confound from the flip-rate
estimator).
