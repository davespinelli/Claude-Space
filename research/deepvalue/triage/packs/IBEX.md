# Triage pack — IBEX · IBEX Ltd

_Generated 2026-09-04 13:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** IBEX · **Name:** IBEX Ltd
- **CIK:** 0001720420
- **SIC:** 7374 — Services-Computer Processing & Data Preparation
- **Fiscal year end (MM-DD):** 06-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/IBEX

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** IBEX Ltd
- **CIK:** 1,720,420 · **SIC:** 7374 (Services-Computer Processing & Data Preparation) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtAndCapitalLeaseObligations

**Valuation**

| metric | value |
|---|---|
| price | 39.41 |
| mktcap | $527.7M |
| ev | $512.8M |
| ev_ebit | 11.0x |
| fcf | $27.3M |
| fcf_yield | 5.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 25.2% |
| net_debt | -$14.8M |
| net_debt_ebit | -0.3x |
| cash | $15.4M |
| ltd | $572k |
| equity | $160.8M |
| ltd_tag | LongTermDebtAndCapitalLeaseObligations |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $558.3M |
| revenue_prior | $508.6M |
| rev_growth | 9.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $46.6M |
| net_income | $36.9M |
| cfo | $45.7M |
| capex | $18.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 13,389,116 |
| shares_py | 13,372,404 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 25.6% |
| r6m | 30.8% |
| off_52w_high | -6.2% |
| adv20 | $4.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.51 |
| r_ev_ebit | 0.72 |
| r_roic | 0.92 |
| r_rev_growth | 0.65 |
| r_buyback | 0.64 |
| score | 0.74 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q1I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 40 |

**Screen rationale:** high ROIC 25.2%; net cash; 12-1 momentum 25.6%


## 3. Share count trend

- Shares outstanding: **13,389,116** (CY2026Q1I) vs **13,372,404** prior year (CY2025Q1I)
- Change: **0.1%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 2 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 12 |
| F | 6 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-06_2-02-results.md)

_Extraction: started at the first release heading, 'Third Quarter Financial Performance'; skipped 1 cover-page block(s) and 9 forward-looking-statement block(s); 13 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ibex-20260506exx991.htm)

Third Quarter Financial Performance

Revenue

• Revenue of $164.4 million, an increase of 16.8% from $140.7 million in the prior year quarter, was driven by broad-based growth across four verticals: HealthTech (+53.7%), Technology (+42.6%), Travel, Transportation and Logistics (+15.1%), and Retail & E-commerce (+8.3%), along with continued growth in the digital acquisition business.

Net Income and Earnings Per Share

• Net income increased to $13.3 million compared to $10.5 million in the prior year quarter. Net income was favorably impacted by revenue growth in our higher margin offshore regions and lower selling, general, and administrative expenses as a percentage of revenue.

• Net income margin increased to 8.1% compared to 7.4% in the prior year quarter.

• Diluted earnings per share increased to $0.89 compared to $0.73 in the prior year quarter.

• Non-GAAP adjusted net income increased to $13.6 million compared to $11.8 million in the prior year quarter (see Exhibit 1 for reconciliation).

• Non-GAAP adjusted diluted earnings per share increased to $0.91 compared to $0.82 in the prior year quarter (see Exhibit 1 for reconciliation).

Non-GAAP Adjusted EBITDA

• Adjusted EBITDA increased to $22.0 million compared to $19.4 million in the prior year quarter (see Exhibit 2 for reconciliation).

• Adjusted EBITDA margin was 13.4% compared to 13.8% in the prior year quarter (see Exhibit 2 for reconciliation).

Cash Flow and Balance Sheet

• Capital expenditures were $5.3 million, consistent with the prior year quarter.

• Cash flow from operating activities was $11.9 million compared to $8.8 million in the prior year quarter.

• Free cash flow was $6.6 million compared to $3.6 million in the prior year quarter (see Exhibit 3 for reconciliation).

• During the quarter, we repurchased 140,300 shares for $4.5 million.

• Net cash was $14.0 million, compared to net cash of $13.7 million as of June 30, 2025 (see Exhibit 4 for reconciliation).

Third Quarter Review and Fiscal 2026 Business Outlook

