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

## Deviations

Written 2026-09-23, after the state, ownership and SEC data were collected and the nowcast panel was built, and BEFORE any announcement or drift return was computed. Everything above is unchanged.

**Forced by the data**

1. **Two samples; only the first carries the verdict.** Mississippi, Colorado and Nevada publish revenue only by region, town or reporting area, not by casino. The verdict sample ("property sample") uses property- or operator-level state data only, exactly as pre-registered. A secondary "region sample" adds those three states, imputing each casino's monthly GGR as its share of its unit's slot win and table win: Mississippi from the Gaming Commission's per-casino slot and table counts; Nevada and Colorado from the casino's slot and table counts in its owner's 10-K property table (nearest fiscal year) over the regulator's unit counts; where no count exists, the unit's GGR divided by the number of casinos reporting. The region sample gets the same tests but no verdict. It is the only way Monarch, Red Rock and most of Century and Full House enter.
2. **Point-in-time state data.** Some monthly reports come out after the company's release, so a nowcast built from all three months would use information the market did not have. The nowcast therefore uses, for each property, only months whose report was published before the 8-K filing date (actual date where found, otherwise month-end + 30 days as in build step 1). A company-quarter qualifies only if the months used cover at least two-thirds of its year-ago covered GGR. The all-three-months version is reported as a sensitivity.
3. **Prices.** Yahoo has no usable daily history for Isle of Capri, Pinnacle, Tropicana Entertainment, Dover Downs, Empire Resorts, MTR Gaming, Affinity, Caesars Acquisition, the pre-2020 Caesars Entertainment Corp (Yahoo's CZR history is Eldorado's), Golden Entertainment (taken private April 2026; Yahoo dropped the symbol) or Bally's/Twin River before 2024-12-06. Their company-quarters stay in the accuracy checks but not in the return tests. Stooq blocks scripted access with a browser check, which was not bypassed.
4. **Measure breaks.** Iowa's AGR excludes promotional play from 2026-07 (about -13% mechanically); Iowa months from 2026-07 are not compared with 2025. West Virginia racetrack data exist only from 2018-07, New York only to 2025-09 (the regulator's site blocks scripted access; Internet Archive copies end there).
5. **VLT states.** Rhode Island and New York report total net terminal income, of which the operator books only its statutory share as revenue, so coverage for Bally's/Twin River and Empire Resorts exceeds what the operator reports. The pre-registered coverage formula is applied literally; this is flagged in the results.
6. **Missing XBRL.** Monarch's Q2 2026 10-Q is missing from the companyfacts API; its values were read from the filing's own XBRL instance.

**Implementation choices the text did not pin down**

7. Growth rates use the absolute value of the base, (new - old) / |old|, so a smaller loss counts as growth; undefined when the base is zero.
8. Covered properties are those whose revenue is in the company's reported revenue: owned or leased-and-operated, consolidated, not in discontinued operations. Equity-method joint ventures (e.g. Borgata for Boyd 2014-16, Hollywood Kansas Speedway for Penn) and management contracts are excluded. "Owned in both periods" means held from the first day of the year-ago quarter to the last day of the current quarter.
9. Coverage denominator (reported gaming revenue a year earlier): us-gaap CasinoRevenue when tagged without dimensions (mostly through 2017, before promotional allowances); otherwise the casino/gaming line of the revenue disaggregation in the 10-Q/10-K (dimensional XBRL, read from the filing instances; 2018 on); total revenue only when neither exists.
10. First-reported financials: among candidate revenue tags, only values from the first filing that reported the quarter are eligible, and the one closest to operating income + total operating costs (net revenue by identity) is taken. Q2/Q3 come from year-to-date differences when no 3-month value was tagged; Q4 = FY - (Q1 + Q2 + Q3); Bally's Q1 2025 predecessor and successor stubs are summed.
11. Announcement date: the first 8-K with Item 2.02 filed within 100 days after quarter-end; if the 10-Q/10-K for the quarter was filed earlier, or no Item 2.02 exists (Tropicana Entertainment, Empire Resorts), that filing's date.
12. Fiscal quarters not ending at a month-end (Isle of Capri; Lakes/Golden before 2015) use the three calendar months ending in the month that holds most of the quarter's last weeks.
13. Industry median flow-through: the median of the own-company slopes of all casino companies in the SEC panel (priced or not, including MGM and Wynn) with at least 8 year-over-year pairs reported before the announcement.
14. Analyst estimates: Alpha Vantage is not available locally, but Yahoo's earnings calendar (via yfinance) gives a free consensus-EPS history, so the test is run on it. It is Yahoo's current record, not a point-in-time snapshot, on an adjusted-EPS basis.
15. Drift window: from the close of the trading day before the latest publication date used in the nowcast to the close of the trading day before the filing date (the start of the announcement window); dropped if empty.
16. Market cap at announcement: latest cover-page shares outstanding filed before the announcement times the split-unadjusted close on the day before the window.
17. Signals are winsorised and standardised once on each test sample; the halves and the small-cap/larger splits use those same standardised values. Halves split the sample at its median announcement date.
