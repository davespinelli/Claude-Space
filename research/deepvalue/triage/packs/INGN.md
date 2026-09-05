# Triage pack — INGN · Inogen Inc

_Generated 2026-09-05 01:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** INGN · **Name:** Inogen Inc
- **CIK:** 0001294133
- **SIC:** 3842 — Orthopedic, Prosthetic & Surgical Appliances & Supplies
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/INGN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Inogen Inc
- **CIK:** 1,294,133 · **SIC:** 3842 (Orthopedic, Prosthetic & Surgical Appliances & Supplies) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 5.45 |
| mktcap | $144.6M |
| ev | $57.4M |
| ev_ebit | n/a |
| fcf | -$13.7M |
| fcf_yield | -9.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -27.2% |
| net_debt | -$87.3M |
| net_debt_ebit | n/a |
| cash | $87.3M |
| ltd | $0.00 |
| equity | $174.9M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $348.7M |
| revenue_prior | $335.7M |
| rev_growth | 3.9% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | -$30.2M |
| net_income | $22.7M |
| cfo | -$11.2M |
| capex | $2.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 26,538,337 |
| shares_py | 27,040,390 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -16.8% |
| r6m | -16.8% |
| off_52w_high | -39.1% |
| adv20 | $1.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.09 |
| r_ev_ebit | 0.00 |
| r_roic | 0.04 |
| r_rev_growth | 0.49 |
| r_buyback | 0.78 |
| score | 0.28 |

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
| rank | 424 |

