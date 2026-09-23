# H5 and H6 pre-registration: can we see operating leverage kicking in before the market?

Written 2026-09-23, before any H5 or H6 number was computed.

Why these tests exist: H2b found the mechanism is real in the accounts (high fixed costs plus accelerating sales, then margins jump the next year, t = 4.46) but not in returns. H2b used annual data 4-6 months old. These tests ask whether acting sooner, or on a leading indicator, gets ahead of the price. Nothing below may change once the first H5 or H6 return is computed.

## Common rules

- Universe:
  - same as H1-H3: non-financial, priced, >= $50M at formation;
  - same `clean_returns` rule;
  - same delisting scenarios (-30% / +15%) with missing shares reported.
- Fundamentals: quarterly values **as first reported**, taken from SEC companyfacts, using the value from the filing that first reported that period (its own accession and filed date). Restated later values are never used. Fixed-cost share is the H2a definition from the latest annual data available before the filing date.
- Timing:
  - A company enters the signal at the first month-end after the filing date of the 10-Q or 10-K that triggers it.
  - It is held for the next 3 months, equal-weighted.
  - Each month holds the average of the three overlapping monthly cohorts (Jegadeesh-Titman).
- Control: all other companies in the universe that filed a 10-Q or 10-K in the same month, held the same way.
- Headline statistic: the equal-weighted monthly spread (signal minus control). The verdict uses the Newey-West (6 lags) t-statistic because cohorts overlap; the plain t is reported beside it.
- Bar: **Yes** only if NW t >= 2.0. Otherwise **No**.
- Period: every month from the first month the data allows through the latest complete month.

## H5 (primary): the quarterly report, acted on the next month

- Sales acceleration: year-over-year revenue growth of the just-reported quarter minus the same measure for the previous quarter.
- Signal: at a filing, the company is in the top 30% of that year's universe on fixed-cost share **and** in the top 30% of that month's filers on sales acceleration, with acceleration > 0.
- Test as in the common rules. Answer Yes only if NW t >= 2.0.
- Fundamental check, no verdict: the next reported quarter's year-over-year change in operating margin, signal versus control. It must be positive for the mechanism to be present at quarterly speed.

## H6 (secondary): backlog running ahead of sales

- Leading indicator: us-gaap:RevenueRemainingPerformanceObligation (contracted revenue not yet recognised; reported since ASC 606, so tests start when year-over-year values exist).
- Signal: RPO year-over-year growth minus revenue year-over-year growth > 0 and in the top 30% of that month's RPO reporters, and fixed-cost share in the top 30% of the year's universe.
- Control: other RPO reporters filing that month.
- Same test and bar.
- Report how many companies report RPO per year. If fewer than 30 signal companies exist in most months, say so in the answer; it does not change the verdict rule.

## Robustness reported (does not change the verdict)

- First and second half of the period.
- Small caps (< $2B) and large caps separately.
- Matched version within size tercile x 2-digit SIC.
- Value-weighted.
- 1-month and 6-month holds.
- Top group after 0.5% a year of costs, against the equal-weighted universe, IWM and SPY.
- Signal counts per month.

## Not tested here (noted for later)

- Whether the H5 signal predicts beating analysts' earnings estimates. That needs the Alpha Vantage earnings-surprise history, whose key lives only in GitHub Actions secrets.
- Monthly industry data (airline traffic, gaming revenue, rail carloads, chip billings) as a nowcast.

## Deviations

Written 2026-09-23, after the quarterly fundamentals were built and the signals classified, and **before any H5 or H6 portfolio return was computed**. Nothing above this section was changed. Where the text above could not be followed literally, or left a choice open, the code in `quarterly/` does the following.

