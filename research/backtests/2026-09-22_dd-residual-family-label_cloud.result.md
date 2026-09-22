# Idea 2079 — is the DD-RESIDUAL a FAMILY LABEL rather than a CONTINUOUS BOOK PROPERTY?

**Lane cloud, 2026-09-22.  Script:** `research/backtests/2026-09-22_dd-residual-family-label_cloud.py`

## ANSWER: NO.  The residual is a CONTINUOUS within-family book property, not a four-valued label.

Idea 911 measured the MaxDD-on-beta residual's IS(2009–2016)→OOS(2017–2026) persistence at
+0.33 to +0.95 and found it lives outside the crash.  2079 asked whether that whole object is
just "MADIST/LOWVOL books draw down less than MOM books at matched beta", i.e. a construction
label known before any return is priced.  It is not, and the margin is not close.

* **The label carries almost none of the residual.**  Between-family `eta^2` of `res_IS` runs
  **0.0005 – 0.0764, median 0.0154** over all 45 (family set × estimator × panel) grid points —
  **0 of 45** reach the pre-stated 0.50 bar (V2 NOT triggered).  `eta^2` of `res_OOS` is larger
  but still minor (median **0.1880**, max 0.3704).  Over 98% of the IS residual's cross-book
  variance is *within* family.
* **Removing the family fixed effect does not weaken the persistence — it slightly strengthens
  it.**  Median share of the pooled rho lost to within-family demeaning is **−0.0715** (negative
  = the correlation goes UP), and `rho_within > rho_pooled` on **32 of 45** blocks.  The
  family-demeaned rho sits **OUTSIDE** its within-family permutation null's central 95% band on
  **40 of 45** blocks (U56 15/15, B136 14/15, SMALL 11/15) — V1 NOT triggered.
* **Every family carries it on its own.**  Per-family rho over the 20 books of a single family is
  positive on **33 of 36** (panel × estimator × family) cells, median **+0.6518**
  (LOWVOL median +0.76, MOMVS +0.80, MOM +0.57, MADIST +0.42).  The three negatives are
  B136/MADIST under OLSD and OLSM and SMALL/MOM under OLSM.
* **The four family means, by contrast, are noise.**  `rho_between` over the 4 family-mean points
  ranges −0.996 to +1.000 and is **negative on 20 of 45** blocks — a coin flip, as 4 points
  should be.  The label is the part of the residual that does *not* persist.

So 911's finding stands and sharpens: the persistent object is a continuous per-book property
that survives stripping construction family, beta, and (per 911) the crash episodes.

## BY-PRODUCT (capital, rule 8): the CONTINUOUS reading buys NOTHING; the LABEL reaches the only 4b pass

Four legal IS-only choosers, parameters chosen on 2009–2016 only, 2017–2026 read ONCE.
Both KEEP paths at every pick; 12 picks, all published in `.walkforward.csv`.

