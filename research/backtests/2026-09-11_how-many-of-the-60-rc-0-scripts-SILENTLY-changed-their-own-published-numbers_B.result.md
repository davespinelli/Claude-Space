# Idea 516 — how many of idea 483's 60 rc=0 scripts SILENTLY changed their own published numbers?
lane B, 2026-09-11 · script `2026-09-11_how-many-of-the-60-rc-0-scripts-SILENTLY-changed-their-own-published-numbers_B.py`

## Verdict: ANSWERED — **the silent class is essentially the whole sample: 35 of 36 (97.2%)**

Idea 513 attributed 4 rc=1 gate failures to drift in `data/prices.csv` and stopped there.
The queue's suspicion was that the 60 scripts that exit **rc=0** are not therefore
reproducing. They are not. **rc=0 is not a reproduction claim**, and in this sample it is
almost never one.

## What was run
- The nested **S36** sample of idea 483's 60 rc=0 scripts (ascending its own `secs`) was
  re-executed under **idea 483's own write sandbox, imported from its module and not
  re-typed**, so every write under the repo landed in a scratch mirror.
- **G1** idea 483's `sweepstatus.csv` read not re-typed: 81 scripts, 60 rc=0 / 17 rc=124 /
  4 rc=1 — PASS. **G2** vintage today: `data/prices.csv` ends **2026-09-10** (idea 483/513
  ran on 2026-09-08); `data/prices_broad.csv` still ends 2026-09-04. **G3** `git status`
  identical before and after the sweep — the sandbox held.
- **36 of 36 exited rc=0 again**, none hit the 600 s cap. Idea 483's own runtime column does
  not transfer cleanly (median 48 s today vs its 57 s; one file it recorded at 6.0 s took
  332 s), so a sample ordered by it is ordered by a proxy, which is reported, not hidden.
- 228 (script, artefact) pairs: 192 committed CSV/MD artefacts against their mirror twins,
  36 committed consoles against today's stdout. Console lines are aligned on their
  non-numeric skeleton; **956 of 12,206 committed lines had no twin and are reported
  UNMATCHED, never counted as agreeing**.

