# Triage pack — GIC · GLOBAL INDUSTRIAL Co

_Generated 2026-09-04 13:59 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** GIC · **Name:** GLOBAL INDUSTRIAL Co
- **CIK:** 0000945114
- **SIC:** 5084 — Wholesale-Industrial Machinery & Equipment
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/GIC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** GLOBAL INDUSTRIAL Co
- **CIK:** 945,114 · **SIC:** 5084 (Wholesale-Industrial Machinery & Equipment) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 39.17 |
| mktcap | $1.5B |
| ev | $1.4B |
| ev_ebit | 14.4x |
| fcf | $74.7M |
| fcf_yield | 5.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 30.1% |
| net_debt | -$86.7M |
| net_debt_ebit | -0.9x |
| cash | $86.7M |
| ltd | $0.00 |
| equity | $342.7M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.4B |
| revenue_prior | $1.3B |
| rev_growth | 4.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $97.6M |
| net_income | $72.1M |
| cfo | $77.8M |
| capex | $3.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 38,108,341 |
| shares_py | 38,374,314 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 6.7% |
| r6m | 22.6% |
| off_52w_high | -1.2% |
| adv20 | $4.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.50 |
| r_ev_ebit | 0.61 |
| r_roic | 0.93 |
| r_rev_growth | 0.52 |
| r_buyback | 0.73 |
| score | 0.71 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 57 |

**Screen rationale:** high ROIC 30.1%; debt data missing (net cash unverified); 12-1 momentum 6.7%


## 3. Share count trend

- Shares outstanding: **38,108,341** (CY2026Q2I) vs **38,374,314** prior year (CY2025Q2I)
- Change: **-0.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-07** — Item 1.01 (Entry into a Material Definitive Agreement): On June 30, 2026, Global Industrial Company (the "Company") and certain of its direct and indirect wholly-owned subsidiaries (together with the Company, the "Borrowers") entered into Amendment No. 4 (the "Amendment") to the Third Amended and Restated Credit...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 9,287 sh / $363,908 -> net $-363,908 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 5).

| code | rows |
|---|---|
| F | 7 |
| J | 3 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'GLOBAL INDUSTRIAL REPORTS SECOND QUARTER 2026 FINANCIAL RESULTS'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (gicform99106302026.htm)

GLOBAL INDUSTRIAL REPORTS SECOND QUARTER 2026 FINANCIAL RESULTS

Sales Increased 7.7% to $386.6 Million and 9.3% on an Average Daily Sales Basis

Board Declared $0.28 Dividend

PORT WASHINGTON, NY, August 4, 2026 – Global Industrial Company (NYSE: GIC) , a value-added distributor and source for industrial equipment and supplies today announced financial results for the second quarter ended June 30, 2026.

Performance Summary* (U.S. dollars in millions, except per share data)
Highlights | Quarter Ended June 30, | Six Months Ended June 30,
GAAP Results | 2026 | 2025 | 2026 | 2025
Net sales | $386.6 | $358.9 | $737.0 | $679.9
Gross profit | $155.4 | $133.0 | $277.3 | $245.1
Gross margin | 40.2% | 37.1% | 37.6% | 36.0%
Operating income from continuing operations | $49.3 | $33.5 | $69.9 | $51.7
Operating margin | 12.8% | 9.3% | 9.5% | 7.6%
Net income from continuing operations | $37.1 | $25.1 | $52.4 | $38.6
Net income per diluted share from continuing operations | $0.96 | $0.65 | $1.35 | $0.99
Net income from discontinued operations | $0.0 | $0.0 | $1.3 | $0.1
Net income per diluted share from discontinued operations | $0.00 | $0.00 | $0.03 | $0.00
Non-GAAP Results**
Gross profit | $134.3 | $133.0 | $256.2 | $245.1
Gross margin | 34.7% | 37.1% | 34.8% | 36.0%
Operating income from continuing operations | $28.2 | $33.5 | $48.8 | $51.7
Operating margin | 7.3% | 9.3% | 6.6% | 7.6%
Net income from continuing operations | $20.7 | $25.1 | $36.0 | $38.6
Net income per diluted share from continuing operations | $0.54 | $0.65 | $0.93 | $0.99
* | Global Industrial Company manages its business and reports using a 52-53 week fiscal year that ends at midnight on the Saturday closest to December 31. For clarity of presentation, fiscal years and quarters are described as if they ended on the last day of the respective calendar month. The actual fiscal quarters ended July 4, 2026 and June 28, 2025, respectively. The second quarters of both 2026 and 2025 included 13 weeks and the first six months of both 2026 and 2025 included 26 weeks. Average daily sales is calculated based upon the number of selling days in each period, with Canadian sales converted to U.S. dollars using the current year's average exchange rate. There were 63 selling days in the U.S. in the second quarter of 2026 compared to 64 selling days in the second quarter of 2025 and there were 128 selling days in the U.S. for the six months ended June 30, 2026 and 2025, respectively. There were 63 selling days in Canada in each of the second quarters of 2026 and 2025, respectively, and there were 126 selling days in Canada for the six months ended June 30, 2026 and 2025, respectively.
** | During the second quarter ended June 30, 2026, the Company recorded approximately $26.2 million associated with refunds of IEEPA tariffs previously paid, comprising $21.1 million related to cost of sales, $4.0 million reduction to inventory not yet sold and $1.1 million of interest income. The non-GAAP results above reflect the exclusion of this one-time benefit from gross profit, operating income from continuing operations, net income and earnings per share.

