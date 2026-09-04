# Triage pack — CRAI · CRA INTERNATIONAL, INC.

_Generated 2026-09-04 14:02 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** CRAI · **Name:** CRA INTERNATIONAL, INC.
- **CIK:** 0001053706
- **SIC:** 8111 — Services-Legal Services
- **Fiscal year end (MM-DD):** 01-02
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/CRAI

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** CRA INTERNATIONAL, INC.
- **CIK:** 1,053,706 · **SIC:** 8111 (Services-Legal Services) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 172.60 |
| mktcap | $1.1B |
| ev | $1.1B |
| ev_ebit | 12.8x |
| fcf | $18.6M |
| fcf_yield | 1.7% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 40.9% |
| net_debt | -$21.4M |
| net_debt_ebit | -0.3x |
| cash | $21.4M |
| ltd | $0.00 |
| equity | $181.8M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $751.6M |
| revenue_prior | $687.4M |
| rev_growth | 9.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $83.1M |
| net_income | $54.8M |
| cfo | $22.4M |
| capex | $3.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -4.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 6,276,860 |
| shares_py | 6,584,093 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -8.2% |
| r6m | -5.9% |
| off_52w_high | -21.9% |
| adv20 | $20.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.29 |
| r_ev_ebit | 0.67 |
| r_roic | 0.97 |
| r_rev_growth | 0.64 |
| r_buyback | 0.87 |
| score | 0.69 |

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
| rank | 70 |

**Screen rationale:** high ROIC 40.9%; buying back stock -4.7%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **6,276,860** (CY2026Q2I) vs **6,584,093** prior year (CY2025Q2I)
- Change: **-4.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-04-02** — Item 5.02 (officer / director change or comp arrangement): the board of directors (the "Board") of CRA International, Inc. (the "Company") that he will be retiring

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 9,838 sh / $1,700,263 -> net $-1,700,263 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 22 (open-market buys 0, sales 8).

| code | rows |
|---|---|
| A | 6 |
| D | 2 |
| F | 2 |
| M | 4 |
| S | 8 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Highlights for Second Quarter Fiscal 2026'; skipped 19 forward-looking-statement block(s); 12 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (craiq2-20268xkexx991xpress.htm)

Highlights for Second Quarter Fiscal 2026

• Revenue grew 12.8% year over year to $210.8 million.

• Utilization was 77% and quarter-end headcount increased 3.3% year over year.

• Net income increased 11.4% year over year to $13.5 million, or 6.4% of revenue, compared with $12.1 million, or 6.5% of revenue, in the second quarter of fiscal 2025; non-GAAP net income increased 9.0% year over year to $13.9 million, or 6.6% of revenue, compared with $12.7 million, or 6.8% of revenue, in the second quarter of fiscal 2025.

• Earnings per diluted share increased 17.3% year over year to $2.10 from $1.79 in the second quarter of fiscal 2025; non-GAAP earnings per diluted share increased 14.9% year over year to $2.16 from $1.88 in the second quarter of fiscal 2025.

• Non-GAAP EBITDA increased 15.3% to $26.8 million, or 12.7% of revenue, compared with $23.3 million, or 12.4% of revenue, in the second quarter of fiscal 2025.

• On a constant currency basis relative to the second quarter of fiscal 2025, revenue would have been lower by $0.4 million, while GAAP net income, and earnings per diluted share would have remained unchanged. Non-GAAP net income would have been lower by $0.1 million, while non-GAAP earnings per diluted share and non-GAAP EBITDA would have remained unchanged.

• CRA returned $31.4 million of capital to its shareholders, consisting of $3.6 million of dividend payments and $27.8 million for share repurchases of approximately 193,000 shares at an average price of $144 per share.

Management Commentary and Financial Guidance

