# Cost / Revenue Ledger

| Month | Cost (Claude Max) | Other cost | Revenue | Net | Notes |
|---|---|---|---|---|---|
| Sep 2026 | $200 | $0 | **$0** | -$200 | Setup month; nothing sold as of 2026-09-27 (PLAN deadline 2026-09-24 missed) |

**Cumulative net:** -$200 · **Paper NAV:** $99,312.76 on 2026-09-26 (-0.69% since 2026-09-03; SPY +0.26% over the same dates) — `paper/nav.csv`

## Revenue pipeline as of 2026-09-27 (every number verifiable from a file in this repo)
| Channel | State | Evidence |
|---|---|---|
| Freelance bids | **377 proposals drafted, 5 submitted, 0 won; channel dropped 2026-09-23** | `products/freelance/INDEX.md`: 372 rows read `drafted`, 5 read `submitted 2026-09-07`; `products/freelance/proposals/` holds 377 files. Nothing submitted in the 20 days since 2026-09-07; the 6-hourly Freelancer scan was stopped in commit "Freelance: stop the 6-hourly Freelancer.com job scan (channel dropped)" (2026-09-23). |
| Bid competitiveness | the 5 submitted bids landed **23/28, 50/66, 81/83, 100+/239, 100+/311** | rank recorded in each `submitted` cell of `products/freelance/INDEX.md`. Four of five were in the bottom half of the bid stack at submission |
| Job scanning | 776 jobs seen, scan stopped 2026-09-23 | `products/freelance/seen.csv` (777 lines incl. header) |
| Own Stripe storefront | **not live** | `research/build_site.py` lines 157-158: `stripe_std` and `stripe_pro` are still empty TODOs, so line 166 renders no buy button |
| Fiverr gig | **not published, 0 orders** | `products/backtester/GIG.md` drafted; `products/backtester/orders/` contains only its README |
| Bounties | none open | `products/bounties/SCOUT_2026-09-03.md` — boards dead or hardware-gated |
| Deep Value Desk | 214 tracked verdicts (5 IDEA / 175 WATCH / 34 PASS), **not monetised** | `research/deepvalue/COVERAGE.md`, `TRACK.md`. No paid distribution exists for it yet |

**PLAN.md's 2026-09-24 deadline passed with $0 booked.** Every paying channel still needs David's one-time
login (MONDAY.md); none happened after 2026-09-07. The freelance channel was dropped on 2026-09-23 with 372
proposals never sent. Stripe links (`research/build_site.py:157-158`) and the Fiverr gig are unchanged.
