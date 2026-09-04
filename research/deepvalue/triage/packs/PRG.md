# Triage pack — PRG · PROG Holdings, Inc.

_Generated 2026-09-04 14:02 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PRG · **Name:** PROG Holdings, Inc.
- **CIK:** 0001808834
- **SIC:** 7359 — Services-Equipment Rental & Leasing, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/PRG

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** PROG Holdings, Inc.
- **CIK:** 1,808,834 · **SIC:** 7359 (Services-Equipment Rental & Leasing, NEC) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 38.47 |
| mktcap | $1.5B |
| ev | $2.3B |
| ev_ebit | 11.3x |
| fcf | $324.9M |
| fcf_yield | 21.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 10.2% |
| net_debt | $801.9M |
| net_debt_ebit | 3.9x |
| cash | $85.2M |
| ltd | $887.1M |
| equity | $805.3M |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $2.4B |
| revenue_prior | $2.4B |
| rev_growth | 0.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $206.8M |
| net_income | $146.8M |
| cfo | $335.0M |
| capex | $10.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 39,831,633 |
| shares_py | 39,543,750 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 32.1% |
| r6m | 14.2% |
| off_52w_high | -18.8% |
| adv20 | $19.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.89 |
| r_ev_ebit | 0.71 |
| r_roic | 0.71 |
| r_rev_growth | 0.36 |
| r_buyback | 0.51 |
| score | 0.69 |

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
| rank | 71 |

**Screen rationale:** top-quartile FCF yield 21.2%; 12-1 momentum 32.1%


## 3. Share count trend

- Shares outstanding: **39,831,633** (CY2026Q2I) vs **39,543,750** prior year (CY2025Q2I)
- Change: **0.7%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-07** — Item 5.02 (officer / director change or comp arrangement): On May 7, 2026, PROG Holdings, Inc. (the "Company") announced that the Company's Board of Directors (the "Board") has elected Steven A. Michaels, the Company's President and Chief Executive Officer, to the additional position of Chairman of the Board...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 4,000 sh / $183,060 -> net $-183,060 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 3).

| code | rows |
|---|---|
| A | 9 |
| F | 1 |
| S | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'PROG Holdings Reports Second Quarter 2026 Results'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (a2026q2ex991earningsrelease.htm)

PROG Holdings Reports Second Quarter 2026 Results

• Consolidated revenues from continuing operations of $719.7 million, up 22.3%; Net earnings from continuing operations of $37.4 million

• Adjusted EBITDA from continuing operations of $88.4 million, up 22.8%

• Diluted EPS from continuing operations of $0.92; Non-GAAP Diluted EPS from continuing operations of $1.19, up 19.0%

• Consolidated GMV of $902.0 million, up 60.1%

• Net leverage ratio ended the quarter at 1.7x

SALT LAKE CITY, July 29, 2026 - PROG Holdings, Inc. (NYSE:PRG), the fintech holding company for Progressive Leasing, Four Technologies, MoneyApp and Purchasing Power, today announced financial results for the second quarter ended June 30, 2026, which includes the results of Purchasing Power since January 2, 2026, the date the Company acquired Purchasing Power.

"PROG Holdings delivered a strong second quarter, with revenue toward the higher end of our outlook and both adjusted EBITDA and Non-GAAP EPS coming in above the top end of our April outlook ranges, a reflection of disciplined execution across the business," said PROG Holdings Chairman, President and CEO Steve Michaels. "Every product in our ecosystem contributed: consolidated GMV grew 60% year-over-year, Progressive Leasing returned to positive GMV growth of 3.4% with adjusted EBITDA margin at 12.7%, Four delivered its eleventh consecutive quarter of triple-digit GMV growth, and Purchasing Power's GMV grew double-digits."

"Equally important was our continued strengthening of the balance sheet. We used our strong cash flow to pay down debt, bringing our net leverage ratio to approximately 1.7 times, down from about 2.5 times right after the acquisition of Purchasing Power, and comfortably within our targeted range of 1.5 to 2.0 times. This deleveraging gave us the confidence to resume share repurchases during the quarter."

