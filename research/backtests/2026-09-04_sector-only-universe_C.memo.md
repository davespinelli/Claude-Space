# Memo — STK20/CAND-n20: a 4a+4b pass that should be REJECTED (idea 10, lane C, 2026-09-04)

1. **What it is.** Idea 2's construction run on `universe.json`'s 20 mega-cap single
   stocks only, ETFs removed: 12.1% / **1.338** / −12.1%, halves 1.341/1.344, turnover 3.5×.
2. **It passes both KEEP paths** — the only point in 30 to pass 4a (Sharpe > RULES v1 in
   both halves, MaxDD −12.1% vs v1's −13.8%) and it passes 4b with margin on every bar.
3. **Rule 8 selects it.** S2 (4b-aware) picks it on in-sample data alone; OOS 14.0% /
   1.449 / −12.1% vs SPY 15.5% / 0.884 / −33.7%. S1 picks STK20/n=10 (OOS 21.2%/1.366).
4. **Recommendation: do not adopt.** The panel is 20 tickers selected as 2026 constituents;
   a 12-1 momentum book on them is close to a look-ahead portfolio.
5. **The run's own control quantifies that.** The stock-leg advantage is +5.19%/yr (t to
   +4.45) on these 20 names and only +0.92%/yr (t max +2.04) on `universe_broad.json`'s
   100 stocks, which also **fail 4b on drawdown** at every n. A 5.6× shrink with a wider
   stock leg is selection, not a premium.
6. **Exact RULES wording it would require** (for the record, so the Sunday review rejects a
   written rule rather than a vibe): *"§2 Universe — eligible instruments are the 20 names
   in `universe.json:megacap`; exchange-traded funds are not eligible. §3 Sizing — hold the
   top 20 eligible names by the v1 composite computed WITHOUT the `/sqrt(vol20)` term,
   equal-weight at 3.75% each (75% gross), rebalanced weekly, with the 200d-MA and
   vol20 < 0.60 eligibility gate unchanged."*
7. Note that at n=20 on a 20-name panel this rule holds **every eligible name** — the
   ranking is inert and the book is `EWall` with a gate. Mean 13.2 eligible, gross 49%.
8. **Prerequisite before it could ever be a KEEP:** a point-in-time mega-cap list (top 20
   by market cap as of each rebalance, including names that later fell out) — idea 71.
9. **Cheaper alternative already in the grid:** `B136/EWall` passes 4b with no ranking and
   no stock/ETF choice at all (10.7% / 1.027 / −17.7%, halves 1.146/0.917, OOS 1.021).
10. **Standing candidates unaffected.** Idea 2's `U56/CAND-n20` reproduces exactly and
    still passes 4b; nothing in this run changes it.
