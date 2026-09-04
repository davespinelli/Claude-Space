# Triage pack — RPD · Rapid7, Inc.

_Generated 2026-09-04 21:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** RPD · **Name:** Rapid7, Inc.
- **CIK:** 0001560327
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/RPD

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Rapid7, Inc.
- **CIK:** 1,560,327 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 11.47 |
| mktcap | $773.1M |
| ev | $347.5M |
| ev_ebit | 30.0x |
| fcf | $146.2M |
| fcf_yield | 18.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$425.6M |
| net_debt_ebit | -36.8x |
| cash | $425.6M |
| ltd | $0.00 |
| equity | $196.7M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $859.8M |
| revenue_prior | $844.0M |
| rev_growth | 1.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $11.6M |
| net_income | $23.4M |
| cfo | $153.8M |
| capex | $7.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 4.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 67,400,640 |
| shares_py | 64,745,948 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -46.8% |
| r6m | 62.9% |
| off_52w_high | -44.9% |
| adv20 | $26.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.88 |
| r_ev_ebit | 0.28 |
| r_roic | 0.50 |
| r_rev_growth | 0.40 |
| r_buyback | 0.22 |
| score | 0.45 |

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
| rank | 287 |

**Screen rationale:** top-quartile FCF yield 18.9%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **67,400,640** (CY2026Q2I) vs **64,745,948** prior year (CY2025Q2I)
- Change: **4.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-31** — Item 5.02 (officer / director change or comp arrangement): On August 27, Michael Burns, Benjamin Holzman, Thomas Schodorf and Reeny Sondhi notified the Board of Directors (the "Board") of Rapid7, Inc. (the "Company") of their respective decisions to resign from the Board and each committee of the Board on which they...
- **2026-06-01** — Item 5.02 (officer / director change or comp arrangement): On May 26, 2026, the Board of Directors (the "Board") of Rapid7, Inc. (the "Company") appointed Wael Mohamed as Chief Executive Officer of the Company, effective as of June 1, 2026.
- **2026-03-30** — Item 1.01 (Entry into a Material Definitive Agreement): On March 26, 2026, Rapid7, Inc. (" Company ") entered into a Nomination and Support Agreement (the " Nomination and Support Agreement ") with JANA Partners Management, LP (together with its controlled affiliates and controlled associates, " JANA ").

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 9 |
| F | 3 |
| J | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-10_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Financial Highlights'; skipped 17 forward-looking-statement block(s); 12 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (q22026rapid78-kex991.htm)

Second Quarter 2026 Financial Highlights

• Revenue: Total revenue of $210.9 million, a decrease of 1.5% year-over-year. Product revenue of $205.1 million, a decrease of 1.5% year-over-year.

• ARR: Annualized recurring revenue of $824.0 million, a decrease of 2.0% year-over-year.

• Operating Income: GAAP income from operations of $3.0 million; Non-GAAP income from operations of $28.9 million.

• Net Income: GAAP net income of $6.1 million or $0.09 per diluted share and non-GAAP net income of $33.0 million or $0.44 per diluted share.

• Cash Flow: Net cash provided by operating activities of $37.0 million and free cash flow of $31.9 million.

• Total cash, cash equivalents, and government securities of $702.6 million as of June 30, 2026.

Recent Business Highlights

• In July, Rapid7 announced general availability of Rapid7 Cyber Governance Risk and Compliance, becoming the first major security operations platform to connect GRC workflows with live Security Operations data in one platform.

• In July, Rapid7 announced a strategic distribution agreement with Mindware to scale regional availability of its managed detection and response (MDR) services and AI-powered platform.

• In July, Rapid7 unveiled key Command Platform updates, introducing "Detection as Code" capabilities via Terraform, bidirectional alert synchronization with Microsoft Defender, and intent-based Ransomware Prevention features.

• In June, Rapid7 achieved GovRAMP Authorization, expanding the availability of its AI-powered cybersecurity operations and MDR services to state, local, and educational (SLED) organizations.

• In June, Rapid7 announced its participation in Anthropic's Project Glasswing, obtaining early access to Claude Mythos Preview to support practitioner-led defensive engineering, deep code reviews, and automated vulnerability patching.

