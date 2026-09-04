# Triage pack — KROS · Keros Therapeutics, Inc.

_Generated 2026-09-04 14:02 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** KROS · **Name:** Keros Therapeutics, Inc.
- **CIK:** 0001664710
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/KROS

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Keros Therapeutics, Inc.
- **CIK:** 1,664,710 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 11.11 |
| mktcap | $220.3M |
| ev | -$37.3M |
| ev_ebit | n/a |
| fcf | $106.0M |
| fcf_yield | 48.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 1,132.4% |
| net_debt | -$257.6M |
| net_debt_ebit | -3.8x |
| cash | $257.6M |
| ltd | $0.00 |
| equity | $262.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $243.9M |
| revenue_prior | $0.00 |
| rev_growth | n/a |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $67.6M |
| net_income | $87.0M |
| cfo | $107.5M |
| capex | $1.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -51.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 19,827,188 |
| shares_py | 40,615,414 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -36.6% |
| r6m | -5.1% |
| off_52w_high | -49.1% |
| adv20 | $2.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.97 |
| r_ev_ebit | 0.00 |
| r_roic | 1.00 |
| r_rev_growth | 0.50 |
| r_buyback | 0.99 |
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
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 66 |

**Screen rationale:** top-quartile FCF yield 48.1%; high ROIC 1132.4%; buying back stock -51.2%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **19,827,188** (CY2026Q2I) vs **40,615,414** prior year (CY2025Q2I)
- Change: **-51.2%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-22** — Item 5.02 (officer / director change or comp arrangement): On July 17, 2026, Keith Regnante resigned from his role as Chief Financial Officer of Keros Therapeutics, Inc. (the "Company"), effective August 3, 2026 (the "Separation Date"), to pursue other opportunities.
- **2026-06-25** — Item 5.02 (officer / director change or comp arrangement): On June 23, 2026, the board of directors (the "Board") of Keros Therapeutics, Inc. (the "Company"), based upon a recommendation from the Nominating and Corporate Governance Committee of the Board (the "Nominating Committee"), voted to appoint Anne Prener...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 3,000 sh / $31,070 vs sells 15,628 sh / $162,990 -> net $-131,920 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: BIENAIME JEAN JACQUES bought 1,000 sh @ $10.61 ($10,610) on 2026-07-15.

Form 4 filings parsed: 12; transaction rows: 14 (open-market buys 3, sales 7).

| code | rows |
|---|---|
| A | 4 |
| P | 3 |
| S | 7 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'Keros Therapeutics Reports Second Quarter 2026 Financial Results'; skipped 9 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (exhibit991q22026.htm)

Keros Therapeutics Reports Second Quarter 2026 Financial Results

LEXINGTON, Mass., August 3, 2026 (GLOBE NEWSWIRE) -- Keros Therapeutics, Inc. ("Keros" or the "Company") (Nasdaq: KROS), a clinical-stage biopharmaceutical company focused on developing and commercializing novel therapeutics to treat a wide range of patients with disorders that are linked to dysfunctional signaling of the transforming growth factor-beta ("TGF-ß") family of proteins, today provided a business update and reported financial results for the quarter ended June 30, 2026.

"We are excited to have initiated our Phase 2 clinical trial evaluating the treatment of rinvatercept in patients with Duchenne muscular dystrophy ("DMD"), marking an important milestone in the development of our program," said Jasbir S. Seehra, Ph.D., President and Chief Executive Officer. "In our Phase 1 clinical trial in healthy volunteers, rinvatercept demonstrated robust pharmacological activity observed through increases in muscle mass and bone mineral density, alongside a decrease in fat mass. We look forward to the progression of the Phase 2 clinical trial, and continue to expect to present initial data in the first half of 2027."

Second Quarter 2026 Financial Results

