# Triage pack — MVST · Microvast Holdings, Inc.

_Generated 2026-09-04 23:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MVST · **Name:** Microvast Holdings, Inc.
- **CIK:** 0001760689
- **SIC:** 3690 — Miscellaneous Electrical Machinery, Equipment & Supplies
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MVST

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Microvast Holdings, Inc.
- **CIK:** 1,760,689 · **SIC:** 3690 (Miscellaneous Electrical Machinery, Equipment & Supplies) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:DebtLongtermAndShorttermCombinedAmount

**Valuation**

| metric | value |
|---|---|
| price | 0.70 |
| mktcap | $269.2M |
| ev | $260.0M |
| ev_ebit | 37.2x |
| fcf | $56.1M |
| fcf_yield | 20.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 1.0% |
| net_debt | -$9.2M |
| net_debt_ebit | -1.3x |
| cash | $127.8M |
| ltd | $118.6M |
| equity | $543.1M |
| ltd_tag | DebtLongtermAndShorttermCombinedAmount |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $427.5M |
| revenue_prior | $379.8M |
| rev_growth | 12.6% |
| rev_growth_note | share count +18.2% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $7.0M |
| net_income | -$29.2M |
| cfo | $75.9M |
| capex | $19.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 18.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 384,534,486 |
| shares_py | 325,354,111 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -67.3% |
| r6m | -67.0% |
| off_52w_high | -89.1% |
| adv20 | $6.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.88 |
| r_ev_ebit | 0.21 |
| r_roic | 0.34 |
| r_rev_growth | 0.71 |
| r_buyback | 0.08 |
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
| rank | 370 |

**Screen rationale:** top-quartile FCF yield 20.8%; share count +18.2% yoy — growth may be acquisition/issuance-driven, not organic; net cash; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **384,534,486** (CY2026Q2I) vs **325,354,111** prior year (CY2025Q2I)
- Change: **18.2%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +18.2% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-07** — Item 5.02 (Departure): of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 105,767 sh / $134,360 -> net $-134,360 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 21 (open-market buys 0, sales 4).

| code | rows |
|---|---|
| A | 14 |
| C | 3 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-11_2-02-results.md)

_Extraction: started at the first release heading, 'Microvast Reports Second Quarter 2026 Financial Results'; skipped 15 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (mvst2026q2ex991earningspre.htm)

Microvast Reports Second Quarter 2026 Financial Results

Houston, Texas, USA — Microvast Holdings, Inc. (NASDAQ:MVST) ("Microvast" or the "Company"), a global leader in advanced battery technologies, announced today its unaudited consolidated financial results for the second quarter ended June 30, 2026 ("Q2 2026").

"In the second quarter, Microvast progressed through a pivotal phase of our global capacity expansion. Delivering $87.3 million in revenue and maintaining a 29.5% gross margin highlights our ability to navigate raw material fluctuations and production utilization cycles. While it impacted our net revenue, returning $2.7 million in IEEPA (1) tariff refunds to our U.S. customers reinforces the strength of our long-term commercial partnerships. With Huzhou Phase 3.2 expected to be on track to deliver up to 2 GWh of next-generation modular capacity and Clarksville pack line localization anticipated to commence operations by year end, we are working to position our business to meet capacity demand across high-barrier commercial and transit markets," said Yang Wu, Microvast's Founder, Chairman, and Chief Executive Officer.

Q2 2026 Results

• Revenues of $87.3 million, compared to $91.3 million in Q2 2025, decreasing by $4.1 million, or 4.5%. This decrease was primarily driven by $2.7 million in IEEPA (1) tariff refunds issued to a U.S. customer, recorded as a reduction to revenue in the current period.

• Gross margin decreased to 29.5% from 34.7% in Q2 2025. Non-GAAP adjusted gross margin* decreased to 29.6% from 34.8% in Q2 2025, primarily due to higher raw material prices, and lower production utilization, which reduced fixed cost absorption, slightly offset by recognition of the IEEPA (1) tariff refunds received.

• Operating expenses increased to $27.5 million, compared to $23.7 million in Q2 2025. Non-GAAP adjusted operating expenses* were $26.7 million, compared to $22.9 million in Q2 2025.