Second Quarter 2026 Financial Summary:

• Consolidated sales increased 7.7% to $386.6 million compared to $358.9 million last year and average daily sales increased 9.3% compared to prior year.

• Consolidated gross margin increased to 40.2% compared to 37.1% last year. Excluding refunds from tariffs, consolidated gross margin would have been 34.7%, in line with historical performance.

• Consolidated operating income from continuing operations increased 47.2% to $49.3 million compared to $33.5 million last year. Excluding refunds from tariffs, consolidated operating income would have been $28.2 million.

• Net income per diluted share from continuing operations increased 47.7% to $0.96 compared to $0.65 last year. Excluding refunds from tariffs, net income per diluted share would have been $0.54.

Year to Date Q2 2026 Financial Summary:

• Consolidated sales increased 8.4% to $737.0 million compared to $679.9 million last year and average daily sales increased 8.4% compared to prior year.

• Consolidated gross margin increased to 37.6% compared to 36.0% last year. Excluding refunds from tariffs, consolidated gross margin would have been 34.8%.

• Consolidated operating income from continuing operations increased 35.2% to $69.9 million compared to $51.7 million last year. Excluding refunds from tariffs, consolidated operating income would have been $48.8 million.

• Net income per diluted share from continuing operations increased 36.4% to $1.35 compared to $0.99 last year. Excluding refunds from tariffs, net income per diluted share would have been $0.93.

Anesa Chaibi, Chief Executive Officer, said, "We delivered another quarter of strong, broad-based growth, with second quarter revenue increasing 7.7%, and 9.3% on an average daily sales basis. This marks our third consecutive quarter of high single-digit average daily sales growth as we benefited from gains in both volume and price."

"We are pleased with the momentum in the business and the progress we are making in advancing our go-to-market approach. We continue to deepen customer relationships, expand e-procurement adoption, strengthen vertical specialization, and enhance coordination across our sales, marketing, merchandising and digital teams. These initiatives are designed to drive sustainable organic growth, increase share of wallet, support continued market-share gains and enhance our long-term performance."

At June 30, 2026, the Company had total working capital of $249.0 million, cash and cash equivalents of $86.7 million, and excess availability under its credit facility of approximately $119.8 million. Operating cash flow provided by continuing operations in the quarter was $41.3 million. During the second quarter ended June 30, 2026, the Company recorded a benefit of approximately $26.2 million associated with refunds of IEEPA tariffs, comprising $21.1 million related to cost of sales, $4.0 million reduction to inventory not yet sold and $1.1 million of interest income. The Company does not expect any future refunds of IEEPA tariffs assessed to date to be material. Quarter end cash balances reflect approximately $15.3 million of tariff refunds received in the fiscal second quarter, with an additional $10.9 million received in early July recorded as a receivable at quarter end. The Company also repurchased approximately 160,000 shares of its common stock at an aggregate purchase price of $4.7 million during the second quarter ended June 30, 2026. The Company's Board of Directors has declared a cash dividend of $0.28 per share to common stock shareholders of record at the close of business on August 17, 2026, payable on August 24, 2026.

Earnings Conference Call Details

Global Industrial Company will host a conference call and question and answer session on its second quarter 2026 results today, August 4, 2026 at 5:00 p.m. Eastern Time. A live webcast of the call will be available on the Company's website at https://investors.globalindustrial.com in the events section. The webcast will also be archived on the website for approximately 90 days.

