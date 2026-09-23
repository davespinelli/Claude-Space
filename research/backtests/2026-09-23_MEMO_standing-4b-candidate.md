# MEMO — the standing 4b KEEP-candidate after the deletion census (2026-09-23, lane cloud, idea 2332)

1. **What it is.** `RG100 + phi = 1.00`: hold every name INSIDE the 200d +/-3% band (clause-2 hysteresis) at `gross / N_in` of NAV, gross = 0.75, weekly, t+1; sweep the residual `1 - sum(w)` into SHY.
2. **Status.** NOT a new candidate — this is idea 2300's incumbent. This run removes one published objection and changes no rule. RULES.md, scan.py, bot.py and baseline.py are untouched.
3. **Headline (U56, 10 bps).** 12.59% CAGR / 1.1934 Sharpe / -17.39% MaxDD; halves 1.24 / 1.17; OOS 13.85% / 1.2397. SPY 15.23% / 0.8897 / -33.72%. Clears 4b (DD cap -20.23%, CAGR floor 10.66%).
4. **Second panel (B136, 10 bps).** 11.99% / 1.0930 / -18.11%; OOS 12.29% / 1.0994 against SPY 15.12% / 0.8844. Clears 4b.
5. **New evidence — it is a BOOK, not a draw.** 4b survives **56 of 56** U56 deletions and **136 of 136** B136 deletions at 0, 10 and 25 bps. Worst single deletion (NFLX) costs 0.0561 of Sharpe on U56; the median deletion is mildly positive.
6. **New evidence — rule 8.** With gross fitted on <= 2016-12-31 per deletion and 2017-2026 read once, **192 of 192 picks take gross 0.75 and 192 of 192 beat SPY's OOS Sharpe** (U56 min OOS Sharpe 1.1793; B136 min 1.0795).
7. **Open risk, NOT closed by this run.** Concentration. Max per-name weight is 15.00% on U56 (20.00% at gross 1.00), and deletion RAISES it (up to 18.75%) because `N_in` falls. Idea 2318 showed widening the band does not de-concentrate either. Idea 2322's per-name cap (`CAP2`) remains the live route at this risk.
8. **Known limits.** 4a fails at every cell (drawdown is 5-6x the live book's). 4b fails at 50 bps and at gross 1.00. SMALL fails at every width (0 of 48). B136 and SMALL are survivorship-biased current constituents; and `MMC` is all-NaN in `data/prices_broad.csv`, so B136 is a **135**-name panel.
9. **Exact RULES wording, if a Sunday review adopts it** (replacing clause 2's weighting, not the gate):
   > **Clause 2 (band gate, unchanged).** A name is IN when its close exceeds its 200-day moving average by more than 3%, OUT when it falls more than 3% below, and otherwise keeps its previous state; OUT until 200 closes exist.
   > **Clause 3 (weighting, REPLACED).** Hold every IN name at `0.75 / N_in` of NAV, where `N_in` is the count of IN, priced names on the rebalance date. Do not rank and do not vol-scale. Rebalance weekly on the last trading day of the week; execute at the next close.
   > **Clause 4 (idle NAV, REPLACED).** Sweep the residual `1 - sum(w)` in full into SHY. Do not re-spread it across IN names and do not hold it as un-remunerated cash.
10. **Recommendation.** Keep as the standing 4b candidate; do not ship this week. The one thing that should gate adoption is the concentration cap, not deletion robustness — that question is now answered.
