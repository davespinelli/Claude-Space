# KEEP-candidate memo — idea 46 eligible-fraction (4b) — for the Sunday review

1. **Candidate:** hold the top **85% of whatever is eligible that day** (`ceil(0.85 × E_t)` names),
   equal-weight at 75% gross, ranked by the v1 composite **without** the `/sqrt(vol20)` term.
   Weekly, 10 bps, next-day execution. Avg book 32 names, turnover 9.6x/yr.
2. **Full sample (2009-01-13 → 2026-09-03), universe.json:** CAGR 11.3%, Sharpe 1.072, MaxDD −16.7%,
   vol 10.5%. Halves 1.092 / 1.058, both above SPY's 0.957 / 0.837. RULES v1: 0.641 / 0.692.
3. **Walk-forward (rule 8), f chosen on 2009–2016 only by the pre-registered 4b-aware rule:** picks
   f=0.85; untouched OOS 2017–2026 **12.4% / 1.132 / −16.7%** vs SPY 15.5% / 0.884 / −33.7% and
   RULES v1 7.8% / 0.751 / −13.8%. Passes all five 4b tests. Fails 4a on MaxDD, as every growth book does.
4. **Its one advantage over lane A's n=20 KEEP is portability, and that is the whole reason to
   consider it.** On the 136-name broad universe it passes 4b again — 11.2% / 1.024 / −18.6%,
   halves 1.128 / 0.928 — with the *same* parameter. n=20 fails H2 there (0.814 vs 0.837); only
   n=40 passes, and selecting it would be tuning. A count is a different rule on a different-sized
   list; a fraction is the same rule.
5. **It is worse than n=20 on return.** −1.4pp CAGR full sample, −2.0pp OOS CAGR, −0.04 OOS Sharpe.
   Better on drawdown (−16.7% vs −18.3%). This is a robustness trade, not an upgrade.
6. **Thin CAGR margin.** 11.3% against a 10.7% 4b floor (primary) and 11.2% against 10.7% (broad) —
   ~0.6pp, against n=20's 2.0pp on the primary list. A weaker SPY decade would flip it either way.
7. **The idea's headline test failed.** At matched average book size the fraction rule beats the
   gross-matched fixed-count arm on Sharpe at only 3 of 8 pairs, mean ΔSharpe −0.002. Adaptivity per
   se buys nothing; f=0.85's cross-universe pass is about *scale invariance*, not about adapting to
   breadth. Do not adopt it on the strength of the adaptivity story.
8. **Related finding the review should fold into the idea-2 memo:** the clause "if fewer than 20 are
   eligible, hold all of them at 3.75% and leave the rest in cash" is worth **+0.02 Sharpe at n=20,
   +0.05 at n=30** versus renormalising to 75%. Keep it deliberately.
9. **Survivorship:** 32 of 56 (or 0.85 × ~91 of 136) names from current-constituent lists; absolute
   CAGRs optimistic. Untested: costs above 10 bps and execution lag beyond one day (idea 45 covers
   this for n=20 only).
10. **Recommendation:** adopt n=20 (idea 2) if the review is willing to accept universe-specific
    tuning, and f=0.85 if it wants one rule that survives a universe change. Do **not** treat the
    two as independent candidates — they are the same book at 85% vs 53% of eligible names.

## Exact RULES wording, if adopted

> **Selection.** Each Friday at the close, list every universe name that is (a) above its own
> 200-day moving average and (b) has 20-day realised volatility below 60% annualised. Call that
> list *eligible* and its length **E**. Rank the eligible names by the composite score
> `mean(pct-rank of 12-1 momentum, pct-rank of 6-month return, pct-rank of 3-month return) ×
> (1.0 if above the 200-day MA else 0.5)`. **No `/sqrt(vol20)` term.**
>
> **Sizing.** Hold the top **K = ceil(0.85 × E)** ranked names — i.e. drop the weakest 15% of the
> eligible list — at **75%/K each**, with 25% in cash. If E is 1 or 2, hold those names at 75%/E.
> The book is always 75% invested; the position count moves with market breadth.
>
> **Execution.** Orders are decided at Friday's close and executed at the next session's close.
>
> **Daily hard exit.** Any held name that closes below its own 200-day moving average is sold at the
> next session's close and its weight goes to cash until the following Friday rebalance.

Adoption note: this replaces RULES v1 wholesale (PROTOCOL rule 6 permits a 4b KEEP to do so). It is
an operationally larger book than idea 2's (32 names vs 20) at the same turnover, and its drawdown
budget is roughly −17%. If the review wants only one change this week, idea 2's n=20 is the
higher-return candidate on the live universe and this one is the more portable; running both as
paper sleeves for a quarter distinguishes them at zero risk.
