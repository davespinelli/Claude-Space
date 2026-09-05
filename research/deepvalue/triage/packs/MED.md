# Triage pack — MED · MEDIFAST INC

_Generated 2026-09-05 03:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MED · **Name:** MEDIFAST INC
- **CIK:** 0000910329
- **SIC:** 2090 — Miscellaneous Food Preparations & Kindred Products
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MED

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** MEDIFAST INC
- **CIK:** 910,329 · **SIC:** 2090 (Miscellaneous Food Preparations & Kindred Products) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 12.54 |
| mktcap | $140.2M |
| ev | $68.3M |
| ev_ebit | n/a |
| fcf | $1.2M |
| fcf_yield | 0.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -9.0% |
| net_debt | -$71.9M |
| net_debt_ebit | n/a |
| cash | $71.9M |
| ltd | $0.00 |
| equity | $196.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $385.8M |
| revenue_prior | $602.5M |
| rev_growth | -36.0% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$14.2M |
| net_income | -$19.0M |
| cfo | $6.9M |
| capex | $5.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 11,180,703 |
| shares_py | 10,991,064 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -12.0% |
| r6m | 16.1% |
| off_52w_high | -13.9% |
| adv20 | $1.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.25 |
| r_ev_ebit | 0.00 |
| r_roic | 0.13 |
| r_rev_growth | 0.00 |
| r_buyback | 0.34 |
| score | 0.15 |

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
| rank | 475 |

**Screen rationale:** debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **11,180,703** (CY2026Q2I) vs **10,991,064** prior year (CY2025Q2I)
- Change: **1.7%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-01** — Item 5.02 (officer / director change or comp arrangement): Effective as of May 29, 2026, Jason L. Groves, Esq., the Chief Legal Officer & Corporate Secretary of Medifast, Inc. (the "Company"), tendered his resignation from the Company.
- **2026-05-26** — Item 5.02 (officer / director change or comp arrangement): Stockholder Approval of the Amended and Restated 2012 Share Incentive Plan
- **2026-03-20** — Item 1.01 (Entry into a Material Definitive Agreement): On March 19, 2026, Medifast, Inc. (the "Company") and Steamboat Capital Partners LLC and certain of its related persons ("Steamboat") entered into a Cooperation Agreement (the "Cooperation Agreement").
- **2026-03-20** — Item 5.02 (officer / director change or comp arrangement): The information included in Item 1.01 of this Current Report on Form 8-K is incorporated by reference into this Item 5.02.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 124,966 sh / $1,486,752 vs sells 0 sh / $0 -> net $1,486,752 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Kiai Parsa bought 41,975 sh @ $12.26 ($514,748) on 2026-08-26.

Form 4 filings parsed: 12; transaction rows: 27 (open-market buys 10, sales 0).

| code | rows |
|---|---|
| A | 11 |
| F | 6 |
| P | 10 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'BALTIMORE – ( BUSINESS WIRE ) — Medifast (NYSE: MED), the health and w'; skipped 10 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (medq22026earningsrelease.htm)

BALTIMORE – ( BUSINESS WIRE ) — Medifast (NYSE: MED), the health and wellness company known for its science-backed comprehensive metabolic health system, Trilivy, today reported results for the second quarter ended June 30, 2026.

Second Quarter 2026

• Revenue: $76.4 million, with revenue per active earning coach of $6,529

• Independent active earning coaches of 11,700

• Net loss of $3.1 million or $0.28 loss per diluted share ("EPS")

• Cash, Cash Equivalents, and Investment Securities of $169.8 million with no debt

Nick Johnson, Chief Executive Officer, commented, "In the second quarter, we continued to see signs of a turnaround in our business. Revenue remained sequentially stable, supported by steady growth in coach productivity and positive coach leadership trends. Combined with the energy and engagement demonstrated at our recent National Coach Convention, these leading indicators have historically been precursors of future growth.

"We're building on that progress by putting new tools in our coaches' hands, with our new brand, Trilivy, our new Reset Fuelings, and our new Medifast Metabolic Health Institute. Each of these is a meaningful step in our 3.0 strategy. Backed by our Metabolic Synchronization science and coach-led model, we believe we are on track to return to profitability in the fourth quarter and have created a foundation that supports our vision for consistent, long-term growth."

Second Quarter 2026 Results

