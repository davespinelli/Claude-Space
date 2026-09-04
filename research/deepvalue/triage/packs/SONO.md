# Triage pack — SONO · Sonos Inc

_Generated 2026-09-04 23:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SONO · **Name:** Sonos Inc
- **CIK:** 0001314727
- **SIC:** 3651 — Household Audio & Video Equipment
- **Fiscal year end (MM-DD):** 10-03
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SONO

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Sonos Inc
- **CIK:** 1,314,727 · **SIC:** 3651 (Household Audio & Video Equipment) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 16.16 |
| mktcap | $1.9B |
| ev | $1.7B |
| ev_ebit | n/a |
| fcf | $108.2M |
| fcf_yield | 5.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -20.3% |
| net_debt | -$206.9M |
| net_debt_ebit | n/a |
| cash | $206.9M |
| ltd | $0.00 |
| equity | $403.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.4B |
| revenue_prior | $1.5B |
| rev_growth | -4.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$50.5M |
| net_income | -$61.1M |
| cfo | $136.9M |
| capex | $28.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 118,293,979 |
| shares_py | 120,880,277 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 13.1% |
| r6m | 6.3% |
| off_52w_high | -15.7% |
| adv20 | $21.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.54 |
| r_ev_ebit | 0.00 |
| r_roic | 0.06 |
| r_rev_growth | 0.19 |
| r_buyback | 0.80 |
| score | 0.37 |

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
| rank | 353 |

**Screen rationale:** buying back stock -2.1%; debt data missing (net cash unverified); 12-1 momentum 13.1%


## 3. Share count trend

- Shares outstanding: **118,293,979** (CY2026Q2I) vs **120,880,277** prior year (CY2025Q2I)
- Change: **-2.1%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-29** — Item 5.02 (officer / director change or comp arrangement): On July 28, 2026, the board of directors (the "Board") of Sonos, Inc. ("Sonos" or the "Company") increased the size of the Board from ten to eleven members and appointed Chris Shackelton to the Board, effective immediately.
- **2026-05-04** — Item 5.02 (officer / director change or comp arrangement): On April 15, 2026, the Company appointed Frank Barbieri as Chief Operating Officer ("COO") and principal operating officer, effective as of May 4, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 228,970 sh / $3,069,414 vs sells 49,710 sh / $819,042 -> net $2,250,372 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Coliseum Capital Management, LLC / Shackelton Christopher S / Coliseum Capital, LLC / COLISEUM CAPITAL PARTNERS, L.P. / Gray Adam / Coliseum Capital Co-Invest IV, L.P. bought 125,000 sh @ $13.57 ($1,696,250) on 2026-03-17.

Form 4 filings parsed: 12; transaction rows: 37 (open-market buys 4, sales 3).

| code | rows |
|---|---|
| A | 2 |
| F | 6 |
| M | 22 |
| P | 4 |
| S | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'Sonos Reports Third Quarter Fiscal 2026 Results'; skipped 4 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (final3q26earningspressrele.htm)

Sonos Reports Third Quarter Fiscal 2026 Results

Q3 Revenue, GAAP and Non-GAAP Gross Margin and Adjusted EBITDA near high end of guidance range

Santa Barbara, CA – Jul 29, 2026 - Sonos, Inc. (Nasdaq: SONO) today reported Third Quarter Fiscal 2026 results.

"Our third quarter demonstrates the inflection we've been talking about, as revenue growth accelerated and the reinvention of the business continued to take hold," said Tom Conrad, Chief Executive Officer of Sonos. "Over the past 18 months, we've built a leaner, more focused company and a healthier core business centered around our system strategy, and that work is showing up in our results. Revenue grew 9% in Q3, up from 2% in the first half, and we're now growing revenue, expanding gross margin, and growing profit at the same time. We're carrying this momentum into the fourth quarter as we focus on building durable growth while operating with discipline."

"Q3 was another strong quarter, as revenue and Adjusted EBITDA both landed near the high end of our guidance range. We generated healthy free cash flow and built our cash balance sequentially and year over year, while returning $30 million to our shareholders through share repurchases," said Saori Casey, Chief Financial Officer of Sonos. "Q3 marks our eighth consecutive quarter of disciplined execution against our commitments and structurally improving our business."

