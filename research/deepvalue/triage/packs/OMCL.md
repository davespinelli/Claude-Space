# Triage pack — OMCL · OMNICELL, INC.

_Generated 2026-09-04 20:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** OMCL · **Name:** OMNICELL, INC.
- **CIK:** 0000926326
- **SIC:** 3571 — Electronic Computers
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/OMCL

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** OMNICELL, INC.
- **CIK:** 926,326 · **SIC:** 3571 (Electronic Computers) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:ConvertibleLongTermNotesPayable

**Valuation**

| metric | value |
|---|---|
| price | 34.82 |
| mktcap | $1.6B |
| ev | $1.5B |
| ev_ebit | 283.8x |
| fcf | $86.9M |
| fcf_yield | 5.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 0.3% |
| net_debt | -$124.0M |
| net_debt_ebit | -24.0x |
| cash | $292.2M |
| ltd | $168.2M |
| equity | $1.3B |
| ltd_tag | ConvertibleLongTermNotesPayable |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.2B |
| revenue_prior | $1.1B |
| rev_growth | 6.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $5.2M |
| net_income | $2.1M |
| cfo | $127.3M |
| capex | $40.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 45,614,884 |
| shares_py | 45,934,251 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 13.3% |
| r6m | -17.6% |
| off_52w_high | -32.2% |
| adv20 | $23.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.52 |
| r_ev_ebit | 0.02 |
| r_roic | 0.31 |
| r_rev_growth | 0.56 |
| r_buyback | 0.73 |
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
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 266 |

**Screen rationale:** net cash; 12-1 momentum 13.3%


## 3. Share count trend

- Shares outstanding: **45,614,884** (CY2026Q2I) vs **45,934,251** prior year (CY2025Q2I)
- Change: **-0.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-01** — Item 5.02 (Departure of Directors or Certain Officers; Election): of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.
- **2026-05-26** — Item 5.02 (Departure of Directors or Certain Officers; Election): of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 13,083 sh / $583,609 -> net $-583,609 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 7 |
| F | 4 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'Updates full year 2026 guidance'; skipped 11 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (exhibit991q2-26.htm)

Updates full year 2026 guidance

FORT WORTH, Texas -- July 30, 2026 -- Omnicell, Inc. (NASDAQ:OMCL) ("Omnicell," "we," "our," or the "Company"), a leading healthcare technology provider focused on empowering autonomous medication management, today reported financial results for the second quarter ended June 30, 2026.

Second quarter results reflected continued execution across the business, supported by demand for Omnicell's connected device portfolio, growth in technical services and SaaS-related offerings, and disciplined cost management. Our business performed well during the quarter, with quarterly revenue coming in at the high end of our expectations, and we continue to see healthcare providers prioritize solutions that are designed to improve operational efficiency, optimize medication workflows, and help address ongoing workforce challenges.

"We delivered solid second quarter results and continued to execute against our strategic priorities," said Randall A. Lipps, chairman, chief executive officer, and founder of Omnicell. "We believe our performance reflects the strength of our diversified business model, the resilience of demand across our core medication management solutions, and our ongoing focus on operational discipline. We also remain confident in the long-term opportunities we see ahead of us and continue to see strong customer interest in solutions that are built to help health systems improve efficiency, safety, and workforce productivity."

"We also recently announced the promotion of Nnamdi Njoku to President and Chief Operating Officer, reflecting his leadership in advancing our operational priorities and strategic initiatives, while continuing to expand customer engagement around Omnicell Titan XT and OmniSphere," Lipps added. "As health systems increasingly seek enterprise-wide visibility, automation, and intelligence across medication workflows, we believe our next-generation platform positions us well to support those needs. We remain focused on customer success, disciplined execution, and creating long-term value for customers and stockholders."

Financial Results

Total revenues for the second quarter of 2026 were $312 million, up $22 million, or 7%, from the second quarter of 2025. The year-over-year increase in total revenues was driven by steady execution across our connected devices portfolio across both North America and international markets, as well as increases in SaaS and Expert Services and technical services revenues.

