# Triage pack — HLLY · Holley Inc.

_Generated 2026-09-04 16:12 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** HLLY · **Name:** Holley Inc.
- **CIK:** 0001822928
- **SIC:** 3714 — Motor Vehicle Parts & Accessories
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/HLLY

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Holley Inc.
- **CIK:** 1,822,928 · **SIC:** 3714 (Motor Vehicle Parts & Accessories) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 3.10 |
| mktcap | $375.8M |
| ev | $825.4M |
| ev_ebit | 10.0x |
| fcf | $33.9M |
| fcf_yield | 9.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.2% |
| net_debt | $449.6M |
| net_debt_ebit | 5.5x |
| cash | $69.0M |
| ltd | $518.6M |
| equity | $449.7M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $613.5M |
| revenue_prior | $602.2M |
| rev_growth | 1.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $82.5M |
| net_income | $19.2M |
| cfo | $46.2M |
| capex | $12.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 121,234,143 |
| shares_py | 120,499,661 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -20.8% |
| r6m | -14.6% |
| off_52w_high | -29.4% |
| adv20 | $3.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.69 |
| r_ev_ebit | 0.76 |
| r_roic | 0.61 |
| r_rev_growth | 0.41 |
| r_buyback | 0.54 |
| score | 0.60 |

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
| rank | 144 |

**Screen rationale:** cheap at 10.0x EV/EBIT


## 3. Share count trend

- Shares outstanding: **121,234,143** (CY2026Q2I) vs **120,499,661** prior year (CY2025Q2I)
- Change: **0.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 16 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 10 |
| F | 6 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter Highlights vs. Prior Year Period'; skipped 16 forward-looking-statement block(s); 11 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (hlly-20260628xexx991.htm)

Second Quarter Highlights vs. Prior Year Period

• Net Sales grew 3.2% to $172.0 million compared to $166.7 million last year

• Core business net sales 1 grew by 4.9% after excluding portfolio divestitures and portfolio rebalancing initiative.

• Net Loss was $(2.4) million, or $(0.02) per diluted share, compared to Net Income of $10.9 million, or $0.09 per diluted share, last year

• Includes a $28.3 million loss on the sale of non-core assets related to the Company's portfolio rebalancing initiative.

• Net Cash Provided by Operating Activities was $47.1 million compared to $40.5 million last year

• Adjusted Net Income 2 was $24.0 million compared to $10.6 million last year

• Adjusted EBITDA 2 was $33.8 million compared to $36.4 million last year

• Adjusted EBITDA margin 1 was 19.6% compared to 21.9% last year

• Free Cash Flow 2 was $40.9 million compared to $35.7 million last year

1 Core business net sales excludes sales of divested businesses and the portfolio rebalancing initiative.

2 See "Use and Reconciliation of Non-GAAP Financial Measures" below.

"Our second quarter results reflect positive core growth and continued execution against the strategic priorities we outlined earlier this year, with three of our four business segments delivering year-over-year core growth," said Matthew Stevenson, President and Chief Executive Officer of Holley.

Stevenson continued, "We believe we are entering the second half of the year with solid momentum, supported by new national retailer placements, a healthy cadence of product innovation, and several important launches slated for the coming months. At the same time, we have reinvigorated our marketing calendar with a greater focus on brand activation and enthusiast engagement, helping to strengthen awareness and demand across our portfolio.

"During the quarter we completed the sale of our non-core Restoration brands, including Scott Drake and Brothers Trucks, a step that further reduces complexity and enables us to concentrate resources on our highest-priority growth opportunities. We remain focused on disciplined execution and believe the actions we have taken position Holley for continued progress in the periods ahead."

Jesse Weaver, Chief Financial Officer of Holley, added, "The second quarter showcased our continued focus on cash generation, balance sheet improvement, and disciplined capital allocation. Our underlying operating performance was stronger than the year-over-year Adjusted EBITDA comparison suggests: the prior-year quarter included a one-time, non-cash benefit from the capitalization of tariff costs that did not repeat this year, and adjust for that item, we believe Adjusted EBITDA performance was approximately flat year-over-year. We generated strong free cash flow in the quarter and year-to-date, which enabled us to continue making progress on our capital priorities.

