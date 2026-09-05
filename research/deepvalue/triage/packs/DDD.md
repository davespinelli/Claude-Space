# Triage pack — DDD · 3D SYSTEMS CORP

_Generated 2026-09-05 03:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** DDD · **Name:** 3D SYSTEMS CORP
- **CIK:** 0000910638
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/DDD

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** 3D SYSTEMS CORP
- **CIK:** 910,638 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 3.32 |
| mktcap | $551.6M |
| ev | $510.9M |
| ev_ebit | n/a |
| fcf | -$97.8M |
| fcf_yield | -17.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -32.6% |
| net_debt | -$40.7M |
| net_debt_ebit | n/a |
| cash | $128.0M |
| ltd | $87.2M |
| equity | $273.6M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $386.9M |
| revenue_prior | $440.1M |
| rev_growth | -12.1% |
| rev_growth_note | share count +29.5% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | net income more than 3x operating income |
| ebit | -$96.1M |
| net_income | $29.9M |
| cfo | -$87.8M |
| capex | $9.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 29.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 166,147,027 |
| shares_py | 128,252,556 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 74.1% |
| r6m | 62.7% |
| off_52w_high | -14.4% |
| adv20 | $7.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.05 |
| r_ev_ebit | 0.00 |
| r_roic | 0.03 |
| r_rev_growth | 0.08 |
| r_buyback | 0.05 |
| score | 0.09 |

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
| rank | 484 |

**Screen rationale:** share count +29.5% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 74.1%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **166,147,027** (CY2026Q2I) vs **128,252,556** prior year (CY2025Q2I)
- Change: **29.5%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +29.5% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-04** — Item 5.02 (officer / director change or comp arrangement): On August 4, 2026, 3D Systems Corporation (the "Company") announced that Dr. Jeffrey A. Graves, the Company's President and Chief Executive Officer and a member of the Company's Board of Directors (the "Board"), will leave the Company and retire from the...
- **2026-06-05** — Item 1.01 (Entry into a Material Definitive Agreement): On June 3, 2026, 3D Systems Corporation (the "Company") entered into an underwriting agreement (the "Underwriting Agreement") with Needham & Company, LLC, as the representative of the several underwriters named in Schedule I thereto (the "Underwriters")...
- **2026-05-15** — Item 5.02 (officer / director change or comp arrangement): On May 14, 2026, as described below under Item 5.07 of this Current Report on Form 8-K, the stockholders of 3D Systems Corporation (the "Company") approved an amendment and restatement (the "Amendment and Restatement") of the Company's 2015 Incentive Plan (as...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 115,500 sh / $376,530 -> net $-376,530 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 8 |
| F | 3 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, '3D Systems Reports Second Quarter 2026 Financial Results'; skipped 6 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (a3dq22026earningsrelease.htm)

3D Systems Reports Second Quarter 2026 Financial Results

ROCK HILL, South Carolina - August 3, 2026 - 3D Systems Corporation (NYSE:DDD) announced today its financial results for the second quarter ended June 30, 2026.

• Q2 2026 revenue of $94.6 million, down 0.3% year-over-year, but up 1.4% excluding divestitures, driven by continued acceleration of new printer sales, with double-digit growth in both metal and polymer hardware printer systems.

• Net loss was $(12.9) million for the quarter, while A djusted EBITDA improved to a loss of $(0.8) million, reflecting benefits from previous cost reduction initiatives. For the first half of 2026, the Company reported a n et loss of $(17.3) million and positive Adjusted EBITDA of $1.3 million.

• Healthcare continued as the Company's largest segment in the quarter, with revenue increasing 6.8% year-over-year, supported by over 20% growth in Med Tech and 3% growth in Dental.

• Industrial revenue declined 6.7% year-over year, or 3.7% excluding divestitures, while increasing 2.4% sequentially, driven by higher product sales and over 20% growth in Aerospace & Defense, our largest Industrial market, and Data Center Infrastructure.

• We remain focused on our four priority markets which all delivered more than 20% growth in the first half of 2026: Med Tech, Dental, Aerospace & Defense, and Data Center Infrastructure.

Summary of Financial Results

(Unaudited)

