# Triage pack — MPTI · M-tron Industries, Inc.

_Generated 2026-09-04 18:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MPTI · **Name:** M-tron Industries, Inc.
- **CIK:** 0001902314
- **SIC:** 3679 — Electronic Components, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MPTI

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** M-tron Industries, Inc.
- **CIK:** 1,902,314 · **SIC:** 3679 (Electronic Components, NEC) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 72.51 |
| mktcap | $315.2M |
| ev | $218.9M |
| ev_ebit | 21.3x |
| fcf | $8.1M |
| fcf_yield | 2.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 36.2% |
| net_debt | -$96.2M |
| net_debt_ebit | -9.4x |
| cash | $96.2M |
| ltd | $0.00 |
| equity | $118.7M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $54.4M |
| revenue_prior | $49.0M |
| rev_growth | 11.0% |
| rev_growth_note | share count +48.7% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $10.3M |
| net_income | $8.4M |
| cfo | $10.7M |
| capex | $2.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 48.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 4,346,476 |
| shares_py | 2,923,905 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 98.3% |
| r6m | 15.1% |
| off_52w_high | -28.0% |
| adv20 | $11.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.34 |
| r_ev_ebit | 0.42 |
| r_roic | 0.95 |
| r_rev_growth | 0.68 |
| r_buyback | 0.04 |
| score | 0.54 |

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
| rank | 210 |

**Screen rationale:** high ROIC 36.2%; share count +48.7% yoy — growth may be acquisition/issuance-driven, not organic; debt data missing (net cash unverified); 12-1 momentum 98.3%


## 3. Share count trend

- Shares outstanding: **4,346,476** (CY2026Q2I) vs **2,923,905** prior year (CY2025Q2I)
- Change: **48.7%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +48.7% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 2,725 sh / $204,228 -> net $-204,228 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 22 (open-market buys 0, sales 4).

| code | rows |
|---|---|
| A | 3 |
| M | 4 |
| S | 8 |
| X | 7 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-12_2-02-results.md)

_Extraction: started at the first release heading, 'M-tron Industries, Inc. Reports Second Quarter 2026 Results'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ex_984906.htm)

M-tron Industries, Inc. Reports Second Quarter 2026 Results

• | Revenues increased 13.8% to $15.1 million for the three months ended June 30, 2026 compared to $13.3 million for the three months ended June 30, 2025

• | Net income increased 19.9% to $1.9 million for the three months ended June 30, 2026 compared to $1.6 million for the three months ended June 30, 2025 , which included $1.0 million in non-cash stock-based compensation directly related to our 2025 bonus award

• | Net income per diluted share decreased 18.9% to $0.43 for the three months ended June 30, 2026 compared to $0.53 for the three months ended June 30, 2025

• | Adjusted EBITDA increased $1.0 million to $3.4 million for the three months ended June 30, 2026 compared to $2.4 million for the three months ended June 30, 2025

• | Backlog increased 37.2% to $84.0 million as of June 30, 2026 compared to $61.2 million as of June 30, 2025

ORLANDO, Florida (August 12, 2026 ) — M-tron Industries, Inc. (NYSE American: MPTI) ("Mtron" or the "Company"), a U.S.-based designer and manufacturer of highly-engineered electronic components and solutions for the aerospace and defense, avionics, and space industries, announced strong financial results for the three and six months ended June 30, 2026 .

"Our second quarter results reflect continued momentum across our defense and aerospace business, with revenue increasing 13.8% and net income increasing 19.9%, and notably, adjusted EBITDA increasing 40.6% from Q2 2025 to $3.4 million," said Cameron Pforr, Chief Executive Officer. "This continues to demonstrate the effectiveness of Mtron's transformation into a strategic RF supplier with revenues doubling and earnings tripling from the Company's performance at the time of our 2022 initial public offering. Our backlog is continuing to grow with another strong quarter of bookings. The strength we are seeing in our core markets gives us confidence in the trajectory of the business, and we remain focused on translating that growth into durable, long-term value for our shareholders."

Three Months Ended June 30, | Six Months Ended June 30,
(in thousands, except share data) | 2026 | 2025 | % Change | 2026 | 2025 | % Change
U.S. GAAP Financial Measures
Revenues | 15,109 | 13,282 | 13.8 | % | 29,795 | 26,014 | 14.5 | %
Gross margin | 41.2 | % | 43.6 | % | (5.5 | %) | 43.0 | % | 43.0 | % | 0.0 | %
Net income | 1,870 | 1,560 | 19.9 | % | 4,258 | 3,190 | 33.5 | %
Net income per diluted share | 0.43 | 0.53 | (18.9 | %) | 1.0736 | 1.0883 | (1.8 | %)
Non-GAAP Financial Measures (a)
Adjusted EBITDA | 3,401 | 2,419 | 40.6 | % | 6,573 | 4,921 | 33.6 | %

