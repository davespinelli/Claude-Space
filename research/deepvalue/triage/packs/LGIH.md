# Triage pack — LGIH · LGI Homes, Inc.

_Generated 2026-09-05 01:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** LGIH · **Name:** LGI Homes, Inc.
- **CIK:** 0001580670
- **SIC:** 1531 — Operative Builders
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/LGIH

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** LGI Homes, Inc.
- **CIK:** 1,580,670 · **SIC:** 1531 (Operative Builders) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 54.47 |
| mktcap | $1.3B |
| ev | $2.9B |
| ev_ebit | 35.9x |
| fcf | -$140.9M |
| fcf_yield | -11.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $1.6B |
| net_debt_ebit | 20.0x |
| cash | $61.1M |
| ltd | $1.7B |
| equity | n/a |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.7B |
| revenue_prior | $2.2B |
| rev_growth | -22.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $79.8M |
| net_income | $72.6M |
| cfo | -$140.0M |
| capex | $924k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 23,248,272 |
| shares_py | 23,056,635 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -1.8% |
| r6m | 16.3% |
| off_52w_high | -18.7% |
| adv20 | $15.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.08 |
| r_ev_ebit | 0.22 |
| r_roic | 0.50 |
| r_rev_growth | 0.03 |
| r_buyback | 0.50 |
| score | 0.27 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 433 |

**Screen rationale:** balanced across factors, no single standout


## 3. Share count trend

- Shares outstanding: **23,248,272** (CY2026Q2I) vs **23,056,635** prior year (CY2025Q2I)
- Change: **0.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 62,349 sh / $2,619,473 -> net $-2,619,473 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 11; transaction rows: 29 (open-market buys 0, sales 18).

| code | rows |
|---|---|
| A | 10 |
| G | 1 |
| S | 18 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'LGI Homes, Inc. Reports Strong Second Quarter 2026 Results and Increas'; skipped 19 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (a06302026ex991earningsrele.htm)

LGI Homes, Inc. Reports Strong Second Quarter 2026 Results and Increases Full-Year 2026 Average Sales Price and Homebuilding Gross Margin Guidance Ranges

THE WOODLANDS, Texas, August 4, 2026 (GLOBE NEWSWIRE) - LGI Homes, Inc. (NASDAQ: LGIH) today announced financial results for the second quarter and the six months ended June 30, 2026.

"We delivered strong results during the second quarter, exceeding expectations across key metrics while navigating a dynamic operating environment," said Eric Lipar, Chairman and Chief Executive Officer of LGI Homes.

"During the quarter, we delivered 1,440 homes, an 8.8% increase year-over-year, generating total revenues of $516.0 million and homebuilding revenues of $501.5 million.

"We ended the quarter with 151 active communities, achieving the low end of our full-year guidance just six months into the year, and representing an increase of 3.4% compared to the same time last year.

"Homebuilding gross margin of 19.8% and adjusted homebuilding gross margin of 23.2% both exceeded the midpoint of our previously increased guidance range, reflecting our disciplined approach to pricing, incentives, and inventory management and the continued benefits of our self-development platform.

"We made significant progress strengthening our balance sheet during the quarter, reducing debt by $128.6 million and ending the period with a debt-to-capital ratio of 42.6%, a 220 basis point improvement year-over-year.

"On the strength of our outperformance in the first half of the year, we are raising our full-year gross margin guidance for the second consecutive quarter. We now expect our homebuilding gross margin will range between 19.0% and 21.0% and adjusted homebuilding gross margin between 22.5% and 24.5%. We are also raising the guidance for our full-year average sales price per home closed to between $360,000 and $370,000."

Mr. Lipar concluded, "With strong visibility into the second half of the year, we are confident in achieving all of our objectives for 2026 and remain focused on balancing sales pace, profitability, and inventory management as we create long-term value for our shareholders."

Second Quarter 2026 Highlights

