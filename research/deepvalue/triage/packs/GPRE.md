# Triage pack — GPRE · Green Plains Inc.

_Generated 2026-09-05 02:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** GPRE · **Name:** Green Plains Inc.
- **CIK:** 0001309402
- **SIC:** 2860 — Industrial Organic Chemicals
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/GPRE

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Green Plains Inc.
- **CIK:** 1,309,402 · **SIC:** 2860 (Industrial Organic Chemicals) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 14.96 |
| mktcap | $1.0B |
| ev | $1.3B |
| ev_ebit | n/a |
| fcf | $73.7M |
| fcf_yield | 7.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -5.0% |
| net_debt | $201.8M |
| net_debt_ebit | n/a |
| cash | $185.4M |
| ltd | $387.2M |
| equity | $869.9M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $2.1B |
| revenue_prior | $2.5B |
| rev_growth | -14.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$67.2M |
| net_income | -$121.3M |
| cfo | $110.9M |
| capex | $37.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 6.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 70,095,328 |
| shares_py | 65,565,368 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 52.7% |
| r6m | -3.5% |
| off_52w_high | -22.2% |
| adv20 | $24.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.59 |
| r_ev_ebit | 0.00 |
| r_roic | 0.18 |
| r_rev_growth | 0.06 |
| r_buyback | 0.15 |
| score | 0.25 |

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
| rank | 446 |

**Screen rationale:** 12-1 momentum 52.7%


## 3. Share count trend

- Shares outstanding: **70,095,328** (CY2026Q2I) vs **65,565,368** prior year (CY2025Q2I)
- Change: **6.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-04-23** — Item 1.01 (Entry into a Material Definitive Agreement): As previously disclosed, on March 25, 2022, Green Plains Finance Company LLC, Green Plains Grain Company LLC, and Green Plains Trade Group LLC (collectively, the "Borrowers"), all wholly owned subsidiaries of Green Plains Inc. (the "Company"), together with...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Green Plains Reports Second Quarter 2026 Financial Results'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (gpreq22026earningsrelease.htm)

Green Plains Reports Second Quarter 2026 Financial Results

Results for the Second Quarter of 2026:

• Net income attributable to Green Plains of $67.1 million, or EPS of $0.83 per diluted share

• Adjusted EBITDA of $93.3 million, inclusive of $34.6 million from the base business and $58.7 million in 45Z production tax credit value net of discounts and other costs

• Cash flow from operating activities of $86.3 million for the second quarter of 2026

• The Superior, Iowa facility joined the Central City, Nebraska facility in achieving the Highly Protected Status from GPRE's property insurance carrier, FM

• Lowered selling, general and administrative expenses by $5.9 million or 21% to $21.7 million for the second quarter of 2026 compared to the second quarter of 2025

• 88% utilization from the eight operating ethanol plants in the quarter

OMAHA, Neb., August 6, 2026 (BUSINESS WIRE) - Green Plains Inc. (NASDAQ:GPRE) ("Green Plains" or the "company") today announced financial results for the second quarter of 2026. Net income attributable to the company was $67.1 million, or $0.83 per diluted share compared to net loss attributable to the company of $72.2 million or $(1.09) per diluted share, for the same period in 2025. Revenues were $446.2 million for the second quarter of 2026 compared with $552.8 million for the same period last year. Core operating profitability strengthened with adjusted EBITDA of $93.3 million compared to $16.4 million for the same period in the prior year.

"The second quarter demonstrated the earnings capability of the Green Plains platform," said Chris Osowski, President and Chief Executive Officer. "Even with lower utilization due to maintenance, we generated more than $67 million of net income. The combination of operational excellence, achieving multiple safety milestones, improved ethanol economics, strong commercial execution and our low-carbon platform is translating into meaningful financial results. "

"Our financial profile continues to improve as we execute on our operating and capital allocation priorities," said Ann Reis, Chief Financial Officer. "Stronger earnings from our plants and continued discipline on SG&A are generating meaningful cash flow, which we intend to direct toward reducing debt and building a more resilient balance sheet that is positioned for growth."

Results of Operations

