# Triage pack — EFOR · Everforth Inc

_Generated 2026-09-04 14:13 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** EFOR · **Name:** Everforth Inc
- **CIK:** 0000890564
- **SIC:** 7363 — Services-Help Supply Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/EFOR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Everforth Inc
- **CIK:** 890,564 · **SIC:** 7363 (Services-Help Supply Services) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 31.83 |
| mktcap | $1.3B |
| ev | $2.6B |
| ev_ebit | 11.2x |
| fcf | $288.1M |
| fcf_yield | 22.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.9% |
| net_debt | $1.3B |
| net_debt_ebit | 5.6x |
| cash | $152.9M |
| ltd | $1.4B |
| equity | $1.8B |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $4.0B |
| revenue_prior | $4.1B |
| rev_growth | -2.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $230.3M |
| net_income | $113.5M |
| cfo | $327.9M |
| capex | $39.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -6.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 41,000,000 |
| shares_py | 43,800,000 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -41.0% |
| r6m | -26.2% |
| off_52w_high | -40.3% |
| adv20 | $21.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.90 |
| r_ev_ebit | 0.71 |
| r_roic | 0.55 |
| r_rev_growth | 0.24 |
| r_buyback | 0.91 |
| score | 0.66 |

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
| rank | 86 |

**Screen rationale:** top-quartile FCF yield 22.1%; buying back stock -6.4%


## 3. Share count trend

- Shares outstanding: **41,000,000** (CY2026Q2I) vs **43,800,000** prior year (CY2025Q2I)
- Change: **-6.4%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-09** — Item 1.01 (Entry into a Material Definitive Agreement): On July 7, 2026, Everforth, Inc. (the "Company") entered into the Third Amendment to its Third Amended and Restated Credit Agreement (the "Third Amendment"), by and among the Company, the lenders party thereto and Wells Fargo Bank, National Association, as...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 76,830 sh / $1,495,015 vs sells 0 sh / $0 -> net $1,495,015 (BUYING).
Distinct insiders buying (code P): 11. Largest buy: Hanson Theodore S. bought 51,965 sh @ $19.24 ($999,786) on 2026-04-24.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 12, sales 0).

| code | rows |
|---|---|
| F | 1 |
| P | 12 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'Everforth Reports Second Quarter 2026 Results'; skipped 9 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (earningsrelease-q226.htm)

Everforth Reports Second Quarter 2026 Results

Revenues, Net Income, Adjusted EBITDA and Adjusted EBITDA Margin Exceed the High-End of Guidance Estimates

July 29, 2026

RICHMOND, VA.— (BUSINESS WIRE) -- Everforth, Inc. (NYSE: EFOR), a leading technology and digital engineering company, reported financial results for the quarter ended June 30, 2026.

Highlights

Second Quarter 2026

• Revenues were $1,007.0 million

• Net income was $14.2 million

• Adjusted EBITDA (a non-GAAP measure) was $96.7 million (9.6 percent of revenues)

• Operating cash flows were $52.2 million and Free Cash Flow (a non-GAAP measure) was $46.3 million

• Repurchased 0.4 million shares of the Company's common stock for $11.5 million and repaid $23.9 million in debt

• Subsequent to the quarter end, in July completed the refinancing and upsizing of revolver, replacing previous revolver and Term Loan A, with a new five-year $600 million revolving facility

IT Consulting Metrics

• Commercial Segment - book-to-bill ratio for the IT Consulting business trailing-twelve-month period ("TTM") was 1.2 to 1

• Federal Government Segment - New contract awards for the TTM were $0.9 billion; book-to-bill ratio was 0.8 to 1

Management Commentary

"Everforth delivered solid second quarter 2026 results, with revenues of $1 billion and Adjusted EBITDA margin of 9.6 percent both exceeding our expectations," said Ted Hanson, Chief Executive Officer of Everforth, Inc. "Performance in the quarter was supported by strength across our Commercial enterprise platform portfolio, where improving bookings conversion contributed meaningfully to our results and drove revenues above guidance for the quarter. In addition, the recent expansion of our revolving credit facility just after quarter end further strengthened our balance sheet and enhanced our financial flexibility."

Hanson continued, "As AI adoption continues to accelerate and customers move from pilots to scaled production environments, the challenge is less about access to technology and more about integrating AI into workflows, data environments, and operating models. We believe that the last mile of the AI valuation equation will be IT services, and Everforth's differentiated combination of talent, industry expertise, governance capabilities, and technology alliances positions us at the intersection of the most important trends shaping our industry. We enter this next phase of AI adoption with confidence in both our strategy and ability to execute."