• Net loss of $12.0 million, compared to net loss of $106.1 million in Q2 2025, primarily due to a reduction in negative impacts from changes in fair value of warrant liability and convertible loan. Non-GAAP adjusted net loss* was $5.3 million, compared to non-GAAP adjusted net profit* of $16.3 million in Q2 2025.

• Net loss per share of $0.03, compared to net loss per share of $0.33 in Q2 2025. Non-GAAP adjusted net loss per share* was $0.01, compared to non-GAAP adjusted net profit per share* of $0.05 in Q2 2025.

• Non-GAAP adjusted EBITDA* of $3.6 million in Q2 2026, compared to non-GAAP adjusted EBITDA* of $25.9 million in Q2 2025.

• Capital expenditures of $11.3 million, compared to $7.4 million in Q2 2025.

• Cash, cash equivalents and restricted cash of $143.1 million as of June 30, 2026, compared to $169.2 million as of December 31, 2025, and $138.8 million as of June 30, 2025.

Six Months Ended June 30, 2026 Results ("YTD 2026")

• Revenues of $147.9 million compared to $207.8 million in the six months ended June 30, 2025 ("YTD 2025"), a decrease of 28.8%. This decrease was primarily a result of evolving regulatory and geopolitical dynamics, including in the Indian and Korean markets, demand shift towards lower-cost products in India, OEM platform ramp-up delays, and a $2.7 million IEEPA (1) tariff refund issued to a customer recorded as a reduction to our revenue in the current period.

• Gross margin decreased to 30.4% from 36.0% in YTD 2025. Non-GAAP adjusted gross margin* decreased to 30.4% from 36.0% in YTD 2025, primarily due to higher raw material prices, lower production utilization, which reduced fixed cost absorption, slightly offset by recognition of the IEEPA (1) tariff refunds received.

• Operating expenses increased to $54.6 million, compared to $52.9 million in YTD 2025. Non-GAAP adjusted operating expenses* were $52.8 million, compared to $51.4 million in YTD 2025.

• Net profit of $36.2 million, compared to net loss of $44.3 million in YTD 2025, primarily due to a reduction in negative impacts from changes in fair value of warrant liability and convertible loan. Non-GAAP adjusted net loss* was $19.9 million, compared to non-GAAP adjusted net profit of $35.6 million in YTD 2025.

• Net profit per share of $0.11, compared to net loss per share of $0.14 in YTD 2025. Non-GAAP adjusted net loss per share* was $0.06, compared to non-GAAP adjusted net profit per share* of $0.11 in YTD 2025.

• Non-GAAP adjusted EBITDA* of negative $1.9 million in YTD 2026, compared to non-GAAP adjusted EBITDA* of $54.4 million in YTD 2025.

• Capital expenditures of $15.5 million, compared to $14.0 million in YTD 2025.

*The Company presents its financial results in accordance with generally accepted accounting principles in the United States of America ("GAAP"). However, management believes that using additional non-GAAP measures will enhance the evaluation of the profitability of the Company and its ongoing operations. Please see the tables on pages 12-15 below for reconciliations of GAAP to non-GAAP financial measures. The Consolidated Balance Sheets, Consolidated Statements of Operations, and Consolidated Statements of Cash Flows are derived from the consolidated financial statements presented in our Quarterly Report on Form 10-Q as of and for the three- and six-month periods ended June 30, 2026.

(1) In February 2026, the United States Supreme Court ruled that certain tariffs imposed under the International Emergency Economic Powers Act ("IEEPA") were not authorized by statute. Following the ruling, the U.S. Court of International Trade ordered U.S. Customs and Border Protection to suspend collection of such tariffs and to establish a process to refund amounts previously collected. As a result of this ruling, the Company is eligible to receive refunds of tariffs previously paid on qualifying imports. In May 2026, the Company received $4.3 million in tariff refunds, excluding interest. Of this amount, $2.7 million was issued in tariff refunds to a customer. The IEEPA tariff refunds received were recognized as a reduction to the cost of revenue, while the refund issued to our customer was recognized as a reduction of revenue for the three and six months ended June 30, 2026.