Green Plains' ethanol production segment sold 160.7 million gallons of ethanol during the second quarter of 2026, compared with 193.6 million gallons for the same period in 2025. The consolidated ethanol crush margin was $95.1 million for the second quarter of 2026, compared with $26.3 million for the same period in 2025. The consolidated ethanol crush margin is the ethanol production segment's operating income before depreciation and amortization, including intercompany marketing and agribusiness fees and excluding net nonethanol operating activities.

Consolidated revenues decreased $106.6 million for the three months ended June 30, 2026, compared with the same period in 2025, primarily due to lower revenues within our ethanol production segment as a result of lower volumes sold primarily driven by the disposition of our Obion, Tennessee plant.

Net income attributable to Green Plains increased $139.4 million and adjusted EBITDA increased $76.9 million for the three months ended June 30, 2026 compared with the same period in 2025 primarily due to recognition of $58.7 million of 45Z production tax credits net of discounts and other costs, higher margins in our ethanol production and agribusiness and energy services segments and lower selling, general and administrative expenses as a result of restructuring costs of $2.5 million incurred during the three months ended June 30, 2025. Interest expense decreased $5.8 million for the three months ended June 30, 2026 compared with the same period in 2025 primarily due to prior year loan fees related to the issuance and modification of warrants in conjunction with access to a short-term line of credit and an amendment on our Junior Notes, offset by higher debt balances associated with carbon sequestration equipment. Income tax benefit was $5.5 million for the three months ended June 30, 2026, compared with income tax expense of $2.3 million for the same period in 2025 primarily due to the changes in the valuation allowance on deferred tax assets, offset by an increase in pre-tax book income from the generation of non-taxable 45Z production tax credits.

During the first quarter of 2026, the company elected to early adopt ASU 2025-10, Accounting for Government Grants Received by Business Entities . Concurrently, the company elected to change its accounting policy related to the recognition of Section 45Z clean fuel production tax credits. The change in accounting policy results in the recognition of Section 45Z clean fuel production tax credits by analogy under the income model of ASU 2025-10, which results in a reduction of cost of goods sold in the statements of operations and recognition as production tax credits on the consolidated balance sheets. The company previously

recorded the credits under ASC 740, Accounting for Income Taxes , which resulted in recognition within income tax benefit in the statements of operations and deferred income taxes, net in the consolidated balance sheets. The company determined that the income model under ASU 2025-10 is preferable because it better reflects the financial benefit of Section 45Z clean fuel production tax credits netted against the costs to produce the low-carbon fuels that the tax legislation was meant to incentivize. The company determined that retrospective adjustment to prior period financials is required. No Section 45Z clean fuel production tax credits were recognized during the first or second quarters of 2025, so no adjustments were made in the statements of operations; however, the company has reclassified balances previously reported as deferred income taxes, net, and other long-term liabilities to production tax credits on the consolidated balance sheets as of December 31, 2025.

Segment Information

The company reports the financial and operating performance for the following two operating segments: (1) ethanol production, which includes the production, storage, and transportation of ethanol, distillers grains, Ultra-High Protein, and renewable corn oil, in addition to CCS operations at our three Nebraska plants and (2) agribusiness and energy services, which includes grain handling and storage, commodity marketing and merchant trading for company-produced and third-party ethanol, distillers grains, renewable corn oil, natural gas and other commodities.

GREEN PLAINS INC.

SEGMENT OPERATIONS

