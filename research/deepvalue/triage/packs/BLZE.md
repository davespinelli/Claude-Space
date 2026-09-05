# Triage pack — BLZE · Backblaze, Inc.

_Generated 2026-09-05 01:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** BLZE · **Name:** Backblaze, Inc.
- **CIK:** 0001462056
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/BLZE

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Backblaze, Inc.
- **CIK:** 1,462,056 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 13.31 |
| mktcap | $823.9M |
| ev | $791.5M |
| ev_ebit | n/a |
| fcf | $18.9M |
| fcf_yield | 2.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -33.3% |
| net_debt | -$32.4M |
| net_debt_ebit | n/a |
| cash | $32.4M |
| ltd | $0.00 |
| equity | $88.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $145.8M |
| revenue_prior | $127.6M |
| rev_growth | 14.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$23.6M |
| net_income | -$25.6M |
| cfo | $23.5M |
| capex | $4.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 9.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 61,900,000 |
| shares_py | 56,500,000 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 121.7% |
| r6m | 254.9% |
| off_52w_high | -34.9% |
| adv20 | $48.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.32 |
| r_ev_ebit | 0.00 |
| r_roic | 0.02 |
| r_rev_growth | 0.75 |
| r_buyback | 0.13 |
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
| rank | 413 |

**Screen rationale:** revenue +14.3%; debt data missing (net cash unverified); 12-1 momentum 121.7%


## 3. Share count trend

- Shares outstanding: **61,900,000** (CY2026Q2I) vs **56,500,000** prior year (CY2025Q2I)
- Change: **9.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-24** — Item 1.01 (Entry into a Material Definitive Agreement): On August 24, 2026, Backblaze, Inc. (the "Company") issued $201.25 million aggregate principal amount of the Company's 0.00%
- **2026-07-02** — Item 1.01 (Entry into a Material Definitive Agreement): On June 30, 2026, Backblaze, Inc. (the "Company") amended the negative covenant in its existing credit agreement with Citizens Bank, N.A. regarding the Company's ability to undertake capitalized lease transactions (the "Credit Agreement Amendment").
- **2026-06-23** — Item 1.01 (Entry into a Material Definitive Agreement): Effective on June 16, 2026, Backblaze, Inc. (the "Company") entered into a Master Strategic Agreement with CoreWeave, Inc. ("CoreWeave"), along with Addendum No. 1 thereto (collectively, the "MSA"), pursuant to which the Company will provide CoreWeave with...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 14,965 sh / $236,746 -> net $-236,746 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 7 |
| D | 4 |
| F | 4 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Financial Highlights: (1)'; skipped 22 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex991blze20260630earningsp.htm)

Second Quarter 2026 Financial Highlights: (1)

• Revenue of $42.7 million, an increase of 18% year-over-year (YoY).

• B2 Cloud Storage revenue was $26.6 million, an increase of 34% YoY.

• Computer Backup revenue was $16.1 million, a decrease of 2% YoY.

• Gross profit of $26.8 million, or 63% of revenue, compared to $23.0 million, or 63% of revenue, in Q2 2025.

• Adjusted gross profit of $34.3 million, or 80% of revenue, compared to $28.8 million, or 79% of revenue, in Q2 2025.

• Net loss was $5.1 million compared to a net loss of $7.1 million in Q2 2025.

• Net loss per share was $0.08 compared to a net loss per share of $0.13 in Q2 2025.

• Adjusted EBITDA was $12.8 million, or 30% of revenue, compared to $6.6 million, or 18% of revenue, in Q2 2025.

• Non-GAAP net income of $5.0 million compared to non-GAAP net income of $0.8 million in Q2 2025.

• Non-GAAP net income per share of $0.08 compared to a non-GAAP net income per share of $0.01 in Q2 2025.

• Cash flow from operations during the six months ended June 30, 2026 was $13.8 million, compared to $8.5 million for the same period in 2025.

• Adjusted free cash flow during the six months ended June 30, 2026 was $1.4 million, compared to $(6.0) million for the same period in 2025.

• Cash, cash equivalents, and marketable securities totaled $49.9 million as of June 30, 2026.

