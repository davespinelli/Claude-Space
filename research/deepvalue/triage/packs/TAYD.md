# Triage pack — TAYD · TAYLOR DEVICES, INC.

_Generated 2026-09-04 23:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TAYD · **Name:** TAYLOR DEVICES, INC.
- **CIK:** 0000096536
- **SIC:** 3569 — General Industrial Machinery & Equipment, NEC
- **Fiscal year end (MM-DD):** 05-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TAYD

**Fetcher warnings for this ticker:** 10-K 2026-08-18: heading split missed Item 1A - Risk Factors

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** TAYLOR DEVICES, INC.
- **CIK:** 96,536 · **SIC:** 3569 (General Industrial Machinery & Equipment, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 60.54 |
| mktcap | $194.9M |
| ev | $204.0M |
| ev_ebit | 27.8x |
| fcf | $4.9M |
| fcf_yield | 2.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 7.1% |
| net_debt | $9.1M |
| net_debt_ebit | 1.2x |
| cash | $905k |
| ltd | $10.0M |
| equity | $72.9M |
| ltd_tag | LineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $41.6M |
| revenue_prior | $46.3M |
| rev_growth | -10.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $7.3M |
| net_income | $8.6M |
| cfo | $7.0M |
| capex | $2.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 3,219,112 |
| shares_py | 3,136,728 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 8.0% |
| r6m | -30.3% |
| off_52w_high | -32.7% |
| adv20 | $2.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.34 |
| r_ev_ebit | 0.30 |
| r_roic | 0.60 |
| r_rev_growth | 0.11 |
| r_buyback | 0.28 |
| score | 0.38 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 348 |

**Screen rationale:** 12-1 momentum 8.0%


## 3. Share count trend

- Shares outstanding: **3,219,112** (CY2025Q4I) vs **3,136,728** prior year (CY2025Q1I)
- Change: **2.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 13,448 sh / $896,878 -> net $-896,878 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 11; transaction rows: 22 (open-market buys 0, sales 8).

| code | rows |
|---|---|
| A | 5 |
| F | 3 |
| M | 6 |
| S | 8 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-08-18_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

The Company is engaged in the design, development, manufacture and marketing of shock absorption, rate control, and energy storage devices for use in various types of machinery, equipment and structures. In addition to manufacturing and selling existing product lines, the Company continues to develop new and advanced technology products. The Company manufactures and sells a group of very similar products that have many different applications for customers. These similar products are included in one of nine categories, namely, Seismic Dampers, Fluidicshoks®, Crane and Industrial Buffers, Self-Adjusting Shock Absorbers, Liquid Die Springs, Vibration Dampers, Machined Springs, Custom Shock and Vibration Isolators, and Custom Actuators. Custom derivations of all of these products are designed and manufactured for many aerospace and defense applications.

Application of Critical Accounting Policies and Estimates

The Company's consolidated financial statements and accompanying notes are prepared in accordance with U.S. generally accepted accounting principles. The preparation of the Company's consolidated financial statements requires management to make estimates, assumptions and judgments that affect the amounts reported. These estimates, assumptions and judgments are affected by management's application of accounting policies, which are discussed in Note 1, "Summary of Significant Accounting Policies," of the Notes to Consolidated Financial Statements and elsewhere in the accompanying consolidated financial statements. As discussed below, our financial position or results of operations may be materially affected when reported under different conditions or when using different assumptions in the application of such policies. In the event estimates or assumptions prove to be different from actual amounts, adjustments are made in subsequent periods to reflect more current information. Management believes the following critical accounting policies affect the more significant judgments and estimates used in the preparation of the Company's consolidated financial statements.

Accounts Receivable

Our ability to collect outstanding receivables from our customers is critical to our operating performance and cash flows. Accounts receivable are stated at an amount management expects to collect from outstanding balances. Management provides for estimated credit losses through a charge to expense and a credit to a valuation allowance based on its assessment of the current status of individual accounts after considering the age of each receivable and communications with the customers involved, historical trends, and forecasted economic conditions. Balances that are collected, for which a credit to a valuation allowance had previously been recorded, result in a current-period reversal of the earlier transaction charging expense and crediting a valuation allowance. Balances that are still outstanding after management has used reasonable collection efforts are written off through a charge to the valuation allowance and a credit to accounts receivable in the current period. The actual amount of accounts written off over the five year

period ended May 31, 2026 were less than 0.1% of sales for that period. The balance of the valuation allowance has decreased from $564,000 at May 31, 2025 to $195,000 at May 31, 2026 due to the full collection of a $751,000 overdue balance at May 31, 2025.

Inventory

Inventory is stated at the lower of average cost or net realizable value. Average cost approximates first-in, first-out cost.

Maintenance and other inventory represent stock that is estimated to have a product life-cycle in excess of twelve-months. This stock represents certain items the Company is required to maintain for service of products sold, and items that are generally subject to spontaneous ordering.

This inventory is particularly sensitive to obsolescence in the near term due to its use in industries characterized by the continuous introduction of new product lines, rapid technological advances, and product obsolescence. Therefore, management of the Company has recorded an allowance for potential inventory obsolescence. Based on certain assumptions and judgments made from the information available at that time, we determine the amount in the inventory allowance. If these estimates and related assumptions or the market changes, we may be required to record additional reserves. Historically, actual results have not varied materially from the Company's estimates. There was $318,000 and $107,000 of inventory disposed of during the years ended May 31, 2026 and 2025, respectively. The provision for potential inventory obsolescence was $225,000 and zero for the years ended May 31, 2026 and 2025, respectively.

Revenue Recognition

Revenue is recognized when, or as, the Company transfers control of promised products or services to a customer in an amount that reflects the consideration to which the Company expects to be entitled in exchange for transferring those products or services.

A performance obligation is a promise in a contract to transfer a distinct good or service to the customer and is the unit of account. A contract's transaction price is allocated to each distinct performance obligation and recognized as revenue when, or as, the performance obligation is satisfied. The majority of our contracts have a single performance obligation as the promise to transfer the individual goods or services is not separately identifiable from other promises in the contracts which are, therefore, not distinct. Promised goods or services that are immaterial in the context of the contract are not separately assessed as performance obligations.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

A summary of the period-to-period changes in the principal items included in the consolidated statements of income is shown below:

Summary comparison of the years ended May 31, 2026 and 2025
Increase /
(Decrease)
Sales, net | $ (4,643,000)
Cost of goods sold | $ (1,512,000)
Research and development costs | $ 332,000
Selling, general and administrative expenses | $ (1,179,000)
Other income | $ 240,000
Income before provision for income taxes | $ (2,044,000)
Provision for income taxes | $ (1,195,000)
Net income | $ (849,000)

For the year ended May 31, 2026 (All figures being discussed are for the year ended May 31, 2026 as compared to the year ended May 31, 2025).

Year ended May 31 | Change
2026 | 2025 | Amount | Percent
Net revenue | $ 41,650,000 | $ 46,293,000 | $ (4,643,000) | -10 %
Cost of goods sold | 23,303,000 | 24,815,000 | (1,512,000) | -6 %
Gross profit | $ 18,347,000 | $ 21,478,000 | $ (3,131,000) | -15 %
… as a percentage of net revenue | 44% | 46%

The Company's consolidated results of operations showed a 10% decrease in net revenue and a 15% decrease in net income. Revenue recorded in the year ended May 31, 2026 for long-term projects was 25% lower than the level recorded in the prior year. We had 40 long-term projects in process during the year ended May 31, 2026 compared with 37 during the same period last year. Revenue recorded in the year ended May 31, 2026 for other than long-term projects (non-projects) was 22% higher than the level recorded in the prior year. The number of long-term projects in process fluctuates from period to period. The changes from the prior year to the year ended May 31, 2026 are not necessarily representative of future results.

Sales of the Company's products are made to three general groups of customers: industrial, structural and aerospace / defense. The Company saw a 31% decrease from last year's level in sales to structural customers who were seeking seismic / wind protection for either construction of new buildings and bridges or retrofitting existing buildings and bridges along with a 1% increase in sales to customers in aerospace / defense and an 11% decrease in sales to customers using our products in industrial applications.

A breakdown of sales to these three general groups of customers, as a percentage of total net revenue for fiscal years ended May 31, 2026 and 2025 is as follows:

Year ended May 31
2026 | 2025
Industrial | 9% | 9%
Structural | 25% | 32%
Aerospace / Defense | 66% | 59%

Total sales within the U.S. were consistent with last year. Total sales to Asia decreased to $3.2 million from $7.0 million last year, while sales to countries outside of the U.S. and Asia decreased $0.7 million from last year. The shift in domestic and international sales concentration from the prior year is attributable to normal changes in structural project activity. Net revenue by geographic region, as a percentage of total net revenue for fiscal years ended May 31, 2026 and 2025 is as follows:

Year ended May 31
2026 | 2025
U.S. | 87% | 79%
Asia | 8% | 15%
Other | 5% | 6%

The gross profit as a percentage of net revenue of 44% in the year ended May 31, 2026 is two percentage points lower than the same period last year (46%).

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-08-18_item1_business.md)

