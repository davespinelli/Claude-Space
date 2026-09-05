# Triage pack — EVH · Evolent Health, Inc.

_Generated 2026-09-05 00:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** EVH · **Name:** Evolent Health, Inc.
- **CIK:** 0001628908
- **SIC:** 8741 — Services-Management Services
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/EVH

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Evolent Health, Inc.
- **CIK:** 1,628,908 · **SIC:** 8741 (Services-Management Services) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 4.26 |
| mktcap | $481.6M |
| ev | $1.3B |
| ev_ebit | n/a |
| fcf | $38.8M |
| fcf_yield | 8.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -26.3% |
| net_debt | $850.8M |
| net_debt_ebit | n/a |
| cash | $115.7M |
| ltd | $966.5M |
| equity | $383.2M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.9B |
| revenue_prior | $2.6B |
| rev_growth | -26.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$410.1M |
| net_income | -$579.4M |
| cfo | $38.8M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -3.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 113,059,335 |
| shares_py | 117,508,717 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -67.8% |
| r6m | 25.3% |
| off_52w_high | -57.4% |
| adv20 | $13.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.65 |
| r_ev_ebit | 0.00 |
| r_roic | 0.04 |
| r_rev_growth | 0.01 |
| r_buyback | 0.84 |
| score | 0.31 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | True |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 402 |

**Screen rationale:** buying back stock -3.8%


## 3. Share count trend

- Shares outstanding: **113,059,335** (CY2026Q2I) vs **117,508,717** prior year (CY2025Q2I)
- Change: **-3.8%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 3 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 65,892 sh / $329,460 -> net $-329,460 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 1).

