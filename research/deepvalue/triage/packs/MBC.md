# Triage pack — MBC · MasterBrand, Inc.

_Generated 2026-09-04 23:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MBC · **Name:** MasterBrand, Inc.
- **CIK:** 0001941365
- **SIC:** 2511 — Wood Household Furniture, (No Upholstered)
- **Fiscal year end (MM-DD):** 12-28
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MBC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** MasterBrand, Inc.
- **CIK:** 1,941,365 · **SIC:** 2511 (Wood Household Furniture, (No Upholstered)) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 8.17 |
| mktcap | $1.7B |
| ev | $2.8B |
| ev_ebit | 23.5x |
| fcf | $117.5M |
| fcf_yield | 7.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 3.0% |
| net_debt | $1.1B |
| net_debt_ebit | 9.5x |
| cash | $241.6M |
| ltd | $1.4B |
| equity | $2.0B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $2.7B |
| revenue_prior | $2.7B |
| rev_growth | 1.3% |
| rev_growth_note | share count +60.6% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $119.0M |
| net_income | $26.7M |
| cfo | $195.7M |
| capex | $78.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 60.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 203,490,490 |
| shares_py | 126,730,924 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -26.8% |
| r6m | -12.2% |
| off_52w_high | -40.9% |
| adv20 | $14.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.59 |
| r_ev_ebit | 0.38 |
| r_roic | 0.42 |
| r_rev_growth | 0.39 |
| r_buyback | 0.04 |
| score | 0.36 |

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
| rank | 356 |

**Screen rationale:** share count +60.6% yoy — growth may be acquisition/issuance-driven, not organic


## 3. Share count trend

- Shares outstanding: **203,490,490** (CY2026Q2I) vs **126,730,924** prior year (CY2025Q2I)
- Change: **60.6%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +60.6% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-28** — Item 5.02 (officer / director change or comp arrangement): The following three (3) former directors of American Woodmark were appointed to serve as independent directors on the Board of Directors of MasterBrand (the "Board"), effective as of the Effective Time: Andrew Cogan, Philip Fracassa and Daniel Hendrix (the...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 16,587 sh / $147,790 vs sells 82,245 sh / $752,782 -> net $-604,991 (SELLING).
Distinct insiders buying (code P): 2. Largest buy: PETRATIS DAVID D bought 11,587 sh @ $8.82 ($102,240) on 2026-06-08.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 2, sales 4).

| code | rows |
|---|---|
| A | 7 |
| P | 2 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'MasterBrand Reports Second Quarter 2026 Financial Results'; skipped 37 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q22026earningspressrelease.htm)

MasterBrand Reports Second Quarter 2026 Financial Results

• Closed transformative all-stock merger with American Woodmark during the quarter and raised long-term annual run-rate cost synergy target to over $100 million

• Net sales were $815.2 million , including a $125.5 million contribution from American Woodmark

• Net loss was $(57.6) million and net loss margin was (7.1)%

• Adjusted EBITDA 1 was $62.5 million, representing an adjusted EBITDA margin 1 of 7.7%

• Diluted (loss) earnings per share were $(0.38), compared to $0.29 in the prior year period, adjusted diluted earnings per share 1 were $0.05, compared to $0.40 in the prior year period

• Company introduces second- half 2026 financial outlook, which includes $15 million of synergy realization from the $30 million in annualized synergies executed to date

BEACHWOOD, Ohio.--(BU SINESS WIRE)--August 4, 2026-- MasterBrand, Inc. (NYSE: MBC, the "Company," or "MasterBrand"), the largest residential cabinet manufacturer in North America, today announced second quarter 2026 financial results.

"The second quarter marked an important milestone for MasterBrand. We completed our merger with American Woodmark, establishing the most comprehensive portfolio of trusted cabinetry brands in North America , while our legacy business delivered results largely in line with our outlook despite continued softness in demand," said Dave Banyard, President and Chief Executive Officer. "With integration ahead of schedule, we remain confident that this combination positions MasterBrand to streamline our cost structure, unlock greater earnings power, and drive growth as our markets recover."

Second Quarter 2026

Results for the second quarter include American Woodmark from the May 28, 2026 close date. Prior year comparisons reflect legacy MasterBrand only.

