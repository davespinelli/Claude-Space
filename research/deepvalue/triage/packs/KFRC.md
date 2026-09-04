# Triage pack — KFRC · KFORCE INC

_Generated 2026-09-04 16:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** KFRC · **Name:** KFORCE INC
- **CIK:** 0000930420
- **SIC:** 7363 — Services-Help Supply Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/KFRC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** KFORCE INC
- **CIK:** 930,420 · **SIC:** 7363 (Services-Help Supply Services) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 53.95 |
| mktcap | $966.2M |
| ev | $1.1B |
| ev_ebit | 21.4x |
| fcf | $46.8M |
| fcf_yield | 4.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 17.2% |
| net_debt | $106.8M |
| net_debt_ebit | 2.1x |
| cash | $330k |
| ltd | $107.1M |
| equity | $123.6M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.3B |
| revenue_prior | $1.4B |
| rev_growth | -5.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $50.1M |
| net_income | $34.8M |
| cfo | $61.6M |
| capex | $14.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -3.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 17,909,000 |
| shares_py | 18,599,000 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 99.1% |
| r6m | 98.3% |
| off_52w_high | -10.8% |
| adv20 | $14.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.48 |
| r_ev_ebit | 0.42 |
| r_roic | 0.85 |
| r_rev_growth | 0.18 |
| r_buyback | 0.84 |
| score | 0.60 |

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
| rank | 143 |

**Screen rationale:** high ROIC 17.2%; buying back stock -3.7%; 12-1 momentum 99.1%


## 3. Share count trend

- Shares outstanding: **17,909,000** (CY2026Q2I) vs **18,599,000** prior year (CY2025Q2I)
- Change: **-3.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 5 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 2,000 sh / $109,800 -> net $-109,800 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| J | 11 |
| L | 1 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-27_2-02-results.md)

_Extraction: started at the first release heading, 'THIRD QUARTER REVENUES EXPECTED TO GROW SEQUENTIALLY AND YEAR OVER YEA'; skipped 8 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT-99.1 (exhibit991q22026.htm)

THIRD QUARTER REVENUES EXPECTED TO GROW SEQUENTIALLY AND YEAR OVER YEAR GROWTH EXPECTED TO ACCELERATE

GROSS PROFIT MARGINS IN THE SECOND QUARTER IMPROVED 140 BASIS POINTS YEAR OVER YEAR

EPS OF $0.73 INCREASED NEARLY 24% YEAR OVER YEAR

TAMPA, FL, July 27, 2026 — Kforce Inc. (NYSE: KFRC), a solutions firm that specializes in technology and other professional staffing services, today announced results for the second quarter of 2026.

Joseph J. Liberatore, President and Chief Executive Officer, said, "We are extremely pleased to have successfully delivered results in the second quarter that again exceeded our expectations from both a revenue and profitability perspective. Overall revenues positively inflected in the first quarter of 2026, meaningfully expanded in the second quarter, and our guidance for the third quarter contemplates continued sequential improvement. There has been a lot of discussion about whether we and the broader sector can continue to deliver revenue growth given the much-speculated negative demand impact of AI tools and technologies. We believe that the need for high-quality talent remains essential in virtually all technology initiatives, including AI-related investments. Encouragingly, we have been successful at delivering three consecutive quarters of revenue growth that has returned to pre-pandemic, and thus pre-AI advancement, averages while generating operating margins that are meaningfully higher than those achieved at comparable historical levels.

I am incredibly proud of the determination of our people and deeply appreciative of the trust our world-class clients continue to place in Kforce as we help them advance more meaningful, higher-value engagements. We believe our go-to-market approach, shaped by our integrated strategy efforts, is gaining traction. Across the Firm, our people are operating more fully as One Kforce, bringing the full breadth of our capabilities to bear across our service offerings."

Quarterly Financial Highlights

• Revenue for the quarter ended June 30, 2026 was $349.3 million, an increase of 5.7% (4.1% on a billing day basis) sequentially and 4.5% year over year.