2026 Outlook & Forward-Looking Information

• We continue to target a stable gross margin profile through sustained operational discipline and premium product positioning. This approach seeks to balance external pressures including inflationary raw material pricing, duties and tariffs, and elevated logistics and freight expenses against the planned absorption of ramp-up expenses tied to our Phase 3.2 expansion.

• Huzhou Phase 3.2 production capacity ramp up remains our primary operational milestone in 2026. The expansion is anticipated to bring online up to 2 GWh of modular capacity to support next-generation cell demand.

• Localized pack assembly at our Clarksville facility remains on schedule, with initial operations anticipated by year-end. This footprint advances our domestic strategy to supply North American commercial vehicle and transit partners with locally integrated battery systems.

• We continue to seek new commercial momentum across EMEA, North America, and APAC. Our long-term focus remains centered on heavy industrial and transit markets, where our vertical integration and newly launched KAF electric powertrain position us to deliver a durable competitive advantage, subject to final product validation, vehicle-level integration with OEM partners, customer qualification, and availability of domestic manufacturing capacity and capital.

Webcast Information

Company management will host a conference call and webcast on August 10, 2026, at 4:00 p.m. Central Time, to discuss the Company's financial results. The live webcast and accompanying slide presentation will be accessible from the Events & Presentations section of Microvast's investor relations website (https://ir.microvast.com/events-presentations/events). A replay will be available following the conclusion of the event.

About Microvast

Microvast strives to be a global leader in advanced battery technologies, with a portfolio of more than 890 patents. Founded in Texas in 2006 and headquartered in Houston, the company has spent two decades engineering cutting-edge battery systems that are intended to power a cleaner future. Microvast stands as a trusted global partner with the mission to provide the high-performance solutions required for today's electrification needs.

For more information, please visit www.microvast.com or follow us on LinkedIn (@microvast).

Contact:

Investor Relations

ir@microvast.com

We believe that both management and investors benefit from referring to these non-GAAP financial measures in assessing our performance and when planning, forecasting, and analyzing future periods. These non-GAAP financial measures also facilitate management's internal comparisons to our historical performance. We believe these non-GAAP financial measures are useful to investors both because (1) they allow for greater transparency with respect to key metrics used by management in its financial and operational decision-making and (2) they are used by our institutional investors and the analyst community to help them analyze the health of our business. Accordingly, we believe that these non-GAAP financial measures provide useful information to investors and others in understanding and evaluating our operating results in the same manner as our management team and board of directors.

Non-GAAP financial measures have limitations as an analytical tool, and you should not consider them in isolation, or as a substitute for, financial information prepared in accordance with GAAP. For example, our calculation of non-GAAP adjusted EBITDA may differ from similarly titled non-GAAP measures, if any, reported by our peer companies, or our peer companies may use other measures to calculate their financial performance, and therefore our use of non-GAAP adjusted EBITDA may not be directly comparable to similarly titled measures of other companies. The principal limitation of non-GAAP adjusted EBITDA is that it excludes significant expenses and income that are required by GAAP to be recorded in our financial statements. In addition, it is subject to inherent limitations as it reflects the exercise of judgments by management about which expense and income are excluded or

included in determining this non-GAAP financial measure. In order to compensate for these limitations, management presents non-GAAP financial measures in connection with GAAP results. In addition, such financial information is unaudited and does not conform to SEC Regulation S-X and as a result, such information may be presented differently in our future filings with the SEC. For example, with respect to the warrant liability resulting from the July 23, 2021 business combination with Tuscan Holdings Corp., we now exclude changes in fair value from net profit/(loss) in our non-GAAP adjusted EBITDA and non-GAAP adjusted net profit/(loss) calculation, which had not been done in prior periods.

MICROVAST HOLDINGS, INC.

CONSOLIDATED BALANCE SHEETS

(In thousands, except per share data, unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-16_item7_mdna.md)

_Extraction: started at the Overview heading._

Overview

Since inception, we have financed our operations primarily through capital contributions from equity holders, the issuance of convertible notes, and bank borrowings. As of December 31, 2025, our principal sources of liquidity included cash, cash equivalents, and restricted cash totaling $169.2 million, of which $105.0 million was comprised in cash and cash equivalents.

Of the cash and cash equivalents as of December 31, 2025, $40.3 million is held by our China subsidiary and $21.9 million is held by our European subsidiaries. These funds are generally intended to support local operations. If we were to repatriate these funds to the U.S., we may be required to accrue and pay applicable withholding taxes. We currently intend to retain available funds and future earnings to support ongoing operations and expansion efforts in China, Europe, and the U.S.

Going Concern Evaluation

In accordance with ASU No. 2014-15, management evaluated whether conditions and events, considered in the aggregate, raise substantial doubt about our ability to continue as a going concern within one year after the date these consolidated financial statements are issued. Based on our current business plan, we projected that existing cash and assets held for sale would not be sufficient to fund operations through the next twelve months. These conditions initially raised substantial doubt about our ability to continue as a going concern.

Management has implemented several primary plans intended to alleviate these conditions:

• Operating Cash Flows : For the year ended December 31, 2025, we generated $75.9 million in net cash from operating activities. Our order backlog stood at $196.1 million, the majority of which is expected to be fulfilled in 2026 and 2027. While we anticipate some absorption pressure during the ramp up of our Huzhou 3.2 manufacturing line expansion, we expect gross margins to remain relatively stable.

• Refinancing of Short-term Borrowings : Based on our historical ability to access credit, we expect to maintain the ability to refinance these obligations as needed as they become due over the next twelve months.

• Equity Funding : Under our Controlled Equity Offering Sales Agreement (the "Sales Agreement"), the Company has received $27.9 million in net proceeds through the date of this issuance. We intend to continue utilizing the Sales Agreement to raise additional capital as needed for general corporate purposes and debt repayment.

Based on the execution of these plans, management has concluded it is probable that these actions will alleviate substantial doubt about the Company's ability to continue as a going concern and provide adequate liquidity to meet our requirements for the next twelve months. However, there is no assurance that the Company will be able to alleviate these concerns.

Additional Liquidity Initiatives

We secured $85.7 million in bank loans during the year ended December 31, 2025 (see Note 12 – Bank Borrowings). The Company has been exploring a potential sale of its Lake Mary, Florida facility with a prospective buyer

for a gross purchase price of $11,500. This divestiture is intended to provide additional liquidity without impacting core operations. The transaction is subject to customary closing conditions and a due diligence period for the buyer. The Company currently anticipates that, if completed, the transaction would close during the second quarter of 2026.

Financings

As of December 31, 2025, our debt obligations consisted of:

• Bank borrowings of $106.3 million, the terms of which range from 1 to 18 months. The interest rates of our bank borrowings ranged from 2.60% to 4.85% per annum.

• Convertible bonds of $41.7 million, with interest rates ranging from 3% to 4%. The convertible bonds are due in 2027.

• Convertible loan measured at fair value of $140.9 million. This loan bears interest at Term SOFR plus an applicable margin of 9.75%. Of this, 3.75% is paid in kind and added to the outstanding principal balance, and the remainder is paid in cash. See Note 25 – Convertible loan measured at fair value for details.

As of December 31, 2025, we were in compliance with all material terms and covenants of our loan agreements, credit agreements, and bonds.

On July 23, 2021, we received $705.1 million in net proceeds from our Business Combination. We have used $514.2 million of the net proceeds to expand our manufacturing facilities and for the purchase of property and equipment associated with our existing manufacturing and R&D facilities. In addition, $190.9 million of the net proceeds were used for general working capital.

Although no additional binding financing agreements have been entered into, the Company remains engaged in discussions with third parties to explore further capital-raising opportunities. Future capital requirements may change based on business developments, market conditions, and liquidity needs. The Company continues to evaluate potential options, including equity offerings and debt financing, to provide financial flexibility and long-term growth.

The exercise price for our outstanding warrants is $11.50 per share of common stock, and the trading price of our common stock was $2.10 as of March 9, 2026. There is no guarantee that the warrants will be exercised prior to their expiration, however, we do not expect this to impact our liquidity.

Capital Expenditures and Other Contractual Obligations

Our capital expenditures amounted to $38.7 million and $49.9 million for the years ended December 31, 2025 and 2024, respectively. Our capital expenditures in 2025 were primarily related to our Huzhou Phase 3.2 expansion, which is funded primarily by localized borrowings and cash flow from our China operations, and deferred payments related to our Clarksville facility. 2024 capital expenditures were primarily related to the construction of manufacturing facilities in Clarksville, Tennessee and Huzhou, China.

In 2021, we started our capacity expansion plans in Huzhou, China, Berlin, Germany and Clarksville, Tennessee. The project in Germany was completed in 2021. The Huzhou Phase 3.1 expansion was successfully completed in 2023.

Because of delays in securing additional financing, in the fourth quarter of 2023 we began experiencing slow progress in continuing construction of our Clarksville expansion, slowing down certain construction work streams due to the need for additional financing. This facility was initially intended to produce 53.5Ah cells for our ESS solutions; however, we believe that LFP cells are better suited for our ESS solutions and intend to utilize the Tennessee facility to produce LFP cells instead of 53.5Ah cells. Additionally, our ESS products that were previously developed and assembled in Colorado are now planned to be assembled at our Tennessee facility once the facility is completed. The proceeds from the Business Combination alone will not be sufficient to complete the Clarksville expansion and meet our general working capital needs. Due to regulatory restrictions, adverse tax consequences, and localized working capital needs, we are currently unable to repatriate cash from China to fund U.S. operations or the Clarksville expansion. We are seeking alternate sources of capital to complete this facility and satisfy domestic content requirements for our U.S. customers.

Our future capital requirements will depend on many factors, including, but not limited to funding planned production capacity expansions and for general working capital. In addition, we may in the future enter into arrangements to acquire or invest in complementary businesses or technologies. We may need to seek additional equity or debt financing in order to meet these future capital requirements. If we are unable to raise additional capital when desired, or on terms that are acceptable to us, our business, financial condition, and results of operations could be adversely affected. There are no material off-balance sheet arrangements other than those described below.

Lease commitments

We lease certain facilities and equipment under non-cancellable lease agreements that expire at various dates through 2036. For additional information, see Note 17 – Leases, in the notes to the consolidated financial statements in Part II, Item 8 of this Report on Form 10-K.

Purchase commitments

We regularly enter into non-cancelable contractual obligations primarily related to purchases of inventory. As of December 31, 2025, such purchase commitments, which do not qualify for recognition on our consolidated balance sheets, amount to $37.2 million, most of which is short-term.

Cash Flows

The following table provides a summary of our cash flow data for the years indicated (in thousands):

Year Ended December 31,
2025 | 2024
Net cash generated from operating activities | 75,908 | 2,814
Net cash used in investing activities | (16,045) | (12,152)
Net cash (used in)/ provided by financing activities | (2,683) | 37,589

Cash Flows from Operating Activities

Net cash provided by operating activities was $75.9 million for the year ended December 31, 2025, an increase of $73.1 million compared to $2.8 million in 2024. This improvement was primarily driven by a $49.9 million increase in net income after adjusting for non-cash items and a $23.2 million net improvement in operating assets and liabilities. The increase in our net operating assets and liabilities was mainly driven by an increase of accounts payable and a decrease of inventories as compared to 2024, partially offset by an increase of accounts receivables due to revenue growth.

Cash Flows from Investing Activities

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-16_item1_business.md)

