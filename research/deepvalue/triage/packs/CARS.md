# Triage pack — CARS · Cars.com Inc.

_Generated 2026-09-04 14:13 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CARS · **Name:** Cars.com Inc.
- **CIK:** 0001683606
- **SIC:** 7374 — Services-Computer Processing & Data Preparation
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CARS

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Cars.com Inc.
- **CIK:** 1,683,606 · **SIC:** 7374 (Services-Computer Processing & Data Preparation) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 11.79 |
| mktcap | $631.2M |
| ev | $1.0B |
| ev_ebit | 17.3x |
| fcf | $147.4M |
| fcf_yield | 23.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.6% |
| net_debt | $413.8M |
| net_debt_ebit | 6.9x |
| cash | $33.3M |
| ltd | $447.1M |
| equity | $443.6M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $723.2M |
| revenue_prior | $719.2M |
| rev_growth | 0.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $60.2M |
| net_income | $20.1M |
| cfo | $151.6M |
| capex | $4.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -12.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 53,532,714 |
| shares_py | 61,445,496 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -8.5% |
| r6m | 40.4% |
| off_52w_high | -14.5% |
| adv20 | $6.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.91 |
| r_ev_ebit | 0.52 |
| r_roic | 0.53 |
| r_rev_growth | 0.36 |
| r_buyback | 0.96 |
| score | 0.66 |

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
| rank | 93 |

**Screen rationale:** top-quartile FCF yield 23.3%; buying back stock -12.9%


## 3. Share count trend

- Shares outstanding: **53,532,714** (CY2026Q2I) vs **61,445,496** prior year (CY2025Q2I)
- Change: **-12.9%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 1,995 sh / $15,082 vs sells 152,580 sh / $1,615,796 -> net $-1,600,714 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: Ross Jenell bought 1,995 sh @ $7.56 ($15,082) on 2026-03-13.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 1, sales 4).

| code | rows |
|---|---|
| A | 8 |
| P | 1 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Cars.com Reports Second Quarter 2026 Results'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (cars-ex99_1.htm)

Cars.com Reports Second Quarter 2026 Results

Delivered expected revenue growth and strong profitability, underpinned by focused strategy with highest Marketplace revenue growth in five years

•
Revenue grew to $179.9 million, up 1% year-over-year and in line with guidance

•
Net income increased to $14.3 million, up 103% year-over-year

•
Adjusted EBITDA grew to $53.0 million, up 4% year-over-year; Adjusted EBITDA margin of 29.4%, outperformed guidance range of 28% to 29% margin

•
Share repurchases totaled 3.7 million shares for $37 million; year-to-date share repurchases totaled 6.2 million shares for $57 million and are on pace to 2026 target of $90 million

CHICAGO, August 6, 2026 -- Cars.com Inc. (NYSE: CARS), a trusted audience-powered and data-driven technology platform that simplifies buying and selling cars, today released its financial results for the second quarter ended June 30, 2026.

"We delivered revenue and profitability growth in the second quarter while making steady progress on our Marketplace-focused strategy. Deliberate prioritization of Marketplace product, processes, and organizational improvements drove Marketplace revenue growth to its highest level since 2021, more than offsetting the expected decline in OEM revenue. New product launches, such as Dealer Verified Listings, as well as stronger customer value delivery through more precise audience targeting, are encouraging signals. Looking ahead, we will deploy these learnings and operational drivers across our ecosystem to deliver sustainable long-term growth and value creation," said Tobias Hartmann, Chief Executive Officer of Cars.com, Inc.

Financial Highlights

(in thousands, except per share data) | Quarter Ended June 30,
2026 | 2025 | Change %
Revenue | $ 179,934 | $ 178,739 | 1%
Net income | 14,263 | 7,009 | 103%
Adjusted net income | 28,699 | 26,412 | 9%
Adjusted EBITDA | 52,981 | 50,898 | 4%
Net income per diluted share | 0.25 | 0.11 | 127%
Adjusted net income per diluted share | 0.51 | 0.41 | 22%

Key Metrics and Operational Highlights

