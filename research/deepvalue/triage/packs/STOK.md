# Triage pack — STOK · Stoke Therapeutics, Inc.

_Generated 2026-09-04 23:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** STOK · **Name:** Stoke Therapeutics, Inc.
- **CIK:** 0001623526
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/STOK

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Stoke Therapeutics, Inc.
- **CIK:** 1,623,526 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

> **EARNINGS QUALITY FLAG — one-off items likely.**
> revenue growth above 50% alongside share count growth above 15% (bought, not organic).
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 29.99 |
| mktcap | $1.9B |
| ev | $1.8B |
| ev_ebit | n/a |
| fcf | $44.9M |
| fcf_yield | 2.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -6.9% |
| net_debt | -$110.0M |
| net_debt_ebit | n/a |
| cash | $110.0M |
| ltd | $0.00 |
| equity | $345.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $184.4M |
| revenue_prior | $36.6M |
| rev_growth | 404.5% |
| rev_growth_note | share count +17.8% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | revenue growth above 50% alongside share count growth above 15% (bought, not organic) |
| ebit | -$20.6M |
| net_income | -$6.9M |
| cfo | $45.6M |
| capex | $670k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 17.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 64,526,242 |
| shares_py | 54,797,418 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 61.5% |
| r6m | -13.4% |
| off_52w_high | -21.8% |
| adv20 | $27.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.32 |
| r_ev_ebit | 0.00 |
| r_roic | 0.16 |
| r_rev_growth | 0.99 |
| r_buyback | 0.08 |
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
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 358 |

**Screen rationale:** revenue +404.5% BUT share count +17.8% yoy — growth may be acquisition/issuance-driven, not organic; debt data missing (net cash unverified); 12-1 momentum 61.5%; EARNINGS QUALITY: revenue growth above 50% alongside share count growth above 15% (bought, not organic) — one-off items likely


## 3. Share count trend

- Shares outstanding: **64,526,242** (CY2026Q2I) vs **54,797,418** prior year (CY2025Q2I)
- Change: **17.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +17.8% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-04-07** — Item 5.02 (officer / director change or comp arrangement): (d) On April 3, 2026, the Board of Directors (the "Board") of Stoke Therapeutics, Inc. ("Stoke" or the "Company"), increased the size of the Board to ten (10) directors and, following the recommendation of the Nominating and Corporate Governance Committee of...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 41,601 sh / $1,305,008 -> net $-1,305,008 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 39 (open-market buys 0, sales 13).

| code | rows |
|---|---|
| A | 4 |
| G | 16 |
| M | 6 |
| S | 13 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'Program Highlights'; skipped 8 forward-looking-statement block(s); 15 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (stok-ex99_1.htm)

Program Highlights

Dravet syndrome (zorevunersen)

•
Pivotal Phase 3 EMPEROR study progress:

o
U.S., UK and Japan: In June, Stoke announced completion of enrollment of 162 patients in the U.S., UK and Japan where sham control is administered via lumbar puncture (LP). This is the planned primary analysis population for the U.S. NDA. Patients are consistently progressing through the study. As of July 31, 2026:

▪
Approximately 145 are through Week 8 and have received either two 70 mg loading doses of zorevunersen or sham.

▪
Approximately 80 are through Week 24 and therefore have one dose of zorevunersen or sham remaining in the 52-week treatment period.

▪
Approximately 60 are through Week 28, the time point at which the primary endpoint of change in major motor seizure frequency will be measured.

▪
The first patients are expected to reach Week 52 in August 2026.

▪
No patients have discontinued treatment in the study.

Data from this cohort are anticipated in the third quarter of 2027 and are expected to be the final clinical data required to complete the planned rolling NDA submission to the FDA. Stoke expects a pre-NDA meeting with the FDA in the second half of 2026 and to initiate the rolling NDA process in the first quarter of 2027, with completion expected in the second half of 2027.

o
Europe (Germany, France, Spain and Italy): An additional cohort of approximately 30 patients is currently being enrolled in Europe, where the sham control is administered via a needle prick (NP). Screening for this cohort has now closed, and the last patient is expected to be enrolled in August 2026.

o
China: Site activation and screening are also underway in China, where zorevunersen was recently granted Breakthrough Therapy Designation. Enrollment is anticipated to complete in the second half of 2026. Data from the additional patients in Europe and China are not planned for inclusion in the U.S. NDA submission to the FDA.

