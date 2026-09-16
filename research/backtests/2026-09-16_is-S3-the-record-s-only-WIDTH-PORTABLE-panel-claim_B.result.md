# Idea 689 — is-S3-the-record-s-only-WIDTH-PORTABLE-panel-claim (lane B, 2026-09-16)

**ANSWERED: NEITHER.** Width-portability is not a property of the REVERSAL form and not a
property of the RATIO form. It is a property of **how finely a statistic resolves**, and on a
re-drawn panel pool **S3 is not width-portable at all**.

Script: `2026-09-16_is-S3-the-record-s-only-WIDTH-PORTABLE-panel-claim_B.py`
Grid: 73 panels (q × k ladder) → 3 supports × 21 statistics = 63 classifications, 438 book
rows, 60 rule-8 selector rows. 2 tuned params (statistic form, k). Every point is published in
`.decomp.csv` / `.portability.csv` / `.books.csv` / `.walkforward.csv` / `.reproduction.csv`.

---

## 0. The reproducibility defect, reported before anything else

Ideas 525 and 685 both ran on `SMALL 439, BSTK 100, calendar .. 2026-09-04 (4194 days)`. On
today's committed caches the same code reads **SMALL 663** (715 screened names less 52 with
`max_1d_move >= 1.0`) on a calendar to **2026-09-11 (4198 days)**. `data/prices_small.csv.gz`
has been re-cached and the sub-$2B screen has grown by **+51.0%** of its names, so
`rng.choice(s_stk, size=q*k)` draws a different column set at every q > 0 cell however
identical the seed and the loop order. A 1e-9 replay of the parents is impossible.

**G0POOL (reported).** The 10 q=0.00 panels draw no small-cap name, so their column sets *are*
byte-identical. On today's longer calendar they still move: max |ΔS3| **0.100** (1 of 10 panels
moves at all), |ΔEW_Sharpe| 7.17e-03, |ΔEbar| 8.74e-03. S3 is a sign-of-difference share over 10
n-pairs, so four extra trading days flip one pair and move it by exactly 1/10.