• In May, Rapid7 announced access to OpenAI's Trusted Access for Cyber (TAC) program, integrating frontier models such as GPT-5.5 into its Agentic SOC workflows to accelerate telemetry triage and reduce false-positive queue times by 25%.

• In May, Rapid7 released its Q1 Threat Landscape Report, identifying vulnerability exploitation (38%) as having officially overtaken social engineering (24%) as the leading initial access vector.

rapid7.com 1

Restructuring

During the second quarter of 2026, the Company initiated a restructuring plan to streamline its organizational structure and better align resources and investments with its Core Platform Solutions, under which approximately 12% of the Company's workforce was notified that their positions would be affected. In connection with this plan, the Company expects to incur restructuring charges of approximately $10 million to $11 million, consisting primarily of severance and related employee costs, substantially all of which are expected to be paid during the third and fourth quarters of 2026 and excluded from the Company's non-GAAP results.

Third Quarter and Full Year 2026 Guidance

Non-GAAP guidance excludes estimates for stock-based compensation expense, amortization of acquired intangible assets, amortization of debt issuance costs, and certain other items such as acquisition-related expenses, impairment of long-lived assets, restructuring expense, induced conversion expense, change in the fair value of derivative assets, non-ordinary course litigation-related expenses and discrete tax items. A reconciliation of non-GAAP guidance measures to the most comparable GAAP measures is not available on a forward-looking basis without unreasonable efforts due to the high variability, complexity and low visibility with respect to the charges excluded from these non-GAAP measures.

Rapid7 anticipates ARR, revenue, non-GAAP income from operations, non-GAAP net income per share and free cash flow to be in the following ranges:

Third Quarter 2026 | Full-Year 2026
(in millions, except per share data)
ARR | Approximately $812 million | Not provided
Year-over-year growth | (3)% | Not provided
Revenue | $208 | to | $210 | $837 | to | $841
Year-over-year growth | (5)% | to | (4)% | (3)% | to | (2)%
Non-GAAP income from operations | $34 | to | $36 | $129 | to | $133
Non-GAAP net income per share, diluted | $0.44 | to | $0.47 | $1.78 | to | $1.83
Weighted average shares used in non-GAAP earnings per share calculation, diluted | 80.1 | 79.4
Free cash flow | Not provided | Approximately $130 million

rapid7.com 2

GAAP financial measures and other metrics provide useful information about our operating results, enhance the overall understanding of past financial performance and future prospects and allow for greater transparency with respect to metrics used by our management in its financial and operational decision-making.

While our non-GAAP financial measures are an important tool for financial and operational decision-making and for evaluating our own operating results over different periods of time, you should review the reconciliation of our non-GAAP financial measures to the comparable GAAP financial measures included below, and not rely on any single financial measure to evaluate our business.

Non-GAAP Financial Measures

We disclose the following non-GAAP financial measures: non-GAAP gross profit, non-GAAP income from operations, non-GAAP net income, non-GAAP net income per share, adjusted EBITDA, free cash flow and unlevered free cash flow. We also disclose non-GAAP gross margin and non-GAAP operating margin derived from these financial measures.

We define non-GAAP gross profit, non-GAAP income from operations, non-GAAP net income and non-GAAP net income per share as the respective GAAP balances excluding the effect of stock-based compensation expense, amortization of acquired intangible assets, amortization of debt issuance costs and certain other items such as acquisition-related expenses, impairment of long-lived assets, change in the fair value of derivative assets, restructuring expense, induced conversion expense and discrete tax items. Non-GAAP net income per basic and diluted share is calculated as non-GAAP net income divided by the weighted average shares used to compute net income per share, with the number of weighted average shares decreased, when applicable, to reflect the anti-dilutive impact of the capped call transactions entered into in connection with our convertible senior notes.

We believe these non-GAAP financial measures are useful to investors in assessing our operating performance due to the following factors:

Stock-based compensation expense . We exclude stock-based compensation expense because of varying available valuation methodologies, subjective assumptions and the variety of equity instruments that can impact our expense. We believe that providing non-GAAP financial measures that exclude stock-based compensation expense allows for more meaningful comparisons between our operating results from period to period.

