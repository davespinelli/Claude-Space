# Triage pack — CERT · Certara, Inc.

_Generated 2026-09-04 19:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CERT · **Name:** Certara, Inc.
- **CIK:** 0001827090
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CERT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Certara, Inc.
- **CIK:** 1,827,090 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 8.13 |
| mktcap | $1.2B |
| ev | $1.3B |
| ev_ebit | 64.0x |
| fcf | $94.6M |
| fcf_yield | 7.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 1.5% |
| net_debt | $104.7M |
| net_debt_ebit | 5.0x |
| cash | $184.1M |
| ltd | $288.9M |
| equity | $966.5M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $418.8M |
| revenue_prior | $385.1M |
| rev_growth | 8.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $21.0M |
| net_income | -$1.6M |
| cfo | $96.3M |
| capex | $1.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -5.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 152,538,780 |
| shares_py | 160,623,580 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -23.7% |
| r6m | 13.7% |
| off_52w_high | -40.2% |
| adv20 | $19.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.62 |
| r_ev_ebit | 0.11 |
| r_roic | 0.36 |
| r_rev_growth | 0.62 |
| r_buyback | 0.88 |
| score | 0.52 |

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
| rank | 226 |

**Screen rationale:** buying back stock -5.0%


## 3. Share count trend

- Shares outstanding: **152,538,780** (CY2026Q2I) vs **160,623,580** prior year (CY2025Q2I)
- Change: **-5.0%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-04** — Item 5.02 (Departure of Directors or Certain Officers; Election): of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.
- **2026-06-17** — Item 5.02 (Departure of Directors or Certain Officers; Election): of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 37 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 11 |
| D | 1 |
| F | 3 |
| M | 22 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'Certara Reports Second Quarter 2026 Financial Results'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99 - EX-99 (q22026earningsreleaseex99.htm)

Certara Reports Second Quarter 2026 Financial Results

A ppoints Julien Perrier Chief Commercial Officer

Completes previously authorized $100 million share repurchase program; Board authorizes additional $50 million under repurchase program

Reaffirms 2026 revenue guidance

RADNOR, PA — August 4, 2026 -- Certara, Inc. (Nasdaq: CERT), a global leader in model-informed drug development, today reported its second quarter 2026 financial results.

Second Quarter Highlights from Continuing Operations:

Financial results of the Regulatory and Medical Writing business are reported as discontinued operations. The discussion in this earnings release presents the results of continuing operations and excludes amounts related to discontinued operations for all periods presented, unless otherwise noted.

• Revenue was $93.3 million, compared to $92.4 million in the second quarter of 2025, representing growth of 1%.

• Software revenue was $48.8 million , compared to $46.7 million in the second quarter of 2025, representing growth of 4%.

• Services revenue was $44.5 million, compared to $45.7 million in the second quarter of 2025, representing a decrease of 3%.

• Net loss was $6.1 million, compared to a net income of $1.5 million in the second quarter of 2025.

• The change primarily reflects the absence of a $5.7 million favorable contingent consideration adjustment recorded in the prior-year period, a $2.9 million unfavorable swing in currency expense, and a $2.2 million increase in reorganization costs, partially offset by lower income tax expense.

• Adjusted EBITDA was $26.2 million, compared to $27.0 million in the second quarter of 2025, representing a decrease of 3%.

"This second quarter was about continuing to execute on our commitments. Overall, we are pleased with our ongoing progress transforming Certara into a company we believe can deliver sustainable double-digit growth," said Jon Resnick, Chief Executive Officer. "We completed the divestiture of our Regulatory and Medical Writing business, implemented our two new business units, and taken necessary actions to strengthen our leadership team and our commercial model. Our focus in the second half of the year is customer impact and speed of execution."

"Our second quarter results were in line with our expectations, and we remain focused on executing against our full-year plan," said Faiz Mohammed, Interim Chief Financial Officer. "We continue to expect full-year revenue growth of 0% to 4% on a comparable continuing operations basis, supported by continued strength in software and improving services performance as we move through the second half of the year."

