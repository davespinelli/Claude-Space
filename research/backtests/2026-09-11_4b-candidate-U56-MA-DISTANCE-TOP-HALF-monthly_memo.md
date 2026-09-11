# 4b candidate memo — U56 MA-DISTANCE TOP-HALF, monthly (idea 536R, cloud 2026-09-11)

*Filed from the independent replication of idea 536; lane B's same-day run reports the same single
4b pass (4b 1/12 picks, 16/324 books, 4a 0/324) and also declines it.*

1. **What it is.** On each rebalance day rank every priced instrument by `dist = px/MA200 − 1`;
   hold the top `ceil(0.50 × N_priced)` by `dist`, equal weight, total gross 0.75, cash otherwise.
   Rebalance **monthly**; weights decided at close t, applied at t+1; 10 bps per unit turnover.
2. **Exact RULES wording, if it were ever adopted.** *"Clause 2 (replacement): on the last
   trading day of each month, rank every instrument priced that day by `px / MA200 − 1`. Hold the
   top ceil(0.50 × N) of them at 0.75/K of NAV each, K = the number held; all other NAV is CASH.
   No score, no volatility filter, no hysteresis band. Between rebalances, drift."*
3. **Numbers, 2009-01-13 → 2026-09-10, U56, 10 bps, next-day execution.** CAGR **15.47%**,
   Sharpe **1.2359**, MaxDD **−19.80%**, halves **1.3518 / 1.1454**, turnover **3.11×/yr**.
4. **Rule 8.** x = 0.50 is the **IS argmax** (IS Sharpe 1.2665, chosen on ≤2016-12-31 alone);
   OOS 2017-01-01→end read once: CAGR **15.95%**, Sharpe **1.2164**, MaxDD **−19.80%**.
5. **4b, all five bars.** H1 1.3518 > SPY 0.9595 ✓ · H2 1.1454 > 0.8211 ✓ · OOS 1.2164 > 0.8721 ✓ ·
   MaxDD 19.80% ≤ 60% of SPY's 33.72% = 20.23% ✓ · CAGR 15.47% ≥ 70% of 15.11% = 10.58% ✓.
6. **Cost stress.** Passes 4b at **0, 10, 25 and 50 bps** (CAGR 15.83 / 15.47 / 14.93 / 14.04%,
   OOS Sharpe 1.2168 / 1.2164 / 1.1800 / —), derived exactly off the same book.
7. **4a: FAILS.** The LIVE RULES v2 book (U56, the PROTOCOL 4a comparand) reads **OOS Sharpe
   1.2834** against this book's **1.2164**, and OOS MaxDD **−11.90%** against −19.80%. Adopting it
   would be a downgrade on the live comparand. **0 of the 324 books in this grid clear 4a.**
8. **The binding bar is a knife-edge.** DD margin **0.43 pp** (−0.1980 vs the −0.2023 cap); the
   neighbouring levels x = 0.20/0.30/0.70/0.80/0.90/0.95 all fail on DD. The pass is a two-rung
   window (0.40/0.50/0.60), the shape ideas 670/675/677 documented.
9. **Base rate.** 16 of this run's 324 books (4.9%) clear 4b and **0 of 324 clear 4a**; idea 502
   measured 78.1% of gross-matched coin flips clearing 4b on U56 at 0 bps. One pass of twelve
   IS-only picks is inside that noise.
10. **RECOMMENDATION: do not adopt, do not promote, no RULES change.** File it as a
    rule-8-reachable 4b pass for the record and re-test it on B136/SMALL439 and on a 1-day-delayed
    calendar before it is ever discussed for capital. SURVIVORSHIP: U56 is a current-constituent
    list, so the 15.47% level is optimistic; nothing here justifies real capital.