"Our strong financial results in fiscal year 2026 are being driven by our differentiated strategy and sustainable growth trends with our clients, giving us confidence in continued outperformance heading into fiscal year 2027. Our third quarter revenue was again led by meaningful growth in our higher margin services and vertical markets, particularly our robust growth in HealthTech. This combination of drivers led to a record quarterly adjusted EBITDA of $22.0 million," said Taylor Greenwald, CFO of ibex.

"As we enter the fourth quarter, our healthy balance sheet and cash flows are enabling us to make thoughtful investments to support increased capacity for anticipated growth as well as to further extend our current AI leadership position. Reflective of our outstanding performance thus far and our forward momentum, we are raising our revenue and adjusted EBITDA guidance for the third time this year."

Fiscal Year 2026 Guidance

• Revenue is expected to be in the range of $638 to $642 million, up from $620 to $630 million.

• Adjusted EBITDA is expected to be in the range of $82 to $84 million, up from $80 to $82 million.

• Capital expenditures are now expected to be in the range of $25 to $30 million, up from our previous range of $20 to $25 million, as a result of ongoing investment to meet increased demand in higher margin regions.

Conference Call and Webcast Information

IBEX Limited will host a conference call and live webcast to discuss its third quarter of fiscal year 2026 financial results at 4:30 p.m. Eastern Time today, May 6, 2026. We will also post to this section of our website the earning slides, which will accompany our conference call and live webcast, and encourage you to review the information that we make available on our website.

Live and archived webcasts can be accessed at: https://investors.ibex.co/ .

Financial Information

This announcement does not contain sufficient information to constitute an interim financial report as defined in Financial Accounting Standards ASC 270, "Interim Reporting." The financial information in this press release has not been audited.

Non-GAAP Financial Measures

We present non-GAAP financial measures because we believe that they and other similar measures are widely used by certain investors, securities analysts and other interested parties as supplemental measures of performance and liquidity. We also use these measures internally to establish forecasts, budgets and operational goals to manage and monitor our business, as well as evaluate our underlying historical performance, as we believe that these non-GAAP financial measures provide a more helpful depiction of our performance of the business by encompassing only relevant and manageable events, enabling us to evaluate and plan more effectively for the future. The non-GAAP financial measures may not be comparable to other similarly titled measures of other companies, have limitations as analytical tools, and should not be considered in isolation or as a substitute for analysis of our operating results as reported in accordance with accounting principles generally accepted in the United States ("GAAP"). Non-GAAP financial measures and ratios are not measurements of our performance, financial condition or liquidity under GAAP and should not be considered as alternatives to operating profit or net income / (loss) or as alternatives to cash flow from operating, investing or financing activities for the period, or any other performance measures, derived in accordance with GAAP.

ibex is not providing a quantitative reconciliation of forward-looking non-GAAP adjusted EBITDA to the most directly comparable GAAP measure because it is unable to predict with reasonable certainty the ultimate outcome of certain significant items without unreasonable effort. These items include, but are not limited to, non-recurring expenses, foreign currency gains and losses, and stock-based compensation expense. These items are uncertain, depend on various factors, and could have a material impact on GAAP reported results for the guidance period.

About ibex

ibex is a global leader in outsourced business services and AI-powered customer experience solutions, enabling the world's best brands to deliver truly differentiated experiences for their customers. Leveraging a global team of more than 36,000 human CX experts – powered by the best AI technology, decades of CX innovation, and deep business insights – ibex engineers seamless, end-to-end customer journeys from AI agents to human agents at scale across retail, e-commerce, healthcare, fintech, utilities, technology, logistics, and more. Discover more at ibex.co and connect with us on LinkedIn.

IBEX LIMITED AND SUBSIDIARIES

Consolidated Statements of Comprehensive Income

(Unaudited)

(in thousands, except per share data)

