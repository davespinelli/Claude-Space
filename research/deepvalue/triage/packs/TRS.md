# Triage pack — TRS · TRIMAS CORP

_Generated 2026-09-04 14:13 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TRS · **Name:** TRIMAS CORP
- **CIK:** 0000842633
- **SIC:** 3460 — Metal Forgings & Stampings
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TRS

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** TRIMAS CORP
- **CIK:** 842,633 · **SIC:** 3460 (Metal Forgings & Stampings) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtAndCapitalLeaseObligations

**Valuation**

| metric | value |
|---|---|
| price | 38.85 |
| mktcap | $1.4B |
| ev | $548.1M |
| ev_ebit | 13.3x |
| fcf | $69.1M |
| fcf_yield | 5.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.5% |
| net_debt | -$845.6M |
| net_debt_ebit | -20.5x |
| cash | $1.2B |
| ltd | $396.9M |
| equity | $1.4B |
| ltd_tag | LongTermDebtAndCapitalLeaseObligations |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $645.7M |
| revenue_prior | $630.8M |
| rev_growth | 2.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $41.3M |
| net_income | $120.1M |
| cfo | $117.5M |
| capex | $48.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -11.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 35,873,873 |
| shares_py | 40,641,562 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 6.4% |
| r6m | 0.6% |
| off_52w_high | -13.6% |
| adv20 | $15.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.49 |
| r_ev_ebit | 0.64 |
| r_roic | 0.53 |
| r_rev_growth | 0.42 |
| r_buyback | 0.95 |
| score | 0.66 |

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
| rank | 90 |

**Screen rationale:** buying back stock -11.7%; net cash; 12-1 momentum 6.4%


## 3. Share count trend

- Shares outstanding: **35,873,873** (CY2026Q2I) vs **40,641,562** prior year (CY2025Q2I)
- Change: **-11.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-03-12** — Item 5.02 (officer / director change or comp arrangement): On March 9, 2026, TriMas Corporation (the "Company") announced that Jill S. Stress would be departing from the Company effective March 27, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 126 sh / $5,046 vs sells 20,000 sh / $881,960 -> net $-876,914 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: Tredwell Daniel P bought 64 sh @ $39.63 ($2,524) on 2026-08-12.

Form 4 filings parsed: 12; transaction rows: 14 (open-market buys 2, sales 3).

| code | rows |
|---|---|
| A | 5 |
| F | 4 |
| P | 2 |
| S | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'TRIMAS REPORTS SECOND QUARTER 2026 RESULTS'; skipped 8 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (trs_06302026xexhibit991.htm)

TRIMAS REPORTS SECOND QUARTER 2026 RESULTS

Raises Low End and Midpoint of Full Year 2026 EPS Outlook

• Second quarter operating profit increased to $10.9 million, while adjusted operating profit increased 29.1% to $14.9 million

• Second quarter diluted EPS increased to $1.86, with adjusted diluted EPS of $0.52

• Repurchased more than 5 million shares of common stock since November 2025

• Ended the quarter with $1.24 billion of cash and cash equivalents

BLOOMFIELD HILLS, Michigan, July 30, 2026 - TriMas (NASDAQ: TRS) today announced financial results for the second quarter ended June 30, 2026.

TriMas reported second quarter 2026 net sales of $174.6 million, a 1.6% increase compared to $171.8 million in second quarter 2025, driven by organic growth within Specialty Products and the benefit of favorable foreign currency exchange. Operating profit increased to $10.9 million in second quarter 2026, compared to $7.4 million in second quarter 2025. Adjusting for Special Items (1) , second quarter 2026 adjusted operating profit was $14.9 million, a 29.1% increase compared to $11.5 million in the prior year period, reflecting the successful execution of cost-reduction and streamlining initiatives.

