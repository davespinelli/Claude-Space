# Triage pack — NPCE · NeuroPace Inc

_Generated 2026-09-05 00:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** NPCE · **Name:** NeuroPace Inc
- **CIK:** 0001528287
- **SIC:** 3841 — Surgical & Medical Instruments & Apparatus
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/NPCE

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** NeuroPace Inc
- **CIK:** 1,528,287 · **SIC:** 3841 (Surgical & Medical Instruments & Apparatus) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 14.75 |
| mktcap | $506.3M |
| ev | $552.8M |
| ev_ebit | n/a |
| fcf | -$11.3M |
| fcf_yield | -2.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -22.1% |
| net_debt | $46.5M |
| net_debt_ebit | n/a |
| cash | $12.5M |
| ltd | $59.0M |
| equity | $11.9M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $100.0M |
| revenue_prior | $79.9M |
| rev_growth | 25.1% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$16.3M |
| net_income | -$21.5M |
| cfo | -$11.0M |
| capex | $332k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 3.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 34,324,274 |
| shares_py | 33,081,498 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 46.4% |
| r6m | 8.5% |
| off_52w_high | -23.5% |
| adv20 | $2.3M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.15 |
| r_ev_ebit | 0.00 |
| r_roic | 0.05 |
| r_rev_growth | 0.87 |
| r_buyback | 0.23 |
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
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 400 |

**Screen rationale:** revenue +25.1%; 12-1 momentum 46.4%


## 3. Share count trend

- Shares outstanding: **34,324,274** (CY2026Q2I) vs **33,081,498** prior year (CY2025Q2I)
- Change: **3.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 15 |
| F | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-11_2-02-results.md)

_Extraction: started at the first release heading, 'NeuroPace Reports Second Quarter 2026 Financial Results and Raises 202'; skipped 9 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99 - EX-99.1 (exhibit991_q22026earningsr.htm)

NeuroPace Reports Second Quarter 2026 Financial Results and Raises 2026 Revenue Guidance

Q2 2026 total revenue of $22.8 million, including $22.5 million in RNS revenue representing 21% growth

Raises full year 2026 total revenue guidance to $99.5 million to $101.5 million, which assumes 21% to 23% growth in core RNS ® revenue from existing indications

Preparation remains on track for SIR meeting with FDA regarding the IGE PMA supplement, supported by

24-month NAUTILUS data showing a 100% median reduction in GTC seizures among evaluable patients 1

Mountain View, Calif. – August 11, 2026 – NeuroPace, Inc. (Nasdaq: NPCE), a medical device company focused on transforming the lives of people living with epilepsy, today reported financial results for the second quarter ended June 30, 2026, and provided a corporate update.

Second Quarter 2026 Financial Highlights

• Total revenue of $22.8 million in the second quarter of 2026

• RNS System revenue of $22.5 million in the quarter, representing 21.3% growth compared to the second quarter of 2025

• Net loss in the second quarter of 2026 was ($6.2) million compared to ($10.0) million in the second quarter of 2025

• Adjusted EBITDA loss of ($2.8) million for the second quarter of 2026, an improvement of $2.1 million compared to a loss of ($4.9) million in the second quarter of 2025

Second Quarter 2026 Operational & Strategic Highlights

• Launched ECoG Assistant™, the first in a planned suite of NeuroPace AI-based clinical decision support tools, uniquely enabled by NeuroPace's proprietary long-term intracranial EEG dataset and designed to help physicians more efficiently review ECoG data and inform individualized treatment decisions

• Published 18-month NAUTILUS results in Epilepsia , a leading peer-reviewed epilepsy journal, providing Level 1 evidence from the first randomized controlled neuromodulation trial in drug-resistant IGE and demonstrating a 77% median reduction in GTC seizures.

• Reached new all-time highs in active prescribers, accounts and patient pipeline

