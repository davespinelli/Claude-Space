# Triage pack — ACU · ACME UNITED CORP

_Generated 2026-09-04 18:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ACU · **Name:** ACME UNITED CORP
- **CIK:** 0000002098
- **SIC:** 3420 — Cutlery, Handtools & General Hardware
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ACU

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ACME UNITED CORP
- **CIK:** 2,098 · **SIC:** 3420 (Cutlery, Handtools & General Hardware) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 63.15 |
| mktcap | $242.1M |
| ev | $259.7M |
| ev_ebit | 17.6x |
| fcf | $7.6M |
| fcf_yield | 3.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 8.4% |
| net_debt | $17.6M |
| net_debt_ebit | 1.2x |
| cash | $5.0M |
| ltd | $22.6M |
| equity | $121.3M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $196.5M |
| revenue_prior | $194.5M |
| rev_growth | 1.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $14.7M |
| net_income | $10.2M |
| cfo | $18.2M |
| capex | $10.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 3,833,823 |
| shares_py | 3,799,252 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 32.8% |
| r6m | 46.0% |
| off_52w_high | -1.0% |
| adv20 | $2.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.38 |
| r_ev_ebit | 0.51 |
| r_roic | 0.66 |
| r_rev_growth | 0.38 |
| r_buyback | 0.48 |
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
| rank | 216 |

**Screen rationale:** 12-1 momentum 32.8%


## 3. Share count trend

- Shares outstanding: **3,833,823** (CY2026Q2I) vs **3,799,252** prior year (CY2025Q2I)
- Change: **0.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-21** — Item 1.01 (ENTRY INTO A MATERIAL DEFINITIVE AGREEMENT): On July 15, 2026 Acme United Corporation (the "Company") entered into a new $65 million syndicated credit facility with HSBC Bank USA, National Association.
- **2026-07-21** — Item 1.02 (TERMINATION OF A MATERIAL DEFINITIVE AGREEMENT): The information set forth under Item 1.01 of this Current Report on Form 8-K is incorporated herein by reference.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 25,722 sh / $1,505,004 -> net $-1,505,004 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 29 (open-market buys 0, sales 11).

| code | rows |
|---|---|
| A | 6 |
| F | 4 |
| M | 8 |
| S | 11 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-23_2-02-results.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit; skipped 9 forward-looking-statement block(s)._

## EX-99.1 - EX-99.1 (acu-ex99_1.htm)

EX-99.1
acu-ex99_1.htm
EX-99.1

EX-99.1

Ex 99.1

ACME UNITED CORPORATION NEWS RELEASE

CONTACT: Paul G. Driscoll Acme United Corporation 1 Waterview Drive Shelton, CT 06484

Phone: (203) 254-6060

FOR IMMEDIATE RELEASE July 23, 2026

ACME UNITED REPORTS SECOND QUARTER 2026 NET SALES INCREASE OF

16% AND NET INCOME INCREASE OF 6%

SHELTON, CT – July 23, 2026 – Acme United Corporation (NYSE American: ACU) today announced that net sales for the quarter ended June 30, 2026 were $62.7 million compared to $54.0 million for the quarter ended June 30, 2025, an increase of 16%. Excluding sales resulting from the acquisition of the assets of My Medic on January 15, 2026, comparable three-month sales increased 8%. Net sales for the six months ended June 30, 2026 were $115.0 million, compared to $100.0 million in the same period in 2025, an increase of 15%. Excluding My Medic sales, comparable six-month sales increased 7%.

Net income was $5.1 million, or $1.22 per diluted share, for the quarter ended June 30, 2026, compared to $4.8 million, or $1.16 per diluted share, for the same period last year, an increase of 6% in net income and 5% in diluted earnings per share. Net income for the six months ended June 30, 2026 was $6.0 million, or $1.46 per diluted share, compared to $6.4 million, or $1.57 per diluted share, for the same period in 2025, a decrease of 6% in net income and 7% in diluted earnings per share, caused primarily by our first quarter results.

