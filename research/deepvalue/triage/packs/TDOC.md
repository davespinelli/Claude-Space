# Triage pack — TDOC · Teladoc Health, Inc.

_Generated 2026-09-05 01:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** TDOC · **Name:** Teladoc Health, Inc.
- **CIK:** 0001477449
- **SIC:** 8011 — Services-Offices & Clinics of  Doctors of  Medicine
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/TDOC

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Teladoc Health, Inc.
- **CIK:** 1,477,449 · **SIC:** 8011 (Services-Offices & Clinics of  Doctors of  Medicine) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 6.47 |
| mktcap | $1.2B |
| ev | $401.1M |
| ev_ebit | n/a |
| fcf | $285.5M |
| fcf_yield | 24.3% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -38.8% |
| net_debt | -$774.3M |
| net_debt_ebit | n/a |
| cash | $774.3M |
| ltd | $0.00 |
| equity | $1.3B |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $2.5B |
| revenue_prior | $2.6B |
| rev_growth | -1.5% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$263.0M |
| net_income | -$200.3M |
| cfo | $294.4M |
| capex | $8.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.8% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 181,684,021 |
| shares_py | 176,690,662 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -10.7% |
| r6m | 26.4% |
| off_52w_high | -33.4% |
| adv20 | $23.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.92 |
| r_ev_ebit | 0.00 |
| r_roic | 0.02 |
| r_rev_growth | 0.29 |
| r_buyback | 0.27 |
| score | 0.30 |

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
| rank | 409 |

**Screen rationale:** top-quartile FCF yield 24.3%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **181,684,021** (CY2026Q2I) vs **176,690,662** prior year (CY2025Q2I)
- Change: **2.8%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-31** — Item 5.02 (officer / director change or comp arrangement): Effective August 31, 2026, Teladoc Health, Inc. (the "Company") hired Michael Grasher as its Chief Financial Officer.
- **2026-08-13** — Item 5.02 (officer / director change or comp arrangement): On August 10, 2026, Mr. David B. Snow, Jr. notified Teladoc Health, Inc. (the "Company") of his intention to retire from the Board effective as of September 30, 2026.
- **2026-08-03** — Item 5.02 (officer / director change or comp arrangement): Effective August 3, 2026, the Board of Directors (the "Board") of Teladoc Health, Inc. (the "Company") increased the number of directors on the Board to ten and appointed Mark V. Anquillare as a director of the Company.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 63,135 sh / $421,935 -> net $-421,935 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 45 (open-market buys 0, sales 11).

| code | rows |
|---|---|
| A | 2 |
| M | 32 |
| S | 11 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'Teladoc Health Reports Second Quarter 2026 Results'; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (tdoc-20260630xexx991.htm)

Teladoc Health Reports Second Quarter 2026 Results

NEW YORK, July 29, 2026 —   Teladoc Health, Inc. (NYSE: TDOC), the global leader in virtual care, today reported financial results for the three months ended June 30, 2026 ("Second Quarter 2026"). Unless otherwise noted, percentage and other changes are relative to the three months ended June 30, 2025 ("Second Quarter 2025").

Highlights

• Second Quarter 2026 revenue of $606.9 million, down 4% year-over-year

• Second Quarter 2026 net loss of $38.9 million, or $0.21 per share

• Second Quarter 2026 adjusted EBITDA of $65.7 million, down 5% year-over-year

• Integrated Care segment revenue of $394.3 million, up 1% year-over-year, and adjusted EBITDA margin of 16.5%

• BetterHelp segment revenue of $212.6 million, down 12% year-over-year, and adjusted EBITDA margin of 0.2%

"We continue to make progress on the priorities we believe are most important to the long-term success of Teladoc Health. Our second-quarter results were within our guidance ranges on a consolidated basis and reflected distinct dynamics across our two segments," said Chuck Divita, Chief Executive Officer of Teladoc Health. "We delivered solid Integrated Care segment performance, with revenue growth and adjusted EBITDA margin above the midpoint of our guidance ranges and continued to advance new innovations designed to strengthen the value we provide to clients and members, including the launch of Teladoc One, our new connected care model for the U.S. market."

