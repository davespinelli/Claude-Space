# Triage pack — LZ · LEGALZOOM.COM, INC.

_Generated 2026-09-04 15:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** LZ · **Name:** LEGALZOOM.COM, INC.
- **CIK:** 0001286139
- **SIC:** 7374 — Services-Computer Processing & Data Preparation
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/LZ

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** LEGALZOOM.COM, INC.
- **CIK:** 1,286,139 · **SIC:** 7374 (Services-Computer Processing & Data Preparation) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 6.40 |
| mktcap | $1.1B |
| ev | $928.9M |
| ev_ebit | 37.2x |
| fcf | $147.9M |
| fcf_yield | 13.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$167.2M |
| net_debt_ebit | -6.7x |
| cash | $167.2M |
| ltd | $0.00 |
| equity | $127.2M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $756.0M |
| revenue_prior | $681.9M |
| rev_growth | 10.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $25.0M |
| net_income | $15.4M |
| cfo | $178.2M |
| capex | $30.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -5.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 171,264,812 |
| shares_py | 180,249,374 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -26.4% |
| r6m | -5.6% |
| off_52w_high | -42.3% |
| adv20 | $16.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.80 |
| r_ev_ebit | 0.21 |
| r_roic | 0.50 |
| r_rev_growth | 0.67 |
| r_buyback | 0.88 |
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
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 129 |

**Screen rationale:** top-quartile FCF yield 13.5%; buying back stock -5.0%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **171,264,812** (CY2026Q2I) vs **180,249,374** prior year (CY2025Q2I)
- Change: **-5.0%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 577,475 sh / $3,375,197 -> net $-3,375,197 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 4).

| code | rows |
|---|---|
| A | 4 |
| F | 7 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'LegalZoom Reports Second Quarter 2026 Financial Results'; skipped 17 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (lz-q22026earningsxexx991.htm)

LegalZoom Reports Second Quarter 2026 Financial Results

• Revenue of $205.3 million, up 7% year-over-year, driven by subscription revenue increasing 11% year-over-year, representing LegalZoom's fifth consecutive quarter of double digit subscription revenue growth

• Subscription revenue of $133.4 million up 11% year-over- year from strength in human-in-the-loop offerings and pricing initiatives

• Net income of $5.2 million and net income margin of 3%; with net income margin increasing approximately 260 basis points year-over-year

• Adjusted EBITDA of $45.9 million and Adjusted EBITDA margin of 22%, ahead of the high end of our guidance range; with Adjusted EBITDA margin increasing approximately 220 basis points year-over-year

• Commitment to shareholder returns; completed $45.5 million of share repurchases in the quarter, with approximately $80.4 million remaining under the existing authorization

• Ended the quarter with cash and cash equivalents of $167.2 million and delivered $39.5 million in cash from operating activities and $33.7 million in free cash flow with no debt outstanding as of June 30, 2026

• Updating full-year 2026 revenue outlook to $795.0–$805.0 million and Adjusted EBITDA to $190.0–$195.0 million, reflecting the recent industry-wide shift in customer discovery away from traditional search, while maintaining strong margin discipline

MOUNTAIN VIEW, California – August 5, 2026 – LegalZoom (Nasdaq: LZ), America's #1 online legal services company, today announced results for its second quarter ended June 30, 2026.

"Since late 2024, we've deliberately repositioned LegalZoom around subscription relationships that pair AI with trusted human expertise," said Jeff Stibel, Chairman and Chief Executive Officer of LegalZoom. "That strategy is working. While demand for what we do is intact, discovery is moving. We have been actively building new customer acquisition channels for more than a year, and our outlook fully reflects today's environment, with no recovery in traditional search assumed. In the AI channels where discovery is heading, every visit is incremental. We've partnered with the leading AI companies, we have more brand references across AI platforms than any competitor, and we haven't assumed how quickly this scales. That's the upside we're positioned to capture."

"We're updating our revenue expectations based on recent changes in the customer acquisition environment, while our profitability outlook reflects the discipline of our operating model," said Noel Watson, Chief Operating Officer and Chief Financial Officer. "We continue to improve operating efficiency, expand margins and generate strong cash flow while investing behind the initiatives that support our long-term growth strategy."

