# Triage pack — BW · Babcock & Wilcox Enterprises, Inc.

_Generated 2026-09-05 03:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** BW · **Name:** Babcock & Wilcox Enterprises, Inc.
- **CIK:** 0001630805
- **SIC:** 3433 — Heating Equipment, Except Electric & Warm Air Furnaces
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE, NYSE, NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/BW

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Babcock & Wilcox Enterprises, Inc.
- **CIK:** 1,630,805 · **SIC:** 3433 (Heating Equipment, Except Electric & Warm Air Furnaces) · **Exchange:** NYSE,NYSE,NYSE

**Debt data:** OK — long-term debt from us-gaap:SecuredLongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 7.13 |
| mktcap | $1.1B |
| ev | $901.4M |
| ev_ebit | 43.5x |
| fcf | -$85.7M |
| fcf_yield | -8.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$160.7M |
| net_debt_ebit | -7.8x |
| cash | $308.6M |
| ltd | $147.9M |
| equity | $57.4M |
| ltd_tag | SecuredLongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $587.7M |
| revenue_prior | $581.0M |
| rev_growth | 1.1% |
| rev_growth_note | share count +47.3% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $20.7M |
| net_income | -$32.8M |
| cfo | -$68.9M |
| capex | $16.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 47.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 148,965,066 |
| shares_py | 101,097,542 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 274.8% |
| r6m | -46.4% |
| off_52w_high | -67.4% |
| adv20 | $52.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.09 |
| r_ev_ebit | 0.16 |
| r_roic | 0.50 |
| r_rev_growth | 0.39 |
| r_buyback | 0.04 |
| score | 0.19 |

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
| rank | 470 |

**Screen rationale:** share count +47.3% yoy — growth may be acquisition/issuance-driven, not organic; net cash; 12-1 momentum 274.8%; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **148,965,066** (CY2026Q2I) vs **101,097,542** prior year (CY2025Q2I)
- Change: **47.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +47.3% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-22** — Item 5.02 (Departure of Directors or Certain Officers; Election of): Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers
- **2026-05-18** — Item 1.01 (Entry into a Material Definitive Agreement): Inc., a Delaware corporation (the "Company") entered into an an underwriting agreement, dated May 14, 2026 (the "Underwriting

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 12,000 sh / $115,050 vs sells 0 sh / $0 -> net $115,050 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Young Kenneth M bought 7,000 sh @ $9.65 ($67,550) on 2026-08-12.

Form 4 filings parsed: 12; transaction rows: 51 (open-market buys 2, sales 0).

| code | rows |
|---|---|
| A | 9 |
| D | 4 |
| F | 8 |
| G | 2 |
| M | 26 |
| P | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-10_2-02-results.md)

_Extraction: started at the first release heading, 'Babcock & Wilcox Enterprises Reports Second Quarter 2026 Results'; skipped 17 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (e-2026q2earningsrelease.htm)

Babcock & Wilcox Enterprises Reports Second Quarter 2026 Results

• Revenue in the second quarter of $319.7 million, a 130% increase compared to the same period of 2025, ahead of consensus street expectations

• Net Income was $14.3 million in the second quarter, compared to a net loss of $58.5 million in the same period of 2025, ahead of consensus street expectations

• Earnings per share of $0.07, compared to a loss per share of $0.63 in the second quarter of 2025

• Adjusted EBITDA in the second quarter of $21.8 million, a 57% increase compared to the same period of 2025, ahead of consensus street expectations

• Bookings of $151.0 million in the second quarter, a 38% increase compared to the same period of 2025

• Backlog of $2.6 billion in the second quarter, a 533% increase compared to the same period of 2025

• Secured an additional 1 gigawatt of steam turbines from Siemens Energy for fast delivery in anticipation of our next data center project

• Total global pipeline exceeds $14.0 billion

• Announced authorized share repurchase program of up to $50 million

• Announced repurchase of remaining $61.8 million of outstanding bonds due December 2026 in August 2026

Q2 2026 Financial Highlights and Outlook

– Revenue of $319.7 million, compared to revenue of $138.9 million in the second quarter of 2025

