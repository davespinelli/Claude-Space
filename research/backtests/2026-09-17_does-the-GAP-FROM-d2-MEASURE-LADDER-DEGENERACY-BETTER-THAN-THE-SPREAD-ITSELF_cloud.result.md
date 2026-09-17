# Idea 1205 — does the GAP FROM d2 measure LADDER DEGENERACY better than the SPREAD ITSELF?

**VERDICT: KILL.** R = range / (d2(k) × rung SD) ranks the record's dials **identically** to the
raw spread under every sampling SD basis (AUC 1.0000 vs 1.0000 at 9 of 9 pooled cells), **worse**
under the only basis where its advertised null is arithmetically reachable, and its "known null"
of R = 1 is **reached by no ladder in the run, including the one built to satisfy d2's own
independence assumption**.

Script: `2026-09-17_does-the-GAP-FROM-d2-MEASURE-LADDER-DEGENERACY-BETTER-THAN-THE-SPREAD-ITSELF_cloud.py`
Artefacts: `.rungs.csv` (279 books), `.rungsd.csv` (837), `.dialgrid.csv` (396), `.calibration.csv`,
`.separation.csv`, `.mechanism.csv`, `.picks.csv` (24 rule-8 picks), `.prediction.csv`, `.gates.csv`,
`.hypotheses.csv`, `.log.txt`. **Gates 7 of 7 PASS**, including `d2(2) = 2/√π` to 0.0e+00 and
`d2(5) = 2.325929` to 5.3e-08 against the published control-chart table, and the fast runner against
`engine.backtest` at 1.4e-17.

## THE TWO DIALS AND NO MORE (rule 4, and the queue names both)
`LADDER SET` {L_RECORD, L_WIDE, L_CTRL} × `SD BASIS` {S_IID, S_BLOCK, S_FOLD, S_CROSS} = **12 cells,
every one published**. NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four dial
ladders {N, H, GROSS, CADENCE}; the statistic {Sharpe, CAGR, MaxDD}; the comparand spreads {RANGE,
RANGE/|MEAN|}; the 4a and 4b legs; the rule-8 arm. Book frozen at the 2026-09-04 KEEP-4b candidate's
construction (composite of 12-1/6m/3m percentile ranks, **no vol scaler**, above-own-200d-MA and
vol20 < 0.60 eligibility, top-N equal weight at g/N, gated-out weight to CASH), 10 bps, next-day
execution, warm-up 260, IS ends 2016-12-31. Anchor N 20 / H 126 / g 0.75 / weekly.

## (A) THE NULL IS NOT REACHABLE, WHICH IS THE WHOLE CLAIM
The queue's case for R is that it has "a known null and no tuning". d2(k) is the expected range of
k **independent** standard normal draws, so R = 1 is the statement *these k rungs are k independent
books*. **CTRL_LIVE is the ladder built to make that statement true** — k = 8 gross-matched null
books, names drawn uniformly at every rebalance, independent across seeds (gate G5: cross-book
|corr| 0.954, not 1). It reads **R = 0.4186 (range 0.1266–0.6186)**, not 1, at every sampling
basis. The reason is structural and not a defect of the construction: a ladder's rungs share the
market factor, so **rung-to-rung dispersion is less than half of any single rung's own time-series
sampling SE** (median single-rung Sharpe SE: S_IID 0.242/0.242/0.256, S_BLOCK 0.208/0.204/0.221,
S_FOLD 0.193/0.214/0.208 on U56/B136/SMALL). **No real ladder reaches the bar either: max R = 0.6894
over 72 (panel × ladder × sampling basis) cells, 0 of 72 at or above 1.**

The escape — reading "its own rung SD" as the SD of the ladder's own rungs (`S_CROSS`) — makes the
null reachable and **makes it vacuous**: R = range/(d2(k)·sd) of k draws is ≈1 for *any* k draws
from *any* distribution, and it duly reads **mean 1.0090 over 29 non-degenerate ladders, range
0.8347–1.1625 — including GROSS at 1.0383, the dial 1189 proved degenerate.** So the statistic has
no usable absolute bar under either reading: unreachable under one, tautological under the other.