Three Months Ended March 31, | Nine Months Ended March 31,
2026 | 2025 | 2026 | 2025
Revenue | 164,407 | 140,736 | 479,807 | 411,135
Cost of services (exclusive of depreciation and amortization presented separately below) | 115,614 | 96,017 | 338,820 | 284,820
Selling, general and administrative | 27,467 | 27,061 | 81,547 | 78,982
Depreciation and amortization | 5,170 | 4,329 | 14,298 | 12,984
Total operating expenses | 148,251 | 127,407 | 434,665 | 376,786
Income from operations | 16,156 | 13,329 | 45,142 | 34,349
Interest income | 62 | 32 | 151 | 926
Interest expense | (249) | (404) | (714) | (1,186)
Income before income taxes | 15,969 | 12,957 | 44,579 | 34,089
Provision for income tax expense | (2,644) | (2,488) | (6,995) | (6,821)
Net income | 13,325 | 10,469 | 37,584 | 27,268
Other comprehensive income
Foreign currency translation adjustments | (1,123) | 374 | (2,704) | 851
Unrealized (loss) / gain on cash flow hedging instruments, net of tax | (1,679) | 385 | (4,283) | 571
Total other comprehensive (loss) / income | (2,802) | 759 | (6,987) | 1,422
Total comprehensive income | 10,523 | 11,228 | 30,597 | 28,690
Net income per share
Basic | 0.99 | 0.79 | 2.80 | 1.80
Diluted | 0.89 | 0.73 | 2.54 | 1.70
Weighted average common shares outstanding
Basic | 13,454 | 13,264 | 13,427 | 15,109
Diluted | 14,994 | 14,404 | 14,780 | 16,135

IBEX LIMITED AND SUBSIDIARIES

Consolidated Statements of Cash Flows

(Unaudited)

(in thousands)

Three Months Ended March 31, | Nine Months Ended March 31,
2026 | 2025 | 2026 | 2025
CASH FLOWS FROM OPERATING ACTIVITIES
Net income | 13,325 | 10,469 | 37,584 | 27,268
Adjustments to reconcile net income to net cash provided by operating activities:
Depreciation and amortization | 5,170 | 4,329 | 14,298 | 12,984
Noncash lease expense | 3,394 | 3,611 | 10,319 | 10,020
Deferred income tax | 642 | (942) | (790) | (1,709)
Stock-based compensation expense | 788 | 1,601 | 4,452 | 3,506
Allowance for expected credit losses | 88 | 105 | 313 | 428
Change in assets and liabilities:
Decrease / (increase) in accounts receivable | 1,222 | 455 | (12,354) | (22,050)
Increase / (decrease) in prepaid expenses and other current assets | (8,167) | 1,405 | (10,373) | 392
Increase / (decrease) in accounts payable and accrued liabilities | 312 | (6,120) | (545) | (3,042)
Decrease / (increase) in deferred revenue | (1,331) | (1,262) | 2,034 | 1,203
Decrease in operating lease liabilities | (3,579) | (4,823) | (10,760) | (11,269)
Net cash inflow from operating activities | 11,864 | 8,828 | 34,178 | 17,731
CASH FLOWS FROM INVESTING ACTIVITIES
Purchase of property and equipment | (5,273) | (5,267) | (24,644) | (13,216)
Net cash outflow from investing activities | (5,273) | (5,267) | (24,644) | (13,216)
CASH FLOWS FROM FINANCING ACTIVITIES
Proceeds from line of credit | 24,600 | 60,150 | 35,600 | 69,310
Repayments of line of credit | (24,600) | (48,550) | (35,600) | (50,210)
Proceeds from the exercise of options | 466 | 2,809 | 3,814 | 3,534
Taxes paid related to net share settlement of equity awards | (2,261) | — | (2,302) | —
Principal payments on finance leases | (284) | (286) | (833) | (639)
Purchase of treasury shares | (4,580) | (25,052) | (10,133) | (76,421)
Net cash outflow from financing activities | (6,659) | (10,929) | (9,454) | (54,426)
Effects of exchange rate difference on cash and cash equivalents | 17 | 139 | (21) | 168
Net (decrease) / increase in cash and cash equivalents | (51) | (7,229) | 59 | (49,743)
Cash and cash equivalents, beginning | 15,460 | 20,206 | 15,350 | 62,720
Cash and cash equivalents, ending | 15,409 | 12,977 | 15,409 | 12,977

IBEX LIMITED AND SUBSIDIARIES

Reconciliation of GAAP Financial Measures to Non-GAAP Financial Measures

EXHIBIT 1: Adjusted net income, adjusted net income margin, and adjusted earnings per share

