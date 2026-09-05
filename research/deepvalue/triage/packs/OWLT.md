# Triage pack — OWLT · Owlet, Inc.

_Generated 2026-09-05 02:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** OWLT · **Name:** Owlet, Inc.
- **CIK:** 0001816708
- **SIC:** 3829 — Measuring & Controlling Devices, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/OWLT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Owlet, Inc.
- **CIK:** 1,816,708 · **SIC:** 3829 (Measuring & Controlling Devices, NEC) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 5.03 |
| mktcap | $147.0M |
| ev | $116.0M |
| ev_ebit | n/a |
| fcf | -$11.1M |
| fcf_yield | -7.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$30.9M |
| net_debt_ebit | n/a |
| cash | $30.9M |
| ltd | $0.00 |
| equity | $23.1M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $106.2M |
| revenue_prior | $77.4M |
| rev_growth | 37.1% |
| rev_growth_note | share count +71.4% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$7.4M |
| net_income | -$38.8M |
| cfo | -$10.8M |
| capex | $273k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 71.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 29,221,677 |
| shares_py | 17,044,460 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -27.1% |
| r6m | -57.2% |
| off_52w_high | -69.6% |
| adv20 | $1.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.10 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.91 |
| r_buyback | 0.02 |
| score | 0.21 |

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
| rank | 463 |

**Screen rationale:** revenue +37.1% BUT share count +71.4% yoy — growth may be acquisition/issuance-driven, not organic; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **29,221,677** (CY2026Q2I) vs **17,044,460** prior year (CY2025Q2I)
- Change: **71.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +71.4% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-14** — Item 5.02 (officer / director change or comp arrangement): On August 12, 2026, Owlet, Inc. (the "Company") held its 2026 annual meeting of stockholders (the "Annual Meeting").
- **2026-07-01** — Item 1.01 (Entry into a Material Definitive Agreement): On June 26, 2026, Owlet, Inc., a Delaware corporation (the "Company"), and its wholly-owned subsidiary Owlet Baby Care, Inc., a Delaware corporation ("OBCI"), entered into new a debt financing arrangement and refinanced (i) OBCI's existing line of credit with...
- **2026-04-06** — Item 5.02 (officer / director change or comp arrangement): On April 3, 2026, the Board of Directors (the "Board") of the Owlet, Inc. (the "Company") appointed Kurt Workman as President and Chief Executive Officer effective April 6, 2026 (the "Effective Date") to succeed Jonathan Harris in these positions.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 90,688 sh / $824,094 -> net $-824,094 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 33 (open-market buys 0, sales 16).

| code | rows |
|---|---|
| A | 16 |
| F | 1 |
| S | 16 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-11_2-02-results.md)

_Extraction: started at the first release heading, 'Q2 2026 Financial Highlights:'; skipped 12 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex-991q226earningspressrel.htm)

Q2 2026 Financial Highlights:

• Record Q2 Revenue of $33.9 million, up 29.9% from Q2 2025

• Record Q2 Subscription Revenue of $3.2 million, up $2.4 million from Q2 2025

• Q2 Gross Margin of 64.4%. Excluding $3.5 million in tariff refund impact, gross margin of 54.0%, up 270 basis points from Q2 2025

• Q2 Net Loss of $0.6 million. Excluding $3.75 million in tariff refund impact, net loss of $4.4 million, compared to net loss of $37.4 million in Q2 2025

• Record Q2 Adjusted EBITDA (non-GAAP) of $2.9 million excluding $3.75 million in tariff refund impact, compared to $0.5 million in Q2 2025; $6.7 million of Adjusted EBITDA including tariff refund impact

"Owlet delivered an exceptional second quarter, with record quarterly revenue, gross profit, and adjusted EBITDA," said Kurt Workman, Owlet's President, Chief Executive Officer, and Co-Founder. "We are executing across each of our strategic growth areas, and it is showing up in our results — strong topline growth, standout international momentum, and continued Owlet360 subscription platform growth. We believe our biggest opportunity from here is growing subscribers, and that is exactly where the company is focused."

