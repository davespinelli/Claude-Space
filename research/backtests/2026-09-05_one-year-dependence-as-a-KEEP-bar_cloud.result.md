# Idea 98 — one-year-dependence-as-a-KEEP-bar (cloud, 2026-09-05)

**Verdict: KILL the proposed bar as a KEEP gate; KEEP the survival count as a reported statistic.**
Every leave-one-year-out bar tested (ex-best-year, every-year, relative-only) is **REPORT-ONLY** on
the pre-registered walk-forward: applied on 2009–2016 alone, none of them selects books that do
better out of sample, and on universe.json all three admit **zero** books while the status-quo 4b
admits four that go on to average **1.213 OOS Sharpe, 4/4 beating SPY**.

## What was run
Idea 89's LOYO harness (delete a calendar year from the book AND SPY AND v1, chain-link the
remainder, recompute every statistic **and every 4b bar** on the retained days) on **every standing
4b pass the project has**, each reconstructed from its own source script and reproduced against its
published leaderboard row before use:

| book | source | published (u56/broad, 10 bps) | reproduced here |
|---|---|---|---|
| top20 | idea 2 | 12.7% / 1.093 / −18.3% | 12.7% / 1.092 / −18.3% ✓ |
| ew-band3-g085 | idea 84 | 12.8% / 1.140 / −17.1%; 12.6% / 1.060 / −18.9% | 12.8% / 1.135 / −17.1%; 12.6% / 1.062 / −18.9% ✓ |
| EWall | idea 72 | 10.7% / 1.027 / −17.7% (broad) | 10.7% / 1.026 / −17.7% ✓ |
| EWall+vol60dg | idea 94 | 11.6% / 1.130 / −16.9%; 12.4% / 1.140 / −18.7% | 11.6% / 1.133 / −16.9%; 12.4% / 1.138 / −18.7% ✓ |
| top20+50S3 | idea 101 | 11.5% / 1.170 / −13.3% | 11.7% / 1.166 / −13.3% ✓ |
| top20+50S4 | idea 99/101/114 | 12.3% / 1.180 / −14.3% | 11.9% / 1.147 / −14.2% (see note) |

*Note:* the S4 blend's published row was run on the **crypto-included** 58-column u56 panel; this
audit runs every book on the crypto-excluded 56-name panel for comparability. Verified directly:
same code gives 12.3% / 1.180 / −14.3% with crypto, 11.9% / 1.147 / −14.2% without. Also included:
`frac085` (idea 46), `ew-band3` (idea 57), and `v1` as a control.

## (1) The queue's literal question — survival of the single best year
Best year = argmax over calendar years of (book total return − SPY total return).

**10 of 14 full-sample 4b passes survive deleting their own best year** (10 bps, both universes).
**The best year is 2022 for 13 of the 14** (top20/u56 is 2018), mean excess in that year **+11.7pp** —
the project-wide finding that the 4b edge over SPY is, in the main, one bear market avoided, now
confirmed across every standing candidate rather than one book.

| universe | book | best yr | excess | survives? | binding | N_surv (of 18) |
|---|---|---|---|---|---|---|
| u56 | top20 | 2018 | +10.5% | **yes** | — | 18 |
| u56 | frac085 | 2022 | +12.3% | **yes** | — | 18 |
| u56 | ew-band3 | 2022 | +13.0% | no | CAGR | 17 |
| u56 | ew-band3-g085 | 2022 | +12.2% | **yes** | — | 17 |
| u56 | EWall+vol60dg | 2022 | +8.4% | **yes** | — | 17 |
| u56 | top20+50S4 | 2022 | +14.7% | **yes** | — | 18 |
| u56 | top20+50S3 | 2022 | +13.1% | **yes** | — | 18 |
| broad | frac085 | 2022 | +11.2% | **yes** | — | 17 |
| broad | ew-band3 | 2022 | +9.7% | **yes** | — | 17 |
| broad | ew-band3-g085 | 2022 | +8.6% | **yes** | — | 17 |
| broad | EWall | 2022 | +9.8% | no | CAGR | **10** |
| broad | EWall+vol60dg | 2022 | +11.8% | **yes** | — | **18** |
| broad | top20+50S4 | 2022 | +14.9% | no | OOS | 17 |
| broad | top20+50S3 | 2022 | +13.2% | no | H2,OOS | 17 |

Survive **every** year deleted (B2): **5 of 14**. Idea 89's ranking is reproduced: `EWall` is the
weakest standing candidate at **10/18** (idea 89: 10/18), and `top20`/`frac085` are 18/18 on u56.

## (2) The finding that kills the bar — 14 of 16 flips are the BAR, not the book
For every year whose deletion flips a passing full-sample row, the binding constraint's book-side
move is compared with its bar-side move:

