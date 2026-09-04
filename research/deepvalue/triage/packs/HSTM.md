# Triage pack — HSTM · HEALTHSTREAM INC

_Generated 2026-09-04 17:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** HSTM · **Name:** HEALTHSTREAM INC
- **CIK:** 0001095565
- **SIC:** 7370 — Services-Computer Programming, Data Processing, Etc.
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/HSTM

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** HEALTHSTREAM INC
- **CIK:** 1,095,565 · **SIC:** 7370 (Services-Computer Programming, Data Processing, Etc.) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 29.74 |
| mktcap | $869.6M |
| ev | $823.4M |
| ev_ebit | 40.7x |
| fcf | $59.6M |
| fcf_yield | 6.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.1% |
| net_debt | -$46.2M |
| net_debt_ebit | -2.3x |
| cash | $46.2M |
| ltd | $0.00 |
| equity | $356.6M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $304.1M |
| revenue_prior | $291.6M |
| rev_growth | 4.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $20.2M |
| net_income | $18.3M |
| cfo | $63.3M |
| capex | $3.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 29,239,955 |
| shares_py | 29,641,207 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 0.3% |
| r6m | 36.5% |
| off_52w_high | -0.1% |
| adv20 | $5.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.58 |
| r_ev_ebit | 0.17 |
| r_roic | 0.52 |
| r_rev_growth | 0.50 |
| r_buyback | 0.76 |
| score | 0.56 |

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
| rank | 189 |

**Screen rationale:** buying back stock -1.4%; debt data missing (net cash unverified); 12-1 momentum 0.3%


## 3. Share count trend

- Shares outstanding: **29,239,955** (CY2026Q2I) vs **29,641,207** prior year (CY2025Q2I)
- Change: **-1.4%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-08** — Item 5.02 (officer / director change or comp arrangement): As disclosed by HealthStream, Inc. (the "Company") in a press release issued on May 4, 2026, announcing the Company's results of operations for the three months ended March 31, 2026, Michael M. Collier has been promoted to the Company's Chief Operating...
- **2026-03-13** — Item 1.01 (Entry into a Material Definitive Agreement): On March 13, 2026, HealthStream, Inc., a Tennessee corporation (the "Company"), and Truist Bank, a North Carolina banking corporation ("Truist"), entered into that certain First Amendment to Amended and Restated Revolving Credit Agreement (the "Amendment")...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 8,000 sh / $224,000 -> net $-224,000 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 34 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 3 |
| M | 29 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026'; skipped 2 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ex_967176.htm)

Second Quarter 2026

• | Revenues of $83.7 million, up 12.5% from $74.4 million in the second quarter of 2025 , setting a new Company record for quarterly revenue

• | Operating income of $8.3 million, up 41.4% from $5.9 million in the second quarter of 2025

• | Net income of $6.7 million, up 23.8% from $5.4 million in the second quarter of 2025

• | Earnings per share (EPS) of $0.23 per share (diluted), up from $0.18 per share (diluted) in the second quarter of 2025

• | Adjusted EBITDA 1 of $20.6 million, up 16.9% from $17.6 million in the second quarter of 2025

• | Board of Directors declared a quarterly cash dividend of $0.035 per share, payable on August 28, 2026 to holders of record on August 17, 2026

Financial Results:

Second Quarter 2026 Compared to Second Quarter 2025

Revenues for the second quarter of 2026 increased by $9.3 million, or 12.5% , to $83.7 million, compared to $74.4 million for the second quarter of 2025 . Subscription revenues increased by $8.0 million, or 11.2%, and professional services revenues increased by $1.3 million compared to the second quarter of 2025 . Compared to the second quarter of 2025, revenue growth for the second quarter of 2026 was positively impacted by $3.1 million from our acquisitions of Virsys12 and MissionCare Collective completed during the fourth quarter of 2025 and $6.2 million from growth across our existing portfolio of solutions, of which $2.0 million related to the resolution of previously constrained estimates of variable consideration under a customer contract, which was recognized as a cumulative catch-up in accordance with ASC 606 during the second quarter of 2026.

Operating income was $8.3 million for the second quarter of 2026 , up 41.4% from $5.9 million in the second quarter of 2025 . The improvement in operating income was primarily attributable to increased revenues and income associated with our sublease that commenced during the second quarter of 2025 . These improvements were partially offset by higher expenses in the second quarter of 2026 including increased personnel costs, third-party software expenses, sales commissions, marketing, cloud hosting, royalties, and amortization expense from our fourth quarter 2025 acquisitions.

