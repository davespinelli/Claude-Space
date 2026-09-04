# Triage pack — AKBA · Akebia Therapeutics, Inc.

_Generated 2026-09-04 14:00 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** AKBA · **Name:** Akebia Therapeutics, Inc.
- **CIK:** 0001517022
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/AKBA

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Akebia Therapeutics, Inc.
- **CIK:** 1,517,022 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 0.98 |
| mktcap | $272.4M |
| ev | $141.6M |
| ev_ebit | 6.0x |
| fcf | $67.7M |
| fcf_yield | 24.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$130.8M |
| net_debt_ebit | -5.6x |
| cash | $155.5M |
| ltd | $24.8M |
| equity | $25.0M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $236.2M |
| revenue_prior | $160.2M |
| rev_growth | 47.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $23.5M |
| net_income | -$5.3M |
| cfo | $68.0M |
| capex | $291k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 4.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 277,106,245 |
| shares_py | 265,145,038 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -58.7% |
| r6m | -17.4% |
| off_52w_high | -69.0% |
| adv20 | $8.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.92 |
| r_ev_ebit | 0.91 |
| r_roic | 0.50 |
| r_rev_growth | 0.94 |
| r_buyback | 0.20 |
| score | 0.69 |

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
| rank | 63 |

**Screen rationale:** top-quartile FCF yield 24.9%; cheap at 6.0x EV/EBIT; revenue +47.5%; net cash


## 3. Share count trend

- Shares outstanding: **277,106,245** (CY2026Q2I) vs **265,145,038** prior year (CY2025Q2I)
- Change: **4.5%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 5 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 69,270 sh / $86,588 vs sells 190,372 sh / $248,932 -> net $-162,344 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: Butler John P. bought 69,270 sh @ $1.25 ($86,588) on 2026-03-04.

Form 4 filings parsed: 12; transaction rows: 21 (open-market buys 1, sales 5).

| code | rows |
|---|---|
| A | 13 |
| M | 2 |
| P | 1 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-05_2-02-results.md)

_Extraction: started at the first release heading, 'Akebia Therapeutics Reports Second Quarter 2026 Financial Results and '; skipped 9 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q22026pr.htm)

Akebia Therapeutics Reports Second Quarter 2026 Financial Results and Business Highlights

Q2 2026 Vafseo® (vadadustat) net product revenues grew to $21.3 million; more than 10,500 p atients now on therapy

Advancement of rare kidney disease pipeline continues with initiation of Phase 2 open-label basket trial evaluating ebribafusp for treatment of IgA nephropathy, lupus nephritis and C3 glomerulopathy; initial data expected in 2027

Interim analysis of VOICE trial demonstrated overwhelming statistical evidence of improved safety outcomes for patients treated with Vafseo versus an ESA

Akebia to host conference call at 4:30 p.m. EDT on August 5, 2026

CAMBRIDGE, Mass.—August 5, 2026—Akebia Therapeutics®, Inc. (Nasdaq: AKBA), a biopharmaceutical company with the purpose to better the lives of people impacted by kidney disease, today reported financial results for the second quarter ended June 30, 2026 and shared recent business highlights related to the commercial launch of Vafseo® (vadadustat) and its advancing rare kidney disease pipeline.

"We're pleased with Vafseo's continued sequential revenue growth this quarter, as well as the recently announced positive VOICE trial results for the primary endpoint, which marks an important step in our ultimate goal of making Vafseo standard of care for the treatment of anemia in patients on dialysis," said John P. Butler, Chief Executive Officer of Akebia. "We also continue to make strong progress advancing our rare kidney disease pipeline with the initiation of our Phase 2 basket trial evaluating ebribafusp for the treatment of three rare glomerular kidney diseases, with initial data expected in 2027. Further, enrollment continues in our Phase 2 trial of praliciguat in FSGS."

Second Quarter and Recent Business Highlights:

• Vafseo net product revenues grew to $21.3 million in Q2, representing a 34% increase over Q1 of this year. More than 10,500 patients were active on Vafseo in Q2, representing a 41% increase from the end of Q1 2026. Total number of prescribers increased to approximately 1,200, representing an increase of approximately 17% versus Q1 2026.

