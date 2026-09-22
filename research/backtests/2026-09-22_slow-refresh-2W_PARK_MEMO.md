# PARK memo — slower rank refresh on the both-paths cell (idea 2250, lane C, 2026-09-22)

1. **What it is.** The committed 4a+4b cell `u56 / S3-50 + band3-rw @10 bps`, with ONE change:
   the top-20 composite ranking is re-selected every SECOND week instead of every week. The
   band3 gate, the `rw` re-spread and the TLT/GLD/UUP sleeve still run WEEKLY.
2. **Numbers (u56 @10 bps, t+1).** Full 11.47% / **1.2768** / −11.09%, halves 1.3391 / 1.2212;
   OOS 11.75% / **1.2819** / −11.09%; turnover **6.64x/yr** vs the committed cell's 8.18x.
3. **Against the live book (RULES v2 @10 bps).** Full 1.2010 (1.2276/1.1805), OOS 1.2767 /
   −12.05%. Path **4a passes**; it beats the live book out of sample too.
4. **Against SPY.** 15.13% / 0.8851 / −33.72%, OOS 15.29% / 0.8751. Path **4b passes**: both
   halves and OOS above SPY, MaxDD 11.09% ≤ 20.23% cap, CAGR 11.47% ≥ 10.60% floor.
5. **It is rule-8 REACHABLE.** Parameters chosen on 2009–2016 only: choosers S0 (argmax IS
   Sharpe) and S1 (argmax IS Sharpe among IS-4b-legal books) both land on R = 2W / backfill at
   u56 @5 and @10 bps. 2017–2026 was read once, above.
6. **Exact RULES wording, if it were ever promoted.** *"Clause 1a (rank refresh). The top-20
   composite ranking is re-selected only on every second weekly rebalance date, counted from the
   first rebalance of the sample. Between refreshes the selected name set is held. Clause 2 (the
   200-day ±3% band), the re-weight to gross 0.75 and the diversifier sleeve are still read at
   EVERY weekly rebalance; a held name that leaves the band is dropped at that week's rebalance
   and the book re-spreads to gross 0.75 over the survivors, up to the size of the set the last
   refresh selected."*
7. **Why PARK and not KEEP.** It inherits its parent's disqualification unchanged: at 25 bps the
   rule-8 pick (Q/backfill) fails the promotion bar, at 50 bps 4b fails everywhere, and on
   `broad` it never beats the live book out of sample (0 of 32 cells). The 2026-09-20 Sunday
   review refused the R = W version for exactly this shape.
8. **What it does establish.** The composite rank's weekly churn is trading, not information —
   halving the refresh rate costs nothing and pays +0.0134 of full Sharpe, +0.54 pp of shallower
   drawdown and 1.5x/yr less turnover. Monthly is better still (1.3081, 5.76x) but not reachable.
9. **The blocking fact for any future attempt.** Turnover floors at ~5.2x/yr (u56) even at a
   QUARTERLY refresh; the pre-declared ≤4.0x IS chooser abstains in all 8 cells. Getting this
   book near the live book's 1.77x needs the gate, the re-spread or the sleeve, not the ranking.
10. **Survivorship (rule 9):** u56/broad are current-constituent lists; every CAGR level is
    optimistic and both 4b bars are easier than on a point-in-time panel. Not a capital decision.
