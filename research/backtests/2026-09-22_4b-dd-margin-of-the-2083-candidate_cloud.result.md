# Idea 2090 (lane cloud, 2026-09-22) — the 2083 KEEP-candidate's +2.56 pp DD margin is **NOT RESOLVABLE at 95%**

**ANSWERED = NO. KILL of the candidate as a capital finding.** The drawdown leg that 2083's 4b
pass stands on is a coin flip: its paired circular-block bootstrap puts **55.8%** of draws on the
passing side, and the 95% interval spans zero at **every one of the six (block, confidence) grid
points**. The CAGR floor is resolvable; the DD leg and the first-half Sharpe leg are not.

## The cell reproduces exactly (gate G4)

| book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|---|---|
| **MADIST/40/g1.00/M (U56, 2083's cell)** | 14.57% | 1.1965 | −17.67% | 1.1834 / 1.2098 | **16.24% / 1.3099 / −17.67%** |
| MOMVS/40/g1.00/M (sibling) | 14.29% | 1.1946 | −18.17% | 1.2106 / 1.1806 | 15.51% / 1.2760 / −18.17% |
| RULES v2 (live, weekly, 10 bps) | 8.62% | 1.2010 | −12.05% | 1.2276 / 1.1806 | 9.46% / 1.2767 / −12.05% |
| SPY | 15.14% | 0.8851 | −33.72% | — | 15.29% / 0.8751 / −33.72% |

2083's committed OOS row (16.24% / 1.3099 / −17.67%) reproduces to the digit. **Path 4a FAILS**
(the book never beats the live book's first half); path 4b PASSES on the point estimate. The
book's worst drawdown falls inside the OOS window, so the full-sample and OOS DD legs are the
same number (+2.5563 pp) read on two different resample windows.

## Every leg, every grid point (U56, MADIST/40; * = interval entirely on the passing side)

| leg | window | point | boot SD (B=21) | point/SD | 95% CI (B=21) | resolvable at 95%, of 3 blocks |
|---|---|---|---|---|---|---|
| L1_H1 Sharpe | H1 | +0.2263 | 0.1985 | +1.14 | [−0.1327, +0.6386] | **0/3** |
| L2_H2 Sharpe | H2 | +0.3834 | 0.1900 | +2.02 | [+0.0038, +0.7239]* | 2/3 |
| L3_OOS Sharpe | OOS | +0.4348 | 0.1806 | +2.41 | [+0.0644, +0.7600]* | 3/3 |
| **L4_DD full** | FULL | **+0.0256** | 0.0400 | **+0.64** | **[−0.0734, +0.0843]** | **0/3** |
| L5_CAGR full | FULL | +0.0398 | 0.0186 | +2.14 | [+0.0035, +0.0756]* | 3/3 |
| **L4_DD OOS** | OOS | **+0.0256** | 0.0384 | **+0.67** | **[−0.0617, +0.0895]** | **0/3** |
| L5_CAGR OOS | OOS | +0.0554 | 0.0246 | +2.25 | [+0.0058, +0.1021]* | 3/3 |

Fraction of draws on the passing side at B=21: L4_DD full **0.512**, L4_DD OOS **0.558** — against
L5_CAGR 0.986 and L3_OOS 0.991. Resolvable cells over the whole 7-leg x 3-block grid: **12/21 at
90%, 11/21 at 95%**. Widening the block from 10 to 63 days does not rescue the DD leg at either
confidence; it never comes close (the interval half-width is ~3x the margin).

## Pre-stated verdicts

- **V1 (the idea's own question) — NOT TRIGGERED.** The OOS DD leg is resolvable at 0/3 block
  lengths. The +2.56 pp is a point estimate.
- **V2 — TRIGGERED.** The CAGR floor is resolvable 3/3 on both the full sample and OOS.
- **V3 — NOT TRIGGERED.** Two of the five 4b legs (L1_H1 and L4_DD) fail to resolve, so the 4b
  pass as a whole is not a resolvable pass.
- **V4 — TRIGGERED.** The MOMVS/40 sibling returns the same DD answer (0/3), so this is a
  property of the cell's shape, not of the MADIST ranking. That is the same direction lane C's
  idea 2094 found today by a different route (the ranking's contribution is indistinguishable
  from zero).

## Generality and rule 8

- **B136**: the same cell **fails 4b outright** (18.08% / 1.0753 / −29.35%; DD margin −9.12 pp),
  and there the failure *is* nearly resolvable (0.6% of draws pass). The candidate is a U56 object.
- **Rule 8** (2083's own 80-book shelf, IS-Sharpe chooser on 2009–2016, 2017+ read once): the
  chooser picks **MOM/5/g1.00/M** on U56 — OOS **20.92% / 0.8446 / −34.61%, 4b FAIL, 4a FAIL** —
  and MOM/20/g1.00/M on B136 (20.81% / 1.0024 / −33.68%, 4b FAIL). 2083's cell ranks **41 of 80**
  (U56) and 39 of 80 (B136) on IS Sharpe: **no IS-Sharpe chooser reaches it.** Shelf-wide 4b
  passes: 20/80 (U56), 6/80 (B136); 4a passes 0/80 and 2/80.

## Caveats, stated not repaired

- A block bootstrap **breaks the single longest loss run**, so a DD interval is conservative-to-
  noisy by construction. That cuts both ways and is exactly why the DD leg is the one worth
  bootstrapping: a margin whose own resampling noise is 1.5x its size is not a finding at any
  convention.
- Windows are resampled independently of one another.
- **Survivorship (rule 9):** U56 and B136 are current-constituent lists, so every CAGR and MaxDD
  level is optimistic and both 4b bars are easier than on a point-in-time panel. The intervals
  are same-tape, same-names, paired contrasts and are first-order immune; the pass levels are not.

**Nothing enacted. No memo. No RULES change.** Script:
`research/backtests/2026-09-22_4b-dd-margin-of-the-2083-candidate_cloud.py`