– Net income of $14.3 million, compared to a net loss of $58.5 million in the second quarter of 2025

– Adjusted Net Income, which excludes non-cash warrants and other stock costs, was $9.1 million in the second quarter

– Earnings per share of $0.07, compared to a loss per share of $0.63 in the second quarter of 2025

– Adjusted EBITDA of $21.8 million, compared to adjusted EBITDA of $13.9 million in the second quarter of 2025

– Company raises full year 2026 Adjusted EBITDA target range to $80.0 million to $105.0 million

(AKRON, Ohio – August 10, 2026) – Babcock & Wilcox Enterprises, Inc. ("B&W", "Babcock & Wilcox" or the "Company") (NYSE: BW) announced its financial results for the second quarter of 2026.

"During the second quarter of 2026, we delivered strong operating results while displaying continued core business momentum, as second quarter revenue, net income and Adjusted EBITDA exceeded Company and consensus street expectations. The growing need for reliable electricity from AI data centers, utilities, industrial customers and expanding economies is accelerating investment in power generation capacity, driving strong demand for our core parts and services, environmental technologies as well as coal and natural gas-fired generation solutions," commented Kenneth Young, B&W's Chairman and Chief Executive Officer. "We continue active discussions on other AI data center opportunities and have placed additional orders with Siemens Energy to secure and deliver an additional 1 gigawatt of steam turbines in

the next 12 to 15 months to secure speed to markets. This increase in global energy demand positions us for sustained success across our higher-margin Global Parts and Services business and provides B&W with a strong outlook for the second half of 2026 and beyond. Continued execution of our strategic objectives is delivering results, positioning B&W to capitalize on strong global demand for baseload generation and behind-the-meter data center projects."

"Additionally, our first data center project with Base Electron is progressing ahead of expectations and on budget, and manufacturing of the boilers and steam turbines and other long-lead-time components are progressing quickly. The permitting process is underway as we work to provide our proven natural gas-fired boilers and related technologies, alongside Siemens Energy steam turbine systems. This progression with Base Electron further demonstrates our ability to rapidly deploy power solutions, which is a key differentiator that enhances our competitive position in pursuing other data center opportunities."

"During the second quarter of 2026, our strong financial results included meaningful growth in net income as well as robust development of our bookings and backlog. As our business expands, we continue hiring in our engineering, business and project development organizations as well as increasing availability of qualified skilled welders and electricians. We are continuing to experience positive momentum at B&W, as we continue to convert our global pipeline of identified project opportunities. In July, we announced that our Board of Directors authorized a share repurchase program of up to $50 million, which reflects confidence in our balance sheet and our strategic approach to building shareholder value. In addition, we have raised the upper end of our 2026 Adjusted EBITDA target range to $80.0 million to $105.0 million, reflecting the continued momentum across our business and confidence in additional opportunities ahead. We remain intently focused on our strategic vision and remain optimistic that we will continue to execute on our existing pipeline while maintaining viability for future expansion as we move forward."

Q2 2026 Financial Summary

Revenues in the second quarter of 2026 were $319.7 million versus revenues of $138.9 million in the second quarter of 2025, primarily driven by an increase in large project volume, including $100.7 million from Base Electron. Operating income in the second quarter of 2026 was $11.8 million, compared to operating income of $7.0 million in the second quarter of 2025. Net income in the second quarter of 2026 was $14.3 million, compared to a net loss of $58.5 million in the second quarter of 2025, driven by the improvement in the operating income results. We benefited from a reduction to interest expense of $6.0 million, change in fair value of customer warrants of $5.9 million and a decrease to tax expense of $5.1 million. Earnings per share in the second quarter of 2026 was $0.07 compared to a loss per share of $0.63 in the second quarter of 2025. Adjusted EBITDA was $21.8 million, an increase compared to $13.9 million in the second quarter of 2025.

Reconciliations of the non-GAAP measures of Adjusted EBITDA and adjusted net income (loss) to the most directly comparable GAAP measures are provided in the exhibits to this release. See "Bookings and Backlog" below for important information regarding our calculation and presentation of those metrics.

Liquidity and Balance Sheet

