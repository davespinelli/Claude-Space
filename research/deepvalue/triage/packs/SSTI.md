# Triage pack — SSTI · SOUNDTHINKING, INC.

_Generated 2026-09-05 01:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SSTI · **Name:** SOUNDTHINKING, INC.
- **CIK:** 0001351636
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SSTI

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** SOUNDTHINKING, INC.
- **CIK:** 1,351,636 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 6.08 |
| mktcap | $80.0M |
| ev | $73.6M |
| ev_ebit | n/a |
| fcf | $4.9M |
| fcf_yield | 6.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -11.7% |
| net_debt | -$6.4M |
| net_debt_ebit | n/a |
| cash | $6.4M |
| ltd | $0.00 |
| equity | $65.6M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $104.1M |
| revenue_prior | $102.0M |
| rev_growth | 2.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$8.7M |
| net_income | -$9.4M |
| cfo | $9.3M |
| capex | $4.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 13,163,790 |
| shares_py | 12,791,251 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -33.4% |
| r6m | -8.7% |
| off_52w_high | -52.8% |
| adv20 | $1.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.54 |
| r_ev_ebit | 0.00 |
| r_roic | 0.11 |
| r_rev_growth | 0.41 |
| r_buyback | 0.26 |
| score | 0.27 |

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
| rank | 432 |

**Screen rationale:** debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **13,163,790** (CY2026Q2I) vs **12,791,251** prior year (CY2025Q2I)
- Change: **2.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-03-10** — Item 5.02 (officer / director change or comp arrangement): On March 6, 2026, Nasim Golzadeh notified SoundThinking, Inc. (the "Company") of her resignation as the Company's Managing Director, TechnoLogic and Executive Vice President, Investigative Solutions and from all other positions she holds with the Company and...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 1,162 sh / $7,032 -> net $-7,032 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 10 |
| F | 2 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-14_2-02-results.md)

_Extraction: started at the first release heading, 'SoundThinking, Inc. Reports First Quarter 2026 Financial Results'; skipped 15 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ssti-ex99_1.htm)

SoundThinking, Inc. Reports First Quarter 2026 Financial Results

Revenues Decreased 15% to $24.2 Million, as Q1 2025 included Revenue of Approximately $3.5 million From Renewal of Two Delayed Contracts with the New York City Police Department

Company Reaffirms FY 2026 Revenue Guidance Range of $109.0 Million to $111.0 Million, Representing Approximately 6% Year-Over-Year Growth at the Midpoint, and Reaffirms FY 2026 Adjusted EBITDA Margin Guidance Range of 16% to 18%

Company Reaffirms Expectation for ARR 1 to Increase from $95.4 Million at the Beginning of 2026 to Approximately $110.0 Million at the Beginning of 2027

FREMONT, CA – May 14, 2026 – SoundThinking, Inc. (Nasdaq: SSTI), a leading public safety technology company, today reported financial results for the first quarter ended March 31, 2026.

First Quarter 2026 Financial and Operational Highlights

•
Revenues decreased 15% to $24.2 million, compared to $28.3 million for the same quarter of 2025.

•
Gross profit decreased 32% to $11.3 million (47% of revenues), compared to $16.6 million (59% of revenues) for the same quarter of 2025.

•
GAAP net loss totaled $7.0 million, compared to GAAP net loss of $1.5 million for the same quarter of 2025.

•
Adjusted EBITDA 1 totaled negative $0.1 million (0% of revenues), compared to $4.5 million (16% of revenues) for the same quarter of 2025.

•
Went "live" in one new city and one new customer.

1 See the section below titled "Non-GAAP Financial Measures and Key Business Metrics" for more information about Adjusted EBITDA and its reconciliation to GAAP net loss and more information about Annual Recurring Revenue (ARR).

Management Commentary

"Our first quarter results reflect the structural shape of our year and the deliberate investments we are making to position SoundThinking for durable, profitable growth," said President and CEO Ralph Clark. "Q1 is, by design, typically our most cost‑concentrated and lightest revenue quarter of the year, with deployments, renewals, and expansions building through the year. With approximately $4 million in annualized savings we are expecting from the workforce optimization we implemented in the first quarter, we have increased visibility of our full‑year framework and we expect meaningful operating leverage to emerge."

