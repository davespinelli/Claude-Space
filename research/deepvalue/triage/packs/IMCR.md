# Triage pack — IMCR · Immunocore Holdings plc

_Generated 2026-09-04 23:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** IMCR · **Name:** Immunocore Holdings plc
- **CIK:** 0001671927
- **SIC:** 2836 — Biological Products, (No Diagnostic Substances)
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/IMCR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Immunocore Holdings plc
- **CIK:** 1,671,927 · **SIC:** 2836 (Biological Products, (No Diagnostic Substances)) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 37.57 |
| mktcap | $1.9B |
| ev | $1.4B |
| ev_ebit | n/a |
| fcf | -$15.1M |
| fcf_yield | -0.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$484.9M |
| net_debt_ebit | n/a |
| cash | $484.9M |
| ltd | $0.00 |
| equity | $419.8M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $400.0M |
| revenue_prior | $310.2M |
| rev_growth | 29.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$45.4M |
| net_income | -$35.5M |
| cfo | -$10.7M |
| capex | $4.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 51,498,617 |
| shares_py | 50,387,068 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -5.6% |
| r6m | 17.7% |
| off_52w_high | -6.6% |
| adv20 | $13.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.19 |
| r_ev_ebit | 0.00 |
| r_roic | 0.50 |
| r_rev_growth | 0.89 |
| r_buyback | 0.31 |
| score | 0.38 |

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
| rank | 344 |

**Screen rationale:** revenue +29.0%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **51,498,617** (CY2026Q2I) vs **50,387,068** prior year (CY2025Q2I)
- Change: **2.2%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 51,050 sh / $1,903,831 -> net $-1,903,831 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 30 (open-market buys 0, sales 6).

| code | rows |
|---|---|
| A | 12 |
| M | 12 |
| S | 6 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Immunocore reports second quarter financial results and provides a bus'; skipped 9 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (pressrelease-q22026.htm)

Immunocore reports second quarter financial results and provides a business update

KIMMTRAK ® (tebentafusp-tebn) net revenues of $115.9 million in Q2 2026, growing by 18% year-over-year

Enrollment in Phase 3 TEBE-AM trial for previously treated advanced cutaneous melanoma nearing the target of 540 patients – Data could come as early as end of 2026

Oral presentation of five-year overall survival data showing KIMMTRAK doubles likelihood of being alive at five years for patients with HLA-A*02:01 positive metastatic uveal melanoma

Promising Phase 1 brenetafusp monotherapy clinical activity in heavily pretreated HLA-A*02:01-positive patients with advanced melanoma, presented at ASCO, supports selected dose for Phase 3 PRISM-MEL-301 trial in first-line advanced melanoma

Cash, cash equivalents and marketable securities of $880 million as of June 30, 2026

Conference call today, August 6 at 8:00 AM ET, 1:00 PM BST

(OXFORDSHIRE, England & RADNOR, PA. & GAITHERSBURG, MD., US, 6 August 2026) Immunocore Holdings plc (Nasdaq: IMCR) ("Immunocore" or the "Company"), a commercial-stage biotechnology company pioneering and delivering transformative immunomodulating medicines to radically improve outcomes for patients with cancer, infectious diseases and autoimmune diseases, today announced its financial results for the first half ended June 30, 2026, and provided a business update.

"The five-year overall survival data for KIMMTRAK underscores the lasting impact of our medicine for patients with metastatic uveal melanoma and reinforces our confidence in the potential of our platform," said Bahija Jallal, CEO of Immunocore. "With enrollment in our Phase 3 TEBE-AM trial nearing target completion and continued progress across our pipeline, we remain focused on our mission: delivering innovative transformative medicines to improve outcomes for patients with serious diseases."

Second Quarter and First Half Highlights (including post-period)

Financial Results

For the second quarter ended June 30, 2026, total net product revenue (or 'net sales') arising from the sales of KIMMTRAK was $115.9 million, compared to $98.0 million for the same period in 2025. Q2 2026 sales were $74.9 million in the United States, $34.1 million in Europe, and $6.9 million in international regions. The increase in net product sales was primarily due to increased volumes in the United States and international regions.

Research and development (R&D) expenses for Q2 2026 were $73.9 million, compared to $69.0 million for Q2 2025. This increase was primarily due to advancement of our clinical programs, including our three Phase 3 studies.

