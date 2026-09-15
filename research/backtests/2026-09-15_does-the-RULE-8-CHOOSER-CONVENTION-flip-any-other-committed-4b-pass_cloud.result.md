# Idea 862 — does the RULE-8 CHOOSER CONVENTION flip any other committed 4b pass?

**cloud lane, 2026-09-15 · ANSWERED = NO FOR THE FLIP 814 FOUND, YES FOR THE PICK · KILL for capital.**
No RULES change, nothing promoted, no PROTOCOL edit; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`
and `baseline.py` untouched.

## What was run
21 rule-8 pick sites = 3 panels (U56 55 names, B136 135, SMALL 663 after the `max_1d_move >= 1.0`
cut) × 7 pick-set members. 258 books, each read at 0 / 10 / 25 bps on FULL / IS / OOS; every rung
of every site is in `.rungs.csv` (774 rows), every pick in `.picks.csv` (84 rows).

Exactly two tuned parameters, both the queue's own, all grid points reported:
1. **CHOOSER SET**, 4 levels, all pre-stated, all reading the IS window (panel start .. 2016-12-31)
   only, ties to the smallest rung index: `C1_SHARPE` (argmax IS Sharpe — the record's de-facto
   convention, the CONTROL), `C2_SHARPE_DD` (argmax IS Sharpe s.t. IS MaxDD ≤ 60% of SPY's IS
   MaxDD — 814's second chooser), `C3_CALMAR` (argmax IS CAGR/|IS MaxDD|), `C4_CAGR`.
2. **PICK SET** ∈ {DIAL, GRID}: DIAL = idea 664/668's five committed 1-D ladders (BAND, N, GROSS,
   VOLCAP, CADENCE, 36 rungs/panel); GRID = the 2-D (dial × gross) shape recent rule-8 passes pick
   over (BAND×GROSS 5×5, N×GROSS 5×5, 50 cells/panel).

**Gates, all PASS before any new number:** `fast_backtest` == `engine.backtest` @10 bps 8.674e-18;
`band_book(0.03,0.75)` == `baseline.rules_v2_weights` 0.000e+00; 0 bps series == gross series
0.000e+00; determinism 0.000e+00; idea 664's committed BAND-dial pick row reproduced at max|d|
**2.675e-06 (U56, vintage 2026-09-09)** and **1.158e-04 (B136, vintage 2026-09-04)** — vintage-pinned
because `data/prices.csv` has gained trading days since 664 ran (third run to hit this; open idea 517).

## The answer
| statistic | result |
|---|---|
| PICK-stable sites (all 4 choosers pick the same cell) | **5 / 21 (23.8%)** |
| 4b-VERDICT-stable sites (OOS-read) | **19 / 21 (90.5%)** |
| 4a-VERDICT-stable sites | 21 / 21 |
| GROSS-stable sites (all 4 choosers land on the same gross) | 17 / 21 |
| **C1-vs-C2 disagreements — 814's exact contrast** | **0 / 21** |
| sites whose 4b verdict moves with the chooser at all | 2 / 21, **both moved by C3_CALMAR** |

- **H_MINORITY CONFIRMED.** The chooser is a real unpriced degree of freedom: it moves the PICK at
  16 of 21 sites. 814's premise is right about the pick.
- **H_FLIP FALSIFIED, and the reason is itself the finding.** The C2 constraint *binds* (C1's own
  argmax violates the IS DD cap) at only **5 of 21** sites, and at all five the 4b verdict is FALSE
  under both choosers, so the C1→C2 flip never reproduces. 814's grid is a rare site where the IS
  argmax is DD-infeasible; on the record's own committed pick shapes the cap is slack.
- **H_VERDICT CONFIRMED** (90.5% > 23.8%): the choosers disagree about the cell and agree about the
  verdict, because most rungs of a dial share one gross and 4b is mostly a gross statistic.
- **H_GROSSDIAL CONFIRMED** (gross-moving sites 8/9 verdict-stable vs 11/12 elsewhere — directionally
  right but a 1-site margin; do not quote it as strong).
- **H_C2COST CONFIRMED.** Mean OOS CAGR C1 8.85% vs C2 8.38% at mean gross 0.857 vs 0.821: the
  DD-constrained chooser pays ~0.5 pp/yr and buys 0.7 pp of OOS drawdown, i.e. it de-grosses.
- The **flipping chooser is C3_CALMAR**, not C2: it alone turns U56/N and B136/BAND×GROSS from 4b
  pass to 4b fail (n4b_OOS 3 vs 5 for the other three choosers).

## Rule 8 (this run IS the walk-forward: every chooser sees IS only, OOS read once)
Mean over the 21 sites, 10 bps:

| chooser | OOS CAGR | OOS Sharpe | OOS MaxDD | mean gross | 4b OOS | 4b FULL | 4a OOS | 4b OOS @25bps |
|---|---|---|---|---|---|---|---|---|
| C1_SHARPE | 8.85% | 0.8873 | −19.96% | 0.857 | 5 | 5 | 0 | 4 |
| C2_SHARPE_DD | 8.38% | 0.8834 | −19.26% | 0.821 | 5 | 5 | 0 | 4 |
| C3_CALMAR | 8.57% | 0.8837 | −18.95% | 0.857 | 3 | 5 | 0 | 2 |
| C4_CAGR | 9.07% | 0.8983 | −19.83% | 0.857 | 5 | 5 | 0 | 4 |

Comparands on the same OOS window: **SPY** 15.27% / 0.8740 / −33.72% (U56 calendar), 15.33% / 0.8767
/ −33.72% (B136, SMALL). **RULES v2** 9.46% / 1.2772 / −12.05% (U56), 7.88% / 1.1059 / −12.24%
(B136), 3.75% / 0.5600 / −13.89% (SMALL). **Every chooser loses to SPY on OOS CAGR and to RULES v2
on OOS Sharpe on average, and 0 of 84 (site, chooser) picks clears 4a.**

## Why nothing is promoted
All 4b passes are gross-1.00 or top-50 band books, and the **matched-gross twin control** (hold every
priced name at the same gross, same cadence, same cost) reads them the way ideas 502/504/596/674/858
already read this shelf: the twin's OOS Sharpe is **within +0.0010 on average** of the arm's, while
the arm's OOS CAGR is 5–6 pp lower and its OOS MaxDD 4–13 pp shallower. The twin fails 4b at **0 of
24** passes — on the drawdown leg alone. This independently replicates today's idea 858 headline
(Sharpe range 0.0010) on a corpus 858 never touched. 4b is certifying exposure, not the clause.

## Caveats
**SURVIVORSHIP:** U56/B136/SMALL are current-constituent lists, so every CAGR and drawdown LEVEL is
optimistic; the chooser-to-chooser DIFFERENCE this run measures is survivorship-neutral by
construction. Idea 835's 2020-dependence caveat applies to every MaxDD comparison here. The
C3_CALMAR result rests on 2 sites — a direction, not a rate.

## What the record should take from this
The chooser belongs in the published specification of a rule-8 pass — it moves the pick at 76% of
sites — but it is **not** the general threat to the 4b pass list that 814's single observation
suggested. The narrower, reportable claim: **a rule-8 pass whose IS argmax is DD-feasible is
chooser-robust; 814's is not, and that is what should be stated beside it.**