Second Quarter 2026 Financial Results - Summary

Three Months Ended
June 30, | March 31,
(In millions, except per share data) | 2026 | 2025 | 2026
Revenues
Commercial Segment | 701.7 | 708.1 | 675.5
Federal Government Segment | 305.3 | 312.5 | 292.8
Consolidated | 1,007.0 | 1,020.6 | 968.3
Gross Margin
Commercial Segment | 32.1 | % | 33.0 | % | 31.0 | %
Federal Government Segment | 19.6 | % | 19.2 | % | 19.6 | %
Consolidated | 28.3 | % | 28.7 | % | 27.5 | %
Net income | 14.2 | 29.3 | 5.5
Earnings per diluted share | 0.35 | 0.67 | 0.13
Non-GAAP Financial Measures
Adjusted Net Income | 37.2 | 51.6 | 28.7
Adjusted Net Income per diluted share | 0.91 | 1.17 | 0.69
Adjusted EBITDA | 96.7 | 108.5 | 83.6
Adjusted EBITDA margin | 9.6 | % | 10.6 | % | 8.6 | %

Definitions of non-GAAP measures and reconciliation to GAAP measurements are included in the tables that accompany this release.

Consolidated revenues for the quarter were $1,007.0 million, compared with $1,020.6 million in the second quarter of 2025. Commercial Segment revenues were 70 percent of total revenues and were $701.7 million, compared with $708.1 million in the second quarter of 2025. Federal Government Segment revenues were 30 percent of total revenues and were $305.3 million, compared with $312.5 million in the prior-year period.

Commercial Segment revenues are categorized into five industries: (i) Consumer and Industrial, (ii) Technology, Media and Telecom ("TMT"), (iii) Financial Services, (iv) Healthcare, and (v) Business Services. Four of the industries decreased year-over-year, while TMT increased by $7.7 million or 5.6 percent.

Federal Segment revenues are categorized into four customer types: (i) Defense and Intelligence, (ii) National Security, (iii) Federal Civilian, and (iv) other clients. The year-over-year revenue decline was attributable to decreases in Defense and Intelligence and Federal Civilian, partially offset by increases in National Security and other clients.

Gross margin for the second quarter of 2026 was 28.3 percent, a compression of 40 basis points from the second quarter of 2025. Gross margin for the Commercial Segment was 32.1 percent, down 90 basis points year-over-year primarily driven by a lower mix of high-margin permanent placement revenues, as well as changes in foreign exchange rates primarily related to our delivery center in Mexico. Gross margin for the Federal Government Segment was 19.6 percent, up 40 basis points year over year, driven by focused efforts to improve profitability across the contract portfolio.

Selling, general, and administrative ("SG&A") expenses were $226.2 million, compared with $216.8 million in the prior-year period. SG&A expenses included $9.8 million in acquisition, integration, and strategic planning expenses, compared with $8.3 million in the prior-year period.

Net income was $14.2 million ($0.35 per diluted share), compared with $29.3 million ($0.67 per diluted share) in the second quarter of 2025.

Adjusted EBITDA (a non-GAAP measure) was $96.7 million, or 9.6 percent of revenues ("Adjusted EBITDA margin," a non-GAAP measure), compared with $108.5 million or 10.6 percent of revenues in the second quarter of 2025.

Capital Resources and Allocation

At June 30, 2026, the Company had:

• Cash and cash equivalents of $152.9 million

• Availability of approximately $180.0 million under the Company's $500.0 million Senior Secured Revolving Credit Facility (due 2028)

• Senior Secured Debt, consisting of a Term Loan A facility with outstanding balance of $97.5 million (due 2028) and a Term Loan B facility with outstanding balance of $486.3 million (due 2030)

• Senior unsecured notes totaling $550.0 million at 4.625 percent (due 2028)

During the quarter the Company repurchased 0.4 million shares of its common stock for $11.5 million at an average price of $30.07 per share. Approximately $923 million remained available at quarter end for repurchases under the Company's stock repurchase plan. Subsequent to the quarter end, in July the Company completed the refinancing and upsizing of its revolver, replacing the previous revolver and Term Loan A with a new five-year $600 million revolving facility.

Third Quarter 2026 Financial Estimates

The Company's financial estimates for the third quarter of 2026, which are set forth below, are based on current market conditions and assume no deterioration in the markets served. Reconciliations of estimated net income to the estimated non-GAAP financial measures are included in the tables that accompany this release.

