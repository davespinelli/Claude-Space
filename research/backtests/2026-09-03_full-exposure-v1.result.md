# Idea 20 — full-exposure-v1 (does the 75% gross cap explain RULES v1's CAGR gap to SPY?)

Script: `research/backtests/2026-09-03_full-exposure-v1.py` · Costs 10 bps · `freq="W"` · `px = baseline.load_universe()` (56 tickers) · sample 2009-01-13 → 2026-09-02 (260-day warm-up skipped by `compare()`).

Variants (all identical to RULES v1 except where stated):

- **A** — v1 selection, 5 names @ **20%** each (100% gross). Only change vs baseline: position size.
- **B** — A + market filter: SPY below its 200d MA → every weight halved (50% gross).
- **C** — A + market filter: SPY below its 200d MA → fully to cash (0% gross).
- **D** — 5 names @ 20% **without the per-name 200d filter** (pure momentum): the 200d MA is removed both as the eligibility gate and as the score's `0.5+0.5*above` tilt; the `vol20 < 0.60` gate is kept, so the only difference vs A is the 200d MA.
- **D2** *(diagnostic, not one of the four)* — gate removed but the score tilt kept, to separate gate from tilt.

SPY was below its 200d MA on 17.1% of days in the eval sample.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | A full-exposure 100% gross | 8.4% | 0.66 | -18.2% | 0.65 / 0.68 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | B full-exposure + SPY-200d half | 7.9% | 0.65 | -17.6% | 0.65 / 0.66 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | C full-exposure + SPY-200d cash | 7.3% | 0.62 | -17.6% | 0.64 / 0.61 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | D full-exposure no per-name 200d | 8.2% | 0.66 | -20.4% | 0.69 / 0.64 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |
| 2026-09-03 | D2 no 200d gate, tilt kept (diagnostic) | 8.5% | 0.67 | -18.2% | 0.65 / 0.68 | 0.66 (0.65/0.68) | KILL | 2026-09-03_full-exposure-v1.py |

Reference rows printed by `compare()` in the same run: **RULES v1 baseline** CAGR 6.4%, Sharpe 0.663, MaxDD -13.8%, H1/H2 0.646/0.682; **SPY** CAGR 15.2%, Sharpe 0.887, MaxDD -33.7%, H1/H2 0.957/0.831.

Supporting stats from the same run:

| | avg gross | ann. vol | corr to baseline | turnover |
|---|---|---|---|---|
| RULES v1 baseline | 74.9% | 10.20% | 1.000 | — |
| A | 99.9% | 13.60% | **1.000** | 31.5x/yr |
| B | 91.4% | 12.96% | 0.985 | 30.4x/yr |
| C | 82.9% | 12.75% | 0.937 | 29.3x/yr |
| D | 100.0% | 13.29% | 0.981 | 31.0x/yr |
| SPY | 100% | 17.72% | 0.525 | — |

## Walk-forward (PROTOCOL rule 8)

No variant has a tunable parameter beyond the choice of variant itself (n=5 and w=20% are fixed by the brief, the 200d lookback is v1's own, and B's halving factor is 1/2 by construction). So the only in-sample decision is **which variant**, made on 2009–2016 Sharpe alone; 2017–2026 is untouched.

| | IS CAGR | IS Sharpe | IS MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| A full-exposure 100% gross | 6.5% | 0.558 | -17.3% | 10.0% | 0.740 | -18.2% |
| B + SPY-200d half | 6.3% | 0.559 | -16.8% | 9.3% | 0.723 | -17.6% |
| C + SPY-200d cash | 6.0% | 0.545 | -16.4% | 8.5% | 0.677 | -17.6% |
| **D no per-name 200d** | **6.9%** | **0.601** | -17.2% | 9.3% | 0.707 | -20.4% |
| D2 (diagnostic) | 6.5% | 0.558 | -17.3% | 10.1% | 0.745 | -18.2% |
| RULES v1 baseline | 5.0% | 0.558 | -13.1% | 7.7% | 0.743 | -13.8% |
| SPY | 15.0% | 0.899 | -22.1% | 15.4% | 0.879 | -33.7% |

