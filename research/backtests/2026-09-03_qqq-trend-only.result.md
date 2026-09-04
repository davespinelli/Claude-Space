# Idea 27 — qqq-trend-only (the simplest growth-plus-trend floor the book must beat)

Script: `research/backtests/2026-09-03_qqq-trend-only.py` · Costs 10 bps per unit turnover · price panel = `baseline.load_universe()` (56 tickers, 2008-01-02 → 2026-09-02) · eval sample 2009-01-13 → 2026-09-02 (17.6y) after the 260-day warm-up `compare()` skips. Long-only, no leverage. Only QQQ, SPY and SHY ever carry weight; the other 53 tickers are held at 0.

| Variant | Risk-on leg | Risk-on condition | Risk-off leg | Check | Tuned params |
|---|---|---|---|---|---|
| A | 100% QQQ | QQQ > 200d MA | 100% SHY | weekly (`freq="W"`) | 1 |
| B | 100% QQQ | QQQ > 200d MA **and** QQQ 12-1 momentum > 0 | 100% SHY | weekly | 2 |
| C | 50% QQQ / 50% SPY | QQQ > 200d MA | 100% SHY | weekly | 2 |
| D | 100% QQQ | QQQ > 200d MA | 100% SHY | **monthly** (`freq="M"`) | 1 |

12-1 momentum = `QQQ.shift(21) / QQQ.shift(252) - 1`. The 200d and 12-1 lookbacks are the textbook values (Faber 2007, Jegadeesh-Titman), not searched on this data. No look-ahead: signals at date `t` use closes through `t`, and `engine.backtest` shifts weights one day before applying them.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | qqq-trend-only A (QQQ/SHY, 200d, weekly) | 14.4% | 0.91 | -27.5% | 0.80 / 1.01 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_qqq-trend-only.py |
| 2026-09-03 | qqq-trend-only B (A + 12-1 mom>0, weekly) | 12.5% | 0.83 | -28.3% | 0.64 / 0.99 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_qqq-trend-only.py |
| 2026-09-03 | qqq-trend-only C (50/50 QQQ+SPY core, weekly) | 12.3% | 0.88 | -26.5% | 0.75 / 1.00 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_qqq-trend-only.py |
| 2026-09-03 | qqq-trend-only D (QQQ/SHY, 200d, monthly) | 14.7% | 0.88 | -28.6% | 0.85 / 0.91 | 0.66 (0.65/0.68) | KILL | research/backtests/2026-09-03_qqq-trend-only.py |

Every KILL here is driven by the MaxDD clause of rule 4, not by Sharpe. All four beat the live baseline's Sharpe by a wide margin; all four draw down roughly twice as deep.

## Full sample + halves (`compare()` equal-row halves; the break falls in late 2017)

| Book | CAGR | Vol | Sharpe | MaxDD | H1 Sharpe | H2 Sharpe | H1 MaxDD | H2 MaxDD | $1 → |
|---|---|---|---|---|---|---|---|---|---|
| A (QQQ/SHY, 200d, weekly) | 14.4% | 16.1% | 0.913 | -27.5% | 0.801 | 1.013 | -27.5% | -25.2% | 10.63 |
| B (A + 12-1 mom>0, weekly) | 12.5% | 15.5% | 0.835 | -28.3% | 0.644 | 0.994 | -28.3% | -25.2% | 7.90 |
| C (50/50 QQQ+SPY, weekly) | 12.3% | 14.3% | 0.881 | -26.5% | 0.749 | 0.998 | -26.5% | -25.9% | 7.71 |
| D (QQQ/SHY, 200d, monthly) | 14.7% | 17.3% | 0.880 | -28.6% | 0.854 | 0.910 | -24.8% | -28.6% | 11.22 |
| **RULES v1 baseline (live)** | 6.4% | 10.2% | 0.663 | -13.8% | 0.646 | 0.682 | -13.1% | -13.8% | 3.00 |
| **SPY buy-and-hold** | 15.2% | 17.7% | 0.887 | -33.7% | 0.957 | 0.831 | -22.1% | -33.7% | 12.06 |
| **QQQ buy-and-hold** | 20.8% | 20.9% | **1.008** | -35.1% | 1.194 | 0.885 | -18.3% | -35.1% | **27.86** |

