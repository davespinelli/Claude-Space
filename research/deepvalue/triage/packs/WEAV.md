# Triage pack — WEAV · Weave Communications, Inc.

_Generated 2026-09-05 01:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** WEAV · **Name:** Weave Communications, Inc.
- **CIK:** 0001609151
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/WEAV

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Weave Communications, Inc.
- **CIK:** 1,609,151 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 7.33 |
| mktcap | $586.4M |
| ev | $538.8M |
| ev_ebit | n/a |
| fcf | $15.2M |
| fcf_yield | 2.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -64.8% |
| net_debt | -$47.6M |
| net_debt_ebit | n/a |
| cash | $47.6M |
| ltd | $0.00 |
| equity | $85.0M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $239.0M |
| revenue_prior | $204.3M |
| rev_growth | 17.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$30.6M |
| net_income | -$28.1M |
| cfo | $17.5M |
| capex | $2.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 3.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 79,999,119 |
| shares_py | 77,036,187 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -10.6% |
| r6m | 32.3% |
| off_52w_high | -8.3% |
| adv20 | $42.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.35 |
| r_ev_ebit | 0.00 |
| r_roic | 0.01 |
| r_rev_growth | 0.79 |
| r_buyback | 0.23 |
| score | 0.28 |

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
| rank | 427 |

**Screen rationale:** revenue +17.0%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **79,999,119** (CY2026Q2I) vs **77,036,187** prior year (CY2025Q2I)
- Change: **3.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-19** — Item 1.01 (Entry into a Material Definitive Agreement): On August 18, 2026, Weave Communications, Inc., a Delaware corporation (the "Company"), entered into an Agreement and Plan of Merger (the "Merger Agreement") with Willow Parent, LLC, a Delaware limited liability company ("Parent"), and Willow Merger Sub...
- **2026-03-30** — Item 1.01 (Entry into a Material Definitive Agreement): On M arch 28, 2026, Weave Communications, Inc. (the "Company") entered into a Cooperation Agreement (the "Cooperation Agreement") with Engine Capital L.P. and certain of its affiliates (collectively, "Engine Capital"), and 2717 Partners LP and certain of its...
- **2026-03-30** — Item 5.02 (officer / director change or comp arrangement): Pursuant to the Cooperation Agreement, in connection with Mr. Robson's appointment to the Board, he was appointed to serve on the Board's Nominating and Governance Committee, and the newly formed Finance Committee.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 7 |
| F | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Second quarter total revenue of $67.5 million, up 15.5% year over year'; skipped 16 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (a991-weaveearningsreleasex.htm)

Weave Announces Second Quarter 2026 Financial Results

• Second quarter total revenue of $67.5 million, up 15.5% year over year

• Second quarter GAAP gross margin of 72.0%, up 30 basis points year over year

• Second quarter Non-GAAP gross margin of 72.6%, up 30 basis points year over year

• Second quarter GAAP loss from operations of $4.4 million, down $5.8 million year over year

• Second quarter Non-GAAP income from operations of $3.2 million, up $3.1 million year over year

• Second quarter cash flow from operating activities of $10.2 million, up $4.8 million year over year

• Second quarter free cash flow of $8.7 million, up $4.2 million year over year

LEHI, Utah—August 6, 2026 – Weave Communications, Inc. ("Weave") (NYSE: WEAV), a leading vertical SaaS platform that delivers AI-powered patient engagement and payment solutions for healthcare practices, today announced its financial results for the second quarter ended June 30, 2026.

"Weave produced strong results for the second quarter, characterized by consistent growth and improvement in our operating leverage. Total revenue rose 15.5% year-over-year, our payments business accelerated at twice that pace, and we added the most new locations ever in a quarter, while also expanding our operating margin to 4.7%," said Brett White, CEO of Weave. "These results are a direct outcome of our unwavering focus on helping healthcare practices grow and teams thrive. We continue to define the intelligent front office in healthcare, building a durable, scalable business that delivers lasting value for all stakeholders."

Second Quarter 2026 Financial Highlights

