# Triage pack — VMD · VIEMED HEALTHCARE, INC.

_Generated 2026-09-04 13:14 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** VMD · **Name:** VIEMED HEALTHCARE, INC.
- **CIK:** 0001729149
- **SIC:** 8090 — Services-Misc Health & Allied Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/VMD

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** VIEMED HEALTHCARE, INC.
- **CIK:** 1,729,149 · **SIC:** 8090 (Services-Misc Health & Allied Services, NEC) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 9.01 |
| mktcap | $343.2M |
| ev | $338.9M |
| ev_ebit | 14.8x |
| fcf | $11.9M |
| fcf_yield | 3.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 13.0% |
| net_debt | -$4.3M |
| net_debt_ebit | -0.2x |
| cash | $10.7M |
| ltd | $6.4M |
| equity | $144.0M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $270.3M |
| revenue_prior | $224.3M |
| rev_growth | 20.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $22.9M |
| net_income | $15.4M |
| cfo | $51.9M |
| capex | $40.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -1.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 38,088,228 |
| shares_py | 38,785,759 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 44.4% |
| r6m | 7.3% |
| off_52w_high | -26.9% |
| adv20 | $3.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.40 |
| r_ev_ebit | 0.59 |
| r_roic | 0.77 |
| r_rev_growth | 0.84 |
| r_buyback | 0.78 |
| score | 0.73 |

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
| rank | 44 |

**Screen rationale:** high ROIC 13.0%; revenue +20.5%; buying back stock -1.8%; net cash; 12-1 momentum 44.4%


## 3. Share count trend

- Shares outstanding: **38,088,228** (CY2026Q2I) vs **38,785,759** prior year (CY2025Q2I)
- Change: **-1.8%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-04** — Item 5.02 (officer / director change or comp arrangement): Viemed Healthcare, Inc. (the "Company") held its Annual General and Special Meeting of Shareholders (the "Meeting") on June 4, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 166,802 sh / $1,585,143 -> net $-1,585,143 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 64 (open-market buys 0, sales 9).

| code | rows |
|---|---|
| A | 6 |
| D | 8 |
| F | 5 |
| M | 36 |
| S | 9 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'Lafayette, Louisiana (August 3, 2026) Viemed Healthcare, Inc. (the "Co'; skipped 12 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q22026earningsrelease.htm)

Lafayette, Louisiana (August 3, 2026) Viemed Healthcare, Inc. (the "Company" or "Viemed") (NASDAQ:VMD), a national provider of technology-enabled, home-based healthcare solutions and chronic disease management, announced today that it has reported its financial results for the three and six months ended June 30, 2026, and updated guidance for the full year ending December 31, 2026.

Operational highlights (all dollar amounts are USD):

• Net revenues for the quarter ended June 30, 2026 were $78.1 million, setting a Company record, representing an increase of $15.0 million, or 23.9%, compared with the prior-year quarter and an increase of approximately 3.6% sequentially.

• Net income attributable to Viemed for the quarter ended June 30, 2026 totaled $2.8 million, or $0.07 per diluted share.

• Adjusted EBITDA for the quarter ended June 30, 2026 totaled $13.7 million, a 4.0% decrease as compared to the quarter ended June 30, 2025. The prior year period included a $1.0 million non-recurring gain on disposal of property and equipment related to the ventilator return program, which benefited net income and concluded during 2025.

• Net cash provided by operating activities totaled $15.9 million for the quarter and $60.8 million for the trailing twelve months ended June 30, 2026. Free cash flow totaled $8.6 million for the quarter and $34.4 million for the trailing twelve months ended June 30, 2026.

• During the second quarter of 2026, the Company repurchased and cancelled 530,802 common shares under its share repurchase program at a cost of $5.1 million (excluding taxes), representing an average buyback price of $9.65 per share.

