# Triage pack — COUR · Coursera, Inc.

_Generated 2026-09-05 02:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** COUR · **Name:** Coursera, Inc.
- **CIK:** 0001651562
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/COUR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Coursera, Inc.
- **CIK:** 1,651,562 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 6.01 |
| mktcap | $1.6B |
| ev | $717.3M |
| ev_ebit | n/a |
| fcf | $107.2M |
| fcf_yield | 6.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -20.7% |
| net_debt | -$871.7M |
| net_debt_ebit | n/a |
| cash | $871.7M |
| ltd | $0.00 |
| equity | $1.2B |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $757.5M |
| revenue_prior | $694.7M |
| rev_growth | 9.0% |
| rev_growth_note | share count +61.5% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$77.4M |
| net_income | -$51.0M |
| cfo | $108.7M |
| capex | $1.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 61.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 264,400,000 |
| shares_py | 163,700,000 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -47.9% |
| r6m | -2.6% |
| off_52w_high | -50.2% |
| adv20 | $25.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.57 |
| r_ev_ebit | 0.00 |
| r_roic | 0.06 |
| r_rev_growth | 0.63 |
| r_buyback | 0.03 |
| score | 0.26 |

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
| rank | 438 |

**Screen rationale:** share count +61.5% yoy — growth may be acquisition/issuance-driven, not organic; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **264,400,000** (CY2026Q2I) vs **163,700,000** prior year (CY2025Q2I)
- Change: **61.5%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +61.5% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 1,930,511 sh / $10,203,399 -> net $-10,203,399 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 24 (open-market buys 0, sales 11).

| code | rows |
|---|---|
| A | 8 |
| F | 5 |
| S | 11 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'Coursera Reports Second Quarter 2026 Financial Results'; skipped 24 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (cour-20260630xexx991.htm)

Coursera Reports Second Quarter 2026 Financial Results

• Delivered second quarter revenue of $299 million and increased full year 2026 revenue outlook to range of $1.220 billion to $1.245 billion

• Now expects to achieve at least $85 million of annual run-rate net synergies by the end of 2026, reflecting accelerated integration execution

• Announced a $100 million strategic investment in LearnVector, a newly formed AI-native learning company founded by Andrew Ng, designed to accelerate Coursera's AI strategy and product innovation

• Repurchased $90 million of shares in the second quarter and more than $140 million to date under the $500 million share repurchase authorization

MOUNTAIN VIEW, Calif. (BUSINESS WIRE) – Coursera, Inc. (NYSE: COUR), a leading global online learning platform, today announced financial results for its second quarter ended June 30, 2026. A shareholder letter with additional discussion of the Company's performance and outlook has been posted to the Investor Relations website at investor.coursera.com.

"Q2 marked an important milestone in Coursera's next chapter of value creation. We closed the Udemy transaction, began operating as a combined company, and now expect to achieve at least $85 million of annual run-rate net synergies by the end of 2026, positioning us to finish the year with a meaningfully stronger financial profile," said Greg Hart, Coursera CEO. "Together, the scale, skills intelligence, and innovation capacity of Coursera and Udemy give us the foundation to build a unified, next-generation platform, while our strategic investment in LearnVector accelerates the creation of more personalized, adaptive, and measurable AI-native learning experiences. By putting AI in service of human development, we are positioning Coursera to help learners and organizations achieve the trusted skills outcomes needed to meet one of the defining workforce challenges of our time."

Key Financial Results

($ millions, except per share data, unaudited) | Three Months Ended June 30,
2026 | 2025 | YoY Change
GAAP Financial Measures
Revenue | 298.6 | 187.1 | 60 | %
Gross profit | 173.4 | 102.7 | 69 | %
Gross profit margin | 58.1 | % | 54.9 | % | 320 bps
Net loss | (80.4) | (7.8) | (931) | %
Net loss per share | (0.34) | (0.05) | (580) | %
Net loss margin | (26.9) | % | (4.2) | % | (2270) bps
Net cash (used in) provided by operating activities (1) | (19.8) | 35.5 | (156) | %
Non-GAAP Financial Measures
Gross profit | 185.8 | 104.7 | 77 | %
Gross profit margin | 62.2 | % | 56.0 | % | 620 bps
Net income | 40.4 | 19.3 | 109 | %
Net income per share | 0.17 | 0.12 | 42 | %
Adjusted EBITDA | 42.7 | 18.0 | 137 | %
Adjusted EBITDA Margin | 14.3 | % | 9.6 | % | 470 bps
Free Cash Flow (1) | (32.6) | 28.6 | (214) | %