• Total revenue was $67.5 million, representing a 15.5% year-over-year increase compared to $58.5 million in the second quarter of 2025.

• GAAP gross margin was 72.0%, compared to 71.7% in 2025.

• Non-GAAP gross margin was 72.6%, compared to 72.3% in 2025.

• GAAP loss from operations was $4.4 million, compared to $10.2 million in the second quarter of 2025.

• Non-GAAP income from operations was $3.2 million, compared to $0.1 million in the second quarter of 2025.

• GAAP net loss was $4.3 million, or $0.05 per share, compared to $8.7 million, or $0.11 per share, in the second quarter of 2025.

• Non-GAAP net income was $3.3 million, or $0.04 per share, compared to $1.5 million non-GAAP net loss, or $0.02 per share, in the second quarter of 2025.

• Cash flow from operating activities was $10.2 million, compared to $5.4 million in the second quarter of 2025.

• Free cash flow was $8.7 million, compared to $4.5 million in the second quarter of 2025.

Recent Business Highlights

• Launched an omnichannel AI Receptionist built on Google Cloud's Gemini Enterprise Agent Platform, enabling practices to execute front office workflows like appointment scheduling, preserve conversation context across voice and text, configure intelligent call routing, answer frequently asked questions, 24x7.

• Deepened the integration between Weave and athenaOne and joined athenahealth's Marketplace program, to help the network's 160,000+ providers maximize revenue capture, streamline administrative tasks and optimize payment collection.

• Announced an authorized integration with Elation Health, connecting patient communications directly to primary care practices' EHR systems and reducing time-consuming manual data entry.

• Expanded the company's enterprise platform capabilities with single sign-on desktop authentication, enhanced AI Receptionist controls, and automated digital insurance eligibility and collection.

• Ranked #1 in G2's Summer 2026 Grid Report for Patient Relationship Management, earning the highest satisfaction score and largest market presence in the category, alongside Leader status across seven adjacent G2 categories.

Financial Third Quarter and Full Year 2026 Outlook

The company expects to achieve the following financial results for the three months ending September 30, 2026, and the full year ending December 31, 2026:

Third Quarter | Full Year
(in millions)
Total revenue | $68.6 - $69.6 | $273.0 - $275.0
Non-GAAP income from operations | $3.0 - $4.0 | $12.0 - $14.0
Weighted average share count | 80.2 | 79.8

Non-GAAP Financial Measures

In this press release, Weave has provided financial information that has not been prepared in accordance with generally accepted accounting principles in the United States ("GAAP"). We disclose the following historical non-GAAP financial measures in this press release: non-GAAP net income, non-GAAP net income margin, non-GAAP net income per share, non-GAAP gross profit, non-GAAP gross margin, non-GAAP operating expenses, non-GAAP income from operations, non-GAAP income from operations margin, Adjusted EBITDA and free cash flow. We use these non-GAAP financial measures internally to analyze our financial results and evaluate our ongoing operational performance. We believe that these non-GAAP financial measures provide an additional tool for investors to use in understanding and evaluating ongoing operating results and trends in the same manner as our management and board of directors. Our use of these non-GAAP financial measures has limitations as an analytical tool, and you should not consider them in isolation or as a substitute for analysis of our financial results as reported under GAAP. Because of these and other limitations, you should consider these non-GAAP financial measures along with other GAAP-based financial performance measures, including various cash flow metrics, operating loss, net loss, and our GAAP financial results. We have provided a reconciliation of these non-GAAP financial measures to their most directly comparable GAAP measures in the tables included in this press release, and investors are encouraged to review the reconciliation.

Non-GAAP net income, non-GAAP net income margin and non-GAAP net income per share

We define non-GAAP net income as GAAP net loss adjusted to exclude stock-based compensation expense, acquisition transaction costs, amortization of acquisition-related intangible assets and costs related to shareholder matters, and non-GAAP net income margin as non-GAAP net income as a percentage of revenue. Acquisition transaction costs include legal and any accounting professional services costs incurred as a result of our acquisition during the applicable period. Although we exclude the amortization of acquisition-related intangible assets from the non-GAAP measure, management believes it is important for investors to understand that such intangible assets were recorded as part of purchase accounting and contribute to revenue generation. Non-GAAP net income per share is calculated as non-GAAP net income divided by the diluted weighted average shares outstanding.

