# Triage pack — HNST · Honest Company, Inc.

_Generated 2026-09-05 01:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** HNST · **Name:** Honest Company, Inc.
- **CIK:** 0001530979
- **SIC:** 5961 — Retail-Catalog & Mail-Order Houses
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/HNST

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Honest Company, Inc.
- **CIK:** 1,530,979 · **SIC:** 5961 (Retail-Catalog & Mail-Order Houses) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 5.85 |
| mktcap | $627.6M |
| ev | $521.7M |
| ev_ebit | n/a |
| fcf | $13.6M |
| fcf_yield | 2.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -23.9% |
| net_debt | -$105.9M |
| net_debt_ebit | n/a |
| cash | $105.9M |
| ltd | $0.00 |
| equity | $167.0M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $371.3M |
| revenue_prior | $378.3M |
| rev_growth | -1.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$18.5M |
| net_income | -$15.7M |
| cfo | $15.1M |
| capex | $1.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -3.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 107,284,379 |
| shares_py | 111,269,491 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -2.8% |
| r6m | 100.3% |
| off_52w_high | 0.0% |
| adv20 | $14.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.32 |
| r_ev_ebit | 0.00 |
| r_roic | 0.05 |
| r_rev_growth | 0.28 |
| r_buyback | 0.83 |
| score | 0.30 |

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
| rank | 412 |

**Screen rationale:** buying back stock -3.6%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **107,284,379** (CY2026Q2I) vs **111,269,491** prior year (CY2025Q2I)
- Change: **-3.6%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-18** — Item 1.01 (Entry into a Material Definitive Agreement): On June 14, 2026, The Honest Company, Inc. (the "Company") entered into a lease agreement (the "Lease") with Dellwood Farm LLC, a Delaware limited liability company (the "Landlord"), for approximately 38,240 rentable square feet located at 12121 Bluff Creek...
- **2026-05-27** — Item 5.02 (officer / director change or comp arrangement): On May 20, 2026, the Board of Directors of The Honest Company, Inc. (the "Company") approved the promotion of Curtiss Bruce to the position of Chief Financial & Operating Officer, effective May 21, 2026 (the "Effective Date").
- **2026-04-06** — Item 1.01 (Entry into a Material Definitive Agreement): On March 31, 2026, The Honest Company, Inc. (the "Company") entered into a First Amendment to Credit Agreement and First Amendment to Pledge and Security Agreement (the "Amendment"), among the Company, as borrower, the lenders party thereto (the "Lenders")...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 307,747 sh / $1,558,758 -> net $-1,558,758 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 19 (open-market buys 0, sales 13).

| code | rows |
|---|---|
| A | 6 |
| S | 13 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'The Honest Company Reports Second Quarter 2026 Results'; skipped 12 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (honestcoq2-26exhibit991.htm)

The Honest Company Reports Second Quarter 2026 Results

Top-Line Momentum Continues Behind Higher-Margin Growth Platforms

Record Profitability & Durable Foundation Enable Accelerated Reinvestment for Sustainable Growth

Raising Full Year 2026 Financial Outlook

LOS ANGELES, Calif. – August 5, 2026 – The Honest Company (Nasdaq: HNST), a personal care company dedicated to creating cleanly-formulated and sustainably-designed products for everyone from babies to adults, today reported financial results for its second quarter ended June 30, 2026.

Second Quarter 2026 Financial Highlights Compared to Prior Year Period:

• Revenue of $83.3 million decreased 10.9%; Organic Revenue (1) increased 6.7%

• Gross margin of 48.4% increased 800 bps; Underlying Adjusted Gross Margin (1) of 43.8% increased 340 bps

• Net income of $10.7 million increased $6.8 million; Underlying Adjusted Net Income (1) was $5.1 million

• Underlying Adjusted EBITDA (1) was $7.8 million; Underlying Adjusted EBITDA Margin (1) of 9.8% increased 160 bps

• Cash and cash equivalents of $105.9 million increased $33.8 million

"For the second quarter we delivered accelerated Organic Revenue growth of 7% and record underlying margins," said Chief Executive Officer, Carla Vernón. "With consumption growth of nearly 8%, we believe the momentum across our fastest-growing, most profitable platforms is proving to be durable. This strong performance, built upon a vibrant growth vision and increased structural profitability, is evidence that The Honest Company is a modern personal care company built to last. We are now well-positioned to thoughtfully deploy additional investments to expand household penetration and drive operational excellence of The Honest Company. With confidence in our continued momentum, we are raising our full-year 2026 financial outlook."