Three Months Ended | Six Months Ended
(in millions, except per share data) | June 30, 2026 | June 30, 2025 | June 30, 2026 | June 30, 2025
Revenue | 94.6 | 94.8 | 190.1 | 189.4
Gross profit | 34.5 | 36.2 | 68.8 | 68.8
Gross profit margin | 36.4 | % | 38.1 | % | 36.2 | % | 36.4 | %
Operating expense | 45.1 | 51.5 | 86.1 | 121.0
Operating loss | (10.6) | (15.4) | (17.3) | (52.1)
Net (loss) income attributable to 3D Systems Corporation | (12.9) | 104.4 | (17.3) | 67.5
Diluted (loss) income per share | (0.09) | 0.57 | (0.12) | 0.37
Non-GAAP measures, excluding divestitures for year-over-year comparisons
Non-GAAP revenue | 94.6 | 93.3 | 190.1 | 179.3
Non-GAAP gross profit margin | 36.7 | % | 38.2 | % | 36.4 | % | 34.3 | %
Non-GAAP operating expense | 39.5 | 44.6 | 76.1 | 101.2
Adjusted EBITDA | (0.8) | (4.7) | 1.3 | (30.8)
Non-GAAP diluted loss per share | (0.04) | (0.06) | (0.05) | (0.23)

Summary Comments on Results

Dr. Jeffrey Graves, President and Chief Executive Officer of 3D Systems, said, "We are pleased with our second-quarter and first-half performance on both the top and bottom line. Revenue growth was driven by strength in our four key markets: Med Tech and Dental in Healthcare, and Aeros pace & Defense and Data Center Infrastructure in Industrial. Data Center Infrastructure is an emerging focus area for us and includes applications in chip manufacturing equipment and high-performance computing. Customers in these markets continue to adopt 3D printing as a core manufacturing technology and are expanding the range of applications they deploy. This performance highlights the market-leading breadth of our additive manufacturing portfolio, spanning direct metal printing and all five major polymer technologies, combined with our deep expertise in advanced applications. Of particular note is the growing impact of metal 3D printing, where design flexibility combined with cost-effective production is enabling higher-performance components and systems."

Dr. Graves concluded, "As the additive manufacturing industry continues to emerge from a multi-year downturn, our sustained investments in research and development are now enabling us to introduce a broad portfolio of new products that are gaining increasing customer traction. While the global economic environment remains uncertain, we are optimistic that, as capital investment activity strengthens, we are well positioned to benefit from the resulting expansion in global manufacturing capacity."

"Adjusting for divestitures completed in 2025, total revenue increased 1.4% year over year and 6% for the first half of 2026, demonstrating continued core revenue growth in the year" said Phyllis Nordstrom, Chief Financial Officer of 3D Systems. "Strong growth in our key markets along with accelerated growth in new printer launches contributed to our success in the quarter. We continue to focus on refreshing our installed base as well as expanding our parts manufacturing capabilities to drive greater margin expansion and profitability as we look ahead."

Second Quarter 2026 Results

Total revenue decreased 0.3% to $94.6 million compared to the prior year period. Adjusting for software divestitures completed in 2025, including Geomagic, 3DXpert and Oqton, total revenue increased by 1.4%.

Healthcare Solutions revenue increased approximately 6.8% to $48.1 million compared to the prior year period. Revenue growth was primarily driven by higher sales of new printer systems in Med Tech and continued growth in Personalized Healthcare Services.

Industrial Solutions revenue decreased approximately 6.7% to $46.5 million compared to the prior year period. Adjusting for divestitures, Industrial Solutions revenue decreased 3.7% year over year. The decline was primarily driven by the absence of revenue from a non-core product offering exited in the prior year and lower hardware services revenue.

Gross profit margin decreased to 36.4% compared to 38.1% in the prior year period. Non-GAAP gross profit margin decreased to 36.7% comp ared to 39.2% in the prior year period. Adjusting for software divestitures, non-GAAP gross profit margin decreased by 150 basis points. Gross profit was impacted by product mix, reflecting higher printer sales and select pricing impacts, partially offset by approximately $2.6 million of tariff refunds recovered in the quarter.

Net income attributable to 3D Systems Corporation decreased by $117.3 million to a loss of $(12.9) million compared to the prior year period. The decrease was primarily related to the gain on the sale of Geomagic and the gain on debt extinguishment recorded in the prior-year period, partially offset by improved operating margins and a lower income tax provision in the current period.

