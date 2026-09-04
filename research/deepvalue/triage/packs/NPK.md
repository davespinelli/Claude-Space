# Triage pack — NPK · NATIONAL PRESTO INDUSTRIES INC

_Generated 2026-09-04 16:12 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** NPK · **Name:** NATIONAL PRESTO INDUSTRIES INC
- **CIK:** 0000080172
- **SIC:** 3480 — Ordnance & Accessories, (No Vehicles/Guided Missiles)
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/NPK

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** NATIONAL PRESTO INDUSTRIES INC
- **CIK:** 80,172 · **SIC:** 3480 (Ordnance & Accessories, (No Vehicles/Guided Missiles)) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 144.70 |
| mktcap | $1.0B |
| ev | $1.0B |
| ev_ebit | 25.3x |
| fcf | -$36.2M |
| fcf_yield | -3.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 8.0% |
| net_debt | -$15.8M |
| net_debt_ebit | -0.4x |
| cash | $15.8M |
| ltd | $0.00 |
| equity | $411.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $503.5M |
| revenue_prior | $388.2M |
| rev_growth | 29.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $40.2M |
| net_income | $33.1M |
| cfo | -$9.1M |
| capex | $27.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 7,136,067 |
| shares_py | 7,149,529 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 32.5% |
| r6m | 7.6% |
| off_52w_high | -7.7% |
| adv20 | $13.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.13 |
| r_ev_ebit | 0.35 |
| r_roic | 0.64 |
| r_rev_growth | 0.89 |
| r_buyback | 0.70 |
| score | 0.59 |

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
| rank | 153 |

**Screen rationale:** revenue +29.7%; debt data missing (net cash unverified); 12-1 momentum 32.5%


## 3. Share count trend

- Shares outstanding: **7,136,067** (CY2026Q2I) vs **7,149,529** prior year (CY2025Q2I)
- Change: **-0.2%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 2,917 sh / $418,053 -> net $-418,053 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 5 |
| F | 5 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit; skipped 1 forward-looking-statement block(s)._

## EX-99.1 - EXHIBIT 99.1 (ex_997628.htm)

EX-99.1
ex_997628.htm
EXHIBIT 99.1

ex_997628.htm

Exhibit 99.1

NEWS RELEASE | CONTACT: David Peuse
FOR IMMEDIATE RELEASE | (715) 839-2146

NATIONAL PRESTO INDUSTRIES, INC. ANNOUNCES

INCREASED SECOND QUARTER 2026 SALES AND EARNINGS

Eau Claire, Wisconsin (July 31, 2026) — National Presto Industries, Inc. (NYSE: NPK) announced today second quarter 2026 sales and earnings as shown in the table below. Net earnings per share have been computed on the basis of the weighted average number of common shares outstanding for the respective periods.

In response to questions about sales and earnings for the quarter, Maryjo Cohen, President, stated, "Defense segment sales for the quarter were up $27.1 million or 27.2% from those reported in the comparable 2025 quarter, reflecting increased shipments from backlog. Sales for the Housewares/Small Appliances segment decreased $1.2 million or 6.2% largely attributable to the impact of the Trump tariffs that affected retail order timing (retailers accelerated orders in 2025 to secure lower pre-tariff pricing) and has resulted in increased retail pricing, which in turn has depressed consumer demand. Safety segment sales, although still nominal, increased by $226,000 or 91.7%. The Defense segment's operating earnings were up $4.9 million or 33.5% from second quarter 2025 earnings largely due to the additional volume referenced above. In contrast to the prior year's loss, Housewares/Small Appliance segment's operating earnings were $2.2 million. Most of those earnings were attributable to a refund of a portion of the tariffs the segment had paid that the Supreme Court declared unauthorized in its February decision. The Safety segment reported a loss as anticipated."

National Presto Industries, Inc. operates in three business segments. The Housewares/Small Appliance segment designs and sells small household appliances and pressure cookers under the PRESTO® brand name. The segment is recognized as an innovator of new products. The Defense segment manufactures a variety of products, including medium caliber training and tactical ammunition, energetic ordnance items, fuzes, cartridge cases, and metal parts. The Safety segment offers smoke and carbon monoxide alarms, and fire extinguishers.