Net sales were $815.2 million , including a $125.5 million contribution from American Woodmark. Legacy MasterBrand net sales were $689.7 million, a decrease of 5.6% compared to the second quarter of 2025, reflecting a mid- to high-single-digit market decline, as expected, slightly offset by favorable net average selling price ("ASP") due to the flow through of tariff pricing.

Gross profit was $205.5 million , with a contribution of $16.7 million from American Woodmark. Gross profit margin was 25.2%. Legacy MasterBrand gross profit was $188.8 million, compared to $239.7 million in the prior year period. Legacy gross profit margin decreased 540 basis points to 27.4%, compared to 32.8% in the second quarter of 2025, driven by lower volume and the related unfavorable fixed cost leverage , unfavorable product mix, and material, labor, and freight inflation, partially offset by our continuous improvement efforts and favorable ASP from tariff pricing flow-through.

Net (loss) income was $(57.6) million, with a contribution of $(28.9) million from American Woodmark and net (loss) income margin was (7.1)%. Legacy net (loss) income was $(28.7) million compared to $37.3 million in the second quarter of 2025 and net (loss) income margin was (4.2)% , compared to net income margin of 5.1% in the prior year, driven by lower gross profit and higher SG&A expenses, primarily due to merger-related costs, and a higher tax expense due to non-deductible expenses and jurisdictional differences, partially offset by the initial benefits of cost actions taken in the quarter.

1 - See "Non-GAAP Financial Measures" and the corresponding financial tables at the end of this press release for definitions and reconciliations of non-GAAP measures.

Adjusted EBITDA 1 was $62.5 million , including a $4.3 million contribution from American Woodmark. Adjusted EBITDA margin 1 was 7.7% . Legacy MasterBrand adjusted EBITDA 1 was $58.2 million compared to $105.4 million in the prior year period, and adjusted EBITDA margin 1 was 8.4%, down 600 basis points due to market driven volume declines and the related unfavorable fixed cost leverage, unfavorable product mix, and material, labor, and freight inflation, partially offset by the flow through of tariff mitigation, our continuous improvement efforts and previously announced cost actions.

Diluted (loss) earnings per share were $(0.38) based on 153.6 million weighted average shares outstanding compared to $0.29 in the second quarter of 2025 based on 129.1 million weighted average shares outstanding. Adjusted diluted earnings per share 1 was $0.05 based on 153.6 million weighted average shares outstanding compared to $0.40 in the second quarter of 2025 based on 129.1 million weighted average shares outstanding.

American Woodmark Integration and Synergies

On May 28, 2026, MasterBrand completed its merger with American Woodmark, creating the most comprehensive portfolio of trusted cabinetry brands in North America . Integration of American Woodmark is underway, with approximately $30 million of annual synergy actions completed as of the end of July. The Company now expects over $100 million in annual run-rate cost synergies by the end of year three post-close, exceeding its original synergy target. This target excludes the previously announced $30 million legacy MasterBrand cost reduction initiative and American Woodmark's closure of its Monterrey, Mexico facility, both of which are incremental.

1 - See "Non-GAAP Financial Measures" and the corresponding financial tables at the end of this press release for definitions and reconciliations of non-GAAP measures.

Balance Sheet, Cash Flow and Capital Allocation

As of June 28, 2026 , th e Company had $241.6 million in cash and $393.9 million of availability under its revolving credit facility. Additionally, total debt was $1,390.3 million, net debt 1 was $1,148.7 million and the ratio of net debt to adjusted EBITDA 1 from the most recent trailing twelve months, inclusive of American Woodmark's most recent trailing twelve-months adjusted EBITDA 1 , was 3.9x. The Company's credit agreement permits the inclusion of trailing twelve-month adjusted EBITDA for American Woodmark and stock-based compensation, among other permitted adjustments, for covenant compliance purposes. The Company remained in full compliance with all applicable financial covenants related to its outstanding debt as of the end of the second quarter.

Net cash provided by operating activities was $5.8 million for the twenty-six weeks ended June 28, 2026, compared to $53.4 million for the twenty-six weeks ended June 29, 2025. Free cash flow 1 was $(17.6) million for the twenty-six weeks ended June 28, 2026, compared to $25.5 million in the prior-year period. The decrease in net cash provided by operating activities and free cash flow were driven by a decrease in net income in the twenty-six weeks ended June 28, 2026 compared to the twenty-six weeks ended June 29, 2025.

