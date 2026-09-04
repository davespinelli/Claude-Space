# Triage pack — IDR · Idaho Strategic Resources, Inc.

_Generated 2026-09-04 18:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** IDR · **Name:** Idaho Strategic Resources, Inc.
- **CIK:** 0001030192
- **SIC:** 1040 — Gold and Silver Ores
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/IDR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Idaho Strategic Resources, Inc.
- **CIK:** 1,030,192 · **SIC:** 1040 (Gold and Silver Ores) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 31.41 |
| mktcap | $497.1M |
| ev | $491.0M |
| ev_ebit | 31.5x |
| fcf | $12.4M |
| fcf_yield | 2.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 10.8% |
| net_debt | -$6.1M |
| net_debt_ebit | -0.4x |
| cash | $8.2M |
| ltd | $2.1M |
| equity | $120.5M |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $42.4M |
| revenue_prior | $25.8M |
| rev_growth | 64.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $15.6M |
| net_income | $16.7M |
| cfo | $19.1M |
| capex | $6.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 9.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 15,826,170 |
| shares_py | 14,505,392 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 17.3% |
| r6m | -18.3% |
| off_52w_high | -40.4% |
| adv20 | $7.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.34 |
| r_ev_ebit | 0.26 |
| r_roic | 0.72 |
| r_rev_growth | 0.96 |
| r_buyback | 0.13 |
| score | 0.53 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 214 |

**Screen rationale:** revenue +64.6%; net cash; 12-1 momentum 17.3%


## 3. Share count trend

- Shares outstanding: **15,826,170** (CY2026Q2I) vs **14,505,392** prior year (CY2025Q2I)
- Change: **9.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 5 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 176,793 sh / $6,180,207 -> net $-6,180,207 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 11; transaction rows: 23 (open-market buys 0, sales 8).

| code | rows |
|---|---|
| F | 3 |
| M | 12 |
| S | 8 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-14_7-01-reg-fd.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit; skipped 3 forward-looking-statement block(s)._

## EX-99.1 - PRESS RELEASE (idr_ex991.htm)

EX-99.1
idr_ex991.htm
PRESS RELEASE

idr_ex991.htm
EXHIBIT 99.1

Idaho Strategic Reports Second Quarter 2026 Operating and Financial Performance

Highlighted by a 13.25% Increase in Revenue to $10,732,335

COEUR D'ALENE, Idaho, August 13, 2026 (BUSINESS WIRE) – Idaho Strategic Resources, Inc . (NYSE American: IDR) ("IDR", "Idaho Strategic" or the "Company") today announced its consolidated operating and financial results for the second quarter ending June 30, 2026. Operating and financial results for the second quarter include:

Operational Performance: | Q2 2026 | % Change | Q2 2025
Ore Tonnes Processed | 11,094 | 8.34% | 10,240
Average Flotation Feed Grade (gpt) | 7.89 | -20.86% | 9.97
Ounces Produced | 3,047* | 1.23% | 3,010
All-In Sustaining Cost Per Ounce ($USD) | $2,261.81 | 16.08% | $1,948.53

Financial Performance ($USD): | Q2 2026 | % Change | Q2 2025
Revenue | $10,732,335 | 13.25% | $9,476,739
Total Cost of Sales | $4,700,607 | 17.49% | $4,000,953
Gross Profit | $6,031,728 | 10.15% | $5,475,786
Net Income Attributable to IDR | $3,651,596 | 31.95% | $2,767,458
Earnings Per Share (EPS) | $0.23 | 15.00% | $0.20
Average Realized Gold Price | $4,277.53 | 32.70% | $3,223.38

*includes in-process ore stockpile inventory

Idaho Strategic's President and CEO, John Swallow stated, "We had a modest record Q2 year over year comparison in revenue, net income, EPS and ounces produced (along with record meters of underground mine development), however the second quarter was one of those where the numbers also don't tell the full story. In addition to the expected increase in exploration field programs and the ramp up of construction activity at the Murray mill, there were unexpected events that tested our team. Overall, I am happy with the resiliency we showed and our ability to adjust on the fly to ultimately produce another positive quarter despite these challenges.

