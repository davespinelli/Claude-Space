# Triage pack — IDN · Intellicheck, Inc.

_Generated 2026-09-04 21:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** IDN · **Name:** Intellicheck, Inc.
- **CIK:** 0001040896
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/IDN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Intellicheck, Inc.
- **CIK:** 1,040,896 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 2.88 |
| mktcap | $58.4M |
| ev | $46.5M |
| ev_ebit | 42.8x |
| fcf | $4.5M |
| fcf_yield | 7.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 8.1% |
| net_debt | -$11.8M |
| net_debt_ebit | -10.9x |
| cash | $11.8M |
| ltd | $0.00 |
| equity | $22.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $22.7M |
| revenue_prior | $20.0M |
| rev_growth | 13.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $1.1M |
| net_income | $1.3M |
| cfo | $4.5M |
| capex | $52k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 20,266,743 |
| shares_py | 20,037,271 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -27.8% |
| r6m | -42.3% |
| off_52w_high | -68.0% |
| adv20 | $1.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.63 |
| r_ev_ebit | 0.16 |
| r_roic | 0.65 |
| r_rev_growth | 0.73 |
| r_buyback | 0.43 |
| score | 0.42 |

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
| rank | 312 |

**Screen rationale:** debt data missing (net cash unverified); WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **20,266,743** (CY2026Q2I) vs **20,037,271** prior year (CY2025Q2I)
- Change: **1.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-22** — Item 5.02 (officer / director change or comp arrangement): On July 16, 2026, Jonathan Robins notified Intellicheck, Inc. (the "Company") of his decision to separate from his employment as the Company's Chief Technology Officer for personal family reasons, effective July 18, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 45,550 sh / $343,859 -> net $-343,859 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 5).

| code | rows |
|---|---|
| A | 6 |
| G | 2 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-13_2-02-results.md)

_Extraction: started at the first release heading, 'Intellicheck Reports Second Quarter 2026 Results'; skipped 3 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (idn_q22026pressrelease.htm)

Intellicheck Reports Second Quarter 2026 Results

Revenue Grows 16% to $5.9 Million

Net Income Rises to $0.7 Million

Adjusted EBITDA Increases to $1.1 Million

MELVILLE, NEW YORK – August 13, 2026 – Intellicheck, Inc. (Nasdaq: IDN) ("Intellicheck" or the "Company"), an industry-leading identity company delivering proprietary on-demand digital and physical identification validation solutions, today reported financial results for the second quarter ended June 30, 2026. The Company today also provided an update on a customer.

Business Highlights

• Revenue was $5.9 million in the second quarter, up 16% year-over-year and 7% on a quarterly sequential basis. SaaS revenue comprised substantially all of total revenue.

• Adjusted EBITDA, a non-GAAP metric, was $1.1 million in the second quarter, increasing $1.0 million year-over-year, and marking the Company's fifth consecutive positive quarter.

• Banking and lending represented approximately 48% of Q2 revenue and continues to be the Company's largest growing vertical in terms of total revenue as it continues to gain traction in Desktop, the Alloy channel, and among smaller institutions.

• Retail represented approximately 29% of Q2 revenue.

• Momentum continued across emerging and adjacent verticals including cargo and freight, foreign auto manufacturers and their supplier networks, stadium and venue concessions, age-related and background-check verticals, and automotive dealer scanning volumes.

"Our second quarter results reflect the benefits from continued progress on our diversification initiative as we now generate revenue from about 500 customers across 14 segments, both of which are diversified significantly from two years ago when we began these efforts," said Bryan Lewis, President and Chief Executive Officer of Intellicheck. "The momentum in our business was clear as revenue rose 16% year-over-year to a Q2 record of $5.9 million. In addition, our focus on operating discipline

has helped drive four consecutive quarters of profitability, and five consecutive quarters of positive adjusted EBITDA which improved $1.0 million compared to the same period last year to $1.1 million."

Customer Update

At the end of the second quarter of 2026, the Company was informed by its customer, which represented approximately 29% of first-half 2026 revenue, the "Customer", that the Customer is shifting from a sole-source to a multi-source vendor architecture and is testing an alternative solution on select use cases that is expected to negatively affect our transaction levels with the Customer. The main phase of the transition was scheduled to commence in late July and as such had no material impact on Intellicheck's results for the three- and six-month periods ended June 30, 2026. As of August 12, 2026, the Company has not yet seen the level of volume reductions this Customer's plans call for.