"Reflecting our second-quarter outperformance and the momentum we see across our product ecosystem, we are raising our full-year 2026 outlook. Our performance is a testament to the resilience of our platform and the discipline with which we run it," concluded Michaels.

Consolidated Results

Consolidated revenues for the second quarter of 2026 were $719.7 million, an increase of 22.3% from the same period in 2025.

Consolidated net earnings from continuing operations for the quarter were $37.4 million, compared with $37.6 million in the prior year period. The effective income tax rate was 26.4% in the second quarter of 2026, compared to 26.5% in the same period in the prior year. Adjusted EBITDA from continuing operations for the quarter was $88.4 million, or 12.3% of revenues, compared with $72.0 million, or 12.2% of revenues for the same period in 2025.

Diluted earnings per share from continuing operations for the second quarter of 2026 were $0.92, compared with $0.93 in the year ago period. On a non-GAAP basis, diluted earnings per share from continuing operations were up 19.0% at $1.19 in the second quarter of 2026, compared with $1.00 for the same period in 2025.

Progressive Leasing Results

Progressive Leasing's second quarter GMV of $428.1 million was up 3.4% compared to the same period in 2025. Revenues were $550.6 million, down 3.4% from the prior year. The provision for lease merchandise write-offs for the quarter was 8.4% of leasing revenues. Earnings before taxes for the second quarter of 2026 were $45.4 million, down 11.9% from the second quarter of 2025. Adjusted EBITDA was $69.9 million, up 0.3% from the second quarter of 2025.

Four Results

Four's GMV for the second quarter of 2026 was $315.1 million, an increase of 110.6% compared to the same period in the prior year. Revenues were $35.1 million, up 118.2% from the year ago period. Four's earnings before taxes for the second quarter of 2026 were $7.1 million, up 139.9% from the second quarter of 2025. Adjusted EBITDA was $8.7 million, up 111.2% from the second quarter of 2025.

Purchasing Power Results

The Company acquired Purchasing Power on January 2, 2026. Purchasing Power's GMV, which is defined as the total value of merchandise and services purchased and delivered to customers through its platform, was $158.8 million, up 15.2% from the second quarter of 2025 on a standalone basis.

Revenues were $130.4 million in the second quarter of 2026. Loss before taxes was $0.3 million and adjusted EBITDA was $10.6 million for the second quarter of 2026.

Liquidity and Capital Allocation

PROG Holdings ended the second quarter of 2026 with cash of $85.2 million and gross debt of $893.7 million. During the quarter, the Company repaid $50.0 million of debt related to the acquisition of Purchasing Power. Since the acquisition of Purchasing Power, the Company has reduced its total debt by $304.9 million. The Company repurchased $10.2 million of its stock in the quarter at an average price of $36.37 per share, leaving $299.4 million of repurchase capacity under its $500 million share repurchase program. Additionally, the Company paid a quarterly cash dividend of $0.14 per share.

2026 Outlook

Due to the strong start to the year and the momentum in the business, the Company is increasing its full year 2026 outlook for revenue and earnings as well as providing guidance for the third quarter of 2026. This outlook assumes an operating environment with no change in the current financial pressures and uncertainties for our customers, no material changes in the Company's decisioning posture, no meaningful increase in unemployment rates for our consumer base, an effective tax rate for non-GAAP EPS of approximately 26% and no impact from additional share purchases.