Selling, general and administrative (SG&A) expenses for Q2 2026 were $43.9 million, compared to $42.8 million for Q2 2025.

Net loss for Q2 2026 was $0.8 million ($0.02 loss per share) compared to $10.3 million ($0.20 loss per share) for Q2 2025. Net income for the six months ended June 30, 2026, was $12.2 million ($0.23 income per share) compared to a net loss for the six months ended June 30, 2025, of $5.3 million ($0.11 loss per share).

Cash, cash equivalents and marketable securities were $880.2 million as of June 30, 2026, as compared to $864.2 million as of December 31, 2025. The Company expects to pay, in the second half of 2026, approximately $120 million in sales-related rebate accruals.

KIMMTRAK

The Company's lead product, KIMMTRAK ® (tebentafusp), is approved in 39 countries and has been launched in over 30 countries globally to date for HLA-A*02:01 positive people with unresectable or metastatic uveal melanoma (mUM). KIMMTRAK continues to be the standard of care in all major markets where it is launched.

The Company sees three key growth areas in the fifth year since the launch of KIMMTRAK as it plans to expand patient reach, including continued US community and global market penetration in mUM, the potential expansion into 2L+ advanced cutaneous melanoma (CM), and the potential expansion into adjuvant uveal melanoma.

Metastatic uveal melanoma

• KIMMTRAK net product sales were $115.9 million and $222.6 million for the three and six months ended June 30, 2026, representing increases of 18% and 16% respectively, as compared to the same periods in 2025.

• 17% year-over-year quarterly sales growth in the United States with mean duration of treatment of 14 months.

• 21% year-over-year quarterly sales growth combined in Europe and International, driven by increased demand.

• Five-year overall survival (OS) data, from the Phase 3 trial of KIMMTRAK in patients with unresectable or mUM, were presented at the AACR 2026 meeting, representing the longest follow-up reported for any T cell engager in a solid tumor.

• KIMMTRAK doubled the likelihood of being alive at five years with an OS rate of 16% versus 8% in the control arm (HR 0.67), and a median OS of 21.6 vs. 16.9 months, respectively.

• The OS benefit with KIMMTRAK was observed regardless of known baseline characteristics including poor prognostic factors (high tumor burden; elevated lactate dehydrogenase [LDH]) or tumor location.

• Data also confirmed OS benefit was primarily driven by KIMMTRAK rather than subsequent therapies.

2L+ advanced cutaneous melanoma

• Enrollment in the registrational Phase 3 TEBE-AM trial, evaluating tebentafusp as monotherapy, and in combination with pembrolizumab, versus a control arm in patients with previously treated advanced CM, is nearing the target of 540 patients. The trial is event driven and topline data could come as early as the end of 2026.

• There is great unmet need in second- and later-line CM, with no therapy having shown an OS improvement post checkpoint inhibitors in a randomized clinical trial to date. The Company estimates there are up to 4,000 previously treated advanced HLA-A*02:01 positive CM patients in the US and Europe.

Adjuvant uveal (or ocular) melanoma

• The European Organisation for Research and Treatment of Cancer (EORTC) continues to expand the site footprint of the Phase 3 Adjuvant Trial in Ocular Melanoma (ATOM), with patients now enrolling in the United States.

• The Company estimates the HLA-A*02:01 positive, high-risk adjuvant uveal melanoma patient population could represent up to 1,200 patients in the US and Europe.

PRAME portfolio

Brenetafusp is the Company's lead PRAME-A02 ImmTAC bispecific candidate. Brenetafusp is being evaluated in combination with nivolumab in a Phase 3 registrational trial (PRISM-MEL-301) in patients with first-line, advanced cutaneous melanoma, and in a Phase 1/2 clinical trial as monotherapy and in combination across multiple tumor types, including ovarian cancer and non-small cell lung cancer (NSCLC).

PRISM-MEL-301 – First PRAME Phase 3 clinical trial with brenetafusp in first-line advanced cutaneous melanoma

• The Company continues with 1:1 randomization of HLA-A*02:01 positive, first-line, advanced or metastatic cutaneous melanoma patients to brenetafusp 160 mcg + nivolumab or a control arm of either nivolumab or nivolumab + relatlimab.

• Despite approved therapies, there remains an unmet need for improved progression-free survival and OS in the first-line setting where there is the potential to address an estimated 10,000 HLA-A*02:01 positive patients across US and Europe.