"We believe our competitive position has never been stronger," Workman continued. "We have the first and only FDA-cleared baby monitor on the market, and we set another record for market share in the quarter. Owlet has numerous growth levers – winning new families, building the subscription platform with Owlet360, expanding the opportunity in pediatric telehealth, and scaling internationally – all anchored by our unique pediatric dataset."

"Our strategy from here is straightforward: firmly position Owlet as a data and services platform through subscription, win approximately one million new customers per year, and keep those families with us for at least two years. Over time, we believe executing that framework points toward a recurring base of more than one million subscribers, and a more durable, higher-value Owlet."

Financial Results for the Second Quarter Ended June 30, 2026

Revenue for the second quarter of 2026 was $33.9 million, compared to revenue in the second quarter of 2025 of $26.1 million, an increase of 29.9%. The increase was due to broad-based growth and continued momentum in subscription.

Subscription revenue for the second quarter of 2026 was $3.2 million, compared to subscription revenue in the second quarter of 2025 of $0.9 million, an increase of $2.4 million.

Cost of revenue for the second quarter of 2026 was $12.0 million with a GAAP gross margin of 64.4%, compared to cost of revenue of $12.7 million with a GAAP gross margin of 51.3% for the second quarter of 2025. Overall gross margin was 54.0%, excluding $3.5 million in tariff refund impacts, increasing approximately 270 basis points year-over-year, primarily reflecting growth in revenue from our Owlet360 subscription service as well as favorable product mix and fixed cost absorption.

Subscription gross margin for the second quarter of 2026 was 68.4%.

Operating expenses, including stock-based compensation, were $20.1 million for the second quarter of 2026, compared to $15.1 million for the same period in 2025. Operating costs increased year-over-year primarily due to higher marketing spend as Prime Day promotional timing shifted from Q3 into Q2, as well as severance costs, including stock-based compensation.

Operating income was $1.7 million for the second quarter of 2026, compared to operating loss of $1.7 million for the second quarter of 2025.

Net loss was $0.6 million for the second quarter of 2026, compared to net loss of $37.4 million for the second quarter of 2025.

Adjusted EBITDA (non-GAAP) was $6.7 million for the second quarter of 2026, compared to $0.5 million for the second quarter of 2025. Excluding $3.75 million in tariff refund impact, Adjusted EBITDA (non-GAAP) was $2.9 million.

Net loss per share was $0.05 for the second quarter of 2026, compared to net loss per share of $2.35 for the second quarter of 2025. Adjusted net income per share (non-GAAP) was $0.20 for the second quarter of 2026, compared to adjusted net loss per share of $0.04 for the same period in 2025.

Updated 2026 Financial Outlook

Our updated full year 2026 financial outlook below reflects the one-time IEEPA tariff refund recognized in the second quarter of 2026 and a measured view of the second half. Excluding the refund, our underlying expectations for the year are essentially unchanged.

• Total Revenue is expected to be in the range of $118 to $122 million, unchanged from our previous guidance.

• Gross Margin is expected to be in the range of 53% to 55%, compared to our previous guidance of 50% to 52%. The increase reflects only the one-time $3.5 million tariff refund benefit to COGS recognized in the second quarter.

• Adjusted EBITDA is expected to be in the range of $10.75 to $12.75 million, compared to our previous guidance of $7 to $9 million. The increase reflects only the one-time $3.75 million tariff refund benefit to Adjusted EBITDA recognized in the second quarter.

The Company's non-GAAP financial measures should not be considered as an alternative to net income (loss) or net income (loss) per share as a measure of financial performance or any other performance measure derived in accordance with GAAP and should not be construed as an inference that the Company's future results will be unaffected by unusual or non-recurring items.

Adjusted EBITDA is defined as net income (loss) adjusted for income tax provision, interest expense, net, depreciation and amortization, impairment of intangible assets, common stock warrant liability adjustment, stock-based compensation, charges related to certain legal matters, restructuring costs, and loss on debt extinguishment.

- 4 -

Adjusted net income (loss) is defined as net income (loss) adjusted for impairment of intangible assets, common stock warrant liability adjustment, stock-based compensation, charges related to certain legal matters, restructuring costs, and loss on debt extinguishment. Adjusted net income (loss) per share is defined as adjusted net income (loss) divided by the basic weighted-average number of shares of common stock outstanding.