Keros reported a net loss of $28.7 million in the second quarter of 2026 as compared to a net loss of $30.7 million in the second quarter of 2025. The decrease of $2.0 million was primarily due to revenue recognized in 2025 related to Keros' license agreement with Takeda and decreased research and development efforts.

Research and development expenses were $22.3 million for the second quarter of 2026 as compared to $43.5 million for the same period in 2025. The decrease of $21.2 million was primarily due to the transition of elritercept-related research and development expenses to Takeda and the corporate restructuring that was completed in 2025.

General and administrative expenses were $8.6 million for the second quarter of 2026 as compared to $14.5 million for the same period in 2025. The decrease of $5.9 million was primarily due to a decrease in professional fees and a decrease in compensation costs in connection with the 2025 corporate restructuring.

Keros' cash and cash equivalents as of June 30, 2026 was $257.6 million compared to $287.4 million as of December 31, 2025. Based on current operating assumptions, Keros expects that its cash and cash equivalents as of June 30, 2026 will enable Keros to fund its operating expenses and capital expenditure requirements into the first half of 2028.

About Keros Therapeutics, Inc.

Keros is a clinical-stage biopharmaceutical company focused on developing and commercializing novel therapeutics to treat a wide range of patients with disorders that are linked to dysfunctional signaling of the TGF-ß family of proteins. Keros is a leader in understanding the role of the TGF-ß family of proteins, which are master regulators of the growth, repair and maintenance of a number of tissues, including skeletal muscle, bone, adipose, heart tissue and blood. By leveraging this understanding, Keros has discovered and is developing protein therapeutics that have the potential to provide meaningful and potentially disease-modifying benefit to patients. Keros' lead product candidate, rinvatercept, is being developed for the treatment of DMD and for the treatment of amyotrophic lateral sclerosis. Keros' most advanced product candidate, elritercept, is being developed for the treatment of cytopenias, including anemia and thrombocytopenia, in patients with myelodysplastic syndrome and in patients with myelofibrosis.

(In thousands, except share and per share data)

(Unaudited)

THREE MONTHS ENDED JUNE 30, | SIX MONTHS ENDED JUNE 30,
2026 | 2025 | 2026 | 2025
REVENUE:
Service and other revenue | — | 18,168 | 367 | 34,059
License revenue | — | — | — | 195,355
Total revenue | — | 18,168 | 367 | 229,414
OPERATING EXPENSES:
Research and development | (22,331) | (43,503) | (38,428) | (92,212)
General and administrative | (8,606) | (14,482) | (18,753) | (24,979)
Total operating expenses | (30,937) | (57,985) | (57,181) | (117,191)
INCOME (LOSS) FROM OPERATIONS | (30,937) | (39,817) | (56,814) | 112,223
OTHER INCOME (EXPENSE), NET
Dividend income | 2,287 | 7,120 | 4,622 | 13,912
Other expense, net | (60) | (221) | (226) | (559)
Total other income, net | 2,227 | 6,899 | 4,396 | 13,353
Income (loss) before income taxes | (28,710) | (32,918) | (52,418) | 125,576
Income tax (provision) benefit | — | 2,222 | — | (7,821)
Net income (loss) | (28,710) | (30,696) | (52,418) | 117,755
Net income (loss) attributable to common stockholders—basic and diluted | (28,710) | (30,696) | (52,418) | 117,755
Weighted-average shares of common stock outstanding — basic | 19,800,322 | 40,612,907 | 19,715,585 | 40,586,279
Weighted-average shares of common stock outstanding — diluted | 19,800,322 | 40,612,907 | 19,715,585 | 41,153,758
Net income (loss) per share of common stock — basic | (1.45) | (0.76) | (2.66) | 2.90
Net income (loss) per share of common stock — diluted | (1.45) | (0.76) | (2.66) | 2.86

KEROS THERAPEUTICS, INC.

Condensed Consolidated Balance Sheets

(In thousands, except share and per share data)

(Unaudited)