(1) Some amounts may not sum due to rounding.

Second Quarter 2026 Operational Highlights:

• Annual recurring revenue (ARR) was $177.3 million, an increase of 21% YoY.

◦ B2 Cloud Storage ARR was $113.3 million, an increase of 39% YoY.

◦ Computer Backup ARR was $64.0 million, relatively flat YoY.

• Net revenue retention rate (NRR) was 103% compared to 106% in Q2 2025.

◦ B2 Cloud Storage NRR was 113% compared to 114% in Q2 2025.

◦ Computer Backup NRR was 94% compared to 99% in Q2 2025.

• Gross customer retention rate was 91% in Q2 2026 compared to 90% in Q2 2025.

◦ B2 Cloud Storage gross customer retention rate was 89% in both Q2 2026 and Q2 2025.

◦ Computer Backup gross customer retention rate was 91% compared to 90% in Q2 2025.

Recent Business Highlights:

• Signed a 5+ year, $335 million strategic agreement with CoreWeave: The landmark agreement includes warrants valued at approximately $22 million, aligning the companies' long-term interests and validating Backblaze as a strategic storage tier provider for AI workloads at massive scale.

• Expanded momentum with larger customers: ARR from customers generating $50,000+ in ARR grew 67% year over year, and the number of these customers increased 57% year over year, reflecting continued success scaling with larger accounts.

• Won largest B2 Overdrive deal to date with a frontier AI model: Signed a seven-figure ARR B2 Overdrive deal with a leading AI model developer, demonstrating demand for high-performance, cost-effective storage for AI workloads.

• Strengthened long-term revenue visibility: RPO reached $396 million, up $319.5 million quarter over quarter, led by the CoreWeave agreement and demand from AI-native companies.

• Expanded the B2 developer ecosystem: Shipped new SDKs and AI agent tools and launched Backblaze's Generative Media Hackathon, increasing awareness of B2 as a storage platform for AI applications.

Financial Outlook:

Based on information available as of the date of this press release,

For the third quarter of 2026, we expect:

• Revenue between $44.4 million and $44.8 million.

• Adjusted EBITDA margin between 27% and 29%.

• Basic weighted average shares outstanding of 62.3 million to 62.5 million shares.

For full-year 2026, we have raised our outlook:

• Revenue between $172.0 million and $174.0 million, raised from $161.5 million to $163.5 million.

• Adjusted EBITDA margin range of 27% to 29%, raised from 23% to 25%.

Conference Call Information:

Backblaze will host a conference call today, August 3, 2026, at 2:00 p.m. PT (5:00 p.m. ET) to review its financial results.

Attend the webcast here: https://events.q4inc.com/attendee/704175018

An archive of the webcast will be available shortly after its completion on the Investor Relations section of the Backblaze website at https://ir.backblaze.com.

Register to listen by phone here: https://events.q4inc.com/analyst/704175018?pwd=29EpzfWI

Phone registrants will receive dial-in information via email.

About Backblaze

Backblaze (NASDAQ: BLZE) is the object storage layer powering AI infrastructure and data-intensive workloads at scale. Built over two decades, the company has leveraged hardware, software, and operational innovation into a platform that delivers the performance and economics the AI era demands—without lock-in. Today, more than 500,000 customers trust Backblaze to move and store the data powering their businesses, reaching hundreds of millions of end users across 175 countries. For more information, visit www.backblaze.com.

Adjusted EBITDA and Adjusted EBITDA Margin

We define Adjusted EBITDA as net loss adjusted to exclude depreciation and amortization, stock-based compensation, interest expense, investment income, income tax provision, realized and unrealized gains and losses on foreign currency transactions, impairment of long-lived assets, restructuring charges, legal settlement costs, and other non-recurring charges. Adjusted EBITDA Margin is defined as Adjusted EBITDA divided by revenues for the period. We use Adjusted EBITDA and Adjusted EBITDA Margin to evaluate our ongoing operations and for internal planning and forecasting purposes. We believe that Adjusted EBITDA and Adjusted EBITDA Margin, when taken together with our GAAP financial results, provide meaningful supplemental information regarding our operating performance by excluding certain items that may not be indicative of our business, results of operations, or outlook. We consider Adjusted EBITDA and Adjusted EBITDA Margin to be important measures because they help illustrate underlying trends in our business and our historical operating performance on a more consistent basis.

