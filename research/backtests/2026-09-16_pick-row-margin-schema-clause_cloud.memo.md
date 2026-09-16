# PROPOSED PROTOCOL rule 5 clause — MARGIN ON EVERY PICK ROW (proposed, NOT applied; rule 6)

Source: idea 1135, `research/backtests/2026-09-16_should-EVERY-committed-PICK-ROW-carry-its-own-MARGIN-COLUMN_cloud.py`.
Gates 6 of 6. Hypotheses 6 of 6. No book promoted, no KEEP claimed. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.

**Exact PROTOCOL wording proposed** (a schema clause on rule 5's output, forward-only):

> Every published row that names a PICK carries, in the same row, the `margin` that decided it
> (pick minus runner-up, in the chooser's own units), the `spread` of the ladder it was picked
> from (max minus min of that same statistic) and the `n_rungs` it was picked over. A pick row
> without those three is not a published pick: no reader can check it against any floor.

**What it would have cost the record that already exists.** Of 480 committed pick-bearing `.csv`
files (79,508 pick rows), **2 files / 69 rows (0.001)** satisfy the trio today. **45,081 rows
(0.568)** are recoverable with **no re-run** because a sibling file of the same run committed the
per-rung ladder — a column copy, not a computation. **34,358 rows (0.432), across 154 run-stems,
are unrecoverable**: the ladder was never committed, so the only route back is re-running the
script. Requiring the margin alone (no spread, no rung count) moves those to 0.755 / 0.245.
Schema cost is +3.34 MB on a 22.4 MB corpus (0.149).

**What it costs a run that has not happened yet: nothing.** On this run's own 39-book ladder
(2 panels × {N, GROSS}, picks made on 2009–2016 alone, OOS read once) the margin, spread and rung
count are functions of rungs already in memory when the argmax is taken. **Books built to satisfy
the clause: 0.**

**Why it is worth the columns.** On those 12 published picks the median margin is **0.111 of the
ladder spread**, and the U56 GROSS IS-Sharpe pick is decided by **+0.0001 on a spread of 0.0014** —
a number that is invisible unless the row carries it, and that 1100's 0.0145 seed floor would bar.

**Scope limit, stated plainly.** The clause is forward-only. Back-filling the 154 lost run-stems is
a re-run order, not a schema change, and this memo does not propose one; the 0.568 that are
recoverable can be back-filled by a reader from committed files without any re-run at all.

**SURVIVORSHIP (rule 9):** the census layer reads committed text and carries no survivorship
exposure. The 39-book price ladder runs on U56 / B136, current-constituent lists, so its levels are
optimistic and its 4b counts (2 of 12 picks pass 4b full, 0 of 12 pass 4a) are UPPER bounds.