"In the BetterHelp segment, insurance revenue came in near the high end of our expectations. However, pressure on cash pay revenue accelerated further in late May and into June, beyond the assumptions underlying our prior outlook. We saw stronger than anticipated demand for insurance covered services that outpaced available provider capacity, limiting our ability to convert a greater share of that demand into sessions and revenue to offset the cash pay decline. Given strong consumer preference for insurance, we accelerated the nationwide insurance rollout ahead of plan, and we are taking focused actions to further support the scaling of insurance.

We continue to expect 2026 insurance revenue within our previously communicated range, but we have lowered our BetterHelp segment revenue outlook to reflect updated assumptions for cash pay including prioritization of the growing insurance market. We are addressing BetterHelp's near-term challenges with urgency and discipline and believe these actions will strengthen our ability to meet growing insurance demand and position the segment for more durable performance over time."

Key Financial Data
(In thousands, except per share data, unaudited)
Three Months Ended | Six Months Ended
June 30, | June 30,
2026 | 2025 | Change | 2026 | 2025 | Change
Revenue | 606,927 | 631,900 | (4) | % | 1,220,772 | 1,261,269 | (3) | %
Net loss | (38,908) | (32,660) | (19) | % | (102,745) | (125,672) | 18 | %
Net loss per share | (0.21) | (0.19) | (11) | % | (0.57) | (0.72) | 21 | %
Adjusted EBITDA (1) | 65,713 | 69,311 | (5) | % | 123,882 | 127,404 | (3) | %

See note (1) in the Notes section that follows.

Second Quarter 2026

Revenue decreased 4% to $606.9 million from $631.9 million in Second Quarter 2025. Access fees revenue decreased 9% to $474.2 million while other revenue increased 23% to $132.7 million. U.S. revenue decreased 6% to $487.4 million while International revenue increased 7% to $119.6 million.

Integrated Care segment revenue increased 1% to $394.3 million in Second Quarter 2026 while BetterHelp segment revenue decreased 12% to $212.6 million.

Net loss totaled $38.9 million, or $0.21 per share, for Second Quarter 2026, compared to $32.7 million, or $0.19 per share, for Second Quarter 2025. Results for Second Quarter 2026 included amortization of intangibles of $88.4 million, or $0.49 per share pre-tax, and stock-based compensation expense of $9.3 million, or $0.05 per share pre-tax.

Results for Second Quarter 2025 included amortization of intangibles of $88.7 million, or $0.50 per share pre-tax, and stock-based compensation expense of $22.3 million or $0.13 per share pre-tax. Net loss for Second Quarter 2025 also included restructuring costs related to severance costs and costs associated with office space reductions of $5.7 million, or $0.03 per share pre-tax. These items were partially offset by an acquisition related tax benefit of $9.7 million, or $0.06 per share.

Adjusted EBITDA (1) decreased 5% to $65.7 million, compared to $69.3 million for Second Quarter 2025. The Integrated Care segment adjusted EBITDA increase of $7.8 million was offset by a $11.4 million decrease of the BetterHelp segment adjusted EBITDA in Second Quarter 2026.

Six Months Ended June 30, 2026

Revenue decreased 3% to $1,220.8 million from $1,261.3 million in the first six months of 2025. Access fees revenue decreased 9% to $958.9 million while other revenue increased 24% to $261.9 million. U.S. revenue decreased 6% to $978.9 million while International revenue increased 12% to $241.9 million.

Integrated Care segment revenue increased 1% to $789.8 million in the first six months of 2026 while BetterHelp segment revenue decreased 10% to $431.0 million.

