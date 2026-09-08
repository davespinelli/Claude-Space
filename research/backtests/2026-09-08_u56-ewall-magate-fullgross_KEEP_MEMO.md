# KEEP-candidate memo — U56 EW-all, 200d-MA gated, FULL gross, monthly (path 4b)

1. **Origin:** by-product of idea 420's fresh 31-arm menu (cloud, 2026-09-08); the same arm is
   the rule-8 IS-Sharpe argmax in idea 417's independent run. Not adopted — Sunday review decides.
2. **Book:** hold every panel name priced that day whose close is above its 200-day moving
   average, equally weighted at 100% gross; gated-out weight goes to CASH; rebalance monthly.
   Panel = `research/universe.json` (U56 ETF/mega-cap). No ranking, no vol filter, no de-grossing.
3. **Full sample (2009-01-13..2026-09-04, 10 bps, next-day execution):** CAGR **11.96%**,
   Sharpe **1.2126**, MaxDD **−15.49%**, halves 1.249 / 1.179. At 25 bps: 11.63% / 1.1822 / −15.54%.
4. **Rule 8 (chosen on IS ≤ 2016-12-31, read once on 2017-01-01..):** OOS CAGR **12.72%**,
   Sharpe **1.2750**, MaxDD **−15.49%**, OOS halves 1.424 / 1.114. At 25 bps: 12.37% / 1.2434 / −15.54%.
5. **4b bars (SPY 15.45% / 0.8820 / −33.72% OOS; full-sample SPY halves both cleared):**
   Sharpe > SPY in both halves ✓, OOS ✓; CAGR 12.72% ≥ 10.82% floor ✓; MaxDD −15.49% ≤ −20.23% cap ✓.
   **Passes 4b on the full sample AND on the OOS window at 10 and 25 bps.**
6. **4a: FAILS** against the live RULES v2 book (v2 OOS 9.53% / 1.2851 / −12.05%) — v2 is
   shallower in drawdown and higher in OOS Sharpe; this candidate buys +3.2 pp of CAGR with 3.4 pp
   more drawdown. It is a 4b (capital) candidate only, never a 4a one.
7. **Not a knife edge:** all 8 gross-1.00 arms on u56@10 clear 4b across bands 0–6% and both
   cadences (weekly: OOS 12.20% / 1.2623 / −15.84%), so the only load-bearing dial is **gross = 1.00**.
8. **Scope limits:** on broad136 it clears 4b at 10 bps and FAILS at 25; on SMALL439 it fails at
   every rung (5.39% / 0.5885 / −21.72% OOS). It is a U56 object first, a broad136 object second.
9. **Caveats:** chosen from a 30-arm menu (multiple comparisons); U56 is a fixed current list, and
   broad/small carry survivorship (data/SMALL_PANEL_README.md); relative to live RULES v2 the only
   change is removing the 0.75 de-gross and slowing to monthly, so idea 296/304's de-gross pricing
   applies directly and should be re-read before any adoption.
10. **Exact RULES wording if adopted:** *"Each month-end, hold every instrument in the universe
    whose close is above its 200-day moving average, equally weighted, investing 100% of NAV
    across those names; hold the remainder in cash. No ranking, no volatility filter, no
    de-grossing. Rebalance monthly at the next close after the signal date."*