(1) Net cash (used in) provided by operating activities includes cash payments of merger and integration related costs of $39.1 million and cash payments of merger-related personnel and severance costs of $18.1 million made during the three months ended June 30, 2026. There were no related cash payments made in the three months ended June 30, 2025.

Earnings Release Q2 2026

For more information regarding the non-GAAP financial measures discussed in this press release, please see "Non-GAAP Financial Measures" and "Reconciliation of GAAP to Non-GAAP Financial Measures" below.

Segment Results

($ millions, unaudited) | Three Months Ended June 30,
2026 | 2025 | YoY Change
Enterprise revenue | 140.0 | 64.3 | 118 | %
Enterprise gross profit | 111.0 | 44.8 | 148 | %
Enterprise gross profit margin | 79.3 | % | 69.7 | % | 960 bps
Consumer revenue | 158.6 | 122.8 | 29 | %
Consumer gross profit | 103.2 | 75.3 | 37 | %
Consumer gross profit margin | 65.1 | % | 61.3 | % | 380 bps

Key Business Metrics (1)
Three Months Ended June 30,
2026 | 2025 | YoY Change
Net Retention Rate for Enterprise Customers (2) | 91 | % | 95 | % | (4) | %

June 30,
2026 | 2025 | YoY Change
Enterprise Customers (3) | 12,107 | 12,325 | (2) | %
Paid Subscribers ( in thousands ) | 1,655 | 1,152 | 44 | %

(1) Key Business Metrics presented above represent the combined metrics of Coursera and Udemy, reflecting a unified reporting methodology. Historical combined metrics have been conformed to this unified reporting methodology for comparability purposes, and, therefore, may not equal the sum of each company's previously reported metrics or be comparable to the financial information presented in this press release, which reflects the completion of the Udemy transaction on May 11, 2026 and incorporates Udemy ' s operating results from the date of acquisition. For more information regarding the metrics discussed in this press release, please see "Key Business Metrics Definitions " below.

(2) On a standalone basis for the three months ended June 30, 2025, Coursera reported Net Retention Rate of 93% and Udemy reported Net Dollar Retention Rate of 95%. These legacy as-reported figures were calculated using each respective company's pre-merger defined reporting methodology and are provided solely for historical reference.

(3) On a standalone basis Coursera reported 1,686 Paid Enterprise Customers and Udemy reported 17,107 Udemy Business Customers as of June 30, 2025. These legacy as-reported figures were calculated using each respective company's pre-merger defined reporting methodology and are provided solely for historical reference.

Financial Outlook

Our guidance reflects the completion of the Udemy transaction on May 11, 2026 and incorporates Udemy's operating results from the date of acquisition. Guidance also reflects the expected pace of synergy realization during 2026, and therefore only a portion of the annual run-rate benefit is expected to be reflected in reported 2026 results.

• Third quarter 2026:

◦ Revenue in the range of $364 million to $372 million

◦ Adjusted EBITDA in the range of $52 million to $56 million

• Full year 2026:

◦ Revenue in the range of $1.220 billion to $1.245 billion

◦ Adjusted EBITDA Margin target increased to approximately 14%

Earnings Release Q2 2026

On July 28, 2026, Coursera announced a $100 million strategic investment in LearnVector, a new AI-native learning company founded and led by Andrew Ng, Coursera's co-founder and Chairman and one of the world's most influential figures in AI. LearnVector aims to put AI agents to work for human development by creating more personalized, one-to-one learning experiences that adapt to each learner and address the growing need for continuous, trusted skills development. Building on the expanded scale, skills intelligence, and innovation capacity created by the Udemy combination, the investment is intended to accelerate Coursera's AI strategy as the Company advances a unified, next-generation platform. The parties are exploring potential commercial collaborations, with updates for learners, customers, instructors, and partners to be shared over time on the Coursera Blog at https://blog.coursera.org.