The Company reported second quarter 2026 income from continuing operations of $67.3 million, or $1.86 per diluted share, compared with $2.4 million, or $0.06 per diluted share, in second quarter 2025. Adjusting for Special Items (1) , second quarter 2026 adjusted income (2) from continuing operations was $19.0 million, more than double the prior year period of $8.1 million. Second quarter 2026 adjusted diluted earnings per share (2) from continuing operations was $0.52, an increase of 160.0% compared to $0.20 in second quarter 2025, primarily reflecting interest income earned on the Company's cash and cash equivalents, cost reductions, improved operating performance and the benefit of a lower share count resulting from the Company's share repurchase activity.

"Our second quarter results reflect continued progress against the priorities we established at the beginning of 2026," said Thomas Snyder, TriMas President and Chief Executive Officer. "We delivered improved profitability and operating margin despite a dynamic market environment, driven by the successful execution of our cost-reduction actions and certain operational improvement initiatives. During the quarter, we also strengthened our leadership team, and enhanced organizational alignment and accountability through our strategic planning process, while advancing customer engagement and operational excellence initiatives."

"As we move through the second half of the year, we expect the run-rate benefits of our cost reduction and operational excellence initiatives to continue building, supporting further performance improvement. At the same time, we remain focused on disciplined capital deployment, having repurchased more than five million shares since announcing the Aerospace divestiture, while preserving the flexibility to invest in organic growth initiatives and strategically aligned, high-quality acquisition opportunities that elevate our Packaging and Life Sciences platforms. We believe the actions we have taken to simplify and strengthen TriMas have positioned us well to continue delivering improved results and long-term shareholder value."

Financial Position

During the second quarter of 2026, the Company returned capital to shareholders through the repurchase of 509,264 shares of its outstanding common stock for $18.9 million. Year to date through June 30, 2026, the Company repurchased 1,996,321 shares for $73.5 million, contributing to a 4.7% net reduction in outstanding shares compared to December 31, 2025. Since announcing the decision to divest TriMas Aerospace in November 2025, the Company has repurchased more than five million shares. As of June 30, 2026, approximately 35.9 million shares were outstanding and $76.5 million remained available under the Company's share repurchase authorization. TriMas also declared and paid a quarterly cash dividend of $0.04 per share.

The Company reported net cash used in operating activities of continuing operations of $38.5 million for second quarter 2026, compared to net cash provided by operating activities of $16.5 million in second quarter 2025. As a result, the Company reported a Free Cash Flow (3) use of $12.9 million for second quarter 2026, compared to Free Cash Flow (3) of $7.7 million in second quarter 2025, primarily due to the timing of sales and collections in the quarter. Please see Appendix I for further details.

TriMas ended second quarter 2026 with $1,242.5 million of cash on hand, $1,446.1 million of cash and available borrowing capacity under its revolving credit facility, and a net leverage ratio of 1.8x as defined in the Company's credit agreement. As of June 30, 2026, the Company reported total debt of $396.9 million and Net Debt (4) of $(845.6) million, reflecting cash on hand that significantly exceeded the Company's debt position following the divestiture of TriMas Aerospace, which generated approximately $1.2 billion in net after‑tax proceeds. The remaining proceeds are currently invested in interest‑bearing investments pending further redeployment.

Second Quarter Segment Results

The TriMas Packaging group reported second quarter net sales of $142.9 million, essentially flat compared to the second quarter of 2025. Sales growth in the industrial and life sciences end markets, along with the benefit of favorable foreign currency translation, was largely offset by lower sales in beauty and personal care applications, and food and beverage products. While second quarter operating profit declined, adjusted operating profit and margin both improved year-over-year and sequentially from the first quarter of 2026, reflecting the benefits of cost‑reduction actions, operational improvement initiatives and a more favorable product sales mix.

TriMas' Specialty Products group reported second quarter net sales of $31.7 million, an increase of 10.2% compared to second quarter 2025. Second quarter operating profit and margin declined year-over-year, as the benefits of higher sales volumes were more than offset by a lag in recovering increased raw material costs and temporary manufacturing inefficiencies related to machine downtime and labor ramp-up.