Adjusted EBITDA, adjusted net income (loss) and adjusted net income (loss) per share are not recognized terms under GAAP, and the Company's presentation of these non-GAAP measures does not replace the presentation of the Company's financial results in accordance with GAAP. Because all companies do not use adjusted EBITDA, adjusted net income (loss) and adjusted net income (loss) per share (and similarly titled financial measures) in the same way, those measures as used by other companies may not be consistent with the way the Company calculates such measures. The non-GAAP financial measures included in this release should not be construed as substitutes for or better indicators of the Company's performance than the most directly comparable GAAP financial measures. See the reconciliation tables that accompany this release for additional information regarding certain of the non-GAAP financial measures included herein.

A reconciliation of the Company's guidance contained in this press release with respect to non-GAAP financial measures to the most directly comparable GAAP financial measure cannot be provided without unreasonable efforts and is not provided herein because of the inherent difficulty in forecasting and quantifying certain amounts that are necessary for such reconciliations, the amounts of which could be material.

Conference Call and Webcast Information

Owlet will host a conference call and webcast today, August 11, 2026, at 4:30 p.m. ET to discuss these results and provide a business update.

Participants may access the call at 833-461-5787 (domestic) or 585-542-9983 (international) and reference Meeting ID 883284960. A simultaneous webcast may be accessed online at the Events section of Owlet's Investor Relations website at investors.owletcare.com . A replay will be available on the Investor Relations website shortly after the webcast concludes.

About Owlet, Inc.

Owlet, Inc. (NYSE: OWLT), a leading pediatric health platform, is the only company in the world to offer U.S. FDA-cleared and internationally medically-certified wearable pediatric monitors, delivering hospital-grade technology directly in the home. Our award-winning pediatric products and innovative software combine clinically tested monitoring systems, an integrated video platform, and a simple, easy-to-use app, providing parents with real-time health insights to stay informed on their child's well-being, support restful sleep, and provide peace of mind anywhere. Since 2012, more than 2.5 million parents have trusted Owlet to monitor their children's well-being and sleep. This adoption has fueled one of the largest collections of pediatric health and sleep data in the world, powering innovations that bridge the critical gap between hospital and home. Owlet is driving a new standard in pediatric wellness by pairing advanced medical technology with consumer-friendly design. Our mission is simple yet ambitious: to give every baby and every family the best possible start in life. Learn more at www.owletcare.com and follow us on LinkedIn and Instagram for company news and updates.

- 5 -

Owlet, Inc.

Condensed Consolidated Balance Sheets - Preliminary, Unaudited 1

(in millions)

Assets | June 30, 2026 | December 31, 2025
Current assets:
Cash and cash equivalents | 30.9 | 35.5
Restricted cash | 5.6 | 5.6
Accounts receivable, net | 33.1 | 22.9
Inventory | 15.7 | 15.3
Prepaid expenses and other current assets | 3.0 | 2.7
Total current assets | 88.3 | 81.9
Property and equipment, net | 0.8 | 0.3
Intangible assets, net | 2.0 | 1.4
Other assets | 2.4 | 2.0
Total assets | 93.6 | 85.6
Liabilities, Mezzanine Equity, and Stockholders' Equity
Current liabilities:
Accounts payable | 12.1 | 12.0
Accrued and other expenses | 21.8 | 19.4
Current portion of deferred revenue | 2.8 | 2.3
Line of credit | 17.1 | 6.9
Current portion of long-term and other debt | — | 3.6
Total current liabilities | 53.8 | 44.2
Long-term debt, net | — | 2.5
Common stock warrant liabilities | 0.8 | 3.3
Other long-term liabilities | 0.1 | 0.2
Total liabilities | 54.7 | 50.2
Total mezzanine equity | 15.7 | 16.4
Total stockholders' equity | 23.1 | 19.0
Total liabilities, mezzanine equity, and stockholders' equity | 93.6 | 85.6

1 Amounts may not sum due to rounding

- 6 -

Owlet, Inc.

