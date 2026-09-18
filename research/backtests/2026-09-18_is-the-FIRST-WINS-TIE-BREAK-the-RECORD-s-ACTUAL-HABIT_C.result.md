# Idea 1202 (lane C, 2026-09-18) — is the POINT FORM's FIRST-WINS TIE-BREAK the RECORD's ACTUAL HABIT, or only 1199's ASSUMPTION?

**ANSWERED: FIRST-WINS *IS* THE HABIT (0.9260 of 3,123 committed selection primitives), BUT IT IS
NOT THE STATED-SORT KIND 1199 ASSUMED — 0.8330 of it is CONSTRUCTION ORDER, and 0.1982 of the
corpus's selections run through a NON-STABLE sort whose "first" is not recoverable from the text.
1199's number nevertheless STANDS: its assumed order and the record's construction order are
decision-identical at 12 of 12 (panel, eps) cells. CAPITAL VERDICT: KILL — no new book, nothing
enacted; 4a 0 of 60 grid cells, 4b 8 of 60, rule-8 mean delta vs do-nothing -0.0585.**

## What was run
Two legs, two dials, 12 census cells and 60 capital cells, all published.
DIAL 1 CLAIM SET {C_CODE, C_PICKFILE, C_TEXT}; DIAL 2 TIE DEFINITION eps {0, 1e-12, 1e-6, 1e-3}.
Capital arm is 1199's own object, frozen: `book_weights` (top-N by the 3-leg composite among
names above their 200d MA, equal weight, GROSS 0.75, no vol filter, no min-hold), N in
{5,10,15,20,30,40} x cadence {W,M}, three panels, the record's GROSS-MATCHED ROTATING null
(N names redrawn at every rebalance row), K = 60 draws (frozen — 1203 already walked K),
CH_PCT = share of the null the book beats on IS Sharpe. Artifacts: `.census.csv.gz`,
`.habit.csv`, `.pickfiles.csv`, `.books.csv`, `.grid.csv`, `.walkforward.csv`, `.gates.csv`,
`.console.txt`.

## Gates
G1 fast runner == `engine.backtest` post-warm-up (1.4e-17). **G6 REPLAY: this run reproduces
1203's committed U56 rule-8 leg to 0.0000** — OOS Sharpe 0.9143, anchor 1.1769, delta -0.2626,
OOS CAGR 19.99%, anchor CAGR 15.76% — so the census below is attached to the same object 1199
and 1203 priced, not to a look-alike. G2 a tie exists at eps=0 (11 books). G3 grid complete (60).
G4 conventions decide distinctly (>=2 picks per cell). G5 census non-empty (10,816 rows).

## (A) The habit census — what the record's code actually does
| claim set | n | H_IMPLICIT_FIRST | H_EXPLICIT | H_RANDOM | S_SORTED (of implicit) | S_BUILD (of implicit) | non-stable sort |
|---|---|---|---|---|---|---|---|
| C_CODE (1,160 committed scripts) | 3,123 | **0.9260** | 0.0733 | 0.0006 | 0.1670 | **0.8330** | 0.1982 |
| C_PICKFILE (96 scripts that commit picks) | 320 | 0.9500 | 0.0469 | 0.0031 | 0.2138 | 0.7862 | 0.2125 |
| C_TEXT (7,373 prose claim lines) | 7,373 | 0.9802 | 0.0198 | 0.0000 | 0.0000 | 1.0000 | 0.0000 |

- **First-wins is the habit, not an assumption**: 92.60% of the record's committed selection
  primitives (`idxmax` / `argmax` / `argsort` / `sort_values(...).iloc[0]` / `nlargest(1)` /
  `max(key=)`) resolve a maximum with no tie-break stated at all. Explicit resolution is 7.33%;
  a random draw, 0.06%.
- **But it is the wrong KIND of first-wins.** 1199 wrote the tie-break as an explicit sort order
  (`sort_values(["cadence","N"])`). Only **16.70%** of the record's implicit-first selections are
  preceded by any sort; **83.30%** take whatever order the frame was CONSTRUCTED in — a loop order,
  not a documented one. So the habit is real but undeclared, and 1199 described it as a convention
  the record does not actually write down.
- **A fifth of it is not reproducible from the text at all**: 19.82% of C_CODE selections run
  through a numpy/pandas default (quicksort/introsort) rather than a stable kind. Such a pick is
  deterministic for a given array and library version, but "first in the order" is not what it
  returns by contract, so no reader can recover it from the committed text.
