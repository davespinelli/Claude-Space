# Triage pack — VTS · Vitesse Energy, Inc.

_Generated 2026-09-04 21:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** VTS · **Name:** Vitesse Energy, Inc.
- **CIK:** 0001944558
- **SIC:** 1311 — Crude Petroleum & Natural Gas
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/VTS

**Fetcher warnings for this ticker:** 10-K 2026-03-02: heading split missed Item 1 - Business

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Vitesse Energy, Inc.
- **CIK:** 1,944,558 · **SIC:** 1311 (Crude Petroleum & Natural Gas) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermLineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 17.41 |
| mktcap | $733.0M |
| ev | $890.7M |
| ev_ebit | 52.0x |
| fcf | $170.3M |
| fcf_yield | 23.2% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 1.7% |
| net_debt | $157.6M |
| net_debt_ebit | 9.2x |
| cash | $884k |
| ltd | $158.5M |
| equity | $623.9M |
| ltd_tag | LongTermLineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $274.0M |
| revenue_prior | $242.0M |
| rev_growth | 13.2% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $17.1M |
| net_income | $25.3M |
| cfo | $170.3M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 9.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 42,104,317 |
| shares_py | 38,613,632 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -32.8% |
| r6m | -5.1% |
| off_52w_high | -26.3% |
| adv20 | $7.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.91 |
| r_ev_ebit | 0.13 |
| r_roic | 0.37 |
| r_rev_growth | 0.73 |
| r_buyback | 0.14 |
| score | 0.45 |

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
| rank | 288 |

**Screen rationale:** top-quartile FCF yield 23.2%


## 3. Share count trend

- Shares outstanding: **42,104,317** (CY2026Q2I) vs **38,613,632** prior year (CY2025Q2I)
- Change: **9.0%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-03-26** — Item 5.02 (officer / director change or comp arrangement): Resignation of Robert W. Gerrity as Chief Executive Officer and Chairman
- **2026-03-13** — Item 5.02 (officer / director change or comp arrangement): On March 11, 2026, Bruce Chernoff notified the Board of Directors of Vitesse Energy, Inc. (the "Company") of his resignation as a director of the Company effective March 13, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 110,000 sh / $1,851,136 vs sells 0 sh / $0 -> net $1,851,136 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: STEINBERG JOSEPH S bought 59,118 sh @ $17.00 ($1,005,006) on 2026-05-28.

Form 4 filings parsed: 12; transaction rows: 12 (open-market buys 3, sales 0).

| code | rows |
|---|---|
| A | 8 |
| G | 1 |
| P | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-03_2-02-results.md)

_Extraction: started at the first release heading, 'GREENWOOD VILLAGE, Colo. – August 3, 2026 – Vitesse Energy, Inc. (NYSE'; skipped 11 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (a2q2026earningspressreleas.htm)

GREENWOOD VILLAGE, Colo. – August 3, 2026 – Vitesse Energy, Inc. (NYSE: VTS) ("we," "our," "Vitesse," or the "Company") today reported the Company's second quarter 2026 financial and operating results.

SECOND QUARTER 2026 HIGHLIGHTS

• As previously announced, declared a quarterly cash dividend of $0.4375 per common share to be paid on September 30, 2026

• Net income of $33.1 million and Adjusted Net Income (1) of $1.8 million, including a non-cash unrealized gain on commodity derivatives of $40.2 million

• Adjusted EBITDA (1) of $40.2 million

• Cash flow from operations of $25.4 million and Free Cash Flow (1) of $16.3 million

• Production of 17,354 barrels of oil equivalent ("Boe") per day (60% oil)

• Total cash capital expenditures of $20.7 million

• Total debt of $158.5 million and Net Debt to Adjusted EBITDA ratio (1) of 1.0

(1) Non-GAAP financial measure; see reconciliation schedules at the end of this release

MANAGEMENT COMMENTS