We define adjusted net income as net income before the effect of the following items: severance costs, foreign currency gains and losses , and stock-based compensation expense, net of the tax impact of such adjustments . We define adjusted net income margin as adjusted net income divided by revenue. We define adjusted earnings per share as adjusted net income divided by weighted average diluted shares outstanding.

The following table provides a reconciliation of net income to adjusted net income, net income margin to adjusted net income margin, and diluted earnings per share to adjusted earnings per share for the periods presented:

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-09-11_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

ibex delivers innovative business process outsourcing ("BPO"), smart digital marketing, online acquisition technology, and end-to-end customer engagement solutions to help companies acquire, engage, and retain valuable customers. Today, ibex operates a global customer experiences ("CX") delivery center model consisting of 30 delivery centers around the world, while deploying next-generation technology to drive superior customer experiences for many of the world's leading companies across various verticals, including Retail & E-commerce, HealthTech, FinTech, Utilities, and Travel, Transportation & Logistics. ibex leverages its diverse global team of approximately 33,000 employees together with industry-leading technology, including its Wave iX platform, to manage nearly 169 million customer interactions on behalf of our clients, driving a truly differentiated customer experience.

Business Highlights

During the fiscal year ended June 30, 2025, the Company delivered strong financial results, and experienced growth with leading clients in our Retail & E-commerce, HealthTech, Travel, Transportation & Logistics, and Other verticals, partially offset by decreases in our FinTech and Telecommunications verticals. We increased capacity in our offshore and nearshore regions and expanded into two new sites. The business performed well in several important areas during the current year, including total revenues and profitability. Our sales pipeline remained strong and we had sixteen new client wins during the fiscal year ended June 30, 2025, consistent with eighteen in the prior year.

Recent Financial Highlights

The Company delivered revenues of $558.3 million during the fiscal year ended June 30, 2025, a 9.8% increase compared to the prior year due to growth from existing and new clients launched throughout fiscal 2024 and fiscal 2025. Net income during the fiscal year ended June 30, 2025 was $36.9 million, a 9.5% increase from $33.7 million during the prior year. Fully diluted earnings per share for the fiscal year ended June 30, 2025 of $2.36, increased from $1.84 in the prior year. The increase in net income was driven by revenue growth in our higher margin offshore regions and improved gross margin performance. The increase in fully diluted earnings per share was driven by higher net income during the current year and fewer diluted shares outstanding compared to the prior year period.

Trends and Factors Affecting our Performance

There are a number of key trends and factors that have affected and may affect our results of operations.

Macroeconomic Trends

Macroeconomic factors, including but not limited to, increasing inflation and interest rates, global economic and geopolitical uncertainty, changes in foreign currency exchange rates, and the impact that these factors are having on our clients and their customers, have also impacted our financial results during fiscal year 2025. Some of our customers have increased their focus on cost reduction, resulting in decisions to shift work from onshore sites to offshore sites, which may impact our revenues and operations in the near term. However, we also believe that they present opportunities with both new and existing clients, as companies maintain a focus on cost reduction and look for new solutions and delivery options.

Artificial Intelligence ("AI")

With the increasing applicability of AI in enhancing business processes, the BPO industry is increasingly evaluating and starting to integrate AI into its range of solutions to improve the customer experience and efficiencies. We are moving aggressively to leverage generative AI in our business. Our Wave iX technology has a three-pronged AI strategy, which continues to keep ibex at the forefront of digital transformation. Our solutions are focused on increasing agent productivity, providing deeper customer insights to elevate the customer experience and putting AI in front of the customer journey with voice and chat bots. We believe we are well positioned to leverage our leadership position in adopting new technology in the CX sector and to create

significant value for our clients through the application of AI. We believe that our approach to bringing a combination of our AI-enabled solutions plus a robust set of third-party AI-enabled solutions to our clients positions us to not only be a fast-mover in the market, but also to capture an outsized share of AI-impacted future revenue, and to help minimize risk to our overall revenue and provide opportunities for future profitability enhancement. While the initial implementation of some AI-solutions may impact revenue directly derived from traditional agent-driven activities, it is our belief that by remaining on the forefront and bringing these solutions to our clients, we will be able to capture a greater share of AI-enabled revenue work and maintain and grow our overall business and results in the near- and long-term.