Share repurchase

As previously announced, following the completion of the Udemy transaction, Coursera's Board of Directors approved a share repurchase program authorizing the Company to repurchase up to $500 million of its common stock. The authorization reflects leadership's confidence in the Company's strengthened financial profile following the Udemy transaction, expected future cash generation, and the ability to both invest in strategic growth initiatives and opportunistically return capital to shareholders.

During the second quarter of 2026, Coursera repurchased approximately 16.5 million shares of its common stock for $90.3 million, including commissions, at an average price of $5.45 per share. As of July 28, 2026, the Company had repurchased approximately $140 million under the program.

Transaction with Udemy

On May 11, 2026, Coursera completed its previously announced all-stock combination with Udemy, Inc. As a result, Coursera's financial results for the second quarter of 2026 incorporate Udemy's operating results from the date of acquisition. Additional information regarding the transaction is available in the Company's filings with the Securities and Exchange Commission.

Conference Call Details

As previously announced, Coursera will hold a conference call to discuss its second quarter 2026 performance today, July 29, 2026, at 2:00 p.m. Pacific Time (5:00 p.m. Eastern Time).

A live audio webcast of the conference call and accompanying earnings materials will be available to the public on our investor relations page at investor.coursera.com. For those unable to listen to the broadcast live, an archived replay will be accessible in the same location for one year.

Disclosure Information

In compliance with disclosure obligations under Regulation FD, Coursera announces material information to the public through a variety of means, including filings with the Securities and Exchange Commission ("SEC"), press releases, company blog posts, public conference calls, and webcasts, as well as via Coursera's investor relations website.

Earnings Release Q2 2026

About Coursera

Coursera was launched in 2012 by Andrew Ng and Daphne Koller with a mission to provide universal access to world-class learning. Coursera partners with leading university and industry partners to offer a broad catalog of content and credentials, including courses, Specializations, Professional Certificates, and degrees. Coursera's platform innovations — including AI-powered personalized guide and features, like Role Play and Course Builder, and role-based solutions like Skills Tracks — enable instructors, partners, and companies to deliver scalable, personalized, and verified learning. Institutions worldwide rely on Coursera to upskill and reskill their employees, students, and citizens in high-demand fields such as GenAI, data science, technology, and business, while learners globally turn to Coursera to master the skills they need to advance their careers. Coursera is a Delaware public benefit corporation and a B Corp. Coursera recently combined with Udemy to create one of the world's most comprehensive skills development platforms.

Contacts

For investors : Cam Carey, ir@coursera.org

For media : Arunav Sinha, press@coursera.org

# # #

Key Business Metrics Definitions

Enterprise Customers

We count the total number of Enterprise Customers that are active on the Coursera or Udemy platforms at the end of each period. For purposes of determining our customer count, we treat each customer account that has a corresponding contract as a unique customer, and a single organization with multiple divisions, segments, or subsidiaries may be counted as multiple customers. We define an "Enterprise Customer" as a customer who purchases Coursera or Udemy solutions via our direct sales force or through reseller and channel partnerships. For purposes of determining our Enterprise Customer count, we exclude customers who do not purchase either via our direct sales force or through reseller and channel partnerships, including organizations engaging through our self service platforms.

Net Retention Rate ("NRR") for Enterprise Customers

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-23_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Coursera operates a global online learning platform that connects an ecosystem of learners, content creators, organizations, and institutions. The platform offers high-quality educational content, credentials, and learning tools to support skills development and career advancement.

We partner with over 375 content creators, including universities and industry organizations, to create and distribute educational content that is modular, flexible, and affordable. As of December 31, 2025, the platform had approximately 197 million cumulative Registered Learners.

