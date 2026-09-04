# Triage pack — BL · BLACKLINE, INC.

_Generated 2026-09-04 15:08 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** BL · **Name:** BLACKLINE, INC.
- **CIK:** 0001666134
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/BL

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** BLACKLINE, INC.
- **CIK:** 1,666,134 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 33.23 |
| mktcap | $1.9B |
| ev | $1.7B |
| ev_ebit | 66.1x |
| fcf | $161.5M |
| fcf_yield | 8.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 27.5% |
| net_debt | -$242.9M |
| net_debt_ebit | -9.5x |
| cash | $242.9M |
| ltd | $0.00 |
| equity | $316.2M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $700.4M |
| revenue_prior | $653.3M |
| rev_growth | 7.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $25.6M |
| net_income | $24.5M |
| cfo | $169.6M |
| capex | $8.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -6.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 58,125,270 |
| shares_py | 61,887,825 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -42.1% |
| r6m | -11.6% |
| off_52w_high | -43.5% |
| adv20 | $33.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.67 |
| r_ev_ebit | 0.10 |
| r_roic | 0.93 |
| r_rev_growth | 0.58 |
| r_buyback | 0.90 |
| score | 0.64 |

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
| rank | 109 |

**Screen rationale:** high ROIC 27.5%; buying back stock -6.1%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **58,125,270** (CY2026Q2I) vs **61,887,825** prior year (CY2025Q2I)
- Change: **-6.1%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-03** — Item 5.02 (officer / director change or comp arrangement): On July 31, 2026 (the "Effective Date"), the BlackLine, Inc. (the "Company") entered into an executive consulting agreement (the "Consulting Agreement") with Therese Tucker, Founder and a member of the Company's Board of Directors, pursuant to which she will...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 76,197 sh / $2,422,307 -> net $-2,422,307 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 27 (open-market buys 0, sales 5).

| code | rows |
|---|---|
| F | 18 |
| M | 4 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Financial Highlights'; skipped 9 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - PRESS RELEASE (exh_991.htm)

Second Quarter 2026 Financial Highlights

Total GAAP revenues of $187.8 million, an increase of 9.2% compared to the second quarter of 2025.

GAAP operating margin of 5.9%, compared to 4.4% in the second quarter of 2025.

Non-GAAP operating margin of 23.3%, compared to 22.1% in the second quarter of 2025.

GAAP net income attributable to BlackLine of $16.5 million, or $0.27 per diluted share compared to GAAP net income attributable to BlackLine of $8.3 million, or $0.13 per diluted share in the second quarter of 2025.

Non-GAAP net income attributable to BlackLine of $42.9 million, or $0.61 per diluted share compared to non-GAAP net income attributable to BlackLine of $37.9 million, or $0.51 per diluted share in the second quarter of 2025.

Billings of $193.0 million, an increase of 5.9% compared to the second quarter of 2025.

Remaining performance obligation of $1.1 billion, an increase of 16.8% compared to the second quarter of 2025.

Operating cash flow of $45.0 million, compared to $32.3 million in the second quarter of 2025.

Free cash flow of $36.5 million, compared to $25.4 million in the second quarter of 2025.

Repurchased approximately 1.2 million shares of common stock for $37.7 million as part of our share repurchase program under which approximately $179.7 million of buyback capacity remained at June 30, 2026.

Second Quarter Key Metrics and Recent Business Highlights

BlackLine had a total of 4,260 customers at June 30, 2026.

Platform pricing Annual Recurring Revenue (ARR) as a percentage of eligible ARR, which excludes SolEx and public sector ARR, was 17% at June 30, 2026.

Achieved a dollar-based net revenue retention rate of 102% at June 30, 2026.

Announced a $100 million increase to the Company's stock buyback program.

Verity Prepare, BlackLine's agentic reconciliations agent, achieved general availability in July.

Announced the expansion of BlackLine's Agentic Financial Operations Platform via the Finance Control Console.

Earned industry recognition for AI innovation and customer trust from Tech Ascension Awards and TrustRadius.

Hosted BeyondTheBlack Paris, BlackLine's France and EMEA region customer conference.

The financial results included in this press release are preliminary and subject to final review. Financial results will not be final until BlackLine files its Quarterly Report on Form 10-Q for the period. Information about BlackLine's use of non-GAAP financial measures is provided below under "Use of Non-GAAP Financial Measures."

Financial Outlook

Third Quarter 2026

Total GAAP revenue is expected to be in the range of $193 million to $195 million.

Non-GAAP operating margin is expected to be in the range of 24.5% to 25.5%.

