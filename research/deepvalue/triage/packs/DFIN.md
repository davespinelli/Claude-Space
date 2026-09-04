# Triage pack — DFIN · Donnelley Financial Solutions, Inc.

_Generated 2026-09-04 13:59 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** DFIN · **Name:** Donnelley Financial Solutions, Inc.
- **CIK:** 0001669811
- **SIC:** 7380 — Services-Miscellaneous Business Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/DFIN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Donnelley Financial Solutions, Inc.
- **CIK:** 1,669,811 · **SIC:** 7380 (Services-Miscellaneous Business Services) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 49.07 |
| mktcap | $1.2B |
| ev | $1.4B |
| ev_ebit | 9.8x |
| fcf | $107.8M |
| fcf_yield | 8.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 19.9% |
| net_debt | $172.9M |
| net_debt_ebit | 1.2x |
| cash | $25.3M |
| ltd | $198.2M |
| equity | $387.4M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $767.0M |
| revenue_prior | $781.9M |
| rev_growth | -1.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $141.1M |
| net_income | $32.4M |
| cfo | $164.9M |
| capex | $57.1M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -10.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 24,585,383 |
| shares_py | 27,494,777 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -10.3% |
| r6m | -7.3% |
| off_52w_high | -13.8% |
| adv20 | $9.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.69 |
| r_ev_ebit | 0.78 |
| r_roic | 0.88 |
| r_rev_growth | 0.27 |
| r_buyback | 0.95 |
| score | 0.71 |

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
| rank | 54 |

**Screen rationale:** cheap at 9.8x EV/EBIT; high ROIC 19.9%; buying back stock -10.6%


## 3. Share count trend

- Shares outstanding: **24,585,383** (CY2026Q2I) vs **27,494,777** prior year (CY2025Q2I)
- Change: **-10.6%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-14** — Item 5.02 (officer / director change or comp arrangement): (b) On May 14, 2026, Donnelley Financial Solutions, Inc. (the "Company") announced that Craig Clay, a named executive officer, will transition out of his current position as the Company's Executive Vice President, President of Global Capital Markets.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 20,780 sh / $999,990 vs sells 10,000 sh / $500,000 -> net $499,990 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: BINZ JOSEPH LEO bought 10,000 sh @ $48.52 ($485,245) on 2026-09-01.

Form 4 filings parsed: 12; transaction rows: 14 (open-market buys 3, sales 2).

| code | rows |
|---|---|
| A | 8 |
| F | 1 |
| P | 3 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'DFIN Reports Second-Quarter 2026 Results'; skipped 13 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (dfin-ex99_1.htm)

DFIN Reports Second-Quarter 2026 Results

CHICAGO – July 30, 2026 – Donnelley Financial Solutions, Inc. (NYSE: DFIN) (the "Company" or "DFIN") today reported financial results for the second quarter of 2026.

Second-Quarter 2026 | Second-Quarter 2025 | $ Change | % Change
Net Sales | $224.2 million | $218.1 million | $6.1 million | 2.8%
Net Earnings | $36.4 million | $36.1 million | $0.3 million | 0.8%
Adjusted EBITDA (a) | $82.3 million | $76.3 million | $6.0 million | 7.9%
Operating Cash Flow (b) | $74.7 million | $68.4 million | $6.3 million | 9.2%
Free Cash Flow (a) | $61.2 million | $51.7 million | $9.5 million | 18.4%
Diluted Shares Outstanding (c) | 25.3 million | 28.2 million | (2.9 million) | (10.3%)

Highlights for the second quarter of 2026:

•
Total net sales of $224.2 million, an increase of $6.1 million, or 2.8%, from the second quarter of 2025. Total net sales were comprised of:

o
Software solutions net sales of $99.4 million, an increase of $7.2 million, or 7.8%,

o
Tech-enabled services net sales of $90.2 million, an increase of $5.0 million, or 5.9%,

o
Print and distribution net sales of $34.6 million, a decrease of $6.1 million, or 15.0%.

•
Software solutions net sales accounted for 44.3% of total net sales, up from 42.3% in the second quarter of 2025.

•
Net earnings of $36.4 million, or $1.44 per diluted share, as compared to $36.1 million, or $1.28 per diluted share, in the second quarter of 2025.