(In millions, except per share data) | Low | High
Revenues | 994.0 | 1,024.0
SG&A expenses (1) | 220.4 | 221.9
Amortization of intangible assets | 17.3 | 17.3
Net income | 14.5 | 23.0
Earnings per diluted share | 0.36 | 0.56
Gross margin | 28.0 | % | 28.5 | %
Effective tax rate (2) | 29.0 | % | 29.0 | %
Non-GAAP Financial Measures:
Adjusted EBITDA | 95.0 | 105.0
Adjusted Net Income (3) | 37.8 | 44.8
Adjusted Net Income per diluted share (4) | 0.92 | 1.10
Adjusted EBITDA margin | 9.6 | % | 10.3 | %

(1) Includes non-cash expenses totaling $27.2 million, comprised of: (i) $14.0 million of stock-based compensation, (ii) $10.1 million of depreciation, and (iii) $3.1 million of amortization related to capitalized cloud-based application implementation costs. Also includes acquisition, integration, and strategic planning expenses of approximately $7.5 million to $9.5 million, related to strategic initiatives including updates to our go-to market strategy, outsourcing of certain back-office functions, ERP implementation, and costs related to the integration of Quinnox.

(2) Estimated effective tax rate before any excess tax benefits or shortfall related to stock-based compensation.

(3) Does not include the cash tax savings benefit of the tax deduction received from the amortization of goodwill and trademarks, approximately $9.6 million per quarter ($0.24 per diluted share).

Conference Call

The Company will hold a conference call today at 4:30 p.m. ET to review its financial results for the second quarter of 2026 and to provide third quarter 2026 estimates. The dial-in number is 877-407-0792 (+1-201-689-8263), and the conference ID number is 13760713. Participants should dial in ten minutes before the call. The prepared remarks, supplemental materials and webcast for this call can be accessed at www.everforth.com.

A replay of the conference call will be available beginning today at 7:30 p.m. ET until August 12, 2026. The access number for the replay is 844-512-2921 (+1-412-317-6671) and the conference ID number is 13760713. A replay of the webcast will be available at www.everforth.com.

About Everforth, Inc.

Everforth, Inc. (NYSE: EFOR) is a leading technology and digital engineering company with six core solution areas: AI and data, cloud and infrastructure, application and digital engineering, customer experience, cybersecurity, and enterprise platforms. Through proprietary assets, accelerators, and proven expertise, Everforth delivers measurable outcomes that help organizations adapt, innovate, and thrive.

Everforth: Adapt and Thrive. TM

Learn more at everforth.com.

RECONCILIATIONS OF GAAP TO NON-GAAP MEASURES (Unaudited)

( In millions, except per share data )

Three Months Ended | Six Months Ended
June 30, | March 31, | June 30,
2026 | 2025 | 2026 | 2026 | 2025
Net income | 14.2 | 29.3 | 5.5 | 19.7 | 50.2
Interest expense | 20.4 | 18.2 | 17.1 | 37.5 | 33.6
Provision for income taxes | 6.5 | 12.1 | 5.1 | 11.6 | 22.4
Depreciation and other amortization (1) | 13.9 | 11.8 | 13.5 | 27.4 | 23.0
Amortization of intangible assets | 17.3 | 16.9 | 14.5 | 31.8 | 31.2
EBITDA (non-GAAP measure) | 72.3 | 88.3 | 55.7 | 128.0 | 160.4
Stock-based compensation | 14.6 | 11.9 | 15.1 | 29.7 | 25.7
Software costs write-off (2) | — | — | — | — | 4.4
Acquisition, integration, and strategic planning expenses (3) | 9.8 | 8.3 | 12.8 | 22.6 | 11.6
Adjusted EBITDA (non-GAAP measure) | 96.7 | 108.5 | 83.6 | 180.3 | 202.1

