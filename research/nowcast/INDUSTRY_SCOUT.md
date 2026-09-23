# Industry scout: which US industries can we nowcast?

*Written 2026-09-23. Research only; no trading.*

**The idea.** Find free monthly or weekly public data that shows a company's quarterly revenue before the company reports. Then push that revenue through the company's fixed-cost structure to estimate earnings. US casinos (state gaming-revenue data) are **in progress** separately in `research/nowcast/gaming/PREREG.md` and are not repeated here.

**How facts were checked.** Every source below was opened on 2026-09-23, either by me or by research agents working from agency pages, data files, SEC EDGAR filing dates and company releases.
- Anything that could not be confirmed says **unverified**.
- Market caps are approximate, taken from stockanalysis.com or Yahoo on 2026-09-23. A * marks under $2B.
- "Days to report" means days from quarter-end to the earnings release. It comes from SEC 8-K Item 2.02 filing dates: the median over 2023-2026, or the Q2 2026 date where stated.
- "Lead" is days to report minus the days until the quarter's data are complete.

---

## The answer first

**Yes, there are good candidates.** The best one is a close twin of the casino data. The Texas Comptroller publishes every bar and restaurant's monthly alcohol sales:
- by named business and address;
- free, through an open API;
- back to January 2007;
- complete for the big chains about 20 days after month-end.

No other industry has regulator data at the location level for named US-listed companies. Nothing else we found gets as close to state gaming data.

**Top 5 after casinos**

| Rank | Industry | Data | Score (max 35) |
|---|---|---|---|
| 1 | Restaurants and "eatertainment" | Texas mixed-beverage receipts | 26 |
| 2 | Movie theaters | Daily box office | 24 |
| 3 | Egg producers | USDA egg prices | 24 |
| 4 | Ethanol producers | EIA weekly output and USDA/CARD margins | 24 |
| 5 | Railroads | Weekly carloads by railroad | 24 |

**Next 3 pilots.** Each is explained at the end.
1. Texas mixed-beverage data for restaurants and eatertainment.
2. Box office for theaters.
3. Price-taker small caps: eggs and ethanol together.

**What changed in 2026.** Several expected sources are gone:
- Sun Country (SNCY) was acquired by Allegiant on 2026-05-13 and delisted.
- Allegiant stopped its monthly traffic releases after the December 2025 report.
- Spirit Airlines shut down in early May 2026, per Allegiant's 2026-05-02 release. I did not verify this independently.
- Civitas merged into SM Energy on 2026-01-30.
- Twin Peaks went bankrupt and now trades over the counter.
- Patterson-UTI stopped its monthly rig reports.
- Cato and PriceSmart no longer report monthly sales.
- The Primary Vision frac-count website is now a domain for sale.

---

## How the ranking works

Each industry gets a 1-5 score on six things. Higher always means better for a pilot.

| Criterion | 5 means | 1 means |
|---|---|---|
| **L**: level of the data | Company or property level, from a regulator | Industry-wide only |
| **D**: lead before the report | Quarter complete 30+ days before the report | Not complete before the report |
| **O**: operating leverage | Very high fixed costs, or a price-taker where price changes hit profit almost one-for-one | Costs move with revenue |
| **A**: analyst neglect (**counted twice**) | Little sign anyone uses the data | Sell-side models it explicitly |
| **E**: build effort | Low (clean API or file) | High |
| **T**: testable sample | 300 or more company-quarters of free archive | Under 100 |

- **Total = L + D + O + 2A + E + T**, out of 35.
- Neglect counts double because the casino idea only works if the market is slow to use the data.
- Rank is my judgment, with the score as a guide. Where they disagree, the text says why.

### Operating leverage by industry, from our own SEC panel

I measured this with the survivorship-free SEC panel from the operating-leverage study (`research/oplev/panel.parquet`).
- **Sample.** Annual data for fiscal years 2014-2025. Companies with revenue above $50M and at least 6 years of data.
- **Method.** For each company, I regressed total operating cost on revenue.
- **Flow-through** = 1 minus the slope. It is the cents of each extra revenue dollar that reach operating income.
- **Fixed-cost share** = the intercept divided by mean cost. This is the same measure as H2a in `research/oplev/RESULTS.md`.
- Each figure is the median across the companies in the group.

| Group (SIC) | Companies | Median fixed-cost share | Median flow-through |
|---|---|---|---|
| E&P (1311) | 50 | 0.55 | 0.64 |
| Drilling contractors (1381) | 14 | 0.49 | 0.49 |
| Water transport, incl. cruise and shipping (4400/4412/4481) | 41 | 0.43 | 0.57 |
| Movie theaters (7830/7832) | 5 | 0.42 | 0.46 |
| Oilfield services (1389/3533) | 30 | 0.22 | 0.25 |
| Semiconductors (3674) | 74 | 0.18 | 0.26 |
| *Hotels and casinos (7011), for reference* | 28 | 0.16 | 0.28 |
| General merchandise and apparel retail | 31 | 0.15 | 0.14 |
| Semiconductor equipment (3559) | 11 | 0.10 | 0.20 |
| Industrial organic chemicals, incl. ethanol (2860/2869) | 24 | 0.09 | 0.16 |
| Oil refining (2911) | 11 | 0.09 | 0.11 |
| Airlines (4512/4513/4522) | 20 | 0.08 | 0.12 |
| Agriculture and livestock, incl. Cal-Maine (0100/0200) | 7 | 0.08 | 0.09 |
| Homebuilders (1531) | 6 | 0.08 | 0.19 |
| Autos (3711) | 10 | 0.05 | 0.12 |
| Trucking (4210/4213/4214) | 20 | 0.04 | 0.11 |
| Freight brokers (4731) | 8 | 0.03 | 0.09 |
| Restaurants (5812) | 41 | 0.02 | 0.10 |
| Health insurers (6324) | 11 | 0.01 | 0.01 |
| Railroads (4011/4013) | 6 | 0.00 | 0.37 |
| Electric utilities (4911/4931/4991) | 63 | -0.07 | 0.13 |
| **All companies** | 2,740 | 0.06 | 0.13 |

**Caveats.**
- These are annual figures. When an input cost moves with price, costs rise and fall with revenue, and the measured fixed share falls. Examples are jet fuel, crude oil, corn, feed, and utility fuel pass-through. So the measure understates short-run leverage for airlines, refiners, utilities and ethanol makers.
- For price-takers (eggs, ethanol), the leverage that matters is to *price*. With volume and costs set for the quarter, a price change flows almost one-for-one to operating income. That is my judgment; this regression does not measure it.

---

## Ranking table

