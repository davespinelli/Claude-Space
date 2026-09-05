# Triage pack — PGNY · Progyny, Inc.

_Generated 2026-09-05 08:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** PGNY · **Name:** Progyny, Inc.
- **CIK:** 0001551306
- **SIC:** 8090 — Services-Misc Health & Allied Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/PGNY

## 2. Screen row (all metrics)

_Source: candidates.csv_

- **Name:** Progyny, Inc.
- **CIK:** 1,551,306 · **SIC:** 8090 (Services-Misc Health & Allied Services, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 25.94 |
| mktcap | $2.0B |
| ev | $1.8B |
| ev_ebit | 21.5x |
| fcf | $191.8M |
| fcf_yield | 9.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 22.4% |
| net_debt | -$152.6M |
| net_debt_ebit | -1.8x |
| cash | $152.6M |
| ltd | $0.00 |
| equity | $453.3M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.3B |
| revenue_prior | $1.2B |
| rev_growth | 10.4% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $85.3M |
| net_income | $58.5M |
| cfo | $210.2M |
| capex | $18.4M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -10.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 76,726,798 |
| shares_py | 85,982,409 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 28.2% |
| r6m | 41.7% |
| off_52w_high | -19.8% |
| adv20 | $26.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.74 |
| r_ev_ebit | 0.43 |
| r_roic | 0.89 |
| r_rev_growth | 0.65 |
| r_buyback | 0.96 |
| score | 0.78 |

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

**Screen rationale:** high ROIC 22.4%; buying back stock -10.8%; debt data missing (net cash unverified); 12-1 momentum 28.2%


## 3. Share count trend

- Shares outstanding: **76,726,798** (CY2026Q2I) vs **85,982,409** prior year (CY2025Q2I)
- Change: **-10.8%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 5 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 23,705 sh / $621,339 -> net $-621,339 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 30 (open-market buys 0, sales 10).

| code | rows |
|---|---|
| F | 14 |
| J | 2 |
| M | 4 |
| S | 10 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter 2026 Highlights:'; skipped 12 forward-looking-statement block(s); 11 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (exhibit991q22026.htm)

Second Quarter 2026 Highlights:
(unaudited; in thousands, except per share amounts) | 2Q 2026 | 2Q 2025
Revenue | $350,511 | $332,874
Gross Profit | $89,301 | $78,973
Gross Margin | 25.5% | 23.7%
Net Income | $28,052 | $17,112
Net Income per Diluted Share 1 | $0.34 | $0.19
Adjusted Earnings per Diluted Share 2 | $0.55 | $0.48
Adjusted EBITDA 2 | $62,104 | $57,946
Adjusted EBITDA Margin 2 | 17.7% | 17.4%
Trailing Twelve-Month Operating Cash Flow | $201,248 | $201,997

1. Net income per diluted share reflects weighted-average shares outstanding as adjusted for potential dilutive securities, including options, restricted stock units, and shares issuable under the employee stock purchase plan .

2. Adjusted Earnings per Diluted Share, Adjusted EBITDA, and Adjusted EBITDA margin are financial measures that are not required by, or presented in accordance with U.S. generally accepted accounting principles ("GAAP"). Please see Annex A of this press release for a reconciliation of Adjusted Earnings per Diluted Share to earnings per share, and Adjusted EBITDA to net income, the most directly comparable financial measures stated in accordance with GAAP for each of the periods presented. We calculate Adjusted Earnings per Diluted Share as net income per diluted share excluding the impact of stock-based compensation, adjusted for the impact of taxes. We calculate Adjusted EBITDA margin as Adjusted EBITDA divided by revenue.

Financial Highlights

Revenue was $350.5 million, a 5.3% increase as compared to the $332.9 million reported in the second quarter of 2025, as the increase in the number of clients and covered lives was partially offset by the impact of the previously disclosed large client who did not renew its services for 2025, though it provided for an extended transition period over the first half of 2025 for members meeting certain criteria. There was no contribution from this client in the second quarter of 2026, and excluding the $17.2 million of revenue from this client in the second quarter of 2025, revenue increased 11.0%.

• Fertility benefit services revenue was $230.2 million, a 7.6% increase from the $213.9 million reported in the second quarter of 2025.

• Pharmacy benefit services revenue was $120.3 million, a 1.2% increase as compared to the $118.9 million reported in the second quarter of 2025.

Gross profit was $89.3 million, an increase of 13% from the $79.0 million reported in the second quarter of 2025, reflecting ongoing efficiencies realized in the delivery of our care management services as well as a decrease in stock-based compensation expense . Gross margin was 25.5%, as compared to 23.7% reported in the prior year .

Net income was $28.1 million, or $0.34 income per diluted share, as compared to the $17.1 million, or $0.19 income per diluted share, reported in the second quarter of 2025. The higher net income was due primarily to the higher operating profit and lower stock-based compensation expense, which was partially offset by lower interest and other income, net, and a higher provision for income taxes.

Adjusted EBITDA was $62.1 million, a increase of 7.2% as compared to the $57.9 million reported in the second quarter of 2025, as the higher gross profit was partially offset by planned investments to expand the features and functionality of our platform . Adjusted EBITDA margin was 17.7% as compared to the 17.4% Adjusted EBITDA margin in the second quarter of 2025. Refer to Annex A for a reconciliation of Adjusted EBITDA to net income.

Cash Flow

Net cash provided by operating activities in the second quarter of 2026 was $50.4 million, as compared to $55.5 million provided by operating activities in the prior year period. Cash flow reflects the timing impact of certain working capital items in both periods.

Balance Sheet and Financial Position

As of June 30, 2026, the Company had total working capital of approximately $272.9 million and no debt. This included cash and cash equivalents and marketable securities of $236.9 million, an increase of $11.8 million from the balances as of March 31, 2026 as the operating cash flow generated during the quarter was partially offset by share repurchase activity during the quarter. The Company's $200 million revolving credit facility remains undrawn, and the Company has no planned use for the facility at this time.

Share Repurchase Activity

During the second quarter of 2026, the Company repurchased nearly 1.2 million shares of its common stock for a total cost of $31.5 million through its May 2026 share repurchase program, which provided for a total authorization of up to $200 million. To date, the Company has repurchased a cumulative 2 million shares of its common stock under this most recent program, and approximately $142.5 million remains under the existing authorization. In combination with its predecessor program which began in November 2025 and concluded earlier this year, the Company has now repurchased an aggregate 10.8 million shares under both its May 2026 and November 2025 share repurchase programs.

Key Metrics

The Company had 604 fertility and family building clients as of June 30, 2026, as compared to 542 clients as of June 30, 2025.

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Assisted Reproductive Treatment (ART) Cycles (*) | 16,998 | 16,938 | 32,645 | 33,098
Utilization - All Members (**) | 0.56% | 0.55% | 0.85% | 0.82%
Utilization - Female Only (**) | 0.49% | 0.48% | 0.71% | 0.69%
Average Members (***) | 7,185,000 | 6,743,000 | 7,176,000 | 6,723,000

* Represents the number of ART cycles performed, including IVF with a fresh embryo transfer, IVF freeze all cycles/embryo banking, frozen embryo transfers, and egg freezing. Includes ART cycles performed in the first half of 2025 under the extended transition of care agreement with the large client who did not renew its service agreement.

** Represents the member utilization rate for all fertility and family building services, including, but not limited to, ART cycles, initial consultations, IUIs, and genetic testing. The utilization rate for all members includes all unique members (female and male) who utilize the benefit during that period, while the utilization rate for female only includes only unique females who utilize the benefit during that period. For purposes of calculating utilization rates in any given period, the results reflect the number of unique members utilizing the benefit for that period. Individual periods cannot be combined as member treatments may span multiple periods. Utilization for 2025 excludes activity under the extended transition of care agreement that ended June 30, 2025 with the large client who did not renew its service agreement, as only members meeting certain criteria were eligible to use the benefit.

***Includes approximately 300,000 members from a single client who are not reflected in utilization as a result of the client's chosen benefit design. 2025 excludes the limited number of members who were eligible to use the benefit under the extended transition of care agreement that ended June 30, 2025 with the large client who did not renew its service agreement.

Financial Outlook

Member engagement typically lessens during the peak of the summer months, and the third quarter guidance reflects a slightly more pronounced seasonal impact on member activity. With our present visibility, activity in September is consistent with the engagement seen over the first half of the year, and this is reflected in the assumptions for the remainder of the year.

The Company is providing the following financial guidance for both the three-month and full year periods ending September 30, 2026.

• Full Year 2026 Outlook:

o Revenue is projected to be $1.360 billion to $1.385 billion, reflecting growth of 5.5% to 7.5%; excluding the $48.5 million of revenue in 2025 from the large client who was under a transition agreement in the first half of 2025, revenue is expected to increase by 9.7% to 11.7%

o Net income is projected to be $104.8 million to $109.9 million, or $1.26 to $1.32 per diluted share, on the basis of approximately 83 million assumed weighted-average fully diluted-shares outstanding

o Adjusted EBITDA 1 is projected to be $233.0 million to $240.0 million

o Adjusted earnings per diluted share 1 is projected to be $2.04 to $2.10

• Third Quarter of 2026 Outlook:

o Revenue is projected to be $335.0 million to $345.0 million, reflecting growth of 6.9% to 10.1%

o Net income is projected to be $24.5 million to $26.7 million, or $0.30 to $0.33 per diluted share, on the basis of approximately 82 million assumed weighted-average fully diluted-shares outstanding

o Adjusted EBITDA 1 is projected to be $56.0 million to $59.0 million

o Adjusted earnings per diluted share 1 is projected to be $0.50 to $0.52

1. Adjusted EBITDA and Adjusted earnings per diluted share are financial measures that are not required by, or presented in accordance with, GAAP. Please see Annex A of this press release for a reconciliation of forward-looking Adjusted EBITDA to forward-looking net income and Adjusted net income to net income, the most directly comparable financial measures stated in accordance with GAAP, for the period presented.

Conference Call Information

Progyny will host a conference call at 4:45 P.M. Eastern Time (1:45 P.M. Pacific Time) today, August 6, 2026, to discuss its financial results. Interested participants from the United States may join by calling 1.866.825.7331 and using conference ID 265484. Participants from international locations may join by calling 1.973.413.6106 and using the same conference ID. A replay of the call will be available until August 13, 2026 at 5:00 P.M. Eastern Time by dialing 1.800.332.6854 (U.S. participants) or 1.973.528.0005 (international) and entering passcode 265484. A live audio webcast of the call and subsequent replay will also be available through the Events & Presentations section of the Company's Investor Relations website at investors.progyny.com.

About Progyny

Progyny (Nasdaq: PGNY) is a global leader in women's health and family building solutions, trusted by the nation's leading employers, health plans and benefit purchasers. We envision a world where everyone can realize their dreams of family and ideal health. Our outcomes prove that comprehensive, inclusive and intentionally designed solutions simultaneously benefit employers, patients, and physicians.

Our benefits solution empowers patients with concierge support, coaching, education, and digital tools; provides access to a premier network of fertility and women's health specialists who use the latest science and technologies; drives optimal clinical outcomes; and reduces healthcare costs.

Headquartered in New York City, Progyny has been recognized for its leadership and growth as a TIME100 Most Influential Company, CNBC Disruptor 50, Modern Healthcare's Best Places to Work in Healthcare, Forbes' Best Employers, Financial Times Fastest Growing Companies, INC. 5000, INC. Power Partners and Crain's Fast 50 for NYC. For more information, visit www.progyny.com.

Investors:

James Hart

investors@progyny.com

Media:

Alexis Ford

media@progyny.com

PROGYNY, INC.

Consolidated Balance Sheets

(Unaudited)

(in thousands, except share and per share amounts)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-27_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Executive Overview

We are a benefits management company specializing in fertility, family building, and women's health benefits solutions primarily in the United States. For further information on our business and strategy, see Part I, Item 1. "Business" of this Annual Report on Form 10-K.

Revenue Model

Fertility Benefits Solution . Our fertility benefits solution includes providing members with access to effective and cost-efficient fertility treatments through our Smart Cycle plan design. Smart Cycles are proprietary treatment bundles designed by us to include those medical services available to our members through our selective network of high-quality fertility specialists. Medical services under our Smart Cycles include everything needed for a comprehensive fertility treatment cycle, including all necessary diagnostic testing and access to the latest technology (such as preimplantation genetic testing, in the case of in vitro fertilization, or IVF). We currently offer 20 different Smart Cycle treatment bundles, which may be used in various combinations depending on the member's need. Each Smart Cycle treatment bundle has a separate unit value (i.e., some have fractional values and some have whole values). Our clients contract to purchase a cumulative Smart Cycle unit value per eligible member. These can range from one to an unlimited unit value. Members, in consultation with their Progyny Care Advocates, or PCAs, can choose their preferred provider clinics within our network and utilize the specific Smart Cycle treatment bundles necessary for the treatment pathway they determine throughout their fertility journey.

In addition, we provide care management services as part of our fertility benefits solution, which include active management of our selective network of high-quality fertility specialists, real-time member eligibility and treatment authorization, member-facing digital solutions, detailed quarterly reporting for our clients supported by our dedicated client success teams and end-to-end comprehensive concierge member support provided by our in-house staff of PCAs. Clients can also add adoption and surrogacy reimbursement programs as part of this solution.

Pharmacy Benefits Solution . Progyny Rx can only be purchased by clients that purchase our fertility benefits solution. Progyny Rx provides our members with access to the medications needed during their fertility treatment. As part of this solution, we provide care management services, which include our formulary plan design, simplified authorization, assistance with prescription fulfillment and timely delivery of the medications by our network of specialty pharmacies, as well as medication administration training, pharmacy support services and continuing PCA support.

Our clients primarily contract with us to provide our fertility benefits solution and, where added on by our clients, our Progyny Rx solution. Our revenue has both a utilization-based component and a population-based component, as follows:

• Utilization Component. Clients pay us for the fertility benefits and Progyny Rx solutions utilized by their employees. With respect to the fertility benefits solution, we bill clients for Smart Cycles in accordance with our bundled case rates, which vary by the type of fertility service rendered and clinic location. Case rates include all third-party fertility specialists, anesthesiology and laboratory services, as well as all of our care management services. With respect to Progyny Rx, we bill the client for the fertility medication dispensed to their employees in connection with the authorized fertility treatments. Medication fees also include our formulary management, drug utilization review and cost containment services and other care management services.

• Population-Based Component. Clients who purchase our fertility benefits solution also typically pay us a per employee per month fee, or PEPM fee, which is population-based. This allows us to provide members with access to our PCAs for fertility and family building education and guidance and other digital tools to all of our members, regardless of whether they ultimately pursue fertility treatment. PEPM fees represented 1% of our total revenue for the years ended December 31, 2025 and 2024, respectively.

Our revenue in a given year is determined by the utilization, including rate of consumption and mix, of our fertility benefits and Progyny Rx solutions by our members as well as the number of members enrolled in our clients' benefits plans. Each year, we contract with new clients for our fertility benefits and Progyny Rx solutions. Given that the majority of our clients contract with us for a January 1 st benefits plan start date, our sales cycle follows the conventional healthcare benefits cycle, which largely concludes by the end of October of the prior year to allow for benefits education and annual open enrollment to occur in November. For some clients that are considering a start date later in the year, the sales cycle can extend through the next year. Similarly, for existing clients, any changes in plan designs are typically elected by the end of October so that clients can inform their employees of the benefits during the open enrollment period ahead of a January 1 st plan year start.

We continue to expand our women's health and family building solutions to include pregnancy and postpartum, menopause and midlife, benefit and leave navigation, and parent and child wellbeing solutions. While these offerings represent strategic areas of investment, they were not a significant portion of our revenue for the years ended December 31, 2025 and 2024.

Key Operational and Business Metrics

In addition to the measures presented in our consolidated financial statements, we use the following key operational and business metrics to evaluate our business, measure our performance, develop financial forecasts, and make strategic decisions.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following tables set forth our results of operations for the periods presented and as a percentage of revenue for those periods:

Year Ended December 31,
2025 | 2024
(in thousands)
Consolidated Statements of Operations Data:
Revenue | 1,288,661 | 1,167,221
Cost of services (1) | 984,177 | 913,858
Gross profit | 304,484 | 253,363
Operating expenses:
Sales and marketing (1) | 72,113 | 63,948
General and administrative (1) | 147,094 | 121,960
Total operating expenses | 219,207 | 185,908
Income from operations | 85,277 | 67,455
Interest and other income, net | 10,155 | 15,747
Income before income taxes | 95,432 | 83,202
Provision for income taxes | 36,912 | 28,866
Net income | 58,520 | 54,336
Adjusted EBITDA (2) | 222,092 | 198,760

(1) Includes stock-based compensation expense as follows:

Year Ended December 31,
2025 | 2024
Cost of services | 35,332 | 36,799
Sales and marketing | 30,702 | 30,490
General and administrative | 65,833 | 60,841
Total stock‑based compensation expense | 131,867 | 128,130

(2) Adjusted EBITDA is a non-GAAP financial measure that we define as net income, adjusted to exclude depreciation and amortization, stock-based compensation expense, interest and other income, net, and provision for income taxes. See "Management's Discussion and Analysis of Financial Condition and Result of Operations – Non-GAAP Financial Measure – Adjusted EBITDA" below for a reconciliation of Adjusted EBITDA to net income, the most directly comparable measure calculated in accordance with U.S. GAAP.

Year Ended December 31,
2025 | 2024
Consolidated Statements of Operations Data, as a percentage of revenue:
Revenue | 100.0 | % | 100.0 | %
Cost of services | 76.4 | % | 78.3 | %
Gross profit | 23.6 | % | 21.7 | %
Operating expenses:
Sales and marketing | 5.6 | % | 5.5 | %
General and administrative | 11.4 | % | 10.4 | %
Total operating expenses | 17.0 | % | 15.9 | %
Income from operations | 6.6 | % | 5.8 | %
Interest and other income, net | 0.8 | % | 1.3 | %
Income before income taxes | 7.4 | % | 7.1 | %
Provision for income taxes | 2.9 | % | 2.5 | %
Net income | 4.5 | % | 4.6 | %
Adjusted EBITDA | 17.2 | % | 17.0 | %
Note: percentages shown in the table may not foot due to rounding.

Non-GAAP Financial Measure – Adjusted EBITDA

Adjusted EBITDA is a supplemental financial measure that is not required by, or presented in accordance with U.S. GAAP. We believe that Adjusted EBITDA, when taken together with our U.S. GAAP financial results, provides meaningful supplemental information regarding our operating performance and facilitates internal comparisons of our historical operating performance on a more consistent basis by excluding certain items that may not be indicative of our business, results of operations, or outlook. In particular, we believe that the use of Adjusted EBITDA is helpful to our investors as it is a measure used by management in assessing the health of our business, determining incentive compensation, evaluating our operating performance, and for internal planning and forecasting purposes.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-27_item1_business.md)