Revised 2026 outlook | Previous 2026 outlook
(In thousands, except per share amounts) | Low | High | Low | High
PROG Holdings - Total revenues from continuing operations | 3,025,000 | 3,100,000 | 3,000,000 | 3,100,000
PROG Holdings - Net earnings from continuing operations | 155,000 | 164,500 | 150,500 | 166,000
PROG Holdings - Adjusted EBITDA from continuing operations | 355,000 | 375,000 | 343,000 | 370,000
PROG Holdings - Diluted EPS from continuing operations | 3.82 | 4.06 | 3.68 | 4.06
PROG Holdings - Diluted non-GAAP EPS from continuing operations | 4.75 | 5.00 | 4.40 | 4.80
Progressive Leasing - Total revenues | 2,247,500 | 2,285,000 | 2,227,500 | 2,285,000
Progressive Leasing - Earnings before taxes | 188,500 | 193,000 | 191,000 | 198,500
Progressive Leasing - Adjusted EBITDA | 272,500 | 279,500 | 269,500 | 279,500
Purchasing Power - Total revenues | 620,000 | 640,000 | 620,000 | 640,000
Purchasing Power - Earnings before taxes | 17,000 | 21,500 | 14,500 | 22,000
Purchasing Power - Adjusted EBITDA | 54,000 | 60,000 | 50,000 | 60,000
Four - Total revenues | 145,000 | 157,000 | 140,000 | 157,000
Four - Earnings before taxes | 22,000 | 25,000 | 16,500 | 20,500
Four - Adjusted EBITDA | 30,000 | 34,000 | 25,000 | 29,000
Other - Total revenues | 12,500 | 18,000 | 12,500 | 18,000
Other - Loss before taxes | (13,500) | (10,500) | (14,500) | (12,000)
Other - Adjusted EBITDA | (1,500) | 1,500 | (1,500) | 1,500

Three months ended September 30, 2026 outlook
(In thousands, except per share amounts) | Low | High
PROG Holdings - Total revenues from continuing operations | 715,000 | 750,000
PROG Holdings - Net earnings from continuing operations | 36,000 | 42,500
PROG Holdings - Adjusted EBITDA from continuing operations | 79,000 | 89,000
PROG Holdings - Diluted EPS from continuing operations | 0.86 | 1.06
PROG Holdings - Diluted non-GAAP EPS from continuing operations | 1.00 | 1.20

Conference Call and Webcast

The Company has scheduled a live webcast and conference call for Wednesday, July 29, 2026, at 8:30 A.M. ET to discuss its financial results for the second quarter of 2026. To access the live webcast, visit the Events and Presentations page of the Company's Investor Relations website, https://investor.progholdings.com/.

About PROG Holdings, Inc.

PROG Holdings, Inc. (NYSE:PRG) is a fintech holding company headquartered in Salt Lake City, UT, that provides inclusive, transparent and competitive payment options to consumers. The Company owns Progressive Leasing, a leading provider of e-commerce, app-based, and in-store point-of-sale lease-to-own solutions; Purchasing Power, a voluntary employee benefit program provider, allowing employees to purchase brand-name products and services through either automatic payroll deductions or allotments; Four Technologies, a provider of Buy Now, Pay Later payment options through its platform, Four; and MoneyApp, a mobile application that offers customers interest-free cash advances. More information on PROG Holdings and its companies can be found at https://investor.progholdings.com/.

(In thousands, except per share data)

(Unaudited) Three months ended | (Unaudited) Six months ended
June 30, | June 30,
2026 | 2025 | 2026 | 2025
Revenues
Lease revenues and fees | 549,830 | 569,674 | 1,146,694 | 1,221,231
Product and service revenues | 128,507 | — | 234,913 | —
Other revenue | 41,378 | 18,829 | 80,782 | 35,700
719,715 | 588,503 | 1,462,389 | 1,256,931
Costs and expenses
Depreciation of lease merchandise | 364,311 | 385,107 | 773,321 | 845,550
Cost of product sales | 75,702 | — | 138,208 | —
Provision for lease merchandise write-offs | 46,499 | 42,633 | 90,150 | 90,651
Operating expenses | 143,417 | 93,409 | 293,617 | 191,533
Provision for credit losses | 30,667 | 8,043 | 54,834 | 13,544
660,596 | 529,192 | 1,350,130 | 1,141,278
Gain on sale of lease receivables | 4,701 | — | 11,158 | —
Gain on change in fair value of receivables | 1,810 | — | 7,522 | —
Operating profit | 65,630 | 59,311 | 130,939 | 115,653
Interest expense | (15,217) | (9,794) | (33,606) | (19,757)
Interest income | 394 | 1,645 | 1,037 | 2,518
Earnings from continuing operations before income tax expense | 50,807 | 51,162 | 98,370 | 98,414
Income tax expense | 13,429 | 13,581 | 24,774 | 26,243
Net earnings from continuing operations | 37,378 | 37,581 | 73,596 | 72,171
(Loss) earnings from discontinued operations, net of tax | (349) | 902 | (513) | 1,030
Net earnings | 37,029 | 38,483 | 73,083 | 73,201
Basic earnings per share
Continuing operations | 0.93 | 0.94 | 1.84 | 1.78
Discontinued operations | (0.01) | 0.02 | (0.01) | 0.03
Total basic earnings per share | 0.92 | 0.96 | 1.83 | 1.81
Diluted earnings per share
Continuing operations | 0.92 | 0.93 | 1.81 | 1.75
Discontinued operations | (0.01) | 0.02 | (0.01) | 0.03
Total diluted earnings per share | 0.91 | 0.95 | 1.80 | 1.78
Cash dividend declared per share
Common stock | 0.14 | 0.13 | 0.28 | 0.26
Weighted average shares outstanding
Basic | 40,177 | 40,130 | 40,038 | 40,484
Diluted | 40,734 | 40,559 | 40,772 | 41,203