Non-GAAP Net Income (Loss) and Non-GAAP Net Income (Loss) Per Share

We define non-GAAP net income (loss) as net income (loss) adjusted to exclude stock-based compensation, realized and unrealized gains and losses on foreign currency transactions, impairment of long-lived assets, restructuring charges, legal settlement costs, and other items we deem non-recurring. Non-GAAP net income (loss) per share is defined as non-GAAP net income (loss) divided by basic and diluted weighted average common shares outstanding. We believe that non-GAAP net income (loss) and non-GAAP net income (loss) per share, when taken together with our GAAP financial results, provide meaningful supplemental information regarding our operating performance by excluding certain items that may not be indicative of our business, results of operations, or outlook.

Adjusted Free Cash Flow and Adjusted Free Cash Flow Margin

We believe that Adjusted Free Cash Flow and Adjusted Free Cash Flow Margin are useful metrics for assessing liquidity that provide information to management and investors about the cash generated from our core operations that can be reinvested in the business. However, these measures should not replace cash flows from operations as a liquidity benchmark. One limitation of these metrics is that they do not reflect our future contractual commitments, nor do they capture the overall changes in our cash balance during a specific period. Nonetheless, we believe that Adjusted Free Cash Flow and Adjusted Free Cash Flow Margin are key metrics providing insight on our financial trajectory that helps us make informed decisions as we work towards sustainable positive cash flow.

We define adjusted free cash flow as net cash provided by operating activities less purchases of property and equipment, capitalized internal-use software costs, principal payments on finance leases and lease financing obligations, as reflected in our consolidated statements of cash flows, and excluding payments on restructuring charges, legal settlement payments, and payments on other non-recurring charges. Adjusted free cash flow margin is calculated as adjusted free cash flow divided by revenue.

Other Non-GAAP Measures

Adjusted Cost of Revenue and Adjusted Operating Expenses

Adjusted research and development, adjusted sales and marketing, and adjusted general and administrative (collectively, "adjusted operating expenses") and adjusted cost of revenue are non-GAAP financial measures that we define as each respective GAAP expense category excluding stock-based compensation expense, depreciation and amortization, restructuring costs, and other non-recurring charges. These measures provide management with greater transparency into the underlying trends in our business by facilitating period-to-period comparisons of our ongoing cost structure, excluding the impact of certain non-cash or non-recurring items that may not be indicative of our operating performance. These measures are intended to assist in forecasting and budgeting by providing greater visibility into our normalized expense base.

Key Business Metrics:

Annual Recurring Revenue (ARR)

We define ARR as the annualized value of all Backblaze B2 and Computer Backup arrangements as of the end of a period. Given the renewable nature of our business, we view ARR as an important indicator of our financial performance and operating results, and we believe it is a useful metric for internal planning and analysis. For subscription-based arrangements, ARR is calculated by multiplying the monthly revenue for the last month of a period by 12. For consumption-based arrangements, ARR is calculated by multiplying average daily revenue for the last month of a period by 365. Total Company ARR represents the annualized value of all B2 Cloud Storage consumption- and subscription-based arrangements and Computer Backup subscription-based arrangements as of the end of a period.

Beginning in the first quarter of 2026, to improve comparability between periods, we revised our methodology for calculating ARR for our consumption-based arrangements to use a daily revenue rate during the last month of the period rather than a monthly rate. Prior period ARR amounts presented have been recast to conform to the current period presentation.

Net Revenue Retention Rate (NRR)

To calculate NRR for a specific quarter, we determine the revenue recognized in that quarter from customers who generated revenue during the last month of the same quarter of the previous year. This revenue is then divided by the revenue generated from those same customers in the prior year quarter.

Beginning in the first quarter of 2026, we are presenting NRR using a single-quarter calculation, comparing current quarter revenue to the corresponding prior year quarter, rather than an average of quarterly rates over the prior four quarters, in order to provide a more current measure of customer retention. Prior period NRR amounts have been recast to conform to the current period presentation.

