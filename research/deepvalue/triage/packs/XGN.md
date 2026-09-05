# Triage pack — XGN · EXAGEN INC.

_Generated 2026-09-05 02:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** XGN · **Name:** EXAGEN INC.
- **CIK:** 0001274737
- **SIC:** 8071 — Services-Medical Laboratories
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/XGN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** EXAGEN INC.
- **CIK:** 1,274,737 · **SIC:** 8071 (Services-Medical Laboratories) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 7.54 |
| mktcap | $182.7M |
| ev | $180.4M |
| ev_ebit | n/a |
| fcf | -$14.3M |
| fcf_yield | -7.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -111.7% |
| net_debt | -$2.3M |
| net_debt_ebit | n/a |
| cash | $24.6M |
| ltd | $22.3M |
| equity | $12.2M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $66.6M |
| revenue_prior | $55.6M |
| rev_growth | 19.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$14.1M |
| net_income | -$20.0M |
| cfo | -$13.6M |
| capex | $641k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 10.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 24,225,339 |
| shares_py | 22,003,641 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -31.3% |
| r6m | 134.2% |
| off_52w_high | -37.0% |
| adv20 | $2.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.10 |
| r_ev_ebit | 0.00 |
| r_roic | 0.01 |
| r_rev_growth | 0.83 |
| r_buyback | 0.12 |
| score | 0.21 |

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
| rank | 461 |

**Screen rationale:** revenue +19.7%


## 3. Share count trend

- Shares outstanding: **24,225,339** (CY2026Q2I) vs **22,003,641** prior year (CY2025Q2I)
- Change: **10.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-04-23** — Item 5.02 (officer / director change or comp arrangement): On April 17, 2026, Ana Hooker notified the Board of Directors (the "Board") of Exagen Inc. (the "Company") of her decision to resign as member of the Board, including all committees thereof, effective April 17, 2026 ("Effective Time").

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 81,113 sh / $628,187 -> net $-628,187 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 0, sales 5).

| code | rows |
|---|---|
| A | 12 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'Exagen Inc. Reports Second Quarter 2026 Financial Results'; skipped 9 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q22026exagenearningspressr.htm)

Exagen Inc. Reports Second Quarter 2026 Financial Results

Achieved record total revenue, test volume and trailing twelve-month ASP

Reduced net loss by nearly 30% and narrowed adjusted EBITDA loss to $0.1 million

Increased full-year revenue guidance to $72 - $75 million

August 4, 2026

Carlsbad, Calif., – Exagen Inc. (Nasdaq: XGN), a leading provider of autoimmune testing solutions, today reported financial results for the quarter ended June 30, 2026, and recent corporate updates.

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Unaudited. In thousands, except ASP data.
Revenue | 19,941 | 17,202 | 37,247 | 32,700
Gross margin | 61.3 | % | 60.4 | % | 60.2 | % | 59.7 | %
Operating expenses | 13,939 | 13,025 | 27,558 | 25,513
Operating loss | (1,722) | (2,630) | (5,136) | (5,995)
Net loss | (3,196) | (4,439) | (7,163) | (8,191)
Adjusted EBITDA | (114) | (1,721) | (2,274) | (4,229)
Trailing-twelve-month average selling price (ASP) | 446 | 428 | 446 | 428
Cash and cash equivalents | 24,588 | 30,033 | 24,588 | 30,033

Second Quarter 2026 and Recent Corporate Highlights:

• Achieved record total revenue of $19.9 million, an increase of 16% compared to second quarter 2025.

• Grew AVISE CTD test volume 11% compared to second quarter 2025.

• Expanded AVISE CTD trailing twelve-month ASP to $446 per test, an increase of $18 per test, or 4% compared to second quarter 2025.

• Drove a significant improvement in adjusted EBITDA, reporting a loss of $0.1 million compared to a loss of $1.7 million in second quarter 2025.

• Ended the quarter with approximately $25 million in cash and cash equivalents.

• Published a systematic review validating strong real-world AVISE Lupus performance in an analysis of over 3,100 patients across 14 medical centers, which demonstrated that use of AVISE CTD correctly identified approximately 25% of SLE patients missed by conventional markers.