(unaudited, in thousands)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | % Var. | 2026 | 2025 | % Var.
Revenues
Ethanol production | 410,768 | 527,153 | (22.1)% | 804,127 | 1,024,925 | (21.5)%
Agribusiness and energy services | 39,546 | 31,531 | 25.4 | 98,151 | 141,360 | (30.6)
Intersegment eliminations | (4,090) | (5,855) | (30.1) | (10,250) | (11,941) | (14.2)
446,224 | 552,829 | (19.3)% | 892,028 | 1,154,344 | (22.7)%
Gross margin
Ethanol production (1) (2) | 104,229 | 33,490 | * | 175,957 | 27,798 | *
Agribusiness and energy services | 8,801 | 8,080 | 8.9 | 25,019 | 16,811 | 48.8
113,030 | 41,570 | 171.9% | 200,976 | 44,609 | *
Depreciation and amortization
Ethanol production | 22,673 | 22,918 | (1.1)% | 45,891 | 43,953 | 4.4%
Agribusiness and energy services (3) | 31 | 3,860 | (99.2) | 62 | 4,458 | (98.6)
Corporate activities | 745 | 782 | (4.7) | 1,133 | 1,536 | (26.2)
23,449 | 27,560 | (14.9)% | 47,086 | 49,947 | (5.7)%
Operating income (loss)
Ethanol production (2) (4) (5) | 70,977 | (12,218) | * | 110,399 | (51,768) | *
Agribusiness and energy services (3) | 6,699 | 849 | * | 20,531 | 3,282 | *
Corporate activities (6) (7) | (9,802) | (16,994) | (42.3) | (18,284) | (42,137) | (56.6)
67,874 | (28,363) | * | 112,646 | (90,623) | *
Adjusted EBITDA
Ethanol production (2) (4) (5) | 94,454 | 8,992 | * | 157,510 | (10,424) | *
Agribusiness and energy services | 6,924 | 5,028 | 37.7 | 20,935 | 8,184 | 155.8
Corporate activities (8) | (8,078) | (42,903) | (81.2) | (13,642) | (68,149) | (80.0)
EBITDA | 93,300 | (28,883) | * | 164,803 | (70,389) | *
Restructuring costs | — | 2,520 | * | — | 19,106 | *
Loss on sale of assets | — | 4,044 | * | — | 4,044 | *
Impairment of assets held for sale | — | 10,724 | * | — | 10,724 | *
Loss on sale of equity method investment | — | 26,987 | * | — | 26,987 | *
Proportional share of EBITDA adjustments to equity method investees | 45 | 1,050 | (95.7) | 90 | 1,828 | (95.1)
93,345 | 16,442 | * | 164,893 | (7,700) | *

(1) Ethanol production includes $60.4 million and $116.5 million of Section 45Z production tax credits net of discounts and other costs for the three and six months ended June 30, 2026, recorded as a reduction of cost of goods sold.

(2) Ethanol production includes margins from a one-time sale of accumulated RINs of $22.6 million for the three and six months ended June 30, 2025.

(3) Depreciation and amortization for agribusiness and energy services includes impairment of property and equipment of $3.1 million for the three and six months ended June 30, 2025.

(4) Ethanol production includes $58.7 million and $113.9 million of 45Z production tax credits recorded net of discounts, other costs and selling, general and administrative expenses for the three and six months ended June 30, 2026, respectively.

(5) Ethanol production includes impairment of assets held for sale of $10.7 million for the three and six months ended June 30, 2025.

(6) Corporate activities includes $1.7 million and $12.0 million of restructuring costs for the three and six months ended June 30, 2025 as a result of the company's cost reduction initiative, including severance related to the departure of its former CEO.

(7) Corporate activities include a pretax loss on sale of assets of $4.0 million for the three and six months ended June 30, 2025.

(8) Corporate activities include a pretax loss on sale of assets of $4.0 million and a pretax loss on sale of equity method investment of $27.0 million for the three and six months ended June 30, 2025, respectively.

* Percentage variance not considered meaningful

GREEN PLAINS INC.

SELECTED OPERATING DATA

(unaudited, in thousands)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | % Var. | 2026 | 2025 | % Var.
Ethanol production
Ethanol (gallons) | 160,700 | 193,571 | (17.0)% | 334,896 | 388,899 | (13.9)%
Distillers grains (equivalent dried tons) | 323 | 413 | (21.8) | 685 | 830 | (17.5)
Ultra-High Protein (tons) | 49 | 66 | (25.8) | 103 | 134 | (23.1)
Renewable corn oil (pounds) | 58,332 | 65,231 | (10.6) | 116,808 | 129,494 | (9.8)
Corn consumed (bushels) | 54,558 | 65,312 | (16.5) | 113,360 | 131,576 | (13.8)
Agribusiness and energy services (1)
Ethanol sold (gallons) | 180,760 | 225,703 | (19.9) | 356,905 | 481,424 | (25.9)

(1) Includes gallons from the ethanol production segment.

GREEN PLAINS INC.

CONSOLIDATED CRUSH MARGIN

(unaudited, in thousands)

Three Months Ended June 30,
2026 | 2025
Ethanol production operating income (loss) (1) | 70,977 | (12,218)
Depreciation and amortization | 22,673 | 22,918
Impairment of assets held for sale | — | 10,724
Adjusted ethanol production operating income | 93,650 | 21,424
Intercompany fees and nonethanol operating activities, net (2) | 1,421 | 4,862
Consolidated ethanol crush margin | 95,071 | 26,286