| code | rows |
|---|---|
| A | 11 |
| F | 3 |
| S | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Highlights include (dollars in thousands, except for average PMPM fees'; skipped 61 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (a2026q2exhibit991.htm)

Highlights include (dollars in thousands, except for average PMPM fees and revenue per case):

For the Three Months Ended June 30,
2026 | 2025
Financial Results:
Revenue | 652,520 | 444,328
Net loss attributable to common shareholders of Evolent Health, Inc. | (28,364) | (51,090)
Net loss margin | (4.3) | % | (11.5) | %
Adjusted EBITDA | 28,050 | 37,547
Adjusted EBITDA Margin | 4.3 | % | 8.5 | %
Average Lives on Platform/Cases by Product Type
Performance Suite | 6,715 | 6,490
Specialty Technology and Services Suite | 75,641 | 77,019
Administrative Services | 1,189 | 1,231
Cases | 12 | 13
Average Unique Members | 39,956 | 40,201
Average PMPM Fees/ Revenue per Case by Product Type
Performance Suite | 24.05 | 13.76
Specialty Technology and Services Suite | 0.34 | 0.35
Administrative Services | 13.46 | 15.13
Cases | 3,608 | 2,969

Medical Expense Ratio | 95.3 | % | 80.0 | %
Medical Expense Ratio excluding Evolent Care Partners | 95.3 | % | 84.9 | %

The rising medical costs impacting health plans continue to drive robust demand for Evolent's complex specialty care solutions.

Evolent has two partnership announcements, bringing the year-to-date total to four:

• First, we are preparing for the go live of an Oncology Performance Suite partnership with an existing advanced imaging client. The partnership will cover approximately 1.5 million lives across Medicaid and Medicare populations spread through 11 states. We currently expect this business to launch by December 2026, subject to certain regulatory approvals, and generate approximately $300 million in annualized revenue. As with other recent Performance Suite arrangements, this relationship includes Evolent's full enhanced contractual protections.

• Second, an existing Specialty Technology & Services Suite client, a regional Blues plan customer, has signed an agreement to broaden its use of our Specialty Technology & Services Suite by adding new products and extending existing solutions to additional populations. We expect these implementations to occur during the third and fourth quarters of this year and annualized revenue from this contract to be less than $5 million.

Financial Results of Evolent Health, Inc.

In our earnings releases, prepared remarks, conference calls, slide presentations and webcasts, we may use or discuss financial measures not prepared in accordance with generally accepted accounting principles ("GAAP"). Definitions of the non-GAAP financial measures as well as reconciliations of non-GAAP financial measures to the most directly comparable GAAP financial measures are presented herein. See "Non-GAAP Financial Measures" for more information.

Reported Results

Evolent Health, Inc. reported the following results in accordance with GAAP (dollars in thousands, except for per share data):

For the Three Months Ended June 30,
2026 | 2025
Revenue | 652,520 | 444,328
Cost of revenue | 571,684 | 343,943
Selling, general and administrative expenses | 68,831 | 75,209
Net loss attributable to common shareholders of Evolent Health, Inc. | (28,364) | (51,090)
Net loss margin | (4.3) | % | (11.5) | %
Loss per share attributable to common shareholders of Evolent Health, Inc.
Basic and diluted | (0.25) | (0.44)

Total cash and cash equivalents was $115.7 million as of June 30, 2026.

Adjusted Results

Evolent Health, Inc. reported the following adjusted results (dollars in thousands, except for per share data):

For the Three Months Ended June 30,
2026 | 2025
Adjusted cost of revenue | 570,989 | 342,893
Adjusted selling, general and administrative expenses | 53,481 | 63,888
Adjusted EBITDA | 28,050 | 37,547
Adjusted EBITDA margin | 4.3 | % | 8.5 | %
Adjusted income (loss) attributable to common shareholders | 2,226 | (11,013)
Adjusted income (loss) per share attributable to common shareholders:
Basic and diluted | 0.02 | (0.10)

Business Outlook

The Company does not believe it can meaningfully reconcile guidance for non-GAAP Adjusted EBITDA to net income (loss) attributable to common shareholders of Evolent Health, Inc. because the Company cannot provide guidance for the more significant reconciling items between net income (loss) attributable to common shareholders of Evolent Health, Inc. and Adjusted EBITDA without unreasonable effort. This is due to the fact that future period non-GAAP guidance includes adjustments for items not indicative of our core operations, and as a result from changes to our business due to transactions and other events. Such items may, from time to time, include change in tax receivable agreement liability, other refinancing fees, gain (loss) from equity method investees, gain (loss) on repayment/extinguishment of debt, other income (expense), gain (loss) on disposal of non-strategic assets, goodwill impairments, right-of-use asset impairments, gain (loss) on lease terminations, stock-based compensation expense, severance costs and transaction-related costs. Such adjustments may be affected by changes in ongoing assumptions, judgments, as well as nonrecurring, unusual or unanticipated charges, expenses or gains (losses) or other items that may not directly correlate to the underlying performance of our business operations. The exact amount of these adjustments is not currently determinable but may be significant.

Full Year 2026 Guidance

Incorporating its year-to-date performance, the Company is raising its 2026 revenue guidance range to $2.6 to $2.7 billion. The Company also tightening its Adjusted EBITDA range to $120 to $135 million.

Additional Outlook Information

The Company expects to deploy $25 million to $30 million in cash for capitalized software development during 2026.

Definitions

Revenue Agreements

Evolent reports the number of new revenue agreements signed for Performance Suite, Specialty Technology and Services Suite, Administrative Services and Case-based products. A new revenue agreement includes incremental revenue to the Company reflecting contracts for services to both new partner entities, corporations or health plans as well as additional sales to existing partners. New revenue agreements may include incremental services, geographic, or line of business expansions or a combination thereof. The conversion of Specialty Technology and Services Suite contracts to Performance Suite are also included in this definition. The Company does not count renewals for existing scope, growth of membership within an existing contract scope or transaction-related purchase agreements, if applicable, in this metric.

Lives on Platform and Per Member Per Month ("PMPM") Fee

Performance Suite Lives on Platform are calculated by summing monthly members covered for specialty care services for contracts not under ASO arrangements divided by the number of months in the period. Specialty Technology and Services Suite Lives on Platform are calculated by summing monthly members covered for oncology, cardiology, musculoskeletal, advanced imaging and other diagnostic specialty care services for contracts under ASO arrangements divided by the number of months in the period. Administrative Services Lives on Platform are calculated by summing monthly members covered for administrative services implementation and core performance services divided by the number of months in the period. Cases are calculated by summing the number of individuals receiving services through our surgery management and advanced care planning programs in a given period. Members covered for more than one category are counted in each category.

Performance Suite Average PMPM fee is defined as revenue pertaining to our Performance Suite during the period reported divided by Performance Suite Lives on Platform for the period divided by the number of months in the period. Specialty Technology and Services Suite Average PMPM fee is defined as revenue pertaining to the Specialty Technology and Services Suite during the period reported divided by Specialty Technology and Services Suite Lives on Platform for the period divided by the number of months in the period. Administrative Services Average PMPM fee is defined as revenue pertaining to the Administrative Services during the period reported divided by the Administrative Services Lives on Platform for the period divided by the number of months in the period. Revenue per Case is calculated by the revenue pertaining to surgery management and advanced care planning programs divided by the number of cases for a given period.

Average Unique Members are calculated by summing members covered by our Performance Suite, Specialty Technology and Services Suite and Administrative Services. In cases where partners cross between multiple solutions, we only capture members from the solution with the maximum number of members.

Management uses Lives on Platform, PMPM fees, Cases, Revenue per Case and Average Unique Members because we believe that they provide insight into the unit economics of our services. We believe that these measures are also useful to investors because they allow further insight into the period over period operational performance.

Medical Expense Ratio

Medical Expense Ratio ("MER") is a key performance indicator used by management for purposes of monitoring operating performance and is calculated as GAAP total claims incurred related to our specialty care management services solution divided by GAAP revenue related to our Performance Suite. Management believes MER is useful to investors because it provides insight into the efficiency with which medical costs are managed relative to revenue and helps identify trends in the underlying performance. For periods prior to the consummation of the sale of Evolent Care Partners ("ECP") in December 2025, we present non-GAAP MER excluding revenues from ECP because is not indicative of ongoing operations.

EVOLENT HEALTH, INC.

CONSOLIDATED STATEMENTS OF OPERATIONS AND COMPREHENSIVE INCOME (LOSS)

(unaudited, in thousands, except per share data)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-25_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

INTRODUCTION

Business Overview

We are a market leader in connecting care for people with complex conditions like cancer, cardiovascular disease, and musculoskeletal diagnoses. We work on behalf of health plans and other risk-bearing entities and payers (our customers) to support physicians and other healthcare providers (our users) in providing high quality evidence-based care to their patients. We believe adherence to evidence-based clinical pathways supports better outcomes for patients, a better experience for physicians, and lower costs for the healthcare system overall.

Specialty care represents a significant and fast-growing portion of healthcare costs in the United States, driven in part by the pace of development of new therapies and treatments. To manage these increasing costs, some health plans and other risk-bearing entities historically deployed cost containment strategies that can limit access to care and operate in narrow silos (for example, prior authorization for radiological studies being considered independently from a comprehensive chemotherapy regimen). We believe Evolent can bring an integrated approach to a patient's condition across multiple specialties, using technology to recommend our

evidence-based clinical pathways in a way that provides rapid feedback to the provider, seeks to remove barriers to care, and aligns financial incentives with the best evidence.

We were an early innovator in value-based care, founded in 2011 by members of our management team, UPMC, an integrated delivery system based in Pittsburgh, Pennsylvania, and The Advisory Board Company.

All of our revenue is recognized in the United States and substantially all of our long-lived assets are located in the United States.

Recent Events

Transactions

The Company has undertaken several transactions, some of which may impact year-to-year comparisons. The following is a discussion of certain of those transactions.

Disposal

During the third quarter, the Company entered into the ECP Purchase Agreement pursuant to which the Company agreed to sell all of the outstanding shares of capital stock of Evolent Care Partners for a purchase price of $100.0 million, subject to customary closing purchase price adjustments, and a contingent payment of up to $13.0 million, subject to the achievement of certain metrics following the closing. The Company consummated the transaction on December 5, 2025. The Company previously recorded its operations from Evolent Care Partners in its total cost of care management solution.

The Company determined that the transaction met the held for sale criteria and ceased recording amortization of provider network contract intangibles at that time. The Company received cash proceeds of $91.3 million after net working capital adjustments. The carrying value of net assets and liabilities of $76.4 million, inclusive of allocated goodwill, was disposed resulting in a gain on disposal of $14.9 million recorded in (gain) loss on disposal of non-strategic assets for the year ended December 31, 2025. The Company allocated $44.8 million of goodwill to the transaction based on the value of the transaction compared to the estimated business enterprise value on the closing date. Refer to "Part II - Item 8. Financial Statements and Supplementary Data - Note 4" for additional discussion regarding our disposal.

2031 Notes Issuance, 2025 Notes Repayment and Common Stock Repurchase

On August 18, 2025, the Company entered into a purchase agreement to sell $145.0 million aggregate principal amount of its 2031 Notes in a private placement to the Purchasers within the meaning of Rule 144A under the Securities Act. The Company granted the Purchasers an option to purchase up to an additional $21.8 million aggregate principal amount of the 2031 Notes, which the Purchasers exercised in full on August 19, 2025. The closing of the 2031 Notes occurred on August 21, 2025 and a total of $166.8 million aggregate principal amount of 2031 Notes were issued at an issue price of 100.00% of par for net proceeds of approximately $161.0 million, after deducting fees and estimated expenses. On August 21, 2025, using proceeds from the sale of the 2031 Notes plus available liquidity, the Company repurchased approximately $167.4 million aggregate principal amount of its 2025 Notes for $166.8 million in cash in note repurchases entered into concurrently with the pricing of the sale of the 2031 Notes. The Company also repurchased $40.0 million of shares of the Company's Class A common stock concurrently with the sale of the 2031 Notes in privately negotiated transactions effected with or through one of the Purchasers or its affiliate at a purchase price per share equal to the last reported sale price of the Company's Class A common stock on August 18, 2025.

Credit Agreement Activity

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

RESULTS OF OPERATIONS

Evolent Health, Inc. is a holding company and its principal asset is all of the Class A common units in Evolent Health LLC, which has owned all of our operating assets and substantially all of our business since inception. The financial results of Evolent Health LLC are consolidated in the financial statements of Evolent Health, Inc.

Key Components of our Results of Operations

Revenue

Our revenue contracts are typically multi-year arrangements with customers to provide solutions designed to lower the medical expenses of our partners and include our total cost of care management and specialty care management services solutions, provide comprehensive health plan operations and claims processing services, and also include transition or run-out services to customers.

Our performance obligation in these arrangements is to provide an integrated suite of services, including access to our platform that is customized to meet the specialized needs of our partners and providers. Generally, we will apply the series guidance to the performance obligation as we have determined that each time increment is distinct. We primarily utilize a variable fee structure for these services that typically includes a monthly payment that is calculated based on a specified per member per month rate, multiplied by the number of members that our partners are managing under a value-based care arrangement or a percentage of plan premiums.

Our arrangements may also include other variable fees related to service level agreements, shared medical savings arrangements and other performance measures. Variable consideration is estimated using the most likely amount based on our historical experience and best judgment at the time.

We also deploy our services in capitation arrangements under our specialty care management solution and total cost of care solution, which we call the "Performance Suite." Capitation arrangements under the Performance Suite may include performance-based arrangements and/or gainshare features. We occasionally use third parties to assist in satisfying our performance obligations. In order to determine whether we are the principal or agent in the arrangement, we review each third-party relationship on a contract-by- contract basis. As we integrate goods and services provided by third parties into our overall service, we control the services provided to the customer prior to its delivery. As such, we are the principal and we will recognize revenue on a gross basis. In certain cases, we act as an agent and do not control the services from third parties before it is delivered to the customer, thereby recognizing revenue on a net basis.

Due to the nature of our arrangements, certain estimates may be constrained if it is probable that a significant reversal of revenue will occur when the uncertainty is resolved. We recognize revenue from services over time using the time elapsed output method. Fixed consideration is recognized ratably over the contract term. In accordance with the series guidance, we allocate variable consideration to the period to which the fees relate.

Cost of Revenue (exclusive of depreciation and amortization)

Our cost of revenue includes direct expenses and shared resources that perform services in direct support of our partners. Costs consist primarily of claims expense, employee-related expenses (including compensation, benefits and stock-based compensation), expenses recorded as part of a Medicare shared savings program and other services, as well as other professional fees. In certain cases, our cost of revenue also includes claims and capitation payments to providers and payments for pharmaceutical treatments and other health care expenditures through performance-based arrangements.

Selling, General and Administrative Expenses

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-25_item1_business.md)

