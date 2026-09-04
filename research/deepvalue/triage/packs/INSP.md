# Triage pack — INSP · Inspire Medical Systems, Inc.

_Generated 2026-09-04 17:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** INSP · **Name:** Inspire Medical Systems, Inc.
- **CIK:** 0001609550
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/INSP

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Inspire Medical Systems, Inc.
- **CIK:** 1,609,550 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 62.14 |
| mktcap | $1.8B |
| ev | $1.7B |
| ev_ebit | 32.7x |
| fcf | $78.5M |
| fcf_yield | 4.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 5.8% |
| net_debt | -$127.8M |
| net_debt_ebit | -2.5x |
| cash | $127.8M |
| ltd | $0.00 |
| equity | $825.6M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $912.0M |
| revenue_prior | $802.8M |
| rev_growth | 13.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $51.0M |
| net_income | $145.4M |
| cfo | $117.0M |
| capex | $38.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -2.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 28,910,375 |
| shares_py | 29,574,316 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -29.8% |
| r6m | -0.5% |
| off_52w_high | -56.8% |
| adv20 | $28.6M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.45 |
| r_ev_ebit | 0.26 |
| r_roic | 0.55 |
| r_rev_growth | 0.74 |
| r_buyback | 0.80 |
| score | 0.56 |

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
| rank | 182 |

**Screen rationale:** buying back stock -2.2%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **28,910,375** (CY2026Q2I) vs **29,574,316** prior year (CY2025Q2I)
- Change: **-2.2%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-24** — Item 5.02 (officer / director change or comp arrangement): On July 20, 2026, the Board of Directors (the "Board") of Inspire Medical Systems, Inc. (the "Company"), upon the recommendation of its Nominating and Corporate Governance Committee, appointed Michael H. Carrel to the Board, effective immediately.
- **2026-07-22** — Item 5.02 (officer / director change or comp arrangement): On July 16, 2026, Casey Tansey, a member of the Board of Directors (the "Board") of Inspire Medical Systems, Inc. (the "Company"), notified the Company of his decision to retire from the Board (and the committees on which he serves) and not stand for...
- **2026-05-05** — Item 5.02 (officer / director change or comp arrangement): As reported below under Item 5.07 of this Current Report on Form 8-K (this "Current Report"), on April 30, 2026, Inspire Medical Systems, Inc. (the "Company") held its 2026 Annual Meeting of Stockholders (the "Annual Meeting"), at which the Company's...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 5,000 sh / $233,292 -> net $-233,292 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 4).

| code | rows |
|---|---|
| A | 7 |
| F | 2 |
| S | 4 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'Second quarter diluted EPS of $0.01; adjusted diluted EPS of $0.14'; skipped 11 forward-looking-statement block(s); 7 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (insp2026-q2pressreleaseex9.htm)

• Generated second quarter revenue of $200.6 million

• Second quarter diluted EPS of $0.01; adjusted diluted EPS of $0.14

• Second quarter operating cash flow of $23.2 million

• Announced strategic growth plan designed to unlock and redeploy $30 million for growth initiatives

MINNEAPOLIS, MN - August 3, 2026 - Inspire Medical Systems, Inc. (NYSE: INSP) (Inspire, or the Company), a medical technology company focused on the development and commercialization of innovative, minimally invasive solutions for patients with obstructive sleep apnea, today reported financial results for the quarter ended June 30, 2026.

"Our second quarter results reflect the increased discipline and focus we are bringing to the business as we continue to support customers through the evolving coding and reimbursement environment and invest in the long-term adoption of Inspire therapy," said Tim Herbert, Chairman and CEO of Inspire Medical Systems. "We are also announcing a strategic growth plan designed to generate approximately $30 million of annualized growth investment capacity, which we intend to redeploy into targeted growth initiatives. We believe these actions will strengthen our operating foundation, sharpen our focus on the highest-return opportunities, and position Inspire for sustainable growth and long-term value creation."

Second Quarter 2026 Financial Results (Second Quarter 2026 compared to Second Quarter 2025)

• Revenue decreased 7.6% to $200.6 million, primarily driven by a decline in U.S. revenue, partially offset by growth in International revenue. The U.S. decline was driven primarily by the impacts of evolving coding and reimbursement environment.