Second Quarter Results

(All comparisons are versus the second quarter of 2025)

For the three months ended June 30,
2026 | 2025 | Change
(In thousands, except percentages)
Revenue | 83,303 | 93,459 | (10.9) | %
Organic Revenue (1) | 80,189 | 75,123 | 6.7 | %
Gross margin | 48.4 | % | 40.4 | % | 800 | bps
Underlying Adjusted Gross Margin (1) | 43.8 | % | 40.4 | % | % | 340 | bps
Net income | 10,687 | 3,870 | 6,817
Underlying Adjusted Net Income (1) | 5,072 | 3,870 | 1,202
Underlying Adjusted Net Income Margin (1) | 6.3 | % | 4.1 | % | 220 | bps
Underlying Adjusted EBITDA (1) | 7,831 | 7,617 | 214
Underlying Adjusted EBITDA Margin (1) | 9.8 | % | 8.2 | % | 160 | bps

(1) These are non-GAAP financial measures. See tables below under "Use of Non-GAAP Financial Measures" for information on how we calculate and define these non-GAAP financial measures, including a reconciliation of these non-GAAP financial measures to the most comparable GAAP financial measures.

Revenue decreased 10.9% to $83.3 million, reflecting the impact of strategic exits under Powering Honest Growth and diaper revenue declines, partially offset by continued growth in wipes and personal care products.

Organic Revenue (1) increased 6.7% to $80.2 million, driven by growth in wipes and personal care products, partially offset by a decline in diaper revenue.

Tracked channel consumption (2) for the Company increased 7.7% versus 2.3% for the comparative categories in the same period.

Gross margin was 48.4%, reflecting an increase of 800 bps. This expansion was primarily driven by tariff refunds, favorable product mix, and improvements related to strategic exits under Powering Honest Growth (3) net of the partial liquidation of the remaining apparel inventory. Adjusted Gross Margin (1) , calculated by excluding the discrete costs of Powering Honest Growth, was 50.1%, reflecting an increase of 970 bps. Underlying Adjusted Gross Margin (1) , calculated by excluding the discrete costs of Powering Honest Growth, tariff refunds and the partial liquidation of the remaining apparel inventory was 43.8%.

Operating expenses decreased $4.1 million to $30.8 million. The decrease in operating expenses was driven by lower selling, general & administrative expenses, partially offset by increased marketing investment to support our higher-growth, higher-margin wipes and personal care platforms. Adjusted Operating Expenses (1) , calculated by excluding the discrete costs of Powering Honest Growth, was $31.2 million. Selling, general & administrative expenses as a percentage of revenue decreased approximately 380 bps mainly driven by operational efficiencies.

Net income increased $6.8 million to $10.7 million primarily related to tariff refunds and growth in Organic Revenue (1) . Adjusted Net Income (1) excluding the impact of Powering Honest Growth was $11.7 million. Underlying Adjusted Net Income (1) , calculated as Adjusted Net Income excluding tariff refunds was $5.1 million.

Adjusted EBITDA (1) was $14.5 million compared to $7.6 million. Underlying Adjusted EBITDA (1) , calculated as Adjusted EBITDA excluding tariff refunds was $7.8 million and Underlying Adjusted EBITDA Margin (1) was 9.8%.

Balance Sheet and Cash Flow

As of June 30, 2026, the Company had no debt outstanding and $105.9 million in cash and cash equivalents, an increase of $33.8 million, primarily related to inventory reductions and higher net income, partially offset by repurchases of common stock versus the prior year period.

Net cash provided by operating activities was $37.8 million for the six months ended June 30, 2026, compared to net cash used in operating activities of $3.7 million in the prior year period.

During the six months ended June 30, 2026, the Company repurchased approximately 5.6 million shares of its common stock for approximately $18.7 million at a weighted average price of $3.35 per share. As of June 30, 2026, the Company had approximately $6.3 million remaining under its share repurchase program.

(1) These are non-GAAP financial measures. See tables below under "Use of Non-GAAP Financial Measures" for information on how we calculate and define these non-GAAP financial measures, including a reconciliation of these non-GAAP financial measures to the most comparable GAAP financial measures.

