# Triage pack — XHR · Xenia Hotels & Resorts, Inc.

_Generated 2026-09-04 15:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** XHR · **Name:** Xenia Hotels & Resorts, Inc.
- **CIK:** 0001616000
- **SIC:** 7011 — Hotels & Motels
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/XHR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Xenia Hotels & Resorts, Inc.
- **CIK:** 1,616,000 · **SIC:** 7011 (Hotels & Motels) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

**Valuation**

| metric | value |
|---|---|
| price | 18.15 |
| mktcap | $1.7B |
| ev | $2.9B |
| ev_ebit | 27.2x |
| fcf | $176.5M |
| fcf_yield | 10.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 3.6% |
| net_debt | $1.2B |
| net_debt_ebit | 11.6x |
| cash | $112.4M |
| ltd | $1.4B |
| equity | $1.1B |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $1.1B |
| revenue_prior | $1.0B |
| rev_growth | 3.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $107.5M |
| net_income | $63.1M |
| cfo | $176.5M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | -3.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 92,245,835 |
| shares_py | 95,780,393 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 48.5% |
| r6m | 19.3% |
| off_52w_high | -16.8% |
| adv20 | $12.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.73 |
| r_ev_ebit | 0.32 |
| r_roic | 0.43 |
| r_rev_growth | 0.49 |
| r_buyback | 0.83 |
| score | 0.61 |

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
| rank | 133 |

**Screen rationale:** buying back stock -3.7%; 12-1 momentum 48.5%


## 3. Share count trend

- Shares outstanding: **92,245,835** (CY2026Q2I) vs **95,780,393** prior year (CY2025Q2I)
- Change: **-3.7%** — buyback / shrinking count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 4 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 144,916 sh / $2,455,748 -> net $-2,455,748 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 10 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'XENIA HOTELS & RESORTS REPORTS SECOND QUARTER 2026 RESULTS'; skipped 8 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ex991q22026xhrearningsrele.htm)

XENIA HOTELS & RESORTS REPORTS SECOND QUARTER 2026 RESULTS

Orlando, FL – July 30, 2026 – Xenia Hotels & Resorts, Inc. (NYSE: XHR) ("Xenia" or the "Company") today announced results for the quarter ended June 30, 2026 .

Second Quarter 2026 Highlights

• Net Loss: Net loss attributable to common stockholders was $19.3 million, compared to net income attributable to common stockholders of $55.2 million in the second quarter of 2025

• Net Loss per Diluted Share: Net loss attributable to common stockholders per diluted share was $0.21, a $0.77 decrease compared to net income attributable to common stockholders per diluted share of $0.56 in the second quarter of 2025

• Adjusted EBITDAre : $78.1 million, decreased 1.8% compared to the second quarter of 2025

• Adjusted FFO per Diluted Share: $0.61, increased 7.0% compared to the second quarter of 2025

• Same-Property Occupancy: 72.3%, flat compared to the second quarter of 2025

• Same-Property ADR: $285.71, increased 5.7% compared to the second quarter of 2025

• Same-Property RevPAR: $206.54, increased 5.6% compared to the second quarter of 2025

• Same-Property Total RevPAR: $366.17, increased 3.3% compared to the second quarter of 2025

• Same-Property Hotel EBITDA : $84.9 million, increased 1.0% compared to the second quarter of 2025

• Same-Property Hotel EBITDA Margin: 28.7%, decreased 65 basis points compared to the second quarter of 2025

• Dividends: Declared a second quarter dividend of $0.14 per share for stockholders of record on June 30, 2026

Year-to-Date 2026 Highlights

• Net Income: Net income attributable to common stockholders was $0.4 million, compared to net income attributable to common stockholders of $70.7 million for the same period in 2025

• Net Income per Diluted Share: Net income attributable to common stockholders per diluted share was $0.00, a $0.71 decrease compared to net income attributable to common stockholders per diluted share of $0.71 for the same period in 2025

• Adjusted EBITDAre: $159.5 million, increased 4.6% compared to the same period in 2025

• Adjusted FFO per Diluted Share: $1.24, increased 14.8% compared to the same period in 2025

• Same-Property Occupancy: 71.8%, increased 80 basis points compared to the same period in 2025

• Same-Property ADR: $287.14, increased 5.2% compared to the same period in 2025

• Same-Property RevPAR: $206.24, increased 6.5% compared to the same period in 2025

