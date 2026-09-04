# Triage pack — CLB · Core Laboratories Inc. /DE/

_Generated 2026-09-04 15:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CLB · **Name:** Core Laboratories Inc. /DE/
- **CIK:** 0001958086
- **SIC:** 1389 — Oil & Gas Field Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CLB

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Core Laboratories Inc. /DE/
- **CIK:** 1,958,086 · **SIC:** 1389 (Oil & Gas Field Services, NEC) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 12.53 |
| mktcap | $574.9M |
| ev | $666.1M |
| ev_ebit | 11.8x |
| fcf | $25.8M |
| fcf_yield | 4.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 12.3% |
| net_debt | $91.1M |
| net_debt_ebit | 1.6x |
| cash | $22.7M |
| ltd | $113.9M |
| equity | $272.7M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $526.5M |
| revenue_prior | $523.8M |
| rev_growth | 0.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $56.5M |
| net_income | $29.7M |
| cfo | $37.0M |
| capex | $11.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 45,884,542 |
| shares_py | 46,893,842 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -6.9% |
| r6m | -22.1% |
| off_52w_high | -36.2% |
| adv20 | $6.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.46 |
| r_ev_ebit | 0.69 |
| r_roic | 0.76 |
| r_rev_growth | 0.36 |
| r_buyback | 0.80 |
| score | 0.61 |

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
| rank | 132 |

**Screen rationale:** high ROIC 12.3%; buying back stock -2.2%


## 3. Share count trend

- Shares outstanding: **45,884,542** (CY2026Q2I) vs **46,893,842** prior year (CY2025Q2I)
- Change: **-2.2%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-25** — Item 5.02 (officer / director change or comp arrangement): On August 19, 2026, Kwaku Temeng verbally notified the Board of Directors of Core Laboratories Inc. (the "Company") of his intention to resign as a director of the Company effective October 1, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 5,000 sh / $53,900 vs sells 0 sh / $0 -> net $53,900 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: Bruno Lawrence bought 5,000 sh @ $10.78 ($53,900) on 2026-07-31.

