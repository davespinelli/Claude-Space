# Triage pack — PD · PagerDuty, Inc.

_Generated 2026-09-04 19:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PD · **Name:** PagerDuty, Inc.
- **CIK:** 0001568100
- **SIC:** 7372 — Services-Prepackaged Software
- **Fiscal year end (MM-DD):** 01-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/PD

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** PagerDuty, Inc.
- **CIK:** 1,568,100 · **SIC:** 7372 (Services-Prepackaged Software) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 14.10 |
| mktcap | $1.1B |
| ev | $1.3B |
| ev_ebit | 218.2x |
| fcf | $111.9M |
| fcf_yield | 10.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 1.1% |
| net_debt | $187.0M |
| net_debt_ebit | 32.0x |
| cash | $233.7M |
| ltd | $420.6M |
| equity | $232.0M |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $492.5M |
| revenue_prior | $467.5M |
| rev_growth | 5.4% |
| rev_growth_note | n/a |
| eq_flag | net income more than 3x operating income |
| ebit | $5.8M |
| net_income | $172.7M |
| cfo | $114.9M |
| capex | $2.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -16.3% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 77,122,565 |
| shares_py | 92,173,975 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -28.0% |
| r6m | 81.7% |
| off_52w_high | -17.9% |
| adv20 | $18.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.73 |
| r_ev_ebit | 0.02 |
| r_roic | 0.35 |
| r_rev_growth | 0.53 |
| r_buyback | 0.97 |
| score | 0.52 |

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
| rank | 225 |

**Screen rationale:** buying back stock -16.3%; EARNINGS QUALITY: net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **77,122,565** (CY2026Q2I) vs **92,173,975** prior year (CY2025Q2I)
- Change: **-16.3%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-07-14** — Item 5.02 (officer / director change or comp arrangement): On July 11, 2026, Elena Gomez informed PagerDuty, Inc. (the "Company") of her resignation from the Board of Directors (the "Board") of the Company and from the audit committee of the Board (the "Audit Committee"), effective July 11, 2026.
- **2026-06-22** — Item 5.02 (officer / director change or comp arrangement): On June 22, 2026, PagerDuty, Inc. (the "Company") announced the appointment of Eric Prengel as the Company's Chief Financial Officer ("CFO"), effective June 22, 2026 (the "Appointment Date").
- **2026-05-11** — Item 5.02 (officer / director change or comp arrangement): On May 11, 2026, PagerDuty, Inc. (the " Company ") announced the

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 398,947 sh / $4,240,938 -> net $-4,240,938 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 8 |
| F | 4 |
| M | 4 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-27_2-02-results.md)

_Extraction: started at the first release heading, 'Second quarter revenue increased 1% year over year to $124 million'; skipped 15 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex991-pagerdutyq2fy27earni.htm)

Second quarter revenue increased 1% year over year to $124 million

Annual Recurring Revenue ( " ARR " ) grew year over year to $501 million

Second quarter operating income was $10 million; non-GAAP operating income was $30 million

Net income was $5 million, representing the fifth consecutive quarter of GAAP profitability

SAN FRANCISCO – (BUSINESS WIRE) – August 27, 2026 – PagerDuty, Inc. (NYSE:PD), a leader in AI-first operations management, today announced financial results for the second quarter of fiscal 2027, ended July 31, 2026.

"We delivered revenue above the high end of our guidance range, crossed $500 million in ARR, and generated $33 million in free cash flow this quarter, providing encouraging signals that our strategy is gaining traction," said John DiLullo, CEO. "Just as importantly, the underlying fundamentals are strengthening. Non-GAAP operating income also came in ahead of expectations and we enjoyed our fifth consecutive quarter of GAAP profitability. AI is transforming how software is built and operated, and PagerDuty is uniquely positioned to benefit from that shift."

Second Quarter Fiscal 2027 Financial Highlights

• Revenue was $124.4 million, an increase of 0.8% year over year.