Non-GAAP net income attributable to BlackLine is expected to be in the range of $45 million to $47 million, or $0.62 to $0.65 per share on 74.5 million diluted weighted average shares outstanding.

Full Year 2026

Total GAAP revenue is expected to be in the range of $765 million to $769 million.

Non-GAAP operating margin is expected to be in the range of 24.1% to 24.6%.

Non-GAAP net income attributable to BlackLine is expected to be in the range of $177 million to $182 million, or $2.47 to $2.54 per share on 74.0 million diluted weighted average shares outstanding.

Guidance for non-GAAP operating margin, non-GAAP net income attributable to BlackLine, and non-GAAP net income per share attributable to BlackLine excludes specified items from the corresponding GAAP financial measures as outlined below under "Use of Non-GAAP Financial Measures" and as detailed in the reconciliations of non-GAAP measures for historical periods. Reconciliations of non-GAAP operating margin, non-GAAP net income attributable to BlackLine, and non-GAAP net income per share attributable to BlackLine guidance to the most directly comparable U.S. GAAP measures are not available on a forward-looking basis without unreasonable efforts due to the unpredictability and complexity of the charges excluded from these non-GAAP financial measures. The Company expects the variability of the above items could have a significant, and potentially unpredictable, impact on its future GAAP operating margin, net income attributable to BlackLine, and net income per share attributable to BlackLine.

Quarterly Conference Call

BlackLine will hold a conference call to discuss its second quarter results at 2:00 p.m. Pacific time on Tuesday, August 4, 2026. A live audio webcast will be accessible on BlackLine's investor relations website at https://investors.blackline.com. Participants can preregister for the conference call. A replay of the webcast will be available at https://investors.blackline.com for 12 months. BlackLine has used, and intends to continue to use, its Investor Relations website as a means of disclosing material non-public information and for complying with its disclosure obligations under Regulation FD.

About BlackLine

BlackLine (Nasdaq: BL), is the trust infrastructure for the AI era of finance: a future where finance drives the agentic era with intelligence, integrity, and trust rising together. The BlackLine Agentic Financial Operations Platform™, powered by Studio360 and Verity™ AI, is where the Office of the CFO scales AI across Record-to-Report, Invoice-to-Cash, and the processes where finance owns the controls and demands integrity at every step.

By unifying data, embedding AI, and engineering trust into every action, BlackLine moves finance and accounting beyond reporting on the business to orchestrating it in real time.

Supported by industry-leading R&D investment and world-class security practices, approximately 4,300 customers across multiple industries partner with BlackLine to lead their organizations into the future.

For more information, please visit blackline.com .

Non-GAAP Net Income Attributable to BlackLine and Diluted Non-GAAP Net Income Per Share Attributable to BlackLine, Inc. Non-GAAP net income attributable to BlackLine is defined as GAAP net income attributable to BlackLine adjusted for the income tax effects of acquisitions, stock-based compensation shortfalls and windfalls, and the discrete tax impact of other non-GAAP adjustments, amortization of intangible assets, stock-based compensation, amortization of debt issuance costs from our convertible senior notes, change in fair value of contingent consideration, transaction-related costs, restructuring costs, legal settlement gains or costs, adjustment to the redeemable non-controlling interest to the redemption amount, and gain on extinguishment of convertible senior notes. Diluted non-GAAP net income per share attributable to BlackLine, Inc. includes the adjustment for shares resulting from the elimination of stock-based compensation. BlackLine believes that presenting non-GAAP net income attributable to BlackLine is useful to investors as it eliminates the impact of items that have been impacted by the Company's acquisitions and other related costs to allow a direct comparison of net income between all periods presented.

Free Cash Flow . Free cash flow is defined as cash flows provided by operating activities less cash flows used to purchase property and equipment, financed and otherwise, capitalized software development, and intangible assets. BlackLine believes that presenting free cash flow is useful to investors as it provides a measure of the Company's liquidity used by management to evaluate the amount of cash generated by the Company's business including the impact of purchases of property and equipment and cost of capitalized software development.

Use of Operating Metrics

BlackLine has provided in this release and the quarterly conference call held on August 4, 2026 certain operating metrics, including (i) number of customers, (ii) Platform pricing ARR as a percentage of eligible ARR, and (iii) dollar-based net revenue retention rate, which BlackLine uses to evaluate its business, measure its performance, identify trends affecting its business, formulate financial projections and make strategic decisions.

Number of Customers . A customer is defined as a company that contributes to our subscription and support revenue as of the measurement date. In situations where an organization has multiple subsidiaries or divisions, each entity that is invoiced as a separate entity is treated as a separate customer. In an instance where an existing customer requests its invoice be divided for the sole purpose of restructuring its internal billing arrangement without any incremental increase in revenue, such customer continues to be treated as a single customer. BlackLine believes that its ability to expand its customer base is an indicator of the Company's market penetration and the growth of its business.

