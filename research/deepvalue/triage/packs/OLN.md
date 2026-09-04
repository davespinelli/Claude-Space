# Triage pack — OLN · OLIN Corp

_Generated 2026-09-04 20:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** OLN · **Name:** OLIN Corp
- **CIK:** 0000074303
- **SIC:** 2800 — Chemicals & Allied Products
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/OLN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** OLIN Corp
- **CIK:** 74,303 · **SIC:** 2800 (Chemicals & Allied Products) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 16.97 |
| mktcap | $1.9B |
| ev | $4.8B |
| ev_ebit | 903.0x |
| fcf | $247.9M |
| fcf_yield | 12.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 0.1% |
| net_debt | $2.9B |
| net_debt_ebit | 538.1x |
| cash | $177.4M |
| ltd | $3.0B |
| equity | $1.7B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $6.8B |
| revenue_prior | $6.5B |
| rev_growth | 3.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $5.3M |
| net_income | -$101.1M |
| cfo | $474.2M |
| capex | $226.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 113,982,490 |
| shares_py | 114,641,535 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -17.8% |
| r6m | -29.8% |
| off_52w_high | -42.6% |
| adv20 | $47.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.79 |
| r_ev_ebit | 0.00 |
| r_roic | 0.31 |
| r_rev_growth | 0.48 |
| r_buyback | 0.72 |
| score | 0.46 |

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
| rank | 281 |

**Screen rationale:** top-quartile FCF yield 12.8%


## 3. Share count trend

- Shares outstanding: **113,982,490** (CY2026Q2I) vs **114,641,535** prior year (CY2025Q2I)
- Change: **-0.6%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-16** — Item 1.01 (Entry into a Material Definitive Agreement): On June 15, 2026, Olin Corporation, a Virginia corporation (" Olin " or, with reference to the post-closing period, the " Combined Company "), entered into an Agreement and Plan of Merger (the " Merger Agreement ") with Huntsman Corporation, a Delaware...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 25 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 5 |
| M | 12 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'Olin Announces Second Quarter 2026 Results'; skipped 41 forward-looking-statement block(s); 9 block(s) of pre-heading matter dropped._

## EX-99.1 - Q2 2026 EARNINGS RELEASE (exhibit991q22026earningspr.htm)

Olin Announces Second Quarter 2026 Results

Highlights

• Second quarter 2026 net loss of ($13.3) million, or ($0.12) per diluted share

• Quarterly adjusted EBITDA of $191.3 million

Clayton, MO, July 30, 2026 – Olin Corporation (NYSE: OLN) announced financial results for the second quarter ended June 30, 2026. Second quarter 2026 reported net loss was ($13.3) million, or ($0.12) per diluted share, which compares to second quarter 2025 reported net loss of ($1.3) million, or ($0.01) per diluted share. Second quarter 2026 adjusted EBITDA of $191.3 million excludes depreciation and amortization expense of $122.1 million, acquisition-related costs of $10.6 million, and restructuring charges of $10.5 million. Second quarter 2025 adjusted EBITDA was $176.1 million. Sales in the second quarter 2026 were $1,741.9 million, compared to $1,758.3 million in the second quarter 2025.

Ken Lane, President and Chief Executive Officer, said, "The Olin team delivered sequential improvement in adjusted EBITDA in a highly volatile environment. Our Chlor Alkali Products and Vinyls business benefited from improved caustic soda and ethylene dichloride pricing and from favorable operating performance driven by our Beyond250 structural cost actions. However, partially offsetting this performance was an unplanned shutdown of the vinyl chloride monomer plant in Freeport, Texas. Operations have resumed at reduced rates. The disruption reduced second quarter adjusted EBITDA by $40 million, with an estimated $20 million impact expected in the third quarter as full rates are planned to resume late in the quarter. Epoxy continued to improve as margins expanded despite persistent weak demand conditions in Europe. Winchester's sequential improvement was driven by stronger commercial demand and pricing actions implemented to offset commodity metals and raw materials cost inflation.

"Looking ahead, we expect our Chemical businesses' third quarter 2026 results to be comparable to the second quarter, as reduced operating rates at the vinyl chloride monomer facility and weaker ethylene dichloride