Net loss totaled $102.7 million, or $0.57 per share, for the first six months of 2026, compared to $125.7 million, or $0.72 per share, for the first six months of 2025. Results for the first six months of 2026 included amortization of intangibles of $178.3 million, or $0.99 per share pre-tax, and stock-based compensation expense of $23.9 million, or $0.13 per share pre-tax. Net loss for the first six months of 2026 also included restructuring costs of $12.9 million, or $0.07 per share pre-tax, primarily related to severance costs.

Results for the first six months of 2025 included a non-cash goodwill impairment charge of $59.1 million, or $0.34 per share pre-tax, amortization of intangibles of $173.0 million, or $0.99 per share pre-tax, and stock-based compensation expense of $47.5 million, or $0.27 per share pre-tax. Net loss for the first six months of 2025 also included restructuring costs related to severance costs and costs associated with office space reductions of $10.0 million, or $0.06 per share pre-tax. These items were partially offset by a discrete tax benefit of $20.1 million, or $0.11 per share, related to the completion of a research and development tax credit study and acquisition related tax benefits of $11.1 million, or $0.06 per share.

The non-cash goodwill impairment charge recorded in the first six months of 2025 was the result of the fair value of the Integrated Care segment being less than its carrying value at the time of the acquisition of Catapult Health, LLC.

Adjusted EBITDA (1) decreased 3% to $123.9 million, compared to $127.4 million for the first six months of 2025. The Integrated Care segment adjusted EBITDA increase of $13.7 million was offset by a $17.2 million decrease of the BetterHelp segment adjusted EBITDA in the first six months of 2026.

Capex and Cash Flow

Cash flow from operations was $64.7 million in Second Quarter 2026, compared to $91.4 million in Second Quarter 2025, and was $74.2 million in the first six months of 2026, compared to $107.4 million in the first six months of 2025. Capital expenditures and capitalized software development costs (together, "Capex")

were $28.9 million in Second Quarter 2026, compared to $30.2 million in Second Quarter 2025, and were $64.7 million in the first six months of 2026, compared to $61.8 million in the first six months of 2025. Free cash flow was $35.7 million in Second Quarter 2026, compared to $61.2 million in Second Quarter 2025, and was $9.4 million in the first six months of 2026, compared to $45.5 million in the first six months of 2025.

Financial Outlook

The outlook provided below is based on current market conditions and expectations and what we know today.

For the full year of 2026, we expect:
Full Year 2026 Outlook Range
Revenue | $2,362 - $2,447 million
Adjusted EBITDA | $271 - $303 million
Net loss per share | ($1.00) - ($0.75)
Free Cash Flow | $130 - $170 million
U.S. Integrated Care Members (2) | 98.5 - 100.5 million
Integrated Care
Revenue growth percentage (year-over-year) | 0.8% - 2.4%
Adjusted EBITDA margin | 15.6% - 16.4%
BetterHelp
Revenue growth percentage (year-over-year) | (19.0%) - (12.7%)
Adjusted EBITDA margin | 3.0% - 4.6%

For the third quarter of 2026, we expect:
3Q 2026 Outlook Range
Revenue | $569 - $609 million
Adjusted EBITDA | $62 - $74 million
Net loss per share | ($0.30) - ($0.20)
U.S. Integrated Care Members (2) | 99.0 - 100.5 million
Integrated Care
Revenue growth percentage (year-over-year) | 0.0% - 3.0%
Adjusted EBITDA margin | 15.7% - 17.2%
BetterHelp
Revenue growth percentage (year-over-year) | (24.2%) - (12.3%)
Adjusted EBITDA margin | 0.5% - 2.5%

See note (2) in the Notes section that follows.

Earnings Conference Call

The Second Quarter 2026 earnings conference call and webcast will be held Wednesday, July 29, 2026 at 5:00 p.m. E.T. The conference call can be accessed by dialing 833-461-5787 for U.S. participants and using the conference ID # 478 236 923. For international participants, please visit the following link for global dial-in numbers, using the same conference ID # 478 236 923: https://help.events.q4inc.com/eahc/international-dial-in-numbers. A live audio webcast will also be available online at http://ir.teladoc.com/news-and-events/events-and-presentations/. A replay of the call will be available via webcast for on-demand listening shortly after the completion of the call, at the same web link, and will remain available for approximately 90 days.

