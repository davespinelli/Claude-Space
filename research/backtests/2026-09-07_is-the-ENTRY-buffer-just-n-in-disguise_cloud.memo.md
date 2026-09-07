# Memo — idea 357 by-product, 4b PASS on U56, **PARK-recommended** (not proposed for RULES)

1. **RULES wording, exact.** *Universe:* research/universe.json (U56). *Eligible:* priced today,
   close above its 200-day moving average, 20-day annualised vol < 0.60. *Rank:* the RULES v1
   composite (mean of the percentile ranks of 12-1 momentum, 6-month and 3-month return, halved
   when below the 200d MA) **with the vol scaler OFF**. *Slots:* k_t = the number of eligible
   names at rank <= 20 on the rebalance day. *Hold:* keep a held name while its rank <= 20; sell
   it the first rebalance its rank passes 20 or it leaves the eligible set. *Buy:* fill free
   slots from the best-ranked names **at rank <= 12** that are not already held; if fewer than
   k_t such names exist, hold fewer. *Weights:* 0.75/k of NAV each, remainder cash. *Cadence:*
   weekly, decided at Friday's close, executed at the next close.
2. Two tuned parameters only: n = 20 and e = 8 (enter at rank <= n-e).
3. **10 bps, 2009-01-13 to 2026-09-04:** CAGR 13.77%, Sharpe 1.060, MaxDD -19.23%, turnover
   8.25x NAV/yr, 14.83 names/day.
4. **Halves:** 1.096 / 1.038 vs SPY 0.957 / 0.834. **OOS (2017-2026, rule 8):** Sharpe 1.104,
   CAGR 15.33%, MaxDD -19.23% vs SPY 0.882.
5. **4b PASS at 0, 10 and 25 bps.** Margins @10 bps: H1 +0.139, H2 +0.204, OOS +0.222,
   DD +1.00pp, CAGR +3.11pp. Breakeven **c\* = 30 bps**, first failing bar H1.
6. **4a FAIL** at every rung (H1 -0.130, H2 -0.153, DD -7.18pp vs RULES v2's -12.05%).
7. **Why PARK, not KEEP.** Fails 4b on B136 and SMALL439 at every rung; it is not the rule-8
   pick on any of the three menus (the BUFFER-ONLY chooser takes e=16, the UNION chooser takes
   HARD n'=4), so its OOS number is read with hindsight.
8. **And why it is not new.** It sits inside idea 349's already-PARKed entry-buffer family; that
   run's standing cell (e=16, x=40) has a higher c\* (60 bps) and a higher Sharpe (1.164).
9. **What idea 357 adds about it:** at matched holdings, 59% of this cell's edge over a plain
   top-15 cut at 10 bps — and 78% at 25 bps — is the turnover differential (8.25 vs 12.32x/yr),
   not return. It is a cheap book, not a better-selecting one.
10. **SURVIVORSHIP:** U56 is a current-constituent list; a 14.8-name momentum book on such a
    list is flattered. Research, not investment advice.