• Same-Property Total RevPAR: $368.14, increased 5.2% compared to the same period in 2025

• Same-Property Hotel EBITDA: $172.7 million, increased 9.0% compared to the same period in 2025

• Same-Property Hotel EBITDA Margin: 29.2%, increased 100 basis points compared to the same period in 2025

• Financing Activity: In February, the Company paid off the $52 million mortgage loan secured by Grand Bohemian Hotel Orlando, Autograph Collection.

"Despite challenging comparisons to the second quarter of 2025, our portfolio delivered another quarter of solid performance which came in ahead of our expectations, with ADR growth driving increases in Same-Property RevPAR and Adjusted FFO per share of 5.6% and 7.0%, respectively." said Marcel Verbaas, Chairman and Chief Executive Officer of Xenia. "The quarter benefitted from encouraging trends across a large and diverse cross-section of our markets which speaks to the quality and diversification of our portfolio. At Grand Hyatt Scottsdale Resort, we continue to track favorably towards stabilization, with this year shaping up to be the strongest group demand year in the resort's history and bookings for future periods continuing to support our expectation for additional growth in the years ahead. The deliberate choices we have made over the years in curating a portfolio of high-quality hotels and resorts, through selective dispositions in addition to acquisitions and targeted value-increasing capital projects, such as the transformational renovation and upbranding of Grand Hyatt Scottsdale, are expected to benefit us as lodging fundamentals continue to improve."

"Our strong balance sheet gives us the flexibility to be active on the transaction front as opportunities arise," continued Mr. Verbaas. "Additionally, we continue to believe our high-quality and well-located portfolio is well-positioned to capitalize on solid ongoing demand for luxury and upper upscale travel. Based on favorable current market conditions, our outperformance in the first half of the year and robust group rooms revenue pace for the second half of the year, we have increased the midpoint of our full year 2026 Adjusted EBITDAre guidance by $7 million compared to the guidance we provided after our first quarter results. The second half of the year is already off to a great start, as we estimate that Same-Property RevPAR for July will increase by approximately 10% compared to July 2025, fueled by substantial RevPAR growth from both the transient and group segments."

Operating Results

The Company's results include the following:

Three Months Ended June 30,
2026 | 2025 | Change
($ amounts in thousands, except hotel statistics and per share amounts)
Net income (loss) attributable to common stockholders | (19,338) | 55,157 | (135.1) | %
Net income (loss) attributable to common stockholders per diluted share | (0.21) | 0.56 | (137.5) | %
Same-Property Number of Hotels (1) | 30 | 30 | —
Same-Property Number of Rooms (1) | 8,868 | 8,868 | —
Same-Property Occupancy (1) | 72.3 | % | 72.3 | % | 0 | bps
Same-Property Average Daily Rate (1) | 285.71 | 270.42 | 5.7 | %
Same-Property RevPAR (1) | 206.54 | 195.51 | 5.6 | %
Same-Property Total RevPAR (1)(2) | 366.17 | 354.50 | 3.3 | %
Same-Property Hotel EBITDA (1)(3) | 84,869 | 84,027 | 1.0 | %
Same-Property Hotel EBITDA Margin (1)(3) | 28.7 | % | 29.4 | % | (65) | bps
Total Portfolio Number of Hotels (4) | 30 | 30 | —
Total Portfolio Number of Rooms (4) | 8,868 | 8,868 | —
Total Portfolio RevPAR (5) | 206.54 | 192.51 | 7.3 | %
Total Portfolio Total RevPAR (2)(5) | 366.17 | 349.28 | 4.8 | %
Adjusted EBITDAre (3) | 78,089 | 79,543 | (1.8) | %
Adjusted FFO (3) | 57,692 | 57,406 | 0.5 | %
Adjusted FFO per diluted share (3) | 0.61 | 0.57 | 7.0 | %

1. "Same-Property" includes all hotels owned as of June 30, 2026 and also includes renovation disruption for multiple capital projects during the periods presented.

2. Total Revenues per available room for the period presented.

3. EBITDA, EBITDAre, Adjusted EBITDAre, FFO, Adjusted FFO, and Same-Property Hotel EBITDA and Hotel EBITDA Margin are non-GAAP financial measures. See definitions and tables later in this press release for how we define these non-GAAP financial measures and for reconciliations from net income to Earnings Before Interest, Taxes, Depreciation and Amortization ("EBITDA"), EBITDA for Real Estate ("EBITDAre"), Adjusted EBITDAre, Funds From Operations ("FFO"), Adjusted FFO, Same-Property Hotel EBITDA and Hotel EBITDA Margin.