•
Continuing awareness of Dravet syndrome and appreciation for zorevunersen with 5 years of clinical data:

o
The Company will continue its educational efforts at major neurology and epilepsy congresses during the second half of 2026. Analyses of data from the ongoing OLEs, including effects on seizure severity, improvements in seizure freedom and quality of life, will support efforts to increase clinician understanding of zorevunersen while the Phase 3 EMPEROR study advances toward completion and the Company prepares for

EX 99.1

a potential U.S. approval and launch. The Company will also continue discussions with the FDA to update the Agency on its long-term data for zorevunersen.

Pipeline beyond zorevunersen

•
The Phase 1 OSPREY study of STK-002 for the treatment of ADOA is continuing through dose escalation cohorts. All eight planned clinical trial sites are now active in the UK, Germany, Denmark, Italy and Austria, and dosing of the first cohort of patients (n=3) is complete with no serious or severe safety events observed to date. Dosing of the second cohort is expected to begin in August 2026. Subject to ongoing safety assessments, dosing in the third and fourth dose cohorts are expected to follow with a readout of safety and efficacy results anticipated in the first half of 2027.

•
Lead optimization is underway to identify a clinical candidate for the treatment of SYNGAP1-related disorders. SYNGAP1-related disorders are severe and rare neurodevelopmental diseases.

•
Stoke is expanding its early research efforts with new targets in haploinsufficient diseases, primarily focused on central nervous system (CNS) diseases.

•
Thomas McCauley, Ph.D., joined Stoke as Chief Scientific Officer in July to support this pipeline growth, leveraging the Company's proprietary RNA medicines platform to advance its pipeline of potential treatments for severe genetic diseases.

Second quarter 2026 financial results

•
The Company has $420.0 million in cash, cash equivalents and marketable securities based on $354.3 million as of June 30, 2026 and $65.7 million in net proceeds generated from an ATM sale to a single investor after June 30, 2026. These funds are expected to support operations through to potential U.S. commercialization of zorevunersen in early 2028.

•
Revenue recognized for the three months ended June 30, 2026, was $9.3 million, a decrease from $13.8 million for the same period in 2025. Revenue is generated from satisfying contractual obligations of the collaboration and licensing agreements with Acadia and Biogen.

•
Net loss for the three months ended June 30, 2026, was $61.6 million (including non-cash stock-based compensation expense of $10.8 million), or $0.93 per share, compared to a net loss of $23.5 million (including non-cash stock-based compensation expense of $7.6 million), or $0.40 per share, for the same period in 2025.

•
Research and development expenses for the three months ended June 30, 2026, were $49.5 million, compared to $25.9 million for the same period in 2025. The increase was driven by increased activities and personnel expenses to support the advancement of zorevunersen.

•
Sales, general and administrative expenses for the three months ended June 30, 2026, increased to $25.3 million from $15.3 million for the same period in 2025. The increase was driven by growth in personnel and launch readiness expenses.

Year-to-Date 2026 Financial Results

•
Revenue recognized for the six months ended June 30, 2026, was $15.6 million, a decrease from $172.4 million for the same period in 2025. The decrease in revenue is primarily driven by the recognition of $150.8 million related to the Biogen IP license performance obligation during the six months ended June 30, 2025.

EX 99.1

•
Net loss for the six months ended June 30, 2026, was $111.6 million (including non-cash stock-based compensation expense of $19.6 million), or $1.73 per share, compared to a net income of $89.4 million (including non-cash stock-based compensation expense of $14.4 million), or $1.50 per diluted share, for the same period in 2025.

•
Research and development expenses for the six months ended June 30, 2026, were $89.2 million, compared to $58.5 million for the same period in 2025. The increase was driven by increased activities and personnel expenses to support the advancement of zorevunersen.

•
Sales, general and administrative expenses for the six months ended June 30, 2026, increased to $45.2 million from $29.9 million for the same period in 2025. The increase was driven by growth in personnel and launch readiness expenses.

Stoke Webcast and Conference Call for Analysts and Investors