•
Adjusted EBITDA (a) of $82.3 million, up $6.0 million, or 7.9%, from the second quarter of 2025; Adjusted EBITDA margin (a) of 36.7%, up approximately 170 basis points from the second quarter of 2025.

•
Gross leverage (a) of 0.8x and net leverage (a) of 0.7x as of June 30, 2026.

•
The Company repurchased 763,451 shares for approximately $34.7 million at an average price of $45.48 per share. As of June 30, 2026, there was $125.4 million remaining on our current $150 million share repurchase authorization.

•
Appointed Ken Napolitano as Chief Revenue Officer to advance the Company's sales transformation and support its long-term growth strategy.

(a) Adjusted EBITDA, Adjusted EBITDA margin, Free Cash Flow, gross leverage and net leverage are non-GAAP financial measures that exclude the impact of certain items noted in the reconciliation tables below. The tables below provide reconciliations to the most comparable GAAP measures.

(b) Defined as net cash provided by operating activities.

(c) Defined as diluted weighted-average number of common shares outstanding.

"We are pleased with our strong second-quarter results, which reflect continued momentum in our operating performance, as we delivered the third consecutive quarter of consolidated net sales growth, an increase in Adjusted EBITDA, and Adjusted EBITDA margin expansion. Total net sales increased by 2.8% from the second quarter of 2025, primarily driven by a rebound in capital markets transactional activity as well as continued growth of our software solutions, despite a moderate decline in traditional compliance revenue, part of which was related to lower print and distribution revenue. The growth in higher-margin capital markets transactional and software solutions net sales, along with the impact of permanent changes to our cost structure and ongoing operating efficiencies, expanded second-quarter Adjusted EBITDA margin to 36.7%, an increase of approximately 170 basis points year-over-year. Additionally, improved profitability combined with lower capital expenditures resulted in strong improvements in both operating cash flow and free cash flow," said Daniel N. Leib, DFIN's President and Chief Executive Officer.

Leib continued, "During the second quarter, we continued to execute our strategy to expand the adoption of our software solutions offerings. We delivered record quarterly software solutions net sales of $99.4 million, an increase of 7.8% compared to the second quarter of 2025, driven by the continued momentum in ActiveDisclosure, a component of our compliance offerings, which grew approximately 29%. Venue delivered strong sequential net sales improvement, which resulted in modest year-over-year growth despite overlapping a large project which benefited last year's second-quarter sales. Software solutions net sales made up 44.3% of second-quarter 2026 total net sales, an increase from 42.3% of last year's second-quarter sales mix. In addition, the capital markets transactional environment remained active during the second quarter, despite heightened geopolitical uncertainty and market volatility, resulting in better-than-expected transactional revenue."

"Our second-quarter performance, including the momentum of our top- and bottom-line results, highlights the progress we are making in our transformation. Our strategy and focus have resulted in DFIN being fundamentally and sustainably more profitable, as we continue to invest to achieve a more recurring sales mix, while aggressively managing our cost structure and being disciplined stewards of capital. While the macroeconomic outlook remains uncertain, the combination of our market position, cost structure, and strong balance sheet positions us well heading into the back half of the year," Leib concluded.

Net Sales

Net sales in the second quarter of 2026 were $224.2 million, an increase of $6.1 million, or 2.8%, from the second quarter of 2025. Net sales increased primarily due to higher capital markets transactional volumes and growth in software solutions net sales, primarily driven by ActiveDisclosure, partially offset by lower capital markets and investment companies traditional compliance revenue, part of which is related to lower print and distribution volumes.

Net Earnings

For the second quarter of 2026, net earnings were $36.4 million, or $1.44 per diluted share, as compared to $36.1 million, or $1.28 per diluted share, in the second quarter of 2025. Net earnings in the second quarter of 2026 included after-tax charges of $8.1 million, or $0.32 per diluted share, primarily related to share-based compensation expense and restructuring, impairment and other charges, net. Net earnings in the second quarter of 2025 included after-tax charges of $6.0 million, or $0.21 per diluted share, primarily related to share-based compensation expense and restructuring, impairment and other charges, net.

Adjusted EBITDA and Adjusted Non-GAAP Net Earnings