"In the second quarter, Vitesse's capital allocation strategy continued to deliver results, with production increasing 9% from the previous quarter following the successful integration of the Powder River Basin assets acquired in April," stated Jamie Benard, Vitesse's Chief Executive Officer and President. "While we've received a number of questions about whether Vitesse's strategy has changed, the answer is simple: it has not. We will continue to prioritize a durable fixed dividend, allocate capital only where returns exceed our hurdle rates and maintain a strong balance sheet. With our third quarter dividend now declared, Vitesse has returned capital to stockholders for fifteen consecutive quarters since becoming a public company."

STOCKHOLDER RETURNS

On July 29, 2026, Vitesse declared its third quarter cash dividend of $0.4375 per share for stockholders of record as of September 15, 2026, which will be paid on September 30, 2026.

On June 30, 2026, the Company paid its second quarter cash dividend of $0.4375 per share to common stockholders of record as of June 15, 2026.

FINANCIAL AND OPERATING RESULTS

Second quarter net income was $33.1 million and Adjusted Net Income was $1.8 million. Adjusted EBITDA was $40.2 million. See "Non-GAAP Financial Measures" below.

Oil and natural gas production for the second quarter of 2026 averaged 17,354 Boe per day, a sequential increase of 9% from the first quarter of 2026. Oil represented 60% of production and 95% of total oil and natural gas revenue. Total revenue, including the effects of our realized hedges, was $72.8 million.

Vitesse's average realized oil and natural gas prices before hedging were $91.98 per Bbl and $1.17 per Mcf, respectively, during the second quarter of 2026. The Company had hedges covering 84% of oil production and its realized oil price with hedging was $71.14 per Bbl. Its realized natural gas price with hedging was $1.55 per Mcf.

Lease operating expenses in the second quarter of 2026 were $18.0 million, or $11.38 per Boe. General and administrative expenses totaled $6.2 million, or $3.89 per Boe.

LIQUIDITY AND CAPITAL EXPENDITURES

As of June 30, 2026, Vitesse had $0.9 million in cash and $158.5 million of borrowings outstanding on its revolving credit facility. Vitesse had total liquidity of $117.4 million as of June 30, 2026, consisting of cash and $116.5 million of committed borrowing availability under its revolving credit facility.

During the second quarter of 2026, Vitesse invested $21.1 million in development capital expenditures and acquired $0.7 million of oil and gas properties. Vitesse also recorded a $1.1 million purchase price adjustment received on the Powder River Basin Acquisition in the second quarter of 2026.

OPERATIONS UPDATE

As of June 30, 2026, the Company owned an interest in 305 gross (6.4 net) wells that were either drilling or in the completion phase, and another 363 gross (13.0 net) locations that had been permitted for development.

REVISED 2026 ANNUAL GUIDANCE

Vitesse tightened its 2026 annual guidance in response to second quarter results and recent market conditions as set forth below:

Prior 2026 Guidance | Revised 2026 Guidance
Annual Production (Boe per day) | 16,000 - 17,500 | 16,300 - 17,200
Oil as a Percentage of Annual Production | 60% - 64% | 60% - 62%
Total Cash Capital Expenditures ($ in millions) | $50 - $80 | $65 - $80

SECOND QUARTER 2026 RESULTS

The following table sets forth selected financial and operating data for the periods indicated.