"We are encouraged by the momentum we are seeing across our public safety and commercial security offerings. Drone‑as‑first‑responder integrations are now live in 16 cities, we have launched SafetySmart ™ Field Agent — our AI‑powered user experience for the SafetySmart ™ platform — and SafePointe ® go‑lives in healthcare are accelerating, with monthly recurring revenue more than doubling during the quarter. Supported by a strong recurring revenue base, a growing multi‑product pipeline, and improving visibility as the year progresses, we remain confident in our ability to execute and drive sustainable, long‑term value for shareholders."

First Quarter 2026 Financial Results

Revenues for the first quarter of 2026 were $24.2 million, compared to $28.3 million for the same quarter of 2025. The decrease in revenues was primarily due to approximately $3.5 million in catch-up revenue in 2025 from the renewal of two delayed contracts with the New York City Police Department and $0.5 million in revenue related to our ShotSpotter contract with Puerto Rico in the first quarter of 2025, which has not currently been renewed.

Gross profit for the first quarter of 2026 was $11.3 million (47% of revenues), compared to $16.6 million (59% of revenues) for the same period in 2025 reflecting lower revenue volume and continued cost pressures related to servicing contracted customers without the benefit of catch-up revenue recognized in the first quarter of 2025.

Total operating expenses for the first quarter of 2026 were $18.1 million, compared to $17.8 million for the same period in 2025. Operating expenses remained consistent with the prior year due to higher employee-related compensation and restructuring charges, partially offset by reduced sales and marketing expenses.

Net loss for the first quarter of 2026 totaled $7.0 million or $(0.54) per basic and diluted share (based on 12.9 million basic and diluted weighted-average shares outstanding), compared to net loss of $1.5 million or $(0.12) per basic and diluted share (based on 12.6 million basic and diluted weighted-average shares outstanding), for the same period in 2025.

Adjusted EBITDA for the first quarter of 2026 totaled negative $0.1 million, compared to $4.5 million in the same period last year.

At quarter end, the company had $14.2 million in cash and cash equivalents, $21.9 million in accounts receivable and contract assets, net, $40.4 million in deferred revenue, $4.0 million in debt and approximately $36.0 million available on its credit facility.

Financial Outlook

The company reaffirmed its full-year 2026 revenue guidance range of $109.0 million to $111.0 million, representing approximately 6% year-over-year growth at the midpoint. The company reaffirmed its Adjusted EBITDA margin guidance range of 16% to 18% for the full year 2026. The company also reaffirmed its expectation for ARR to increase from $95.4 million at the beginning of 2026 to approximately $110.0 million at the start of 2027.

"We are reaffirming our full‑year outlook and believe we are well positioned to deliver improved performance as we move through 2026, even without a ShotSpotter contract renewal in Chicago," added Mr. Clark. "We await the outcome of the current gunshot detection RFP process that remains underway, and believe our submission represents a comprehensive and compelling proposal. Our long-term financial targets of 70% gross margin and 40% Adjusted EBITDA margin do not include Chicago, as we remain confident in the enduring success of ShotSpotter and accelerating adoption of our broader SafetySmart platform."

SoundThinking believes Adjusted EBITDA also provides useful information to investors and others in understanding and evaluating its operating results in the same manner as its management and board of directors. For example, SoundThinking adjusts EBITDA for stock-based compensation expense because such expenses often vary for reasons that are generally unrelated to financial and operational performance in a particular period. Stock-based compensation is utilized by SoundThinking to attract and retain employees with a goal of long-term retention and the alignment of employee interests with those of the company and its stockholders, rather than to address operational performance for any particular period's financial performance measures, in particular net loss, or its other GAAP financial results.

The following table presents a reconciliation of GAAP net loss, the most directly comparable GAAP measure, to Adjusted EBITDA for each of the periods indicated (in thousands):