For the second quarter of 2026, Adjusted EBITDA was $82.3 million, an increase of $6.0 million as compared to the second quarter of 2025. Adjusted EBITDA margin was 36.7%, up approximately 170 basis points from the second quarter of 2025. The increase in Adjusted EBITDA and Adjusted EBITDA margin was primarily due to higher net sales, a favorable sales mix driven by the growth in higher-margin software solutions and tech-enabled services net sales, and cost control initiatives, partially offset by higher selling expense as a result of the increase in sales volumes.

For the second quarter of 2026, adjusted non-GAAP net earnings were $44.5 million, or $1.76 per diluted share, as compared to $42.1 million, or $1.49 per diluted share, in the second quarter of 2025.

Reconciliations of reported net sales to organic net sales and consolidated net earnings (loss) to Adjusted EBITDA, Adjusted EBITDA margin and adjusted non-GAAP net earnings are presented in the tables.

Guidance

The Company provides the following guidance for the third quarter of 2026.

Third-Quarter Guidance
Total net sales | $175 million to $185 million
Adjusted EBITDA margin | 26% to 28%
Capital markets transactional net sales | $45 million to $50 million

About DFIN

DFIN is the leading global provider of compliance and regulatory software and services, fueling end-to-end investment company regulatory compliance needs, complex capital markets transactions, and essential financial reporting at every stage of the corporate lifecycle. Our mission is simple: to empower clients with the software and support they need to stay ahead of public company filings, investment company filings, private reporting, and beneficial owner reporting, while enhancing workflow efficiency. We bring deep expertise to every engagement, driving transparency and collaboration built on confidence and reliability. Learn more a t DFINsolutions.com or follow us on LinkedIn .

Investor Contact:

Mike Zhao

Investor Relations

investors@dfinsolutions.com

Use of Non-GAAP Information

This news release contains certain non-GAAP financial measures, including non-GAAP gross profit, adjusted non-GAAP gross profit, non-GAAP gross margin, adjusted non-GAAP selling, general and administrative expenses ("SG&A"), adjusted non- GAAP income from operations, adjusted non-GAAP operating margin, Adjusted EBITDA, Adjusted EBITDA margin, adjusted non-GAAP net earnings, adjusted non-GAAP earnings per diluted share, Free Cash Flow and organic net sales. The Company believes that these non-GAAP financial measures, when presented in conjunction with comparable GAAP measures, provide useful information about the Company's operating results and liquidity and enhance the overall ability to assess the Company's financial performance. The Company uses these measures, together with other measures of performance under GAAP, to compare the relative performance of operations in planning, budgeting and reviewing the performance of its business.

The Company's non-GAAP statement of operations measures, which include non-GAAP gross profit, adjusted non-GAAP gross profit, non-GAAP gross margin, adjusted non-GAAP SG&A, adjusted non-GAAP income from operations, adjusted non- GAAP operating margin, Adjusted EBITDA, Adjusted EBITDA margin, adjusted non-GAAP net earnings and adjusted non-GAAP net earnings per diluted share, are adjusted to exclude the impact of certain costs, expenses, gains and losses and other specified items that management believes are not indicative of our ongoing operations. These adjusted measures exclude the impact of expenses associated with the Company's pension plan settlement charge, non-income tax, net, accelerated rent (benefit) expense, share-based compensation expense and eliminate potential differences in results of operations between periods caused by factors such as historic cost and age of assets, financing and capital structures, taxation positions or regimes, restructuring, impairment and other charges, net and gain or loss on certain investments, business sales and asset sales.

Free Cash Flow is a non-GAAP financial measure and is defined by the Company as net cash flow provided by operating activities less capital expenditures. By adjusting for the level of capital investment in operations, the Company believes that free cash flow can provide useful additional basis for understanding the Company's ability to generate cash after capital investment and provides a comparison to peers with differing capital intensity.

Organic net sales is a non-GAAP financial measure and is defined by the Company as reported net sales adjusted for the changes in foreign currency exchange rates and the impact of dispositions.

These non-GAAP financial measures should be considered in addition to, not a substitute for, or superior to, measures of financial performance prepared in accordance with GAAP. In addition, these measures are defined differently by different companies in our industry and, accordingly, such measures may not be comparable to similarly-titled measures of other companies.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-17_item7_mdna.md)

_Extraction: started at the Overview heading._

Executive Overview