Total GAAP net income for the second quarter of 2026 was $24 million, or $0.52 per diluted share. This compares to GAAP net income of $6 million, or $0.12 per diluted share, for the second quarter of 2025.

Total non-GAAP net income for the second quarter of 2026 was $44 million, or $0.94 per diluted share. This compares to non-GAAP net income of $21 million, or $0.45 per diluted share, for the second quarter of 2025.

Total non-GAAP EBITDA for the second quarter of 2026 was $67 million. This compares to non-GAAP EBITDA of $38 million for the second quarter of 2025.

During the quarter ended June 30, 2026, the Company received $15 million in refunds for previously paid IEEPA tariffs. This amount primarily reduced the cost of product revenues and total cost of revenues in the second quarter of 2026, and also increased the GAAP net income, non-GAAP net income, non-GAAP EBITDA, and cash flows in the period.

Balance Sheet

As of June 30, 2026, Omnicell's balance sheet reflected cash and cash equivalents of $292 million, total debt (net of unamortized debt issuance costs) of $168 million, and total assets of $2.0 billion. Cash flows provided by operating activities in the second quarter of 2026 totaled $68 million. This compares to cash flows provided by operating activities totaling $43 million in the second quarter of 2025.

As of June 30, 2026, the Company had $350 million of availability under its revolving credit facility with no outstanding balance.

Corporate Highlights

• On July 1, 2026, Nnamdi Njoku was named President and Chief Operating Officer of Omnicell. In this role, Mr. Njoku will shape and advance Omnicell's long-term growth strategy and innovation roadmap, focused on scaling global operations while seeking to ensure seamless operational execution and excellence across product, innovation, and customer experience. Randall Lipps will continue to serve as Chief Executive Officer and Chairman of the Board, with a continued focus on strategic collaborations and the long-term evolution of Omnicell's solution portfolio.

• Omnicell has added two new executive roles to support long-term growth and innovation. Rick Couldry has joined in the newly created position of Senior Vice President, Chief Pharmacy and Clinical Officer, bringing more than 30 years of hospital pharmacy leadership experience to help ensure Omnicell's solutions address real-world clinical and operational needs. Dan Mandoli, a seasoned healthcare executive with deep expertise in pharmacy operations and specialty pharmacy services, was named Senior Vice President and General Manager, Specialty Pharmacy Services. Mr. Mandoli will lead the expansion of specialty pharmacy and 340B capabilities focused on strengthening customer value and supporting the Company's long-term growth strategy.

2026 Guidance

The table below summarizes Omnicell's third quarter and updated full year 2026 guidance. Given our strong second quarter 2026 profitability performance and continued focus on disciplined execution, we are increasing our full year 2026 non-GAAP EBITDA and non-GAAP earnings per share guidance ranges. In addition, as we are through the first half of the year, we are tightening our full year 2026 revenues guidance ranges. We are also updating our product bookings guidance to reflect our current assessment of the range of potential outcomes for full year 2026 and our annual recurring revenue guidance to reflect certain growth opportunities that we now expect will take longer to develop than previously projected.

Q3 2026 | 2026
Product Bookings | Not provided | $425 million - $560 million
Annual Recurring Revenue | Not provided | $660 million - $680 million
Total Revenues | $301 million - $307 million | $1.225 billion - $1.245 billion
Product Revenues | $169 million - $172 million | $690 million - $700 million
Service Revenues | $132 million - $135 million | $535 million - $545 million
Technical Services Revenues | Not provided | $267 million - $272 million
SaaS and Expert Service Revenues | Not provided | $268 million - $273 million
Non-GAAP EBITDA | $32 million - $37 million | $175 million - $185 million
Non-GAAP Earnings Per Share | $0.35 - $0.43 | $2.15 - $2.30

