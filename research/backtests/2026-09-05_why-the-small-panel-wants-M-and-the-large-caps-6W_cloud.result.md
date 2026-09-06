# Idea 188 — why-does-the-small-panel-want-M-and-the-large-caps-6W (cloud, 2026-09-05)

**ANSWERED, and the answer is SIGNAL, not COST. The M-minus-6W gap is almost entirely a
forecast-horizon effect: on the sub-$2B panel the composite's rank IC is dead by h = 30 bars
(IC(30)/IC(21) = 0.24 full-sample, −0.17 out of sample), while on U56 and ETF36 it is still
*rising* at h = 84 (ratios 1.08 / 1.06). Pricing turnover explains 6–8% of the gap and nothing
more. The universe clause idea 77 wants is written below. No RULES change, no new book; one
by-product 4b passer memo'd and NOT proposed.**

Script `2026-09-05_why-the-small-panel-wants-M-and-the-large-caps-6W_cloud.py`; artefacts
`.console.txt`, `.ladder.csv`, `.paired.csv`, `.episodes.csv`, `.decay.csv`,
`.walkforward.csv`, `.refs.csv`. 49 s.

## Design and reproduction

Idea 175's script imported verbatim (`cad_mask`, `fast_backtest`, `Book`, `build_corpus`,
`family_of`, `rel_margin`, `keep_4a`, `keep_4b`, the 7-point ladder and the 115-book corpus).
7 cadences × 115 books × 3 cost rungs = **2415 rung-rows**, t+1, IS ≤ 2016-12-31,
OOS ≥ 2017-01-01 read once. The book is idea 2's 4b candidate throughout (top-20 EW on the
scan.py composite, no vol scaler, gross 0.75, bare 200d gate, vol20 < 0.60); **only cadence
moves.**

**The cost axis is derived, not re-simulated.** `net(c) = gross − turnover·c/1e4` exactly,
so the 0 / 10 / 25 bps books are the *same book, bar for bar* and the cost/signal split is an
identity rather than two noisy runs. Control **[d]**: max |direct − derived| over 3 books ×
7 cadences × 3 rungs = **0.000e+00**.

Asserted before any new number: `cad_mask` == `engine.rebalance_mask` at D/W/M/Q;
`fast_backtest` == `engine.backtest` (max |dret| 1.4e-16); CAND-20 weights == idea 78/171's
`weights_cand` at 0.000e+00; numpy metric kernels == `engine.metrics` at **0.000e+00**; and
**the derived 10 bps rung matches idea 175's committed `ladder.csv` on all 805 rows at
7.1e-15 with 0 verdict mismatches.** Idea 175's headline re-derives: its published M +0.0978
and 6W +0.0163 on the small family differ by +0.0815, which is exactly this run's SMALL
M-minus-6W OOS Sharpe gap at 10 bps.

## Q2/Q3 — the gap, and how little of it is cost

M minus 6W, paired over books (positive = the faster of the two wins):

| score | family | n | 0 bps | 10 bps | 25 bps | cost effect (10 − 0) |
|---|---|---|---|---|---|---|
| Sharpe | SMALL | 49 | **+0.1107** (t +7.78) | +0.1033 | +0.0921 | **−0.0074** |
| Sharpe | U56 | 33 | −0.0059 (t −1.44) | −0.0111 | −0.0189 | −0.0052 |
| Sharpe | ETF | 33 | +0.0143 (t +3.12) | +0.0099 | +0.0033 | −0.0044 |
| OOS Sharpe | SMALL | 49 | **+0.0902** (t +4.19, 35W) | +0.0815 | +0.0684 | **−0.0087** |
| OOS Sharpe | U56 | 33 | **−0.1106** (t −13.33, **0W/33L**) | −0.1171 | −0.1269 | −0.0065 |
| OOS Sharpe | ETF | 33 | **−0.0807** (t −15.28, **0W/33L**) | −0.0870 | −0.0964 | −0.0062 |

**COST IS NOT THE MECHANISM.** Turnover pricing moves the gap by 0.004–0.009 of Sharpe
between 0 and 25 bps — **6–8% of the SMALL gap's magnitude** — and it moves *every* family in
the same direction (toward 6W, the slower point) rather than splitting them. The whole split
is already present at **zero cost**, where the small panel prefers M by +0.1107 and U56
prefers 6W by 0.0059 with the OOS reading 0 wins out of 33 books.

On OOS Sharpe the three-way sign split (SMALL +, U56 −, ETF −) holds at **9 of 9** family ×
rung cells. On full-sample Sharpe it does not: ETF is weakly positive (+0.0143 → +0.0033), so
P4 as written misses. The family-mean ladder argmax on OOS Sharpe is **M on SMALL and 6W on
U56 and ETF at all three rungs** — the queue's premise, confirmed and now cost-independent.

