# Triage pack — OMDA · Omada Health, Inc.

_Generated 2026-09-05 01:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** OMDA · **Name:** Omada Health, Inc.
- **CIK:** 0001611115
- **SIC:** 8000 — Services-Health Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/OMDA

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Omada Health, Inc.
- **CIK:** 1,611,115 · **SIC:** 8000 (Services-Health Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 22.29 |
| mktcap | $1.4B |
| ev | $1.1B |
| ev_ebit | n/a |
| fcf | $16.9M |
| fcf_yield | 1.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -30.5% |
| net_debt | -$221.7M |
| net_debt_ebit | n/a |
| cash | $221.7M |
| ltd | $0.00 |
| equity | $252.7M |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $260.2M |
| revenue_prior | $169.8M |
| rev_growth | 53.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$12.0M |
| net_income | -$12.8M |
| cfo | $18.3M |
| capex | $1.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 6.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 61,216,703 |
| shares_py | 57,574,921 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -18.9% |
| r6m | 63.9% |
| off_52w_high | -16.8% |
| adv20 | $33.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.27 |
| r_ev_ebit | 0.00 |
| r_roic | 0.03 |
| r_rev_growth | 0.95 |
| r_buyback | 0.16 |
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
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 422 |

**Screen rationale:** revenue +53.2%


## 3. Share count trend

- Shares outstanding: **61,216,703** (CY2026Q2I) vs **57,574,921** prior year (CY2025Q2I)
- Change: **6.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-06** — Item 5.02 (officer / director change or comp arrangement): On August 6, 2026, the Company announced that Sean Duffy, the Company's current Chief Executive Officer, will become the Company's Executive Chairman of the Board of Directors (the "Board"), and Wei-Li Shao, the Company's current President, will succeed Mr....

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 97,135 sh / $2,296,906 -> net $-2,296,906 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 50 (open-market buys 0, sales 16).

| code | rows |
|---|---|
| F | 4 |
| M | 30 |
| S | 16 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Omada Health Reports Second Quarter 2026 Results and Announces CEO Tra'; skipped 11 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99 - EX-99 (q2fy26pressrelease.htm)

Omada Health Reports Second Quarter 2026 Results and Announces CEO Transition

• Revenue Grew 43% and Total Members Increased 45% Year over Year, with Gross Margin Reaching a New Quarterly Record

• Company Announces Sean Duffy to Become Executive Chair and Wei-Li Shao to Become Chief Executive Officer on January 1, 2027

SAN FRANCISCO - August 6, 2026 - Omada Health, Inc. (Nasdaq: OMDA), the virtual between-visit healthcare provider, today reported financial results for the second quarter ended June 30, 2026. Omada Health also announced co-founder and CEO Sean Duffy will transition to Founder and Executive Chair effective January 1, 2027, with President Wei-Li Shao assuming the role of CEO.

Financial Highlights

• Revenue of $88 million, compared with total revenue of $61 million in Q2 2025

• Gross margin of 73% in the second quarter, up from 66% in Q2 2025

• Non-GAAP gross margin of 74% in the second quarter, up from 68% in Q2 2025

• Net income of $5 million in the second quarter, compared with a net loss of $5 million in Q2 2025

• Adjusted EBITDA of $11 million in the second quarter, compared with an adjusted EBITDA loss of $0.2 million in Q2 2025

• Trailing twelve-month revenue per total member grew approximately 2% year over year to $284

• Cash and cash equivalents of $222 million

Please see the non-GAAP Financial Measures section below and reconciliations of GAAP to non-GAAP measures at the end of this press release.

Operational Highlights

• Total Members increased 45% year over year, reflecting continued demand across Omada Health's integrated cardiometabolic care platform and strong enrollment momentum across diabetes and hypertension programs.

• Broadened partnership with Health Care Services Corporation (HCSC), extending our Prevention & Weight Health and Hypertension Management programs across HCSC's fully insured book of business in Illinois, Oklahoma, and New Mexico, reaching an additional 1.5 million covered lives.

• Omada Health launched the first deployment of its cholesterol management offering in July, expanding personalized multi-condition care for employees of one of the nation's largest retailers.

• Since the announcement of our prescribing program, we have closed our first customer, which would yield revenue in 2027, providing early evidence of market demand.

"Our outstanding second quarter reflects the strength of our strategy, the momentum we've built across the business, and the exceptional team driving Omada forward," said Sean Duffy, co-founder and CEO of Omada Health. "Reflecting continued demand for our integrated between-visit care platform, total members increased 45% year over year as we expanded our commercial channels, deepened relationships with our leading PBM channels, and introduced our cholesterol management program with one of the nation's largest retailers. The opportunity ahead is significant, and we'll remain focused on disciplined execution as we look to broaden our capabilities, deepen customer relationships and improve the health of even more members."

Wei-Li Shao to become CEO of Omada Health

Effective January 1, 2027, Wei-Li Shao will become CEO of Omada Health, with responsibility for the company's strategy, operations, and results, reporting to the Board of Directors. Sean Duffy, Founder and CEO, will transition to Founder and Executive Chair, supporting Wei-Li and the Board on Omada Health's long-term mission, key partnerships, and strategic initiatives. In connection with Sean's transition, Jeryl "Jeri" Hilleman, who has served as Chairperson of the Board since July 2020, will become Lead Independent Director and continue as Chairperson of the Audit Committee, also effective January 1, 2027.

"Over the past seven years, Wei-Li and I have worked together to build a strong company as Wei-Li has steadily increased his scope of responsibility. His track record of delivering innovation, commercial wins, and strong financial growth has shaped Omada and demonstrates that Wei-Li is the right leader to take Omada to the next level of impact and scale," said Sean Duffy.

Wei-Li joined Omada Health in 2019 as Chief Commercial Officer and was appointed President in 2021. Since then, he has held direct accountability for Omada Health's P&L and full operating agenda, leading the product, commercial, and operational strategy that scaled the company from a single-condition program into a multi-condition care platform. He built the long-range plan that guides how Omada Health runs today and has been a close strategic partner to Sean throughout the company's growth. Wei-Li brings to the role 18 years at Eli Lilly and Company, where he held senior leadership roles across its global healthcare and biopharmaceutical businesses, including deep experience in the cardiometabolic and diabetes markets at the center of Omada Health's mission.

"I'm honored to lead Omada and continue building on the strong foundation this incredible team has created," said Wei-Li Shao, President of Omada Health. "Fifteen years ago, Sean designed an innovative solution to help Americans bridge the healthcare gap. Together, we've shown the model works, yet I believe our biggest impact is still ahead. Our results serve as a foundation to raise our ambitions. Now is the time to scale, push harder on our mission, and bend the curve of chronic disease."

Financial Outlook

"We delivered another strong quarter, setting quarterly records for revenue of $88 million, GAAP gross margin of 73%, non-GAAP gross margin of 74%, net income of $5 million, and adjusted EBITDA of $11 million. Revenue grew 43% year-over-year. This marks Omada Health's most profitable quarter to date, both in absolute terms and on a margin basis, demonstrating continued operating leverage," said Steve Cook, Chief Financial Officer of Omada Health. "At the midpoint, our raised full‑year outlook represents approximately 30% year‑over‑year revenue growth and a fourfold increase in adjusted EBITDA, reflecting our extraordinary second‑quarter performance and our path of sustainable profitability."

For the year ending December 31, 2026, Omada Health expects:

• Revenue in the range of $334 million to $340 million, with the midpoint representing 30% growth compared with 2025; this range is up from the prior range of $322 million to $330 million.

• Adjusted EBITDA in the range of $21 million to $27 million, with the midpoint representing a four times increase compared with 2025; this range is up from the prior range of $14 million to $20 million.

We have not provided an outlook for net loss (GAAP) or a reconciliation of expected adjusted EBITDA to net loss (GAAP) because net loss (GAAP) on a forward-looking basis is not available without unreasonable effort due to the potential variability and complexity of the items that are excluded from adjusted EBITDA, such as loss on debt extinguishment; provision for income taxes; depreciation and amortization; share-based compensation; change in fair value of warrant liabilities; amortization of intangible assets; and loss on disposal of property and equipment.

Investor Day

Omada Health will host an Investor Day on September 10, 2026 in New York City, where management will present Omada Health's vision, strategy, and long-term growth plans.

Please reach out to investor relations at ir@omadahealth.com for more information.

Conference Call

Omada Health will host a conference call at 1:30 p.m. PT/4:30 p.m. ET today, August 6, 2026, during which management will discuss second quarter 2026 results.

A live audio webcast of the call will be available online at https://investors.omadahealth.com. A replay will be available shortly after the conclusion of the call at the same link and will remain accessible for approximately 12 months.

Those participating via conference call can pre-register using the following link:

https://register-conf.media-server.com/register/BI1da25a61227f4480b4afdedba6928bce

About Omada Health

Omada Health (Nasdaq: OMDA) is reverse engineering the way healthcare is delivered in America, putting the space between doctor visits–where health is won or lost–at the center of care. Today's healthcare system poorly serves chronic conditions that require ongoing support outside of the exam room, like obesity, diabetes, hypertension, cholesterol, and musculoskeletal conditions. Omada's virtual-first model combines human-led care teams, connected devices, and AI-enabled technology to deliver personalized care at scale, including support for GLP-1 therapy. Omada has served more than two million members since launch across 2,000+ employers, health plans, pharmacy benefit managers, and health systems. Learn more at omadahealth.com.

Omada Health, Inc.
Consolidated Balance Sheets
(in thousands, except per-share amounts)
(unaudited)

June 30, 2026 | December 31, 2025
Assets
Current assets
Cash and cash equivalents | 221,712 | 222,036
Accounts receivable, net (1) | 56,573 | 34,585
Inventory | 4,119 | 4,486
Deferred commissions, current | 3,959 | 3,539
Prepaid expenses and other current assets (2) | 8,548 | 8,288
Total current assets | 294,911 | 272,934
Property and equipment, net | 9,098 | 7,942
Deferred commissions, non-current | 9,222 | 8,711
Intangible assets, net | 1,536 | 2,414
Goodwill | 13,240 | 13,240
Other assets | 215 | 165
Total assets | 328,222 | 305,406
Liabilities and stockholders' equity
Current liabilities
Accounts payable (3) | 11,804 | 10,276
Accrued expenses and other current liabilities (4) | 35,978 | 40,392
Deferred revenue (5) | 27,701 | 25,058
Total current liabilities | 75,483 | 75,726
Other liabilities, non-current | - | -
Total liabilities | 75,483 | 75,726
Commitments and contingencies
Stockholders' equity
Common stock, $0.001 par value per share; 750,000 and 750,000 shares authorized as of June 30, 2026 and December 31, 2025, respectively; 60,606 and 58,429 shares issued and outstanding as of June 30, 2026 and December 31, 2025, respectively | 61 | 58
Additional paid-in capital | 707,098 | 686,366
Accumulated deficit | (454,420) | (456,744)
Total stockholders' equity | 252,739 | 229,680
Total liabilities and stockholders' equity | 328,222 | 305,406

(1) Includes amounts from a related party of $40.4 million and $22.8 million as of June 30, 2026 and December 31, 2025, respectively.

(2) Includes amounts from a related party of $0.5 million and $0.3 million as of June 30, 2026 and December 31, 2025, respectively.

(3) Includes amounts from a related party of $0 and $1.0 million as of June 30, 2026 and December 31, 2025, respectively.

(4) Includes amounts from a related party of $6.8 million and $4.9 million as of June 30, 2026 and December 31, 2025, respectively.

(5) Includes amounts from a related party of $20.6 million and $18.8 million as of June 30, 2026 and December 31, 2025, respectively.

Omada Health, Inc.
Condensed Consolidated Statements of Operations and Comprehensive Income (Loss)
(in thousands, except per-share data)
(unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-06_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Our mission is to bend the curve. Our hope is that, one day, tomorrow's epidemiologists will notice a bend in disease curves, wonder what might be happening, and conclude that part of that impact has been Omada. As part of that mission, we strive to inspire and enable people to make lasting health changes on their own terms. We launched our initial program in diabetes prevention and weight health in 2012, with the goal of showing that a virtual program could achieve the same clinical results as its in-person archetype. Today, we offer cardiometabolic programs for prediabetes, diabetes, hypertension, and high cholesterol; a physical therapy program to address musculoskeletal ("MSK") conditions; additional support for members taking glucagon-like peptide-1 agonists ("GLP-1") in our cardiometabolic programs ("GLP-1 Care Tracks"); and behavioral health support across all programs. As of December 31, 2025, we had more than 2,000 customers and over 886,000 total members enrolled in one or more programs.

Our virtual care programs are rooted in evidence and combine relationship-based, human-led clinical care with purpose-built technology. We call this approach Compassionate Intelligence. Our Care Teams, composed of health coaches, select relevant specialists, and licensed physical therapists, depending on the program, deliver healthcare to our members within the scope of their credentials. Our prescribing capability also incorporates third-party licensed obesity care providers for prescribing AOMs and related medication management. Omada Care Teams are supported by our proprietary Care Team Platform that is purpose-built to magnify the impact of our Between-Visit Care model and drive operational excellence in a trusted and secure way. Broadly, our integrated technology platform supports activities across the entire lifecycle of our work with customers, channel partners, and members: from benefit eligibility confirmation and enrollment outreach to application and member onboarding, device management and fulfillment, member-facing tools and applications, Care Team tools, data capture and storage, and platform and billing infrastructure. The investments in our technology and Care Team Platform have enabled us to scale and serve nearly two million members since launch, while maintaining the ability to deliver an exceptional member experience, with high clinical quality and consistency.

Key Factors Affecting Our Performance

Key Factors Affecting Our Performance

We believe that our future growth, success, and performance are dependent on many factors, including those set forth below. While these factors present significant opportunities for us, they also represent the challenges that we must successfully address in order to grow our business and improve our results of operations.

Acquisition of New Customers and Channel Partners

We believe there is substantial opportunity to further grow our base of customers and channel partners in our large addressable market. Historically, we have relied on a limited number of customers and channel partners, including employers, health plans, PBMs, health systems, and government entities, for a substantial portion of our total sales. Our customers include employers that cover our programs for their employees and their dependents and health systems that cover our programs for patients, among other types of customers. In addition, our channel partners, which include certain of the health plans, PBMs, and other entities that we work with, operate as resellers of our programs to their employer customers or other end customers, which can limit an end customer's ability to continue purchasing our programs if the customer no longer works with a particular channel partner. Some of the health plans and PBMs we work with as channel partners also cover our programs directly, for a portion of their own members, as our customers.

We seek to grow our business by acquiring more covered lives across multiple buyer categories: selling to new customers and channel partners as well as expanding within our existing channel partners to new lines of business. Our diverse go-to-market strategy affords us flexibility to pursue growth via multiple distinct channels, including through new channels and in lines of business where we have yet to place significant focus, such as Medicare Advantage.

Customer and Channel Partner Retention

Our ability to increase revenue depends on maintaining and deepening relationships with customers and channel partners over time, driving both renewal revenue and expansion revenue as customers and channel partners add new programs to provide to their member base. We have invested and plan to continue to invest across our data, analytics, operations, and customer success capabilities to build the infrastructure that supports our go-to-market approach.

Program Expansion within Existing Customer Base

We believe that the ability to grow the share of revenue that we generate from existing customers is a key driver of long-term growth. We have seen significant expansion over time as existing customers and channel partners have added our newer Diabetes, Hypertension, and Cholesterol programs, and we remain focused on driving multi-program adoption as a key growth lever. We believe there is still opportunity to continue multi-condition expansion.

Member Enrollment

Having served nearly two million members since launch, there is still significant opportunity to enroll more members. We are focused on achieving higher enrollment rates by helping more customers and channel partners adopt our enrollment outreach best practices, including enabling Omada-led enrollment outreach campaigns, implementing strategies to reach individuals with known risk, and evaluating new enrollment strategies and channels.

Member Engagement and Outcomes

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following discussion and analysis includes a comparison of our results of operations for the year ended December 31, 2025 to the year ended December 31, 2024, unless otherwise stated. For a comparison of the results of operations for the year ended December 31, 2024 to the year ended December 2023, see the section titled "Management's Discussion and Analysis of Financial Condition and Results of Operations" in our prospectus dated June 5, 2025, filed with the SEC on June 9, 2025.

The following table sets forth our results of operations for each of the periods presented:

Year Ended December 31,
2025 | 2024 | 2023
(in thousands)
Revenue
Services | 241,043 | 157,789 | 114,531
Hardware | 19,167 | 12,011 | 8,253
Total revenue | 260,210 | 169,800 | 122,784
Cost of revenue
Services (1)(2)(3) | 51,839 | 42,520 | 36,735
Hardware | 37,432 | 24,403 | 16,078
Total cost of revenue | 89,271 | 66,923 | 52,813
Gross profit | 170,939 | 102,877 | 69,971
Operating expenses
Research and development (1)(3) | 40,683 | 35,923 | 33,738
Sales and marketing (1)(2)(3) | 90,044 | 68,053 | 66,249
General and administrative (1)(3) | 52,184 | 42,555 | 35,981
Total operating expenses | 182,911 | 146,531 | 135,968
Operating loss | (11,972) | (43,654) | (65,997)
Other expense, net
Interest expense | (2,534) | (4,506) | (4,705)
Interest income | 5,305 | 805 | 5,775
Loss on debt extinguishment | (2,109) | - | (1,536)
Change in fair value of warrant liabilities | (1,468) | 218 | (1,048)
Total other expense, net | (806) | (3,483) | (1,514)
Loss before provision for income taxes | (12,778) | (47,137) | (67,511)
Provision for income taxes | - | - | -
Net loss and comprehensive loss | (12,778) | (47,137) | (67,511)

(1) Includes share-based compensation expense as follows:

Year Ended December 31,
2025 | 2024 | 2023
(in thousands)
Cost of services revenue | 169 | 219 | 87
Research and development | 2,228 | 1,713 | 1,585
Sales and marketing | 3,918 | 2,602 | 2,180
General and administrative | 6,640 | 4,886 | 4,888
Total share-based compensation expense | 12,955 | 9,420 | 8,740

(2) Includes amortization of intangible assets as follows:

Year Ended December 31,
2025 | 2024 | 2023
(in thousands)
Cost of services revenue | 1,757 | 1,755 | 1,793
Sales and marketing | 94 | 252 | 251
Total amortization of intangible assets | 1,851 | 2,007 | 2,044

(3) Includes depreciation and amortization as follows:

Year Ended December 31,
2025 | 2024 | 2023
(in thousands)
Cost of services revenue | 3,293 | 2,406 | 1,974
Research and development | 88 | 83 | 83
Sales and marketing | 121 | 118 | 122
General and administrative | 138 | 189 | 225
Total depreciation and amortization (i) | 3,640 | 2,796 | 2,404

(i) Depreciation and amortization includes depreciation of property and equipment and amortization of capitalized internal-use software costs.

Percentage of Revenue Data

Year Ended December 31,
2025 | 2024 | 2023
(in thousands)
Revenue
Services | 93 | % | 93 | % | 93 | %
Hardware | 7 | 7 | 7
Total Revenue | 100 | 100 | 100
Cost of revenue
Services | 20 | 25 | 30
Hardware | 14 | 14 | 13
Total cost of revenue | 34 | 39 | 43
Gross profit | 66 | 61 | 57
Operating expenses
Research and development | 16 | 21 | 28
Sales and marketing | 35 | 41 | 54
General and administrative | 20 | 24 | 29
Total operating expenses | 71 | 86 | 111
Operating loss | (5) | (25) | (54)
Other expense, net
Interest expense | (1) | (4) | (4)
Interest income | 2 | 1 | 5
Loss on debt extinguishment | (1) | — | (1)
Change in fair value of warrant liabilities | (1) | — | (1)
Total other expense, net | (1) | (3) | (1)
Loss before provision for income taxes | (6) | (28) | (55)
Provision for income taxes | — | — | —
Net loss and comprehensive loss | (6) | % | (28) | % | (55) | %

Comparison of the years ended December 31, 2025 and 2024

Revenue

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-06_item1_business.md)

Item 1. Business

Overview

Our mission is to bend the curve. Our hope is that, one day, tomorrow's epidemiologists will notice a bend in disease curves, wonder what might be happening, and conclude that part of that impact has been Omada. As part of that mission, we strive to inspire and enable people to make lasting health changes on their own terms. We deliver virtual care between doctor's visits, providing an engaging, personalized, and integrated experience for the individuals in our programs, which we call our "members." Our care is designed to improve their health while delivering value for the employers, health insurance companies ("health plans"), health systems, pharmacy benefit managers ("PBMs"), and other entities that cover the cost of our programs. Our platform is grounded in evidence and supported by peer-reviewed clinical research and third-party accreditations, which we believe enhances credibility with customers, our reseller partners, and other stakeholders. We differentiate through our human-led, technology-enabled care model, which combines proactive Care Teams with data-driven tools to deliver personalized support at scale. We call this approach Compassionate Intelligence. We work to develop trust with each member and use technology to help us personalize their experience, enabling us to unlock results at scale.

Since our founding, our programs have had a meaningful, positive impact. As of December 31, 2025, we had more than 2,000 customers, over 886,000 total members enrolled in one or more programs, and had supported nearly two million members since launch. We sell our programs to customers that cover the cost for covered individuals, either by contracting with us directly or by arranging access through entities that we call "channel partners," which resell our programs to their own end customers. We count a member as enrolled in a program to the extent their participation was billed at least once in the preceding 12 months. We believe our programs serve a clear need for our customers and channel partners as well as our members, which is reinforced by our strong customer satisfaction and member engagement rates. As of December 2025, more than 55% of members in month 12 and more than 50% of members in month 24 of our cardiometabolic programs still engaged with the platform at least once during the respective month. We consider members to be still engaged after one year or two years in the program if, during their twelfth or twenty-fourth month of program participation in a cardiometabolic program, they complete at least one interaction with us, such as logging in or interacting with the Omada mobile app, sending messages to Omada Care Team members, or recording metrics such as weight, blood pressure, or blood glucose values.

We believe we compete effectively based on a combination of clinical rigor, differentiated care delivery, and a scalable go-to-market strategy. In addition, our multi-condition platform enables customers and members to access support for multiple conditions through a single partner, and the high rate of comorbidities across these conditions can be addressed in a more coordinated manner. Our diversified go-to-market strategy further allows flexible deployment across employers, health plans, PBMs, and other channels, supporting broad adoption and long-term relationships.

Our Programs

Omada Cardiometabolic Programs

We launched our first program focused on diabetes prevention in 2012. Since then, we also observed a demand from our customers and channel partners to expand beyond diabetes prevention and weight management and into other conditions, such as the treatment and management of diabetes, hypertension, and high cholesterol as well as supporting members on their glucagon-like peptide-1 agonists ("GLP-1") weight-loss journeys. We refer to these as our "Cardiometabolic Programs." The significant overlap across these chronic conditions created a natural growth avenue by enabling a coordinated, context-informed care approach across conditions. Within our Cardiometabolic Programs, we pair members with a dedicated health coach and/or a Certified Diabetes Care and Education Specialist, when clinically appropriate, for the entirety of their experience. We further support our members with third-party connected devices such as connected scales, blood glucose monitors, continuous glucose monitors, and blood pressure monitors, depending on their individual needs, a personalized learning path, nutrition counseling, and support from peer groups to build community.

Omada for Prevention & Weight Health : Omada for Prevention & Weight Health, our first program, focuses on prediabetes and weight management, two critical elements of preventing diabetes and heart disease. Informed by guidelines and recommendations set by the U.S. Preventive Services Task Force and the Centers for Disease Control and Prevention

"CDC", the goal of the program is to enable members to lose weight, maintain a healthy weight, and increase physical activity.

Omada for Diabetes : Launched in 2018, Omada for Diabetes is designed to help members with type 1 or type 2 diabetes achieve stable blood glucose levels and meet and reach their A1C reduction goals based in part on treatment guidelines from the ADA. Because most people with type 2 diabetes have obesity or are overweight, we also support members with reaching and maintaining a healthy weight through modifications in diet, exercise, and other behaviors.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-06_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-06_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-06_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-06_item7_mdna.md, 10-K_2026-03-06_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