Second Quarter 2026 and Recent Corporate Updates

• In May, Certara closed the divestiture of its global medical writing and related regulatory services business ("the Regulatory and Medical Writing business") and announced the reorganization of its company around two business units, Model Informed Discovery and Drug Development (MID3) and Accelerated Clinical Evidence (ACE).

• In parallel with the reorganization, during the second quarter, Certara executed a reduction in force, focusing predominantly on overhead, impacting approximately 5% of its global employee base. This action, combined with other steps towards operational excellence, is expected to result in a run-rate savings of approximately $13 million. These reductions allow the Company to accelerate innovation and growth and streamline the Company's cost base, including stranded costs from the divestiture.

• Certara has appointed Julien Perrier Chief Commercial Officer, effective August 1, 2026. Mr. Perrier brings nearly two decades of international commercial leadership in the life sciences. Most recently, he served as Chief Executive Officer of Ziwig, where he led the commercial development of the AI-powered diagnostic EndoTest. Prior to Ziwig, Mr. Perrier served as a Vice President at IQVIA, Head of the Immunology division, France at AbbVie, and Head of Office Specialty Care Division at Sanofi. As part of Certara's move to align sales and marketing under a unified commercial leadership model in support of the business units, Mr. Perrier will focus on deepening customer engagement, sharpening go-to-market execution, and ensuring Certara's products and services deliver clear, demonstrable value to customers worldwide.

• Certara has appointed Eric Jahn as Chief Information Officer. Mr. Jahn previously served as Senior Vice President, IT. He joined Certara in 2022 and has helped scale the business globally by partnering with all functions as a strategic business partner. Prior to Certara, Mr. Jahn served as Vice President, IT Infrastructure at TIBCO Software and spent seven years at Rocket Software in various IT leadership roles.

Second Quarter 2026 Results from Continuing Operations

Financial results of the Regulatory and Medical Writing business are reported as discontinued operations. The discussion in this earnings release presents the results of continuing operations and excludes amounts related to discontinued operations for all periods presented, unless otherwise noted. Refer to Note 4 "Divestiture and Discontinued Operation" in our Form 10-Q for the quarter ended June 30, 2026 for further details.

Total revenue for the second quarter of 2026 was $93.3 million, representing year-over-year growth of 1% on a reported basis. Software revenue for the second quarter of 2026 was $48.8 million, representing year-over-year growth of 4% on a reported basis. Services revenue for the second quarter of 2026 was $44.5 million, representing a year-over-year decrease of 3% on a reported basis.

Total Bookings for the second quarter of 2026 were $98.3 million, representing a year-over-year increase of 1%.

Software Bookings for the second quarter of 2026 were $50.7 million, representing a year-over-year increase of 9%.

Services Bookings for the second quarter of 2026 were $47.6 million, representing a year-over-year decrease of 6%.

Total cost of revenues for the second quarter of 2026 was $35.1 million, an increase of $0.8 million from $34.3 million in the second quarter of 2025. The increase in cost of revenues was primarily due to a $1.0 million increase in employee-related costs and a $0.9 million increase in professional and consulting expenses, partially offset by a decrease in equity-based compensation expense and other miscellaneous expenses.

Total operating expenses for the second quarter of 2026 were $58.3 million, which increased by $7.9 million from $50.4 million in the second quarter of 2025. Higher operating expenses were primarily attributable to a $5.7 million increase related to the remeasurement of the fair value of business acquisition contingent consideration, primarily due to the absence of a non-recurring favorable change recognized in the prior year that reduced expenses in that period, a $1.1 million increase in professional and consulting expenses, a $1.0 million increase in employee-related costs, a $0.8 million increase in depreciation expense, and a $0.6 million increase in executive recruiting expenses, partially offset by a decrease in equity-based compensation expense.