• The Company ended the second quarter of 2026 with a record 12,635 ventilator patients, an increase of 4.0% over June 30, 2025, and a 4.5% sequential increase from March 31, 2026.

• The Company increased its PAP therapy patient count to 37,825 as of June 30, 2026, an increase of 44.0% over June 30, 2025, and a 5.3% sequential increase from March 31, 2026. The Company's sleep resupply patient count was 37,035 as of June 30, 2026, up 46.7% year over year and 10.0% sequentially.

• As of June 30, 2026, the Company maintained a cash balance of $10.7 million and an overall working capital balance of $6.1 million. The Company repaid $2.2 million of its term loan during the quarter ended June 30, 2026. Long-term debt totaled $6.4 million and the Company has $46 million available under existing credit facilities.

Updated Full Year 2026 Guidance (all dollar amounts are USD):

Based on first-half performance and favorable operating trends across ventilation and the broader platform, the Company is raising the low end and narrowing the range of its full-year net revenue guidance. The Company is also revising its Adjusted EBITDA guidance and net capital expenditure outlook. The revised guidance reflects the growing contribution from less capital-intensive product and service revenue.

• Net revenue is now expected to be in the range of $314 million to $320 million, compared with the previous range of $312 million to $320 million.

• Adjusted EBITDA is now expected to range from $64 million to $68 million, compared with the previous range of $65 million to $69 million.

• Net capital expenditures are now expected to range from 8.5% to 10.0% of net revenue, compared with the previous range of 9.0% to 10.5%.

See "Use of Non-GAAP Financial Information and Financial Guidance" below for further information about non-GAAP financial measures and non-GAAP financial guidance.

Casey Hoyt, Viemed's CEO, noted, "Viemed delivered another record quarter, with revenue reaching $78.1 million and our ventilator patient census rising to the highest level in company history. Strong ventilator setup activity, improving patient compliance, record PAP volume, and continued expansion in resupply and maternal health demonstrate the momentum building across our entire platform."

"The strength of these results reflects the durable and increasingly diversified company we have built. Viemed has multiple growth engines, strong cash generation, a solid balance sheet, and the financial flexibility to continue investing in our people, technology, and patient care capabilities. We are making those investments deliberately to support the patient growth already entering the platform, and we enter the second half of 2026 confident in Viemed's ability to deliver consistent and increasingly predictable growth."

Conference Call Details

The Company will host a conference call to discuss second quarter results on Tuesday, August 4, 2026, at 11:00 a.m. ET.

Interested parties may participate in the call by dialing:

877-407-6176 (US Toll-Free)

+1 201-689-8451 (International)

Live Audio Webcast: https://event.choruscall.com/mediaframe/webcast.html?webcastid=peVp8cbE

Following the conclusion of the call, an audio recording and transcript of the call can be accessed on the Company's website.

ABOUT VIEMED HEALTHCARE, INC.

Viemed is a provider of home medical equipment and post-acute healthcare services in the United States, with a focus on respiratory, chronic care, and women's health products and services. Viemed's model emphasizes efficient, high-quality care delivered in the home through a combination of high-touch clinical support and technology-enabled services, including therapy, education, and counseling provided by our clinical practitioners. For more information, visit our website at www.viemed.com.

For further information, please contact:

Investor Relations

ir@viemed.com

Trae Fitzgerald

Chief Financial Officer

337-504-3802

CONDENSED CONSOLIDATED STATEMENTS OF INCOME

(Expressed in thousands of U.S. Dollars, except outstanding shares and per share amounts)