The My Medic business acquired in January, which sells tactical, trauma and emergency response products directly to consumers, contributed to sales growth but due to the seasonal nature of the My Medic business there was minimal impact on earnings in the second quarter and the first half of 2026. As a direct-to-consumer seasonal business, My Medic has historically generated the majority of its profitability in the fourth quarter and we expect this pattern to continue.

Chairman and CEO, Walter C. Johnsen said, "In the second quarter we had record revenues and income from operations as we drove growth across all geographies and product lines. In the U.S. net sales of our first aid business without My Medic's

Ex 99.1

contribution increased 10% in the quarter. Net sales of Westcott cutting tools grew 8% in the second quarter, an important improvement over last year due to a return of promotional activity and stronger retail demand.

Mr. Johnsen continued, "As we anticipated, gross margins in the U.S. business were affected by products purchased at elevated tariff levels, though the impact was less than in the first quarter. We expect prior high tariffs to continue pressuring margins in the coming quarters, but at a decreasing rate."

Mr. Johnsen concluded, "The My Medic acquisition is progressing well. We are aggressively presenting its products to new potential industrial and retail customers, as well as leveraging our sourcing team and scale to improve product costs. We have also reduced overhead. These actions, taken together, are designed to deliver strengthening quarterly profitability by driving growth on a lower cost base. It will take time, but we are making progress."

For the second quarter of 2026, net sales in the U.S. segment increased 17% compared to the same period in 2025. For the six months ended June 30, 2026, net sales in the U.S. segment increased 15% compared to the same period in 2025. The sales increases for the three and six months were due to strong sales across all product lines and contribution from the acquisition of the My Medic business.

European net sales for the second quarter of 2026 increased 24% in U.S. dollars and 19% in local currency compared to the second quarter of 2025. Net sales for the six months ended June 30, 2026 increased 28% in U.S. dollars and 19% in local currency compared to the same period of 2025. The sales increases for the three and six months were due primarily to higher ecommerce sales and contribution from the line of cutting and sharpening products acquired in Germany on October 1, 2025.

Net sales in Canada for the second quarter of 2026 increased 1% in U.S. dollars and 3% in local currency compared to the same period in 2025. Net sales for the six months ended June 30, 2026 increased 7% in U.S. dollars and 6% in local currency compared to the same

Ex 99.1

period of 2025. The sales increases for the three and six months were due to higher sales of first aid products.

Gross margin was 42.6% in the second quarter of 2026 versus 41.0% in the comparable period last year. Gross margin was 41.3% for the six-month period ended June 30, 2026, compared to 40.1% for the same period in 2025. The increases for the three and six months were primarily due to the inclusion of the new My Medic direct to consumer business.

The Company's bank debt less cash as of June 30, 2026 was $27.3 million compared to $22.8 million as of June 30, 2025. During the twelve-month period ended June 30, 2026, the Company paid approximately $14.5 million for the acquisition of the assets of My Medic ($18.6 million purchase price less $4.1 million of holdbacks), distributed approximately $2.4 million in dividends on its common stock and purchased the cutting and sharpening line of products in Germany for approximately $1.6 million. During the same period, the Company generated approximately $15.5 million in free cash flow.

On July 15, 2026, the Company entered into a new $65 million syndicated credit facility with HSBC Bank USA, N.A and City National Bank, a U.S. subsidiary of Royal Bank of Canada. The new facility, which replaces the Company's prior $65 million credit facility with HSBC, expires on July 15, 2029.

Conference Call and Webcast Information

Acme United will hold a conference call to discuss its quarterly results, which will be broadcast on Thursday, July 23, 2026, at 12:00 p.m. ET. To listen or participate in a question-and-answer session, dial 877-407-0784 . International callers may dial 201-689-8560. The confirmation code is 13761594. You may access the live webcast of the conference call through the Investor Relations section of the Company's website, www.acmeunited.com . A replay may be accessed under Investor Relations, Audio Archives.

About Acme United

Ex 99.1

