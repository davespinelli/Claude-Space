# Idea 1779 (lane C, 2026-09-22) — is the NAME-SET CHOOSER just a TRAILING-RETURN CHOOSER in disguise?

**VERDICT: ANSWERED = YES, largely. A chooser that never runs a backtest — the mean trailing
2009–2016 total return of the draw's 20 names — matches or beats 1749's best BOOK statistic at
20 of 32 (D, q, target) cells on U56 and 23 of 32 on B136, ranks the 480 draws at
ρ = +0.896 against `IS_CAGRSLACK`, and under rule 8 reaches MORE 4b passes than the book
statistics do (14 of 20 picks vs 13 of 16). KILL of the "the chooser carries BOOK information"
reading of 1749's headline. The one thing it never reaches is path 4a.**

Script `research/backtests/2026-09-22_name-set-chooser-vs-trailing-return_C.py` (30.1 s, offline,
deterministic, **9/9 gates**). 1749's construction unchanged: U56/B136, N = 20, band c = 0.03,
gross 0.75, weekly, t+1, 10 bps binding, seed stream `default_rng(16320000 + 1009*N + d)`,
IS ≤ 2016-12-31 / OOS ≥ 2017-01-01. Two tuned dials and no more: **CONTROL STATISTIC** (5 naive
controls) × **DECILE WIDTH q** {0.05, 0.10, 0.20, 0.25}. Reported, not tuned: D ∈ {24, 96, 240,
480} (nested), cost ∈ {0, 10, 25, 50} bps, panel, and both 4b targets. 3,840 cells published in
`.grid.csv.gz`, 720 decile rows in `.decile.csv`, 72 rule-8 picks in `.rule8.csv`.

**G3 replicates the record exactly:** U56 D = 480 base 42/480 = 8.75% (1749 quoted 43/480, 1775
re-read 42 after the price-cache refresh), top decile `IS_CAGRSLACK` **25/48 = 52.08%**, the
published number to the draw.

## 1. The naive controls (no band, no book, no backtest — adjusted closes ≤ 2016-12-31 only)

| | definition |
|---|---|
| `NAIVE_MEANRET` | mean over the draw's 20 names of each name's IS total return (**the idea's own wording**) |
| `NAIVE_MEDRET` | median of the same per-name IS total returns |
| `NAIVE_LOGRET` | mean of log(1 + IS total return) |
| `NAIVE_EWBH` | IS total return of an equal-weight, never-rebalanced buy-and-hold basket |
| `NAIVE_MEANSHR` | mean of the names' own IS Sharpe ratios (the one non-pure-return control) |

**G9** permutes the band — a different book entirely — and recomputes all five: worst |Δ| =
**0.000e+00**. They cannot be reading the book. **G4**: no statistic touches a row ≥ 2017-01-01,
so all five are legal rule-8 choosers.

## 2. The headline — top-q OOS-4b rate, U56 N=20, the idea's named target (`4b OOS`)

| D | q | base | `IS_CAGRSLACK` | best BOOK | **best NAIVE** | naive ≥ CAGRSLACK? |
|---|---|---|---|---|---|---|
| 480 | 0.05 | 105/480 = 21.88% | 16/24 = 66.67% | 66.67% (`IS_LEGS`) | **19/24 = 79.17%** (`LOGRET`) | **yes, +12.50 pp** |
| 480 | 0.10 | 21.88% | 29/48 = 60.42% | 60.42% | **32/48 = 66.67%** (`MEANRET`, `EWBH`) | **yes, +6.25 pp** |
| 480 | 0.20 | 21.88% | 46/96 = 47.92% | 47.92% | **50/96 = 52.08%** (`LOGRET`) | **yes, +4.17 pp** |
| 480 | 0.25 | 21.88% | 54/120 = 45.00% | 45.00% | **56/120 = 46.67%** (`MEANRET`, `LOGRET`) | **yes, +1.67 pp** |

**On the target the idea names, the naive control beats the book statistic at all four decile
widths.** Every one of those naive rates carries p ≤ 1.2e-09 exact hypergeometric against the
same base rate.

On 1749's own published target (`4b BOTH`) the book statistic keeps a hair: at D = 480, q = 0.10
`IS_CAGRSLACK` is 25/48 = 52.08% against `NAIVE_MEANRET`/`NAIVE_EWBH` **24/48 = 50.00%** — a
**one-draw** difference, and the naive control wins that cell at q = 0.05 (18/24 = 75.00% vs
16/24 = 66.67%).

Pooling all 32 (D, q, target) cells per panel:

| panel | best naive ≥ `IS_CAGRSLACK` | best naive ≥ best BOOK |
|---|---|---|
| U56 | **23 of 32** | **20 of 32** |
| B136 | **23 of 32** | **23 of 32** |

## 3. It is not merely matching the rate — it is picking the same draws

Spearman ρ over all 480 U56 draws at 10 bps:

| statistic | ρ vs `IS_CAGRSLACK` | ρ(S, OOS CAGR margin) | ρ(S, OOS Sharpe margin) |
|---|---|---|---|
| `IS_SHARPE` | +0.8957 | +0.4333 | +0.3774 |
| `IS_LEGS` | +0.7361 | +0.3271 | +0.2729 |
| `IS_CAGRSLACK` | 1.0000 | +0.5897 | +0.3570 |
| **`NAIVE_MEANRET`** | **+0.8960** | **+0.5686** | **+0.3985** |
| **`NAIVE_EWBH`** | **+0.8960** | +0.5686 | +0.3985 |
| `NAIVE_LOGRET` | +0.7891 | +0.5545 | +0.3008 |
| `NAIVE_MEDRET` | +0.5945 | +0.4717 | +0.1462 |
| `NAIVE_MEANSHR` | +0.5832 | +0.3195 | +0.1033 |

`NAIVE_MEANRET` is **more** rank-correlated with `IS_CAGRSLACK` (+0.8960) than `IS_SHARPE` is
(+0.8957), and it correlates with the OOS Sharpe margin *better* than `IS_CAGRSLACK` does
(+0.3985 vs +0.3570). Top-set overlap with `IS_CAGRSLACK` at D = 480 runs **64.6%** (q = 0.10)
to **76.7%** (q = 0.25). The book statistic is ~90% rank-explained by a number that never sees
the book.

## 4. Rule 8, 2017–2026 read ONCE — the naive chooser reaches MORE 4b passes than the book one

| panel | kind | picks | 4b BOTH | 4b OOS | 4b FULL | 4a FULL | 4a OOS |
|---|---|---|---|---|---|---|---|
| U56 | BOOK | 16 | 13 | 13 | 13 | **2** | 2 |
| U56 | **NAIVE** | 20 | **14** | 14 | 14 | **0** | 3 |
| B136 | BOOK | 16 | 0 | 0 | 2 | 0 | 0 |
| B136 | NAIVE | 20 | 0 | 0 | 3 | 0 | 0 |

At D = 24, 96 and 240 the naive chooser picks the **identical draw** the book chooser picks —
18, 30 and **166**, the latter being 1749's own headline book. At D = 480 it diverges and picks a
**better** one: draw 364, OOS **12.90% / 1.3088 / −15.33%** against draw 166's
11.74% / 1.3112 / −13.16%, i.e. +1.16 pp of OOS CAGR and a +2.20 pp CAGR-floor margin against
draw 166's +1.04 pp. (SPY OOS 15.29% / 0.8751 / −33.72%; live RULES v2 OOS 9.46% / 1.2767 /
−12.05%; 4b OOS bars: DD cap −20.23%, CAGR floor 10.70%.)