Discontinued Operations

The divestiture of TriMas Aerospace was completed on March 16, 2026, for approximately $1.5 billion in cash, generating net after-tax proceeds of approximately $1.2 billion. To date, proceeds have been used to repay borrowings under the Company's revolving credit facility, fund additional share repurchases and satisfy a portion of transaction-related tax obligations, while the remaining balance has been invested in liquid, interest-bearing accounts. The Company intends to deploy the remaining proceeds in support of capital allocation priorities, which may include organic growth investments, strategic acquisitions and additional share repurchases.

The results of TriMas Aerospace, along with transaction-related costs, have been classified as discontinued operations for all periods presented.

Realignment and Cost-Out Initiatives

TriMas has completed the closure and consolidation of its Atkins, Arkansas, packaging facility. The Company remains on track to deliver approximately $10.5 million of savings in 2026 and $16.0 million of annualized savings related to the previously communicated cost-out actions.

2026 Outlook

The Company has raised the low end and midpoint of its previously issued full-year 2026 adjusted diluted earnings per share (2) (EPS) outlook and now expects adjusted diluted EPS in the range o f $1.60 to $1.70, compared to the prior outlook of $1.50 to $1.70, provided on February 26, 2026. This outlook assumes between $9 million and $10 million of interest income per each remaining quarter of 2026, and assumes no significant change in interest rates or the redeployment of the cash proceeds for the remainder of the year. The Company continues to expect sales growth of 3% to 6% year-over-year across its combined Packaging and Specialty Products businesses, along with more than 300 basis points of adjusted operating profit margin improvement, driven by cost reductions and organizational realignment initiatives.

The above outlook includes the impact of all announced acquisitions and divestitures as of July 30, 2026. The outlook provided assumes no significant impact related to input costs or end market demand associated with global conflicts or geopolitical actions. All of the above amounts considered as 2026 guidance are after adjusting for any current or future amounts that may be considered Special Items. The inability to predict the amount and timing of the impacts of these Special Items makes a detailed reconciliation of these forward-looking non-GAAP financial measures impracticable. (1)

Conference Call Information

TriMas will host its second quarter 2026 earnings conference call today, Thursday, July 30, 2026, at 10 a.m. ET. To participate via phone, please dial (877) 407-0890 (U.S. and Canada) or +1 (201) 389-0918 (outside the U.S. and Canada), and ask to be connected to the TriMas second quarter 2026 earnings conference call. The conference call will also be simultaneously webcast via the TriMas website at www.trimas.com , under the "Investors" section, with an accompanying slide presentation. A replay of the conference call will be available on the TriMas website or by dialing (877) 660-6853 (U.S. and Canada) or +1 (201) 612-7415 (outside the U.S. and Canada) with a meeting ID of 13761489, beginning July 30, 2026, at 3:00 p.m. ET through August 13, 2026, at 3:00 p.m. ET.

(3) The Company defines Free Cash Flow as Net Cash Provided by/Used for Operating Activities, excluding the cash impact of Special Items, less Capital Expenditures. Please see Appendix I for additional details.

(4) The Company defines Net Debt as Total Debt less Cash and Cash Equivalents. Please see Appendix I for additional details.

About TriMas

TriMas designs, manufactures and supplies a broad range of innovative and high‑quality products for the consumer packaging, life sciences and industrial markets through its TriMas Packaging and Specialty Products groups. With approximately 2,500 employees in 12 countries, TriMas is committed to empowering customer success through deep partnerships, strong technical expertise, focused innovation, and exceptional quality and service. Guided by a culture of continuous improvement and operational excellence, TriMas invests in its people and capabilities to deliver long‑term value for all stakeholders. Headquartered in Bloomfield Hills, Michigan, TriMas is publicly traded on NASDAQ under the ticker symbol "TRS." For more information, please visit www.trimas.com .