"During the quarter, we repurchased approximately $2.0 million of our common stock, reflecting our confidence in the long-term value of the business. Following a $15.0 million voluntary debt prepayment made after quarter-end, we have now reduced debt by $115.0 million through voluntary prepayments since September 2023. Combined with our strong cash generation, these actions contributed to another quarter of leverage reduction helping us maintain progress towards finishing the year below our targeted leverage ratio of 3.5x.

"Based on our first-half performance and the opportunities we see in the second half of the year, we are reiterating our full-year guidance and remain focused on delivering sustainable value for our shareholders."

Strategic Business Highlights and Recent Events

• 27 brands delivered growth across DTC and B2B channels.

• Generated $40.9 million of free cash flow and remain on track for year-end leverage below 3.5x.

• Long Term Strategic initiatives drove $13.4 million in revenue and delivered $8.3 million in cost savings.

• Realigned marketing to strengthen consumer engagement and brand activation.

• Repurchased ~$2.0 million of shares, reinforcing confidence in our long-term value creation.

• Continued portfolio rebalancing through the divestiture of the non-core Restoration brands.

• Reduced debt by an additional $15.0 million, bringing total debt reduction to $115.0 million since September 2023.

• Well positioned for H2 2026 with new retail placements and a strong product launch pipeline.

Outlook

**For the year ending December 31, 2026, core business revenue guidance remains unchanged:

Metric | Current Full Year 2026 Outlook
Net Sales Core Business Growth Rate % 1 | $610 - $640 million ~2% to ~7%
Adjusted EBITDA* | $127 - $137 million
Capital Expenditures | $15 - $20 million
Depreciation and Amortization Expense | $24 - $26 million
Interest Expense (excluding collar revaluation) | $42 - $47 million

1 Core Business Growth Rate, excludes impact from Portfolio Rebalancing Initiative.

* Holley is not providing reconciliations of forward-looking full year 2026 Adjusted EBITDA outlook because certain information necessary to calculate the most comparable GAAP measure, net income, is unavailable due to the uncertainty and inherent difficulty of predicting the occurrence and the future financial statement impact of certain items. Therefore, as a result of the uncertainty and variability of the nature and amount of future adjustments, which could be significant, Holley is unable to provide these forward-looking reconciliations without unreasonable effort. Accordingly, Holley is relying on the exception provided by Item 10(e)(1)(i)(B) of Regulation S-K to exclude these reconciliations.

About Holley Performance Brands

Holley Performance Brands (NYSE: HLLY) leads in the design, manufacturing and marketing of high-performance products for automotive enthusiasts. The company owns and manages a portfolio of iconic brands, catering to a diverse community of enthusiasts passionate about the customization and performance of their vehicles. Holley Performance Brands distinguishes itself through a strategic focus on four consumer vertical groupings, including American Performance, Modern Truck & Off-Road, Euro & Import, and Safety & Racing, ensuring a wide-ranging impact across the automotive aftermarket industry. Renowned for its innovative approach and strategic acquisitions, Holley Performance Brands is committed to enhancing the enthusiast experience and driving growth through innovation. For more information on Holley Performance Brands and its dedication to automotive excellence, visit https://www.holley.com.

Nathan Espinosa/Michael Murray

Kahn Media

818-881-5246

Holley@KahnMedia.com

[Financial Tables to Follow]

HOLLEY INC. and SUBSIDIARIES

CONDENSED CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME

(In thousands)

(Unaudited)

