# Triage pack — NXH · NEIGHBORHOOD INTELLIGENCE, INC.

_Generated 2026-09-05 03:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** NXH · **Name:** NEIGHBORHOOD INTELLIGENCE, INC.
- **CIK:** 0001130713
- **SIC:** 5961 — Retail-Catalog & Mail-Order Houses
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq, Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/NXH

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** NEIGHBORHOOD INTELLIGENCE, INC.
- **CIK:** 1,130,713 · **SIC:** 5961 (Retail-Catalog & Mail-Order Houses) · **Exchange:** Nasdaq,NYSE,Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 3.89 |
| mktcap | $370.8M |
| ev | $284.8M |
| ev_ebit | n/a |
| fcf | -$64.1M |
| fcf_yield | -17.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -37.6% |
| net_debt | -$86.0M |
| net_debt_ebit | n/a |
| cash | $99.5M |
| ltd | $13.5M |
| equity | $214.8M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.0B |
| revenue_prior | $1.4B |
| rev_growth | -25.1% |
| rev_growth_note | share count +66.1% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$61.2M |
| net_income | -$258.8M |
| cfo | -$56.7M |
| capex | $7.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 66.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 95,330,379 |
| shares_py | 57,405,976 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -46.0% |
| r6m | -25.3% |
| off_52w_high | -67.9% |
| adv20 | $9.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.05 |
| r_ev_ebit | 0.00 |
| r_roic | 0.02 |
| r_rev_growth | 0.01 |
| r_buyback | 0.02 |
| score | 0.02 |

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
| rank | 485 |

**Screen rationale:** share count +66.1% yoy — growth may be acquisition/issuance-driven, not organic


## 3. Share count trend

- Shares outstanding: **95,330,379** (CY2026Q2I) vs **57,405,976** prior year (CY2025Q2I)
- Change: **66.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +66.1% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-13** — Item 5.02 (officer / director change or comp arrangement): On August 8, 2026, Jill Windrum was appointed as the Company's Chief Accounting Officer and Deputy Chief Financial Officer, effective August 31 , 2026.
- **2026-08-05** — Item 5.02 (officer / director change or comp arrangement): On August 4, 2026, the board of directors (the "Board") of Bed Bath & Beyond, Inc. (the "Company") approved the adoption of the Bed Bath &

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 89,476 sh / $406,828 vs sells 9,943 sh / $63,436 -> net $343,392 (BUYING).
Distinct insiders buying (code P): 3. Largest buy: LEMONIS MARCUS bought 43,382 sh @ $4.67 ($202,594) on 2026-08-05.

Form 4 filings parsed: 12; transaction rows: 42 (open-market buys 4, sales 1).

| code | rows |
|---|---|
| A | 11 |
| F | 6 |
| M | 20 |
| P | 4 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'NASHVILLE, Tennessee - August 4, 2026 - Bed Bath & Beyond, Inc. (NYSE:'; skipped 5 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex991q226pressrelease.htm)

NASHVILLE, Tennessee - August 4, 2026 - Bed Bath & Beyond, Inc. (NYSE:BBBY), owner of Bed Bath & Beyond, Overstock, buybuy BABY, the Kirkland's and Kirkland's Home brands, and more recently The Container Store, Elfa, Closet Works, and SFV Services, as well as a blockchain asset portfolio, today reported financial results for the second quarter ended June 30, 2026.

Second Quarter 2026 Highlights

Net revenue was $361 million, an increase of 28.0% year-over-year, marking the Company's second consecutive quarter of year-over-year revenue growth following nineteen quarters of decline. Growth reflects continued strength in the Company's base online marketplace business, improved assortment, the realization of investments in the customer experience, and the inclusion of The Brand House Collective (owner of the Kirkland's and Kirkland's Home brands), which was acquired during the quarter.

Active customers increased to 6.4 million, up 47% year-over-year, and orders delivered increased to 2.8 million, up 117% year-over-year, reflecting growth in the base business and the inclusion of acquired brands. Orders per active customer increased to 1.79 from 1.32 in the prior year period, an increase of 36%.

Gross profit was $97 million, or 26.8% of net revenue.

Sales & Marketing expense was $43 million, or 11.9% of net revenue, an improvement of 160 basis points year-over-year.

