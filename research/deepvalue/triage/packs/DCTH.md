# Triage pack — DCTH · DELCATH SYSTEMS, INC.

_Generated 2026-09-04 18:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** DCTH · **Name:** DELCATH SYSTEMS, INC.
- **CIK:** 0000872912
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/DCTH

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** DELCATH SYSTEMS, INC.
- **CIK:** 872,912 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 16.48 |
| mktcap | $571.8M |
| ev | $524.3M |
| ev_ebit | 794.4x |
| fcf | $21.0M |
| fcf_yield | 3.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 0.7% |
| net_debt | -$47.5M |
| net_debt_ebit | -72.0x |
| cash | $47.5M |
| ltd | $0.00 |
| equity | $121.1M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $85.2M |
| revenue_prior | $37.2M |
| rev_growth | 129.1% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | $660k |
| net_income | $2.7M |
| cfo | $22.5M |
| capex | $1.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 34,698,795 |
| shares_py | 34,981,253 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 15.9% |
| r6m | 81.5% |
| off_52w_high | -5.1% |
| adv20 | $10.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.41 |
| r_ev_ebit | 0.00 |
| r_roic | 0.34 |
| r_rev_growth | 0.98 |
| r_buyback | 0.74 |
| score | 0.55 |

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
| rank | 201 |

**Screen rationale:** revenue +129.1%; debt data missing (net cash unverified); 12-1 momentum 15.9%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **34,698,795** (CY2026Q2I) vs **34,981,253** prior year (CY2025Q2I)
- Change: **-0.8%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-14** — Item 5.02 (officer / director change or comp arrangement): At the 2026 annual meeting of stockholders held on May 13, 2026 (the "Annual Meeting"), the stockholders of Delcath Systems, Inc. (the "Company") approved an amendment to the Company's 2020 Omnibus Equity Incentive Plan (the "2020 EIP") to increase by...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 16,733 sh / $150,328 vs sells 0 sh / $0 -> net $150,328 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: MICHEL GERARD J bought 11,200 sh @ $8.96 ($100,309) on 2026-03-02.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 2, sales 0).

| code | rows |
|---|---|
| A | 15 |
| P | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Delcath Systems Reports Second Quarter 2026'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (dcth-q22026erex991.htm)

Delcath Systems Reports Second Quarter 2026

Results and Business Highlights

Increases 2026 Revenue Guidance to a Range of $104M to $108M

Conference Call Today at 8:30 a.m. Eastern Time

QUEENSBURY, NY – August 6, 2026, Delcath Systems, Inc. (Nasdaq: DCTH), an interventional oncology company focused on the treatment of primary and metastatic liver cancers, today announced financial results and business highlights for the second quarter ended June 30, 2026.

Second Quarter 2026 Financial Results

• Total revenue of $29.1 million, compared with $24.2 million in the second quarter of 2025

◦ HEPZATO KIT™ revenue of $27.1 million, compared to $22.5 million in the second quarter of 2025

◦ CHEMOSAT ® revenue of $2.0 million, compared to $1.7 million in the second quarter of 2025

• Gross margins of 90%, compared to 86% in the second quarter of 2025

• Net income of $2.7 million for both second quarters in 2026 and 2025

• Non-GAAP adjusted EBITDA of $7.6 million, compared to $9.8 million in the second quarter of 2025

• Cash provided by operations of $5.7 million in the quarter; compared to $7.3 million in the second quarter of 2025

• Cash and investments of $95.9 million as of June 30, 2026

Business Highlights

• Currently 31 active treatment centers

• Approximately 30% growth in HEPZATO volume in the second quarter 2026 compared to the second quarter 2025

• Independent investigators presented retrospective data at ESMO Breast Cancer 2026 showing a 60% hepatic partial response rate with percutaneous hepatic perfusion in heavily pretreated patients with liver-dominant metastatic breast cancer