Non-GAAP gross profit and non-GAAP gross margin

We define non-GAAP gross profit as GAAP gross profit adjusted to exclude stock-based compensation expense and amortization of acquisition-related intangible assets. Although we exclude the amortization of acquisition-related intangible assets from the non-GAAP measure, management believes it is important for investors to understand that such intangible assets were recorded as part of purchase accounting and contribute to revenue generation. Non-GAAP gross margin is defined as non-GAAP gross profit as a percentage of revenue.

Non-GAAP operating expenses

We define non-GAAP operating expenses, in the aggregate or its individual components (i.e., sales and marketing, research and development or general and administrative), as the applicable GAAP operating expenses adjusted to exclude the applicable stock-based compensation expense, acquisition transaction costs, amortization of acquisition-related intangible assets and costs related to shareholder matters. Although we exclude the amortization of acquisition-related intangible assets from the non-GAAP measure, management believes it is important for investors to understand that such intangible assets were recorded as part of purchase accounting and contribute to revenue generation.

Non-GAAP income from operations and non-GAAP income from operations margin

We define non-GAAP income from operations as GAAP loss from operations less stock-based compensation expense, acquisition transaction costs, amortization of acquisition-related intangible assets and costs related to shareholder matters. Although we exclude the amortization of acquisition-related intangible assets from the non-GAAP measure, management believes it is important for investors to understand that such intangible assets were recorded as part of purchase accounting and contribute to revenue generation. Non-GAAP income from operations margin is defined as non-GAAP income from operations as a percentage of revenue.

Adjusted EBITDA

We define EBITDA as earnings before interest expense, interest income, other income/expense, income tax expense, depreciation, and amortization. Our depreciation adjustment includes depreciation on operating fixed assets and we do not adjust for amortization of finance lease right-of-use assets on phone hardware provided to our customers. Our amortization adjustment includes the amortization of capitalized costs from both internal-use software development and cloud computing arrangements. We further adjust EBITDA to exclude stock-based compensation expense, a non-cash item, acquisition transaction costs, which we believe are not reflective of ongoing results of operations in the period incurred and not directly related to the operation of our business, amortization of acquisition-related intangible assets, and costs related to shareholder matters, including third-party legal, consulting, and advisory fees related to a cooperation agreement, which we believe are outside of the ordinary course of business and not reflective of operational performance. Although we exclude the amortization of acquisition-related intangible assets from the non-GAAP measure, management believes it is important for investors to understand that such intangible assets were recorded as part of purchase accounting and contribute to revenue generation. We believe that Adjusted EBITDA provides management and investors consistency and comparability with our past financial performance and facilitates period-to-period comparisons of operations. Additionally, management uses Adjusted EBITDA to measure our financial and operational performance and prepare our budgets.

Free cash flow

We define free cash flow as net cash provided by operating activities, less purchases of property and equipment and capitalized internal-use software costs. We believe that free cash flow is a useful indicator of liquidity that provides useful information to management and investors, even if negative, as it provides information about the amount of cash consumed by our combined operating and investing activities. For example, as free cash flow has in the past been negative, we have needed to access cash reserves or other sources of capital for these investments.

Limitations and Reconciliation of Non-GAAP Financial Measures

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-05_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Weave is a leading AI-powered patient communications, engagement, and payments platform purpose-built for small and medium-sized ("SMB") healthcare practices. We strive to elevate patient experiences through a unified platform that improves business operations, allowing healthcare professionals to focus on what matters most: patient care.

Weave serves as the orchestration layer for modern healthcare practices, bringing together voice, text, and AI-powered workflows into a single system of work. Our platform is built on nearly two decades of domain expertise and billions of patient interactions, allowing us to leverage our vertically specialized data to deliver high-accuracy automation within strict privacy and regulatory frameworks.

