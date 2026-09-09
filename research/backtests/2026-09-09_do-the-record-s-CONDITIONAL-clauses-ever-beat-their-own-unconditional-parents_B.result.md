# Idea 317R — do the record's CONDITIONAL clauses ever beat their own unconditional parents?

**Lane B, 2026-09-09. Verdict: KILL of the PROTOCOL proposal. No new KEEP. Rules unchanged.**

> **A cloud lane ran idea 317 concurrently and pushed first, reaching the OPPOSITE
> recommendation** (`Research cloud: ... KILL of the clause family`, commit `c359077`): it
> proposes the bar as PROTOCOL rule 4c. This run is an independent replication on a different
> corpus and is logged as **317R**. Neither result is withdrawn; see "Reconciliation" below,
> and the addendum script, for exactly where they agree, where they differ, and why. **Both
> recommendations should go to the Sunday review together.**
Two corrections to the record fall out of it.

Script: `2026-09-09_do-the-record-s-CONDITIONAL-clauses-ever-beat-their-own-unconditional-parents_B.py`
Outputs: `.console.txt` `.cells.csv` (288 rows) `.placebo.csv` (576 rows) `.rates.csv` `.walkforward.csv`

## What was run

288 conditional books = 6 clause families x 4 state families x 4 firing rates x 3 panels, each
against **its own two unconditional parents at matched gross**. A conditional book is
`C_t = A_t if RISK-ON at close t else B_t`; A and B are its parents; every one of C, A, B is
rescaled on its WEIGHTS (and re-run, so costs scale too) to the same mean target gross on
rebalance days — G2 asserts the three agree to < 1e-12 and that nothing levers past gross 1.0.

Families (A risk-on / B risk-off): TREND EWall/MA-DG · VOLCAP EWall/VOLCAP-DG ·
WIDEN TOP20/EWall (idea 318's pair) · CONC TOP20/TOP10 (idea 316's pair) ·
GROSS EW@1.00/EW@0.375 · DEFEND TOP20/LOWVOL20.
States (all causal, trailing 5y rolling quantile q, *not* expanding — idea 399): BREADTH, SPYTR,
XVOL, DD. Panels U56 / B136 / SMALL439. Pinned: gross 0.75, weekly, t+1, 10 bps, MA 200d,
vol 20d, cap 0.60, n=10/20. **2 tuned parameters (state, q); all 16 grid points reported for all
18 panel x family cells.** G1: the vectorised runner reproduces `engine.backtest` at **≤ 2.8e-17**
on returns and ≤ 6.7e-16 on turnover across all three panels.

## Result 1 — the bar is passed rarely, and almost never twice

| parents-test leg | pass |
|---|---|
| full-sample Sharpe | **82/288 (28.5%)** |
| H1 alone / H2 alone | 39/288 (13.5%) / 87/288 (30.2%) |
| **BOTH halves Sharpe** | **15/288 (5.2%)** |
| out-of-sample Sharpe | 92/288 (31.9%) |
| full-sample CAGR | 21/288 (7.3%) |
| full-sample MaxDD | 149/288 (51.7%) |

The full-sample rate reproduces idea 48's 4/16 (25%) at 288 cells. But the halves carry almost no
information about each other: P(H2 pass | H1 pass) = 0.385 vs P(H2 pass | H1 fail) = 0.289, and
the observed both-halves rate 5.2% is barely above the 4.09% that independence predicts. **The
both-halves form of the bar is close to a 1-in-20 lottery, not evidence.**

## Result 2 — the placebo: the bar barely separates real conditioning from a shifted mask

Every cell re-run with the same risk-off mask circularly shifted +504 and +1260 trading days —
identical firing rate, near-identical clustering, no alignment with the market state.

| arm | cells | full Sharpe | both halves | OOS | MaxDD |
|---|---|---|---|---|---|
| REAL | 288 | 28.5% | 5.2% | 31.9% | 51.7% |
| PLACEBO +504d | 288 | 17.7% | 1.0% | 20.8% | 29.5% |
| PLACEBO +1260d | 288 | 18.4% | 4.5% | 11.1% | 20.8% |
| **PLACEBO pooled** | 576 | **18.1%** | **2.8%** | 16.0% | 25.2% |
| REAL ex-degenerate | 240 | 23.3% | 4.6% | 24.2% | 42.1% |
| PLACEBO ex-degenerate | 480 | 17.5% | 3.3% | 15.6% | 22.5% |

Lift is **+10.4 pp** on full-sample Sharpe and **+2.4 pp** on both halves (ex-degenerate: +5.8 pp
and +1.3 pp). A book whose conditioning is deliberately pointed at the wrong days clears the bar
roughly **one time in five**. On TREND the placebo actually *beats* the real state (41.7% vs
12.5%). Median Sharpe margin over the better parent is **negative for both arms** — REAL -0.0345,
PLACEBO -0.0492 — i.e. the typical conditional book loses to its own better parent either way.

## Result 3 — idea 48's "0/16 on drawdown" does NOT survive matched gross

At matched gross **51.7% of conditional books beat both parents on MaxDD** (GROSS 48/48,
VOLCAP 38/48, CONC 33/48, TREND 30/48; WIDEN and DEFEND 0/48). Idea 48's drawdown wipeout was an
**exposure artefact**: a de-grossing clause compared against a parent that stays fully invested
must lose on drawdown by construction. Once average exposure is equalised the DD leg is a coin
flip. The record should stop citing "0/16 on drawdown" as a property of conditional clauses.

## Result 4 — a whole clause family cannot be tested this way at all (gate G3)

