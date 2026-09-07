# Idea 367 — does the NUMERAIRE clause screen the record's DD-improving overlays? — **KILL as a pre-screen** (2026-09-07, lane C)

Script: `2026-09-07_does-the-NUMERAIRE-clause-screen-the-queues-open-overlay-ideas_C.py` ·
grid `…_C.grid.csv` (324 rows) · ladder `…_C.ladder.csv` · census `…_C.census.csv` (2,630 rows) ·
coverage `…_C.coverage.csv` · leaderboard `…_C.leaderboard.csv` · walk-forward `…_C.walkforward.csv` ·
gates `…_C.gates.csv` · console `…_C.console.txt`

## Question
Idea 351 found the GROSS dial buys drawdown at the book's own `|MaxDD|/CAGR` at zero Sharpe cost, so
any real overlay must beat that free arithmetic. Idea 372 corrected the bar downward (the ladder point
you can *actually buy* is 10–13% below the closed form). Apply the bar retrospectively to every
DD-improving overlay claim in the record: how many would have been **killed on sight**, and would that
verdict have agreed with the verdict a full run produces?

## Design (2 tuned params, all points reported)
- **bar version**: `CF` = `|MaxDD_ctrl|/CAGR_ctrl` (idea 351) vs `MATCH` = the realised gross-ladder
  drawdown at *the same* pp of CAGR given up (idea 372's correction), solved on a 98-point dial
  m ∈ [0.02, 1.00] per book per rung.
- **the overlay dial**, one per family — inherited verbatim from idea 351 so its grid reproduces.
- reported axes: panel ∈ {U56, B136, SMALL439} × n ∈ {3, 20} × rung ∈ {0, 10, 25} bps × 5 families;
  **all 324 live points written to the grid CSV**, plus 2,630 census points and 66 leaderboard points.

Reproduction gates, read before any new number: rung identity vs `engine.backtest` **0.000e+00** at 10
and 25 bps; idea 40/41's published U56 n=3 NONE row 21.85%/1.036/-25.81% (1.014/1.061) to 4.6e-04;
GROSS linearity **0.000e+00**; and a full rebuild of **idea 351's committed 306-point grid, 324/324
rows matched, worst column diff 2.8e-14** (family medians reproduce exactly: GROSS +1.472,
VOLTGT +1.350, BREADTH +0.403, DDCTRL -1.582, CADENCE -3.619).

## Answer 1 — the bar kills three quarters of the record, and that is the problem
Scoreable census: **32 committed grid CSVs** expose a treated row paired to its own control on the same
axes → 7,175 pairs, of which **2,630 bought drawdown by giving up CAGR** (832 more were free and are
quarantined off the ruler, never counted as passes).

| bar | killed on sight |
|---|---|
| CF (closed form) | **1,986 / 2,630 = 75.5%** |
| MATCH, shrink 0.935 (lo) | 1,702 / 2,630 = 64.7% |
| MATCH, shrink 0.965 (med) | 1,859 / 2,630 = 70.7% |
| MATCH, shrink 1.081 (hi) | 2,041 / 2,630 = 77.6% |
| de-duplicated (1,676 distinct points) | CF 74.4%, MATCH-med 67.6% |
| restricted to overlay-named arms (2,204) | CF 77.3%, MATCH-med 76.0% |

So the queue's "if the hit rate is high" condition is **met** — and it is met *too well*.

## Answer 2 — the hit rate is high because almost everything fails anyway (LIFT 1.06)
On the 74 live on-ruler points at 10 bps, where the screen's verdict can be compared to the verdict a
full run actually produces (4b):

| bar | KILL & 4b-fail | KILL & 4b-**PASS** | kept & fail | kept & pass | precision | base rate | **lift** |
|---|---|---|---|---|---|---|---|
| CF | 50 | **5** | 14 | 5 | 0.909 | 0.865 | **1.051** |
| MATCH | 55 | **5** | 9 | 5 | 0.917 | 0.865 | **1.060** |

The screen would have saved 81% of the runs — and **destroyed 5 of the record's 10 4b-passing overlay
points (50%)** to do it. A rule that discards half the passes to raise precision from 86.5% to 91.7%
is not a pre-screen; it is a coin flip with a high base rate, the same shape as idea 375's KILL of the
loss-share pre-screen.

## Answer 3 — rule 8: the screen does not improve the pick
Menu = every (n, family, dial) **including the overlay-OFF control**, at 10 bps; chosen on 2008–2016
by IS Sharpe, once unscreened and once after dropping every point whose **IS** ratio is below its
**IS** matched-ladder bar; 2017–2026 read once.

| panel | screened pick | OOS CAGR / Sharpe / MaxDD | vs unscreened | vs control | regret vs oracle |
|---|---|---|---|---|---|
| U56 | *control* (screen leaves 1 of 36) | 23.81% / **1.0554** / -25.81% | **-0.0442** | +0.0000 | -0.2287 |
| B136 | *control* (screen leaves 6 of 36) | 12.49% / **0.8919** / -20.05% | **-0.0159** | +0.0000 | -0.3010 |
| SMALL439 | VOLTGT 0.20 (screen leaves 3) | 6.72% / **0.4743** / -27.69% | **+0.0734** | -0.0130 | -0.0130 |

Anchors, OOS 2017–2026 @10 bps: RULES v2 **1.2851** (U56) / 1.1185 (B136) / 0.5680 (SMALL439);
SPY **0.8820** (15.45% CAGR, -33.72% MaxDD). The screened pick beats the unscreened pick on **1 of 3**
panels, and on the two large-cap panels it simply collapses the menu back to doing nothing. 4a **0/108
at every rung** (0/324 in total); 4b 33/108 @0 bps, 16/108 @10, 2/108 @25 — unchanged from idea 351, as
the reproduction gate requires.

## Answer 4 — a correction to idea 372's correction
Idea 372 published "the realised ladder ratio is 1.47–1.52 and **never** above the closed form (0/114)".
On 14 (panel, n, rung) cells with control CAGR ≥ 5%/yr, the shrink (realised median / closed form) is
**0.965, range 0.935–1.081**, and the ladder ratio **exceeds** `|MaxDD|/CAGR` on **4 of 14** cells —
every one of them a cell whose own bar is high (bar_CF ≥ 2.38, vs ≤ 1.87 wherever the bound holds:
B136 n=3 @10/25 bps and SMALL439 n=20 @0/10 bps). The closed form is an upper bound on *low-bar,
high-CAGR* books only. Which bar you quote moves the census kill rate by 13 pp (64.7% → 77.6%).

## Answer 5 — against the comparator each row itself quotes, the bar barely bites
Of 2,875 committed LEADERBOARD rows, only **13** state a drawdown improvement in prose (the record's DD
claims are numbers in columns, not words). Scoring the columns instead: 101 rows carry a parseable
(CAGR, MaxDD) *and* a quoted comparator triple; 66 of those bought drawdown with CAGR; **15/66 = 22.7%**
would be killed on sight (median ratio 3.708 vs median bar 2.214). The bar bites at **~75%** against a
book's *own control* and at **~23%** against SPY/RULES v2 — because de-grossing SPY is an expensive way
to buy drawdown. Any adopted clause must name which control it means.

## Verdict
**KILL as a pre-screen.** The clause is a correct *ruler* (idea 351's finding stands, reproduced to
2.8e-14) but a bad *filter*: lift 1.06 over the base rate, 50% of the record's own 4b passes destroyed,
no rule-8 improvement, and a 13 pp swing in its own verdict depending on which version of the bar is
quoted. **Report-only** — the same disposition idea 375 reached for the loss-share statistic.

Proposed (for Sunday review, not applied here): a leaderboard/PROTOCOL *column*, not a gate —
"ratio vs own-control numeraire (bar version, control named)" — reported beside any DD improvement,
with no verdict attached.

## Caveats
Current-constituent panels (SURVIVORSHIP) — the census reads differences against an own-control, but the
4b DD cap is a level test. SMALL439 starts 2010-01-04, so its halves differ in calendar. SMALL439 n=3 is
excluded from the shrink estimate (control CAGR 0.04%/yr → bar 1512). The census's control pairing is
mechanical (a control token in a non-numeric arm column, grouped on whitelisted axis columns); 32 of
1,108 CSVs qualify, three pairs of them commit the same corpus twice (de-dup reported). CADENCE is not
an exposure overlay and is labelled at every point of use. B1's prose census is a floor, not a
measurement.