"Second-quarter performance showed continued momentum in our core RNS business driven by increased adoption within our current focal epilepsy indication," said Joel Becker, Chief Executive Officer of NeuroPace. "We also maintained strong financial discipline while continuing to invest in the long-term growth of the business and advance our product roadmap. The launch of ECoG Assistant marked an important first-of-its-kind step in extending the differentiated capabilities of the RNS System, building on NeuroPace's unique ability to continuously monitor and record each patient's intracranial EEG data, efficiently identify ECoGs of interest and support more individualized therapy, reinforcing a data advantage that other neuromodulation platforms cannot replicate.

Looking ahead, we remain focused on sustaining momentum in our core business. Additionally, we look forward to continuing our engagement with the FDA regarding the path forward for our IGE PMA Panel Track supplement and remain on track with our clinical and regulatory timelines".

1 Based on participants who received stimulation for 23 of 24 months following implant and had completed 24-month follow-up with evaluable data.

Discontinued Operations & Basis of Presentation

Following the expiration of the Company's distribution agreement with DIXI Medical and the related wind-down, the Company concluded in the second quarter of 2026 that the abandonment of its DIXI Medical product operations met the criteria for presentation as a discontinued operation under ASC 205-20. Unless otherwise noted, the results discussed in this release reflect continuing operations; prior-period amounts have been reclassified accordingly, with no effect on previously reported net loss, total assets, total liabilities, or total stockholders' equity. See the accompanying financial statements for the GAAP presentation of continuing and discontinued operations.

Second Quarter 2026 Financial Results

RNS System revenue totaled $22.5 million in the second quarter of 2026, representing growth of 21.3% compared to the second quarter of 2025. Total revenue in the second quarter of 2026 grew 17% to $22.8 million, compared with revenue of $19.5 million in the second quarter of 2025.

Non-GAAP gross margin for the second quarter of 2026 was 83.4%, compared with 84.0% in the second quarter of 2025. The slight year-over-year decline was driven by slightly higher material costs partially offset by favorable pricing. Total GAAP gross margin from continuing operations in the second quarter of 2026 was 82.8%.

Non-GAAP operating expenses in the second quarter of 2026 were $21.9 million, compared with $21.3 million in the second quarter of 2025. GAAP operating expenses in the second quarter of 2026 were $24.0 million.

Non-GAAP sales and marketing expense in the second quarter of 2026 was $11.5 million, compared with $10.7 million in the second quarter of 2025. The year-over-year increase was largely due to personnel-related expenses associated with ongoing scaling of commercial activities and other sales-related expenses.

Non-GAAP research and development expense in the second quarter of 2026 was $6.3 million, compared with $6.0 million in the second quarter of 2025. The year-over-year increase was primarily driven by an increase in product development-related expenses associated with a next-generation platform and AI-enabled tools.

Non-GAAP general and administrative expense in the second quarter of 2026 was $4.1 million compared with $4.6 million in the second quarter of 2025. The year-over-year decline was largely due to one-time expenses incurred in the prior period related to executive transition, partially offset by an increase in personnel-related expenses in the current period.

Non-GAAP loss from operations was ($2.8) million in the second quarter of 2026, compared with loss from operations of ($5.0) million in the second quarter of 2025. Non-GAAP net loss was ($3.9) million for the second quarter of 2026 compared with net loss of ($6.8) million in the second quarter of 2025. GAAP net loss in the second quarter of 2026 was ($6.2) million.

The Company's cash, cash equivalents, short-term investments and restricted cash balance as of June 30, 2026 was $51.9 million compared with $54.8 million at the end of the prior quarter. Long-term borrowings totaled $59.0 million as of June 30, 2026.

Full Year 2026 Financial Guidance

• Increase total revenue guidance for full year 2026 to between $99.5 million and $101.5 million, compared with previously issued guidance of $99 million to $101 million. The higher guidance reflects expected service revenue of approximately $1 million, up from approximately $500,000 previously, while the underlying RNS growth outlook of 21% to 23% remains unchanged. Consistent with previous guidance, this range excludes any contribution from idiopathic generalized epilepsy indication expansion.

• Increase full year non-GAAP gross margin to between 82.0% and 83.0%, an increase compared to 81.5% to 82.5% previously

