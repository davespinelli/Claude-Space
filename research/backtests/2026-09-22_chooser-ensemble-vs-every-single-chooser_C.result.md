# Idea 2105 — does a CHOOSER ENSEMBLE beat EVERY SINGLE CHOOSER out of sample?

**Lane C, 2026-09-22.**  **ANSWERED = NO on the claim as filed, and the panel-stability half is
refuted in the WRONG DIRECTION.  An ensemble over the six legal IS-only choosers is a MEDIAN
MEMBER, not a dominator: it beats the best single member on `0 of 9` (panel x family) cells on
OOS percentile (`1 of 9` on 4b reach), and its mean rank among the seven rules is `3.4-4.4 of 7`.
Its 4b REACH is the one place it earns its keep — mean rank `2.0-2.4 of 7`, pooled reach
`0.2637` against the member mean `0.1803` and a uniform coin's `0.1573` — but it is LESS
panel-stable than its own members, not more: the U56-vs-B136 spread of 4b reach runs `0.1705`
for the five ensembles against `0.1020` for the six members, and the ensemble is the wider one
in all three families.  KILL of the ensemble as a rule-8 device.**  One by-product is
capital-relevant and is written up below: **a both-paths cell, `B136 / TURNBUDGET / t = 0.08,
B = 3.0`, KEEP-candidate on path 4b** (and on 4a against the panel-matched live book), reached
by two of the five ensembles and by two members.

Script: `2026-09-22_chooser-ensemble-vs-every-single-chooser_C.py` (companion
`..._C.verify.py`).  Grid `.grid.csv.gz` (**11,280 (panel, family, draw, cell) rows, all
published**), per-draw picks `.picks.csv` (7,191 rows), per-cell chooser table `.choosers.csv`,
`.v1.csv`, `.members_beaten.csv`, `.stability.csv`, `.clean_picks.csv`, `.costladder.csv`,
`.votes.csv`, gates `.gates.csv`, console `.log.txt`.

## What was priced

2087 left the chooser machinery with a **157x selection width** on one grid and no panel-stable
best member.  This run asks the obvious follow-up: does aggregating the members fix it.

**THREE FAMILIES x THREE PANELS, one selection problem per (family, panel, draw).**
`TURNBUDGET` (2087's own grid: equal weight, `g = clip(t/sigma20, 0, 1)`, MONTHLY trade, annual
turnover budget `B`; `t` x `B` = 30 cells), `BANDGROSS` (RULES v2's family: equal weight at
`gross/N`, 200d MA band with hysteresis, gated weight de-grossed to cash, WEEKLY; band x gross =
25 cells), `TOPN` (the 2026-09-04 KEEP-4b family: top-`n` momentum composite, no vol scaler,
equal weight at `gross/n`, WEEKLY; `n` x gross = 25 cells).  Panels U56, B136 and SMALL, each
re-priced on seeded admission haircuts at depths `{0.10, 0.20, 0.30}` (20 draws per depth on
U56/B136, 6 on SMALL) plus the clean panel: **61 + 61 + 19 = 141 selection problems per
family**, everything (equal weight, sigma20, the ranks, the band) rebuilt on the survivors.

