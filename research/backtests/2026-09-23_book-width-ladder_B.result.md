# idea 2467 (lane B, run 53, 2026-09-23) — IS THE CANDIDATE'S 4b PASS A BOOK-WIDTH EFFECT, AND DOES A ONE-INSTRUMENT BAND BOOK REACH IT AT A TENTH OF THE TURNOVER?

**ANSWERED = NO, TWICE OVER. KILL of book width as a turnover device, and — via the single-instrument limit — a CONFIRM that the standing 4b candidate's whole margin is CROSS-SECTIONAL, not timing. NO KEEP-CANDIDATE, NO RULES CHANGE.**

Script `research/backtests/2026-09-23_book-width-ladder_B.py`, **1,600 published rows** over 400 realised weight paths, **16 of 16 gates pass** (G3 `K = ALL` is the committed CAP2 book to max|d| **0.000e+00** on both panels against an independent construction; G3b reproduces the committed U56 headline 11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318, turnover 3.51x to 3.95e-05; G1 replica == `engine.backtest` to 0.000e+00).

## The premise, and why it was wrong

Run 51's diagnosis: *"a device that cuts turnover without cutting exposure remains the only thing that would work."* Run 50 proved by identity that the committed candidate IS "hold every in-band name at 2% of NAV, ceiling `g`, residual to SHY", leaving only two moving parts — the band, and **how many instruments the rule is run over**. The filed argument was that turnover is roughly LINEAR in the number of positions rebalanced while gross is `g x` the in-band fraction, a breadth statistic largely invariant to width.

**Both halves of that argument are false, and the run says exactly why.**

## 1. TURNOVER IS FLAT IN WIDTH, BECAUSE NARROWING THE BOOK CONVERTS RISK-LEG CHURN INTO SWEEP-LEG CHURN ALMOST ONE-FOR-ONE

Turnover is `sum |dw|` in NAV units, and position size scales as `1/K`, so fewer positions each move proportionally more. Worse, a narrow book's gross swings the full `0 -> g` on a single flip, and the SHY sweep must absorb every bit of that swing. Headline convention (SHY sweep, g 0.75, 10 bps), turnover per year split **total = risk leg + sweep leg**:

| panel | K=1 | K=2 | K=4 | K=8 | K=16 | K=32 | ALL (committed) | SPYONLY |
|---|---|---|---|---|---|---|---|---|
| U56 total | 2.85 | 3.66 | 3.89 | 3.51 | 3.80 | 3.57 | **3.51** | 1.99 |
| U56 risk / sweep | 1.42 / **1.42** | 2.29 / 1.37 | 2.64 / 1.26 | 2.52 / 0.98 | 2.83 / 0.97 | 2.71 / 0.86 | 2.70 / **0.80** | 1.00 / 1.00 |
| B136 total | 3.21 | 4.45 | 5.12 | 5.59 | 5.12 | 4.76 | **4.68** | 1.99 |
| B136 risk / sweep | 1.60 / **1.60** | 3.28 / 1.17 | 4.35 / 0.77 | 4.89 / 0.70 | 4.55 / 0.57 | 4.28 / 0.48 | 4.29 / **0.39** | 1.00 / 1.00 |

The risk leg does fall (U56 2.70 -> 1.42) — and the sweep leg rises by almost exactly as much (0.80 -> 1.42). **The best the whole width dial does against idea 2431's -31.0% adoption bar is -18.8% (U56 K=1) and -31.4% (B136 K=1), and at intermediate widths turnover RISES** (U56 K=4 3.89x, +11.0%; B136 K=8 5.59x, +19.6%). **0 of 14 seed-mean width arms clear the 2.42x bar except the two SPYONLY cells** (1.99x), which fail 4b outright.

## 2. WIDTH IS ALSO AN EXPOSURE DIAL, WHICH THE PREMISE DENIED

Mean realised risk gross falls monotonically as the book narrows — U56 **0.672 (ALL) -> 0.670 / 0.665 / 0.663 / 0.625 / 0.568 / 0.516 (K=1)**, B136 **0.736 -> 0.519** — a range of **0.156 / 0.217 of NAV** (G8, published). A wide book only de-grosses when breadth falls below 67%; a narrow book de-grosses linearly in breadth. So width fails the one test that distinguished it from the eleven devices the record has already closed.

## 3. THE 4b PASS COLLAPSES MONOTONICALLY AS THE BOOK NARROWS