• Operating income was $10.2 million; operating margin was 8.2%.

• Non-GAAP operating income was $29.5 million; non-GAAP operating margin was 23.7%.

• Net income attributable to PagerDuty, Inc. common stockholders was $4.7 million, representing the Company's fifth consecutive quarter of GAAP profitability.

• Net income per diluted share attributable to PagerDuty, Inc. common stockholders was $0.06.

• Non-GAAP net income per diluted share attributable to PagerDuty, Inc. common stockholders was $0.32.

• Net cash provided by operating activities was $36.9 million; free cash flow was $32.8 million.

• Cash, cash equivalents, and investments were $470.0 million as of July 31, 2026.

The section titled "Non-GAAP Financial Measures" below contains a description of the non-GAAP financial measures and reconciliations between GAAP and non-GAAP financial information.

Second Quarter and Recent Highlights

• ARR as of July 31, 2026 was $501 million.

• Customers with ARR over $100 thousand was 884 as of July 31, 2026.

• Dollar-based net retention rate was 98% as of July 31, 2026.

• Total paid customers were 15,506 as of July 31, 2026,.

• Lands and expands include: Anthropic, PBC, Banco Pichincha, C.A., Coreweave, Inc., Delivery Hero SE, Kawasaki Heavy Industries, Ltd., and Palo Alto Networks, Inc.

• Appointed John DiLullo as Chief Executive Officer.

• Named Eric Prengel as Chief Financial Officer and announced the retirement of Howard Wilson.

• Appointed Alex Shootman to the Board of Directors.

• In Q2, major upgrades were made to PagerDuty's autonomous SRE agent, incident management lifecycle integration, and the Company's agentic offering for simplifying on-call shift management.

• Announced distribution agreement in Australia with Ingram Micro.

Financial Outlook

For the third quarter of fiscal 2027, PagerDuty currently expects:

• Total revenue of $123.0 million - $125.0 million.

• Non-GAAP operating margin of 26.5% to 27.5%.

• Non-GAAP net income per diluted share attributable to PagerDuty, Inc. common stockholders of $0.34 - $0.36, assuming approximately 80 million diluted shares and a non-GAAP tax rate of 20%.

For the full fiscal year 2027, PagerDuty currently expects:

• Total revenue of $491.5 million - $496.5 million.

• Non-GAAP operating margin of 25.0% to 26.0%.

• Non-GAAP net income per diluted share attributable to PagerDuty, Inc. common stockholders of $1.33 - $1.37, assuming approximately 80 million diluted shares and a non-GAAP tax rate of 20%.

Debbie O'Brien

media@pagerduty.com

SOURCE PagerDuty

Source: PagerDuty, Inc.

PAGERDUTY, INC.

CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS

(in thousands, except per share data)

(unaudited)

Three months ended July 31, | Six months ended July 31,
2026 | 2025 | 2026 | 2025
Revenue | 124,436 | 123,411 | 245,403 | 243,216
Cost of revenue (1) | 20,037 | 19,001 | 39,057 | 38,185
Gross profit | 104,399 | 104,410 | 206,346 | 205,031
Operating expenses:
Research and development (1) | 30,897 | 30,897 | 60,885 | 64,945
Sales and marketing (1) | 38,325 | 44,456 | 77,935 | 94,501
General and administrative (1) | 24,938 | 25,491 | 48,104 | 52,346
Total operating expenses | 94,160 | 100,844 | 186,924 | 211,792
Income (loss) from operations | 10,239 | 3,566 | 19,422 | (6,761)
Interest income | 4,101 | 6,149 | 8,027 | 12,160
Interest expense | (2,113) | (2,286) | (4,220) | (4,650)
Other (expense) income, net | (157) | 120 | (228) | 234
Income before provision for (benefit from) income taxes | 12,070 | 7,549 | 23,001 | 983
Provision for (benefit from) income taxes | 4,357 | (1,865) | 10,158 | (1,052)
Net income | 7,713 | 9,414 | 12,843 | 2,035
Net loss attributable to redeemable non-controlling interest | (72) | (161) | (225) | (378)
Net income attributable to PagerDuty, Inc. | 7,785 | 9,575 | 13,068 | 2,413
Less: Adjustment attributable to redeemable non-controlling interest | 3,059 | (202) | (1,904) | (867)
Net income attributable to PagerDuty, Inc. common stockholders | 4,726 | 9,777 | 14,972 | 3,280
Weighted average shares used in calculating net income per share
Basic | 77,334 | 92,600 | 77,980 | 91,997
Diluted | 79,141 | 94,198 | 79,294 | 93,895
Net income per share attributable to PagerDuty, Inc. common stockholders
Basic | 0.06 | 0.11 | 0.19 | 0.04
Diluted | 0.06 | 0.10 | 0.19 | 0.03

