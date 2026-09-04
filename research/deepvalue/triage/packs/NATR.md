# Triage pack — NATR · NATURES SUNSHINE PRODUCTS INC

_Generated 2026-09-04 15:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** NATR · **Name:** NATURES SUNSHINE PRODUCTS INC
- **CIK:** 0000275053
- **SIC:** 2834 — Pharmaceutical Preparations
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/NATR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** NATURES SUNSHINE PRODUCTS INC
- **CIK:** 275,053 · **SIC:** 2834 (Pharmaceutical Preparations) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 13.80 |
| mktcap | $242.8M |
| ev | $160.3M |
| ev_ebit | 6.5x |
| fcf | $28.8M |
| fcf_yield | 11.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | n/a |
| net_debt | -$82.5M |
| net_debt_ebit | -3.3x |
| cash | $82.5M |
| ltd | $0.00 |
| equity | n/a |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $480.1M |
| revenue_prior | $454.4M |
| rev_growth | 5.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $24.7M |
| net_income | $19.5M |
| cfo | $35.3M |
| capex | $6.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -0.2% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 17,595,520 |
| shares_py | 17,635,552 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 16.5% |
| r6m | -46.6% |
| off_52w_high | -50.4% |
| adv20 | $3.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.76 |
| r_ev_ebit | 0.90 |
| r_roic | 0.50 |
| r_rev_growth | 0.54 |
| r_buyback | 0.70 |
| score | 0.63 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | n/a |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 112 |

**Screen rationale:** top-quartile FCF yield 11.9%; cheap at 6.5x EV/EBIT; debt data missing (net cash unverified); 12-1 momentum 16.5%; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **17,595,520** (CY2026Q2I) vs **17,635,552** prior year (CY2025Q2I)
- Change: **-0.2%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-08-06** — Item 5.02 (officer / director change or comp arrangement): Appointment of Executive Vice President and Chief Financial Officer
- **2026-05-11** — Item 5.02 (officer / director change or comp arrangement): On May 8, 2026, L. Shane Jones notified Nature's Sunshine Products, Inc. (the "Company") that he is resigning as the Company's Chief Financial Officer effective June 5, 2026.
- **2026-05-07** — Item 5.02 (officer / director change or comp arrangement): On May 6, 2026, Nature's Sunshine Products, Inc. (the "Company") held its 2026 Annual Meeting of Shareholders (the "Annual Meeting") and the shareholders of the Company approved the adoption of the 2026 Stock Incentive Plan (the "Plan").
- **2026-03-10** — Item 5.02 (officer / director change or comp arrangement): On February 24, 2026, the Compensation Committee of the Company approved an increase to the base salary of the Company's Chief Financial Officer, Mr. L. Shane Jones, from $478,400 to $492,752 which increase is effective March 8, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 161,389 sh / $2,612,712 vs sells 35,696 sh / $742,411 -> net $1,870,301 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: PRESCOTT GROUP CAPITAL MANAGEMENT, L.L.C. / PRESCOTT GROUP AGGRESSIVE SMALL CAP LP / PRESCOTT GROUP AGGRESSIVE SMALL CAP II LP / PRESCOTT GROUP AGGRESSIVE SMALL CAP MASTER FUND GP / FROHLICH PHIL bought 30,000 sh @ $16.68 ($500,400) on 2026-08-07.

Form 4 filings parsed: 12; transaction rows: 25 (open-market buys 14, sales 5).

| code | rows |
|---|---|
| A | 5 |
| F | 1 |
| P | 14 |
| S | 5 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'Nature's Sunshine Reports Second Quarter 2026 Results'; skipped 37 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (natrq22026earningsrelease.htm)

Nature's Sunshine Reports Second Quarter 2026 Results

Net Sales up 2% to $117.0 million, Gross Profit Margin up 194 Basis Points to 73.7%