(Unaudited)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenue | 78,097 | 63,056 | 153,511 | 122,185
Cost of revenue | 33,049 | 26,325 | 65,636 | 52,175
Gross profit | 45,048 | 36,731 | 87,875 | 70,010
Operating expenses
Selling, general and administrative | 37,132 | 28,803 | 71,924 | 57,228
Research and development | 504 | 847 | 1,083 | 1,644
Stock-based compensation | 2,032 | 2,341 | 4,483 | 4,652
Depreciation and amortization | 388 | 353 | 776 | 701
Loss (gain) on disposal of property and equipment | 598 | (636) | 954 | (3,004)
Other income, net | (67) | (72) | (102) | (147)
Income from operations | 4,461 | 5,095 | 8,757 | 8,936
Non-operating income and expenses
Loss from investments | 162 | — | 162 | —
Interest expense, net | 248 | 132 | 553 | 311
Net income before taxes | 4,051 | 4,963 | 8,042 | 8,625
Provision for income taxes | 1,151 | 1,713 | 2,429 | 2,665
Net income | 2,900 | 3,250 | 5,613 | 5,960
Net income attributable to noncontrolling interest | 136 | 93 | 267 | 178
Net income attributable to Viemed Healthcare, Inc. | 2,764 | 3,157 | 5,346 | 5,782
Net income per share
Basic | 0.07 | 0.08 | 0.14 | 0.15
Diluted | 0.07 | 0.08 | 0.13 | 0.14
Weighted average number of common shares outstanding:
Basic | 38,245,491 | 39,515,247 | 38,336,534 | 39,471,244
Diluted | 41,125,716 | 41,083,760 | 40,851,506 | 41,393,523

VIEMED HEALTHCARE, INC.

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS

(Expressed in thousands of U.S. Dollars)

(Unaudited)

Six Months Ended June 30,
2026 | 2025
Cash flows from operating activities
Net income | 5,613 | 5,960
Adjustments for:
Depreciation and amortization | 15,141 | 13,504
Stock-based compensation expense | 4,483 | 4,652
Loss (gain) on disposal of property and equipment | 954 | (3,004)
Amortization of deferred financing costs | 132 | 64
Deferred income tax benefit | — | (1,961)
Loss from other investments | 162 | —
Changes in working capital:
Accounts receivable, net | (6,643) | (1,638)
Inventory | (221) | (4)
Prepaid expenses and other assets | (1,665) | (150)
Trade payables | 2,072 | 1,598
Deferred revenue | 483 | 499
Accrued liabilities | 1,405 | (1,979)
Income tax payable/receivable | 2,057 | (2,433)
Net cash provided by operating activities | 23,973 | 15,108
Cash flows from investing activities
Purchase of property and equipment | (15,172) | (23,612)
Investment in equity investments | (552) | —
Proceeds from sale of property and equipment | 2,401 | 13,355
Net cash used in investing activities | (13,323) | (10,257)
Cash flows from financing activities
Proceeds from exercise of options | 1,057 | 1,368
Principal payments on term notes | (5,422) | (220)
Shares redeemed to pay income tax | (2,038) | (1,631)
Payments for share repurchase programs | (6,761) | (1,664)
Repayments of finance lease liabilities | — | (35)
Distributions to non-controlling interest | (307) | (193)
Net cash used in financing activities | (13,471) | (2,375)
Net increase (decrease) in cash and cash equivalents | (2,821) | 2,476
Cash and cash equivalents at beginning of year | 13,501 | 17,540
Cash and cash equivalents at end of period | 10,680 | 20,016
Supplemental disclosures of cash flow information
Cash paid during the period for interest | 390 | 212
Cash paid during the period for income taxes, net of refunds | 373 | 7,059
Supplemental disclosures of non-cash transactions
Equipment and other fixed asset purchases payable at end of period | 4,802 | 3,955
Equipment sales receivable at end of period | — | 986
Repurchases of shares not yet settled | — | 169

Reconciliation from GAAP Net Income to Non-GAAP Adjusted EBITDA