Phase 1/2 clinical trials of brenetafusp and IMC-P115C (PRAME-A02 Half-Life Extended) in multiple solid tumors

Melanoma

• The Phase 1/2 data, presented at the 2026 ASCO meeting, showed improved clinical activity of brenetafusp monotherapy, in patients with heavily-pretreated advanced melanoma, with an overall response rate (ORR) of 17% and a disease control rate (DCR) of 67%, in the 160 mcg versus 40 mcg cohort (ORR 6% and DCR 56%), despite patients on the high dose having less favorable prognostic factors. These data support the selected dose for the ongoing Phase 3 PRISM-MEL-301 trial in first-line advanced melanoma.

• The median OS for brenetafusp monotherapy of 14.3 months was similar to other Phase 1/2 trials of combination therapies in heavily pre-treated patients with advanced melanoma, including studies with autologous cell therapies.

• Brenetafusp in combination with pembrolizumab (n=6) demonstrated promising clinical activity with ORR of 33% and DCR 67% in patients with PD1 primary resistance (defined as progressive disease within 6 months of starting first PD1-based regimen).

• Brenetafusp was generally well tolerated as monotherapy and in combination with pembrolizumab.

Other tumors and IMC-P115C

• After observing an initial brenetafusp monotherapy signal in platinum-resistant ovarian cancer (PROC), the Company is evaluating, as part of an ongoing Phase 1/2 trial, combination therapy with bevacizumab in earlier lines, including platinum-sensitive ovarian cancer (PSOC). In the same trial, the Company continues signal detection across multiple metastatic non-small cell lung cancer (NSCLC) cohorts, including combinations with standards of care in earlier-line NSCLC.

• The Company is enrolling patients in the Phase 1 dose escalation trial evaluating IMC-P115C in patients with multiple solid tumors.

• The Company expects to present Phase 1/2 data from both trials in the second half of 2026.

ImmTAV candidates for a functional cure in infectious diseases

The Company's bispecific TCR technology platform has the potential to offer a new approach for the treatment of certain chronic infections by eliminating evidence of remaining virus in circulation after the patient stops taking medication – known as a 'functional cure'. The Company is studying an investigational candidate for people living with human immunodeficiency virus (HIV).

Phase 1/2 trial of IMC-M113V (Gag-A02) for people living with HIV

• In July 2026, at the International AIDS Society meeting in Rio de Janeiro, the Company presented translational data, from the first three cohorts of the multiple ascending dose part of the Phase 1/2 trial, demonstrating that IMC-M113V induces robust type I and II interferon-associated immune programs, with stronger induction in participants who maintained viral control after treatment interruption.

• The data also showed that, in addition to previously demonstrated direct killing of HIV-infected cells, IMC-M113V redirection of T cells results in induction of a robust interferon-associated immune program that may contribute to post-treatment viral control.

• The Company completed enrollment of additional patients at higher dose cohorts, up to 1200 mcg, as part of the multiple ascending dose (MAD) part of the Phase 1/2 trial. Analysis of the new data is ongoing with results planned to be shared early next year.

Tissue-specific down modulation of the immune system for autoimmune diseases

The key differentiator of the ImmTAAI platform is down modulation of the immune system in a tissue-specific manner. The candidates achieve this by suppressing pathogenic T cells via PD1 receptor agonism only when tethered to the target tissue.

• Clinical trial sites for the Phase 1 trial with IMC-S118AI are open, and the Company expects the first type 1 diabetes patient to be dosed in the coming weeks.

• The Company, in collaboration with the University of Florida, published preclinical data in Science Advances demonstrating that in live human pancreas tissue slices from a recent-onset type 1 diabetes donor, IMC-S118AI selectively binds to HLA-A*02:01-positive beta cells and suppresses autoreactive T cell activity around islets, helping protect beta cells and preserve insulin secretion.

• IMC-S118AI is designed to bind pre-pro-insulin on beta cells of the pancreas and deliver a PD-1 agonist signal to nearby auto-reactive T cells thereby protecting the pancreatic beta cells from T cell attack while preserving beta cell mass.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-25_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a commercial stage biotechnology company pioneering and delivering transformative immunomodulating medicines to radically improve outcomes for patients with cancer, infectious diseases, and autoimmune diseases. Leveraging our proprietary, flexible, off-the-shelf ImmTAX ( I mmune m obilizing m onoclonal T CRs A gainst X disease) platform, we are developing a deep pipeline in multiple therapeutic areas, including clinical stage programs in oncology and infectious disease, advanced preclinical programs in autoimmune disease and earlier preclinical programs across three therapeutic areas.

