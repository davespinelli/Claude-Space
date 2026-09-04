# Triage pack — XPEL · XPEL, Inc.

_Generated 2026-09-04 14:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** XPEL · **Name:** XPEL, Inc.
- **CIK:** 0001767258
- **SIC:** 3470 — Coating, Engraving & Allied Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/XPEL

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** XPEL, Inc.
- **CIK:** 1,767,258 · **SIC:** 3470 (Coating, Engraving & Allied Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 50.90 |
| mktcap | $1.4B |
| ev | $1.4B |
| ev_ebit | 22.4x |
| fcf | $62.9M |
| fcf_yield | 4.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 16.0% |
| net_debt | $2.8M |
| net_debt_ebit | 0.0x |
| cash | $40.7M |
| ltd | $43.5M |
| equity | $306.1M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $476.2M |
| revenue_prior | $420.4M |
| rev_growth | 13.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $62.6M |
| net_income | $51.2M |
| cfo | $66.9M |
| capex | $4.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 27,570,748 |
| shares_py | 27,672,747 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 43.0% |
| r6m | 20.7% |
| off_52w_high | -7.4% |
| adv20 | $9.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.46 |
| r_ev_ebit | 0.39 |
| r_roic | 0.83 |
| r_rev_growth | 0.73 |
| r_buyback | 0.71 |
| score | 0.67 |

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
| rank | 79 |

**Screen rationale:** high ROIC 16.0%; 12-1 momentum 43.0%


## 3. Share count trend

- Shares outstanding: **27,570,748** (CY2026Q2I) vs **27,672,747** prior year (CY2025Q2I)
- Change: **-0.4%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-31** — Item 5.02 (officer / director change or comp arrangement): (b) On July 30th, 2026, Mark Thornton notified the Board of Directors (the "Board") of XPEL, Inc. (the "Company") of his resignation as a member of the Board, effective immediately.
- **2026-05-20** — Item 1.01 (Entry into a Material Definitive Agreement): On May 15, 2026, XPEL, Inc. (the "Company"), through Harvest Ventures Holding Company, a Texas corporation and wholly-owned subsidiary of the Company ("Harvest"), completed the acquisition (the "Acquisition") of the real property and improvements constituting...
- **2026-04-29** — Item 5.02 (officer / director change or comp arrangement): On April 23, 2026, the Board of Directors of XPEL, Inc. (the "Company) appointed Mark Thornton to the Board of Directors of the Company.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 24 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 7 |
| F | 4 |
| J | 1 |
| M | 12 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Overview:'; skipped 16 forward-looking-statement block(s); 6 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (xpelq22026earnings.htm)

Second Quarter 2026 Overview:

• Revenue increased 14.7% to $143.1 million in the second quarter of 2026 compared to $124.7 million in the second quarter of 2025.

• Gross margin of 44.1% in the second quarter of 2026 compared to 42.9% in the second quarter last year.

• Net income attributable to stockholders of the company increased 10.7% to $18.0 million, or $0.65 per basic and diluted share, versus net income attributable to stockholders of the Company of $16.3 million, or $0.59 per basic and diluted share in the second quarter of 2025.

• Adjusted net income attributable to stockholders increased 15.6% to $18.8 million. Adjusted earnings per share was $0.68 per basic and diluted share. Adjusted net income attributable to stockholders and adjusted earnings per share exclude costs related to the start-up and ramp-up of the Company's San Antonio and China manufacturing investments incurred prior to reaching full operational capacity. 2

• EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) increased 17.6% to $27.6 million, or 19.3% of revenue, compared to $23.4 million, or 18.8% of revenue in the second quarter of 2025. 2

• Adjusted EBITDA grew 20.7% to $28.3 million or 19.8% of revenue. Adjusted EBITDA excludes costs related to the start-up and ramp-up of the Company's San Antonio and China manufacturing investments incurred prior to reaching full operational capacity. 2

First Six Months 2026 Overview:

• Revenue increased 14.0% to $260.4 million in the first six months of 2026 compared to $228.5 million in the same period in 2025.

• Gross margin of 43.9% in the first six months of 2026 compared to 42.6% in the first six months last year.

• Net income attributable to stockholders of the company increased 14.1% to $28.4 million, or $1.03 per basic and diluted share, versus net income attributable to stockholders of the Company of $24.9 million, or $0.90 per basic and diluted share in the first six months of 2025.

• EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) increased 17.7% to $44.5 million, or 17.1% of revenue, compared to $37.8 million, or 16.6% of revenue in the first six months of 2025. 2

