# idea 124 — book-size-floor-for-any-quoted-price (lane B, 2026-09-07) — INDEPENDENT THIRD RUN

> **Provenance.** Two other runs of idea 124 landed upstream while this one was executing
> (`…_B` SPLIT and `…_cloud` KILL). This run was written and executed without sight of either
> and is committed under the `_B2` stem so none of their files are overwritten. All three
> reach the same headline (no statable book-size floor). Section F reconciles this run against
> the committed `_B` run row by row: **384 shared rows, 0 disagreements on the deterministic
> D1/D2 legs and on `published`, 10 disagreements on `admissible`, from two identified causes,
> one of which is checkable against idea 122's own committed file.**

**VERDICT: KILL of the queue's premise — there is NO book-size floor to state.** The
admissible fraction is not monotone in n on either panel (spearman(n, adm_frac) +0.116 on
u56, +0.486 on B136), the pooled curve's WORST rung is n=20 (0.551) — the very number the
record uses informally — and the only rung clearing 0.90 on both panels at the headline is
ALL, at every one of the 12 (q, tau) points. A floor is the wrong shape for this quantity.
Two substantive by-products below: the record's attribution of the failures was **wrong**,
and where size does act is **priceability**, not sign stability.

Script `2026-09-07_book-size-floor-for-any-quoted-price_B2.py`; 448 published rows
(7 books x 16 arms x 2 costs x 2 panels), 2382 s, deterministic (seed 20260905, idea 122's).

## Design
One family, one dial. `TOPn` = idea 2's composite ranking, no vol scaler, no gate, top-n at
GROSS/n, GROSS = 0.75 at every rung, n in {3, 5, 10, 20, 40, ALL}. Same score, same days,
same gross, same 16 instruments, same cost rungs — the rungs differ in CONCENTRATION only.
`V1u` (5 names AND the 1/sqrt(vol20) scaler) is carried as an **off-ladder reference** so the
ladder's own n=5 rung can separate size from the scaler, which idea 122 could not.
Sign test inherited verbatim from idea 119/122: D1 cost {0,5,10,25} bps, D2 window IS/OOS,
D3 panel = 40 name-deletion draws per q. **Two tuned parameters, both of the test** (q, tau);
all 12 grid points reported. n is the measured axis, never selected.

## Reproduction gates (all EXACT, read before any new number)
| gate | result |
|---|---|
| ladder rung TOP20 and V1u vs idea 94 `targets()` | **0.000e+00** |
| control vs `engine.backtest` @10 bps, all 7 books | **0.000e+00** |
| TOP20 + V1u vs idea 122's committed `signtest.csv` (dCAGR, dMaxDD, rate, dMaxDD_IS/OOS, D1, D2; 64 rows each) | **≤1.8e-15** |
| TOP20 + V1u vs idea 122's committed `d3.csv` (frac_pos full/IS/OOS, 96 cells each; same seed, same draws) | **0.000e+00** |

So this ladder literally contains two of idea 94's three books, and the audit is of that file.

## A. The answer — admissible fraction by rung, headline (q, tau) = (0.10, 0.90)
| rung | n | u56 pub / adm_frac | B136 pub / adm_frac | pooled adm_frac | pooled **yield** (adm / all 32 candidate rows) |
|---|---|---|---|---|---|
| TOP3 | 3 | 18 / 0.889 | 19 / 0.421 | 0.649 | 0.375 |
| TOP5 | 5 | 12 / **1.000** | 14 / 0.714 | 0.846 | 0.344 |
| TOP10 | 10 | 22 / 0.864 | 18 / 0.389 | 0.650 | 0.406 |
| TOP20 | 20 | 22 / 0.818 | 27 / 0.333 | **0.551 (worst)** | 0.422 |
| TOP40 | 40 | 24 / **1.000** | 28 / 0.786 | 0.885 | 0.719 |
| TOPALL | 56 / 136 | 24 / 0.958 | 24 / **1.000** | **0.979** | 0.734 |
| *V1u (off-ladder)* | *5* | *24 / 0.333* | *17 / 0.471* | *0.390* | *0.250* |

n* (smallest rung ≥ 0.90 on BOTH panels) = **ALL** at every (q, tau); at a slacker 0.80 bar it
is TOP40 for the three q=0.05 cells and ALL everywhere else; at a 1.00 bar no rung qualifies.
**Not monotone on either panel** (P1 REFUTED), so "quote no rate below n names" cannot be
written: TOP5 outscores TOP10 and TOP20 on both panels, and the record's informal ~20 is the
single worst rung of the six.

## B. What the record got wrong — it is the SCALER, not the size (P4 CONFIRMED)
| book | n | u56 adm_frac | u56 D3 | B136 adm_frac | B136 D3 |
|---|---|---|---|---|---|
| TOP5 (5 names, no scaler) | 5 | **1.000** | **1.000** | **0.714** | **1.000** |
| V1u (5 names + 1/sqrt(vol20)) | 5 | 0.333 | 0.333 | 0.471 | 0.529 |

At matched book size the clean rung is 0.857 admissible against V1u's 0.402 (mean over
panels). Idea 122 reported "all 24 panel-axis and all 5 cost-axis failures are the 5-name V1u
book" and the record read that as a book-size result; at matched size the panel axis kills
**0 of 26** TOP5 rows and **24 of 41** V1u rows. The fragile ingredient is the vol scaler
that finding 1 of the Sep-3 recommendation already showed cancels the composite's IC — its
1/sqrt(vol20) division makes the top-5 set jump on small panel perturbations. **The record's
"~20 names" rule of thumb is measuring the wrong variable.**