(in millions, except dealer data) | Quarter Ended
June 30, 2026 | March 31, 2026 | June 30, 2025 | Change % Q/Q | Change % Y/Y
Average Monthly Unique Visitors | 22.8 | 25.8 | 26.6 | (12%) | (14%)
Traffic ("Visits") | 143.0 | 159.6 | 162.0 | (10%) | (12%)
Monthly Average Revenue Per Dealer ("ARPD") | $ 2,500 | $ 2,473 | $ 2,435 | 1% | 3%
Dealer Customers | 19,343 | 19,390 | 19,412 | NM | NM

NM = Not meaningful

•
Marketplace revenue grew over 7% Y/Y and represents the fastest quarterly growth rate since 2021.

•
Dealer count declined slightly Y/Y, reflecting lower Solutions adoption that was partially offset by Marketplace strength; Marketplace dealer customers grew 2% Y/Y, reaching four consecutive quarters of Y/Y subscriber growth.

•
Traffic and UV performance reflects a deliberate strategic shift to value delivery, which produced year-to-date growth in lead volume.

•
Dealer Verified Listings feature launched on marketplace, adding inspection and pricing insights onto vehicle listings.

Q2 2026 Results

Revenue for the second quarter was $179.9 million, up 1% year-over-year. Subscription-based Dealer revenue of $163.3 million was up 3% year-over-year, primarily driven by improved Marketplace value delivery and dealer count, partially offset by a decline in media products. OEM and National revenue of $13.6 million was down 18% year-over-year, consistent with previously communicated expectations of OEM advertising.

Total operating expenses for the second quarter were $152.1 million compared to $163.5 million in the prior year period, down 7% year-over-year. Lower depreciation and amortization was the largest driver of the year-over-year decline, though expenses were broadly down and reflective of improving operating leverage across the business and a partial quarter of efficiencies associated with April cost reduction activities. Adjusted operating expenses were $144.3 million, down 6% year-over-year, driven by the aforementioned factors.

Net income for the second quarter was $14.3 million, or $0.25 per diluted share, compared to $7.0 million, or $0.11 per diluted share, in the year-ago period. The change in Net income is primarily attributable to improved operating income. Adjusted net income for the second quarter was $28.7 million, or $0.51 per diluted share, compared to $26.4 million, or $0.41 per diluted share a year ago.

Adjusted EBITDA for the second quarter was $53.0 million, or 29.4% of revenue, compared to $50.9 million, or 28.5% of revenue in the year-ago period. Adjusted EBITDA grew 4% year-over-year, demonstrating operating leverage against revenue growth.

Cash Flow and Balance Sheet

Net cash provided by operating activities for the six-month period ended June 30, 2026 was $55.6 million, compared to $55.7 million in the prior year. Free cash flow for the six-month period ended June 30, 2026 totaled $43.5 million, compared to $41.8 million in the prior year.

Total debt outstanding was $450.0 million as of June 30, 2026. Total liquidity as of June 30, 2026 was $333.3 million, which is defined as Cash and cash equivalents of $33.3 million and revolver capacity of $300.0 million.

Share Repurchase

The Company repurchased 3.7 million shares of common stock for $37 million in the second quarter ended June 30, 2026, and 6.2 million shares of common stock for $57 million year-to-date in 2026. The Company's 2026 share repurchase target remains $90 million, reflecting its commitment to returning capital to stockholders. Shares repurchased and retired year-to-date through June 30, 2026 represent over 10% of the Company's common shares outstanding as of prior year end.

As of June 30, 2026, approximately $116.6 million remains available under the current share repurchase authorization, which expires in February 2028.

"Second quarter financial performance was anchored by strong Marketplace growth, coupled with improved operating leverage and Adjusted EBITDA margin outperformance. We also continued to return significant capital to stockholders, and are pacing comfortably to our $90 million share repurchase target for 2026. Looking ahead, we remain focused on efficient and disciplined growth to create long-term value for stakeholders," said Sonia Jain, Chief Financial Officer of Cars.com, Inc.

Outlook

Third Quarter 2026

•
Revenue is expected to be flat to up 2% year-over-year, driven by continued Dealer revenue growth and Marketplace improvement. OEM and National revenue is expected to reflect ongoing pressure in OEM advertising investment.

•
Adjusted EBITDA margin is expected to be between 28.5% and 29.5%, reflecting continued operating efficiencies and cost savings.

Full Year 2026

The Company reaffirms its full year 2026 guidance:

•
Revenue is expected to be flat to up 2% year-over-year

•
Adjusted EBITDA margin is expected to be between 29.0% to 30.0%

Q2 2026 Earnings Call

As previously announced, management will hold a conference call and webcast today at 8:00 a.m. CT. This webcast may be accessed at the Cars.com Investor Relations website, investor.cars.com. An archive of the webcast will be available at investor.cars.com following the conclusion of the call.

About Cars Commerce

Cars.com Inc. (NYSE:CARS) is a trusted audience-powered and data-driven technology platform that simplifies buying and selling cars. The flagship Cars.com marketplace connects millions of consumers to dealerships across the U.S., powering the car buying experience with artificial intelligence ("AI") shopping tools and comprehensive vehicle reviews and content. Our interconnected ecosystem of products enables dealers and OEMs to sell more cars by efficiently leveraging our marketplace, dealer websites, trade and appraisal tools, and proprietary in-market media solutions. Learn more at www.carscommerce.inc.

Non-GAAP Financial Measures

This earnings release discusses Adjusted EBITDA, Adjusted EBITDA margin, Adjusted net (loss) income, Free Cash Flow and Adjusted Operating Expenses. These financial measures are not prepared in accordance with generally accepted accounting principles in the United States ("GAAP"). These financial measures are presented as supplemental measures of operating performance because the Company believes they provide meaningful information regarding the Company's performance and provide a basis to compare operating results between periods. In addition, the Company uses Adjusted EBITDA as a measure for determining incentive compensation targets. Adjusted EBITDA also is used as a performance measure under the Company's credit agreement and includes adjustments such as the items defined below and other further adjustments, which are defined in the credit agreement. These non-GAAP financial measures are frequently used by the Company's lenders, securities analysts, investors and other interested parties to evaluate companies in the Company's industry.

While a reconciliation of non-GAAP measures to corresponding GAAP measures is not available on a forward-looking basis without unreasonable effort due to, as applicable, the timing, amount, valuation and number of future employee equity awards and the uncertainty relating to the timing, frequency, and effect of acquisitions and the significance of the resulting transaction-related expenses, the Company has

provided a reconciliation of non-GAAP financial measures to their most directly comparable financial measure prepared in accordance with GAAP in this earnings release, see "Non-GAAP Reconciliations" below.

Other companies may define or calculate these measures differently, limiting their usefulness as comparative measures. Because of these limitations, non-GAAP financial measures should not be considered in isolation or as substitutes for performance measures calculated in accordance with GAAP. Definitions of these non-GAAP financial measures and reconciliations to the most directly comparable GAAP financial measures are presented in the tables below.

The Company defines Adjusted EBITDA as net income (loss) before (1) interest expense, net, (2) income tax (benefit) expense, (3) depreciation, (4) amortization of intangible assets, (5) stock-based compensation expense, (6) unrealized mark-to-market adjustments and cash transactions related to derivative instruments, (7) unrealized foreign currency exchange gains and losses, and (8) certain other items, such as transaction-related items, severance, transformation and other exit costs and write-off and impairments of goodwill, intangible assets and other long-lived assets.

Transaction-related items result from actual or potential transactions such as business combinations, mergers, acquisitions, dispositions, spin-offs, financing transactions, and other strategic transactions, including, without limitation, (1) transaction-related bonuses and (2) expenses for advisors and representatives such as investment bankers, consultants, attorneys and accounting firms. Transaction-related items may also include, without limitation, transition and integration costs such as retention bonuses and acquisition-related milestone payments to acquired employees, consulting, compensation and other incremental costs associated with integration projects, fair value changes to contingent considerations and amortization of deferred revenue related to the AccuTrade acquisition.

The Company defines Adjusted Net Income as GAAP net (loss) income excluding, net of their related tax effects: (1) amortization of intangible assets, (2) stock-based compensation expense, (3) unrealized mark-to-market adjustments and cash transactions related to derivative instruments, (4) unrealized foreign currency exchange gains and losses, and (5) certain other items, such as transaction-related costs, severance, transformation and other exit costs and write-off and impairments of goodwill, intangible assets and other long-lived assets.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview of Results

Year Ended December 31,
(In thousands) | 2025 | 2024 | 2023
Revenue | 723,239 | 719,152 | 689,183
Net income (1) | 20,052 | 48,188 | 118,442

