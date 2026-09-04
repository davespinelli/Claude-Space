# Triage pack — TLS · TELOS CORP

_Generated 2026-09-04 23:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TLS · **Name:** TELOS CORP
- **CIK:** 0000320121
- **SIC:** 7373 — Services-Computer Integrated Systems Design
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TLS

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** TELOS CORP
- **CIK:** 320,121 · **SIC:** 7373 (Services-Computer Integrated Systems Design) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 4.87 |
| mktcap | $364.0M |
| ev | $313.3M |
| ev_ebit | n/a |
| fcf | $29.4M |
| fcf_yield | 8.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -73.7% |
| net_debt | -$50.6M |
| net_debt_ebit | n/a |
| cash | $50.6M |
| ltd | $0.00 |
| equity | $93.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $164.8M |
| revenue_prior | $108.3M |
| rev_growth | 52.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$39.9M |
| net_income | -$36.5M |
| cfo | $30.2M |
| capex | $739k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 74,736,789 |
| shares_py | 72,703,011 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -27.7% |
| r6m | 11.7% |
| off_52w_high | -37.2% |
| adv20 | $2.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.65 |
| r_ev_ebit | 0.00 |
| r_roic | 0.01 |
| r_rev_growth | 0.95 |
| r_buyback | 0.27 |
| score | 0.38 |

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
| rank | 349 |

**Screen rationale:** revenue +52.2%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **74,736,789** (CY2026Q2I) vs **72,703,011** prior year (CY2025Q2I)
- Change: **2.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-28** — Item 5.02 (officer / director change or comp arrangement): Effective May 28, 2026, John B. Wood, President, Chief Executive Officer and Chairman of the Board of Telos Corporation (the "Company"), has returned from his medical leave of absence and has resumed his full duties and responsibilities.
- **2026-05-07** — Item 5.02 (officer / director change or comp arrangement): On May 7, 2026 Telos Corporation (the "Company") held the annual meeting of its stockholders.
- **2026-04-29** — Item 5.02 (officer / director change or comp arrangement): Telos Corporation (the "Company") has announced that John B. Wood, the Company's President, Chief Executive Officer and Chairman of the Board, is taking a medical leave of absence.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 406,170 sh / $1,782,531 -> net $-1,782,531 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 0, sales 9).

| code | rows |
|---|---|
| A | 8 |
| F | 1 |
| S | 9 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-10_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Financial Results'; skipped 9 forward-looking-statement block(s); 16 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q22026earningspressrelease.htm)

## EX-99.2 - EX-99.2 (q22026june302026financialr.htm)

Second Quarter 2026 Financial Results

August 10, 2026

Telos Corporation Reports 33% Revenue Growth and Continued Robust Cash Flow Margins; Raises Full Year Profit Guidance

• Substantial Growth: Revenue grew 33% year-over-year to $47.7 million, exceeding guidance, and driven by 44% growth in Security Solutions primarily due to the expansion of large programs in Telos ID.

• Healthy Gross Margins: GAAP Gross Margin and Cash Gross Margin 1 both exceeded guidance assumptions and expanded YoY primarily due to performance of Telos ID. GAAP Gross Margin was 35.0% and Cash Gross Margin 1 was 40.6%.

• Disciplined Cost Management: GAAP Operating Expenses declined 25% year-over-year primarily due to lower stock-based compensation expense. Adjusted Operating Expenses 1 declined 6% primarily due to restructuring and ongoing cost management initiatives.

• Expanded Operating Margins: GAAP Net Income was $0.7 million; Adjusted EBITDA 1 was $6.9 million, exceeding guidance. GAAP Net Income Margin was 1.4%; Adjusted EBITDA Margin 1 expanded from 1.1% to 14.4% year-over-year primarily due to revenue growth in Telos ID and lower operating expenses.

• Robust Cash Flow Margins: Cash Flow from Operations was $8.8 million or 18.5% of revenue. Free Cash Flow 1 increased 43% year-over-year to $6.6 million. Free Cash Flow Margin 1 was 13.9% and represents the sixth consecutive quarter over 12.0%.