(a) | A reconciliation of non-GAAP financial measures to the most comparable GAAP measure is provided at the end of this press release.

Results from Operations

Second Quarter 2026

Revenu e was $15.1 million for the three months ended June 30, 2026 compared with $13.3 million for the three months ended June 30, 2025 . The increase was primarily due to continued strong aerospace and defense program shipments and quarter over quarter growth for both avionics and space product shipments.

Gross margin was 41.2% for the three months ended June 30, 2026 compared with 43.6% for the three months ended June 30, 2025 . The decrease reflects the impact of approximately $0.5 million of stock-based compensation recorded in Manufacturing cost of sales in connection with the 2025 bonus awards, a 3.1% impact to gross margin. This charge is not expected to recur at comparable levels in future periods. There was no such stock-based compensation in the three months ended June 30, 2025 for the 2024 bonus award.

Net income was $1.9 million , or $0.43 per diluted share, for the three months ended June 30, 2026 compared with $1.6 million , or $0.53 per diluted share, for the three months ended June 30, 2025 . Current period results include $1.0 million of non-cash stock-based compensation expense associated with the accelerated vesting of the 2025 bonus award. This charge is not expected to recur at comparable levels in future periods. The decrease in diluted earnings per share is due to the increase in weighted shares outstanding related to the rights offering that was completed in April 2026.

Adjusted EBITDA was $3.4 million for the three months ended June 30, 2026 compared with $2.4 million for the three months ended June 30, 2025 . The increase was primarily due to higher revenues partially offset by an increase in engineering, selling and administrative expenses.

Fiscal Year to Date 2026

Revenue was $29.8 million for the six months ended June 30, 2026 compared with $26.0 million for the six months ended June 30, 2025 . The increase was primarily due to continued strong aerospace and defense program shipments as well as year-over-year growth in avionics product shipments.

Net income was $4.3 million , or $1.07 per diluted share, for the six months ended June 30, 2026 compared with $3.2 million , or $1.09 per diluted share, for the six months ended June 30, 2025 . This reflects $1.0 million of non-cash stock compensation associated with the accelerated vesting of the 2025 bonus award. The increase in net income was driven by higher shipments partially offset by an increase in overall operating expenses, which grew at a slower rate than revenues. The decrease in earnings per diluted share was primarily due to the increase in weighted shares outstanding related to the rights offering completed in April 2026.

Adjusted EBITDA was $6.6 million for the six months ended June 30, 2026 compared with $4.9 million for the six months ended June 30, 2025 . The increase was primarily due to higher revenues partially offset by an increase in engineering, selling and administrative expenses.

Backlog

Backlog was $84.0 million as of June 30, 2026 compared to $76.4 million as of December 31, 2025 and $61.2 million as of June 30, 2025 . The increase in backlog reflects broad demand for our products including continued purchasing under several large aerospace and defense programs, the initiation of orders for new aerospace and defense programs, and a recent uptick in avionics and space industry orders.

Strategic Investment

During the quarter, the Company made a small investment in a synchronization and timing systems company Skyline Instruments, LLC, which is making significant advancements critical for the synchronization of RF sensor data and operations in GPS denied environments. This is part of the Company's effort to continue to innovate and learn about future market opportunities in areas critical to our national defense.

Investor Call

Management, including Mr. Pforr, will host a conference call with the investment community on Thursday August 13, 2026, to discuss the Company's second quarter 2026 results and to respond to investor questions.

The call will begin at 10:30 a.m. Eastern Time (U.S. and Canada) on Thursday August 13, 2026, and can be accessed using the dial-in details below:

Toll-Free Dial-in Number: | +1 833 461 5787

Toll Dial-in Number: | +1 585 542 9983

Conference ID: | 466 106 739

Webcast URL: | https://events.q4inc.com/attendee/466106739

An archive will be available after the call on the Investor Relations section of Mtron's website at ir.mtron.com, along with Mtron's earnings release.

About Mtron