We deliver powerful communication and engagement capabilities previously only available to enterprises, made them intuitive and easy to use and put them in one solution. Our verticalized software platform helps streamline the day-to-day operations of running an SMB healthcare practice.

Supplemental Financial Information — Disaggregated Revenue and Cost of Revenue

To supplement our discussion of our consolidated results of operations, we have separated our revenue and cost of revenue into recurring and onboarding categories to disaggregate revenue and costs of revenue that are one-time in nature from those that are term-based and renewable.

We generate revenue primarily from recurring subscription fees charged to access our platform, which also includes embedded lease revenue on phone hardware. These recurring revenues accounted for 91% and 92% of our revenue for each of the years ended December 31, 2025 and 2024, respectively. In addition, we provide recurring payment processing services through Weave Payments and derive revenue from transactions between our customers that utilize Weave Payments and their end consumers.

We also derive revenue associated with installation fees for onboarding customers. We utilize our onboarding services and phone hardware as customer acquisition tools and price them competitively to lower the barriers to entry for new customers adopting our platform. As a result, the variable cost associated with providing phone hardware and onboarding assistance has historically exceeded the related revenue, resulting in negative gross profit for each. The revenue and related costs associated with onboarding new customers are primarily associated with the initial setup of a customer's software and phone system. Revenue on phone hardware provided to our customers, deemed embedded lease revenue, is recognized over the related subscription period. The associated costs, which primarily represent depreciation expense on phone hardware financed under finance lease arrangements, are incurred over the useful lives of the phone hardware, which is 36 months. We consider the net costs of onboarding and phone hardware, in addition to our sales and marketing activities, to be core elements of our customer acquisition approach.

The table below sets forth the revenue and associated cost of revenue for our recurring subscription and payment processing services, as well as for our onboarding services and phone hardware:

Year Ended December 31,
2025 | 2024
(dollars in thousands)
Subscription and payment processing:
Revenue | 228,769 | 196,106
Cost of revenue | (50,583) | (43,567)
Gross profit | 178,186 | 152,539
Gross margin | 78 | % | 78 | %
Onboarding:
Revenue | 3,463 | 3,547
Cost of revenue | (8,757) | (7,793)
Gross profit | (5,294) | (4,246)
Gross margin | (153) | % | (120) | %
Phone Hardware:
Revenue | 6,792 | 4,661
Cost of revenue (1) | (7,376) | (7,072)
Gross profit | (584) | (2,411)
Gross margin | (9) | % | (52) | %

(1) Cost of revenue related to hardware represents depreciation of phone hardware over a 3-year useful life.

Factors Affecting Our Performance

Our historical financial performance has been, and we expect our financial performance in the future to be, driven by our ability to attract new customers, retain and expand within our customer base, add new products, and expand into new industry verticals.

Attract New Customers

Our ability to attract new customers is dependent upon a number of factors, including the effectiveness of our pricing and products, the sum total of the features and pricing of the alternative point solution patchwork, the effectiveness of our marketing efforts, the effectiveness of our channel partners in selling and marketing our platform, our ability to integrate our platform with PMS and EHR software, which strengthens our product market fit and increases the value our platform provides to customers, and the growth of the market for a customer experience and payments software platform. Sustaining our growth requires continued adoption of our platform by new customers. We aim to add new customers through a combination of unpaid channels, such as recommendations and word of mouth, and paid channels, such as digital marketing, direct mail, trade shows and industry events, brand marketing and our teams of sales representatives. Historically, our go-to-market strategy focused on increasing the number of locations with most of our customers having a single location.

In addition to pursuing continued customer growth among small businesses, we intend to pursue opportunities to expand our customer base among medium-sized businesses through sales of Weave Enterprise, which is designed for multi-location businesses, with a particular focus on our core specialty healthcare verticals. Our ability to expand among medium-sized businesses will depend upon our ability to successfully sell our enhanced Weave platform to multi-location organizations, and effectively retain them.

Retain and Expand Within Our Customer Base

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth our consolidated statements of operations data for the periods indicated:

Year Ended December 31,
2025 | 2024
(in thousands)
Revenue | 239,024 | 204,314
Cost of revenue (1)(3) | 66,716 | 58,432
Gross profit | 172,308 | 145,882
Operating expenses:
Sales and marketing (1)(2)(3) | 102,703 | 84,612
Research and development (1)(2) | 44,462 | 40,231
General and administrative (1)(2) | 55,753 | 52,452
Total operating expenses | 202,918 | 177,295
Loss from operations | (30,610) | (31,413)
Other income (expense):
Interest income | 1,811 | 1,851
Interest expense | (1,700) | (1,523)
Other income (expense), net | 1,523 | 2,928
Loss before income taxes | (28,976) | (28,157)
Income tax benefit (provision) | 924 | (189)
Net loss | (28,052) | (28,346)

(1) Includes stock-based compensation expense as shown below

(2) Includes acquisition transaction costs as shown below

(3) Includes amortization of acquisition-related intangibles as shown below

Year Ended December 31,
2025 | 2024
(in thousands)
Cost of revenue | 894 | 1,014
Sales and marketing | 7,510 | 6,582
Research and development | 8,806 | 8,374
General and administrative | 14,921 | 16,250
Total stock-based compensation | 32,131 | 32,220

See Note 14 to our consolidated financial statements included elsewhere in this Annual Report on Form 10-K for further details on stock-based compensation expense.
Year Ended December 31,
2025 | 2024
(in thousands)
Sales and marketing | 16 | —
Research and development | 116 | —
General and administrative | 1,564 | —
Total acquisition transaction costs | 1,696 | —

Year Ended December 31,
2025 | 2024
(in thousands)
Cost of revenue | 535 | —
Sales and marketing | 331 | —
Total amortization of acquisition-related intangibles | 866 | —

See Note 4 to our consolidated financial statements included elsewhere in this Annual Report on Form 10-K for further details on amortization of acquisition related intangibles.

The following table sets forth our consolidated statements of operations data expressed as a percentage of revenue for the periods indicated:

Year Ended December 31,
2025 | 2024
(percentage of total revenue)
Revenue | 100 | % | 100 | %
Cost of revenue | 28 | 29
Gross margin | 72 | 71
Operating expenses:
Sales and marketing | 43 | 41
Research and development | 19 | 20
General and administrative | 23 | 26
Total operating expenses | 85 | 87
Loss from operations | (13) | (16)
Other income (expense):
Interest income | 1 | 1
Interest expense | (1) | (1)
Other income (expense), net | 1 | 1
Loss before income taxes | (12) | (15)
Income tax benefit (provision) | — | —
Net loss | (12) | % | (15) | %

Comparison of the Years Ended December 31, 2025 and December 31, 2024

Revenue

Year Ended December 31, | Change
2025 | 2024 | Amount | Percentage
(dollars in thousands)
Revenue | 239,024 | 204,314 | 34,710 | 17 | %

Revenue increased by $34.7 million, or 17%, for the year ended December 31, 2025 compared to the year ended December 31, 2024. Approximately $23.9 million, or 69% of our revenue growth was attributable to revenue generated from new customer locations acquired during the year ended December 31, 2025, and $10.8 million, or 31% of the increase was attributable to revenue generated from existing customer locations under subscription as of December 31, 2024. Customer locations totaled 39,625 and 34,997 as of December 31, 2025 and 2024, respectively.

Cost of Revenue and Gross Margin

Year Ended December 31, | Change
2025 | 2024 | Amount | Percentage
(dollars in thousands)
Cost of revenue | 66,716 | 58,432 | 8,284 | 14 | %
Gross margin | 72 | % | 71 | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-05_item1_business.md)

Item 1. Business

Our Mission

Our mission is to elevate the patient experience through a unified platform that improves business operations so healthcare professionals can focus on patient care and realize their dreams.

Overview

Weave is a leading AI-powered patient communications, engagement, and payments platform purpose-built for small and medium-sized ("SMB") healthcare practices. We strive to elevate patient experiences through a unified platform that improves business operations, allowing healthcare professionals to focus on what matters most: patient care.