Amortization of acquired intangible assets. We believe that excluding the impact of amortization of acquired intangible assets allows for more meaningful comparisons between operating results from period to period as the intangible assets are valued at the time of acquisition and are amortized over several years after the acquisition.

Amortization of debt issuance costs. The expense for the amortization of debt issuance costs related to our convertible senior notes and our former revolving credit facility is a non-cash item, and we believe the exclusion of this interest expense provides a more useful comparison of our operational performance in different periods.

Acquisition-related expenses. We exclude acquisition-related expenses, including accretion expense associated with contingent consideration, as costs that are unrelated to the current operations and are neither comparable to the prior period nor predictive of future results.

Discrete tax items. We exclude certain discrete tax items such as income tax expenses or benefits that are not related to ongoing business operations in the current year and adjustments to uncertain tax position reserves as these charges are not indicative of our ongoing operating results, and they are not considered when we are forecasting our future results.

Restructuring expense. We exclude non-ordinary course restructuring expenses related to the restructuring activities because we do not believe these charges are indicative of our core operating performance and we believe the exclusion of restructuring expense provides a more useful comparison of our performance in different periods.

Adjusted EBITDA. Adjusted EBITDA is a non-GAAP measure that we define as net income (loss) before (1) interest income, (2) interest expense, (3) other (income) expense, net, (4) provision for income taxes, (5) depreciation expense, (6) amortization of intangible assets, (7) stock-based compensation expense, (8) acquisition-related expenses, and (9) restructuring expense. We believe that the use of adjusted EBITDA is useful to investors and other users of our financial statements in evaluating our operating performance because it provides them with an additional tool to compare business performance across companies and across periods.

Free Cash Flow and Unlevered Free Cash Flow. Free cash flow is a non-GAAP measure that we define as cash provided by operating activities less purchases of property and equipment and capitalization of internal-use software costs. We consider free cash flow to be a liquidity measure that provides useful information to management and investors about the amount of cash generated by the business after necessary capital expenditures. We define unlevered free cash flow as free cash flow adjusted for the after-tax cash flow impact of interest income and interest expense. We believe unlevered free cash flow provides

rapid7.com 3

investors with useful supplemental information regarding our liquidity because it provides insight into the cash generated by our business before cash interest payments on financing obligations and excluding interest received on cash and investments. Management uses unlevered free cash flow to assess our ability to invest in the business and satisfy future contractual obligations. However, given our debt obligations, non-cancelable commitments and other contractual obligations, unlevered free cash flow does not represent residual cash flow available for discretionary expenses.

We include all non-GAAP financial measures in the current year or any comparative year that will be included in the non-GAAP reconciliation during the current fiscal year annual Form 10-K. As such, not all non-GAAP financial measures listed above may be included in the current reporting period non-GAAP reconciliation in the GAAP to Non-GAAP Reconciliation section below.

Our non-GAAP financial measures may not provide information that is directly comparable to that provided by other companies in our industry, as other companies in our industry may calculate non-GAAP financial results differently, particularly related to non-recurring, unusual items. In addition, there are limitations in using non-GAAP financial measures because the non-GAAP financial measures are not prepared in accordance with GAAP, may be different from non-GAAP financial measures used by other companies and exclude expenses that may have a material impact upon our reported financial results. Further, stock-based compensation expense has been and will continue to be for the foreseeable future a significant recurring expense in our business and an important part of the compensation provided to our employees.

Other Metrics

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-19_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Rapid7 is a global cybersecurity software and service provider on a mission to create a safer digital world by making cybersecurity simpler and more accessible. For more than twenty years, Rapid7 has partnered with enterprises across the globe representing a diverse range of industries to improve the efficacy and productivity of their security operations ("SecOps"). In today's rapidly evolving IT environment, customers are encountering escalating challenges due to the widening spectrum of attackers and techniques, including the proliferation of cyberattacks leveraging AI and targeted automation. We empower security professionals to manage a modern attack surface through our trusted AI infused technology, leading-edge research, and broad, strategic expertise. Rapid7's comprehensive security solutions help our global customers unite exposure management with threat detection and response to reduce attack surfaces and eliminate threats with speed and precision.

