# Idea 269 — back-fill-the-breakeven-column-arithmetically-not-by-re-running (cloud, 2026-09-06)

*(Numbering note: two ideas carry the number 269 in QUEUE.md after concurrent lanes appended
on 2026-09-06. This is the one slugged `back-fill-the-breakeven-column-arithmetically-not-by-
re-running`.)*

**Verdict: KEEP AMENDED (pre-registered branch (b)) — the back-fill is free, but not from the
numbers the queue named. The operational use of the column (Q6) is PARK, not KEEP.**

## Q1/Q2 — the census kills the premise's arithmetic and rescues its conclusion

Every committed CSV under `research/backtests/` (783 files) classified mechanically:

| what the file carries | files |
|---|---|
| a Sharpe column | 256 / 783 |
| a cost-rung column | 381 / 783 |
| Sharpe at **≥ 2 distinct rungs** | **170 / 783** (315,666 rows) |
| a turnover column | 66 / 783 |
| a **volatility** column | **20 / 783** |
| **Sharpe + turnover + vol (the queue's "four numbers")** | **2 / 783** (1,014 rows) |

The two files that carry all four are `2026-09-05_is-075-the-argmax-on-every-corpus_cloud.
ladder.csv` and idea 263's own `.grid.csv` from this morning. **Volatility is the number the
record does not publish** — 64 files carry turnover with no vol beside it.

So the queue's route needs a re-run almost everywhere. But it does not matter, because
`dSharpe(c)` is affine in `c`: **a pair quoted at any two distinct rungs pins the same line
with no turnover and no volatility at all**, `c* = −a/b` from `dSharpe(c) = a + b·c`. That
route is available on **170 files instead of 2**, and it rescues 32 of the 64 turnover-but-no-
vol files outright.

## Q3 — every route reproduces the exact breakeven

Scored against idea 263's exact `c*` (0.05-bps ladder + bisection to 1e-6) on its 138 pairs:

| route | n flipping | median err | p90 err | R² | TP | FP | FN | TN |
|---|---|---|---|---|---|---|---|---|
| `law` (turnover + vol) | 58 | 0.0149 bps | 0.4386 | 0.9996 | 34 | 0 | 0 | 104 |
| `LOW2` (two lowest rungs) | 58 | 0.0076 | 1.2376 | 0.9984 | 34 | 0 | 0 | 104 |
| `HI2` (two highest rungs) | 58 | 0.0199 | 0.6811 | 0.9996 | 34 | 0 | 0 | 104 |
| `OLS` (all rungs) | 58 | **0.0060** | 0.8210 | 0.9993 | 34 | 0 | 0 | 104 |
| `R1025` (the 10/25 pair the record most often quotes) | 58 | 0.0127 | 0.6199 | 0.9995 | 34 | 0 | 0 | 104 |

**All five give 34 TP / 0 FP / 0 FN.** The commonest thing the record already publishes — the
same book at 10 and 25 bps — is sufficient on its own.

## Q4 — the back-fill, run

**87,863 pairs across 75 files** (15 files truncated at MAX_PAIRS = 4000; the truncation is
stated, not fitted). **11,539 (13.1%) have a back-filled breakeven inside 0–25 bps**, and
**50 of 75 files carry at least one flagged comparison.** Median flagged `c*` = 11.5 bps —
i.e. the typical rung-conditional comparison flips *right at PROTOCOL's own 10 bps*.

Highest flagged shares: `is-the-1bp-breakeven-general-to-the-records-null-arms_C.walkforward`
0.444, `scale-free-as-a-corpus-eligibility-rule_C.grid.u56` 0.381, `..grid.broad` 0.297,
`is-the-defensive-class-one-book_cloud.grid` 0.289, `cagr-floor-calibration_B.ladder` 0.285.
By dial: `m` 0.397, `gross_mode` 0.312, `selector` 0.267, `g` 0.244, `n` 0.165, `conv` 0.163,
`book` 0.148 — against `panel` 0.053, `key` 0.042, `seed` 0.031, `window` 0.000.

**Caveat that matters:** these pairs are formed mechanically (two rows differing in exactly one
key column), so they include comparisons no one ever published as a claim. 13.1% is the flagged
share of *formable* comparisons, not of *headline* verdicts.

## Q5 — rule 8 on the corpus

Convention chosen on files dated ≤ 2026-09-05, the 2026-09-06 files read once. On the IS
corpus the conventions agree on the flag for **0.9996 / 0.9998 / 0.9998** of 56,188 pairs, so
`OLS` was chosen and read once on OOS. **OOS flagged share 9.4% (2,565/27,242) vs IS 14.8%
(8,974/60,621).** The *estimator* is stable across the split; the *flag rate* is not — it is a
function of which files a day's lanes happened to commit, so 13.1% should be quoted as this
corpus's number, never as a constant.

## Q6 — the column's operational use: PARK, not KEEP

Pre-registered selector on idea 263's re-simulated 24-book × 3-panel grid (504 points, all
committed): IS ≤ 2016-12-31 argmax at 10 bps, and where the runner-up's back-filled `c*`
against the winner sits inside 0–25 bps, take the **lower-turnover** arm; OOS ≥ 2017 read once
at 10 bps.

| panel | plain IS-argmax | OOS Sharpe | column tie-break | OOS Sharpe | fired? |
|---|---|---|---|---|---|
| U56 | `FWD20gate-none` | **1.162** (CAGR 16.4%, DD −21.6%) | `FWD10@M` | 1.090 (17.1%, −23.2%) | yes (c\* 13.4) |
| B136 | `FWD10@Q` | 0.795 (14.2%, −28.6%) | same | 0.795 | no |
| SMALL439 | `FWD20vs` | 0.319 (3.4%, −29.0%) | `FWD20gate-none` | **0.792** (16.6%, −30.8%) | yes (c\* 16.2) |

Mean OOS Sharpe **0.759 → 0.892 (+0.134)** — but that is **one win, one loss and one no-fire on
three panels**. There is no evidence here that the tie-break is a rule; it is reported because
it was pre-registered, and it is a PARK. Anchors: RULES v1 OOS 0.747 / 0.576 / 0.492, SPY OOS
0.882 (CAGR 15.5%, MaxDD −33.7%).

## KEEP paths (504 book-rung points, all committed)

4a passes **116/504**, 4b passes **85/504** — identical to idea 263's grid, which is the point
(the books reproduce exactly through the imported `book_specs`). At 10 bps the only book
passing **both** paths is `U56 FWD40@M`: CAGR 10.9%, Sharpe 1.194, MaxDD −13.8%, halves
1.183/1.206, OOS Sharpe 1.300 / CAGR 12.1% / MaxDD −13.8%, turnover 2.36×/yr, vs RULES v1 full
0.664 and SPY 0.889. **It is a point of the already-published n × cadence grid, not a new rule,
and is not proposed as one.** Binding 4b clause at 10 bps: DD 43, H2 41, CAGR 37, OOS 34, H1 32.

## Caveats

SMALL439 is the sub-$2B panel with the 44 `max_1d_move >= 1.0` tickers dropped — **current
constituents of the screen only, no delistings (survivorship)**, never pooled with the large
caps. U56 and B136 are current-constituent lists (PROTOCOL rule 9). The affine-in-`c` step is
an approximation whose error is measured in Q3 (median 0.006–0.020 bps on flipping pairs), not
assumed.