• In August, Akebia announced that it initiated a Phase 2 open-label basket trial of ebribafusp (previously known as AKB-097 and ADX-097), a next-generation complement inhibitor. The trial of ebribafusp in patients with IgA nephropathy, lupus nephritis or C3 glomerulopathy is expected to enroll up to 30 patients dosed subcutaneously once weekly. As part of this study, Akebia will measure urine protein creatinine ratio (UPCR), kidney function measured by estimated glomerular filtration rate (eGFR), and ebribafusp pharmacokinetics. In addition, the trial will measure blood and urine complement biomarkers to determine if ebribafusp reduces complement activity in kidneys while avoiding complement system inhibition in the blood. The Phase 2 basket trial is open-label, and Akebia expects to report initial data in 2027.

• In June, U.S. Renal Care (USRC) and Akebia announced that a planned interim analysis of the VOICE trial (n=2,116) met its predefined stopping criteria. The data showed a statistically significant improved safety outcome in patients treated with Vafseo dosed three times per week (TIW) versus erythropoiesis stimulating agents (ESA) on the hierarchical composite endpoint of all-cause mortality and hospitalization (win odds 1.16; 95% CI 1.06, 1.28; p=0.0016), driven by a significant reduction in hospitalizations. The trial results replicated the safety outcomes from the post-hoc win statistics analysis of the Phase 3 INNO 2 VATE clinical trial. USRC expects to submit the data for presentation at an upcoming medical meeting.

Exhibit 99.1

• In June, Akebia announced it had strengthened its Vafseo intellectual property portfolio with a new Orange Book–listed patent (U.S. Patent No. 12,569,474, expiring June 2034) and eligibility for a five-year patent term extension on a composition of matter patent, which would extend that patent's term to mid-2032. Akebia's Vafseo portfolio now includes 14 Orange Book–listed patents, with expiration dates out to 2036.

• In May, Akebia announced the publication of a post-hoc win odds statistics analysis of all-cause mortality and hospitalization from its global Phase 3 INNO 2 VATE program in the Journal of the American Society of Nephrology, which demonstrated a statistically significant improvement relative to the ESA, darbepoetin alfa, on a hierarchical composite endpoint of all-cause mortality and hospitalization in patients with anemia due to chronic kidney disease receiving dialysis.

• In April, Akebia appointed Philip J. Vickers, Ph.D. to its Board of Directors. Dr. Vickers is the President and Chief Executive Officer and a member of the Board of Directors of Solu Therapeutics. He brings deep expertise spanning research and development, translational science and corporate strategy across a broad range of therapeutic areas to the Board.

Financial Results

• Revenues: Total revenues were $49.1 million in the second quarter of 2026 compared to $62.5 million in the second quarter of 2025. This decrease was due to a decrease in Auryxia® (ferric citrate) revenues which was partially offset by higher Vafseo revenues.

▪ Vafseo net product revenues were $21.3 million in the second quarter of 2026 compared to $13.3 million in the second quarter of 2025.

▪ Auryxia net product revenues were $25.5 million in the second quarter of 2026 compared to $47.2 million in the second quarter of 2025. We continue to expect Auryxia revenues to decrease in 2026 as compared to 2025 due to generic competition and pricing pressure.

▪ License, collaboration and other revenues were $2.4 million in the second quarter of 2026 compared to $2.0 million in the second quarter of 2025.

• Cost of Goods Sold (COGS): Cost of goods sold was $10.4 million in the second quarter of 2026 compared to $9.9 million in the second quarter of 2025. Of note, Vafseo-related COGS in both periods was derived from pre-launch inventory, which does not include the full cost of manufacturing as a portion of those inventory-related expenses were recorded as research and development expenses in the period incurred prior to Vafseo's approval in the U.S.

• Research & Development Expenses: Research and development expenses were $14.1 million in the second quarter of 2026 compared to $11.0 million in the second quarter of 2025. The increase in expenses was driven by increased clinical trial activities related to our mid-stage pipeline assets, which include praliciguat and ebribafusp, as well as higher headcount-related costs.

• SG&A Expenses: Selling, general and administrative expenses were $28.2 million in the second quarter of 2026 compared to $26.6 million in the second quarter of 2025. This increase was driven by higher commercialization-related activities.

• Net Income (Loss): Net loss was $8.9 million in the second quarter of 2026 compared to net income of $0.2 million in the second quarter of 2025. The change to a net loss in the second quarter of 2026 resulted from lower revenues and higher expenses during the quarter, including a $1.9 million restructuring expense related to the reorganization of our commercial organization aimed at increasing the efficiency and effectiveness of our commercial efforts.

• Cash Position: Cash and cash equivalents as of June 30, 2026 were approximately $155.5 million as compared to $162.6 million as of March 31, 2026. We believe our existing cash resources and the cash we expect to generate from product, royalty, supply and license revenues, along with

