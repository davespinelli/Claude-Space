# Triage pack — RDVT · Red Violet, Inc.

_Generated 2026-09-04 20:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** RDVT · **Name:** Red Violet, Inc.
- **CIK:** 0001720116
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/RDVT

**Fetcher warnings for this ticker:** 10-K 2026-03-04: heading split missed Item 7 - MD&A

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Red Violet, Inc.
- **CIK:** 1,720,116 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 76.43 |
| mktcap | $1.2B |
| ev | $1.2B |
| ev_ebit | 89.5x |
| fcf | $28.8M |
| fcf_yield | 2.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 16.8% |
| net_debt | -$50.0M |
| net_debt_ebit | -3.8x |
| cash | $50.0M |
| ltd | $0.00 |
| equity | $111.6M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $90.3M |
| revenue_prior | $75.2M |
| rev_growth | 20.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $13.1M |
| net_income | $13.2M |
| cfo | $29.3M |
| capex | $563k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 14.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 16,046,975 |
| shares_py | 13,977,738 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 39.7% |
| r6m | 65.1% |
| off_52w_high | 0.0% |
| adv20 | $19.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.33 |
| r_ev_ebit | 0.07 |
| r_roic | 0.84 |
| r_rev_growth | 0.83 |
| r_buyback | 0.09 |
| score | 0.48 |

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
| rank | 264 |

**Screen rationale:** high ROIC 16.8%; revenue +20.0%; debt data missing (net cash unverified); 12-1 momentum 39.7%


## 3. Share count trend

- Shares outstanding: **16,046,975** (CY2026Q2I) vs **13,977,738** prior year (CY2025Q2I)
- Change: **14.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-07** — Item 1.01 (Entry into a Material Definitive Agreement): On August 5, 2026, Red Violet, Inc. (the "Company" or "Red Violet") entered into an underwriting agreement (the "Underwriting Agreement") with Raymond James & Associates, Inc. and Needham & Company, LLC, as representatives of the several underwriters named in...
- **2026-06-05** — Item 5.02 (officer / director change or comp arrangement): The information set forth under Item 5.07 is incorporated herein by reference.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 2,000 sh / $142,980 vs sells 46,000 sh / $2,641,830 -> net $-2,498,850 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: LIVEK WILLIAM PAUL bought 2,000 sh @ $71.49 ($142,980) on 2026-08-27.

Form 4 filings parsed: 12; transaction rows: 16 (open-market buys 1, sales 8).

| code | rows |
|---|---|
| A | 7 |
| P | 1 |
| S | 8 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-11_2-02-results.md)

_Extraction: started at the first release heading, 'red violet Reports Second Quarter 2026 Financial Results'; skipped 12 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (rdvt-ex99_1.htm)

red violet Reports Second Quarter 2026 Financial Results

Record Revenue of $26.7 Million, an Increase of 23%; Record Cash Flow from Operations of $10.6 Million

BOCA RATON, Fla. – August 10, 2026 – Red Violet, Inc. (NASDAQ: RDVT), a leading identity intelligence and analytics company, today announced financial results for the quarter ended June 30, 2026.

"The demand we are seeing for identity intelligence has never been stronger, and red violet is exceptionally well positioned to capture it. In Q2, we added a record 447 new customers to IDI in a quarter where revenue, profitability, and cash flow all hit new highs," stated Derek Dubner, red violet's CEO. "Our success is rooted in our proprietary assets, including an AI-embedded architecture consisting of a unique entity resolution engine which fuels a differentiated identity graph, that continues to prove its value across consequential transactions in the economy. With no debt, more than $160 million in cash following our recently completed offering, and the strongest pipeline of strategic initiatives in the Company's history, we are positioned to extend our leadership in ways that were not possible even twelve months ago. We remain disciplined in how we deploy capital, yet we have never been more confident in the opportunities ahead."

Second Quarter Financial Results

For the three months ended June 30, 2026 as compared to the three months ended June 30, 2025:

•
Total revenue increased 23% to $26.7 million.

•
Gross profit increased 29% to $20.2 million. Gross margin increased to 76% from 72%.

•
Adjusted gross profit increased 25% to $22.9 million. Adjusted gross margin increased to 86% from 84%.

•
Net income increased 85% to $5.0 million, which resulted in earnings of $0.35 and $0.34 per basic and diluted share, respectively. Net income margin increased to 19% from 12%.