Second quarter 2026 revenue decreased 27.6% to $76.4 million from $105.6 million for the second quarter of 2025, primarily driven by a decrease in the number of active earning coaches. The total number of active earning coaches decreased 48.7% to 11,700 compared to 22,800 for the second quarter of 2025, primarily driven by continued pressure with client acquisition reflecting broader challenges in the operating environment, including rapid adoption of GLP-1 medications for weight loss. While the company continues its transformation to focus on metabolic health, it expects the number of active earning coaches to continue to decline in 2026. The average revenue per active earning coach was $6,529, compared to $4,630 for the second quarter last year, an increase of 41.0% which was driven by greater alignment of the company's network of coaches, prioritizing productive coaches and more efficient coach network structures.

Gross profit decreased 30.3% to $53.4 million from $76.6 million for the second quarter of 2025. The decrease in gross profi t was due to lower sales volumes. The company's gross profit margin was 69.9% compared to 72.6% in the second quarter of 2025. The decrease in gross profit as a percentage of revenue was primarily driven by the loss of leverage on fixed costs.

Selling, general, and administrative expenses ("SG&A") decreased 25.7% to $57.7 million compared to $77.7 million for the second quarter of 2025. The decrease in SG&A was primarily due to a $12.6 million decrease in coach compensation on lower volume and fewer active earning coaches, a $2.3 million decrease in employee salary and benefit expenses, and a $2.0 million decrease in company-led marketing costs. As a percentage of revenue, SG&A increased 200 basis points year-over-year to 75.6% of revenue, as compared to 73.6% for the second quarter of 2025. The increase in SG&A as a percentage of revenue was primarily due to approximately

290 basis points associated with the loss of leverage on fixed costs and 60 basis points associated with the launch of the company's new Trilivy Reset product line, partially offset by a 190 basis point reduction related to company-led marketing expenses. During Q2 the company launched its Catalyst program with the majority of the execution expected to take place in Q3. The Catalyst program is designed to drive additional cost savings through facility rationalization, AI-related efficiencies and other means.

The company's loss from operations for the period was $4.3 million compared to $1.1 million in the prior year comparable period. As a percentage of revenue, loss from operations was 5.7% for the second quarter of 2026 compared to 1.0% in the prior-year comparable period due to the factors described above impacting revenue and SG&A expenses.

Other income decreased $2.6 million to $1.3 million compared to $3.9 million for the second quarter of 2025 primarily due to gains on the company's investment in LifeMD, Inc. common stock in the prior year period. The company sold its investment in LifeMD during the quarter ended June 30, 2025.

Income tax expense for the period was $0.1 million, an effective rate of negative 3.6%, as compared to $0.4 million for the second quarter of 2025, an effective rate of 13.7%. Due to the existence of a full valuation allowance against its deferred tax assets recorded as of December 31, 2025, the company calculated income tax expense for the current period based on actual results for the quarter. The decrease in the effective tax rate was primarily driven by the increased loss incurred in the June 30, 2026 period and the valuation allowance on the net deferred tax assets.

In the second quarter of 2026, the company's net loss was $3.1 million, or $0.28 per share, based on approximately 11.1 million shares of common stock outstanding compared to a net income of $2.5 million, or $0.22 per share, based on approximately 11.1 million shares of common stock outstanding in the prior year comparable period.

Capital Allocation and Balance Sheet

During the second quarter of 2026, the company executed an amendment to extend the lease and reduce the square footage for the company's Havre de Grace distribution facility, and remeasured its right-of-use asset and corresponding lease liability by $12.5 million and $12.7 million, respectively. This action is in addition to the commencement of the company's new headquarters office space during the first quarter, where the company recorded an initial right-of-use asset and corresponding lease liability of $6.8 million .

The company's balance sheet remains strong with cash, cash equivalents and investment securities of $169.8 million and no debt as of June 30, 2026, compared to $167.3 million in cash, cash equivalents and investment securities and no debt at December 31, 2025. Working capital as defined as current assets less current liabilities as of June 30, 2026 was $160.5 million, compared to $158.7 million of working capital at December 31, 2025.

Outlook

The company expects third quarter 2026 revenue to be in the range of $60 million to $80 million and third quarter 2026 loss per share to be in the range of $0.15 to $0.65. This excludes any one-time costs associated with the execution of the company's Catalyst initiatives. The company expects full year 2026 revenue to be in the range of $270 million to $300 million and full year 2026 loss per share to range from $0.25 to $1.75.

Conference Call Information