Third Quarter Fiscal 2026 Financial Highlights (unaudited)

• Revenue increased 9% year-over-year to $375 million

• GAAP gross margin 2 of 50.4%, Non-GAAP gross margin 1 of 45.5%

• GAAP net income 3 increased by $33 million year-over-year to $30 million, GAAP diluted income per share (EPS) 3 increased by $0.28 year-over-year to $0.25

• Non-GAAP net income 1 increased 51% year-over-year to $33 million, Non-GAAP diluted EPS 1 increased 52% year-over-year to $0.27

• Adjusted EBITDA 1 increased 24% year-over-year to $44 million

• Returned $30 million to shareholders through repurchase of 2.0 million shares

• Free cash flow 3 increased by $8 million year-over-year to $40 million

(1) Non-GAAP Gross Margin, Adjusted EBITDA, Non-GAAP Net Income and Non-GAAP EPS are non-GAAP figures and exclude the non-recurring benefit from IEEPA tariff refunds received in Q3 of Fiscal 2026. See "Use of Non-GAAP Measures" and reconciliations to GAAP measures below

(2) Includes $23.2 million of IEEPA tariff refunds

(3) Includes $23.2 million of IEEPA tariff refunds and $0.8 million of interest earned on IEEPA tariff refunds

Guidance

The company will provide guidance on its Third Quarter Fiscal 2026 earnings call.

Supplemental Earnings Presentation

The company has posted a supplemental earnings presentation accompanying its Third Quarter Fiscal 2026 results to the Earnings Reports section of its investor relations website at https://investors.sonos.com/reports-and-filings/default.aspx#section=earningsreports .

Conference Call, Webcast and Transcript

The company will host a webcast of its conference call and Q&A related to its Third Quarter Fiscal 2026 results on July 29, 2026, at 4:30 p.m. Eastern Time (1:30 p.m. Pacific Time). Participants may access the live webcast in listen-only mode on the Sonos investor relations website at https://investors.sonos.com/news-and-events/default.aspx.

The conference call may also be accessed by dialing (888) 330-2454 with conference ID 8641747. Participants outside the U.S. can access the call by dialing (240) 789-2714 using the same conference ID.

An archived webcast of the conference call and a transcript of the company's prepared remarks and Q&A session will also be available at https://investors.sonos.com/reports-and-filings/default.aspx#section=earningsreports following the call.

Condensed Consolidated Statements of Operations and Comprehensive Income (Loss)
(unaudited, in thousands, except share and per share amounts)
Three Months Ended | Nine Months Ended
June 27, 2026 | June 28, 2025 | June 27, 2026 | June 28, 2025
Revenue | $ 375,260 | $ 344,764 | $ 1,202,449 | $ 1,155,376
Cost of revenue | 185,950 | 195,040 | 635,030 | 650,637
Gross profit | 189,310 | 149,724 | 567,419 | 504,739
Operating expenses
Research and development | 67,875 | 59,750 | 191,771 | 218,011
Sales and marketing | 59,624 | 62,576 | 187,273 | 213,430
General and administrative | 30,277 | 30,327 | 88,001 | 89,357
Total operating expenses | 157,776 | 152,653 | 467,045 | 520,798
Operating income (loss) | 31,534 | (2,929) | 100,374 | (16,059)
Other income (expense), net
Interest income | 2,182 | 1,572 | 5,442 | 5,406
Interest expense | (110) | (117) | (330) | (336)
Other income (expense), net | 695 | 661 | (246) | (5,176)
Total other income (expense), net | 2,767 | 2,116 | 4,866 | (106)

Income (loss) before provision for income taxes | 34,301 | (813) | 105,240 | (16,165)
Provision for income taxes | 4,448 | 2,566 | 10,475 | 7,121
Net income (loss) | $ 29,853 | $ (3,379) | $ 94,765 | $ (23,286)
Earnings (loss) per share:
Basic | $ 0.25 | $ (0.03) | $ 0.79 | $ (0.19)
Diluted | $ 0.25 | $ (0.03) | $ 0.77 | $ (0.19)
Weighted-average shares used in computing earnings (loss) per share:
Basic | 118,961,126 | 120,423,439 | 119,886,795 | 120,804,730
Diluted | 120,982,504 | 120,423,439 | 122,761,707 | 120,804,730
Total comprehensive income (loss)
Net income (loss) | 29,853 | (3,379) | 94,765 | (23,286)
Change in foreign currency translation adjustment | (416) | 3,496 | (444) | 3,036
Net unrealized loss on marketable securities | (29) | (23) | (71) | (140)
Comprehensive income (loss) | $ 29,408 | $ 94 | $ 94,250 | $ (20,390)

