# Triage pack — CERS · CERUS CORP

_Generated 2026-09-05 00:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CERS · **Name:** CERUS CORP
- **CIK:** 0001020214
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CERS

**Fetcher warnings for this ticker:** 10-K 2026-03-02: heading split missed Item 7 - MD&A

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** CERUS CORP
- **CIK:** 1,020,214 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:SecuredLongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 2.57 |
| mktcap | $517.9M |
| ev | $534.8M |
| ev_ebit | n/a |
| fcf | $1.1M |
| fcf_yield | 0.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -7.9% |
| net_debt | $16.8M |
| net_debt_ebit | n/a |
| cash | $18.0M |
| ltd | $34.8M |
| equity | $70.0M |
| ltd_tag | SecuredLongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $233.8M |
| revenue_prior | $201.3M |
| rev_growth | 16.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$8.7M |
| net_income | -$15.6M |
| cfo | $4.8M |
| capex | $3.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 5.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 201,524,898 |
| shares_py | 191,698,794 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 73.3% |
| r6m | 26.0% |
| off_52w_high | -21.6% |
| adv20 | $5.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.21 |
| r_ev_ebit | 0.00 |
| r_roic | 0.15 |
| r_rev_growth | 0.78 |
| r_buyback | 0.18 |
| score | 0.32 |

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
| rank | 394 |

**Screen rationale:** revenue +16.1%; 12-1 momentum 73.3%


## 3. Share count trend

- Shares outstanding: **201,524,898** (CY2026Q2I) vs **191,698,794** prior year (CY2025Q2I)
- Change: **5.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-10** — Item 5.02 (officer / director change or comp arrangement): As previously disclosed, William "Obi" Greenman, former President and Chief Executive Officer and Chairman of the Board of Directors (the "Board") of Cerus Corporation (the "Company"), ceased serving as President and Chief Executive Officer and began serving...
- **2026-06-08** — Item 1.01 (Entry into a Material Definitive Agreement): On June 5, 2026, (the "Closing Date"), Cerus Corporation (the "Company") entered into (i) a Second Amended and Restated Credit, Security and Guaranty Agreement (Term Loan) (the "Term Loan Credit Agreement"), by and among the Company, the lenders party thereto...
- **2026-06-08** — Item 1.02 (Termination of a Material Definitive Agreement): The information in Item 1.01 above with respect to the Company's existing indebtedness under the Existing Term Loan Credit Agreement and the Existing Revolving Loan Credit Agreement is incorporated by reference into this Item 1.02.
- **2026-06-03** — Item 5.02 (officer / director change or comp arrangement): (e) On June 2, 2026, the stockholders of Cerus Corporation (the "Company") approved an amendment and restatement of the Company's 2024 Equity Incentive Plan (the "2024 Equity Incentive Plan").
- **2026-04-21** — Item 5.02 (officer / director change or comp arrangement): On April 17, 2026, the board of directors (the "Board") of Cerus Corporation (the "Company"), upon the recommendation of its compensation committee, adopted a new severance plan (the "Severance Plan") and the Company subsequently entered into individual...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 286,070 sh / $840,674 -> net $-840,674 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 0, sales 8).

| code | rows |
|---|---|
| A | 10 |
| S | 8 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Total Revenue of $63.3 million; Second Quarter 202'; skipped 9 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (cers-ex99_1.htm)

Second Quarter 2026 Total Revenue of $63.3 million; Second Quarter 2026 Product Revenue of $57.4 million, +10% Y/Y

Raising Lower End of 2026 Product Revenue Guidance: Range now $229 to $231 million;

Raising 2026 IFC Sales Outlook to $23 to $25 million, up approximately 40% to 50% Y/Y

CONCORD, CA, July 30, 2026 - Cerus Corporation (Nasdaq: CERS) announced today financial results for the second quarter ended June 30, 2026, and provided a business update.

"This quarter we made significant progress in expanding patient access to safer blood components around the globe," said Vivek Jayaraman, Cerus' president and chief executive officer. "I'm particularly pleased with the performance of our INTERCEPT Fibrinogen Complex (IFC) franchise in the U.S. The value proposition for blood centers, hospitals and clinicians is resonating and leading to earlier patient access to fibrinogen across the country. We view IFC as a compelling growth driver for Cerus."

Additional highlights include:

•
Second-quarter 2026 total revenue comprised of (in millions, except percentages):

