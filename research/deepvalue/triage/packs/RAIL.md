# Triage pack — RAIL · FreightCar America, Inc.

_Generated 2026-09-04 23:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** RAIL · **Name:** FreightCar America, Inc.
- **CIK:** 0001320854
- **SIC:** 3743 — Railroad Equipment
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/RAIL

**Fetcher warnings for this ticker:** 10-K 2026-03-09: heading split missed Item 1A - Risk Factors

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** FreightCar America, Inc.
- **CIK:** 1,320,854 · **SIC:** 3743 (Railroad Equipment) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 7.01 |
| mktcap | $229.9M |
| ev | $264.7M |
| ev_ebit | 7.8x |
| fcf | $31.4M |
| fcf_yield | 13.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | $34.9M |
| net_debt_ebit | 1.0x |
| cash | $63.0M |
| ltd | $97.8M |
| equity | n/a |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $501.0M |
| revenue_prior | $559.4M |
| rev_growth | -10.4% |
| rev_growth_note | share count +71.4% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $33.9M |
| net_income | n/a |
| cfo | $34.8M |
| capex | $3.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 71.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 32,791,280 |
| shares_py | 19,127,412 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -5.7% |
| r6m | -46.7% |
| off_52w_high | -52.6% |
| adv20 | $1.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.81 |
| r_ev_ebit | 0.83 |
| r_roic | 0.50 |
| r_rev_growth | 0.10 |
| r_buyback | 0.02 |
| score | 0.35 |

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
| rank | 367 |

**Screen rationale:** top-quartile FCF yield 13.7%; cheap at 7.8x EV/EBIT; share count +71.4% yoy — growth may be acquisition/issuance-driven, not organic; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **32,791,280** (CY2026Q2I) vs **19,127,412** prior year (CY2025Q2I)
- Change: **71.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +71.4% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-05** — Item 1.01 (Entry into a Material Definitive): of Directors (the "Board") of FreightCar America, Inc., a Delaware corporation (the "Company"), declared a dividend
- **2026-06-16** — Item 5.02 (officer / director change or comp arrangement): On June 10, 2026, the Board of Directors (the "Board") of FreightCar America, Inc. (the "Company") appointed Bradley J. Pickard to the Board as a Class II director, effective June 10, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 12 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'FreightCar America, Inc. Reports Second Quarter 2026 Results'; skipped 8 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (rail-ex99_1.htm)

FreightCar America, Inc. Reports Second Quarter 2026 Results

Exceptional Order Intake and Increasing Market Share Drive Sequential Backlog Growth of 121%

Aftermarket revenue growth of 13% Year over Year; Second Aftermarket acquisition completed following Quarter-End

Operating cash flow of $12.1 million, and Free Cash Flow of $11.3 million, up 43% year over year

CHICAGO, August 3, 2026 – FreightCar America, Inc. (NASDAQ: RAIL) ("FreightCar America" or the "Company"), a diversified manufacturer and supplier of railroad freight cars, railcar parts and components, today reported results for the second quarter ended June 30, 2026.

Second Quarter 2026 Highlights

•
Revenues of $113.1 million, compared to $118.6 million in the second quarter of 2025, with railcar deliveries of 927 units compared to 939 units in the prior year period

•
Aftermarket revenues grew 13% year over year, reflecting continued organic growth in parts and components and the contribution from our recent acquisition

•
Gross margin of 5.5% with gross profit of $6.2 million, inclusive of $2.2 million of workforce realignment costs, compared to gross margin of 15.0% with gross profit of $17.8 million in the second quarter of 2025

•
Recorded a $24.9 million non-cash loss related to share price appreciation accounting on the warrant liability, resulting in a net loss of $30.1 million, or $(0.94) per diluted share, and adjusted net loss of $0.8 million, or $(0.02) per diluted share, compared to adjusted net income of $3.8 million, or $0.11 per diluted share, in the prior year period.

•
Holder exercised outstanding warrants during the quarter, reducing the warrant liability to $14.0 million at June 30, 2026 from $119.4 million at March 31, 2026 and resulting in positive stockholders' equity of $36.2 million.

•
Adjusted EBITDA of $1.2 million, representing a margin of 1.0%, compared to $9.3 million and a margin of 7.8% in the second quarter of 2025

•
Ended the quarter with a backlog of 3,972 units valued at $344 million, reflecting a diversified mix of new railcar builds, conversions and retrofits