(2) According to Circana, Inc. MULO+ tracked channel consumption data. Reflects consumption in the categories in which the Company competes. Weighted category growth represents retail consumption growth of the categories in which the Company competes, weighted by the Company's category growth for the latest 13 weeks ended June 28, 2026.

(3) Refer to the table below under "Transformation 2.0: Powering Honest Growth" for additional information on costs incurred in connection with Powering Honest Growth for the six months ended June 30, 2026.

Raising Full Year 2026 Financial Outlook

The Company is raising its full year 2026 financial outlook for Revenue, Organic Revenue growth, Adjusted Gross Margin and Adjusted EBITDA.

Updated | Prior
Revenue | $319 million to $325 million | $306 million to $312 million
Organic Revenue Growth (1) | 5% to 7% | 4% to 6%
Adjusted Gross Margin (2) | Mid 40%s | Low 40%s
Adjusted EBITDA (2) | $23.0 million to $25.0 million | $20.0 million to $23.0 million

Our financial outlook reflects assumptions, including current tariff levels and our tariff mitigation measures, which are subject to change given the macroeconomic environment. Additional information on the Company's strategic plans and long-term financial algorithm can be found in its Investor Presentation on its Investor Relations website at http://investors.honest.com .

(1) Represents the current outlook for Organic Revenue growth excluding (i) product revenue from our apparel line of $38.5 million in 2025; (ii) revenue from our Honest.com website as a fulfillment center of $35.3 million in 2025; and (iii) revenue from sales to Canadian retailers or channels of $3.4 million in 2025.

(2) We do not provide guidance for the most directly comparable GAAP measures, gross margin and net income, as applicable, and similarly cannot provide a reconciliation between our Adjusted Gross Margin outlook and gross margin and Adjusted EBITDA outlook and net income without unreasonable effort due to the unavailability of reliable estimates for certain components of gross margin and net income, including restructuring-related costs, and interest and other (income) expense, net, and the respective reconciliations. These items are not within our control and may vary greatly between periods and could significantly impact our financial results calculated in accordance with GAAP.

Webcast and Conference Call Information

A webcast and conference call to discuss second quarter 2026 results is scheduled for today, August 5, 2026, at 1:45 p.m. Pacific time/4:45 p.m. Eastern time. Those interested in participating in the conference call by phone, please go to the Q2 2026 Earnings Call and you will be provided with dial-in details. A live webcast of the conference call will be available online at: http://investors.honest.com . A replay of the webcast will be available on the Company's website for one year.

Media Contact:

Brenna Israel Mast

bisrael@thehonestcompany.com

The Honest Company, Inc.

Condensed Consolidated Statements of Comprehensive Income

(Unaudited)

(in thousands, except share and per share amounts)

For the three months ended June 30, | For the six months ended June 30,
2026 | 2025 | 2026 | 2025
Revenue | 83,303 | 93,459 | 161,402 | 190,709
Cost of revenue | 42,943 | 55,707 | 87,771 | 115,287
Gross profit | 40,360 | 37,752 | 73,631 | 75,422
Operating expenses
Selling, general and administrative | 14,967 | 20,352 | 32,436 | 41,393
Marketing | 14,476 | 12,552 | 28,469 | 24,822
Restructuring | (383) | — | 223 | —
Research and development | 1,722 | 1,960 | 3,584 | 3,812
Total operating expenses | 30,782 | 34,864 | 64,712 | 70,027
Operating income | 9,578 | 2,888 | 8,919 | 5,395
Interest and other income (expense), net | 1,174 | 1,026 | 1,838 | 1,812
Income before provision for income taxes | 10,752 | 3,914 | 10,757 | 7,207
Income tax provision | 65 | 44 | 111 | 84
Net income | 10,687 | 3,870 | 10,646 | 7,123
Net income per share attributable to common stockholders:
Basic | 0.10 | 0.03 | 0.10 | 0.06
Diluted | 0.09 | 0.03 | 0.09 | 0.06
Weighted-average shares used in computing net income per share attributable to common stockholders:
Basic | 110,734,911 | 110,991,363 | 111,771,587 | 110,275,931
Diluted | 113,106,023 | 114,041,772 | 113,355,168 | 114,310,420
Comprehensive income | 10,687 | 3,870 | 10,646 | 7,123

