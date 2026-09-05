# Idea 202 — is-the-inert-cell-a-leaderboard-defect (lane C, 2026-09-05)

**VERDICT: SPLIT. The DEFECT is real, exact, and quantified — 28.6% of idea 191's 4b
headline is the untilted control wearing an overlay label. The proposed INERT FLAG is a
KILL: it is redundant at the LEADERBOARD's own printed precision (precision 1.000, recall
1.000) and it changes no decision (0 of 6 rule-8 picks). What the record needs instead is
one cheaper thing the flag was a proxy for: publish the CONTROL ROW beside every overlay
grid. No new book; no KEEP candidate; RULES untouched.**

Two by-product record defects found on the way and reported rather than swept under:
LEADERBOARD.md is **double-appended** (3034 of 3380 table rows are verbatim repeats, 1517
pairs), and **29.4% of distinct rows publish no numeric CAGR/Sharpe/MaxDD at all**.

## Corpus and reproduction

Idea 191's real grid **rebuilt from source, not read**: 3 panels (U56=55, BROAD136=132,
SMALL439=439) x 3 families (DDCTL/BUDGET/SLEEVE) x 5 thresholds x 2 depths x 2 cost rungs
= **180 real cells** + 3 controls x 2 rungs. Base book fixed at idea 2/78's top-20 EW
composite, gross 0.75, weekly, t+1. Exactly **two tuned parameters** (threshold, depth);
all 180 grid points are in `.cells.csv`.

Reproduction asserted before any new number was read:

| gate | result |
|---|---|
| [a] `fast_backtest` == `engine.backtest`, 3 panels | max\|dret\| 1.388e-17 / 2.082e-17 / 2.776e-17 — PASS |
| [b] 10/25 bps cost identity from one 0 bps run | 1.388e-17 / 2.082e-17 / 2.776e-17 — PASS |
| [c] base CAND-20 weights == idea 78/171 `weights_cand` | **0.000e+00** on all three — PASS |
| [d] RULES v1 on U56 @10bps | 6.45305% / 0.66418 / -13.82780% to every digit — PASS |
| [e] all 180 rebuilt cells == idea 191's published `grid.csv` | max\|dSharpe\| 2.220e-16, max\|dMaxDD\| 8.327e-17, max\|d on-share\| 1.110e-16 — PASS |

**A definitional gap found at gate [e], reported not hidden:** 191's on-share denominator
includes the **54 warm-up rebalances** that cannot move any reported number. Measured on
the evaluation window instead, on-share is up to **5.955pp higher** (always upward, 12 of
90 configs affected, all BUDGET). No configuration fires *only* in warm-up, so the inert
SET is identical under both definitions — the published column is diluted, not wrong.

## T2 — the inertness identity, proven not asserted

Idea 191 *reported* 16 never-fire cells as an aside. It never tested what that implies.

- Cells with on-share exactly 0.0%: **16 of 180** (all DDCTL: U56 at D=0.15 and 0.25,
  BROAD136 and SMALL439 at D=0.25 — the base book's drawdown never reaches the threshold).
- **max |r_cell − r_control| over all 16: 0.000e+00. max |dSharpe|: 0.000e+00.**

So every published number on those rows — CAGR, Sharpe, MaxDD, H1, H2, OOS Sharpe,
pass4a, pass4b — **is the control's number**, to machine zero. The row is not weak
evidence about the overlay; it is zero evidence about the overlay.

The honest superset was tested too: cells that *fire* yet change nothing (BUDGET-half on
an unchanged book, BUDGET-skip on a no-trade date) = **0**; never-fire cells whose returns
nevertheless differ = **0**. In this corpus behavioural inertness and never-firing are the
same set, so the cheap `on_share == 0` test is sufficient. That is a property of this
corpus, not a theorem — the two can separate elsewhere.

## T3 — window inertness: a negative result

A sharper defect was hypothesised and **not found**: a cell firing in-sample but never in
2017-2026 would carry a genuine full-sample on-share and a *control's* OOS Sharpe — and 4b
tests OOS Sharpe. **0 of 180 cells** are window-only inert; all 16 OOS-inert cells are the
never-fire ones. The cheap flag loses nothing here.

## T3b — how much of the parent's headline is the control in disguise

| bar | passes | inert | live | share of headline that is the control |
|---|---|---|---|---|
| 4a | 11 | **0** | 11 | 0.0% |
| 4b | 28 | **8** | 20 | **28.6%** |

The mechanism is exact, not statistical: an inert cell inherits the control's verdict, so
inert passes = (inert cells) x 1{control passes}. Predicted vs observed on all 6
(panel, cost) groups: **exact, 6/6**. The whole contamination sits on U56, the one panel
whose untilted control clears 4b on its own (4 inert cells x 2 rungs = 8). The 4a headline
is untouched precisely because no control passes 4a.

So the defect's size is not a property of overlays at all — it is a restatement of
"the U56 control passes 4b", multiplied by however many DDCTL thresholds were set above
the book's worst drawdown.

## T4 — the decisive test for the PROPOSAL: is the flag redundant?

At the LEADERBOARD's own printed precision (CAGR .1%, Sharpe .2f, MaxDD .1%, H1/H2 .2f,
per `baseline.compare`), asking only "does this row print identically to the control row":

- true positives 16, **false positives 0**, **false negatives 0**
- **precision 1.000, recall 1.000**