**TWO TUNED DIALS, every value reported.**  AGGREGATION `{MEANRANK, MEDRANK, VOTE}` and VOTE
THRESHOLD `k in {2, 3, 4}` (below `k` the vote falls back to MEANRANK), over the six informative
members `IS_SHARPE, IS_LEGS, IS_CALMAR, IS_MINMARG, IS_CAGRSLACK, IS_DD`.  Reported, not tuned:
a 7-voter variant that lets the no-information control `CELL_ALPHA` vote, the haircut depths and
draw counts, the three families' own ladders, the cost ladder, and the `COIN` (a uniform draw
from the same grid, scored EXACTLY as the grid's own mean and 4b share, so it carries no
sampling noise) and `ORACLE_OOS` (the grid's best OOS-Sharpe cell) bounds.

**Gates 6 of 6 PASS.**  G1-G4 the clean U56 TURNBUDGET cell `t=0.12|B=5.0` reproduces the
committed 1795 candidate exactly — FULL 14.07% / 1.251 / −15.90%, OOS 15.40% / 1.357.  G5 the
numpy scheduler equals `engine.backtest` to `6.94e-18`.  **G6 the pick flags are float64** —
this gate was added after the first build silently mixed `bool` chooser flags with `float` COIN
shares in one column, making it object-dtype and reporting EVERY chooser's 4b reach as `1/61`.
The first run was discarded and the whole grid re-priced; the numbers below are the re-run.

## V1 — the ensemble does NOT beat the best single member ANYWHERE

Mean OOS percentile of the picked cell, over 9 (panel, family) cells:

| ensemble | beats BEST member | beats member MEAN | beats COIN | mean rank of 7 |
|---|---|---|---|---|
| ENS_MEANRANK | **0 / 9** | 6 / 9 | 5 / 9 | 3.67 |
| ENS_MEDRANK | **0 / 9** | 7 / 9 | 6 / 9 | 3.67 |
| ENS_VOTE2 | **0 / 9** | 4 / 9 | 5 / 9 | 4.44 |
| ENS_VOTE3 | **0 / 9** | 7 / 9 | 5 / 9 | 3.44 |
| ENS_VOTE4 | **0 / 9** | 5 / 9 | 5 / 9 | 3.67 |

On 4b reach the same table gives `1 / 9` for ENS_MEANRANK and ENS_VOTE4 and `0 / 9` for the
rest.  Pooled over the nine cells: member mean OOS percentile `0.5226`, ensemble mean `0.5494`,
COIN `0.5189`, ORACLE `1.0000`.  **The ensemble buys about 2.7 percentage points of OOS
percentile over the average member and over a coin — and gives up 45 points to the oracle.**

## V2/V4 — it does not even beat the member mean or the coin reliably

29 of 45 (ensemble x cell) comparisons beat the member mean; 26 of 45 beat the COIN.  Both
gates FAIL as pre-stated ("every ensemble, every cell").

## The one thing the ensemble IS good at: 4b REACH

Pooled per-cell means: **ensembles `0.2637`, members `0.1803`, COIN `0.1573`, CELL_ALPHA
`0.0874`.**  Pooled over all (draw x chooser) picks: ensembles **`0.3423` (724/2115)**, members
`0.2340` (594/2538), coin expectation `0.2041`, CELL_ALPHA `0.1135` (48/423).  Rank among the
seven rules: **2.00-2.44 of 7 in every cell, never worse than 6th, best or second in 5 of 9.**
That is the ensemble behaving exactly as a variance reducer should — it is never the best rule
and it is never the disaster.  The disaster is real and it is member-specific: `IS_DD` reaches
4b on `0.0164` pooled while topping the OOS-percentile table in 6 of 9 cells, and `IS_SHARPE`
runs `0.656` reach on U56/TURNBUDGET against `IS_DD`'s `0.098` on the same grid.

## V3 — REFUTED, and backwards: the ensemble is LESS panel-stable than its members

Spread of 4b reach across panels within a family (SMALL is a `0.000` floor for every rule in
every family, so the honest statistic is the U56-vs-B136 gap):

| family | members (mean abs U56−B136) | ensembles |
|---|---|---|
| TURNBUDGET | 0.2131 | **0.2885** |
| BANDGROSS | 0.0437 | **0.1311** |
| TOPN | 0.0492 | **0.0918** |
| pooled | **0.1020** | **0.1705** |

The mechanism is in `.votes.csv`: the members rarely agree, so the vote is decided by whichever
one or two rules happen to coincide on that panel.  Mean max-votes is **1.80 of 6** on
U56/TURNBUDGET and 2.16 on B136/TURNBUDGET; `>= 3` members agree on 11.5% of U56 draws and
`>= 4` on **none**, so `ENS_VOTE3` and `ENS_VOTE4` are MEANRANK in disguise on that grid
(identical rows in the table above).  Aggregation cannot stabilise what it is aggregating when
the inputs disagree this much — it inherits the disagreement and adds a tie-break.

## Rule 8 — the clean-panel walk-forward, both KEEP paths

Parameters chosen on 2009-2016 only, 2017-2026 read once.  The five ensembles' clean-panel
picks clear **4b FULL+OOS on 15 of 45** (ensemble x panel x family) and **4a on 2 of 45**.
Members on 4b: `IS_LEGS` 5 of 9, `IS_SHARPE`/`IS_CALMAR`/`IS_CAGRSLACK` 2, `IS_MINMARG` 1,
`IS_DD` 0, `CELL_ALPHA` 1; on 4a only `IS_LEGS` and `IS_CALMAR` pass, once each.  U56 headline books at 10 bps against the live book and SPY:

| book | FULL CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD |
|---|---|---|---|
| LIVE RULES v2 | 8.62% / 1.201 / −12.05% | 1.228 / 1.181 | 9.46% / 1.277 / −12.05% |
| SPY | 15.14% / 0.885 / −33.72% | 0.957 / 0.826 | 15.29% / 0.875 / −33.72% |
| ENS_MEANRANK TURNBUDGET `t=0.12,B=5.0` | 14.07% / 1.251 / −15.90% | 1.246 / 1.256 | 15.40% / 1.357 / −15.90% |
| ENS_MEANRANK BANDGROSS `band=0.03,g=1.25` | 14.46% / 1.201 / −19.69% | 1.229 / 1.179 | 15.91% / 1.275 / −19.69% |
| ENS_MEANRANK TOPN `n=20,g=0.75` | 15.45% / 1.169 / −22.21% | 1.269 / 1.103 | 16.55% / 1.163 / −22.21% |

The first is 1795's own cell, already PARKed by 2087 on its chooser leg; this run reaches it
with three of five ensembles and does not rehabilitate it.

## The by-product: one BOTH-PATHS cell, and it is not the U56 one

`keep4b AND keep4a` holds on **40 of 11,280** grid rows (0.35%), and 38 of those 40 are ONE
family on ONE panel: **B136 / TURNBUDGET**, at `t=0.08, B=3.0` (19 rows) and `t=0.10, B=5.0`
(18).  The first is the stronger and is reached by legal IS-only rules on the clean panel
(`ENS_MEDRANK`, `ENS_VOTE2`, `IS_LEGS`, `IS_CALMAR`; across the 61 B136 draws `IS_CALMAR`
reaches it 32.8% of the time, `ENS_MEDRANK` 26.2%).  Clean panel, 10 bps, t+1:

| | CAGR | Sharpe | MaxDD | halves | OOS CAGR / Sharpe / MaxDD | turnover |
|---|---|---|---|---|---|---|
| **cell** | **11.38%** | **1.2425** | **−12.07%** | **1.3187 / 1.1648** | **11.88% / 1.3288 / −12.07%** | **2.89x/yr** |
| live v2 on B136 | — | 1.0972 | −12.24% | 1.2296 / 0.9669 | — / — / — | 1.77x/yr (U56) |
| SPY (B136 sample) | 15.12% | 0.8844 | −33.72% | 0.9571 / 0.8249 | 15.26% / 0.8737 / −33.72% | — |

4b bars on this panel: CAGR floor 10.59% (cleared by 0.79 pp), MaxDD cap −20.23% (cleared by
8.16 pp).  **Admission robustness: 4b holds on 54 of 60 haircut draws (0.90)** — 0.85 / 0.95 /
0.90 at d = 0.10 / 0.20 / 0.30 — with 4a holding on 19 of 60 (0.32).  **Cost x latency
(companion script, 12 cells, all published): 4b holds at 0/10/25 bps at t+1 and fails at 50 bps;
it holds at 0/10 bps at t+2 and 0/10/25 bps at t+3.  4a holds on 11 of 12.**

**The honest caveat on its 4a leg.**  4a here is scored against RULES v2 run on the SAME panel,
which is this record's convention under haircuts — not against the live book as it actually
runs (U56: 1.2010 FULL, halves 1.2276 / 1.1805, −12.05%).  Against THAT book the cell wins the
full Sharpe (1.2425) and OOS (1.3288 vs 1.2767) but **fails 4a on H2 (1.1648 < 1.1805) and on
MaxDD by 2 bps (−12.07% vs −12.05%)**.  So it is a **4b KEEP-candidate**, not a 4a one.
B136 is a current-constituent list (protocol rule 9): the level is survivorship-inflated, and
only the paired chooser-vs-chooser contrasts above are protected from that.

## The 10-line memo (exact RULES wording, if this cell is ever promoted)

1. **Universe:** all instruments in `research/universe_broad.json` priced on the decision day; call that count `N`.
2. **Selection:** hold every priced name. No ranking, no band, no volatility filter.
3. **Sizing, unscaled:** each name at `1/N` of the book's gross.
4. **Gross:** `g_t = min(t_target / sigma20_t, 1.00)` with `t_target = 0.08`, where `sigma20_t` is the annualised 20-day realised volatility of the unlevered equal-weight portfolio through close `t`. Gross not deployed stays in cash — the book de-grosses, it is never re-spread.
5. **Trade cadence:** the last trading day of each MONTH. No intra-month trading.
6. **Refresh trigger:** `g_t` is re-read whenever it moves, but a re-gross executes only if trailing-252-trading-day realised turnover plus that trade's own turnover stays within **3.0 turns/yr**. Over budget, the previous gross is carried.
7. **Budget accounting:** month-end re-spreads always execute and are charged to the same budget.
8. **Execution:** weights decided at close `t`, filled at close `t+1`; 10 bps per unit turnover. Acceptance also holds at 0 and 25 bps and at t+2 / t+3 at ≤10 bps; it FAILS at 50 bps.
9. **No shorting, no leverage:** gross is capped at 1.00 by construction.
10. **Acceptance:** PROTOCOL path 4b on B136, 2009-01-13..2026-09-18, 10 bps, t+1 — CAGR 11.38%, Sharpe 1.2425, MaxDD −12.07%, halves 1.3187 / 1.1648, OOS 11.88% / 1.3288 / −12.07%, turnover 2.89x/yr; SPY 15.12% / 0.8844 / −33.72%. NOT a 4a pass against the live U56 book.

## Verdict

**KILL** — the chooser ensemble, as a device for reaching capital-worthy books, does not do what
idea 2105 predicted: it never beats the best member, it beats the member mean only 6-7 times in
9, and it is *less* panel-stable than the members it aggregates.  What survives is narrower and
should be stated narrowly: **on the 4b-reach metric an ensemble is a reliable second-best, worth
using when the cost of picking the worst member (IS_DD's 0.0164) is what you are insuring
against — and it is not a fix for 2087's 157x selection width.**  Every rule-8 verdict in this
record that leans on "reached by a legal IS-only chooser" still carries that width.
**PARK** the B136 `t=0.08, B=3.0` cell as a 4b KEEP-candidate pending a Sunday review: it is
admission-robust and latency-robust, but it is cost-fragile at 50 bps, it lives on a
survivorship-biased current-constituent panel, and its 4a pass is panel-matched only.