Net sales for the year ended December 31, 2025 decreased by $14.9 million, or 1.9%, to $767.0 million from $781.9 million for the year ended December 31, 2024, including a $0.8 million, or 0.1%, increase due to changes in foreign currency exchange rates. Net sales decreased primarily due to lower tech-enabled services net sales of $22.5 million, primarily driven by lower capital markets compliance volumes, and lower print and distribution net sales of $21.1 million, primarily driven by lower investment companies and capital markets compliance volumes, partially offset by higher software solutions net sales of $28.7 million, primarily due to higher ActiveDisclosure net sales of $12.7 million and higher Arc Suite net sales of $12.3 million.

Income from operations for the year ended December 31, 2025 increased by $4.5 million, or 3.3%, to $141.1 million from $136.6 million for the year ended December 31, 2024. Income from operations increased primarily due to lower cost of sales of $17.5 million and lower SG&A expenses of $13.0 million, partially offset by lower net sales of $14.9 million, as described above, a net gain of $9.8 million on the sale of land during the year ended December 31, 2024 and higher restructuring, impairment and other charges, net of $3.8 million. The lower cost of sales is largely driven by lower sales volumes, cost control initiatives and lower overhead costs, whereas the lower SG&A expenses are primarily driven by cost control initiatives, lower bad debt expense of $6.5 million, lower overhead costs and lower incentive compensation expense, partially offset by higher share-based compensation expense of $6.2 million and higher healthcare expense of $2.3 million.

Pension Plan Termination and Settlement

In August 2024, the Company executed an amendment to commence the process of terminating the Company's primary defined benefit plan (the "Plan"). During the year ended December 31, 2025, the Company settled the Plan obligations through a combination of lump sum payments to certain Plan participants and the purchase of a non-participating irrevocable group annuity contract (the "Plan Settlement"). In connection with the Plan Settlement, the Company made an $11.3 million, net cash contribution to fully fund the Plan.

As a result of the Plan Settlement, the Company remeasured the Plan's assets and obligations and recognized a non-cash settlement charge of $82.8 million during the year ended December 31, 2025, due to the recognition of unrealized accumulated Plan losses previously reported within accumulated other comprehensive loss on the audited Consolidated Balance Sheets. The Plan Settlement was recorded within Corporate.

Financial Review

In the financial review that follows, the Company discusses its consolidated results of operations, segment net sales, Segment Adjusted EBITDA, financial position, cash flows and certain other information. The Company's cost of sales as a percentage of net sales, consolidated income from operations, Segment Adjusted EBITDA and Segment Adjusted EBITDA margin may be affected by sales mix (i.e., a higher proportion of sales of higher or lower margin services or products relative to total sales). Sales mix can vary period to period and is impacted by regulatory filing seasonality and global capital markets volatility. This discussion and analysis should be read in conjunction with the Company's audited Consolidated Financial Statements and related notes thereto.

A discussion of the Company's financial condition, changes in financial condition and results of operations for the year ended December 31, 2024 as compared to the year ended December 31, 2023, can be found in Part II. Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations of DFIN's Annual Report on Form 10-K for the year ended December 31, 2024, filed with the SEC on February 18, 2025.

Results of Operations for the Year Ended December 31, 2025 as Compared to the Year Ended December 31, 2024

The following table shows the results of operations for the years ended December 31, 2025 and 2024:

Year Ended December 31,
2025 | 2024 | $ Change | % Change
(in millions, except percentages)
Net sales
Software solutions | 358.4 | 329.7 | 28.7 | 8.7 | %
Tech-enabled services | 298.3 | 320.8 | (22.5 | (7.0 | %)
Print and distribution | 110.3 | 131.4 | (21.1 | (16.1 | %)
Total net sales | 767.0 | 781.9 | (14.9 | (1.9 | %)
Cost of sales (a)
Software solutions | 111.4 | 107.4 | 4.0 | 3.7 | %
Tech-enabled services | 112.8 | 120.6 | (7.8 | (6.5 | %)
Print and distribution | 56.2 | 69.9 | (13.7 | (19.6 | %)
Total cost of sales | 280.4 | 297.9 | (17.5 | (5.9 | %)
Selling, general and administrative expenses (a) | 277.9 | 290.9 | (13.0 | (4.5 | %)
Depreciation and amortization | 59.3 | 60.2 | (0.9 | (1.5 | %)
Restructuring, impairment and other charges, net | 10.4 | 6.6 | 3.8 | 57.6 | %
Other operating income, net | (2.1 | (10.3 | 8.2 | (79.6 | %)
Income from operations | 141.1 | 136.6 | 4.5 | 3.3 | %
Interest expense, net | 12.9 | 12.9 | — | —
Pension plan settlement charge | 82.8 | — | 82.8 | nm
Investment and other loss (income), net | 2.3 | (1.4 | 3.7 | nm
Earnings before income taxes | 43.1 | 125.1 | (82.0 | (65.5 | %)
Income tax expense | 10.7 | 32.7 | (22.0 | (67.3 | %)
Net earnings | 32.4 | 92.4 | (60.0 | (64.9 | %)

nm – Not meaningful

(a)
Exclusive of depreciation and amortization

Consolidated

Net sales of software solutions of $358.4 million for the year ended December 31, 2025 increased $28.7 million, or 8.7%, as compared to the year ended December 31, 2024. Net sales of software solutions increased due to $12.7 million of higher ActiveDisclosure net sales, $6.5 million of increases in non-TSR-related Arc Suite net sales, $5.8 million of higher net sales from the Company's TSR offering and $3.7 million of higher Venue net sales.

Net sales of tech-enabled services of $298.3 million for the year ended December 31, 2025 decreased $22.5 million, or 7.0%, as compared to the year ended December 31, 2024. Net sales of tech-enabled services decreased due to lower capital markets net sales of $18.4 million, driven by a decline in both compliance and transactional volumes, as well as lower investment companies net sales of $4.1 million, largely driven by a decline in compliance volumes.

Net sales of print and distribution of $110.3 million for the year ended December 31, 2025 decreased $21.1 million, or 16.1%, as compared to the year ended December 31, 2024. Net sales of print and distribution decreased due to lower investment companies net sales of $14.0 million and lower capital markets net sales of $7.1 million, both largely driven by a decline in compliance volumes.

Software solutions cost of sales of $111.4 million for the year ended December 31, 2025 increased $4.0 million, or 3.7%, as compared to the year ended December 31, 2024. Software solutions cost of sales increased primarily due to higher product development costs of $1.4 million and a lower allocation of overhead costs. As a percentage of software solutions net sales, software solutions costs of sales decreased 1.5%, primarily driven by $12.7 million of higher ActiveDisclosure net sales and Arc Suite price increases, partially offset by higher product development costs and a lower allocation of overhead costs.

Tech-enabled services cost of sales of $112.8 million for the year ended December 31, 2025 decreased $7.8 million, or 6.5%, as compared to the year ended December 31, 2024. Tech-enabled services cost of sales decreased primarily due to lower sales volumes of $22.5 million, a lower allocation of overhead costs and cost control initiatives. As a percentage of tech-enabled services net sales, tech-enabled services cost of sales increased 0.2%.

Print and distribution cost of sales of $56.2 million for the year ended December 31, 2025 decreased $13.7 million, or 19.6%, as compared to the year ended December 31, 2024. Print and distribution cost of sales decreased primarily due to lower sales volumes of $21.1 million, a lower allocation of overhead costs and cost control initiatives. As a percentage of print and distribution net sales, print and distribution cost of sales decreased 2.2%, primarily driven by a lower allocation of overhead costs and cost control initiatives.

SG&A expenses of $277.9 million for the year ended December 31, 2025 decreased $13.0 million, or 4.5%, as compared to the year ended December 31, 2024. SG&A expenses decreased primarily due to cost control initiatives, lower bad debt expense of $6.5 million, lower overhead costs and lower incentive compensation expense, partially offset by higher share-based compensation expense of $6.2 million and higher healthcare expense of $2.3 million. As a percentage of net sales, SG&A expenses decreased from 37.2% for the year ended December 31, 2024 to 36.2% for the year ended December 31, 2025.

Depreciation and amortization of $59.3 million for the year ended December 31, 2025 decreased $0.9 million, or 1.5%, as compared to the year ended December 31, 2024, primarily due to $2.8 million of accelerated amortization expense related to discontinued software recorded during the year ended December 31, 2024 and lower depreciation expense of $1.5 million, partially offset by higher software amortization expense of $3.4 million, driven by additional software development.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-17_item1_business.md)

ITEM 1. B USINESS

Company Overview

DFIN is a leading global provider of compliance and regulatory software and services, supporting its clients' complex capital markets transactions and essential financial reporting at every stage of the corporate lifecycle and fueling end-to-end investment company regulatory compliance needs. The Company provides regulatory filing and deal solutions via its software, technology-enabled services and print and distribution solutions to public and private companies, mutual funds and other regulated investment firms, to serve its clients' regulatory and compliance needs. DFIN helps its clients comply with applicable regulations where and how they want to work in a digital world, providing numerous solutions tailored to each client's business needs. The prevailing trend is toward clients choosing to utilize the Company's software solutions, in conjunction with its tech-enabled services, to meet their document and filing needs, while at the same time shifting away from physical print and distribution of documents, except for when it is still regulatorily required or requested by clients.

The Company serves its clients' regulatory and compliance needs throughout their respective life cycles. For its capital markets clients, the Company offers solutions that allow companies to comply with U.S. Securities and Exchange Commission ("SEC") regulations and support their corporate financial transactions and regulatory/financial reporting through the use of digital document creation and online content management tools; filing agent services, where applicable; solutions to facilitate clients' communications with their investors; and virtual data rooms and other deal management solutions. For investment companies clients, the Company provides solutions that allow investment companies to comply with SEC regulations and support financial and regulatory reporting through the use of content management and technology-enabled solutions for creating, compiling and filing regulatory communications as well as digital-driven solutions for distributing content to investors.

Technological advancements, regulatory changes, and evolving workflow preferences have led to the Company's clients managing more of the financial disclosure process themselves, changing the marketplace for the Company's services and products. DFIN's strategy in its Software Solutions segments (CM-SS and IC-SS, as defined below) aligns with the changing marketplace by focusing the Company's resources in its advanced software solutions, primarily ActiveDisclosure® ("ActiveDisclosure"), Arc Suite® software platform ("Arc Suite") and Venue® Virtual Data Room ("Venue"), while making targeted investments to further enhance product features. In its Compliance & Communications Management segments (CM-CCM and IC-CCM, as defined below), the Company's strategy focuses on maintaining its market-leading position by offering a high-touch, service-oriented experience, using its unique combination of tech-enabled services and print and distribution capabilities.

Company History

On October 1, 2016, DFIN became an independent publicly traded company through the distribution by R.R. Donnelley & Sons Company ("RRD") of shares of DFIN common stock to RRD stockholders (the "Separation"). Since the Separation, the Company has primarily grown organically, focusing resources on software solutions development and making targeted investments to further enhance product features.

Capital Markets

The Company provides software solutions, tech-enabled services and print and distribution solutions to public and private companies for deal solutions and compliance to companies that are, or are preparing to become, subject to the filing and reporting requirements of the Securities Act of 1933, as amended (the "Securities Act") and the Securities Exchange Act of 1934, as amended (the "Exchange Act"). The Company supports clients primarily in North America, Europe and Asia. Capital markets clients leverage the Company's software offerings, proprietary technology, deep industry expertise and experience to successfully navigate the SEC's specified file formats when submitting documents through the SEC's Electronic Data Gathering, Analysis, and Retrieval ("EDGAR") system for their transactional and ongoing compliance needs.

The Company assists its capital markets clients throughout the course of initial public offerings ("IPOs"), secondary offerings, mergers and acquisitions ("M&A"), public and private debt offerings, leveraged buyouts, spinouts, special purpose acquisition companies ("SPAC") and subsequent de-SPAC transactions and other similar transactions. In addition, the Company provides clients with compliance solutions to prepare their ongoing required Exchange Act filings that are compatible with the SEC's EDGAR system, most notably Form 10-K, Form 10-Q, Form 8-K and proxy filings. These solutions include the Company's traditional full-service EDGAR filing preparation and filing agent services, tech-enabled services and print and distribution solutions as well as the Company's software solutions, ActiveDisclosure, predominantly a compliance solution, and Venue, predominantly a transactional solution.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-17_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-17_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-17_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-30_2-02-results.md, 10-K_2026-02-17_item7_mdna.md, 10-K_2026-02-17_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
