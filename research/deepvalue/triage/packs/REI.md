# Triage pack — REI · RING ENERGY, INC.

_Generated 2026-09-05 00:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** REI · **Name:** RING ENERGY, INC.
- **CIK:** 0001384195
- **SIC:** 1311 — Crude Petroleum & Natural Gas
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/REI

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** RING ENERGY, INC.
- **CIK:** 1,384,195 · **SIC:** 1311 (Crude Petroleum & Natural Gas) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LineOfCredit

**Valuation**

| metric | value |
|---|---|
| price | 1.50 |
| mktcap | $390.8M |
| ev | $749.7M |
| ev_ebit | n/a |
| fcf | $150.8M |
| fcf_yield | 38.6% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -2.4% |
| net_debt | $358.9M |
| net_debt_ebit | n/a |
| cash | $1.1M |
| ltd | $360.0M |
| equity | $753.4M |
| ltd_tag | LineOfCredit |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $307.2M |
| revenue_prior | $366.3M |
| rev_growth | -16.1% |
| rev_growth_note | share count +26.1% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$34.3M |
| net_income | -$34.7M |
| cfo | $150.8M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 26.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 260,539,607 |
| shares_py | 206,544,770 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 25.5% |
| r6m | -3.2% |
| off_52w_high | -24.2% |
| adv20 | $4.4M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.97 |
| r_ev_ebit | 0.00 |
| r_roic | 0.24 |
| r_rev_growth | 0.05 |
| r_buyback | 0.05 |
| score | 0.31 |

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
| rank | 398 |

**Screen rationale:** top-quartile FCF yield 38.6%; share count +26.1% yoy — growth may be acquisition/issuance-driven, not organic; 12-1 momentum 25.5%


## 3. Share count trend

