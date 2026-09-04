# Triage pack — RGR · STURM RUGER & CO INC

_Generated 2026-09-04 21:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** RGR · **Name:** STURM RUGER & CO INC
- **CIK:** 0000095029
- **SIC:** 3480 — Ordnance & Accessories, (No Vehicles/Guided Missiles)
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/RGR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** STURM RUGER & CO INC
- **CIK:** 95,029 · **SIC:** 3480 (Ordnance & Accessories, (No Vehicles/Guided Missiles)) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 37.22 |
| mktcap | $594.7M |
| ev | $564.1M |
| ev_ebit | n/a |
| fcf | $38.5M |
| fcf_yield | 6.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -3.7% |
| net_debt | -$30.7M |
| net_debt_ebit | n/a |
| cash | $30.7M |
| ltd | $0.00 |
| equity | $289.8M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $546.1M |
| revenue_prior | $535.6M |
| rev_growth | 1.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$12.3M |
| net_income | -$4.4M |
| cfo | $54.3M |
| capex | $15.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 15,978,256 |
| shares_py | 16,162,030 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 12.8% |
| r6m | 1.4% |
| off_52w_high | -20.1% |
| adv20 | $4.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.56 |
| r_ev_ebit | 0.00 |
| r_roic | 0.21 |
| r_rev_growth | 0.41 |
| r_buyback | 0.75 |
| score | 0.44 |

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
| rank | 300 |

**Screen rationale:** buying back stock -1.1%; debt data missing (net cash unverified); 12-1 momentum 12.8%


## 3. Share count trend

- Shares outstanding: **15,978,256** (CY2026Q2I) vs **16,162,030** prior year (CY2025Q2I)
- Change: **-1.1%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-04** — Item 5.02 (officer / director change or comp arrangement): of Directors (the "Board") of Sturm, Ruger & Company, Inc., a Delaware corporation (the "Company"), in consultation

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 7,500 sh / $288,615 vs sells 0 sh / $0 -> net $288,615 (BUYING).
Distinct insiders buying (code P): 3. Largest buy: WIDMAN PHILLIP bought 5,000 sh @ $38.00 ($190,000) on 2026-05-12.

Form 4 filings parsed: 12; transaction rows: 20 (open-market buys 3, sales 0).

| code | rows |
|---|---|
| A | 17 |
| P | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Results'; skipped 8 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex99-1.htm)

Second Quarter 2026 Results

Delivered Second Quarter Net Sales of $158.1 Million

Earnings per Share was $0.43, Adjusted Earnings
per Share was $0.52

Generated $17.3 Million of Cash from Operations

Declares Quarterly Dividend of $0.21 Per Share

MAYODAN, NC – July 29, 2026 – Sturm, Ruger &
Company, Inc. (NYSE: RGR) ("Ruger" or the "Company") announced today its financial results for the
second quarter 2026.

Second Quarter 2026 Financial Highlights

· | The Company achieved net sales of $158.1 million, a 19% increase over the $132.5 million achieved in the corresponding period in 2025.

· | Diluted earnings were $0.43 per share compared to $1.05 diluted loss per share in the corresponding period in 2025.

· | On an adjusted basis, diluted earnings for the second quarter of 2026 were $0.52 per share compared to $0.41 per share in the corresponding period in 2025.

· | Average selling price increased 10% to $384 during the quarter, while improved product mix and operational execution contributed to a 4% increase in adjusted gross margin compared to Q2 2025.

· | Net Income Margin for the Quarter was 4.4%. Adjusted EBITDA Margin for the Quarter was 10.5%

During the second quarter, the Company incurred incremental
expenses associated with negotiating and finalizing the Strategic Cooperation Agreement ("Agreement") with Beretta Holding
S.A. ("Beretta Holding"), which was announced on May 4, 2026. The Company incurred legal, professional and advisory fees
and other expenses totaling approximately $1.2 million related to the Agreement negotiations during the quarter. Additionally, there
were one-time expenses related to the transition of the Chief Financial Officer that were incurred in the quarter. These items do not,
in the opinion of management, reflect the underlying performance of the core business.

The Company announced today that its Board of Directors
declared a dividend of $0.21 per share for the second quarter for shareholders of record as of August 14, 2026, payable on August 28,
2026. This dividend equates to approximately 40% of adjusted net income of $0.52 per share for the second quarter of 2026.

The second quarter reflected continued execution
of the Company's 2026 Plan, highlighted by improved operating performance, strong core product demand and the introduction of the Ruger
Business System, establishing the Company's long-term operating framework.