Technology and general and administrative expense was $82 million compared to $37 million in the prior year period, reflecting the expansion of the Company's physical retail footprint, including store labor, occupancy, distribution, and other operating costs associated with The Brand House Collective.

Net loss was $39 million, compared to a net loss of $19 million in the prior year period. The current period includes $21 million of special items, primarily acquisition-related costs, restructuring costs, and non-cash store-closure impairments.

Adjusted EBITDA (non-GAAP) was ($12) million, compared to ($8) million in the prior year period.

Cash, cash equivalents, and restricted cash totaled $126 million at quarter end.

Strategic Progress

"Our second quarter results show that the transformation of this business is taking hold," said Marcus Lemonis, Executive Chairman and Chief Executive Officer. "After eight quarters of meaningful operating improvement, we have now delivered two consecutive quarters of revenue growth following nineteen quarters in the other direction. Two quarters is not a victory and we have no intention of treating it as one, but it is hard evidence that the direction of this business has changed. We are growing revenue and active customers while continuing to take cost out of the business and operate more efficiently, and that combination matters."

"Our omnichannel retail brands remain the front door to the customer," Lemonis continued. "We are seeing better engagement, stronger conversion, and more frequent orders per customer, which tells us the customer is responding to the investments we have made."

During and following the quarter, the Company continued to assemble the capabilities that support its strategy. The acquisition of The Brand House Collective closed during the quarter, and the acquisition of The Container Store, Elfa, and Closet Works closed on July 8, 2026. The Company also announced definitive agreements to acquire Fathom Holdings Inc. and F9 Brands Inc. in June and July 2026, respectively. As signed transactions close and fold into the Company's results, the Company expects continued revenue growth in its base online marketplace business, together with growth in total revenue and active customer count, over the coming quarters.

"We are acquiring capabilities and active customers while eliminating infrastructure we no longer need," Lemonis continued. "As revenue ramps, we believe that over the next twelve months we can remove more than fifty million dollars of annualized cost by bringing our businesses together onto one platform, eliminating non-performing assets, consolidating disciplines and shared resources, improving the cost of our supply chain infrastructure, and eliminating or consolidating duplicative third-party services, software agreements, and locations. We would not call it cost cutting; we would call it finishing the merger."

Corporate Transformation to Neighborhood Intelligence

In a shareholder letter issued today and available at https://investors.beyond.com, the Company announced that its parent company is becoming Neighborhood Intelligence, that it will begin trading on Nasdaq under the ticker NXH, with its last day of trading on the NYSE on August 14, 2026 and its first day of trading on Nasdaq on August 17, 2026, and that it will relocate its corporate headquarters to Nashville, Tennessee. The letter describes the Company's organization around three interconnected pillars: Omni-Channel Retail, which helps customers create a home they love; Home Services, which helps them improve, maintain, and protect it; and Home Ownership, which brings together the financial, transactional, and advisory capabilities that support one of life's most important investments. Together, the pillars are designed to create an ecosystem that serves customers before they purchase a home, while they own it, as they improve it, and when they ultimately decide to sell or transfer it, in support of a single mandate: to make homeownership simpler and more affordable while creating long-term value for shareholders.

The Company's consumer brands remain at the center of its customer relationships. Neighborhood Intelligence is the intelligence layer that connects them, making each brand smarter, more connected, and more valuable while preserving the unique identity and trust customers already know. The letter also describes the Company's proprietary agent, Norm™, which the Company is actively building today, with its first customer-facing version planned for later this year.

Earnings Webcast and Replay Information

Bed Bath & Beyond will host a webcast to discuss its second quarter 2026 financial results and its strategic vision, key initiatives, and provide business updates on Tuesday, August 4, 2026, at 4:30 p.m. ET. To access the live webcast, visit https://investors.beyond.com . Questions may be emailed in advance of the call to ir@beyond.com .

A replay of the webcast will be available at https://investors.beyond.com shortly after the live event has ended.

On August 4, 2026, in connection with the release of financial results, the Company posted an updated presentation in the "Events & Presentation" portion of its investor relations website at https://investors.beyond.com .

About Bed Bath & Beyond