About Teladoc Health

Teladoc Health is the global leader in virtual care. The company is delivering and orchestrating care across patients, care providers, platforms, and partners — transforming virtual care into a catalyst for how better health happens. Through our relationships with health plans, employers, providers, health systems and consumers, we are enabling more access, driving better outcomes, extending provider capacity and lowering costs. Learn more at www.teladochealth.com.

Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Cost of revenue (exclusive of depreciation and amortization, which are shown separately) | 124 | 506 | 471 | 1,079
Advertising and marketing | 426 | 1,302 | 1,286 | 2,805
Sales | 1,460 | 3,594 | 3,537 | 7,853
Technology and development | 1,735 | 4,247 | 4,462 | 10,032
General and administrative | 5,556 | 12,695 | 14,156 | 25,738
Total stock-based compensation expense (3) | 9,301 | 22,344 | 23,912 | 47,507

See note (3) in the Notes section that follows.

Revenues

Three Months Ended | Six Months Ended
June 30, | June 30,
(In thousands, unaudited) | 2026 | 2025 | Change | 2026 | 2025 | Change
Revenue by Type
Access Fees | 474,215 | 523,703 | (9) | % | 958,870 | 1,049,439 | (9) | %
Other | 132,712 | 108,197 | 23 | % | 261,902 | 211,830 | 24 | %
Total Revenue | 606,927 | 631,900 | (4) | % | 1,220,772 | 1,261,269 | (3) | %
Revenue by Geography
U.S. | 487,360 | 519,689 | (6) | % | 978,865 | 1,044,659 | (6) | %
International | 119,567 | 112,211 | 7 | % | 241,907 | 216,610 | 12 | %
Total Revenue | 606,927 | 631,900 | (4) | % | 1,220,772 | 1,261,269 | (3) | %

Summary Operating Metrics

Consolidated

Three Months Ended | Six Months Ended
June 30, | June 30,
(In millions) | 2026 | 2025 | Change | 2026 | 2025 | Change
Total Visits | 4.1 | 4.1 | (2) | % | 8.4 | 8.6 | (2) | %

Integrated Care

As of June 30,
(In millions) | 2026 | 2025 | Change
U.S. Integrated Care Members (2) | 100.3 | 102.4 | (2) | %
Chronic Care Program Enrollment (4) | 1.272 | 1.117 | 14 | %

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-26_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Teladoc, Inc. was incorporated in the State of Texas in June 2002 and changed its state of incorporation to the State of Delaware in October 2008. Effective August 10, 2018, Teladoc, Inc. changed its corporate name to Teladoc Health, Inc. Unless the context otherwise requires, Teladoc Health, Inc., together with its subsidiaries, is referred to herein as "Teladoc Health," the "Company," or "we." In June 2025, the Company relocated its principal executive office from Purchase, New York to New York, New York. Teladoc Health is the global leader in virtual care.

More than 20 years ago, we were founded on a simple, yet revolutionary idea: that everyone should have access to the best healthcare, anywhere in the world on their terms.

Our mission is to empower all people everywhere to live their healthiest lives by transforming the healthcare experience. Today, we are transforming virtual care into a catalyst for how better health happens around the world. We connect patients, care providers, healthcare platforms and partners to provide more complete and personalized care. Through our unique technology, breadth of services and depth of clinical expertise, we are delivering and orchestrating care in order to improve health outcomes and reduce healthcare costs around the world.