Second Quarter 2026 Highlights

• Revenue was $205.3 million for the quarter, up 7% year-over-year.

◦ Transaction revenue of $71.9 million decreased 1% year-over-year.

◦ Subscription revenue of $133.4 million grew 11% year-over-year.

• Net income was $5.2 million for the quarter, or 3% of revenue, compared to a net loss of $0.3 million, or less than 1% of revenue, in the same period in 2025.

• Adjusted EBITDA was $45.9 million for the quarter, or 22% of revenue, compared to $39.0 million, or 20% of revenue, in the same period in 2025.

• Non-GAAP net income was $27.4 million for the quarter compared to $28.3 million in the same period in 2025.

• Cash and cash equivalents were $167.2 million as of June 30, 2026 compared to $203.1 million as of December 31, 2025.

• Cash flows provided by operating activities were $39.5 million for the quarter ended June 30, 2026 compared to $39.1 million in the same period in 2025.

• Free cash flow was $33.7 million for the quarter ended June 30, 2026 compared to $31.6 million in the same period in 2025.

• Basic and diluted net income per share was $0.03 for the quarter compared to a basic and diluted net loss per share of $— for the same period in 2025. Basic and diluted Non-GAAP net income per share was $0.16 for the quarter compared to basic and diluted Non-GAAP net income per share of $0.16 and $0.15, respectively, for the same period in 2025.

Key Business Metrics and Non-GAAP Financial Measures

(Unaudited, in thousands except AOV, ARPU and percentages)

Three Months Ended June 30, | % Growth | Six Months Ended June 30, | % Growth
(Decline) | (Decline)
2026 | 2025 | YOY | 2026 | 2025 | YOY
Total revenue | 205,289 | 192,509 | 7 | % | 412,070 | 375,619 | 10 | %
Transaction revenue | 71,890 | 72,611 | (1) | % | 148,513 | 139,464 | 6 | %
Subscription revenue | 133,399 | 119,898 | 11 | % | 263,557 | 236,155 | 12 | %
Gross profit | 139,930 | 125,111 | 12 | % | 272,183 | 241,661 | 13 | %
Gross margin | 68 | % | 65 | % | 5 | % | 66 | % | 64 | % | 3 | %
Net Income (loss) | 5,183 | (266) | n/m | 6,287 | 4,861 | 29 | %
Net income (loss) margin | 3 | % | — | % | n/m | 2 | % | 1 | % | 100 | %
Net Income (loss) per share — basic: | 0.03 | — | n/m | 0.04 | 0.03 | 33 | %
Net Income (loss) per share — diluted: | 0.03 | — | n/m | 0.04 | 0.03 | 33 | %
Net cash provided by operating activities | 39,547 | 39,139 | 1 | % | 86,829 | 89,842 | (3) | %
Non-GAAP Financial Measures
Non GAAP net income | 27,444 | 28,329 | (3) | % | 49,515 | 52,151 | (5) | %
Non GAAP net income per share — basic: | 0.16 | 0.16 | — | % | 0.28 | 0.29 | (3) | %
Non GAAP net income per share — diluted: | 0.16 | 0.15 | 7 | % | 0.28 | 0.29 | (3) | %
Adjusted EBITDA | 45,898 | 38,965 | 18 | % | 82,360 | 75,977 | 8 | %
Adjusted EBITDA margin | 22 | % | 20 | % | 10 | % | 20 | % | 20 | % | — | %
Free cash flow | 33,690 | 31,609 | 7 | % | 74,664 | 72,934 | 2 | %
Key Business Metrics
Transaction units | 281 | 278 | 1 | % | 656 | 619 | 6 | %
Business formations | 125 | 131 | (5) | % | 267 | 262 | 2 | %
Average order value (AOV) | 256 | 262 | (2) | % | 227 | 225 | 1 | %
Subscription units at period end | 1,892 | 1,955 | (3) | % | 1,892 | 1,955 | (3) | %
Average revenue per subscription unit (ARPU) at period end | 270 | 256 | 5 | % | 270 | 256 | 5 | %
Certain percentages may not recalculate due to rounding.

Financial Guidance and Outlook

LegalZoom is updating its revenue outlook and Adjusted EBITDA outlook for the full year ending December 31, 2026 as follows:

