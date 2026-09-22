# Memo — KEEP-4b candidate from idea 913 (lane cloud, 2026-09-22): B136 / MOM / k=20 / gross 0.50 / monthly

1. **What it is.** On the 136-name broad panel, monthly at each month-end close, rank every name
   passing the gate by the composite momentum score and hold the top 20 at 2.5% of NAV each
   (gross 0.50); the rest of NAV sits in cash. Fills next close, 10 bps per unit turnover.
2. **Exact RULES wording if it were ever enacted (it should not be — see line 8):**
   *"Clause M. Each month-end close, score every instrument priced that day by the mean of its
   percentile ranks on 12-1 momentum, 6-month return and 3-month return. An instrument is
   ELIGIBLE if its close is above its 200-day moving average and its 20-day realised volatility
   is below 60% annualised. Hold the 20 eligible instruments with the highest score at 2.5% of
   NAV each; hold no other position. Weight not allocated stays in CASH and is never re-spread.
   Trade at the next close."*
3. **Numbers (full 2009-01-13 .. 2026-09-18, 10 bps, t+1):** CAGR 10.74%, Sharpe 1.0894,
   MaxDD −18.00%, halves 1.3252 / 0.9040.
4. **Out of sample (2017-01-01 onward, read once under rule 8):** 10.32% / 0.9925 / −18.00%.
5. **Against the live book (RULES v2):** 7.96% / 1.0972 / −12.24% full, OOS 7.85% / 1.1017 /
   −12.24%. **Path 4a FAILS** — the live book has the higher full-sample Sharpe and a 5.8 pp
   shallower drawdown.
6. **Against SPY:** 15.12% / 0.8844 / −33.72% full, OOS 15.26% / 0.8737 / −33.72%, halves
   0.9571 / 0.8249. **Path 4b PASSES** on all five legs.
7. **How it was reached (rule 8):** an IS-only screen on 2009–2016 only — admit books whose
   episode-window beta is ≤ 0.60, then take the highest in-sample Sharpe — then 2017–2026 read
   once. Two independent screens (the fixed-episode beta and the plain full-sample beta) reach
   the **identical** book, so the pick does not depend on the episode calendar.
8. **RECOMMENDATION: DO NOT ENACT.** The two binding legs are inside this record's own measured
   noise. The CAGR-floor margin is **+0.157 pp** and the drawdown margin **+2.23 pp**, against the
   paired circular-block bootstrap SDs of **1.86 pp** and **4.00 pp** that idea 2090 measured on
   this same shelf shape in this same session — 0.08 and 0.56 of one SD. By 2090's own standard
   this is a point estimate, not a finding.
9. **Survivorship (rule 9):** B136 is a CURRENT-constituent list, so the CAGR and MaxDD levels are
   optimistic and the 4b bars are easier than on a point-in-time panel. The candidate's pass is a
   level claim and is NOT immune to that bias.
10. **What would change the verdict:** a paired block bootstrap of this cell's own five legs (the
    2090 machinery applied to B136 / MOM / 20 / 0.50), and a cost x latency ladder. Until both
    are run and published, this is a recorded candidate only — **no RULES change, no version
    bump, nothing enacted this run.**