The impact that the imposition of tariffs and changes to global trade policies will have on our consolidated results of operations is uncertain. We expect tariffs on goods imported into the U.S. from Canada, Mexico, and China, and other countries upon which tariffs may be imposed, to continue to be met with retaliatory tariffs from those countries which would impact our consolidated results of operations as we import components for assembling welcome kits, refill kits, and replacement components for our chronic care management solutions and virtual care devices manufactured for sale or lease as part of our hosted virtual care platform solution. The extent and duration of tariffs and the resulting impact on macroeconomic conditions and on our business are uncertain and may depend on various factors, including negotiations between the U.S. and affected countries, retaliation imposed by other countries, tariff exemptions, negative sentiment toward U.S. companies and products, and availability of lower cost inputs that may be sourced domestically or in other countries with no or lower tariffs. We will continue to evaluate the nature and extent of the impact to our business and consolidated results of operations. For further information, see "Risk Factors—We depend on a limited number of third-party suppliers for certain components of our medical devices, and the loss of any of these suppliers, or their inability to provide us with an adequate supply of materials, could harm our business," and "—Our international operations pose certain political, legal and compliance, operational, regulatory, economic, and other risks to our business that may be different from or more significant than risks associated with our domestic operations, and our exposure to these risks is expected to increase" included elsewhere in this Annual Report on Form 10-K.

Key Factors Affecting Our Performance

We believe that our future performance will depend on many factors, including the following:

As it relates to the Integrated Care segment:

Number of U.S. Integrated Care Members. U.S. Integrated Care members represent the number of unique individuals who have paid access and visit fee only access to our suite of integrated care services in the U.S. at the end of the applicable period. Individuals who have paid access fees offer a greater margin than those who have visit fee only access and, over time, the mix of those who have paid access fees as compared to those who have visit fee only access has declined. Our revenue growth rate and long-term profitability are affected by our ability to increase cross selling capability among our existing members over time because we derive a substantial portion of our revenue from access and other fees via Client contracts that provide members access to the THMG Association professional provider network in exchange for a contractual based periodic fee. Therefore, we believe that our ability to add new members and retain existing members and to increase utilization and penetration further into existing and new health plan and employer Clients is a key indicator of our increasing market adoption, the growth of our business, and our future revenue potential. We further believe that increasing our membership is an integral objective that will provide us with the ability to continually innovate our services

and support initiatives that will enhance members' experiences. However, certain health plans that have historically promoted our services to our employer Clients have developed, and may in the future continue to develop, solutions that replicate our services or offer competitive services at discounted prices to our current or prospective Clients, which could result in a loss of members. For further information, see "Risk Factors—Risks Related to Our Business and Industry—We operate in a competitive industry, and if we are not able to compete effectively, our business, financial condition, and results of operations will be harmed," and "—A significant portion of our revenue comes from a limited number of Clients, the loss of which could have a material adverse effect on our business, financial condition and results of operations" included elsewhere in this Annual Report on Form 10-K. U.S. Integrated Care members increased by 8.0 million, or 9%, to 101.8 million at December 31, 2025, compared to the same period in 2024.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Consolidated Results of Operations

The following table sets forth our consolidated statement of operations data for the years ended December 31, 2025 and 2024 and the dollar and percentage change between the respective periods (dollars in thousands, except per share data).

