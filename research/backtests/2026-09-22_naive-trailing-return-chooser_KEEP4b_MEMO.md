# KEEP-candidate memo (path 4b) — idea 1779, lane C, 2026-09-22 — **RECORDED, NOT RECOMMENDED**

1. **Object.** The live band book (RULES v2 clause 2, c = 0.03, gross 0.75, weekly, t+1, 10 bps)
   on a 20-name subset of U56 chosen by a **zero-backtest** IS-only statistic: the mean 2009–2016
   total return of the draw's own names. Script
   `research/backtests/2026-09-22_name-set-chooser-vs-trailing-return_C.py`; 3,840 cells in
   `.grid.csv.gz`, 720 decile rows in `.decile.csv`, 72 rule-8 picks in `.rule8.csv`.
2. **Why it is a candidate at all.** Under rule 8 (both dials — control statistic and decile
   width — fixed on 2009–2016 only, 2017–2026 read once) the naive chooser clears 4b FULL *and*
   OOS at **14 of 20 picks**, against 13 of 16 for idea 1749's four book statistics. At D = 480 it
   picks **draw 364**, a strictly better 4b cell than 1749's standing candidate.
3. **The headline book (D = 480, S = `NAIVE_MEANRET`, draw 364).** FULL 12.36% / **1.3120** /
   **−15.33%**, halves **1.4273 / 1.2158**. OOS 2017–2026 **12.90% / 1.3088 / −15.33%**. SPY FULL
   15.14% / 0.8851 / −33.72%, OOS 15.29% / 0.8751 / −33.72%. Live RULES v2 FULL 8.62% / 1.2010 /
   −12.05%, OOS 9.46% / 1.2767 / −12.05%. Turnover 1.83 /yr.
4. **4b legs, all five, with margins.** H1 +0.4702, H2 +0.3894, OOS Sharpe +0.4337; MaxDD −15.33%
   against the −20.23% cap (**+4.90 pp**); CAGR 12.36% against the 10.60% floor (**+1.77 pp**) and
   OOS 12.90% against 10.70% (**+2.20 pp**). Every margin on the CAGR leg is **wider** than 1749's
   draw 166 (+1.15 / +1.04 pp); its DD margin is narrower (+4.90 vs +7.07 pp).
5. **Cost.** Reconstructed exactly off the cost-0 leg (G2, 3.1e-17). Draw 364 clears 4b FULL and
   OOS at **0, 10, 25 and 50 bps** (OOS 13.10% / 1.3278 → 12.07% / 1.2326).
6. **Path 4a is NOT met and is not claimed.** 0 of 20 naive picks clear 4a FULL; 3 of 20 clear 4a
   OOS. Beating the live low-return book in both halves is the one target this chooser cannot
   find — the book statistics reach it at 2 of 16.
7. **WHY THIS MEMO RECOMMENDS AGAINST ITSELF.** The run that produced this cell exists to test
   whether 1749's chooser carries book information, and the answer is that it largely does not:
   ρ(`NAIVE_MEANRET`, `IS_CAGRSLACK`) = **+0.896** over 480 draws, the naive control matches or
   beats the best book statistic at 20 of 32 (D, q, target) cells on U56 and 23 of 32 on B136, and
   at D = 24/96/240 it picks the *identical* draw. A rule whose entire selection content is "hold
   the 20 names on a current-constituent list that rose most in 2009–2016" is a **survivorship
   screen**, not a strategy. Its OOS margin is the bias, measured.
8. **Survivorship (PROTOCOL rule 9), first-order and decisive here.** U56 is a CURRENT-constituent
   list; draw 364 is a 35.7% cut of it selected to maximise realised 2009–2016 return. The
   +2.20 pp OOS CAGR margin is smaller than any plausible point-in-time haircut. Treat the pass as
   an upper bound and nothing more.
9. **Exact RULES wording, if it were ever adopted (it should not be without a point-in-time
   vintage).** *"Clause 2a (name set). Trade only these 20 U56 tickers, fixed once on 2009–2016
   data and never re-chosen: AMD, AMZN, AVGO, CRM, DIA, HYG, IWM, LQD, NFLX, NVDA, PLTR, SPY,
   TSLA, UUP, VTI, XBI, XLC, XLI, XLU, XOM. Clause 2b (gate). Hold every one of those 20 names
   whose close is inside the 200-day moving-average band (IN above ma × 1.03, OUT below
   ma × 0.97, previous state in between, OUT before 200 closes exist) at 0.75 / N of NAV, N = the
   number of the 20 priced that day; gated-out weight goes to cash and is never re-spread.
   Clause 2c (cadence). Rebalance weekly, decide at the close of t, execute at t+1, 10 bps per
   unit turnover. No shorting, no leverage."*
10. **What would kill it — and what already has.** (a) A point-in-time U56 vintage; §7 is the
    reason to expect it to fail one. (b) Panel: **0 of 36** rule-8 picks on B136 clear 4b BOTH, by
    either kind, so nothing here travels off U56. (c) It is already killed as an *information*
    claim: this memo exists so the record carries the cell and the reason not to fund it in the
    same file. **Not proposed for the Sunday review.**