Gross Customer Retention Rate

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-10_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a high-performance cloud storage platform for data-intensive use cases in the artificial intelligence ("AI") era and across a broad range of modern cloud workloads, designed to help customers address complex storage needs by reducing the barriers of lock-in, complexity, and cost. Our mission is to make customers succeed by solving their toughest data storage challenges. We aim to achieve this mission through our purpose-built, web-scale software infrastructure, which is essential to the global data center and compute infrastructure buildout.

We provide cloud services through a purpose-built, web-scale software infrastructure built on commodity hardware. We believe that by offering a cloud storage solution optimized for price-to-performance at scale, engineered for efficiency, and priced predictably, we substantially reduce the cost, complexity and frustration of storing, using, and protecting data, and we empower customers to focus on their core business operations. Customers use us to support their AI workflows, help ensure the cyber-resilience of their organizations, streamline their media workflows, and enable a variety of other data-focused application and information technology ("IT") needs. Through our blog and culture of transparency, we have built a community of millions of readers and brand advocates. Our direct sales activities, channel and technology partners, and referrals from our community of brand advocates, combined with our highly efficient and self-serve customer acquisition model have allowed us to attract over 500,000 customers as of December 31, 2025, and our direct sales activities have historically supported us in acquiring larger customers, including leading neocloud platforms via our Powered by Backblaze program. As we move up-market, we expect our direct sales activities to increasingly contribute to the acquisition of customers like these. Our customers use our Backblaze Storage Cloud platform across more than 175 countries to store and protect their data with an aggregate of approximately 5 billion gigabytes of data storage under management.

Our Backblaze Storage Cloud provides a platform that is the foundation for our B2 Cloud Storage Infrastructure-as-a-Service ("IaaS") offering, our B2 Overdrive high-performance IaaS offering, our Powered by Backblaze white label IaaS offering, and our Computer Backup Software-as-a-Service ("SaaS") offering. B2 Cloud Storage enables customers to store data, developers to build applications, and partners to expand their use cases. The amount of data stored in this cloud service can scale up and down as needed primarily on a pay-as-you-go basis or can be paid for on a capacity or committed contract basis for greater predictability. B2 Overdrive is built on the foundation of B2 Cloud Storage. It enables AI and data-driven workloads with up to 1Tbps throughput, unlimited free egress, and private networking support. Powered by Backblaze is also built on the foundation of B2 Cloud Storage. It enables neocloud and application platforms to bolster existing products or expand their product offerings with cloud storage via the Backblaze Partner API and custom domains (CNAME) technology. Computer Backup automatically backs up data from laptops and desktops for businesses and individuals. This cloud backup service offers easily understood primarily flat-rate pricing to continuously back up a virtually unlimited amount of data.

We focus on specialized storage and an open cloud ecosystem that integrates with a broad range of partners. Ongoing investment in our technology platform and related features has driven customer, community, and product milestones. Starting in the second half of 2024, we initiated a go-to-market transformation that is actively moving the company up-market, which has been evidenced by the signing of multiple deals with total contract values over $1.0 million each and revenue growth for B2 Cloud Storage of 26% for the year ended December 31, 2025 compared to 2024.

Product Updates

To support our up-market expansion and evolving customer needs, we recently launched B2 Overdrive, our premium-priced, ultra high-throughput performance cloud storage solution, designed to meet the demands of data-intensive workloads including AI and machine-learning training, large-scale analytics, high-performance computing, and media processing. We also introduced a suite of enterprise cyber security features including AI-powered anomaly alerts, mandatory multifactor authentication, bucket access logging, and Enterprise Web Console which streamlines role-based administrative control in complex environments to help with cybersecurity and account management. These launches expand our addressable market among enterprise and AI-driven customers and lay the groundwork for further innovation to drive differentiated value for these customers.

Financial Developments

Banking Relationship and Line of Credit

On June 4, 2025, we entered into a credit agreement with Citizens Bank, N.A., establishing a senior secured revolving credit facility with a total borrowing capacity of up to $20.0 million to be used for general corporate purposes and working capital needs. As of December 31, 2025, the Company had no outstanding borrowings under this facility.