• Revenue is expected to be in the range of $795 million to $805 million, or 6% year-over-year growth at the midpoint. This compares to the Company's previous revenue outlook in the range of $810 million to $830 million, or 8% growth at the midpoint. LegalZoom's outlook reflects the continued scaling of our higher-value growth initiatives and ongoing momentum from our partner channel, partially offset by a more cautious view of customer acquisition for the remainder of the year.

• Adjusted EBITDA is expected to be in the range of $190 million to $195 million, reflecting 12% year-over-year growth at the midpoint, and a 24% margin. This compares to the Company's previous Adjusted EBITDA outlook of $190 million to $200 million, or 13% year-over-year growth, and a 24% margin. LegalZoom's outlook reflects disciplined cost management, ongoing gross margin improvement and the benefits from a 13% workforce reduction announced today.

For the third quarter ending September 30, 2026 LegalZoom expects:

• Revenue in the range of $192 million to $196 million, or 2% year-over-year growth at the midpoint.

• Adjusted EBITDA in the range of $49 million to $51 million, an 8% year-over-year increase at the midpoint, and a 26% margin.

Webcast and Conference Call Information

A webcast and conference call to discuss second quarter 2026 results is scheduled for today, August 5, 2026, at 4:30 p.m. Eastern time/1:30 p.m. Pacific time. Those interested in participating in the conference call are invited to register Here.

A live audio webcast of the event will be available on the LegalZoom Investor Relations website: https://investors.legalzoom.com. An archived replay of the webcast also will be available shortly after the live event.

We are not providing a reconciliation for our non-GAAP outlook on a forward-looking basis (including the information under "Financial Guidance and Outlook" above), as we are unable to provide a meaningful

calculation or estimation of reconciling items and the information is not available without unreasonable effort. This is due to the inherent difficulty of forecasting the timing or amount of various items that would impact the most directly comparable forward-looking GAAP financial measure that have not yet occurred, are out of LegalZoom's control and/or cannot be reasonably predicted. Forward-looking non-GAAP financial measures provided without the most directly comparable GAAP financial measures may vary materially from the corresponding GAAP financial measures.

The tables in this press release contain more details on the GAAP financial measures that are most directly comparable to non-GAAP financial measures and the related reconciliations between these financial measures.

LegalZoom

LegalZoom is a leading online platform for legal services, transforming how individuals and small businesses navigate the legal system. By combining intuitive technology with access to experienced attorneys, whether through our vast independent attorney network or our own law firm, we offer the tools and guidance people need to confidently manage everything from business formation and compliance to intellectual property protection and ongoing business management and legal support.

As AI reshapes how legal work gets done, LegalZoom is at the forefront of the human-in-the-loop approach, ensuring that the speed and efficiency of AI is always backed by the judgment and accountability of qualified professionals. With over two decades of experience and millions of customers served, LegalZoom helps individuals and small businesses navigate legal needs with confidence. For more information, please visit www.legalzoom.com.

Contact

Investor Relations

investor@legalzoom.com

LegalZoom.com, Inc.

Unaudited Condensed Consolidated Balance Sheets

(In thousands, except par values)

June 30, 2026 | December 31, 2025
Assets
Current assets:
Cash and cash equivalents | 167,227 | 203,100
Accounts receivable, net of allowance | 19,759 | 20,589
Prepaid expenses and other current assets | 25,187 | 18,234
Total current assets | 212,173 | 241,923
Property and equipment, net | 53,540 | 58,045
Goodwill | 140,705 | 140,705
Intangible assets, net | 14,932 | 18,152
Operating lease right-of-use assets | 14,150 | 13,414
Deferred income taxes | 24,095 | 31,884
Other assets | 6,764 | 7,399
Total assets | 466,359 | 511,522
Liabilities and stockholders' equity
Current liabilities:
Accounts payable | 35,875 | 27,167
Accrued expenses and other current liabilities | 56,055 | 83,361
Deferred revenue | 221,180 | 203,653
Operating lease liabilities | 5,003 | 4,338
Total current liabilities | 318,113 | 318,519
Operating lease liabilities, non-current | 10,133 | 10,025
Deferred revenue | 234 | 277
Other liabilities | 10,723 | 10,819
Total liabilities | 339,203 | 339,640
Commitments and contingencies
Stockholders' equity:
Preferred stock, $0.001 par value; 100,000 shares authorized at June 30, 2026 and December 31, 2025, none issued or outstanding at June 30, 2026 and December 31, 2025 | — | —
Common stock, $0.001 par value; 1,000,000 shares authorized; 167,451 shares and 177,624 shares issued and outstanding at June 30, 2026 and December 31, 2025, respectively | 169 | 179
Additional paid-in capital | 1,344,473 | 1,305,936
Accumulated deficit | (1,217,855) | (1,134,414)
Accumulated other comprehensive income | 369 | 181
Total stockholders' equity | 127,156 | 171,882
Total liabilities and stockholders' equity | 466,359 | 511,522

