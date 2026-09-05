# Triage pack — ASMB · ASSEMBLY BIOSCIENCES, INC.

_Generated 2026-09-05 00:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ASMB · **Name:** ASSEMBLY BIOSCIENCES, INC.
- **CIK:** 0001426800
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ASMB

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ASSEMBLY BIOSCIENCES, INC.
- **CIK:** 1,426,800 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

> **EARNINGS QUALITY FLAG — one-off items likely.**
> revenue growth above 50% alongside share count growth above 15% (bought, not organic).
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 36.13 |
| mktcap | $735.6M |
| ev | $703.3M |
| ev_ebit | n/a |
| fcf | -$41.2M |
| fcf_yield | -5.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -3.5% |
| net_debt | -$32.3M |
| net_debt_ebit | n/a |
| cash | $32.3M |
| ltd | $0.00 |
| equity | $305.6M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $72.3M |
| revenue_prior | $28.5M |
| rev_growth | 153.5% |
| rev_growth_note | share count +165.4% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | revenue growth above 50% alongside share count growth above 15% (bought, not organic) |
| ebit | -$12.1M |
| net_income | -$6.1M |
| cfo | -$41.1M |
| capex | $66k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 165.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 20,360,596 |
| shares_py | 7,672,261 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 11.0% |
| r6m | 30.6% |
| off_52w_high | -6.2% |
| adv20 | $10.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.11 |
| r_ev_ebit | 0.00 |
| r_roic | 0.22 |
| r_rev_growth | 0.99 |
| r_buyback | 0.00 |
| score | 0.31 |

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
| rank | 397 |

**Screen rationale:** revenue +153.5% BUT share count +165.4% yoy — growth may be acquisition/issuance-driven, not organic; debt data missing (net cash unverified); 12-1 momentum 11.0%; EARNINGS QUALITY: revenue growth above 50% alongside share count growth above 15% (bought, not organic) — one-off items likely


## 3. Share count trend

- Shares outstanding: **20,360,596** (CY2026Q2I) vs **7,672,261** prior year (CY2025Q2I)
- Change: **165.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +165.4% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-05** — Item 5.02 (officer / director change or comp arrangement): Amendment No. 3 to Amended and Restated 2018 Stock Incentive Plan
- **2026-05-26** — Item 1.01 (Entry into a Material Definitive Agreement): On May 21, 2026, Assembly Biosciences, Inc. (the "Company") entered into an underwriting agreement (the "Underwriting Agreement") with Guggenheim Securities, LLC ("Guggenheim Securities") and UBS Securities LLC, as representatives of the several underwriters...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 29 sh / $674 -> net $-674 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 11 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-14_2-02-results.md)

_Extraction: started at the first release heading, 'Assembly Biosciences Reports Second Quarter 2026 Financial Results and'; skipped 9 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (asmb-ex99_1.htm)

Assembly Biosciences Reports Second Quarter 2026 Financial Results and Recent Updates

– Expanded ABI-6250 clinical development into cholestatic liver diseases, including primary biliary cholangitis (PBC) and primary sclerosing cholangitis (PSC) –

– Completed $115 million gross financing to support advancement of pipeline programs through key development milestones –

– GS-1179 (formerly ABI-1179) selected to advance in HSV HPI program, with Phase 2 initiation expected by year-end 2026 –

– Cash runway projected into 2029, including first $75 million Gilead collaboration extension payment due in Q4 2026 –

SOUTH SAN FRANCISCO, Calif. – August 13, 2026 – Assembly Biosciences, Inc. (Nasdaq: ASMB), a biotechnology company developing innovative therapeutics targeting serious viral and liver diseases, today reported financial results for the second quarter ended June 30, 2026, and recent business updates.

"During the second quarter, we advanced several important strategic priorities, including expanding ABI-6250 into cholestatic liver diseases and strengthening our balance sheet through a successful financing to support the continued advancement of our pipeline," said Jason Okazaki, chief executive officer and president of Assembly Bio. "We were also pleased to receive Gilead's clinical development plan for the HSV helicase primase inhibitor program, which includes plans for GS-1179 to advance into a Phase 2 clinical trial by the end of 2026. The plan also contemplates evaluation of GS-1179 across broader prevention settings, including in connection with HIV PrEP, further reinforcing the potential opportunity for this program. We expect to make our determination on whether to opt-in to the U.S. cost and profit share soon after we receive the commercial cost estimates from Gilead, which will complete the opt-in package."