At June 30, 2026, the Company had secured debt and bonds of $239.8 million, and a cash, cash equivalents and restricted cash balance of $382.8 million. During the quarter B&W announced the repurchase of the remaining $61.8 million of outstanding December 2026 bonds in August 2026.

Earnings Call Information

B&W plans to host a conference call and webcast on Monday, August 10, 2026 at 5 p.m. ET to discuss the Company's second quarter 2026 results. The listen-only audio of the conference call will be broadcast live via the Internet on B&W's Investor Relations site. The dial-in number for participants in the U.S. is (833) 461-5787; the dial-in number for participants in Canada is (365) 657-4084; the dial-in number for participants in all other locations is (585) 542-9983. The conference ID for all participants is 808869498. A replay of this conference call will remain accessible in the investor relations section of the Company's website for a limited time.

Non-GAAP Financial Measures

The Company uses non-GAAP financial measures internally, also referred to in this release as "adjusted" financial measures, to evaluate its performance and in making financial and operational decisions. When viewed in conjunction with GAAP results and the accompanying reconciliation, the Company believes that its presentation of these measures provides investors with greater transparency and a greater understanding of factors affecting its financial condition and results of operations than GAAP measures alone. The presentation of non-GAAP financial measures should not be considered in isolation or as a substitute for the Company's related financial results prepared in accordance with GAAP.

Adjusted EBITDA on a consolidated basis is a non-GAAP metric and is calculated as earnings before interest expense, tax, depreciation and amortization adjusted for items such as gains or losses arising from the sale of non-income producing assets, net pension benefits, stock-based compensation, restructuring activities, impairments, gains and losses on debt extinguishment, legal and settlement costs, and costs related to financial consulting. In addition, the Company presents consolidated Adjusted EBITDA because it believes it is useful to investors to help facilitate comparisons of the ongoing, operating performance before overhead and other expenses not attributable to the operating performance of the Company.

The Company also presents the non-GAAP financial measure of adjusted net income, which excludes $(5.2) million of non-cash warrants and other stock-related costs, as management believes it is a useful measure for investors to accurately reflect the impact of recent stock price growth on costs related to customer warrants and stock-based compensation.

This release also presents certain targets for the Company's Adjusted EBITDA in the future; these targets are not intended as guidance regarding how the Company believes the business will perform. The Company is unable to reconcile these targets to their GAAP counterparts without unreasonable effort and expense. Prior period results have been revised to conform with the revised definition and present separate reconciling items in our reconciliation, including business transition costs.

Bookings and Backlog

Bookings and backlog are our measures of remaining performance obligations under our sales contracts. It is possible that our methodology for determining bookings and backlog may not be comparable to methods used by other companies.

We generally include expected revenue from contracts in our backlog when we receive written confirmation from our customers authorizing the performance of work and committing the customers to payment for work performed. Backlog may not be indicative of future operating results, and contracts in our backlog may be canceled, modified or otherwise altered by customers. Backlog can vary significantly from period to period, particularly when large new-build projects or operations and maintenance contracts

are booked because they may be fulfilled over multiple years. Because we operate globally, our backlog is also affected by changes in foreign currencies each period. We do not include orders of our unconsolidated joint ventures in backlog.

Bookings represent changes to the backlog. Bookings include additions from booking new business, subtractions from customer cancellations or modifications, changes in estimates of liquidated damages that affect selling price and revaluation of backlog denominated in foreign currency. We believe comparing bookings on a quarterly basis or for periods less than one year is less meaningful than for longer periods and that shorter-term changes in bookings may not necessarily indicate a material trend.

Pipeline

Pipeline represents our uncontracted, potential opportunities, which have been identified and are in active discussions, that could reach a decision to proceed over the next 36 months. Pipeline is an internal metric monitored by management to understand the anticipated growth of our Company and our estimated future revenue, which may increase or decrease from time to time.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-16_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

BUSINESS OVERVIEW

We are a globally focused energy technologies provider with nearly 160 years of experience providing diversified energy and emissions control solutions to a broad range of industrial, electrical utility, municipal and other customers. Our innovative products and services are organized in one reporting segment. For a description of our reportable segment see Item 1, Business of this Form 10-K.