PROG Holdings, Inc.

Consolidated Balance Sheets

(In thousands, except share data)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-18_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Business Overview

PROG Holdings, Inc. ("we," "our," "us," the "Company," or "PROG Holdings") is a financial technology holding company that provides transparent and competitive payment options to consumers. As of December 31, 2025, PROG Holdings has two reportable segments: (i) Progressive Leasing, an in-store, app-based, and e-commerce point-of-sale lease-to-own solutions provider; and (ii) Four Technologies, Inc. ("Four"), which offers Buy Now, Pay Later ("BNPL") payment options to consumers through the Four platform. Vive Financial ("Vive"), an omnichannel provider of second-look revolving credit products, had been an operating segment prior to October 20, 2025. On that date, the Company sold substantially all of Vive's loan receivables portfolio and began the process of discontinuing its remaining operations. Vive is presented as discontinued operations in the Company's consolidated financial statements.

Our Progressive Leasing segment provides consumers with lease-purchase solutions through its point-of-sale partner locations and e-commerce website partners (collectively, "POS partners"). It does so by purchasing merchandise from the POS partners desired by customers and, in turn, leasing that merchandise to the customers through a cancellable lease-to-own transaction. Progressive Leasing has no stores of its own, but rather offers lease-purchase solutions to the customers of traditional and e-commerce retailers. The Progressive Leasing segment comprised approximately 96% of our consolidated revenues from continuing operations for the year ended December 31, 2025.

Four allows shoppers to pay for merchandise through four interest-free installments. Four's proprietary platform capabilities and its base of customers and retailers expand PROG Holdings' ecosystem of financial technology offerings by introducing a payment solution that further diversifies the Company's consumer financial technology offerings. Shoppers use Four to purchase furniture, clothing, electronics, health and beauty products, footwear, jewelry, and other consumer goods from retailers across the United States. The average ticket size of a Four transaction is significantly smaller than a transaction with Progressive Leasing.

PROG Holdings also owns MoneyApp, a mobile application that offers customers interest-free cash advances. MoneyApp is not a reportable segment in 2025 as its financial results are not significant to the Company's consolidated financial results. MoneyApp's financial results are reported within "Other" for segment reporting purposes.

Sale of Receivables and Presentation of Vive as Discontinued Operations

On October 20, 2025, we completed the sale of substantially all of the assets of Vive, consisting of the majority of its loans receivable portfolio, along with the related customer and merchant relationships. This transaction resulted in $143.9 million of net cash consideration. Subsequent to the sale, the operations of Vive began to wind down. The transaction resulted in a strategic shift that will have a significant effect on our operations and financial results. Accordingly, Vive is now reported as discontinued operations in our consolidated financial statements for all periods presented. All of Vive's revenues and expenses, other than allocated corporate overhead, are excluded from the results of continuing operations.

Acquisition of Purchasing Power

On January 2, 2026, we completed the acquisition of Purchasing Power for $420.0 million in cash. In addition, Purchasing Power had approximately $338.6 million of non-recourse funding debt that remained in place following the closing of the acquisition. Purchasing Power is a voluntary employee benefit program provider allowing employees to purchase brand-name products and services from Purchasing Power and then pay for those purchases through either automatic payroll deductions or allotments. Millions of employees nationwide have access to Purchasing Power's innovative purchasing options and financial wellness offerings. This MD&A does not include, reflect, or give effect to the acquisition of Purchasing Power. See Note 16 in our consolidated financial statements included in this Form 10-K for additional information.