• Homebuilding revenues of $501.5 million, an increase of 3.7%

• Total home closings of 1,440, including 75 currently and previously leased homes, an increase of 8.8%

• Home closings of 1,365, an increase of 3.2%

• Average sales price per home closed of $367,407, an increase of 0.5%

• Homebuilding gross margin as a percentage of homebuilding revenues of 19.8%

• Adjusted homebuilding gross margin* as a percentage of homebuilding revenues of 23.2%

• Net income before income taxes of $36.6 million

• Net income of $27.0 million or $1.16 basic EPS and $1.16 diluted EPS

Six Months Ended June 30, 2026 Highlights

• Homebuilding revenues of $821.2 million, a decrease of 1.6%

• Total home closings of 2,356, including 110 currently and previously leased homes, an increase of 1.6%

• Home closings of 2,246, a decrease of 3.1%

• Average sales price per home closed of $365,649, an increase of 1.6%

• Homebuilding gross margin as a percentage of homebuilding revenues of 19.4%

• Homebuilding gross margin excluding inventory impairment* as a percentage of homebuilding revenues of 20.0%

• Adjusted homebuilding gross margin* as a percentage of homebuilding revenues of 23.3%

• Net income before income taxes of $40.9 million

• Net income of $29.1 million or $1.26 basic EPS and $1.25 diluted EPS

• Adjusted net income* of $32.6 million, or $1.41 adjusted basic EPS* and $1.40 adjusted diluted EPS*

*Please see " Non-GAAP Measures " for a reconciliation of Homebuilding Gross Margin Excluding Inventory Impairment (a non-GAAP measure) and Adjusted Homebuilding Gross Margin (a non-GAAP measure) to Homebuilding Gross Margin, and Adjusted Net Income (a non-GAAP measure) to Net Income, the most directly comparable GAAP measures, and for calculations of adjusted basic EPS and adjusted diluted EPS.

Balance Sheet Highlights

• Total liquidity of $468.0 million at June 30, 2026, including cash and cash equivalents of $61.1 million and $406.9 million of availability under the Company's revolving credit facility

• Net debt to capital ratio* of 41.6% at June 30, 2026

*Please see " Non-GAAP Measures " for a reconciliation of net debt to capital ratio (a non-GAAP measure) to debt to capital ratio, the most directly comparable GAAP measure.

Full Year 2026 Outlook

Headquartered in The Woodlands, Texas, LGI Homes, Inc. is a pioneer in the homebuilding industry, successfully applying an innovative and systematic approach to the design, construction and sale of homes across 36 markets in 21 states. LGI Homes has closed over 80,000 homes since its founding in 2003 and has delivered profitable financial results every year. Nationally recognized for its quality construction and exceptional customer service, LGI Homes was named to Newsweek's list of the World's Most Trustworthy Companies. LGI Homes' commitment to excellence extends to its employees, earning the Company numerous workplace awards at the local, state, and national level, including the Top Workplaces USA 2026 Award. For more information about LGI Homes and its unique operating model focused on making the dream of homeownership a reality for families across the nation, please visit the Company's website at www.lgihomes.com.

June 30, | December 31,
2026 | 2025
ASSETS
Cash and cash equivalents | 61,081 | 61,247
Accounts receivable | 33,850 | 32,467
Real estate inventory | 3,512,613 | 3,555,602
Pre-acquisition costs and deposits | 19,248 | 28,950
Property and equipment, net | 149,579 | 107,145
Other assets | 119,812 | 119,909
Deferred tax assets, net | 10,392 | 9,904
Goodwill | 12,018 | 12,018
Total assets | 3,918,593 | 3,927,242
LIABILITIES AND EQUITY
Accounts payable | 58,750 | 16,179
Accrued expenses and other liabilities | 146,280 | 157,971
Notes payable, net | 1,580,907 | 1,656,803
Total liabilities | 1,785,937 | 1,830,953
COMMITMENTS AND CONTINGENCIES
EQUITY
Common stock, par value $0.01, 250,000,000 shares authorized, 27,904,864 shares issued and 23,248,272 shares outstanding as of June 30, 2026 and 27,789,678 shares issued and 23,133,086 shares outstanding as of December 31, 2025 | 279 | 277
Additional paid-in capital | 354,476 | 347,308
Retained earnings | 2,187,483 | 2,158,339
Treasury stock, at cost, 4,656,592 shares as of June 30, 2026 and December 31, 2025 | (409,582) | (409,635)
Total equity | 2,132,656 | 2,096,289
Total liabilities and equity | 3,918,593 | 3,927,242