Year Ended December 31, | Variance | %
2025 | 2024
Revenue | 2,529,977 | 2,569,574 | (39,597) | (2) | %
Costs and expenses:
Cost of revenue (exclusive of depreciation and amortization, which are shown separately below) | 771,593 | 751,270 | 20,323 | 3 | %
Advertising and marketing | 653,372 | 705,787 | (52,415) | (7) | %
Sales | 194,518 | 204,993 | (10,475) | (5) | %
Technology and development | 277,922 | 307,274 | (29,352) | (10) | %
General and administrative | 431,891 | 435,490 | (3,599) | (1) | %
Goodwill impairments | 71,763 | 790,000 | (718,237) | (91) | %
Acquisition, integration, and transformation costs | 9,010 | 1,743 | 7,267 | n/m
Restructuring costs | 18,785 | 20,355 | (1,570) | (8) | %
Amortization of intangible assets | 350,764 | 363,365 | (12,601) | (3) | %
Depreciation of property and equipment | 13,314 | 10,183 | 3,131 | 31 | %
Total costs and expenses | 2,792,932 | 3,590,460 | (797,528) | (22) | %
Loss from operations | (262,955) | (1,020,886) | 757,931 | 74 | %
Interest income | (36,770) | (57,071) | 20,301 | (36) | %
Interest expense | 19,714 | 23,803 | (4,089) | (17) | %
Other expense (income), net | (10,369) | 6,035 | (16,404) | n/m
Loss before provision for income taxes | (235,530) | (993,653) | 758,123 | 76 | %
Provision for income taxes | (35,208) | 7,592 | (42,800) | n/m
Net loss | (200,322) | (1,001,245) | 800,923 | 80 | %
Net loss per share, basic and diluted | (1.14) | (5.87) | 4.73 | 81 | %
Adjusted EBITDA (1) | 281,095 | 310,711 | (29,616) | (10) | %

n/m – not meaningful

(1) Non-GAAP Financial Measures

The following table reconciles net loss, the most directly comparable GAAP measure, to Adjusted EBITDA for the years ended December 31, 2025 and 2024 (in thousands):

Year Ended December 31,
2025 | 2024
Net loss | (200,322) | (1,001,245)
Add:
Provision for income taxes | (35,208) | 7,592
Other expense (income), net | (10,369) | 6,035
Interest expense | 19,714 | 23,803
Interest income | (36,770) | (57,071)
Depreciation of property and equipment | 13,314 | 10,183
Amortization of intangible assets | 350,764 | 363,365
Restructuring costs | 18,785 | 20,355
Acquisition, integration, and transformation costs | 9,010 | 1,743
Goodwill impairments | 71,763 | 790,000
Stock-based compensation | 80,414 | 145,951
Adjusted EBITDA | 281,095 | 310,711
Integrated Care | 239,222 | 232,902
BetterHelp | 41,873 | 77,809
Adjusted EBITDA | 281,095 | 310,711

Revenue. The following table presents revenues disaggregated by revenue source and geography for the years ended December 31, 2025 and 2024 (dollars in thousands):

Year Ended December 31,
2025 | 2024 | Variance | %
Revenue by Type
Access Fees | 2,091,941 | 2,215,220 | (123,279) | (6) | %
Other | 438,036 | 354,354 | 83,682 | 24 | %
Total Revenue | 2,529,977 | 2,569,574 | (39,597) | (2) | %
Revenue by Geography
U.S. Revenue | 2,071,739 | 2,159,959 | (88,220) | (4) | %
International Revenue | 458,238 | 409,615 | 48,623 | 12 | %
Total Revenue | 2,529,977 | 2,569,574 | (39,597) | (2) | %

Revenue. Total revenue was $2,530.0 million for the year ended December 31, 2025, compared to $2,569.6 million for the year ended December 31, 2024, a decrease of $39.6 million, or 2%. This decrease in revenue was driven by lower revenue in our BetterHelp segment, partially offset by higher revenue in our Integrated Care segment. The acquisitions of Catapult Health, Uplift, and Telecare increased total revenue for the year ended December 31, 2025 by approximately 2 percentage points.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-26_item1_business.md)

Item 1. Business

Overview

Teladoc Health is the global leader in virtual care. More than 20 years ago, we were founded on a simple, yet revolutionary idea: that everyone should have access to the best healthcare, anywhere in the world on their terms. Our mission is to empower all people everywhere to live their healthiest lives by transforming the healthcare experience. Today, we are transforming virtual care into a catalyst for how better health happens around the world. We connect patients, care providers, healthcare platforms and partners to provide more complete and personalized care. Through our unique technology, breadth of services and depth of clinical expertise, we are delivering and orchestrating care in order to improve health outcomes and reduce healthcare costs around the world.

