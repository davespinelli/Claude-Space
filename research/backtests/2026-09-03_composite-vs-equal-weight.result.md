# Idea 25 — composite-vs-equal-weight (does the v1 score add anything over its own eligibility filter?)

Script: `research/backtests/2026-09-03_composite-vs-equal-weight.py` · Costs 10 bps · `freq="W"` · `px = baseline.load_universe()` (56 tickers) · sample 2009-01-13 → 2026-09-02 (260-day warm-up skipped by `compare()`).

RULES v1 does two separable things: **(1)** filter to names above their 200d MA with `vol20 < 0.60`, and **(2)** rank the survivors by the composite score and buy the top 5 at 15%. Step (1) is a standard trend/vol filter. Step (2) is the part that claims cross-sectional skill. This tests step (2).

Variants (all weekly, 10 bps, same eligibility filter):

- **A** — equal-weight **all** eligible names, 75% gross. Score never used.
- **B** — same as A at 100% gross (removes the cash-drag confound).
- **C** — v1 top-5 by score at 75%. This **is** the baseline, run as a variant so it sits in the same table; its numbers match the baseline row exactly, as they must.
- **D** — **bottom-5** by score among eligible, 75% gross. Falsification test: if the score has information, D must be clearly worse than C.
- **E** — top-5 by a single simple signal, **12-1 momentum only**, among the same eligible names, 75% gross.
- **C2** *(diagnostic, not one of the five)* — top-5 by the composite **without** the `/sqrt(vol20)` division, 75% gross. Isolates the vol-scaling term.

Eligible names per day: mean 37.5, median 41, min 3, max 55; never zero. Nothing is tuned inside any variant — n=5, w=15%, the 200d / `vol20<0.60` gates and the 21/63/126/252-day lookbacks are all v1's own, and E's 12-1 momentum is a component already inside the composite.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | A equal-weight all eligible 75% gross | 10.4% | 1.05 | -15.9% | 1.07 / 1.03 | 0.66 (0.65/0.68) | KILL 4a / PARK 4b | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | B equal-weight all eligible 100% gross | 13.9% | 1.05 | -20.9% | 1.07 / 1.03 | 0.66 (0.65/0.68) | KILL 4a / PARK 4b | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | C v1 top-5 by score 75% (= baseline) | 6.4% | 0.66 | -13.8% | 0.65 / 0.68 | 0.66 (0.65/0.68) | KILL (is the baseline) | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | D BOTTOM-5 by score 75% | 7.4% | 0.59 | -23.9% | 0.51 / 0.65 | 0.66 (0.65/0.68) | KILL | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | E top-5 by 12-1 momentum only 75% | 19.9% | 1.06 | -24.1% | 1.05 / 1.08 | 0.66 (0.65/0.68) | KILL 4a / PARK 4b | 2026-09-03_composite-vs-equal-weight.py |
| 2026-09-03 | C2 top-5 by composite, no vol-scaling (diagnostic) | 16.5% | 0.95 | -21.6% | 0.90 / 1.00 | 0.66 (0.65/0.68) | KILL | 2026-09-03_composite-vs-equal-weight.py |

`compare()` prints KILL for all six because it only implements rule 4a. The rule 4b assessment is below; the Verdict column above reflects both paths. Reference rows printed by `compare()` in the same run: **RULES v1 baseline** CAGR 6.4%, Sharpe 0.663, MaxDD -13.8%, H1/H2 0.646/0.682; **SPY** CAGR 15.2%, Sharpe 0.887, MaxDD -33.7%, H1/H2 0.957/0.831.

Full sample plus both halves, with correlations and holding stats from the same run:

