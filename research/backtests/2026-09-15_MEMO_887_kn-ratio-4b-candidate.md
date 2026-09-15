# MEMO — idea 887, 4b KEEP-candidate: the k/n-RATIO book on U56 (cloud, 2026-09-15)

1. **The book.** U56 (`research/universe.json`), monthly, fills t+1, 10 bps, cash never respread.
   Signal = `baseline.score(px, vol_scale=True)` (RULES v1's composite, **with** the vol scaler).
   Gate = close > 200d MA AND vol20 < 0.60. Width is a RATIO of eligible breadth, not a fixed k.
2. **Exact RULES wording, if a Sunday review adopts it.**
   *"Each month end, score every instrument by the mean of the cross-sectional percentile ranks of
   (t−21/t−252 − 1), (t/t−126 − 1) and (t/t−63 − 1), multiplied by 1.0 if the close is above its
   200-day mean and 0.5 if not, divided by the square root of its 20-day annualised volatility
   floored at 0.08. An instrument is ELIGIBLE if its close is above its 200-day mean and its
   20-day annualised volatility is below 0.60. Hold the top k eligible names by score at GROSS/k
   of NAV each, where k = min(max(5, round(0.35 × n_eligible)), n_eligible). Any shortfall stays
   in CASH and is never respread. Rebalance monthly, fill next day."*
3. **GROSS is the open decision.** g = 1.00 is what the IS-only selector picks; g = 0.75 is what
   survives every stress below. A Sunday review should take **g = 0.75**, not 1.00 — see line 7.
4. **Full sample (2009-01-13..2026-09-14), 10 bps.** g=1.00: CAGR **15.7%**, Sharpe **1.152**,
   MaxDD **−16.9%**, halves 1.251 / 1.071. g=0.75: **11.7% / 1.150 / −12.9%**, halves 1.249 / 1.070.
   SPY: 15.13% / 0.885 / −33.72% (halves 0.959 / 0.824). RULES v2 live: 8.62% / 1.201 / −12.05%.
5. **PROTOCOL 4b, full sample.** Sharpe > SPY in both halves ✓✓; MaxDD ≤ −20.23% ✓ (−16.9%);
   CAGR ≥ 10.59% ✓ (15.7%). **PASS.** Path **4a FAILS** — 0 of 576 cells in this run beat the live
   book's −12.05% MaxDD, this one included.
6. **PROTOCOL rule 8 (params on 2009–2016 only, OOS read once).** All three declared IS-only
   selectors — PICK-SHARPE, PICK-CALMAR and PICK-4bIS — land on this same cell. OOS 2017-01-01..:
   **16.1% / 1.136 / −16.9%** against SPY OOS 15.27% / 0.874 / −33.72%; OOS bars DD cap −20.23%,
   CAGR floor 10.69%. **4b PASS out of sample.** At 25 bps: 14.0% / 1.045 / −17.1%, still PASS.
7. **THE FRAGILITY, stated up front.** One FURTHER day of execution delay moves g=1.00's MaxDD
   **−4.51 pp to −21.37%**, through the cap: **4b FAILS under DELAY1 at g = 1.00.** At g = 0.75 the
   same width reads −16.42% delayed and **PASSES**; r = 0.50 / g = 0.75 passes too. The IS-Sharpe
   selector prefers g=1.00 over g=0.75 by 0.002 of Sharpe, so the rung it picks is the fragile one.
8. **Not a knife edge in width.** r = 0.35 and r = 0.50 (k_med 14 and 20) both clear 4b full-sample
   and OOS at 10 **and** 25 bps. r ≥ 0.75 fails the DD cap; r ≤ 0.20 fails OOS. Turnover is high:
   **9.6x/yr** at r=0.35, 8.0x at r=0.50 — the 25 bps rung is the one that matters here.
9. **SURVIVORSHIP.** `universe.json` is the CURRENT constituent list, so every level above is
   optimistic and both 4b bars are easier than on a point-in-time panel. SPY is a listed
   constituent and this book can hold it. 2020 and 2022 are the only stress episodes in the window.
10. **Rule 6.** This is not a rules change. It is a candidate for a Sunday review, at g = 0.75.