• Gross margin increased 150 bps to 85.5%, primarily due to increased sales mix of the Inspire V system, which has a higher gross margin than the Inspire IV system.

• Operating expenses decreased $13.8 million, or 7.4%, to $172.0 million, primarily driven by lower stock-based compensation costs due to accelerated stock-based compensation expenses recognized in the prior year period as well as lower marketing expenses.

• Operating earnings increased $2.8 million to an operating loss of $0.5 million, and operating margin of (0.3)%. Adjusted operating income was $3.2 million, and adjusted operating margin was 1.6%.

• Interest and dividend income, net decreased by $0.7 million, primarily due to lower average interest rates and lower average cash, cash equivalents, and investment balances.

• Other expense, net decreased by $3.4 million, primarily due to a $4.0 million impairment charge recognized in the prior year period, partially offset by a decrease in interest and dividend income in the current period due to lower average interest rates and lower average cash, cash equivalents, and investment balances in the current period.

• The effective tax rate was 89.9% compared to (54.0)%. The increase in the effective tax rate was primarily driven by tax shortfall related to stock-based compensation. For the three months ended June 30, 2025, the Company maintained a full valuation allowance against federal and state deferred tax assets, which was subsequently released at December 31, 2025.

• Net earnings was $0.3 million and adjusted net earnings was $4.0 million.

• Diluted EPS was $0.01 and adjusted diluted EPS was $0.14.

Financial Condition

• Net cash provided by operating activities for the three months ended June 30, 2026 was $23.2 million, compared to $2.7 million in the prior year period. The change was primarily driven by improved working capital, primarily in receivables and inventories.

• As of June 30, 2026, cash, cash equivalents, and investments increased $10.6 million to $415.2 million as compared to December 31, 2025.

Full Year 2026 Guidance

The Company is raising its previously announced revenue outlook to be in the range of $835 million to $875 million. Additionally, the Company now expects annual adjusted operating margin to be in the range of 4% to 6%, diluted EPS to be in the range of $(0.42) to $0.17 and adjusted diluted EPS to be in the range of $1.05 to $1.45.

The Company's outlook assumes an effective tax rate of approximately 95% to 100% and an adjusted effective tax rate of 30% to 35%, estimated weighted average diluted shares outstanding of approximately 29.4 million, and capital expenditures between $35 million to $40 million.

Strategic Growth Plan

On August 3, 2026, the Company announced a strategic growth plan, named Project Horizon, intended to create additional investment capacity to accelerate revenue growth through:

• Aligning resources to revenue growth initiatives;

• Streamlining the organization; and

• Optimizing the Company's supply chain by consolidating production to support quality, scale, and efficiency.

The Company expects to incur a total of $20 million to $25 million of pre-tax restructuring charges in connection with the first phase of Project Horizon, including approximately $4 million to $5 million of employee-related costs, and $16 million to $20 million of other expenses, which will be non-cash in nature. These actions are expected to generate approximately $30 million of annualized growth investment capacity which is expected to be invested in revenue growth initiatives. The Company expects the majority of actions related to the restructuring to be completed in the third quarter and all actions to be substantially complete by the end of 2026.

Webcast and Conference Call

The Company's management will host a conference call after market close today, Monday, August 3, 2026, at 5:00 p.m. Eastern Time to discuss these results and answer questions.

To access the conference call, please preregister on

https://register-conf.media-server.com/register/BI05401f2d26b24d47a1416936675b79be .

Registrants will receive confirmation with dial-in details.

A live webcast of the event can be accessed on https://edge.media-server.com/mmc/p/qu4ekmuy/ . A replay of the webcast will be available on https://investors.inspiresleep.com starting approximately two hours after the event and archived on the site for two weeks.

About Inspire Medical Systems

Inspire Medical Systems is a medical technology company focused on the development and commercialization of innovative, minimally invasive solutions for patients with obstructive sleep apnea. Inspire's proprietary Inspire therapy is the first FDA, EU MDR, and PDMA-approved neurostimulation technology that provides a safe and effective treatment for moderate to severe obstructive sleep apnea.

For additional information about Inspire, please visit www.inspiresleep.com .

Use of Non-GAAP Financial Measures