Exhibit 99.1

our plan to refinance our senior secured term loan facility, will enable us to fund our current operating plan for at least two years.

Conference Call

Akebia will host a conference call on Wednesday, August 5, 2026 at 4:30 p.m. EDT to discuss second quarter 2026 earnings. To access the call, please dial (646) 307-1963 or toll-free (800) 715-9871 and enter passcode: 4727037. To avoid delays and ensure timely connection, we encourage dialing into the conference call 15 minutes ahead of the scheduled start time.

A live webcast of the conference call will be available via the "Investors" section of Akebia's website at: https://ir.akebia.com/. An online archive of the webcast can be accessed via the Investors section of Akebia's website at https://ir.akebia.com approximately two hours after the event.

About Akebia Therapeutics

Akebia Therapeutics, Inc. is a fully integrated biopharmaceutical company with the purpose to better the lives of people impacted by kidney disease. Akebia was founded in 2007 and is headquartered in Cambridge, Massachusetts . For more information, please visit our website at www.akebia.com, which does not form a part of this release.

About Vafseo® (vadadustat) tablets

Vafseo® (vadadustat) tablets is a once-daily oral hypoxia-inducible factor prolyl hydroxylase inhibitor that activates the physiologic response to hypoxia to stimulate endogenous production of erythropoietin, increasing hemoglobin and red blood cell production to manage anemia. Vafseo is approved for use in 37 countries.

INDICATION

VAFSEO is indicated for the treatment of anemia due to chronic kidney disease (CKD) in adults who have been receiving dialysis for at least three months.

Limitations of Use

• VAFSEO has not been shown to improve quality of life, fatigue, or patient well-being.

• VAFSEO is not indicated for use:

• As a substitute for red blood cell transfusions in patients who require immediate correction of anemia.

• In patients with anemia due to CKD not on dialysis.

IMPORTANT SAFETY INFORMATION about VAFSEO (vadadustat) tablets

WARNING: INCREASED RISK OF DEATH, MYOCARDIAL INFARCTION, STROKE, VENOUS THROMBOEMBOLISM, and THROMBOSIS OF VASCULAR ACCESS.

VAFSEO increases the risk of thrombotic vascular events, including major adverse cardiovascular events (MACE).

Targeting a hemoglobin level greater than 11 g/dL is expected to further increase the risk of death and arterial and venous thrombotic events, as occurs with erythropoietin stimulating agents (ESAs), which also increase erythropoietin levels.

No trial has identified a hemoglobin target level, dose of VAFSEO, or dosing strategy that does not increase these risks.

Exhibit 99.1

Use the lowest dose of VAFSEO sufficient to reduce the need for red blood cell transfusions.

CONTRAINDICATIONS

• Known hypersensitivity to VAFSEO or any of its components

• Uncontrolled hypertension

WARNINGS AND PRECAUTIONS

• Increased Risk of Death, Myocardial Infarction (MI), Stroke, Venous Thromboembolism, and Thrombosis of Vascular Access

A rise in hemoglobin (Hb) levels greater than 1 g/dL over 2 weeks can increase these risks. Avoid

in patients with a history of MI, cerebrovascular event, or acute coronary syndrome within the 3

months prior to starting VAFSEO. Targeting a Hb level of greater than 11 g/dL is expected to

further increase the risk of death and arterial and venous thrombotic events. Use the lowest

effective dose to reduce the need for red blood cell (RBC) transfusions. Adhere to dosing and Hb

monitoring recommendations to avoid excessive erythropoiesis.

• Hepatotoxicity

Hepatocellular injury attributed to VAFSEO was reported in less than 1% of patients, including

one severe case with jaundice. Elevated serum ALT, AST, and bilirubin levels were observed

in 1.8%, 1.8%, and 0.3% of CKD patients treated with VAFSEO , respectively. Measure ALT,

AST, and bilirubin before treatment and monthly for the first 6 months, then as clinically

indicated. Discontinue VAFSEO if ALT or AST is persistently elevated or accompanied by elevated

bilirubin. Not recommended in patients with cirrhosis or active, acute liver disease.

• Hypertension

Worsening of hypertension was reported in 14% of VAFSEO and 17% of darbepoetin alfa

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Business Overview

We are a fully integrated biopharmaceutical company with two commercial products for patients impacted by kidney disease. We have built a business focused on developing and commercializing innovative therapeutics that we believe serve as a foundation for future growth, including by contributing net product revenue to support the development and advancement of our robust pipeline of mid-stage programs targeting rare kidney diseases and early-stage programs targeting kidney disease and non-kidney focused indications.

