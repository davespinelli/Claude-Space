# Triage pack — ANGO · ANGIODYNAMICS INC

_Generated 2026-09-05 01:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ANGO · **Name:** ANGIODYNAMICS INC
- **CIK:** 0001275187
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** 05-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ANGO

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ANGIODYNAMICS INC
- **CIK:** 1,275,187 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 15.47 |
| mktcap | $639.4M |
| ev | $585.5M |
| ev_ebit | n/a |
| fcf | $508k |
| fcf_yield | 0.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -27.0% |
| net_debt | -$53.9M |
| net_debt_ebit | n/a |
| cash | $53.9M |
| ltd | $0.00 |
| equity | $170.8M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $320.2M |
| revenue_prior | $292.5M |
| rev_growth | 9.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$39.9M |
| net_income | -$36.7M |
| cfo | $3.1M |
| capex | $2.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 41,332,389 |
| shares_py | 40,633,885 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 41.6% |
| r6m | 42.3% |
| off_52w_high | -4.1% |
| adv20 | $5.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.21 |
| r_ev_ebit | 0.00 |
| r_roic | 0.04 |
| r_rev_growth | 0.64 |
| r_buyback | 0.35 |
| score | 0.30 |

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
| rank | 411 |

**Screen rationale:** debt data missing (net cash unverified); 12-1 momentum 41.6%


## 3. Share count trend

- Shares outstanding: **41,332,389** (CY2026Q2I) vs **40,633,885** prior year (CY2025Q2I)
- Change: **1.7%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 23,370 sh / $344,006 -> net $-344,006 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 22 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 6 |
| F | 5 |
| M | 10 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-14_2-02-results.md)

_Extraction: started at the first release heading, 'AngioDynamics Reports Record Fiscal Year 2026 Fourth Quarter and Full '; skipped 6 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ef20077916_ex99-1.htm)

AngioDynamics Reports Record Fiscal Year 2026 Fourth Quarter and Full Year Financial Results; Continued Execution Drives Med Tech Growth and Full-Year Profitability

Delivered its seventh consecutive quarter of double-digit Med Tech segment growth and positive adjusted EBITDA

LATHAM, N.Y.--(BUSINESS WIRE)— July 14, 2026-- AngioDynamics, Inc. (NASDAQ: ANGO), a leading and transformative medical technology company focused on restoring healthy
blood flow in the body's vascular system, expanding cancer treatment options, and improving quality of life for patients, today announced financial results for the fourth quarter and fiscal year 2026, which ended May 31, 2026.

Fiscal Year 2026 Fourth Quarter Financial Highlights

Quarter Ended May 31, 2026 | Pro Forma* YoY Growth
Pro Forma* Net Sales | $86.6 million | 8.0%
Med Tech Net Sales | $41.8 million | 16.7%
Med Device Net Sales | $44.8 million | 1.1%

• | GAAP gross margin of 54.0%

• | GAAP loss per share of $0.27

• | Adjusted loss per share of $0.07

• | Adjusted EBITDA of $3.3 million

Fiscal Year 2026 Financial Highlights

Year Ended May 31, 2026 | Pro Forma* YoY Growth
Pro Forma* Net Sales | $320.2 million | 9.4%
Med Tech Net Sales | $150.0 million | 18.4%
Med Device Net Sales | $170.2 million | 2.5%

• | GAAP gross margin of 54.6%

• | GAAP loss per share of $0.88

• | Adjusted loss per share of $0.24

• | Adjusted EBITDA of $13.2 million

• | Ended fiscal year 2026 with $53.9 million in cash

*Pro forma results exclude the Dialysis and BioSentry businesses divested in June 2023 and the PICC and Midline product portfolios divested in
February 2024, as well as the discontinued RadioFrequency and Syntrax products in February 2024.

Clinical, Regulatory, and Market Access Highlights

During the fiscal year:

• | Received FDA IDE approval for APEX-Return study evaluating AlphaReturn Blood Management System when used with AlphaVac F18 85 System

• | Received FDA IDE approval for PAVE clinical study evaluating AngioVac System for treatment of right-sided infective endocarditis

• | Initiated both the AMBITION BTK and RECOVER-AV trials

During the fourth quarter:

• | Two-year follow up data from its PRESERVE pivotal trial presented at the American Urological Association conference in 2026 demonstrating NanoKnife's durable prostate cancer outcomes