Our Command Platform is anchored on our cloud security, security information and event management ("SIEM"), advanced detection and response, and vulnerability management offerings. Rapid7 enables the Security Operations Center ("SOC") to understand their fragmented attack surface with attacker perspective, allowing them to proactively secure their attack surface and better detect and respond to threats. Enriched by years of managed services expertise, our integrated security operations platform enables SecOps teams to move away from a reactive approach, reduce their attack surface, and enhance response efficiency with a deep contextual understanding of their environment.

In the past few years, we have observed the industry undergoing a customer-driven shift to consolidated security platforms. As part of this transition, customers are moving away from cloud security as a specialized function towards cloud security as an integrated capability for SecOps teams. We view this as a demand driver for integrated SecOps, and believe that we have an opportunity to be a leader in delivering integrated risk and threat management across on-premise, cloud, and external attack surfaces. As we have shifted our strategic focus to SecOps consolidation, we are focused on continuing to drive innovation

across our core products and capabilities to accelerate customer value and provide a frictionless and integrated cloud security experience.

As the threat landscape continues to grow in complexity, customers are demonstrating demand for integrated expertise to support them in effectively managing their security technologies. The convergence of these key trends – security consolidation, integrated cloud security, and expertise driven outcomes – are the foundation of what our customers require for the modern SOC. Our focus is to be the leading provider of integrated security operations solutions by providing exposure and threat management that leverages our ability to give customers command of their attack surface.

We market and sell our products and professional services to organizations of all sizes globally, including mid-market businesses, enterprises, non-profits, educational institutions and government agencies. Our customers span a wide variety of industries such as technology, energy, financial services, healthcare and life sciences, manufacturing, media and entertainment, retail, education, real estate, transportation, government and professional services. As of December 31, 2025, we had over 11,500 customers in 150 countries, including 36% of the Fortune 100. Our revenue was not concentrated with any individual customer and no customer represented more than 1% of our revenue for the years ended December 31, 2025, 2024 or 2023.

Our Business Model

We offer our products through a variety of delivery models to meet the needs of our diverse customer base, including:

• Cloud-based subscriptions, which provide our software capabilities to our customers through cloud access and on a subscription basis. Our Incident Command, Exposure Command, and Threat Command products are offered as cloud-based subscriptions, with an option for a one or multi-year term.

• Managed services, through which we operate our products and provide our capabilities on behalf of our customers. Our Managed Vulnerability Management, Managed Detection and Response, and Managed Application Security products are offered on a managed service basis, pursuant to one or multi-year agreements.

• Licensed on-premise software consists of term licenses. When licensed on-premise software is purchased, maintenance and support and content subscriptions, as applicable, are bundled with the license for the term period. Our Nexpose and Metasploit products are offered through term software licenses with an option for one or multi-year terms. Our maintenance and support provides our customers with telephone and web-based support and ongoing bug fixes and repairs during the term of the maintenance and support agreement, and our customers who purchase our Nexpose and Metasploit products also purchase content subscriptions, which provide them with real-time access to the latest vulnerabilities and exploits.

Additionally, we offer our products through our consolidation offerings, which unify our products and services to our customers in a single package. Our Threat Complete and Cloud Risk Complete packages are offered as cloud based subscriptions, with an option for a one or multi-year term. Our Managed Threat Complete Offering is offered on a managed service basis, generally pursuant to one or multi-year agreements.

For the years ended December 31, 2025, 2024 and 2023, recurring revenue, defined as revenue from term software licenses, content subscriptions, managed services, cloud-based subscriptions and maintenance and support, was 96%, 96%, and 95% respectively, of total revenue.

Immaterial Correction of an Error

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table presents the consolidated statement of operations data (in thousands):