LEHI, Utah – August 6, 2026 – Nature's Sunshine Products, Inc. (Nasdaq: NATR) ("Nature's Sunshine"), a global leader in manufacturing and marketing high-quality herbal and nutritional supplements, reported financial results for the second quarter ended June 30, 2026.

Second Quarter 2026 Financial Summary vs. Same Year-Ago Quarter

• Net sales were up 2% to $117.0 million compared to $114.8 million (up 4% in constant currency).

• Gross profit margin increased 194 basis points to 73.7% compared to 71.7%.

• GAAP net income attributable to common shareholders was $3.5 million, or $0.19 per diluted common share, compared to $5.3 million, or $0.28 per diluted common share.

• Adjusted EBITDA was $11.3 million compared to $11.3 million.

Management Commentary

"We delivered a solid quarter, with constant currency sales growth of 4% across nearly all of our geographic regions," said Ken Romanzi, CEO of Nature's Sunshine. "Results were led by 5% growth in Asia Pacific, driven by strong consultant engagement, and by North America, where digital sales increased 26%, fueled by continued momentum among new and returning customers. Growth was supported by continued customer acquisition, expansion of our digital capabilities, increased adoption of our auto-ship subscription programs, and solid consultant growth. Strong execution, disciplined cost management, and ongoing productivity initiatives also drove further gross margin expansion.

"The second quarter marked the beginning of investments in our Vision for Growth, our plan to accelerate our longer-term growth rate including continued expansion of our digital business, enhanced digital tools for our consultant base, deeper penetration of existing markets, and expansion into new markets. We believe these investments, combined with our strong business model and disciplined execution, position us to deliver sustainable, accelerated long-term growth."

Second Quarter 2026 Financial Results

Net Sales by Operating Segment (Amounts in Thousands)
Three Months Ended June 30, | 2026 | 2025 | Percent Change | Impact of Currency Exchange | Percent Change Excluding Impact of Currency
Asia | 52,997 | 52,664 | 0.6 | % | (2,466) | 5.3 | %
Europe | 22,694 | 21,741 | 4.4 | 156 | 3.7
North America | 35,951 | 34,977 | 2.8 | (6) | 2.8
Latin America and Other | 5,343 | 5,368 | (0.5) | 174 | (3.7)
116,985 | 114,750 | 1.9 | % | (2,142) | 3.8 | %

Net sales in the second quarter increased 2% to $117.0 million compared to $114.8 million in the same year-ago quarter. Excluding the impact from foreign exchange rates, net sales in the second quarter of 2026 increased 4% compared to the year-ago quarter.

Gross profit margin in the second quarter increased to 73.7% compared to 71.7% in the year-ago quarter. The increase was driven by cost savings initiatives and market mix.

Volume incentives as a percentage of net sales were 30.6% compared to 29.9% in the year-ago quarter. The increase was primarily due to timing of promotional incentives and market mix.

Selling, general and administrative expenses ("SG&A") in the second quarter were $44.9 million compared to $43.7 million in the year‐ago quarter. The increase was primarily related to consultant events and variable selling expenses, partially offset by compensation costs. As a percentage of net sales, SG&A expenses were 38.4% for the second quarter of 2026 compared to 38.1% in the year-ago quarter.

Operating income in the second quarter increased to $5.5 million, or 4.7% of net sales, compared to $4.3 million, or 3.7% of net sales, in the year-ago quarter.

Other income (expense), net, in the second quarter of 2026 was $(0.1) million compared to $3.3 million in the second quarter of 2025. Other income (expense), net, primarily consisted of foreign exchange losses in Asia, partially offset by foreign exchange gains in Europe and Latin America that resulted from net changes in foreign currencies. The provision for income taxes was $1.8 million in the second quarter of 2026 compared to $2.0 million for the year-ago quarter.

GAAP net income attributable to common shareholders decreased to $3.5 million, or $0.19 per diluted common share, compared to $5.3 million, or $0.28 per diluted common share, in the second quarter of 2025. As a result of the December 2025 purchase of noncontrolling interests, there was no net income attributable to NSP China for the second quarter of 2026, compared to $0.9 million, or $0.05 per diluted common share, for the second quarter of 2025.