| | CAGR | Vol | Sharpe | MaxDD | H1 | H2 | corr base | corr SPY | names held | avg vol20 held | turnover |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A equal-weight all eligible 75% | 10.4% | 9.9% | **1.048** | -15.9% | 1.069 | 1.032 | 0.740 | 0.802 | 37.5 | 19.8% | 8.2x/yr |
| B equal-weight all eligible 100% | 13.9% | 13.2% | 1.048 | -20.9% | 1.069 | 1.032 | 0.740 | 0.803 | 37.5 | 19.8% | 10.9x/yr |
| C v1 top-5 by score 75% (baseline) | 6.4% | 10.2% | 0.663 | **-13.8%** | 0.646 | 0.682 | 1.000 | 0.525 | 5.0 | **14.1%** | 23.6x/yr |
| D bottom-5 by score 75% | **7.4%** | 13.7% | 0.587 | -23.9% | 0.513 | 0.653 | 0.397 | 0.663 | 5.0 | 23.9% | 39.1x/yr |
| E top-5 by 12-1 momentum 75% | 19.9% | 18.8% | **1.060** | -24.1% | 1.046 | 1.084 | 0.643 | 0.599 | 5.0 | 30.3% | 15.1x/yr |
| C2 composite, no vol-scaling (diag) | 16.5% | 17.8% | 0.951 | -21.6% | 0.901 | 0.999 | 0.710 | 0.583 | 4.9 | 29.4% | 17.6x/yr |
| RULES v1 baseline | 6.4% | 10.2% | 0.663 | -13.8% | 0.646 | 0.682 | 1.000 | 0.525 | 5.0 | 14.1% | — |
| SPY | 15.2% | 17.7% | 0.887 | -33.7% | 0.957 | 0.831 | 0.525 | 1.000 | — | — | — |

Head-to-head spreads (daily, same 75% gross, same eligibility filter):

- **C − D** (top-5 minus bottom-5): **-1.27%/yr, t = -0.40**, corr(C,D) 0.397. The score's own long-short spread is indistinguishable from zero, and its sign is *wrong*.
- **C − A** (score minus filter-only): **-3.62%/yr, t = -2.09**. Adding the score to the filter destroys return at ~2 sigma.

## Rank information coefficient

Spearman correlation across **eligible names only**, per weekly rebalance, between the signal known at t and the forward return actually earned — entry at the close of t+1 (the day `engine.backtest` applies weights) through the close of t+1 week / t+4 weeks. 917 weekly cross-sections. The 4-week series overlaps 3-deep, so a Newey-West t-stat (lag 3) is reported next to the naive one.

| Signal | Horizon | n weeks | mean IC | std IC | t-stat | t (Newey-West) | % weeks IC > 0 |
|---|---|---|---|---|---|---|---|
| **v1 composite score (as traded)** | 1w | 917 | **+0.0042** | 0.302 | **0.42** | — | 52.2% |
| **v1 composite score (as traded)** | 4w | 914 | **+0.0011** | 0.300 | **0.11** | **0.07** | 52.2% |
| composite before vol-scaling | 1w | 917 | +0.0445 | 0.320 | 4.21 | — | 56.5% |
| composite before vol-scaling | 4w | 914 | +0.0691 | 0.306 | 6.83 | 4.51 | 62.1% |
| 12-1 momentum only | 1w | 917 | +0.0455 | 0.354 | 3.89 | — | 55.0% |
| 12-1 momentum only | 4w | 914 | +0.0662 | 0.332 | 6.03 | 3.90 | 59.9% |
| 1/sqrt(vol20) only (the scaler) | 1w | 917 | -0.0494 | 0.343 | -4.37 | — | 43.0% |
| 1/sqrt(vol20) only (the scaler) | 4w | 914 | -0.0909 | 0.317 | -8.68 | -5.68 | 37.1% |

Split by era, the traded score is zero in both: 1w IC +0.0028 (t +0.19) in 2009–2016 and +0.0053 (t +0.39) in 2017–2026; 4w IC +0.0053 (t +0.37) then **-0.0023 (t -0.17)**.

## Walk-forward (PROTOCOL rule 8)

The only in-sample decision is *which variant* — no variant has a tunable parameter of its own — so the choice is made on 2009–2016 Sharpe alone among the four briefed alternatives (A, B, D, E; C is the incumbent and C2 a diagnostic, so neither is a candidate), and 2017–2026 is untouched.

