# Memo — idea 376 by-product: breadth-SPEED cash gate (4b pass, PARKed not proposed)

1. **Cell.** SPEED40 gate, arming quantile q=0.10, depth 0.50, on equal-weight books, 10 bps.
2. **4b at 10 bps (full / H1 / H2 / OOS Sharpe, CAGR, MaxDD):** U56 EWALL 1.171 / 1.229 / 1.115
   / **1.197**, 12.1%, -18.8%; U56 TOP20 1.130 / 1.139 / 1.126 / **1.199**, 12.1%, -12.9%;
   B136 EWALL 1.188 / 1.284 / 1.090 / **1.191**, 12.9%, -15.6%. SPY: 0.889 / 0.957 / 0.834 /
   0.882, 15.2%, -33.7%. All three clear every 4b bar and beat their own ungated control OOS.
3. **Rule 8:** the IS(<=2016)-Sharpe chooser picks exactly this cell on those three books out of
   a 25-cell menu, so the pass is not an OOS-fitted one.
4. **Why it is PARKed, not proposed:** the LEVEL cell it was built to replace (q=0.20, depth
   0.50) clears 4b at 10 bps on **4** books, one more than this one, with a higher OOS Sharpe on
   U56 EWALL (1.295 vs 1.197). The idea's own hypothesis loses its head-to-head.
5. **Exchange rate:** median dDD per pp of CAGR given up is 0.79 for SPEED40 against 1.19 for
   LEVEL and a free-numeraire bar of 1.72 — the gate is a worse way to buy drawdown than simply
   holding less gross (idea 351's clause).
6. **Footprint:** 3 of 18 books, 2 of 3 panels, and 0 of 6 book forms outside equal-weight
   constructions (EWALL, TOP20). SMALL439 fails every bar at every setting.
7. **Cost sensitivity:** survives to 25 bps only on B136 EWALL; U56 EWALL fails the DD bar and
   U56 TOP20 the H1/CAGR bars at 25 bps.
8. **RULES wording, exact, if a Sunday review ever revives it:** *"Clause N (breadth-speed
   exposure gate). Let E_t be the share of priced universe members trading above their own 200d
   moving average, SPY excluded. Let S_t = E_t - mean(E_{t-39..t}). If S_{t-1} is below the
   causal expanding 10th percentile of S computed from data up to t-1 (minimum 252
   observations), hold 50% of the book's normal gross and the remainder in cash from the next
   rebalance; otherwise hold normal gross. Weekly cadence, next-day execution."*
9. **Do not adopt without:** a panel outside the two that produced it, a survivorship-clean
   drawdown level, and a re-read against the LEVEL cell at matched realised armed-day frequency
   (this run matches the target quantile, not the realised 0.095-vs-0.080 frequency).
10. **Status: PARK.** Script `2026-09-07_does-a-DRAWDOWN-SPEED-signal-beat-a-breadth-LEVEL-signal_C.py`;
    grid, windows and walk-forward CSVs committed beside it.