Lewis commented, "We are actively engaged with this Customer as they test their alternative solution. To date, the total traffic shift has not been to the extent their plan called for. Additionally, the Customer has indicated that their shift from a single source to a multi-source vendor architecture is not being driven by our results, as they have recently signed another purchase order and have indicated an intention to transition to our newest API. We believe this reflects recognition of the broader capabilities we can provide and the opportunity to further expand our support of their needs over the longer term."

"Our business is significantly stronger and more diversified today than it was even several years ago, and as such is much better positioned to address this challenge than at any other time in our history. Excluding this Customer, revenue from our remaining base grew approximately 19% in the first half of 2026, and we expect this growth will continue as we continue to execute on our customer and vertical diversification initiative. We are focused on accelerating our pipeline of new customers and expanding the scope of what we do with existing customers which we expect will help drive positive adjusted EBITDA generation for the second half of the year as well as position the Company to be profitable for the full year."

Financial and Balance Sheet Highlights

• Gross margin was 91% in the second quarter as compared to 90% in the year-ago period.

• Operating expenses were $4.9 million in both the 2026 and 2025 second quarters.

• Income from operations was $0.6 million and net income was $0.7 million, up from a loss of $(0.3) million and a net loss of $(0.3) million in the year-ago period.

• Adjusted EBITDA was $1.1 million in the second quarter, marking the Company's fifth consecutive positive quarter. Adjusted EBITDA was $0.1 million in the second quarter of 2025

• The Company ended the quarter with $11.8 million in cash and no debt. Cash from operations for the first half was $2.2 million.

"We remain focused on cost discipline, while continuing to fund the engineering behind our platform accuracy and availability, and the go-to-market investment required to grow our revenue from current and new customers," said Adam Sragovicz, Chief Financial Officer of Intellicheck. "Importantly, we have a strong balance sheet, with $11.8 million in cash and no debt, which provides us the flexibility to execute on our growth initiatives."

Earnings Conference Call Details

• Date / Time: Thursday, August 13 at 4:30 PM ET / 1:30 PM PT

• U.S. Dial-in: 877-407-8037

• International Dial-in: 201-689-8037

A replay of the conference call will be available shortly after completion of the live event. To listen to the replay, please dial 877-660-6853 and use conference identification number 13761557. For callers outside the U.S., please dial 201-612-7415 and use conference identification number 13761557. The replay will be available beginning approximately three hours after the completion of the live event and will remain available until August 20, 2026.

INTELLICHECK, INC.

UNAUDITED CONDENSED BALANCE SHEETS

JUNE 30, 2026 AND DECEMBER 31, 2025

(in thousands, except share and per share amounts)

June 30, 2026 | December 31, 2025
(Unaudited)
ASSETS
CURRENT ASSETS:
Cash and cash equivalents | 11,837 | 9,650
Accounts receivable, net of allowance for credit losses of $157 at June 30, 2026 and December 31, 2025 | 2,660 | 3,365
Other current assets | 816 | 892
Total current assets | 15,313 | 13,907
PROPERTY AND EQUIPMENT, NET | 351 | 394
GOODWILL | 8,102 | 8,102
INTANGIBLE ASSETS, NET | 1,798 | 2,077
OTHER ASSETS | 1 | 1
Total assets | 25,565 | 24,481
LIABILITIES AND STOCKHOLDERS' EQUITY
CURRENT LIABILITIES:
Accounts payable | 385 | 226
Accrued expenses | 1,496 | 1,897
Deferred revenue | 1,195 | 1,661
Total current liabilities | 3,076 | 3,784
Total liabilities | 3,076 | 3,784
COMMITMENTS AND CONTINGENCIES
STOCKHOLDERS' EQUITY:
Preferred stock - $0.01 par value; 30,000 shares authorized; Series A convertible preferred stock, zero shares issued and outstanding at June 30, 2026 and December 31, 2025 | — | —
Common stock - $0.001 par value; 40,000,000 shares authorized; 20,252,888 and 20,225,323 shares issued and outstanding at June 30, 2026 and December 31, 2025, respectively | 20 | 20
Additional paid-in capital | 154,380 | 153,887
Accumulated deficit | (131,911) | (133,210)
Total stockholders' equity | 22,489 | 20,697
Total liabilities and stockholders' equity | 25,565 | 24,481

