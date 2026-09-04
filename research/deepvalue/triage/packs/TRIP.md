# Triage pack — TRIP · TripAdvisor, Inc.

_Generated 2026-09-04 15:12 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TRIP · **Name:** TripAdvisor, Inc.
- **CIK:** 0001526520
- **SIC:** 7370 — Services-Computer Programming, Data Processing, Etc.
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TRIP

**Fetcher warnings for this ticker:** 10-K 2026-02-13: heading split missed Item 1A - Risk Factors; 10-Q 2026-08-06: MD&A heading not detected, wrote truncated full text

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** TripAdvisor, Inc.
- **CIK:** 1,526,520 · **SIC:** 7370 (Services-Computer Programming, Data Processing, Etc.) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 9.29 |
| mktcap | $1.1B |
| ev | $1.1B |
| ev_ebit | 13.3x |
| fcf | $163.0M |
| fcf_yield | 15.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 9.9% |
| net_debt | -$27.3M |
| net_debt_ebit | -0.3x |
| cash | $843.2M |
| ltd | $815.9M |
| equity | $662.5M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.9B |
| revenue_prior | $1.8B |
| rev_growth | 3.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $80.0M |
| net_income | $40.0M |
| cfo | $245.0M |
| capex | $82.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 117,199,342 |
| shares_py | 116,133,591 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -18.6% |
| r6m | -11.5% |
| off_52w_high | -51.5% |
| adv20 | $32.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.82 |
| r_ev_ebit | 0.65 |
| r_roic | 0.70 |
| r_rev_growth | 0.45 |
| r_buyback | 0.47 |
| score | 0.62 |

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
| rank | 119 |

**Screen rationale:** top-quartile FCF yield 15.0%; net cash


## 3. Share count trend

