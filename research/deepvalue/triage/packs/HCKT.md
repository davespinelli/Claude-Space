# Triage pack — HCKT · HACKETT GROUP, INC.

_Generated 2026-09-04 14:13 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** HCKT · **Name:** HACKETT GROUP, INC.
- **CIK:** 0001057379
- **SIC:** 8742 — Services-Management Consulting Services
- **Fiscal year end (MM-DD):** 12-26
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/HCKT

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** HACKETT GROUP, INC.
- **CIK:** 1,057,379 · **SIC:** 8742 (Services-Management Consulting Services) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 11.08 |
| mktcap | $275.6M |
| ev | $342.3M |
| ev_ebit | 14.5x |
| fcf | $32.4M |
| fcf_yield | 11.8% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 13.8% |
| net_debt | $66.7M |
| net_debt_ebit | 2.8x |
| cash | $14.2M |
| ltd | $80.9M |
| equity | $68.2M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $305.6M |
| revenue_prior | $313.9M |
| rev_growth | -2.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $23.5M |
| net_income | $12.9M |
| cfo | $40.3M |
| capex | $7.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -9.6% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 24,877,873 |
| shares_py | 27,510,689 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -41.6% |
| r6m | -21.1% |
| off_52w_high | -46.2% |
| adv20 | $2.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.76 |
| r_ev_ebit | 0.60 |
| r_roic | 0.79 |
| r_rev_growth | 0.25 |
| r_buyback | 0.94 |
| score | 0.67 |

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
| rank | 84 |

**Screen rationale:** top-quartile FCF yield 11.8%; high ROIC 13.8%; buying back stock -9.6%


## 3. Share count trend

- Shares outstanding: **24,877,873** (CY2026Q2I) vs **27,510,689** prior year (CY2025Q2I)
- Change: **-9.6%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-04** — Item 1.01 (Entry into a Material Definitive Agreement): On August 3, 2026, The Hackett Group, Inc. (the "Company") entered into a Fourth Amended and Restated Credit Agreement (the "Credit Agreement") with Bank of America, N.A., as administrative agent, and the lenders party thereto, pursuant to which the lenders...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 22 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 13 |
| D | 3 |
| F | 4 |
| M | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-05_2-02-results.md)

_Extraction: started at the first release heading, 'Financial Highlights'; skipped 8 forward-looking-statement block(s); 8 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (hckt-ex99_1.htm)

Financial Highlights

▪
Total revenue in the first quarter of 2026 was $68.8 million and revenue before reimbursements was $67.8 million. This compares to total revenue of $77.9 million and revenue before reimbursements of $76.2 million in the first quarter of the prior year.

▪
GAAP diluted earnings per share was $0.17 in the first quarter of 2026, as compared to $0.11 in the first quarter of 2025.

▪
Adjusted diluted earnings per share, a non-GAAP measure, for the first quarter of 2026 was $0.34, which was at the low end of our guidance, as compared to $0.41 in the first quarter of 2025. Adjusted financial information is provided to enhance the understanding of the Company's financial performance and is reconciled to the Company's GAAP information in the accompanying tables.

▪
As of March 27, 2026, the Company's cash balances were $6.1 million, with $79.0 million outstanding on the Company's credit facility. Cash flows utilized by operations were $5.1 million in the first quarter of 2026, as compared to cash flows from operations of $4.2 million in the first quarter of 2025. As of March 27, 2026, the Company had $22.0 million available under its share repurchase plan.

▪
Subsequent to the end of the first quarter, the Company's Board of Directors declared the second quarterly dividend of $0.12 per share for its shareholders of record on June 22, 2026, to be paid on July 6, 2026.

Business Outlook for the Second Quarter of 2026

Based on the Company's current outlook:

▪
The Company estimates total revenue before reimbursements for the second quarter of 2026 will be in the range of $68.5 million to $70.0 million.

▪
The Company estimates adjusted diluted earnings per share for the second quarter of 2026 to be in the range of $0.33 and $0.35, assuming a GAAP effective tax rate of 26.6%.

Conference Call and Webcast Details

▪
On Tuesday, May 5, 2026, senior management will discuss first quarter results in a conference call at 5:00 P.M. ET. The number for the conference call is (800) 593-0486, [Passcode: First Quarter]. For International callers, please dial (517) 308-9371. Please dial in at least 5-10 minutes prior to start time. If you are unable to participate on the conference call, a rebroadcast will be available beginning at 8:00 P.M. ET on Tuesday, May 5, 2026 and will run through 5:00 P.M. ET on Tuesday, May 19, 2026. To access the rebroadcast, please dial (800) 835-8067. For International callers, please dial (203) 369-3354.