The conference call is scheduled for today, Monday, August 3, 2026 at 4:30 p.m. ET. The call will be broadcast live over the Internet, hosted on the Investor Relations section of Medifast's website at www.MedifastInc.com or directly at https://viavid.webcasts.com/starthere.jsp?ei=1768081&tp_key=644d7ae69f and will be archived

online and available through November 3, 2026. In addition, listeners may dial (201) 389-0879 to join via telephone.

A telephonic playback will be available from 8:30 p.m. ET, August 3, 2026, through August 10, 2026. Participants can dial (412) 317-6671 and enter passcode 13761321 to hear the playback.

About Medifast ® :

Medifast (NYSE: MED) is the metabolic health and wellness company known for its science-backed comprehensive metabolic health system, Trilivy. Designed to help address the challenges of metabolic dysfunction, the company's holistic approach integrates science-backed plans and products, personal 1:1 coaching, a supportive community, and behavioral science support to develop healthy habits.

Driven to improve metabolic health through advanced science and comprehensive behavioral support, Medifast has introduced Metabolic Synchronization®, a breakthrough science that targets metabolic dysfunction through a comprehensive system focused on fat loss, lean mass preservation, and long-term health. Trilivy's comprehensive three-part metabolic health system is designed to help people reset their metabolism, refine their health, and renew their lives. By integrating science, coaching, and healthy habits into a single approach, Trilivy helps people look, feel, and live better.

Backed by more than 45 years of clinical heritage, Medifast continues to advance its mission of lifelong transformation through metabolic science and human connection TM . For more information, visit Trilivyhealth.com and Medifastinc.com.

MED-F

(U.S. dollars in thousands, except per share amounts & dividend data)

Three months ended June 30, | Six months ended June 30,
2026 | 2025 | 2026 | 2025
Revenue | 76,384 | 105,555 | 152,428 | 221,283
Cost of sales | 22,988 | 28,911 | 47,276 | 60,395
Gross profit | 53,396 | 76,644 | 105,152 | 160,888
Selling, general, and administrative | 57,723 | 77,710 | 112,774 | 163,217
Loss from operations | (4,327) | (1,066) | (7,622) | (2,329)
Other income
Interest income | 1,347 | 1,369 | 2,726 | 2,671
Other income (expense) | (11) | 2,572 | (36) | 3,059
1,336 | 3,941 | 2,690 | 5,730
Income (loss) before provision for income taxes | (2,991) | 2,875 | (4,932) | 3,401
Provision for income taxes | 109 | 395 | 290 | 1,693
Net income (loss) | (3,100) | 2,480 | (5,222) | 1,708
Earnings (loss) per share - basic | (0.28) | 0.23 | (0.47) | 0.16
Earnings (loss) per share - diluted | (0.28) | 0.22 | (0.47) | 0.15
Weighted average shares outstanding
Basic | 11,135 | 10,991 | 11,071 | 10,970
Diluted | 11,135 | 11,060 | 11,071 | 11,045

MEDIFAST, INC. AND SUBSIDIARIES

CONDENSED CONSOLIDATED BALANCE SHEETS (UNAUDITED)

(U.S. dollars in thousands, except par value)

June 30, 2026 | December 31, 2025
ASSETS
Current Assets
Cash and cash equivalents | 71,910 | 89,303
Inventories, net | 21,181 | 20,228
Investments | 97,911 | 77,970
Income taxes, prepaid | 5,258 | 5,116
Prepaid expenses and other current assets | 5,774 | 9,066
Total current assets | 202,034 | 201,683
Property, plant and equipment, net of accumulated depreciation | 27,980 | 31,230
Right-of-use assets | 24,314 | 7,232
Other assets | 6,073 | 7,828
TOTAL ASSETS | 260,401 | 247,973
LIABILITIES AND STOCKHOLDERS' EQUITY
Current Liabilities
Accounts payable and accrued expenses | 36,406 | 38,359
Current lease obligations | 5,158 | 4,603
Total current liabilities | 41,564 | 42,962
Lease obligations, net of current lease obligations | 22,460 | 6,091
Total liabilities | 64,024 | 49,053
Stockholders' Equity
Common stock, par value $.001 per share: 20,000 shares authorized;
11,181 and 10,991 issued and outstanding
at June 30, 2026 and December 31, 2025, respectively | 11 | 11
Additional paid-in capital | 43,306 | 40,406
Accumulated other comprehensive income | 11 | 234
Retained earnings | 153,049 | 158,269
Total stockholders' equity | 196,377 | 198,920
TOTAL LIABILITIES AND STOCKHOLDERS' EQUITY | 260,401 | 247,973

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-17_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

