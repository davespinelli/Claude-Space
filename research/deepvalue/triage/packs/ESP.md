# Triage pack — ESP · ESPEY MFG & ELECTRONICS CORP

_Generated 2026-09-04 15:08 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ESP · **Name:** ESPEY MFG & ELECTRONICS CORP
- **CIK:** 0000033533
- **SIC:** 3679 — Electronic Components, NEC
- **Fiscal year end (MM-DD):** 06-30
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ESP

**Fetcher warnings for this ticker:** 10-K 2025-09-16: heading split missed Item 1A - Risk Factors

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ESPEY MFG & ELECTRONICS CORP
- **CIK:** 33,533 · **SIC:** 3679 (Electronic Components, NEC) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 62.56 |
| mktcap | $187.4M |
| ev | $166.3M |
| ev_ebit | 20.5x |
| fcf | $16.6M |
| fcf_yield | 8.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 18.2% |
| net_debt | -$21.2M |
| net_debt_ebit | -2.6x |
| cash | $21.2M |
| ltd | $0.00 |
| equity | $56.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $44.0M |
| revenue_prior | $38.7M |
| rev_growth | 13.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $8.1M |
| net_income | $8.1M |
| cfo | $21.0M |
| capex | $4.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 5.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 2,995,922 |
| shares_py | 2,831,399 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 33.4% |
| r6m | 16.8% |
| off_52w_high | -13.0% |
| adv20 | $1.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.68 |
| r_ev_ebit | 0.45 |
| r_roic | 0.86 |
| r_rev_growth | 0.73 |
| r_buyback | 0.17 |
| score | 0.63 |

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
| rank | 111 |

**Screen rationale:** high ROIC 18.2%; debt data missing (net cash unverified); 12-1 momentum 33.4%


## 3. Share count trend

- Shares outstanding: **2,995,922** (CY2026Q1I) vs **2,831,399** prior year (CY2025Q1I)
- Change: **5.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 11,100 sh / $727,678 -> net $-727,678 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 100 (open-market buys 0, sales 84).

| code | rows |
|---|---|
| G | 4 |
| M | 12 |
| S | 84 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-09-16_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

Net sales for the years ended June 30, 2025 and
2024 were $43,950,872 and $38,736,319, respectively, an approximate 13.5% increase. In general, sales fluctuations within product categories
will occur during a comparable fiscal period as the direct result of product mix, influenced by the duration of specific programs and
the contractual terms of firm orders placed for product and services under those programs including contract value, scope of work and
contract delivery schedules. Deliverables within firm contracts are often subject to delivery schedules which also contributes to sales
fluctuations between comparable periods. Sales in fiscal year 2025 were higher when compared to the prior year primarily attributable
to (i) several large multi-year contracts for shipboard transformers and power distribution panels, (ii) power systems for combat vehicles,
and (iii) power systems for aircraft radar and missile platforms. Additionally, the Company saw increases on build to print sales.
These increases were partially offset by a slight decrease in sales related to our magnetics programs where various contracts had fewer
or no sales in the current reporting period as compared to the same period last year due to order completion or planned customer delivery
schedules.

Gross profits for the years ended June 30, 2025
and 2024 were $12,684,631 and $10,653,060, respectively. Gross profit as a percentage of sales was 28.9% and 27.5%, for the same periods,
respectively. The primary factors in determining the change in gross profit and net income are overall sales levels and product mix. The
gross profits on mature products and build to print contracts are typically higher as compared to products which are still in the engineering
development stage or in early stages of production. In the case of the latter, the Company can incur what it refers to as "loss
contracts," primarily on engineering design contracts in which the Company invests with the objective of developing future product
sales. In any given accounting period, the mix of product shipments between higher margin programs and less mature programs, and expenditures
associated with loss contracts, has a significant impact on gross profit and net income.

The increase in gross profit for the year ended
June 30, 2025 when compared to the same period last year resulted primarily from (i) sales levels and general product mix, (ii) higher
than average profit margins on completed milestone sales, and (iii) non-recurring cost savings related to realized labor efficiencies
and savings on material purchases. Moreover, the gross profit in fiscal year 2024 had been negatively impacted by significant unanticipated
costs incurred on several fixed-priced engineering design contracts and a specific build to print contract, all for power supplies, due
to unforeseen complexities of the designs. These factors did not impact the fiscal year 2025 gross profit. Finally, gross profit
in fiscal year 2025 was increased by an improvement in the overhead rate on shipments. This is attributed to the recorded pension withdrawal
obligation established in the last quarter of fiscal year 2024 that was paid in full during fiscal year 2025. See Financial Statement
Note 7. Pension Expense for further details.

