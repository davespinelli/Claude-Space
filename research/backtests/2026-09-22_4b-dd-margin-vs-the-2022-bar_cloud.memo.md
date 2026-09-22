# PARK memo — idea 915, lane cloud run 4, 2026-09-22.  **DO NOT ADOPT.**

1. **Cell.** U56, RULES v2's own 200d ±3% hysteresis band form, **gross 1.00** (not 0.75),
   **weekly**, t+1, 10 bps.  Gated-out weight to cash; no ranking, no vol filter.
2. **Numbers (published bar, 10 bps).** FULL 11.53% / 1.2009 / −15.91%; IS 10.16% / 1.1047 /
   −10.45%; **OOS 12.67% / 1.2760 / −15.91%** (H1 1.430 / H2 1.106).
3. **Against the live book (OOS).** RULES v2 9.46% / 1.2767 / −12.05%.  Against SPY OOS
   15.29% / 0.8751 / −33.72% (4b cap −20.23%, floor 10.70%).
4. **4b.** PASS on FULL and OOS, all four legs, at 5 of 5 rebalance offsets.  4a FAIL.
5. **Why it is PARK and not KEEP.** It **FAILS 4b in the IS window**, on a CAGR margin of
   −0.308 pp that is itself *inside* its own 0.875 pp offset spread — i.e. unresolvable.
   Selecting this cell requires having read 2017–2026.  Idea 2119 reached the same PARK on a
   different grid; this run reproduces it independently and adds the unresolvability.
6. **Its monthly sibling is worse, not better.**  Gross 1.00 monthly passes 4b in all three
   windows but its DD margin (+1.43 pp) is **4.1× smaller than its own monthly offset spread**
   (5.87 pp) and the verdict holds at only 2 of 5 offsets.  Killed outright by idea 914's clause.
7. **Exact RULES wording IF a Sunday review ever adopted it (it should not, on 5):**
   *"2. Hold every instrument whose close is above its 200-day moving average × 1.03, and keep
   holding it until the close falls below that average × 0.97.  Weight each held name at
   1.00 / N of NAV, N = instruments priced that day; weight freed by the gate goes to cash and
   is never re-spread.  Rebalance weekly, at the last trading day of the week, executing at the
   next session's close."*
   This is RULES v2 verbatim with **0.75 replaced by 1.00** — one dial, nothing else.
8. **What adoption would cost.** Gross rises 33%; OOS MaxDD −12.05% → −15.91% (the live book's
   unspent drawdown budget is what funds it), OOS CAGR 9.46% → 12.67%, OOS Sharpe unchanged to
   3 dp (1.2767 → 1.2760).  It is a pure slide along a fixed Sharpe ray — idea 2085's finding.
9. **Survivorship (rule 9).** U56 is a current-constituent list; the absolute levels are
   optimistic.  The gross contrast is within-tape and does not repair the level.
10. **Status: PARK, reported not proposed.  RULES.md, PROTOCOL.md, scan.py, bot.py and
    baseline.py are untouched by this run.**