We have established the Company as a leader in the kidney community and believe our cross-organizational expertise in kidney disease positions us for success. Chronic kidney disease, or CKD , is a condition in which the kidneys are progressively damaged to the point that they cannot properly filter the blood circulating in the body. This damage causes waste products to build up in the patient's blood, leading to other health problems, including anemia, cardiovascular disease and bone disease. CKD significantly impacts the United States, or U.S. , healthcare system, potentially affecting approximately 35.5 million

Akebia Therapeutics, Inc. | Form 10-K | Page 120

patients. In 2022, in the U.S. treating Medicare beneficiaries with CKD cost an estimated $95.7 billion, and treating people on dialysis cost an estimated $45.3 billion. Our two commercial products address certain complications of kidney disease.

Our current product portfolio includes:

Vafseo® (vadadustat) is an orally administered medicine that was approved by the U.S. Food and Drug Administration, or the FDA , in March 2024 for the treatment of anemia due to CKD in adult patients on dialysis for at least three months. The current U.S. market opportunity for the treatment of anemia due to CKD in patients with dialysis is approximately $1 billion based on current erythropoiesis stimulating agent, or ESA , pricing. Vafseo is the only oral hypoxia inducible factor, or HIF , based treatment available in the U.S. Vafseo entered the market in January 2025, at which time we had commercial supply agreements for the purchase of Vafseo in place with dialysis organizations caring for nearly 100% of dialysis patients in the U.S. Throughout 2025, we worked closely with dialysis organizations as their medical teams developed, implemented and operationalized protocols to enable prescribers to write Vafseo prescriptions for clinically appropriate patients. Currently, approximately 290,000 dialysis patients in the U.S. have prescribing access to Vafseo.

Vafseo is approved for use in adults in 37 countries and is marketed in certain countries outside the U.S. by our partners. See Part I, Item 1, License and Collaboration Agreements, for details.

Auryxia® (ferric citrate) is an orally administered medicine approved and marketed in the U.S. for two indications: (1) the control of serum phosphorus levels in adult patients with dialysis dependent chronic kidney disease, or DD-CKD , and (2) the treatment of iron deficiency anemia, or IDA , in adult patients with non-dialysis-dependent chronic kidney disease, or NDD-CKD .

Today, we market Auryxia in the U.S. Auryxia became part of our portfolio in 2018 and has historically contributed meaningful revenue to the business. In March 2025, Auryxia reached loss of exclusivity, or LoE . On January 22, 2026, Teva Pharmaceuticals Ltd., or Teva , received tentative approval for its Abbreviated New Drug Application for Auryxia. Currently, there is only one authorized generic for Auryxia sold by our distributor, but we expect additional generic competition in 2026. If additional generics are approved and enter the market, we expect it will adversely impact our revenue.

Ferric citrate is approved for use and marketed in certain countries outside the U.S. by our partners. See Part I, Item 1, License and Collaboration Agreements, for details.

Our development pipeline includes:

Our mid-stage rare kidney disease pipeline assets , praliciguat and AKB-097, are being evaluated to target areas of unmet need. In June 2021, we licensed praliciguat from Cyclerion Therapeutics, Inc., or Cyclerion , via an exclusive global license, which includes certain intellectual property rights to research, develop and commercialize the asset. Praliciguat is an oral, once-daily soluble guanylate cyclase, or sGC , stimulator. We are evaluating praliciguat for the treatment of biopsy-confirmed focal segmental glomerulosclerosis, or FSGS , a rare kidney disease, in a Phase 2 clinical trial. The first patient was dosed in this trial in December 2025. We also plan to assess the use of praliciguat in other rare podocytopathies in the future.

In November 2025, we entered into an asset purchase agreement with Q32 Bio Inc. and Q32 Bio Operations Inc., together Q32 , pursuant to which we purchased and assumed substantially all assets and liabilities of Q32 and its affiliates related to the research, development, manufacture and commercialization of Q32's clinical-stage development candidate known as ADX-097, now referred to as AKB-097, an anti-C3d-Factor H fusion protein complement inhibitor. AKB-097 is a potential next-generation complement inhibitor, and we believe AKB-097 has applicability across a wide range of complement-mediated rare kidney diseases. AKB-097 is intended to provide targeted regulation of complement activation at sites of tissue injury while limiting systemic complement inhibition. We expect to initiate a Phase 2 basket study in the second half of 2026 to evaluate AKB-097 for the following indications: IgA Nephropathy, or IgAN ; C3 Glomerulopathy, or C3G; and Lupus Nephritis, or LN .

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Comparison of the years ended December 31, 2025 and 2024

