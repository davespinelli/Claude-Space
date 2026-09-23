# Can we spot operating leverage kicking in before the market? Quarterly tests H5 and H6

*Generated 2026-09-23 by `research/oplev/quarterly/run_quarterly.py`. Signals are formed at each month-end from 10-Q and 10-K filings, using every number as the SEC filing first reported it. H5 returns run Aug 2011 to Aug 2026 (181 months); H6 May 2019 to Aug 2026 (88 months). Every number below is in `results_quarterly.json`. Pre-registration: `../H5_H6_PREREG.md`; its Deviations section was written before any H5 or H6 return was computed.*

## The short answer

| Test | Answer | Signal minus control, per year (equal-weighted) | Newey-West t | Plain t | Years signal won |
|---|---|---|---|---|---|
| H5. Fixed costs + sales acceleration, bought the month after each 10-Q/10-K | No | +0.5 points | 0.38 | 0.37 | 9 of 16 |
| H6. Backlog (RPO) growing faster than sales, fixed costs | No | +3.7 points | 1.22 | 0.93 | 5 of 8 |

"Signal minus control" is the difference between the two portfolios' compound annual returns. Each month holds three overlapping monthly cohorts, so the verdict uses the Newey-West t-statistic (6 lags) on the monthly return differences; 2.0 is the pre-registered bar. Years are calendar years; the first and last are partial. Benchmarks over H5's months: equal-weighted universe of filers 14.1% a year, IWM 10.5%, SPY 14.5%.

In one line each: **H5** No (+0.5 points a year, NW t = 0.38, 9 of 16 years); the margins do jump the next quarter (+1.33 points vs the control), but the price has already moved. **H6** No (+3.7 points a year, NW t = 1.22, 5 of 8 years), on a thin portfolio (median 28 stocks).

## Read this first

H2b (see `../RESULTS.md`) found that operating leverage is real in the accounts but not in returns when acted on with annual data four to six months old. These tests act on each 10-Q and 10-K at the first month-end after it is filed, using only numbers as first reported (never later restatements), so they ask whether the lag was the problem.

The missing-company problem of H1-H3 applies unchanged. The universe comes from every company that filed with the SEC at the time; companies later acquired or delisted usually have no Yahoo price and cannot be held. They are counted, placed in the signal or control group with their own filings, and re-run under the -30% and +15% assumptions in each test. Filings per calendar year (a company files about four times a year):

| Year | Universe filings (priced, >= $50M) | Missing: passes filters, no price | Missing share | Missing with float >= $50M | Not yet listed (excluded) |
|---|---|---|---|---|---|
| 2011 | 1,997 | 1,378 | 41% | 1,310 | 211 |
| 2012 | 4,020 | 5,716 | 59% | 3,834 | 611 |
| 2013 | 4,377 | 5,898 | 57% | 3,908 | 565 |
| 2014 | 4,590 | 5,591 | 55% | 3,804 | 478 |
| 2015 | 4,813 | 5,283 | 52% | 3,789 | 452 |
| 2016 | 4,915 | 4,690 | 49% | 3,476 | 423 |
| 2017 | 5,148 | 4,132 | 45% | 2,989 | 375 |
| 2018 | 5,488 | 3,733 | 40% | 2,748 | 311 |
| 2019 | 5,904 | 3,462 | 37% | 2,661 | 332 |
| 2020 | 6,185 | 2,939 | 32% | 2,235 | 263 |
| 2021 | 6,916 | 2,626 | 28% | 1,903 | 201 |
| 2022 | 7,661 | 2,621 | 25% | 2,078 | 202 |
| 2023 | 7,717 | 2,155 | 22% | 1,604 | 181 |
| 2024 | 7,865 | 1,369 | 15% | 1,015 | 140 |
| 2025 | 8,152 | 773 | 9% | 543 | 106 |
| 2026 | 4,595 | 152 | 3% | 89 | 38 |

2026 covers filings through July (held into August). In both tests the signal and control groups lose about the same share of companies (see each test), so the comparison between them is less exposed than the absolute returns.

## H5. The quarterly report, acted on the next month