Adjusted EBITDA in the second quarter remained flat at $11.3 million compared to $11.3 million in the year-ago quarter. Adjusted EBITDA, which is a non-GAAP financial measure, is defined here as net income from continuing operations before taxes, depreciation, amortization, and other income (expense) adjusted to exclude share-based compensation expense and certain noted adjustments. A reconciliation of net income to adjusted EBITDA is provided in the attached financial tables.

Balance Sheet and Cash Flow

Net cash used by operating activities was $1.0 million for the six months ended June 30, 2026, compared to $6.9 million provided in the prior year period. Capital expenditures during the six months ended June 30, 2026, totaled $5.3 million compared to $2.5 million in the comparable period of 2025. During the six months ended June 30, 2026, the Company repurchased 113,000 shares at a total cost of $2.6 million or $22.55 per share. As of June 30, 2026, the Company had cash and cash equivalents of $82.5 million and zero debt.

Outlook

Reflecting the impact of a stronger U.S. dollar and recent softness in the China market, Nature's Sunshine now expects full year 2026 net sales to range between $490 to $500 million ($500 to $515 million prior). Adjusted EBITDA is now expected to range between $48 to $52 million ($50 to $54 million prior).

Conference Call

The Company will hold a conference call today at 5:00 p.m. Eastern time to discuss its second quarter of 2026 results.

Date: Thursday, August 6, 2026

Time: 5:00 p.m. Eastern time (3:00 p.m. Mountain time)

Toll-free dial-in number: 1-800-717-1738

International dial-in number: 1-646-307-1865

Conference ID: 39783

Please call the conference telephone number 5-10 minutes prior to the start time. An operator will register your name and organization. If you have any difficulty connecting with the conference call, please contact Gateway Group at 1-949-574-3860.

The conference call will be broadcast live and available for replay here and via the Events section of the Nature's Sunshine website here.

A replay of the conference call will be available after 8:00 p.m. Eastern time on the same day through Thursday, August 20, 2026.

Toll-free replay number: 1-844-512-2921

International replay number: 1-412-317-6671

Replay ID: 11139783

About Nature's Sunshine Products

Nature's Sunshine Products (Nasdaq: NATR), a leading natural health and wellness company, markets and distributes nutritional and personal care products in more than 40 countries. Nature's Sunshine manufactures most of its products through its own state-of-the-art facilities to ensure its products continue to set the standard for the highest quality, safety, and efficacy on the market today. Additional information about the company can be obtained at its website, www.naturessunshine.com.

With respect to our adjusted EBITDA outlook for the full year 2026, a quantitative reconciliation to the corresponding GAAP information cannot be provided without unreasonable effort because of the inherent difficulty of accurately forecasting the occurrence and financial impact of the various adjusting items necessary for such reconciliation that have not yet occurred, are out of our control, or cannot be reasonably predicted, including but not limited to warrant liabilities and stock based compensation. For the same reasons, we are unable to assess the probable significance of the unavailable information, which could have a material impact on our future GAAP financial results.

Investor Relations:

Gateway Group, Inc.

Cody Slach

1-949-574-3860

NATR@gateway-grp.com

NATURE'S SUNSHINE PRODUCTS, INC. AND SUBSIDIARIES

CONDENSED CONSOLIDATED STATEMENTS OF INCOME

(Amounts in thousands, except per share information)

