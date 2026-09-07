# Idea 324 — does-the-IS-CHOOSER-ever-beat-a-coin-across-BOOKS (lane C, 2026-09-07)

**ANSWERED / KILL as a book. Rules unchanged; no KEEP (4a 0/4, 4b 0/4 composites).**
**But the answer to the question is YES-with-conditions, and it is the opposite of idea 47's
reading: pooled over the record's dials the rule-8 IS chooser beats a coin, weakly.**

## What was run
Six of the record's own dial families rebuilt as live grids — N (top-n, 7 arms), F (fraction
of eligibles, 6), B (RULES v2 band, 7), V (vol20 eligibility cap, 6), G (breadth-quintile cash
gate, 5), R (rebalance frequency, 4) = **35 arms** — on **U56 / B136 / SMALL439**, all at
10 bps and t+1, 105 backtests, every arm in `.grid.csv`. The two tuned parameters are the
*chooser* itself, not any book: **chooser statistic ∈ {IS_Sharpe, IS_CAGR, IS_4b}** ×
**IS/OOS split ∈ {2014, 2016, 2018}**. 6 × 3 × 3 × 3 = **162 census cells, all reported**
(`.census.csv`). "A coin" = the **arm-average**: the expected OOS Sharpe of picking an arm at
random from the same grid. Coin expectation for the pick's OOS percentile rank is 0.500.

## The census (162 cells)
| statistic | result | coin |
|---|---|---|
| IS pick beats the arm-mean OOS Sharpe | **113/162 (69.8%)** | 50.0% |
| mean OOS percentile rank of the pick | **0.611** (median 0.667) | 0.500 |
| IS pick *is* the OOS-best arm | **48/162** | 28.9 |
| mean OOS Sharpe, pick − arm-mean | **+0.049** (median +0.045) | 0.000 |
| mean effect size (pick − mean)/sd(arms) | **+0.267** | 0.000 (OOS-best sits at +1.115) |
| mean Spearman(IS Sharpe, OOS Sharpe), 54 orderings | **+0.410** | 0.000 |

At **rule 8's own statistic** (IS_Sharpe, 54 orderings): beats the arm-mean **38/54 (70.4%),
sign-test p = 0.0038**, mean z +0.271. The choice of statistic is immaterial — IS_Sharpe and
IS_4b are identical in aggregate (the 4b bars were unsatisfiable in 43/54 IS windows and the
chooser fell back), IS_CAGR differs by 0.013 of z.

## Three qualifications that matter more than the headline
1. **It is one panel.** Per panel at IS_Sharpe: **B136 15/18, mean z +0.735; U56 12/18, +0.065;
   SMALL439 11/18, +0.014.** Two of three panels are a coin to two decimals. The pooled
   significance rides on B136.
2. **It is not significant at a single clean split.** Splits 2014/2016/2018 reuse overlapping
   data. At PROTOCOL's own 2016 split alone: **12/18, p = 0.238**, mean z +0.173.
3. **It is one quarter of what is there.** The pick averages +0.27 sd of the arm spread while
   the OOS-best sits at +1.115 sd; mean regret vs the OOS-best is 0.080 Sharpe. And the edge is
   concentrated in families where **one arm dominates in both windows** — G (+0.41 z, ρ +0.57)
   and V (+0.34, ρ +0.49), where the chooser mostly learns "the gate hurts" and "don't cap vol
   at 0.25". Where arms are genuinely close it is a coin: family **B** (band) is 5/9, ρ +0.18,
   and its per-ordering ρ runs −0.643 to +1.000 — sign-unstable.

## Does the arm-by-arm edge survive into a book? No.
At PROTOCOL's setting (IS_Sharpe, split 2016), CHOOSER = equal blend of the 6 IS-picked arms;
COIN = equal blend of all 35. OOS 2017+:

| panel | book | OOS CAGR | OOS Sharpe | OOS MaxDD | vs COIN |
|---|---|---|---|---|---|
| U56 | CHOOSER | 10.30% | 1.058 | −16.03% | **−0.051 Sharpe** |
| U56 | COIN | 9.73% | 1.109 | −14.22% | — |
| B136 | CHOOSER | 8.54% | 0.892 | −16.22% | **+0.024 Sharpe** |
| B136 | COIN | 7.62% | 0.868 | −15.20% | — |
| — | RULES v2 | 9.53% / 7.98% | 1.285 / 1.119 | −12.05% / −12.24% | |
| — | SPY | 15.45% | 0.882 | −33.72% | |

Full sample (`compare`, vs RULES v2 and SPY; CHOOSER's IS half is contaminated by construction):
CHOOSER-U56 9.8%/1.04/−16.0% (H 1.11/0.98), COIN-U56 8.9%/1.05/−14.2% (1.08/1.02),
CHOOSER-B136 9.3%/0.97/−16.2% (1.17/0.79), COIN-B136 8.2%/0.94/−15.2% (1.12/0.77);
RULES v2 1.21 (1.23/1.19) on U56 and 1.11 (1.23/0.98) on B136; SPY 15.2%/0.89/−33.7%
(0.96/0.83). **4a 0/4** (every composite loses both half-Sharpes to RULES v2 and has a worse
MaxDD). **4b 0/4** (every composite fails CAGR ≥ 70% of SPY's 15.2% — 8–10% is 54–65% — and
the B136 pair also fails H2 vs SPY). Blending 6 or 35 momentum books is a diversified,
low-return, low-drawdown thing; it is not capital-worthy on either path.

## Verdict
**KILL** as a book (0/4 on both KEEP paths). **ANSWERED** as a question: rule 8's IS chooser is
weakly informative, not anti-informative — idea 47's B136 anti-correlation was a
four-book, one-family accident, not the record's general case. But at +0.27 sd of arm spread,
significant only when three overlapping splits are pooled, driven by one panel and by dials
whose ordering is stable in both windows, **rule 8 should be read as a weak filter that
removes clearly-bad arms, not as evidence that a chosen parameter is the right one.** Every
"chosen on 2009–2016" claim in this record carries ≈0.08 Sharpe of expected regret against
the OOS-best of its own grid.

Not a PROTOCOL change (rule 6: Sunday review only). Suggested wording for that review, if it
wants one: *rule 8 selects, it does not validate; report the arm-average alongside the pick.*

**SURVIVORSHIP:** U56, B136 and SMALL439 are current-constituent lists, so all absolute CAGRs
are optimistic. The census statistic is a within-panel, within-family comparison of a pick
against its own arm-average and is far less exposed than the levels are.

Files: `.py`, `.grid.csv` (105 arms), `.census.csv` (162 cells), `.composites.csv`,
`.console.txt`.
