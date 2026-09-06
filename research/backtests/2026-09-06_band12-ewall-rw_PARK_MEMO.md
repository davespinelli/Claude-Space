# PARK memo — `EWall + band12-rw` (idea 61 by-product, 2026-09-06, cloud)

1. **The book.** Equal-weight every name whose 200d gate is IN under a **±12% hysteresis band**,
   at **gross 0.75 / N_in** (re-weight convention: gated-out weight is re-spread over the
   survivors, so realised gross is pinned at 0.7503), weekly, applied at t+1, 10 bps.
2. **U56 @10bps:** CAGR **14.02%**, Sharpe **1.2264**, MaxDD **−19.42%**, halves
   **1.2611 / 1.2048**, turnover **1.93x/yr** (vs the live book's 7.9x on the same panel).
3. **U56 @25bps:** 13.69% / **1.2000** / −19.53% — it survives the higher rung intact,
   because 1.93x/yr turnover is the whole point.
4. **Rule 8:** IS 1.1762, **OOS 1.2662** (CAGR 15.16%, MaxDD −19.42%) against SPY OOS 0.8820.
   It is the *best* OOS Sharpe of all 41 full-sample 4b passes in this run.
5. **4b PASS on U56 at both rungs.** Against SPY (Sharpe 0.8890, halves 0.9566/0.8340, CAGR
   15.23%, MaxDD −33.72%): H1 1.261 > 0.957, H2 1.205 > 0.834, MaxDD −19.42% inside
   0.60×(−33.72%) = −20.23%, CAGR 14.02% above 0.70×15.23% = 10.66%.
6. **Not a gross-ladder point:** against the un-gated constant-gross ladder at its own realised
   0.7503, dSharpe **+0.1024** — the largest gross-matched margin in the run (idea 277's control).
7. **4a FAIL** (H2 1.205 vs the live book's 1.191 clears, but MaxDD −19.4% is worse than
   −12.05%). The live book is not beaten on its own terms.
8. **Why PARK, not KEEP.** It **fails 4b on B136** — same arm, same convention: 13.64% / 1.1764 /
   **−21.74%** against the −20.2% drawdown cap, the DD bar and nothing else. A candidate that
   passes on one large-cap panel and misses the cap by 1.5pp on the other is scoped, not adopted.
9. **And no honest chooser picks it.** The pre-registered rule-8 IS-Sharpe chooser on this cell
   picks `STALE/63` (OOS 0.9994), not `BAND/0.12`; b = 0.12 is one grid step from the edge
   (0.20) and the cell's plateau is a single arm wide.
10. **Exact RULES wording if it is ever adopted** (do NOT edit RULES.md from here — Sunday review
    only): *"Clause 2 (eligibility). A name is IN when its close exceeds its 200-day moving
    average by more than 12%, OUT when it falls more than 12% below, and otherwise holds its
    previous state; OUT before 200 closes exist. Clause 3 (weights). Hold every IN name at
    0.75 / N_in of NAV, N_in = names IN that day; if no name is IN, hold cash. Clause 4
    (cadence). Rebalance weekly, at the last trading day of the week, executed at the next
    close."*

**SURVIVORSHIP:** U56 and B136 are current-constituent lists. The bias runs *against* the slow
arm — a ±12% band is slow to exit a name a delisting-aware panel would kill — so this book's
real-world numbers are worse than shown, not better. Stated, not adjusted. No level here is a
tradable estimate.
