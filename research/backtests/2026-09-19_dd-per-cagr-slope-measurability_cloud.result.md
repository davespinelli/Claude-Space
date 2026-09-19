# Idea 1468 (cloud lane, 2026-09-19) — is the DD-per-CAGR SLOPE a MEASURABLE STATISTIC on ANY device family?

**VERDICT: KILL — the statistic is broken for the RECORD, not for the beta band.**
Script `research/backtests/2026-09-19_dd-per-cagr-slope-measurability_cloud.py`; 26/26 gates pass; 27s.

## The question
Idea 1461 put a paired circular-block bootstrap on the beta band's exchange rate (pp of drawdown
bought per pp of CAGR given up) and found SE 0.61..8.96 against a five-rung spread of 0.92 — no
rung resolved from any other at |t| > 0.20. It could not say whether the defect belonged to the
BAND or to the STATISTIC. This run re-forms the identical statistic and the identical bootstrap
on the record's **three other DD-buying families**, each on its **own published dial ladder**:

| family | device | published ladder | source |
|---|---|---|---|
| G | gross scalar | g {0.25, 0.375, 0.50, 0.625, **0.75**, 0.875, 1.00} | ideas 1446 / 1454 |
| V | intra-book inverse-vol, w ∝ vol^(−p), renormalised to the same gross | p {**0.0**, 0.5, 1.0, 1.5, 2.0} | idea 1433 |
| S | trailing equity stop, RESTORE = SAME | depth {0.05, 0.075, 0.10, 0.125, 0.15, 0.20} | idea 1405 |

All three families share **one anchor** — the frozen 2026-09-04 incumbent (N=20, H=126, gross
0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1) — asserted bit-identical at gate G2, which
makes the three ladders directly comparable. Dials: the family dial, and L ∈ {21, 63, 126}, the
block length (all reported, 63 primary). Nothing else is tuned.

## THE ANSWER — 1 of 144, and the one is a boundary case
**Adjacent rung-to-rung gaps resolving at |t| > 2, over 4 ladders × 3 panels × 3 block lengths:
`1 of 144`** (all within-family pairs: **1 of 378**). The single passer is U56 family G at
L = 126 and reads **|t| = 2.0628** — it clears the bar by 3%, and the same gap reads |t| < 2 at
both other block lengths. Per family: **G 1/27** (median |t| 0.9367), **V 0/27** (0.0649),
**S at FRAC 0.50 0/45** (0.1163), **S at FRAC 1.00 0/45** (0.1894). The pre-registered
MEASURABLE bar — half a family's adjacent gaps resolving at L = 63 on U56 AND B136, plus a
ladder spread exceeding the median rung SE — is cleared by **no family on any panel**.

**The gross scalar is the decisive case.** It is the most mechanical DD-buyer that exists: it
scales the whole book linearly, so its exchange rate ought to be the easiest thing in the record
to measure. Its ladder spread is **0.0453** (U56) and **0.0489** (B136) against median rung SEs
of **0.42–0.77** — spread/SE **0.064 to 0.108**. The slope is not noisy *and* varying; it is
**very nearly constant by construction** (U56: −1.1740 / −1.1571 / −1.1414 / −1.1287 at
g = 0.25 / 0.375 / 0.50 / 0.625) and the noise is an order of magnitude larger than what little
variation there is. There is no rung to find.

**On SMALL the statistic is not merely unresolved, it is degenerate.** Median rung SEs run
**10.3 to 63.6** against spreads of **0.13 to 1.64** — spread/SE **0.0022 to 0.159** — because
the anchor's own CAGR difference sits near zero and the ratio's denominator nearly vanishes. Its
family-V ladder-mean slope even reads the **wrong sign** (+4.93). Every SMALL exchange rate in
the record is unreadable.

