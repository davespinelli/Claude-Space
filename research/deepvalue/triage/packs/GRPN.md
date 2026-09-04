# Triage pack — GRPN · Groupon, Inc.

_Generated 2026-09-04 19:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** GRPN · **Name:** Groupon, Inc.
- **CIK:** 0001490281
- **SIC:** 7311 — Services-Advertising Agencies
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/GRPN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Groupon, Inc.
- **CIK:** 1,490,281 · **SIC:** 7311 (Services-Advertising Agencies) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 18.86 |
| mktcap | $766.9M |
| ev | $802.1M |
| ev_ebit | 33.9x |
| fcf | $49.9M |
| fcf_yield | 6.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $35.1M |
| net_debt_ebit | 1.5x |
| cash | $226.2M |
| ltd | $261.4M |
| equity | -$72.2M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $498.4M |
| revenue_prior | $492.6M |
| rev_growth | 1.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $23.6M |
| net_income | -$83.2M |
| cfo | $64.5M |
| capex | $14.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 40,665,296 |
| shares_py | 40,425,985 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 11.5% |
| r6m | 52.2% |
| off_52w_high | -34.0% |
| adv20 | $26.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.56 |
| r_ev_ebit | 0.25 |
| r_roic | 0.50 |
| r_rev_growth | 0.39 |
| r_buyback | 0.54 |
| score | 0.50 |

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
| rank | 246 |

**Screen rationale:** 12-1 momentum 11.5%


## 3. Share count trend

- Shares outstanding: **40,665,296** (CY2026Q2I) vs **40,425,985** prior year (CY2025Q2I)
- Change: **0.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-08** — Item 5.02 (officer / director change or comp arrangement): On June 8, 2026, Groupon, Inc. (the "Company") announced the appointment of Aditya Rajkumar as Chief Operating Officer, effective August 3, 2026 (the "Effective Date").
- **2026-05-26** — Item 5.02 (officer / director change or comp arrangement): On May 21, 2026, Jiri Ponrt, Chief Operating Officer of the Company, notified the Company of his decision to resign from his employment with the Company, effective July 10, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 32 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 12 |
| F | 5 |
| M | 15 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Groupon Reports Second Quarter 2026 Results'; skipped 19 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (a2026q28-kxexhibit991.htm)

Groupon Reports Second Quarter 2026 Results

Global Revenue and Billings down 1%

Loss from continuing operations was $1.5 million and Adjusted EBITDA was $14.8 million, at the high end of guidance

Project Foundry, our AI-native transformation, is beginning to deliver better outcomes for customers and faster execution across the company

CHICAGO - August 6, 2026 - Groupon, Inc. (NASDAQ: GRPN) today announced its financial results for the second quarter ended June 30, 2026. Results and a shareholder letter for the second quarter are posted on Groupon's Investor Relations site (investor.groupon.com). The Company has also filed its Form 10-Q with the Securities and Exchange Commission.

"Project Foundry, our AI-native redesign of how Groupon operates, remains the most consequential work underway at the company, and just over four months in we are extremely pleased with the progress we have made," said Dusan Senkypl, Chief Executive Officer of Groupon. "While Q2 fell slightly short on the top line, we entered the third quarter with momentum and expect growth to accelerate in the second half. We continue to make meaningful progress across our strategic bets, with organic channels returning to growth, managed channels continuing to improve and personalization scaling across our consumer platform, giving us confidence in our outlook for the second half of 2026."

Second Quarter 2026 Highlights

• Global Revenue down 1% and Billings down 1% (down 1% FX-neutral) year-over-year.

• North America Local Revenue down 2% and Local Billings down 1%, reflecting softness in Health, Beauty & Wellness, partially offset by strength in Things to Do and recovery within our organic and managed channels.

• International Local Revenue up 8% and Local Billings up 2% (down 1% FX-neutral). Excluding Giftcloud, International Local Revenue up 9% and International Local Billings up 5%, driven by improved organic performance from our new consumer platform and an expansion of seasonally relevant supply across major International cities, led by our Health, Beauty & Wellness and Things to Do offerings.