## Q4 — holding-episode length (idea 76 / idea 9's instrument)

`persistence` = mean holding-episode length ÷ the cadence's block length. ≈1 means the book
re-picks from scratch every block; ≫1 means names survive rebalances and the dial barely moves
the book.

| family | M: blk bars | mean episode | **persistence** | ep/yr | turn/yr | 6W: persistence | turn/yr |
|---|---|---|---|---|---|---|---|
| SMALL (49 books) | 20.9 | 72.9 d | **3.48** | 45.9 | 3.58 | 3.07 | 2.89 |
| U56 (33 books) | 20.9 | 137.2 d | **6.55** | 32.5 | 2.58 | 5.66 | 2.14 |
| ETF (33 books) | 20.9 | 177.1 d | **8.46** | 17.6 | 1.39 | 7.24 | 1.15 |

On the **fixed** panels (no sub-panel averaging) the split is sharper still: at M, SMALL439's
persistence is **1.90** (mean episode 39.7 d on a 20.9-bar block) against U56's **4.18** and
ETF36's **5.71**. A small-cap book at monthly cadence turns over roughly half its names every
other block; a mega-cap book holds the same names through four to six blocks. **The cadence
dial is a much bigger intervention on the small panel than on the large ones**, which is why
its cadence answer can differ at all.

Turnover on its own still does not explain the direction: SMALL turns 3.58×/yr at M vs U56's
2.58× — the small panel is the *more expensive* one, so cost alone would push it toward 6W,
not M. It goes to M anyway.

## Q5 — realised signal decay, the mechanism

Cross-sectional rank IC of the composite against forward h-bar returns, among **eligible**
names only (the discrimination the book actually uses):

| window | panel | h=5 | h=10 | **h=21 (M)** | **h=30 (6W)** | h=42 | h=63 | h=84 | **IC(30)/IC(21)** |
|---|---|---|---|---|---|---|---|---|---|
| FULL | **SMALL439** | 0.0109 | 0.0115 | **0.0070** | **0.0017** | −0.0023 | −0.0027 | −0.0070 | **0.241** |
| FULL | U56 | 0.0475 | 0.0602 | 0.0740 | 0.0800 | 0.0867 | 0.1064 | 0.1238 | **1.081** |
| FULL | ETF36 | 0.0394 | 0.0471 | 0.0498 | 0.0528 | 0.0540 | 0.0751 | 0.0920 | **1.061** |
| OOS | **SMALL439** | 0.0122 | 0.0132 | 0.0068 | **−0.0011** | −0.0053 | −0.0043 | −0.0075 | **−0.168** |
| OOS | U56 | 0.0550 | 0.0684 | 0.0724 | 0.0748 | 0.0865 | 0.1269 | 0.1434 | 1.033 |
| OOS | ETF36 | 0.0452 | 0.0568 | 0.0519 | 0.0528 | 0.0601 | 0.1082 | 0.1303 | 1.018 |

**The curves have opposite slopes.** On the small panel the composite's IC peaks at h ≈ 10,
has lost 76% of its h=21 value by h=30, and is **negative** past h=30 out of sample — a
30-bar hold is on the wrong side of the signal. On U56 and ETF36 the IC *increases*
monotonically out to h=84; these are longer-horizon momentum panels where holding longer is
strictly better information, and the 6W point is not "stale", it is closer to the signal's
natural horizon. The realised top-20-minus-eligible-mean excess says the same in return
units: SMALL439 decays 5.74% → 1.76% annualised across the horizon grid while U56 is flat
(3.66% → 3.38%) and ETF36 is flat and small (1.11% → 0.85%).

The IS window shows the same ordering with a milder small-panel slope (0.843 vs 1.135/1.118),
so this is not an OOS-only artefact — but see the caveat below: the level of every small-panel
IC is survivorship-inflated and the ratio is only safe if that bias is horizon-neutral, which
cannot be shown from this data.

## Q6 — rule 8, and the disagreement between the Sharpe argmax and 4b

Pooled OOS by arm (chose on ≤ 2016-12-31 only; ORACLE is not implementable):

| family | CONST-W | **CONST-M** | **CONST-6W** | SEL-SHARPE | SEL-4B | ORACLE |
|---|---|---|---|---|---|---|
| SMALL @10 bps | 0.2052 | **0.3030** | 0.2215 | 0.2525 | 0.2497 | 0.3692 |
| U56 @10 bps | 1.2230 | 1.2699 | **1.3870** | 1.2236 | 1.1902 | 1.3873 |
| ETF @10 bps | 0.8413 | 0.9143 | **1.0013** | 0.9058 | 0.8931 | 1.0228 |

**On U56 and ETF the pre-registered constant 6W is within 0.0003 and 0.0215 of the ORACLE**,
and on SMALL the constant M beats both fitted selectors at every rung (0.3030 vs SEL-SHARPE's
0.2525 at 10 bps). This is the twelfth-odd instance of the project's do-nothing result: the
right move is to *know which panel you are on*, not to fit the dial per book.