(1) For the three months ended June 30, 2025, ethanol production includes margins from a one-time sale of accumulated RINs of $22.6 million and an inventory lower of cost or net realizable value adjustment of $2.3 million.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-10_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Incorporated in Iowa, Green Plains is a renewable fuels and agricultural technology company focused on producing low-cost, low-CI ethanol and related co-products, including high protein feeds and corn oil from locally sourced corn. Our goal is to create value through an operational excellence focus including disciplined operations, cost leadership and carbon reduction as we position the company to benefit from expanding low-carbon fuel markets.

Founded in 2004, Green Plains now owns nine strategically located plants across the Midwest, capable of processing approximately 287 million bushels of corn annually, when all plants are operating. Today, our focus is to continue operating safely, efficiently and cost-effectively while reducing the CI of our products and maintaining financial flexibility to support long-term growth. During the year, under new leadership, the company completed targeted asset sales, strengthened liquidity and reduced debt, positioning Green Plains to capture value from the next phase of the low-carbon transition. Our streamlined platform is positioned to create value through our focus on operational excellence, continuous improvement and disciplined capital allocation.

Our carbon reduction strategy plays a central role in achieving lower CI biofuel production and participation in various clean fuel programs. Carbon capture and storage ("CCS") is operational at our three Nebraska facilities. These plants are connected to the Tallgrass Trailblazer CO2 Pipeline, while our Iowa and Minnesota locations are committed to CCS through Summit Carbon Solutions, which publicly projects operations commencing in 2028. CCS initiatives are expected to significantly lower CI across our platform. Further, the company has purchased RECs to lower CIs at certain plants. Based on current CI score estimates, all eight operational Green Plains facilities are expected to qualify for the Section 45Z Clean Fuel Production Credit beginning in 2026, with six facilities qualifying in 2025, inclusive of three non-CCS facilities. In addition, we are collaborating with global partners to explore innovative options for carbon use where pipeline transport or direct injection may not be feasible. Reducing the CI of our fuel ethanol could allow us to benefit from state and federal clean fuel programs, including LCFS and federal tax credits under the IRA and OBBB, and could position our low-carbon ethanol as a potential feedstock for ATJ pathways to produce SAF.

We have installed and are operating FQT MSC™ technology at four of our biorefineries. Through our value-added ingredients initiative, we produce Ultra-High Protein, a feed ingredient with protein concentrations of 50% or greater and yeast concentrations of 25%, and increase production of renewable corn oil. We successfully completed full scale 60% protein production runs using FQT's MSC™ system, which is our new specialty feed ingredient branded as Sequence™.

In September 2022, we broke ground at our biorefinery in Shenandoah, Iowa, as the first location to deploy FQT's CST™ at commercial scale, and during 2024 the company successfully commissioned the CST™ equipment in the Shenandoah facility. FQT's CST™ technology allows for the production of both food and industrial grade dextrose at a dry mill ethanol plant to target applications in food production, in addition to serving as a feedstock for renewable chemicals and synthetic biology. The facility has a rated capacity of 60 million pounds of product per year. The facility has been idled since the first quarter of 2025 as the company focuses on optimizing its product mix to maximize current returns. The decision to temporarily pause operations presents an opportunity to make some related infrastructure improvements, which would require additional investment.

Additionally, we have taken advantage of opportunities to divest certain assets to reallocate capital toward our current growth initiatives. We are focused on generating stable and growing operating margins through our business segments and risk management strategy.

SAF is a drop-in fuel, chemically identical to petroleum-based jet fuel and can be blended into the fuel supply at varying levels. There is an increasing focus on using this fuel to reduce the carbon footprint of air travel. SAF can be produced from vegetable and waste oil feedstocks, such as our renewable corn oil. Additionally, ATJ technologies are emerging and being commercialized that use low-CI ethanol as a feedstock to produce SAF.

T a b le of Contents