LGI HOMES, INC.

CONSOLIDATED STATEMENTS OF OPERATIONS

(Unaudited)

(In thousands, except share and per share data)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenues
Homebuilding revenues | 501,511 | 483,485 | 821,247 | 834,905
Land and other revenues | 14,537 | 4,757 | 27,677 | 36,725
Total revenues | 516,048 | 488,242 | 848,924 | 871,630
Cost of sales
Homebuilding costs | 402,117 | 372,877 | 661,924 | 650,584
Land and other costs | 12,235 | 5,725 | 24,175 | 32,729
Total cost of sales | 414,352 | 378,602 | 686,099 | 683,313
Selling expenses | 44,149 | 41,599 | 76,799 | 83,941
General and administrative | 28,571 | 29,401 | 56,432 | 60,603
Other income, net | (7,615) | (3,400) | (11,316) | (3,991)
Net income before income taxes | 36,591 | 42,040 | 40,910 | 47,764
Income tax provision | 9,607 | 10,507 | 11,766 | 12,237
Net income | 26,984 | 31,533 | 29,144 | 35,527
Earnings per share:
Basic | 1.16 | 1.36 | 1.26 | 1.52
Diluted | 1.16 | 1.36 | 1.25 | 1.52
Weighted average shares outstanding:
Basic | 23,201,571 | 23,221,565 | 23,191,411 | 23,308,534
Diluted | 23,279,553 | 23,265,062 | 23,248,046 | 23,364,957

Homebuilding Revenues, Home Closings, Average Sales Price Per Home Closed (ASP), Average Community Count, Average Monthly Absorption Rate, and Ending Community Count by Reportable Segment

(Revenues in thousands, unaudited)

Three Months Ended June 30, 2026 | As of June 30, 2026
Reportable Segment | Homebuilding Revenues | Home Closings | ASP | Average Community Count | Average Monthly Absorption Rate | Community Count at End of Period
Central | 127,777 | 419 | 304,957 | 50.0 | 2.8 | 50
Southeast | 108,145 | 323 | 334,814 | 29.7 | 3.6 | 30
Northwest | 59,605 | 121 | 492,603 | 17.0 | 2.4 | 17
West | 134,609 | 299 | 450,197 | 28.7 | 3.5 | 29
Florida | 71,375 | 203 | 351,601 | 24.3 | 2.8 | 25
Total | 501,511 | 1,365 | 367,407 | 149.7 | 3.0 | 151

Three Months Ended June 30, 2025 | As of June 30, 2025
Reportable Segment | Homebuilding Revenues | Home Closings | ASP | Average Community Count | Average Monthly Absorption Rate | Community Count at End of Period
Central | 112,986 | 360 | 313,850 | 47.3 | 2.5 | 46
Southeast | 150,110 | 456 | 329,189 | 33.7 | 4.5 | 35
Northwest | 53,487 | 100 | 534,870 | 16.0 | 2.1 | 16
West | 100,339 | 230 | 436,257 | 24.7 | 3.1 | 25
Florida | 66,563 | 177 | 376,062 | 24.3 | 2.4 | 24
Total | 483,485 | 1,323 | 365,446 | 146.0 | 3.0 | 146

