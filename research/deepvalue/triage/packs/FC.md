# Triage pack — FC · FRANKLIN COVEY CO

_Generated 2026-09-04 15:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** FC · **Name:** FRANKLIN COVEY CO
- **CIK:** 0000886206
- **SIC:** 8741 — Services-Management Services
- **Fiscal year end (MM-DD):** 08-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/FC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** FRANKLIN COVEY CO
- **CIK:** 886,206 · **SIC:** 8741 (Services-Management Services) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 18.40 |
| mktcap | $207.8M |
| ev | $195.8M |
| ev_ebit | 34.3x |
| fcf | $20.7M |
| fcf_yield | 10.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 14.6% |
| net_debt | -$12.0M |
| net_debt_ebit | -2.1x |
| cash | $12.0M |
| ltd | $0.00 |
| equity | $42.9M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $267.1M |
| revenue_prior | $287.2M |
| rev_growth | -7.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $5.7M |
| net_income | $3.1M |
| cfo | $29.0M |
| capex | $8.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -10.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 11,293,873 |
| shares_py | 12,641,822 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 15.7% |
| r6m | 42.9% |
| off_52w_high | -28.0% |
| adv20 | $1.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.72 |
| r_ev_ebit | 0.23 |
| r_roic | 0.79 |
| r_rev_growth | 0.14 |
| r_buyback | 0.95 |
| score | 0.62 |

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
| rank | 126 |

**Screen rationale:** high ROIC 14.6%; buying back stock -10.7%; debt data missing (net cash unverified); 12-1 momentum 15.7%


## 3. Share count trend

- Shares outstanding: **11,293,873** (CY2026Q2I) vs **12,641,822** prior year (CY2025Q2I)
- Change: **-10.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-09-01** — Item 5.02 (officer / director change or comp arrangement): On September 1, 2026, Franklin Covey Co. (the "Company" or "FranklinCovey") announced the following changes to its executive leadership team.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 5 |
| F | 5 |
| G | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-01_2-02-results.md)

_Extraction: started at the first release heading, 'Third Quarter Fiscal 2026 Financial Overview'; skipped 8 forward-looking-statement block(s); 15 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (fc-ex99_1.htm)

Third Quarter Fiscal 2026 Financial Overview

The Company's consolidated revenue for Q3 FY2026 increased to $67.8 million compared with $67.1 million in Q3 FY2025. The Company's financial results for Q3 FY2026 include the following:

•
Enterprise Division revenue for Q3 FY2026 increased to $48.1 million compared with $47.3 million in the prior year.

•
Enterprise Division revenue reflected a $1.0 million increase in North America segment revenue partially offset by a $0.2 million decrease in International segment revenue. The North America segment was favorably affected by higher service revenue, partially offset by lower recognized subscription revenue.

•
Enterprise North America invoiced amounts grew 4% year-over-year.

•
Deferred revenue for the Enterprise Division increased 15% year-over-year.

•
Education Division revenue in Q3 FY2026 increased to $19.0 million compared with $18.6 million in the prior year.

•
The increase was driven by higher subscription revenue, primarily due to the delivery of more training and coaching days, partially offset by decreased materials revenue during the quarter.

•
Consolidated subscription and subscription services revenue for Q3 FY2026 was $57.5 million compared with $57.7 million in Q3 FY2025. Subscription and contractually committed services invoiced for Q3 FY2026 totaled $37.0 million, growth of 17%, compared with $31.7 million in Q3 FY2025.

•
The Company recognized net income for Q3 FY2026 of $3.1 million, or $0.27 per diluted share, compared with a net loss of $(1.4) million, or $(0.11) per share, in Q3 FY2025.

•
Adjusted EBITDA for Q3 FY2026 increased 14% to $8.3 million compared with $7.3 million in the prior year.

•
Consolidated deferred revenue at May 31, 2026 increased 7% to $96.0 million compared with $89.3 million at May 31, 2025.

