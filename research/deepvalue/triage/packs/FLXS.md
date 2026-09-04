# Triage pack — FLXS · FLEXSTEEL INDUSTRIES INC

_Generated 2026-09-04 14:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** FLXS · **Name:** FLEXSTEEL INDUSTRIES INC
- **CIK:** 0000037472
- **SIC:** 2510 — Household Furniture
- **Fiscal year end (MM-DD):** 06-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/FLXS

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** FLEXSTEEL INDUSTRIES INC
- **CIK:** 37,472 · **SIC:** 2510 (Household Furniture) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 80.37 |
| mktcap | $430.4M |
| ev | $413.7M |
| ev_ebit | 15.5x |
| fcf | $33.7M |
| fcf_yield | 7.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 18.0% |
| net_debt | -$16.7M |
| net_debt_ebit | -0.6x |
| cash | $16.7M |
| ltd | $0.00 |
| equity | $133.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $441.1M |
| revenue_prior | $412.8M |
| rev_growth | 6.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $26.6M |
| net_income | $20.2M |
| cfo | $37.0M |
| capex | $3.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 5,355,531 |
| shares_py | 5,273,253 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 70.0% |
| r6m | 68.7% |
| off_52w_high | -2.2% |
| adv20 | $6.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.64 |
| r_ev_ebit | 0.57 |
| r_roic | 0.86 |
| r_rev_growth | 0.57 |
| r_buyback | 0.38 |
| score | 0.65 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 98 |

**Screen rationale:** high ROIC 18.0%; debt data missing (net cash unverified); 12-1 momentum 70.0%


## 3. Share count trend

- Shares outstanding: **5,355,531** (CY2026Q1I) vs **5,273,253** prior year (CY2025Q1I)
- Change: **1.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-04-28** — Item 1.01 (Entry into a Material Definitive Agreement): On April 26, 2026, Flexsteel Industries, Inc. (the "Company") entered into a stock repurchase agreement (the "Stock Repurchase Agreement") with F. Brooks Bertsch, a director of the Company, and certain family related entities listed on Schedule 1 thereto (the...
- **2026-04-28** — Item 5.02 (officer / director change or comp arrangement): F. Brooks Bertsch resigned from the Board pursuant to the terms of the Stock Repurchase Agreement.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 15,858 sh / $1,289,549 -> net $-1,289,549 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 37 (open-market buys 0, sales 21).

| code | rows |
|---|---|
| A | 5 |
| F | 7 |
| M | 4 |
| S | 21 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-17_2-02-results.md)

_Extraction: started at the first release heading, 'Flexsteel Industries, Inc. Reports Fourth Quarter and Fiscal Year 2026'; skipped 8 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (flxs-ex99_1.htm)

Flexsteel Industries, Inc. Reports Fourth Quarter and Fiscal Year 2026 Results; Continued Net Sales Growth and Record Diluted Earnings Per Share

Dubuque, Iowa – August 17, 2026 – Flexsteel Industries, Inc. (NASDAQ: FLXS) ("Flexsteel" or the "Company"), one of the largest manufacturers, importers, and marketers of residential furniture products in the United States, today reported fourth quarter and fiscal year 2026 results.

Key Results for the Fourth Quarter and Fiscal Year Ended June 30, 2026

•
Net sales for the quarter of $115.4 million compared to $114.6 million in the prior year quarter, an increase of 0.7%. For the year, net sales increased 4.1% to $459.2 million compared to $441.1 million in the prior year.

•
GAAP operating income of $16.3 million or 14.2% of net sales for the fourth quarter and $42.6 million or 9.3% of net sales for the year compared to $14.0 million or 12.2% of net sales in the prior year quarter and $26.6 million or 6.0% of net sales for the prior year.

o
Adjusted operating income of $8.2 million or 7.1% of net sales for the fourth quarter and $34.4 million or 7.5% of net sales for the year compared to $10.3 million or 9.0% of net sales in the prior year quarter and $31.3 million or 7.1% of net sales for the prior year.

•
GAAP net income per diluted share of $2.58 for the current quarter and $6.07 for the year compared to net income per diluted share of $1.89 for the prior year quarter and net income per diluted share of $3.55 for the prior year.

o
Adjusted net income per diluted share of $1.33 for the quarter and $4.94 for the year compared to adjusted net income per diluted share of $1.40 for the prior year quarter and $4.17 for the prior year.