| Rank | Industry and main data | Level | Lead before report | Operating leverage | Analyst watch | Effort | Small caps (<$2B) | L | D | O | A | E | T | Score |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| - | **Casinos (state gaming revenue)** | Property | ~0-20 days | High | Medium | High | Several | **In progress. See gaming/PREREG.md** | | | | | | |
| 1 | Restaurants and eatertainment (Texas mixed-beverage receipts) | Location, alcohol only, Texas only | ~9-18 days | Medium | Low | Medium | BJRI, PLAY | 4 | 3 | 3 | 4 | 3 | 5 | **26** |
| 2 | Movie theaters (daily box office) | Industry; film by film, close to company | ~19-36 days | Very high (0.42 fixed share) | High (medium for MCS) | Low | MCS, RDI | 3 | 4 | 5 | 2 | 5 | 3 | **24** |
| 3 | Egg producers (USDA egg prices) | Industry price; Cal-Maine is a price-taker | ~25-52 days | High (to price) | Low to medium | Medium-high (archive risk) | VITL | 3 | 5 | 4 | 4 | 2 | 2 | **24** |
| 4 | Ethanol producers (EIA output, USDA/CARD margin) | Industry | ~28-32 days | High (to margin) | Low to medium | Medium | GPRE, REX, ALTO | 2 | 4 | 4 | 4 | 3 | 3 | **24** |
| 5 | Railroads (weekly carloads by railroad) | Company | ~17-22 days | High (0.37 flow-through) | High | Low | None | 5 | 4 | 4 | 1 | 5 | 4 | **24** |
| 6 | Semiconductors (Taiwan MOPS monthly revenue, ADRs) | Company, self-reported | ~6-32 days | Above median (0.18) | High | Low | None (IMOS now $2.36B) | 5 | 3 | 4 | 1 | 5 | 4 | **23** |
| 7 | Mexican airport groups (monthly traffic) | Company and airport, self-reported | ~8-21 days | High (judgment) | Medium-high | Low | None | 4 | 3 | 4 | 2 | 5 | 3 | **23** |
| 8 | Container shipping (SCFI, Drewry WCI, LA port volumes) | Industry | ~15-50 days | Very high (0.43) | Low to medium | Medium-high (no free archive) | None | 2 | 5 | 5 | 4 | 2 | 1 | **23** |
| 9 | Drillers and oilfield services (rig count, frac crews) | Industry | ~17-43 days | Very high for drillers (0.49) | High | Low | NBR, PDS, PUMP, ACDC, AESI, SND, RES, NINE, KLXE | 2 | 4 | 5 | 1 | 4 | 4 | **21** |
| 10 | Trucking and freight, incl. small caps (Cass, ATA, DAT) | Industry | ~9-24 days | Low (0.04) | Low to medium for small caps | Low | HTLD, MRTN, CVLG, PAMT, ULH, HUBG, FWRD | 1 | 3 | 2 | 3 | 5 | 4 | **21** |
| 11 | Autos (monthly unit sales by maker) | Company units, self-reported | ~20-60 days | Low to medium (0.05) | Very high | Low | None | 4 | 5 | 2 | 1 | 5 | 3 | **21** |
| 12 | Airlines (TSA, Latin carriers' monthly traffic, airfare CPI, jet fuel) | Industry; some carriers | ~9-34 days | High in the short run (panel 0.08) | High | Low to medium | JBLU, ULCC | 3 | 4 | 3 | 1 | 4 | 4 | **20** |
| 13 | Hotels, Las Vegas and Hawaii (LVCVA, DBEDT, STR) | Market level | ~2-26 days | High (0.16) | High | Low | Some lodging REITs (unverified) | 3 | 2 | 4 | 2 | 4 | 3 | **20** |
| 14 | Health insurers (CMS Medicare Advantage enrollment) | Contract level | ~30-50 days | Lowest (0.01) | High | Medium | ALHC | 5 | 5 | 1 | 1 | 3 | 4 | **20** |
| 15 | Utilities and power (EIA-861M, nuclear outages, degree days) | Utility / reactor level | Negative for EIA-861M; ~23-37 days for weather and nuclear | Low (pass-through) | High | Medium | None checked | 4 | 2 | 2 | 2 | 3 | 4 | **19** |
| 16 | E&P (state production by operator: ND, TX, NM, CO, PA) | Well and operator | Negative (last month arrives after the report) | Highest (0.55) | Medium-high | High | HPK | 4 | 1 | 5 | 2 | 1 | 4 | **19** |
| 17 | Retail, outside Texas (Census retail sales, Placer.ai, BofA, Costco/Buckle) | Industry, or self-reported | ~13-22 days | Medium-low | High | Low | BKE (cap unverified) | 2 | 3 | 2 | 1 | 5 | 3 | **17** |
| 18 | Dry bulk and tankers (Baltic indices) | Industry | ~13-36 days | Very high | Medium (companies pre-release) | High (no free archive) | GNK, SB, DSX | 2 | 3 | 5 | 2 | 1 | 2 | **17** |
| 19 | Credit-card issuers (monthly credit 8-Ks, trust 10-Ds) | Company, but credit not revenue | Last month withheld | Low | High | Low | None | 5 | 2 | 1 | 1 | 4 | 4 | 18, moved down: measures credit, not revenue |
| 20 | Homebuilders (Census new home sales) | Industry | ~-10 to +13 days | Medium-low (0.08) | High | Low | LGIH, BZH, HOV, CCS, DFH | 1 | 2 | 2 | 1 | 5 | 4 | **16** |
| 21 | Cruise (none found) | None | n/a | High (0.43) | High | n/a | LIND (cap unverified) | 1 | 1 | 5 | 1 | 1 | 1 | **11** |

**Judgment calls on the ranking.**
- **Theaters rank above eggs and ethanol** on the same score. They have the only verified free deep archive of the three (daily box office back to 1985) and the highest measured leverage.
- **Railroads rank last of the 24s.** They are the most heavily watched.
- **Semiconductors and Mexican airports rank below the 24s.** Both self-report their monthly numbers. The market sees those numbers the day they come out, so any edge must come from the operating-leverage step alone.

---

## Industry detail

### Casinos: in progress
- **Status.** Covered by `research/nowcast/gaming/PREREG.md`. Not repeated here.
- **Possible extensions, for that team to decide:**
  - New York weekly and monthly mobile sports-wagering reports by operator: https://gaming.ny.gov/revenue-reports. The weekly DraftKings file was posted about 4 days after the week closed. Maps to DKNG, FLUT, RSI.
  - Macau DICJ monthly gross gaming revenue. Industry level, 1-day lag, English file from 2010. Maps to LVS, WYNN, MLCO* ($1.8B).
  - LVCVA Strip RevPAR (see Hotels below).

### 1. Restaurants and eatertainment: Texas Mixed Beverage Gross Receipts

**Source**
- Dataset: https://data.texas.gov/dataset/Mixed-Beverage-Gross-Receipts/naix-2893
- API: https://data.texas.gov/resource/naix-2893.json

**Access, frequency, lag and archive**
- Free, no key. Monthly.
- Returns are due on the 20th of the next month.
- The portal was last updated 2026-09-19. By then, August 2026 was already complete for the big chains; I checked location counts myself:

| Chain | Locations in August | Locations in July |
|---|---|---|
| Chili's | 216 | 216 |
| BJ's | 37 | 37 |
| Main Event | 22 | 22 |
| Dave & Buster's | 19 | 18 |
| Chuy's | 54 | 54 |

- Across all filers, August was only about 59% filed (13,188 of about 22,500), because small bars file late.
- **So a chain's quarter is complete about 20 days after quarter-end.**
- Archive: January 2007 to date, 3.84 million rows. I confirmed this with the API.

**Level: location.**
- Fields: taxpayer name and number; location name, address and county; TABC permit; liquor, wine, beer and cover-charge receipts; total.
- Alcohol only.
- Mixed-beverage permit holders only, so beer-and-wine-only places are missing. Cracker Barrel has 1 row.
- Texas only.

**Companies (July 2026 Texas locations and alcohol receipts, matched by name)**

| Company | Texas brands | Locations | Alcohol receipts |
|---|---|---|---|
| Brinker (EAT) | Chili's; Maggiano's | 213; 7 | $8.6M; $0.5M |
| Texas Roadhouse (TXRH) | Texas Roadhouse | about 108-111 | $7.4M |
| Darden (DRI) | Olive Garden, LongHorn, Cheddar's, Yard House, Chuy's | 86 / 44 / 59 / 10 / 58 | not tallied |
| BJ's Restaurants (BJRI*, $1.3B) | BJ's | 37 | $2.4M |
| Cheesecake Factory (CAKE) | Cheesecake Factory | 21 | $1.8M |
| Dave & Buster's (PLAY*, about $240M) | D&B; Main Event | 16-19; 22 | not tallied |
| Lucky Strike (LUCK) | Lucky Strike | 19 | not tallied |
| Cinemark (CNK) | Cinemark | 45 | not tallied |
| AMC | AMC | 41 | not tallied |
| Bloomin' Brands | Outback | 51 | not tallied |
| Others | First Watch, Kura Sushi | small | small |

- Market caps for LUCK, Bloomin', First Watch and Kura are unverified.
- **Drop from the list:**
  - Twin Peaks: Chapter 11 on 2026-01-26; now trades OTC as TWNPQ.
  - Topgolf: 60% owned by Leonard Green since 2026-01-01.

**Timing.** Days to report: CAKE 29, BJRI 30, CNK 34, EAT 35, TXRH 37, PLAY 38. PLAY's fiscal quarters end a month after calendar quarters. That gives a **lead of about 9-18 days**.

**Operating leverage: medium.**
- Panel restaurants: 0.02 fixed share, 0.10 flow-through, below the all-company median.
- The theaters and eatertainment in this dataset carry more fixed cost.

**Analyst watch on this dataset: low.**
- The research found no public evidence that analysts or funds use it.
- Commercial resellers exist (alcoholsales.com, barmart.net, alcoholsalestracker.com), so the data is known.
- The companies themselves are well covered: EAT, TXRH and DRI each have about 24-29 analysts; BJRI 11 (MarketBeat); PLAY 9.

**Effort: medium.**
- Company-to-taxpayer matching. Texas Roadhouse uses one entity per store.
- Build a same-store panel.
- Map calendar months to fiscal quarters.
- The casino pipeline (ownership timeline, same-store growth, flow-through) can be reused.

**Quick sanity check (not a test).**
- I summed Chili's Texas alcohol receipts from the API over Brinker's fiscal quarters, approximated as calendar months.
  - FY25 Q2 (Oct-Dec 2024): **+13.3%** year on year.
  - FY25 Q3 (Jan-Mar 2025): **+11.4%**.
- Chili's reported comparable sales for the same quarters:
  - Q2: about +31% ([Restaurant Dive](https://www.restaurantdive.com/news/chilis-31-percent-comprable-sales-broke-records-traffic-up-fiscal-q2-2025/738678/)).
  - Q3: +31.6% (Brinker release).
- The signal got the direction and the acceleration right, but only about a third of the size. Chili's surge was driven by food and value deals, not drinks.
- **Lesson.** Treat this as a sample that needs per-company calibration. The first gate of any pilot is how well Texas same-store alcohol growth tracks each company's reported comps.

### 2. Movie theaters: daily box office

**Sources**
- Box Office Mojo daily: https://www.boxofficemojo.com/date/2026-09-21/. Daily data goes back to at least 1985-01-01.
- The Numbers daily: https://www.the-numbers.com/box-office-chart/daily/2026/09/22. 2000 onward confirmed; earlier years unverified.
- Both free. Next-day lag.

**Level.** Industry: domestic (US and Canada) grosses film by film. The big chains' share of admissions is fairly stable, and concessions scale with attendance, so it is close to company level for domestic revenue.
- International revenue (for example CNK's Latin America and AMC's Europe) is not covered. A free source for it is unverified.

**Companies**

| Ticker | Market cap | Q2 2026 report |
|---|---|---|
| AMC | about $2.3B, borderline | Jul 20 (20 days) |
| CNK | about $4.1B | Jul 30 |
| IMAX | $2.97B | Jul 23 |
| MCS* | $852M | Jul 29-30; also owns hotels |
| RDI* | $44M | unverified |

**Timing.** The quarter is complete the day after quarter-end. Median days to report over 2023-2026: AMC 37, IMAX 26, CNK 34, MCS 35. **Lead about 19-36 days.**

**Operating leverage: very high.** Panel theaters: 0.42 fixed share, 0.46 flow-through. That is 4th of 22 groups and about 3.6 times the all-company median.

**Analyst watch: high** for AMC, CNK and IMAX; medium for MCS.
- Evidence: B. Riley's Eric Wold, in a June 2023 note, cited quarter-to-date domestic box office ($2.575B) as a risk to IMAX and Marcus estimates.
- CNK has 13-15 analysts; MCS has 6.

**Effort: low.**

### 3. Egg producers: USDA egg prices

**Sources**
- USDA AMS Egg Markets Overview, weekly: https://www.ams.usda.gov/mnreports/ams_3725.pdf. Latest dated 2026-09-18.
- Daily National Shell Egg Index: https://mymarketnews.ams.usda.gov/viewReport/2843
- Weekly Combined Regional report: https://mymarketnews.ams.usda.gov/viewReport/2848
- All free.

**Archive (the main risk)**
- MyMarketNews: back to at least March 2025.
- USDA ESMIS archive (https://esmis.nal.usda.gov/publication/egg-markets-overview): back to about December 2023.
- A deeper free wholesale price archive: **unverified**.
- The MARS API refused requests without credentials. Whether a key is free: unverified.
- Long free fallback: the BLS average retail price for Grade A large eggs (FRED APU0000708111). It is monthly; August 2026 was $2.272, released 2026-09-11. It is said to start in 1980 (start date unverified), and retail prices lag wholesale.

**Level.** Industry price. Cal-Maine is the largest US producer and a price-taker. Cal-Maine itself cites Urner Barry quarter-to-date prices, which are paid (for example $0.72 a dozen over the first five weeks of fiscal Q1).

**Companies**
- CALM: $3.35B, 4-5 analysts.
- VITL*: $445M, 10 analysts. Its pasture-raised pricing is only weakly tied to commodity egg prices (judgment).

**Timing**
- Prices are complete a day after quarter-end.
- CALM reports about 32 days after its fiscal Q1-Q3 and 53 days after Q4. The fiscal year ends around late May or early June.
- CALM's next report is **2026-09-30**.
- VITL reports at about 39 days.
- **Lead about 25-52 days.**

**Operating leverage: high to price.** The panel's agriculture group (0.08 / 0.09, 7 companies) does not measure the price effect; see the caveat under the leverage table.

**Analyst watch: low to medium.** CALM has 4-5 analysts. An Investing.com piece (2026-08-18) presented this USDA tool as a Cal-Maine signal.

**Effort: medium,** mainly because the price history has to be pieced together.

### 4. Ethanol producers: EIA weekly output and USDA/CARD margins

**Sources**
- EIA weekly ethanol production: https://www.eia.gov/dnav/pet/pet_pnp_wprode_s1_w.htm. Free, released Wednesdays with about a 5-day lag, from 2010.
- USDA AMS ethanol reports on MyMarketNews: National Weekly Ethanol Report (3616), daily (3617), grain co-products (3618).
- Iowa State CARD ethanol margin tool: https://www.card.iastate.edu/research/biorenewables/tools/hist_eth_gm.aspx
  - It tracks returns over operating cost from daily prices.
  - Its benchmark changed in February 2026 to the Platts Chicago swap, after CBOT ethanol futures were delisted.
  - Its archive and download option are unverified.

**Level: industry.**

**Companies (all small caps)**

| Ticker | Market cap | Analysts | Days to report |
|---|---|---|---|
| GPRE* | $1.05B | 6 | 37 |
| REX* | $1.45B | unverified | 33 (fiscal quarters end Jan/Apr/Jul/Oct) |
| ALTO* | $291M | 2 | 36-37 |

**Lead: about 28-32 days.**

**Operating leverage: high to the crush spread**, damped by hedging.
- The panel's "industrial organic chemicals" group (0.09 / 0.16) mixes ethanol makers with chemical companies.
- GPRE reports its own "consolidated ethanol crush margin".

**Analyst watch: low to medium.** GPRE missed Q2 2026 revenue ($446M against $498M expected), so estimates are imperfect.

**Effort: low to medium.**

### 5. Railroads: weekly carloads

**Industry source.** AAR weekly report: https://www.aar.org/data-center/
- The 5-page PDF is free. Detail by railroad is paid.
- Published Wednesdays at noon, about 4 days after the week ends.
- PDFs load from April 2018. Figures can be revised for up to a year.
- FRED's monthly RAILFRTCARLOADSD11 covers 2000 to date.
- The US table leaves out the US operations of CPKC and CN.

**Company sources (all free, weekly)**

| Railroad | Where | Lag | Archive |
|---|---|---|---|
| Union Pacific | https://investor.unionpacific.com/carloads-2025 | 4 days or less | 2018 onward |
| CSX | https://investors.csx.com/metrics/default.aspx | unverified | Excel of weekly metrics from 2022 |
| Norfolk Southern | https://norfolksouthern.investorroom.com/weekly-performance-reports | 5 days or less | 2018 onward |
| CPKC | https://investor.cpkcr.com/key-metrics/default.aspx | Mondays by 2pm ET | unverified |
| CN | https://www.cn.ca/en/investors/key-weekly-metrics/ | a few days | 2016 onward |

- STB EP 724 (https://www.stb.gov/reports-data/rail-service-data/) has weekly originated and received carloads for each Class I railroad, including privately owned BNSF.
  - Lag about 5 days. Consolidated file from 2017.
  - The form's approval number expires 2026-12-31.

**Level: company.** Revenue also depends on revenue per car: mix and fuel surcharge. The surcharge can be estimated from EIA diesel prices.

**Companies.** UNP $164B, CSX $88B, NSC $71B, CP $77B, CNI $72B. No small caps.
- **Merger.** The STB accepted the revised UNP-NSC merger application effective 2026-05-28. The companies expect to close in mid-2027, so NSC will likely stop as a separate series.

**Timing.** Days to report: CSX 22, UNP 24, NSC 25. **Lead about 17-22 days.**

**Operating leverage: high.** 0.37 flow-through, the 2nd highest incremental margin in the panel. The fixed share shows near 0 because costs grew with the business over the decade.

**Analyst watch: high.**
- About 25 analysts each.
- On 2026-06-17, BofA raised its CSX estimates because quarter-to-date carloads were running +6.0% against its +2.7% estimate.

**Effort: low.**

### 6. Semiconductors: Taiwan MOPS monthly revenue, plus industry data

**MOPS (company level)**
- Summary pages: https://mopsov.twse.com.tw/nas/t21/sii/t21sc03_115_8_0.html (August 2026).
- English pages: https://emops.twse.com.tw/nas/t21/sii/t21sc03_2026_8_e_0.html
- The main mops.twse.com.tw host now blocks scripts; the "mopsov" host works.
- Free CSV. TWSE OpenAPI has the latest month only: https://openapi.twse.com.tw/v1/opendata/t187ap05_L
- **Rule:** monthly revenue is due by the 10th of the next month. This comes from a secondary source citing Securities and Exchange Act Art. 36; I did not read the statute.
- Archive: Chinese pages from June 2001; English from January 2013.

**US-listed companies that report monthly**

| Company | TWSE code | US listing | August 2026 revenue | Filed |
|---|---|---|---|---|
| TSMC | 2330 | TSM | NT$514.8B | 6-K Sep 10 |
| UMC | 2303 | UMC | NT$25.0B | Sep 3 |
| ASE | 3711 | ASX | NT$82.3B | Sep 9 |
| ChipMOS | 8150 | IMOS | NT$2.8B | Sep 10 |

- **IMOS is about $2.36B, so no longer a small cap.** It has 5 analysts on the Taiwan line.
- Chunghwa Telecom (CHT) also reports monthly: revenue, operating income, net income and EPS.
- **No monthly revenue:** HIMX, SIMO and GGR.

**Industry sources**

| Source | Where | Free? | Frequency | Lag | Archive |
|---|---|---|---|---|---|
| SIA / WSTS | https://www.wsts.org/67/Historical-Billings-Report | Historical file free; detailed data paid | Monthly | About 5 weeks (July 2026 on 2026-09-04) | 1986 onward |
| SEAJ Japan equipment | https://www.seaj.or.jp/english/statistics/index.html | Yes | Monthly, 3-month average | 18-21 days | Free XLS from 2005 |
| Korea customs exports | https://www.customs.go.kr/kcs/na/ntt/selectNttList.do?bbsId=1362&mi=2891 | Yes | Days 1-10 and 1-20 of each month | 1 day | Mid-2024 onward confirmed |

- SIA's July 2026 headline: 3-month average $146.8B.
- Korea's September 1-20 chip exports: $34.1B, +259%.
- SEMI's North America figures:
  - Book-to-bill discontinued in 2017.
  - Monthly billings press release stopped in February 2022.
  - Whether the current report is free: unverified.

**Timing.** Days to report: TSM 16, UMC 29, ASX 30, IMOS 42. With data complete about 10 days after quarter-end, the **lead is about 6-32 days**.

**Operating leverage: above median.** Panel semiconductors: 0.18 fixed share, 0.26 flow-through. Foundries and packaging houses carry heavy depreciation.

**Analyst watch: high.**
- Reuters compared TSMC's Q1 revenue from the monthly reports with the LSEG estimate from 20 analysts, 6 days before earnings.
- CNBC covers the monthly figures.
- Barchart uses UMC's monthly sales as a read-through.

**Effort: low.**

**Role.** Revenue is published by the company before the report, so the revenue surprise at earnings is about zero. That makes this a clean test of the operating-leverage step alone.

### 7. Mexican airport groups: monthly passenger traffic

**Sources**
- OMA: https://ir.oma.aero/en/traffic-reports/ (PDFs from December 2006).
- GAP: https://www.aeropuertosgap.com.mx/en/investors.html (airport by airport).
- ASUR: releases on prnewswire.com; archive unverified.
- All also filed as 6-Ks. Free.
- August 2026 came out Sep 4 (GAP, OMA) and Sep 8 (ASUR): **4-8 days after month-end.**

**Level.** Company and airport. Passengers only, not revenue. ASUR added 20 airports (Motiva) on 2026-09-01, so its totals change from September data.

**Companies.** PAC $12.4B, ASR $7.3B, OMAB $5.0B. No small caps.

**Timing.** Days to report (Q2 2026): GAP about 14, ASUR 23, OMA 27. **Lead about 8-21 days.**

**Operating leverage: high** (judgment: concession and depreciation costs are fixed). Not in our panel, because these are foreign filers.

**Revenue link: loose.** Aeronautical tariffs are regulated per passenger, but:
- GAP Q2 2026: traffic -5.6%, revenue +3.7% (an acquisition, plus non-aeronautical revenue +23.9%).
- ASUR Q2 2026: traffic -2.7%, revenue excluding construction -0.3%.

**Analyst watch: medium.** 7-9 analysts each, and every release gets wire coverage.

**Effort: low.**

### 8. Container shipping

**Sources**

| Source | Where | Free? | Frequency | Archive |
|---|---|---|---|---|
| SCFI | en.sse.net.cn | Current and prior week only | Weekly | Behind a subscriber login, **not free** |
| Drewry World Container Index | drewry.co.uk | Yes | Weekly, Thursdays (Sep 17: $4,500 per 40ft) | Unverified |
| Freightos FBX | freightos.com | Partly; exports paid | Daily | Unverified |
| Port of Los Angeles volumes | https://www.portoflosangeles.org/business/statistics/container-statistics | Yes | Monthly, about the 15th | 1995 onward |

**Level: industry.**

**Companies**
- ZIM: $3.65B, 4 analysts, reports about 50 days after quarter-end. Its Q2 2026 presentation cites SCFI.
- MATX: $6.7B, 3 analysts. Preliminary 8-K at 15 days, full results at 34.

**Operating leverage: very high.** Panel water transport: 0.43 fixed share, 0.57 flow-through.

**Why it is not higher.** There is no free rate archive, and ZIM has only listed since 2021, so the sample is too small.

### 9. Drillers and oilfield services

**Baker Hughes rig count**
- https://rigcount.bakerhughes.com/na-rig-count
- Free. Weekly, Fridays at noon Central, same-week data (September 18: 595 US rigs).
- Excel archives: annual by state from 1987, weekly by state from 2000, pivot table 2011-2024, detailed report 2013-2025, plus the current filterable file.
- Level: industry, by basin, state, county and well type. **No contractor or operator detail.**

**Frac crews**
- Primary Vision's count is still quoted weekly (184 crews for the week to Sep 11, per Oilprice.com on 2026-09-18).
- But primaryvision.com now redirects to a domain-for-sale page. Its free headline and history are unverified.
- Free alternative: FracFocus (https://fracfocus.org/data-download).
  - Well-level completions with operator and treatment date, from 2011.
  - Updated 5 days a week.
  - Disclosure lag varies by state: unverified.

**Company releases**
- Patterson-UTI issued monthly rig-count releases through December 2023 (released 2024-01-08). No later ones were found, so they were probably discontinued in 2024.
- H&P, Nabors and Precision report quarterly only.
- Offshore drillers (Transocean, Valaris, Noble, Borr) publish fleet status reports quarterly.
- Transocean and Valaris signed a merger agreement on 2026-02-09.

**Companies**

| Ticker | Market cap | Days to report |
|---|---|---|
| HP | $3.9B | 35-37 |
| PTEN | $4.2B | 23-30 |
| LBRT | about $3.0B | 17-29 |
| NBR* | $1.3B | 28-29 |
| PDS* | $1.1B | 22-30 |
| PUMP* | $1.2B | 29-30 |
| ACDC* | $0.85B | 37-41 |
| AESI* | $1.45B | 34-35 |
| RES* | $1.3B | 24-37 |
| SND* | $0.21B | 42-43 |
| NINE* | $0.13B | 30-43 |
| KLXE* | about $0.03B | 36-43 |

**Lead about 17-43 days.**

**Operating leverage: very high for drillers** (0.49 fixed share, 2nd highest). Oilfield services: 0.22.

**Analyst watch: high** (judgment). The rig count is the most widely reported weekly oil-activity number, and Flotek and TETRA cite the frac count in their own materials.

**Effort: low** for the rig count. The weakness is the link to each company: contractor-level rig counts are sold by Enverus (paid).

### 10. Trucking and freight, including small caps

**Industry sources**

| Source | Where | Free? | Frequency | Lag | Archive |
|---|---|---|---|---|---|
| Cass Freight Index | https://www.cassinfo.com/freight-audit-payment/cass-transportation-indexes | Yes | Monthly | 11-14 days | FRED 2016 onward; Cass PDFs 2018 onward |
| ATA Truck Tonnage | https://www.trucking.org/news-insights | Headline free; history paid | Monthly | About 22 days | FRED TRUCKD11 (from BTS) 2000 onward, about 2 months behind |
| DAT truckload rates | https://www.dat.com/company/news-events/news-releases | Headline free; history paid | Monthly, plus a weekly spot snapshot | About 15 days | Paid |

- FRED series for Cass: FRGSHPUSM649NCIS and FRGEXPUSM649NCIS.
- Cass also publishes a Truckload Linehaul Index.

**Company mid-quarter updates.** These come **once a quarter, not monthly**. They cover the first two months of the quarter and come out 2-8 days after the second month ends:
- ODFL: https://ir.odfl.com
- XPO
- SAIA
- ARCB
- TFI and KNX give no regular updates between quarters.

**Small caps**

| Ticker | Market cap | Analysts | Days to report |
|---|---|---|---|
| HTLD* | $900M | 6 | 30 |
| MRTN* | $1.08B | 3 | 23 |
| CVLG* | $870M | 5 | 29 |
| PAMT* (formerly PTSI) | $245M | 1 (possibly stale) | 35 |
| ULH* | $430M | 1 true sell-side | 31 |
| HUBG* | $1.94B | unverified | unverified |
| FWRD* | $504M | unverified | unverified |

- HUBG filed a non-reliance 8-K on 2026-02-05, meaning its earlier financial statements can no longer be relied on.
- Over $2B: WERN $2.09B, ARCB $2.95B, SNDR $5.7B.

**Lead:** about 9-24 days on Cass.

**Operating leverage: low.** Trucking: 0.04 fixed share, 0.11 flow-through. Driver pay, fuel and purchased transport move with volume.

**Analyst watch.** Low to medium for the small caps. I found no sell-side note citing Cass or ATA (unverified).

**Weakness.** Industry indices only. A truckload carrier's revenue depends on its own fleet and contract rates.

### 11. Autos

**Monthly US unit sales** (released about 1-2 days after month-end)
- Ford (for example https://s205.q4cdn.com/882619693/files/doc_news/2026/Sep/02/Ford-U-S-August-2026-Sales-Release.pdf).
- Toyota, Honda, Hyundai, Kia, Subaru and Mazda. Their individual newsroom URLs are unverified.

**Quarterly only**
- GM (https://news.gm.com), Stellantis and Nissan.
- Tesla: deliveries come 2 days after quarter-end, each backed by an 8-K.

**Other sources**
- NIO, XPEV and LI still report deliveries monthly, on the 1st (for example on globenewswire.com, 2026-09-01).
- Industry: FRED TOTALSA and ALTSALES, about a 4-day lag, from 1976.
- Cox Automotive publishes a free monthly forecast.

**Timing.** Days to report: GM 21, TSLA 22, F 28, XPEV about 55, LI about 57, NIO about 63. **Lead about 20-60 days.**

**Operating leverage: low to medium.** Autos: 0.05 fixed share, 0.12 flow-through.

**Analyst watch: very high.** Analysts forecast deliveries directly; Tesla's Q2 2026 deliveries beat consensus by about 74,000 (Electrek, 2026-07-02). Unit numbers are priced the day they come out. Surprises at earnings come from price, mix and credits.

**Effort: low.**

### 12. Airlines

**Sources**

| Source | Where | Free? | Frequency | Lag | Archive | Level |
|---|---|---|---|---|---|---|
| TSA checkpoint numbers | https://www.tsa.gov/travel/passenger-volumes | Yes | Daily | 1 day | From 2019, one page per year | National |
| BTS T-100 | https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FIM | Yes | Monthly | About 72-74 days | 1990 onward | Carrier |
| BTS DB1B ticket sample | transtats.bts.gov | Yes | Quarterly | Stale | Download stops at Q2 2025 | Carrier |
| BLS airline fares CPI (CUUR0000SETG01) | https://data.bls.gov/timeseries/CUUR0000SETG01 | Yes | Monthly | About 10-14 days | From 1963 | Industry |
| EIA Gulf Coast jet fuel | https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EER_EPJK_PF4_RGC_DPG&f=D | Yes | Daily values, published Wednesdays | About 1 week | From 1990 | Market price |

- **TSA 2026 data problem.** There was a funding lapse from about March to April 2026. Airport-level data for March 1 to June 13 was re-posted on 2026-07-22. Whether the national totals were corrected is unverified.
- TSA also posts weekly airport-by-hour PDFs in its FOIA reading room, about 2 days behind.
- **T-100 comes too late.** March 2026 data came out June 11 and May on August 13, which is after every airline reports. It covers passengers, seats and departures, not revenue.
- DB1B's average-fare summary is still published (Q1 2026 by June 25).
- The airline fares CPI has no value for October 2025.
- Jet fuel is also on FRED as DJFUELUSGULF.

**Airline monthly traffic**
- **Allegiant stopped** after its December 2025 data (released 2026-01-22; archive at https://ir.allegiantair.com/financials/traffic-updates/default.aspx).
- **Sun Country delisted** after Allegiant closed the acquisition on 2026-05-13 ([Allegiant release](https://ir.allegiantair.com/news/news-details/2026/Allegiant-Completes-Acquisition-of-Sun-Country-Airlines-Creating-the-Leading-Leisure-Focused-U-S--Airline/default.aspx)).
- Still monthly:

| Airline | Where | Released | Metrics |
|---|---|---|---|
| Copa (CPA) | https://copa.gcs-web.com | 7th-12th | Capacity, traffic, load factor |
| Volaris (VLRS) | https://ir.volaris.com | 3rd-5th | Passengers, capacity, traffic |
| LATAM (LTM) | https://ir.latam.com/English/results-center/traffic-releases/default.aspx | 8th-10th | Traffic by segment |
| Aeroméxico (AERO) | NYSE since Nov 2025, about $2.3B | 2nd-8th | Unverified |

**Airports by airline**
- Las Vegas: monthly PDFs of passengers by airline, about 4 weeks behind: https://www.harryreidairport.com/business/airport-operations/financial-reporting-statistics/airport-activity/2026-aviation-statistics
- Orlando: monthly by airline, 23 days or less: https://flymco.com/airport-business/traffic-statistics/

**Companies and timing (Q2 2026 days to report)**

| DAL | UAL | ALK | LUV | AAL | JBLU* | ULCC* | ALGT | CPA |
|---|---|---|---|---|---|---|---|---|
| 10 | 15 | 21 | 22 | 23 | 28 | 29 | 35 | 36 |

- Market caps: JBLU $1.66B, ULCC $1.37B, ALGT $2.13B, CPA $5.37B.
- **Lead:** about 9-34 days on TSA; zero or less for DAL on the airfare CPI.

**Operating leverage.**
- The panel shows 0.08 / 0.12, but fuel costs move with revenue in annual data.
- Within a quarter the schedule is already set, so most costs are fixed (judgment: high).
- Surprises come mainly from unit revenue (price), which TSA volumes do not show.

**Analyst watch: high.** Small caps still have 12-17 analysts. Evidence that analysts model revenue from TSA is weak: a Jefferies quote (July 2025) and FlightBI selling airport-level TSA data.

### 13. Hotels, Las Vegas and Hawaii

**Sources**

| Source | Where | Free? | Frequency | Lag | Archive | Level |
|---|---|---|---|---|---|---|
| LVCVA | https://www.lvcva.com/research/visitor-statistics/ | Yes | Monthly | About 27 days | 2020 onward, plus a 1970-2025 history file | Las Vegas market |
| STR/CoStar weekly results | https://www.costar.com/products/str-benchmark/resources/press-releases | Headline free | Weekly | About 9-10 days (trade-press reposts) | Unverified | US and top-25 markets |
| Hawaii visitor statistics | https://dbedt.hawaii.gov/visitor/tourism/ | Yes | Monthly | About 27 days | Unverified | State |
| Hawaii hotel performance | https://files.hawaii.gov/dbedt/economic/tourism/hotel-performance/Hotel-performance-2026-07.pdf | Yes | Monthly | About 24 days | Unverified | Island, region and hotel class (STR data) |

- LVCVA covers visitors, occupancy, RevPAR (including the Strip), room nights and conventions.
- STR covers occupancy, room rate and RevPAR.
- **Texas hotel tax by property** exists, with each hotel's name and room receipts. A 2017 law (SB 1086) took it off public websites; it now needs a secure-site login. **Not free and public.**

**Companies.** Hotel REITs (Park, Host, Pebblebrook and others). Strip casino operators are already in the casino pilot.
- Days to report: PK 32, HST 36, PEB 29.
- **Lead:** about 2-9 days for LVCVA and Hawaii; about 19-26 days for STR.

**Operating leverage: high.** Hotels and casinos: 0.16 fixed share, 0.28 flow-through.

**Analyst watch: high** (judgment; lodging analysts routinely use STR).

**Best use.** As an extra input to the casino pilot (Strip RevPAR), and for Park's Hawaii exposure, rather than as a standalone pilot.

### 14. Health insurers: CMS Medicare Advantage monthly enrollment

**Source.** CMS monthly enrollment by contract: https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/monthly-enrollment-contract
- Free. Monthly, posted mid-month **for the same month** (the September file was posted 2026-09-14).
- Archive from December 2006.
- Contract level. A third-party catalog says the files carry a parent-organization field; unverified.

**Companies.** UNH, HUM, CVS, ELV, CI, CNC, MOH; CLOV $2.4B; **ALHC* $1.6B**.

**Timing.** The quarter is known about 2 weeks before quarter-end. Days to report are 15-36, so the **lead is about 30-50 days.**

**Operating leverage: the lowest of any group** (0.01 / 0.01). Premium revenue moves with medical costs, and these stocks move on medical-cost surprises.

**Analyst watch: high.** Healthcare Dive, Fierce Healthcare and KFF write up each release.

**Verdict.** Excellent data, but it fails the operating-leverage half of the idea.

### 15. Utilities and power

**Sources**

| Source | Where | Frequency | Lag | Archive | Level |
|---|---|---|---|---|---|
| EIA-861M sales and revenue | https://www.eia.gov/electricity/data/eia861m/ | Monthly | About 8 weeks (June 2026 on 2026-08-26) | Utility level from 1990 | Utility operating company and state, about 355 utilities |
| EIA-923 generation | https://www.eia.gov/electricity/data/eia923/ | Monthly | About 57 days | Utility plants from 1970 | Plant |
| NRC reactor status | https://www.nrc.gov/reading-rm/doc-collections/event-status/reactor-status/ps.html | Daily | Same day | 1999 onward | Reactor unit |
| EIA nuclear outages (mirror) | https://api.eia.gov/v2/nuclear-outages/generator-nuclear-outages/ | Daily | Same day | 2007 onward | Generator |
| NOAA CPC degree days | https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/degree_days/ | Daily, weekly, monthly | About 1-3 days | Daily weighted from 1981 | State, region, US |

- EIA-861M gives revenue, MWh and customer counts by sector.
- nrc.gov blocks scripts; use the EIA mirror, which needs a free key.
- **Operator mapping.** I did not check which reactor units belong to CEG, VST or TLN.

**Timing.** Days to report: NEE 24, DUK 35, TLN 36, CEG 37, VST 38.
- The quarter's last EIA-861M month arrives **after** these reports.
- Weather and nuclear data give **about 23-37 days of lead**.

**Operating leverage: low.** Fuel pass-through gives a -0.07 fixed share and 0.13 flow-through. Generators hedge heavily.

**Analyst watch: high on weather** (judgment; utilities report weather-normalized results).

**Effort: medium.**

### 16. E&P: state production by operator

**Sources**

| State | Where | Free? | Level | Lag | Archive |
|---|---|---|---|---|---|
| North Dakota | https://www.dmr.nd.gov/oilgas/mprindex.asp (monthly Excel) | Yes | Well, with operator | About 7 weeks (July 2026 posted 2026-09-21) | Excel from May 2015, PDFs from 2003 |
| Texas | https://webapps.rrc.texas.gov/PDQ/home.do, plus the bulk dump listed at https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/ | Yes | Lease, with operator | Loaded through July 2026 as of Sep 23 | From 1993 |
| New Mexico | https://www.emnrd.nm.gov/ocd/wp-content/uploads/sites/6/FTPDataSetDescriptions.pdf; GO-TECH https://octane.nmt.edu/gotech/ | Yes | Well and operator | Unverified | Unverified |
| Colorado | https://ecmc.state.co.us/documents/data/downloads/production/monthly_prod.csv | Yes | Well, with operator | About 85% complete at 7.5 weeks | From 1999 |
| Pennsylvania | https://greenport.pa.gov/ReportExtracts/OG/OilGasWellProdReport | Yes | Well, with operator | 8 weeks or less | Unconventional wells monthly from 2015 |
| Oklahoma | Corporation Commission has no production files; the Tax Commission takes requests | Unverified | Unverified | Unverified | Unverified |

- North Dakota's figures are gross operated volumes, not the company's net share. Chord's wells appear under its legacy entity names.
- The Texas bulk dump is a CSV of more than 25GB, updated monthly. Wells awaiting a lease number are reported separately.
- New Mexico: free XML extracts refreshed monthly.

**Companies**

| Ticker | Market cap | Where it produces |
|---|---|---|
| CHRD | $7.6B | North Dakota and Montana |
| NOG | $2.5B | Non-operated; 30% Williston |
| RRC | $9.1B | Pennsylvania only |
| EQT | $32B | Appalachia |
| CNX | $4.9B | Appalachia |
| FANG | $52B | Permian |
| HPK* | $1.0B | Midland Basin, Texas |

Civitas no longer exists as a listed company; it merged into SM Energy on 2026-01-30.

**Timing.** Days to report are 21-42. **The quarter's last month arrives after the report**, so only 2 of 3 months are available. Several E&Ps also pre-release realized prices 9-16 days after quarter-end.

**Operating leverage: highest in the panel** (0.55 / 0.64). But revenue is driven by oil and gas prices, which everyone already sees.

**Analyst watch: medium-high.** Enverus packages this data for more than 300 financial institutions.

**Effort: high.**

### 17. Retail outside Texas

**Industry sources (all free)**

| Source | Where | Frequency | Lag | Archive | Level |
|---|---|---|---|---|---|
| Census monthly retail sales | https://www.census.gov/retail/sales.html | Monthly | About 16 days | From 1992 | Industry |
| Placer.ai Retail and Dining Index | placer.ai | Monthly | About 15 days | About 12 months in the free tool | Industry; a free single-location tool too |
| BofA Consumer Checkpoint | https://institute.bankofamerica.com/economic-insights/consumer-checkpoint-september-2026.html | Monthly | Unverified | Unverified | Category level |

Census delayed its January 2026 data to March 6.

**Companies that still report monthly sales**
- Costco (COST), about 3 days after month-end.
- Buckle (BKE), about 5 days.
- **Stopped:** Cato (April 2020) and PriceSmart (May 2021).
- Other monthly self-reporters outside retail: HOOD, IBKR, TW and CPA.

**Iowa liquor sales**
- https://data.iowa.gov/catalog/dataset/1263 (the old Socrata URL is dead).
- Free. Invoice-level rows by vendor, product and store. About 5 days behind. From 2012.
- Vendors include Diageo, Sazerac, Brown-Forman, Luxco (MGP Ingredients) and Constellation.
- Iowa is a small share of US spirits (judgment).

**Operating leverage: medium-low** (0.15 / 0.14).

**Analyst watch: high** for Costco.

### 18. Dry bulk and tankers

**Data**
- The Baltic Dry Index can be viewed free (for example on Trading Economics), but a free archive is unverified. The Baltic Exchange is subscription.
- No free tanker index archive was found.

**Companies pre-release their own numbers**
- DHT released its Q2 charter earnings 13 days after quarter-end, with Q3 bookings to date.
- Genco gives an estimate from fixtures already booked.

**Companies.** GNK* $1.15B, SB* $951M, DSX* $333M, SBLK $3.5B, STNG $3.7B, INSW $5.1B, DHT $3.4B, TNK $3.3B, FRO $10.5B.

**Verdict.** Little left to nowcast.

### 19. Credit-card issuers

**Data**
- Monthly credit 8-Ks around the 14th-15th: Synchrony, Capital One, Bread Financial, American Express.
- Monthly trust reports (10-Ds) filed on EDGAR.

**Timing gaps**
- Synchrony releases the quarter's last month with earnings.
- Capital One and Bread file nothing between mid-June and earnings.
- AmEx does file June data before its July report.

**Verdict.** These are **credit metrics that drive loss provisions, not revenue**. Low fit.

### 20. Homebuilders

**Census new home sales** (https://www.census.gov/construction/nrs/)
- Monthly, about 25 days behind.
- Each release revises the prior 3 months; the first estimate moves about 5% on average.
- National and regional only. FRED HSN1F from 1963.

**Builder-level data** is patchy: for example Austin's permit data names the contractor.

**Timing and companies.** Days to report run from LEN at 15 to BZH at 38. Small caps: LGIH* $1.17B, BZH* $860M, HOV* $699M, CCS* $1.78B, DFH* $1.08B.

**Operating leverage: medium-low** (0.08 / 0.19). Deliveries come largely from backlog the builders have already disclosed.

**Analyst watch: high.**

### 21. Cruise

**Data.** No free company-level monthly data was found.
- Port Everglades publishes annual figures: https://www.porteverglades.net/about-us/statistics/cruise-statistics/
- PortMiami: annual and milestone announcements only.
- Port Canaveral: occasional record announcements; its financials are annual.
- CLIA: annual.

**Timing.** Days to report: CCL 19-29, RCL 28-30, NCLH 30-34, VIK 44-62, LIND 34-57. Revenue is largely booked ahead and guided (judgment).

**Verdict.** Ranked last.

### Also considered, not ranked

- **Florida medical-marijuana weekly report** (https://knowthefactsmmj.com/about/weekly-updates/).
  - Company level (dispensaries and volume by licensee), 1-day lag, from 2016.
  - The most casino-like data found, but every company named trades OTC or in Canada. Revisit if they uplist.
- **Staffing.**
  - BLS temporary-help employment (FRED TEMPHELPS): August 2026 released 2026-09-04, a 4-day lag.
  - ASA Staffing Index: weekly; headline free; history for subscribers.
  - Industry level only. The staffing companies' market caps were not checked.
- **Coal.** MSHA mine-level production is quarterly, not monthly (https://arlweb.msha.gov/OpenGovernmentData/OGIMSHA.asp, from 2000). The filing deadline is unverified.
- **Steel.** AISI weekly raw-steel output: industry level, heavily watched.
- **Federal contracts** (USAspending, DoD announcements). These record awards, not revenue booked in the quarter. Low value.

---

## Top 3 next pilots after casinos

### 1. Restaurants and eatertainment: Texas mixed-beverage receipts

**Why**
- The only regulator dataset found that gives **location-level monthly sales for named US-listed companies**, like state gaming data.
- Free API. Back to 2007. Complete for chains about 20 days after month-end, which is 9-18 days before reports.
- About 10 listed companies, including small caps BJRI and PLAY. That is roughly 500 company-quarters.
- No evidence the sell-side uses it.
- The casino pipeline (ownership timeline, same-store growth, flow-through, announcement-return test) carries over almost unchanged.

**Main risk.** It is a Texas-only, alcohol-only sample. The Chili's check found the right direction but a third of the size.

**Gate before running returns.** Pre-register a minimum correlation between Texas same-store alcohol growth and each company's reported comparable sales. If it fails, stop.

### 2. Movie theaters: daily box office

**Why**
- Highest measured operating leverage of any group with a usable signal (0.42 fixed share).
- Daily data free back to 1985.
- The quarter is complete the day after quarter-end, 19-36 days before reports.
- About a day to build.

**Main risks**
- The data is heavily watched.
- Only 5 companies, 2 of them small caps.
- International revenue is not covered, and the COVID years must be dropped.

**What it adds.** It shows whether *watched* data still gets mispriced once the operating-leverage step is applied. That is the counterpoint to pilot 1's *unwatched* data.

### 3. Price-taker small caps: eggs plus ethanol (CALM, VITL, GPRE, REX, ALTO)

**Why**
- In both industries a free public price sets most of the quarter's revenue change while volume and costs are set.
- The price is complete at quarter-end, **25-52 days** before reports, the longest lead of the top candidates.
- Coverage is thin (2-6 analysts, except VITL).
- Four of the five are under $2B.
- One pilot, one method: price times volume gives revenue; minus input cost gives margin. Both use USDA MyMarketNews.

**Main risk: price history.**
- Free wholesale egg history is confirmed only from about December 2023. The fallback is the BLS retail egg price.
- The CARD ethanol-margin archive is unverified.

**Gate.** Assemble a free price history back to at least 2012, and check it against each company's own reported quarterly selling prices, before committing.

### Runners-up

- **Taiwan MOPS monthly revenue (TSM, UMC, ASX, IMOS).**
  - The cheapest test of the operating-leverage step on its own, because revenue is known exactly before earnings.
  - Worth doing in an hour as a check on the method.
- **Railroads.** Company-level weekly data and 0.37 flow-through, but the most closely watched of the candidates.