Macroeconomic and Business Environment

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Results of Operations – Years Ended December 31, 2025 and 2024

Change
Year Ended December 31, | 2025 vs. 2024
(In Thousands) | 2025 | 2024 | %
REVENUES:
Lease Revenues and Fees | 2,322,754 | 2,366,489 | (43,735) | (1.8) | %
Other Revenues | 86,469 | 32,592 | 53,877 | 165.3
2,409,223 | 2,399,081 | 10,142 | 0.4
COSTS AND EXPENSES:
Depreciation of Lease Merchandise | 1,590,240 | 1,621,101 | (30,861) | (1.9)
Provision for Lease Merchandise Write-offs | 173,115 | 178,338 | (5,223) | (2.9)
Operating Expenses | 445,747 | 404,917 | 40,830 | 10.1
2,209,102 | 2,204,356 | 4,746 | 0.2
Gain on Sale of Receivables | 6,652 | — | 6,652 | nmf
OPERATING PROFIT | 206,773 | 194,725 | 12,048 | 6.2
Interest Expense, Net | (32,254) | (31,289) | (965) | (3.1)
EARNINGS FROM CONTINUING OPERATIONS BEFORE INCOME TAX EXPENSE (BENEFIT) | 174,519 | 163,436 | 11,083 | 6.8
INCOME TAX EXPENSE (BENEFIT) | 50,167 | (33,875) | 84,042 | nmf
NET EARNINGS FROM CONTINUING OPERATIONS | 124,352 | 197,311 | (72,959) | (37.0)
EARNINGS FROM DISCONTINUED OPERATIONS, NET OF TAX | 22,436 | (62) | 22,498 | nmf
NET EARNINGS | 146,788 | 197,249 | (50,461) | (25.6) | %

nmf—Calculation is not meaningful

Revenues

Information about our revenues by source and reportable segment is as follows:

Year Ended December 31, 2025 | Year Ended December 31, 2024
(In Thousands) | Progressive Leasing | Four | Other | Total | Progressive Leasing | Four | Other | Total
Lease Revenues and Fees | 2,322,754 | — | — | 2,322,754 | 2,366,489 | — | — | 2,366,489
Other Revenues | — | 73,722 | 12,747 | 86,469 | — | 27,351 | 5,241 | 32,592
Total Revenues | 2,322,754 | 73,722 | 12,747 | 2,409,223 | 2,366,489 | 27,351 | 5,241 | 2,399,081

The decrease in Progressive Leasing revenues was primarily the result of the 8.6% decrease in GMV for 2025 as compared to the prior year, which was largely attributable to the closure of Big Lots' store locations following its bankruptcy in late 2024, a tightening in our decisioning posture in early 2025, and a decrease in consumer confidence, disposable income and demand for leasable durable consumer goods for our customer base, as a result of elevated living costs and economic uncertainty. The increase in Four revenue was primarily driven by a 144.2% increase in Four's GMV as compared to 2024, due to increased loan originations, which resulted from the significant growth in Four's business year over year. Four's revenue also benefitted from an increase in subscription fee revenues in 2025 when compared to the prior year. The average ticket size of a BNPL transaction with Four is significantly lower than a transaction with Progressive Leasing. For this reason, we believe demand for the merchandise financed through Four is not impacted by the macroeconomic headwinds discussed above to the same degree as demand for larger-ticket leasable goods. The increase to Other operations revenue was primarily driven by growth in our MoneyApp business.

Operating Expenses

Information about certain significant components of operating expenses is as follows:

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-18_item1_business.md)

ITEM 1. BUSINESS

Unless otherwise indicated or unless the context otherwise requires, all references in this Annual Report on Form 10-K to the "Company," "we," "us," "our" and similar expressions are references to PROG Holdings, Inc. ("PROG Holdings") and its consolidated subsidiaries.

Overview

