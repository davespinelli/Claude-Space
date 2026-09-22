# Idea 2098 (lane cloud, 2026-09-22) — does the QUIET-TAPE THRESHOLD have a STABLE ARGMAX, or is q=0.40 a BOUNDARY PICK?

**Script:** `research/backtests/2026-09-22_quiet-tape-threshold-argmax_cloud.py`
**Artifacts:** `.grid.csv` (165 rows, every grid point), `.shelf.csv` (240 books, every shelf book
scored on both KEEP paths), `.curves.csv` (18 argmax curves), `.ladder.csv` (24 cost x lag cells),
`.gates.csv`, `.log.txt`.

## VERDICT — **ANSWERED (q=0.40 is a genuine INTERIOR argmax, not a boundary artefact) + KILL of the quiet-tape chooser as a DEVICE.**

The narrow question 2098 asked is settled in idea 2083's favour. The question it did not ask —
*is the chooser worth anything at all* — is settled against it by the shelf's own base rate.

## 1. THE ARGMAX IS INTERIOR (V1 YES, 14 of 18 curves)

Extending the ladder to `q in {0.10,0.20,0.30,0.40,0.50,0.60,0.80,0.90,1.00}` (the four rungs
below 0.50 are new; 2083 stopped at 0.40) puts the REACH argmax strictly inside the ladder on
**14 of 18** (panel x definition x form) curves. REACH = min over the seven 4b legs of the
margin normalised by its own bar; REACH > 0 iff the point clears 4b FULL *and* OOS (gate G6b:
exact on 165 of 165 rows).

## 2. 2083's OWN CELL PEAKS AT q=0.40 WITH A STRICT FALL-OFF ON BOTH SIDES (V2 YES)

U56 / NEARHI_EXP / QRESID (NEARHI_252 is identical row-for-row):

| q | pick | OOS CAGR / Sharpe / MaxDD | DD gap vs cap | REACH | 4b |
|---|---|---|---|---|---|
| 0.10 **NEW** | MOM/20/1.00 | 22.24% / 1.272 / −25.25% | −5.02 pp | −0.2481 | 0 |
| 0.20 **NEW** | MOM/20/1.00 | 22.24% / 1.272 / −25.25% | −5.02 pp | −0.2481 | 0 |
| 0.30 **NEW** | MOM/40/1.00 | 16.17% / 1.297 / −17.96% | +2.27 pp | +0.1122 | **1** |
| **0.40** | MADIST/40/1.00 | **16.24% / 1.310 / −17.67%** | **+2.56 pp** | **+0.1264** | **1** |
| 0.50 | MADIST/ALL/1.00 | 17.45% / 1.217 / −22.18% | −1.95 pp | −0.0965 | 0 |
| 0.60 | MOM/ALL/1.00 | 17.47% / 1.219 / −22.18% | −1.95 pp | −0.0965 | 0 |
| 0.80 / 0.90 / 1.00 | MADIST/ALL/1.00 | 17.45% / 1.217 / −22.18% | −1.95 pp | −0.0965 | 0 |

REACH rises 0.10 → 0.40 and falls at 0.50, so q = 0.40 is an interior maximum with a strictly
worse neighbour on each side. **The pass is not endpoint-ness** (cf. idea 1153). But the passing
region is only **2 of 9 rungs** ({0.30, 0.40}); at q ≤ 0.20 the chooser jumps to MOM/20/1.00 and
misses the DD leg by 5.02 pp. The dial has an optimum, and it is narrow.

## 3. THE SUB-0.40 REGION IS LIVE (V3 YES, 2 of 54)