The Company does not provide guidance for GAAP net income or GAAP earnings per share, nor a reconciliation of any forward-looking non-GAAP financial measures to the most directly comparable GAAP financial measures on a forward-looking basis because it is unable to predict certain items contained in the GAAP measures without unreasonable efforts. These forward-looking non-GAAP financial measures do not include certain items, which may be significant, including, but not limited to, unusual gains and losses, costs associated with future restructurings, acquisition-related expenses, and certain tax and litigation outcomes.

Omnicell Conference Call Information

Omnicell will hold a conference call today, Thursday, July 30, 2026, at 8:30 a.m. ET to discuss second quarter 2026 financial results. The conference call can be monitored by dialing (833) 461-5787 in the U.S. or (585) 542-9983 in international locations. The Conference ID is 656119963. A link to the live and archived webcast will also be available on the Investor Relations section of Omnicell's website at https://ir.omnicell.com/events-and-presentations/.

About Omnicell

Since 1992, Omnicell has been committed to delivering innovative, outcomes-centric pharmacy and nursing solutions for all settings of care. As an intelligent medication management technology company, Omnicell empowers autonomous medication management by unifying automation and AI-enabled intelligence, optimized by expert services, to drive clinical and business outcomes that improve efficiency and enhance patient safety for healthcare facilities worldwide. Learn more at omnicell.com.

From time to time, Omnicell may use the Company's investor relations website and other online social media channels, including its LinkedIn page www.linkedin.com/company/omnicell, and Facebook page www.facebook.com/omnicellinc, to disclose material non-public information and comply with its disclosure obligations under Regulation Fair Disclosure ("Reg FD").

OMNICELL and the Omnicell logo are registered trademarks of Omnicell, Inc. or one of its subsidiaries. This press release may also include the trademarks and service marks of other companies. Such trademarks and service marks are the marks of their respective owners.

d) Amortization of debt issuance costs. Debt issuance costs represent costs associated with the issuance of revolving credit facilities and convertible senior notes. The costs include underwriting fees, original issue discount, ticking fees, and legal fees. These non-cash expenses are not considered by management to reflect the core cash-generating performance of the business and therefore are excluded from our non-GAAP results.

e) Legal and regulatory expenses. We excluded from our non-GAAP results certain non-recurring legal and regulatory expenses, representing settlement amounts, related to certain claims of non-compliance with our government contracts that are outside of the ordinary course of our business. We believe that excluding these amounts provides more meaningful comparisons of the financial results to our historical operations and forward-looking guidance, and to the financial results of peer companies.

f) Management severance costs. We excluded from our non-GAAP results the severance expense of certain senior management associated with the restructuring of our senior leadership team. We believe that excluding these expenses provides more meaningful comparisons of the financial results to our historical operations and forward-looking guidance, and to the financial results of peer companies.

g) Executives transition costs. We excluded from our non-GAAP results the transition costs associated with the departure of a certain executive officer, primarily consisting of severance expenses. These expenses are unrelated to our ongoing operations and we do not expect them to occur in the ordinary course of business. We believe that excluding these expenses provides more meaningful comparisons of the financial results to our historical operations and forward-looking guidance, and to the financial results of peer companies.

h) Professional Services restructuring costs. We excluded from our non-GAAP results nonrecurring restructuring charges related to organizational and resource adjustments within Professional Services to improve scalability and better align with evolving customer needs. These expenses are unrelated to our ongoing operations and we believe that excluding these expenses provides more meaningful comparisons of the financial results to our historical operations and forward-looking guidance, and to the financial results of peer companies.

i) Product organization restructuring costs. We excluded from our non-GAAP results the nonrecurring charges related to the restructuring of the product organization to better align teams, resources, and priorities with our strategic goals and future growth plans. These charges consisted primarily of severance and other related expenses. We believe that excluding these expenses provides more meaningful comparisons of the financial results to our historical operations and forward-looking guidance, and to the financial results of peer companies.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

OVERVIEW

Our Business