PROG Holdings is a financial technology holding company that provides transparent and competitive payment options to consumers. PROG Holdings' operating segments include Progressive Leasing, an in-store, app-based, and e-commerce point-of-sale lease-to-own solutions provider, and Four Technologies, Inc. ("Four"), a modern, cloud-native mobile app which offers Buy Now, Pay Later ("BNPL") payment options to consumers through the Four platform. PROG Holdings also owns MoneyApp, a mobile application that offers customers interest-free cash advances. Many of our customers fall within the near-prime or subprime Fair Isaac and Company ("FICO") score categories and may have difficulty purchasing big-ticket and other durable goods they desire. The unified financial technologies ecosystem we continue to build, which we have expanded through our recent acquisition of Purchasing Power (as described below) provides these underserved customers with alternatives to traditional financing options.

The Progressive Leasing segment comprised approximately 96% of our consolidated revenues for the year ended December 31, 2025. Progressive Leasing provides consumers with lease-purchase solutions for merchandise, including furniture, appliances, electronics, mobile phones and accessories, jewelry, mattresses, and automobile electronics and accessories from leading traditional and e-commerce retailers (whom we refer to as our point-of-sale partners, "POS partners," or "retail partners"). Progressive Leasing's technology-based, proprietary decisioning platform offers prompt lease decisioning at the point-of-sale and is integrated with both traditional and e-commerce POS partners' systems. Progressive Leasing provides customers with transparent and competitive lease payment options along with flexible terms that are designed to help customers achieve merchandise ownership, including through low initial payments and early buyout options. Lease-to-own transactions facilitated through our Company also benefit our POS partners by generating incremental sales to credit-challenged consumers, who typically would not have qualified for financing offers traditionally provided by these retailers.

The Four segment enables consumers of all credit backgrounds to pay for purchases over time through short-term, interest-free installment BNPL plans. Four offers transparent, fixed-term payment options, powered by its proprietary risk-decisioning engine and its direct-to-consumer mobile app.

Sale of Vive Financial

On October 20, 2025, PROG Holdings sold substantially all of the loans receivable portfolio of Vive Financial ("Vive"), an omnichannel provider of second-look revolving credit products, which had been an operating segment prior to the sale. Following the sale, the Company began the wind-down of Vive's operations. See Note 2 in our consolidated financial statements included in this Form 10-K for additional information.

Acquisition of Purchasing Power

On January 2, 2026, PROG Holdings acquired Purchasing Power, a company that provides the employees of Purchasing Power's employer-clients with a voluntary employee benefit program that allows employees to purchase brand-name products and services from Purchasing Power and pay for those purchases through either automatic payroll deductions or allotments. Millions of employees nationwide have access to Purchasing Power's innovative purchasing options and financial wellness offerings. See Note 16 in our consolidated financial statements included in this Form 10-K for additional information.

By expanding the products offered by the Company, we are building a unified financial ecosystem, as illustrated below.

Strategy

We have a three pillared strategy, which we believe positions us for success over the long-term, as follows:

• Grow our gross merchandise volume ("GMV") through existing merchant partners, new partners, and direct-to-consumer initiatives - We plan to grow GMV through strategic collaboration and marketing efforts with our existing POS partners and by focusing on converting our pipeline of retailers into new POS partners. Our ability to maintain and strengthen new and existing relationships, including addressing the changing needs of our POS partners, is critical to the long-term growth of our business. We will also continue to expand our direct-to-consumer marketing efforts to attract new customers and drive more GMV through in-store and online retailers. In addition, we plan to grow GMV through Four, which, as a cloud-enabled mobile app is capable of scaling rapidly and efficiently. Four enables us to reach a broader customer base beyond traditional lease-to-own transactions and capture incremental GMV through short-term installment plans across a wide range of merchants and categories by engaging customers directly, as well as providing cross-promotion opportunities.

• Enhance our industry-leading consumer experience - We are investing in technology platforms that promote customer engagement and simplify the application, origination and servicing experience. We are committed to providing our customers with transparency, flexibility, and more choices on how and where they choose to shop. We

are expanding and innovating our e-commerce capabilities to benefit existing and new POS partners and customers. Through Four, we are also investing in digital payment technologies that provide customers with transparent and flexible installment options, integrated with an intuitive mobile app experience.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-18_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-18_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-18_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-02-18_item7_mdna.md, 10-K_2026-02-18_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