Homebuilding Revenues, Home Closings, Average Sales Price Per Home Closed (ASP), Average Community Count, and Average Monthly Absorption Rate by Reportable Segment

(Revenues in thousands, unaudited)

Six Months Ended June 30, 2026 | As of June 30, 2026
Reportable Segment | Homebuilding Revenues | Home Closings | ASP | Average Community Count | Average Monthly Absorption Rate | Community Count at End of Period
Central | 216,937 | 715 | 303,408 | 48.5 | 2.5 | 50
Southeast | 180,468 | 542 | 332,967 | 29.7 | 3.0 | 30
Northwest | 96,611 | 187 | 516,636 | 15.7 | 2.0 | 17
West | 210,459 | 471 | 446,834 | 27.7 | 2.8 | 29
Florida | 116,772 | 331 | 352,785 | 23.6 | 2.3 | 25
Total | 821,247 | 2,246 | 365,649 | 145.2 | 2.6 | 151

Six Months Ended June 30, 2025 | As of June 30, 2025
Reportable Segment | Homebuilding Revenues | Home Closings | ASP | Average Community Count | Average Monthly Absorption Rate | Community Count at End of Period
Central | 214,132 | 690 | 310,336 | 49.2 | 2.3 | 46
Southeast | 251,792 | 768 | 327,854 | 31.5 | 4.1 | 35
Northwest | 87,724 | 165 | 531,661 | 16.3 | 1.7 | 16
West | 167,295 | 389 | 430,064 | 25.2 | 2.6 | 25
Florida | 113,962 | 307 | 371,212 | 24.8 | 2.1 | 24
Total | 834,905 | 2,319 | 360,028 | 147.0 | 2.6 | 146

Owned and Controlled Lots

The table below shows (i) home closings by reportable segment for the six months ended June 30, 2026 and (ii) the Company's owned or controlled lots by reportable segment as of June 30, 2026.

Six Months Ended June 30, 2026 | As of June 30, 2026
Reportable Segment | Home Closings | Owned (1) | Controlled | Total
Central | 715 | 18,272 | 256 | 18,528
Southeast | 542 | 12,868 | 1,212 | 14,080
Northwest | 187 | 5,795 | 1,142 | 6,937
West | 471 | 8,621 | 3,145 | 11,766
Florida | 331 | 4,966 | 1,129 | 6,095
Total | 2,246 | 50,522 | 6,884 | 57,406

(1) Of the 50,522 owned lots as of June 30, 2026, 33,775 were raw/under development lots and 16,747 were finished lots. Finished lots included 1,858 completed homes, including information centers, and 1,899 homes in progress.

Backlog Data

As of the dates set forth below, the Company's net orders, cancellation rate and ending backlog homes and value were as follows (dollars in thousands, unaudited):

Six Months Ended June 30,
Backlog Data | 2026 (4) | 2025 (5)
Net orders (1) | 2,260 | 2,528
Cancellation rate (2) | 47.4 | % | 24.2 | %
Ending backlog – homes (3) | 1,298 | 808
Ending backlog – value (3) | 525,549 | 322,466

(1) Net orders are new (gross) orders for the purchase of homes during the period, less cancellations of existing purchase contracts during the period.

(2) Cancellation rate for a period is the total number of purchase contracts cancelled during the period divided by the total new (gross) orders for the purchase of homes during the period.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-20_item7_mdna.md)

_Extraction: started at the Overview heading._

Overview

As of December 31, 2025, we had $61.2 million of cash and cash equivalents. Cash flows for each of our active communities depend on the status of the development cycle and can differ substantially from reported earnings.