Net loss for the second quarter of 2026 was $6.1 million, compared to net income of $1.5 million in the second quarter of 2025. The $7.6 million increase in loss was primarily driven by higher operating expenses, including a $5.7 million increase related to the remeasurement of the fair value of acquisition-related contingent consideration, $1.1 million aggregate increase in executive recruiting and lease abandonment charges, increased total other expenses, and a higher cost of revenue, partially offset by lower tax expense and higher revenue.

Diluted loss per share for the second quarter of 2026 was $(0.04), as compared to diluted earnings per share of $0.01 for the second quarter of 2025.

Adjusted EBITDA for the second quarter of 2026 was $26.2 million compared to $27.0 million for the second quarter of 2025, a decrease of $0.8 million. See note (1) in the section titled "A Note on Non-GAAP Financial Measures" below for more information on adjusted EBITDA.

Adjusted net income for the second quarter of 2026 was $12.5 million compared to $12.7 million for the second quarter of 2025, a decrease of $0.2 million. Adjusted diluted earnings per share for the second quarter of 2026 was $0.08, compared to $0.08 for the second quarter of 2025. See note (2) in the section titled "A Note on Non-GAAP Financial Measures" below for more information on adjusted net income and adjusted diluted earnings per share.

THREE MONTHS ENDED JUNE 30, | SIX MONTHS ENDED JUNE 30,
2026 | 2025 | 2026 | 2025
Key Financials | (in millions, except per share data)
Revenue | 93.3 | 92.4 | 187.4 | 184.5
Software revenue | 48.8 | 46.7 | 98.5 | 93.1
Service revenue | 44.5 | 45.7 | 88.8 | 91.4
Total bookings | 98.3 | 97.4 | 195.5 | 195.7
Software bookings | 50.7 | 46.6 | 99.4 | 87.3
Services bookings | 47.6 | 50.8 | 96.1 | 108.4
Net income (loss) | (6.1) | 1.5 | (17.9) | 3.0
Diluted earnings (loss) per share | (0.04) | 0.01 | (0.11) | 0.02
Adjusted EBITDA | 26.2 | 27.0 | 52.9 | 55.4
Adjusted net income | 12.5 | 12.7 | 21.6 | 29.5
Adjusted diluted earnings per share | 0.08 | 0.08 | 0.14 | 0.18
Cash and cash equivalents | 184.1 | 162.3

2026 Financial Outlook

Certara is reaffirming its revenue growth and updating its adjusted EBITDA margin, adjusted diluted earnings per share, and fully diluted share guidance for the full year 2026, to reflect the divestiture of the Regulatory and Medical Writing business and Continuing Operations reporting:

• Revenue growth for Continuing Operations, excluding the Regulatory and Medical Writing business, is expected to be 0% to 4%, or revenue of $367 million to $382 million.

• Full year 2026 adjusted EBITDA margin for Continuing Operations, excluding the Regulatory and Medical writing business, is expected to be approximately 29% to 31%.

• Full year adjusted diluted earnings per share for Continuing Operations, excluding the Regulatory and Medical Writing business is expected to be in the range of $0.31 to $0.36.

• Fully diluted shares are expected to be in the range of 155 million to 157 million.

Financial results of the Regulatory and Medical Writing business will be reported as discontinued operations for 2026. Through the transaction closing on May 8, 2026, the year-to-date discontinued operations Revenue was $19.2 million.

In the second quarter, the Company repurchased $17.4 million in shares, which completed a $100 million share repurchase program under terms previously authorized by the Board. In the third quarter, the Board approved an additional $50 million under the share repurchase program, reflecting the Company's continued confidence in the business and its disciplined approach to capital allocation. The program does not have an express expiration date, and all repurchase plans must be brought in advance to the Board.

Please note that the Company has not reconciled adjusted EBITDA, adjusted EBITDA margin or adjusted diluted earnings per share forward-looking guidance included in this press release to the most directly comparable GAAP measures because this cannot be done without unreasonable effort due to the variability and low visibility with respect to costs related to acquisitions, financings, and employee stock compensation programs, which are potential adjustments to future earnings. The Company expects the variability of these items to have a potentially unpredictable, and a potentially significant, impact on our future GAAP financial results.

