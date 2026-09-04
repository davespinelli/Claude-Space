# Triage pack — SXC · SunCoke Energy, Inc.

_Generated 2026-09-04 23:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SXC · **Name:** SunCoke Energy, Inc.
- **CIK:** 0001514705
- **SIC:** 3312 — Steel Works, Blast Furnaces & Rolling Mills (Coke Ovens)
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SXC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** SunCoke Energy, Inc.
- **CIK:** 1,514,705 · **SIC:** 3312 (Steel Works, Blast Furnaces & Rolling Mills (Coke Ovens)) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 10.19 |
| mktcap | $864.9M |
| ev | $1.5B |
| ev_ebit | n/a |
| fcf | $42.3M |
| fcf_yield | 4.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -2.9% |
| net_debt | $611.2M |
| net_debt_ebit | n/a |
| cash | $42.7M |
| ltd | $653.9M |
| equity | $585.6M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.8B |
| revenue_prior | $1.9B |
| rev_growth | -5.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$44.4M |
| net_income | -$44.2M |
| cfo | $109.1M |
| capex | $66.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 84,874,850 |
| shares_py | 84,665,509 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 33.6% |
| r6m | 67.2% |
| off_52w_high | -3.6% |
| adv20 | $11.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.49 |
| r_ev_ebit | 0.00 |
| r_roic | 0.23 |
| r_rev_growth | 0.18 |
| r_buyback | 0.61 |
| score | 0.35 |

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
| rank | 365 |

**Screen rationale:** 12-1 momentum 33.6%


## 3. Share count trend

- Shares outstanding: **84,874,850** (CY2026Q2I) vs **84,665,509** prior year (CY2025Q2I)
- Change: **0.2%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 27,500 sh / $158,918 vs sells 0 sh / $0 -> net $158,918 (BUYING).
Distinct insiders buying (code P): 3. Largest buy: Hardesty Phillip Michael bought 12,209 sh @ $5.83 ($71,178) on 2026-02-25.

Form 4 filings parsed: 12; transaction rows: 42 (open-market buys 5, sales 0).

| code | rows |
|---|---|
| A | 8 |
| D | 3 |
| F | 6 |
| J | 2 |
| M | 18 |
| P | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'SUNCOKE ENERGY, INC. REPORTS SECOND QUARTER 2026 RESULTS'; skipped 11 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (sxcearningsrelease2026q2.htm)

SUNCOKE ENERGY, INC. REPORTS SECOND QUARTER 2026 RESULTS

• Second quarter 2026 net income was $15.6 million, compared to $3.5 million in the prior year period; second quarter 2026 net income attributable to SXC was $13.1 million, or $0.15 per diluted share, compared to $1.9 million, or $0.02 per diluted share in the prior year period

• Consolidated Adjusted EBITDA (1) for the quarter was $69.6 million, compared to $43.6 million in the prior year period

• Declared a cash dividend of $0.12 per share, representing the Company's 28th consecutive quarterly dividend, payable on September 2, 2026

• Middletown turbine resumed operations and power generation

• Increasing full-year 2026 Consolidated Adjusted EBITDA (1) guidance range to $250 million - $265 million

LISLE, Ill. (July 30, 2026) - SunCoke Energy, Inc. (NYSE: SXC) today reported results for the second quarter 2026, reflecting strong operational and financial performance.

"Our second quarter results reflect very strong operating performance from our Industrial Services and Domestic Coke businesses," said Katherine Gates, President and Chief Executive Officer of SunCoke Energy, Inc. "Industrial Services had its best quarter to date for Adjusted EBITDA since the acquisition of Phoenix, while our Domestic Coke segment benefited from favorable coal-to-coke yields due to improved operating conditions. Additionally, we successfully returned the Middletown turbine to service in May." Gates continued, "We expect this strong performance to continue, and with solid outlooks for both business segments throughout the second half of the year, we are increasing our full-year 2026 Consolidated Adjusted EBITDA guidance range to $250 million to $265 million."

(1) See definition of Adjusted EBITDA and reconciliation to GAAP elsewhere in this release.

SECOND QUARTER CONSOLIDATED RESULTS

Three Months Ended June 30,
(Dollars in millions) | 2026 | 2025 | Increase (decrease)
Revenues | 475.3 | 434.1 | 41.2
Net income attributable to SXC | 13.1 | 1.9 | 11.2
Adjusted EBITDA (1) | 69.6 | 43.6 | 26.0