Our principal uses of capital are operating expenses, land and lot purchases, lot development, home construction, interest costs on our indebtedness and the payment of various liabilities. In addition, we may purchase land, lots, homes under construction or other assets as part of an acquisition and repurchase shares of our common stock. Early stages of development or expansion require significant cash outlays for land acquisitions, land development, plats, vertical development, construction of information centers, general landscaping, and other amenities. Because these costs are a component of our inventory and are not recognized in our statement of operations until a home closes, we incur significant cash outflows prior to recognition of home sales revenues. In the later stages of an active community, cash inflows may exceed home sales revenues reported for financial statement purposes, as the costs associated with home and land construction were previously incurred.

Net Debt to Capital Ratio

As of December 31, 2025, our net debt to capital ratio was 43.2%. We use this ratio as a supplemental measure of financial leverage and capital efficiency. This ratio is calculated as net debt (which is total debt minus cash and cash equivalents) divided by net debt plus total equity. Our net debt to capital ratio reflects our balanced approach to financing growth while maintaining liquidity. We continue to monitor leverage levels in light of evolving market conditions to keep an eye on capital efficiency and shareholder value. At December 31, 2025, we were in compliance with all of the covenants contained in the Credit Agreement (as defined herein), including minimum tangible net worth, maximum leverage ratio, minimum liquidity amount, and minimum EBITDA to interest expense ratio, and with all of the covenants contained in the LGI Living Loan Agreement (as defined herein). As of December 31, 2025, $273.6 million was available to borrow under the Credit Agreement, providing ample liquidity to support operations and growth initiatives.

Short-term Liquidity and Capital Resources

We generally rely on our ability to finance our operations by generating operating cash flows and borrowing under the Credit Agreement to adequately fund our short-term working capital obligations and to purchase land and other assets, develop lots and homes and repurchase shares of our common stock. As needed, we will consider accessing the debt and equity capital markets as part of our ongoing financing strategy. We rely on our ability to obtain performance, payment and completion surety bonds as well as letters of credit to finance our projects. Furthermore, we utilize, on a limited and strategic basis, land banking financing arrangements to access short-term liquidity.

As of the date of this Annual Report on Form 10-K, we believe that we will be able to fund our current and foreseeable liquidity needs for at least the next twelve months with our cash on hand, cash generated from operations and cash expected to be available from the Credit Agreement or through accessing debt or equity capital, as needed. However, our ability to engage in the transactions described above may be constrained by volatile or tight economic, capital, credit and financial market conditions, as well as moderated investor or lender interest or capacity and our liquidity, leverage and net worth, and we can provide no assurance as to successfully completing, the costs of, or the operational limitations arising from any one or series of such transactions.

Long-term Liquidity and Capital Resources

We believe that our long-term principal uses of liquidity and capital resources will be inventory related purchases concerning land, lot development, repurchases of shares of our common stock, other capital expenditures, and principal and interest payments on our debt obligations maturing between 2028 and 2032. We believe that we will be able to fund our long-term liquidity needs with cash generated from operations and cash expected to be available to borrow under the Credit Agreement or through accessing debt or equity capital, as needed, although no assurance can be provided that such additional debt or equity capital will be available when needed or on terms that we find attractive. Additionally, we may further utilize, on a limited and strategic basis, land banking financing arrangements to maximize long-term liquidity for lot development projects where we have sufficient finished lot availability in certain markets. To the extent these sources of capital are insufficient to meet our needs, we may also conduct additional public or private offerings of our securities, refinance our indebtedness, or dispose of certain assets to fund our operating activities and capital needs.

Material Cash Requirements

We are a party to many agreements that include contractual obligations and commitments to make payments to third parties. These obligations impact our short-term and long-term liquidity and capital resource needs. Certain contractual obligations are reflected on the consolidated balance sheet as of December 31, 2025, while others are considered future commitments. Our contractual obligations primarily consist of principal and interest payments on our senior notes, notes payable and land banking financing arrangements, including our unsecured revolving credit facility, letters of credit and surety bonds and operating leases. We have no senior note maturities until 2028. We also enter into certain commitments to fund our existing or future unconsolidated joint ventures, letters of credit and other purchase obligations in the normal course of business. For more information regarding our primary obligations, refer to Note 5 , "Accrued Expenses and Other Liabilities," Note 6 , "Notes Payable," and Note 13 , "Commitments and Contingencies," to our consolidated financial statements included in Part II, Item 8 of this Annual Report on Form 10-K for amounts outstanding as of December 31, 2025, related to accrued expenses and other liabilities, debt and commitments and contingencies, respectively.