This press release includes non-GAAP financial measures, including without limitation, adjusted operating income, adjusted operating margin, adjusted earnings before income taxes, adjusted income tax expense, adjusted effective tax rate, adjusted net earnings, adjusted net earnings per diluted share ("EPS"), adjusted EBITDA, and adjusted EBITDA margin, which differ from financial measures calculated in accordance with U.S. generally accepted accounting principles ("GAAP").

We define adjusted operating income as operating income or loss adjusted for items that are not indicative of our ongoing operations. Operating income is the most directly comparable GAAP financial measure to adjusted operating income. We define adjusted operating margin in this release as adjusted operating income divided by revenue. Operating margin is the most directly comparable GAAP financial measure to adjusted operating margin. Adjusted earnings before income taxes is defined as earnings before income taxes, adjusted for items that are not indicative of our ongoing operations. Earnings before income taxes is the most directly comparable GAAP financial measure. Adjusted income tax expense is defined as income tax expense, adjusted for items that are not indicative of our ongoing operations. Adjusted effective tax rate is adjusted income tax expense divided by adjusted earnings before income taxes. Income tax expense is the most directly comparable GAAP financial measure. Adjusted net earnings is defined as net earnings or loss, adjusted for items that are not indicative of our ongoing operations. Net earnings or loss is the most directly comparable GAAP financial measure to adjusted net earnings. Adjusted net earnings per diluted share is calculated as adjusted net earnings divided by the diluted weighted average shares outstanding. Net earnings or loss per diluted share is the most directly comparable GAAP financial measure to adjusted net earnings per diluted share. We define adjusted EBITDA as net earnings or loss, less interest and dividend income, net, plus income tax expense, plus depreciation and amortization, plus stock-based compensation expense, adjusted for items that are not indicative of our ongoing operations. Net earnings or loss is the most directly comparable GAAP financial measure to adjusted EBITDA. We define adjusted EBITDA margin in this release as adjusted EBITDA divided by revenue. Net earnings or loss margin is the most directly comparable GAAP measure to adjusted EBITDA margin. Reconciliations of these non-GAAP financial measures to their most directly comparable GAAP measures are included in this press release.

These non-GAAP financial measures are presented because we believe they are useful indicators of our operating performance and facilitate a more meaningful trend analysis without the distortion of various adjustment items. Management uses these measures principally as measures of our underlying operating performance, trends, and for planning purposes, including the preparation of our annual operating plan and financial projections. We believe these measures are useful to investors as supplemental information and because they are frequently used by analysts, investors, and other interested parties to evaluate companies in our industry. We also believe these non-GAAP financial measures are useful to our management and investors as a measure of comparative operating performance from period to period.

These non-GAAP financial measures should not be considered as an alternative to, or superior to, the most directly comparable GAAP financial measures, as measures of financial performance or cash flows from operations, as a measure of liquidity, or any other performance measure derived in accordance with GAAP, and they should not be construed to imply that our future results will be unaffected by unusual or non-recurring items. In addition, Adjusted EBITDA is not intended to be a measure of cash flow for management's discretionary use, as it does not reflect certain cash requirements such as tax payments, capital expenditures, and certain other cash costs that may recur in the future. Adjusted EBITDA contains certain other limitations, including the failure to reflect our cash expenditures, cash requirements for working capital needs, and cash costs to replace assets being depreciated and amortized. In evaluating our non-GAAP financial measures, you should be aware that in the future we may incur expenses that are the same as or similar to some of the adjustments in this presentation. Our presentation of non-GAAP financial measures should not be construed to imply that our future results will be unaffected by any such adjustments. Management compensates for these limitations by primarily relying on our GAAP results in addition to using non-GAAP financial measures on a supplemental basis. These measures and their definitions are discussed in more detail below and our definition of these non-GAAP financial measures is not necessarily comparable to other similarly titled captions of other companies due to different methods of calculation.

Consolidated Statements of Operations (unaudited)

(in thousands, except share and per share amounts)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-13_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a medical technology company focused on the development and commercialization of innovative, minimally invasive solutions for patients with obstructive sleep apnea ("OSA"). Our proprietary Inspire system is the only FDA, European Union ("EU") Medical Devices Regulation ("MDR"), and Japan Pharmaceuticals and Medical Devices Agency-approved neurostimulation technology of its kind that provides a safe and effective treatment for patients with moderate to severe OSA. We have developed a novel, closed-loop solution that continuously monitors a patient's breathing and delivers mild hypoglossal nerve stimulation to maintain an open airway. Inspire therapy is indicated for patients with moderate to severe OSA who do not have significant central sleep apnea and do not have a complete concentric collapse of the airway at the soft palate level.