"Through the first two quarters of fiscal 2026, on a constant currency basis relative to fiscal 2025, CRA generated total revenue of $408.8 million and non-GAAP EBITDA of $49.7 million, achieving a margin of 12.2%. These revenue and profit dollars represent the highest first-half performance in CRA's history," said Maleh. "Reflecting the strong start to the year, we are raising our revenue guidance and reaffirming our profit margin guidance. For full-year fiscal 2026, on a constant currency basis relative to fiscal 2025, we expect revenue in the range of $805 million to $820 million and non-GAAP EBITDA margin in the range of 12.0% to 13.0%. This new revenue guidance compares with a prior range of $785 million to $805 million."

"We expect that the constant currency adjustment will decrease CRA's reported annual revenue by approximately $2.5 million and will decrease CRA's reported annual EBITDA by less than $250,000 for fiscal 2026. As previously reported, non-cash forgivable loan amortization, which is reflected as an expense when presenting EBITDA metrics, is expected to increase in fiscal 2026 by approximately $15 million, reflecting investments in talent to drive profitable growth. Finally, as a reminder, fiscal 2026 returns to CRA's typical 52-week year, whereas fiscal 2025 contained an extra week in the fourth quarter and resulted in a 53-week year. We are encouraged by the strong start to the year, and by supportive market trends, and a continued replenishing of our sales pipeline. Of course, we remain mindful that evolving geopolitical, global macroeconomic, and business conditions can affect our business."

CRA does not provide reconciliations of its annual non-GAAP EBITDA margin guidance to GAAP net income margin because the Company is unable to estimate with reasonable certainty and without unreasonable effort: (i) unusual gains or charges, foreign currency exchange rates and the resulting effect of these items on CRA's taxes and (ii) the impact of equity awards on CRA's taxes. These items are uncertain, depend on various factors, and may have a material effect on CRA's results computed in accordance with GAAP. A reconciliation between the historical GAAP and non-GAAP financial measures presented in this press release is provided in the financial tables at the end of this press release.

Credit Facility

On August 6, 2026, CRA announced the successful refinancing to increase and extend its existing credit facility as it approached the final year before maturity. The expanded facility will run for five years with an aggregate principal amount of up to $400 million, consisting of a $75 million term loan and a $325 million revolving credit facility. The revolving credit facility includes a seasonal flex that provides CRA with the option to reduce the facility by $75 million during periods when working capital demands are typically lower.

Quarterly Dividend

On August 6, 2026, CRA announced a quarterly cash dividend of $0.57 per common share, payable on September 14, 2026 to shareholders of record as of August 25, 2026. CRA expects to continue paying quarterly dividends, the declaration, timing and amounts of which remain subject to the discretion of CRA's Board of Directors.

Conference Call Information and Prepared CFO Remarks

CRA will host a conference call today at 10:00 a.m. ET to discuss its second-quarter 2026 financial results. To listen to the live call, please visit the " Investor Relations " section of CRA's website at http://www.crai.com , or dial (877) 709-8155 or (201) 689-8881. An archived version of the webcast will be available on CRA's website for one year.

In combination with this press release, CRA has posted prepared remarks by its CFO, Eric Nierenberg, under "Quarterly Earnings" in the " Investor Relations " section on CRA's website at http://www.crai.com . These remarks are offered each quarter to provide the investment community with additional background on CRA's financial results prior to the start of the conference call.

About Charles River Associates (CRA)

Charles River Associates® is a leading global consulting firm specializing in economic, financial, and management consulting services . CRA advises clients on economic and financial matters pertaining to litigation and regulatory proceedings, and guides corporations through critical business strategy and performance-related issues. Since 1965, clients have engaged CRA for its unique combination of functional expertise and industry knowledge, and for its objective solutions to complex problems. Headquartered in Boston, CRA has offices throughout the world. Detailed information about Charles River Associates, a registered trade name of CRA International, Inc., is available at www.crai.com . Follow us on LinkedIn , Instagram , and Facebook .

NON-GAAP FINANCIAL MEASURES