• Continued Share Repurchases: Deployed $4.7 million to repurchase over 1.0 million shares at an average price of $4.50 per share.

• Forecast : Sequential revenue growth and ongoing share repurchases in the third quarter. Raising full year profit outlook on slightly lower revenues.

Financial Guidance for the Third Quarter and Full Year Ending December 31, 2026
Third Quarter | Full Year
Prior | Updated
Revenue | $49.2 million - $50.6 million | $187 million - $200 million | $187 million - $195 million
Year-Over-Year Growth | (4%) - (2%) | 14% - 21% | 14% - 18%
Adjusted EBITDA 2 | $6.0 million - $6.8 million | $20.6 million - $28.0 million | $23.6 million - $28.6 million
Adjusted EBITDA Margin 2 | 12.2% - 13.4% | 11.0% - 14.0% | 12.6% - 14.7%

1 Cash Gross Margin, Adjusted Operating Expenses, Adjusted EBITDA, Adjusted EBITDA Margin, Free Cash Flow and Free Cash Flow Margin are non-GAAP financial measures. Refer to "Non- GAAP Financial Measures" below.

2 Adjusted EBITDA and Adjusted EBITDA Margin are non-GAAP financial measures. The Company has not provided a reconciliation to the most directly comparable GAAP measures to these forward-looking non-GAAP financial measures because certain items are out of the Company's control or cannot be reasonably predicted. Accordingly, reconciliations of forward-looking Adjusted EBITDA and Adjusted EBITDA Margin are not available without unreasonable effort.

Second Quarter 2026 Financial Highlights
Three Months Ended
June 30, 2026 | June 30, 2025
(amounts in millions, except per share data)
Revenue | 47.7 | 36.0
Gross Profit | 16.7 | 11.9
Gross Margin | 35.0 | % | 33.2 | %
Adjusted Gross Profit 1 | 16.9 | 12.1
Adjusted Gross Margin 1 | 35.4 | % | 33.6 | %
Cash Gross Profit 1 | 19.4 | 13.8
Cash Gross Margin 1 | 40.6 | % | 38.4 | %
GAAP Net Income (Loss) | 0.7 | (9.5)
GAAP Net Income (Loss) Margin | 1.4 | % | (26.5 | %)
Adjusted Net Income (Loss) 1 | 3.4 | (2.3)
EBITDA 1 | 3.7 | (7.4)
Adjusted EBITDA 1 | 6.9 | 0.4
Adjusted EBITDA Margin 1 | 14.4 | % | 1.1 | %
GAAP EPS, basic | 0.01 | (0.13)
Weighted-average Shares of Common Stock Outstanding, basic (GAAP) | 74.9 | 73.2
GAAP EPS, diluted 2 | 0.01 | (0.13)
Weighted-average Shares of Common Stock Outstanding, diluted/basic 2 (GAAP) | 77.5 | 73.2
Adjusted EPS 1 | 0.04 | (0.03)
Weighted-average Shares of Common Stock Outstanding, diluted/basic 2 (non-GAAP) | 77.5 | 73.2
Cash Flow from Operations | 8.8 | 7.0
Free Cash Flow 1 | 6.6 | 4.6
Free Cash Flow Margin 1 | 13.9 | % | 12.9 | %
1 Adjusted Gross Profit, Adjusted Gross Margin, Cash Gross Profit, Cash Gross Margin, Adjusted Net Income (Loss), EBITDA, Adjusted EBITDA, Adjusted EBITDA Margin, Adjusted EPS, Free Cash Flow, and Free Cash Flow Margin are non-GAAP financial measures. Refer to "Non-GAAP Financial Measures" below.

2 This line is labeled "diluted/basic" because for a period of net loss, potentially dilutive shares are not included in the calculation of diluted earnings (loss) per share, because to do so would be anti-dilutive. For the second quarter of 2025, the basic and diluted weighted-average share of common stock outstanding are the same due to a Net Loss position.

About Telos Corporation