"We continue to advance Exagen's unique mission to bring clarity to autoimmune disease," said John Aballi, President and Chief Executive Officer. "Second quarter financial results demonstrate the progress we're making in improving the growth and operating profile of our business, putting us within reach of sustainable profitability and cash generation. At the same time, we are building on Exagen's leadership in autoimmune diagnostics through continued investment in clinical evidence generation, pipeline innovation and AI-powered tools that support rheumatology workflows to strengthen our role in rheumatology decision-making."

2026 Guidance

The Company increased full-year 2026 revenue guidance to $72 million - $75 million compared to previous guidance of $70 million - $73 million.

Conference Call and Webcast

• Date: August 4, 2026

• Time: 8:30 a.m. ET/ 5:30 a.m. PT

• U.S. dial-in: 877-407-0890

• International dial-in: +1 201-389-0918

• Webcast: Available via the Exagen Investor Relations website at investors.exagen.com

Replay: A telephone replay will be available until Tuesday, August 18, 2026:

• U.S. replay: 877-660-6853

• International replay: +1 201-612-7415

• Replay passcode: 13760979

• Webcast: A recording of the webcast will be available one hour after the call concludes via the Exagen Investor Relations website at investors.exagen.com

Use of Non-GAAP Financial Measures (Unaudited)

In addition to the financial results prepared in accordance with generally accepted accounting principles in the United States (GAAP), this press release contains the metric adjusted EBITDA, which is not calculated in accordance with GAAP and is a non-GAAP financial measure. Adjusted EBITDA is defined as net loss adjusted for interest income (expense), income tax expense (benefit), depreciation and amortization expense, stock‑based compensation expense, change in fair value of warrant liability, and certain other non‑cash, unusual or non‑recurring items, including, for example, losses on extinguishment of debt and changes in the fair value of warrant liabilities; we do not exclude normal, recurring, cash operating expenses from this measure. Such items could have a significant impact on the calculation of GAAP net loss.

Exagen uses adjusted EBITDA internally because the company believes these metrics provide useful supplemental information in assessing its operating performance reported in accordance with GAAP. Exagen believes adjusted EBITDA may enhance an evaluation of the operating

performance because it excludes the impact of prior decisions made about capital investment, financing, investing and certain expenses the company believes are not indicative of the ongoing performance. However, this non-GAAP financial measure may be different from non-GAAP financial measures used by other companies, even when the same or similarly titled terms are used to identify such measures, limiting their usefulness for comparative purposes.

This non-GAAP financial measure is not meant to be considered in isolation or used as a substitute for net loss reported in accordance with GAAP, should be considered in conjunction with the financial information presented in accordance with GAAP, has no standardized meaning prescribed by GAAP, is unaudited, and is not prepared under any comprehensive set of accounting rules or principles. In addition, from time to time in the future, there may be other items that Exagen may exclude for purposes of these non-GAAP financial measures, and the company may in the future cease to exclude items that it has historically excluded for purposes of these non-GAAP financial measures. Likewise, Exagen may determine to modify the nature of adjustments to arrive at these non-GAAP financial measures. Because of the non-standardized definitions of non-GAAP financial measures, the non-GAAP financial measure as used by the company in this press release and the accompanying reconciliation table have limits in their usefulness to investors and may be calculated differently from, and therefore may not be directly comparable to, similarly titled measures used by other companies. Accordingly, investors should not place undue reliance on non-GAAP financial measures.

A reconciliation of net loss to non-GAAP adjusted EBITDA is provided in the financial schedules that are part of this press release.

About Exagen

Exagen Inc. (Nasdaq: XGN) is a leading provider of autoimmune diagnostics, committed to transforming care for patients with chronic and debilitating autoimmune conditions. Based in San Diego County, California, Exagen's mission is to provide clarity in autoimmune disease decision-making and improve clinical outcomes through its innovative testing portfolio. The company's flagship product, AVISE® CTD, enables clinicians to more effectively diagnose complex autoimmune conditions such as lupus, rheumatoid arthritis, and Sjögren's disease earlier and with greater accuracy. Exagen's CLIA-certified, CAP-accredited laboratory specializes in the testing of rheumatic diseases, delivering precise and timely results, supported by a suite of AVISE-branded tests for disease diagnosis, prognosis, and monitoring. With a focus on research, innovation, education, and patient-centered care, Exagen is dedicated to addressing the ongoing challenges of autoimmune disease management.

