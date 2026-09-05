# Idea 112 — 2013 as the IS window's single point of failure — **KILL (as posed) / real finding on G**

Lane C, 2026-09-05. Script `2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py`,
console `…_C.console.txt`, data `…_C.{grid,picks,swaps,deltas,peryear,walkforward}.csv`.

Harness identical to ideas 99/109: 6 overlay grids (sleeve, band, breadth, stop, crypto, gross)
x 2 books (top20, ewall) x 2 universes (u56, broad) x 2 cost rungs (10/25 bps), weekly, next-day
execution = **44 cells / 208 grid points / 164 non-null points**. Tuned: overlay parameter x
dropped year (8 + control); every point of every window is reported. Idea 99's full-IS control
reproduces to the third decimal (pooled mean G −0.058, 82.3% negative, per-grid values identical),
so the two runs are directly comparable.

## The four pre-registered questions

**S4 premise — TRUE.** 2013 is the worst calendar year for overlays in the sample: pooled mean
d = **−0.386** (u56 −0.360, broad −0.417) against a next-worst of 2017 at −0.169, i.e. **2.3x the
runner-up**. Inside the IS window the ranking is 2013 −0.386, 2012 −0.146, 2015 −0.096, 2010
−0.003, 2016 +0.034, 2014 +0.051, 2011 +0.215.

**S1 pick stability — NOT SUPPORTED.** Deleting 2013 from the IS window changes rule 8's pick in
**8 of 44 cells**; the median IS year changes 8.5 and **2011 changes 16**. The pre-registered bar
(strictly most cells AND ≥2x the median) fails on both clauses. 2013 is not the year that selects.
What the test does show is that rule 8's pick is *generically* one-year-fragile: **72 pick changes
across the 8 single-year deletions — 20.5% of the 352 cell-year combinations**, and no year leaves the pick
untouched.

**S2 cost of the swap.** Pooled over all 72 swaps the ex-year pick is **worse** out of sample:
mean ΔOOS Sharpe **−0.014**, worse in 40/72, net 4b **−10**, net 4b-OOS **−9**. 2013's own 8 swaps
are OOS-**neutral** on Sharpe (+0.003, worse in 4/8) but still cost 4 full-sample 4b passes: the ex-2013 picks give up
2.2pp of OOS CAGR for 3.2pp less OOS drawdown. Across the 44 cells the full-IS window beats the
ex-2013 window on 4b (20 vs 16) and 4b-OOS (22 vs 19) while mean OOS Sharpe is unchanged
(1.048 vs 1.049). **Deleting 2013 does not improve rule 8.**

**S3 G survival — FAILS, and 2013 is the only year that fails it.** Pooled mean G goes
**−0.058 → −0.019** (frac negative 82.3% → 68.3%), i.e. **2013 alone carries 66% of idea 99's
in-sample/out-of-sample gap**. The pre-registered survival test (mean G still negative, frac > 0.50,
|mean| ≥ half the full-IS value) passes for 7 of 8 dropped years and fails only for 2013. The
collapse is **entirely the sleeve grid**: G_sleeve **−0.169 → +0.035** (shift +0.204, the sign
flips), while band +0.004, crypto +0.010, breadth −0.013, stop and gross 0.000. By measured label,
defensive points go −0.104 → −0.038 and gross-neutral −0.037 → −0.009; measured-offensive stays
+0.001. The mirror image is 2011, whose deletion makes G *more* negative (−0.101, shift −0.044).

## What this means

- The queue's framing is wrong in the direction it feared and right in a direction it did not
  name. 2013 does **not** drive rule 8's parameter choice, and removing it makes the walk-forward
  strictly worse on both KEEP paths. There is no case for excising it.
- 2013 **does** drive idea 99's headline statistic. "The sleeve is the most rule-8-invisible
  overlay (G −0.169)" is a **one-year artefact**: delete 2013 and the sleeve's gap flips positive.
  The residual, year-robust part of G is the small negative in band/breadth/crypto — an order of
  magnitude smaller than the number idea 99 published, and it survives every deletion.
- The genuinely uncomfortable number is not 2013 at all: **rule 8's pick moves in ~20% of cells for
  every single year you delete, and the deletions are OOS-negative on average.** The selector sits
  on a flat, noisy IS surface. That is an argument for reporting the IS Sharpe *margin* at the pick,
  not for moving the split date.
- **The standing KEEP-4b candidate is untouched.** In its own cell (sleeve / u56 / top20 / 10 bps)
  rule 8 picks f = 0.50 under the full IS window and under **every one of the 8 leave-one-year-out
  windows**; ex-2013 IS Sharpes are 0.815 / 0.884 / **0.953** / 0.933 / 0.582 across f, still an
  interior argmax. Walk-forward unchanged: full 12.3% / 1.180 / −14.3%, halves 1.161 / 1.200,
  OOS 13.6% / **1.261** / −14.3% vs SPY 15.5% / 0.882 / −33.7% and RULES v1 0.649 (OOS 0.699).
  4b PASS, 4a fail (drawdown vs the low-return live book), identical under both IS windows.

## Recommendation to the Sunday review (no RULES change from this run)

1. Amend the idea 99 entry: its per-grid G values are not year-robust; quote G alongside its
   leave-one-year-out range, and strike the "sleeve is the most under-selected overlay" reading.
2. If PROTOCOL rule 8 gains a robustness clause, the LOYO statistic to quote is **pick-change
   count across single-year deletions** (this run: 72/352 cell-year combinations, 20.5%) plus the
   **IS Sharpe margin at the pick**, not a re-derived split date.
3. Do **not** re-cut the IS window to exclude 2013: it costs 4 full-sample and 3 OOS 4b passes and
   buys nothing on mean OOS Sharpe.

## Caveats

Survivorship: both panels are current constituents; the bias is identical across every window and
every dropped year, which is all this run compares. Crypto's IS window is short (BTC from
2014-09-17), so its 2009-2013 deletions are near-no-ops; crypto is shown in and out of every pooled
statistic. Calendar-day index caveat (queue idea 38) applies identically to every point. Sharpe on
a spliced series is mean/std as in idea 89's convention; MaxDD is never taken on a spliced series.
2009 is a partial year (eval starts 2009-01) and is excluded from the per-year d table, included in
the LOYO deletions.
