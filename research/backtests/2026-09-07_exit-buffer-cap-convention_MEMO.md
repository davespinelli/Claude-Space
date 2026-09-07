# Memo — idea 358, the exit buffer under three cap conventions (2026-09-07, cloud)

1. **No promotion.** The grid's best 4b cell (U56, KT cap, x=40: 12.73% CAGR, Sharpe 1.127, MaxDD
   -15.27%, halves 1.183/1.089, OOS 1.189, c* 46 bps) is idea 349's committed `e=0, x=40` row
   reproduced at < 1e-12, already PARKed. The two NEW forms are dominated by it.
2. Exact RULES wording, were the leading cell ever adopted (it is not, today):
   *"Rank the eligible universe (above its 200d MA, vol20 < 0.60) by the v1 composite with the
   vol scaler off. Buy a name when its rank reaches 20 or better; sell it only once its rank
   passes 60. Hold at most |{rank <= 20}| names, weighting each 0.75/k of NAV. Rebalance weekly,
   execute at the next close."*
3. The exit buffer's value is **not** a cap-convention artefact: mean marginal Sharpe +0.0577
   (KT) / +0.0572 (FLAT) / +0.0444 (UNCAP), **15/15 positive under all three**.
4. What the cap DOES own is name-count neutrality: dnames +0.000 (KT) / +0.048 (FLAT) /
   **+7.673** (UNCAP), spearman(x, names) 0.000 / 0.113 / **+0.956**.
5. Even UNCAP's widened book beats its holdings-matched hard cut 14/15 (mean +0.0491, OOS 11/15
   +0.0283) at 9.43 vs 13.89x/yr — the width is not what pays. Opposite of the entry dial.
6. `FLAT` is not a materially different cap: it differs from `k_t` only through **rank ties**
   (seed days 88/975 U56, 92/975 B136, 14/870 SMALL439).
7. But the buffer's memory **carries a tie divergence forward** — 154-664 differing rebalances,
   up to **0.037** of Sharpe. **PROTOCOL should require any band/buffer row to state its cap
   convention**; without it a published band cell is not reproducible.
8. Rule 8: mean OOS Sharpe KT 0.8761 > UNCAP 0.8580 > FLAT 0.8559; the IS chooser beats
   do-nothing 20/27 (+0.0538); the cap rule moves the pick in 2 of 9.
9. KEEP paths over 162 rows: **4a 0/54 at every rung**; 4b 29/20/15 of 54 at 0/10/25 bps.
10. SURVIVORSHIP: all three panels are current-constituent lists; levels are optimistic, the
    cap- and x-differences much less so. SMALL439 drops 44 names with `max_1d_move >= 1.0`.