In 2022, we received approval for our lead product, KIMMTRAK, for the treatment of unresectable or metastatic uveal melanoma ("mUM") from the FDA, the European Commission, and other health authorities. KIMMTRAK is now approved in 39 countries for the treatment of unresectable or mUM. We have commercially launched KIMMTRAK in 30 countries globally including the United States, Germany and France through December 31, 2025, with further commercial launches planned in additional territories where KIMMTRAK is approved.

KIMMTRAK is the lead product from our ImmTAX platform and was the first approved therapy in mUM. To date, we have treated over 2,000 cancer patients with KIMMTRAK, tebentafusp, and our other ImmTAX product candidates, which we believe is the largest clinical data set of any T cell engager bispecific in solid tumors and any TCR therapeutic. Our clinical programs are being conducted with patients with a broad range of cancers including melanoma, ovarian, lung, and colorectal, among others. We believe that these tumor types have large addressable patient populations and significant unmet need. We are progressing three late-stage clinical programs within our ImmTAC ( I mmune m obilizing m onoclonal T CRs A gainst C ancer) portfolio, including KIMMTRAK and PRAME-targeted brenetafusp.

Since our inception, we have focused on organizing and staffing our company, raising capital, performing research and development activities to advance our research, development and technology, and commercialization of KIMMTRAK. While we have successfully generated revenue from KIMMTRAK, which is our first marketed product, our ability to generate higher levels of revenue from other marketed products, which may never be fully developed or commercialized, depends on the successful development and regulatory approval of one or more of our product candidates and our ability to finance operations. We have raised funds through our initial public offering, private placements of our ordinary and preferred shares, debt financings, revenue and historical payments from our collaboration partners. These funds have been and are being used to fund operations and invest in activities for technology creation, drug discovery and clinical development programs, infrastructure, creation of portfolio of intellectual property and commercial and administrative support.

We have incurred significant operating losses and expect to continue to incur significant expenses and operating losses for the near future. We had net losses of $35.5 million, $51.1 million and $55.3 million, for the years ended December 31, 2025, 2024 and 2023 , respectively. As of December 31, 2025, our accumulated deficit was $831.3 million. We expect to continue to incur significant and increasing expenses and to incur operating losses for the foreseeable future, as we advance our product candidates through preclinical and clinical development and seek regulatory approvals, manufacture drug product and drug supply, maintain and expand our intellectual property portfolio, as well as hire additional personnel, pay for further accounting, audit, legal, regulatory and consulting services, and pay costs associated with maintaining compliance with Nasdaq listing rules and the requirements of the SEC, director and officer liability insurance, investor and public relations activities and other expenses associated with operating as a public company.

We do not expect to generate revenue from the sale of our other product candidates unless and until we successfully complete clinical development of and obtain regulatory approval for such product candidates. As a result, we may need additional funding to support our continued operations and pursue our clinical development and growth strategy. Until we can generate sufficient revenue from product sales, if ever, we expect to finance our operations through a combination of public or private equity offerings, debt financings, government funding arrangements, collaborations and marketing and distribution and licensing arrangements. We may be unable to raise additional funds or enter into such other arrangements on favorable terms, or at all, particularly in light of recently worsening macroeconomic conditions, such as supply chain disruptions, fluctuations in interest rates and volatility in the capital markets. If we fail to raise capital or enter into such arrangements as, and when, needed, we may have to significantly delay, scale back or discontinue the development and commercialization of one or more of our programs.

Because of the numerous risks and uncertainties associated with pharmaceutical development, we are unable to predict the timing or amount of future revenues, increased expenses or when or if we will be able to achieve or maintain profitability. If we fail to become profitable or are unable to sustain profitability on a continuing basis, then we may be unable to continue our operations at planned levels and may be forced to reduce our operations.

Recent Developments

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Comparison of the Years ended December 31, 2025 and 2024

Revenue

The following table summarizes our total revenue (in thousands):

Year Ended December 31,
2025 | 2024 | Increase / (decrease) | % Increase / (decrease)
Revenue from sale of therapies, net | 400,016 | 309,989 | 90,027 | 29 | %
Collaboration revenue | — | 213 | (213) | (100) | %
Total revenue | 400,016 | 310,202 | 89,814 | 29 | %