During the planned transition period from mining the H-vein to mining the Jumbo vein and development to the Paymaster, a section of the lower H-vein was encountered where the H-vein widens and flattens out as it approaches its intersection with the Idaho Fault. This transitional zone hosts slightly lower gold grades but higher tonnages resulting in about the same number of ounces as modeled but with a different orebody geometry than previous mining of the H-vein higher in elevation. This transitional zone required a slight change in mining methods to a drift and fill method with as many as four cuts side by side to efficiently recover the gold ore.

Idaho Strategic Resources, Inc. · 201 N. 3 rd Street · Coeur d'Alene, Idaho 83814

Also, during the quarter, a wildfire caused the New Jersey mill to shut down and evacuate from approximately June 16 th to June 24 th . Ultimately, all of Idaho Strategic personnel and equipment were unharmed but valuable processing time was lost at the end of the quarter that resulted in a strong last-minute push from our milling crews to do their best to make up for the lost time in the remaining days and nights prior to the end of the quarter on June 30 th .

Moving forward, we have a much better understanding of the lower H-vein stopes, we've advanced the development and mining timeline of the high-grade Jumbo vein, and our development to the Paymaster is modestly ahead of schedule. Considering the circumstances both within our control and outside of our control, I am pleased with our performance."

Golden Chest Highlights for Q2 2026 Include:

· | At the Golden Chest, ore mined from underground stopes totaled approximately 12,835 tonnes with all of the tonnage coming from H-Vein stopes.
· | During the quarter, a record 384 meters of development was completed between three projects: the Paymaster, the MAR and the Jumbo. A new portal, the No. 2, was established in early May to develop the high-grade Jumbo vein. From the No. 2 portal, an up-ramp was driven and connected to the No. 1 portal providing a secondary escapeway and allowing for production from the Jumbo vein to begin in the third quarter. Another quarterly record of 4,860 cubic meters of cemented rockfill backfill was placed during the quarter.
· | For the quarter ended June 30, 2026, a total of 11,094 dry metric tonnes were processed at the Company's New Jersey Mill with a flotation feed head grade of 7.89 gpt gold and gold recovery of 91.4%. Milling operations were affected by a wildfire adjacent to the mill in June where access to the mill was blocked for one week. Luckily there was no damage to the mill or the Company's equipment, though some of its timberland did burn.
· | The Company received the permit to construct a new tailings storage facility from the Idaho Department of Water Resources at the Golden Chest. Construction began in the quarter with the relocation of a low-grade stockpile and continued with building of the embankments and diversion structures.
· | Construction continued on the new mill at the Golden Chest with the installation of the fine ore bin, placement of the screen, foundations for the ball mill, and electrical work throughout the mill building. Engineering, design and procurement activities continued for the new mill also, and conveyor fabrication is also underway.
· | An exploration program consisting of surface and underground core drilling was continued during the second quarter at the Golden Chest. Approximately 10,000 meters of drilling were completed targeting the Paymaster and the H-vein.

Rare Earth Highlights for Q2 2026 Include:

· | Included in the inaugural list of companies that make up the Sprott Rare Earths Ex-China ETF (REXC).
· | Initiated metallurgical work at SGS Laboratory on representative samples from two of IDR's REE prospects.

Idaho Strategic Resources, Inc. · 201 N. 3 rd Street · Coeur d'Alene, Idaho 83814

John Swallow concluded, "I continue to believe that the combination of gold production backing significant exploration of rare earth elements, gold, and copper-silver is proving to be the right business plan at the right time. Despite the price action of gold during the quarter, global central banks continue to make it a focal point of their strategies moving forward and it is undoubtedly playing a larger role as a neutral reserve asset in the global monetary system. Additionally, the United States (along with end user participation) has continued to show support for redomiciling its rare earth elements supply chain amid the looming deadlines toward the end of this year that could see a reintroduction of China's dual-use export controls and new domestic sourcing requirements for rare earth elements vital to many national defense and advanced manufacturing industries. Finally, we are seeing a tightening of the copper market that is being reflected in the copper prices where we are anticipating a large increase in demand due to new power requirements led by datacenter buildout and AI, combined with many global producers running into operational challenges and a widespread decrease in the global copper grades.

