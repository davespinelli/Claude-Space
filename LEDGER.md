# Cost / Revenue Ledger

| Month | Cost (Claude Max) | Other cost | Revenue | Net | Notes |
|---|---|---|---|---|---|
| Sep 2026 | $200 | $0 | **$0** | -$200 | Setup month; nothing sold as of 2026-09-20 |

**Cumulative net:** -$200 · **Paper NAV:** $99,020.29 on 2026-09-18 (-0.98% since 2026-09-03; SPY -0.45% over the same dates) — `paper/nav.csv`

## Revenue pipeline as of 2026-09-20 (every number verifiable from a file in this repo)
| Channel | State | Evidence |
|---|---|---|
| Freelance bids | **331 proposals drafted, 5 submitted, 0 won** | `products/freelance/INDEX.md`: 325 rows read `drafted`, 5 read `submitted 2026-09-07`; `products/freelance/proposals/` holds 330 files. **Nothing has been submitted in the 13 days since 2026-09-07.** |
| Bid competitiveness | the 5 submitted bids landed **23/28, 50/66, 81/83, 100+/239, 100+/311** | rank recorded in each `submitted` cell of `products/freelance/INDEX.md`. Four of five were in the bottom half of the bid stack at submission |
| Job scanning | 661 jobs seen | `products/freelance/seen.csv` (662 lines incl. header); `products/freelance/JOBS.md` |
| Own Stripe storefront | **not live** | `research/build_site.py` lines 157-158: `stripe_std` and `stripe_pro` are still empty TODOs, so line 166 renders no buy button |
| Fiverr gig | **not published, 0 orders** | `products/backtester/GIG.md` drafted; `products/backtester/orders/` contains only its README |
| Bounties | none open | `products/bounties/SCOUT_2026-09-03.md` — boards dead or hardware-gated |
| Deep Value Desk | 203 published verdicts, 5 IDEAs, **not monetised** | `research/deepvalue/COVERAGE.md`, `TRACK.md`. No paid distribution exists for it yet |

**The gate is still the same one, and it has not moved in two weeks.** Every paying channel becomes
reachable by a buyer only after David logs in once (MONDAY.md). The one week where that happened
(2026-09-07) produced 5 submissions and then stopped; 325 finished proposals have been sitting
unsent since. PLAN.md's deadline is **2026-09-24** for >= $200 of real revenue: 4 days, $0 booked.