4b pass rate over all 1,600 rows by width: **ALL 20/32 (62.5%) -> K32 103/256 (40.2%) -> K16 68/256 (26.6%) -> K8 18/256 (7.0%) -> K4 24/256 (9.4%) -> K2 0/256 -> K1 0/256 -> SPYONLY 0/32.** At the headline cell the seed-mean pass rate reads U56 **1.00 / 0.625 / 0.500 / 0.125 / 0.250 / 0.00 / 0.00** and B136 **1.00 / 0.500 / 0.250 / 0.00 / 0.00 / 0.00 / 0.00** walking ALL -> K=1. **4a is 0 of 1,600** — no width, seed, gross, sweep or rung beats live RULES v2 in both halves without a worse drawdown.

## 4. THE SINGLE-INSTRUMENT LIMIT: THE 200d BAND ON SPY ALONE EARNS NOTHING

`SPYONLY` — hold SPY when it is above its own 200d +/-3% band, else bills — is the canonical version of this family's timing rule with the cross-section removed, and it was named in QUEUE.md before compute. U56, SHY sweep, g 0.75, 10 bps: **7.84% CAGR / Sharpe 0.8375 / MaxDD -20.07%, halves 0.92 / 0.77, OOS 8.40% / 0.8544, turnover 1.99x**, against SPY buy-and-hold's **15.23% / 0.8897 / -33.72%, halves 0.96 / 0.84, OOS 0.8784**.

**Leg string 00010: it fails `L_H1`, `L_H2`, `L_OOS` and `L_CAGR`, and passes only `L_DD` (margin +0.16 pp).** The timing rule buys drawdown and nothing else — it does not improve risk-adjusted return over simply owning the index in either half or out of sample. Every bit of the standing candidate's 4b margin is therefore **cross-sectional**: it comes from applying the band to many names and letting breadth size the book, not from the band itself. This is the one arm in the run with **no survivorship exposure at all**.

## 5. RULE 8 IS UNANIMOUS

Both dials fitted on warm-up..2016-12-31 only, on the **seed mean** so no seed is selectable either, 2017-2026 read ONCE, 32 picks (2 panels x 2 sweeps x 4 rungs x 2 choosers): **32 of 32 land on `K = ALL`, 0 of 32 on any narrower book** (24 at g 0.75, 8 at g 1.00). Picks beat SPY's OOS Sharpe 32 of 32, the live book's 12 of 32, the committed cell's 8 of 32 (all of them the `ALL / g1.00` B136 ZERO cells, i.e. a gross decision, not a width one). Mean OOS **12.36% / 1.1529 / -17.57%** against the committed cell's **11.50% / 1.1489 / -16.28%** at **4.04x turnover vs 3.80x** — more turnover for +0.0040 of Sharpe.

## The 18 rows that clear both 4b and the turnover bar, and why they are NOT candidates

18 of 1,600 rows pass 4b at turnover <= 2.42x. **Every one is a single SEED** (U56 / ZERO sweep / K=4 seed 2, K=8 seeds 1 and 3, K=16 seed 4). The seed is a published distribution, never a dial: their own width's seed-mean fails 4b (K=4 2 of 8, K=8 1 of 8), rule 8 picks that width 0 of 32 times, and an operator cannot implement "the right 4 of 56 names" without knowing them in advance. They are recorded here and **filed as seed lotteries, not KEEP-candidates**. The only 3 narrow cells that dominate the committed cell on OOS Sharpe AND turnover are likewise single seeds at K=32 with turnover 1-3% below ALL's.

## Survivorship (PROTOCOL rule 9)

U56 and B136 are CURRENT constituents of their screens held from 2008, so a narrow random sub-book of survivors is a narrow book of WINNERS. **Every small-`K` result above is therefore biased in the device's favour and must be read as an upper bound** — the collapse is, if anything, understated. `SPYONLY` is the one arm with no survivorship exposure.

## What this closes

Width joins admission (2447), exit (2351, 2328), re-size magnitude (2391, 2404, 2408), the re-size trigger (2457, an identity), de-grossing (2443), the extended-name trim (2419), the breadth cap (2387) and the ETF exclusion (2435). **The last structural dial the committed candidate had is now priced, and the turnover is the price of the diversification that earns the pass.** Idea 2431's adoption bar — 3.51x -> 2.42x at unchanged returns — stands unmet, and this run is evidence it may be unreachable by construction rather than by search: the only thing that cuts the risk leg also hands the saving straight to the sweep leg and removes the cross-section the pass is made of.

No change to `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py` (rule 6). The live book and the standing 4b candidate are unchanged.