(Unaudited)
Three Months Ended June 30, | Six Months Ended June 30,
2026 | 2025 | 2026 | 2025
Net sales | 116,985 | 114,750 | 239,877 | 227,998
Cost of sales | 30,811 | 32,451 | 63,726 | 64,102
Gross profit | 86,174 | 82,299 | 176,151 | 163,896
Operating expenses:
Volume incentives | 35,817 | 34,360 | 72,710 | 69,204
Selling, general and administrative | 44,876 | 43,665 | 88,415 | 84,246
Operating income | 5,481 | 4,274 | 15,026 | 10,446
Other income (expense):
Interest and other income, net | 161 | 268 | 235 | 473
Interest expense | (53) | (24) | (88) | (45)
Foreign exchange gains (losses), net | (223) | 3,026 | (1,652) | 3,779
(115) | 3,270 | (1,505) | 4,207
Income before provision for income taxes | 5,366 | 7,544 | 13,521 | 14,653
Provision for income taxes | 1,828 | 2,025 | 4,865 | 4,250
Net income | 3,538 | 5,519 | 8,656 | 10,403
Net income attributable to noncontrolling interests | — | 186 | — | 323
Net income attributable to common shareholders | 3,538 | 5,333 | 8,656 | 10,080
Basic and diluted net income per common share:
Basic earnings per share attributable to common shareholders | 0.20 | 0.29 | 0.49 | 0.55
Diluted earnings per share attributable to common shareholders | 0.19 | 0.28 | 0.48 | 0.54
Weighted average basic common shares outstanding | 17,812 | 18,406 | 17,667 | 18,446
Weighted average diluted common shares outstanding | 18,337 | 18,966 | 18,003 | 18,832

NATURE'S SUNSHINE PRODUCTS, INC. AND SUBSIDIARIES

CONDENSED CONSOLIDATED BALANCE SHEETS

(Amounts in thousands)

(Unaudited)
June 30, 2026 | December 31, 2025
Assets
Current assets:
Cash and cash equivalents | 82,503 | 93,891
Accounts receivable, net of allowance for doubtful accounts of $61 and $69, respectively | 13,861 | 8,602
Inventories | 71,730 | 68,312
Prepaid expenses and other | 10,302 | 8,040
Total current assets | 178,396 | 178,845
Property, plant and equipment, net | 30,955 | 32,915
Operating lease right-of-use assets | 19,284 | 17,600
Restricted investment securities - trading | 1,250 | 1,132
Deferred income tax assets | 19,495 | 20,068
Other assets | 10,443 | 10,586
Total assets | 259,823 | 261,146
Liabilities and Shareholders' Equity
Current liabilities:
Accounts payable | 7,726 | 8,021
Accrued volume incentives and service fees | 25,320 | 22,624
Accrued liabilities | 25,794 | 34,080
Deferred revenue | 1,981 | 5,840
Income taxes payable | 3,499 | 4,703
Current portion of operating lease liabilities | 4,425 | 3,270
Total current liabilities | 68,745 | 78,538
Liability related to unrecognized tax benefits | 106 | 428
Long-term portion of operating lease liabilities | 17,003 | 15,630
Deferred compensation payable | 1,250 | 1,132
Deferred income tax liabilities | 886 | 954
Other liabilities | 2,517 | 2,911
Total liabilities | 90,507 | 99,593
Shareholders' equity:
Common stock, no par value, 50,000 shares authorized, 17,614 and 17,508 shares issued and outstanding, respectively | 100,787 | 102,192
Retained earnings | 85,584 | 76,928
Accumulated other comprehensive loss | (17,055) | (17,567)
Total shareholders' equity | 169,316 | 161,553
Total liabilities and shareholders' equity | 259,823 | 261,146

NATURE'S SUNSHINE PRODUCTS, INC. AND SUBSIDIARIES

CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS

(Amounts in thousands)

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-10_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

OVERVIEW

Our Business, Industry and Target Market

We are a global leader in manufacturing and marketing high-quality herbal and nutritional supplements. We are a Utah corporation with our principal place of business in Lehi, Utah, and sell our products directly to customers and to a sales force of independent consultants who resell our products to consumers.

Our independent consultants market and sell our products to customers and sponsor other independent consultants who also market our products to customers. Because a significant amount of revenue is generated through the sales of our independent consultants, our revenue can be impacted by the number and productivity of our independent consultants. We seek to motivate and provide incentives to our independent consultants by offering high quality products, product support, training seminars and financial incentives, among other considerations.