• Independent investigators presented two investigator-initiated Trials-in-Progress abstracts at ASCO 2026: one evaluating sequential HEPZATO followed by tebentafusp in metastatic uveal melanoma, and one evaluating HEPZATO in combination with nivolumab/relatlimab in metastatic cutaneous melanoma with liver metastases

• Dosed the first patient in the global Phase 2 trial of HEPZATO in combination with standard of care in patients with liver-dominant HER2-negative metastatic breast cancer

"Our strong second quarter, including total revenue of $29.1 million and quarterly operating cash flow of $5.7 million, reflects continued momentum in HEPZATO procedures," said Gerard Michel, Chief Executive Officer of Delcath Systems. "As we grow our active treatment center network and drive physician adoption, we are seeing increased usage of HEPZATO in combination with systemic therapies to treat metastatic uveal melanoma. The growing clinical experience with this treatment strategy is strengthening physician confidence in HEPZATO and supporting its development as a multi-indication, liver-directed therapy platform, including colorectal and breast cancer."

Exhibit 99.1

2026 Full Year Financial Guidance

The Company's financial outlook for fiscal year 2026:

• Total HEPZATO KIT and CHEMOSAT revenue to range from $104 million to $108 million, reflecting an increase in HEPZATO KIT volume of at least 28% over 2025

• Full year gross margins in the range of 86% to 89%

• Positive adjusted EBITDA

Second Quarter 2026 Results

Total revenue for the quarter ending June 30, 2026 was $29.1 million compared to $24.2 million for the same period in the prior year. Revenue in the quarter includes sales of $27.1 million of HEPZATO in the U.S. and $2.0 million of CHEMOSAT in Europe.

Research and development expenses for the quarter ending June 30, 2026, were $10.4 million compared to $6.9 million for the same period in the prior year. The increase is primarily due to increased clinical headcount and increased clinical trial activity.

Selling, general and administrative expenses for the quarter ended June 30, 2026, were $13.4 million compared to $11.4 million for the same period in the prior year. The increase is primarily due to continued commercial expansion activities.

Net income was $2.7 million for both the quarters ended June 30, 2026 and June 30, 2025.

Non-GAAP adjusted EBITDA for the quarter ended June 30, 2026 was $7.6 million compared to adjusted EBITDA of $9.8 million for the same period in the prior year. A table reconciling non-GAAP measures is included in this press release for reference.

As of June 30, 2026, the Company had $95.9 million in cash and investments, and no debt.

Conference Call Information

To participate in this event, dial in approximately 5 to 10 minutes before the beginning of the call.

Event Date: Thursday, August 6, 2026

Time: 8:30 AM Eastern Time

Participant Numbers:

Toll Free: 1-800-717-1738

International: 1-646-307-1865

Webcast: https://viavid.webcasts.com/starthere.jsp?ei=1767384&tp_key=cbc23b55c8

A replay of the webinar will be available shortly after the conclusion of the call and will be archived on the company's website https://investors.delcath.com/news-events/events-and-presentations.

GAAP v. Non-GAAP Measures

Delcath's reported earnings are prepared in accordance with generally accepted accounting principles in the United States, or GAAP, and represent earnings as reported to the Securities and Exchange Commission. Delcath has provided in this release certain financial information that has not been prepared in accordance with GAAP. Delcath's management believes that the non-GAAP adjusted EBITDA described in this release, which includes adjustments for specific items that are generally not indicative of our core operations, provides additional information that is useful to investors in understanding Delcath's underlying performance, business and performance trends, and helps facilitate period-to-period comparisons and comparisons of its financial measures with other companies in Delcath's industry. However, the non-GAAP financial measures that Delcath uses may differ from measures that other companies may use. Non-GAAP financial measures are not required to be uniformly applied, are not audited and should not be considered in isolation or as substitutes for results prepared in accordance with GAAP.

Exhibit 99.1

