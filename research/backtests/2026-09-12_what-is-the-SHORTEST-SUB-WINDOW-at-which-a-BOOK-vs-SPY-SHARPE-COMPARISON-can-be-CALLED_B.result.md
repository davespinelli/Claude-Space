# Idea 838 (lane B, 2026-09-12) — what is the SHORTEST SUB-WINDOW at which a BOOK-vs-SPY SHARPE COMPARISON can be CALLED?

**VERDICT: KILL of the queue's premise. There is no PROTOCOL-grade minimum callable length in this
record's data — at the PROTOCOL cost rung the shortest callable sub-window is LONGER THAN THE
SAMPLE. No RULES change, no book promoted, no KEEP claimed, no memo. RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.**

## Gates (printed before any new number)
5 of 6 PASS. **G1/G2 12 of 12** books reproduce their committed triples (LIVE = 8.63%/1.2018/−12.05%
against RULES v2's 8.63%/1.202/−12.05%). **G3 6 of 6 EXACT** — idea 832's committed noise table is
reproduced to 4 decimals on its own block set (0.9858 / 0.9908 / 0.9821 / 0.9649 / 0.9845 / 0.9888,
max |d| 0.0000). **G4 PASS** (2.220e-16 vs bar 1e-10). **G5 PASS** (analytic/bootstrap sd ratio
median 1.1595, IQR 1.0669–1.2615). **G6 FAILS** and its failure is a finding: the closed form the
analytic band implies, L̂ = 1.96²·V₁ₐ/d², evaluated at each book's median 756d block, gives a median
**5,299d (21 years)** and range 1,033d–10,128d, and agrees with the swept L* within one rung at only
**2 of the 5** books where L* is defined — the crossing is driven by the upper tail of |d|, not the
median block, so the closed form is not a substitute for the sweep.

## The answer to the filed question (P1 × P2, all 16 rungs × 3 nulls × 3 tilings × 3 cost rungs reported)
`inside_share` = the share of a cell's book-vs-SPY Sharpe comparisons that sit INSIDE their own
two-sided 95% band, i.e. the share the data cannot call. Pooled over the 12 committed 4b passes,
OVERLAP21, 10 bps, ANALYTIC null, by block length in months:

| 6 | 9 | 12 | 15 | 18 | 24 | 30 | 36 | 48 | 60 | 72 | 96 | 120 | 144 | 180 | 211.6 (full) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| .9793 | .9832 | .9912 | .9898 | .9854 | .9738 | .9693 | .9583 | .9441 | .9079 | .8631 | .8046 | .7373 | .6875 | .6458 | **.5833** |

**No rung crosses 0.50 — including the entire 4,443-day scored sample read as ONE block (0.5833:
7 of the 12 books cannot separate their own FULL-SAMPLE Sharpe from SPY's at 95%).** The answer to
"what is the shortest callable sub-window" at 10 bps is therefore **longer than 17.6 years**, which
is not a constant PROTOCOL can carry. DISJOINT (idea 839's tiling lesson) and OVERLAP63 give the
same 0.5833 at the full rung and never cross either.

## Why the constant does not exist (four independent reasons, all pre-registered)
1. **H_CONST FAIL.** L* is defined (any rung < 0.50) at only **5 of 12** books; among those it spans
   1,512d (72mo, K6) to 4,443d (211.6mo, K5), **ratio 2.94**. Spearman(|full-sample dSharpe|, L*) =
   **−0.8996** — L* is a property of the size of the gap being tested, not of the calendar, so it
   cannot be published as a length.
2. **H_MONO FAIL at 12 of 12 books.** inside_share RISES from 6 to 12 months before falling (pooled
   .9793 → .9912), so 6-month blocks are called MORE often than 12-month ones. A threshold crossing
   read from below picks 6 months for the wrong reason: fat-tailed small-sample z, not resolution.
3. **The answer moves with the null and with the cost rung, neither of which is a tuned dial.** At
   10 bps: ANALYTIC never crosses (min .5833), **BOOTSTRAP crosses at 144 months (.4965)**, PERM
   never (min .9618) — **H_NULL FAIL, 8 of 12 books agree within one rung**. Across PROTOCOL's own
   reported cost rungs the ANALYTIC pooled curve goes 0 bps **crosses at 144 months (.4350)**,
   10 bps never (.5833), 25 bps never (.7500). **H_TILE FAIL** — OVERLAP21 and DISJOINT agree
   within one rung at 11 of 12 books; **K4 does not** (L* 2,520d overlapping vs 4,443d disjoint,
   three rungs apart), so the tiling alone can move a per-book answer by a factor of 1.76.
4. **H_WF FAIL for the strongest reason — the quantity is not selectable in sample.** On IS blocks
   (ending ≤ 2016-12-31) the minimum inside_share is **0.9514** at the longest IS-feasible rung
   (1,512d); no IS rung crosses 0.50, so rule 8 cannot choose an L at all. OOS minimum 0.8292 at
   2,016d. **0 of 6 pre-registered hypotheses PASS.**

## Both KEEP paths, with 4b's sub-window leg re-read at every block length
| block (months) | 6 | 9 | 12 | 15 | 18 | 24 | 30 | 36 | 48 | 60 | 72 | 96 | 211.6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4b PASS of 12 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 4 | 8 | 11 | 11 | 11 | 11 |
| 4a PASS of 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**4a is 0 of 12 at every length** (every book's MaxDD is worse than the live book's −12.05%). The
record's 11 committed 4b passes exist only because the halves reading uses ~105-month blocks; every
block length short enough to be a robustness test (≤ 24 months) takes 4b to **0 of 12**, and every
length long enough to be callable (≥ 144 months under the only null that crosses) leaves at most one
block per window, i.e. the clause collapses into the standing full-window Sharpe leg. **There is no
block length that is both callable and shorter than the window, so 4b's sub-window clause cannot be
repaired by choosing a better length.**

## Rule 8 (b) — the mandated book leg, OOS 2017-01-01.. (read once)
OOS CAGR / Sharpe / MaxDD: K1 14.4%/1.130/−18.3, K2 15.2%/1.235/−17.2, K3 13.8%/1.286/−12.4,
K4 12.7%/1.269/−15.5, K5 12.7%/1.278/−15.9, K6 15.1%/1.261/−19.4, K7 6.4%/1.187/−11.1,
K8 **16.0%/1.394/−12.7**, R1 12.0%/1.165/−19.1, R2 12.4%/1.106/−18.7, R3 16.0%/1.215/−20.0,
R4 14.5%/1.040/−19.4. Baseline **LIVE 9.47%/1.2782/−12.05%**; **SPY 15.33%/0.8767/−33.72%**.
Full sample: LIVE 8.63%/1.2018/−12.05% (halves 1.2349/1.1757), SPY 15.16%/0.8861/−33.72%
(0.9595/0.8259). Nothing here is new about any book — the corpus is idea 832's verbatim.

## Declared limitations
- **The PERM null (C9) is conservative by construction**: a 21d-block label swap randomises the SIGN
  of each block's gap rather than removing it, so its null spread scales with the effect size. Its
  "never callable" reading is reported as an upper bound on uncallability, not as evidence; the
  ANALYTIC/BOOTSTRAP pair carries the finding.
- The resampling nulls run on a fixed-seed subsample of ≤ 24 blocks per (book, L) cell, 400 draws;
  cell counts are printed beside every number (12 blocks at the long rungs, so those shares move in
  steps of 1/12).
- SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every level
  is optimistic. The object here is a within-block resolution contrast, which that bias does not
  create.

## What the record should carry forward
Not a constant. The publishable statement is the **curve plus its null**, and the operational
consequence: a book-vs-SPY Sharpe comparison shorter than the full sample is, at the PROTOCOL cost
rung, majority-uncallable at every length swept — so PROTOCOL 4b's sub-window clause is
measurement-free at every length that would make it a test. Ideas 832 (clause inert on the fixed
window, flips 0.1416 of 756d verdicts) and 839 (clause never positively informative) now have their
resolution statement: the clause is not mis-tuned, it is unmeasurable.