ITEM 1. BUSINESS

Overview

Progyny is a global leader in women's health and family building solutions. We envision a world where everyone can realize their dreams of family and ideal health. Our mission is to empower healthier, supported journeys through transformative fertility, family building and women's health benefits. Through our differentiated approach to benefits plan design, member education and support and active network management, our clients' employees are able to pursue the most effective treatment across life's milestones from the best providers and specialists and achieve optimal outcomes.

We launched our fertility benefits solution in 2016 with five employer clients and have since expanded our platform to include solutions in pregnancy and postpartum, menopause and midlife, benefit and leave navigation and parent and child wellbeing in order to address the continuum of women's health. Today, we have grown our current base of clients to more than 590 employers, each with at least 1,000 covered lives. Our clients include many of the nation's most prominent employers across a broad array of industries. We currently have contracts to provide coverage to approximately 7.2 million employees and their covered dependents (known in our industry as covered lives, and to whom we refer to as our members). We have achieved this growth by demonstrating that our purpose-built, data-driven and disruptive platform consistently delivers superior clinical outcomes in a cost-efficient manner, while driving exceptional client and member satisfaction. We have retained substantially all of our clients since we launched our fertility benefits solution, and our member satisfaction is evidenced by our most recent industry-leading Net Promoter Score, or NPS, of +81 for our fertility benefits solution and +79 for Progyny Rx, our integrated pharmacy benefits solution, as of December 31, 2025.