Stoke management will host a webcast and conference call for analysts and investors on Monday, August 3, 2026, at 4:30PM Eastern Time. The webcast will be available on the Investors & News section of Stoke's website at https://investor.stoke therapeutics.com/ . Research analysts who plan to join the call and participate in the Q&A session may register here to receive the dial-in details and a unique PIN. All other participants are invited to access the listen-only webcast by clicking here . A replay of the webcast will be archived and available for at least 90 days following the event.

About Dravet Syndrome

Dravet syndrome is a severe developmental and epileptic encephalopathy (DEE) characterized by recurrent seizures as well as significant cognitive and behavioral impairments. Most cases of Dravet are caused by mutations in one copy of the SCN1A gene, leading to insufficient levels of NaV1.1 protein in neuronal cells in the brain. Even when treated with the best available anti-seizure medicines (ASMs), up to 57 percent of patients with Dravet syndrome do not achieve ≥50 percent reduction in seizure frequency. Complications of the disease often contribute to a poor quality of life for patients and their caregivers. Developmental and cognitive impairments often include intellectual disability, developmental delays, movement and balance issues, language and speech disturbances, growth defects, sleep abnormalities, disruptions of the autonomic nervous system and mood disorders. Compared with the general epilepsy population, people living with Dravet syndrome have a higher risk of sudden unexpected death in epilepsy, or SUDEP; up to 20 percent of children and adolescents with Dravet syndrome die before adulthood due to SUDEP, prolonged seizures, seizure-related accidents or infections 1 . Dravet syndrome occurs globally and is not concentrated in a particular geographic area or ethnic group. Currently, it is estimated that up to 38,000 people are living with Dravet syndrome in the U.S. (~16,000), UK, EU-4 and Japan 2 . There are no approved disease-modifying therapies for people living with Dravet syndrome.

About Zorevunersen

Zorevunersen is an investigational antisense oligonucleotide that is designed to treat the underlying cause of Dravet syndrome by increasing functional NaV1.1 protein production in brain cells from the unaffected (wild-type) copy of the SCN1A gene. This highly differentiated mechanism of action aims to reduce seizure frequency beyond what has been achieved with anti-seizure medicines and to improve neurodevelopment, cognition and behavior. Zorevunersen has demonstrated the potential for disease modification and has been granted orphan drug designation by the FDA and the EMA. The FDA has also granted zorevunersen rare pediatric disease designation and Breakthrough Therapy Designation for the treatment of Dravet syndrome with a confirmed mutation not associated with

EX 99.1

gain-of-function in the SCN1A gene, and China's Center for Drug Evaluation has granted zorevunersen Breakthrough Therapy Designation. Stoke has a strategic collaboration with Biogen (Nasdaq: BIIB) to develop and commercialize zorevunersen for Dravet syndrome. Under the collaboration, Stoke retains exclusive rights for zorevunersen in the United States, Canada, and Mexico; Biogen receives exclusive rest of world commercialization rights. Zorevunersen is currently in clinical development, and its safety and efficacy have not been evaluated by any regulatory authority.

About the Phase 1/2a and Open-Label Extension Studies