Condensed Consolidated Balance Sheets
(unaudited, in thousands, except par values)
As of
June 27, 2026 | September 27, 2025
Assets
Current assets:
Cash and cash equivalents | $ 206,894 | $ 174,668
Marketable securities | 54,132 | 52,858
Accounts receivable, net | 117,190 | 65,847
Inventories | 158,143 | 171,020
Prepaids and other current assets | 55,844 | 39,642
Total current assets | 592,203 | 504,035
Property and equipment, net | 60,141 | 72,277
Operating lease right-of-use assets | 42,790 | 45,297
Goodwill | 82,854 | 82,854
Intangible assets, net | 64,418 | 75,356
Deferred tax assets | 10,043 | 10,509
Other noncurrent assets | 29,672 | 32,950
Total assets | $ 882,121 | $ 823,278

Liabilities and stockholders' equity
Current liabilities:
Accounts payable | $ 179,897 | $ 184,109
Accrued expenses | 87,889 | 79,094
Accrued compensation | 31,249 | 21,331
Deferred revenue, current | 21,989 | 21,771
Other current liabilities | 45,775 | 46,107
Total current liabilities | 366,799 | 352,412
Operating lease liabilities, noncurrent | 50,192 | 53,288
Deferred revenue, noncurrent | 58,515 | 59,453
Deferred tax liabilities | 113 | 126
Other noncurrent liabilities | 2,970 | 2,774
Total liabilities | 478,589 | 468,053
Commitments and contingencies
Stockholders' equity:
Common stock, $0.001 par value | 121 | 123
Treasury stock | (46,529) | (37,398)
Additional paid-in capital | 465,965 | 502,775
Accumulated deficit | (17,313) | (112,078)
Accumulated other comprehensive income | 1,288 | 1,803
Total stockholders' equity | 403,532 | 355,225
Total liabilities and stockholders' equity | $ 882,121 | $ 823,278

Condensed Consolidated Statements of Cash Flows
(unaudited, dollars in thousands)
Nine Months Ended
June 27, 2026 | June 28, 2025
Cash flows from operating activities
Net income (loss) | $ 94,765 | $ (23,286)
Adjustments to reconcile net income (loss) to net cash provided by operating activities:
Stock-based compensation expense | 46,386 | 64,789
Depreciation and amortization | 36,924 | 48,657
Restructuring and other charges | 1,088 | 6,323
Provision for excess and obsolete inventory | 1,573 | 9,242
Deferred income taxes | 386 | 942
Other | 5,078 | 2,432
Foreign currency transaction loss | 2,122 | 572
Changes in operating assets and liabilities:

Accounts receivable | (53,604) | (49,010)
Inventories | 11,303 | 106,223
Other assets | (15,882) | 11,616
Accounts payable and accrued expenses | 6,021 | (55,341)
Accrued compensation | 10,330 | 10,352
Deferred revenue | (157) | (1,033)
Other liabilities | (2,166) | 1,470
Net cash provided by operating activities | 144,167 | 133,948
Cash flows from investing activities
Purchases of marketable securities | (44,616) | (43,949)
Purchases of property and equipment | (16,681) | (23,418)
Maturities of marketable securities | 43,340 | 43,200
Net cash used in investing activities | (17,957) | (24,167)
Cash flows from financing activities
Payments for repurchase of common stock | (95,277) | (60,602)
Payments for repurchase of common stock related to shares withheld for tax in connection with vesting of stock awards | (20,417) | (20,754)
Proceeds from exercise of stock options | 23,101 | 2,653
Payments for debt issuance costs | (780) | —
Net cash used in financing activities | (93,373) | (78,703)
Effect of exchange rate changes on cash and cash equivalents | (611) | 463
Net increase in cash and cash equivalents | 32,226 | 31,541
Cash and cash equivalents
Beginning of period | 174,668 | 169,732
End of period | $ 206,894 | $ 201,273
Supplemental disclosure
Cash paid for interest | $ 185 | $ 197
Cash paid for taxes, net of refunds | $ 4,387 | $ 19,065
Cash paid for amounts included in the measurement of lease liabilities, net of tenant improvement reimbursements received | $ 7,088 | $ 3,460
Supplemental disclosure of non-cash investing and financing activities
Purchases of property and equipment in accounts payable and accrued expenses | $ 3,635 | $ 2,155
Right-of-use assets obtained in exchange for new operating lease liabilities | $ 1,829 | $ 1,491
Excise tax on share repurchases, accrued but not paid | $ 258 | $ 187

