# Triage pack — AZTA · Azenta, Inc.

_Generated 2026-09-04 21:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** AZTA · **Name:** Azenta, Inc.
- **CIK:** 0000933974
- **SIC:** 3559 — Special Industry Machinery, NEC
- **Fiscal year end (MM-DD):** 09-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/AZTA

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Azenta, Inc.
- **CIK:** 933,974 · **SIC:** 3559 (Special Industry Machinery, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 31.18 |
| mktcap | $1.4B |
| ev | $1.2B |
| ev_ebit | n/a |
| fcf | $38.3M |
| fcf_yield | 2.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -1.6% |
| net_debt | -$189.7M |
| net_debt_ebit | n/a |
| cash | $189.7M |
| ltd | $0.00 |
| equity | $1.5B |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $593.8M |
| revenue_prior | $573.4M |
| rev_growth | 3.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$26.8M |
| net_income | -$55.8M |
| cfo | $72.2M |
| capex | $33.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -4.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 43,808,393 |
| shares_py | 45,839,728 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 8.3% |
| r6m | 25.8% |
| off_52w_high | -24.0% |
| adv20 | $25.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.36 |
| r_ev_ebit | 0.00 |
| r_roic | 0.26 |
| r_rev_growth | 0.47 |
| r_buyback | 0.87 |
| score | 0.44 |

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
| rank | 293 |

**Screen rationale:** buying back stock -4.4%; debt data missing (net cash unverified); 12-1 momentum 8.3%


## 3. Share count trend

- Shares outstanding: **43,808,393** (CY2026Q2I) vs **45,839,728** prior year (CY2025Q2I)
- Change: **-4.4%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-24** — Item 5.02 (officer / director change or comp arrangement): On August 22, 2026, John P. Marotta resigned as President and Chief Executive Officer of Azenta, Inc. (the "Company") and as a member of the Company's Board of Directors (the "Board"), effective as of August 22, 2026 (the "Effective Date").
- **2026-08-11** — Item 5.02 ((c)): On August 6, 2026, the Board of Directors (the "Board") of Azenta, Inc. (the "Company") appointed Erik J. Bello, age 51, as the Company's Vice President, Chief Accounting Officer, effective upon the commencement of his employment with the Company, which is...
- **2026-07-08** — Item 1.01 (Entry into a Material Definitive Agreement): On July 1, 2026, in connection with the closing of the Transaction (as defined in Item 2.01 below), Azenta Germany GmbH, a wholly owned subsidiary of Azenta, Inc. (the "Company"), entered into a Vendor Loan Agreement (the "Vendor Loan Agreement") with Thelema...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 10,335 sh / $171,896 vs sells 0 sh / $0 -> net $171,896 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Cornog William L bought 10,000 sh @ $16.38 ($163,800) on 2026-05-18.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 2, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 2 |
| P | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-04_2-02-results.md)

_Extraction: started at the first release heading, 'Azenta Reports Third Quarter Results for Fiscal 2026, Ended June 30, 2'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (azta-2026q326erxexx991.htm)

Azenta Reports Third Quarter Results for Fiscal 2026, Ended June 30, 2026.

BURLINGTON, Mass., August 4, 2026 (PR Newswire) – Azenta, Inc. (Nasdaq: AZTA) today reported financial results for the third quarter ended June 30, 2026.

The results of B Medical Systems are reported as discontinued operations and reflected in total diluted EPS. The Company entered into a definitive agreement to sell the business during fiscal 2025, and the transaction closed on July 1, 2026, on the terms described in the Company's Current Report on Form 8-K filed on July 8, 2026.

Quarter Ended
Dollars in millions, except per share data | June 30, | March 31, | June 30, | Change
2026 | 2026 | 2025 (1) | Prior Qtr | Prior Yr.
Revenue from Continuing Operations | 161 | 145 | 144 | 11 | % | 12 | %
Organic growth | 9 | %
Sample Management Solutions | 88 | 81 | 78 | 9 | % | 14 | %
Multiomics | 73 | 64 | 66 | 14 | % | 10 | %
Diluted EPS Continuing Operations | (0.03) | (3.41) | (0.01) | 99 | % | NM
Diluted EPS Total | 0.05 | (3.49) | (1.05) | NM | NM
Non-GAAP Diluted EPS Continuing Operations | 0.16 | (0.04) | 0.17 | NM | (6) | %
Adjusted EBITDA - Continuing Operations | 18 | 8 | 17 | NM | 6 | %
Adjusted EBITDA Margin - Continuing Operations | 11.4 | % | 5.4 | % | 12.1 | %