About Global Industrial Company

Global Industrial Company (NYSE: GIC), is a leading distributor of high-quality, industrial-strength equipment and supplies, serving organizations of all sizes across a wide range of industries. With more than 75 years of experience, customers rely on Global Industrial for its broad portfolio of national and private brands, trusted service and focus on value. We help customers keep their operations running by delivering the right products when they need them, because We Can Supply That ® . Visit Globalindustrial.com, and follow us on Facebook, Instagram, and LinkedIn.

Condensed Consolidated Statements of Operations - Unaudited

(In millions, except per share amounts)

Quarter Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Net sales | 386.6 | 358.9 | 737.0 | 679.9
Cost of sales | 231.2 | 225.9 | 459.7 | 434.8
Gross profit | 155.4 | 133.0 | 277.3 | 245.1
Gross margin | 40.2 | % | 37.1 | % | 37.6 | % | 36.0 | %
Selling, general and administrative expenses | 106.1 | 99.5 | 207.4 | 193.4
Operating income from continuing operations | 49.3 | 33.5 | 69.9 | 51.7
Operating margin | 12.8 | % | 9.3 | % | 9.5 | % | 7.6 | %
Interest and other (income) expense, net | (1.0) | (0.3) | (1.1) | (0.2)
Income from continuing operations before income taxes | 50.3 | 33.8 | 71.0 | 51.9
Provision for income taxes | 13.2 | 8.7 | 18.6 | 13.3
Net income from continuing operations | 37.1 | 25.1 | 52.4 | 38.6
Net income from discontinued operations | 0.0 | 0.0 | 1.3 | 0.1
Net income | 37.1 | 25.1 | 53.7 | 38.7
Net income per common share from continuing operations:
Basic | 0.96 | 0.65 | 1.35 | 1.00
Diluted | 0.96 | 0.65 | 1.35 | 0.99
Net income per common share from discontinued operations:
Basic | 0.00 | 0.00 | 0.03 | 0.00
Diluted | 0.00 | 0.00 | 0.03 | 0.00
Net income per common share:
Basic | 0.96 | 0.65 | 1.38 | 1.00
Diluted | 0.96 | 0.65 | 1.38 | 0.99
Weighted average common and common equivalent shares:
Basic | 38.2 | 38.4 | 38.2 | 38.4
Diluted | 38.2 | 38.4 | 38.3 | 38.4

GLOBAL INDUSTRIAL COMPANY

Condensed Consolidated Balance Sheets - Unaudited

(In millions)

June 30, | December 31,
2026 | 2025
Current assets:
Cash and cash equivalents | 86.7 | 67.5
Accounts receivable, net | 186.8 | 139.6
Inventories | 163.6 | 174.6
Prepaid expenses and other current assets | 12.2 | 14.8
Total current assets | 449.3 | 396.5
Property, plant and equipment, net | 17.8 | 18.5
Operating lease right-of-use assets | 88.7 | 91.8
Goodwill and intangibles | 62.7 | 64.3
Other assets | 9.9 | 9.7
Total assets | 628.4 | 580.8
Current liabilities:
Accounts payable and accrued expenses | 185.9 | 162.4
Operating lease liabilities | 14.4 | 16.1
Total current liabilities | 200.3 | 178.5
Operating lease liabilities | 84.5 | 87.5
Other liabilities | 0.9 | 1.6
Shareholders' equity | 342.7 | 313.2
Total liabilities and shareholders' equity | 628.4 | 580.8

GLOBAL INDUSTRIAL COMPANY

Condensed Consolidated Statements of Cash Flows - Unaudited

(In millions)

