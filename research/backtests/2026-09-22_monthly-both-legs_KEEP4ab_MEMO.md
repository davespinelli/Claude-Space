# KEEP-candidate memo — the both-paths book on a MONTHLY clock (idea 2256, lane cloud, run 12)

1. **What it is.** The record's only 4a+4b book — idea 142's `S3-50 + band3-rw` blend — refreshed
   MONTHLY instead of weekly. Nothing else changes: same n=20, same 0.50 blend, same TLT/GLD/UUP
   sleeve, same 3% band, same gross 0.75, same t+1 execution.
2. **Why it exists.** The 2026-09-20 Sunday review refused the weekly cell on turnover alone
   (8.18x/yr vs the live book's 1.77x). Monthly cuts that to **3.87x/yr** — and raises Sharpe.
3. **u56 @10 bps, FULL:** 12.06% / 1.3171 / −10.35%, halves **1.3256 / 1.3109**, turnover 3.87x/yr,
   mean realised gross 0.7513. Live RULES v2: 8.62% / 1.2010 / −12.05% (1.2276/1.1806).
4. **u56 @10 bps, OOS (2017–2026, read once):** 12.71% / **1.3591** / −10.35% vs live 9.46% /
   1.2767 and SPY 15.29% / 0.8751 / −33.72%.
5. **Both KEEP paths, both panels, 5/10/25 bps.** 4a: Sharpe higher in BOTH halves and MaxDD
   1.70 pp shallower than the live book. 4b: halves beat SPY's 0.9570/0.8264, OOS Sharpe beats
   0.8751, MaxDD −10.35% inside the −20.23% cap, CAGR 12.06% above the 10.60% floor.
6. **Rule 8 reaches it with ONE parameter.** IS-Sharpe argmax over the four same-clock cadence
   rungs on 2009–2016 alone picks M at **8 of 8** panel x cost cells; 4a 8/8, 4b FULL 7/8, 4b OOS
   7/8. (Disclosure: this chooser was added post-hoc, after the split-clock device died.)
7. **Where it breaks.** u56 at 50 bps loses 4b on the FULL sample (CAGR 10.34% vs a 10.60% floor)
   while keeping 4a and 4b OOS; broad at 50 bps loses 4b OOS. Monthly is not cost-proof, only
   cost-robust to 25 bps — which is the first time this book has been.
8. **Survivorship (rule 9).** u56 / broad are 2026 constituents held from 2008; CAGR levels are
   optimistic and both 4b level legs are easier than on a point-in-time panel.
9. **Not adopted here.** PROTOCOL rule 6 gives a rules change to the Sunday review, one per week.
10. **Exact RULES wording if adopted** (replaces RULES v2 clauses 1–3 wholesale):

> **1. Universe.** The 56-name ETF/mega-cap panel (`research/universe.json`).
> **2. Signal.** A name is IN if its close has crossed above its 200-day moving average x 1.03 and
> has not since crossed below x 0.97 (sticky in between; OUT before 200 closes exist).
> **3. Book.** On the last trading day of each MONTH, compute the composite rank (12-1 momentum,
> 6-month and 3-month return, each percentile-ranked and averaged) over the IN names only, take
> the top 20 at equal weight for HALF the book, and the TLT/GLD/UUP momentum-vote x 60-day
> risk-parity sleeve, masked by the same band, for the other HALF; rescale the blend so total
> gross equals 0.75 of NAV. Gated-out weight goes to CASH. Execute at the NEXT close.
> **4. No rebalancing between month-ends.** Positions drift.
