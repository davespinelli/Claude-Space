# MEMO — idea 579's 4b passer: U56 TOP10 monthly + VT(0.10). **Recommendation: PARK.**

1. **What it is.** Idea 311's pre-registered TOP10 book on `research/universe.json`, rebalanced
   monthly at gross 0.75, with a 10% vol-target overlay that scales the whole book DOWN only.
2. **How it was chosen (rule 8).** Clause family and dial picked on 2009-01-13..2016-12-31 by
   largest in-sample matched-MaxDD edge over cash among cells clearing all five IS 4b legs;
   2017-01-01..2026-09-04 read exactly once. Rebuild check |dIS_Sharpe| = 0.00e+00.
3. **Full sample:** CAGR **13.00%**, Sharpe **1.157**, MaxDD **−18.77%**, H1/H2 **1.369 / 0.961**,
   turnover 4.39x/yr, 10 bps costs, weights decided at close t applied at t+1.
4. **Out of sample:** CAGR **11.40%**, Sharpe **1.010**, MaxDD **−18.77%** vs SPY 15.45% / 0.882 /
   −33.72% and RULES v2 (U56) 9.53% / 1.285 / −12.05%.
5. **PROTOCOL 4b: PASSES** on the full sample and on the OOS window — H1 1.369 > 0.957,
   H2 0.961 > 0.834, OOS 1.010 > 0.882, MaxDD −18.77% ≥ −20.23%, CAGR 13.00% ≥ 10.66%.
6. **PROTOCOL 4a: FAILS.** It loses to the live book on Sharpe in both halves and out of sample
   (1.010 vs 1.285 OOS), so it cannot be promoted on the beat-the-book path.
7. **Why PARK and not KEEP (a).** The walk-forward selector searched 564 IS cells over FOUR axes
   (form x cadence x family x dial); only two of them were declared tuned under rule 4.
8. **Why PARK and not KEEP (b).** Its own selection statistic reverses: the matched-MaxDD edge
   over cash runs **IS +3.409 pp → OOS −1.901 pp**. Out of sample, de-grossing the same parent
   to the same MaxDD would have earned 1.90 pp/yr MORE — the clause is not what earned the pass.
9. **Why PARK and not KEEP (c).** It is a dial placement: on this parent's own VT ladder 4b
   passes at 0.10 and 0.12 and fails at 0.06, 0.08, 0.15 and 0.20 — 2 of 6 points.
10. **Exact RULES wording, if a future Sunday review ever promotes it.** No rules change is
    proposed now; RULES.md, scan.py, bot.py and baseline.py are unmodified.

> **1. UNIVERSE.** The names in `research/universe.json`, priced that day.
> **2. SCORE.** For each name, the mean of the cross-sectional percentile ranks of three
> returns: `px[t−21]/px[t−252] − 1`, `px[t]/px[t−126] − 1`, and `px[t]/px[t−63] − 1`. No
> volatility scaling and no 200-day filter enter the score.
> **3. BOOK.** Hold the top 10 names by that score, equal weight, at a gross of 0.75 of NAV.
> **4. VOL TARGET.** Multiply the whole book by `min(1, 0.10 / rv)`, where `rv` is the
> annualised 60-day standard deviation of the unscaled book's own daily returns, lagged one
> day. This scales gross DOWN only; the de-grossed remainder is held in CASH at 0% and is
> never re-spread across names.
> **5. CADENCE.** Rebalance on the last trading day of each calendar month. Weights are decided
> at that close and applied at the next close. No shorting, no leverage.

**Survivorship:** `research/universe.json` is a list fixed as of today, so the full-sample level
is biased up relative to what was investable in 2009.