## C. Where book size DOES act: priceability, not sign stability
Conditional on a row being published, small books are fine. What small books do is fail to
produce a quotable row at all: idea 94's absolute floor (|dMaxDD| > 0.10 pp) drops 20 of 32
TOP5 rows on u56 and 18 of 32 on B136, and the dominant cause is a **negative** denominator —
the instrument makes drawdown WORSE on a concentrated book.
- frac(dMaxDD ≤ 0) by rung, u56: .344 / .438 / .312 / .250 / .250 / .219, spearman(n, ·) **−0.928**
- B136: .250 / .531 / .438 / .125 / .125 / .125, spearman **−0.759**
- yield (admissible rows / all 32 candidates) rises 0.50 → 0.72 (u56) and 0.25 → 0.75 (B136),
  spearman(n, yield) **+0.829 / +0.714** — the only genuinely size-ordered statistic here.

So the honest clause PROTOCOL can carry is not a floor on n but: **report the yield.** A
price list must state how many of its candidate cells produced no quotable denominator, and
why (sign vs magnitude), because at n ≤ 10 that is a third to a half of them.

## D. Rule 8 walk-forward (28 cells; parameters chosen on 2009–2016, read once on 2017–2026)
S1 = idea 94's selector (lowest IS rate among arms buying ≥1 pp IS MaxDD). S2 = same,
restricted to arms passing the sign test computed on IS data only.
- S1 mean OOS Sharpe **0.8735**, S2 **0.8761**; own control 0.8949, **RULES v2 1.1815**,
  RULES v1 0.4695, **SPY 0.8820**. Beats SPY 15/28, beats RULES v2 3/28 (both selectors).
- The IS sign screen changes the pick in **2 of 28** cells and both selectors sit below the
  do-nothing control — consistent with ideas 122/129/151: the screen is report-only.
- **S3, the floor as a walk-forward object: n\*_IS and n\*_OOS agree at 0 of 12 (q, tau)
  points** (n\*_IS is undefined at 10 of 12 — no rung clears the bar on IS data alone —
  while n\*_OOS lands on TOP5 six times, TOP20 twice, ALL three times). A number that cannot
  be reproduced across the split is not a number PROTOCOL can state. This is the decisive
  reason the answer is KILL rather than "the floor is 40".

## E. KEEP paths (all 448 rows)
- **4b: 52 of 448** (u56 TOP20 15, TOP40 11, TOPALL 8, TOP5 3, TOP10 1; B136 TOP40 6,
  TOPALL 8; V1u and TOP3 zero). Best: u56 TOP40 band3-rw @10 bps — CAGR 11.4%, Sharpe 1.211,
  MaxDD −15.7%. All are re-measurements of families the record already holds (ideas 28/331/
  359/360); none beats the standing candidates and none is promoted here.
- **4a vs live RULES v2: 2 of 448**, and both are **degenerate** — u56 TOPALL band3-dg at 10
  and 25 bps IS RULES v2 under a different name-count denominator: mean |Δw| 8.0e-05,
  return correlation **0.99983**, Sharpe 1.2088 vs 1.2056, identical MaxDD −12.05%. Adopting
  it would be a no-op, so **no rules change is proposed and no memo is written.** Excluding
  that duplicate, 4a is 0/448 (the idea-136 pathology again). 4a vs the retired RULES v1 is
  112/448 and is reported only for continuity.
- P5 therefore holds in substance: this is a measurement run and produced no new KEEP.

## F. Reconciliation with the same-day `…_B` run (384 shared rows)

Both runs price the same 7 books x 16 arms x 2 costs x 2 panels under the same inherited sign
test. Joined on (uni, book, cost, arm):