Reconciliation of GAAP to Non-GAAP Cost of Revenue and Gross Profit
(unaudited, in thousands, except percentages)
Three Months Ended | Nine Months Ended
June 27, 2026 | June 28, 2025 | June 27, 2026 | June 28, 2025
Reconciliation of GAAP cost of revenue
GAAP cost of revenue | $ 185,950 | $ 195,040 | $ 635,030 | $ 650,637
Stock-based compensation expense | 1,257 | 1,633 | 3,709 | 4,588
Amortization of intangibles | 3,278 | 3,278 | 10,802 | 9,752
Restructuring and other charges | 131 | (514) | 795 | 3,420
IEEPA tariff refund benefit | (23,154) | — | (23,154) | —
Non-GAAP cost of revenue | $ 204,438 | $ 190,643 | $ 642,878 | $ 632,877
Reconciliation of GAAP gross profit
GAAP gross profit | $ 189,310 | $ 149,724 | $ 567,419 | $ 504,739
Stock-based compensation expense | 1,257 | 1,633 | 3,709 | 4,588
Amortization of intangibles | 3,278 | 3,278 | 10,802 | 9,752
Restructuring and other charges | 131 | (514) | 795 | 3,420
IEEPA tariff refund benefit | (23,154) | — | (23,154) | —
Non-GAAP gross profit | $ 170,822 | $ 154,121 | $ 559,571 | $ 522,499
GAAP gross margin | 50.4% | 43.4% | 47.2% | 43.7%
Non-GAAP gross margin | 45.5% | 44.7% | 46.5% | 45.2%

Reconciliation of Selected Non-GAAP Financial Measures
(unaudited, dollars in thousands)
Three Months Ended | Nine Months Ended
June 27, 2026 | June 28, 2025 | June 27, 2026 | June 28, 2025
Research and Development (GAAP) | $ 67,875 | $ 59,750 | $ 191,771 | $ 218,011
Stock-based compensation | 5,909 | 7,944 | 17,869 | 29,280
Amortization of intangibles | 20 | 20 | 61 | 216
Restructuring and other charges (2)(3) | 4,014 | (824) | 4,871 | 11,882
Research and Development (Non-GAAP) | $ 57,932 | $ 52,610 | $ 168,970 | $ 176,633
Sales and Marketing (GAAP) | $ 59,624 | $ 62,576 | $ 187,273 | $ 213,430
Stock-based compensation | 2,884 | 3,466 | 8,492 | 13,078
Amortization of intangibles | - | - | - | -
Restructuring and other charges (2)(3) | 46 | 1,038 | 1,499 | 3,831
Sales and Marketing (Non-GAAP) | $ 56,694 | $ 58,072 | $ 177,282 | $ 196,521
General and Administrative (GAAP) | 30,277 | 30,327 | 88,001 | 89,357
Stock-based compensation | 6,280 | 6,309 | 16,316 | 17,843

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-11-14_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Comparison of Fiscal Years 2025 and 2024

Revenue

Fiscal Year Ended | Change from Prior Fiscal Year
September 27, 2025 | September 28, 2024 | %
(Dollars in thousands)
Sonos speakers | 1,121,808 | 1,169,604 | (47,796) | (4.1) | %
% of total revenue | 77.7 | % | 77.0 | %
Sonos system products | 249,237 | 267,744 | (18,507) | (6.9)
% of total revenue | 17.3 | % | 17.6 | %
Partner products and other revenue | 72,231 | 80,708 | (8,477) | (10.5)
% of total revenue | 5.0 | % | 5.3 | %
Total revenue | 1,443,276 | 1,518,056 | (74,780) | (4.9) | %
Volume data (products sold in thousands) | Units | %
Total products sold | 4,625 | 5,000 | (375) | (7.5) | %