Not one of the 164 live cells collides with the control at published precision. The
information a dedicated `inert` column would carry is therefore **already fully present in
the numbers the schema already prints** — provided the control row is printed beside the
overlay rows. That proviso is the real gap: idea 191 published aggregate statistics, not
per-cell rows, so a reader holding its LEADERBOARD entry has no control row to compare
against. The fix is one row, not a new column for every row.

## T4b — the record-wide sweep (the queue's actual ask)

Applying the same printed-precision detector to `research/LEADERBOARD.md`:

- 3380 table rows, but only **1863 distinct lines**: **3034 rows are verbatim repeats**
  (1517 groups, max repeat 2). The file has been double-appended. Collapsed before the
  detector ran, or it would have dominated it (uncollapsed the detector reads 99.1%).
- Of the 1861 parsed distinct rows, only **1314 (70.6%) publish numeric CAGR/Sharpe/MaxDD**;
  the other 547 carry `n/a` or `-` and **no detector can be applied to them at all**.
- Of those 1314: **57 rows (4.3%) in 8 scripts / 27 clusters** share an identical printed
  metric tuple with a sibling row of the same script — the observable signature of one
  book published under several labels. **3 of them carry a KEEP verdict**
  (`2026-09-04_defensive-sleeve_cloud.py`, `2026-09-04_sharpe-bound-book-change_cloud.py`);
  in the latter two cases the label itself says "control", so they are honest.

Duplicate printed tuples are necessary, not sufficient, evidence of inertness — but T4
measured the false-positive rate at 0/164 within a grid, so 4.3% is a defensible upper
bound on how much of the numeric record is a book wearing more than one label.

## T5 — rule 8 walk-forward (parameters on ..2016-12-31, evaluated 2017-01-01.. untouched)

Arms: **S0** do-nothing (untilted control) / **A1** IS-Sharpe pick over all cells /
**A2** IS-Sharpe pick after dropping inert cells (the proposed flag, in action).

| panel | bps | A1 pick | A2 pick | changed | dOOS Sharpe |
|---|---|---|---|---|---|
| U56 | 10 | BUDGET/0.5/skip | BUDGET/0.5/skip | **False** | +0.0000 |
| U56 | 25 | BUDGET/0.05/half | BUDGET/0.05/half | **False** | +0.0000 |
| BROAD136 | 10 | BUDGET/0.2/skip | BUDGET/0.2/skip | **False** | +0.0000 |
| BROAD136 | 25 | BUDGET/0.2/skip | BUDGET/0.2/skip | **False** | +0.0000 |
| SMALL439 | 10 | BUDGET/0.3/skip | BUDGET/0.3/skip | **False** | +0.0000 |
| SMALL439 | 25 | BUDGET/0.3/skip | BUDGET/0.3/skip | **False** | +0.0000 |

**Picks changed in 0 of 6 cases.** The reason is structural: an inert cell can only win an
IS-Sharpe contest if the control wins it, and on none of these six panels/rungs does the
control have the best in-sample Sharpe. Dropping inert cells is therefore free — and
worthless as a selector modification.

Mean OOS Sharpe: **S0 0.7766, A1 0.6555, A2 0.6555 (A2−S0 −0.1211)**. The **eleventh
consecutive do-nothing win** in this project's rule-8 record: the untilted control beats
the IS-selected overlay on every panel at 10 bps (U56 1.1775 vs 1.1026, BROAD136 0.8758 vs
0.6986, SMALL439 0.4997 vs 0.2176), and loses only on U56 at 25 bps (1.0618 vs 1.1303).

OOS references: RULES v1 baseline 0.7471 / 0.5762 / 0.6617 by panel; SPY 0.8820
(CAGR 15.5%, MaxDD −33.7%).

## Both KEEP paths, on every arm's picked book

`4a passes among the 18 picked books: 0/18. 4b passes: 4/18` — and all four are U56: the
do-nothing control at both rungs, and BUDGET/0.05/half at 25 bps, which is the control's
verdict propagated through a near-identical book. Full-sample rows are in the
LEADERBOARD entries; SPY over the same window is CAGR 15.2% / Sharpe 0.89 / MaxDD −33.7%
(H1 0.96, H2 0.83).

**No book from this run is a KEEP candidate, and none was expected to be — this is a
schema audit, not a strategy.**

## What should actually change (for Sunday review, not applied here)

1. **Do NOT add an inert column.** Redundant at published precision (P=1.000, R=1.000) and
   decision-free under rule 8 (0/6 picks changed). This is the eighth proposed schema
   column in the record and the first killed on *redundancy* rather than on noise.
2. **DO publish the control row** in any grid entry that publishes overlay rows. One row
   makes the existing printed numbers sufficient to detect the defect, and it is what the
   flag was really a proxy for.
3. **Maintenance, independent of the above:** LEADERBOARD.md is double-appended
   (1517 verbatim duplicate pairs) and 29.4% of its distinct rows publish no metrics.
   Both are pre-existing and both silently corrupt any record-wide sweep, including this
   one before the repeats were collapsed.

Survivorship: BROAD136 and SMALL439 are current constituents only, no delistings.

Outputs: `.console.txt` `.cells.csv` (all 180 grid points) `.sweep.csv` `.detect.csv`
`.record.csv` `.walkforward.csv` `.leaderboard.txt`.