No share repurchases were made during the second quarter of 2026. The Company intends to prioritize integration investments and debt reduction and is currently targeting net leverage below 2.0x by the end of 2028.

Second-Half 2026 Financial Outlook

For the second half of 2026, the Company expects the following:

• Net sales of $2.05 to $2.11 billion

• Adjusted EBITDA 1,2 in the range of $129 to $149 million, with related adjusted EBITDA margin 1,2 in the range of 6.3% to 7.1%

• Adjusted diluted earnings per share 1,2 in the range of $(0.05) to $0.03

◦ Reflects interest expense of approximately $50 million, reflecting the newly arranged $375 million delayed-draw Term Loan A used to retire American Woodmark's debt at close

This outlook reflects the combined company, with American Woodmark included for the full second half, and includes approximately $15 million of synergy capture and approximately $11 million of IEEPA duty refunds received and expected to be received over the period.

For full year 2026, MasterBrand is reiterating its expectation that its addressable market will be down mid-single digits. The Company now expects the following:

• Gross tariff costs of approximately 5-6% of full-year 2026 net sales; expected to be fully offset on a dollar-for-dollar run-rate basis by end of year

• The Company continues to expect free cash flow¹ for full-year 2026 to be in excess of net income

1 - See "Non-GAAP Financial Measures" and the corresponding financial tables at the end of this press release for definitions and reconciliations of non-GAAP measures.

2 - We have not provided a reconciliation of our second half of 2026 adjusted EBITDA, adjusted EBITDA margin and adjusted diluted EPS guidance because the information needed to reconcile these measures is unavailable due to the inherent difficulty of forecasting the timing or amount of various items that have not yet occurred and which may be excluded from adjusted EBITDA, adjusted EBITDA margin and adjusted diluted EPS. Additionally, estimating such GAAP measures and providing a meaningful reconciliation for future periods requires a level of precision that is unavailable for these future periods and cannot be accomplished without unreasonable effort. Forward-looking non-GAAP measures are estimated consistent with the relevant definitions and assumptions used for historical non-GAAP measures.

This financial outlook only reflects the impact of those tariffs in effect as of the date of this release and does not reflect any other potential tariffs or tariff-related impacts on company costs or end market demand. The Company believes the dynamic nature of tariffs, specifically the uncertainty of implementation, potential timing and duration, limits the usefulness of estimating this information. MasterBrand undertakes no obligation to update this outlook as circumstances evolve. This outlook reflects the combined company including American Woodmark.

"Our teams continued to execute cost actions and tariff mitigation efforts while accomplishing early synergy realization from the combination," said Andi Simon, Executive Vice President and Chief Financial Officer. "With the merger complete and integration planning continuing and converting to execution, we are introducing second-half 2026 outlook for the combined company. Our priorities from here are clear: disciplined execution on costs and synergies, and steady progress on the balance sheet."

Conference Call Details

The Company will hold a live conference call and webcast at 4:30 p.m. ET today, August 4, 2026, to discuss the financial results and business outlook. Telephone access to the live call will be available at ( 877) 407-4019 (U.S.) or by dialing +1 ( 201) 689-8337 (international). The live audio webcast can be accessed on the "Investors" section of the MasterBrand website www.masterbrand.com .

A telephone replay will be available approximately one hour following completion of the call through August 18, 2026. To access the replay, please dial (877) 660-6853 (U.S.) or +1 (201) 612-7415 (international). The replay passcode is 13761068 . An archived webcast of the conference call will also be available on the "Investors" page of the Company's website.

Non-GAAP Financial Measures

To supplement the financial information presented in accordance with generally accepted accounting principles in the United States ("GAAP") in this earnings release, certain non-GAAP financial measures as defined under SEC rules have been included. It is our intent to provide non-GAAP financial information to enhance understanding of our financial information as prepared in accordance with GAAP. Non-GAAP financial measures should be considered in addition to, not as a substitute for, other financial measures prepared in accordance with GAAP. Our methods of determining these non-GAAP financial measures may differ from the methods used by other companies for these or similar non-GAAP financial measures. Accordingly, these non-GAAP financial measures may not be comparable to measures used by other companies.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-13_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Introduction

