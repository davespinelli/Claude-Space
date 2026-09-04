# Triage pack — SPOK · Spok Holdings, Inc

_Generated 2026-09-04 16:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SPOK · **Name:** Spok Holdings, Inc
- **CIK:** 0001289945
- **SIC:** 4812 — Radiotelephone Communications
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SPOK

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Spok Holdings, Inc
- **CIK:** 1,289,945 · **SIC:** 4812 (Radiotelephone Communications) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 10.68 |
| mktcap | $223.4M |
| ev | $206.8M |
| ev_ebit | 10.5x |
| fcf | $25.2M |
| fcf_yield | 11.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 12.6% |
| net_debt | -$16.6M |
| net_debt_ebit | -0.8x |
| cash | $16.6M |
| ltd | $0.00 |
| equity | $139.9M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $139.7M |
| revenue_prior | $137.7M |
| rev_growth | 1.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $19.7M |
| net_income | $15.9M |
| cfo | $28.9M |
| capex | $3.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 20,918,137 |
| shares_py | 20,590,924 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -32.5% |
| r6m | -6.3% |
| off_52w_high | -34.3% |
| adv20 | $1.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.75 |
| r_ev_ebit | 0.73 |
| r_roic | 0.76 |
| r_rev_growth | 0.40 |
| r_buyback | 0.37 |
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
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 141 |

**Screen rationale:** top-quartile FCF yield 11.3%; high ROIC 12.6%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **20,918,137** (CY2026Q2I) vs **20,590,924** prior year (CY2025Q2I)
- Change: **1.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-04-14** — Item 5.02 (officer / director change or comp arrangement): realignment designed to reduce costs, the Board of Directors of Spok Holdings, Inc. (the "Company") appointed Michael W. Wallace,

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 45,211 sh / $473,524 vs sells 28,320 sh / $319,810 -> net $153,715 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Stein Todd J bought 35,211 sh @ $10.41 ($366,705) on 2026-06-16.

Form 4 filings parsed: 12; transaction rows: 25 (open-market buys 5, sales 2).

| code | rows |
|---|---|
| A | 15 |
| P | 6 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'Spok Reports Second Quarter 2026 Results'; skipped 7 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (a2q26-ex991earningspressre.htm)

Spok Reports Second Quarter 2026 Results

Company Generates $4.1 Million of Net Income and $9.1 Million of Adjusted EBITDA

Software Operations Bookings Up Nearly 92% From the Prior Quarter

Executes Agreement to Sell Narrowband Licenses for $8 Million

Plano, Tx. (July 29, 2026) - Spok Holdings, Inc. (NASDAQ: SPOK), a global leader in healthcare communications, today announced results for the second quarter ended June 30, 2026. In addition, the Company's Board of Directors declared a regular quarterly dividend of $0.3125 per share, payable on September 9, 2026, to stockholders of record on August 19, 2026.

Recent Highlights:

• Adjusted EBITDA totaled $9.1 million in the second quarter of 2026, up 22.1% from the prior year period. Second-quarter net income of $4.1 million, which included $1.5 million of severance and restructuring charges related to the previously announced strategic realignment, was down from second quarter 2025 net income of $4.6 million, which included a $0.7 million gain on the sale of one of its domain names

• Second-quarter software operations bookings totaled $9.5 million and included 14 six-figure customer contracts and 1 seven-figure customer contract

• Software revenue in the second quarter was up more than 3% from the prior year period, driven by a nearly 52% year-over-year growth in license revenue and a 53% year-over-year increase in managed services revenue

• Software backlog totaled $57.1 million at June 30, 2026, as the Company continues to focus on multi-year and managed services bookings

• Second quarter 2026 wireless average revenue per unit (ARPU) was $8.20, consistent with the prior year period

• Wireless units in service declined by 1.8% in the second quarter, an 84-basis point improvement from the first quarter decline and consistent with prior year levels

• Capital returned to stockholders in the second quarter of 2026 totaled $6.5 million

• Research and development costs totaled $3.3 million in the second quarter of 2026 , supporting Spok's incorporation of Artificial Intelligence and further enhancements in the Company's industry-leading solutions

Spok.com

Exhibit 99.1
NEWS RELEASE

• Cash and cash equivalents balance of $16.6 million at June 30, 2026, and no debt

• Spok executed an agreement to sell certain narrowband spectrum licenses in its two-way paging inventory for $8 million in cash which subsequently closed on July 20, 2026

