# MEMO — 4a KEEP-candidate: B136 scored-eligible equal weight at g=0.375 with the residual in SHY

1. **Object.** Idea 329/333's anchor arm at `n = ALL`, `gross = 0.375`, on B136, with the
   un-invested 62.5% of NAV held in **SHY** (1–3y Treasuries) instead of earning zero.
   Source: idea 383, `2026-09-07_does-the-CALMAR-RAY-survive-a-NON-CASH-de-gross_cloud.py`.
2. **Numbers @10 bps, full sample (2009-01-13 → 2026-09-04):** CAGR **6.27%**, Sharpe
   **1.1777**, MaxDD **−11.10%**, H1/H2 **1.2605 / 1.1044**, turnover 4.43x/yr, 90.6 names.
3. **4a bars (vs RULES v2 on B136 @10 bps: 8.03% / 1.106 / −12.24%, H1/H2 1.229/0.984):**
   H1 **+0.032**, H2 **+0.120**, MaxDD **+1.14 pp better**. **PASSES 4a.**
4. **Rule 8 (PROTOCOL 8).** Parameters chosen on IS 2008-2016 Sharpe @10 bps pick this
   exact cell; OOS 2017-2026 read once: **OOS Sharpe 1.2025** vs RULES v2 OOS 1.1185 and
   SPY OOS 0.8820; OOS CAGR 6.47%, OOS MaxDD −11.10%; regret to the OOS argmax +0.0110.
   **Survives.**
5. **4b: FAILS**, on the CAGR floor alone — 6.27% against the 10.66% required (70% of SPY's
   15.23%). The DD cap, both half-Sharpe bars and the OOS bar all clear comfortably. This
   is a low-return defensive book, not a capital-worthy one.
6. **Fragility, stated up front.** 4a passes in **1 of 180 cells at 10 bps**, 9 of 180 at
   0 bps, and **0 of 180 at 25 bps** (H1 is the failing bar there). Its edge does not
   survive a doubling of the cost assumption.
7. **What it actually is.** SHY earns 1.34% CAGR at Sharpe 0.984 over the sample. Most of
   the gain over the identical cash cell (5.40% / 1.020 / −9.77%) is the **risk-free rate
   the record has been setting to zero**, not an edge in this book. The remainder is a
   diversification effect from a near-uncorrelated 0.98-Sharpe sleeve.
8. **Regime caveat.** 2009–2021 is a one-directional rate environment for SHY. Its −5.71%
   drawdown is concentrated in 2022 and the sleeve is 62.5% of NAV; this is a duration
   position, small but real, and it is not hedged.
9. **Exact RULES wording, if the Sunday review adopts it** (proposed as a clause on the
   existing book, replacing nothing):
   > **Clause 4 (residual sleeve).** Weight not invested in the book is held in SHY, not
   > in cash. The sleeve is rebalanced to `1 − gross` of NAV on the same weekly schedule
   > as the book, and its turnover is charged at the same rate.
10. **Recommendation: DO NOT adopt this week.** Take amendment 3 of idea 383's result
    instead — price the zero-cash convention across the record before writing a residual
    sleeve into RULES, because if the convention is the effect, the clause is an
    accounting fix that belongs in the backtester, not a rule. Survivorship applies (B136
    is a current-constituent list).
