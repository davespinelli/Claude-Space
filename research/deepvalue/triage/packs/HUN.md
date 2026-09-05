# Triage pack — HUN · Huntsman CORP

_Generated 2026-09-05 01:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** HUN · **Name:** Huntsman CORP
- **CIK:** 0001307954
- **SIC:** 2800 — Chemicals & Allied Products
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/HUN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Huntsman CORP
- **CIK:** 1,307,954 · **SIC:** 2800 (Chemicals & Allied Products) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 9.40 |
| mktcap | $1.6B |
| ev | $3.0B |
| ev_ebit | n/a |
| fcf | $116.0M |
| fcf_yield | 7.0% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -2.6% |
| net_debt | $1.3B |
| net_debt_ebit | n/a |
| cash | $369.0M |
| ltd | $1.7B |
| equity | $2.7B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $5.7B |
| revenue_prior | $6.0B |
| rev_growth | -5.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$131.0M |
| net_income | -$284.0M |
| cfo | $289.0M |
| capex | $173.0M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.9% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 175,349,112 |
| shares_py | 173,752,121 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -2.1% |
| r6m | -24.2% |
| off_52w_high | -40.8% |
| adv20 | $21.7M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.59 |
| r_ev_ebit | 0.00 |
| r_roic | 0.24 |
| r_rev_growth | 0.17 |
| r_buyback | 0.47 |
| score | 0.29 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q1I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 415 |

**Screen rationale:** balanced across factors, no single standout


## 3. Share count trend

