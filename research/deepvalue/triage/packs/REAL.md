# Triage pack — REAL · TheRealReal, Inc.

_Generated 2026-09-04 22:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** REAL · **Name:** TheRealReal, Inc.
- **CIK:** 0001573221
- **SIC:** 5900 — Retail-Miscellaneous Retail
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/REAL

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** TheRealReal, Inc.
- **CIK:** 1,573,221 · **SIC:** 5900 (Retail-Miscellaneous Retail) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermNotesPayable

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income exceeds revenue; net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 10.06 |
| mktcap | $1.2B |
| ev | $1.2B |
| ev_ebit | n/a |
| fcf | $18.4M |
| fcf_yield | 1.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $25.2M |
| net_debt_ebit | n/a |
| cash | $119.1M |
| ltd | $144.3M |
| equity | -$377.7M |
| ltd_tag | LongTermNotesPayable |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $692.8M |
| revenue_prior | $600.5M |
| rev_growth | 15.4% |
| rev_growth_note | n/a |
| eq_flag | net income exceeds revenue; net income more than 3x operating income |
| ebit | -$23.9M |
| net_income | $41.8B |
| cfo | $37.0M |
| capex | $18.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 5.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 121,671,115 |
| shares_py | 115,237,276 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 52.8% |
| r6m | -11.5% |
| off_52w_high | -40.5% |
| adv20 | $37.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.27 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.77 |
| r_buyback | 0.17 |
| score | 0.39 |

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
| rank | 326 |

**Screen rationale:** revenue +15.4%; 12-1 momentum 52.8%; EARNINGS QUALITY: net income exceeds revenue; net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **121,671,115** (CY2026Q2I) vs **115,237,276** prior year (CY2025Q2I)
- Change: **5.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-03-09** — Item 5.02 (officer / director change or comp arrangement): On March 6, 2026, Niki Leondakis resigned from the Board of Directors (the "Board") of The RealReal, Inc. (the "Company").

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 173,004 sh / $1,899,363 -> net $-1,899,363 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 23 (open-market buys 0, sales 16).

| code | rows |
|---|---|
| A | 7 |
| S | 16 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter Highlights'; skipped 10 forward-looking-statement block(s); 10 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (real-20260807xex991pressre.htm)

Second Quarter Highlights

• GMV wa s $617 million, an increase of 22% compared to the same period in 2025

• Total Revenue was $193 million, an increase of 17% compared to the same period in 2025

• Gross Profit was $143 million, an increase of $21 million compared to the same period in 2025

• Gross Margin was 74.4%, an increase of 10 basis points compared to the same period in 2025

• Net Loss was $(27) million or (14.1)% of total revenue, compared to $(11) million or (6.9)% of total revenue in the same period in 2025. Second Quarter 2026 Net Loss includes a $(18.6) million non-cash adjustment as a result of the change in fair value of warrant liability.

• Adjusted EBITDA was $13.5 million or 7.0% of total revenue compared to $6.8 million or 4.1% of total revenue in the same period in 2025

• GAAP basic net loss per share was $(0.23) compared to $(0.10) in the prior year period and GAAP diluted net loss per share was $(0.23) compared to $(0.13) in the prior year period

• Non-GAAP basic and diluted net loss attributable to common stockholders per share was $(0.01) compared to $(0.06) in the prior year period

• Top-line-related Metrics

◦ Trailing twelve months active buyers was 1,107,000, an increase of 11% compared to the same period in 2025

◦ Average order value (AOV) was $659, an increase of 13% versus the same period in 2025

Q3 and Full Year 2026 Guidance

Based on market conditions as of August 6, 2026, we are raising our full year guidance. Additionally, we are providing guidance for third quarter 2026 GMV, Total Revenue and Adjusted EBITDA, which is a Non-GAAP financial measure.

We have not reconciled forward-looking Adjusted EBITDA to net income (loss), the most directly comparable GAAP measure, because we cannot predict with reasonable certainty the ultimate outcome of certain components of

such reconciliations including payroll tax expense on employee stock transactions that are not within our control, or other components that may arise, without unreasonable effort. For these reasons, we are unable to assess the probable significance of the unavailable information, which could materially impact the amount of future net income (loss).

Q3 2026 | Full Year 2026
GMV | $610 - $620 million | $2.535 - $2.565 billion
Total Revenue | $194 - $198 million | $788 - $797 million
Adjusted EBITDA | $13.5 - $14.5 million | $66.0 - $69.0 million

