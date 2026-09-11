# Idea 776 — price-the-STAND-DOWN-RULE-on-its-own-as-a-book (cloud, 2026-09-11)

**VERDICT: KILL as a book. The stand-down gate is real but it is a SELECTOR VETO, not capital.**
At its best rung it buys **+0.0080 of mean OOS Sharpe over the incumbent** (0.9951 vs 0.9871
across 12 cells) and **+0.0384 over plain rule-8 selection** (ARGMAX 0.9567), never loses a
cell, and clears **neither KEEP path in 84 of 84 decision books** (4a 0, 4b 0). The single 4b
pass in the whole run belongs to the control that ignores the floor (ARGMAX adopting n=20 on
U56 — the record's own standing 2026-09-04 KEEP-4b book), and **every stand-down rule vetoes
it**, because that book's IS margin against RULES v2 is −0.1114, i.e. negative.

## Construction
Incumbent = RULES v2 (`rules_v2_weights`, band 0.03, gross 0.75, W) on each panel, 10 bps,
t+1 execution, warm-up `px.index[260]`, IS ≤ 2016-12-31, OOS ≥ 2017-01-01 (PROTOCOL 2/3/8).
Four published dial families — GROSS {0.50, 0.75, 1.00}, CADENCE {W, M, Q}, BAND {0.00, 0.03,
0.06}, N {10, 20, 30, 50} (top-n, no vol scaler, vol20 < 0.60) — on U56 / B136 / SMALL439.
Decision at IS_END: challenger = the dial's IS-Sharpe argmax; margin = IS Sharpe challenger −
incumbent; floor = SD of that margin under a moving-block bootstrap (block 21d, B = 400, seed
776) of the paired IS daily rows; **SD(f): adopt iff margin > f × floor, else hold RULES v2.**
Tuned parameters (max 2): f ∈ {0, 0.5, 1.0, 1.5, 2.0} and the dial family. All 48 rungs and
all 84 decision books are in `.grid.csv` / `.walkforward.csv`; nothing is chosen on OOS data.

## Gates (pre-registered, all PASS)
G1 `fast_backtest` == `engine.backtest` **6.939e-18** · G2 `band_book(0.03,0.75)` ==
`rules_v2_weights` **0.000e+00** · G3 SMALL dropped the **44** `max_1d_move >= 1.0` tickers →
440 cols · G4 IS statistics recomputed on a frame TRUNCATED at IS_END **0.000e+00** (the
decision reads no future bar) · G5 floor > 0 in all 9 non-degenerate cells (min 0.0007); **3
of 12 cells are DEGENERATE** — the dial's IS argmax *is* the incumbent (U56 BAND, B136
CADENCE, B136 BAND) — so the decision there is a no-op whatever f is.

## The answer (12 cells × 7 rules, every point published)

| rule | adopted | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | beats incumbent | ties | loses | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|
| NEVER (pure incumbent) | 0/12 | 0.9871 | 7.09% | −12.99% | 0 | 12 | 0 | 0 | 0 |
| ARGMAX (adopt always) | 12/12 | 0.9567 | 8.75% | −16.66% | 2 | 3 | 7 | 0 | **1** |
| SD(f=0.0) = rule-8 selector | 6/12 | 0.9905 | 7.77% | −14.41% | 2 | 6 | 4 | 0 | 0 |
| SD(f=0.5) | 5/12 | 0.9948 | 7.76% | −14.22% | 2 | 7 | 3 | 0 | 0 |
| SD(f=1.0) | 4/12 | 0.9949 | 7.49% | −13.89% | 2 | 8 | 2 | 0 | 0 |
| **SD(f=1.5)** | 2/12 | **0.9951** | 7.17% | −13.19% | 2 | **10** | **0** | 0 | 0 |
| SD(f=2.0) | 1/12 | 0.9915 | 7.14% | −13.17% | 1 | 11 | 0 | 0 | 0 |

