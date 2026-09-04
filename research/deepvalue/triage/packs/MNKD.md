# Triage pack — MNKD · MANNKIND CORP

_Generated 2026-09-04 20:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MNKD · **Name:** MANNKIND CORP
- **CIK:** 0000899460
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MNKD

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** MANNKIND CORP
- **CIK:** 899,460 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 3.96 |
| mktcap | $1.3B |
| ev | $1.5B |
| ev_ebit | 39.7x |
| fcf | $13.7M |
| fcf_yield | 1.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 15.4% |
| net_debt | $266.2M |
| net_debt_ebit | 6.9x |
| cash | $52.9M |
| ltd | $319.1M |
| equity | -$67.2M |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $349.0M |
| revenue_prior | $285.5M |
| rev_growth | 22.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $38.8M |
| net_income | $5.9M |
| cfo | $18.3M |
| capex | $4.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 4.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 321,540,637 |
| shares_py | 306,828,335 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -25.6% |
| r6m | 39.9% |
| off_52w_high | -36.2% |
| adv20 | $13.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.26 |
| r_ev_ebit | 0.18 |
| r_roic | 0.81 |
| r_rev_growth | 0.85 |
| r_buyback | 0.19 |
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
| rank | 283 |

**Screen rationale:** high ROIC 15.4%; revenue +22.2%


## 3. Share count trend

- Shares outstanding: **321,540,637** (CY2026Q2I) vs **306,828,335** prior year (CY2025Q2I)
- Change: **4.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 115,645 sh / $469,278 -> net $-469,278 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 41 (open-market buys 0, sales 3).

| code | rows |
|---|---|
| A | 6 |
| F | 22 |
| M | 10 |
| S | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'MannKind Reports Second Quarter 2026 Financial Results and Provides Bu'; skipped 8 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (mnkd-ex99_1.htm)

MannKind Reports Second Quarter 2026 Financial Results and Provides Business Update

•
Achieved three major catalysts to drive future growth:

o
Launched the pediatric indication of Afrezza ® following FDA approval

o
FUROSCIX ReadyFlow™ autoinjector approved for treatment of edema in HF and CKD

o
Positive nintedanib DPI Phase 1b data in IPF patients validates continued Phase 2 advancement

•
Encouraging early momentum in Afrezza pediatric launch

o
1 in 3 of the top 100 pediatric insulin writers have prescribed

•
Q2 2026 total revenues of $109.4M, +43% vs. Q2 2025

•
Conference call and webcast today at 4:30 p.m. ET

DANBURY, Conn. and WESTLAKE VILLAGE, Calif., August 5, 2026 (GLOBE NEWSWIRE) -- MannKind Corporation (Nasdaq: MNKD)

a biopharmaceutical company dedicated to transforming chronic disease care through innovative, patient-centric solutions for cardiometabolic and orphan lung diseases, today reported financial results for the second quarter of 2026, and provided a business update.

"This was a transformative period for MannKind, during which we delivered all three major catalysts we set out to achieve in 2026," said Michael Castagna, Chief Executive Officer of MannKind. "The two recent FDA approvals are expected to fuel our near-term growth opportunities to help patients living with diabetes, heart failure and CKD. The positive Phase 1b INFLO-1 results for MNKD-201 reduces development risk and strengthens our confidence in the ability of our platform to help people living with IPF and other fibrotic diseases. Together, these milestones validate our diversification strategy and position MannKind for sustainable growth."

Business Update and Upcoming Milestones

Commercial Products

•
Revenue from marketed products (Afrezza, Furoscix ® ) grew 27% from Q1 2026 to Q2 2026

Furoscix

•
Furoscix (furosemide injection) generated $22.2 million in net sales for Q2 2026

•
Continued growth in Integrated Delivery Networks, increasing doses purchased by 36% over Q1 2026

•
Record number of nephrology units dispensed, increasing by 67% over Q1 2026