Adjusted EBITDA improved by $4.6 million, to $(0.8) million compared to the prior yea r period, driven primarily by the impact of prior cost reduction initiatives and the impact of tariff refunds recovered in the quarter. Adjusting for software divestitures, Adjusted EBITDA improved $3.9 million.

Financial Liquidity

During the second quarter 2026, the Company issued 18.9 million shares of common stock, par value $0.001 per share, for $53.2 million in cash, net of offering costs. At June 30, 2026, the Company had total cash of $129.0

million, which included cash and cash equivalents of $128.0 million and restricted cash of $1.0 million. A total of $3.9 million in principal amount of debt is scheduled to mature in the fourth quarter of 2026, with the remaining $92.0 million principal maturing in 2030.

Third Quarter 2026 Outlook

Revenue: $96 - $99 million

Adjusted EBITDA: ($3) million - ($1) million

3D Systems does not provide forward-looking guidance for certain measures on a GAAP basis. The Company is unable to provide a quantitative reconciliation of forward-looking Adjusted EBITDA to the most directly comparable forward-looking GAAP measures without unreasonable effort because certain items, including litigation expenses, acquisition expenses, stock-based compensation expense, intangible amortization expense, restructuring expenses, and goodwill impairment, are difficult to predict and estimate. These items are inherently uncertain and depend on various factors, many of which are beyond the Company's control, and as such, any associated estimate and its impact on GAAP performance could vary materially.

Second Quarter 2026 Conference Call and Webcast

The Company will host a conference call and simultaneous webcast to discuss these results on August 4, 2026, which may be accessed as follows:

Date: Tuesday, August 4, 2026

Time: 8:30 a.m. Eastern Time

Listen via webcast: www.3dsystems.com/investor

Participate via telephone: 877-407-8291 or 201-689-8345

A replay of the webcast will be available approximately two hours after the live presentation at www.3dsystems.com/investor .

(in thousands, except par value) | June 30, 2026 | December 31, 2025
ASSETS
Current assets:
Cash and cash equivalents | 127,951 | 95,635
Accounts receivable, net of reserves — $5,719 and $3,608 | 80,174 | 83,806
Inventories | 121,847 | 127,496
Prepaid expenses and other current assets | 35,639 | 39,770
Total current assets | 365,611 | 346,707
Property and equipment, net | 49,697 | 49,249
Intangible assets, net | 15,646 | 16,614
Goodwill | 15,404 | 15,575
Operating lease right-of-use assets | 41,170 | 45,364
Finance lease right-of-use assets | 7,160 | 7,774
Long-term deferred income tax assets | 2,443 | 2,787
Other assets | 38,113 | 37,658
Total assets | 535,244 | 521,728
LIABILITIES, REDEEMABLE NON-CONTROLLING INTEREST AND EQUITY
Current liabilities:
Current portion of long-term debt, net of deferred financing costs | 3,944 | 3,944
Current operating lease liabilities | 9,266 | 11,583
Accounts payable | 32,425 | 41,017
Accrued and other liabilities | 39,781 | 46,656
Customer deposits and deferred revenue | 22,182 | 17,423
Total current liabilities | 107,598 | 120,623
Long-term debt, net of deferred financing costs | 87,240 | 86,394
Long-term operating lease liabilities | 41,238 | 45,420
Long-term deferred income tax liabilities | 2,818 | 2,740
Other liabilities | 22,787 | 24,000
Total liabilities | 261,681 | 279,177
Commitments and contingencies
Redeemable non-controlling interest | — | 2,193
Stockholders' equity:
Preferred stock, 5,000 shares authorized; $0.001 par value; no shares issued and outstanding as of June 30, 2026 and December 31, 2025 | — | —
Common stock, $0.001 par value, authorized 220,000 shares; shares issued 166,149 and 145,581 as of June 30, 2026 and December 31, 2025, respectively | 166 | 146
Additional paid-in capital | 1,677,775 | 1,620,399
Accumulated deficit | (1,349,645) | (1,332,360)
Accumulated other comprehensive loss | (54,733) | (47,827)
Total stockholders' equity | 273,563 | 240,358
Total liabilities, redeemable non-controlling interest and stockholders' equity | 535,244 | 521,728