Contact

Sherry Lauderback

VP, Investor Relations, Communications & Sustainability

(248) 631-5506

sherry.lauderback@trimas.com

TriMas Corporation

Condensed Consolidated Balance Sheet

(Dollars in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-02_item7_mdna.md)

_Extraction: started at the Overview heading._

Introduction

TriMas designs, develops and manufactures a diverse set of products primarily for the consumer products and industrial markets through its TriMas Packaging and Specialty Products groups. Our wide range of innovative products are designed and engineered to solve application-specific challenges that our customers face. We believe our businesses share important and distinguishing characteristic s, including: innovative product technologies and features; a high-degree of customer approved processes and qualifications; established distribution networks; modest capital investment requirements; strong cash flow conversion and long-term growth opportunities. While the majority of our revenue is in the United States, we manufacture and supply products globally to a wide range of companies. We are principally engaged in two reportable segments: Packaging and Specialty Products.

On November 4, 2025, we entered into an Equity Purchase Agreement (the "Purchase Agreement") with Takeoff Buyer, Inc. (the "Purchaser"), an affiliate of Tinicum L.P. and funds managed by Blackstone, Inc., to sell TriMas Aerospace. The purchase price for the sale of TriMas Aerospace consists of approximately $1.45 billion in cash, subject to customary adjustments. The sale of TriMas Aerospace is expected to close in the first quarter of 2026, subject to the satisfaction or waiver of customary and other closing conditions. The financial results of our Aerospace business were previously reported within our Aerospace reportable segment, and are presented as assets held for sale in our consolidated balance sheet and as discontinued operations in our consolidated statement of income for all periods presented in the financial statements.

Key Factors Affecting Our Reported Results

Demand for the products our businesses produce and results of operations depend upon general economic conditions. We serve customers in industries that are highly competitive and that may be significantly impacted by changes in economic or geopolitical conditions.

Our results of operations have been materially impacted over the past few years by macro-economic factors, most recently by cost inflation (raw materials, wage rates and freight) and a lack of material, and in certain regions, skilled labor availability. Additionally, during 2025, the U.S. government altered its approach to international trade policy and announced baseline tariffs on products from all countries and additional individualized reciprocal tariffs on the countries with which the United States has the largest trade deficits, including China. This change in international trade policy has also created uncertainty with respect to future tariffs, including any retaliatory tariffs imposed by other countries, or other potential governmental actions. These factors have affected each of our businesses and how we operate, albeit in different ways and magnitudes. The current tariffs, predominately those imposed on China-based imports, have increased the costs of certain products sourced from non-U.S. countries.

Sales of certain of our products for industrial applications, for example steel cylinders for packaged gas applications, have experienced volatility in demand related to customers securing high order rates in prior periods, only to enter a period of destocking in more recent periods. This significant level of volatility in demand levels, input and transportation costs, and material and labor availability, have pressured our ability to operate efficiently in recent periods. While some areas of demand volatility and softness remain, such as in our our Norris Cylinder business within our Specialty Products segment, we have experienced more steady and consistent demand in our Packaging segment.

Overall, 2025 net sales increased $14.9 million, or 2.4%, compared to 2024. We experienced organic growth of 4.1% within our Packaging segment compared to 2024. The increase was partially offset by lower sales of 7.0% in our Specialty Products segment as compared to the prior year, as higher sales of steel cylinders more than offset the lost sales due to the divestiture of our Arrow Engine business in January 2025. Our overall sales increase included $2.2 million of currency exchange, as our reported results in U.S. dollars were favorably impacted as a result of a weakening U.S. dollar relative to foreign currencies.