(1) Reflects revisions for an immaterial classification error among cost of revenue, research and development expenses, and selling, general and administrative expenses, and other immaterial adjustments, as further described in the Annual Report on Form 10-K for the fiscal year ended September 30, 2025.

Management Comments

"Despite an uneven and challenging market backdrop, our third quarter results exceeded our expectations, with continued strength in our recurring revenue businesses, and a modest improvement in Multiomics in North America," said John Marotta, President and Chief Executive Officer. "While these results represent an encouraging step forward, our turnaround continues, and we remain focused on executing against our strategic priorities."

Third Quarter Fiscal 2026 Results - Continuing Operations

• Revenue was $161 million, up 12% year over year. Organic revenue, which excludes a 1-percentage point impact from foreign exchange and a 3-percentage point impact from the acquisition of UK Biocentre Limited, was up 9% year over year, reflecting higher revenue in Sample Management Solutions and Multiomics.

• Sample Management Solutions revenue was $88 million, up 14% year over year.

◦ Organic revenue, which excludes the impact from foreign exchange and the contribution from the acquisition of UK Biocentre Limited, was up 9%, mainly driven by higher revenue in Sample Repository Solutions and Consumables and Instruments, partially offset by lower revenue in Automated Stores.

• Multiomics revenue was $73 million, up 10% year over year.

◦ Organic revenue, which excludes the impact from foreign exchange, was up 8% year over year, primarily driven by higher revenue in Next Generation Sequencing and Gene Synthesis, partially offset by lower Sanger Sequencing revenue.

Summary of GAAP Earnings Results - Continuing Operations

• Operating loss was $4.2 million. Operating margin was (2.6%), down 131 basis points year over year.

◦ Gross margin was 44.9%, a decrease of 130 basis points year over year, primarily driven by unfavorable fixed-cost absorption associated with lower sales volumes in certain areas of the portfolio as well as costs related to quality remediation and rework activities in Automated Stores. These impacts were partially offset by improved operating leverage and the benefits of ongoing cost initiatives.

◦ Operating expenses in the quarter were $77 million, up 12% year over year, driven by higher research and development expenses and higher selling, general and administrative expenses, partially offset by lower restructuring and transformation charges.

• Total other income included $4 million of net interest income, versus $5 million in the prior year period.

• Diluted EPS from continuing operations was ($0.03) compared to ($0.01) in the third quarter of fiscal year 2025. Diluted EPS from discontinued operations was $0.09, compared to ($1.04) a year ago. Total diluted EPS was $0.05, compared to ($1.05) a year ago.

Summary of Non-GAAP Earnings Results - Continuing Operations

• Adjusted operating income was $4.7 million. Adjusted operating margin was 2.9%, a decrease of 180 basis points year over year.

◦ Adjusted gross margin was 46.2%, down 140 basis points compared to the third quarter of fiscal 2025, primarily driven by unfavorable fixed-cost absorption associated with lower sales volumes in certain areas of the portfolio as well as costs related to quality remediation and rework activities in Automated Stores. These impacts were partially offset by improved operating leverage and the benefits of ongoing cost initiatives.

◦ Adjusted operating expenses in the quarter were $70 million, up 13% year over year, driven by higher selling, general and administrative expenses and higher research and development expenses.

• Adjusted EBITDA was $18.5 million, and Adjusted EBITDA margin was 11.4%, a decrease of 60 basis points year over year.

• Non-GAAP Diluted EPS was $0.16, compared to $0.17 one year ago.

Cash and Liquidity as of June 30, 2026

• The Company ended the quarter with a total balance of cash, cash equivalents, restricted cash and marketable securities of $529 million.

• Operating cash flow was $1 million in the quarter. Capital expenditures were $7 million, and free cash flow (cash flow from operations less capital expenditures) was negative $5 million.

Share Repurchase Program Update