4. As of end of periods presented.

5. Results of all hotels as owned during the periods presented, including the results of hotels sold or acquired for the actual period of ownership by the Company.

Six Months Ended June 30,
2026 | 2025 | Change
($ amounts in thousands, except hotel statistics and per share amounts)
Net income attributable to common stockholders | 433 | 70,742 | (99.4) | %
Net income attributable to common stockholders per diluted share | — | 0.71 | (100.0) | %
Same-Property Number of Hotels (1) | 30 | 30 | —
Same-Property Number of Rooms (1) | 8,868 | 8,868 | —
Same-Property Occupancy (1) | 71.8 | % | 71.0 | % | 80 | bps
Same-Property Average Daily Rate (1) | 287.14 | 272.88 | 5.2 | %
Same-Property RevPAR (1) | 206.24 | 193.66 | 6.5 | %
Same-Property Total RevPAR (1)(2) | 368.14 | 349.85 | 5.2 | %
Same-Property Hotel EBITDA (1)(3) | 172,680 | 158,477 | 9.0 | %
Same-Property Hotel EBITDA Margin (1)(3) | 29.2 | % | 28.2 | % | 100 | bps
Total Portfolio Number of Hotels (4) | 30 | 30 | —
Total Portfolio Number of Rooms (4) | 8,868 | 8,868 | —
Total Portfolio RevPAR (5) | 206.24 | 190.59 | 8.2 | %
Total Portfolio Total RevPAR (2)(5) | 368.14 | 345.13 | 6.7 | %
Adjusted EBITDAre (3) | 159,470 | 152,485 | 4.6 | %
Adjusted FFO (3) | 118,246 | 109,466 | 8.0 | %
Adjusted FFO per diluted share (3) | 1.24 | 1.08 | 14.8 | %

1. "Same-Property" includes all hotels owned as of June 30, 2026 and also includes renovation disruption for multiple capital projects during the periods presented.

2. Total Revenues per available room for the period presented.

3. EBITDA, EBITDAre, Adjusted EBITDAre, FFO, Adjusted FFO, and Same-Property Hotel EBITDA and Hotel EBITDA Margin are non-GAAP financial measures. See definitions and tables later in this press release for how we define these non-GAAP financial measures and for reconciliations from net income to Earnings Before Interest, Taxes, Depreciation and Amortization ("EBITDA"), EBITDA for Real Estate ("EBITDAre"), Adjusted EBITDAre, Funds From Operations ("FFO"), Adjusted FFO, Same-Property Hotel EBITDA and Hotel EBITDA Margin.

4. As of end of periods presented.

5. Results of all hotels as owned during the periods presented, including the results of hotels sold or acquired for the actual period of ownership by the Company.

Liquidity and Balance Sheet

As of June 30, 2026, the Company had total outstanding debt of approximately $1.4 billion with a weighted-average interest rate of 5.49%. The Company had approximately $112 million of cash and cash equivalents, including hotel working capital, and full availability on its revolving line of credit, resulting in total liquidity of approximately $612 million as of June 30, 2026. In addition, the Company held approximately $84 million of restricted cash and escrows at the end of the second quarter.

In June, the Company paid down by $5.2 million the mortgage loan collateralized by Andaz Napa.

Capital Markets

The Company did not repurchase any shares of its common stock during the quarter and currently has $97.5 million in capacity remaining under its repurchase authorization. The Company did not issue any shares of its common stock

through its At-The-Market ("ATM") program in the quarter and had $200 million of remaining availability as of June 30, 2026.

Transactions

Subsequent to quarter end, the Company sold the 85-room Kimpton RiverPlace Hotel in Portland, Oregon, for $11 million, or approximately $129,400 per key. The sale price represented a 19.4x multiple and a 2.0% capitalization rate on Hotel EBITDA and Net Operating Income for the trailing twelve months ended June 30, 2026, respectively. These transaction price metrics are exclusive of significant near-term capital expenditures that would have been required. Net proceeds from the sale will be utilized for general corporate purposes, which may include debt repayments, potential acquisitions consistent with the Company's strategy, and/or share repurchases under the Company's existing authorization. In the second quarter, the Company recorded a non-cash impairment charge of $38.8 million related to this property.

Capital Expenditures