Coursera offers a range of learning products to meet diverse educational and professional development needs, including Guided Projects, industry micro-credentials, and accredited degree programs. We continue to invest in platform capabilities to enhance and scale the delivery of online education. Recent innovations include generative AI-powered features such as Coach, Role Play, and Course Builder, as well as role-based solutions like Skills Tracks. These tools enable content creators and institutions to deliver targeted learning aligned with evolving workforce needs. Organizations across the public and private sectors use Coursera to upskill and reskill employees, students, and citizens in fields such as generative AI, data science, technology, and business.

Coursera serves individual learners and institutional customers through two operating segments: Consumer and Enterprise. The Consumer segment focuses on attracting learners via branded content, institutional partnerships, and digital marketing, supported by personalized discovery and localized recommendations. The Enterprise segment engages employers, academic institutions, and government organizations through a direct sales team, as well as data-driven insights derived from activity on the Consumer platform. This approach enables Coursera to efficiently expand its reach, while delivering learning solutions and essential skills aligned with the evolving needs of both individuals and institutions.

Recent Developments

Transaction with Udemy

On December 17, 2025, we entered into an Agreement and Plan of Merger (the "Merger Agreement") to combine with Udemy, Inc., an online learning platform. Under the terms of the Merger Agreement, each issued and outstanding share of Udemy common stock would be converted into the right to receive 0.800 shares of our common stock. The Merger, which is anticipated to close by the second half of calendar year 2026, is subject to approval by Coursera and Udemy stockholders, the receipt of required regulatory approvals including the expiration or termination of the applicable waiting period under the Hart-Scott-Rodino Antitrust Improvements Act of 1976, as amended (the "HSR Act"), and other customary closing conditions. On February 9, 2026, the Federal Trade Commission granted early termination of the waiting period under the HSR Act. In the event of a termination of the Merger Agreement under certain specified circumstances, we will be required to pay Udemy a termination fee in the amount of $40.5 million.

Key Financial Results for the Year Ended 2025

• Total revenue was $757.5 million, up 9% from $694.7 million a year ago.

• Gross profit was $413.4 million, compared to $371.4 million a year ago. Non-GAAP gross profit was $421.6 million, compared to $379.6 million a year ago.

• Net loss was $(51.0) million, compared to $(79.5) million a year ago. Non-GAAP net income was $66.8 million, compared to $55.6 million a year ago.

• Net loss per share was $(0.31), compared to $(0.51) a year ago. Non-GAAP net income per share was $0.39, compared to $0.34 a year ago.

• Adjusted EBITDA was $63.5 million, compared to $41.5 million a year ago.

• Net cash provided by operating activities was $108.7 million, compared to $95.4 million a year ago. Free Cash Flow was $78.5 million, compared to $59.3 million a year ago.

The foregoing highlights mention both GAAP and non-GAAP financial measures. For definitions of our non-GAAP financial measures and why we believe they are useful, please see "Non-GAAP Financial Measures" below.

Organizational Updates and Strategic Realignment

Leadership Transitions

Effective February 3, 2025, our Board of Directors (the "Board") appointed Gregory Hart as our President, Chief Executive Officer ("CEO"), and a Class III director on our Board. Effective October 29, 2025, Kenneth Hahn resigned from his positions as Senior Vice President, Chief Financial Officer, and Treasurer, and transitioned to an advisory role for a one-year period. Our Board appointed Mr. Hart, Coursera's President, CEO, and principal executive officer, to serve as Coursera's principal financial officer, effective October 30, 2025. On November 13, 2025, the Board appointed Michael Foley to serve as Senior Vice President, Chief Financial Officer and Treasurer, and principal financial officer on an interim basis. Effective January 3, 2026, our Board also designated Mr. Foley to also serve as our principal accounting officer. For additional information, refer to Note 1, Basis of Presentation and Description of Business , and Note 11, Employee Benefit Plans , both included in the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Form 10-K and Item 9B, Other Information, included in Part II of this Form 10-K.

Reporting Segments

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table summarizes our results of operations, which are not necessarily indicative of future results.