Net income was $6.7 million in the second quarter of 2026 , up 23.8% from $5.4 million in the second quarter of 2025 , and EPS was $0.23 per share (diluted) in the second quarter of 2026 , up from $0.18 per share (diluted) in the second quarter of 2025 .

1 Adjusted EBITDA is a non-GAAP financial measure. A reconciliation of adjusted EBITDA to net income and disclosure regarding why we believe adjusted EBITDA provides useful information to investors is included later in this release.

HealthStream Announces Second Quarter 2026 Results Page 2 August 3, 2026

Adjusted EBITDA was $20.6 million for the second quarter of 2026 , up 16.9% from $17.6 million in the second quarter of 2025 .

At June 30, 2026 , the Company had cash, cash equivalents, and marketable securities of $66.7 million. The Company does not have any outstanding indebtedness from borrowed money. Capital expenditures incurred during the second quarter of 2026 were $8.5 million.

Year-to-Date 2026 Compared to Year-to-Date 2025

For the six months ended June 30, 2026 , revenues were $164.9 million, an increase of 11.5% over revenues of $147.9 million for the first six months of 2025 . Operating income for the first six months of 2026 increased by 54.2% to $15.8 million, compared to $10.3 million for the first six months of 2025 . The increase in operating income was primarily attributable to higher revenues and income associated with our sublease that commenced during the second quarter of 2025, partially offset by higher expenses to support investments in several areas of the business, primarily in our platform and enterprise applications, resulting in higher labor costs, third-party software, royalties expense, cloud hosting, along with higher commissions expense. Net income for the first six months of 2026 increased to $12.6 million, compared to $9.7 million for the first six months of 2025 . Earnings per share were $0.43 per share (diluted) for the first six months of 2026 , compared to $0.32 per share (diluted) for the first six months of 2025 . Adjusted EBITDA increased by 20.4% to $40.7 million for the first six months of 2026 , compared to $33.8 million for the first six months of 2025 .

Other Business Updates

On March 13, 2026, the Company announced a new share repurchase program approved by the Board of Directors under which the Company is authorized to repurchase up to $10.0 million of its outstanding shares of common stock. Pursuant to this authorization, the Company is authorized to make repurchases in the open market, including under Rule 10b5-1 plans, through privately negotiated transactions, or otherwise. This share repurchase program will terminate on the earlier of September 12, 2026 or when the maximum dollar amount under the plan is expended. During the three months ended June 30, 2026, the Company repurchased 90,131 shares of common stock at an aggregate fair value of $1.8 million under this authorization. Moreover, during the six months ended June 30, 2026, the Company repurchased 209,498 shares of common stock at an aggregate fair value of $4.3 million under this authorization.

Additionally, during the three months ended March 31, 2026, the Company repurchased 222,978 shares of common stock at an aggregate fair value of $5.0 million under its prior share repurchase program that was authorized on November 11, 2025. This program authorized the Company to repurchase up to $10.0 million of its outstanding shares of common stock and terminated during the three months ended March 31, 2026 when the maximum dollar amount under the program was expended.

In the aggregate during the first six months of 2026, the Company repurchased 432,476 shares of common stock under the share repurchase programs described above on a collective basis at an aggregate fair value of $9.3 million, reflecting an average purchase of $21.50 per share (excluding the cost of broker commissions and the 1% share repurchase excise tax imposed by the Inflation Reduction Act of 2022).

On August 3, 2026, the Board of Directors approved a quarterly cash dividend under the Company's dividend policy of $0.035 per share, payable on August 28, 2026 to holders of record on August 17, 2026.

HealthStream Announces Second Quarter 2026 Results Page 3 August 3, 2026

Financial Outlook for 2026

The Company is updating its guidance for 2026 for the measures set forth below.

Full Year 2026 Guidance
Low | High
Revenue 1 | 327.0 | - | 332.0 | million
Net Income 2 | 19.5 | - | 22.2 | million
Adjusted EBITDA 3 | 74.0 | - | 78.0 | million
Capital Expenditures | 31.0 | - | 34.0 | million

1 Previous expected Revenue guidance range was $323.0 to $330.0 million.

2 Previous expected Net Income guidance range was $20.4 to $22.8 million.