W ebcast and Conference Call

The RealReal will host a conference call to review the company's second quarter results beginning at approximately 2:00 p.m. Pacific Time today (5:00 p.m. Eastern Time). A live webcast of the conference call and accompanying materials will be available online at investor.therealreal.com . A replay of the webcast will be available at the same location. To access the conference please register using this link:

https://the-realreal-earnings-call-q2-2026.open-exchange.net/registration.

About The RealReal, Inc.

The RealReal is the world's largest online marketplace for authenticated, resale luxury goods, trusted by more than 40 million members. Our full-service consignment model—offering virtual appointments, in-home pickup, drop-off, and direct shipping—enables consumers to buy and sell luxury across fashion, fine jewelry and watches, art, and home categories with ease. The company combines a rigorous, expert-led authentication process with proprietary technology, including AI and machine learning, to power optimal pricing and processing for our members and to help scale the business. By extending the life of millions of luxury goods, the company is leading a more circular economy, all the while delivering a seamless experience for buyers and sellers.

Investor Relations Contact:

IR@therealreal.com

Press Contact:

PR@therealreal.com

Free cash flow is a non-GAAP financial measure that is calculated as net cash (used in) provided by operating activities less net cash used to purchase property and equipment and capitalized proprietary software development costs. We believe free cash flow is an important indicator of our business performance, as it measures the amount of cash we generate. Accordingly, we believe that free cash flow provides useful information to investors and others in understanding and evaluating our operating results in the same manner as our management.

Non-GAAP net loss per share attributable to common stockholders, basic and diluted is a non-GAAP financial measure that is calculated as GAAP net loss plus stock-based compensation expense, provision (benefit) for income taxes, payroll tax expense on employee stock transactions, gain on extinguishment of debt, change in fair value of warrant liabilities and certain one-time expenses divided by weighted average shares outstanding. We believe that

making these adjustments before calculating per share amounts for all periods presented provides a more meaningful comparison between our operating results from period to period.

THE REALREAL, INC.

Statements of Operations

(In thousands, except share and per share data)

(Unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue:
Consignment revenue | 148,216 | 128,620 | 294,109 | 252,434
Direct revenue | 25,787 | 20,495 | 51,595 | 40,949
Shipping services revenue | 18,568 | 16,073 | 36,582 | 31,838
Total revenue | 192,571 | 165,188 | 382,286 | 325,221
Cost of revenue:
Cost of consignment revenue | 16,075 | 13,761 | 31,522 | 26,715
Cost of direct revenue | 20,407 | 17,185 | 40,691 | 32,420
Cost of shipping services revenue | 12,887 | 11,566 | 25,537 | 23,387
Total cost of revenue | 49,369 | 42,512 | 97,750 | 82,522
Gross profit | 143,202 | 122,676 | 284,536 | 242,699
Operating expenses:
Marketing | 18,382 | 15,548 | 36,939 | 31,403
Operations and technology | 74,706 | 68,986 | 147,425 | 135,964
Selling, general and administrative | 52,397 | 48,027 | 104,729 | 97,988
Total operating expenses (1) | 145,485 | 132,561 | 289,093 | 265,355
Loss from operations | (2,283) | (9,885) | (4,557) | (22,656)
Change in fair value of warrant liability | (18,583) | 4,537 | 28,752 | 47,040
Gain on extinguishment of debt | — | — | — | 37,101
Interest income | 902 | 1,109 | 1,903 | 2,483
Interest expense | (7,322) | (7,038) | (14,543) | (13,358)
Other income, net | 154 | — | 357 | 608
Income (loss) before provision for income taxes | (27,132) | (11,277) | 11,912 | 51,218
Provision for income taxes | 101 | 89 | 209 | 184
Net income (loss) attributable to common stockholders | (27,233) | (11,366) | 11,703 | 51,034
Net income (loss) per share attributable to common stockholders
Basic | (0.23) | (0.10) | 0.10 | 0.45
Diluted | (0.23) | (0.13) | (0.13) | (0.27)
Weighted average shares used to compute net income (loss) per share attributable to common stockholders
Basic | 121,023,931 | 114,044,057 | 120,277,907 | 113,046,607
Diluted | 121,023,931 | 119,484,716 | 126,390,826 | 120,178,570
(1) Includes stock-based compensation as follows:
Marketing | 422 | 424 | 767 | 727
Operations and technology | 2,580 | 2,677 | 4,557 | 4,901
Selling, general and administrative | 4,573 | 5,107 | 8,524 | 9,939
Total | 7,575 | 8,208 | 13,848 | 15,567

THE REALREAL, INC.

Condensed Balance Sheets

(In thousands, except share and per share data)

(Unaudited)

June 30, 2026 | December 31, 2025
Assets
Current assets
Cash and cash equivalents | 119,132 | 151,231
Accounts receivable, net | 20,073 | 23,822
Inventory, net | 35,431 | 30,843
Prepaid expenses and other current assets | 18,682 | 21,595
Total current assets | 193,318 | 227,491
Property and equipment, net | 100,558 | 96,148
Operating lease right-of-use assets | 63,240 | 64,641
Restricted cash | 14,777 | 14,808
Other assets | 6,394 | 5,945
Total assets | 378,287 | 409,033
Liabilities and Stockholders' Deficit
Current liabilities
Accounts payable | 15,049 | 14,565
Accrued consignor payable | 95,062 | 111,497
Operating lease liabilities, current portion | 23,095 | 24,645
Other accrued and current liabilities | 100,274 | 113,533
Total current liabilities | 233,480 | 264,240
Operating lease liabilities, net of current portion | 64,404 | 66,793
Convertible Senior Notes, net | 231,516 | 230,833
Non-convertible notes, net | 144,293 | 140,980
Warrant liability | 74,688 | 114,353
Other noncurrent liabilities | 7,636 | 7,352
Total liabilities | 756,017 | 824,551
Stockholders' deficit:
Common stock, $0.00001 par value; 500,000,000 shares authorized as of June 30, 2026, and December 31, 2025; 121,666,258 and 118,318,917 shares issued and outstanding as of June 30, 2026, and December 31, 2025, respectively | 1 | 1
Additional paid-in capital | 906,192 | 880,107
Accumulated deficit | (1,283,923) | (1,295,626)
Total stockholders' deficit | (377,730) | (415,518)
Total liabilities and stockholders' deficit | 378,287 | 409,033

THE REALREAL, INC.

Condensed Statements of Cash Flows

(In thousands)

(Unaudited)

Six Months Ended June 30,
2026 | 2025
Cash flows from operating activities:
Net income | 11,703 | 51,034
Adjustments to reconcile net income to cash used in operating activities:
Depreciation and amortization | 15,917 | 16,631
Stock-based compensation expense | 13,848 | 15,567
Reduction of operating lease right-of-use assets | 8,562 | 7,943
Bad debt expense | 1,342 | 1,214
Non-cash interest expense | 3,227 | 5,483
Accretion of debt discounts and issuance costs | 940 | 1,060
Provision for inventory write-downs and shrinkage | 1,810 | 1,485
Gain on debt extinguishment | — | (37,101)
Change in fair value of warrant liability | (28,752) | (47,040)
Loss (gain) related to warehouse fire, net | — | (353)
Other adjustments | 78 | (36)
Changes in operating assets and liabilities:
Accounts receivable, net | 2,407 | (10,020)
Inventory, net | (6,398) | (6,678)
Prepaid expenses and other current assets | 2,913 | 6,595
Other assets | (479) | (501)
Operating lease liability | (11,100) | (10,876)
Accounts payable | (266) | 2,357
Accrued consignor payable | (16,435) | (13,709)
Other accrued and current liabilities | (14,538) | (14,743)
Other noncurrent liabilities | 213 | (152)
Net cash used in operating activities | (15,008) | (31,840)
Cash flow from investing activities:
Insurance proceeds related to warehouse fire | — | 2,309
Capitalized proprietary software development costs | (6,837) | (6,483)
Purchases of property and equipment | (11,502) | (12,518)
Net cash used in investing activities | (18,339) | (16,692)
Cash flow from financing activities:
Proceeds from exercise of stock options | 308 | 114
Taxes paid related to restricted stock vesting | (109) | (83)
Repayment of 2025 Notes | — | (26,749)
Proceeds from issuance of stock in connection with the Employee Stock Purchase Program | 1,018 | 838
Cash received from settlement of capped calls in conjunction with the 2025 Note Exchanges | — | 1,499
Issuance costs paid related to the 2025 Note Exchanges | — | (5,006)
Net cash provided by (used in) financing activities | 1,217 | (29,387)
Net decrease in cash, cash equivalents and restricted cash | (32,130) | (77,919)
Cash, cash equivalents and restricted cash
Beginning of period | 166,039 | 187,123
End of period | 133,909 | 109,204

The following table reflects the reconciliation of net income (loss) to Adjusted EBITDA for each of the periods indicated (in thousands):

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are the world's largest online marketplace for authenticated resale luxury goods. We are revolutionizing luxury resale by providing an end-to-end service that unlocks supply from consignors and creates a trusted, curated online marketplace for buyers globally. Since our inception in 2011, we have cultivated a loyal and engaged consignor and buyer base through our investments in our technology platform, logistics infrastructure and people. We offer a wide selection of authenticated, primarily pre-owned luxury goods on our online marketplace bearing the brands of thousands of luxury and premium designers. We offer products across multiple categories including women's and men's fashion, fine jewelry and watches. We have built a vibrant online marketplace that we believe expands the overall luxury market, promotes the recirculation of luxury goods and contributes to a more sustainable world.

We have transformed the luxury consignment experience by removing the friction and pain points inherent in the traditional consignment model. Our growth playbook centers on scalable supply engine, and helps us forge enduring relationships with our consignors. We offer concierge at-home consultation and pickup as well as virtual consultations. Consignors may also drop off items at our luxury consignment offices. Our retail stores provide an alternative location to drop off consigned items and an opportunity to interact with our authentication experts. Consignors may also utilize our complimentary shipping directly to our authentication centers. We leverage our proprietary transactional database and market insights from over 50 million item sales since our inception to deliver optimal pricing and rapid sell-through. For buyers, we offer highly coveted and exclusive authenticated pre-owned luxury goods at attractive values, as well as a high-quality experience befitting the products we offer. Our online marketplace is powered by our proprietary technology platform, including consumer facing applications and purpose-built software that supports our complex, single-SKU inventory management system.

The substantial majority of our revenue is generated by consignment sales. We also generate revenue from other services and direct sales.

• Consignment revenue . When we sell goods through our online marketplace or retail stores on behalf of our consignors, we retain a percentage of the proceeds, which we refer to as our take rate. Take rates vary depending on the total value of goods sold through our online marketplace on behalf of a particular consignor as well as the category and price point of the items. In 2025 and 2024, our overall take rate on consigned goods was 37.7% and 38.4% respectively. The decrease in our take rate was due to sales mix into higher value items. Additionally, we earn revenue from our subscription program, First Look, in which we offer buyers early access to the items we sell in exchange for a monthly fee.

• Direct revenue . When we accept out of policy returns from buyers, or when we make direct purchases from businesses and consignors, we take ownership of goods and retain 100% of the proceeds when the goods subsequently sell through our online marketplace or retail stores.

• Shipping services revenue . When we deliver purchased items to our buyers, we charge shipping fees to buyers for the outbound shipping and handling services. We also generate shipping services revenue from the shipping fees for consigned products returned by our buyers to us within policy. Shipping services revenue is recognized net of immaterial buyer incentives and excludes the effect of sales tax.

We generate revenue from orders processed through our website, mobile app and retail stores. Our omni-channel experience enables buyers to purchase anytime and anywhere. We have a global base of more than 40 million members as of December 31, 2025. A member is any user who has registered an email address on our website or downloaded our mobile app, thereby agreeing to our terms of service.

Factors Affecting Our Performance

To analyze our business performance, determine financial forecasts and help develop long-term strategic plans, we focus on the factors described below. While each of these factors presents significant opportunity for our business, collectively, they also pose important challenges that we must successfully address in order to sustain our growth, improve our operating results and achieve and maintain our profitability.

Consignors and Buyers

Consignor growth and retention . We grow our sales by increasing the supply of luxury goods offered through our consignment online marketplace. We grow our supply both by attracting new consignors and by creating lasting engagement with existing consignors. We generate leads for new consignors through our advertising activity and through the activity of our sales team. Our sales professionals, who are trained and incentivized to identify and source high-quality, coveted luxury goods, convert those leads into active consignors. Our sales professionals form a consultative relationship with consignors and deliver a high-quality, full-service consigning experience. Our existing relationships with consignors allow us to unlock valuable supply across multiple categories, including women's fashion, men's fashion, jewelry and watches.

We measure the ratio of demand versus supply in a given period, which we refer to as our online marketplace sell-through ratio. Sell-through ratio is defined as GMV in the period divided by the aggregate initial value of items added to our online marketplace in the period. In 2025, our online marketplace sell-through ratio was over 80%.

Our growth has been driven in significant part by repeat sales by existing consignors concurrent with growth of our consignor base. In 2025 and 2024, repeat consignors accounted for over 80% of GMV.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The results of operations presented below should be reviewed in conjunction with the financial statements and notes included elsewhere in the Annual Report. Prior year comparisons for 2024 and 2023 are included in "Part II, Item 7 – Management's Discussion and Analysis of Financial Condition and Results of Operations" of our Annual Report on Form 10-K for the fiscal year ended December 31, 2024. The following tables set forth our results of operations (in thousands) and such data as a percentage of revenue for the periods presented:

Year Ended December 31,
2025 | 2024 | 2023
(In thousands)
Revenue:
Consignment revenue | 535,877 | 473,396 | 415,572
Direct revenue | 91,091 | 64,580 | 79,160
Shipping services revenue | 65,877 | 62,508 | 54,572
Total revenue | 692,845 | 600,484 | 549,304
Cost of revenue:
Cost of consignment revenue | 56,582 | 53,801 | 58,120
Cost of direct revenue | 70,682 | 55,809 | 74,343
Cost of shipping services revenue | 48,759 | 43,353 | 40,563
Total cost of revenue | 176,023 | 152,963 | 173,026
Gross profit | 516,822 | 447,521 | 376,278
Operating expenses:
Marketing | 63,251 | 55,256 | 58,275
Operations and technology | 275,916 | 260,827 | 257,041
Selling, general and administrative | 201,589 | 187,737 | 183,793
Restructuring charges | — | 196 | 43,462
Total operating expenses | 540,756 | 504,016 | 542,571
Loss from operations | (23,934) | (56,495) | (166,293)
Change in fair value of warrant liability | (35,769) | (68,167) | —
Gain on extinguishment of debt | 40,785 | 4,177 | —
Interest income | 4,257 | 7,943 | 8,805
Interest expense | (27,701) | (21,384) | (10,701)
Other income, net | 926 | — | —
Loss before provision for income taxes | (41,436) | (133,926) | (168,189)
Provision for income taxes | 363 | 276 | 283
Net loss | (41,799) | (134,202) | (168,472)

Year Ended December 31,
2025 | 2024 | 2023
Revenue:
Consignment revenue | 77 | % | 79 | % | 76 | %
Direct revenue | 13 | 11 | 14
Shipping services revenue | 10 | 10 | 10
Total revenue | 100 | 100 | 100
Cost of revenue:
Cost of consignment revenue | 8 | 9 | 11
Cost of direct revenue | 10 | 9 | 14
Cost of shipping services revenue | 7 | 7 | 7
Total cost of revenue | 25 | 25 | 32
Gross profit | 75 | 75 | 68
Operating expenses:
Marketing | 9 | 9 | 11
Operations and technology | 40 | 43 | 47
Selling, general and administrative | 29 | 31 | 33
Restructuring charges | — | — | 8
Total operating expenses | 78 | 83 | 99
Loss from operations | (3) | (8) | (31)
Change in fair value of warrant liability | (5) | (11) | —
Gain on extinguishment of debt | 6 | 1 | —
Interest income | 1 | 1 | 2
Interest expense | (4) | (4) | (2)
Other income, net | — | — | —
Loss before provision for income taxes | (5) | (21) | (31)
Provision for income taxes | — | — | —
Net loss | (5) | % | (21) | % | (31) | %

Comparison of 2025 and 2024

Consignment Revenue

Year Ended December 31, | Change
2025 | 2024 | Amount | %
(In thousands, except percentage)
Consignment revenue | 535,877 | 473,396 | 62,481 | 13 | %

Consignment revenue increased by $62.5 million, or 13%, in 2025 compared to 2024. The increase in revenue was driven primarily by a 15% increase in consignment GMV in the year ended December 31, 2025.

Our take rate decreased to 37.7% from 38.4% during the year ended December 31, 2025 compared to last year due to sales mix into higher value items.

Direct Revenue

Year Ended December 31, | Change
2025 | 2024 | Amount | %
(In thousands, except percentage)
Direct revenue | 91,091 | 64,580 | 26,511 | 41 | %

Direct revenue increased by $26.5 million, or 41%, in 2025 compared to 2024. The increase was primarily driven by higher sales of items acquired from businesses, individual sellers, and from out of policy returns. Direct revenue as a percentage of total revenue may vary from period to period primarily based on the amount of consignment revenue.

Shipping Services Revenue

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business.

Overview

The RealReal is the world's largest online marketplace for authenticated, resale luxury goods. We are revolutionizing luxury resale by providing an end-to-end service that unlocks supply and creates a trusted, curated online marketplace for buyers globally. Since our inception, we have cultivated a loyal and engaged consignor and buyer base through continuous investment in our technology platform, logistics infrastructure, brand and people.

We offer a wide selection of authenticated, primarily pre-owned luxury goods on our online marketplace bearing the brands of thousands of luxury and premium designers. The top-selling luxury designers on our online marketplace include Cartier, Chanel, Christian Dior, Gucci, Hermès, Louis Vuitton, Prada, Rolex, Saint Laurent, Tiffany & Co., Van Cleef & Arpels and Bvlgari. We offer products across multiple categories including women's fashion, men's fashion, jewelry and watches. We have built a vibrant online marketplace that we believe expands the overall luxury market, promotes the recirculation of luxury goods and contributes to a more sustainable world.

The Company executes against three strategic pillars that amplify one another to drive sustainable, profitable growth. The three components are: unlocking supply through our growth playbook, driving operational efficiency aided by technology, automation, and proprietary data and obsessing over service for buyers and consignors.

A strong network effect drives the growth of our online marketplace. As we bring more consignors onto our platform, we unlock more high-quality, luxury supply, which increases our merchandise assortment and attracts more buyers. This, in turn, increases sales velocity and commissions for our consignors. In addition, a meaningful share of our consignors are buyers and vice versa, which creates a differentiated flywheel that enhances the network effect of our online marketplace.

We operate neighborhood retail stores which are typically 1,800 to 3,500 square feet with items for sale reflecting a selection of the Company's online assortment. These smaller footprint neighborhood stores are located in areas we have identified as having a large amount of potential customers. These stores attract new customers and provide an in person consignment experience for our consignors. In addition, we operate several larger footprint flagship stores in San Francisco, California, Los Angeles, California and New York, New York. Our flagship stores are typically 8,000 to 10,000

square feet with thousands of unique items for sale and are located in highly desirable, densely populated locations with strong foot traffic.

Our Market

The existing luxury resale market is fragmented, difficult to access and laden with counterfeit goods. Primarily due to these challenges, a vast quantity of consignable luxury goods languishes in homes, and buyers can be hesitant to purchase pre-owned luxury goods. We are transforming the luxury resale experience by addressing these challenges.

• We provide a seamless consignment experience enabled by our proprietary technology platform and data. Our sales team, enabled by our proprietary technology and data analytics, provides world-class service, making consignment easy, convenient, reliable and fast. As a result, we unlock luxury supply from first-time consignors, convert consignors who typically consign at local brick-and-mortar shops to our online marketplace and drive high repeat consignment rates. We leverage data from millions of transactions and current market data to optimize pricing and sales velocity for our consignors.

• We offer buyers a vast, yet curated supply of primarily pre-owned luxury goods and instill trust in the buying process. All consigned items are put through our authentication process and thoroughly inspected for quality and condition, which builds trust in our buyer base. This trust drives repeat purchases from our buyer base and instills confidence in first-time buyers to purchase pre-owned luxury goods.

• We also operate store s. Our retail stores are valuable to us in multiple ways as they help us reach higher value consignors and buyers, increase lifetime value, i ncrease average order value, and lower return rates. We also benefit from increased brand awareness that accelerates overall market growth.

Our Competition

We compete with vendors of new and pre-owned luxury goods, including branded luxury goods stores, department stores, traditional brick-and-mortar consignment stores, pawn shops, auction houses, specialty retailers, discount chains, independent retail stores, the online offerings of traditional retail competitors, resale players focused on niche or single categories, as well as technology-enabled marketplaces that may offer the same or similar luxury goods and services that we offer. As the market evolves, new competitors may emerge, including traditional retail competitors who expand their offerings to include resale. We are able to compete for consignors based on our strong market positioning, diverse category and brand offerings, rich data and technology, and advanced authentication capabilities and expertise. Our full service, multi-channel approach provides consignors with convenient consignment options. For more information regarding risks of competitive factors impacting our business, see the information in "Item 1A: Risk Factors".

Our Consignors

By making consignment easy, convenient, reliable and fast for our consignors, we aim to unlock a vast quantity of desirable, high-quality, primarily pre-owned luxury goods. Our sales professionals remove friction from the consignment process and build lasting relationships with our consignors. In 2025, over 80% of our gross merchandise value ("GMV") came from repeat consignors. Our unique service model incentivizes consumers to consign by making the process easy.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