JUNE 30, 2026 | DECEMBER 31, 2025
ASSETS
CURRENT ASSETS:
Cash and cash equivalents | 257,606 | 287,415
Accounts receivable | — | 3,567
Prepaid expenses and other current assets | 7,027 | 22,202
Current income tax receivable | 2,250 | 2,250
Total current assets | 266,883 | 315,434
Operating lease right-of-use assets | 15,553 | 16,841
Property and equipment, net | 3,715 | 4,297
Restricted cash | 1,449 | 1,449
TOTAL ASSETS | 287,600 | 338,021
LIABILITIES AND STOCKHOLDERS' EQUITY
CURRENT LIABILITIES:
Accounts payable | 1,816 | 1,967
Current portion of operating lease liabilities | 2,597 | 2,408
Accrued expenses and other current liabilities | 7,740 | 16,039
Total current liabilities | 12,153 | 20,414
Operating lease liabilities, net of current portion | 13,127 | 14,475
Total liabilities | 25,280 | 34,889
STOCKHOLDERS' EQUITY:
Preferred stock, par value of $0.0001 per share; 10,000,000 shares authorized as of June 30, 2026 and December 31, 2025; no shares issued and outstanding | — | —
Series A junior participating preferred stock, par value of $0.0001 per share; 500,000 authorized as of June 30, 2026 and December 31, 2025; no shares issued and outstanding | — | —
Common stock, par value of $0.0001 per share; 200,000,000 shares authorized as of June 30, 2026 and December 31, 2025; 40,953,948 shares issued and 19,827,188 shares outstanding as of June 30, 2026 and 40,670,466 shares issued and 19,543,706 shares outstanding as of December 31, 2025 | 4 | 4
Treasury stock, at cost; 21,126,760 shares as of June 30, 2026 and December 31, 2025 | (384,558) | (384,558)
Additional paid-in capital | 1,181,057 | 1,169,451
Accumulated deficit | (534,183) | (481,765)
Total stockholders' equity | 262,320 | 303,132
TOTAL LIABILITIES AND STOCKHOLDERS' EQUITY | 287,600 | 338,021

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-04_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a clinical-stage biopharmaceutical company focused on developing and commercializing novel therapeutics to treat a wide range of patients with disorders that are linked to dysfunctional signaling of the transforming growth factor-beta, or TGF-ß, family of proteins. We are a leader in understanding the role of the TGF-ß family of proteins, which are master regulators of the growth, repair and maintenance of a number of tissues, including skeletal muscle, bone, adipose, heart tissue and blood. By leveraging this understanding, we have discovered and are developing protein therapeutics that have the potential to provide meaningful and potentially disease-modifying benefit to patients. Our lead product candidate, rinvatercept (KER-065), is being developed for the treatment of Duchenne muscular dystrophy and for the treatment of amyotrophic lateral sclerosis. Our most advanced product candidate, elritercept (KER-050), is being developed for the treatment of low blood cell counts, or cytopenias, including anemia and thrombocytopenia, in patients with myelodysplastic syndromes, or MDS, and in patients with myelofibrosis. In December 2024, we entered into an exclusive license agreement with Takeda Pharmaceuticals U.S.A., Inc., or Takeda, which became effective on January 16, 2025, to further develop, manufacture and commercialize elritercept worldwide outside of mainland China, Hong Kong and Macau.

Since our inception in 2015, we have devoted the majority of our efforts into business planning, research and development of our product candidates, including by conducting clinical trials and preclinical studies, raising capital and recruiting management and technical staff to support these operations. To date, we have not generated any revenue from product sales as none of our product candidates have been approved for commercialization. We have historically financed our operations primarily through the sale of convertible preferred stock and common stock and cash received from licensing agreements.

ATM Sales Agreement

