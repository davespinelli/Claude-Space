# Idea 126 — execution-lag-sensitivity-of-the-whole-price-list (lane C, 2026-09-05)

**Verdict: ANSWERED — and it is a KILL of the queue's speed-threshold hypothesis.**
The execution convention is a **first-order axis of the price list**, not a nuisance. Idea 96's
sign flip was not a stop-specific curiosity: the **median published price moves 84% of its own
value** when execution moves by one bar or to the next rebalance, and **no speed threshold
separates the stable rows from the unstable ones** — so PROTOCOL cannot quote one. What it can
quote is a lag band on every price.

Script: `2026-09-05_execution-lag-sensitivity-of-the-price-list_C.py`
Outputs: `.console.txt`, `.pricelist.csv` (612 rows), `.stability.csv` (204), `.grid.csv` (408),
`.walkforward.csv` (60), `.paramgrid.csv` (9).

## What was run

Idea 94's entire menu — 3 books (V1u 5-name, TOP20, EWall 56/136-name) × 17 treated arms
(5 gates × {de-gross, reweight}, 2 trailing stops, 2 book DD controls, 2 entry budgets) ×
2 universes × 2 cost rungs (10, 25 bps) — re-priced at three execution conventions:

| lag | convention |
|---|---|
| `t+1` | decide at close t, trade at close t+1 — **PROTOCOL rule 2, the published one** |
| `t+2` | decide at close t, trade at close t+2 |
| `nr` | decide at rebalance d, trade at the execution bar of rebalance d+1 (nothing moves faster than the cadence) |

The lag is applied to **every** moving part: target book, gate, per-name stop exit, the DD
control's own equity reading, and the entry budget. The `t+1` simulator reproduces idea 94's
`run()` **exactly** (max|diff| = 0.000e+00 over 51 arm-points per universe) and reproduces
`engine.backtest` exactly for the controls, so this is an audit of that file's numbers, not a
re-derivation. Costs 10 bps inside the loop, weekly, long-only, no leverage.

Tuned parameters: **two, both of the test** — `floor` ∈ {0.10, 0.50, 1.00} pp and `tol` ∈
{0.25, 0.50, 1.00}. All 9 points reported. Headline (0.10, 0.50) = idea 94's own floor and a
deliberately generous tolerance. No trading parameter is tuned anywhere in this run.

## Headline numbers

Of the 192 menu rows, **138 were priceable at t+1** at all (finite rate, dMaxDD > 0.10 pp).
Both stops are already unpriceable at t+1 in **24 of 24** rows — idea 96's sign-flipping row
never entered the published price list.

| bar | rows | result |
|---|---|---|
| sign-stable (dMaxDD > 0.10 pp at all three lags) | 138 | **126 (91.3%)**; 6 denominators flip sign outright |
| **lag-stable** (sign + rate within 50% of its t+1 value) | 138 | **48 (34.8%)** |
| lag-stable at tol = 0.25 | 138 | 20 (14.5%) |
| lag-stable at tol = 1.00 (the price may double) | 138 | 78 (56.5%) |

The floor is nearly inert (0.10 → 1.00 pp moves sign-stability 126 → 103 and lag-stability not
at all, 48 → 48); **the tolerance is what binds**. Median relative rate swing = **0.84**.

**P1 CONFIRMED — the lag axis is bigger than the instrument axis.** Median lag swing of dMaxDD
**1.858 pp** (mean 2.133, p90 3.958, max 6.181) against a median within-family instrument
spread of 1.731 pp. Per family the lag swing is 1.20 pp (dd, whose family spread is 0.00),
1.30 (bud, spread 2.04) and 2.28 (gate, spread 5.47): the gate family is the only one where
choosing the instrument matters more than choosing the execution bar.

**P2 CONFIRMED — fewer than half survive.** 34.8% at the headline.
By universe: u56 45.7%, broad 23.5%. By book: **EWall 52.1%, TOP20 28.6%, V1u 22.0%**.
By family: **dd 75.0%, bud 35.7%, gate 25.0%, stop 0 of 0 priceable**. By cost: 35.3% / 34.3%
— the cost rung is irrelevant to lag stability.

**P3 SPLIT — the book half is right, the speed half is wrong.** The 5-name V1u book is the
least stable and the 56-name EWall the most, as predicted. But there is **no speed threshold**:
Spearman(dTO, lag swing) = **0.172**, Spearman(dTO, lag-stable) = **0.045**, and the dTO ranges
of stable and unstable rows overlap completely (stable rows run up to +6.79 turnover/yr,
unstable rows down to −19.12/yr). Within the gate family — the one place where speeds share
units — Spearman(gate flips per ticker per year, lag swing) = **−0.297**: the *faster* gates are
if anything the *more* lag-stable ones. The slowest instrument on the menu (`ddctl`, 0.5
episodes/yr) is the most stable family at 75%, but the second-slowest (`band3`, 1.8 flips/tkr/yr)
sits at 25–36% while the fastest (`v1gate-dg`, 7.8 flips/tkr/yr) is 70%. Speed does not order it.