Management's Discussion and Analysis of Financial Condition and Results of Operations ("MD&A") is a supplement to the accompanying consolidated financial statements of MasterBrand and its consolidated subsidiaries and provides additional information on our business, recent developments, financial condition, liquidity and capital resources, cash flows and results of operations.

MD&A is organized as follows:

• Overview : This section provides a general description of our business, as well as recent developments we believe are important in understanding our results of operations and financial condition or in understanding anticipated future trends.

• Results of Operations : Our consolidated financial statements have been prepared in accordance with accounting principles generally accepted in the United States of America ("GAAP") and are based on a 52- or 53-week fiscal year ending on the last Sunday in December in each calendar year. This section provides an analysis of our results of operations for the 52-week period that ended on December 28, 2025 as compared to the 52-week period that ended on December 29, 2024. Unless the context otherwise requires, references to years and quarters contained in this Annual Report on Form 10-K pertain to our fiscal years and fiscal quarters. Additionally, unless the context otherwise requires, references in this Annual Report on Form 10-K to: (1) "2025," "fiscal 2025" or our "2025 fiscal year" refers to our 2025 fiscal year that is a 52-week period that ended on December 28, 2025; (2)"2024," "fiscal 2024" or our "2024 fiscal year" refers to our 2024 fiscal year that was a 52-week period that ended on December 29, 2024; and (3) "2023," "fiscal 2023" or our "2023 fiscal year" refers to our 2023 fiscal year that was a 53-week period that ended on December 31, 2023.

• Liquidity and Capital Resources : This section provides a discussion of our financial condition and an analysis of our cash flows for our 2025 fiscal year as compared to our 2024 fiscal year. This section also provides a discussion of our contractual obligations, other purchase commitments and customer credit risk that existed at December 28, 2025 and December 29, 2024, as well as a discussion of our ability to fund our future commitments and ongoing operating activities through internal and external sources of capital.

• Recently Issued Accounting Standards : This section identifies our adoption of recently issued accounting standards.

• Critical Accounting Estimates : This section identifies and summarizes those accounting policies that significantly impact our reported results of operations and financial condition and require significant judgment or estimates on the part of management in their application.

Overview

Founded over 70 years ago, we are the largest manufacturer of residential cabinets in North America. Our superior product quality, innovative design and service excellence drives a compelling value proposition. We have insight into the fashion and features consumers desire, which we use to tailor our product lines across price points. Our volume leadership allows us to achieve an advantaged cost structure and service platform by standardizing product platforms and components to the greatest extent possible—resulting in an improved facility footprint and an efficient supply chain. Further, our decades of experience have informed how we use global geographies to optimize procurement and manufacturing costs. Finally, with the most extensive dealer network throughout the United States and Canada, we have an advantaged distribution model that cannot be easily replicated. We expect to further extend our competitive advantages by using technology and data to enhance the consumer's experience from visualization to ordering to delivery and installation.

On December 14, 2022, our former parent company, Fortune Brands, completed a tax free spin-off transaction to separate its Cabinets segment into a standalone publicly-traded company. The Separation was completed through a series of transactions ending with a pro rata distribution of all of the shares of MasterBrand, Inc. common stock owned by Fortune Brands to Fortune Brands shareholders, after which we became an independent, publicly-traded company. Separating the former Cabinets segment of Fortune Brands into a standalone publicly-traded company significantly enhanced the long-term growth and return prospects of our Company and offers substantially greater long-term value to shareholders, customers and associates.

On July 10, 2024, we acquired all of the issued and outstanding limited liability interests of Dura Investment Holdings LLC, parent company of Supreme, a cabinetry company, from GHK Capital Partners LP. Supreme was a domestic manufacturer of residential cabinetry with a portfolio of product lines significantly focused on premium products. Supreme, with manufacturing facilities located in Minnesota, Iowa and North Carolina, and its two brands, Dura Supreme and Bertch cabinetry, crafts framed and frameless cabinetry for a nationwide network of dealers. The combined company is reaching more customers, through its highly complementary dealer networks, with greater efficiency and effectiveness. Through this transaction, MasterBrand broadened its portfolio of premium cabinetry in the resilient and attractive kitchen and bath categories, further diversifying its channel distribution and adding to its strategically located facility footprint. The acquisition was funded with a combination of cash on hand and proceeds from our revolving credit facility.