▪
In addition, The Hackett Group ® will also be webcasting this conference call live. To participate, simply visit https://www.thehackettgroup.com approximately 10 minutes prior to the start of the call and click on the conference call link provided. An online replay of the call will be available after 8:00 P.M. ET on Tuesday, May 5, 2026 and will run through 5:00 P.M. ET on Tuesday, May 19, 2026. To access the replay, visit www.thehackettgroup.com.

Use of Non-GAAP Financial Measures

The Company provides adjusted earnings results (which excludes non-cash stock based compensation expense, stock price award program compensation expense, acquisition-related cash and non-cash stock based compensation expense, amortization expense, acquisition related costs and any one-time costs and includes a GAAP tax rate) as a complement to results provided in accordance with Generally Accepted Accounting Principles (GAAP). These non-GAAP results are provided to enhance the users' overall understanding of the Company's current financial performance and its prospects for the future. The Company believes the non-GAAP results provide useful information to both management and investors and by excluding certain expenses that it believes are not indicative of its core operating results. The non-GAAP measures are included to provide investors and management with an alternative method for assessing operating results in a manner that is focused on the performance of its ongoing primary operations and to provide a consistent basis for comparison between quarters. Further, these non-GAAP results are one of the primary indicators management uses for planning and forecasting. The presentation of this additional non-GAAP information should be considered in addition to, and not as a substitute for or superior to, any results prepared in accordance with GAAP. See the reconciliation of actual results titled "Reconciliation of GAAP to Non-GAAP Measures" in the accompanying tables.

The Company believes that the presentation of non-GAAP financial information on a forward-looking basis, including the guidance contained in this release, provides important supplemental information to management and investors regarding its anticipated results of operations. The Company is unable to provide a reconciliation of GAAP measures to corresponding forward-looking non-GAAP measures without unreasonable effort due to the high variability and low visibility of most of the items that have been excluded from these non-GAAP measures. For example, non-cash stock-based compensation expense is impacted by the Company's future hiring needs, the type and volume of equity awards necessary for such future hiring, and the price at which the Company's stock will trade in those future periods. In addition, the provision or benefit for income taxes is impacted by non-recurring income tax adjustments, valuation allowance on deferred tax assets, and the income tax effect of non-GAAP exclusions. The effects of these reconciling items may be significant, as the items that are being excluded are difficult to predict.

About The Hackett Group®

The Hackett Group, Inc. (NASDAQ: HCKT) is a Gen AI strategic consulting and digital transformation firm

that enables Digital World Class® performance. Using Hackett AI XPLR™, ZBrain™, XT™, AIXelerator™,

AskHackett™, and Quantum Leap® platforms, the company's experienced professionals and engineers

help organizations realize the power of Gen AI from ideation through implementation to achieve

quantifiable, breakthrough results with unprecedented speed, allowing it to be key architects of their Gen

AI journey. The company's expertise is grounded in unparalleled best practices insights from enterprise

performance benchmarks from the world's leading businesses – including 97% of the Dow Jones

Industrials, 90% of the Fortune 100, 68% of the DAX 40 and 53% of the FTSE 100. Visit us at

www.thehackettgroup.com/.

# # #

Trademarks

The Hackett Group®, quadrant logo, Digital World Class® and Quantum Leap® are the registered marks of The Hackett Group®.

(unaudited)