- Shares outstanding: **117,199,342** (CY2026Q2I) vs **116,133,591** prior year (CY2025Q2I)
- Change: **0.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-03** — Item 1.01 (Entry Into a Definitive Material Agreement): As previously disclosed, on June 14, 2026, Tripadvisor, Inc., a Nevada corporation (the " Company "), entered into a put option agreement (the " Put Option Agreement ") with American Express Travel Related Services Company, Inc., a New York corporation ("...
- **2026-06-15** — Item 1.01 (Entry Into a Definitive Material Agreement): On June 14, 2026, TripAdvisor, Inc., a Nevada corporation (the " Company "), entered into a put option agreement (the " Put Option Agreement ") with American Express Travel Related Services Company, Inc., a New York corporation (" Buyer ").

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 7,908 sh / $118,620 -> net $-118,620 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 59 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 2 |
| F | 18 |
| M | 38 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Tripadvisor Reports Second Quarter 2026 Financial Results'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (trip-ex99_1.htm)

Tripadvisor Reports Second Quarter 2026 Financial Results

NEEDHAM, MA, August 6, 2026 — Tripadvisor, Inc. (NASDAQ: TRIP) today announced financial results for the second quarter ended June 30, 2026.

"We delivered second quarter results in-line with our expectations, while making progress in our strategy to focus on experiences and simplify our portfolio," said Chief Executive Officer Matt Goldberg. "We continue to focus on additional opportunities across the business to enhance the value of our assets and catalyze shareholder value. The sale of TheFork unlocks significant value, adds flexibility for capital allocation, and marks another step reshaping the Company around experiences – the largest, most durable growth category in travel."

"Our second quarter performance reflected consistent execution in an attractive experiences marketplace, even with the backdrop of a fluctuating macro environment," said Chief Financial Officer Mike Noonan. "Our confidence in the Group's operational and financial trajectory remains firm as we prioritize our experiences-led strategy. We remain intently focused on initiatives that strengthen our product, marketing, and supply flywheel to drive long-term growth and margin expansion."

Pending Sale of TheFork

As previously announced on June 14, 2026, the Company entered into a put option agreement for the sale of TheFork, its European online restaurant and management platform, to American Express Travel Related Services Company, Inc. for $700.0 million in cash, subject to certain adjustments. Pursuant to the agreement, American Express Travel provided an irrevocable commitment to acquire TheFork. On August 1, 2026, following the completion of the required consultation process with the relevant French Works Council on July 30, 2026, the Company exercised the put option. On August 2, 2026, the Company entered into an Equity Purchase Agreement with American Express Travel to sell TheFork. The closing of the transaction remains subject to certain customary closing conditions, including regulatory approvals. The sale of TheFork is expected to be completed by the end of 2026.

As a result of the pending transaction, the financial results of TheFork are classified as discontinued operations, and are no longer a reportable segment. The Company's remaining segments, Experiences and Hotels and Other, are classified as continuing operations. As such, for all periods presented in this release and unless otherwise noted, all amounts, percentages, and any discussion in this press release reflect the results from these continuing operations, while TheFork is presented on a discontinued operations basis. All prior period segment disclosure information in this press release has been recast to conform to the current reporting structure.

Financial Highlights for Continuing Operations

•
Revenue for the second quarter was $441.9 million, a decline of 7% year-over-year.

•
Net income for the second quarter was $22.8 million, or $0.19 diluted EPS.

•
Non-GAAP net income for the second quarter was $41.0 million, or $0.35 diluted EPS.

•
Adjusted EBITDA for the second quarter was $76.4 million, or 17.3% of revenue.

Second Quarter 2026 Financial Summary for Continuing Operations

Three months ended June 30,
(In millions, except percentages and per share amounts) | 2026 | 2025 | % Change
Total Revenue | 441.9 | 476.0 | (7 | )%
Experiences | 278.6 | 270.5 | 3 | %
Hotels and Other | 163.3 | 205.5 | (21 | )%
GAAP Net Income (Loss) from continuing operations | 22.8 | 36.5 | (38 | )%
Total Adjusted EBITDA from continuing operations (1) | 76.4 | 97.2 | (21 | )%
Experiences | 30.8 | 37.8 | (19 | )%
Hotels and Other | 45.6 | 59.4 | (23 | )%
Non-GAAP Net Income (Loss) from continuing operations (1) | 41.0 | 56.0 | (27 | )%
Diluted Net Income (Loss) per Share from continuing operations:
GAAP | 0.19 | 0.28 | (32 | )%
Non-GAAP (1) | 0.35 | 0.43 | (19 | )%
Cash flow from operating activities from continuing operations | 141.2 | 203.7 | (31 | )%
Free cash flow from continuing operations (1) | 129.8 | 183.4 | (29 | )%

(1)
"Total Adjusted EBITDA from continuing operations," "Non-GAAP Net Income (Loss) from continuing operations," "Non-GAAP Diluted Net Income (Loss) per Share from continuing operations," and "Free cash flow from continuing operations" are non-GAAP measures as defined by the U.S. Securities and Exchange Commission (the "SEC"). Please refer to " Non-GAAP Financial Measures " below for definitions and explanations of these non-GAAP financial measures, as well as tabular reconciliations to the most directly comparable GAAP financial measures.

Cost performance – Total costs and expenses from continuing operations were $404.1 million for the second quarter, a decrease of 3% year-over-year, primarily driven by the following:

For the Three Months Ended June 30,
2026 | 2025 | % Change
Cost of sales | 31.0 | 36.5 | (15 | )%
Marketing | 215.4 | 207.4 | 4 | %
Personnel | 99.2 | 125.5 | (21 | )%
Technology | 21.6 | 21.5 | 0 | %
General and administrative | 14.5 | 9.5 | 53 | %
Percentage of Total Revenue
Cost of sales | 7.0 | % | 7.7 | %
Marketing | 48.7 | % | 43.6 | %
Personnel | 22.4 | % | 26.4 | %
Technology | 4.9 | % | 4.5 | %
General and administrative | 3.3 | % | 2.0 | %

Cash & Liquidity – As of June 30, 2026, the Company had $843.2 million of cash and cash equivalents from continuing operations, a decrease of $134.8 million from December 31, 2025. As previously announced, on April 1, 2026, the Company used $345.4 million of its existing cash and cash equivalents to fully repay its 2026 Senior Notes due on April 1, 2026.

Segments Highlights

Experiences

•
Revenue for the second quarter was $278.6 million, reflecting year-over-year growth of 3%. Excluding the impact of currency exchange rate fluctuations, year-over-year growth was approximately 2%.

•
The number of experience bookings was approximately 6.5 million during the second quarter, an increase of approximately 5%, when compared to the same period in 2025. Experience bookings include a single tour, activity,

or attraction that can be purchased through Viator's platform for one or several travelers, prior to adjustments such as date changes, refunds, or cancellations.

•
Gross bookings value ("GBV") reached approximately $1.4 billion during the second quarter, reflecting year-over-year growth of approximately 3%. GBV is reported at the time of booking and is gross of cancellations, whereas revenue is recorded at the time of the experience and is net of cancellations.

•
Adjusted EBITDA for the second quarter was $30.8 million, or 11.1% of revenue, compared to adjusted EBITDA in the same period a year ago of $37.8 million, or 14.0% of revenue.

Hotels and Other

•
Revenue for the second quarter was $163.3 million, reflecting a year-over-year decline of 21%.

o
Hotels revenue for the second quarter was $117.9 million, reflecting a year-over-year decline of 23%.

o
Media and advertising revenue for the second quarter was $31.2 million, reflecting a year-over-year decline of 12%.

o
Other revenue for the second quarter was $14.2 million, reflecting a year-over-year decline of 20%.

•
Adjusted EBITDA for the second quarter was $45.6 million, or 27.9% of revenue, compared to adjusted EBITDA in the same period a year ago of $59.4 million, or 28.9% of revenue.

Restructuring and Related Reorganization Action

As previously disclosed, during the fourth quarter of 2025, the Company initiated a series of cost savings actions to support the Company's positioning as an experiences-led and AI-enabled company. As a result of these actions, the Company incurred pre-tax restructuring and other related reorganization costs of $3.9 million during the second quarter of 2026, which consisted of employee severance and related benefits, primarily in our Hotels and Other segment.

Conference Call

Tripadvisor will host a conference call later this morning, August 6, 2026, at 8:30 a.m., Eastern Time, to discuss the Company's second quarter 2026 financial results, which may include forward-looking information about Tripadvisor's business. Investors and other interested parties may also go to the Investor Relations section of Tripadvisor's website at http://ir.tripadvisor.com for a live webcast of the conference call. A replay of the conference call will be available on Tripadvisor's website for three months.

SELECTED FINANCIAL INFORMATION

Tripadvisor, Inc.

Unaudited Condensed Consolidated Statements of Operations

(in millions, except per share amounts)

Three Months Ended | Six Months Ended
June 30, 2026 | June 30, 2025 | June 30, 2026 | June 30, 2025
Revenue | 441.9 | 476.0 | 767.7 | 828.5
Costs and expenses:
Cost of sales (exclusive of depreciation and amortization as shown separately below) | 31.0 | 36.5 | 58.0 | 58.6
Marketing | 215.4 | 207.4 | 376.6 | 360.8
Personnel (including stock-based compensation of $16.8, $26.2, $35.3 and $51.5, respectively) | 99.2 | 125.5 | 204.7 | 248.0
Technology | 21.6 | 21.5 | 43.2 | 41.0
General and administrative | 14.5 | 9.5 | 25.7 | 23.5
Depreciation and amortization | 18.5 | 17.7 | 37.6 | 34.8
Restructuring and other related reorganization costs | 3.9 | — | 6.9 | 9.3
Total costs and expenses | 404.1 | 418.1 | 752.7 | 776.0
Operating income (loss) | 37.8 | 57.9 | 15.0 | 52.5
Other income (expense):
Interest expense | (15.0 | (17.3 | (30.8 | (29.1
Interest income | 5.3 | 10.1 | 13.0 | 20.0
Other income (expense), net | — | (5.8 | 1.5 | (9.1
Total other income (expense), net | (9.7 | (13.0 | (16.3 | (18.2
Income (loss) before income taxes | 28.1 | 44.9 | (1.3 | 34.3
(Provision) benefit for income taxes | (5.3 | (8.4 | (6.5 | (0.6
Net income (loss) from continuing operations | 22.8 | 36.5 | (7.8 | 33.7
Net income (loss) from discontinued operations, net of tax | (0.4 | (0.5 | (2.2 | (8.7
Net income (loss) | 22.4 | 36.0 | (10.0 | 25.0
Net income (loss) per share attributable to common stockholders from continuing operations:
Basic | 0.20 | 0.29 | (0.07 | 0.25
Diluted | 0.19 | 0.28 | (0.07 | 0.25
Net income (loss) per share attributable to common stockholders from discontinued operations:
Basic | — | — | (0.02 | (0.07
Diluted | — | — | (0.02 | (0.06
Net income (loss) per share attributable to common stockholders:
Basic | 0.19 | 0.29 | (0.09 | 0.19
Diluted | 0.19 | 0.28 | (0.09 | 0.19
Numerator used to compute net income (loss) per share from continuing operations attributable to common stockholders:
Basic | 22.8 | 36.5 | (7.8 | 33.7
Diluted | 22.8 | 36.8 | (7.8 | 34.4
Numerator used to compute net income (loss) per share attributable to common stockholders:
Basic | 22.4 | 36.0 | (10.0 | 25.0
Diluted | 22.4 | 36.3 | (10.0 | 25.7
Weighted average common shares outstanding:
Basic | 116.7 | 124.9 | 116.1 | 133.0
Diluted | 117.9 | 130.2 | 116.1 | 138.7

Tripadvisor, Inc.

Unaudited Condensed Consolidated Balance Sheets

(in millions, except number of shares and per share amounts)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-13_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

The Tripadvisor group (the "Group") is a portfolio of global online platforms purpose-built to connect travelers with experiences, accommodations, restaurants and other relevant travel destination points of interest ("POIs"). Our mission is to be the world's most trusted source for travel and experiences.

We offer travelers the ability to search, discover, book, and review experiences, hotels, and restaurants seamlessly through our two-sided marketplaces across three primary consumer-facing brands: Viator, Tripadvisor, and TheFork. Tripadvisor also plays a unique role in broader travel planning and guidance, offering authentic traveler-submitted reviews and content, travel planning tools and related technology to instill confidence for travelers in every part of their travel journey.

The Company measures its financial performance within the following reportable segments: Experiences, Hotels and Other, and TheFork. The Company's strategy is focused on growing and scaling its Experiences and TheFork marketplaces, which we believe represents an attractive long-term value creation opportunity, while optimizing its legacy offerings within the Hotels and Other segment for profitability.

The Experiences segment includes both Viator and Tripadvisor points-of-sale. Viator is a pure-play experiences online travel agency ("OTA"), offering an online global marketplace focused on merchandising bookable experiences to travelers that typically have relatively higher purchase intent either pre-destination or in-destination. Tripadvisor is an online global travel guidance platform that also merchandises experiences to its audience, which more commonly serves travelers in the discovery and planning phases. The Hotels and Other segment primarily consists of the Tripadvisor hotel and restaurant guidance platform, which includes hotel

metasearch, and related advertising offerings primarily for hotels and restaurants. TheFork segment operates an online dining marketplace by enabling diners to discover and book reservations with restaurants in Europe.

The Group's globally recognized brands and extensive user-generated content ("UGC") support traveler search, discovery, and planning, which in-turn generates high-intent demand for its experiences and dining marketplace offerings as well for commercial partners in the hotels category and advertising opportunities for endemic and non-endemic advertisers. In turn, clickstream and behavioral data reflecting traveler intent, transactional data from its experiences and dining marketplaces, UGC, and structured and unstructured data related to millions of POIs attractions, and destinations enhance the customer experience through product enhancements and personalization, reinforcing the discovery and engagement loop over time. In addition, the breadth, depth, and scale of first party data is uniquely valuable in the Company's pursuit to innovate in the application of artificial intelligence ("AI") for travel and experiences discovery, planning, and booking.

Trends

The online travel industry in which we operate is large, highly dynamic and competitive. We describe below current trends affecting our overall business and segments, including opportunities, but also uncertainties that may impact our ability to execute on our objectives and strategies.

Our Experiences and TheFork businesses are two-sided online marketplaces, which have exhibited consistent revenue growth and improving profitability. The Company's consolidated revenue and adjusted EBITDA continue to shift more towards its marketplace businesses, as shown in our segment financial information. Importantly, as of the year ended December 31, 2025, the Experiences and TheFork segments represented approximately 60% of the Company's consolidated revenue and 35% of our consolidated adjusted EBITDA. As the Company continues to execute on its growth strategies and invest in these marketplace businesses, we expect these trends to continue to grow in the future. We expect this will result in less exposure to our media-based and click-based advertising offerings.

In particular, our highest strategic priority is to extend our position as a leader in the experiences category. The global experiences market is large, growing, highly fragmented, and under penetrated, with the vast majority of bookings still occurring through traditional offline sources. We expect to benefit from ongoing market tailwinds as consumers increasingly book experiences online and consumer behavior continues to allocate more discretionary spending to travel and experiences and away from physical goods. Likewise, the global restaurants category is also benefiting from increased online adoption by both consumers and restaurant partners, particularly in Europe. These trends present attractive growth opportunities for our business, as well as to many competitors. Given the competitive positioning of our businesses relative to the attractive growth prospects in the experiences and restaurant categories, we expect to continue to invest in these categories across Tripadvisor Group to continue growing revenue, operating scale, and market share for the long-term.

We generate a significant amount of direct traffic from search engines, including Google, through search engine optimization ("SEO") performance across all segments. We believe our SEO traffic acquisition performance has been negatively impacted by search engines changing their search result placement and underlying algorithms to increase the prominence of their own products in search results across our business. We believe that our Hotels and Other segment will continue to be impacted by these challenges and others, including AI overviews displacing top-ranked links, reduced click-through rates and a shift towards platform based non-traditional search.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Consolidated Results of Operations

In the fourth quarter of 2025, the Company announced the realignment of its operating model to support its long-term goals and strategic priorities. As a result, in consultation with our Chief Executive Officer, who is our Chief Operating Decision Maker ("CODM"), we evaluated our operations and updated our reportable segment information which the CODM regularly assesses to evaluate performance for operating decision-making purposes, including allocation of resources. The revised segment reporting structure includes the following reportable segments: (1) Experiences; (2) Hotels and Other; and (3) TheFork. This re-segmentation had no impact to TheFork segment. For further information, including the change in segments and principal revenue streams within these segments, refer to "Note 18: Segment and Geographic Information " in the notes to our consolidated financial statements in Item 8 of this Annual Report on Form 10-K. All prior period segment disclosure information has been recast to conform to the current reporting structure in this Form 10-K. This recast had no effect on our consolidated financial statements in any period.

A discussion regarding our financial condition and results of operations for fiscal year 2025 compared to fiscal year 2024 is presented below. A discussion regarding our financial condition and results of operations for fiscal year 2024 compared to fiscal year 2023 can be found in Part II, Item 7. "Management's Discussion and Analysis of Financial Condition and Results of Operations" of our Annual Report on Form 10-K for the year ended December 31, 2024, filed with the SEC on February 20, 2025, except for the discussions related to our new Experiences and Hotels and Other reportable segments as a result of our revised segment reporting structure, as noted above. We have included a discussion regarding our financial condition and results of operations for fiscal year 2024 compared to fiscal year 2023, where applicable, as we believe the changes in our Experiences and Hotels and Other reportable segments is a material change for investors to understand the financial condition, changes in financial conditions, and results of operations of these revised reportable segments.

Results of Operations

Selected Financial Data

(in millions, except percentages)

Year ended December 31, | % Change
2025 | 2024 | 2023 | 2025 vs. 2024 | 2024 vs. 2023
Revenue | 1,891.3 | 1,834.6 | 1,788.0 | 3 | % | 3 | %
Costs and expenses:
Cost of sales | 144.6 | 131.2 | 119.1 | 10 | % | 10 | %
Marketing | 791.4 | 728.6 | 705.2 | 9 | % | 3 | %
Personnel (including stock-based compensation of $107.8, $119.7, and $95.8) | 573.4 | 594.9 | 569.6 | (4 | )% | 4 | %
Technology | 98.7 | 91.3 | 80.0 | 8 | % | 14 | %
General and administrative | 67.9 | 90.5 | 79.1 | (25 | )% | 14 | %
Depreciation and amortization | 92.4 | 85.1 | 87.0 | 9 | % | (2 | )%
Restructuring and other related reorganization costs | 43.4 | 21.1 | 22.2 | 106 | % | (5 | )%
Total costs and expenses: | 1,811.8 | 1,742.7 | 1,662.2 | 4 | % | 5 | %
Operating income (loss) | 79.5 | 91.9 | 125.8 | (13 | )% | (27 | )%
Other income (expense):
Interest expense | (63.3 | (46.4 | (44.0 | 36 | % | 5 | %
Interest income | 39.9 | 48.6 | 47.5 | (18 | )% | 2 | %
Other income (expense), net | (11.4 | (7.4 | (4.1 | 54 | % | 80 | %
Total other income (expense), net | (34.8 | (5.2 | (0.6 | 569 | % | 767 | %
Income (loss) before income taxes | 44.7 | 86.7 | 125.2 | (48 | )% | (31 | )%
(Provision) benefit for income taxes | (4.9 | (81.8 | (114.8 | (94 | )% | (29 | )%
Net income (loss) | 39.8 | 4.9 | 10.4 | 712 | % | (53 | )%
Other financial data:
Adjusted EBITDA (1) | 318.7 | 338.5 | 334.0 | (6 | )% | 1 | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-13_item1_business.md)

Item 1. Business

Overview

The Tripadvisor group (the "Group") is a portfolio of global online platforms purpose-built to connect travelers with experiences, accommodations, restaurants and other relevant travel destination points of interest ("POIs"). Our mission is to be the world's most trusted source for travel and experiences.

We offer travelers the ability to search, discover, book, and review experiences, hotels, and restaurants seamlessly through our two-sided marketplaces across three primary consumer-facing brands: Viator, Tripadvisor, and TheFork. Tripadvisor also plays a unique role in broader travel planning and guidance, offering authentic traveler-submitted reviews and content, travel planning tools and related technology to instill confidence for travelers in every part of their travel journey.

The Company measures its financial performance within the following business segments: Experiences, Hotels and Other, and TheFork. The Company's strategy is focused on growing and scaling its Experiences and TheFork marketplaces, which we believe represents an attractive long-term value creation opportunity, while optimizing its legacy offerings within the Hotels and Other segment for profitability.

The Group's globally recognized brands and extensive user-generated content ("UGC") support traveler search, discovery, and planning, which in-turn generates high-intent demand for its experiences and dining marketplace offerings as well for commercial partners in the hotels category and advertising opportunities for endemic and non-endemic advertisers. In turn, clickstream and behavioral data reflecting traveler intent, transactional data from its experiences and dining marketplaces, UGC, and structured and unstructured data related to millions of POIs, attractions, and destinations enhance the customer experience through product enhancements and personalization, reinforcing the discovery and engagement loop over time. In addition, the breadth, depth, and scale of first party data is uniquely valuable in the Company's pursuit to innovate in the application of artificial intelligence ("AI") for travel and experiences discovery, planning, and booking.

The Company believes its portfolio of unique assets creates a compelling global travel platform for travelers, including:

•
Tripadvisor's content and branded platform for upper-funnel traveler intent for experiences, and Viator's content and branded platform for mid-and-lower funnel traveler intent for experiences. Both branded platforms leverage a shared global supply platform of more than 425,000 bookable experiences from 70,000 operators;

•
The trusted Tripadvisor brand within Hotels and Other travel categories to drive traveler discovery, intent, and data engine;

•
TheFork's recognized brand, content, relationships with more than 50,000 restaurants, and scaled diner community across 11 European countries; and

•
Integrated AI and machine learning capabilities serving as the connective layer for ongoing enhancements to traveler personalization, planning, and conversion.

Our Business Models

The Company measures its financial performance within the following business segments: Experiences, Hotels and Other, and TheFork. For additional information regarding our segments and the recent restructuring and related reorganization actions, please see Part II, Item 7 of this Annual Report on Form 10-K under the heading " Management's Discussion and Analysis of Financial Condition and Results of Operations—Recent Developments. "

The Experiences segment includes both Viator and Tripadvisor points-of-sale. Viator is a pure-play experiences online travel agency ("OTA"), offering an online global marketplace focused on merchandising bookable experiences to travelers that typically have relatively higher purchase intent either pre-destination or in-destination. Tripadvisor is an online global travel guidance platform that also merchandises experiences to its

audience, which more commonly serves travelers in the discovery and planning phases. Both brands leverage Viator's centralized supply platform that supports operator onboarding, operator inventory management, bookings, payments, fraud prevention, and customer support. This architecture enables the Company to serve different customer intents across brands while benefiting from shared scale, data, and marketplace economics. In addition to its owned and operated platforms (Viator and Tripadvisor), the Company also syndicates its experiences supply to other third-party endemic and non-endemic demand partners. Demand from these partners largely reaches travelers from regions outside our core geographic markets and, therefore, drives incremental traveler demand. The Experiences segment revenue is generated primarily through commission-based transactions on completed experiences offerings.

The Hotels and Other segment primarily consists of the Tripadvisor hotel and restaurant guidance platform, which includes hotel metasearch, and related advertising offerings primarily for hotels and restaurants and, to a lesser extent, cruises through our branded subsidiary Cruise Critic. Hotels and Other revenue is generated primarily through click-based advertising including cost-per-click ("CPC") and cost-per-acquisition ("CPA"); media advertising revenue is primarily generated through impression-based advertising ("CPM"). This segment primarily provides travelers with tools to research, compare, and plan travel while delivering qualified traffic to partners and advertisers primarily across the experiences, hotels, restaurants, and cruise travel categories.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-13_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-13_item7_mdna.md, 10-K_2026-02-13_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