LegalZoom.com, Inc.

Unaudited Condensed Consolidated Statements of Operations

(In thousands, except per share amounts)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-23_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

LegalZoom is a leading online platform for legal services, transforming how individuals and small businesses navigate the legal system. By combining intuitive technology with access to experienced attorneys—whether through our vast independent attorney network or our own law firm—we offer the tools and guidance people need to confidently manage everything from business formation and compliance to intellectual property protection and ongoing business management and legal support. We operate across all 50 states and in over 3,000 counties in the U.S. With over two decades of experience and millions of customers served, LegalZoom helps individuals and small businesses navigate legal needs with confidence.

Key Factors Affecting Our Performance

We believe that our future performance will depend on many factors, including the following:

• Macroeconomic factors . Adverse changes in, or uncertainty with respect to, general macroeconomic, political, regulatory and market conditions can negatively impact consumer spending patterns, the success of existing small businesses and the formation of new small businesses. While we continue to actively monitor the impacts of the evolving macroeconomic environment on all aspects of our business, future negative or decelerating impacts from factors such as inflation, tariffs, higher interest rates, regulatory obstacles or changes in laws and regulations remain uncertain.

• Our share of small and medium-sized businesses (SMBs) . In 2025, business formations represented the largest share of our total transaction orders. Business formations act as an entrance point for many customers to the LegalZoom ecosystem, where they then often purchase a mix of transaction and subscription offerings alongside and after the initial formation transaction. In addition, we are expanding our go-to-market strategy to focus on emerging and established business, which we believe will decrease our dependence on business formations over time. As a result, our operating results depend on the continuation of new business formations in the U.S. and even more so, on our ability to increase our share of new business formations and to attract existing businesses to our platform.

• Ability to enhance customer lifetime value . Our future performance depends on our ability to integrate new products and services into our LegalZoom ecosystem and to increase recurring revenue through subscription offerings. As we continue to optimize our subscription business, including by testing various commercialization strategies for our offerings and introducing new, higher value DIFM subscription offerings, we have experienced and we expect to continue to experience increased volatility across our key business metrics.

• Ability to integrate augmented legal expertise . We believe that the future of legal and small business services involves a combination of AI and human expertise. We aim to utilize AI to drive efficiency and scale, while relying on our team of concierge managers and our independent network of attorneys to provide the judgment and trust that customers need. The extent to which we are able to combine AI with our human expertise in order to drive cost efficiencies and increase the consumption of our DIFM offerings will impact our future results of operations.

Key Components of our Results of Operations

Revenue

We generate revenue from the sources identified below.

Transaction revenue —Transaction revenue is primarily generated from our customized legal document services upon fulfillment of these services. Transaction revenue includes filing fees and is net of cancellations, promotional discounts, sales allowances and credit reserves. We also earn fees from third-party providers in connection with lead generation activities, where referred customers purchased services that are transactional in nature.

Subscription revenue —Subscription revenue is generated primarily from subscriptions to our registered agent, compliance packages, attorney advice, legal forms, tax and accounting, virtual mail and eSignature

services, and software-as-a-service, or SaaS, subscriptions. We generally recognize revenue from our subscriptions ratably over the subscription term. Subscription terms generally range from thirty days to one year. Subscription revenue also includes amounts earned from third-party providers in connection with lead generation activities, where referred customers purchased services that are subscription in nature. Subscription revenue includes the transaction price allocated to bundled free trials for our subscription services and is net of promotional discounts, cancellations, sales allowances and credit reserves and payments to third-party service providers such as legal plan law firms.

