# Idea 513 — three-committed-scripts-fail-their-own-reproduction-gates-today (lane C, 2026-09-09)

**Verdict: ANSWERED / DATA DRIFT, localised to ONE file and ONE panel. Not the environment, not
a genuine reproduction failure. No KEEP-candidate, no memo, no RULES change; RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `2026-09-09_three-committed-scripts-fail-their-own-reproduction-gates-today_C.py`;
console `…_C.console.txt`; artefacts `.rerun.csv`, `.attribution.csv`, `.consoleagree.csv`,
`.census.csv`, `.gatecensus.csv`, `.drift.csv`, `.walkforward.csv`.

## What was run

Idea 483's `sweepstatus.csv` has 81 re-executions: 60 rc 0, **17 rc 124 (that sweep's own
timeout, not a failure)** and **4 rc 1**. The queue says three; there are four. Each of the four
was re-executed once per data vintage — two parameters, both reported at every point, neither
tuned on an outcome:

* **P1 vintage of `data/prices.csv`** — `NOW` (4700 rows, ends 2026-09-08), `TRUNC` (the same
  file cut to 2026-09-04, 4699 rows — isolates the appended row), `OLD` (the file as committed
  at 44bc66f, 4699 rows — the values the four runs published on).
* **P2 the arm** — the 4 scripts in [A], the 10 books in [C].

Children run in-process with `pandas.read_csv` patched to serve the chosen vintage and every
write under `research/backtests/` redirected to a scratch mirror, so no committed artefact is
touched. Same interpreter, same pandas 3.0.5 / numpy 2.4.6, unmodified script code.

## [0] The two drift channels

`data/prices.csv` is the only price file the daily-close job touches, and it does two things:
it **appends** (one new row, 2026-09-08) and it **restates history** — 46 of 58 columns move on
the shared block, max |d| 3.000e-04 in price units (5.094e-05 relative). `prices_broad.csv`
(4699 rows) and `prices_small.csv.gz` (4194 rows) did not move; every affected console.txt
states its panels end 2026-09-04.

## [A] Re-execution, 4 scripts x 3 vintages, all 12 runs reported

| script | NOW | TRUNC | OLD |
|---|---|---|---|
| 402 levered-f-060 | GATE-FAIL | GATE-FAIL | GATE-FAIL |
| 389 MAB-DD-scale | GATE-FAIL | GATE-FAIL | GATE-FAIL |
| 348 U56-6W-m20-c* | GATE-FAIL | GATE-FAIL | GATE-FAIL |
| 440 168c-k-crossing | GATE-FAIL | **PASS (complete, rc 0)** | **PASS (complete, rc 0)** |

The gate quantities, not just the pass/fail:

* **402** `max\|dSharpe\|` on its own EXACT subset (published **4.441e-16**): NOW 3.453e-03 →
  TRUNC 4.076e-06 → OLD 4.636e-06. The rollback removes 99.9% of the gap.
* **348** `c*_FULL` vs committed breakeven, 36 integer cells: NOW **34/36** with both
  mismatches on U56 (`M` 69 vs 68 and **`6W` m20 106 vs 104 — the cell the idea is named
  after**); TRUNC and OLD **36/36 exact**. Its second gate (tol 1e-12, published 2.151e-16):
  OLD 2.152e-05, TRUNC 3.281e-03.
* **389** G6 vs idea 387's `matched.csv` (published 2.842e-14): NOW 8.865e-03, TRUNC 1.931e-03,
  OLD 2.888e-03 — all of it in one bp-scaled column (see [A2]).
* **440** reproduces **334 of 338** committed console lines verbatim at OLD (98.8%) and 119 at
  NOW (35.2%), and completes.

## [A2] Which panel carries it — the decisive table

Joining each re-run's own recomputed artefact against the committed reference its gate reads:

| script | vintage | broad136 / SMALL439 | U56 |
|---|---|---|---|
| 402 vs idea 138's grid | NOW | 6.661e-16 | 6.171e-03 |
| 402 | TRUNC | 6.661e-16 | 7.931e-06 |
| 402 | OLD | 6.661e-16 | 1.031e-05 |
| 389 vs idea 387's matched | NOW | **0.000e+00** | 8.865e-03 |
| 389 | TRUNC | **0.000e+00** | 1.931e-03 |
| 389 | OLD | **0.000e+00** | 2.888e-03 |

**Every panel served by a static cache reproduces at machine precision at every vintage,
today's included; 100% of the failure is on U56, the panel served by `data/prices.csv`.** That
rules out the environment and rules out a code-level reproduction failure. For 389 the residual
after rollback is 1.9e-3 in `dMaxDD_bp` only — 1.9e-7 in MaxDD units, i.e. the column's own
1e4 scaling times restatement noise; every other column collapses to 2.8e-07 or below.