(1)
Net income for the year ended December 31, 2023 is primarily related to the release of a significant portion of our valuation allowance for deferred tax assets that had been recorded as a result of the 2020 goodwill and indefinite-lived intangible asset impairments. For more information, see Note 12 (Income Taxes) to the accompanying Consolidated Financial Statements included in Part II, Item 8. "Financial Statements and Supplementary Data" of this Annual Report on Form 10-K.

Key Operating Metrics

We regularly review a number of key metrics to evaluate our business, measure our performance, identify trends affecting our business, formulate financial projections and make operating and strategic decisions. Key Operating Metrics are as follows (Traffic and Average Monthly Unique Visitors in thousands):

Year Ended December 31,
2025 | 2024 | % Change
Average Monthly Unique Visitors | 25,708 | 25,517 | 1 | %
Traffic | 627,141 | 627,556 | (0 | )%
Monthly Average Revenue Per Dealer - Annual | 2,460 | 2,483 | (1 | )%

December 31, 2025 | December 31, 2024 | YoY % Change | September 30, 2025 | QoQ % Change
Dealer Customers | 19,544 | 19,206 | 2 | % | 19,526 | 0 | %
Monthly Average Revenue Per Dealer - Quarterly | 2,472 | 2,475 | (0 | )% | 2,460 | 0 | %

Average Monthly Unique Visitors ("UVs") and Traffic. UVs and Traffic are fundamental to our business. They are indicative of our consumer reach and the level of engagement consumers have with our platform. Although our consumer engagement does not directly result in revenue, we believe our ability to reach in-market car shoppers is attractive to our dealers, OEMs and national customers and a primary reason they do business with us. We believe we have achieved audience scale as measured by UVs and Traffic. Traffic is driven by a combination of UVs visiting our properties, repeat visitation and engagement. We monetize impressions, clicks and other connections that result from traffic to our site via our products and services.

We define UVs in a given month as the number of distinct visitors that engage with our platform during that month. Visitors are identified upon first visit to an individual Cars.com property on an individual device/browser combination or installation of one of our mobile apps on an individual device. If a visitor accesses more than one of our web properties or apps or uses more than one device or browser, each of those unique property/browser/app/device combinations counts toward the number of UVs. Traffic is defined as the number of

visits to Cars.com desktop and mobile properties (responsive sites and mobile apps). We measure UVs and Traffic via RudderStack. These metrics do not include traffic to Dealer Inspire, D2C Media or DealerClub websites.

UVs increased 1% year-over-year and Traffic remained flat year-over-year for the year ended December 31, 2025, reflecting the impacts of tariff-motivated consumer demand at the beginning of the year and tactical improvements in the marketing mix throughout the year, partially offset by depressed consumer demand due to the federal government shutdown at the end of the year.

Dealer Customers . Dealer Customers represent dealerships using our products as of the end of each reporting period. Each physical or virtual dealership location is counted separately, whether it is a single-location proprietorship or part of a large, consolidated dealer group. Multi-franchise dealerships at a single location are counted as one dealer. Dealer Customer metrics do not include DealerClub.

Dealer Customers increased 2% from December 31, 2024, primarily due to an increase in marketplace customers. Dealer Customers remained flat from September 30, 2025.

Monthly Average Revenue Per Dealer ("ARPD"). We believe that our ability to grow ARPD is an indicator of the value proposition of our platform. We define ARPD as Dealer revenue, excluding digital advertising services and DealerClub, during the period divided by the monthly average number of Dealer Customers during the same period.

For the annual period of 2025, ARPD decreased 1% compared to the annual period 2024, primarily due to changes in our customer and product mix.

For the three months ended December 31, 2025, ARPD remained flat compared to the three months ended December 31, 2024, primarily due to marketplace repackaging, offset by changes in our customer and product mix.

For the three months ended December 31, 2025, ARPD remained flat compared to the three months ended September 30, 2025, primarily due to changes in our customer and product mix.