- Shares outstanding: **175,349,112** (CY2026Q1I) vs **173,752,121** prior year (CY2025Q2I)
- Change: **0.9%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-16** — Item 1.01 (Entry into a Material Definitive): Corporation, a Delaware corporation (" Huntsman " or, with reference to the post-closing period, the " Combined

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 100,000 sh / $981,000 vs sells 0 sh / $0 -> net $981,000 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: Huntsman Peter R bought 100,000 sh @ $9.81 ($981,000) on 2026-08-03.

Form 4 filings parsed: 12; transaction rows: 33 (open-market buys 1, sales 0).

| code | rows |
|---|---|
| A | 9 |
| F | 17 |
| M | 6 |
| P | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'Second Quarter'; skipped 9 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (tm2621698d1_ex99-1.htm)

Second Quarter
Highlights

· | Second quarter 2026 net loss attributable to Huntsman of $6 million compared to a net loss of $158 million in the prior year period; second quarter 2026 diluted loss per share of $0.03 compared to diluted loss per share of $0.92 in the prior year period.

· | Second quarter 2026 adjusted net income attributable to Huntsman of nil compared to adjusted net loss of $34 million in the prior year period; second quarter 2026 adjusted diluted income per share of nil compared to adjusted diluted loss per share of $0.20 in the prior year period.

· | Second quarter 2026 adjusted EBITDA of $120 million compared to $74 million in the prior year period.

· | Second quarter 2026 net cash used in operating activities from continuing operations was $60 million. Free cash flow was a use of cash of $90 million for the second quarter 2026 compared to a source of cash of $55 million in the prior year period.

· | On June 16, 2026, we announced that we signed an agreement to complete an all-stock merger of equals with Olin Corporation.

Three months ended | Six months ended
June 30, | June 30,
In millions, except per share amounts | 2026 | 2025 | 2026 | 2025
Revenues | 1,663 | 1,458 | 3,083 | 2,868
Net loss attributable to Huntsman Corporation | (6 | (158 | (59 | (163
Adjusted net income (loss) (1) | - | (34 | (35 | (53
Diluted loss per share | (0.03 | (0.92 | (0.34 | (0.94
Adjusted diluted income (loss) per share (1) | - | (0.20 | (0.20 | (0.31
Adjusted EBITDA (1) | 120 | 74 | 193 | 146
Net cash (used in) provided by operating activities from continuing operations | (60 | 92 | (113 | 21
Free cash flow (2) | (90 | 55 | (181 | (52

See
end of press release for footnote explanations and reconciliations of non-GAAP measures.

THE WOODLANDS, Texas –
Huntsman Corporation (NYSE: HUN) today reported second quarter 2026 results with revenues of $1,663 million, net loss attributable to
Huntsman of $6 million, adjusted net income attributable to Huntsman of nil and adjusted EBITDA of $120 million.

Peter R. Huntsman,
Chairman, President, and CEO, commented:

"We delivered a solid quarter,
supported by higher volumes across all three segments and pricing actions that offset a significant increase in raw material costs. Improved
industrial demand helped counter continued softness in construction. Rising and volatile energy and crude oil related costs, particularly
in Europe, remain a headwind, and we will stay focused on additional price increases and cost-reduction initiatives to help offset these
pressures.

Our planned merger of equals with
Olin Corporation continues to progress at pace. The strong collaboration between our teams reinforces my confidence in our ability to
deliver the synergy targets we have outlined. We also expect the combined company to benefit from vertical integration, greater scale,
and a stronger financial profile, creating meaningful value for shareholders of both companies. The stockholder vote is scheduled for
August 25, 2026, and we are excited about the future of OlinHuntsman."

Segment Analysis for 2Q26 Compared
to 2Q25

Polyurethanes

The increase in revenues in our Polyurethanes
segment for the three months ended June 30, 2026 compared to the same period of 2025 was primarily due to higher average selling
prices and higher sales volumes. MDI average selling prices increased across all three regions due to improved supply and demand dynamics.
MDI sales volumes increased in the Americas and Europe regions. The increase in segment adjusted EBITDA was primarily due to higher average
selling prices, higher sales volumes, higher equity earnings from our minority-owned joint venture in China and cost savings achieved
from our cost optimization program, partially offset by higher raw materials costs.

Performance Products

The increase in revenues in our Performance
Products segment for the three months ended June 30, 2026 compared to the same period of 2025 was primarily due to higher sales
volumes and slightly higher average selling prices. Sales volumes increased primarily due to favorable demand in our performance amines
business. Average selling prices increased primarily due to higher raw materials costs. The increase in segment adjusted EBITDA was primarily
due to higher sales volumes and lower fixed costs achieved from our cost optimization program.

Advanced Materials

The increase in revenues in our Advanced
Materials segment for the three months ended June 30, 2026 compared to the same period of 2025 was primarily due to higher average
selling prices and higher sales volumes. Average selling prices increased primarily due to favorable sales mix and the positive impact
of major foreign currency exchange rate movements against the U.S. dollar. Sales volumes increased primarily in our aerospace, power
and automotive markets. The increase in segment adjusted EBITDA was primarily due to higher margins and higher sales volumes.

Liquidity and Capital Resources

During the three months ended June 30,
2026, our free cash flow used was $90 million as compared to a source of cash of $55 million in the same period of 2025. As of June 30,
2026, we had approximately $0.9 billion of combined cash and unused borrowing capacity.

- 2 -

During the three months ended June 30,
2026, we spent $30 million on capital expenditures as compared to $37 million in the same period of 2025. During 2026, we expect capital
expenditures to be approximately $170 million.

Income Taxes

In the second quarter of 2026, our effective
tax rate was 65% and our adjusted effective tax rate was 61%.

Earnings Conference Call Information

We will hold a conference call to discuss
our second quarter 2026 financial results on Friday, July 31, 2026, at 10:00 a.m. ET.

Webcast link: https://event.choruscall.com/mediaframe/webcast.html?webcastid=r4UuXqgQ

Participant dial-in numbers:

Domestic callers: | (877) 402-8037
International callers: | (201) 378-4913

The conference call will be accompanied
by presentation slides that will be accessible via the webcast link and Huntsman's investor relations website, www.huntsman.com/investors .
Upon conclusion of the call, the webcast replay will be accessible via Huntsman's website.

Upcoming Conferences

During the third quarter 2026, a member
of management is expected to present at:

Seaport Summer Investor Conference,
August 18, 2026

UBS Conference, September 9, 2026

Jefferies Industrials Conference, September 10,
2026

Alembic Conference, September 14,
2026

Deutsche Bank Leveraged Finance Conference,
September 28, 2026

A webcast of the presentation, if applicable,
along with accompanying materials will be available at www.huntsman.com/investors .

- 3 -

Table 1 – Results of Operations

Three months ended | Six months ended
June 30, | June 30,
In millions, except per share amounts | 2026 | 2025 | 2026 | 2025
Revenues | 1,663 | 1,458 | 3,083 | 2,868
Cost of goods sold | 1,418 | 1,276 | 2,655 | 2,485
Gross profit | 245 | 182 | 428 | 383
Operating expenses:
Selling, general and administrative | 183 | 160 | 346 | 326
Research and development | 28 | 33 | 57 | 65
Restructuring, impairment and plant closing costs | 9 | 124 | 15 | 125
Gain on sale of business, net | (22 | - | (22 | -
Gain on acquisition of assets, net | - | - | - | (5
Income associated with litigation matter, net | - | - | - | (33
Other operating expense (income), net | 10 | (15 | 11 | (17
Total operating expenses | 208 | 302 | 407 | 461
Operating income (loss) | 37 | (120 | 21 | (78
Interest expense, net | (23 | (21 | (44 | (40
Equity in income (loss) of investment in unconsolidated affiliates | 5 | (2 | 10 | (1
Other income, net | 7 | 4 | 10 | 7
Income (loss) from continuing operations before income taxes | 26 | (139 | (3 | (112
Income tax expense | (17 | (7 | (28 | (22
Income (loss) from continuing operations | 9 | (146 | (31 | (134
(Loss) income from discontinued operations, net of tax | (2 | 1 | (3 | -
Net income (loss) | 7 | (145 | (34 | (134
Net income attributable to noncontrolling interests | (13 | (13 | (25 | (29
Net loss attributable to Huntsman Corporation | (6 | (158 | (59 | (163
Adjusted EBITDA (1) | 120 | 74 | 193 | 146
Adjusted net income (loss) (1) | - | (34 | (35 | (53
Basic loss per share | (0.03 | (0.92 | (0.34 | (0.94
Diluted loss per share | (0.03 | (0.92 | (0.34 | (0.94
Adjusted diluted income (loss) per share (1) | - | (0.20 | (0.20 | (0.31
Common share information:
Basic weighted average shares | 173 | 173 | 173 | 172
Diluted weighted average shares | 173 | 173 | 173 | 172
Diluted shares for adjusted diluted income (loss) per share | 174 | 173 | 173 | 172

See end of press release for footnote explanations.

- 4 -

Table
2 -- Results of Operations by Segment

Three months ended | Six months ended
June 30, | Better / | June 30, | Better /
In millions | 2026 | 2025 | (worse) | 2026 | 2025 | (worse)
Segment revenues:
Polyurethanes | 1,079 | 932 | 16 | % | 2,002 | 1,844 | 9 | %
Performance Products | 283 | 270 | 5 | % | 511 | 527 | (3 | %)
Advanced Materials | 313 | 264 | 19 | % | 592 | 513 | 15 | %
Total reportable segments' revenues | 1,675 | 1,466 | 14 | % | 3,105 | 2,884 | 8 | %
Intersegment eliminations | (12 | (8 | N/M | (22 | (16 | N/M
Total revenues | 1,663 | 1,458 | 14 | % | 3,083 | 2,868 | 7 | %
Segment adjusted EBITDA (1) :
Polyurethanes | 66 | 31 | 113 | % | 105 | 73 | 44 | %
Performance Products | 37 | 32 | 16 | % | 63 | 62 | 2 | %
Advanced Materials | 64 | 45 | 42 | % | 109 | 81 | 35 | %

N/M = not meaningful

See end of press release for footnote explanations.

Table 3 -- Factors Impacting Sales Revenue

Three months ended
June 30, 2026 vs. 2025
Average selling price (a)
Local | Exchange | Sales
currency & mix | rate | volume (b) | Total
Polyurethanes | 10 | % | 2 | % | 4 | % | 16 | %
Performance Products | 1 | % | 1 | % | 3 | % | 5 | %
Advanced Materials | 8 | % | 3 | % | 8 | % | 19 | %
Combined segments | 8 | % | 2 | % | 4 | % | 14 | %

Six months ended
June 30, 2026 vs. 2025
Average selling price (a)
Local | Exchange | Sales
currency & mix | rate | volume (b) | Total
Polyurethanes | 2 | % | 3 | % | 4 | % | 9 | %
Performance Products | (2 | %) | 2 | % | (3 | %) | (3 | %)
Advanced Materials | 6 | % | 4 | % | 5 | % | 15 | %
Combined segments | 2 | % | 3 | % | 3 | % | 8 | %

(a) Excludes sales from tolling arrangements, by-products and raw materials.
(b) Excludes sales from by-products and raw materials.

- 5 -

Table 4 – Reconciliation
of U.S. GAAP to Non-GAAP Measures

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-18_item7_mdna.md)

_Extraction: no Overview/Results heading found; took the start of Item 7._

ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS

R eSULTS OF O PERATIONS

As discussed in "Note 4. Discontinued Operations—Sale of Textile Effects Business" to our consolidated financial statements, the results from continuing operations primarily exclude the results of our Textile Effects Business for all periods presented. For each of our Company and Huntsman International, the following tables set forth our consolidated results of operations for the years ended December 31, 2025, 2024 and 2023 (in millions, except per share amounts).

Huntsman Corporation

December 31, | Percent change
2025 | 2024 | 2023 | 2025 vs 2024 | 2024 vs 2023
Revenues | 5,683 | 6,036 | 6,111 | (6 | )% | (1 | )%
Cost of goods sold | 4,932 | 5,170 | 5,205 | (5 | )% | (1 | )%
Gross profit | 751 | 866 | 906 | (13 | )% | (4 | )%
Operating expenses:
Selling, general and administrative | 670 | 671 | 689 | — | (3 | )%
Research and development | 120 | 121 | 115 | (1 | )% | 5 | %
Restructuring, impairment and plant closing costs | 148 | 39 | 18 | 279 | % | 117 | %
Income associated with litigation matter, net | (33 | — | — | NM | NM
Gain on acquisition of assets, net | (5 | (51 | — | (90 | )% | NM
Prepaid asset write-off | — | 71 | — | (100 | )% | NM
Loss on dissolution of subsidiaries | — | 39 | — | (100 | )% | NM
Other operating (income) expense, net | (18 | 1 | — | NM | NM
Total operating expenses | 882 | 891 | 822 | (1 | )% | 8 | %
Operating (loss) income | (131 | (25 | 84 | 424 | % | NM
Interest expense, net | (79 | (79 | (65 | — | 22 | %
Equity in income of investment in unconsolidated affiliates | 4 | 44 | 83 | (91 | )% | (47 | )%
Other income (expense), net | 14 | 21 | (3 | (33 | )% | NM
(Loss) income from continuing operations before income taxes | (192 | (39 | 99 | 392 | % | NM
Income tax expense | (26 | (61 | (64 | (57 | )% | (5 | )%
(Loss) income from continuing operations | (218 | (100 | 35 | 118 | % | NM
(Loss) income from discontinued operations, net of tax | (9 | (27 | 118 | (67 | )% | NM
Net (loss) income | (227 | (127 | 153 | 79 | % | NM
Reconciliation of net (loss) income to adjusted EBITDA (1) :
Net income attributable to noncontrolling interests | (57 | (62 | (52 | (8 | )% | 19 | %
Interest expense, net from continuing operations | 79 | 79 | 65 | — | 22 | %
Income tax expense from continuing operations | 26 | 61 | 64 | (57 | )% | (5 | )%
Income tax (benefit) expense from discontinued operations | — | (11 | 17 | (100 | )% | NM
Depreciation and amortization of continuing operations | 287 | 289 | 278 | (1 | )% | 4 | %
Other adjustments:
Business acquisition and integration (gain) expenses and purchase accounting inventory adjustments, net | (4 | 21 | 4
EBITDA from discontinued operations (2) | 9 | 38 | (135
Fair value adjustments to Venator investment, net and other tax matter adjustments | — | (12 | 5
Certain legal and other settlements and related (income) expenses, net (3) | (30 | 13 | 6
Loss on sale of business/assets | 5 | 1 | —
Loss on dissolution of subsidiaries (4) | — | 39 | —
Certain nonrecurring information technology project implementation costs | — | — | 5
Amortization of pension and postretirement actuarial losses | 34 | 39 | 37
Restructuring, impairment and plant closing and transition costs (5) | 153 | 46 | 25
Adjusted EBITDA (1) | 275 | 414 | 472 | (34 | )% | (12 | )%
Net cash provided by operating activities from continuing operations | 298 | 285 | 251 | 5 | % | 14 | %
Net cash (used in) provided by investing activities from continuing operations | (132 | (126 | 309 | 5 | % | NM
Net cash used in financing activities | (76 | (326 | (620 | (77 | )% | (47 | )%
Capital expenditures from continuing operations | (173 | (184 | (230 | (6 | )% | (20 | )%
Amounts attributable to Huntsman Corporation:
Loss from continuing operations | (275 | (162 | (17
(Loss) income from discontinued operations, net of tax | (9 | (27 | 118
Net (loss) income | (284 | (189 | 101

Huntsman International

December 31, | Percent change
2025 | 2024 | 2023 | 2025 vs 2024 | 2024 vs 2023
Revenues | 5,683 | 6,036 | 6,111 | (6 | )% | (1 | )%
Cost of goods sold | 4,932 | 5,170 | 5,205 | (5 | )% | (1 | )%
Gross profit | 751 | 866 | 906 | (13 | )% | (4 | )%
Operating expenses:
Selling, general and administrative | 667 | 668 | 686 | — | (3 | )%
Research and development | 120 | 121 | 115 | (1 | )% | 5 | %
Restructuring, impairment and plant closing costs | 148 | 39 | 18 | 279 | % | 117 | %
Income associated with litigation matter, net | (33 | — | — | NM | NM
Gain on acquisition of assets, net | (5 | (51 | — | (90 | )% | NM
Prepaid asset write-off | — | 71 | — | (100 | )% | NM
Loss on dissolution of subsidiaries | — | 39 | — | (100 | )% | NM
Other operating (income) expense, net | (18 | 1 | — | NM | NM
Total operating expenses | 879 | 888 | 819 | (1 | )% | 8 | %
Operating (loss) income | (128 | (22 | 87 | 482 | % | NM
Interest expense, net | (79 | (79 | (65 | — | 22 | %
Equity in income of investment in unconsolidated affiliates | 4 | 44 | 83 | (91 | )% | (47 | )%
Other income (expense), net | 14 | 21 | (3 | (33 | )% | NM
(Loss) income from continuing operations before income taxes | (189 | (36 | 102 | 425 | % | NM
Income tax expense | (27 | (62 | (65 | (56 | )% | (5 | )%
(Loss) income from continuing operations | (216 | (98 | 37 | 120 | % | NM
(Loss) income from discontinued operations, net of tax | (9 | (27 | 118 | (67 | )% | NM
Net (loss) income | (225 | (125 | 155 | 80 | % | NM
Reconciliation of net (loss) income to adjusted EBITDA (1) :
Net income attributable to noncontrolling interests | (57 | (62 | (52 | (8 | )% | 19 | %
Interest expense, net from continuing operations | 79 | 79 | 65 | — | 22 | %
Income tax expense from continuing operations | 27 | 62 | 65 | (56 | )% | (5 | )%
Income tax (benefit) expense from discontinued operations | — | (11 | 17 | (100 | )% | NM
Depreciation and amortization of continuing operations | 287 | 289 | 278 | (1 | )% | 4 | %
Other adjustments:
Business acquisition and integration (gain) expenses and purchase accounting inventory adjustments, net | (4 | 21 | 4
EBITDA from discontinued operations (2) | 9 | 38 | (135
Fair value adjustments to Venator investment, net and other tax matter adjustments | — | (12 | 5
Certain legal and other settlements and related (income) expenses, net (3) | (30 | 13 | 6
Loss on sale of business/assets | 5 | 1 | —
Loss on dissolution of subsidiaries (4) | — | 39 | —
Certain nonrecurring information technology project implementation costs | — | — | 5
Amortization of pension and postretirement actuarial losses | 34 | 39 | 37
Restructuring, impairment and plant closing and transition costs (5) | 153 | 46 | 25
Adjusted EBITDA (1) | 278 | 417 | 475 | (33 | )% | (12 | )%
Net cash provided by operating activities from continuing operations | 299 | 285 | 253 | 5 | % | 13 | %
Net cash used in investing activities from continuing operations | (137 | (138 | (42 | — | 229 | %
Net cash used in financing activities | (72 | (314 | (271 | (77 | )% | 16 | %
Capital expenditures from continuing operations | (173 | (184 | (230 | (6 | )% | (20 | )%
Amounts attributable to Huntsman International:
Loss from continuing operations | (273 | (160 | (15
(Loss) income from discontinued operations, net of tax | (9 | (27 | 118
Net (loss) income | (282 | (187 | 103

Huntsman Corporation

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-18_item1_business.md)

ITEM 1. BUSINESS

O verview

We are a global manufacturer of diversified organic chemical products. We operate in three segments: Polyurethanes, Performance Products and Advanced Materials. Our products comprise many different chemicals and chemical formulations, which we market globally to a wide range of consumers that consist primarily of industrial and building product manufacturers. Our products are used in a broad range of applications, including those in the adhesives, aerospace, automotive, coatings and construction, construction products, durable and non-durable consumer products, electronics, insulation, power generation and refining. Many of our products offer effects such as premium insulation in homes and buildings and the lightweighting of airplanes and automobiles that help conserve energy. We are a leading global producer in many of our key product lines, including MDI, amines, maleic anhydride and epoxy-based polymer formulations. Our revenues for the years ended December 31, 2025, 2024 and 2023 were $5,683 million, $6,036 million and $6,111 million, respectively.

Our company, a Delaware corporation, was formed in 2004 to hold the Huntsman businesses, which were founded by Jon M. Huntsman. Mr. Huntsman founded the predecessor to our Company in 1970 as a small packaging materials company. Since then, we have transformed through a series of acquisitions and divestitures and now own a global portfolio of businesses with a primary focus on improving energy efficiency. On February 28, 2023, we completed the sale of our textile chemicals and dyes business ("Textile Effects Business") to Archroma, a portfolio company of SK Capital Partners ("Archroma"). For more information, see "Note 4. Discontinued Operations—Sale of Textile Effects Business" to our consolidated financial statements. We operate all of our businesses through Huntsman International, our wholly-owned subsidiary. Huntsman International is a Delaware limited liability company and was formed in 1999.

Our principal executive offices are located at 10003 Woodloch Forest Drive, The Woodlands, Texas 77380, and our telephone number at that location is (281) 719-6000.

O ur B u sines s S e gment s

(1) | For a reconciliation of total reportable segments' adjusted EBITDA to (loss) income from continuing operations before income taxes, see "Note 27. Operating Segment Information" to our consolidated financial statements. Percentage allocations in this chart do not give effect to Corporate and other unallocated items and eliminations.

The following table identifies the key product lines, principal end markets and applications, representative customers, raw materials and representative competitors of each of our business segments:

Product lines | End markets / applications | Representative customers | Raw materials | Representative competitors

Polyurethanes | MDI | Polyurethane chemicals are used to produce rigid and flexible foams, as well as coatings, adhesives, sealants and elastomers. Major end markets include: building insulation, construction products, automotive, including electric vehicles, and footwear. They are also used in cold chain, furniture and specialized engineering applications. | Benzene, chlorine and industrial gases
Polyols | Polyols are combined with MDI and other isocyanates to create a broad spectrum of polyurethane products, such as rigid and flexible foams and other non-foam applications. | Autoneum, Carpenter, GAF, Johns Manville, Amrize, Lear, Louisiana Pacific, Magna, Schmitz Cargobull, TopBuild and West Fraser | PO, polyester polyols and EO | BASF, Carlisle Construction Materials, Coim, Covestro, Dow, Lubrizol and Wanhua Chemical Group
TPU | TPU is a high-quality, fully-formulated thermal plastic that can be tailored with unique qualities. It can be used in injection molding and small components for automotive and footwear. It is also extruded into films, wires and cables for use in the coatings, adhesives, sealants and elastomers markets. | Isocyanate (such as MDI) and a polyol

Performance Products | Amines | Amines are a family of intermediate chemicals that are valued for their properties as a reactive agent, emulsifier, dispersant, detergent, solvent or corrosion inhibitor. Amines are used in polyurethane foam, fuel and lubricant additives, paints and coatings, composites, gas treatment, construction materials and semiconductor cleaning solutions. | Afton, Bayer, Chevron, DuPont, Evonik, Hipower, Infineum, Lubrizol, Quadra Chemicals and Univar | EO, PO, glycols, ethylene dichloride, caustic soda, ammonia, hydrogen, methylamines and acrylonitrile | BASF, Chenhua, Delamine, Dow, Evonik, Longhua, Nouryon, Tosoh and Zhengda
Maleic anhydride | Maleic anhydride is an intermediate chemical used primarily to produce unsaturated polyester resins (UPRs). UPRs are mainly used in the production of fiberglass reinforced resins for construction, automotive, marine and recreation products. Maleic anhydride is also used in components or additives for lubricants, copolymers, food acidulants and water and paper chemicals. | Afton, AOC, BASF, Chevron, Ineos, Infineum, Polynt-Reichhold, Primient, Reacciones Quimicas and Solenis | Normal butane | AOC, Bartek, Ineos and Lanxess

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-18_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-18_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-18_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-30_2-02-results.md, 10-K_2026-02-18_item7_mdna.md, 10-K_2026-02-18_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