ACME UNITED CORPORATION is a leading worldwide supplier of innovative safety solutions and cutting technology to the school, home, office, hardware, sporting goods and industrial markets. Its leading brands include First Aid Only ®, First Aid Central ®, Physicians Care ®, Pac-Kit®, Spill Magic ®, Westcott ®, Clauss ®, DMT ®, Med-Nap ®, Elite First Aid ® and My Medic ® . For more information, visit www.acmeunited.com .

Ex 99.1

ACME UNITED CORPORATION
CONDENSED CONSOLIDATED STATEMENTS OF INCOME
SECOND QUARTER REPORT 2026
(Unaudited)
Six Months Ended | Six Months Ended
Amounts in 000's except per share data | June 30, 2026 | June 30, 2025
Net sales | 115,017 | 99,954
Cost of goods sold | 67,544 | 59,888
Gross profit | 47,473 | 40,066
Selling, general and administrative expenses | 38,899 | 31,250
Operating income | 8,574 | 8,816
Net interest expense | 1,018 | 798
Other expense (income), net | 11 | (188
Income before income tax expense | 7,545 | 8,206
Income tax expense | 1,511 | 1,802
Net income | 6,034 | 6,404
Shares outstanding - basic | 3,815 | 3,772
Shares outstanding - diluted | 4,138 | 4,070
Earnings per share - basic | 1.58 | 1.70
Earnings per share - diluted | 1.46 | 1.57

Ex 99.1

ACME UNITED CORPORATION
CONDENSED CONSOLIDATED BALANCE SHEETS
SECOND QUARTER REPORT 2026
(Unaudited)
Amounts in $000's
June 30, 2026 | June 30, 2025
Assets
Current assets:
Cash and cash equivalents | 5,041 | 3,641
Accounts receivable, net | 38,726 | 36,174
Inventories | 64,099 | 57,309
Prepaid expenses and other current assets | 4,465 | 4,217
Total current assets | 112,331 | 101,341
Property, plant and equipment, net | 39,217 | 32,901
Operating lease right of use asset | 6,001 | 7,607
Intangible assets, less accumulated amortization | 33,188 | 19,111
Goodwill | 9,908 | 9,908
Total assets | 200,645 | 170,868
Liabilities and stockholders' equity
Current liabilities:
Accounts payable | 14,151 | 10,181
Operating lease liability - short term | 1,330 | 1,525
Mortgage payable - short term | 463 | 445
Other current liabilities | 18,870 | 11,323
Total current liabilities | 34,814 | 23,474
Long-term debt | 22,637 | 16,352
Mortgage payable - long term | 9,229 | 9,662
Operating lease liability - long term | 4,821 | 6,177
Deferred income taxes | 3,685 | 1,465
Other non-current liabilities | 4,157 | 16
Total liabilities | 79,343 | 57,146
Total stockholders' equity | 121,302 | 113,722
Total liabilities and stockholders' equity | 200,645 | 170,868

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-11_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations 2025 Compared with 2024

Traditionally, the Company's sales and profits are stronger in the second and third quarters and weaker in the first and fourth quarters of the fiscal year, due to the seasonal nature of the Westcott back-to-school market.

Net Sales

In 2025, sales increased by $2,051,825, or 1%, to $196,541,816 compared to $194,489,991 in 2024.

The U.S. segment sales decline by 1% in 2025 compared to 2024. Sales of first aid and medical products were strong. However, sales of school and office products were lower mainly due to the cancellation of customer orders in the third and fourth quarters as a result of tariff uncertainty.

European net sales for the year ended December 31, 2025, increased 8% in U.S. dollars (4% in local currency), compared with the same period in 2024. On October 1, 2025, the Company's German subsidiary acquired a line of cutting and sharpening tools that contributed $0.5 million in sales during the year ended December 31, 2025.

Net sales in Canada for the year ended December 31, 2025, increased 14% in U.S. dollars (16% in local currency) compared to the same period in 2024. The increase in sales for the year ended December 31, 2025 was due to strong sales of first aid products.

Gross Profit

Gross profit was $77,409,848 (39.4% of net sales) in 2025 compared to $76,350,824 (39.3% of net sales) in 2024.

Selling, General and Administrative

Selling, general and administrative ("SG&A") expenses were $62,685,334 in 2025 compared with $62,210,882 in 2024, an increase of $474,452, or 0.8%. SG&A expenses were 31.9% of net sales in 2025 compared to 32.0% in 2024.

Operating Income

Operating income was $14,724,514 in 2025 compared with $14,139,942 in 2024, an increase of $584,572.

Operating income in the U.S. segment increased in 2025 by approximately $117,000 compared to 2024.

Operating income in the European segment increased in 2025 by $143,000 compared to 2024. The increase in operating income was primarily due to higher sales as well as improved gross margins.

Operating income in Canada increased in 2025 by approximately $326,000 compared to 2024. The increase in operating income was primarily due to higher sales as well as improved gross margins.

Interest Expense, net

Net interest expense for 2025 was $1,559,920 compared with $1,942,643 for 2024, a decrease of $382,723. The decrease in net interest expense resulted from lower average outstanding borrowings as well as lower average interest rates on the debt outstanding.

Total Other (Expense) Income, net

Total other (expense), net was $46,972 in 2025 compared to other income, net of $95,110 in 2024. The change in total other expense, net was primarily related to higher losses from foreign currency transactions.

Income Tax Expense

Income tax expense was $2,933,201 in 2025, resulting in an effective tax rate of 22% compared to $2,270,058 in 2024, an effective tax rate of 18%. In 2025, the Company recorded a tax credit of approximately $300,000 related to employee exercise of stock options, compared to $600,000 in 2024.

Off-Balance Sheet Transactions

The Company did not engage in any off-balance sheet transactions during 2025.

Liquidity and Capital Resources

During 2025, working capital increased by approximately $0.7 million compared to December 31, 2024. Inventory increased by approximately $3.6 million, or 6%. Inventory turnover, calculated using a twelve-month average inventory balance, was 2.1 at December 31, 2025 as compared to 2.1 at December 31, 2024. The reserve for slow moving and obsolete inventory was $1,477,849 at December 31, 2025 compared to $1,254,121 at December 31, 2024. We do not anticipate material increases in the allowance for slow moving and obsolete inventory in the ordinary course of business during 2026. Receivables increased by approximately $0.9 million at December 31, 2025 compared to December 31, 2024. The average number of days sales outstanding in accounts receivable was 55 days in 2025 compared to 54 days in 2024.

Long-term debt consists of (i) borrowings under the Company's revolving loan agreement with HSBC Bank, N.A. and (ii) amounts outstanding under the fixed rate mortgage on the Company's manufacturing and distribution facilities in Rocky Mount, NC and Vancouver, WA. Effective as of June 26, 2025, Acme United Corporation (the "Company") entered into Amendment No. 11 to the Revolving Loan Agreement dated as of April 5, 2012, as amended (the "Loan Agreement"), between the Company and HSBC Bank, N.A. Amendment No. 11 extends the scheduled maturity of the $65 million dollar secured revolving credit facility under the Loan Agreement to May 31, 2027. The revolving loan agreement provides for borrowings of up to $65 million, which presently bears interest at SOFR plus 1.70%; interest is payable monthly. The loan agreement has an expiration date of May 31, 2027. The Company must pay a facility fee, payable quarterly, in an amount equal to one eighth of one percent (.125%) per annum of the average daily unused portion of the revolving credit line. The facility is intended to provide liquidity for growth, share repurchases, dividends, acquisitions, and other business activities. Under the revolving loan agreement, the Company is required to maintain specific amounts of funded debt to EBITDA, a fixed charge coverage ratio and must have annual net income greater than $0, measured as of the end of each fiscal year. As of December 31, 2025, the Company was in compliance with the covenants under the revolving loan agreement as then in effect.

At December 31, 2025, total debt outstanding under the Company's revolving credit facility decreased by approximately $5.8 million compared to total debt outstanding at December 31, 2024. As of December 31, 2025, $11,863,085 was outstanding, and $53,136,915 was available for borrowing under the Company's revolving credit facility.

On July 15, 2025, the Company purchased a manufacturing and distribution center in Mt. Pleasant, TN for approximately $6.0 million using funds available under its revolving credit facility. The property consists of 77,000 square feet of manufacturing and warehouse space on 12 acres and is designed to be expanded by up to an additional 60,000 square feet. The facility will primarily be used to manufacture our Spill Magic line of bodily fluid and spill clean up solutions.

The Company's manufacturing and distribution facilities in Rocky Mount, NC and Vancouver, WA were financed by a fixed rate mortgage with HSBC Bank, N.A. at a fixed interest rate of 3.8%. The Company entered into the agreement on December 1, 2021. Payments of principal and interest are due monthly, with all amounts outstanding due on maturity on December 1, 2031. The outstanding principal on December 31, 2025, was $9,975,587.

On May 23, 2024, the Company acquired the assets of Elite First Aid, Inc ("Elite First Aid") for approximately $7.1 million of which $1.0 million is subject to holdbacks as follows: (a) $500,000, the payment of which is contingent upon certain revenue milestones during an consecutive 12-month period from May 31, 2024 to December 31, 2025. The acquired business did not meet the required milestones within the allowable period; therefore, the contingent amount was not payable. Accordingly, the Company reversed the related $500,000 liability.

An additional holdback of (b) $500,000, was subject to a 13 month holdback as a non-exclusive source of recovery primarily to satisfy certain types of indemnification claims under the Asset Purchase Agreement; the Company paid this amount in July 2025.

Capital expenditures during 2025 and 2024 were $10,651,913 and $7,148,648, respectively, which were, in part, financed with borrowings under the Company's revolving credit facility. The increase in capital expenditures is primarily related to the purchase of the manufacturing facility in Mt. Pleasant, TN as discussed above.

The Company believes that cash on hand, and cash generated from operating activities, together with funds available under its revolving credit facility, are expected, under current conditions, to be sufficient to finance the Company's planned operations for at least the next twelve months from the issuance of this Form 10-K.

Recently Issued Accounting Standards

Standards not yet Adopted

In November 2024, the Financial Accounting Standards Board (FASB) issued Accounting Standards Update (ASU) 2024-03, Income Statement – Reporting Comprehensive Income – Expense Disaggregation Disclosures (Subtopic 220-40): Disaggregation of Income Statement Expenses. This ASU requires more detailed information about specified categories of expenses (purchases of inventory, employee compensation, depreciation, intangible asset amortization and depletion) included in certain expense captions presented on the face of the income statement. The ASU is effective for fiscal years beginning after December 15, 2026 and for interim periods beginning after December 15, 2027. The ASU may be applied either prospectively to financial statements issued for reporting periods after the effective date of this ASU or retrospectively to all prior periods presented in the financial statements and early adoption is permitted. The Company is currently evaluating the impact of adopting this ASU on our consolidated financial statements and related disclosures.

Standards Adopted

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-11_item1_business.md)