• | Palmetto GBA (Government Benefits Administrators) finalized a local coverage determination covering NanoKnife IRE for qualifying Medicare patients in prostate and liver cancer, effective July 5, 2026

Subsequent to fiscal year end:

• | Received FDA IDE (Investigational Device Exemption) approval for the RELIEF study evaluating NanoKnife IRE for the treatment of benign prostatic hyperplasia

"Our strong fourth quarter capped a year of consistent execution at AngioDynamics," said Jim Clemmer, President and Chief Executive Officer of
AngioDynamics, Inc. "Full-year Med Tech growth of more than 18% reflects the continued progress of our strategic transformation, as our innovative platform technologies across cardiology and interventional oncology took share in large,
fast-growing global markets. Combined with our operational discipline, that growth drove continued profitability even as we absorbed tariff-related headwinds."

"We advanced our portfolio on multiple fronts during the year. We generated compelling two-year PRESERVE clinical data and secured a critical
Medicare coverage pathway for NanoKnife in prostate and liver, while achieving key regulatory milestones across our Mechanical Thrombectomy portfolio, including IDE approvals for our AlphaVac blood return and AngioVac right-sided endocarditis
studies. Auryon delivered its 20th consecutive quarter of double-digit growth, and NanoKnife adoption accelerated following the effective date of the Category I CPT code for prostate."

Mr. Clemmer continued, "As we look ahead to fiscal 2027, we remain focused on driving sustained growth led by our Med Tech segment. Med Tech
represented 47% of our total revenue in fiscal 2026, up approximately 22% from when we began our strategic transformation in 2020. We expect that mix to continue shifting toward our higher-growth, higher-margin platforms. With a differentiated
technology portfolio, multiple growth catalysts ahead, and a debt-free balance sheet with positive cash generation, we are well-positioned to deliver continued value creation in fiscal 2027 and beyond."

Fiscal Fourth Quarter 2026 Financial Results

Unless otherwise noted, all financial comparisons below are presented on a pro forma basis excluding the Dialysis and BioSentry businesses
divested in June 2023, the PICC, Midline, and tip location product portfolios divested in February 2024, and the RadioFrequency and Syntrax support catheter products discontinued in February 2024.

Net sales for the fourth quarter of fiscal year 2026 were $86.6 million, an increase of 8.0% compared to the prior-year quarter.

Med Tech net sales were $41.8 million, a 16.7% increase from $35.8 million in the prior-year period. Med Tech includes the Auryon peripheral
atherectomy platform, our thrombus management platform which is led by AlphaVac and AngioVac, and the NanoKnife irreversible electroporation platform.

Growth during the quarter was driven by solid performance across the Med Tech segment. Auryon sales were $17.8 million, an increase of 14.4%
compared to the prior-year quarter. In our Mechanical Thrombectomy business, AlphaVac sales grew 38.4% compared to the prior year quarter, while AngioVac faced a tough comparison, declining 15.8% versus prior year. Overall, Mechanical
Thrombectomy delivered sales of $11.1 million, a decrease of 1.1% compared to the prior-year quarter. NanoKnife sales were $11.8 million, an increase of 64.5% compared to the prior-year quarter, including 47.0% growth in probes and 132.5% growth
in capital sales.

Med Device net sales were $44.8 million, a 1.1% increase compared to $44.4 million in the prior-year period.

Gross margin for the fourth quarter of fiscal 2026 was 54.0%, which was 130 basis points higher compared to the fourth quarter of fiscal 2025,
primarily driven by favorable pricing and the ongoing revenue mix shift toward Med Tech, partially offset by the manufacturing transition and global inflation all of which were in-line with the Company's expectations.

The Company recorded a GAAP net loss of $11.4 million, or a loss per share of $0.27, in the fourth quarter of fiscal 2026, compared to a net
loss of $6.1 million, or a loss per share of $0.15, a year ago. Excluding the items shown in the non-GAAP reconciliation table below, adjusted net loss for the fourth quarter of fiscal 2026 was $2.8 million, or a loss per share of $0.07. This
compares to an adjusted net loss during the fiscal fourth quarter of 2025 of $1.1 million, or a loss per share of $0.03.

Adjusted EBITDA in the fourth quarter of fiscal 2026, excluding the items shown in the non-GAAP reconciliation table below, was $3.3 million,
compared to $3.4 million in the fourth quarter of fiscal 2025.

Tariff-related expenses were $0.5 million during the quarter, compared to $1.6 million for the prior year quarter, in-line with the Company's
expectations.