INTELLICHECK, INC.

UNAUDITED CONDENSED STATEMENTS OF OPERATIONS

FOR THE THREE AND SIX MONTHS ENDED JUNE 30, 2026 AND 2025

(in thousands, except share and per share amounts)

Three months ended June 30, | Six months ended June 30,
2026 | 2025 | 2026 | 2025
REVENUES | 5,941 | 5,123 | 11,465 | 10,017
COST OF REVENUES | (517) | (523) | (1,016) | (1,025)
Gross profit | 5,424 | 4,600 | 10,449 | 8,992
OPERATING EXPENSES
Selling, general and administrative | 3,481 | 3,535 | 6,724 | 6,988
Research and development | 1,370 | 1,363 | 2,610 | 2,650
Total operating expenses | 4,851 | 4,898 | 9,334 | 9,638
Income (loss) from operations | 573 | (298) | 1,115 | (646)
OTHER INCOME (EXPENSE), NET
Other income, net | 90 | 47 | 184 | 77
Total other income, net | 90 | 47 | 184 | 77
Net income (loss) before provision for income taxes | 663 | (251) | 1,299 | (569)
Provision for income taxes | — | — | — | —
Net income (loss) | 663 | (251) | 1,299 | (569)
PER SHARE INFORMATION
Income (loss) per common share -
Basic | 0.03 | (0.01) | 0.06 | (0.03)
Diluted | 0.03 | (0.01) | 0.06 | (0.03)
Weighted average common shares used in computing per share amounts
Basic | 20,244,802 | 19,795,189 | 20,243,718 | 19,357,364
Diluted | 20,930,380 | 19,795,189 | 20,876,861 | 19,357,364

INTELLICHECK, INC.

UNAUDITED CONDENSED STATEMENTS OF STOCKHOLDERS' EQUITY

FOR THE THREE AND SIX MONTHS ENDED JUNE 30, 2026 AND 2025

(in thousands, except number of shares)

Three months ended June 30, 2026
Common Stock | Additional Paid-in Capital | Accumulated Deficit | Total Stockholders' Equity
Shares | Amount
BALANCE, March 31, 2026 | 20,239,060 | 20 | 154,087 | (132,574) | 21,533
Stock-based compensation | – | – | 289 | – | 289
Stock option exercises, net of cashless exercises | 1,667 | – | 4 | – | 4
Issuance of shares for vested restricted stock grants | 12,161 | – | – | – | –
Net income | – | – | – | 663 | 663
BALANCE, June 30, 2026 | 20,252,888 | 20 | 154,380 | (131,911) | 22,489

Three months ended June 30, 2025
Common Stock | Additional Paid-in Capital | Accumulated Deficit | Total Stockholders' Equity
Shares | Amount
BALANCE, March 31, 2025 | 19,816,043 | 19 | 152,390 | (134,801) | 17,608
Stock-based compensation | – | – | 202 | – | 202
Stock option exercises, net of cashless exercises | 181,256 | 1 | 445 | – | 446
Issuance of shares for vested restricted stock grants | 28,544 | – | – | — | —
Net loss | – | – | – | (251) | (251)
BALANCE, June 30, 2025 | 20,025,843 | 20 | 153,037 | (135,052) | 18,005

Six months ended June 30, 2026
Common Stock | Additional Paid-in Capital | Accumulated Deficit | Total Stockholders' Equity
Shares | Amount
BALANCE, December 31, 2025 | 20,225,323 | 20 | 153,887 | (133,210) | 20,697
Stock-based compensation | – | – | 489 | – | 489
Stock option exercises, net of cashless exercises | 1,667 | 4 | – | 4
Issuance of shares for vested restricted stock grants | 25,898 | – | – | – | –
Net income | – | – | – | 1,299 | 1,299
BALANCE, June 30, 2026 | 20,252,888 | 20 | 154,380 | (131,911) | 22,489