Three Months Ended March 31,
2026 | 2025
(Unaudited)
GAAP net loss | (7,005 | (1,484
Less:
Interest expense, net | (24 | 12
Income taxes | 29 | 100
Depreciation, amortization and impairment | 2,840 | 2,507
Stock-based compensation expense | 2,479 | 3,404
Restructuring and related expense | 1,586 | —
Adjusted EBITDA | (95 | 4,539

Annual Recurring Revenue (ARR): ARR is calculated for a year based on the expected GAAP revenue for the year from contracts that are in effect on January 1st of such year, assuming all such contracts that are due for renewal during the year renew as expected on or near their renewal date, and including contracts executed during the year after January 1st, but for which GAAP revenue recognition starts January 1st of the year. ARR is used by management internally to provide a clearer picture of its sustainable revenue base. SoundThinking believes ARR provides useful information to investors and others in understanding and evaluating growth of its recurring services because recurring revenue is particularly relevant for businesses operating under a subscription model, where customer retention and contract renewals play a significant role in long-term financial performance.

astewart@soundthinking.com

Investor Relations Contacts:

Ankit Hira

Solebury Strategic Communications for SoundThinking, Inc.

+1 (203) 546 0444

ahira@soleburystrat.com

SoundThinking, Inc.

Condensed Consolidated Statements of Operations

(In thousands, except share and per share data)

(Unaudited)

Three Months Ended March 31,
2026 | 2025
Revenues | 24,178 | 28,349
Costs
Cost of revenues | 12,483 | 11,718
Impairment of property and equipment | 435 | 37
Total costs | 12,918 | 11,755
Gross profit | 11,260 | 16,594
Operating expenses
Sales and marketing | 6,500 | 7,259
Research and development | 4,405 | 4,065
General and administrative | 6,676 | 6,474
Restructuring expense | 535 | -
Total operating expenses | 18,116 | 17,798
Operating loss | (6,856 | (1,204
Other expense, net
Interest expense, net | 24 | (12
Other expense, net | (144 | (168
Total other expense, net | (120 | (180
Loss before income taxes | (6,976 | (1,384
Provision for income taxes | 29 | 100
Net loss | (7,005 | (1,484
Net loss per share, basic and diluted | (0.54 | (0.12
Weighted-average shares used in computing net loss per share, basic and diluted | 12,857,891 | 12,648,370

SoundThinking, Inc.

Condensed Consolidated Balance Sheets

(In thousands)

(Unaudited)

March 31, | December 31,
2026 | 2025
Assets
Current assets
Cash and cash equivalents | 14,242 | 15,797
Accounts receivable and contract assets, net | 21,852 | 28,570
Prepaid expenses and other current assets | 4,138 | 4,225
Total current assets | 40,232 | 48,592
Property and equipment, net | 18,429 | 18,816
Operating lease right-of-use assets | 1,751 | 1,904
Goodwill | 34,213 | 34,213
Intangible assets, net | 28,376 | 29,335
Other assets | 2,724 | 2,894
Total assets | 125,725 | 135,754
Liabilities and Stockholders' Equity
Current liabilities
Accounts payable | 3,663 | 3,789
Accrued expenses and other current liabilities | 7,954 | 9,578
Line of credit | 4,000 | 4,000
Deferred revenue, short-term | 36,948 | 40,035
Total current liabilities | 52,565 | 57,402
Deferred revenue, long-term | 3,402 | 3,845
Deferred tax liability | 1,386 | 1,359
Operating lease liabilities, net of current portion | 764 | 976
Total liabilities | 58,117 | 63,582
Stockholders' equity
Common stock: $0.005 par value; 500,000,000 shares authorized; 12,953,943 and 12,825,960 shares issued and outstanding as of March 31, 2026 and December 31, 2025, respectively | 64 | 64
Additional paid-in capital | 188,600 | 186,115
Accumulated deficit | (120,723 | (113,718
Accumulated other comprehensive loss | (333 | (289
Total stockholders' equity | 67,608 | 72,172
Total liabilities and stockholders' equity | 125,725 | 135,754

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-30_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a leading public safety technology company that combines data-driven solutions and strategic advisory services for law enforcement, security teams and civic leadership. In April 2023, we changed the company name, ShotSpotter, Inc., to SoundThinking, Inc., reflecting our broader impact on public safety through a growing set of industry-leading law enforcement tools and community-focused solutions. As part of the rebranding, we introduced the SafetySmart TM platform that includes six data-driven tools consisting of: (i) our flagship product, ShotSpotter ® , our leading outdoor gunshot detection, location and alerting system trusted by 178 cities and 22 universities and corporations as of December 31, 2025; (ii) CrimeTracer TM , an agency-wide crime data and intelligence platform that enables investigators, analysts, patrol officers and command staff to search through more than one billion criminal justice records from across jurisdictions, leverage dashboards and AI-assisted tools to generate tactical leads, and quickly make intelligent connections to solve cases; (iii) CaseBuilder TM , a one-stop investigative case management system for tracking, reporting, and collaborating on cases; (iv) ResourceRouter TM , which directs the deployment of patrol and community anti-violence resources in an objective way to help maximize the impact of limited resources and improve community safety; (v) PlateRanger TM powered by Rekor ® , an ALPR and vehicle identification solution that leverages AI and machine learning to enhance investigative efficiency and provide real-time data sharing for law enforcement and (vi) SafePointe TM , an AI-based weapons detection system designed to provide discreet, high-throughput screening that complements physical security measures without compromising visitor experience. These solutions may operate independently or together as an integrated system that connects detection, data analysis, resource deployment and case management workflows. We also offer other security use-case specific solutions, including ShotSpotter for Campus and ShotSpotter for Corporate, which are typically smaller-scale deployments of ShotSpotter gunshot detection vertically marketed to universities, corporate campuses and key infrastructure centers to mitigate risk and enhance security by notifying authorities of outdoor gunfire incidents, saving critical minutes for first responders to arrive. In the first quarter of 2025, we rolled out a perimeter-based sniper gunshot detection solution targeting utility substations, with initial pilots aimed at utility customers, conducted through SoundThinking Labs. SoundThinking Labs supports innovative use cases of the Company's technology to help protect wildlife and the environment.

Our gunshot detection solutions consist of highly-specialized, cloud-based software integrated with proprietary, internet-enabled sensors designed to detect outdoor gunfire. The speed and accuracy of our gunfire alerts enable law enforcement and security personnel to consistently and quickly respond to shooting events including those unreported through 911, which can increase the chances of apprehending the shooter, providing timely aid to victims, and identifying witnesses before they scatter, as well as aid in evidence collection and serve as an overall deterrent. When a potential gunfire incident is detected by our sensors, our system precisely locates where the incident occurred and applies machine classification combined with human review to analyze and validate the incident. An alert containing a location on a map and critical information about the incident is sent directly to subscribing law enforcement or security personnel through any internet-connected computer and to iPhone or Android mobile devices.

Our software sends gunfire data along with the audio of the triggering sound to our Incident Review Center ("IRC"), where our trained incident review specialists are on duty 24 hours a day, seven days a week, 365 days a year to screen and confirm actual gunfire incidents. Our trained incident review specialists can supplement alerts with additional tactical information, such as the potential presence of multiple shooters or the use of high-capacity weapons. Gunshot incidents reviewed by our IRC result in alerts typically sent within approximately 45 seconds of the receipt of the gunfire incident.

We offer our solutions on a software-as-a-service subscription model to our customers. We generate annual subscription revenues from the deployment of ShotSpotter on a per-square-mile basis. Our security solutions, ShotSpotter for Campus and ShotSpotter for Corporate are typically sold on a subscription basis, each with a

customized deployment plan. Our ResourceRouter solution, CaseBuilder, PlateRanger and CrimeTracer are also sold on a subscription basis generally customized based on the number of sworn officers in a particular city. We generate annual subscription revenues from the deployment of SafePointe on a per-lane basis, a lane being the detection area between two lanes. As of December 31, 2025, we had ShotSpotter, ShotSpotter for Campus, and ShotSpotter for Corporate coverage areas under contract for over 1,092 square miles, of which over 1,064 square miles had gone live. Coverage areas under contract for ShotSpotter included 178 cities and coverage areas under contract for ShotSpotter for Campus and ShotSpotter for Corporate included 22 campuses/sites across the United States, South Africa, Brazil, Uruguay and the Bahamas, including some of the largest cities in the United States. As of December 31, 2025, we had 291 SafePointe lanes under contract. Most of our revenues are attributable to customers based in the United States.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth our consolidated statements of operations data for the years ended December 31, 2025 and 2024 (in thousands):

As a % of | As a % of | Change
2025 | Revenues | 2024 | Revenues | %
Revenues | 104,127 | 100 | % | 102,031 | 100 | % | 2,096 | 2 | %
Costs
Cost of revenues | 47,055 | 45 | % | 43,542 | 43 | % | 3,513 | 8 | %
Impairment of property and equipment | 434 | 1 | % | 605 | 1 | % | (171 | -28 | %
Total costs | 47,489 | 46 | % | 44,147 | 44 | % | 3,342 | 8 | %
Gross profit | 56,638 | 54 | % | 57,884 | 56 | % | (1,246 | -2 | %
Operating expenses:
Sales and marketing | 26,100 | 25 | % | 28,138 | 28 | % | (2,038 | -7 | %
Research and development | 15,866 | 16 | % | 13,925 | 14 | % | 1,941 | 14 | %
General and administrative | 23,207 | 22 | % | 23,894 | 23 | % | (687 | -3 | %
Change in fair value of contingent consideration | — | — | (554 | -1 | % | 554 | -100 | %
Restructuring expense | 197 | — | 336 | — | (139 | -41 | %
Total operating expenses | 65,370 | 63 | % | 65,739 | 64 | % | (369 | -1 | %
Operating loss | (8,732 | -9 | % | (7,855 | -8 | % | (877 | 11 | %
Other expense, net | (575 | — | (547 | — | (28 | -5 | %
Provision for income taxes | 113 | — | 778 | 1 | % | (665 | -85 | %
Net loss | (9,420 | -9 | % | (9,180 | -9 | % | (240 | 3 | %

Revenues

The increase of $2.1 million was primarily attributable to an $9.0 million increase in revenues from new customers and expansions of existing customer coverage areas, $3.7 million increase in revenue from New York City, $3.5 million of catch-up revenue from two three-year contract renewals with the New York City Police Department which were renewed in the first quarter of 2025 and $0.8 million increase from Puerto Rico, offset by a reduction in revenue due to non-renewal of contracts of $14.9 million of which $9.7 million was related to the City of Chicago. ShotSpotter went live in 10 new cities and 2 universities during the year ended December 31, 2025.

Costs

The increase in costs of $3.3 million was primarily due to an increase of $2.2 million in information technology ("IT") costs and $1.3 million in reimbursable product cost, offset by a reduction of $0.2 million in payroll and compensation related to headcount and other expense.

Gross Profit

Gross profit as a percentage of revenues decreased 2% compared to 2024.

Operating Expenses

Sales and Marketing Expense

Sales and marketing expense decreased by $2.0 million, primarily due to $1.7 million in commission expense related to brokerage services for the contract with the NYPD in 2024 without a corresponding service for the contract with the NYPD in 2025 and a decrease of $0.3 million in other sales and marketing expense.

Research and Development Expense

Research and development expense increased by $1.9 million, primarily due to an increase of $1.0 million in consulting expense associated with SafePointe and a $0.9 million increase in IT expense related to our investments in enhancing our AI capabilities.

General and Administrative Expense

General and administrative expense decreased by $0.7 million, primarily due to a decrease of $1.0 million in IT and facility expenses and a $0.3 million decrease in legal expense, offset by a $0.4 million increase in insurance and license fees and a $0.2 million increase in accounting and consulting fees related to our efforts to comply with the requirement to include an auditor attestation report on the effectiveness of our internal control over financial reporting in our annual report on Form 10-K as a result of our expectation of becoming an accelerated filer in the future.

Change in Fair Value of Contingent Consideration

There was no fair value adjustment for contingent consideration liabilities during 2025 resulting in a decrease of $0.6 million compared to 2024.

Restructuring Expense

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-30_item1_business.md)

Item 1. B USINESS

Overview

We are a leading public safety technology company that combines data-driven solutions and strategic advisory services for law enforcement, security teams and civic leadership. As of December 31, 2025, we had approximately 319 customers and to date have worked with approximately 2,100 agencies to help drive more efficient, effective, and equitable public safety outcomes.

Our SafetySmart TM platform includes six data-driven tools consisting of: (i) our flagship product, ShotSpotter ® , the leading outdoor gunshot detection, location and alerting system trusted by 178 cities and 22 universities and corporations as of December 31, 2025; (ii) CrimeTracer TM , an agency-wide crime data and intelligence platform that enables investigators, analysts, patrol officers and command staff to search through more than one billion criminal justice records from across jurisdictions, leverage dashboards and AI-assisted tools to generate tactical leads and quickly make intelligent connections to solve cases; (iii) CaseBuilder TM , a one-stop investigative case management system for tracking, reporting and collaborating on cases; (iv) ResourceRouter TM , which directs the deployment of patrol and community anti-violence resources in an objective way to help maximize the impact of limited resources and improve community safety; (v) PlateRanger TM powered by Rekor ® , an automatic license plate recognition ("ALPR") and vehicle identification solution that leverages artificial intelligence ("AI") and machine learning to enhance investigative efficiency and provide real-time data sharing for law enforcement; and (vi) SafePointe TM , an AI-based weapons detection system designed to provide discreet, high-throughput screening that complements physical security measures without compromising visitor experience. These solutions may operate independently or together as an integrated system that connects detection, data analysis, resource deployment and case management workflows. We also offer other use-case specific solutions including ShotSpotter for Campus and ShotSpotter for Corporate, which are typically smaller-scale deployments of ShotSpotter gunshot detection vertically marketed to universities, corporate campuses and key infrastructure centers to mitigate risk and enhance security by notifying authorities of outdoor gunfire incidents, saving critical minutes for first responders to arrive. We offer the majority of our solutions on a software-as-a-service subscription model to our customers. In the first quarter of 2025, we rolled out a perimeter-based sniper gunshot detection solution targeting utility substations, with initial pilots aimed at utility customers, conducted through SoundThinking Labs. SoundThinking Labs supports innovative use cases of the Company's technology.

As of December 31, 2025, we had ShotSpotter, ShotSpotter for Campus and ShotSpotter for Corporate coverage areas under contract for over 1,092 square miles, of which over 1,064 square miles had gone live. Coverage areas under contract included 178 cities and 22 universities and corporations across the United States, South Africa, Uruguay, Brazil and the Bahamas, including some of the largest cities in the United States. Most of our revenue is attributable to customers based in the United States. Since our founding over 29 years ago, SoundThinking has been and continues to be a purpose-led company. We are a mission-driven organization that is focused on improving public safety outcomes. We accomplish this by earning the trust of law enforcement and providing solutions to help them better engage and strengthen the police-community relationships in fulfilling their sworn obligation to serve and protect all. Our inspiration comes from our principal founder, Dr. Bob Showen, who believes that the highest and best use of technology is to promote social good. We are committed to developing comprehensive, respectful and engaged partnerships with law enforcement agencies, elected officials and communities focused on making a positive difference in the world.

Industry Background: The Public Safety Gap

Local police departments are challenged to serve and protect in an increasingly transparent fashion without unintentionally over-policing and under serving their communities. This mandate must be met while facing municipal budget pressures, evolving public safety policies, and calls for police reform, all while violent crime remains a critical concern and case closure rates struggle to improve. There are three distinct problems associated with the public safety gap, which are discussed below.

The Violent Crime Problem

We believe the majority of urban gunfire goes unreported. A 2016 report published by the Brookings Institution analyzing data collected from ShotSpotter and our customers suggests that approximately 80% of the gunshots detected by our public safety solution are not reported to 911 by residents. Even in the instances when 911 calls are made, the information reported by the caller is often incomplete or inaccurate as to the time and location of the gunshot. Furthermore, in many cases it is often difficult for the caller to authenticate the incident as gunfire. In addition, we believe that in communities plagued by gun violence, there is often a lack of trust between the community's residents and its police force, which can exacerbate the underreporting of gunfire and create a vicious cycle of underreporting, lack of response and increased mistrust due to continued unaddressed gun violence in the community. When gunfire is not reported or is reported inaccurately, law enforcement and medical personnel cannot address injuries nor effectively investigate and solve related crimes or prevent future incidents.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-30_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-30_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-30_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-14_2-02-results.md, 10-K_2026-03-30_item7_mdna.md, 10-K_2026-03-30_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