During the three and six months ended June 30, 2026, the Company invested $15.4 million and $30.6 million in portfolio improvements, respectively.

During the second quarter, the Company:

• Finalized planning at Royal Palms Resort & Spa for the renovation of guest rooms and corridors in the 68-room Monte Vista Building and a renovation of T. Cook's Restaurant which will take place during the third quarter

• Performed or continued planning mechanical system upgrades at eight hotels and minor guest room upgrades at three hotels which are expected to be completed in 2026

Additionally, the Company made substantial progress preparing for two significant renovations that include:

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-24_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Xenia is a self-advised and self-administered REIT that invests primarily in uniquely positioned luxury and upper upscale hotels and resorts with a focus on the top 25 lodging markets as well as key leisure destinations in the United States ("U.S."). As of December 31, 2025, we owned 30 hotels and resorts, comprising 8,868 rooms across 14 states. Our hotels are primarily operated and/or licensed by industry leaders such as Marriott, Hyatt, Kimpton, Fairmont, Loews, Hilton, and The Kessler Collection.

We plan to grow our business through a differentiated acquisition strategy, proactive asset management and capital investment in our properties. We primarily target markets and sub-markets with particular positive characteristics, such as multiple demand generators, favorable supply and demand dynamics and attractive projected hotel revenue growth. We believe our focus on a broader range of markets allows us to evaluate a greater number of acquisition opportunities and, as a result, be highly selective in our pursuit of only those opportunities that best fit our investment criteria. We own and pursue hotels and resorts in the luxury and upper upscale hotel segments that are affiliated with premium leading brands, as we believe that these segments yield attractive risk-adjusted returns. Within these segments, we focus on hotels and resorts that will provide guests with a distinctive lodging experience and that are tailored to reflect local market environments.

We also target properties that exhibit an opportunity for us to enhance operating performance through proactive asset management and targeted capital investment. While we do not operate our hotel properties, our asset management team and our executive management team monitor and work with our hotel managers by conducting regular revenue, sales, and financial performance reviews and also perform in-depth on-site reviews focused on ongoing operating margin improvement initiatives. We interact frequently with our management companies and on-site management personnel, including conducting regular meetings with key executives of our management companies and brands. Through these efforts, we aim to enhance the guest experience, improve property efficiencies, lower costs, maximize revenues, and grow property operating margins, which we expect will increase long-term returns to our stockholders.

Basis of Presentation

The accompanying consolidated financial statements include the accounts of the Company, the Operating Partnership and XHR Holding. The Company's subsidiaries generally consist of limited liability companies, limited partnerships and the TRS. The effects of all inter-company transactions have been eliminated. Corporate costs directly associated with our executive offices, personnel and other administrative costs are reflected as general and administrative expenses on the consolidated statements of operations and comprehensive income.

Market Outlook

The U.S. lodging industry has historically exhibited a strong correlation to U.S. GDP, which increased at an annual rate of approximately 2.2% during 2025, according to the U.S. Department of Commerce, in comparison to an increase of approximately 2.8% during 2024. The increase in U.S. GDP during the year ended December 31, 2025 reflected increases in consumer spending and investment. During the fourth quarter of 2025, U.S. GDP increased at an annual rate of 1.4%, a decrease from the annual rate increase of 4.4% for the third quarter of 2025. The increase during the fourth quarter of 2025 reflected increases in consumer spending and investment as well as a decrease in imports that were partially offset by decreases in government spending and exports. In addition, the unemployment rate remained flat at 4.4% in December 2025 compared to September 2025 and rose compared to 4.1% in June 2025.

Overall industry lodging demand decreased 0.5% and new hotel supply increased by 0.7% during the year ended December 31, 2025 compared to 2024. Industry RevPAR decreased 0.3% for the year ended December 31, 2025 compared to 2024, which was primarily driven by a 1.2% decrease in occupancy partially offset by a 0.9% increase in ADR. All U.S. data for the year ended December 31, 2025 are per industry reports.

Significant Events

The following significant events occurred during the year ended December 31, 2025:

• In January 2025, we drew the $100 million 2024 Delayed Draw Term Loan and used a portion of the borrowing to repay the then outstanding balance on the Revolving Credit Facility.

• In March 2025, we purchased the fee simple interest in the land associated with the ground lease at Hyatt Regency Santa Clara in Santa Clara, California for a purchase price of $25.4 million including transactions costs.

