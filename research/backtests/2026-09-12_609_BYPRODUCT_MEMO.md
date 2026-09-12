# 4b KEEP-CANDIDATE memo — B136 breadth-QROLL half-gate (POST-HOC by-product of idea 609)

1. **Status: POST-HOC. Not proposed for any Sunday review.** It is a by-product of idea 609, whose
   question was the twin ORDERING census, not a search for a book. PROTOCOL rule 6 is untouched;
   `RULES.md`, `scan.py`, `bot.py`, `baseline.py` are not modified by this run.
2. **Exact RULES wording, if it were ever adopted.** *Clause: hold every instrument that is above
   its 200-day moving average with vol20 < 0.60, equal-weighted, at 100% gross, rebalanced weekly.
   Each day, compute BREADTH = the share of priced instruments trading above their own 200-day
   moving average. If BREADTH is below its own trailing 252-trading-day 17th percentile, multiply
   every weight by 0.50 and hold the released half in CASH; never re-spread it. Weights decided at
   close t are applied at close t+1.*
3. **Two parameters only** (q = 0.17, w = 252), both on idea 602/605's published dial ladder; depth
   0.50, daily gate evaluation and gross 1.00 are reported axes of that same grid, not free dials.
4. **Headline, B136, 10 bps, next-day fill:** CAGR **13.29%**, Sharpe **1.134**, MaxDD **−15.19%**,
   halves **1.210 / 1.054**; OOS 2017+ **13.33% / 1.190 / −15.19%**.
5. **Comparands:** SPY 15.16% / 0.886 / −33.72% (OOS 15.33% / 0.877 / −33.72%); RULES v2 (live) OOS
   7.88% / 1.106 / −12.24%. It gives up **1.87 pp of CAGR to SPY and buys 18.5 pp of drawdown.**
6. **PROTOCOL 4b, every leg with its margin:** H1 +0.250, H2 +0.228, OOS +0.313, CAGR floor
   **+2.67 pp**, DD cap **+5.04 pp**. No leg is a knife edge. **4a FAILS** (as nearly every arm in
   this run does — 4a is 0 of 648 at 10 bps).
7. **Cost robustness: 4b passes at 0, 10 AND 25 bps** — CAGR margin +4.20 / +2.67 / +0.41 pp, DD
   margin +5.17 / +5.04 / +3.90 pp. It is not a 10-bps artefact.
8. **Earned, not inherited:** its own matched-gross twin — the same book holding 100% of the arm's
   mean gross with no timing — is 12.65% / **1.021** / −20.76% and **fails 4b at every rung**. The
   clause, not the exposure, carries the pass.
9. **Rule 8:** it **was** the IS pick for its (panel, family, gross, depth, cadence) cell chosen on
   IS Sharpe alone (1.0753), and its OOS was read once. **Transports to U56** (13.43% / 1.179 /
   −15.42%, OOS Sharpe 1.329, 4b passes). **Fails on SMALL** (6.51% / 0.514 / −29.94%), where no arm
   in this run passes 4b at any rung.
10. **Caveats before any capital.** SURVIVORSHIP: B136 is a current-constituent list, so the level
    is optimistic. The binding drawdown is 2020 on every panel, so this is one stress episode, not
    a distribution of them. The gate is evaluated daily against a rolling quantile of a breadth
    series computed on that same survivor panel. It is a near-neighbour of idea 604's committed
    U56 breadth-q0.17 candidate and idea 606's B136 CORR-HI candidate, so it is **not** independent
    evidence for that family — a third reading of one idea. Nothing here justifies real capital
    ahead of the ≥ 8 weeks of live tracking the 2026-09-03 recommendation memo already requires.