Quarter Ended
March 27, | March 28,
2026 | 2025
Revenue:
Revenue before reimbursements | 67,843 | 76,231
Reimbursements | 954 | 1,634
Total revenue | 68,797 | 77,865
Costs and expenses:
Cost of service:
Personnel costs before reimbursable expenses (includes $589 and $4,928 of non-cash stock based compensation reversal and expense in the three months ended March 27, 2026 and March 28, 2025, respectively) | 38,505 | 48,380
Reimbursable expenses | 954 | 1,634
Total cost of service | 39,459 | 50,014
Selling, general and administrative costs (includes $2,068 and $4,744 of non-cash stock based compensation expense in the three months ended March 27, 2026 and March 28, 2025, respectively) | 18,446 | 23,448
Restructuring costs | 1,956 | -
Total costs and operating expenses | 59,861 | 73,462
Operating income | 8,936 | 4,403
Other expense, net:
Interest expense, net | (1,008 | (202
Income before income taxes | 7,928 | 4,201
Income tax expense | 3,647 | 1,058
Net income | 4,281 | 3,143
Basic net income per common share:
Income per common share | 0.17 | 0.11
Weighted average common shares outstanding | 25,166 | 27,587
Diluted net income per common share:
Income per common share | 0.17 | 0.11
Weighted average common and common equivalent shares outstanding | 25,258 | 28,385

Page 5 of 8 - The Hackett Group, Inc. Announces First Quarter Results

The Hackett Group, Inc.

CONDENSED CONSOLIDATED BALANCE SHEETS

(in thousands)

(unaudited)

March 27, | December 27,
2026 | 2025
ASSETS
Current assets:
Cash | 6,068 | 18,197
Accounts receivable and contract assets, net | 70,284 | 59,505
Prepaid expenses and other current assets | 5,316 | 6,175
Total current assets | 81,668 | 83,877
Property, software and equipment, net | 25,163 | 24,011
Other assets | 356 | 358
Intangible assets | 2,869 | 3,252
Goodwill | 90,187 | 90,659
Operating lease right-of-use assets | 2,151 | 2,484
Deferred tax asset | 1,996 | 1,806
Total assets | 204,390 | 206,447
LIABILITIES AND SHAREHOLDERS' EQUITY
Current liabilities:
Accounts payable | 4,749 | 6,295
Accrued expenses and other liabilities | 24,340 | 28,824
Contract liabilities | 13,216 | 12,317
Income tax payable | - | 74
Operating lease liabilities | 1,168 | 1,259
Total current liabilities | 43,473 | 48,769
Deferred tax liability | 14,966 | 12,537
Long-term debt | 78,836 | 75,818
Operating lease liabilities | 1,103 | 1,223
Total liabilities | 138,378 | 138,347
Shareholders' equity | 66,012 | 68,100
Total liabilities and shareholders' equity | 204,390 | 206,447

Page 6 of 8 - The Hackett Group, Inc. Announces First Quarter Results

The Hackett Group, Inc.

SEGMENT PROFIT

(in thousands)

(unaudited)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-27_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

The following Management's Discussion and Analysis ("MD&A") is intended to help the reader understand the results of operations and financial condition of Hackett. MD&A is provided as a supplement to, and should be read in conjunction with, our consolidated financial statements and the accompanying Notes to our consolidated financial statements included in this Annual Report on Form 10-K. We have omitted discussion of fiscal 2023 items and year-to-year comparisons between fiscal years 2024 and 2023 where it would be redundant with the discussion previously included in Part II, Item 7 (MD&A) of the Company's Annual Report on Form 10-K for the fiscal year ended December 26, 2025.

Hackett is a global IP platform-based Gen AI strategic consulting and executive advisory digital transformation firm. The Hackett Group provides dedicated expertise in Gen AI enabled enterprise transformation services across front, mid and back office areas, including its highly recognized Oracle, SAP, OneStream and eProcurement implementation offerings.

In early 2024, we launched our AI assessment platform, AI XPLR which helps clients identify, evaluate and design Gen AI enablement opportunities. Using AI XPLR, our experienced professionals guide organizations to harness the power of Gen AI solutions designed to digitally transform their operations to achieve quantifiable, breakthrough results, allowing us to be key architects of our clients' Gen AI journey.

We believe Gen AI will fundamentally change the way companies operate as well as the way consulting services are sold and delivered. We believe the Gen AI platform capabilities we have developed in AI XPLR which were expanded with ZBrain, which we acquired as part of the LeewayHertz acquisition, is highly differentiating and we expect will enable us to effectively compete in this emerging and important space.

The Hackett Group has completed over 28,400 benchmarking and performance studies with major organizations. These studies are executed utilizing our Quantum Leap platform which drives our DTP. This includes the firm's benchmarking metrics, best practices repository, and best practice configuration and process flow accelerators, which enables our clients and partners to achieve digital world-class performance.

Our transformation expertise is grounded in best practices insights from benchmarking the world's leading businesses – including 97% of the Dow Jones Industrials, 90% of the Fortune 100, 68% of the DAX 40 and 53% of the FTSE 100, which inform and are delivered utilizing our platforms.

Impact of Macroeconomic Conditions on Our Business

The level of revenue we achieve is based on our ability to deliver market leading services and solutions and to deploy skilled teams of professionals quickly. Our results of operations are affected by economic conditions, including macroeconomic conditions and levels of business confidence. Any deterioration in the current macroeconomic environment or economic downturn as a result of weak or uncertain economic conditions due to inflation, high interest rates, national or geopolitical events or other factors impacting economic activity or business confidence could adversely affect our clients' financial condition or outlook which may reduce the clients' demand for our services.

Critical Accounting Policies and Estimates

In the ordinary course of business, we make a number of estimates and assumptions relating to the reporting of results of operations and financial position in conformity with generally accepted accounting principles in the United States ("GAAP"). Actual results could differ from those estimates under different assumptions and conditions. We believe the following discussion addresses our most critical accounting policies that have had or are reasonably likely to have a material impact on our financial condition or results of operations. These policies require management to exercise judgment on issues that are often difficult, subjective and complex due to the necessity of estimating the effect of matters that are inherently uncertain.

Revenue Recognition

Determining revenue recognition requires management to exercise judgment on the interpretation of service contracts which may include one or multiple performance obligations. The judgments that management must make include determining whether the control of the goods and services provided are transferred to our customers at a point in time or over the course of the service period utilizing a proportionate performance approach.

In fixed-fee billing arrangements, which would also include contracts with capped fees, we set the fees based on our estimates of the costs and timing for completing the engagements. We generally recognize revenue under fixed-fee or capped fee arrangements

using a proportionate performance approach, which is based on work completed to-date as compared to estimates of the total services to be provided under the engagement. Estimates of total engagement revenue and cost of services are monitored regularly during the term of the engagement based on the best available information. If our estimates indicate a potential loss, such loss is recognized in the period in which the loss first becomes probable and reasonably estimable.

Allowances for Credit Losses

We review accounts receivable to assess our estimates of collectability regularly. When establishing allowances for doubtful accounts, management must base their judgment on the information available at that point in time, which may include historical experiences, current economic trends and client credit worthiness, to determine the likelihood of collectability.

Business Combinations

For transactions that are considered business combinations, we utilize fair values in determining the carrying values of the purchased assets and assumed liabilities, which are recorded at fair value at acquisition date, and identifiable intangible assets are recorded at fair value. Costs directly related to the business combinations are recorded as expenses as they are incurred. Fair values are subject to refinement for up to one year after the closing date of an acquisition as information relative to closing date fair values become available. A bargain purchase gain on an acquisition occurs when the net of the estimated fair value of the assets acquired and liabilities assumed exceeds the consideration paid.

Goodwill

For acquisitions accounted for as a business combination, goodwill represents the excess of the cost over the fair value of the net assets acquired. The Company has organized its operating and internal reporting structure to align with its primary market solutions. In accordance with ASC 280, management made the determination to present three operating segments, three reportable segments and three reporting units as follows: (1) Global S&BT, (2) Oracle Solutions, and (3) SAP Solutions. A reporting unit is an operating segment or one level below an operating segment to which goodwill is assigned. The goodwill has been allocated to the reporting unit based on the reporting unit's relative fair value.

Goodwill is tested at least annually for impairment at the reporting unit level utilizing the market approach. In assessing the recoverability of goodwill and intangible assets, we utilize the market approach and makes estimates based on assumptions regarding various factors to determine if impairment tests are met. The market approach utilizes valuation multiples based on operating data from publicly traded companies within the same industry. Multiples derived from guideline companies provide an indication of how much a market participant would be willing to pay for a company. These multiples are then applied to the our reporting units to arrive at an indication of value. This approach contains management's judgment, using appropriate and customary assumptions available at the time.

We performed our annual impairment test of goodwill in the fourth quarter of fiscal years 2025, 2024 and 2023 and determined that goodwill was not impaired.

Stock Based Compensation

We recognize compensation expense for awards of equity and liability instruments, which have only a service condition, to employees based on the grant-date fair value of those awards, over the requisite service period, with limited exceptions.

In September 2024, a stock price award program was offered to certain leaders. These equity awards were granted with both a market condition (three tranches, each with varying market share price thresholds) and service conditions. We measured these equity awards using the Monte Carlo valuation model to determine the fair value as of the grant date. The Monte Carlo valuation model, using different share price paths, calculated a derived service period which is the median share price path on which the market condition is satisfied for each tranche. The assumptions utilized in the model are as of a point in time and may differ from the actual value of the equity awards. The requisite service period was determined to be service conditions as the service conditions are greater than the derived service period. For each of the three tranches, stock compensation expense is recognized on a straight-line basis over the requisite service period. We elected to account for forfeitures as incurred. If an employee forfeits nonvested shares subsequent to meeting a service condition, the previously recognized expense is not reversed. See Note 10, "Stock Based Compensation," to our consolidated financial statements included in our Annual Report on Form 10-K for additional information.

Please refer to Note 1, "Basis of Presentation and General Information," to our consolidated financial statements included in our Annual Report on Form 10-K for the discussion of all of our critical accounting policies.

Results of Operations

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-27_item1_business.md)

ITEM 1. BUSI NESS

GENERAL

In this Annual Report on Form 10-K, unless the context otherwise requires, "The Hackett Group," "Hackett," the "Company," "we," "us," and "our" refer to The Hackett Group, Inc. and its subsidiaries and predecessors. We were originally incorporated on April 23, 1997.

Our fiscal year ended December 26, 2025.

OVERVIEW

The Hackett Group, Inc. (NASDAQ: HCKT) is a global, IP platform-based generative artificial intelligence ("Gen AI") strategic advisory, business transformation, and enterprise application implementation firm. We combine proprietary benchmarking and best-practice process intelligence intellectual property ("IP") with Gen AI–enabled delivery platforms to help clients identify, prioritize, design, and implement high-impact improvements across enterprise functions, including supply chain and operations, finance, human resources, information technology, procurement and corporate services, as well as selected enterprise application implementation services, including Oracle, SAP, OneStream, and eProcurement applications.

WHAT MAKES US DIFFERENT?

Over the past two years, we have systematically developed a suite of IP Gen AI platforms delivery platforms, which are distinctly enabled by our Hackett Domain Specific Language Model, which we refer to as our Solution Language Model ("SLM"). The Hackett SLM does not produce generic ideas. It applies domain expertise, our process performance benchmarks and best practices intelligence IP, and a structured ideation and solution-design approach to rapidly turn AI opportunities into deployable, implementation-ready solutions. This innovation allows us to accelerate and enhance all of our client AI transformation efforts and highly differentiates our offerings. We do not believe that you can successfully deploy high impact solutions without a detail understanding of the client specific requirements. Without client specific business, process, automation and data requirements, there is no way to drive true breakthrough or transformative value to complex enterprise environments.

Our platform-enabled model is grounded in our globally recognized Digital World Class® performance benchmarks and best-practice process intelligence (collectively, "Hackett Intelligence IP"). As of December 26, 2025, we have completed over 28,400 benchmarking and performance studies and have measured and evaluated enterprise processes for thousands of organizations globally. This proprietary process benchmarking and intelligence IP is the foundation for our offerings and power the structured knowledge embedded within our Gen AI platforms.

MARKET CONTEXT AND INDUSTRY DYNAMICS

We believe we are entering a massive automation expansion era, which will significantly increase the automation footprint of most organizations. This new opportunity will require enterprise software and service providers to expand their agentic capabilities to capture this opportunity. We believe this AI transition is also forcing organizations to reassess the nature of transformation investments in response to rapidly evolving Gen AI capabilities. While demand for traditional digital transformation remains present, many organizations are redirecting an increasing amount of their Gen AI experimentation and tactical initiatives to enterprise wide assessment of high impact AI solutions.

We believe that sustainable AI value realization requires more than access to large language models or other generic automation tools. Meaningful return on investment ("ROI") results depend on enterprise discovery efforts that allows organizations to prioritize their investment to more ambitious solutions which are pursued based on strategic priorities and the capability of the respective organization. Our platforms are designed to address these requirements and help clients move from experimentation to transformational operationalized, measurable outcomes.

OUR OFFERINGS AND IP PLATFORM-BASED DELIVERY MODEL

Our platforms have now allowed us to transition from a traditional labor-based delivery model to an IP platform enabled approach. Under our new delivery model our consultants leverage our new platforms to accelerate and enhance the value we deliver to our clients. This Gen AI enabled model is highly differentiated and allows us to deliver measurable ROI outcomes which we believe will allow us to increase our addressable market with new enterprise-wide solutions which we expect will increase our Gen AI revenues and expand our margins.

Hackett Intelligence IP

Our proprietary intellectual property includes benchmarking metrics, productivity and cost analytics, best practices, process taxonomies, software configuration guides and best-practice process flows developed over decades of client transformational benchmarking engagements and research. We use this IP to quantify performance gaps, identify performance improvement opportunities, conduct enterprise application fit analyses and define target-state operating models to support execution. Our IP is continuously refreshed through ongoing benchmark studies, client engagements, and hands-on delivery experience.

Hackett Solution Language Model and Platform Architecture

Our Gen AI delivery platforms leverage a proprietary domain specific SLM and structured knowledge derived from our Hackett Intelligence IP. This architecture is designed, trained and tuned to deliver context-aware insight and repeatable solution designs from end to end process to an individual work step level. It is this granular capability that allows us to create complete and precise solution outcomes.

Hackett AI XPLR™

Hackett AI XPLR ("AI XPLR") enables enterprises to identify feasible AI opportunities, design optimal AI‑enabled agentic workflows, and invest with confidence, which is supported by Hackett performance intelligence validated ROI.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-27_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-27_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-27_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-05_2-02-results.md, 10-K_2026-02-27_item7_mdna.md, 10-K_2026-02-27_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