Year Ended December 31,
2025 | 2024 | 2023
(in millions)
Revenue | 757.5 | 694.7 | 635.8
Cost of revenue (1) | 344.1 | 323.3 | 306.0
Gross profit | 413.4 | 371.4 | 329.8
Operating expenses:
Research and development (1) | 121.6 | 132.1 | 160.1
Sales and marketing (1) | 255.7 | 234.9 | 222.8
General and administrative (1) | 114.4 | 108.7 | 98.3
Restructuring related charges (1) | (0.9) | 8.9 | (5.8)
Total operating expenses | 490.8 | 484.6 | 475.4
Loss from operations | (77.4) | (113.2) | (145.6)
Interest income, net | 32.0 | 36.7 | 34.4
Other expense, net | (0.5) | (2.0) | —
Loss before income taxes | (45.9) | (78.5) | (111.2)
Income tax expense | 5.1 | 1.0 | 5.4
Net loss | (51.0) | (79.5) | (116.6)

(1) Includes stock-based compensation expense as follows:

Year Ended December 31,
2025 | 2024 | 2023
(in millions)
Cost of revenue | 2.5 | 2.7 | 2.6
Research and development | 34.8 | 41.8 | 49.9
Sales and marketing | 20.8 | 28.1 | 31.3
General and administrative | 38.6 | 35.5 | 31.4
Restructuring related charges | (1.6) | — | (5.6)
Total stock-based compensation expense | 95.1 | 108.1 | 109.6

The following table summarizes our results of operations as a percentage of revenue:

Year Ended December 31,
2025 | 2024 | 2023
Revenue | 100.0 | % | 100.0 | % | 100.0 | %
Cost of revenue | 45.4 | 46.5 | 48.1
Gross profit | 54.6 | 53.5 | 51.9
Operating expenses:
Research and development | 16.1 | 19.0 | 25.2
Sales and marketing | 33.8 | 33.8 | 35.0
General and administrative | 15.0 | 15.7 | 15.5
Restructuring related charges | (0.1) | 1.3 | (0.9)
Total operating expenses | 64.8 | 69.8 | 74.8
Loss from operations | (10.2) | (16.3) | (22.9)
Other income (expense):
Interest income, net | 4.2 | 5.3 | 5.4
Other expense, net | (0.1) | (0.3) | —
Loss before income taxes | (6.1) | (11.3) | (17.5)
Income tax expense | 0.6 | 0.1 | 0.8
Net loss | (6.7) | % | (11.4) | % | (18.3) | %

Comparison of the Years Ended December 31, 2025 and 2024

Revenue

Year Ended December 31, | Change
2025 | 2024 | %
(in millions, except percentages)
Revenue:
Consumer | 502.2 | 455.8 | 46.4 | 10 | %
Enterprise | 255.3 | 238.9 | 16.4 | 7 | %
Total revenue | 757.5 | 694.7 | 62.8 | 9 | %

Revenue for the year ended December 31, 2025 was $757.5 million, an increase of $62.8 million, or 9%, compared to $694.7 million for the prior year. Revenue growth was primarily driven by an 18% increase in the average total number of Registered Learners, resulting in more paid learners, and a 10% increase in the average total number of Paid Enterprise Customers with growth supported by increased Coursera Plus subscription adoption, ongoing platform improvements, and localized pricing, payment, and promotional capabilities.

Consumer revenue for the year ended December 31, 2025 increased by $46.4 million, or 10%, compared to the prior year. This increase was primarily driven by growth in subscription revenue from Coursera Plus, partially offset by a decline in direct purchases of Specializations.

Enterprise revenue for the year ended December 31, 2025 increased by $16.4 million, or 7%, compared to the prior year, attributable to an increase in new customers. Acquisitions of new customers drove an increase of $16.7 million.

Cost of Revenue, Gross Profit, and Gross Margin

Year Ended December 31, | Change
2025 | 2024 | %
(in millions, except percentages)
Cost of revenue | 344.1 | 323.3 | 20.8 | 6 | %
Gross profit | 413.4 | 371.4 | 42.0 | 11 | %
Gross margin | 54.6 | % | 53.5 | %

Cost of revenue for the year ended December 31, 2025 was $344.1 million, compared to $323.3 million for the prior year. The primary drivers of the increase were revenue growth, which resulted in an increase of $12.3 million in content-related costs and a $4.6 million increase in amortization expense of content assets.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-23_item1_business.md)