"Our second-quarter results reflect two different realities," said Nick Randall, President and Chief Executive Officer of FreightCar America. "Commercially, we delivered one of the strongest order quarters in our recent history, with backlog value increasing 121% sequentially and our share of industry new-railcar orders reaching approximately 45%. Operationally, the production ramp began later than planned due to customer delivery timing, reducing fixed-cost absorption and shifting a portion of expected 2026 deliveries into early 2027."

Randall continued, "We realigned our Castaños operating footprint to the productivity improvements achieved over the past two years, while preserving the installed capacity and critical capabilities required to scale. As a result, we expect to generate approximately $12 million of annualized structural savings, with benefits beginning in the third quarter. Combined with 13% growth in aftermarket revenue and the addition of our second acquisition following quarter-end, we enter the second half with a substantially larger backlog, a lower cost base and a broader presence across the railcar lifecycle."

Fiscal Year 2026 Outlook

The Company has updated its outlook for fiscal year 2026 as follows:

Updated Fiscal 2026 Outlook | Year-over-Year Change at Midpoint of Range
Railcar Deliveries | 3,500 – 3,900 railcars | (10.3)%
Revenue | $410 - $460 million | (13.2)%
Adjusted EBITDA 1 | $36 - $44 million | (2.9)%

1. The Company does not provide a reconciliation of forward-looking Adjusted EBITDA guidance due to the inherent difficulty in forecasting and quantifying adjustments necessary to calculate such non-GAAP measure without unreasonable effort. Material changes to such adjustments, including warrant liability and non-core operating items, could affect future GAAP results.

Mike Riordan, Chief Financial Officer of FreightCar America, added, "Free cash flow rose 43% year over year to $11.3 million, while maintaining solid balance sheet flexibility. We also closed our second aftermarket acquisition in under a year, an immediately accretive addition to our business as we continue to execute on our capital allocation priorities. While our updated full-year outlook reflects the shift in new railcar delivery timing, our lower cost structure and robust order intake support stronger results in the back half. Our long-term growth trajectory and value we are building for the years ahead remain firmly on track."

Second Quarter 2026 Conference Call & Webcast Information

The Company will host a conference call and live webcast on Tuesday, August 4, 2026, at 11:00 a.m. (Eastern Time) to discuss its second quarter 2026 financial results. FreightCar America invites shareholders and other interested parties to listen to its financial results conference call. Teleconference details are as follows:

•
August 4, 2026

•
11:00 a.m. Eastern Time

•
Phone: 1-877-407-0789 or 1-201-689-8562

•
Webcast access: FreightCar America Second Quarter 2026 Earnings Conference Call - 1769392

An audio replay of the conference call will be available beginning at 3:00 p.m. (Eastern Time) on Tuesday, August 4, 2026, until 11:59 p.m. (Eastern Time) on Tuesday, August 18, 2026. To access the replay, please dial (844) 512-2921 or (412) 317-6671. The replay passcode is 13761654. An archived version of the webcast will also be available on the FreightCar America Investor Relations website.

About FreightCar America

FreightCar America, headquartered in Chicago, Illinois, is a leading designer, producer and supplier of railroad freight cars, railcar parts and components. We also specialize in railcar repairs, complete railcar rebody services and railcar conversions that repurpose idled rail assets back into revenue service. Since 1901, our customers have trusted us to build quality railcars that are critical to economic growth and instrumental to the North American supply chain. To learn more about FreightCar America, visit www.freightcaramerica.com .

(In thousands, except for share data)

(Unaudited)