Omnicell, a leading healthcare technology provider focused on empowering autonomous medication management, is committed to solving the critical challenges inherent in medication management and elevating the role of clinicians within healthcare as an essential component of care delivery. Omnicell is focused on helping its customers define and deliver a cost-effective medication management strategy designed to equip and empower pharmacists and nurses to focus on patient care rather than administrative tasks, and to drive improved clinical, operational, and financial outcomes across all care settings. We are doing this with an industry-leading medication management infrastructure which includes storage and dispensing automation powered by an intelligence ecosystem. Our comprehensive set of solutions provides the critical foundation for customers to realize the Autonomous Pharmacy, an industry-wide vision defined by pharmacy leaders for improving operational efficiencies and ultimately targeting zero-error medication management alongside 5 other outcomes laid out in the Autonomous Pharmacy framework.

Omnicell solutions are helping healthcare facilities worldwide to uncover cost savings, improve labor efficiency, establish new revenue streams, enhance supply chain control, support compliance, and move closer to the industry-defined vision of the Autonomous Pharmacy. We sell our hardware, software, and consumable solutions together with related service offerings. Revenues generated in the United States represented 90% of our total revenues for the year ended December 31, 2025.

Our business has expanded from a single-point solution to a platform of products and services that will help further advance the industry-defined vision of the Autonomous Pharmacy. This expansion has resulted in larger deal sizes across multiple products, services, and implementations for customers and, we believe, more comprehensive, valuable, and enduring relationships. As our business evolves, we continue to evaluate the metrics and methods we use to measure the success of our business.

Global Trade Relations

In recent years, the U.S. government has advocated for greater restrictions on trade generally. For example, in 2025, the U.S. imposed tariffs on a wide variety of products manufactured in multiple foreign jurisdictions, including China, Mexico, and Malaysia. In response to the ongoing changes in tariffs, several foreign countries have imposed reciprocal tariffs on goods manufactured in the United States. These tariff rates have fluctuated and may continue to fluctuate going forward. In an effort to address these actions, we have implemented various mitigation measures, including dual-sourcing of components and nearshoring manufacturing. While these actions have effectively mitigated some of the impact of these costs, there can be no assurance that we will be able to offset future increased costs or other adverse impacts. Although we continue to work to mitigate the impact of current or potential tariffs, we may incorrectly anticipate outcomes, forgo or pass up business opportunities, or fail to appropriately adapt or manage our business strategies in response to these changes. As a result of these factors , we may experience direct and indirect adverse effects on our business, operating results, cash flow, or financial condition.

In addition, on February 20, 2026, the U.S. Supreme Court struck down certain tariffs imposed under the International Emergency Powers Act. It is unclear at this time what impact this decision will have on our business or future operating results, including whether we will be able to obtain refunds of amounts previously collected for such tariffs or the level of replacement tariffs the current U.S. Administration may impose through other means.

Product Bookings and Annual Recurring Revenue

We utilize product bookings and Annual Recurring Revenue ("ARR"), each as further described below, as key performance metrics for our business. We view product bookings as an indicator of the success of certain portions of our business that generate nonrecurring revenue and we view ARR as an indicator of the success of the portions of our business that generate recurring revenues. The definitions and descriptions included below are relevant to these key performance metrics.

Product Bookings

We utilize product bookings as an indicator of the success of certain portions of our business that generate non-recurring revenue. We define product bookings generally as the value of non-cancelable contracts for our connected devices and software licenses. We typically exclude freight revenue and other less significant items ancillary to our products from product bookings. In addition, dependent upon counterparty or credit risk, which is evaluated at the time of contract signing, for a given multi-year subscription contract we may reduce the value of the contractual commitment booked at a given time. Connected devices and software license bookings are recorded as revenue upon customer acceptance of the installation or receipt of goods. As part of most connected device product sales, we generally provide installation planning and consulting, which is typically included in the initial price of the solution. Product bookings were $535 million and $558 million during the years ended December 31, 2025 and 2024, respectively.

Annual Recurring Revenue

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