Item 1. B usiness

Overview

Acme United Corporation, a Connecticut corporation (together, with its subsidiaries, the "Company"), is a leading worldwide supplier of innovative first aid and medical products and cutting technology to the school, home, office, hardware, sporting goods and industrial markets. Its principal products sold across all segments are first aid kits and medical products, scissors, shears, knives, and sharpening tools. The Company sells its products primarily to mass market and e-commerce retailers, industrial distributors, wholesale, contract and retail stationery distributors, office supply superstores, sporting goods stores, and hardware chains.

The Company's operations are in the United States, Canada, Europe (located in Germany) and Asia (located in Hong Kong and China). The operations in the United States, Canada and Europe are primarily involved in product development, marketing, sales, administrative, manufacturing and distribution activities. The operations in Asia consist of sourcing, product development, production planning, quality control and sales activities. Total net sales in 2025 were $196.5 million. The Company was organized as a partnership in l867 and incorporated in l882 under the laws of the State of Connecticut.

The Company sources most of its products from suppliers located outside the United States, primarily in Asia. In recent years, as a result of acquisitions, the amount of first aid and medical products produced in North America has been increasing substantially. The components for first aid kits are sourced from both U.S. and international suppliers. The Company assembles its first aid kits at its facilities in the following locations:

•
Vancouver, WA,

