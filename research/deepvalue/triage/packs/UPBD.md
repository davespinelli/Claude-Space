# Triage pack — UPBD · UPBOUND GROUP, INC.

_Generated 2026-09-04 12:44 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** UPBD · **Name:** UPBOUND GROUP, INC.
- **CIK:** 0000933036
- **SIC:** 7359 — Services-Equipment Rental & Leasing, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /Users/davidspinelli/Documents/Claude Space/research/deepvalue/filings/UPBD

## 2. Screen row (all metrics)

_Source: candidates.csv_

- **Name:** UPBOUND GROUP, INC.
- **CIK:** 933,036 · **SIC:** 7359 (Services-Equipment Rental & Leasing, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 18.67 |
| mktcap | $1.1B |
| ev | $983.1M |
| ev_ebit | 4.4x |
| fcf | $238.7M |
| fcf_yield | 21.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 28.1% |
| net_debt | -$105.3M |
| net_debt_ebit | -0.5x |
| cash | $105.3M |
| ltd | $0.00 |
| equity | $733.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $4.7B |
| revenue_prior | $4.3B |
| rev_growth | 8.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $223.3M |
| net_income | $73.0M |
| cfo | $305.6M |
| capex | $66.9M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 58,299,405 |
| shares_py | 57,895,609 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -12.3% |
| r6m | -5.5% |
| off_52w_high | -26.0% |
| adv20 | $14.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.92 |
| r_ev_ebit | 0.96 |
| r_roic | 0.93 |
| r_rev_growth | 0.60 |
| r_buyback | 0.43 |
| score | 0.77 |

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

**Screen rationale:** top-quartile FCF yield 21.9%; cheap at 4.4x EV/EBIT; high ROIC 28.1%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **58,299,405** (CY2026Q2I) vs **57,895,609** prior year (CY2025Q2I)
- Change: **0.7%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

- Last 18.67 (as of 2026-09-03) · 52w range 16.10 - 27.35 · -31.7% vs 52w high · 16.0% above 52w low

_Source: yfinance, live._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-03** — Item 5.02 (Departure of Directors): or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.
- **2026-05-19** — Item 5.02 (Departure of Directors or Certain Officers; Election): of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 9,077 sh / $178,997 vs sells 16,000 sh / $339,880 -> net $-160,883 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: BROWN JEFFREY J bought 1,841 sh @ $20.09 ($36,986) on 2026-07-07.

Form 4 filings parsed: 68; transaction rows: 94 (open-market buys 8, sales 2).

| code | rows |
|---|---|
| A | 63 |
| F | 21 |
| P | 8 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-30_2-02-results.md)

_Extraction: started at the first release heading, 'Upbound Group, Inc. Reports Second Quarter 2026 Results'; skipped 11 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (upbd-ex99_1.htm)

Upbound Group, Inc. Reports Second Quarter 2026 Results

PLANO, Texas--(BUSINESS WIRE)—July 30, 2026-- Upbound Group, Inc. (the "Company" or "Upbound") (NASDAQ:UPBD) today announced results for the quarter ended June 30, 2026. The earnings release, financial tables and related materials can be found on the Company's investor relations website at https://investor.upbound.com .

Today at 9 a.m. ET, Fahmi Karam, Chief Executive Officer, and Hal Khouri, Chief Financial Officer, will host a conference call to review the Company's financial results. Interested parties can access a live webcast of the conference call via this link ( Webcast Link ) or through the Company's investor relations website.

Second Quarter 2026 Highlights 1

•
Consolidated Results All Within Guided Ranges: Consolidated revenue of approximately $1.2 billion.

•
Brigit Continues Strong Momentum: Brigit revenue increased 37% year-over-year to $71 million, supported by approximately 30% growth in paying subscribers² to 1.7 million and a 6.3% increase in ARPU³ to $14.30.