On August 6, 2025, we announced the execution of a definitive agreement whereby the Company will combine with American Woodmark in an all-stock transaction. Merger Sub, a direct wholly owned subsidiary of the Company, will merge with and into American Woodmark, with American Woodmark surviving the merger and continuing as a wholly owned subsidiary of the Company. The closing of the Merger, which is expected to occur in early 2026, is subject to the receipt of clearance under the Hart-Scott-Rodino Antitrust Improvements Act of 1976, as amended, and the satisfaction or waiver of other customary closing conditions. Both companies received the necessary shareholder approval at their respective special meetings of shareholders held on October 30, 2025.

In February 2026, we announced plans to implement $30 million dollars of planned cost reductions. The cost reductions, which will primarily be in selling, general and administrative expenses, will begin in the first quarter of 2026, with full realization expected by the end of fiscal 2026.

Recent Developments

Tariffs

The Company continues to actively monitor recent trade policy and tariff announcements, including the recently announced Section 232 tariffs on timber, lumber, and derivative wood products (including kitchen cabinets, vanities and related wood products), effective October 14, 2025. As a result of the Section 232 proceedings, a 10 percent tariff applies to softwood lumber and timber imports, and a 25 percent tariff applies to kitchen cabinets and vanities, although the tariff on cabinets and vanities may increase after January 1, 2027. Increased restrictions on global trade, including an increase in U.S. tariffs and any retaliatory responses thereto, have resulted in and could further result in, among other things, increased input costs, supply chain disruptions, decreased consumer demand and volatility in foreign exchange rates and financial markets. We continue to analyze the impact of these actions and adjust our mitigation strategy, including pricing, productivity and repositioning our supply chain to offset the impact of the tariff exposure as trade policy evolves. The uncertain and evolving market dynamics and global trade environment could have a material adverse effect on the Company's business, financial condition, and results of operations.

OBBBA

On July 4, 2025, the "One Big Beautiful Bill Act" ("OBBBA") was enacted into U.S. law. The OBBBA includes changes to several corporate tax provisions, including tax deductions for qualified research expenditures, changes to business interest expense limitations and bonus depreciation. The OBBBA legislation does not materially impact our 2025 annual effective tax rate, but reduced 2025 cash taxes.

Pillar Two

In 2024, certain jurisdictions in which we operate enacted, or announced their intention to enact, legislation consistent with one or more Organization for Economic Co-operation and Development Global Anti-Base Erosion Model Rules ("Pillar Two"). The model rules include qualified domestic minimum top-up taxes, income inclusion rules, and undertaxed profit rules all aimed to ensure that multinationals pay a minimum effective corporate tax rate of 15 percent in each jurisdiction in which they operate, with some rules effective in 2024, 2025 and 2026. The Pillar Two legislation, as enacted in certain jurisdictions in which we operate, does not materially impact our 2025 annual effective tax rate but is expected to unfavorably impact our annual effective tax rate in 2026.

Additionally, material changes to our separate legal entity pre-tax book income and structure, the valuation allowance, nondeductible acquisition-related transaction costs related to the American Woodmark transaction, enacted local legislation, or changes in jurisdictions in which we operate could also impact our effective tax rate in fiscal 2026.

Results of Operations

The following discussion includes a comparison of results of operations for the fifty-two weeks ended December 28, 2025 compared to the fifty-two weeks ended December 29, 2024. For comparisons of our 2024 fiscal year compared to our 2023 fiscal year, please refer to the heading "Results of Operations" in Part II, Item 7 of our Annual Report on Form 10-K for the fiscal year ended December 29, 2024, as filed with the SEC.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-13_item1_business.md)

Item 1. Business