We are transforming women's health benefits, proving that comprehensive, inclusive, and intentionally designed solutions can simultaneously benefit employers, members and providers. We believe the value proposition we deliver to all of these constituents is key to our success and growth. Our solutions empower members with concierge support, coaching, education, and digital tools; provide access to a premier network of fertility and women's health specialists who use the latest science and technologies; drive optimal clinical outcomes; and reduce healthcare costs.

Market Opportunity

We believe we have a significant opportunity to provide employers with a superior comprehensive solution that addresses the unique challenges and complexities of women's health and family building benefits. We estimate that the market for women's health and family building benefits in the United States will continue to grow, especially as current estimates of the market exclude those individuals who do not have access to a comprehensive family building benefit and, as a result, do not seek treatment for infertility.

We contract with employers to provide women's health and family building benefits to their employees and covered dependents. We believe our addressable market primarily consists of large self-insured employers as well as labor populations under the Labor Management Relations Act of 1947 (also known as the Taft-Hartley Act) and federal government populations. There are approximately 9,000 employers in the United States who have a minimum of 1,000 employees, who together with the Taft-Hartley populations and federal government populations, represent approximately 106 million potential covered lives in total. As such, we estimate that our current member base of 7.2 million covered lives under contract represents a mid-single digit percent of our total market opportunity.