2025 Performance

In 2025, we experienced an increase in our consolidated net sales of 5.7 percent (or 5.3 percent in local currencies) compared to 2024. Asia net sales increased approximately 6.7 percent (or 6.4 percent in local currencies) compared to 2024. Europe net sales increased approximately 9.8 percent (or 7.8 percent in local currencies) compared to 2024. North America net sales increased approximately 3.4 percent (or 3.6 percent in local currencies) compared to 2024. Latin America and Other net sales decreased approximately 5.5 percent (or 4.2 percent in local currencies) compared to 2024. The strengthening of the U.S. dollar versus the local currencies, primarily in our Europe and Asia markets, resulted in an approximate 0.4 percent, or $1.8 million, increase of our net sales during the year ended December 31, 2025.

Cost of sales increased $2.7 million during 2025, compared to the same period in 2024, and as a percentage of net sales, were 27.6 percent and 28.5 percent for 2025 and 2024, respectively. The decrease in cost of sales percentage is primarily due to cost savings initiatives and market mix.

In absolute terms, selling, general and administrative expenses increased $14.4 million during 2025, and as a percentage of net sales, were 37.2 percent and 36.1 percent for 2025 and 2024, respectively. The increase was primarily related to the timing of compensation costs, incremental investment in digital marketing and consultant events, increased service fees due to China's higher net sales, as well as other non-recurring expenses.

As an international business, we have significant sales and costs denominated in currencies other than the U.S. Dollar. We expect foreign markets with functional currencies other than the U.S. Dollar will continue to represent a substantial portion of our overall sales and related operating expenses. Accordingly, changes in foreign currency exchange rates could materially affect sales and costs or the comparability of sales and costs from period to period as a result of translating foreign markets' financial statements into our reporting currency.

Eastern Europe

On February 24, 2022, Russian forces launched significant military action against Ukraine. There continues to be sustained conflict and disruption in the region, which is expected to endure for the foreseeable future. Our consultants in the impacted regions continue to operate their independent businesses, albeit at a reduced level than prior to the start of the conflict. We expect that this will continue to impact our business for the foreseeable future. We will continue monitoring the social, political, regulatory and economic environment in Ukraine and Russia and will consider further actions as appropriate.

More broadly, there could be additional negative impacts to our net sales, earnings and cash flows should the situation escalate beyond its current scope, including, among other potential impacts, economic recessions in certain neighboring countries.

Net sales related to Eastern Europe for the years ended December 31, 2025 and 2024, were $60.0 million and $54.8 million, respectively. Operating income related to Eastern Europe for the years ended December 31, 2025 and 2024, were $4.7 million and $4.2 million, respectively. As of December 31, 2025, Eastern Europe had assets of $5.0 million, net of working capital reserves related to inventories.

In November 2024, we began an internal investigation regarding our past compliance with relevant U.S. trade controls and made an initial voluntary self-disclosure of apparent trade controls violations to the U.S. Department of Commerce's

Bureau of Industry and Security ("BIS"). In addition, in April 2025, we filed an initial voluntary self-disclosure with the Office of Foreign Asset Control ("OFAC") relating to the same internal investigation. Following our internal investigation, we filed final voluntary self-disclosures with BIS and OFAC on September 5, 2025. We estimate that such potential violations represented less than one percent of our net revenue in each of our last three fiscal years. An unfavorable outcome of this investigation may include fines or penalties imposed in response to our voluntary disclosures. While we believe the amount of any fines or penalties would not be material to our financial condition and results of operation we are unable to predict the outcome or the timing of resolution of these matters.

China Joint Ventures

On June 30, 2025, we entered into share purchase agreements with Fosun Industrial Co., Ltd. ("Fosun Industrial," an affiliate of Fosun Pharma) to purchase Fosun Industrial's interest in our two joint ventures, Nature's Sunshine Hong Kong Limited and Shanghai Nature's Sunshine Health Products Co., Ltd., for cash consideration in the amount of $3.9 million and $3.1 million, respectively.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