Six Months Ended June 30,
2026 | 2025
CASH FLOWS FROM OPERATING ACTIVITIES:
Net income from continuing operations | 52.4 | 38.6
Adjustments to reconcile net income from continuing operations to net cash provided by (used in) operating activities:
Depreciation and amortization | 3.9 | 3.8
Stock-based compensation | 3.1 | 3.7
Provision for deferred taxes | (0.1) | (0.3)
Change in working capital | (14.5) | (11.3)
Other, net | 1.2 | 0.6
Net cash provided by operating activities from continuing operations | 46.0 | 35.1
Net cash provided by operating activities from discontinued operations | 1.8 | 0.0
Net cash provided by operating activities | 47.8 | 35.1
CASH FLOWS FROM INVESTING ACTIVITIES:
Purchases of property, plant and equipment | (1.7) | (1.6)
Acquisition, net of cash acquired | 0.0 | (4.0)
Net cash used in investing activities | (1.7) | (5.6)
CASH FLOWS FROM FINANCING ACTIVITIES:
Dividends paid | (21.6) | (20.1)
Stock-based compensation share issuances, net | 0.4 | 1.2
Purchase of treasury shares | (5.6) | 0.0
Net cash used in financing activities | (26.8) | (18.9)
EFFECT OF EXCHANGE RATE CHANGES ON CASH | (0.1) | (0.1)
NET INCREASE IN CASH | 19.2 | 10.5
CASH AND CASH EQUIVALENTS – BEGINNING OF PERIOD | 67.5 | 44.6
CASH AND CASH EQUIVALENTS – END OF PERIOD | 86.7 | 55.1

GLOBAL INDUSTRIAL COMPANY

Reconciliation of GAAP to Non-GAAP Measures - Unaudited

(In millions)

The following tables reconciles GAAP operating results to Non-GAAP operating results for the quarter ended June 30, 2026.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-27_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Global Industrial Company, through its subsidiaries, is a value-added distributor and source for industrial equipment and supplies in North America going to market through a system of branded e-commerce websites and relationship marketers.

In April 2025, the Company completed the acquisition of an equipment service provider for approximately $4.3 million in cash. At closing, $0.3 million was held in escrow for settlement of potential obligations. The accounts acquired are included in the accompanying consolidated financial statements from the date of acquisition. This acquisition broadens the Company's value-added offerings in certain key equipment categories.

The Company acquired 100% of the outstanding equity interests of Indoff, a business-to-business direct marketer of material handling products, commercial interiors and business products with operations in North America, on May 19, 2023 for approximately $72.6 million in cash. The Indoff accounts are included in the accompanying consolidated financial statements from the date of acquisition. This acquisition expands the Company's presence in the maintenance, repair and operations ("MRO") market in North America.

See Note 4, Acquisition, of Notes to Consolidated Financial Statements for additional financial information regarding these acquisitions.

Continuing Operations

The Company specializes in providing maintenance, repair and operations solutions to businesses ranging from small to enterprise, and to the public sector. The Company is committed to its customer-centric strategy and uses industry expertise, products from its own Global Industrial Exclusive Brands TM , and nationally known brands to provide customers with a breadth of offerings to meet their needs. These industrial and MRO products are manufactured by other companies. Some products are manufactured for us and sold as a white label product, and some are manufactured to our own design and marketed as private brand products under the trademarks: Global™, GlobalIndustrial.com™, Nexel™, Paramount™, Interion™ and Absocold™.

Operating Conditions

The market for the sale of industrial products in North America is highly fragmented and is characterized by multiple distribution channels. Industrial products distribution is working capital intensive, requiring us to incur significant costs associated with the warehousing of many products, including the costs of maintaining inventory, leasing warehouse space, inventory management systems and employing personnel to perform the associated tasks. We supplement our on-hand product availability by maintaining relationships with major distributors and manufacturers, utilizing a combination of stock and drop-shipment fulfillment.

The primary component of our operating expenses historically has been employee-related costs, which includes items such as wages, commissions, bonuses, employee benefits and equity-based compensation, as well as marketing expenses, primarily comprised of digital marketing spend, and occupancy related charges associated with our leased distribution and call center facilities. We continually assess our operations to ensure that they are efficient, aligned with market conditions and responsive to customer needs.

The discussion of our results of operations and financial condition that follows will provide information that will assist in understanding our financial statements, the factors that we believe may affect our future results and financial condition as well as information about how certain accounting policies and estimates affect the consolidated financial statements.

The Company has elected to omit discussion of the earliest year presented, December 31, 2023, in MD&A. This discussion can be found in Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations in Form 10-K for the year ended December 31, 2024, filed on February 26, 2025.

Business Outlook

2025 was a year of solid execution and significant progress for Global Industrial, with revenue growing 4.8% to $1.38 billion. We delivered strong margin performance, generated healthy cash flows and we continue to make progress on our strategic initiatives, which we believe will enable us to drive profitable top-line growth and scale the business in 2026 and beyond. This includes transforming our business model to become a more customer-centric organization along with reframing our go-to-market strategy to more effectively address our customer's needs.

Highlights from 2025 vs. 2024