In December 2022, we filed a prospectus supplement to our registration statement on Form S-3ASR with the Securities and Exchange Commission, or the SEC, for the issuance and sale, if any, of up to $250.0 million of shares of our common stock pursuant to a sales agreement with Leerink Partners LLC, or Leerink, as sales agent, which we refer to as the ATM Sales Agreement, under which we may offer and sell, from time to time, shares of our common stock, or the ATM Shares, through Leerink, which we refer to as the ATM Offering. In May 2024, we filed a new registration statement on Form S-3ASR, which we refer to as the New Shelf Registration Statement, to replace the prior shelf registration statement that was set to expire, including a base prospectus, which became effective immediately upon filing, under which we could issue an unspecified amount of shares of our common stock, preferred stock, debt securities and warrants. In June 2024, we filed a prospectus supplement to the New Shelf Registration Statement for the issuance and sale, if any, of up to an additional $350.0 million of shares of our common stock under the ATM Sales Agreement. As of the filing of our Annual Report on Form 10-K for the year ended December 31, 2024, we no longer qualified as a well-known seasoned issuer and therefore were not eligible to use the New Shelf Registration Statement as an automatic shelf registration statement, and no shares were sold during the year ended December 31, 2025.

Under the ATM Sales Agreement, Leerink may sell the ATM Shares by methods deemed to be an "at the market offering" as defined in Rule 415(a)(4) promulgated under the Securities Exchange Act of 1934, as amended. We may sell the ATM Shares in amounts and at times to be determined by us from time to time subject to the terms and conditions of the ATM Sales Agreement, but we have no obligation to sell any of the ATM Shares in the ATM Offering. As of December 31, 2025, we have sold a total of 4,290,096 shares of our common stock pursuant to the ATM Offering for aggregate net proceeds of approximately $228.6 million after deducting sales agent commissions and estimated offering expenses. As of December 31, 2025, we may not offer and sell any ATM shares.

January 2024 Public Offering of Common Stock

On January 8, 2024, we closed an underwritten public offering in which we issued and sold 4,025,000 shares of common stock, which included 525,000 shares of common stock issued and sold pursuant to the full exercise of the underwriters' option to purchase additional shares, at a public offering price of $40.00 per share. The aggregate net proceeds to us from the public offering were approximately $151.1 million, after deducting underwriting discounts and commissions and estimated offering expenses.

October 2025 Share Repurchases

On October 15, 2025, we entered into the Repurchase Agreements with the ADAR1 Parties and the Pontifax Parties. Pursuant to the terms and conditions of the Repurchase Agreements, the ADAR1 Parties and the Pontifax Parties sold all of the shares of our common stock beneficially owned by them, being an aggregate of 10,176,595 shares of common stock, to us at a per share purchase price of $17.75 per share, for an aggregate purchase price of $180.6 million. In addition, concurrently with the execution of the Pontifax Repurchase Agreement, each of Tomer Kariv and Ran Nussbaum resigned from our board of directors and all committees thereof.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Comparison for the years ended December 31, 2025 and 2024

The following table summarizes our results of operations for the years ended December 31, 2025 and 2024 (in thousands):

YEAR ENDED DECEMBER 31,
2025 | 2024
REVENUE:
Service and other revenue | 38,706 | 550
License revenue | 205,355 | 3,000
Total revenue | 244,061 | 3,550
OPERATING EXPENSES:
Research and development | (129,643) | (173,629)
General and administrative | (46,849) | (40,754)
Total operating expenses | (176,492) | (214,383)
INCOME (LOSS) FROM OPERATIONS | 67,569 | (210,833)
OTHER INCOME (EXPENSE), NET:
Research and development incentive income | — | 1,238
Dividend income | 24,867 | 23,496
Other expense, net | (539) | (954)
Total other income, net | 24,328 | 23,780
Income (loss) before income taxes | 91,897 | (187,053)
Income tax provision | (4,883) | (300)
Net income (loss) | 87,014 | (187,353)

Revenue