We are equipping care teams to perform at their highest caliber, providing effective care and support that addresses and resolves comprehensive health needs— physical and mental, simple and complex, urgent and ongoing. By applying the power of technology and insights from millions of health interactions, we are guiding targeted health actions and elevating healthcare experiences to make moments of care more impactful. We work with health plans, employers, health systems, and partners around the world, giving us visibility into best practices and health journeys that enable us to drive impact at scale.

We offer a portfolio of services and solutions, bolstered by technology, artificial intelligence ("AI"), machine learning and human expertise to provide an effective care experience that people value and trust. By combining the latest in data science and analytics with a personalized user experience through a set of highly flexible integrated technology platforms, we completed 17.1 million telehealth visits in 2025 through our business-to-business ("B2B") and direct-to-consumer ("D2C") channels. We provide access to healthcare 24 hours a day, 7 days a week, and 365 days a year.

We have two reportable segments: Integrated Care and BetterHelp.

Our Integrated Care segment delivers high-quality virtual care that is available to more than 100 million members through their employers and insurers. These virtual care services address a broad spectrum of care needs including preventive care, primary care, 24/7 urgent care, mental healthcare, chronic care and expert second opinions. Teladoc Health care teams also coordinate, or orchestrate, care needs by referring patients to high-quality in-person care in their communities when medically appropriate. For hospitals and health systems, we provide highly-scalable connected care solutions -- including hardware, software and services — that help organizations deliver telehealth services to their patients in virtual care and hybrid care models. Services in this segment are distributed primarily on a B2B basis.

Our BetterHelp segment primarily consists of our market leading mental health platform. Online counseling and therapy services are provided via our network of nearly 35,000 licensed clinicians leveraging our platform for web, mobile app, phone, and text-based interactions.

Who We Serve

As of December 31, 2025, approximately 102 million members in the United States ("U.S.") have access to one or more of our services. The customers of our Integrated Care segment primarily consist of employers, health plans, hospitals and health systems, insurance companies, and financial services companies (collectively "Clients"), as well as individuals who turn to us for care. We help Clients to expand access to high-quality healthcare, improve outcomes, and lower healthcare costs. Our solutions offer our Clients substantial savings opportunities and an attractive return on investment. As part of this segment, we sell to our Clients on behalf of their beneficiaries, including employees and health plan members. In our various sales channels, a range of third parties, including health plans, pharmacy benefits managers, financial institutions, brokers, agents, benefits consultants, and resellers, sell our solutions to various end markets around the world. Our BetterHelp segment primarily provides mental health services to individuals who self-pay or are covered by insurance.

How We Generate Revenue

For the year ended December 31, 2025, 83% of our consolidated revenue was derived from access fees. To a lesser extent, we generate revenue from visit fees as well as sales of hardware and other related services to hospital and health systems, which is reported in "other revenue".

Integrated Care Segment

Our Integrated Care segment primarily generates revenue on a contractually recurring, access fee basis. Clients pay monthly access fees on a per-member-per-month ("PMPM") model, a per-employee-per-month ("PEPM") model, or on a per-participant-per-month ("PPPM") model, based on the number of actively enrolled members each month.

Access fees are paid by our Clients on behalf of their employees, dependents, policy holders, card holders, beneficiaries, clinicians, or as is the case with certain of our subscribers, fees are paid by our members themselves.

We also generate revenue from Clients on a per-telehealth visit basis. These visit fees are typically paid by Clients and/or members.

Depending on the product, we may generate revenue from Clients through a combination of access fees and visit fees, while certain Clients may have access-fee only or visit fee only arrangements.

This segment also generates revenue from software licenses and implementation fees related to hospitals & health systems Clients who use our technology to deliver virtual care. These Clients also purchase and lease related hardware devices such as robots, carts, and tablets.

Some of our contracts place a portion of our fees at risk or provide an opportunity to earn performance-based payments for achieving specific targets for service-level metrics, cost savings, and/or clinical outcomes.

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

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-02-26_item7_mdna.md, 10-K_2026-02-26_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