Sortino / Calmar: A 1.112 / 0.52 · B 0.989 / 0.44 · C 1.053 / 0.46 · D 1.056 / 0.52 · baseline 0.843 / 0.47 · SPY 1.103 / 0.45 · QQQ 1.314 / 0.59.

## Calendar halves — 2009-2016 (rule-8 selection window) vs 2017-2026 (untouched OOS)

| Book | Period | CAGR | Vol | Sharpe | MaxDD |
|---|---|---|---|---|---|
| A | 2009-2016 | 8.5% | 14.4% | 0.637 | -27.5% |
| A | 2017-2026 | 19.5% | 17.5% | **1.108** | -25.2% |
| B | 2009-2016 | 5.4% | 13.5% | 0.455 | -28.3% |
| B | 2017-2026 | 18.7% | 17.0% | 1.094 | -25.2% |
| C | 2009-2016 | 7.5% | 13.3% | 0.606 | -26.5% |
| C | 2017-2026 | 16.5% | 15.1% | 1.085 | -25.9% |
| D | 2009-2016 | 10.5% | 15.8% | **0.710** | -24.8% |
| D | 2017-2026 | 18.4% | 18.5% | 1.004 | -28.6% |
| RULES v1 baseline | 2009-2016 | 5.0% | 9.5% | 0.558 | -13.1% |
| RULES v1 baseline | 2017-2026 | 7.7% | 10.7% | 0.743 | -13.8% |
| SPY buy-and-hold | 2009-2016 | 15.0% | 17.2% | 0.899 | -22.1% |
| SPY buy-and-hold | 2017-2026 | 15.4% | 18.2% | 0.879 | -33.7% |
| QQQ buy-and-hold | 2009-2016 | 20.3% | 18.4% | 1.098 | -18.3% |
| QQQ buy-and-hold | 2017-2026 | 21.2% | 22.8% | 0.957 | -35.1% |

## Calendar-year returns, requested years

| Year | A | B | C | D | RULES v1 | SPY B&H | QQQ B&H |
|---|---|---|---|---|---|---|---|
| 2018 | +8.5% | +8.5% | +5.1% | +10.7% | +8.0% | -4.6% | -0.1% |
| 2020 | +42.0% | +35.5% | +27.4% | +28.9% | +8.4% | +18.3% | +48.4% |
| 2022 | -14.8% | -14.8% | -13.0% | -11.9% | **+2.6%** | -18.2% | -32.6% |

Full calendar-year table (2026 is a partial year, through 2026-09-02):

| Year | A | B | C | D | RULES v1 | SPY B&H | QQQ B&H |
|---|---|---|---|---|---|---|---|
| 2009 | +32.0% | +12.8% | +29.8% | +33.7% | +9.1% | +31.1% | +55.8% |
| 2010 | +6.9% | +6.9% | +5.2% | -1.5% | +4.3% | +15.1% | +20.1% |
| 2011 | **-20.4%** | -19.9% | -19.7% | -2.3% | +1.9% | +1.9% | +3.5% |
| 2012 | +5.1% | -1.7% | +5.7% | +8.6% | +6.8% | +16.0% | +18.1% |
| 2013 | +33.3% | +35.0% | +30.9% | +36.6% | +11.5% | +32.3% | +36.6% |
| 2014 | +19.2% | +19.2% | +16.3% | +19.2% | +6.6% | +13.5% | +19.2% |
| 2015 | +4.7% | +4.7% | +1.7% | +0.2% | +3.1% | +1.2% | +9.4% |
| 2016 | -2.8% | -5.1% | -1.2% | -3.1% | -3.1% | +12.0% | +7.1% |
| 2017 | +32.7% | +32.7% | +27.1% | +32.7% | +14.8% | +21.7% | +32.7% |
| 2018 | +8.5% | +8.5% | +5.1% | +10.7% | +8.0% | -4.6% | -0.1% |
| 2019 | +19.3% | +20.7% | +16.9% | +23.9% | +6.7% | +31.2% | +39.0% |
| 2020 | +42.0% | +35.5% | +27.4% | +28.9% | +8.4% | +18.3% | +48.4% |
| 2021 | +27.4% | +27.4% | +28.1% | +27.4% | +20.2% | +28.7% | +27.4% |
| 2022 | -14.8% | -14.8% | -13.0% | -11.9% | +2.6% | -18.2% | -32.6% |
| 2023 | +33.4% | +29.1% | +26.0% | +40.8% | +1.3% | +26.2% | +54.9% |
| 2024 | +25.6% | +25.6% | +25.3% | +25.6% | +9.7% | +24.9% | +25.6% |
| 2025 | +14.0% | +14.0% | +14.1% | +9.3% | +7.7% | +17.7% | +20.8% |
| 2026* | +10.1% | +10.1% | +9.0% | -0.2% | -3.6% | +12.8% | +15.7% |

