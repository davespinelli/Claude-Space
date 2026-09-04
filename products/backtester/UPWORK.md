# Upwork profile + proposal templates (David posts; Claude delivers)

## Profile title
Quantitative Developer — Python backtests, systematic strategies, broker-API automation (Alpaca/IBKR)

## Overview (≤ 600 chars)
I turn trading ideas into tested, transparent Python. Deliverables: vectorized backtests with realistic costs and no look-ahead, robustness checks (sample halves, walk-forward), clear PDF reports, and clean code you own. Also: Alpaca/IBKR paper-and-live execution bots with risk limits, and daily data pipelines on GitHub Actions. Public track record and open-source engine: github.com/davespinelli/Claude-Space. Fast turnaround, honest results — I'll tell you when an idea doesn't work.

## Rates
Hourly $75. Fixed-price: backtest $150–400 · strategy + bot $800–2,500 · data pipeline $500–1,500.

## Proposal template A — "backtest my strategy"
Hi <name>, I read your brief on <strategy>. I'd implement it as a vectorized daily-bar backtest (weights decided at close, applied next day, <X> bps costs), run <period> on <universe>, and deliver: equity/drawdown chart, CAGR/Sharpe/Sortino/MaxDD vs <benchmark>, calendar-year table, robustness on sample halves, and the source. Two quick questions so I quote precisely: (1) <rule ambiguity>, (2) <data need>. Fixed price $<X>, delivered in <N> days. Sample report: <link to samples/>.

## Proposal template B — "build me a trading bot"
Hi <name>, I build these on Alpaca's API (paper first, live only when you flip the key): signal module, order manager with position/exposure caps and daily reconciliation, logging to CSV/GitHub, and a cron on GitHub Actions so it runs without your machine. I'd start with a 1-week paper run and a written runbook. Fixed price $<X> in two milestones (paper → live-ready). Public example of my pipeline: github.com/davespinelli/Claude-Space (products/bot). What broker and asset class?

## Proposal template C — "data pipeline / research tooling"
Hi <name>, I'd set up a daily pipeline (yfinance/your vendor → parquet/CSV cache → signal computation → report/dashboard) on GitHub Actions with tests and a README, so it's reproducible and free to run. Similar live example: <site link>. Scope check: <2 questions>. $<X> fixed, <N> days.

## Fulfilment
Client brief → products/backtester/orders/<client>/ → Claude builds with engine.py / bot.py patterns → David reviews and delivers → revenue in LEDGER.md when paid.