​ | ​ | THREE MONTHS ENDED | ​
​ | ​ | July 5, 2026 | ​ | ​ | June 29, 2025 | ​
Net Sales | ​ | 146,596,000 | ​ | ​ | 120,449,000 | ​
Net Earnings | ​ | 15,862,000 | ​ | ​ | 5,152,000 | ​
Net Earnings Per Share | ​ | 2.21 | ​ | ​ | .72 | ​
Weighted Shares Outstanding | ​ | ​ | 7,167,000 | ​ | ​ | ​ | 7,147,000 | ​

​ | ​ | ​ SIX MONTHS ENDED | ​
​ | ​ | July 5, 2026 | ​ | ​ | June 29, 2025 | ​
Net Sales | ​ | 265,245,000 | ​ | ​ | 224,088,000 | ​
Net Earnings | ​ | 22,488,000 | ​ | ​ | 12,762,000 | ​
Net Earnings Per Share | ​ | 3.14 | ​ | ​ | 1.79 | ​
Weighted Shares Outstanding | ​ | ​ | 7,164,000 | ​ | ​ | ​ | 7,146,000 | ​

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-13_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS

﻿

An overview of the Company's business and segments in which the Company operates and risk factors can be found in Items 1 and 1A of this Form 10-K. Forward-looking statements in this Management's Discussion and Analysis of Financial Condition and Results of Operations, elsewhere in this Form 10-K, in the Company's 2025 Annual Report to Shareholders, in the Proxy Statement for the annual meeting to be held May 19, 2026, and in the Company's press releases and oral statements made with the approval of an authorized executive officer are made pursuant to the safe harbor provisions of the Private Securities Litigation Reform Act of 1995. There are certain important factors that could cause results to differ materially from those anticipated by some of the statements made herein. Investors are cautioned that all forward-looking statements involve risks and uncertainty. In addition to the factors discussed herein and in the notes to Consolidated Financial Statements, among the other factors that could cause actual results to differ materially are the following: consumer spending and debt levels; interest rates; continuity of relationships with and purchases by major customers; product mix; the benefit and risk of business acquisitions; competitive pressure on sales and pricing; development and market acceptance of new products; increases in material, freight/shipping, tariffs, or production cost which cannot be recouped in product pricing; delays or interruptions in shipping or production; shipment of defective product which could result in product liability claims or recalls; work or labor disruptions stemming from a unionized work force; changes in government requirements, military spending, and funding of government contracts which could result, among other things, in the modification or termination of existing contracts; dependence on subcontractors or vendors to perform as required by contract; the ability of startup businesses to ultimately have the potential to be successful; the efficient start-up and utilization of capital and equipment investments; political actions of federal and state governments which could have an impact on everything from the value of the U.S. dollar vis-à-vis other currencies to the availability of affordable labor and energy; and security breaches and disruptions to our information technology system. Additional information concerning these and other factors is contained in the Company's Securities and Exchange Commission filings.

﻿

2025 COMPARED TO 2024

﻿

Readers are directed to Note L, "Business Segments," to the Company's Consolidated Financial Statements for data on the financial results of the Company's three business segments for the years ended December 31, 2025 and 2024.

﻿

On a consolidated basis, sales increased by $115,296,000 (30%), gross profit increased by $1,759,000 (2%), selling and general expense increased by $4,030,000 (13%), impairment of vendor deposit increased $2,701,000, and amortization was consistent. Other income decreased by $3,579,000 (66%), earnings before provision for income taxes decreased by $8,551,000 (17%), and net earnings decreased by $8,376,000 (20%). Details concerning these changes can be found, by segment, in the comments below.

﻿

Net sales of the Housewares/Small Appliance segment decreased by $7,195,000 (7%), from $102,799,000 to $95,604,000, primarily attributable to a decrease in units shipped, approximately 47% was offset by an increase in pricing. Net sales of the Defense segment increased by $121,912,000 (43%), from $284,025,000 to $405,937,000, reflecting an increase in shipments from the segment's backlog. Safety segment sales increased $579,000 to $1,983,000, reflecting an increase in shipments.

﻿

