# 1084 — U56 / N=12 / H=126: a 4b PASS that dominates the incumbent and rule 8 cannot reach. PARK.

1. The cell: U56, CAND20 composite, no vol scaler, above-200d & 20d-vol < 0.60 eligibility, N=12 slots,
   min hold H=126, gross 0.75, weekly, 10 bps, t+1. Full sample CAGR **17.69%**, Sharpe **1.1686**,
   MaxDD **-20.17%**, halves 1.274 / 1.088, OOS(2017-) CAGR 18.87% / Sharpe 1.1748 / MaxDD -20.17%.
   All five 4b legs clear against SPY (15.13% / 0.8848 / -33.72%).
2. Exact RULES wording if it were ever adopted:
   "Universe U56. Score = mean percentile rank of 12-1, 6m and 3m returns, halved for names at or
   below their own 200d MA; no volatility scaler. Eligible = above own 200d MA and 20d realised vol
   < 0.60. Hold the top 12 eligible names, equal weight 0.75/12 of NAV, gated weight to CASH.
   Rebalance on the last trading day of each week, executing at the next close. A name entering the
   book must be held at least 126 trading days before it can be displaced."
3. The only change from the standing 2026-09-04 KEEP 4b book is N: 20 -> 12. Nothing else moves.
4. It DOMINATES the incumbent on every axis the record prices: +2.07 pp of CAGR, +0.026 of full
   Sharpe, +0.006 of OOS Sharpe, at 3.04 against 2.90 turns per year (+0.14, i.e. +1.4 bp/yr at
   10 bps). Its drawdown is 1.04 pp deeper (-20.17% vs -19.13%).
5. WHY IT IS PARK AND NOT KEEP (protocol rule 8): no IS-only chooser reaches it. C_ISEDGE picks N=5,
   C_ISCAGR picks N=5, C_ISSHARPE picks N=40 — N=12 is IS-Sharpe rank 2 of 9, behind N=40 by 0.0101.
   At H=63 one chooser at one split picks N=12; at H=126, none of nine decisions does.
6. The DD leg is decided inside a hair: -20.169% against the cap -20.2304% is a margin of **0.061 pp**,
   which is 1259's complaint about publishable precision. Two extra tape rows of a bad week would
   flip it, and G4 in this run shows U56's own cache moves history by up to 5e-05 relative.
7. Its 4a verdict FAILS (A_H2, A_DD) against live RULES v2, as every growth book on this panel does.
8. Not re-scored at 25/50 bps, on a delayed-execution variant, or on a survivorship-free panel. All
   three are prerequisites before any capital conversation, and the turnover gap makes the first cheap.
9. RECOMMENDATION: **PARK**. Log the cell, do not enact it (rule 6), and do not quote it as a KEEP:
   a full-sample pass that no honest in-sample procedure selects is a description of this tape.
10. SURVIVORSHIP (rule 9): U56 is a current-constituent list, so 17.69% and -20.17% are both
    optimistic, and the leg this cell clears by 0.061 pp is the leg survivorship flatters most.