Item 1. Business

Overview

Our mission is to provide universal access to world-class learning so that anyone, anywhere can transform their life through learning. We believe learning is a powerful source of human progress, transforming our world from illness to health, from poverty to prosperity, and from conflict to peace.

As a global platform, Coursera unites educators, learners, and institutions, serving approximately 197 million learners from over 230 countries and territories as of December 31, 2025. Our content is created by a world-class ecosystem of expert instructors, including more than 200 universities and 175 industry leaders, who have developed a broad catalog of content and credentials, ranging from entry-level industry microcredentials to university degrees. These offerings are distributed globally through our platform, making high-quality, affordable education more accessible around the world.

Coursera serves learners with educational content and product experiences designed to support skills development and verification for career advancement, including interactive learning tools and personalized learning paths. Our offerings are delivered directly through our global website, on the job through employers, and through programs sponsored by colleges, universities, and government organizations. The graphic below illustrates our global learning ecosystem as of December 31, 2025:

Technology is advancing faster than the world's ability to adapt and acquire new skills. We believe that advancements in artificial intelligence ("AI") and other emerging technologies are reshaping how we live, learn, and work, and we expect these changes will further increase the global skills gap. The rapid adoption of new technologies, tools, and processes creates an urgent need for organizations and learners to adapt in order to remain competitive. To seize the opportunities created by the digital economy, many aspiring and existing professionals need to develop, master, and validate their skills in business, technology, AI, and data science. We believe education will continue to evolve with blended classrooms powered by online learning, a focus on job-relevant skills, and lifelong learning to help people adapt and learn skills that can be used to gain employment, obtain new job opportunities, improve performance in their current jobs, or run their businesses.

We envision a future of higher education that emphasizes relevance, accessibility, and affordability, meeting the demands of a rapidly changing economy. We believe that online learning will become the primary means of meeting the global demand for emerging skills and that the adoption of online education, combined with the increased flexibility enabled by remote and hybrid workforces, holds the promise to increase global access. Cross-sector collaboration is required between employers, government organizations, and universities in order to bridge the skills gap.

World-class teaching is the foundation of the Coursera experience. Coursera provides learners with high-quality, modular content and credentials at varying skill levels, price points, and durations. Product innovation such as our AI-enabled Course Builder solution is designed to streamline content production in various formats and enable customers to personalize courses tailored to their organization's objectives. Additionally, our AI translations and dubbing initiative has led to delivering our high-quality content in up to 26 languages. By leveraging Coursera's global reach and scale supported by our platform, our content creators can effectively tap into the worldwide demand for education, reaching individual learners, organizations, and institutions around the globe.

Reaching and serving a world of learners lies at the heart of our model. We strive to make it easy for learners to discover and engage with high-quality, job-relevant learning in flexible, hands-on online learning environments at affordable prices. Content and credentials from well-recognized university and industry brands have helped us attract approximately 197 million learners cost effectively and build a global consumer audience. We use data-driven marketing to efficiently attract learners to a wide range of paid offerings, including standalone courses, multi-course specializations, industry certificate programs, and university degrees. We believe this efficient learner acquisition model has allowed us to build one of the largest global audiences of adult learners and serve these learners at various price points, with competitive margins for us and our content creators.

We expect the long, episodic nature of higher education will break down into shorter, more relevant units of consumption designed to increase affordability and provide more immediate access to workforce participation. Our model lets learners leverage flexible and affordable career and learning pathways across our catalog, including "stacking" content and credentials to count as progress towards a broader program of study. Qualifying our high-quality learning catalog for credit recognition through organizations like the American Council on Education ("ACE"), the European Credit Transfer and Accumulation System ("ECTS"), and India's National Skills Qualification Framework ("NSQF") enables this. For example, eligible learners who complete the Google Data Analytics Certificate can earn a credit recommendation of up to 12 college credits, the equivalent of four college courses at the bachelor's degree level in participating programs.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-23_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-23_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-23_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-02-23_item7_mdna.md, 10-K_2026-02-23_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