In the ordinary course of business, we enter into land purchase contracts in order to procure land and lots for the construction of our homes. We are subject to customary obligations associated with entering into contracts for the purchase of land and improved lots. These contracts typically require cash deposits and the purchase of properties under these contracts is generally contingent upon satisfaction of certain requirements by the sellers, which may include obtaining applicable property and development entitlements or the completion of development activities and the delivery of finished lots. We also utilize contracts with land sellers as a method of acquiring lots and land in staged takedowns, which helps us manage the financial and market risk associated with land holdings and minimize the use of funds from our corporate financing sources. Such contracts generally require a non-refundable deposit for the right to acquire land or lots over a specified period of time at pre-determined prices. We generally have the right at our discretion to terminate our obligations under purchase contracts during the initial feasibility period and receive a refund of our deposit, or we may terminate the contracts after the end of the feasibility period by forfeiting our cash deposit with no further financial obligations to the land seller. In addition, our deposit may also be refundable if the land seller does not satisfy all conditions precedent in the respective contract. As of December 31, 2025, we had $19.2 million of cash deposits pertaining to land purchase contracts for 8,952 lots with an aggregate purchase price of $285.7 million. Approximately $8.2 million of the cash deposits as of December 31, 2025 are secured by third-party guarantees or indemnity mortgages on the related property.

Our utilization of land purchase contracts is dependent on, among other things, the availability of land sellers willing to enter into contracts at acceptable terms, which may include option takedown arrangements, the availability of capital to financial intermediaries to finance the development of optioned lots, general housing conditions, and local market dynamics. Land purchase contracts may be more difficult to procure from land sellers in strong housing markets and are more prevalent in certain markets.

Revolving Credit Facility

On August 1, 2025, we entered into a Letter Agreement with several financial institutions, and Wells Fargo Bank, National Association, as administrative agent (the "Letter Agreement Amendment"), which amended the Fifth Amended and Restated Credit Agreement, dated as of April 28, 2021, with several financial institutions, and Wells Fargo Bank, National Association, as administrative agent (as amended to date, including the Letter Agreement Amendment, the "Credit Agreement"). The Credit Agreement provides for a $1.1825 billion revolving credit facility, which can be increased at the request of the Company by up to $95.0 million, subject to the terms and conditions of the Credit Agreement. The Credit Agreement matures on April 28, 2029 with respect to $972.5 million, or 82.2%, of the $1.1825 billion of commitments thereunder and on April 28, 2028 with respect to 17.8% of the commitments thereunder.

Before each anniversary of the Credit Agreement, we may request a one-year extension of its maturity date. The Credit Agreement is guaranteed by, among others, each of our subsidiaries that have gross assets of at least $0.5 million, other than subsidiaries whose sole purpose is to own and operate single-family rental homes.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-20_item1_business.md)

ITEM 1. BUSINESS

General

We are engaged in the design, construction and sale of new homes in markets in Texas, Arizona, Florida, Georgia, New Mexico, Colorado, North Carolina, South Carolina, Washington, Tennessee, Minnesota, Oklahoma, Alabama, California, Oregon, Nevada, West Virginia, Virginia, Pennsylvania, Maryland and Utah. Our management team has been in the residential land development business since the mid-1990s. Since commencing home building operations in 2003, we have constructed and closed over 80,000 homes.