•
Acima Delivers Improved Portfolio Quality: Acima generated $604 million of revenue, down approximately 2.5% year-over-year, but saw lease charge-off rate⁴ improve 50 basis points year-over-year to 8.8% and EBITDA margin expanded 117 basis points to 16.2%.

•
Rent-A-Center Achieves Third Consecutive Quarter of Same-Store Sales Growth: Same store sales⁵ increased approximately 160 basis points year-over-year, while achieving $466 million in revenue.

•
Robust Cash Flow Generation: Net cash provided by operating activities of approximately $123 million, while increasing free cash flow to $84 million.

•
2026 Outlook: Full-year consolidated revenue range narrowed to $4.70–$4.85 billion. Adjusted EBITDA⁶ range of $500–$535 million and non-GAAP diluted EPS⁶ range of $4.00–$4.35 reaffirmed. For the third quarter of 2026, the Company expects

consolidated revenue of $1.05–$1.15 billion, Adjusted EBITDA⁶ of $105–$115 million, and non-GAAP diluted EPS⁶ of $0.85–$0.95.

About Upbound Group, Inc.

Upbound Group, Inc. (NASDAQ: UPBD), is a technology and data-driven leader in accessible and inclusive financial solutions that address the evolving needs and aspirations of underserved consumers. The Company's customer-facing operating units include industry-leading brands such as Acima®, Brigit™, and Rent-A-Center® that facilitate consumer transactions across a wide range of store-based and digital channels in the United States, Mexico and Puerto Rico. Upbound Group, Inc. is headquartered in Plano, Texas. For additional information about the Company, please visit our website Upbound.com.

(1)
The selected highlights referenced herein do not provide a complete review of the Company's results for the quarter or updated guidance and outlook. Please refer to the Company's full earnings release and related materials, as noted in this release, for additional information.

(2)
Brigit Paying Subscribers: Represents Brigit customers who have an active Plus or Premium account, not delinquent (not 45 days past due) on a cash advance, and made at least 1 of the last 2 subscription payments.

(3)
ARPU: Average monthly revenue per Brigit Paying Subscriber, where Brigit Paying Subscriber is defined in footnote 2 above.

(4)
Lease Charge-Offs: Represents charge-offs of the net book value of unrecoverable on-rent merchandise with lease-to-own customers who are past due. This is typically expressed as a percentage of revenues for the applicable period. For the Rent-A-Center segment, LCOs exclude Get It Now, Home Choice, and Franchisee-owned Rent-A-Center locations. For the Acima segment, LCO's exclude fraudulent lease-to-own contract losses.

(5)
Same Store Sales (SSS): Same store sales generally represents revenue earned in Company-owned Rent-A-Center stores that were operated by us for 13 months or more and are reported on a constant currency basis as a percentage of total revenue earned in stores of the segment during the indicated period. The Company excludes from the same store sales base any store that receives a certain level of customer accounts from closed stores or acquisitions. The receiving store will be eligible for inclusion in the same store sales base in the 30th full month following account transfer.

(6)
See "Non-GAAP Financial Measures" below for the definitions and other information regarding our non-GAAP financial measures included in this release.

972-801-1103

## EX-99.2 - EX-99.2 (upbd-ex99_2.htm)

EX-99.2
upbd-ex99_2.htm
EX-99.2