About Delcath Systems, Inc ., HEPZATO KIT and CHEMOSAT

Delcath Systems, Inc. is an interventional oncology company focused on the treatment of primary and metastatic liver cancers. The company's proprietary products, HEPZATO KIT™ (HEPZATO (melphalan) for Injection/Hepatic Delivery System) and CHEMOSAT® Hepatic Delivery System (HDS) for Melphalan percutaneous hepatic perfusion (PHP), are designed to administer high-dose chemotherapy to the liver while controlling systemic exposure and associated side effects during a PHP procedure.

In the United States, HEPZATO KIT is considered a combination drug and device product and is regulated and approved for sale as a drug by the FDA. HEPZATO KIT is comprised of the chemotherapeutic drug melphalan and Delcath ' s proprietary HDS. The HDS is used to isolate the hepatic venous blood from the systemic circulation while simultaneously filtrating hepatic venous blood during melphalan infusion and washout. The use of the HDS results in loco-regional delivery of a relatively high melphalan dose, which can potentially induce a clinically meaningful tumor response with minimal hepatotoxicity and reduce systemic exposure. HEPZATO KIT is approved in the United States as a liver-directed treatment for adult patients with metastatic uveal melanoma (mUM) with unresectable hepatic metastases affecting less than 50% of the liver and no extrahepatic disease, or extrahepatic disease limited to the bone, lymph nodes, subcutaneous tissues, or lung that is amenable to resection or radiation. Please see the full Prescribing Information, including BOXED WARNING for the HEPZATO KIT.

In Europe, the device-only configuration of the HDS is regulated as a Class III medical device and is approved for sale under the trade name CHEMOSAT Hepatic Delivery System for Melphalan, or CHEMOSAT, where it has been used in the conduct of percutaneous hepatic perfusion procedures at major medical centers to treat a wide range of cancers of the liver.

(Unaudited)

(in thousands, except share and per share data)

June 30, 2026 | December 31, 2025
Assets
Current assets
Cash and cash equivalents | 47,521 | 43,454
Short-term investments | 48,381 | 47,582
Accounts receivable | 15,942 | 11,744
Inventories | 11,713 | 10,252
Prepaid expenses and other current assets | 6,979 | 6,498
Total current assets | 130,536 | 119,530
Property, plant and equipment, net | 4,019 | 3,166
Right-of-use assets | 2,463 | 936
Total assets | 137,018 | 123,632
Liabilities and Stockholders' Equity
Current liabilities
Accounts payable | 4,011 | 2,658
Accrued expenses | 9,072 | 8,191
Lease liabilities, current | 196 | 101
Total current liabilities | 13,279 | 10,950
Lease liabilities, non-current | 2,267 | 835
Other liabilities, non-current | 327 | 628
Total liabilities | 15,873 | 12,413
Commitments and contingencies
Stockholders' equity
Preferred stock, $0.01 par value; 10,000,000 shares authorized; 14,192 and 14,192 shares issued and outstanding at June 30, 2026 and December 31, 2025, respectively | — | —
Common stock, $0.01 par value; 80,000,000 shares authorized; 34,636,252 shares and 34,691,671 shares issued and outstanding at June 30, 2026 and December 31, 2025, respectively | 346 | 347
Additional paid-in capital | 647,791 | 639,145
Accumulated deficit | (527,250) | (528,848)
Accumulated other comprehensive income | 258 | 575
Total stockholders' equity | 121,145 | 111,219
Total liabilities and stockholders' equity | 137,018 | 123,632

Exhibit 99.1

DELCATH SYSTEMS, INC.

Condensed Consolidated Statements of Operations and Comprehensive Income

(Unaudited)

(in thousands, except share and per share data)