(1) See definition of Adjusted EBITDA and reconciliation to United States generally accepted accounting principles ("GAAP") elsewhere in this release.

Revenues in the second quarter of 2026 increased $41.2 million as compared to the same prior year period, primarily driven by the addition of Phoenix, partially offset by lower blast coke sales volumes due to the shutdown of our Haverhill I cokemaking facility, the pass-through of lower coal prices on our long-term, take-or-pay agreements, and lower energy sales due to the Middletown cokemaking facility turbine failure.

Net income attributable to SXC increased $11.2 million as compared to the same prior year period, primarily driven by the inclusion of Phoenix results and higher terminals handling volumes.

Adjusted EBITDA increased $26.0 million as compared to the same prior year period, primarily driven by the inclusion of Phoenix, higher terminals handling volumes due to improved market conditions, and favorable coal-to-coke yields due to improved operating conditions, partially offset by lower coke sales volumes due to the shutdown of our Haverhill I cokemaking facility.

SECOND QUARTER SEGMENT RESULTS

Domestic Coke

Domestic Coke consists of cokemaking facilities and heat recovery operations at our Jewell, Indiana Harbor, Haverhill II, Granite City and Middletown plants.

Three Months Ended June 30,
(Dollars in millions, except per ton amounts) | 2026 | 2025 | Increase (decrease)
Revenues | 367.5 | 410.4 | (42.9)
Adjusted EBITDA (1) | 42.5 | 40.5 | 2.0
Sales volumes (thousands of tons) | 878 | 943 | (65)
Adjusted EBITDA per ton (2) | 48.41 | 42.95 | 5.46

(1) See definition of Adjusted EBITDA elsewhere in this release.

(2) Reflects Domestic Coke Adjusted EBITDA divided by Domestic Coke sales volumes.

Revenues in the second quarter of 2026 decreased $42.9 million as compared to the same prior year period, primarily driven by lower blast coke sales volumes due to the shutdown of our Haverhill I cokemaking facility, the pass-through of lower coal prices on our long-term, take-or-pay agreements, and lower energy sales due to the Middletown cokemaking facility turbine failure.

Adjusted EBITDA in the second quarter of 2026 increased $2.0 million as compared to the same prior year period, primarily driven by favorable coal-to-coke yields due to improved operating conditions, partially offset by lower blast coke sales volumes due to the shutdown of our Haverhill I cokemaking facility.

Industrial Services

Industrial Services consists of the handling and mixing services of coal and other aggregates at our logistics terminals, including Convent Marine Terminal ("CMT"), Lake Terminal, and Kanawha River Terminals ("KRT"), and fifteen molten slag removal, handling, and processing operating sites in four countries.

Three Months Ended June 30,
(Dollars in millions, except per ton amounts) | 2026 | 2025 | Increase (decrease)
Revenues | 98.4 | 15.1 | 83.3
Intersegment sales | 5.8 | 5.9 | (0.1)
Adjusted EBITDA (1) | 34.4 | 7.7 | 26.7
Terminals handling volumes (thousands of tons) (2) | 6,672 | 4,746 | 1,926
Steel customer volumes serviced (thousands of tons) (3) | 5,763 | — | 5,763

(1) See definition of Adjusted EBITDA elsewhere in this release.

(2) Reflects inbound tons handled during the period.

(3) Reflects volumes serviced in the form of slag handling, metal recovery, scrap preparation, and other mill services.

Revenues and Adjusted EBITDA increased in the second quarter of 2026 by $83.3 million and $26.7 million, respectively, as compared to the same prior year period, primarily driven by the addition of Phoenix results and higher terminals handling volumes.

Corporate and Other

Corporate expenses that can be identified with a segment have been included in determining segment results. The remainder is included in Corporate and Other, which is not a reportable segment, but which also includes licensing and operating fees payable to us under long-term contracts with ArcelorMittal Brazil as well as the expenses related to those operations and activity from our legacy coal mining business.

Corporate and Other Adjusted EBITDA, which includes results from our legacy coal mining business and Brazil cokemaking business, was an expense of $7.3 million during the second quarter of 2026, compared to an expense of $4.6 million during the second quarter of 2025, primarily driven by higher employee related costs.

2026 REVISED OUTLOOK

Our 2026 revised guidance is as follows:

• Domestic coke total sales are expected to be approximately 3.4 million tons (1)

• Consolidated Net Income is expected to be between $23 million and $42 million

• Consolidated Adjusted EBITDA is expected to be between $250 million and $265 million

