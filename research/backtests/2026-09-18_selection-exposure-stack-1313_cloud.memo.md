# KEEP-4b memo — idea 1313 STACK (selection N=15/H=63 + vol-target 6%/21d, U56)
*(2026-09-18, lane cloud. Evidence: `2026-09-18_do-SELECTION-and-EXPOSURE-STACK-at-SMALL-s-DD-CAP_cloud.{py,grid.csv,walkforward.csv,console.txt}`. Not a RULES change — rule 6 reserves that for the Sunday review.)*

1. **Path.** KEEP-**4b** (capital-worthy) on U56, full sample AND rule-8 OOS. 4a is 0/48 — the live book's drawdown is not beatable here and that leg is not claimed.
2. **Full sample (10 bps, t+1):** 11.81% / **1.2290** / **-10.66%**, H1 1.294 / H2 1.172, turnover 3.79x/yr — vs SPY 15.13% / 0.8849 / -33.72% (cap -20.23%, floor 10.59%) and the frozen anchor 13.66% / 1.1706 / -16.38%.
3. **Rule 8 (params on warm-up..2016-12-31, 2017-2026 read once):** the IS argmax picks this exact cell; OOS **12.31% / 1.2444 / -10.66%** vs SPY OOS 15.28% / 0.8747 / -33.72% and anchor OOS 15.12% / 1.1947 / -16.38% — **+0.0497 OOS Sharpe and +5.72 pp OOS MaxDD for -2.81 pp OOS CAGR.**
4. **Breadth:** 11 of 16 stacked cells pass 4b on U56 (full and OOS), 12 of 16 on B136; the pass is not one cell.
5. **Mechanism:** super-additive (resid +6.13 pp). Selection alone at N=15/H=63 makes drawdown worse (-21.22%, 4b FAIL); exposure alone reaches -11.95% at a bigger CAGR cost. Only the stack gets both.
6. **Honest cost:** every pass is bought with CAGR. This is a drawdown-for-return trade, not dominance over the frozen incumbent.
7. **Does NOT generalise:** SMALL663 is 0/16 on both bases (cap cleared in 3 cells, CAGR floor missed by 4.4 pp in all of them). Do not read this memo as a SMALL result.
8. **Two dials only** (N, TARGET); H, WINDOW, CAP, cadence, cost were frozen at values certified by ideas 1301 and 1297 before this run and were not searched.
9. **Survivorship (rule 9):** U56 is a current-constituent list; absolute levels are biased up, cross-cell comparisons are the defensible part.
10. **Exact RULES wording, if a Sunday review adopts it:**
    > **Clause S (selection).** At each weekly rebalance, rank every instrument priced that day by the 3-leg composite (21/252, 0/126, 0/63 percentile ranks, averaged, halved unless the close is above its 200d MA), admit only names above their 200d MA with 20d annualised vol < 0.60, and hold the top **N = 15**. A held name is retained until it has been held **H = 63** trading days; only the shortfall to N is refilled from the ranking.
    > **Clause E (exposure).** Size the book at `k_t = min(0.60, 0.06 / v_t)` of NAV, where `v_t` is the annualised standard deviation of the clause-S book's constant-gross daily returns over the **21** trading days **ending at t-1**; the ungrossed remainder is held as CASH and is never re-spread. Weights are decided at close t and applied at close t+1; costs 10 bps per unit turnover.