pricing offset expected stronger caustic soda volumes. In our Winchester business, seasonally improving commercial demand is expected to support sequential earnings growth. With continued significant global volatility, third quarter 2026 adjusted EBITDA is forecast to be in the range of $160 million to $200 million," Lane concluded.

SEGMENT REPORTING

Olin defines segment earnings as income (loss) before interest expense, net, other operating income (expense), non-operating pension income, other income, and income taxes.

CHLOR ALKALI PRODUCTS AND VINYLS

Chlor Alkali Products and Vinyls sales for the second quarter 2026 were $819.5 million, compared to $979.5 million in the second quarter 2025. The decrease in sales was due to lower volumes, primarily resulting from lower trading volumes associated with Blue Water Alliance and lower vinyl chloride monomer volumes. The Blue Water Alliance joint venture concluded operations at the end of 2025. Second quarter 2026 segment earnings were $53.4 million, compared to $64.9 million in the second quarter 2025. Second quarter 2026 segment results were negatively impacted by $40.1 million from operating issues with the vinyl chloride monomer plant at the Freeport, Texas facility resulting in higher costs and reduced profit from lost sales. The remaining $28.6 million increase in segment earnings was primarily due to higher pricing, primarily caustic soda and ethylene dichloride, partially offset by higher raw material costs, primarily natural gas and electrical power costs. Chlor Alkali Products and Vinyls second quarter 2026 results included depreciation and amortization expense of $98.1 million compared to $106.3 million in the second quarter 2025.

EPOXY

Epoxy sales for the second quarter 2026 were $422.1 million, compared to $331.2 million in the second quarter 2025. The increase in sales was due to higher volumes and improved pricing. Second quarter 2026 segment earnings were $16.0 million, compared to a segment loss of ($23.7) million in the second quarter 2025. The $39.7 million increase in segment results was primarily due to higher volumes, improved product margins, and lower operating costs. Product margins improved year-over-year with higher pricing partially offset by higher raw material costs, primarily benzene and propylene. Epoxy second quarter 2026 results included depreciation and amortization expense of $11.7 million compared to $13.1 million in the second quarter 2025.

WINCHESTER

Winchester sales for the second quarter 2026 were $500.3 million, compared to $447.6 million in the second quarter 2025. The increase in sales was primarily due to higher commercial ammunition sales and higher

military project revenue. Second quarter 2026 segment earnings were $28.1 million, compared to $25.0 million in the second quarter 2025. The $3.1 million increase in segment earnings was primarily due to higher commercial ammunition pricing and volume and higher military project revenue, partially offset by higher raw material costs, primarily commodity metal costs, and higher operating costs. Winchester second quarter 2026 results included depreciation and amortization expense of $8.8 million compared to $7.9 million in the second quarter 2025.

CORPORATE AND OTHER COSTS

Other corporate and unallocated costs in the second quarter of 2026 increased $5.4 million compared to the second quarter 2025 primarily due to an unfavorable impact from foreign currency, partially offset by lower stock-based compensation, which includes mark-to-market adjustments.

PROPOSED MERGER OF EQUALS

On June 16, 2026, Olin and Huntsman Corporation announced that they have entered into a definitive agreement to combine in an all-stock merger of equals to form a combined company, OlinHuntsman Corporation. Second quarter 2026 results included acquisition-related costs of $10.6 million related to this pending merger.

Completion of the merger, which is expected to occur in the first half of 2027, is subject to the satisfaction of customary closing conditions, including the receipt of required regulatory approvals and approval of the merger by both Olin shareholders and Huntsman stockholders.

LIQUIDITY

The cash balance on June 30, 2026, was $177.4 million. Olin ended the second quarter 2026 with net debt of approximately $2.85 billion and a net debt to adjusted EBITDA ratio of 5.0 times. On June 30, 2026, Olin had available liquidity of approximately $1.2 billion, including unrestricted access to the undrawn portion of its revolving credit facility. Working capital increased $183.0 million in the first half 2026. In addition to the normal seasonal working capital built in first half of the year, which we expect to liquidate during the second half, Olin paid approximately $93 million, including previously accrued reserves, to resolve legacy Shintech litigation matters and expect to pay the remaining approximately $100 million in the second half of 2026.

CONFERENCE CALL INFORMATION