• Technology Flex revenue increased 5.6% (4.0% on a billing day basis) sequentially and 4.0% year over year. FA Flex revenue increased 2.4% (0.8% on a billing day basis) sequentially and 6.0% year over year.

• Gross profit margins of 28.5% increased 120 basis points sequentially and 140 basis points year over year. Flex gross profit margins of 26.9% increased 100 basis points sequentially and increased 110 basis points year over year.

• SG&A expenses as a percentage of revenue was 22.7% for the quarter ended June 30, 2026, which decreased 50 basis points sequentially and increased 50 basis points year over year.

• Operating margins were 5.4% for the quarter ended June 30, 2026, which increased 180 basis points sequentially and 90 basis points year over year.

• Diluted earnings per share for the quarter ended June 30, 2026 was $0.73, an increase of 58.7% sequentially and 23.7% year over year.

• We returned $9.6 million in capital to our shareholders in the form of open market share repurchases and quarterly dividends during the second quarter of 2026.

• Our Board of Directors approved a third quarter cash dividend of $0.40 per share to shareholders of record as of the close of business on September 11, 2026, which will be payable on September 25, 2026.

Third Quarter 2026 - Guidance

Looking forward to the third quarter of 2026, there will be 64 billing days, compared to 64 billing days in the second quarter of 2026 and third quarter of 2025. Current estimates for the third quarter of 2026 are:

• Revenue of $349 million to $357 million

• Earnings per share of $0.71 to $0.79

• Gross profit margins of 28.1% to 28.3%

• Flex gross profit margins of 26.7% to 26.9%

• SG&A expenses as a percent of revenue of 22.2% to 22.4%

• Operating margin of 5.3% to 5.7%

• WASO of 17.2 million

• Effective tax rate of 30.4%

Conference Call

On Monday, July 27, 2026, Kforce will host a conference call at 5:00 p.m. E.T. to discuss these results. The dial-in number is (833) 461-5787 and the conference passcode is 778 562 393. The prepared remarks for this call and webcast are available on the Investor Relations page of the Kforce Inc. website in the News and Events section. The replay of the call can be accessed at http://investor.kforce.com.

About Kforce Inc.

Kforce Inc. (the "Firm") is a solutions firm specializing in technology, finance and accounting, and other professional staffing services. Our KNOWLEDGEforce® empowers industry-leading companies to achieve their digital transformation goals. We curate teams of technical experts who deliver solutions custom-tailored to each client's needs. These scalable, flexible outcomes are shaped by deep market knowledge, thought leadership and our multi-industry expertise.

Our integrated approach is rooted in over 60 years of proven success deploying highly skilled professionals on a temporary and direct-hire basis. Each year, approximately 17,000 talented experts work with Fortune 500 and other leading companies. Together, we deliver Great Results Through Strategic Partnership and Knowledge Sharing®.

Michael R. Blackman, Chief Corporate Development Officer

(813) 552-2927

Consolidated Balance Sheets

(In Thousands)

(Unaudited)

June 30, 2026 | December 31, 2025
ASSETS
Current assets:
Cash and cash equivalents | 330 | 2,142
Trade receivables, net of allowances | 220,857 | 190,461
Prepaid expenses and other current assets | 10,118 | 9,669
Total current assets | 231,305 | 202,272
Fixed assets, net | 5,026 | 6,023
Other assets, net | 145,003 | 129,267
Deferred tax assets, net | 3,818 | 3,036
Goodwill | 25,040 | 25,040
Total assets | 410,192 | 365,638
LIABILITIES AND STOCKHOLDERS' EQUITY
Current liabilities:
Accounts payable and other accrued liabilities | 62,863 | 67,609
Accrued payroll costs | 50,297 | 42,328
Current portion of operating lease liabilities | 3,477 | 3,342
Income taxes payable | 3,126 | 451
Total current liabilities | 119,763 | 113,730
Long-term debt – credit facility | 107,100 | 66,400
Other long-term liabilities | 59,701 | 60,905
Total liabilities | 286,564 | 241,035
Commitments and contingencies
Stockholders' equity:
Preferred stock | — | —
Common stock | 743 | 742
Additional paid-in capital | 566,505 | 558,297
Retained earnings | 558,001 | 552,180
Treasury stock, at cost | (1,001,621) | (986,616)
Total stockholders' equity | 123,628 | 124,603
Total liabilities and stockholders' equity | 410,192 | 365,638