Two Phase 1/2a open-label, multicenter studies evaluated the effects of zorevunersen in patients with highly refractory Dravet syndrome ages 2 to 18 years (N=81). Primary endpoints were the safety profile, plasma pharmacokinetics (PK) and exposure in cerebrospinal fluid (CSF) of single and multiple doses of zorevunersen. Secondary endpoints included percentage change from baseline in major motor seizure frequency, overall clinical status (a measure of patients' overall functioning) and quality of life. The ADMIRAL Phase 1/2a study included an exploratory endpoint to evaluate changes in neurodevelopmental status (cognition & behavior) as measured by Vineland Adaptive Behavior Scales, Third Edition (Vineland-3). The Phase 1/2a studies were completed in November 2023. Following treatment in the Phase 1/2a studies, eligible patients continued treatment with zorevunersen every four months in one of two OLEs. There was at least a 6-month gap between the last dose administered in the Phase 1/2a studies and the first dose administered in the OLEs. The primary endpoints are the safety profile of multiple doses of zorevunersen. Secondary endpoints include PK parameters, percentage change from baseline in major motor seizure frequency, change in overall clinical status, and change from baseline in quality of life. Exploratory endpoints include changes in neurodevelopment status as measured by Vineland-3. The OLE studies are ongoing.

About the Phase 3 EMPEROR Study

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-16_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a late-stage clinical company dedicated to addressing the underlying causes of severe diseases by upregulating protein expression with RNA-based medicines. Using our proprietary TANGO (Targeted Augmentation of Nuclear Gene Output) approach, we are developing antisense oligonucleotides ("ASOs") to selectively restore protein levels.

Our first investigational new medicine in development, zorevunersen (STK-001), is a potential disease modifying medicine that is in late-stage clinical testing for the treatment of Dravet syndrome. Dravet syndrome is characterized by frequent, prolonged and refractory seizures beginning within the first year of life. The disease is classified as a developmental and epileptic encephalopathy (DEE) due to the developmental delays and cognitive impairment associated with it. Dravet syndrome is one of many diseases caused by a haploinsufficiency, in which a loss of approximately 50% of normal protein levels leads to disease.

Following discussions with the U.S. Food and Drug Administration ("FDA"), European Medicines Agency ("EMA"), and Japan's Pharmaceuticals and Medical Devices Agency ("PMDA"), a global Phase 3 study, EMPEROR, was initiated in May 2025, with the first patient dosed in August 2025. This trial follows the completion of two open-label Phase 1/2a studies, MONARCH in the United States and ADMIRAL in the United Kingdom, and further evaluates the efficacy and safety of zorevunersen in children and adolescents ages 2 to up to 18 with Dravet syndrome.

In addition to the MONARCH and ADMIRAL studies, we continue to run open-label extension ("OLE") studies in patients who completed the Phase 1/2a studies and met study entry criteria. The four studies have shown substantial and durable reductions in convulsive seizure frequency when administered on top of standard of care anti-seizure medicines. In the Phase 1/2a studies, 85% of patients were taking at least three and 54% were taking at least four medicines to control seizures. Half the patients in the studies were taking concomitant fenfluramine. Ongoing treatment has led to continuous improvements in cognition and behavior through three years. Additional improvements were indicated within the first nine months of treatment among patients in the Phase 1/2a study. These improvements were observed across multiple domains of the Vineland-3 (Vineland Adaptive Behavior Scale, Third Edition), a standardized assessment of behavioral outcomes that is a key secondary endpoint for the Phase 3 study. Zorevunersen has been generally well tolerated across the studies.

In addition to our Dravet program, we are also pursuing treatment for a second haploinsufficient disease, autosomal dominant optic atrophy ("ADOA"), the most common inherited optic nerve disorder for which there are currently no approved treatments. STK-002 is our clinical candidate for the treatment of ADOA. STK-002 is designed to upregulate OPA1 protein expression by leveraging the non-mutant (wild-type) copy of the OPA1 gene to restore OPA1 protein expression with the aim to stop or slow vision loss in patients with ADOA. In a non-human primate (NHP) model of ADOA conducted in collaboration with UC Davis, treatment with STK-002 was well tolerated and helped protect, and possibly improve, eye health. The data suggest that STK-002 may help preserve the function of important vision-related nerve cells, which could potentially improve or maintain vision. We received authorization in the UK to proceed with a Phase 1 open-label study (OSPREY) of children and adults ages 6 to 55 who have an established diagnosis of ADOA and have evidence of a genetic mutation in the OPA1 gene. In February 2026, we dosed the first patient with STK-002 in the OSPREY Phase 1 study for the treatment of ADOA.

In terms of our liquidity and capital resources, in May 2022, we filed a universal Shelf Registration statement on Form S-3 (the "2022 Registration Statement") with the SEC. The 2022 Registration Statement was declared effective by the SEC on May 31, 2022, and contained two prospectuses: a base prospectus, which covered the offering, issuance and sale by us of up to a maximum aggregate offering price of $400.0 million of our common stock, preferred stock, debt securities, warrants to purchase common stock, preferred stock or debt securities, subscription rights to purchase common stock, preferred stock or debt securities and/or units consisting of some or all of these securities; and a sales agreement prospectus covering the offering, issuance and sale by us of up to a maximum aggregate offering price of $150.0 million of common stock that may be issued and sold under a Controlled Equity Offering Sales Agreement (the "Sales Agreement").

On April 2, 2024, we completed an underwritten public offering, pursuant to the 2022 Registration Statement, of 5,555,557 shares of common stock at a public offering price of $13.50 per share and issued pre-funded warrants to purchase

3,703,730 shares of common stock at a public offering price of $13.499 per share subject to an exercise price equal to $0.0001. The common stock and pre-funded warrants sold resulted in net proceeds of approximately $119.9 million after deducting underwriting discounts, commissions and offering costs. No pre-funded warrants have been exercised as of December 31, 2025.

In October 2024, we filed an automatic universal Shelf Registration statement on Form S-3 (the "2024 Registration Statement") with the SEC. Following the filing of our Annual Report on Form 10-K for the year ended December 31, 2024 in March 2025, the 2024 Registration Statement became ineffective.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations for the Years Ended December 31, 2025 and 2024

The following table sets forth our results of operations (in thousands):

Year ended December 31,
2025 | 2024
Consolidated statements of operations
Revenue | 184,420 | 36,555
Operating expenses:
Research and development | 137,922 | 89,133
Sales, general and administrative | 67,088 | 48,794
Total operating expenses | 205,010 | 137,927
Loss from operations | (20,590 | (101,372
Other income (expense):
Interest income, net | 13,756 | 12,638
Other income (expense), net | (51 | (247
Total other income (expense) | 13,705 | 12,391
Net loss | (6,885 | (88,981

Revenue

Revenue for the year ended December 31, 2025 was $184.4 million compared to $36.6 million for the year ended December 31, 2024, an increase of $147.8 million. Revenue is generated from satisfying contractual obligations of the collaboration and licensing agreements with Acadia and Biogen. The increase of $147.8 million is primarily driven by revenue of $150.8 million related to the IP license performance obligation and $17.5 million for global development activities as part of the Biogen Agreement offset by a decrease in revenue related to the Acadia Agreement.

Research and development expenses

Research and development expenses were $137.9 million for the year ended December 31, 2025 as compared to $89.1 million for the year ended December 31, 2024, an increase of $48.8 million. The table below summarizes our research and development expenses (in thousands):

Year Ended December 31,
2025 | 2024
Zorevunersen | 63,753 | 29,980
ADOA | 5,106 | 5,811
SYNGAP1 | 3,334 | 1,138
MECP2 | (33 | 1,066
Personnel-related expenses | 49,973 | 36,203
Third-party services | 3,189 | 1,111
Scientific consulting | 1,468 | 1,754
Facilities and other research and development expenses | 11,132 | 12,070
Total research and development expenses | 137,922 | 89,133

The increase in research and development expenses was driven primarily by a $33.8 million increase in expenses related to our zorevunersen program, which consisted of third‑party services and scientific consulting fees, $13.8 million increase in personnel‑related costs, a $1.8 million increase in external third‑party expenses related to non–program-specific expenses and $1.1 million in expenses related to SYNGAP1 and MECP2, both of which consisted of third‑party services and scientific consulting fees. These increases were partially offset by a $0.7 million decrease in expenses related to our ADOA program and a $1.0 million decrease in facilities and other non–program-related expenses.

Sales, general and administrative expenses

Sales, general and administrative expenses were $67.1 million for the year ended December 31, 2025 as compared to $48.8 million for the year ended December 31, 2024, an increase of $18.3 million.

The increases in sales, general and administrative expenses was primarily attributable to an increase of $7.4 million in personnel‑related costs, including increases in stock-based compensation expense, from increases in headcount and options awarded and an increase of $10.9 million in third-party services to support our in-house personnel in various aspects of developing and supporting the business including commercialization efforts, human resources, information technology, audit, tax, public relations, communications and other sales, general and administrative activities.

Other income (expense)

Our other income (expense), net includes (i) interest income earned on cash reserves in our operating, money market fund, investment accounts and on our marketable securities investments and (ii) other items of income (expense), net.

Liquidity and Capital Resources

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-16_item1_business.md)

Item 1. Bu siness.

Overview

We are a late-stage clinical company dedicated to addressing the underlying causes of severe diseases by upregulating protein expression with RNA-based medicines. Using our proprietary TANGO (Targeted Augmentation of Nuclear Gene Output) approach, we are developing antisense oligonucleotides ("ASOs") to selectively restore protein levels.

Our first investigational, new medicine in development, zorevunersen (STK-001), is a potential disease modifying medicine that is in late-stage clinical testing for the treatment of Dravet syndrome, a severe and progressive genetic epilepsy. Dravet syndrome is characterized by frequent, prolonged and refractory seizures beginning within the first year of life. The disease is classified as a developmental and epileptic encephalopathy due to the developmental delays and cognitive impairment associated with it. There are currently no disease modifying medicines approved for the treatment of Dravet syndrome.

Dravet syndrome is one of many diseases caused by a haploinsufficiency in which a loss of approximately 50% of normal protein levels leads to disease. Our initial focus is on haploinsufficiencies and diseases of the central nervous system and the eye, although proof of concept has been demonstrated in other organs, tissues, and systems, supporting our belief in the broad potential for our proprietary approach.

Zorevunersen is currently being evaluated in our global Phase 3 clinical study, EMPEROR, which was initiated in May 2025 , with the first patient dosed in August 2025.. We expect to complete enrollment of approximately 150 patients in the second quarter of 2026, with pivotal Phase 3 data anticipated in mid-2027 to support the submission of a New Drug Application ("NDA") to the U.S. Food and Drug Administration ("FDA"). We plan to initiate a rolling NDA submission in the first half of 2027.

This trial follows the completion of two open-label Phase 1/2a studies, MONARCH in the United States and ADMIRAL in the United Kingdom, and further evaluates the efficacy and safety of zorevunersen in children and adolescents ages 2 to up to 18 with Dravet syndrome. The Phase 1/2a and open-label extension ("OLE") studies in patients with Dravet syndrome have provided positive data, showing substantial and durable reductions in convulsive seizure frequency on top of currently available anti-seizure medicines. Additionally, ongoing treatment has led to continuous improvements in cognition and behavior, as measured by Vineland-3 (Vineland Adaptive Behavior Scale, Third Edition), a standardized assessment of behavioral outcomes. Zorevunersen was generally well tolerated across the studies.

We are led by an executive management team that has extensive expertise across human genetics and modulation of RNA processes using ASOs, as well as a track record of success in rare disease drug development, commercialization, and corporate strategy. Our executive team and co-founders have been previously involved with other companies in the discovery, clinical development, business development and commercialization of many treatments for rare diseases, including Vertex's Kalydeco, Sarepta's Exondys 51 (eteplirsen) and Biogen's SPINRAZA. Their collective expertise supports our efforts to advance our pipeline, execute strategic transactions and bring innovative therapies to patients worldwide.

Our strategy

We are using our proprietary RNA therapeutics platform to create ASOs for the treatment of severe diseases. The critical pillars of our strategy include:

•
Deliver zorevunersen to patients as quickly as possible . We believe zorevunersen has the potential to significantly reduce both the occurrence and frequency of seizures and improve non-seizure aspects of Dravet syndrome, such as cognition and behavior. We have robust Phase 1/2a and ongoing OLE data supporting zorevunersen's long-term, disease modifying potential. We have engaged with clinical sites to efficiently recruit patients and project data from our Phase 3 EMPEROR study by mid-2027. In parallel, we continue to leverage Breakthrough Therapy Designation to engage with the FDA to identify opportunities to deliver zorevunersen to patients faster.

•
Expand capabilities to ensure successful commercialization of zorevunersen in the U.S., Canada and Mexico. We continue to invest in our internal capabilities, with a focus on expanding our medical affairs and commercial teams. We are recruiting experienced commercial leaders from across the rare disease space to help identify and access potential patients and educate healthcare providers on the benefits and risks of our medicines. To complement these efforts, we have a collaboration for the development and commercialization of zorevunersen

outside of the United States, Canada, and Mexico (the "Biogen Territory"). We believe that Biogen is the ideal partner given its global capabilities, deep experience in neurology and successful track record commercializing high-value, disease-modifying medicines for rare genetic diseases.

•
Advance and expand our pipeline. We are advancing our second product candidate, STK-002, a potential disease modifying therapy for the treatment of autosomal dominant optic atrophy (ADOA), via an ongoing Phase 1 study. In addition, we are expanding into other disease areas. We leverage proprietary bioinformatics algorithms and extensive in-house expertise in whole-transcriptome RNA sequencing to rapidly and systematically identify diseases that we believe can be addressed using our approach. We are advancing several preclinical programs across multiple disease areas, including the central nervous system (the "CNS") and eye. We will continue to establish strategic collaborations with biopharmaceutical companies whose capabilities and expertise complement our scientific platform.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-16_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-16_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-16_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-03-16_item7_mdna.md, 10-K_2026-03-16_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
