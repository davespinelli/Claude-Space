# KEEP-4b memo — idea 1635 (lane cloud, 2026-09-19). PROPOSED for Sunday review, NOT enacted.

1. **What passed.** The 2026-09-04 candidate (U56, top-20 equal weight, no vol scaler, 126-row min
   hold, weekly) at **gross 0.65** clears PROTOCOL path **4b on 16 of 16** (L, c) cells: execution
   lag L ∈ {1,2,3,5} trading days × cost c ∈ {0,10,25,50} bps. Worst cell (L=5, c=50): 12.33% CAGR,
   Sharpe 1.0442, MaxDD −18.17%, DD margin +2.06 pp, CAGR margin +1.74 pp.
2. **Anchor (L=1, 10 bps):** FULL 13.68% / 1.1540 / −16.73%, halves 1.207 / 1.121 (SPY 0.957 /
   0.825); **OOS 2017-2026 14.99% / 1.1858 / −16.73%** (SPY OOS 15.26% / 0.8737). Turnover 2.41/yr.
3. **Rule 8.** Nothing is chosen. N = 20 and gross 0.65 are inherited frozen from idea 1293; L and
   c are adversarial axes with no chooser. IS and OOS are published separately at every cell and
   the OOS 4b legs are scored against SPY's own OOS bars.
4. **Why 0.65 and not 0.75.** At 0.75 the DD margin is +1.10 pp and **one further day of lag cuts
   it to +0.16 pp**; at 0.65 it is +3.50 pp and survives L=5 at 50 bps. 2.1 pp/yr of CAGR buys
   2.4 pp on the only leg that binds.
5. **Path used: 4b.** Path 4a passes 0 of 96 cells and cannot adjudicate a growth book against a
   −12.05% MaxDD incumbent.
6. **PROPOSED RULES wording**, exact, to be pasted only if Sunday review adopts it:
   > **Growth book (satellite).** Each Friday at the close, rank every instrument that is above its
   > 200-day moving average and whose 20-day annualised volatility is below 0.60, by the equal
   > average of the percentile ranks of (a) the 252-day return skipping the last 21 days, (b) the
   > 126-day return and (c) the 63-day return, that average halved for any name below its 200-day
   > average. Hold the **top 20** names at **equal weight**, **0.65 / 20 = 3.25% of NAV each**
   > (total gross 0.65, remainder in cash). A name once bought is held for at least **126 trading
   > days** unless it stops being priced. Orders are placed after the Friday close and may be
   > filled at any close from the next trading day up to **five trading days later**. No vol
   > scaler, no ranking of held names, no re-spreading of gated-out weight.
7. **What this does NOT license.** It is not a replacement for live RULES v2 and does not touch it.
   It is a satellite proposal at 4b, for the Sunday review to size or reject.
8. **Survivorship (rule 9).** U56 is a current-constituent hand-kept mega-cap/ETF list; delisted
   and acquired names are absent. Every figure above is an upper bound. This alone argues for
   sizing well below any figure here.
9. **Replication.** B136 at 0.65 clears 4b only out to L = 3 and fails at 50 bps; SMALL clears
   0 of 32. The book is a **large-cap fact**, not a demonstrated mechanism. Say so in any sizing.
10. **Open doubt to carry.** The margin is small in absolute terms against idea 1511's 2.93 pp
    paired SE for a MaxDD contrast (+3.50 pp ≈ 1.2 SE). A bootstrap of this exact contrast is the
    next thing to run before any capital moves.