Olin senior management will host a conference call to discuss second quarter 2026 financial results at 9:00 a.m. Eastern Time on Friday, July 31, 2026. Remarks will be followed by a question-and-answer session. Associated slides and the conference call webcast are accessible via Olin's website, www.olin.com , under the second

quarter conference call icon. An archived replay of the webcast will also be available in the Investor Relations section of Olin's website beginning at 12:00 p.m. Eastern Time. A final transcript of the call will be posted the next business day.

COMPANY DESCRIPTION

Olin Corporation is a leading vertically integrated global manufacturer and distributor of chemical products and a leading U.S. manufacturer of ammunition. The chemical products produced include chlorine and caustic soda, vinyls, epoxies, chlorinated organics, bleach, hydrogen, and hydrochloric acid. Winchester's principal manufacturing facilities produce and distribute sporting ammunition, law enforcement ammunition, reloading components, small caliber military ammunition and components, industrial cartridges, and clay targets, along with contracted U.S. military project revenue.

Visit www.olin.com for more information on Olin Corporation.

Olin Corporation
Consolidated Balance Sheets (a)
June 30, | December 31, | June 30,
($ in millions, except per share data) | 2026 | 2025 | 2025
Assets:
Cash and Cash Equivalents | 177.4 | 167.6 | 223.8
Accounts Receivable, Net | 988.6 | 844.5 | 1,044.5
Income Taxes Receivable | 54.3 | 66.6 | 29.1
Inventories, Net | 847.2 | 784.5 | 919.1
Other Current Assets | 120.4 | 107.9 | 70.2
Total Current Assets | 2,187.9 | 1,971.1 | 2,286.7
Property, Plant and Equipment (Less Accumulated Depreciation of $5,587.3, $5,508.7 and $5,417.0) | 2,089.0 | 2,196.9 | 2,260.8
Operating Lease Assets, Net | 365.4 | 298.6 | 281.8
Deferred Income Taxes | 45.2 | 47.2 | 59.7
Other Assets | 1,169.8 | 1,210.0 | 1,159.7
Intangibles, Net | 155.6 | 174.4 | 193.7
Goodwill | 1,427.7 | 1,427.6 | 1,425.5
Total Assets | 7,440.6 | 7,325.8 | 7,667.9
Liabilities and Shareholders' Equity:
Current Installments of Long-term Debt | — | 109.7 | 19.2
Accounts Payable | 910.3 | 806.1 | 901.0
Income Taxes Payable | 13.7 | 23.9 | 44.1
Current Operating Lease Liabilities | 73.0 | 59.7 | 61.0
Accrued Liabilities | 546.1 | 630.1 | 520.6
Total Current Liabilities | 1,543.1 | 1,629.5 | 1,545.9
Long-term Debt | 3,029.1 | 2,717.6 | 2,977.5
Operating Lease Liabilities | 305.4 | 252.5 | 226.4
Accrued Pension Liability | 197.2 | 200.9 | 227.4
Deferred Income Taxes | 312.8 | 317.6 | 380.8
Other Liabilities | 341.2 | 337.1 | 322.1
Total Liabilities | 5,728.8 | 5,455.2 | 5,680.1
Commitments and Contingencies
Shareholders' Equity:
Common Stock, $1.00 Par Value Per Share; Authorized 240.0 Shares; Issued and Outstanding 114.0, 113.6 and 114.6 Shares | 114.0 | 113.6 | 114.6
Additional Paid-in Capital | 11.9 | — | —
Accumulated Other Comprehensive Loss | (412.4) | (414.5) | (451.4)
Retained Earnings | 1,997.9 | 2,139.8 | 2,294.0
Olin Corporation's Shareholders' Equity | 1,711.4 | 1,838.9 | 1,957.2
Noncontrolling Interests | 0.4 | 31.7 | 30.6
Total Equity | 1,711.8 | 1,870.6 | 1,987.8
Total Liabilities and Equity | 7,440.6 | 7,325.8 | 7,667.9
(a) Unaudited.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-20_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

Net loss was $(100.5) million for 2025 compared to net income of $108.6 million for 2024, a decrease of $209.1 million. The decrease in results from the prior year was primarily due to lower operating results across all of our business segments. Diluted net loss per share was $(0.88) for 2025 compared to diluted net income per share of $0.91 for 2024, a decrease of $1.79 per share, or 197%.