- **Nor from the record's own artifacts**: of the 96 committed `.picks.csv` files, 0.9167 carry a
  candidate statistic and 0.6250 a pick column, but only **0.5729 carry BOTH** — the share on which
  a tie-break is adjudicable from what the record committed. For the other 42.71% the habit is
  unauditable by design.
- **The prose is silent**: 7,373 committed claim lines mention a pick / chooser / argmax; **98.02%
  state no tie-break**. That is the answer to the queue's question in its own terms — the record
  does not break ties by a second statistic and does not say it breaks them by sort order; it
  simply publishes whatever the primitive returned.

## (B) The capital arm — what the habit is worth
Tie sets at eps=0: **U56 10 of 12, B136 11 of 12, SMALL 3 of 12** books tied at the top of CH_PCT
(mean 8.00 of 12), so the tie-break decides the book on every panel. Pooled OOS Sharpe of the pick
over the 12 (panel, eps) cells:

| convention | pooled OOS Sharpe | gap vs O_1199 | what it is |
|---|---|---|---|
| O_HOLD (largest N) | 0.9738 | +0.0922 | control, not a first-wins order |
| O_LAST (last in 1199's order) | 0.9738 | +0.0922 | control, not a first-wins order |
| **O_1199** (`sort_values(["cadence","N"])`) | **0.8816** | 0.0000 | 1199's assumption |
| **O_BUILD** (the record's construction order) | **0.8816** | **+0.0000** | **the census's actual habit** |
| O_IDXMAX (frame row order) | 0.8816 | +0.0000 | the same object |

**O_1199 and O_BUILD pick the same book at 12 of 12 (panel, eps) cells.** The two orders can only
diverge when the smallest-N monthly book leaves the tie set while the smallest-N weekly book stays,
which never happens on these panels. So the ORDER 1199 assumed is harmless, and its committed
-0.0671 is not an artefact of the assumption; the whole 0.0922 spread here is the two CONTROLS,
i.e. it re-confirms 1203's mechanism (whatever points at a broader book wins) rather than 1199's
order. Outcome (1) fires on the class, outcome (3) on the reproducibility.

The eps dial moves nothing: all four tolerances give identical picks on all three panels, because
the tie at the top of a 60-draw percentile is EXACT (many books at 1.0000), not approximate.

## Capital and rule 8 (the verdict)
- **4a: 0 of 36 books and 0 of 60 grid cells** — nothing beats live RULES v2 (full-sample Sharpe
  1.2018 / 1.0994 / 0.7130 on U56 / B136 / SMALL, MaxDD -12.05% / -12.24% / -12.18%) on its own path.
- **4b: 6 of 36 books, and the same 6 also clear the rule-8 OOS leg.** U56 N=15/W (CAGR 16.06%,
  Sharpe 1.170, MaxDD -19.69%, H1/H2 1.240/1.129, OOS Sharpe 1.187), N=20/W, N=30/W, N=30/M,
  N=40/M, and B136 N=40/W — against SPY 15.13% / 0.885 / -33.72% (U56 sample). 8 of 60 grid cells,
  all of them the O_LAST/O_HOLD controls landing on N=40/W.
- **Rule 8 (both dials chosen on warm-up..2016-12-31 by IS Sharpe, 2017-2026 read once):** all three
  panels choose O_1199/eps=0. U56 picks N=5/M -> OOS Sharpe 0.9143, CAGR 19.99%, MaxDD -28.73%
  against the do-nothing anchor (N=20/W held throughout) 1.1769 / 15.76% / -19.09%, **delta
  -0.2626**. B136 picks N=5/M, +0.0401. SMALL picks N=15/W, +0.0470. **Mean delta -0.0585.**
- **The tie-break habit is an anti-selector.** None of the six 4b-clearing books is what any
  first-wins convention selects: the saturated percentile ties the whole ladder, and first-wins
  then lands on the smallest-N book, which is the one that fails. Declaring the tie and resolving
  it by "hold more names" is worth +0.0922 pooled — but that is 1203's finding, already priced,
  and it is a ladder fact (OOS Sharpe rises in N on U56), not a tie-break fact.

## Honest limits
Survivorship (PROTOCOL rule 9): U56 / B136 / SMALL are current constituents only, which flatters
every momentum book here and inflates the null's own level. The census is a CODE census: it
classifies selection primitives by their context (±4 lines) and will misread a selection whose
tie-break lives further away; 0.0733 explicit is therefore a floor, not a point estimate. K=60 is
frozen, so the tie widths are 1203's K=50-100 region and not its K=400 region, where SMALL's tie
set collapses to zero. Nothing here justifies real capital: PROTOCOL rules 6 and the live-tracking
caveat stand, and RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.