The most significant drivers affecting our financial results in 2025 compared with 2024, other than as directly impacted by sales changes, were the impact of the divestiture of our Arrow Engine business, our recognition of a net benefit to recognize our asbestos insurance recovery asset and update our liability to our recent actuarial valuation, realignment costs related to actions to reorganize our corporate office, charges associated with environmental remediation liabilities, the refinancing of our existing Credit Agreement ("Credit Agreement"), the year-over-year impact of accelerated depreciation charges in 2024 related to shortening the useful lives of certain machinery and equipment in our Specialty Products segment, and a decrease in our effective tax rate.

On January 31, 2025, we completed the sale of our Arrow Engine business within the Specialty Products segment for net cash proceeds of $21.0 million. As a result, we recorded a pre-tax gain of $5.4 million for the year ended December 31, 2025.

In third quarter 2025, we commissioned our actuary to update our asbestos study, and upon completion we recorded a pre-tax charge of $8.0 million. In the fourth quarter 2025, we reassessed the facts and circumstances surrounding the CIP agreement with the consortium of insurance companies and deemed the realization of the claim for loss recovery probable. We estimated the loss recovery of indemnity and defense costs under the CIP agreement, and recognized an insurance recovery asset of $35.8 million, which was commensurate with the assumptions used to calculate the asbestos liability. See Note 16, " Commitments and Contingencies ," to our consolidated financial statements attached herein with this Form 10-K.

During 2025, we recorded $5.2 million of realignment costs related to actions to reorganize our corporate office, primarily for severance and consulting costs, including $1.5 million of non-cash compensation expense.

During 2025 we recorded pre-tax charges of $6.5 million for environmental remediation for waste sites in which we had been named a potential responsible party. In 2024, we recorded pre-tax charges of $3.2 million for similar environmental matters.

In March 2025, we amended our Credit Agreement to extend the maturity date through March 31, 2030. We incurred fees and expenses of $1.3 million related to the amendment, all of which was capitalized as debt issuance costs.

In 2024, following a strategic demand and profitability study of our cylinders products within our Specialty Products segment, we ceased use of our second hot forge, which primarily produced lower profitability products, resulting in pre-tax non-cash charges related to accelerated depreciation expense of $8.2 million due to the shortening of the assets expected useful lives.

Our effective tax rate for 2025 and 2024 was (198.1)%, and 53.3%, respectively. The decrease in effective tax rate for 2025 as compared to 2024 is primarily as a result of us recognizing a $53.9 million tax benefit in 2025 related to the tax-basis versus book-basis difference in our Aerospace business. Otherwise, the remaining difference is due to a change in the mix of domestic and foreign pre-tax results.

Additional Key Risks that May Affect Our Reported Results

We have executed meaningful realignment actions over the past few years to address variable and structural costs where demand has fallen. We will continue to assess and take further actions if required. However, as a result of the current period of macroeconomic inflation and uncertainty, including uncertainty regarding the scope and duration of current and future tariffs and trade actions, and the potential impact of such factors to our future results of operations, as well as if there is an impact to TriMas' overall performance and market capitalization, we may record additional cash and non-cash charges related to further realignment actions, asset impairments, including impairments to our goodwill, intangible assets, fixed assets, inventory or customer receivable account balances.

Despite the potential for declines in future demand levels and results of operations, at present, we believe our capital structure is in a strong position. We have sufficient cash and available liquidity under our revolving credit facility to meet our debt service obligations, capital expenditure requirements and other short-term and long-term obligations for the foreseeable future.

Critical factors affecting our ability to succeed include: our ability to generate organic growth through product development, cross-selling and extending product-line offerings, and our ability to quickly and cost-effectively introduce and successfully launch new products; our ability to acquire and integrate companies or products that supplement existing product lines, add adjacent distribution channels and new customers, or expand our geographic coverage; our ability to manage our cost structure more efficiently via supply chain management, internal sourcing and/or purchasing of materials, selective outsourcing and/or purchasing of support functions, working capital management, and greater leverage of our administrative functions; and our ability to absorb, or recover via commercial actions, inflationary or other cost increases, including tariffs and duties.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-02_item1_business.md)

Item 1. Business