Item 1. Business.

Taylor Devices, Inc. (referred to herein as the "Company," "we," "us" or "our") was incorporated in the State of New York on July 22, 1955 and is engaged in the design, development, manufacture and marketing of shock absorption, rate control, and energy storage devices for use in various types of machinery, equipment and structures. In addition to manufacturing and selling existing product lines, the Company continues to develop new and advanced technology products.

Principal Products

The Company manufactures and sells a group of very similar products that have many different applications for customers. These similar products are included in one of nine categories, namely, Seismic Dampers, Fluidicshoks®, Crane and Industrial Buffers, Self-Adjusting Shock Absorbers, Liquid Die Springs, Vibration Dampers, Machined Springs, Custom Shock and Vibration Isolators, and Custom Actuators. Custom derivations of all of these products are designed and manufactured for many aerospace and defense applications. The following is a summary of the capabilities and applications for these products.

Seismic Dampers are designed to mitigate the effects of earthquakes on structures and represent a substantial portion of the Company's sales. Fluidicshoks® are small, extremely compact shock absorbers with up to 19,200 inch-pound capacities, produced in 12 standard sizes for primary use in the defense, aerospace and commercial industries. Crane and Industrial Buffers are larger versions of the Fluidicshoks® with up to 10,890,000 inch-pound capacities, produced in more than 50 standard sizes for industrial applications on cranes and crane trolleys, truck docks, ladle and ingot cars, ore trolleys and train car stops. Self-Adjusting Shock Absorbers, which include versions of Fluidicshoks® and crane and industrial buffers, automatically adjust to different impact conditions, and are designed for high cycle application primarily in heavy industry. Liquid Die Springs are used as component parts of machinery and equipment used in the manufacture of tools and dies. Vibration Dampers are used primarily by the aerospace and defense industries to control the response of electronics and optical systems subjected to air, ship, or spacecraft vibration. Machined Springs are precisely controlled mechanical springs manufactured from a variety of materials. These are used primarily for aerospace applications that require custom features that are not possible with conventional wound coil springs. Custom Shock and Vibration Isolators are comprised of various configurations including liquid springs, fluid dampers, elastomeric springs and Pumpkin™ Mounts. They are typically used for defense applications. Custom Actuators are typically of the gas-charged type, using high pressure, that have custom features not available from other suppliers. These actuators are used for special aerospace and defense applications.