**B1 PASS** — SD(f) at f = 0.5, 1.0, 1.5, 2.0 is ≥ the incumbent in a majority of cells and
strictly better in at least one. **B2**: the floor changes the decision in **5 of 12 cells**;
adoption falls 6 → 5 → 4 → 2 → 1 as f goes 0 → 2. **B3**: 4a 0/84, 4b 1/84 (the ARGMAX cell).

Where the edge lives: **both wins are SMALL439** — CADENCE (adopt M, OOS Sharpe 0.6207 vs
0.5680, +0.0526) and BAND (adopt 0.06, 0.6112 vs 0.5680, +0.0431). On U56 and B136 the gate's
whole contribution is refusing trades: every adopted challenger there loses OOS Sharpe
(U56 GROSS −0.0007, U56 CADENCE −0.0521, U56 N −0.1099, B136 GROSS −0.0011, B136 N −0.2153),
so the incumbent's 1.2747 / 1.1185 is never improved on the two large-cap panels by any rung
of any dial. That is the same stand-down direction idea 774's WF-B reported, now priced.

## Reference rows (full sample from `px.index[260]`, halves, OOS)

| panel | book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|---|---|
| U56 | RULES v2 | 8.61% | 1.1998 | −12.05% | 1.2349 / 1.1718 | 9.45% | 1.2747 | −12.05% |
| U56 | SPY | 15.11% | 0.8835 | −33.72% | 0.9595 / 0.8211 | 15.24% | 0.8721 | −33.72% |
| B136 | RULES v2 | 8.03% | 1.1058 | −12.24% | 1.2291 / 0.9844 | 7.98% | 1.1185 | −12.24% |
| B136 | SPY | 15.23% | 0.8890 | −33.72% | 0.9566 / 0.8340 | 15.45% | 0.8820 | −33.72% |
| SMALL439 | RULES v2 | 3.81% | 0.5725 | −14.68% | 0.5699 / 0.5770 | 3.85% | 0.5680 | −14.68% |
| SMALL439 | SPY | 14.13% | 0.8615 | −33.72% | 0.8907 / 0.8577 | 15.45% | 0.8820 | −33.72% |

## Why this is a KILL and not a PARK for capital
The gate cannot manufacture return: by construction its book is either the incumbent or a
challenger the incumbent's own dial already contains, so its best case is the incumbent's
9.45% / 8.0% / 3.9% OOS CAGR against SPY's 15.2–15.5%. **4b's CAGR floor (≥ 70% of SPY) is
failed by the incumbent on all three panels**, and the gate inherits that whole. The +0.008
mean-Sharpe edge is two cells on the weakest panel read once; 10 of 12 cells at f = 1.5 are
literally the incumbent's own returns.

## What is worth carrying forward (no PROTOCOL edit made here)
The floor is *not* inert as a **selection discipline**: monotone in f up to 1.5, it removes
every losing adoption that plain rule-8 selection (SD(f=0) — the record's standing practice)
makes, at the cost of the one 4b pass. Stated as a number a Sunday review could act on:
**plain rule-8 selection loses 4 of its 6 adoptions OOS; SD(f=1.5) loses 0 of its 2.**
`RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and `baseline.py` are untouched.

## Caveats
SURVIVORSHIP (idea 54): U56, B136 and SMALL439 are current-constituent panels with no
delistings, so every CAGR level is inflated and both KEEP columns inherit that; SMALL439 is
the current sub-$2B screen with the 44 `max_1d_move >= 1.0` names dropped. One decision per
cell, one OOS window: 12 decisions are not 12 independent experiments, and the two wins share
a panel. The record's convention keeps SPY as an investable column in each panel (as
`rules_v2_weights` does) and that is kept here so the incumbent is the live book verbatim.

Artefacts: `.grid.csv` (48 dial rungs), `.decisions.csv` (12 decisions with margin and floor),
`.walkforward.csv` (84 decision books), `.reference.csv`, `.console.txt`.