Condensed Consolidated Statements of Cash Flows - Preliminary, Unaudited 1

(in millions)

Six Months Ended June 30,
2026 | 2025
Net cash used in operating activities | (5.1) | (8.3)
Net cash used in investing activities | (1.4) | (0.2)
Net cash provided by financing activities | 2.0 | 9.9
Net change in cash, cash equivalents, and restricted cash | (4.5) | 1.4

1 Amounts may not sum due to rounding

- 7 -

Owlet, Inc.

Condensed Consolidated Statements of Operations and Comprehensive Income (Loss) - Preliminary, Unaudited 1

(in millions, except share and per share amounts)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-09_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Owlet is a leading pediatric health platform and the only company globally to offer U.S. FDA-cleared and internationally medically-certified wearable pediatric monitors for home use. By delivering hospital-grade technology through a consumer-friendly interface, we bridge the critical gap between clinical care and the home.

Our mission is to empower parents with the right information at the right time, to give them more peace of mind and help them find more joy in the journey of parenting. Our digital parenting platform aims to give parents real-time data and insights to help parents feel calmer and more confident. We believe that every parent deserves peace of mind and the opportunity to feel their well-rested best. We also believe that every child deserves to live a long, happy, and healthy life, and we are working to develop products to help facilitate that belief.

Components of Operating Results

Revenues

We recognize revenue primarily from products and the associated mobile applications. Revenues are recognized when control of goods and services is transferred to customers in an amount that reflects the consideration expected to be received by us in exchange for those goods and services. Substantially all of our revenues were derived from product sales, with a growing minority portion of revenues being generated from subscriptions to our Owlet360 service.

Cost of Revenues

Cost of revenues consists of product costs, including contract manufacturing, shipping and handling, depreciation and amortization relating to tooling and manufacturing equipment and software, warranty replacement, fulfillment costs, warehousing, hosting and platform costs, and reserves for excess and obsolete inventory. Cost of revenues associated with Owlet360 mainly consist of app store distribution fees.

Operating Expenses

General and Administrative. General and administrative expenses consist primarily of salaries, benefits, stock-based compensation, and bonuses for finance and accounting, legal, human resources, operations, quality and administrative executives and employees; third-party legal, accounting, customer service, software, and other professional services; corporate travel and entertainment; depreciation and amortization of property and equipment, asset impairment charges, litigation settlement costs, insurance loss recovery, and facilities rent.

Sales and Marketing. Sales and marketing expenses consist primarily of salaries, commissions, benefits, stock-based compensation, and bonuses for sales and marketing employees and contractors; third-party marketing expenses such as social media and search engine marketing, retail marketing, email marketing, and print marketing.

Research and Development. Research and development expenses consist primarily of salaries, benefits, stock-based compensation, and bonuses for employees and contractors engaged in the design, development, maintenance, and testing of our products, platforms and services, including quality and clinical testing.

Other Income (Expense)

Interest Income (Expense), Net. Interest income (expense), net consists of interest incurred on our outstanding borrowings and amortization of debt financing costs. Interest income consists of interest earned on our money market funds and other cash and cash equivalents.

Common Stock Warrant Liability Adjustment. Mark to market adjustment to recognize the change in fair value of common stock warrant liabilities.

Other Income (Expense), Net. Other income (expense), net includes our net gain (loss) on foreign exchange transactions and transaction costs.

Income Tax Provision. Income tax provision consists primarily of U.S. federal and state income taxes related to the tax jurisdictions in which we conduct business.

Results of Operations

The following table sets forth our results of operations for the periods presented (dollars in thousands, except per share amounts):