Three Months Ended | Six Months Ended
June 30, | March 31, | June 30,
2026 | 2025 | 2026 | 2026 | 2025
Net income | 14.2 | 29.3 | 5.5 | 19.7 | 50.2
Software costs write-off (2) | — | — | — | — | 4.4
Acquisition, integration, and strategic planning expenses (3) | 9.8 | 8.3 | 12.8 | 22.6 | 11.6
Tax effect on adjustments | (2.5) | (2.2) | (3.3) | (5.8) | (4.1)
Non-GAAP net income | 21.5 | 35.4 | 15.0 | 36.5 | 62.1
Amortization of intangible assets | 17.3 | 16.9 | 14.5 | 31.8 | 31.2
Other | (1.6) | (0.7) | (0.8) | (2.4) | (1.3)
Adjusted Net Income (non-GAAP measure) (4) | 37.2 | 51.6 | 28.7 | 65.9 | 92.0
Per diluted share:
Net income | 0.35 | 0.67 | 0.13 | 0.48 | 1.14
Adjustments | 0.56 | 0.50 | 0.56 | 1.12 | 0.95
Adjusted Net Income (non-GAAP measure) (4) | 0.91 | 1.17 | 0.69 | 1.60 | 2.09
Common shares and share equivalents (diluted) | 41.0 | 44.0 | 41.4 | 41.2 | 44.0

(1) The three months ended June 30, 2026 include $2.6 million of amortization related to capitalized cloud-based application implementation costs included in SG&A expenses.

(2) Write-off of previously capitalized costs related to software enhancements that will no longer be placed into service.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-25_item7_mdna.md)

_Extraction: started at the Overview heading._

OVERVIEW

ASGN provides IT solutions across the commercial and government sectors. ASGN operates through two segments, Commercial and Federal Government. The Commercial Segment, which is the largest segment, provides consulting, creative digital marketing, and permanent placement services primarily to Fortune 1000 and large mid-market companies. The Federal Government Segment provides advanced IT solutions in data and AI, cybersecurity, and enterprise transformation to some of the world's leading agencies in the public and private sectors. Virtually all of the Company's revenues are generated in the United States.

Critical Accounting Policies and Estimates

Our financial statements are prepared in conformity with accounting principles generally accepted in the United States ("GAAP"), which require us to make certain assumptions and related estimates affecting the amounts reported in the consolidated financial statements. Actual results could differ from those estimates.

Critical accounting policies are those we believe are both most important to the portrayal of our financial condition and results and require our most difficult, subjective or complex judgments, often because we must make estimates about matters that are inherently uncertain. Judgments and uncertainties affecting the application of those policies may result in materially different amounts being reported under different conditions or using different assumptions. We believe the accounting policies and estimates most critical in understanding the judgments involved in preparing our financial statements are goodwill and acquired intangible assets.

Recognition of Goodwill and Acquired Intangible Assets — Determining the fair value of goodwill and intangible assets requires management's judgment, the use of significant estimates and assumptions and, in some cases, the utilization of independent valuation experts. The most critical assumptions utilized in this determination are the future cash flow estimates associated with the acquired businesses, as well as discount rates and royalty rates applied to those cash flow estimates.

Recoverability of Goodwill and Trademarks — Goodwill and trademarks are evaluated for impairment annually on October 31 st , or more frequently if an event occurs or circumstances change, including but not limited to, a significant decrease in expected revenues or cash flows;

an adverse change in the business environment, regulatory environment or legal factors; or a substantial sustained decline in the market capitalization of our stock. Goodwill is tested at the reporting unit level, which is generally an operating segment or one level below the operating segment level, where a business operates and for which discrete financial information is available and reviewed by segment management. The Company's only identifiable indefinite-lived intangible assets are its trademarks.

When evaluating goodwill and trademarks for impairment, the Company may first perform a qualitative assessment to determine whether it is more likely than not that there has been an impairment. A qualitative assessment takes into consideration (i) macroeconomic, industry and market conditions; (ii) cost factors; (iii) overall financial performance compared with prior projections, including changes in assumptions since the last quantitative assessment; (iv) future performance and projections; (v) the excess of fair value over carrying value as of the most recent quantitative assessment performed; and (vi) other relevant entity-specific events. The decision to perform a qualitative assessment in a given year is influenced by a number of factors including the significance of the excess of the estimated fair value over carrying amount at the last quantitative assessment date and the amount of time between quantitative fair value assessments. If the Company decides not to perform a qualitative assessment, or if it determines that it is more likely than not that the carrying amount of goodwill or trademarks exceeds their fair value, a quantitative assessment is performed to determine the estimated fair value of the reporting unit or trademark.

To estimate the fair value of a reporting unit, quantitative analysis would generally include a combination of a discounted cash flow ("DCF") model and a market approach. Key inputs to the DCF model would include (i) future revenues; (ii) earnings before interest, taxes, depreciation and amortization; and (iii) the weighted average cost of capital discount rate. As a result of a quantitative assessment, if the carrying amount exceeds the estimated fair value, an impairment charge would be recorded to reduce the carrying amount of goodwill.