Years ended December 31, | Change
(dollars in thousands) | 2025 | 2024 | %
Revenues
Product revenue, net | 227,332 | 152,180 | 75,152 | 49 | %
License, collaboration and other revenue | 8,864 | 8,000 | 864 | 11 | %
Total revenues | 236,196 | 160,180 | 76,016 | 47 | %
Cost of goods sold
Cost of product and other revenue | 39,462 | 27,135 | 12,327 | 45 | %
Amortization of intangible asset | — | 36,042 | (36,042) | (100) | %
Total cost of goods sold | 39,462 | 63,177 | (23,715) | (38) | %
Operating expenses
Research and development | 62,359 | 37,652 | 24,707 | 66 | %
Selling, general and administrative | 107,480 | 106,545 | 935 | 1 | %
License | 3,396 | 3,220 | 176 | 5 | %
Restructuring | — | 58 | (58) | (100) | %
Total operating expenses | 173,235 | 147,475 | 25,760 | 17 | %
Operating income (loss) | 23,499 | (50,472) | 73,971 | (147) | %
Other expense, net | (24,121) | (18,091) | (6,030) | 33 | %
Change in fair value of warrant liability | (3,099) | (330) | (2,769) | 839 | %
Loss on extinguishment of debt | — | (517) | 517 | (100) | %
Loss before income taxes | (3,721) | (69,410) | 65,689 | (95) | %
Income tax expense | (1,624) | — | (1,624) | *
Net loss | (5,345) | (69,410) | 64,065 | (92) | %

*Percentage change not meaningful.

Product Revenue, Net— Net product revenue is derived from sales of Auryxia and Vafseo in the U.S. We distribute Auryxia and Vafseo principally through a limited number of dialysis organizations, wholesale distributors, certain specialty pharmacy providers and our AG Distributor for Auryxia.

Net product revenue was $227.3 million for the year ended December 31, 2025, compared to net product revenue of $152.2 million for the year ended December 31, 2024. The increase was primarily due to Vafseo's entry to the market in January 2025 and an increase in sales volumes of Auryxia.

Auryxia lost exclusivity in the U.S. in March 2025, which may have a negative impact on future Auryxia revenue. Following LoE, our AG Distributor has been selling an authorized generic version of Auryxia in the U.S., which may slightly offset a revenue decline after entry of other generics. However, our ability to generate revenue from sales of Auryxia following entry of other generics will depend on many factors, including our ability to maintain contracts with dialysis organizations, the timing and number of additional generics that enter the market and the pricing of generics and other products on the market that compete with Auryxia.

The following table summarizes our product revenue for the years ended December 31, 2025 and 2024 (in thousands):

Years Ended December 31,
Product | 2025 | 2024
Vafseo (1) | 45,790 | —
Auryxia (2) | 181,542 | 152,180
Total product revenues | 227,332 | 152,180

Akebia Therapeutics, Inc. | Form 10-K | Page 125

(1) Vafseo entered the U.S. market in January 2025.

(2) Includes the authorized generic version of Auryxia sold and distributed by our AG Distributor during the year ended December 31, 2025.

License, Collaboration and Other Revenue— License, collaboration and other revenue was $8.9 million for the year ended December 31, 2025, compared to $8.0 million for the year ended December 31, 2024.

Cost of Goods Sold: Cost of Product and Other Revenue—Cost of product and other revenue was $39.5 million for the year ended December 31, 2025, compared to $27.1 million for the year ended December 31, 2024. The increase was primarily due to higher Auryxia volume during the year ended December 31, 2025. In addition, cost of product and other revenue for the year ended December 31, 2024 was offset by a $12.3 million benefit that we recorded due to our ability to sell inventory previously written-down as excess inventory during the year ended December 31, 2024.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business

Overview

We are a fully integrated biopharmaceutical company with two commercial products for patients impacted by kidney disease. We have built a business focused on developing and commercializing innovative therapeutics that we believe serve as a foundation for future growth, including by contributing net product revenue to support the development and advancement of our robust pipeline of mid-stage programs targeting rare kidney diseases and early-stage programs targeting kidney disease and non-kidney focused indications.