Total revenue decreased $74.8 million, or 4.9% for fiscal 2025 compared to fiscal 2024, driven by challenges resulting from our app rollout in May 2024 and softer demand due to market conditions, partially offset by the introduction of Arc Ultra in October 2024.

Sonos speakers represented 77.7% of total revenue for fiscal 2025 and decreased 4.1% compared to fiscal 2024, primarily driven by expected declines in Arc and Sonos One, as well as Beam, Move, and Sub Mini. These declines were partially offset by the

introduction of Arc Ultra, as well as Era 100. Sonos system products represented 17.3% of total revenue for fiscal 2025 and decreased 6.9% compared fiscal 2024. Partner products and other revenue represented 5.0% of total revenue for fiscal 2025, and decreased 10.5% compared to fiscal 2024.

The volume of products sold decreased 7.5% for fiscal 2025, compared to fiscal 2024.

Revenue by Region

Fiscal Year Ended
September 27, 2025
Change (%) | Constant Currency Change (%) (1)
Americas | (8.1 | %) | (7.7 | %)
Europe, Middle East and Africa | 2.5 | % | 0.4 | %
Asia Pacific | (4.5 | %) | (3.4 | %)

(1) Constant currency is a financial measure that is not calculated in accordance with U.S. GAAP. For additional information, see the section titled "Non-GAAP Financial Measures" above.

Cost of Revenue and Gross Profit

Fiscal Year Ended | Change from Prior Fiscal Year
September 27, 2025 | September 28, 2024 | %
(Dollars in thousands)
Cost of revenue | 812,746 | 828,683 | (15,937) | (1.9) | %
Gross profit | 630,530 | 689,373 | (58,843) | (8.5) | %
Gross margin | 43.7 | % | 45.4 | %

Cost of revenue consists of product costs, including costs of our contract manufacturers for production, components, shipping and handling, tariffs, duty costs, warranty replacement costs, packaging, fulfillment costs, manufacturing and tooling equipment depreciation, warehousing costs, hosting costs, and excess and obsolete inventory write-downs. It also includes licensing costs, such as royalties to third parties, and amortization attributable to acquired developed technology. In addition, we allocate certain costs related to management and facilities, personnel-related expenses, and supply chain logistic costs. Personnel-related expenses consist of salaries, bonuses, benefits, and stock-based compensation expenses.

Cost of revenue decreased $15.9 million, or 1.9%, for fiscal 2025 compared to fiscal 2024, primarily due to a decrease in product and material costs as well as decrease in products sold, partially offset by the impact of reorganization efforts, and increased amortization primarily related to the completion of our Mayht in-process research and development project and related reclassification into finite-lived intangible assets.

Gross margin decreased approximately 170 basis points for fiscal 2025 compared to fiscal 2024. The decrease was primarily due to the impact of reorganization efforts, unfavorable channel mix, and increased amortization primarily related to the completion of our Mayht in-process research and development project and related reclassification into finite-lived intangible assets, partially offset by decreased product and material costs.

Operating Expenses

Fiscal Year Ended | Change from Prior Fiscal Year
September 27, 2025 | September 28, 2024 | %
(Dollars in thousands)
Research and development | 279,969 | 304,558 | (24,589) | (8.1 | %)
Less restructuring and other charges (1) | 12,555 | 5,743 | 6,812 | 118.6
Research and development, net of restructuring and other charges | 267,414 | 298,815 | (31,401) | (10.5 | %)
Sales and marketing | 281,192 | 290,609 | (9,417) | (3.2) | %
Less restructuring and other charges (1) | 9,779 | 2,770 | 7,009 | 253.0
Sales and marketing, net of restructuring and other charges | 271,413 | 287,839 | (16,426) | (5.7) | %
General and administrative | 119,837 | 142,252 | (22,415) | (15.8) | %
Less restructuring and other charges (1) | 7,736 | 3,340 | 4,396 | 131.6
General and administrative, net of restructuring and other charges | 112,101 | 138,912 | (26,811) | (19.3) | %
Operating expenses | 680,998 | 737,419 | (56,421) | (7.7) | %
Less restructuring and other charges (1) | 30,070 | 11,853 | 18,217 | 153.7
Operating expenses, net of restructuring and other charges | 650,928 | 725,566 | (74,638) | (10.3) | %

