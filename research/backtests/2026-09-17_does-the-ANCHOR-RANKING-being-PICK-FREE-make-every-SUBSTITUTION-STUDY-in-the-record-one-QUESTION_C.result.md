# Idea 1240 (lane C, 2026-09-17) — does the ANCHOR RANKING being PICK-FREE make every SUBSTITUTION STUDY in the record ONE QUESTION?

**ANSWER: NO. KILL (capital) / PREMISE REFUTED.** 9 of 9 gates pass. No RULES change, no book
promoted, no PROTOCOL edit, no memo.

## The identity is confirmed — and generalising it is what kills the premise

1237's G9 read `DELTA(A) == meanOOS(A) - meanOOS(picks)` at **one** pick set. In general, with
cell = (panel, fold) and `w_P(c)` the share of P's picks in cell c:

    DELTA(A, P) = SUM_c w_P(c) * S(A ; c)  -  K(P)

- **G5** verifies this at **8.05e-16** over all 9 x 19 (alternative, pick set) pairs.
- **G6** verifies `K(P)` is constant across alternatives to **1.33e-15** — it is the additive
  constant, exactly as 1237 found.

That same algebra names the **exact** criterion, narrower than 1237's fold-set version:

> **rank-degenerate  <=>  the contrast is MEAN-FORM *and* the two pick sets induce the SAME
> cell-weight vector `w_P`.**

Two escapes therefore exist: **(E1)** a pick set that weights cells differently, **(E2)** a
contrast that is not mean-form. Both are common.

## The criterion is rarely met

9 rule-8-legal pick sets spanning `w` x 19 distinct books x 3 panels x 14 folds → 36 pairs:

| | count | rate |
|---|---|---|
| pairs sharing `w` (→ FORCED under C_MEAN) | 3 of 36 | 0.083 |
| C_MEAN pairs identical **in fact** | 4 of 36 | 0.111 |
| forced pairs that are identical (G7) | 3 of 3 | **1.000, 0 misses** |

Against the record's own text — 34,011 committed units read from 1,164 memo/result files plus
LEADERBOARD rows and CHANGELOG paragraphs:

| study set | units | mean-form share | degenerate share (upper) | UNSTATED share | share if UNSTATED = ALL mean-form |
|---|---|---|---|---|---|
| S_STRICT | 99 | 0.0909 | **0.0101** | 0.4444 | 0.0595 |
| S_BROAD | 124 | 0.1210 | **0.0134** | 0.4597 | 0.0645 |
| S_ALL | 1092 | 0.1429 | **0.0159** | 0.4597 | **0.0670** (G8) |

The premise needs > 0.50. It misses by ~30x, and **the verdict does not turn on how the
unstated-statistic units are assigned** (G8: the most generous reading still caps at 0.0670).
Pre-declared outcome **(B) NOT ONE QUESTION** fires.

## 1224 is not refuted; its generalisation is

**G9** rebuilds 1224's pick set and replays its committed incumbent rank — **5 of 19**, bit for
bit. What 1224 had was a stable *book*, not a degenerate *ranking*: across the 33 mean-form
pairs whose `w` differs, the incumbent's own rank moves 0 places at **0.545** of them while the
**full** ranking survives at only **0.030**.

## What actually makes the record's substitution studies agree: the statistic

Hold `w` fixed and walk dial 2 instead. 0 of 12 same-`w` non-mean pairs are rank-identical.

| contrast | mean-form | same-w pairs identical | median Kendall tau | median \|incumbent rank move\| | max |
|---|---|---|---|---|---|
| C_MEAN | yes | 3 of 3 | 0.7836 | 0.0 | 3 |
| C_TRIM | no | 0 of 3 | 0.7251 | 1.0 | — |
| C_T | no | 0 of 3 | 0.6199 | 3.0 | — |
| C_WIN | no | 0 of 3 | 0.5088 | 2.0 | 15 |
| C_MED | no | 0 of 3 | 0.4971 | 3.0 | — |

The incumbent ranks **5 of 19 under C_MEAN and 18 of 19 under C_WIN**. The pick set was never
the load-bearing choice; the statistic was, and **0.444-0.460 of every study set names no
ranking statistic at all**. That share, not the degeneracy, is the record's real exposure.

## Rule 8 and both KEEP paths (PROTOCOL rules 4, 8, 9)

Benchmarks: U56 SPY 15.06% / 0.8815 / -33.72% (halves 0.9600/0.8171), OOS 15.15% / 0.8686 /
-33.72%. U56 live RULES v2 8.60% / 1.1982 / -12.05% (1.2332/1.1705), OOS 9.42% / 1.2717 /
-12.05%.

- **66 candidate books, nothing selected on:** 4a **0 of 66**; 4b full 17, 4b OOS 16, **BOTH 15**
  → 12 distinct on 1211's realised-return key, all U56/B136 and all in the standing 2026-09-04
  candidate's neighbourhood. Best: U56 N=15, full 17.07% / 1.1675 / -20.14% (1.2596/1.1091),
  OOS 18.87% / 1.1894 / -20.14%.
- **88 rule-8 rows** (3 panels x 9 pick sets x 5 contrasts; every choice made on folds < 2017
  and IS-window cell Sharpes only, 2017-2026 read once): 4a **0 of 88**; 4b BOTH 9 → 3 books the
  record already holds.
- **Every contrast loses to doing nothing.** Mean rule-8 OOS Sharpe: C_MEAN 0.8281, C_WIN
  0.8461, C_MED 0.8501, C_TRIM 0.8501, C_T 0.8684 — all below the do-nothing anchor's **0.8845**.
  The chooser names the incumbent at **0 of 85** rows.

**Survivorship (rule 9):** U56 (55 names) and B136 (135) are CURRENT constituents; SMALL is the
sub-$2B screen with 51 of 715 tickers dropped for max_1d_move >= 1.0 (664 investable); SPY is
benchmark only. The bias does not cancel out of the OOS levels or the 4b legs, so any pass there
is an upper bound.

**Census reflexivity (defect 1230):** the 34,011-unit count describes the tree as it stood when
this run executed. The degenerate-share figures are ratios far from their 0.50 bar, so no
plausible drift in the denominator reaches the verdict.

## Gates

| gate | value | target |
|---|---|---|
| G1 fast runner == engine.backtest | 2.78e-17 | < 1e-10 |
| G2 live RULES v2 U56 MaxDD == committed -12.05% | -0.120549 | -0.1205 |
| G3 the four anchor keys are ONE book | 0.0 | 0.0 |
| G4 distinct candidate set size | 19 | 19 |
| G5 DELTA(A,P) == SUM_c w_P(c)S(A;c) - K(P) | 8.05e-16 | < 1e-12 |
| G6 K(P) constant across alternatives | 1.33e-15 | < 1e-12 |
| G7 forced => identical in fact | 0 misses | 0 |
| G8 verdict robust to the UNSTATED assignment | 0.0670 | < 0.50 |
| G9 replay of 1224's committed incumbent rank | 5 of 19 | 5 |

## Proposed for the Sunday review (rule 6) — one sentence, nothing more

> A substitution study is rank-degenerate **if and only if** its contrast is mean-form and its
> pick sets share a cell-weight vector; the record meets both conditions at about **one per
> cent** of its claims, while failing to state the contrast at all in **nearly half** of them.