• Active customers grew 2% to 16.1 million, with growth in both North America and International Local categories.

• Unit sales were 8.5 million, down 7% year-over-year, reflecting lower transaction volume in North America and International, partially offset by an increase in average order value as customers purchased higher-value local inventory.

• Loss from continuing operations was $1.5 million, compared with income from continuing operations of $20.6 million in the prior year period.

• Adjusted EBITDA, a non-GAAP financial measure, was positive $14.8 million, compared with positive $15.6 million in the prior year period.

• Operating cash inflow from continuing operations was $18.1 million and free cash flow, a non-GAAP financial measure, was positive $15.0 million.

• Cash and cash equivalents as of June 30, 2026 were $226.3 million.

• The restructuring plan we announced in May is underway and on track. The payroll actions are estimated to result in $20.0 million to $25.0 million in annualized cost savings. We recorded $3.2 million of restructuring charges in the second quarter under our 2026 Restructuring Plan. The Company estimates total pre-tax charges of $7.0 million to $13.0 million, with a majority of the related headcount reductions expected by the end of the third quarter.

• Made progress across Project Foundry and our strategic bets to deepen customer engagement and drive durable growth: the rollout of our new consumer platform nears completion with conversion improving on nearly every surface, organic channels returned to growth, managed channels continued to improve, and we scaled new personalization and trust and quality capabilities.

Definitions and reconciliations of all non-GAAP financial measures and additional information regarding operating measures are included below in the section titled "Non-GAAP Financial Measures and Operating Metrics" and in the accompanying tables.

2026 Outlook 1

For the third quarter and full year 2026, the Company expects:

As of August 6, 2026 | Q3 2026 Guidance | 2026 Guidance
Low-end | High-end | Low-end | High-end
Billings | +4% | +6% | +3% | +5%
Revenue | $128M | $130M | $513M | $523M
+4% | +6% | +3% | +5%
Adjusted EBITDA | $19M | $21M | $75M | $80M
Free Cash Flow | Negative | At least $60M

1 We do not provide a reconciliation for non-GAAP estimates on a forward-looking basis where we are unable to provide a meaningful calculation or estimation of reconciling items and the information is not available without unreasonable effort. This is due to the inherent difficulty of forecasting the timing or amount of various items that would impact the most directly comparable forward-looking U.S. GAAP financial measure that have not yet occurred, are out of the Company's control and/or cannot be reasonably predicted. Forward-looking non-GAAP financial measures provided without the most directly comparable U.S. GAAP financial measures may vary materially from the corresponding U.S. GAAP financial measures. Reconciling items to the amounts above include foreign currency gains and losses, restructuring and other cost savings-related charges, investment-related activity such as observable price changes, gains and losses on discrete transactions, certain income tax items, and impairment or other charges.

Stock-based compensation. We exclude stock-based compensation because it is primarily non-cash in nature and we believe that non-GAAP financial measures excluding this item provide meaningful supplemental information about our operating performance and liquidity.

Depreciation and amortization. We exclude depreciation and amortization expenses because they are non-cash in nature and we believe that non-GAAP financial measures excluding these items provide meaningful supplemental information about our operating performance and liquidity.

Income taxes, interest, and other non-operating items. Income taxes, interest, and other non-operating items include: income taxes, foreign currency gains and losses, loss on extinguishment of debt, interest income and interest expense. We exclude interest and other non-operating items from certain of our non-GAAP financial measures because we believe that excluding these items provides meaningful supplemental information about our core operating performance and facilitates comparisons to our historical operating results.

Special charges and credits. We exclude special charges and credits related to our 2026 Restructuring Plan, Italy Restructuring Plan, 2022 Restructuring Plan and 2020 Restructuring Plan, as well as gain on sale of assets, and gain on sale of business. We exclude special charges and credits from Adjusted EBITDA because we believe that excluding those items provides meaningful supplemental information about our core operating performance and facilitates comparisons with our historical results.