In the fourth quarter of fiscal 2026, the Company generated $17.5 million of cash from
operations, slightly ahead of the Company's expectations.

Full-Year 2026 Financial Results

Unless otherwise noted, all financial comparisons below are presented on a pro forma basis excluding the Dialysis and BioSentry businesses
divested in June 2023, the PICC, Midline, and tip location product portfolios divested in February 2024, and the RadioFrequency and Syntrax support catheter products discontinued in February 2024.

Net sales were $320.2 million, an increase of 9.4%, compared to $292.7 million for the prior year period.

Med Tech net sales were $150.0 million, an 18.4% increase from $126.7 million in the prior year.

Med Device net sales were $170.2 million, an increase of 2.5% from $166.0 million in the prior year.

Gross margin increased 70 basis points to 54.6% from 53.9% in the prior year, with tariffs creating a 151-basis point headwind.

The Company's GAAP net loss was $36.7 million, or a loss per share of $0.88, compared to a net loss of $34.0 million, or a loss per share of
$0.83, a year ago. Excluding the items shown in the non-GAAP reconciliation table below, adjusted net loss was $10.0 million, with adjusted loss per share of $0.24, compared to adjusted net loss of $10.2 million, or adjusted loss per share of
$0.25, a year ago.

Adjusted EBITDA, excluding the items shown in the reconciliation table below, was $13.2 million, compared to $7.6 million for the prior year.

Tariff-related expenses were $4.8 million during the year, compared to $1.6 million for the prior year, in-line with the Company's expectations.

In the full year of fiscal 2026, the Company generated $3.1 million of cash from operations , slightly ahead of the Company's stated expectations following Q3.

At May 31, 2026, the Company had $53.9 million in cash and maintains a debt-free balance sheet.

FDA IDE Approval for RELIEF BPH Study

Subsequent to fiscal year-end, the Company received FDA approval of its IDE for the RELIEF study, a feasibility trial evaluating NanoKnife IRE for
the treatment of benign prostatic hyperplasia. The study is designed to enroll 40 subjects at up to five U.S. clinical sites, with a primary endpoint measuring change in the International Prostate Symptom Score at six months. RELIEF extends the
NanoKnife IRE platform beyond oncology into one of the most common conditions affecting men's health. The Company views the study as an important step in expanding the long-term addressable market for its IRE technology.

Two-Year PRESERVE Data Demonstrates Durable Prostate Cancer Outcomes

In May 2026, the Company presented two-year results from its PRESERVE pivotal trial at the American Urological Association Annual Meeting,
demonstrating durable outcomes for the NanoKnife System in the focal ablation of intermediate-risk prostate cancer. PRESERVE is a prospective, single-arm pivotal IDE study that enrolled 121 patients across 17 U.S. clinical sites in collaboration
with the Society of Urologic Oncology Clinical Trials Consortium. At 24 months, no new treatment failures were identified among patients with available follow-up, and 97% of patients had a PSA below their baseline value, with no new device- or
procedure-related adverse events reported between the 12- and 24-month assessments. These results build on the trial's previously published 12-month primary endpoint and reinforce the durability of focal IRE as a treatment option that preserves
quality of life.

Category I CPT Codes and Medicare Coverage Advance NanoKnife Reimbursement

The Company continued to advance the reimbursement framework for irreversible
electroporation (IRE) delivered by the NanoKnife System. Effective January 1, 2026, Category I CPT codes for IRE procedures in the prostate and liver became active, reflecting the American Medical Association's formal recognition of the
procedure and supporting standardized billing across hospital outpatient and ambulatory surgical center settings. Building on this, in May 2026 Palmetto GBA issued a final Local Coverage Determination establishing Medicare coverage guidance for IRE in favorable intermediate-risk prostate cancer and metastatic colorectal
cancer to the liver, effective July 5, 2026. Together, these milestones enable eligible patients and treating physicians to access reimbursement under Medicare and mark an important step toward broader national payer adoption.

FDA IDE Approval for APEX-Return Study

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-07-14_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations for the years ended May 31, 2026 and 2025

For the fiscal year ended May 31, 2026, the Company reported a net loss of $36.7 million, or a loss of $0.88 per diluted share, on net sales of $320.2 million compared to a net loss of $34.0 million, or a loss of $0.83 per diluted share, on net sales of $292.5 million in fiscal year 2025.

Net Sales

