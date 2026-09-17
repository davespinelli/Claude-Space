# Memo — idea 1161 (lane B, 2026-09-17): the `U56 / W / N=12 / H=126` book. **RECOMMENDATION: PARK.**

Written because PROTOCOL rule 4 path 4b passed on this run's 216-book population, not because
anything here should be enacted. This idea is a question about resample nulls; the book below
is a by-product of its mandatory rule-8 population and is proposed by nobody, this memo included.

1. **Exact RULES wording, if it were ever enacted:** *"each Friday, rank every priced name
   inside the 200-day trend gate and under the 0.60 realised-volatility ceiling by the CAND20
   composite (12-1 momentum, 6-month and 3-month total return, equal-weighted percentile
   ranks); hold the top 12 at 0.75/N of NAV with a 126-trading-day minimum holding period;
   gated-out weight goes to CASH, never re-spread; weights decided at Friday's close are
   applied at the next session's close at 10 bps per unit turnover."*
2. **What passes.** Full sample **17.65% CAGR / 1.1658 Sharpe / −20.17% MaxDD** (halves
   1.2741 / 1.0833); OOS 2017–2026 **18.78% / 1.1701 / −20.17%**. Against SPY full 15.06% /
   0.8814 / −33.72%, OOS 15.15% / 0.8684 / −33.72%; against live RULES v2 full 8.60% /
   1.1980 / −12.05%, OOS 9.42% / 1.2714 / −12.05%.
3. **THE PASS IS A KNIFE EDGE ON THE DRAWDOWN CAP AND THAT IS DISQUALIFYING ON ITS OWN.** 4b's
   cap is 0.60 × SPY's 33.72% = **20.232%**. This book sits at **20.17%** — it clears by
   **0.06 pp**. Its immediate neighbour `N=15/H=126/W` has a *higher* OOS Sharpe (**1.1869**)
   and **fails**, at 20.97%. A rule whose verdict flips between N = 12 and N = 15 on the
   second decimal of a drawdown is not a rule, it is a coincidence with a parameter attached.
4. **Rule 8 does not reach it.** No chooser on this grid picks it: CH_ISSHARPE and CH_ISCAGR
   pick `N5/H21/M` (OOS 0.8723, fails 4b), CH_ISDD picks `N40/H21/W` (OOS 1.1243, passes 4b),
   CH_NULLDD picks `N15/H21/W` (OOS 1.1100). **0 of 180 picks reach this book.**
5. **Path 4a is 0 of 216 books and 0 of 180 picks.** It never beats the live book's Sharpe in
   both halves at a drawdown no worse — it carries 8.1 pp more drawdown than RULES v2 for
   −0.1013 of OOS Sharpe.
6. **It is prior art, one rung over.** `U56 / W / N=20 / H=126` — the record's own standing
   CAND20 anchor — passes the same two gates at 15.55% / 1.1381 / −19.13% (OOS 1.1615) with a
   **shallower** drawdown. The N = 12 book buys +0.0086 of OOS Sharpe for +1.04 pp of drawdown.
7. **Survivorship (rule 9).** U56 is a current-constituent panel. The 4b CAGR floor and the
   drawdown cap are both measured against an inflated book and the bias does **not** cancel;
   at a 0.06 pp margin on the cap, survivorship alone is larger than the margin.
8. **This run's own subject bears on it.** The 4b drawdown cap is a **maximum-keyed** number,
   and this run measures that a book's |MaxDD| sits ~6% below a re-ordering of its own returns
   with a 1000-draw seed noise of ~1.8%. A 0.06 pp (0.3%) margin is well inside that.
9. **Nothing is proposed for the Sunday review** (rule 6). `RULES.md`, `PROTOCOL.md`,
   `scan.py`, `bot.py` and `baseline.py` are untouched by this run.
10. **PARK.** Unreachable by any honest chooser, failing 4a, dominated by the incumbent one
    rung over, and passing 4b by less than its own measurement noise.
