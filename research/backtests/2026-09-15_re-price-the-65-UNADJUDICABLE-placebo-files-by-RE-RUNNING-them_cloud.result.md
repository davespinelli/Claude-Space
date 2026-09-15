# Idea 886 (cloud lane, idea 1 of 2, 2026-09-15) — re-price the 65 UNADJUDICABLE placebo files by RE-RUNNING them

**ANSWERED: THE 65 DO NOT NEED RE-RUNNING, AND RE-RUNNING WOULD NOT HAVE WORKED. 880's
"92.9% can never be re-priced" is a FILE-level artefact of a PROSE-matched census.
KILL for capital.** Nothing promoted, no rule changed; `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py`, `baseline.py` untouched (rule 6). Script
`research/backtests/2026-09-15_re-price-the-65-UNADJUDICABLE-placebo-files-by-RE-RUNNING-them_cloud.py`,
wall 878s, deterministic, no network.

SELECTION: the FIRST open entry in QUEUE.md, per the cloud lane's rule.

## Gates — all three pass before any new number is read
| gate | quantity | bar | got |
|---|---|---|---|
| G0a | idea 871's placebo-bearing file census | 70 | **70 PASS** |
| G0b | idea 880's RE-PRICEABLE files | 5 | **5 PASS** |
| G0c | the queue's "65 unadjudicable" | 65 | **65 PASS** |

## The defect, stated before any number was read
871 enumerated files whose **prose** matches the null names; that selects `.py` and
`.result.md` and **cannot** select a per-arm CSV, because a CSV of numbers contains no prose.
880 then opened only the files 871 had named. So "unadjudicable" was never a statement about
what a run committed — only about which of its files contain the word BLOCK.

## H_SIBLING — CONFIRMED
The 70 files collapse to **44 run stems**, of which **34 have a surviving script** (the 10
without are 2 memos, `CHANGELOG`/`QUEUE`/`LEADERBOARD`, and 5 `deepvalue/triage` packs that
match on unrelated prose). Reading every committed sibling artifact of those 34 runs:

- **9 of 34 runs (26.5%) already carry per-arm, seed-bearing placebo cells — 432,709 of them.**
- 880's file-level reading of the same corpus: **5 of 70 files (7.1%)**.

The record's placebo mass was adjudicable all along. It is recovered by **reading**, at
essentially zero cost, not by re-running.

## Both estimators, seed dispersion stored (the queue's instruction, on the recovered corpus)
At the record's own seed budget (10): **12 artifact-columns, 4,896 arms** re-priced from
committed data alone.

- **ABS** median reading **0.0397** against its own seed-noise floor **0.0124** (ratio **8.116**) —
  the ABS estimator still has no zero of its own; it is only adjudicable because the per-arm
  seed dispersion is now stored.
- **SIGNED** sign test over arms: a **determinate sign (|z| ≥ 2) in 9 of 12** artifact-columns.

Seed-budget sensitivity (tuned param 2), every grid point:

| SEED_MIN | artifact-columns | arms | determinate | median \|signed\|/floor |
|---|---|---|---|---|
| 3 | 12 | 5,226 | 10 of 12 | 2.579 |
| 5 | 12 | 5,053 | 10 of 12 | 2.958 |
| 10 | 12 | 4,896 | 9 of 12 | 2.958 |
| 20 | 11 | 2,339 | 10 of 11 | 2.469 |

## H_RERUN — REFUTED, as pre-registered, by actually running the tranche
Static census of the 34 scripts (AST-level, so docstrings cannot trigger a flag): **network-using
0**, **unseeded RNG 0**, **missing committed input 5**, **re-runnable as committed 29 of 34**.
Residual (no committed per-arm cells *and* statically re-runnable) = **21 runs**; **8 attempted**
inside the 900s budget at the 120s cap, **13 never reached**.

- **completed 2 of 8 attempted** (62.8s and 13.0s); **6 timed out at 120s**.
- **per-arm cell files recovered by re-running: 0 (0 cells).** A script that never wrote per-arm
  cells writes the same aggregate again. The queue's proposed route recovers nothing.
- **H_REPRO also fails: 0 of 2 completed re-runs left their committed artifacts bit-identical.**
  Both rewrote committed CSVs. The panels have gained trading days since those runs, so a re-run
  today prices a *different* sample than the committed number — re-running could not adjudicate
  the old claim even if it did emit cells.

Every attempt, its wall time, its byte-level effect on the tree and its restore is printed in
`.rerun.csv`. The tree was restored with `git` after **every** script and verified clean.

## Honest limits
The 120s cap is this run's own choice; 13 residual runs were never attempted, so "0 cells
recovered" is established on 8 of 21, not 21 of 21 — but it is a *mechanical* property of a
script's output set, not a sampling question. `inputs_missing` is a static proxy; the two
completed runs confirm the direction. The 432,709 recovered cells are per-arm differences
between nulls on one fixed real arm at a time; no claim's *verdict* is restated here beyond the
sign counts above — that is the follow-up, now cheap, that this run makes possible.

## RULE 8 on the books (IS-only selector on 2009–2016, OOS 2017–2026 read once, 10 bps, next-day, weekly)
| panel | IS pick | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|
| U56 | RULESV2 | 8.62% / 1.201 / −12.05% | 1.232 / 1.177 | 9.46% / 1.277 / −12.05% | ✗ | ✗ |
| B136 | RULESV2 | 7.98% / 1.099 / −12.24% | 1.235 / 0.966 | 7.88% / 1.106 / −12.24% | ✗ | ✗ |
| SMALL | RULESV2 | 4.30% / 0.664 / −13.89% | 0.806 / 0.555 | 3.75% / 0.560 / −13.89% | ✗ | ✗ |

SPY U56 **15.13% / 0.885 / −33.72%** (OOS Sharpe 0.874); B136 15.16% / 0.886 (OOS 0.877);
SMALL 14.06% / 0.858 (OOS 0.877). RULES v2 live baseline is the U56 row itself.
Unselected base rate over all 18 grid points: **4a 0 (0.0%), 4b 4 (22.2%)** — every 4b pass is a
gross-carried point of the same book family the record has already declined; **nothing proposed.**

SURVIVORSHIP: U56/B136 are current-constituent lists; SMALL is a current-constituent sub-$2B
screen with **52** tickers dropped for `max_1d_move ≥ 1.0`. CAGR and drawdown **levels** are
optimistic on all three. The headline quantity (cells recoverable by reading vs by re-running)
is a property of the committed files and is not exposed to that bias.

## Follow-ups queued
888 (restate the 9 runs' published placebo verdicts under the signed estimator, now that the
cells are recovered), 889 (census the record's ARTIFACT families, not its prose, for every
committed claim class), 890 (is bit-for-bit reproduction of a committed run possible at all
given a growing price panel — and should PROTOCOL require a panel stamp).
