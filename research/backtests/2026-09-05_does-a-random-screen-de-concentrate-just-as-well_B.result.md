# IDEA 198 — does-a-random-screen-de-concentrate-just-as-well (lane B, 2026-09-05)

**VERDICT: KILL of the IS-window 4b SCREEN as a selector. The queue's "if it is inside" branch
fires. The screen's published +0.0287 sits at the 54.5th percentile of a null that admits a
RANDOM subset of the screen's own admitted size — dead centre, z +0.11. Idea 199's floor
`n >= 25` sits at the 100.0th percentile of the same null, z +4.57. Restriction per se buys
+0.0272 of the screen's +0.0287; the screen adds +0.0015.**

Script: `2026-09-05_does-a-random-screen-de-concentrate-just-as-well_B.py`
Outputs: `.console.txt`, `.corpus.csv`, `.null.csv`, `.percell.csv`, `.ladder.csv`,
`.instruments.csv`, `.walkforward.csv`

## Reproduction, asserted before any new number was read
Idea 199's base pass was IMPORTED and re-run; the resulting 1003-row corpus matches **both**
committed copies (idea 178's and idea 199's) at **0.000e+00** on all 11 metrics with 0 `n`
mismatches, and the two published edges reproduce exactly: screen [AS165] **+0.0287**
(idea 178 published +0.0287) and `SIZE n>=25` **+0.1297** (idea 199 published +0.1297).

## The null, stated exactly
For cell *c* the instrument admits *s_c* of *N_c* books. One draw picks a uniform random
*s_c*-subset, takes the IS-Sharpe argmax inside it, and is scored against S0 (the full-pool
IS-Sharpe argmax) exactly as the real instrument is. When *s_c* = 0 the real instrument falls
back to S0 and scores 0; the null does the same, so the seven structurally-empty cells are ties
on both sides. 200 draws per cell, seed 198. Pooled statistic = mean paired dOOS over the 11
cells — the same statistic idea 178 published.

## Q2/Q3 — where each instrument sits in its OWN size-matched null

| selector | live cells | mean s | real dOOS | null mean | null sd | null p5 | null p95 | pct | z | inside 5–95 |
|---|---|---|---|---|---|---|---|---|---|---|
| SCREEN 4bIS [AS165] | 4 | 5.7 | +0.0287 | +0.0272 | 0.0139 | +0.0038 | +0.0485 | 54.5 | +0.11 | **YES** |
| SCREEN 4bIS [PUB] | 4 | 3.7 | +0.0172 | +0.0205 | 0.0228 | −0.0235 | +0.0519 | 34.0 | −0.15 | **YES** |
| SIZE n>=10 | 11 | 61.4 | +0.0543 | +0.0267 | 0.0155 | +0.0049 | +0.0539 | 95.0 | +1.78 | no |
| SIZE n>=15 | 11 | 47.7 | +0.0760 | +0.0358 | 0.0152 | +0.0123 | +0.0594 | 99.0 | +2.65 | no |
| SIZE n>=20 | 11 | 43.2 | +0.0708 | +0.0406 | 0.0170 | +0.0139 | +0.0681 | 96.0 | +1.78 | no |
| SIZE n>=25 | 11 | 36.7 | +0.1297 | +0.0471 | 0.0181 | +0.0201 | +0.0745 | **100.0** | **+4.57** | no |

Both tuned parameters are reported at every grid point: the coefficient convention (AS165 / PUB)
and the floor k (10/15/20/25). The screen is inside its null under **both** conventions; every
floor is at or outside the 95th percentile, and the ordering of the floors is monotone in z
apart from k=20.

## The screen's alleged mechanism, measured against the same null
Idea 178 diagnosed the screen as a de-concentration instrument. Inside its own null it
de-concentrates **less than chance**:

| selector | real mean picked n | null mean picked n | n percentile | real dMaxDD | null dMaxDD |
|---|---|---|---|---|---|
| SCREEN 4bIS [AS165] | 9.73 | 10.49 | **35** | −0.0075 | −0.0022 |
| SCREEN 4bIS [PUB] | 13.91 | 10.63 | 94.5 | −0.0116 | −0.0037 |
| SIZE n>=25 | 27.82 | 10.32 | **100** | −0.0353 | −0.0031 |

Per cell, the screen fires in only 4 of 11 (admitted sizes 35, 23, 3, 2). In its **largest**
firing cell — C159/broad@10bps, 35 of 98 books admitted — the screen leaves the pick unchanged
and scores **+0.0000 against a null mean of +0.0554, the 4th percentile**. Its other three live
cells sit at the 60.5th, 56.0th and 39.5th.

## Q4 — why restriction alone works: the IS argmax is a concentration machine
Random subsets at a **fixed** size in every cell (no matching to any instrument):

| subset size | 1 | 2 | 3 | 5 | 8 | 12 | 20 | 35 | 50 | 75 |
|---|---|---|---|---|---|---|---|---|---|---|
| mean dOOS | +0.0121 | +0.0648 | **+0.0756** | +0.0732 | +0.0706 | +0.0662 | +0.0573 | +0.0449 | +0.0326 | +0.0131 |
| mean picked n | 27.4 | 29.7 | 27.1 | 23.1 | 17.3 | 13.9 | 11.3 | 9.8 | 9.1 | 8.9 |