Net sales - Net sales are derived from the sale of our products and related freight charges, less discounts, rebates and returns.

Year ended May 31,
(in thousands) | 2026 | 2025 | $ Change
Net Sales
Med Tech | 149,954 | 126,653 | 23,301
Med Device | 170,220 | 165,845 | 4,375
Total | 320,174 | 292,498 | 27,676
Net Sales by Geography
United States | 274,923 | 250,983 | 23,940
International | 45,251 | 41,515 | 3,736
Total | 320,174 | 292,498 | 27,676

For the year ended May 31, 2026, net sales increased $27.7 million to $320.2 million compared to the year ended May 31, 2025. At May 31, 2026, the Company had a backlog of $0.3 million compared to $0.3 million at the end of May 31, 2025.

The Med Tech business net sales increased $23.3 million for the year ended May 31, 2026 compared to the prior year. The change in sales from the prior year was primarily driven by:

• Increased Auryon sales of $10.0 million;

• Increased sales of the thrombus management platform of $4.6 million, which was driven by increases in AngioVac and AlphaVac sales of $0.6 million and $4.7 million, respectfully, which was partially offset by a decrease in thrombolytic sales of $0.7 million; and

• Increased NanoKnife sales of $8.6 million which was driven by increased disposable and capital sales.

The Med Device business net sales increased $4.4 million for the year ended May 31, 2026 compared to the prior year. The backlog, which primarily impacted sales of Core and Vascular Access products, was $0.3 million at May 31, 2026 compared to $0.3 million at May 31, 2025. The change in sales from the prior year was primarily driven by:

• Increased sales of Core and Venous of $3.6 million and $2.2 million, respectively. This increase was partially offset by decreased sales of Ports, Microwave and other Oncology products of $1.2 million, $0.1 million and $0.3 million, respectively.

Gross Margin

Year ended May 31,
(in thousands) | 2026 | 2025 | $ Change
Med Tech | 95,356 | 78,515 | 16,841
Gross margin % of sales | 63.6 | % | 62.0 | %
Med Device | 79,536 | 79,190 | 346
Gross margin % of sales | 46.7 | % | 47.7 | %
Total | 174,892 | 157,705 | 17,187
Gross margin % of sales | 54.6 | % | 53.9 | %

Gross margin - Gross margin consists of net sales less the cost of goods sold, which includes the costs of materials, products purchased from third parties and sold by us, manufacturing personnel, royalties, freight, business insurance, depreciation of property and equipment and other manufacturing overhead, exclusive of intangible amortization.

Total Company gross margin increased by $17.2 million compared to the prior year. The change from the prior year was primarily driven by:

• Sales volume, price and product mix, which positively impacted gross margin by $26.6 million;

• Benefits from product lines transitioned to third-party manufacturers along with other incentives, which positively impacted gross margin by $0.9 million;

• Production volume and other operations costs, which negatively impacted gross margin by $5.2 million;

• Tariffs, which negatively impacted gross margin by $3.2 million; and

• Inflation, which negatively impacted gross margin by $1.9 million.

The Med Tech segment gross margin increased by $16.8 million compared to the prior year. The change from the prior year was primarily driven by:

• Sales volume and price, which positively impacted gross margin by $16.4 million;

• Favorable purchasing price variance due to shifting to lower cost suppliers, which positively impacted gross margin by $2.7 million;

• Tariffs, which positively impacted gross margin by $0.6 million due to refunds received and lower tariff rates;

• Freight and other costs, which negatively impacted gross margin by $1.2 million;

• Product mix, which negatively impacted gross margin by $0.7 million;

• Production volume, which negatively impacted gross margin by $0.1 million; and

• Incremental depreciation on placement units of $0.8 million.

The Med Device segment gross margin increased by $0.3 million compared to the prior year. The change from the prior year was primarily driven by:

• Price and product mix, which positively impacted gross margin by $11.5 million;

• Benefits from product lines transitioned to third-party manufacturers along with other incentives, which positively impacted gross margin by $2.1 million;

• Sales volume, which negatively impacted gross margin by $0.5 million;

• Production volume and other operations costs, which negatively impacted gross margin by $5.1 million;

• Tariffs, which negatively impacted gross margin by $3.8 million;

• Inflation, which negatively impacted gross margin by $4.6 million; and

• A decrease in incremental depreciation on placement units of $0.8 million.

Operating Expenses and Other Income (Expense)

