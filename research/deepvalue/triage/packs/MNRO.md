# Triage pack — MNRO · MONRO, INC.

_Generated 2026-09-04 22:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MNRO · **Name:** MONRO, INC.
- **CIK:** 0000876427
- **SIC:** 7500 — Services-Automotive Repair, Services & Parking
- **Fiscal year end (MM-DD):** 03-27
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MNRO

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** MONRO, INC.
- **CIK:** 876,427 · **SIC:** 7500 (Services-Automotive Repair, Services & Parking) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 12.60 |
| mktcap | $393.9M |
| ev | $492.8M |
| ev_ebit | 24.6x |
| fcf | $38.8M |
| fcf_yield | 9.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $98.9M |
| net_debt_ebit | 4.9x |
| cash | $9.5M |
| ltd | $108.4M |
| equity | n/a |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.2B |
| revenue_prior | $1.2B |
| rev_growth | -3.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $20.0M |
| net_income | $2.2M |
| cfo | $70.4M |
| capex | $31.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 4.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 31,264,060 |
| shares_py | 29,978,942 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -18.4% |
| r6m | -30.1% |
| off_52w_high | -44.2% |
| adv20 | $13.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.71 |
| r_ev_ebit | 0.36 |
| r_roic | 0.50 |
| r_rev_growth | 0.24 |
| r_buyback | 0.20 |
| score | 0.40 |

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
| rank | 324 |

**Screen rationale:** balanced across factors, no single standout


## 3. Share count trend

- Shares outstanding: **31,264,060** (CY2026Q2I) vs **29,978,942** prior year (CY2025Q2I)
- Change: **4.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 10 |
| D | 2 |
| F | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'First Quarter Results'; skipped 8 forward-looking-statement block(s); 11 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (d66984dex991.htm)

First Quarter Results