**Variant selected on 2009–2016 Sharpe: D (0.601, the only variant that beat the baseline's 0.558 in-sample).**
Its untouched 2017–2026 result: **CAGR 9.3%, Sharpe 0.707, MaxDD -20.4%** vs **baseline OOS CAGR 7.7%, Sharpe 0.743, MaxDD -13.8%** and **SPY OOS CAGR 15.4%, Sharpe 0.879, MaxDD -33.7%**. D's entire in-sample Sharpe edge (+0.043 over baseline) reverses out of sample (-0.036), while its drawdown stays 6.6pp worse — the IS pick did not transfer.

## Memo

1. **The 75% cap explains only about a quarter of the gap.** Baseline→SPY CAGR gap is 8.7pp (6.4% vs 15.2%). Going 15%→20% per name (variant A) adds 2.0pp of CAGR, i.e. **23% of the gap**; the other 6.7pp comes from the selection itself, not from the cash sleeve.
2. **Exposure is a pure lever, not an edge.** A's daily returns correlate **1.000** with the baseline and its vol is 13.60% vs 10.20% — exactly the 20/15 = 1.333 ratio. Sharpe is unchanged (0.662 vs 0.663) and MaxDD scales with it (-18.2% vs -13.8%). Answering the question as asked: the cap costs ~2pp of CAGR and buys ~4.4pp of drawdown. That is a risk-appetite dial, and dialling it does not close the gap to SPY.
3. **The residual 6.7pp is beta and selection, not sizing.** The book correlates only 0.525 with SPY and runs 13.6% vol against SPY's 17.7% at full gross; a vol-scaled momentum book of 5 names out of 56 simply did not keep up with a US large-cap index in 2009–2026. Even at 100% gross the book beat SPY in only 4 of 18 calendar years (2011, 2015, 2018, 2022) — it wins in the drawdown years and loses the melt-ups.
4. **The market filter (component 2) is a net negative.** B and C both cut CAGR (7.9% / 7.3% vs A's 8.4%) *and* Sharpe (0.652 / 0.620 vs 0.662) for only 0.6pp of MaxDD relief (-17.6% vs -18.2%). C is worse in both halves (0.639/0.605). Because v1 already gates every name on its own 200d MA, the index gate is largely redundant and mostly adds whipsaw: 2022 was A +3.1% but C **-5.9%**, and 2023 A +1.5% vs C -3.5%. It earned its keep only in 2016 (+3.6% vs -4.3%) and 2020 (+12.3% vs +10.6%).
5. **The per-name 200d filter (component 3) earns its keep, cheaply.** Removing it (D) costs 0.2pp of CAGR and 2.2pp of MaxDD (-20.4% vs -18.2%) at the same Sharpe. Its value is concentrated: 2022 A +3.1% vs D **-5.1%**, an 8.2pp swing in the one year the momentum names broke down. D2 (hard gate removed, score tilt kept) is statistically indistinguishable from A (CAGR 8.5%, Sharpe 0.667, MaxDD -18.2%, corr 0.999), so it is the **soft tilt inside the score** that does the work — the hard eligibility gate is nearly redundant on top of it.
6. **Ranking of components by influence on the gap to SPY:** exposure (2.0pp, Sharpe-neutral) ≫ per-name filter (−0.2pp CAGR, +2.2pp DD protection) > market filter (−0.5 to −1.1pp CAGR *and* Sharpe). None of the three is the missing edge.
7. **Verdict per rule 4: KILL for all four variants (A, B, C, D) and for D2.** KEEP requires Sharpe above baseline in **both** halves and MaxDD no worse. A ties H1 (0.646/0.646) and loses H2 (0.680 vs 0.682); B loses H2; C loses both; D loses H2 (0.644 vs 0.682); and every variant's MaxDD is 3.8–6.6pp worse than the baseline's -13.8%. No variant clears either condition.
8. **Verdict per rule 8: PARK-at-best, and in fact KILL.** D was the only variant with an in-sample Sharpe edge, and it is the textbook failure mode — the edge was in-sample only (IS 0.601 vs baseline 0.558; OOS 0.707 vs 0.743) with a materially deeper OOS drawdown. Rule 8 says a candidate that only wins in-sample is not a KEEP; here it does not even survive as an interesting PARK, because the mechanism (dropping a filter that pays off in exactly one regime) is understood and adverse.
9. **RULES wording: no change recommended.** No variant qualifies, so RULES v1 rule 4 stands as written. For the record, had A qualified, the change would have been — **rule 4:** "**Sizing:** 20% of current NAV per position (max 5 positions → 100% invested, no cash floor). Round shares down to whole units."; and **rule 5** would have to move with it: "…do not top-up/trim existing positions unless weight > 29% or < 11% of NAV" (the 22%/8% bands scaled by 20/15). This is a mandate/risk-appetite change, not an alpha change, and per rule 6 it would need a Sunday review entry and a version bump — it should not be made on this evidence, since it buys CAGR only by accepting proportionally more drawdown at identical Sharpe.
10. **Caveats.** `load_universe()` downloads live prices, so the final bar can move between runs — a re-run minutes later shifted baseline CAGR 6.5%↔6.4% and Sharpe 0.665↔0.663; conclusions are far outside that noise. Universe is the current 56-ticker `universe.json` (survivorship bias in the single names). Turnover rises with gross (A 31.5x/yr vs the baseline's 75%-gross book) and those costs are included at 10 bps. B's halving factor and C's full-cash rule are the only two points tested of a continuum of de-risking factors; a milder filter was not searched, deliberately — searching it would be the tuning rule 7 forbids. The engine models next-day execution and no slippage beyond the 10 bps.