| leg | agreement |
|---|---|
| `published` (idea 94's absolute floor) | **384 / 384** |
| dCAGR, dMaxDD, rate, dMaxDD_IS, dMaxDD_OOS (D1 + D2, deterministic) | identical wherever both publish |
| `admissible` | **374 / 384** — 10 disagreements, all on u56 |

The 10 split into exactly two causes, both identified:

**(i) Definition — 2 rows (TOP20 abs12-dg @10 and @25 bps).** The `_B` file marks these
`admissible = True` with `published = False`; this run's `ADMISSIBLE` conjoins `published`, so
idea 94's absolute floor (|dMaxDD| > 0.10 pp) is carried into the verdict and the rows are
False. Both conventions are defensible — but they are different statistics, and since the
share is reported *of published rows*, mixing them changes the headline curve. This is the
whole of the TOP3/TOP20 gap between the two runs' floor tables (their u56 0.556 / 0.727 at
n = 3 / 20 against this run's 0.889 / 0.818).

**(ii) The D3 bootstrap on the three PATH-DEPENDENT arms — 8 rows (TOP3 and TOP20 x
ebud-0.10, ebud-0.20, stop15).** Both runs use idea 122's seed, q order and NDRAW, so the
kept-column sets are identical; the gate arms agree to the last digit in both runs. On the
stateful arms they do not, and idea 122's **committed** `d3.csv` breaks the tie:

| u56 TOP20, q = 0.10 | idea 122 (committed) | this run | `…_B` run |
|---|---|---|---|
| ebud-0.10 `frac_pos_full` | 0.925 | **0.925** | 0.875 |
| ebud-0.20 | 0.400 | **0.400** | 0.350 |
| stop15 | 0.100 | **0.100** | 0.075 |
| abs12-dg (gate) | 0.975 | 0.975 | 0.975 |
| g200-dg (gate) | 1.000 | 1.000 | 1.000 |

Each stateful disagreement is exactly 0.025 = one draw of forty. This run reproduces the
record's committed D3 at 0.000e+00 across all 16 arms (gate C above); the `…_B` run differs
from it by one draw on each path-dependent instrument. That does not overturn either run's
headline — both are far from any bar — but the record should carry one number, so the
discrepancy is queued as idea 382 rather than asserted away here.

**Where the two runs agree:** no statable floor; non-monotone in n; the whole panel is the
only rung clearing the bar on both panels; the published set shrinks with concentration; and
no KEEP. The `…_B` run additionally reads the unconditional draw-level statistic as making
TOP5 the *least* stable rung, which is the same phenomenon this run reports in section C from
the other side (at n = 5 the instrument's denominator is negative on 14/32 and 17/32 rows, so
the few rows that survive the floor are the biggest movers).

## Prediction scorecard (all written before any number was read)
| | prediction | result |
|---|---|---|
| P1 | admissible fraction monotone non-decreasing in n | **REFUTED** (False on both panels) |
| P2 | n* ≤ 20 on both panels | **REFUTED** (n* = ALL, or nothing) |
| P3 | the binding axis at small n is D3 (panel), not D1 (cost) | **CONFIRMED** (D3 37 failures vs D1 6; at n ≤ 5, 31 vs 6 — but 24 of the 31 are V1u's, see B) |
| P4 | clean TOP5 more admissible than V1u | **CONFIRMED** (0.857 vs 0.402) |
| P5 | no new KEEP | **holds** (4b 52 all re-measurements, 4a 2 both duplicates of the live book) |

## Caveats
- SURVIVORSHIP: universe.json (56) and universe_broad.json (136) are current-constituent
  lists; every absolute CAGR is optimistic. The results above are within-cell differences and
  sign stabilities, far less exposed than levels, but a survivorship-free panel could move
  which rows pass.
- The ALL rung is the n → ∞ limit of the composite family (every name with a defined score),
  which is NOT identical to idea 94's EWall (every name PRICED): max |Δw| 0.0150, and the two
  counts differ on 1530 of 4439 u56 eval days. Idea 94's EWall, read from idea 122's
  committed d3.csv on the identical draws, has mean frac_pos 0.7609 against this ALL rung's
  0.8133 — a 5-point sign-stability gap created purely by which names the denominator counts.
  That gap is a defect in its own right and is queued as idea 378.
- The printed census table in section D of the console double-counts `rows`/`unpriceable` for
  the ALL rung (it groups by (book, n) and ALL has a different n per panel); the corrected
  per-panel census is in the table above and in `.signtest.csv`, from which it is recomputed.

## Files
`.py`, `.console.txt`, `.grid.csv` (448 rows), `.signtest.csv` (per-row 3-axis verdicts),
`.floorcurve.csv` (all 12 (q, tau) x 14 book-panel curves), `.d3.csv` (2 x 3 x 7 x 16
bootstrap summaries), `.bootstrap.csv` (26,880 draw-level rows), `.walkforward.csv`,
`.floorwf.csv` (S3), `.census.csv`, `.reproduction.csv`.  Committed under the `_B2`
stem; the same-day `…_B` and `…_cloud` runs are untouched.
