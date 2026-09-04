# Triage pack — MAGN · Magnera Corp

_Generated 2026-09-04 18:10 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MAGN · **Name:** Magnera Corp
- **CIK:** 0000041719
- **SIC:** 2621 — Paper Mills
- **Fiscal year end (MM-DD):** 09-26
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MAGN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Magnera Corp
- **CIK:** 41,719 · **SIC:** 2621 (Paper Mills) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 12.40 |
| mktcap | $443.9M |
| ev | $2.1B |
| ev_ebit | 413.0x |
| fcf | $36.0M |
| fcf_yield | 8.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 0.1% |
| net_debt | $1.6B |
| net_debt_ebit | 324.2x |
| cash | $280.0M |
| ltd | $1.9B |
| equity | $1.0B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $3.2B |
| revenue_prior | $2.2B |
| rev_growth | 46.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $5.0M |
| net_income | -$159.0M |
| cfo | $103.0M |
| capex | $67.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 35,800,000 |
| shares_py | 35,600,000 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 16.6% |
| r6m | 0.1% |
| off_52w_high | -18.7% |
| adv20 | $5.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.65 |
| r_ev_ebit | 0.01 |
| r_roic | 0.31 |
| r_rev_growth | 0.94 |
| r_buyback | 0.55 |
| score | 0.54 |

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
| rank | 204 |

**Screen rationale:** revenue +46.5%; 12-1 momentum 16.6%


## 3. Share count trend

- Shares outstanding: **35,800,000** (CY2026Q2I) vs **35,600,000** prior year (CY2025Q2I)
- Change: **0.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 9 |
| F | 2 |
| M | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Magnera Reports Third Quarter'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ef20079553_ex99-1.htm)

Magnera Reports Third Quarter

Third Quarter Highlights

• | GAAP: Net sales of $857 million, Operating income of $22 million

• | Non-GAAP: Adjusted EBITDA of $99 million

• | Twelve-month adjusted free cash flow yield of greater than 25% as of quarter-end

Curt Begle, Magnera's CEO, commented: "We delivered a record third quarter led by organic volume growth, combined with the savings benefits of synergy initiatives and Project Core. In addition, our commercial team executed the disciplined actions required to effectively manage the significant spike in inflationary costs of certain raw materials. As we continue to navigate a dynamic macro-economic environment, we remain focused on executing our strategic objectives and delivering dependable financial results. Consistent with that commitment, we are reaffirming our full-year free cash flow outlook, while holding to the lower end of our adjusted EBITDA guidance range."

Key Financials