Six months ended June 30, 2025
Common Stock | Additional Paid-in Capital | Accumulated Deficit | Total Stockholders' Equity
Shares | Amount
BALANCE, December 31, 2024 | 19,782,311 | 19 | 152,211 | (134,483) | 17,747
Stock-based compensation | – | – | 381 | – | 381
Stock option exercises, net of cashless exercises | 181,256 | 1 | 445 | – | 446
Issuance of shares for vested restricted stock grants | 62,276 | – | – | – | –
Net loss | – | – | – | (569) | (569)
BALANCE, June 30, 2025 | 20,025,843 | 20 | 153,037 | (135,052) | 18,005

INTELLICHECK, INC.

UNAUDITED CONDENSED STATEMENTS OF CASH FLOWS

FOR THE SIX MONTHS ENDED JUNE 30, 2026 AND 2025

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-19_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

We are a prominent technology company engaged in developing, integrating and marketing identity verification solutions to address challenges that include commercial retail and banking fraud prevention. Our products include solutions for preventing identity fraud across any industry delivered via smartphone, tablet, POS integration or other electronic devices.

Critical Accounting Policies and the Use of Estimates

The preparation of our financial statements in conformity with accounting principles generally accepted in the United States ("GAAP") requires management to make estimates and assumptions that affect the amounts reported in our financial statements and accompanying notes. Significant estimates and assumptions that affect amounts reported in the financial statements include impairment consideration and valuation of goodwill and intangible assets including software development costs, revenue recognition (including breakage revenue), and the fair value of stock options under our stock-based compensation plans. Due to the inherent uncertainties involved in making estimates, actual results reported in future periods may be different from those estimates.

Revenue Recognition and Deferred Revenue

SaaS fees and service revenues are generated from a combination of fixed-price and per-scan contracts. Under the per-scan revenue model, customers are charged a fee each time the customer scans an identity document, such as a driver's license, with our software. Under the fixed-price revenue model customers are charged a fixed monthly fee either per device or physical business location to access our software. In certain instances, customization services are determined to be essential to the functionality of the delivered software. Under Accounting Standards Codification ("ASC") 606,

" Revenue from Contracts with Customers, " revenue is recognized when a customer obtains control of promised goods or services in an amount that reflects the consideration expected to be received in exchange for those goods or services. We measure revenue based on the consideration specified in a customer arrangement, and revenue is recognized when the performance obligations in an arrangement are satisfied. The Company adopted an additional revenue model where customers purchase a predetermined number of transactions for the term of the contract, where revenue for these transactions is recognized on a per transaction basis. The Company estimates the number of transactions that will be unused by the end of each contract period and recognized a portion of that revenue as breakage revenue each reporting period. Reference Note 2, "Significant Accounting Policies," in the Notes to Financial Statements for additional details on the Company's recognized and deferred revenue. The Company also has a revenue model where customers purchase access to the Company's platform that includes a fixed, non-refundable annual access fee associated with a spend commitment that grants the customers stand-ready access to the platform. Revenue for this access is recognized ratably over the contract term, consistent with the nature of the stand-ready service.

Stock-based Compensation

We account for the issuance of stock-based compensation awards to employees in accordance with ASC 718, " Compensation – Stock Compensation ", which requires that the cost resulting from all stock-based compensation payment transactions be recognized in the financial statements. This pronouncement establishes fair value as the measurement objective in accounting for stock-based compensation payment arrangements and requires all companies to apply a fair value-based measurement method in accounting for all stock-based compensation payment transactions with employees. Reference Note 9, "Stockholders' Equity," in the Notes to Financial Statements for details on the Company's stock-based compensation plans.

Valuation of long-lived assets

Our long-lived assets include property and equipment, goodwill, and intangible assets. As of December 31, 2025, the balances of property and equipment, goodwill and intangible assets, all net of accumulated depreciation and amortization, were $394, $8,102 and $2,077, respectively. As of December 31, 2024, the balances of property and equipment, goodwill and intangible assets, all net of accumulated depreciation and amortization, were $536, $8,102 and $2,374, respectively. Reference Note 2, "Significant Accounting Policies"; Note 4, "Property and Equipment"; and Note 5, "Goodwill and Intangible Assets" in the Notes to Financial Statements for details on the Company's valuations of our long-lived assets.

Internal Use Capitalized Software