For the thirteen weeks ended | For the twenty-six weeks ended
June 28, | June 29, | Variance | Variance | June 28, | June 29, | Variance | Variance
2026 | 2025 | ($) | (%) | 2026 | 2025 | ($) | (%)
Net sales | 172,007 | 166,661 | 5,346 | 3.2 | % | 319,337 | 319,705 | (368) | -0.1 | %
Cost of goods sold | 101,463 | 97,103 | 4,360 | 4.5 | % | 188,057 | 186,059 | 1,998 | 1.1 | %
Gross profit | 70,544 | 69,558 | 986 | 1.4 | % | 131,280 | 133,646 | (2,366) | -1.8 | %
Selling, general, and administrative | 40,427 | 32,954 | 7,473 | 22.7 | % | 75,829 | 69,653 | 6,176 | 8.9 | %
Research and development costs | 3,740 | 5,086 | (1,346) | -26.5 | % | 7,736 | 9,179 | (1,443) | -15.7 | %
Amortization of intangible assets | 3,416 | 3,350 | 66 | 2.0 | % | 6,844 | 6,882 | (38) | -0.6 | %
Restructuring costs | 840 | 355 | 485 | 136.7 | % | 1,715 | 818 | 897 | 109.7 | %
Loss on sale of assets | 28,259 | — | 28,259 | nm | 28,224 | — | 28,224 | nm
Other operating (income) expense | (8,903) | 299 | (9,202) | nm | (9,341) | 257 | (9,598) | nm
Total operating expense | 67,779 | 42,044 | 25,735 | 61.2 | % | 111,007 | 86,789 | 24,218 | 27.9 | %
Operating income | 2,765 | 27,514 | (24,749) | -89.9 | % | 20,273 | 46,857 | (26,584) | -56.7 | %
Change in fair value of warrant liability | (548) | (7) | (541) | nm | (1,579) | (80) | (1,499) | nm
Change in fair value of earn-out liability | (1,258) | (219) | (1,039) | nm | (1,772) | (404) | (1,368) | nm
Interest expense, net | 8,201 | 13,374 | (5,173) | -38.7 | % | 18,119 | 29,082 | (10,963) | -37.7 | %
Total non-operating expense | 6,395 | 13,148 | (6,753) | -51.4 | % | 14,768 | 28,598 | (13,830) | -48.4 | %
Income (loss) before income taxes | (3,630) | 14,366 | (17,996) | -125.3 | % | 5,505 | 18,259 | (12,754) | -69.8 | %
Income tax (benefit) expense | (1,200) | 3,503 | (4,703) | nm | 679 | 4,579 | (3,900) | nm
Net income (loss) | (2,430) | 10,863 | (13,293) | -122.4 | % | 4,826 | 13,680 | (8,854) | -64.7 | %
Comprehensive income (loss):
Foreign currency translation adjustment | (1,869) | 1,239 | (3,108) | -250.9 | % | (2,825) | 954 | (3,779) | -396.2 | %
Total comprehensive income (loss) | (4,299) | 12,102 | (16,401) | -135.5 | % | 2,001 | 14,634 | (12,633) | -86.3 | %
Common Share Data:
Basic net income (loss) per share | (0.02) | 0.09 | (0.11) | -122.2 | % | 0.04 | 0.11 | (0.07) | -65.0 | %
Diluted net income (loss) per share | (0.02) | 0.09 | (0.11) | -122.3 | % | 0.04 | 0.11 | (0.07) | -65.2 | %
Weighted average common shares outstanding - basic | 120,285 | 119,163 | 1,122 | 0.9 | % | 120,050 | 119,006 | 1,044 | 0.9 | %
Weighted average common shares outstanding - diluted | 120,285 | 119,791 | 494 | 0.4 | % | 121,149 | 119,677 | 1,472 | 1.2 | %
nm - not meaningful

HOLLEY INC. and SUBSIDIARIES

CONDENSED CONSOLIDATED BALANCE SHEET

(In thousands)

(Unaudited)

As of
June 28, 2026 | December 31, 2025
Assets
Cash and cash equivalents | 69,020 | 37,231
Accounts receivable, less allowance for credit losses of $2,086 and $1,856, respectively | 64,158 | 57,895
Inventory | 180,202 | 205,661
Prepaids and other current assets | 17,231 | 15,374
Total current assets | 330,611 | 316,161
Property, plant, and equipment, net | 50,174 | 45,127
Goodwill | 370,958 | 372,340
Other intangibles assets, net | 369,753 | 396,910
Right-of-use assets | 40,872 | 33,415
Total assets | 1,162,368 | 1,163,953
Liabilities and Stockholders' Equity
Accounts payable | 55,972 | 60,121
Accrued liabilities | 40,553 | 48,316
Accrued interest | 3,401 | 115
Current portion of long-term debt | 8,207 | 6,571
Total current liabilities | 108,133 | 115,123
Long-term debt, net of current portion | 518,606 | 516,078
Warrant liability | 444 | 2,024
Earn-out liability | 273 | 2,045
Deferred taxes | 47,362 | 46,540
Other noncurrent liabilities | 37,812 | 33,218
Total liabilities | 712,630 | 715,028
Common stock | 12 | 12
Additional paid-in capital | 385,684 | 384,873
Treasury stock, at cost, 707,113 and zero shares held as of June 28, 2026 and December 31, 2025, respectively | (2,000) | —
Accumulated other comprehensive income (loss) | (2,705) | 120
Retained earnings | 68,747 | 63,920
Total stockholders' equity | 449,738 | 448,925
Total liabilities and stockholders' equity | 1,162,368 | 1,163,953