Upbound Group, Inc. Earnings Release July 30, 2026 Second Quarter 2026 Results & Key Metrics $1,163M $22M $127M $0.37 $1.07 $0.39 Total Revenue Adjusted EBITDA1 GAAP Diluted EPS Non-GAAP Quarterly Dividend Per Share Net Earnings Diluted EPS1 Brigit Delivers over 35% Topline Growth, Acima LCO Improves Below 9%, Rent-A-Center Achieves Third Consecutive Quarter of Positive Same-Store Sales Affirming full year EBITDA and EPS Guidance. Second Quarter Results Within All Guided Ranges Second Quarter Consolidated Results CEO Commentary • Consolidated revenue of $1,163.4 million increased $5.9 million, or 0.5%, year-over-year. "The second quarter reflected continued solid execution for Upbound. We • GAAP operating profit of $54.3 million and non-GAAP operating profit1 of $108.7 million, compared to $50.7 million of GAAP operating profit and $116.2 million of non-GAAP operating profit in the prior year period. Second quarter 2026 GAAP operating profit margin was 4.7%, compared to 4.4% in the prior year period. delivered results within all of our guided ranges, generated robust cash flow, and made meaningful progress strengthening our balance sheet all while advancing our long-term strategic priorities," said CEO Fahmi Karam. • Net earnings on a GAAP basis of $21.6 million, compared to $15.5 million in the prior year period, a $6.1 million increase. Net profit margin of 1.9% increased 60 basis points year-over-year. "Our three complementary brands give us multiple avenues for growth and allow us to deepen customer relationships across products. Despite a tough operating environment, we executed well across the business including Rent-A-Center launching Amazon package pickups and returns at 1,500 stores nationally, Brigit executing a partnership agreement with Experian, and Acima expanding Adjusted EBITDA margin to over 16 percent." • Adjusted EBITDA1 decreased 4.6% year-over-year to $127.0 million. • Adjusted EBITDA margin1 of 10.9% decreased 60 basis points compared to the prior year period. • GAAP diluted earnings per share was $0.37, compared to GAAP diluted earnings per share of $0.26 in the prior year period. • Non-GAAP diluted earnings per share1, which excludes the impact of special items described at the end of this release, was $1.07 for the second quarter of 2026, compared to $1.12 in the prior year period. "We're energized by the opportunities ahead. By reinforcing underwriting discipline, strategically investing in AI, shared data platforms, and a more connected, personalized customer experience, we're building a stronger, more efficient platform positioned to sustain profitability and create long-term value for our shareholders," concluded Mr. Karam. • Improvement in lease-to-own charge-off performance, with Acima LCO rate decreasing 50 basis points year-over-year while Rent-A- Center LCO rate increased 30 basis points year-over-year. • Quarterly dividend per share of $0.39, or $1.56 annualized. (1)Non-GAAP financial measure. Refer to definitions and reconciliations elsewhere in this release.

Second Quarter Segment Highlights • Paying subscribers increased 399k, an increase of 30.2%, y/y and 10.3% compared to the first quarter. Total Revenue Paying Subscribers $71.1M +37.1% y/y 1.72M +30.2% y/y • Average monthly revenue per user (ARPU) increased 6.3% y/y, driven by increased shift towards Brigit's Premium subscription tier, deeper engagement with marketplace offers, and higher expedited transfer revenue. Net Advance Loss Rate ARPU • Net advance loss rate increased 100 bps y/y and increased 10 bps sequentially. 3.6% +100 bps y/y $14.30 +6.3% y/y • Net earnings of $7.5M with a net profit margin of 10.6%, and Adjusted EBITDA1 of $11.8M with an Adjusted EBITDA margin1 of 16.6%. • Revenue of $603.5M decreased approximately 2.5% y/y. Total Revenue Net Earnings • GMV decreased approximately 10.7% y/y in the second quarter. $603.5M $73.4M -2.5% y/y -10.4% y/y • Lease charge-off rate decreased 50 bps y/y and flat compared to the first quarter. LCO Rate Adjusted EBITDA1 8.8% -50 bps y/y $98.0M +5.1% y/y • Net earnings margin was 12.2%, a decrease of 100 bps from the prior year period, and Adjusted EBITDA margin1 was 16.2%, an increase of 117 bps y/y. • Company-owned same store sales increased 1.6% y/y, while consolidated segment revenue of $466.4M decreased approximately 0.2% y/y. Total Revenue Net Earnings $466.4M $54.7M -0.2% y/y -13.2% y/y • Lease charge-offs for company-owned Rent-A-Center stores were 5.0%, increasing 30 bps y/y. • Net earnings of $54.7M and Adjusted EBITDA1 of $63.2M decreased 13.2% and 7.6% y/y, respectively. LCO Rate 5.0% Adjusted EBITDA1 $63.2M -7.6% y/y +30 bps y/y Note: Definitions of certain key performance metrics are available on page five of this release. (1) Non-GAAP financial measure. Refer to definitions and reconciliations elsewhere in this release.