(1) Restructuring and other charges for fiscal 2025 and fiscal 2024 primarily reflect costs associated with our cost transformation initiatives including the 2024 restructuring plan, 2025 restructuring plan, rationalization of our product roadmap, and non-recurring costs related to write-offs of assets no longer in use, as well as non-recurring CEO transition costs related to modifications to equity awards. See Note 13. Restructuring and Other Charges in the notes to our consolidated financial statement for further information.

Research and Development

Research and development expenses consist primarily of personnel-related expenses, third-party resources expenses, tooling, test equipment, prototype materials, and related overhead costs. To date, software development costs have been expensed as incurred because the period between achieving technological feasibility and the release of the software has been short and development costs qualifying for capitalization have been insignificant.

Research and development expenses excluding restructuring and other charges decreased $31.4 million, or 10.5%, for fiscal 2025 compared to fiscal 2024. This decrease was primarily driven by lower personnel-related costs due to lower headcount and our reorganization efforts, partially offset by higher variable compensation costs.

Sales and Marketing

Sales and marketing expenses consist primarily of advertising and marketing activity for our products and personnel-related expenses, maintenance and repair expenses for product displays, as well as related depreciation, customer experience expenses, revenue related sales fees from our direct-to-consumer and installer solutions sales channels, and related overhead costs.

Sales and marketing expenses excluding restructuring and other charges decreased $16.4 million, or 5.7%, for fiscal 2025 compared to fiscal 2024. This decrease was primarily driven by lower marketing costs compared to prior year when we incurred significant costs associated with our launch of Sonos Ace in June 2024 marking our entry into the headphones market, partially offset by increased depreciation costs associated with our product displays.

General and Administrative

General and administrative expenses consist of administrative personnel-related expenses for our information technology, finance, legal, human resources, and similar personnel, as well as the costs of professional services, information technology, litigation, patents, related overhead, and other administrative expenses.

General and administrative expenses excluding restructuring and other charges decreased $26.8 million, or 19.3%, for fiscal 2025 compared to the fiscal 2024. This decrease was primarily driven by lower personnel-related costs, professional fees and information technology costs as a result of lower headcount and our cost transformation efforts.

Interest Income, Interest Expense, and Other Income (Expense), Net

Fiscal Year Ended | Change from Prior Fiscal Year
September 27, 2025 | September 28, 2024 | %
(Dollars in thousands)
Interest income | 6,934 | 11,965 | (5,031) | (42.0 | %)
Interest expense | (465) | (441) | (24) | 5.4
Other income (expense), net | (6,498) | 9,371 | (15,869) | (169.3)
Total other income (expense), net | (29) | 20,895 | (20,924) | (100.1) | %

Interest income consists primarily of interest income earned on our cash, cash equivalents, and marketable securities balances. Interest expense consists primarily of interest expense associated with our debt financing arrangements and amortization of debt issuance costs. Other income (expense), net consists primarily of our foreign currency exchange gains and losses relating to transactions and remeasurement of asset and liability balances denominated in currencies other than the U.S. dollar. We expect our foreign currency gains and losses to continue to fluctuate in the future due to changes in foreign currency exchange rates.

Interest income for fiscal 2025 compared to fiscal 2024 decreased primarily due to lower yields on our cash and cash equivalents combined with lower average cash balances. Interest expense for fiscal 2025, compared to fiscal 2024, increased primarily due to increased bank fees. The increase in other income (expense), net for fiscal 2025, compared to fiscal 2024, was primarily due to non-cash foreign currency exchange fluctuations.

Provision for Income Taxes

Fiscal Year Ended | Change from Prior Fiscal Year
September 27, 2025 | September 28, 2024 | %
(Dollars in thousands)
Provision for income taxes | 10,647 | 10,995 | (348) | (3.2) | %

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-11-14_item1_business.md)

Item 1: Business

Overview

Sonos is a leading audio company dedicated to elevating life through sound. Since pioneering multi-room wireless audio in 2005, Sonos has built a system that unites every dimension of sound - music, movies, stories and conversations - into one connected platform. The portfolio includes home theater speakers, components, plug-in and portable speakers, and headphones that compound in value with every room and device its customers add. Known for exceptional sound, thoughtful design, ease of use and seamless access to the world's audio content, Sonos is trusted by more than 17 million households in 60+ countries around the world.

