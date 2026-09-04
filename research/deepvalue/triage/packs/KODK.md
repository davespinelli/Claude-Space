# Triage pack — KODK · EASTMAN KODAK CO

_Generated 2026-09-04 22:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** KODK · **Name:** EASTMAN KODAK CO
- **CIK:** 0000031235
- **SIC:** 3861 — Photographic Equipment & Supplies
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/KODK

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** EASTMAN KODAK CO
- **CIK:** 31,235 · **SIC:** 3861 (Photographic Equipment & Supplies) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 9.15 |
| mktcap | $895.8M |
| ev | $713.8M |
| ev_ebit | n/a |
| fcf | $446.0M |
| fcf_yield | 49.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 0.0% |
| net_debt | -$182.0M |
| net_debt_ebit | n/a |
| cash | $290.0M |
| ltd | $108.0M |
| equity | $623.0M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.1B |
| revenue_prior | $1.0B |
| rev_growth | 2.5% |
| rev_growth_note | share count +20.9% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | $0.00 |
| net_income | -$128.0M |
| cfo | $480.0M |
| capex | $34.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 20.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 97,900,000 |
| shares_py | 81,000,000 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 71.2% |
| r6m | 32.6% |
| off_52w_high | -36.9% |
| adv20 | $8.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.98 |
| r_ev_ebit | 0.00 |
| r_roic | 0.31 |
| r_rev_growth | 0.43 |
| r_buyback | 0.07 |
| score | 0.41 |

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
| rank | 318 |

**Screen rationale:** top-quartile FCF yield 49.8%; share count +20.9% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 71.2%


## 3. Share count trend

- Shares outstanding: **97,900,000** (CY2026Q2I) vs **81,000,000** prior year (CY2025Q2I)
- Change: **20.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +20.9% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 2,000 sh / $20,600 vs sells 0 sh / $0 -> net $20,600 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: Katz Philippe D bought 2,000 sh @ $10.30 ($20,600) on 2026-05-13.

Form 4 filings parsed: 12; transaction rows: 50 (open-market buys 1, sales 0).

| code | rows |
|---|---|
| A | 16 |
| D | 11 |
| F | 6 |
| M | 16 |
| P | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'Kodak Reports Second-Quarter 2026 Financial Results'; skipped 10 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (kodk-ex99_1.htm)

Kodak Reports Second-Quarter 2026 Financial Results

Company Delivered Year-Over-Year Growth in Revenue, Gross Profit and Operational EBITDA for the Fourth Consecutive Quarter

Key Print and AM&C Businesses Achieved Increases in Revenue and Operational EBITDA

ROCHESTER, N.Y., August 4, 2026 – Eastman Kodak Company (NYSE: KODK) today reported financial results for the second quarter 2026.

Second quarter 2026 highlights include:

•
Consolidated revenues of $311 million, compared with $263 million for Q2 2025, an increase of $48 million or 18 percent

o
Advanced Materials & Chemicals (AM&C) revenues were $105 million, compared with $75 million for Q2 2025, an increase of $30 million or 40 percent

o
Print revenues were $195 million, compared with $178 million for Q2 2025, an increase of $17 million or 10 percent

•
Gross profit of $82 million, compared with $51 million for Q2 2025, an increase of $31 million or 61 percent

•
Gross profit percentage of 26 percent, compared with 19 percent for Q2 2025, an increase of 7 percentage points

•
GAAP net income of $17 million, compared with GAAP net loss of $26 million for Q2 2025, an increase of $43 million

•
Operational EBITDA of $36 million, compared with $9 million for Q2 2025, an increase of $27 million

•
A quarter-end cash balance of $290 million, compared with $337 million on December 31, 2025, a decrease of $47 million primarily driven by the repayments of the Term Loans, partially offset by cash received from the redemptions of KRIP investment assets

Kodak Reports Second-Quarter 2026 Financial Results Page 2

•
Cash flow from operations improved $5 million from the prior year period

"The words that sum up our performance in the second quarter are stability and growth," said Jim Continenza, Kodak's Executive Chairman and CEO. "We continued to deliver strong results for the fourth consecutive quarter, achieving significant year-over-year improvement in revenue, gross profit and Operational EBITDA. The momentum we have built is the result of consistent execution of our long-term plan, especially our investments in product development and manufacturing infrastructure and our focus on operational excellence. Looking forward, we are entering a new phase in Kodak's transformation where we have the operational and financial leverage to focus on growth. To capitalize on that opportunity, we will continue to expand our core businesses, increase efficiency and accelerate our investments in R&D to support our growth initiatives."