•
The Company generated $24.3 million of cash flow from operations and completed $62.6 million of share repurchases in the fourth quarter.

GAAP to non-GAAP reconciliations follow the financial statements in this press release

Management Commentary

"Fiscal year 2026 was a year of strong financial performance and meaningful strategic progress despite increasingly difficult industry conditions," said Derek Schmidt, CEO of Flexsteel Industries, Inc. "For the year, we delivered sales growth of approximately 4 percent to $459 million, expanded adjusted operating margin to 7.5 percent, generated record adjusted earnings per diluted share of $4.94, and produced more than $47.5 million of free cash flow. Our strong cash generation and balance sheet enabled us to repurchase approximately $64 million of stock during the year and recently increased our dividend by 25 percent. These results were achieved despite a challenging demand environment, evolving tariff policies, geopolitical uncertainty, and rising inflationary pressures, demonstrating the resilience of our business model and the agility of our organization."

Mr. Schmidt continued, "While fourth quarter sales were only modestly above the prior year period, it was our eleventh consecutive quarter of year-over-year growth, driven by our key growth initiatives which continue to

perform well. Our health and wellness category, strategic account relationships, and recent product introductions all delivered positive contributions during the quarter despite softer overall industry demand. Consumer demand for furniture remains pressured by weak confidence, affordability constraints, and macroeconomic uncertainty related to the ongoing conflict in the Middle East. Even consumers shopping at higher price points have become increasingly value-conscious in today's environment. Despite these headwinds, we delivered strong adjusted operating margin of approximately 7.1 percent in the quarter, reflecting disciplined product portfolio management, operational productivity improvements, and prudent management of selling and administrative expenses while continuing to fund critical growth investments."

Mr. Schmidt concluded, "Beyond the financial results, we made significant progress strengthening the long-term competitive position of the Company. We continued to expand our capabilities in consumer insights, innovation, product development, and marketing, enabling us to bring more relevant products to market and drive stronger engagement with both consumers and retail partners. Looking ahead, we remain measured in our outlook as macroeconomic uncertainty, elevated inflation, rising energy costs, and trade policy uncertainty continue to pressure industry demand and profitability. While near-term conditions may remain challenging, our strategy and priorities are unchanged. We will continue to operate with agility, maintain disciplined cost control, and invest in the capabilities that we believe will drive long-term growth, market share gains, and shareholder value creation. With a strong balance sheet, a resilient operating model, and clear strategic priorities, we believe Flexsteel is well positioned to successfully navigate the current environment and emerge even stronger over time."

Operating Results for the Fourth Quarter Ended June 30, 2026

Net sales were $115.4 million for the fourth quarter compared to net sales of $114.6 million in the prior year quarter, an increase of $0.8 million, or 0.7%. The increase was driven by higher unit volume from soft seating products, partially offset by decreases in our ready-to-assemble products sold under the homestyles brand.

Gross margin for the quarter ended June 30, 2026, was 30.0%, compared to 23.9% for the prior year quarter, an increase of 610 basis points ("bps"). The 610-bps increase was primarily due to a 780-bps benefit from IEEPA Tariff Refunds received, offset by a 100-bps unfavorable impact of foreign currency translation of our peso-denominated assets in Mexico versus the prior period, and a 70-bps unfavorable cost impact related to the decision to exit our ready-to-assemble product category sold under the homestyles brand.

Selling, general and administrative (SG&A) expense was 15.8% of net sales for the quarter ended June 30, 2026, compared to 15.0% in the prior year quarter. The 80-bps increase was due to incremental investments in consumer insights, innovation, new products, and marketing to maintain our growth momentum.

Operating income for the quarter ended June 30, 2026, was $16.3 million compared to $14.0 million in the prior year quarter. On an adjusted basis, operating income for the quarter ended June 30, 2026, was $8.2 million compared to $10.3 million in the prior year quarter.

Income tax expense was $3.8 million, or an effective rate of 23.0%, during the fourth quarter compared to tax expense of $3.6 million, or an effective rate of 25.0%, in the prior year quarter.

Net income was $12.7 million, or $2.58 per diluted share, for the quarter ended June 30, 2026, compared to net income of $10.7 million, or $1.89 per diluted share, in the prior year quarter. On an adjusted basis, net income for the quarter ended June 30, 2026, was $6.6 million or $1.33 per diluted share compared to adjusted net income of $7.9 million or $1.40 per diluted share in the prior year quarter.