For transaction and subscription revenue, we generally collect payments and fees at the time orders are placed and prior to services being rendered. We record amounts collected for services that have not been performed as deferred revenue on our consolidated balance sheet. The transaction price that we record is generally based on the contractual amounts and is reduced for estimated sales allowances for price concessions, charge-backs, sales credits and refunds, which are accounted for as variable consideration when estimating the amount of revenue to recognize.

See the section titled "— Critical Accounting Estimates—Revenue Recognition " below for a description of the accounting policies related to revenue recognition, including arrangements that contain multiple deliverables.

Cost of revenue

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The table below sets forth our consolidated statement of operations data for each of the periods indicated. The period-to-period comparison of financial results should not be considered as a prediction or indicative of our future results.

Year Ended December 31,
2025 | 2024
(in thousands)
Revenue | 756,043 | 681,881
Cost of revenue (1)(2) | 257,960 | 240,093
Gross profit | 498,083 | 441,788
Operating expenses:
Sales and marketing (1)(2) | 261,745 | 207,684
Technology and development (1)(2) | 81,941 | 89,584
General and administrative (1)(2) | 143,758 | 108,939
Gain on sale of assets held for sale | (14,337) | —
Total operating expenses | 473,107 | 406,207
Income from operations | 24,976 | 35,581
Interest expense | (1,294) | (446)
Interest income | 7,569 | 7,850
Other income, net | 1,187 | 98
Income before income taxes | 32,438 | 43,083
Provision for income taxes | 17,011 | 13,120
Net income | 15,427 | 29,963

(1) Includes stock-based compensation expense as follows:

Year Ended December 31,
2025 | 2024
(in thousands)
Cost of revenue | 5,538 | 5,833
Sales and marketing | 16,810 | 8,077
Technology and development | 15,097 | 19,573
General and administrative | 76,263 | 38,027
Total stock-based compensation expense | 113,708 | 71,510

Stock-based compensation expense increased for the year ended December 31, 2025 compared to the year ended December 31, 2024 primarily due to a full year of expense recognition in 2025 for our awards with performance conditions as well as those with market-based conditions, or, collectively, PSUs, granted in 2024, compared to a partial year of expense in 2024. Refer to Note 14 to our consolidated financial statements included elsewhere in this Annual Report on Form 10-K.

(2) Includes depreciation and amortization expense for our property and equipment, including capitalized internal-use software and intangible assets as follows:

Year Ended December 31,
2025 | 2024
(in thousands)
Cost of revenue | 20,687 | 18,902
Sales and marketing | 9,261 | 3,736
Technology and development | 8,516 | 7,688
General and administrative | 5,659 | 4,601
Total depreciation and amortization expense | 44,123 | 34,927

Comparison of the Year Ended December 31, 2025 and 2024

Revenue

Year Ended December 31,
2025 | 2024 | $ change | % change
(in thousands, except percentages)
Revenue by type
Transaction | 263,582 | 245,692 | 17,890 | 7 | %
Subscription | 492,461 | 436,189 | 56,272 | 13 | %
Total revenue | 756,043 | 681,881 | 74,162 | 11 | %

The 11% increase in total revenue for the year ended December 31, 2025 compared to the year ended December 31, 2024 was driven by an increase in subscription revenue. Subscription revenue was 65% and 64% of total revenue for the years ended December 31, 2025 and 2024, respectively, and transaction revenue was 35% and 36% of total revenue for the years ended December 31, 2025 and 2024, respectively.

Transaction revenue increased 7% year-over-year for the year ended December 31, 2025 primarily due to approximately $33.2 million in revenue from transactions derived from our acquisition of Formation Nation in February 2025 and an increase in revenue from annual report filing fees and trademark filings, partially offset by a decline in beneficial ownership information report revenue due to the FinCEN ruling on March 21, 2025 that eliminated this filing requirement for U.S. companies.