Sales for the first quarter
of the fiscal year ending March 27, 2027 ("fiscal 2027") decreased 4.6% to $287.1 million, as compared to sales of $301.0 million for the first quarter of the fiscal year ended March 28, 2026 ("fiscal
2026"). This was primarily driven by a reduction in sales of $9.0 million from the closure of 145 underperforming stores in the first quarter of fiscal 2026, as well as a 1.7% decrease in comparable store sales from continuing store
locations.

Comparable store sales increased 8% for batteries and 1% for front end/shocks and alignments compared to the prior year period. Comparable
store sales decreased 1% for tires and brakes and 5% for maintenance services compared to the prior year period. Please refer to the "Comparable Store Sales" section below for a discussion of how the Company defines comparable store
sales.

Gross margin decreased 50 basis points compared to the prior year period, primarily from higher occupancy costs as a percentage of sales, which
were partially offset by lower technician labor costs as a percentage of sales.

Total operating expenses for the first quarter of fiscal 2027 were $96.7 million, or 33.7% of sales, as
compared to $113.0 million, or 37.5% of sales in the prior year period. The decrease was primarily driven by $17.8 million of lower store closing costs in the first quarter of fiscal 2027, $4.1 million of lower costs from the closure
of 145 underperforming stores in the first quarter of fiscal 2026, and $3.7 million of lower costs incurred in connection with consultants related to the Company's operational improvement plan. These were partially offset by
$4.9 million of increased marketing costs to support the Company's topline and $4.6 million of increased costs at continuing locations, primarily front shop labor.

Operating income for the first quarter of fiscal 2027 was $3.7 million, or 1.3% of sales, as compared to an operating loss of $6.1 million, or -2.0% of sales in the prior year period. Adjusted operating income, a non-GAAP measure, for the first quarter of fiscal 2027 was $2.2 million, or 0.8% of sales, as
compared to adjusted operating income of $14.0 million, or 4.7% of sales in the prior year period. Please refer to the reconciliation of adjusted operating income in the table below for details regarding excluded items in the first quarters of
fiscal 2027 and 2026. Please refer to the "Non-GAAP Financial Measures" section below for a discussion of this non-GAAP measure.

Interest expense was $4.6 million for the first quarter of fiscal 2027, as compared to $4.8 million for the first quarter of fiscal 2026,
principally due to lower weighted average debt, which was driven by a decrease in finance lease obligations related to the Company's store locations.

Income tax expense in the first quarter of fiscal 2027 was $0.2 million, or an effective tax rate of -7.7%,
compared to an income tax benefit of $2.7 million, or an effective tax rate of 24.8% in the prior year period. The year-over-year difference in effective tax rate is primarily related to a decrease in unrecognized tax benefits as well as the
impact from other adjustments, none of which are significant, on the change in pre-tax loss.

Net loss for the
first quarter of fiscal 2027 was $2.1 million, as compared to a net loss of $8.1 million in the same period of the prior year. Diluted loss per share for the first quarter of fiscal 2027 was $.08. This compares to diluted loss per share of
$.28 in the first quarter of fiscal 2026. Adjusted diluted loss per share, a non-GAAP measure, for the first quarter of fiscal 2027 was $.09. This compares to adjusted diluted earnings per share of $.22 in the
first quarter of fiscal 2026. Please refer to the reconciliation of adjusted net (loss) income and adjusted diluted (loss) earnings per share in the tables below for details regarding excluded items in the first quarters of fiscal 2027 and 2026.
Please refer to the "Non-GAAP Financial Measures" section below for a discussion of these non-GAAP measures.

Monro ended the first quarter with 1,115 company-operated stores and 47 franchised locations.

"Our first quarter comparable store sales declined 1.7%, reflecting an operating environment, which continued to challenge the full-service auto
aftermarket. This was driven by lower store traffic as well as consumers that continued to defer higher-ticket spending decisions in tires and brakes and traded-down to lower-cost alternatives in our tire category. However, and importantly, we were
able to hold our tire unit volumes flat, and we believe this allowed us to take market share, both in our tier one tires as well as in our overall tire category in the quarter. We believe that this is a direct result of our promotional effectiveness
and the timely expansion of our tier four tire offerings, which allowed us to meet the needs of our customers across the price spectrum. The effectiveness of our ConfiDrive courtesy inspection process helped us drive average repair order growth in
the quarter. This was driven by meaningful improvements in certain of our higher-margin service categories, including batteries, alignments, and front/end shocks. This performance reinforces that we continue to deliver genuine value to our
full-service customers, even in a difficult spending environment. Importantly, we maintained our marketing investment during the quarter, despite the sales headwinds we faced", said Peter Fitzsimmons, President and Chief Executive Officer.

Fitzsimmons continued, "While we're not satisfied with our results, we remain confident that the operational progress we've made is
building a foundation for improved performance as consumer spending stabilizes."

Financial Position

As of June 27, 2026, the Company had availability under its credit facility of $261.5 million and cash and equivalents of $9.5 million.

First Quarter Fiscal 2027 Cash Dividend

On
June 16, 2026, the Company paid a cash dividend for the first quarter of fiscal 2027 of $.28 per share.

Environmental, Social & Governance (ESG)

Monro recently released its sixth annual ESG Report, which covers fiscal 2026. The report highlights the Company's ESG initiatives, including ongoing
commitments to operational excellence and responsible business practices as the foundation for driving growth, strengthening relationships, and delivering long-term value to stakeholders. The report is available on the Company's corporate
website at corporate.monro.com/esg/default.aspx .

Company Expectations

Monro is not providing fiscal 2027 financial guidance at this time but will provide perspective on its expectations for fiscal 2027 during its earnings
conference call.

Earnings Conference Call and Webcast

The Company will host a conference call and audio webcast on July 29, 2026 at 8:30 a.m. Eastern Time. The conference call may be accessed by dialing 1-800-715-9871 and using the required access code of 4507272. A replay will be available approximately two hours after the recording
through Wednesday, August 12, 2026 and can be accessed by dialing 1-800-770-2030 and using the required access code of
4507272. A replay can also be accessed via audio webcast at the Investors section of the Company's website, located at corporate.monro.com/investors .

About Monro, Inc.

Monro, Inc. (NASDAQ: MNRO) is
one of the nation's leading automotive service and tire providers, delivering best-in-class auto care to communities across the country, from oil changes, tires
and parts installation, to the most complex vehicle repairs. With a focus on sustainable growth, the Company generated approximately $1.2 billion in sales in fiscal 2026. Monro brings customers the professionalism and high-quality service they
expect from a national retailer, with the convenience and trust of a neighborhood garage. Monro's highly trained teammates and certified technicians bring together hands-on experience and state-of-the-art technology to diagnose and address automotive needs every day to get customers back on the road safely. For more
information, please visit corporate.monro.com .

Source: Monro, Inc.

MNRO-Fin

###

MONRO, INC.

Financial Highlights

(Unaudited)

(Dollars and share
counts in thousands)

Quarter Ended Fiscal June
2026 | 2025 | % Change
Sales | 287,129 | 301,035 | (4.6 | )%
Cost of sales, including occupancy costs | 186,734 | 194,129 | (3.8 | )%
Gross profit | 100,395 | 106,906 | (6.1 | )%
Operating, selling, general and administrative expenses | 96,700 | 112,981 | (14.4 | )%
Operating income (loss) | 3,695 | (6,075 | 160.8 | %
Interest expense, net | 4,635 | 4,784 | (3.1 | )%
Other expense (income), net | 1,056 | (158 | 768.4 | %
Loss before income taxes | (1,996 | (10,701 | 81.3 | %
Provision for (benefit from) income taxes | 153 | (2,651 | 105.8 | %
Net loss | (2,149 | (8,050 | 73.3 | %
Diluted loss per share | (0.08 | (0.28 | 71.4 | %
Weighted average number of diluted shares outstanding | 30,145 | 29,967
Number of stores open (at end of quarter) | 1,115 | 1,115

MONRO, INC.

Financial Highlights

(Unaudited)

(Dollars in thousands)

June 27, 2026 | March 28, 2026
Assets
Cash and equivalents | 9,526 | 14,633
Inventory | 156,225 | 155,270
Other current assets | 65,980 | 66,738
Total current assets | 231,731 | 236,641
Property and equipment, net | 239,346 | 241,857
Finance lease and financing obligation assets, net | 142,842 | 148,807
Operating lease assets, net | 179,239 | 175,899
Other non-current assets | 763,348 | 764,773
Total assets | 1,556,506 | 1,567,977
Liabilities and Shareholders' Equity
Current liabilities | 472,873 | 517,837
Long-term debt | 108,435 | 60,000
Long-term finance leases and financing obligations | 184,070 | 193,173
Long-term operating lease liabilities | 159,169 | 156,209
Other long-term liabilities | 49,457 | 49,285
Total liabilities | 974,004 | 976,504
Total shareholders' equity | 582,502 | 591,473
Total liabilities and shareholders' equity | 1,556,506 | 1,567,977

MONRO, INC.

Reconciliation of Adjusted Operating Income

(Unaudited)

(Dollars in Thousands)

Quarter Ended Fiscal June
2026 | 2025
Operating Income (Loss) | 3,695 | (6,075
Consulting costs related to operational improvement plan | 1,009 | 4,722
Transition costs related to back-office optimization | 333 | 571
Costs related to shareholder matters | 80 | —
Store closing costs, net (a) | (2,960 | 14,816
Adjusted Operating Income | 2,157 | 14,034

MONRO, INC.

Reconciliation of Adjusted Net (Loss) Income

(Unaudited)

(Dollars in Thousands)

Quarter Ended Fiscal June
2026 | 2025
Net Loss | (2,149 | (8,050
Pension settlement expense | 1,171 | —
Consulting costs related to operational improvement plan | 1,009 | 4,722
Transition costs related to back-office optimization | 333 | 571
Write-off of debt issuance costs | 221 | 263
Costs related to shareholder matters | 80 | —
Store closing costs, net (a) | (2,960 | 14,816
Provision for (benefit from) income taxes on pre-tax adjustments (b) | 38 | (5,297
Adjusted Net (Loss) Income | (2,257 | 7,025

MONRO, INC.

Reconciliation of Adjusted Diluted (Loss) Earnings Per Share

(Unaudited)

Quarter Ended Fiscal June
2026 | 2025
Diluted Loss Per Share | (0.08 | (0.28
Pension settlement expense | 0.03 | —
Consulting costs related to operational improvement plan | 0.02 | 0.12
Transition costs related to back-office optimization | 0.01 | 0.01
Write-off of debt issuance costs | 0.01 | 0.01
Costs related to shareholder matters | 0.00 | —
Store closing costs, net (a) | (0.07 | 0.37
Adjusted Diluted (Loss) Earnings Per Share | $ (0.09) | 0.22

Note: Amounts may not foot due to rounding.

a) | Amounts include the closing costs and asset write-offs related to the closure of 145 underperforming stores, in accordance with the store closure plan, net of related gains on the sale of owned locations, lease assignments and early lease terminations.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-05-27_item7_mdna.md)

_Extraction: started at the Overview heading._

Executive Overview

We continue to make strategic investments to support our operating and financial model designed to drive sustainable sales and profit growth. We have done this through our investment strategy focused on improving guest experience, enhancing customer-centric engagement, optimizing product and service offerings, and accelerating productivity and team engagement.

Recent Developments

On November 9, 2025, the Board of Directors approved the adoption of a limited-duration shareholder rights plan (The "Rights Plan"), intended to protect the best interests of all Company shareholders and enable them to realize the full potential value of their investment in the Company. The Rights Plan is designed to reduce the likelihood that any entity, person or group would gain control of the Company through the open-market or other accumulation of the Company's shares without appropriately compensating all shareholders for control. The Rights Plan is not intended to prevent or interfere with any attempt to purchase the entire Company. It is also not intended to prevent or interfere with any action with respect to the Company that the Board determines to be in the best interests of the Company and its shareholders. Instead, it will position the Board to fulfill its fiduciary duties on behalf of all shareholders by ensuring that the Board has sufficient time to make informed judgements about any attempts to control or significantly influence the Company. The Rights Plan will encourage anyone seeking to gain a significant interest in the Company to negotiate directly with the Board prior to attempting to control or significantly influence the Company. Pursuant to the Rights Plan, the Company issued one right for each common share outstanding, as of the close of business on November 24, 2025. The rights will initially trade with the Company's common stock and will generally become exercisable only if an entity, person or group acquires beneficial ownership of 17.5% or more of the Company's outstanding shares (the "triggering event"). Under the Rights Plan, any person that owns more than the triggering percentage as of the adoptions of the Rights Plan may continue to own its shares of common stock but may not acquire any additional shares without triggering the Rights Plan. The Rights Plan has a one-year duration, expiring on November 6, 2026. The Board of Directors may consider an earlier termination of the Rights Plan as circumstances warrant. See additional discussion related to the Rights Plan in Note 17 to our consolidated financial statements.

In connection with Mr. Fitzsimmons' appointment as President and Chief Executive Officer as of March 28, 2025, the Company entered into a consulting agreement with AlixPartners, LLP ("AlixPartners") as of March 28, 2025, pursuant to which AlixPartners assessed the Company's operations to develop a plan to improve the Company's financial performance. On December 2, 2025, the Company entered into an employment agreement with Peter Fitzsimmons whereby he will continue to serve as our President and Chief Executive Officer and appointed him as a member of the Board of Directors. Prior to December 2, 2025, Mr. Fitzsimmons served as the President and Chief Executive Officer, pursuant to an engagement letter between the Company and AP Services, LLC, an affiliate of AlixPartners. Following Mr. Fitzsimmons' departure from AlixPartners, on December 23, 2025 the Company and AlixPartners entered into a master service agreement pursuant to which AlixPartners will be able to serve promptly in consulting roles as needed at its standard engagement rates to support the development and implementation of the Company's long-term growth strategy to improve the Company's financial performance. See additional discussion in Note 16 to our consolidated financial statements.

On May 23, 2025, following an evaluation of market segmentation and demographic data specific to geographic areas where our stores are located, our Board of Directors approved a plan to close 145 underperforming stores that we identified to have failed to maintain an acceptable level of profitability (the "Store Closure Plan"). These stores were closed and $14.8 million of closing costs were recorded during the first quarter of fiscal 2026. As of March 28, 2026, the Company had a remaining liability of $3.7 million, representing such costs to be settled in future periods, with $1.8 million and $1.9 million included within Other current liabilities and Other long-term liabilities in our Consolidated Balance Sheets, respectively. We expect these costs to be settled within the next one to five years.

As of March 28, 2026, the Company sold 26 owned stores and related equipment. We received net proceeds of $19.7 million and recorded a net gain of $9.9 million. Additionally, the Company assigned 36 leases to third parties and early terminated 32 leases. We received net proceeds of $5.6 million and recorded a net gain of $12.2 million, which included the derecognition of lease liabilities.

The net gain of $7.3 million was recorded in operating, selling, general and administrative expenses in our Consolidated Statements of Income (Loss) and Comprehensive Income (Loss) for the year ended March 28, 2026. Net store closing costs/net gains on closings represent expected costs to be incurred related to the vacating of stores, utilities, real estate taxes, maintenance, other on-going costs related to the properties, and the disposal of inventory and other store assets, net of gains on early lease terminations, lease assignments and sales of owned locations. See additional discussion in Note 1 to our consolidated financial statements.

Monro, Inc. 2026 Form 10-K | 24

MANAGEMENT'S DISCUSSION AND ANALYSIS

On May 21, 2026, we entered into an amendment (the "Sixth Amendment") to our Credit Facility, which, among other things, amends the terms of certain of the financial and restrictive covenants in the credit agreement to provide us with additional flexibility to operate our business. See additional discussion under Part II , Item 9B , " Other Information ", and Note 6 to our consolidated financial statements.

Economic Conditions

The United States economy has experienced significant inflation and rising energy costs during fiscal 2025 and fiscal 2026 and there are market expectations that consumer prices may remain at elevated levels for a sustained period. In addition, labor availability has continued to be constrained and market labor costs have continued to increase. These conditions may give rise to an economic slowdown, and perhaps a recession, and could further increase our costs and/or impact our revenues. It is unclear whether the current economic conditions and government responses to these conditions, including inflation, rising energy costs, tariffs, changing interest rates, and geopolitical uncertainty, will result in an economic slowdown or recession in the United States. If that occurs, demand for our products and services may further decline, possibly significantly, which may significantly and adversely impact our business, results of operations and financial position.

Financial Summary

Fiscal 2026 included the following notable items:

 Diluted earnings per common share ("EPS") was $0.03.

 Adjusted diluted earnings per common share, a non-GAAP measure, was $0.42.

 Sales decreased 3.2 percent, due to closed stores partially offset by higher comparable store sales.

 Comparable store sales increased 1.4 percent from the prior year.

 Operating income of $20.0 million was 59.4 percent higher than the prior year.

 Adjusted operating income, a non-GAAP measure, was $35.8 million.

 Net income was $2.2 million.

 Adjusted net income, a non-GAAP measure, was $14.0 million.

Earnings Per Common Share | Percent Change
2026 | 2025 | 2026/2025
Diluted earnings (loss) per common share | 0.03 | (0.22) | 113.6 | %
Adjustments | 0.39 | 0.70
Adjusted diluted earnings per common share | 0.42 | 0.48 | (12.5) | %

Adjusted operating income, adjusted net income and adjusted diluted EPS, each of which is a measure not derived in accordance with generally accepted accounting principles in the U.S. ("GAAP"), exclude the impact of certain items. Management believes that adjusted operating income, adjusted net income and adjusted diluted EPS are useful in providing period-to-period comparisons of the results of our operations by excluding certain items that are not part of our core operations, such as consulting costs related to the Company's Operational Improvement Plan, transition costs related to back-office optimization, costs related to shareholder matters, management restructuring/transition costs, store impairment charges, write-off of debt issuance costs, litigation reserve costs, gain on sale of corporate headquarters net of closing and relocation costs, and net of gains (losses) on sales of closed stores, lease assignments and early lease terminations. Reconciliations of these non-GAAP financial measures to GAAP measures are provided beginning on page 28 under "Non-GAAP Financial Measures."

We define comparable store sales as sales for locations that have been opened or owned at least one full fiscal year. We believe this period is generally required for new store sales levels to begin to normalize. Management uses comparable store sales to assess the operating performance of the Company's stores and believes the metric is useful to investors because our overall results are dependent upon the results of our stores. Comparable sales measures vary across the retail industry. Therefore, our comparable store sales calculation is not necessarily comparable to similarly titled measures reported by other companies.

Analysis of Results of Operations

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-05-27_item1_business.md)

Total | 1,115

The typical format for a Monro store is a free-standing building consisting of a sales area, fully equipped service bays and a parts/tires storage area. Most service bays are equipped with above-ground electric vehicle lifts. Individual store sizes, number of bays, and stocking levels vary greatly and are dependent primarily on the availability of suitable store locations, population, demographics, and intensity of competition among other factors.

A certain number of our retail locations also service commercial customers. Our locations that serve commercial customers generally operate consistently with our other retail locations, except that the sales mix for these locations includes a higher number of commercial tires.

As of March 29, 2025, Monro had 1,260 Company-operated stores. On May 23, 2025, following an evaluation of market segmentation and demographic data, our Board of Directors approved a plan to close 145 underperforming Company-operated retail stores, that were subsequently closed during the first quarter of fiscal 2026 (the "Store Closure Plan"). For information, see Part II, Item 7., "Management's Discussion and Analysis of Financial Condition and Results of Operations" of this Form 10-K.

As of March 28, 2026, Monro had two retread facilities, 46 Car-X franchised locations and 1,115 Company-operated stores in 32 states.

Our operations are organized and managed in one operating segment. The internal management financial reporting that is the basis for evaluation to assess performance and allocate resources by our chief operating decision maker consists of consolidated data that includes the results of our retail and commercial locations. As such, our one operating segment reflects how our operations are managed, how resources are allocated, how operating performance is evaluated by senior management, and the structure of our internal financial reporting.

Monro incorporated in New York in 1959. We maintain our corporate headquarters in Fairport, New York.

Monro, Inc. 2026 Form 10-K | 5

BUSINESS

Business Strategy

Our vision is to be America's leading auto and tire service center, trusted by consumers as the best place in their neighborhoods for quality automotive service and tires. We believe that success in this vision will position Monro to deliver consistent and sustainable organic growth as well as lead to strong, long-term financial performance. Specifically, we are committed to seeing this vision executed across all aspects of the business, through the following actions:

• Exceed guest expectations. We will continue to invest in and execute strategic initiatives to improve our guests' in-store experience. This includes leveraging our scale and the strength of our financial position to make critical investments in our business, our technicians and technology, allowing us to further execute on our operational excellence initiatives in 2026.

• Provide consistent value . We intend to be able to offer better value than new car dealers to more price-sensitive consumers. Vehicles generally need more service and repairs as they advance in age. However, as consumers' vehicles age, the consumers' willingness to pay higher prices decreases. Monro's service menu is focused on items that are purchased frequently, like oil changes and other scheduled services, along with higher value services like tires, brakes, and other undercar services. We have rolled out several enhanced offerings, including a walk-in oil service option to provide hassle-free service, which is in addition to our existing online appointment system, and Good, Better, Best oil service package updates to give guests competitively priced options to meet their budgets. We also offer combined tire and related service packages, including installation, alignment, and brake service packages, to better connect tire sales to service categories. Additionally, our tire pricing and category management system allows us to dynamically track demand trends and make rapid adjustments to optimize our tire assortment by leveraging our direct access to tire brands from third-party nationwide distribution networks and express tire delivery programs as well as other tire brands in our tire portfolio to offer the right tires at what we believe are the right price points.

• Build a committed, knowledgeable organization of friendly and professional teammates. We will continue to invest in technology and training to accelerate productivity and team engagement. This includes our data-driven cloud-based store staffing and scheduling software that re-balances our store technician labor to meet customer demand as well as utilizing Monro University, an extensive cloud-based learning curriculum, to provide our employees, referred to as "teammates," with the technical training needed to effectively serve our customers today and into the future.

We are committed to building an omni-channel presence through our primary brand websites to create a seamless buying experience for our customers. With responsive optimized design for mobile users, a streamlined tire search and improved content and functionality, our brand websites better position us to address our customers' needs. These websites, aligned with our primary brand names, help customers search for store locations, access coupons, make service appointments, shop for tires, and access information on our services and products, as well as car care tips. Importantly, they better showcase the solutions we provide to our customers, including our Good, Better, Best product and service packages.

Growth Strategy

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-05-27_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-05-27_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-05-27_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-05-27_item7_mdna.md, 10-K_2026-05-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
