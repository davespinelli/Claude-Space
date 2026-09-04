# Triage pack — MCFT · MasterCraft Boat Holdings, Inc.

_Generated 2026-09-04 18:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MCFT · **Name:** MasterCraft Boat Holdings, Inc.
- **CIK:** 0001638290
- **SIC:** 3730 — Ship & Boat Building & Repairing
- **Fiscal year end (MM-DD):** 06-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MCFT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** MasterCraft Boat Holdings, Inc.
- **CIK:** 1,638,290 · **SIC:** 3730 (Ship & Boat Building & Repairing) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 23.33 |
| mktcap | $379.8M |
| ev | $304.4M |
| ev_ebit | 27.1x |
| fcf | $26.4M |
| fcf_yield | 6.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.8% |
| net_debt | -$75.4M |
| net_debt_ebit | -6.7x |
| cash | $75.4M |
| ltd | $0.00 |
| equity | $189.1M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $284.2M |
| revenue_prior | $322.4M |
| rev_growth | -11.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $11.2M |
| net_income | $7.0M |
| cfo | $35.6M |
| capex | $9.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 16,279,890 |
| shares_py | 16,605,130 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 13.1% |
| r6m | 13.8% |
| off_52w_high | -14.8% |
| adv20 | $4.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.58 |
| r_ev_ebit | 0.33 |
| r_roic | 0.63 |
| r_rev_growth | 0.08 |
| r_buyback | 0.79 |
| score | 0.53 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q1I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 215 |

**Screen rationale:** buying back stock -2.0%; debt data missing (net cash unverified); 12-1 momentum 13.1%


## 3. Share count trend

- Shares outstanding: **16,279,890** (CY2026Q1I) vs **16,605,130** prior year (CY2025Q1I)
- Change: **-2.0%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-15** — Item 5.02 (officer / director change or comp arrangement): In accordance with the Merger Agreement and following the First Effective Time, MasterCraft's board of directors (the "MasterCraft Board") was increased from a total of seven directors to a total of ten directors, including two former members of the Marine...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 29 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 1 |
| F | 6 |
| M | 22 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-07_2-02-results.md)

_Extraction: started at the first release heading, 'MasterCraft Boat Holdings, Inc. Reports Fiscal 2026 Third Quarter Resu'; skipped 7 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (mcft-ex99_1.htm)

MasterCraft Boat Holdings, Inc. Reports Fiscal 2026 Third Quarter Results

VONORE, Tenn. – May 7, 2026 – MasterCraft Boat Holdings, Inc. (NASDAQ: MCFT) today announced financial results for its fiscal 2026 third quarter ended March 29, 2026.

The overview, commentary, and results provided herein relate to our continuing operations, which consists of our MasterCraft and Pontoon segments.

Overview:

▪
Continued expectation to complete the combination with Marine Products Corporation ("Marine Products") shortly after our special meeting of shareholders scheduled on May 12, 2026, subject to customary closing conditions

▪
Net sales for the third quarter were $78.2 million, up $2.2 million, or 3.0%, from the comparable prior-year period

▪
Dealer pipeline discipline remains strong, with stabilized dealer pipelines, supported by aligned production plans and a flexible, demand‑driven wholesale approach

▪
Loss from continuing operations in the third quarter was ($0.7) million, or ($0.04) per diluted share, down from prior-year income of $3.8 million, or $0.23 per diluted share, primarily due to one-time transaction costs related to the pending Marine Products combination

▪
Adjusted Net Income, a non-GAAP measure, was $7.2 million, or $0.45 per diluted share, up from $5.0 million, or $0.30 per diluted share, in the prior-year period

▪
Adjusted EBITDA, a non-GAAP measure, was $10.7 million, up $3.2 million from the comparable prior-year period

▪
Ended the third quarter with cash and investments of $84.6 million

Brad Nelson, Chief Executive Officer, commented, "We delivered results that outperformed our expectations during the third quarter, driven by disciplined execution across our business and continued new product momentum. In a market that's evolving week to week, we've remained focused on our core strengths—delivering operational efficiencies, aligning production with demand, and differentiated innovation that resonates with customers and dealers."

