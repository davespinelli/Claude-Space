# Idea 523 — restate idea 276's 26-file UPPER BOUND on the headline block

cloud, 2026-09-11 · script `2026-09-11_restate-idea-276-s-26-file-UPPER-BOUND-on-the-headline-block_cloud.py`
Console `…_cloud.console.txt` · CSVs `.grid` (64 points) `.census` (headline cell, per file) `.census_raw` `.walkforward` `.keeppaths`

## Verdict: ANSWERED — **the 26 collapses to 1 and the 14 collapses to 1; 24 of the 25-file fall is the SITE defect, only 1 is the ROLE defect the queue named. The 136 does not move with the window at all. No KEEP (4a 0/3, 4b 0/3).**

## Reproduction gate — and a census fact found while passing it

Idea 276's rule, run on idea 276's own tree (`78ab84b`, read from git, regexes **imported**
from its module, never re-typed), returns:

```
files 292 · small 140 · large 266 · cross 136 · cmp 126 · prop 26 · breadth 14   ← published
files 292 · small 140 · large 266 · cross 136 · cmp 126 · prop 26 · breadth 14   ← re-derived
```

**All seven columns exact.** But only after one correction, which is itself worth recording:
run with idea 276's own `…_cloud.result.md` left in the corpus, every column is **+1**
(293/141/267/137/127/**27**/**15**). A census that globs `research/backtests/*.md` **counts
itself** once committed, so a published census number and the same number re-derived from the
record afterwards can never agree unless the census self-excludes. Reported, not silently
corrected. (Idea 682, this session, measured the general corpus-growth channel; this is its
degenerate n=1 case, and it is deterministic rather than drifting.)

## The two defects, priced separately

| block | window | `prop` RAW | `prop` ROLE-FILTERED | `breadth` RAW | `breadth` ROLE-FILT | cross |
|---|---|---|---|---|---|---|
| WHOLE FILE | block | **26** | 25 | **14** | 13 | 136 |
| WHOLE FILE | 400 | 19 | 19 | 11 | 11 | 136 |
| WHOLE FILE | 200 | 18 | 18 | 10 | 10 | 136 |
| WHOLE FILE | 80 | 12 | 11 | 7 | 6 | 136 |
| FIRST 40 LINES | block | 6 | 6 | 4 | 4 | 76 |
| FIRST 40 LINES | 200 | 6 | 6 | 3 | 3 | 76 |
| FIRST 20 LINES | any | 1 | 1 | 1 | 1 | 50 |
| **TITLE+VERDICT** | **200** | **1** | **1** | **1** | **1** | **10** |
| TITLE+VERDICT | block | 2 | 2 | 2 | 2 | 10 |

All 64 grid points (4 windows × 4 block rules × {RAW, ROLE-FILTERED} × 2 corpora) are in
`.grid.csv`.

**Decomposition of the 26 → 1 fall:**
- **ROLE** (the defect the queue named — `breadth60`, `breadth gate`, `disp8` are instruments,
  not panel properties): **removes exactly 1 file** (26→25 prop, 14→13 breadth), and **0**
  once the block is narrowed. The queue's premise (a) is **real but nearly empty.**
- **SITE** (the word must be in the file's headline block, near a panel token): **removes the
  other 24.** This is where the whole overstatement lives.

## What each published bound becomes

- **`prop` = 26 (UPPER BOUND) → 1** at the tightest defensible cell (headline block, property
  within 200 chars of a panel token, instrument spellings removed). Span across the whole
  grid: **1 … 26**.
- **`breadth` = 14 (tight LOWER bound) → 1.** Span: **1 … 14**. The "tight lower bound" was
  not tight: it falls by the same factor as the bound it was supposed to bracket.
- **`cross` = 136 is WINDOW-invariant** (136 at all four windows — the window is about the
  property word, and cross-cap does not use one) **but not SITE-invariant: 136 → 76 → 50 →
  10** across WHOLE FILE / FIRST 40 / FIRST 20 / TITLE+VERDICT.

**So the two numbers idea 276 published side by side are not the same kind of number.** One is
insensitive to the parameter that halves the other. Quoting "136 cross-cap, 26 exposed" as a
pair implies a common denominator that does not exist.

**This mechanically confirms idea 286's semantic read.** Idea 286 read the 14 by hand and
found "only **1** of the 12 headline files puts `breadth` in its own headline as a panel
property". A purely mechanical rule — headline block, 200-char window, instruments stripped —
returns **breadth = 1**. Two independent methods, same integer.

## Today's corpus — the restatement is stable under 2.5× growth

Today's record is **722 files vs 292 (+147%)**. Idea 276's rule now returns cross 452 / prop
**137** / breadth **83**; the tightest cell returns cross 31 / prop **3** / breadth **2**
(ROLE-FILTERED, 200 chars). The *ratio* barely moves: **26→1 is 3.8%** of the loose count,
**137→3 is 2.2%**. The overstatement factor is a property of the counting rule, not of the
corpus size.

## Tuned parameters — 2, all points reported
**P1 window** {80, 200, 400, whole-block} × **P2 block rule** {WHOLE FILE, FIRST 20 LINES,
FIRST 40 LINES, TITLE+VERDICT}, each × {RAW, ROLE-FILTERED} × 2 corpora = **64 points, all in
`.grid.csv`**. The headline is not knife-edged on either: `prop` is 1 at every window inside
FIRST 20 LINES and 1–2 inside TITLE+VERDICT; it is 18–26 at every window on the WHOLE FILE.
The parameter that matters is **P2, and only P2**.

## Rule 8 (PROTOCOL 8) and both KEEP paths — the book axis
IS 2009–2016 chooses, OOS 2017–2026 read once. U56, 10 bps, weekly, next-day.

| book | CAGR | Sharpe | MaxDD | H1 / H2 | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| RULES v2 (live) | 8.61% | 1.1998 | −12.05% | 1.2349 / 1.1718 | 1.1043 | 9.45% | **1.2747** | −12.05% |
| RULES v1 | 6.36% | 0.6554 | −13.83% | 0.6472 / 0.6662 | 0.5547 | 7.54% | 0.7309 | −13.83% |
| SPY | 15.11% | 0.8835 | −33.72% | 0.9595 / 0.8211 | 0.8986 | 15.24% | 0.8721 | −33.72% |

**4a 0 of 3, 4b 0 of 3.** RULES v2 clears 4b's Sharpe legs in both halves and OOS and clears
the DD cap (−12.05% vs bar −20.23%) but **fails the CAGR floor: 8.61% against 0.70 × 15.11% =
10.58%.** No KEEP, no memo, no RULES change. This idea is a prose audit and carries no
tradable claim; the book block is reported because PROTOCOL requires it, not because the idea
proposes a book.

## Caveats
The census is keyword-and-position, not semantic — `near()` measures character distance, which
is a proxy for "is about". The TITLE+VERDICT block rule depends on files carrying a
recognisable verdict line; files without one fall back to their first 3 lines, which biases
that column **down**, so `prop = 1` is a floor, not a point estimate. Idea 276's `PROP_TOK`
includes `\bdisp\b` and `\bcorr\b`, which also appear as code identifiers; the ROLE filter
removes parameterised spellings but not bare ones. Survivorship: the book block uses U56
(current constituents); the census carries no market exposure.

## For the queue
PROTOCOL has no rule about WHERE in a file a claim must live for a census to count it, and
this run shows that choice moves a published bound by 26×. Any future census in this record
should state its block rule and window in the same breath as its count — and should
self-exclude, or say that it did not.