Webcast and Conference Call Details

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Executive Overview

We are a global leader in biosimulation science, technology and consulting services for using Model-Informed Drug Development ("MIDD") in the global biopharmaceutical and biotech industry. MIDD is an approach that utilizes biological and statistical models derived from preclinical, clinical, and evidence data to inform decision-making in drug research and development, and commercialization. Biosimulation is a critical component of MIDD that uses computer-aided mathematical simulation of biological processes and systems to understand the action of a drug in a human body or a population of humans. Our goal is to enable the life science industry to use data, modeling, and analytics to make better decisions during drug research, development and commercialization to increase productivity rates and vastly reduce development costs.

Drug development is necessarily a highly regulated process involving the collection of vast amounts of laboratory, clinical and evidence data, and there are many failures at every step along the way that add to total cost. On average, the pharmaceutical industry spends more than $290 billion annually on research and development("R&D"). Generally, companies spend an average of $6.2 billion per FDA-approved drug to develop one new medicine, including the cost of failures, according to "Analysis of pharma R&D productivity - a new perspective needed" on Drug Discovery Today. Our technology and scientists incorporate modern advances in scientific understanding, drug research and development experience, data analysis, and AI, resulting in significant opportunities to decrease the cost and increase the odds of new drug approval and commercial success.

Our approach to AI is grounded in our long-standing expertise in mechanistic and empirical modeling. We deploy AI capabilities within validated scientific frameworks and expert-led workflows, rather than as standalone automated systems. This expert-in-the-loop model allows us to leverage native AI capabilities in a manner that is consistent with regulatory expectations for transparency, reproducibility, and explainability.

Our proprietary biosimulation platforms are built on biology, chemistry, and pharmacology principles with proprietary mathematical algorithms that model how medicines and diseases behave in the body. For over two decades, our scientists have developed and validated our biosimulation technology using data from scientific literature, laboratory research, preclinical and clinical studies. To do this, we have developed scientifically based solutions for the collection, standardization, validation, storage, and analysis of the preclinical, clinical and evidence data needed for MIDD. These data solutions are used internally and industry wide by life sciences companies.

The scientific principles underlying our work must be transparent and fully explainable during the regulatory process, so we have developed expertise in incorporating data, references and results into regulatory documents. Our software and regulatory scientific services streamline the creation of regulatory filings and speed regulatory data flow to maximize the chances of successful commercialization.

Native AI and machine learning technologies are being incorporated across our technology and consulting services portfolios, providing opportunities to expand the number of data sources utilized, better predict outcomes, and streamline reporting. For example, we are using machine learning to automate and speed the process of biosimulation, and we have created generative AI applications to aid in drafting regulatory documents from scientific analyses and clinical data.

We apply AI capabilities within established modeling environments and under the supervision of experienced scientists and regulatory experts. Our modeling platforms, curated datasets, and regulatory experience position us to incorporate emerging AI techniques in a controlled and scientifically rigorous manner. While AI can enhance productivity and insight generation, our solutions continue to rely on validated models and expert interpretation to support decision-making in regulated environments.

We leverage our validated software applications to deliver technology-enabled services. Our services are delivered by scientists with extensive drug development experience who aid our customers in applying biosimulation and MIDD to their specific projects.

Since 2014, customers who leverage our solutions have received 90% or more of all new drug approvals by FDA. We have worked with more than 2,600 life sciences companies and academic institutions and have collaborated on more than 10,000 customer projects in the last decade across a wide variety of therapeutic areas ranging from cancer and hematology to diabetes and hundreds of rare diseases. Our software products are licensed by more than 160,000 users and are also used by 20 global drug regulatory agencies, including the FDA, the UK's MHRA, Japan's PMDA, and China's NMPA.

With continued innovation in and adoption of our biosimulation software, technology, and services, we believe more life science companies worldwide will leverage more of our end-to-end platform to reduce cost, accelerate speed to market, and ensure safety and efficacy of medicines for all patients.

Key Factors Affecting Our Performance