Sales and Distribution

The Company uses a technical sales force consisting of Company employees for sales in the United States. From time to time, the Company uses the services of non-employee sales representatives for sales throughout the rest of the world. Specialized technical sales in custom marketing activities outside the U.S. are serviced by these sales representatives under the direction and with the assistance of the Company's in-house technical sales staff. Sales representatives typically have non-exclusive agreements with the Company, which, in most instances, provide for payment of commissions on sales at 5% to 10% of the product's net aggregate

selling price. The Company recorded zero non-employee commission expense for both the years ending May 31, 2026 and 2025. A limited number of foreign sales representatives also have non-exclusive agreements with the Company to purchase the Company's products for resale purposes.

Competition

The Company faces some competition for hydraulic energy absorbers on mature aerospace and defense programs. Other competition in these sectors include the use of competing technologies, not necessarily of similar design as the Company's products. For the industrial products group, several foreign companies and two U.S. companies are the Company's main competitors in the production of crane buffers and industrial shock absorbers.

The Company competes directly against three other firms supplying structural damping devices for use in the U.S. For structural applications outside of the U.S., the Company competes directly with several other firms, particularly in Japan and Taiwan. The Company competes with numerous other firms that supply alternative seismic protection technologies.

Raw Materials and Supplies

The principal raw materials and supplies used by the Company in the manufacture of its products are provided by numerous U.S. and foreign suppliers. Management believes that the loss of any one of these suppliers would not have a material adverse effect on the Company.

Dependence Upon Major Customers

Sales to five customers accounted for approximately 45% (11%, 11%, 10%, 8% and 5%, respectively) of our net sales for 2026. Sales to three customers accounted for approximately 42% (21%, 15% and 6%, respectively) of our net sales for 2025. Management believes that the loss of any or all of these customers, unless the business is replaced by the Company, would have a material adverse effect on the Company.

Patents, Trademarks and Licenses

The Company holds 24 patents expiring at different times until the year 2042.

Terms of Sale

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-08-18_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-08-18_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-08-18_item7_mdna.md, 10-K_2026-08-18_item1_business.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