This press release refers to "Adjusted EBITDA", which is a financial measure that is not prepared in accordance with generally accepted accounting principles in the United States ("GAAP"). Adjusted EBITDA should be considered in addition to, not as a substitute for, or superior to, financial measures calculated in accordance with GAAP. Management believes Adjusted EBITDA provides helpful information with respect to the Company's operating performance as viewed by management, including a view of the Company's business that is not dependent on the impact of the Company's capitalization structure and items that are not part of the Company's day-to-day operations. Management uses Adjusted EBITDA (i) to compare the Company's operating performance on a consistent basis, (ii) to calculate incentive compensation for the Company's employees, (iii) for planning purposes, including the preparation of the Company's internal annual operating budget, and (iv) to evaluate the performance and effectiveness of the Company's operational strategies. Accordingly, management believes that Adjusted EBITDA provides useful information in understanding and evaluating the Company's operating performance in the same manner as management. Adjusted EBITDA is not a measurement of the Company's financial performance under GAAP and should not be considered as an alternative to revenue or net income, as applicable, or any other performance measures derived in accordance with GAAP. Adjusted EBITDA has limitations as an analytical tool and you should not consider it in isolation or as a substitute for analysis of the Company's operating results as reported under GAAP. Adjusted EBITDA does not reflect the impact of certain cash charges resulting from matters the Company considers not to be indicative of ongoing operations; and other companies in the Company's industry may calculate Adjusted EBITDA differently than we do, limiting its usefulness as a comparative measure. In calculating Adjusted EBITDA, certain items (mostly non-cash) are excluded from net income attributable to Viemed Healthcare, Inc., including depreciation and amortization of capitalized assets, net interest expense, stock based compensation, transaction costs, impairment of assets, and taxes.

The following unaudited table is a reconciliation of net income attributable to Viemed Healthcare, Inc., the most directly comparable GAAP measure, to Adjusted EBITDA, on a historical basis for the periods indicated:

(Expressed in thousands of U.S. Dollars)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-04_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We provide an array of home medical equipment, services and supplies, specializing in post-acute respiratory care services in the United States. Viemed's primary objective is to drive growth by increasing the number of patients served and the level of care provided through its technology-enabled, home-based clinical care and chronic disease management model. Viemed's care programs are designed specifically to treat patients in the home for less total cost and with a superior quality of care. Viemed's services include respiratory disease management (through the rental of various HME devices), neuromuscular care, in-home sleep testing and sleep apnea treatment, oxygen therapy, the sale of associated supplies, women's health products and services, and healthcare staffing services.

We derive a significant portion of our revenue through the rental of non-invasive and invasive ventilators which represented 50.6% and 55.6% of our revenue for the years ended December 31, 2025 and 2024, respectively. We combine the benefits of home ventilation support with licensed RTs to drive improved patient outcomes and reduce costly hospital readmissions.

We expect to grow through expansion of existing service areas as well as in new territories through a cost efficient launch that reduces location expenses. We currently serve patients in all 50 states. Viemed expects to expand its workforce of licensed clinical practitioners, including RTs, to support the Company's growth and ensure the high service model is maintained in the home. As of December 31, 2025, we employed 401 licensed RTs, representing approximately 29% of our company-wide employee count. Beyond fulfilling its internal staffing needs, Viemed also provides healthcare staffing and recruitment services, offering tailored workforce solutions to external healthcare institutions and partners seeking qualified clinical professionals.

By focusing overhead costs on personnel that service the patient rather than physical location costs, we anticipate that we will efficiently scale our business in territories that are currently not being effectively serviced.

The continued trend of servicing patients in the home rather than in hospitals is aligned with our business objective and we anticipate that this trend will continue to offer growth opportunities for us. We expect to continue to be a solution to the rising health care costs in the United States by offering more cost-effective, home-based solutions while increasing the quality of life for patients fighting serious chronic diseases.

For the year ended December 31, 2025, we generated revenues of $270.3 million and had net income of $15.4 million, compared to revenues of $224.3 million and net income of $11.4 million for the year ended December 31, 2024. Net revenue increased $46.0 million (or 20.5% ) from the comparable period in 2024. Revenue derived from the rental and sale of home medical equipment represented a combined 90.8% and 91.0%, respectively, of Viemed's 2025 and 2024 revenue.