Telos Corporation (NASDAQ: TLS) empowers and protects the world's most security-conscious organizations with efficient, adaptable, and secure solutions that safeguard people, systems, and information. We deliver advanced capabilities across cyber governance, risk, and compliance (GRC) with Xacta ® ; identity and biometric solutions; secure networks and communications; and TSA PreCheck ® enrollment services. Serving the U.S. federal government, regulated industries, and global enterprises, Telos helps customers stay ahead of evolving threats, accelerate compliance, and achieve mission success. Driven by purpose and guided by our core values, we build trusted partnerships, deliver superior solutions, and help create a more secure, interconnected world. Learn more at www.telos.com .

Media:

media@telos.com

Investors:

InvestorRelations@telos.com

TELOS CORPORATION

CONSOLIDATED STATEMENTS OF OPERATIONS

(Unaudited)

For the Three Months Ended | For the Six Months Ended
June 30, 2026 | June 30, 2025 | June 30, 2026 | June 30, 2025
(in thousands, except per share amounts)
Revenue – Security Solutions | 46,662 | 32,474 | 92,632 | 58,292
Revenue – Secure Networks | 1,083 | 3,494 | 2,855 | 8,292
Total revenue | 47,745 | 35,968 | 95,487 | 66,584
Cost of sales – Security Solutions (excluding depreciation and amortization) | 27,651 | 19,462 | 54,165 | 32,719
Cost of sales – Secure Networks (excluding depreciation and amortization) | 888 | 2,859 | 2,145 | 6,533
Depreciation and amortization | 2,514 | 1,715 | 5,110 | 3,218
Total cost of sales | 31,053 | 24,036 | 61,420 | 42,470
Gross profit | 16,692 | 11,932 | 34,067 | 24,114
Operating expenses:
Research and development expenses | 1,345 | 1,512 | 2,702 | 3,083
Selling, general and administrative expenses | 15,037 | 20,303 | 29,600 | 39,936
Total operating expenses | 16,382 | 21,815 | 32,302 | 43,019
Operating income (loss) | 310 | (9,883) | 1,765 | (18,905)
Other income | 501 | 553 | 1,198 | 1,114
Interest expense | (107) | (141) | (218) | (288)
Income (loss) before income taxes | 704 | (9,471) | 2,745 | (18,079)
Provision for income taxes | (44) | (46) | (62) | (42)
Net income (loss) | 660 | (9,517) | 2,683 | (18,121)
Net income (loss) per share:
Basic | 0.01 | (0.13) | 0.04 | (0.25)
Diluted | 0.01 | (0.13) | 0.03 | (0.25)
Weighted-average shares outstanding:
Basic | 74,895 | 73,163 | 74,361 | 72,940
Diluted | 77,547 | 73,163 | 77,576 | 72,940

TELOS CORPORATION

CONSOLIDATED BALANCE SHEETS

(Unaudited)

June 30, 2026 | December 31, 2025
(in thousands, except per share amount and share data)
Assets:
Cash and cash equivalents | 50,647 | 53,180
Accounts receivable, net | 18,000 | 17,000
Inventories, net | 4,917 | 996
Prepaid expenses | 7,562 | 10,565
Deferred program expenses | 13,920 | 10,006
Other current assets | 1,779 | 2,666
Total current assets | 96,825 | 94,413
Property and equipment, net | 2,490 | 3,071
Finance lease right-of-use assets, net | 3,560 | 4,170
Operating lease right-of-use assets, net | 298 | 410
Goodwill | 3,006 | 3,006
Intangible assets, net | 29,213 | 30,281
Other assets | 4,357 | 4,513
Total assets | 139,749 | 139,864
Liabilities and Stockholders' Equity
Liabilities:
Accounts payable | 6,390 | 4,087
Accrued liabilities | 5,673 | 6,900
Accrued compensation and benefits | 8,985 | 12,309
Contract liabilities – current portion | 17,220 | 11,223
Finance lease obligations – current portion | 2,113 | 2,033
Operating lease obligations – current portion | 255 | 232
Total current liabilities | 40,636 | 36,784
Contract liabilities – non-current portion | 874 | 1,124
Finance lease obligations – non-current portion | 4,536 | 5,608
Operating lease obligations – non-current portion | 62 | 186
Deferred income taxes | 57 | 53
Other liabilities | 171 | 159
Total liabilities | 46,336 | 43,914
Commitments and contingencies
Stockholders' equity:
Common stock, $0.001 par value, 250,000,000 shares authorized, 74,736,789 shares and 72,773,272 shares issued and outstanding as of June 30, 2026 and December 31, 2025, respectively | 113 | 111
Additional paid-in capital | 454,611 | 459,828
Accumulated other comprehensive loss | (101) | (96)
Accumulated deficit | (361,210) | (363,893)
Total stockholders' equity | 93,413 | 95,950
Total liabilities and stockholders' equity | 139,749 | 139,864

