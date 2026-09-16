# PROPOSED PROTOCOL rule 4 clause — BOTH NULL KINDS (proposed, NOT applied; rule 6)

Source: idea 969, `2026-09-16_re-score-EVERY-committed-4b-PASS-against-its-OWN-CELL-s-PER-LEG-NULL-under-BOTH-NULL-KINDS_cloud.py`.
Gates 6 of 8 (both failures are on a clause of their own bar, not on the arithmetic — see below). Hypotheses 5 of 6.
No book promoted, no book KEEP claimed. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched, and idea 998's committed script imported read-only.

**Exact RULES wording proposed** (it completes the clause `2026-09-15_4b-leg-certification-clause_cloud.memo.md` already asks for, and which the record has never actually built):

> A per-leg null base rate is published under BOTH null kinds the certification clause names —
> ROTATING (the basket redrawn every rebalance) and FIXED (the basket drawn once and carried) —
> and the kind is stated beside every number. On the record's own 93 scored cells the two kinds
> are not interchangeable: median null annual turnover runs 8.93 → 1.01 and the per-leg base
> rates move `L_H1` 0.5400 → 0.9900, `L_OOS` 0.3900 → 0.7450, `L_CAGR` 0.0250 → 0.3700, so the
> `L_H1` leg is NON-CERTIFYING in 60.2% of cells under FIXED against 34.4% under ROTATING.
> The ROTATING kind is the EASIER comparand — it pays a churn cost no book pays — so a 4b PASS
> certified against it alone is certified against the weaker of the two nulls the clause names.
> A chooser that reads a null percentile states its kind: `C_ISPCT` picks a different
> (book, gross) in 6 of 9 (panel, cadence) cells on the kind alone, worth up to 0.32 of OOS
> Sharpe. Where a cell is DEGENERATE under one kind it is reported under the other: the FIXED
> kind cures all 17 of the `EWELIG` cells the rotating draw degenerates (idea 998's defect).

**What the record may no longer say:** that a per-leg base rate, a null percentile, or a
percentile-based chooser pick is well defined without naming its null kind.

**What still stands:** idea 998's published numbers, reproduced here EXACTLY on the rotating
kind — every per-leg base rate to max|d| 0.00e+00 and every distinct-draw count to 0 on all 93
shared cells — and its degeneracy finding, confirmed (all 17 degenerate cells are `EWELIG`).

**The two gate failures, stated plainly.** G1 fails only on the `>= 100 shared cells` clause of
its own bar: 93 cells were available because the text corpus shrank between the two runs (see
below), while the reproduction itself is exact. G5 fails only on its monotonicity leg (84 of 93);
all 9 violations are `EWELIG` cells — the same 17 the rotating draw degenerates — where a
half-rotated basket carries names that have left the pool and so churns slightly more than a
fully redrawn one. Its construction leg passes (φ = 1.00 reproduces ROT's per-leg base rates to
0.0450 against 3 MC SE of 0.1061).

**The one hypothesis that PASSED on the wrong statistic, reported as such.** H_KIND's bar is a
MEDIAN |base_ROT − base_FIX| ≤ 0.05 and it reads 0.0200, so it PASSES — but 23.0% of the 465
(cell, leg) points read exactly 0.000 under both kinds, and of the rest **43.2% move by more than
0.05, 39.1% by more than 0.10 and 29.0% by more than 0.25, with a maximum of 1.0000**. The bar
was declared before the run and is scored as written; the distribution beside it says the
opposite, and the clause above rests on the distribution.

**CORPUS NOTE (why this run's harvest is not 998's).** 6,595 claim units / 1,811 asserted 4b
passes / 17 STRICT and 88 WIDE cells here, against 998's committed 6,880 / 1,977 / 17 / 157.
Cause found: commit `b909f86` overwrote `research/CHANGELOG.md` instead of prepending to it,
deleting 1,787 lines, and three later lanes appended to the truncated file. Repaired in commit
`78bfe4a`. The PRICE leg is unaffected and reproduces 900 of 900 ladder rows to 3.55e-15 — the
price record is reproducible, the text record was not.

**SURVIVORSHIP (rule 9):** U56 / B136 / SMALL663 are current-constituent lists (SMALL663 drops
the tickers with `max_1d_move` ≥ 1.0 per `data/small_meta.csv`), so every LEVEL is optimistic and
every 4b count an UPPER bound, most severely on SMALL663. The measured object is a DIFFERENCE
between two nulls drawn from the SAME pool over the SAME tape, so the inflation very largely
cancels; where it does not it raises BOTH base rates together, which pushes BOTH kinds toward the
0.90 bar and so works against the survival counts on both.