• Capital expenditures are projected to be between $90 million and $100 million

• Operating cash flow is estimated to be between $240 million and $260 million

• Net cash tax receipts are projected to be between $8 million and $12 million

Disclaimer: The Company's 2026 outlook and guidance are based on the Company's current estimates and assumptions that are subject to change and may be outside the control of the Company. If actual results vary from these estimates and assumptions, the Company's expectations may change. There can be no assurances that SunCoke will achieve the results expressed by this outlook and guidance.

(1) The production of foundry coke does not replace blast furnace coke on a ton for ton basis, resulting in a difference between guidance of ~3,400Kt coke sales (inclusive of foundry and blast) versus the stated Domestic Coke blast furnace equivalent capacity of ~3,690Kt

RELATED COMMUNICATIONS

We will host our quarterly earnings call at 11:00 am ET (10:00 a.m. CT) today. The conference call will be webcast live at https://app.webinar.net/bYkw7yWOJmd and archived for replay in the Investors section of www.suncoke.com. Investors and analysts may participate in this call by dialing 1-800-715-9871 in the U.S. or 1-646-307-1963 if outside the U.S., conference ID 5888042.

SUNCOKE ENERGY, INC.

SunCoke Energy, Inc. (NYSE: SXC) supplies high-quality coke to domestic and international customers. Our coke is used in the blast furnace production of steel as well as the foundry production of casted iron, with the majority of sales under long-term, take-or-pay contracts. We also export coke to overseas customers seeking high-quality product for their blast furnaces. Our process utilizes an innovative heat-recovery technology that captures excess heat for steam or electrical power generation and draws upon more than 60 years of cokemaking experience to operate our facilities in Illinois, Indiana, Ohio, Virginia and Brazil. Our industrial services business provides export and domestic material handling services to coke, coal, steel, power and other bulk customers, as well as mission-critical services to leading steel producers globally. The logistics terminals have the collective capacity to mix and transload more than 40 million tons of material each year and are strategically located to reach Gulf Coast, East Coast, Great Lakes and international ports. Additional industrial services include the removal, handling, and processing of molten slag at customer sites, as well as preparation and transportation of metal scraps, raw materials, and finished products. To learn more about SunCoke Energy, Inc., visit our website at www.suncoke.com.

SunCoke routinely announces material information to investors and the marketplace using press releases, Securities and Exchange Commission filings, public conference calls, webcasts, sustainability reports, and SunCoke's website at https://www.suncoke.com/en/investors/overview. The information that SunCoke posts to its website may be deemed to be material. Accordingly, SunCoke encourages investors and others interested in SunCoke to routinely monitor and review the information that SunCoke posts on its website, in addition to following SunCoke's press releases, Securities and Exchange Commission filings, sustainability reports, and public conference calls and webcasts.

NON-GAAP FINANCIAL MEASURES

In addition to U.S. GAAP measures, this press release contains certain non-GAAP financial measures. These non-GAAP financial measures should not be considered as alternatives to the measures derived in accordance with U.S. GAAP. Non-GAAP financial measures have important limitations as analytical tools, and you should not consider them in isolation or as substitutes for results as reported under U.S. GAAP. Additionally, other companies may calculate non-GAAP metrics differently than we do, thereby limiting their usefulness as a comparative measure. Because of these and other limitations, you should consider our non-GAAP measures only as supplemental to other U.S. GAAP-based financial performance measures, including revenues and net income. Reconciliations to the most comparable GAAP financial measures are included following the presentation of financial and operating results included at the end of this press release.

DEFINITIONS

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-20_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Consolidated Results of Operations

The following section includes year-over-year analysis of consolidated results of operations for the year ended December 31, 2025 as compared to the year ended December 31, 2024. See "Analysis of Segment Results" later in this Item 7 for further details of these results. Refer to "Management's Discussion and Analysis of Financial Condition and Results of Operations" in our 2024 Annual Report on Form 10-K for the year-over-year analysis of consolidated results of operations for the year ended December 31, 2024 as compared to the year ended December 31, 2023.