In July 2023, we announced a technology collaboration with Equilon Enterprises LLC, which allows us to use FQT's precision separation and processing technology with Shell Fiber Conversion Technology. The two technologies will combine fermentation, mechanical separation and processing, and fiber conversion into one platform. This has the potential to create a new process to liberate nearly all available distillers corn oil currently bound in the fiber fraction of the corn kernel, generate cellulosic sugars for production of low-carbon ethanol, and enhance and expand available high protein to produce high-quality ingredients for global animal feed diets. The large-scale demonstration facility is operational and technology and product development has continued to advance through 2025.

Our profitability is highly dependent on commodity prices, particularly for ethanol, distillers grains, Ultra-High Protein, renewable corn oil, soybean meal, corn, and natural gas. Since market price fluctuations of these commodities are not always correlated, our operations may be unprofitable at times. We use a variety of risk management tools and hedging strategies to monitor price risk exposure at our ethanol plants and lock in favorable margins or reduce production when margins are compressed. Our profitability could be significantly impacted by price movements of the aforementioned commodities.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

We maintained an average utilization rate of approximately 82%, or 94% excluding Fairmont, of capacity during 2025, compared with 87% of capacity for the prior year, with both years measured using our updated capacity as discussed in Item 1 of this filing. Our operating strategy is to transform our company to a value-add agricultural technology company creating lower carbon, high-value ingredients from existing resources. Depending on the margin environment, we may exercise operational discretion that results in reductions in production volumes. It is possible that throughput volumes could fluctuate in the future, depending on various factors that drive each biorefinery's variable contribution margin, including future driving and gasoline demand for the industry, demand for valuable co-products we produce, and the supply and pricing of renewable feedstocks needed to operate our biorefineries.

Comparability

The following summarizes various events that affect the comparability of our operating results for the past three years:

• September 2025 | Sale of ethanol plant in Rives, Tennessee (or the "Obion Transaction")
• April 2025 | Ceasing of a third-party ethanol marketing agreement effective April 1, 2025
• January 2025 | Began generating Section 45Z clean fuel production tax credits
• January 2025 | Began corporate restructuring and cost savings initiatives lasting throughout 2025
• January 2025 | Idling of ethanol plant in Fairmont, Minnesota
• September 2024 | Sale of terminal located in Birmingham, Alabama
• September 2023 | Sale of ethanol plant located in Atkinson, Nebraska

A discussion regarding our financial condition and results of operations for the year ended December 31, 2024, compared to the year ended December 31, 2023, can be found under Item 7 in our Annual Report on Form 10-K for the fiscal year ended December 31, 2024, filed with the SEC on February 7, 2025.

T a b le of Contents

Segment Results

We report the financial and operating performance for the following two operating segments: (1) ethanol production, which includes the production, storage, and transportation of ethanol, distillers grains, Ultra-High Protein and renewable corn oil and (2) agribusiness and energy services, which includes grain handling and storage, commodity marketing and merchant trading for company-produced and third-party ethanol, distillers grains, renewable corn oil, natural gas and other commodities.

Corporate activities include gain on sale of assets and selling, general and administrative expenses, consisting primarily of compensation, professional fees and overhead costs not directly related to a specific operating segment.

During the normal course of business, our operating segments do business with each other. For example, our agribusiness and energy services segment procures grain and natural gas and sells products, including ethanol, distillers grains, Ultra-High Protein, and renewable corn oil of our ethanol production segment. These intersegment activities are treated like third-party transactions with origination, marketing and storage fees charged at estimated market values. Consequently, these transactions affect segment performance; however, they do not impact our consolidated results since the revenues and corresponding costs are eliminated.

When we evaluate segment performance, we review the following segment information as well as earnings before interest expense, income taxes, depreciation and amortization, or EBITDA, and adjusted EBITDA.

The selected operating segment financial information are as follows (in thousands):

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-10_item1_business.md)

(1) Produces Ultra-High Protein.

(2) Connected to Tallgrass Trailblazer Pipeline.

(3) Committed to Summit Carbon Solutions Pipeline.

(4) Plant idled in January 2025.

Our business is directly affected by the supply and demand for ethanol and other fuels in the markets served by our assets. Miles driven typically increase during the spring and summer months related to vacation travel, followed closely by the fall season due to holiday travel.

T a b le of Contents