Customer demand is heavily affected by the variations in our customers' business cycles, power demand in their operating territories, and by the overall economies, energy, environmental and regulatory requirements of the countries in which they

operate.

We have manufacturing facilities in Canada, Mexico and the United States. Many aspects of our operations and properties could be affected by political developments, environmental regulations and operating risks. These and other factors may have a material impact on our international and domestic operations or our business as a whole.

Through our restructuring efforts, we have made and will continue working to make significant progress reducing costs and improving profitability. We continue to explore other cost saving initiatives and in conjunction with top-line growth driven by opportunities for our core technologies, we will continue to improve cash generation and strengthen our liquidity. These initiatives have been and may continue to be important factors that could cause our actual results to differ materially from those indicated in these financial statements. If one or more events related to these or other risks or uncertainty materialize, or if our underlying assumptions prove to be incorrect, actual results may differ materially from what we anticipate.

Discontinued Operations

ASH

On October 31, 2025, we completed a sale of the net assets comprising our ASH business for $29 million, subject to customary fees and adjustments and recorded a gain of $21.5 million on the sale. For more information on this sale, see Note 4 to the Consolidated Financial Statements.

The revenue and operating results presented for ASH for the year ended December 31, 2025 represent the financial results for January through October 2025 operations. While there is a slight decline in revenue for 2025 compared to prior years, operating margins are consistent at approximately 28%.

Diamond Power

On July 31, 2025, we closed the sale of our Diamond Power business for a base purchase price of $177 million, subject to certain offsets and adjustments. We recorded a gain of $53.2 million on the sale. For more information on this sale, see Note 4 to the Consolidated Financial Statements.

The revenue and operating results presented for Diamond Power for the year ended December 31, 2025 represent the financial results for January through July 2025 operations. Revenue and operating margins are lower in 2025 compared to 2024 and 2023 due to the sale closing in July 2025 and related transaction costs incurred.

Vølund

On April 29, 2025, we sold our Vølund business for a base purchase price equal to $15.0 million plus $0.1 million (400,000 Danish krone). We recorded a net loss of $36.8 million, which included a write off of CTA of $52.6 million. For more information, see Note 4 to the Consolidated Financial Statements.

The revenue and operating results for the year ended December 31, 2025 primarily represent the financial results for January through April 2025 operations as well as the net loss on the sale primarily from the write off of CTA. The decrease in revenue and operating margin is a result of the slowdown in sales and engagement of projects toward the end of 2024 and into 2025 as the Company engaged in the sale of the business.

B&W Solar

During the third quarter of 2023, we committed to a plan to sell our B&W Solar business, resulting in a significant change that would impact our operations. As of September 30, 2023, we met all of the criteria for the assets and liabilities of this business to be accounted for as held for sale. In addition, we also determined that the operations of the B&W Solar business qualified as a discontinued operation, primarily based upon its significance to our current and historic operating losses. The decision to sell the B&W Solar business, along with the significant increase in estimated costs to complete the B&W Solar loss contracts, resulted in a triggering event that required us to immediately perform certain valuations. Certain trade accounts receivable and contract assets were determined to be uncollectible, resulting in charges of $17.6 million. During 2023, we recognized an impairment of $56.6 million, or the entire balance of goodwill associated with B&W Solar. These charges have been included in Loss from discontinued operations, net of tax in the Consolidated Statements of Operations. The decrease in revenue and operating margin is a result of the focus on the sale of the business in 2024 and 2025.

During the fourth quarter of 2025, we discontinued marketing B&W Solar for sale due to lack of potential buyers and terminated our broker arrangement with a third party provider. As of December 31, 2025, B&W Solar was disposed of through abandonment, as we ceased all business operations and either transferred or wrote off its remaining assets. As a result, the B&W Solar business no longer meets the criteria of held for sale as of December 31, 2025, but continues to meet the criteria for discontinued operations for all periods presented.

BWRS, SPIG and GMAB