Years Ended December 31,
2025 | 2024 | Increase (Decrease)
(Dollars in millions)
Revenues
Sales and other operating revenue | 1,837.3 | 1,935.4 | (98.1)
Costs and operating expenses
Cost of products sold and operating expenses | 1,553.0 | 1,603.4 | (50.4)
Selling, general and administrative expenses | 84.8 | 61.2 | 23.6
Depreciation and amortization expense | 153.6 | 118.9 | 34.7
Long-lived asset impairment | 90.3 | — | 90.3
Total costs and operating expenses | 1,881.7 | 1,783.5 | 98.2
Operating (loss) income | (44.4) | 151.9 | (196.3)
Interest expense, net | 28.4 | 23.4 | 5.0
(Loss) income before income tax (benefit) expense | (72.8) | 128.5 | (201.3)
Income tax (benefit) expense | (34.0) | 25.0 | (59.0)
Net (loss) income | (38.8) | 103.5 | (142.3)
Less: Net income attributable to noncontrolling interests | 5.4 | 7.6 | (2.2)
Net (loss) income attributable to SunCoke Energy, Inc. | (44.2) | 95.9 | (140.1)

Sales and Other Operating Revenue and Costs of Products Sold and Operating Expenses. Sales and other operating revenue and costs of products sold and operating expenses decreased during 2025 compared to the same prior year period, driven by lower pricing in our Domestic Coke segment mainly driven by the mix of contracted and non-contracted blast coke sales in the current year period, lower contracted coke tons delivered due to Algoma Steel's breach of contract, the impact of the Granite City contract extension economics and the impact of the pass-through of lower coal prices on our long-term, take-or-pay agreements. Additionally, sales and other operating revenue during 2025 were negatively impacted by lower volumes due to unfavorable coal-to-coke yields. The decreases in sales and other operating revenue and costs of products sold and operating expenses were partially offset by the inclusion of five months of Phoenix Global results.

Selling, General and Administrative Expenses. S elling, general and administrative expenses increased during 2025, reflecting transaction costs of $10.1 million incurred related to the acquisition of Phoenix Global as well as the absence of a $9.5 million gain, which was the result of the extinguishment of certain liabilities related to our legacy coal mining business in the prior year period. See Note 13 to our consolidated financial statements for further detail. Additionally, s elling, general and administrative expenses during 2025 further increased due to the inclusion of Phoenix Global's costs in the current year period. These increased costs were partially offset by lower employee related expenses and lower legal expenses in the current year period.

Depreciation and Amortization Expense. The increase to depreciation and amortization expense during 2025 reflects the inclusion of Phoenix Global's expense in the current year period. This increase was partially offset by the expiration of the useful lives of assets in our Domestic Coke segment placed into service in prior periods.

Long-lived Asset Impairment. During the fourth quarter of 2025, a triggering event occurred requiring a review for impairment at our Haverhill I cokemaking facility, which resulted in a $90.1 million impairment charge. See Note 7 to our consolidated financial statements for further detail.

Interest Expense, net. Interest expense, net, during 2025 increased as a result of interest incurred on Revolving Facility borrowings related to the acquisition of Phoenix Global.

Income Tax (Benefit) Expense. Income tax (benefit) expense during 2025 benefited from an analysis conducted as part of tax planning on the Company's capital investments under Section 48 of the Internal Revenue Code as well as the income tax impact of the Haverhill I long-lived asset impairment charge, which resulted in a net tax benefit. This benefit was partially offset by nondeductible transaction costs in connection with the acquisition of Phoenix Global. See Note 5 to our consolidated financial statements for further detail.

Noncontrolling Interest. Net i ncome attributable to noncontrolling interests represents a 14.8 percent third-party interest in our Indiana Harbor cokemaking facility and fluctuates with the financial performance of that facility.

Results of Reportable Business Segments

Following the acquisition of Phoenix Global and as discussed in Note 20 – Business Segment Information, we updated our reportable segments and have recast all segment information for all prior periods presented herein to reflect this change.

We report our business results through two reportable segments:

• Domestic Coke consists of our Jewell facility, located in Virginia, our Indiana Harbor facility, located in Indiana, our Granite City facility located in Illinois, and our Middletown and Haverhill facilities located in Ohio.

• Industrial Services consists of logistics terminals including CMT, located in Louisiana, KRT, located in West Virginia, and Lake Terminal, located in Indiana. Lake Terminal is located adjacent to our Indiana Harbor cokemaking facility. Additionally, Industrial Services includes fifteen molten slag removal, handling and processing operating sites across the United States, Brazil, Slovakia and Spain.

Corporate expenses that can be identified with a segment have been included in determining segment results. The remainder is included in Corporate and Other, including licensing and operating fees payable to us under long-term contracts with ArcelorMittal Brazil as well as the expenses related to those operations and activity from our legacy coal mining business, which is not considered a reportable segment and therefore, not included in our segment information in Note 20. However, we have included Corporate and Other within our operating data below.