•
Received FDA approval of Furoscix ReadyFlow™ on July 23, 2026, the first and only autoinjector delivering IV-equivalent diuretic therapy for the treatment of edema in adults with heart failure (HF) or chronic kidney disease (CKD); expected to be commercially available in late August

Afrezza

•
Afrezza (insulin human) Inhalation Powder generated $17.0 million in net sales for Q2 2026

•
Received FDA approval of Afrezza on May 29, 2026 for use in children and adolescents ages 6 and older living with diabetes

•
Awarded Breakthrough T1D grant supporting advancement of INHALE-1 ST , a pediatric trial of Afrezza in youth with newly diagnosed type 1 diabetes

Development

Nintedanib DPI (MNKD-201)

•
Topline data readout of U.S. Phase 1b INFLO-1 demonstrates safety and tolerability in IPF patients

•
Site activation and enrollment underway in the global Phase 2 INFLO-2 study

Ralinepag DPI (MNKD-1501)

•
On track for IND filing by year end

•
Received a $5 million payment from United Therapeutics (UT) to support the rapid advancement of ralinepag DPI

Corporate Update

•
Cash, cash equivalents and investments as of June 30, 2026, totaled $111 million

•
Closed $50 million private placement on July 24, 2026; proceeds will fund the $45 million CVR payment triggered by the FDA approval of Furoscix ReadyFlow

Second Quarter 2026 Financial Results

Revenues