In addition to the ASH, Diamond Power, V ø lund and B&W Solar businesses, discontinued operations include the following subsidiaries divested in 2024: BWRS, SPIG, and GMAB. These sale transactions were part of a previously announced strategy to divest certain non-core businesses to reduce our debt, improve our balance sheet and increase liquidity. Results of operations and cash flows for these businesses and the financial position of the divested subsidiaries are reported as discontinued operations for all periods presented and the notes to the financial statements have been adjusted on a retrospective basis. For more information, see Note 4 to the Consolidated Financial Statements.

RESULTS OF OPERATIONS–YEARS ENDED DECEMBER 31, 2025, 2024 AND 2023

Consolidated Results of Operations

The following discussion is of our consolidated results of operations below.

Year ended December 31,
(in thousands) | 2025 | 2024 | $ Change
Revenues | 587,676 | 581,039 | 6,637
Costs and expenses:
Cost of operations | 443,825 | 454,326 | (10,501)
Selling, general and administrative expenses | 119,481 | 124,541 | (5,060)
Research and development costs | 1,457 | 5,133 | (3,676)
Impairment of long-lived assets | 950 | 3,729 | (2,779)
Loss (gain) on asset disposals, net | 1,226 | (354) | 1,580
Operating income (loss) | 20,737 | (6,336) | 27,073
Loss from continuing operations | (32,848) | (104,272) | 71,424

2025 vs 2024 Consolidated Results

Revenues increased by $6.6 million to $587.7 million in 2025 compared to $581.0 million 2024. The increase is driven by larger parts volume of $35.2 million and two natural gas conversion projects of $25.7 million offset partially by lower volume related to ESP projects of $20.0 million, construction projects of $18.7 million and package boilers of $10.7 million.

Costs of operations decreased by $10.5 million to $443.8 million in 2025 compared to $454.3 million in 2024. The decrease is primarily driven by a shift in business mix, as higher‑margin parts sales increased, revenue from larger projects declined and the remaining large projects required lower costs to complete.

SG&A expenses decreased by $5.1 million to $119.5 million in 2025 compared to $124.5 million in 2024. The decrease is primarily related to cost savings, partially offset by increased expenses in employee benefits in the current year.

Research and development costs decreased by $3.7 million to $1.5 million in 2025 compared to $5.1 million in 2024. The decrease is primarily driven by less development activity due to the increased commercialization of our BrightLoop ™ technology.

Impairment of long-lived assets decreased by $2.8 million to $1.0 million in 2025 compared to $3.7 million 2024. The decrease is driven by the construction in process facility that was impaired in 2024, partially offset by impairment recognized in the current year relating to a reduction in our real estate footprint.

Loss (gain) on asset disposals increased in 2025 compared to 2024 relating to the write-off of equipment in one of our manufacturing locations which was disposed of in 2025 compared to 2024 which had minor disposals.

Operating income increased by $27.1 million to $20.7 million in 2025 compared to an operating loss of $6.3 million in 2024, primarily due to the revenue as described above and an increase in gross profit due to the improvement in cost of operations in product mix.

Loss from continuing operations decreased by $71.4 million to $32.8 million in 2025 compared to $104.3 million in 2024, primarily due to the revenue as described above and an increase in gross profit due to the improvement in cost of operations in product mix, reduction in benefit plan expense for the year due to better asset performance in 2025 than anticipated and reduced interest expense due to the debt repayments and refinancing during the year.

Year ended December 31,
(in thousands) | 2024 | 2023 | $ Change
Revenues | 581,039 | 587,448 | (6,409)
Costs and expenses:
Cost of operations | 454,326 | 465,977 | (11,651)
Selling, general and administrative expenses | 124,541 | 134,940 | (10,399)
Research and development costs | 5,133 | 6,462 | (1,329)
Impairment of long-lived assets | 3,729 | — | 3,729
(Gain) loss on asset disposals, net | (354) | 134 | (488)
Operating loss | (6,336) | (20,065) | 13,729
Loss from continuing operations | (104,272) | (109,212) | 4,940

2024 vs 2023 Consolidated Results

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-16_item1_business.md)

ITEM 1. Business

