# Triage pack — WYY · WIDEPOINT CORP

_Generated 2026-09-05 00:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** WYY · **Name:** WIDEPOINT CORP
- **CIK:** 0001034760
- **SIC:** 7373 — Services-Computer Integrated Systems Design
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/WYY

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** WIDEPOINT CORP
- **CIK:** 1,034,760 · **SIC:** 7373 (Services-Computer Integrated Systems Design) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 11.39 |
| mktcap | $113.9M |
| ev | $103.9M |
| ev_ebit | n/a |
| fcf | $5.5M |
| fcf_yield | 4.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -132.6% |
| net_debt | -$10.0M |
| net_debt_ebit | n/a |
| cash | $10.0M |
| ltd | $0.00 |
| equity | $11.7M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $150.5M |
| revenue_prior | $142.6M |
| rev_growth | 5.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$2.8M |
| net_income | -$2.8M |
| cfo | $5.7M |
| capex | $237k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 9,998,255 |
| shares_py | 9,776,906 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 115.1% |
| r6m | 143.9% |
| off_52w_high | -43.6% |
| adv20 | $1.2M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.48 |
| r_ev_ebit | 0.00 |
| r_roic | 0.00 |
| r_rev_growth | 0.54 |
| r_buyback | 0.31 |
| score | 0.32 |

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
| rank | 395 |

**Screen rationale:** debt data missing (net cash unverified); 12-1 momentum 115.1%


## 3. Share count trend

- Shares outstanding: **9,998,255** (CY2026Q2I) vs **9,776,906** prior year (CY2025Q2I)
- Change: **2.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-13** — Item 5.02 (officer / director change or comp arrangement): On August 7, 2026, Jason Holloway tendered his resignation as Executive Vice President and Chief Revenue Officer of WidePoint Corporation (the "Company") effective December 31, 2026.
- **2026-06-25** — Item 1.01 (Entry into a Material Definitive Agreement): On June 24, 2026,WidePoint Corporation (NYSE American: WYY), a leading provider of Secure Mobility Management solutions, was selected as the single awardee of the Department of Homeland Security's (DHS) Cellular Wireless Managed Services (CWMS) 3.0 contract...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 429,934 sh / $7,257,330 -> net $-7,257,330 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 21 (open-market buys 0, sales 17).

| code | rows |
|---|---|
| A | 2 |
| F | 2 |
| S | 17 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-17_2-02-results.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit._

## EX-99.1 - TRANSCRIPT OF EARNINGS CALL (wyy_ex991.htm)

EX-99.1
wyy_ex991.htm
TRANSCRIPT OF EARNINGS CALL

wyy_ex991.htm
EXHIBIT 99.1

## EX-99.2 - PRESS RELEASE (wyy_ex992.htm)

EX-99.2
wyy_ex992.htm
PRESS RELEASE

wyy_ex992.htm
EXHIBIT 99.2

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-25_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS

This discussion should be read in conjunction with the other sections of this Form 10-K, including "Risk Factors," and the Financial Statements and notes thereto. The various sections of this discussion contain a number of forward-looking statements, all of which are based on our current expectations and could be affected by the uncertainties and risk factors described throughout this Annual Report on Form 10-K. See "Cautionary Note Regarding Forward Looking Statements and Risk Factor Summary." Our actual results may differ materially.

Organizational Overview

We are a leading provider of Technology Management as a Service (TMaaS) that consists of federally certified communications management, identity management, and interactive bill presentment and unified communication analytics solutions and IT as a Service (ITaaS). We help our clients achieve their organizational missions for mobility management and security objectives in this challenging and complex business environment.

We offer our TMaaS solutions through a flexible "As-a-Service" model or "Xaas" which includes both a scalable and comprehensive set of functional capabilities that can be used by any customer to meet the most common functional, technical and security requirements for mobility management. Our TMaaS solutions were designed and implemented with flexibility in mind such that it can accommodate a large variety of customer requirements through simple configuration settings rather than through costly software development. The flexibility of our TMaaS solutions enables our customers to be able to quickly expand or contract their mobility management requirements. Our TMaaS solutions are hosted and accessible on-demand through a secure federal government certified proprietary portal that provides our customers with the ability to manage, analyze and protect their valuable communications assets, and deploy identity management solutions that provide secured virtual and physical access to restricted environments.