CONSOLIDATED RESULTS OF OPERATIONS - 2025 COMPARED TO 2024

The following table reflects our Consolidated Statements of Operations for the years ended December 31, 2025 and 2024 (in thousands, except percentages):

2025 | 2024 | $ Change | % Change
Revenue | 385,788 | 602,463 | (216,675) | (36.0)%
Cost of sales | 110,601 | 157,840 | (47,239) | (29.9)%
Gross profit | 275,187 | 444,623 | (169,436) | (38.1)%
Selling, general, and administrative | 289,400 | 441,745 | (152,345) | (34.5)%
Income (loss) from operations | (14,213) | 2,878 | (17,091) | (593.8)%
Other income
Interest income | 5,516 | 4,804 | 712 | 14.8 | %
Other income (expense) | 3,058 | (3,895) | 6,953 | 178.5%
8,574 | 909 | 7,665 | 843.2 | %
Income (loss) before provision for income taxes | (5,639) | 3,787 | (9,426) | (248.9)%
Provision for income taxes | 13,033 | 1,696 | 11,337 | 668.5%
Net income (loss) | (18,672) | 2,091 | (20,763) | (993.0)%
% of revenue
Gross profit | 71.3% | 73.8%
Selling, general, and administrative | 75.0% | 73.3%
Income (loss) from operations | (3.7)% | 0.5%

Revenue: Revenue decreased $216.7 million, or 36.0%, to $385.8 million in 2025 from $602.5 million in 2024. The year-over-year decline in revenue was primarily driven by a decrease in the number of active earning coaches. The total number of active earning coaches for the three months ended December 31, 2025 decreased to 16,100 from 27,100 for the corresponding period in 2024, a decrease of 40.6%. The number of active earning coaches has been trending downward year-over-year since the first quarter of 2023. The decrease in the number of active earning coaches was driven by continued pressure with client acquisition reflecting broader challenges in the operating environment, including rapid adoption of GLP-1 medications for weight loss. The average revenue per active earning coach increased 6.2% to $4,664 for the three months ended December 31, 2025 from $4,391 for the three months ended December 31, 2024. The increase in the revenue per active earning coach for the quarter was driven by greater alignment of our network of coaches, prioritizing productive coaches and efficient coach network structures.

Costs of sales: Cost of sales decreased $47.2 million, or 29.9%, to $110.6 million in 2025 from $157.8 million in 2024. The decrease in cost of sales was primarily driven by an approximately $54.9 million decrease due to lower sales volumes and a $2.6 million decrease due to restructuring of external manufacturing agreements that did not recur in 2025, partially offset by $8.0 million of loss of leverage on fixed costs and $3.0 million of inventory reserves which are primarily related to the reformulation of the Essential product line.

Gross profit: In 2025, gross profit decreased $169.4 million, or 38.1%, to $275.2 million from $444.6 million in 2024. The decrease in gross profit was primarily attributable to lower revenue. As a percentage of sales, gross profit decreased 250 basis points to 71.3% for 2025 from 73.8% for 2024 primarily driven by the loss of leverage on fixed costs.

Selling, general and administrative: Selling, general and administrative ("SG&A") expenses were $289.4 million in 2025, a decrease of $152.3 million, or 34.5%, as compared to $441.7 million in 2024, primarily due to a $85.1 million decrease in

coach compensation due to lower sales volumes and a decrease in the number of active earning coaches, a $13.4 million decrease in company-led marketing related expenses, a $12.5 million decrease for supply chain optimization that did not recur in 2025, a $9.3 million net decrease in employee compensation resulting from the realignment of the employee base to lower revenue levels partially offset by one-time restructuring charges, a $7.5 million decrease for medically supported weight loss expenses that did not recur in 2025, and a $5.7 million decrease in coach event costs. As a percentage of sales, SG&A expenses were 75.0% for 2025 as compared to 73.3% for 2024, primarily due to 340 basis points of loss of leverage on fixed costs and 300 basis points of loss of leverage on employee compensation, partially offset by a 200 basis point decrease due to supply chain optimization that did not recur in 2025, 130 basis points of reduced company-led marketing related expenses, and 120 basis points of medically supported weight loss expenses that did not recur in 2025. SG&A expenses included research and development costs of $4.3 million and $4.6 million for 2025 and 2024, respectively, in connection with the development of new products and programs and clinical research activities.

