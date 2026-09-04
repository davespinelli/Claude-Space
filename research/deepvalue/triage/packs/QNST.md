# Triage pack — QNST · QUINSTREET, INC

_Generated 2026-09-04 18:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** QNST · **Name:** QUINSTREET, INC
- **CIK:** 0001117297
- **SIC:** 7389 — Services-Business Services, NEC
- **Fiscal year end (MM-DD):** 06-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/QNST

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** QUINSTREET, INC
- **CIK:** 1,117,297 · **SIC:** 7389 (Services-Business Services, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 18.76 |
| mktcap | $1.1B |
| ev | $1.0B |
| ev_ebit | 164.6x |
| fcf | $82.9M |
| fcf_yield | 7.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 1.8% |
| net_debt | -$58.3M |
| net_debt_ebit | -9.4x |
| cash | $128.3M |
| ltd | $70.0M |
| equity | $323.1M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.1B |
| revenue_prior | $613.5M |
| rev_growth | 78.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $6.2M |
| net_income | $4.7M |
| cfo | $85.0M |
| capex | $2.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 57,445,370 |
| shares_py | 56,951,925 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 2.0% |
| r6m | 49.8% |
| off_52w_high | -14.8% |
| adv20 | $24.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.63 |
| r_ev_ebit | 0.05 |
| r_roic | 0.37 |
| r_rev_growth | 0.97 |
| r_buyback | 0.49 |
| score | 0.55 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 198 |

**Screen rationale:** revenue +78.3%; net cash; 12-1 momentum 2.0%


## 3. Share count trend

- Shares outstanding: **57,445,370** (CY2026Q1I) vs **56,951,925** prior year (CY2025Q1I)
- Change: **0.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 862,026 sh / $17,423,897 -> net $-17,423,897 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 45 (open-market buys 0, sales 9).

| code | rows |
|---|---|
| A | 6 |
| F | 24 |
| G | 6 |
| S | 9 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'QuinStreet Reports Record Fiscal Fourth Quarter and Full Year 2026 Res'; skipped 9 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (qnst-ex99_1.htm)

QuinStreet Reports Record Fiscal Fourth Quarter and Full Year 2026 Results

•
Record quarterly Revenue of $373.9 million, up 43% year-over-year

•
Record quarterly Net Income of $19.1 million, up 496% year-over-year

•
Record quarterly Adj. EBITDA of $41.4 million, up 87% year-over-year

•
Record Full Fiscal Year Revenue of $1.3 billion, up 18% year-over-year

•
Record Full Fiscal Year Net Income of $81.2 million, up 1,626% year-over-year

•
Record Full Fiscal Year Adj. EBITDA of $112.5 million, up 38% year-over-year

FOSTER CITY, CA – August 6, 2026 – QuinStreet, Inc. (Nasdaq: QNST), a leader in performance marketplaces and technologies for the financial services and home services industries, today announced financial results for the fiscal fourth quarter and fiscal year ended June 30, 2026.

For the fiscal fourth quarter, the Company reported revenue of $373.9 million, up 43% year-over-year.

GAAP net income for the fiscal fourth quarter was $19.1 million, or $0.33 per diluted share. Adjusted net income for the fiscal fourth quarter was $29.0 million, or $0.50 per diluted share.

Adjusted EBITDA for the fiscal fourth quarter was $41.4 million, up 87% year-over-year.

For full fiscal year 2026, the Company reported revenue of $1.3 billion, up 18% year-over-year.

GAAP net income for fiscal year 2026 was $81.2 million, or $1.40 per diluted share. Adjusted net income for fiscal year 2026 was $73.8 million, or $1.27 per diluted share.

Adjusted EBITDA for fiscal year 2026 was $112.5 million, up 38% year-over-year.

For full fiscal year 2026, the Company generated $130.9 million in operating cash flow and closed the quarter with $128.3 million in cash and cash equivalents.

"Fiscal Q4 was another record quarter of strong performance and progress, capping a record year for QuinStreet," commented Doug Valenti, CEO of QuinStreet. "We grew quarterly revenue 43% year-over-year with strength in both Financial Services and Home Services. Adjusted EBITDA was up 87% year-over-year and came in at an 11.1% margin, a 270 basis-point improvement over the year-ago quarter."

"For full fiscal year 2026, revenue grew 18% year-over-year to $1.3 billion, and adjusted EBITDA grew 38% year-over-year to $112.5 million, an 8.7% margin and a 130-basis point year-over-year margin expansion. Over the past 2 years, we have more than doubled our revenue and grown adjusted EBITDA by more than 450%."

"We expect to continue to grow revenue at strong double-digit rates and to expand margins in fiscal year 2027 and beyond. Our market opportunities are large, and we believe that we are still in their early innings. Our revenue growth continues to be driven by the relentless shift of marketing budgets to digital and performance marketing, and by our proven ability to consistently deliver results at scale for clients. Our key competitive advantage continues to be our industry-leading technologies, including our core AI optimization algorithms. We are also accelerating improvements in performance and productivity from new AI applications across the business."

"Turning to our outlook, we expect revenue in fiscal Q1 to be between $370 and $380 million, implying 31% growth year-over-year at the midpoint of the range. We expect adjusted EBITDA to be between $38 and $40 million, implying 90% growth, a 10.4% margin and a 320 basis-point margin expansion year-over-year at the midpoint of the range."

"As an initial full fiscal year 2027 outlook, we expect revenue of $1.45 billion to $1.55 billion, implying 16% growth year-over-year at the midpoint of the range. We expect adjusted EBITDA of $150 to $160 million, implying growth of 38%, a 10.3% margin and another 160 basis-point margin expansion year-over-year at the midpoint of the range on top of last year's 130 basis-point expansion. We believe that there may be opportunities to grow revenue and expand margins even further, and we will refine our outlook as the year progresses," concluded Valenti.

Conference Call Today at 2:00 p.m. PT

The Company will host a conference call and corresponding live webcast at 2:00 p.m. PT. To access the conference call dial +1 800-717-1738 (domestic) or +1 646-307-1865 (international). A replay of the conference call will be available beginning approximately two hours after the completion of the call by dialing +1 844-512-2921 (domestic) or +1 412-317-6671 (international) and using passcode #1132818. The webcast of the conference call will be available live and via replay on the investor relations section of the Company's website at http://investor.quinstreet.com .

About QuinStreet

QuinStreet, Inc. (Nasdaq: QNST) is a leader in performance marketplaces and technologies for the financial services and home services industries. QuinStreet is a pioneer in delivering online marketplace solutions to match searchers with brands in digital media, and is committed to providing consumers with the information and tools they need to research, find and select the products and brands that meet their needs.

Non-GAAP Financial Measures and Definitions of Client Verticals

This release and the accompanying tables include a discussion of adjusted EBITDA, adjusted net income, adjusted diluted net income per share and free cash flow and normalized free cash flow, all of which are non-GAAP financial measures that are provided as a complement to results provided in accordance with accounting principles generally accepted in the United States of America ("GAAP"). The term "adjusted EBITDA" refers to a financial measure that we define as net income (loss) excluding depreciation and amortization expense, stock-based compensation expense, interest and other expense, net, provision for (benefit from) income taxes, restructuring costs, acquisition costs, litigation settlement expense, impairment charges, and contingent consideration adjustment. The term "adjusted net income" refers to a financial measure that we define as net income (loss) adjusted for amortization expense, stock-based compensation expense, acquisition costs, contingent consideration adjustment, litigation settlement expense, restructuring costs, impairment charges, tax valuation allowance, and the related income tax effects of these adjustments. The term "adjusted diluted net income (loss) per share" refers to a financial measure that we define as adjusted net income divided by weighted average diluted shares outstanding. The term "free cash flow" refers to a financial measure that we define as net cash provided by operating activities, less capital expenditures and internal software development costs. The term "normalized free cash flow" refers to free cash flow less changes in operating assets and liabilities. These non-GAAP measures should be considered in addition to results prepared in accordance with GAAP, but should not be considered a substitute for, or superior to, GAAP results. In addition, our definition of adjusted EBITDA, adjusted net income, adjusted diluted net income per share and free cash flow and normalized free cash flow may not be comparable to the definitions as reported by other companies.

We believe adjusted EBITDA, adjusted net income and adjusted diluted net income per share are relevant and useful information because they provide us and investors with additional measurements to analyze the Company's operating performance.

Adjusted EBITDA is useful to us and investors because (i) we seek to manage our business to a level of adjusted EBITDA as a percentage of net revenue, (ii) it is used internally by us for planning purposes, including preparation of internal budgets; to allocate resources; to evaluate the effectiveness of operational strategies and capital expenditures as well as the capacity to service debt, (iii) it is a key basis upon which we assess our operating performance, (iv) it is one of the primary metrics investors use in evaluating Internet marketing companies, (v) it is a factor in determining compensation, (vi) it is an element of certain financial covenants under our historical borrowing arrangements, and (vii) it is a factor that assists investors in the analysis of ongoing operating trends. In addition, we believe adjusted EBITDA and similar measures are widely used by investors, securities analysts, ratings agencies and other interested parties in our industry as a measure of financial performance, debt-service capabilities and as a metric for analyzing company valuations.

We use adjusted EBITDA as a key performance measure because we believe it facilitates operating performance comparisons from period to period by excluding potential differences caused by variations in capital structures (affecting interest expense), tax positions (such as the impact of changes in effective tax rates or fluctuations in permanent differences or discrete quarterly items), non-recurring charges, certain other items that we do not believe are indicative of core operating activities (such as litigation settlement expense, acquisition costs, contingent consideration adjustment, restructuring costs, impairment charges and other income and expense) and the non-cash impact of depreciation expense, amortization expense and stock-based compensation expense.

With respect to our adjusted EBITDA guidance, the Company is not able to provide a quantitative reconciliation to the most directly comparable GAAP financial measure without unreasonable efforts due to the high variability, complexity and low visibility with respect to certain items such as taxes, and income and expense from changes in fair value of contingent consideration from acquisitions. We expect the variability of these items to have a potentially unpredictable and potentially significant impact on future GAAP financial results, and, as such, we also believe that any reconciliations provided would imply a degree of precision that would be confusing or misleading to investors.

Adjusted net income and adjusted diluted net income per share are useful to us and investors because they present an additional measurement of our financial performance, taking into account depreciation, which we believe is an ongoing cost of doing business, but excluding the impact of certain non-cash expenses (stock-based compensation, amortization of intangible assets, and contingent consideration adjustment), non-recurring charges and certain other items that we do not believe are indicative of core operating activities. We believe that analysts and investors use adjusted net income and adjusted diluted net income per share as supplemental measures to evaluate the overall operating performance of companies in our industry.

Free cash flow is useful to investors and us because it represents the cash that our business generates from operations, before taking into account cash movements that are non-operational, and is a metric commonly used in our industry to understand the underlying cash generating capacity of a company's financial model. Normalized free cash flow is useful as it removes the fluctuations in operating assets and liabilities that occur in any given quarter due to the timing of payments and cash receipts and therefore helps investors understand the underlying cash flow of the business as a quarterly metric and the cash flow generation potential of the business model. We believe that analysts and investors use free cash flow multiples as a metric for analyzing company valuations in our industry.

We intend to provide these non-GAAP financial measures as part of our future earnings discussions and, therefore, the inclusion of these non-GAAP financial measures will provide consistency in our financial reporting. A reconciliation of these non-GAAP measures to GAAP is provided in the accompanying tables.

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-08-26_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

A discussion regarding our results of operations for fiscal year 2026 compared to fiscal year 2025 is presented below. A discussion regarding our results of operations for fiscal year 2025 compared to fiscal year 2024 can be found under the heading Results of Operation in Part II, Item 7., Management's Discussion and Analysis of Financial Condition and Results of Operations of our Annual Report on Form 10-K for fiscal year 2025, filed with the SEC on August 21, 2025, which is available on the SEC's website at www.sec.gov .

The following table presents our consolidated statements of operations for the periods indicated:

Fiscal Year Ended June 30,
2026 | 2025 | 2024
(In thousands, except percentages)
Net revenue | 1,293,712 | 100.0 | % | 1,093,711 | 100.0 | % | 613,514 | 100.0 | %
Cost of revenue (1) | 1,147,903 | 88.7 | 982,840 | 89.9 | 567,268 | 92.5
Gross profit | 145,809 | 11.3 | 110,871 | 10.1 | 46,246 | 7.5
Operating expenses: (1)
Product development | 37,303 | 2.9 | 33,872 | 3.1 | 30,045 | 4.9
Sales and marketing | 27,259 | 2.1 | 18,289 | 1.7 | 13,607 | 2.2
General and administrative | 45,821 | 3.5 | 52,517 | 4.8 | 30,659 | 5.0
Operating income (loss) | 35,426 | 2.7 | 6,193 | 0.5 | (28,065 | (4.6
Interest income | 96 | — | 23 | — | 408 | 0.1
Interest expense | (4,393 | (0.3 | (400 | — | (680 | (0.1
Other income (expense), net | 81 | — | (183 | — | (2,059 | (0.3
Income (loss) before income taxes | 31,210 | 2.4 | 5,633 | 0.5 | (30,396 | (4.9
Benefit from (provision for) income taxes | 50,025 | 3.9 | (926 | (0.1 | (935 | (0.2
Net income (loss) | 81,235 | 6.3 | % | 4,707 | 0.4 | % | (31,331 | (5.1 | )%

(1)
Cost of revenue and operating expenses include stock-based compensation expense as follows:

Cost of revenue | 14,860 | 1.1 | % | 11,658 | 1.1 | % | 8,409 | 1.4 | %
Product development | 6,117 | 0.5 | 4,386 | 0.4 | 3,147 | 0.5
Sales and marketing | 5,130 | 0.4 | 4,408 | 0.4 | 2,968 | 0.5
General and administrative | 11,325 | 0.9 | 11,314 | 1.0 | 9,177 | 1.5

Gross Profit

Fiscal Year Ended June 30, | 2026 - 2025 | 2025 - 2024
2026 | 2025 | 2024 | % Change | % Change
(In thousands)
Net revenue | 1,293,712 | 1,093,711 | 613,514 | 18 | % | 78 | %
Cost of revenue | 1,147,903 | 982,840 | 567,268 | 17 | % | 73 | %
Gross profit | 145,809 | 110,871 | 46,246 | 32 | % | 140 | %
Gross profit % | 11 | % | 10 | % | 8 | %

Net Revenue

Net revenue increased by $200.0 million, or 18%, in fiscal year 2026 compared to fiscal year 2025. Revenue from our home services client vertical increased by $128.8 million, or 47%, primarily as a result of the acquisition of HomeBuddy , which contributed $88.9 million in net revenue, in addition to increased client budgets, and successful execution of growth initiatives. Revenue from our financial services client vertical increased by $71.2 million, or 9%, primarily due to an increase in revenue in our insurance business of $79.0 million, attributable to higher demand from a broad base of carrier clients, offset by a decrease in our other financial services client verticals of $7.8 million.

Cost of Revenue and Gross Profit Margin

Cost of revenue increased by $165.1 million, or 17%, in fiscal year 2026 compared to fiscal year 2025. This was primarily driven by increased media and marketing costs of $161.4 million due to higher revenue volumes. Personnel costs increased by $5.1 million mainly due to higher stock-based compensation expense due to higher average grant date share prices in the current year.

Gross profit margin, which is the difference between net revenue and cost of revenue as a percentage of net revenue, was 11% and 10% in fiscal years 2026 and 2025. Our gross profit was $145.8 million for fiscal year 2026 compared to $110.9 million for fiscal year 2025, an increase of $34.9 million, or 32%. The increase in gross profit margin was attributable to a decrease in personnel cost and depreciation cost as a percentage of net revenue, partially offset by an increase in media and marketing costs as a percentage of net revenue.

Operating Expenses

Fiscal Year Ended June 30, | 2026 - 2025 | 2025 - 2024
2026 | 2025 | 2024 | % Change | % Change
(In thousands)
Product development | 37,303 | 33,872 | 30,045 | 10 | % | 13 | %
Sales and marketing | 27,259 | 18,289 | 13,607 | 49 | % | 34 | %
General and administrative | 45,821 | 52,517 | 30,659 | (13 | %) | 71 | %
Operating expenses | 110,383 | 104,678 | 74,311 | 5 | % | 41 | %

Product Development Expenses

Product development expenses increased by $3.4 million, or 10%, in fiscal year 2026 compared to fiscal year 2025. This was primarily due to increased stock-based compensation expense due to higher average grant date share prices in the current year and increased personnel cost due to higher headcount as a result of the HomeBuddy acquisition.

Sales and Marketing Expenses

Sales and marketing expenses increased by $9.0 million, or 49%, in fiscal year 2026 compared to fiscal year 2025. This was primarily due to increased personnel cost due to higher headcount as a result of the HomeBuddy acquisition and retention bonus, and increased amortization expense due to the acquisition of related intangible assets.

General and Administrative Expenses

General and administrative expenses decreased by $6.7 million, or 13%, in fiscal year 2026 compared to fiscal year 2025. The decrease was primarily driven by a lower increase in the fair value adjustments to contingent consideration related to the AquaVida acquisition compared to the prior year period of $12.0 million, offset by higher professional fees of $6.3 million primarily related to the HomeBuddy acquisition.

Interest and Other (Expense) Income, Net

Fiscal Year Ended June 30, | 2026 - 2025 | 2025 - 2024
2026 | 2025 | 2024 | % Change | % Change
(In thousands)
Interest income | 96 | 23 | 408 | 317 | % | (94 | %)
Interest expense | (4,393 | (400 | (680 | 998 | % | (41 | %)
Other income (expense), net | 81 | (183 | (2,059 | (144 | %) | (91 | %)
Interest and other expense, net | (4,216 | (560 | (2,331 | 653 | % | (76 | %)

Interest income relates to interest earned on our cash and cash equivalents. Interest expense consists primarily of financing costs associated with our revolving credit facility, and imputed interest on post-closing acquisition related payment obligations. Interest expense increased by $4.0 million in fiscal year 2026 compared to fiscal year 2025, primarily reflecting financing and interest costs associated with our revolving credit facility, as well as higher interest accretion on post-closing payment obligations related to the HomeBuddy acquisition due to a higher average outstanding balance of such obligations.

Benefit from (Provision for) Income Taxes

Fiscal Year Ended June 30,
2026 | 2025 | 2024
(In thousands)
Benefit from (provision for) income taxes | 50,025 | (926 | (935
Effective tax rate | (160.3 | %) | 16.5 | % | (3.1 | %)

We maintained a valuation allowance against the majority of our deferred tax assets through the end of fiscal year 2025. In the second quarter of fiscal year 2026, due to the preponderance of positive evidence, including our cumulative profit before taxes and future forecasts of continued profitability in the United States, we determined that sufficient positive evidence existed to conclude that substantially all of our valuation allowance was no longer needed. Accordingly, we recorded a one-time non-cash benefit from income taxes of $60.7 million related to the release of the valuation allowance for the majority of our federal and states deferred tax assets. In addition to the income tax benefit, the Company recorded approximately $9.9 million and $0.8 million of deferred and current federal, state, and foreign tax expense due to current operations.

We recorded a provision for income taxes of $0.9 million in fiscal year 2025, primarily as a result of current state and foreign income taxes of $0.6 million and net expense for deferred federal, state and foreign income taxes of $0.3 million. The net deferred tax expense is related to indefinite lived deferred tax liabilities unable to be offset with deferred tax assets. As a result of cumulative operating losses through fiscal year 2025, the Company maintained a valuation allowance against its net deferred tax assets.

We recorded a provision for income taxes of $0.9 million in fiscal year 2024, primarily as a result of a net expense for deferred federal, state and foreign income taxes of $0.5 million and current state and foreign income taxes of $0.4 million. The net deferred tax expense is related to indefinite lived deferred tax liabilities unable to be offset with deferred tax assets. As a result of continued operating losses through fiscal 2024, the Company maintained a valuation allowance against its net deferred tax assets.

Our effective tax rate was (160.3%), 16.5% and (3.1%) in fiscal years 2026, 2025 and 2024. The change in the effective tax rate in fiscal year 2026 was primarily due to the release of the valuation allowance related to the United States federal and state deferred tax assets with the exception of capital loss carryforwards, foreign NOLs and the California research and development tax credits.

Adjusted EBITDA

Fiscal Year Ended June 30,
2026 | 2025 | 2024
(In thousands)
Other Financial Data:
Adjusted EBITDA (1) | 112,473 | 81,263 | 20,365

(1)
We define adjusted EBITDA as net income (loss) excluding depreciation and amortization expense, stock-based compensation expense, interest and other expense, net, provision for (benefit from) income taxes, restructuring costs, acquisition costs, litigation settlement expense, and contingent consideration adjustment.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-08-26_item1_business.md)

Item 1. B usiness

Our Company

We are a leader in performance marketplaces and technologies for the financial services and home services industries. Our approach to proprietary performance marketing technologies allows clients to engage high-intent digital media or traffic from a wide range of device types (e.g., mobile, desktop, tablet), in multiple formats or types of media (e.g., search engines, large and small media properties or websites, email), and in a wide range of cost-per-action, or CPA, forms. These forms of contact are the primary "products" we sell to our clients, and include qualified clicks, leads, calls, applications and customers. We specialize in customer acquisition for clients in high value, information-intensive markets, or "verticals," including financial services and home services. Our clients include some of the world's largest companies and brands in those markets. The majority of our operations and revenue are in North America.

We generate revenue by delivering measurable online marketing results to our clients. The benefits to our clients include cost-effective and measurable customer acquisition costs, as well as management of highly targeted but also highly fragmented online media sources and access to our world-class proprietary technologies. We are predominantly paid on a negotiated or market-driven "per click," "per lead," or other "per action" basis that aligns with the customer acquisition cost targets of our clients. We bear the cost of paying Internet search companies, third-party media sources, strategic partners and other online media sources to generate qualified clicks, leads, calls, applications or customers for our clients.

Our competitive advantages include our media buying power, proprietary technologies, extensive data and experience in performance marketing, and significant online media market share in the markets or verticals we serve. Our advantage in online media buying is key to our business model and comes from our ability to effectively segment and match high-intent, unbranded media or traffic – one of the largest sources of traffic for customer acquisition – to as many as hundreds of clients or client offerings and, in most cases, to match those visitors to multiple clients, which also satisfies the visitor's desire to choose among alternatives and to shop multiple offerings. Together, the ability to match more visitors in any given flow of traffic or media to a client offering, and to do so multiple times, adds up to a significant media buying advantage compared to individual clients or other buyers for these types of media.

Our proprietary technologies have been developed over the past 27 years to allow us to best segment and match media or traffic, to deliver optimized results for our clients and to operate our high volume and highly complex channel cost-efficiently.

Our extensive data and experience in performance marketing reflect the execution, knowledge and learning from billions of dollars of media spend on these campaigns over time. This is a steep and expensive learning curve. These learnings address millions of permutations of media sources, mix and order of creative and content merchandising, and approaches to the matching and segmentation of Internet visitors to optimize their experience and the results for clients. Together, these learnings allow us to run thousands of campaigns simultaneously and cost-effectively for our clients at acceptable media costs and margins to us.

Because of our deep expertise and capabilities in running financially successful performance marketing programs, we are able to effectively compete for sources and partners of high-intent, unbranded media, and our market share in our client verticals of this media is significant. Our media sources include owned-and-operated organic or search engine optimization ("SEO") websites, targeted search engine marketing ("SEM") or pay-per-click ("PPC") campaigns, native, social media and mobile programs, internal email databases, call center operations, partnerships with large and small online media companies, and more. Our collective media presence results in engagement with a significant share of online visitors in those markets or verticals, which leads us to be included in client online media buys.

We were incorporated in California on April 16, 1999 and reincorporated in Delaware on December 31, 2009. We have been a pioneer in the development and application of measurable marketing on the Internet. Clients pay us for the actual opt-in actions by visitors or customers that result from our marketing activities on their behalf, versus traditional impression-based advertising and marketing models in which an advertiser pays for a broad audience's exposure to an advertisement.

Market Opportunity

Change in marketing strategy and approach

We believe that marketing approaches are changing as budgets shift from offline, analog advertising media to digital advertising media such as Internet marketing. These changing approaches require a shift to fundamentally new competencies, including:

From qualitative, impression-driven marketing to analytic, data-driven marketing

Growth in Internet marketing enables a more data-driven approach to advertising. The measurability of online marketing allows marketers to collect a significant amount of detailed data on the performance of their marketing campaigns, including the effectiveness of ad format and placement and user responses. This data can then be analyzed and used to improve marketing campaign performance and cost-effectiveness on substantially shorter cycle times than with traditional offline media.

From account management-based client relationships to results-based client relationships

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-08-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-08-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-08-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-08-26_item7_mdna.md, 10-K_2026-08-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