Full Year and Q3 2026 Guidance CFO Commentary "Second-quarter results came in within our guided ranges across revenue, EBITDA, and EPS, even as top-line growth ran below plan on softer consumer demand," said CFO Hal Khouri. The Company reaffirms EBITDA & EPS FY 2026 guidance, while tightening revenue guidance, and providing guidance for Q3 2026 "At the segment level, Acima continued to benefit from prior underwriting actions, with lease charge-offs Table 1 Consolidated Guidance1,2 Full Year 2026 Third Quarter 2026 improving year-over-year to Revenues ($B) $4.70 - $4.85 $1.05 - $1.15 approximately 8.8 percent and EBITDA margins expanding. Brigit sustained strong double-digit growth in revenue and paying users, while Rent-A-Center achieved its third consecutive quarter of positive same-store sales." Adj. EBITDA Excluding SBC ($M)3 Non-GAAP Diluted Earnings Per Share3 $500 - $535 $105 - $115 $4.00 - $4.35 $0.85 - $0.95 "Cash generation remained strong in the quarter, with free cash flow well above both plan and the prior year, supporting continued progress on debt reduction and balance-sheet strength. Liquidity remained solid at approximately $487 million at quarter end, and net leverage continued to trend lower sequentially, towards our goal of 2.0x net leverage." 1. Consolidated includes Acima, Brigit, Rent-A-Center, Mexico, and Corporate Segments. 2. Due to the inherent uncertainty related to the special items identified in the tables below, management does not believe it is able to provide a meaningful forecast of the comparable GAAP measures or reconciliation to any forecasted GAAP measure without unreasonable effort. The actual amount of these items during 2026 may have a significant impact on our future GAAP results. 3. Non-GAAP financial measure. See descriptions below in this release. "Our capital allocation priorities are unchanged as we move through the second half of the year: invest in the business, strengthen the balance sheet, and return capital to shareholders while maintaining flexibility to support long-term value creation." concluded Mr. Khouri Conference Call and Webcast Information Upbound Group, Inc. will host a conference call to discuss second quarter 2026 results, guidance and other operational matters on the morning of Thursday, July 30, 2026, at 9:00 a.m. ET. For a live webcast of the call, visit https://investor.upbound.com. Certain financial and other statistical information that will be discussed during the conference call will also be provided on the same website.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-02-23_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Overview

The following briefly summarizes certain of our financial information for the year ended December 31, 2025 as compared to the year ended December 31, 2024.

During the year ended December 31, 2025, consolidated revenues and gross profit increased by approximately $374.5 million and $191.3 million, respectively, primarily due to the addition of Brigit segment revenues and an increase in the Acima segment revenues, partially offset by a decrease in Rent-A-Center segment revenues described below. Operating profit decreased by approximately $68.3 million, primarily due to increases in non-labor operating expenses, other gains and charges and general and administrative expenses of $138.3 million, $107.6 million and $19.5 million, respectively, partially offset by the increase in gross profit noted above and a decrease in operating labor expenses of $6.9 million.

The Acima segment revenues increased approximately $251.0 million for the year ended December 31, 2025, due to increases in rentals and fees revenues and merchandise sales of $192.5 million and $59.0 million, respectively, primarily resulting from higher GMV of 8.6%. Growth in GMV was primarily due to an increase in third-party retailer locations and productivity, which resulted in more leases per retailer, and expanded direct-to-consumer offerings. Operating profit increased approximately $39.4 million for the year ended December 31, 2025, primarily due to an increase in gross profit of $60.3 million and decreases in operating labor costs and other gains and charges of $4.4 million and $1.7 million, respectively, partially offset by an increase in non-labor operating expenses of $26.4 million. See "Segment Performance" below for further discussion of Acima segment operating results for the year ended December 31, 2025.