HOLLEY INC. and SUBSIDIARIES

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS

(In thousands)

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-16_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

We are a designer, marketer, and manufacturer of high-performance automotive aftermarket products serving car and truck enthusiasts, with sales, processing, and distribution facilities reaching most major markets in the United States, Canada, Europe and China. Holley designs, markets, manufactures and distributes a diversified line of performance automotive products including fuel injection systems, tuners, exhaust products, carburetors, safety equipment and various other performance automotive products. Our products are designed to enhance street, off-road, recreational and competitive vehicle performance and safety.

Central to our business and growth strategy is a commitment to innovation. We have a history of developing innovative products, including new additions to existing product families, expansions of product lines, accessory offerings, and ventures into entirely new categories. We believe this strategic approach allows us to continually adapt to evolving consumer needs. Furthermore, strategic acquisitions have played a significant role in our evolution. These acquisitions have enabled us to expand our brand portfolio, enter new product categories and consumer segments, enhance DTC scale and connection, increase market share in existing product categories, and realize valuable revenue and cost synergies. While we anticipate continued organic growth, we intend to continue evaluating opportunities for strategic acquisitions that align with our current business, expanding our reach within the target market.

Factors Affecting our Performance

We believe that our performance and future success depend on a number of factors that present significant opportunities for us but also pose risks and challenges, including those discussed below and in the section of this Form 10-K titled "Risk Factors."

Business Combination

On July 16, 2021, we consummated the Business Combination pursuant to the Merger Agreement, by and among Empower, Merger Sub I, Merger Sub II, and Holley Intermediate. The Merger Agreement provided for, among other things, the following transactions: (i) Merger Sub I merged with and into Holley Intermediate, the separate corporate existence of Merger Sub I ceased and Holley Intermediate became the surviving corporation, and (ii) Holley Intermediate merged with and into Merger Sub II, the separate corporate existence of Holley Intermediate, and Merger Sub II became the surviving limited liability company. Upon closing of the Business Combination, Empower changed its name to Holley Inc. and its trading symbol on the NYSE from "EMPW" to "HLLY."

The Business Combination was accounted for as a reverse recapitalization in accordance with U.S. Generally Accepted Accounting Principles ("U.S. GAAP"). Holley Intermediate was deemed the accounting acquirer with Holley Inc. as the successor registrant. As such, Empower was treated as the acquired company for financial reporting purposes, and financial statements for periods prior to the Business Combination are those of Holley Intermediate.

As a result of the Business Combination, Holley Inc. listed on the NYSE, which required us to hire additional personnel and implement procedures and processes to address public company regulatory requirements and customary practices. We have incurred and expect to continue to incur additional annual expenses as a public company for, among other things, directors' and officers' liability insurance, director fees, and additional internal and external accounting, legal, and administrative resources, including increased personnel costs, audit and other professional service fees.

Acquisitions

We have historically pursued a growth strategy through both organic growth and acquisitions. We have pursued acquisitions that we believe will help drive profitability, cash flow and stockholder value. We target companies that we believe are market leaders, expand our geographic presence, provide a highly synergistic opportunity and/or enhance our ability to provide a wide array of our products to our customers through our distribution network.

The acquisitions have all been accounted for in accordance with Financial Accounting Standards Board ("FASB") Accounting Standards Codification ("ASC") Topic 805, Business Combinations , and the operations of the acquired entities are included in our historical results for the periods following the closing of the applicable acquisition. See Note 1, " Description of the Business, Basis of Presentation, and Summary of Significant Accounting Policies " in the Notes to the Consolidated Financial Statements included in this Annual Report on Form 10-K for additional information related to our acquisitions and investments.