Idea 387's and idea 389's committed `matched.csv` still agree with each other at **0.000e+00**
on all 21 joined cells, so no reference artefact was silently rewritten: the references are
intact and it is the input that moved.

## The residual, stated honestly

Three of four gates do not come back even at OLD, because OLD is not the run-time vintage —
it is the oldest vintage this **shallow clone** can reach (history starts 2026-09-08). The
residual is 4.6e-06 (402), 2.2e-05 (348) and 1.9e-07 in native units (389), i.e. **the size of
one restatement step** ([C] measures that channel at 1.9e-06 of Sharpe), and for 402 OLD is
marginally *worse* than TRUNC (4.636e-06 vs 4.076e-06) — the true run-time file is not
recoverable here. **No re-run of these three can ever satisfy a 1e-9 assertion again.**

## [B] What the record hangs on the four runs

24 LEADERBOARD rows, 0 CHANGELOG references, 34 committed artefacts, 116,532 published CSV
cells and 5 importer scripts other than this one (idea 404-vs-142, the levered-sleeve turnover
run, the MAB half-width run, the exact-per-cell-means run, the N=50 census). Their verdicts are
PARK (402), KILL-of-premise (389, 348) and ANSWERED (440); **none of them is a KEEP and none
feeds RULES.md**, so nothing live rests on the affected numbers.

Record-wide exposure: of **470** committed backtests, **158 carry an assert-style reproduction
gate** (136 with a tolerance ≤ 1e-6, 22 with `==` / `.equals` only), 26 of which read a
committed artefact back. Every one of those is a test of the data vintage as much as of the
code, and every one of them that touches U56 is on the same clock.

## [C] The same drift priced in PROTOCOL units — it is worth nothing

U56, weekly, t+1, 10 bps, eval from 2009-01-13; 10 books x 3 vintages, all 30 points reported
in `.drift.csv`. Channel sizes (max over the 10 books):

| channel | CAGR | Sharpe | H1 | H2 | OOS Sharpe | 4a flips | 4b flips |
|---|---|---|---|---|---|---|---|
| appended row (NOW−TRUNC) | 3.9e-04 | 3.6e-03 | 6.1e-03 | 8.5e-03 | 6.3e-03 | **0** | **0** |
| restatement (TRUNC−OLD) | 2.1e-07 | 1.9e-06 | 5.5e-06 | 1.2e-06 | 8.4e-07 | **0** | **0** |
| both (NOW−OLD) | 3.9e-04 | 3.6e-03 | 6.1e-03 | 8.5e-03 | 6.3e-03 | **0** | **0** |

4a passes 0/30, 4b passes 3/30 — the standing 2026-09-04 candidate (U56 top-20 equal weight,
no vol scaler) at all three vintages: CAGR 11.81%, Sharpe 1.0650, MaxDD −16.51%, halves
1.0809/1.0559 (NOW) and 1.0748/1.0612 (OLD), OOS 13.24% / 1.1329 / −16.51%. Live RULES v2
1.2037 (halves 1.2309/1.1828, MaxDD −12.05%); SPY 15.19% / 0.8871 / −33.72% (halves
0.9587/0.8287, OOS 15.38% / 0.8786 / −33.72%).

**Rule 8** (band chosen on 2009–2016 only, 2017–2026 read once): the pick is `band 0.03` — the
live constant — at **all three vintages**, IS Sharpe 1.1043 identical, OOS Sharpe 1.2817 (NOW)
vs 1.2851 (OLD/TRUNC) against SPY OOS 0.8786/0.8820. The vintage moves no choice and no verdict.

## What this means for the protocol

One trading day of fresh data moves a published Sharpe by ~4e-03 — **economically nil, six
orders of magnitude above a 1e-9 assertion.** An exact-equality gate against a committed
artefact is therefore a test of the data vintage, and it fails by design the first time the
daily-close job runs. Two candidate amendments (NOT adopted here — PROTOCOL is not modified by
this run):

1. Every committed artefact should carry the panel's last date and row count, so a re-run can
   say *which* vintage it is comparing against rather than only that it disagrees.
2. A reproduction gate should be stated as a tolerance in the units the record cares about
   (e.g. |dSharpe| < 1e-3, |dCAGR| < 1e-4) rather than at machine precision — under that gate
   **all four scripts pass today on every panel except U56, and 389/402 pass on U56 too at any
   rolled-back vintage.**

## Caveats

Shallow clone: the true run-time vintage of `data/prices.csv` is unrecoverable, so the residual
is bounded, not eliminated. The mirror redirection is verified by `git status` staying clean
over the 12 child runs. Nothing here is a trading claim; the [C] numbers exist to price the
drift, and they carry the record's standing survivorship caveat on `universe.json`.