Revenues in our Rent-A-Center segment decreased approximately $83.2 million for the year ended December 31, 2025, due to decreases in same store sales of 2.2% and lower corporate-owned store count as a result of prior year store closures, resulting in decreases in rentals and fees revenues and merchandise sales of $79.9 million and $3.5 million, respectively. Operating profit decreased approximately $47.6 million for the year ended December 31, 2025, primarily due to a decrease in gross profit of approximately $51.1 million driven by lower revenues, in addition to higher general and administrative expenses and other gains and charges of approximately $9.1 million and $6.2 million, respectively, partially offset by decreases in non-labor operating expenses and operating labor expense of approximately $13.2 million and $6.4 million, respectively. See " Segment Performance " below for further discussion of Rent-A-Center segment operating results for the year ended December 31, 2025.

The Brigit segment had revenues and operating profit of $206.0 million and $30.7 million, respectively, during the period beginning on the Closing Date and ending on December 31, 2025. See " Segment Performance " below for further discussion of Brigit segment operating results for the year ended December 31, 2025.

The Mexico segment revenues and gross profit increased by 0.8% and 0.2% for the year ended December 31, 2025, respectively, primarily due to increases in rentals and fees revenue, partially offset by negative impacts of exchange rate fluctuations. Operating profit increased 13.4%, primarily due to an increase in gross profit and a decrease in general and administrative expenses, partially offset by negative impacts of exchange rate fluctuations. See "Segment Performance" below for further discussion of Mexico segment operating results for the year ended December 31, 2025.

Cash flow from operations was $305.6 million for the year ended December 31, 2025. As of December 31, 2025, we held $120.5 million of cash and cash equivalents and had outstanding indebtedness of $1.6 billion.

The following table is a reference for the discussion that follows.
Year Ended December 31, | 2025-2024 Change
(dollar amounts in thousands) | 2025 | 2024 | %
Revenues
Rentals and fees | 3,627,019 | 3,513,658 | 113,361 | 3.2 | %
Merchandise sales | 829,268 | 773,744 | 55,524 | 7.2 | %
Subscription and fees | 206,024 | — | 206,024 | nm
Other | 32,750 | 33,162 | (412) | (1.2) | %
Total revenues | 4,695,061 | 4,320,564 | 374,497 | 8.7 | %
Cost of revenues
Cost of rentals and fees | 1,441,758 | 1,355,539 | 86,219 | 6.4 | %
Cost of merchandise sold | 957,621 | 884,674 | 72,947 | 8.2 | %
Cost of subscription and fees | 23,973 | — | 23,973 | nm
Total cost of revenues | 2,423,352 | 2,240,213 | 183,139 | 8.2 | %
Gross profit | 2,271,709 | 2,080,351 | 191,358 | 9.2 | %
Operating expenses
Operating labor | 602,301 | 609,169 | (6,868) | (1.1) | %
Non-labor operating expenses | 949,918 | 811,635 | 138,283 | 17.0 | %
General and administrative expenses | 231,963 | 212,450 | 19,513 | 9.2 | %
Depreciation and amortization | 51,959 | 50,886 | 1,073 | 2.1 | %
Other gains and charges | 212,221 | 104,580 | 107,641 | 102.9 | %
Total operating expenses | 2,048,362 | 1,788,720 | 259,642 | 14.5 | %
Operating profit | 223,347 | 291,631 | (68,284) | (23.4) | %
Debt refinancing charges | 4,894 | 6,604 | (1,710) | (25.9) | %
Interest, net | 110,362 | 107,486 | 2,876 | 2.7 | %
Earnings before income taxes | 108,091 | 177,541 | (69,450) | (39.1) | %
Income tax expense | 34,849 | 54,063 | (19,214) | (35.5) | %
Net earnings | 73,242 | 123,478 | (50,236) | (40.7) | %

nm - percent change is not meaningful for comparison

