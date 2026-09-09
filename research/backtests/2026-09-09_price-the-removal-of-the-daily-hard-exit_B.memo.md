# Memo — idea 275: the daily hard exit is now priced. KILL. (2026-09-09, lane B)

**Not a KEEP.** This is a live-rules fidelity answer, and it confirms the live book. No rules
change is proposed here; PROTOCOL 6 reserves that for the Sunday review.

1. **What was tested.** RULES v1's removed clause — "sell at the next close any day the gate
   flips, buy back only on schedule" — built on both books, U56 + BROAD136, weekly, next-day
   execution, 15 grid points (`x` = exit depth below ma200 in {0, .01, .03, .05, .10}, `c` =
   confirmation days in {1,2,3}), 3 cost rungs, each against its own no-exit control.
   Gates: the exit-disabled path reproduces `engine.backtest` at **7e-18**, and the live v2 row
   comes in at 8.64% / 1.2037 / −12.05% against RULES.md's published 8.66% / 1.2056 / −12.05%
   (prices.csv advanced 2026-09-04 → 09-08).
2. **On the live v2 book the clause is a loser.** Literal form (x=0.00, c=1): CAGR 8.64% → 7.68%,
   Sharpe 1.2037 → 1.1473 (**−0.0564**, worse in both halves), MaxDD −12.05% → −10.50%, and
   turnover **1.78x → 5.32x/yr** on 3,068 early sells in 4,700 days. It buys 1.55pp of drawdown
   for a point of Sharpe and a percentage point of CAGR a year.
3. **On v1's own book it is near-vacuous.** v1's top-5 ranked book already turns over 23.6x/yr,
   so the weekly rebalance almost always beats the daily exit to the sell: the clause fires
   **50 times in 4,700 days** and adds +0.19x of turnover. It is worth +0.0079 Sharpe on U56 and
   +0.0081 on B136, but its drawdown sign **flips with the panel** (−1.73pp deeper on U56,
   +1.07pp shallower on B136). That is noise on 50 events, not an effect.
4. **The verdict is a COST verdict, not a signal verdict.** Gross of costs the literal clause on
   v2 is a wash: **dSharpe −0.0015 at 0 bps**, −0.0564 at 10, −0.1389 at 25, with dMaxDD
   rung-invariant at +1.4 to +1.6pp. The monotone "the more it fires the worse it does" ordering
   (corr of dSharpe with log fire-rate) is **−0.14 at 0 bps and −0.75/−0.78 at 10/25 bps** — the
   ordering does not exist until you charge for it. Priced at zero, this clause reads as free
   insurance; that is exactly the mistake the 10 bps convention exists to prevent.
5. **Rule 8.** IS 2009-2016 argmax on both v2 panels is (x=0.05, c=3), the most inert corner of
   the grid. OOS 2017– it beats its control by +0.0066 (U56) / +0.0050 (B136) of Sharpe — but the
   whole-grid OOS mean on U56/v2 is **−0.0095, median −0.0003, positive 7/15**. The selector's
   "win" is it choosing to do almost nothing.
6. **KEEP paths: 4b 0 of 60 arms** (every arm lands at 6.4–8.7% CAGR against SPY's 10.63% floor).
   **4a 1 of 60** — U56/v2 x=0.05, c=3 (1.2085 / −11.94%, clearing at 0, 10 **and** 25 bps) —
   and it is a **32-event no-op**: 32 early sells in 17.7 years, dTurnover +0.00x/yr, dCAGR
   +0.02%, and it is the IS argmax, so rule 8 is not independent of it. Reported, not adopted.
   Filed as idea 506 (a minimum-activity clause for PROTOCOL's 4a).
7. **For the next Sunday review, a wording note only.** RULES v2 clause 6 currently justifies the
   removal as *"a daily exit would be an unpriced addition to the book."* That justification is
   now spent: it **is** priced, and it costs 0.056 of Sharpe and 0.97pp/yr. The clause should keep
   its conclusion and swap its reason, citing this run.