Descriptions of the non-GAAP financial measures included in this release and the accompanying tables are as follows:

Foreign currency exchange rate neutral operating results show current period operating results as if foreign currency exchange rates had remained the same as those in effect in the prior year period. Those measures are intended to facilitate comparisons to our historical performance.

Adjusted EBITDA is a non-GAAP performance measure that we define as Income (loss) from continuing operations excluding income taxes, interest and other non-operating items, depreciation and amortization, stock-based compensation and other special charges and credits, including items that are unusual in nature or infrequently occurring. Our definition of Adjusted EBITDA may differ from similar measures used by other companies, even when similar terms are used to identify such measures. Adjusted EBITDA is a key measure used by our management and Board to evaluate operating performance, generate future operating plans and make strategic decisions. Accordingly, we believe that Adjusted EBITDA provides useful information to investors and others in understanding and evaluating our operating results in the same manner as our management and Board. However, Adjusted EBITDA is not intended to be a substitute for Income (loss) from continuing operations.

Free cash flow is a non-GAAP liquidity measure that comprises Net cash provided by (used in) operating activities from continuing operations less purchases of property and equipment and capitalized software. We use free cash flow to conduct and evaluate our business because, although it is similar to Net cash provided by (used in) operating activities from continuing operations, we believe that it typically represents a more useful measure of cash flows because purchases of fixed assets, software developed for internal use and website development costs are necessary components of our ongoing operations. Free cash flow is not intended to represent the total increase or decrease in our cash balance for the applicable period.

Descriptions of the operating metrics included in this release and the accompanying tables are as follows:

Gross billings is the total dollar value of customer purchases of goods and services. Gross billings is presented net of customer refunds, order discounts and sales and related taxes. The substantial majority of our revenue transactions are comprised of sales of vouchers and similar transactions in which we collect the transaction price from the customer and remit a portion of the transaction price to the third-party merchant who will provide the related goods or services. For these transactions, gross billings differs from Revenue reported in our Condensed

Consolidated Statements of Operations, which is presented net of the merchant's share of the transaction price. Gross billings is an indicator of our growth and business performance as it measures the dollar volume of transactions generated through our marketplaces. Tracking gross billings also allows us to monitor the percentage of gross billings that we are able to retain after payments to merchants.

Active customers are unique user accounts, identified by a distinct email address, that have made a purchase during the trailing twelve months ("TTM") either through one of our online marketplaces or directly with a merchant for which we earned a commission. We consider this metric to be an important indicator of our business performance as it helps us to understand how the number of customers actively purchasing our offerings is trending. Some customers could establish and make purchases from more than one account, so it is possible that our active customer metric may count certain customers more than once in a given period. We do not include consumers who solely make purchases with retailers using digital coupons accessed through our websites or mobile applications in our active customer metric, nor do we include consumers who solely make purchases of our inventory through third-party marketplaces with which we partner.

Units are the number of purchases during the reporting period, before refunds and cancellations, made either through one of our online marketplaces, a third-party marketplace, or directly with a merchant for which we earn a commission. We do not include purchases with retailers using digital coupons accessed through our websites or mobile applications in our units metric. We consider units to be an important indicator of the total volume of business conducted through our marketplaces.

press@groupon.com

Groupon, Inc.

Non-GAAP Reconciliation Schedules

(in thousands)

(unaudited)

The following is a quarterly reconciliation of Adjusted EBITDA to the most comparable U.S. GAAP performance measure, Income (loss) from continuing operations:

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-10_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Groupon is a global scaled two-sided marketplace that connects consumers to merchants. Consumers access our marketplace through our mobile applications and our websites. We operate in two segments, North America and International, and in three categories, Local, Goods and Travel. See Item 8, Note 19, Segment and Geographical Information, for additional information.