We believe that the growth of and future success of our business depends on many factors. While each of these factors presents significant opportunities for our business, they also pose important challenges that we must successfully address to sustain our growth and improve results of operations.

Customer Retention and Expansion

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

YEAR ENDED DECEMBER 31,
2025 | 2024 | 2023
(dollars in thousands)
Statement of operations data:
Revenues | 418,838 | 385,148 | 354,337
Cost of revenues | 161,126 | 154,516 | 141,022
Operating expenses:
Sales and marketing | 53,720 | 47,444 | 32,022
Research and development | 41,040 | 37,105 | 34,173
General and administrative | 85,380 | 94,221 | 95,385
Depreciation and amortization expense | 56,556 | 53,593 | 45,525
Goodwill impairment expense | — | — | 46,984
Total operating expenses | 236,696 | 232,363 | 254,089
Income (loss) from operations | 21,016 | (1,731) | (40,774)
Other expenses:
Interest expense | (19,738) | (21,520) | (22,916)
Net other income | 6,338 | 6,067 | 8,547
Total other expenses | (13,400) | (15,453) | (14,369)
Income (loss) before income taxes | 7,616 | (17,184) | (55,143)
Provision (benefit) for income taxes | 9,211 | (5,133) | 214
Net income (loss) | (1,595) | (12,051) | (55,357)

Comparison of the Years Ended December 31, 2025 and 2024

Revenues

YEAR ENDED DECEMBER 31, | CHANGE
2025 | 2024 | %
(in thousands)
Software | 183,275 | 155,696 | 27,579 | 18 | %
Services | 235,563 | 229,452 | 6,111 | 3 | %
Total revenues | 418,838 | 385,148 | 33,690 | 9 | %

Revenues increased by $33.7 million, or 9%, to $418.8 million for the year ended December 31, 2025, as compared to the same period in 2024. The overall revenue growth was primarily due to an increase in our technology-enabled services and software product offerings, driven by strong demand from existing customers, expansion of relationships with existing customers and new customers, and growth from the Chemaxon acquisition.

Software revenue increased by $27.6 million, or 18%, to $183.3 million for the year ended December 31, 2025, as compared to the same period in 2024, primarily driven by strong demand within existing customers, and expansion of relationships with existing customers, and business acquisitions.

Services revenue increased by $6.1 million, or 3%, to $235.6 million for the year ended December 31, 2025, as compared to the same period in 2024, primarily attributed to continued growth in technology-enabled services with existing and new customers.

Cost of Revenues

YEAR ENDED DECEMBER 31, | CHANGE
2025 | 2024 | %
(in thousands)
Cost of revenues | 161,126 | 154,516 | 6,610 | 4 | %

Cost of revenues increased by $6.6 million, or 4%, to $161.1 million for the year ended December 31, 2025, as compared to the same period in 2024. The increase was primarily due to a $4.2 million increase in intangible assets amortization, a $2.6 million increase in license and service expense, a $1.9 million increase in consulting and professional services cost, a $0.5 million increase related to executive recruiting expenses, and a $0.5 million increase in equipment and software expense, partially offset by a $2.0 million decrease in employee-related costs, and a $1.1 million decrease in equity-based compensation cost.

Sales and Marketing Expense

YEAR ENDED DECEMBER 31, | CHANGE
2025 | 2024 | %
(in thousands)
Sales and marketing | 53,720 | 47,444 | 6,276 | 13 | %
% of total revenues | 13 | % | 12 | %

Sales and marketing expense increased by $6.3 million, or 13%, to $53.7 million for the year ended December 31, 2025, as compared to the same period in 2024. Sales and marketing expense increased primarily due to a $5.4 million increase in employee-related costs mainly resulting from headcount growth driven by acquisitions along with investment to build the commercial organization, a $0.9 million increase in equity-based compensation cost, and a $0.3 million increase in equipment and software expense, partially offset by a $0.3 million decrease in consulting and professional services expense.

Research and Development Expense