Ryan Pape, President and Chief Executive Officer of XPEL, commented, "We saw solid top and bottom line performance in the second quarter and finished the first half of the year with nice momentum. We also were able to accomplish the first key objectives of our manufacturing expansion. We look forward to continuing to execute our strategy as we progress through the remainder of the year. "

Financial Highlights for the Second Quarter 2026:

Summary consolidated financial information for the second quarter ended June 30, 2026 and 2025 (unaudited, dollars in thousands):

Three Months Ended June 30, | % Change
2026 | % of Total Revenue | 2025 | % of Total Revenue | 2026 vs. 2025
Total revenue | 143,053 | 100.0 | % | 124,713 | 100.0 | % | 14.7 | %
Gross margin | 63,140 | 44.1 | % | 53,517 | 42.9 | % | 18.0 | %
Operating Expenses | 39,925 | 27.9 | % | 34,219 | 27.4 | % | 16.7 | %
Net income attributable to stockholders of the Company | 18,039 | 12.6 | % | 16,290 | 13.1 | % | 10.7 | %
EBITDA 2 | 27,559 | 19.3 | % | 23,432 | 18.8 | % | 17.6 | %
Net cash provided by operating activities | 30,789 | 21.5 | % | 27,888 | 22.4 | % | 10.4 | %

Geographical Revenue Summary

Three Months Ended June 30, | % Change | % of Total Revenue
2026 | 2025 | Inc (Dec) | 2026 | 2025
United States | 78,586 | 70,380 | 11.7 | % | 54.9 | % | 56.4 | %
Canada | 15,795 | 14,254 | 10.8 | % | 11.0 | % | 11.5 | %
North America | 94,381 | 84,634 | 11.5 | % | 65.9 | % | 67.9 | %
China | 15,924 | 7,705 | 106.7 | % | 11.1 | % | 6.2 | %
Asia Other | 6,178 | 5,428 | 13.8 | % | 4.3 | % | 4.3 | %
Asia Pacific | 22,102 | 13,133 | 68.3 | % | 15.4 | % | 10.5 | %
EU, UK, and Africa | 16,961 | 17,360 | (2.3) | % | 11.9 | % | 13.9 | %
India and Middle East | 6,410 | 6,746 | (5.0) | % | 4.5 | % | 5.4 | %
Latin America | 3,199 | 2,840 | 12.6 | % | 2.3 | % | 2.3 | %
Total | 143,053 | 124,713 | 14.7 | % | 100.0 | % | 100.0 | %

Overall Revenue

• Total revenue grew 14.7% compared to second quarter 2025 ("YoY").

• US revenue increased 11.7%YoY.

Product and Service Revenue

• Adjusted product revenue (combining cutbank credits revenue and product revenue) increased 14.4% YoY.

• Total window film revenue increased 16.1% YoY and represented 22.7% of total revenue.

• Normalized total service revenue increased 16.0% YoY.

• Total installation revenue (labor and product combined) grew 10.8% YoY.

Other Financial Information

• Gross margin was 44.1% and 42.9% in the second quarter of 2026 and 2025, respectively.

• Total operating expenses increased 16.7% YoY.

• Sales and marketing expenses increased 29.7% YoY and represented 10.8% of revenue.

• General and administrative expenses increased 9.8% YoY and represented 17.2% of revenue.

• Other Short Term Liabilities increased primarily due to the remaining purchase price payable pursuant to the acquisition of a manufacturing facility in China.

Cash Flows from Operations