Bed Bath & Beyond, Inc. (NYSE:BBBY), (and after August 14, trading on NASDAQ: NXH on August 17) is an omni channel-focused retailer with an affinity model that owns or has ownership interests in various retail brands, offering a comprehensive array of products and services that enable its customers to enhance everyday life through quality, style, and value. The Company currently owns Bed Bath & Beyond, Overstock, buybuy BABY, and Kirkland's and Kirkland's Home, and now SFV Services and The Container Store, as well as other related brands and websites and a blockchain asset portfolio inclusive of tZERO, GrainChain, and other assets. The Company regularly posts information and updates on its Newsroom and Investor Relations pages on its website, bedbathandbeyond.com.

Contact Information Investor Relations ir@beyond.com pr@beyond.com

Bed Bath & Beyond, Inc. Consolidated Balance Sheets (Unaudited) (in thousands, except per share data)
June 30, 2026 | December 31, 2025
Assets
Current assets:
Cash and cash equivalents | 99,485 | 175,295
Restricted cash | 26,891 | 26,924
Accounts receivable, net | 29,797 | 20,829
Inventories | 52,157 | 5,162
Prepaids and other current assets | 29,037 | 11,905
Total current assets | 237,367 | 240,115
Property and equipment, net | 42,876 | 13,712
Intangible assets, net | 46,419 | 45,140
Goodwill | 101,946 | 6,160
Equity securities | 55,928 | 66,641
Operating lease right-of-use assets | 115,796 | 5,156
Other long-term assets, net | 33,819 | 48,554
Total assets | 634,151 | 425,478
Liabilities and Stockholders' Equity
Current liabilities:
Accounts payable | 140,533 | 89,992
Accrued liabilities | 68,251 | 51,297
Unearned revenue | 46,818 | 34,429
Operating lease liabilities, current | 33,565 | 928
Short-term debt, net | 23,000 | 15,500
Total current liabilities | 312,167 | 192,146
Long-term debt, net | 13,455 | —
Operating lease liabilities, non-current | 83,068 | 5,643
Other long-term liabilities | 10,373 | 9,745
Total liabilities | 419,063 | 207,534
Stockholders' equity:
Preferred stock, $0.0001 par value, authorized shares - 5,000, issued and outstanding - none | — | —
Common stock, $0.0001 par value, authorized shares - 200,000
Issued shares - 89,604 and 76,358
Outstanding shares - 81,760 and 68,863 | 9 | 8
Additional paid-in capital | 1,294,141 | 1,239,338
Accumulated deficit | (898,606) | (842,711)
Accumulated other comprehensive loss | (2,574) | (2,574)
Treasury stock at cost - 7,844 and 7,495 | (178,206) | (176,478)
Equity attributable to stockholders of Bed Bath & Beyond, Inc. | 214,764 | 217,583
Equity attributable to noncontrolling interests | 324 | 361
Total stockholders' equity | 215,088 | 217,944
Total liabilities and stockholders' equity | 634,151 | 425,478

Bed Bath & Beyond, Inc. Consolidated Statements of Operations (Unaudited) (in thousands, except per share data)
Three months ended June 30, | Six months ended June 30,
2026 | 2025 | 2026 | 2025
Net revenue | 361,159 | 282,251 | 608,914 | 513,999
Cost of goods sold | 264,478 | 215,282 | 453,035 | 388,898
Gross profit | 96,681 | 66,969 | 155,879 | 125,101
Operating expenses
Sales and marketing | 43,108 | 38,209 | 75,418 | 69,499
Technology | 24,334 | 23,221 | 45,548 | 49,939
General and administrative | 57,527 | 14,088 | 72,390 | 28,402
Customer service and merchant fees | 11,579 | 9,331 | 20,597 | 18,688
Other operating income, net 1 | 3,016 | (5,454) | 3,016 | (5,790)
Total operating expenses | 139,564 | 79,395 | 216,969 | 160,738
Operating loss | (42,883) | (12,426) | (61,090) | (35,637)
Interest income, net | 750 | 889 | 2,479 | 1,651
Other expense, net 1 | 120 | (7,489) | 449 | (24,758)
Loss before income taxes | (42,013) | (19,026) | (58,162) | (58,744)
Provision (benefit) for income taxes | (2,516) | 287 | (2,267) | 481
Net loss | (39,497) | (19,313) | (55,895) | (59,225)
Net loss per share of common stock:
Basic | (0.53) | (0.34) | (0.78) | (1.07)
Diluted | (0.53) | (0.34) | (0.78) | (1.07)
Weighted average shares of common stock outstanding:
Basic | 74,308 | 57,503 | 71,693 | 55,593
Diluted | 74,308 | 57,503 | 71,693 | 55,593