TELOS CORPORATION

CONSOLIDATED STATEMENTS OF CASH FLOWS

(Unaudited)

For the Three Months Ended | For the Six Months Ended
June 30, 2026 | June 30, 2025 | June 30, 2026 | June 30, 2025
(in thousands)
Cash flows from operating activities:
Net income (loss) | 660 | (9,517) | 2,683 | (18,121)
Adjustments to reconcile net income (loss) to cash flows from operations:
Stock-based compensation | 3,213 | 7,757 | 6,184 | 14,805
Depreciation and amortization | 3,347 | 2,509 | 6,776 | 4,845
Loss on disposal of fixed assets | 1 | — | 52 | —
Provision for inventory obsolescence | 42 | — | 42 | —
Amortization of debt issuance costs | 9 | 18 | 17 | 35
Deferred income taxes | 2 | 31 | 4 | 27
Provision for (recovery from) doubtful accounts | — | (15) | 1 | (20)
Changes in operating assets and liabilities:
Accounts receivable | (1,576) | (341) | (1,001) | 86
Inventories | (817) | (1,373) | (1,942) | (1,079)
Prepaid expenses, deferred program expenses, other current assets and other assets | 7,069 | (4,655) | 4,445 | (1,933)
Accounts payable | (594) | 9,628 | (2,158) | 9,540
Accrued compensation and benefits | 325 | 226 | (208) | 601
Contract liabilities | (953) | 6,207 | 5,746 | 6,114
Accrued liabilities and other liabilities | (1,895) | (3,525) | (3,152) | (1,844)
Net cash provided by operating activities | 8,833 | 6,950 | 17,489 | 13,056
Cash flows from investing activities:
Capitalized software development costs | (1,970) | (2,187) | (4,102) | (4,401)
Purchases of property and equipment | (246) | (134) | (391) | (257)
Net cash used in investing activities | (2,216) | (2,321) | (4,493) | (4,658)
Cash flows from financing activities:
Payment of tax withholding related to net share settlement of equity awards | (1,007) | (958) | (7,626) | (1,062)
Repurchases of common stock | (4,691) | (4,002) | (6,889) | (4,002)
Payments under finance lease obligations | (501) | (462) | (992) | (914)
Payments for debt issuance costs | — | — | (21) | —
Net cash used in financing activities | (6,199) | (5,422) | (15,528) | (5,978)
Net change in cash, cash equivalents, and restricted cash | 418 | (793) | (2,532) | 2,420
Cash, cash equivalents, and restricted cash, beginning of period | 50,370 | 57,930 | 53,320 | 54,717
Cash, cash equivalents, and restricted cash, end of period | 50,788 | 57,137 | 50,788 | 57,137

NON-GAAP FINANCIAL MEASURES

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-16_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

For an overview of our business, including our business segments and a discussion of the services and products we provide, see Item 1, "Business " in Part I and Note 1 6 – Segment Information of the notes to the consolidated financial statements contained within this 10-K.

