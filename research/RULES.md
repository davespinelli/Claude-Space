# Paper Book Rules — v2 (effective 2026-09-06)
Applied mechanically by the daily routine. The held set is computed from the full-history price
cache `data/prices.csv` (refreshed by `research/cache_prices.py` before the rules are applied);
`reports/<date>.csv` (output of research/scan.py) supplies the trade prices and is otherwise
informational under v2.

1. **Universe:** all instruments in research/universe.json except BTC-USD and ETH-USD. Call the
   number of them that have a price on the decision day `N` (N = 56 on 2026-09-06).
2. **Membership gate (replaces v1's eligibility test):** a 200-day moving-average band with
   hysteresis, per name. A name becomes **IN** on the first close above `ma200 * 1.03`; it stays
   IN until a close below `ma200 * 0.97`, which makes it **OUT**; it stays OUT until the next
   close above the upper band. Between the two bands the previous state persists. A name with
   fewer than 200 closes is OUT. There is **no volatility filter** and **no momentum ranking**:
   v1's `score` column is informational only and is not used to select or size anything.
3. **Selection:** hold every IN name. There is no top-N cut and no ranking.
4. **Sizing:** each IN name is held at `0.75 / N` of current NAV (1.3393% at N = 56). Round shares
   down to whole units. Names that are OUT are not held and **their weight stays in cash — the
   book de-grosses.** Do NOT re-spread the gross over the IN names: a re-grossed book is a
   different, unpriced book (idea 81).
5. **Rebalance:** on the last trading day of each week only. On that day sell in full every
   holding that is OUT, buy every name that is IN and not held, and reset every position to
   `0.75 / N` of NAV.
6. **No intra-week trading.** v1's "hard exit any day" clause is **removed**: the backtest that
   qualified these rules applies its weights on the weekly schedule only, so a daily exit would be
   an unpriced addition to the book. A name that leaves the band on a Tuesday is sold on Friday.
7. **Trade price:** last close in the report (paper fill, no slippage modeled; note this as a
   known bias). Priced at 10 bps per unit turnover with next-day execution; the acceptance below
   also holds at 5, 25 and 50 bps.
8. **Reason string:** always `"RULES v2: <rebalance|exit> band=<in|out> d200=<x>"`, where `d200`
   is `close / ma200 - 1`.

## Acceptance record (why v2 replaces v1)
PROTOCOL path **4a**, verified three ways on 2026-09-06 (idea 94's `EWall + band3-dg` arm,
`research/backtests/2026-09-04_drawdown-insurance-price-list_B.py`; re-derived from scratch in the
Sunday review; robustness extended by the review). Panel u56 (research/universe.json), 2009-01-13
to 2026-09-04, weekly, next-day execution, 10 bps:

| Book | CAGR | Sharpe | MaxDD | Sharpe H1 / H2 | OOS 2017– Sharpe | Turnover |
|---|---|---|---|---|---|---|
| **v2 (this rule set)** | **8.66%** | **1.2056** | **−12.05%** | **1.2259 / 1.1908** | **1.2851** | 1.77x/yr |
| v1 (previous live rules) | 6.45% | 0.6642 | −13.83% | 0.6409 / 0.6878 | 0.7471 | — |
| SPY buy & hold | 15.23% | 0.8890 | −33.72% | 0.9566 / 0.8340 | 0.8820 | — |

v2 beats v1 on CAGR, Sharpe **and** MaxDD simultaneously, in both halves and out of sample, so it
clears 4a with no regression on any acceptance axis. Robustness measured in the review: 4a holds
at **5 of 5** weekday phases of the weekly schedule, at **5, 10, 25 and 50 bps**, and at band
widths 0%, 2%, 3%, 5% and 10% (8% fails the drawdown bar by 0.6pp).

## Scope and what v2 does NOT claim
- **Not a capital recommendation.** v2 fails PROTOCOL **4b** on one bar only — CAGR 8.66% against
  the 10.66% floor (70% of SPY). It clears the other four 4b bars, including OOS Sharpe 1.2851 vs
  SPY's 0.8820. Real capital still needs a 4b book plus ≥8 weeks of live tracking (PLAN Tier 3).
- **Scoped to research/universe.json**, which is a current-constituent list (idea 54): the absolute
  CAGR is survivorship-optimistic. The margin over v1 is a same-names, same-days difference and is
  much less exposed.
- The standing **4b** candidate remains idea 182's R6 top-20 monthly book (13.61%/1.1557/−18.81%,
  OOS 1.1695), which is NOT adopted here — see research/CHANGELOG.md 2026-09-06.

Changes require a dated entry in research/CHANGELOG.md and a version bump here.