Weave serves as the orchestration layer for modern healthcare practices, bringing together voice, text, and AI-powered workflows into a single system of work. Our platform is built on nearly two decades of domain expertise and billions of patient interactions, allowing us to leverage a vertically specialized data that allows us to deliver high-accuracy automation within strict privacy and regulatory frameworks.

Our platform integrates with more than 90 practice management systems ("PMS") to provide more personalized interactions between practices and patients. We have democratized powerful communication and engagement capabilities previously only available to enterprises, made them intuitive and easy to use, and put them in one solution. Key current capabilities include:

• Communications: our proprietary telephony platform unifies voice and text interactions and manages the practice's trusted phone number.

• AI-powered Workflows: we provide agentic AI functionality that handles scheduling automation, responds to frequently asked questions, and follows up on marketing leads.

• AI-powered Insights: our analytic tools transcribe phone calls, assesses call sentiment, creates follow-up tasks, and surfaces opportunities for additional revenue in the practice.

• Weave Payments: we provide payment processing, with point-of-sale and digital payment solutions that allow patients to make payments from anywhere, and patient financing solutions.

• Practice Growth Tools: we offer a suite of solutions that help practices strengthen their brand reputation, attract new patients, and improve patient outreach.

• Productivity Tools: we offer a suite of solutions that help practices improve in-office operations, communicate effectively with other staff and with patients, and improve the patient's experience.

The market for healthcare practice software is highly fragmented. We compete primarily against a "patchwork" of point solutions. We support the following verticals: Dental, Optometry, Veterinary, and Specialty Medical. Specialty Medical comprises 29 specialties and is now our second-largest and fastest-growing vertical by location count. We are currently focused on four specialties within Specialty Medical: primary care, physical and occupational therapy, aesthetics, and med spa.

Looking ahead, we intend to further establish Weave as an "always-on teammate" for our customers to further help practices attract, communicate with, and engage patients and clients to grow their business around the clock using AI.

Our Customers

As of December 31, 2025, we had nearly 40,000 locations under subscription and more than 30,000 customers in the U.S. and Canada. These customers represent many healthcare industries with the majority being in dental, optometry, veterinary, and other medical specialty services. No one single customer represents more than 5% of our revenue.

Our Platform

Weave's vertical software platform helps SMB healthcare practices manage essential patient interactions. We consolidate technologies that our customers need to grow their practices, effectively engage with patients, and streamline practice operations into one simple, easy and elegant solution. We allow practitioners and their staff to facilitate and manage patient interactions in a unified, modernized and personalized manner that best fits their patients' needs and preferences. We enable practitioners and their staff to do what they do best: care for their patients.

The key benefits of our platform include:

• Easy to Use and Intuitive . SMB healthcare practices typically do not have dedicated technology staff, so they need solutions that are easy to implement and manage. Our platform is designed to be simple and intuitive. We deliver enterprise-grade customer communications and engagement capabilities, saving our customers time and allowing them to effectively and efficiently communicate with their patients.

• Unified Communications and Engagement . We unify phones, text messaging, appointment scheduling, staff collaboration, email marketing, reviews, payments, and digital forms products in one platform.

• High ROI . Our platform helps our customers attract new patients, reduce appointment cancellations, keep schedules full, increase treatment acceptance rates, reduce outstanding accounts receivable, and improve staff efficiency and effectiveness. Weave provides more functionality at a significantly lower cost than the combined cost of point solutions

• Reduced Churn for Our Customers . Our platform enables our customers to increase patient loyalty and retention by helping them keep their patients engaged through multi-channel communications—phone, text messaging, or email, and reducing friction with online appointments, digital forms, and convenient and flexible payment options, including text to pay, online bill pay, and payment plans.

• Improved Ability to Attract New Patients . Our platform helps practices attract new patients by collecting and managing online reviews, ensuring practices do not miss a call or text, and eliminating the friction typically associated with scheduling appointments and completing forms.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-05_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-05_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-05_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-05_item7_mdna.md, 10-K_2026-03-05_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
