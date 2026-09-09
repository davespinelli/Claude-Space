# MEMO — idea 317's 4b passer: `EWALL|LOWVOL20@CALM70` on U56 (2026-09-09, cloud). **PARK, not KEEP.**

1. **Status.** Passes PROTOCOL path **4b** on a genuine rule-8 selection (pair+state chosen on 2010–2016
   by IS Sharpe, 2017–2026 read once). Fails **4a**. Recommended disposition: **PARK** — it fails idea 48's
   parents bar on CAGR and MaxDD, and its only win over both parents is the generic mixing gain.
2. **Numbers (U56, 10 bps, weekly, next-day, gross 0.75).** Full 11.51% / Sharpe 1.210 / MaxDD -17.79%,
   H1 1.294, H2 1.126; **OOS 11.20% / 1.224 / -17.79%**. SPY 15.19% / 0.887 / -33.72% (H1 0.959, H2 0.829;
   OOS 15.38% / 0.879). Live RULES v2 8.64% / 1.204 / -12.05% (OOS 9.51% / **1.282** / -12.05%).
3. **4b legs, all five:** H1 1.294 > 0.959 ✓; H2 1.126 > 0.829 ✓; OOS 1.224 > 0.879 ✓; MaxDD -17.79% ≥
   0.6·SPY -20.23% ✓; CAGR 11.51% ≥ 0.7·SPY 10.63% ✓.
4. **Why PARK.** Parents EWALL 13.25% / 1.123 / -22.53% and LOWVOL20 6.81% / 1.000 / -14.79%: the
   candidate's CAGR and MaxDD sit strictly *between* them. It clears 4b only because 4b's DD and CAGR
   legs are bracketing floors that each parent fails on opposite sides. It also loses to the live book OOS
   on both Sharpe and drawdown, and 25 other U56 books in the same menu pass 4b.

## Exact RULES wording, if the Sunday review overrules the PARK

> **RULES vNEXT — U56 calm-state blend (replaces clause 2).**
> Universe: `research/universe.json` (56 instruments). Rebalance weekly, on the last trading day of
> each week; weights decided at that close are applied at the next close. Gross 0.75 of NAV; the
> remainder is cash. No shorting, no leverage.
> **State (decided at the same close):** let `v_t` be the 20-day realised volatility, annualised, of the
> equal-weighted daily return of all instruments priced that day. The state is **CALM** if `v_t` is
> strictly below its own expanding 70th percentile computed from the first available bar through `t`
> (minimum 252 observations; before that, not CALM).
> **Holdings when CALM:** hold every instrument priced that day at `0.75 / N` of NAV, `N` = the number
> priced.
> **Holdings when NOT CALM:** hold the 20 instruments with the lowest 20-day annualised realised
> volatility that day, each at `0.75 / 20` of NAV.
> Gated-out weight is held as cash and is never re-spread.

Reproduce: `research/backtests/2026-09-09_do-the-record-s-CONDITIONAL-clauses-ever-beat-their-own-unconditional-parents_cloud.py`
(row `panel=U56, book=EWALL|LOWVOL20@CALM70` in `.books.csv`).