3 Previous expected Adjusted EBITDA guidance range was $73.0 to $77.0 million. Adjusted EBITDA is a non-GAAP financial measure. A reconciliation of projected adjusted EBITDA to projected net income (the most comparable GAAP measure) is included later in this release.

The Company's guidance for 2026, as set forth above, reflects the Company's assumptions regarding, among other things, expectations for new sales and renewals, and assumes that general economic conditions do not deteriorate. This guidance does not include the impact of any future acquisitions or dispositions that we may complete during 2026, gains or losses from changes in the fair value of non-marketable equity investments or contingent consideration, or impairment of long-lived assets.

Robert A. Frist, Jr., Chief Executive Officer, HealthStream, said, "In the second quarter of 2026, HealthStream delivered record revenue of $83.7 million, up 12.5%, and adjusted EBITDA of $20.6 million, up 16.9%, compared to the second quarter of 2025. This performance gives us the flexibility to continue investing in our hStream platform and products that we believe will drive durable, long-term growth as we build an even stronger ecosystem for the healthcare organizations and professionals we serve."

A conference call with Robert A. Frist, Jr., Chief Executive Officer, Scott A. Roberts, Chief Financial Officer and Senior Vice President, and Mollie Condra, Head, Investor Relations and Communications, will be held on Tuesday, August 4, 2026, at 9:00 a.m. (ET). Participants may access the conference call live via webcast using this link: https://edge.media-server.com/mmc/p/jzehvmr3. To participate via telephone, please register in advance using this link: https://register-conf.media-server.com/register/BIe2f962877acd428995d6691d8adf91a5. A replay of the conference call and webcast will be archived on the Company's website in the Investor Relations section under "Events & Presentations."

HealthStream Announces Second Quarter 2026 Results Page 4 August 3, 2026

Use of Non-GAAP Financial Measures

This press release presents adjusted EBITDA, a non-GAAP financial measure used by management in analyzing the Company's financial results and ongoing operational performance. In order to better assess the Company's financial results, management believes that net income before interest, income taxes, stock-based compensation, depreciation and amortization, impairments of long-lived assets, changes in fair value of contingent consideration, and changes in fair value of, including gains (losses) on the sale of, non-marketable equity investments ("adjusted EBITDA") is a useful measure for evaluating the operating performance of the Company because adjusted EBITDA reflects net income adjusted for certain GAAP accounting, non-cash, and/or non-operating items which may not, in any such case, fully reflect the underlying operating performance of our business. We believe that adjusted EBITDA is useful to investors to assess the Company's ongoing operating performance and to compare the Company's operating performance between periods. In addition, certain short-term cash incentive bonuses and performance-based equity awards are based on the achievement of adjusted EBITDA (as defined in applicable bonus and equity grant documentation) targets.

Adjusted EBITDA is a non-GAAP financial measure and should not be considered as a measure of financial performance under GAAP. Because adjusted EBITDA is not a measurement determined in accordance with GAAP, adjusted EBITDA is susceptible to varying calculations. Accordingly, adjusted EBITDA, as presented, may not be comparable to other similarly titled measures of other companies and has limitations as an analytical tool.

Adjusted EBITDA should not be considered a substitute for, or superior to, measures of financial performance, which are prepared in accordance with GAAP. Investors are encouraged to review the reconciliations of adjusted EBITDA to net income (the most comparable GAAP measure), which is set forth below in this release.

About HealthStream

HealthStream (Nasdaq: HSTM) is the healthcare industry's largest ecosystem of platform-delivered clinical workforce solutions that empowers healthcare professionals to do what they do best: deliver excellence in patient care. For more information about HealthStream, visit www.healthstream.com or call 615-301-3100.

HealthStream Announces Second Quarter 2026 Results Page 5 August 3, 2026

HEALTHSTREAM, INC.

Condensed Consolidated Statements of Income

(In thousands, except per share data)

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-27_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

OVERVIEW

HealthStream provides primarily SaaS based applications for healthcare organizations—all designed to improve business and clinical outcomes by supporting the people who deliver patient care. We are focused on helping individuals and organizations in healthcare meet their ongoing learning, clinical development, credentialing, and scheduling needs. We also provide our solutions to nursing schools and nursing students.