As part of our growth strategy, we anticipate expanding our addressable market to include large group fully insured employers. Overall, we believe our market opportunity is substantial and is continuing to grow as a result of the rising demand for women's health and family building benefits solutions, the lack of adequate offerings in the market today and the increased awareness of the challenges of women's health that we are helping to drive.

Solutions

We are redefining women's health and family building benefits through our purpose-built, data-driven and disruptive platform through which we offer our benefits solutions. Our innovative and comprehensive solutions have proven to be simultaneously beneficial for our clients, our members and our network of providers and specialists. Through our differentiated approach to benefits plan design, member education and support and active network management, our clients' employees are able to pursue the most effective treatment from the best providers and specialists and achieve optimal outcomes in a cost-efficient manner, while our clients and members achieve savings in upfront treatment costs as well as reduced maternity and neonatal intensive care unit, or NICU, expenses.

Fertility Benefits Solution

Differentiated Benefits Plan Design

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

- **CALL PERIOD: 2026Q2** (no event date from the source; file dated 2026-09-05 when retrieved — judge recency by the call period)
- **Recency:** no earnings release to compare against.
- **File:** transcript_2026Q2_2026-09-05.md
- **Type:** REAL CALL TRANSCRIPT / PREPARED REMARKS — management's own words
- **Source:** https://www.alphavantage.co/documentation/#transcript

