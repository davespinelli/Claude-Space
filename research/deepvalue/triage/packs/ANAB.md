# Triage pack — ANAB · ANAPTYSBIO, INC

_Generated 2026-09-04 19:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ANAB · **Name:** ANAPTYSBIO, INC
- **CIK:** 0001370053
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ANAB

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ANAPTYSBIO, INC
- **CIK:** 1,370,053 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 57.46 |
| mktcap | $1.7B |
| ev | $1.4B |
| ev_ebit | 29.7x |
| fcf | $19.6M |
| fcf_yield | 1.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$248.5M |
| net_debt_ebit | -5.2x |
| cash | $248.5M |
| ltd | $0.00 |
| equity | $12.7M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $234.6M |
| revenue_prior | $91.3M |
| rev_growth | 157.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $47.9M |
| net_income | -$13.2M |
| cfo | $19.7M |
| capex | $87k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 3.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 29,100,902 |
| shares_py | 27,996,963 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 266.1% |
| r6m | 50.5% |
| off_52w_high | -17.7% |
| adv20 | $22.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.26 |
| r_ev_ebit | 0.29 |
| r_roic | 0.50 |
| r_rev_growth | 0.99 |
| r_buyback | 0.22 |
| score | 0.50 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q1I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 242 |

**Screen rationale:** revenue +157.0%; debt data missing (net cash unverified); 12-1 momentum 266.1%


## 3. Share count trend

- Shares outstanding: **29,100,902** (CY2026Q1I) vs **27,996,963** prior year (CY2025Q2I)
- Change: **3.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-22** — Item 1.01 (Entry into a Material Definitive Agreement): On June 15, 2026, AnaptysBio, Inc. (the "Company"), entered into a Sublease Agreement (the "Sublease") with First Tracks Biotherapeutics, Inc., a Delaware corporation ("First Tracks"), pursuant to which the Company agreed to sublease to First Tracks...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 75 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 37 |
| D | 32 |
| M | 6 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-12_2-02-results.md)

_Extraction: started at the first release heading, 'SAN DIEGO, CA — May 12, 2026 — AnaptysBio, Inc. (Nasdaq: ANAB), a comp'; skipped 7 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (anab-ex99_1.htm)

SAN DIEGO, CA — May 12, 2026 — AnaptysBio, Inc. (Nasdaq: ANAB), a company focused on managing the financial collaborations for Jemperli with GSK and imsidolimab with Vanda, today reported financial results for the first quarter ended March 31, 2026, and provided a business update.

"Following the completion of the spin-off of First Tracks Bio in late April, Anaptys now exclusively manages the financial collaborations for Jemperli and imsidolimab, with streamlined operations requiring limited FTEs, minimal operating expenses and delivering an EBIT margin greater than 95%," said Daniel Faga, president and chief executive officer. "With Chris Murphy joining as CFO, who brings deep business development and investment banking experience, our priority continues to be to protect our two royalty streams and return their value to shareholders."

GSK Jemperli Financial Collaboration

•
GSK announced strong commercial performance for Jemperli ($313 million/£232 million in Q1 2026 sales, with >40% year-over-year growth 1 )

•
Anaptys continues to expect to achieve >$390 million in annualized Jemperli royalties payable to Anaptys as early as 2029 at GSK's peak sales guidance of >$2.7 billion 2

•
Anaptys estimates Sagard will have accrued ~$275 million in royalties and sales milestones through Q1 2026 and anticipates paydown of the remaining ~$325 million non-recourse debt monetization by the end of Q2 2027 3

•
Substantial GSK investment in additional monotherapy and potential combination trials for Jemperli, including:

o
AZUR-1 – pivotal Phase 2 – dostarlimab monotherapy in untreated stage II/III dMMR/MSI-H locally advanced rectal cancer

▪
Data expected in H2 2026; U.S. FDA Breakthrough Therapy Designation

▪
Received an FDA Commissioner's National Priority Voucher (CNPV) in Nov. 2025 allowing for only a one to two-month sBLA review timeline for US FDA approval

o
AZUR-2 – pivotal Phase 3 – dostarlimab versus standard of care in untreated TN40 or stage III dMMR/ MSI-H resectable colon cancer