Business Environment

Our business and results of operations, financial condition, and liquidity are impacted by broad economic conditions including inflation, labor shortages, disruption of the supply chain, and potential tariffs, as well as by geopolitical events, including military conflicts (including the conflict in Ukraine, the conflict in Israel and surrounding areas, and the possible expansion of such conflicts). Our operations have been adversely impacted, and may continue to be adversely impacted, by inflationary pressures primarily related to transportation, labor and component costs. In response to the global supply chain volatility and inflationary impacts, we have attempted to minimize potential adverse impacts on our business with cost savings initiatives, price increases to customers, and by increasing inventory levels of certain products and working closely with our suppliers and customers to minimize disruptions in delivering products to customers. Our profitability has been, and may continue to be, adversely affected by constrained consumer demand, a shift in sales mix to lower-margin products, which is offset by our cost cutting and operating efficiency gains. Should the ongoing macroeconomic conditions not improve, or worsen, or if our attempts to mitigate the impact on our supply chain, operations and costs is not successful, our business, results of operations and financial condition may be adversely affected.

Key Components of Results of Operations

Net Sales

The principal activity from which we generate our sales is the designing, marketing, manufacturing and distribution of performance aftermarket automotive parts for our end consumers. Sales are displayed net of rebates and sales returns allowances. Sales returns are recorded as a charge against gross sales in the period in which the related sales are recognized.

Cost of Goods Sold

Cost of goods sold consists primarily of the cost of purchased parts and manufactured products, including materials and direct labor costs. In addition, warranty, incoming shipping and handling and inspection and repair costs are also included within costs of goods sold. Reductions in the cost of inventory to its net realizable value are also a component of cost of goods sold.

Selling, General, and Administrative

Selling, general, and administrative consist of payroll and related personnel expenses, IT and office services, office rent expense and professional services. In addition, self-insurance, advertising, research and development, outgoing shipping costs, pre-production and start-up costs are also included within selling, general, and administrative. We have incurred additional expenses as a result of operating as a public company, including expenses necessary to comply with the rules and regulations applicable to companies listed on a national securities exchange and related to compliance and reporting obligations pursuant to the rules and regulations of the SEC, as well as higher expenses for general and director and officer insurance, investor relations and other professional services.

Amortization of Intangible Assets

Amortization of intangible assets represents the non‑cash expense related to the systematic write down of our definite‑lived intangible assets.

Impairment of Indefinite-lived Assets

Impairment of indefinite-lived assets relates to indefinite-live trade name impairment charges.

Impairment of Goodwill

Impairment of goodwill relates to goodwill impairment charges.

Loss on Sale of Assets

Loss on sale of assets relates to the loss incurred related to the sale of Detroit Speed Engineering in the year ended December 31, 2024 .

Restructuring Costs

Restructuring costs consist of professional fees for legal, accounting, consulting, administrative, and other professional services directly attributable to restructuring.

Interest Expense

Interest expense consists of interest due on the indebtedness under our credit facilities. On December 31, 2025, $529.4 million was outstanding under the Credit Agreement. Interest is based on the secured overnight financing rate ("SOFR") or prime rate, plus the applicable margin rate.

Change in Fair Value of Warrant Liability

Change in fair value of warrant liability represents remeasurement gains or losses on outstanding warrant liabilities, driven primarily by changes in our stock price and related valuation inputs.

Change in Fair Value of Earn-out Liability

Change in fair value of earn‑out liability reflects adjustments to contingent consideration based on revised expectations of earn‑out performance and updated valuation assumptions.

Loss (Gain) on Early Extinguishment of Debt

Extinguishment of debt consists of gains or losses recognized in connection with the termination, refinancing, or repayment of existing debt arrangements. These amounts include the write‑off of unamortized deferred financing costs, prepayment penalties, and the impact of any negotiated settlement amounts differing from the carrying value of the extinguished debt.

Results of Operations

Year Ended December 31, 2025 Compared With Year Ended December 31, 2024

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-16_item1_business.md)

Item 1. Business

About Us