Three months ended June 30, | Six months ended June 30,
2026 | 2025 | 2026 | 2025
Product revenue | 29,133 | 24,156 | 54,127 | 43,940
Cost of goods sold | (2,985) | (3,318) | (6,721) | (6,163)
Gross profit | 26,148 | 20,838 | 47,406 | 37,777
Operating expenses:
Research and development expenses | 10,380 | 6,882 | 20,204 | 11,889
Selling, general and administrative expenses | 13,373 | 11,366 | 26,444 | 22,656
Total operating expenses | 23,753 | 18,248 | 46,648 | 34,545
Operating income | 2,395 | 2,590 | 758 | 3,232
Interest income | 781 | 649 | 1,568 | 1,267
Other expense | (17) | (34) | (75) | (30)
Income before income taxes | 3,159 | 3,205 | 2,251 | 4,469
Income tax expense | 491 | 508 | 653 | 703
Net income | 2,668 | 2,697 | 1,598 | 3,766
Other comprehensive income:
Unrealized gain on investments adjustments | (295) | 57 | (250) | 296
Foreign currency translation adjustments | (18) | 154 | (67) | 214
Total comprehensive income | 2,355 | 2,908 | 1,281 | 4,276
Common share data:
Basic income per common share | 0.07 | 0.08 | 0.04 | 0.11
Weighted average number of basic shares outstanding | 35,891,915 | 35,786,813 | 35,956,205 | 35,217,887
Diluted income per common share | 0.07 | 0.07 | 0.04 | 0.09
Weighted average number of dilutive shares outstanding | 39,761,480 | 40,262,764 | 39,584,329 | 39,890,102

DELCATH SYSTEMS, INC.

Reconciliation of Reported Net Income (GAAP) to Adjusted EBITDA (NON-GAAP Measure)

(Unaudited)

(in thousands)

Three months ended June 30, | Six months ended June 30,
2026 | 2025 | 2026 | 2025
Net income | 2,668 | 2,697 | 1,598 | 3,766
Stock-based compensation expense | 5,118 | 7,209 | 10,064 | 14,072
Depreciation | 113 | 51 | 215 | 94
Interest income | (781) | (649) | (1,568) | (1,267)
Income tax expense | 491 | 508 | 653 | 703
Adjusted EBITDA (Non-GAAP) | 7,609 | 9,816 | 10,962 | 17,368

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are an interventional oncology company focused on the treatment of cancers primary or metastatic to the liver. Our lead product, the HEPZATO KIT (melphalan for Injection/Hepatic Delivery System), a drug/device combination product, was approved by the FDA on August 14, 2023, indicated as a liver-directed treatment for adult patients with uveal melanoma with unresectable hepatic metastases affecting less than 50% of the liver and no extrahepatic disease, or extrahepatic

disease limited to the bone, lymph nodes, subcutaneous tissues, or lung that is amenable to resection, or radiation. The first commercial use of the HEPZATO KIT for the treatment of mUM took place in January 2024.

In the United States, HEPZATO is considered a combination drug and device product and is regulated as a drug by the FDA. Primary jurisdiction for regulation of HEPZATO has been assigned to the FDA's Center for Drug Evaluation and Research. The FDA has granted us six orphan drug designations (five for melphalan in the treatment of patients with ocular (uveal) melanoma, cutaneous melanoma, intrahepatic cholangiocarcinoma, hepatocellular carcinoma, and neuroendocrine tumor indications and one for doxorubicin in the treatment of patients with hepatocellular carcinoma).

We have sufficient raw material and component constituent parts of the HEPZATO KIT to meet anticipated demand and we intend to manage supply chain risk through stockpiled inventory and contracting with multiple suppliers for critical components.

In Europe, the hepatic delivery system is a stand-alone medical device having the same device components as HEPZATO, but without the melphalan hydrochloride and is approved for sale under the trade name CHEMOSAT Hepatic Delivery System for Melphalan, or CHEMOSAT, where it has been used at major medical centers to treat a wide range of cancers in the liver. On February 28, 2022, CHEMOSAT received MDR certification under the European Medical Devices Regulation (EU) 2017/745, which may be considered by jurisdictions when evaluating reimbursement. As of March 1, 2022, we have assumed direct responsibility for sales, marketing and distribution of CHEMOSAT in Europe.

