# RESULT — idea 2419, the EXTENDED-NAME TRIM on the capped 4b candidate (2026-09-23, lane C, run 45)

**ANSWERED = NO. KILL.** Not a KEEP-candidate, so no adoption memo — nothing here changes RULES.md,
scan.py, bot.py or baseline.py, and none of those files was touched.

1. **Question.** Idea 2387 priced the breadth cap (KEEP the `N_max` names furthest above the 200d MA)
   and killed it. This run priced its mirror: DROP the top `f` fraction of the band's IN set by
   `px/ma - 1` and hold the rest, residual to SHY at phi = 1.00. `f = 0.00` IS CAP2.
2. **Integrity.** 14 of 14 gates pass. `f = 0.00` is bit-identical to an independent CAP2
   construction through `engine.backtest` under BOTH conventions (max|d| **0.000e+00**), the numpy
   replica matches the engine on the live book AND on a trimmed book to 0.000e+00, the truncation
   test finds no lookahead, and the anchor reproduces the committed U56 headline
   (11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318, turnover 3.51x) to 3.95e-05.
3. **The ladder is monotone downhill.** U56 / CAP2 / conv R / g 0.75 / 10 bps, `f` 0.00 -> 0.30:
   CAGR 11.62% -> 10.19% -> 9.44% -> 8.23% -> 7.32%; Sharpe 1.2687 -> 1.1694 -> 1.1383 -> 1.1039 ->
   1.1308; OOS Sharpe 1.3318 -> 1.2361. Every `f > 0` cell fails 4b, and every one fails on `L_CAGR`
   alone (leg string 11110) — the trim buys drawdown it cannot afford.
4. **The exchange rate is worse than a pure exposure dial's.** pp of CAGR per pp of drawdown, 16
   cells: median **1.39**, only 4 under 1.0, 3 cells made drawdown WORSE, Sharpe improved in 0 of 16.
   Idea 2381 measured one-for-one for every cross-sectional device; this one is worse than that.
5. **The placebo is the kill, and it is sign-definite.** Random-trim control (same `k_t`, same
   de-grossing, per-name score fixed over the sample, 5 seeds, only the criterion differs):
   **EXT beats the random mean Sharpe in 0 of 16 cells** and is the **worst of its own 6-book bundle
   in 16 of 16** (mean rank 6.00, chance 3.50). Extendedness on this book is a RETURN SOURCE; the
   most-extended names are not where the drawdown lives.
6. **The two channels, separated.** conv D (de-gross, trimmed weight to SHY) beats conv R (re-spread
   over survivors) at every `f` on U56 — 1.1832 vs 1.1308 at `f = 0.30`. Re-concentrating into the
   LESS extended names is itself harmful: the same finding said a second way.
7. **It makes the only stated adoption blocker worse.** Turnover rises monotonically in `f`: U56 conv
   R 3.51 -> 6.35 x/yr, B136 conv R 4.68 -> 9.69 x/yr (live book 1.77x). Under conv R mean max
   per-name weight also rises (1.87% -> 2.06% U56, 0.94% -> 1.24% B136) — the trim re-concentrates
   the exact risk CAP2 exists to cap.
8. **Rule 8, unanimous.** `f` fitted on <= 2016-12-31 only, 2017-2026 read once, 128 picks:
   **128 of 128 land on `f = 0.00`**; 0 of 128 beat the anchor OOS on Sharpe, MaxDD or CAGR; U56 and
   B136 agree in 64 of 64 cells.
9. **Two surviving 4b cells, filed NOT recommended.** B136 / CAP2 / conv R / `f` = 0.05 and 0.10 at
   the live gross still clear all five legs, but each is strictly dominated by the anchor on CAGR and
   Sharpe, and `f` = 0.05 is worse on MaxDD too (-17.45% vs -17.10%). Dominated is not a candidate.
10. **Limits.** U56 / B136 only — the candidate family has no 4b pass on SMALL to keep or break.
    B136 and SMALL are survivorship-biased current constituents (rule 9), so `L_CAGR` is the
    contaminated leg; the trimmed-vs-untrimmed contrast is same-tape and first-order immune.