Income (loss) from operations: Income (loss) from operations in 2025 decreased $17.1 million to a $14.2 million loss from operations, compared to income from operations of $2.9 million in 2024 primarily as a result of decreased gross profit, partially offset by decreased SG&A expenses. Income (loss) from operations as a percentage of sales decreased to a 3.7% loss from operations as a percentage of revenue for 2025 as compared to 0.5% income from operations as a percentage of revenue for 2024 due to the factors described above in the explanations for gross profit and SG&A expenses.

Other income: Other income was $8.6 million in 2025, an increase of $7.7 million, as compared to other income of $0.9 million for the corresponding period in 2024 primarily attributable to the change in the market value of the Company's investment in LifeMD common stock. The Company sold its investment in LifeMD during the quarter ended June 30, 2025.

Provision for income taxes: For 2025, the Company recorded $13.0 million in income tax expense, an effective tax rate of negative 231.1%, as compared to $1.7 million in income tax expense and an effective tax rate of 44.8%, for 2024. The decrease in the effective tax rate for 2025 as compared to 2024 was primarily driven by the 214.0% impact of a valuation allowance on the net deferred tax asset balance, the 34.5% impact of the tax shortfall from stock compensation, and the 23.5% impact of state taxes, partially offset by the 26.2% increase from the impact of research and development tax credits, all of which were magnified by the loss position in the current period versus the near breakeven income position in the prior year.

Net income (loss): Net loss was $18.7 million, or a loss of $1.70 per diluted share, in 2025 as compared to income of $2.1 million, or $0.19 per diluted share, in 2024. The period-over-period changes were driven by the factors described above in the explanations from operations, other income, and provision for income taxes.

Additionally, refer to Item 7: Management's Discussion and Analysis of Financial Condition and Results of Operations in our Annual Report on Form 10-K for the fiscal year ended December 31, 2024 for management's discussion and analysis of financial condition and results of operations for the fiscal year 2024 compared to fiscal year 2023.

Liquidity and Capital Resources

The Company had stockholders' equity of $198.9 million and working capital of $158.7 million at December 31, 2025 compared with $210.1 million and $150.2 million at December 31, 2024. The $11.2 million net decrease in stockholders' equity reflects the $18.7 million net loss for 2025 and $7.6 million for shared-based compensation offset by other equity transactions described in the Consolidated Statements of Changes in Stockholders' Equity included in our consolidated financial statements included in this report. The Company's cash, cash equivalents and investment securities increased to $167.3 million at December 31, 2025 from $162.3 million at December 31, 2024. In December 2023, the Company's board of directors determined to change the Company's capital allocation priorities and discontinued the Company's quarterly cash dividend to support investments in technology and future growth. The decision to declare and pay dividends in the future will depend on general business conditions, the effect of such payments on our financial condition and other factors the Company's board of directors consider relevant.

Net cash provided by operating activities decreased $17.6 million to $6.9 million for 2025 from $24.5 million for 2024 primarily as a result of a $20.8 million decrease in net income and adjustments to reconcile net income to cash provided by operating activities.

Net cash used in investing activities was $7.9 million for 2025 as compared to $26.5 million for 2024. This year-over-year change resulted primarily from a $54.6 million increase in proceeds from sale and maturities of investment securities partially offset by a $37.8 million increase in purchases of investment securities for 2025 as compared to 2024.

Net cash used in financing activities decreased $1.0 million to $0.6 million for 2025 from $1.5 million for 2024. This decrease was primarily due to $0.5 million decrease in cash dividends paid to stockholders and a $0.5 million decrease in net shares repurchased for employee taxes for 2025 as compared to 2024.

The Company is currently investing in new growth initiatives which have the potential to impact liquidity in future periods. The Company's current growth initiatives, which are focused on advancing its breakthrough science and product offerings that reverses metabolic dysfunction, are variable in nature and will be scaled at the discretion of management. We do not believe there is any significant impact on our liquidity or capital resources.

In pursuing its business strategy, the Company may require additional cash for operating and investing activities. The Company expects future cash requirements, if any, to be funded from operating cash flow and financing activities.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-17_item1_business.md)

ITEM 1. BUSINESS

SUMMARY