June 30, 2026 | December 31, 2025
Assets
Current assets
Cash, cash equivalents and restricted cash equivalents | 62,978 | 64,295
Accounts receivable, net | 13,215 | 12,443
VAT receivable | 6,665 | 6,097
Inventories, net | 57,831 | 68,295
Prepaid expenses and other current assets | 10,226 | 8,875
Total current assets | 150,915 | 160,005
Property, plant and equipment, net | 28,384 | 30,969
Right of use asset lease | 39,381 | 40,281
Intangibles, net | 4,491 | 4,877
Deferred income taxes | 52,053 | 52,970
Other long-term assets | 872 | 947
Total assets | 276,096 | 290,049
Liabilities and Stockholders' Equity (Deficit)
Current liabilities
Accounts and contractual payables | 63,177 | 55,671
Accrued payroll and other employee costs | 5,803 | 9,110
Accrued warranty | 1,989 | 2,050
Deferred revenue | 3,046 | 539
Current portion of long-term debt | 2,875 | 9,728
Lease liability, current | 1,990 | 1,888
Other current liabilities | 4,390 | 6,611
Total current liabilities | 83,270 | 85,597
Long-term debt, net of current portion | 97,850 | 97,514
Warrant liability | 13,977 | 168,529
Accrued pension costs | 1,292 | 1,256
Lease liability, long-term | 42,205 | 43,233
Other long-term liabilities | 1,301 | 1,333
Total liabilities | 239,895 | 397,462
Stockholders' equity (deficit)
Common stock | 358 | 221
Additional paid-in capital | 204,519 | 72,557
Accumulated other comprehensive income | 2,293 | 2,324
Accumulated deficit | (170,969 | (182,515
Total stockholders' equity (deficit) | 36,201 | (107,413
Total liabilities and stockholders' equity (deficit) | 276,096 | 290,049

FreightCar America, Inc.

Condensed Consolidated Statements of Operations

(In thousands, except for share and per share data)

(Unaudited)

Three Months Ended | Six Months Ended
June 30, | June 30,
2026 | 2025 | 2026 | 2025
Revenues | 113,138 | 118,623 | 177,446 | 214,913
Cost of sales | 106,967 | 100,802 | 160,465 | 182,698
Gross profit | 6,171 | 17,821 | 16,981 | 32,215
Selling, general and administrative expenses | 10,467 | 10,114 | 21,871 | 20,637
Operating (loss) income | (4,296 | 7,707 | (4,890 | 11,578
Interest expense | (3,045 | (4,382 | (6,421 | (8,718
(Loss) gain in fair market value of warrant liability | (24,889 | (47,630 | 24,215 | 5,258
Other (expense) income | (218 | 3,296 | (24 | 3,157
(Loss) income before income taxes | (32,448 | (41,009 | 12,880 | 11,275
Income tax (benefit) provision | (2,345 | (52,688 | 1,334 | (50,852
Net (loss) income | (30,103 | 11,679 | 11,546 | 62,127
Net (loss) earnings per common share - basic | (0.94 | 0.36 | 0.35 | 1.89
Net (loss) earnings per common share - diluted | (0.94 | 0.34 | 0.32 | 1.79
Weighted average common shares outstanding – basic | 31,939,312 | 31,793,746 | 31,933,492 | 31,727,903
Weighted average common shares outstanding – diluted | 31,939,312 | 33,398,330 | 35,549,254 | 33,603,627

FreightCar America, Inc.

Condensed Consolidated Segment Information

(In thousands)

(Unaudited)

Three Months Ended | Three Months Ended
June 30, 2026 | June 30, 2025
Manufacturing | Aftermarket | Total | Manufacturing | Aftermarket | Total
Revenues | 104,282 | 8,856 | 113,138 | 110,757 | 7,866 | 118,623
Cost of sales | 101,000 | 5,967 | 95,831 | 4,971
Segment gross profit | 3,282 | 2,889 | 6,171 | 14,926 | 2,895 | 17,821
Other segment items (1) | 599 | 946 | 402 | 510
Segment income | 2,683 | 1,943 | 4,626 | 14,524 | 2,385 | 16,909

(1) Other segment items in Manufacturing and Aftermarket segments include selling, general and administrative expenses.

Six Months Ended | Six Months Ended
June 30, 2026 | June 30, 2025
Manufacturing | Aftermarket | Total | Manufacturing | Aftermarket | Total
Revenues | 157,238 | 20,208 | 177,446 | 200,932 | 13,981 | 214,913
Cost of sales | 146,637 | 13,828 | 173,896 | 8,802
Segment gross profit | 10,601 | 6,380 | 16,981 | 27,036 | 5,179 | 32,215
Other segment items (1) | 963 | 1,895 | 759 | 1,076
Segment income | 9,638 | 4,485 | 14,123 | 26,277 | 4,103 | 30,380

(1) Other segment items in Manufacturing and Aftermarket segments include selling, general and administrative expenses.

FreightCar America, Inc.

Condensed Consolidated Statements of Cash Flows

(In thousands)

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-09_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

OVERVIEW

You should read the following discussion in conjunction with our consolidated financial statements and related notes included elsewhere in this Annual Report on Form 10-K. This discussion contains forward-looking statements that are based on management's current expectations, estimates and projections about our business and operations. Our actual results may differ materially from those currently anticipated and expressed in such forward-looking statements. See "Forward-Looking Statements."

We are a diversified manufacturer of railcars and railcar components. We design and manufacture a broad variety of railcar types for transportation of bulk commodities and containerized freight products primarily in North America. We also provide railcar rebody and repair services, railcar conversion services that repurpose idled rail assets back into revenue service, and supply railcar parts. We have been manufacturing railcars since 1901.

The Company's operations consist of two operating and reportable segments, Manufacturing and Aftermarket. The Company identifies reportable segments based on differences in products and services. The Company's Manufacturing segment includes new railcar manufacturing, used railcar sales, and major conversions and rebodies. The Company's Aftermarket segment includes the selling of forged, cast and fabricated railcar parts, replacement components and other supplies for all railcar types, and provides aftermarket services including safety training, railcar inspections, and preventative maintenance.

Our Manufacturing segment revenues are generated primarily from sales of the railcars that we manufacture. Our Manufacturing segment sales depend on industry demand for new railcars, which is driven by overall economic conditions and the demand for railcar transportation of various products such as steel products, minerals, cement, motor vehicles, forest products, agricultural commodities and coal. Our Manufacturing segment sales are also affected by competitive market pressures that impact our market share, the prices for our railcars and by the types of railcars sold. Our Manufacturing segment revenues also include revenues from railcar conversions and rebodies. Our Aftermarket segment revenues are generated primarily from sales of railcar replacement parts and other supplies for all railcar types.

The variable purchase patterns of our customers and the timing of completion, delivery and customer acceptance may cause our revenues and income from operations to vary substantially each quarter, which will result in significant fluctuations in our quarterly results. Further, recent changes to United States and foreign trade policies, including the imposition of new tariffs, have created increased geopolitical and macroeconomic uncertainty. Future changes in governmental and economic policies could impact our cost

structure, demand for our products and results of operation. We continue to actively monitor new global trade policies and remain focused on strategic initiatives to drive operational efficiencies.

Total net railcar orders received for the year ended December 31, 2025 were 3,254 railcars, consisting of 2,454 new railcars and 800 converted and rebodied railcars, compared to orders for 4,245 units in the year ended December 31, 2024, consisting of 2,850 new railcars and 1,395 converted and rebodied railcars. Total backlog of unfilled orders decreased from 2,797 railcars as of December 31, 2024 to 1,926 railcars as of December 31, 2025. The estimated sales value of the backlog was $137 million and $267 million, respectively, as of December 31, 2025 and 2024.

RESULTS OF OPERATIONS

Year Ended December 31, 2025 compared to Year Ended December 31, 2024

Revenues

Our consolidated revenues for the year ended December 31, 2025 were $501.0 million compared to $559.4 million for the year ended December 31, 2024. Manufacturing segment revenues for the year ended December 31, 2025 were $473.9 million compared to $541.2 million for the year ended December 31, 2024. The decrease in Manufacturing segment revenues for 2025 compared to 2024

reflects a decrease in the number of railcars delivered from 4,362 railcars in 2024 to 4,125 railcars in 2025. Aftermarket segment revenues for the year ended December 31, 2025 were $27.1 million compared to $18.2 million for the year ended December 31, 2024, reflecting increased volume of component sales during the year ended December 31, 2025.

Gross Profit

Our consolidated gross profit for the year ended December 31, 2025 was $73.2 million compared to $67.0 million for the year ended December 31, 2024. Consolidated gross margin was 14.6% for the year ended December 31, 2025 compared to 12.0% for the year ended December 31, 2024. Manufacturing segment gross profit for the year ended December 31, 2025 was $63.8 million compared to $58.4 million for the year ended December 31, 2024. The $6.2 million increase in consolidated gross profit and $5.4 million increase in Manufacturing segment gross profit is primarily due to favorable product mix in the cars delivered during the period. Aftermarket segment gross profit for the year ended December 31, 2025 was $9.4 million compared to $8.6 million for the year ended December 31, 2024. The $0.8 million increase in Aftermarket segment gross profit is primarily due to favorable volume.

Selling, General and Administrative Expenses

Consolidated selling, general and administrative expenses for the year ended December 31, 2025 were $39.3 million compared to $32.9 million for the year ended December 31, 2024. Consolidated selling, general and administrative expenses for the year ended December 31, 2025 included increases of $5.5 million in professional services expenses and $0.5 million in stock-based compensation expenses. Consolidated selling, general and administrative expenses were 7.8% and 5.9% of revenue for the years ended December 31, 2025 and December 31, 2024, respectively. Manufacturing segment selling, general and administrative expenses for the year ended December 31, 2025 were $1.6 million compared to $2.0 million for the year ended December 31, 2024. Manufacturing segment selling, general and administrative expenses for the year ended December 31, 2025 were 0.3% of revenue compared to 0.4% of revenue for the year ended December 31, 2024. Aftermarket segment selling, general and administrative expenses for the year ended December 31, 2025 were $2.2 million compared to $1.5 million for the year ended December 31, 2024. Corporate selling, general and administrative expenses were $35.5 million for the year ended December 31, 2025 compared to $29.5 million for the year ended December 31, 2024. Corporate selling, general and administrative expenses for the year ended December 31, 2025 were primarily driven by the aforementioned increases in professional services expenses and stock-based compensation.

Litigation Settlement

During the year ended December 31, 2025, we did not record any litigation settlements. During the year ended December 31, 2024, we recorded a pre-tax litigation settlement gain of $3.2 million related to a dispute with a former lessee of our railcars.

Operating Income

Our consolidated operating income for the year ended December 31, 2025 was $33.9 million compared to consolidated operating income of $37.3 million for the year ended December 31, 2024 driven primarily by the previously mentioned favorable product mix and no litigation settlement gains recognized in 2025, offset by the previously mentioned increase in selling, general and administrative expenses.

Operating income for the Manufacturing segment was $62.2 million for the year ended December 31, 2025 compared to operating income of $59.6 million for the year ended December 31, 2024, reflecting the favorable product mix during the year ended December 31, 2025. Operating income for the Aftermarket segment was $7.2 million for each of the years ended December 31, 2025 and 2024.

Corporate operating loss was $35.5 million for the year ended December 31, 2025 compared to $29.5 million for the year ended December 31, 2024, reflecting the increases in professional services expenses, stock-based compensation, and professional services expenses during the year ended December 31, 2025.

Interest Expense

Interest expense was $17.6 million for the year ended December 31, 2025 compared to $6.9 million for the year ended December 31, 2024. The increase is driven by the Term Loan agreement entered on December 31, 2024 (the "Term Loan"). See Note 11 - Debt Financing and Credit Facilities.

Loss on Change in Fair Market Value of Warrant Liability

Loss on change in fair market value of warrant liability was $32.2 million for the year ended December 31, 2025 compared to $99.5 million for the year ended December 31, 2024. The change in fair market value of warrant liability is driven by the fluctuation of the stock price used to remeasure the liability at the end of each period.

Other Income (Expense)

Other income was $5.0 million for the year ended December 31, 2025, compared to other expense of $1.0 million for the year ended December 31, 2024. The increase in other income is primarily driven by the $3.3 million Employee Retention Credit received during the year ended December 31, 2025 and the $2.1 million bargain purchase gain associated with the Carly Railcar Components, LLC ("CRC") acquisition.

Income Taxes

Our income tax benefit was $49.0 million for the year ended December 31, 2025 compared to income tax provision of $5.8 million for the year ended December 31, 2024. The income tax benefit is primarily attributable to the release of a majority of a valuation allowance U.S. on federal deferred tax assets. Our effective tax rate for the year ended December 31, 2025 was 450.46% compared to (8.34)% for the year ended December 31, 2024.

Net Income (Loss)

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-09_item1_business.md)

Item 1. Business .

OVERVIEW

FreightCar America, Inc., a Delaware corporation ("FreightCar"), with its subsidiaries (the "Company", "we", "us", or "our" refers to FreightCar and its subsidiaries), is a diversified manufacturer and supplier of railcars and railcar components. We design and manufacture a broad variety of railcar types for transportation of bulk commodities and containerized freight products primarily in North America. We also provide railcar rebody and repair services, railcar conversion services that repurpose idled rail assets back into revenue service, and supply railcar parts. We have been manufacturing railcars since 1901.

Our primary customers are financial institutions and shippers, which represented 78% and 16%, respectively, of our total sales attributable to each type of customer for the year ended December 31, 2025. In the year ended December 31, 2025, we delivered 4,125 railcars, comprised of 3,714 new railcars and 411 rebuilt railcars, compared to 4,362 railcars, comprised of 4,252 new railcars and 110 rebuilt railcars, delivered in the year ended December 31, 2024. Our total backlog of firm orders for railcars decreased from 2,797 railcars as of December 31, 2024 to 1,926 railcars as of December 31, 2025. Our backlog as of December 31, 2025 includes a variety of railcar types and the estimated sales value of the backlog is $137 million.

Our website is www.freightcaramerica.com. We make available, free of charge, on or through our website items related to corporate governance, including, among other things, our corporate governance guidelines, charters of various committees of our Board of Directors (the "Board") and our code of business conduct and ethics. Our annual reports on Form 10-K, quarterly reports on Form 10-Q and current reports on Form 8-K, and amendments thereto, are available on our website and on the SEC's website at www.sec.gov. Any stockholder of our company may also obtain copies of these documents, free of charge, by sending a request in writing to Investor Relations at FreightCar America, Inc., 125 South Wacker Drive, Suite 1500, Chicago, Illinois 60606.

The information contained in or accessible through our website is not incorporated by reference into and is not a part of this Annual Report on Form 10-K.

OUR PRODUCTS AND SERVICES

We design and manufacture a broad variety of freight cars including box cars, covered hoppers, open top hoppers, gondolas, intermodal and non-intermodal flat cars that transport numerous types of dry bulk and containerized freight products.

In the last seven years, we have added nearly 50 new or redesigned products to our portfolio, including box cars in 50' and 60' lengths; various covered hopper cars with cubic capacities from 3,282 to 6,500 cubic feet; open top hopper car designs for ballast, ore and coke with manual or automatic door systems; VersaFlood II ™ open top hoppers in all steel and hybrid configurations (aluminum/stainless steel) with a patented automatic door system; 52' and 66' mill gondolas in multiple cubic capacities; rotary and non-rotary aggregate gondolas; triple hoppers in all steel and hybrid configurations; intermodal flats (including single unit, 2 unit and 3 unit, 53' well cars) and non-intermodal flat cars including 64' - 89' length for general purpose, steel slab (hot and cold); and bulkhead flats. Focused product development activity continues in areas where we can leverage our technical knowledge base and capabilities to realize market opportunities.

The types of railcars listed below include the major types of railcars that we are capable of manufacturing. We rebuild and convert railcars and sell forged, cast and fabricated parts for all of the railcars we produce, as well as those manufactured by others. Many of our railcars are produced using a patented one-piece center sill, the main longitudinal structural component of the railcar. In addition to railcars designed for use in North America, we have manufactured railcars for export to Latin America and the Middle East. Railroads outside of North America are constructed with a variety of track gauges that are sized differently than in North America, which requires us, in some cases, to alter our manufacturing specifications accordingly.

Any of the railcar types listed below may be further developed to meet the characteristics of the materials being transported and customer specifications.

•
VersaFlood Hopper Cars . The VersaFlood™ product series offers versatile design options for transportation of aggregates, sand or minerals. Our VersaFlood™ series open-top hopper railcars include steel, stainless steel or hybrid steel and aluminum-bodied designs equipped with three-pocket (transverse gate) or two-pocket (longitudinal gate) discharge door systems with manual, independent or fully automatic door operation.

•
Covered Hopper Cars . Our covered hopper railcar product offerings encompass a wide range of cubic foot ("cf") capacity designs for shipping dry bulk commodities of varying densities including: 3,282 cf covered hopper cars for cement, sand and roofing granules; 4,300 cf covered hopper cars for potash or similar commodities; 5,200 cf, 5,400 cf, 5,450 cf, 5,700 cf and 5,800 cf-covered hopper cars for grain and other agricultural products; and 5,850 cf and 6,500 cf covered hopper cars for plastic pellets.

•
DynaStack Series . Our intermodal doublestack railcar product offering includes the DynaStack  articulated 3-unit, 53' well cars for transportation of international and domestic containers.

•
Steel Products Cars . Our portfolio of railcar types also includes 52' and 66' mill gondola railcars used to transport steel products and scrap; slab, hot slab and coil steel railcars designed specifically for transportation of steel slabs and coil steel products, respectively.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-09_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-09_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-03-09_item7_mdna.md, 10-K_2026-03-09_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