Page | 31

Our primary sources of capital to date have been from operating cash flows. Our existing commercial credit facilities provide access to additional liquidity through a revolving credit facility of up to $30.0 million and a delayed draw term loan facility of up to $30.0 million. An accordion feature allows the Company to increase the size of such facilities by up to an additional $30.0 million, subject to certain conditions, for a total borrowing capacity of up to $90.0 million.

Trends Affecting Our Business

Demographic and Market Trends

Home medical equipment markets are witnessing sustained expansion, with a notable focus on the complex respiratory and Obstructive Sleep Apnea ("OSA") device segments. Analysts in the industry anticipate a consistent and robust growth trajectory, projecting Compound Annual Growth Rates ("CAGR") of approximately 6% for respiratory devices and 8% for OSA devices. This upward trend underscores the increasing demand for innovative solutions in respiratory care and sleep apnea management, highlighting the industry's responsiveness to evolving healthcare needs. As technological advancements and awareness drive the adoption of these specialized devices, we believe the HME markets, particularly in respiratory and OSA, are positioned for continuous expansion, offering promising opportunities for both providers and consumers alike.

The aging population remains a pivotal driver for the industry, as the elderly, constituting a substantial portion of HME patients, are expected to represent a higher percentage of the overall population. Projections from industry analysts indicate a consistent annual growth in the number of Medicare beneficiaries, contributing to ongoing patient volume growth. A significant contributing factor to the industry's growth is the rising incidence of chronic diseases. Factors such as increasing obesity rates, consequences of past smoking prevalence, under-diagnosis of certain health conditions, and higher diagnosis rates for chronic diseases collectively shape the industry. There is a notable shift towards home-based treatment for these conditions.

The industry is undergoing a transition to value-based healthcare, with both government and commercial payors increasingly adopting models that emphasize the transition of patients from acute care settings to home care. We believe HME providers are well-positioned to benefit from this industry shift. Advancements in technology and medical equipment have led to an increased prevalence of in-home treatments. The broader range of treatments administered in patient homes is expected to continue growing. Projections from industry analysts indicate that U.S. home healthcare spending will increase, reaching $250 billion by 2031, with a CAGR of approximately 7%.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Comparison of the Years Ended December 31, 2025 and 2024:

The following table summarizes our results of operations for the years ended December 31, 2025 and 2024:

Year Ended December 31,
2025 | % of Total Revenue | 2024 | % of Total Revenue | $ Change | % Change
Revenue | 270,280 | 100.0 | % | 224,257 | 100.0 | % | 46,023 | 20.5 | %
Cost of revenue | 114,822 | 42.5 | % | 91,054 | 40.6 | % | 23,768 | 26.1 | %
Gross profit | 155,458 | 57.5 | % | 133,203 | 59.4 | % | 22,255 | 16.7 | %
Selling, general and administrative | 121,366 | 44.9 | % | 106,199 | 47.4 | % | 15,167 | 14.3 | %
Research and development | 3,017 | 1.1 | % | 3,068 | 1.3 | % | (51) | (1.7) | %
Stock-based compensation | 9,132 | 3.4 | % | 6,285 | 2.8 | % | 2,847 | 45.3 | %
Depreciation and amortization | 1,485 | 0.5 | % | 1,483 | 0.6 | % | 2 | 0.1 | %
Gain on disposal of property and equipment | (2,239) | (0.8) | % | (1,905) | (0.8) | % | (334) | 17.5 | %
Other expense (income), net | (252) | (0.1) | % | 173 | 0.1 | % | (425) | (245.7) | %
Income from operations | 22,949 | 8.5 | % | 17,900 | 8.0 | % | 5,049 | 28.2 | %
Non-operating income and expenses
Income (loss) from investments | — | — | % | (954) | (0.4) | % | 954 | (100.0) | %
Interest expense, net | (1,182) | (0.4) | % | (776) | (0.4) | % | (406) | 52.3 | %
Net income before taxes | 21,767 | 8.1 | % | 16,170 | 7.2 | % | 5,597 | 34.6 | %
Provision for income taxes | 6,391 | 2.4 | % | 4,761 | 2.1 | % | 1,630 | 34.2 | %
Net income | 15,376 | 5.7 | % | 11,409 | 5.1 | % | 3,967 | 34.8 | %
Net income attributable to noncontrolling interest | 442 | 0.2 | % | 144 | 0.1 | % | 298 | 206.9 | %
Net income attributable to Viemed Healthcare, Inc. | 14,934 | 5.5 | % | 11,265 | 5.0 | % | 3,669 | 32.6 | %

