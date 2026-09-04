# Triage pack — KRT · Karat Packaging Inc.

_Generated 2026-09-04 14:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** KRT · **Name:** Karat Packaging Inc.
- **CIK:** 0001758021
- **SIC:** 3089 — Plastics Products, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/KRT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Karat Packaging Inc.
- **CIK:** 1,758,021 · **SIC:** 3089 (Plastics Products, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 47.06 |
| mktcap | $938.0M |
| ev | $899.6M |
| ev_ebit | 21.7x |
| fcf | $33.1M |
| fcf_yield | 3.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 25.5% |
| net_debt | -$38.4M |
| net_debt_ebit | -0.9x |
| cash | $38.4M |
| ltd | $0.00 |
| equity | $166.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $467.7M |
| revenue_prior | $422.6M |
| rev_growth | 10.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $41.4M |
| net_income | $31.5M |
| cfo | $33.8M |
| capex | $756k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 19,931,721 |
| shares_py | 20,092,755 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 79.0% |
| r6m | 106.6% |
| off_52w_high | -5.5% |
| adv20 | $7.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.40 |
| r_ev_ebit | 0.40 |
| r_roic | 0.92 |
| r_rev_growth | 0.67 |
| r_buyback | 0.74 |
| score | 0.68 |

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
| rank | 75 |

**Screen rationale:** high ROIC 25.5%; debt data missing (net cash unverified); 12-1 momentum 79.0%


## 3. Share count trend

- Shares outstanding: **19,931,721** (CY2026Q2I) vs **20,092,755** prior year (CY2025Q2I)
- Change: **-0.8%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 6,500 sh / $308,485 -> net $-308,485 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 22 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 3 |
| F | 3 |
| M | 14 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Karat Packaging Reports Second Quarter 2026 Financial Results'; skipped 10 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (krt-20260806xpressrelease.htm)

Karat Packaging Reports Second Quarter 2026 Financial Results

— Online Growth Fuels Record Sales and Solid Profitability —

CHINO, Calif., August 6, 2026 – Karat Packaging Inc. (Nasdaq: KRT) ("Karat Packaging" or the "Company"), a specialty distributor and manufacturer of environmentally friendly, disposable foodservice products and related items, today announced financial results for its second quarter ended June 30, 2026.

Second Quarter 2026 Highlights

• Record quarterly net sales of $136.3 million, up 9.9 percent, from $124.0 million in the prior-year quarter.

• International Emergency Economic Powers Act ("IEEPA") tariff refunds reduced costs of goods sold by $25.8 million, reversing IEEPA tariff costs absorbed in prior periods, and increased other income, net by $0.9 million, from interest received related to the refunds.

• Gross profit of $77.2 million, including contribution of $25.8 million from the IEEPA tariff refunds, up 57.1 percent, from $49.1 million in the prior-year quarter.

• Gross margin of 56.6 percent, including contribution of 1,890 basis points from the IEEPA tariff refunds, compared with 39.6 percent in the prior-year quarter.

• Net income of $29.6 million, including contribution of $20.2 million from the IEEPA tariff refunds, up 168.3 percent, from $11.1 million in the prior-year quarter.

• Net income margin of 21.8 percent, including contribution of 1,480 basis points from the IEEPA tariff refunds, versus 8.9 percent in the prior-year quarter.

• Adjusted EBITDA of $41.6 million, including contribution of $25.8 million from the IEEPA tariff refunds, versus $17.7 million in the prior-year quarter.

• Adjusted EBITDA margin of 30.5 percent, including contribution of 1,890 basis points from the IEEPA tariff refunds, versus 14.3 percent in the prior-year quarter.

Guidance

• Net sales for the 2026 third quarter expected to increase by low double-digits from the prior-year quarter.

• Gross margin for the 2026 third quarter expected to be within 35 to 37 percent, including insignificant IEEPA tariff refunds anticipated during the quarter.

• Adjusted EBITDA margin for the 2026 third quarter expected to be within 9 to 11 percent, including insignificant IEEPA tariff refunds anticipated during the quarter.

• Net sales for full-year 2026 expected to increase by low double-digits from the prior year.

• Gross margin for full-year 2026 expected to be in the low 40 percents, including IEEPA tariff refunds recorded during the first half of 2026.

• Adjusted EBITDA margin for full-year 2026 expected to be approximately mid-teens, including IEEPA tariff refunds recorded during the first half of 2026.

"We delivered record quarterly net sales of $136.3 million, driven by solid customer demand and accelerated momentum in our online business growth," said Alan Yu, Chief Executive Officer. "Our financial performance included a benefit from the IEEPA tariff refunds, which further contributed to strong reported profitability.

"We continue to experience encouraging momentum across the business and our sales pipeline is expanding. During the quarter, we added four new chain accounts and our online business grew 23.6 percent over the prior-year quarter, further strengthening our growth prospects. At the same time, we continue to execute plans to enhance operational efficiency and manage costs to support sustainable profitability.

"To support our long-term growth strategy, we are currently finalizing a lease for a 47,000-square-foot warehouse for a new distribution center in Orlando, Florida, which we expect to be operational by the third quarter of this year. The new facility is expected to enhance Karat's ability to better serve customers throughout the Southeast, improve fulfillment capabilities for our growing e-commerce business, reduce delivery times, and provide additional infrastructure to support future growth," Yu added.

Second Quarter 2026 Financial Results

Net sales for the 2026 second quarter increased 9.9 percent to $136.3 million, from $124.0 million in the prior-year quarter. The increase was primarily driven by $13.1 million in volume growth and product mix, as well as a $0.4 million favorable year-over-year pricing comparison, partially offset by a decrease of $1.1 million in shipping and logistics revenue.

Cost of goods sold for the 2026 second quarter decreased 21.0 percent to $59.1 million, from $74.9 million in the prior-year quarter. The decrease was primarily driven by IEEPA tariff refunds of $25.8 million, partially offset by higher product costs of $6.9 million, primarily due to increased sales volume and resin price, coupled with higher import costs, including duty and tariffs and ocean freight of $3.5 million, mainly due to a 4.3 percent increase in number of containers imported and an 8.9 percent increase in average container rate compared to the prior-year quarter.

Gross profit for the 2026 second quarter increased to $77.2 million, including contribution of $25.8 million from the IEEPA tariff refunds, from $49.1 million in the prior-year quarter. Gross margin was 56.6 percent in the 2026 second quarter, including contribution of 1,890 basis points from the IEEPA tariff refunds, compared with 39.6 percent in the prior-year quarter. Partially offsetting this benefit, product costs as a percentage of net sales increased to 49.2 percent from 48.5 percent, and import costs as a percentage of net sales increased to 11.1 percent from 9.5 percent compared to the prior-year quarter.

Operating expenses for the 2026 second quarter increased to $39.6 million, from $32.6 million in the prior-year quarter. The increase was primarily driven by $3.1 million in higher shipping and transportation costs due to increased shipping volume and shipping rate, $0.6 million higher online platform fees, and $0.5 million higher marketing expense due to a 23.6 percent online sales growth. Other increases included a $1.1 million increase in salaries and benefits, a $0.6 million increase in bad debt expense, and a $0.4 million increase in warehouse expense. Further, 2026 second quarter included a $0.1 million loss compared with a $0.3 million gain on disposal of machinery in the normal course of business in the prior-year quarter.

Other income, net for the 2026 second quarter was $1.4 million, compared with other expenses, net, of $2.0 million in the prior-year quarter. The increase in other income, net was mainly driven from a loss on foreign currency transactions of $0.1 million, compared to a loss of $2.9 million during the same period last year. In addition, interest income increased $0.5 million due to $0.9 million interest income related to IEEPA tariff refunds recognized in the 2026 second quarter, partially offset by a decrease of $0.4 million in interest income from investment in certificates of deposit compared to the prior-year quarter.

Net income for the 2026 second quarter increased 168.3 percent to $29.6 million, including contribution of $20.2 million from the IEEPA tariff refunds, from $11.1 million in the prior-year quarter. Net income margin was 21.8 percent in the 2026 second quarter, including contribution of 1,480 basis points from the IEEPA tariff refunds, compared with 8.9 percent in the prior-year quarter.

Net income attributable to Karat Packaging for the 2026 second quarter was $29.3 million, or $1.46 per diluted share, including contribution of 1.00 per share from the IEEPA tariff refunds, compared with $10.9 million in the prior-year quarter, or $0.54 per diluted share.

Adjusted EBITDA, a non-GAAP measure defined below, was $41.6 million for the 2026 second quarter, including contribution of $25.8 million from the IEEPA tariff refunds, compared with $17.7 million for the prior-year quarter. Adjusted EBITDA margin, a non-GAAP measure defined below, was 30.5 percent of net sales for the 2026 second quarter, including contribution of 1,890 basis points from the IEEPA tariff refunds, compared with 14.3 percent for the prior-year quarter.

Adjusted diluted earnings per common share, a non-GAAP measure defined below, was $1.48 per share for the 2026 second quarter, including contribution of $1.00 per share from the IEEPA tariff refunds, compared with $0.57 per share for the prior-year quarter.

Six-Month 2026 Financial Results

Net sales for the first half of 2026 increased 11.3 percent to $253.2 million, from $227.6 million in the same period last year. The increase was primarily due to an increase of $25.4 million in volume and change in product mix, as well as a $2.3 million favorable year-over-year pricing comparison, partially offset by a decrease of $2.0 million in shipping and logistics revenue.

Cost of goods sold for the first half of 2026 decreased 2.3 percent to $134.6 million, from $137.7 million in the same period last year, primarily due to IEEPA tariff refunds of $25.8 million in the first half of 2026. This decrease is partially offset by an increase of $12.1 million in product costs primarily driven by higher sales volume and resin price, and an increase of $10.7 million in import costs, including duty and tariffs and ocean freight, primarily as a result of higher import duty and tariffs.

Gross profit for the first half of 2026 increased 32.1 percent to $118.7 million, including contribution of $25.8 million from the IEEPA tariff refunds, from $89.9 million in the same period last year. Gross margin was 46.9 percent for the first half of 2026, including contribution of 1,020 basis points from the IEEPA tariff refunds, compared with 39.5 percent in the same period last year. Product costs as a percentage of net sales decreased to 48.8 percent from 48.9 percent, while import costs increased to 12.4 percent from 9.1 percent, compared to the same period of 2025.

Operating expenses for the first half of 2026 were $72.6 million, compared with $65.5 million in the same period last year. The increase was primarily driven by a $2.7 million increase in shipping and transportation costs due to higher shipping volume and increased shipping rate, as well as higher salaries and benefits, bad debt expense, warehouse expense, and marketing expenses. Further, the first half of 2026 included a $0.1 million loss compared to a $0.3 million gain on disposal of machinery in the normal course of business in the same period of 2025.

Other income, net for the first half of 2026 was $2.3 million, compared with other expenses, net, of $0.9 million in the same period last year. The increase in other income, net was mainly driven by a gain on foreign currency transactions of $0.2 million, compared to a loss of $2.6 million during the same period last year. In addition, interest income increased $0.2 million due to $0.9 million interest income related to IEEPA tariff refunds recognized in the first half of 2026, partially offset by a decrease of $0.7 million in interest income from investment in certificates of deposit compared to the same period of 2025.

Net income increased 105.9 percent to $36.8 million for the first half of 2026, including contribution of $20.2 million from the IEEPA tariff refunds, from $17.9 million in the same period last year. Net income margin was 14.5 percent in the first half of 2026, including a contribution of 800 basis points from the IEEPA tariff refunds, compared with 7.8 percent in the same period of 2025.

Net income attributable to Karat Packaging was $36.1 million, or $1.80 per diluted share, including contribution of 1.00 per share from the IEEPA tariff refunds, for the first half of 2026, compared with $17.3 million, or $0.86 per diluted share, in the same period of 2025.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-13_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a rapidly-growing and nimble distributor and manufacturer of disposable foodservice products and related items, including food and take-out containers, bags, boxes, tableware, cups, lids, cutlery, straws, specialty beverage ingredients, gloves, janitorial supplies, and other products. Our products are available in plastic, paper, biopolymer-based, and other compostable forms. We are a leader in product innovation, offering a growing line of environmentally-friendly products to our customers, who are increasingly focused on sustainability. We also offer customized solutions to our customers, including new product development, design, printing, and logistics services.

We operate our business strategically and with broad flexibility to provide both our large and small customers with the wide spectrum of products they need to successfully run and grow their businesses. We believe we have established ourselves as a differentiated and reliable provider of high-quality products relative to our competitors. Our operating model entails generating the majority of our revenue from the distribution of products sourced from a diversified global network, complemented by select manufacturing capabilities in the U.S., which allows us to provide customers with broad product choices and customized offerings with short lead times. This model provides us with the flexibility to adjust the mix of our product offering from import and manufacturing in evolving economic environments to drive operating efficiency and sustained margin expansion and ensure quality of our customer service and product availability during global supply chain disruptions. Starting in 2023 and continuing into 2025, in light of the rising domestic labor and other operating costs and dropping ocean freight rates, we executed a strategy to pivot into a more asset-light model by increasing imports and scaling back domestic manufacturing. Amidst the evolving tariff environment throughout 2025, we have placed our strategic emphasis on expanding and diversifying our global vendor network to enhance the resilience of our supply chain, minimize tariff impact on our operations and financial results, and maintain a strong margin profile and operating cash flows. We are prioritizing strong partnerships with reliable and cost-efficient sources and more favorable trade terms, negotiating additional vendor support, exploring opportunities to collaborate with vendors in new countries and geographies, while reallocating our own domestic production capabilities to optimize overall product margin.

We operate an approximately 500,000 square foot distribution center located in Rockwall, Texas, an approximately 300,000 square foot distribution center in Chino, California, and an approximately 76,000 square foot distribution center located in Kapolei, Hawaii. We have selected manufacturing capabilities in all of these facilities. In addition, we operate seven othe r distribution centers lo cated in Puyallup, Washington; Branchburg, New Jersey; Kapolei, Hawaii; Aurora, Illin ois; Mesa, Arizona; Sugar Land, Texas, and Chino, California. Our distribution centers are strategically located in proximity to major population centers, including the Los Angeles, New York, Chicago, Dallas, Houston, Seattle, Phoenix, Atlanta, and Honolulu metro areas. On October 17, 2025, we announced that Lollicup, our wholly-owned business operating subsidiary, relocated its headquarters to Rockwall, Texas, from Chino, California.

We manage and evaluate our operations in one reportable segment.

2025 Business Highlights and Trends

• We have strategically and swiftly realigned our global supply chain in 2025 against a backdrop of higher tariffs. We reduced purchases from China from approximately 22% of global sourcing in 2024 to approximately 15% in 2025, maintained purchases from Taiwan at approximately 50% of our global sourcing, and diversified sourcing to countries with more favorable trade conditions, including Malaysia and Vietnam, which in aggregate accounted for approximately 17% of our global sourcing in 2025 compared to 9% in 2024.

• We continued to expand our eco-friendly product offerings, contributing to meaningful sales growth. Sales from eco-friendly products as a percentage of total sales increased from 33.6% for the year ended December 31, 2024 to 34.1% for the year ended December 31, 2025. We started shipment on a newly-acquired paper bag contract with a chain account in the second half of 2025, growing paper bags sales from $7.9 million for the year ended December 31, 2024 to $13.7 million for the year ended December 31, 2025.

• We continued our transition to a more asset-light model by further scaling back manufacturing in the U.S. and increasing imports from diversified sources to continue to improve our margin profile. For the year ended December 31, 2025, manufacturing accounted for approximately 9% of our net sales, down from 11% in the prior year.

• We achieved record net sales of $467.7 million for the year ended December 31, 2025, an increase of 10.7% in net sales amount and 11.2% in volume compared to the year ended December 31, 2024.

• We recorded gross margin of 36.8% for the year ended December 31, 2025, reflecting an expected decrease of 210-basis-point compared to the year ended December 31, 2024, as cost of goods sold in 2025 reflected elevated inventory cost due to tariffs in place.

• We recorded net income of $32.7 million for the year ended December 31, 2025, an increase of 6.0% compared to the year ended December 31, 2024.

• We recorded net income margin of 7.0% for the year ended December 31, 2025, compared to 7.3% for the year ended December 31, 2024, reflecting the decrease in gross margin, as discussed above, and an improvement in operating cost leverage.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Year ended December 31, 2025 compared to the year ended December 31, 2024

Year Ended December 31,
2025 | 2024
(in thousands)
Net sales | 467,743 | 422,633
Cost of goods sold | 295,607 | 258,304
Gross profit | 172,136 | 164,329
Operating expenses | 130,722 | 126,568
Operating income | 41,414 | 37,761
Other income, net | 1,608 | 2,934
Provision for income taxes | 10,358 | 9,871
Net income | 32,664 | 30,824

Net sales

Net sales were $467.7 million for the year ended December 31, 2025 compared to $422.6 million for the year ended December 31, 2024, representing an increase of $45.1 million, or 10.7%. Net sales for the year ended December 31, 2024 were understated by $0.7 million, which represented products shipped and recognized as revenue in 2023 but not delivered until 2024. Including this impact, the year-over-year increase is primarily driven by an increase of $39.7 million from volume and an increase of $11.9 million from product mix. Such increases were partially offset by a $6.5 million unfavorable year-over-year pricing comparison, as the overall pricing environment remained competitive due to customers' heightened focus on value.

Cost of goods sold

Cost of goods sold was $295.6 million for the year ended December 31, 2025 compared to $258.3 million for the year ended December 31, 2024, representing an increase of $37.3 million, or 14.4%. Cost of goods sold for the year ended December 31, 2024 was understated by $0.4 million related to products shipped and recognized as cost of goods sold in 2023 but not delivered until 2024, as discussed above. Including this impact, the year-over-year increase in cost of goods sold was primarily driven by an increase in ocean freight and duty costs of $20.6 million, resulting from higher duties and tariffs, which nearly doubled from $14.7 million for the year ended December 31, 2024 to $29.3 million for the year ended December 31, 2025. This increase was further driven by a 22.0% increase in import volume, partially offset by a 5.4% decrease in average freight container rates. In addition, product costs increased by $18.1 million due to higher sales volume and better product mix, partially offset by more favorable vendor pricing.

Gross profit

Gross profit was $172.1 million for the year ended December 31, 2025 compared to $164.3 million for the year ended December 31, 2024, representing an increase of $7.8 million, or 4.8%. Gross profit for the year ended December 31, 2024 was understated by $0.3 million related to products shipped and recognized as revenue and cost of goods sold in 2023 but not delivered until 2024, as discussed above. Gross margin was 36.8% for the year ended December 31, 2025 compared to 38.9% for the year ended December 31, 2024, a decrease of 210 basis points. Gross margin was negatively impacted by rising freight and duty costs, as discussed above, which as a percentage of net sales increased to 11.8% during the year ended December 31, 2025 from 8.2% during the year ended December 31, 2024. This erosion in margin was partially offset by a decrease in product costs as a percentage of net sales from 49.9% during the year ended December 31, 2024 to 48.9% during the year ended December 31, 2025, as a result of more favorable vendor pricing and increased imports as a percentage of total product mix, as discussed above. Depreciation expense on production equipment as a percentage of net sales also decreased to 1.3% during the year ended December 31, 2025 from 1.5% during the year ended December 31, 2024.

Operating expenses

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-13_item1_business.md)