The following discussion of our results of operations and financial condition will provide information that will assist in understanding our financial statements and information about how certain accounting principles and estimates affect the consolidated financial statements. This discussion should be read in conjunction with the consolidated financial statements included herein.

• Consolidated sales increased 4.8% to $1.38 billion in U.S. dollars compared to $1.32 billion last year and average daily sales increased 3.2% compared to prior year.

• Consolidated gross margin increased to 35.5 % compared to 34.3% last year.

• Consolidated operating income from continuing operations increased 21.2% to $97.6 million compared to $80.5 million last year.

• Net income per diluted share from continuing operations increased 17.8% to $1.85 compared to $1.57 last year.

*Average daily sales is calculated based upon the number of selling days in each period, with Canadian sales converted to U.S. dollars using the current year's average exchange rate. There were 257 selling days in the U.S. in 2025 compared to 253 selling days in 2024 and in Canada, there were 254 selling days in 2025 compared to 250 selling days in 2024.

Results of Operations (1)

Key Performance Indicators (in millions):

Years Ended December 31, | Change
2025 | 2024 | 2025 vs. 2024
Results of continuing operations:
Consolidated net sales | 1,379.1 | 1,315.9 | 4.8 | %
Consolidated gross profit | 490.2 | 452.0 | 8.5 | %
Consolidated gross margin | 35.5 | % | 34.3 | % | 1.2 | %
Consolidated SD&A costs | 392.6 | 371.5 | 5.7 | %
Consolidated SD&A costs as % of sales | 28.5 | % | 28.2 | % | 0.3 | %
Consolidated operating income | 97.6 | 80.5 | 21.2 | %
Consolidated operating margin from continuing operations: | 7.1 | % | 6.1 | % | 1.0 | %
Effective income tax rate | 26.2 | % | 23.9 | % | 2.3 | %
Net income from continuing operations | 72.0 | 60.7 | 18.6 | %
Net margin from continuing operations | 5.2 | % | 4.6 | % | 0.6 | %
Net income from discontinued operations, net of tax | 0.1 | 0.3 | NM

NM=not meaningful

1 | Global Industrial Company manages its business and reports using a 52-53 week fiscal year that ends at midnight on the Saturday closest to December 31. For clarity of presentation, fiscal years are described as if they ended on the last day of the respective calendar month. Fiscal years 2025 and 2024 ended on January 3, 2026 and December 28, 2024, respectively. The fiscal year ended 2025 included 53 weeks and 2024 included 52 weeks.

Management's discussion and analysis that follows includes current operations.

NET SALES

The Company's net sales increased 4.8% to $1.38 billion compared to $1.32 billion in 2024, benefiting from price capture, strong sales from our largest strategic accounts and volume improvement in the second half of the year, partially offset by a reduction in our smaller and transactional customer sales. U.S. sales increased 4.7% in 2025 compared to 2024 and Canada sales increased 7.0%, 9.2% in local currency in 2025 compared to 2024.

There were 257 selling days in the U.S. in 2025 compared to 253 in 2024 and 254 selling days in Canada in 2025 compared to 250 selling days in 2024.

GROSS MARGIN

Gross margin is dependent on variables such as product mix including sourcing and category, trade policy inclusive of the imposition of tariffs, competition, pricing strategy, vendor volume rebates, freight pricing decisions including the use of free or other promotional freight plans, freight cost inflation including both domestic outbound freight as well as international inbound ocean freight, inventory valuation and obsolescence and other variables, any or all of which may result in fluctuations in gross margin.

Gross margin was 35.5% compared to 34.3% in the prior year, a 120 basis point improvement. The year over year improvement resulted strategic pricing management including the timing benefit from pre-tariff inventory flowing through cost of sales and overall freight management, including both inbound and outbound logistics as well as quality initiatives that reduced freight claims and customer returns. In the prior year, the Company's margin reflected modest price actions taken throughout the year to offset both the increased costs of inbound ocean transportation, as well as, higher parcel fulfillment costs.

Management of our margin profile remains a key area of focus for the Company. Performance will continue to reflect the impact of strategic promotion and freight actions as part of our competitive pricing initiatives, tariff related actions and ocean freight costs. The Company continues to anticipate that there may be increased margin variability in future periods given the timing dynamics of on-hand inventory, inflationary pressures associated with tariff related cost increases and our efforts to continue to diversify our supply chain as well as historical seasonality.

SELLING, GENERAL, AND ADMINISTRATIVE EXPENSES ("SG&A")