Form 4 filings parsed: 12; transaction rows: 33 (open-market buys 1, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 4 |
| M | 20 |
| P | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'CORE LAB REPORTS SECOND QUARTER 2026 RESULTS:'; skipped 9 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (clb-ex99_1.htm)

CORE LAB REPORTS SECOND QUARTER 2026 RESULTS:

•
REVENUE OF $124.6 MILLION, UP 2% SEQUENTIALLY AND DOWN 4% YEAR-OVER-YEAR

•
OPERATING INCOME OF $9.2 MILLION; EX-ITEMS, $9.4 MILLION, UP 42% SEQUENTIALLY AND DOWN 36% YEAR-OVER-YEAR

•
GAAP EARNINGS PER SHARE OF $0.13; EPS EX-ITEMS OF $0.11, UP 85% SEQUENTIALLY AND DOWN 42% YEAR-OVER-YEAR

•
FREE CASH FLOW OF $3.1 MILLION

•
COMPANY REPURCHASED 214,712 SHARES OF COMMON STOCK, FOR $2.7 MILLION AGGREGATE PURCHASE PRICE

•
COMPANY ANNOUNCES Q3 2026 QUARTERLY DIVIDEND

HOUSTON (July 29, 2026)—Core Laboratories Inc. (NYSE: "CLB") ("Core," "Core Lab," or the "Company") reported second quarter 2026 revenue of $124,600,000. Core's operating income was $9,200,000, with earnings per diluted share ("EPS") of $0.13, all in accordance with U.S. generally accepted accounting principles ("GAAP"). Operating income, ex-items, a non-GAAP financial measure, was $9,400,000, yielding operating margins of 8%, and EPS, ex-items, of $0.11. A full reconciliation of non-GAAP financial measures is included in the attached financial tables.

Core's CEO, Larry Bruno, stated, "Our second quarter results displayed sequential improvement in revenue, operating income and earnings per share despite continued geopolitical conflicts that affected portions of our business, particularly Reservoir Description. Notably, we saw improvement in activity in Africa, U.S., and Asia-Pacific regions, where operators continued to call on Core Lab's specialized technical expertise to facilitate critical reservoir characterization and production optimization projects. In addition, higher sequential product sales and completion diagnostic service activity were achieved across many regions including the U.S., while international growth of Production Enhancement's products and services reflected the expanded adoption of our innovative technologies.

"As mentioned, client operations were disrupted in the Middle East, and laboratory testing in support of the maritime transportation and trade of crude oil and derived products was largely suspended in the region. Increased military action and evolving sanctions related to the Russia-Ukraine conflict also presented headwinds during the second quarter. Looking forward, we see several international regions poised for continued growth, coupled with modestly improving U.S. onshore activity which we believe sets the stage for sequential improvement in the third quarter."

Reservoir Description

Reservoir Description operations are closely correlated with trends in international and offshore activity levels, with approximately 80% of revenue sourced from projects originating outside the United States. Revenue for Reservoir Description in the second quarter of 2026 was $78,700,000, down 4% sequentially and 9% year-over-year. During the quarter, military conflicts in both the Middle East and Russia-Ukraine resulted in increased attacks on energy infrastructure, which suspended client projects and disrupted global transportation and trade of crude oil and derived products. These events negatively impacted demand for services in both the directly affected regions and across the Company's international crude oil assay laboratory network. Operating income on both a GAAP basis and ex-items was $3,700,000 yielding operating margins of 5%. Margins were impacted by: 1) reduced client activity in the Middle East, 2) lower global crude assay activity resulting from disruptions to hydrocarbon cargo shipments through the Strait of Hormuz, and 3) increased military action and expanded European sanctions associated with the Russia-Ukraine conflict. Core Lab has maintained its operational capabilities and cost structure in the Middle East, reflecting its expectation that hydrocarbon trading routes and client activity will normalize over time. The Company has taken steps to improve profitability in Russia-Ukraine operations.

During the second quarter of 2026, Core Lab was engaged to support multiple exploration, appraisal, and carbon storage projects across Asia-Pacific and Africa. The Company was engaged to perform a reservoir rock evaluation study for an onshore gas development in Australia. Leveraging the Company's Advanced Technology Center in Australia, Core Lab is using its Advanced Digital Imaging System ("ADIS") to generate high-resolution core images that combine with physical laboratory measurements to evaluate geologic attributes, reservoir quality, and flow properties. The resulting datasets will be incorporated into Core Lab's proprietary RAPID™ database, providing the operator with secure data access and accelerated interpretation of results.

In Africa, Core Lab was selected by a major international operator to provide a data analytical program on a conventional core from an exploration well offshore Namibia. Utilizing its Advanced Technology Center in Scotland, the Company is performing a comprehensive laboratory analytical program. A wide variety of Core Lab's proprietary laboratory technologies are being used to characterize the geological and petrophysical properties of the strata. These physical measurements will provide the hard data points that form the foundation of the detailed reservoir model. Conventional core analysis programs like this provide robust datasets that allow operators to reduce risk on the large capital investments required for offshore international exploration and appraisal programs.

Also in Africa, during the second quarter of 2026, Core Lab initiated a reservoir characterization program in support of Murphy Oil Corporation's recently announced discovery offshore Côte d'Ivoire. Following recovery operations at the wellsite, core samples were transported to Core Lab's Houston facility for accelerated analysis using the Company's proprietary Dual Energy CT technology. Core Lab is very pleased to be assisting Murphy Oil in its Côte d'Ivoire project.

Collectively, these second quarter engagements highlight Core Lab's ability to leverage its global laboratory network, specialized technical expertise, and proprietary technologies to deliver advanced reservoir evaluation solutions for complex exploration, appraisal, and development projects.

Production Enhancement

Production Enhancement operations, which are focused on complex completions in unconventional oil and gas reservoirs in the U.S., as well as conventional and unconventional projects across the globe, posted second quarter 2026 revenue of $45,900,000, up 15% sequentially and 5% year-over-year. Operating income for the second quarter on a GAAP basis was $5,200,000. Operating income, ex-items was $5,300,000, yielding operating margins of 12% and sequential incremental margins of 59%. While the conflict in the Middle East delayed completion diagnostic projects in the region, U.S. completion activity improved modestly during the second quarter of 2026, though most operators maintained drilling and completion activities in line with their original plans. Product sales increased nicely in both the U.S. and international markets compared to the first quarter of 2026. Diagnostic service revenue also increased in the U.S. and international markets that were targeted for strategic growth. Second quarter operating margins included a modest benefit associated with the recovery of certain tariffs incurred in prior periods.

During the second quarter of 2026, a national oil company ("NOC") in Asia-Pacific engaged Core Lab to support the development of its in-house Tubing Conveyed Perforating ("TCP") capability. Core Lab supplied a complete TCP equipment package, along with technical training, which enabled the operator to quickly, successfully, and safely execute its first in-house TCP operation. By combining Core Lab's proven TCP technology and expertise, the NOC was able to establish protocols for cost-effective, in-sourced project execution. The operator plans to apply Core Lab's TCP technologies as they expand their perforating program.

Also during the second quarter, Core Lab received regulatory approval to deploy its proprietary SpectraStim™ proppant tracing and SpectraScan® spectral gamma ray logging technologies in the United Arab Emirates ("UAE"). These approvals significantly expand the Company's reservoir optimization capabilities in one of the Middle East's most strategically important oil and gas markets. Core Lab's unique technologies have the Company well-positioned to serve operators seeking advanced completion diagnostics to analyze frac performance and maximize hydrocarbon recovery. Together with the Company's expanded laboratory presence in the region, these approvals create new opportunities to support field development programs throughout the UAE.

Liquidity, Free Cash Flow, Share Repurchases, and Dividend

Core continues to focus on maximizing free cash flow ("FCF"), a non-GAAP financial measure defined as cash from operations less capital expenditures. For the second quarter of 2026, cash from operations was $7,800,000, up from $4,000,000 in the first quarter of 2026, and capital expenditures associated with operations were $4,700,000, yielding FCF of $3,100,000. Capital expenditures in the second quarter of 2026 were higher than previous quarters, and include: 1) investments to support a multi-year contract in the Asia-Pacific region, and 2) rebuilding the facilities in the Mediterranean that incurred weather-related damage in the first quarter of 2026.