We sell our Inspire system to hospitals and ambulatory surgery centers ("ASCs") in the U.S. and in select countries in Europe and Japan through a direct sales organization and we sell our Inspire system in Singapore, Hong Kong, and Thailand through distributors. Our direct sales force engages in sales efforts and promotional activities primarily focused on ENT physicians and sleep centers. In addition, we highlight our compelling clinical data and value proposition to increase awareness and adoption amongst referring physicians. We build upon this top-down approach with strong direct-to-consumer marketing initiatives to create awareness of the benefits of our Inspire system and drive interest through patient empowerment. We believe this outreach helps to educate thousands of patients on our Inspire therapy.

Although our sales and marketing efforts are directed at patients and physicians because they are the primary users of our technology, we consider the hospitals and ASCs where the procedure is performed to be our customers, as they are the purchasing agents of our Inspire system. Our customers are reimbursed according to the coding and correlated payment by various third-party payors, such as commercial payors and government healthcare programs. Our Inspire system is currently covered on a per-patient basis for patients insured by commercial payors, under Local Coverage Determinations for patients insured by Medicare and Medicare Advantage, and under U.S. government contract for patients who are treated by the Veterans Health Administration. As of February 13, 2026, we have secured positive coverage policies with many U.S. commercial payors, including all large national commercial insurers, covering more than 300 million lives in the U.S. In addition, all seven Medicare Administrative Contractors provide coverage of Inspire therapy when certain coverage criteria are met.

Third-party payors require physicians and hospitals to identify the service for which they are seeking reimbursement by using Current Procedural Terminology ("CPT") codes, which are created and maintained by the American Medical Association. Our various generations of Inspire therapy have been billed under different codes and reimbursement approaches throughout our history. For example, the procedures performed to implant our Inspire IV device are described for billing purposes using Category I CPT code 64582. And for 2025, the procedures performed to implant our Inspire V device were described for billing purposes using Category I CPT code 64568. There are also other relevant CPT codes for revisions, explants and DISE.

In November 2025, the final 2026 Medicare reimbursement payments were announced. There has been, and still is currently, confusion on the appropriate reimbursement and coding for our products from CMS and Medicare Administrative Contractors ("MACs"), as well as other payors and stakeholders in the overall reimbursement and coding process. Most recently, we received clarification regarding the coding that should be used for the Inspire V procedure. Currently, healthcare centers and physicians should bill the most recent healthcare policies, be it a Medicare Administrative Contractor (MACs) or a commercial payor, and based on this clarification, we believe the

code will transition to CPT code 64582 for the Inspire V procedure, including the use of a -52 modifier. To date, our top commercial payers by volume have all adopted the guidance of 64568 for coding and reimbursement of Inspire V. Confusion will remain until there is definitive and public guidance from various stakeholders and we have sufficient claims data that has been submitted and processed across payers. The resulting coding and reimbursement decisions may impact our business, financial condition and results of operations, in particular our future revenues. We continue to work with the relevant stakeholders to get specific and accurate direction for Inspire V coding, including the -52 modifier that we would expect to reduce the professional fee for Inspire V procedures under CPT code 64582 by approximately 10% to 50% of the base rate. In any case, we believe that a significant decrease in the professional fee resulting from use of the –52 modifier will likely influence physicians' willingness to perform the Inspire V procedure and may limit the number of cases they choose to undertake. Beyond our short-term initiatives intended to minimize the actual reduction applied to the professional fee, as well as to drive consistency across the country, we are seeking a long-term solution, including the creation of a separate CPT code. There can be no guarantee as to the timing or outcome of the CPT code to be applied.

Reimbursement in other countries can often be established through a combination of private (commercial insurance) and public funding sources, or at the hospital level through innovation budgets.

For the year ended December 31, 2025, 95.6% of our revenue was derived in the U.S. and 4.4% was derived outside of the U.S. No single customer accounted for more than 10% of our revenue.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Year Ended December 31, 2025 Compared to Year Ended December 31, 2024