•
Adjusted EBITDA increased 48% to $11.2 million. Adjusted EBITDA margin increased to 42% from 35%.

•
Adjusted net income increased 58% to $7.2 million, which resulted in adjusted earnings of $0.51 and $0.50 per basic and diluted share, respectively.

•
Net cash provided by operating activities increased 42% to $10.6 million.

•
Cash and cash equivalents were $50.0 million as of June 30, 2026.

Second Quarter and Recent Business Highlights

•
Announced the August 2026 closing of an underwritten public offering of 1,916,667 shares of common stock, including 250,000 shares of common stock sold pursuant to the full exercise of the underwriters' option, providing net proceeds of approximately $109.0 million, after deducting underwriting discounts and commissions and estimated offering expenses. The Company intends to use the net proceeds from the offering for working capital and general corporate purposes, including potential strategic acquisitions.

•
Added a record 447 customers to IDI ™ during the second quarter, ending the quarter with 10,869 customers.

•
Added 25,493 users to FOREWARN ® during the second quarter, ending the quarter with 443,173 users. 660 REALTOR ® Associations throughout the U.S. are now contracted to use FOREWARN.

•
Purchased 74,500 shares of the Company's common stock year to date through June 30, 2026, at an average price of $41.87 per share pursuant to the Company's Stock Repurchase Program. As of June 30, 2026, the Company had $15.5 million remaining under the Stock Repurchase Program.

Conference Call

In conjunction with this release, red violet will host a conference call and webcast today at 4:30 pm ET to discuss its quarterly results and provide a business update. Please click here to pre-register for the conference call and obtain your dial in number and passcode. To access the live audio webcast, visit the Investors section of the red violet website at www.redviolet.com . Please login at least 15 minutes prior to the start of the call to ensure adequate time for any downloads that may be required. Following the completion of the conference call, an archived webcast of the conference call will be available on the Investors section of the red violet website at www.redviolet.com .

About red violet ®

At red violet, we build proprietary technologies and apply analytical capabilities to deliver identity intelligence. Our technology powers critical solutions, which empower organizations to operate with confidence. Our solutions enable the real-time identification and location of people, businesses, assets and their interrelationships. These solutions are used for purposes including identity verification, risk mitigation, due diligence, fraud detection and prevention, regulatory compliance, and customer acquisition. Our cloud-native, AI-embedded identity intelligence platform, CORE™, is purpose-built for the enterprise, yet flexible enough for organizations of all sizes, bringing clarity to massive datasets by transforming data into intelligence. Our solutions are used today to enable frictionless commerce, enhance safety, and mitigate fraud and the related financial losses borne by society. For more information, please visit www.redviolet.com .

Company Contact:

Camilo Ramirez

Red Violet, Inc.

561-757-4500

ir@redviolet.com

Investor Relations Contact:

Steven Hooser

Three Part Advisors

214-872-2710

ir@redviolet.com

Use of Non-GAAP Financial Measures

Management evaluates the financial performance of our business on a variety of key indicators, including non-GAAP metrics of adjusted EBITDA, adjusted EBITDA margin, adjusted net income, adjusted earnings per share, adjusted gross profit, adjusted gross margin, and free cash flow ("FCF"). Adjusted EBITDA is a non-GAAP financial measure equal to net income, the most directly comparable financial measure based on US GAAP, excluding interest income, income tax expense, depreciation and amortization, share-based compensation expense, acquisition-related costs, litigation costs, and write-off of long-lived assets. We define adjusted EBITDA margin as adjusted EBITDA as a percentage of revenue. Adjusted net income is a non-GAAP financial measure equal to net income, the most directly comparable financial measure based on US GAAP, adjusted to exclude share-based compensation expense, amortization of share-based compensation capitalized in intangible assets, acquisition-related costs, litigation costs, and write-off of long-lived assets, and to include the tax effect of adjustments. We define adjusted earnings per share as adjusted net income divided by the weighted average shares outstanding. We define adjusted gross profit as gross profit plus depreciation and amortization of certain intangible assets, and adjusted gross margin as adjusted gross profit as a percentage of revenue. We define FCF as net cash provided by operating activities reduced by purchase of property and equipment, and capitalized costs included in intangible assets.