We generate service revenue from Local, Goods and Travel categories. Revenue primarily represents the net commissions earned from selling goods or services on behalf of third-party merchants. Revenue is reported on a net basis as the purchase price collected from the customer less the portion of the purchase price that is payable to the third-party merchant. We also earn commissions when customers make purchases with retailers using digital coupons accessed through our websites and mobile applications.

How We Measure Our Business

We use several operating and financial metrics to assess the progress of our business and make strategic decisions. Certain of the financial metrics are reported in accordance with GAAP and certain of those metrics are considered non-GAAP financial measures. As our business evolves, we may make changes to the key financial and operating metrics that we use to measure our business. For further information and reconciliations to the most applicable financial measures under GAAP, refer to our discussion under Non-GAAP Financial Measures in the Results of Operations section.

Operating Metrics

• Gross billings is the total dollar value of customer purchases of goods and services. Gross billings is presented net of customer refunds, order discounts and sales and related taxes. The substantial majority of our revenue transactions are comprised of sales of vouchers and similar transactions in which we collect the transaction price from the customer and remit a portion of the transaction price to the third-party merchant who will provide the related goods or services. For these transactions, gross billings differs from Revenue reported in our Consolidated Statements of Operations, which is presented net of the merchant's share of the transaction price. Gross billings is an indicator of our growth and business performance as it measures the dollar volume of transactions generated through our marketplaces. Tracking gross billings also allows us to monitor the percentage of gross billings that we are able to retain after payments to merchants.

• Units are the number of purchases during the reporting period, before refunds and cancellations, made either through one of our online marketplaces, a third-party marketplace, or directly with a merchant for which we earn a commission. We do not include purchases with retailers using digital coupons accessed through our websites or mobile applications in our units metric. We consider units to be an important indicator of the total volume of business conducted through our marketplaces.

• Active customers are unique user accounts, identified by a distinct email address, that have made a purchase during the TTM either through one of our online marketplaces or directly with a merchant for which we earned a commission. We consider this metric to be an important indicator of our business performance as it helps us to understand how the number of customers actively purchasing our offerings is trending. Some customers could establish and make purchases from more than one account, so it is possible that our active customer metric may count certain customers more than once in a given period. We

do not include consumers who solely make purchases with retailers using digital coupons accessed through our websites or mobile applications in our active customer metric, nor do we include consumers who solely make purchases of our inventory through third-party marketplaces with which we partner.

Our gross billings, units and TTM active customers for the years ended December 31, 2025 and 2024 were as follows (in thousands):

Year Ended December 31,
2025 | 2024
Gross billings | 1,665,755 | 1,558,203
Units | 36,826 | 36,640
TTM Active customers | 16,229 | 15,432

Financial Metrics

• Revenue is earned through transactions for which we generate commissions by selling goods or services on behalf of third-party merchants. Revenue from those transactions is reported on a net basis as the purchase price collected from the customer for the offering less an agreed upon portion of the purchase price paid to the third-party merchant. Revenue also includes commissions we earn when customers make purchases with retailers using digital coupons accessed through our digital properties.

• Cost of revenue consists of direct and certain indirect costs incurred to generate revenue. Costs incurred to generate revenue, which include credit card processing fees, editorial costs, compensation expense for technology support personnel who are responsible for maintaining the infrastructure of our websites, amortization of internal-use software relating to customer-facing applications, web hosting and other processing fees are attributed to the cost of service.

• Gross profit reflects the net margin we earn after deducting our Cost of revenue from our Revenue.

• Contribution Profit measures the amount of marketing investment needed to generate revenue and is defined as net revenues less cost of sales and marketing expense. See Item 8, Note 19, Segment and Geographical Information , for additional information.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

North America

Operating Metrics

North America segment gross billings, units and TTM active customers for the years ended December 31, 2025 and 2024 were as follows (in thousands, except percentages):

