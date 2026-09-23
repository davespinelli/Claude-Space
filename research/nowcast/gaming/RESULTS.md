# Do monthly state casino data get ahead of casino earnings? Pre-registered pilot

*Generated 2026-09-23 by `research/nowcast/gaming/scripts/write_results.py` from `results.json`. Design in `PREREG.md` (locked), with the Deviations section written before any return was computed. State revenue data 2012-01 to 2026-08, earnings announcements April 2013 to August 2026.*

## The short answer

**No.** Monthly state casino revenue tells you a casino company's same-store revenue before it reports, and pushing it through the company's operating leverage gives a better EBITDA forecast than "same as last quarter". But the stock does not move with it. Companies whose state data pointed to an earnings acceleration did only +0.67 percentage points better around the release per standard deviation of the signal (t = 0.93, bar 2.0). The slope was positive in both halves (+0.50 and +1.80), but too small and noisy to count. Nothing happened before the release either, and the signal did not predict whether EPS beat consensus. The likeliest reading: analysts and investors already track these public state numbers, so they are in the price and the consensus by report day.

| Test | Property-level states (verdict) | With Mississippi / Colorado / Nevada proxies (no verdict) |
|---|---|---|
| **Primary: announcement return on EBITDA-acceleration nowcast** | **No.** +0.67 points per SD, t = 0.93, n = 189; halves +0.50 / +1.80 | +0.57 points per SD, t = 1.54, n = 396; halves +0.79 / +0.36 |
| Pre-announcement drift (last state report to release) | +0.17 points per SD, t = 0.34, n = 189 | -0.07 points per SD, t = -0.21, n = 395 |
| Revenue-only nowcast (no operating-leverage step) | -0.50 points per SD, t = -0.79, n = 189 | +0.03 points per SD, t = 0.06, n = 396 |
| Sign of EPS surprise vs consensus (Yahoo) | hit rate 51.7% of 174, p = 0.70 | 51.0% of 361, p = 0.75 |
| Small caps (< $2B at announcement) | +0.51 points per SD, t = 0.39, n = 66 | +0.21 points per SD, t = 0.29, n = 176 |
| Larger companies | +0.95 points per SD, t = 1.07, n = 122 | +0.88 points per SD, t = 1.75, n = 218 |

Slopes are the abnormal return (stock minus SPY, close before the 8-K filing day to close after it) in percentage points for a one-standard-deviation higher signal, after winsorising the signal at the 5th/95th percentiles; t-statistics are clustered by calendar quarter. "Halves" split the sample at its median announcement date.

In one line: **Primary No** (slope +0.67 points per SD, clustered t = 0.93, positive in both halves: +0.50 in 2013-2022, +1.80 in 2022-2026).

## Sample sizes