Revenue from sale of therapies, net

Revenue from sale of therapies, net is presented by country / region based on location of the end customer in the table below (in thousands) :

Year Ended December 31,
2025 | 2024 | Increase / (decrease) | % Increase / (decrease)
United States | 256,998 | 226,687 | 30,311 | 13 | %
Europe | 131,422 | 73,224 | 58,198 | 79 | %
International | 11,596 | 10,078 | 1,518 | 15 | %
Revenue from sale of therapies, net | 400,016 | 309,989 | 90,027 | 29 | %

For the year ended December 31, 2025 , we generated net revenue from sale of therapies of $400.0 million due to the sale of KIMMTRAK, of which $257.0 million was in the United States, $131.4 million in Europe, including the impact of a net decrease in estimated reserves related to prior periods of $6.0 million, and $11.6 million in International. Revenue from the sale of therapies, net increased in the year ended December 31, 2025 as compared to December 31, 2024 due primarily to increased volume in the United States and Europe as well as global country expansion.

R&D Expenses

The following table summarizes our R&D expenses (in thousands):

Year Ended December 31,
2025 | 2024 | Increase / (decrease) | % Increase / (decrease)
External R&D expenses:
PRAME programs | 82,594 | 90,377 | (7,783) | (9) | %
Tebentafusp programs | 40,824 | 31,166 | 9,658 | 31 | %
Infectious disease programs | 6,450 | 6,662 | (212) | (3) | %
All other external clinical and preclinical costs | 59,716 | 23,747 | 35,969 | 151 | %
Total external R&D expenses | 189,584 | 151,952 | 37,632 | 25 | %
Internal R&D expenses:
Salaries and other employee-related costs | 49,898 | 43,706 | 6,192 | 14 | %
Share-based compensation expense | 8,776 | 7,771 | 1,005 | 13 | %
All other internal R&D costs | 33,821 | 28,328 | 5,493 | 19 | %
U.K. R&D tax credits | (7,210) | (9,606) | 2,396 | (25) | %
Total internal R&D expenses | 85,285 | 70,199 | 15,086 | 21 | %
Total R&D expenses | 274,869 | 222,151 | 52,718 | 24 | %

For the year ended December 31, 2025 , our R&D expenses were $274.9 million, as compared to $222.2 million for the year ended December 31, 2024 .

For the year ended December 31, 2025 , our external R&D expenses increased by $37.6 million due to an increase in all other external clinical and preclinical costs of $36.0 million related to continued progress in the pipeline, primarily for our autoimmune programs, including clinical material manufacturing for anticipated Phase 1 initiation. In addition, R&D expenses incurred for our tebentafusp programs increased by $9.7 million as a result of continued advancement of the TEBE-AM and ATOM Phase 3 trials, and purchases of drug consumables. There was a decrease of $7.8 million in expenses incurred for our PRAME programs primarily resulting from higher costs in the year ended December 31, 2024, due to timing of manufacturing batches and purchases of drug consumables for our clinical trials, partially offset by higher costs in the year ended December 31, 2025 due to enrollment in our PRISM-MEL-301 Phase 3 clinical trial.

For the year ended December 31, 2025 , our internal R&D expenses increased by $15.1 million primarily due to an increase in salaries and employee-related expenses and other internal R&D costs following the growth of our clinical and preclinical programs.

SG&A Expenses

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-25_item1_business.md)

Item 1. Business

We are a commercial stage biotechnology company pioneering and delivering transformative immunomodulating medicines to radically improve outcomes for patients with cancer, infectious diseases, and autoimmune diseases. Leveraging our proprietary, flexible, off-the-shelf ImmTAX ® ( I mmune m obilizing m onoclonal T CRs A gainst X disease) platform, we are developing a deep pipeline in multiple therapeutic areas, including clinical stage programs in oncology and infectious disease, advanced pre-clinical programs in autoimmune disease and earlier pre-clinical programs across three therapeutic areas.

In 2022, we received approval for our lead product, KIMMTRAK, for the treatment of unresectable or metastatic uveal melanoma ("mUM") from the FDA, the European Commission and other health authorities. KIMMTRAK is now approved in 39 countries and the Company has commercially launched the product in 30 countries, including the United States, Germany and France, among other territories.