To estimate the fair value of a trademark, quantitative analysis would generally include, an income approach, specifically a relief-from-royalty method. As a result of a quantitative assessment, if the carrying amount exceeds the estimated fair value, an impairment charge would be recorded to reduce the carrying amount of the trademark.

For the 2025 impairment test of goodwill and trademarks, the Company performed a qualitative assessment and determined there were no indicators of impairment and it was more likely than not that the fair value of its two reporting units, Commercial and Federal Government, and its trademarks, exceeded their respective carrying amounts.

RESULTS OF OPERATIONS FOR THE YEAR ENDED DECEMBER 31, 2025 COMPARED WITH THE YEAR ENDED DECEMBER 31, 2024

In this section, we discuss the results of our operations for the year ended December 31, 2025 compared with the year ended December 31, 2024. For a discussion of the year ended December 31, 2024 compared with the year ended December 31, 2023, please refer to Part II, Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations in our Annual Report on Form 10-K for the year ended December 31, 2024.

Revenues

Revenues for the year were $4.0 billion, down 2.9 percent year-over-year. The table below shows our revenues by segment (in millions).

% of Total
2025 | 2024 | Change | 2025 | 2024 | Change
Commercial:
Consulting | 1,290.1 | 1,128.2 | 14.4 | % | 32.4 | % | 27.5 | % | 4.9 | %
Assignment | 1,500.1 | 1,740.5 | (13.8) | % | 37.7 | % | 42.5 | % | (4.8) | %
2,790.2 | 2,868.7 | (2.7) | % | 70.1 | % | 70.0 | % | 0.1 | %
Federal Government | 1,190.2 | 1,231.0 | (3.3) | % | 29.9 | % | 30.0 | % | (0.1) | %
Consolidated | 3,980.4 | 4,099.7 | (2.9) | % | 100.0 | % | 100.0 | %

Commercial Segment revenues (70.1 percent of total revenues) were down 2.7 percent year-over-year and are categorized into five industries: (i) Consumer and Industrial, (ii) Financial Services, (iii) Technology, Media and Telecom ("TMT"), (iv) Healthcare, and (v) Business Services. The Consumer and Industrials industry was up low-teens and Healthcare was up low single digits, while the remaining three industries declined. Federal Government Segment revenues (29.9 percent of total revenues) were down 3.3 percent year-over-year. Federal Government Segment revenues are categorized into four customer types: (i) Defense and Intelligence, (ii) National Security, (iii) Civilian, and (iv) other clients. Federal Civilian and Defense and Intelligence both declined year-over-year, while National Security was up.

Total IT consulting services revenues were $2.5 billion (62.3 percent of total revenues), up 5.1 percent year-over-year. Commercial Segment consulting revenues were $1.3 billion, up 14.4 percent year-over-year. Federal Government Segment revenues, which are all consulting revenues, were $1.2 billion, down 3.3 percent year-over-ye a r mainly related to the loss of certain contracts as a result of initiatives associated with DOGE. Assignment revenues, which totaled $1.5 billion (37.7 percent of total revenues), were down 13.8 percent year-over-year, reflecting con tinued softness in the portions of the Commercial Segment Business that are more sensitive to changes in the macroeconomic cycles.

Gross Profit and Gross Margin

The table below shows gross profit and gross margin by segment (in millions).

Gross Profit | Gross Margin
2025 | 2024 | Change | 2025 | 2024 | Change
Commercial | 914.4 | 932.9 | (2.0) | % | 32.8 | % | 32.5 | % | 0.3 | %
Federal Government | 234.7 | 250.8 | (6.4) | % | 19.7 | % | 20.4 | % | (0.7) | %
Consolidated | 1,149.1 | 1,183.7 | (2.9) | % | 28.9 | % | 28.9 | % | — | %

Gross profit is comprised of revenues, less costs of services, which consist primarily of compensation for our billable professionals, other direct costs, and reimbursable out-of-pocket expenses.

Consolidated gross profit declined 2.9 percent consistent with the decline in revenues, resulting in a consistent gross margin of 28.9 percent in each year. Gross margin for the Commercial Segment was up 30 basis points, reflecting a higher mix of consulting revenues. Gross margin for the Federal Government Segment was down 70 basis points, primarily due to a higher volume of revenues from low-margin software licenses, the loss of certain higher margin contracts as a result of initiatives associated with DOGE, and higher rates of fringe benefits.

Selling, General, and Administrative Expenses

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-25_item1_business.md)

Item 1. Business

