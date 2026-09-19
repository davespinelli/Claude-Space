# KEEP-4b memo — U56 two-state gross on SPY's 100d MA (idea 1562, lane cloud, 2026-09-19)

1. **Path.** 4b only (capital-worthy).  4a fails 0 of 144 cells: the live book is shallower.
2. **Book (rule-8 reachable; BOTH legal IS-only choosers pick it on U56 from IS rows alone).**
   U56 panel, frozen incumbent frame (N = 20, min-hold H = 126, per-name 200d MA gate, MAXVOL
   0.60, equal weight, weekly, t+1), gross **0.75 when SPY closed above its own 100-day MA on the
   prior bar, 0.5625 otherwise**; de-gross goes to cash at 0%, never re-spread, never levered.
3. **Full sample @10 bps** 14.65% / **1.1817** / -16.54%, halves 1.2289 / 1.1508.
   **OOS (2017-01-03..2026-09-18, read once)** 16.15% / **1.2247** / -16.54%.
4. **4b legs, FULL:** H1 1.2289 > SPY 0.957; H2 1.1508 > 0.825; MaxDD -16.54% >= -20.23% (cap);
   CAGR 14.65% >= 10.59% (floor).  **OOS:** Sharpe 1.2247 > SPY 0.8738; MaxDD and CAGR clear.
5. **Against the frozen 2026-09-04 anchor** (15.80% / 1.1537 / -19.13%; OOS 17.32% / 1.1857):
   +0.0280 Sharpe full (**t +0.97**), +0.0390 OOS, -1.15 pp of CAGR, **+2.59 pp of MaxDD**.
6. **Against its own CAGR-matched constant de-gross twin (g\* = 0.6958)** — the comparand this
   memo exists to disclose: +0.0281 Sharpe full (**t +0.97**), +0.0393 OOS (**t +0.94**),
   +1.29 pp of MaxDD.  **The margin is inside one paired-bootstrap SE.  It is not resolved.**
7. **Cost ladder 0/10/25/50 bps:** 1.2092 / 1.1817 / 1.1402 / 1.0710 Sharpe, 4b PASS full and OOS
   at every rung; the margin over the twin decays +0.0344 / +0.0281 / +0.0188 / +0.0033.
8. **Lag:** reading the SPY signal 2 days late gives 1.2042, 5 days late **1.1698** — below the
   anchor's own 1.1537 by only +0.016.  The device is a 1-to-2-day object.
9. **RULES wording, exact, if a Sunday review ever enacts it:** *"Clause 3 (EXPOSURE STATE).  At
   each weekly rebalance, if SPY's prior close is above its own trailing 100-day simple moving
   average, hold each selected name at 0.75/N of NAV; otherwise hold each at 0.5625/N.  The
   difference is held as cash and is never re-spread across the remaining names."*
10. **Recommendation: DO NOT ENACT.**  Survivorship (U56 is a current-constituent list) makes the
    level an upper bound; the edge over a plain constant de-gross is +0.028 of Sharpe at t < 1,
    dies at 50 bps and at a 5-day signal lag, and does not replicate on SMALL (7 of 12 cells).
    Filed as a candidate so the record carries it, not as a proposal.