• Cash flows provided by operations were $30.8 million in the second quarter 2026 compared to $27.9 million in the second quarter of 2025.

•

Cash Flows Used in Investing Activities

• Cash flows used in investing activities were $72.9 million in the second quarter 2026 compared to $1.3 million in the second quarter 2025. This increase was primarily due to our manufacturing investments in San Antonio and China.

2026 Third Quarter Outlook

• The Company expects third quarter 2026 revenue of approximately $137 - $139 million.

XPEL is a leading provider of protective films and coatings, including automotive paint protection film, surface protection film, automotive and architectural window films, and ceramic coatings. With a global footprint, a network of trained installers and proprietary DAP software, XPEL is dedicated to exceeding customer expectations by providing high-quality products, leading customer service, expert technical support and world-class training. XPEL, Inc. is publicly traded on Nasdaq under the symbol "XPEL".

1 The results summarized above for 2026 are preliminary and unaudited. As the Company completes its quarter-end financial close processes and finalizes its financial statements for the second quarter of 2026, it is possible that the Company may identify items that require it to make adjustments to the preliminary information set forth above, and those adjustments could be material. Full second quarter 2026 financial information will be included in the filing of the Company's Quarterly Report on Form 10-Q with the Securities and Exchange Commission which is anticipated on or prior to August 7, 2026.

2 See "Non-GAAP Financial Measure" and "Reconciliation of Non-GAAP Financial Measure" below.

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue
Product revenue | 111,674 | 94,795 | 200,388 | 173,507
Service revenue | 31,379 | 29,918 | 60,019 | 55,011
Total revenue | 143,053 | 124,713 | 260,407 | 228,518
Cost of Sales
Cost of product sales | 65,462 | 58,190 | 117,828 | 106,630
Cost of service | 14,451 | 13,006 | 28,209 | 24,475
Total cost of sales | 79,913 | 71,196 | 146,037 | 131,105
Gross Margin | 63,140 | 53,517 | 114,370 | 97,413
Operating Expenses
Sales and marketing | 15,386 | 11,862 | 30,549 | 23,737
General and administrative | 24,539 | 22,357 | 47,595 | 43,258
Total operating expenses | 39,925 | 34,219 | 78,144 | 66,995
Operating Income | 23,215 | 19,298 | 36,226 | 30,418
Interest expense | 262 | 7 | 266 | 83
Foreign currency exchange gain | (403) | (1,039) | (683) | (1,275)
Income before income taxes | 23,356 | 20,330 | 36,643 | 31,610
Income tax expense | 5,053 | 4,122 | 7,836 | 6,816
Net Income | 18,303 | 16,208 | 28,807 | 24,794
Net income attributed to non-controlling interest | 264 | (82) | 423 | (82)
Net income attributable to stockholders of the Company | 18,039 | 16,290 | 28,384 | 24,876
Earnings per share attributable to stockholders of the Company
Basic | 0.65 | 0.59 | 1.03 | 0.90
Diluted | 0.65 | 0.59 | 1.03 | 0.90
Weighted Average Number of Common Shares
Basic | 27,562 | 27,666 | 27,576 | 27,660
Diluted | 27,643 | 27,673 | 27,654 | 27,675

XPEL, Inc.

Consolidated Balance Sheets

(In thousands except share and per share data)