(1) Includes stock-based compensation expense as follows:

Three months ended July 31, | Six months ended July 31,
2026 | 2025 | 2026 | 2025
Cost of revenue | 665 | 1,213 | 1,514 | 2,310
Research and development | 5,592 | 9,560 | 11,729 | 19,400
Sales and marketing | 3,064 | 5,285 | 7,248 | 11,504
General and administrative | 7,151 | 9,902 | 13,944 | 18,499
Total | 16,472 | 25,960 | 34,435 | 51,713

PAGERDUTY, INC.

CONDENSED CONSOLIDATED BALANCE SHEETS

(in thousands)

(unaudited)

July 31, 2026 | January 31, 2026
Assets
Current assets:
Cash and cash equivalents | 233,651 | 237,402
Investments | 236,392 | 232,436
Accounts receivable, net of allowance for credit losses of $838 and $1,175 as of July 31, 2026 and January 31, 2026, respectively | 71,738 | 108,430
Deferred contract costs, current | 18,351 | 18,401
Prepaid expenses and other current assets | 18,983 | 15,570
Total current assets | 579,115 | 612,239
Property and equipment, net | 34,355 | 29,192
Deferred contract costs, non-current | 24,982 | 25,010
Lease right-of-use assets | 11,325 | 12,509
Goodwill | 137,401 | 137,401
Intangible assets, net | 13,765 | 15,645
Deferred tax assets | 153,657 | 153,657
Other assets | 3,719 | 4,862
Total assets | 958,319 | 990,515
Liabilities, redeemable non-controlling interest, and stockholders' equity
Current liabilities:
Accounts payable | 5,581 | 6,718
Accrued expenses and other current liabilities | 18,288 | 19,868
Accrued compensation | 23,810 | 25,856
Deferred revenue, current | 233,528 | 246,451
Lease liabilities, current | 6,010 | 5,000
Total current liabilities | 287,217 | 303,893
Convertible senior notes, net, non-current | 396,930 | 395,729
Deferred revenue, non-current | 2,462 | 2,483
Lease liabilities, non-current | 9,877 | 12,598
Other liabilities | 14,929 | 5,147
Total liabilities | 711,415 | 719,850
Redeemable non-controlling interest | 14,943 | 17,072
Stockholders' equity
Common stock | — | —
Additional paid-in capital | 649,436 | 679,410
Accumulated other comprehensive loss | (1,128) | (183)
Accumulated deficit | (408,729) | (421,797)
Treasury stock | (7,618) | (3,837)
Total stockholders' equity | 231,961 | 253,593
Total liabilities, redeemable non-controlling interest, and stockholders' equity | 958,319 | 990,515

PAGERDUTY, INC.

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS

(in thousands)

(unaudited)