Selling, general and administrative expenses were
$4,557,945 for the fiscal year ended June 30, 2025, an increase of $444,337 compared to the fiscal year ended June 30, 2024. The increase
in spending for the year ended June 30, 2025 compared to the same period in 2024 mainly arose from the temporary increase in employee
compensation costs related to a brief overlap in a few positions requiring a training and transition
period due to retirements that occurred during 2025. In addition, the Company had an increase in ESOP contributions, facility costs due
to the completion of the new building, and travel and entertainment expenses . These increases were offset, in part, by a decrease
in the cost of insurance, conference and training costs, and marketing and advertising costs.

Other income for the fiscal years ended June
30, 2025 and 2024 was $1,601,978 and $755,562, respectively. The increase is due to the increase in interest income resulting from an
increase in investment securities and an increase in fixed interest rates. The Company also received a one-time Capital Investment Grant
in the amount of $300,000 related to the completion of the new building in fiscal 2025. Interest income is a function of the level of
investments and investment strategies that generally tend to be conservative.

The Company's effective tax rate was approximately
16.3% in fiscal year 2025 and approximately 20.3% in fiscal year 2024. The effective tax rate in fiscal 2025 is less than the statutory
tax rate mainly due to the benefit received from stock option exercises, dividends paid on allocated ESOP shares, and a benefit from foreign
derived intangible income, offset in part by permanent differences related to incentive stock options. The effective tax rate in fiscal
2024 is less than the statutory tax rate mainly due to the benefit received from ESOP dividends paid on allocated shares and a benefit
from foreign derived intangible income, offset in part by permanent differences related to incentive stock options.

The Company generated net income for fiscal year
2025 of $8,142,954 or $3.14 and $3.02 per share, basic and diluted, compared to net income of $5,815,140 or $2.34 and $2.29 per share,
basic and diluted, for fiscal year 2024. The increase in net income in the year ended June 30, 2025 compared to the same period in 2024
is primarily attributable to higher sales, a higher gross profit margin percentage, an increase in other income, offset in part, by an
increase in selling, general, and administrative expenses and an increase in the provision for income taxes.

Liquidity and Capital Resources

The Company's working capital is an appropriate
indicator of the liquidity of its business, and during the past two fiscal years, the Company, when possible, has funded all of its operations
with cash flows resulting from operating activities and when necessary, from its existing cash and investments. The Company did not borrow
any funds during the last two fiscal years. Management has available a $3,000,000 line of credit to help fund further growth or working
capital needs, if necessary, but does not anticipate the need for any borrowed funds in the foreseeable future. Contingent liabilities
on outstanding standby letters of credit agreements aggregated to zero at June 30, 2025 and 2024. The existing line of credit was extended
and expires February 28, 2026.

The Company's working capital as of June 30, 2025
and 2024 was approximately $46.9 million and approximately $38 million, respectively. The Company may at times be required to repurchase
shares at the ESOP participants' request at the fair market value. During the years ended June 30, 2025 and 2024, the Company did
not repurchase any shares held by the ESOP. Under existing authorizations from the Company's Board of Directors, as of June 30, 2025,
management is authorized to purchase an additional $783,460 of Company stock.

The table below presents the summary of cash flow
information for the fiscal years indicated:

2025 | 2024
Net cash provided by operating activities | 20,991,372 | 10,595,200
Net cash used in investing activities | (6,938,966 | (7,840,277
Net cash used in financing activities | 458,268 | (1,151,708

Net cash provided by operating activities fluctuates
between periods primarily as a result of differences in sales and net income, provision for income taxes, the timing of the collection
of accounts receivable, purchase of inventory, and payment of accounts payable. The increase in cash provided by operating activities
compared to the prior year primarily relates to an increase in contract liabilities and a decrease in inventory, offset in part, by an
increase in accounts receivable, increase in prepaid expenses and other current assets, and a decrease in accounts payable. Net cash used
in investing activities decreased in the year ended June 30, 2025 as compared to the same period in 2024 due to a decrease in proceeds
received from grant awards and a decrease in additions to property, plant and equipment. This was partially offset by a decrease in the
purchase of investment securities net of proceeds from the sale and maturity of investment securities when compared to the same period
last year. Cash used in financing activities for the year ended June 30, 2025 relates primarily to dividend payments on common stock,
offset in full, by proceeds from the exercise of stock options.

The Company currently believes that
the cash flow generated from operations and when necessary, from cash and cash equivalents, will be sufficient to meet its long-term funding
requirements for the foreseeable future.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-09-16_item1_business.md)

Item 1. | Business

General

Espey Mfg. & Electronics Corp. ("Espey")
is a power electronics design and original equipment manufacturing (OEM) company with a long history of developing and delivering highly
reliable products for use in military and severe environment applications. Design, manufacturing, and testing is performed in our 174,000+
square foot facility located at 233 Ballston Ave., Saratoga Springs, New York. Espey is classified as a "smaller reporting company"
for purposes of the reporting requirements under the Securities Exchange Act of 1934, as amended. Espey's common stock is publicly-traded
on the NYSE American under the symbol "ESP."

Espey began operations after incorporation in
New York in 1928. We strive to remain competitive as a leader in high power energy conversion and transformer solutions through the design
and manufacture of new and improved products by using advanced and "cutting edge" electronics technologies.

Espey is an ISO 9001:2015 and AS9100:2016 certified
manufacturer of power conversion, advanced magnetics and build to specifications provided by the customer "build to print"
products for the rugged industrial and military marketplace. Our primary products are power supplies, power converters, filters, power
transformers, magnetic components, power distribution equipment, UPS systems, and antennas. The applications of these products include
AC and DC locomotives, shipboard power, shipboard radar, airborne power, ground-based radar, and ground mobile power.

Espey services include design and development
to specification, build to specifications provided by the customer "build to print", design services, design studies, environmental
testing services, metal fabrication, painting services, and development of automatic testing equipment. Espey is vertically integrated,
meaning that the Company produces individual components (including inductors), populates printed circuit boards, fabricates metalwork,
paints, wires, qualifies, and fully tests items, mechanically, electrically and environmentally, in house. Portions of the manufacturing
and testing process are subcontracted to vendors from time to time.

In fiscal years ended June 30, 2025 and 2024,
the Company's total sales were $43,950,872 and $38,736,319, respectively. Sales to six customers accounted for 16%, 13%, 12%, 12%, 11%
and 10%, respectively, of total sales in 2025. Sales to five customers accounted for 20%, 18%, 16%, 16% and 11%, respectively, of total
sales in 2024. This concentration level presents significant risk. A loss of one of these customers or programs related to these customers
could significantly impact the financial performance of the Company. Historically, a small number of customers have accounted for a large
percentage of the Company's total sales in any given fiscal year. In some instances, our sales may include shipments to more than
one business unit of a particular customer.

Export shipments in fiscal years 2025 and 2024
were $3,124,820 and $2,350,087, respectively. The increase is primarily due to the increase in shipments on a large power supply contract
in the current year when compared to the same period last year.

Sources of Raw Materials.

The Company has at least two potential sources
of supply for a majority of its raw materials. However, certain components used in its products are available from a single or a limited
number of sources. Despite the risk associated with single or limited source suppliers, the benefits of higher quality goods minimize
and often limit any potential risk and can eliminate problems with part failures during production. At times, replacements are required
to cover obsolete parts.

Ongoing demand in the power electronics industry
across multiple manufacturing sectors continues to create shortages and extended lead times. In some instances, waiting times for certain
components approach a year or more. We adequately factor supplier-provided lead times into internal planning schedules and new customer
quotations. From time to time, we encounter part obsolescence which requires us to identify an alternate part suitable for use. We continue
to work with our customers on strategies to mitigate any adverse impact upon our ability to service their requirements. Factors which
may arise after the placement of the customer's order may cause us to miss projected delivery dates. Inflationary costs are expected
to continue but are not expected to have a significant impact on operating income in fiscal year 2026.

Tariffs on steel and aluminum imports from various
countries continue to be in effect. Although we are not currently experiencing any significant financial or raw material sourcing issues
resulting from the product tariffs, the Company cannot provide any assurance that the existing tariffs, the potential of additional tariffs,
and the associated volatility arising from foreign trade policies, will not have a negative impact on our future earnings by increasing
our raw material prices and augmenting the lead time for the availability of raw materials.

Sales Backlog

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-09-16_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-09-16_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2025-09-16_item7_mdna.md, 10-K_2025-09-16_item1_business.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
