# MEMO — KEEP-4b candidate reached by a LEGAL rule-8 chooser (idea 2094, 2026-09-22, lane C)

1. CANDIDATE: U56 panel, gate close>200dMA & vol20<0.60, **ALPHABETICAL top-30** at 1/30 of NAV
   each (shortfall in CASH), MONTHLY trade, fills t+1, 10 bps. Reached by the rule-8 IS-Sharpe
   chooser over 25 (ranking, k) cells; 2017–2026 read once. It uses NO return-based ranking.
2. PATH: 4b only. 4a FAILS — FULL MaxDD −18.56% is worse than live RULES v2's −12.05%. Nothing
   here challenges the live book on 4a.
3. FULL 15.99% / 1.2233 / −18.56% (halves 1.2401 / 1.2119); IS 14.07% / 1.1258 / −12.71%;
   OOS 17.59% / 1.2996 / −18.56% (DD margin +1.67 pp over the −20.23% cap).
4. SPY FULL 15.14% / 0.8851 / −33.72% (halves 0.9570 / 0.8264); SPY OOS 15.29% / 0.8751 /
   −33.72%. All seven 4b legs clear on FULL and OOS; CAGR floors 10.60% / 10.70%.
5. WHY IT IS FILED HERE AND NOT PROPOSED: its sibling ALPHA k=40 (OOS 15.92% / 1.3266 / −16.60%,
   +3.63 pp) and MADIST k=50 / ALPHA k=50 (13.2% / 1.293 / −15.48%, +4.75 pp, identical across
   all five rankings to 4dp) both dominate it on the drawdown leg, so the WIDTH is an unresolved
   dial, not a settled one. Two cells of the same shelf disagree about where to sit.
6. ROBUST: at k=40 every ranking clears 4b at 8 of 8 cost {0,10,25,50} bps × lag {0,+1d} cells;
   at k=30 the 4b pass rate across rankings is 0.92. The pass is NOT a ≤10 bps object.
7. NOT ROBUST ACROSS WIDTH: 4b pass rate by k = 0.00 / 0.92 / 1.00 / 1.00 / 0.00 for
   k = 20/30/40/50/ALL. k=20 is too concentrated and k=ALL re-spreads to full gross; both fail
   the DD leg. A deployment must fix k in advance, and only the interior rungs work.
8. EXACT RULES WORDING (were this proposed at a Sunday review — NOT proposed here):
     "On the last trading day of each month, list every U56 name whose close is above its 200-day
      moving average and whose 20-day annualised realised vol is below 0.60. Sort that list
      alphabetically by ticker and hold the first 30 at 3.333% of NAV each; if fewer than 30
      names qualify, hold only those that do and leave the remainder in CASH (never re-spread,
      never lever). Hold the positions unchanged between month-ends. Weights decided at close t
      apply at t+1. Costs 10 bps per unit turnover."
9. SURVIVORSHIP: U56 is a CURRENT-constituent 56-name list, so CAGR and MaxDD are upper bounds
   and the 4b bars are easier here than on a point-in-time panel. An ALPHABETICAL selector is
   also the construction most exposed to that bias: it holds a fixed, hand-picked slice of names
   already known to have survived. Treat the levels as indicative only.
10. RELATION TO RECORD: this run's real content is the KILL beside it — MADIST's ordering earns
    none of idea 2083's +2.56 pp margin (it is the SMALLEST of the five at k=40; MADIST − ALPHA
    OOS dSharpe is −0.0166, 95% [−0.0708, +0.0363]) and even the REVERSED ranking clears 4b.
    The earning device is the 200d-MA gate plus the FIXED-DENOMINATOR cash buffer, i.e. the
    de-gross the CHANGELOG already credits elsewhere. Against the standing 1795 candidate
    (OOS 15.40% / 1.357 / −15.90%) this carries more OOS CAGR, less OOS Sharpe and a deeper
    drawdown. The Sunday review question is now the WIDTH/GROSS rung on a plain gated book, not
    which ranking sits inside it — 2083 and 2079 already bracketed the gross rung, and this run
    shows the ranking axis is empty.