Year Ended December 31, | Change
2025 | 2024 | %
(in thousands, except percentages)
Revenue | 911,981 | 802,804 | 109,177 | 13.6 | %
Cost of goods sold | 133,225 | 122,986 | 10,239 | 8.3 | %
Gross profit | 778,756 | 679,818 | 98,938 | 14.6 | %
Gross margin | 85.4 | % | 84.7 | %
Operating expenses:
Research and development | 103,165 | 114,128 | (10,963) | (9.6) | %
Selling, general and administrative | 624,637 | 529,607 | 95,030 | 17.9 | %
Total operating expenses | 727,802 | 643,735 | 84,067 | 13.1 | %
Operating income | 50,954 | 36,083 | 14,871 | 41.2 | %
Other income, net | (14,743) | (22,370) | 7,627 | (34.1) | %
Income before income taxes | 65,697 | 58,453 | 7,244 | 12.4 | %
Income taxes | (79,725) | 4,944 | (84,669) | (1712.6) | %
Net income | 145,422 | 53,509 | 91,913 | 171.8 | %

Revenue

Revenue increased $109.2 million, or 13.6%, to $912.0 million for the year ended December 31, 2025, compared to the year ended December 31, 2024. The increase was attributable to a $101.0 million increase in sales of our Inspire system in the U.S and an increase of $8.1 million outside of the U.S. Overall revenue growth was primarily due to increased market penetration, and, we believe, increased physician and patient awareness of our Inspire system, partially offset by ENT surgeon capacity constraints and some U.S. patients and physicians delaying Inspire therapy until Inspire V is available at their location or while they trial GLP-1 medications.

Revenue information by region is summarized as follows:

Year Ended December 31,
2025 | 2024 | Change
Amount | % of Revenue | Amount | % of Revenue | %
(in thousands, except percentages)
United States | 872,086 | 95.6 | % | 771,040 | 96.0 | % | 101,046 | 13.1 | %
All other countries | 39,895 | 4.4 | % | 31,764 | 4.0 | % | 8,131 | 25.6 | %
Total revenue | 911,981 | 100.0 | % | 802,804 | 100.0 | % | 109,177 | 13.6 | %

Revenue generated in the U.S. was $872.1 million for the year ended December 31, 2025, an increase of $101.0 million, or 13.1%, over the year ended December 31, 2024. Revenue growth in the U.S. was primarily due to increased market penetration, and, we believe, increased physician and patient awareness of our Inspire system, partially offset by ENT surgeon capacity constraints and some patients and physicians delaying Inspire therapy until Inspire V is available at their location or while they trial GLP-1 medications.

Revenue generated outside of the U.S. was $39.9 million in the year ended December 31, 2025, an increase of $8.1 million, or 25.6%, over the year ended December 31, 2024. Revenue growth outside the U.S. was primarily due to increased market penetration, and, we believe, increased physician and patient awareness of our Inspire system.

Cost of Goods Sold and Gross Margin

Cost of goods sold increased $10.2 million, or 8.3%, to $133.2 million for the year ended December 31, 2025 compared to $123.0 million for the year ended December 31, 2024. The increase was primarily due to product costs associated with the higher sales volume of our Inspire system, and to a lesser extent, the $2.1 million charge associated with excess components related to Inspire IV.

Gross margin was 85.4% for the year ended December 31, 2025 compared to 84.7% for the year ended December 31, 2024. This increase was primarily due to increased sales volume as well as increased sales mix of the Inspire V system, which is less expensive to manufacture and therefore has a higher gross margin than the Inspire IV system, partially offset by the excess inventory component charge discussed above.

Research and Development Expenses

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-13_item1_business.md)

Item 1. Business.

Overview