We capitalize certain costs related to the development of our platform and other software applications for internal use. In accordance with authoritative guidance, we capitalize our costs to develop software when preliminary development efforts are successfully completed, management has authorized and committed project funding, and it is probable that the project will be completed and the software will be used as intended. We stop capitalizing these costs when the software is substantially complete and ready for its intended use, including the completion of all significant testing. These costs are amortized on a straight-line basis over the estimated useful life of the related asset. We also capitalize costs related to specific upgrades and enhancements when it is probable the expenditure will result in additional functionality and expense costs incurred for maintenance and minor upgrades and enhancements. Costs incurred prior to meeting these criteria together with costs incurred for training and maintenance are expensed as incurred and recorded within research and development expenses in the statements of operations. We exercise judgment in determining the point at which various projects may be capitalized, in assessing the ongoing value of the capitalized costs and in determining the estimated useful lives over which the costs are amortized.

Income Taxes and Valuation Allowance

We account for income taxes in accordance with ASC 740, Income Taxes. Under this standard, deferred tax assets and liabilities are recognized for the estimated future tax consequences attributable to differences between the financial statement carrying amounts of existing assets and liabilities and their respective tax bases, as well as for net operating loss and tax credit carryforwards. Deferred tax assets and liabilities are measured using enacted tax rates expected to apply to taxable income in the years in which those temporary differences are expected to be recovered or settled.

We establish a valuation allowance against deferred tax assets when, based on the weight of available evidence, it is more likely than not that some or all of the deferred tax assets will not be realized. In making this determination, we consider all available positive and negative evidence, including:

• Our cumulative results for the most recent three-year period, adjusted for permanent differences between book and taxable income;

• The nature, frequency, and magnitude of current and cumulative financial reporting income and losses;

• Our forecasts of future taxable income, considering the predictability and sustainability of recent operating trends;

• The length of time net operating loss and tax credit carryforwards remain available, including the distinction between carryforwards with definite expiration dates and those that carry forward indefinitely;

• The nature and timing of reversals of existing taxable and deductible temporary differences; and

• Available tax planning strategies that could be implemented, if necessary, to accelerate taxable income.

As of December 31, 2025, we maintained a full valuation allowance of approximately $6,677 against our net deferred tax assets. Our three-year cumulative result through December 31, 2025, after adjusting for permanent differences, remained in a loss position, which constitutes significant objective negative evidence under ASC 740. While we generated pre-tax income of approximately $1,331 during the year ended December 31, 2025, representing a meaningful improvement from prior-year losses of $2,042 in 2023 and $885 in 2024, we have not yet established a sustained pattern of profitability sufficient to overcome this negative evidence.

This assessment requires significant judgment. Should we continue to generate taxable income in future periods such that the three-year cumulative result transitions to a positive position, and should we conclude that the weight of positive evidence outweighs the negative evidence, we may determine that a partial or full release of the valuation allowance is appropriate. Any such release would be recorded as a non-cash deferred income tax benefit in the period the determination is made and could be material to our results of operations. Based on the gross deferred tax assets as of December 31, 2025, a full release of the valuation allowance would result in a tax benefit of approximately $6,677.

Results of Operations

COMPARISON OF THE YEAR ENDED DECEMBER 31, 2025

TO THE YEAR ENDED DECEMBER 31, 2024

REVENUES . Revenues for the year ended December 31, 2025 increased $2,669 or 13% to $22,666 compared to $19,997 for the year ended December 31, 2024. The increase in revenues is primarily the result of higher SaaS revenue for the current period. SaaS revenues, which consists of software licensed on a subscription basis, increased $2,626 or 13% to $22,436 for the year ended December 31, 2025 compared to $19,810 for the year ended December 31, 2024.

GROSS PROFIT . Gross profit increased by $2,334 or 13%, to $20,500 for the year ended December 31, 2025, compared to $18,166 in the year ended December 31, 2024. Our gross profit, as a percentage of revenues, was 90.4% and 90.8% for the years ended December 31, 2025 and 2024, respectively.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-19_item1_business.md)

Item 1. Business

OVERVIEW