Chlor Alkali Products and Vinyls repo rted segment income was $181.1 million for 2025 compared to segment income of $296.4 million for 2024. Chlor Alkali Products and Vinyls 2025 segment income included a $75.0 million pretax charge associated with a litigation loss contingency related to a VCM customer dispute and 2024 segment income included a $93.6 million penalty associated with Hurricane Beryl. The remaining decrease of $133.9 million in segment income from the prior year was primarily due to lower pricing, primarily EDC, and higher raw material and operating costs, including planned maintenance turnaround expenses, partially offset by higher volumes and the 45V Tax Credit (defined below in Other Items).

Epoxy reported segment loss was $(103.5) million for 2025 compared to segment loss of $(85.0) million for 2024. Epoxy's 2024 segment loss included a $32.7 million penalty associated with Hurricane Beryl. The remaining decrease of $51.2 million in Epoxy segment results, as compared to the prior year, was primarily due to higher operating costs, including unabsorbed fixed manufacturing costs incurred from planned inventory reductions and planned maintenance turnarounds, partially offset by improved volumes. Global epoxy demand remains challenged, with continued market saturation from subsidized Asian competition.

Winchester reported segment income of $67.7 million for 2025 compared to segment income of $237.9 million for 2024. Winchester segment results were lower than in the prior year primarily due to decreased commercial ammunition sales volumes and pricing, along with higher raw material and operating costs, including commodity metal and propellant costs, partially offset by higher military project revenue.

Liquidity and Share Repurchases

During 2025, we repurchased and retired 2.2 million shares of common stock at a total value of $50.5 million. As of December 31, 2025, we had $1.9 billion of remaining authorization to repurchase shares of our common stock under our 2022 Repurchase Authorization and 2024 Repurchase Authorization (both defined in Liquidity and Capital Resources) programs.

On March 14, 2025, we issued $600.0 million aggregate principal amount of 6.625% senior notes due April 1, 2033 (2033 Notes), in a private offering exempt from the registration requirements of the Securities Act of 1933, as amended.

On March 14, 2025, we entered into a new $1,850.0 million senior credit facility (2025 Senior Credit Facility), which increased the borrowing limit of our then-existing credit facility by $300.0 million and extended the maturity date from October 11, 2027 to March 14, 2030. Pursuant to the agreement, the aggregate principal amount under our term loan facility increased from $350.0 million to $650.0 million and the aggregate principal amount under our revolving credit facility remained at $1,200.0 million. The term loan was fully drawn on the closing date.

During 2025, we had debt repayments, net of borrowings, of $11.2 million. Proceeds from the 2033 Notes, together with borrowings under the 2025 Senior Credit Facility, were used to redeem the $108.6 million 9.50% senior notes due 2025 (2025 Notes), redeem the $500.0 million 5.125% senior notes due 2027 (2027 Notes), refinance the then-existing $1,550.0 million senior credit facility (2022 Senior Credit Facility), comprised of $505.0 million of borrowings under the revolving credit

facility with aggregate commitments of $1,200.0 million (2022 Revolving Credit Facility) and $332.5 million of borrowings under the term loan facility with aggregate commitments of $350.0 million (2022 Term Loan Facility), and pay related fees and expenses.

Subsequent Event - Credit Facility

On February 19, 2026, we executed an amendment to the 2025 Senior Credit Facility (Senior Secured Credit Facility) which, among other things, modified the financial covenants to be less restrictive and incorporated guarantees and collateral by certain of our domestic subsidiaries. The amendment required all remaining principal amortization payments under the Secured Term Loan Facility (as defined in Liquidity and Capital Resources) to be satisfied. Borrowings under the Senior Secured Revolving Credit Facility (as defined in Liquidity and Capital Resources) were used to satisfy the $109.7 million remaining principal amortization payments under the Secured Term Loan Facility. The maturity date for the Senior Secured Credit Facility remained March 14, 2030.

The amendment requires that the obligations under the Senior Secured Credit Facility be guaranteed by certain of our domestic subsidiaries. The obligations under the Senior Secured Credit Facility are also secured by liens on substantially all of Olin's and the subsidiary guarantors' personal property (Collateral), other than certain principal properties and capital stock of subsidiaries, and subject to certain other exceptions. The amendment provides that substantially all guarantees under the Senior Secured Credit Facility and liens on Collateral be released automatically upon notice by Olin, or after September 30, 2027, upon which time all covenant reliefs expire.