Three Months Ended | Six Months Ended
June 30, | Change | June 30, | Change
2026 | 2025 | % | 2026 | 2025 | %
Product Revenue | 57.4 | 52.4 | 5.0 | 10 | % | 111.1 | 95.7 | 15.4 | 16 | %
Government Contract Revenue | 5.9 | 7.7 | (1.8 | -24 | % | 12.1 | 13.3 | (1.2 | -9 | %
Total Revenue | 63.3 | 60.1 | 3.2 | 5 | % | 123.2 | 109.0 | 14.2 | 13 | %
Numbers may not sum due to rounding. Percentages calculated from unrounded figures.

•
Demand for IFC continued to increase, with second quarter volumes - including kits and finished therapeutic doses (measured in FC15* equivalent units) – up approximately 20% compared to the prior year period. Second quarter U.S. IFC sales totaled $6.7 million, up from $5.6 million in the prior year period.

•
Submitted PMA for the INTERCEPT Blood System for Platelets with INT200 Illuminator, the Company's next generation LED-based illumination device, to the FDA as planned. Given review timelines, a regulatory decision is anticipated in early 2027.

•
Completed debt refinancing, including a $30 million reduction in the outstanding term loan funded with $20 million of cash on hand and $10 million drawn under the new, lower-cost revolving credit facility.

•
Expanded the Company's ongoing collaboration with the Biomedical Advanced Research and Development Authority, or BARDA, to further advance the development of the INTERCEPT Red Blood Cell system, increasing the total potential value of the 2024 contract by $21.9 million from $248.6 million to $270.5 million. The BARDA contract is funded in whole or in part with federal funds from the Department of Health and Human Services' Administration for Strategic Preparedness and Response, Biomedical Advanced Research and Development Authority under Contract No. 75A50124C00046.

•
Cash, cash equivalents, and short-term investments were $56.3 million at June 30, 2026.

Revenue

Product revenue for the second quarter of 2026 was $57.4 million, compared to $52.4 million for the prior year period, representing year-over-year growth of 10%. Second quarter growth was driven by increases across all product categories.

Government contract revenue for the second quarter of 2026 was $5.9 million, compared to $7.7 million during the prior year period. The decrease reflects the completion of the Company's FDA contract in 2025, the wind-down of the BARDA 2016 contract, and timing of expenses related to the BARDA 2024 contract.

Product Gross Profit & Margin

Product gross profit for the second quarter of 2026 was $29.5 million, compared to $29.0 million, increasing by 2% over the prior year period. Product gross margin for the second quarter was 51.4% compared to 55.2% in the same period last year. The year-over-year decrease in gross margin was largely driven by a weaker U.S. dollar relative to the Euro and higher product costs driven by inflationary pressures.

Operating Expenses

Total operating expenses for the second quarter of 2026 were $37.3 million, compared to $40.1 million for the same period of the prior year, reflecting a year-over-year decrease of 7%.

R&D expenses for the second quarter of 2026 were $14.4 million, compared to $18.9 million in the second quarter of 2025. The primary contributors to lower R&D expenses were decreased development costs on the INT200, with the U.S. PMA submission completed, as well as lower development costs tied to government-funded projects, as reflected in the government contract revenue.

SG&A expenses totaled $22.9 million for the second quarter of 2026, compared to $21.2 million for the second quarter of 2025. The year-over-year increase in SG&A expenses was due to higher costs across various functions.

Net Loss Attributable to Cerus Corporation

Net loss attributable to Cerus Corporation for the second quarter of 2026 was $2.9 million, or $0.01 per basic and diluted share, compared to a net loss attributable to Cerus Corporation of $5.7 million, of $0.03 per basic and diluted share, for the same period of the prior year. Net loss attributable to Cerus Corporation for the first half of 2026 was $4.6 million, compared to a net loss attributable to Cerus Corporation of $13.4 million for the first half of 2025.

Non-GAAP Adjusted EBITDA

Non-GAAP adjusted EBITDA for the second quarter of 2026 was positive $3.0 million, compared to non-GAAP adjusted EBITDA of positive $0.9 million for the same period of the prior year. Non-GAAP adjusted EBITDA for the first half of 2026 was a positive $7.0 million compared to non-GAAP adjusted EBITDA of positive $1.1 for the first half of 2025.

Balance Sheet and Cash Flows

At June 30, 2026, the Company had cash, cash equivalents, and short-term investments of $56.3 million, compared to $82.9 million at December 31, 2025.

As of June 30, 2026, the Company had $35.0 million outstanding on its term loan and $30.1 million drawn on its revolving credit facility. The Company's revolving line of credit allows for an additional $14.9 million as of June 30, 2026, which is dependent on eligible assets supporting the borrowing base.

For the second quarter of 2026, cash used in operations totaled $2.7 million compared to $2.4 million used during the same period of the prior year. Cash use in operations in the second quarter of 2026 was tied to an increase in working capital, namely inventory in support of the expected growth.

Narrowing And Raising Low End of 2026 Product Revenue Guidance

The Company now expects full-year 2026 product revenue to be in the range of $229 million to $231 million, reflecting growth of 11% to 12% from 2025. Included in this range is increased full-year 2026 IFC revenue guidance of $23 million to $25 million. Previously, the Company's 2026 product revenue guidance range was $227 million to $231 million, including IFC revenue guidance between $22 million to $24 million.

Quarterly Conference Call

The Company will host a conference call at 4:30 P.M. ET this afternoon, during which management will discuss the Company's financial results and provide a general business overview and outlook. To listen to the live webcast, please visit the Investor Relations page of the Cerus website at http://www.cerus.com/ir.

A replay will be available on Cerus' website and will be available approximately three hours after the call through August 20, 2026.

*FC15 equivalent to a therapeutic dose of a cryoAHF pool.

ABOUT CERUS

Cerus Corporation is dedicated solely to safeguarding the world's blood supply and aims to become the preeminent global blood products company. Headquartered in Concord, California, the company develops and supplies vital technologies and pathogen-protected blood components to blood centers, hospitals, and ultimately patients who rely on safe blood. The INTERCEPT Blood System for platelets and plasma is available globally and remains the only pathogen reduction system with both CE mark and FDA approval for these two blood components. In the U.S., the INTERCEPT Blood System for Cryoprecipitation is approved for the production of Pathogen Reduced Cryoprecipitated Fibrinogen Complex (commonly referred to as INTERCEPT Fibrinogen Complex), a therapeutic product for the treatment and control of bleeding, including massive hemorrhage, associated with fibrinogen deficiency. The INTERCEPT red blood cell system is under regulatory review in Europe, and in late-stage clinical development in the U.S. For more information about Cerus, visit www.cerus.com and follow us on LinkedIn.

Cerus, INTERCEPT, and the Cerus logo are trademarks of Cerus Corporation.

ir@cerus.com

925-288-6128

Supplemental Tables

Three Months Ended | Six Months Ended
June 30, | June 30,
2026 vs. 2025 | 2026 vs. 2025
Platelet Kit Growth
North America | 2% | 4%
International | -3% | 9%
Worldwide | 1% | 5%
Change in Calculated Number of Treatable Platelet Doses
North America | 4% | 6%
International | -9% | 6%
Worldwide | 0% | 6%
Dose treatable calculation based on the number of kits sold and the product configuration (single and double dose kits)

Three Months Ended | Six Months Ended
June 30, | June 30,
2026 vs. 2025 | 2026 vs. 2025
Total IFC* Demand Growth | ~20% | ~50%
(including kits and finished therapeutic doses)
*FC15 equivalent to a therapeutic dose of a cryoAHF pool.

CERUS CORPORATION
REVENUE BY REGION
(in thousands, except percentages)
Three Months Ended | Six Months Ended
June 30, | Change | June 30, | Change
2026 | 2025 | % | 2026 | 2025 | %
North America | 38,356 | 35,286 | 3,070 | 9 | % | 75,111 | 65,886 | 9,225 | 14 | %
Europe, Middle East and Africa | 18,336 | 16,612 | 1,724 | 10 | % | 34,014 | 28,824 | 5,190 | 18 | %
Other | 749 | 547 | 202 | 37 | % | 1,977 | 974 | 1,003 | 103 | %
Total product revenue | 57,441 | 52,445 | 4,996 | 10 | % | 111,102 | 95,684 | 15,418 | 16 | %

CERUS CORPORATION
CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS
UNAUDITED
(in thousands, except per share data)
Three Months Ended | Six Months Ended
June 30, | June 30,
2026 | 2025 | 2026 | 2025
Product revenue | 57,441 | 52,445 | 111,102 | 95,684
Cost of product revenue | 27,909 | 23,470 | 53,676 | 41,285
Gross profit on product revenue | 29,532 | 28,975 | 57,426 | 54,399
Government contract revenue | 5,862 | 7,684 | 12,094 | 13,298
Operating expenses:
Research and development | 14,388 | 18,900 | 28,920 | 35,505
Selling, general and administrative | 22,864 | 21,182 | 42,812 | 41,468
Total operating expenses | 37,252 | 40,082 | 71,732 | 76,973
Loss from operations | (1,858 | (3,423 | (2,212 | (9,276
Total non-operating expense, net | (1,029 | (2,216 | (2,232 | (4,007
Loss before income taxes | (2,887 | (5,639 | (4,444 | (13,283
Provision for income tax | 95 | 76 | 186 | 150
Net loss | (2,982 | (5,715 | (4,630 | (13,433
Net loss attributable to noncontrolling interest | (42 | (8 | (50 | (9
Net loss attributable to Cerus Corporation | (2,940 | (5,707 | (4,580 | (13,424
Net loss per share attributable to Cerus Corporation
Basic and diluted | (0.01 | (0.03 | (0.02 | (0.07
Weighted average shares outstanding:
Basic and diluted | 200,565 | 191,301 | 197,371 | 189,195

_[...truncated at ~12,000 chars of this document]_

## 8. MD&A — no 10-K Item 7 fetched, using 10-Q MD&A (10-Q_2026-07-30_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Since our inception in 1991, we have devoted substantially all of our efforts and resources to the research, development, clinical testing and commercialization of the INTERCEPT Blood System. Our INTERCEPT Blood System is intended for use with blood components and certain of their derivatives: plasma, platelets, red blood cells and to produce INTERCEPT Fibrinogen Complex, or IFC, and pathogen reduced plasma, cryoprecipitate reduced. The INTERCEPT Blood System for platelets, or platelet system, and the INTERCEPT Blood System for plasma, or plasma system, have received a broad range of regulatory approvals and certifications, and are being marketed and sold in a number of countries around the world, including the U.S., certain countries in Europe, the Commonwealth of Independent States, or CIS, the Middle East, and Latin America and selected countries in other regions of the world. Additionally, we have received FDA approval for the INTERCEPT Blood System for Cryoprecipitation which uses our plasma system to produce IFC for the treatment and control of bleeding, including massive hemorrhage, associated with fibrinogen deficiency. In addition, the INTERCEPT Blood System for Cryoprecipitation is used to produce pathogen reduced plasma, cryoprecipitate reduced. We currently sell the platelet and plasma systems using our direct sales force and through distributors and we sell IFC or disposable kits to manufacture IFC in the U.S. using our direct sales force.

The platelet system is approved by the FDA in the U.S. for ex vivo preparation of pathogen-reduced apheresis platelet components collected and stored in 100% plasma or InterSol in order to reduce the risk of transfusion-transmitted infection, or TTI, including sepsis, and as an alternative to gamma irradiation for prevention of transfusion-associated graft versus host disease or TA-GVHD. The plasma system is approved by the FDA in the U.S. for ex vivo preparation of pathogen-reduced, whole blood derived or apheresis plasma in order to reduce the risk of TTI when treating patients requiring therapeutic plasma transfusion, and as an alternative to gamma irradiation for prevention of TA-GVHD. Outside of the U.S., we have received CE Certificates of Conformity issued by our Notified Body in accordance with the European Union Medical Devices Regulation 2017/745, or MDR, for the platelet system and the plasma system and affixed the CE Mark to these products.

The INTERCEPT Blood System for red blood cells, or the red blood cell system, is currently in development and has not been commercialized anywhere in the world. We filed our application for conformity assessment to obtain a CE Certificate of Conformity to affix the CE Mark to the red blood cell system in December 2018 under the Medical Device Directive 93/42/EEC, or MDD, and in June 2021, we completed the resubmission of our application under the MDR. In October 2024, we announced that TÜV-SÜD, our Notified Body for the red blood cell system, in consultation with the Dutch Medicines Evaluation Board, or CBG, the Competent Authority for the red blood cell system, reviewed information regarding the medicinal product or active pharmaceutical ingredient of our MDR application and concluded that the data provided were insufficient to support the proposed classification of the impurity profile of the final product, necessitating the closure of our MDR application without successful completion of the conformity assessment and issuance

of a CE Certificate of Conformity. In collaboration with TÜV-SÜD, we developed a plan for resubmission of our application and identified a new Competent Authority. We revised our MDR application to address the questions raised by CBG and submitted a new MDR application for the red blood cell system to TÜV-SÜD. In July 2025, we announced that TÜV-SÜD completed their clinical assessment of our new MDR application and transferred information regarding the active substances, or API, to the identified competent authority, the State Institute for Drug Control, or SÚKL. After discussions with TÜV-SÜD, we decided to transfer the review of the API from SÚKL to the French National Agency for Medicines and Health Products Safety, or ANSM. We cannot predict if or when a decision concerning certification would occur. In addition, as a result of the resubmission of our MDR application, our product development costs will be ongoing. See also the risk factor entitled "The red blood cell system is currently in development and may never receive any marketing approvals or CE Certificates of Conformity" under "Item 1A— Risk Factors " of this Quarterly Report on Form 10-Q. In 2017, we initiated a Phase 3 clinical, double-blind study in the U.S., known as the RedeS study, to assess the safety and efficacy of INTERCEPT-treated red blood cells when compared to conventional, red blood cells. In addition, in the first quarter of 2024, we announced positive topline results from a Phase 3 clinical trial in the U.S., known as the ReCePI study, that was designed to evaluate the efficacy and safety of INTERCEPT-treated red blood cells in patients requiring transfusion for acute blood loss during surgery. We announced that the ReCePI study met its primary efficacy endpoint, demonstrating non-inferiority for INTERCEPT RBCs compared to conventional RBCs as measured by the incidence of acute kidney injury (AKI) following transfusion of study RBCs. We continue to believe that we will need to conduct, complete and generate acceptable data from an additional Phase 3 clinical trial in chronic anemia patients in the U.S., in vitro studies, and other necessary activities before the FDA will consider our red blood cell system for potential approval.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Three and six months ended June 30, 2026 and 2025

Revenue

Three Months Ended | Six Months Ended
June 30, | June 30,
(in thousands, except percentages) | 2026 | 2025 | Change | 2026 | 2025 | Change
Product revenue | 57,441 | 52,445 | 4,996 | 10 | % | 111,102 | 95,684 | 15,418 | 16 | %
Government contract revenue | 5,862 | 7,684 | (1,822 | (24 | %) | 12,094 | 13,298 | (1,204 | (9 | %)
Total revenue | 63,303 | 60,129 | 3,174 | 5 | % | 123,196 | 108,982 | 14,214 | 13 | %

Product revenue increased during the three and six months ended June 30, 2026, compared to the three and six months ended June 30, 2025. The increase in product revenue during the three months ended June 30, 2026 was primarily due to sales volume growth in disposable platelet and plasma kit sales and IFC sales to U.S. customers. The increase in product revenue during the six months ended June 30, 2026 was primarily due to sales volume growth in disposable platelet kits sales and IFC sales to U.S. customers. We expect product revenue for INTERCEPT disposable kits to increase in future periods driven by growth in our global platelet and plasma business and U.S. IFC business, due in part to increased market acceptance of the INTERCEPT Blood System and adoption of the INTERCEPT Blood System in geographies where commercialization efforts are underway.

Government contract revenue decreased during the three and six months ended June 30, 2026, compared to the three and six months ended June 30, 2025, primarily due to the completion of our FDA agreement in September 2025, decreased activities under the 2024 BARDA Agreement relative to the same period last year, and decreased activities under the 2016 BARDA Agreement. We anticipate that government contract revenue will increase in future periods as multiple contracts are active and as activities supporting those contracts ramp up.

Cost of Product Revenue

Our cost of product revenue consists of the cost of the INTERCEPT Blood System sold, provisions for obsolete, slow-moving and unsaleable product, certain order fulfillment costs, to the extent applicable and costs for idle facilities. Inventory is accounted for on a first-in, first-out basis.

Three Months Ended | Six Months Ended
June 30, | June 30,
(in thousands, except percentages) | 2026 | 2025 | Change | 2026 | 2025 | Change
Cost of product revenue | 27,909 | 23,470 | 4,439 | 19 | % | 53,676 | 41,285 | 12,391 | 30 | %

Cost of product revenue increased during the three and six months ended June 30, 2026 compared to the three and six months ended June 30, 2025, primarily due to the increase in product revenue compared to the same period, tariffs, and higher freight charges.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-02_item1_business.md)

Item 1. B usiness

Overview

We are a biomedical products company focused on developing and commercializing the INTERCEPT Blood System to enhance blood safety. The INTERCEPT Blood System, which is based on our proprietary technology for controlling biological replication, is designed to reduce blood-borne pathogens in donated blood components intended for transfusion.

Our INTERCEPT Blood System is intended for use with blood components and certain of their derivatives: platelets, plasma, red blood cells and to produce INTERCEPT Fibrinogen Complex, or IFC, and pathogen reduced plasma, cryoprecipitate reduced. The INTERCEPT Blood System for platelets, or platelet system, and the INTERCEPT Blood System for plasma, or plasma system, have received a broad range of regulatory approvals and certification, including but not limited to FDA approval in the U.S., CE Certificates of Conformity delivered in accordance with the Medical Devices Regulation 2017/745, or MDR, permitting us to affix the CE Mark to our products and place them on the market in the European Union and other jurisdictions that recognize the CE Mark, and are being marketed and sold in a number of countries around the world, including the U.S., certain countries in Europe, the Commonwealth of Independent States, or CIS, the Middle East, and Latin America and selected countries in other regions of the world. Additionally, we have received FDA approval for the INTERCEPT Blood System for Cryoprecipitation. The INTERCEPT Blood System for Cryoprecipitation uses our plasma system to produce IFC for the treatment and control of bleeding, including massive hemorrhage, associated with fibrinogen deficiency. In addition, the INTERCEPT Blood System for Cryoprecipitation is used to produce pathogen reduced plasma, cryoprecipitate reduced. We currently sell the platelet and plasma systems using our direct sales force and through distributors and sell IFC or disposable kits to manufacture IFC in the U.S. using our direct sales force. If we are unable to gain or maintain widespread commercial adoption in markets where our blood safety products are approved for commercialization, including in the U.S., we will have difficulties achieving and maintaining profitability.

The INTERCEPT Blood System for red blood cells, or the red blood cell system, is currently in development and has not been commercialized anywhere in the world. We are currently conducting a Phase 3 clinical trial - the RedeS study, to assess the safety and efficacy of INTERCEPT-treated red blood cells when compared to conventional, un-treated, red blood cells. With respect to our application for conformity assessment under the MDR to obtain a CE Certificate of Conformity and affix the CE Mark, or MDR application, in the European Union, or EU, we announced in October 2024 that the Dutch Medicines Evaluation Board, or CBG, the Competent Authority for the red blood cell system, reviewed the active pharmaceutical ingredient module of our MDR application and concluded that the data included in the module were insufficient to support the proposed classification of the impurity profile of the final product, necessitating the closure of our MDR application without successful completion of the conformity assessment or issuance of a CE Certificate of Conformity. In collaboration with TÜV-SÜD, our Notified Body for the red blood cell system, we developed a plan for resubmission of our application and identified a new Competent Authority. We revised our MDR application to address the questions raised by CBG and submitted a new MDR application for the red blood cell system to TÜV-SÜD. In July 2025, we announced that TÜV-SÜD completed their clinical assessment of our new MDR application and transferred information regarding the active substances, or API, to the identified competent authority, the State Institute for Drug Control, or SÚKL. After discussions with TÜV-SÜD, we decided to transfer the review of the API from SÚKL to the French National Agency for Medicines and Health Products Safety, or ANSM. We cannot predict if or when a decision concerning certification would occur. In addition, as a result of the failure to obtain a CE Certificate of Conformity following MDR application, our product development costs will be ongoing. See also the risk factor entitled "The red blood system is currently in development and may never receive any marketing approvals or CE Certificates of Conformity" under "Item 1A— Risk Factors " of this Annual Report on Form 10-K.

In order to successfully commercialize all of our products and product candidates, we will be required to conduct significant research, development, preclinical and clinical evaluation, commercialization and regulatory compliance activities for our products and product candidates, which, together with selling, general and administrative expenses, may result in operating losses. While our goal is to achieve and maintain a profitable level of operations, we may be unable to do so.

We were incorporated in California in 1991 and reincorporated in Delaware in 1996. Our wholly-owned subsidiary, Cerus Europe B.V., was formed in the Netherlands in 2006. Information regarding our revenues, net losses, and total assets for the last three fiscal years can be found in the consolidated financial statements and related notes found elsewhere in this Annual Report on Form 10-K.

Product Development

Background

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-02_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | **MISSING** |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-02_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-30_2-02-results.md, 10-Q_2026-07-30_mdna.md (10-Q MD&A used in place of the 10-K), 10-K_2026-03-02_item1_business.md

**Missing:** 10-K Item 7 MD&A (substituted 10-Q MD&A), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