The Honest Company, Inc.

Condensed Consolidated Balance Sheets

(Unaudited)

(in thousands, except share and per share amounts)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-25_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Founded in 2012, The Honest Company (the "Company," or "Honest," or which may also be referred to as "we," "us" or "our") is a personal care company dedicated to creating cleanly-formulated and sustainably-designed products for everyone from babies to adults. By combining thoughtful design with science-based innovation, we deliver personal care products for everyone from babies to adults, spanning categories across wipes, personal care, diapers, and beauty. Our commitment to our core values, continual innovation and engaging our community has differentiated and elevated our brand and our products. Since our launch, we have cultivated deep trust around what matters most to our consumers: their health, their families and their homes. We seek to meet consumers wherever they want to shop, balancing deep consumer connection with broad convenience and availability. We believe our distribution strategy positions us for continued growth through our trusted brand and award-winning multi-category product offering.

The Honest Standard, the Company's rigorous set of guiding principles that shape every step of product innovation and development, reflects Honest's ongoing dedication to safety, transparency and integrity. As a leader in clean and sustainable products, Honest continues to set a new standard for clean formulations, bringing joy to a community that seeks authenticity, transparency and efficacy in everyday essentials. Honest products are available nationwide at major retailers, including Amazon, Target and Walmart.

Effective December 31, 2025, we have transitioned away from Honest.com as a shipping and fulfillment channel, while maintaining Honest.com as a resource for educating consumers, showcasing our complete product portfolio, and driving consumers to purchase through our leading retailers and their websites, and third-party ecommerce sites.

Transformation 2.0: Powering Honest Growth

In 2023, we executed a broad-based Transformation Initiative designed to build the Honest brand and drive growth in higher-margin areas of the portfolio, strengthen our cost structure, drive focus on the most productive areas of our business, deliver greater impact from brand-building investments, and improve executional excellence across the enterprise. The restructuring element of the Transformation Initiative was substantially completed by December 31, 2023.

In October 2025, our Board of Directors approved Transformation 2.0: Powering Honest Growth ("Powering Honest Growth") which builds upon our original Transformation Pillars of Brand Maximization, Margin Enhancement and Operating Discipline. Powering Honest Growth is aimed at improving simplicity, focus and profitability, which includes exiting certain lower margin, non-strategic categories and channels, including exiting Honest.com fulfillment and apparel, as well as exiting retail and online stores in Canada, optimizing our cost structure by rightsizing selling, general and administrative expenses and implementing supply chain efficiencies.

Powering Honest Growth is projected to result in the following:

• Costs associated with Powering Honest Growth, including restructuring costs, are expected to be approximately $30.0 million to $35.0 million to be recognized through the first quarter of 2027. During the year ended December 31, 2025, we have recognized $24.0 million of total costs related to Powering Honest Growth. See table below for additional details of total costs.

◦ Of this range, we expect approximately $5.0 million to $8.0 million to be related to restructuring costs, primarily comprising contractual and external obligation costs, employee and personnel-related costs and asset and other restructuring-related costs, and approximately $25.0 million to $27.0 million to be related to other costs included in cost of revenue, primarily related to a discrete inventory write-down related to exiting apparel, fixed asset impairments, and costs associated with the warehouse closure, some of which

have already been incurred. For the year ended December 31, 2025, we have recognized $4.2 million in restructuring costs and $19.8 million in cost of revenue included on the consolidated statements of comprehensive loss.

• Powering Honest Growth is expected to result in annualized benefits in the range of approximately $10.0 million to $15.0 million, and the Company expects to begin seeing benefits in 2026. These benefits include reduction in costs of revenue and reduction in operating expenses, offset by a decrease in revenue related to the exit of lower margin non-strategic portfolios.

• The cash impact of costs related to Powering Honest Growth is expected to be in the range of approximately $15.0 million to $20.0 million for the full year 2026, with an immaterial amount of costs incurred during the year ended December 31, 2025 and the remainder to be incurred in 2026 and 2027.

• We expect the restructuring element of Powering Honest Growth to be substantially completed by December 31, 2026. We may incur other costs or cash expenditures not currently contemplated as a result of or in connection with Powering Honest Growth.

