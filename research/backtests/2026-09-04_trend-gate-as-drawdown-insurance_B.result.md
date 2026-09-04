# Idea 57 — trend-gate-as-drawdown-insurance (lane B, 2026-09-04)

Script: `research/backtests/2026-09-04_trend-gate-as-drawdown-insurance_B.py`
Console: `2026-09-04_trend-gate-as-drawdown-insurance_B.console.txt`

**Verdict: KILL for the incumbent weekly 200d gate as an insurance instrument — it never
pays at any cost — plus a 4b KEEP-candidate for the cheap instrument that replaces it,
which is the first arm in this project to clear 4b on BOTH large-cap universes.**

## Question

Idea 55 reframed the 200d-MA gate: its return contribution on the large-cap lists is
statistically indistinguishable from zero, but the gate-only control showed it buying
2.5-3.1pp of drawdown for 6.4x/yr of extra turnover. That makes it an insurance contract.
This run prices it: (a) at 5/10/25/50 bps, does the drawdown reduction pay? (b) is a
cheaper instrument — monthly re-evaluation, or a 3%/5% re-entry band — the same insurance
at a fraction of the turnover?

## Design

2 books x 5 gate instruments x 4 cost levels = **40 points per universe, all reported**,
on `universe.json` (56 names) and `universe_broad.json` (136 names). Weekly rebalance,
weights at close t applied at t+1, long-only, 75% gross. 2 tuned params: the instrument
family (continuous / monthly / band) and the band width (3% or 5%). `n=20` and the
`vol20 < 0.60` half of the filter are pre-chosen from ideas 2/55 and are **not** tuned.

* Books — `top20` (idea 2/55's KEEP-candidate construction) and `ew-all` (idea 28's
  equal-weight-every-eligible-name book, the control where idea 55 measured the insurance).
* Instruments — `none`, `200d` (the incumbent, re-evaluated every rebalance), `200d-M`
  (evaluated on month-ends and held constant), `band3` / `band5` (hysteresis: enter above
  `(1+b)·MA200`, exit below `(1-b)·MA200`, sticky in between).
* Costs applied analytically, `returns(c) = gross − turnover·c/1e4`. **Harness check 1**
  confirms this is bit-identical to a real `cost_bps=10` engine run (max abs diff 0.00e+00).
  **Harness check 2/3** reproduce idea 2's KEEP row (12.7%/1.093/-18.3%, halves 1.088/1.103)
  and idea 55's candidate row (13.7%/1.123/-18.5%) to the decimal.

Benchmarks on the common sample (2009-01-13 → 2026-09-03): SPY 15.3%/0.890/-33.7%
(halves 0.957/0.837, OOS Sharpe 0.884); RULES v1 live 6.5%/0.666/-13.8%.
4b bars: H1 > 0.957, H2 > 0.837, OOS > 0.884, MaxDD ≥ -20.2%, CAGR ≥ 10.7%.

## (a) Does the insurance pay? No — not at any cost, on either book.

Every arm minus the uninsured (`gate=none`) arm, same book, same days, `universe.json`:

| book | gate | bps | ΔCAGR | ΔSharpe | ΔMaxDD | Δturnover | pp CAGR per pp DD |
|---|---|---|---|---|---|---|---|
| top20 | 200d | 5 | -1.06 | **-0.027** | +0.25 | +0.1x | 4.23 |
| top20 | 200d | 10 | -1.06 | **-0.030** | +0.24 | +0.1x | 4.45 |
| top20 | 200d | 25 | -1.06 | **-0.037** | +0.20 | +0.1x | 5.27 |
| top20 | 200d | 50 | -1.06 | **-0.049** | +0.23 | +0.1x | 4.71 |
| ew-all | 200d | 5 | -1.46 | **-0.044** | +2.51 | +6.4x | 0.58 |
| ew-all | 200d | 10 | -1.81 | **-0.077** | +2.51 | +6.4x | 0.72 |
| ew-all | 200d | 25 | -2.85 | **-0.176** | +2.42 | +6.4x | 1.18 |
| ew-all | 200d | 50 | -4.55 | **-0.341** | +0.30 | +6.4x | 15.15 |

The incumbent gate has a **negative Sharpe delta at every cost on both books**, and the
trade degrades monotonically with cost. On the ranked `top20` book there is barely any
insurance to buy in the first place — 0.24pp of MaxDD for 1.06pp of CAGR, a price of
4.45pp per pp — because the momentum ranking already excludes most below-MA names.
On the `ew-all` control, where the gate is the only thing doing work, the drawdown
purchase is real (+2.51pp) but at 50 bps the turnover has eaten the protection itself:
the gated arm's MaxDD advantage collapses to +0.30pp while it gives up 4.55pp of CAGR.
Paired daily differences vs `none` at 10 bps are negative on every arm of `universe.json`
(top20 200d -1.00%/yr t -1.61; ew-all 200d -1.71%/yr t -1.47) and on the broad list the
`ew-all` gate arms are significantly negative (200d -2.06%/yr **t -2.13**).

Break-even: the `ew-all` gate arms are behind on *gross* return and dearer to run, so
they are behind at every cost inside 0-200 bps. On `top20`, `200d` is behind at every
cost; the cheap instruments are behind on gross but cheaper, catching up only above
57-135 bps — far outside anything tradeable.

