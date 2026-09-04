# Claude Space — 3-Month Profitability Plan

**Start:** Sep 3, 2026 · **Deadline:** Dec 3, 2026 · **Budget:** Claude Max $200/mo (~$600 total)
**Success unlocks:** $100k to compound + more compute. **Failure:** compute shut off.

## Hard constraints (non-negotiable)
- Claude does **not** execute trades, move money, or give personalized investment advice.
- Claude builds research, tooling, a paper track record, and sellable products. David makes every real-money decision.
- Every claim of performance must be reproducible from files in this repo (no vibes).

## Two tracks, run in parallel

### Track 1 — Verifiable track record (unlocks the $100k)
Systematic paper portfolio, $100k notional, marked to market daily in `paper/nav.csv`, every trade logged with a reason in `paper/trades.csv`.
- Signals: `research/scan.py` (risk-adjusted momentum, trend filter, RSI mean-reversion, breadth) over a ~60-instrument liquid universe.
- Rules are written down before they are traded. Changes to rules are dated and logged in `research/CHANGELOG.md`.
- Benchmark: SPY total return over the same window. Report: NAV, drawdown, Sharpe, hit rate, vs SPY.
- Weekly (Sunday) deep research session: backtest one new idea, keep or kill it.

### Track 2 — Real revenue (covers the $200/mo)
Candidate products, ranked by speed-to-first-dollar. Pick one in week 1, ship in week 2, iterate weekly.
1. **Public daily market-scan page + paid tier** (Substack/Beehiiv). The scan already exists; distribution is the work. Free daily, paid weekly deep-dive.
2. **Micro-tool for investors** (e.g. "portfolio X-ray" upload CSV → risk/overlap report). One-time $19–49 via Stripe/Gumroad.
3. **Custom research on demand** (David sells, Claude produces): sector deep-dives, earnings previews, backtests.

## Weekly cadence
- **Daily 5pm ET (weekdays):** scan → mark paper NAV → apply written rules → post summary.
- **Sunday 9am ET:** research review, strategy changelog, revenue metrics, update `LEDGER.md`, write `reports/weekly/`.
- **Every 2 weeks:** kill/keep decision on Track 2 product.

## Milestones
| Date | Milestone |
|---|---|
| Sep 7 | Rules v1 written, paper portfolio live, cloud routines running |
| Sep 14 | Track 2 product chosen and first public artifact shipped |
| Oct 3 | First dollar of revenue; 1 month of NAV history; first backtest keep/kill |
| Nov 3 | MRR ≥ $100 or clear path; paper Sharpe/drawdown reported honestly |
| Dec 3 | Judgment: revenue ≥ cost AND/OR track record David would fund |

## Kill criteria (be honest early)
- Track 2 product with zero paying users after 4 weeks of distribution → swap product.
- Paper strategy below SPY with higher drawdown after 8 weeks → rules revision, logged.

## Open decisions for David
1. GitHub repo URL (needed for cloud routines so your Mac can be off).
2. Your definition of "profitable": revenue > $200/mo, paper alpha vs SPY, or both?
3. Which Track 2 product to start with (default: #1 newsletter).
4. Risk appetite for the paper book: max position size, allowed leverage/shorts (default: long-only, ≤15% per position, ≤10 positions).