1 The amounts in prior period columns have been revised to conform to current period's presentation for the correction of immaterial errors.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-24_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are an e-commerce-focused retailer with an affinity model that owns or has ownership interests in various brands, offering a comprehensive array of products and services that enable its customers to enhance everyday life through quality, style, and value. In addition, we also offer an increasing number of add-on services across our platforms, including warranties, shipping insurance, and installation services. Our customer engagement and retention are bolstered by our welcome rewards+ membership program, enhancing the overall value proposition for our customers. We currently own Bed Bath & Beyond, Overstock, and buybuy BABY, among other brands. As used herein, "Bed Bath & Beyond," "the Company," "we," "our" and similar terms include Bed Bath & Beyond, Inc. and its controlled subsidiaries, unless the context indicates otherwise.

Through our Bed Bath & Beyond brand, we provide an extensive array of home-related products tailored specifically for our target customers - consumers who seek comprehensive support throughout their shopping journey, aspiring to discover quality, stylish products at competitive prices that align with their budget requirements. We regularly refresh our product assortment to reflect the evolving preferences of our customers and aim to stay aligned with current trends. The mission of this brand is to achieve category-leading ownership of four distinct rooms of the home: the bedroom, the bathroom, the kitchen, and the patio, and our goal is for our assortment to include not only core legacy categories like bedding and kitchenware, but also adjacent categories like bedroom and outdoor furniture and rugs. Furniture across all rooms continues to play a critical role in our strategy. Leveraging an asset-light supply chain, direct shipping is offered to customers from both our suppliers and third-party logistics providers.

Bed Bath & Beyond's strategic priorities include curating stylish, high-quality assortments to make product selection intuitive and affordable, in addition to enhancing offerings with trusted aspirational brands. We transform the customer experience by building trust, creating life-stage experiences, and consistently delivering inspiration, quality, and value.

Through our Overstock brand, we aim to provide a wide array of quality goods at discounted prices, and a treasure hunt-like experience for our target customers - consumers who are highly engaged, very accustomed to purchasing online, and actively seeking great deals. The mission of this brand is to delight our customers by offering them deals on products they will love. Our product assortment includes home categories such as indoor and outdoor furniture, rugs, décor, and lighting, as well as lifestyle categories such as jewelry and watches, apparel and accessories, and designer shoes and handbags.

The buybuy BABY brand acquisition allows us to reunite two traditionally related brands, Bed Bath & Beyond and buybuy BABY, and support our customers through key life stage shopping moments.

In August 2025, we changed our corporate name from Beyond, Inc. to Bed Bath & Beyond, Inc. and changed our ticker symbol from "BYON" to "BBBY".

Merger Agreement

On November 24, 2025, we entered in an Agreement and Plan of Merger (the "Merger Agreement"), by and among the Company, Knight Merger Sub II, Inc., a wholly owned subsidiary of the Company, and TBHC, pursuant to which, subject to the terms and conditions set forth therein, Merger Sub will merge with and into TBHC (the "Merger"), with TBHC surviving such Merger as a wholly owned subsidiary of the Company.

Under the Merger Agreement, at the effective time of the Merger (the "Effective Time"), each share of common stock, no par value, of TBHC (the "TBHC Common Stock") issued and outstanding immediately prior to the Effective Time (other than treasury shares and any shares of TBHC Common Stock held directly by the Company or Merger Sub) will be converted

into the right to receive 0.1993 shares (the "Exchange Ratio") of a fully paid and non-assessable share of common stock, par value $0.0001 per share, of the Company (the "Company Common Stock") and, if applicable, cash in lieu of fractional shares, subject to any applicable withholding.