Comparison of the Years Ended December 31, 2025 and 2024

Revenue. Total revenue increased by $374.5 million, or 8.7%, to $4,695.1 million for the year ended December 31, 2025, from $4,320.6 million for 2024, primarily due to an increase of approximately $251.0 million in the Acima segment and the addition of the Brigit segment with $206.0 million in revenue, partially offset by a decrease of approximately $83.2 million in the Rent-A-Center segment, as discussed further in the "Segment Performance" section below.

Cost of Rentals and Fees. Cost of rentals and fees consists primarily of depreciation of rental merchandise. Cost of rentals and fees for the year ended December 31, 2025 increased by $86.3 million, or 6.4%, to $1,441.8 million, as compared to $1,355.5 million in 2024. The increase was primarily attributable to an increase of approximately $116.5 million in the Acima segment driven by an increase in rentals and fees revenues, partially offset by a decrease of approximately $30.8 million in the Rent-A-Center segment resulting from a decrease in rentals and fees revenue. Cost of rentals and fees expressed as a percentage of rentals and fees revenue increased to 39.8% for the year ended December 31, 2025, as compared to 38.6% in 2024, primarily due to the continued growth of the Acima segment as a percent of total rentals and fees revenue.

Cost of Merchandise Sold. Cost of merchandise sold represents the net book value of rental merchandise at time of sale. Cost of merchandise sold increased by $72.9 million, or 8.2%, to $957.6 million for the year ended December 31, 2025, from $884.7 million in 2024, primarily attributable to an increase of $74.3 million in the Acima segment primarily driven by higher merchandise sales. The gross margin percent of merchandise sales decreased to (15.5)% for the year ended December 31, 2025, from (14.3)% in 2024 primarily due to the conversion of Acceptance Now locations to the Acima Holdings Lease Management platform.

Gross Profit. Gross profit increased by $191.3 million, or 9.2%, to $2,271.7 million for the year ended December 31, 2025, from $2,080.4 million in 2024, primarily due to the addition of the Brigit segment with $182.1 million in gross profit and an increase of $60.3 million in the Acima segment, partially offset by a decrease of approximately $51.1 million in the Rent-A-Center segment, as discussed further in the "Segment Performance" section below. Gross profit as a percentage of total revenue increased to 48.4% in 2025, as compared to 48.1% in 2024.

Operating Labor. Operating labor includes all salaries and wages paid to operational employees and district managers, together with payroll taxes and benefits. Operating labor decreased by $6.9 million, or 1.1%, to $602.3 million for the year ended December 31, 2025, as compared to $609.2 million in 2024, primarily due to decreases of $6.4 million and $4.4 million in the Rent-A-Center and Acima segments, respectively, partially offset by the addition of the Brigit segment with $4.0 million in operating labor. The decrease in Rent-A-Center operating labor was primarily attributable to a decrease in corporate-owned store count, resulting from prior year store closures and refranchising. Operating labor expressed as a percentage of total revenue was 12.8% for the year ended December 31, 2025, as compared to 14.1% in 2024.

Non-Labor Operating Expenses. Non-labor operating expenses include LCOs, occupancy, delivery, advertising, selling, insurance, travel and other operating expenses. Non-labor operating expenses increased by $138.3 million, or 17.0%, to $949.9 million for the year ended December 31, 2025, as compared to $811.6 million in 2024, primarily due to the addition of the Brigit segment with $124.5 million in non-labor operating expenses and an increase of approximately $26.4 million in the Acima segment primarily related to an increase of $27.2 million in lease charge-off expense, partially offset by a decrease of approximately $13.2 million in the Rent-A-Center segment, primarily attributable to decreases of $11.3 million in lease-to-own store merchandise losses. Non-labor operating expenses expressed as a percentage of total revenue was 20.2% for the year ended December 31, 2025, as compared to 18.8% in 2024.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-02-23_item1_business.md)

Item 1. Business.

Upbound Group, Inc.

