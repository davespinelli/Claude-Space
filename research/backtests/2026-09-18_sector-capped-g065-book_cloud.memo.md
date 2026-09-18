# KEEP-4b candidate memo for the Sunday review — the SECTOR-CAPPED U56 BOOK AT g = 0.65
(idea 1295, lane cloud, 2026-09-18. Rule 6 reserves enactment for the Sunday review; nothing is enacted
here. This proposes a CAPPED variant of the standing U56 candidate, and it is the first book in this
family that is both stress-robust AND Sharpe-dominant over the uncapped incumbent.)

1. **The book the rule-8 chooser lands on.** U56, top **N = 20** by the frozen 21/252 + 0/126 + 0/63
   composite among names above their own 200d MA with vol20 < 0.60, min-hold H = 126, equal weight,
   **gross 0.65 of NAV**, **at most 5 names per sector**, weekly decide / trade next session. 19.74 names
   held on average, 2.42 turns/yr — the cap costs 0.01 turns/yr over the uncapped book.
2. **Full sample 13.76% / 1.2116 / −19.06%**, halves **1.2937 / 1.1491**, OOS (2017–2026, read once)
   **14.60% / 1.2261 / −19.06%**. SPY on the same dates: 15.13% / 0.8848 / −33.72%, OOS 15.28% / 0.8745.
   4b **PASS** on every leg: DD margin +1.17 pp, CAGR margin +3.16 pp.
3. **It is STRESS-ROBUST: 4b at all 15 of idea 1292's phase × delay points** (5 decision weekdays × 3
   execution lags), worst point Thu / t+3 at 13.31% / 1.1593 / −20.20%, OOS Sharpe 1.1739; worst OOS
   Sharpe over the ensemble **1.0995**, still 0.225 above SPY's 0.8745. The same arm reproduces idea
   1292's two published control counts exactly — uncapped g=0.65 **15/15**, uncapped g=0.75 **9/15**.
4. **The cap is what 1289 said it was NOT, once the book is sized.** At the frozen g = 0.75 a 5-name cap
   FAILS 4b (−21.76% MaxDD against a −20.23% cap, margin −1.53 pp), which is what idea 1289 reported. At
   g = 0.65 the identical cap **PASSES** with +1.17 pp to spare. The cap costs **zero** rungs of size:
   c=5 and c=20 both first clear 4b at g = 0.55 on U56.
5. **At matched gross the cap BUYS Sharpe and SELLS drawdown.** c=5 minus c=20 at g = 0.65: Sharpe
   **+0.0590**, OOS Sharpe **+0.0428**, CAGR **+0.09 pp**, MaxDD **−2.33 pp**. It is the only cap on U56
   that improves Sharpe; c=2, c=3 and c=8 all lose it (−0.0379 / −0.0668 / −0.0245).
6. **It dominates the standing uncapped candidate on every Sharpe leg** (full 1.2116 vs 1.1526, H1 1.2937
   vs 1.2130, H2 1.1491 vs 1.1129, OOS 1.2261 vs 1.1833) at the same CAGR (13.76% vs 13.66%) and a 2.33 pp
   deeper drawdown. It also cuts the drawdown's phase × delay **spread** from 2.98 pp to **1.18 pp** — the
   cap stabilises the leg this family keeps dying on.
7. **The one number that should give a reviewer pause.** The pick's worst-case DD margin over the ensemble
   is **+0.03 pp** — Thu / t+3 lands at −20.20% against a −20.23% cap. One rung down, **c=5 / g=0.60** is
   also 15/15 robust with a worst-case joint margin of **+0.95 pp** (full 12.68% / 1.2117 / −17.69%, OOS
   13.46% / 1.2263). Rule 8's declared chooser picks 0.65; the safer rung is 0.60, and the review should
   decide which. This is the same one-rung optimism idea 1290 found in the single-point joint argmax.
8. **Not a panel-wide fact.** B136's chooser picks c=3 / g=0.60 (4b PASS, OOS 11.39% / 1.0095) but that
   cell is not stress-run here. **SMALL clears 4b at 0 of 45 cells at every cap and every gross** — as in
   every run of this family, this is a mega-cap/ETF result. 4a is **0 of 135**.
9. **Survivorship (rule 9).** U56 / B136 are current-constituent hand-kept lists, SMALL a current sub-$2B
   screen. Delisted and bankrupt names are absent, which flatters the UNCAPPED book most — the corner the
   screen concentrates into is the corner whose survivors are known — so the cap's measured cost here is
   if anything an over-statement and its measured benefit an under-statement. No number is live expectancy.
10. **Exact RULES wording, if a Sunday review enacted it.** *"Each week at the close of the last trading
    session, rank every instrument in the mega-cap/ETF universe that is above its own 200-day moving
    average and has 20-day annualised volatility below 0.60, by the equal-weighted average of its
    percentile ranks on (t−21 / t−252), (t / t−126) and (t / t−63) total return. Take names in rank order
    until 20 are held, skipping any name whose sector already holds 5 of the 20; a name's sector is the
    sector ETF its daily returns correlated with most over its own first 252 trading days, and a name with
    fewer than 252 trading days of history is exempt from the limit. Hold the selected names equally
    weighted at 0.65 of NAV with the remainder in cash; a holding is retained for at least 126 trading
    days from the session it was bought, and a retained holding keeps its slot and counts against its
    sector's limit. Trade at the next session's close."*

Script: `research/backtests/2026-09-18_does-the-CERTIFIED-U56-g0.65-BOOK-AFFORD-a-SECTOR-CAP-the-g0.75-one-could-NOT_cloud.py`