Management believes Adjusted EBITDA is an important measure of operating performance, which is used by the chief operating decision maker as one of the measurements to help determine the allocation of costs and resources to our reportable segments. Adjusted EBITDA should not be considered a substitute for the reported results prepared in accordance with GAAP. See the "Non-GAAP Financial Measures" section for both the definition of Adjusted EBITDA and the reconciliation from GAAP to the non-GAAP measurement.

Segment Operating Data

The following table sets forth financial and operating data by segment for the years ended December 31, 2025 and 2024:
Years Ended December 31,
2025 | 2024 | Increase (Decrease)
(Dollars in millions, except per ton amounts)
Sales and other operating revenue:
Domestic Coke | 1,613.8 | 1,817.3 | (203.5)
Industrial Services | 187.8 | 83.0 | 104.8
Industrial Services intersegment sales | 21.9 | 22.9 | (1.0)
Elimination of intersegment sales | (21.9) | (22.9) | 1.0
Total sales and other operating revenue reportable segments | 1,801.6 | 1,900.3 | (98.7)
Corporate and other, net (1) | 35.7 | 35.1 | 0.6
Total Sales and other operating revenue | 1,837.3 | 1,935.4 | (98.1)
Adjusted EBITDA:
Domestic Coke | 170.0 | 234.7 | (64.7)
Industrial Services | 62.3 | 50.4 | 11.9
Total Adjusted EBITDA reportable segments | 232.3 | 285.1 | (52.8)
Corporate and Other, net (1) | (13.1) | (12.3) | (0.8)
Total Adjusted EBITDA (2) | 219.2 | 272.8 | (53.6)
Coke Operating Data:
Domestic Coke capacity utilization (3) | 93 | % | 100 | % | (7) | %
Domestic Coke production volumes (thousands of tons) | 3,749 | 4,032 | (283)
Domestic Coke sales volumes (thousands of tons) | 3,668 | 4,028 | (360)
Domestic Coke Adjusted EBITDA per ton (4) | 46.35 | 58.27 | (11.92)
Industrial Services Operating Data:
Terminals handling volumes (thousands of tons) | 20,320 | 22,540 | (2,220)
Steel customer volumes serviced (thousands of tons) | 9,223 | — | 9,223

(1) Corporate and Other, net is not a reportable segment and includes the results of Brazil cokemaking operations.

(2) See the "Non-GAAP Financial Measures" section below for both the definition of Adjusted EBITDA and the reconciliation from GAAP to the non-GAAP measurement.

(3) The production of foundry coke tons does not replace blast furnace coke tons on a ton for ton basis, as foundry coke requires longer coking time. The Domestic Coke capacity utilization is calculated assuming a single ton of foundry coke replaces approximately two tons of blast furnace coke.

(4) Reflects Domestic Coke Adjusted EBITDA divided by Domestic Coke sales volumes.

Analysis of Segment Results

Domestic Coke

The following table explains year-over-year changes in our Domestic Coke segment's sales and other operating revenues and Adjusted EBITDA results:
Sales and other operating revenue | Adjusted EBITDA
2025 vs 2024 | 2025 vs 2024
(Dollars in millions)
Beginning | 1,817.3 | 234.7
Volume (1) | (151.1) | (45.0)
Price (2) | (55.8) | (39.8)
Operating and maintenance costs (3) | N/A | 12.9
Energy and other (4) | 3.4 | 7.2
Ending | 1,613.8 | 170.0

(1) Volumes during 2025 were negatively impacted by lower coal-to-coke yields, lower contracted coke tons delivered due to Algoma Steel's breach of contract and lower coke tons in the Granite City contract extension.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-20_item1_business.md)

Item 1. Business

Overview

SunCoke Energy, Inc. ("SunCoke Energy," "SunCoke," "Company," "we," "our" and "us") is the largest independent producer of high-quality coke in the Americas, as measured by tons of coke produced each year, and has more than 65 years of coke production experience. Coke is produced by heating metallurgical coal in a refractory oven, which releases certain volatile components from the coal, thus transforming the coal into coke. Our coke is primarily used as a principal raw material in the blast furnace steelmaking process as well as in the foundry production of casted iron, and the majority of our sales are derived from blast furnace coke sales made under long-term, take-or-pay agreements. We also sell coke produced utilizing capacity in excess of that reserved for our long-term, take-or-pay agreements to customers in both the export and North American domestic coke markets seeking high-quality product for their blast furnaces. We have designed, developed and built, and we currently own and operate five cokemaking facilities in the United States ("U.S.") with collective nameplate capacity to produce approximately 3.7 million tons of blast furnace coke per year. Additionally, we designed and currently operate one cokemaking facility in Brazil under licensing and operating agreements on behalf of ArcelorMittal Brasil S.A. ("ArcelorMittal Brazil"), which has approximately 1.7 million tons of annual cokemaking capacity.