## The two tuned parameters, all 42 grid points reported
P1 sample S12/S24/S36 × P2 tolerance {exact, 1e-12, 1e-9, 1e-6, **5.094e-05 = one
restatement step** (idea 513's measured relative restatement of `prices.csv`), 1e-3, 1e-2}
× channel {RESULT, ALL tokens}. Share of scripts moving a number:

| sample | exact | 1e-12 … 1e-3 | 1e-2 |
|---|---|---|---|
| S12 | 1.0000 | 0.9167 | 0.8333 |
| S24 | 1.0000 | 0.9583 | 0.9167 |
| S36 | 1.0000 | **0.9722** | 0.9167 |

**Neither tuned parameter matters.** The RESULT channel (run metadata — wall clock, vintage
dates, the offline notice — removed) and the ALL-tokens channel are identical at every rung
but one, so the result is not a timing artefact.

## Attribution (36 scripts)
| cause | n |
|---|---|
| PANEL DRIFT — recomputed on a moved price cache | **31** |
| CORPUS GROWTH — a census re-scans a record that gained files | 4 |
| REPRODUCES | **1** (`2026-09-05_the-on-share-column_cloud.py`, worst move 4.16e-17) |

Ten artefact pairs are **STRUCTURAL** (the recomputed table changed shape): e.g.
`…the-pool-mean-as-a-leaderboard-column_cloud.claims.csv` 29,630 → 44,294 rows,
`…a-within-cell-DIFFERENCE-curve….census.csv` 41 → 87 rows.

## The exhibit — the two comparands every book in the record is judged against
136 lines mentioning `SPY` or `RULES v2` move by more than one restatement step, in 27 of
36 scripts. From `2026-09-08_is-the-pool-sign-the-whole-selector-story_B`:

```
committed:  SPY full 15.23%/0.889/-33.72% | OOS 15.45%/0.882/-33.72%
today    :  SPY full 15.11%/0.883/-33.72% | OOS 15.24%/0.872/-33.72%
committed:  RULES v2 @10bps 8.66%/1.206/-12.05% | OOS 9.53%/1.285/-12.05%
today    :  RULES v2 @10bps 8.61%/1.200/-12.05% | OOS 9.45%/1.275/-12.05%
```

Its own gate passed **both times** (`fast_backtest vs engine.backtest` 6.939e-18 then, the
same order now) because that gate compares two quantities computed **inside the same run**.
A self-consistency gate is blind to vintage by construction. This is the mechanism.

## The number-level reading (the honest counterweight)
Over **2,461,416** paired published numbers: **3.26%** move by more than one restatement
step (5.23% move at all, 0.47% by more than 1e-2); median move 0.000e+00, q99 7.0e-03.
So the drift is **sparse but almost universally present**: nearly every script contains at
least one moved number, while ~97% of individual numbers are fine. The largest single move
in the run, 7.532, is a **degenerate** ratio column (`C_SPY K_RANDOM`, 1.24e16 → 1.06e17) —
reported, not removed, and the reason the token-level ladder and not the max is the
statistic to read.

## PROTOCOL 4a / 4b — does the drift move a verdict?
Today's bars, U56 @10 bps weekly: RULES v2 8.61% / **1.1998** / −12.05% (H 1.2349/1.1718,
OOS 1.2747); SPY 15.11% / 0.8835 / −33.72% (H 0.9595/0.8211, OOS 0.8721). 4a: H1>1.2349,
H2>1.1718, MaxDD≥−12.05%. 4b: H1>0.9595, H2>0.8211, MaxDD≥−20.23%, CAGR≥10.58%,
OOS Sharpe>0.8721.

Re-adjudicated on 26 artefacts / 153,429 book-rows (an **upper-bound proxy**: any committed
table carrying H1/H2/MaxDD[/CAGR] is read as if those columns were a book's):

- **4a** passes 3,366 → 3,368, **20 row-level flips**
- **4b** passes 14,732 → 14,741, **11 row-level flips**
- **13 of 26 artefacts carry at least one flip**, including a 4a pass appearing from nothing
  in `2026-09-07_two-same-day-runs-disagree-on-D3_B.keeppaths.csv` (0 → 1).

Two calendar days of price drift move **0.59% of 4a passes and 0.07% of 4b passes**. Small
in the aggregate, non-zero at the level a KEEP decision is actually made.

## Rule 8 (PROTOCOL 8), on the census's own axis
Tolerance chosen on the scripts committed **2026-09-04..06 only** (n=18), the
**2026-09-07..09** half (n=18) read **once**. IS picks 1e-12 (the smallest rung at which the
IS share stops falling by >5 pp); **OOS moved share 1.0000 against IS 0.9444** — the census
walks forward, and if anything understates out of sample. Every rung is in
`.walkforward.csv`; the OOS share is ≥0.9444 at all seven.

## Prescription for Sunday review (no RULES change proposed)
1. **`rc=0` must never be quoted as reproduction.** Idea 483's `sweepstatus` column, and any
   census built on it, states only that the interpreter exited.
2. **A self-consistency gate is not a reproduction gate.** Idea 515's 520 assert clauses are
   overwhelmingly of the first kind. A gate that reads only quantities computed inside its
   own run cannot see the panel move under it, which is why 36 of 36 pass while 35 of 36 move.
3. The operative fix is idea 514's, and this run is a second independent argument for it:
   **stamp the panel vintage at compute time**. Without it a committed number cannot be
   checked at all, and this sample shows the checking is not optional.

## Caveats
- One sample of 36 of 60 rc=0 files, ordered by a runtime proxy that does not transfer; the
  24 unsampled files are unmeasured and are not claimed either way.
- `data/prices_broad.csv` and the small panel did **not** move in this window (weekly cache),
  so B136/SMALL439-only scripts are under-represented in the drift count — the 97.2% is a
  statement about a corpus dominated by U56, which is the panel the daily job touches.
- The 4a/4b re-adjudication is a column-name proxy and an upper bound, stated as such.
- SURVIVORSHIP (idea 54): every panel here is current constituents only.
- No book promoted, no memo, no KEEP. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
  `baseline.py` untouched.