Gross profit of the Housewares/Small Appliance segment decreased $17,889,000 from $25,478,000 (25% of sales) in 2024 to $7,589,000 (8% of sales) in 2025, primarily reflecting the decrease in sales mentioned above and the Trump administration's tariffs that went into effect on goods deemed to have been shipped from the Orient after January 31, 2025. Those tariffs are generally treated as period costs and expensed as they are incurred, reflecting the segment's LIFO inventory cost valuation method. The relocation costs of the segment's distribution center from Canton to Nettleton, Mississippi also served to reduce gross profit by approximately $1,261,000. Defense gross profit increased $19,471,000 from $58,173,000 (21% of sales) in 2024 to $77,644,000 (19% of sales) in 2025, primarily reflecting the increase in sales mentioned above, as well as differences in mix efficiencies, and material costs. Due to the startup nature of the businesses in the Safety segment and resulting limited revenues, gross margins were negative in both years.

﻿

Selling and general expenses for the Housewares/Small Appliance segment increased $1,304,000, primarily reflecting increased personnel costs of $768,000, computers and technology costs of $266,000, and the favorable adjustment to the reserve for bad debts of $285,000 that occurred in the prior year. Defense segment selling and general expenses increased $3,941,000, primarily due to increased personnel costs of $3,012,000, legal and professional expenses of $347,000, repairs and maintenance costs of $334,000, and computers and software expenses of $256,000. Safety segment selling and general expenses decreased $1,215,000, primarily reflecting the sale of OneEvent's refrigeration monitoring business that occurred on July 31, 2025.

During the first quarter of 2025, the Company made deposits totaling $2,701,000 with a vendor in its Housewares/Small Appliances segment. On May 29, 2025, the vendor filed for protection in the U.S. Bankruptcy Court in the Northern District of Texas. As recovery of the deposit is deemed unlikely, the Company recorded an impairment of the full deposit during the second quarter of 2025.

The above items were responsible for the change in operating profit from continuing operations.

﻿

The $3,579,000 decrease in other income was attributable to a decrease of $3,009,000 in interest income on marketable securities and an increase in interest expense of $830,000 related to the outstanding balance of the Company's revolving line of credit during 2025. Both stem from the increased investments in inventory required to support augmented Defense segment awards.

﻿

Earnings before provision for income taxes decreased $8,551,000 from $50,670,000 to $42,119,000. The provision for income taxes decreased $175,000 from $9,210,000 to $9,035,000, which resulted in an effective income tax rate of 22% and 18% for the years ended December 31, 2025 and 2024, respectively. The increase in the effective income tax rate was primarily attributable to the absence of favorable adjustments recognized in 2024 related to prior year estimates. Net earnings decreased $8,376,000 from $41,460,000 to $33,084,000.

﻿

2024 COMPARED TO 2023

﻿

Readers are directed to Note L, "Business Segments," to the Company's Consolidated Financial Statements for data on the financial results of the Company's three business segments for the years ended December 31, 2024 and 2023.

﻿

On a consolidated basis, sales increased by $47,316,000 (14%), gross profit increased by $11,114,000 (17%), selling and general expense increased by $1,054,000 (3%), and intangibles amortization decreased by $120,000 (7%). Other income decreased by $1,941,000 (26%), earnings before provision for income taxes increased by $8,239,000 (19%), and net earnings increased by $6,901,000 (20%). Details concerning these changes can be found, by segment, in the comments below.

﻿

Net sales of the Housewares/Small Appliance segment increased by $5,180,000, from $97,619,000 to $102,799,000, or 5%, primarily attributable to the increase in units shipped. Net sales of the Defense segment increased by $42,322,000, from $241,703,000 to $284,025,000, or 18%, reflecting an increase in units shipped.

﻿

Gross profit of the Housewares/Small Appliance segment increased $5,611,000 from $19,867,000 (20% of sales) in 2023 to $25,478,000 (25% of sales) in 2024, primarily reflecting the increase in sales mentioned above, augmented by an improved product mix and a favorable LIFO inventory adjustment. Defense gross profit increased $6,170,000 from $52,003,000 (22% of sales) in 2023 to $58,173,000 (21% of sales) in 2024, primarily reflecting the increase in sales mentioned above. Due to the startup nature of the businesses in the Safety segment, gross margins were negative in both years. The comparative decrease in gross margins of $667,000 were primarily due to increased product development and testing.

﻿