ITEM 1. BUSINESS

As used in this Annual Report on Form 10-K, "we", "us", "our", "Karat", "the Company" or "our Company" refer to Karat Packaging Inc., a Delaware corporation, and, unless the context requires otherwise, our operating subsidiaries. References to "Global Wells" or "our variable interest entity" refer to Global Wells Investment Group LLC, a Texas limited liability company and our consolidated variable interest entity, in which the Company has an equity interest and which is controlled by one of our stockholders. References to "Lollicup" refer to Lollicup USA Inc., our wholly-owned subsidiary incorporated in California in 2001 and redomesticated to the State of Texas in October 2025.

Our Company

We are a rapidly-growing and nimble distributor and manufacturer of disposable foodservice products and related items, including food and take-out containers, bags, boxes, tableware, cups, lids, cutlery, straws, specialty beverage ingredients, gloves, janitorial supplies, and other products. Our products are available in plastic, paper, biopolymer-based, and other compostable forms. We are a leader in product innovation, offering a growing line of environmentally-friendly products to our customers, who are increasingly focused on sustainability. We also offer customized solutions to our customers, including new product development, design, printing and logistics services.

We operate our business strategically and with broad flexibility to provide both our large and small customers with the wide spectrum of products they need to successfully run and grow their businesses. We believe we have established ourselves as a differentiated provider of high-quality products relative to our competitors. Our operating model entails generating the majority of our revenue from the distribution of products sourced from a diversified global network of nearly 150 vendors, complemented by select manufacturing capabilities in the U.S., which allows us to provide customers with broad product choices and customized offerings with short lead times. This model provides us with the flexibility to adjust the mix of our product offering from import and manufacturing in evolving economic environments to drive operating efficiency and sustained margin expansion and ensure quality of our customer service and product availability during global supply chain disruptions. Starting in 2023 and continuing into 2025, in light of the rising domestic labor and other operating costs and dropping ocean freight rates, we executed a strategy to pivot into a more asset-light model by increasing imports and scaling back domestic manufacturing.