As discussed under Item 1A, "Risk Factors ," we derive a substantial portion of our revenues from contracts and subcontracts with the U.S. federal government. Our revenues are generated from a number of contract vehicle and task orders. The U.S. federal government has increasingly relied on contracts that are subject to a competitive bidding process (including BPA and IDIQ Task Orders, OTAs, and other GSA schedule solicitations), resulting in greater competition and increased pricing pressure. We expect that a majority of the business that we seek in the foreseeable future will be awarded through a competitive bidding process.

Over the past several years we have sought to diversify and improve our operating margins through the evolution of our business from an emphasis on product reselling to an advanced solutions technologies provider. Although we continue to offer resold products through our contract vehicles or our prime partners' contracts, we have focused on the transformation and growth of our software and service solutions offerings, as well as the design and delivery of our manufactured and branded technologies. We emphasize leveraging technology and innovation, specifically in cybersecurity, cloud, and identity solutions, to drive growth and ensure a secure and defendable network. We continue to invest in and develop in AI integration, enhancing automation and improving existing solutions to maintain a competitive edge.

We believe our contract portfolio reflects low to moderate financial risk due to the limited number of long-term fixed-price development contracts, thus minimizing the risk of cost overruns. Our firm-fixed-price activities consist primarily of contracts for products and services at established contract prices that are designed to be repeatable solution offerings. For 2025 and 2024, the Company's revenue derived from firm-fixed-price contracts was 73.3% and 75.3%, respectively; time-and-material contract revenue was 21.8% and 14.6%, respectively; and cost-plus contract revenue was 4.9% and 10.1%, respectively.

Business Environment

U.S. Federal Government Budget

In fiscal year ("FY") 2025, we generated approximately 91.0% of our revenues from the U.S. federal government, either as prime contractor or a subcontractor to other contractors engaged in work for the U.S. federal government, including 58.1% of our revenue from the DoW. Accordingly, our business performance is affected by the overall level of U.S. federal government spending and the alignment of our offerings and capabilities with current and future budget priorities of the U.S. federal government.

While we view the budget environment as constructive and believe there is bipartisan support for continued investment in the areas of defense and national security, it is uncertain when (and if) in any particular government fiscal year appropriations bills will be passed. During those periods of time when appropriations bills have not been passed and signed into law, U.S. federal government agencies operate under a continuing resolution ("CR"), a temporary measure that allows the government to continue operations at prior year funding levels.

The FY2025 U.S. federal government appropriations, which ran through September 30, 2025, were determined by a full-year CR. While the Administration has submitted its FY2026 budget proposal outlining its priorities, partisan disagreements over federal spending levels, among other things, have stalled progress on the required appropriations bills. Recently, on February 3, 2026, Congress passed another full-year CR for FY2026 to end the partial government shutdown. This enacted bill provides full-year funding for several programs, including defense and national security, through September 30, 2026; and also extended homeland security funding through February 13, 2026. A partial government shutdown began on February 14, 2026 after the lawmakers and the White House failed to reach a deal on legislation to fund DHS through September 2026. The impasse affects agencies such as the Transportation Security Administration, the Federal Emergency Management Agency, U.S. Coast Guard, the Secret Service, U.S. Immigration and Custom Enforcement, and U.S. Customs and Border Protection.

Congress approved a FY2026 Defense Appropriations Bill that provides $838.7 billion in discretionary funding, including $838.5 billion in defense funding and $180 million in nondefense funding. This funding prioritizes restoring military strength, accelerating modernization, and supporting personnel through pay raises. This bill moves in parallel with the National Defense Authorization Act ("NDAA"), signed in December 2025, which authorizes up to approximately $900.6 billion for national defense.

The federal government's cybersecurity and IT spending priorities for fiscal years 2025 and 2026 present both significant opportunities and notable risks for our suite of security solutions. The FY2026 NDAA authorizes approximately $15.1 billion for DoW cyber activities, representing a 4.1% increase. The FY2026 NDAA emphasizes securing the defense industrial base, accelerating artificial intelligence ("AI") integration, and harmonizing cybersecurity requirements. This increase directly aligns with our core offerings in cyber risk management (e.g., Xacta).

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Consolidated Results

