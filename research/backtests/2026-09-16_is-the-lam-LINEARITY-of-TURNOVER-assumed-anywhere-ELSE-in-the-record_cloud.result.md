# 1111 — is the lam-LINEARITY of TURNOVER assumed anywhere ELSE in the record?

**ANSWERED = NO, as written arithmetic. KILL of the record-wide-defect reading; CONFIRM of the
mechanism; CORRECTION to 1106's own "1.75% of peak" envelope.** No RULES change, no book
promoted, no PROTOCOL edit (rule 6). RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py
untouched.

**THE TWO DIALS AND NO MORE (rule 4).** `CLAIM SET` {STRICT, WIDE} x `TOLERANCE`
{0.5%, 1%, 2%, 5%} of peak rebalance turnover. All 8 grid points published. PANEL {U56, B136},
`n` {5, 10, 20, 40} and the lam ladder {0.25, 0.50, 0.75, 1.25, 1.50, 2.00} are COORDINATE
SETS — every rung is reported, none is chosen. Frozen: gross 0.75, max_vol 0.60, W cadence,
10 bps, LAG 1, 20 seeds, 34 bisection steps, warm-up 260 rows skipped as `compare()` does.

**THE CENSUS. 973 committed scripts scanned (this one self-excluded — it quotes the shortcut
in its own regexes). STRICT = 1: only 1106 itself**, the run that found the defect, caught it
with a declared gate and fixed it in the same commit. **The shortcut `matched / lam` is written
down nowhere else in the record.** `WIDE = 14`: scripts that build a DD-match lambda AND commit
a turnover/cost/drag figure — exposed only to a reader who divides. **3 of those 14 carry the
false assertion in prose**, a `gross_rescaler` docstring copied forward saying the turnover path
"is exactly `lam` * the `lam=1` turnover". It is not, and the sentence is the actual carrier.

**THE RE-PRICE. 320 DD-matched nulls + 48 book-ladder points, all published.** `ERR =
matched/lam - raw`: median **+0.0291 turns/yr (+0.045% of raw)**, range [-0.0098, +0.0718];
as a share of peak rebalance turnover, **median 2.00%, max 8.70%** on the nulls and **median
3.07%, max 15.92%** down the book ladder. **1106's headline 1.75% is a point on a distribution
that runs to 15.9%** — a CORRECTION to the envelope, not to the number.

**THE MECHANISM IS THE ONE THE CLOSED FORM NAMES.** `Spearman(|ERR|, |cash sleeve|_max) =
+0.6783`; `Spearman(|ERR|, lam) = -0.9407` (the error is largest where the match pushes lam
furthest from 1, mean |1-lam| = 0.2932). **H_SIGN FAILS: 62 of 320 cells are NEGATIVE.** The
shortcut is not a one-way bias that could be corrected with a constant — it is a cell-dependent
error, which is why only a direct `lam=1` evaluation fixes it.

**MATERIAL BY 1106's BAR, IMMATERIAL IN MONEY.** At tol = 1% of peak, 230 of 320 cells (71.9%)
are flagged; at 5%, 20 (6.2%). In charged cost the whole error is worth **0.291 bps/yr median
and 0.718 bps/yr max at 10 bps** (1.45 / 3.59 bps/yr at 50 bps). Nothing in the record turns on
it, and the single script that performed the arithmetic already publishes the size of the error
instead of asserting the linearity.

**HYPOTHESES 4 of 6.** H_WIDE, H_SIZE, H_SLEEVE, H_MATERIAL pass. **H_EXPOSED FAILS** (STRICT
is empty beyond 1106) and **H_SIGN FAILS** — and the two failures together are the answer.

**GATES 10 of 10 PASS, printed before any result number.** Fast runner NET returns and turnover
== `engine.backtest` post-warm-up at 1.39e-17 / 3.33e-16; rescaler at lam=1 == fast runner at
6.94e-18 / 5.55e-17; the defect itself reproduced (G2 max |tl/lam - t1| = 3.35e-02) and its
named term shown non-zero (G2b |S_p - W_sp|_max = 8.31e-02); live RULES v2 MaxDD == -12.05%;
every book at gross 0.75 exactly. **G1e is a MEASURED note, not a claim of this run's:
`engine.backtest` emits 2 NaN rows at the open** (weights are `fillna`'d BEFORE `.shift(1)`),
so any reproduction gate read on the FULL index returns NaN rather than a difference. This
run's first pass did exactly that and G1 duly failed.

**RULE 8 AND BOTH KEEP PATHS — nothing proposed.** IS 2009-2016 chooses, OOS 2017-2026 read
once. **4a 0 of 8, 4b full 0 of 8, 4b OOS 1 of 8.** The binding leg is `L_CAGR` at **0 of 8**:
the vol-scaled composite at gross 0.75 tops out at 9.84% full-sample CAGR against the 10.57%
floor (70% of SPY's 15.10%). `L_DD` 7/8, `L_H1` 5/8, `L_H2` 2/8, `L_OOS` 2/8. Of the four
declared choosers only `C_SHARPE` on U56 (picks n=40 -> OOS 10.78% / 1.2407 / -13.80%) clears
4b out-of-sample, and it fails the same CAGR leg full-sample, so it is **not a candidate**.
Benchmarks: SPY on U56 full 15.10% / 0.8829 / -33.72%, OOS 15.21% / 0.8711 / -33.72%; on B136
full 15.16% / 0.8861 / -33.72%, OOS 15.33% / 0.8767 / -33.72%. Live RULES v2 8.62% / 1.2007 /
-12.05%.

**SURVIVORSHIP (rule 9).** U56 and B136 are CURRENT-CONSTITUENT panels: every CAGR/Sharpe level
is optimistic and the 4a/4b counts are UPPER bounds. The ERR and sleeve measurements are
within-book on one tape and the bias very largely cancels out of them.

**WHAT SHOULD CHANGE (not a RULES edit; a note for whoever next copies the helper).** Delete the
"is exactly `lam` * the `lam=1` turnover" sentence from `gross_rescaler`'s docstring wherever it
is carried forward, and take raw turnover from a direct `lam=1` evaluation. Both are one line.

Script `research/backtests/2026-09-16_is-the-lam-LINEARITY-of-TURNOVER-assumed-anywhere-ELSE-in-the-record_cloud.py`;
5 CSVs (census 973 rows, reprice 368, grid 8, hypotheses 6, walkforward 8) + console log.