At the Effective Time, (i) each award of TBHC restricted share units ("TBHC RSU") that is outstanding as of immediately prior to the Effective Time will automatically fully vest and be converted into the right to receive, without interest and subject to applicable withholding taxes, (A) a number of shares of Company Common Stock equal to the number of shares of TBHC subject to the TBHC RSU multiplied by the Exchange Ratio and (B) if applicable, cash in lieu of fractional shares, and (ii) each option to purchase TBHC Common Stock ("TBHC Option") that is outstanding as of immediately prior to the Effective Time will be automatically converted into the right to receive, without interest and subject to applicable withholding taxes, (A) a number of shares of Company Common Stock equal to the Net Option Share Amount (as defined in the Merger Agreement) applicable to the TBHC Option multiplied by the Exchange Ratio and (B) if applicable, cash in lieu of fractional shares.

For additional information on the proposed merger, see Item 8 of Part II, "Financial Statements and Supplementary Data"—Note 25—Subsequent Events.

Executive Commentary

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Our Annual Report on Form 10-K for the year ended December 31, 2024, filed on February 25, 2025, includes a discussion and analysis of our year-over-year changes, financial condition, and results of operations for the years ended December 31, 2024 and 2023 in Item 7 of Part II, "Management's Discussion and Analysis of Financial Condition and Results of Operations."

Net revenue, costs of goods sold, gross profit and gross margin

The following table summarizes our net revenue, costs of goods sold, gross profit and gross margin for the years ended December 31, 2025 and 2024 (in thousands):

Year ended December 31,
2025 | 2024
Net revenue | 1,044,616 | 1,394,964
Cost of goods sold
Product costs and other cost of goods sold | 787,094 | 1,104,800
Gross profit | 257,522 | 290,164
Year-over-year percentage change
Net revenue | (25.1) | %
Gross profit | (11.2) | %
Percent of net revenue
Cost of goods sold
Product costs and other cost of goods sold | 75.3 | % | 79.2 | %
Gross margin | 24.7 | % | 20.8 | %

Revenue for the year ended December 31, 2025, was $1,044.6 million, compared to $1,395.0 million for the year ended December 31, 2024, representing a decrease of $350.3 million or 25%. The decrease was primarily due to a 30% decrease in the number of orders delivered, which contributed $439.6 million of the revenue decline, partially offset by an 8% or $14.22 increase in average order value, which resulted in a revenue increase of approximately $89.3 million. The decrease in orders delivered was driven by a decline in website visits influenced in part by a reduction in overall sales and marketing spend as we focus on improving more efficient traffic channels and refine our assortment as well as a shift in consumer spending preferences and macroeconomic factors impacting consumer sentiment and the home furnishings industry. The increase in average order value was largely driven by orders mixing into categories with higher average unit retail price.

Estimate of unearned product revenue on undelivered product

Our revenue related to merchandise sales is recognized upon delivery to our customers. As we ship high volumes of packages through multiple carriers, it is not practical for us to track the actual delivery date of each shipment. Therefore, we use estimates to determine which shipments are delivered and, therefore, recognized as revenue at the end of the period. Our delivery date estimates are based on average shipping transit times. We review and update our estimates on a quarterly basis based on our actual transit time experience. However, actual shipping times may differ from our estimates, which can be further impacted by uncertainty, volatility, and any disruption to our carriers caused by certain macroeconomic conditions, such as supply chain challenges, inflation, rising interest rates, climate and weather events, or geopolitical events.

The following table shows the effect that hypothetical changes in the estimate of average shipping transit times would have had on the reported amount of revenue and income before taxes (in thousands):

Year Ended December 31, 2025
Change in the Estimate of Average Transit Times (Days) | Increase (Decrease) Revenue | Increase (Decrease) Income Before Income Taxes
2 | (3,629) | (594)
1 | (2,354) | (385)
As reported | As reported | As reported
(1) | 5,614 | 919
(2) | 8,590 | 1,406

Gross profit and gross margin

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-24_item1_business.md)

ITEM 1. BUSINESS

The following description of our business contains forward-looking statements relating to future events or our future financial or operating performance that involve risks and uncertainties, as set forth above under "Special Note Regarding Forward-Looking Statements." Our actual results could differ materially from those anticipated in these forward-looking statements as a result of certain factors described in this Annual Report, including those set forth under "Special Cautionary Note Regarding Forward-Looking Statements" Item 1A under the heading "Risk Factors," or elsewhere in this Annual Report.

Introduction