THREE MONTHS ENDED JUNE 30, | INCREASE (DECREASE)
($ in thousands, except production and per unit data) | 2026 | 2025 | AMOUNT | PERCENT
Financial and Operating Results:
Revenue
Oil | 86,507 | 66,611 | 19,896 | 30 | %
Natural gas | 4,497 | 15,144 | (10,647) | (70 | %)
Total revenue | 91,004 | 81,755 | 9,249 | 11 | %
Operating Expenses
Lease operating expense | 17,975 | 19,629 | (1,654) | (8 | %)
Production taxes | 8,459 | 6,180 | 2,279 | 37 | %
General and administrative | 6,150 | 311 | 5,839 | *
Depletion, depreciation, amortization, and accretion | 34,809 | 34,576 | 233 | 1 | %
Equity-based compensation | 2,735 | 2,403 | 332 | 14 | %
Interest Expense | 3,022 | 2,539 | 483 | 19 | %
Commodity Derivative Gain, Net | 22,043 | 18,451 | 3,592 | 19 | %
Income Tax (Benefit) Expense | 6,776 | 9,871 | (3,095) | (31 | %)
Production Data:
Oil (MBbls) | 940 | 1,119 | (179) | (16 | %)
Natural gas (MMcf) | 3,832 | 3,630 | 202 | 6 | %
Combined volumes (MBoe) | 1,579 | 1,724 | (145) | (8 | %)
Daily combined volumes (Boe/d) | 17,354 | 18,950 | (1,596) | (8 | %)
Average Realized Prices before Hedging:
Oil (per Bbl) | 91.98 | 59.50 | 32.48 | 55 | %
Natural gas (per Mcf) | 1.17 | 4.17 | (3.00) | (72 | %)
Combined (per Boe) | 57.63 | 47.41 | 10.22 | 22 | %
Average Realized Prices with Hedging:
Oil (per Bbl) | 71.14 | 64.21 | 6.93 | 11 | %
Natural gas (per Mcf) | 1.55 | 4.17 | (2.62) | (63 | %)
Combined (per Boe) | 46.12 | 50.47 | (4.35) | (9 | %)
Average Costs (per Boe):
Lease operating | 11.38 | 11.38 | — | — | %
Production taxes | 5.36 | 3.58 | 1.78 | 50 | %
General and administrative | 3.89 | 0.18 | 3.71 | *
Depletion, depreciation, amortization, and accretion | 22.04 | 20.05 | 1.99 | 10 | %

*Not meaningful.

COMMODITY HEDGING

Vitesse hedges a portion of its expected oil and natural gas production volumes to increase the predictability and certainty of its cash flow and to help maintain a strong financial position to support its dividend. Based on the midpoint of its revised 2026 guidance, Vitesse has approximately 70% of its remaining 2026 oil production hedged and approximately 48% of its remaining 2026 two-stream natural gas production hedged through its natural gas and natural gas liquids hedges. The following tables summarize Vitesse's open commodity derivative contracts scheduled to settle after June 30, 2026.

Crude oil swaps:

INDEX | SETTLEMENT PERIOD | VOLUME HEDGED (Bbls) | WEIGHTED AVERAGE FIXED PRICE
WTI-NYMEX | Q3 2026 | 490,679 | $65.01
WTI-NYMEX | Q4 2026 | 457,155 | $64.97
WTI-NYMEX | Q1 2027 | 270,000 | $69.25
WTI-NYMEX | Q2 2027 | 480,000 | $68.05
WTI-NYMEX | Q3 2027 | 495,000 | $68.38
WTI-NYMEX | Q4 2027 | 465,000 | $67.88
WTI-NYMEX | Q1 2028 | 360,000 | $70.60
WTI-NYMEX | Q2 2028 | 360,000 | $70.60
WTI-NYMEX | Q3 2028 | 360,000 | $70.60
WTI-NYMEX | Q4 2028 | 270,000 | $70.80
WTI-NYMEX | Q1 2029 | 180,000 | $66.50
WTI-NYMEX | Q2 2029 | 180,000 | $66.50
WTI-NYMEX | Q3 2029 | 180,000 | $66.50
WTI-NYMEX | Q4 2029 | 180,000 | $66.50

Crude oil collars:

INDEX | SETTLEMENT PERIOD | VOLUME HEDGED (Bbls) | WEIGHTED AVERAGE FLOOR/CEILING PRICE
WTI-NYMEX | Q3 2026 | 213,000 | $61.62 / $72.58
WTI-NYMEX | Q4 2026 | 168,000 | $58.04 / $67.51
WTI-NYMEX | Q1 2027 | 300,000 | $55.75 / $66.44
WTI-NYMEX | Q2 2027 | 45,000 | $60.00 / $64.25