(Unaudited) | (Audited)
June 30, 2026 | December 31, 2025
Assets
Current
Cash and cash equivalents | 40,675 | 50,864
Accounts receivable, net | 53,613 | 49,846
Inventory | 128,011 | 122,755
Prepaid expenses and other current assets | 4,601 | 6,651
Income tax receivable | — | 581
Total current assets | 226,900 | 230,697
Property and equipment, net | 104,460 | 15,797
Right-of-use lease assets | 17,422 | 21,561
Intangible assets, net | 53,702 | 49,620
Deferred tax asset, net | 1,776 | —
Other non-current assets | 7,072 | 5,574
Goodwill | 61,316 | 59,277
Total assets | 472,648 | 382,526
Liabilities
Current
Short-term debt | 1,344 | 59
Current portion of lease liabilities | 5,373 | 6,094
Accounts payable and accrued liabilities | 57,157 | 54,289
Income tax payable | 2,233 | —
Other short-term liabilities | 20,828 | 10,558
Total current liabilities | 86,935 | 71,000
Deferred tax liability, net | — | 120
Other long-term liabilities | 10,324 | 9,511
Non-current portion of lease liabilities | 13,377 | 16,710
Long-term debt | 43,456 | —
Total liabilities | 154,092 | 97,341
Stockholders' equity
Preferred stock, $0.001 par value; authorized 10,000,000; none issued and outstanding | — | —
Capital stock, $0.001 par value; 100,000,000 shares authorized; 27,717,393 and 27,682,807, issued, respectively | 28 | 28
Additional paid-in-capital | 19,822 | 18,049
Accumulated other comprehensive loss | (1,510) | (135)
Retained earnings | 293,723 | 265,339
Treasury stock, 147,645 and 78,624 shares at cost, respectively | (5,938) | (2,999)
Stockholders' equity | 306,125 | 280,282
Non-controlling interest | 12,431 | 4,903
Total stockholders' equity | 318,556 | 285,185
Total liabilities and stockholders' equity | 472,648 | 382,526

XPEL, Inc.

Consolidated Statements of Cash Flows (Unaudited)