"Our focus continues to be on generating cash flow and returning capital to stockholders, while responsibly investing for future growth," said Vincent D. Kelly, chief executive officer of Spok Holdings, Inc. "In the second quarter, we were able to deliver a nearly 92% increase in software operations bookings compared to the first quarter, a more than 3% year-over-year increase in software revenue, and an 84-basis point improvement in wireless unit attrition from the first quarter, as well as stable year-over-year wireless average revenue per unit. Additionally, we generated adjusted EBITDA totaling $9.1 million, a nearly 74% increase from the first quarter and a more than 22% increase from the prior year period.

"As part of the strategic realignment that we outlined last quarter, we completed the sale of certain of our narrowband spectrum licenses as we continue to find efficiencies within our organization and monetize our valuable asset base. We are confident that actions such as this will continue to create significant value for stockholders, while supporting both our investment in our Care Connect® Suite and our quarterly dividend, which currently represents a yield in excess of 10% for our stockholders. Additionally, Spok is actively implementing artificial intelligence to drive further operational efficiencies across the organization, with a particular focus on accelerating product development timelines, reducing time to market for new Care Connect Suite capabilities and other internal uses.

"Based on the anticipated full-year financial impact of the strategic realignment, first half software operations bookings levels and our visibility into our product sales pipeline, we are adjusting our full year 2026 financial guidance estimates for revenue, while maintaining the midpoint of our guidance for adjusted EBITDA. We now expect the midpoint for total revenue to be $136 million, while the midpoint for adjusted EBITDA remains at $30 million. The detail for this guidance is contained in the table attached to our press release," concluded Kelly.

Spok.com

Exhibit 99.1
NEWS RELEASE

Financial Highlights :

For the three months ended June 30, | For the six months ended June 30,
(Dollars in thousands) | 2026 | 2025 | Change (%) | 2026 | 2025 | Change (%)
Revenue
Wireless revenue
Paging revenue | 16,011 | 17,192 | (6.9) | % | 32,580 | 34,799 | (6.4) | %
Product and other revenue | 1,202 | 1,248 | (3.7) | % | 2,119 | 2,115 | 0.2 | %
Total wireless revenue | 17,213 | 18,440 | (6.7) | % | 34,699 | 36,914 | (6.0) | %
Software revenue
License | 3,632 | 2,394 | 51.7 | % | 4,994 | 5,025 | (0.6) | %
Professional services - projects | 2,768 | 3,831 | (27.7) | % | 6,096 | 8,302 | (26.6) | %
Professional services - managed services | 2,332 | 1,520 | 53.4 | % | 4,391 | 2,835 | 54.9 | %
Hardware | 128 | 376 | (66.0) | % | 314 | 697 | (54.9) | %
Maintenance and subscription | 8,938 | 9,125 | (2.0) | % | 17,743 | 18,207 | (2.5) | %
Total software revenue | 17,798 | 17,246 | 3.2 | % | 33,538 | 35,066 | (4.4) | %
Total revenue | 35,011 | 35,686 | (1.9) | % | 68,237 | 71,980 | (5.2) | %

For the three months ended June 30, | For the six months ended June 30,
(Dollars in thousands) | 2026 | 2025 | Change (%) | 2026 | 2025 | Change (%)
GAAP
Operating expenses | 29,586 | 30,294 | (2.3) | % | 60,368 | 60,570 | (0.3) | %
Net income | 4,120 | 4,552 | (9.5) | % | 6,107 | 9,748 | (37.4) | %
Cash and cash equivalents (as of period end) | 16,592 | 20,242 | (18.0) | % | 16,592 | 20,242 | (18.0) | %
Capital returned to stockholders | 6,536 | 6,477 | 0.9 | % | 14,494 | 14,424 | 0.5 | %
Non-GAAP
Adjusted operating expenses | 27,112 | 29,420 | (7.8) | % | 56,580 | 58,780 | (3.7) | %
Adjusted EBITDA | 9,143 | 7,489 | 22.1 | % | 14,400 | 15,693 | (8.2) | %

Spok.com

Exhibit 99.1
NEWS RELEASE

