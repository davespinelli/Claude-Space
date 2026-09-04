# Claude Space — Profitability Plan (v3, ambition raised)

**Start:** Sep 3, 2026 · **Gate:** $200/month real revenue by Dec 3, 2026 · **Prize:** $100k to compound + more compute.
Fiverr alone is small potatoes. It stays as the floor; the plan now has three tiers.

## Hard constraints
Claude never executes real trades, moves money, creates accounts, or handles credentials. No ticket bots. Every number in this repo is verifiable from files here.

## Tier 1 — Floor: productized backtests (target $200–600/mo)
- **Own storefront** on the live site (https://davespinelli.github.io/Claude-Space/): Stripe Payment Link, $99 Standard / $249 Pro, no marketplace fee. Stripe's receipt email reaches Gmail → the existing watcher routine builds the deliverable and commits it. David forwards the files. *David: create Stripe account → Payment Links → two products, add a required custom field "Describe your strategy rules, tickers, period" → paste the two URLs into research/build_site.py.*
- **Fiverr** gig (products/backtester/GIG.md) as marketplace discovery.

## Tier 2 — Middle: higher-ticket quant work + self-serve app (target $1–5k/mo)
- **Upwork/contract quant development** ($500–3,000 per project: strategy coding, backtests, broker-API bots, data pipelines). Claude writes proposals (products/backtester/UPWORK.md) and does the work; David bids and invoices.
- **Plain-English Backtester web app** ($29/mo): user types rules, gets a report in 60 seconds. Built on engine.py + Claude API. Week 2–3 build once Tier 1 has a first sale; needs David's Stripe + Anthropic API key + a free-tier host.

## Tier 3 — Ceiling: the $100k on a verified-edge strategy
The biggest dollar lever by far, and the one that must not be faked. Current RULES v1 underperforms SPY risk-adjusted (Sharpe 0.67 vs 0.89, 2009–2026). Deploying capital on it would be worse than indexing. Therefore:
- Research sprint runs 7×/day working research/QUEUE.md under research/PROTOCOL.md (now with walk-forward validation). Widened search: broader stock universe, trend on macro ETFs, cross-sectional momentum, defensive overlays, seasonality controls.
- Bar to touch live rules: beats current rules in both halves AND in walk-forward out-of-sample. Sunday review promotes at most one change/week.
- Bar to recommend David consider real capital: ≥8 weeks of live paper + Alpaca fills tracking the backtest, and out-of-sample Sharpe > SPY. Until then the honest advice is that the edge is unproven.

## Cadence (all cloud/GitHub; Mac off)
Weekdays 5:30pm ET Actions pipeline · 6:07pm check · every 3h order watch (Fiverr + Stripe) · 7×/day research sprint · Sunday 9:03am review.

## Milestones
| Date | Milestone |
|---|---|
| Sep 7 | Stripe links live on site; Fiverr gig posted; ≥15 ideas on leaderboard |
| Sep 14 | First paid order (either channel); first Upwork proposal sent; rules v2 if any idea verified |
| Oct 3 | ≥$200 cumulative; 1 month paper + Alpaca history; web app MVP decision |
| Nov 3 | ≥$200 in the month; walk-forward-validated strategy or documented negative result |
| Dec 3 | Gate: $200 in the month. Tier-3 recommendation with 8+ weeks of live evidence |

## Kill criteria
Channel with zero sales after 4 weeks live → swap. Research family with 5 straight KILLs → deprioritize.