Medifast, Inc. ("Medifast," the "Company," "we" or "us") is the 40+ year old health and wellness company known for its science-backed, coach-guided lifestyle system. As we enter 2026, the Company is moving from transformation to execution, leveraging its extensive experience in structured weight loss coupled with recent scientific research and enhanced product offerings to address the needs of a broader metabolic health market. Medifast's approach focuses on addressing the root cause of metabolic dysfunction. This strategic shift targets a larger and more sustainable market, focusing on a long-term growth strategy designed to guide the Company over the next decade by aligning science, products, and coaching with increasing demand for new solutions as awareness of metabolic dysfunction grows.

This growth strategy is fueled by improving coach productivity and expanding our coach network. We operate a well-capitalized business with strong effective leadership, a powerful lifestyle solution, and a business model that has impacted over 3 million lives and, for the quarter ended December 31, 2025, had a network of approximately 16,100 active earning independent coaches. Medifast stands at the forefront of evidence-based wellness solutions, and its coach-first model creates significant opportunities for coaches' individual businesses. This is designed to create a "flywheel effect" as new clients join, driving coach productivity, which in turn attracts new active earning coaches, leading to even more new clients and further productivity.

The Company offers a simple, yet comprehensive approach to achieving optimal metabolic health and well-being by empowering individuals to make lasting changes. Through the dedicated support of our coaches, approximately 90% of whom were clients first, our clients are guided through every step of their wellness journey.

Our scientifically developed products and habit creation framework, reinforced by coaches and community support, provide proven health benefits and serve as a promising foundation to develop a comprehensive metabolic health system. We continuously innovate and build upon our scientific and clinical heritage to fulfill our mission of Lifelong Transformation, Making a Healthy Lifestyle Second Nature ® . Coaches provide unparalleled support along with community, nutrition, and healthy habits. In a world where health and well-being can often be a difficult and solitary journey, our comprehensive system offers intensely personalized support to individuals seeking to transform their health. The goal of this holistic approach is to empower people to master their metabolic health and improve body composition, beginning with a quality weight loss journey and offering the flexibility to achieve it on their own terms. The metabolic health system is designed for real life and built around four key components:

• Independent Coaches: Coaches provide individualized support and guidance to clients on their path to optimal health and well-being.

• Community: A community of like-minded individuals offers real-time connection and support.

• The Habits of Health Transformational System: A proprietary system that provides easy steps toward a sustainable healthy lifestyle.

• Products & Plans: Clinically proven plans and scientifically developed products, backed by dietitians, scientists, and physicians.

In October 2025, Medifast announced its strategic transformation, unveiling its focus on holistic metabolic health. The Company introduced Metabolic Synchronization™ — a breakthrough science that reverses metabolic dysfunction through a targeted reset of the body's metabolism. Research demonstrates that the Company's comprehensive system improves metabolic health by activating strong and targeted fat burn, (i.e., by reducing bad visceral fat), preserving lean mass, and protecting muscle. 1 This approach results in healthy, quality weight loss that extends beyond the scale, ultimately empowering individuals to achieve their health goals.

Metabolic health, often misunderstood or overlooked, refers to the body's ability to efficiently convert food into energy and regulate critical bodily functions. Metabolic dysfunction is a state that can often go unnoticed, placing strain on the body's metabolic processes and potentially leading to serious health challenges.

1 In a clinical study, individuals on the Company's 5 & 1 Plan experienced a reduction of 14% visceral fat and 98% of lean mass was retained at 16 weeks. Arterburn, L.M., C.D. Coleman, J. Kiel, et al. Randomized controlled trial assessing two commercial weight loss programs in adults with overweight or obesity. Obes Sci Pract 2019; 5/1: 3-14.

Science has always been integral to Medifast's identity. Through ongoing research and compelling data that elevate the science behind the Company's plans and innovative products, the Company is energizing its coach community to empower individuals to take control of their metabolic health. Looking ahead, Medifast plans to launch significant product innovations, incorporating next-generation ingredients for metabolic enhancement. We expect to bring this new product line to market in 2026. These upcoming innovations are designed to further strengthen the Company's offerings to help achieve optimal metabolic health.

While GLP-1 medication usage continues to accelerate, medication alone may not be adequate. Recent research indicates that approximately one-third of users discontinue the medication after six months, and up to 74% stop after a year. 2 Furthermore, studies show that two-thirds of weight lost on GLP-1 medications is typically regained within 12 months of stopping treatment, with cardiometabolic benefits often reversing as well. 3 GLP-1 medications can be effective tools, but lasting results require more than just medication—they demand holistic behavior change.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-02-17_item7_mdna.md, 10-K_2026-02-17_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