Unless the context indicates otherwise, references to "we," "us", "our", and the "Company" refer to the consolidated business operations of Upbound Group, Inc., the parent, and any or all of its direct and indirect subsidiaries. For any references in this document to Note A through Note U, refer to the Notes to consolidated financial statements in Item 8 included in this Annual Report on Form 10-K.

We are a technology and data-driven leader in accessible and inclusive financial solutions that address the evolving needs and aspirations of underserved consumers. Through our Acima and Rent-A-Center segments, we are a leading lease-to-own provider with operations in the United States, Puerto Rico and Mexico. We provide a critical service for underserved consumers by providing them with access to, and the opportunity to obtain ownership of, high-quality, name brand durable products under a flexible lease-purchase agreement with no long-term debt obligation. Our Acima segment offers lease-to-own solutions through retailers in stores and online enabling such retailers to grow sales by expanding their customer base utilizing our differentiated offering and allowing customers to access our flexible lease-to-own solutions at thousands of retailers and to lease a wide range of durable products. Through our Rent-A-Center segment, we provide a fully integrated customer experience through our e-commerce platform and brick and mortar presence.

On January 31, 2025, we completed the acquisition of Brigit, a holistic financial health technology company that has helped millions of customers improve their financial health and literacy, find ways to earn and save money, access their earned wages before their regularly scheduled payday, build their credit through savings and protect themselves from identity theft. Its mission is to help customers build a better financial future. See Note B in our consolidated financial statements included in this Annual Report on Form 10-K for additional information.

We were incorporated in the State of Delaware in 1986, and our common stock is traded on The Nasdaq Stock Market under the ticker symbol " UPBD. " Our principal executive offices are located at 5501 Headquarters Drive, Plano, Texas 75024. Our telephone number is (972) 801-1100 and our company website is www.upbound.com. Information contained on our website is not incorporated by reference into this Annual Report on Form 10-K.

The Lease Purchase Transaction

The lease purchase transaction is a flexible alternative that provides freedom for consumers who wish to obtain use and enjoyment of brand name merchandise with no long-term obligation and without having to pay the full price up front. Our customer has the right, but is not obligated, to acquire title to the merchandise either through an early purchase option or through payment of all lease renewals that would be required to obtain ownership.

The unit economics of the lease purchase transaction vary depending on the length of time customers take to obtain ownership of the product or whether the customer chooses to return the product without obtaining ownership. If a customer elects an early purchase option within a designated period of time following the initial lease, such as 90 or 120 days, a customer generally pays the retail price of the product plus a premium to the cost. Other lease-to-own transactions involve the customer leasing our merchandise through all optional lease renewal terms required to obtain ownership of the merchandise at the conclusion of the final lease renewal term. A customer may also elect to obtain ownership any time after the initial lease period, but prior to the completion of all lease renewals otherwise required to obtain ownership. Due to the longer lease period as a result of completing all lease renewals, along with the other benefits that are part of the lease-to-own transaction, obtaining ownership through payment of all lease renewals involves a higher total cost compared to the cost of the general retail price of the product if it was purchased upfront. Customers primarily take ownership of the merchandise through early purchase options, where the customer elects to make a lump-sum payment at a discounted purchase price prior to the final lease renewal. In the Rent-A-Center segment, the product is often rented more than one time before a customer ultimately obtains ownership.

There are differences in the unit economics between our Acima and Rent-A-Center segments, as we generally purchase our merchandise at wholesale prices for our Rent-A-Center segment and at retail prices for our Acima segment. Historically, operating margin for our Acima segment has benefited from the lower overhead cost associated with the virtual options employed at many third-party locations.

Key features of the lease purchase transaction include:

No long term obligation. A customer may terminate a lease purchase agreement at any time without penalty. Such customers have no obligation for remaining payments other than any outstanding balances to the date of return.

Convenient payment options. Our customers make payments on a weekly, bi-weekly, semi-monthly or monthly basis in our stores, at our third-party retailer locations, online or by telephone. We accept cash, credit or debit cards and payment via certain electronic platforms (such as PayPal and Venmo).