Kforce Inc.

Key Statistics

(Unaudited)

Q2 2026 | Q1 2026 | Q2 2025
Total Firm
Total Revenue (000's) | 349,331 | 330,364 | 334,316
GP % | 28.5% | 27.3% | 27.1%
Flex revenue (000's) | 341,829 | 324,228 | 328,411
Hours (000's) | 3,926 | 3,772 | 3,787
Flex GP % | 26.9% | 25.9% | 25.8%
Direct Hire revenue (000's) | 7,502 | 6,136 | 5,905
Placements | 309 | 276 | 269
Average fee | 24,278 | 22,270 | 21,964
Billing days | 64 | 63 | 64
Technology
Total Revenue (000's) | 323,876 | 305,963 | 310,527
GP % | 27.6% | 26.5% | 26.3%
Flex revenue (000's) | 320,035 | 302,955 | 307,844
Hours (000's) | 3,520 | 3,365 | 3,404
Flex GP % | 26.8% | 25.7% | 25.6%
Direct Hire revenue (000's) | 3,841 | 3,008 | 2,683
Placements | 148 | 139 | 116
Average fee | 26,038 | 21,659 | 23,154
Finance and Accounting
Total Revenue (000's) | 25,455 | 24,401 | 23,789
GP % | 39.3% | 37.1% | 38.1%
Flex revenue (000's) | 21,794 | 21,273 | 20,567
Hours (000's) | 406 | 407 | 383
Flex GP % | 29.1% | 27.9% | 28.5%
Direct Hire revenue (000's) | 3,661 | 3,128 | 3,222
Placements | 161 | 137 | 153
Average fee | 22,671 | 22,891 | 21,063

Kforce Inc.

Non-GAAP Financial Measures

(Unaudited)

In addition to our financial results presented in accordance with GAAP, Kforce may use certain non-GAAP financial measures, which we believe provide useful information to investors in evaluating our core operating performance. The following non-GAAP financial measures presented may not provide information that is directly comparable to that provided by other companies, as other companies may calculate such financial results differently. Our non-GAAP financial measures are not measurements of financial performance under GAAP and should not be considered as alternatives to amounts presented in accordance with GAAP. We view these non-GAAP financial measures as supplemental, which are not intended to be a substitute for, or superior to, the information provided by GAAP financial results. A reconciliation of the non-GAAP financial measures to the most directly comparable GAAP financial measures is provided below.

Revenue Growth Rates

"Revenue growth rates," a non-GAAP financial measure, is defined by Kforce as revenue growth after removing the impacts on reported revenues from the changes in the number of billing days. Management believes this data is particularly useful because it aids in evaluating revenue trends over time. The impact of billing days is calculated by dividing each comparative period's reported revenues by the number of billing days for the respective period to arrive at a per billing day amount for each quarter. Growth rates are then calculated using the per billing day amounts as a percentage change compared to the respective period. Management calculates the number of billing days for each reporting period based on the number of holidays and business days in the quarter.

Sequential Growth Rates (GAAP)
2026 | 2025
Q2 | Q1 | Q4 | Q3 | Q2
Technology Flex | 5.6% | (0.2)% | (0.2)% | (1.2)% | 1.8%
FA Flex | 2.4% | (5.6)% | 2.4% | 6.9% | 2.1%
Total Flex revenue | 5.4% | (0.6)% | (0.1)% | (0.7)% | 1.8%
Sequential Growth Rates (Non-GAAP)
2026 | 2025
Q2 | Q1 | Q4 | Q3 | Q2
Billing Days | 64 | 63 | 62 | 64 | 64
Technology Flex | 4.0% | (1.8)% | 3.0% | (1.2)% | 0.2%
FA Flex | 0.8% | (7.1)% | 5.7% | 6.9% | 0.5%
Total Flex revenue | 3.8% | (2.2)% | 3.2% | (0.7)% | 0.2%

Year-Over-Year Growth Rates (GAAP)
2026 | 2025
YTD | Q2 | Q1 | YTD | Q2 | Q1
Technology Flex | 2.1% | 4.0% | 0.2% | (5.0)% | (5.0)% | (5.0)%
FA Flex | 5.8% | 6.0% | 5.7% | (20.1)% | (16.8)% | (23.2)%
Total Flex revenue | 2.3% | 4.1% | 0.5% | (6.1)% | (5.8)% | (6.4)%
Year-Over-Year Growth Rates (Non-GAAP)
2026 | 2025
YTD | Q2 | Q1 | YTD | Q2 | Q1
Billing Days | 127 | 64 | 63 | 127 | 64 | 63
Technology Flex | 2.1% | 4.0% | 0.2% | (4.3)% | (5.0)% | (3.5)%
FA Flex | 5.8% | 6.0% | 5.7% | (19.5)% | (16.8)% | (22.0)%
Total Flex revenue | 2.3% | 4.1% | 0.5% | (5.4)% | (5.8)% | (4.9)%

Free Cash Flow

"Free Cash Flow," a non-GAAP financial measure, is defined by Kforce as net cash provided by operating activities determined in accordance with GAAP, less capital expenditures. Management believes this provides an additional way of viewing our liquidity that, when viewed with our GAAP results, provides a more complete understanding of factors and trends affecting our cash flows and is useful information to investors as it provides a measure of the amount of cash generated from the business that can be used for strategic opportunities including investing in our business, repurchasing common stock, paying dividends or making acquisitions. Free Cash Flow has limitations due to the fact that it does not represent the residual cash flow available for discretionary expenditures. Therefore, we believe it is important to view Free Cash Flow as a complement to, but not a replacement of, our unaudited condensed consolidated statements of cash flows.

The following table presents a reconciliation of Cash (Used in) Provided by Operating Activities to Free Cash Flow:

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-20_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

EXECUTIVE SUMMARY

The following is an executive summary of what Kforce believes are highlights for the year ended December 31, 2025, which should be considered in the context of the additional discussions herein and in conjunction with the consolidated financial statements and notes thereto.

• Revenue for the year ended December 31, 2025 decreased 5.4% (5.1% on a billing day basis) to $1.33 billion in 2025 from $1.41 billion in 2024. Revenue decreased 4.8% (4.5% on a billing day basis) and 12.3% (11.9% on a billing day basis) for Technology and FA, respectively, in 2025, primarily driven by decreases in consultants on assignment. We believe these decreases are primarily related to macroeconomic uncertainties and the natural impacts of the early phases of significant technology evolutions (such as AI) as companies assess the implications on their businesses and their investment strategies.

• Flex revenue decreased 5.3% (4.9% on a billing day basis) to $1.30 billion in 2025 from $1.38 billion in 2024. In 2025, Flex revenue decreased 4.7% (4.4% on a billing day basis) for Technology and 12.8% (12.5% on a billing day basis) for FA. Notably, Tech Flex revenue decreased 0.2% sequentially (increased 3.0% on a billing day basis), and FA Flex revenue improved sequentially 2.4% (5.7% on a billing day basis) in the fourth quarter 2025. For our FA business, this represented the third consecutive quarter of sequential improvement, primarily due to, in our opinion, the benefits of a realignment in early 2025 intended to bring a greater intensity and focus on our FA business.

• Direct Hire revenue decreased 11.1% to $25.7 million in 2025 from $28.9 million in 2024.

• Gross profit margin decreased 20 basis points to 27.2% in 2025 from 27.4% in 2024, primarily driven by a decline in the mix of Direct Hire revenue.

• Flex gross profit margin decreased 10 basis points to 25.8% for 2025 from 25.9% in 2024. Flex gross profit margin decreased 10 basis points for Technology and 80 basis points for FA in 2025 as compared to 2024. Notably, our Flex gross profit margin increased 40 basis points in our Technology business in the fourth quarter of 2025 as compared to the same period in 2024.

• Selling, General and Administrative ("SG&A") expenses as a percentage of revenue for the year ended December 31, 2025, increased to 23.0% from 22.0% in 2024, primarily driven by the declines in revenue and gross profit. In the fourth quarter of 2025, we recognized charges of $3.4 million related to refinements in our organizational structure and other non-recurring costs, which negatively impacted earnings per share for the fourth quarter of 2025 and fiscal 2025 by $0.13, net of the related tax effect.

• Net income for the year ended December 31, 2025, decreased 30.9% to $34.8 million, or $1.96 diluted earnings per share, from $50.4 million, or $2.68 diluted earnings per share, in 2024.

• The Firm returned $76.0 million of capital to our shareholders in the form of open market repurchases totaling $48.5 million, or 1.2 million shares, and quarterly dividends totaling $27.5 million during the year ended December 31, 2025. The total capital returned to shareholders in 2025 represented over 100% of operating cash flows.

• Cash provided by operating activities was $61.6 million during the year ended December 31, 2025, as compared to $86.9 million for 2024. The decrease was primarily related to lower profitability levels, higher capitalized implementation costs related to cloud computing arrangements for Workday, and the payment of 2024 federal income taxes that were deferred pursuant to IRS guidance.

RESULTS OF OPERATIONS

Certain discussions of the changes in our results of operations from the year ended December 31, 2024, as compared to the year ended December 31, 2023, have been omitted from this Form 10-K, and may be found in "Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations" of our Form 10-K for the fiscal year ended December 31, 2024, filed with the SEC on February 21, 2025.

While early 2025 began with optimism around U.S. economic growth and increased investment in technology initiatives, the macro environment remained challenging throughout the year, with significant disruption beginning in April 2025 as a result of global trade policy negotiations and the labor market data continuing to reflect a persistently weak and largely frozen hiring landscape characterized by prolonged stagnation in job gains. We believe the relative impact of AI on revenue trends and the effects of a fairly soft economy and weak labor market has created uncertainty, leading many organizations to proceed cautiously in their strategic planning and near‑term technology investments. Despite these conditions, our recent operating trends, combined with our historical experience, give us confidence that companies typically turn to flexible talent solutions as an initial step prior to making permanent hires while they assess the durability of the macro environment. The potential use of flexible talent solutions may be further influenced by the growing belief that the returns that will be generated from continuing AI investments may take longer to realize and may be more specific in nature to unique business problems rather than an overarching solution to all technology challenges. Although client conversations and broader market signals reaffirm that we are still operating in a demand‑constrained environment, our results in the fourth quarter of 2025 and the relatively stronger start to 2026 suggest greater confidence in the operating environment heading into 2026. We believe clients have maintained a meaningful backlog of strategically essential technology initiatives that they expect to advance once confidence in the macroeconomic outlook improves and their technology roadmaps are better defined.

The following table presents certain items in our Consolidated Statements of Operations as a percentage of revenue for the years ended:
December 31,
2025 | 2024 | 2023
Revenue by segment:
Technology | 92.6 | % | 92.0 | % | 90.4 | %
FA | 7.4 | 8.0 | 9.6
Total Revenue | 100.0 | % | 100.0 | % | 100.0 | %
Revenue by type:
Flex | 98.1 | % | 97.9 | % | 97.5 | %
Direct Hire | 1.9 | 2.1 | 2.5
Total Revenue | 100.0 | % | 100.0 | % | 100.0 | %
Gross profit | 27.2 | % | 27.4 | % | 27.9 | %
Selling, general and administrative expenses | 23.0 | % | 22.0 | % | 21.9 | %
Depreciation and amortization | 0.4 | % | 0.4 | % | 0.3 | %
Income from operations | 3.8 | % | 5.0 | % | 5.7 | %
Income before income taxes | 3.5 | % | 4.8 | % | 5.6 | %
Net income | 2.6 | % | 3.6 | % | 4.0 | %

Revenue. The following table presents revenue by type for each segment and the percentage change from the prior period for the years ended December 31:
(in thousands) | 2025 | Increase (Decrease) | 2024 | Increase (Decrease) | 2023
Technology
Flex revenue | 1,218,117 | (4.7) | % | 1,278,715 | (6.4) | % | 1,366,095
Direct Hire revenue | 12,154 | (13.4) | % | 14,028 | (24.0) | % | 18,458
Total Technology revenue | 1,230,271 | (4.8) | % | 1,292,743 | (6.6) | % | 1,384,553
FA
Flex revenue | 85,220 | (12.8) | % | 97,729 | (23.5) | % | 127,679
Direct Hire revenue | 13,516 | (8.9) | % | 14,836 | (24.0) | % | 19,524
Total FA revenue | 98,736 | (12.3) | % | 112,565 | (23.5) | % | 147,203
Total Flex revenue | 1,303,337 | (5.3) | % | 1,376,444 | (7.9) | % | 1,493,774
Total Direct Hire revenue | 25,670 | (11.1) | % | 28,864 | (24.0) | % | 37,982
Total Revenue | 1,329,007 | (5.4) | % | 1,405,308 | (8.3) | % | 1,531,756

Flex Revenue. The key drivers of Flex revenue are the number of consultants on assignment, billable hours, the bill rate per hour and, to a limited extent, the amount of billable expenses incurred by Kforce.

Flex revenue for our Technology business decreased 4.7% (4.4% on a billing day basis) during the year ended December 31, 2025, as compared to the same period in 2024, primarily due to a decrease in consultants on assignment, which we believe is primarily related to macroeconomic uncertainties. Our average Technology bill rate was approximately $90 per hour for the year ended December 31, 2025, which remained flat as compared to 2024. Notably, Flex revenues in our Technology business in the fourth quarter of 2025 improved 3.0% sequentially on a billing day basis. In the first quarter of 2026, we expect Technology Flex revenue to decrease on a sequential billing day basis in the low single digits due to normal seasonality and slightly decline on a year over year basis.

Our FA business experienced a decrease in Flex revenue of 12.8% (12.5% on a billing day basis) during the year ended December 31, 2025, as compared to the same period in 2024, primarily driven by a decrease in consultants on assignment, which we believe is primarily related to macroeconomic uncertainties. Notably, FA Flex revenue improved sequentially 2.4% (5.7% on a billing day basis) in the fourth quarter, representing the third consecutive quarter of sequential improvement, primarily due to more consultants on assignment. Our average FA bill rate was approximately $53 per hour for the year ended December 31, 2025, which improved 3.9% as compared to 2024. In the first quarter of 2026, we expect FA Flex revenue to decline sequentially on a billing day basis in the mid-single digits and to increase in the mid to high single digits year over year.

The following table presents the key drivers for the change in Flex revenue by segment over the prior period (in thousands):
Year Ended December 31, | Year Ended December 31,
2025 vs. 2024 | 2024 vs. 2023
Key Drivers - Increase (Decrease) | Technology | FA | Technology | FA
Volume - hours billed | (59,777) | (14,926) | (90,372) | (32,440)
Bill rate | (971) | 2,436 | 3,092 | 2,469
Billable expenses | 150 | (19) | (100) | 21
Total change in Flex revenue | (60,598) | (12,509) | (87,380) | (29,950)

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-20_item1_business.md)

ITEM 1. BUSINESS.

COMPANY OVERVIEW

Kforce Inc., along with its subsidiaries (collectively, "Kforce"), is a solutions firm specializing in technology, finance and accounting, and other professional staffing services. Through our KNOWLEDGEforce ® , we help industry-leading companies realize their digital transformation initiatives. We assemble and deploy teams of skilled technical experts who design and deliver solutions tailored to the unique requirements of each client. These scalable and flexible solutions are shaped by our deep market insight, thought leadership and broad experience across multiple industries.

Our integrated approach is rooted in more than 60 years of proven success providing highly skilled professionals on a temporary ("Flex") basis, whether through traditional staffing assignments or solutions-oriented engagements where we are responsible for delivering defined outcomes. We also support our clients by placing highly skilled professionals in permanent ("Direct Hire") roles. Each year, approximately 17,000 talented experts work with Fortune 500 and other leading companies, enabling us to achieve Great Results Through Strategic Partnership and Knowledge Sharing ® .

Over more than a decade, we have executed meaningful strategic changes to sharpen our focus on technology talent solutions, including completing a series of divestitures of businesses that were outside our core offerings.

During 2025, we expanded our delivery capabilities by establishing a development center in Pune, India, which is frequently ranked as one of the top information technology hubs in India. Beginning in January 2025, our India operations began supporting engagements with our U.S. clients. We believe that combining this offshore capability with our strong U.S. sales and delivery teams and our high-quality vendor network enhances our ability to meet clients' evolving needs, whether onshore, nearshore or offshore.

$1.1 Billion Total Capital Returned to Shareholders Since 2007 | 93% Revenue Concentrated in Technology Staffing and Solutions | #1 Recognized Brand by Technology Consultants per Staffing Industry Analysts
1962 Year Founded | KFRC Listed on New York Stock Exchange | 17,000 Consultants Placed Annually

Our operating results are influenced by several factors, including:

• the number of billing days;

• seasonal patterns in our clients' business;

• changes in holidays and vacation days taken, which is usually highest in the fourth quarter of each calendar year; and

• increased payroll-related costs resulting from the annual reset of certain U.S. state and federal employment taxes at the beginning of each calendar year, which negatively impacts gross profit and overall profitability in the first quarter of each calendar year.

Our Technology and Finance and Accounting ("FA") businesses represent our two reportable segments. Our Technology business comprises 93% of our overall revenues, and the remainder is generated by our FA business. For our Flex services, we provide our clients with qualified individuals ("consultants"), or teams of consultants, on a finite basis when the skills and experience of the consultants are the right match for our clients. For our Direct Hire services, we identify qualified individuals ("candidates") for permanent placement with our clients. We further describe our two reportable segments below.

Our Technology Business

We deliver talent solutions to our clients across a range of highly skilled disciplines including, but not limited to, systems and applications architecture and development (mobility and web); data management and analytics; cloud architecture and engineering; business and artificial intelligence ("AI"); machine learning; project and program management; and network architecture and security.

Over time, our service offerings have expanded beyond traditional staffing to include solutions-oriented engagements in response to evolving client demand. Clients continue to prioritize efficient access to specialized talent and view our solutions offering as a cost-effective means for advancing their technology initiatives. This offering has been a meaningful contributor to the financial performance of our Technology business in recent years, and we expect the mix of this offering to continue to grow in the future.

We serve clients across virtually all major industries, with a diversified presence in financial and business services, communications, insurance, retail and technology, among others.

The demand for our solutions engagements contributed positively to the results of our Technology business again in 2025, experiencing growth on a year-over-year basis, while our traditional staff augmentation offering has experienced relatively weaker results. Our integrated strategy initiative seeks to capitalize on the strong relationships we have with world-class companies by utilizing the full breadth of our existing sales teams, recruiters, consulting solutions professionals, and technology practice experts, among other teams within the Firm, to effectively provide higher value engagements to our clients, cost efficiently. We expect to continue to fuel investments in our consulting solutions offering and further integrate this capability within the Firm.

According to the September 2025 report published by Staffing Industry Analysts ("SIA"), temporary technology staffing was projected to decline 2% in 2025 and return to modest growth of 1% in 2026. Technology, as a discipline, continues to be project driven, even amidst generational technological changes like AI. We believe companies must continue investing in technology initiatives to remain competitive and to effectively change how they operate and deliver value to their customers, clients, investors and employees, regardless of macroeconomic conditions.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-20_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-20_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-20_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-27_2-02-results.md, 10-K_2026-02-20_item7_mdna.md, 10-K_2026-02-20_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
