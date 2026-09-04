# Idea 24 — core-plus-trend-sleeve (passive trend-gated equity core + macro-trend-ensemble B defensive sleeve)

Script: `research/backtests/2026-09-03_core-plus-trend-sleeve.py` · Costs 10 bps · `freq="W"` · price panel = `baseline.load_universe()` (56 tickers, 2008-01-02 → 2026-09-02); eval sample 2009-01-13 → 2026-09-02 after the 260-day warm-up `compare()` skips.

**Goal as stated:** SPY-like CAGR at roughly half the drawdown.

**Sleeve** = idea 18 variant B, copied faithfully (same `MACRO` list of 9 ETFs — SPY QQQ IWM EFA EEM TLT GLD DBC UUP — same `MOM_LAGS` 252/126/63, same `VOL_WINDOW` 60): vote v ∈ {0, ⅓, ⅔, 1} on the signs of {12-1 momentum, 6m return, 3m return}, times inverse-60d-vol risk-parity weights normalized to 1.0, remainder cash. Scaled by the sleeve fraction (0.40 or 0.50).

**Core** = the core ticker at its fraction when it is above **its own** 200d MA, else cash. (In variant B "same with QQQ as core" is read literally: the gate is QQQ > QQQ's 200d MA, not SPY's.) Core and sleeve weights are **added**, so SPY in variant A can carry 60% core + ~9% sleeve simultaneously; gross never exceeds 100%, long-only, no leverage.

**Tuned parameters (rule 4 count): 2** — the core/sleeve split, and the 200d MA window. The sleeve's lookbacks are canonical TSMOM values carried over unchanged from idea 18; 200d is the window RULES v1 already uses.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | core-plus-sleeve A (60% SPY>200d + 40% sleeve) | 7.8% | 0.86 | -14.7% | 0.80 / 0.92 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_core-plus-trend-sleeve.py |
| 2026-09-03 | core-plus-sleeve B (60% QQQ>200d + 40% sleeve) | 10.8% | 0.95 | -18.9% | 0.84 / 1.04 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_core-plus-trend-sleeve.py |
| 2026-09-03 | core-plus-sleeve C (50% SPY>200d + 50% sleeve) | 7.3% | 0.88 | -13.0% | 0.81 / 0.94 | 0.66 (0.65/0.68) | KEEP-candidate | research/backtests/2026-09-03_core-plus-trend-sleeve.py |
| 2026-09-03 | core-plus-sleeve D (60% SPY no filter + 40% sleeve) | 11.3% | 0.93 | -24.1% | 0.97 / 0.90 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_core-plus-trend-sleeve.py |

A, B and D are KILLs on the **MaxDD leg of rule 4 only** (-14.7% / -18.9% / -24.1% vs baseline -13.8%); all three beat the baseline's Sharpe in both halves. C is the only variant that clears every leg.

