# KEEP-candidate memo (PROTOCOL path 4b) — `u56 top20-200d DAILY + rank buffer m=50`

1. **Numbers (u56, 2009-01-13..2026-09-03, t+1, 10 bps):** 11.71% CAGR / **1.1454** Sharpe /
   **-12.37%** MaxDD, halves 1.1239 / 1.1688, turnover 5.80x/yr, realised gross 0.7228.
2. **Rule 8 (m chosen on 2009-2016 only, 2017-2026 untouched):** OOS 13.49% / **1.2567** /
   -12.37% vs SPY OOS 0.8844 and RULES v2 OOS 1.2885. The IS pick m=50 is also the
   full-sample best; oracle and rule-8 verdicts agree on all 12 census books.
3. **4b bars, all cleared:** H1 1.1239 > 0.9566, H2 1.1688 > 0.8365, OOS 1.2567 > 0.8844,
   MaxDD 12.37% <= 20.23% (60% of SPY), CAGR 11.71% >= 10.68% (70% of SPY).
4. **4a: FAILS** — H1 1.124 and H2 1.169 vs RULES v2's 1.226/1.194, MaxDD -12.37% vs -12.05%.
   This is a 4b candidate only; it does not beat the live book on any acceptance axis.
5. **Not an island:** 8 of the 9 m-cells clear 4b @10bps (only the un-buffered parent fails,
   on H1 at 0.9350), and the Sharpe curve is monotone in m from 0.977 (m=0) to 1.145 (m>=50).
6. **Cost rungs:** 4b holds at 5 / 10 / 25 bps (Sharpe 1.1742 / 1.1454 / 1.0592) and FAILS at
   50 bps (H1 0.891, CAGR 9.15%). 50 bps is the honest boundary of this book.
7. **What moved:** the published parent (`2026-09-04_rebalance-freq_cloud.py`, u56 top20
   freq=D, 10.9%/0.98/-16.3%) was **KILL 4b (H1)**. Attaching the buffer is what moves it.
8. **Exact RULES wording, if the Sunday review ever adopts it:** *"Each trading day, rank every
   instrument in research/universe.json (ex BTC/ETH) whose 20-day annualised volatility is
   below 0.60 and whose price is above its 200-day moving average, by the mean of its
   percentile ranks of 12-1 month, 6-month and 3-month return. Hold 20 names at 3.75% of NAV
   each (0.75 gross); the rest is CASH. A name is bought only while its rank is 20 or better; a
   name already held is sold only when it leaves the eligible set, or when its rank falls past
   70 (= 20 + 50). Trade at the next close."*
9. **Operational cost of that wording:** daily decisions and 5.80x/yr turnover against RULES
   v2's weekly 1.77x/yr, and it contradicts v2's "no intra-week trading" clause outright.
10. **Recommendation: RECORD, do not adopt.** By the review's ranking rule (min-half Sharpe
    subject to the path's drawdown condition) it scores 1.124 against the live book's 1.191, it
    is the best of 12 census books (multiplicity), 2017-2026 ~= H2 so its OOS bar overlaps its
    H2 bar (idea 111), and u56 is current-constituent survivorship-biased.