As mentioned in the Company's prior earnings releases, in February 2024, fire damaged a building on the campus of Core Lab's Advanced Technology Center in Scotland. Losses caused by the fire are covered by Core Lab's property and casualty insurance. Insurance proceeds and the capital expenditures associated with replacing the equipment and restoring the building are disclosed separately in the investing

section of the cash flow statement. Capital expenditures associated with these items were $1,100,000 for the second quarter of 2026 and are not included in the calculation of FCF.

In the second quarter of 2026, Core Lab repurchased 214,712 shares at an aggregate purchase price of approximately $2,700,000.

As of June 30, 2026, Core's net debt (defined as long-term debt less cash and cash equivalents) was $93,600,000, decreasing by $500,000 during the quarter. Also, during the second quarter of 2026, the Company's leverage ratio (calculated as total net debt divided by trailing twelve months adjusted EBITDA) was at 1.30. The Company remains focused on executing its strategic business initiatives and continues to evaluate allocation of capital to reduce debt and other uses of free cash to return value to shareholders.

On April 29, 2026, Core's Board of Directors ("Board") announced a quarterly cash dividend of $0.01 per share of common stock, which was paid on June 1, 2026, to shareholders of record on May 11, 2026.

On July 29, 2026, the Board approved a cash dividend of $0.01 per share of common stock, payable on August 31, 2026, to shareholders of record on August 10, 2026.

Return On Invested Capital

The Board and the Company's Executive Management continue to focus on strategies that maximize return on invested capital ("ROIC") and FCF, factors that have high correlation to total shareholder return. Core's commitment to an asset-light business model and disciplined capital stewardship promotes capital efficiency and are designed to produce more predictable and superior long-term ROIC.

The Board has established an internal metric to demonstrate ROIC performance relative to the oilfield services companies listed as Core's Comp Group by Bloomberg, as the Company continues to believe superior ROIC will result in higher total shareholder return. Using Bloomberg's formula, Core Lab's ROIC for the second quarter of 2026 was 8.3%.

Industry and Core Lab Outlook and Guidance

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-23_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

Operating Results for the Year Ended December 31, 2025 Compared to the Years Ended December 31, 2024 and 2023

We evaluate our operating results by analyzing revenue, operating income and operating income margin (defined as operating income divided by total revenue). Since we have a relatively fixed cost structure, decreases in revenue generally translate into lower operating income results. Results for the years ended December 31, 2025, 2024 and 2023 are summarized in the following chart.

Results of operations as a percentage of applicable revenue for the years ended December 31, 2025, 2024 and 2023 are as follows (in thousands, except for per share information):