Flexible options to obtain ownership. Ownership of the merchandise generally transfers to the customer if the customer continuously renews the lease purchase agreement for a required period of between seven and 30 months, depending upon the product type, or exercises a specified early purchase option.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

- **CALL PERIOD: 2026Q2** (call dated 2026-07-30)
- **Recency:** same fiscal period as the latest earnings release in this pack.
- **File:** transcript_2026Q2_2026-07-30.md
- **Type:** EARNINGS PRESS RELEASE ONLY, not the call — no Q&A, no unscripted management commentary. Do not attribute call quotes to this.
- **Source:** https://www.sec.gov/Archives/edgar/data/933036/000119312526324902/upbd-ex99_2.htm

EX-99.2

3

upbd-ex99_2.htm

EX-99.2

Upbound Group, Inc. Earnings Release July 30, 2026 Second Quarter 2026 Results & Key Metrics $1,163M $22M $127M $0.37 $1.07 $0.39 Total Revenue Adjusted EBITDA1 GAAP Diluted EPS Non-GAAP Quarterly Dividend Per Share Net Earnings Diluted EPS1 Brigit Delivers over 35% Topline Growth, Acima LCO Improves Below 9%, Rent-A-Center Achieves Third Consecutive Quarter of Positive Same-Store Sales Affirming full year EBITDA and EPS Guidance. Second Quarter Results Within All Guided Ranges Second Quarter Consolidated Results CEO Commentary • Consolidated revenue of $1,163.4 million increased $5.9 million, or 0.5%, year-over-year. “The second quarter reflected continued solid execution for Upbound. We • GAAP operating profit of $54.3 million and non-GAAP operating profit1 of $108.7 million, compared to $50.7 million of GAAP operating profit and $116.2 million of non-GAAP operating profit in the prior year period. Second quarter 2026 GAAP operating profit margin was 4.7%, compared to 4.4% in the prior year period. delivered results within all of our guided ranges, generated robust cash flow, and made meaningful progress strengthening our balance sheet all while advancing our long-term strategic priorities," said CEO Fahmi Karam. • Net earnings on a GAAP basis of $21.6 million, compared to $15.5 million in the prior year period, a $6.1 million increase. Net profit margin of 1.9% increased 60 basis points year-over-year. "Our three complementary brands give us multiple avenues for growth and allow us to deepen customer relationships across products. Despite a tough operating environment, we executed well across the business including Rent-A-Center launching Amazon package pickups and returns at 1,500 stores nationally, Brigit executing a partnership agreement with Experian, and Acima expanding Adjusted EBITDA margin to over 16 percent." • Adjusted EBITDA1 decreased 4.6% year-over-year to $127.0 million. • Adjusted EBITDA margin1 of 10.9% decreased 60 basis points compared to the prior year period. • GAAP diluted earnings per share was $0.37, compared to GAAP diluted earnings per share of $0.26 in the prior year period. • Non-GAAP diluted earnings per share1, which excludes the impact of special items described at the end of this release, was $1.07 for the second quarter of 2026, compared to $1.12 in the prior year period. "We're energized by the opportunities ahead. By reinforcing underwriting discipline, strategically investing in AI, shared data platforms, and a more connected, personalized customer experience, we're building a stronger, more efficient platform positioned to sustain profitability and create long-term value for our shareholders," concluded Mr. Karam. • Improvement in lease-to-own charge-off performance, with Acima LCO rate decreasing 50 basis points year-over-year while Rent-A- Center LCO rate increased 30 basis points year-over-year. • Quarterly dividend per share of $0.39, or $1.56 annualized.

_[...truncated at ~3,000 chars of this document]_

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-02-23_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-02-23_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-02-23_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-30_2-02-results.md, 10-K_2026-02-23_item7_mdna.md, 10-K_2026-02-23_item1_business.md, transcript_2026Q2_2026-07-30.md

**Missing:** none

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