•
Rocky Mount, NC,

•
Keene, NH

•
Laval, Canada

The Company has additional manufacturing facilities in the U.S. as follows:

•
La Vergne, TN - Spill Magic products

•
Santa Ana, CA - Spill Magic products

•
Marlborough, MA - DMT sharpening tools

•
Brooksville, FL - Med-Nap alcohol and benzalkonium chloride non-alcohol (BZK) wipes.

Recent Accomplishments and Initiatives

Quantitative Achievements

In 2025, the Company's key financial accomplishments included the following:

•
Sales Growth – Average annual growth rate over eleven years of 7%.

•
Strong Financial Position – In recent years the Company has significantly reduced bank debt to provide at December 31, 2025, approximately $53 million of availability under its $65 million credit facility. This strong liquidity will allow the Company to fund acquisitions and growth.

•
Dividend Increase - Increase in the quarterly dividend from $.02 per share in 2004 to $.16 per share in 2025 – an eight-fold increase.

Business and Operational Milestones and Achievements

•
Diversification of Product Lines – During the past nine years, sales of first aid and medical products have grown to approximately 66% of total sales. As a result, we have broadened our customer and revenue base.

•
Cutting Acquisition – On October 1, 2025, the Company acquired a line of cutting and sharpening tools in Germany with annual revenue of approximately $2 million.