Amidst the evolving tariff environment, we have placed our strategic emphasis on expanding and diversifying our global vendor network to enhance the resilience of our supply chain, minimize tariff impact on our operations and financial results, and maintain a strong margin profile and operating cash flows. We are prioritizing strong partnerships with reliable and cost-efficient sources and more favorable trade terms, negotiating additional vendor support, exploring opportunities to collaborate with vendors in new countries and geographies, while reallocating our own domestic production capabilities to optimize overall product margin. Although we have scaled back domestic manufacturing since 2023 by disposing of certain production machinery and related raw materials and reducing our production workforce, we have largely maintained our manufacturing infrastructure in the U.S. While we expect manufacturing to remain a relatively small portion of our sales mix going forward, we plan to keep manufacturing capabilities domestically to retain our nimble business model and resilient supply chain. For the year ended December 31, 2025, manufacturing accounted for approximately 9% of our net sales, down from 11% in the prior year.

Our customers include a wide variety of national and regional distributors, restaurant and supermarket chains, retail establishments and online customers. Our products are well suited to address our customers' needs towards take-out and food delivery orders. Our diverse and growing blue chip customer base includes well-known fast casual chains such as Applebee's Neighborhood Grill + Bar, Chili's Grill & Bar, PF Chang's China Bistro, Chipotle Mexican Grill, and Olive Garden, fast food chains such as The Coffee Bean & Tea Leaf, El Pollo Loco, In-N-Out Burger, Jack in the Box, Panda Express, and Raising Cane's Chicken Fingers. Additionally, in 2025, we initiated a strategic emphasis on growing our paper bag business. We have won a paper bag contract with one of our largest national chain accounts with forecast annualized revenue of approximately $17.0 million, and we are looking into replicating the success with our other customers. We expect our paper bag business to significantly scale, and become one of the most significant growth drivers for our business in the next two to three years. As our capabilities, product offering, and footprint expand, we aim to broaden our reach to national and regional airlines, entertainment venues, and other non-restaurant customers. Our increasingly strong brand recognition in the foodservice industry, nimble operations and scaled distribution position us strongly for new customer acquisition and continued wallet share expansion with existing customers. For the years ended December 31, 2025 and 2024, no single customer represented more than 10% of our revenue.

We are an omni-channel provider and have made significant investments in e-commerce, distribution network, technology, supply chain, and customer initiatives, such as online ordering and same day pickup. We operate our e-commerce

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-13_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-13_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-13_item7_mdna.md, 10-K_2026-03-13_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