M-tron Industries, Inc. (NYSE American: MPTI) designs, manufactures, and markets highly engineered, high reliability frequency and spectrum control products and solutions. As an engineering-centric company, Mtron provides close support to its customers throughout our products' entire life cycle, including product design, prototyping, production, and subsequent product upgrades. Mtron has design and manufacturing facilities in Orlando, Florida, and Yankton, South Dakota, a sales office in Hong Kong, and a manufacturing facility in Noida, India. For more information, visit www.mtron.com.

M-tron Industries, Inc.

Condensed Consolidated Statements of Operations

(Unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
(in thousands, except share data) | 2026 | 2025 | 2026 | 2025
Revenues | 15,109 | 13,282 | 29,795 | 26,014
Costs and expenses:
Manufacturing cost of sales | 8,883 | 7,490 | 16,975 | 14,816
Engineering, selling and administrative | 4,507 | 3,948 | 8,491 | 7,341
Total costs and expenses | 13,390 | 11,438 | 25,466 | 22,157
Operating income | 1,719 | 1,844 | 4,329 | 3,857
Other income (expense):
Interest income, net | 690 | 124 | 1,060 | 235
Other income (expense), net | 34 | 27 | (88 | 17
Total other income, net | 724 | 151 | 972 | 252
Income before income taxes | 2,443 | 1,995 | 5,301 | 4,109
Income tax expense | 573 | 435 | 1,043 | 919
Net income | 1,870 | 1,560 | 4,258 | 3,190
Income per common share:
Basic | 0.46 | 0.55 | 1.13 | 1.12
Diluted | 0.43 | 0.53 | 1.07 | 1.09
Weighted average shares outstanding:
Basic | 4,056,379 | 2,853,383 | 3,775,004 | 2,848,419
Diluted | 4,339,332 | 2,934,594 | 3,965,962 | 2,931,053

M-tron Industries, Inc.

Condensed Consolidated Balance Sheets

(Unaudited)

(in thousands) | June 30, 2026 | December 31, 2025
Assets:
Current assets:
Cash and cash equivalents | 96,245 | 20,891
Accounts receivable, net of allowance of $208 and $204, respectively | 8,221 | 6,656
Inventories, net | 10,884 | 9,673
Prepaid expenses and other current assets | 2,523 | 1,662
Warrant proceeds receivable | — | 22,335
Total current assets | 117,873 | 61,217
Property, plant and equipment, net | 7,290 | 6,514
Right-of-use lease asset | 182 | 217
Intangible assets, net | 40 | 40
Deferred income tax asset | 196 | 272
Other assets | 354 | 123
Total assets | 125,935 | 68,383
Liabilities:
Total current liabilities | 7,088 | 4,891
Non-current liabilities | 132 | 277
Total liabilities | 7,220 | 5,168
Total stockholders' equity | 118,715 | 63,215
Total liabilities and stockholders' equity | 125,935 | 68,383

Non-GAAP Financial Measures

Throughout this press release, including the results from operations, the Company presents its financial condition and results of operations in the way it believes will be most meaningful and representative of its business results. Some of the measurements the Company uses are "Non-GAAP financial measures" under SEC rules and regulations. The non-GAAP financial measures the Company presents are listed below and may not be comparable to similarly-named measures reported by other companies. the reconciliations of such measures to the most comparable GAAP measures in accordance with Regulation G are included within the relevant tables attached to this press release. The presentation of this additional information is not meant to be considered in isolation or as a substitute for net earnings or diluted earnings per share prepared in accordance with GAAP.

The Company uses the following operating performance measure because the Company believes it provides both management and investors with a more complete understanding of the underlying operational results and trends and our marketplace performance

Adjusted EBITDA is derived by excluding the items set forth below from Income before income taxes. Excluded items include the following:

• | Interest income

• | Interest expense

• | Depreciation

• | Amortization

• | Non-cash stock-based compensation

• | Other discrete items that might have a significant impact on comparable GAAP measures and could distort the evaluation of our normal operating performance

Reconciliation of GAAP Income Before Income Taxes to Non-GAAP Adjusted EBITDA

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-26_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Mtron is engaged in the designing, manufacturing and marketing of highly-engineered, high reliability frequency and spectrum control products used to control the frequency or timing of signals in electronic circuits in various applications. Mtron's primary markets are aerospace and defense, space, and avionics.

The accompanying consolidated financial statements include the accounts of the Company and all of its majority-owned subsidiaries.

For a discussion of the year ended December 31, 2024 compared to the year ended December 31, 2023, refer to Part II, Item 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations" in our Annual Report on Form 10-K for the year ended December 31, 2024, filed with the SEC on March 27, 2025, which is available free of charge on the SEC's website at https://www.sec.gov and on our website at ir.mtron.com.

Trends and Uncertainties

We are not aware of any material trends or uncertainties, other than the global economic conditions affecting our industry generally, that may reasonably be expected to have a material impact, favorable or unfavorable, on our revenues or income other than those listed in Part I, Item 1A, Risk Factors, of this Annual Report on Form 10-K.

Results of Operations

The following table presents our Consolidated Statements of Operations for the periods indicated:

Year Ended December 31,
(in thousands) | 2025 | 2024 | $ Change | % Change
Revenues | 54,417 | 49,012 | 5,405 | 11.0 | %
Costs and expenses:
Manufacturing cost of sales | 30,269 | 26,372 | 3,897 | 14.8 | %
Engineering, selling and administrative | 13,857 | 13,246 | 611 | 4.6 | %
Total costs and expenses | 44,126 | 39,618 | 4,508 | 11.4 | %
Operating income | 10,291 | 9,394 | 897 | 9.5 | %
Other income:
Interest income, net | 539 | 243 | 296 | 121.8 | %
Other income, net | 124 | 138 | (14 | -10.1 | %
Total other income, net | 663 | 381 | 282 | 74.0 | %
Income before income taxes | 10,954 | 9,775 | 1,179 | 12.1 | %
Income tax expense | 2,507 | 2,139 | 368 | 17.2 | %
Net income | 8,447 | 7,636 | 811 | 10.6 | %

2025 compared to 2024

Total Revenues

Total revenues increased $5,405, or 11.0%, from $49,012 in 2024 to $54,417 in 2025 primarily due to strong defense program product and solution shipments, as well as an increase in shipments in the avionics and industrials sectors.

Total Costs and Expenses

Total costs and expenses increased $4,508, or 11.4%, from $39,618 in 2024 to $44,126 in 2025 primarily due to:

• | a $3,897, or 14.8%, increase in Manufacturing cost of sales from $26,372 in 2024 to $30,269 in 2025 driven by the increase in production of several new products, which result in higher initial manufacturing costs, as well as the impact of tariffs; and

• | a $611, or 4.6%, increase in Engineering, selling and administrative from $13,246 in 2024 to $13,857 in 2025 driven by continued investment in research and development; higher sales commissions consistent with the growth in revenues; higher stock-based compensation; higher sales and marketing costs; and an increase in administrative and corporate expenses consistent with the overall growth in the business.

The Company's total costs and expenses for 2024 included bonus expense of approximately $1.5 million, or 3.0% of revenues, which was not incurred in 2025.

Gross Margin

Gross margin (Revenues less Manufacturing cost of sales as a percentage of Revenues) decreased 180 basis points from 46.2% in 2024 to 44.4% in 2025 reflecting product mix and higher tariff-related costs.

Total Other Income, Net

Total other income, net increased $282, or 74.0%, from $381 in 2024 to $663 in 2025 primarily due to a $296 increase in Interest income, net from $243 in 2024 to $539 in 2025 driven by higher average balances invested in money market mutual funds.

Income Tax Expense

Income tax expense
increased
$368, or
17.2%, from
$2,139 in
2024 to
$2,507 in
2025 primarily due to the increase in Income before income taxes discussed above.

Backlog

As of December 31, 2025, our order backlog was $76,425, an increase of $29,186, or 61.8%, from $47,239 as of December 31, 2024. The increase in backlog from December 31, 2024 reflects the nature of a program centric business model, which can materially affect backlog based on the timing and size of these orders.

The backlog of unfilled orders includes amounts based on signed contracts and purchase orders, which are likely to be fulfilled substantially within the next 12 to 24 months. Order backlog is adjusted quarterly to reflect project cancellations, deferrals, revised project scope and cost. We expect to fill the vast majority of our order backlog as of December 31, 2025 during 2026 and 2027, but cannot provide assurances as to what portion of the order backlog will be fulfilled in any given year.

Non-GAAP Financial Measures

To supplement our Consolidated Financial Statements presented on a U.S. GAAP basis, the Company presents its financial condition and results of operations in the way it believes will be most meaningful and representative of its business results. Some of the measurements the Company uses are "Non-GAAP financial measures" under SEC rules and regulations. The non-GAAP financial measures the Company presents are listed below and may not be comparable to similarly-named measures reported by other companies. The presentation of this additional information is not meant to be considered in isolation or as a substitute for net earnings or diluted earnings per share prepared in accordance with U.S. GAAP.

The Company uses the following operating performance measure because the Company believes it provides both management and investors with a more complete understanding of the underlying operational results and trends and our marketplace performance as well as a more accurate view of the Company's ability to generate profits:

Adjusted Earnings Before Interest, Taxes, Depreciation, and Amortization ("EBITDA") is derived by excluding the items set forth below from Income before income taxes. Excluded items include the following:

• | Interest income

• | Interest expense

• | Depreciation

• | Amortization

• | Non-cash stock-based compensation

• | Other discrete items that might have a significant impact on comparable GAAP measures and could distort the evaluation of our normal operating performance.

Reconciliation of GAAP Income Before Income Taxes to EBITDA and Non-GAAP Adjusted EBITDA

The following table presents a reconciliation of income before income taxes to Adjusted EBITDA, a non-GAAP measure:

Three Months Ended December 31, | Year Ended December 31,
(in thousands, except share data) | 2025 | 2024 | 2025 | 2024
Income before income taxes | 4,082 | 2,758 | 10,954 | 9,775
Adjustments:
Interest income, net | (161 | (104 | (539 | (243
Depreciation | 286 | 251 | 1,086 | 968
Amortization | — | — | — | 5
Total adjustments | 125 | 147 | 547 | 730
EBITDA | 4,207 | 2,905 | 11,501 | 10,505
Non-cash stock compensation | 278 | 151 | 1,081 | 636
Adjusted EBITDA | 4,485 | 3,056 | 12,582 | 11,141

Three months ended December 31, 2025 compared to three months ended December 31, 2024

Adjusted EBITDA increased $1,429 from $3,056 for the three months ended December 31, 2024 to $4,485 for the three months ended December 31, 2025. The increase was primarily due to higher revenues and lower engineering, selling and administrative expenses partially offset by lower gross margin discussed above.

Year ended 2025 compared to Year ended 2024

Adjusted EBITDA increased $1,441 from $11,141 in 2024 to $12,582 in 2025. The increase was primarily due to higher revenues discussed above, continued operating leverage, and lower incentive compensation partially offset by lower gross margin discussed above. Adjusted EBITDA in 2024 included bonus expense of approximately 3.0% of revenues, which was not incurred in 2025.

Liquidity and Capital Resources

Overview

Liquidity refers to our ability to access sufficient sources of cash to meet the requirements of our operating, investing and financing activities.

Capital refers to our long-term financial resources available to support business operations and future growth.

Our ability to generate and maintain sufficient liquidity and capital depends on the profitability of the business, timing of cash flows, general economic conditions and access to the capital markets and the other sources of liquidity and capital described herein.

As of December 31, 2025 and 2024, Cash and cash equivalents were $20,891 and $12,641, respectively.

Cash Flow Activity

The following table presents the cash flow activity for the period indicated:

As of December 31,
(in thousands) | 2025 | 2024
Cash and cash equivalents, beginning of year | 12,641 | 3,913
Cash provided by operating activities | 10,659 | 7,521
Cash used in investing activities | (2,551 | (1,898
Cash provided by financing activities | 142 | 3,105
Net change in cash and cash equivalents | 8,250 | 8,728
Cash and cash equivalents, end of year | 20,891 | 12,641

Operating Activities

Cash provided by operating activities was $10,659 in 2025 compared to $7,521 in 2024, an increase of $3,138 primarily due to the following:

• | Higher net income;

• | Higher non-cash adjustments, including:

◦ | Stock-based compensation expense, which increased $445 from $636 in 2024 to $1,081 in 2025;

◦ | Deferred income tax provision, which decreased $1,268 from $212 in 2024 to $1,480 in 2025;

• | Working capital movements, including:

◦ | Accounts receivable, which decreased $186 in 2025 compared to an increase of $2,040 in 2024, reflecting shorter customer payment cycles;

◦ | Inventories, net, which increased $164 in 2025 compared to $625 in 2024;

◦ | Prepaid expenses and other assets, which increased $1,156 in 2025 compared to $165 in 2024, primarily due to higher income taxes receivable; and

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-26_item1_business.md)

Item 1. | Business

In this Annual Report on Form 10-K, the terms "Mtron," the "Company," "we," "us," and "our" refer collectively to M-tron Industries, Inc. and its subsidiaries. Unless otherwise stated, all dollar amounts are in thousands.

General

Originally founded in 1965, M-tron Industries, Inc. is engaged in the designing, manufacturing and marketing of highly engineered, high reliability frequency and spectrum control products used to control the frequency or timing of signals in electronic circuits in various applications. Mtron's primary markets are aerospace and defense, avionics, industrials, and space.

Our component-level devices and integrated modules are used extensively in electronic systems for applications in aerospace and defense, avionics, satellites, global positioning systems, down-hole drilling, medical systems, instrumentation, and industrial devices. As an engineering-centric company, Mtron provides close support to the customer throughout its products' entire life cycles, including product design, prototyping, production and subsequent product upgrades and maintenance. This collaborative approach has resulted in the development and growth of long-standing business relationships with its customers.

The Company has manufacturing facilities in Orlando, Florida; Yankton, South Dakota; and Noida, India. The Company also has a sales office in Hong Kong. All of Mtron's production facilities are International Organization for Standardization ("ISO") 9001:2015 certified (the international standard for creating a quality management system) and Restriction of Hazardous Substances ("RoHS") compliant. In addition, the Company's U.S. production facilities in Orlando and Yankton are International Traffic in Arms Regulations ("ITAR") registered and International Aerospace Quality Group AS9100 Rev D certified and our Yankton, South Dakota production facility is Military Standard ("MIL-STD") 790 certified. Mtron's production facility in India operates under a Manufacturing License Agreement ("MLA") issued by the United States Department of State.

We maintain our executive offices at 2525 Shader Road, Orlando, Florida 32804. Our telephone number is (407) 298-2000.

Our common stock is traded on the NYSE American ("NYSE") under the symbol "MPTI."

Business Strategy

Our objective is to deliver long-term growth to our stockholders and maximize stockholder value. Mtron employs a market-based approach of designing and offering new products to its customers through both organic research and development, and through strategic partnerships, joint ventures, acquisitions, or mergers. We seek to leverage our core strength as an engineering leader to expand client access, add new capabilities and continue to diversify our product offerings. We believe that successful execution of this strategy will lead to a transformation of our product portfolio towards multi-component integrated offerings, longer product life cycles, better margins and an improved competitive position.

Business Segment

The Company conducts its business through one business segment: Electronic Components, which includes all products manufactured and sold by Mtron.

Products

Mtron's portfolio is divided into three product groupings: Frequency Control, Spectrum Control and Integrated Microwave Assemblies (Solutions), and has expanded from primarily crystal-based components to include higher levels of integration, advanced materials science, cavity-based products, and various types of compensation methods employing integrated circuits and other methods to create products geared for applications that require high reliability in harsh environments. These products are differentiated by their precise level of accuracy, stability over time and within harsh environments, and very low phase noise.

Frequency Control

Mtron's Frequency Control product group includes a broad portfolio of quartz crystal resonators, clock oscillators, voltage-controlled crystal oscillator ("VCXO"), temperature-compensated crystal oscillator ("TCXO"), oven-controlled crystal oscillator ("OCXO"), and temperature-compensated voltage-controlled crystal oscillator ("TCVCXO") devices which meet some of the tightest specifications, including Institute of Electrical and Electronics Engineers ("IEEE") 1588 standards. These devices may be based on quartz, quartz micro-electromechanical systems ("MEMS") or advanced materials designed to achieve higher performance levels beyond what is achieved with quartz. Mtron's products offer high reliability over a wide temperature range and are well-suited for harsh environments, including shock and vibration-resistant oscillators with low-g sensitivity. These products are designed for applications within aerospace and defense, avionics, and industrial markets.

Spectrum Control

Mtron's Spectrum Control product group includes a wide array of radio frequency ("RF"), microwave and millimeter wave filters and diplexers covering a frequency range from 1 MHz to 30 GHz, and solid-state power amplifiers covering a frequency range from 300 MHz to 26 GHz, with power output from 10 Watts to 10kW. Filter devices include crystal, ceramic, LC, planar, combline, cavity, interdigital and metal insert waveguide, as well as switched filter arrays and RF subsystems. Power amplifiers add active devices to Mtron's portfolio and include gallium nitride ("GaN"), gallium arsenide ("GaAS") field-effect transistors ("FET"), laterally-diffused metal-oxide semiconductors ("LDMOS") and chip and wire technologies in narrow or broadband, module or rack-mounted packages. These products are employed in applications within the commercial and military aerospace and defense, space, avionics, and industrial markets.

Radio Frequency Solutions

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-12_2-02-results.md, 10-K_2026-03-26_item7_mdna.md, 10-K_2026-03-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
