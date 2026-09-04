# Triage pack — VRRM · VERRA MOBILITY Corp

_Generated 2026-09-04 13:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** VRRM · **Name:** VERRA MOBILITY Corp
- **CIK:** 0001682745
- **SIC:** 4700 — Transportation Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/VRRM

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** VERRA MOBILITY Corp
- **CIK:** 1,682,745 · **SIC:** 4700 (Transportation Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income exceeds revenue.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 4.20 |
| mktcap | $638.0M |
| ev | $1.6B |
| ev_ebit | 6.8x |
| fcf | $136.7M |
| fcf_yield | 21.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 15.7% |
| net_debt | $975.1M |
| net_debt_ebit | 4.1x |
| cash | $49.6M |
| ltd | $1.0B |
| equity | $223.6M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $133.0M |
| revenue_prior | $116.0M |
| rev_growth | 14.6% |
| rev_growth_note | n/a |
| eq_flag | net income exceeds revenue |
| ebit | $238.4M |
| net_income | $136.6M |
| cfo | $255.8M |
| capex | $119.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -4.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 151,906,653 |
| shares_py | 159,540,820 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -77.1% |
| r6m | -74.5% |
| off_52w_high | -83.2% |
| adv20 | $14.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.89 |
| r_ev_ebit | 0.88 |
| r_roic | 0.82 |
| r_rev_growth | 0.76 |
| r_buyback | 0.87 |
| score | 0.75 |

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
| rank | 35 |

**Screen rationale:** top-quartile FCF yield 21.4%; cheap at 6.8x EV/EBIT; high ROIC 15.7%; revenue +14.6%; buying back stock -4.8%; EARNINGS QUALITY: net income exceeds revenue — one-off items likely; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **151,906,653** (CY2026Q2I) vs **159,540,820** prior year (CY2025Q2I)
- Change: **-4.8%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-17** — Item 5.02 (officer / director change or comp arrangement): On June 13, 2026, the Compensation Committee (the "Compensation Committee") of the Board of Directors (the "Board") of Verra Mobility Corporation (the "Company") approved the grant of an equity award to Stacey Moser, who has been named the Company's Chief...
- **2026-06-15** — Item 5.02 (officer / director change or comp arrangement): On June 9, 2026, Verra Mobility Corporation (the "Company") determined that Jonathan Baldwin, Executive Vice President, Government Solutions, will depart from the Company on July 9, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 29 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 10 |
| F | 3 |
| M | 16 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Financial Highlights'; skipped 27 forward-looking-statement block(s); 14 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (vrrm-ex99_1.htm)

Second Quarter 2026 Financial Highlights

•
Revenue : Total revenue for the second quarter of 2026 was $263.6 million, an increase of 12% compared to $236.0 million for the second quarter of 2025. Service revenue growth was 10%, driven by 17% growth in our Government Solutions segment and 6% growth in our Commercial Services segment. Government Solutions service revenue growth was driven primarily by a $12.0 million increase in New York City revenues associated with new camera installations, net of pricing changes under the new contract. The remaining $5.1 million in growth is attributable to expansion in bus lane, speed and other services. The increase in Commercial Services revenue was due to increased product adoption and tolling activity compared to the prior year which contributed to a $4.1 million growth in rental car companies (" RACs ") tolling revenue, with the remainder primarily driven by higher violations processing. Parking Solutions service revenue increased by $0.2 million compared to the second quarter of 2025, as increased revenue from our software as a service (" SaaS ") product offerings was partially offset by decreases in subscription services and professional services revenue related to parking management solutions.

•
Net (loss) income and Diluted Earnings Per Share ("EPS") : Net loss for the second quarter of 2026 was $(48.2) million, or $(0.32) per share, based on 151.9 million diluted weighted average shares outstanding.

Exhibit 99.1

Net income for the comparable 2025 period was $38.6 million, or $0.24 per share, based on 161.5 million diluted weighted average shares outstanding. The decrease in net income for the second quarter of 2026 was primarily due to impairments on goodwill and intangible assets recorded for the three months ended June 30, 2026 and an increase in operating expenses, partially offset by margins on product sales and installation services and a decrease in selling, general and administrative expenses.

•
Adjusted EPS* : Adjusted EPS for the second quarter of 2026 was $0.38 per share compared to $0.34 per share for the second quarter of 2025.

•
Adjusted EBITDA* : Adjusted EBITDA was $110.7 million for the second quarter of 2026 compared to $105.3 million for the same period in 2025. Adjusted EBITDA Margin* was 42% and 45% of total revenue for the 2026 and 2025 periods, respectively.

•
Net Cash Provided from Operations : Cash provided by operating activities decreased by $18.7 million from $75.1 million for the three months ended June 30, 2025 to $56.4 million for the three months ended June 30, 2026. Net (loss) income quarter-over-quarter decreased by $86.8 million, from $38.6 million in 2025 to $(48.2) million in 2026. The aggregate adjustments to reconcile net (loss) income to net cash provided by operating activities increased $94.3 million mainly due to the impairments on goodwill and intangible assets recorded for the current period, a prior period uncertain tax position reserve release and the mark-to-market adjustment on the share-based proceeds, partially offset by decreases in stock-based compensation, deferred income taxes and credit loss expense. The aggregate changes in operating assets and liabilities decreased by $26.3 million in 2026 compared to the prior year period and were primarily due to an increase in the net use of working capital, of which the majority was attributable to an increase in accounts receivable, unbilled receivables and inventory, partially offset by an increase in accounts payable.

•
Free Cash Flow* : Free Cash Flow was $32.6 million for the second quarter of 2026 compared to $40.3 million for the prior year period. The decline in Free Cash Flow is attributable to the items impacting cash provided by operating activities (as discussed above), partially offset by a reduction in capital expenditures.

*Non-GAAP measure; refer to "Non-GAAP Financial Measures" further below for explanatory notes and a reconciliation to the most directly comparable GAAP measure.

We report our results of operations based on three operating segments:

•
Commercial Services offers automated toll and violations management and title and registration solutions to rental car companies, fleet management companies and other large fleet owners.

•
Government Solutions delivers automated safety solutions to municipalities, school districts and government agencies, including services and technology that enable photo enforcement cameras to detect and process traffic violations related to speed, red-light, school bus and city bus lane management.

•
Parking Solutions provides an integrated suite of parking software, transaction processing and hardware solutions to universities, municipalities, parking operators, healthcare facilities and transportation hubs in the United States and Canada.

Second Quarter 2026 Segment Detail

•
The Commercial Services segment generated total revenue of $115.1 million, a 6% increase compared to $109.1 million in the same period in 2025. Segment profit was $77.2 million, a 7% increase from $72.0 million in the prior year period. The increases in revenue and segment profit compared to the prior year period resulted from increased product adoption and tolling activity compared to the prior year which contributed to a $4.1 million growth in RAC tolling revenue, with the remainder primarily driven by higher violations

Exhibit 99.1

processing. The segment profit margin was 67% for the second quarter of 2026 and 66% for the second quarter of 2025. Second quarter 2026 segment profit margins benefitted from lower credit loss expense.

•
The Government Solutions segment generated total revenue of $128.5 million, a 20% increase compared to $107.1 million in the same period in 2025. The increase was due to a 17% increase in service revenue over the prior year period, primarily driven by a $12.0 million increase in New York City revenues associated with new camera installations, net of pricing changes under the new contract. The remaining $5.1 million in growth was attributable to an expansion in bus lane and speed camera-related revenue and other services. In addition, product revenue increased approximately $4.3 million from the prior year period. The segment profit was $31.2 million in 2026 compared to $30.1 million in the prior year period with segment profit margins of 24% for 2026 and 28% for 2025. The decline in segment profit margins compared to the prior year period was primarily driven by increased costs to support project implementations and the pricing change under the New York City contract.

•
The Parking Solutions segment generated total revenue of $20.0 million, a 1% increase compared to $19.9 million in the same period in 2025, which was due primarily to an increase in SaaS product offerings, partially offset by decreases in subscription services and professional services revenue related to parking management solutions compared to the prior year period. The segment profit was $2.3 million compared to $3.2 million in the prior year period with segment profit margins of 11% for 2026 and 16% for 2025.

Liquidity and Debt : As of June 30, 2026, cash and cash equivalents were $49.6 million and total debt, net was $1,035 million. Net cash provided by operating activities was $56.4 million for the three months ended June 30, 2026, and $97.2 million for the six months ended June 30, 2026.

Net Debt and Net Leverage* : As of June 30, 2026, Net Debt was $993.2 million and Net Leverage was 2.4x, as compared to $971.8 million and 2.3x as of December 31, 2025.

*Non-GAAP measure; refer to "Non-GAAP Financial Measures" further below for explanatory notes and a reconciliation to the most directly comparable GAAP measure.

Change in Executive Leadership and Organizational Realignment

On June 1, 2026, we announced that David Roberts had departed as our President and Chief Executive Officer and as a member of our Board of Directors. The Board appointed Jon Keyser, previously our Chief Transformation Officer and Executive Vice President and Chief Legal Officer, as Interim President and Chief Executive Officer and retained an executive search firm to assist with a comprehensive search for a permanent successor.

On June 17, 2026, we announced organizational changes intended to accelerate our transformation initiatives, strengthen customer focus and create a more agile and efficient operating model. These changes are intended to build upon a hybrid operating model that centralizes key functions, including Human Resources, Finance, Legal, Government Relations, Engineering and Product Management. Stacey Moser was appointed Chief Customer Officer with responsibility for sales, account management and marketing across our Commercial Services and Government Solutions businesses. We are evaluating the effect of these organizational and internal management reporting changes on our operating and reportable segments.

Commercial Services Customer Contracts

We announced that one of our three significant Commercial Services customers had issued a notice terminating its contract with us; that customer subsequently withdrew and rescinded the notice and instead entered into a seven-year contract extension on terms materially less favorable to us than the prior agreement, including an option for the customer to modulate its fleet volume. A second significant Commercial Services customer entered into a five-year extension, with options to extend, also on materially less favorable terms and with fleet volume modulation rights.

Fluctuations in fleet volume under these arrangements could cause our revenue, results of operations, and cash flows to vary from period to period and could have a material adverse effect on our business, financial condition,

Exhibit 99.1

and results of operations. Additionally, any future termination of either extended contract could have a material adverse effect on our business, financial condition, and results of operations.

Goodwill and Intangible Assets Impairments

We recorded a $64.0 million impairment to goodwill in our Parking Solutions segment during the six months ended June 30, 2026, which is presented in a separate line item on the consolidated statements of operations. This was in connection with our 2026 assessment of goodwill impairment which determined that the Parking Solutions reporting unit carrying value exceeded the estimated fair value. As part of this assessment, we determined that the carrying value of certain intangibles within the Parking Solutions segment were not recoverable and recorded a $40.4 million impairment to intangibles in our Parking Solutions segment during the six months ended June 30, 2026, which is presented in a separate line item on the consolidated statements of operations.

2026 Full Year Guidance

Time: 5:00 p.m. Eastern Time

To access this conference call by telephone, register here to receive dial-in numbers and a unique PIN to join the call.

Webcast Information: Available live in the "Investor Relations" section of our website at http://ir.verramobility.com.

A replay of the call will also be made available on the Investor Relations website. A copy of the earnings call presentation will be available on the Investor Relations section of our website.

About Verra Mobility

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-24_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a leading provider of smart mobility technology solutions, principally operating throughout the United States, Australia, Europe, and Canada. We make transportation safer, smarter, and more connected through our integrated, data-driven solutions, including toll and violations management, title and registration services, automated safety and traffic enforcement, and commercial parking management. We bring together vehicles, hardware, software, data, and people to solve transportation challenges for customers around the world, including commercial fleet owners such as RACs, Direct Fleets, and FMCs, as well as governments, universities, parking operators, healthcare facilities, transportation hubs, and violation-issuing authorities. Our vision is to continue to develop and use technology and data intelligence to make transportation safer, smarter, and more connected globally.

Our Segments

We have three operating and reportable segments, Commercial Services, Government Solutions, and Parking Solutions:

•
Our Commercial Services segment offers toll and violation management solutions and title and registration services for commercial fleet customers, including RACs and FMCs in North America. In Europe, we provide tolling and violations processing services.

•
Our Government Solutions segment offers photo enforcement automated safety solutions and services to states, municipalities, counties, school districts, and law enforcement agencies of all sizes, primarily in the United States, Canada, and Australia. We provide complete, end-to-end speed, red-light, school bus stop arm, and city bus lane enforcement solutions. Our international operations primarily involve the sale of traffic enforcement products and recurring maintenance services related to the equipment and software.

•
Our Parking Solutions segment provides an integrated suite of parking software, transaction processing, and hardware solutions to universities, municipalities, commercial parking operators, and health care facilities in the United States and Canada.

Segment performance is based on revenues and income from operations before depreciation, amortization, and stock-based compensation. The measure also excludes interest expense, net, income taxes, and certain other transactions and is inclusive of other income, net.

Executive Summary

We operate under long-term contracts and a reoccurring service revenue model. We continue to execute our strategy to grow revenue organically year over year and focus on initiatives that support our long-term strategy. During the periods presented, we:

•
Increased total revenue by $99.9 million, or 11.4%, from $879.2 million in fiscal year 2024 to $979.1 million in fiscal year 2025. The increase was mainly due to service revenue resulting from increased product adoption, tolling activity, and activity in our European operations in the Commercial Services segment, and installation revenue from the NYCDOT program, the growth from city bus lane and school bus stop arm enforcement programs, back-office software-as-a-service (" SaaS ") programs and higher product sales in the Government Solutions segment.

•
Generated cash flows from operating activities of $255.8 million and $223.6 million for fiscal years 2025 and 2024, respectively. Our cash on hand was $65.3 million as of December 31, 2025.

•
Used existing cash on hand of $133.4 million during fiscal year 2025 to repurchase approximately 6.0 million shares authorized under a 2025 share repurchase program.

•
Continued to focus on debt management and lowering our exposure to higher interest rates, and as a result, we refinanced our debt during fiscal year 2025 which reduced our interest rate by 25 basis points. In addition, we made early repayments of approximately $8.5 million and $9.0 million on our Amended Term Loan and 2021 Term Loan (defined below) during fiscal year 2025 and 2024, respectively.

Recent Events

NYCDOT Red-Light Camera Expansion

In March 2025, NYCDOT instructed us through a change order to our then existing contract with NYCDOT to install additional red-light cameras by year-end 2025 as part of a legislatively authorized expansion. We installed 300 red-light cameras during the third and fourth quarters of 2025, which contributed approximately $38.4 million of revenue in fiscal year 2025, of which approximately $23.9 million was installation services revenue and approximately $14.5 million was product revenue.

NYCDOT Contract Renewal

Our contract with NYCDOT expired on December 31, 2025, and we entered into a new contract with NYCDOT, effective January 1, 2026, to manage New York City's automated enforcement camera safety program for a five-year period, with an option for the parties to extend for an additional five-year term. The total contract value for the new NYCDOT contract is $998 million. The terms of the new contract are materially different than our prior contract with NYCDOT, including service level agreements, service credits, liquidated damages, cybersecurity, and subcontracting requirements. See also " Our Commercial Services and Government Solutions segments have several large customers, including NYCDOT, that account for a significant portion of our revenue, and a reduction in demand, materially different terms or pricing in new or amended agreements, or loss of one or more of such customers could have a material adverse effect on our business. " in Item 1A, "Risk Factors."

Refinancing

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Fiscal Year 2025 Compared to Fiscal Year 2024

The following table sets forth our statements of operations data and expresses each item as a percentage of total revenue for the periods presented as well as the changes between periods. The tables and information provided in this section were derived from exact numbers and may have immaterial rounding differences.

Year Ended December 31,
Percentage of Revenue | Increase (Decrease) 2025 vs 2024
($ in thousands) | 2025 | 2024 | 2025 | 2024 | %
Service revenue | 918,137 | 841,676 | 93.8 | % | 95.7 | % | 76,461 | 9.1 | %
Product sales | 60,942 | 37,531 | 6.2 | % | 4.3 | % | 23,411 | 62.4 | %
Total revenue | 979,079 | 879,207 | 100.0 | % | 100.0 | % | 99,872 | 11.4 | %
Cost of service revenue, excluding depreciation and amortization | 30,318 | 18,988 | 3.1 | % | 2.2 | % | 11,330 | 59.7 | %
Cost of product sales | 45,517 | 27,058 | 4.6 | % | 3.1 | % | 18,459 | 68.2 | %
Operating expenses | 333,241 | 295,937 | 34.0 | % | 33.7 | % | 37,304 | 12.6 | %
Selling, general and administrative expenses | 215,274 | 195,054 | 22.0 | % | 22.2 | % | 20,220 | 10.4 | %
Depreciation, amortization and (gain) loss on disposal of assets, net | 116,315 | 109,072 | 11.9 | % | 12.3 | % | 7,243 | 6.6 | %
Goodwill impairment | — | 97,076 | 0.0 | % | 11.0 | % | (97,076 | (100.0 | )%
Total costs and expenses | 740,665 | 743,185 | 75.6 | % | 84.5 | % | (2,520 | (0.3 | )%
Income from operations | 238,414 | 136,022 | 24.4 | % | 15.5 | % | 102,392 | 75.3 | %
Interest expense, net | 64,618 | 73,902 | 6.6 | % | 8.4 | % | (9,284 | (12.6 | )%
Tax receivable agreement liability adjustment | 687 | (257 | 0.1 | % | (0.0 | )% | 944 | (367.3 | )%
Loss on interest rate swap | — | 494 | 0.0 | % | 0.1 | % | (494 | (100.0 | )%
Loss on extinguishment of debt | 1,335 | 1,745 | 0.1 | % | 0.2 | % | (410 | (23.5 | )%
Other income, net | (23,208 | (18,970 | (2.4 | )% | (2.2 | )% | (4,238 | 22.3 | %
Total other expenses | 43,432 | 56,914 | 4.4 | % | 6.5 | % | (13,482 | (23.7 | )%
Income before income taxes | 194,982 | 79,108 | 20.0 | % | 9.0 | % | 115,874 | 146.5 | %
Income tax provision | 58,349 | 47,660 | 6.0 | % | 5.4 | % | 10,689 | 22.4 | %
Net income | 136,633 | 31,448 | 14.0 | % | 3.6 | % | 105,185 | 334.5 | %

Service Revenue . Service revenue increased by $76.5 million, or 9.1%, to $918.1 million for fiscal year 2025 from $841.7 million in fiscal year 2024, representing 93.8% and 95.7% of total revenue, respectively. The following table depicts service revenue by segment:

Year Ended December 31,
Percentage of Revenue | Increase (Decrease) 2025 vs 2024
($ in thousands) | 2025 | 2024 | 2025 | 2024 | %
Service revenue
Commercial Services | 435,791 | 407,680 | 44.5 | % | 46.4 | % | 28,111 | 6.9 | %
Government Solutions | 415,637 | 367,914 | 42.5 | % | 41.8 | % | 47,723 | 13.0 | %
Parking Solutions | 66,709 | 66,082 | 6.8 | % | 7.5 | % | 627 | 0.9 | %
Total service revenue | 918,137 | 841,676 | 93.8 | % | 95.7 | % | 76,461 | 9.1 | %

Commercial Services service revenue increased by $28.1 million, or 6.9%, from $407.7 million in fiscal year 2024 to $435.8 million in fiscal year 2025. This increase was primarily due to increased product adoption and tolling activity compared to the prior year. These factors contributed to a $22.5 million growth in RAC tolling revenue and the remaining increase was driven mainly by an increase of $4.9 million from European operations during the year ended December 31, 2025, compared to the prior year.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-24_item1_business.md)

Item 1. B usiness

Overview

We are a leading provider of smart mobility technology solutions, principally operating throughout the United States, Australia, Europe, and Canada. Our goal is to make transportation safer, smarter, and more connected through our integrated, data-driven solutions, including toll and violations management, title and registration services, automated safety and traffic enforcement, and commercial parking management. We bring together vehicles, hardware, software, data, and people to solve transportation challenges for customers around the world, including commercial fleet owners, such as rental car companies (" RACs "), direct commercial fleet owner-operators (" Direct Fleets ") and fleet management companies (" FMCs "), as well as governments, universities, parking operators, healthcare facilities, transportation hubs, and other violation-issuing authorities.

Segments

Our solutions are offered through three segments: (i) Commercial Services, (ii) Government Solutions, and (iii) Parking Solutions.

Commercial Services

Our Commercial Services segment generated approximately $435.8 million in revenue for 2025, or approximately 45% of our total revenue. Commercial Services provides automated toll and violations management and title and registration solutions to RACs, Direct Fleets, FMCs, and other large fleet owners primarily in North America. Our toll and violations management solutions facilitate timely payment of tolls and violations incurred by our customers' vehicles, accurate transfer of liability on our customers' behalf, and billing of, and collections from, individual drivers. We also manage regional toll transponder installation and vehicle association—a critical and highly complex process for RAC, Direct Fleet, and FMC customers—to ensure that transponders and corresponding toll transactions are associated with the correct vehicle.

We have long-standing relationships with, among others, the three largest RACs in the United States, Avis Budget Group, Enterprise Mobility, and The Hertz Corporation. We also have relationships with key European RACs and leading FMCs in the United States. Through our established relationships with more than 50 individual tolling authorities throughout the United States, we provide an automated and outsourced administrative solution for our customers while also providing convenience for vehicle drivers and benefits to tolling and issuing authorities. Toll management solutions accounted for approximately 39% of our 2025 total revenues.

Our violations management solution processes violations incurred by the drivers of RAC, Direct Fleet, and FMC vehicles by working with domestic violation-issuing authorities to pay fines on behalf of vehicle owners, for which we are able to bill individual drivers or transfer liability directly to vehicle drivers. Vehicle-issued violations include parking and photo enforcement violations. In Europe, we specialize in the identification, notification, and collection of unpaid traffic, parking, and public transport-related fees, charges, and penalties issued to foreign-registered vehicles and individuals on behalf of issuing authorities in 20 European countries, as of December 31, 2025. Violation management solutions accounted for approximately 4% of our 2025 total revenues.

Our title and registration solutions provide RAC, Direct Fleet, and FMC customers with an integrated, end-to-end solution for managing vehicle title, registration, and annual renewals. We provide automated title and registration solutions by working with individual departments of motor vehicles in 17 states, as of December 31, 2025. Title and registration solutions accounted for approximately 2% of our 2025 total revenues.

Government Solutions

Our Government Solutions segment generated approximately $460.7 million in revenue for 2025, or approximately 47% of our 2025 total revenue. Our Government Solutions segment provides photo enforcement automated safety solutions to states, municipalities, counties, school districts, and law enforcement agencies of all sizes, primarily in the United States, Canada, and Australia. These programs are designed to reduce traffic violations and resulting collisions, injuries, and fatalities. Our proprietary technologies are designed to provide government agencies with the information, data, and automated end-to-end administrative capabilities to enforce traffic violations through photo enforcement. We install, maintain, and manage hardware and software automated safety solutions to process event data, apply customer-specific rules, and connect traffic violations to responsible drivers or vehicle owners on behalf of our customers. We also offer an end-to-end solution, in which we automatically send captured events to our customer's designated enforcement agency, and, once a violation is confirmed, we manage citation mailing, billing, and other administrative tasks on behalf of the customer.

In the United States, we provide government agencies with road safety cameras to detect and process traffic violations for red-light, speed, school bus, and city bus lanes. For many international customers, we design, engineer, and maintain roadside photo enforcement technology, including both hardware and software, which is sold or licensed to government agencies and often maintained with maintenance contracts to support the technology. Service revenue from speed, red-light, school bus cameras, and city bus lane cameras typically have initial terms of three to five years with renewal options and accounted for approximately 42% of our 2025 total revenues. Product sales to customers are not recurring and are dependent on our customers' needs, and account for approximately 5% of total revenue for 2025.

Parking Solutions

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

- **CALL PERIOD: UNKNOWN** (call dated 2026-08-05)
- **Recency:** Call period could not be determined from the file; judge its recency from the source, not from the file name.
- **File:** transcript_2026-08-05.md
- **Type:** EARNINGS PRESS RELEASE ONLY, not the call — no Q&A, no unscripted management commentary. Do not attribute call quotes to this.
- **Source:** https://www.sec.gov/Archives/edgar/data/1682745/000119312526335111/vrrm-ex99_1.htm

Verra Mobility Announces Second Quarter 2026 Financial Results

•
Total revenue of $263.6 million
•
Net loss of $(48.2) million
•
Net cash provided from operations of $56.4 million
•
Entered into a seven-year contract extension with Avis Budget Group, Inc.
•
Entered into a five-year contract extension with Hertz
•
Revising fiscal year 2026 guidance

MESA, Ariz., August 5, 2026 /PRNewswire/ –
Verra Mobility Corporation (NASDAQ: VRRM), a leading provider of smart mobility technology solutions, announced today the financial results for the second quarter ended June 30, 2026.

"I am proud of what our team accomplished during the second quarter, delivering revenue and profitability above our internal expectations while continuing to execute well across the business," said Jon Keyser, Interim Chief Executive Officer of Verra Mobility. "During the quarter, we also retained two of our most important customer relationships by extending our long-standing agreements with Avis Budget Group and Hertz. These agreements, together with our selection by the City of Los Angeles to implement California's largest speed safety program, reflect the strength of our technology, our operational capabilities and the trust our customers place in Verra Mobility."

"This has been a transformative quarter for our company. On behalf of our leadership team, I want to sincerely thank our employees for embracing change, acting with urgency and re-centering our focus on customer success. Their commitment is helping build a more agile, customer-centric Verra Mobility and positions us for long-term value creation."
Second Quarter 2026 Financial Highlights
•
Revenue
: Total revenue for the second quarter of 2026 was $263.6 million, an increase of 12% compared to $236.0 million for the second quarter of 2025. Service revenue growth was 10%, driven by 17% growth in our Government Solutions segment and 6% growth in our Commercial Services segment. Government Solutions service revenue growth was driven primarily by a $12.0 million increase in New York City revenues associated with new camera installations, net of pricing changes under the new contract. The remaining $5.1 million in growth is attributable to expansion in bus lane, speed and other services. The increase in Commercial Services revenue was due to increased product adoption and tolling activity compared to the prior year which contributed to a $4.1 million growth in rental car companies (“
RACs
”) tolling revenue, with the remainder primarily driven by higher violations processing. Parking Solutions service revenue increased by $0.2 million compared to the second quarter of 2025, as increased revenue from our software as a service (“
SaaS
”) product offerings was partially offset by decreases in subscription services and professional services revenue related to parking management solutions.
•
Net (loss) income and Diluted Earnings Per Share (“EPS”)

_[...truncated at ~3,000 chars of this document]_

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-24_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-24_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-24_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-24_item7_mdna.md, 10-K_2026-02-24_item1_business.md, transcript_2026-08-05.md

**Missing:** current-period call material (Call period could not be determined from the file; judge its recency from the source, not from the file name.)

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