Each variant beats QQQ buy-and-hold in only 2 of 18 calendar years (3 for C).

## Round-trips per year (a round trip = one exit from the risk-on leg plus the re-entry)

| Year | A | B | C | D |
|---|---|---|---|---|
| 2009 | 0.5 | 0.5 | 0.5 | 0.5 |
| 2010 | 3.0 | 3.0 | 3.0 | 2.0 |
| 2011 | 5.0 | 4.5 | 5.0 | 1.0 |
| 2012 | 3.0 | 4.5 | 3.0 | 0.0 |
| 2013 | 0.0 | 1.0 | 0.0 | 0.0 |
| 2014 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2015 | 1.0 | 1.0 | 1.0 | 1.0 |
| 2016 | 4.0 | 4.0 | 4.0 | 2.0 |
| 2017 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2018 | 1.5 | 1.5 | 1.5 | 0.0 |
| 2019 | 1.5 | 3.5 | 1.5 | 2.0 |
| 2020 | 1.0 | 2.0 | 1.0 | 1.0 |
| 2021 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2022 | 1.5 | 1.5 | 1.5 | 0.5 |
| 2023 | 0.5 | 0.5 | 0.5 | 0.5 |
| 2024 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2025 | 1.0 | 2.0 | 1.0 | 1.0 |
| 2026* | 1.0 | 1.0 | 1.0 | 1.0 |
| **avg/yr** | **1.39** | **1.73** | **1.39** | **0.71** |

Time in the risk-on leg: A 84.0%, B 77.8%, C 84.0%, D 84.0% of days. Annual turnover: A 5.34x, B 5.57x, C 5.50x, D 2.84x.

## PROTOCOL rule 8 walk-forward — select on 2009-2016 Sharpe, evaluate 2017-2026

In-sample 2009-2016 Sharpe: **D 0.710** > A 0.637 > C 0.606 > B 0.455. **Selected: D (monthly checks).**

| Book | OOS CAGR | OOS Vol | OOS Sharpe | OOS MaxDD | OOS Sortino | OOS total |
|---|---|---|---|---|---|---|
| **D — selected on IS Sharpe** | 18.4% | 18.5% | **1.004** | -28.6% | 1.175 | +408% |
| A | 19.5% | 17.5% | 1.108 | -25.2% | 1.328 | +457% |
| B | 18.7% | 17.0% | 1.094 | -25.2% | 1.284 | +421% |
| C | 16.5% | 15.1% | 1.085 | -25.9% | 1.266 | +335% |
| RULES v1 baseline | 7.7% | 10.7% | 0.743 | -13.8% | 0.928 | +104% |
| SPY buy-and-hold | 15.4% | 18.2% | 0.879 | -33.7% | 1.061 | +298% |
| QQQ buy-and-hold | 21.2% | 22.8% | 0.957 | -35.1% | 1.231 | +538% |

Selected variant OOS Sharpe **1.004 vs baseline 0.743**; OOS MaxDD **-28.6% vs -13.8%**. The selection rule picked the variant that turned out *worst* of the four out-of-sample — an honest demonstration that an 8-year Sharpe ranking among near-identical variants is noise.

## Attribution — "QQQ beat SPY" vs "the trend filter helped"

Full sample 2009-01-13 → 2026-09-02, decomposed in two steps: SPY B&H → QQQ B&H (asset choice) → A (add the trend filter).

| Step | ΔCAGR | ΔSharpe | ΔMaxDD |
|---|---|---|---|
| 1. Asset choice (QQQ B&H − SPY B&H) | **+5.61%** | **+0.121** | -1.4% (deeper) |
| 2. Trend filter (A − QQQ B&H) | **-6.43%** | **-0.095** | +7.6% (shallower) |

