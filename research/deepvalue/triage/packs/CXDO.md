# Triage pack — CXDO · Crexendo, Inc.

_Generated 2026-09-04 21:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CXDO · **Name:** Crexendo, Inc.
- **CIK:** 0001075736
- **SIC:** 4813 — Telephone Communications (No Radiotelephone)
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CXDO

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Crexendo, Inc.
- **CIK:** 1,075,736 · **SIC:** 4813 (Telephone Communications (No Radiotelephone)) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:SecuredLongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 5.92 |
| mktcap | $196.9M |
| ev | $183.0M |
| ev_ebit | 39.0x |
| fcf | $9.3M |
| fcf_yield | 4.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.8% |
| net_debt | -$13.9M |
| net_debt_ebit | -3.0x |
| cash | $18.3M |
| ltd | $4.4M |
| equity | $78.1M |
| ltd_tag | SecuredLongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $68.2M |
| revenue_prior | $60.8M |
| rev_growth | 12.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $4.7M |
| net_income | $5.1M |
| cfo | $9.3M |
| capex | $18k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 10.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 33,253,790 |
| shares_py | 30,169,531 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 5.8% |
| r6m | -14.0% |
| off_52w_high | -43.5% |
| adv20 | $1.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.48 |
| r_ev_ebit | 0.19 |
| r_roic | 0.55 |
| r_rev_growth | 0.70 |
| r_buyback | 0.12 |
| score | 0.46 |

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
| rank | 286 |

**Screen rationale:** net cash; 12-1 momentum 5.8%


## 3. Share count trend