## (b) Is a cheaper instrument the same insurance? Yes — it is strictly better insurance.

Gate churn, `universe.json` (mean trend-state flips per ticker per year):
`200d` **7.55** · `200d-M` **1.69** · `band3` **1.77** · `band5` **1.23** — the cheap
instruments toggle **4-6x less often**. On the `ew-all` book that is 8.2x/yr turnover
for the incumbent vs 4.6x / 4.9x / 4.1x.

At 10 bps on `ew-all` (`universe.json`), against `none`:

| gate | ΔCAGR | ΔSharpe | ΔMaxDD | Δtop-5 DD | turnover |
|---|---|---|---|---|---|
| 200d | -1.81 | -0.077 | +2.51 | +0.98 | 8.2x |
| 200d-M | -0.84 | -0.018 | **+3.67** | +1.38 | 4.6x |
| band3 | -0.96 | **+0.009** | +3.25 | **+1.80** | 4.9x |
| band5 | -0.75 | -0.020 | +2.56 | +1.03 | 4.1x |

The cheap instruments buy **more** drawdown reduction for **less** forgone return at
**half** the turnover. `band3` is the only instrument anywhere in the grid with a
non-negative Sharpe delta at the protocol cost (+0.009 at 10 bps, +0.025 at 5 bps).
The mechanism is visible in the calendar year table: at `top20`, 2020 reads `none`
+13.8%, `200d` +15.4%, `200d-M` **+18.1%**, `band3` +16.4%; 2022 reads `none` -8.9%,
`200d` -9.0%, `200d-M` **-6.8%**, `band3` -7.1%. The continuously-re-evaluated gate
whipsaws out and back in at exactly the moments it is supposed to protect.

## The KEEP-candidate: `ew-all` + 3% band

At the protocol cost of 10 bps, **three arms clear all five 4b tests on BOTH large-cap
universes** — and all three are the equal-weight book with a *cheap* gate. The incumbent
`200d` is not among them (it misses `universe.json`'s CAGR floor), nor is any `top20` arm.

| arm | universe.json | broad |
|---|---|---|
| ew-all 200d-M | 11.4%/1.109/-14.7%, halves 1.096/1.123, OOS 12.6%/1.197/-14.7%, 4.6x | 11.3%/1.051/-17.2%, halves 1.153/0.955, OOS 11.3%/1.054/-17.2%, 4.6x |
| **ew-all band3** | **11.3%/1.136/-15.1%, halves 1.113/1.160, OOS 12.6%/1.234/-15.1%, 4.9x** | **11.1%/1.064/-16.8%, halves 1.163/0.971, OOS 11.2%/1.074/-16.8%, 5.2x** |
| ew-all band5 | 11.5%/1.108/-15.8%, halves 1.092/1.125, OOS 12.8%/1.199/-15.8%, 4.1x | 11.1%/1.043/-17.5%, halves 1.131/0.960, OOS 11.3%/1.063/-17.5%, 4.2x |

This is the test **idea 2's n=20 and idea 55's K=none candidate both fail** — the standing
fragility of every KEEP-candidate this project has produced. That three neighbouring arms
pass together, rather than one lucky point, is the reassuring part. `band3` also fixes
idea 28's exact failure: equal-weight-all-eligible missed 4b's CAGR floor by 0.23pp, and
the band raises CAGR from 10.4% to 11.3%, clearing the 10.7% bar with drawdown to spare.

**Rule-8 walk-forward** (instrument chosen on 2009-2016 across all 10 arms, evaluated
untouched 2017-2026, both rules fixed before any OOS number was read):

* `universe.json`: both rules pick **top20/none**, OOS 14.9%/1.164/-18.5%, clears the OOS
  4b bars. **It does not pick the band.**
* `universe_broad.json`: plain-Sharpe picks ew-all/none (OOS 12.5%/1.104/-20.8%, misses the
  OOS DD bar); the **4b-aware rule picks ew-all/band3**, OOS 11.2%/1.074/-16.8%, clears.

So the band arm is the pre-registered pick on one list and not the other. That is the
honest limit on the candidate: it wins on cross-universe 4b, not on primary-universe
selection.

## Caveats

1. **Cost ceiling.** At 25 bps nothing passes 4b on both universes (5/10 and 0/10);
   at 50 bps, 1/10 and 0/10. The candidate is a 10 bps rule, not a 25 bps rule.
2. **Selection breadth.** 40 points per universe were searched. The cross-universe filter
   and the walk-forward are the guards; the walk-forward disagrees on the primary list.
3. **Survivorship.** Both lists are current constituents, so absolute CAGR/Sharpe are
   optimistic and the `ew-all` book holds the whole list. The gate-vs-gate comparisons that
   answer (a) and (b) are far less exposed — every arm draws from the same names on the
   same days.
4. **H2 on the broad list is thin** for `band3` (0.971 vs SPY's 0.837) but it is the
   binding half everywhere, and it clears.

## What this means for RULES

The live book re-evaluates the 200d filter *daily* (v1's hard-exit clause). This run says
that is the most expensive version of the instrument and buys the least protection. If the
Sunday review keeps a trend gate at all, it should be the monthly or band version. Memo
with exact wording: `2026-09-04_trend-gate-as-drawdown-insurance_B.memo.md`.

Ideas 58-60 queued.