Strategy

During 2025, we focused on increasing our customer base and our sales pipeline and leveraging our strategic relationships with key system integrators and strategic partners to capture additional market share. On February 19, 2025 WidePoint's Intelligent Technology Management System (ITMS) achieved FedRAMP Authorized status from the Federal Risk and Authorization Management Program (FedRAMP) Program Management Office (PMO). In fiscal 2026, we will continue to focus on the following key goals:

· | Winning the DHS CWHS 3.0 re-compete,
· | Continue to find additional avenues for capturing new sales opportunities,
· | Continue to provide unmatched level of services to our current customer base,
· | Leverage our FedRAMP Authorized status as a differentiator from our competitors in pursuing government business,
· | Grow our recurring managed services revenues,
· | Add incremental capabilities to our Technology Management solution set and develop and possibly acquire new high margin business lines,
· | Leverage our software platforms to grow our SaaS revenues and take advantage of the opportunities emerging from the growth in remote working,
· | Expand our commercial customer base organically,
· | Continue to leverage the R2v3 Certification,
· | Execute cross-sell opportunities identified from ITA acquisition, including Identity Management (IdM), Telecommunications Lifecycle Management (TLM) and Digital Billing & Analytics (DB&A) solution,
· | Growing our sales pipeline by continuing to invest in our business development and sales team assets,
· | Pursuing additional opportunities with our key systems integrator and strategic partners,
· | Expanding our solution offerings into the commercial space, and

· | Explore integration of artificial intelligence into our solution to provide better information security, and improve service delivery while reducing response time and cost.
· | Our strategy for achieving our longer-term goals include:
· | Establishing a market leadership position in the trusted mobility management (TM2) sector,
· | pursuing strategic acquisitions to expand our solutions and our customer base,
· | delivering new incremental offerings to add to our existing TM2 offering,
· | creating and testing innovative new offerings that enhance our TM2 offering, and
· | transitioning our data center and support infrastructure into a more cost-effective and federally approved cloud environment to comply with perceived future contract requirements.

We believe these actions could drive a strategic repositioning to our TM2 offering and could include the sale of non-aligned offerings coupled with acquisitions of complementary and supplementary offerings that could result in a more focused core set of TM2 offerings.

Critical Accounting Policies and Estimates

Refer to Note 2 to the consolidated financial statements for a summary of our significant accounting policies referenced, as applicable, to other notes. In many cases, the accounting treatment of a particular transaction is specifically dictated by U.S. GAAP and does not require management's judgment in its application. Our senior management has reviewed these critical accounting policies and estimates and related disclosures with its Audit Committee. See Note 2 to consolidated financial statements, which contain additional information regarding accounting policies and other disclosures required by U.S. GAAP. The following section below provides information about certain critical accounting policies and estimates that are important to the consolidated financial statements and that require significant management assumptions and judgments.

Segments

Segments are defined by authoritative guidance as components of a company in which separate financial information is available and is evaluated by the chief operating decision maker (CODM), or a decision-making group, in deciding how to allocate resources and in assessing performance. Our CODM is our chief executive officer.

We operate in one segment based on the consolidated information used by our CODM in evaluating the financial performance of our business and allocation resources. This single segment represents our Company's business, which is providing managed services for government and commercial clients under the umbrella of Technology Management as a Service (TMaaS), that includes Identity Management (IdM), secure Mobility Managed Services (MMS), Telecom Lifecycle Management, Digital Billing & Analytics and IT as a service (ITaaS).

We present a single segment for purposes of financial reporting and prepared consolidated financial statements upon that basis.

Revenue Recognition

Our managed services solutions may require a combination of labor, third party products and services. Our managed services are generally not interdependent and our contract performance obligations are delivered consistently on a monthly basis. In the event there are undelivered performance obligations our practice is to recognize the revenue when the performance obligation has been satisfied.

A substantial portion of our revenues are derived from firm fixed price contracts with the U.S. federal government that are fixed fee arrangements tied to the number of devices managed. Our actual reported revenue may fluctuate quarter to quarter depending on the hours worked, number of users, number of devices managed, actual or prospective proven expense savings, actual technology spend, or any other metrics as contractually agreed to with our customers.

Our revenue recognition policies for our managed services are summarized and shown below:

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-25_item1_business.md)