- Shares outstanding: **33,253,790** (CY2026Q2I) vs **30,169,531** prior year (CY2025Q2I)
- Change: **10.2%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-30** — Item 5.02 (officer / director change or comp arrangement): On July 29, 2026, the Board of Directors of Crexendo, Inc. (the " Company ") appointed Chris Aaker as the Company's Chief Technology Officer, effective August 1, 2026.
- **2026-05-05** — Item 1.01 (Entry into a Material Definitive Agreement): On May 1, 2026, Crexendo, Inc. (the "Company") entered into a Credit Agreement with Wells Fargo Bank, National Association (the "Credit Agreement"), providing for a revolving line of credit in an aggregate principal amount up to $5,000,000 (the "Line of...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 25,000 sh / $162,500 -> net $-162,500 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 70 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| F | 23 |
| M | 46 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter Financial highlights:'; skipped 9 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - PRESS RELEASE (cxdo_ex991.htm)

Second Quarter Financial highlights:

· | Total revenue increased 49% year-over-year to $24.6 million
· | GAAP net income of $1.1 million, or $0.03 per basic and diluted common share.
· | Non-GAAP net income of $4.1 million, or $0.12 per basic and diluted common share.

Financial Results for the Second Quarter of 2026

Total Revenue: Consolidated total revenue for the second quarter of 2026 increased 49%, or $8.1 million, to $24.6 million compared to $16.6 million for the second quarter of 2025.

Service Revenue: Consolidated service revenue for the second quarter of 2026 increased 78%, or $6.5 million, to $14.9 million compared to $8.4 million for the second quarter of 2025.

Software Solutions Revenue: Consolidated software solutions revenue for the second quarter of 2026 increased 5%, or $0.4 million, to $7.3 million compared to $7.0 million for the second quarter of 2025.

Product Revenue: Consolidated product revenue for the second quarter of 2026 increased 104%, or $1.2 million, to $2.5 million compared to $1.2 million for the second quarter of 2025.

Operating Expenses: Consolidated operating expenses for the second quarter of 2026 increased 53%, or $8.1 million, to $23.6 million compared to $15.4 million for the second quarter of 2025.

Net Income/(Loss): The Company reported net income of $1.1 million for the second quarter of 2026, or $0.03 per basic and diluted common share, compared to net income of $1.2 million, or $0.04 per basic and diluted common share for the second quarter of 2025.

Non-GAAP: Non-GAAP net income of $4.1 million for the second quarter of 2026, or $0.12 per basic and diluted common share, compared to non-GAAP net income of $2.9 million or $0.10 per basic common share and $0.09 per diluted common share for the second quarter of 2025.

EBITDA and Adjusted EBITDA: EBITDA for the second quarter of 2026 of $3.0 million compared to $2.0 million for the second quarter of 2025. Adjusted EBITDA for the second quarter of 2026 of $4.1 million compared to $2.8 million for the second quarter of 2025.

Financial Results for the six months ended June 30, 2026

Total Revenue: Consolidated total revenue for the six months ended June 30, 2026 increased 39%, or $12.7 million, to $45.4 million compared to $32.6 million for the six months ended June 30, 2025.

Service Revenue: Consolidated service revenue for the six months ended June 30, 2026 increased 54%, or $8.9 million, to $25.4 million compared to $16.6 million for the six months ended June 30, 2025.

Software Solutions Revenue: Consolidated software solutions revenue for the six months ended June 30, 2026 increased 9%, or $1.2 million, to $15.1 million compared to $13.8 million for the six months ended June 30, 2025.

Product Revenue: Consolidated product revenue for the six months ended June 30, 2026 increased 121%, or $2.7 million, to $4.9 million compared to $2.2 million for the six months ended June 30, 2025.

Operating Expenses: Consolidated operating expenses for the six months ended June 30, 2026 increased 44%, or $13.5 million, to $43.9 million compared to $30.4 million for the six months ended June 30, 2025.

Net Income/(Loss): The Company reported net income of $1.6 million for the six months ended June 30, 2026, or $0.05 per basic and diluted common share, compared to net income of $2.4 million, or $0.08 per basic and diluted common share for the six months ended June 30, 2025.

Non-GAAP: Non-GAAP net income of $7.3 million for the six months ended June 30, 2026, or $0.23 per basic common share and $0.22 per diluted common share, compared to non-GAAP net income of $5.5 million or $0.19 per basic common share and $0.18 per diluted common share for the six months ended June 30, 2025.

EBITDA and Adjusted EBITDA: EBITDA for the six months ended June 30, 2026 of $4.6 million compared to $3.9 million for the six months ended June 30, 2025. Adjusted EBITDA for the six months ended June 30, 2026 of $7.3 million compared to $5.5 million for the six months ended June 30, 2025.

Cash and Cash Equivalents: Total cash and cash equivalents at June 30, 2026 was $18.3 million compared to $31.4 million at December 31, 2025.

Cash Flow: Cash provided by operating activities for the six months ended June 30, 2026 was $4.8 million compared to cash provided by operating activities of $2.5 million for the six months ended June 30, 2025. Cash used in investing activities for the six months ended June 30, 2026 was ($26.2) million compared to nill for the six months ended June 30, 2025. Cash provided by financing activities for the six months ended June 30, 2026 was $8.3 million compared to cash provided by financing activities of $2.7 million for the first six months of 2025.

Management Commentary

"Crexendo delivered another strong quarter, with total revenue increasing 49% year-over-year to $24.6 million and adjusted EBITDA increasing 46% to $4.1 million," said Jeff Korn, Crexendo Chief Executive Officer and Chairman of the Board. "I am particularly pleased and excited that we secured eleven new platform logos through the second quarter of 2026, compared with only two over the same period last year. This substantial increase reinforces our belief that the Crexendo NetSapiens platform is increasingly the platform of choice for providers seeking a new, improved and scalable communications platform. These wins should provide a meaningful recurring revenue opportunity as these customers convert more of their existing subscriber bases to our platform, expand their businesses and purchase additional licenses in the future. In addition, I could not be more pleased with the ESI acquisition and the contributions the ESI team is already making to Crexendo. The integration is progressing exceptionally well, the employees are engaged, sales are exceeding our initial expectations, and we are already realizing the benefits of combining our accounting, legal, marketing, and engineering capabilities. ESI has significantly improved our revenue, strengthened our customer base, and added an experienced team that shares our commitment to innovation and outstanding customer service. The acquisition is performing exactly as we had hoped and further validates our disciplined approach to identifying and integrating strategic, accretive acquisitions."

Korn added "I am also very pleased with our continued margin improvement and the substantial expansion in operating cash flow, with cash provided by operating activities increasing 89% to $4.8 million during the first six months of the year compared to the same period of the prior year. This increased cash generation strengthens our balance sheet and provides us with greater flexibility to pursue additional strategic M&A opportunities while seeking to minimize dilution to our shareholders. Our recently released AI offerings, while not yet meaningful contributors to revenue, continue to receive strong praise and market acceptance. I expect adoption to continue expanding and believe AI-related revenue can become meaningful in 2027. With accelerating platform momentum, a highly successful acquisition, improving margins and increasing cash generation, I remain extremely enthusiastic about our ability to deliver profitable growth and enhance long-term shareholder value."

Conference Call

Crexendo management will hold a conference call today, August 4, 2026, at 4:30 PM Eastern time to discuss these results. Company CEO Jeff Korn, CFO Ron Vincent, and President and COO Doug Gaylor will host the call, followed by a question-and-answer period.

Dial-in Numbers:

Domestic Participants: 888-506-0062

International Participants: 973-528-0011

Participant Access Code: 550804

Please dial in five minutes prior to the beginning of the call at 4:30 PM Eastern time and reference participant access code 550804 and the Crexendo earnings call. A replay of the call will be available until August 18, 2026, by dialing toll-free at 877-481-4010 or 919-882-2331 for international callers. The replay passcode is 54291.

About Crexendo

Crexendo, Inc. is an award-winning software technology company that is a premier provider of cloud communication platform and services, video collaboration and managed IT services tailored to businesses of all sizes. Our solutions currently support over seven million end users globally, through our extensive global network of over 240 cloud communication platform software subscribers and our direct retail offering.

CREXENDO, INC. AND SUBSIDIARIES

Condensed Consolidated Balance Sheets

(Unaudited, in thousands, except par value and share data)

June 30, 2026 | December 31, 2025
Assets
Current assets:
Cash and cash equivalents | 18,289 | 31,378
Trade receivables, net of allowance of $73 and $124, respectively | 6,187 | 4,913
Contract assets, net of allowance of $2 and $0, respectively | 114 | -
Inventories | 1,380 | 454
Equipment financing receivables, net of allowance of $75 and $50, respectively | 2,741 | 1,416
Contract costs | 4,156 | 2,318
Prepaid expenses | 1,663 | 892
Income tax receivable | 214 | 234
Other current assets | 58 | 292
Total current assets | 34,802 | 41,897
Contract assets, net of current portion, net of allowance of $139 and $145, respectively | 848 | 402
Long-term equipment financing receivables, net of allowance of $149 and $107, respectively | 5,351 | 3,223
Property and equipment, net | 376 | 195
Operating lease right-of-use assets | 751 | 1,006
Intangible assets, net | 38,302 | 17,860
Goodwill | 14,170 | 9,454
Contract costs, net of current portion | 6,077 | 3,319
Other long-term assets | 361 | 330
Total Assets | 101,038 | 77,686
Liabilities and Stockholders' Equity
Current liabilities:
Accounts payable | 1,384 | 649
Accrued expenses | 10,561 | 8,391
Finance leases | 1 | 2
Notes payable | 454 | 114
Operating lease liabilities | 511 | 493
Income tax payable | 148 | 151
Contract liabilities | 3,856 | 2,528
Total current liabilities | 16,915 | 12,328
Contract liabilities, net of current portion | 1,334 | 1,008
Notes payable, net of current portion | 4,407 | -
Operating lease liabilities, net of current portion | 269 | 529
Total liabilities | 22,925 | 13,865
Stockholders' equity:
Preferred stock, par value $0.001 per share - authorized 5,000,000 shares; none issued | — | —
Common stock, par value $0.001 per share - authorized 50,000,000 shares, 33,248,336 shares issued and outstanding as of June 30, 2026 and 31,004,327 shares issued and outstanding as of December 31, 2025 | 33 | 31
Additional paid-in capital | 158,000 | 145,325
Accumulated deficit | (80,090 | (81,719
Accumulated other comprehensive income | 170 | 184
Total stockholders' equity | 78,113 | 63,821
Total Liabilities and Stockholders' Equity | 101,038 | 77,686

CREXENDO, INC. AND SUBSIDIARIES

Condensed Consolidated Statements of Operations

(Unaudited, in thousands, except per share and share data)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-03_item7_mdna.md)

_Extraction: started at the Overview heading._

OVERVIEW

Crexendo, Inc. is an award-winning software technology company that is a premier provider of cloud communication platform and services, video collaboration and managed IT services tailored to businesses of all sizes. By providing a variety of comprehensive and scalable solutions, we are able to cater to businesses of all sizes on a monthly subscription basis without the need for expensive capital investments, regardless of where their business is in its lifecycle. Our products and services can be categorized in the following offerings:

Cloud Telecommunications Services – Our cloud telecommunications services transmit calls using IP or cloud technology, which converts voice signals into digital data packets for transmission over the Internet or cloud. Each of our calling plans provides a number of basic features typically offered by traditional telephone service providers, plus a wide range of enhanced features that we believe offer an attractive value proposition to our customers. This platform enables a user, via a single "identity" or telephone number, to access and utilize services and features regardless of how the user is connected to the Internet or cloud, whether it's from a desktop device or an application on a mobile device.

We generate recurring revenue from our cloud telecommunications services, broadband Internet services, managed IT services, software license sales, and infrastructure as a service. Our cloud telecommunications contracts typically have a thirty-nine to ninety-month term. We may also charge activation and flash fees and the Company generally allocates a portion of the activation fees to the desktop devices, which is recognized at the time of the installation or customer acceptance, and a portion to the service, which is recognized over the contract term using the straight-line method. We also charge other various contracted and non-contracted fees.

We generate product revenue, equipment financing revenue, and device as a service revenue from the sale and lease of our cloud telecommunications equipment. Revenues from the sale of equipment, including those from sales-type leases, are recognized at the time of sale or at the inception of the lease, as appropriate.

Our Cloud Telecommunications service revenue increased 6% or $1,933 to $33,782 for the year ended December 31, 2025 as compared to $31,849 for the year ended December 31, 2024. Our Cloud Telecommunications product revenue decreased 16% or $894 to $4,721 for the year ended December 31, 2025 as compared to $5,615 for the year ended December 31, 2024.

Software Solutions – Our software solutions segment derives revenues from three primary sources: software licenses, software maintenance support and professional services. Software and services may be sold separately or in bundled packages. Generally, contracts with customers contain multiple performance obligations, consisting of software and services. For bundled packages, the Company accounts for individual products and services separately if they are distinct – i.e. if a product or service is separately identifiable from other items in the bundled package and if a customer can benefit from it on its own or with other resources that are readily available to the customer. The consideration is allocated between separate products and services in a bundle based on their relative stand-alone selling prices. The stand-alone selling prices are determined based on the prices at which the Company separately sells the software licenses and professional services. For items that are not sold separately (e.g. additional features) the Company estimates stand-alone selling prices using the adjusted market assessment approach. When we provide a free trial period, we do not begin to recognize recurring revenue until the trial period has ended and the customer has been billed for the services.

We generate software license revenue from the sale of perpetual software licenses, term-based software licenses that expire, and Software-as-a-Service ("SaaS") based software which are referred to as subscription arrangements. The Company does not recognize software revenue related to the renewal of subscription software licenses earlier than the beginning of the subscription period.

We generate subscription and maintenance support revenue from customer support and other supportive services. The Company offers warranties on its products. The warranty period for our licensed software is generally 90 days. Certain of the Company's warranties are considered to be assurance-type in nature and do not cover anything beyond ensuring that the product is functioning as intended. Based on the guidance in ASC 606, assurance-type warranties do not represent separate performance obligations. The Company also sells separately-priced maintenance service contracts, which qualify as service-type warranties and represent separate performance obligations. The Company does not typically allow and has no history of accepting material product returns. Customer support includes software updates on a when-and-if-available basis, telephone support, integrated web-based support and bug fixes or patches. Subscription and maintenance support revenue is recognized ratably over the term of the customer support agreement, which is typically one year.

We generate professional services and other revenue from consulting, technical support, resident engineer services, design services and installation services. Revenue for professional services and other is recognized when the performance obligation is complete and the customer has accepted the performance obligation.

Our Software solutions revenue increased 27%, or $6,290 to $29,664 for the year ended December 31, 2025, compared to $23,374 for the year ended December 31, 2024.

Results of Consolidated Operations

The following discussion of financial condition and results of operations should be read in conjunction with the Consolidated Financial Statements and Notes thereto and other financial information included herein this Annual Report.

Results of Consolidated Operations (in thousands, except for per share amounts)

Year Ended December 31,
Consolidated | 2025 | 2024
Service revenue | 33,782 | 31,849
Software solutions revenue | 29,664 | 23,374
Product revenue | 4,721 | 5,615
Total revenue | 68,167 | 60,838
Income/(loss) before income tax | 5,371 | 1,889
Income tax (provision)/benefit | (300 | (212
Net income/(loss) | 5,071 | 1,677
Basic earnings per share | 0.17 | 0.06
Diluted earnings per share | 0.16 | 0.06

For the three months ended
Consolidated | March 31, | June 30, | September 30, | December 31,
2025 | 2025 | 2025 | 2025
Service revenue | 8,182 | 8,374 | 8,607 | 8,619
Software solutions revenue | 6,868 | 6,975 | 7,521 | 8,300
Product revenue | 1,007 | 1,203 | 1,369 | 1,142
Total revenue | 16,057 | 16,552 | 17,497 | 18,061
Income/(loss) before income tax | 1,215 | 1,280 | 1,493 | 1,383
Income tax (provision)/benefit | (44 | (48 | (43 | (165
Net income/(loss) | 1,171 | 1,232 | 1,450 | 1,218
Basic earnings per share (1) | 0.04 | 0.04 | 0.05 | 0.04
Diluted earnings per share (1) | 0.04 | 0.04 | 0.05 | 0.04

For the three months ended
Consolidated | March 31, | June 30, | September 30, | December 31,
2024 | 2024 | 2024 | 2024
Service revenue | 7,845 | 8,067 | 7,953 | 7,984
Software solutions revenue | 5,146 | 5,325 | 5,860 | 7,043
Product revenue | 1,295 | 1,293 | 1,814 | 1,213
Total revenue | 14,286 | 14,685 | 15,627 | 16,240
Income/(loss) before income tax | 461 | 615 | 194 | 619
Income tax (provision)/benefit | (27 | (27 | (46 | (112
Net income/(loss) | 434 | 588 | 148 | 507
Basic earnings per share (1) | 0.02 | 0.02 | 0.01 | 0.02
Diluted earnings per share (1) | 0.01 | 0.02 | 0.00 | 0.02

———————

(1) | Earnings per share is computed independently for each of the quarters presented. Therefore, the sums of quarterly earnings per share amounts do not necessarily equal the total for the twelve month periods presented.

Year Ended December 31, 2025 Compared to Year Ended December 31, 2024

Total Revenue

Total revenue consists of service revenue, software solutions revenue and product revenue. The following table reflects our total revenue for the year ended December 31, 2025, compared to the year ended December 31, 2024:

Year Ended December 31,
2025 | 2024 | Dollar Change | Percent Change
Total revenue | 68,167 | 60,838 | 7,329 | 12 | %

The increase in total revenue is due to an increase in software solutions revenue of $6,290 and an increase in service revenue of $1,933, offset by a decrease in product revenue of $894.

Income/(loss) Before Income Tax

The following table reflects our income/(loss) before income tax for the year ended December 31, 2025, compared to the year ended December 31, 2024:

Year Ended December 31,
2025 | 2024 | Dollar Change | Percent Change
Income/(loss) before income tax | 5,371 | 1,889 | 3,482 | 184 | %

The increase in income/(loss) before income tax is primarily related to an increase in revenue of $7,329 and an increase in other income/(expense) of $616, offset by an increase in operating expenses of $4,463. The increase in revenue is primarily related to organic growth from new and existing customers. The increase in operating expenses is primarily related to an increase in salaries, benefits, bonuses and share-based compensation of $1,267, an increase in commission expense of $986, an increase in contract labor and outsourced engineering services of $699, an increase in third-party telecommunication charges of $590, an increase in software costs of $415, an increase in hosting services fees of $295, an increase in annual user group meeting expenses of $169, and an increase in other expenses of $42. The increase in other income/(expense) is primarily related to an increase in interest income of $446, an increase in other income of $147, and a decrease in interest expense of $23.

Income Tax Benefit/(Provision)

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-03_item1_business.md)

ITEM 1. BUSINESS

OVERVIEW

Crexendo, Inc. is an award-winning software technology company that is a premier provider of cloud communication platform software and unified communications as a service (UCaaS) offering, including voice, video, contact center, and managed IT services tailored to businesses of all sizes. Our cloud communications software solutions currently support over seven million end users globally, through an extensive network of over 240 cloud communication platform software subscribers and our direct retail offering. Our products and services can be categorized in the following offerings:

Cloud Telecommunications Services – Our cloud telecommunications services transmit calls using IP or cloud technology, which converts voice signals into digital data packets for transmission over the Internet or cloud. Each of our calling plans provides a number of basic features typically offered by traditional telephone service providers, plus a wide range of enhanced features that we believe offer an attractive value proposition to our customers. This platform enables a user, via a single "identity" or telephone number, to access and utilize services and features regardless of how the user is connected to the Internet or cloud, whether it's from a desktop device or an application on a mobile device or computer.

We generate recurring revenue from our cloud telecommunications services, broadband Internet services, managed IT services, software license sales, and infrastructure as a service. Our cloud telecommunications contracts typically have a thirty-six to sixty-month term. We may also charge activation and flash fees and the Company generally allocates a portion of the activation fees to the desktop devices, which is recognized at the time of the installation or customer acceptance, and a portion to the service, which is recognized over the contract term using the straight-line method. We also charge other various contracted and non-contracted fees.

We generate product revenue, equipment financing revenue, and device as a service revenue from the sale and lease of our cloud telecommunications equipment. Revenues from the sale of equipment, including those from sales-type leases, are recognized at the time of sale or at the inception of the lease, as appropriate.

Software Solutions – Our software solutions segment derives revenues from three primary sources: software licenses, software maintenance support and professional services. Software and services may be sold separately or in bundled packages. Generally, contracts with customers contain multiple performance obligations, consisting of software and services. For bundled packages, the Company accounts for individual products and services separately if they are distinct – i.e. if a product or service is separately identifiable from other items in the bundled package and if a customer can benefit from it on its own or with other resources that are readily available to the customer. The consideration is allocated between separate products and services in a bundle based on their relative stand-alone selling prices. The stand-alone selling prices are determined based on the prices at which the Company separately sells the software licenses and professional services. For items that are not sold separately (e.g. additional features) the Company estimates stand-alone selling prices using the adjusted market assessment approach. When we provide a free trial period, we do not begin to recognize recurring revenue until the trial period has ended and the customer has been billed for the services.

We generate software license revenue from the sale of perpetual software licenses, term-based software licenses that expire, and Software-as-a-Service ("SaaS") based software which are referred to as subscription arrangements. The Company does not recognize software revenue related to the renewal of subscription software licenses earlier than the beginning of the subscription period.

We generate subscription and maintenance support revenue from customer support and other supportive services. The Company offers warranties on its products. The warranty period for our licensed software is generally 90 days. Certain of the Company's warranties are considered to be assurance-type in nature and do not cover anything beyond ensuring that the product is functioning as intended. Based on the guidance in ASC 606, assurance-type warranties do not represent separate performance obligations. The Company also sells separately-priced maintenance service contracts, which qualify as service-type warranties and represent separate performance obligations. The Company does not typically allow and has no history of accepting material product returns. Customer support includes software updates on a when-and-if-available basis, telephone support, integrated web-based support and bug fixes or patches. Subscription and maintenance support revenue is recognized ratably over the term of the customer support agreement, which is typically one to three years.

We generate professional services and other revenue from consulting, technical support, resident engineer services, design services and installation services. Revenue for professional services and other is recognized when the performance obligation is complete and the customer has accepted the performance obligation.

OUR SERVICES AND PRODUCTS

Our solution was recently recognized as the fastest growing UCaaS platform in the United States. By providing a variety of comprehensive and scalable solutions, we are able to cater to businesses of all sizes on a monthly subscription basis without the need for expensive capital investments, regardless of where their business is in its lifecycle. Our products and services can be categorized in the following offerings:

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-03_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-03_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-03_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-03-03_item7_mdna.md, 10-K_2026-03-03_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