In this press release, CRA has supplemented the presentation of its financial results calculated in accordance with U.S. generally accepted accounting principles or "GAAP" with the following financial measures that are not calculated in accordance with GAAP: non‑GAAP net income, non‑GAAP earnings per diluted share, non‑GAAP EBITDA and non-GAAP EBITDA margin. CRA believes that the non-GAAP financial measures described in this press release are important to management and investors because these measures supplement the understanding of CRA's ongoing operating results and financial condition. In addition, these non-GAAP measures are used by CRA in its budgeting process, and the non-GAAP adjustments are made to the performance measures for some of CRA's performance-based compensation.

As used herein, CRA defines non-GAAP EBITDA as net income before interest expense (net), provision for income taxes, and depreciation and amortization further adjusted for the impact of certain items that we do not consider indicative of our core operating performance, such as non-cash amounts relating to valuation changes in contingent consideration, acquisition-related costs, foreign currency (gains) losses, net, restructuring costs and related tax effects. Non-GAAP net income and non-GAAP earnings per diluted share also exclude non-cash amounts relating to valuation changes in contingent consideration, acquisition-related costs, foreign

currency (gains) losses, net, restructuring costs and related tax effects. This press release also presents certain current fiscal period financial measures on a "constant currency" basis in order to isolate the effect that foreign currency exchange rate fluctuations can have on CRA's financial results. These constant currency measures are determined by recalculating the current fiscal period local currency financial measure using the specified corresponding prior fiscal period's foreign exchange rates. On a constant currency basis for the fiscal year-to-date period ended July 4, 2026 relative to the fiscal year-to-date period ended June 28, 2025, revenue and non-GAAP EBITDA would have been lower by $3.0 million and $0.3 million, respectively.

All of the non-GAAP financial measures referred to above should be considered in conjunction with, and not as a substitute for, the GAAP financial information presented in this press release. The financial measures identified in this press release as "non-GAAP" are reconciled to their GAAP comparable measures in the financial tables appended to the end of this press release. In evaluating these non-GAAP financial measures, note that the non-GAAP financial measures used by CRA may be calculated differently from, and therefore may not be comparable to, similarly titled measures used by other companies.

CRA INTERNATIONAL, INC.

RECONCILIATION OF NON-GAAP FINANCIAL MEASURES

FOR THE FISCAL QUARTERS ENDED

JULY 4, 2026 COMPARED TO JUNE 28, 2025

(IN THOUSANDS, EXCEPT PER SHARE DATA)

Fiscal Quarter Ended | Fiscal Year-to-Date Period Ended
July 4, 2026 | As a % of Revenue | June 28, 2025 | As a % of Revenue | July 4, 2026 | As a % of Revenue | June 28, 2025 | As a % of Revenue
Revenues | 210,815 | 100.0 | % | 186,878 | 100.0 | % | 411,790 | 100.0 | % | 368,729 | 100.0 | %
Net income | 13,508 | 6.4 | % | 12,122 | 6.5 | % | 24,640 | 6.0 | % | 30,124 | 8.2 | %
Adjustments needed to reconcile GAAP net income to non-GAAP net income:
Restructuring and other (1)(2) | — | — | % | — | — | % | 1,759 | 0.4 | % | (4,170) | -1.1 | %
Foreign currency (gains) losses, net | 467 | 0.2 | % | 815 | 0.4 | % | 88 | — | % | 1,290 | 0.3 | %
Tax effect on adjustments (1) | (107) | -0.1 | % | (214) | -0.1 | % | 479 | 0.1 | % | 733 | 0.2 | %
Non-GAAP net income | 13,868 | 6.6 | % | 12,723 | 6.8 | % | 26,966 | 6.5 | % | 27,977 | 7.6 | %
Non-GAAP net income per share:
Basic | 2.19 | 1.90 | 4.20 | 4.15
Diluted | 2.16 | 1.88 | 4.14 | 4.10
Weighted average number of shares outstanding:
Basic | 6,348 | 6,694 | 6,430 | 6,734
Diluted | 6,407 | 6,753 | 6,498 | 6,807
(1) Fiscal year-to-date period ended July 4, 2026 includes cash severance of $1.6 million and non-cash charges of $1.0 million associated with portfolio optimization actions.
(2) Fiscal year-to-date period ended June 28, 2025 includes $1.2 million of restructuring charges, net of the reversal of $5.4 million of non-cash charges associated with a previously recorded performance award.