(In thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-27_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Executive Summary

Set forth below is summary financial information for the years ended December 31, 2025, 2024, and 2023. This information is not necessarily indicative of results of future operations, and should be read in conjunction with Part I, Item 1A, "Risk Factors," Part II, Item 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations" and the consolidated financial statements and accompanying notes thereto included in Part II, Item 8, "Financial Statements and Supplementary Data" of this Annual Report to fully understand factors that may affect the comparability of the information presented below (dollars in thousands).

Year Ended December 31, | % Change
2025 | % of Total Revenue | 2024 | % of Total Revenue | 2023 | % of Total Revenue | 2025 vs. 2024 | 2024 vs. 2023
Total Revenue | 476,200 | 100.0 | % | 420,400 | 100.0 | % | 396,293 | 100.0 | % | 13.3 | % | 6.1 | %
Total Cost of Sales | 275,181 | 57.8 | % | 243,040 | 57.8 | % | 233,879 | 59.0 | % | 13.2 | % | 3.9 | %
Gross Margin | 201,019 | 42.2 | % | 177,360 | 42.2 | % | 162,414 | 41.0 | % | 13.3 | % | 9.2 | %
Total Operating Expenses | 138,370 | 29.1 | % | 118,213 | 28.1 | % | 95,442 | 24.1 | % | 17.1 | % | 23.9 | %
Operating Income | 62,649 | 13.2 | % | 59,147 | 14.1 | % | 66,972 | 16.9 | % | 5.9 | % | (11.7) | %
Other (Income) Expense | (1,412) | (0.3) | % | 2,369 | 0.6 | % | 941 | 0.2 | % | (159.6) | % | 151.8 | %
Income Tax | 12,472 | 2.6 | % | 11,289 | 2.7 | % | 13,231 | 3.3 | % | 10.5 | % | (14.7) | %
Net Income | 51,589 | 10.8 | % | 45,489 | 10.8 | % | 52,800 | 13.3 | % | 13.4 | % | (13.8) | %

Company Overview

We are a supplier of protective films, coatings and related services primarily to the automobile aftermarket, new car dealerships and OEMs. The majority of our revenue is derived from the sale of our automotive products and related services while the remainder of our revenue is derived from non-automotive products including architectural window film and marine and flat surface protection films.

Key Business Metric - Non-GAAP Financial Measures

Our management regularly monitors certain financial measures to track the progress of our business against internal goals and targets. We believe that the most important measure to the Company is Earnings Before Interest, Taxes, Depreciation, and Amortization ("EBITDA").

EBITDA is a non-GAAP financial measure. We believe EBITDA provides helpful information with respect to our operating performance as viewed by management, including a view of our business that is not dependent on (i) the impact of our capitalization structure and (ii) items that are not part of our day-to-day operations. Management uses EBITDA (1) to compare our operating performance on a consistent basis, (2) to calculate incentive compensation for our employees, (3) for planning purposes including the preparation of our internal annual operating budget, (4) to evaluate the performance and effectiveness of

our operational strategies, and (5) to assess compliance with various metrics associated with the agreements governing our indebtedness. Accordingly, we believe that EBITDA provides useful information in understanding and evaluating our operating performance in the same manner as management. We define EBITDA as net income plus (a) total depreciation and amortization, (b) interest expense, net, and (c) income tax expense.

The following table is a reconciliation of Net Income to EBITDA for the years ended December 31, 2025, 2024, and 2023 (dollars in thousands):

2025 | % of Total Revenue | 2024 | % of Total Revenue | 2023 | % of Total Revenue
Net Income | 51,589 | 10.8 | % | 45,489 | 10.8 | % | 52,800 | 13.3 | %
Interest | 83 | — | % | 996 | 0.2 | % | 1,248 | 0.3 | %
Taxes | 12,472 | 2.6 | % | 11,289 | 2.7 | % | 13,231 | 3.3 | %
Depreciation | 6,264 | 1.3 | % | 5,820 | 1.4 | % | 4,534 | 1.1 | %
Amortization | 6,990 | 1.5 | % | 5,877 | 1.4 | % | 5,059 | 1.3 | %
EBITDA | 77,398 | 16.3 | % | 69,471 | 16.5 | % | 76,872 | 19.4 | %

Use of Non-GAAP Financial Measures

EBITDA should be considered in addition to, not as a substitute for, or superior to, financial measures calculated in accordance with GAAP. It is not a measurement of our financial performance under GAAP and should not be considered as alternatives to revenue or net income, as applicable, or any other performance measures derived in accordance with GAAP and may not be comparable to other similarly titled measures of other businesses. EBITDA has limitations as an analytical tool, and you should not consider it in isolation or as a substitute for analysis of our operating results as reported under GAAP.

EBITDA does not reflect the impact of certain cash charges resulting from matters we consider not to be indicative of ongoing operations; and other companies in our industry may calculate EBITDA differently than we do, limiting its usefulness as a comparative measure.

Results of Operations

This section of this Annual Report on Form 10-K generally discusses the years ended December 31, 2025 and 2024 and year-over-year comparisons between those years. Discussions of the periods prior to the year ended December 31, 2024 that are not included in this Annual Report on Form 10-K are found in "Management's Discussion and Analysis of Financial Condition and Results of Operations" in Part II, Item 7 of our Annual Report on Form 10-K for the year ended December 31, 2024 and the discussion therein for the year ended December 31, 2024 compared to the year ended December 31, 2023 is incorporated by reference into this Annual Report.

The following tables summarize revenue results for the years ended December 31, 2025, 2024 and 2023 (dollars in thousands):

Year Ended December 31, | % Change | % of Total Revenue
2025 | 2024 | 2023 | 2025 vs 2024 | 2024 vs 2023 | 2025 | 2024 | 2023
Product Revenue
Paint protection film | 249,401 | 226,710 | 229,880 | 10.0 | % | (1.4) | % | 52.4 | % | 53.9 | % | 58.0 | %
Window film | 94,544 | 77,666 | 67,951 | 21.7 | % | 14.3 | % | 19.9 | % | 18.5 | % | 17.1 | %
Other | 15,910 | 14,473 | 13,575 | 9.9 | % | 6.6 | % | 3.3 | % | 3.4 | % | 3.5 | %
Total | 359,855 | 318,849 | 311,406 | 12.9 | % | 2.4 | % | 75.6 | % | 75.8 | % | 78.6 | %
Service Revenue
Software | 8,729 | 8,061 | 6,518 | 8.3 | % | 23.7 | % | 1.8 | % | 1.9 | % | 1.6 | %
Cutbank credits | 16,530 | 17,015 | 17,626 | (2.9) | % | (3.5) | % | 3.5 | % | 4.0 | % | 4.4 | %
Installation labor | 87,049 | 74,478 | 58,477 | 16.9 | % | 27.4 | % | 18.3 | % | 17.7 | % | 14.8 | %
Other | 4,037 | 1,997 | 2,266 | 102.2 | % | (11.9) | % | 0.8 | % | 0.6 | % | 0.6 | %
Total | 116,345 | 101,551 | 84,887 | 14.6 | % | 19.6 | % | 24.4 | % | 24.2 | % | 21.4 | %
Total | 476,200 | 420,400 | 396,293 | 13.3 | % | 6.1 | % | 100.0 | % | 100.0 | % | 100.0 | %

Because many of our international customers require us to ship their orders to freight forwarders located in the United States, we cannot be certain about the ultimate destination of the product. The following table represents our estimate of sales by geographic regions based on our understanding of ultimate product destination based on customer interactions, customer locations and other factors for the years ended December 31, 2025 and 2024 (dollars in thousands):

Year Ended December 31, | % | % of Total Revenue
2025 | 2024 | 2025 vs 2024 | 2025 | 2024
United States | 265,756 | 240,569 | 10.5 | % | 55.8 | % | 57.2 | %
Canada | 49,545 | 52,139 | (5.0) | % | 10.4 | % | 12.4 | %
North America | 315,301 | 292,708 | 7.7 | % | 66.2 | % | 69.6 | %
China | 39,921 | 24,148 | 65.3 | % | 8.4 | % | 5.7 | %
Asia Other | 20,895 | 16,825 | 24.2 | % | 4.4 | % | 4.0 | %
Asia Pacific | 60,816 | 40,973 | 48.4 | % | 12.8 | % | 9.7 | %
EU, UK, and Africa | 64,095 | 53,983 | 18.7 | % | 13.5 | % | 12.9 | %
India and Middle East | 24,984 | 21,072 | 18.6 | % | 5.2 | % | 5.0 | %
Latin America | 11,004 | 11,664 | (5.7) | % | 2.3 | % | 2.8 | %
Total | 476,200 | 420,400 | 13.3 | % | 100.0 | % | 100.0 | %

Revenue

Product Revenue. Product revenue increased 12.9% during the year ended December 31, 2025 as compared to 2024 and represented 75.6% of our consolidated 2025 revenue. Within this category, revenue from our paint protection film product line increased 10.0% as compared to the prior year and represented 52.4% of total consolidated revenue for the year ended December 31, 2025. The total increase in paint protection film sales was due to increased demand for our film products across multiple regions.

Revenue from our window film product line grew 21.7% during the year ended December 31, 2025 and represented 19.9% of our consolidated annual 2025 revenue. This increase was driven by continued demand resulting from increased product adoption in multiple regions for automotive window film. Our windshield protection film revenue for the year ended December 31, 2025 was $7.0 million and represented 7.4% of total window film revenue and 1.5% of total consolidated revenue. Our windshield protection film product was launched during the fourth quarter 2024.

Other product revenue for the year ended December 31, 2025 grew 9.9% to $15.9 million and represented 3.3% of total consolidated revenue. This increase was driven by an increase in demand for our non-film related products such as ceramic coating, plotters, chemicals and other film installation tools and accessories.

Geographically, we experienced continued growth in most of our regions during the year ended December 31, 2025 including growth of 65.3%, 24.2%, and 18.7% in China, Asia-Other, and EU/UK/Africa respectively. Additionally, we saw 10.5% growth in the US region, our largest market. The increase in China was driven primarily by increased demand and incremental direct revenue resulting from the completion of the acquisition of our China distributor late in the third quarter 2025. Other increases were primarily due to increasing product awareness and adoption.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-27_item1_business.md)