Year Ended December 31,
2025 | 2024 | 2023
Revenue:
Product subscriptions | 831,325 | 808,906 | 740,168
Professional services | 28,469 | 35,101 | 37,539
Total revenue | 859,794 | 844,007 | 777,707
Cost of revenue (1) :
Product subscriptions | 230,119 | 225,547 | 203,140
Professional services | 24,921 | 25,488 | 28,906
Total cost of revenue | 255,040 | 251,035 | 232,046
Operating expenses (1) :
Research and development | 190,660 | 173,126 | 177,937
Sales and marketing | 317,665 | 298,809 | 313,661
General and administrative | 84,861 | 86,002 | 85,340
Impairment of long-lived assets | — | — | 30,784
Restructuring | — | — | 22,227
Total operating expenses | 593,186 | 557,937 | 629,949
Income (loss) from operations | 11,568 | 35,035 | (84,288)
Interest income | 23,019 | 21,063 | 10,177
Interest expense | (10,436) | (10,963) | (64,700)
Other income (expense), net | 6,030 | (3,680) | (14,522)
Income (loss) before income taxes | 30,181 | 41,455 | (153,333)
Provision (benefit) for income taxes | 6,800 | 15,929 | (518)
Net income (loss) | 23,381 | 25,526 | (152,815)

(1) Cost of revenue and operating expenses include stock-based compensation expense and depreciation and amortization expense as follows (in thousands):
Year Ended December 31,
2025 | 2024 | 2023
Stock-based compensation expense:
Cost of revenue | 9,641 | 12,208 | 11,005
Research and development | 39,357 | 37,566 | 39,183
Sales and marketing | 28,230 | 28,718 | 30,350
General and administrative | 27,107 | 29,469 | 31,098
Total stock-based compensation expense | 104,335 | 107,961 | 111,636

Year Ended December 31,
2025 | 2024 | 2023
Depreciation and amortization expense:
Cost of revenue | 36,059 | 33,140 | 31,447
Research and development | 2,734 | 3,312 | 4,217
Sales and marketing | 5,222 | 6,707 | 7,801
General and administrative | 1,421 | 1,734 | 2,474
Total depreciation and amortization expense | 45,436 | 44,893 | 45,939

The following table sets forth our consolidated statements of operations data expressed as a percentage of revenue:

Year Ended December 31,
2025 | 2024 | 2023
Revenue:
Product subscriptions | 96.7 | % | 95.8 | % | 95.2 | %
Professional services | 3.3 | 4.2 | 4.8
Total revenue | 100.0 | 100.0 | 100.0
Cost of revenue :
Product subscriptions | 26.8 | 26.7 | 26.1
Professional services | 2.9 | 3.0 | 3.7
Total cost of revenue | 29.7 | 29.7 | 29.8
Operating expenses :
Research and development | 22.2 | 20.5 | 22.9
Sales and marketing | 36.9 | 35.4 | 40.3
General and administrative | 9.9 | 10.2 | 11.0
Impairment of long-lived assets | — | — | 4.0
Restructuring | — | — | 2.9
Total operating expenses | 69.0 | 66.1 | 81.1
Income (loss) from operations | 1.3 | 4.2 | (10.9)
Interest income | 2.7 | 2.5 | 1.3
Interest expense | (1.2) | (1.3) | (8.3)
Other income (loss), net | 0.7 | (0.4) | (1.9)
Income (loss) before income taxes | 3.5 | 5.0 | (19.7)
Provision (benefit) for income taxes | 0.8 | 1.9 | (0.1)
Net income (loss) | 2.7 | % | 3.1 | % | (19.6) | %

Comparison of the Years Ended December 31, 2025 and 2024

All numbers presented below are in thousands, except for percentages.

Revenue

Year Ended December 31, | Change
2025 | 2024 | %
Revenue:
Product subscriptions | 831,325 | 808,906 | 22,419 | 2.8 | %
Professional services | 28,469 | 35,101 | (6,632) | (18.9) | %
Total revenue | 859,794 | 844,007 | 15,787 | 1.9 | %

The increase in total revenue for the year ended December 31, 2025 as compared to the same period in 2024 was primarily driven by renewals, upselling activities, and cross-selling initiatives conducted with the existing customer base, reflecting sustained expansion among existing customers. This increase in revenue was partially offset by a decline in revenue generated from new customers during the respective periods, as compared to the revenue derived from new customers in the corresponding periods of the prior year.

Cost of Revenue

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-19_item1_business.md)