We have established the Company as a leader in the kidney community and believe our cross-organizational expertise in kidney disease positions us for success. Chronic kidney disease, or CKD , is a condition in which the kidneys are progressively damaged to the point that they cannot properly filter the blood circulating in the body. This damage causes waste products to build up in the patient's blood, leading to other health problems, including anemia, cardiovascular disease and bone disease. CKD significantly impacts the United States, or U.S. , healthcare system, potentially affecting approximately 35.5 million patients. In 2022, in the U.S. treating Medicare beneficiaries with CKD cost an estimated $95.7 billion, and treating people on dialysis cost an estimated $45.3 billion. Our two commercial products address certain complications of kidney disease.

Our current product portfolio includes:

Vafseo® (vadadustat) is an orally administered medicine that was approved by the U.S. Food and Drug Administration, or the FDA , in March 2024 for the treatment of anemia due to CKD in adult patients on dialysis for at least three months. The current U.S. market opportunity for the treatment of anemia due to CKD in patients with dialysis is approximately $1 billion based on current erythropoiesis stimulating agent, or ESA , pricing. Vafseo is the only oral hypoxia inducible factor, or HIF , based treatment available in the U.S. Vafseo entered the market in January 2025, at which time we had commercial supply agreements for the purchase of Vafseo in place with dialysis organizations caring for nearly 100% of dialysis patients in the U.S. Throughout 2025, we worked closely with dialysis organizations as their medical teams developed, implemented and operationalized protocols to enable prescribers to write Vafseo prescriptions for clinically appropriate patients. Currently, approximately 290,000 dialysis patients in the U.S. have prescribing access to Vafseo.

Vafseo is approved for use in adults in 37 countries and is marketed in certain countries outside the U.S. by our partners. See the section titled, "License and Collaboration Agreements" for details.

Auryxia® (ferric citrate) is an orally administered medicine approved and marketed in the U.S. for two indications: (1) the control of serum phosphorus levels in adult patients with dialysis dependent chronic kidney disease, or DD-CKD , and (2) the treatment of iron deficiency anemia, or IDA , in adult patients with non-dialysis-dependent chronic kidney disease, or NDD-CKD .

Today, we market Auryxia in the U.S. Auryxia became part of our portfolio in 2018 and has historically contributed meaningful revenue to the business. In March 2025, Auryxia reached loss of exclusivity, or LoE . On January 22, 2026, Teva Pharmaceuticals Ltd., or Teva , received tentative approval for its Abbreviated New Drug Application for Auryxia. Currently, there is only one authorized generic for Auryxia sold by our distributor, but we expect additional generic competition in 2026. If additional generics are approved and enter the market, we expect it will adversely impact our revenue.

Ferric citrate is approved for use and marketed in certain countries outside the U.S. by our partners. See the section titled "License and Collaboration Agreements" for details.

Our development pipeline includes:

Our mid-stage rare kidney disease pipeline assets , praliciguat and AKB-097, are being evaluated to target areas of unmet need. In June 2021, we licensed praliciguat from Cyclerion Therapeutics, Inc., or Cyclerion , via an exclusive global license, which includes certain intellectual property rights to research, develop and commercialize the asset. Praliciguat is an oral, once-daily soluble guanylate cyclase, or sGC , stimulator. We are evaluating praliciguat for the treatment of biopsy-confirmed focal segmental glomerulosclerosis, or FSGS , a rare kidney disease, in a Phase 2 clinical trial. The first patient was dosed in this trial in December 2025. We also plan to assess the use of praliciguat in other rare podocytopathies in the future.

In November 2025, we entered into an asset purchase agreement with Q32 Bio Inc. and Q32 Bio Operations Inc., together Q32 , pursuant to which we purchased and assumed substantially all assets and liabilities of Q32 and its

Akebia Therapeutics, Inc. | Form 10-K | Page 6

affiliates related to the research, development, manufacture and commercialization of Q32's clinical-stage development candidate known as ADX-097, now referred to as AKB-097, an anti-C3d-Factor H fusion protein complement inhibitor. AKB-097 is a potential next-generation complement inhibitor, and we believe AKB-097 has applicability across a wide range of complement-mediated rare kidney diseases. AKB-097 is intended to provide targeted regulation of complement activation at sites of tissue injury while limiting systemic complement inhibition. We expect to initiate a Phase 2 basket study in the second half of 2026 to evaluate AKB-097 for the following indications: IgA Nephropathy, or IgAN ; C3 Glomerulopathy, or C3G; and Lupus Nephritis, or LN .

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