3D SYSTEMS CORPORATION

Condensed Consolidated Statements of Operations

(Unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-09_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Business Overview

3D Systems Corporation ("3D Systems" or the "Company" or "we," "our" or "us") markets our products and services through subsidiaries in North America and South America ("Americas"), Europe and the Middle East ("EMEA") and Asia Pacific and Oceania ("APAC"). We provide comprehensive 3D printing and digital manufacturing solutions, including 3D printers for plastics and metals, materials, software, and services, including maintenance, advanced manufacturing and applications engineering.

Our solutions support advanced applications in two key industry verticals which are our reportable segments: Healthcare Solutions (which includes dental, medical devices, personalized health services and regenerative medicine) and Industrial Solutions (which includes aerospace, defense, transportation and general manufacturing). We have more than 35 years of experience and expertise, which have proven vital to our development of an ecosystem and end-to-end digital workflow solutions that enable customers to optimize product designs, transform workflows, bring innovative products to market and drive new business models.

Recent Developments

2025 Restructuring Plan

In March 2025, the Company authorized the next phase of its multi-faceted cost savings and restructuring initiative (the "2025 Restructuring Plan"). The 2025 Restructuring Plan includes initiatives to deliver sustainable growth and profitability, enabled by a streamlining of both infrastructure and business processes, while consistently investing in core research and development ("R&D") activities to support long-term growth opportunities. Additionally, in May 2025, in response to the uncertain macroeconomic environment, the Company announced an incremental cost reduction initiative focused on labor force reductions to deliver incremental cost savings.

We incurred $8.5 million in severance and termination benefit costs related to headcount reductions during the year ended December 31, 2025. These costs were primarily cash charges and were generally recognized when probable and estimable consistent with the Company's past practices or statutory law. The Company does not expect to incur significant additional restructuring charges in 2026 related to the 2025 Restructuring Plan.

Divestitures

In December 2024, the Company entered into a definitive agreement with Hexagon AB for the sale of its Geomagic software business ("Geomagic"), which was included in our Industrial Solutions segment. On April 1, 2025, the Company completed the sale of Geomagic and received $119.4 million in cash, which reflected applicable purchase price adjustments. The Company recorded a pre-tax gain of $125.7 million from the sale of Geomagic in the year ended December 31, 2025.

In September 2025, the Company entered into a definitive agreement for the sale of its 3DXpert and Oqton businesses to Hubb Global Holdings, LLC. On October 31, 2025, the Company completed the sale of the 3DXpert and Oqton businesses for $3.3 million in cash, which reflected applicable purchase price adjustments, plus a revenue-based royalty receivable which had a present value of $7.1 million.

Neither of these divestitures is presented as discontinued operations in the consolidated financial statements because they do not represent a strategic shift that will have a major impact on the Company's operations.

Background

We earn revenue from the sale of products and services through our Healthcare Solutions and Industrial Solutions segments. The product categories include 3D printers and corresponding materials, digitizers, software licenses, 3D scanners and haptic devices. The majority of materials used in our 3D printers are proprietary. The services categories include maintenance contracts and services on 3D printers, software maintenance, software as a service subscriptions and healthcare solutions services.

Given the relatively high price of certain 3D printers and a corresponding lengthy selling cycle, as well as relatively low unit volume of the higher-priced printers in any particular period, a shift in the timing and concentration of orders and shipments from one period to another can materially affect reported revenue in any given period.

In addition to changes in sales volumes, there are two other primary drivers of changes in revenue from one period to another: (1) the combined effect of changes in product mix and average selling prices and (2) the impact of fluctuations in foreign currencies. As used in this MD&A, the price and mix effects relate to changes in revenue that are not able to be specifically attributed to changes in unit volume or changes in foreign exchange rates.

RESULTS OF OPERATIONS

Comparison of Results of Operations

Year Ended December 31,
(in thousands) | 2025 | 2024 | Change
Revenue | 386,902 | 440,121 | (53,219)
Cost of sales | 255,857 | 275,943 | (20,086)
Selling, general and administrative expenses ("SG&A") | 161,331 | 210,132 | (48,801)
Research and development expenses ("R&D") | 65,037 | 86,479 | (21,442)
Asset impairment charges | 760 | 144,967 | (144,207)
Loss from operations | (96,083) | (277,400) | 181,317

Revenue

The following table sets forth changes in our revenue for the year ended December 31, 2025.

(Dollars in thousands) | Products | Services | Total
Revenue — year ended December 31, 2024 | 279,178 | 160,943 | 440,121
Change in revenue:
Volume | (56,138) | (20.1) | % | 439 | 0.3 | % | (55,699) | (12.7) | %
Price/mix | (3,025) | (1.1) | % | — | — | % | (3,025) | (0.7) | %
Foreign currency translation | 3,390 | 1.2 | % | 2,115 | 1.3 | % | 5,505 | 1.3 | %
Net change | (55,773) | (20.0) | % | 2,554 | 1.6 | % | (53,219) | (12.1) | %
Revenue — year ended December 31, 2025 | 223,405 | 163,497 | 386,902

For the year ended December 31, 2025, revenue decreased $53.2 million, or 12.1%, compared to the year ended December 31, 2024. The decrease in revenue was primarily due to a decline in product revenue of $55.8 million driven by lower materials volume to customers in the dental, service bureaus, and jewelry markets, and the impact of divestitures. Service revenue increased $2.6 million due to increased volume and the impact of foreign currency translation which was partially offset by the impact of the divestitures. Service revenue for the year ended December 31, 2024 was also impacted by an $8.7 million reversal of revenue due to a cumulative catch-up adjustment under a collaboration arrangement as the Company determined that incremental revenue attributable to milestone payments that are contingent upon the achievement of contractual development criteria are no longer probable of being earned.

Cost of sales and gross profit

Year Ended December 31,
2025 | 2024 | Change in Gross Profit | Change in Gross Profit Margin
(Dollars in thousands) | Gross Profit | Gross Profit Margin | Gross Profit | Gross Profit Margin | % | Percentage Points | %
Products | 72,260 | 32.3 | % | 103,319 | 37.0 | % | (31,059) | (30.1) | % | (4.7) | (12.7) | %
Services | 58,785 | 36.0 | % | 60,859 | 37.8 | % | (2,074) | (3.4) | % | (1.8) | (4.8)
Total | 131,045 | 33.9 | % | 164,178 | 37.3 | % | (33,133) | (20.2) | % | (3.4) | (9.1) | %

For the year ended December 31, 2025, cost of sales decreased to $255.9 million compared to $275.9 million for the year ended December 31, 2024. This decline was primarily attributable to a lower volume of printer and material sales. Gross profit for the year ended December 31, 2025 decreased $33.1 million, or 20.2%, compared to the year ended December 31, 2024. The decrease in gross profit was primarily due to a combination of lower materials sales volumes and the impact of the divestitures. Gross profit margin decreased to 33.9% for the year ended December 31, 2025 compared to 37.3% for the year ended December 31, 2024, primarily due to the divestitures and lower sales volumes.

Selling, general and administrative expenses

For the year ended December 31, 2025, SG&A decreased $48.8 million, or 23.2%, compared to the year ended December 31, 2024. The year-over-year decline in SG&A was primarily due to:

• $21.3 million decrease in compensation and benefits expense primarily related to lower compensation expense due to the impact of our restructuring actions and lower stock-based compensation expense;

• $19.0 million decrease in third-party service provider and consulting costs due to the increased cost to complete our fiscal 2023 audit during the year ended December 31, 2024, and decreased legal fees; and

• $10.2 million decrease in intangible asset amortization expense due to lower intangible asset balances in 2025 because of the impairment charges assessed during the quarter ended September 30, 2024, as described further below;

• partially offset by a $4.7 million increase due to severance costs associated with our restructuring actions.

Research and development expenses

For the year ended December 31, 2025, R&D decreased $21.4 million, or 24.8%, compared to year ended December 31, 2024. The year-over-year decline in R&D was primarily due to:

• $15.8 million decrease in compensation and benefits expense and other R&D expenses primarily due to improved operating efficiency and cost reductions realized from our restructuring activities.

Asset impairment charges

During the year ended December 31, 2025, the Company recognized a $0.6 million impairment of a right of use asset related to a lease of a facility that was exited as part of its 2025 Restructuring Plan and could not be subleased. The impairment is included within Asset impairment charges in our consolidated statements of operations.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-09_item1_business.md)