RESULTS OF OPERATIONS

The following table summarizes our consolidated net income from continuing operations results as a percentage of net sales for the periods indicated:
Year Ended December 31,
2025 | 2024
Net sales | 100.0 | % | 100.0 | %
Cost of sales | (27.6) | (28.5)
Gross profit | 72.4 | 71.5
Operating expenses:
Volume incentives | 30.1 | 30.9
Selling, general and administrative | 37.2 | 36.1
Operating income | 5.1 | 4.5
Other income (expense):
Interest and other income, net | 0.1 | —
Interest expense | — | —
Foreign exchange gains (losses), net | 0.9 | (0.4)
1.0 | (0.4)
Income from operations before provision for income taxes | 6.1 | 4.1
Provision for income taxes | 1.9 | 2.3
Net income | 4.2 | % | 1.8 | %

Net Sales

International operations have provided, and are expected to continue to provide, a significant portion of our total net sales. As a result, total net sales will continue to be affected by fluctuations in the U.S. dollar against foreign currencies. In order to provide a framework for assessing how our underlying businesses performed, excluding the effect of foreign currency fluctuations, in addition to comparing the percent change in net sales from one period to another in U.S. dollars, we present net sales excluding the impact of foreign exchange fluctuations. We compare the percentage change in net sales from one period to another period by excluding the effects of foreign currency exchange as shown below. Net sales excluding the impact of foreign exchange fluctuations is not a U.S. GAAP financial measure and removes from net sales in U.S. dollars the impact of changes in exchange rates between the U.S. dollar and the functional currencies of our foreign subsidiaries by translating the current

period net sales into U.S. dollars using the same foreign currency exchange rates that were used to translate the net sales for the previous comparable period. We believe presenting the impact of foreign currency fluctuations is useful to investors because it allows a more meaningful comparison of net sales of our foreign operations from period to period. However, net sales excluding the impact of foreign currency fluctuations should not be considered in isolation or as an alternative to net sales in U.S. dollar measures that reflect current period exchange rates or to other financial measures calculated and presented in accordance with U.S. GAAP. Throughout the last five years, foreign currency exchange rates have fluctuated significantly. See Item 7A. Quantitative and Qualitative Disclosures About Market Risk .

Year Ended December 31, 2025, as Compared to the Year Ended December 31, 2024

Net Sales

The following table summarizes the changes in net sales by operating segment with a reconciliation to net sales, excluding the impact of currency fluctuations for the years ended December 31, 2025 and 2024 (dollar amounts in thousands).

Net Sales by Operating Segment
2025 | 2024 | Percent Change | Impact of Currency Exchange | Percent Change Excluding Impact of Currency
Asia | 221,777 | 207,794 | 6.7 | % | 668 | 6.4 | %
Europe | 93,133 | 84,837 | 9.8 | % | 1,682 | 7.8 | %
North America | 143,611 | 138,849 | 3.4 | % | (210) | 3.6 | %
Latin America and Other | 21,623 | 22,884 | (5.5) | % | (295) | (4.2) | %
480,144 | 454,364 | 5.7 | % | 1,845 | 5.3 | %

Consolidated net sales for the year ended December 31, 2025, were $480.1 million compared to $454.4 million in 2024, or an increase of approximately 5.7 percent. The increase was related to product sales increases in our Asia, Europe and North America operating segments. Excluding the impact of foreign currency exchange rate fluctuations, consolidated net sales for the year ended December 31, 2025 would have increased by 5.3 percent from 2024.

Asia

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-10_item1_business.md)

Item 1. Business

The Company

We are a natural health and wellness company primarily engaged in the manufacturing and direct selling of nutritional and personal care products. We are a Utah corporation formed in 1976 with our principal place of business in Lehi, Utah. We sell our products to a sales force of independent consultants who use the products themselves or resell them to consumers.