| binding | BAR-side | BOOK-side |
|---|---|---|
| CAGR floor (0.70 × SPY) | 6 | 2 |
| MaxDD cap (0.60 × SPY) | **6** | **0** |
| H2 | 1 | 0 |
| OOS | 1 | 0 |

**14 of 16** (idea 89 reported 12 of 14). Every single DD flip is bar-side: deleting 2020 raises
SPY's 60%-of-MaxDD cap by **5.53pp** while the books move 0.68–2.85pp. The relative-only column tells
the same story from the other end — under B3 (H1/H2/OOS vs SPY on the same retained days, absolute
bars checked full-sample only) **every candidate is 18/18 at 10 bps**. All of 4b's one-year
dependence lives in its two absolute bars, and those bars are statements about SPY.

## (3) Walk-forward (PROTOCOL rule 8) — do the bars SELECT? No.
Each bar applied on **2009–2016 alone** (book returns, SPY's bars, and the LOYO deletions all
restricted to IS), the admitted books then evaluated on the untouched 2017–2026 window:

| universe | bar | n admitted | mean OOS Sharpe | mean OOS CAGR | beat SPY |
|---|---|---|---|---|---|
| u56 | **B0** (status quo) | 4 | **1.213** | 13.0% | 4/4 |
| u56 | B1 ex-best-year | **0** | — | — | — |
| u56 | B2 every-year | **0** | — | — | — |
| u56 | B3 relative-only | **0** | — | — | — |
| broad | **B0** | 7 | 1.041 | 11.5% | 7/7 |
| broad | B1 | 7 (identical set) | 1.041 (**+0.000**) | 11.5% | 7/7 |
| broad | B2 | **0** | — | — | — |
| broad | B3 | 5 | 1.062 (**+0.020**) | 11.5% | 5/5 |

Pre-registered bar was +0.05 mean OOS Sharpe on **both** universes. B1 adds nothing (same set),
B2 empties the shortlist, B3 gains +0.020 on broad and empties u56. All three: **REPORT-ONLY**.

The u56 column is the whole argument. Its IS window is 2009–2016 — eight years, four of them
partial for some books — so deleting any one of them makes every candidate miss the levered
absolute bars, and the LOYO gate discards **four books that all beat SPY out of sample by
0.13–0.35 Sharpe**. A bar that costs four true positives to buy zero true negatives is not a bar.

## (4) SPY and both KEEP paths (10 bps, full sample)
SPY: 15.2% / 0.889 / −33.7%, halves 0.957 / 0.834, OOS 0.882. RULES v1 (u56): 6.5% / 0.664 / −13.8%,
halves 0.641 / 0.688, OOS 0.747 — fails 4b on H1, H2, OOS and the CAGR floor, as always.
Of the 14 standing passes, **1 also passes 4a on u56** (`top20+50S3`, 11.7% / 1.166 / −13.3%) and
**all 7 pass 4a on broad**. At 25 bps exactly **two books still pass 4b on both universes**:
idea 94's `EWall+vol60dg` (u56 11.4% / 1.113 / −16.9%, halves 1.137/1.091; broad 12.1% / 1.119 /
−18.7%, halves 1.238/1.006) and idea 84's `ew-band3-g085` (u56 11.9% / 1.061 / −17.2%; broad 11.6% /
0.988 / −19.1%). `EWall+vol60dg` is also the most year-robust book in the run — 17/18 and 18/18 at
10 bps, **17/18 and 18/18 at 25 bps**, against `ew-band3-g085`'s 17/18 and 16/18. That is a stronger
result for idea 94's candidate than anything the bar itself produced, and it is the row the Sunday
review should look at.

## Recommendation to the Sunday review (no file was modified)
Do **not** add a LOYO survival gate to PROTOCOL 4b. Instead, add the diagnostic that this run and
idea 89 both produce, with the decomposition attached:

> Every 4b KEEP must report its **leave-one-year-out survival count** (of the ~18 calendar years),
> its **single best year** (max excess return over SPY) and whether 4b survives deleting it, **and**
> for each failing year whether the flip was book-side or bar-side. The count is **descriptive, not
> a gate**: on 14 standing passes, 14 of 16 flips were the 4b bars moving with SPY, not the book
> weakening, and applying the count as a gate on the in-sample window selects no better out of
> sample (u56 +nan, 0 books admitted; broad +0.000 for ex-best-year, +0.020 for relative-only,
> against a pre-registered +0.05 bar).

## Caveats
Survivorship: both panels are current constituents (levels biased up; identical across every book,
year and window compared). MaxDD on a spliced series is an approximation — a drawdown spanning the
deleted year is shortened — applied identically to book and SPY, so the 4b DD comparison stays
like-for-like (idea 89's convention, kept for comparability). 2009 and 2026 are partial years and are
flagged in `.loyo.csv`. The selection test is 8 candidate books × 2 universes; the per-book detail is
printed so the reader can see it is 0–7 books a side, which is why the u56 zero-admission result,
not the broad +0.020, is the load-bearing evidence.