Three Months Ended June 30,
2026 | 2025 | $ Change | % Change
Revenues | (Dollars in thousands)
Afrezza | 17,021 | 18,329 | (1,308 | (7 | %)
Furoscix | 22,191 | — | 22,191 | N/A
V-Go ® | 2,770 | 4,125 | (1,355 | (33 | %)
Collaborations and services | 35,022 | 22,845 | 12,177 | 53 | %
Royalties | 32,370 | 31,228 | 1,142 | 4 | %
Total revenues | 109,374 | 76,527 | 32,847 | 43 | %

Total revenues for the second quarter of 2026 increased compared to the same period in the prior year due to the addition of Furoscix to our product portfolio through the October 7, 2025 acquisition of scPharma, as well as increases in collaborations and services revenue, and royalties. The increase in collaborations and services revenue was primarily attributable to increased product sold to UT and revenue earned related to the development of ralinepag DPI. The increase in royalties was due to UT's increase in net revenue from sales of Tyvaso DPI.

Operating Expenses and Other Financial Highlights


Cost of goods sold – commercial, excluding amortization of acquired intangible assets, was $14.4 million for the three months ended June 30, 2026, compared to $4.6 million for the same period in 2025.


The increase is primarily attributable to the inclusion of Furoscix into our product portfolio following the acquisition of scPharma in October 2025. Gross margin percentage decreased in the current period due to the inclusion of Furoscix, which has a lower gross margin percentage than Afrezza.


Research and development expenses were $18.0 million for the three months ended June 30, 2026, compared to $13.7 million for the same period in 2025, an increase of 32%.


The increase was primarily attributable to the development of the Furoscix ReadyFlow Formulation as well as higher personnel costs following the acquisition of scPharma and increased development costs for MNKD-201, which has begun enrolling subjects. The increase was partially offset by lower clinical development expenses resulting from the discontinuation of the ICoN-1 clinical study for MNKD-101 and the completion of the Afrezza pediatric study (INHALE-1).


Selling, general and administrative expenses were $58.3 million for the three months ended June 30, 2026, compared to $31.6 million for the same period in 2025, an increase of 84%.


The increase was primarily related to costs associated with the promotion and support of Furoscix, as well as expanding our field-based teams and activities to support the launches associated with the recent approvals of the pediatric indication for Afrezza and the Furoscix ReadyFlow Autoinjector.

Six Months Ended June 30, 2026

Revenues

Six Months Ended June 30,
2026 | 2025 | $ Change | % Change
Revenues | (Dollars in thousands)
Afrezza | 32,294 | 33,216 | (922 | (3 | %)
Furoscix | 37,684 | — | 37,684 | N/A
V-Go | 5,911 | 8,211 | (2,300 | (28 | %)
Collaborations and services | 58,536 | 52,221 | 6,315 | 12 | %
Royalties | 65,119 | 61,233 | 3,886 | 6 | %
Total revenues | 199,544 | 154,881 | 44,663 | 29 | %

Total revenues for the six months ended June 30, 2026 increased compared to the same period in the prior year due to the addition of Furoscix to our product portfolio through the October 7, 2025 acquisition of scPharma, as well as increases in collaborations and services revenue, and royalties. The increase in collaborations and services revenue was primarily attributable to an increase in revenue earned related to the development of ralinepag DPI. The increase in royalties was due to UT's increase in net revenue from sales of Tyvaso DPI.

Operating Expenses and Other Financial Highlights


Cost of goods sold – commercial, excluding amortization of acquired intangible assets, was $21.9 million for the six months ended

June 30, 2026, compared to $8.4 million for the same period in 2025.


The increase is primarily attributable to the inclusion of Furoscix into our product portfolio following the acquisition of scPharma in October 2025. Gross margin percentage decreased in the current period due to the inclusion of Furoscix, which has a lower gross margin percentage than Afrezza.


Research and development expenses were $35.2 million for the six months ended June 30, 2026, compared to $24.7 million for the same period in 2025, an increase of 43%.


The increase was primarily attributable to the development of the Furoscix ReadyFlow Formulation as well as higher personnel costs following the acquisition of scPharma and increased development costs for MNKD-201, which has begun enrolling subjects. The increase was partially offset by lower clinical development expenses resulting from the discontinuation of the ICoN-1 clinical study for MNKD-101 and the completion of the Afrezza pediatric study (INHALE-1).


Selling, general and administrative expenses were $112.4 million for the six months ended June 30, 2026, compared to $56.6 million for the same period in 2025, an increase of 98%.


The increase was primarily related to costs associated with the promotion and support of Furoscix, as well as expanding our field-based teams and activities to support the launches associated with the recent approvals of the pediatric indication for Afrezza and the Furoscix ReadyFlow Autoinjector.

Conference Call and Webcast

MannKind will host a conference call and webcast to discuss these results today at 4:30 p.m. Eastern Time. The webcast will be accessible via a link on MannKind's website at https://investors.mannkindcorp.com/events-and-presentations . A replay will also be available in the same location within 24 hours after the call and accessible for approximately 90 days.

About MannKind

MannKind Corporation (Nasdaq: MNKD) is a biopharmaceutical company dedicated to transforming chronic disease care through innovative, patient-centric solutions. Focused on cardiometabolic and orphan lung diseases, we develop and commercialize treatments that address serious unmet medical needs, including diabetes, pulmonary hypertension, and fluid overload in heart failure and chronic kidney disease.

With deep expertise in drug-device combinations, MannKind aims to deliver therapies designed to fit seamlessly into daily life.

Learn more at mannkindcorp.com.

Media Relations

Christie Iacangelo

Email: media@mnkd.com

MANNKIND CORPORATION AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF OPERATIONS

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
(In thousands except per share data)
Revenues:
Commercial product sales | 41,982 | 22,454 | 75,889 | 41,427
Collaborations and services | 35,022 | 22,845 | 58,536 | 52,221
Royalties | 32,370 | 31,228 | 65,119 | 61,233
Total revenues | 109,374 | 76,527 | 199,544 | 154,881
Expenses:
Cost of goods sold – commercial, excluding amortization of acquired intangible assets | 14,409 | 4,607 | 21,917 | 8,375
Cost of revenue – collaborations and services | 15,131 | 15,961 | 25,094 | 29,709
Research and development | 18,001 | 13,675 | 35,232 | 24,697
Selling, general and administrative | 58,302 | 31,622 | 112,389 | 56,636
Amortization of acquired intangible assets | 4,367 | — | 8,734 | —
(Gain) loss on foreign currency transaction | (486 | 5,363 | (1,804 | 7,872
Total expenses | 109,724 | 71,228 | 201,562 | 127,289
(Loss) income from operations | (350 | 5,299 | (2,018 | 27,592
Other income (expense):
Interest income, net | 1,022 | 1,832 | 2,452 | 3,788
Interest expense | (11,894 | (285 | (19,372 | (4,930
Interest expense on liability for sale of future royalties | (510 | (3,473 | (3,073 | (7,050
Interest expense on financing liability | (2,414 | (2,433 | (4,807 | (4,843
Loss on settlement of debt | — | — | (917 | —
Other expense | (4,992 | — | (7,769 | —
Total other expense | (18,788 | (4,359 | (33,486 | (13,035
(Loss) income before income tax (benefit) expense | (19,138 | 940 | (35,504 | 14,557
Income tax (benefit) expense | (106 | 272 | 147 | 731
Net (loss) income | (19,032 | 668 | (35,651 | 13,826
Net (loss) income per share – basic | (0.06 | 0.00 | (0.12 | 0.05
Weighted average shares used to compute net (loss) income per share – basic | 309,191 | 304,954 | 308,732 | 304,222
Net (loss) income per share – diluted | (0.06 | 0.00 | (0.12 | 0.04
Weighted average shares used to compute net (loss) income per share – diluted | 309,191 | 311,484 | 308,732 | 312,381

MANNKIND CORPORATION AND SUBSIDIARIES CONSOLIDATED BALANCE SHEETS

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a biopharmaceutical company dedicated to transforming chronic disease care through innovative, patient-centric solutions. Focused on cardiometabolic and orphan lung diseases, we develop and commercialize treatments that address serious unmet medical needs, including diabetes, pulmonary hypertension, and fluid overload in heart failure and chronic kidney disease. With deep expertise in drug-device combinations, we aim to deliver therapies designed to fit seamlessly into daily life.

Our cardiometabolic business is currently comprised of three commercial products: Afrezza (insulin human) Inhalation Powder; Furoscix (furosemide injection); and the V-Go wearable insulin delivery device:

•
Afrezza is an ultra rapid-acting inhaled insulin indicated to improve glycemic control in adults with diabetes. Afrezza was developed by us and consists of a dry powder formulation of human insulin delivered from a small portable inhaler. Administered at the beginning of a meal, Afrezza dissolves rapidly upon inhalation to the lung and delivers insulin quickly to the bloodstream.

•
Furoscix is a novel formulation of furosemide that delivers an 80 mg dose via an on-body infusor over a five-hour period. Furoscix is indicated for the treatment of edema in pediatric patients who weigh at least 43 kg and adult patients with chronic heart failure or chronic kidney disease. Furoscix is the first FDA-approved subcutaneous loop diuretic that delivers intravenous-equivalent diuresis at home as opposed to a hospital setting. Furoscix was developed by scPharma, which we acquired in October 2025. See Note 3 - Business Combinations in the Consolidated Financial Statements included in Part II, Item 8 – Financial Statements and Supplementary Data.

•
V-Go is a mechanical basal-bolus insulin delivery system that is worn like a patch and can eliminate the need for taking multiple daily injections. V-Go administers a continuous preset basal rate of insulin over 24 hours and provides discreet on-demand bolus dosing at mealtimes. V-Go received 510(k) clearance by the FDA in 2010 and has been available commercially since 2012. In May 2022, we acquired V-Go from Zealand.

We anticipate two potential milestones for our cardiometabolic business in 2026 based on regulatory submissions that we made in 2025. The FDA is currently reviewing a sBLA pursuant to which we are seeking approval for Afrezza in children and adolescents living with type 1 or type 2 diabetes. The sBLA has been assigned a PDUFA target action date of May 29, 2026. The FDA is also reviewing a sNDA pursuant to which we are seeking approval for Furoscix ReadyFlow Autoinjector, a high-concentration formulation of furosemide that is delivered subcutaneously in under ten seconds. The sNDA has been assigned a PDUFA target action date of July 26, 2026.

In the United States, we are solely responsible for the commercialization of Afrezza, Furoscix and V-Go. Outside of the U.S., our strategy has been to establish regional partnerships in foreign jurisdictions where there are commercial opportunities, subject to the receipt of necessary foreign regulatory approvals. In December 2025, we supplied our partner in India, Cipla, with an initial shipment of Afrezza to support their launch of Afrezza in India.

The proprietary formulation and inhaler technologies used in Afrezza have also been deployed in our efforts to develop products to treat orphan lung diseases. Our first product to address an orphan lung disease, Tyvaso DPI (treprostinil) inhalation powder, received FDA approval in May 2022 for the treatment of PAH and PH-ILD. Our development and marketing partner, United Therapeutics, began commercializing Tyvaso DPI in June 2022 and is obligated to pay us a royalty on net sales of the product. We also receive revenue for the supply of Tyvaso DPI that we manufacture for UT. In August 2025, we announced the expansion of our collaboration, pursuant to which we will formulate MNKD-1501, a second investigational molecule using our proprietary technologies, and United Therapeutics will conduct preclinical and clinical development activities. Per the agreement, we received an upfront payment and are eligible to receive milestone payments upon achievement of specified development milestones as well as royalties on net sales of MNKD-1501, if approved.

The other major program in our pipeline that will potentially address an orphan lung disease is MNKD-201, a dry-powder formulation of nintedanib for the treatment of IPF. An oral dosage form of nintedanib has been available for more than a decade. However, a fairly large oral dose is required in order to achieve sufficient drug levels in lung tissue. High systemic levels of nintedanib are often associated with

undesirable side effects. Our goal with an inhaled formulation is to deliver a therapeutic amount of nintedanib to the lungs while avoiding high levels of the drug in other tissues. In 2024, we conducted a Phase 1 clinical study of MNKD-201, which met its primary objective of demonstrating positive safety results and good tolerability in healthy volunteers. We are currently conducting a Phase 1b study of MNKD-201 in the United States, top line data expected in early 2H 2026, as well as a global Phase 2 study to assess the potential safety and efficacy of this investigational product in patients with IPF, in which we expect the first patient to be enrolled in in Q2 2026.

MNKD-701 is another pipeline opportunity that we are exploring. This program is focused on bumetanide, a more potent loop diuretic than furosemide. We are currently evaluating the feasibility of formulating bumetanide as a dry-powder that can be administered via oral inhalation.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Trends and Uncertainties

Our collaboration agreement with UT entitles us to receive a 10% royalty on net sales of Tyvaso DPI, subject to our sale of a 1% royalty on future net sales to a royalty purchaser (leaving us with a 9% royalty). Our royalty revenue reflects the trend in net sales of Tyvaso DPI in the marketplace. See Note 16 – Commitments and Contingencies in the Notes to Consolidated Financial Statements included in Part II, Item 8 – Financial Statements and Supplementary Data.

Our future success is dependent on our, and our current and future collaboration partners', ability to effectively commercialize approved products. Our future success is also dependent on our pipeline of new products. There is a high rate of failure inherent in the R&D process for new drugs. As a result, there is a high risk that the funds we invest in research programs will not generate sufficient financial returns. Products may appear promising in development but fail to reach market within the expected or optimal timeframe, or at all.

Years ended December 31, 2025 and 2024

Revenues

The following table provides a comparison of the revenue categories for the years ended December 31, 2025 and 2024 (dollars in thousands):

Year Ended December 31,
2025 | 2024 | $ Change | % Change
Revenues
Commercial product sales:
Gross revenue from commercial product sales | 168,090 | 136,127 | 31,963 | 23 | %
Less: Wholesaler distribution fees, rebates and chargebacks, product returns and other discounts | 53,953 | 53,798 | 155 | 0 | %
Commercial product sales | 114,137 | 82,329 | 31,808 | 39 | %
Gross-to-net revenue adjustment percentage | 32 | % | 40 | %
Collaborations and services | 106,713 | 100,840 | 5,873 | 6 | %
Royalties | 128,116 | 102,335 | 25,781 | 25 | %
Total revenues | 348,966 | 285,504 | 63,462 | 22 | %

Afrezza — Gross revenue from sales of Afrezza increased by $10.6 million, or 11%, for the year ended December 31, 2025 compared to the prior year, primarily driven by increased price and higher demand. The gross-to-net adjustment was 32% of gross revenue, or $34.9 million, for the year ended December 31, 2025 compared to 35% of gross revenue, or $34.9 million, for the prior year. The decreased gross-to-net percentage was primarily attributable to a decrease in rebates in accordance with contractual arrangements. As a result, net revenue from sales of Afrezza increased by $10.5 million, or 16%, for the year ended December 31, 2025 compared to the prior year.

Furoscix — Gross revenue from sales of Furoscix was $32.4 million for the period from the October 7, 2025 acquisition date of scPharma to December 31, 2025. The gross to net adjustment was 28% resulting in net revenue of $23.2 million for the year ended December 31, 2025.

V-Go — Gross revenue from sales of V-Go decreased by $11.0 million, or 30%, for the year ended December 31, 2025 compared to the prior year and was primarily a result of lower demand partially offset by lower gross to net deductions. The gross-to-net adjustment was 38% of gross revenue, or $9.8 million, for the year ended December 31, 2025 compared to 51% of gross revenue, or $18.9 million, for the prior year. The improved gross-to-net percentage was primarily attributable to a decrease in rebates related to a reduction in active contracts. As a result, net revenue from sales of V-Go decreased by $1.9 million, or 10%, for the year ended December 31, 2025 compared to the prior year.

Collaborations and Services and Royalties — Net revenue from collaborations and services increased by $5.9 million, or 6%, for the year ended December 31, 2025 compared to the prior year. The increase in revenue was primarily attributable to increased manufacturing volume for product sold to UT. Royalty revenue from UT increased by $25.8 million, or 25%, for the year ended December 31, 2025 compared to the prior year due to UT's increase in net revenue from sales of Tyvaso DPI.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. B usiness

Unless the context requires otherwise, the words "MannKind," "we," "Company," "us" and "our" refer to MannKind Corporation and its subsidiaries.

We are a biopharmaceutical company dedicated to transforming chronic disease care through innovative, patient-centric solutions. Focused on cardiometabolic and orphan lung diseases, we develop and commercialize treatments that address serious unmet medical needs, including diabetes, pulmonary hypertension, and fluid overload in heart failure and chronic kidney disease. With deep expertise in drug-device combinations, we aim to deliver therapies designed to fit seamlessly into daily life.

Our cardiometabolic business is currently comprised of three commercial products: Afrezza (insulin human) Inhalation Powder; Furoscix (furosemide injection); and the V-Go wearable insulin delivery device:

•
Afrezza is an ultra rapid-acting inhaled insulin indicated to improve glycemic control in adults with diabetes. Afrezza was developed by us and consists of a dry powder formulation of human insulin delivered from a small portable inhaler. Administered at the beginning of a meal, Afrezza dissolves rapidly upon inhalation to the lung and delivers insulin quickly to the bloodstream.

•
Furoscix is a novel formulation of furosemide that delivers an 80 mg dose via an on-body infusor over a five-hour period. Furoscix is indicated for the treatment of edema in pediatric patients who weigh at least 43 kg and adult patients with chronic heart failure or chronic kidney disease. Furoscix is the first FDA-approved subcutaneous loop diuretic that delivers intravenous-equivalent diuresis at home as opposed to a hospital setting. Furoscix was developed by scPharmaceuticals Inc. ("scPharma"), which we acquired in October 2025. See Note 3 - Business Combinations in the Consolidated Financial Statements included in Part II, Item 8 – Financial Statements and Supplementary Data.

•
V-Go is a mechanical basal-bolus insulin delivery system that is worn like a patch and can eliminate the need for taking multiple daily injections. V-Go administers a continuous preset basal rate of insulin over 24 hours and provides discreet on-demand bolus dosing at mealtimes. V-Go received 510(k) clearance by the FDA in 2010 and has been available commercially since 2012. In May 2022, we acquired V-Go from Zealand Pharma A/S and Zealand Pharma US, Inc. (together "Zealand").

We anticipate two potential milestones for our cardiometabolic business in 2026 based on regulatory submissions that we made in 2025. The FDA is currently reviewing a supplemental Biologics License Application ("sBLA") pursuant to which we are seeking approval for Afrezza in children and adolescents living with type 1 or type 2 diabetes. The sBLA has been assigned a Prescription Drug User Fee Act ("PDUFA") target action date of May 29, 2026. The FDA is also reviewing a supplemental New Drug Application ("sNDA") pursuant to which we are seeking approval for Furoscix ReadyFlow Autoinjector ("ReadyFlow Formulation"), a high-concentration formulation of furosemide that is delivered subcutaneously in under ten seconds. The sNDA has been assigned a PDUFA target action date of July 26, 2026.

In the United States, we are solely responsible for the commercialization of Afrezza, Furoscix and V-Go. Outside of the U.S., our strategy has been to establish regional partnerships in foreign jurisdictions where there are commercial opportunities, subject to the receipt of necessary foreign regulatory approvals. In December 2025, we supplied our partner in India, Cipla Ltd. ("Cipla"), with an initial shipment of Afrezza to support their launch of Afrezza in India.

The proprietary formulation and inhaler technologies used in Afrezza have also been deployed in our efforts to develop products to treat orphan lung diseases. Our first product to address an orphan lung disease, Tyvaso DPI (treprostinil) inhalation powder, received FDA approval in May 2022 for the treatment of pulmonary arterial hypertension ("PAH") and pulmonary hypertension associated with interstitial lung disease ("PH-ILD"). Our development and marketing partner (sometimes referred to as our collaboration partner), United Therapeutics Corporation ("United Therapeutics" or "UT") began commercializing Tyvaso DPI in June 2022 and is obligated to pay us a royalty on net sales of the product. We also receive revenue for the supply of Tyvaso DPI that we manufacture for UT. In August 2025, we announced the expansion of our collaboration, pursuant to which we will formulate MNKD-1501, a second investigational molecule using our proprietary technologies, and United Therapeutics will conduct preclinical and clinical development activities. Per the agreement, we received an upfront payment and are eligible to receive milestone payments upon achievement of specified development milestones as well as royalties on net sales of MNKD-1501, if approved.

The other major program in our pipeline that will potentially address an orphan lung disease is MNKD-201, a dry-powder formulation of nintedanib for the treatment of idiopathic pulmonary fibrosis ("IPF"). An oral dosage form of nintedanib has been available for more than a decade. However, a fairly large oral dose is required in order to achieve sufficient drug levels in lung tissue. High systemic levels of nintedanib are often associated with undesirable side effects. Our goal with an inhaled formulation is to deliver a therapeutic amount of nintedanib to the lungs while avoiding high levels of the drug in other tissues. In 2024, we conducted a Phase 1 clinical study of MNKD-201, which met its primary objective of demonstrating positive safety results and good tolerability in healthy volunteers. We are currently conducting a Phase 1b

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-05_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