MasterBrand, Inc. ("we," "us," "our," "MasterBrand" or the "Company"), was founded over 70 years ago in 1954 under the name United Cabinet Incorp orated. We are the largest manufacturer of residential cabinets in North America, based on 2024 reported net sales. O ur products are sold throughout the United States and Canada to the remodeling and new construction markets through three primary channels: dealers, retailers and builders.

On December 14, 2022, our former parent company, Fortune Brands Innovations, Inc. (formerly known as Fortune Brands Home & Security, Inc.) ("Fortune Brands"), completed a tax free spin-off transaction to separate its Cabinets segment into a standalone publicly-traded company (the "Separation"). The Separation was completed through a series of transactions ending with a pro rata distribution of all of the shares of MasterBrand, Inc. common stock owned by Fortune Brands to Fortune Brands shareholders, after which we became an independent, publicly-traded company.

On July 10, 2024, we acquired all of the issued and outstanding limited liability interests of Dura Investment Holdings LLC, the parent company of Supreme Cabinetry Brands, Inc. ("Supreme"), a cabinetry company. Supreme was a domestic manufacturer of residential cabinetry with a portfolio of product lines significantly focused on premium products. Supreme, with manufacturing facilities located in Minnesota, Iowa and North Carolina, and its two brands, Dura Supreme and Bertch cabinetry, crafts framed and frameless cabinetry for a nationwide network of dealers.

On August 6, 2025, we announced the execution of a definitive agreement whereby the Company will combine with American Woodmark Corporation ("American Woodmark"), a Virginia corporation, in an all-stock transaction. The Company, Maple Merger Sub, Inc. ("Merger Sub"), a Virginia corporation and direct, wholly owned subsidiary of the Company, and American Woodmark entered into an Agreement and Plan of Merger (the "Merger Agreement"), pursuant to which, and subject to the satisfaction or waiver of the conditions set forth in the Merger Agreement, Merger Sub will merge with and into American Woodmark, with American Woodmark surviving the merger and continuing as a wholly owned subsidiary of the Company (the "Merger"). The closing of the Merger, which is expected to occur in early 2026, is subject to the receipt of clearance under the Hart-Scott-Rodino Antitrust Improvements Act of 1976, as amended, and the satisfaction or waiver of other customary closing conditions. Both companies received the necessary shareholder approval at their respective special meetings of shareholders held on October 30, 2025.

Strategy

Our superior product quality, innovative design and service excellence drives a compelling value proposition. We have insight into the fashion and features consumers desire, which we use to tailor our product lines across price points. Our volume leadership allows us to achieve an advantaged cost structure and service platform by standardizing product platforms and components to the greatest extent possible—resulting in a more flexible facility footprint and an efficient supply chain. Further, our decades of experience have informed how we use global geographies to optimize procurement and manufacturing costs. Finally, with the most extensive dealer network throughout the United States and Canada, we have an advantaged distribution model that we believe cannot be easily replicated. We plan to further extend our competitive advantages by using technology and data to enhance the consumer's experience from visualization and ordering to delivery and installation.

We believe we are only beginning to unlock the potential value of our unique combination of scale, operational agility, data-first operating model and strong continuous improvement culture. We intend to continue to distinguish this advantaged platform by capitalizing on the powerful demographic trends that we expect will drive repair and remodel ("R&R") and new construction growth for years to come. We believe the combination of our leading market position and size, strategic vision, strong partnerships and commitment to continuous improvement will drive our future growth.

We seek to achieve exceptional financial performance and growth through the disciplined execution of The MasterBrand Way and our continued strategic transformation.

The MasterBrand Way

Our ever-evolving business system and center of our culture is The MasterBrand Way. Based on foundational lean tools, The MasterBrand Way enables our associates across all locations and levels of work to operate under common frameworks and a consistent lexicon to effectively develop cross-functional solutions to complex business issues. The MasterBrand Way organizes these proven lean tools around three guiding principles: The Four Basics, Continuous Improvement and Associate Engagement. Our disciplined deployment of these tools in recent years has driven our strategic transformation and improvements in commercial and operational efficiency. To derive further efficiencies, we added three incremental initiatives to The MasterBrand Way: Align to Grow, Lead Through Lean and Tech Enabled.

Align to Grow – Deliver on the unique needs of each customer

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-13_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-13_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-02-13_item7_mdna.md, 10-K_2026-02-13_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