• On December 8, 2025, our Board of Directors approved a share repurchase program authorizing the repurchase of up to $250 million of our common stock through December 31, 2028, or the 2025 Repurchase Program. Repurchases under the 2025 Repurchase Program may be made in the open market or through privately negotiated transactions (including under an accelerated share repurchase agreement), or by other means, including through the use of trading plans intended to qualify under Rule 10b5-1 under the Exchange Act, subject to market and business conditions, legal requirements, and other factors. As of June 30, 2026, the Company repurchased 2.3 million shares of common stock for $50.0 million (excluding fees, commissions, and excise tax) pursuant to the 2025 Repurchase Program. All shares of common stock repurchased under the 2025 Repurchase Program have been retired.

Fourth Quarter Fiscal 2026 Guidance - Continuing Operations

• Total organic revenue, which excludes the impact of foreign exchange and the contribution from the acquisition of UK Biocentre Limited, is expected to decline approximately in the low single digits relative to the fourth quarter of fiscal 2025.

• Adjusted EBITDA is expected to range approximately between $20 million and $23 million.

Full Year Fiscal 2026 Guidance - Continuing Operations

The Company now expects total reported revenue from continuing operations to range approximately between $613 to $618 million, compared to prior guidance of $603 to $621 million for the fiscal year ending September 30, 2026.

• Total organic revenue, which excludes the impact of foreign exchange and the contribution from the acquisition of UK Biocentre Limited, is now expected to range approximately between flat to up 1%, compared to prior guidance of down 2% to up 1% relative to fiscal 2025.

◦ Organic revenue for Sample Management Solutions is expected to grow low-single-digits, consistent with prior guidance.

◦ Organic revenue for Multiomics is now expected to range approximately between down 1% to flat, compared to prior guidance of down mid-single-digits.

• Adjusted EBITDA is expected to be in the range of $59 million to $62 million, including an anticipated impact of approximately 30 basis points of margin dilution from the UK Biocentre acquisition.

• Free cash flow (cash flow from operations less capital expenditures) is expected to improve approximately 10% to 15% year-over-year, consistent with prior guidance.

Azenta does not provide forward-looking guidance on a GAAP basis for the measures on which it provides forward-looking non-GAAP guidance as the Company is unable to provide a quantitative reconciliation of forward-looking non-GAAP measures to the most directly comparable forward-looking GAAP measure, without unreasonable effort, because of the inherent difficulty in accurately forecasting the occurrence and financial impact of the various adjusting items necessary for such reconciliations that have not yet occurred, are dependent on various factors, are out of the Company's control, or cannot be reasonably predicted. Such adjustments include, but are not limited to, transformation costs, restructuring charges, costs related to acquisitions and divestitures, governance-related matters, goodwill and intangible impairments, stock-based compensation, and other gains and charges that are not representative of the normal operations of the business.

Conference Call and Webcast

Azenta management will webcast its third quarter fiscal 2026 earnings conference call on August 5, 2026 at 8:30 a.m. Eastern Time. During the call, Company management will respond to questions concerning, but not limited to, the Company's financial performance, business conditions and industry outlook. Management's responses could contain information that has not been previously disclosed.

The call will be broadcast live over the Internet and, together with presentation materials and supplemental information referenced on the call, will be hosted at the Investor Relations section of Azenta's website at https://investors.azenta.com/events. The supplemental information is being posted at the time of this earnings release, and the presentation materials will be posted ahead of the earnings call. A replay of the webcast will be archived on the website for convenient on-demand access.

Regulation G – Use of Non-GAAP Financial Measures