We are a globally-focused energy technologies provider with nearly 160 years of experience providing diversified energy and emissions control solutions to a broad range of industrial, electrical utility, municipal and other customers. We support global energy needs and baseload power demand by providing advanced technologies that utilize coal, natural gas, hydrogen, waste and biomass to produce energy, environmental solutions and carbon capture systems. Our proven platforms help utilities, data centers, oil and gas, and other industries meet rising demand, while our comprehensive aftermarket services keep existing power plants operating efficiently. Our advanced environmental and decarbonization technologies help to reduce greenhouse gases and other emissions and capture carbon. We also are investing in new coal and natural gas technologies to produce steam or hydrogen from solid fuels and simultaneously isolate and capture CO 2 .

In the fourth quarter of 2025, we reassessed our segment structure as a result of the completion of our strategic shift to streamline and simplify our business. This transformation included the divestiture of certain non-core assets, as described in Note 4 to the Consolidated Financial Statements that accompany this report. As a result of this assessment, we have determined we have one reportable segment, labeled as B&W. The revised segment presentation has been applied retrospectively to all periods presented. For further information regarding our segment reporting, see Note 6 to the Consolidated Financial Statements that accompany this report.

Our vast installed base of steam generation equipment includes aftermarket parts, construction, maintenance and field services. We have an extensive global base of installed equipment for utilities and general industrial applications including refining, petrochemical, food processing, metals and others. We provide aftermarket parts, construction, maintenance, engineered upgrades and field services for our installed base as well as the installed base of other original equipment manufacturers. In addition to our aftermarket offerings, we also provide complete steam generation systems including package boilers, watertube and firetube waste heat boilers, and other boilers to medium and heavy industrial customers. Our unique range of offerings, coupled with the strength of our brand, provides a competitive advantage in existing and emerging markets, including utilities and power generation, AI data centers, and other industrial markets, including oil and gas. We also offer specialized technologies in industrial energy production, including hydrogen and syngas.

Our business depends significantly on the capital, operations and maintenance expenditures of global electric power generating companies, including renewable and thermal powered heat generation industries and industrial facilities with environmental compliance policy requirements. Several factors may influence these expenditures, including:

• climate change initiatives promoting environmental policies to meet legislative requirements and clean energy portfolio standards in North America, Europe, Middle East and Asia;

• regulations requiring environmental improvements in various industries and global markets;

• expectations regarding future governmental requirements to further limit or reduce greenhouse gas and other emissions in the United States, Europe and other international climate change sensitive countries;

• prices for electricity, along with the cost of production and distribution, including the cost of fuels, within the United States, Europe, Middle East and Asia;

• demand for electricity and other end products of steam-generating facilities;

• level of capacity utilization at operating power plants and other industrial users of steam production;

• maintenance and upkeep requirements at operating power plants, including to address the accumulated effects of usage;

• overall strength of the industrial industry;

• ability of electric power generating companies and other steam users to raise capital; and

• the impact of geopolitical conflicts, including the ongoing conflicts in Ukraine and the Middle East.

Customer demand is heavily affected by the variations in our customers' business cycles, power demand in their operating territories and by the overall economies and energy, environmental and noise abatement needs of the countries in which they operate.

Market Update

Management continues to adapt to macroeconomic conditions, including the impacts from inflation, higher interest rates and foreign exchange rate volatility, current and potential tariff actions and geopolitical conflicts. In certain instances, these situations have resulted in cost increases and delays or disruptions that have had, and could continue to have, an adverse impact on our ability to meet customers' demands. We continue to actively monitor the impact of these market conditions on current and future periods and actively manage costs and our liquidity position to provide additional flexibility while still supporting our customers and their specific needs. The duration and scope of these conditions cannot be predicted, and therefore, any anticipated negative financial impact on our operating results cannot be reasonably estimated.

Equity Capital Activities

For information regarding our equity activities, see Note 16 to the Consolidated Financial Statements included in Part II, Item 8 of this Annual Report.

Debt Capital Activities

For information regarding our debt activities, see Note 15 to the Consolidated Financial Statements included in Part II, Item 8 of this Annual Report.

Contracts

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-16_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-16_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-16_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-10_2-02-results.md, 10-K_2026-03-16_item7_mdna.md, 10-K_2026-03-16_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