YEAR ENDED DECEMBER 31, | CHANGE
2025 | 2024 | %
(in thousands)
Research and development | 41,040 | 37,105 | 3,935 | 11 | %
% of total revenues | 10 | % | 10 | %

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business.

Our Company

We are a global leader in biosimulation science, technology, and consulting services for using Model-Informed Drug Development ("MIDD") in the global biopharmaceutical and biotech industry. MIDD is an approach that utilizes biological and statistical models derived from preclinical, clinical, and evidence data to inform decision-making in drug research and development, and commercialization. Biosimulation is a critical component of MIDD that uses computer-aided mathematical simulation of biological processes and systems to understand the action of a drug in a human body or a population of humans.

Biosimulation and hereby MIDD can increase the probability of success in bringing a new drug to market, accelerate its development and decrease the costs of drug development. There are many examples of currently approved drugs where models were successfully used in discovery, preclinical, first-in-human dose predictions, clinical trial simulations and protocol design, and for drug interaction label claims. Biosimulation is also used to support drug development beyond the approval stage; examples include determining formulation or manufacturing changes and label extensions. In addition, MIDD strategies are increasingly utilized to help predict commercial success, a critical part of the drug research and development process as new products must be both approved by regulators and adopted by the market.

The diagram below shows the different areas of expertise that come together to enable MIDD. Our organization has been purposefully designed to include all these capabilities to collectively enable a new model of drug research and development for our clients.

Our goal is to enable the life sciences industry to use data, modeling, and analytics to make better decisions during drug research, development and commercialization to increase productivity rates and vastly reduce development costs. The pharmaceutical industry spends more than $290 billion annually on research and development. On average, it takes 10-15 years and costs $6.2 billion to develop one new medicine, including the cost of failures. Drug development is necessarily a highly regulated process involving the collection of vast amounts of laboratory, clinical and evidence data, and there are many failures at every step along the way that add to total cost.

Our technology and scientists incorporate modern advances in scientific understanding, drug research and development experience, data analysis, and AI, resulting in significant opportunities to decrease the cost and increase the odds of new drug approval and commercial success.

Our approach to AI is grounded in our long-standing expertise in mechanistic and empirical modeling. We deploy AI capabilities within validated scientific frameworks and expert-led workflows, rather than as standalone automated systems. This expert-in-the-loop model allows us to leverage native AI capabilities in a manner that is consistent with regulatory expectations for transparency, reproducibility, and explainability.

Our proprietary biosimulation platforms are built on biology, chemistry, and pharmacology principles with proprietary mathematical algorithms that model how medicines and diseases behave in the body. For over two decades, our scientists have developed and validated our biosimulation technology using data from scientific literature, laboratory research, preclinical and clinical studies. To do this, we have developed scientifically based solutions for the collection, standardization, validation, storage, and analysis of the preclinical, clinical and evidence data needed for MIDD. These data solutions are used internally and industry wide by life sciences companies.

The scientific principles underlying our work must be transparent and fully explainable during the regulatory process, so we have developed expertise in incorporating data, references and results into regulatory documents. Our software and regulatory scientific services streamline the creation of regulatory filings and speed regulatory data flow to maximize the chances of successful commercialization.

Native AI and machine learning technologies are being incorporated across our technology and consulting services portfolios, providing opportunities to expand the number of data sources utilized, better predict outcomes, and streamline reporting. For example, we are using machine learning to automate and speed the process of biosimulation, and we have created generative AI applications to aid in drafting regulatory documents from scientific analyses and clinical data.

We apply AI capabilities within established modeling environments and under the supervision of experienced scientists and regulatory experts. Our modeling platforms, curated datasets, and regulatory experience position us to incorporate emerging AI techniques in a controlled and scientifically rigorous manner. While AI can enhance productivity and insight generation, our solutions continue to rely on validated models and expert interpretation to support decision-making in regulated environments.

We leverage our validated software applications to deliver technology-enabled services. Our services are delivered by scientists with extensive drug development experience who aid our customers in applying biosimulation and MIDD to their specific projects.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