I make these comments to point out that there are a number of tailwinds behind the company, and we are capitalizing on these opportunities while remaining focused on our shareholders and playing to our strengths. I am looking forward to the remaining summer months and the results of the investments we are making in our future."

Notes accompanying the financial statements below can be found in the Company's quarterly report filed this morning with the SEC on EDGAR.

Qualified person

IDR's Vice President, Grant A. Brackebusch, P.E. is a qualified person as such term is defined under S-K 1300 and has reviewed and approved the technical information and data included in this press release.

About Idaho Strategic Resources, Inc.

Idaho Strategic Resources (IDR) is an Idaho-based gold producer which also controls the largest rare earth elements land package in the United States. The Company's production-backed exploration business plan was established in anticipation of today's volatile geopolitical and macroeconomic environment. In addition to gold production, the Company has built a substantial land position in Idaho across multiple commodities, providing significant exploration exposure to gold and rare earth elements – in addition to thorium, copper, and silver. IDR finds itself in a unique position as one of the only publicly traded companies with growing gold production and significant blue-sky potential for discovery and development.

For more information on Idaho Strategic Resources, please visit www.idahostrategic.com or call:

Travis Swallow, Investor Relations & Corporate Development

Email: tswallow@idahostrategic.com

Phone: (208) 625-9001

Idaho Strategic Resources, Inc. · 201 N. 3 rd Street · Coeur d'Alene, Idaho 83814