Platform Pricing ARR as a Percentage of Eligible ARR. Platform pricing ARR as a percentage of eligible ARR is calculated as platform annual recurring revenue divided by our eligible annual recurring revenue. We define eligible ARR as total annual recurring revenue, excluding revenue from SAP solutions-extensions ("SolEx") and the public sector.

Dollar-based Net Revenue Retention Rate . Dollar-based net revenue retention rate is calculated as the implied monthly subscription and support revenue at the end of a period for the base set of customers from which the Company generated subscription revenue in the year prior to the calculation, divided by the implied monthly subscription and support revenue one year prior to the date of calculation for that same customer base. This calculation does not reflect implied monthly subscription and support revenue for new customers added during the one-year period but does include the effect of customers who terminated during the period. Implied monthly subscription and support revenue is defined as the total amount of minimum subscription and support revenue contractually committed to, under each of BlackLine's customer agreements over the entire term of the agreement, divided by the number of months in the term of the agreement. BlackLine believes that dollar-based net revenue retention rate is an important metric to measure the long-term value of customer agreements and the Company's ability to retain and grow its relationships with existing customers over time.

Investor Contact:

Matt Humphries, CFA

matt.humphries@blackline.com

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We provide a unified, scalable, and flexible platform tailored to the evolving needs of the Office of the CFO and deliver a purpose-built suite of applications that address critical processes, including record-to-report and invoice-to-cash. Our software and services provide critical technology and industry-leading practices that deliver accurate, efficient, and intelligent financial operations. We are a holding company and conduct our operations through our wholly-owned subsidiary, BlackLine Systems.

At December 31, 2025, we had 4,394 customers, exclusive of on-premise software. Additionally, we continue to build strategic relationships with technology vendors, professional services firms, business process outsourcers, and resellers.

Our cloud-based solutions, delivered by our BlackLine Studio360 Platform, include Account Reconciliations, Transaction Matching, Task Management, Reporting & Analysis, Journal Entry, Journals Risk Analyser, Account Analysis, Consolidation, Compliance, Smart Close for SAP, Cash Application, Credit & Risk Management, Collections Management, Disputes & Deductions Management, Team & Task Management, AR Intelligence, Electronic Invoicing & Payments, Intercompany Create, Intercompany Balance & Resolve, and Intercompany Net & Settle.

In September 2025, we launched Verity, a comprehensive suite of AI capabilities that provides finance and accounting teams with a digital workforce of embedded and auditable AI. Verity is integrated throughout our solutions and supports a broad range of use cases across our customers' financial operations, offering flexible capabilities that help deliver best practices across end-to-end record-to-report and invoice-to-cash processes.

We derived approximately 95% of our revenue from subscriptions to our cloud-based software platform and approximately 5% from professional services for the year ended December 31, 2025. Our subscription contracts have initial non-cancellable terms of one year to three years with renewal options. The majority of new contracts in 2025 and 2024 carried an initial non-cancellable term of three years. In 2025, we updated our pricing model to reflect the value of our solutions based on factors such as product mix, organization size, and volumetrics (e.g. number of transactions or entities). We typically invoice subscription fees annually in advance, which are initially recorded as deferred revenue and recognized ratably over the contract term. First-year subscription fees are generally payable within 30 days of contract execution, with subsequent fees due upon renewal.

Professional services consist primarily of implementation and consulting services. Our products are available for immediate use upon granting customer access. We typically assist customers with implementation and provide consulting services to help them optimize the use of our solutions. We invoice customers for our consulting services

on a time-and-materials basis and recognize that revenue as services are performed. A limited number of our customers are provided professional services for a fixed fee, for which we invoice in advance. The fee is initially recorded as deferred revenue and recognized on a proportional-performance basis as the services are rendered.

We sell our solutions primarily through our direct sales force, which leverages our relationships with technology vendors, professional services firms, and business process outsourcers. Our solutions integrate with SAP's ERP systems, and SAP resells our product as SAP SolEx, for which we receive a percentage of the related revenues. We also maintain a strategic agreement with Google Cloud through which we jointly engage in selling and go-to-market activities to bring enhanced automation capabilities to customers.

Our ability to maximize the lifetime value of our customer relationships depends, in part, on the willingness of customers to purchase additional licenses and products from us. Our sales and customer success teams focus on maintaining high satisfaction and educating customers on the value of our full product portfolio to support account expansion.