KIMMTRAK is the lead product from our ImmTAX platform and was the first approved therapy in mUM. To date, we have treated over 2,000 cancer patients with KIMMTRAK (tebentafusp), and our other ImmTAX product candidates, which we believe is the largest clinical data set of any T cell engager bispecific in solid tumors and any T cell receptor ("TCR") therapeutic. Our clinical programs are being conducted with patients with a broad range of cancers including melanoma, ovarian, lung, and colorectal, among others. We believe that these tumor types have large addressable patient populations and significant unmet need. We are progressing three late-stage clinical programs within our ImmTAC ® ( I mmune m obilizing m onoclonal T CRs A gainst C ancer) portfolio, including KIMMTRAK and the PRAME-targeted brenetafusp.

KIMMTRAK is manufactured at facilities located in Denmark and Germany, with final packaging completed in the Netherlands. We are supporting the appropriate use of KIMMTRAK in the United States and Europe through a well-equipped and fit-for-purpose trained commercial team that includes commercial, medical, sales, and value access team members. We utilize a hybrid commercialization model that includes an in-house sales force in the United States and contracted resources in the United States and Europe. To support our commercialization efforts, we have an exclusive multi-regional collaboration with Medison Pharma Ltd. ("Medison") to help seek regulatory authorization and commercialize KIMMTRAK in Canada, Australia, New Zealand, Israel, Central and Eastern Europe, South and Central America and the Caribbean and we have entered into a distribution and commercialization agreement with Er-Kim Pharmaceuticals Bulgaria EOOD ("Er-Kim") for commercialization of KIMMTRAK in Turkey, the Middle East, North Africa, Caucasus, and the Commonwealth of Independent States regions.

Unlike antibody targeted immunotherapies that have a relatively small target pool, our approach relies on the power of TCRs, which are naturally occurring receptors found on the surface of T cells that have the ability to target nearly all of the human proteome. Natural TCRs give T cells the ability to scan for abnormalities in nearly any cell in the body that are presented as protein fragments, or antigens, by human leukocyte antigen ("HLA"), on the cell surface. Our ImmTAX platform builds upon these natural TCRs to engineer soluble targeted and high-affinity TCRs. By engineering these TCRs through our ImmTAX platform, we are developing off-the-shelf, bispecific therapeutics, which are able to precisely target a wide range of proteins uniquely expressed by unhealthy and abnormal cells that cannot be targeted by current antibody-based immunotherapies.

Our ImmTAX bispecific therapeutics are designed to couple the targeting power of these engineered TCRs on one end with the other end displaying pre-optimized effector functions, which have the ability to drive a desired immune response at the site of the disease. This combination is designed to provide us with significant flexibility as we are able to engineer and tailor our ImmTAX therapeutics to target proteins that are specific to the disease we are trying to treat and then modulate the corresponding immune response by either boosting or inhibiting the immune system.

We will also continue pioneering immunotherapy and unlocking the full potential of our platform to generate transformative treatments for patients, by using different targeting mechanisms and immune effectors for next-generation bispecific therapies.

Our Pipeline

We are currently leveraging our platform within three therapeutic areas: cancer, infectious diseases, and autoimmune diseases. Our oncology portfolio includes numerous pre-clinical to late stage programs, including Phase 3 clinical trials of KIMMTRAK (tebentafusp) in advanced cutaneous melanoma and adjuvant uveal melanoma, brenetafusp in a Phase 3 clinical trial in first-line advanced cutaneous melanoma and in a Phase 1/2 clinical trial in multiple tumor types, IMC-R117C (PIWIL-1) in a Phase 1/2 clinical trial in advanced solid tumors, including colorectal cancer, and IMC-P115C (PRAME-HLE-A02) in a Phase 1 clinical trial for patients with tumors that express PRAME. In infectious diseases, we are currently evaluating IMC-M113V, in Phase 1 clinical trials for a potential functional cure in human immunodeficiency virus ("HIV"). We have expanded the ImmTAX platform into autoimmune diseases with the addition of two potential first-in-class new bispecific candidates entering the pipeline: IMC-S118AI, for which we have submitted a clinical trial application ("CTA") in December 2025, and IMC-U120AI for which we plan to submit a CTA or investigational new drug application ("IND") in the second half of 2026. Our current pipeline is below.

Our ImmTAC Platform (Oncology)

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-25_item7_mdna.md, 10-K_2026-02-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