The FOCUS Trial

Our clinical development program for HEPZATO was comprised of the FOCUS Trial, a global registration clinical trial that investigated objective response rate in patients with mUM. The current focus of our clinical development program is to generate clinical data for CHEMOSAT and HEPZATO in patients with mUM, either as monotherapy or in combination with immunotherapy. On May 6, 2024, we announced the publication of results from our Phase 3 FOCUS Trial, including an ORR of 36.3%, which included 7.7% of patients with Complete Response, as determined by an Independent Review Committee. An ORR of 36.3% in the FOCUS study was statistically significantly better than the pooled ORR estimate (a weighted mean of the observed ORR) of 5.5% in the historical control group. We expect that the publication will support increased clinical adoption of and reimbursement for CHEMOSAT in Europe, and support reimbursement in various jurisdictions, including the United States.

In addition to HEPZATO's use to treat mUM, the Company believes that HEPZATO has the potential to treat other cancers in the liver, such as metastatic colorectal cancer, metastatic breast cancer, metastatic neuroendocrine tumors and intrahepatic cholangiocarcinoma.

Our IND application for a Phase 2 clinical trial evaluating HEPZATO in combination with SOC for liver-dominant mCRC was cleared by the FDA in December 2024. The Phase 2 trial will evaluate the safety and efficacy of HEPZATO in combination with trifluridine-tipiracil and bevacizumab compared to trifluridine-tipiracil and bevacizumab alone in patients with liver-dominant mCRC receiving third-line treatment. Approximately 90 patients will be enrolled in this randomized, controlled trial. Patient enrollment began during the third quarter of 2025, with the study expected to take place at more than 20 sites across the United States and Europe. In July 2025, we received authorization from the European Union and United Kingdom regulatory authorities for the clinical study of Melphalan for Injection/Hepatic Delivery System in patients with refractory metastatic colorectal cancer with the liver dominant disease. The trial's primary endpoint, hPFS, is anticipated to read out by the end of 2027, while OS, a secondary endpoint, is expected in 2028. We estimate that the total addressable market ("TAM") for liver-dominant mCRC receiving third-line treatment is between 6,000 and 10,000 patients annually in the United States. This market includes patients who present with significant liver disease burden, with liver-dominant status determined through radiological and clinical criteria. By targeting this patient population, we aim to provide a novel treatment option for those with limited therapeutic alternatives.

On April 28, 2025, we announced our IND application clearance by the FDA for the Phase 2 clinical trial of HEPZATO in mBC. The Phase 2 trial will evaluate the safety and efficacy of HEPZATO in combination with SOC versus SOC alone in patients with liver-dominant HER2-negative mBC following the failure of previous treatments. The SOC options will be the physician's choice of eribulin, vinorelbine or capecitabine. We expect approximately 90 patients will be enrolled in this randomized, controlled trial. The study will take place at more than 15 sites across the United States and Europe, with patient enrollment expected to begin in the first quarter of 2026. The trial's primary endpoint, hPFS, is anticipated to read out by the end of 2028, while results for OS, a secondary endpoint, is expected in 2029.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Year ended December 31,
(In thousands) | 2025 | 2024
Total revenues | 85,231 | 37,205
Cost of goods sold | (11,797) | (6,188)
Gross profit | 73,434 | 31,017
Research and development expenses | 29,246 | 13,874
Selling, general and administrative expenses | 43,528 | 29,553
Total operating expenses | 72,774 | 43,427
Operating income (loss) | 660 | (12,410)
Interest and other income (expense) | 2,850 | (13,976)
Income tax expense | 810 | —
Net income (loss) | 2,700 | (26,386)

Revenue