• In April 2025, we completed the disposition of the 545-room Fairmont Dallas, in Dallas, Texas for a sale price of $111.0 million resulting in a gain on sale of $40.0 million. Net cash proceeds from the sale, after transaction closing costs and other credits, were $101.4 million.

• During the year ended December 31, 2025, 9,353,816 shares were repurchased at a weighted-average price of $12.87 per share for an aggregate purchase price of $120.4 million.

• We invested approximately $86.6 million in portfolio improvements, which we believe will drive positive performance at these properties in the future.

Our Customers

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Operating Results Overview

Our total portfolio RevPAR, which includes the results of hotels sold or acquired for the period of ownership by the Company, increased 4.8% to $180.65 for the year ended December 31, 2025, compared to $172.36 for the year ended December 31, 2024. The increase in our total portfolio RevPAR for the year ended December 31, 2025 compared to the same period in 2024 was driven by increases in occupancy and ADR, disruption from renovations in 2024 and year over year growth at Grand Hyatt Scottsdale Resort due to continued ramp up in performance following its renovation. Further, demand has continued to shift to a

more traditional mix of leisure, business transient and group within our portfolio. Excluding dispositions and Grand Hyatt Scottsdale Resort, which underwent a transformative renovation during 2024, RevPAR increased 0.7% to $181.03 for the year ended December 31, 2025 compared to $179.76 for the year ended December 31, 2024.

Net income increased 296.6% for the year ended December 31, 2025 compared to 2024, which was primarily attributed to:

• a $38.3 million increase on gain on sale of investment properties;

• a $33.7 million increase in hotel operating income for our 30-comparable hotels;

• a $3.9 million reduction in loss on extinguishment of debt; and

• a $0.2 million reduction in impairment and other losses.

These increases were partially offset by:

• an $8.9 million reduction in operating income attributed to the sale of Lorien Hotel & Spa in July 2024 and Fairmont Dallas in April 2025;

• a $5.8 million increase in interest expense;

• income tax expense of $1.4 million in 2025 compared to an income tax benefit of $3.7 million in 2024;

• a $2.0 million increase in depreciation and amortization expense;

• a $1.9 million reduction in other income;

• a $1.8 million reduction in gain on business interruption insurance;

• a $0.5 million increase in general and administrative expenses; and

• a $0.1 million increase in other operating expenses.

Adjusted EBITDAre and Adjusted FFO attributable to common stock and unit holders increased 8.9% and 5.7%, respectively, for the year ended December 31, 2025 compared to 2024. The increase during the year ended December 31, 2025 was primarily attributable to an increase in operating income as well disruption from renovations in 2024 and year over year growth at Grand Hyatt Scottsdale Resort due to continued ramp up in performance following its renovation, partially offset by a reduction in operating income attributed to the sale of Lorien Hotel & Spa in July 2024 and Fairmont Dallas in April 2025. Refer to "Non-GAAP Financial Measures" for the definition of these financial measures, a description of how they are useful to investors as key supplemental measures of our operating performance and the reconciliation of these non-GAAP financial measures to net income attributable to common stock and unit holders.

Portfolio Composition

As of December 31, 2025 and 2024, the Company owned 30 lodging properties with a total of 8,868 rooms and owned 31 lodging properties with a total of 9,408 rooms, respectfully. As of December 31, 2023, the Company owned 32 lodging properties with a total of 9,514 rooms.

The following represents the disposition details for the properties sold in the years ended December 31, 2025 and 2024 (in thousands, except number of rooms):

Property | Date | No. of Rooms | Gross Sale Price
Fairmont Dallas | 04/2025 | 545 | 111,000
Total for the year ended December 31, 2025 | 545 | 111,000
Lorien Hotel & Spa | 07/2024 | 107 | 30,000
Total for the year ended December 31, 2024 | 107 | 30,000

No hotels were sold during the year ended December 31, 2023.

No hotels were acquired during the years ended December 31, 2025, 2024 and 2023.

Comparison of the year ended December 31, 2025 to the year ended December 31, 2024

Operating Information

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-24_item1_business.md)

Item 1. Business

General

Xenia Hotels & Resorts, Inc. is a Maryland corporation that primarily invests in uniquely positioned luxury and upper upscale hotels and resorts with a focus on the top 25 lodging markets as well as key leisure destinations in the United States ("U.S.").