**Both KEEP paths are lag-dependent.** Across the 204 book×arm×cost×lag rows:
4a passes 56 (t+1) / 61 (t+2) / 50 (nr) and **flips with the lag in 22 rows**;
4b passes **29 / 25 / 14** and **flips in 41 rows (20%)**. Slowing execution to the rebalance
cadence halves the 4b pass count. Both stops on broad EWall/TOP20 pass 4b at t+2 and at no
other lag — the same arm, the same data, a one-bar convention change.

## Rule 8 walk-forward (required)

Instrument chosen on 2009–2016 only at the published lag t+1, evaluated untouched on 2017–2026
at all three lags. S1 = idea 94's selector (lowest IS rate among arms buying ≥ 1.0 pp of IS
MaxDD); S2 = the same restricted to arms lag-stable **on IS data only**.

| selector | lag | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS dMaxDD vs control | control Sharpe | v1 Sharpe | SPY Sharpe |
|---|---|---|---|---|---|---|---|---|
| S1 (n=12) | t+1 | 8.9% | 0.801 | −19.0% | +4.35 pp | 0.852 | 0.469 | 0.882 |
| S1 | t+2 | 8.8% | 0.785 | −19.5% | +4.87 | 0.833 | 0.432 | 0.882 |
| S1 | nr | 8.7% | 0.762 | −20.3% | +3.44 | 0.811 | 0.388 | 0.882 |
| S2 (n=8) | t+1 | 8.3% | 0.803 | −17.8% | +5.91 | 0.837 | 0.439 | 0.882 |
| S2 | t+2 | 8.1% | 0.769 | −19.1% | +5.68 | 0.819 | 0.403 | 0.882 |
| S2 | nr | 7.7% | 0.711 | −19.7% | +4.53 | 0.777 | 0.323 | 0.882 |

Both selectors **lose to their own ungated control on OOS Sharpe at every lag** and both lose to
SPY's 0.882; both beat live RULES v1. The lag screen (S2) does not improve the selection — it
costs 0.09 of mean OOS Sharpe at `nr` and gains nothing at `t+1`. The OOS *purchase* is mostly
robust (1 of 20 picks flips sign: broad EWall `stop25`, −1.21 / +6.38 / −0.22 pp).

**P4 REFUTED as literally worded, and the refutation is the finding.** 20 of the 60 pick-rows
pass 4b — but of the 20 distinct picks, **only 5 pass 4b at all three lags, 5 pass at only one or
two, and 10 never pass**. A quarter of the picks have a KEEP verdict that exists only under one
execution convention. (4a: 4 / 3 / 13.) The five that survive every lag are `band3-rw` on
u56/EWall at both cost rungs and `ddctl-8/.5/recover` on u56/TOP20 at 10 bps.

## What this means for the project

1. **No price on idea 74/94's menu is quotable to the precision it was published at.** Two
   thirds move by more than half their own value under a convention change that no price claim
   ever depended on. The sign is mostly fine (91%); the *number* is not.
2. **The queue's conditional resolves to its second branch.** "If the slow instruments are stable
   and only the fast ones are not, PROTOCOL can quote a speed threshold" — they are not, and it
   cannot. Nothing about an instrument's trigger rate predicts whether its price survives.
3. **Proposed PROTOCOL clause (for Sunday review, not applied here).** Add to rule 4:
   *"Any ratio whose denominator is a drawdown difference must be published as a band across
   execution conventions {t+1, t+2, next-rebalance}, quoting the t+1 value and the width of the
   band. A ratio whose band exceeds 50% of its t+1 value is reported as the (dCAGR, dMaxDD) pair
   with its lag swing, never as a rate. A KEEP verdict that holds at t+1 but not at all three
   conventions is PARK, not KEEP."*
   Under that clause 41 of 204 rows lose their 4b verdict and 90 of 138 rows lose their rate.
4. **It does not touch the live book.** The current KEEP 4b candidate (top-20 equal-weight, no
   vol scaler) is a *book*, not a drawdown instrument, and carries no published price. Nothing
   here argues for or against it.

## Caveats

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every
absolute level is optimistic. This run reports within-cell differences and the stability of a
number, which are far less exposed than levels — but a survivorship-free panel could move which
rows pass. The calendar-day index (queue idea 38) is unfixed and applies here as everywhere: a
"one-bar" lag is one calendar day, which across a weekend is three. That makes `t+2` a slightly
harsher perturbation than a trading-day index would give, and is a reason the `nr` column — which
is cadence-defined and index-independent — is the more trustworthy of the two perturbations.
`nr` is also where the 4b pass count collapses (29 → 14), so the finding does not rest on the
index bug.