**Operator** — *Operator*

Good day, ladies and gentlemen, and welcome to the Progyny Inc. Second Quarter 2026 Earnings Conference Call. At this time, all participants are on a listen-only mode. The floor will be open for questions and comments after the presentation. If you wish to join the queue at any time to ask a question, you can press star 1 on your telephone keypad. Should you wish to remove yourself from queue, you can press star 2. It is now my pleasure to turn the call over to your host, James Hart. James, the floor is yours.

**James Hart** — *Head of Investor Relations*

Thank you, Tom, and good afternoon, everyone. Welcome to our second quarter conference call. With me today are Peter Anevski, Chief Executive Officer of Progyny, and Mark S. Livingston, Chief Financial Officer. We will begin with some prepared remarks before we open the call for your questions. Before we begin, I would like to remind you that our comments and responses to your questions today reflect management's views as of today only. We will include statements related to our financial outlook for both the third quarter and full-year 2026 and the assumptions and drivers underlying such guidance, the demand for our solutions, our expectations for our selling season for 2027 launches, anticipated employment levels of our clients in the industries that we serve, the timing of client decisions, our expected utilization rates and mix, the potential benefits of our solution, our ability to acquire new clients and retain and upsell existing clients, our market opportunity, and our business strategy, plans, goals, and expectations concerning our market position, future operations, and other financial and operating information. These are forward-looking statements under the federal securities laws. Actual results may differ materially from those contained in or implied by these forward-looking statements due to risks and uncertainties associated with our business as well as other important factors. For a discussion of the material risks, uncertainties, assumptions, and other important factors that could impact our actual results please refer to our SEC filings and today's press release, both of which can be found on our Investor Relations website. Any forward-looking statements that we make on this call are based on assumptions as of today, and we undertake no obligation to update these statements as a result of new information or future events. During the call, we will also refer to non-GAAP financial measures such as adjusted EBITDA. More information about these non-GAAP financial measures including reconciliations with the most comparable GAAP measures are available in the press release, which is available at investors.progyny.com. I would now like to turn the call over to Peter.

**Peter Anevski** — *Chief Executive Officer*

_[...truncated at ~3,000 chars of this document]_

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-27_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-27_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-27_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-27_item7_mdna.md, 10-K_2026-02-27_item1_business.md, transcript_2026Q2_2026-09-05.md

**Missing:** none

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