Table MD&A 2: Consolidated Financial Results Comparison
For the Year Ended December 31,
2025 | 2024 | Dollar Change
(dollars in thousands)
Revenue | 164,805 | 108,272 | 56,533
Cost of sales | 103,788 | 73,843 | 29,945
Gross profit | 61,017 | 34,429 | 26,588
Gross margin | 37.0 | % | 31.8 | %
Operating expenses | 100,898 | 90,302 | 10,596
Operating expenses as percentage of revenue | 61.2 | % | 83.4 | %
Operating loss | (39,881) | (55,873) | 15,992
Other income | 3,225 | 4,023 | (798)
Interest expense | (553) | (644) | 91
Loss before income taxes | (37,209) | (52,494) | 15,285
Benefit from (provision for) income taxes | 663 | (26) | 689
Net loss | (36,546) | (52,520) | 15,974

Our business segments have different factors driving revenue fluctuations and profitability. A discussion of the changes in our net revenue and profitability is covered in greater detail under the section that follows: "Segment Results." We generate revenue from the delivery of products and services to our customers. Cost of sales, for both products and services, consists of labor, materials, subcontracting costs and an allocation of indirect costs.

Operating Expenses : Operating expenses increased by $10.6 million or 11.7% in 2025, compared to 2024. A goodwill impairment of $14.9 million was recorded in the fourth quarter of 2025 associated with our Secure Networks reporting unit (see Note 6 - Goodwill for more information), whereas an impairment loss on intangible assets of $6.4 million was recorded in 2024.

Research and development ("R&D") expenses decreased by $1.4 million, or 16.4% in 2025, compared to 2024. This was due to a $2.2 million reduction in amortization costs from the discontinued development of selected solutions or parts of solutions associated with the restructuring plan in 2024. This reduction was partially offset by an increase of $1.4 million in stock-based compensation. R&D restructuring expenses were approximately flat year-over-year. The remaining R&D expenses decreased by $0.6 million due to the restructuring effort in 2024 and ongoing disciplined cost management

Selling, general and administrative ("SG&A") expenses increased by $3.4 million, or 4.6%, in 2025, compared to 2024, due to a $7.6 million increase in stock-based compensation costs and $0.1 million increase in restructuring expenses. SG&A depreciation and amortization expenses were approximately flat year-over-year. These increases were partially offset by a $4.2 million reduction in the remaining SG&A expenses due to the 2024 restructuring effort and ongoing disciplined cost management.

Other income : Other income decreased by 19.8% in 2025, compared to 2024, primarily due to the change in dividend income from money market placements, partially offset by the gain on fair value adjustment of an investment and the one-time tax refund recorded in the fourth quarter of 2025.

Segment Results

The accounting policies of each business segment are the same as those followed by the Company as a whole. Management evaluates business segment performance based on gross profit.

Table MD&A 3: Security Solutions Segment - Financial Results Comparison
For the Year Ended December 31,
2025 | 2024 | Dollar Change
(dollars in thousands)
Revenues | 149,600 | 76,760 | 72,840
Cost of sales (excluding impairment loss, depreciation and amortization) | 83,868 | 37,352 | 46,516
Impairment loss on intangible assets | — | 5,333 | (5,333)
Depreciation and amortization | 8,173 | 6,396 | 1,777
Total cost of sales | 92,041 | 49,081 | 42,960
Gross profit | 57,559 | 27,679 | 29,880
Gross margin | 38.5 | % | 36.1 | %

Security Solutions segment revenue increased by 94.9% in 2025, compared to 2024, primarily due to the expansion of multiple large programs in Telos ID.

Security Solutions segment gross profit increased by 108.0% in 2025, compared to 2024, primarily due to higher segment revenue and higher segment gross margin.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-16_item1_business.md)

Item 1. Business

Overview

Telos Corporation is a Maryland corporation headquartered in Ashburn, Virginia. Telos Corporation, together with its subsidiaries (the "Company" or "Telos" or "We"), offers technology solutions and services that empower and protect the world's most security-conscious organizations.