On the OOS leg alone (2017-2026): asset choice +5.80% CAGR / +0.078 Sharpe; trend filter -1.69% CAGR / **+0.151 Sharpe**.

Daily-return correlations: A↔QQQ 0.767, A↔SPY 0.673, A↔baseline 0.650; A↔B 0.959, A↔C 0.981, A↔D 0.891.

## PROTOCOL rule 4 — both KEEP paths evaluated explicitly

`research/PROTOCOL.md` rule 4 gained a second KEEP path (**4b, "capital-worthy"**) in commit `8d69180`, timestamped 2026-09-03 23:25 — *during this run*, after the protocol was read at task start. Both paths are therefore evaluated here so the verdict does not depend on which revision the reader has. SPY reference: Sharpe 0.887 (H1 0.957 / H2 0.831), OOS Sharpe 0.879, MaxDD -33.7%, CAGR 15.19%. 4b thresholds: MaxDD floor **-20.2%**, CAGR floor **10.6%**.

| Variant | 4a (beat the book) | 4b (capital-worthy) |
|---|---|---|
| A | FAIL — MaxDD -27.5% vs baseline -13.8% | FAIL — H1 Sharpe 0.801 < SPY 0.957; MaxDD -27.5% worse than -20.2% |
| B | FAIL — H1 0.644 < 0.646; MaxDD | FAIL — H1 0.644 < 0.957; MaxDD -28.3% |
| C | FAIL — MaxDD -26.5% | FAIL — H1 0.749 < 0.957; MaxDD -26.5% |
| D | FAIL — MaxDD -28.6% | FAIL — H1 0.854 < 0.957; MaxDD -28.6% |

All four pass 4b's CAGR floor (12.3%–14.7% vs 10.6%) and all four pass 4b's OOS-Sharpe-beats-SPY test (1.004–1.108 vs 0.879). They fail on the **2009-2016 half**, where SPY's Sharpe of 0.957 is higher than any variant's, and on **drawdown**. Verdict is KILL under both paths — the mid-run rule change does not rescue this idea.

## Memo