Client's Underlying Business Performance

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following summarizes the results of our operations for the fiscal years ended June 30, 2025 and 2024:

Year ended June 30,
($000s) | 2025 | 2024
Revenue | 558,273 | 508,569
Cost of services | 385,692 | 356,536
Selling, general and administrative | 108,738 | 93,143
Depreciation and amortization | 17,232 | 19,461
Income from operations | 46,611 | 39,429
Interest income | 955 | 2,071
Interest expense | (1,634) | (514)
Income before income taxes | 45,932 | 40,986
Provision for income tax expense | (9,068) | (7,331)
Net income | 36,864 | 33,655

Fiscal Years Ended June 30, 2025 and 2024

Revenue

Our revenue was $558.3 million for the fiscal year ended June 30, 2025, an increase of $49.7 million, or 9.8%, compared to the prior year. This increase was primarily driven by increases in our Retail & E-commerce vertical of $16.2 million, or 12.6%, HealthTech vertical of $15.5 million, or 23.2%, Travel, Transportation & Logistics vertical of $9.4 million, or 13.7%, and Other vertical of $20.3 million, or 37.6%, largely due to growth in our digital acquisition business, compared to the prior year. These increases were partially offset by decreases in the FinTech vertical of $8.7 million, or 12.2% and Telecommunications vertical of $3.5 million, or 4.6%, compared to the prior year.

As a percentage of total revenue, the revenue from our Retail & E-commerce vertical increased to 26.0% for the fiscal year ended June 30, 2025 compared to 25.4% in the prior year, the revenue from our HealthTech vertical increased to 14.7% compared to 13.1%, the revenue from our Travel, Transportation & Logistics vertical increased to 13.9% compared to 13.4%, and the revenue from our Other vertical increased to 13.3% compared to 10.6%. Conversely, the revenue from our FinTech vertical decreased to 11.2% for the fiscal year ended June 30, 2025 compared to 14.0% in the prior year, and the revenue from our Telecommunications vertical decreased to 13.1% compared to 15.0%.

Operating Expenses

Cost of services

Cost of services was $385.7 million during the fiscal year ended June 30, 2025, an increase of $29.2 million, or 8.2%, compared to the prior year. The increase in cost of services was primarily due to increases in payroll and related costs, reseller commissions and lead expenses, IT expenses, telecom, local transportation and other site related expenses, and stock-based compensation.

Payroll and related costs were $291.0 million during the fiscal year ended June 30, 2025, an increase of $16.6 million, or 6.0%, compared to the prior year, due to increased revenues during the current year. As a percent of revenue, payroll costs decreased to 52.1% during the fiscal year ended June 30, 2025 compared to 54.0% during the prior year, reflecting our continuing trend towards lower cost regions.

Reseller commissions and lead expenses were $20.7 million during the fiscal year ended June 30, 2025, an increase of $8.7 million, or 72.7%, compared to the prior year. These increases were primarily due to increases in the utilization of our third-party affiliates for inbound inquiries as well as search engine costs in connection with increased revenue in our higher margin digital sales and marketing efforts.

IT expenses were $6.8 million during the fiscal year ended June 30, 2025, an increase of $1.7 million or 32.8%, compared to the prior year, primarily due to additional software license fees.

Telecom, local transportation and other site related expenses were $15.3 million during the fiscal year ended June 30, 2025, an increase of $1.7 million, or 12.2%, compared to the prior year, driven primarily by increased activity corresponding to our increased revenues during the current year.

Stock-based compensation was $0.5 million during the fiscal year ended June 30, 2025, an increase of $0.4 million compared to the prior year, primarily due to a higher share price impacting liability-based grants.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-09-11_item1_business.md)

ITEM 1. BUSINESS

Company Overview

ibex delivers innovative business process outsourcing ("BPO"), smart digital marketing, online acquisition technology, and end-to-end customer engagement solutions to help companies acquire, engage, and retain valuable customers. We combine our strong heritage of delivering leading customer experience ("CX") operations, services and solutions that span omnichannel customer engagement and support, digital marketing and customer experience management to help our clients measure customer sentiment and deliver a superior CX to their end-customers.