**G0CAL (reported — and this run's second reproducibility finding).** Those same q=0.00 panels,
re-run with the price frame truncated to the parents' own last day (2026-09-04), still do **not**
recover their numbers: |ΔS3| 1.00e-01, |ΔEW_Sharpe| **1.56e-03**, |ΔEbar| **1.20e-03**,
|Δbreadth| 3.01e-05. Ebar and EW_Sharpe both **exceed the record's own record-unit bar of 1e-3**
(idea 515), so `data/prices_broad.csv` has been restated in VALUE, not merely extended in length
— idea 513 measured that drift at ~1e-5 for `data/prices.csv`; on these panels it is two orders
of magnitude larger. **The parents' committed numbers are not recoverable in this sandbox at any
bar tighter than ~2e-3 on a continuous quantity, or one grid step (0.100) on S3.**

**G0DET (asserted, PASS).** One q=0 panel measured twice in-process returns **0.0e+00** on every
book statistic, every panel measure and S3. This run's code path is deterministic, so every
residual above is attributable to the DATA and not to the measurement.

**Ladder cache, declared not hidden.** The 73-panel ladder is a pure function of the committed
caches and the two seeds, so the script reuses its own committed `.panels/.stats/.books` CSVs
when they name exactly the panels it built. A fresh checkout has none and recomputes all 73
(~1,030 s); deleting the three files forces a recompute; G0DET re-measures a panel from scratch
on every run regardless.

Because the pool re-draw is exactly what idea 689 is testing, the re-measurement of 685's five
statistics is **reported, never asserted** — aborting on it would be refusing to publish the
answer.

## 1. KILL — 685's headline does not survive a re-draw of the panel pool

Idea 685's committed verdicts, and the same five statistics re-measured here on today's pool,
under 525's own pre-registered bar (|mean within-slice ρ| ≥ 0.30, sign in ⌈8/11·L⌉ levels):

| statistic | committed B / N / W | re-measured B / N / W | held |
|---|---|---|---|
| S1 ρ(n, OOS Sharpe) | breadth / breadth / JOINT | breadth / **n_elig** / breadth | 1 of 3 |
| S2 INV-vs-NONE overlap | JOINT / JOINT / n_elig | JOINT / **n_elig** / n_elig | 2 of 3 |
| **S3 Sharpe-vs-CAGR reversal** | breadth / breadth / **breadth** | breadth / breadth / **NULL** | **2 of 3** |
| S4 argmax_n premium | breadth / NULL / breadth | **n_elig** / **n_elig** / **NULL** | 0 of 3 |
| S5 fixed − adaptive | NULL / NULL / NULL | NULL / NULL / NULL | 3 of 3 |

**8 of 15 verdicts hold across the re-draw; mean |Δβ_logbreadth| = 0.143.** S3's betas move
`+0.692 / +0.581 / +0.520` (committed) → **`+0.619 / +0.392 / +0.270`** (re-measured), and its
WIDE verdict falls out of `breadth` into `NULL`. **On today's pool ZERO of the five statistics
carry a non-null verdict identical on all three supports** — S5 is identical everywhere and says
nothing, which is the whole reason "S3 is the ONLY portable claim" was a true sentence in 685's
memo. The claim idea 689 was sent to generalise is a property of one draw of one pool, not of
the statistic.

A defect found and fixed inside this run, reported because the record cares: the first cut of
`.portability.csv` labelled its beta columns **by position**, but `DataFrame.pivot` sorts support
columns alphabetically (NARROW, WIDE, laneB) rather than in the order the supports are declared,
so every published beta was attached to the wrong support. The committed script now indexes those
columns **by name**, and the console prints them beside each verdict so the labelling is checkable
from the artifact itself.

## 2. The queue's question, on the matched 16-statistic family

4 of 16 are WIDTH-PORTABLE (same verdict on all three supports, and not NULL):

| portable | form | kind | verdict | β_logbreadth B/N/W | spread |
|---|---|---|---|---|---|
| LV_CAGR | LEVEL | plain | breadth | +0.897 / +0.710 / +0.716 | 0.187 |
| LV_DD (\|MaxDD\|) | LEVEL | plain | JOINT | −0.518 / −0.522 / −0.567 | 0.048 |
| RA_CALMAR | RATIO | plain | breadth | +0.874 / +0.717 / +0.726 | 0.157 |
| RL_SHARPE_ARET | RATIO | reversal | breadth | +0.626 / +0.358 / +0.284 | 0.342 |

- **H_S3UNIQUE FAIL.** S3 (`RL_SHARPE_CAGR`) is not in the portable set; four other statistics
  are. The uniqueness claim is a small-family artefact **and** a single-pool artefact.
- **H_FORM FAIL, and the direction is the finding.** RATIO-form portable **2 of 10 = 0.200**
  against LEVEL-form **2 of 6 = 0.333**. The dimensionless reading predicted ratio ≥ 2× level;
  level ports *more often*.
- **H_REV FAIL, same way.** REVERSAL portable **1 of 8 = 0.125** against PLAIN **3 of 8 =
  0.375**. The reversal form ports **3× less**, not more.
- **H_SIGN FAIL at 0 of 4.** No ratio×level reversal reproduces S3's signature
  (β_logbreadth > 0 and |β_logk| < 0.25·|β_logbreadth|) on 3 of 3 supports — S3 itself no
  longer does either.
- **H_DIM FAIL, and it fails exactly where the width extends.** Median |β_logk| RATIO vs LEVEL
  reads **0.075 vs 0.234** on lane B and **0.063 vs 0.214** on NARROW — the dimensionless
  reading holds on both 2.5× supports — and **inverts to 0.270 vs 0.211 on WIDE**. Ratios look
  width-insensitive only while you never look at much width.

## 3. What DOES port — the mechanism, reported not pre-registered

The portable four are the finely-resolved statistics. Over the 51 WIDE panels:

| class | distinct values taken | mean β_logbreadth spread |
|---|---|---|
| plain (8) | **51 of 51** on every one | **0.196** |
| reversal (8) | **4 to 11** | **0.278** |

(Labelled sensitivities, not the headline: verdict-identical including NULL = 6 of 16;
β_logbreadth spread ≤ 0.30 = 12 of 16.)

A reversal share over 10 n-pairs lives on a grid of 0.1 — `RR_SHARPE_SORTINO` takes four
distinct values across the whole ladder. A rank regression fitted on a statistic with eleven
possible values is estimating a slope from a variable that is nearly constant, and its verdict
is correspondingly fragile to which panels are in the support. **S3 was never stable because
it was a reversal or because one side was a ratio; it was stable because 685's particular 51
panels happened to land its coarse grid the same way twice.** This also explains G0POOL: four
extra trading days move S3 by a full grid step (0.100) on a byte-identical panel.

## 4. PROTOCOL rule 4 — both KEEP paths, every book row, 10 bps, next-day execution

| support | 4a vs RULES v2 | 4b vs SPY |
|---|---|---|
| lane B (q∈[0,1], k≤100) | **0 of 348** (0.000) | 21 of 348 (0.060) |
| NARROW (q≥0.5, k≤100) | **0 of 216** (0.000) | 1 of 216 (0.005) |
| WIDE (q≥0.5, k≤400) | **0 of 306** (0.000) | 1 of 306 (0.003) |

**4a is 0 of 870 rows.** All 21 4b passes sit at **q ≤ 0.50 and k ≤ 100** — the large-cap-heavy,
narrow corner that the q ≥ 0.5 envelope of NARROW/WIDE almost entirely excludes. On WIDE the 4b
rate is 0.019 at k=40 and **0.000 at every one of k = 60, 80, 100, 200, 400**, and 0.020 on
CAND-20 against 0.000 on CAND-5/10/15/30 and EWall. Benchmarks on the common sample: SPY CAGR
14.06%, Sharpe 0.858 (H1 0.914 / H2 0.834), MaxDD −33.72%; RULES v2 Sharpe 0.862 (0.990 /
0.749), MaxDD −12.80%. Mean CAND-20 book over all 73 panels: CAGR 8.06%, Sharpe 0.685, MaxDD
−22.47% — **no arm here is a capital candidate, and none is proposed.**

## 5. PROTOCOL rule 8 — walk-forward, panel statistics from 2010–2016 only, 2017+ read once

Six selectors × 5 book sizes × 2 choice sets = 60 picks. OOS means:

| selector | OOS CAGR | OOS Sharpe | OOS MaxDD | beats anchor | beats v2 | beats SPY |
|---|---|---|---|---|---|---|
| RATIO-SHARPE-MAX | 7.1% | 0.561 | −22.9% | 8/10 | 0/10 | 0/10 |
| RATIO-CALMAR-MAX | 7.9% | 0.665 | −21.8% | 10/10 | 0/10 | 0/10 |
| LEVEL-CAGR-MAX | 8.1–8.7% | 0.639 / 0.661 | −23.4% | 10/10 | 0/10 | 0/10 |
| LEVEL-DD-MIN | 8.1% | 0.635 | −24.0% | 6/10 | 0/10 | 0/10 |
| S3-MAX | 7.8% | 0.589 | −21.4% | 10/10 | 0/10 | 0/10 |
| **S3-MIN** | **13.0%** | **0.981** | **−17.9%** | 10/10 | **10/10** | **10/10** |

against the do-nothing anchor 0.522 (NARROW) / 0.499 (WIDE), RULES v2 OOS ~0.85 (CAGR 6.1%,
MaxDD −13.2%) and SPY OOS 0.877 (CAGR 15.33%, MaxDD −33.72%).

**RATIO-chosen and LEVEL-chosen are indistinguishable OOS** (pooled Sharpe 0.613 vs 0.643,
beats-anchor 18 of 20 vs 16 of 20, beats-SPY 0 of 20 both) —
the forward-looking form of H_FORM fails the same way the classification does. The one selector
that clears every bar is **S3-MIN, and it is not evidence**: its mirror S3-MAX scores 0 of 10
against the same bars, which is the signature of a coin flip on a two-sided dial, and S3-MIN
returns the identical pick on NARROW and WIDE, so the 20 rows are 10 distinct panels. Its OOS
CAGR 13.0% is still below SPY's 15.33%. **PARK the S3-MIN dial, do not promote it.**

## 6. Verdict

**KILL** — of 685's own claim ("S3 is the record's only width-portable panel claim": 0 of 5
statistics are width-portable once the pool is re-drawn, and only 8 of its 15 committed verdicts
hold at all), **KILL** of both readings idea 689
put up (H_FORM and H_REV both fail, and both fail in the *opposite* direction to the
prediction), **KILL** of H_S3UNIQUE, H_SIGN and H_DIM. **CONFIRM** that a width classification
*can* port — 4 of 16 statistics do, all of them finely-resolved — and **CONFIRM** the
resolution mechanism: the reversal class takes 4–11 distinct values where the plain class takes
51, and carries a 42% larger β_logbreadth spread.

Nothing is promoted. No RULES change is proposed. 4a 0 of 870, 4b 23 of 870 and every passer
outside the NARROW/WIDE envelope.

**Recommendation for PROTOCOL (proposed, not applied):** a published panel-property verdict
should state the RESOLUTION of the statistic it is read on — the number of distinct values the
statistic takes over the support it was fitted on. A verdict read on a statistic with eleven
possible values is not the same object as one read on a continuous one, and the record
currently prints them side by side.

**SURVIVORSHIP:** SMALL439/663 and BSTK100 are current constituents of their screens
(`data/SMALL_PANEL_README.md`); every level here is optimistic at the small/wide end, and the
q ≥ 0.5 envelope makes NARROW and WIDE more exposed than lane B. The object under test is which
coordinate of a panel carries a statistic and whether that answer is stable in width;
survivorship reaches it only through the level of the eligible share, not through the k slice.