2025 Restructuring and Transformation Plan

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth our consolidated statements of operations and comprehensive loss data for the periods indicated:

For the Years Ended December 31,
2025 | 2024 | 2023
(in thousands)
Revenue | 145,835 | 127,628 | 102,019
Cost of revenue | 57,042 | 58,285 | 52,162
Gross profit | 88,793 | 69,343 | 49,857
Operating expenses:
Research and development | 46,109 | 42,098 | 39,527
Sales and marketing | 37,397 | 44,440 | 41,270
General and administrative | 28,910 | 29,094 | 26,965
Total operating expenses | 112,416 | 115,632 | 107,762
Loss from operations | (23,623) | (46,289) | (57,905)
Investment income | 1,961 | 1,422 | 1,984
Interest expense | (3,866) | (3,658) | (3,792)
Loss before provision for income taxes | (25,528) | (48,525) | (59,713)
Income tax provision | 84 | 6 | —
Net loss and comprehensive loss | (25,612) | (48,531) | (59,713)

The following table sets forth our consolidated statements of operations and comprehensive loss data expressed as a percentage of revenue for the periods indicated: (1)

For the Years Ended December 31,
2025 | 2024 | 2023
Revenue | 100 | % | 100 | % | 100 | %
Cost of revenue | 39 | 46 | 51
Gross profit | 61 | 54 | 49
Operating expenses:
Research and development | 32 | 33 | 39
Sales and marketing | 26 | 35 | 40
General and administrative | 20 | 23 | 26
Total operating expenses | 77 | 91 | 106
Loss from operations | (16) | (36) | (57)
Investment income | 1 | 1 | 2
Interest expense | (3) | (3) | (4)
Loss before provision for income taxes | (18) | (38) | (59)
Income tax provision | — | — | —
Net loss | (18) | % | (38) | % | (59) | %

(1) Totals may not sum due to rounding.

The following table includes stock-based compensation, depreciation and amortization, and restructuring charges as they are included in the results of operations:

For the Years Ended December 31,
2025 | 2024 | 2023
(in thousands)
Stock-based compensation (1)
Cost of revenue | 1,557 | 1,616 | 1,986
Research and development | 12,094 | 10,392 | 9,218
Sales and marketing | 6,119 | 8,280 | 8,721
General and administrative | 6,655 | 5,816 | 5,127
Total stock-based compensation | 26,425 | 26,104 | 25,052
Depreciation and amortization (2)
Cost of revenue | 25,136 | 27,761 | 24,331
Research and development | 170 | 262 | 261
Sales and marketing | 117 | 190 | 189
General and administrative | 70 | 115 | 131
Total depreciation and amortization | 25,493 | 28,328 | 24,912
Restructuring charges
Cost of revenue | 115 | 460 | —
Research and development | 285 | 1,278 | 2,311
Sales and marketing | 687 | 1,867 | 1,025
General and administrative | 1,385 | 1,256 | 280
Total restructuring charges | 2,472 | 4,861 | 3,616

(1) $2.5 million of stock-based compensation incurred during the year ended December 31, 2024 is classified as restructuring charges in the table above, including $0.3 million related to cost of revenue , $0.9 million related to research and development costs, $1.2 million related to sales and marketing costs, and $0.1 million related to general and administrative costs. $0.1 million of stock-based compensation incurred during the year ended December 31, 2023, which were related to sales and marketing and general and administrative costs, is classified as restructuring charges in the table above. A nominal amount of stock-based compensation incurred during the year ended December 31, 2025 is classified as restructuring charges in the table above. For further information on our restructuring plan, s ee Note 16 to our consolidated financial statements included elsewhere in this Annual Report on Form 10-K.

(2) $0.1 million of depreciation and amortization expense recorded to cost of revenue for the year ended December 31, 2025 is classified as restructuring charges in the table above, as these charges were incurred as part of our 2025 Restructuring and Transformation Plan.

Comparison of the Years Ended December 31, 2025 and 2024

Revenue

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-10_item1_business.md)

Item 1. Business

Overview

