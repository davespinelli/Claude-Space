# Fiverr / Upwork gig listing (David posts this; Claude fulfills)

**Title:** I will backtest your stock or ETF trading strategy in Python with a full report in 48 hours

**Category:** Finance & Accounting → Financial Consulting / Data → Data Analysis

**Packages**
| | Basic $75 | Standard $125 | Premium $200 |
|---|---|---|---|
| Strategies tested | 1 | 1 + 2 parameter variants | up to 3 strategies or 5 variants |
| Universe | ≤10 tickers | ≤30 tickers | ≤100 tickers |
| History | 5 years | 10 years | 15+ years |
| Report | PDF/Markdown: CAGR, Sharpe, max drawdown, yearly returns, equity + drawdown chart, benchmark comparison | + robustness (sample halves), turnover & cost sensitivity | + walk-forward test, position-level trade log, Python source code |
| Delivery | 48h | 48h | 72h |
| Revisions | 1 | 2 | 3 |

**Description**
Have a trading idea and want to know if it actually worked before risking money? I turn your rules into code and test them on real historical daily data, with transaction costs, no look-ahead bias, and a plain-English report you can act on.

What you get:
- Your rules translated into a transparent Python backtest (no black box)
- Performance vs. buy-and-hold benchmark: CAGR, volatility, Sharpe, Sortino, max drawdown, Calmar, win rate
- Calendar-year returns table, equity curve and drawdown chart
- Robustness check: does it hold in both halves of the sample?
- Honest verdict, including when the idea doesn't beat the benchmark

Works for: momentum/trend following, moving-average crossovers, RSI/mean reversion, sector rotation, seasonal patterns, dual momentum, risk parity, rebalancing schedules, and more. Stocks, ETFs, indices, crypto (daily bars).

Not included: intraday/tick data, options pricing, live trading bots (ask for a custom quote), and anything I'd have to present as investment advice. Results are research, not a recommendation.

**Requirements from buyer (Fiverr "requirements" form)**
1. Describe your entry and exit rules in plain English (e.g. "buy SPY when it closes above the 200-day average, sell when below").
2. Tickers or universe (or say "you choose a sensible one").
3. Start year, rebalance frequency (daily/weekly/monthly), position sizing, starting capital.
4. Benchmark to compare against (default SPY).

**FAQ**
- *Do you use real data?* Yes, adjusted daily closes from Yahoo Finance; other sources on request.
- *Can I get the code?* Included in Premium; add-on for other tiers.
- *Will you tell me if my strategy is bad?* Yes. That's the point.

**Portfolio samples to attach:** `samples/sector_momentum_top3.png`, `samples/spy_200d_trend_filter.png`, `samples/sector_rsi2_mean_reversion.png` and their .md reports.

**Tags:** backtesting, trading strategy, python, quantitative analysis, algorithmic trading, stock market, ETF, financial analysis

## Fulfillment workflow (Claude side)
1. David pastes the buyer's requirements into a Claude session (or a file in `products/backtester/orders/<id>.md`).
2. Claude writes the strategy function, runs `engine.backtest` + `engine.report`, reviews for look-ahead bias, produces PDF via markdown.
3. David uploads the deliverable. Revenue logged in LEDGER.md with the order id.
