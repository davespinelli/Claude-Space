# Triage pack — TSSI · TSS, Inc.

_Generated 2026-09-04 19:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TSSI · **Name:** TSS, Inc.
- **CIK:** 0001320760
- **SIC:** 8742 — Services-Management Consulting Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TSSI

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** TSS, Inc.
- **CIK:** 1,320,760 · **SIC:** 8742 (Services-Management Consulting Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 8.10 |
| mktcap | $228.6M |
| ev | $172.8M |
| ev_ebit | 27.3x |
| fcf | $2.1M |
| fcf_yield | 0.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 20.4% |
| net_debt | -$55.8M |
| net_debt_ebit | -8.8x |
| cash | $67.7M |
| ltd | $11.9M |
| equity | $80.3M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $245.7M |
| revenue_prior | $148.1M |
| rev_growth | 65.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $6.3M |
| net_income | $15.1M |
| cfo | $34.9M |
| capex | $32.7M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 11.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 28,219,070 |
| shares_py | 25,364,244 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -9.9% |
| r6m | -14.7% |
| off_52w_high | -60.3% |
| adv20 | $9.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.25 |
| r_ev_ebit | 0.32 |
| r_roic | 0.88 |
| r_rev_growth | 0.96 |
| r_buyback | 0.11 |
| score | 0.51 |

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
| rank | 236 |

**Screen rationale:** high ROIC 20.4%; revenue +65.9%; net cash


## 3. Share count trend

- Shares outstanding: **28,219,070** (CY2026Q2I) vs **25,364,244** prior year (CY2025Q2I)
- Change: **11.3%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 5 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 524,649 sh / $8,294,833 -> net $-8,294,833 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 17 (open-market buys 0, sales 10).

| code | rows |
|---|---|
| A | 3 |
| F | 4 |
| S | 10 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-13_2-02-results.md)

_Extraction: started at the first release heading, 'TSS Reports Second Quarter 2026 Financial Results'; skipped 8 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - PRESS RELEASE (tssi_ex991.htm)

TSS Reports Second Quarter 2026 Financial Results

Systems Integration Revenue Increased 46% Year-Over-Year, Representing 39% of Total Revenue

~$17 Million Investment Expected to Drive Increased Systems Integration Revenue from Next Generation AI Data Center Technology

GEORGETOWN, TEXAS – Aug. 13, 2026 – TSS, Inc. (Nasdaq: TSSI), a data center services company that provides integration and related services for AI and other high-performance computing infrastructure and software, today reported results for its second quarter ended June 30, 2026, showing a continued strategic shift of its revenue base toward higher margin AI and infrastructure services.

· | Systems integration revenue grew 46% year-over-year
· | Facilities management revenue grew 84%
· | Reduction in total revenues reflects shift from lower margin procurement business to higher margin systems integration and facilities management business lines
· | The company began deploying capital for its planned $17 million investment in readiness for the next generation of AI data center technology, which is expected to convert into higher systems integration revenues beginning in the third quarter of 2026

"Systems integration revenue represented 39% of total revenues in the quarter, compared with just 22% in the prior year quarter. Over time, we expect growth in Systems Integration will continue to outpace the other segments of our business given the strong demand signals we are seeing and our proven ability to address complex technology needs," said Darryll Dewan, CEO of TSS, Inc.

Second Quarter 2026 Financial Highlights :

(All comparisons are to Second Quarter 2025)

· | Revenues of $35.1 million, down 20%, with growth in higher margin business lines

o | Procurement revenues of $18.2 million, down 45%
o | Systems Integration revenues of $13.9 million, up 46%
o | Facilities Management revenues of $2.7 million, up 84%
o | Operating lease income of $0.3 million as we began warehouse operations May 1, 2026 using our previously idle former Round Rock integration facility