Selling and general expenses for the Housewares/Small Appliance segment increased $361,000, primarily reflecting increased personnel costs of $654,000 and accrual levels for self insurance of $339,000, partially offset by changes to accrual levels for bad debt of $571,000. Defense segment selling and general expenses increased $1,530,000, primarily due to increased personnel costs of $1,609,000, partially offset by decreased legal and professional expenses of $156,000. Safety segment selling and general expenses decreased $837,000, primarily reflecting decreased personnel costs of $935,000 and legal and professional expenses of $322,000, partially offset by the absence of the prior year's gain on the sale of Rusoh, Inc. of $351,000. See Notes L to the Company's Consolidated Financial Statements.

Intangibles amortization decreased as a result of the absence of the prior year's amortization of intellectual property intangibles from the acquisition of Knox Safety, Inc.

The above items were responsible for the change in operating profit from continuing operations.

﻿

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-13_item1_business.md)

ITEM 1. BUSINESS

﻿

A. DESCRIPTION OF BUSINESS

﻿

The business of National Presto Industries, Inc. (the "Company" or "National Presto") consists of three business segments. For a further discussion of the Company's business, the segments in which it operates, and financial information about the segments, please refer to Note L to the Consolidated Financial Statements. The Housewares/Small Appliance segment designs, markets and distributes housewares and small electrical appliances, including pressure cookers and canners, kitchen electrics, and comfort appliances that enrich the lives of consumers by making life easier, more productive and more enjoyable. The Defense segment protects the lives of the citizens of our nation, as well as the citizens of our nation's allies, by providing our warfighters with reliable products. It manufactures 40mm ammunition, precision mechanical and electro-mechanical assemblies, medium caliber cartridge cases and metal parts; performs Load, Assemble and Pack (LAP) operations on ordnance-related products primarily for the United States Government and prime contractors; and manufactures detonators, booster pellets, release cartridges, lead azide, other military energetic devices and materials, and assemblies. The Safety segment provides innovative safety technology empowering organizations and individuals to protect what is most important. The segment's startup company, Rely Innovations, Inc., offers smoke, carbon monoxide (CO), and combo smoke/CO alarms with an array of voice messages in English and Spanish that clearly inform of incipient danger. The CO alarms have large digital displays as well. The segment also markets an economy line of carbon monoxide and smoke alarms and a PFAS-Free Foam commercial fire extinguisher.

﻿

1. Housewares/Small Appliance Segment

Housewares and electrical appliances sold by the segment include pressure cookers and canners; the Presto Control Master® heat control line of skillets in several sizes, griddles, woks and multi-purpose cookers; slow cookers; deep fryers of various sizes; waffle makers; pizza ovens; slicer/shredders; electric heaters; corn poppers (hot air, oil, and microwave); dehydrators; vacuum sealers; microwave bacon cookers; coffeemakers and coffeemaker accessories; electric knife sharpeners; and timers. Pressure cookers and canners are available in a range of sizes, in stovetop and digital forms, and are made from aluminum and/or stainless steel.

﻿

For the year ended December 31, 2025, approximately 9% of consolidated net sales were provided by cast products (griddles, waffle makers, die cast deep fryers, skillets and multi-cookers), and approximately 9% by noncast/thermal appliances (stamped cookers and canners, pizza ovens, corn poppers, coffee makers, microwave bacon cookers, dehydrators, slow cookers, electric stainless steel appliances, non-cast fryers, air fryers and heaters). For the year ended December 31, 2024, approximately 10% of consolidated net sales were provided by cast products, and approximately 15% by noncast/thermal appliances. For the year ended December 31, 2023, approximately 9% of consolidated net sales were provided by cast products, and approximately 18% by noncast/thermal appliances. For the year ended December 31, 2025, this segment had no customers that accounted for 10% of the Company's consolidated net sales. For the years ended December 31, 2024 and 2023, Amazon.com, Inc. accounted for 10% and 11%, respectively, of the Company's consolidated net sales. The loss of Amazon.com, Inc. as a customer would have a material adverse effect on the Company.

﻿

Products are sold primarily in the United States and Canada directly to retailers and also through independent distributors. Although the segment has long established relationships with many of its customers, it does not have long-term supply contracts with them. The loss of, or material reduction in, sales to any of the segment's major customers could adversely affect the segment's business. The majority of the housewares and electrical appliances are sourced from vendors in the Orient. (See Note J to the Consolidated Financial Statements.)

﻿

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-13_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-13_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-03-13_item7_mdna.md, 10-K_2026-03-13_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