We recognized $205.4 million of license revenue related to the upfront payment and achievement of a development milestone under the Takeda Agreement and $38.5 million of service and other revenue related to the transition services agreement with Takeda, or the TSA, for the year ended December 31, 2025, compared to zero for the year ended December 31, 2024. In connection with the Hansoh Agreement, we recognized $0.2 million of service and other revenue for the year ended December 31, 2025, compared to $3.0 million of license revenue and $0.5 million of service and other revenue for the year ended December 31, 2024.

Research and Development Expenses

The following table summarizes our research and development expenses for the years ended December 31, 2025 and 2024 (in thousands):

YEAR ENDED DECEMBER 31, | $ CHANGE
2025 | 2024 | 2025 vs 2024
Rinvatercept | 7,081 | 16,090 | (9,009)
Elritercept | 38,030 | 44,319 | (6,289)
Cibotercept | 12,562 | 29,777 | (17,215)
Preclinical and development fees | 6,847 | 12,008 | (5,161)
Personnel expenses (including stock-based compensation) | 47,647 | 55,946 | (8,299)
Professional fees | 6,474 | 5,083 | 1,391
Facilities and supplies | 8,947 | 7,832 | 1,115
Other expenses | 2,055 | 2,574 | (519)
129,643 | 173,629 | (43,986)

Research and development expenses were $129.6 million for the year ended December 31, 2025, compared to $173.6 million for the year ended December 31, 2024. The decrease of $44.0 million was primarily due to a decrease in program-related costs, including (i) a $9.0 million decrease of rinvatercept-related expenses, which was driven by a net decrease of $7.8 million in manufacturing and preclinical activities and a $1.2 million decrease in clinical spend associated with our completed Phase 1 clinical trial; (ii) a net decrease of $6.3 million in elritercept-related expenses, primarily driven by a decrease of $8.4 million in clinical spend associated with our ongoing Phase 2 clinical trials, one in patients with MDS and

one in patients with myelofibrosis, and the advancement of the Phase 3 RENEW clinical trial, as clinical activities transitioned to Takeda during 2025, partially offset by an increase of $2.1 million in manufacturing activities; (iii) a $17.2 million decrease of cibotercept-related expenses, primarily driven by a $9.5 million decrease in clinical spend associated with our terminated Phase 2 clinical trial and a net decrease of $7.7 million in manufacturing and preclinical activities; (iv) a $5.2 million decrease in preclinical pipeline and development activities; and (v) a $8.3 million decrease in personnel costs, including a decrease of $5.0 million of stock-based compensation costs, driven by a reduction in headcount. These decreases were partially offset by (a) a $1.4 million increase in professional fees and (b) a net increase of $0.6 million in facilities and supplies and other expenses.

General and Administrative Expenses

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-04_item1_business.md)

ITEM 1. BUSINESS

Overview

We are a clinical-stage biopharmaceutical company focused on developing and commercializing novel therapeutics to treat a wide range of patients with disorders that are linked to dysfunctional signaling of the transforming growth factor-beta, or TGF-ß, family of proteins. We are a leader in understanding the role of the TGF-ß family of proteins, which are master regulators of the growth, repair and maintenance of a number of tissues, including skeletal muscle, bone, adipose, heart tissue and blood. By leveraging this understanding, we have discovered and are developing protein therapeutics that have the potential to provide meaningful and potentially disease-modifying benefit to patients. Our lead product candidate, rinvatercept (KER-065), is being developed for the treatment of neuromuscular diseases. Our most advanced product candidate, elritercept (KER-050), is being developed for the treatment of low blood cell counts, or cytopenias, including anemia and thrombocytopenia, in patients with myelodysplastic syndromes, or MDS, and in patients with myelofibrosis. In December 2024, we entered into an exclusive license agreement with Takeda Pharmaceuticals U.S.A., Inc., or Takeda, to further develop, manufacture and commercialize elritercept worldwide outside of mainland China, Hong Kong and Macau, which became effective on January 16, 2025.