Three months ended July 31, | Six months ended July 31,
2026 | 2025 | 2026 | 2025
Cash flows from operating activities:
Net income attributable to PagerDuty, Inc. common stockholders | 4,726 | 9,777 | 14,972 | 3,280
Net loss and adjustment attributable to redeemable non-controlling interest | 2,987 | (363) | (2,129) | (1,245)
Net income | 7,713 | 9,414 | 12,843 | 2,035
Adjustments to reconcile net income to net cash provided by operating activities:
Depreciation and amortization | 2,899 | 3,122 | 5,955 | 7,084
Amortization of deferred contract costs | 5,332 | 5,703 | 10,533 | 11,217
Amortization of debt issuance costs | 606 | 655 | 1,201 | 1,332
Stock-based compensation | 16,472 | 25,960 | 34,435 | 51,713
Non-cash lease expense | 995 | 514 | 1,980 | 893
Deferred income taxes | 4,114 | (1,786) | 9,850 | (1,624)
Other | (28) | (556) | (623) | (1,367)
Changes in operating assets and liabilities:
Accounts receivable | 4,043 | 8,919 | 36,661 | 36,529
Deferred contract costs | (5,809) | (5,664) | (10,502) | (10,243)
Prepaid expenses and other assets | 1,698 | 2,888 | (3,347) | (428)
Accounts payable | 1,696 | (562) | (1,129) | (459)
Accrued expenses and other liabilities | 3,561 | (3,421) | 758 | (5,394)
Accrued compensation | 2,256 | (996) | (2,237) | (9,332)
Deferred revenue | (7,354) | (9,519) | (12,734) | (15,930)
Lease liabilities | (1,248) | (697) | (2,415) | (1,382)
Net cash provided by operating activities | 36,946 | 33,974 | 81,229 | 64,644
Cash flows from investing activities:
Purchases of property and equipment | (2,226) | (874) | (3,191) | (1,315)
Capitalized software costs | (1,937) | (2,893) | (4,063) | (4,136)
Purchases of available-for-sale investments | (46,005) | (48,169) | (86,301) | (92,317)
Proceeds from maturities of available-for-sale investments | 44,531 | 44,510 | 81,951 | 88,910
Proceeds from sales of available-for-sale investments | — | 1,248 | — | 1,248
Purchases of non-marketable equity investments | — | (1,000) | — | (1,250)
Proceeds from liquidation of non-marketable equity investments | — | — | 894 | —
Net cash used in investing activities | (5,637) | (7,178) | (10,710) | (8,860)
Cash flows from financing activities:
Repurchases of common stock | (7,477) | — | (72,933) | —
Repayments of convertible senior notes | (57,500) | — | (57,500)
Proceeds from employee stock purchase plan | 3,479 | 4,618 | 3,479 | 4,618
Excise tax paid on repurchases of common stock | (808) | — | (808) | —
Proceeds from issuance of common stock upon exercise of stock options | 1,788 | 208 | 1,792 | 3,810
Employee payroll taxes paid related to net share settlement of restricted stock units | (3,504) | (6,411) | (5,660) | (13,968)
Net cash used in financing activities | (6,522) | (59,085) | (74,130) | (63,040)
Effects of foreign currency exchange rates on cash, cash equivalents, and restricted cash | (16) | (222) | (140) | 113
Net change in cash, cash equivalents, and restricted cash | 24,771 | (32,511) | (3,751) | (7,143)
Cash, cash equivalents, and restricted cash at beginning of period | 209,959 | 373,696 | 238,481 | 348,328
Cash, cash equivalents, and restricted cash at end of period | 234,730 | 341,185 | 234,730 | 341,185

Note: Certain reclassifications of prior period amounts have been made in the Company's condensed consolidated statements of cash flows to conform to the current period presentation. Refer to the notes to our Quarterly Report on Form 10-Q for more information.

Non-GAAP Financial Measures

This press release and the accompanying tables contain the following non-GAAP financial measures: non-GAAP gross profit, non-GAAP gross margin, non-GAAP research and development, non-GAAP sales and marketing, non-GAAP general and administrative, non-GAAP operating income, non-GAAP operating margin, non-GAAP net income attributable to PagerDuty, Inc. common stockholders, non-GAAP net income per share attributable to PagerDuty, Inc. common stockholders, free cash flow, and free cash flow margin.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-12_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

