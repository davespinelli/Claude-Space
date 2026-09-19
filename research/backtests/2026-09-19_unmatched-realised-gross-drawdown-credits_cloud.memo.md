# MEMO — idea 1656 (lane cloud, 2026-09-19): the record's drawdown credits are INFLATED, not FABRICATED — and an incidental KEEP-4b candidate whose CAGR is ABOVE SPY

1. **WHAT WAS TESTED.** Idea 1649 found a +1.02 pp MaxDD credit REVERSE to −0.28 pp at matched realised gross, and its G11 showed a constant de-gross moves |dSharpe| ≤ 0.0004 while moving MaxDD by up to 6.9 pp. The strong reading — *every* committed drawdown credit is an exposure claim wearing a device's name — is testable. **Part A** censuses the committed record; **Part B** re-prices five device families against two comparands: UNMATCHED (equal-weight at the same TARGET gross, the record's convention) and MATCHED (equal-weight at the constant gross whose REALISED mean equals the device's own). 3 panels × 5 families × 3 gross rungs × 4 cost rungs = **216 grid cells and 180 paired contrasts, every one published**. ONE tuned dial (gross `g`); family thresholds are the record's own live values (band 0.03, maxvol 0.60, N=20, vol target 0.15). Cost axis derived EXACTLY off the c=0 run (G5 = 0.000e+00).
2. **PART A — THE CENSUS IS DAMNING.** **149 of 2,540** committed MaxDD contrast sites (**5.87%**) name a realised-gross match; **2,391 (94.13%) do not.** By corpus: memos **18 / 1,242 (1.45%)**, CHANGELOG.md **0 / 48 (0.00%)**, LEADERBOARD.md **131 / 1,250 (10.48%)**. All 2,391 unmatched sites are published verbatim (first 2,000 in `.unmatched_sites.csv`).
3. **PART B — THE STRONG HYPOTHESIS IS KILLED.** MaxDD shallower than the UNMATCHED comparand in **174 of 180** cells (mean **+9.67 pp**); shallower than the MATCHED twin in **174 of 180** (mean **+5.06 pp**). **0 of 174 credits REVERSE sign.** Not one of the 173 credits ≥ 1 pp falls below 1 pp on matching. 1649's reversal is a small-credit special case, not the rule.
4. **WHAT MATCHING DOES DO: IT HALVES THEM.** Mean |dMaxDD shift| **4.61 pp**, max **18.32 pp** (SMALL/MA200 g=1.00). Fraction of the credit erased, by family: **BAND 60.6%**, **MA200 61.0%**, **VOLTGT 26.9%**, **MAXVOL 22.0%**, **TOPN −0.0%** (TOPN is fully invested, realised gross = target, so matching is a no-op — the run's internal control, and it lands at 0.000).
5. **THE SHARPE HALF OF 1649's G11 GENERALISES EXACTLY.** Mean |dSharpe shift on matching| **0.0004**, max **0.0018**; OOS **0.0005**. Over 180 contrasts on three panels, a constant de-gross is Sharpe-invariant to four decimal places and MaxDD-decisive. **A committed Sharpe claim needs no gross match; a committed MaxDD claim needs one and 94.13% of them do not have one.**
6. **AND THE MIS-QUOTING CHANGES DECISIONS, WHICH IS THE PART THAT COSTS MONEY.** Two rule-8 choosers that differ only in which comparand they price the DD credit against — `C_DDCREDIT_UNMATCHED` and `C_DDCREDIT_MATCHED` — **pick different arms in 11 of 12 (panel, cost) cells**, and clear 4b OOS **5 of 12** vs **0 of 12**. Sign-preservation is not decision-preservation.
7. **INCIDENTAL, AND RULE-8 LEGITIMATE: VOLTGT g = 1.00 CLEARS 4b FULL *AND* OOS ON TWO PANELS.** Equal-weight every priced name, scaled so the sleeve's trailing 20d vol hits 15%, capped at 100% gross; weekly, 10 bps. **U56 FULL 15.27% / 1.2075 / −19.29%**, halves **1.2808 / 1.1411** vs SPY 0.9570 / 0.8249; **OOS 15.68% / 1.2327 / −19.29%** vs SPY OOS 15.26% / 0.8737 / −33.72% and the live book's 9.46% / 1.2766 / −12.05%. **B136 FULL 15.45% / 1.2013 / −18.33%**, halves 1.3340 / 1.0730; **OOS 15.02% / 1.1899 / −18.33%** vs the live book's 7.85% / 1.1017 / −12.24%. Rule 8: `C_SHARPE` and `C_CALMAR`, fitted on rows ≤ 2016-12-31 only, **pick it on both panels**; 4b OOS PASS at 0/10/25 bps on U56 and at **all four cost rungs on B136**. Turnover 1.9–2.0x/yr. **Its CAGR is ABOVE SPY on both panels** — unlike the 2026-09-19 static-mix 4b passer, which sits 3.84 pp below.
8. **AND IT DIES ON SMALL.** SMALL FULL 8.09% / 0.6091 / −30.74%, halves **0.9761 / 0.3143**, OOS 4.85% / 0.3888 — 4b FAIL at every cost rung. Two of three panels is not three. It also fails path **4a** everywhere (−19.29% vs the live book's −12.05%): this is a growth book, not a drawdown book.
9. **LIMITS — AND ONE THAT BARS ENACTMENT.** VOLTGT's **vol target 0.15 and 20-day window were INHERITED from the record, not laddered under rule 8 here**; only `g` was. Until those two dials are walk-forwarded, the candidate is **KEEP-4b conditional**, filed as idea 1678. Survivorship (rule 9): U56/B136/SMALL are **current-constituent** lists, so every absolute level — the 4b pass included — is an **UPPER BOUND**; the matched-minus-unmatched contrast is same-names/same-days and first-order immune. SMALL additionally drops 54 tickers with `max_1d_move ≥ 1.0` (665 tradable). The census is a **line-level regex**, so a site is a line, not a claim, and it counts neither claims whose match is stated one line away nor the difference between "named" and "actually performed".
10. **NOTHING IS ENACTED.** PROTOCOL rule 6 reserves enactment for the Sunday review; RULES.md, scan.py, bot.py and baseline.py are untouched by this run.

## Exact RULES wording if the Sunday review adopts the 4b candidate (replaces clauses 1-3 wholesale)

> **Clause 1 (universe).** Every instrument in `research/universe.json` priced that day, excluding
> `BTC-USD` and `ETH-USD`.
>
> **Clause 2 (equity leg).** Form the equal-weighted sleeve over every clause-1 instrument priced
> that day. **No trend gate, no ranking, no volatility filter.**
>
> **Clause 3 (exposure).** Let `rv(t)` be the annualised standard deviation of that sleeve's last
> **20** daily returns, computed from closes up to and including day `t`. Hold the sleeve at
> `k(t) = min(0.15 / rv(t), 1.00)` of NAV, the remainder in 0% cash. Never levered, never shorted.
> Rebalance weekly on the last trading day of the week, executed at the next close.
>
> **Clause 4 (costs).** 10 bps per unit of turnover.
>
> The single dial laddered under rule 8 is the 1.00 gross cap. **The 0.15 target and the 20-day
> window are inherited, not walk-forwarded — clause 3 may not be enacted until idea 1678 ladders
> them on 2009-2016 rows only.**