Nelson continued, "Within MasterCraft, premium product momentum continues to build across the lineup. Last month, we announced the reintroduction of the X23, marking the return of a historic name in our portfolio and completing the next‑generation X‑series."

Third Quarter Results

For the third quarter of fiscal 2026, MasterCraft Boat Holdings, Inc. reported consolidated net sales of $78.2 million, up $2.2 million from the third quarter of fiscal 2025. The increase in net sales was primarily due to favorable model mix and options sales, increased prices, and decreased dealer incentives, partially offset by lower unit volumes.

Gross margin percentage increased 420 basis points during the third quarter of fiscal 2026, compared to the prior-year period. Higher margins were primarily the result of increased net sales, as discussed above, combined with effective cost controls.

Operating expenses increased $9.2 million for the third quarter of fiscal 2026, compared to the prior-year period, due to business development and consulting costs related to the combination with Marine Products, increased selling and marketing costs, and consulting costs related to the implementation of our enterprise resource planning system ("ERP implementation costs").

Loss from continuing operations was ($0.7) million for the third quarter of fiscal 2026, compared to income from continuing operations of $3.8 million in the prior-year period. Diluted loss from continuing operations per share was ($0.04), compared to diluted income from continuing operations per share of $0.23 for the third quarter of fiscal 2025.

Adjusted Net income was $7.2 million for the third quarter of fiscal 2026, or $0.45 per diluted share, compared to $5.0 million, or $0.30 per diluted share, in the prior-year period.

Adjusted EBITDA was $10.7 million for the third quarter of fiscal 2026, compared to $7.5 million in the prior-year period. Adjusted EBITDA margin was 13.7% for the third quarter, up from 9.9% for the prior-year period.

See "Non-GAAP Measures" below for a reconciliation of Adjusted EBITDA, Adjusted EBITDA margin, Adjusted Net Income, Adjusted Net Income per share, and Free Cash Flow, which we refer to collectively as the "Non-GAAP Measures", to the most directly comparable financial measures presented in accordance with GAAP.

Combination with Marine Products Corporation

On February 5, 2026, we announced that we have entered into a definitive agreement under which we will merge with Marine Products, a leading manufacturer of recreation and sport fishing powerboats, in a cash and stock transaction. Our special meeting of shareholders is scheduled for May 12, 2026, and we expect to close shortly thereafter, subject to customary closing conditions.

Outlook

Concluded Nelson, "Looking ahead, we remain confident and credible in our ability to navigate the current macroeconomic environment by remaining disciplined, agile, and focusing on our strengths. With a strong balance sheet, a variable operating model, and a premium product portfolio that continues to resonate, we believe we're well positioned as we move through the remainder of fiscal 2026 and into the next cycle."

The Company's outlook is as follows:

•
For full year fiscal 2026, we now expect consolidated net sales to be $312 million, with Adjusted EBITDA of $40 million, and Adjusted Earnings per share of $1.65. We now expect capital expenditures to be approximately $8 million for the year.

The outlook provided does not include the pending combination with Marine Products.

Conference Call and Webcast Information

MasterCraft Boat Holdings, Inc. will host a live conference call and webcast to discuss fiscal third quarter 2026 results today, May 7, 2026, at 8:30 a.m. ET. Participants may access the conference call live via webcast on the investor section of the Company's website, Investors.MasterCraft.com , by clicking on the webcast icon. To participate via telephone, please register in advance at this link . Upon registration, all telephone participants will receive a confirmation email detailing how to join the conference call, including the dial-in number along with a unique passcode and registrant ID that can be used to access the call. A replay of the conference call and webcast will be archived on the Company's website.

About MasterCraft Boat Holdings, Inc.

Headquartered in Vonore, Tenn., MasterCraft Boat Holdings, Inc. (NASDAQ: MCFT) is a leading innovator, designer, manufacturer and marketer of recreational powerboats through its three brands, MasterCraft, Crest, and Balise. For more information about MasterCraft Boat Holdings, and its three brands, visit: Investors.MasterCraft.com, www.MasterCraft.com, www.CrestPontoonBoats.com, and www.BalisePontoonBoats.com.