Item 1. Business

Company Overview

We are a supplier of protective films, coatings and related services primarily to the automobile aftermarket, new car dealerships and automobile original equipment manufacturers, or OEMs. The majority of our revenue is derived from the sale of our automotive products and related services while the remainder of our revenue is derived from non-automotive products including architectural window film and marine and flat surface protection films.

The Company began as a software company designing vehicle patterns used to produce cut-to-fit protective film for headlights and painted surfaces of automobiles. In 2007, we began selling automotive paint protection film products to complement our software business. As paint protection film technology improved and became more durable, awareness and adoption of paint protection film continued to increase, driving significant industry growth over the last several years. Initial adoption of paint protection film came primarily from luxury car enthusiasts in the United States and Canada. These enthusiasts were primarily served by a growing automotive aftermarket of independent installers of automotive paint protection and window films. Internationally, nascent demand began to build as awareness and adoption in the United States and Canada continued to increase. Over the last few years, new car dealership interest in the product increased due to their exposure to the aftermarket installer network, while OEM interest in the product increased through their exposure to the new car dealerships who were selling the product.

Our strategy initially centered on how best to serve and grow our network of independent installers in the US and Canada and to sell products internationally through independent distributors while simultaneously building and enhancing the XPEL brand. This "best-in-class" service strategy was then extended to new car dealerships and OEMs. Internationally, while our initial market entry has primarily been through indirect distribution, we desire to ultimately sell directly to the majority of the top 25 car markets in the world, which is an important element of our acquisition strategy. To that end, we have acquired distributors in several international markets including India, Thailand, Japan and, most recently, China.