ITEM 1. BUSINESS

Business Overview

Founded in 2006 and headquartered in Stafford, Texas, Microvast Holdings, Inc. (NASDAQ: MVST) is a global leader in advanced specialized battery technologies. Since our public listing in 2021, we have focused on delivering high-performance lithium-ion battery solutions for the next generation of commercial and industrial electrification. We specialize in the design, development, and manufacturing of battery components and systems primarily for electric commercial vehicles and energy storage systems ("ESS"). Our guiding principle is to innovate lithium-ion battery designs from the ground up without relying on legacy technologies. We believe that this approach allows us to create purpose-built solutions for new markets, rather than repurposing existing ones.

Our mission is to become a leader in U.S. domestic battery production, reducing reliance on overseas suppliers, and strengthening national energy independence. We believe that this mission, along with our engineering expertise, vertically integrated business model, and our focus on continuous investment in our research and development and operations, differentiates us from competitors and positions us for long-term revenue and income growth.

We employ a vertically integrated approach, which we believe provides a competitive advantage in optimizing performance and cost. Our proprietary technology stack spans the entire battery system, including core cell materials (cathode, anode, electrolyte, and separator), cells, modules, packs, thermal management systems, and intelligent battery management systems. This end-to-end expertise has driven critical advancements in ultra-fast charging, high energy density, long cycle life, and safety, all critical factors for commercial transportation and ESS applications. With significant in-house capabilities in design, testing, and R&D, we continue to build an industry-leading body of knowledge in battery chemistry and performance.