Item 1. Business

Market Opportunity

Evolent is a market leader in connecting care for people with complex conditions like cancer, cardiovascular disease, and musculoskeletal diagnoses. We work on behalf of health plans and other risk-bearing entities and payers (our customers) to support physicians and other healthcare providers (our users) in providing high quality evidence-based care to their patients. We believe adherence to evidence-based clinical pathways supports better outcomes for patients, a better experience for physicians, and lower costs for the healthcare system overall.

Specialty care represents a significant and fast-growing portion of healthcare costs in the United States, driven in part by the pace of development of new therapies and treatments. To manage these increasing costs, some health plans and other risk-bearing entities historically deployed cost containment strategies that can limit access to care and operate in narrow silos (for example, prior authorization for radiological studies being considered independently from a comprehensive chemotherapy regimen). We believe Evolent can bring an integrated approach to a patient's condition across multiple specialties, using technology to recommend our evidence-based clinical pathways in a way that provides rapid feedback to the provider, seeks to remove barriers to care, and aligns financial incentives with the best evidence.

Our Business

Our History

Evolent was founded in 2011 by members of our management team, UPMC, an integrated delivery system in Pittsburgh, Pennsylvania, and The Advisory Board Company, to enable providers to pursue a value-based business model and evolve their competitive position and market opportunity. Since that time, we have grown both organically and through acquisitions. Our acquisitions have been focused on companies with extensive experience assisting customers in managing the large and complex specialties of oncology, cardiology, radiology, musculoskeletal, physical medicine, and genetics care.