We deliver efficient, adaptable, and secure solutions that protect people, organizations, and information across government and industry. From cyber governance, risk and compliance ("GRC") with Xacta ® , to identity and biometric solutions, secure networks, and TSA PreCheck ® enrollment, we help customers stay ahead of evolving threats. Our primary customers include the U.S. federal government, large commercial organizations and international customers. Our deep domain expertise, cleared workforce, and proven technologies give us a unique position at the intersection of cybersecurity, identity, and network security. Driven by purpose and guided by our core values, we build lasting partnerships, deliver superior solutions, and help create a more secure, interconnected world.

Our Business Segments

We conduct our business through two reportable and operating segments: Security Solutions and Secure Networks. These segments enable the alignment of our strategies and objectives and provide a framework for the timely and rational allocation of resources within the line of business.

Additional information regarding our segments is presented in Note 1 6 – Segment Information to the consolidated financial statements at Item 8 of this Annual Report on Form 10-K.

Security Solutions Segment:

The Security Solutions segment delivers cybersecurity, cloud, identity, and secure messaging solutions that help government and commercial customers protect critical systems, manage cyber risk, and operate securely in complex and regulated environments. This segment combines cyber GRC solutions, secure cloud services, identity and biometric technologies, and secure messaging platforms to support mission-critical requirements for government and commercial customers operating in highly regulated and security-sensitive environments.

Security Solutions represented 90.8% and 70.9% of total revenues for fiscal years 2025 and 2024, respectively.

The Security Solutions segment offers the following solutions and services:

• Xacta: Deployed at some of the world's most security-conscious organizations, Xacta is a cyber GRC automation platform designed to help its customers meet the complex challenges of managing cyber risk and security compliance by automating processes for assessment and authorization, remediation, and continuous monitoring.

Xacta is a premier platform delivering automated cyber risk management and continuous compliance processes for systems based in the cloud, on-premises, and in hybrid environments. It supports a wide-range of frameworks and regulatory content, including National Institute of Standards and Technology ("NIST") Risk Management Framework ("RMF"), the Cybersecurity Risk Management Construct for Department of War ("DoW") IT, the NIST Cybersecurity Framework, the Federal Risk and Authorization Management Program ("FedRAMP") and the DoW's Cybersecurity Maturity Model Certification ("CMMC") program, across all industries with no-code customization options for tailoring content to fit the organization's needs.

Recently, Telos launched Xacta.ai TM , the artificial intelligence ("AI") capability at the core of the Xacta cyber GRC platform, dramatically reducing compliance time and effort. Xacta.ai delivers expert-level guidance and real-time insights, empowering organizations to move from reactive compliance to proactive risk management.

• Cybersecurity Services: We offer solutions and services for the full cybersecurity lifecycle, including RMF consulting services, security assessment and compliance, engineering and evaluation, operations, penetration testing, and digital forensics. With a pedigree in cybersecurity and information assurance that spans three decades, our multi-certified cybersecurity personnel provide services and solutions that deliver continuous security assurance for business, government, and public sector critical infrastructure.

• Telos Automated Message Handling System ("Telos AMHS ™ "): Telos AMHS is a web-based organizational message distribution and management solution for mission-critical communications; the recognized gold standard for organizational messaging in the U.S. government. Telos AMHS is used by military field operatives for critical communications on the battlefield using the Defense Information System Agency's Organizational Messaging Service and its specialized communications protocols. Telos AMHS is also used by the Intelligence Community ("IC") for timely situational awareness and assessment reporting utilizing the Director of National Intelligence's Information Transport Service, Organizational Messaging data standards and computing infrastructure. Because Telos AMHS supports timely and reliable delivery for authoritative communications, its uses include terrorist warnings, "eyes-only" messages, military execution orders, intelligence information, overflight clearances, and Emergency Action Messages for nuclear command and control. Information exchanged at this level and for these purposes requires operational requirements for time-sensitive, guaranteed delivery, precedence, high availability, and reliability.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-16_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-16_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-16_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-10_2-02-results.md, 10-K_2026-03-16_item7_mdna.md, 10-K_2026-03-16_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
