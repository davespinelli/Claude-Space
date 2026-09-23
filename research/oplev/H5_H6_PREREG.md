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