| | IS CAGR | IS Sharpe | IS MaxDD | OOS CAGR | OOS Sharpe | OOS MaxDD |
|---|---|---|---|---|---|---|
| A equal-weight all eligible 75% | 9.3% | 0.970 | -11.2% | 11.3% | 1.110 | -15.9% |
| B equal-weight all eligible 100% | 12.4% | 0.970 | -14.8% | 15.1% | 1.110 | -20.9% |
| C v1 top-5 by score 75% (baseline) | 5.0% | 0.558 | -13.1% | 7.7% | 0.743 | -13.8% |
| D bottom-5 by score 75% | 5.4% | 0.468 | -19.7% | 9.0% | 0.678 | -23.9% |
| **E top-5 by 12-1 momentum 75%** | **16.9%** | **1.033** | -17.7% | **22.4%** | **1.089** | -24.1% |
| C2 composite, no vol-scaling (diag) | 14.2% | 0.895 | -18.3% | 18.5% | 0.995 | -21.6% |
| RULES v1 baseline | 5.0% | 0.558 | -13.1% | 7.7% | 0.743 | -13.8% |
| SPY | 15.0% | 0.899 | -22.1% | 15.4% | 0.879 | -33.7% |

**Variant selected on 2009–2016 Sharpe: E (1.033).** Its untouched 2017–2026 result: **CAGR 22.4%, Sharpe 1.089, MaxDD -24.1%**, versus **baseline OOS CAGR 7.7%, Sharpe 0.743, MaxDD -13.8%** and **SPY OOS CAGR 15.4%, Sharpe 0.879, MaxDD -33.7%**. The edge did not decay out of sample — but it is bought with 10.3pp more drawdown than the baseline, and see memo line 9 on survivorship.

## KEEP path 4b (added to PROTOCOL.md by commit 8d69180 while this script was running)

Thresholds computed from SPY over the same sample: H1 Sharpe > 0.957, H2 Sharpe > 0.831, OOS Sharpe > 0.879, MaxDD ≥ -20.23% (60% of SPY's -33.7%), CAGR ≥ 10.63% (70% of SPY's 15.2%).

| | H1 | H2 | OOS | MaxDD | CAGR | 4b verdict |
|---|---|---|---|---|---|---|
| A equal-weight all eligible 75% | PASS | PASS | PASS | PASS | **fail (10.4% vs 10.63%)** | fails CAGR by 0.23pp |
| B equal-weight all eligible 100% | PASS | PASS | PASS | **fail (-20.9% vs -20.23%)** | PASS | fails MaxDD by 0.7pp |
| C v1 top-5 by score 75% (baseline) | fail | fail | fail | PASS | fail | fails 4 of 5 |
| D bottom-5 by score 75% | fail | fail | fail | fail | fail | fails all 5 |
| E top-5 by 12-1 momentum 75% | PASS | PASS | PASS | **fail (-24.1%)** | PASS | fails MaxDD |
| C2 composite, no vol-scaling (diag) | fail | PASS | PASS | fail | PASS | fails 2 of 5 |

**No variant is a 4b KEEP.** A and B are the *same strategy at two gross levels* and they bracket the test: at 75% gross it misses the CAGR floor by 0.23pp, at 100% gross it misses the drawdown ceiling by 0.7pp. Some intermediate gross (roughly 85–90%) would clear both — and picking that number now, knowing the thresholds, is precisely the "tune until it works" that rule 7 forbids. It is not done here. The honest status is PARK, pending a gross level chosen on 2009–2016 alone and re-tested on 2017–2026 in a separate pre-registered script.

## Memo

