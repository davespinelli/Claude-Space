# MEMO — KEEP-4b candidate (idea 1795, 2026-09-22, lane cloud)

1. CANDIDATE: U56 panel, equal-weight, vol-target exposure scalar g = clip(0.12/σ20, 0, 1),
   gross capped at 1.00, MONTHLY trade cadence, refresh under a TURNOVER BUDGET B = 5.0 turns/yr.
2. PATH: 4b (capital-worthy). 4a FAILS — DD −15.9% is worse than live RULES v2's −12.05%.
3. FULL 14.07% / 1.251 / −15.90%; IS 12.48% / 1.122 / −13.10%; OOS 15.40% / 1.357 / −15.90%.
4. SPY OOS 15.29% / 0.875 / −33.72% — candidate beats SPY on Sharpe in both halves, OOS, and full;
   CAGR ≥ 70% of SPY; MaxDD ≤ 60% of SPY's (−15.9% vs −33.7%). All four 4b legs clear.
5. Reached by a LEGAL IS-only chooser (IS_LEGS: maximise 2009–2016 4b-leg count, ties on IS Sharpe)
   — the pick is made on 2009–2016 only; 2017–2026 read exactly once.
6. ROBUST: 4b holds at 0/10/25/50 bps; survives t+2 execution lag; holds at both budget neighbours
   (B=3.0, ∞) and both target neighbours (t=0.10, 0.16). Not a knife edge.
7. σ convention FIXED (L=20, d=0); budget accounting window 252d; B=∞ reproduces daily refresh.
8. EXACT RULES WORDING (were this proposed at a Sunday review — NOT proposed here):
     "Hold the U56 equal-weight panel at gross g_t = min(1, 0.12 / σ20_t), where σ20_t is the
      annualised 20-day realised vol of the equal-weight panel through close t. Re-scale to g_t
      whenever the held gross has drifted from g_t, but execute a re-scale only while trailing
      252-day realised turnover plus the re-scale's own turnover stays at or below 5.0. Trade
      (re-spread names) monthly; a monthly re-spread always executes and is charged to the budget.
      Weights decided at close t apply at t+1. Costs 10 bps/unit turnover."
9. SURVIVORSHIP: U56 is a CURRENT-constituent list. LEVELS are optimistic; the 4b bar is easier
   here than on a point-in-time panel. Treat CAGR/DD as upper bounds.
10. RELATION TO RECORD: same VOLTGT/fresh-scalar object as ideas 1789/1793 (daily refresh is the
    4b-clearing one); the new content is that a TURNOVER BUDGET reaches it with a legal IS-only
    chooser at a MONTHLY trade cadence, and that idea 1795's own premise (stale = saved cost) is
    FALSIFIED — the stale preference is a gross-return fact (turnover share of gap median 0.148).