For the three months ended June 30, | For the six months ended June 30,
(Dollars in thousands, excluding units in service and ARPU) | 2026 | 2025 | Change (%) | 2026 | 2025 | Change (%)
Key Statistics
Wireless units in service (000's) (as of period end) | 645 | 694 | (7.1) | % | 645 | 694 | (7.1) | %
Wireless average revenue per unit (ARPU) | 8.20 | 8.20 | — | % | 8.23 | 8.21 | 0.2 | %
Software operations bookings (1) | 9,467 | 11,661 | (18.8) | % | 14,406 | 19,998 | (28.0) | %
Software backlog (as of period end) (2) | 57,108 | 65,187 | (12.4) | % | 57,108 | 65,187 | (12.4) | %

(1) Software operations bookings includes net new (i.e., new customers or incremental add-on sales to existing customers) sales of license, professional services, equipment, and first-year maintenance.

(2) Software backlog excludes $17.0 million and $10.1 million of contractual obligations that are deemed cancellable by the customer without significant penalty as of June 30, 2026 and 2025, respectively.

Financial Outlook:

The Company is updating its prior financial guidance and now expects the following for the full year 2026:

(Unaudited and in millions) | Current Guidance Full Year 2026 | Prior Guidance Full Year 2026
From | To | From | To
Revenue
Wireless | 67.0 | 70.0 | 68.0 | 71.0
Software | 65.5 | 69.5 | 68.0 | 72.0
Total Revenue | 132.5 | 139.5 | 136.0 | 143.0
Adjusted EBITDA | 28.0 | 32.0 | 27.5 | 32.5

2026 Second Quarter Call:

Management will host a conference call and webcast to discuss these financial results on Wednesday, July 29, 2026, at 5:00 p.m. Eastern Time. The presentation is open to all interested parties and may include forward-looking information.

Conference Call Details
Date/Time: | Wednesday, July 29, 2026, at 5:00 p.m. ET
Webcast: | https://www.webcast-eqs.com/registration/Spok_Q2_2026
U.S. Toll-Free Dial In: | 877-407-0890
International Dial In: | 1-201-389-0918

Spok.com

Exhibit 99.1
NEWS RELEASE

To access the call, please dial in approximately ten minutes before the start of the call. For those unable to join the live call, an OnDemand version of the webcast will be available following the call under the URL link and on the investor relations website.

* * * * * * * * *

About Spok

Spok Holdings, Inc. (NASDAQ: SPOK), headquartered in Plano, Texas, is proud to be a global leader in healthcare communications. We deliver clinical information to care teams when and where it matters most to improve patient outcomes. Top hospitals rely on the Spok Care Connect® platform to enhance workflows for clinicians and support administrative compliance. Our customers send approximately 70 million messages each month through their Spok® solutions. Spok enables smarter, faster clinical communication. For more information, visit spok.com .

Spok is a trademark of Spok Holdings, Inc. Spok Care Connect and Spok Mobile are trademarks of Spok, Inc.

Non-GAAP Financial Measures

This press release contains the following non-GAAP financial measures: adjusted operating expenses and adjusted EBITDA. Adjusted operating expenses excludes depreciation and accretion expense, impairment of intangible assets and severance and restructuring costs. Adjusted EBITDA represents net income/(loss) before interest income/expense, income tax benefit/expense, depreciation and accretion expense, stock-based compensation expense, impairment of intangible assets, legal costs unrelated to core business activities and non-recurring in nature, and severance and restructuring. With respect to our expectations under "Financial Outlook" above, reconciliation of adjusted EBITDA to net income is not available without unreasonable efforts on a forward-looking basis due to the high variability, complexity and uncertainty with respect to certain items included in net income that are excluded from adjusted EBITDA, in particular, income tax benefit/expense, stock-based compensation expenses, impairment of intangible assets, severance and restructuring and other non-recurring expenses. These items can have unpredictable fluctuations based on unforeseen activity that is out of our control and/or cannot be reasonably predicted.

We believe that these non-GAAP financial measures provide useful information to management and investors regarding certain financial and business trends relating to Spok's financial condition and results of operations. We use these non-GAAP measures for financial, operational, and budgetary decision-making purposes, to understand and evaluate our core operating performance and trends, and to generate future operating plans. We believe that these non-GAAP financial measures permit

Spok.com

Exhibit 99.1
NEWS RELEASE

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview and Highlights

We offer a focused suite of unified clinical communication and collaboration solutions that include call center applications, clinical alerting and notifications, one-way and advanced two-way wireless messaging services, mobile communications and public safety solutions. Our customers rely on Spok for workflow improvement, secure texting, paging services, contact center optimization and public safety response. Our product offerings are capable of addressing a customer's clinical communications needs. We develop, sell and support enterprise-wide systems for healthcare and other organizations needing to automate, centralize and standardize their approach to clinical communications. While our primary market has been the healthcare industry with a focus on prominent hospitals, our solutions can be found in prominent hospitals, large government agencies, leading public safety institutions, colleges and universities, large hotels, resorts and casinos and well-known manufacturers.

Revenue generated by wireless messaging services (including voice mail, personalized greetings, message storage and retrieval, equipment, maintenance plans and/or equipment loss protection to both one-way and two-way messaging subscribers) is presented as wireless revenue in our Consolidated Statements of Operations. Revenue generated by the sale of our software solutions, which includes revenue from our perpetual and term software license arrangements, revenue from the sale of hardware that facilitates the use of our software solutions, professional services revenue related to the implementation of our solutions and value-added services, and maintenance and subscription revenue that is generated from the ongoing support of our perpetual and term software license arrangements, is presented as software revenue in our Consolidated Statements of Operations. Our software is licensed to end users under an industry standard software license agreement.

Results of Operations

The following table is a summary of our Consolidated Statements of Operations for the years ended December 31, 2025, 2024 and 2023, and the discussion that follows compares the year ended December 31, 2025 to the year ended December 31, 2024. For a discussion and analysis of the year ended December 31, 2024, compared to the year ended December 31, 2023, please refer to Management's Discussion and Analysis of Financial Condition and Results of Operations included in Part II, Item 7 of our Annual Report on Form 10-K for the year ended December 31, 2024, filed with the SEC on February 27, 2025:

(Dollars in thousands) | 2025 | Change | 2024 | Change | 2023
Revenue:
Wireless revenue | 72,522 | (1,001) | (1.4) | % | 73,523 | (2,445) | (3.2) | % | 75,968
Software revenue | 67,186 | 3,056 | 4.8 | % | 64,130 | 1,073 | 1.7 | % | 63,057
Total revenue | 139,708 | 2,055 | 1.5 | % | 137,653 | (1,372) | (1.0) | % | 139,025
Operating expenses:
Cost of revenue (exclusive of items shown separately below) | 29,785 | 1,078 | 3.8 | % | 28,707 | 1,613 | 6.0 | % | 27,094
Research and development | 12,216 | 522 | 4.5 | % | 11,694 | 1,010 | 9.5 | % | 10,684
Technology operations | 24,603 | (1,032) | (4.0) | % | 25,635 | (1,510) | (5.6) | % | 27,145
Selling and marketing | 17,703 | 1,483 | 9.1 | % | 16,220 | (526) | (3.1) | % | 16,746
General and administrative | 31,804 | 624 | 2.0 | % | 31,180 | 121 | 0.4 | % | 31,059
Severance and restructuring | 458 | (646) | (58.5) | % | 1,104 | 531 | 92.7 | % | 573
Depreciation and accretion | 3,429 | (719) | (17.3) | % | 4,148 | (348) | (7.7) | % | 4,496
Total operating expenses | 119,998 | 1,310 | 1.1 | % | 118,688 | 891 | 0.8 | % | 117,797
Operating income | 19,710 | 745 | 3.9 | % | 18,965 | (2,263) | (10.7) | % | 21,228
Interest income | 820 | (333) | (28.9) | % | 1,153 | 54 | 4.9 | % | 1,099
Other income (expense) | 912 | 998 | (1,160.5) | % | (86) | (84) | 4,200.0 | % | (2)
Income before income taxes | 21,442 | 1,410 | 7.0 | % | 20,032 | (2,293) | (10.3) | % | 22,325
Provision for income taxes | (5,561) | (494) | 9.7 | % | (5,067) | 1,592 | (23.9) | % | (6,659)
Net income | 15,881 | 916 | 6.1 | % | 14,965 | (701) | (4.5) | % | 15,666
Supplemental Information
FTEs | 421 | 11 | 2.7 | % | 410 | 26 | 6.8 | % | 384
Active transmitters | 2,869 | (179) | (5.9) | % | 3,048 | (167) | (5.2) | % | 3,215

Certain amounts in the Consolidated Financial Statements, for the years ended December 31, 2024 and 2023, have been reclassified to conform to the current presentation for the year ended December 31, 2025. Management concluded that presenting certain information technology ("IT") expenses within their respective functional expense categories provides a more meaningful and representative depiction of the nature of these costs. Accordingly, we reclassified these IT-related

expenses from general and administrative to the applicable functional categories for all periods presented. These reclassifications had no effect on the reported results of operations or the statement of financial position.

To conform with the current year presentation, we reclassified previously reported operating expenses for the years ended December 31, 2024 and 2023 as follows:

For the Year Ended December 31, 2024
(Dollars in thousands) | As Previously Reported | Adjustment | As Reclassified
Cost of revenue | 28,430 | 277 | 28,707
Research and development | 11,548 | 146 | 11,694
Technology operations | 24,306 | 1,329 | 25,635
Selling and marketing | 15,851 | 369 | 16,220
General and administrative | 33,301 | (2,121) | 31,180
Total operating expenses | 113,436 | — | 113,436
For the Year Ended December 31, 2023
(Dollars in thousands) | As Previously Reported | Adjustment | As Reclassified
Cost of revenue | 26,818 | 276 | 27,094
Research and development | 10,549 | 135 | 10,684
Technology operations | 25,843 | 1,302 | 27,145
Selling and marketing | 16,350 | 396 | 16,746
General and administrative | 33,168 | (2,109) | 31,059
Total operating expenses | 112,728 | — | 112,728

Revenue

We offer a focused suite of unified clinical communications and collaboration solutions that include call center applications, clinical alerting and notifications, one-way and advanced two-way wireless messaging services, mobile communications and public safety solutions.

We develop, sell and support enterprise-wide systems for healthcare, government, and large enterprise and other organizations needing to automate, centralize and standardize their approach to clinical communications and collaboration. Our solutions can be found in prominent hospitals, large government agencies, leading public safety institutions, colleges and universities, large hotels, resorts and casinos and well-known manufacturers. Our primary market is the healthcare industry, particularly hospitals. While we have historically identified hospitals with 200 or more beds as the primary targets for our software solutions, as well as our paging services, we have recently expanded our focus to include smaller hospitals with shorter sales cycles, including academic medical centers.

Revenue generated by wireless messaging services (including voice mail, personalized greetings, message storage and retrieval, equipment, maintenance plans and/or equipment loss protection to both one-way and two-way messaging subscribers) is presented as wireless revenue in our Consolidated Statements of Operations. Revenue generated by the sale of our software solutions, which includes revenue from our perpetual and term software license arrangements, revenue from the sale of hardware that facilitates the use of our software solutions, professional services revenue related to the implementation of our solutions and value-added services, and maintenance and subscription revenue that is generated from the ongoing support of our perpetual and term software license arrangements, is presented as software revenue in our Consolidated Statements of Operations. Our software is licensed to end users under an industry standard software license agreement.

Refer to Note 3, "Revenue, Deferred Revenue and Prepaid Commissions," in the Notes to Consolidated Financial Statements for additional information on our wireless and software revenue streams.

The table below details total revenue for the periods stated:

(Dollars in thousands) | 2025 | Change | 2024 | Change | 2023
Wireless revenue:
Paging revenue | 68,559 | (2,399) | (3.4) | % | 70,958 | (2,177) | (3.0) | % | 73,135
Product and other revenue | 3,963 | 1,398 | 54.5 | % | 2,565 | (268) | (9.5) | % | 2,833
Wireless revenue | 72,522 | (1,001) | (1.4) | % | 73,523 | (2,445) | (3.2) | % | 75,968
Software revenue:
License | 7,347 | (301) | (3.9) | % | 7,648 | (1,073) | (12.3) | % | 8,721
Professional services - projects | 15,496 | 880 | 6.0 | % | 14,616 | 1,311 | 9.9 | % | 13,305
Professional services - managed services | 6,623 | 3,364 | 103.2 | % | 3,259 | 1,870 | 134.6 | % | 1,389
Hardware | 1,287 | (95) | (6.9) | % | 1,382 | (1,293) | (48.3) | % | 2,675
Maintenance and subscription | 36,433 | (792) | (2.1) | % | 37,225 | 258 | 0.7 | % | 36,967
Software revenue | 67,186 | 3,056 | 4.8 | % | 64,130 | 1,073 | 1.7 | % | 63,057
Total revenue | 139,708 | 2,055 | 1.5 | % | 137,653 | (1,372) | (1.0) | % | 139,025

Wireless Revenue

Wireless revenue consists of two primary components: paging revenue and product and other revenue. Paging revenue consists primarily of recurring fees associated with the provision of messaging services and fees for paging devices and is net of a provision for service credits. Product and other revenue reflects system sales, sales of paging devices and charges for devices that are not returned and are net of anticipated credits. See "Item 1. Business" for more details.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

ITEM 1. BUSINESS

Overview

Spok, Inc., a wholly owned subsidiary of Spok Holdings, Inc. (NASDAQ: SPOK), is proud to be a global leader in healthcare communications. We deliver clinical information to care teams when and where it matters most to improve patient outcomes. Top hospitals rely on Spok products and services to enhance workflows for clinicians, support administrative compliance, and provide a better experience for patients.

Our headquarters is located at 3000 Technology Drive, Suite 400 , Plano, Texas 75074, and our telephone number is 800-611-8488. We maintain a website at http://www.spok.com . This website address is for information only and is not intended to be an active link or to incorporate any website information into this Annual Report on Form 10-K for the year ended December 31, 2025 (the "2025 Form 10-K").

We deliver smart, reliable clinical communication and collaboration solutions to help protect the health, well-being, and safety of people in the United States and abroad, on a limited basis, in Europe, Canada, Australia, Asia and the Middle East. Our customers rely on Spok for workflow improvement, secure texting, paging services, contact center optimization, and public safety response. We develop, sell, and support enterprise-wide systems primarily for healthcare and other organizations needing to automate, centralize, and standardize their approach to clinical and critical communications. Our solutions can be found in prominent hospitals, large government agencies, leading public safety institutions, colleges and universities, large hotels, resorts and casinos and well-known manufacturers. We offer our services and products to three major market segments: healthcare, government, and large enterprise, with a greater emphasis on the healthcare market segment.

Industry Overview

The United States healthcare market continues to experience significant change. Healthcare costs continue to rise, reimbursements from Centers for Medicare and Medicaid Services are being reduced in certain areas, digitization of healthcare information continues, and the industry continues to shift towards a value-based purchasing model and away from the traditional fee-for-service model. The value-based purchasing model places an emphasis on incentivizing value and quality at an individual patient level in order to provide better patient outcomes and reduce 30-day readmissions.

In response, healthcare providers now require greater communication and better collaboration between clinicians in order to generate improvements in the quality, safety, satisfaction and efficiency of patient care delivery. Improvements in these areas are necessary for healthcare providers to successfully navigate many of these issues. Many providers are seeking improvement through the adoption of technology, looking to take advantage of workflow automation, process improvement and, in limited circumstances, machine learning and artificial intelligence. Providers also look to increase efficiencies through consolidation as larger health systems continue to acquire smaller hospitals for the primary purpose of gaining regional market share amongst tough competition.

We believe these changes and continued pressure for organizations to provide improved services with fewer resources place an even greater emphasis on the need for improved clinical communication and collaboration tools to meet the increasing requirements demanded by the healthcare industry in today's marketplace. Our solutions help hospitals significantly increase the quality and safety of patient care delivery, while increasing patient and provider satisfaction and simultaneously increasing employee productivity, reducing costs and clinician burnout. This is accomplished through workflow enhancement; secure, reliable and integrated communication tools; and mobile accessibility.

Sales and Marketing

We offer a focused suite of unified clinical communication and collaboration solutions primarily to organizations in the healthcare sector. We generate wireless revenue from the sales of wireless messaging services, equipment, maintenance plans and/or equipment loss protection to both one-way and two-way messaging subscribers. We generate software revenue from the sale of our software solutions, including software licenses, professional services, equipment we procure from third parties, and post-contract support.

Sales

We market and distribute our clinical communication and collaboration solutions through a direct sales force and an indirect sales channel.

The direct sales force contracts or sells products, solutions, messaging services and other services directly to customers ranging from small and medium-sized businesses to companies in the Fortune 1000, as well as federal, state, and local government agencies. We will continue to market primarily to commercial enterprises, with a focus on healthcare organizations, interested in our communication solutions. We maintain a sales presence in key markets throughout the United States, and in limited markets internationally through strategic partnerships, in an effort to gain new customers and to retain and increase sales to existing customers. The direct sales force targets leadership responsible for the procurement of clinical communication and collaboration solutions such as chief information officers, chief technology officers, chief medical officers, chief nursing officers, information technology directors, telecommunications directors, laboratory directors, radiology directors and contact center managers. The timing for a direct sale varies but may take from six to 18 months depending on the type and scope of software solution.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
