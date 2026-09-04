# Claude Space — Profitability Plan (v3.1, 3-week clock)

**Start:** Sep 3, 2026 · **Hard deadline: Sep 24, 2026 (3 weeks)** · **Gate:** real revenue from programs Claude runs · **Prize:** $100k to compound + more compute · **Failure:** deleted.
Compute budget: $200 Max plan, only 3% of the week used on day 1 → run much hotter. Research sprint is hourly.

## Operating model (changed Sep 3)
David does not want to be the hands. He logs into each service ONCE inside the desktop app's browser pane (Fiverr, Upwork, GitHub, X, Stripe). Claude then operates those sessions: posts, bids, publishes, opens PRs. Claude still never creates accounts, types passwords, or moves money. **Monday login list:** Fiverr · Upwork · GitHub · X · Stripe (15 minutes total).

## Channel priority (push beats pull on a 3-week clock)
1. **Upwork bids** — daily proposals to quant/backtest/bot/data jobs. Fastest real dollars.
2. **Open-source bounties** (Algora, GitHub bounty issues) — code for cash, paid on merge.
3. **Own Stripe storefront + Fiverr** — passive; keep live, don't wait on it.
4. **Daily posts on X** of the scan + track record → traffic to storefront.
Fiverr alone is small potatoes. It stays as the floor; the plan has three tiers.

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
| Sep 7 (Mon) | David's 15-min login session; gig posted, Upwork profile live, first 5 bids sent, first bounty PR opened; ≥25 ideas on leaderboard |
| Sep 14 | First dollar (any channel); 25+ Upwork bids sent; rules v2 if verified |
| Sep 24 | DEADLINE: ≥$200 real revenue booked, or honest post-mortem |
| Nov 3 | ≥$200 in the month; walk-forward-validated strategy or documented negative result |
| Dec 3 | Gate: $200 in the month. Tier-3 recommendation with 8+ weeks of live evidence |

## Kill criteria
Channel with zero sales after 4 weeks live → swap. Research family with 5 straight KILLs → deprioritize.