1. **The composite as traded carries essentially no cross-sectional information.** Its rank IC among eligible names is **+0.0042 at 1 week (t = 0.42)** and **+0.0011 at 4 weeks (t = 0.11, NW 0.07)** — zero to three decimals, and zero separately in 2009–2016 and 2017–2026. It is right in 52% of weeks, which is what a coin does.
2. **The falsification test fails outright.** Bottom-5 by score (D) *out-earned* top-5 (C): 7.4% vs 6.4% CAGR. The C−D long-short spread is **-1.27%/yr with t = -0.40** — no skill, and the point estimate has the wrong sign. If the score ranked returns, this number would be large and positive.
3. **D's worse Sharpe is a volatility artefact, not evidence of skill.** C holds names averaging **14.1%** vol20 and D **23.9%**; D's return is 14% higher and its vol 34% higher. Dividing by `sqrt(vol20)` makes the score a low-volatility selector, so C wins on ratio while losing on return. That is a risk dial, not alpha.
4. **The filter alone beats filter-plus-score decisively.** At identical 75% gross, A returns **10.4% at Sharpe 1.05** against the baseline's 6.4% at 0.66, with *lower* volatility (9.9% vs 10.2%), higher Sharpe in **both** halves (1.07/1.03 vs 0.65/0.68), and a third of the turnover (8.2x vs 23.6x/yr). Adding the score subtracts **3.62%/yr at t = -2.09**. Essentially all of RULES v1's Sharpe comes from step (1); step (2) is a drag.
5. **The information is real — the `/sqrt(vol20)` transform is what destroys it.** Before vol-scaling the composite's IC is **+0.045 (t 4.2) at 1w and +0.069 (NW t 4.5) at 4w**. The scaler on its own scores **-0.049 (t -4.4) and -0.091 (NW t -5.7)**. Two roughly equal-and-opposite signals are multiplied and the product is noise. C2 confirms it in returns: dropping only that division takes the same top-5 rule from 6.4% / 0.66 to **16.5% / 0.95**.
6. **The three-factor composite adds nothing over one plain momentum number.** 12-1 alone scores IC +0.046/+0.066 against the un-scaled composite's +0.045/+0.069 — statistically the same signal. In returns, E (19.9%, Sharpe 1.06) edges C2 (16.5%, 0.95). The 6m and 3m legs are decoration.
7. **Rule 4a: KILL for all five variants and the diagnostic.** A, B, E and C2 clear the both-halves Sharpe test against the live book comfortably; every one of them has a deeper drawdown than the baseline's -13.8%, so none passes 4a. D fails both conditions.
8. **Rule 4b: no KEEP either, but two near-misses, and rule 8 says they are not in-sample luck.** A fails only the CAGR floor (by 0.23pp) and B — the same book at 100% gross — fails only the drawdown ceiling (by 0.7pp); E fails only MaxDD. E was picked on 2009–2016 alone and its OOS numbers are *better* than in-sample (Sharpe 1.089 vs 1.033; 22.4% vs 16.9% CAGR), the opposite of the idea-20 failure mode, and A's OOS Sharpe is 1.110 against the baseline's 0.743. **PARK A, B and E; KILL C, D and C2.** An intermediate gross would convert A/B into a 4b KEEP, and choosing it here would be the tuning rule 7 forbids — it needs a pre-registered follow-up.
9. **The one thing that could still be an illusion is survivorship, and it hits E hardest.** `universe.json`'s megacap list is *current* constituents (NVDA, TSLA, PLTR, AVGO, META), so "top-5 by 12-1 momentum among 56 current large caps" is exactly the rule that most benefits from knowing which names survived. A and B equal-weight ~37 names and are far less exposed; the composite-carries-no-information result (lines 1–5) is a within-universe comparison between rules that share the same filter and the same 56 tickers, so it is immune to the bias entirely. E should be re-run on a point-in-time universe before anyone believes 22% OOS CAGR.
10. **What this implies for the live rules.** Do **not** ship E on this evidence. The defensible changes are to stop pretending the score ranks anything: **(a)** drop the `/sqrt(vol20)` division from `baseline.score` — a one-line edit that restores a t≈4 signal — or **(b)** stop selecting on score at all and equal-weight the eligible set (variant A): better Sharpe in both halves, lower vol, a third of the turnover, no free parameters. (a) is the smaller, better-understood edit; (b) is the stronger result but changes the book from 5 positions to ~37, which the live bot is not sized for. Both are alpha changes to RULES v1 rules 2–3 and per rule 6 require a Sunday review entry, a CHANGELOG line and a version bump in `RULES.md` / `products/bot/bot.py` — neither should be made from one script. **Caveats:** `load_universe()` downloads live prices so the last bar can move between runs (three runs here reproduced every figure to the reported precision); costs are 10 bps on next-day execution with no other slippage; IC is measured on the tradable t+1 grid and the 4-week series overlaps, hence the Newey-West column.

*Per instruction, `research/LEADERBOARD.md` was not modified — the six rows above are ready to append, and nothing was committed by this session. Note: commit `8d69180`, made by a concurrent session at 23:25, swept this script into its tree while it was still being written; the file on disk is the final version and supersedes what that commit captured.*