Founded in 1903, Holley, Inc. has been a part of the automotive industry for well over a century. We design, manufacture, and distribute high-performance automotive aftermarket products to car and truck enthusiasts primarily in the United States, Canada and Europe. Our products span a number of automotive platforms and are sold across multiple channels. We are a leading manufacturer of a diversified line of performance automotive products, including carburetors, fuel pumps, fuel injection systems, nitrous oxide injection systems, superchargers, exhaust headers, mufflers, distributors, ignition components, engine tuners and automotive performance plumbing products. We are also a leading manufacturer of exhaust products as well as shifters, converters, transmission kits, transmissions, tuners and automotive software. Our products are designed to enhance street, off-road, recreational and competitive vehicle performance through increased horsepower, torque and drivability. We have locations in the United States, Canada, Italy and China.

We attribute a major component of our success to our brands, including Holley, Holley EFI, MSD, Simpson, Flowmaster, EDGE, Cataclean, and Accel, among others. Through these strategic acquisitions, we have increased our market position in the otherwise highly fragmented performance automotive aftermarket industry.

We operate in the performance automotive aftermarket parts industry. We believe there is ample opportunity to continue our expansion into new products and markets, such as exterior accessories and mobile electronics, representing a natural progression for us to grow market share as these adjacencies are driven by passionate enthusiasts, consistent with our core categories. See also "Risk Factors — Risks Relating to Holley's Business and Industry — If the Company is unable to successfully design, develop and market new products, the Company business may be harmed" for a discussion of the risks related to the Company's new product development.

On July 16, 2021, we consummated a business combination (the "Business Combination") pursuant to that certain Agreement and Plan of Merger dated March 11, 2021 (the "Merger Agreement"), by and among Empower Ltd., ("Empower"), Empower Merger Sub I Inc., a direct wholly owned subsidiary of Empower ("Merger Sub I"), Empower Merger Sub II LLC, a direct wholly owned subsidiary of Empower ("Merger Sub II"), and Holley Intermediate Holdings, Inc. ("Holley Intermediate") on July 16, 2021, (the "Closing" and such date, the "Closing Date"). The Merger Agreement provided for, among other things, the following transactions: (i) Merger Sub I merged with and into Holley Intermediate, the separate corporate existence of Merger Sub I ceased, and Holley Intermediate became the surviving corporation, and (ii) Holley Intermediate merged with and into Merger Sub II, the separate corporate existence of Holley Intermediate ceased, and Merger Sub II became the surviving limited liability company. On the Closing Date, Empower changed its name to Holley Inc. and its trading symbol on the NYSE from "EMPW" to "HLLY."

Business Strategy

For over 120 years, we have pursued our mission of bringing innovation, discovery and fun to motor life. Today, as Holley Performance Brands, we are a leader in delivering high performance platform solutions, driven to accelerate the passion of auto enthusiasts around the globe. Through our portfolio of leading brands – ranging from icons of the American Road, to emerging technologies – we serve a large, diverse community of expert partners and enthusiast consumers across four distinct consumer verticals: American Performance, Modern Truck & Off-Road, Euro & Import, and Safety & Racing.

We plan to unlock the full potential of Holley's innovation-led research and development ("R&D") product portfolio and brand powerhouse in the performance automotive aftermarket across all four verticals through our highly focused Steering Principles of Fueling our Teammates, Supercharging our Customers and Accelerating Profitable Growth.

• Fueling our teammates : At the heart of our growth strategy lies not just innovation, but the people who drive it. Our first principle is to create a premier place to work that attracts, retains, and empowers talented individuals who share our passion for automotive performance. We aim to achieve this by creating an environment that excites, empowers, and nurtures our teammates to their full

potential by providing them with the resources, knowledge, encouragement, and motivation they need to excel in their roles. This commitment extends beyond traditional employee engagement strategies; it recognizes the critical link between an enthusiast-driven workforce and the development of highly differentiated products that resonate with our target market. By fostering an environment where our teammates' automotive passions thrive, with shared goals, we aim to create a synergy that sparks creative solutions, fuels collaboration, and propels us to new heights.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-16_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-16_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-16_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-03-16_item7_mdna.md, 10-K_2026-03-16_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
