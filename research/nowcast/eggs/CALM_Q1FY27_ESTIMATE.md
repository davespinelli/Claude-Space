# Cal-Maine Foods (CALM): fiscal Q1 2027 estimate, frozen before the report

**Written 2026-09-23, 15:20 EDT.** Frozen. Nothing above "Result after the report" changes after this time.
This is a research estimate to test a method. It is not investment advice and does not recommend buying or selling anything.

## The answer

**We estimate revenue of $539M (range $509M to $572M) and EPS of -$0.85 (range -$1.27 to -$0.59). Consensus is $578.5M and -$0.71 (MarketBeat, 2026-09-23).**

- **Revenue: we expect a miss.** Consensus sits above the top of our range. Every model variant we tried came in below consensus, between $518M and $553M. That covers all 24 variants plus the New York and no-lag price series.
- **EPS: we lean towards a miss, with low confidence.** We expect a loss about $0.15 a share bigger than consensus. Consensus is inside our range, so an in-line result would not be surprising.
- **Why:**
  - USDA wholesale egg prices over the quarter were about 14% below the previous quarter and 73% below a year earlier.
  - Our model turns that into a conventional egg price of about $0.99 a dozen. That is below Cal-Maine's cost of sales of roughly $1.43 a dozen of shell eggs to produce, buy and pack, before overheads.
  - Costs barely move with price, so the lower price drops almost straight into the loss.
- **Operating leverage:**
  - Each 10 cents a dozen on Cal-Maine's realised conventional price moves EPS by about **$0.34**.
  - Each 10 cents on the USDA wholesale price moves EPS by about **$0.22**. The effect is smaller because only about 74% of a market move reaches Cal-Maine's conventional price, and part of it is offset by cheaper eggs bought from other farms.

**The report** comes out **Wednesday 2026-09-30 at about 6:00 a.m. ET, before the market opens**. The call is at 9:00 a.m. ET. This is confirmed by the company's GlobeNewswire release of 2026-09-09, 4:30 p.m. ET, and Nasdaq's feed says the same.

**The quarter** runs from 2026-05-31 to 2026-08-29 and is 13 weeks long.
- The FY2026 10-K says the fiscal year ends on the Saturday closest to May 31, and FY2026 ended 2026-05-30.
- The next fiscal year end is 2027-05-29, so FY2027 has 52 weeks and Q1 has 13.
- We worked out the Q1 end date from this rule. No filing states it yet.

---

## 1. Method in plain words

1. **The price Cal-Maine gets follows a free public price.**
   - We compared Cal-Maine's reported net price for conventional eggs (44 quarters, FY2016 to FY2026) with free wholesale series.
   - The best match is USDA's monthly "Grade A large, Combined regional" wholesale price, published by USDA ERS. We average it over each fiscal quarter's exact dates, shifted back 7 days.
   - The fit has R² 0.992 and a typical miss of 6 cents a dozen (table in section 3).
   - Cal-Maine's price ≈ $0.36 + 0.74 × USDA price. This is fitted on the latest 12 quarters because the contract mix changes over time.
   - The intercept exists because about half of its conventional eggs are sold on grain-cost or hybrid formulas that do not fall with the market. The FY2026 10-K says "split almost evenly", and management said on the Q4 call that it realised about 102% of Urner Barry in Q4.
   - We add half of last quarter's miss (+1.5 cents this time).