| panel | chooser | pick | FULL CAGR / Sharpe / MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | 4b FULL | 4b OOS | 4a |
|---|---|---|---|---|---|---|---|---|
| U56 | IS_WITHIN | LOWVOL\|ALL\|1.00 | 15.82% / 1.141 / −22.18% | 1.15 / 1.14 | 17.45% / 1.217 / −22.18% | no | no | no |
| U56 | IS_POOLED (911's) | MADIST\|ALL\|1.00 | 15.82% / 1.141 / −22.18% | 1.15 / 1.14 | 17.45% / 1.217 / −22.18% | no | no | no |
| U56 | **IS_FAMILY (label only)** | **MADIST\|40\|0.75** | **10.86% / 1.194 / −13.55%** | **1.18 / 1.21** | **12.08% / 1.308 / −13.55%** | **YES** | **YES** | no |
| U56 | IS_SHARPE | MOM\|5\|1.00 | 24.93% / 1.016 / −34.61% | 1.24 / 0.84 | 20.92% / 0.845 / −34.61% | no | no | no |
| B136 | IS_WITHIN | MADIST\|40\|1.00 | 18.08% / 1.075 / −29.35% | 1.19 / 0.98 | 18.28% / 1.054 / −29.35% | no | no | no |
| B136 | IS_POOLED | MADIST\|40\|1.00 | 18.08% / 1.075 / −29.35% | 1.19 / 0.98 | 18.28% / 1.054 / −29.35% | no | no | no |
| B136 | IS_FAMILY | MOMVS\|40\|0.75 | 10.97% / 0.997 / −22.69% | 1.22 / 0.81 | 10.23% / 0.905 / −22.69% | no | no | no |
| B136 | IS_SHARPE | MOM\|20\|1.00 | 21.84% / 1.099 / −33.68% | 1.34 / 0.91 | 20.81% / 1.002 / −33.68% | no | no | no |
| SMALL | IS_WITHIN | MOM\|40\|1.00 | 6.88% / 0.432 / −50.25% | 0.70 / 0.24 | 4.10% / 0.296 / −50.25% | no | no | no |
| SMALL | IS_POOLED | MADIST\|40\|1.00 | 8.04% / 0.483 / −48.02% | 0.59 / 0.40 | 7.33% / 0.438 / −48.02% | no | no | no |
| SMALL | IS_FAMILY | LOWVOL\|40\|0.75 | 6.80% / 0.743 / −33.11% | 1.50 / 0.36 | 4.66% / 0.478 / −33.11% | no | no | no |
| SMALL | IS_SHARPE | LOWVOL\|10\|1.00 | 8.24% / 0.803 / −35.26% | 1.82 / 0.28 | 4.71% / 0.444 / −35.26% | no | no | no |

References on the same tape (10 bps, t+1): **RULES v2 (live)** U56 8.62% / 1.201 / −12.05%, halves
1.23 / 1.18, OOS 9.46% / 1.277 / −12.05%; B136 7.96% / 1.097 / −12.24%, OOS 7.85% / 1.102;
SMALL 4.26% / 0.659 / −14.16%, OOS 3.63% / 0.545.  **SPY** 15.14% / 0.885 / −33.72%, halves
0.96 / 0.83, OOS 15.29% / 0.875 / −33.72% (SMALL's tape starts 2011: 14.03% / 0.857 / −33.72%).

* **V3 NOT TRIGGERED.**  IS_WITHIN reaches 4b FULL+OOS on **0 of 3** arms, exactly as IS_POOLED
  does (911's KILL reproduces).  Both continuous choosers argmax onto `gross=1.00` books whose
  drawdown blows the 4b DD cap.  Naming the residual continuous buys no capital.
* **4a is empty: 0 of 12 picks.**  No shelf book beats the live RULES v2 book in both halves at
  no worse drawdown.
* The **only** 4b FULL+OOS pass in the whole arm comes from the *label-only* chooser on U56.
  That is the irony worth recording: the family label is demonstrably not what the residual *is*
  (arms 1–2), yet it is the only part of it that survives contact with the 4b bar — because the
  label chooser lands on a de-grossed mid-width book while the continuous argmax does not.
  See the memo (`.memo.md`) for the caveats; the FULL CAGR margin is **0.26 pp**.

## GATES

All pass.  G0 sample ≥ 10y (U56/B136 18.7y, SMALL 16.7y).  G2 a 100%-SPY book reads beta 1.0000
under all three estimators (max |β−1| = 0.0000).  G3 no leverage (max shelf gross 1.0000).
G4 every grid point published (45 = 3 panels × 5 family sets × 3 estimators).

## DIALS AND HONESTY

Exactly two tuned dials, every value reported: **FAMILY SET** (ALL4 + four leave-one-out triples)
× **BETA ESTIMATOR** (OLSD / OLSM / DOWN).  Panel {U56, B136, SMALL} and the four choosers are
reported, not tuned.  Nothing was selected on any dial; all 45 grid points are in `.grid.csv`,
all 36 per-family cells in `.perfamily.csv`, all 720 book-window rows in `.shelf.csv`, all 12
capital picks in `.walkforward.csv`.  Permutation null: 2000 draws, seed 20260922, shuffled
*inside* each family so the null preserves family structure and destroys only book-level pairing.

**SURVIVORSHIP.**  U56 and B136 are current-constituent lists; SMALL is a current sub-$2B screen
(54 of 720 tickers with `max_1d_move >= 1.0` dropped first, 666 kept).  Every CAGR, Sharpe and
MaxDD **level** above — including the U56 4b pass — is survivorship-optimistic.  The
decomposition arms (pooled vs within vs between) are same-shelf, same-tape contrasts with only
the residual's fixed effects changed, so they are first-order immune to that bias.

**One convention to flag:** IS_FAMILY's "median-ordered book" tie-break sorts widths as strings
(`"10","20","40","5","ALL"`), so the median of 20 books is `k=40, gross=0.75`.  The chooser is
IS-only and pre-stated in the script, but the *specific* book it lands on is a sort-order
artefact, not a fitted quantity.  A different tie-break reaches a different book.