Our Strategy

Our objective is to drive long-term stakeholder value by scaling our proprietary battery technologies across high-growth sectors. Since 2008, our research and development efforts have been dedicated to pioneering cutting-edge battery technologies that offer ultra-fast charging, extended cycle life, high energy density, and enhanced safety. Our commitment to innovation has well positioned us developing the next-generation lithium-ion batteries. We are focused on designing battery technologies for electric commercial vehicles and ESS. Our solutions empower industries to transition to cleaner, more efficient power sources, unlocking new levels of performance, longevity, and cost efficiency. Historically, demand for electric commercial vehicle batteries was concentrated in the Asia & Pacific regions. We are now working towards a balanced global strategy throughout EMEA and North America. As customer demand for our products and services has grown in Europe and the U.S., we have expanded to meet these growth opportunities. We continue to invest in our operations in Asia-Pacific to capitalize on regional growth. This provides a balanced global strategy while maintaining strong partnerships with OEMs in high-demand markets. We have primarily supplied our battery solutions to OEMs for use in electric commercial and specialty vehicles. We are continuously advancing our battery technologies to improve performance, efficiency, and reliability in commercial applications.

We believe the energy storage industry is positioned for continued expansion. In 2025, third-party industry data shows that global power capacity grew by approximately 90 gigawatts, an estimated 23% increase from the previous year. Industry projections indicate expected further expansion, with an average CAGR in deployed gigawatts of 23% between 2025 and 2035. The U.S. and China are expected to lead this growth, with U.S. power capacity projected to increase from approximately 45 gigawatts in 2025 to approximately 125 gigawatts by 2030. By refining our technology, we aim to advance our ESS solutions to meet the evolving demand of power sector and complement existing resources in meeting growing global demand for reliable and flexible power. We are leveraging many of the component-level technologies from our commercial vehicle segment to develop our energy storage products.