Item 1. Business

Overview

Rapid7 is a global cybersecurity operations software and service provider on a mission to create a safer digital world by making cybersecurity simpler and more accessible. For twenty-five years, Rapid7 has partnered with customers across the globe representing a diverse range of industries and sizes to improve the efficacy and productivity of their security operations ("SecOps"). In today's rapidly evolving IT environment, customers are encountering escalating challenges due to the widening spectrum of attackers and techniques, including the proliferation of cyberattacks leveraging AI. We empower security professionals to manage a modern attack surface through our best-in-class AI-driven technology, leading-edge research, and broad, strategic expertise. Rapid7's comprehensive security solutions, including our market-leading managed detection and response ("MDR") services, next-gen security information and event management ("SIEM"), and exposure management help our global customers unify exposure management with threat detection and response to prioritize and reduce material risk, and eliminate threats with greater speed, precision, and consistency.

We believe that Rapid7 is poised to expand the capabilities of today's SecOps teams through our integrated, open data security operations platform which is powered by our AI enabled detection and response, automation, and exposure management capabilities. Rapid7 enables the Security Operations Center ("SOC") to understand their fragmented attack surface through an attacker's perspective, thereby allowing them to proactively reduce exposures and better detect and respond to threats. Enriched by years of industry-leading risk research and managed services expertise, our integrated AI-driven platform replaces reactive security with a preemptive, risk-aware approach that reduces attack surfaces and enables faster, more confident response through contextually rich insights and deep operational visibility.

In recent years, security leaders have increasingly prioritized consolidating fragmented point products into unified security operations platforms to improve visibility, operational efficiency, and risk outcomes. In 2022, Gartner reported that approximately 75% of organizations were pursuing security vendor consolidation as part of their SecOps strategies. This shift reflects mounting challenges associated with managing expanding attack surfaces, disconnected exposure data, escalating alert volume, and the need to continuously prioritize and respond to risk across complex environments. As a result, customers are seeking platforms that unify exposure management with threat detection and response, enabling them to identify where they are most vulnerable, anticipate how attackers may exploit those exposures, and respond with speed and precision. At the same time, customers are increasingly relying on MDR and adjacent managed services to deliver continuous expertise, higher-fidelity detection, and faster response outcomes that extend and augment internal SOC teams. In this context, organizations are prioritizing open, integrated security operations platforms that pair technology with expertise to deliver risk-aware detection and response across on-premise, cloud, identity, and external attack surfaces. We have been an active participant in advancing this shift toward consolidated SecOps by innovating across our open platform architecture, strengthening our exposure management and AI-driven SOC capabilities, and expanding our managed services portfolio. As we continue to execute on our SecOps consolidation strategy, we are advancing innovation across our core platform capabilities and managed services to accelerate customer value and deliver a frictionless, integrated security operations experience.

As the threat landscape continues to grow in complexity, customers are demonstrating demand for integrated expertise to support them in effectively managing their security technologies. The convergence of these key trends – security consolidation, AI-enabled SOC capabilities, integrated cloud security, and expertise driven outcomes – forms the foundation of what our customers require for the modern SOC. Our focus is to be the leading provider of integrated, AI-driven security solutions infused with human expertise for the modern SOC by providing risk-aware detection and response that outpaces attackers and strengthens security program maturity.

As of December 31, 2025, we had more than 11,500 global customers that rely on Rapid7 technology, services, and research to improve security outcomes and securely advance their organizations.

Revenue has increased from $535.4 million in 2021 to $859.8 million in 2025, representing a 13% compound annual growth rate.

In 2025, 2024 and 2023 recurring revenue, defined as revenue from term software licenses, content subscriptions, managed services, cloud-based subscriptions and maintenance and support, was 96%, 96% and 95%, respectively, of total revenue. We achieved net income of $23.4 million and $25.5 million in 2025 and 2024, respectively, and incurred a net loss of $152.8 million in 2023, as we continued to invest for long-term growth.

Our Platform

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-19_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-19_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-19_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-10_2-02-results.md, 10-K_2026-02-19_item7_mdna.md, 10-K_2026-02-19_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