RESULTS OF OPERATIONS

Total Revenues

Year Ended December 31, | Change in
2025 | 2024 | %
(Dollars in thousands)
Product revenues | 665,697 | 630,507 | 35,190 | 6%
Percentage of total revenues | 56% | 57%
Service revenues | 519,148 | 481,731 | 37,417 | 8%
Percentage of total revenues | 44% | 43%
Total revenues | 1,184,845 | 1,112,238 | 72,607 | 7%

Product revenues represented 56% and 57% of total revenues for the years ended December 31, 2025 and 2024, respectively. Product revenues increased by $35.2 million, primarily due to the increase in revenues from our XTExtend offering, partially offset by lower volumes from our XT Series automated dispensing systems business due to the timing of our XT Series systems lifecycle, as we are largely through the replacement cycle, as well as the decrease in revenues from products related to our Central Pharmacy Dispensing Service offering.

Service revenues represented 44% and 43% of total revenues for the years ended December 31, 2025 and 2024, respectively. Service revenues include revenues from technical services and SaaS and Expert Services offerings. Service revenues increased by $37.4 million, due to an increase of $21.9 million in technical services revenues primarily as a result of growth in our installed customer base and the impact of pricing actions. The increase is also driven by an increase of $15.6 million in SaaS and Expert Services revenues due to continued customer demand, including an increase in revenues from our Specialty Pharmacy Services offering, partially offset by lower revenues from the EnlivenHealth portfolio.

Our international sales represented 10% and 9% of total revenues for the years ended December 31, 2025 and 2024, respectively. In future periods, we expect our revenues to be affected by foreign currency exchange rate fluctuations. We are unable to predict the extent to which revenues in future periods will be impacted by changes in foreign currency exchange rates.

Our ability to grow product and service revenues is dependent on our ability to continue to obtain orders from customers, including contract renewals, which may be dependent upon customers' capital equipment budgets and/or capital equipment approval cycles, our ability to produce quality products and consumables to fulfill customer demand, the volume of implementations we are able to complete, our ability to meet customer needs by providing a quality implementation experience and solutions that meet expected service levels, our ability to develop new or enhance existing solutions, and our flexibility in workforce allocations among customers to complete implementations on a timely basis. The timing of our revenues is primarily dependent on when our customers' schedules and/or staffing levels allow for implementations.

Cost of Revenues and Gross Profit

Cost of revenues is primarily comprised of three general categories: (i) standard product costs which account for the majority of the product cost of revenues that are provided to customers, and are inclusive of purchased material, labor to build the product, and overhead costs associated with production; (ii) costs of providing services and installation costs, including costs of personnel and other expenses; and (iii) other costs, including variances in standard costs and overhead, scrap costs, rework, provisions for excess and obsolete inventory, and amortization of software development costs and intangibles.

Year Ended December 31, | Change in
2025 | 2024 | %
(Dollars in thousands)
Cost of revenues:
Cost of product revenues | 379,162 | 383,025 | (3,863) | (1)%
As a percentage of related revenues | 57% | 61%
Cost of service revenues | 302,241 | 258,210 | 44,031 | 17%
As a percentage of related revenues | 58% | 54%
Total cost of revenues | 681,403 | 641,235 | 40,168 | 6%
As a percentage of total revenues | 58% | 58%
Gross profit | 503,442 | 471,003 | 32,439 | 7%
Gross margin | 42% | 42%

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

ITEM 1. BUSINESS

Overview

Omnicell, a leading healthcare technology provider focused on empowering autonomous medication management, is committed to solving the critical challenges inherent in medication management and elevating the role of clinicians within healthcare as an essential component of care delivery. Omnicell is focused on helping its customers define and deliver a cost-effective medication management strategy designed to equip and empower pharmacists and nurses to focus on patient care rather than administrative tasks, and to drive improved clinical, operational, and financial outcomes across all care settings. We are doing this with an industry-leading medication management infrastructure which includes storage and dispensing automation powered by an intelligence ecosystem. Our comprehensive set of solutions provides the critical foundation for customers to realize the Autonomous Pharmacy, an industry-wide vision defined by pharmacy leaders for improving operational efficiencies and ultimately targeting zero-error medication management alongside 5 other outcomes laid out in the Autonomous Pharmacy framework.