Our Products and Services

We believe the commercial vehicle market represents a continued growth opportunity. Our technology is currently deployed across a wide variety of platforms, including buses, heavy-duty trucks, port equipment, and heavy mining equipment. We have supported the deployment of the IVECO eDaily and various bus platforms (Citybus, Intercity, and Crossway). We also maintain active collaborations with leading OEMs including BAIC Truck, Higer Bus, and JBM Electric Vehicles. In the port and mining sectors, we have supplied Kalmar Corp., XCMG, and LGMG.

In November 5, 2025 we announced a partnership with Škoda Group to develop "Made in Europe" battery systems. The current solution under development utilizes Microvast's 37Ah LTO cell platform. This platform provides an energy density of approximately 95 Wh/kg at the cell level and is designed for high-rate charge and discharge capability. Under defined test conditions, the cell platform has demonstrated cycle life durability exceeding 20,000 cycles with approximately 80% capacity retention. The LTO chemistry is recognized for its rapid charge acceptance, long cycle life characteristics, and strong thermal stability, making it suitable for heavy-duty and high-cycle rail applications. The first prototype vehicles integrating the jointly developed battery electric multiple units are expected to be completed by the end of 2026 and are anticipated to be deployed starting in 2027.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-11_2-02-results.md, 10-K_2026-03-16_item7_mdna.md, 10-K_2026-03-16_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