Factors Affecting Our Performance. Our business is impacted by changes in the larger automotive ecosystem, including supply and demand for new and used vehicle inventory, global supply chain and information systems disruptions, semiconductor and raw material shortages, vehicle acquisition cost, vehicle retail prices, the rate of electric vehicle adoption, employee retention and changes related to automotive advertising, among other macroeconomic factors including the political environment, inflationary and affordability pressures, tariffs and prevailing interest rates. Changes in vehicle sales volumes in the United States and Canada also influence OEMs' and dealerships' willingness to increase investments in marketing spend and technology solutions and could impact our pricing strategies and/or revenue mix.

Our long-term success will depend in part on our ability to attract and engage an in-market audience, to grow inventory supply and our dealer customers, to expand our relationship with dealers through greater adoption of our product offering, to transform our OEM relationships and to create operating leverage. We believe our core strategic strengths, including our Cars.com brand, growing high-quality audience and suite of digital solutions for dealers and OEMs, including AI-based tools, will assist us as we navigate a rapidly changing automotive environment.

Results of Operations

Year Ended December 31, 2025 Compared to Year Ended December 31, 2024

(In thousands, except percentages) | 2025 | 2024 | $ Change | % Change
Revenue:
Dealer | 644,053 | 640,722 | 3,331 | 1 | %
OEM and National | 65,305 | 65,894 | (589 | (1 | )%
Other | 13,881 | 12,536 | 1,345 | 11 | %
Total revenue | 723,239 | 719,152 | 4,087 | 1 | %
Operating expenses:
Cost of revenue and operations | 123,328 | 124,332 | (1,004 | (1 | )%
Product and technology | 117,330 | 117,875 | (545 | (0 | )%
Marketing and sales | 239,365 | 232,280 | 7,085 | 3 | %
General and administrative | 91,124 | 83,985 | 7,139 | 9 | %
Depreciation and amortization | 91,842 | 107,182 | (15,340 | (14 | )%
Total operating expenses | 662,989 | 665,654 | (2,665 | (0 | )%
Operating income | 60,250 | 53,498 | 6,752 | 13 | %
Nonoperating expense:
Interest expense, net | (30,382 | (32,197 | 1,815 | (6 | )%
Other income, net | 4,438 | 40,562 | (36,124 | (89 | )%
Total nonoperating (expense) income, net | (25,944 | 8,365 | (34,309 | ***
Income before income taxes | 34,306 | 61,863 | (27,557 | (45 | )%
Income tax expense | 14,254 | 13,675 | 579 | 4 | %
Net income | 20,052 | 48,188 | (28,136 | (58 | )%

*** Not meaningful

Dealer revenue . Dealer revenue is typically subscription-oriented and consists of marketplace, digital experience, including website solutions, trade and appraisal and media products sold to dealer customers. Dealer revenue is our largest revenue stream, representing 89% of total revenue for both the years ended December 31, 2025 and 2024. Dealer revenue increased $3.3 million or 1%, primarily due to continued growth in solutions, partially offset by declines in marketplace and media, as a result of lower average dealer count during the first half of 2025 and changes in our customer mix.

OEM and National revenue . OEM and National revenue largely consists of media solutions products, including display advertising and other solutions sold to OEMs, advertising agencies, automotive dealer associations and auto adjacent businesses, including insurance companies. OEM and National revenue represented 9% of total revenue for both the years ended December 31, 2025 and 2024. OEM and National revenue decreased $0.6 million or 1%, which we believe is primarily due to shifts in spending by OEM partners.

Other revenue. Other revenue primarily consists of revenue related to vehicle listing data sold to third parties. Other revenue represented 2% of total revenue for both the years ended December 31, 2025 and 2024. Other revenue increased $1.3 million or 11%.

Cost of revenue and operations . Cost of revenue and operations expense primarily consists of costs related to processing dealer vehicle inventory, product fulfillment and compensation and severance costs for the product fulfillment and customer service teams. Cost of revenue and operations expense represented 17% of total revenue for both the years ended December 31, 2025 and 2024. Cost of revenue and operations decreased $1.0 million or 1%, primarily due to lower compensation expense, partially offset by higher third-party costs associated with certain products driven by slight shifts in product mix.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business. Cars.com Inc. (NYSE:CARS) is a trusted audience-powered and data-driven technology platform that simplifies buying and selling cars. The flagship Cars.com marketplace connects millions of consumers to dealerships across the U.S., powering the car buying experience with artificial intelligence ("AI") shopping tools and comprehensive vehicle reviews and content. Our interconnected ecosystem of products enables dealers and OEMs to sell more cars by efficiently leveraging our marketplace, dealer websites, trade and appraisal tools and proprietary in-market media solutions. Learn more at www.carscommerce.inc.

Our premier automotive marketplace, Cars.com, empowers shoppers with the data, resources and digital tools they need to make informed buying decisions and seamlessly connect with automotive retailers. We also equip dealerships and OEMs with innovative solutions and data-driven intelligence to better reach and influence our 26 million average monthly shoppers. Not only does our marketplace drive ready-to-buy customers to the dealership, we believe our interconnected ecosystem of products also allows dealerships to operate more efficiently by facilitating a faster and easier car buying and selling experience.

The strength of our products and solutions has attracted approximately 19,500 franchise and independent dealer customers across the U.S. and Canada to our platform. Approximately 80% of our dealer customers subscribe to either the Cars.com marketplace or the marketplace and additional interconnected solutions, with our remaining customers subscribing to standalone digital website solutions. In addition, substantially all OEMs selling vehicles in the U.S. and Canada do business with us today.

For Consumers. Buying a car is one of life's most significant and researched decisions. Consumers are challenged with makes, models and trim-levels, opaque, yet negotiable prices, and gaps in the online-to-offline shopping experience, all of which add complexity to an often overwhelming decision-making process. Shoppers desire a more streamlined, simplified and trustworthy automotive retail experience. We help car shoppers cut through the noise with AI-powered features designed to move them confidently from search to signature.

We believe our marketplace functions as a definitive resource for car shoppers. We are known for the depth and scale of our listings and reviews, as evidenced by our over 4.6 million monthly unique VINs and over 16 million consumer reviews as of December 31, 2025. In addition, our expert editorial content, including news and research publications, aid shoppers in their purchase journey. We also allow consumers to better understand cost of ownership from the convenience of their home with financing tools and vehicle trade-in values. Overall, our consumer experience is focused on reducing friction and improving speed to purchase through pricing, comparison shopping, research and communication tools that empower shoppers.

For Customers. Our platform provides local dealers, OEMs, dealer groups and auto-adjacent companies a variety of digital and media solutions to improve their marketing and operational efficiency. Dealers and OEMs particularly value our marketplace for the opportunity to connect with our in-market audience of 26 million average monthly users in 2025. We complement our marketplace products with digital solutions, including websites and trade and appraisal technology, in-market media solutions. For example, U.S. website customers that also have a marketplace subscription see approximately 45% more connections to their website, in addition to

the associated marketplace leads they receive, as compared to those without marketplace. Importantly, we believe that many of the tools we have built for consumers, particularly those that support trade-in valuation, benefit our dealer customers and OEMs by enhancing consumer trust and reducing points of friction that can often arise in the purchase journey.

Industry Dynamics. As an audience-driven technology company, we are focused on helping our customers, primarily automotive dealerships, drive profitable vehicle sales. Consumer expectations on their digital purchase journey have only increased. As a result, some dealers seek to invest more in their websites and technology solutions to drive operational efficiency, while supporting shoppers in their preferred purchase channels (i.e., online, in person or both). We believe we are the first truly integrated marketplace-centric platform, providing a comprehensive suite of sales-oriented products and solutions that support dealers' local retail operations.

Products. Our interconnected product suite is organized around four core capabilities: Marketplace, Digital Experience, Media Solutions and Trade & Appraisal.

•
Marketplace. Central to our platform is Cars.com, the most recognized automotive marketplace brand, which we believe serves a critical role as a trusted and neutral third-party marketplace connecting consumers, dealers and OEMs to drive automotive retail at scale. We enabled dealers and OEMs to professionally merchandise their inventory to our 26 million average monthly shoppers in 2025. Importantly, the majority of our traffic comes to us organically so that we provide our customers with a truly complementary and unduplicated audience. We offer dealers packages that include reputation management technology and digital financing tools, with additional functionality like media solutions, for our upper-tier packages. Notably, dealers purchasing these upper-tier packages typically experience a double-digit improvement in leads per listing. We continue to add new consumer features, such as Carson TM , to our marketplace. Carson TM , which launched in 2025, provides consumers with an AI-powered natural language search experience. Shoppers utilizing Carson TM generate two times more leads than other shoppers.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