Year ended May 31,
(in thousands) | 2026 | 2025 | $ Change
Research and development | 29,447 | 26,222 | 3,225
% of sales | 9.2 | % | 9.0 | %
Selling and marketing | 113,401 | 103,135 | 10,266
% of sales | 35.4 | % | 35.3 | %
General and administrative | 43,691 | 42,092 | 1,599
% of sales | 13.6 | % | 14.4 | %

Research and development expense - Research and development ("R&D") expense includes internal and external costs to develop new products, enhance existing products, validate new and enhanced products, manage clinical, regulatory and medical affairs.

R&D expense increased $3.2 million compared to the prior year. The change from the prior year was primarily driven by:

• The timing of certain projects and clinical spend associated with the ongoing clinical trials, which increased R&D expense by $2.0 million; and

• Compensation and benefits expenses, which increased $1.2 million.

Sales and marketing expense - Sales and marketing ("S&M") expense consists primarily of salaries, commissions, travel and related business expenses, attendance at medical society meetings, product promotions and marketing activities.

S&M expense increased by $10.3 million compared to the prior year. The change from the prior year was primarily driven by:

• Compensation and benefits expense, which increased by $7.6 million;

• Consulting, travel and other selling expenses, which increased $1.7 million; and

• Trade shows, subscriptions and other marketing expenses, which increased $1.0 million.

General and administrative expense - General and administrative ("G&A") expense includes executive management, finance, information technology, human resources, business development, legal, and the administrative and professional costs associated with those activities.

G&A expense increased by $1.6 million compared to the prior year. The change from the prior year was primarily driven by:

• Compensation and benefits expense, which increased $5.6 million;

• Other outside consultant spend, which decreased $3.2 million; and

• Depreciation and other corporate expenses, which decreased $0.8 million.

Year ended May 31,
(in thousands) | 2026 | 2025 | $ Change
Amortization of intangibles | 10,682 | 10,318 | 364
Change in fair value of contingent consideration | — | 272 | (272)
Acquisition, restructuring and other items, net | 17,598 | 15,620 | 1,978
Other income | 3,627 | 5,922 | (2,295)

Amortization of intangibles - Represents the amount of amortization expense that was taken on intangible assets held by the Company.

• Amortization expense remained consistent compared to the prior year.

Change in fair value of contingent consideration - Represents changes in contingent consideration driven by changes to estimated future payments on earn-out liabilities created through acquisitions and amortization of present value discounts on long-term contingent consideration.

• The change in the fair value for the year ended May 31, 2026 is related to the Eximo contingent consideration. The final milestone associated with the contingent consideration was reached during the third quarter of fiscal year 2025 and was paid during the fourth quarter of fiscal year 2025.

Acquisition, restructuring and other items, net - Acquisition, restructuring and other items, net represents costs associated with mergers and acquisitions, restructuring expenses, legal costs that are related to litigation that is not in the ordinary course of business, legal settlements and other one-time items.

Acquisition, restructuring and other items, net increased by $2.0 million compared to the prior year. The change from the prior year was primarily driven by:

• Legal expense, related to litigation that is outside of the normal course of business, which increased $1.3 million;

• Mergers and acquisitions expense, which decreased $0.7 million;

• Transaction services agreements that were entered into as a result of the divestiture of the PICCs, Midline, dialysis and BioSentry businesses. The decrease in the fees invoiced was $0.3 million;

• Plant closure expense, related to the restructuring of our manufacturing footprint which was announced on January 5, 2024, which decreased $0.6 million;

• Transition expenses related to the upcoming retirement of our CEO which was announced on January 6, 2026, which increased $1.6 million; and

• Other expenses, mainly severance associated with organizational changes, which increased $0.1 million.

Other income (expense) - Other expense includes interest income and expense, foreign currency impacts and bank fees.

Other income, net decreased by $2.3 million compared to the prior year. The change from the prior year was primarily driven by:

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-07-14_item1_business.md)

Item 1. Business.

OVERVIEW

AngioDynamics is a dynamic, diversified medical technology company committed to expanding treatment options and improving patient outcomes and quality of life by designing, manufacturing and selling products and technologies which aid clinicians in the treatment of patients with cardiovascular disease and cancer diagnoses. Our execution strategy is built on innovative R&D, clinical and regulatory pathway expansion and customer centric sales performance.

HISTORY