June Quarter | June YTD
GAAP results | 2026 | 2025 | 2026 | 2025
Net sales | 857 | 839 | 2,445 | 2,365
Operating income | 22 | 13 | 53 | (5

June Quarter | Reported | Comparable (1) | June YTD | Reported | Comparable (1)
Adjusted non-GAAP results | 2026 | 2025 | % | % | 2026 | 2025 | % | %
Net sales | 857 | 839 | 2 | % | - | 2,445 | 2,365 | 3 | % | (5 | %)
Adjusted EBITDA (1) | 99 | 91 | 9 | % | 9 | % | 282 | 264 | 7 | % | 3 | %

(1) | Adjusted non-GAAP results exclude items not considered to be ongoing operations. In addition, comparable change % normalizes the impacts of foreign currency and the merger with Glatfelter. Further details related to non-GAAP measures and reconciliations can be found under "Reconciliation of Non-GAAP Financial Measures and Estimates" section or in reconciliation tables in this release. Dollars in millions

Consolidated Overview

The net sales increase included a favorable foreign currency change of $21 million and a 1% organic volume
improvement, partially offset by an $8 million decrease in selling prices primarily due to negative product mix net of the pass-through of higher raw material costs. The volume increase was mainly attributed to strength in our consumer
solutions product categories globally and recovery in North America from winter storm disruptions experienced in the second quarter.

The adjusted EBITDA was up 9% primarily as a result of favorable price cost spread of $11 million.

Americas

The net sales increase included a favorable foreign currency change of $10 million and a 1% organic volume improvement, partially offset by a
$13 million decrease in selling prices primarily due to negative product mix net of the pass-through of higher raw material costs.

The adjusted EBITDA improvement resulted mostly from a favorable price cost spread of $11 million due to the realized benefits from Project CORE
and merger synergies that were partially offset by higher selling, general and administrative costs.

Page | 1

Rest of World

The net sales increase included a favorable foreign currency change of $11 million
and a $5 million increase in selling prices due to the pass-through of higher raw material costs.

The adjusted EBITDA declined $2 million as benefits from Project CORE and synergy realization were offset by higher inflation in the region,
timing of material pass throughs and higher selling, general and administrative costs.

Investor Conference Call

The Company will host a conference call, August 6, 2026, at 10:00 AM U.S. Eastern
Time to discuss the third quarter results. The webcast can be accessed here . A replay of the webcast will be available via the same
link on the Company's website after the completion of the call.

By Telephone

Participants may register for the call here now or any time up to and during the time of the call and will immediately receive the dial-in number and a unique pin
to access the call. While you may register at any time up to and during the time of the call, you are encouraged to join the call 15 minutes prior to the start of the event.

About Magnera

Magnera Corporation (NYSE: MAGN) serves 1,000+ customers worldwide, offering a wide range of material solutions, including components for absorbent hygiene
products, protective apparel, wipes, specialty building and construction products, and products serving the food and beverage industry. Operating across 44 global facilities, Magnera is supported by over 8,000+ employees. Magnera's purpose
is to better the world with new possibilities made real. For more than 160 years, the Company has delivered the material solutions their partners need to thrive. Through economic upheaval, global pandemics and changing end-user needs, we
have consistently found ways to solve problems and exceed expectations. The distinct scale and comprehensive portfolio of products brings customers more materials and choices. Magnera builds personal partnerships that withstand an
ever-changing world.

Visit Magnera.com for more information and follow @MagneraCorporation on social platforms.

Non-GAAP Financial Measures and Estimates

This press release includes non-GAAP financial measures including, but not limited to, Adjusted EBITDA, free cash flow, and comparable basis net sales and
adjusted EBITDA. A reconciliation of these non-GAAP financial measures to comparable measures determined in accordance with accounting principles generally accepted in the United States of America (GAAP) is set forth at the end of this
press release. Information reconciling forward-looking adjusted EBITDA and adjusted free cash flow are not provided because such information is not available without unreasonable effort due to high variability, complexity, and low
visibility with respect to certain items, including debt refinancing activity or other non-comparable items. These items are uncertain, depend on various factors, and could be material to our results computed in accordance with U.S. GAAP.

Condensed Consolidated Balance Sheets (unaudited)

(in millions of dollars ) | June 27, 2026 | September 27, 2025
Cash and cash equivalents | 280 | 305
Accounts receivable | 531 | 522
Inventories | 498 | 474
Other current assets | 83 | 122
Property, plant, and equipment | 1,393 | 1,476
Goodwill, intangible assets, and other long-term assets | 1,049 | 1,090
Total assets | 3,834 | 3,989
Current liabilities, excluding current debt | 569 | 601
Current and long-term debt | 1,901 | 1,952
Other long-term liabilities | 347 | 372
Stockholders' equity | 1,017 | 1,064
Total liabilities and stockholders' equity | 3,834 | 3,989

Page | 3

Reconciliation of Non-GAAP Measures and Estimates

(in millions of dollars)

Reconciliation of Net sales and Adjusted EBITDA on a supplemental comparable basis by segment
Quarterly Period ended June 27, 2026 | Quarterly Period ended June 28, 2025
Americas | Rest of World | Total | Americas | Rest of World | Total
Net sales | 476 | 381 | 857 | 473 | 366 | 839
Constant FX rates | 10 | 11 | 21
Comparable net sales (1)(6) | 476 | 381 | 857 | 483 | 377 | 860
Operating Income | 28 | (6 | 22 | 12 | 1 | 13
Depreciation and amortization | 32 | 18 | 50 | 35 | 23 | 58
Integration, business consolidation and other activities | 8 | 8 | 16 | 9 | 4 | 13
Argentina hyperinflation | - | - | - | 1 | - | 1
Other non-cash charges (5) | 3 | 8 | 11 | 4 | 2 | 6
Adjusted EBITDA (1) | 71 | 28 | 99 | 61 | 30 | 91
Constant FX rates | - | - | -
Comparable Adjusted EBITDA (1)(6) | 71 | 28 | 99 | 61 | 30 | 91
% vs. prior year comparable | 16 | % | (7 | %) | 9 | %
Three Quarterly Periods ended June 27, 2026 | Three Quarterly Periods ended June 28, 2025
Americas | Rest of World | Total | Americas | Rest of World | Total | LTM
Net sales | 1,353 | 1,092 | 2,445 | 1,366 | 999 | 2,365
Constant FX rates | 29 | 76 | 105
GLT prior year | 42 | 70 | 112
Comparable net sales (1)(6) | 1,353 | 1,092 | 2,445 | 1,437 | 1,145 | 2,582
Operating Income | 46 | 7 | 53 | 13 | (18 | (5 | 63
Depreciation and amortization | 95 | 55 | 150 | 107 | 62 | 169 | 186
Integration, business consolidation and other activities (2) | 34 | 18 | 52 | 43 | 21 | 64 | 82
Argentina hyperinflation | 3 | - | 3 | 1 | - | 1 | 8
GAAP carve-out allocation (3) | - | - | - | 2 | 1 | 3 | -
Other non-cash charges (4)(5) | 9 | 15 | 24 | 15 | 17 | 32 | 33
Adjusted EBITDA (1) | 187 | 95 | 282 | 181 | 83 | 264 | 372
Constant FX rates | - | 3 | 3
GLT prior year | 5 | 3 | 8
Comparable Adjusted EBITDA (1)(6) | 187 | 95 | 282 | 186 | 89 | 275
% vs. prior year comparable | 1 | % | 7 | % | 3 | %
PF Divestiture | (2
Synergies and cost reductions | 35
PF Adjusted EBITDA | 405

(1) | Supplemental financial measures that are not required by, or presented in accordance with, accounting principles generally accepted in the United States ("GAAP"). These non-GAAP financial measures should not be considered as alternatives to operating or net income or cash flows from operating activities, in each case determined in accordance with GAAP. Comparable basis measures exclude the impact of currency translation effects and acquisitions. These non-GAAP financial measures may be calculated differently by other companies, including other companies in our industry, limiting their usefulness as comparative measures. Management believes that Adjusted EBITDA and other non-GAAP financial measures are useful to our investors because they allow for a better period-over-period comparison of operating results by removing the impact of items that, in management's view, do not reflect our core operating performance. We define "free cash flow" as cash flow from operating activities less net additions to property, plant, and equipment. We believe free cash flow is useful to an investor in evaluating our liquidity because free cash flow and similar measures are widely used by investors, securities analysts, and other interested parties in our industry to measure a company's liquidity. We believe free cash flow is also useful to an investor in evaluating our liquidity as it can assist in assessing a company's ability to fund its growth through its generation of cash and as pre-merger cash flow is not indicative of our current structure and operations.

We also use Adjusted EBITDA and comparable basis measures, among other measures, to evaluate management performance and in determining performance-based compe nsation. Adjusted EBITDA is a measure widely used by investors, securities analysts, and other interested parties in our industry to measure a company's performance. We also believe these measures are useful to an investor in evaluating our performance without regard to revenue and expense recognition, which can vary depending upon accounting methods.

(2) | Includes restructuring, business optimization and other charges, which includes $17 million of transaction compensation expense in the prior year

(3) | Consists of estimated parent-allocated charges for the period prior to merger which is required by GAAP as part of the carve-out financial statement process

(4) | Prior year includes $12 million inventory step-up charge related to the merger and other non-cash charges

(5) | Includes expense for stock compensation and disposals and sale of assets

(6) | The prior year comparable basis change excludes the impacts of foreign currency and acquisitions/mergers

IR Contact Information

Robert Weilminster

EVP, Investor Relations

IR@magnera.com

Page | 4

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-11-25_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

Item 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS

Outlook

The Company is affected by
general economic and industrial growth, raw material availability, cost
inflation, supply chain disruptions, new and changing tariffs and general
industrial production. Our business has both geographic and end
market diversity, which reduces the effect of any one of these factors on our
overall performance. Our results are affected by our ability to pass
through raw material and other cost changes, including tariffs, to our
customers, improve manufacturing productivity and adapt to volume changes of
our customers. During fiscal 2025, the Company announced capacity
rationalizations (Project CORE) in order to deliver future cost savings and optimize equipment
utilization. In total, over the next two years, these actions are projected to
cost approximately $20 million with the operations savings intended to counter
general economic softness. Despite global macro-economic challenges
and uncertainties attributed to inflation, changing tariff
policies and general market softness, we continue to believe our underlying
long-term demand fundamental in all segments will remain strong as we focus on
providing advantaged products in targeted markets. For fiscal year 2026 ("fiscal 2026"),
we project cash from operations between $170 to $190 million and free cash
flow between $90 to $110 million. Projected fiscal 2026 free cash flow assumes $80 million of capital
spending. For the definition of free cash flow and further
information related to free cash flow as a non-GAAP financial measure, see
"Liquidity and Capital Resources."

Discussion of Results of Operations for Fiscal 2025 Compared to Fiscal 2024

Business integration expenses consist of restructuring and impairment charges, divestiture-related costs, and other business optimization costs. Tables present dollars in millio ns. A
discussion and analysis regarding our results of operations for fiscal year
2024 compared to fiscal year 2023 can be found on Form 8-K/A, filed with the
SEC on January 31, 2025 .

Consolidated Overview | Fiscal Year
2025 | 2024 | $ Change | % Change
Net sales | 3,204 | 2,187 | 1,017 | 47 | %
Operating income (loss) | 5 | (141) | 146 | 104 | %

Net
sales: The net sales
increase included revenue from the Transaction of $1,145 million partially
offset by decreased selling prices of $45 million primarily due to the
pass-through of lower raw material costs, a $32 million unfavorable impact from
foreign currency changes and a 2% organic volume decline, that was attributed
to general market softness in Europe and competitive pressures from imports in
South America.

Operating income
(loss): The operating income
improvement is primarily attributed to the $171 million goodwill impairment
charge in fiscal 2024, the elimination of $18 million in corporate expense
allocations, an $11 million favorable change from prior year hyperinflation
in Argentina, and operating income from GLT, partially offset by a $16 million inventory fair value step-up
charge related to the Transaction, a $25 million unfavorable impact from increased business integration
costs, a $12 million increase in stock compensation expense, and an unfavorable impact from volume declines.

Other expense (income), net | Fiscal Year
2025 | 2024 | $ Change | % Change
Other expense (income), net | 30 | (9) | 39 | 433 | %

The Other expense (income) increase is
due to a $15 million prepayment penalty charge for retiring debt concurrently
with the Transaction, $8 million of non-cash charges associated with
pre-Transaction tax liabilities, and a $12 million unfavorable change in currency charges related to intercompany
loans.

Interest expense, net | Fiscal Year
2025 | 2024 | $ Change | % Change
Interest expense, net | 141 | 3 | 138 | 4,600 | %

The Interest expense increase
is due to increased borrowings from the Transaction.

Comprehensive income (loss) | Fiscal Year
2025 | 2024 | $ Change | % Change
Comprehensive income (loss) | (186) | (151) | (35) | (23) | %

The decrease is primarily attributed to a $30 million unfavorable change in currency translation combined with a $5 million decline in net income. Currency translation changes are primarily related to non-U.S. subsidiaries with a functional currency other than the U.S. dollar whereby assets and liabilities are translated from the respective functional currency into U.S. dollars using period-end exchange rates. The change in currency translation was primarily attributed to locations utilizing the euro or Brazilian real as their functional currency. As part of its overall risk management, the Company uses derivative instruments to reduce foreign currency exposure to translation of certain foreign operations. The Company records changes to the fair value of these instruments in Accumulated other comprehensive loss. The change in fair value of these instruments in the year is primarily attributed to the change in the forward foreign currency exchange curves between measurement dates.

Segment Overview

Americas | Fiscal Year
2025 | 2024 | $ Change | % Change
Net sales | 1,833 | 1,493 | 340 | 23 | %
Adjusted EBITDA | 241 | 223 | 18 | 8 | %

Net sales: The net sales increase included revenue from the
Transaction of $440 million partially offset by decreased selling prices of $35 million primarily due to the pass-through of lower raw material costs, a $36
million unfavorable impact from foreign currency changes and a 2% organic
volume decline that was primarily attributed to competitive pressures from
imports in South America .

Adjusted EBITDA: The EBITDA increase included EBITDA from the
Transaction of $40 million partially offset by unfavorable price cost spread of $14 million and a $7 million unfavorable impact from currency changes.

Rest of World | Fiscal Year
2025 | 2024 | $ Change | % Change
Net sales | 1,371 | 694 | 677 | 98 | %
Adjusted EBITDA | 113 | 59 | 54 | 92 | %

Net
sales: The net sales
increase included revenue from the Transaction of $705 million partially offset
by decreased selling prices of $10 million due to the pass-through of lower raw materials, as well as a 3% organic volume decline that was primarily attributed to general market
softness in Europe.

Adjusted EBITDA: The EBITDA increase included EBITDA from the
Transaction of $45 million and favorable price cost spread of 11 million.

Liquidity and Capital Resources

We manage our global cash
requirements considering (i) available funds among the many subsidiaries
through which we conduct our business, (ii) the geographic location of our
liquidity needs, and (iii) the cost to access international cash
balances. At the end of the fiscal 2025, the Company had no
outstanding balance on its asset-based revolving line of credit that matures in
November 2029 and the Company was in compliance with all covenants.

Cash Flows from Operating Activities

Net cash from operating
activities declined $89 million, primarily related to a d ecline in net income prior to non-cash
activities.

Cash Flows from Investing Activities

Net cash from investing activities improved $31 million, primarily attributed to cash acquired in
connection with the Transaction and settlement of net investment hedges in fiscal
2025 compared to the settlement of short-term marketable securities in fiscal
2024.

Cash Flows from Financing Activities

Net cash used in financing activities improved $88 million attributed to higher transfers from Berry prior
to the Transaction partially offset by repayments of long-term debt in fiscal
2025 and debt fees related to the Transaction.

Free Cash Flow

Our consolidated free cash flow for the fiscal 2025 are summarized as
follows:

September 27, 2025
Cash flow from operating activities | 103
Pre-Transaction free cash flow from operating activities (1) | 90
Additions to property, plant and equipment, net | (67
Free cash flow | 126

(1) Pre-merger cash flow includes pre-Transaction cash from operations and other cash payments burdened by the Transaction.

We use free cash flow metrics as a
supplemental measure of liquidity as it assists us in assessing our ability to
fund growth through generation of cash.
Free cash flow metrics may be calculated differently by other companies,
including other companies in our industry or peer group, limiting its
usefulness on a comparative basis. Free
cash flow metrics are not a financial measure presented in accordance with GAAP
and should not be considered as an alternative to any other measure determined
in accordance with GAAP.

Liquidity Outlook

At the end of fiscal 2025, our
cash balance was $305 million, of which approximately
86% was located outside the U.S. We believe our existing and future U.S.-based cash and cash flow from U.S. operations will be adequate to meet our
short-term and long-term liquidity needs. The Company has the
ability to repatriate the cash located outside the U.S. to the extent not
needed to meet operational and capital needs without significant
restrictions. Our unremitted foreign earnings were $336 million at
the end of fiscal 2025. The computation of the deferred tax
liability associated with unremitted earnings is not practicable.

Critical Accounting Policies and Estimates

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-11-25_item1_business.md)

Item 1. BUSINESS

(In millions of dollars, except as otherwise noted)

General

The Company is a leading global supplier of a diverse portfolio of innovative specialty materials comprised of organic and synthetic raw ingredients. We market our products predominantly into stable, consumer-oriented end markets for disposable and durable applications. End user examples include wipes, healthcare, adult incontinence, apparel, baby, feminine care, air filtration, and food and beverage. We also provide technical solutions in infrastructure markets. Our customers include a mix of leading global and national brands, private label, and small to mid-sized regional businesses.

On November 4,
2024 (the "Closing Date"), Treasure Holdco, Inc. ("Treasure"), which was a
wholly owned subsidiary of Berry Global Group, Inc. ("Berry"), completed its
merger (the "Transaction") with the Glatfelter Corporation ("GLT" or
"Glatfelter") which concurrently changed its name to Magnera Corporation (the
"Company," "we," or "Magnera"). As a result, pre-Transaction
Treasure shareholders received shares of Magnera representing 90% of the
combined company and GLT shareholders retained 10%. As Treasure was
identified as the accounting acquirer, the prior year presentation represents
standalone Treasure results with the acquisition method of accounting being
applied to the assets acquired and liabilities assumed from GLT. See Note
2. Acquisition.

Additional financial information about our segments is provided in "Management's Discussion and Analysis of Financial Condition and Results of Operations" and the "Notes to Consolidated and Combined Financial Statements," which are included elsewhere in this report.

Segment Overview

The Company's operations are organized into two operating and
reportable segments: Americas and Rest of World. The structure is designed to
align us with our customers, provide improved service, enable future growth initiatives and efficiency of decision making to facilitate synergy realization.

Americas

The Americas segment is the Company's largest segment, accounting for 57% of consolidated net sales. Our Americas operations consist of 22 manufacturing facilities - 14 in the United States, 3 in Brazil, 2 in Mexico, 2 in Canada, and 1 in Colombia. The segment primarily manufactures a wide range of products and components of personal care and consumer solution products and components of products including medical garments, wipes, dryer sheets, filtration, baby diapers and adult incontinence.

Rest of World

The Rest of World segment represents 43% of our consolidated net sales. Our Rest of World operations consist of 23 manufacturing facilities - 7 in Germany, 5 in France, 4 in United Kingdom, 2 in China, 2 in Spain, and 1 each in Italy, Netherlands, and Philippines. This segment primarily manufactures a broad collection of personal care and consumer solution products and components of products including tea bags, coffee filters, wipes, cable wrap, filtration, baby diapers and adult incontinence.

Marketing, Sales, and Competition

We reach our customer base through a direct sales force of dedicated professionals. Our scale enables us to dedicate certain sales and marketing efforts to particular customers, when applicable, which enables us to develop expertise that we believe is valued by our customers.

The major markets in which the Company sells its products are highly competitive. Areas of competition include service, innovation, quality, and price. This competition is significant as to both the size and the number of competing firms. Competitors include, but are not limited to, Ahlstrom, Avgol, Mativ, PFNonwovens, Freudenberg, and Fitesa.

Raw Materials

Our primary raw materials are polymer resin,
wood-based fibers, and pulps. In addition, we use other materials in
various manufacturing processes. While temporary industry-wide
shortages of raw materials have occurred, we have historically been able to
manage the supply chain disruption by working closely with our suppliers and
customers. Changes in the price of raw materials are generally
passed on to customers through contractual price mechanisms over time, during
contract renewals, and other means.

Patents, Trademarks and Other Intellectual Property

We customarily seek patent and trademark protection for our products and brands while seeking to protect our proprietary know-how. While important to our business in the aggregate, sales of any one individually patented product is not considered material to any specific segment or our consolidated results.

Environment and Sustainability

Sustainability is comprehensively embedded across our business, from how we run our manufacturing operations more efficiently to the investments we are making in sustainable solutions. With our global scale, deep industry experience, and strong capabilities, we are uniquely positioned to assist our customers in the design and development of sustainable solutions. We also work globally on
continuous improvement of energy usage, water efficiency,
waste reduction, recycling, and reducing our greenhouse gas emissions.

Human Capital and Employees

Health and Safety

Safe ty for our approximately 8,500 employees is our number one priority. We believe when it comes to employee safety, our best should always be our standard. It is through the adherence to our global environment, health, and safety principles that we have been able to identify and mitigate operational risks and drive continuous improvement.

Talent and Development

We seek to attract, develop and retain talent throughout the Company. Our succession management strategy focuses on a structured succession framework and multiple years of performance. Our holistic approach to developing key managers and identifying future leaders includes challenging assignments, formal development plans and professional coaching.

Employee Engagement

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-11-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-11-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-11-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2025-11-25_item7_mdna.md, 10-K_2025-11-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