2. **Specialty price** (cage-free, organic, Eggland's Best and so on) is last quarter's price plus a small link to the market: 0.14 × the change in the USDA price.
3. **Dozens sold** are the same quarter a year earlier, grown at the last reported year-on-year rate.
   - That rate is +3.1% for conventional and -5.9% for specialty, from the Q4 FY26 release.
   - Specialty gets +2.8% more for the Eggland's Best Northeast territory bought on 2026-07-10. Management expects about +5% a year, and Cal-Maine owned it for 7.3 of the 13 weeks.
4. **Other revenue** (egg products, prepared foods such as Echo Lake, and other) is held at last quarter's $92.4M.
5. **Costs: the operating-leverage step.**
   - Shell-egg cost of sales per dozen is last quarter's $1.434, adjusted as follows:
     - **Market price:** each $1.00 fall in the market price cuts it by $0.117. This covers the roughly 10% of eggs Cal-Maine buys from other farms at market prices.
     - **Feed:** a feed index built from corn and soybean meal prices over a 6-month window lagged 30 days (fit R² 0.94), with 59% pass-through.
     - **Drift:** a small upward trend.
     - All coefficients are fitted on earlier quarters only.
   - Other revenue is assumed to carry a 20% gross margin.
   - SG&A is the year-ago quarter times the latest year-on-year change. This keeps Q4's year-end corporate bump ($38M of unallocated corporate SG&A in Q4 FY26) out of Q1.
6. **Below the line:**
   - Other income is the year-ago figure plus last quarter's year-on-year change. Interest income is lower now that cash has fallen to $924M.
   - Tax uses the trailing four-quarter rate of 22.6%.
   - Minority interest is last quarter's $0.8M.
   - Shares are 46.85M: 46.92M were outstanding on 2026-07-22, a loss means diluted equals basic, and we allow for a little buyback.

### The live quarter against the quarter before and the year before

| Item | Q1 FY26 actual | Q4 FY26 actual | **Q1 FY27 estimate** |
|---|---|---|---|
| USDA combined price, $/dozen (quarter average, 7-day lag) | 3.09 | 0.98 | **0.84** |
| Conventional net price, $/dozen | 2.54 | 1.10 | **0.99** |
| Specialty net price, $/dozen | 2.40 | 2.14 | **2.12** |
| Conventional dozens (M) | 199.3 | 195.4 | **205.5** |
| Specialty dozens (M) | 118.3 | 114.6 | **114.4** |
| Egg products + prepared foods + other ($M) | 133.2 | 92.4 | **92.4** |
| **Net sales ($M)** | 922.6 | 552.6 | **538.6** |
| Shell-egg cost of sales per dozen ($) | 1.59 | 1.43 | **1.43** |
| Cost of sales ($M) | 611.3 | 518.5 | **529.7** |
| SG&A ($M) | 69.5 | 93.6 | **68.5** |
| Operating income ($M) | 249.2 | -58.8 | **-59.7** |
| Other income, net ($M) | 14.1 | 12.3 | **9.0** |
| Pre-tax income ($M) | 263.3 | -46.5 | **-50.6** |
| Net income attributable ($M) | 199.3 | -35.9 | **-40.0** |
| Diluted shares (M) | 48.4 | 47.0 | **46.85** |
| **Diluted EPS ($)** | 4.12 | -0.76 | **-0.85** |

Q4 FY26 volumes and prices are rebuilt from the release's segment table, using the volume and price changes against Q4 FY25. The FY2026 10-K stopped publishing per-dozen tables.

### Main drivers
- **Price, which matters most.** USDA combined regional averaged $0.56 in June, $1.01 in July and about $1.07 in August. The August figure is ERS's current-month estimate from 2026-08-27.
  - This fits management's comment that Urner Barry averaged $0.72 over the first five weeks and then rose by more than 90%.
  - Prices then fell again in late August. USDA put the New York large egg at $0.92 in the week of Aug 21 and $0.82 on Sep 18.
  - The quarter's average came in slightly below Q4 FY26's.
- **Costs stay put.** Feed is flat year on year. The modelled feed cost is $0.46 a dozen against $0.47 actual in Q1 FY26, with corn at about $4.40 and soybean meal at about $300 over the window. Much of the cost base is fixed.
- **Why this is not worse:**
  - Half of conventional volume is on grain or hybrid pricing.
  - Specialty is still profitable at about $2.12 a dozen.
  - Q1 SG&A is seasonally about $25M lower than Q4.
  - Eggs bought from other farms are cheap.
- **Sensitivity (operating leverage):**
  - +10 cents a dozen realised conventional price: **+$20.5M pre-tax, +$0.34 EPS**.
  - +10 cents on the USDA price: **+$16.8M revenue, +$0.22 EPS**.

### A second view: building up segment by segment
- **Inputs:** the recast FY24-FY26 segment tables in the Q4 FY26 release (data/calm_segments.csv), with each segment's Q4 FY26 cost per dozen.
- **Segments:**
  - Conventional: -$61M.
  - Specialty: +$17M.
  - Prepared foods: +$9M, held at Q4.
  - Other segment: -$7M, held at Q4. Egg-product prices were even lower in Q1.
  - Corporate SG&A: -$23M, the FY26 Q1-Q3 average.
- **Total:** operating income -$66M, which gives **EPS -$0.96**.
- **Conclusion:** this agrees with the main model's -$0.85. Both point to a loss larger than consensus's -$0.71.

---

## 2. Backtest: how much to trust the number

- **What we did:**
  - We re-estimated each of 36 past quarters, from FY18 Q1 (reported 2017-10-02) to FY26 Q4 (reported 2026-07-22).
  - Each estimate used only Cal-Maine numbers reported before that quarter's release, plus the USDA and grain prices for the quarter itself.
  - All coefficients are refitted each time on earlier quarters only.
- **How the model was chosen:**
  - We compared 24 variants: cost anchor (last quarter or year-ago), share of last miss carried (0, 0.5 or 1), volume trend window (last quarter or four quarters), and price-fit window (all quarters or 12).
  - EPS error varied only from $0.25 to $0.38 across them.
  - We picked the variant with the best conventional-price accuracy, which was also within $0.01 of the best EPS error. All variants are in data/backtest_variants.csv.
  - Choosing after looking makes these accuracy figures slightly flattering.

| Measure | All 36 quarters | Last 12 quarters |
|---|---|---|
| Revenue, mean absolute % error | **3.8%** (median 2.6%) | 4.3% (median 3.0%) |
| Revenue bias (+ = too high) | +0.4% | +2.0% |
| EPS, mean absolute error | **$0.26** (median $0.19) | $0.36 (median $0.35) |
| EPS bias (+ = too optimistic) | +$0.06 | +$0.19 |
| EPS within ±$0.25 | 58% of quarters | |
| Operating-income error as % of revenue, mean absolute | 3.2% | 2.8% |
| Conventional price, mean absolute error | $0.05 a dozen | $0.10 a dozen |
| Direction of EPS change vs the prior quarter | right 34 of 35 times | |

- **Trough quarters** are the 17 quarters where the USDA price averaged below $1.30. The EPS error there was $0.22, but the model ran **too optimistic by +$0.11 on average**. For the most similar quarter, Q4 FY26, it said -$0.22 when the actual was -$0.76. If that pattern holds, the risk leans towards a bigger loss than our -$0.85.
- **How the ranges were built:** the 10th to 90th percentile of past errors applied to this quarter.
  - Revenue errors ran from -5.9% to +5.7%.
  - Operating-income errors ran from -2.9% to +4.7% of revenue, which is -$0.30 to +$0.62 in EPS terms at past scales and is rescaled here to this quarter's revenue.

### Last 12 quarters

| Quarter | Reported | USDA price | Conventional price, est / actual | Revenue est ($M) | Revenue actual ($M) | Error | EPS est | EPS actual | Error |
|---|---|---|---|---|---|---|---|---|---|
| FY24 Q1 | 2023-10-03 | 1.21 | 1.23 / 1.24 | 523 | 459 | +13.8% | +0.35 | +0.02 | +0.33 |
| FY24 Q2 | 2024-01-03 | 1.50 | 1.47 / 1.46 | 519 | 523 | -0.8% | +0.69 | +0.35 | +0.34 |
| FY24 Q3 | 2024-04-02 | 2.35 | 2.18 / 2.15 | 692 | 703 | -1.6% | +2.64 | +3.00 | -0.36 |
| FY24 Q4 | 2024-07-23 | 2.28 | 2.10 / 2.06 | 654 | 641 | +2.1% | +2.34 | +2.32 | +0.02 |
| FY25 Q1 | 2024-10-01 | 2.79 | 2.52 / 2.42 | 726 | 786 | -7.6% | +3.44 | +3.06 | +0.38 |
| FY25 Q2 | 2025-01-07 | 3.44 | 3.02 / 2.94 | 963 | 955 | +0.9% | +4.55 | +4.47 | +0.08 |
| FY25 Q3 | 2025-04-08 | 6.03 | 5.09 / 4.77 | 1,493 | 1,418 | +5.3% | +11.11 | +10.38 | +0.73 |
| FY25 Q4 | 2025-07-22 | 4.42 | 3.64 / 3.78 | 1,092 | 1,104 | -1.1% | +6.56 | +7.04 | -0.48 |
| FY26 Q1 | 2025-10-01 | 3.09 | 2.75 / 2.54 | 953 | 923 | +3.3% | +4.88 | +4.12 | +0.76 |
| FY26 Q2 | 2026-01-07 | 2.11 | 1.88 / 1.80 | 817 | 769 | +6.2% | +2.22 | +2.13 | +0.09 |
| FY26 Q3 | 2026-04-01 | 1.33 | 1.27 / 1.42 | 649 | 667 | -2.6% | +0.89 | +1.06 | -0.17 |
| FY26 Q4 | 2026-07-22 | 0.98 | 1.13 / 1.10 | 587 | 553 | +6.2% | -0.22 | -0.76 | +0.54 |

The full 36-quarter table is in data/backtest.csv.

**Model against consensus over the last 3 quarters.** Consensus figures are from Investing.com's earnings history, read 2026-09-23.

| Quarter | EPS actual | Model EPS | Consensus EPS | Revenue actual | Model revenue | Consensus revenue |
|---|---|---|---|---|---|---|
| FY26 Q2 | 2.13 | 2.22 | 2.08 | 769.5 | 817.1 | 814.2 |
| FY26 Q3 | 1.06 | 0.89 | 0.89 | 667.0 | 649.4 | 678.2 |
| FY26 Q4 | -0.76 | -0.22 | +0.11 | 552.6 | 586.7 | 657.1 |

Over three quarters the model was about as accurate as consensus, and closer in the one trough quarter. That is far too few quarters to prove anything.

---

## 3. Which free price series tracks Cal-Maine best

Cal-Maine's conventional net price per dozen, regressed on each series averaged over the fiscal quarter's dates, using all 44 quarters from FY16 Q1 to FY26 Q4 (data/price_fit.csv):

| Series | Lag | R² | Typical miss (RMSE, $/dozen) |
|---|---|---|---|
| **USDA ERS Grade A large, Combined regional wholesale (monthly)** | **7 days** | **0.992** | **0.082** |
| same | 0 / 14 days | 0.983 / 0.990 | 0.120 / 0.092 |
| USDA ERS Grade A large, New York wholesale | 7 / 14 days | 0.984 / 0.985 | 0.115 / 0.113 |
| BLS PPI, eggs, large (WPU01710703) | 7 days | 0.986 | 0.108 |
| BLS PPI, eggs for fresh use (WPU017107) | 7 days | 0.985 | 0.111 |
| BLS PPI, chicken eggs (WPU0171) | 7 days | 0.982 | 0.121 |
| BLS average retail price, Grade A large (APU0000708111) | 0 days | 0.905 | 0.281 |
| Longer lags (21, 30, 45 days), every series | | worse at each step | |

- **Lag:** the best lag is about one week. Cal-Maine's formula prices trail the quote only slightly. Monthly data cannot pin the lag down more precisely than that.
- **Retail prices** fit much worse because retail price moves are damped and delayed.
- **The New York series** puts this quarter higher, at $0.94 against $0.84 on the combined series. Using it would give EPS of -$0.78 instead of -$0.85.
- **The weekly USDA reports** (Egg Markets Overview, ams_3725; the daily National Shell Egg Index, 2843; and the combined regional report, 2848) could not be used for history:
  - The free ESMIS archive stops at 2025-09-26.
  - MyMarketNews was unreachable from this machine.
  - The MARS API needs a key; it returned 403.
  - ERS's monthly table is built from the same AMS data and goes back to 2000.

---

## 4. Data sources, all accessed 2026-09-23

**Cal-Maine (SEC EDGAR, CIK 16160).**
- Pulled with User-Agent `ClaudeSpace research dspinjr@gmail.com` at no more than about 6.5 requests a second.
- Coverage: 45 earnings releases (8-K Item 2.02, EX-99.1) and 45 10-Qs and 10-Ks, from FY2016 Q1 to FY2026 Q4. Each quarter's source URLs are in data/calm_sources.csv.
- Key documents:
  - Q4 FY26 release, 2026-07-22, including the segment recast and Urner Barry quarter-to-date comment: https://www.sec.gov/Archives/edgar/data/16160/000156276226000078/exhibit991.htm
  - FY2026 10-K, 2026-07-22: https://www.sec.gov/Archives/edgar/data/16160/000156276226000080/calm2026053010K.htm
  - Q1 FY26 10-Q (the year-ago quarter): https://www.sec.gov/Archives/edgar/data/16160/000156276225000251/calm-20250830.htm
  - XBRL companyfacts, used to fill gaps where release text did not parse: https://data.sec.gov/api/xbrl/companyfacts/CIK0000016160.json
- Figures are as first reported: the current-quarter column of each release.
- Q4 values = 10-K year minus Q1-Q3. The 10-K's revenue note gives Q4 sales directly from FY2019.
- Specialty includes the co-pack specialty line that was reported separately until FY2019.
- Echo Lake Foods (prepared foods) was bought on 2025-06-02, at the start of FY26 Q1. It added $70.5M of sales in that quarter.

**Egg prices.**
- USDA ERS, Livestock and Meat Domestic Data, "Wholesale prices" workbook: Eggs, Grade A large, Combined regional and New York, in cents a dozen, monthly from 2000.
  - Page: https://www.ers.usda.gov/data-products/livestock-and-meat-domestic-data
  - File: https://www.ers.usda.gov/media/5538/wholesale-prices.xlsx
  - Last updated 2026-08-27; the next update is 2026-09-29, the day before the report. August 2026 is ERS's current-month estimate.
- FRED (BLS): WPU017107, WPU01710703, WPU0171 and APU0000708111. Links take the form https://fred.stlouisfed.org/series/WPU017107.
- USDA AMS Egg Markets Overview:
  - Current report: https://www.ams.usda.gov/mnreports/ams_3725.pdf (2026-09-18).
  - Archive: https://esmis.nal.usda.gov/publication/egg-markets-overview (2023-12-22 to 2025-09-26).

**Feed.**
- USDA ERS broiler, turkey and egg feed costs workbook: corn No. 2 yellow Chicago and soybean meal Decatur, monthly to February 2026. ERS stopped updating it in April 2026.
  - https://www.ers.usda.gov/media/20291/broiler-turkey-and-egg-feed-costs.xlsx
- Extended with CBOT corn front-month from Yahoo Finance (ZC=F, daily) and IMF soybean meal from FRED (PSMEAUSDM), each scaled to the ERS level over 2022-26.

**Management comments.**
- Q4 FY26 earnings call transcript: https://www.investing.com/news/transcripts/earnings-call-transcript-calmaine-foods-q4-2026-miss-hits-shares-as-egg-prices-slump-93CH-4806250
- Points used:
  - Q4 Urner Barry averaged $1.08.
  - About 102% of Urner Barry was realised.
  - Conventional pricing is about 50/50 market and hybrid.
  - Prepared foods capacity comes on from Q2 FY27.

**Report date.**
- https://www.globenewswire.com/news-release/2026/09/09/3359080/0/en/cal-maine-foods-schedules-first-quarter-fiscal-2027-earnings-release-conference-call-and-webcast.html

**Consensus** (data/consensus_snapshot.csv):

| Source | EPS | Revenue ($M) | Note |
|---|---|---|---|
| MarketBeat, article dated 2026-09-23 | -0.706 | 578.5 | Checked directly; number of analysts not stated. [link](https://www.marketbeat.com/instant-alerts/upcoming-cal-maine-foods-calm-projected-to-release-earnings-on-wednesday-2026-09-23/) |
| Investing.com | -0.474 | 587.8 | Checked directly. **Disagrees:** a much smaller loss. [link](https://www.investing.com/equities/cal-maine-foods-earnings) |
| TradingView | -0.71 | 574.8 | From the research sub-agent; not re-checked. |
| TipRanks | -0.71 | n/a | From the research sub-agent. |
| TradingKey | -0.71 | 578.5 | From the research sub-agent. An older undated copy showed -$0.15 and $597.8M, which suggests estimates came down. |
| Zacks, Yahoo, Nasdaq | n/a | n/a | Could not be retrieved: bot checks, rate limits, or "forecast not available". |

**Headline consensus used here:** -$0.71 and $578.5M. The sources mostly agree, and Investing.com is the outlier. Against Investing.com's figures, we would call both revenue and EPS a miss.

---

## 5. Caveats

1. **The conventional price is the whole game, and the free series disagree on it.**
   - The combined regional series says this quarter was 14% below Q4. The New York series says roughly flat.
   - Management's Urner Barry figures ($0.72 for five weeks, then +90%) point to an Urner Barry average near $1.05-1.10, which is about Q4's $1.08.
   - If Cal-Maine realised Q4's $1.10 again, instead of our $0.99, EPS would be about -$0.48 and revenue about $561M. That would beat EPS consensus and still miss on revenue.
2. **The model has run too optimistic in troughs:** +$0.11 on average, and +$0.54 last quarter. If anything, that skews the risk the other way from caveat 1.
3. **The August price is an estimate**, made by ERS on about Aug 27. Prices fell hard in the last week of August. With the 7-day lag, our window ends on Aug 22.
4. **Accounting and structure changes.**
   - Cal-Maine now reports three segments and has dropped the per-dozen tables.
   - Our Q4 FY26 volumes and prices are rebuilt from percentage changes.
   - The Q1 FY27 release may not report dozens or the net price per dozen, so we will score mainly on revenue and EPS, and on the segment volume and price percentages.
5. **SG&A is set to Q1's seasonal low** ($68.5M). If it runs at $75M (Van's, the Eggland's Best territory, franchise fees), EPS drops by about $0.11.
6. **Items the model cannot see:**
   - The DOJ settlement: $1.5M plus 30 million donated eggs. It depends on court approval and its accounting timing is unknown.
   - Insurance or involuntary-conversion gains.
   - Write-downs.
   - Egg-product losses. The USDA breaking-stock price was about $0.07 a dozen by September.
   - Buybacks during the quarter.
   - No Cal-Maine bird-flu (HPAI) outbreak was found for June to August. The last one was 352,000 pullets in Maryland in March 2026.
7. **Egg products and prepared foods are held flat at Q4's $92.4M.** Prepared-foods capacity additions start in Q2 FY27 and Q1 is seasonally soft, so that is probably fair.
8. **Selection.** We chose one of 24 variants after seeing the backtest.
   - All 24 variants give revenue of $518M to $550M for this quarter.
   - Their EPS runs from -$1.20 to -$0.38.
   - The 12 variants that anchor costs on last quarter all give a loss at least as big as consensus: -$0.72 to -$1.20. Anchoring on last quarter backtests better, with EPS error of $0.25-0.30.
   - The 12 that anchor on the same quarter a year earlier give -$0.38 to -$0.86. They backtest worse, with EPS error of $0.30-0.38, and they have to stretch the cost-to-price link over a $2.25 fall in the market price.

---

## 6. How to rerun

From research/nowcast/eggs/:
- `python3 scripts/sec_fetch.py` fetches the SEC filings into cache/sec.
- `python3 scripts/parse_sec.py` builds data/calm_quarterly.csv and data/calm_sources.csv.
- `python3 scripts/prices.py` builds data/prices_monthly.csv.
- `python3 scripts/model.py` produces data/price_fit.csv, data/backtest_variants.csv, data/backtest.csv and data/live_estimate.json.
- `python3 scripts/segment_check.py` produces data/calm_segments.csv and data/segment_check.json.

Downloads are cached in cache/, which git ignores.

---

## Result after the report (fill in after 2026-09-30)

Scoring is against the frozen numbers above.

Scored 2026-10-11 from Cal-Maine's earnings release of 2026-09-30. The scoring scheduled for 2026-09-30 did not run. Every figure below comes from filings or data published on or before 2026-09-30, except the stock prices.

### The answer

- **Revenue: our call was right, and the number was almost exact.**
  - Cal-Maine reported net sales of **$539.6M**. We said $538.6M (range $509M to $572M).
  - Consensus was **$561.6M on report day**. It was $578.5M when we froze.
  - The result was inside our range, near the middle.
  - Our "miss" call was right: revenue came in below both consensus figures.
- **EPS: the direction was right, but the loss was much bigger than we said.**
  - Diluted EPS was **-$1.26**. We said -$0.85 (range -$1.27 to -$0.59).
  - Consensus was **-$0.77 on report day**. It was -$0.71 when we froze.
  - The result was inside our range, but only by one cent at the bottom.
  - Our "lean miss" call was right. We were $0.41 too optimistic. Consensus was $0.49 too optimistic, or $0.55 on the frozen figure.
- **Price input: close, but slightly too low.**
  - Cal-Maine says its conventional price per dozen fell 59.3% from a year earlier. Applied to the year-ago $2.54, that is about **$1.03 a dozen**.
  - Our implied price was $0.99, about 4 cents (4%) too low.
  - The release and 10-Q give no price per dozen or dozens sold, only percentage changes.
- **Error source:**
  - On revenue, our price and volume errors cancelled out, and shell eggs lost about what we expected at the gross level.
  - The miss came from costs outside the egg price. Overheads (SG&A) came in $13M above our seasonal-low assumption. Egg products and prepared foods made about $9M less gross profit than the 20% margin we assumed.
- **Stock reaction (for the record only; not a test):**
  - CALM closed at $68.55 on 2026-09-29 and $68.06 on 2026-09-30, down 0.7%. The S&P 500 fell 0.3% that day.
  - The stock opened 7.4% lower, at $63.50, and recovered during the day.
  - Source: Yahoo Finance via yfinance, read 2026-10-11.
- **Caveat:** this is one company and one quarter. It shows how the method works; it proves nothing about whether the method works in general.

### Scoring table

Errors are our figure minus the actual. A plus sign means too high for revenue and operating income, and too optimistic for EPS.

| Item | Our estimate | Consensus (frozen / report day) | Actual | Our error | Consensus error (frozen / report day) |
|---|---|---|---|---|---|
| Net sales ($M) | 538.6 (509-572) | 578.5 / 561.6 | **539.6** | **-1.0 (-0.2%)** | +38.9 (+7.2%) / +22.0 (+4.1%) |
| Diluted EPS ($) | -0.85 (-1.27 to -0.59) | -0.71 / -0.77 | **-1.26** | **+0.41** | +0.55 / +0.49 |
| Operating income ($M) | -59.7 | n/a | -82.2 | +22.5 | n/a |
| Conventional segment, average price change vs Q1 FY26 | about -61% ($0.99 vs $2.54 on the old basis) | n/a | -59.3% (about $1.03 on the old basis) | about -1.6 points (-4 cents) | n/a |
| Conventional segment, volume change vs Q1 FY26 | +3.1% | n/a | -0.7% | +3.8 points | n/a |
| Specialty segment, average price change vs Q1 FY26 | about -12% (-11.6%) | n/a | -10.7% | -0.9 points | n/a |
| Specialty segment, volume change vs Q1 FY26 | about -3% (-3.3%) | n/a | -3.8% | +0.5 points | n/a |

### Details

**What Cal-Maine reported** for the 13 weeks to 2026-08-29:
- Net sales were $539.6M and gross profit $0.4M.
- The operating loss was $82.2M. Net loss attributable to Cal-Maine was $58.6M, or -$1.26 a diluted share on 46.70M shares.
- Segment results:
  - Conventional shell eggs: -$71.0M.
  - Specialty shell eggs: +$14.9M.
  - Prepared foods: +$7.8M.
  - Other (mainly egg products): -$8.4M.
  - Unallocated corporate SG&A: -$24.6M.
  - Loss on disposal of fixed assets: -$0.9M.

**Price and dozens, implied.** These figures are worked out from the reported percentage changes and the year-ago figures on the old basis. They are not reported directly.

| | Our estimate | Implied actual |
|---|---|---|
| Conventional price, $/dozen | 0.99 | about 1.03 (1.02 using segment net sales) |
| Conventional dozens (M) | 205.5 | about 197.9 |
| Specialty price, $/dozen | 2.12 | about 2.14 |
| Specialty dozens (M) | 114.4 | about 113.8 |
| All shell eggs, $/dozen | 1.39 | about 1.44 |
| All shell-egg dozens (M) | 319.9 | about 311.7 |

**Revenue: why it came out right.** We were $1.0M low in total. The pieces were bigger and mostly cancelled:
- Conventional price higher than ours: +$8.1M.
- Conventional volume lower than ours: -$7.5M.
- Specialty price higher than ours: +$2.5M.
- Specialty volume lower than ours: -$1.3M.
- Egg products, prepared foods and other: -$0.7M.

Part of the accuracy was luck: two errors of about $8M each, in opposite directions.

**EPS: from our -$0.85 to the actual -$1.26.** Each step is after tax at our 22.6% rate.
- **SG&A: -$0.22.**
  - SG&A was $81.7M against our $68.5M.
  - Unallocated corporate SG&A rose 53% from a year earlier, on insurance and on legal and professional fees.
  - Fuel-driven delivery costs and the Creighton farms added to segment SG&A.
  - Caveat 5 flagged this risk at $75M. It went higher.
- **Cost of sales: -$0.16.**
  - Cost of sales was $539.2M against our $529.7M.
  - Shell eggs had a gross loss of about $9.5M, against about $9.6M in our model, so that part was on target.
  - The gap was in egg products and prepared foods. They made about $9.9M of gross profit; our 20% margin assumption implied $18.5M.
  - Egg-product prices fell 65%, so that business sold below cost. Prepared-foods volume fell 19% during capacity work.
- **Smaller items: -$0.03 net.**
  - Minority interest: -$0.03. Its share of profit, mainly from the Crepini joint venture, was $2.4M against our $0.8M.
  - Other income: -$0.02.
  - Loss on disposal of fixed assets: -$0.02.
  - Revenue: +$0.02.
  - A higher tax rate on the loss (24.2% against our 22.6%): +$0.03.
  - Slightly fewer shares (46.70M against our 46.85M): under $0.01.
- **One-off items:** none of any size. There was no settlement charge, write-down or insurance gain in the quarter.

**Other observations:**
- **Caveat 2 held.** The model was too optimistic in a trough quarter again: by $0.41 this time and $0.54 last quarter.
- **The segment-by-segment check in section 1 came closer on EPS.** It said -$0.96, which was $0.30 too optimistic.
- **Consensus moved towards our number before the report.**
  - In the week after we froze, revenue consensus fell from $578.5M to $561.6M and EPS consensus from -$0.71 to -$0.77.
  - Our lead over the report-day consensus was therefore smaller than over the frozen one.
  - Alphastreet counts only two analysts, so "consensus" here is thin.

### Sources for the result

- **Earnings release** (8-K, EX-99.1, filed 2026-09-30): https://www.sec.gov/Archives/edgar/data/16160/000156276226000111/exhibit991.htm
- **Q1 FY27 10-Q** (filed 2026-09-30), used for segment costs, the SG&A reasons, the tax rate and minority interest: https://www.sec.gov/Archives/edgar/data/16160/000156276226000113/calm-20260829.htm
- **Report-day consensus:**

| Source | EPS | Revenue ($M) | Note |
|---|---|---|---|
| StockStory, 2026-09-30 | -0.77 | 561.7 | [link](https://www.financialcontent.com/article/stockstory-2026-9-30-cal-maine-nasdaqcalm-reports-sales-below-analyst-estimates-in-q3-cy2026-earnings-stock-drops) |
| MarketBeat-syndicated report, 2026-09-30 | -0.77 | 561.57 | [link](https://www.thecerbatgem.com/2026/09/30/cal-maine-foods-nasdaqcalm-issues-earnings-results.html) |
| Alphastreet preview | -0.76 | 561.6 | 2 analysts; EPS range -0.88 to -0.64, revenue range 540.0 to 609.7. From the search summary only, because the page blocked direct reading. [link](https://news.alphastreet.com/cal-maine-foods-calm-q1-2027-preview-eps-est-0-76-reports-september-30/) |
| Investing.com | -0.47 | 587.8 | Cited after the report as the estimate missed, from the search summary; the same figures as on 2026-09-23. Still the outlier. |

- **Stock prices:** Yahoo Finance daily data via yfinance (CALM and ^GSPC), read 2026-10-11.

This is research to test a method. It is not investment advice.