Item 1. Business

General

3D Systems Corporation ("3D Systems" or the "Company" or "we," "our" or "us") markets our products and services through subsidiaries in North America and South America ("Americas"), Europe and the Middle East ("EMEA") and Asia Pacific and Oceania ("APAC"). We provide comprehensive 3D printing and digital manufacturing solutions, including 3D printers for plastics and metals, materials, software, and services, including maintenance, advanced manufacturing and applications engineering. Our solutions support advanced applications in two key industry verticals: Healthcare Solutions (which includes dental, medical devices, personalized health services and regenerative medicine) and Industrial Solutions (which includes aerospace, defense, transportation and general manufacturing). We have more than 35 years of experience and expertise, which have proven vital to our development of an ecosystem and end-to-end digital workflow solutions that enable customers to optimize product designs, transform workflows, bring innovative products to market and drive new business models.

Business Strategy

Accelerating Additive Manufacturing Adoption

We partner with customers to enable them to adopt and scale additive manufacturing in their production environments. We believe that our additive manufacturing capabilities can help customers solve a number of design and manufacturing challenges – such as improved lead times, enhanced design freedom, part consolidation and the ability for mass customization. We believe that we have both the scale and the breadth of technologies, encompassing hardware platforms, materials and software, that our customers require for the successful implementation of additive manufacturing into their design and manufacturing processes.

