# Idea 38 — small-cap-momentum-clean (cloud lane, 2026-09-04)

**Verdict: KILL — 0 of 8 grid points pass PROTOCOL 4a or 4b.** But the run overturns one
sub-conclusion of ideas 39/49 and localises the damage they found.

Script: `research/backtests/2026-09-04_small-cap-momentum-clean_cloud.py`
Console: `2026-09-04_small-cap-momentum-clean_cloud.console.txt`

## Question

Ideas 39 and 49 killed the v1 *composite* book (mean pct-rank of 12-1, 6m and 3m, gated on
200d-MA **and** vol20<0.60) on the sub-$2B panel and concluded the momentum ranking was
"close to irrelevant" there — the whole f-sweep sat in a 3.5–6.2% CAGR band under a 10.2%
unfiltered control. Idea 38 as filed asks the cleaner question: does **plain 12-1
momentum** — no rank blend, no vol scaler, no vol20 gate — rank small caps at all?

## Design

439 names (483 less the 44 with `max_1d_move >= 1.0` in `data/small_meta.csv`); SPY is a
benchmark column and is never holdable. Signal `px.shift(21)/px.shift(252)-1`. Book: top-n
equal-weight at 0.75/n (75% gross, v1's own), cash if fewer than n eligible. Weekly, t+1,
10 bps. Sample 2011-01-13 → 2026-09-03. Exactly two tuned parameters — n ∈ {10,20,40,60}
and the 200d gate ∈ {ON, OFF}; **all 8 points reported**.

Harness sanity: RULES v1 on the small panel reproduces ideas 39/49 to the decimal
(8.1%/0.602/-32.8%), as does the unfiltered control (10.2%/0.677/-36.2%).

## Results (full sample, vs SPY 14.2%/0.863/-33.7%, halves 0.886/0.864)

| gate | n | CAGR | Sharpe | MaxDD | H1/H2 | OOS Sh | turn | fails 4b on |
|---|---|---|---|---|---|---|---|---|
| 200d | 10 | 16.0% | 0.698 | -35.6% | 0.721/0.704 | 0.810 | 15.3x | H1,H2,OOS,DD |
| 200d | 20 | 13.4% | 0.693 | -33.0% | 0.755/0.676 | 0.687 | 14.1x | H1,H2,OOS,DD |
| 200d | 40 | 11.4% | 0.693 | -30.3% | 0.746/0.675 | 0.719 | 12.7x | H1,H2,OOS,DD |
| 200d | 60 | 7.6% | 0.531 | -30.2% | 0.546/0.535 | 0.591 | 11.9x | H1,H2,OOS,DD,CAGR |
| none | 10 | 14.9% | 0.646 | -38.9% | 0.640/0.667 | 0.770 | 14.5x | H1,H2,OOS,DD |
| none | 20 | 13.5% | 0.679 | -34.9% | 0.732/0.662 | 0.673 | 12.9x | H1,H2,OOS,DD |
| **none** | **40** | **14.6%** | **0.797** | **-33.9%** | **0.803/0.816** | **0.818** | 11.5x | H1,H2,OOS,DD |
| none | 60 | 10.7% | 0.648 | -36.5% | 0.666/0.654 | 0.664 | 10.5x | H1,H2,OOS,DD |

References on the same window: EW all 439 @75% control 10.2%/0.677/-36.2% (turn 1.7x);
RULES v1 small panel 8.1%/0.602/-32.8%; RULES v1 live (universe.json) 6.3%/0.650/-13.8%.

**0 of 8 pass either path, and none is close on drawdown** — the best point's -33.9% is
13.7pp outside 4b's -20.2% cap, and every point's Sharpe is below SPY's in both halves.

## What is new relative to ideas 39/49

**(1) Pure 12-1 momentum *does* rank on this panel; the composite did not.** `none/n=40`
returns 14.6%/0.797 against the unfiltered control's 10.2%/0.677 — **+4.4pp CAGR and
+0.12 Sharpe over the panel's own beta, net of 11.5x turnover at 10 bps**. Ideas 39/49
found the ranking worth nothing (every arm *below* the control). The difference is not the
lookback: it is that this book drops the `vol20 < 0.60` gate and the 6m/3m blend.

**(2) The gate damage is mostly the vol20 gate, not the 200d MA.** Holding the 12-1
ranking and n=40 fixed: none 14.6%/0.797 → 200d 11.4%/0.693 → vol20 7.4%/0.524 → both
5.6%/0.441. The vol20 filter alone costs 0.27 of Sharpe, the 200d filter alone 0.10.
Ideas 39/49 measured the two gates only in combination with the composite scorer.

**(3) The 200d gate has no stable sign here.** Its Sharpe effect at matched n is +0.053
(n=10), +0.015 (n=20), -0.105 (n=40), -0.117 (n=60): it helps a concentrated book and
hurts a broad one. Neither idea 39's "inverted" nor RULES v1's "the gate is the edge"
survives as a general statement on this panel.

**(4) The honest counter-evidence, and it is decisive against trading any of this.**
Compounded EW decile portfolios by 12-1 momentum (daily, 0 bps, 100% gross) are U-shaped,
not monotone: D1 (best momentum) 21.5%/0.865 but **D10 (worst momentum) 29.2%/0.937** —
higher CAGR *and* Sharpe than the winners — with D2–D9 flat in a 8.0–12.4% band. The
arithmetic D1−D10 spread is **-8.11%/yr, t -1.15**. D10 is exactly the beaten-down cohort
the survivorship bias flatters most (the panel is current constituents of a sub-$2B screen
as of 2026-09-03; names that crashed and delisted are absent), so the D10 figure is not
tradeable — but it means finding (1) cannot be read as "momentum has a real cross-sectional
premium here". Both tails beat the middle, and only one of them is survivorship-clean.

**(5) Costs consume most of the margin.** At 0 bps the best point reads 15.9%/0.856 — it
merely *ties* SPY's 0.863 frictionless. 10 bps 14.6%/0.797, 25 bps 12.6%/0.709, 50 bps
9.4%/0.561. An 11.5x-turnover book on sub-$2B names would realistically pay more than 10.

## Rule-8 walk-forward (IS 2011-01-13→2017-01-03, OOS 2017-01-03→2026-09-03)

Two selection rules fixed before any OOS number was read.
- **plain in-sample Sharpe** picks `none/n=40` (IS 0.785). OOS **16.3%/0.818/-33.9%** vs
  SPY 15.5%/0.884/-33.7% and RULES v1 live 7.8%/0.751/-13.8%. It beats SPY on CAGR and
  loses on Sharpe; it beats the live book on both, at 2.5x the drawdown.
- **4b-aware** picks **nothing**: no in-sample point met the -11.2% in-sample drawdown cap
  (shallowest -20.1%). Same structural outcome as ideas 39, 46 and 49 — a 75%-gross
  small-cap book cannot be made to satisfy 4b's drawdown test by selection alone.

The pick's OOS Sharpe (0.818) exceeded its IS Sharpe (0.785), so this is not an
overfitting signature; the book is simply not better than SPY risk-adjusted.

## Caveats

- **Survivorship, one-directional and large**: current constituents only. It flatters every
  arm, and hardest the ones holding beaten-down names — which is why finding (4) is
  recorded as evidence about the *shape* of the cross-section, not as a strategy.
- **Benchmark**: no IWM/IJR in the cache, so 4b compares a small-cap book to SPY. The
  control comparison in (1) does not depend on the benchmark; the 4b verdict does.
- Costs are modelled at 10 bps flat with no spread/impact term; sub-$2B names would pay
  more, and finding (5) shows the result is cost-fragile.

## Consequence for the Sunday review

Nothing to adopt. The one live-book-relevant item is finding (2): the `vol20 < 0.60` gate
in RULES v1 is the larger of the two eligibility filters by damage on small caps, and it
has never been tested in isolation on `universe.json`, where it is assumed to be part of
the edge. Queued as idea 56.