Liquidity

The Company ended the quarter with a cash balance of $16.7 million, working capital (current assets less current liabilities) of $94.6 million, and availability of approximately $54.1 million under its secured line of credit.

Capital expenditures for the year ended June 30, 2026, were $3.9 million.

Financial Outlook

For the first quarter of fiscal year 2027, the Company expects sales growth of 1% to 4% compared to the prior year quarter and operating margin of 6.5% to 7%. The most significant drivers of variability in the financial outlook are consumer demand and logistics and material cost inflation driven by elevated energy prices.

First Quarter Fiscal Year 2027
Sales | $111 - 115 million
Sales Growth (vs. Prior Year) | 1% to 4%
GAAP Operating Margin | 6.5% to 7%

Conference Call and Webcast

The Company will host a conference call and audio webcast with analysts and investors on Tuesday, August 18, 2026, at 8:00 a.m. Central Time to discuss the results and answer questions.

•
Live conference call: 833-816-1123 (domestic) or 412-317-0710 (international)

•
Conference call replay available through August 25, 2026: 855-669-9658 (domestic) or 412-317-0088 (international)

•
Replay access code: 7455617

•
Live and archived webcast: ir.flexsteel.com

To pre-register for the earnings conference call and avoid the need to wait for a live operator, investors can visit https://dpregister.com/sreg/10210984/1049369efa0 and enter their contact information. Investors will then be issued a personalized phone number and PIN to dial into the live conference call.

About Flexsteel

Flexsteel Industries, Inc. and Subsidiaries (the "Company," "Flexsteel," or "Our") is one of the largest residential furniture manufacturers, importers, and marketers in the U.S. Flexsteel addresses different consumer groups through our core brand, Flexsteel, and several category-specific sub-brands: Zecliner, Statements, Zen, Perfect Match, and Pulse, all of which have unique value propositions tailored to specific consumer needs. We offer a wide assortment of product solutions for different areas within the home including stationary and motion sofas, loveseats, chairs, and sectionals, as well as bedroom furniture, dining tables and chairs, occasional and entertainment tables, and kitchen storage. For more than 130 years, Flexsteel has strived to create strong consumer value with unmatched quality, comfort, and durability, backed by innovation and highlighted by its patented Blue Steel Spring technology, designed to deliver lasting comfort and support. Today, Flexsteel products are available nationwide through retail partners and online channels.

CONSOLIDATED STATEMENTS OF INCOME AND COMPREHENSIVE INCOME (UNAUDITED)

(in thousands, except per share data)