Using a strong application focus in our Industrial and Healthcare verticals, our Applications Innovation Group integrates our printer hardware, materials, software, and professional and technical services in unique combinations to solve customers' product needs. Once complete, we can scale the process for the customer to a certain production level through our Advanced Manufacturing solutions, and, with increasing demand, we can enable a customer to continue scaling to high volumes within their own production facilities. This transfer of the workflow involves providing the printing systems, materials and software, along with the process definition and other technical expertise, that enables a seamless transfer of capability to the manufacturer. We expect the result of this approach to drive recurring revenue streams as customers adopt additive manufacturing solutions and consume materials to produce parts, utilize software to manage the print process and manufacturing operations, and make use of our service offerings for application development, maintenance and upgrades. Our proficiency in providing industry focused application and solution development for customers includes a number of internal assets and capabilities, including:

a. A full range of additive manufacturing hardware technologies and materials to address needs in metals and plastics (including biocompatible materials for medical use), wax and bioprinting.

b. Software that enables optimal use of the printing system to improve output and automation; intelligence that manages fleets of machines to enhance efficiency and productivity; and advanced capabilities for workflow optimization, complex geometries, application performance, and machine optimization.

c. An Application Innovation Group that includes industry and technology application experts, customer innovation and advanced manufacturing centers and post-sale service and support.

d. Scale that includes significant and diverse experience in production parts and applications combined with a global reach to service our customers worldwide.

Healthcare Solutions

Leveraging decades of experience, we provide industry-leading surgical planning, implants, instrumentation, and medical education solutions to help medical device manufacturers and healthcare providers accelerate innovation, and ultimately, transform healthcare. Core areas of our Healthcare business include Medical Technology, Dental and Regenerative Medicine.

We are accelerating innovation across the Medical Technology industry and transforming personalized care by enabling patient-specific implants, surgical guides and anatomical models that improve precision in both planned procedures and trauma cases. These advancements will lead the way to enhancing surgical outcomes, reducing recovery times, and redefining how complex bone structures are designed, replaced, and restored.

In the Dental vertical, we are building on our reputation as a longtime leader in the clear aligner technology used to straighten teeth to address the full continuum of oral care. This includes protecting (nightguards), repairing (crowns and bridges) and replacing (multi-material monolithic jetted dentures) teeth. By leveraging our experience in straightening to these other critical areas we expect to play an important role in shaping the future of orthodontic and dental innovation.

Within Healthcare, a portion of our business focuses on opportunities for additive manufacturing to be applied to Regenerative Medicine. To date, our efforts in the area of Regenerative Medicine have consisted primarily of pre-commercial bio-technology research and development ("R&D") in the areas described below.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-09_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-09_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-09_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-03-09_item7_mdna.md, 10-K_2026-03-09_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