We expect to continue driving benefits from the three Transformation Pillars of Brand Maximization, Margin Enhancement, and Operating Discipline:

1) Brand Maximization

• Leveraging the strength of the Honest brand to drive growth through greater availability, expanded household penetration, product innovation, margin-accretive products, and marketing effectiveness.

• Pricing strategy as a driver of revenue is also a component of Brand Maximization.

2) Margin Enhancement

• Focusing our resources on the United States, which included the exit of our low-margin products in Europe and Asia in 2023 and, most recently, Canada in 2025.

• Exiting low-margin elements of cleaning and sanitization products in 2023 and apparel in 2025.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth our consolidated statements of comprehensive loss data for each of the periods indicated:

For the year ended December 31,
2025 | 2024
(In thousands)
Revenue | 371,317 | 378,340
Cost of revenue | 247,562 | 233,683
Gross profit | 123,755 | 144,657
Operating expenses
Selling, general and administrative (1) | 79,510 | 99,044
Marketing | 51,200 | 45,093
Restructuring | 4,159 | —
Research and development (1) | 7,347 | 6,851
Total operating expenses | 142,216 | 150,988
Operating loss | (18,461) | (6,331)
Interest and other income (expense), net | 2,979 | 282
Loss before provision for income taxes | (15,482) | (6,049)
Income tax provision | 204 | 75
Net loss | (15,686) | (6,124)

(1) Includes stock-based compensation expense as follows:

For the year ended December 31,
2025 | 2024
(In thousands)
Selling, general and administrative | 9,734 | 15,105
Research and development | 778 | 570
Total | 10,512 | 15,675

The following table sets forth our consolidated statements of comprehensive loss data expressed as a percentage of revenue*:

For the year ended December 31,
2025 | 2024
(as a percentage of revenue)
Revenue | 100.0 | % | 100.0 | %
Cost of revenue | 66.7 | 61.8
Gross profit | 33.3 | 38.2
Operating expenses
Selling, general and administrative | 21.4 | 26.2
Marketing | 13.8 | 11.9
Restructuring | 1.1 | —
Research and development | 2.0 | 1.8
Total operating expenses | 38.3 | 39.9
Operating loss | (5.0) | (1.7)
Interest and other income (expense), net | 0.8 | 0.1
Loss before provision for income taxes | (4.2) | (1.6)
Income tax provision | 0.1 | —
Net loss | (4.2) | % | (1.6) | %

* Amounts may not sum due to rounding.

Comparison of the Year Ended December 31, 2025 and 2024

Revenue

For the year ended December 31,
2025 | 2024 | $ change | % change
(In thousands, except percentages)
Revenue | 371,317 | 378,340 | (7,023) | (1.9) | %

Revenue was $371.3 million for the year ended December 31, 2025, as compared to $378.3 million for the year ended December 31, 2024. The decrease of $7.0 million, or 1.9%, was primarily due to the discrete exits related to Powering Honest Growth of $21.9 million (inclusive of a decrease in DTC revenue of $13.2 million, a decrease in apparel revenue of $7.7 million and a decrease in Canada revenue of $1.0 million), partially offset by an increase in retail customer revenue (excluding apparel and Canada revenue) of $14.9 million. The increase in retail customer revenue is primarily due to an increase in wipes revenue of $27.6 million and an increase in baby personal care revenue of $6.7 million, partially offset by a decline in diaper revenue of $14.4 million primarily related to distribution losses, the lapping of certain retailer promotional events and changes in consumer shopping behavior, and a decline in adult facial care (including skin care and cosmetics) of $5.7 million. Refer to the Organic Revenue table under "Non-GAAP Financial Measures" below for further details of revenue excluding the revenue associated with the discrete exits related to Powering Honest Growth.

Cost of Revenue and Gross Profit
For the year ended December 31,
2025 | 2024 | $ change | % change
(In thousands, except percentages)
Cost of revenue | 247,562 | 233,683 | 13,879 | 5.9 | %
Gross profit | 123,755 | 144,657 | (20,902) | (14.4) | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-25_item1_business.md)

Item 1. Business

Overview of Business