CRA INTERNATIONAL, INC.

RECONCILIATION OF NON-GAAP FINANCIAL MEASURES

FOR THE FISCAL QUARTERS ENDED

JULY 4, 2026 COMPARED TO JUNE 28, 2025

(IN THOUSANDS)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

We are a leading worldwide economic, financial, and management consulting firm that applies advanced analytic techniques and in-depth industry knowledge to complex engagements for a broad range of clients.

We derive revenues principally from professional services rendered by our employee consultants. In most instances, we charge clients on a time-and-materials basis and recognize revenues in the period when we provide our services. We charge consultants' time at hourly rates, which vary from consultant to consultant depending on a consultant's position, experience, expertise, and other factors. We derive a portion of our revenues from fixed-price engagements. Revenues from fixed-price engagements are recognized using a proportional performance method based on the ratio of costs incurred to the total estimated project costs. We generate substantially all of our professional services fees from the work of our own employee consultants and a portion from the work of our non-employee experts. Factors that affect our professional services revenues include the number and scope of client engagements, the number of consultants we employ, the consultants' billing rates, and the number of hours our consultants work. Revenues also include reimbursements for costs we incur in fulfilling our performance obligations, including travel and other out-of-pocket expenses, fees for outside consultants and other reimbursable expenses.

Our costs of services include the salaries, bonuses, share-based compensation expense, forgivable loan amortization, and benefits of our employee consultants. Our bonus program awards discretionary bonuses based on our revenues and profitability and individual performance. Costs of services also include out-of-pocket and other third-party vendor expenses, and the salaries of support staff whose time is billed directly to clients, such as librarians, editors, and programmers, as well as the amounts billed to us by our outside consultants for services rendered while completing a project. Costs of services does not include depreciation and amortization. Selling, general and administrative expenses include salaries, bonuses, share-based compensation expense, and benefits of our administrative and support staff, commissions to non-employee experts for generating new business, office rent, marketing, and other operating costs.

Utilization and Seasonality

We derive the majority of our revenues from the number of hours worked by our employee consultants. Our utilization of those employee consultants is one key indicator that we use to measure our operating performance. We calculate utilization by dividing the total hours worked by our employee consultants on engagements during the measurement period by the total number of hours that our employee consultants were available to work during that period. Utilization was 77%, 75%, and 70% for fiscal 2025, fiscal 2024, and fiscal 2023, respectively.

We experience certain seasonal effects that impact our revenue. Concurrent vacations or holidays taken by a large number of consultants can adversely impact our revenue. For example, we usually experience fewer billable hours in our fiscal third quarter, as that is the summer vacation season for most of our offices, and in our fiscal fourth quarter, as that is the quarter that typically includes the December holiday season. In addition, much of our junior staff hiring occurs in our fiscal third quarter during which our new colleagues receive training and become acclimated to the organization. As a result, utilization may be impacted for the latter half of the year.

International Operations

Revenues outside of the U.S. accounted for approximately 20% of our total revenues in fiscal 2025, 19% of our total revenues in fiscal 2024, and 21% of our total revenues in fiscal 2023. Revenue by country is detailed in Note 2 to our Notes to Consolidated Financial Statements.

Critical Accounting Policies and Estimates

The discussion and analysis of our financial condition and results of operations are based upon our consolidated financial statements, which have been prepared in accordance with accounting principles generally accepted in the United States of America. The preparation of these financial statements requires us to make significant estimates and judgments that affect the reported amounts of assets and liabilities, as well as related disclosure of contingent assets and liabilities, at the date of the financial statements, and the reported amounts of revenues and expenses during the reporting period. These estimates are monitored and analyzed by management for changes in facts and circumstances, and material changes in these estimates could occur in the future. Changes in estimates are recorded in the period in which they become known. We base our estimates on historical experience and various other assumptions that we believe to be reasonable under the circumstances. Actual results may differ from our estimates if our assumptions based on past experience or our other assumptions do not turn out to be substantially accurate.