Year Ended December 31,
2025 | 2024
Revenues | 105,708 | 78,056
Cost of revenues | 52,175 | 38,748
Gross profit | 53,533 | 39,308
Operating expenses:
General and administrative | 29,245 | 33,967
Sales and marketing | 18,473 | 15,760
Research and development | 14,076 | 9,801
Total operating expenses | 61,794 | 59,528
Operating loss | (8,261) | (20,220)
Other income (expense):
Interest expense, net | (3,418) | (1,630)
Common stock warrant liability adjustment | (26,571) | 9,293
Other income (expense), net | (1,400) | 75
Total other income (expense), net | (31,389) | 7,738
Loss before income tax provision | (39,650) | (12,482)
Income tax provision | (28) | (54)
Net loss and comprehensive loss | (39,678) | (12,536)
Accretion on convertible preferred stock | (3,392) | (4,926)
Accretion on redeemable common stock | (84) | (25)
Allocation of net loss attributable to redeemable common stockholders | 1,299 | 270
Net loss attributable to redeemable common stockholders | (1,215) | (245)
Net loss attributable to common stockholders | (41,855) | (17,217)
Net loss per share attributable to redeemable common stockholders
Basic and diluted | (2.16) | (1.42)
Weighted-average number of shares outstanding used to compute net loss per share attributable to redeemable common stockholders
Basic and diluted | 562,500 | 172,131
Net loss per share attributable to common stockholders
Basic and diluted | (2.31) | (1.57)
Weighted-average number of shares outstanding used to compute net loss per share attributable to common stockholders
Basic and diluted | 18,093,925 | 10,951,270

Revenues

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Revenues | 105,708 | 78,056 | 27,652 | 35.4 | %

The increase was primarily due to higher sales of Dream Sock and Dream Duo products, reflecting an increase in consumer demand as compared to the prior year. To a lesser extent, growth in revenue generated from subscriptions to our Owlet360 service, which launched in January 2025, also contributed to the increase.

Cost of Revenues and Gross Profit

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Cost of revenues | 52,175 | 38,748 | 13,427 | 34.7 | %
Gross margin | 50.6 | % | 50.4 | %

The increase in cost of revenues was primarily due to the increase in product sales. The increase in gross margin was primarily due to higher revenue, favorable product mix, improved fixed cost absorption, and lower direct product and fulfillment costs. To a lesser extent, the increase in gross margin was also attributed to the growth in revenue from subscriptions to our Owlet360 service. These contributions to gross margin expansion were partially offset by the impact of tariffs, which was more pronounced during the second half of 2025.

General and Administrative

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
General and administrative | 29,245 | 33,967 | (4,722) | (13.9 | %)

The decrease was driven primarily by the absence of significant litigation settlement costs and impairment charges recognized in 2024, which did not recur in the current period, and lower severance expenses. The decrease was partially offset by increases in headcount related expenses, including salaries, bonus, and benefits, as well as increased stock-based compensation, driven by a notable increase in our common stock price during 2025.

Sales and Marketing

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Sales and marketing | 18,473 | 15,760 | 2,713 | 17.2 | %

The increase was driven primarily by higher marketing expenses and increases in headcount related expenses, including salaries, commissions, bonus, and benefits.

Research and Development

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Research and development | 14,076 | 9,801 | 4,275 | 43.6 | %

The increase was driven primarily by increased investment in research and development, particularly with product development, quality, and clinical testing, and increases in headcount related expenses, including salaries, bonus, and benefits.

Other Income (Expense), Net

Year Ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Interest expense, net | (3,418) | (1,630) | (1,788) | 109.7 | %
Common stock warrant liability adjustment | (26,571) | 9,293 | (35,864) | (385.9 | %)
Other income (expense), net | (1,400) | 75 | (1,475) | (1966.7 | %)

The increase in interest expense was driven primarily by interest and amortization of debt financing costs related to our current term loan facility and asset-based revolving credit facility, which were entered into in September 2024, as well as the absence of a gain on interest for forgiveness of interest accrued related to an arrangement with a significant vendor that was fully settled in September 2024, partially offset by the absence of termination fees related to the SVB term loan that was terminated in September 2024.

Fluctuations in our common stock warrant liability adjustment resulted from an increase in our common stock price, and the related increase in the fair value of liability-classified common stock warrants. As described further in Note 9, most of these common stock warrants were exchanged for common shares in October 2025.

Changes in other income (expense) were driven primarily by transaction costs related to the Warrant Exchange as discussed in Note 9. Common Stock Issuance, Redeemable Common Stock, Common Stock Warrants, and Convertible Preferred Stock, within the Notes to Consolidated Financial Statements included elsewhere in this Report.