1. **Universe per formation month.** Current SIC not 6000-6999 or 4900-4999, not a foreign private issuer, latest fiscal-year revenue (first reported, filed before the formation month-end, fiscal year ended within 550 days) > $10M, latest total assets > 0, a Yahoo price at the formation month-end and market cap >= $50M there. Market cap = month-end close x the most recent share count filed before that date (cover-page count, else balance-sheet count, else weighted-average count), put on Yahoo's split basis and checked with build_panel.py's rules (3x agreement between sources, market cap / max(revenue, assets) within 0.002-100). Tickers, historical-ticker checks (public-float band, clash with the symbol's current holder) and the per-month duplicate rule follow build_panel.py; the clash rule uses the annual panel's filer lists by formation year. Candidate companies are the annual study's set (revenue > $10M and assets > 0 in some fiscal year 2010-2024); a company that first crossed $10M in fiscal 2025 is not covered.
2. **Month-end** means the last NYSE trading day. A filing dated on or after that day enters at the next month-end, because a filing made after the close of the last trading day cannot be bought at that close.
3. **Triggers** are original 10-Q and 10-K filings only (no amendments, no 10-KT/10-QT transition reports). If one company has two triggers entering the same month, the one covering the later period is used.
4. **First-reported values** come from the first 10-K/10-Q-family filing (an amendment counts only if it was first) that reported the exact period; S-1s and 8-Ks are not used. Revenue: the first tag present in that filing in build_panel.py's order (Revenues, RevenueFromContractWithCustomerExcludingAssessedTax, SalesRevenueNet, RevenueFromContractWithCustomerIncludingAssessedTax), else goods + services. A quarter is a 75-125 day period (covers 12-, 13-, 14- and 16-week quarters). **Q4** is whichever becomes available first: a directly reported 3-month value; FY (first reported in the 10-K) minus the first-reported 9-month year-to-date value from the Q3 10-Q (used rather than the sum of three separately first-reported quarters, because it is one consistent number and absorbs mid-year reclassifications); or, if no 9-month value exists, FY minus the three first-reported quarters. A derived Q4 revenue <= 0 is discarded. The year-ago quarter is the one ending 350-380 days earlier; the previous quarter is the one ending 70-125 days earlier. Growth needs positive revenue in both quarters.
5. **Fixed-cost share "from the latest annual data available before the filing date"**: annual first-reported revenue and operating income from 10-Ks filed strictly before the filing date; the latest fiscal year plus those ending within about four years before it (five fiscal years), at least four needed; otherwise exactly H2a.
6. **"Top 30% of that year's universe" on fixed-cost share**: 70th percentile of fixed-cost share across the universe (rule 1) on the last trading day of June of year t, with fixed-cost share as of that day, applied to cohorts formed July t to June t+1 (the H1-H3 formation-year convention). The June 2026 breakpoint is used for July 2026. There is no usable June 2010 breakpoint, so signals start with the July 2011 cohort; until 2013 only companies with several years of XBRL history (mostly large ones) have a fixed-cost share.
7. **"Top 30% of that month's filers"** (acceleration for H5, RPO-minus-revenue growth for H6): 70th percentile among the month's universe filers (H6: universe RPO reporters) with the measure defined; a value equal to the breakpoint is not in the top, as in run_tests.py. No breakpoint, hence no signal, when fewer than 10 such filers exist (this only bites before fixed-cost shares exist). Unpriced ("missing") companies are classified with the priced breakpoints, as in H1-H3.
8. **Controls.** H5: literally every other universe company that filed that month, including those whose acceleration or fixed-cost share cannot be computed. A control limited to companies where the signal could be evaluated is reported as an extra line, not used for the verdict. H6: every other universe company whose filing reports an RPO value at its quarter end.
9. **Holding.** A cohort formed at month-end M holds months M+1 to M+3. Each cohort's return in a month is the simple average of its members' returns that month (equal weights reset monthly, as run_tests.py); the portfolio's return is the simple average of the cohorts formed in the previous three months that have returns. Value-weighted: formation market cap grown by each stock's own return within the hold (as run_tests.py's Book).
10. **Returns** come from the annual study's Yahoo monthly cache (`../cache/prices/monthly_long.parquet`, read-only), computed exactly as build_panel.py does and cleaned with run_tests.py's `clean_returns`, because `returns.parquet` holds only the stocks the annual study held; the result is checked cell by cell against `returns.parquet`. Returns run through August 2026, the latest complete month.
11. **Delisting scenarios for 3-month holds.** A held stock whose price series stops before the end of its hold earns -30% (or +15%) in the month after its last price, as in H1-H3. A missing company (passes the filters and filed, but has no price at formation and is not "not yet listed") earns the H1-H3 assumption at the same monthly rate, (1 - 30%)^(1/12) - 1 (or (1 + 15%)^(1/12) - 1) for each month held, rather than the full -30% in three months. Reported for all missing companies and for those whose last public float was >= $50M.
12. **Years won** are calendar years (the first and last are partial), because the portfolio is rebalanced monthly; the "first and second half" split the spread's months into two equal halves.
13. **Size split**: signal and control defined exactly as in the headline, then both limited to small (< $2B at formation) or large companies. **Matched version**: within each cohort, market-cap terciles of the test's own sample (universe filers for H5, RPO reporters for H6) crossed with current 2-digit SIC; each signal stock is compared with the average of the control stocks in its cell, and signal stocks without a control in their cell are dropped.
14. **Costs**: 0.5% a year deducted from the signal portfolio (0.5%/12 a month), compared with the equal-weighted universe (all universe filers, held the same way), IWM and SPY.
15. **H6 "fewer than 30 signal companies in most months"** is counted on the distinct companies held in the signal portfolio each month (across the three overlapping cohorts). Signal classification before any return showed a median near 28, so the H6 answer will carry that warning.
16. **Fundamental check**: the next reported quarter (ending 70-125 days after the signal quarter), its first-reported operating margin minus the first-reported margin of the same quarter a year earlier, median for signal versus control (universe members), overall and by calendar year. Pre-registered for H5; reported for H6 for information only.
17. **Extra lines, clearly labelled and not part of any verdict**: the evaluable-only control (rule 8) and raw Yahoo returns without the bad-print rule, as reported for H1-H3.