For more information, visit Exagen.com or follow Exagen on LinkedIn.

(in thousands, except share and per share amounts)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue | 19,941 | 17,202 | 37,247 | 32,700
Cost of revenue | 7,724 | 6,807 | 14,825 | 13,182
Gross margin | 12,217 | 10,395 | 22,422 | 19,518
Operating expenses:
Selling, general and administrative expenses | 12,513 | 11,542 | 24,579 | 22,746
Research and development expenses | 1,426 | 1,483 | 2,979 | 2,767
Total operating expenses | 13,939 | 13,025 | 27,558 | 25,513
Loss from operations | (1,722) | (2,630) | (5,136) | (5,995)
Interest expense | (1,201) | (1,124) | (2,468) | (1,669)
Loss on extinguishment of debt | — | (295) | — | (295)
Change in fair value of warrant liability | (426) | (438) | 456 | (438)
Other income (expense), net | 153 | 85 | 21 | 243
Loss before income taxes | (3,196) | (4,402) | (7,127) | (8,154)
Income tax expense | — | (37) | (36) | (37)
Net loss | (3,196) | (4,439) | (7,163) | (8,191)
Net loss per share, basic and diluted | (0.13) | (0.21) | (0.30) | (0.41)
Weighted-average number of shares used to compute net loss per share, basic and diluted | 24,164,569 | 21,085,749 | 24,012,761 | 19,830,265

Exagen Inc.

Unaudited Condensed Balance Sheets

(in thousands, except share and per share amounts)

June 30, 2026 | December 31, 2025
Assets
Current assets:
Cash and cash equivalents | 24,588 | 32,220
Accounts receivable, net | 12,407 | 10,855
Prepaid expenses and other current assets | 5,862 | 5,818
Total current assets | 42,857 | 48,893
Property and equipment, net | 6,565 | 6,938
Operating lease right-of-use assets | 1,953 | 1,435
Other assets | 560 | 756
Total assets | 51,935 | 58,022
Liabilities and Stockholders' Equity
Current liabilities:
Accounts payable | 4,439 | 4,153
Accrued and other current liabilities | 4,939 | 6,327
Deferred revenue | 1,492 | 675
Finance lease liabilities, current | 1,091 | 1,135
Operating lease liabilities, current | 979 | 1,226
Borrowings, current | 517 | 643
Total current liabilities | 13,457 | 14,159
Borrowings, non-current, net of discounts and debt issuance costs | 22,322 | 22,264
Finance lease liabilities, non-current | 1,617 | 1,960
Operating lease liabilities, non-current | 1,130 | 438
Warrant liability | 1,193 | 1,752
Total liabilities | 39,719 | 40,573
Commitments and contingencies (Note 5)
Stockholders' equity:
Preferred stock, $0.001 par value; 10,000,000 shares authorized, no shares issued or outstanding as of June 30, 2026 and December 31, 2025 | — | —
Common stock, $0.001 par value; 200,000,000 shares authorized as of June 30, 2026 and December 31, 2025; 24,193,101 and 22,911,575 shares issued and outstanding as of June 30, 2026 and December 31, 2025, respectively | 24 | 23
Additional paid-in capital | 333,637 | 331,708
Accumulated deficit | (321,445) | (314,282)
Total stockholders' equity | 12,216 | 17,449
Total liabilities and stockholders' equity | 51,935 | 58,022

Exagen Inc.

Reconciliation of Non-GAAP Financial Measures (UNAUDITED)