Second Quarter 2026 and Recent Updates

•
Announced expansion of ABI-6250 into cholestatic liver diseases, including PBC and PSC, with a Phase 2 study anticipated to initiate in the first quarter of 2027

•
Completed $115 million gross financing expected to extend funding beyond planned ABI-6250 Phase 2 studies in hepatitis delta virus (HDV) and cholestatic liver diseases

•
Presented topline Phase 1a data for ABI-6250 at the European Association for the Study of the Liver (EASL) Congress 2026 and participated in several scientific and investor conferences during the quarter

•
Received the clinical development plan from Gilead Sciences, Inc. (Gilead) for the herpes simplex virus (HSV) helicase-primase inhibitor (HPI) program. The plan indicates GS-1179 (formerly ABI-1179) has been selected to advance, with a Phase 2 clinical trial in participants with recurrent genital herpes expected to initiate by the end of 2026. The program is also being considered for possible evaluation as part of a combination strategy with HIV pre-exposure prophylaxis (PrEP). Assembly Bio's decision to opt in to the 40% U.S. cost-profit share will be made after receipt and review of Gilead's commercial cost estimates, which will complete the opt-in package.

Anticipated Milestones and Events

•
Following receipt of Gilead's commercial cost estimates for the complete opt-in package for the HSV HPI program, determine by year-end 2026 whether to exercise Assembly Bio's option to participate in a 40% U.S. cost-profit share in lieu of receiving U.S. milestones and royalties

•
Initiate a Phase 2 clinical study evaluating ABI-6250 in participants with chronic HDV by year-end 2026

•
Initiate a Phase 2 clinical study evaluating ABI-6250 in participants with cholestatic liver diseases, including PBC and PSC, in the first quarter of 2027

Upcoming Conferences

•
American Chemical Society (ACS) Fall 2026: August 23-27, 2026 – Chicago, Illinois

•
International HBV Meeting: September 6-10, 2026 – Singapore

•
ID Week: October 21-24, 2026 – Washington, D.C.

•
American Association for the Study of Liver Diseases (AASLD): November 5-9, 2026 – Denver, Colorado

GS-1179 and ABI-6250 are investigational product candidates that have not been approved anywhere globally, and their safety and efficacy have not been established. GS-1179 is exclusively licensed to Gilead under the collaboration between Assembly Bio and Gilead, and Gilead has the sole right and responsibility for further clinical development and commercialization of the HSV HPI program.

Second Quarter 2026 Financial Results

•
Cash, cash equivalents and marketable securities were $320.4 million as of June 30, 2026, compared to $226.6 million as of March 31, 2026. The company's cash position, including the first $75 million extension fee due from Gilead in the fourth quarter of 2026 following the third anniversary of the collaboration agreement, is projected to fund operations into 2029.

•
Revenue from collaborative research with Gilead was $13.4 million for the three months ended June 30, 2026, compared to $9.6 million for the same period in 2025. The increase reflects the timing of activities performed and progress toward completion of services under the Gilead Collaboration Agreement, and includes a $5.1 million cumulative catch-up adjustment related to updated estimates of future activities under the collaboration.

•
Research and development expenses were $14.9 million for the three months ended June 30, 2026, compared to $16.1 million for the same period in 2025. The decrease was primarily driven by lower external program expenses due to the completion of clinical trials, partially offset by increased research and discovery activities and higher employee-related expenses.

•
General and administrative expenses were $4.8 million for the three months ended June 30, 2026, compared to $4.6 million for the same period in 2025, primarily driven by increased stock-based compensation related to performance-based awards.

•
Net loss attributable to common stockholders was $3.9 million, or $0.20 per basic and diluted share, for the three months ended June 30, 2026, compared to $10.2 million, or $1.33 per basic and diluted share, for the same period in 2025. The lower net loss was driven by increased revenue, lower research and development expenses and higher interest income from a larger cash balance following Assembly Bio's recent financings. Lower net loss per share also reflects a higher weighted-average share count in 2026.

About Assembly Biosciences