We are a medical technology company focused on the development and commercialization of innovative, minimally invasive solutions for patients with obstructive sleep apnea ("OSA"). Our proprietary Inspire system is the first FDA, European Union ("EU") Regulation No. 2017/745 ("MDR" or "EU Medical Devices Regulation"), and Japan Pharmaceuticals and Medical Devices Agency-approved neurostimulation technology of its kind that provides a safe and effective treatment for patients with moderate to severe OSA. We have developed a novel, closed-loop solution that continuously monitors a patient's breathing and delivers mild hypoglossal nerve stimulation to maintain an open airway. A significant body of clinical data, which includes a publication in the New England Journal of Medicine , multiple publications in leading respiratory, ear, nose and throat ("ENT") and sleep medicine journals, and more than 385 peer-reviewed publications, supports the safety and efficacy of Inspire therapy. Inspire therapy received premarket approval ("PMA") from the FDA in 2014 and has been commercially available in certain European markets since 2011. Japan's Ministry of Health, Labour and Welfare ("MLHW") approved Inspire therapy to treat moderate to severe OSA in 2018. Inspire therapy is indicated for patients with moderate to severe OSA who do not have significant central sleep apnea and do not have a complete concentric collapse of the airway at the soft palate level. Physicians have treated more than 125,000 patients with Inspire therapy across the United States ("U.S."), Europe, and Asia.

Sleep apnea is a serious and chronic disease that negatively impacts a patient's sleep, health, and quality of life. OSA is the most common form of sleep apnea. OSA occurs when a person's breathing is interrupted during sleep by a partially or completely blocked airway and affects patients of all ages, sexes, and body types. The severity of OSA is measured by the number of partial or complete airway blockages that a patient experiences in an hour, referred to as the apnea-hypopnea index ("AHI"). Moderate OSA patients have an AHI of 15 to 30 events per hour, while severe OSA patients have an AHI of 30 more events per hour. Left untreated, OSA increases the risk of high blood pressure, hypertension, heart failure, stroke, coronary artery disease, and other life-threatening diseases.

Continuous positive airway pressure ("CPAP") is the leading therapy for patients with moderate to severe OSA. CPAP is delivered through a face or nasal mask that connects through a hose to a bedside air pump. In order for CPAP to be most effective, the mask must form an airtight seal on the patient's face or nose and the mask must be worn every night. The effectiveness of CPAP has been limited by low patient compliance as many patients find the mask or treatment cumbersome, uncomfortable, and loud. When CPAP fails or cannot be tolerated, patients' remaining treatment options consist primarily of invasive surgical procedures developed to modify or remove existing tissue in an attempt to create free air flow. These invasive surgical procedures have limited or unpredictable clinical benefit, are irreversible, and can be extremely painful.

We believe that there continues to be both an urgent clinical need and a strong market opportunity for an alternative to CPAP that is effective and minimally invasive. Data shows that patients with CPAP intolerant OSA have a higher risk for mortality than patients with CPAP-tolerant OSA and higher healthcare utilization rates based on increased cardiovascular health risks. Two findings published in 2022 from Medicare and the French national healthcare insurance databases have demonstrated, in large national cohorts, risks of CPAP intolerance. Specifically, Medicare patients with CPAP intolerance had higher risks of new cardiovascular events than those who were adherent. Similarly, the French national reimbursement database showed that in over 176,000 patients, CPAP non-adherent patients had a higher risk for mortality and new onset of heart failure than those who were adherent. These findings show the urgency of treating CPAP-intolerant OSA to improve patient outcomes and potentially reduce healthcare utilization.

Inspire therapy is an innovative, closed-loop, minimally invasive solution designed to provide comfort and convenience, and which results in high compliance for patients with moderate to severe OSA. Once implanted, the Inspire system delivers electrical stimulation that causes a slight forward movement of the back of the tongue, which helps to maintain an open airway, enabling the patient to inhale freely without interruption. We believe our Inspire therapy provides the following benefits:

• Safe, effective, and durable treatment supported by compelling clinical data, including long-term efficacy results out to five years from initial treatment.

• Closed-loop system that uses a proprietary algorithm to continuously monitor patients' breathing and provide electrical stimulation during the inspiratory phase.

• Comfortable and convenient therapy resulting in high patient satisfaction that was reported to be 90% in patients who were followed an average of 12 months from initial treatment, according to the most recent publication of our ongoing global patient registry.

• Strong patient compliance , with 80% of patients reporting continued nightly use through five years from initial treatment in our Stimulation Therapy for Apnea Reduction ("STAR") trial.

• Minimally invasive outpatient procedure with short recovery time.

• Long-lasting solution with a battery designed to last approximately 11 years without charging or maintenance.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-13_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-13_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-13_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-02-13_item7_mdna.md, 10-K_2026-02-13_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