Rinvatercept is designed to bind to and inhibit TGF-ß ligands, including myostatin (GDF8) and activin A, which are negative regulators of muscle and bone mass and strength. Through inhibition of these TGF-ß ligands, we believe that rinvatercept has the potential to increase skeletal muscle regeneration, increase muscle size and strength, reduce body fat, reduce fibrosis of the skeletal muscle and increase bone strength. We are developing rinvatercept for the treatment of Duchenne muscular dystrophy, or DMD and for the treatment of amyotrophic lateral sclerosis, or ALS. In March 2025, we announced initial topline results from the Phase 1 clinical trial of rinvatercept in healthy adult volunteers. We expect to commence a Phase 2 clinical trial of rinvatercept in patients with DMD in the second quarter of 2026. We also plan to engage regulators on the design of a Phase 2 clinical trial of rinvatercept in patients with ALS in the second half of 2026.

Elritercept is an engineered ligand trap comprised of a modified ligand-binding domain of the TGF-ß receptor known as activin receptor type IIA, or ActRIIA, that is fused to the portion of the human antibody known as the Fc domain. Elritercept is designed to increase red blood cell and platelet production by inhibiting the signaling of a subset of the TGF-ß family of proteins to promote hematopoiesis. We believe elritercept has the potential to provide benefit to patients suffering from red blood cell and platelet differentiation and maturation defects occurring across the spectrum from early through terminal stages of hematopoiesis, and consequently may be effective for many patients that have limited treatment options or are refractory to available therapies. In July 2025, we announced that the first patient was dosed in the placebo-controlled Phase 3 RENEW clinical trial in patients with very low-, low-, or intermediate-risk MDS, which we refer to as lower-risk MDS. The dosing of the first patient triggered a $10 million milestone payment to us under the license agreement with Takeda.

Our strategy focuses on the role of members of the TGF-ß family of proteins in the development of a number of tissues, including skeletal muscle, bone, adipose, heart tissue and blood. Aged and damaged cells are routinely replaced by new cells in normally functioning organs. These new cells are derived from stem cells that have the ability to differentiate into cells with specialized functions when appropriate signals are provided to maintain the homeostatic state of the tissue. Members of the TGF-ß family of proteins, including activins and bone morphogenic proteins (BMPs), provide the necessary signals for this process of self-renewal and repair.

We seek to address the limitations of current therapeutic approaches to treating diseases whose manifestations are linked to dysfunction of TGF-ß signaling pathways by:

• leveraging our comprehensive insights into the TGF-ß signaling pathways to discover therapeutics to treat disorders that are linked to dysfunctional TGF-ß signaling;

• expanding our library of proprietary molecules that are engineered to induce desired biological effects, such as increased muscle mass and strength, increased muscle regeneration, improved muscle quality and reduced tissue fat, improved bone mineral density, reduced inflammation, reduced fibrosis and modulated blood cell production;

• engineering proprietary molecules to selectively target specific proteins in the TGF-ß signaling pathways to provide therapeutic benefit while potentially minimizing safety risks;

• developing product candidates for the treatment of diseases where targeting the TGF-ß signaling pathways has clinical validation or biological rationale to improve our probability of success in the clinic; and

• targeting the TGF-ß family of proteins, which are highly conserved throughout evolution, permitting the use of animal models to potentially predict with high confidence the therapeutic benefit in patients.

We are led by a highly experienced management team and scientific advisory board who have significant experience and expertise researching and developing therapeutics in targeting the TGF-ß family of proteins. Our team has collectively worked on marketed therapeutics such as Reblozyl and Winrevair, and led drug discovery at companies including Acceleron Pharma Inc. (which was acquired by Merck & Co. Inc. in November 2021) and Wyeth Pharmaceuticals Inc.

Our Pipeline

The following table sets forth our product candidates and their current development stages:

[NTD:

Our Strategy

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-04_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-04_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-04_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-03-04_item7_mdna.md, 10-K_2026-03-04_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