Our significant accounting policies are discussed in Note 1 in our Notes to Consolidated Financial Statements. A summary of the accounting policies that we believe are most critical to understanding and evaluating our financial results is set forth below. We believe the following accounting policies involve our more subjective and complex judgments that have the most significant potential impact to the presentation of our financial statements. This summary should be read in conjunction with our consolidated financial statements and the related notes included in Item 8 of this annual report on Form 10-K.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

The following table provides operating information as a percentage of revenues for the periods indicated:

Fiscal Year Ended
January 3, 2026 (53 weeks) | December 28, 2024 (52 weeks) | December 30, 2023 (52 weeks)
Revenues | 100.0 | % | 100.0 | % | 100.0 | %
Costs of services (exclusive of depreciation and amortization) | 69.1 | 69.8 | 70.5
Selling, general and administrative expenses | 18.0 | 18.2 | 18.4
Depreciation and amortization | 1.9 | 1.7 | 1.9
Income from operations | 11.1 | 10.3 | 9.2
Interest expense, net | (0.7) | (0.6) | (0.6)
Foreign currency gains (losses), net | (0.2) | — | (0.2)
Income before provision for income taxes | 10.2 | 9.6 | 8.4
Provision for income taxes | 2.9 | 2.8 | 2.2
Net income | 7.3 | % | 6.8 | % | 6.2 | %

Fiscal 2025 Compared to Fiscal 2024

Our fiscal year end is the Saturday nearest December 31 of each year. Our fiscal years periodically contain 53 weeks rather than 52 weeks. Fiscal 2025 was a 53-week year, and fiscal 2024 was a 52-week year.

Revenues. Revenues increased by $64.2 million, or 9.3%, to $751.6 million for fiscal 2025 from $687.4 million for fiscal 2024. Utilization increased to 77% for fiscal 2025 from 75% for fiscal 2024, while consultant headcount increased by 13 consultants during fiscal 2025. Billable hours increased by 6.0% for fiscal 2025 when compared to fiscal 2024.

Overall, revenues outside of the U.S. increased to 20% of net revenues for fiscal 2025 from 19% for fiscal 2024. Revenues derived from fixed-price engagements decreased to 17% of net revenues for fiscal 2025 from 18% for fiscal 2024. Revenues derived from time-and-materials engagements increased to 83% of net revenues for fiscal 2025 from 82% for fiscal 2024. The percentages of revenue derived from fixed-price engagements depends largely on the proportion of our revenues

derived from our management consulting business, which typically has a higher concentration of fixed-price service engagements.

Costs of Services (exclusive of depreciation and amortization). Costs of services (exclusive of depreciation and amortization) increased by $39.4 million, or 8.2%, to $519.3 million for fiscal 2025 from $479.9 million for fiscal 2024. The increase in costs of services was due primarily to an increase of $35.8 million in employee compensation and fringe benefit costs, and an increase of $6.3 million of client reimbursable indirect project expenses in fiscal 2025 compared to fiscal 2024. These increases were partially offset by a decrease in forgivable loan amortization of $2.6 million and a decrease of $0.1 million in expense related to miscellaneous and other expenses in fiscal 2025 compared to fiscal 2024. As a percentage of net revenue, costs of services decreased to 69.1% for fiscal 2025 as compared to 69.8% for fiscal 2024.

Selling, General and Administrative Expenses. Selling, general and administrative expenses increased by $9.9 million, or 7.9%, to $135.0 million for fiscal 2025 from $125.1 million for fiscal 2024. This increase was due primarily to a $3.5 million increase in legal and professional services, a $2.4 million increase in employee compensation and fringe benefit costs, a $1.5 million increase in rent expense, a $1.5 million increase in travel and entertainment expenses, a $1.1 million increase in other operating expenses, and a $0.8 million increase in software subscription and data services. These increases were partially offset by a $0.9 million decrease in commissions to our non-employee experts.