Overview

TriMas designs, develops and manufactures a diverse portfolio of products primarily for the consumer products, aerospace and defense, and industrial markets through its TriMas Packaging, TriMas Aerospace and Specialty Products groups. We believe our businesses share important attributes, including: innovative produc t technologies and features; customer-approved processes and qualified products; demonstrated operating discipline; strong cash generation; long-term growth opportunities; and a commitment to sustainability. Headquartered in Bloomfield Hills, Michigan, TriMas, including our Aerospace operations, has approximately 3,700 employees who serve our customers from 37 manufacturing and support locations in 13 countries.

On November 4, 2025, we entered into an Equity Purchase Agreement (the "Purchase Agreement") with Takeoff Buyer, Inc. (the "Purchaser"), an affiliate of Tinicum L.P. and funds managed by Blackstone, Inc., to sell TriMas Aerospace. The purchase price for the sale of TriMas Aerospace consists of approximately $1.45 billion in cash, subject to customary adjustments. The sale of TriMas Aerospace is expected to close in the first quarter of 2026, subject to the satisfaction or waiver of customary and other closing conditions. As a result, the financial results of our Aerospace segment are presented as a discontinued operation and the assets and liabilities have been retrospectively reclassified to assets and liabilities held for sale for all periods presented in the financial statements included in this Annual Report of Form 10-K

During 2025, our net sales from continuing operations were $645.7 million, operating profit from continuing operations was $41.3 million, and net cash provided by operating activities was $117.5 million. Approximately 66% of our 2025 net sales from continuing operations were generated from sales in North America.

Our Competitive Strengths

Our management team believes TriMas benefits from a number of competitive strengths, including:

• Innovative Manufacturing and Product Technologies. We believe our businesses are well-positioned through years of refined manufacturing know-how, innovative product development, application engineering and solutions design. We continue to prioritize investments that enhance and protect our product designs and manufacturing competencies. Our proprietary manufacturing processes, advanced automation and specialized technical capabilities are often difficult and costly to replicate, providing a competitive advantage. TriMas Packaging delivers a consistent pipeline of new and enhanced solutions that improve functionality, aesthetics and sustainability. Our recent product innovations include fully recyclable Singolo™ polymeric pumps made from a single material; an expanded line of all‑plastic foamers and small‑dosage treatment pumps; and tethered caps designed to improve recyclability. Additional offerings include certified flame‑mitigation closures and patent‑pending child‑resistant closures engineered with less plastic to reduce environmental impact without compromising performance. We also continue to support customers in medical and wellness markets with high‑precision, technically advanced components used in testing, diagnostics and treatment applications. TriMas Packaging's emphasis on engineering excellence and intellectual property protection has resulted in a growing global patent portfolio, with 27 patents filed and 18 issued in 2025.

• Long-Term Customer Relationships and Customer-Focused Solutions. We believe that TriMas has long‑standing relationships with many of the world's leading consumer, industrial and life sciences companies, supported by product lines and businesses that customers have relied on for decades. Rieke ® , part of our Packaging group, for example, has operated for more than a century, while Norris Cylinder™, with over 70 years of experience, is a large manufacturer of high‑ and low‑pressure cylinders. Across key product categories, we serve as an integral supplier, providing the technical expertise, reliability and innovation our customers depend on for product launches and ongoing programs. We collaborate closely with customers throughout the design, development and production life cycle to deliver solutions that meet evolving technical, marketing and sustainability requirements. A significant portion of our offerings are customized, including specialty caps, closures and dispensing solutions featuring tailored colors, collar sizes, venting, lining and precision‑metering options. Investments in high‑quality multi‑color printing, advanced application engineering and flexible manufacturing cells further enable us to support short lead times for high‑volume products as well as customized solutions for moderate‑volume orders.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-07-30_2-02-results.md, 10-K_2026-03-02_item7_mdna.md, 10-K_2026-03-02_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