## (B) AGAINST THE SPREAD, THE QUEUE'S ACTUAL QUESTION: NO GAIN, EVER
Separating GROSS (1189's degenerate dial, pre-declared) from {N, H, CADENCE} across both real ladder
sets and all three panels:

| SD basis | AUC(R) | AUC(RANGE) | AUC(RANGE/\|MEAN\|) | R − RANGE |
|---|---|---|---|---|
| S_IID | 1.0000 | 1.0000 | 1.0000 | **+0.0000** |
| S_BLOCK | 1.0000 | 1.0000 | 1.0000 | **+0.0000** |
| S_FOLD | 1.0000 | 1.0000 | 1.0000 | **+0.0000** |
| S_CROSS | 0.6852 | 1.0000 | 1.0000 | **−0.3148** |

**The mechanism is measured, not asserted.** Within a panel the denominator d2(k) × rung-SD moves
by a factor of **1.96–2.52** across the eight real ladders while the numerator RANGE moves by
**35.4–107.8×**. R is therefore the spread divided by a near-constant — a monotone transform of it —
and a monotone transform cannot reorder anything. That is why the AUCs are equal to four decimals
rather than merely close, and it is a general argument: **any normaliser that varies an order of
magnitude less than what it normalises adds no ranking information.**

## (C) RULE 8 AND BOTH KEEP PATHS — 24 PICKS, 0 CLEAR EITHER
Benchmarks (10 bps, post warm-up): **U56 SPY 15.06% / 0.8814 / −33.72% (halves 0.9598/0.8170), OOS
15.15% / 0.8684; U56 RULES v2 (live) 8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714; B136 SPY 15.16% /
0.8861 / −33.72%, OOS 15.33% / 0.8767; B136 LIVE 7.98% / 1.0993 / −12.24%, OOS 7.88% / 1.1059;
SMALL SPY 14.06% / 0.8581 / −33.72%, OOS 15.33% / 0.8767; SMALL LIVE 4.30% / 0.6637 / −13.89%, OOS
3.75% / 0.5600.** Rung chosen on IS (warm-up → 2016-12-31) by IS Sharpe, 2017-2026 read ONCE.

**4b full 0 of 24, 4b OOS 0 of 24, 4a 0 of 24; 13 of 24 beat SPY on OOS Sharpe.** Best pick:
**U56 / GROSS / g = 1.00 — 20.79% / 1.1387 / −24.93%, halves 1.205/1.094, OOS 22.65% / 1.1623 /
−24.93%** — which fails 4b on the drawdown leg (cap is 60% of SPY's −33.72% = −20.23%) and is the
incumbent book with more of it, not a new rule. Worst: **U56 / L_WIDE / N = 3, OOS 0.8157**, below
SPY. **The GROSS dial's IS argmax lands on the ladder's TOP rung g = 1.00 at 6 of 6 (panel × ladder
set) cells** — an independent reproduction of 1195's boundary premise on a statistic 1189 already
showed is flat in gross, and it buys the drawdown.

## (D) R DOES NOT PREDICT WHAT CHOOSING IS WORTH EITHER
Spearman of each score against |OOS Sharpe(IS-argmax rung) − mean OOS Sharpe over the ladder|, n = 24:
**R_SIID +0.7591, R_SBLOCK +0.7513, R_SFOLD +0.7348, R_SCROSS −0.0357 — against the raw RANGE
+0.7678 and RANGE/|MEAN| +0.7522.** The raw spread is the best of the six. The ordering it recovers
is the one already in the record: mean |choose-gain| runs **N 0.1073 > CADENCE 0.0440 > H 0.0274 >
GROSS 0.0020**.

## WHAT THIS IS WORTH
Nothing is enacted, no candidate, no memo. The capital content is negative and specific: **the
record should not add a d2 normalisation to its ladder readings.** It costs a bootstrap per rung,
changes no ranking it would have made from the spread alone, and attaches an absolute bar (R = 1)
that no ladder on this tape can reach and that a second reading of the same words makes meaningless.
1155's 0.273 gross shortfall is real but it is the spread being small, restated in different units.

## SURVIVORSHIP (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current output of a sub-$2B screen
(`data/SMALL_PANEL_README.md`) less the documented `max_1d_move >= 1.0` exclusion — 52 of 715
dropped, 663 investable names plus SPY as benchmark only. Every CAGR and drawdown LEVEL above is
optimistic and the 4a/4b counts are an UPPER bound (here, of zero). R, the spread and the AUCs are
ratios of one construction against itself on one tape and the bias very largely cancels out of them;
it does NOT cancel out of the rule-8 OOS levels in (C).

## FOLLOW-UPS FILED (filed 1213->1216, 1214->1217, 1215->1218 on push: lane collision, defect 932 again)
1216 (is every normaliser the record has added order-of-magnitude smaller than what it normalises),
1217 (the GROSS IS-argmax lands on the top rung at 6 of 6 — should a boundary pick be reportable at
all), 1218 (rung-to-rung dispersion is under half a single rung's sampling SE — what IS the right
null for a ladder).