•
First Aid Acquisition – In 2025, the Company successfully negotiated the acquisition of the assets of My Medic. The transaction closed on January 15, 2026. My Medic is a leading supplier of tactical, trauma and emergency response products with annual revenue of approximately $19 million.

•
Product Innovation – In 2025, we introduced new first aid bar code scanning technology that expedites replenishment, ensuring OSHA compliance.

•
Cost Reduction Initiatives – In 2025, the Company invested in robotics in three of its manufacturing and distribution facilities which has already improved productivity. Additionally, the Company invested in equipment to automate its Spill Magic powder manufacturing process; the project is expected to be completed in 2026.

•
Capacity Expansion - In 2025, the Company purchased a 77,000 square foot manufacturing and distribution center in Mt. Pleasant, Tennessee for its growing Spill Magic absorbent business .

Principal Products

The Company markets and sells under two main product categories: i) first aid and medical; and ii) cutting and sharpening. The first aid and medical category includes first aid and safety products (First Aid Only®, PhysiciansCare®, Pac-Kit®, Spill Magic®, First Aid Central®, Med-Nap, Safety Made, Elite and My Medic brands). The cutting and sharpening categories include school, home and office products (Westcott® brand), and hardware, industrial and sporting goods products (Clauss® and DMT® brands).

FIRST AID AND MEDICAL

First Aid Only

The First Aid Only brand offers first aid and medical products that meet regulatory requirements for a broad range of industries. The Smart Compliance® first aid system is an effective solution for maintaining compliance with the American National Standards Institute (ANSI) standards. The Company's SafetyHub App technology digitizes the replenishment process for a broad range of first aid components and provides data analytics to manage costs. Our next generation SmartCompliance Complete™ offers a modular system that addresses first aid, bloodborne pathogen, bleed control, eyewash and OTC medication requirements for the most challenging workplace environments.

PhysiciansCare

The PhysiciansCare brand offers a variety of portable eyewash solutions and over-the counter medications, including the active ingredients aspirin, acetaminophen and ibuprofen.

Spill Magic

Spill Magic is a leader in bodily fluid and spill clean-up solutions with a lightweight, absorbent powder that quickly encapsulates a spill. The Spill Response System provides all the necessary tools to effectively clean up spills, saving time, money and reducing slip & fall accidents in various venues, including grocery, retail, and big box stores; food service & hotel chains; municipal facilities; and industry-specific distributors in the U.S.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-11_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-11_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-11_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-23_2-02-results.md, 10-K_2026-03-11_item7_mdna.md, 10-K_2026-03-11_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