▪
Data expected in 2028

o
AZUR-4 – Phase 2 – dostarlimab plus chemotherapy versus standard of care (chemotherapy) in untreated stage III MMRp/MSS resectable colon cancer

▪
Data expected in Q4 2026

o
JADE – pivotal Phase 3 – dostarlimab monotherapy versus placebo in locally advanced unresected head and neck squamous cell carcinoma (PD-L1 CPS≥1) post chemoradiation

▪
Data expected in 2028

Vanda Imsidolimab Financial Collaboration

•
FDA target action date (PDUFA) of Dec. 12, 2026 for imsidolimab in generalized pustular psoriasis (GPP)

Recent Leadership and Board of Directors Appointments

•
Announced appointment of Chris Murphy as Chief Financial Officer (CFO)

o
Mr. Murphy brings >20 years' experience in business development, commercial operations, corporate strategy and investment banking in the biopharmaceutical industry

•
Announced appointment of industry veterans Susannah Gray and Owen Hughes to Board of Directors

o
Ms. Gray brings >25 years' experience in both finance and investment banking in the biopharmaceutical industry, formerly CFO of Royalty Pharma

o
Mr. Hughes brings >25 years' experience as both an operator and investor in the biopharmaceutical industry, currently leading XOMA Royalty as CEO

Stock Repurchase Plan

•
Announced a $100.0 million Stock Repurchase Plan in March 2026. It will expire on Dec. 31, 2026, may be suspended or discontinued at any time, and does not obligate the company to acquire any amount of common stock

First Quarter Financial Results

•
The separation of Anaptys and First Tracks Bio was completed on April 20, 2026. As a result, in the first quarter of 2026, the financial results include assets, liabilities and expenses related to both companies. Beginning in the second quarter of 2026, Anaptys expects to reclassify historical First Tracks Bio related assets, liabilities and expenses as discontinued operations.

•
Cash, cash equivalents and investments totaled $286.5 million as of March 31, 2026, compared to $311.6 million as of Dec. 31, 2025, for a decrease of $25.1 million due primarily to operating activities offset by $14.0 million received from stock option exercises.

•
Collaboration revenue was $25.6 million for the three months ended March 31, 2026, compared to $27.8 million for the three months ended March 31, 2025. The decrease in revenue was primarily due to $9.7 million in revenue recognized for the Vanda license agreement for the three months ended March 31, 2025 offset by Jemperli royalties increasing 44% from $17.2 million to $24.7 million for the three months ended March 31, 2026.

•
Research and development expenses were $34.0 million for the three ended March 31, 2026, compared to $41.2 million for the three months ended March 31, 2025. The decrease for the three months ended March 31, 2026 was primarily due to decreased development costs for rosnilimab and ANB032 offset by increased costs relating to the phase 1 trials for ANB033. The R&D non-cash, stock-based compensation expense was $4.6 million for the three months ended March 31, 2026 as compared to $4.4 million in the same period in 2025.

•
General and administrative expenses were $26.2 million for the three months ended March 31, 2026, compared to $14.1 million for the three months ended March 31, 2025. The increase was due primarily to legal costs for the separation of the company, ongoing GSK litigation and non-cash stock compensation costs incurred for our

former Chief Financial Officer and former Chief Legal Officer. The G&A non-cash, stock-based compensation expense was $9.7 million for the three months ended March 31, 2026 as compared to $4.8 million in the same period in 2025.

•
Net loss was $52.9 million for the three months ended March 31, 2026, or a net loss per share of $1.84, compared to a net loss of $39.3 million for the three months ended March 31, 2025, or a net loss per share of $1.28.

About AnaptysBio

Anaptys manages the financial collaborations for Jemperli with GSK and imsidolimab with Vanda, with a focus on protecting and returning the value of its royalties to shareholders. To learn more, visit www.AnaptysBio.com or follow us on LinkedIn .

2.
CEO Emma Walmsley, 2025 JP Morgan CEO Series fireside chat, 9/11/2025, "there's no change to our peak year sales overall ambition for Jemperli, that's for sure, which is far more than £2 billion." ; Converted from GBP to USD using Q3 2025 average exchange rate (1.35x)