Our business is managed and organized around our single platform strategy, also referred to as our One HealthStream approach. At the center of this single platform strategy is our hStream technology platform. By enabling our applications through hStream, we believe that stand-alone applications, which already provide a powerful value proposition on their own, are beginning to leverage each other to more efficiently and effectively empower our customers to manage their businesses and improve their outcomes. Further, the Company's internal structure and executive leadership are likewise shaped by the organizing principle of a single platform, including with regard to technology, operations, accounting, internal reporting (including the nature of information reviewed by our key decision makers), organizational structure, compensation, performance assessment, and resource allocation. Ongoing progress towards One HealthStream is exemplified by our recent refinement and adoption of a standardized, enterprise-wide implementation, onboarding, and customer success operational model.

Our solutions are powered by our hStream technology platform that enables activity across HealthStream's diverse ecosystem of applications. These underlying solutions are comprised primarily of SaaS, subscription-based applications that are used by healthcare organizations to meet a broad range of their workforce development needs around learning, clinical development, credentialing, and scheduling. Our solutions are also utilized by nursing schools as they prepare the healthcare workforce of tomorrow and by nursing students as they prepare to enter that workforce. Our numerous content libraries allow customers to subscribe to a wide array of courseware, which includes content from leading healthcare and nursing associations, medical and healthcare publishers, and other ecosystem partners. Our scheduling solutions provide organizations with the tools to visualize and manage real-time clinical staff scheduling to enable them to optimize their workforce, reduce costs, and improve care. Our flagship credentialing, privileging, and enrollment solution, CredentialStream, provides customers an intuitive, modern user experience with a continual stream of enhancements, evidence-based content, and curated data, all of which provides healthcare organizations with tools to support the provider lifecycle management from recruiting, application submission, verification of licensure and other credentials, privileging, appointments by credentialing committees, enrollment, network, management, onboarding, and performance evaluations of providers.

As HealthStream's business continues to evolve, we remain solely dedicated to the healthcare market, and our primary customers continue to be healthcare organizations across the continuum of care and other participants in the healthcare industry, such as nursing schools and nursing students, whether through our enterprise applications or our emerging career networks.

Revenues for the year ended December 31, 2025 were $304.1 million, compared to $291.6 million for the year ended December 31, 2024, an increase of 4%. The contributions to growth were $13.3 million in subscription revenues, partially offset by a decrease of $0.9 million in professional services revenues. Subscription revenue increases resulted from growth in several products, including Competency Suite, CredentialStream, and ShiftWizard, coupled with contributions from our recent acquisitions (Virsys12 and MissionCare), but were partially offset by declines in our legacy credentialing, scheduling, and content program solutions. Operating income decreased by 5% to $20.2 million for 2025, compared to $21.3 million for 2024. Net income decreased to $18.3 million for 2025, compared to $20.0 million for 2024. Earnings per share were $0.61 per share (diluted) for 2025, compared to $0.66 per share (diluted) for 2024.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

RESULTS OF OPERATIONS

Revenues and Expense Components

The following descriptions of the components of revenues and expenses apply to the comparison of results of operations.

Revenues, net. The products and services generating revenues are increasingly oriented around and drive value in relation to our hStream technology platform. Subscription or software licensing services primarily consist of the provision of services through our platform, learning management application, a variety of training and development tools and content subscriptions, our applications that help facilitate provider credentialing, privileging, and enrollment administration, and staff scheduling applications. Professional services primarily consist of training, implementation and onboarding, and consulting services to serve professionals that work within healthcare organizations.

Cost of Revenues (excluding depreciation and amortization). Cost of revenues (excluding depreciation and amortization) consist primarily of salaries and employee benefits, stock-based compensation, employee travel and lodging, materials, contract labor, hosting costs, third party software licensing costs, and other direct expenses associated with revenues, as well as royalties paid by us to ecosystem partners. Personnel costs within cost of revenues are associated with individuals that facilitate product delivery, provide services, handle customer support calls or inquiries, manage the technology infrastructure for our applications, manage content, and provide training or implementation services.

Product Development. Product development consists primarily of salaries and employee benefits, contract labor, stock-based compensation, employee travel and lodging, costs associated with the development of new software and feature enhancements, new products, third party software licensing costs, and costs associated with maintaining and developing our products. Personnel costs within product development include our systems teams, application development, quality assurance teams, product managers, and other personnel associated with software and product development.

Sales and Marketing. Sales and marketing consist primarily of salaries and employee benefits, commissions and amortization of deferred commissions, stock-based compensation, employee travel and lodging, third party software licensing costs, advertising, trade shows, customer conferences, promotions, and related marketing costs. Personnel costs within sales and marketing include our sales teams and marketing personnel.