Reference rows from the same run: **RULES v1 baseline** CAGR 6.4%, Sharpe 0.663, MaxDD -13.8%, H1/H2 0.646/0.682 · **SPY** CAGR 15.2%, Sharpe 0.887, MaxDD -33.7%, H1/H2 0.957/0.831 · **sleeve B standalone at full size** CAGR 5.0%, Sharpe 0.865, MaxDD -10.1%, H1/H2 0.753/0.979. (H1/H2 are `compare()`'s equal-row halves — the break falls in late 2017, not at year-end 2016.)

## Full sample + halves (rule 4)

| Strategy | CAGR | Sharpe | MaxDD | H1 Sharpe | H2 Sharpe | H1 MaxDD | H2 MaxDD |
|---|---|---|---|---|---|---|---|
| A (60% SPY>200d + 40% sleeve) | 7.8% | 0.864 | -14.7% | 0.803 | 0.923 | -14.7% | -11.5% |
| B (60% QQQ>200d + 40% sleeve) | 10.8% | 0.950 | -18.9% | 0.845 | 1.044 | -18.1% | -18.9% |
| C (50% SPY>200d + 50% sleeve) | 7.3% | 0.876 | -13.0% | 0.807 | 0.944 | -13.0% | -11.2% |
| D (60% SPY no filter + 40% sleeve) | 11.3% | 0.933 | -24.1% | 0.975 | 0.900 | -13.9% | -24.1% |
| RULES v1 baseline | 6.4% | 0.663 | -13.8% | 0.646 | 0.682 | -13.1% | -13.8% |
| SPY | 15.2% | 0.887 | -33.7% | 0.957 | 0.831 | -22.1% | -33.7% |
| sleeve B standalone (100%) | 5.0% | 0.865 | -10.1% | 0.753 | 0.979 | -8.6% | -10.1% |

## Walk-forward (PROTOCOL rule 8) — select on 2009-2016, evaluate 2017-2026 untouched

In-sample (2009-2016) Sharpe: **A 0.680 · B 0.681 · C 0.681 · D 0.897**.
**Rule-8 pick = D** (60% SPY, *no* 200d filter, + 40% sleeve).

| Strategy | Period | CAGR | Vol | Sharpe | MaxDD |
|---|---|---|---|---|---|
| **D (rule-8 pick)** | 2009-2016 (IS) | 10.5% | 11.9% | 0.897 | -13.9% |
| **D (rule-8 pick)** | **2017-2026 (OOS)** | **11.9%** | 12.5% | **0.962** | **-24.1%** |
| A | 2009-2016 (IS) | 6.0% | 9.2% | 0.680 | -14.7% |
| A | 2017-2026 (OOS) | 9.2% | 9.1% | 1.018 | -11.5% |
| B | 2009-2016 (IS) | 6.8% | 10.5% | 0.681 | -18.1% |
| B | 2017-2026 (OOS) | 14.2% | 12.2% | 1.146 | -18.9% |
| C | 2009-2016 (IS) | 5.6% | 8.6% | 0.681 | -13.0% |
| C | 2017-2026 (OOS) | 8.8% | 8.4% | 1.041 | -11.2% |
| RULES v1 baseline | 2009-2016 (IS) | 5.0% | 9.5% | 0.558 | -13.1% |
| RULES v1 baseline | 2017-2026 (OOS) | 7.7% | 10.7% | 0.743 | -13.8% |
| SPY | 2009-2016 (IS) | 15.0% | 17.2% | 0.899 | -22.1% |
| SPY | 2017-2026 (OOS) | 15.4% | 18.2% | 0.879 | -33.7% |
| sleeve B standalone | 2009-2016 (IS) | 3.6% | 6.0% | 0.614 | -8.6% |
| sleeve B standalone | 2017-2026 (OOS) | 6.2% | 5.7% | 1.084 | -10.1% |

All four variants beat the baseline's OOS Sharpe (0.743). Only A and C also beat its OOS MaxDD (-13.8%).

## Stress years and gross exposure

| Variant | 2020 | 2022 | Avg gross (full) | IS | OOS | min / max gross | Avg core (SPY+QQQ) | Turnover | Core in cash |
|---|---|---|---|---|---|---|---|---|---|
| A | +10.70% | -8.96% | 76.1% | 74.3% | 77.6% | 8.7% / 100.0% | 56.5% | 3.7x/yr | 17.1% of days |
| B | +26.07% | -8.06% | 76.8% | 75.8% | 77.6% | 8.7% / 100.0% | 57.1% | 3.5x/yr | 16.0% of days |
| C | +9.76% | -7.90% | 74.4% | 72.3% | 76.2% | 10.9% / 100.0% | 49.9% | 3.8x/yr | 17.1% of days |
| D | +13.70% | -11.70% | 86.4% | 85.0% | 87.6% | 68.7% / 100.0% | 66.7% | 1.9x/yr | never |
| RULES v1 baseline | +8.44% | **+2.58%** | 74.9% | 75.0% | 74.9% | 45.0% / 75.0% | — | — | — |
| SPY | +18.33% | -18.18% | 100% | — | — | — | — | — | — |
| sleeve B standalone | +4.85% | -2.50% | 65.9% | 62.4% | 68.9% | 21.9% / 100.0% | — | 4.6x/yr | — |

Growth of $1 over the eval sample: A $3.73 · B $6.09 · C $3.47 · D $6.54 · baseline $3.00 · SPY $12.06 · sleeve $2.37.
Daily-return correlations: A–C **0.998**, A–B 0.870, A–D 0.771, D–SPY **0.989**, C–baseline 0.751, C–sleeve 0.894.

## Memo

1. **Tested:** a beta core plus the idea-18 variant-B macro TSMOM sleeve, weekly, 10 bps, long-only, gross ≤ 100%, on the standard `load_universe()` panel — A 60% SPY-above-200d + 0.4×sleeve, B the same with QQQ as core (gated on QQQ's own 200d), C 50/50, D 60% SPY ungated + 0.4×sleeve. Two tuned parameters (core split, 200d window); the sleeve was reused unchanged, not re-fit.
2. **The stated goal was not met by any variant.** "SPY-like CAGR at roughly half the drawdown" would be ~15% CAGR at ~-17%. The best CAGR here is D at 11.3% with -24.1% DD (72% of SPY's), and the best drawdown is C at -13.0% (39% of SPY's) with a CAGR of 7.3% — 48% of SPY's. Blending a defensive sleeve in at 40-50% moves return and risk together, roughly proportionally; it does not buy a free drawdown reduction. Nearest-to-goal is **B**: 10.8% CAGR (71% of SPY) at -18.9% DD (56% of SPY).
3. **Rule 4 verdicts:** all four beat the baseline's Sharpe in both halves by wide margins (0.80–0.98 / 0.90–1.04 vs 0.65/0.68), so the deciding leg is MaxDD ≥ baseline's -13.8%. A (-14.7%), B (-18.9%) and D (-24.1%) fail it → **KILL**. C (-13.0%) passes → **KEEP-candidate**.
4. **Rule 8 is the damning result.** Selecting on 2009-2016 Sharpe alone picks **D — the variant with no trend filter at all** (IS Sharpe 0.897 vs a three-way tie of 0.680/0.681/0.681 for A/B/C). D's OOS is respectable on Sharpe (0.962 vs baseline 0.743) but its OOS MaxDD is -24.1% against the baseline's -13.8%, so the honest walk-forward answer is: *the variant an out-of-sample-clean selection procedure would have chosen fails rule 4 on drawdown.* C wins OOS on both legs (Sharpe 1.041, MaxDD -11.2%) — but nothing in the IS data would have told you to pick C over A or B, since all three tie to three decimal places.
5. **What the 200d filter actually adds (A vs D, the clean isolation):** it costs 3.5pp of CAGR (7.8% vs 11.3%), removes 9.4pp of drawdown (-14.7% vs -24.1%), cuts average gross from 86.4% to 76.1%, and *lowers* Sharpe (0.864 vs 0.933) while roughly doubling turnover (3.7x vs 1.9x). It is a drawdown-purchasing device paid for in return, not a risk-adjusted-return improvement.
6. **The filter's year-by-year record is worse than its headline.** It helped in exactly one year of the sample — 2022 (A -8.96% vs D -11.70%). It *hurt* in 2011 (-7.55% vs +2.20%), 2015 (-7.00% vs -0.22%), 2019 (+10.97% vs +21.57%) and, tellingly, **2020** (+10.70% vs +13.70%): the COVID crash was too fast for a 200d gate to exit ahead of, and the recovery too fast to re-enter into. A drawdown filter that loses money in four whipsaw years to help in one is one bear market's worth of evidence.
7. **C's rule-4 pass is fragile to the point of being noise.** C and A are 0.998 correlated — C is literally A with the dial moved 10pp. The entire difference between "KEEP-candidate C" and "KILL A" is a 0.8pp MaxDD margin (-13.0% vs -13.8% baseline) produced by moving one of the two tuned parameters. Any honest reading treats that as a knob found on the sample, not an edge.
8. **The baseline still owns the one real crisis.** In 2022 RULES v1 made **+2.58%** while every blend lost 7.9%–11.7%. The blends beat the baseline on Sharpe everywhere and on 2020, but the year the book most needed protection, the live rules protected better than the sleeve blend did. That should temper any claim that this is a defensive improvement.
9. **Caveats:** two genuine stress regimes (2020, 2022) in 17.6 years is thin evidence for a construction whose entire pitch is drawdown; the sleeve inherits idea 18's inverse-vol tilt into UUP (~13% of the sleeve's NAV is effectively cash, mechanically flattering Sharpe and depressing CAGR); the four variants are not four ideas (A–C correlate 0.87–1.00, D correlates 0.989 with SPY); per-ticker spreads on DBC/UUP are wider than the flat 10 bps modeled; no `write_report`, no leaderboard file, and no other file was modified in this run — the rows above are ready to append.
10. **Verdict: KILL A, B and D on rule 4 (MaxDD). C is a protocol KEEP-candidate — it clears rule 4 and survives rule 8's OOS leg — but I recommend PARK, not KEEP**, because (a) rule 8's own selection step picks D, not C, so C is not identifiable ex ante; (b) C's margin over the baseline's drawdown is 0.8pp and is entirely a function of the split knob; and (c) the idea fails its stated objective — 7.3% CAGR is not SPY-like. Next test that would change my mind: fix the split at 50/50 a priori and re-run across core sleeves (SPY/QQQ/equal-weight) and MA windows (100/150/200/250) to see whether the drawdown edge is a plateau or a point.

### Exact RULES wording (drafted only because C technically qualifies under rule 4 — **not** recommended for adoption; PROTOCOL rule 6 requires a Sunday review, a CHANGELOG entry and a version bump, none of which this run performs)

> **9. Core-plus-sleeve overlay (v2 candidate).** In addition to rules 1-8, hold a two-part overlay book rebalanced on the same weekly schedule as rule 5:
> **(a) Core — 50% of NAV in SPY** whenever SPY's last close is above its 200-day simple moving average; otherwise hold that 50% in cash. Evaluate the gate at the weekly rebalance only.
> **(b) Sleeve — 50% of NAV allocated across SPY, QQQ, IWM, EFA, EEM, TLT, GLD, DBC, UUP.** For each of the nine, compute vote v = (number of {12-1 momentum with 21-day skip, 6-month return, 3-month return} that are positive) / 3, and risk-parity weight rp = (1/60-day return volatility) normalized so the nine rp values sum to 1. Position = 0.50 × v × rp. The unallocated remainder is cash.
> Core and sleeve weights for the same ticker are additive. Long-only, no leverage; total gross must not exceed 100% of NAV. Reason string: "RULES v2: core|sleeve <ticker> v=<v> rp=<rp>".

_Research, not investment advice. Past performance is not indicative of future results._