Assembly Biosciences is a biotechnology company dedicated to the development of innovative small-molecule therapeutics aimed at advancing the treatment paradigm of serious viral and liver diseases and improving the lives of patients worldwide. Led by an accomplished leadership team in antiviral and liver disease drug development, Assembly Bio is committed to improving outcomes for people living with the chronic impacts of herpesvirus, hepatitis delta virus (HDV) infections, cholestatic liver diseases and hepatitis B virus (HBV). For more information, visit assemblybio.com.

Jamie Strachota

Sam Brown LLC

(703) 819-7647

ASMBMedia@sambrown.com

ASSEMBLY BIOSCIENCES, INC.

CONDENSED CONSOLIDATED BALANCE SHEETS

(In thousands except for share amounts and par value)

June 30, | December 31,
2026 | 2025
(Unaudited)
ASSETS
Current assets
Cash and cash equivalents | 32,286 | 58,450
Marketable securities | 288,075 | 189,656
Accounts receivable from collaboration with a related party | 822 | 974
Prepaid expenses and other current assets | 6,795 | 5,469
Total current assets | 327,978 | 254,549
Property and equipment, net | 315 | 221
Operating lease right-of-use assets | 2,227 | 2,508
Other assets | 312 | 312
Total assets | 330,832 | 257,590
LIABILITIES AND STOCKHOLDERS' EQUITY
Current liabilities
Accounts payable | 1,180 | 1,171
Accrued research and development expenses | 2,007 | 2,387
Other accrued expenses | 3,342 | 7,749
Deferred revenue from a related party | 16,304 | 36,904
Operating lease liabilities - short-term | 612 | 569
Total current liabilities | 23,445 | 48,780
Operating lease liabilities - long-term | 1,738 | 2,059
Total liabilities | 25,183 | 50,839
Commitments and contingencies
Stockholders' equity
Preferred stock, $0.001 par value; 5,000,000 shares authorized; no shares issued or outstanding | — | —
Common stock, $0.001 par value; 150,000,000 shares authorized as of June 30, 2026 and December 31, 2025; 19,850,342 and 15,855,329 shares issued and outstanding as of June 30, 2026 and December 31, 2025, respectively | 20 | 16
Additional paid-in capital | 1,151,235 | 1,038,823
Accumulated other comprehensive loss | (623 | (41
Accumulated deficit | (844,983 | (832,047
Total stockholders' equity | 305,649 | 206,751
Total liabilities and stockholders' equity | 330,832 | 257,590

ASSEMBLY BIOSCIENCES, INC.

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS AND COMPREHENSIVE LOSS

(In thousands except for share and per share amounts)

(Unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Collaboration revenue from a related party | 13,374 | 9,626 | 21,587 | 19,045
Operating expenses
Research and development | 14,917 | 16,125 | 29,817 | 30,976
General and administrative | 4,801 | 4,594 | 9,484 | 9,103
Total operating expenses | 19,718 | 20,719 | 39,301 | 40,079
Loss from operations | (6,344 | (11,093 | (17,714 | (21,034
Other income
Interest and other income, net | 2,487 | 895 | 4,778 | 2,018
Total other income | 2,487 | 895 | 4,778 | 2,018
Net loss | (3,857 | (10,198 | (12,936 | (19,016
Other comprehensive loss
Unrealized loss on marketable securities | 255 | 26 | 582 | 68
Comprehensive loss | (4,112 | (10,224 | (13,518 | (19,084
Net loss per share, basic and diluted | (0.20 | (1.33 | (0.72 | (2.51
Weighted average common shares outstanding, basic and diluted | 18,853,646 | 7,655,854 | 17,882,335 | 7,581,501

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-19_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a biotechnology company developing innovative therapeutics targeting serious viral diseases with the potential to improve the lives of patients worldwide. Our pipeline includes multiple clinical-stage investigational therapies, including: (1) two long-acting helicase-primase inhibitors (HPI) for the treatment of recurrent genital herpes; (2) an orally bioavailable hepatitis delta virus (HDV) entry inhibitor; and (3) a highly potent next-generation capsid assembly modulator (CAM) designed to disrupt the replication cycle of hepatitis B virus (HBV) at several key points. Our pipeline also includes a novel, oral broad-spectrum non-nucleoside polymerase inhibitor (NNPI) for the treatment of transplant-related herpesviruses, which is currently undergoing studies to enable a regulatory filing, and we have additional research programs against multiple antiviral targets. In December 2025, pursuant to our collaboration with Gilead Sciences, Inc. (Gilead and the Gilead Collaboration), Gilead exercised its option to license our HPI program for the treatment of recurrent genital herpes, including our long-acting investigational candidates ABI-1179 (1179) and ABI-5366 (5366). For additional information regarding Gilead's exercise of its option, see "Collaboration and License Agreement—Gilead Sciences, Inc.—Option Exercise."

Our Clinical Programs and Regulatory Filing-Enabling Program

2025 was a pivotal year for us, as we reported data readouts for 5366, 1179, 4334 and 6250 as follows:

•
February 2025:

o
1179 – Positive Phase 1a interim results in the Phase 1a/b study

•
June 2025:

o
4334 – Positive Phase 1b topline results

•
August 2025:

o
5366 – Positive Phase 1b interim results from the weekly dosing cohorts in the Phase 1a/b study

o
6250 – Positive Phase 1a interim results

•
December 2025:

o
1179 – Positive Phase 1b interim results in the Phase 1a/b study

o
5366 – Positive Phase 1b interim results from the monthly dosing cohorts in the Phase 1a/b study

In addition, during December 2024, we identified a development candidate, ABI-7423 (7423), in our broad-spectrum NNPI program targeting transplant-associated herpesviruses. 7423 is a prodrug, and in October 2025, we transitioned our development from 7423 to 7272, its parent molecule. 7272 is currently in regulatory filing enabling studies.

Recurrent Genital Herpes/HSV-1 and HSV-2

Genital herpes can be caused by either herpes simplex virus type 1 (HSV-1) or herpes simplex virus type 2 (HSV-2). HSV-1 and HSV-2 are acquired by oral or genital contact either during symptomatic or asymptomatic reactivation of the virus. Both viruses replicate in neurons, where they can remain latent for the rest of the individual's life and periodically reactivate, with the virus spreading, replicating and causing disease in epithelial tissues. Initial infection can be asymptomatic or can be marked by serious symptoms, including painful skin lesions, swelling of lymph nodes and urinary problems that can persist for two to three weeks. While genital herpes can be caused by either HSV-1 or

HSV-2, recurrences are more likely to be experienced by individuals infected by HSV-2. Genital herpes recurrence can cause painful genital lesions that can lead to increased transmission and debilitate individuals, and symptoms may become more serious with additional episodes. Additional complications include increased risk of HIV infection, as 30% of HIV infections acquired through sexual transmission are attributable to HSV-2 infection. In addition, people with recurrent genital herpes often experience associated psychosocial impacts, including anxiety, concerns about transmission, depression and social stigma. Immunocompromised individuals may experience more severe and prolonged symptoms due to increased recurrence rates.

HPIs are antiviral agents in development for the treatment of recurrent genital herpes, with a clinically-validated mechanism of action. HPIs inhibit the HSV helicase-primase complex, which is a unique viral enzyme complex without a human homolog, consisting of helicase, primase and cofactor subunits. These subunits have functions that are essential for viral DNA replication and are conserved across HSV-1 and HSV-2. Unlike nucleoside analogs, these compounds do not require phosphorylation by the HSV thymidine kinase (TK) and ongoing viral replication to become active drugs. As a result, HPIs are active immediately upon reactivation of latent HSV-1 and HSV-2. Furthermore, HPIs are active against TK-deficient HSV-1 and HSV-2, which is a major mechanism of resistance to nucleoside analogs.

Most people with initial symptomatic genital herpes who are infected with HSV-2 have frequent recurrences, generally between three and 15 per year, impacting over four million people in the United States and France, Germany, Italy and Spain (collectively, the EU4) and the United Kingdom (UK). Currently, there are three antiviral drugs (all nucleoside analogs) that have been approved in the United States and the EU4/UK for the treatment of genital herpes. However, no new drugs have been approved in these regions to treat genital herpes for more than 25 years. In addition to the approved nucleoside analogs, agents such as local anesthetics or analgesics may be used to alleviate local symptoms of minor pain and discomfort.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Comparison of the Years Ended December 31, 2025 and 2024

Collaboration Revenue

The following table summarizes the period-over-period changes in our collaboration revenue (in thousands, except for percentages):

Year Ended December 31, | $ Change | % Change
2025 | 2024 | 2025 vs. 2024 | 2025 vs. 2024
Collaboration revenue from a related party | 72,303 | 28,520 | 43,783 | 154 | %

Collaboration revenue was $72.3 million for the year ended December 31, 2025 compared to $28.5 million for the year ended December 31, 2024. The $43.8 million increase was primarily driven by the recognition of $35.0 million of revenue associated with the exclusive license granted and transferred to Gilead for the HPI program in December 2025. The increase also reflects the additional $10.0 million payment we received in December 2024 under the First Amendment to the Gilead Collaboration Agreement, which was largely recognized in 2025.

Research and Development Expenses

Research and development expenses consist primarily of employee-related expenses, fees paid to CROs and CMOs, lab supplies and other third-party expenses that support our research and discovery, nonclinical and clinical activities. External program costs represent a significant portion of our research and development expenses, which we track by product candidate once it has been nominated. We use our employee and infrastructure resources, as well as certain third-party costs, across multiple research and development programs, and we do not specifically allocate these costs to our programs.

The following table summarizes the period-over-period changes in our research and development expenses (in thousands, except for percentages):

Year Ended December 31, | $ Change | % Change
2025 | 2024 | 2025 vs. 2024 | 2025 vs. 2024
External program expenses:
5366 | 9,353 | 6,215 | 3,138 | 50 | %
1179 | 8,119 | 4,239 | 3,880 | 92 | %
6250 | 5,780 | 6,396 | (616 | (10 | %)
4334 | 890 | 2,646 | (1,756 | (66 | %)
7272 (1) | 2,300 | — | 2,300 | 100 | %
Research and discovery | 8,161 | 8,985 | (824 | (9 | %)
VBR | — | (43 | (2) | 43 | (100 | %)
Total external program expenses | 34,603 | 28,438 | 6,165 | 22 | %
Employee and contractor-related expenses | 26,729 | 23,819 | 2,910 | 12 | %
Facility and other expenses | 3,481 | 3,676 | (195 | (5 | %)
Total research and development expenses | 64,813 | 55,933 | 8,880 | 16 | %

(1)
In October 2025, we transitioned our discovery and development from 7423 to its parent molecule, 7272, which is currently in regulatory filing-enabling preclinical studies.

(2)
Reflects net amounts refundable to us after final reconciliation of costs for the clinical trial conducted pursuant to the Clinical Trial Collaboration Agreement with Arbutus Biopharma Corporation, which was terminated in February 2023. We received the refund in 2025.

Research and development expenses were $64.8 million for the year ended December 31, 2025, compared to $55.9 million for the year ended December 31, 2024. The $8.9 million increase was primarily driven by higher external program expenses as we advanced our pipeline. Most notably, our HPI program incurred additional costs as both the 1179 and 5366 Phase 1a/b studies were underway during 2025, with more participants enrolled than in 2024. Employee and contractor-related expenses also increased, reflecting $2.1 million in increased compensation costs driven by annual salary increases and larger bonuses due to strong performance against our 2025 corporate objectives. The increase additionally reflects $1.1 million of higher stock-based compensation expense associated with performance stock units (PSUs) granted in 2025. These increases were partially offset by decreases in external program expenses from the completion of our 4334 Phase 1b study in mid-2025.

General and Administrative Expenses

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-19_item1_business.md)

Item 1. Business

Overview

We are a biotechnology company developing innovative therapeutics targeting serious viral diseases with the potential to improve the lives of patients worldwide. Our pipeline includes multiple clinical-stage investigational therapies, including: (1) two long-acting helicase-primase inhibitors (HPIs) for the treatment of recurrent genital herpes; (2) an orally bioavailable hepatitis delta virus (HDV) entry inhibitor; and (3) a highly potent next-generation capsid assembly modulator (CAM) designed to disrupt the replication cycle of hepatitis B virus (HBV) at several key points. Our pipeline also includes a novel, oral broad-spectrum non-nucleoside polymerase inhibitor (NNPI) for the treatment of transplant-related herpesviruses, which is currently undergoing studies to enable a regulatory filing, and we have additional research programs against multiple antiviral targets. In December 2025, pursuant to our collaboration (Gilead Collaboration) with Gilead Sciences, Inc. (Gilead), Gilead exercised its option to license our HPI program for the treatment of recurrent genital herpes, including our long-acting investigational candidates ABI-1179 (1179) and ABI-5366 (5366). For additional information regarding Gilead's exercise of its option, see "Collaboration and License Agreement—Gilead Sciences, Inc.—Option Exercise."

Our Strategy

Our current business strategy focuses on applying our deep research and development expertise in virology to discover, develop and advance next-generation therapeutics to patients in areas of high unmet medical need with significant market opportunities to market. We continue to rapidly advance our portfolio toward near-term clinical readouts, highlighted by the following on-going and future activities by doing the following:

•
Recurrent Genital Herpes (HSV-1, HSV-2) – Transitioning our HPI program, including 5366 and 1179 to Gilead and, upon receiving a clinical development plan and budget from Gilead, deciding whether to opt in to the Profit-Share (as defined below under the heading "Collaboration and License Agreement—Gilead Sciences, Inc.—Option Exercise").

•
HDV – Completing Phase 2 preparation activities and studies of ABI-6250 (6250), with Phase 2 initiation expected in the fourth quarter of 2026.

•
HBV – Evaluating partnering opportunities for ABI-4334 (4334), for which we have initiated a structured process to find potential partners to further advance the program.

•
Transplant-Associated Herpesviruses – Advancing ABI-7272 (7272), our oral broad-spectrum NNPI for the treatment of transplant-associated herpesviruses through nonclinical studies to enable a regulatory filing.

•
Research and Discovery – Continuing to leverage our research team's expertise to identify and nominate new viral targets and novel compounds to address significant unmet medical needs.

We have recruited an accomplished leadership team and research and development organization, with a collective team track record of over 15 approved drugs across multiple viral diseases. In addition, our collaboration with Gilead also brings us an industry-leading partner and brings together the teams' expertise in virology and provides an established partner for late-stage development and commercialization. For additional information regarding the Gilead Collaboration, see "Collaboration and License Agreements—Gilead Sciences, Inc."

Our Clinical Programs and Regulatory Filing-Enabling Program

2025 was a pivotal year for us, as we reported positive data readouts for 5366, 1179, 4334 and 6250 as follows:

•
February 2025:

o
1179 – Positive Phase 1a interim results in the Phase 1a/b study

•
June 2025:

o
4334 – Positive Phase 1b topline results

•
August 2025:

o
5366 – Positive Phase 1b interim results from the weekly dosing cohorts in the Phase 1a/b study

o
6250 – Positive Phase 1a interim results

•
December 2025:

o
1179 – Positive Phase 1b interim results in the Phase 1a/b study

o
5366 – Positive Phase 1b interim results from the monthly dosing cohorts in the Phase 1a/b study

In addition, during December 2024, we identified a development candidate, ABI-7423 (7423), in our broad-spectrum NNPI program targeting transplant-associated herpesviruses. 7423 is a prodrug of the parent molecule 7272, and in October 2025, we transitioned our development from 7423 to 7272. 7272 is currently in regulatory filing enabling studies.

Recurrent Genital Herpes/HSV-1 and HSV-2

Genital herpes can be caused by either herpes simplex virus type 1 (HSV-1) or herpes simplex virus type 2 (HSV-2). HSV-1 and HSV-2 are acquired by oral or genital contact either during symptomatic or asymptomatic reactivation of the virus. Both viruses replicate in neurons, where they can remain latent for the rest of the individual's life and periodically reactivate, with the virus spreading, replicating and causing disease in epithelial tissues. Initial infection can be asymptomatic or can be marked by serious symptoms, including painful skin lesions, swelling of lymph nodes and urinary problems that can persist for two to three weeks. While genital herpes can be caused by either HSV-1 or HSV-2, recurrences are more likely to be experienced by individuals infected by HSV-2. Genital herpes recurrence can cause painful genital lesions that can lead to increased transmission and debilitate individuals, and symptoms may become more serious with additional episodes. Additional complications include increased risk of HIV infection, as 30% of HIV infections acquired through sexual transmission are attributable to HSV-2 infection. In addition, people with recurrent genital herpes often experience associated psychosocial impacts, including anxiety, concerns about transmission, depression and social stigma. Immunocompromised individuals may experience more severe and prolonged symptoms due to increased recurrence rates.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-19_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-19_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-19_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-14_2-02-results.md, 10-K_2026-03-19_item7_mdna.md, 10-K_2026-03-19_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