We have one operating segment and one reportable segment as our chief operating decision maker ("CODM"), who is our Chief Executive Officer, assesses the performance of our operations, develops strategy and reviews financial information on a consolidated basis for purposes of evaluating financial performance and allocating resources.

Our Solutions

The majority of our revenues derive from our primary solution, Specialty Care Management Services, however we also offer additional administrative services to our customers. From time to time, we package our solutions under various go-to-market brand names to create product differentiation. Our partners may engage us to provide one, or multiple types of solutions, depending on their specific needs.

During the third quarter, the Company entered into a Stock Purchase Agreement (the "ECP Purchase Agreement") pursuant to which the Company agreed to sell all of the outstanding shares of capital stock of Evolent Care Partners, subject to customary closing purchase price adjustments. The Company consummated the transaction on December 5, 2025. The Company previously recorded its operations from Evolent Care Partners in its total cost of care management solution.

Specialty Care Management Services Solution

The foundation for our specialty care management services solution was our acquisition in 2018 of New Century Health, a national leader in managing specialty care for Medicare members under performance-based and technology and services arrangements. Since then, we have continued to invest in the solution to broaden, deepen, and scale its capabilities. Today we focus on the oncology, cardiology, and musculoskeletal markets, supported by diagnostics like radiology and genetic testing, with the objective of helping providers and payers deliver higher quality, more affordable care. In addition, we provide comprehensive quality management for oncology and cardiology patients from diagnosis through advance care planning services as well as identifying high quality, lowest cost of care for outpatient orthopedic surgeries.