We originally were incorporated in the state of New York in 1994 as Intelli-Check, Inc. In August 1999, we reincorporated in Delaware. On March 14, 2008, our corporation was renamed Intelli-Check - Mobilisa, Inc. after the consummation of the merger with Mobilisa, Inc. ("Mobilisa") (references to "Intelli-Check" in this annual report refer to the Company prior to the merger with Mobilisa). At the closing of the merger, our headquarters were moved to Mobilisa's offices in Port Townsend, Washington. On October 27, 2009, we made a further change in our name to Intellicheck Mobilisa, Inc. On May 4, 2017, with the approval of our shareholders, we changed our name to Intellicheck, Inc. ("Intellicheck," "we," "our," "us," or "the Company"). On August 31, 2009, the Company acquired 100% of the common stock of Positive Access Corporation ("Positive Access"), a developer of driver's license reading technology. The acquisition of Positive Access expanded the Company's technology portfolio and related product offerings and allowed the Company to reach a larger number of customers through Positive Access's extensive distribution network. On December 31, 2018, we formally merged the Mobilisa and Positive Access subsidiaries into one corporation under the name Intellicheck, Inc.

We are a prominent technology company that delivers on-demand digital identity validation solutions for Know Your Customer ("KYC") fraud, and age verification needs. We validate both digital and physical identities for financial services, fintech companies, BNPL providers, e-commerce, retail commerce businesses, law enforcement and government agencies across North America. Our software solutions can be used through a mobile device, a browser, or a retail point-of-sale scanner.

We plan to expand our business in the near term by continuing to pursue a strategy designed to increase market share in our existing markets and expand into new product markets that are expected to benefit from fraud prevention and identity validation. For example, we have extended our technologies into online applications to provide identity validation and fraud prevention for the billions of transactions that occur online each day. We also have incorporated biometric, facial recognition and other enhancements to several of our current product offerings in order to stay on the leading edge of technology.

We plan to leverage our intellectual property in the markets we are targeting to strengthen our competitive position.

Our primary businesses include Identity Systems products, which include commercial applications of identity card reading authentication.

Our technologies address problems such as:

■ Commercial Fraud – financial institutions and merchants use our technology to prevent economic losses from check cashing, debit and credit card transactions, account take overs, and e-commerce as well as other types of fraud such as identity theft that principally use fraudulent identification documents as proof of identity;

■ Instant Credit Card Approval – retail stores and financial institutions use our technology to scan a driver's license at a kiosk or at the Point of Sale (POS) to confirm that an applicant is who they claim to be with additional certainty. Once confirmed that a driver's license is valid, the transaction can proceed to the underwriting stage where qualified applicants can get instant approval for a loyalty-branded credit card. This technique protects consumer data and is significantly more likely to result in a completed transaction compared to in-store personnel asking customers to fill out a paper form and then entering the data;

■ Age Restricted Product Access – products validate driver's licenses and other government forms of identification to confirm the age of customers purchasing age restricted products. Target industries include alcohol, cannabis, tobacco, gambling, bars and nightclubs.

■ Unauthorized Access – our systems and software are designed to increase security and deter terrorism at airports, shipping ports, rail and bus terminals, military installations, high profile buildings and infrastructure where security is a concern;

■ Fraudulent Retail Purchase Returns – implementing our validation software solutions can prevent fraudulent retail returns in situations where customers are seeking store credit or cash compensation for items being returned without a receipt when the transaction requires a driver's license for identification; and

■ Inefficiencies Associated with Manual Data Entry – by reading encoded data contained in the bar code and magnetic stripe of an identification card with a quick swipe or scan of the card, where permitted by law, customers are capable of accurately and instantaneously inputting information into forms, applications and the like without the errors associated with manual data entry.

IDENTITY CARD READING AND VERIFICATION SECTOR

Background on Identification Documentation

Driver's license

The driver's license is the most widely used form of government issued photo identification in North America. The Real ID Act, which became federal law in May 2005, recognizes that the driver's license is also a quasi-identification card. In addition to its primary function, the driver license is used to verify identity for social services, firearm sales, check cashing, credit card issuance and use and other applications. Our technology can read the digitally stored barcode information on all currently issued driver's licenses even those that do not comply with the standards of the American Association of Motor Vehicle Administrators ("AAMVA"), the American National Standards Institute ("ANSI") and the International Standards Organization ("ISO"). Today, all 50 states, the District of Columbia, territories of the United States, United States Military, and all 13 Canadian provinces/territories digitally store information on their driver license.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-19_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-19_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-19_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-13_2-02-results.md, 10-K_2026-03-19_item7_mdna.md, 10-K_2026-03-19_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