q = 0.30 clears 4b on both near-high definitions, reaching a **different** book (MOM/40/1.00,
FULL 14.56% / 1.195 / −17.96%, OOS 16.17% / 1.297 / −17.96%). Whole grid: **5 of 165** points
clear 4b FULL+OOS, all on U56 — the two q=0.30 rows, the two q=0.40 rows (2083's cell, reproduced
to 4 dp by gate G1b) and one new VOL60 / q=0.80 row reaching MOMVS/40/1.00. **4a: 0 of 165.**
QRAW clears 0 of 81. The IS_SHARPE reference chooser clears 0 of 3 panels.

## 4. AND THE CHOOSER IS WORSE THAN ITS OWN SHELF (post-hoc diagnostic, ARM 4 — NOT pre-stated)

ARM 3 showed every clearer is a **k = 40, gross 1.00** book, so the shelf's own base rate was
measured. It is the result that matters:

| panel | shelf books clearing 4b | QRESID picks clearing 4b | lift |
|---|---|---|---|
| U56 | **20 of 80 (25.0%)** | 5 of 27 (18.5%) | **−6.5 pp** |
| B136 | 4 of 80 (5.0%) | 0 of 27 (0.0%) | −5.0 pp |
| SMALL | 0 of 80 (0.0%) | 0 of 27 (0.0%) | +0.0 pp |

On U56 a **uniform draw from the shelf beats the quiet-tape chooser**, and on B136 the chooser
reaches none of the 4 books that clear. Counted over DISTINCT books instead of grid points
(the picks are heavily duplicated — 9 distinct books over 27 U56 points), the chooser reaches
3 clearers out of 9 distinct books (33.3%) against the shelf's 25.0%: a positive but tiny
direction on a sample far too small to resolve. Neither reading supports the device.

Decisive: at U56 / k=40 / gross 1.00 **all four families clear 4b** — MOM 1.2971, MOMVS 1.2760,
MADIST 1.3099, LOWVOL 1.2304 OOS Sharpe, every one inside the −20.23% cap. The 4b pass is a
property of **that cell** (top-40 of a 56-name current-constituent list at full gross, monthly),
not of the family and not of the quiet-tape statistic. The chooser's only job is to land there,
and it does so on 5 of 81 QRESID points.

## 5. ROBUSTNESS AND RULE 8

Rule 8 throughout: the chooser sees 2009–2016 only; 2017–2026 read once. Cost {0,10,25,50} bps x
signal lag {0,+1 day} at all three clearing books: **24 of 24 cells hold 4b**. A +1-day lag costs
~1.9 pp of drawdown margin on each (OOS MaxDD −17.67% → −19.61% for MADIST/40 at 10 bps), so the
margin is thin but not a knife edge — identical to 2083's finding.

## 6. GATES

G0 sample ≥ 10y; G1/G1b 2083's q=0.40 pick and OOS numbers reproduced exactly; G1c 911's q=1.00
pick (MADIST/ALL/1.00, OOS −22.18%) reproduced; G2 SPY beta 1.0000; G3 no leverage (max gross
1.0000); G4 all three distress series causal (max|diff| = 0); G5 all 165 grid points published;
G6a both near-high definitions keep every IS day at q=1.00; G6b VOL60 drops exactly its 20-day
`min_periods` warm-up (inherited from 2083's definition — causal, and it does not touch the
2083 comparison; 2083 published this as a FAIL with the same cause); G6b' REACH > 0 iff 4b on
165 of 165; G7 ladder reproduces the grid row at lag 0 / 10 bps (max|diff| = 0).

## 7. SURVIVORSHIP (rule 9)

U56 / B136 are CURRENT-constituent lists; SMALL is a CURRENT sub-$2B screen (665 names after
dropping `max_1d_move >= 1.0`). Every CAGR and MaxDD LEVEL is optimistic and both 4b bars are
easier here than on a point-in-time panel — the 25% U56 shelf base rate is itself a survivorship
number and is the strongest reason to read section 4 as a ceiling, not a floor. The ARGMAX
CONTRAST (where reach peaks on the q ladder) is same-shelf / same-tape with only the day mask
moved, so it is first-order immune; the pass COUNTS are not.