Bed Bath & Beyond, Inc., is an e-commerce-focused retailer with an affinity model that owns or has ownership interests in various brands, offering a comprehensive array of products and services that enable its customers to enhance everyday life through quality, style, and value. We currently own Bed Bath & Beyond, Overstock, and buybuy BABY, among other brands. We strive to curate an exceptional online shopping experience. Our diversified portfolio of retail offerings allow us to offer a comprehensive array of products and add-on services, catering to customers in the United States. Our e-commerce platform, which is also accessible through our mobile apps, includes www.bedbathandbeyond.com and www.overstock.com, and is collectively referred to as the "Website." The Website is targeted at customers seeking a diverse array of top-tier, on-trend products at competitive prices. From furniture, bedding, and bath essentials to patio and outdoor furniture, area rugs, tabletop and cookware, décor, storage, jewelry, watches, and fashion – we offer an extensive range of products at a smart value. In addition to products, we also offer an increasing number of add-on services across our platforms, including warranties, shipping insurance, and installation services.

Our company, based in Murray, Utah, was founded as a Utah limited liability company in 1997, reorganized as a C corporation in the State of Utah in 1998, and reincorporated in Delaware in 2002. We launched our initial website in March 1999. In November 2023, we changed our corporate name from Overstock.com, Inc. to Beyond, Inc., and transferred the principal listing of our common stock from the Nasdaq Global Market to the New York Stock Exchange. In August 2025, we changed our corporate name from Beyond, Inc. to Bed Bath & Beyond, Inc. and changed our ticker symbol from "BYON" to "BBBY". Our common stock ceased trading under the ticker symbol "BYON" at the close of market August 28, 2025, and on August 29, 2025, our common stock began trading under the ticker symbol "BBBY" on the New York Stock Exchange. We will not distinguish between our prior and current corporate name and will refer to our current corporate name throughout this Annual Report on Form 10-K. As used herein, "Bed Bath & Beyond", "the Company", "we", "our" and similar terms include Bed Bath & Beyond, Inc. and its controlled subsidiaries, unless the context indicates otherwise.

Our Business

Our mission revolves around delivering an unparalleled shopping experience for products and services, tailored especially for our target audience – discerning consumers who seek seamless support in their search for high-quality, stylish products at competitive prices. Our commitment extends to providing a diverse range of offerings that cater to varied budget requirements.

In an ever-evolving market, our focus is on standing out in the online sphere by offering products and services for the home. We believe that our competitive edge lies in the following:

• Simplified Customer Experience: We prioritize an easy, user-friendly interface, emphasizing price, value, and quality. Our extensive product range is delivered in a personalized format, accessible seamlessly through our mobile apps, and complemented by our dedicated customer service team.

• Cutting-edge Technologies: Our proprietary technologies and strategic technical alliances enhance the overall shopping experience, providing our customers with an intuitive and streamlined experience.

• Specialized Logistics: Our logistics capabilities are finely tuned to the demands of the furniture and home furnishings category, which we have honed over decades of e-commerce expertise.

• Strategic Partnerships: We foster long-term, mutually beneficial relationships with third-party manufacturers, distributors, and suppliers, collectively referred to as our "partners". This network forms the backbone of our supply chain, allowing us to pursue our goal of consistently meeting customer demands. We also partner with third parties to provide various financial products and services.

• Omni-Channel Relaunch: In addition to our partners, we've had a collaborative partnership with The Brand House Collective, Inc. (formerly known as Kirkland's, Inc.) ("TBHC"), and own approximately 40% of TBHC's common stock. In 2025, TBHC converted several Kirkland's Home stores and launched Bed Bath & Beyond brand stores

through an exclusive license with the Company to operate Bed Bath & Beyond neighborhood stores. Additionally, we've entered into a pending merger agreement with TBHC slated to close in the first half of 2026, that is intended to further enable the Company to bring back the omni-channel experience to our Bed Bath & Beyond and buybuy BABY customer base. In January 2025, we also entered into an asset purchase agreement with BBBY Acquisition Co. LLC to acquire certain rights in the buybuy BABY brand, as well as assets, data, information and content related to the associated buybuy BABY website.

• Customer Loyalty Programs: Our customer engagement and retention are bolstered by our welcome rewards+ membership program and private label credit card, enhancing the overall value proposition for our customers.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-24_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-24_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-24_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-02-24_item7_mdna.md, 10-K_2026-02-24_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
