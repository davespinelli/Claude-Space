# Memo — U56 CADENCE Q cell: 4b PASSER, PARKED (not KEEP), 2026-09-16, idea 1099, lane C

1. **STATUS: PARK, not KEEP.** The cell clears PROTOCOL 4b full AND OOS at 10 bps, but no honest
   IS-only chooser reaches it at the protocol's own penalty rung, so rule 8 forbids calling it KEEP.
2. **NUMBERS (U56, 10 bps, 2009-2026):** full 15.40% / Sharpe 1.1388 / MaxDD -19.94%, halves
   1.2214 / 1.0911; OOS 2017-2026 17.28% / 1.1726 / -19.94%; turnover 1.65x/yr, 71 rebalances.
3. **AGAINST SPY (the 4b bar):** SPY full 15.10% / 0.8829 / -33.72% (halves 0.9588 / 0.8207), OOS
   15.21% / 0.8711. All five 4b legs pass full, all three pass OOS, at 0, 10, 25 and 50 bps.
4. **AGAINST THE INCUMBENT W BOOK:** OOS Sharpe 1.1726 vs 1.1643 (+0.0083) at 1.65x/yr turnover
   against 2.90x. The gain is real in sign and an order of magnitude below 877's 0.0145 seed floor.
5. **WHY IT IS PARKED:** at LAM = 10 bps the IS-Sharpe-net-of-turnover chooser prefers W by
   +0.0002, and LAM*(Q) = 11 bps on C4, 76 bps on C9, 107 bps on B136/C4, never on B136/C9.
6. **RULES WORDING, EXACT, IF A SUNDAY REVIEW EVER PROMOTES IT (not proposed here):** *"Rebalance
   on the last trading day of each calendar quarter. Hold the top 20 names of the CAND20 composite
   (mean percentile rank of 21d-skip-252d, 126d and 63d returns, halved for names at or below their
   200d MA) among names above their 200d MA with 20d annualised vol below 0.60, at 0.75 / 20 of NAV
   each, cash otherwise. A name held fewer than 126 trading days is retained regardless of rank.
   Weights decided at the close are applied the next day."*
7. **WHAT WOULD HAVE TO BE TRUE TO PROMOTE IT:** a chooser declared in advance, independent of this
   result, that prefers Q at a penalty no larger than the cost the protocol charges — which on this
   tape means resolving a 0.0002 IS-Sharpe gap the record cannot resolve.
8. **DO NOT PROMOTE IT AS A TURNOVER SAVING EITHER:** the 1.25x/yr of turnover saved is worth
   ~1.25 bps/yr at 10 bps, well inside the halves-Sharpe noise that decides its own 4b legs.
9. **SURVIVORSHIP (rule 9):** U56 is a current-constituent list; every figure above is an upper
   bound, and the cell's B136 twin fails 4b at all four cost rungs.
10. **NOTHING PROPOSED AS CAPITAL. No RULES change, no PROTOCOL edit; rule 6 unchanged.**