**Question.** When a company whose costs are mostly fixed reports a quarter in which year-over-year sales growth sped up (top 30% of that month's filers, and faster than the quarter before), does buying at the first month-end after the filing and holding three months beat the other companies that filed that month?

**Answer: No.** The signal portfolio (high fixed costs, accelerating sales) did not reliably beat the other companies that filed that month (Newey-West t = 0.38, below the pre-registered bar of 2.0).

**Size of the effect (equal-weighted, the pre-registered headline).** The signal portfolio (high fixed costs, accelerating sales) returned 14.5% a year against 14.0% for the other companies that filed that month, a gap of +0.5 points a year (Aug 2011 to Aug 2026, 181 months). Monthly spread: Newey-West t 0.38, plain t 0.37. The signal was ahead in 9 of 16 calendar years. $10,000 would have become $77,494 in the signal portfolio and $72,068 in the control, before costs.

**How much to trust it.**

- First half (Aug 2011 to Jan 2019): +1.6 points a year (NW t = 0.68, t = 0.66; signal ahead in 6 of 9 years). Second half (Feb 2019 to Aug 2026): -0.5 points a year (NW t = -0.08, t = -0.08; signal ahead in 3 of 8 years).
- Small caps (< $2B): -0.1 points a year (NW t = 0.08, t = 0.08; signal ahead in 8 of 16 years). Large caps (>= $2B): +1.0 points a year (NW t = 0.66, t = 0.55; signal ahead in 12 of 16 years).
- Matched within size tercile x 2-digit SIC (each signal stock against the control stocks of the same size tercile and industry that month): -2.2 points a year (NW t = -0.87, t = -0.92; signal ahead in 7 of 16 years); 6,991 of 7,464 signal filings had a match.
- Value-weighted: +2.0 points a year (NW t = 0.77, t = 0.78; signal ahead in 9 of 16 years).
- Holding 1 month instead of 3: +0.6 points a year (NW t = 0.38, t = 0.33; signal ahead in 8 of 16 years). Holding 6 months: +3.3 points a year (NW t = 1.88, t = 1.88; signal ahead in 11 of 16 years).
- Missing companies: 37.1% of the would-be signal filings and 36.7% of the would-be control filings have no price (30.1% and 29.6% counting only public float >= $50M), so the two sides lose companies at about the same rate. If every missing company lost 30% a year: +0.4 points, NW t = 0.30 (float >= $50M only: +0.2 points, NW t = 0.21); if every missing company gained 15%: +1.1 points, NW t = 0.78 (+0.8 points, NW t = 0.56). The sign does not change across these assumptions, and none lifts the t-statistic to 2.
- Raw Yahoo returns, no bad-print rule: -0.5 points a year (NW t = -0.20, t = -0.21; signal ahead in 8 of 16 years). Most or all of the difference from the cleaned result is Chord Energy's November 2020 splice (+30,991%, in the control group; see Caveats).
- Extra, not pre-registered: control limited to companies where the signal could be computed at all: +0.5 points a year (NW t = 0.34, t = 0.35; signal ahead in 9 of 16 years).
- The signal portfolio after 0.5% a year of trading costs: 14.0% a year vs 14.1% for the equal-weighted universe of filers (-0.1 points, t = 0.03), 10.5% for IWM (+3.5 points, t = 1.60) and 14.5% for SPY (-0.5 points, t = 0.16).
- Signal counts: median 123 companies held in a month (min 5, max 243); 13 of 181 months held fewer than 30 (first Aug 2011, last Feb 2013); 1,326 distinct companies over the period; the control held a median 1,223. Monthly counts are in `results_quarterly.json`.

**Fundamental check (next reported quarter vs the same quarter a year earlier, first-reported numbers).**

| Group | Next quarter: change in operating margin (median, pts) | Next quarter: revenue growth (median) | Signal quarter: revenue growth (median) | Change in growth, next vs signal quarter (median, pts) | Filings (with a next quarter) |
|---|---|---|---|---|---|
| Signal | +1.48 | 11.1% | 14.3% | -1.7 | 7,464 (7,258) |
| Control | +0.16 | 6.0% | 5.9% | -0.2 | 83,658 (75,156) |

Signal minus control: +1.33 points of operating margin; the signal group was ahead in 13 of 16 calendar years (mean yearly gap +1.48 points, t = 2.72). The difference is positive, so the mechanism is present at quarterly speed.

**For picking stocks.** Acting fast on the quarterly report does not help. Operating leverage does kick in at quarterly speed: the signal companies' operating margins rose a median +1.48 points year over year in the next quarter, against +0.16 for the other filers. But the stocks did no better than the other filers held the same way (+0.5 points a year), and against companies of the same size in the same industry they did worse (-2.2 points). By the first month-end after the 10-Q, the price already reflects the acceleration. Do not buy a fixed-cost company because its latest quarter showed sales speeding up.

## H6. Backlog running ahead of sales

**Question.** When a high-fixed-cost company's remaining performance obligations (contracted revenue not yet recognised, reported since ASC 606) grow faster than its sales, does the stock beat other companies reporting RPO that month?

**Answer: No.** The signal portfolio (RPO growth well ahead of sales growth, high fixed costs) did not reliably beat the other RPO reporters that filed that month (Newey-West t = 1.22, below the pre-registered bar of 2.0). **Fewer than 30 signal companies were held in most months** (49 of 88; median 28), as the pre-registration asked to flag.

**Size of the effect (equal-weighted, the pre-registered headline).** The signal portfolio (RPO growth well ahead of sales growth, high fixed costs) returned 21.7% a year against 17.9% for the other RPO reporters that filed that month, a gap of +3.7 points a year (May 2019 to Aug 2026, 88 months). Monthly spread: Newey-West t 1.22, plain t 0.93. The signal was ahead in 5 of 8 calendar years. $10,000 would have become $42,113 in the signal portfolio and $33,515 in the control, before costs.

**How much to trust it.**

- First half (May 2019 to Dec 2022): +5.1 points a year (NW t = 1.35, t = 0.97; signal ahead in 3 of 4 years). Second half (Jan 2023 to Aug 2026): +2.2 points a year (NW t = 0.40, t = 0.33; signal ahead in 2 of 4 years).
- Small caps (< $2B): +4.7 points a year (NW t = 0.63, t = 0.55; signal ahead in 5 of 8 years). Large caps (>= $2B): +0.1 points a year (NW t = 0.33, t = 0.29; signal ahead in 5 of 8 years).
- Matched within size tercile x 2-digit SIC (each signal stock against the control stocks of the same size tercile and industry that month): -0.2 points a year (NW t = 0.13, t = 0.14; signal ahead in 5 of 8 years); 691 of 825 signal filings had a match.
- Value-weighted: +2.8 points a year (NW t = 0.63, t = 0.56; signal ahead in 5 of 8 years).
- Holding 1 month instead of 3: -7.4 points a year (NW t = -1.08, t = -0.80; signal ahead in 2 of 8 years). Holding 6 months: +4.2 points a year (NW t = 1.58, t = 1.21; signal ahead in 4 of 8 years).
- Missing companies: 20.9% of the would-be signal filings and 23.0% of the would-be control filings have no price (17.7% and 20.4% counting only public float >= $50M), so the two sides lose companies at about the same rate. If every missing company lost 30% a year: +0.6 points, NW t = 0.31 (float >= $50M only: +1.8 points, NW t = 0.59); if every missing company gained 15%: +1.8 points, NW t = 0.65 (+2.9 points, NW t = 0.91). The sign does not change across these assumptions, and none lifts the t-statistic to 2.
- Raw Yahoo returns, no bad-print rule: -1.6 points a year (NW t = -0.32, t = -0.30; signal ahead in 5 of 8 years). Most or all of the difference from the cleaned result is Chord Energy's November 2020 splice (+30,991%, in the control group; see Caveats).
- Extra, not pre-registered: control limited to companies where the signal could be computed at all: +4.3 points a year (NW t = 1.44, t = 1.05; signal ahead in 6 of 8 years).
- The signal portfolio after 0.5% a year of trading costs: 21.1% a year vs 13.3% for the equal-weighted universe of filers (+7.8 points, t = 1.68), 10.2% for IWM (+10.9 points, t = 2.18) and 15.6% for SPY (+5.4 points, t = 1.16).
- Signal counts: median 28 companies held in a month (min 2, max 41); 49 of 88 months held fewer than 30 (first May 2019, last Mar 2026); 215 distinct companies over the period; the control held a median 388. Monthly counts are in `results_quarterly.json`.

**Fundamental check (next reported quarter vs the same quarter a year earlier, first-reported numbers).** Reported for information; the pre-registration set this check for H5 only.

| Group | Next quarter: change in operating margin (median, pts) | Next quarter: revenue growth (median) | Signal quarter: revenue growth (median) | Change in growth, next vs signal quarter (median, pts) | Filings (with a next quarter) |
|---|---|---|---|---|---|
| Signal | +0.60 | 7.0% | 4.2% | +1.9 | 825 (796) |
| Control | +0.67 | 8.0% | 8.4% | -0.5 | 12,603 (11,531) |

Signal minus control: -0.07 points of operating margin; the signal group was ahead in 3 of 8 calendar years (mean yearly gap +0.20 points, t = 0.30). The difference is not positive, so the mechanism does not show up at quarterly speed.

**For picking stocks.** Backlog growing faster than sales is not a usable signal on this evidence. The gap (+3.7 points a year) is statistically weak, comes from small caps (+4.7 points) rather than large ones (+0.1 points), and disappears against same-size companies in the same industry (-0.2 points). The accounts do not back it either: the signal companies' next-quarter margins moved +0.60 points against +0.67 for other RPO reporters. With a median of 28 stocks held and under eight years of data, a real effect of a few points a year could not be told apart from luck; treat a growing backlog as a question to ask, not a reason to buy. The signal portfolio's 21.7% a year against IWM's 10.2% mostly reflects which companies report RPO (the other RPO reporters returned 17.9%) and the missing-company bias, not the signal.

**How many companies report RPO.** Distinct companies whose 10-Q or 10-K reported a total remaining performance obligation at the quarter end, by calendar year of the formation month:

| Year | In the universe (priced, >= $50M) | All that pass the filters (incl. unpriced) | H6 signal filings |
|---|---|---|---|
| 2018 | 324 | 580 | 0 |
| 2019 | 371 | 647 | 52 |
| 2020 | 411 | 655 | 90 |
| 2021 | 450 | 660 | 102 |
| 2022 | 483 | 701 | 125 |
| 2023 | 508 | 694 | 135 |
| 2024 | 527 | 657 | 127 |
| 2025 | 526 | 629 | 123 |
| 2026 | 543 | 605 | 71 |

Year-over-year RPO needs a year of reporting after ASC 606 took effect (2018), so H6 starts in spring 2019.

## Caveats

- **First-reported numbers.** Every quarterly value is taken from the first filing that reported that period, available from its filing date. Q4 is rarely reported on its own: 30,158 of 214,668 company-quarters are a derived Q4 (the 10-K's full year minus the first-reported nine months), and for 25,769 of the 10-K triggers the just-reported quarter is such a derived Q4. Revenue follows the annual study's tag order within each filing; when a company switched revenue tags between the quarter and the year-ago quarter the growth rate compares two tags.
- **What counts as acceleration.** Year-over-year growth includes acquisitions, so some H5 signals are deals rather than organic demand (for example Shentel after buying nTelos in 2016). H6's gap is "RPO growth minus sales growth", so a shrinking company whose backlog falls less than its sales, or a tiny RPO balance that multiplies, also qualifies (examples in the data: LSB Industries 2023, Sturm Ruger 2025). Both definitions were fixed in advance and are not changed here.
- **Price errors.** The H1-H3 bad-print rule removed 80 one-month 10x round trips and 139 monthly returns above +1,000% across all symbols. Only three fell in stocks these tests held, all in the control groups: Chord Energy's November 2020 +30,991% (a bankruptcy splice that never happened to a holder), GameStop's +1,625% in January 2021 and Urban One's +1,446% in June 2020. The raw-return lines above differ from the cleaned ones mainly because of Chord. The return matrix was rebuilt from the annual study's price cache and matches `../cache/returns.parquet` in 100.0% of cells.
- **Early years.** Fixed-cost share needs four fiscal years of XBRL data, so until 2013 mostly large, long-listed companies have one and the H5 signal portfolio is small (every month with fewer than 30 holdings falls between Aug 2011 and Feb 2013).
- **H6 is thin.** 215 distinct companies ever enter the H6 signal, over 88 months; a real effect of a few points a year could not reach t = 2 in a sample this size.
- **Several looks.** Two hypotheses, each cut about a dozen ways. The closest cut to the bar is H5 held six months (+3.3 points a year, NW t = 1.88); with this many cuts one near 2 is expected by chance, and the matched and half-period results do not support it.
- **Other data limits.** Industry codes are each company's current SIC code. Market caps use the most recent SEC share count before the month-end on Yahoo's split basis (only the $50M filter, the $2B split, size terciles and value weights depend on them). The company list is the annual study's (revenue above $10M in some fiscal year 2010-2024). Only the signal-versus-universe comparison deducts costs (0.5% a year); a portfolio that turns over every three months would cost more in practice.

## Files

- `research/oplev/quarterly/fetch_facts.py` downloads SEC companyfacts (cached in `quarterly/cache/`)
- `research/oplev/quarterly/build_quarterly.py` builds first-reported quarterly fundamentals, fixed-cost shares and RPO per filing
- `research/oplev/quarterly/run_quarterly.py` the pre-registered tests; `md_quarterly.py` renders this file
- `research/oplev/quarterly/results_quarterly.json` every number; `monthly_returns_quarterly.csv` monthly signal, control and universe returns
- `research/oplev/H5_H6_PREREG.md` the pre-registration and its Deviations section