International Trade

Tariffs and trade flows continue to impact the demand outlook amid varying market responses. While we are continuing to monitor the situation, as of the date of this filing, the direct impact from current tariffs has not been significant to our chemicals businesses. Our chemicals businesses generally source and sell where we produce. An exception to this would be potential retaliatory tariffs on caustic soda and EDC exports, which could alter the economics rapidly within the respective countries. We continue to monitor and assess the impact of tariffs on goods being imported into the United States and the competitiveness of our export products in markets which implement retaliatory tariffs. Additionally, although Winchester procures the majority of metals domestically, we have realized price inflation that we believe is partially tariff driven for the domestic supply of copper, steel and tungsten products. Winchester has also realized secondary effects from suppliers consuming tariff impacted metals in their end products. Our global supply chain organization continuously monitors market trends and works to mitigate those and other cost increases through economies of scale in global procurement and efficient sourcing practices.

Other Items

On April 18, 2025, Olin acquired AMMO, Inc.'s small caliber ammunition manufacturing assets for total consideration of $55.8 million. The acquisition, which includes AMMO Inc.'s brass shellcase capabilities and its 185,000 square foot production facility located in Manitowoc, WI, is included in Olin's Winchester segment. The acquisition was financed with cash on hand.

On September 18, 2025, we announced a mutual decision with Mitsui & Co., Ltd. to end our joint venture, Blue Water Alliance, by the end of 2025. This decision was made to evolve our EDC participation by emphasizing longer-term structural opportunities that enhance value and optionality. On November 11, 2025, Olin announced a commercial arrangement with Braskem, one of the largest petrochemical companies in the Americas and the leading producer of PVC in South America, for Olin to supply EDC to Braskem, aligning with Braskem's transformation of its chlor alkali and vinyl assets in Brazil.

In the third quarter of 2025, Olin determined that it qualified for the clean hydrogen production tax credit under Section 45V as part of the Inflation Reduction Act of 2022 (45V Tax Credit). We received notice of our provisional carbon dioxide emissions rate from the United States Department of Energy, which was a major milestone for recognition. The 45V Tax Credit is available for qualified clean hydrogen produced and sold during the 10-year period beginning on the date the qualified clean hydrogen production facility was originally placed in service. Since the 45V Tax Credit is refundable, we account for the 45V Tax Credit under a government grant model. As a result, during 2025 Olin recorded a $34.5 million reduction to cost of goods sold primarily related to the sale and use of hydrogen produced at certain of our chlor alkali plants. We expect an annual pretax benefit of $15 million to $20 million for years 2026 through 2028, with lower amounts through 2032. The impact of the 45V Tax Credit is included within the Chlor Alkali Products and Vinyls segment results.

Subsequent Event - Litigation Matter

In April 2023, Shintech filed a lawsuit against Olin Corporation and its wholly owned subsidiary, Blue Cube Operations LLC. Shintech alleged that Olin breached a long‑term VCM supply agreement relating to deliveries to Shintech's PVC facility in Freeport, TX, following a pricing dispute, a 2023 maintenance turnaround at Olin's Freeport, TX VCM facility, and Olin's declaration of force majeure at Olin's Freeport, TX VCM facility. After nearly three years of litigation, on February 10, 2026, the jury returned a verdict in favor of Shintech on its breach‑of‑contract claims. As a result of this verdict, the Company obtained new information related to this litigation loss contingency and recorded a pretax charge of $75.0 million in the fourth quarter 2025. During the first half of 2026, we expect to pay approximately $185 million to Shintech associated with the litigation matter, and previously recorded accruals for a VCM pricing dispute with Shintech.

CONSOLIDATED RESULTS OF OPERATIONS

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-20_item1_business.md)

Item 1. BUSINESS

GENERAL