Corn Feedstock and Ethanol Production. Our plants use corn as feedstock in a dry mill ethanol production process. Each of our plants requires on average approximately 32 million bushels of corn annually, depending on its production capacity. The price and availability of corn are subject to significant fluctuations driven by a number of factors that affect commodity prices in general, including crop conditions, weather, governmental programs, freight costs and global demand. Ethanol producers are generally unable to pass increased corn costs to customers.

Our corn supply is obtained primarily from local markets. We use cash and forward purchase contracts with grain producers and elevators to buy corn. We maintain direct relationships with local farmers, grain elevators and cooperatives, which serve as our primary sources of grain feedstock for all ten of our ethanol plants. This allows us to purchase much of the corn we need directly from farmers throughout the year. Each of our plants is also situated on rail lines or has other logistical solutions to access corn supplies from other regions of the country should local supplies become insufficient.

Corn is received at the plant by truck or rail then weighed and unloaded into a receiving building. Grain storage facilities are used to inventory grain that is passed through a scalper to remove rocks and debris prior to processing. The corn is then transported to a hammer mill where it is ground into flour and conveyed into a slurry tank for enzymatic processing. Water, heat and enzymes are added to convert the complex starch molecules into simpler carbohydrates. The slurry is heated to reduce the potential of microbial contamination and pumped into a liquefaction tank where additional enzymes are added. Next, the grain slurry is pumped into fermenters, where yeast, enzymes, and nutrients are added and the fermentation process is started. A beer column, within the distillation system, separates the alcohol from the spent grain mash. The alcohol is dehydrated to 200-proof alcohol and pumped into a holding tank and blended with approximately 2% denaturant as it is pumped into finished product storage tanks.

Distillers Grains. The spent grain mash is pumped from the beer column into a decanter-type centrifuge for dewatering. The water, or thin stillage, is pumped from the centrifuge into an evaporator, where it is concentrated into a thick syrup. The solids, or wet cake, that exit the centrifuge are conveyed to the dryer system and dried at varying temperatures to produce distillers grains. Syrup is reapplied to the wet cake prior to drying to provide additional nutrients. Distillers grains, the principal co-product of the ethanol production process, are used as mid-protein, high-energy animal feed and marketed to the dairy, beef, swine and poultry industries.

We can produce three forms of distillers grains, depending on the number of times the solids are passed through the dryer system:

• wet distillers grains, which contain approximately 65% to 70% moisture, have a shelf life of approximately three days and is therefore sold to dairies or feedlots within the immediate vicinity of our plants;

• modified wet distillers grains, which is dried further to approximately 50% to 55% moisture, have a shelf life of approximately three weeks and are marketed to regional dairies and feedlots; and

• dried distillers grains, which have been dried more extensively to approximately 10% to 12% moisture, have an almost indefinite shelf life and may be stored, sold and shipped to any market.

Ultra-High Protein . Ultra-High Protein is fermented corn protein produced by further processing of the spent grain mash from the beer column. The spent grain is processed using FQT's MSC™ technology, which contains a series of screening equipment to remove fiber from the spent grain which is sent to the distillers grain dryer. The remaining product is washed and clarified into a wet protein stream which is dried in a ring dryer to produce Ultra-High Protein meal with protein concentrations of approximately 50%. Our specialty feed ingredient, Sequence™ has protein concentrations of approximately 60%.

Renewable Corn Oil. Renewable corn oil systems extract non-edible renewable corn oil from the thin stillage evaporation process immediately before the production of distillers grains. Renewable corn oil is produced by processing the syrup through a decanter-style, or disk-stack, centrifuge. The centrifuges separate the relatively light renewable corn oil from the heavier components of the syrup. Across our entire platform, we extract on average approximately 1.0 pound of renewable corn oil per bushel of corn used to produce ethanol. Industrial uses for renewable corn oil are primarily as a feedstock for renewable diesel and biodiesel. Additionally, it is also used as a livestock feed additive.

Natural Gas . Depending on production parameters, our ethanol plants use on average approximately 27,000 BTUs of natural gas per gallon of production. We have service agreements to acquire the natural gas we need and transport the gas through pipelines to our plants.

T a b le of Contents

Electricity . Our plants require on average approximately 0.9 kilowatt hours of electricity per gallon of production. Local utilities supply the necessary electricity to all of our ethanol plants.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-10_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-10_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-10_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-10_item7_mdna.md, 10-K_2026-02-10_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