PagerDuty, Inc. transforms critical work for modern business by building operational resilience, reducing risk, improving customer experience, and driving operational efficiency across digital operations. As a global leader in digital operations management since 2009, PagerDuty helps enterprises manage the complex web of infrastructure, applications, and systems that power today's digital experiences. The PagerDuty Operations Cloud sits at the center of the enterprise technology stack as a system of intelligence and action, ingesting signals from over 700 integrations—including monitoring, observability, security, customer service, and development tools—to orchestrate the right response across people, machines, and software.

Built for the modern era of artificial intelligence ("AI"), PagerDuty empowers customers to maximize the value of their AI investments through agentic workflows, AI-powered automation, and intelligent orchestration that accelerates incident detection and resolution while enabling teams to focus on innovation rather than firefighting.

In today's environment, every business is fundamentally a digital business. Whether in retail, financial services, healthcare, telecommunications, or supply chain logistics, modern commerce depends on increasingly complex networks of digital infrastructure, cloud services, applications, and distributed teams that operate in an always-on world. This complexity continues to accelerate as organizations adopt AI-driven systems and integrate artificial intelligence across their operations.

Customer expectations have never been higher. Incidents are measured not just in lost revenue but in damaged brand reputation and customer trust. Organizations face mounting pressure to deliver always-on digital experiences, resolve issues proactively before customers are impacted, and innovate rapidly without proportionally increasing operational costs or headcount. The ability to anticipate, orchestrate, and resolve time-sensitive, critical, and unplanned work before it escalates has become a strategic imperative and competitive differentiator.

Since our founding in 2009, PagerDuty has evolved from a single product focused on on-call management for developers into a comprehensive, multi-product operations cloud that spans the entire enterprise. Today, our platform breaks down organizational silos across development, IT operations, security, customer service, and business operations, reaching technical practitioners and executive stakeholders alike.

Over more than a decade, we have built one of the industry's most comprehensive integration ecosystems, with over 700 direct integrations spanning monitoring tools, cloud platforms, collaboration systems, ITSM solutions, and business applications. We also support the Model Context Protocol ("MCP"), enabling seamless integration with AI agents and large language model-powered tools to extend our platform's capabilities into emerging AI workflows. This deep integration fabric allows our customers to gather and correlate digital signals from across their entire technology stack – both modern cloud-native and legacy systems – without the friction of context switching or manual data aggregation.

These same integrations enable powerful workflow automation, connecting technical operations with popular collaboration tools and business applications to drive coordinated responses and accelerate resolution. Our open platform approach and extensive partner ecosystem have become a strategic moat, making PagerDuty increasingly embedded and essential within our customers' operations.

We generate revenue primarily from cloud-hosted software subscriptions, with additional revenue from term-license arrangements. Our land-and-expand business model drives viral adoption and natural expansion as teams experience value and extend PagerDuty to new users, use cases, and products. During the current fiscal year, we took initial steps to provide customers with more flexible pricing options, including usage-based pricing models that enable customers to seamlessly scale between human responders, agents, and automated solutions, better aligning customer investments to business outcomes rather than headcount and licenses, and supporting our transition from traditional single-year seat-based licensing to multiyear platform usage agreements.

While the PagerDuty platform serves organizations of all sizes, we have strategically focused our go-to-market investments, including our enterprise field sales organization, on serving enterprise customers where we see the greatest opportunity for platform adoption and expansion. Today, nearly half of the Fortune 500, half of the Forbes AI 50, and approximately two-thirds of the Fortune 100 rely on PagerDuty as mission-critical infrastructure. Our enterprise customers represent the majority of our revenue and demonstrate strong retention and expansion characteristics.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table sets forth our consolidated statements of operations data for the periods indicated and as a percentage of revenue (in thousands, except percentages):