Year Ended December 31, | % Change
2025 | 2024 | 2025 vs 2024
Gross billings
Local | 1,142,285 | 999,836 | 14.2 | %
Goods | 34,077 | 53,589 | (36.4)
Travel | 77,817 | 79,347 | (1.9)
Total gross billings | 1,254,179 | 1,132,772 | 10.7
Units
Local | 23,516 | 21,805 | 7.8 | %
Goods | 943 | 1,882 | (49.9)
Travel | 302 | 321 | (5.9)
Total units | 24,761 | 24,008 | 3.1
TTM Active customers | 11,051 | 10,289 | 7.4 | %

Comparison of the Years Ended December 31, 2025 and 2024:

North America gross billings, units and TTM active customers increased by $121.4 million, 0.8 million and 0.8 million, respectively, for the year ended December 31, 2025 compared with the prior year period. Our Local category experienced growth in gross billings and units driven by our continued execution of our hyperlocal marketplace strategy and increased marketing spend, with strength in our core local business supported by improved supply quality and effective category management. The Local category growth is partially offset by a de-emphasis on our Goods category evidenced by a decrease of our Goods active customers that resulted in fewer unit sales and lower gross billings year over year in the Goods category.

Financial Metrics

North America segment revenue, cost of revenue and gross profit for the years ended December 31, 2025 and 2024 were as follows (in thousands, except percentages):

Year Ended December 31, | % Change
2025 | 2024 | 2025 vs 2024
Revenue
Local | 366,787 | 350,876 | 4.5 | %
Goods | 5,484 | 10,990 | (50.1)
Travel | 13,560 | 14,206 | (4.5)
Total revenue | 385,831 | 376,072 | 2.6
Cost of revenue
Local | 31,695 | 34,070 | (7.0) | %
Goods | 705 | 1,405 | (49.8)
Travel | 1,712 | 2,433 | (29.6)
Total cost of revenue | 34,112 | 37,908 | (10.0)
Gross profit
Local | 335,092 | 316,806 | 5.8 | %
Goods | 4,779 | 9,585 | (50.1)
Travel | 11,848 | 11,773 | 0.6
Total gross profit | 351,719 | 338,164 | 4.0
% of Consolidated revenue | 77.4 | % | 76.4 | %
% of Consolidated cost of revenue | 74.3 | 78.6
% of Consolidated gross profit | 77.7 | 76.1

Comparison of the Years Ended December 31, 2025 and 2024:

North America revenue and gross profit increased by $9.8 million, and $13.6 million, respectively, while cost of revenue decreased by $3.8 million for the year ended December 31, 2025 compared with the prior year period. Our Local revenue increased by 4.5%, lagging the rate of growth in gross billings as a result of promotional discounts and higher redemption rates. The decrease in cost of revenue is primarily due to a decrease in amortization of internally-developed software relating to customer-facing applications, which is a direct result of our cost savings initiatives. Gross profit increased due to an increase in revenue and decrease in cost of revenue. The decline in our Goods category is primarily attributable to our overall de-emphasis of the Goods category.

Marketing and Contribution Profit

North America marketing and contribution profit for the years ended December 31, 2025 and 2024 were as follows (in thousands, except percentages):

Year Ended December 31, | % Change
2025 | 2024 | 2025 vs 2024
Marketing | 127,608 | 113,096 | 12.8 | %
% of Revenue | 33.1 | % | 30.1 | %
Contribution Profit | 224,111 | 225,068 | (0.4) | %

Comparison of the Years Ended December 31, 2025 and 2024:

North America marketing expense increased for the year ended December 31, 2025 compared with the prior year period, primarily due to increased investment in our online marketing spend to drive customer acquisition and demand growth. Marketing expense as a percentage of revenue increased as revenue growth did not keep pace with our marketing investment as strong performance in paid channels was offset by headwinds in non-paid channels.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-10_item1_business.md)

ITEM 1. BUSINESS