Subscription revenue increased 13% year-over-year for the year ended December 31, 2025 primarily due to approximately $18.2 million in revenue from subscriptions derived from our acquisition of Formation Nation in February 2025, as well as an 11% increase in revenue from compliance-related subscriptions, an increase in revenue from our virtual mail offering and revenue earned from the 1-800 Accountant partnership entered into in December 2024. Subscription revenue growth was partially offset by our prior discontinuation of new customer acquisition for our tax offering.

Cost of revenue

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-23_item1_business.md)

Item 1. Business

Overview

LegalZoom is a leading online platform for legal services, transforming how individuals and small businesses navigate the legal system. By combining intuitive technology with access to experienced attorneys—whether through our vast independent attorney network or our own law firm—we offer the tools and guidance people need to confidently manage everything from business formation and compliance to intellectual property protection and ongoing business management and legal support. Our ongoing business management services include virtual mail, legal forms, bookkeeping and estate planning services, among others. We operate across all 50 states and in over 3,000 counties in the U.S. With over two decades of experience and millions of customers served, LegalZoom helps individuals and small businesses navigate legal needs with confidence.

In February 2025, we acquired Formation Nation, Inc., or Formation Nation, a small business service company. Formation Nation provides services ranging from white-glove business formation and compliance offerings under its Nevada Corporate Headquarters (NCH) business to low-cost business formations under its flagship Inc Authority brand.

Our Customers and Solutions

As of June 30, 2025. there were over 36 million U.S. small businesses in operation, and millions of new small businesses are formed in the U.S. every year. Many small businesses operate without forming a legal entity, unintentionally introducing financial risk to the owners' personal assets. The businesses that recognize that risk upfront often struggle to address it. Once they understand the need to be protected, they often do not know what to do, where to turn or how much it will cost to get help. Further, even when formed properly, small businesses often fail to comply with ongoing compliance requirements, thereby reintroducing personal liability or facing significant financial and operational risk. Per the U.S. Chamber of Commerce Small Business Index (Q4 2025), 44% of small businesses say that compliance requirements make it harder to grow their business. Our solutions aim to simplify these complex legal and regulatory tasks, remove friction, and enable small business owners to focus on running and growing their businesses.

We aim to service a broad range of small business owners, from first-time formers to seasoned small business owners. We provide a mix of transaction and subscription offerings relevant for new and existing small businesses to solve their legal, compliance and business management needs. Our services range from technology-enabled do-it-yourself, or DIY, offerings to emerging full-service do-it-for-me, or DIFM, solutions led by concierge managers and attorneys.

Our small business customers' initial purchase is typically a business formation product that streamlines the process of starting a business. After business formation, we aim to deepen our relationship with our customers by providing ongoing legal, compliance and business management support throughout the lifecycle of their business. For example, our customers can purchase a legal advisory subscription to receive additional legal support for their small business needs, subscribe to our compliance concierge offering for complete management of business compliance requirements, or complete a one-time transaction to register their company name and/or logo as a trademark. The recurring revenue gained through subscription services and additional purchases from existing customers during the lifecycle of their business allows us to increase customer lifetime value. For the year ended December 31, 2025, approximately 65% of our revenue was derived from subscriptions.

See below under " Our Products and Services " for additional information regarding our transaction products and subscription offerings.

We believe we earn our customers' trust and drive significant organic traffic through our brand name recognition and reputation. Our small business customers' initial purchase is typically a business formation product that streamlines the process of starting a business. As of December 31, 2025, we had formed over 5.0 million businesses since our inception. Our position at business formation gives us unparalleled knowledge of our customers' needs, oftentimes prior to the business being operational or discoverable by other service providers. We leverage this valuable knowledge and our position as a small business' first advisor to introduce our customers to the most relevant business solutions to help them manage other aspects of their business.

We are also beginning to expand our customer funnel to reach current small business owners who are not yet a part of the LegalZoom ecosystem. As of June 30, 2025, there were approximately 36 million U.S. existing small businesses who were required to remain compliant with federal and state laws in order to remain operational and we can help them mitigate the risk, cost and time invested in managing these requirements.

Our Platform, Experts and Human Support

As more businesses are created, the need for a trusted legal and compliance partner only grows, and we believe that our combination of technology and human assistance helps our customers stay compliant, protected, and confident over time.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-23_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-23_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-23_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-23_item7_mdna.md, 10-K_2026-02-23_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