The increase in total revenue for the year ended December 31, 2025 compared to the same period for 2024 was due to the continued commercial expansion and demand of HEPZATO in the United States and CHEMOSAT in Europe. During the year ended December 31, 2025, 24 sites had treated at least one patient in HEPZATO versus 14 sites in the year ended December 31, 2024 .

On October 23, 2025, the Company entered into a National Drug Rebate Agreement ("NDRA") with CMS, which also subjected the Company to entering into a Pharmaceutical Pricing Agreement ("PPA") with the Public Health Service and a master agreement with the U.S. Department of Veterans Affairs ("VA"). Pursuant to the NDRA, the Company must pay mandated rebates to states for Medicaid usage. Under the PPA, beginning on July 1, 2025, the Company began selling HEPZATO to eligible covered entities at the statutory 340B price. The Company is also obligated to make any sales to the VA at the Federal Ceiling Price. See Note 4, Revenue , in the accompanying notes to the consolidated financial statements for further details.

Cost of Goods Sold

During the year ended December 31, 2025, we recorded $11.8 million in cost of goods sold. Cost of goods sold increased $5.6 million over the same period in 2024. This increase is directly related to the increase in demand for product revenue which requires an increase in personnel and those associated costs.

Research and Development Expenses

Research and development expenses are incurred for the development of HEPZATO and consist primarily of payroll and payments to contract research and development companies. The increase for the year ended December 31, 2025 compared to the same period in 2024 is due to costs associated with expanding the clinical team including share-based compensation expense related to an increase in headcount and initiation of the Phase 2 clinical trial evaluating HEPZATO in combination with standard of care for mCRC and mBC. In 2024, these costs primarily related to medical affairs and regulatory costs associated with the approved products.

Selling, General and Administrative Expenses

Selling, general and administrative expenses consist primarily of payroll and professional services such as accounting, legal, marketing and commercial preparation services. For the year ended December 31, 2025 compared to the same period in 2024, selling, general and administrative expenses increased due to continued commercial expansion activities including marketing-related travel expenses and additional personnel on the commercial team. In addition, the increase in personnel along with higher grant date exercise prices has increased the share-based compensation expense.

Interest and other Income/Expense

Interest and other income in 2025 are primarily related to the interest income associated with marketable securities and cash on hand. In 2024, this amount was offset by interest expense related to our debt instruments and the change in fair value of warrant liability. There was no interest expense for the year ended December 31, 2025 due to all debt being paid

off in 2024. There was no change in warrant valuation during the year ended December 31, 2025 due to the exercise of all Tranche B Warrants in 2024.

Critical Accounting Estimates

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business.

Unless the context otherwise requires, all references in this Annual Report on Form 10-K to the "Company", "Delcath", "Delcath Systems", "we", "our", and "us" refers to Delcath Systems, Inc., a Delaware corporation, incorporated in August 1988, and all entities included in our consolidated financial statements. Our corporate offices are located at 566 Queensbury Avenue, Queensbury, New York 12804. Our telephone number is (518) 743-8892 and our internet address is www.delcath.com. The information found on, or otherwise accessible through, our website is not incorporated by reference into, and does not form a part of, this Annual Report on Form 10-K.

Company Overview

We are an interventional oncology company focused on the treatment of cancers primary or metastatic to the liver. Our lead product, the HEPZATO TM KIT (melphalan for Injection/Hepatic Delivery System), a drug/device combination product ("HEPZATO" or "HEPZATO KIT"), was approved by the US Food and Drug Administration (the "FDA") on August 14, 2023, indicated as a liver-directed treatment for adult patients with uveal melanoma with unresectable hepatic metastases affecting less than 50% of the liver and no extrahepatic disease, or extrahepatic disease limited to the bone, lymph nodes, subcutaneous tissues, or lung that is amenable to resection, or radiation. The first commercial use of the HEPZATO for the treatment of metastatic hepatic dominant uveal melanoma ("mUM") took place in January 2024.

