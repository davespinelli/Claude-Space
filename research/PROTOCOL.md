# Research Protocol (anti-overfitting rules for every backtest)
1. **Data:** `data/prices.csv` via `products/backtester/engine.load_prices` (falls back offline). Minimum 10 years. Universe = research/universe.json unless the idea is about universe.
2. **Execution realism:** weights decided at close t, applied at t+1 (engine does this). Costs 10 bps per unit turnover (`cost_bps=10`). No shorting, no leverage unless the idea says so.
3. **Baseline:** always compare against `research/baseline.py: rules_v1_weights` (the live paper rules) AND SPY buy-and-hold. Use `baseline.compare(name, weights_fn, px)`.
4. **Robustness:** report full sample + first/second half. KEEP requires: Sharpe > baseline in BOTH halves, MaxDD no worse than baseline overall, and no more than 2 tuned parameters. Otherwise KILL or PARK (interesting, needs more work).
5. **One idea per script**, `research/backtests/YYYY-MM-DD_<slug>.py`, deterministic, runnable standalone. Append one row to `research/LEADERBOARD.md`.
6. **Rules change only via Sunday review**, max one change per week, logged in CHANGELOG.md with version bump in RULES.md and `products/bot/bot.py`.
7. Report honestly. A KILL is a useful result. Never tune until it works.
