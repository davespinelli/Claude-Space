# MEMO — U56 / MA-DG / MONTHLY / 21-OFFSET ENSEMBLE / g=1.00 (idea 807, lane C, 2026-09-15)

1. **What passed.** PROTOCOL path **4b** at the pre-declared cell (g=1.00, 10 bps, next-day fills):
   full **11.68% / 1.177 / −19.07%**, halves **1.230 / 1.135**, OOS 2017+ **12.70% / 1.230 / −19.07%**
   against SPY **15.13% / 0.886 / −33.72%** (halves 0.959 / 0.824, OOS 15.27% / 0.874 / −33.72%).
   All five legs true; also at 0/5/15/20/25/50 bps and at execution lags 1, 2 and 3. Path **4a FAILS**
   (0 of 714 cells).
2. **Exact RULES wording, were it ever adopted** (it is NOT proposed for adoption):
   *"Universe: the 56 names of `research/universe.json`. Each trading day compute each name's
   200-day mean close. Hold every name whose close exceeds its 200-day mean at 1/N of sleeve NAV,
   N = names priced that day; the weight of every other name is held in CASH and never re-spread.
   Split capital once into 21 equal sleeves. Sleeve k (k = 0…20) applies its targets only on the
   k-th trading day after each month end, and drifts in between. Sleeves are never re-equalised.
   Fills next day, 10 bps per unit turnover."*
3. **Turnover / gross:** 1.96× NAV per year, realised gross 0.710. ENS-NAV charges only the sleeves'
   own turnover — there is no cross-sleeve transfer — so the ensemble costs no more than the single
   calendar it replaces.
4. **Why this memo does NOT propose a RULES change.** The DD leg clears its cap (−20.23%) by
   **1.16pp**, which is *smaller* than the 4.74pp of the single-calendar book idea 805 already
   killed, and one seventh of the 8.37pp spread across the 21 calendars.
5. Averaging the calendar away buys **+0.31pp** of drawdown (ensemble −19.07% vs mean sleeve
   −19.38%) because the 21 sleeves correlate **0.968** daily and **all 21 trough inside March 2020**.
   One crash, seen 21 times.
6. The published k=0 calendar **ranks 1 of 21 on MaxDD**. Idea 805's 4.74pp margin is the margin of
   that rank; the calendar-free book's margin is 1.16pp.
7. **Rule 8 is half-satisfied.** IS-SHARPE (2009–2016 only) picks g=1.00 and that pick passes 4b OOS;
   IS-BAND-MIDPOINT has **no pick** — the IS window's own 4b band is EMPTY, all 17 gross rungs fail
   the IS CAGR leg. The band this book lives in is an ex-post object (idea 809's pattern).
8. **Fragility:** margin 1.16pp at lag 1, **0.78pp at lag 2, 0.17pp at lag 3**; the 4b gross band is
   {0.95, 1.00} at 10 bps, flush against the ladder's top endpoint, with no interior.
9. **It beats nothing it is compared to on its own terms:** OOS CAGR 12.70% < SPY 15.27%; OOS Sharpe
   1.230 < RULES v2's 1.277; OOS MaxDD −19.07% vs RULES v2's −12.05%.
10. **SURVIVORSHIP:** U56 is the current constituent list; dead names absent, so the CAGR floor and
    DD cap are both easier here than on a point-in-time panel, and the 1.16pp margin is smaller than
    the 1.10pp median |ΔMaxDD| a panel re-vintage alone moved in idea 823. **Verdict: PARK, not KEEP.
    Nothing promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.**