We provide a differentiated approach by (i) assembling networks of high-performance providers, (ii) designing evidence-based clinical pathways and (iii) deploying proprietary specialty care management technology.

(i) Assembling high-performance provider networks

We develop high-performance provider networks with tools, capabilities and incentives to align and support physicians and other healthcare providers. We develop and manage comprehensive specialty networks, provide physician engagement and support and identify provider financial incentive alignment. Key features include:

• Direct contracts with specialists facilitate ease of care.

• Comprehensive specialty networks include multiple downstream subspecialists.

• Incentivizes financial payment for quality and cost-efficient utilization.

• Minimizes "buy and bill" incentives through shared savings methodologies.

• Dedicated provider operations provide staff to support practices.

• Clinical response team provides clinical education on-site to practice staff.

• Dedicated central call center facilitates referrals and helps to resolve claims issues.

• Provides established system of ongoing provider education and training.

• Increases the frequency of utilization and value of advance care planning.

(ii) Designing evidence-based clinical pathways

We design high-quality evidence-based clinical pathways to drive provider behavior towards improved quality of care at a lower cost. The transparent pathway development process for our specialty care management service solution's health focal areas, oncology and cardiology, is designed to achieve the following objectives:

• Reduce unnecessary clinical variation.

• Support physician clinical decision making of evidence-based therapies.

• Increase patient engagement.

• Facilitate total cost-of-care management.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-25_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-25_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-25_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-25_item7_mdna.md, 10-K_2026-02-25_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