Leveraging our proprietary technology platform, company culture and operational excellence, ibex helps more than 140 clients create innovative and differentiated customer experiences to help increase loyalty, enhance brand awareness and drive revenue in an era of rapid change and digital transformation.

Our Service Offerings

The Company is an end-to-end provider of technology-enabled customer lifecycle experience ("CLX") solutions. Through the Company's integrated CLX platform, a comprehensive portfolio of solutions is offered to help optimize customer acquisition, engagement, expansion and experience for clients. The Company leverages sophisticated technology and proprietary analytics, in combination with its global footprint and BPO expertise, to protect and enhance clients' brands.

Our Connect business lies at the core of our offerings and generates the majority of the Company's revenue. This business unit delivers differentiated customer service (assisting our clients' customers with information about our clients and their products or services), technical support (providing specialized teams to provide information, assistance and technical guidance to our clients' customers on a specific product or service), revenue generation (upselling and cross selling) and other value-added outsourced back office services (finance and accounting, marketing support, sales operations, and human resources administration) to our clients. We deploy these capabilities through a true omni-channel CX model, which integrates voice, email, chat, SMS, social media and other communication applications.

In addition, our ibex Digital suite of solutions works with consumer-facing businesses to help them build, grow and scale technology-driven customer acquisition solutions, while helping drive digital transformation. We offer digital marketing, e-commerce technology, and platform solutions for our clients, helping them build new customer acquisition channels, increase acquired customers, and often do both at a reduced cost. We also have a small suite of what we call CX services which measures, monitors and manages our clients' holistic customer experiences.

Our Culture

Ibex is built around an agent-first culture, developed and delivered through a combination of branded sites, technology-enabled recruiting and hiring, geographically and culturally specific benefits, and world-class employee engagement. Ibex offers a unique employee experience that includes a full range of activities and events for employees year-round, including annual employee VIP events, Customer Service Week and ongoing employee wellness programs. This culture resonates with our employees across the globe, where we score an Employee Net Promoter Score ("eNPS") of 77, and externally, where we have been recognized as:

• 2025 Forbes America's Best Large Employers

• 2025 Newsweek's America's Most Admired Workplaces

• 2025 North American Inspiring Workplaces – Inspiring Workplaces Group

• 2025 Globee Award for Technology in AI-Driven Customer Experience

• 2025 Leader in Frost & Sullivan Radar for Customer Experience Management in N. America and Latin America

• 2025 Gold Stevie Award for Achievement in Technology Innovation

• 2025 Product of the Year for Wave iX Translate and AI Virtual Agent – CUSTOMER Magazine

• 2025 Titan Award – Achievement in Technology Innovation

• 2025 Contact Center Partner of the Year – Philippine Airlines

• 2024 Best Place to Work in Nicaragua – Great Place to Work

• 2024 America's Best Employers for Tech Workers – Forbes

• 2024 Customer Experience Innovation Award – CUSTOMER Magazine

• 2024 Globee Award for Customer Excellence

• 2024 Contact Center Technology Award – CUSTOMER Magazine

• 2024 Stevie Award for Technology Excellence

• 2024 Gold Globee Winner at the Golden Bridge Awards

• 2024 Netty Award for Tech – Best CX Innovation

• 2024 Generative AI Product of the Year Award – TMC and Generative AI Expo

Our Technology

The foundation for ibex service offerings is our Wave iX technology platform, the current evolution of our prior WaveX technology platform. Wave iX is a differentiated suite of digital and technology solutions designed to power enhanced agent interactions, exceptional client CX, and overall better performance. We have created a three-pronged AI strategy, which continues to keep ibex at the forefront of digital transformation.

Our solutions are focused on increasing agent productivity, providing deeper customer insights to elevate the customer experience and putting AI in front of the customer journey with voice and chat bots. Our technology helps clients drive insights and manage interactions across their entire customer journey. We believe this capability allows us to provide innovative, automated and customizable solutions to our clients more efficiently versus a pure labor arbitrage-based delivery model.

Our Business Insights

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-09-11_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-09-11_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-09-11_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-06_2-02-results.md, 10-K_2025-09-11_item7_mdna.md, 10-K_2025-09-11_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
