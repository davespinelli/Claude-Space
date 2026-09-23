# Industry nowcast pilot: US casinos. Pre-registration

Written 2026-09-23, before any data was collected. Nothing below may change once the first announcement return is computed. Anything forced by the data goes in a "Deviations" section, written BEFORE returns are computed.

## Idea

State gaming regulators publish each casino's revenue every month, usually 2-4 weeks after month-end. Operators report their quarter about 4-6 weeks after quarter-end. So by the time a company reports, the state data already show most of its quarter.

Casinos carry high fixed costs, so a revenue change flows through to earnings at a much higher rate. If we nowcast revenue from state data and push it through each company's own flow-through rate, do we know the earnings news before the market does?

## Build (before any return is computed)

1. **Monthly property data.** Monthly gross gaming revenue for every casino property in every state that publishes property-level or operator-level monthly figures, as far back as the archives go (target 2014 on). Keep the publication date of each monthly report where it can be found; otherwise assume month-end plus 30 days.
2. **Ownership timeline.** Which listed company owned or managed each property, with start and end dates, from 10-K property lists and M&A 8-Ks. Include companies later acquired or delisted where prices exist, and list the ones excluded for lack of prices.
3. **Coverage.** A company-quarter qualifies only if its covered properties' GGR in the same quarter a year earlier was at least 60% of its reported gaming revenue that quarter (or of total revenue, if gaming revenue isn't split out).
4. **Quarterly financials, as first reported.** From SEC companyfacts: revenue, operating income, and D&A when tagged. EBITDA = operating income + D&A. Where D&A is missing, use operating income and say so.
5. **Flow-through (operating leverage).**
   - For each company-quarter, regress year-over-year change in EBITDA on year-over-year change in revenue, using only quarters reported before that quarter's announcement.
   - Minimum 8 quarters; otherwise use the industry median.
   - Shrink 50% toward the industry median to tame noisy single-company estimates.
6. **Nowcast.**
   - Revenue growth nowcast g = same-store YoY growth in summed covered GGR over the quarter's 3 months (only properties owned in both periods).
   - EBITDA nowcast = EBITDA a year ago + flow-through x (revenue a year ago x g).
   - Nowcast EBITDA growth versus a year ago.
7. **Announcement dates.** The 8-K Item 2.02 filing date. The announcement window runs from the close of the trading day before the filing date to the close of the trading day after it, so it covers releases before the open and after the close.

## Tests

**Primary (carries the verdict).**
- Signal: EBITDA acceleration nowcast = nowcast EBITDA YoY growth for quarter q minus the company's reported EBITDA YoY growth for quarter q-1. The latter is the naive "market expects more of the same" baseline.
- Outcome: announcement abnormal return = the company's return over the window minus SPY's over the same window.
- Statistic: pooled regression of the outcome on the signal, with signals winsorised at the 5th/95th percentile and standardised by their full-sample SD. The t-statistic is clustered by calendar quarter.
- **Yes** only if the slope t >= 2.0 **and** the slope is positive in both halves of the sample by date. Otherwise **No**.

**Secondary (reported, no verdict).**
- Pre-announcement drift: the same regression, with the return running from the publication date of the quarter's last monthly state report (or quarter-end + 30 days) to the close before the announcement. This shows whether the market prices the state data before the report.
- Revenue-only version: revenue acceleration nowcast instead of EBITDA, to see whether the operating-leverage step adds anything.
- Versus analyst estimates: if an EPS-estimate history can be obtained without new paid data (for example Alpha Vantage EARNINGS via GitHub Actions), test whether the nowcast predicts the sign of the EPS surprise (hit rate against 50%, binomial p). If the data aren't available, say "not run".
- Small caps (< $2B market cap at announcement) versus larger, since analyst coverage is thinner there.

**Accuracy checks (no verdict; they show whether the machine works).**
- Correlation of nowcast revenue growth with reported revenue growth.
- Correlation of nowcast EBITDA growth with reported EBITDA growth.
- Mean absolute error of each.

## Reporting

A RESULTS.md in the style of research/oplev/RESULTS.md:
- plain-English answer first;
- sample sizes (companies, company-quarters, states, years);
- the accuracy checks;
- primary and secondary results;
- the names and dates excluded and why;
- a "For picking stocks" line.

Research only; no trading.