June 30, 2026 | December 31, 2025
ASSETS:
Current assets:
Cash and cash equivalents | 49,972 | 43,557
Accounts receivable, net of allowance for doubtful accounts of $145 and $231 as of June 30, 2026 and December 31, 2025, respectively | 12,904 | 10,697
Prepaid expenses and other current assets | 2,359 | 2,281
Total current assets | 65,235 | 56,535
Property and equipment, net | 914 | 882
Intangible assets, net | 41,196 | 39,264
Goodwill | 5,227 | 5,227
Right-of-use assets | 2,311 | 2,570
Deferred tax assets | 4,618 | 6,585
Other noncurrent assets | 847 | 949
Total assets | 120,348 | 112,012
LIABILITIES AND SHAREHOLDERS' EQUITY:
Current liabilities:
Accounts payable | 1,489 | 1,977
Accrued expenses and other current liabilities | 2,882 | 4,469
Current portion of operating lease liabilities | 428 | 396
Deferred revenue | 1,195 | 1,028
Total current liabilities | 5,994 | 7,870
Noncurrent operating lease liabilities | 2,219 | 2,396
Other noncurrent liabilities | 523 | 820
Total liabilities | 8,736 | 11,086
Shareholders' equity:
Preferred stock—$0.001 par value, 10,000,000 shares authorized, and 0 shares issued and outstanding, as of June 30, 2026 and December 31, 2025 | - | -
Common stock—$0.001 par value, 200,000,000 shares authorized, 14,114,395 and 14,151,350 shares issued and outstanding, as of June 30, 2026 and December 31, 2025 | 14 | 14
Additional paid-in capital | 89,966 | 88,628
Retained earnings | 21,632 | 12,284
Total shareholders' equity | 111,612 | 100,926
Total liabilities and shareholders' equity | 120,348 | 112,012

RED VIOLET, INC.

CONDENSED CONSOLIDATED STATEMENTS O F OPERATIONS

(Amounts in thousands, except share data)

(unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue | 26,718 | 21,774 | 52,548 | 43,777
Costs and expenses (1) :
Cost of revenue (exclusive of depreciation and amortization) | 3,818 | 3,501 | 7,637 | 7,162
Sales and marketing expenses | 5,750 | 5,622 | 11,608 | 11,029
General and administrative expenses | 8,268 | 7,253 | 16,167 | 13,427
Depreciation and amortization | 2,787 | 2,647 | 5,597 | 5,197
Total costs and expenses | 20,623 | 19,023 | 41,009 | 36,815
Income from operations | 6,095 | 2,751 | 11,539 | 6,962
Interest income | 394 | 339 | 738 | 647
Income before income taxes | 6,489 | 3,090 | 12,277 | 7,609
Income tax expense | 1,529 | 404 | 2,929 | 1,483
Net income | 4,960 | 2,686 | 9,348 | 6,126
Earnings per share:
Basic | 0.35 | 0.19 | 0.66 | 0.44
Diluted | 0.34 | 0.18 | 0.65 | 0.42
Weighted average shares outstanding:
Basic | 14,175,312 | 14,018,629 | 14,184,951 | 14,008,385
Diluted | 14,464,461 | 14,553,282 | 14,436,339 | 14,528,789
(1) Share-based compensation expense in each category:
Cost of revenue (exclusive of depreciation and amortization) | 14 | - | 29 | -
Sales and marketing expenses | 147 | 193 | 375 | 388
General and administrative expenses | 2,075 | 1,634 | 3,882 | 3,035
Total | 2,236 | 1,827 | 4,286 | 3,423

RED VIOLET, INC.

CONDENSED CONSOLIDATED S TATEMENTS OF CASH FLOWS

(Amounts in thousands)

(unaudited)

Six Months Ended June 30,
2026 | 2025
CASH FLOWS FROM OPERATING ACTIVITIES:
Net income | 9,348 | 6,126
Adjustments to reconcile net income to net cash provided by operating activities:
Depreciation and amortization | 5,597 | 5,197
Share-based compensation expense | 4,286 | 3,423
Write-off of long-lived assets | 1 | 2
Provision for bad debts | 367 | 274
Noncash lease expenses | 259 | 257
Deferred income tax expense | 1,967 | 1,187
Changes in assets and liabilities:
Accounts receivable | (2,574 | (2,024
Prepaid expenses and other current assets | (78 | (510
Other noncurrent assets | 102 | (162
Accounts payable | (488 | (293
Accrued expenses and other current liabilities | (1,587 | (863
Deferred revenue | 167 | 94
Operating lease liabilities | (145 | (220
Net cash provided by operating activities | 17,222 | 12,488
CASH FLOWS FROM INVESTING ACTIVITIES:
Purchase of property and equipment | (168 | (252
Capitalized costs included in intangible assets | (6,803 | (4,984
Net cash used in investing activities | (6,971 | (5,236
CASH FLOWS FROM FINANCING ACTIVITIES:
Taxes paid related to net share settlement of vesting of restricted stock units | (714 | (727
Repurchases of common stock | (3,122 | -
Dividend payable | - | (4,181
Net cash used in financing activities | (3,836 | (4,908
Net increase in cash and cash equivalents | 6,415 | 2,344
Cash and cash equivalents at beginning of period | 43,557 | 36,504
Cash and cash equivalents at end of period | 49,972 | 38,848
SUPPLEMENTAL DISCLOSURE INFORMATION:
Cash paid for interest | - | -
Cash paid for income taxes | 531 | 681
Share-based compensation capitalized in intangible assets | 888 | 752
Retirement of treasury stock | 3,836 | 727
Right-of-use assets obtained in exchange of operating lease liabilities | - | 1,153

Use and Reconciliation of Non-GAAP Financial Measures

_[...truncated at ~12,000 chars of this document]_

## 8. MD&A — no 10-K Item 7 fetched, using 10-Q MD&A (10-Q_2026-08-10_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Red Violet, Inc., a Delaware corporation, is dedicated to making the world a safer place and reducing the cost of doing business. We build proprietary technologies and apply analytical capabilities to deliver identity intelligence. Our technology powers critical solutions, which empower organizations to operate with confidence. Our solutions enable the real-time identification and location of people, businesses, assets, and their interrelationships. These solutions are used for purposes including identity verification, risk mitigation, due diligence, fraud detection and prevention, regulatory compliance, and customer acquisition. Our cloud-native, AI-embedded identity intelligence platform, CORE TM , is purpose-built for the enterprise, yet flexible enough for organizations of all sizes, bringing clarity to massive datasets by transforming data into intelligence. We drive workflow efficiency and enable organizations to make better data-driven decisions.

With artificial intelligence and machine learning embedded directly into CORE's architecture from inception, and integrated with extensive proprietary data assets and regulated workflows, the platform enables customers to uncover actionable insights, accelerate decision-making, and operate at enterprise scale with materially reduced manual effort and operating costs. These AI-driven capabilities support the streamlining of labor-intensive workflows through automated, intelligence-driven processes that materially enhance efficiency and outcomes across risk management, compliance, and investigative functions.

Organizations are challenged by the structure, volume, velocity, and disparity of data. Our platform and applications provide real-time analytics, transforming the way our customers interact with information by presenting connections and relevance of information otherwise unattainable, which drives actionable insights and better outcomes. Leveraging cloud-native proprietary technology and applying machine learning and advanced analytical capabilities, CORE provides essential solutions to public and private sector organizations through intuitive, easy-to-use analytical interfaces. With extensive data assets consisting of public record, proprietary, and publicly-available data, our differentiated information and innovative platform and solutions deliver identity intelligence – entities, relationships, affiliations, interactions, and events. Our solutions are used today to enable frictionless commerce, enhance safety, and mitigate fraud and the related financial losses across the markets we serve.

While our platform powers a vast array of solutions for our customers, we presently market our solutions primarily through two brands, IDI ™ and FOREWARN ® . IDI is a leading-edge, analytics and information solutions provider delivering actionable intelligence to an expansive and diverse set of industries in support of use cases such as the verification and authentication of consumer identities, due diligence, prevention of fraud and abuse, legislative compliance, and debt recovery. idiCORE ™ is IDI's flagship product. idiCORE is a next-generation, investigative solution used to address a variety of organizational challenges, including, but not limited to, due diligence, risk mitigation, identity authentication, and regulatory compliance, by financial services companies, insurance companies, healthcare companies, law enforcement and government, identity verification platforms, collections, law firms, retail, telecommunication companies, corporate security, and investigative firms. FOREWARN is an app-based solution currently tailored for the real estate industry, providing instant knowledge prior to face-to-face engagement with a consumer, helping professionals identify and mitigate risk. As of June 30, 2026 and 2025, IDI had 10,869 and 9,549 billable customers, respectively, and FOREWARN had 443,173 and 346,671 users, respectively. We define a billable customer of IDI as a single entity that generated revenue during the last three months of the period. Billable customers are typically corporate organizations. In most cases, corporate organizations will have multiple users and/or departments purchasing our solutions; however, we count the entire organization as a discrete customer. We define a user of FOREWARN as a unique person that has a subscription to use the FOREWARN service as of the last day of the period. A unique person can only have one user account.

We generate substantially all of our revenue from licensing our solutions. Customers access our solutions through a hosted environment using an online interface, batch processing, API, and custom integrations. We recognize revenue from licensing fees (a) on a transactional basis determined by the customer's usage, (b) via a monthly fee or (c) from a combination of both. Revenue pursuant to pricing contracts containing a monthly fee is recognized ratably over the contract period. Pricing contracts are generally annual contracts or longer, with auto renewal. For each of the three months ended June 30, 2026 and 2025, 77% of total revenue was attributable to customers with pricing contracts, versus 23% attributable to transactional customers. For each of the six months ended June 30, 2026 and 2025, 76% of total revenue was attributable to customers with pricing contracts, versus 24% attributable to transactional customers.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Three months ended June 30, 2026 compared to three months ended June 30, 2025

Revenue

Revenue increased $4.9 million, or 23%, to $26.7 million for the three months ended June 30, 2026, compared to $21.8 million for the same period in 2025. The increase was driven by strong onboarding of new customers and volume expansion across the existing customer base.

•
Revenue from new customers increased $0.5 million, or 36%, to $2.0 million; and

•
Revenue from existing customers increased $4.4 million, or 22%, to $24.7 million.

Revenue from new customers represents total monthly revenue generated from customers during their first six full calendar months of revenue contribution. Revenue from existing customers represents total monthly revenue generated from customers beginning in their seventh full calendar month of revenue contribution.

As of June 30, 2026, our IDI billable customer base increased to 10,869 customers, up from 9,549 customers a year earlier. Our FOREWARN user base increased to 443,173 users, up from 346,671 users a year earlier.

Cost of revenue (exclusive of depreciation and amortization)

Cost of revenue (exclusive of depreciation and amortization) increased $0.3 million, or 9%, to $3.8 million for the three months ended June 30, 2026, compared to $3.5 million for the same period in 2025.

Our cost of revenue primarily consists of data acquisition costs, which include the cost to acquire data under flat-fee licensing agreements, including unlimited usage arrangements, as well as purchases on a transactional basis. We continue to enhance the breadth and depth of our data by the addition and expansion of relationships with key data suppliers, including our largest data supplier, which accounted for 46% of our total data acquisition costs for each of the three months ended June 30, 2026 and 2025. Effective on May 1, 2025, we entered into an amendment with our largest data supplier, extending the term of the agreement through April 30, 2031.

Additional components of our cost of revenue include cloud infrastructure fees, and pertinent personnel-related costs and share-based compensation expense.

Due to the fixed-cost nature of our primary data licensing structure, cost of revenue as a percentage of revenue decreased to 14% for the three months ended June 30, 2026, compared to 16% for the same period in 2025. We expect this percentage to continue to decline over time as our revenue increases.

Sales and marketing expenses

Sales and marketing expenses increased $0.2 million, or 2%, to $5.8 million for the three months ended June 30, 2026, compared to $5.6 million for the same period in 2025. We continued to invest in expanding our go-to-market capabilities to support long-term revenue growth.

Sales and marketing expenses include personnel-related expenses, advertising, marketing and agency expenses, travel expenses, and share-based compensation expense incurred by our sales team, and provision for bad debts.

For the three months ended June 30, 2026 and 2025, sales and marketing expenses consisted primarily of:

•
personnel-related expenses of $4.5 million and $4.5 million, respectively;

•
share-based compensation expense of $0.1 million and $0.2 million, respectively; and

•
advertising, marketing and agency expenses of $0.4 million and $0.3 million, respectively.

General and administrative expenses

General and administrative expenses increased $1.0 million, or 14%, to $8.3 million for the three months ended June 30, 2026, compared to $7.3 million for the same period in 2025. The increase reflects higher personnel-related expenses and share-based compensation expense to support the continued growth of the business.

For the three months ended June 30, 2026 and 2025, general and administrative expenses consisted primarily of:

•
personnel-related expenses of $4.1 million and $3.5 million, respectively;

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-04_item1_business.md)

Item 1. B usiness.

This business description should be read in conjunction with our audited consolidated financial statements and accompanying notes thereto appearing elsewhere in this Annual Report on Form 10-K for the year ended December 31, 2025 (the "2025 Form 10-K"), which are incorporated herein by this reference.

Company Overview

Red Violet, Inc. ("we," "us," "our," "red violet," or the "Company"), a Delaware corporation, is dedicated to making the world a safer place and reducing the cost of doing business. We build proprietary technologies and apply analytical capabilities to deliver identity intelligence. Our technology powers critical solutions, which empower organizations to operate with confidence. Our solutions enable the real-time identification and location of people, businesses, assets, and their interrelationships. These solutions are used for purposes including identity verification, risk mitigation, due diligence, fraud detection and prevention, regulatory compliance, and customer acquisition. Our cloud-native, AI-enabled identity intelligence platform, CORE TM , is purpose-built for the enterprise, yet flexible enough for organizations of all sizes, bringing clarity to massive datasets by transforming data into intelligence. We drive workflow efficiency and enable organizations to make better data-driven decisions.

With artificial intelligence and machine learning embedded directly into CORE's architecture from inception, and integrated with extensive proprietary data assets and regulated workflows, the platform enables customers to uncover actionable insights, accelerate decision-making, and operate at enterprise scale with materially reduced manual effort and operating costs. These AI-driven capabilities support the streamlining of labor-intensive workflows through automated, intelligence-driven processes that materially enhance efficiency and outcomes across risk management, compliance, and investigative functions.

Organizations are challenged by the structure, volume, velocity, and disparity of data. Our platform and applications provide real-time analytics, transforming the way our customers interact with information by presenting connections and relevance of information otherwise unattainable, which drives actionable insights and better outcomes. Leveraging cloud-native proprietary technology and applying machine learning and advanced analytical capabilities, CORE provides essential solutions to public and private sector organizations through intuitive, easy-to-use analytical interfaces. With extensive data assets consisting of public record, proprietary, and publicly-available data, our differentiated information and innovative platform and solutions deliver identity intelligence – entities, relationships, affiliations, interactions, and events. Our solutions are used today to enable frictionless commerce, enhance safety, and mitigate fraud and the related financial losses across the markets we serve.

While our platform powers a vast array of solutions for our customers, we presently market our solutions primarily through two brands, IDI ™ and FOREWARN ® . IDI is a leading-edge, analytics and information solutions provider delivering actionable intelligence to an expansive and diverse set of industries in support of use cases such as the verification and authentication of consumer identities, due diligence, prevention of fraud and abuse, legislative compliance, and debt recovery. idiCORE ™ is IDI's flagship product. idiCORE is a next-generation, investigative solution used to address a variety of organizational challenges, including, but not limited to, due diligence, risk mitigation, identity authentication, and regulatory compliance, by financial services companies, insurance companies, healthcare companies, law enforcement and government, identity verification platforms, collections, law firms, retail, telecommunication companies, corporate security, and investigative firms. FOREWARN is an app-based solution currently tailored for the real estate industry, providing instant knowledge prior to face-to-face engagement with a consumer, helping professionals identify and mitigate risk. As of December 31, 2025 and 2024, IDI had 10,022 and 8,926 billable customers, respectively, and FOREWARN had 390,018 and 303,418 users, respectively. We define a billable customer of IDI as a single entity that generated revenue during the last three months of the period. Billable customers are typically corporate organizations. In most cases, corporate organizations will have multiple users and/or departments purchasing our solutions, however, the Company counts the entire organization as a discrete customer. We define a user of FOREWARN as a unique person that has a subscription to use the FOREWARN service as of the last day of the period. A unique person can only have one user account.

We generate substantially all of our revenue from licensing our solutions. Customers access our solutions through a hosted environment using an online interface, batch processing, API and custom integrations. We recognize revenue from licensing fees (a) on a transactional basis determined by the customer's usage, (b) via a monthly fee or (c) from a combination of both. Revenue pursuant to pricing contracts containing a monthly fee is recognized ratably over the contract period. Pricing contracts are generally annual contracts or longer, with auto renewal. For the years ended December 31, 2025 and 2024, 76% and 77% of total revenue was attributable to customers with pricing contracts, respectively, versus 24% and 23% attributable to transactional customers, respectively.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-04_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | **MISSING** |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-04_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-11_2-02-results.md, 10-Q_2026-08-10_mdna.md (10-Q MD&A used in place of the 10-K), 10-K_2026-03-04_item1_business.md

**Missing:** 10-K Item 7 MD&A (substituted 10-Q MD&A), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
