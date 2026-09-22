# Idea 2121 (lane cloud, 2026-09-22) — can an IS-ONLY CHOOSER THAT SEES GROSS beat IS SHARPE on a band × gross ladder?

**ANSWERED = NO — and the idea's premise, inherited from 2119, is itself wrong.**
Script `research/backtests/2026-09-22_gross-seeing-is-chooser-on-band-gross-ladder_cloud.py`.
200 published grid rows (`.grid.csv`), 72 published picks (`.picks.csv`). 5 of 5 gates PASS
(G3 max|d| 0.000e+00 — the ladder's centre cell IS `baseline.rules_v2_weights`; G1 max|d|
0.000e+00 against `engine.backtest`). **No RULES change. RULES.md / PROTOCOL.md / scan.py /
bot.py / baseline.py untouched.**

## The setup
RULES v2's own form on its own two dials: band b ∈ {0.00, 0.02, 0.03, 0.05, 0.08} × gross
g ∈ {0.50, 0.60, 0.75, 0.85, 1.00}, 25 cells, weekly, t+1, panels U56 and B136, costs
{0, 10, 25, 50} bps. Seven legal IS-only choosers taken verbatim from ideas 2087/2109
(IS_SHARPE, IS_MINMARG, IS_CALMAR, IS_CAGRSLACK, IS_LEGS, IS_DD, CELL_ALPHA), each picking
one cell on 2009–2016 rows only; 2017–2026 read ONCE. Two zero-parameter comparands priced
beside them: **MAXGROSS** (live band 0.03, top gross rung, reads no in-sample data at all)
and **RANDCELL** (the 25-cell mean = the uniform-random-draw expectation).

## B1 — the premise is half right: three choosers really do see gross
Gross share of each IS statistic's own spread (gspread / (gspread + bspread)), 10 bps:

| panel | IS_SHARPE | IS_MINMARG | IS_CALMAR | IS_CAGRSLACK | IS_LEGS | IS_DD |
|---|---|---|---|---|---|---|
| U56  | **0.015** | 0.860 | 0.087 | 0.860 | 0.500 | 0.825 |
| B136 | **0.025** | 0.826 | 0.237 | 0.826 | 0.800 | 0.855 |

IS Sharpe's whole-ladder gross spread reproduces 2119 exactly (0.0010 U56 / 0.0022 B136).
IS_MINMARG and IS_CAGRSLACK are 34–56× more gross-sensitive. **So the choosers the idea named
do see the dial.**

## B2 — and it changes nothing: they pick the same gross rung IS Sharpe already picks
**5 of 7 choosers land on gross 1.00, in 8 of 8 panel × cost instances — IS_SHARPE among
them.** At 10 bps, IS_SHARPE / IS_MINMARG / IS_CAGRSLACK / IS_LEGS all pick `b0.08_g1.00` on
**both** panels. Only IS_CALMAR differs (U56 `b0.02_g1.00`, B136 `b0.03_g1.00`), and it
differs on the **band**, not the gross.

## B7 — why: 2119's "rule 8 COIN-FLIPS GROSS" reading is wrong
A statistic can be nearly flat in a dial and still order it perfectly. Over all 40
(panel × cost × band) blocks:

| statistic | monotone ↑ in gross | monotone ↓ | argmax at g=1.00 | mean span |
|---|---|---|---|---|
| **IS Sharpe** | **40 / 40** | 0 | **40 / 40** | 0.00214 |
| OOS CAGR | 40 / 40 | 0 | 40 / 40 | 0.05569 |
| **OOS Sharpe** | **0 / 40** | **30 / 40** | **0 / 40** | 0.00140 |
| FULL Sharpe | 14 / 40 | 14 / 40 | 14 / 40 | 0.00076 |

IS Sharpe's 0.0021 gross gradient **never once reverses**. Its argmax is deterministic, not a
coin flip — which is why a gross-seeing chooser has nothing to add. **The finding that does
matter is the sign: the IS gross gradient is INVERTED against OOS Sharpe.** Every legal
chooser walks up the gross ladder; OOS Sharpe walks down it. The picks are "right" only
because the 4b CAGR floor is an exposure bar and OOS CAGR is monotone up in gross — which is
2125's conclusion reached from the chooser side.

## B3 / B4 — the OOS verdict spread the idea asked for
34 of 56 chooser picks clear 4b OOS. Per instance the 7 choosers land on **3–4 distinct
cells**, with an OOS Sharpe spread of **0.0187–0.1322** and an OOS MaxDD spread of
**11.0–11.3 pp**; they **disagree on the 4b OOS verdict in 7 of 8 instances**. So idea 2109's
selection-width finding replicates on this ladder: a single-chooser rule-8 verdict here
carries roughly 0.1 of unreported OOS Sharpe and a whole 4b verdict.

## B5 — THE KILL: no fitted chooser beats a rule that reads no data at all
Mean over the 8 panel × cost instances:

| rule | mean OOS Sharpe | mean OOS CAGR | 4b FULL+OOS | beats MAXGROSS on OOS Sharpe |
|---|---|---|---|---|
| **MAXGROSS (0 params)** | **1.1579** | 0.1125 | 4 / 8 | — |
| IS_DD | 1.1571 | 0.0554 | 0 / 8 | 6 / 8 |
| IS_CALMAR | 1.1434 | 0.1133 | 6 / 8 | 4 / 8 |
| RANDCELL (25-cell mean) | 1.1361 | 0.0818 | — | 2 / 8 |
| CELL_ALPHA (0 information) | 1.1299 | 0.0531 | 0 / 8 | 2 / 8 |
| IS_SHARPE = IS_MINMARG = IS_CAGRSLACK = IS_LEGS | 1.1089 | 0.1128 | 7 / 8 | 2 / 8 |

**MAXGROSS has the highest mean OOS Sharpe of all nine rules** and the same mean OOS CAGR as
the fitted choosers (0.1125 vs 0.1128). Fitting 25 cells on eight years of in-sample data
buys **−0.049 of OOS Sharpe and −0.0003 of OOS CAGR** against reading no in-sample data at
all. The fitted choosers do win the 4b *count* (7/8 vs 4/8) — but only because they pick the
looser band 0.08, whose extra exposure clears the CAGR floor more often while being the
**worst** band on OOS Sharpe (U56 1.1625 at the IS pick vs 1.2784 at b0.02; B136 1.0921 vs
1.1211). That is the 4b bar rewarding exposure, not a chooser finding one.

## Rule 8, 10 bps, 2017–2026 read once (the headline numbers)
Benchmarks — U56 OOS: RULES v2 9.46% / 1.2767 / −12.05%; SPY 15.29% / 0.8751 / −33.72%.
B136 OOS: RULES v2 7.85% / 1.1017 / −12.24%; SPY 15.26% / 0.8737 / −33.72%.

| panel | chooser | cell | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b FULL | 4b OOS | 4a |
|---|---|---|---|---|---|---|---|---|
| U56 | IS_SHARPE / MINMARG / CAGRSLACK / LEGS | b0.08_g1.00 | 12.00% | 1.1625 | −19.05% | ✓ | ✓ | ✗ |
| U56 | IS_CALMAR | b0.02_g1.00 | **12.53%** | **1.2784** | **−15.65%** | ✓ | ✓ | ✗ |
| U56 | MAXGROSS (0 params) | b0.03_g1.00 | 12.67% | 1.2760 | −15.91% | ✓ | ✓ | ✗ |
| B136 | IS_SHARPE / MINMARG / CAGRSLACK / LEGS | b0.08_g1.00 | 10.98% | 1.0921 | −19.50% | ✓ | ✓ | ✗ |
| B136 | IS_CALMAR | b0.03_g1.00 | 10.47% | 1.1006 | −16.16% | ✓ | **✗** | ✗ |
| B136 | MAXGROSS (0 params) | b0.03_g1.00 | 10.47% | 1.1006 | −16.16% | ✓ | **✗** | ✗ |

**PATH 4a: 0 of 72 picks pass, on either panel, at any cost rung** — every cell's MaxDD is
worse than RULES v2's, which is what the de-grossed live book buys.

## Verdict: KILL for capital, no new KEEP, no RULES change
The question as filed is answered **NO**: a gross-seeing IS-only chooser does not beat IS
Sharpe, because IS Sharpe was never coin-flipping gross — it was flat and perfectly ordered.
The one chooser that departs from it (IS_CALMAR) departs on the band, wins by +0.116 OOS
Sharpe on U56 and **loses on B136 (4b OOS FAIL)**, i.e. it is not panel-stable; and on U56 it
is indistinguishable from MAXGROSS (1.2784 vs 1.2760, −15.65% vs −15.91%), a rule with no
parameters and no in-sample read. Picking IS_CALMAR after seeing this table would be a third
tuned dial — the very selection width B4 measures.

**PARK (recorded, not promoted):** `U56 band 0.02 / gross 1.00 weekly`, FULL 11.33% / 1.1934
/ −15.65% (H1 1.206 / H2 1.186), OOS 12.53% / 1.2784 / −15.65%, clears 4b on FULL and OOS at
0/10/25 bps. 2119 PARKed this cell as *unreachable* (rank 11th on IS Sharpe); this run shows
it **is** reachable, by 1 of 7 legal choosers. It stays PARK, not KEEP, for three reasons:
(i) it FAILS 4b in the IS window itself (`keep4b_is` False); (ii) the chooser that reaches it
fails on the second panel; (iii) a zero-parameter rule matches it. Memo: `.memo.md`.

## Survivorship (PROTOCOL rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists, so every absolute CAGR and drawdown here is
optimistic. This run is a within-tape contrast between choosers on the same 25 cells and the
same dates; it does not repair the level. The PARK cell's absolute numbers inherit the bias
in full.