•
At May 31, 2026, 59% of the Company's AAP contracts in North America were for at least two years, compared with 58% at May 31, 2025, and the percentage of contracted amounts represented by multi-year contracts was 60% compared with 62% on May 31, 2025.

•
Unbilled deferred revenue totaled $61.1 million at May 31, 2026, compared with $62.0 million at May 31, 2025.

•
Cash provided by operating activities for Q3 FY2026 was $1.1 million compared with $6.3 million in the prior year.

•
Free cash flow for Q3 FY2026 was $(1.0) million compared with $2.8 million in Q3 FY2025.

•
Cash and cash equivalents totaled $12.0 million compared with $33.7 million as of May 31, 2025.

Paul Walker, President and Chief Executive Officer commented, "We are pleased with the continued strong momentum particularly in Enterprise North America, which achieved 4% growth in invoiced amounts in the third quarter, or 6% year-to-date, and where we achieved 18% growth in our deferred revenue balance year-over-year, and over 25% growth in our year-to-date services booking pace – all of which position us well for meaningful growth in fiscal 2027. This marks our third consecutive quarter of invoiced growth in Enterprise North America, reflecting both the increasing strategic importance of what we do for our clients and the traction from the go-to-market transformation we implemented last year.

While we experienced an unexpected headwind in our Education business due to a last-minute state budget reduction that removed funding for a large state contract, the underlying strength of our business across both Enterprise North America and Education remains solid and we remain confident in our trajectory for meaningful growth in fiscal 2027 and beyond."

Jessi Betjemann, Chief Financial Officer said, "In the third quarter, we demonstrated strong operational discipline, with Adjusted EBITDA growing 14% to $8.3 million. We are pleased that our consolidated deferred revenue balance increased 7% year-over-year to $96.0 million and that our balance sheet remains strong with over $74 million in total liquidity. We are revising our fiscal 2026 revenue guidance to a range of $260 million to $267 million while maintaining our expectation to achieve Adjusted EBITDA guidance within a narrower range through continued cost discipline."

Fiscal 2026 Guidance

The Company has revised its revenue guidance to allow for a timing shift in previously invoiced services delivery from this year to next for a large contract in Enterprise North America, a large new school contract with an existing state-wide Education client that experienced gubernatorial budget reductions which we expect to return next year, and the impact of the challenging international environment due to ongoing geo-political tensions. These factors, combined with a disciplined view of the variability risk that could occur as we close the year, have led the Company to revise its revenue guidance.

The Company updates its fiscal 2026 guidance to the following, in constant currency:

•
Total revenue in the range of $260 million to $267 million, versus prior guidance of $265 million to $275 million.

•
Adjusted EBITDA in the range of $28 million to $31 million, within prior guidance of $28 million to $33 million.

Despite the revision of the revenue guidance range, the Company has maintained its prior Adjusted EBITDA guidance within a narrower range, reflecting the effectiveness of cost reduction measures implemented throughout the year. The Company believes it is well-positioned to deliver net revenue, Adjusted EBITDA, and Free Cash Flow growth in fiscal 2027 and beyond.

Earnings Conference Call

On Wednesday, July 1, 2026, at 5:00 p.m. Eastern (3:00 p.m. Mountain Time) Franklin Covey will host a conference call to review its third quarter fiscal 2026 financial results. Interested persons may access a live audio webcast at https://edge.media-server.com/mmc/p/8yjq5b3i or may participate via telephone by registering at https://register-conf.media-server.com/register/BI57ddeb8339fa49c0a62b3ff26faa5415 . Once registered, participants will have the option of 1) dialing into the call from their phone (via a personalized PIN); or 2) clicking the "Call Me" option to receive an automated call directly to their phone. For either option, registration will be required to access the call. A replay of the conference call webcast will be archived on the Company's website for at least 30 days.