But **the 4b verdict inverts the U56 Sharpe ranking**. On the fixed U56 panel, 6W has the best
Sharpe at every rung (1.2252 @10 bps vs M's 1.2081) and **fails 4b on drawdown at every rung**
(−21.99% against the cap 0.60 × |SPY −33.72%| = −20.23%), while **M passes 4b at 0, 10 AND
25 bps**. SPY on the same window: 15.23% CAGR / 0.8890 Sharpe / −33.72% MaxDD (H1 0.9566,
H2 0.8340). This is idea 152's Sharpe-vs-4b-margin sign flip, reproduced on the cadence dial.

KEEP paths over all 805 ladder rows: 4b 87 → 59 → 30 as cost rises 0 → 10 → 25 bps, while 4a
rises 99 → 195 → 392 (its comparator, RULES v1, is the higher-turnover book and is re-costed
at the same rung). On the fixed panels **every 4b pass at every rung is U56** — SMALL439 0/7
and ETF36 0/7 at 0, 10 and 25 bps. Idea 136's small-panel null reproduces once more, now on
the cadence dial and at three cost rungs. RULES v1 OOS: U56 0.9780 → 0.7471 → 0.3992;
SMALL 0.7090 → 0.4923 → 0.1673.

## Q7 — the universe clause (the output idea 77 asked for)

> **Cadence is not a free parameter and it is not a cost parameter — it is a property of the
> panel's forecast horizon.** Set the rebalance interval from the panel's realised rank-IC
> decay, not from a fitted argmax and not from a turnover budget: where the eligible-name IC
> is still rising at h = 30 bars (U56 1.08, ETF36 1.06), hold longer; where it has lost more
> than half its h = 21 value by h = 30 (SMALL439 0.24), do not. The decision is
> cost-insensitive over 5–25 bps: pricing turnover moves the M-vs-6W margin by under 0.009 of
> Sharpe, 6–8% of the effect it would have to explain.

Two limits stated with it: the clause is measured on three panels and one composite, and the
small-panel leg of it rests on a survivorship-inflated IC whose horizon-neutrality is
unverified.

## By-product, memo'd and NOT proposed

`U56 + top-20 EW + gross 0.75 + MONTHLY` passes 4b at 0, 10 and 25 bps (see
`.memo.md`). It is not new — it reproduces the standing candidate the queue already carries as
idea 182 — and it is **single-universe**: the same construction is 0/7 on SMALL439 and 0/7 on
ETF36 at every rung, which is idea 53's cross-universe failure. Nothing is proposed for
Sunday review.

## Predictions

5 of 7 hit. **P1** (reproduction), **P2** (additivity), **P3** (the gap survives at 0 bps,
+0.1107), **P5** (IC(30)/IC(21) smaller on SMALL: 0.241 vs 1.081) and **P6** (persistence at M
lower on SMALL439: 1.90 vs 4.18) all hit. **P4** missed: the three-way sign split is 9/9 on
OOS Sharpe but ETF is weakly *positive* on full-sample Sharpe. **P7** missed: 4 / 3 / 2
fixed-panel 4b passes at 0 / 10 / 25 bps, all U56, all re-cadencings of a book already in the
record (idea 144).

## Caveats (also in the script docstring)

SURVIVORSHIP (idea 54) — SMALL439 is the sub-$2B screen with the 44 `max_1d_move ≥ 1.0` names
dropped and is a **current-constituent list**; U56 and ETF36 are current lists too. Every
cadence inherits it equally so the paired M-minus-6W comparison is unaffected, but every LEVEL
is biased upward and no small-panel CAGR or Sharpe here is attainable. **The bias is not
neutral for Q5:** removing the names with the worst forward returns inflates the measured IC
at every horizon, and the cross-panel comparison read here is the *shape* of the decay curve,
which is still contaminated if the bias is horizon-dependent — that cannot be ruled out from
this data. Idea 38: prices.csv is calendar-day indexed from 2014-09-17, so M and 6W are
slightly different bar counts on U56/ETF36 than on the small panel; the realised counts
(20.93/28.93 vs 20.94/29.01) are measured in Q4 rather than assumed. The books are not
independent (112 of 115 are sub-panels of three parents), so every paired t is over correlated
units and the exact sign test sits beside it. The three cost rungs share one simulation per
book × cadence, so they are perfectly paired and carry no simulation noise — and are therefore
not three independent replications. Cost is a flat linear bps charge on turnover; real cost is
spread plus impact and scales with liquidity, so 10 bps on a 439-name sub-$2B panel is not the
same instrument as 10 bps on U56, and that alone is the largest reason the SMALL numbers here
are soft.