"Our second quarter results demonstrate our
ability to deliver against our strategy," said Todd Seyfert, President and Chief Executive Officer. "We delivered sequential
and year-over-year sales growth, improved bottom-line results and improved manufacturing execution following first quarter production
constraints."

Second Quarter 2026 Operational Highlights

· | The estimated sell-through of the Company's products from the independent distributors to retailers in Q2 2026 increased by 19% from Q2 2025, exceeding a 5% increase in adjusted NICS during the same period.

· | Compared to the second quarter of 2025, the Company's finished goods inventories decreased 100,100 units while distributors' inventories decreased 45,800 units, reflecting strong retail pull through of our new products.

"Adjusted NICS remained above prior-year levels
during the quarter, and Ruger continued to outperform the broader market," Seyfert added. "Improved manufacturing execution
also allowed us to begin rebuilding finished goods inventory, enhancing product availability for our customers while maintaining disciplined
inventory management."

An important milestone during the quarter was the
formal establishment of the Ruger Business System – the operating framework for how the company will plan, execute and continuously
improve performance across the enterprise.

"The establishment of the Ruger Business System
is much more than a new operating process," Seyfert continued. "It creates a common way of working company-wide, aligning
our people around shared objectives, reinforcing accountability and providing the tools and capabilities for successful execution of our
Ruger 2030 strategy, and beyond."

Year-to-Date 2026 Highlights

Through the first six months of 2026, the Company
continued executing its 2026 Plan while strengthening its operational foundation through improved manufacturing performance and disciplined
capital allocation. Other highlights include:

· | The Company achieved net sales of $299.4 million for the period, a 12% increase over the $268.2 million achieved in the corresponding period in 2025.

· | Diluted earnings were $0.44 per share for the period compared to $0.57 diluted loss per share in the corresponding period in 2025.

· | On an adjusted basis, excluding severance costs related to a first quarter reduction-in-force and legal, professional and advisory fees and other expenses related to the stockholder matters, diluted earnings for the first six months of 2026 were $0.79 per share compared to adjusted earnings of $0.87 per share for the first half of 2025. The 2025 adjusted earnings exclude the inventory and related other asset write-off, product rationalization, and organizational realignment incurred in the second quarter of 2025.

· | Sales of new products, including the RXM pistol, Marlin 1894 lever-action rifles, American Centerfire Rifle Generation II, Glenfield rifles, Harrier rifles and the Ruger Red Label III Shotgun, represented $80.9 million, or 29%, of firearm sales for the period. New product sales include only major new products that were introduced in the past two years.

· | Cash generated from operations during the first half of 2026 totaled $36.1 million, compared to $25.9 million in 2025.

· | As of June 27, 2026, Ruger's cash and short-term investments totaled $117.5 million. The Company's current ratio is 3.3 to 1 and there is no debt.

· | For the period, capital expenditures totaled $8.1 million. The Company expects capital expenditures to total approximately $30 million for the year for continued investments in new product introductions, expanded capacity for product lines in greatest demand, upgraded manufacturing capabilities and strengthened facility infrastructure.

· | In the first six months, the Company returned $3.0 million to its shareholders through the payment of quarterly dividends. The Company did not repurchase any shares of its common stock during the period.

"As we reach the midpoint of 2026, we are encouraged
by the progress we've made across the business. While there is still important work ahead, we believe the operational foundation we continue
building positions Ruger to execute with greater consistency, respond more effectively to changing market conditions and create durable
long-term value for our shareholders," Seyfert concluded.

Today, the Company filed its Quarterly Report on
Form 10-Q for the second quarter of 2026. The financial statements included in this Quarterly Report on Form 10-Q are attached to this
press release.

The Quarterly Report on Form 10-Q for the second
quarter of 2026 is available on the SEC website at SEC.gov and the Ruger website at Ruger.com/corporate. Investors are urged to read the
complete Quarterly Report on Form 10-Q to ensure that they have adequate information to make informed investment judgments.

Earnings Call Information

The Company will host a webcast at 4:30pm ET today
to discuss the second quarter 2026 financial results. Participants may access the live webcast via this link or by visiting Ruger.com/corporate.
Those who wish to ask questions during the webcast will need to pre-register prior to the meeting.

About Sturm, Ruger & Co., Inc.