For GROSS, `max |A_Sharpe − B_Sharpe| = 4.4e-16`: matching gross collapses EW@1.00 and EW@0.375
to **literally the same book**. 48 of 288 cells are therefore a one-parent test, and their 54.2%
pass rate is not comparable with the rest. **Any clause that only moves gross is invisible to the
parents test at matched gross** — a structural limit on the bar, not a result about the clause.

## Rule 8 (walk-forward) and the KEEP paths

(state, q) chosen on IS 2009–2016 Sharpe per (panel, family); OOS 2017-01-01..2026-09 read once.
Picks beat **both parents OOS in 7/18**, beat SPY OOS on Sharpe in 9/18, clear CAGR ≥ 70% of SPY
in 8/18. Median pick: **OOS CAGR 10.38% / Sharpe 0.823 / MaxDD −20.93%**, against
**SPY 15.45% / 0.882 / −33.72%** and **RULES v2 7.98% / 1.119 / −12.24%**. Over all 288 cells the
IS→OOS parents verdict agrees 258/288, overwhelmingly by agreeing on *failure*.

KEEP paths: **4a 0/288** for conditional books and **0/288 for both parents**. 4b: C 83/288 —
but **A 48/288 and B 48/288 too**, i.e. more than half the 4b flags are earned by books with no
conditioning at all. 4b here is a panel fact (0.75-gross equal-weight large-cap clears it on U56
and B136; SMALL439 contributes 0 of the 83), not an idea, so no 4b KEEP is claimed from it.

## The PROTOCOL question, answered

Would the parents bar, placed ahead of 4a/4b, be worth having?

- On the 83 4b passes it would reject **26 (31.3%)** on full-sample Sharpe and **72 (86.7%)** on
  both halves (ex-degenerate: 17 of 56, and 47 of 56).
- What that buys: mean OOS Sharpe of the survivors rises from **1.127 → 1.223** (ex-degenerate
  1.111 → 1.182; the both-halves form, 1.151 → 1.210 on 9 survivors of 56).

**A screen that discards five of six candidates to move mean OOS Sharpe by +0.07, and that a
deliberately misaligned placebo clears 18% of the time, is not a KEEP precondition.** Recommend
PROTOCOL rule 4 is left as it is. What the run does support, and what is worth adding as
*reporting* rather than as a gate, is narrower and cheap:

> Any book with a state-conditional clause should report its two unconditional parents at
> **matched mean gross**, so the reader can see how much of the book is the conditioning and how
> much is the exposure it happens to run. No pass/fail attaches to it.

(That is a reporting line, not a KEEP path. `RULES.md`, `scan.py`, `bot.py`, `baseline.py`
untouched; PROTOCOL.md not edited — rule changes go through the Sunday review.)

## Honesty / limits

- SURVIVORSHIP: B136 and SMALL439 are **current constituents**; every LEVEL is biased up. All
  claims here are book-vs-its-own-parents differences on a fixed panel.
- The corpus is 6 clause families reconstructed in the record's own book forms, not the literal
  committed scripts; a family the record used that is not one of these six is not covered.
- The placebo is 2 deterministic circular shifts, not a full permutation distribution, so its
  rates carry roughly ±3 pp of sampling noise at n=576. The +2.4 pp both-halves lift is inside
  that band; the +10.4 pp full-sample lift is not.
- `pt_sharpe` is a full-sample statistic and therefore contains the OOS window, so the
  P(OOS | full) = 0.878 figure in the console is contaminated and is not used above.

## Reconciliation with the concurrent cloud run (addendum script)

| corpus | cells | CAGR leg | Sharpe leg | MaxDD leg | ALL3 |
|---|---|---|---|---|---|
| lane B, 6 named clause families, no cash parent | 240 | 7.1% | 23.3% | 42.1% | 2.9% |
| lane B corpus, risk-off parent replaced by CASH | 240 | 9.2% | 15.8% | **0.0%** | **0.0%** |
| cloud run, 30 ordered pairs over a 6-book menu **including cash** | 720 | 4.2% | 6.2% | 8.2% | 0.3% |

The cloud menu admits **CASH** as a parent; lane B's does not. Re-running lane B's exact
machinery with a cash risk-off parent shows why that matters:

- **MaxDD leg and ALL3: fully explained.** Against a cash parent, C must beat a 0.00% drawdown.
  Observed 0/240; the *best* C_MaxDD over all 240 cells is −9.40%. Cash pairs are 10 of the
  cloud run's 30 ordered pairs, so **a third of its 720 cells cannot pass ALL3 by construction**,
  and its 0.3% headline is computed over that corpus.
- **Sharpe leg: NOT explained by cash.** Cash pairs clear it here at 15.8% — *higher* than the
  cloud run's 6.2% — because against a zero-Sharpe parent the leg reduces to a one-parent test.
  The cloud run's low Sharpe leg comes from the rest of its corpus (both orderings of arbitrary
  book pairs, many never run as clauses, crossed with 8 states) rather than from cash. Which
  corpus answers the queued question is a judgement call the two runs made differently; neither
  is an error, and this memo does not claim the cloud number is wrong.

**Where the two runs agree, and both should be believed:** idea 48's "0/16 on drawdown" does not
generalise; no conditional book on any panel clears 4a; conditional clauses beat both parents
rarely, and rarely twice.

**Where they disagree:** the cloud run reads 0.3% ALL3 as grounds for a gate. Lane B does not,
for two reasons it can show: a third of that corpus cannot pass by construction, and — the piece
the cloud run does not have — a **placebo mask clears the bar's legs at 18.1% / 2.8%**, close to
the real rate. A bar that rejects almost everything is not the same as a bar that selects.