**Screen rationale:** buying back stock -1.9%; debt data missing (net cash unverified); EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **26,538,337** (CY2026Q2I) vs **27,040,390** prior year (CY2025Q2I)
- Change: **-1.9%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-01** — Item 5.02 (officer / director change or comp arrangement): On June 2, 2026, the Board of Directors ("Board") of Inogen, Inc. (the "Company") appointed Andrew (Andy) Reding to serve as Executive Vice President, Chief Operating Officer ("COO") of the Company, effective July 6, 2026.
- **2026-06-11** — Item 5.02 (officer / director change or comp arrangement): On June 5, 2026, at the annual meeting of stockholders of Inogen, Inc. (the "Company" and the "Annual Meeting"), the Company's stockholders approved the adoption of the Company's Amended and Restated 2023 Equity Incentive Plan (the "Amended and Restated 2023...
- **2026-04-06** — Item 1.01 (Entry into a Material Definitive Agreement): On April 6, 2026, the Board of Directors of (the "Board") of Inogen, Inc. (the "Company") appointed Mr. Vafa Jamali as a member of the Board as a Class I director, effective as of the earlier of (a) the date of the Company's 2026 annual meeting of...
- **2026-04-06** — Item 5.02 (officer / director change or comp arrangement): On April 6, 2026, the Board appointed Vafa Jamali as a Class I director, effective as of the Effective Date, to serve a term expiring at the Company's 2027 annual meeting of stockholders or until his successor is duly elected and qualified.
- **2026-03-30** — Item 5.02 (officer / director change or comp arrangement): On March 24, 2026, the Board of Directors ("Board") of Inogen, Inc. (the "Company") appointed Jason Richardson to serve as Executive Vice President, Chief Financial Officer and Treasurer ("CFO") of the Company, effective April 6, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 10,938 sh / $72,146 -> net $-72,146 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 11 |
| F | 1 |
| M | 2 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Highlights'; skipped 8 forward-looking-statement block(s); 9 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ingn-ex99_1.htm)

Highlights

•
Achieved second quarter 2026 revenue of $95.1 million, representing 3.0% year-over-year growth, including international revenue of $41.3 million, an increase of 14.8% year-over-year.

•
Reported GAAP net loss for the second quarter of 2026 of $3.9 million, compared to a net loss of $4.2 million in the prior-year period.

•
Delivered second quarter 2026 positive adjusted EBITDA of $2.4 million, an increase of 15.2% year-over-year, and generated $2.9 million of positive operating cash flow in the quarter.

•
Raised adjusted EBITDA guidance for the full year 2026 to approximately $4.0 million, representing a 48.1% increase from adjusted EBITDA of $2.7 million reported in 2025 and updated full-year revenue guidance to $355 million to $361 million reflecting approximately 3% growth at the midpoint of the range.

•
Published the Questionnaire for Oxygen Therapy Evaluation (QuOTE) assessment tool in ERJ Open Research, a nine-question questionnaire designed to simplify and standardize Long-Term Oxygen Therapy (LTOT) patient monitoring by assessing symptoms, therapy adherence, side effects, and equipment-related issues during routine clinical visits.

•
Launched the Rove 6 portable oxygen concentrator in Canada, strengthening Inogen's ongoing international market expansion and bringing its best-in-class oxygen therapy technology to approximately two million Canadians diagnosed with chronic obstructive pulmonary disease.

•
Completed enrollment and achieved Last Patient Last Visit (LPLV) for the Simeox H SCOPE Study in China, with statistical analysis results expected in the second half of 2026, marking an important milestone in expanding Simeox H into additional large global markets.

•
Strengthened Inogen's leadership team with the addition of Andy Reding as Chief Operating Officer, whose extensive respiratory care expertise and deep industry experience will support the Company's strategic growth initiatives and expansion of its product portfolio.

Second Quarter 2026 Financial Results

Total revenue in the second quarter of 2026 was $95.1 million, an increase of 3.0% from $92.3 million in the prior-year period, primarily driven by higher demand for portable oxygen concentrators, or POCs, in international markets and the favorable impact of foreign exchange rates. While U.S. sales and rentals remained below the prior-year period, the Company continued to gain traction with U.S. distributors and the expanded product portfolio, reinforcing confidence in its long-term opportunities in the U.S. market.

Total gross margin was 45.5% in the second quarter of 2026 compared to 44.8% in the prior-year period. Adjusted gross margin improved by 65 basis points to 45.6% compared to 44.9% in the prior-year period due to improvements in cost of revenue.

GAAP net loss for the second quarter of 2026 was $3.9 million compared to a net loss of $4.2 million in the prior-year period. Adjusted net loss improved $0.6 million year-over-year to less than $0.1 million in the second quarter of 2026, compared with an adjusted net loss of $0.7 million in the prior-year period.

Adjusted EBITDA was a positive $2.4 million in the second quarter of 2026, compared to a positive $2.1 million in the prior-year period, an improvement of $0.3 million.

Cash, cash equivalents, marketable securities, and restricted cash were $106.8 million as of June 30, 2026, with no debt outstanding. The Company repurchased 1,145,150 shares of its common stock in the first half of 2026 for consideration of $7.5 million under the share repurchase program that was announced in the first quarter of 2026.

Reconciliations of adjusted gross margin, adjusted EBITDA, and adjusted net loss for the three and six months ended June 30, 2026 and 2025 are in the financial schedules that are a part of this press release. An explanation of these non-GAAP financial measures is also included below under the heading "Reconciliation of U.S. GAAP to Non-GAAP Financial Measures."

Third Quarter and Full Year 2026 Financial Outlook

Inogen expects third quarter 2026 revenue to be approximately in line with third quarter 2025 revenue, reflecting the continued U.S. sales channel mix shift as well as the timing impact of select international distributor inventory purchases.

For the full year 2026, Inogen now expects reported revenue in the range of $355 million to $361 million, reflecting approximately 3% growth at the midpoint of the range relative to the Company's 2025 revenue.

The Company now expects full year 2026 adjusted EBITDA of approximately $4.0 million representing a 48.1% increase from $2.7 million reported in 2025.

The Company has not provided a reconciliation of forward-looking Adjusted EBITDA to the most directly comparable GAAP measure because certain items that impact net income are uncertain or outside the Company's control and cannot be reasonably predicted without unreasonable effort.

Quarterly Conference Call Information

On August 6, 2026, the Company will host a conference call at 5:00 p.m. Eastern Time / 2:00 p.m. Pacific Time.

Individuals interested in listening to the conference call may do so by dialing:

U.S. domestic callers (877) 841-3961

Non-U.S. callers (201) 689-8589

Please reference Inogen to join the call. A live audio webcast and archived recording of the conference call will be available to all interested parties through the News / Events page on the Inogen Investor Relations website. This webcast will also be archived on the website for six months.

A replay of the call will be available approximately three hours after the live webcast ends and will be accessible through August 13, 2026. To access the replay, dial (877) 660-6853 or (201) 612-7415 and reference Conference ID: 13761255.

Inogen has used, and intends to continue to use, its Investor Relations website, http://investor.inogen.com/ , as a means of disclosing material non-public information and for complying with its disclosure obligations under Regulation FD.

About Inogen

Inogen, Inc. (Nasdaq: INGN) is a leading global medical technology company offering innovative respiratory products for use in the homecare setting. Inogen supports patient respiratory care by developing, manufacturing, and marketing innovative best-in-class respiratory therapy devices used to deliver care to patients suffering from chronic respiratory conditions. Inogen partners with patients, prescribers, home medical equipment providers, and distributors to make its respiratory therapy products widely available, allowing patients the chance to manage the impact of their disease.

For more information, please visit www.inogen.com .

(amounts in thousands, except share and per share amounts)

Three months ended June 30, | Six months ended June 30,
2026 | 2025 | 2026 | 2025
Revenue
Sales revenue | 83,525 | 79,172 | 155,929 | 147,642
Rental revenue | 11,559 | 13,105 | 24,264 | 26,915
Total revenue | 95,084 | 92,277 | 180,193 | 174,557
Cost of revenue
Cost of sales revenue | 44,949 | 43,469 | 85,126 | 81,552
Cost of rental revenue, including depreciation of $2,475 and $3,017 for the three months ended and $5,103 and $6,051 for the six months ended, respectively | 6,863 | 7,467 | 13,932 | 15,292
Total cost of revenue | 51,812 | 50,936 | 99,058 | 96,844
Gross profit | 43,272 | 41,341 | 81,135 | 77,713
Operating expense
Research and development | 5,871 | 5,209 | 10,968 | 9,243
Sales and marketing | 24,824 | 25,390 | 49,427 | 49,147
General and administrative | 17,673 | 16,871 | 35,172 | 33,108
Total operating expense | 48,368 | 47,470 | 95,567 | 91,498
Loss from operations | (5,096 | (6,129 | (14,432 | (13,785
Other income
Interest income, net | 861 | 1,123 | 1,741 | 2,152
Other income, net | 231 | 701 | 189 | 1,057
Total other income, net | 1,092 | 1,824 | 1,930 | 3,209
Loss before benefit for income taxes | (4,004 | (4,305 | (12,502 | (10,576
Benefit for income taxes | (154 | (153 | (328 | (250
Net loss | (3,850 | (4,152 | (12,174 | (10,326
Other comprehensive (loss) income, net of tax
Change in foreign currency translation adjustment | (350 | 3,926 | (1,195 | 5,781
Change in net unrealized (losses) gains on foreign currency hedging | (142 | 36 | (179 | (696
Less: reclassification adjustment for net gains (losses) included in net loss | 164 | (606 | 201 | (739
Total net change in unrealized gains (losses) on foreign currency hedging | 22 | (570 | 22 | (1,435
Change in net unrealized (losses) gains on marketable securities | (11 | 42 | 6 | 42
Total other comprehensive (loss) income, net of tax | (339 | 3,398 | (1,167 | 4,388
Comprehensive loss | (4,189 | (754 | (13,341 | (5,938
Basic net loss per share attributable to common stockholders (1) | (0.14 | (0.15 | (0.45 | (0.40
Diluted net loss per share attributable to common stockholders (1) (2) | (0.14 | (0.15 | (0.45 | (0.40
Weighted average number of shares used in calculating net loss per share attributable to common stockholders:
Basic shares of common stock | 27,045,095 | 26,962,465 | 27,183,000 | 26,068,421
Diluted shares of common stock | 27,045,095 | 26,962,465 | 27,183,000 | 26,068,421

(1) Reconciliations of net loss attributable to common stockholders basic and diluted can be found in Inogen's Quarterly Report on Form 10-Q for the quarter ended June 30, 2026 to be filed with the Securities and Exchange Commission.

(2) Due to a net loss for the three and six months ended June 30, 2026 and June 30, 2025, diluted loss per share is the same as basic.

Consolidated Balance Sheets

(unaudited)

(amounts in thousands)

June 30, 2026 | December 31, 2025
Assets
Current assets
Cash and cash equivalents | 87,276 | 103,729
Marketable securities | 18,263 | 15,848
Restricted cash | 1,303 | 1,289
Accounts receivable, net | 46,157 | 38,863
Inventories | 28,633 | 25,969
Prepaid expenses and other current assets | 12,504 | 12,601
Total current assets | 194,136 | 198,299
Property and equipment, net | 31,781 | 36,362
Goodwill | 10,395 | 10,698
Intangible assets, net | 27,447 | 30,763
Operating lease right-of-use asset | 14,914 | 16,501
Other assets | 6,899 | 6,002
Total assets | 285,572 | 298,625
Liabilities and stockholders' equity
Current liabilities
Accounts payable and accrued expenses | 39,678 | 33,941
Accrued payroll | 12,796 | 10,629
Warranty reserve - current | 10,414 | 10,116
Operating lease liability - current | 3,253 | 3,163
Deferred revenue - current | 4,723 | 5,503
Income tax payable | — | 183
Total current liabilities | 70,864 | 63,535
Long-term liabilities
Warranty reserve - noncurrent | 17,961 | 18,194
Operating lease liability - noncurrent | 12,541 | 14,313
Deferred revenue - noncurrent | 2,857 | 3,603
Deferred tax liability | 6,485 | 6,749
Total liabilities | 110,708 | 106,394
Stockholders' equity
Common stock | 27 | 27
Additional paid-in capital | 359,519 | 363,545
Accumulated deficit | (187,758 | (175,584
Accumulated other comprehensive income | 3,076 | 4,243
Total stockholders' equity | 174,864 | 192,231
Total liabilities and stockholders' equity | 285,572 | 298,625

Condensed Consolidated Cash Flow

(unaudited)

(amounts in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-27_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

•
Results of operations

•
Liquidity and capital resources

•
Sources of funds

•
Use of funds

•
Non-GAAP financial measures

Critical accounting policies and estimates

Our discussion and analysis of our financial condition and results of operations are based upon our consolidated financial statements which have been prepared in accordance with generally accepted accounting principles in the United States of America, or U.S. GAAP. The preparation of these financial statements requires us to make estimates and judgments that affect the reported amounts of assets and liabilities and related disclosure of contingent assets and liabilities, revenue and expenses at the date of the financial statements. Generally, we base our estimates on historical experience and on various other assumptions in accordance with U.S. GAAP that we believe to be reasonable under the circumstances. Actual results may differ from these estimates and such differences could be material to the financial position and results of operations.

Critical accounting policies and estimates are those that we consider the most important to the portrayal of our financial condition and results of operations because they require our most difficult, subjective or complex judgments, often as a result of the need to make estimates about the effect of matters that are inherently uncertain. Our critical accounting policies and estimates include those related to:

•
revenue recognition; and

•
acquisitions and related acquired intangible assets and goodwill.

Revenue recognition

We generate revenue primarily from sales and rentals of our products. Our products consist of our proprietary line of oxygen concentrators and related accessories. Other revenue primarily comes from service contracts, replacement parts and freight revenue for product shipments.

Revenue is recognized upon transfer of control of promised products or services to customers in an amount that reflects the consideration we expect to receive in exchange for those products or services. Revenue from product sales is generally recognized upon shipment of the product but is deferred for certain transactions when control has not yet transferred to the customer.

Our product is generally sold with a right of return and we may provide other incentives, which are accounted for as variable consideration when estimating the amount of revenue to recognize. Returns and incentives are estimated at the time sales revenue is recognized. The provisions for estimated returns are made based on known claims and estimates of additional returns based on historical data and future expectations. Sales revenue incentives within our contracts are estimated based on the most likely amounts expected on the related sales transaction and recorded as a reduction to revenue at the time of sale in accordance with the terms of the contract. Accordingly, revenue is recognized net of allowances for estimated returns and incentives.

For a fixed price, we also offer a lifetime warranty for direct-to-consumer sales for our oxygen concentrators. The revenue is allocated to the distinct lifetime warranty performance obligation based on a relative stand-alone selling price, or SSP, method. We have vendor-specific objective evidence of the selling price for our equipment. To determine the selling price of the lifetime warranty, we use the best estimate of the SSP for the distinct performance obligation, as the lifetime warranty is neither separately priced nor is the selling price available through third-party evidence. To estimate the selling price associated with the lifetime warranties, management considers the profit margins of service revenue, the average estimated cost of lifetime warranties and the price of extended warranties. Revenue from the distinct lifetime warranty is deferred after the delivery of the equipment and recognized based on an estimated mortality rate over five years, which is the estimated performance period of the contract based on the average patient life expectancy.

Revenue from the sale of our repair services is recognized when the performance obligations are satisfied, and collection of the receivables is probable. Other revenue from the sale of replacement parts is generally recognized when product is shipped to customers.

Freight revenue consists of fees associated with the deployment of products internationally and domestically when expedited freight options are requested or when minimum order quantities are not met. Freight revenue is generally recognized upon shipment of the product but is deferred if control has not yet transferred to the customer. Shipping and handling costs for sold products and rental assets shipped to our customers are included on the consolidated statement of comprehensive income as part of cost of sales revenue and cost of rental revenue, respectively.

The payment terms and conditions of customer contracts vary by customer type and the products and services offered. For certain products or services and customer types, we require payment before the products or services are delivered to the customer. The timing of sales revenue recognition, billing and cash collection results in billed accounts receivable and deferred revenue in the consolidated balance sheet.

Contract liabilities primarily consist of deferred revenue related to lifetime warranties on direct-to-consumer sales revenue when cash payments are received in advance of services performed under the contract. The contract with the customer states the final terms of the sale, including the description, quantity, and price of each product or service purchase.

We elected to apply the practical expedient in accordance with Accounting Standards Codification, or ASC, 606— Revenue Recognition and did not evaluate contracts of one year or less for the existence of a significant financing component. We do not expect any revenue to be recognized over a multi-year period with the exception of revenue related to lifetime warranties.

We recognize equipment rental revenue over the non-cancelable lease term, which is one month, less estimated adjustments, per ASC 842— Leases . We have separate contracts with each patient that are not subject to a master lease agreement with any payor. We evaluate the individual lease contracts at lease inception and the start of each monthly renewal period to determine if there is reasonable assurance that the bargain renewal option associated with the potential capped free rental period would be exercised. Historically, the exercise of such bargain renewal option is not reasonably assured at lease inception and most subsequent monthly lease renewal periods. If we determine that the reasonable assurance threshold for an individual patient is met at lease inception or at a monthly lease renewal period, such determination would impact the bargain renewal period for an individual lease. We would first consider the lease classification (sales-type lease or operating lease) and then appropriately recognize or defer rental revenue over the lease term, which may include a portion of the capped rental period. To date, we have not deferred any amounts associated with the capped rental period. Amounts related to the capped rental period have not been material in the periods presented.

The lease term begins on the date products are shipped to patients and are recorded at amounts estimated to be received under reimbursement arrangements with third-party payors, including Medicare, private payors, and Medicaid. Due to the nature of the industry and the reimbursement environment in which we operate, certain estimates are required to record net revenue and accounts receivable at their net realizable values. Inherent in these estimates is the risk that they will have to be revised or updated as additional information becomes available. Specifically, the complexity of many third-party billing arrangements and the uncertainty of reimbursement amounts for certain services from certain payors may result in adjustments to amounts originally recorded. Such adjustments are typically identified and recorded at the point of cash application, claim denial or account review. Accounts receivables are reduced by an allowance for doubtful accounts which provides for those accounts from which payment is not expected to be received, although product was delivered and revenue was earned. Upon determination that an account is uncollectible, it is written-off and charged to the allowance. Amounts billed but not earned due to the timing of the billing cycle are deferred and recognized in revenue on a straight-line basis over the monthly billing period. For example, if the first day of the billing period does not fall on the first of the month, then a portion of the monthly billing period will fall in the subsequent month and the related revenue and cost would be deferred based on the service days in the following month.

Rental revenue is recognized as earned, less estimated adjustments. Revenue not billed at the end of the period is reviewed for the likelihood of collections and accrued. The rental revenue stream is not guaranteed, and payment will cease if the patient no longer needs oxygen or returns the equipment. Revenue recognized is at full estimated allowable reimbursement rates. Rental revenue is earned for that month if the patient is on service on the first day of the 30-day period commencing on the recurring date of service for a particular claim regardless of whether there is a change in condition or death after that date. In the event that a third-party payor does not accept the claim for payment, the consumer is ultimately responsible for payment for the products and services. We have determined that the balances are collectable at the time of revenue recognition because the patient signs a notice of financial responsibility outlining their obligations.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-27_item1_business.md)

ITEM 1. BUSINESS

General

Inogen, Inc. is a medical technology business that primarily focuses on respiratory health. We develop, manufacture, and market innovative respiratory health products, including portable oxygen concentrators, or POCs, used to deliver supplemental long-term oxygen therapy to patients suffering from chronic respiratory conditions and the Simeox ® product for airway clearance treatment. In addition, we have started distributing the Inogen Voxi ® 5 stationary oxygen concentrator as well as the Aurora ® continuous positive airway pressure, or CPAP, masks in the United States. Our proprietary Inogen One ® and Inogen Rove ® POC systems concentrate the air around the patient to offer a source of supplemental oxygen 24 hours a day, seven days a week with a battery and can be plugged into an outlet when at home, in a car, or in a public place with outlets available. While often used together with stationary oxygen concentrators and oxygen compressed gas tanks, our POCs are designed to reduce the patient's reliance on stationary concentrators and scheduled deliveries of tanks with a finite supply of oxygen, thereby improving patient quality of life and fostering mobility. Our Simeox product is a technology-enabled mucus management device predominantly aimed at serving patients requiring airway clearance, such as those with bronchiectasis – a condition characterized by damaged and widened bronchi that can occur in patients with cystic fibrosis, chronic obstructive pulmonary disease, or COPD, or other chronic respiratory diseases. The Voxi 5 stationary oxygen concentrator is used to provide continuous, long-term oxygen therapy to patients who need supplemental oxygen at home or in clinical settings. The Aurora CPAP masks are used to deliver CPAP therapy through a separate device primarily for treating obstructive sleep apnea, or OSA.

Corporate history

We were incorporated in Delaware on November 27, 2001. On February 14, 2014, we completed an initial public offering of common stock and began trading on the Nasdaq Global Select Market, trading under the ticker symbol "INGN".

We incorporated Inogen Europe Holding B.V., a Dutch limited liability company, on April 13, 2017. On May 4, 2017, Inogen Europe Holding B.V. acquired all issued and outstanding capital stock of MedSupport Systems B.V., or MedSupport, and began operating under the name Inogen Europe B.V. We merged Inogen Europe Holding B.V. and Inogen Europe B.V. on December 28, 2018. Inogen Europe B.V. is the remaining legal entity. We completed the acquisition of New Aera, Inc., or New Aera, on August 9, 2019. On September 14, 2023, we completed the acquisition of all of the issued and outstanding capital stock of Physio-Assist SAS, or Physio-Assist, and its wholly-owned subsidiary PhysioAssist GmbH.

On January 25, 2025, we entered into a Strategic Collaboration Agreement, or the Collaboration Agreement, with Jiangsu Yuyue Medical Equipment & Supply Co., Ltd., or Yuwell. The collaboration with Yuwell has broadened our product portfolio through distribution of certain respiratory products in the United States and select other territories, expanded and enhanced our innovation pipeline through research and development collaboration, and is working to accelerate the entry of our brand into the Chinese market. Pursuant to the Collaboration Agreement, we have started distributing the Inogen Voxi 5 stationary oxygen concentrator as well as the Aurora CPAP masks in the United States, and Yuwell has commenced distributing certain POCs supplied by us in specified countries in the Asia-Pacific region.

The market

Chronic obstructive pulmonary disease

We are focused on oxygen therapy and other opportunities in the global respiratory care market. We believe that our oxygen therapy solutions can help patients with chronic respiratory conditions, including patients with COPD.

COPD is a group of lung diseases including chronic bronchitis and emphysema. The primary risk for developing COPD is smoking, but other factors, including air pollution, secondhand smoke, dust, fumes, and chemical exposures, are also associated with COPD. There is currently no cure for COPD, and it is a progressive and debilitating disease that is characterized by a gradual loss of lung function and airflow limitation that is not fully reversible. The symptoms of COPD can range from chronic cough and sputum production to insufficient levels of oxygen in the blood and severe shortness of breath.

COPD has a huge impact on patients and the healthcare system. According to a report published by the Forum of International Respiratory Societies in 2022, an estimated 200 million people in the world have COPD. The Centers for Disease Control and Prevention, or CDC, in the United States estimates that prevalence of COPD among adults 18 years or older was approximately 6.1% based on CDC data of age-adjusted prevalence of COPD from 2011 to 2021. COPD is a major cause of disability and the sixth leading cause of death according to the CDC. In terms of economic impact, the total annual economic cost from COPD in the United States was projected to be approximately $50 billion with nearly one million COPD emergency department visits each year.

A peer-reviewed article in the New England Journal of Medicine has stated that long-term oxygen therapy has been shown to help COPD patients who have severely low blood oxygen or hypoxemia. Hypoxemic patients are unable to convert oxygen found in the air into the bloodstream in an efficient manner. Over time it can lead to a lack of oxygen in organs and tissues, known as hypoxia, and acute respiratory failure. As COPD progresses into later stages, patients may need long-term oxygen therapy as part of their treatment. Other diseases including long term COVID-19 or congestive heart failure may lead to lower oxygen in the bloodstream and may also benefit from long-term oxygen therapy.

Oxygen therapy

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-27_item7_mdna.md, 10-K_2026-02-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