AngioDynamics was founded in Queensbury, N.Y., U.S., in 1988 and began manufacturing and shipping product in the early 1990s. The Company is headquartered in Latham, N.Y., with manufacturing primarily out of the Queensbury facility. Initially dedicated to the research and development of products used in interventional radiology, the Company soon became well established as a producer of diagnostic catheters for non-coronary angiography and thrombolytic delivery systems.

The Company grew over the following years as a result of acquisitions of companies including RITA Medical Systems in January 2007, Oncobionic in May 2008, the assets of Diomed in June 2008, Vortex Medical, Inc. in October 2012, the assets of Microsulis Medical Limited in January 2013, and Clinical Devices in August 2013. These acquisitions added product lines including ablation and NanoKnife systems, vascular access products, angiographic products and accessories, dialysis products, drainage products, thrombolytic products, embolization products and venous products. In May 2012, the Company acquired Navilyst Medical's Fluid Management business, which the Company sold in May 2019 to Medline Industries, Inc. pursuant to an asset purchase agreement.

In August 2018, the Company acquired the BioSentry product line from Surgical Specialties, LLC, which the Company sold in June 2023 to Merit Medical Systems, Inc. pursuant to an asset purchase agreement. In September 2018, the Company acquired RadiaDyne, which included endorectal and vaginal balloons. On October 2, 2019, the Company acquired Eximo Medical, Ltd., a pre-commercial stage medical device company and its proprietary 355nm laser atherectomy technology (now called Auryon), which treats Peripheral Artery Disease. On December 17, 2019, the Company acquired the C3 Wave tip location asset from Medical Components Inc. On July 27, 2021, AngioDynamics acquired the Camaro Support Catheter asset from QX Medical, LLC.

On June 8, 2023, the Company completed the sale of the dialysis and BioSentry businesses to Merit Medical Systems, Inc. On February 15, 2024, the Company completed the sale of its PICC and Midline businesses, which included the C3 Wave tip location asset, to Spectrum Vascular. As of February 29, 2024, the Company discontinued the RadioFrequency Ablation and Syntrax product lines.

AngioDynamics is publicly traded on the NASDAQ stock exchange under the symbol ANGO.

PRODUCTS

Our product offerings fall within two segments, Med Tech and Med Device. All products discussed below have been cleared for sale in the United States by the Food and Drug Administration. International regulatory clearances vary by product and jurisdiction.

Med Tech

Auryon

The Auryon Atherectomy System represents one of our latest advancements in the treatment of peripheral arterial disease. The device is engineered to deliver an optimized wavelength and short pulse width to remove a wide range of lesion types while minimizing damage to the vessel wall endothelium. Incorporating integrated aspiration, the Auryon System enhances procedural safety by helping remove plaque from the vasculature. The device delivers safe, effective and versatile treatment across a broad spectrum of lesion types and anatomical locations including above and below the knee. Designed for flexibility, the device supports femoral, pedal or radial access allowing physicians to expand treatment options for their patients. The Auryon system delivers a safe, efficient and comprehensive treatment option on one single platform.

Thrombectomy

Our Thrombus Management portfolio includes the AlphaVac Mechanical Thrombectomy System, AngioVac venous drainage cannula and circuit, as well as catheter directed thrombolytic devices, including the Uni-Fuse system and the Uni-Fuse+ system. AngioDynamics offers a range of options when treating thrombus and removing fresh, soft thrombi or emboli.

AngioVac

Our AngioVac venous drainage system includes a Venous Drainage Cannula and Extracorporeal Circuit. The cannula is indicated for use as a venous drainage cannula and for removal of fresh, soft thrombi or emboli during extracorporeal bypass. The AngioVac circuit is indicated for use in procedures requiring extracorporeal circulatory support for periods of up to six hours. AngioVac devices are for use with other manufacturers' off-the-shelf pump, filter and reinfusion cannula, to facilitate venous drainage as part of an extracorporeal bypass procedure.

The AngioVac venous drainage cannula is a 22 French flat coil-reinforced cannula designed with a proprietary self-expanding nitinol reinforced funnel shaped distal tip. The funnel shaped tip enhances venous drainage flow when the distal tip is exposed by retracting the sheath, helps prevent clogging of the cannula with commonly encountered undesirable intravascular material, and facilitates embolic removal of such extraneous material.

AlphaVac

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-07-14_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-07-14_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-07-14_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-14_2-02-results.md, 10-K_2026-07-14_item7_mdna.md, 10-K_2026-07-14_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