· | Gross profit of $8.0 million, up 11%
· | Pre-tax income up 19% on favorable leveraging of expense structure
· | Net income of $1.4 million and Diluted EPS of $0.05, compared to net income of $1.5 million and Diluted EPS of $0.06 after full tax provision, following Q4 2025 removal of valuation allowance on deferred tax asset
· | Adjusted EBITDA of $4.5 million, up 12%, reflecting a shift in total revenues to higher margin systems integration

Year-to-Date 2026 Financial Highlights :

(All comparisons are to the First Six Months of 2025)

· | Revenues of $90.5 million, down 37%, with growth skewed towards higher margin business lines

o | Procurement revenues of $58.2 million, down 53%
o | Systems Integration revenues of $28.0 million, up 65%
o | Facilities Management revenues of $4.0 million, up 44%

· | Gross profit of $16.8 million, up 2%

o | Reflects current period $1.9 million allocation of depreciation to COGS vs $0.6 million in the prior year period

· | Pre-tax income of $4.5 million, down only 1% despite comparison to record procurement revenues in the prior year period
· | Net income of $3.7 million and Diluted EPS of $0.13 compared to net income of $4.5 million and Diluted EPS of $0.17 after full tax provision, following Q4 2025 removal of valuation allowance on deferred tax asset
· | Adjusted EBITDA of $9.8 million, up 5%, reflecting a shift in total revenues to higher margin systems integration

2026 Outlook

Dewan concluded, "Looking ahead, we expect the second half of this year to be stronger than the first half with accelerated growth in Systems Integration as we continue to see strong demand across our business. We maintain our 2026 outlook for Adjusted EBITDA to be at the upper end of our $20 million to $22 million range.

Conference Call Details

The Company will conduct a conference call at 5 p.m. Eastern time today. To participate on the conference call, please dial 888-506-0062 toll free from the U.S. or Canada. Other international callers may access the call at 1-973-528-0011. The event ID is 473873. Investors may also access a live audio webcast of this conference call and replay the call for one year following the webcast at https://www.webcaster5.com/Webcast/Page/2294/54255.

About Non-GAAP Financial Measures

Adjusted EBITDA is a supplemental financial measure not defined under Generally Accepted Accounting Principles (GAAP). We define Adjusted EBITDA as net income (loss) before net interest expense and bank factoring costs, income taxes, depreciation and amortization, impairment loss on goodwill and other intangibles, stock-based compensation, and certain extraordinary items. We present Adjusted EBITDA because we believe this supplemental measure of operating performance is helpful in comparing our operating results across reporting periods on a consistent basis by excluding items that may or could have a disproportionately positive or negative impact on our results of operations in any particular period. We also use Adjusted EBITDA as a factor in evaluating the performance of certain management personnel when determining incentive compensation.

Adjusted EBITDA may not be comparable to similarly titled measures reported by other companies. Adjusted EBITDA, while providing useful information, should not be considered in isolation or as an alternative to net income or cash flows as determined under GAAP. Consistent with Regulation G under the U.S. federal securities laws, Adjusted EBITDA has been reconciled to the nearest GAAP measure; this reconciliation is located under the heading "Adjusted EBITDA Reconciliation" following the Consolidated Statements of Operations included in this press release. The Company is unable to provide a reconciliation of forward-looking Adjusted EBITDA to GAAP net income because certain reconciling items are outside the Company's control or cannot be reasonably predicted without unreasonable efforts. These items may include stock-based compensation expense, fluctuations in prevailing interest rates and the resulting impacts on bank factoring fees, interest expense and interest income, and other adjustments that may be material.

About TSS, Inc.

TSS specializes in simplifying the complex. The TSS mission is to streamline the integration and deployment of high-performance computing infrastructure and software, ensuring that end users quickly receive and efficiently utilize the necessary technology. Known for flexibility, the company builds, integrates, and deploys custom, high-volume solutions that empower data centers and catalyze the digital transformation of generative AI and other leading-edge technologies essential for modern computing, data, and business needs. TSS' reputation is built on passion and experience, quality, and fast time to value. As trusted partners of the world's leading data center technology providers, the company manages and deploys billions of dollars in technology each year. For more information, visit www.tssiusa.com.