LGI Homes, Inc. is a Delaware corporation incorporated on July 9, 2013. Our principal executive offices are located at 1450 Lake Robbins Drive, Suite 430, The Woodlands, Texas 77380, and our telephone number is (281) 362-8998. Information on or linked to our website is not incorporated by reference into this Annual Report on Form 10-K unless expressly noted.

Unless otherwise indicated or the context requires, "LGI," the "Company," "we," "our" and "us" refer collectively to LGI Homes, Inc. and its subsidiaries.

Business Opportunities

Since December 2013, we have grown substantially, expanding our operations from eight markets in four states to 36 markets in 21 states. As of December 31, 2025, we were active in 144 communities throughout the United States and expect to continue increasing our community count in the future.

Driven by commitment to our customers and our desire to make their dreams of homeownership a reality, we offer multiple product lines, including attached and detached entry-level homes and active adult offerings that are marketed and sold under our LGI Homes brand and luxury homes that are marketed and sold under our Terrata Homes brand.

During 2025, our average home completion time was approximately 105 to 135 days, our home size ranged between 900 to approximately 4,000 square feet and our overall sales prices ranged from approximately $192,000 to more than $1,230,000. For the year ended December 31, 2025, we closed 4,788 homes, including 103 currently or previously leased single-family homes. Excluding the 103 currently or previously leased single-family homes, our average sales price per home closed was $364,035. During 2024, our average home completion time was approximately 105 to 135 days, our home size ranged between 900 to approximately 4,100 square feet and our overall sales prices ranged from approximately $191,000 to more than $1,000,000. For the year ended December 31, 2024, we closed 6,131 homes, including the bulk sale of 103 leased single-family homes. Excluding the bulk sale of 103 leased single-family homes, our average sales price per home closed was $365,394.

We pursue a flexible land acquisition strategy of purchasing or optioning finished lots at attractive prices, or purchasing raw land for residential development. Given our successful history as a land developer, we are experienced in converting raw land into residential communities. We endeavor to maintain a pipeline of desirable land positions for replacement and new communities. We generally target land acquisitions that are further away from urban centers than many other suburban communities but have access to major thoroughfares, retail districts and centers of business. Such areas generally result in a better value for the homeowner, either through lower sales prices or larger lot sizes. We consider development opportunities that meet our profit and return objectives, including opportunities that may involve the sale of home sites as a part of the product mix. Projects of interest are typically evaluated at the division level using an extensive due diligence checklist that includes assessing the permitting and regulatory requirements, environmental considerations and local market conditions and evaluating anticipated floor plans, pricing and financial returns. We also determine the number of potential residents in the market and rental households that are within driving distance of the proposed project. We will continue to focus primarily on entry-level homebuyers.

Additionally, we engage in other business activities that leverage or complement our core homebuilding operations. Our wholesale business sells homes primarily to large institutions interested in acquiring single-family rental properties through bulk sales agreements. Beginning in 2021, we began building and leasing a number of single-family homes in select, existing communities. These rental projects are income producing and we maintain the option to sell these homes in a bulk purchase agreement. Finally, from time to time, we enter into strategic joint ventures. We have two equity-method real estate joint ventures and four additional joint ventures engaged primarily to provide services, such as mortgage and insurance, to our homebuyers.

Sales and Marketing

Our well-defined sales and marketing approach focuses on converting renters of apartments and single-family homes into homeowners. We use extensive digital and print advertising to attract potential homebuyers. We employ various marketing methods, such as digital marketing strategies, interactive online media, social media, directional signage, and billboards. These

methods have proven highly successful in reaching our target market, placing potential homebuyers in front of our trained sales professionals and communicating our core messages of value and dream fulfillment.

While a proportion of our business comes from realtors, our marketing efforts are principally designed to connect directly with potential customers currently renting their residences and encourage them to schedule an in-person appointment at one of our information centers. Our information centers are typically open 8 to 10 hours per day, 359 days per year, and are generally staffed by two to four sales professionals.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-02-20_item7_mdna.md, 10-K_2026-02-20_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