FRANKLIN COVEY CO.
Condensed Consolidated Statements of Operations
(in thousands, except per-share amounts, and unaudited)
Quarter Ended | Three Quarters Ended
May 31, | May 31, | May 31, | May 31,
2026 | 2025 | 2026 | 2025
Revenue | 67,807 | 67,121 | 191,499 | 195,819
Cost of revenue | 17,710 | 15,799 | 47,755 | 46,040
Gross profit | 50,097 | 51,322 | 143,744 | 149,779
Selling, general, and administrative | 43,263 | 46,232 | 132,882 | 138,468
Restructuring costs | 696 | 4,739 | 5,650 | 6,723
Building exit costs | 143 | 444 | 1,272 | 498
Depreciation | 1,185 | 1,012 | 3,424 | 2,979
Amortization | 614 | 1,098 | 1,971 | 3,294
Income (loss) from operations | 4,196 | (2,203 | (1,455 | (2,183
Interest income (expense), net | (30 | 76 | (72 | 295
Income (loss) before income taxes | 4,166 | (2,127 | (1,527 | (1,888
Income tax benefit (provision) | (1,081 | 718 | (659 | 584
Net income (loss) | 3,085 | (1,409 | (2,186 | (1,304
Net income (loss) per common share:
Basic and diluted | 0.27 | (0.11 | (0.19 | (0.10
Weighted average common shares:
Basic | 11,260 | 12,891 | 11,630 | 13,028
Diluted | 11,451 | 12,891 | 11,630 | 13,028
Other data:
Adjusted EBITDA (1) | 8,331 | 7,307 | 16,115 | 17,041

(1) Adjusted EBITDA (earnings before interest, income taxes, depreciation, amortization, stock-based compensation, and certain other items) is a non-GAAP financial measure that the Company believes is useful to investors in evaluating its results. For a reconciliation of this non-GAAP measure to a comparable GAAP measure, refer to the Reconciliation of Net Income (Loss) to Adjusted EBITDA as shown below.

FRANKLIN COVEY CO.
Reconciliation of Net Income (Loss) to Adjusted EBITDA
(in thousands and unaudited)
Quarter Ended | Three Quarters Ended
May 31, | May 31, | May 31, | May 31,
2026 | 2025 | 2026 | 2025
Reconciliation of net income (loss) to Adjusted EBITDA:
Net income (loss) | 3,085 | (1,409 | (2,186 | (1,304
Adjustments:
Interest expense (income), net | 30 | (76 | 72 | (295
Income tax provision (benefit) | 1,081 | (718 | 659 | (584
Amortization | 614 | 1,098 | 1,971 | 3,294
Depreciation | 1,185 | 1,012 | 3,424 | 2,979
Stock-based compensation | 1,497 | 2,217 | 5,591 | 5,730
Restructuring costs | 696 | 4,739 | 5,650 | 6,723
Building exit costs | 143 | 444 | 1,272 | 498
Gain on license liability restructuring | - | - | (338 | -
Adjusted EBITDA | 8,331 | 7,307 | 16,115 | 17,041
Adjusted EBITDA margin | 12.3 | % | 10.9 | % | 8.4 | % | 8.7 | %

FRANKLIN COVEY CO.
Additional Financial Information
(in thousands and unaudited)
Quarter Ended | Three Quarters Ended
May 31, | May 31, | May 31, | May 31,
2026 | 2025 | 2026 | 2025
Revenue by Division/Segment:
Enterprise Division:
North America | 38,024 | 37,054 | 106,763 | 111,711
International | 10,052 | 10,212 | 30,410 | 30,685
48,076 | 47,266 | 137,173 | 142,396
Education Division | 18,998 | 18,640 | 52,590 | 50,169
Corporate and other | 733 | 1,215 | 1,736 | 3,254
Consolidated | 67,807 | 67,121 | 191,499 | 195,819
Gross Profit by Division/Segment:
Enterprise Division:
North America | 30,213 | 30,708 | 86,923 | 92,503
International | 7,616 | 7,869 | 23,362 | 23,905
37,829 | 38,577 | 110,285 | 116,408
Education Division | 11,936 | 12,227 | 32,620 | 31,968
Corporate and other | 332 | 518 | 839 | 1,403
Consolidated | 50,097 | 51,322 | 143,744 | 149,779
Adjusted EBITDA by Division/Segment:
Enterprise Division:
North America | 7,748 | 6,201 | 18,938 | 19,788
International | 2,073 | 1,662 | 5,533 | 3,565
9,821 | 7,863 | 24,471 | 23,353
Education Division | 1,685 | 2,053 | 1,166 | 2,006
Corporate and other | (3,175 | (2,609 | (9,522 | (8,318
Consolidated | 8,331 | 7,307 | 16,115 | 17,041

FRANKLIN COVEY CO.
Condensed Consolidated Balance Sheets
(in thousands and unaudited)
May 31, | August 31,
2026 | 2025
Assets
Current assets:
Cash and cash equivalents | 11,972 | 31,698
Accounts receivable, less allowance for
credit losses of $2,091 and $2,929 | 50,285 | 68,415
Inventories | 5,804 | 5,165
Prepaid expenses and other current assets | 23,745 | 24,199
Total current assets | 91,806 | 129,477
Property and equipment, net | 12,557 | 14,324
Intangible assets, net | 31,843 | 34,551
Goodwill | 31,220 | 31,220
Deferred income tax assets | 242 | 231
Other long-term assets | 30,342 | 33,109
198,010 | 242,912
Liabilities and Shareholders' Equity
Current liabilities:
Current portion of notes payable | - | 823
Accounts payable | 6,424 | 8,780
Deferred revenue | 92,950 | 106,534
Customer deposits | 20,027 | 16,327
Accrued liabilities | 20,728 | 24,828
Total current liabilities | 140,129 | 157,292
Other liabilities | 10,921 | 14,718
Deferred income tax liabilities | 4,024 | 3,991
Total liabilities | 155,074 | 176,001
Shareholders' equity:
Common stock | 1,353 | 1,353
Additional paid-in capital | 229,260 | 230,251
Retained earnings | 124,086 | 126,272
Accumulated other comprehensive loss | (1,170 | (1,032
Treasury stock at cost, 15,756 and 14,565 shares | (310,593 | (289,933
Total shareholders' equity | 42,936 | 66,911
198,010 | 242,912

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-11-12_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

EXECUTIVE SUMMARY

General Overview

Franklin Covey Co. is a global company focused on individual and organizational performance improvement. Our mission is to "enable greatness in people and organizations everywhere," and our worldwide resources are organized to help individuals and organizations achieve sustained superior performance at scale through changes in human behavior. We believe that our content and services create the connection between capabilities and results. In the training and consulting marketplace, we believe there are three important characteristics that distinguish us from our competitors.

1. World Class Content – Our content is based on timeless principles of human effectiveness and is designed to help people change both their mindset and behavior. When our content is applied consistently in an organization, we believe the culture of that organization will change and improve to enable the organization to get desired results and achieve its own great purposes.

2. Breadth and Scalability of Delivery Options – We have a wide range of content delivery options, including: the All Access Pass and Leader in Me membership subscriptions, coaching and consulting, organization-wide transformational processes, intellectual property licenses, digital online learning, on-site training, training led through certified facilitators, and blended learning. We believe our expert delivery consultants combined with investments in digital delivery modalities have enabled us to deliver our content to clients in a high-quality learning environment whether those clients are working remotely or in a centralized location.

3. Global Capability – We have sales professionals in the United States and Canada who serve clients in the private sector, in government, and in educational institutions; wholly owned subsidiaries that serve clients in Australia, Austria, China, France, Germany, Ireland, Japan, New Zealand, Switzerland, and the United Kingdom; and we contract with independent licensee partners who deliver our content and provide services in approximately 150 countries and territories around the world. Our capabilities allow us to serve a wide range of clients from small locally owned entities to large multinational enterprises.

We have some of the best-known offerings in the training industry, including a suite of individual-effectiveness and leadership-development training content based on the best-selling books, The 7 Habits of Highly Effective People , The Speed of Trust , Multipliers , The 4 Disciplines of Execution , and Trust & Inspire , and proprietary content in the areas of Execution, Sales Performance, Productivity, Customer Loyalty, Leadership, and Education. We believe that our offerings help individuals, teams, and entire organizations transform their results through achieving systematic, sustainable, and

measurable changes in human behavior. Our offerings are described in further detail at www.franklincovey.com . The information contained in, or that can be accessed through, our website does not constitute a part of this Annual Report on Form 10-K, and the descriptions found therein should not be viewed as a warranty or guarantee of results.

Our fiscal year ends on August 31, and unless otherwise indicated, fiscal 2025, fiscal 2024, and fiscal 2023 refer to the twelve-month periods ended August 31, 2025, 2024, 2023, and so forth.

Key Strategic Objectives

The theme of our fiscal 2026 Company kickoff was, "Deep Roots, Bold Future." Building on our enduring areas of competitive strength and the significant growth investments we made in fiscal 2025, we plan to focus on the following four strategic objectives that we intend to execute with discipline in fiscal 2026 to help us achieve our vision of helping our clients achieve their missions and strategic objectives.

 Clarify our position in the market. FranklinCovey is not just a training company. We believe we are a trusted leadership and performance partner and that our comprehensive solutions can help drive breakthroughs in performance as our clients engage leaders and teams across their organizations to move their strategies forward. In fiscal 2026, our message to potential and current clients is designed to firmly position us in this more strategic, outcomes-oriented place in the market.

 Focus and declare who we serve. In fiscal 2026 we intend to significantly increase the precision and impact of our outcome-oriented messaging to our target buyers, namely, senior executive leaders who own the responsibility for achieving strategic outcomes and who can make the spending decisions to do what it takes to achieve them. Our messaging target also includes senior, performance-oriented talent and human resource leaders who serve as internal partners to these executives inside of their organizations. As we increase the effectiveness of our messaging, we expect that we will engage with more significant clients in more strategic ways, driving better results for our clients and for FranklinCovey.

 Build and sell like a "solutions leadership" company. A solutions leadership company is differentiated by the strength of its products and services. We intend to increasingly position and package our solutions as integrated offerings that drive collective action and deliver breakthrough results for clients. Our trusted content and frameworks will be more frequently combined with consulting and technology to help clients achieve measurable outcomes at scale—enabling lasting client impact and durable growth for FranklinCovey.

‎

 Model what we teach, internally and visibly. As we pursue our growth strategy, we will heavily use and model our own methodologies and frameworks. This process includes further investments in our already strong culture to increase our ability to execute with even higher trust and accountability as we engage our own leaders and teams in achieving our own breakthrough results.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth, for the fiscal years indicated, the percentage of total sales represented by the line items through income before income taxes in our consolidated income statements. This table should be read in conjunction with the accompanying discussion and analysis, the consolidated financial statements, and the related notes to the consolidated financial statements.

YEAR ENDED
AUGUST 31, | 2025 | 2024 | 2023
Amounts shown as a percent of total revenue
Revenue | 100.0 | 100.0 | 100.0
Cost of revenue | 23.8 | 23.0 | 23.9
Gross profit | 76.2 | 77.0 | 76.1
Selling, general, and administrative | 68.4 | 61.3 | 63.4
Restructuring costs | 2.5 | 1.0 | 0.2
Impaired asset | - | 0.3 | -
Depreciation | 1.5 | 1.4 | 1.5
Amortization | 1.6 | 1.5 | 1.6
Total operating expenses | 74.0 | 65.5 | 66.7
Income from operations | 2.2 | 11.5 | 9.4
Interest income | 0.3 | 0.4 | 0.4
Interest expense | (0.2) | (0.4) | (0.6)
Income before income taxes | 2.3 | 11.5 | 9.2

FISCAL 2025 COMPARED WITH FISCAL 2024 RESULTS OF OPERATIONS

Enterprise Division

North America Segment

The North America segment includes our personnel that serve clients in the United States and Canada. The following comparative information is for our North America segment in the periods indicated (in thousands):

Fiscal Year Ended | Fiscal Year Ended
August 31, | % of | August 31, | % of
2025 | Sales | 2024 | Sales | Change
Revenue | 147,609 | 100.0 | 163,384 | 100.0 | (15,775)
Cost of revenue | 25,008 | 16.9 | 26,964 | 16.5 | (1,956)
Gross profit | 122,601 | 83.1 | 136,420 | 83.5 | (13,819)
SG&A expenses | 95,203 | 64.5 | 89,779 | 54.9 | 5,424
Adjusted EBITDA | 27,398 | 18.6 | 46,641 | 28.5 | (19,243)

Revenue. In fiscal 2025, our North America segment revenue was $147.6 million compared with $163.4 million in the prior year. North America segment revenues in fiscal 2025 were adversely impacted by the uncertain macroeconomic environment and by canceled or postponed government contracting. During fiscal 2025, North America subscription and subscription service revenues were $131.1 million compared with $138.9 million in fiscal 2024. While we remain optimistic about the future impact of our new North America go-to-market strategy and sales force restructuring, continued economic uncertainty, including threatened or enacted tariffs and continued decreases in governmental spending, including due to the U.S. federal government shutdown, may prevent us from achieving expected sales goals until these conditions stabilize or are resolved. Foreign exchange rates had a $0.2 million adverse impact on North America segment revenues and a $0.1 million adverse impact on operating results during fiscal 2025.

Gross Profit. Gross profit was impacted by lower revenue as described above. North America gross margin remained strong during fiscal 2025 and was 83.1% of revenue compared with 83.5% in the prior year.

SG&A Expense. North America SG&A expenses increased primarily due to associate costs resulting from new sales and sales support personnel primarily related to our new go-to-market strategy and the reorganization of our North America sales force in fiscal 2025.

International Direct Offices

Our directly owned international offices serve clients in Australia, Austria, China, France, Germany, Ireland, Japan, New Zealand, Switzerland, and the United Kingdom. The following comparative information is for our International Direct Office segment in the periods indicated (in thousands):

Fiscal Year Ended | Fiscal Year Ended
August 31, | % of | August 31, | % of
2025 | Sales | 2024 | Sales | Change
Revenue | 29,344 | 100.0 | 33,327 | 100.0 | (3,983)
Cost of revenue | 7,738 | 26.4 | 7,812 | 23.4 | (74)
Gross profit | 21,606 | 73.6 | 25,515 | 76.6 | (3,909)
SG&A expenses | 22,008 | 75.0 | 22,157 | 66.5 | (149)
Adjusted EBITDA | (402) | (1.4) | 3,358 | 10.1 | (3,760)

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-11-12_item1_business.md)

ITEM 1 . BUSINESS

General Information

Franklin Covey is a global company focused on organizational performance improvement. Our mission is to "enable greatness in people and organizations everywhere," and our global structure is designed to help individuals and organizations achieve results that require collective behavior change. From the foundational work of Dr. Stephen R. Covey in leadership and personal effectiveness, and Hyrum W. Smith in productivity and time management, we have developed deep expertise that extends to helping organizations and individuals achieve desired results through lasting behavioral change. We believe that our clients are able to utilize our content and offerings to create cultures which include high-performing, collaborative individuals, led by effective, trust-building leaders who execute with excellence and deliver measurably improved results for all of their key stakeholders.

The Company was incorporated in 1983 under the laws of the state of Utah, and we merged with the Covey Leadership Center in 1997 to form Franklin Covey Co. Our consolidated net revenue for the fiscal year ended August 31, 2025 totaled $267.1 million and our shares of common stock are traded on the New York Stock Exchange (NYSE) under the ticker symbol "FC."

Our fiscal year ends on August 31 of each year. Unless otherwise noted, references to fiscal years apply to the 12 months ended August 31 of the specified year.

The Company's principal executive offices are located at 13907 South Minuteman Dr., Suite 500, Draper, Utah 84020, and our telephone number is (801) 817 - 1776. Our website, where you can find information about us, is www.franklincovey.com .

‎

Franklin Covey Services and Offerings

Our mission is to "enable greatness in people and organizations everywhere." To accomplish this mission, we partner with senior executives and talent leaders to achieve breakthrough performance by engaging leaders and teams throughout an organization in focused, highly effective ways that drive their strategies forward. Our solutions are designed to transform our clients' results and bring a unique blend of technology, content, and consulting expertise to the most critical challenges they face. Our solutions are researched-backed, grounded in time-proven principles, and have been tested in thousands of implementations in business, government, and educational organizations throughout the world.

FranklinCovey solutions are delivered as a combination of subscription-based access to proprietary content, implementation tools, assessments, and expert consulting and advisory services to help clients engage and align their people around their desired outcomes. Our subscription offerings include the All Access Pass (AAP), which is primarily sold through our Enterprise Division, and the Leader in Me membership, which is designed specifically for our Education Division. These subscriptions enable clients to scale our solutions throughout their organizations and maximize the impact on their results.

We believe that our Enterprise Division's AAP is a powerful way to deliver our solutions to clients of various sizes, including large, multinational organizations. As part of their engagement, clients can deploy complete content offerings such as The 7 Habits of Highly Effective People , The Four Disciplines of Execution , The Speed of Trust , and Multipliers , or use individual concepts from any of these well-known offerings to create a custom solution to fit their organization's goals. Strategic deployments are supported by expert consultants and coaches, who work with clients to align our solutions and implementation processes in ways that maximize their impact on client results. The AAP also includes access to Franklin Covey's AI Coach, which helps individuals deepen their learning and application of our content. Our AAP-based solutions can be deployed in numerous languages, enabling multinational clients to achieve impact throughout their operations. This global capability also provides us with substantial international sales opportunities.

In our Education Division, we offer the Leader in Me membership, which provides access to the Leader in Me online service, and authorizes Education clients to use Franklin Covey's proprietary intellectual property. The Leader in Me online service provides access to digital curriculum, leadership lessons, illustrated leadership stories, and a variety of other resources to enable an educational institution to effectively implement and utilize the Leader in Me program. In addition to the content and materials, we provide experienced coaches and consultants to assist schools with the implementation of the Leader in Me program. The coaches and consultants who serve in the Education Division are primarily former educators, including teachers, principals, and administrators, who have a deep understanding of the current challenges facing educators and students and understand how the Leader in Me program can effectively address these challenges. We believe that the Leader in Me solution provides measurable results in the areas of student leadership, improved school culture, and increased academic proficiency.

Each division operates globally with a common brand and a business model designed to provide clients around the world with the same high level of service. We have sales and support associates throughout the United States and Canada, and operate wholly owned subsidiaries that serve clients in Austria, Australia, China, France, Germany, Ireland, Japan, New Zealand, Switzerland, and the United Kingdom. In foreign locations where we do not have a directly owned office, we may contract with independent licensee partners who deliver our content and provide services in approximately 150 other countries and territories around the world.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-11-12_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-11-12_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-11-12_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-01_2-02-results.md, 10-K_2025-11-12_item7_mdna.md, 10-K_2025-11-12_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