As a percentage of revenues, selling, general and administrative expenses decreased to 18.0% for fiscal 2025 from 18.2% for fiscal 2024. Commissions to non-employee experts decreased to 1.8% of revenue in fiscal 2025 compared to 2.1% of revenues in fiscal 2024.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business

Unless otherwise indicated or required by the context, when we use the terms "CRA", "the Company," "us," "we," or "our" we mean CRA International, Inc., a Massachusetts corporation, and its consolidated subsidiaries.

Company Overview

We are a leading global consulting firm specializing in providing economic, financial and management consulting services. We advise clients on economic and financial matters pertaining to litigation and regulatory proceedings, and guide corporations through critical business strategy and performance-related issues. Since our inception in 1965, we have been engaged by clients for our unique combination of functional expertise and industry knowledge, and for our objective solutions to complex problems. We combine economic and financial analysis with expertise in litigation and regulatory support, business strategy and planning, market and demand forecasting, and policy analysis. We are often retained in high-stakes matters, such as multibillion-dollar mergers and acquisitions, new product introductions, major strategy and capital investment decisions, and complex litigation, the outcomes of which often have significant consequences for the parties involved. These matters often require independent analysis and, as a result, the parties involved must rely on outside experts. Our analytical strength enables us to reach objective, factual conclusions that help clients make important business and policy decisions and resolve critical disputes. Clients turn to us because we can provide highly credentialed and experienced economic and finance experts to address critical, tough assignments, with high-stakes outcomes.

We offer consulting services in two broad areas: litigation, regulatory, and financial consulting and management consulting. We provide our consulting services primarily through our highly credentialed and experienced staff of employee consultants. Our employee consultants have backgrounds in a wide range of disciplines, including economics, business, corporate finance, materials sciences, accounting, and engineering. They combine outstanding intellectual acumen with practical experience and in-depth understanding of industries and markets. To enhance the expertise we provide to our clients, we maintain close working relationships with a select group of renowned academic and industry non-employee experts.

Our business is diversified across multiple dimensions, including service offerings and vertical industry coverage, as well as areas of functional expertise, client base, and geography. We believe this diversification reduces our dependence on any particular market, industry, or geographic area.

We provide consulting services to corporate clients and attorneys in a wide range of litigation and regulatory proceedings, providing high-quality research and analysis, expert testimony, and comprehensive support in litigation and regulatory proceedings in all areas of finance, accounting, economics, insurance, and forensic accounting and investigations. We also use our expertise in economics, finance, and business to offer law firms, businesses, and government agencies services related to class certification, damages analysis, expert reports and testimony, regulatory analysis, antitrust and competition matters, strategy development, forensic accounting, cybersecurity, information security and privacy matters, labor and employment disputes, transfer pricing issues, valuation of tangible and intangible assets, intellectual property litigation and damages, risk management, and transaction support. In our management consulting services, we use our expertise in economics, finance, and business analysis to offer our clients such services as strategy development, performance improvement, corporate strategy and portfolio analysis, estimation of market demand, environmental, social and corporate governance and sustainability strategy and analysis, design and implementation of auction and competitive bidding, new product pricing

strategies, survey and market research, valuation of intellectual property and other assets, assessment of competitors' actions, and analysis of new sources of supply. Our analytical expertise in advanced economic and financial methods is complemented by our in-depth expertise in specific industries, including blockchain, cryptocurrency, and digital assets; communications and media; consumer products, health, and wellness; energy; entertainment and leisure; financial services; healthcare; life sciences; manufacturing and industrials; natural resources; retail and distribution; technology; and transportation.

We have completed thousands of engagements for clients around the world, including domestic and foreign companies; federal, state, and local domestic government agencies; governments of foreign countries; public and private utilities; and national and international trade associations. We also work with many of the world's leading law firms. We experience a high level of repeat business.

We deliver our services through an international network of coordinated offices. Headquartered in Boston, Massachusetts, we have offices throughout the Americas, Europe, and Australia.

Industry Overview

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-26_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-26_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-26_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