Natural gas collars:

INDEX | SETTLEMENT PERIOD | VOLUME HEDGED (MMBtu) | WEIGHTED AVERAGE FLOOR/CEILING PRICE
Henry Hub-NYMEX | Q3 2026 | 1,510,800 | $3.73 / $4.90
Henry Hub-NYMEX | Q4 2026 | 1,452,700 | $3.73 / $4.90
Henry Hub-NYMEX | Q1 2027 | 795,000 | $4.00 / $5.68

Natural gas basis swaps:

INDEX | SETTLEMENT PERIOD | VOLUME HEDGED (MMBtu) | WEIGHTED AVERAGE FIXED PRICE
Chicago City Gate to Henry Hub | Q3 2026 | 1,510,800 | $(0.100)
Chicago City Gate to Henry Hub | Q4 2026 | 1,452,700 | $(0.100)
Chicago City Gate to Henry Hub | Q1 2027 | 795,000 | $0.300

Natural gas liquids swaps:

SETTLEMENT PERIOD | VOLUME HEDGED (Bbls) | WEIGHTED AVERAGE FIXED PRICE
2H 2026 | 129,738 | $31.77
2027 | 115,714 | $32.92

The following table presents Vitesse's settlements on commodity derivative instruments and unsettled gains and losses on open commodity derivative instruments for the periods presented:

THREE MONTHS ENDED JUNE 30,
(in thousands) | 2026 | 2025
Realized (loss) gain on commodity derivatives (1) | (18,170) | 5,271
Unrealized gain on commodity derivatives (1) | 40,213 | 13,180
Total commodity derivative gain | 22,043 | 18,451

(1) Realized and unrealized gains and losses on commodity derivatives are presented herein as separate line items but are combined for a total commodity derivative gain (loss) in the statements of operations included below. Management believes the separate presentation of the realized and unrealized commodity derivative gains and losses is useful, providing a better understanding of our hedge position.

SECOND QUARTER 2026 EARNINGS CONFERENCE CALL

In conjunction with Vitesse's release of its financial and operating results, investors, analysts and other interested parties are invited to listen to a conference call with management on Tuesday, August 4, 2026 at 11:00 a.m. Eastern Time.

An updated corporate slide presentation that may be referenced on the conference call will be posted prior to the conference call on Vitesse's website, www.vitesse-vts.com, in the "Investor Relations" section of the site, under "News & Events," sub-tab "Presentations."

Those wishing to listen to the conference call may do so via the Company's website or by phone as follows:

Website: https://event.choruscall.com/mediaframe/webcast.html?webcastid=GpKD5XwJ

Dial-In Number: 877-407-0778 (US/Canada) and +1 201-689-8565 (International)

Conference ID: 13761677 - Vitesse Energy Second Quarter 2026 Earnings Call

Replay Dial-In Number: 877-660-6853 (US/Canada) and +1 201-612-7415 (International)

Replay Access Code: 13761677 - Replay will be available through August 11, 2026

UPCOMING INVESTOR EVEN TS

Vitesse management will participate in the following upcoming investo r events:

• EnerCom Denver Energy Conference - Denver - August 18-19, 2026

• Midwest IDEAS Conference - Chicago - August 27, 2026

Any investor presentations to be used for this event will be posted prior to the event on Vitesse's website, www.vitesse-vts.com, in the "Investor Relations" section of the site, under "News & Events," sub-tab "Presentations."

ABOUT VITESSE ENERGY, INC.

Vitesse Energy, Inc. is focused on returning capital to stockholders through owning financial interests predominantly as a non-operator in oil and gas wells drilled by leading U.S. operators.

More information about Vitesse can be found at www.vitesse-vts.com.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-02_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Executive Overview

