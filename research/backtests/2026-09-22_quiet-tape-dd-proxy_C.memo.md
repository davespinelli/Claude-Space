# MEMO — KEEP-4b candidate (idea 2083, 2026-09-22, lane C)

1. CANDIDATE: U56 panel, MADIST top-40 equal-weight (rank by close/200dMA − 1), gross 1.00/40 per
   name, MONTHLY trade, fills t+1, 10 bps. Reached by the EX-ANTE QUIET-TAPE chooser at q = 0.40.
2. PATH: 4b (capital-worthy). 4a FAILS — FULL MaxDD −17.67% is worse than live RULES v2's −12.05%
   and H1 1.1834 is below the live book's 1.2276. Nothing here challenges the live book on 4a.
3. FULL 14.57% / 1.1965 / −17.67% (halves 1.1834 / 1.2098); IS 12.58% / 1.0567 / −12.70%;
   OOS 16.24% / 1.3099 / −17.67%.
4. SPY FULL 15.14% / 0.8851 / −33.72% (halves 0.9570 / 0.8264), OOS 15.29% / 0.8751 / −33.72%.
   All seven 4b legs clear: both halves and OOS Sharpe above SPY; MaxDD −17.67% inside the
   −20.23% cap FULL and OOS; CAGR 14.57% / 16.24% above the 10.60% / 10.70% floors.
5. LEGAL IS-only chooser: across the 80-book shelf, regress each book's 2009–2016 drawdown ON
   QUIET DAYS ONLY on its 2009–2016 SPY beta, take the largest positive residual. Quiet = SPY
   within 0.91% of its running high (the 40th percentile of that distance over 2009–2016). Both
   near-high definitions (expanding high, 252-day high) pick this book. 2017–2026 read once.
6. ROBUST: 4b holds at ALL 16 cells of cost {0,10,25,50} bps × signal lag {0,+1 day}; OOS Sharpe
   1.336→1.202 across the cost ladder. Turnover 3.09x/yr vs live 1.77x — it does NOT die above
   10 bps, unlike the 2026-09-20 review's 8.18x candidate. A +1-day lag spends 1.9 of the 2.56 pp
   drawdown margin (OOS MaxDD −19.61% at 10 bps), so the margin is thin but not a knife edge.
7. NOT ROBUST ACROSS PANELS OR DIALS: 3 of 93 grid points clear, ALL U56 (B136 misses the DD leg
   by 7.96–10.50 pp, SMALL665 by 15–28 pp); only 3 of 24 U56 q<1.00 points clear, and two of those
   are the same cell via two interchangeable definitions. The (definition, q) pair is a tuned
   choice a deployment must fix in advance. No bootstrap CI was run on the margin (cf. idea 2042).
8. EXACT RULES WORDING (were this proposed at a Sunday review — NOT proposed here):
     "On the last trading day of each month, rank every U56 name whose close is above its 200-day
      moving average and whose 20-day annualised realised vol is below 0.60 by (close / 200-day
      moving average − 1), descending. Hold the top 40 at 2.5% of NAV each; if fewer than 40 names
      qualify, hold only those that do and leave the remainder in CASH (never re-spread, never
      lever). Hold the positions unchanged between month-ends. Weights decided at close t apply at
      t+1. Costs 10 bps per unit turnover."
9. SURVIVORSHIP: U56 is a CURRENT-constituent 56-name list. LEVELS are optimistic and the 4b bar
   is easier here than on a point-in-time panel; treat CAGR and MaxDD as upper bounds. The
   chooser CONTRAST is same-tape and first-order immune; the 3-of-93 pass count is not.
10. RELATION TO RECORD: this is idea 911's shelf and 911's chooser with one substitution — the
    drawdown statistic is taken on an EX-ANTE causal quiet-tape mask instead of a hindsight crash
    calendar — and that substitution alone converts 911's 0-of-3 (best pick −22.18%, a 1.95 pp
    miss) into a pass. Top-40-of-56 is a plain book, so its 4b pass may be mostly the 200d-MA
    gate; against the standing 1795 candidate (OOS 15.40% / 1.357 / −15.90%) it carries more OOS
    CAGR, less OOS Sharpe and a deeper drawdown, and is a DIFFERENT family (ranked MA-distance
    rather than a vol-target scalar), so the two are comparands, not versions of one book.
    INDEPENDENT CONVERGENCE (found on the rebase, not by design): lane cloud's idea 2079 reached
    the SAME panel/family/width/cadence cell at the adjacent gross rung 0.75 (OOS 12.08% / 1.308 /
    -13.55%) via a different chooser. OOS Sharpe 1.308 vs 1.3099. It parked at 0.75 because the
    FULL CAGR margin there is 0.26 pp; at gross 1.00 that margin is 3.97 pp and the drawdown is
    still inside the cap. The GROSS RUNG is therefore the live question, and the two runs bracket
    it — which is the first thing a Sunday review should price.