The length of our sales cycle depends on the size of a potential customer and contract, as well as the type of solution or product being purchased. Sales cycles for global enterprise customers are generally longer than those for mid-size customers, and cycle duration increases for larger or more strategic products, such as our Intercompany solutions. As we focus on increasing average contract size and expanding adoption of strategic products, we expect the sales cycle to lengthen and remain less predictable which may contribute to variability in period-to-period results.

We have historically signed a high percentage of agreements with new customers, as well as renewal agreements with existing customers, in the fourth quarter of each year and usually during the last month of the quarter. Because most contracts have annual terms, agreements entered into late in the year typically renew during the same period in subsequent years. While this seasonality is reflected in our billings and bookings, the impact on overall revenue is minimal due to our ratable revenue recognition model.

For the years ended December 31, 2025, 2024, and 2023, we had revenues totaling $700.4 million, $653.3 million, and $590.0 million, respectively. We generated net income attributable to BlackLine, Inc. of $24.5 million, $161.2 million, and $52.8 million for the years ended December 31, 2025, 2024, and 2023, respectively.

Global Macroeconomic Factors

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following tables set forth selected historical consolidated statements of operations data, which should be read in conjunction with Critical Accounting Estimates, Liquidity and Capital Resources, and Contractual Obligations and Commitments included in this Item 7, as well as Quantitative and Qualitative Disclosures About Market Risk and the Consolidated Financial Statements and Notes thereto included elsewhere in this Annual Report on Form 10-K.

Year Ended December 31,
2025 | 2024
(in thousands)
Revenues
Subscription and support | 662,928 | 619,287
Professional services | 37,499 | 34,049
Total revenues | 700,427 | 653,336
Cost of revenues
Subscription and support | 144,038 | 135,308
Professional services | 29,347 | 26,657
Total cost of revenues | 173,385 | 161,965
Gross profit | 527,042 | 491,371
Operating expenses
Sales and marketing | 258,930 | 248,347
Research and development | 109,202 | 100,973
General and administrative | 118,732 | 121,795
Restructuring costs | 14,626 | 1,720
Total operating expenses | 501,490 | 472,835
Income from operations | 25,552 | 18,536
Other income (expense)
Interest income | 32,825 | 49,808
Interest expense | (10,149) | (8,758)
Gain on extinguishment of convertible senior notes | — | 65,112
Other income, net | 22,676 | 106,162
Income before income taxes | 48,228 | 124,698
Provision for (benefit from) income taxes | 20,971 | (43,067)
Net income | 27,257 | 167,765
Net income attributable to redeemable non-controlling interest | 3,086 | 1,952
Adjustment attributable to redeemable non-controlling interest | (347) | 4,639
Net income attributable to BlackLine, Inc. | 24,518 | 161,174

Revenues

Year Ended December 31, | Change
2025 | 2024 | %
(in thousands, except percentages)
Subscription and support | 662,928 | 619,287 | 43,641 | 7 | %
Professional services | 37,499 | 34,049 | 3,450 | 10 | %
Total revenues | 700,427 | 653,336 | 47,091 | 7 | %

Year Ended December 31,
2025 | 2024
Dollar-based net revenue retention rate | 105 | % | 102 | %
Platform pricing ARR as a percentage of eligible ARR | 11 | % | —
Number of customers | 4,394 | 4,443

The increase in revenues for the year ended December 31, 2025, compared to the year ended December 31, 2024, was primarily driven by revenue from product expansion from existing customers and bookings from new customers. The total number of customers at December 31, 2025 remained relatively flat as compared to December 31, 2024.

Cost of revenues

Year Ended December 31, | Change
2025 | 2024 | %
(in thousands, except percentages)
Subscription and support | 144,038 | 135,308 | 8,730 | 6 | %
Professional services | 29,347 | 26,657 | 2,690 | 10 | %
Total cost of revenues | 173,385 | 161,965 | 11,420 | 7 | %
Gross margin | 75.2 | % | 75.2 | %

The increase in total cost of revenues for the year ended December 31, 2025, compared to the year ended December 31, 2024, was primarily due to the following:

• $6.6 million increase in computer software expenses due to upgrades to support business growth and penetration in the public sector and overseas markets;

• $3.8 million increase in amortization of developed technology due to net additions to software placed into service;

• $1.5 million increase in professional fees; and

• $1.5 million increase in employee compensation and benefits; partially offset by

• $2.2 million decrease in depreciation and amortization due to certain assets becoming fully amortized in prior periods and an overall operational shift from traditional data centers to a cloud environment.

Sales and marketing