Business Segments

We have four business segments (Asia, Europe, North America and Latin America and Other) based primarily upon the geographic region where each segment operates, as well as the internal organization of our officers and their responsibilities. The geographic segments operate under the Nature's Sunshine Products and Synergy WorldWide® brands. The Latin America and Other segment includes our wholesale business in which we sell products to various locally-managed entities, independent of the Company, that we have granted distribution rights for the relevant market.

Product Categories

Our line of over 800 products includes several different product classifications, such as immune, cardiovascular, digestive, personal care, weight management and other general health products. We purchase herbs and other raw materials in bulk, and after quality control testing, we formulate, encapsulate, tablet or concentrate them, label and package them for shipment. Most of our products are manufactured at our facility in Spanish Fork, Utah. Contract manufacturers produce some of our products in accordance with our specifications and standards. We have implemented quality control procedures to verify that our contract manufacturers have complied with our specifications and standards.

A summary of the U.S. dollar amounts from the sale of general health, immune, cardiovascular, digestive, personal care and weight management products for the years ended December 31, 2025 and 2024, by business segment can be found in Note 12, "Business Segment and International Operation Information," to our Consolidated Financial Statements, in Item 8, Part 2 of this report.

The following table summarizes the Company's product lines by category:
Category | Description
General health | We distribute a wide selection of general health products. The general health line is a combination of assorted health products related to blood sugar support, bone health, cellular health, cognitive function, joint health, mood, sexual health, sleep, sports and energy and vision.
Immune | We distribute immune products. The immune line has been designed to offer products that support and strengthen the human immune system.
Cardiovascular | We distribute cardiovascular products. The cardiovascular line has been designed to offer products that combine a variety of superior heart health ingredients to give the cardiovascular system optimum support.
Digestive | We distribute digestive products. The digestive line has been designed to offer products that regulate intestinal and digestive functions in support of the human digestive system.
Personal care | We distribute a variety of personal care products for external use, including oils and lotions, aloe vera gel, herbal shampoo, herbal skin treatment, toothpaste and skin cleanser.
Weight management | We distribute a variety of weight management products. The weight management line has been designed to simplify the weight management process by providing healthy meal replacements and products that increase caloric burn rate.

Distribution and Marketing

We market our products primarily through our network of independent consultants, who market our products to customers through direct selling techniques. We seek to motivate and provide incentives to our independent consultants by offering high quality products and providing independent consultants with product support, training seminars, sales conventions, travel programs and financial incentives.

Our products sold in the United States are shipped directly from our manufacturing and warehouse facilities located in Spanish Fork, Utah, as well as from our regional warehouses located in Georgia, Ohio and Texas. Many of our international operations maintain warehouse facilities and inventory to supply their independent consultants. However, in foreign markets where we do not maintain warehouse facilities, we have contracted with third-parties to distribute our products and provide support services to our force of independent consultants.

In the United States, we generally sell our products on a cash or credit card basis. From time to time, our U.S. operations extend short-term credit associated with product promotions. For certain of our international operations, we use independent distribution centers and offer credit terms that are generally consistent with industry standards within each respective country.

We pay sales commissions, or "volume incentives" to our independent consultants based upon their own product sales and the product sales of their sales organization. As an exception, in China we do not pay volume incentives; rather, we pay independent service fees, which are included in selling, general and administrative expense. These volume incentives are recorded as an expense in the year earned. The amounts of volume incentives that we expensed during the years ended December 31, 2025 and 2024, are set forth in our Consolidated Financial Statements in Item 8 of this report. In addition to the opportunity to receive volume incentives, independent consultants who attain certain levels of monthly product sales are eligible for additional incentive programs including automobile allowances, sales convention privileges and travel awards.

Source and Availability of Raw Materials

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-10_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-10_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-10_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-10_item7_mdna.md, 10-K_2026-03-10_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