Revenue

The following table summarizes our revenue for the years ended December 31, 2025 and 2024:

Year Ended December 31,
2025 | % of Total Revenue | 2024 | % of Total Revenue | $ Change | % Change
Net revenue from rentals
Ventilator rentals, non-invasive and invasive | 136,749 | 50.6 | % | 124,577 | 55.6 | % | 12,172 | 9.8 | %
Other home medical equipment rentals | 58,386 | 21.6 | % | 48,651 | 21.7 | % | 9,735 | 20.0 | %
Net revenue from sales and services
Equipment and supply sales | 50,254 | 18.6 | % | 30,896 | 13.7 | % | 19,358 | 62.7 | %
Service revenues | 24,891 | 9.2 | % | 20,133 | 9.0 | % | 4,758 | 23.6 | %
Total net revenue | 270,280 | 100.0 | % | 224,257 | 100.0 | % | 46,023 | 20.5 | %

For the year ended December 31, 2025, revenue totaled $270.3 million, an increase of $46.0 million (or 20.5%) from the comparable period in 2024. The primary driver of this growth was our equipment and supply sales revenue, which increased by $19.4 million (or 62.7%), largely due to the success of our sleep resupply program and the addition of maternal health offerings in connection with the Lehan Drugs, Inc ("Lehan") acquisition (as discussed in Note 3 – Business Combinations of the Notes to Consolidated Financial Statements). Ventilator rental revenue increased by $12.2 million (or 9.8%), primarily as a result of higher patient volumes and sustained demand for ventilation services. Rental revenue from other HME increased by $9.7 million (or 20.0%), reflecting an expanding patient base and strong demand for PAP, oxygen, and airway clearance therapies. Services revenue increased by $4.8 million (or 23.6%) primarily due to the growth of healthcare staffing offerings.

Page | 35

Cost of Revenue and Gross Profit

Cost of revenue for the year ended December 31, 2025 was $114.8 million, an increase of $23.8 million (or 26.1%) compared to the same period in 2024. This increase was primarily driven by higher patient volumes and the expansion of our service offerings, including higher personnel and product costs associated with servicing a larger patient base and supporting increased sales activity.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-04_item1_business.md)

Item 1. Business

Company Overview

Viemed Healthcare, Inc. (the "Company" or "Viemed"), through its subsidiaries, is a provider of home medical equipment ("HME") and post-acute healthcare services in the United States, with a focus on respiratory, chronic care, and women's health products and services. The Company's primary service offerings are focused on effective in-home treatment with clinical practitioners providing therapy and counseling to patients in their homes using cutting edge technology.

Viemed's primary objective is to drive growth by increasing the number of patients served and the level of care provided through its technology-enabled, home-based clinical care and chronic disease management model. Viemed's care programs are designed specifically to treat patients in the home for less total cost and with a superior quality of care. Viemed's services include respiratory disease management (through the rental of various HME devices), neuromuscular care, in-home sleep testing and sleep apnea treatment, oxygen therapy, the sale of associated supplies, women's health products and services, and healthcare staffing services.