2025 / 2024 | 2024 / 2023
2025 | 2024 | 2023 | % Change
REVENUE:
Services | 399,422 | 75.9 | % | 388,205 | 74.1 | % | 371,914 | 73.0 | % | 2.9 | % | 4.4 | %
Product sales | 127,098 | 24.1 | % | 135,643 | 25.9 | % | 137,876 | 27.0 | % | (6.3 | )% | (1.6 | )%
Total revenue | 526,520 | 100.0 | % | 523,848 | 100.0 | % | 509,790 | 100.0 | % | 0.5 | % | 2.8 | %
OPERATING EXPENSES:
Cost of services* (1) | 302,206 | 75.7 | % | 297,324 | 76.6 | % | 282,135 | 75.9 | % | 1.6 | % | 5.4 | %
Cost of product sales* (1) | 115,381 | 90.8 | % | 123,198 | 90.8 | % | 117,822 | 85.5 | % | (6.3 | )% | 4.6 | %
Total cost of services and product sales | 417,587 | 79.3 | % | 420,522 | 80.3 | % | 399,957 | 78.5 | % | (0.7 | )% | 5.1 | %
General and administrative expense (1) | 45,430 | 8.6 | % | 39,770 | 7.6 | % | 40,259 | 7.9 | % | 14.2 | % | (1.2 | )%
Depreciation and amortization | 14,649 | 2.8 | % | 14,953 | 2.9 | % | 15,784 | 3.1 | % | (2.0 | )% | (5.3 | )%
Other (income) expense, net | (7,614 | (1.4 | )% | (9,953 | (1.9 | )% | (850 | (0.2 | )% | NM | NM
OPERATING INCOME | 56,468 | 10.7 | % | 58,556 | 11.2 | % | 54,640 | 10.7 | % | (3.6 | )% | 7.2 | %
Interest expense | 10,572 | 2.0 | % | 12,369 | 2.4 | % | 13,430 | 2.6 | % | (14.5 | )% | (7.9 | )%
Income before income taxes | 45,896 | 8.7 | % | 46,187 | 8.8 | % | 41,210 | 8.1 | % | (0.6 | )% | 12.1 | %
Income tax expense | 15,505 | 2.9 | % | 14,034 | 2.7 | % | 4,185 | 0.8 | % | 10.5 | % | 235.3 | %
Net income | 30,391 | 5.8 | % | 32,153 | 6.1 | % | 37,025 | 7.3 | % | (5.5 | )% | (13.2 | )%
Net income attributable to non-controlling interest | 722 | 0.1 | % | 753 | 0.1 | % | 350 | 0.1 | % | NM | NM
Net income attributable to Core Laboratories Inc. | 29,669 | 5.6 | % | 31,400 | 6.0 | % | 36,675 | 7.2 | % | (5.5 | )% | (14.4 | )%
Diluted earnings per share | 0.65 | 0.67 | 0.78 | (3.0 | )% | (14.1 | )%
Diluted earnings per share attributable to Core Laboratories Inc. | 0.63 | 0.66 | 0.77 | (4.5 | )% | (14.3 | )%
Diluted weighted average common shares outstanding | 47,028 | 47,685 | 47,523
Other Data:
Current ratio (2) | 2.02:1 | 2.16:1 | 2.53:1
Debt to EBITDA ratio (3) | 1.20:1 | 1.37:1 | 2.11:1
Debt to Adjusted EBITDA ratio (4) | 1.10:1 | 1.31:1 | 1.76:1
* Percentage based on applicable revenue rather than total revenue.
"NM" means not meaningful.
(1) Excludes depreciation.
(2) Current ratio is calculated as follows: current assets divided by current liabilities. The current ratio at December 31, 2024 has been revised from 2.32:1 to 2.16:1 as a result of certain prior period immaterial corrections. See Note 2 – Summary of Significant Accounting Policies of the Notes to the Consolidated Financial Statements.
(3) Debt to EBITDA ratio is calculated as follows: debt less cash divided by the sum of consolidated net income plus interest, taxes, depreciation and amortization and certain non-cash adjustments.
(4) Debt to Adjusted EBITDA ratio (as defined in our Credit Facility) is calculated as follows: debt less cash divided by the sum of consolidated net income plus interest, taxes, depreciation, amortization, impairments, severance and certain non-cash adjustments.

Service Revenue

Service revenue is primarily tied to activities associated with the exploration, production, movement and refinement of oil, gas and derived products outside the U.S. Service revenue for the year ended December 31, 2025, was $399.4 million, an increase of 3% compared to 2024. Approximately 70% of service revenue is generated from international markets. The increase in service revenue was due to growth in both U.S. and international markets. In 2025, growth occurred in several international markets, primarily in Europe and Africa, despite the headwinds from the on-going geopolitical conflicts and expanded sanctions previously discussed. The increase in U.S. service revenue in 2025 compared to 2024, was attributable to increased demand for well completion diagnostic services and growing client activity for our laboratory crude assay services in 2025. Growth in service revenue in 2025 has been negatively impacted by certain projects that were planned and scheduled but were canceled, as the well drilled by our clients were determined to be uneconomical or unsuccessful. Service revenue for the year ended December 31, 2024, was $388.2 million, an increase of 4% compared to 2023. The increase was due to growth in activity levels in both U.S. and international markets. In 2024, growth occurred in several international markets, primarily in

Europe, Africa and Asia Pacific, despite the headwinds from the on-going geopolitical conflicts. The increase in U.S. service revenue in 2024 compared to 2023, benefited from increased demand for reservoir core and reservoir fluids analysis services on international projects that are often conducted in our advanced technology center located in Houston, Texas, as well as a growing demand for CCS projects. Well completion diagnostic services in the U.S. market also showed strong growth in 2024 compared to 2023.

Product Sales Revenue

Product sales revenue is equally tied to the completion of onshore wells in North America and international activities. Product sales to the U.S. onshore markets are generally delivered more frequently and in smaller quantities, versus product sales to international markets which are typically shipped and delivered in bulk and the timing of delivery can vary from one period to another. Product sales revenue for the year ended December 31, 2025, was $127.1 million, a decrease of 6% compared to 2024. The decline in our product sales revenue was in line with the 6% decline in U.S. land-based average rig count in 2025 compared to 2024. Product sales revenue for the year ended December 31, 2024, was $135.6 million, a decrease of 2% compared to 2023. The decline in our product sales revenue was primarily associated with the activity decline in the U.S. onshore market, where the U.S. land-based average rig count decreased 13% in 2024 compared to 2023. The decrease in product sales to the U.S. market was partially offset by a higher level of product sales to international markets in 2024.

Cost of Services, excluding depreciation

Cost of services for the year ended December 31, 2025 was $302.2 million, an increase of 2% compared to 2024, which is lower than the change in service revenue. Cost of services expressed as a percentage of service revenue decreased to 76% in 2025 compared to 77% in 2024. The improvement in cost of services as a percentage of service revenue in 2025 compared to 2024, was primarily due to increased efficiencies and the benefits of lower compensation costs as a result of cost reduction initiatives implemented during 2025. Cost of services for the year ended December 31, 2024 was $297.3 million, an increase of 5% compared to 2023, which is slightly higher than the change in service revenue. Cost of services expressed as a percentage of service revenue increased to 77% in 2024 compared to 76% in 2023. The slight increase in cost of services as a percentage of service revenue in 2024, was primarily associated with higher employee compensation and higher operating costs incurred due to the fire incident at our Aberdeen, U.K. facility. The fire related costs and loss of income from business interruption were substantially covered by insurance proceeds recorded in Other (income) expense, net.

Cost of Product Sales, excluding depreciation

Cost of product sales for the year ended December 31, 2025 was $115.4 million, a decrease of 6% compared to 2024, which was in line with the changes in product sales revenue. Cost of product sales as a percentage of sales revenue remained flat between 2025 and 2024. In 2025, cost of product sales as a percentage of product sales was affected by higher absorption of fixed costs on a lower revenue base; but was offset by improved manufacturing efficiency and cost reduction initiatives implemented and lower inventory and asset write-downs of $1.8 million in 2025 compared to $3.3 million in 2024. Cost of product sales for the year ended December 31, 2024 was $123.2 million, an increase of 5% compared to 2023. Cost of product sales expressed as a percentage of product sales revenue increased to 91% in 2024 from 86% in 2023 primarily due to certain inventory and asset write-downs in 2024 as discussed above, with no such write-downs in 2023.

General and Administrative Expense, excluding depreciation

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-23_item1_business.md)

ITEM 1. BUSINESS

General

Core Laboratories Inc. is a Delaware corporation. We were established in 1936 and are one of the world's leading providers of proprietary and patented reservoir description and production enhancement services and products to the oil and gas industry, primarily through client relationships with many of the world's major, national and independent oil companies. These services and products can enable our clients to evaluate and improve reservoir performance and increase oil and gas recovery from their new and existing fields. We make measurements on reservoir rocks, reservoir fluids (crude oil, natural gas and water) and their derived products. In addition, we assist clients in evaluating subsurface targets associated with Carbon Capture and Sequestration ("CCS") projects or initiatives. We have over 70 offices in more than 50 countries and have approximately 3,300 employees.

On May 1, 2023, Core Laboratories N.V. completed its previously announced redomestication transaction (the "Redomestication Transaction"), which through a series of steps, resulted in the merger of Core Laboratories N.V., a holding company in the Netherlands, with and into Core Laboratories Luxembourg S.A., a public limited liability company incorporated under the laws of Luxembourg, with Core Laboratories Luxembourg S.A. surviving, and subsequently the migration of Core Laboratories Luxembourg S.A. out of Luxembourg and its domestication as Core Laboratories Inc., a Delaware corporation. See Note 1 - Description of Business of the Notes to the Consolidated Financial Statements.

References to "Core Laboratories", "Core Lab", "the Company", "we", "our", "us" and similar phrases are used throughout this Annual Report on Form 10-K (this "Form 10-K") and relate collectively to Core Laboratories Inc. and its consolidated affiliates.

Business Strategy

Our business strategy is to provide advanced technologies that improve reservoir performance by (i) continuing the development of proprietary technologies through client-driven research and development, (ii) expanding the services and products offered throughout our global network of offices and (iii) acquiring complementary technologies that add key technologies or market presence and enhance existing services and products.

Development of New Technologies, Services and Products

We conduct research and development to meet the needs of our clients who are continually seeking new services and technologies to lower their costs of finding, developing and producing oil and gas. While the aggregate number of wells being drilled per year fluctuates in response to market conditions, oil and gas producers have, on a proportional basis, increased expenditures on technology services to improve their understanding of the reservoir, increased production of oil and gas from their producing fields, and more recently, CCS projects. We intend to continue concentrating our efforts on services and technologies that help our clients reduce risk by evaluating geologic and engineering aspects of subsurface stratigraphic targets to improve reservoir performance and increase oil and gas recovery, as well as CCS projects and other projects directed at the global objective to reduce carbon emissions.

International Expansion of Services and Products

Another component of our business strategy is to broaden the spectrum of services and products offered to our clients on a global basis. We intend to continue using our worldwide network of offices to offer our services and products that have been developed internally or obtained through acquisitions. This global emphasis allows us to increase our revenue and enhance our profit through efficient utilization of our worldwide network.

Acquisitions

We continually review potential acquisitions to add key services and technologies, enhance market presence or complement existing business.

More information relating to any significant acquisitions is included in Note 3 - Acquisitions and Divestures of the Notes to the Consolidated Financial Statements.

Operations

We derive our revenue from services and product sales to clients primarily in the oil and gas and associated industries.

We operate our business in two segments. These complementary operating segments provide different services and products and utilize different technologies for evaluating and improving reservoir performance and increasing oil and gas recovery from new and existing fields. Disclosure relating to the operations and financial information of these operating segments is included in Note 20 - Segment Reporting and Other Disaggregated Information of the Notes to the Consolidated Financial Statements.

•
Reservoir Description : Encompasses the characterization of petroleum reservoir rock, and reservoir fluids samples to increase production and improve recovery of crude oil and natural gas from our clients' reservoirs. We provide laboratory-based analytical and field services to characterize properties of crude oil and crude oil-derived products to the oil and gas industry. Services associated with these fluids include determining the quality and measuring the quantity of the reservoir fluids and their derived products, such as gasoline, diesel and biofuels. We also provide proprietary and joint industry studies based on these types of analyses and manufacture associated laboratory equipment. In addition, we provide reservoir description capabilities that support various activities associated with energy transition projects, including services that support carbon capture, utilization and storage, geothermal projects, and the evaluation and appraisal of mining activities around lithium and other elements necessary for energy storage.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-03-23_item7_mdna.md, 10-K_2026-03-23_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