We are a high-performance cloud storage platform for data-intensive use cases in the artificial intelligence ("AI") era and across a broad range of modern cloud workloads, designed to help customers address complex storage needs by reducing the barriers of lock-in, complexity, and cost. Our mission is to make customers succeed by solving their toughest data storage challenges. We aim to achieve this mission through our purpose-built, web-scale software infrastructure, which is essential to the global data center and compute infrastructure buildout.

We provide cloud services through a purpose-built, web-scale software infrastructure built on commodity hardware. We believe that by offering a cloud storage solution optimized for price-to-performance at scale, engineered for efficiency, and priced predictably, we substantially reduce the cost, complexity and frustration of storing, using, and protecting data, and we empower customers to focus on their core business operations. Customers use us to support their AI workflows, help ensure the cyber-resilience of their organizations, streamline their media workflows, and enable a variety of other data-focused application and information technology ("IT") needs. Through our blog and culture of transparency, we have built a community of millions of readers and brand advocates. Our direct sales activities, channel and technology partners, and referrals from our community of brand advocates, combined with our highly efficient and self-serve customer acquisition model have allowed us to attract over 500,000 customers as of December 31, 2025, and our direct sales activities have historically supported us in acquiring larger customers, including leading neocloud platforms via our Powered by Backblaze program. As we move up-market, we expect our direct sales activities to increasingly contribute to the acquisition of customers like these. Our customers use our Backblaze Storage Cloud platform across more than 175 countries to store and protect their data with an aggregate of approximately 5 billion gigabytes of data storage under management.

At its founding, Backblaze set out to dramatically simplify the process of storing, using, and protecting data. Over the following years, we focused relentlessly on cutting away the complexity common among traditional cloud vendors' services and legacy on-premises system vendors. Today, we believe that our solutions are differentiated by their performance and cost efficiency while also delivering reliability and ease of use. Our strategy centers on a focused set of storage use cases and participation in an open cloud ecosystem, which we believe positions us to prioritize opportunities with emerging data-heavy workloads like those with AI model builders and neocloud platforms utilizing our Powered by Backblaze program. Alongside these emerging opportunities, we continue to grow our business and opportunities among the developers of application storage solutions while also continuing to service our foundational use cases including media and entertainment and cyber resilience. Finally, we continue to invest in our self-serve user base, where developers who are experimenting with AI can experiment and grow within our storage platform.

Our Platform and Cloud Services

Backblaze Storage Cloud

The Backblaze Storage Cloud provides the core platform for our cloud services and is designed to deliver high-performance, secure, reliable object storage at exabyte scale. It currently manages ov er 1 trillion files which are available on demand and is designed to scale efficiently to meet growing enterprise workloads and AI-driven data demands. The key enabler of the Backblaze Storage Cloud is its proprietary global-scale system and software architecture, which manages our global physical infrastructure, including hundreds of thousands of hard drives across multiple data centers.

The web-scale software layer receives, stores, and delivers data for customers across the globe, intelligently allocating storage based on capacity and demand to maintain availability and durability at scale. Managing ever-growing volumes of data across increasingly large hard drives while maintaining durability, availability, and throughput is highly complex. We believe that continued investment in developing performance optimization, efficiency improvements, operational support, and other software innovation enhances our ability to efficiently leverage hardware and scale cost-effectively. Alongside these core processes, this software architecture manages load balancing, caching, deletion, billing, and other essential

functions for hundreds of thousands of customers. Regular updates to our codebase further strengthen these capabilities and improve the overall performance of our Infrastructure-as-a-Service platform ("IaaS").

Our vault architecture creates redundancy for the storage of customer data using proprietary and other algorithms. Our software splits each uploaded customer file into several data parts, adds multiple redundant parts, and stores these parts across discrete hard drives in different servers in a data center. As a result, even if a few of the parts are entirely lost or offline, we are able to reconstruct the customer data from the remaining parts for durability and availability. Our globally distributed storage platform also offers customers multi-region geographic choice for their data, including East and West Coast regions in the United States, as well as regions in Canada, and Europe, providing flexibility for different needs including geopolitical considerations, regulatory requirements, and performance optimization.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-03-10_item7_mdna.md, 10-K_2026-03-10_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