Our business strategy is focused on creating long-term stockholder value through the profitable acquisition, development and production of oil and natural gas assets that provide an attractive return on invested capital, while maintaining a strong balance sheet and distributing a meaningful dividend to our stockholders. We invest in working and mineral interests in oil and natural gas properties with our core area of focus currently in the Bakken and Three Forks formations of the Williston Basin of North Dakota and Montana. We also have interests in wells in the Denver-Julesburg Basin located in Colorado and Wyoming and the Powder River Basin located in Wyoming. As of December 31, 2025, we had a working interest in 6,402 gross (226.1 net) productive wells and 283 gross (6.1 net) wells that were being drilled or completed, and an additional 336 gross (15.9 net) wells that had been permitted for development by us or our operators. In addition, we had a royalty only interest in 1,301 gross (3.2 net) productive wells.

Our financial and operating performance for the year ended December 31, 2025 included the following:

■ Paid $92.1 million in dividends to our equity holders.

■ Production of 17,444 Boe/d with 65% of production from oil.

■ Total revenue of $274.0 million.

■ Net income of $25.3 million.

■ Cash flows from operations of $170.3 million.

■ Invested $127.7 million in capital development and acquisitions.

■ Proved reserves of 47.8 MMBoe and $473 million PV-10 value at December 31, 2025, as estimated by our third-party reserve engineers using SEC guidelines.

■ Total debt of $124.5 million at December 31, 2025.

See Non-GAAP Financial Information for additional information about PV-10.

On March 7, 2025, we closed the Lucero Acquisition pursuant to which we acquired Lucero in an all-stock transaction. Lucero shareholders received 8,169,368 shares of Vitesse common stock. Lucero is an oil and natural gas operator with assets in the Bakken and Three Forks formations in the Williston Basin area of North Dakota.

Industry Trends Impacting Our Business

Commodity prices are a significant factor impacting our earnings, operating cash flows and our acquisition and divestiture strategy, as well as the decisions of us and our operators in conducting operations. During the last several years, prices for oil and natural gas have experienced periodic downturns and sustained volatility, impacted by general economic and political conditions, the conflict between Russia and Ukraine, hostilities in the Middle East, the evolving situation in Venezuela, supply chain constraints, elevated interest rates and costs of capital, and changes in production by OPEC and its key member, Saudi Arabia, and certain other non-OPEC oil-producing countries.

As a result of such commodity price volatility, which we expect to continue throughout 2026, our earnings and operating cash flows can vary substantially. While we do hedge a substantial portion of our production, we are still significantly subject to movements in commodity prices. Such volatility can make it difficult to predict future effects on our financial results and the decisions of our operators. Factors that we expect will continue to impact commodity prices include product demand connected with global economic conditions, inflationary factors, industry production and inventory levels, the United States Department of Energy's planned repurchases (or possible releases) of oil from the strategic petroleum reserve, technology advancements, production quotas or other actions imposed by OPEC and other oil-producing countries, the

imposition of and changes in tariffs and other controls on imports and exports and resulting consequences of such, actions of regulators, and regional supply interruptions or fears thereof that may be caused by military conflicts, civil unrest or political uncertainty, including a prolonged U.S. government shutdown. Any of the foregoing can have a substantial impact on the prices of oil and natural gas, which in turn impacts our decisions and the decision of our operators to drill and extract resources.

Source of Our Revenues

We derive our revenues from the sale of oil and natural gas produced from our properties. Revenues are a function of the volume produced, the prevailing market price at the time of sale, oil quality, Btu content and transportation costs to market. We use derivative instruments to hedge future sales prices on a substantial, but varying, portion of our oil and natural gas production. We expect our derivative activities will help us achieve more predictable cash flows and reduce our exposure to downward price fluctuations. The use of derivative instruments has in the past, and may in the future, prevent us from realizing the full benefit of upward price movements but also mitigates the effects of declining price movements.

Principal Components of Our Cost Structure