Non-GAAP Adjusted EBITDA

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-09_item1_business.md)

Item 1. Business

We are Owlet

Owlet is a leading pediatric health platform and the only company globally to offer U.S. FDA-cleared and internationally medically-certified wearable pediatric monitors for home use. By delivering hospital-grade technology through a consumer-friendly interface, we bridge the critical gap between clinical care and the home.

Our ecosystem—comprising clinically tested monitoring systems, an integrated video platform, and an intuitive mobile app—supports families from "night one" and throughout the most challenging parts of the parenting journey. Since 2012, more than 2.5 million parents have trusted Owlet to provide the real-time insights in support of their child's well-being and to promote restful sleep for the entire family.

Globally, over 140 million new lives are brought into the world every year. While welcoming a new child is a meaningful milestone for families, the first year of life is often marked by sleep disruption, health concerns, and increased stress for caregivers. In the United States alone, we estimate families lose an average of 44 nights of sleep in the first year, and young children account for millions of annual sick visits and emergency room consultations.

We believe these challenges underscore a dire need for a paradigm shift in pediatric wellness. Rather than relying solely on reactive care, Owlet enables a more proactive, data-informed approach to infant and early childhood health. We are moving beyond simple monitoring to provide a comprehensive window into a child's health, helping parents stay informed, get more rest, and find lasting peace of mind.

Our vision is to become the world's most trusted parenting platform, providing insights and care for every family. We are committed to:

• Guiding parents through the unknown: Delivering real-time, clinically grounded insights that help families navigate the earliest stages of parenting with confidence.

• Supporting health, safety and sleep: Prioritizing the core needs of the early years to improve well-being for both children and caregivers.

• Leading in pediatric data and insights: Leveraging one of the world's largest datasets of pediatric health and sleep information to drive continuous innovation, personalized experiences, and responsible integration with the broader healthcare ecosystem.

By pairing advanced medical technology with human-centric design and AI-powered intelligence, Owlet is building more than a monitoring solution. We are building a platform that advances health and wellness outcomes for families and fosters a trusted partnership with parents that begins on night one and continues well beyond.

Products and Services

Our integrated platform delivers a dual-value proposition: medical-grade monitoring for health and safety and data-driven insights for long-term family wellness.

Owlet provides medically certified, over-the-counter wearable monitors that bring hospital-grade technology into the home. Our wearable sensors provide a notification to the caregiver when a child's pulse rate and/or oxygen saturation values moves outside of preset ranges ("Health Notifications") and displays the child's live pulse rate and oxygen saturation values and trends ("Live Health Readings"). This combination creates a medical-grade safety net designed to provide parents with the security of knowing they will be alerted when their attention is required.

Beyond health monitoring, our software services transform physiological data into actionable guidance, helping parents get more sleep and provide more informed care. We leverage one of the world's largest pediatric datasets to provide parents with personalized data and insights. By analyzing sleep trends and health patterns, we empower caregivers to make informed decisions and shift from reactive monitoring to proactive wellness. These app-based services are designed to reduce uncertainty during the early months of the parenting journey. By providing a clear window into a child's well-being, our software services can help reduce parental anxiety and enable a more restful home environment. This emphasis on clarity and confidence helps families feel safe, well-rested, and supported in their daily routines.

Dream Sock: An award-winning wearable infant health monitor equipped with pulse oximetry technology that tracks vital signs, including pulse rate, oxygen level, activity, and sleep patterns. It delivers real-time notifications to caregivers when pulse rate and/or oxygen saturation values fall outside preset ranges and provides tailored sleep insights in the Owlet Dream App. Dream Sock with Live Health Readings and Health Notifications has received FDA marketing authorization in the United States, and has regulatory clearances in the European Union, United Kingdom, Australia, South Africa, India, and Israel. A version of Dream Sock without Live

Health Readings and Health Notifications is available in Canada and tracks Sleep Quality Indicators, including heart rate and 10-minute historic average oxygen levels. Dream Sock is the next-generation monitor that replaced our legacy Smart Sock product.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-09_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-09_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-09_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-11_2-02-results.md, 10-K_2026-03-09_item7_mdna.md, 10-K_2026-03-09_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