Idaho Strategic Resources, Inc. Condensed Consolidated Statements of Operations (Unaudited) For the Three and Six-Month Periods Ended June 30, 2026 and 2025
June 30, 2026 | June 30, 2025
Three Months | Six Months | Three Months | Six Months
Revenue:
Sales of products, net | 10,732,335 | 25,214,621 | 9,476,739 | 16,755,275
Total revenue | 10,732,335 | 25,214,621 | 9,476,739 | 16,755,275
Costs of Sales:
Cost of sales and other direct production costs | 3,854,967 | 8,058,570 | 3,459,215 | 6,490,044
Depreciation and amortization | 845,640 | 1,559,425 | 541,738 | 1,091,359
Total costs of sales | 4,700,607 | 9,617,995 | 4,000,953 | 7,581,403
Gross profit | 6,031,728 | 15,596,626 | 5,475,786 | 9,173,872
Other operating expenses:
Exploration | 1,730,879 | 3,120,228 | 2,244,761 | 3,616,194
Management | 243,785 | 433,428 | 268,214 | 532,959
Professional services | 98,520 | 279,871 | 153,260 | 336,998
General and administrative | 295,640 | 518,667 | 223,735 | 460,753
(Gain) loss on sale of equipment | - | (632 | 68,942 | 308,840
Total other operating expenses | 2,368,824 | 4,351,562 | 2,958,912 | 5,255,744
Operating income | 3,662,904 | 11,245,064 | 2,516,874 | 3,918,128
Other (income) expense:
Equity (income) loss on investment in Buckskin Gold and Silver, Inc | (1,245 | (1,077 | 159 | (1,187
Loss on investment in equity securities and mutual funds | - | 304,241 | - | -
Timber revenue net of costs | - | (3,209 | (2,848 | (6,704
Dividend income | (13,233 | (68,765 | - | -
Interest income | (677,372 | (1,069,390 | (220,409 | (405,804
Total other income | (691,850 | (838,200 | (223,098 | (413,695
Income before income taxes | 4,354,754 | 12,083,264 | 2,739,972 | 4,331,823
Income tax provision | 726,914 | 2,086,234 | - | -
Net income | 3,627,840 | 9,997,030 | 2,739,972 | 4,331,823
Net loss attributable to non-controlling interest | (23,756 | (42,558 | (27,486 | (44,614
Net income attributable to Idaho Strategic Resources, Inc | 3,651,596 | 10,039,588 | 2,767,458 | 4,376,437
Net income per common share-basic | 0.23 | 0.64 | 0.20 | 0.32
Weighted average common share outstanding-basic | 15,813,075 | 15,804,123 | 14,007,582 | 13,837,894
Net income per common share-diluted | 0.23 | 0.63 | 0.20 | 0.31
Weighted average common shares outstanding-diluted | 15,983,254 | 15,979,299 | 14,134,531 | 13,939,790

Idaho Strategic Resources, Inc. · 201 N. 3 rd Street · Coeur d'Alene, Idaho 83814

Idaho Strategic Resources, Inc.

Condensed Consolidated Balance Sheets (Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-23_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

Idaho Strategic's financial performance for the years ended December 31, 2025, and 2024 is summarized below:

· | Revenue from concentrate sales increased 64.6% to $42,406,253 for the year ending December 31, 2025, compared to $25,765,373 for the comparable period in 2024. The increase was due to 665 more ounces of gold sold during the year, as well as higher realized gold prices recognized on concentrate sales. Realized gold price for 2025 was $3,583.43 vs $2,306.86 in 2024. Ore from the H-vein is anticipated to be the primary source of ore for 2026 as it was in 2025.
· | Gross profit for the year ended December 31, 2025 was $26,205,927 compared to a gross profit of $12,950,493 in 2024. This resulted in an increase in gross profit as a percentage of sales from 50.3% in 2024 to 61.8% in 2025. This increase is attributable to the higher head grade from H-Vein ore processed at the Company's New Jersey Mill, as well as higher gold prices recognized on concentrate sales.
· | Net income for the year ended December 31, 2025 was $16,631,198 compared to net income for the year ended December 31, 2024 of $8,753,377. The increase was primarily due to higher gold prices.
· | The consolidated net income included non-cash charges of $4,556,936 ($1,973,746 in 2024) as follows: depreciation and amortization of $2,338,100 ($1,953,388 in 2024), accretion of asset retirement obligation of $20,042 ($18,761 in 2024), loss on disposal of equipment of $343,945 ($1,431 in 2024), equity income on investment in Buckskin Gold and Silver, Inc. $3,646 ($2,667 in 2024), write down of reclamation bond $0 ($300 in 2024) stock-based compensation of $1,505,244 ($0 in 2024), unrealized gain on equity securities and mutual funds of $110,092 ($0 in 2024), amortization of discount on US treasury notes of $37,197 ($2,080 in 2024), and accrued income tax liability of $426,146 ($0 in 2024).
· | Cash cost per ounce increased $116.80 compared to 2024 due to slightly higher input costs.
· | All-in sustaining cost per ounce increased $417.74 compared to 2024 due to increased exploration at the Golden Chest which also increased sustaining capital. Adjusted all-in sustaining cost per ounce without exploration was $1,494.75 and $1,256.16 for 2025 and 2024, respectively.
· | Gold sales receivable increased to $3,912,922 from $1,578,694 at December 31, 2025 compared to 2024.
· | The Company saw an increase in exploration expenses of $4,716,900 for 2025 due to the expanded drilling program at the Golden Chest mine for development and exploration purposes.

Cash Costs and All-In Sustaining Costs Reconciliation to Generally Accepted Accounting Principles ("GAAP")

Reconciliation of cost of sales and other direct production costs and depreciation, depletion, and amortization (GAAP) to cash cost per ounce and All-In Sustaining Costs ("AISC") per ounce (non-GAAP).

The table below presents reconciliations between the most comparable GAAP measure of cost of sales and other direct production costs and depreciation, depletion, and amortization to the non-GAAP measures of cash cost per ounce produced and AISC per ounce produced for the Company's gold production for the years ended December 31, 2025, and 2024. The cost per ounce calculations are based on ounces produced. Upon sale, the Company typically receives payment at an average rate of 94% of ounces produced after smelting and refining charges are deducted.

Cash cost per ounce is an important operating measure that we utilize to measure operating performance. AISC per ounce is an important measure that we utilize to assess net cash flow after costs for pre-development, exploration, reclamation, and sustaining capital. Current GAAP measures used in the mining industry, such as cost of goods sold do not capture all the expenditures incurred to discover, develop, and sustain gold production. During 2024, the Company adjusted the method of calculating sustaining capital to better reflect actual costs required to sustain mining operations. Prior periods have been restated in the table below to reflect this change. Idaho Strategic calculates sustaining capital by including depreciation and amortization as an estimate of property, plant, and equipment wear and tear necessary to maintain production capacity, plus Golden Chest capitalized development costs, net of current period amortization, to reflect expenses for sustaining mine access and gold production.

December 31,
2025 | 2024
Cost of sales and other direct production costs and depreciation, depletion, and amortization | 16,200,326 | 12,814,880
Less depreciation, depletion, amortization and stock-based compensation | (3,265,706 | (1,953,388
Change in inventory | (65,188 | (23,243
Cash Cost | 12,869,432 | 10,838,249
Exploration | 7,637,435 | 2,920,535
Less non-gold exploration and stock-based compensation | (2,659,417 | (324,333
Sustaining capital | 5,974,247 | 3,385,893
General and administrative | 1,092,822 | 763,040
Less stock-based compensation and other non-cash items | (769,124 | (20,058
AISC | 23,719,249 | 17,563,326
Divided by ounces produced | 12,538 | 11,915
Cash cost per ounce | 1,026.43 | 909.63
AISC per ounce | 1,891.79 | 1,474.05

Financial Condition and Liquidity

For the Years Ended December 31,
Net cash provided (used) by: | 2025 | 2024
Operating activities | 19,101,691 | 10,840,886
Investing activities | (61,458,139 | (20,762,889
Financing activities | 51,139,312 | 8,741,905
Net change in cash and cash equivalents | 8,782,864 | (1,180,098
Cash and cash equivalents, beginning of period | 1,106,901 | 2,286,999
Cash and cash equivalents, end of period | 9,889,765 | 1,106,901

The Company has retained earnings of approximately $8.3 million at December 31, 2025 and earned a consolidated net profit in 2025 of $16,631,198. The Company's working capital at December 31, 2025 is $47,669,136. The Company is currently producing from underground at the Golden Chest. During 2025, production generated positive cash flow from operations of $19,101,691 compared to a positive cash flow from operations of $10,840,886 in 2024. Planned production for the next 18 months indicates a positive cash flow from operations will continue as underground mining of the H-Vein and Jumbo vein remains the primary source of ore feed for the mill. In prior years, the Company has been successful in raising required funds for ongoing operations from sale of its common stock or borrowing. Management believes it can meet its contractual obligations with continuing cash flows from operations, existing cash, and potential financings for the next 18 months.

## 9. 10-K Item 1 - Business (10-K_2026-03-23_item1_business.md)

ITEM 1. DESCRIPTION OF THE BUSINESS

History and Organization

Idaho Strategic Resources, Inc. ("the Company", "Idaho Strategic" or "IDR") was incorporated under the laws of the State of Idaho on July 18, 1996. The Company's head office and registered records office is located at 201 N. 3 rd St. Coeur d'Alene, ID 83814. On December 6, 2021, the Company changed its name to Idaho Strategic Resources, Inc. (formerly New Jersey Mining Company ("NJMC")) to better reflect its corporate focus, Idaho-based operations and being domiciled in Idaho. IDR is one of the few resource-based companies (public or private) possessing the combination of officially recognized U.S. domestic rare earth element properties (in Idaho) and Idaho-based gold production located in an established mining community.

Any Bankruptcy, Receivership or Similar Proceedings

There have been no bankruptcy, receivership, or similar proceedings.

Any Material Reclassification, Merger, Consolidation, or Purchase or Sale of a Significant Amount of Assets Not in the Ordinary Course of Business.

There have been no material reclassifications, mergers, consolidations, purchases, or sales not in the ordinary course of business for the past three years.

General Description of the Business

Idaho Strategic produces gold at the Golden Chest Mine located in the Murray Gold Belt ("MGB"), the northern portion of the world-class Coeur d'Alene Mining District, north of the prolific Silver Valley. With over 20,000 acres of patented and unpatented land, the Company has the largest private land and mineral claim position in the area following its consolidation of the Murray Gold Belt for the first time in over 100-years.

The Company is an established gold producer, with prior surface and current underground mining operations at its 100-percent owned Golden Chest Mine and conducts milling operations at its majority-owned New Jersey Mill. In addition to gold and gold production, the Company maintains an important strategic presence in the U.S. Critical Minerals sector, specifically focused on the more "at-risk" rare earth elements ("REE"). The Company's Mineral Hill, Lemhi Pass, and Diamond Creek properties are included the U.S. national REE inventory as listed in United States Geologic Survey ("USGS"), Idaho Geologic Survey ("IGS") and Department of Energy ("DOE") publications. All three projects are in central Idaho near the Company's field office in Salmon, Idaho.

The Company focuses its exploration and production efforts in historical mining districts mostly located within the state of Idaho. Its portfolio of mineral properties includes:

· | The Golden Chest Mine, a producing gold mine located in the Murray Gold Belt of North Idaho;
· | Niagara, an intermediate-stage copper-silver exploration property located in the Murray Gold Belt of North Idaho;
· | Little Baldy, an intermediate-stage gold exploration property located in the Murray Gold Belt of North Idaho;
· | Approximately 1,510 acres of additional patented mineral property and over 14,880 acres of nearby and adjacent unpatented mineral property. These holdings are considered early-stage exploration properties and located within the Murray Gold Belt, many of which include historic gold mines and known gold mineralization;
· | REE Projects–located in the Idaho Rare Earth Element-Thorium ("REE-Th") Belt near Salmon, Idaho. Projects include;

○ | Mineral Hill – Nationally recognized and high grade REE property in the northern portion of the Idaho REE-Th Belt
○ | Lemhi Pass – Significant land package with high value REE potential–USGS also recognized as the #1 thorium prospect in the U.S.
○ | Diamond Creek – Nationally recognized rare earth prospects in the US

· | A significant portfolio of early-stage exploration properties throughout Idaho.

In addition to its portfolio of exploration, pre-development, and producing properties, the Company is also the manager and majority-owner of the New Jersey Mill, which currently processes ore from the Golden Chest Mine. The New Jersey Mill can process gold and silver ore through a 360-tonne per day flotation plant.

The Company has focused its efforts on underground development and growing production at the Golden Chest Mine and exploration at its extensive land holdings within the MGB area. With all debt associated with land acquisition and the start-up of operations behind it, the Company significantly increased its exploration and growth initiatives in the Murray Gold Belt. This progress, combined with the existing infrastructure and development, has created a solid foundation of value regardless of market cycles.

Competitive Business Conditions

While there has been a market for gold and precious metals historically, the Company competes on several different fronts within the minerals exploration industry. The Company may find the need to compete with other junior mining companies for the capital necessary to sustain its exploration and development programs. IDR has focused its gold operations at and near the Golden Chest Mine, however if it chose to expand to other geographic areas it may compete with other mining companies for exploration properties and mining assets. The Company has been successful in resuming operations at the New Jersey Mill, consolidating 100% ownership of the Golden Chest Mine, and assembling one of the largest rare earth element landholdings in the US. In October 2016 production at the Golden Chest resumed with the Company as the sole owner and operator.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-23_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-23_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-23_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-14_7-01-reg-fd.md, 10-K_2026-03-23_item7_mdna.md, 10-K_2026-03-23_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