General and Administrative Expenses. General and administrative expenses consist primarily of salaries and employee benefits, stock-based compensation, employee travel and lodging, facility expenses, sublease income, office expenses, fees for professional services, business development and acquisition-related costs, third party software licensing costs, provision for credit losses, and other operational expenses. Personnel costs within general and administrative expenses include individuals associated with normal corporate functions, including accounting, legal, business development, human resources, administrative, internal information systems, and executive management.

Depreciation and Amortization. Depreciation and amortization consist of fixed asset depreciation, amortization of intangibles considered to have definite lives, and amortization of capitalized software development.

Interest Income. Interest income consists of interest earned on cash, cash equivalents, and marketable securities.

Other (Expense) Income, Net. The primary components of other (expense) income are interest expense, the income or loss attributed to equity method investments, fair value adjustments related to non-marketable equity investments, and foreign currency gains and losses.

2025 Compared to 2024

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-27_item1_business.md)

Item 1. Business

OVERVIEW AND HISTORY

HealthStream's focus is and has always been on improving the quality of healthcare through the development and support of the dedicated individuals who deliver care. Like healthcare itself, our mission remains constant, but how we accomplish that mission continues to evolve and improve over time. Originally, we pioneered the use of online learning to hospitals, which began with courses specifically tailored to educate healthcare professionals and meet hospitals' required regulatory needs, and we remain a leading innovator in those areas today. Since our inception, the scope of HealthStream's Software-as-a-Service (SaaS) solutions has expanded well beyond our governance, risk, and compliance (GRC) offerings to include a diverse ecosystem of applications that optimize and support the healthcare workforce and the students preparing to enter that workforce. Today, we are characterized by our single platform strategy, which is designed to create interoperability among the various applications in our ecosystem through our proprietary hStream technology platform. Increasingly, our hStream technology platform extends artificial intelligence (AI) capabilities to the applications it powers and serves as the system of record on which healthcare workforce AI relies. We believe that our single platform strategy, as represented by hStream, is the best way to realize our mission of improving the quality of care by developing the people who deliver care, and the best way to create value for our shareholders in the process.

For healthcare organizations—our primary customers—HealthStream's solutions help to effectively onboard, retain, engage, educate, manage, and develop workforce talent; meet rigorous GRC requirements; optimize staff scheduling and capacity management; and automate the management of medical staff credentialing, privileging, and enrollment.

For healthcare professionals and students—our primary end users—HealthStream's solutions help them to professionally develop their knowledge and skills, manage and fulfill their required continuing education and certifications, manage their schedules, including swapping and filling shifts, engage with peers, provide personalized competency development, and optimize their career pathways. Additionally, our emerging Career Networks provide value directly to healthcare professionals and students, enabling them to evolve their professional identity, skills, portfolio, and career over time.

For both healthcare organizations and healthcare professionals and students, HealthStream's solutions are generally accessed through SaaS application suites that are increasingly enhanced through our hStream technology platform, including through the functionality it offers and the data it originates and enriches. Our learning, credentialing, and scheduling application suites are designed to help solve the most critical problems facing the healthcare workforce today. This is achieved through a combination of established and cutting-edge technologies, such as initiative and workflow management capabilities; proprietary taxonomy engines; dynamic engagement models; AI and machine learning (ML) driven clinical assessments; physical-based simulations; healthcare-specific benchmarks; and automated license monitoring and validation.

HealthStream's success in offering one of the largest, most diverse ecosystem of workforce solutions in healthcare has made it a thought leader and barometer of innovation for the industry. From its roots in originating online learning for healthcare organizations to the Company's more recent release of "Competency Suite" the first AI/ML-driven clinical competency development system, HealthStream continues to believe that the key to quality patient care lies in the people who deliver care. To that end, we are solely dedicated to providing solutions for the healthcare workforce and for those about to enter it.

The Company was incorporated in 1990. It began providing its SaaS-based workforce solutions in 1999, its provider solutions in 2012, and launched the hStream technology platform in 2018. Since January 2023, the Company's operations have been streamlined around a consolidated, enterprise approach, and since January 1, 2023, the Company has had a single reportable segment and presents financial information on a single segment basis. HealthStream is headquartered in Nashville, Tennessee and had 1,139 full-time and 21 part-time employees as of December 31, 2025.

INDUSTRY BACKGROUND

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-27_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-27_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-27_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-02-27_item7_mdna.md, 10-K_2026-02-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