We also own and operate an industrial services business that provides export and domestic material handling and/or mixing services to coke, coal, steel, power and other bulk customers, as well as mission-critical mill services to leading steel producers globally. Our logistics terminals have the collective capacity to mix and transload more than 40 million tons of coal and other products annually and have storage capacity of approximately 3 million tons. These terminals are strategically located to reach Gulf Coast, East Coast, Great Lakes and international ports. Industrial services also include the removal, handling, and processing of molten slag at customer sites, as well as preparation and transportation of metal scraps, raw materials, and finished products.

We report our business results through two reportable segments: Domestic Coke and Industrial Services.

Domestic Coke

Our Domestic Coke segment consists of cokemaking facilities and heat recovery operations at our Jewell, Indiana Harbor, Haverhill, Granite City and Middletown plants. Our core business model is predicated on providing steelmakers an alternative to investing capital in their own captive coke production facilities and to serve as the long-term supplier of high quality coke by investing in our facilities with leading technology, as well as safety and environmental performance. Our cokemaking ovens utilize efficient, modern heat recovery technology designed to combust the coal's volatile components during the cokemaking process and use the hot flue gas to generate steam and electricity for sale through steam generation facilities or cogeneration plants, respectively. This differs from by-product cokemaking, which repurposes the coal's volatile components for other uses. Steam generated is generally sold to customers pursuant to steam supply and purchase agreements, and electricity generated is generally sold into the regional power market or to customers pursuant to energy sales agreements.

We believe our advanced heat recovery cokemaking process has numerous advantages over by-product cokemaking, including producing higher quality coke, using waste heat to generate derivative energy for resale, and reducing the environmental footprint. The Clean Air Act Amendments of 1990 specifically directed the U.S. Environmental Protection Agency ("EPA") to evaluate our heat recovery coke oven technolog y as a basis for establishing Maximum Achievable Control Technology ("MACT") standards for new cokemaking facilities. In addition, each of the four cokemaking facilities that we have built since 1990 has either met or exceeded the applicable Best Available Control Technology ("BACT"), or Lowest Achievable Emission Rate ("LAER") standards, as applicable, set forth by the EPA for cokemaking facilities. We have constructed the only greenfield cokemaking facilities in the U.S. in over 35 years and are the only North American coke producer that utilizes heat recovery technology in the cokemaking process.

The following table sets forth information about our cokemaking facilities:
Facility | Location | Year of Start Up | Use of Waste Heat | Number of Coke Ovens | Annual Cokemaking Nameplate Capacity (1) (thousands of tons) | Customer (2) | Contract Expiration | Contract Volume (thousands of tons)
Owned and Operated:
Middletown (3) | Middletown, Ohio | 2011 | Power generation | 100 | 550 | Cliffs Steel | December 2032 | Capacity
Granite City | Granite City, Illinois | 2009 | Steam for power generation | 120 | 650 | U.S. Steel | December 2026 | Capacity (4)
Indiana Harbor | East Chicago, Indiana | 1998 | Heat for power generation | 268 | 1,220 | Cliffs Steel | September 2035 | Capacity
Haverhill II | Franklin Furnace, Ohio | 2008 | Power generation | 100 | 550 | Cliffs Steel/Algoma Steel (5) | December 2028 (6) /December 2026 | 500/150
Jewell | Vansant, Virginia | 1962 | Partially used for coal drying | 142 | 720
Total (7) | 730 | 3,690
Operated:
Vitória | Vitória, Brazil | 2007 | Steam for power generation | 320 | 1,700 | ArcelorMittal Brazil | January 2028 | Capacity
Total | 1,050 | 5,390

(1) Cokemaking nameplate capacity represents stated capacity for production of blast furnace coke equivalent production. The production of foundry coke tons does not replace blast furnace coke tons on a ton for ton basis, as foundry coke requires longer coking time.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-20_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-20_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-20_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-30_2-02-results.md, 10-K_2026-02-20_item7_mdna.md, 10-K_2026-02-20_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