Commodity price differentials. The price differential between our wellhead price for oil and the WTI benchmark price is primarily driven by the cost to transport oil via pipeline, train or truck to refineries. The price differential between our wellhead price for natural gas and the NYMEX benchmark price is primarily driven by Btu content along with gathering, processing and transportation costs.

Commodity derivatives gain (loss), net. We utilize commodity derivative financial instruments to reduce our exposure to fluctuations in the prices of oil and natural gas. Gain (loss) on commodity derivatives, net is comprised of (1) cash gains and losses we recognize on settled commodity derivatives during the period, and (2) non-cash mark-to-market gains and losses we incur on commodity derivative instruments outstanding at period-end.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Year Ended December 31, 2025 Compared with Year Ended December 31, 2024

The following table sets forth selected operating data for the periods indicated.

YEAR ENDED DECEMBER 31, | INCREASE (DECREASE)
($ in thousands, except per unit data) | 2025 | 2024 | AMOUNT | PERCENT
Operating Results:
Revenue
Oil | 244,414 | 230,164 | 14,250 | 6 | %
Natural gas | 29,575 | 11,834 | 17,741 | 150 | %
Total revenue | 273,989 | 241,998 | 31,991 | 13 | %
Operating Expenses
Lease operating expense | 69,535 | 47,599 | 21,936 | 46 | %
Production taxes | 23,354 | 21,500 | 1,854 | 9 | %
General and administrative | 24,314 | 23,510 | 804 | 3 | %
Depletion, depreciation, amortization, and accretion | 129,411 | 100,308 | 29,103 | 29 | %
Equity-based compensation | 10,246 | 8,110 | 2,136 | 26 | %
Interest Expense | 10,205 | 9,980 | 225 | 2 | %
Income Tax Expense | 9,798 | 7,672 | 2,126 | 28 | %
Commodity Derivative Gain (Loss) | 27,930 | (2,348) | 30,278 | *
Production Data:
Oil (MBbls) | 4,133 | 3,291 | 842 | 26 | %
Natural gas (MMcf) | 13,403 | 8,809 | 4,594 | 52 | %
Combined volumes (MBoe) | 6,367 | 4,759 | 1,608 | 34 | %
Daily combined volumes (Boe/d) | 17,444 | 13,003 | 4,441 | 34 | %
Average Realized Prices before Hedging:
Oil (per Bbl) | 59.14 | 69.94 | (10.80) | (15 | %)
Natural gas (per Mcf) | 2.21 | 1.34 | 0.87 | 65 | %
Combined (per Boe) | 43.03 | 50.85 | (7.82) | (15 | %)
Average Realized Prices with Hedging:
Oil (per Bbl) | 62.95 | 71.48 | (8.53) | (12 | %)
Natural gas (per Mcf) | 2.31 | 1.34 | 0.97 | 72 | %
Combined (per Boe) | 45.72 | 51.91 | (6.19) | (12 | %)
Average Costs (per Boe):
Lease operating expense | 10.92 | 10.00 | 0.92 | 9 | %
Production taxes | 3.67 | 4.52 | (0.85) | (19 | %)
General and administrative | 3.82 | 4.94 | (1.12) | (23 | %)
Depletion, depreciation, amortization, and accretion | 20.33 | 21.08 | (0.75) | (4 | %)

*Not meaningful

Oil and Natural Gas Revenue and Volumes. Oil and natural gas revenue increased to $274.0 million for the year ended December 31, 2025 from $242.0 million for the year ended December 31, 2024. The increase in oil and natural gas revenue was due to a 34% increase in production volumes, and was partially offset by a 15% decrease in the average realized prices per Boe before hedging for the year ended December 31, 2025. The increase in production volumes increased oil and natural gas revenue by approximately $69.2 million, while the decrease in average realized prices per Boe before hedging decreased oil and natural gas revenue by approximately $37.2 million. The increase in production volumes was in part due to the Lucero Acquisition.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-02_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-02_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-03_2-02-results.md, 10-K_2026-03-02_item7_mdna.md

**Missing:** 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