Overview and History

ASGN Incorporated ("ASGN," "our", "we," or "us") is a leading provider of information technology (IT) solutions to the commercial and government sectors. In November 2025, ASGN announced its intent to rebrand to Everforth, a new parent brand that will unify our six brands — Apex Systems, Creative Circle, CyberCoders, ECS, GlideFast, and TopBloc — under a single identity. Everforth is a leading technology and digital engineering company with six core solution areas: (i) Cloud and Infrastructure, (ii) Data and AI, (iii) Software Development and Engineering, (iv) Customer Experience, (v) Cybersecurity, and (vi) Enterprise Platforms. Through proprietary assets, accelerators, and proven expertise, Everforth delivers measurable outcomes that help organizations adapt, innovate, and thrive.

Our Company operates through two segments, Commercial and Federal Government, and across six industries, which together promote balance, strength, and resiliency throughout economic cycles. The transition from ASGN to Everforth is slated for the first half of 2026.

Our Company has grown through a combination of organic growth and strategic acquisitions. Over the last five years, we completed six acquisitions which align with our strategy to offer higher-end, higher-value IT consulting solutions and digital engineering capabilities. We have built a sizable consulting platform, with 62 percent of our 2025 consolidated revenues in a combination of commercial and federal government IT consulting work.

Our clients set rigorous requirements for expertise, technological proficiency, and solutions capabilities. Their expectations have increased as we've evolved our business. To meet their requirements, we leverage a deep talent pool of professionals that has been expertly built over decades. This enables us to differentiate our Company in the marketplace, by quickly identifying and building tailored, just-in-time teams for our clients.

We support clients across a diverse set of industries. No client, other than the U.S. federal government, represented more than 10 percent of consolidated revenues in 2025. Revenues from contracts directly with several U.S. federal government agencies in which our Federal Government Segment is a prime contractor combined were 26 percent of consolidated revenues in 2025.

ASGN was incorporated in 1992. Our principal office is located at 4400 Cox Road, Suite 110, Glen Allen, Virginia 23060, and our telephone number is (888) 482-8068.

Commercial Segment

Our Commercial Segment (70 percent of 2025 consolidated revenues) provides IT solutions to Fortune 1000 and large mid-market clients across six harmonized solutions areas: (i) Cloud and Infrastructure, (ii) Data and AI, (iii) Software Development and Engineering, (iv) Customer Experience, (v) Cybersecurity, and (vi) Enterprise Platforms; and five industries: (i) Financial Services, (ii) Consumer and Industrial, (iii) Technology, Media and Telecom ("TMT"), (iv) Healthcare, and (v) Business and Government Services.

Our business heritage is providing our clients with experienced IT and creative digital marketing professionals for project engagements. These roots as a premier IT staffing provider differentiate how we go to market. As aforementioned, by leveraging our deep talent pool, we can quickly build custom-fit teams for our clients incorporating the latest technology skillsets. Building on our staffing foundation, we have cultivated enduring, trusted relationships with enterprise clients and established a significant presence within their organizations.

Over the past six years, we have strategically refined our focus and broadened our service portfolio to encompass high-value, high-margin consulting solutions that enable us to effectively address the evolving and increasingly complex needs of our client base. Our subject matter experts deliver solutions that are tailored for specific industries and customer environments, meeting business challenges at greater speed and with more accuracy and precision than ever before. By harnessing proprietary assets and accelerators and leveraging our technology alliance partner ecosystem to co-sell, co-develop, and co-deliver our solutions capabilities, we are driving greater revenue opportunities and actively building our pipeline of new business. The Commercial Segment provides services under time-and-materials and fixed-price contracts.

Corporate support activities for this segment are primarily based in Richmond, Virginia, with offices across the United States, Canada, and Europe. In addition, we have two near-shore delivery centers in Mexico and maintain a growing delivery center in India.

Consulting — Our business focus and growth strategy lies in providing our clients with higher value IT consulting services. A byproduct of our decades-long, trusted client relationships over the years, our customers have increasingly engaged us in higher-value consulting contracts. Consulting contracts leverage the same talent pool as our assignment work but offer higher margin opportunities and increased revenue visibility.

Assignment — Our business heritage is in providing our clients with experienced IT and creative digital marketing billable professionals for temporary assignments and project engagements. Our billable professionals have knowledge and experience in specialized technical and creative digital marketing services that make them qualified to fill a given assignment or project.

Federal Government Segment

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-02-25_item7_mdna.md, 10-K_2026-02-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