Sturm, Ruger & Co., Inc. is one of the nation's
leading manufacturers of rugged, reliable firearms for the commercial sporting market. With products made in America, Ruger offers consumers
almost 800 variations of 40 product lines, across the Ruger, Marlin and Glenfield brands. For over 75 years, Ruger has been a model of
corporate and community responsibility. Our motto, "Arms Makers for Responsible Citizens ® ," echoes our commitment
to these principles as we work hard to deliver quality and innovative firearms.

CONDENSED CONSOLIDATED BALANCE SHEETS (UNAUDITED)
(Continued)

(Dollars in thousands, except per share data )

June 27, 2026 | December 31, 2025
Liabilities and Stockholders' Equity
Current Liabilities
Trade accounts payable and accrued expenses | 39,061 | 34,122
Contract liabilities with customers | 465 | —
Product liability | 777 | 964
Employee compensation and benefits | 26,727 | 15,023
Workers' compensation | 4,399 | 4,638
Total Current Liabilities | 71,429 | 54,747
Lease liabilities | 1,009 | 1,158
Employee compensation | 1,995 | 2,271
Product liability accrual | 61 | 61
Contingent liabilities | — | —
Stockholders' Equity
Common Stock, non-voting, par value $1:
Authorized shares 50,000; none issued | — | —
Common Stock, par value $1:
2026 – 60,000,000 shares authorized
24,524,481 issued,
15,978,256 outstanding
2025 – 40,000,000 shares authorized
24,490,478 issued,
15,944,253 outstanding | 24,524 | 24,490
Additional paid-in capital | 57,293 | 55,356
Retained earnings | 426,107 | 422,045
Less: Treasury stock – at cost
2026 – 8,546,225 shares
2025 – 8,546,225 shares | (218,131 | (218,131
Total Stockholders' Equity | 289,793 | 283,760
Total Liabilities and Stockholders' Equity | 364,287 | 341,997

STURM, RUGER & COMPANY, INC.

CONDENSED CONSOLIDATED STATEMENTS OF INCOME (LOSS) AND COMPREHENSIVE INCOME
(LOSS) (UNAUDITED)

(Dollars in thousands, except per share
data)

Three Months Ended | Six Months Ended
June 27, 2026 | June 28, 2025 | June 27, 2026 | June 28, 2025
Net firearms sales | 157,679 | 131,567 | 298,575 | 266,762
Net castings sales | 379 | 924 | 839 | 1,467
Total net sales | 158,058 | 132,491 | 299,414 | 268,229
Cost of products sold | 124,316 | 127,345 | 237,594 | 233,188
Gross profit | 33,742 | 5,146 | 61,820 | 35,041
Operating expenses:
Selling | 10,303 | 10,277 | 19,659 | 19,690
General and administrative | 15,810 | 15,585 | 36,481 | 27,595
Total operating expenses | 26,113 | 25,862 | 56,140 | 47,285
Operating income (loss) | 7,629 | (20,716 | 5,680 | (12,244
Other income:
Interest income | 702 | 954 | 1,503 | 1,992
Interest expense | (23 | (22 | (45 | (38
Other income, net | 592 | 396 | 1,688 | 649
Total other income, net | 1,271 | 1,328 | 3,146 | 2,603
Income (loss) before income taxes | 8,900 | (19,388 | 8,826 | (9,641
Income taxes | 1,919 | (2,162 | 1,717 | (183
Net income (loss) and comprehensive income (loss) | 6,981 | (17,226 | 7,109 | (9,458
Basic earnings (loss) per share | 0.44 | (1.05 | 0.45 | (0.57
Diluted earnings (loss) per share | 0.43 | (1.05 | 0.44 | (0.57
Weighted average number of common shares outstanding - Basic | 15,957,073 | 16,370,674 | 15,951,342 | 16,494,828
Weighted average number of common shares outstanding - Diluted | 16,272,905 | 16,370,674 | 16,231,621 | 16,494,828
Cash dividends per share | 0.11 | 0.18 | 0.19 | 0.42

STURM, RUGER & COMPANY, INC.

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS (UNAUDITED)

( Dollars in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-02_item7_mdna.md)

_Extraction: started at the Overview heading._

Company Overview

Sturm, Ruger & Company, Inc. (the "Company")
is principally engaged in the design, manufacture, and sale of firearms to domestic customers. Approximately 99% of sales are from firearms.
Export sales represent approximately 5% of total sales. The Company's design and manufacturing operations are located in the United
States and almost all product content is domestic. The Company's firearms are sold through a select number of independent wholesale
distributors, principally to the commercial sporting market.

The Company also manufactures investment castings
made from steel alloys and metal injection molding ("MIM") parts for internal use in its firearms and for sale to unaffiliated,
third-party customers. Less than 1% of sales are from the castings segment.

Results
of Operations - 2025

Product Demand

The estimated sell-through of the Company's
products from the independent distributors to retailers in 2025 increased 5% from 2024. In 2025, adjusted NICS decreased 4% from 2024.
The increase in the sell-through of the Company's products despite the decrease in adjusted NICS background checks may be attributable
to new product introductions, like the Ruger American Rifle Generation II bolt-action rifles, the Marlin lever-action rifles, Glenfield
and Harrier rifles, and the RXM pistol, which helped offset aggressive promotions, discounts, rebates, and the extension of payment terms
offered by the Company's competitors.

Estimated sell-through from distributors to retailers and total adjusted
NICS background checks:

2025 | 2024 | 2023
Estimated Units Sold from Distributors to Retailers (1) | 1,537,600 | 1,471,300 | 1,406,600
Total Adjusted NICS Background Checks (2) | 14,612,300 | 15,239,000 | 15,848,000

(1) | The estimates for each period were calculated by taking the beginning inventory at the distributors, plus shipments from the Company to distributors during the period, less the ending inventory at distributors. These estimates are only a proxy for actual market demand as they:

· | Rely on data provided by independent distributors that are not verified by the Company,

· | Do not consider potential timing issues within the distribution channel, including goods-in-transit, and

· | Do not consider fluctuations in inventory at retail.

(2) | NICS background checks are performed when the ownership of most firearms, either new or used, is transferred by a Federal Firearms Licensee. NICS background checks are also performed for permit applications, permit renewals, and other administrative reasons.

The adjusted NICS data presented above
was derived by the NSSF by subtracting NICS checks that are not directly related to the sale of a firearm, including checks used for concealed
carry ("CCW") permit application checks as well as checks on active CCW permit databases.

Adjusted NICS data can be impacted by
changes in state laws and regulations and any directives and interpretations issued by governmental agencies.

Orders Received and Ending
Backlog

The Company uses the estimated unit sell-through
of its products from the independent distributors to retailers, along with inventory levels at the independent distributors and at the
Company, as the key metrics for planning production levels.

The units ordered, value of orders received and ending backlog, net
of Federal Excise Tax, for the trailing three years are as follows (dollars in millions, except average sales price):

2025 | 2024 | 2023
Orders Received | 515.8 | 533.3 | 433.8
Average Sales Price of Orders Received | 322 | 377 | 374
Ending Backlog | 285.0 | 252.9 | 229.0
Average Sales Price of Ending Backlog | 524 | 568 | 522

Production

The Company reviews the estimated sell-through
from the independent distributors to retailers, as well as inventory levels at the independent distributors and at the Company, to plan
production levels and manage inventories. These reviews resulted in an increase in total unit production of 6% in 2025 compared to 2024.

Annual
Summary Unit Data

Firearms unit data for orders, production, and
shipments follows:

2025 | 2024 | 2023
Units Ordered | 1,602,700 | 1,414,300 | 1,159,000
Units Produced | 1,456,300 | 1,379,500 | 1,398,200
Units Shipped | 1,504,000 | 1,407,800 | 1,367,500
Average Sales Price | 364 | 377 | 395
Units – Backlog | 543,900 | 445,300 | 438,800

Inventories

The Company's finished goods inventory decreased
by 47,700 units during 2025, while distributor inventories of the Company's
products decreased by 33,500 units during the same period.

Inventory data follows:

2025 | 2024 | 2023
Units – Company Inventory | 67,500 | 115,200 | 143,500
Units – Distributor Inventory (3) | 162,300 | 195,800 | 259,300
Total inventory (4) | 229,800 | 311,000 | 402,800

(3) | Distributor ending inventory as provided by the independent distributors of the Company's products. These numbers do not include goods-in-transit inventory that has been shipped from the Company but not yet received by the distributors.

(4) | This total does not include inventory at retailers. The Company does not have access to data on retailer inventories.

Year ended December 31, 2025, as compared to year ended December
31, 2024:

Net Sales,
Cost of Products Sold, and Gross Profit

Net
sales, c ost of products sold, and gross profit data for the year ended December 31, (dollars in millions):

2025 | 2024 | Change | % Change
Net firearms sales | 543.5 | 532.6 | 10.9 | 2.0 | %
Net casting sales | 2.6 | 3.0 | (0.4 | (14.9 | )%
Total net sales | 546.1 | 535.6 | 10.5 | 1.9 | %
Cost of products sold | 464.9 | 421.2 | 43.7 | 10.4 | %
Gross profit | 81.2 | 114.4 | (33.2 | (29.1 | )%
Gross margin | 14.9% | 21.4% | (6.5 | )% | (30.4 | )%

Firearms sales increased 2%, driven by a 7% increase
in unit shipments, partially offset by the $5.7 million reduction related to the close out of 67,000 units of discontinued models in the
second quarter of 2025. New products represented $169.5 million or 33% of firearms sales in 2025, an increase from $159.3 million or 32%
of firearms sales in 2024. New product sales include only major new products that were introduced in the past two years. In 2025, new
products included the RXM pistol, American Centerfire Rifle Generation II, Marlin 1894 lever-action rifles, Glenfield rifles, Harrier
rifles, and the Ruger Red Label Shotgun, as well as the Super Wrangler revolver, which was only included for a portion of the year.

The decreased gross profit for the year ended
December 31, 2025 is attributable to inventory rationalization write-offs and the aforementioned sales reductions taken in the second
quarter of 2025, $4.3 million of operating costs at the new Hebron facility that was acquired in July, increased

costs
associated with material and technology, a product mix shift toward products with relatively lower margins that remain in relatively stronger
demand and increased sales promotional expenses, partially off-set by favorable deleveraging of fixed costs resulting from increased production .

The decrease in gross margin for the year ended
December 31, 2025 is attributable to the aforementioned factors.

Selling,
General and Administrative

Selling and general and administrative expenses data for the year ended
December 31, (dollars in millions):

2025 | 2024 | Change | % Change
Selling expenses | 39.1 | 38.8 | 0.3 | 0.8%
General and administrative expenses | 54.2 | 44.0 | 10.2 | 23.2%
Other operating expenses | 0.2 | — | 0.2 | 100.0%
Total operating expenses | 93.5 | 82.8 | 10.7 | 12.9%

Selling expenses for the year ended December 31,
2025 were substantially unchanged from 2024, as increases in promotional and marketing initiatives was largely offset by decreases in
spending on industry shows, personnel costs, and shipping expenses.

The increase in general and administrative expenses
for the year ended December 31, 2025 was primarily attributable to expenses incurred due to the Company's leadership transition
and organizational realignment, as well as increased information technologies related expenses and professional fees associated with the
purchase of the Anderson Manufacturing assets and the implementation of the Rights Plan.

Operating (Loss) Income

Operating loss was $12.3 million or 2.3% of sales
in 2025. This is a decrease of $43.9 million from 2024 operating income of $31.6 million or 5.9% of sales.

Other Operating Income (Expense),
Net

Other income data for the year ended December 31, (dollars
in millions):

2025 | 2024 | Change | % Change
Royalty income | 1.4 | 0.8 | 0.6 | 63.5 | %
Interest income | 3.2 | 4.9 | (1.7 | (33.3 | )%
Interest expense | (0.1 | (0.1 | — | (7.8 | )%
Other income, net | 0.6 | 0.5 | 0.1 | 18.9 | %
Other income | 5.1 | 6.1 | (1.0 | (16.1 | )%

The decrease in other income for the year ended
December 31, 2025 was primarily the result of decreases in interest income due to decreased interest rates earned on short-term investments
and other income, partially offset by increased royalty income.

Income
Taxes and Net Income

The
effective income tax rate was 38.7% in 2025 and 19.1% in 2024. The Company's 2025 and 2024 effective tax rates differ from the
statutory federal tax rate due principally to research and development tax credits, state income taxes, and the nondeductibility of certain
executive compensation.

As a result of the foregoing factors, consolidated
net loss was $4.4 million in 2025. This represents a decrease of $35.0 million from 2024 consolidated net income of $30.6 million.

Non-GAAP Financial Measure

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-02_item1_business.md)

PART
I

ITEM
1—BUSINESS

Company
Overview

Sturm, Ruger & Company, Inc. and Subsidiaries
(the "Company") is principally engaged in the design, manufacture, and sale of firearms to domestic customers. Virtually all
of the Company's sales for the year ended December 31, 2025 were from the firearms segment, with less than 1% from the castings
segment. Export sales represent approximately 5% of firearms sales. The Company's design and manufacturing operations are located
in the United States and almost all product content is domestic.

The Company has been in business since 1949 and was
incorporated in its present form under the laws of Delaware in 1969. The Company primarily offers products in four industry product categories
– rifles, pistols, shotguns, and revolvers. The Company's firearms are sold through independent wholesale distributors, principally
to the commercial sporting market.

The Company manufactures and sells investment
castings made from steel alloys and metal injection molding ("MIM") parts for internal use in the firearms segment and has
minimal sales to outside customers. The castings and MIM parts are sold to outside customers, either directly or through manufacturers'
representatives.

For the years ended December 31, 2025, 2024, and
2023, net sales attributable to the Company's firearms operations were $543.5 million, $532.6 million and $540.7 million. The balance
of the Company's net sales for the aforementioned periods was attributable to its castings operations.

Firearms
Products

The Company presently offers firearm products,
under the "Ruger" name and trademark, in the following industry categories:

Rifles | Revolvers
· | Single-shot | · | Single-action
· | Autoloading | · | Double-action
· | Bolt-action
· | Modern sporting | Shotguns
· | Over-under
Pistols
· | Rimfire autoloading
· | Centerfire autoloading

In addition, the Company offers lever-action rifles
under the "Marlin" name and trademark and bolt-action rifles under the "Glenfield" name and trademark.

Most firearms are available in several models
based upon caliber, finish, barrel length, and other features.

Rifles

A rifle is a long gun with spiral grooves cut
into the interior of the barrel to give the bullet a stabilizing spin after it leaves the barrel. Net sales of rifles by the Company accounted
for $338.2 million, $310.2 million, and $306.8 million of total net sales for the years 2025, 2024, and 2023, respectively.

Pistols

A pistol is a handgun in which the ammunition
chamber is an integral part of the barrel and which typically is fed ammunition from a magazine contained in the grip. Net sales of pistols
by the Company accounted for $141.9 million, $135.3 million, and $131.4 million of revenues for the years 2025, 2024, and 2023, respectively.

Revolvers

A revolver is a handgun that has a cylinder that
holds the ammunition in a series of chambers which are successively aligned with the barrel of the gun during each firing cycle. There
are two general types of revolvers, single-action and double-action. To fire a single-action revolver, the hammer is pulled back to cock
the gun and align the cylinder before the trigger is pulled. To fire a double-action revolver, a single trigger pull advances the cylinder
and cocks and releases the hammer. Net sales of revolvers by the Company accounted for $39.2 million, $54.8 million, and $72.5 million
of revenues for the years 2025, 2024, and 2023, respectively.

Shotguns

A shotgun is a long gun with a smooth barrel interior
which fires lead or steel pellets. Sales of shotguns by the Company accounted for approximately $0.1 million of revenues for 2025. Shotgun
sales were de minimis for 2024 and 2023.

Accessories

The Company also manufactures and sells accessories
and replacement parts for its firearms. These sales accounted for $27.4 million, $33.3 million, and $30.0 million of total net sales for
the years 2025, 2024, and 2023, respectively.

Castings
Products

Net sales attributable to the Company's
casting operations (excluding intercompany transactions) accounted for $2.6 million, $3.0 million, and $3.0 million, for 2025, 2024, and
2023, respectively. These sales represented less than 1% of total net sales in each year.

Manufacturing

Firearms

The Company produces some of its pistol models,
most of its revolvers, and some of its rifle models at the Newport, New Hampshire facility. One model of revolver, one model of rifle,
and most of the Company's pistols are produced at the Prescott, Arizona facility. Some rifle models and pistol models are produced
at the Mayodan, North Carolina facility. Some rifle models are manufactured at the Hebron, Kentucky facility, which was acquired in July
2025.

Many of the basic metal component parts of the
firearms manufactured by the Company are produced by the Company's castings segment through precision investment casting and metal injection
molding. See "Manufacturing- Investment Castings and Metal Injected Moldings" below for a description of these processes. The Company
believes that investment castings and MIM parts provide greater design flexibility and result in component parts which are generally close
to their ultimate shape and, therefore, require less machining than processes requiring machining a solid billet of metal to obtain a
part. Through the use of investment castings and MIM parts, the Company endeavors to produce durable and less costly component parts for
its firearms.

All assembly, inspection, and testing of firearms
manufactured by the Company are performed at the Company's manufacturing facilities. Every firearm, including every chamber of every revolver
manufactured by the Company, is test-fired prior to shipment.

Investment
Castings and Metal Injection Moldings

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-02_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-02_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-02_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-03-02_item7_mdna.md, 10-K_2026-03-02_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