Founded in 2012, The Honest Company (the "Company," or "Honest," or which may also be referred to as "we," "us" or "our") is a personal care company dedicated to creating cleanly-formulated and sustainably-designed products for everyone from babies to adults. By combining thoughtful design with science-based innovation, we deliver personal care products for everyone from babies to adults, spanning categories across wipes, personal care, diapers, and beauty. Our commitment to our core values, continual innovation and engaging our community has differentiated and elevated our brand and our products. Since our launch, we have cultivated deep trust around what matters most to our consumers: their health, their families and their homes. We seek to meet consumers wherever they want to shop, balancing deep consumer connection with broad convenience and availability. We believe our distribution strategy positions us for continued growth through our trusted brand and award-winning multi-category product offering.

Our Products and Product Categories

Our Chief Executive Officer, as the chief operating decision maker, organizes the Company, manages resource allocations, and measures performance on the basis of one operating segment. We offer an array of cleanly-formulated and sustainably-designed products, including a portfolio of wipes and a personal care collection for everyone from babies to adults, as well as diapers. We use cleanly-formulated and safe ingredients designed for the whole family, including many naturally-derived ingredients that, most importantly, are effective. We also offer a portfolio of wipes, including all-purpose wipes, flushable wipes in both toddler and adult variations, sanitizing wipes, and make-up remover wipes. Our Clean Conscious® wipes are compostable and plant-based, made with over 99% water and designed to protect delicate skin. We have an extensive collection of personal care products for everyone from babies to adults, as well as adult facial care products designed for a range of skin types and concerns, many of which are certified by trusted experts and institutions, including the National Eczema Association. Our ingredients and formulas are toxicologist-audited for potential health concerns. Primary components of our diapers include responsibly sourced, plant-based fluff pulp and other plant-derived materials. Our diapers have an extensive modern and efficient design that uses less material.

Our Distribution Strategy

We seek to meet consumers wherever they want to shop, balancing deep consumer connection with broad convenience and availability. Our distribution strategy positions us for continued growth through our trusted brand and award-winning multi-category product offerings. Since our launch, we have expanded our product availability, including the launch of strategic partnerships with Target, Amazon and Walmart in 2014, 2017 and 2022, respectively , as well as distribution with many other retailers nationwide . We have retail partnerships with leading retailers that sell our products through brick and mortar stores and on their own websites. Our retail partnerships expand brand awareness and product availability , creating meaningful marketing efficiencies as we continue to scale. Additionally, these retail partnerships support our differentiated value proposition by making our products conveniently available in the many places where our consumer shops.

Effective December 31, 2025, we have transitioned away from Honest.com as a shipping and fulfillment channel, while maintaining Honest.com as a resource for educating consumers, showcasing our complete product portfolio, and driving consumers to purchase through our leading retailers and their websites, and third-party ecommerce sites.

Our Growth Strategy

The core of our growth strategy centers around increasing physical and digital availability of our products, including through expanded stores, doors, aisles, shelves and facings. While we have made significant progress in our distribution gains, we are still under-indexed compared to competition. Our marketing strategy is focused on building a purpose-driven brand with deep connection to the community of shoppers we serve. We apply a modern, data-driven marketing approach and continuously innovate, optimize and identify new ways to reach and connect with our community. We believe this includes a best-in-class social media and influencer marketing strategy and a highly strategic approach to paid media.

In 2023, we executed a broad-based Transformation Initiative designed to build the Honest brand and drive growth in higher-margin areas of the portfolio, strengthen our cost structure, drive focus on the most productive areas of our business, deliver greater impact from brand-building investments, and improve executional excellence across the enterprise.

On October 30, 2025, our Board of Directors approved Transformation 2.0: Powering Honest Growth ("Powering

Honest Growth") which builds upon our original Transformation Pillars of Brand Maximization, Margin Enhancement and Operating Discipline. Powering Honest Growth is aimed at improving simplicity, focus and profitability, which includes exiting certain lower margin, non-strategic categories and channels, including exiting Honest.com fulfillment and apparel, as well as exiting retail and online stores in Canada, optimizing our cost structure by rightsizing selling, general and administrative expenses, and implementing supply chain efficiencies. We expect to substantially complete the actions under Powering Honest Growth by December 31, 2026.

Our strategic plan is grounded in our Transformation Pillars, which set the building blocks for long-term value creation. We expect to realize revenue growth of 4% to 6% annually and continued Adjusted EBITDA margin expansion.

Supply Chain and Operations

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-25_item7_mdna.md, 10-K_2026-02-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