1. **What was tested:** four one-line "own QQQ while it trends, else own T-bills" rules at 10 bps, weekly or monthly checks, over 2009-01-13 → 2026-09-02, against the live RULES v1 book, SPY buy-and-hold, and — added as the honesty control — QQQ buy-and-hold. The purpose was to set a floor, not to find an edge.
2. **The floor is far above the live book.** All four variants beat RULES v1 on Sharpe (0.835–0.913 vs 0.663) and crush it on return (12.3%–14.7% CAGR vs 6.4%; $1 → $7.71–$11.22 vs $3.00). A, C and D beat the baseline's Sharpe in *both* `compare()` halves. This is the result that matters: the book currently does not beat a rule you could write on a napkin.
3. **Verdict is KILL for all four under both rule-4 paths.** Under 4a the binding clause is MaxDD, not Sharpe: -26.5% to -28.6% against the baseline's -13.8%, roughly double (B additionally misses the both-halves Sharpe test by a hair, H1 0.644 vs 0.646). Under the new 4b they clear the CAGR floor and beat SPY out-of-sample, but lose the 2009-2016 half to SPY (best variant H1 0.854 vs SPY 0.957) and still breach the -20.2% drawdown floor. Parameter counts are inside the limit (A and D use 1, B and C use 2) and every lookback is a textbook value, so overfitting is not the problem — risk profile is. These are not drop-in replacements for the live book; they are a benchmark it fails.
4. **Rule 8 walk-forward: PARK, not KEEP, and for an instructive reason.** Selecting on 2009-2016 Sharpe picks D (0.710). D's untouched 2017-2026 leg is Sharpe 1.004 vs the baseline's 0.743 and CAGR 18.4% vs 7.7% — it wins OOS on return and Sharpe, and loses on MaxDD (-28.6% vs -13.8%). But D was the *worst* of the four OOS (A 1.108, B 1.094, C 1.085), so the selection step subtracted value. With four near-identical variants an 8-year Sharpe ranking is noise; do not read the selection as skill.
5. **How much is "QQQ beat SPY" and how much is "the trend filter helped"? Overwhelmingly the former.** QQQ buy-and-hold alone returns 20.8% CAGR at Sharpe 1.008 — a higher Sharpe and 2.6x the terminal wealth of the best trend variant ($27.86 vs $11.22). Over the full sample the trend filter *subtracts* 6.43% of CAGR and 0.095 of Sharpe; it only buys you drawdown (-27.5% vs -35.1%). Picking the asset added +5.61% CAGR and +0.121 Sharpe. The variants beat QQQ in only 2 of 18 calendar years.
6. **The one place the filter earns its keep is out-of-sample risk-adjusted return**: on 2017-2026 it costs just 1.69% of CAGR and adds +0.151 Sharpe versus QQQ B&H, because it sidestepped part of 2022 (A -14.8% vs QQQ -32.6%; intra-2022 drawdown -16.6% vs -34.8%) and all of 2018's Q4 (A +8.5% vs SPY -4.6%). If the goal is "QQQ-like returns without QQQ-like drawdowns", the filter does something real. If the goal is terminal wealth, it does not.
7. **Whipsaw cost of checking weekly vs monthly is essentially zero on average and enormous in specific years.** D (monthly) earns *more* than A (weekly) — 14.7% vs 14.4% CAGR — on half the turnover (2.84x vs 5.34x) and half the round-trips (0.71 vs 1.39/yr), while A has the better Sharpe (0.913 vs 0.880). The averages hide 2011, where weekly checking cost 18 points (A -20.4%, D -2.3%, QQQ B&H +3.5%) by flipping five times through a choppy summer; and 2020, where weekly checking gained 13 points (A +42.0%, D +28.9%) by re-entering fast after the March crash. Frequency choice is a bet on the character of the next drawdown, not a free improvement.
8. **The extra complications both hurt.** Adding the 12-1 momentum gate (B) lowers Sharpe from 0.913 to 0.835, cuts CAGR by 1.9 points, deepens MaxDD slightly, and raises round-trips to 1.73/yr — it keeps you out of the 2009 recovery (+12.8% vs A's +32.0%). The 50/50 QQQ/SPY core (C) does what diluting toward SPY should: lower return (12.3%), lower vol (14.3%), shallower MaxDD (-26.5%), Sharpe roughly unchanged (0.881). Neither earns its second parameter.
9. **Caveats I will not paper over.** (a) 2009-2026 is one regime and QQQ's run in it is historically exceptional; selecting QQQ as the growth leg *in 2026, knowing what it did*, is itself the biggest look-ahead in this study, and none of these numbers survive if the next 17 years are the 2000-2009 kind. (b) The engine drifts weights between rebalances, so "100% QQQ" is exact only at rebalance dates. (c) 2026 is a partial year through 2026-09-02. (d) SHY is a real T-bill proxy but pays essentially nothing in 2009-2021 and ~4-5% in 2023-2025, so the risk-off leg's contribution is regime-dependent. (e) Per-ticker spreads are not modeled; 10 bps flat is generous for QQQ/SPY/SHY and so mildly flatters, not penalizes, the high-turnover variants.
10. **Process flag, then the recommendation.** Rule 4 was rewritten mid-run (commit `8d69180`, 23:25, adding path 4b whose stated rationale is that judging drawdown against the low-return book "kills every growth idea") — precisely the clause that was about to kill this idea. I did not adopt it silently: both paths are reported above and the verdict is KILL either way, so nothing here turns on it, but a protocol edit that lands while the result it would reclassify is being computed deserves a human look, and the same commit swept this script into git without my doing so (I ran no `git` write command). **Recommendation: KILL all four as candidate strategies, PARK variant A as the standing benchmark row.** Every future idea in this book should be reported against `qqq-trend-only A` — Sharpe 0.913, CAGR 14.4%, MaxDD -27.5% — and against QQQ buy-and-hold (Sharpe 1.008, CAGR 20.8%), not only against RULES v1 and SPY. The next useful test is not another variant of this rule; it is to ask what RULES v1 is buying with the 21 points of CAGR it gives up, and whether a risk-matched comparison (e.g. levering the baseline to 17% vol, or de-levering A to 10%) still leaves the book behind. No leaderboard file was modified in this run (per task instruction); the rows above are ready to append.