Three Months Ended | Twelve Months Ended
June 30, | June 30,
2026 | 2025 | 2026 | 2025
Net sales | 115,365 | 114,611 | 459,178 | 441,073
Cost of goods sold | 80,744 | 87,175 | 345,742 | 343,129
Gross profit | 34,621 | 27,436 | 113,436 | 97,944
Selling, general and administrative expenses | 18,277 | 17,164 | 70,886 | 66,696
Right-of-use asset impairment | — | — | — | 14,079
(Gain) on sale of real estate | — | — | — | (753
(Gain) on disposal of assets held for sale | — | (3,702 | — | (8,693
Operating income | 16,344 | 13,974 | 42,550 | 26,615
Other income (expense):
Interest income | 183 | 288 | 1,288 | 421
Interest (expense) | (22 | — | (22 | (70
Total other income (expense) | 161 | 288 | 1,266 | 351
Income before income taxes | 16,505 | 14,262 | 43,816 | 26,966
Income tax provision | 3,793 | 3,560 | 10,688 | 6,812
Net income and comprehensive income | 12,712 | 10,702 | 33,128 | 20,154
Weighted average number of common shares outstanding:
Basic | 4,502 | 5,276 | 5,125 | 5,249
Diluted | 4,929 | 5,677 | 5,456 | 5,678
Earnings per share of common stock
Basic | 2.82 | 2.03 | 6.46 | 3.84
Diluted | 2.58 | 1.89 | 6.07 | 3.55

FLEXSTEEL INDUSTRIES, INC. AND SUBSIDIARIES

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS (UNAUDITED)

(in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-08-19_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

The following table has been prepared as an aid in understanding the Company's results of operations on a comparative basis for the fiscal years ended June 30, 2026, 2025, and 2024. Amounts presented are percentages of the Company's net sales.

For the years ended June 30,
2026 | 2025 | 2024
Net sales | 100.0 | % | 100.0 | % | 100.0 | %
Cost of goods sold | 75.3 | 77.8 | 78.9
Gross margin | 24.7 | 22.2 | 21.1
Selling, general and administrative expenses | 15.4 | 15.1 | 17.1
Restructuring expense | — | — | 0.7
Right-of-use asset impairment | — | 3.2 | —
(Gain) on sale of real estate | — | (0.2 | —
(Gain) on disposal of assets held for sale | — | (2.0 | (0.8
Operating income | 9.3 | 6.0 | 4.1
Interest income | 0.3 | 0.1 | 0.0
Interest (expense) | — | — | (0.4
Income before income taxes | 9.5 | 6.1 | 3.8
Income tax provision | 2.3 | 1.5 | 1.2
Net income and comprehensive income | 7.2 | % | 4.6 | % | 2.6 | %

Fiscal 2026 Compared to Fiscal 2025

Net sales were $459.2 million for the year ended June 30, 2026, compared to net sales of $441.1 million in the prior year, an increase of $18.1 million or 4.1%. The increase in sales was primarily driven by $28.0 million of growth in soft seating products, partially offset by a $9.0 million decline in homestyles branded ready-to-assemble product sales and $0.9 million decline in Flexsteel branded casegoods.

Gross margin for the year ended June 30, 2026, was 24.7%, compared to 22.2% for the prior fiscal year, an increase of 250 basis points ("bps"). The 250-bps increase was primarily driven by a 200-bps benefit from the International Emergency Economic Powers Act ("IEEPA") Tariff Refunds received and to a lesser extent favorable mix driven by product and customer portfolio optimization initiatives.

Selling, general, and administrative ("SG&A") expenses increased by $4.2 million in the year ended June 30, 2026, compared to the prior fiscal year. As a percentage of net sales, SG&A expense was 15.4% in fiscal year 2026 compared to 15.1% of net sales in the prior fiscal year. The increase of 30-bps is primarily due to a 70-bps benefit from fixed cost leverage on higher sales volume offset by 70-bps increase in investments in consumer insights, new products and marketing to execute our growth strategy and a 30-bps increase from higher incentive compensation expense.

Income tax expense was $10.7 million, or an effective rate of 24.4%, for the year ended June 30, 2026, compared to income tax expense of $6.8 million in the prior year, or an effective tax rate of 25.3%. The current year effective tax rate was primarily impacted by lower non-deductible compensation, effect of state and foreign taxes, partially offset by stock-based compensation and a research and development credit benefit. The prior year tax rate was primarily impacted by the effect of state and foreign taxes, offset by a research and development credit benefit. The Company adjusted its provision for income tax and measurement of deferred tax assets in accordance with the One Big Beautiful Act ("OBBBA"). See Note 10, Income Taxes, of the Notes to Consolidated Financial Statements, included in this Annual Report on Form 10-K for more information.

Net income was $33.1 million, or $6.07 per diluted share for the year ended June 30, 2026, compared to net income of $20.2 million, or $3.55 per diluted share in the prior year.

On July 31, 2025, the President of the United States issued an executive order intended to clarify certain matters related to previously issued executive orders on tariffs. This executive order included, among other things, an increase in the country specific tariff from 10%

to 20% on goods imported from Vietnam. Accordingly, both our seating and case goods products sourced from Vietnam were subject to tariffs under IEEPA during this period. In addition, beginning in October 2025, substantially all of the seating products we source from Vietnam and manufacture in Mexico became subject to a 25% tariff under Section 232 of the Trade Expansion Act of 1962 pursuant to the Presidential Proclamation Adjusting Imports of Timber, Lumber, and their Derivative Products into the United States. For these seating products, the Section 232 tariff superseded the previously applicable IEEPA tariffs. Our case goods products sourced from Vietnam continued to be subject to the applicable IEEPA tariffs until February 2026, when the U.S. Supreme Court held that the tariffs imposed under IEEPA exceeded the authority granted under that statute. Following the Supreme Court's decision, a temporary 10% global import surcharge was imposed under Section 122 of the Trade Act of 1974 and became applicable to our case goods products sourced from Vietnam. On July 24, 2026, the U.S. implemented a new tariff framework under Section 301 of the Trade Act of 1974. The new framework imposes tariffs of either 10% or 12.5% on imports from certain trading partners, including Vietnam. This Section 301 tariff applies to bedroom, dining and occasional casegood products we source from Vietnam. The majority of our seating products sourced from Vietnam and manufactured in Mexico remain subject to the 25% Section 232 tariffs which, under the existing proclamation, is scheduled to increase to 30% effective January 1, 2027, unless modified prior to that date, and are generally not subject to the additional Section 301 tariffs. In addition, as a result of the U.S. Supreme Court's February 2026 decision regarding the IEEPA tariff program, the U.S. Court of International Trade ordered the U.S. government to process refunds of tariffs collected under the IEEPA tariff program. These refunds relate only to tariffs imposed under the IEEPA authority and do not affect the Section 232 tariffs that continue to apply to the majority of the Company's upholstered seating products.

Fiscal 2025 Compared to Fiscal 2024

Net sales were $441.1 million for the year ended June 30, 2025, compared to net sales of $412.8 million in the prior year, an increase of $28.3 million or 6.9%. The increase in sales was primarily driven by unit volume in our soft seating products, offset by a decline in our homestyles ready-to-assemble product line.

Gross margin for the year ended June 30, 2025, was 22.2%, compared to 21.1% for the prior fiscal year, an increase of 110 basis points ("bps"). The 110-bps increase was primarily driven by fixed cost leverage on higher sales, supply chain cost savings, and product portfolio management.

Selling, general, and administrative ("SG&A") expenses decreased by $3.7 million in the year ended June 30, 2025, compared to the prior fiscal year. As a percentage of net sales, SG&A expense was 15.1% in fiscal year 2025 compared to 17.1% of net sales in the prior fiscal year. The decrease of 200-bps is primarily due to fixed cost leverage on higher sales volume and structural cost savings partially offset by investments in growth initiatives. The prior year SG&A expense also included a $1.5 million expense due to CEO transition costs associated with the revaluation of previously awarded equity awards which did not recur in the year ended June 30, 2025.

In July 2022, Flexsteel commenced a 12-year lease for a manufacturing facility in Mexicali, Mexico to support strong demand growth which was elevated due to pandemic-driven buying at that time. Subsequently, U.S. furniture demand reverted to pre-pandemic norms, and the Company's plan for the facility pivoted to subleasing the space short-term while maintaining the option to utilize it longer term to support growth. While the Company secured multiple short-term sublease tenants at the beginning of the lease term, substantial changes in U.S. trade policy in early 2025 created significant uncertainty in US-Mexico trade relations, slowed foreign direct investment in Mexico, and greatly diminished tenant interest in subleasing the Mexicali facility. As a result, management concluded that the right of use asset related to this lease was not fully recoverable and recorded a pre-tax non-cash asset impairment charge of $14.1 million during the quarter ended March 31, 2025. See Note 2, Leases, of the Notes to Consolidated Financial Statements, included in this Annual Report on Form 10-K for more information.

During the year ended June 30, 2025, the Company completed the sale of its Dublin, Georgia facility which had been previously recorded as held for sale. The Company recorded a pre-tax gain of $5.0 million related to the sale. See Note 6, Assets Held For Sale , of the Notes to Consolidated Financial Statements, included in this Annual Report on Form 10-K for more information.

During the year ended June 30, 2025, the Company completed the sale of 2 separate ancillary buildings, formerly part of its Huntingburg, Indiana distribution center complex. The Company received proceeds of $0.8 million and recorded a pre-tax gain of $0.7 million related to the first sale. The Company received proceeds of $4.0 million and recorded a pre-tax gain of $3.7 million related to the second sale. The Company has adequate distribution capacity to support our growth as we continue to optimize our distribution and logistics network. See Note 6, Assets Held For Sale , of the Notes to Consolidated Financial Statements, included in this Annual Report on Form 10-K for more information.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-08-19_item1_business.md)

Item 1. Business

General

Flexsteel Industries, Inc. and Subsidiaries (the "Company," "Flexsteel," or "Our") is one of the largest residential furniture manufacturers, importers, and marketers in the U.S. Flexsteel addresses different consumer groups through our core brand, Flexsteel, and several category-specific sub-brands: Zecliner, Statements, Zen, Perfect Match, and Pulse, all of which have unique value propositions tailored to specific consumer needs. We offer a wide assortment of product solutions for different areas within the home including stationary and motion sofas, loveseats, chairs, and sectionals, as well as bedroom furniture, dining tables and chairs, occasional and entertainment tables, and kitchen storage. For more than 130 years, Flexsteel has strived to create strong consumer value with unmatched quality, comfort, and durability, backed by innovation and highlighted by its patented Blue Steel Spring technology, designed to deliver lasting comfort and support. Today, Flexsteel products are available nationwide through retail partners and online channels.

The Company operates in one reportable segment, furniture products. The Company's furniture products business involves the distribution of manufactured and imported products consisting of a broad line of furniture for the residential market.

Manufacturing and Offshore Sourcing

During the fiscal year ended June 30, 2026, the Company operated manufacturing facilities located in Juarez, Mexico. This ongoing manufacturing operation is integral to the Company's product offerings and distribution strategy by offering smaller and more frequent product runs of a wider product selection. The Company identifies and eliminates manufacturing inefficiencies and adjusts manufacturing schedules frequently to meet customer requirements. The Company has established relationships with key suppliers to ensure prompt delivery of quality component parts. The Company's production includes the use of selected component parts sourced offshore to enhance value in the marketplace.

The Company integrates manufactured products with finished products acquired from offshore suppliers who can meet quality specifications and lead-time requirements. The Company will continue to pursue and refine this blended product offering and supply chain strategy, offering customers the requisite amount of choice of made-to-order manufactured goods, and ready-to-deliver imported products. This blended focus on products allows the Company to provide a wide range of price points, styles and product categories to satisfy customer requirements.

Competition

The furniture industry is highly competitive and includes a large number of U.S. and foreign manufacturers and distributors, none of which dominate the market. The Company competes in markets with a large number of relatively small manufacturers; however, certain competitors have substantially greater sales volumes than the Company. The Company's products compete based on style, quality, comfort, functionality, price, delivery, service and durability. The Company believes its patented, guaranteed-for-life Blue Steel Spring,

manufacturing and sourcing capabilities, facility locations, commitment to customers, product quality, consumer insights, innovation, delivery, service, value and experienced production, sales, marketing and management teams, are some of its competitive advantages.

Seasonality

The Company's overall business is not considered materially seasonal.

Foreign Operations

The Company has minimal export sales. On June 30, 2026, the Company had approximately 30 employees located in Asia to ensure Flexsteel's quality standards are met and to coordinate the delivery of products acquired from overseas suppliers. The Company leases and operates three manufacturing facilities in Juarez, Mexico and leases one manufacturing facility in Mexicali, Mexico. The Company had approximately 900 employees located in Mexico on June 30, 2026. The four Mexico facilities total 1,061,000 square feet. As of June 30, 2026, the Company has not begun operations in the Mexicali facility and expects to sublease the facility until such time that demand necessitates the additional capacity. See "Risk Factors" in Item 1A and Note 2, Leases, of the Notes to Consolidated Financial Statements included in this Annual Report on Form 10-K for further discussion of the leased assets.

Customer Backlog

The approximate backlog of customer orders believed to be firm as of the end of the current fiscal year and the prior two fiscal years were as follows (in thousands):

June 30, 2026 | June 30, 2025 | June 30, 2024
70,105 | 66,465 | 59,543

Raw Materials

The Company utilizes various types of wood, fabric, leather, filling material, high carbon spring steel, bar and wire stock, polyurethane foam and other raw materials in manufacturing furniture. The Company purchases these materials from numerous outside suppliers, both U.S. and foreign, and is not dependent upon any single source of supply. The costs of certain raw materials fluctuate, but all continue to be readily available within supplier lead-times; however, we could experience supply-chain disruptions at any time, which could impact the availability of materials.

Artificial Intelligence ("AI")

The Company is leveraging AI to strengthen the efficiency and effectiveness of its operational execution.

Industry Factors

The Company has exposure to actions by governments, including tariffs, see "Risk Factors" in Item 1A of this Annual Report on Form 10-K.

Government Regulations

The Company is subject to various local, state, and federal laws, regulations and agencies that affect businesses generally, see "Risk Factors" in Item 1A of this Annual Report on Form 10-K. Our compliance with federal, state and local laws and regulations did not have a material effect upon our capital expenditures, earnings or competitive position during the fiscal year ended June 30, 2026.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-08-19_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-08-19_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-08-19_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-17_2-02-results.md, 10-K_2026-08-19_item7_mdna.md, 10-K_2026-08-19_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