Year ended January 31,
2026 | 2025
Revenue | 492,546 | 100.0 | % | 467,499 | 100.0 | %
Cost of revenue (1) | 74,142 | 15.1 | % | 79,665 | 17.0 | %
Gross profit | 418,404 | 84.9 | % | 387,834 | 83.0 | %
Operating expenses:
Research and development (1) | 126,937 | 25.8 | % | 141,489 | 30.3 | %
Sales and marketing (1) | 184,040 | 37.4 | % | 201,821 | 43.2 | %
General and administrative (1) | 101,587 | 20.6 | % | 104,296 | 22.3 | %
Total operating expenses | 412,564 | 83.8 | % | 447,606 | 95.7 | %
Income (loss) from operations | 5,840 | 1.2 | % | (59,772) | (12.8) | %
Interest income | 22,693 | 4.6 | % | 27,492 | 5.9 | %
Interest expense | (8,857) | (1.8) | % | (9,258) | (2.0) | %
Other income (expense), net | 489 | 0.1 | % | (215) | — | %
Income (loss) before (benefit from) provision for income taxes | 20,165 | 4.1 | % | (41,753) | (8.9) | %
(Benefit from) provision for income taxes | (152,544) | (31.0) | % | 1,783 | 0.4 | %
Net income (loss) | 172,709 | 35.1 | % | (43,536) | (9.3) | %
Net loss attributable to redeemable non-controlling interest | (664) | (0.1) | % | (801) | (0.2) | %
Net income (loss) attributable to PagerDuty, Inc. | 173,373 | 35.2 | % | (42,735) | (9.1) | %
Less: Adjustment attributable to redeemable non-controlling interest | (481) | (0.1) | % | 11,725 | 2.5 | %
Net income (loss) attributable to PagerDuty, Inc. common stockholders | 173,854 | 35.3 | % | (54,460) | (11.6) | %

Note: Certain figures may not sum due to rounding.

(1) Includes stock-based compensation expense as follows (in thousands):

Year ended January 31,
2026 | 2025
Cost of revenue | 4,283 | 5,984
Research and development | 36,345 | 44,691
Sales and marketing | 22,420 | 31,185
General and administrative | 34,756 | 44,350
Total | 97,804 | 126,210

Revenue

We generate revenue primarily from cloud-hosted software subscription fees. We also generate revenue from term-license software subscription fees. Our subscriptions are typically one year in duration but can range from monthly to multi-year. Subscription fees are driven primarily by the number of customers, the number of users per customer, and the level of subscription purchased. We generally invoice customers in advance in annual installments for subscriptions to our software. Revenue related to our cloud-hosted software subscriptions is recognized ratably over the related contractual term beginning on the date that our platform is made available to a customer. For our term-license software subscriptions, we recognize license revenue upon delivery, and software maintenance revenue ratably, typically beginning on the start of the contractual term of the arrangement.

Due to the low complexity of implementation and integration of our platform with our customers' existing infrastructure, revenue from professional services has not been material to date.

The following sets forth our revenue for the periods indicated (in thousands, except percentages):

Year ended January 31, | Change
2026 | 2025 | %
Revenue | 492,546 | 467,499 | 25,047 | 5 | %

Revenue increased primarily due to growth from existing customers, which was driven by an increase in the number of users and upsell of additional products and services.

Cost of Revenue and Gross Margin

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-12_item1_business.md)

Item 1. Business

Overview

PagerDuty, Inc. ("PagerDuty," "we," "us" or "our") transforms critical work for modern business by building operational resilience, reducing risk, improving customer experience, and driving operational efficiency across digital operations. As a global leader in digital operations management since 2009, PagerDuty helps enterprises manage the complex web of infrastructure, applications, and systems that power today's digital experiences. The PagerDuty Operations Cloud sits at the center of the enterprise technology stack as a system of intelligence and action, ingesting signals from over 700 integrations—including monitoring, observability, security, customer service, and development tools—to orchestrate the right response across people, machines, and software.