This release includes non-GAAP financial measures, including organic revenue, adjusted gross profit and margin, adjusted operating income, expenses and margin, EBITDA, Adjusted EBITDA and Adjusted EBITDA margin, non-GAAP net income, non-GAAP diluted EPS and free cash flow. Management believes these measures give investors additional insight into the results of business operations, improve period-to-period comparability and facilitate comparison with peers. Management uses these measures to evaluate business performance and uses organic revenue (referred to as Core Revenue in the Company's proxy statement), Adjusted EBITDA and free cash flow in determining compensation under the Company's annual incentive plan. They are not presented in accordance with, and are not a substitute for, U.S. generally accepted accounting principles, or GAAP, should always be considered together with the most directly comparable GAAP measures, and may not be comparable to similarly titled measures used by other companies. These measures are presented on a continuing operations basis, except free cash flow, which is presented on a total company basis inclusive of B Medical Systems. Non-GAAP diluted EPS does not exclude stock-based compensation; the Company separately presents non-GAAP adjusted net income excluding stock-based compensation. Reconciliations to the most directly comparable GAAP measures, and descriptions of the adjustments, are included at the end of this release under "Notes on Non-GAAP Financial Measures." Certain amounts may not sum due to rounding, and all percentages are calculated using unrounded amounts.

ir@azenta.com

Maria Isabel Cuartas

Manager Investor Relations

ir@azenta.com

AZENTA, INC.

CONSOLIDATED STATEMENTS OF OPERATIONS

(unaudited)

(In thousands, except per share data)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-12-04_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

OVERVIEW

General

We are a leading global provider of biological and chemical compound sample exploration and management solutions for the life sciences industry. We entered the life sciences market in 2011, leveraging our in-house precision automation and cryogenics capabilities that we were then applying in the semiconductor manufacturing market. This led us to develop solutions for automated ultra-cold storage. Since then, we have expanded our life sciences offerings through internal investments and through a series of acquisitions. We support our customers from research and clinical development to commercialization with our sample management and automated storage systems, as well as genomic services expertise to help our customers bring impactful therapies to market faster. We understand the importance of sample integrity and offer a broad portfolio of products and services supporting customers at every stage of the life cycle of samples, including procurement, automated storage systems, genomic services and a multitude of sample consumables, informatics and data software, along with sample repository services. Our expertise, global footprint and leadership positions enable us to be a trusted global partner to pharmaceutical, biotechnology and life sciences research institutions. In total, we employ approximately 3,000 full-time employees, part-time employees and contingent workers worldwide as of September 30, 2025 and have sales in approximately 95 countries. We are headquartered in Burlington, Massachusetts and have operations in North America, Asia, and Europe.

Our portfolio includes product and service offerings developed by us internally, as well as obtained through acquisitions, designed to provide comprehensive capabilities to our customers, addressing their needs in sample exploration and management, automated storage and multiomics. We continue to develop new product and service offerings and enhance existing and acquired offerings through the expertise of our research and development resources. We believe our acquisition, investment and integration approach has allowed us to accelerate internal development and significantly accelerate time to market for our life sciences solutions.

Segments

Within our Sample Management Solutions segment, we operate as a single business unit offering end-to-end sample management products and services, including Sample Repository Services, or SRS, and Core Products (Automated Stores, Cryogenic Systems, Automated Sample Tube, Consumables and Instruments, and Controlled Rate Thawing Devices). This portfolio provides customers with a high level of sample quality, security, availability, intelligence and integrity throughout the lifecycle of samples, providing customers with complete end-to-end "cold chain of custody" capabilities. We also offer expert-level consultation services to our clients throughout their experimental design and implementation processes.

Within our Multiomics segment, our genomic services business advances research and development activities by providing gene sequencing, synthesis, and related services. We offer a comprehensive, global portfolio that we believe has broad appeal in the life sciences industry and enables customers to select the best solution for their research and development challenges. This portfolio also offers unique solutions for key markets such as CGT, antibody development and biomarker discovery by addressing genomic complexity and throughput challenges.

Business and Financial Performance

Our performance for the fiscal years ended September 30, 2025, 2024 and 2023 is as follows (in thousands):

Year Ended September 30,
2025 | 2024 | 2023
Revenue | 593,821 | 573,448 | 551,486
Cost of revenue | 323,541 | 318,826 | 312,276
Gross profit | 270,280 | 254,622 | 239,210
Operating expenses
Research and development | 30,390 | 31,524 | 32,141
Selling, general and administrative | 261,563 | 262,958 | 263,738
Impairment of goodwill and intangible assets | — | 4,658 | —
Restructuring charges | 5,171 | 6,766 | 4,577
Total operating expenses | 297,124 | 305,906 | 300,456
Operating loss | (26,844 | (51,284 | (61,246
Other income (expense)
Interest income, net | 18,779 | 32,891 | 43,541
Other income (expense), net | 922 | (732 | (2,300
Loss before income taxes | (7,143 | (19,125 | (20,005
Income tax (benefit) expense | (31,601 | 5,241 | (11,965
Income (loss) from continuing operations | 24,458 | (24,366 | (8,040
Loss from discontinued operations, net of tax | (80,221 | (140,531 | (6,596
Net loss | (55,763 | (164,897 | (14,636

Results of Operations

Fiscal Year Ended September 30, 2025 compared to Fiscal Year Ended September 30, 2024

Revenue increased 4% for fiscal year 2025 compared to fiscal year 2024 driven by increased revenue in the Sample Management Solutions and Multiomics segments. Gross margin was 45.5% for fiscal year 2025 compared to 44.4% for fiscal year 2024 primarily driven by higher revenue, operational efficiencies, favorable sales mix and improved cost management. Operating expenses decreased in fiscal year 2025 compared to the prior fiscal year, primarily driven by lower research and development expense, selling, general and administrative expense and restructuring charges, partially offset by higher transformation costs. We generated net income from continuing operations of $24.5 million for fiscal year 2025 compared to a net loss from continuing operations of $24.4 million for fiscal year 2024, primarily due to higher income tax benefit, partially offset by decreased interest income during fiscal year 2025. We generated a net loss from discontinued operations, net of tax, of $80.2 million for fiscal year 2025 compared to a net loss from discontinued operations, net of tax, of $140.5 million for fiscal year 2024, primarily driven by the estimated loss on assets held for sale recorded during fiscal year 2025 and the impairment of goodwill recorded during fiscal year 2024.

Fiscal Year Ended September 30, 2024 compared to Fiscal Year Ended September 30, 2023

Revenue increased 4% for fiscal year 2024 compared to fiscal year 2023 driven by increased revenue in the Sample Management Solutions and Multiomics segments. Gross margin was 44.4% for fiscal year 2024 compared to 43.4% for fiscal year 2023 driven by margin expansion in the Sample Management Solutions and Multiomics segments. Operating expenses increased in fiscal year 2024 compared to fiscal year 2023, primarily due to the $4.7 million non-cash impairment of intangible assets and increased restructuring costs recognized in fiscal year 2024. We generated a net loss from continuing operations of $24.4 million for fiscal year 2024 compared to a net loss from continuing operations of $8.0 million for fiscal year 2023, primarily due to the non-cash impairment of intangible assets, higher income tax expense, and decreased interest income during fiscal year 2024. We generated a net loss from discontinued operations, net of tax, of $140.5 million for fiscal year 2024 compared to a net loss from discontinued operations, net of tax, of $6.6 million for fiscal year 2023, primarily driven by the impairment of goodwill recorded during fiscal year 2024.

CRITICAL ACCOUNTING POLICIES AND ESTIMATES

The preparation of the consolidated financial statements requires us to make estimates and judgments that affect the reported amounts of assets, liabilities, revenue and expenses, and related disclosure of contingent assets and liabilities. On an ongoing basis, we evaluate our estimates, including those related to revenue, business combinations, intangible assets, goodwill and other long-lived assets, inventories, income taxes, and stock-based compensation. We base our estimates on historical experience and various other assumptions that we deem reasonable under the circumstances. We evaluate current and anticipated worldwide economic conditions, both in general and specific to the life sciences industry, that serve as a basis for making judgments about the carrying values of assets and liabilities that are not readily determinable based on information from other sources. Actual results may differ from these estimates and could have a material impact on our financial condition and results of operations.

We believe that the assumptions and estimates associated with the following critical accounting policies involve significant judgment and thus have the most significant potential impact on our consolidated financial statements.

Revenue Recognition

We generate revenue from the sale of products and services. A description of our revenue recognition policies is included in Note 2, Summary of Significant Accounting Policies in the Notes to the consolidated financial statements included in Part II, Item 8, "Financial Statements and Supplementary Data" of this Annual Report on Form 10‑K.

Although most of our sales agreements contain standard terms and conditions, certain agreements contain multiple performance obligations or non-standard terms and conditions. For customer contracts that contain more than one performance obligation, we allocate the total transaction consideration to each performance obligation based on the relative stand-alone selling price of each performance obligation within the contract. We rely on either observable standalone sales or an expected cost-plus margin approach to determine the standalone selling price of offerings, depending on the nature of the performance obligation. Performance obligations whose standalone selling price is estimated using an expected cost-plus margin approach relate to the sale of customized automated cold sample management systems and service-type warranties within the Sample Management Solutions segment.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-12-04_item1_business.md)

Item 1. Business

Overview

We are a leading global provider of biological and chemical compound sample exploration and management solutions for the life sciences industry. We entered the life sciences market in 2011, leveraging our in-house precision automation and cryogenics capabilities that we were then applying in the semiconductor manufacturing market. This led us to develop and provide solutions for automated ultra-cold storage. Since then, we have expanded our life sciences offerings through internal investments and through a series of acquisitions. We support our customers from research and clinical development to commercialization with our sample management and automated storage systems, as well as genomic services expertise to help our customers bring impactful therapies to market faster. We understand the importance of sample integrity and offer a broad portfolio of products and services supporting customers at every stage of the life cycle of samples, including procurement, automated storage systems, genomic services and a multitude of sample consumables, informatics and data software, along with sample repository services. Our expertise, global footprint, and leadership positions enable us to be a trusted global partner to pharmaceutical, biotechnology and life sciences research institutions. In total, we employ approximately 3,000 full-time employees, part-time employees and contingent workers worldwide as of September 30, 2025 and have sales in approximately 95 countries. We are headquartered in Burlington, Massachusetts and have operations in North America, Asia and Europe.

Our Company was founded in 1978 and became a leading automation provider and partner to the global semiconductor manufacturing industry. We divested the last of our semiconductor businesses in February 2022 for $2.9 billion in cash and since then operate solely as a life sciences company. On December 1, 2021, we changed our corporate name from "Brooks Automation, Inc." to "Azenta, Inc." and our common stock started to trade on the Nasdaq Global Select Market under the symbol "AZTA". During the first quarter of fiscal year 2025, we announced that we are pursuing a sale of our B Medical Systems business, a manufacturer and global distributor of medical refrigeration devices based in Luxembourg. This strategic action is intended to simplify our portfolio and allow management to focus on driving revenue growth and profitability in our core Sample Management Solutions and Multiomics segments. The B Medical Systems business has been classified as held for sale and a discontinued operation under generally accepted accounting principles in the United States, or GAAP. Both the semiconductor automation results and the B Medical Systems business results are classified as discontinued operations, and, unless otherwise noted, the description of our business in this Annual Report on Form 10-K relates solely to our continuing operations.

Our portfolio includes product and service offerings developed by us internally, as well as obtained through acquisitions, designed to provide comprehensive capabilities to our customers, addressing their needs in sample exploration and management, automated storage and multiomics. We continue to develop new product and service offerings and enhance existing and acquired offerings through the expertise of our research and development resources. We believe our acquisition, investment, and integration approach has allowed us to accelerate internal development and significantly accelerate time to market for our life sciences solutions.

For further information on our acquisitions, please refer to Note 4, Business Combinations to our consolidated financial statements included under Part II, Item 8, "Financial Statements and Supplementary Data" of this Annual Report on Form 10-K.

Life Sciences Market

Our businesses serve a broad range of end markets within the life sciences industry to help our customers advance the development of therapies to improve people's lives and cure diseases. With the advent of biologics and personalized medicine, biological samples have become critical assets to the success of drug and therapy pipelines, and the proper management and protection of these samples are important to our customers. As a result, we believe there is a sizable market opportunity for us to provide comprehensive sample management and genomic solutions.

Since the successful mapping of the full human genome at the turn of this century, the market for genomic services has grown in support of research in biologic drug development, personalized medicine, and cell and gene therapy, or CGT. Top pharmaceutical and biotechnology companies and institutions can use their in-house laboratory resources to sequence millions of genes as part of their research workflow. Many companies and institutions, however, look to outsource all or a part of their gene sequencing to independent laboratories that provide expedited results and expert consultation services. We participate in this market as a value-added laboratory services provider, offering high quality genetic testing services with fast turnaround times and expert customer support.

We have approximately 14,000 customers globally and believe we are well positioned to expand our customer base. We serve top pharmaceutical and biotechnology companies, the most advanced research hospitals performing clinical research and therapy development, as well as some of the newest and leading-edge start-ups in the biotech space. In addition, we serve academic and government institutions. We believe that the sample-based services and products businesses will continue to demonstrate a growth trajectory.

Segments

Our operating and reportable segments consist of the following:

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-12-04_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-12-04_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-12-04_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-04_2-02-results.md, 10-K_2025-12-04_item7_mdna.md, 10-K_2025-12-04_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