TSS, Inc.

Consolidated Statements of Operations

(Unaudited, In thousands except per-share values)

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Revenues
Procurement | 18,249 | 33,002 | 58,229 | 123,179
Facilities management | 2,723 | 1,482 | 4,013 | 2,780
System integration | 13,880 | 9,486 | 27,956 | 16,970
Operating lease income | 289 | - | 289 | -
Total revenues | 35,141 | 43,970 | 90,487 | 142,929
Cost of revenues
Cost of revenues | 25,908 | 36,155 | 71,512 | 125,904
Cost of revenues - depreciation | 989 | 618 | 1,925 | 618
Cost of lease operations | 235 | - | 235 | -
Total cost of revenues | 27,132 | 36,773 | 73,672 | 126,522
Gross Profit | 8,009 | 7,197 | 16,815 | 16,407
Operating Expenses:
Selling, general and administrative | 5,560 | 4,735 | 11,082 | 9,622
Depreciation and amortization | 320 | 226 | 626 | 436
Bank factoring fees | 510 | 859 | 1,214 | 2,327
Loss on sale or disposal of assets | 17 | - | 17 | -
Total operating expenses | 6,407 | 5,820 | 12,939 | 12,385
Income from operations | 1,602 | 1,377 | 3,876 | 4,022
Interest expense | 322 | - | 655 | -
Interest income | (565 | (175 | (1,290 | (558
Other expense (income) | - | - | (1 | -
Pre-tax income | 1,845 | 1,552 | 4,512 | 4,580
Income tax expense | 413 | 69 | 804 | 118
Net income | 1,432 | 1,483 | 3,708 | 4,462
Earnings per common share - Basic | 0.05 | 0.06 | 0.13 | 0.19
Earnings per common share - Diluted | 0.05 | 0.06 | 0.13 | 0.17

TSS, Inc.

Adjusted EBITDA Reconciliation (GAAP to non-GAAP)

(Unaudited, In thousands)

Three Months Ended June 30, | Six Month Ended June 30,
2026 | 2025 | 2026 | 2025
Net income | 1,432 | 1,483 | 3,708 | 4,462
Interest expense | 322 | - | 655 | -
Bank factoring fees | 510 | 859 | 1,214 | 2,327
Interest income | (565 | (175 | (1,290 | (558
Depreciation and amortization | 1,309 | 844 | 2,551 | 1,054
Income tax expense | 413 | 69 | 804 | 118
EBITDA | 3,421 | 3,080 | 7,642 | 7,403
Stock based compensation | 1,049 | 930 | 2,099 | 1,851
Loss on sale or disposal of assets | 17 | -- | 17 | -
Adjusted EBITDA | 4,487 | 4,010 | 9,758 | 9,254

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-18_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

TSS, Inc. ("TSS", the "Company", "we", "us" or "our") provides a comprehensive suite of services for the integration of complex Artificial Intelligence (AI) technologies, planning, design, deployment, maintenance and refresh of end-user and enterprise systems, including the mission-critical facilities in which they are housed. We provide a single source solution for enabling technologies in data centers, operations centers, network facilities, server rooms, security operations centers, communications facilities and the infrastructure systems that are critical to their function. Our services consist of technology consulting, design and engineering, project management, systems integration, systems installation, facilities management and IT procurement services. Beginning in 2024, our systems integration services have been enhanced to include integration of AI enabled data center server racks. TSS was incorporated in Delaware in December 2004.

We deliver complex solutions to a broad range of enterprise customers who utilize our services to deploy solutions in their own data centers, in modular data centers (MDCs), in colocation facilities or at the edge of the network. This market remains highly competitive and is subject to constant evolution as new computing technologies or applications drive continued demand for more advanced computing and storage capacity. In recent years, these enterprises have shifted their investment priorities towards AI and accelerated computing infrastructure initiatives. Enterprise and data center operators are facing immense pressure to rapidly integrate and deploy the latest generative, inferencing and agentic AI equipment and GPUs (Graphics Processing Units) and will need to adapt these next-generation servers and custom rack-scale architectures to quickly and successfully compete in the market. Ensuring adequate power and thermal management systems are implemented to support these new technologies while meeting increasingly stringent sustainability requirements is critical to a successful deployment. TSS exists to assist these operators in achieving these benefits over the life cycle of their IT investments.

Over the last ten years, we have optimized our business by providing world-class integration services to our customer base. As computing technologies evolve and as we see new power and cooling technologies emerge, including direct liquid-cooled IT solutions and the rapid adoption of AI computing solutions, we will continue to adapt our systems integration business and capabilities to support these new products. We will also continue to offer expanded services to enable the integration, deployment, support, and maintenance of these new IT solutions. We compete in expanding market segments, often against larger competitors who have extensive resources. We rely on several large relationships and one US-based OEM (original equipment manufacturer) strategic customer to win contracts and to provide business to us under a Master Relationship Agreement. A material decline in volume from, or loss of this OEM customer would have a material effect on our results. Our operational focus is to ensure this does not occur.

Most of the components used in our systems integration business are consigned to us by our largest OEM customer or its end-user customers. Thus, our revenues reflect only the services we provide, and the consigned components are not reflected in our statement of operations or on our balance sheet. We also offer procurement services whereby we procure third-party hardware, software and services on their behalf. Our configuration and integration services businesses often integrate these components to deliver a complete system to our customers.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

In this section, we discuss the results of our operations for the year ended December 31, 2025 (the "current year" or "2025") compared to the year ended December 31, 2024 (the "prior year" or "2024"). For a discussion of the year ended December 31, 2024 compared to the year ended December 31, 2023, please refer to Part II, Item 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations" in our Annual Report on Form 10-K for the year ended December 31, 2024.

Revenue

Revenues consist of fees earned from the planning, design and project management for mission-critical facilities and information infrastructures, as well as fees earned from providing maintenance services for these facilities. We also earn revenues from providing system configuration and integration services, as well as procurement services, to IT equipment vendors. We began integration services on AI racks in June 2024 and have continued that activity to date. Currently we derive substantially all our revenue from the U.S. market.

We contract with our customers with various contract types: service and maintenance, time and material, and guaranteed maximum price contracts, all of which are fixed-price exclusive of time and material contracts. Guaranteed maximum price contracts are typically lower risk arrangements and thus yield lower profit margins than time-and-materials arrangements which generally generate higher profit margins, relative to their higher risk. Certain of our service and maintenance contracts provide comprehensive coverage of all the customers' equipment (excluding IT equipment) at a facility during the contract period.

Most of our revenue is generated based on services provided either by our employees or subcontractors. To a lesser degree, the revenue we earn includes reimbursable travel and other costs to support the project. Since we earn higher profits from the labor services that our employees provide compared with use of subcontracted labor and other reimbursable costs, we seek to optimize our labor content on the contracts we are awarded to maximize our profitability. Occasionally, our revenues will reflect certain reimbursements received from customers for expanding our capacity, typically through capital expenditures, or for adding headcount to support specific customer requests. In 2024, we invested approximately $1.7 million in our Round Rock facility to expand our capacity to integrate generative AI-enabled server racks, including both air-cooled and direct-liquid cooled systems. One of our customers reimbursed us for the majority of those investments. Prior to December 2025, we were amortizing that reimbursement into service integration revenues over the expected useful life of three years; the same period over which we were depreciating the related fixed assets. As the production of AI racks has now fully moved to our Georgetown facility and we no longer expect to utilize the assets installed in our Round Rock facility, we accelerated the revenue recognition and depreciation of those assets in the fourth quarter of 2025. The acceleration of recognition of the reimbursement amounted to approximately $0.8 million which is included in the 2025 systems integration revenues; the acceleration of depreciation of these assets amounted to $0.7 million, and is reported on the face of our income statement as "loss on sale or disposal of assets." Our Round Rock facility is currently idle, as we seek additional business to utilize the space or to sublease the space if not used in our operations.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-18_item1_business.md)

PART I.

Item 1. Business

Company Overview

TSS, Inc. ("TSS", the "Company", "we", "us" or "our") provides a comprehensive suite of services for the integration of complex Artificial Intelligence (AI) technologies, planning, design, deployment, maintenance and refresh of end-user and enterprise systems, including the mission-critical facilities in which they are housed. We provide a single source solution for enabling technologies in data centers, operations centers, network facilities, server rooms, security operations centers, communications facilities and the infrastructure systems that are critical to their function. Our services consist of technology consulting, design and engineering, project management, systems integration, systems installation, facilities management and IT procurement services. Beginning in 2024, our systems integration services have been enhanced to include integration of AI enabled data center server racks. TSS was incorporated in Delaware in December 2004. In the second quarter of 2025 we relocated our corporate offices and primary integration facility from Round Rock, Texas to Georgetown, Texas and continued to operate a secondary integration facility in our Round Rock facility for approximately one additional quarter before all operations were migrated to our new facility in Georgetown.

We deliver complex solutions to a broad range of enterprise customers who utilize our services to deploy solutions in their own data centers, in modular data centers (MDCs), in colocation facilities or at the edge of the network. This market remains highly competitive and is subject to constant evolution as new computing technologies or applications drive continued demand for more advanced computing and storage capacity. In recent years, these enterprises have shifted their investment priorities towards AI and accelerated computing infrastructure initiatives. Enterprise and data center operators are facing immense pressure to rapidly integrate and deploy the latest generative, inferencing and agentic AI equipment and GPUs (Graphics Processing Units) and will need to adapt these next-generation servers and custom rack-scale architectures to quickly and successfully compete in the market. Ensuring adequate power and thermal management systems are implemented to support these new technologies while meeting increasingly stringent sustainability requirements is critical to a successful deployment. TSS exists to assist these operators in achieving these benefits over the life cycle of their IT investments.

Over the last ten years, we have optimized our business by providing world-class integration services to our customer base. As computing technologies evolve and as we see new power and cooling technologies emerge, including direct liquid-cooled IT solutions and the rapid adoption of AI computing solutions, we will continue to adapt our systems integration business and capabilities to support these new products. We will also continue to offer expanded services to enable the integration, deployment, support, and maintenance of these new IT solutions. We compete in expanding market segments, often against larger competitors who have extensive resources. We rely on several large relationships and one US-based OEM (original equipment manufacturer) strategic customer to win contracts and to provide business to us under a Master Relationship Agreement. A material decline in volume from, or loss of this OEM customer would have a material effect on our results. Our operational focus is to ensure this does not occur.

Most of the components used in our systems integration business are consigned to us by our largest OEM customer or its end-user customers. Thus, our revenues reflect only the services we provide, and the consigned components are not reflected in our statement of operations or on our balance sheet. We also offer procurement services whereby we procure third-party hardware, software and services on their behalf. Our configuration and integration services businesses often integrate these components to deliver a complete system to our customers.

In some cases, in the performance of procurement services, we also act as an agent and arrange for the purchase of third-party hardware, software or services that are to be provided to our customers by another party but have no control of the goods or services before they are transferred to the customer. In these instances, we are acting as an agent in the transaction. These procurement services allow us to develop relationships with new hardware, software and professional service providers and allow us to generate higher profits on integration projects by broadening our revenue and customer base.

Recent Developments

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-18_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-18_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-18_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-13_2-02-results.md, 10-K_2026-03-18_item7_mdna.md, 10-K_2026-03-18_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