Substantially all of the Company's assets are held by, and all the operations are conducted through XHR LP (the "Operating Partnership"). XHR GP, Inc. is the sole general partner of the Operating Partnership and is wholly-owned by the Company. As of December 31, 2025, the Company collectively owned 94.4% of the common limited partnership units issued by the Operating Partnership ("Operating Partnership Units"). The remaining 5.6% of the Operating Partnership Units are owned by the other limited partners comprised of certain of our executive officers and current or former members of our Board of Directors and includes vested and unvested long-term incentive plan ("LTIP") partnership units. LTIP partnership units may or may not vest based on the passage of time and meeting certain market-based performance objectives.

Xenia operates as a real estate investment trust ("REIT") for U.S. federal income tax purposes. To qualify as a REIT, the Company cannot operate or manage its hotels. Therefore, the Operating Partnership and its subsidiaries lease the hotel properties to XHR Holding, Inc. and its subsidiaries (collectively with its subsidiaries, "XHR Holding"), the Company's taxable REIT subsidiary ("TRS"), which engages third-party eligible independent contractors to manage the hotels. The third-party hotel operators manage each hotel pursuant to a management agreement, the terms of which are discussed in more detail under "Part I-Item 2. Properties - Our Principal Agreements."

The Company's consolidated financial statements include the accounts of the Company, the Operating Partnership, and XHR Holding and each of their wholly-owned subsidiaries. The Company's subsidiaries generally consist of limited liability companies ("LLCs"), limited partnerships ("LPs") and our TRS. The effects of all inter-company transactions are eliminated.

As of December 31, 2025, the Company owned 30 lodging properties with a total of 8,868 rooms.

The Company's principal executive offices are located at 200 S. Orange Avenue, Suite 2700, Orlando, Florida, 32801, and our telephone number is (407) 246-8100. The Company's website is www.xeniareit.com. The information contained on our website, or that can be accessed through our website, neither constitutes part of this Annual Report nor is incorporated by reference herein.

The following chart shows our structure as of December 31, 2025:

(1) Ownership percentages include vested and unvested LTIP partnership units which may or may not vest based on the passage of time and meeting certain market-based performance objectives.

Business Objectives and Growth Strategies

Our objective is to allocate capital in order to invest primarily in a high-quality diversified portfolio of uniquely positioned luxury and upper upscale hotels and resorts with a focus on the top 25 lodging markets as well as key leisure destinations in the United States. We invest at valuation levels that we believe will generate attractive risk-adjusted returns. We pursue this objective through the following investment and growth strategies:

• Follow a Differentiated Investment Strategy Across Targeted Markets. We use our management team's network of relationships in the lodging industry, real estate brokers and our relationships with multiple hotel brands and management companies, among others, to source acquisition opportunities. When evaluating opportunities, we use a multi-pronged approach to investing that we believe provides us the flexibility to pursue attractive opportunities in a variety of markets across any point in the economic cycle. We consider the following characteristics when making investment decisions:

- Market Characteristics. We seek opportunities across a range of urban and dense suburban areas, primarily in the top 25 lodging markets as well as key leisure destinations in the U.S. We believe this strategy provides us with a broader range of opportunities and allows us to target markets and sub-markets with particular positive characteristics, such as multiple demand generators, favorable supply and demand dynamics and attractive long-term projected RevPAR growth. We believe assets in the top 25 lodging markets and key leisure destinations in the U.S. present attractive investment opportunities considering the favorable supply and demand dynamics, RevPAR growth trends, attractive valuations and better opportunities for diversification.

- Asset Characteristics. We generally pursue uniquely positioned hotels in the luxury and upper upscale segments that are affiliated with leading brands as we believe these segments yield attractive risk-adjusted returns. Within these segments, we seek hotels that will provide guests with a distinctive lodging experience, often tailored to reflect local market environments, which draws demand from both business and leisure transient and group business segments. We seek properties with desirable locations within their markets, exceptional facilities, and other competitive advantages that are hard to replicate. We also favor properties that can be purchased below estimated replacement cost. We believe our focus on uniquely positioned luxury and upper upscale hotel assets allows us to seek appropriate investments that are well-suited for specific markets.

- Operational and Structural Characteristics. We pursue both new or recently constructed assets that require limited capital investment, as well as more mature and complex properties with opportunities for our dedicated asset and project management teams to create value through more active operational oversight and targeted capital expenditures.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-24_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-24_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-24_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-30_2-02-results.md, 10-K_2026-02-24_item7_mdna.md, 10-K_2026-02-24_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