Year Ended December 31, | Change
2025 | 2024 | %
(in thousands, except percentages)
Sales and marketing | 258,930 | 248,347 | 10,583 | 4 | %
Percentage of total revenues | 37.0 | % | 38.0 | %

The increase in sales and marketing expenses for the year ended December 31, 2025, compared to the year ended December 31, 2024, was primarily due to the following:

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business

Overview

The Office of the Chief Financial Officer ("CFO") is relied upon to deliver timely and accurate financial reporting and business insights. The CFO role has evolved from traditional accounting processes to driving growth, profitability, and governance across the enterprise to improve business outcomes while finance and accounting teams are facing unprecedented system and process complexity, growing data volumes, and evolving regulatory requirements, coupled with expanding roles and responsibilities. As a result, digital transformation has become a top priority for CFOs, as they require powerful technology to meet these demands.

At BlackLine, our mission is to inspire, power, and guide digital finance transformation for the Office of the CFO. Our secure, flexible, and scalable cloud-based platform empowers finance and accounting teams to achieve future-ready financial operations, modernizing processes for mid-size and enterprise organizations across all industries.

Many organizations rely on enterprise resource planning ("ERP") systems to manage general ledger activities. However, these systems often fail to address end-to-end processes that occur across other systems and in spreadsheets, hampering an organization's ability to deliver accurate data, insights, controls, and transparency. Our platform connects data and processes at their origin, enhancing financial reporting integrity, streamlining activities, and delivering faster insights. This approach drives immediate impact and sustained value, maximizes cash flow, and accelerates the record-to-report and invoice-to-cash processes.

Our platform integrates with the leading ERP systems offered by Workday, Inc., SAP SE ("SAP"), Oracle Corporation, Microsoft Dynamics 365 ("Microsoft Dynamics"), an application offered by Microsoft Corporation ("Microsoft"), Sage Intacct, Inc., and NetSuite, Inc. It also connects to diverse financial data sources, including banks, point-of-sale, treasury, payroll, procurement, and other systems, bringing data into unified workflows. This deep connectivity provides finance and accounting teams with accurate, actionable insights, reducing errors and

improving compliance. This, in turn, frees finance and accounting teams to focus on complex, high-value challenges where human judgement is essential.

For nearly 25 years, BlackLine has pioneered customer-centric innovation in financial software, optimizing mission-critical processes for the Office of the CFO. BlackLine's Studio360 Platform, Verity AI capabilities, and our comprehensive record-to-report and invoice-to-cash solutions uniquely address the increasing complexity of data, systems, and processes.

BlackLine was founded in 2001. We are a holding company and conduct our operations through our wholly-owned subsidiary, BlackLine Systems, Inc. ("BlackLine Systems") and its subsidiaries. Our growth has been driven by a combination of organic innovation and a series of strategic acquisitions and initiatives, including the following:

Our cloud-based solutions, delivered by our BlackLine Studio360 Platform, include Account Reconciliations, Transaction Matching, Task Management, Reporting & Analysis, Journal Entry, Journals Risk Analyser, Account Analysis, Consolidation, Compliance, Smart Close for SAP, Cash Application, Credit & Risk Management, Collections Management, Disputes & Deductions Management, Team & Task Management, AR Intelligence, Electronic Invoicing & Payments, Intercompany Create, Intercompany Balance & Resolve, and Intercompany Net & Settle.

In September 2025, we launched Verity, a comprehensive suite of AI capabilities that provides finance and accounting teams with a digital workforce of embedded and auditable AI. Verity is integrated throughout our solutions and supports a broad range of use cases across our customers' financial operations, offering flexible capabilities that help deliver best practices across end-to-end record-to-report and invoice-to-cash processes.

On December 15, 2025, we acquired WiseLayer, ("WL" and such acquisition, the "WL Acquisition"), a New York-based company that has pioneered a digital workforce of AI-powered agents to automate complex, judgment-based finance and accounting processes. The primary purpose of the WL Acquisition is to accelerate BlackLine's own AI roadmap and in so doing, strengthen our competitive offering, which is focused on transforming and modernizing finance and accounting, against key competitors.

Our Growth Strategy

Our principal growth strategies include the following:

Continue to Innovate and Expand our Solutions. Our ability to internally develop or make strategic acquisitions of new, market-leading applications and functionalities, particularly those powered by AI, is integral to our success. Our recent launch of Verity is a testament to our commitment to delivering advanced, AI-powered solutions. We intend to deepen our existing capabilities and extend the functionality and range of our applications to bring new solutions to the Office of the CFO.

Enhance our Leadership Position within the Marketplace. We intend to focus on customer expansion, geography, and industry to maintain and grow our leadership position.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