ITEM 1. BUSINESS

Company Overview

We are a leading provider of Technology Management as a Service (TMaaS) that consists of federally certified communications management, and identity management. We also provide interactive bill presentment and analytics, and Information Technology as a Service Solutions (ITaaS). We help our clients achieve their organizational missions for mobility management, information technology management, and cybersecurity objectives in this challenging and complex business environment.

We offer our TMaaS solutions through a flexible "As-a-Service" model or XaaS which includes both a scalable and comprehensive set of functional capabilities that can be used by any customer to meet the most common functional, technical and security requirements for mobility management. Our TMaaS solutions were designed and implemented with flexibility in mind such that it can accommodate a large variety of customer requirements through simple configuration settings rather than through costly software development. The flexibility of our TMaaS solutions enables our customers to be able to quickly expand or contract their mobility management requirements. Our TMaaS solutions are hosted and accessible on-demand through both a secure federal government certified proprietary portal and/or through a secure enterprise portal that provides our customers with the ability to manage, analyze and protect their valuable communications assets, and deploy identity management solutions that provide secured virtual and physical access to restricted environments.

Our Managed Services

Our TMaaS framework combines the strengths of our core capabilities into a single secure comprehensive enterprise-wide solution set that offers our customer's the ability to securely enable and manage their mobile IT and telecommunication assets as described below:

Telecom Lifecycle Management

We offer comprehensive telecom lifecycle management solutions to enterprises both in the public and the private sectors. Our solutions are delivered in a hosted and secure multi-modal delivery environment. Our solutions provide full visibility of telecom assets for our clients thereby enabling our clients to securely and efficiently manage all aspects of telecom assets, while reducing the overall cost of ownership. We offer state-of-the-art call centers that are available 24/7 to help our customers stay productive.

Mobile and Identity Management

As one of two Department of Defense (DoD) designated External Certificate Authorities (ECA), we offer several different federally certified digital certificates and credentials that enable our customers to provide strong multifactor authentication (MFA) solution to conduct business through secure portals owned and managed by the U.S. federal government, access government facilities and secure mobile devices that are used to access corporate networks, databases and other IT assets. We also offer comprehensive mobile security solutions that protect users, devices, and corporate resources, including establishing effective policies to create a scalable, adaptable, successful mobile program. We also offer the same MFA solution to enterprises in the private sectors with the same level of cybersecurity assurance.

Digital Billing and Unified Communications Analytics Solutions

We offer innovative and interactive billing communications and analytics solutions to large communications service providers (CSPs). Our customized solutions give their end customers the ability to view and analyze their bills online via our advanced self-serve user portal 24/7.Our solutions are delivered in a hosted and secure environment and provide our CSPs with full visibility into their revenue model which provides stronger customer experience and reduces their operating costs and improves profitability.

IT as a Service

We provide comprehensive information technology (IT) as a service offerings (ITaaS), including cybersecurity, cloud services, network operations, and professional services. We provide a complete outsourcing solution that includes hardware, software, network, cybersecurity, and associated management for our clients' IT needs. Additionally, we provide development operations support, artificial intelligence implementation, and the Microsoft stack of technologies to help our customers to be productive, agile, and efficient in a secure environment. We provide the above solutions from the cloud that ensures scalability, resiliency, and security. We also provide "migration to the cloud" services that enables our customers to take advantage of cost savings through economies of scale and elimination of redundancy as well as taking advantage of built in scalability and resiliency of the cloud.

Our Carrier Services

We also provide our customers with carrier services, which consists of phone, data and satellite and related mobile services for a connected device or end point. We procure, process and pay communications carrier invoices on behalf of customers. Under many of our carrier services arrangements, we recognize revenues and related costs on a gross basis. A significant portion of our overall reported revenue consists of revenue from carrier services; however, it represents an insignificant portion of our overall reported gross profit. This is a commodity type service and margins are nominal, but this is a necessary service to deliver to federal government customers that engage us to provide a full-service solution as part of our platform. We support the consolidation, validation, and administration of telecom charges across multiple carriers and vendors, allowing customers to simplify billing and related payment processes without assuming direct responsibility for carrier relationships.

Sales Cycle

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-17_2-02-results.md, 10-K_2026-03-25_item7_mdna.md, 10-K_2026-03-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