The table below presents the reconciliation of adjusted EBITDA, which is a non-GAAP financial measure. See "Use of Non-GAAP Financial Measures (UNAUDITED)" above for further information regarding Exagen's use of non-GAAP financial measures.

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
(in thousands)
Adjusted EBITDA
Net loss | (3,196) | (4,439) | (7,163) | (8,191)
Other (income) expense | (153) | (85) | (21) | (243)
Interest expense | 1,201 | 1,124 | 2,468 | 1,669
Loss on extinguishment of debt | — | 295 | — | 295
Change in fair value of warrant liability | 426 | 438 | (456) | 438
Income tax expense (benefit) | — | 37 | 36 | 37
Depreciation and amortization expense | 628 | 466 | 1,227 | 906
Stock-based compensation expense | 980 | 443 | 1,635 | 860
Adjusted EBITDA (Non-GAAP) | (114) | (1,721) | (2,274) | (4,229)

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-10_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a medical technology company primarily focused on the design, development and commercialization of a next-generation portfolio of innovative testing products under our AVISE ® brand, which allow for the differential diagnosis, prognosis and monitoring of complex rheumatic, autoimmune and autoimmune-related disease including, among others, SLE and RA. We believe our strong focus and extensive background in the field of rheumatology, combined with our commitment to exceptional customer service and support, position us well to respond to the needs of rheumatologists, primary care physicians, other specialists, and the patients they serve.

Our tests are used in a variety of clinical settings to provide clarity in autoimmune disease decision-making with the goal of improving patients' clinical outcomes. We commercially launched our flagship testing product, AVISE ® CTD, in 2012. AVISE ® CTD enables differential diagnosis for patients presenting with symptoms indicative of a wide variety of CDTs and other related diseases with overlapping symptoms. Traditional screening methods often lack accuracy, resulting in repeat testing and delayed diagnosis. With significant increases in autoimmune incidence in recent years, AVISE ® CTD provides unique biomarkers that empower clinicians to confidently and quickly diagnose various CTDs.

Beginning in late 2022, w e revitalized our organization with the addition of key members to our senior leadership team, each with successful industry track records in diagnostics, medical device and medical technology, including our Chief Executive Officer, Chief Financial Officer, Chief Scientific Officer, Vice President of Sales, Vice President of Commercial Strategy, and Medical and Laboratory Director. By leveraging our team's extensive experience to create clinically distinct solutions that improve patient lives, we have created a strong foundation for growth and believe that we are well-positioned to positively impact patient care and address unmet clinical needs in autoimmune disease . We strive to become a partner of choice for doctors, hospitals, healthcare systems, and payors.

Under the leadership of our Chief Executive Officer, John Aballi, who joined Exagen in October 2022, we have executed an operational turnaround of the business, resulting in a return to revenue growth and gross margin expansion while significantly reducing operating expenses and cash burn.

All of our AVISE ® tests are performed in our approximately 13,000 square foot laboratory located in Vista, California, which is certified under the CLIA and accredited by CAP. Our laboratory is certified for performance of high-complexity testing by CMS in accordance with CLIA and is licensed by all states requiring out-of-state licensure. Our clinical laboratory typically reports all AVISE ® testing product results within five business days.

Reimbursement for our testing services comes from several sources, including commercial payors (such as insurance companies and health maintenance organizations), government payors (such as Medicare and Medicaid), client payors (such as hospitals, other laboratories, etc.) and patients. Reimbursement rates vary by product and payor.

Since launching AVISE ® CTD, we have produced an extensive body of peer-reviewed literature supporting the test's clinical validity and utility, demonstrating the importance of AVISE ® CTD in patient care. Revenue from this product comprised 91% of our revenue for each of the years ended December 31, 2025 and 2024.

In addition to providing diagnostic testing, we are leveraging our clinical laboratory to enter into agreements in the normal course of business with leading pharmaceutical companies and contract research organizations for the use of our testing products and/or the de-identified data generated from such tests. We believe the quality of our testing, proprietary offerings and specialized knowledge give us an advantage in this space. We plan to continue to pursue additional partnerships with leading pharmaceutical companies and academic research centers that are synergistic with our evolving portfolio of testing products, as more of these organizations realize the extent of the service we can provide.

We market our AVISE ® testing products using our specialized sales force covering 45 territories in the United States. Many diagnostic sales forces are trained only to understand the comparative benefits of the tests they promote. In contrast, the specialized backgrounds of our sales personnel, coupled with our comprehensive training, enables our sales representatives to interpret results from our de-identified patient test reports and provide unique insights in a highly tailored discussion with rheumatologists. We believe our focus on and experience in the field of rheumatology, combined with our commitment to excellent customer service and support, position us very well to respond to the needs of rheumatologists and the patients they serve.

Factors Affecting Our Performance

We believe there are several important factors that have impacted, and that we expect will impact, our operating performance and results of operations, including:

▪ Commercial Launch of AVISE ® CTD Enhancements . Our flagship product, AVISE ® CTD, enables clinicians to more effectively diagnose complex autoimmune conditions such as SLE, RA, and Sjögren's syndrome earlier and with greater accuracy, in each case, as compared to the current standard of care. Our laboratory specializes in the testing of rheumatic diseases, delivering precise and timely results, supported by a full suite of AVISE ® -branded tests for disease diagnosis, prognosis, and monitoring. With a focus on research, innovation, education, and patient-centered care, we are dedicated to addressing the ongoing challenges of autoimmune disease management.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Comparison of the Years Ended December 31, 2025 and 2024:
Year Ended December 31, | Change
2025 | 2024
(in thousands)
Revenue | 66,575 | 55,641 | 10,934
Cost of revenue | 27,776 | 22,529 | 5,247
Gross profit | 38,799 | 33,112 | 5,687
Operating expenses:
Selling, general and administrative expenses | 46,615 | 41,373 | 5,242
Research and development expenses | 6,254 | 5,375 | 879
Total operating expenses | 52,869 | 46,748 | 6,121
Loss from operations | (14,070) | (13,636) | (434)
Interest expense | (4,318) | (2,234) | (2,084)
Loss on extinguishment of debt | (295) | — | (295)
Change in fair value of warrant liability | (1,506) | — | (1,506)
Interest income | 289 | 767 | (478)
Loss before income taxes | (19,900) | (15,103) | (4,797)
Income tax expense | (51) | (12) | (39)
Net loss | (19,951) | (15,115) | (4,836)

Revenue

Revenue increased $10.9 million, or 19.7%, for the year ended December 31, 2025 compared to the year ended December 31, 2024, due to an increase in test volume and continued ASP expansion. The number of AVISE ® CTD tests delivered in the year ended December 31, 2025 increased by approximately 11% compared to the same period in 2024. In addition, our AVISE ® CTD trailing twelve-month ASP increased by $30 per test to $441 per test in the fourth quarter of 2025 from $411 per test in the fourth quarter of 2024.

Cost of Revenue

Cost of revenue increased $5.2 million, or 23.3%, for the year ended December 31, 2025 compared to the year ended December 31, 2024. This increase was primarily due to increases of $3.7 million in materials and supplies expenses, $1.4 million in payroll and stock-based compensation expense, and $0.3 million in facilities and allocated overhead expenses. These increases were partially offset by a decrease of $0.2 million in shipping and handling costs.

Gross Margin

Gross margin as a percentage of revenue decreased slightly to 58.3% for the year ended December 31, 2025 compared to 59.5% for the year ended December 31, 2024, primarily due to the changes to revenue and cost of revenue described above.

Selling, General and Administrative Expenses

Selling, general and administrative expenses increased $5.2 million, or 12.7%, for the year ended December 31, 2025 compared to the year ended December 31, 2024. This increase was primarily due to increases of $2.2 million in salaries, $1.6 million in commissions, $0.7 million in travel and entertainment, $0.5 million in outside services, $0.2 million in stock-based compensation expense, and $0.1 million in other expenses, partially offset by a decrease of $0.1 million in bonuses.

Research and Development Expenses

Research and development expenses increased $0.9 million, or 16.4%, for the year ended December 31, 2025 compared to the year ended December 31, 2024. This increase was primarily due to an increase of $0.6 million of

personnel costs (including salaries, benefits and stock-based compensation) resulting from increased allocation of labor to research and development for laboratory personnel working on the validation of the T-Cell Biomarkers and RA Sub-Profile Biomarkers, and an increase of $0.3 million in clinical and facility-related expenses.

Interest Expense

Interest expense increased by $2.1 million, including an increase of $0.8 million in non-cash interest expense, for the year ended December 31, 2025 compared to the year ended December 31, 2024, primarily due to the Perceptive Term Loan Facility that we entered into in April 2025 and the embedded finance lease related to the supply agreement, as amended, with one of our suppliers for certain reagents. We expect to continue to incur this interest expense under the Perceptive Term Loan Facility.

Loss on Extinguishment of Debt

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-10_item1_business.md)

Item 1. Business.

Overview