Groupon is a global scaled two-sided marketplace that connects consumers to merchants. Consumers access our marketplace through our mobile applications and our websites, which are primarily localized groupon.com sites in thirteen countries. We operate in two segments, North America and International, and in three categories, Local, Goods and Travel. See Item 8, Note 19, Segment and Geographical Information, for additional information.

Revenue is earned through transactions during which we generate commissions by selling goods or services on behalf of third-party merchants. Revenue also includes commissions we earn when customers make purchases with retailers using digital coupons accessed through our digital properties.

Our Strategy

Our strategy is to be the trusted local experience marketplace where customers go to buy quality local services and experiences at unbeatable value. We plan to grow our revenue by building long-term relationships with local merchants to strengthen our online selection and by enhancing the customer reach through experience curation and improved convenience in order to drive customer demand and purchase frequency.

We continue to invest in making our platform more efficient, stable and agile. By improving our technology, our customer base can enjoy a modernized experience along with seamless execution of new product innovation, improved customer experience and customer satisfaction. Central to this is our continued investment in our product and engineering organization, building the development velocity, platform depth, and technical capabilities required to deliver faster innovation and more personalized experiences for both customers and merchants. Our product agenda is focused on driving growth through smarter discovery, deeper personalization, and an increasingly seamless experience across every surface we serve.

We believe the next generation of local commerce will be driven by AI native experiences, for which AI agents will become an important discovery and transaction channel. We are building and beginning to implement modern API architecture, AI-ready search & relevance, AI-ready checkout in addition to internal AI tools to drive productivity and efficiency. We are investing now with the goal of Groupon being well positioned to be the partner of choice for local experiences as this channel scales.

Our Categories

Local . Our Local category includes experiences and services from local and national merchants, and other revenue sources that are primarily generated through our relationships with local and national merchants. Our local inventory includes, things to do, beauty and wellness, food and drink, home and automotive services, online services, as well as other types of experiences and services.

Goods . In our Goods category, we earn revenue from transactions in which third-party merchants sell products to customers through our marketplaces. Our Goods category includes merchandise across multiple product lines, such as electronics, sporting goods, jewelry, toys, household items and apparel.

Travel . Through our Travel category, we feature travel experiences at both discounted and market rates, including hotels, airfare and package deals covering both domestic and international travel. For many of our travel experiences, the customer makes reservations directly through our websites and mobile applications. However, for some travel experiences, customers must contact the merchant directly to make a travel reservation after purchasing a travel voucher from us.

Traffic Channels and Platforms

Our customers access our online local commerce marketplaces through our mobile applications and our websites. Our applications and mobile websites enable consumers to browse, purchase, manage and redeem deals on their mobile devices. For the year ended December 31, 2025, approximately 84% of our global transactions were completed on mobile devices.

We use a variety of marketing channels to direct customers to the offerings available through these marketplaces, as described in the Marketing section below.

Marketing

We use marketing to acquire and retain customers and promote awareness of our marketplaces and brand. We use a variety of marketing channels to make customers aware of our offerings, including search engines, email and push notifications, affiliate channels, social and display advertising and offline marketing.

Search engines. Customers can access our offerings indirectly through third-party search engines. We use SEO and SEM to increase the visibility of our offerings in web search results.

Email and mobile messaging. We communicate offerings through email, push notifications and SMS to our customers based on their locations and personal preferences. A customer who interacts with these communications is directed to our website or mobile application to learn more about the deal and to make a purchase.

Affiliate channels. We have an affiliate program that uses third parties to promote our offerings online. Affiliates earn commissions when customers access our offerings through links on their websites and make purchases on our platform.

Social and display. We promote and publish our content and offerings through various social networks and adapt our notifications to the particular format of each of these social networking platforms. Our websites and mobile applications enable consumers to share our offerings with their personal social networks. We also promote our offerings via display advertising across various content publishers.

Human Capital Management

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-10_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-10_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-10_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-10_item7_mdna.md, 10-K_2026-03-10_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