Built for the modern era of artificial intelligence ("AI"), PagerDuty empowers customers to maximize the value of their AI investments through agentic workflows, AI-powered automation, and intelligent orchestration that accelerates incident detection and resolution while enabling teams to focus on innovation rather than firefighting.

In today's environment, every business is fundamentally a digital business. Whether in retail, financial services, healthcare, telecommunications, or supply chain logistics, modern commerce depends on increasingly complex networks of digital infrastructure, cloud services, applications, and distributed teams that operate in an always-on world. This complexity continues to accelerate as organizations adopt AI-driven systems and integrate artificial intelligence across their operations.

Customer expectations have never been higher. Incidents are measured not just in lost revenue but in damaged brand reputation and customer trust. Organizations face mounting pressure to deliver always-on digital experiences, resolve issues proactively before customers are impacted, and innovate rapidly without proportionally increasing operational costs or headcount. The ability to anticipate, orchestrate, and resolve time-sensitive, critical, and unplanned work before it escalates has become a strategic imperative and competitive differentiator.

Since our founding in 2009, PagerDuty has evolved from a single product focused on on-call management for developers into a comprehensive, multi-product operations cloud platform that spans the entire enterprise. Today, our platform breaks down organizational silos across development, IT operations, security, customer service, and business operations, reaching technical practitioners and executive stakeholders alike.

Our platform ingests and analyzes digital signals from virtually any software-enabled system or device across our customers' technology estates. Leveraging advanced AI and machine learning capabilities, we correlate, process, predict, and remediate both incidents and opportunities in real time. This intelligence powers our core capabilities in incident management, bringing together the right people with the right context and recommended actions so they can resolve issues in minutes or seconds, from anywhere.

We have made significant investments in generative AI to fundamentally transform how organizations manage critical work. Our AI capabilities enable teams to work smarter and faster, automating routine tasks, providing intelligent recommendations, and accelerating time to resolution. These innovations are increasingly central to our value proposition as customers seek to do more with existing resources while managing growing operational complexity.

Over more than a decade, we have built one of the industry's most comprehensive integration ecosystems, with over 700 direct integrations spanning monitoring tools, cloud platforms, collaboration systems, ITSM solutions, and business applications. We also support the Model Context Protocol ("MCP"), enabling seamless integration with AI agents and large language model-powered tools to extend our platform's capabilities into emerging AI workflows. This deep integration fabric allows our customers to gather and correlate digital signals from across their entire technology stack – both modern cloud-native and legacy systems – without the friction of context switching or manual data aggregation.

These same integrations enable powerful workflow automation, connecting technical operations with popular collaboration tools and business applications to drive coordinated responses and accelerate resolution. Our open platform approach and extensive partner ecosystem have become a strategic moat, making PagerDuty increasingly embedded and essential within our customers' operations.

We generate revenue primarily from cloud-hosted software subscriptions, with additional revenue from term-license arrangements. Our land-and-expand business model drives viral adoption and natural expansion as teams experience value and extend PagerDuty to new users, use cases, and products. During the current fiscal year, we took initial steps to provide customers with more flexible pricing options, including usage-based pricing models that enable customers to seamlessly scale between human responders, agents, and automated solutions, better aligning customer investments to business outcomes rather than headcount and licenses, and supporting our transition from traditional single-year seat-based licensing to multiyear platform usage agreements.

While the PagerDuty platform serves organizations of all sizes, we have strategically focused our go-to-market investments, including our enterprise field sales organization, on serving enterprise customers where we see the greatest opportunity for platform adoption and expansion. Today, nearly half of the Fortune 500, half of the Forbes AI 50, and approximately two-thirds of the Fortune 100 rely on PagerDuty as mission-critical infrastructure. Our enterprise customers represent the majority of our revenue and demonstrate strong retention and expansion characteristics.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-27_2-02-results.md, 10-K_2026-03-12_item7_mdna.md, 10-K_2026-03-12_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