Business Strategy

In 2024, the United States spent $806 billion on prescription drugs, a 10.2% increase from 2023. We believe there are significant challenges facing the practice of pharmacy today. These challenges include, but are not limited to, budget constraints and acute workforce shortages, where 88% of hospitals report technician deficits and 92% lack sufficient sterile compounding expertise. In addition, health systems face rising liability related to drug diversion, with a 61% increase in the average number of investigations per hospital since the beginning of 2023. We also recognize that these challenges may impact the timing of contracting for, or implementation of, our products, solutions, or services. However, we believe that over time these significant challenges facing pharmacists will drive demand for increased automation, visibility, insights, and improved medication management outcomes that our solutions are designed to enable. Because of this, we believe that our solutions are well-positioned to address the evolving needs of healthcare institutions and therefore present opportunities for long-term growth.

In an effort to address these challenges and deliver solutions to help drive positive medication management outcomes, we continue to make significant investments in our research and development efforts to further advance the industry-defined vision of the Autonomous Pharmacy. Furthermore, we believe a combination of dispensing automation and an intelligence ecosystem is needed in every care setting where medications are managed. We are focused on delivering solutions to help our customers realize the industry-defined vision of the Autonomous Pharmacy and driving positive medication management outcomes with superior customer experience in two core market categories through:

• Hospital and Health System Solutions: This category enables the end-to-end medication process across the entire continuum of care. It unifies Central Pharmacy automation, robotics, and IV sterile compounding with Point of Care automated dispensing in Nursing Units and Operating Room/Procedural areas. From the loading dock to the bedside, this is designed to provide for medication safety, availability, and workflow efficiency. This category also supports Consolidated Pharmacy Service Center operations.

• Points of Care. As a market leader, we anticipate continued expansion into this product market as customers increasingly utilize our dispensing systems in more areas within hospitals and ambulatory care settings. The 2025–2028 healthcare landscape, however, faces significant fiscal headwinds driven by sweeping changes in health policy, specifically the One Big Beautiful Bill Act ("OBBBA"), which is expected to result in a $910 billion Medicaid spending reduction across states. Coupled with rising input costs from tariffs and acute labor shortages, these pressures are likely to further compress operating margins. We believe this financial strain makes the status quo unsustainable, which we anticipate compelling health systems to focus on capital efficiency and operational resilience through accelerated investments in pharmacy modernization, especially automation to address labor shortages and advanced analytics to manage rising costs of drug diversion and non-adherence. As hospitals navigate this liquidity challenge, we expect a critical shift in purchasing behavior from traditional capital expenditures to flexible payment models, such as leasing, subscriptions, and "as-a-service" structures, enabling institutions to adopt essential regulatory compliance and safety technologies while preserving operating cash flow.

• Central Pharmacy. This market represents the beginning of medication management in acute care settings. Given the current environment, we believe there is a significant opportunity for automation as many health systems aim to eliminate manual, repetitive, and error-prone processes to address acute workforce shortages. With hospitals facing technician shortages and often lacking adequate sterile compounding expertise, we think automating central pharmacy dispensing and compounding is crucial for reallocating limited labor, enhancing patient safety, and enabling compliance with the new Drug Supply Chain Security Act ("DSCSA")

requirements. Manual compounding of sterile IV preparations poses safety risks and, when outsourced, can increase costs and supply volatility. Therefore, IV automation offers a key opportunity to standardize sterile workflows, offset the resources currently used for managing drug shortages, and reduce the annual cost of non-optimized medication therapy. We expect these technology-driven services to become increasingly vital as health systems focus on operational resilience amid severe financial pressures.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-07-30_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