Viemed seeks to grow through expansion of existing service areas as well as in new territories through a cost efficient launch that reduces location expenses. The Company currently serves patients in all 50 states of the United States. Viemed anticipates expanding its workforce of licensed clinical practitioners, including respiratory therapists ("RTs") to support the Company's growth and ensure the high service model is maintained in the home. As of December 31, 2025, the Company employed 401 licensed RTs, representing approximately 29% of the Company-wide employee count. Beyond fulfilling its internal staffing needs, Viemed also provides healthcare staffing and recruitment services, offering tailored workforce solutions to external healthcare institutions and partners seeking qualified clinical professionals.

By focusing overhead costs on personnel that service the patient rather than physical location costs, Viemed anticipates continuing to efficiently scale its business in territories that are currently not being effectively serviced. The continued trend of servicing patients in the home rather than in hospitals is aligned with Viemed's business objectives and management anticipates that this trend will continue to offer growth opportunities for the Company. Viemed expects to continue to be a solution to the rising health costs in the United States by offering more cost-effective, home-based solutions while increasing the quality of life for patients managing chronic and complex health conditions.

Corporate Information

Viemed Healthcare, Inc. is a holding company incorporated in British Columbia under the Business Corporations Act in December 2016. The common shares of Viemed trade on the Nasdaq Stock Market LLC ("NASDAQ") under the trading symbol "VMD". Viemed's registered and records office is located at Suite 2800, Park Place, 666 Burrard Street, Vancouver, British Columbia V6C 2Z7 Canada and its principal executive office is located at 625 E. Kaliste Saloom Road, Lafayette, Louisiana 70508.

Copies of our Annual Report on Form 10-K, Quarterly Reports on Form 10-Q, Current Reports on Form 8-K, and amendments to those reports filed or furnished pursuant to Section 13(a) or 15(d) of the Securities Exchange Act of 1934, as amended (the "Exchange Act"), are available free of charge through our website (www.viemed.com) as soon as reasonably practicable after we electronically file the material with, or furnish it to, the Securities and Exchange Commission. These reports and other information are also available, free of charge, at www.sec.gov. Information contained on any website referred to in this Annual Report on Form 10-K is not part of this Annual Report on Form 10-K.

Page | 5

Products and Services

Viemed's services include the following:

• Home Medical Equipment : Viemed provides respiratory and other home medical equipment solutions (primarily through monthly rental arrangements), including home ventilation (invasive and non-invasive), BiPAP (bi-level positive airway pressure) and CPAP (continuous positive airway pressure) devices, percussion vests, oxygen concentrators, and other medical equipment. Viemed provides home medical equipment through the following service programs:

◦ Respiratory disease management , including treatment of Chronic Obstructive Pulmonary Disease ("COPD"), is designed to improve quality of life and reduce hospital readmissions by using proven methodology and leading technologies, such as non-invasive ventilation ("NIV"), percussion vests, and other therapies. Viemed provides ventilation (both invasive and non-invasive) and related equipment and supplies to patients suffering from COPD through a high-touch model.

◦ Neuromuscular care is focused on helping neuromuscular patients breathe more comfortably while living an active, healthier life and uses respiratory therapy treatments which can lessen the effort required to breathe.

◦ Oxygen therapy provides patients with extra oxygen, which is sometimes used to manage certain chronic health problems, including COPD. Oxygen therapy may be performed in the home or in another setting.

◦ Sleep apnea management provides sleep solutions and/or equipment such as Positive Airway Pressure ("PAP"), the AutoPAP (automatic continuous positive airway pressure), and BiPAP machines. Viemed provides in home sleep apnea testing services, which is an alternative to the traditional sleep lab testing environment.

◦ Women's health provides breast pumps and related lactation equipment and supplies, including fulfillment and support services, to eligible patients as part of its home medical equipment offerings.

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