**The single thing the book statistic buys.** Path **4a FULL is reached at 2 of 16 BOOK picks and
0 of 20 NAIVE picks** (`IS_SHARPE`, D = 96/240, draw 76: FULL 10.23% / 1.3264 / −11.75%, OOS
10.28% / 1.2846, and it *fails* 4b on the CAGR floor). Beating the live low-return book on Sharpe
in both halves is the one target a pure trailing-return ranking cannot find. That is the residual
information content of 1749's chooser, and it is worth 2 picks out of 16 on a path 1749 did not
claim.

## 5. Why this had to be true — the binding leg

Of the 375 U56 draws failing 4b OOS, **375 fail on the CAGR floor**, 1 on OOS Sharpe and **0 on
drawdown** (1749 read 373/373/1/0). The 4b OOS bar is, on this construction, a **return floor
with two nearly free companions**, and `IS_CAGRSLACK` is by construction an IS CAGR. A statistic
whose target is "did this basket compound fast enough" is approximated to ρ = +0.90 by "did these
names go up", because on a 56-name current-constituent list over 2009–2016 the two are nearly the
same question.

## 6. Cost ladder (reported, not tuned) — U56, 480 draws

| | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---|---|---|---|
| 4b FULL | 57 | 43 | 29 | 13 |
| 4b OOS | 124 | 105 | 78 | 51 |
| 4b BOTH | 55 | 42 | 28 | 13 |

Draw 364 (the naive rule-8 pick) clears 4b FULL **and** OOS at **all four rungs** — OOS 13.10% /
1.3278 at 0 bps down to 12.07% / 1.2326 at 50 bps.

## 7. Gates — 9/9

G1 runner == `engine.backtest` on returns AND turnover, both panels (worst |d| 1.804e-16); G2
cost identity (3.123e-17); G3 cross-run replication of 1749/1775 (base 42/480, top decile 25/48,
exact); G4 no statistic reads an OOS row; G5 exactly two tuned dials; G6 3,840 of 3,840 cells
published; G7 seed stream unchanged from 1632/1749/1775; G8 max realised target gross 0.750000;
G9 the naive controls are bit-identical under a permuted band.

## 8. What the record should now say

1749's wording — *"the NAME SET is a REACHABLE axis"* — survives; its **mechanism claim does
not**. The axis is reachable by a statistic that never runs the book, so the lift is evidence
about **trailing returns on a current-constituent list**, not about the band book. Three
consequences:

1. **1749's KEEP-4b memo point 2** ("this is name-set information") should read *"this is
   trailing-return information on a survivorship-biased list"*. The chooser is a
   momentum/survivor screen wearing a backtest.
2. **Memo point 10(a) is now partly answered.** 1749 named a point-in-time U56 vintage as what
   would kill it. This run shows the chooser it would have to survive is literally
   "buy the 20 names that went up most", which is exactly the selection a vintage-honest list
   removes. The +1.04/+2.20 pp OOS CAGR margins are upper bounds and should be read as such.
3. **A 4b pass reached by a zero-backtest chooser is recorded** (draw 364, §4) and a memo is
   written for the record — **but it is recorded-not-recommended**, for the reason this run
   exists. See `2026-09-22_naive-trailing-return-chooser_KEEP4b_MEMO.md`.

**SURVIVORSHIP (PROTOCOL rule 9), first-order.** U56 and B136 are CURRENT-constituent lists. This
run is a direct measurement of the exposure rather than a control for it: a trailing-return
chooser over survivors is the purest form of it, and the fact that it *wins* is the finding.