Surface and Paint Protection Film: Our primary products are paint and surface protection films. Most of the products sold are for automotive applications. Paint protection film, our flagship product, is a self-adhesive film designed to be applied to painted surfaces of automobiles and other surfaces. We offer both clear and colored paint protection film as well as a variety of product lines each with their own unique characteristics, warranties and intended uses. Surface and paint protection film sales represented approximately 52.4% of our consolidated revenue for the year ended December 31, 2025.

Automotive Window Film (or Tint): We sell several lines of automotive window or tint films, primarily under the XPEL PRIME brand name, which exhibit a range of performance characteristics and appearances. Automotive window film sales represented approximately 16.6% of our consolidated revenue for the year ended December 31, 2025.

Windshield Protection Film: We sell windshield protection film which, unlike automotive window tint, is applied to the outside of a windshield, helping to make the windshield more impact-resistant and prevent costly repairs.

Architectural Window Film: We sell architectural glass solutions for commercial and residential buildings under the VISION brand name, representing our first product set with a fully non-automotive use. Architectural window films come in several broad categories, including:

Solar: Solar films are designed to provide solar energy rejection. We offer a variety of films with varying colors, visual light transmissions and price points.

Safety & Security: Safety and Security films are clear, thick polyethylene terephthalate, or PET, films to secure glass in the event of a breakage. We offer a variety of thicknesses and offer films with varying adhesive characteristics for different types of installations.

Other: In addition to the main categories of Solar and Safety & Security films, we also offer anti-graffiti, exterior applied and decorative films.

Ceramic coating: We sell a hydrophobic, self-cleaning coating that can be applied to a variety of surface types for automobiles, aircraft and marine applications.

Miscellaneous Products, Tools and Pre-Cut Films: We sell a variety of other miscellaneous product sets including pre-cut film products, tools and accessories and merchandise and apparel.

Services

Installation Services: We offer installation services for the installation of all of our products through our various sales channels. We have over 640 installation technicians who are highly trained to install our products effectively and efficiently. Installation labor revenue represented approximately 18.3% of our consolidated revenue for the year ended December 31, 2025.

Software: A key component of our product offering is our Design Access Platform ("DAP"). DAP is a proprietary SAAS platform and database consisting of over 90,000 vehicle applications used by the Company and its customers to cut automotive protection film into vehicle panel shapes for both paint protection film and window film products.

We commit significant resources to keep the pattern database updated with a goal toward having a pattern for every panel of every vehicle. When new vehicle models are introduced to the market, we strive to create the pattern as soon as practicable. Our patterns and software increase installer efficiency and reduce waste.

Our DAP customers pay a monthly access fee to access our proprietary database.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-27_item7_mdna.md, 10-K_2026-02-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
