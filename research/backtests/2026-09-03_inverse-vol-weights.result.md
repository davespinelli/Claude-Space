# Idea 7 — inverse-vol-weights (results)

Script: `research/backtests/2026-09-03_inverse-vol-weights.py`
Run: 2026-09-03 · 56 tickers · 2008-01-02 → 2026-09-03 (4698 rows) · costs 10 bps · freq="W" · next-day execution
Selection is RULES v1 verbatim (top 5 by `baseline.score`, 200d-MA filter, vol20 < 0.60). Only sizing varies.

## LEADERBOARD rows

| Date | Idea | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | Baseline Sharpe (H1/H2) | Verdict | Script |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | inv-vol 75% gross | 5.0% | 0.57 | -14.4% | 0.60 / 0.54 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_inverse-vol-weights.py |
| 2026-09-03 | inv-vol 100% gross | 6.5% | 0.57 | -19.1% | 0.60 / 0.54 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_inverse-vol-weights.py |
| 2026-09-03 | equal-weight 100% gross (diagnostic) | 8.5% | 0.67 | -18.2% | 0.65 / 0.69 | 0.67 (0.64/0.69) | KILL | research/backtests/2026-09-03_inverse-vol-weights.py |

Full `compare()` tables as printed:

```
                   CAGR  Sharpe  MaxDD    H1    H2
inv-vol 75% gross 0.050   0.568 -0.144 0.601 0.543
RULES v1 baseline 0.065   0.668 -0.138 0.645 0.692
SPY               0.153   0.890 -0.337 0.957 0.837

                    CAGR  Sharpe  MaxDD    H1    H2
inv-vol 100% gross 0.065   0.567 -0.191 0.601 0.540
RULES v1 baseline  0.065   0.668 -0.138 0.645 0.692
SPY                0.153   0.890 -0.337 0.957 0.837

                                      CAGR  Sharpe  MaxDD    H1    H2
equal-weight 100% gross (diagnostic) 0.085   0.669 -0.182 0.648 0.691
RULES v1 baseline                    0.065   0.668 -0.138 0.645 0.692
SPY                                  0.153   0.890 -0.337 0.957 0.837
```

## Memo

1. Tested: RULES v1 selection held fixed; the 5 held names sized ∝ 1/vol20 (vol floored at 0.08, as in `score`) instead of a flat 15%, at 75% gross (v1-comparable) and 100% gross, plus an equal-weight 100% gross diagnostic to separate weighting from exposure.
2. Both halves vs baseline: inv-vol 75% posts Sharpe 0.601 / 0.543 against the baseline's 0.645 / 0.692 — worse in H1 and materially worse in H2, so it fails PROTOCOL rule 4 on the first test.
3. inv-vol 100% is essentially the same risk-adjusted result (0.567 full, 0.601 / 0.540 halves): levering the sleeve up raises CAGR from 5.0% to 6.5% but scales the drawdown with it, leaving Sharpe unchanged.
4. All three variants are far below SPY buy-and-hold (Sharpe 0.890, CAGR 15.3%), which remains the uncomfortable headline for this whole family of rules.
5. MaxDD: inv-vol 75% is -14.4% vs baseline -13.8% — slightly worse despite identical gross exposure, i.e. the concentration cost is not repaid. inv-vol 100% is -19.1% and equal-weight 100% is -18.2%, both clearly worse than baseline.
6. Weighting vs exposure: the diagnostic settles it. Equal-weight at 100% gross reproduces the baseline's Sharpe almost exactly (0.669 vs 0.668; halves 0.648 / 0.691 vs 0.645 / 0.692) and only lifts CAGR to 8.5% by taking a proportionally deeper -18.2% drawdown — pure exposure scaling, no edge.
7. Therefore the entire Sharpe degradation from 0.67 to 0.57 is attributable to the 1/vol20 weighting itself, not to the change in gross exposure. Exposure is Sharpe-neutral here; weighting is Sharpe-destructive.
8. Mechanism: `score` already divides by sqrt(vol20), so the selection is tilted low-vol before sizing. Weighting by 1/vol20 applies the tilt a second time and concentrates hard — a single name reached 43.3% of NAV at 75% gross (min held weight 4.0%), turning a 5-name book into an effectively 2-3 name book.
9. Verdict per PROTOCOL rule 4: **KILL** for both inv-vol variants — Sharpe fails to beat baseline in either half, and MaxDD is no better. The equal-weight 100% diagnostic is also KILL (H2 Sharpe 0.691 vs 0.692, MaxDD -18.2% vs -13.8%); it is a diagnostic, not a candidate.
10. Risks/caveats: single-run, single-universe, no parameter search was done and none should be (rule 7); the vol20 floor of 0.08 is inherited from `score` and drives the concentration, so a different floor would change the concentration but is exactly the kind of tuning rule 4's parameter budget is meant to prevent; half-split is a fixed 50/50 on row count, so H1/H2 straddle regimes rather than clean cycles; and the 43% single-name weight would in practice raise position-limit and liquidity concerns well before the Sharpe result mattered.