We are a medical technology company primarily focused on the design, development and commercialization of a next-generation portfolio of innovative testing products under our AVISE ® brand, which allow for the differential diagnosis, prognosis and monitoring of complex rheumatic, autoimmune and autoimmune-related disease including, among others, systemic lupus erythematosus (SLE) and rheumatoid arthritis (RA). We believe our strong focus and extensive background in the field of rheumatology, combined with our commitment to exceptional customer service and support, position us well to respond to the needs of rheumatologists, primary care physicians, other specialists, and the patients they serve.

Our tests are used in a variety of clinical settings to provide clarity in autoimmune disease decision-making with the goal of improving patients' clinical outcomes. We commercially launched our flagship testing product, AVISE ® CTD, in 2012. AVISE ® CTD enables differential diagnosis for patients presenting with symptoms indicative of a wide variety of connective tissue diseases (CTDs) and other related diseases with overlapping symptoms. Traditional screening methods often lack accuracy, resulting in repeat testing and delayed diagnosis. With significant increases in autoimmune incidence in recent years, AVISE ® CTD provides unique biomarkers that empower clinicians to confidently and quickly diagnose various CTDs.

Since launching AVISE® CTD, we have produced an extensive body of peer-reviewed literature supporting the test's clinical validity and utility, demonstrating the importance of AVISE® CTD in patient care. In 2025, we added eight new biomarkers to our AVISE CTD panel enhancing the clinical utility of our tests in the diagnoses of SLE and RA. Revenue from this product comprised 91% of our revenue for each of the years ended December 31, 2025 and 2024.

Beginning in late 2022, w e revitalized our organization with the addition of key members to our senior leadership team each with successful industry track records in diagnostics, medical device and medical technology, including our Chief Executive Officer, Chief Financial Officer, Chief Scientific Officer, Vice President of Sales, Vice President of Commercial Strategy and Medical and Laboratory Director. By leveraging our team's extensive experience to create clinically distinct solutions that improve patient lives, we have created a strong foundation for growth and believe that we are well-positioned to positively impact patient care and address unmet clinical needs in autoimmune disease . We strive to become a partner of choice for doctors, hospitals, healthcare systems, and payors.

Under the leadership of our Chief Executive Officer, John Aballi, who joined Exagen in October 2022, we have been executing an operational turnaround of the business, which has resulted in a return to revenue growth and gross margin expansion while significantly reducing operating expenses and cash burn. Comparing our financial results in fiscal 2025 to fiscal 2022, we have grown annual revenue by over 45%, expanded our AVISE® CTD trailing twelve-month average selling price by over 50%, improved gross margin by over 1,100 basis points, reduced operating expenses by over 20% and reduced net loss by nearly 60%. At the same time, we have nearly doubled our salesforce productivity and brought an intense focus to our Research and Development (R&D) investments - resulting in more than 35% reduction in related expenses and prioritization of near-term pipeline opportunities.

Revenue was a record $66.6 million for the year ended December 31, 2025, an increase of approximately 19.7% compared to the year ended December 31, 2024. This increase was driven by an approximate 11% increase in testing volume and an approximate 7% increase in average selling price (ASP) each as compared to the year ended December 31, 2024. These trends are consistent with the growth strategy we initiated in 2022. We believe these results highlight the power of combining volume with reimbursement growth and the resulting top line impact when both are moving in the same direction. Our execution across commercial, scientific, and operations underpinned this outcome — notably Q3 and Q4 volumes were our highest ever for those periods, without the typical second half seasonality we have experienced in the past.

Our AVISE CTD trailing twelve-month ASP for 2025 was $441, up roughly 7%, or $30 per test, over 2024. The consistent ASP expansion reflects disciplined payer engagement, appeals and revenue cycle optimization, and the accretive impact of new biomarkers; however, our new biomarker reimbursement ramped more gradually than expected, and we experienced some payer headwinds in the second half of the year.

We believe we are well positioned to deliver continued revenue growth and positive Adjusted EBITDA in the next 12-18 months.

Research and Development

We continue our thoughtful approach to research and development. We believe there is significant potential to enhance existing or develop new testing products with superior clinical utility, on our own or through collaboration with partners.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-10_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-10_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-10_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-03-10_item7_mdna.md, 10-K_2026-03-10_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