3.
~$275 million accrued to Sagard through Q1 2026 and assumes a ~10% quarter-over-quarter growth rate for Jemperli from Q4'25 through Q2'27 and milestone payments associated with filing ($5mm) and approval ($10mm) of dMMR rectal approval in the EU

AnaptysBio, Inc.

Consolidated Balance Sheets

(in thousands, except par value data)

(unaudited)

March 31, 2026 | December 31, 2025
ASSETS
Current assets:
Cash and cash equivalents | 248,469 | 238,196
Receivables from collaborative partners | 25,747 | 33,850
Short-term investments | 37,986 | 73,442
Prepaid expenses and other current assets | 3,907 | 4,762
Total current assets | 316,109 | 350,250
Property and equipment, net | 1,280 | 1,370
Operating lease right-of-use assets | 12,039 | 12,519
Other long-term assets | 256 | 256
Total assets | 329,684 | 364,395
LIABILITIES AND STOCKHOLDERS' EQUITY
Current liabilities:
Accounts payable | 7,517 | 3,871
Accrued expenses | 32,065 | 32,674
Current portion of operating lease liability | 2,120 | 2,080
Total current liabilities | 41,702 | 38,625
Liability related to sale of future royalties | 263,742 | 276,528
Operating lease liability, net of current portion | 11,493 | 12,032
Stockholders' equity:
Preferred stock, $0.001 par value, 10,000 shares authorized and no shares, issued or outstanding at March 31, 2026 and December 31, 2025, respectively | — | —
Common stock, $0.001 par value, 500,000 shares authorized, 29,031 shares and 28,019 shares issued and outstanding at March 31, 2026 and December 31, 2025, respectively | 29 | 28
Additional paid-in capital | 838,307 | 809,765
Accumulated other comprehensive loss | (146 | (24
Accumulated deficit | (825,443 | (772,559
Total stockholders' equity | 12,747 | 37,210
Total liabilities and stockholders' equity | 329,684 | 364,395

AnaptysBio, Inc.

Consolidated Statements of Operations and Comprehensive Loss

(in thousands, except per share data)

(unaudited)

Three Months Ended March 31,
2026 | 2025
Collaboration revenue | 25,556 | 27,771
Operating expenses:
Research and development | 33,991 | 41,180
General and administrative | 26,202 | 14,130
Total operating expenses | 60,193 | 55,310
Loss from operations | (34,637 | (27,539
Other income (expense), net:
Interest income | 2,653 | 4,413
Non-cash interest expense for the sale of future royalties | (20,859 | (18,061
Other (expense) income, net | (1 | 1,902
Total other expense, net | (18,207 | (11,746
Loss before income taxes | (52,844 | (39,285
Provision for income taxes | (40 | (44
Net loss | (52,884 | (39,329
Other comprehensive loss:
Unrealized loss on available-for-sale securities | (122 | (144
Comprehensive loss | (53,006 | (39,473
Net loss per common share:
Basic and diluted | (1.84 | (1.28
Weighted-average number of shares outstanding:
Basic and diluted | 28,691 | 30,644

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-03_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a clinical-stage biotechnology company focused on delivering innovative immunology therapeutics for autoimmune and inflammatory diseases. Our clinical-stage pipeline includes rosnilimab, a selective pathogenic T cell depleter, for which we completed a Phase 2b trial for the treatment of moderate-to-severe rheumatoid arthritis ("RA"), ANB033, a CD122 antagonist, in a Phase 1b trial for celiac disease ("CeD") and eosinophilic esophagitis ("EoE"), and ANB101, a BDCA2 modulator, in a Phase 1a trial. We also discovered and out-licensed, in financial collaborations, multiple therapeutic antibodies, including a PD-1 antagonist (Jemperli (dostarlimab-gxly) or "Jemperli") to GSK and an IL-36R antagonist (imsidolimab) to Vanda Pharmaceuticals Inc. ("Vanda"). We currently recognize revenue from milestones and royalties achieved under our immuno-oncology collaboration with GSK and license and transition services revenue from our collaboration with Vanda.

Intention to Separate Company

In September 2025, we announced that our board of directors ("Board of Directors") approved plans to explore separating our business into two independent, publicly traded companies. One company is expected to hold and continue to manage the financial collaboration for Jemperli from GSK and for imsidolimab from Vanda, with a focus on protecting and returning value of the royalties to its shareholders. The other company is expected to be a clinical-stage biotechnology company focused on the development and potential commercialization of innovative therapeutics for autoimmune and inflammatory diseases, including rosnilimab, ANB033 and ANB101. Upon completion of the proposed separation, which we expect to complete in the second quarter of 2026, we intend to launch the clinical-stage biotechnology company with adequate capital to fund operations for at least twelve months after the date the proposed separation is completed. While the proposed separation is anticipated to be a taxable event, we are focused on minimizing overall corporate and shareholder-level taxes across the entire transaction. Completion of the proposed separation is subject to final approval by our Board of Directors and other customary conditions, including the effectiveness of a registration statement with the Securities and Exchange Commission (the "SEC").

Our Wholly Owned Clinical-Stage Pipeline

Our antibodies are in development to treat inflammatory diseases. We believe these molecules have potential applicability across a broad range of autoimmune and inflammatory diseases, including in gastroenterology, rheumatology, dermatology, respiratory, and other therapeutic areas.

Rosnilimab

Rosnilimab is an IgG1 antibody that directly targets pathogenic T cells, such as activated Tph/Tfh and T effector cells, in the periphery or inflamed tissue. These T cells, when activated, proliferate and migrate, and secrete the inflammatory cytokines that are the drivers of autoimmune and inflammatory diseases. Rosnilimab is designed to selectively deplete pathogenic T cells in both inflamed tissue and the periphery while sparing non-pathogenic T cells, including naïve T cells, to preserve overall immune function and restore immune homeostasis. This drives specific immunological outcomes, such as a reduction in T cell proliferation, migration and cytokine secretion, and a reduction of plasma cell generation and autoantibody levels. We announced top-line data from a healthy volunteer Phase 1 trial of rosnilimab in November 2021 that supported advancement of rosnilimab into subsequent patient trials. A total of 144 subjects were enrolled in the randomized, double-blind, placebo-controlled healthy volunteer Phase 1 trial, where single ascending dose ("SAD") cohorts received subcutaneous ("SC") or intravenous ("IV") single doses of rosnilimab up to 600mg or placebo, while multiple ascending dose ("MAD") cohorts received four weekly subcutaneous doses of rosnilimab ranging up to 400mg or placebo. Rosnilimab was generally well-tolerated and no dose-limiting toxicities were observed. Rosnilimab demonstrated a sustained systemic exposure and dose-proportionality with an estimated two-week half-life for subcutaneous and IV routes of administration.

In February 2025, we announced initial data, which was subsequently updated in June 2025, from rosnilimab's randomized, placebo-controlled, global 424-patient, Phase 2b clinical trial for moderate-to-severe rheumatoid arthritis. Patients were randomized to receive either 100mg of subcutaneous rosnilimab every four weeks (Q4W), 400mg Q4W, 600mg every two weeks, or placebo.

During the three-month placebo-controlled period, the trial achieved its primary endpoint by observing the reduction of disease activity using the disease activity score, 28 joints (DAS-28) C-Reactive Protein ("CRP") score, as well as ACR20 response (an accepted Phase 3 registrational endpoint), at Week 12 in all three doses of rosnilimab compared to placebo. Rosnilimab achieved its secondary endpoint by demonstrating statistical significance in at least one dose and numerical superiority at all doses, including once monthly administration, on ACR20, ACR50 and with respect to the clinical disease activity index ("CDAI") low disease activity ("LDA") score at Week 12. Specifically, at Week 12, ACR20 achieved statistical significance at 100 mg (p < 0.05), 400 mg (p < 0.01), and 600 mg (p < 0.001); ACR50 achieved statistical significance at 600 mg (p < 0.05); and CDAI LDA achieved statistical significance at 100 mg (p < 0.05) and 400 mg (p < 0.01).

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Collaboration Revenue

Collaboration revenue was $234.6 million for the year ended December 31, 2025, compared to $91.3 million for the year ended December 31, 2024. A comparison of collaboration revenue is as follows:

Year Ended December 31,
(in thousands) | 2025 | 2024 | Increase
GSK Milestone Revenue | 75,000 | — | 75,000
GSK Milestone Revenue (non-cash) | 50,000 | 40,000 | 10,000
GSK Royalty Revenue - Jemperli (non-cash) | 95,945 | 47,381 | 48,564
GSK Royalty Revenue - Zejula (non-cash) | 3,917 | 3,899 | 18
Vanda License and Transition Services Revenue | 9,741 | — | 9,741
Total collaboration revenue | 234,603 | 91,280 | 143,323

Collaboration revenue during the year ended December 31, 2025 increased $143.3 million compared to the year ended December 31, 2024 due to an increase of $85.0 million in Jemperli sales milestones, $48.6 million increase in Jemperli and Zejula royalty revenue and $9.7 million increase in Vanda license and transition services revenue.

We expect that any collaboration revenue we generate will continue to fluctuate from period to period as a result of the timing and amount of milestones and royalties from our existing collaborations.

Research and Development Expenses

Research and development expenses were $136.0 million during the year ended December 31, 2025 compared to $163.8 million during the year ended December 31, 2024, for a decrease of $27.8 million. The decrease is primarily attributable to a $21.6 million decrease in clinical expenses and a decrease of $12.0 million in outside services for manufacturing expenses, offset by a $5.5 million increase in salaries and related costs, including a $2.3 million increase in stock compensation expense and a decrease of $0.6 million in recruiting costs, and a $0.9 million increase in other research and development expenses.

We do not track fully burdened research and development costs separately for each of our product candidates. We review our research and development expenses by focusing on external development and internal development costs. External development expenses consist of costs associated with our external preclinical and clinical trials, including pharmaceutical development and manufacturing. Included in preclinical and other unallocated costs are external corporate overhead costs that are not specific to any one program. Internal costs consist of salaries and wages, stock-based compensation and benefits, which are not tracked by product

candidate as several of our departments support multiple product candidate research and development programs. The following table summarizes the external costs attributable to each program and internal costs:

Year Ended December 31,
(in thousands) | 2025 | 2024 | Increase/(Decrease)
External Costs
Rosnilimab | 42,744 | 53,422 | (10,678
ANB033 | 20,427 | 12,460 | 7,967
ANB101 | 8,138 | 3,367 | 4,771
ANB032 | 48 | 26,084 | (26,036
Imsidolimab | (2,273 | 8,284 | (10,557
Preclinical and other unallocated costs | 16,093 | 14,350 | 1,743
Total External Costs | 85,177 | 117,967 | (32,790
Internal Costs
Salaries and wages | 33,658 | 30,424 | 3,234
Stock compensation | 17,135 | 14,823 | 2,312
Other internal costs | — | 626 | (626
Total Internal Costs | 50,793 | 45,873 | 4,920
Total Costs | 135,970 | 163,840 | (27,870

General and Administrative Expenses

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-03_item1_business.md)

Item 1. Busi ness

Overview

We are a clinical-stage biotechnology company focused on delivering innovative immunology therapeutics for autoimmune and inflammatory diseases. Our clinical-stage pipeline includes rosnilimab, a selective pathogenic T cell depleter, for which we completed a Phase 2b trial for the treatment of moderate-to-severe rheumatoid arthritis ("RA"), ANB033, a CD122 antagonist, in a Phase 1b trial for celiac disease ("CeD") and eosinophilic esophagitis ("EoE"), and ANB101, a BDCA2 modulator, in a Phase 1a trial. We also discovered and out-licensed, in financial collaborations, multiple therapeutic antibodies, including a PD-1 antagonist (Jemperli (dostarlimab-gxly) or "Jemperli") to GSK and an IL-36R antagonist (imsidolimab) to Vanda Pharmaceuticals Inc. ("Vanda"). We currently recognize revenue from milestones and royalties achieved under our immuno-oncology collaboration with GSK and license and transition services revenue from our collaboration with Vanda.

Intention to Separate Company

In September 2025, we announced that our board of directors ("Board of Directors") approved plans to explore separating our business into two independent, publicly traded companies. One company is expected to hold and continue to manage the financial collaboration for Jemperli from GSK and for imsidolimab from Vanda, with a focus on protecting and returning value of the royalties to its shareholders. The other company is expected to be a clinical-stage biotechnology company focused on the development and potential commercialization of innovative therapeutics for autoimmune and inflammatory diseases, including rosnilimab, ANB033 and ANB101. Upon completion of the proposed separation, which we expect to complete in the second quarter of 2026, we intend to launch the clinical-stage biotechnology company with adequate capital to fund operations for at least twelve months after the date the proposed separation is completed. While the proposed separation is anticipated to be a taxable event, we are focused on minimizing overall corporate and shareholder-level taxes across the entire transaction. Completion of the proposed separation is subject to final approval by our Board of Directors and other customary conditions, including the effectiveness of a registration statement with the Securities and Exchange Commission (the "SEC").

Our Wholly Owned Clinical-Stage Pipeline

Our antibodies are in development to treat inflammatory diseases. We believe these molecules have potential applicability across a broad range of autoimmune and inflammatory diseases, including in gastroenterology, rheumatology, dermatology, respiratory, and other therapeutic areas.

Rosnilimab

Rosnilimab is an IgG1 antibody that directly targets pathogenic T cells, such as activated Tph/Tfh and T effector cells, in the periphery or inflamed tissue. These T cells, when activated, proliferate and migrate, and secrete the inflammatory cytokines that are the drivers of autoimmune and inflammatory diseases. Rosnilimab is designed to selectively deplete pathogenic T cells in both inflamed tissue and the periphery while sparing non-pathogenic T cells, including naïve T cells, to preserve overall immune function and restore immune homeostasis. This drives specific immunological outcomes, such as a reduction in T cell proliferation, migration and cytokine secretion, and a reduction of plasma cell generation and autoantibody levels. We announced top-line data from a healthy volunteer Phase 1 trial of rosnilimab in November 2021 that supported advancement of rosnilimab into subsequent patient trials. A total of 144 subjects were enrolled in the randomized, double-blind, placebo-controlled healthy volunteer Phase 1 trial, where single ascending dose ("SAD") cohorts received subcutaneous ("SC") or intravenous ("IV") single doses of rosnilimab up to 600mg or placebo, while multiple ascending dose ("MAD") cohorts received four weekly subcutaneous doses of rosnilimab ranging up to 400mg or placebo. Rosnilimab was generally well-tolerated and no dose-limiting toxicities were observed. Rosnilimab demonstrated a sustained systemic exposure and dose-proportionality with an estimated two-week half-life for subcutaneous and IV routes of administration.

In February 2025, we announced initial data, which was subsequently updated in June 2025, from rosnilimab's randomized, placebo-controlled, global 424-patient, Phase 2b clinical trial for moderate-to-severe rheumatoid arthritis. Patients were randomized to receive either 100mg of subcutaneous rosnilimab every four weeks (Q4W), 400mg Q4W, 600mg every two weeks, or placebo.

During the three-month placebo-controlled period, the trial achieved its primary endpoint by observing the reduction of disease activity using the disease activity score, 28 joints (DAS-28) C-Reactive Protein ("CRP") score, as well as ACR20 response (an accepted Phase 3 registrational endpoint), at Week 12 in all three doses of rosnilimab compared to placebo. Rosnilimab achieved its secondary endpoint by demonstrating statistical significance in at least one dose and numerical superiority at all doses, including once monthly administration, on ACR20, ACR50 and with respect to the clinical disease activity index ("CDAI") low disease activity ("LDA") score at Week 12. Specifically, at Week 12, ACR20 achieved statistical significance at 100 mg (p < 0.05), 400 mg (p < 0.01), and 600 mg (p < 0.001); ACR50 achieved statistical significance at 600 mg (p < 0.05); and CDAI LDA achieved statistical significance at 100 mg (p < 0.05) and 400 mg (p < 0.01).

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-03_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-03_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-03_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-12_2-02-results.md, 10-K_2026-03-03_item7_mdna.md, 10-K_2026-03-03_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