Since we launched our first product 20 years ago, we have grown our install base by launching innovative new products, delivering a seamless customer experience, and expanding our global footprint. In fiscal 2025, existing customers accounted for approximately 45% of new product registrations. As of September 27, 2025, we had a total of nearly 53.4 million products registered in approximately 17.1 million households globally. Our customers have typically purchased additional Sonos products over time. As of September 27, 2025, 61% of our 17.1 million households had registered more than one Sonos product. As of September 27, 2025, our households owned 3.13 products on average.

In fiscal 2025, we made several executive leadership changes, including the appointment of Tom Conrad as our new Chief Executive Officer in July 2025 following his tenure as interim Chief Executive Officer since January 2025. Under Mr. Conrad's direction, we have significantly improved our software products, reorganized our operations to improve our efficiency and effectiveness and recommitted to delivering the kind of premium experience our customers expect. With every new product, software feature and integration, the Sonos platform becomes more powerful and provides greater value to our customers.

We started a cost transformation initiative in fiscal 2024 aimed at optimizing our investments for sustainable, long-term growth and to enhance our agility. We have taken steps to streamline, reorganize and flatten our organizational structures, including workforce reductions of approximately 6% in August 2024 (the "2024 restructuring plan") and approximately 12% in February 2025 (the "2025 restructuring plan"). See Note 13. Restructuring and Other Charges in the notes to our consolidated financial statements for further information. Furthermore, we remain focused on additional transformation efforts to improve both our operational efficiency and effectiveness. Additionally, during the third quarter of fiscal 2025, we began the process of exiting a partnership with one of our contract manufacturers to consolidate and improve supply chain efficiency. We expect to complete this exit with minimal disruption to our business by the second quarter of fiscal 2026. We continue to maintain diversified contract manufacturing partnerships.

Macroeconomic environment

Our business and financial performance depend significantly on worldwide economic conditions. We face global macroeconomic challenges such as inflation, ongoing geopolitical conflicts, uncertainty in the financial markets, volatility in exchange rates, low or negative growth in certain regions, declining consumer sentiment of international customers towards U.S.-based companies as a result of U.S. trade policy, and uncertainty in consumer demand. In addition, our business may be adversely impacted by the potential expansion of tariffs on goods imported into the U.S., as well as any retaliatory tariffs or policies enacted in other countries or any "trade wars."

Global economic and political conditions and uncertainties, including global trade tensions, have caused and may continue to cause volatility in demand for our products as well as cost of materials and logistics, and as a result may impact our results of operations. We are continuing to evaluate and implement mitigating actions, including taking measures to manage our expenses and contain costs, leveraging our supply chain flexibility and evaluating potential pricing and promotion strategies.

Our Purpose

Our purpose is to elevate life through sound. We deliver this through the Sonos system, which unites every dimension of sound - music, movies, stories, and conversations - into one connected platform.

The Sonos system is independent by design and is the premier platform to connect first and third party experiences with incredible audio. We bring together Bluetooth, Airplay, Spotify Connect, and analog sources alongside formats like Dolby Atmos and lossless audio to uniquely deliver every dimension of sound. As our platform grows, its value to our customer compounds: stronger with scale, smarter through continual evolution, and more essential to our customers over time.

Our Strategy

The Sonos platform occupies a unique and trusted position in our customers' homes. Our hardware and software roadmaps are designed to build on this position in the home to deliver a set of exceptional experiences that make Sonos even more relevant and

beloved in the eyes of our customers. Our growth strategy is underpinned by a compounding model built on generating new households and increasing lifetime value.

Generating New Households

We aim to expand our installed base by introducing Sonos to more homes around the world. This includes developing compelling gateway products, executing sharper and more resonant marketing campaigns that articulate our brand story, and continuing our international expansion efforts.

Increasing Lifetime Value

We seek to deepen relationships with existing households by growing their Sonos systems over time: adding new rooms, new products, or more comprehensive room setups.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-11-14_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-11-14_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-11-14_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2025-11-14_item7_mdna.md, 10-K_2025-11-14_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