• Reiterate full year non-GAAP operating expenses to be between $90 million and $92 million, excluding approximately $10 million in stock-based compensation, a non-cash expense

• Increase Adjusted EBITDA to be between ($7.5) million and ($8.5) million compared to previous guidance between ($8.5) million to ($9.5) million

Non-GAAP Measure

To supplement NeuroPace's condensed financial statements presented in accordance with GAAP, the Company uses non-GAAP measures of certain components of financial performance. These non-GAAP measures include Adjusted EBITDA, non-GAAP gross margin, non-GAAP cost of goods sold, non-GAAP sales and marketing expense, non-GAAP research and development expense, non-GAAP general and administrative expense, non-GAAP operating expenses, non-GAAP loss from operations, and non-GAAP net loss from operations. NeuroPace believes the presentation of its non-GAAP financial measures enhances the user's overall understanding of the Company's historical financial performance. The presentation of the Company's non-GAAP financial measures is not meant to be considered in isolation or as a substitute for the Company's financial results prepared in accordance with GAAP, and the Company's non-GAAP measures may be different from non-GAAP measures used by other companies.

Webcast and Conference Call Information

NeuroPace will host a conference call to discuss the second quarter and full year 2026 financial results after market close on Tuesday, August 11, 2026, at 4:30 P.M. Eastern Time. Investors interested in listening to the conference call may do so by accessing a live and archived webcast of the event at https://events.q4inc.com/attendee/246660202 . Individuals interested in participating in the call via telephone may access the call by dialing + 1 (833) 461-5787 and referencing Conference ID 246 660 202. The webcast will be archived on the Company's investor relations website at https://investors.neuropace.com/news-and-events/events and will be available for replay for at least 90 days after the event.

About NeuroPace, Inc.

Based in Mountain View, Calif., NeuroPace is a medical device company focused on transforming the lives of people living with epilepsy by reducing or eliminating the occurrence of debilitating seizures. Its novel and differentiated RNS System is the first and only commercially available, brain-responsive platform that delivers personalized, real-time treatment at the seizure source. This platform can drive a better standard of care for patients living with drug-resistant epilepsy and has the potential to offer a more personalized solution and improved outcomes to the large population of patients suffering from other brain disorders.

Condensed Statements of Operations and Comprehensive Loss

(unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
(in thousands, except for share and per share amounts) | 2026 | 2025 | 2026 | 2025
Revenue | 22,826 | 19,501 | 44,829 | 37,822
Cost of goods sold | 3,920 | 3,288 | 7,912 | 6,478
Gross profit | 18,906 | 16,213 | 36,917 | 31,344
Operating expenses:
Sales and marketing | 12,124 | 11,489 | 23,707 | 21,894
Research and development | 6,898 | 6,845 | 14,087 | 14,285
General and administrative | 5,027 | 6,068 | 9,871 | 10,114
Total operating expenses | 24,049 | 24,402 | 47,665 | 46,293
Loss from continuing operations | (5,143) | (8,189) | (10,748) | (14,949)
Interest income | 523 | 718 | 1,088 | 1,511
Interest expense | (1,539) | (2,059) | (3,060) | (4,212)
Other income (expense), net | (41) | (486) | (206) | (568)
Net loss and comprehensive loss from continuing operations | (6,200) | (10,016) | (12,926) | (18,218)
Net income from discontinued operations | — | 1,365 | 37 | 2,978
Net loss and comprehensive loss | (6,200) | (8,651) | (12,889) | (15,240)
Net loss per share from continuing operations attributable to common stockholders, basic and diluted | (0.18) | (0.30) | (0.38) | (0.57)
Net income per share from discontinued operations attributable to common stockholders, basic and diluted | 0.00 | 0.04 | 0.00 | 0.10
Net loss per share attributable to common stockholders, basic and diluted | (0.18) | (0.26) | (0.38) | (0.47)
Weighted-average shares used in computing net loss per share attributable to common stockholders, basic and diluted | 34,104,430 | 32,863,031 | 33,911,692 | 32,175,789

NeuroPace, Inc.

Condensed Balance Sheets

(unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-03_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a medical device company focused on transforming the lives of people living with epilepsy by reducing or eliminating the occurrence of debilitating seizures. Our novel and differentiated RNS System is the first and only commercially available, brain-responsive neuromodulation system that delivers personalized, real-time treatment at the seizure source. By continuously monitoring and analyzing the brain's electrical activity, recognizing patient-specific abnormal electrical patterns, and responding in real time with imperceptible electrical pulses to prevent seizures, our RNS System delivers the precise amount of therapy when and where it is needed and provides exceptional clinical outcomes with approximately three minutes of stimulation on average per day. Our RNS System is also the only commercially available device that records continuous brain activity data and allows clinicians to monitor patients not only in person, but also remotely, providing them the data they need to make more informed treatment decisions, thus optimizing patient care. We believe the therapeutic advantages of our RNS System, combined with the insights obtained from our extensive brain data set, offer a significant leap forward in epilepsy treatment.

Our RNS System is currently indicated in the United States for use in adult epilepsy patients, meaning patients who are 18 years of age or older, with drug-resistant focal epilepsy. Primary effectiveness endpoint data from our Post-approval Study in this patient population demonstrated that the RNS System efficacy improved over time, with a 62.5% median seizure reduction at six months after implant (n=314) and an 82.0% median seizure reduction at 36 months after implant (n=255). Additionally, 42.5% of patients experienced a period of seizure-freedom for at least six months, and 22% of patients were seizure free for at least one year were presented at the American Academy of Neurology Annual Meeting in April 2025.

We are conducting studies to expand our indication for use in patients with drug-resistant idiopathic generalized epilepsy and patients with drug-resistant focal epilepsy under the age of 18. In March 2025, the last patient in our NAUTILUS study for drug-resistant idiopathic generalized epilepsy completed one year of follow up. In May 2025, we announced the preliminary results from the NAUTILUS study based on analysis of the one-year data. The study met the 12-week post-implant primary safety endpoint, demonstrating excellent safety outcomes and confirming the favorable safety profile of the RNS System. While the primary effectiveness endpoint did not reach statistical significance in the overall study, pre-specified secondary endpoints did show meaningful and clinically significant seizure reduction. In December 2025, we filed the Premarket Approval Supplement, or PMA-S, to support label expansion for our RNS System in patients who have drug-resistant idiopathic generalized epilepsy. The PMA-S is supported by pre-specified secondary endpoint data, which demonstrated robust 77% median GTC seizure reduction and a favorable safety profile in this highly refractory patient population at 18 months of therapy. Patients in the NAUTILUS trial continue to participate in the study through the completion of two years after the device implant, with prespecified collection of safety and effectiveness data occurring upon completion of the two years post-implant, and we anticipate the final patient two-year completion in the first half of 2026.

In 2025, in an effort to further support the pediatric focal epilepsy label expansion efforts that we began with the RESPONSE study, we began a collaboration with the National Evaluation System for health Technology, or NEST, and the FDA to pursue the use of real-world data to support expanded labeling for patients ages 12 to 17. These efforts are continuing into 2026.

Our commercial efforts have historically been focused on growing adoption and utilization across Level 4 comprehensive epilepsy centers, or CECs, in the United States that facilitate appropriate care for drug-resistant epilepsy patients. In 2023, we received FDA approval of a PMA-S which updated the qualification criteria for centers and clinicians that may prescribe and implant the RNS System. We initiated a pilot program to begin our outreach to these centers and clinicians in 2024 and are expanding these efforts through 2025. We are actively addressing this opportunity in a targeted manner with incremental expansion of our sales force.

Since our inception, we have generated significant losses. We have financed our operations primarily through sales of our products, issuance of equity securities, and debt financing. As of December 31, 2025, we had an accumulated deficit of $552.4 million, cash, cash equivalents and short-term investments of $61.1 million, and $58.9 million of outstanding debt under a term loan, net of debt discount and issuance costs.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Comparison of the Years Ended December 31, 2025 and 2024

The following table summarizes our results of operations for the periods indicated:

Years Ended December 31,
(in thousands) | 2025 | 2024 | Change | % Change
Revenue | 99,986 | 79,906 | 20,080 | 25 | %
Cost of goods sold | 22,766 | 20,821 | 1,945 | 9 | %
Gross profit | 77,220 | 59,085 | 18,135 | 31 | %
Operating expenses:
Sales and marketing | 46,580 | 39,669 | 6,911 | 17 | %
Research and development | 27,888 | 23,653 | 4,235 | 18 | %
General and administrative | 19,090 | 17,434 | 1,656 | 9 | %
Total operating expenses | 93,558 | 80,756 | 12,802 | 16 | %
Loss from operations | (16,338) | (21,671) | 5,333 | (25) | %
Interest income | 2,816 | 3,024 | (208) | (7) | %
Interest expense | (7,457) | (8,798) | 1,341 | (15) | %
Other income (expense), net | (486) | 304 | (790) | (260) | %
Net loss | (21,465) | (27,141) | 5,676 | (21) | %

Revenue

Revenue increased by $20.1 million, or 25%, to $100.0 million during the year ended December 31, 2025, compared to $79.9 million during the year ended December 31, 2024, due to an increase in the number of RNS System units sold, an increase in sales of DIXI Medical products, and an increase in service revenue. Revenue from sales of DIXI Medical products represented approximately 16% of our total revenue for the year ended December 31, 2025, as compared to approximately 17% for the year ended December 31, 2024. All of our revenue, with the exception of $0.9 million and $0.2 million for the years ended December 31, 2025 and 2024, respectively, was generated from sales in the United States.

Cost of Goods Sold and Gross Margin

Cost of goods sold increased by $2.0 million, or 9%, to $22.8 million during the year ended December 31, 2025, compared to $20.8 million during the year ended December 31, 2024, primarily due to an increase in the number of RNS Systems sold and the costs of distributing DIXI Medical products. Our gross margin increased from 73.9% for the year ended December 31, 2024 to 77.2% for the year ended December 31, 2025, primarily due to lower fixed costs per unit as a result of increased production volume of the RNS System.

Sales and Marketing Expenses

Sales and marketing expenses increased by $6.9 million, or 17%, to $46.6 million during the year ended December 31, 2025, compared to $39.7 million during the year ended December 31, 2024, primarily due to an increase of $4.1 million in personnel-related expenses resulting from an increase in sales and field support personnel costs, including sales commissions, increase in headcount, employee bonus, and one-time severance costs, and an increase of $2.6 million in marketing expenses, including travel, for the year ended December 31, 2025.

Research and Development Expenses

Research and development expenses increased by $4.2 million, or 18%, to $27.9 million during the year ended December 31, 2025, compared to $23.7 million during the year ended December 31, 2024, primarily due to an increase of $2.5 million in personnel-related expenses, including employee bonus and stock-based compensation, driven by an increase in headcount, and a decrease of $1.2 million in grant funds received primarily under the National Institutes of Health funding agreement which are recognized as a reduction in research and development expenses, and an increase of $0.5 million in product development expenses.

General and Administrative Expenses

General and administrative expenses increased by $1.7 million, or 9%, to $19.1 million during the year ended December 31, 2025, compared to $17.4 million during the year ended December 31, 2024, primarily due to an increase of $1.7 million in personnel-related expenses and one-time severance costs.

Interest Expense and Income

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-03_item1_business.md)

Item 1. Business.

Overview

We are a medical device company focused on transforming the lives of people living with epilepsy by reducing or eliminating the occurrence of debilitating seizures. Our novel and differentiated RNS System is the first and only commercially available, brain-responsive neuromodulation system that delivers personalized, real-time treatment at the seizure source. By continuously monitoring and analyzing the brain's electrical activity, recognizing patient-specific abnormal electrical patterns, and responding in real time with imperceptible electrical pulses to prevent seizures, our RNS System is programmed by clinicians to deliver the precise amount of therapy when and where it is needed and provides exceptional clinical outcomes with approximately three minutes of stimulation on average per day. Our RNS System is also the only commercially available device that records continuous brain activity data and allows clinicians to monitor patients not only in person, but also remotely, providing them the data they need to make more informed treatment decisions, thus optimizing patient care. We believe the therapeutic advantages of our RNS System, combined with the insights obtained from our extensive brain data set, offer a significant leap forward in epilepsy treatment. As of December 31, 2025, over 8,000 patients have received our RNS System. We believe our compelling body of long-term clinical data, demonstrating continuous improvement in outcomes over time, will support the continued adoption of our RNS System among the approximately 575,000 adults in the United States with drug-resistant focal epilepsy. We continue seeking indication expansion to, over time, cover the entire approximately 1.2 million drug-resistant epilepsy patients in the United States and may additionally seek to expand our operations to reach the approximately 16.5 million drug-resistant epilepsy patients globally.

Epilepsy is a devastating chronic disorder characterized by a tendency of the brain to produce sudden abnormal bursts of electrical energy that disrupt brain functions and cause seizures. The goal for treating epilepsy is to reduce the number and intensity of seizures that a patient experiences, without causing treatment-related side effects. While antiepileptic drugs are considered first-line treatment and are effective at controlling seizures in a large portion of the epilepsy population, approximately one-third of epilepsy patients are considered drug-resistant because they do not achieve complete seizure control or cannot tolerate the side effects of these drugs. According to the International League Against Epilepsy, or ILAE, drug-resistant epilepsy is defined as a patient failing to achieve sustained seizure freedom after trying two antiseizure medications. These drug-resistant epilepsy patients struggle with a variety of life-impacting challenges including psychological dysfunction, social stigmatization, reduced quality of life, and increased risk of mortality.

Epilepsy is further classified into two main categories– focal epilepsy and generalized epilepsy. Approximately 60% of epilepsy patients have focal epilepsy, which is characterized by electrical discharges that originate in a specific part of the brain. The remaining 40% of patients have generalized epilepsy, which is characterized by widespread electrical discharges that involve the entire brain at once. Our paradigm-shifting RNS System is currently indicated in the United States for use in adult epilepsy patients, meaning patients who are 18 years of age or older, with drug-resistant focal epilepsy, which we believe represents an approximately $27 billion total addressable market. While we are presently focused on this significant market opportunity, we have investigational device exemption, or IDE, approval for clinical trials to evaluate use of the RNS System to treat drug-resistant idiopathic generalized epilepsy, or IGE, and patients between ages 12 and 17 and we may later seek regulatory approval in markets outside the United States. We do not believe we will need to modify our RNS System for potential use in generalized epilepsy or in patients under the age of 18; however, we will need to complete clinical studies and obtain FDA approval prior to marketing the RNS System for these indications. We also believe that our RNS System may be effective in treating other brain disorders including depression, memory disorders, and post-traumatic stress disorder. We will need to conduct additional studies to determine if any modifications to the RNS System are necessary to address these other brain disorders and to obtain FDA approval for any new indications.

Our commercial efforts have historically been focused on growing adoption and utilization across Level 4 comprehensive epilepsy centers, or CECs, in the United States that facilitate appropriate care for drug-resistant epilepsy patients. In 2023, we received FDA approval of a Premarket Approval Supplement, or PMA-S, which updated the qualification criteria for centers and clinicians that may prescribe and implant the RNS System. This

supplemental approval allows us to expand our commercial efforts to target and be able to qualify the approximately 1,800 additional epileptologists outside of Level 4 CECs and the entire population of functional neurosurgeons, empowering them to provide the RNS System as a much-needed treatment option for their patients and expanding our current market opportunity to all 575,000 adults in the United States with drug-resistant focal epilepsy.

Our RNS System has an estimated average battery life of nearly 11 years, an increase from the previous model of the device. The sale of replacement neuromodulation devices provides a recurring revenue stream that is additive to the market opportunity for initial implants.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-11_2-02-results.md, 10-K_2026-03-03_item7_mdna.md, 10-K_2026-03-03_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