A random **3-book** subset returns +0.0756 — **263% of the screen's published edge**, with two
tuned parameters fewer. The curve is an inverted U: at s=1 the pick is uniform (mean n 27.4 =
the pool mean, dOOS +0.0121 with sd 0.055); as s grows the IS-Sharpe argmax reaches further into
its own tail, mean picked n falls monotonically to S0's 8.55 (rho(size, picked n) = **−0.988**)
and the OOS gain drains away. Within-cell, rho(n, OOS Sharpe) is **+0.489** (t +3.67) while
rho(n, IS Sharpe) is only +0.195 — so OOS rewards big books, and the extreme IS-Sharpe tail is
small ones. Everything the screen, the floors and the null have in common is that they stop the
argmax reaching that tail. Inside the draws, a draw's mean picked n predicts its dOOS
(mean rho +0.262 across the six matched nulls).

## Q5 — rule 8 (all picks made on ≤2016-12-31; 2017–2026 read once)

| arm | OOS CAGR | OOS Sharpe | OOS MaxDD | dOOS vs S0 | mean n | 4a | 4b |
|---|---|---|---|---|---|---|---|
| S0 do-nothing (IS-Sharpe argmax) | 13.53% | 0.7515 | −25.76% | 0.0000 | 8.5 | 3/11 | 0/11 |
| SCREEN 4bIS [AS165] | 13.45% | 0.7802 | −25.01% | +0.0287 | 9.7 | 3/11 | 2/11 |
| **NULL matched to the screen (mean draw)** | — | **0.7787** | — | **+0.0272** | — | — | — |
| SIZE n>=25 | 10.96% | 0.8812 | −22.23% | +0.1297 | 27.8 | 3/11 | 4/11 |
| NULL matched to n>=25 (mean draw) | — | 0.7986 | — | +0.0471 | — | — | — |
| RULES v1 @ each cell's cost | 5.04% | 0.4849 | −21.96% | — | — | — | — |
| SPY buy-and-hold | 15.45% | 0.8820 | −33.72% | — | — | — | — |

The screen and its null are separated by **0.0015 of OOS Sharpe**. Pool-wide both KEEP paths:
302/1003 books pass 4a, 162/1003 pass 4b, 229/1003 clear the OOS window. **This run proposes no
new book and no new rule, so it produces no KEEP candidate**; every book is idea 159/165/168's,
already priced. Note also that no arm here beats SPY on OOS CAGR, and only `n>=25` reaches SPY's
OOS Sharpe (0.8812 vs 0.8820) — while paying 4.5pp of CAGR for it.

## Pre-registered predictions: 5 of 5 hit
1. corpus + both published edges reproduce — **HIT** (0.000e+00; +0.0287 / +0.1297)
2. the screen sits INSIDE its size-matched null — **HIT** (54.5th pct, z +0.11)
3. the best size floor sits ABOVE its own null — **HIT** (n>=25, 100.0th pct, z +4.57)
4. within the null, a draw's mean picked n predicts its dOOS — **HIT** (mean rho +0.262)
5. the pure pool-size ladder is not flat at zero — **HIT** (max |mean dOOS| 0.0756)

## What this changes in the record
* Idea 178's screen is **a book-size prior wearing a 4b label**, and a weak one: it is
  indistinguishable from a random subset of its own size, and it de-concentrates less than that
  random subset does (35th percentile on picked n).
* Idea 199's `n >= k` floor survives this null. The two results together say: **restriction per
  se is not the mechanism and de-concentration is** — the floor beats its null precisely because
  it raises n far above what a same-size random subset raises it to.
* Note what is NOT claimed: on this corpus every instrument, screen and floors alike, **beats**
  do-nothing on OOS Sharpe (dOOS +0.0172 to +0.1297). The record's usual "the fit loses to
  do-nothing" result does not recur here. What fails is the screen against the *right* null,
  which is a different and stronger objection: it beats do-nothing by exactly as much as noise
  of its own size does.
* A methodological by-product worth a PROTOCOL note: **any selector that restricts an IS-argmax
  pool must be priced against a size-matched random restriction**, because restricting an
  overfit argmax is worth up to +0.0756 OOS Sharpe on this corpus for free. Comparing such a
  selector against do-nothing overstates it by roughly its whole effect.

## Caveats carried
* SURVIVORSHIP (idea 54): all three panels are current constituents; the small panel contains no
  delistings and its levels are biased upward. Every arm reads the same biased panel, so the
  comparison is unaffected; no level here is a tradable estimate.
* The screen fires in only 4 of 11 cells, so its null has 4 live cells and correspondingly little
  power. This is a property of the screen, not a choice made here. The result is that the screen
  cannot be distinguished from chance — not that it is proven equal to chance.
* 11 cells sharing three panels and two corpora is a small, correlated sample; every paired
  difference is an estimate and is reported with its t / W-L-T or its percentile.
* Idea 38 (calendar-day index after 2014-09-17 on u56/broad) and idea 126 (t+1 only) apply.
