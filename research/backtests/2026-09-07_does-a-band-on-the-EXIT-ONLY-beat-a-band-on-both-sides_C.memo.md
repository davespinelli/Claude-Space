# KEEP-candidate memo (PROTOCOL path 4b) — idea 349, lane C, 2026-09-07 — **PARK-recommended**

1. **Book.** U56, weekly. Rank every eligible name (above its 200d MA, vol20 < 0.60) by the RULES
   v1 composite with the vol scaler OFF. Buy an unheld name only at rank <= 4; sell a held name
   only once its rank passes 60. Hold count capped at `k_t = |{rank <= 20}|`; weights `0.75/k`.
2. **Exact RULES wording** if it were ever adopted (it should not be, see 8-10):
   *"2. Rank the eligible universe by the v1 composite (12-1 momentum, 6m and 3m returns, equally
   ranked; no volatility scaler). Enter a name only when its rank is 4 or better. Hold it until
   its rank passes 60 or it leaves the eligible set. Cap holdings at the count of names ranked 20
   or better. Weight every holding at 0.75/N of NAV, N = names held; the remainder is CASH.
   Rebalance weekly at the close, execute at the next close."*
3. **Full sample** (2009-01-13 -> 2026-09-04, 10 bps, next-day): CAGR **16.52%**, Sharpe
   **1.164**, MaxDD **-19.02%**, turnover 5.45x/yr, ~11.1 names held.
4. **Halves:** H1 **1.245** / H2 **1.096** against SPY's 0.957 / 0.834 — both bars cleared.
5. **Rule 8 (walk-forward):** OOS 2017-2026 Sharpe **1.168**, CAGR 17.18%, MaxDD -19.02%, against
   SPY's 0.882 / 15.45% / -33.72%. It is the FULL menu's own IS pick, so this OOS number carries
   no hindsight; its regret against the OOS-best cell is -0.021.
6. **4b bars, all five, at 10 bps:** H1 +0.288, H2 +0.262, OOS +0.286, DD +0.012 (-19.02% vs the
   -20.23% cap), CAGR +0.059. **PASS at 0, 10 and 25 bps.** Breakeven **c\* = 60 bps**, the
   record's highest weekly breakeven (idea 331's was 47); the first bar to fail is DD.
7. **4a: FAIL** — H2 **-0.095** and MaxDD **-0.070** (-19.02% against the live RULES v2 book's
   -12.05%); H1 clears by +0.019.
8. **Why PARK, reason 1 — it does not travel.** The identical construction fails 4b on B136 and on
   SMALL439 at every rung (B136 0/42 at 10 and 25 bps, SMALL439 0/42 everywhere). Every 4b pass
   in this run's 126 cells is a U56 pass.
9. **Why PARK, reason 2 — this run's own rule 8 argues against the dial that produced it.**
   Taking the entry buffer OFF the chooser's menu is worth **+0.0426** of mean OOS Sharpe across
   the three panels and halves its regret (-0.089 -> -0.046); the exit-only menu beats the (0,0)
   anchor and idea 331's cell on 3/3 panels where the full menu manages 2/3 and 1/3. On B136 the
   full menu's entry-buffered pick lands at OOS 0.772, below SPY.
10. **Why PARK, reason 3 — it is a concentration bet, not a band.** The entry buffer's effect is
    almost entirely on holdings count (spearman(e, names) **-0.988**) and barely on turnover
    (-0.298); at e=16 the book holds ~11 names, not 20. On a current-constituent panel
    (**SURVIVORSHIP**) an 11-name momentum book is the most flattered object this record trades.
    Recommendation: keep the EXIT buffer as the record's band instrument, do not adopt the entry
    buffer, and leave RULES v2 unchanged.