Results of Operations for the Three and Nine Months Ended March 29, 2026

MASTERCRAFT BOAT HOLDINGS, INC. AND SUBSIDIARIES

CONSOLIDATED STATEMENTS OF OPERATIONS

(Dollars in thousands, except per share data)

Three Months Ended | Nine Months Ended
March 29, | March 30, | March 29, | March 30,
2026 | 2025 | 2026 | 2025
Net sales | 78,206 | 75,960 | 218,967 | 204,687
Cost of sales | 58,664 | 60,195 | 168,502 | 166,232
Gross profit | 19,542 | 15,765 | 50,465 | 38,455
Operating expenses:
Selling and marketing | 3,360 | 2,845 | 9,649 | 8,543
General and administrative | 17,030 | 8,356 | 34,267 | 23,258
Amortization of other intangible assets | 450 | 450 | 1,350 | 1,350
Total operating expenses | 20,840 | 11,651 | 45,266 | 33,151
Operating income (loss) | (1,298 | 4,114 | 5,199 | 5,304
Other income (expense):
Interest expense | (58 | — | (146 | (1,169
Interest income | 760 | 760 | 2,257 | 2,649
Loss on extinguishment of debt | (71 | — | (71 | —
Income (loss) before income tax expense | (667 | 4,874 | 7,239 | 6,784
Income tax expense | 49 | 1,053 | 1,811 | 1,521
Income (loss) from continuing operations | (716 | 3,821 | 5,428 | 5,263
Loss from discontinued operations, net of tax | (26 | (78 | (7 | (3,917
Net income (loss) | (742 | 3,743 | 5,421 | 1,346
Income (loss) per share
Basic
Continuing operations | (0.04 | 0.23 | 0.34 | 0.32
Discontinued operations | (0.01 | — | — | (0.24
Net income (loss) | (0.05 | 0.23 | 0.34 | 0.08
Diluted
Continuing operations | (0.04 | 0.23 | 0.33 | 0.32
Discontinued operations | (0.01 | — | — | (0.24
Net income (loss) | (0.05 | 0.23 | 0.33 | 0.08
Weighted average shares used for computation of:
Basic earnings per share | 16,136,132 | 16,414,340 | 16,147,425 | 16,471,352
Diluted earnings per share | 16,136,132 | 16,540,345 | 16,263,844 | 16,554,235

MASTERCRAFT BOAT HOLDINGS, INC. AND SUBSIDIARIES

CONSOLIDATED BALANCE SHEETS

(Dollars in thousands, except per share data)

March 29, | June 30,
2026 | 2025
ASSETS
CURRENT ASSETS:
Cash and cash equivalents | 75,403 | 28,926
Short-term investments | 9,220 | 50,518
Accounts receivable, net of allowances of $254 and $156, respectively | 11,230 | 4,086
Income tax receivable | 1,740 | 208
Inventories, net | 34,769 | 30,469
Prepaid expenses and other current assets | 9,484 | 7,006
Total current assets | 141,846 | 121,213
Property, plant and equipment, net | 53,517 | 53,576
Goodwill | 28,493 | 28,493
Other intangible assets, net | 30,500 | 31,850
Deferred income taxes | 17,569 | 18,914
Other long-term assets | 5,927 | 5,902
Total assets | 277,852 | 259,948
LIABILITIES AND EQUITY
CURRENT LIABILITIES:
Accounts payable | 21,895 | 8,255
Income tax payable | 1,773 | 1,773
Accrued expenses and other current liabilities | 53,884 | 55,182
Total current liabilities | 77,552 | 65,210
Unrecognized tax positions | 9,346 | 9,067
Other long-term liabilities | 1,702 | 2,085
Total liabilities | 88,600 | 76,362
COMMITMENTS AND CONTINGENCIES
EQUITY:
Common stock, $.01 par value per share — authorized, 100,000,000 shares; issued and outstanding, 16,279,890 shares at March 29, 2026 and 16,406,788 shares at June 30, 2025 | 163 | 164
Additional paid-in capital | 52,805 | 52,559
Retained earnings | 136,084 | 130,663
MasterCraft Boat Holdings, Inc. equity | 189,052 | 183,386
Noncontrolling interest | 200 | 200
Total equity | 189,252 | 183,586
Total liabilities and equity | 277,852 | 259,948

Supplemental Operating Data

The following table presents certain supplemental operating data for the periods indicated:

Three Months Ended | Nine Months Ended
March 29, | March 30, | March 29, | March 30,
2026 | 2025 | Change | 2026 | 2025 | Change
(Dollars in thousands)
Unit sales volume:
MasterCraft | 409 | 422 | (3.1 | % | 1,195 | 1,196 | (0.1 | %
Pontoon | 162 | 197 | (17.8 | % | 524 | 527 | (0.6 | %
Consolidated | 571 | 619 | (7.8 | % | 1,719 | 1,723 | (0.2 | %
Net sales:
MasterCraft | 66,764 | 64,227 | 4.0 | % | 186,647 | 174,857 | 6.7 | %
Pontoon | 11,442 | 11,733 | (2.5 | % | 32,320 | 29,830 | 8.3 | %
Consolidated | 78,206 | 75,960 | 3.0 | % | 218,967 | 204,687 | 7.0 | %
Net sales per unit:
MasterCraft | 163 | 152 | 7.2 | % | 156 | 146 | 6.8 | %
Pontoon | 71 | 60 | 18.3 | % | 62 | 57 | 8.8 | %
Consolidated | 137 | 123 | 11.4 | % | 127 | 119 | 6.7 | %
Gross margin | 25.0 | % | 20.8 | % | 420 bps | 23.0 | % | 18.8 | % | 420 bps

Non-GAAP Measures

EBITDA, Adjusted EBITDA, EBITDA margin, and Adjusted EBITDA margin

We define EBITDA as income (loss) from continuing operations, before interest, income taxes, depreciation and amortization. We define Adjusted EBITDA as EBITDA further adjusted to eliminate certain non-cash charges or other items that we do not consider to be indicative of our core and/or ongoing operations. For the periods presented herein, the adjustments include share-based compensation, senior leadership transition and organizational realignment costs, ERP implementation costs, and business development and consulting costs. We define EBITDA margin and Adjusted EBITDA margin as EBITDA and Adjusted EBITDA, respectively, each expressed as a percentage of Net sales.

Adjusted Net Income and Adjusted Net Income per share

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-08-27_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Discontinued Operations

On October 18, 2024, the Company completed the Aviara Transaction and on December 23, 2024, the Company completed the Aviara Facility Sale. In fiscal 2023, the Company sold its NauticStar business. The Company's results for all periods presented, as discussed in Management's Discussion and Analysis, are presented on a continuing operations basis. Results related to our Aviara and NauticStar reporting units are reported as discontinued operations for all periods presented. See Notes 1 and 3 in Notes to Consolidated Financial Statements for more information on discontinued operations.

Leadership Transition

On April 7, 2025 Timothy M. Oxley, Chief Financial Officer ("CFO") of the Company, announced his retirement from the Company, effective December 31, 2025. Prior to his retirement, Mr. Oxley stepped down as CFO, effective June 30, 2025, at which time, Mr. Oxley began serving as a Special Advisor. Scott Kent, Vice President of Finance, succeeded Mr. Oxley as CFO, effective July 1, 2025.

Tariff and Trade Environment

The recently imposed U.S. tariffs did not materially impact our fiscal 2025 results, but their effects and the potential imposition of modified or additional tariffs may, among other things, create new trade barriers that disrupt supply chains, raise costs, weaken consumer confidence and impact consumer demand for our products, and impact our ability to export our products, all of which could have an adverse effect on our business and financial results. The extent of the impact of tariffs on the Company's business is highly uncertain and difficult to predict. We are closely monitoring the rapidly evolving tariff landscape and are working diligently with key suppliers to mitigate risks. For additional information regarding the potential impacts of tariffs on our business and results of operations, see Item 1A "Risk Factors — Risks Relating to Our Regulatory, Accounting, Legal, and Tax Environment."

Results of Operations

Fiscal 2025 was impacted by anticipated market and economic uncertainty. Net sales decreased primarily due to planned lower unit volumes aimed at aligning dealer inventories with retail demand. Gross margin declined due to lower cost absorption driven by decreased production volume.

We derived the consolidated statements of operations for the fiscal years ended June 30, 2025 and 2024 from our audited consolidated financial statements and related notes included elsewhere in this Form 10-K. Our historical results are not necessarily indicative of the results that may be expected in the future.

Consolidated Results

2025 | 2024 | Change | % Change
(Dollar amounts in thousands)
Consolidated statements of operations :
NET SALES | 284,203 | 322,351 | (38,148 | (11.8 | %)
COST OF SALES | 227,338 | 250,741 | (23,403 | (9.3 | %)
GROSS PROFIT | 56,865 | 71,610 | (14,745 | (20.6 | %)
OPERATING EXPENSES:
Selling and marketing | 11,740 | 11,203 | 537 | 4.8 | %
General and administrative | 32,093 | 31,119 | 974 | 3.1 | %
Amortization of other intangible assets | 1,800 | 1,812 | (12 | (0.7 | %)
Total operating expenses | 45,633 | 44,134 | 1,499 | 3.4 | %
OPERATING INCOME | 11,232 | 27,476 | (16,244 | (59.1 | %)
OTHER INCOME (EXPENSE):
Interest expense | (1,169 | (3,292 | 2,123 | (64.5 | %)
Interest income | 3,472 | 5,789 | (2,317 | (40.0 | %)
INCOME BEFORE INCOME TAX EXPENSE | 13,535 | 29,973 | (16,438 | (54.8 | %)
INCOME TAX EXPENSE | 2,820 | 6,730 | (3,910 | (58.1 | %)
INCOME FROM CONTINUING OPERATIONS | 10,715 | 23,243 | (12,528 | (53.9 | %)
Additional financial and other data:
Unit sales volume:
MasterCraft | 1,548 | 1,755 | (207 | (11.8 | %)
Pontoon | 745 | 1,241 | (496 | (40.0 | %)
Consolidated unit sales volume | 2,293 | 2,996 | (703 | (23.5 | %)
Net sales:
MasterCraft | 240,763 | 262,736 | (21,973 | (8.4 | %)
Pontoon | 43,440 | 59,615 | (16,175 | (27.1 | %)
Consolidated net sales | 284,203 | 322,351 | (38,148 | (11.8 | %)
Net sales per unit:
MasterCraft | 156 | 150 | 6 | 4.0 | %
Pontoon | 58 | 48 | 10 | 20.8 | %
Consolidated net sales per unit | 124 | 108 | 16 | 14.8 | %
Gross margin | 20.0 | % | 22.2 | % | (220) bps

Net Sales. Net Sales decreased 11.8 percent for fiscal 2025 when compared to fiscal 2024. The decrease was a result of planned lower unit volumes and changes in price, partially offset by favorable model mix related to new product introductions, favorable option sales, and decreased dealer incentives.

Gross Margin. Gross Margin percentage declined 220 basis points during fiscal 2025 when compared to fiscal 2024. Lower margins were the result of lower cost absorption due to decreased production volume, material and overhead inflation, and changes in sales price.

Operating Expenses . Operating expenses increased 3.4 percent during fiscal 2025 when compared to the same prior year period mainly due to increased variable compensation costs.

Interest Expense. Interest expense decreased $2.1 million primarily due to all outstanding borrowings under the Credit Agreement being repaid during the first six months of fiscal 2025.

Interest Income. Interest income decreased $2.3 million during fiscal 2025 primarily due to certain investment securities being sold to repay outstanding borrowings under the Revolving Credit Facility during the second quarter of fiscal 2025.

Income Tax Expense. Our consolidated effective income tax rate decreased to 20.8 percent for fiscal 2025 from 22.5 percent for fiscal 2024. See Note 10 in Notes to Consolidated Financial Statements for more information.

Segment Results

MasterCraft Segment

The following table sets forth MasterCraft segment results for the fiscal years ended:

(Dollar amounts in thousands) | 2025 | 2024 | Change | % Change
Net sales | 240,763 | 262,736 | (21,973 | (8.4 | %)
Operating income | 20,658 | 29,573 | (8,915 | (30.1 | %)
Purchases of property, plant and equipment | 7,219 | 7,912 | (693 | (8.8 | %)
Unit sales volume | 1,548 | 1,755 | (207 | (11.8 | %)
Net sales per unit | 156 | 150 | 6 | 4.0 | %

Net sales decreased 8.4 percent during fiscal 2025, when compared to fiscal 2024. The decrease was primarily driven by lower unit volumes and changes in price, partially offset by favorable model mix, decreased dealer incentives, and favorable option sales.

Operating income decreased 30.1 percent during fiscal 2025, when compared to the same prior year period. The overall decrease was driven by decreased net sales, as discussed above, increased materials and overhead inflation, and increased variable compensation costs.

Pontoon Segment

The following table sets forth Pontoon segment results for the fiscal years ended:

(Dollar amounts in thousands) | 2025 | 2024 | Change | % Change
Net sales | 43,440 | 59,615 | (16,175 | (27.1 | %)
Operating loss | (9,426 | (2,097 | (7,329 | 349.5 | %
Purchases of property, plant and equipment | 1,979 | 2,613 | (634 | (24.3 | %)
Unit sales volume | 745 | 1,241 | (496 | (40.0 | %)
Net sales per unit | 58 | 48 | 10 | 20.8 | %

Net sales decreased 27.1 percent during fiscal 2025, when compared to fiscal 2024, as a result of decreased unit volume and increased dealer incentives, partially offset by favorable model mix and favorable option sales.

Operating loss was $9.4 million during fiscal 2025, compared to $2.1 million in fiscal 2024. The change was primarily due to decreased net sales, as discussed above, and increased labor and materials cost.

Non-GAAP Measures

EBITDA, Adjusted EBITDA, EBITDA Margin, and Adjusted EBITDA Margin

We define EBITDA as income from continuing operations, before interest, income taxes, depreciation and amortization. We define Adjusted EBITDA as EBITDA further adjusted to eliminate certain non-cash charges or other items that we do not consider to be indicative of our core and/or ongoing operations. For the periods presented herein, these adjustments include share-based compensation, senior leadership transition and organizational realignment costs, and business development consulting costs, as described in more detail below. We define EBITDA margin and Adjusted EBITDA margin as EBITDA and Adjusted EBITDA, respectively, expressed as a percentage of Net sales.

Adjusted Net Income and Adjusted Net Income Per Share

We define Adjusted Net Income and Adjusted Net Income per share as income from continuing operations adjusted to eliminate certain non-cash charges or other items that we do not consider to be indicative of our core and/or ongoing operations and reflecting income tax expense on adjusted net income before income taxes at our estimated annual effective tax rate. For the periods presented herein, these adjustments include other intangible asset amortization, share-based compensation, senior leadership transition and organizational realignment costs, and business development consulting costs.

Free Cash Flow

We define Free Cash Flow from continuing operations as net cash flows from operating activities less purchases of property, plant, and equipment.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-08-27_item1_business.md)

ITEM 1. B USINESS

We are a leading innovator, designer, manufacturer, and marketer of recreational powerboats sold through our three brands, MasterCraft, Crest, and Balise. As a leader in recreational marine, we strive to deliver the best on-water experience through innovative, high-quality products with a relentless focus on the consumer.

Our Segments

MasterCraft Segment

Our MasterCraft segment, which manufactures and sells premium ski/wake boats, consists of our MasterCraft brand. The MasterCraft brand was founded in 1968 and evolved over the next 55-plus years to become the most award-winning ski/wake boat manufacturer in the world. Today, MasterCraft participates in one of the highest margin producing category within the powerboat industry by manufacturing the industry's premier competitive water ski, wakeboarding, and wake surfing performance boats. We believe the MasterCraft brand is known among boating enthusiasts for high performance, premier quality, and relentless innovation. We believe that the market recognizes MasterCraft as a premier brand in the powerboat industry due to the overall superior value proposition that our boats deliver to consumers. We work tirelessly every day to maintain this iconic brand reputation.

Pontoon Segment

Our Pontoon segment, which manufactures and sells pontoon boats, consists of our Crest and our Balise brands. The Pontoon segment participates in the largest unit producing category in the powerboat industry. Crest, which we acquired in October 2018, was founded in 1957 and has grown to be one of the top producers of innovative, high-quality pontoon boats ranging from 20 to 27 feet. Crest's long-standing reputation for high-quality, standard features and content, and innovation provides Crest with strong dealer and consumer bases in its core geographic markets.

Our Balise brand, an all-new, independent pontoon brand which was launched in April 2024, has been conceived with the discerning consumer in mind. With luxurious accents and appointments not typically found in pontoons, we seek to manufacture our Balise boats to the highest quality standards and to position the brand as the most luxurious pontoon on the market.

Unless the context otherwise requires, "MasterCraft" and "Pontoon," as used herein, refer to our segments as described above.

Our Products

We design, manufacture, and sell premium recreational inboard ski/wake and outboard boats that we believe deliver superior performance for water skiing, wakeboarding, and wake surfing, as well as general recreational boating. In addition, we offer various accessories, including trailers and aftermarket parts.

Our MasterCraft portfolio of ProStar, XStar, X, XT, and NXT models are designed for the highest levels of performance, styling, and enjoyment for both recreational and competitive use. The ProStar, XStar and X models are geared towards the consumer seeking the most premium and highest performance boating experience that we offer, and generally command a price premium over our competitors' boats at retail prices ranging from approximately $120,000 to $500,000. The MasterCraft XT lineup is designed to offer ultimate flexibility to consumers with maximum customization and maximum performance at retail prices ranging from approximately $155,000 to $225,000. The NXT models offer the quality, performance, styling, and innovation of the MasterCraft brand to the entry-level consumer, with retail prices ranging from approximately $110,000 to $150,000.

Our Crest portfolio of pontoon boats are designed for the ultimate in comfort and recreational pleasure boating. Crest's pontoon boats are designed to offer consumers the best in luxury, style and performance without compromise across a diverse model lineup ranging in length from 20 to 27 feet. The Signature Line is home to Crest's Classic models. The Premium Line boasts the Caribbean and Upper Sun Deck models with sleek lines, available tower options, unique color combinations and top-quality construction. The Ultimate Luxury Line represents the pinnacle of lavish amenities, featuring the Continental, Continental NX, and Savannah models. This lineup anticipates every need with thoughtful options, an industry-first integrated dual windshield and premium upholstery and audio upgrades. The Electric Line harmonizes industry innovations by introducing eco-friendly pontoon boats. The Current model allows consumers to

enjoy a level of peace and relaxation with less noise and minimal emissions. Crest's retail prices range from approximately $40,000 to $300,000.

We believe our Balise portfolio of models are the most refined pontoon boats in the luxury watercraft space. With sizes ranging from 24 to 26 feet and two unique seating configurations, the Balise line is the perfect boat for the discerning consumer. Our two models, Horizon and Helix, bring unrivaled luxury to the pontoon segment. Balise retail prices range from $230,000 to $350,000.

Our products are sold through extensive networks of independent dealers domestically and internationally. We target our distribution to the market category's highest performing dealers. The majority of our MasterCraft brand dealers are exclusive to our MasterCraft product lines within the ski/wake category, highlighting the commitment of our key dealers to the MasterCraft brand. Our other brands are generally served on a nonexclusive basis by their respective dealers.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-08-27_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-08-27_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-08-27_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-07_2-02-results.md, 10-K_2025-08-27_item7_mdna.md, 10-K_2025-08-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