## The second job the record asks of this statistic — also fails, but the ORDERING survives
Exchange rates are used for two things: picking a rung inside a family, and ranking one device
against another. (b) above only prices the first, so this run adds the **cross-family** contrast
(paired difference of two families' ladder-mean slopes, same block-start matrix):
**1 of 36 resolve at |t| > 2** (median |t| 0.2786, max 2.0763). But the **sign fraction** is a
different story: G-vs-S(1.00) holds its sign in **0.950–0.995** of replicates and G-vs-S(0.50) in
**0.830–0.995** on U56/B136, with G steepest in every case (U56 ladder-mean **−1.1503** vs V
**−0.6690** and S(0.50) **−0.9947**; B136 **−1.2307** vs **−1.0322** / **−0.9084**). The plain
de-gross buys drawdown more cheaply than either device on both large-cap panels — the seventh
consecutive run to find that — and it is the ordering, not the magnitude, that the tape supports.

**RECOMMENDED SCHEMA CHANGE, NOT ENACTED** (PROTOCOL rule 6 confines rules changes to the Sunday
review; this run modifies no rule file): the record should stop publishing DD-per-CAGR exchange
rates as **valued** findings with rung-level precision, and publish them as **orderings** — a
sign fraction and the block length it was read at — or not at all.

## A correction made during this run and kept in the record
Family S was first specified at FRAC = 1.00 (full de-risk) on the stated reasoning that the
largest exposure cut is the most favourable case for measurability. That reasoning was wrong and
the cell is **degenerate: at FRAC = 1.00 the brake is an ABSORBING state.** The braked book holds
only cash, so its own equity stops moving, its drawdown from peak can never shrink, and the
release condition can never fire. U56 depth 0.05: braked on **4,411 of 4,708 rows after exactly
ONE episode**, entire 2017-2026 OOS window flat (CAGR 0.00%, Sharpe undefined). Those numbers
**replay idea 1405's own committed FRAC = 1.00 cells to 4.7e-07** (gate G12), so this is a
property of the record's published grid, not of this script — 1405 committed six absorbing cells
per panel per RESTORE without flagging them. Episode counts, gate G13: FRAC 1.00
`[1, 1, 1, 1, 1, 0]` against FRAC 0.50 `[41, 21, 14, 16, 4, 0]`. The FRAC = 1.00 arm is published
in full as the diagnostic; the headline slope arm is FRAC = 0.50; FRAC is a reported axis at both
values, not a third dial, and the bar was declared on the non-absorbing arm before either arm's
slopes were read.

## Capital (PROTOCOL rules 3, 4, 8, 9)
78 real books, every one published in `.grid.csv`. **4a: 0 of 78.** **4b full: 18 of 78; 4b full
AND OOS: 18 of 78.** Binding legs: L_CAGR 44 > L_H2 42 > L_H1 36 > L_DD 30.

**Rule 8** (family dial chosen on warm-up..2016-12-31 by argmax IS Sharpe; 2017-2026 read ONCE):
the chooser picks **depth = 0 — the un-braked anchor — for every stop family on every panel**,
and g = 1.00 for every gross family. Mean Δ(OOS Sharpe) vs the frozen anchor **+0.0056**, beating
it **4 of 12**; three of those four are the g = 1.00 lever pick, which then fails 4b on the DD
leg (OOS MaxDD −24.93% U56 / −26.97% B136 against SPY's −33.72% cap at 0.60 → −20.23%).

**H_HINDSIGHT fires again.** One comparand book clears 4b FULL and OOS *and* beats the anchor on
both Sharpes — U56, family S at FRAC 0.50, **depth 0.075**: full 13.71% / **1.1713** / −14.54%
(anchor 15.80% / 1.1537 / −19.13%), OOS 15.52% / **1.2689** / −14.54% (anchor 17.32% / 1.1857 /
−19.13%). **No rule-8 chooser in this run reaches it** — the IS-argmax picks depth 0 — so under
rule 8 it is **PARK, not KEEP**, and no RULES memo is written for it. Consistent with 1461 /
1350 / 1331 / 1323 / 1321 / 904.

**SURVIVORSHIP (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010 (54 tickers with max_1d_move ≥ 1.0 dropped per `data/small_meta.csv`;
665 investable names remain). Every absolute level is optimistic and every 4b pass an optimistic
one. The headline is a **resolution** reading on contrasts between books built over the SAME
names on the SAME days at the SAME bootstrap draws, which the bias cannot manufacture; the
18-of-78 pass count is not so protected.

**Gates 26/26**, including G1/G1b (the frozen U56 anchor replays at 15.8028% / 1.1537 / −19.1276%
full and 1.1857 OOS Sharpe), G2 (the three families' anchors are bit-identical, 0.000e+00),
G6/G6b (no leverage; every slope-ladder rung at or below the incumbent's 0.75), G7 (family V's
exposure channel shut, 0.000e+00), G8 (every family dial bites), G9 (one block-start matrix per
(panel, L)), G10 (bit-identical recompute), G12/G13 as above.

**No RULES change.** RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.