Selling, general and administrative expenses totaled $392.6 million and $371.5 million for the years ended December 31, 2025 and 2024, respectively.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-27_item1_business.md)

Item 1. Business.

General

Global Industrial Company, through its operating subsidiaries, is a value-added distributor of industrial equipment and source for industrial equipment and supplies in North America going to market through a system of branded e-commerce websites and relationship marketers. The Company was incorporated in Delaware in 1995. Certain predecessor businesses which now constitute the Company's operations have been in business since 1949. Our headquarters office is located at 11 Harbor Park Drive, Port Washington, New York.

Continuing operations

The Company sells a wide array of industrial and maintenance, repair and operation ("MRO") products, including its own Global Industrial Exclusive Brands TM , which are marketed in North America. These industrial and MRO products are manufactured by other companies. Some products are manufactured for us and sold as a white label product, and some are manufactured to our own design and marketed as private brand products under the trademarks: Global™, GlobalIndustrial.com™, Nexel™, Paramount™, Interion™ and Absocold™.

On April 28, 2025, the Company completed the acquisition of an equipment service provider for approximately $4.3 million in cash. This acquisition broadens the Company's value-added offerings in certain key equipment categories.

On May 19, 2023 the Company acquired 100% of the outstanding equity interests of Indoff LLC ("Indoff"), a business-to-business direct marketer of material handling products, commercial interiors and business products with operations in North America, for approximately $72.6 million in cash. This acquisition expanded the Company's presence in the MRO market in North America.

See Note 4, Acquisitions, and Note 6, Revenue, of Notes to Consolidated Financial Statements included in Item 15 of this Form 10-K for additional financial information about our business, recent acquisitions as well as information about our geographic operations.

Customer Focused Strategy

The Company's evolving go to market strategy is focused on customer centricity and ensuring alignment of our actions with the specific needs of our customer base. In order to achieve this we have realigned our sales force to be targeted to specific customer end market verticals, and creating an enhanced collaboration within our Sales, Marketing, and Merchandising organizations to best service these customers. This renewed focus guides our actions across the business, and specifically in our customer end-to-end purchase, service, and delivery experience, has at its core building of customer loyalty and trust by addressing unique customer needs through a responsive and tailored sales, product, and service experience. We build customer loyalty and trust through personalized and high touch customer interactions that often feature strong one to one relationships. The Company's digital and multi-channel sales model drives customer acquisition and with rigorous vetting we are able to identify opportunities for product category expansion, with a renewed focus on Maintenance, Repair, and Consumable products. Category expansion with our customers drives repeat orders and increases their annual and average spend. We maximize customer satisfaction and loyalty by coupling close customer relationships with product expertise, efficient and competitive fulfillment and delivery and exceptional customer service.

WE CAN SUPPLY THAT ®

Products

Our broad product offering and focus on responsiveness to our customers is captured in our promise " We Can Supply That ® ". We offer our customers a competitive assortment of leading products and services, a sales force with deep product knowledge and expertise, and timely and relative industry and product content via The Knowledge Center . Our go to market strategy also focuses on leveraging our deep product knowledge and experience by offering our customers a broad and deep product selection from leading and specialty national brands, as well as, seeking to expand our higher margin private brand line of Global products by adding additional products and product categories. We offer hundreds of thousands of brand name and private brand products available through our e-commerce sites and have access to many more additional long tail products from

our network of vendor partners. We endeavor to expand and keep current the breadth of our product offerings to fulfill the increasingly wide range of product needs of our customers, and periodically remove certain products from our offering to improve efficiencies or to address vendor or market changes. Sourcing hard to find or non-standard product helps to differentiate our business from our competitors and we believe provides us with a competitive advantage.

The Company has focused on offering competitive pricing, high service levels, broad and deep product offering, extensive product and sales expertise, and most importantly a private brand offering that provides high quality with an attractive price point. Products generally are categorized within the following categories: storage and shelving, safety and security, carts and trucks, HVAC and fans, furniture and decor, material handling, janitorial and facility maintenance, workbenches and shop desks, tools and instruments, plumbing and pumps, office and school supplies, packaging and shipping, lighting and electrical, foodservice and retail, medical and laboratory, motors and power transmission, building supplies, machining, fasteners and hardware, vehicle maintenance, and raw materials. We have become a destination and trusted supplier of these products and continue to evaluate expansion within key end markets.

Sales and Marketing

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-27_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-27_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-27_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-02-27_item7_mdna.md, 10-K_2026-02-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
