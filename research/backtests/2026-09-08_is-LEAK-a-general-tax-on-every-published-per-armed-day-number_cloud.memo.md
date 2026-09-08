# MEMO — 4b KEEP-candidate by-product of idea 248 (cloud, 2026-09-08). **PARK-recommended, NOT adopted.**

1. **Object.** u56 panel, EWall base book, a `vol60-dg` de-grossing overlay ARMED only when
   cross-sectional breadth sits in its own expanding bottom-20th-percentile (3y warm-up).
2. **Provenance.** Chosen on IS Sharpe alone over 2009-01-13..2016-12-31 from a 48-point
   (instrument × arming-rate) menu; 2017-01-01..2026-09-04 read once. Rule-8 clean.
3. **Numbers, 10 bps, weekly, t+1:** CAGR **12.85%**, Sharpe **1.158**, MaxDD **−18.1%**,
   halves **1.199 / 1.119**; OOS CAGR 13.00%, OOS Sharpe **1.193**, OOS MaxDD −18.1%.
   At 25 bps: 12.67% / 1.144 / −18.1%, OOS 1.176. SPY 15.23% / 0.889 / −33.7%, OOS 0.882.
4. **4b arithmetic.** Beats SPY in both halves and OOS; MaxDD 18.1% ≤ the 20.23% cap
   (0.60 × SPY); CAGR 12.85% ≥ the 10.66% floor (0.70 × SPY). PASSES at both cost rungs.
5. **What the overlay buys.** Its own un-overlaid control is 13.27% / 1.124 / **−22.5%** and
   FAILS 4b on drawdown alone; the overlay pays 0.4 pp of CAGR for 4.4 pp of MaxDD.
6. **4a: FAILS** against the live RULES v2 book (0 of 882 rows in this grid pass 4a vs v2) and
   against RULES v1. It also loses to RULES v2 on OOS Sharpe, 1.193 vs 1.285.
7. **PARK reason 1 — coverage asymmetry.** The gate arms **3.1% of in-sample days against
   13.2% out-of-sample**. The out-of-sample result is priced on 4× the arming the choice was
   made on; this is the defect that PARKed idea 247's arm and it is not fixed here.
8. **PARK reason 2 — the chooser.** Over the other 17 (panel × book × cost) cells the same
   IS-Sharpe selector beats its own do-nothing control in 5/18 and has median OOS Sharpe 0.627
   against the control's 0.760. This cell is the good draw from a bad chooser.
9. **PARK reason 3 — panel.** 4b passes are 65 on u56 and 29 on broad, **0 on small439**;
   nothing here transfers to the small panel. SURVIVORSHIP: small439 is current constituents of
   a sub-$2B screen only, tickers with max_1d_move ≥ 1.0 dropped.
10. **RULES wording IF a future Sunday review ever adopts it** (not proposed today):
    *"Clause N — breadth-armed volatility de-grossing. Base book: hold every name priced that
    day at 75%/N of NAV (N = names priced), rebalanced weekly. Compute cross-sectional breadth
    as the share of priced names trading above their own 200-day mean. On any day where
    breadth is at or below its expanding 20th percentile (minimum 756 prior observations),
    set to ZERO the weight of every name whose 20-day realised volatility is at or above 60%
    annualised and send that weight to CASH — never re-spread it. On all other days hold the
    base weights unchanged. Weights are decided at close t and applied at t+1."*
    (The regime is read at the close before the rebalance; the gate is a per-name eligibility
    mask, not a portfolio-level scalar.)