- Shares outstanding: **260,539,607** (CY2026Q2I) vs **206,544,770** prior year (CY2025Q2I)
- Change: **26.1%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +26.1% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-05-07** — Item 5.02 (officer / director change or comp arrangement): On May 4, 2026, the Board of Directors (the "Board") of the Company appointed Sundip "Sonu" S. Johl as Principal Financial Officer of the Company in addition to his current positions as Executive Vice President, Chief Financial Officer and Treasurer of the...
- **2026-03-06** — Item 5.02 (officer / director change or comp arrangement): On March 5, 2026, Ring Energy, Inc. (the "Company") granted a restricted stock unit ("RSUs") award for 317,460 RSUs (the "RSU Inducement Award") and a performance stock unit ("PSUs") award for 476,190 PSUs (for which up to 952,380 shares may be earned) (the...

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 281,000 sh / $338,340 vs sells 0 sh / $0 -> net $338,340 (BUYING).
Distinct insiders buying (code P): 2. Largest buy: Johl Sundip Singh bought 231,000 sh @ $1.21 ($278,840) on 2026-06-15.

Form 4 filings parsed: 12; transaction rows: 20 (open-market buys 2, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 10 |
| P | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-08-06_2-02-results.md)

_Extraction: started at the first release heading, 'The Woodlands, TX – August 5, 2026 – Ring Energy, Inc. (NYSE American:'; skipped 11 forward-looking-statement block(s); 6 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (reiq22026earningsrelease.htm)

The Woodlands, TX – August 5, 2026 – Ring Energy, Inc. (NYSE American: REI) ("Ring" or the "Company") today reported operational and financial results for the second quarter of 2026, announced an expanded development program for second half of 2026, updated guidance for the remainder of 2026 and provided guidance for 2027.

Second Quarter 2026 Highlights

Strengthened Financial Position

• Reported net income of $64.8 million (included a $42.2 million unrealized mark-to-market gain on commodity derivative contracts), or $0.27 per diluted share, and Adjusted Net Income 1 of $24.0 million, or $0.10 per diluted share;

• Reduced borrowings under the Company's revolving credit facility by $66 million during the quarter and increased liquidity to approximately $226.1 million at June 30, 2026;

• Increased Adjusted EBITDA 1 42% to $54.5 million from $38.3 million in the first quarter; year-to-date Adjusted EBITDA totaled $92.8 million; and

• Generated net cash provided by operating activities of $40.8 million and remained cash flow positive for over 6 consecutive years.

Continued Operational and All-In Cash Cost 1 Improvements

• Produced 12,683 barrels of oil per day and 19,990 barrels of oil equivalent ("Boe") per day, both within guidance;

• Reported lease operating expense of $10.12 per Boe, near the low end of guidance and below first quarter levels; and

• Reduced Company all-in-cash costs by 5% in first half 2026 to $21.68 per Boe as compared to first half 2025.

Advanced Development and Infrastructure Initiatives

• Invested approximately $43.2 million in capital expenditures during the quarter, including three ~2-mile horizontal wells drilled, one saltwater disposal well ("SWD"), a frac pond, and other infrastructure projects; and

• Continued execution of multiple technical and operational initiatives aimed at improving capital efficiency, expanding development opportunities and enhancing long-term stockholder value.

Positioned for Improved Returns and Sustainable Growth

• Second half 2026 oil production guidance range of 13,000 to 13,950 Bopd, with the midpoint approximately 2% above prior guidance.

• Second half 2026 LOE per Boe guidance range of $10.00 to $10.60, with the midpoint approximately 2% below prior guidance.

• Initial 2027 guidance targets:

◦ Production growth approximately 10% over full-year 2026;

◦ LOE per Boe approximately 1% lower than full-year 2026; and

◦ Capital expenditures approximately 10% lower than full-year 2026.

Management Commentary

Mr. Paul D. McKinney, Chairman of the Board and Chief Executive Officer, commented, "The second quarter marked another period of efficient and effective execution for Ring Energy. We delivered production within guidance, reduced per-Boe operating costs, significantly increased Adjusted EBITDA, and generated positive Adjusted Free Cash Flow 1 for the 27th straight quarter. Additionally, we continued strengthening our balance sheet while positioning the Company for the next phase of its development strategy. The equity offering completed during the quarter gave us the balance sheet capacity to fund the acceleration of our development transition without losing focus on decreasing our leverage ratio. Rather than choosing between strengthening the balance sheet and investing in the highest-return phase of our development plan, the timing of this raise allowed us to do both. We expect our expanded drilling program to be funded primarily through operating cash flow going forward, with leverage continuing to trend toward our 1.25x target as this investment cycle completes. When considering these results and the expansion of our undeveloped drilling inventory due to our 2026 capital program, the Company is meaningfully stronger in almost every regard than it was at the beginning of the year."

Mr. McKinney concluded, "Over the past eighteen months, we have strengthened our balance sheet, improved liquidity and advanced a number of initiatives designed to enhance long-term value of our asset base. Looking ahead and supported by improving commodity prices, greater exposure to those prices through an improved hedge position and encouraging early drilling results, we are increasing our capital investment program for the remainder of 2026 that will allow for our transition to a more capital efficient development program of longer lateral wells and co-horizontal-development of our stacked-pay drilling opportunities. We strongly believe this transition will enhance economic returns, improve capital efficiency and increase the long-term value of our inventory. As a result, we expect increased production, reserves and free cash flow generation over time. We expect to fund this expanded program primarily through operating cash flow while maintaining Ring's commitment to financial discipline, free cash flow generation, balance sheet strength and per share return metrics. Also, as a part of our ongoing portfolio management, we continue to evaluate select non-core assets that do not fit our long-term development plans and any proceeds from such divestitures would be directed toward further debt reduction, consistent with our capital allocation priorities."

1 A non-GAAP financial measure; see the "Non-GAAP Financial Information" section in this release for more information including reconciliations to the most comparable GAAP measures.

Summary Results and Additional Key Items

Q2 2026 | Q1 2026 | Q2 2026 to Q1 2026 % Change | Q2 2025 | Q2 2026 to Q2 2025 % Change | YTD 2026 | YTD 2025 | YTD % Change
Average Daily Sales Volumes (Boe/d) | 19,990 | 19,351 | 3% | 21,295 | (6)% | 19,672 | 19,851 | (1)%
Crude Oil (Bo/d) | 12,683 | 12,276 | 3% | 14,511 | (13)% | 12,480 | 13,299 | (6)%
Net Sales (MBoe) | 1,819.1 | 1,741.6 | 4% | 1,937.9 | (6)% | 3,560.7 | 3,593.1 | (1)%
Realized Price - All Products ($/Boe) | $57.55 | $42.30 | 36% | $42.63 | 35% | $50.09 | $45.00 | 11%
Realized Price - Crude Oil ($/Bo) | $95.45 | $68.97 | 38% | $62.69 | 52% | $82.50 | $66.17 | 25%
Revenues ($MM) | $104.7 | $73.7 | 42% | $82.6 | 27% | $178.4 | $161.7 | 10%
Net Income (Loss) ($MM) | $64.8 | $(220.6) | 129% | $20.6 | 215% | $(155.8) | $29.7 | (625)%
Adjusted Net Income 1 ($MM) | $24.0 | $7.4 | 224% | $11.0 | 118% | $31.4 | $21.7 | 45%
Adjusted EBITDA 1 ($MM) | $54.5 | $38.3 | 42% | $51.5 | 6% | $92.8 | $97.9 | (5)%
Capital Expenditures ($MM) | $43.2 | $34.5 | 25% | $16.8 | 157% | $77.7 | $49.3 | 58%
Adjusted Free Cash Flow 1 ($MM) | $4.4 | $0.2 | NM (2) | $24.8 | (82)% | $4.6 | $30.6 | (85)%

(1) Adjusted Net Income, Adjusted EBITDA, and Adjusted Free Cash Flow are non-GAAP financial measures, which are described in more detail and reconciled to the most comparable GAAP measures, in the tables shown later in this release under "Non-GAAP Financial Information." In addition, see section titled "Condensed Operating Data" for additional details concerning costs and expenses presented below.

(2) Not meaningful.

Select Expenses and Other Items

Q2 2026 | Q1 2026 | Q2 2026 to Q1 2026 % Change | Q2 2025 | Q2 2026 to Q2 2025 % Change | YTD 2026 | YTD 2025 | YTD % Change
Lease operating expenses ("LOE") ($MM) | $18.4 | $18.1 | 2% | $20.2 | (9)% | $36.5 | $39.9 | (9)%
Lease operating expenses ($/BOE) | $10.12 | $10.41 | (3)% | $10.45 | (3)% | $10.26 | $11.11 | (8)%
Depreciation, depletion and amortization ($MM) | $20.1 | $21.4 | (6)% | $25.6 | (21)% | $41.5 | $48.2 | (14)%
Depreciation, depletion and amortization ($/BOE) | $11.06 | $12.29 | (10)% | $13.19 | (16)% | $11.66 | $13.41 | (13)%
General and administrative expenses ("G&A") ($MM) | $8.0 | $7.4 | 8% | $7.1 | 13% | $15.4 | $15.8 | (3)%
General and administrative expenses ($/BOE) | $4.37 | $4.27 | 2% | $3.68 | 19% | $4.32 | $4.39 | (2)%
G&A excluding share-based compensation ($MM) | $5.8 | $5.9 | (2)% | $5.8 | —% | $11.7 | $12.7 | (8)%
G&A excluding share-based compensation ($/BOE) | $3.19 | $3.40 | (6)% | $2.99 | 7% | $3.29 | $3.54 | (7)%
G&A excluding share-based compensation & transaction costs ($MM) | $5.8 | $5.9 | (2)% | $5.8 | —% | $11.7 | $12.7 | (8)%
G&A excluding share-based compensation & transaction costs ($/BOE) | $3.19 | $3.40 | (6)% | $2.99 | 7% | $3.29 | $3.54 | (7)%
Interest expense ($MM) | $8.4 | $8.6 | (2)% | $11.8 | (29)% | $17.0 | $21.3 | (20)%
Interest expense ($/BOE) | $4.61 | $4.94 | (7)% | $6.07 | (24)% | $4.77 | $5.92 | (19)%
Gain (loss) on derivative contracts ($MM) (1) | $23.7 | $(82.2) | 129% | $14.6 | 62% | $(58.5) | $13.7 | (527)%
Realized gain (loss) on derivative contracts ($MM) | $(18.5) | $(5.2) | (256)% | $0.6 | NM (2) | $(23.7) | $0.1 | NM (2)
Unrealized gain (loss) on derivative contracts ($MM) | $42.2 | $(77.0) | 155% | $14.0 | 201% | $(34.8) | $13.6 | (356)%

(1) A summary listing of the Company's outstanding derivative positions as of August 4, 2026 is included in the tables shown later in this release. As of August 4, 2026, for the remainder (July through December) of 2026, the Company has approximately 1.7 million barrels of oil (approximately 70% of oil sales guidance midpoint) hedged at an average upside protection price of $71.47 and approximately 2.4 billion cubic feet of natural gas (approximately 62% of natural gas sales guidance midpoint) hedged at an average downside protection price of $3.78.

(2) Not meaningful.

Balance Sheet and Liquidity

Total liquidity (defined as cash and cash equivalents plus borrowing base availability under the Company's credit facility) at June 30, 2026 was approximately $226.1 million, consisting of $225.0 million of availability under our revolving credit facility, which included a reduction of $35 thousand for letters of credit, and $1.1 million in cash and cash equivalents. On June 30, 2026, the Company had $360 million in borrowings outstanding on its credit facility that has a current borrowing base of $585 million. This reflects a reduction of $66 million from the balance of $426 million at March 31, 2026 . T he Company intends to resume debt reduction, dependent on market conditions, the timing and level of capital spending, and other considerations.

Drilling and Completion Activity

In 2 Q 2026 the Company continued execution of its development program across its core positions. In the Northwest Shelf the Company drilled and completed one 1.5-mile horizontal (98% working interest) and one 1-mile horizontal well (100% working interest) in Yoakum County. In the Central Basin Platform, the Company drilled and completed one 1.5-mile horizontal well (99% working interest) in Andrews County, and one 1.5-mile horizontal well (96% working interest) in Crane County. The latter of these two wells, while completed, was not put on pump until 3Q 2026 and did not contribute significant volumes in 2Q 2026. Also in Crane County, the Company drilled three 2-mile horizontal wells (each with working interest of 100%) and was in the process of drilling one SWD well. The three 2-mile horizontal wells represent the first laterals of this length drilled by the Company in an area that

has been historically developed with vertical wells. All four of these wells are expected to be completed during the third quarter of 2026.

The table below sets forth Ring's drilling and completion activities in the first half of 2026:

Quarter | Area | Wells Drilled | Wells Completed | Drilled Uncompleted ("DUC")
1Q 2026 | Northwest Shelf (Horizontal) | 5 | 5 | —
Central Basin Platform (Horizontal) (1) | — | 1 | —
Central Basin Platform (Vertical) | 1 | 1 | —
Total | 6 | 7 | —
2Q 2026 | Northwest Shelf (Horizontal) | 2 | 2 | —
Central Basin Platform (Horizontal) | 5 | 2 | 3
Total | 7 | 4 | 3

(1) The horizontal well completed in the Central Basin Platform in the first quarter of 2026 is the completion of a previously drilled but uncompleted ("DUC") well.

Remaining Quarters of 2026 and Full-Year 2027 Sales Volumes, Capital Investment and Operating Expense Guidance

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-04_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Overview

Ring Energy, Inc. (the "Company," "Ring," "we," "us," "our" and similar terms) is a growth oriented independent oil and natural gas exploration and production company based in The Woodlands, Texas engaged in oil and natural gas development, production, acquisition, and exploration activities currently focused in the Permian Basin of Texas. Our drilling operations target the oil and liquids rich producing formations in the Northwest Shelf and the Central Basin Platform, in the Permian Basin in Texas.

Business Description and Plan of Operation

The Company is focused on balancing the need to reduce long-term debt and further developing our oil and gas properties to maintain or grow our annual production. We intend to achieve both through proper allocation of cash flow generated by our operations and potentially through the sale of non-core assets. We intend to continue evaluating potential transactions to acquire strategic producing assets with attractive acreage positions that can provide competitive returns for our shareholders.

• Growing production and reserves by developing our oil-rich resource base through conventional and horizontal drilling . In an effort to maximize its value and resources potential, Ring intends to drill and develop its acreage base in both the Northwest Shelf and Central Basin Platform assets, allowing Ring to execute on its plan of operating within its generated cash flow.

• Reduction of long-term debt and deleveraging of asset. Ring intends to reduce its long-term debt primarily through the use of excess cash flow and potentially through the sale of non-core assets. The Company believes that with its attractive field level margins, it is positioned to maximize the value of its assets and deleverage its balance sheet. The Company also believes through potential accretive acquisitions and strategic asset dispositions, it can accelerate the strengthening of its balance sheet. During the three months ended December 31, 2025, the Company made net paydowns of $8 million on its revolving line of credit, resulting in the outstanding long-term debt balance of $420 million.

• Employ industry leading drilling and completion techniques . Ring's executive team intends to continue to utilize new and innovative technological advancements for completion optimization, comprehensive geological evaluation, and reservoir engineering analysis to generate value and to build future development opportunities. These technological advancements have led to a low-cost structure that helps maximize the returns generated by our drilling programs.

• Pursue strategic acquisitions with attractive upside potential. Ring has a history of acquiring leasehold positions that it believes to have additional resource potential that meet its targeted returns on invested capital and comparable to its existing inventory of drilling locations. We pursue an acquisition strategy designed to increase reserves at attractive finding costs and complement existing core properties. Management intends to continue to pursue strategic acquisitions and structure the potential transactions financially, so they improve our balance sheet metrics and are accretive to shareholders. Our executive team, with its extensive experience in the Permian Basin, has many relationships with operators and service providers in the region.

2025 Developments and Highlights

Lime Rock Acquisition

On March 31, 2025, the Company, as buyer, and Lime Rock Resources IV-A, L.P. ("LRRA"), and Lime Rock Resources IV-C, L.P. ("LRRC" and with LRRA, "Lime Rock"), as seller, consummated the transactions contemplated in that certain Purchase and Sale Agreement dated February 25, 2025, by and among the Company, LRRA and LRRC (the "Purchase Agreement") that was previously reported on Form 8-K filed on February 28, 2025 with the Securities and Exchange Commission ("SEC"). At the closing of the Purchase Agreement, among other things, the Company acquired (the "Lime Rock Acquisition") interests in oil and gas leases and related property of Lime Rock located in Andrews County, Texas, for an aggregate consideration consisting of: (i) approximately $69.3 million in cash, net of customary purchase price adjustments, paid at the closing of the Lime Rock Acquisition, (ii) $10.0 million in cash paid on December 31, 2025, and (iii) 6,452,879 shares of common stock (the "LRR Shares"). On March 31, 2025, in connection with the closing of the Lime Rock Acquisition, the Company and Lime Rock entered into a customary registration rights agreement relating to the LRR Shares. On May 2, 2025, a registration statement on Form S-3 with respect to the resale of the LRR Shares was declared effective by the SEC.

Credit Agreement

On June 18, 2025, the Company as borrower, Bank of America, N. A. as the Administrative Agent and Issuing Bank ("Bank of America"), and the lenders party thereto (the "Lenders") entered into the Third Amended and Restated Credit Agreement (the "Credit Agreement") which amended and restated that certain Second Amended and Restated Credit Agreement dated as of August 31, 2022, by and among the Company, Truist Bank, as administrative agent, and the lenders party thereto, as amended by that certain First Amendment to Second Amended and Restated Credit Agreement, dated as of February 12, 2024 (the "Existing Credit Agreement"). All of the obligations under the Credit Agreement, and the guarantees of those obligations, are secured by substantially all of the Company's assets. Among other things, the Credit Agreement changed the administrative agent from Truist Bank to Bank of America; reduced the borrowing base and aggregate elected commitment from $600 million to $585 million; extended the maturity date of the Credit Agreement from August 31, 2026 to June 18, 2029; reduced the applicable margin pricing grid by 25 basis points; and made certain administrative changes to the Existing Credit Agreement.

Drilling and Completion

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

For the years ended December 31, | 2025 | 2024 | 2023
Net production:
Oil (Bbls) | 4,841,164 | 4,861,628 | 4,579,942
Natural gas (Mcf) | 6,980,958 | 6,423,674 | 6,339,158
Natural gas liquids (Bbls) | 1,387,818 | 1,258,814 | 976,852
Net sales:
Oil | 307,553,614 | 363,971,394 | 349,044,863
Natural gas | (9,297,614) | (9,265,335) | 334,175
Natural gas liquids | 8,922,072 | 11,621,355 | 11,676,963
Average sales price:
Oil (per Bbl) | 63.53 | 74.87 | 76.21
Natural gas (per Mcf) | (1.33) | (1.44) | 0.05
Natural gas liquids (Bbl) | 6.43 | 9.23 | 11.95
Production costs and expenses:
Lease operating expenses | 79,353,806 | 78,310,949 | 70,158,227
Gathering, transportation and processing costs | 585,087 | 506,333 | 457,573
Ad valorem taxes | 7,906,586 | 8,069,064 | 6,757,841
Oil and natural gas production taxes | 14,312,232 | 16,116,565 | 18,135,336
Other costs and operating expenses:
Depreciation, depletion and amortization | 96,414,150 | 98,702,843 | 88,610,291
Ceiling test impairment | 108,825,446 | — | —
Asset retirement obligation accretion | 1,490,255 | 1,380,298 | 1,425,686
Operating lease expense | 700,362 | 700,362 | 541,801
General and administrative expense ("G&A") | 31,928,576 | 29,640,300 | 29,188,755
Share-based compensation | 6,135,957 | 5,506,017 | 8,833,425
G&A excluding share-based compensation | 25,792,619 | 24,134,283 | 20,355,330
Other income (expense):
Interest income | 290,879 | 491,946 | 257,155
Interest (expense) | (40,430,929) | (43,311,810) | (43,926,732)
Gain (loss) on derivative contracts | 31,658,839 | (2,365,917) | 2,767,162
Gain (loss) on disposal of assets | 446,400 | 89,693 | (87,128)
Other income | 189,294 | 106,656 | 198,935
Benefit from (Provision for) Income Taxes | 7,452,746 | (20,440,954) | (125,242)

Year Ended December 31, 2025 Compared to Year Ended December 31, 2024

Oil sales . Oil sales decreased approximately $56.4 million to $307.6 million in 2025 from $364.0 million in 2024. This was due to a price variance of approximately $(54.9) million from a decrease in the average realized per barrel oil price to $63.53 in 2025 from $74.87 in 2024. Also impacting the oil sales was a volume variance of approximately $(1.5) million from a decrease in sales volumes to 4,841,164 barrels of oil in 2025 from 4,861,628 barrels of oil in 2024,

primarily driven by natural asset decline, offset by production from wells within the assets acquired with the Lime Rock Acquisition (closed in March 2025) and organic growth from workovers, new drills, and other capital expenditures.

Natural gas sales. Natural gas sales remained essentially constant, with approximately $(9.3) million in 2025 and $(9.3) million in 2024. The average realized per Mcf gas price increased to $(1.33) in 2025 from $(1.44) in 2024. The positive change in price was due to an increase in the average gross realized price that was higher than the increase in the average fees. In 2025, the average gross realized price for natural gas was $0.75 per Mcf, and the average fees per Mcf were $(2.08), bringing the net average price to $(1.33) per Mcf. In 2024, the average gross realized price for natural gas was $0.29 per Mcf, and the average fees per Mcf were $(1.73), bringing the net average price to (1.44) per Mcf. The natural gas sales volume increased to 6,980,958 Mcf in 2025 from 6,423,674 Mcf in 2024.

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-04_item1_business.md)

Item 1: Business

General

Ring Energy, Inc., a Nevada corporation ("Ring," "Ring Energy," the "Company," "we," "us," "our," or similar terms), is a growth oriented independent oil and natural gas exploration and production company based in The Woodlands, Texas engaged in oil and natural gas development, production, acquisition, and exploration activities currently focused in the Permian Basin of Texas. Our drilling operations target the oil and liquids rich producing formations in the Northwest Shelf and the Central Basin Platform, in the Permian Basin in Texas.

As of December 31, 2025, our leasehold acreage positions totaled 111,714 gross (96,234 net) acres and we held interests in 919 gross (758 net) producing wells. Proved reserves as of December 31, 2025 (based upon the report of our independent petroleum engineer of that date) were approximately 153.3 million Boe, of which we are the operator of approximately 99%. All of our properties are located in the Permian Basin and our proved reserves are oil-weighted, with approximately 59% consisting of oil, 19% consisting of natural gas, and 22% consisting of NGLs. Approximately 68% of the reserves are classified as PD and 32% are classified as PUD. Within the PD reserve category, 238 recompletion and re-activation opportunities are classified as PDNP and within the PUD reserve category, we have a total of 247 proved locations (38% horizontal and 62% vertical) based on the reserve report as of December 31, 2025. We believe our core leasehold in the Northwest Shelf and Central Basin Platform contain additional potential drilling locations.

2025 Highlights and Major Developments

• Closed the Lime Rock Acquisition on March 31, 2025.

• Achieved record full year production of 20,253 Boepd (65% oil), a year-over-year increase in total Boe of 3%.

• Lowered lifting costs to $10.73 per Boe, or 1% year over year including 9 months of the LRR acquisition assets.

• Responded to lower commodity price environment by pulling back on capital expenditures, executing a phased drilling program in 2025 that included drilling 18 gross, 17 net operated wells consisting of 12 horizontal and six vertical wells (gross).

• Total proved reserves were 153.3 MMBoe at year-end 2025, which increased 19.1 MMBoe, or 14% from year-end 2024. Total proved developed reserves were 103.8 MMBoe at year-end 2025, which increased 11.2 MMBoe, or 12% from year-end 2024.

• Maintained our revolving credit facility borrowing base of $585 million.

Our Mission

Ring's mission is to deliver competitive and sustainable returns to its shareholders by developing, acquiring, exploring for, and commercializing oil and natural gas resources that are vital to the world's health and welfare.

Our Key Principles

Successfully achieving Ring's mission requires a firm commitment to operating safely in a socially responsible and environmentally friendly manner. Key principles supporting Ring's strategic vision are to:

• Ensure health, safety, and environmental excellence with a strong commitment to Ring's employees and the communities in which we work and operate;

• Continue our focus on generating adjusted free cash flow to improve and build a sustainable financial foundation;

• Pursue rigorous capital discipline focused on Ring's highest returning opportunities;

• Improve margins and drive value by targeting additional operating cost reductions and capital efficiencies; and

• Strengthen our balance sheet by paying down debt, divesting of non-core assets and becoming a peer leader in Debt/EBITDA metrics.

Our Business Strategy

Our business strategy is guided by the above key principles and implemented by pursuing the following five strategic objectives, which are foundational aspects of our culture and success.

Attract and retain highly qualified people – Achieving our mission is only possible through our employees. It is critical to have compensation, development, and human resource programs that attract, retain, and motivate the people we need to succeed.

Pursue operational excellence with a sense of urgency – We seek to deliver low cost, consistent, timely, and efficient execution of our drilling campaigns, work programs, and operations. We execute our operations in a safe and environmentally responsible manner, focus on reducing our emissions, applying advanced technologies, and continuously seeking ways to reduce our operating cash costs on a per barrel basis.

Invest in high-margin, high rate-of-return projects – We prioritize our work programs and allocate capital to the highest return opportunities in our inventory on an ongoing basis. This objective is key to profitably growing our production and reserve levels and generating the excess cash from operations.

Focus on generating adjusted free cash flow and strengthening our balance sheet – We seek to continuously reduce long-term debt using excess cash from operations and potentially through the sale of non-core assets. Continuing to generate adjusted free cash flow through a disciplined capital allocation program and reducing our operating and corporate costs are key components of this objective. Our capital program is funded by operational cash flow and we seek to balance our production and reserve growth with paying down debt. We believe that remaining focused and disciplined in this regard will lead to meaningful returns for our shareholders and provide additional financial flexibility to manage potential future swings in business cycles. Our commodity hedges are designed to help ensure the necessary cash flow to adhere to these plans while retaining the flexibility to participate in prevailing commodity markets.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-04_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-04_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-04_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-08-06_2-02-results.md, 10-K_2026-03-04_item7_mdna.md, 10-K_2026-03-04_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