In the United States, HEPZATO is considered a combination drug and device product and is regulated as a drug by the FDA. Primary jurisdiction for regulation of HEPZATO has been assigned to the FDA's Center for Drug Evaluation and Research. The FDA has granted us six orphan drug designations (five for melphalan in the treatment of patients with ocular (uveal) melanoma, cutaneous melanoma, intrahepatic cholangiocarcinoma, hepatocellular carcinoma, and neuroendocrine tumor indications and one for doxorubicin in the treatment of patients with hepatocellular carcinoma).

We have sufficient raw material and component constituent parts of the HEPZATO KIT to meet anticipated demand and we intend to manage supply chain risk through stockpiled inventory and contracting with multiple suppliers for critical components.

In Europe, the hepatic delivery system is a stand-alone medical device having the same device components as HEPZATO, but without the melphalan hydrochloride and is approved for sale under the trade name CHEMOSAT Hepatic Delivery System for Melphalan, or CHEMOSAT, where it has been used at major medical centers to treat a wide range of cancers in the liver. On February 28, 2022, CHEMOSAT received Medical Device Regulation ("MDR") certification under the European Medical Devices Regulation (EU) 2017/745, which may be considered by jurisdictions when evaluating reimbursement. As of March 1, 2022, we assumed direct responsibility for sales, marketing and distribution of CHEMOSAT in Europe.

We operate as one operating segment. See Note 16 - " Segment Information " in the accompanying notes to our consolidated financial statements for further detail.

Cancers in the Liver—A Significant Unmet Medical Need

According to the American Cancer Society's ("ACS") Cancer Facts & Figures 2025 report, cancer is the second leading cause of death in the United States, with more than 618,000 deaths and over 2 million new cases expected to be diagnosed in 2025. Cancer is one of the leading causes of death worldwide, accounting for approximately 10 million deaths and 20 million new cases in 2022 according to GLOBOCAN, the database of the International Association of Cancer Registries. The financial burden of cancer is enormous for patients, their families and society. The liver is often the life-limiting organ for cancer patients and cancer that spreads to the liver is one of the leading causes of cancer death. Cancer that begins in one area of the body often metastasizes to the liver. Patient prognosis is generally poor once cancer has spread to the liver. Consequently, cancers in the liver remain a major unmet medical need globally.

Cancers in the Liver—Incidence and Mortality

Cancers in the liver consist of primary liver cancer and cancers metastatic to the liver. Primary liver cancers, hepatocellular carcinoma and intrahepatic cholangiocarcinoma, originate in the liver or biliary tract and are particularly prevalent in populations where the primary risk factors for the disease, such as hepatitis-B, hepatitis-C, high levels of alcohol consumption, aflatoxin, cigarette smoking and exposure to industrial pollutants, are present. Cancers metastatic to the liver, also called liver metastasis, or secondary liver cancer, result from the spread or "metastases" of a primary cancer into the liver. These metastases often continue to grow even after the primary cancer in another part of the body has been removed or successfully treated. Given the vital biological functions of the liver, including processing nutrients from food and

filtering toxins from the blood, it is not uncommon for metastases to settle in the liver. In many cases patients die not as a result of their primary cancer, but from the tumors that metastasize to their liver. In the United States, metastatic liver disease is more prevalent than primary liver cancer. We estimate that the total potential addressable market for liver cancer (primary and metastatic) is approximately 200,000 in the United States per year. Based on industry reports, it is estimated the total addressable market ("TAM") in the United States for mUM, metastatic cholangiocarcinoma ("mCCA"), metastatic neuroendocrine tumor ("mNET"), metastatic colorectal cancer ("mCRC"), metastatic breast cancer ("mBC"), metastatic non-small cell lung cancer ("mNSCLC"), metastatic pancreatic cancer ("mPC") and HCC, is well over $1.0 billion.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