- **Return tests, property sample (verdict):** 189 company-quarters, 8 companies (Penn 52, Boyd 39, Eldorado/Caesars (CZR) 37, Churchill Downs 26, Century 13, Full House 12, Bally's 7, MGM 3), 53 calendar quarters, announcements 2013-04-23 to 2026-08-14; state data from 18 states (DE, FL, IA, IL, IN, KS, LA, MA, MD, ME, MI, MO, NJ, NY, OH, PA, RI, WV).
- **Return tests, region sample:** 396 company-quarters, 11 companies (Full House 54, Penn 54, Boyd 53, Churchill Downs 51, Eldorado/Caesars (CZR) 46, Red Rock 37, MGM 34, Monarch 30, Century 22, Wynn 8, Bally's 7), 21 states.
- **Accuracy checks** use every qualifying company-quarter whether or not the stock has prices: 332 company-quarters of 17 companies (property sample), 594 of 21 (region sample).
- **State data:** 21 states, monthly, mostly 2012-01 to 2026-07/08 (table at the end). Every state's property rows add up to the regulator's own statewide total (largest gap 0.02%, except Kansas 0.8% against a later year's comparison column).
- **Ownership timeline:** 523 ownership spells, 294 casinos, 34 companies, 511 of them checked against 10-K property lists and 8-K closing notices.
- A company-quarter qualifies when its covered casinos' GGR a year earlier was at least 60% of its reported gaming revenue then (the casino line of the revenue breakdown; total revenue only where no gaming line exists), and the state reports for at least two-thirds of that were public before the release.

## How accurate the nowcasts were (the machine works)

Property sample, all qualifying company-quarters. "No portfolio change" drops quarters where the company bought or sold a casino in the past year (reported growth then includes the deal; the nowcast is same-store by design). Pearson correlations are dominated by the 2020-21 closures and reopenings, so rank correlations and median errors are the better guide. Growth is in fractions (0.05 = 5%).

| Quarters | n | Revenue: correlation / rank corr. / median miss | Naive (last quarter's growth) | EBITDA: correlation / rank corr. / median miss | Naive |
|---|---|---|---|---|---|
| All | 332 | 0.32 / 0.40 / 0.059 | 0.66 / 0.69 / 0.047 | 0.77 / 0.41 / 0.29 | 0.27 / 0.32 / 0.42 |
| No portfolio change | 147 | 0.93 / 0.69 / 0.022 | 0.22 / 0.59 / 0.038 | 0.87 / 0.43 / 0.24 | 0.22 / 0.29 / 0.37 |
| No portfolio change, ex-COVID | 138 | 0.48 / 0.68 / 0.022 | 0.61 / 0.69 / 0.033 | 0.90 / 0.39 / 0.21 | 0.20 / 0.25 / 0.33 |

Pre-registered figures (all qualifying quarters): revenue-growth correlation 0.32, mean absolute error 0.265; EBITDA-growth correlation 0.77, mean absolute error 1.27. Same-store, the state data nail revenue (median miss 2.2 points of growth vs 3.8 for the naive forecast). EBITDA is much harder (median miss 24 points) because operating income carries impairments, pre-opening costs, online losses and rent changes that no revenue data can see, but it still beats "same as last quarter".

By company (property sample, all qualifying quarters; rank correlations):

| Company | Quarters | Period | Median coverage | Revenue rank corr. | Revenue median miss | EBITDA rank corr. | In return tests |
|---|---|---|---|---|---|---|---|
| Penn | 52 | 2013-03 to 2026-06 | 0.80 | 0.64 | 0.052 | 0.41 | 52 |
| Boyd | 39 | 2013-03 to 2026-06 | 0.67 | 0.60 | 0.041 | 0.38 | 39 |
| Eldorado/Caesars (CZR) | 37 | 2014-09 to 2025-03 | 0.68 | 0.53 | 0.203 | 0.58 | 37 |
| Bally's | 28 | 2019-06 to 2026-06 | 0.80 | 0.56 | 0.186 | 0.33 | 7 |
| Churchill Downs | 26 | 2017-09 to 2026-06 | 0.68 | 0.02 | 0.157 | -0.19 | 26 |
| Empire Resorts | 26 | 2013-03 to 2019-09 | 0.98 | 0.09 | 0.029 | 0.60 | 0 |
| Tropicana Ent. | 22 | 2013-03 to 2018-06 | 0.94 | 0.78 | 0.030 | 0.56 | 0 |
| Dover Downs | 19 | 2013-06 to 2018-12 | 0.97 | 0.88 | 0.019 | 0.32 | 0 |
| Century | 13 | 2021-03 to 2026-06 | 0.63 | 0.32 | 0.057 | 0.24 | 13 |
| Isle of Capri | 13 | 2013-04 to 2016-04 | 0.70 | 0.66 | 0.031 | 0.62 | 0 |
| Full House | 12 | 2013-03 to 2026-06 | 0.71 | -0.17 | 0.073 | 0.53 | 12 |
| Pinnacle (to 2016) | 12 | 2013-03 to 2015-12 | 0.95 | -0.37 | 0.126 | 0.30 | 0 |
| Golden/Lakes | 9 | 2014-09 to 2016-06 | 1.01 | -0.33 | 0.107 | 0.66 | 0 |
| Pinnacle (2016-18) | 9 | 2016-06 to 2018-06 | 0.95 | 0.83 | 0.044 | 0.52 | 0 |
| Caesars Ent. Corp (old) | 8 | 2013-06 to 2020-03 | 0.69 | 0.74 | 0.065 | 0.31 | 0 |
| MTR Gaming | 4 | 2013-09 to 2014-06 | 0.61 | n/a | n/a | n/a | 0 |
| MGM | 3 | 2021-09 to 2023-09 | 0.62 | n/a | n/a | n/a | 3 |

## Primary test

Signal: nowcast EBITDA growth for the quarter (state GGR growth x revenue a year ago x the company's flow-through rate, added to EBITDA a year ago) minus the company's reported EBITDA growth the quarter before. Flow-through (dollars of EBITDA per dollar of revenue change, estimated only on quarters reported before each release, shrunk halfway to the industry median) had a median of about 0.4 in the sample.

- Result: slope +0.67 points per SD (standard error 0.72), clustered t = 0.93, 189 company-quarters, 53 calendar-quarter clusters, R-squared 0.006.
- First half (2013-04-23 to 2022-02-22): +0.50 points (t = 0.66, n = 94).
- Second half (2022-02-23 to 2026-08-14): +1.80 points (t = 1.19, n = 95).
- Using all three months of state data even when a report came out after the release (the literal PREREG signal): +0.69, t = 0.95.
- Excluding fiscal quarters from 2020 Q1 to 2021 Q2 (closures): +0.66, t = 0.93, n = 167.
- **Verdict: No.** Positive in both halves, but t = 0.93 is well short of 2.0.

## Secondary tests (no verdict)

**Does the market price the state data before the report?** Return from the day the last state report used was published to the day before the release (median 7 calendar days): +0.17 points per SD, t = 0.34, n = 189; halves +0.13 / +0.75. Region sample: -0.07 points per SD, t = -0.21, n = 395. No drift in the direction of the nowcast. Most state reports are out one to four weeks before the release; the market does not trend toward the nowcast in that window and does not react to it on the day, which together say the information is already in prices (or is not news).

**Revenue-only version:** -0.50 points per SD, t = -0.79, n = 189 (region +0.03 points per SD, t = 0.06, n = 396). The operating-leverage step turns a slightly negative revenue signal into a slightly positive EBITDA one; neither is distinguishable from zero.

**Versus analyst estimates:** Alpha Vantage was not available locally, but Yahoo's earnings calendar (via yfinance) gives a free consensus-EPS history. The nowcast signal's sign matched the sign of the EPS surprise in 90 of 174 releases (51.7%, binomial p = 0.70); small caps 45.8% of 59, larger 54.8% of 115. Region sample 51.0% of 361 (p = 0.75). Yahoo's consensus is today's record, not a point-in-time snapshot, and uses adjusted EPS.

**Small caps versus larger** (market cap at the announcement below $2B; signals standardised on the whole sample):

| | Property sample | Region sample |
|---|---|---|
| Small caps, announcement | +0.51 points per SD, t = 0.39, n = 66 | +0.21 points per SD, t = 0.29, n = 176 |
| Larger, announcement | +0.95 points per SD, t = 1.07, n = 122 | +0.88 points per SD, t = 1.75, n = 218 |
| Small caps, drift | +0.54 points per SD, t = 0.62, n = 66 | -0.16 points per SD, t = -0.33, n = 176 |
| Larger, drift | -0.50 points per SD, t = -1.05, n = 122 | +0.02 points per SD, t = 0.04, n = 217 |
| Small caps, revenue-only | +0.06 points per SD, t = 0.05, n = 66 | +0.03 points per SD, t = 0.04, n = 176 |
| Larger, revenue-only | -0.80 points per SD, t = -0.80, n = 122 | -0.06 points per SD, t = -0.11, n = 218 |

The property-sample small caps are Penn 17, Century 13, Full House 12, Eldorado/Caesars (CZR) 10, Bally's 7, Boyd 7 (Penn, Boyd and Eldorado were under $2B in parts of 2013-2016). The thinner analyst coverage of small caps does not show up as a larger reaction to the state data; if anything the slope is smaller.

## The region sample (Mississippi, Colorado, Nevada)

These states publish revenue only by region, town or reporting area, so each casino's revenue is imputed from its share of the area's slot machines and tables (10-K property tables for Nevada and Colorado, the Gaming Commission's per-casino counts for Mississippi). That brings in Monarch, Red Rock, the Las Vegas side of Boyd and Caesars, and most of Century and Full House. Result: +0.57 points per SD, t = 1.54, n = 396, positive in both halves (+0.79, t = 1.85; +0.36, t = 0.67). Closer to the bar than the verdict sample but still short, and it has no verdict under the pre-registration.

## Names and dates excluded, and why

**No daily prices on Yahoo** (kept in the accuracy checks, left out of the return tests). Qualifying company-quarters lost, property / region sample:

- Affinity: 0 / 14 (never exchange-listed)
- Bally's: 21 / 21 (Yahoo's history starts 2024-12-06; Twin River/Bally's 2019-2024 missing)
- Caesars Ent. Corp (old): 8 / 24 (Yahoo's CZR history is Eldorado's)
- Dover Downs: 19 / 19 (merged into Twin River Mar 2019)
- Golden/Lakes: 9 / 31 (taken private April 2026; Yahoo dropped the symbol)
- Isle of Capri: 13 / 16 (acquired by Eldorado May 2017)
- MTR Gaming: 4 / 4 (merged into Eldorado Sept 2014)
- Empire Resorts: 26 / 26 (taken private Nov 2019 (Yahoo's NYNY today is an unrelated company))
- Pinnacle (2016-18): 9 / 9 (acquired by Penn Oct 2018)
- Pinnacle (to 2016): 12 / 12 (Pinnacle before the 2016 GLPI deal)
- Tropicana Ent.: 22 / 22 (acquired by Eldorado Oct 2018)
- Caesars Acquisition Co, Nevada Gold, Lakes (LACO) and ERI/TRWH under their old tickers: no Yahoo history. Stooq blocks scripted access with a browser check, which was not bypassed.

**Never qualified in the property sample** (coverage below 60%): Monarch and Red Rock (all Nevada/Colorado), Wynn (Macau, Las Vegas), MGM in all but 3 quarters (Strip, Macau); Caesars after 2020 mostly (Strip). Churchill Downs does qualify, because the pre-registered rule measures coverage against casino revenue, although most of its revenue is racing, historical racing machines and online.

**States not collected:** Kentucky (Churchill's historical racing machines), New Mexico (Penn's Zia Park), Virginia (Caesars Virginia, 2024 on), Nebraska, Washington card rooms, tribal casinos (no public property data). Their properties count as uncovered.

**Data gaps:** West Virginia racetracks before July 2018 (no archive found); New York after September 2025 (the regulator blocks scripted access; Internet Archive copies end there); Iowa from July 2026 (AGR redefined, about -13% mechanically; excluded from year-over-year comparisons); Maine November-December 2017; Illinois April-June 2020 set to zero (closed, no reports); Nevada 2020-04/05 and 2025-06/07 rebuilt from later reports' three-month columns; Mississippi 2012-2015 Central/Northern split imputed.

**Point-in-time drops:** company-quarters whose state reports covering two-thirds of the year-ago GGR were not public before the release were dropped: 7 in the property sample (1 priced), 33 in the region sample (26 priced; Nevada publishes about four weeks after month-end).

## Caveats

- **Small cross-section.** Only 8 companies (property sample) have usable prices; Penn, Boyd and Eldorado/Caesars supply 128 of 189 observations. The companies bought out in 2017-2019 (Isle, Pinnacle, Tropicana, Dover Downs, Empire) are exactly the ones with the cleanest single-state coverage, and they have no prices.
- **EBITDA as defined here is noisy.** Operating income + D&A carries impairments and one-offs, and growth on small or negative bases explodes; the signal subtracts last quarter's reported EBITDA growth, which is dominated by those swings (winsorisation caps it but the signal is mostly baseline noise). A cleaner adjusted-EBITDA series would need the press releases.
- **The coverage rule is literal.** Coverage is against casino revenue, so Churchill Downs qualifies although state data cover a minority of its business; Rhode Island and New York report total net terminal income, of which the operator books only its share, so Bally's and Empire Resorts look better covered than they are.
- **Publication dates are partly assumed.** Where a report's date could not be found (Illinois from 2020, most of Ohio, Iowa, Colorado, Delaware, Florida), month-end + 30 days was used; 95% of property-sample test quarters use at least one assumed date. Some state archives hold revised rather than first-published figures (Iowa, Florida, Missouri).
- **Region imputation** assumes each casino earns its machine share of the area's win; big Strip resorts and local casinos differ.
- **Fixed after the first run:** Red Rock has no cover-page share count in the SEC data, so the first run left it out of the size split; the reported numbers use its Class A weighted share count (listed shares only). Only the region-sample size split changed (first run: small caps +0.18, t = 0.24, n = 163; larger +0.89, t = 1.71, n = 195); nothing else was affected.
- Research only; no trading.

## For picking stocks

Do not trade casino earnings off the monthly state revenue reports: they forecast same-store revenue well, but the market already has them. No reliable announcement-day edge (t = 0.93), no drift after the reports (t = 0.34), and a coin-flip on beating consensus (52%), in small caps as in large. They remain useful for knowing what a quarter will look like, not for beating the market to it.

## Live nowcast, Q3 2026 (July-September; `data/live_nowcast.csv`)

State reports published by 2026-09-23: July and August for most states, July only for Nevada and Colorado. September is not out yet, so these are two-month (or one-month) reads. Given the results above, treat them as a preview of the quarter, not a trading signal.

| Company | Sample | Months | Coverage | Same-store GGR growth | Nowcast EBITDA growth | Last quarter's EBITDA growth | Signal (SD) | Reports |
|---|---|---|---|---|---|---|---|---|
| Bally's | prop | 2026-07,2026-08 | 0.80 | 1.8% | 4.5% | -16.8% | +0.21 | 2026-11-09 |
| Boyd | prop | 2026-07,2026-08 | 0.71 | 0.9% | 1.7% | -6.6% | +0.08 | 2026-10-22 |
| Churchill Downs | prop | 2026-07,2026-08 | 0.76 | 0.2% | 0.4% | 7.9% | -0.08 | 2026-10-28 |
| Century | prop | 2026-07,2026-08 | 0.66 | -1.1% | -1.1% | 2.6% | -0.04 | 2026-11-06 |
| Full House | prop | 2026-07,2026-08 | 0.71 | 10.6% | 22.5% | 20.8% | +0.02 | 2026-11-05 |
| Penn | prop | 2026-07,2026-08 | 0.84 | 3.6% | 3.9% | 32.7% | -0.29 | 2026-11-05 |
| Bally's | region | 2026-07,2026-08 | 0.95 | 1.7% | 4.3% | -16.8% | +0.20 | 2026-11-09 |
| Boyd | region | 2026-07,2026-08 | 1.18 | 0.6% | 1.0% | -6.6% | +0.07 | 2026-10-22 |
| Churchill Downs | region | 2026-07,2026-08 | 0.84 | 0.0% | 0.0% | 7.9% | -0.07 | 2026-10-28 |
| Century | region | 2026-07,2026-08 | 0.86 | 0.2% | 0.2% | 2.6% | -0.02 | 2026-11-06 |
| Eldorado/Caesars (CZR) | region | 2026-07,2026-08 | 0.99 | 0.4% | 0.4% | -2.5% | +0.03 | 2026-10-27 |
| Full House | region | 2026-07,2026-08 | 1.33 | 4.7% | 9.9% | 20.8% | -0.10 | 2026-11-05 |
| Monarch | region | 2026-07 | 0.84 | 1.3% | 1.5% | 1.7% | -0.00 | 2026-10-20 |
| MGM | region | 2026-07,2026-08 | 0.61 | 1.3% | 17.5% | 21.6% | -0.04 | 2026-10-28 |
| Penn | region | 2026-07,2026-08 | 1.03 | 3.5% | 3.8% | 32.7% | -0.27 | 2026-11-05 |
| Red Rock | region | 2026-07 | 1.06 | -3.8% | -3.8% | -9.7% | +0.05 | 2026-10-27 |

Notes: Penn's and MGM's year-ago quarters carry large impairments, so their EBITDA growth rates are not meaningful; Bally's coverage is overstated (see caveats); Iowa's July-August 2026 figures are left out (AGR redefined).

## State data used

| State | Source | Measure | Months | Units | Publication date |
|---|---|---|---|---|---|
| PA | Gaming Control Board revenue workbooks | slot + table GGR | 2011-07 to 2026-08 | 18 casinos (incl. Category 4) | press releases, ~16 days |
| NJ | Division of Gaming Enforcement releases | casino win (slots + tables) | 2012-01 to 2026-08 | 14 casinos | release date, ~14 days |
| DE | Delaware Lottery | video lottery + table win (periods pro-rated) | 2012-01 to 2026-08 | 3 | assumed |
| MD | Lottery & Gaming Control Agency releases | GGR | 2012-01 to 2026-08 | 6 | release date, ~5 days |
| MA | Gaming Commission | GGR | 2015-06 to 2026-08 | 3 | upload date, ~15 days |
| NY | Gaming Commission (Internet Archive copies) | VGM net win / casino GGR | 2012-01 to 2025-09 | 15 | partly, ~8 days |
| RI | RI Lottery | net terminal income + tables | 2012-01 to 2026-07 | 3 | partly, ~27 days |
| ME | Gambling Control Unit | GGR | 2012-01 to 2026-08 | 2 | ~6 days |
| OH | Casino Control Commission + Ohio Lottery | casino AGR; racino VLT net win | 2012-05 to 2026-08 | 4 casinos + 7 racinos | partly |
| MI | Gaming Control Board | AGR (Detroit) | 2012-01 to 2026-08 | 3 | from 2021, ~11 days |
| WV | WV Lottery weekly (pro-rated to months) | VLT + table revenue | 2018-07 to 2026-08 | 5 | partly |
| KS | Racing and Gaming Commission | gaming facility revenue | 2012-01 to 2026-08 | 4 | PDF date, ~16 days |
| IN | Gaming Commission | win before deductions | 2012-01 to 2026-08 | 15 | PDF date, ~9 days |
| IL | Gaming Board | AGR | 2012-01 to 2026-08 | 17 | to 2020-03, ~4 days |
| IA | Racing & Gaming Commission | AGR | 2012-01 to 2026-08 | 20 | 2026 only |
| MO | Gaming Commission | AGR | 2012-01 to 2026-08 | 13 | file date, ~9 days |
| LA | State Police Gaming Division | AGR (riverboats, racinos), GGR (land-based) | 2012-01 to 2026-08 | 22 | file date, ~16 days |
| FL | Division of Pari-Mutuel Wagering | net slot revenue | 2012-01 to 2026-08 | 8 | mostly assumed |
| MS | Gaming Commission | AGR by region (no casino detail) | 2012-01 to 2026-08 | 3 regions | ~17 days |
| CO | Division of Gaming | AGP by town (no casino detail) | 2012-01 to 2026-07 | 3 towns | mostly assumed |
| NV | Gaming Control Board | win ex race/sports by area (no casino detail) | 2012-01 to 2026-07 | 21 areas | press release, ~29 days |

Scripts: `scripts/state_<st>.py` (download and parse, sources and spot checks in each docstring), `ownership.py`, `property_map.py`, `property_devices.py`, `sec_fetch.py`, `gaming_revenue.py`, `prices.py`, `eps_estimates.py`, `build_nowcast.py` (no returns), `run_tests.py`, `live_nowcast.py`, `write_results.py`.