Olin Corporation (Olin, the Company, we or our) is a Virginia corporation, incorporated in 1892, having its principal executive offices in Clayton, MO. We are a leading vertically integrated global manufacturer and distributor of chemical products and a leading U.S. manufacturer of ammunition. Our operations are concentrated in three business segments: Chlor Alkali Products and Vinyls, Epoxy and Winchester. All of our business segments are capital-intensive manufacturing businesses. The Chlor Alkali Products and Vinyls segment manufactures and sells chlorine and caustic soda, ethylene dichloride (EDC) and vinyl chloride monomer (VCM), methyl chloride, methylene chloride, chloroform, carbon tetrachloride, perchloroethylene, hydrochloric acid, hydrogen, bleach products and potassium hydroxide, which represented 54% of 2025 sales. The Epoxy segment produces and sells a full range of epoxy materials and precursors, including aromatics (acetone and phenol), allyl chloride, epichlorohydrin, liquid epoxy resins, solid epoxy resins and formulated solutions products such as converted epoxy resins and additives, which represented 20% of 2025 sales. The Winchester segment produces and sells sporting ammunition, reloading components, small caliber military ammunition and components, industrial cartridges and clay targets, along with contracted U.S. military project revenue, which represented 26% of 2025 sales. See our discussion of our segment disclosures contained in Item 7—"Management's Discussion and Analysis of Financial Condition and Results of Operations."

GOVERNANCE

We maintain a website at www.olin.com . Our reports on Form 10-K, Form 10-Q and Form 8-K, as well as amendments to those reports, are available free of charge on our website, as soon as reasonably practicable after we file the reports with the Securities and Exchange Commission (SEC). Also, a copy of our electronically filed materials can be obtained at www.sec.gov . Our Principles of Corporate Governance, Committee Charters and Code of Conduct are available on our website at www.olin.com in the Leadership & Governance Section under Governance Documents and Committees.

PRODUCTS, SERVICES AND STRATEGIES

Chlor Alkali Products and Vinyls

Products and Services

We have been involved in the chlor alkali industry for approximately 135 years and consider ourselves the leading global chlor alkali and derivatives producer. Chlorine, caustic soda and hydrogen are co-produced commercially by the electrolysis of salt at a fixed ratio of 1.0 ton of chlorine to 1.1 tons of caustic soda and 0.03 tons of hydrogen. The industry refers to this as an Electrochemical Unit or ECU.

Chlorine is used as a raw material in the production of thousands of products, including vinyls, urethanes, epoxy, water treatment chemicals and a variety of other organic and inorganic chemicals. A significant portion of chlorine production is consumed in the manufacturing of vinyls intermediates, EDC and VCM, both of which our Chlor Alkali Products and Vinyls segment produces. A large portion of our EDC production is utilized in the production of VCM, but we are also one of the largest global participants in merchant EDC sales. In addition to marketing Olin produced EDC, we also purchase EDC for re-sale on a global basis. EDC and VCM are precursors for polyvinyl chloride (PVC), a material used in applications such as vinyl siding, pipe, pipe fittings and automotive parts.

Our Chlor Alkali Products and Vinyls segment is one of the largest global marketers of caustic soda, including caustic soda produced by Olin, and globally produced material purchased by Olin for re-sale. The diversity of caustic soda sourcing allows us to cost effectively supply customers worldwide. Caustic soda has a wide variety of end-use applications, the largest of which includes water treatment, alumina, pulp and paper, urethanes, detergents and soaps and a variety of other organic and inorganic chemicals.

Our Chlor Alkali Products and Vinyls segment also includes our chlorinated organics business, which is a significant global producer of chlorinated organic products that include chloromethanes (methyl chloride, methylene chloride, chloroform and carbon tetrachloride) and chloroethanes (perchloroethylene). Our chlorinated organics business participates in both the solvent segment and the intermediate segment where Olin's products are used as feedstocks for fluorocarbons, silicones and cellulosics.

We also manufacture and sell other chlor alkali-related products, including hydrochloric acid, sodium hypochlorite (bleach) and potassium hydroxide. These products, along with chlorinated organics products and epoxy resins, generally consume chlorine as a raw material creating downstream applications that upgrade the value of the ECU. Our industry leadership in the production of chlorinated organics and epoxy resins, as well as other products, offers us multiple outlets for our captive chlorine.

Our products are delivered by pipeline, marine vessel, deep-water and coastal barge, railcar and truck. We own, operate, and lease a geographically dispersed terminal infrastructure at our production sites and other locations that expand our geographic coverage and enhance our service capabilities. At our largest integrated product sites, our deep-water access allows us to reach global markets.

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