For the quarter ended June 30, 2026, revenues were $311 million, an increase of $48 million or 18 percent compared to the same period in 2025.

GAAP net income was $17 million for the quarter, compared to GAAP net loss of $26 million in 2025, an increase of $43 million primarily due to improvements in gross profit, reduction in interest expense and lower asset impairments compared to the prior period, partially offset by lower pension income. Operational EBITDA for the quarter ended June 30, 2026, was $36 million, compared to $9 million in 2025, an increase of $27 million. The increase in Operational EBITDA was driven by improved pricing and higher volume, partially offset by higher silver and aluminum prices and selling, general and administrative costs primarily related to the net change in employee benefit reserves and costs associated with corporate infrastructure.

Kodak ended the quarter with a cash balance of $290 million, a decrease of $47 million from December 31, 2025. The decrease was primarily driven by the required repayment of the Term Loans of $101 million and an increase in inventory of $37 million primarily driven by silver and aluminum commodities, partially offset by cash proceeds from redemptions of Kodak Retirement Income Plan reversion investments of $87 million.

##

Kodak Reports Second-Quarter 2026 Financial Results Page 3

Revenue and Operational EBITDA by Reportable Segment Q2 2026 vs. Q2 2025

(in millions)
Q2 2026 Actuals | Print | Advanced Materials & Chemicals | Brand | Total
Revenue | 195 | 105 | 7 | 307
Operational EBITDA * | 8 | 22 | 6 | 36
Q2 2025 Actuals | Print | Advanced Materials & Chemicals | Brand | Total
Revenue | 178 | 75 | 6 | 259
Operational EBITDA * | (4 | 8 | 5 | 9
Q2 2026 vs. Q2 2025 Actuals B(W) | Print | Advanced Materials & Chemicals | Brand | Total
Revenue | 17 | 30 | 1 | 48
Operational EBITDA * | 12 | 14 | 1 | 27

* Total Operational EBITDA is a non-GAAP financial measure. The reconciliation between GAAP and non-GAAP measures is provided in Appendix A of this press release.

Foreign currency had no impact on revenues or Operational EBITDA for the three months ended June 30, 2026 compared to the three months ended June 30, 2025.

Eastman Business Park segment is not a reportable segment and is excluded from the tables above.

About Kodak

Kodak (NYSE: KODK) is a leading global manufacturer focused on commercial print and advanced materials & chemicals. With 79,000 worldwide patents earned over 130 years of R&D, we believe in the power of technology and science to enhance what the world sees and creates. Our innovative, award-winning products, combined with our customer-first approach, make us the partner of choice for commercial printers worldwide. Kodak is committed to environmental stewardship, including industry leadership in developing sustainable solutions for print. For additional information on Kodak, visit us at kodak.com , or follow us on X @Kodak and LinkedIn .

Kodak Reports Second-Quarter 2026 Financial Results Page 4

Kodak Reports Second-Quarter 2026 Financial Results Page 5

policies, including tariffs or other trade restrictions or the threat of such actions, intellectual property rights, and commodity supply constraints; Kodak's ability to effectively anticipate technology and industry trends, including related to artificial intelligence (AI), and develop and market new products, solutions and technologies, including products based on its technology and expertise that relate to industries in which it does not currently conduct material business; Kodak's ability to effect strategic transactions, such as investments, acquisitions, strategic alliances, divestitures and similar transactions, or to achieve the benefits sought to be achieved from such strategic transactions; Kodak's ability to comply with the covenants in its various credit facilities; Kodak's continued ability to manage, defend and resolve a variety of current and legacy claims without incurring material losses or disruptions to its business and to bear the costs associated with such claims; Kodak's ability to discontinue, sell or spin-off certain non-core businesses or operations, or otherwise monetize assets; and the potential impact of force majeure events, cyber‐attacks or other data security incidents or information technology (IT) outages that could disrupt or otherwise harm Kodak's operations.

Kodak Reports Second-Quarter 2026 Financial Results Page 6

The following table reconciles the most directly comparable GAAP measure of Net Earnings (Loss) to Operational EBITDA for the three months ended June 30, 2026 and 2025, respectively:

(in millions) | Q2 2026 | Q2 2025 | $Change | % Change
Net Earnings (Loss) | 17 | (26 | 43 | (165 | )%
All other | (1 | — | (1
Depreciation and amortization | 6 | 7 | (1
Restructuring costs and other | 1 | 6 | (5
Stock based compensation | 9 | 1 | 8
Consulting and other costs (1) | — | (1 | 1
Idle costs (2) | 2 | 1 | 1
Other operating expense, net (3) | 4 | — | 4
Interest expense (3) | 6 | 15 | (9
Pension income excluding service cost component (3) | (5 | (16 | 11
Loss on early extinguishment of debt (3) | 1 | — | 1
Other (income) charges, net (3) | (8 | 20 | (28
Provision for income taxes (3) | 4 | 2 | 2
Operational EBITDA | 36 | 9 | 27 | 300 | %

Footnote Explanations:

(1)
Consulting and other costs are professional services and internal costs associated with corporate strategic initiatives and litigation. Consulting and other costs included $1 million of income in the three months ended June 30, 2025, representing insurance reimbursement of legal costs previously paid by the Company associated with investigations and litigation matters.

(2)
Consists of third-party costs such as security, maintenance, and utilities required to maintain land and buildings in certain locations not used in any Kodak operations and the costs, net of any rental income received, of underutilized portions of certain properties .

(3)
As reported in the Consolidated Statement of Operations.

Kodak Reports Second-Quarter 2026 Financial Results Page 7

A.
FINANCIAL STATEMENTS

Eastman Kodak Company

Consolidated Statement of Operations (Unaudited)

Three Months Ended
June 30,
(in millions, except per share data) | 2026 | 2025
Revenues
Sales | 276 | 226
Services | 35 | 37
Total revenues | 311 | 263
Cost of revenues
Sales | 206 | 184
Services | 23 | 28
Total cost of revenues | 229 | 212
Gross profit | 82 | 51
Selling, general and administrative expenses | 53 | 41
Research and development costs | 9 | 9
Restructuring costs and other | 1 | 6
Other operating expense, net | 4 | —
Earnings (loss) from operations before interest expense, pension income excluding service cost component, loss on early extinguishment of debt, other (income) charges, net and income taxes | 15 | (5
Interest expense | 6 | 15
Pension income excluding service cost component | (5 | (16
Loss on early extinguishment of debt | 1 | —
Other (income) charges, net | (8 | 20
Earnings (loss) from operations before income taxes | 21 | (24
Provision for income taxes | 4 | 2
NET EARNINGS (LOSS) | 17 | (26
Basic net earnings (loss) per share attributable to Eastman Kodak Company common shareholders | 0.13 | (0.36
Diluted net earnings (loss) per share attributable to Eastman Kodak Company common shareholders | 0.13 | (0.36
Number of common shares used in basic and diluted net earnings (loss) per share
Basic | 97.8 | 80.9
Diluted | 102.8 | 80.9

The notes accompanying the financial statements contained in the second quarter Form 10-Q are an integral part of these consolidated financial statements.

Kodak Reports Second-Quarter 2026 Financial Results Page 8

Eastman Kodak Company

Consolidated Statement of Financial Position (Unaudited)

June 30, | December 31,
(in millions, except per share data) | 2026 | 2025
ASSETS
Cash and cash equivalents | 290 | 337
Trade receivables, net of allowances of $7 at both periods | 149 | 145
Inventories, net | 253 | 218
Other current assets | 74 | 141
Total current assets | 766 | 841
Property, plant and equipment, net of accumulated depreciation of $507 and $499, respectively | 196 | 191
Goodwill | 12 | 12
Intangible assets, net | 17 | 17
Operating lease right-of-use assets | 34 | 37
Restricted cash | 90 | 96
Pension and other postretirement assets | 304 | 302
Other long-term assets | 108 | 121
TOTAL ASSETS | 1,527 | 1,617
LIABILITIES, REDEEMABLE CONVERTIBLE PREFERRED STOCK AND EQUITY
Accounts payable, trade | 108 | 101
Short-term borrowings and current portion of long-term debt | 2 | 1
Current portion of operating leases | 11 | 11
Other current liabilities | 142 | 155
Total current liabilities | 263 | 268
Long-term debt, net of current portion | 108 | 208
Pension and other postretirement liabilities | 186 | 191
Operating leases, net of current portion | 27 | 30
Other long-term liabilities | 246 | 207
Total liabilities | 830 | 904
Commitments and Contingencies (Note 9)
Redeemable, convertible preferred stock, no par value, $100 per share liquidation preference | 74 | 99
EQUITY
Common stock, $0.01 par value | 1 | 1
Additional paid in capital | 1,286 | 1,278
Treasury stock, at cost | (29 | (26
Accumulated deficit | (520 | (521
Accumulated other comprehensive loss | (115 | (118
Total shareholders' equity | 623 | 614
TOTAL LIABILITIES, REDEEMABLE CONVERTIBLE PREFERRED STOCK AND EQUITY | 1,527 | 1,617

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-12_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

EXECUTIVE OVERVIEW

The following MD&A provides a historical and prospective narrative on the Company's financial condition and results of operations for the year ended December 31, 2025 as compared to the year ended December 31, 2024. Cross references to Notes in this MD&A are to the Notes in the Financial Statements included in Part II, Item 8, "Financial Statements and Supplementary Data". The discussion of the Company's financial condition and results of operations for the year ended December 31, 2024 compared to 2023 is included in Part II, Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations in the Company's Annual Report on Form 10–K for the year ended December 31, 2024.

Consolidated revenues in the year ended December 31, 2025 were $ 1.069 billion, an increase of $ 26 million (2%) from 2024 . Currency fluctuations impacted revenue favorably in 2025 compared to 2024 ($11 million).

Print revenues, which accounted for 67% of Kodak's total revenues in 2025, declined by $ 22 million (3%) compared to 2024. Advanced Materials and Chemicals revenue improved $45 million (17%) from 2024 to 2025.

Economic Environment and Other Global Events

Kodak's products are sold and serviced in numerous countries across the globe with more than half of sales generated outside the U.S. Current global economic conditions remain highly volatile due to the uncertain and unpredictable macroeconomic environment, heightened levels of inflation, changes in trade policies, including tariffs or other trade restrictions or the threat of such actions, fluctuations in commodity prices and other global events which impacted Kodak's operations.

The U.S. government imposed new tariffs on a range of imported goods, including aluminum, steel and certain raw materials and component parts used in Kodak's manufacturing and supply chain. The tariffs imposed have resulted in increased manufacturing costs which the Company has been able to largely mitigate through pricing actions, supplier negotiations, obtaining certain exemptions and other cost savings measures. As a result of these actions, the tariffs that have been enacted or expanded by the U.S. did not have a material adverse effect on Kodak's operations, financial condition or cash flows for the year ended December 31, 2025.

Kodak continues to actively monitor the developments related to tariffs and to assess additional actions that may be taken to mitigate the effects of future tariff changes, including further pricing actions, additional cost reduction measures, securing alternative suppliers and evaluating potential changes to the Company's manufacturing footprint.

However, there is substantial uncertainty about the duration of existing tariffs or pauses in tariffs, tariff levels and whether additional tariffs or other retaliatory actions may be imposed, modified or suspended. Countries subject to such tariffs have imposed or may in the future impose reciprocal or retaliatory tariffs and other trade measures. These actions and the related rising political tensions could negatively impact global macroeconomic conditions and the stability of global financial markets. The ultimate impact of any tariffs is uncertain and will depend on various factors, including whether the tariffs are maintained and/or implemented, the duration of the tariffs, any exceptions or exemptions that are or may become available and the timing of their implementation,

amount and scope, all of which could have a material adverse effect on Kodak's business, financial condition and results of operations.

Kodak has experienced revenue declines primarily within its Print segment due to a slowdown in customer demand largely for plates related to global economic conditions that have negatively impacted volume. The Print segment has implemented various pricing actions and customer-focused initiatives to reduce the impact of lower volumes on revenue. In addition, the Advanced Materials and Chemicals segment implemented various pricing actions primarily within its Industrial Films and Chemicals and Motion Picture businesses.

Kodak is experiencing increased manufacturing costs for certain businesses due to lower volumes and increases in labor, material and distribution costs, as well as supply chain disruptions and shortages in materials and labor. In addition to the pricing actions and customer-focused initiatives described above, Kodak has implemented supply chain and workforce optimization, productivity improvements and other cost savings activities. The combined actions have largely mitigated the impact of increased manufacturing costs. However, the potential worsening of economic conditions, continued decreases in volume and increases in manufacturing and other costs without further price increases, productivity improvements or other cost saving measures, could unfavorably impact Kodak's operating results.

The Advanced Materials and Chemicals segment has also experienced labor shortages in certain manufacturing areas. Increased demand for consumer film products along with manufacturing equipment limitations and labor shortages have contributed to increased backorders. During 2024, the Advanced Materials and Chemicals segment reduced the amount of backorders compared to levels seen in prior years. This was driven by increased headcount and capital investments in equipment upgrades and new equipment that increased capacity and streamlined processes. Increased demand for film products may continue to place stress on manufacturing equipment and the labor force without further investment or additional hiring in specific areas.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

RESULTS OF OPERATIONS

Year Ended | Year Ended
December 31, | % of | December 31, | % of | $ Change vs.
(in millions) | 2025 | Sales | 2024 | Sales | 2024
Revenues | 1,069 | 1,043 | 26
Cost of revenues | 837 | 840 | (3
Gross profit | 232 | 22 | % | 203 | 19 | % | 29
Selling, general and administrative expenses | 174 | 16 | % | 179 | 17 | % | (5
Research and development costs | 33 | 3 | % | 33 | 3 | % | —
Restructuring costs and other | 21 | 2 | % | 8 | 1 | % | 13
Other operating expense (income), net | 4 | 0 | % | (10 | (1 | %) | 14
(Loss) earnings from continuing operations before interest expense, pension income excluding service cost component, loss on early extinguishment of debt, other charges (income), net and income taxes | — | — | (7 | (1 | %) | 7
Interest expense | 62 | 6 | % | 59 | 6 | % | 3
Pension income excluding service cost component | (128 | (12 | %) | (173 | (17 | %) | 45
Loss on early extinguishment of debt | 7 | 1 | % | — | — | 7
Other charges (income), net | 171 | 16 | % | (3 | (0 | %) | 174
(Loss) earnings from continuing operations before income taxes | (112 | (10 | %) | 110 | 11 | % | (222
Provision for income taxes | 16 | 1 | % | 8 | 1 | % | 8
NET (LOSS) EARNINGS | (128 | (12 | %) | 102 | 10 | % | (230

Revenues

For the year ended December 31, 2025, revenues increased approximately $ 26 million compared with 2024 primarily due to improved pricing in Print ($29 million) and Advanced Materials and Chemicals ($26 million), higher volume in Advanced Materials and Chemicals ($19 million), favorable foreign currency fluctuations ($11 million) and higher volume in Brand ($3 million), partially offset by lower volume in Print ($62 million). See segment discussions for additional details.

Gross Profit

Gross profit for 2025 increased approximately $29 million compared with 2024, primarily due to improved pricing in Print ($27 million) and Advanced Materials and Chemicals ($24 million), lower inventory reserve adjustments for Electrophotographic Printing Solutions ("EPS") compared to the prior year ($5 million), higher volume in Advanced Materials and Chemicals ($4 million) and Brand ($3 million) and favorable foreign currency fluctuations ($1 million). These favorable impacts were partially offset by higher manufacturing costs in Print ($11 million) and Advanced Materials and Chemicals ($7 million), higher aluminum costs ($9 million) and lower volumes in Print ($7 million). See segment discussions for additional details.

Selling, General and Administrative Expenses

Consolidated Selling, General & Administrative expenses (SG&A) decreased $5 million in 2025 compared with 2024 primarily due to a decline in selling and administrative costs ($5 million) related to lower spending on organizational changes compared to the prior year, along with a decline in consulting and project costs ($1 million) primarily related to an insurance reimbursement received in the second quarter of 2025 and a decline in equity compensation costs ($1 million). These favorable impacts were partially offset by the net change in employee benefit reserves ($2 million).

Research and Development Costs

Consolidated R&D expenses were flat in 2025 compared with 2024.

Restructuring Costs and Other

These costs, as well as restructuring costs reported in Cost of revenues, are discussed under the "Restructuring Costs and Other" section in this MD&A and Note 19, "Restructuring Costs and Other."

Interest Expense

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-12_item1_business.md)

ITEM 1. BU SINESS

When used in this report, unless otherwise indicated, "we," "our," "us," the "Company" and "Kodak" refer to the consolidated company on the basis of consolidation described in Note 1 to the consolidated financial statements in Part II, Item 8, "Financial Statements and Supplementary Data" of this Form 10-K Report.

Kodak is a global manufacturer focused on commercial print and advanced materials and chemicals. With 79,000 patents earned over 130 years of research and development ("R&D"), Kodak believes in the power of technology and science to enhance what the world sees and creates. Kodak's innovative, award-winning products, combined with its customer-first approach, make us the partner of choice for commercial printers worldwide. Kodak is committed to environmental stewardship, including industry leadership in developing sustainable solutions for print.

The Company was founded by George Eastman in 1880 and incorporated in 1901 in the State of New Jersey. Kodak is headquartered in Rochester, New York.

DESCRIPTION OF THE BUSINESS

Kodak's operations are classified into three reportable segments: Print, Advanced Materials and Chemicals, and Brand. The balance of Kodak's continuing operations, which do not meet the criteria of a reportable segment, are reported in All Other and primarily represent the Eastman Business Park ("EBP") operations.

Print

The Print segment is comprised of four lines of business: the Prepress Solutions business, the Prosper business, the Software business and the Electrophotographic Printing Solutions business. Print segment products include digital offset plate offerings and computer-to-plate ("CTP") imaging solutions, production press systems, consumables (primarily ink), inkjet components, software and services, and high-quality digital printing solutions using electrically charged toner-based technology. The Print segment serves a variety of commercial industries, including commercial print, direct mail, book publishing, newspapers and magazines and packaging/labels. Print products are sold to customers through both a direct sales team as well as indirectly through dealers and channel partners. Key competitors are Fuji, EC03, HP, Canon, Ricoh and Screen. Products and services included in Kodak's offerings are described below.

This segment is experiencing challenges from higher raw material and other supply chain costs, including impacts from tariffs, competitive pricing pressures and declines in volume. Refer to the Business Overview and Strategy section of Item 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations" for additional information on the opportunities and challenges related to the Print segment.

•
Prepress Solutions:

•
The Prepress Solutions business provides digital offset plate offerings and CTP imaging solutions.

•
The goal of Prepress Solutions is to pursue a contract-based, stable and recurring cash flow-generative business model. The average duration of customer contracts is two years. These contracts generate recurring revenue. The core of the business is the manufacturing of aluminum digital printing plates of varying sizes. These plates can be as small as 23cm x 27cm and as large as 126cm x 287cm. Unexposed plates are sold to commercial printing companies for use in the offset printing process. Kodak also manufactures equipment, known as CTP equipment, which images the plates with a laser. The offset printing process transfers ink from the plate onto a rubber blanket and then onto the substrate to be printed. Due to the nature of the imaging and printing process, a new plate must be used for each printing run. As a result, there is a recurring revenue stream from the sale of these plates.

•
The Digital offset plate offerings include KODAK SONORA Process Free Plates. Instead of the traditional process in which a plate is run through processing equipment containing a solution of developer, chemicals and water to set the image, KODAK SONORA Process Free Plates enable printers to set the image on the platesetter, then go directly to press. Processing variability is eliminated, so process-free plate users benefit from more consistent and stable plates. The solution is designed to be a much more environmentally friendly approach that could eliminate all processing chemicals, water and excess energy and waste from the plate-making process. These plates are designed to deliver cost savings and efficiency for customers and promote environmental sustainability practices.

•
Prosper:

•
The Prosper business product offerings include PROSPER press systems and PROSPER components, based on KODAK's Continuous Inkjet Technologies KODAK Stream and ULTRASTREAM, along with KODACHROME and KODAK EKTACOLOR Inks and KODAK OPTIMAX Primers. Examples include the PROSPER 7000 Turbo Press and the PROSPER ULTRA 520 Press, which is powered by ULTRASTREAM, Kodak's 4th generation inkjet technology, which Kodak believes delivers exceptional quality at the fastest speeds, even on the most demanding jobs with heavy ink coverage on glossy and coated papers.

•
In addition to Kodak-branded presses, PROSPER print head components are integrated into original equipment manufacturer ("OEM") partner products and systems. Applications include publishing, commercial print, direct mail, packaging and décor. The modular and scalable design of print heads powered by our ULTRASTREAM inkjet technology facilitates integration in print widths from 104 – 2500 mm (4" – 98") for applications on paper, film, plastic, and other substrates, expanding the footprint of inkjet printing to take on the challenges of a new age of digital printing.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-12_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-12_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-12_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2026-03-12_item7_mdna.md, 10-K_2026-03-12_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
