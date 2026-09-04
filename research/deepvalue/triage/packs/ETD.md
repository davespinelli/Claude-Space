# Triage pack — ETD · ETHAN ALLEN INTERIORS INC

_Generated 2026-09-04 15:12 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** ETD · **Name:** ETHAN ALLEN INTERIORS INC
- **CIK:** 0000896156
- **SIC:** 2511 — Wood Household Furniture, (No Upholstered)
- **Fiscal year end (MM-DD):** 06-30
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/ETD

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** ETHAN ALLEN INTERIORS INC
- **CIK:** 896,156 · **SIC:** 2511 (Wood Household Furniture, (No Upholstered)) · **Exchange:** NYSE

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 21.87 |
| mktcap | $556.5M |
| ev | $482.9M |
| ev_ebit | 7.8x |
| fcf | $50.4M |
| fcf_yield | 9.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 12.3% |
| net_debt | -$73.6M |
| net_debt_ebit | -1.2x |
| cash | $73.6M |
| ltd | $0.00 |
| equity | $471.5M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $614.6M |
| revenue_prior | $646.2M |
| rev_growth | -4.9% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $62.0M |
| net_income | $63.8M |
| cfo | $61.7M |
| capex | $11.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 25,446,339 |
| shares_py | 25,429,960 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -12.1% |
| r6m | 17.1% |
| off_52w_high | -11.1% |
| adv20 | $15.1M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.69 |
| r_ev_ebit | 0.83 |
| r_roic | 0.76 |
| r_rev_growth | 0.19 |
| r_buyback | 0.65 |
| score | 0.63 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q1I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 117 |

**Screen rationale:** cheap at 7.8x EV/EBIT; high ROIC 12.3%; debt data missing (net cash unverified)


## 3. Share count trend

- Shares outstanding: **25,446,339** (CY2026Q1I) vs **25,429,960** prior year (CY2025Q1I)
- Change: **0.1%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-02 among the 2 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 1,000 sh / $24,610 vs sells 26,144 sh / $654,578 -> net $-629,968 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: Tsai Cynthia Ekberg bought 1,000 sh @ $24.61 ($24,610) on 2026-08-05.

Form 4 filings parsed: 12; transaction rows: 27 (open-market buys 1, sales 10).

| code | rows |
|---|---|
| A | 7 |
| F | 9 |
| P | 1 |
| S | 10 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-29_2-02-results.md)

_Extraction: started at the first release heading, 'Ethan Allen Reports Fiscal 2026 Full Year and Fourth Quarter Results; '; skipped 10 forward-looking-statement block(s); 4 block(s) of pre-heading matter dropped._

## EX-99.1 - EXHIBIT 99.1 (ex_994023.htm)

Ethan Allen Reports Fiscal 2026 Full Year and Fourth Quarter Results; Strong Margins and Robust Balance Sheet Despite Macroeconomic Challenges; Declares Special and Regular Cash Dividend

DANBURY, CT – July 29, 2026 – Ethan Allen Interiors Inc. ("Ethan Allen" or the "Company") (NYSE: ETD), a leading interior design destination, today reported its results for the fiscal 2026 full year and fourth quarter ended June 30, 2026 and announced a special and regular cash dividend.

Farooq Kathwari, Ethan Allen's Chairman, President and CEO commented, "We are pleased to report our fiscal 2026 financial and operating results, which include strong margins and a robust balance sheet despite a challenging operating environment. Fiscal 2026 marked a year where we further strengthened many areas of our vertically integrated enterprise, including our talent, product offerings, marketing, technology, retail network, manufacturing, logistics and social responsibility. Recent product introductions, which portray classics with a modern perspective, resonate with our clients. We remain confident in our long-term strategy as the interior design destination, operating a vertically integrated enterprise with 171 Ethan Allen Retail Design Centers in North America and more internationally, and supported by strong North American manufacturing and logistics."

"We remain focused on implementing meaningful strategies to further strengthen our business. We have been able to improve operating efficiency and run a leaner enterprise despite a reduction in business with the U.S. State Department and sluggish demand. For the quarter ended June 30, 2026, we reported consolidated net sales of $146.8 million, adjusted gross margin of 59.7%, adjusted operating income of $10.8 million, adjusted operating margin of 7.4% and adjusted diluted EPS of $0.36. Wholesale segment written orders declined 11.9% compared to last year while our Retail segment written orders declined 10.8% as a difficult prior year comparison combined with lower design center traffic and broader macroeconomic uncertainty, including global unrest, created near-term pressure on our written sales. Our adjusted operating margin of 7.4% reflects the impact of tariffs partially offset by our focus on cost control and operational efficiencies."

"We remain debt-free with substantial liquidity and a robust balance sheet to support long-term growth. During the just completed fourth quarter we generated $22.4 million in operating cash flow, including $5.0 million from tariff refunds. Our strong operating cash flow combined with disciplined capital management helped drive our ending total cash and investments to $187.5 million, which reflects our commitment to maintaining the financial strength needed in today's challenging environment. We continued our history of returning capital to shareholders by paying a regular quarterly cash dividend of $10.0 million and are pleased to announce that yesterday our Board approved a special cash dividend of $0.25 per share and a regular quarterly cash dividend of $0.39 per share, both payable on August 26, 2026."

"Our vertical integration and focus on one brand are our strengths. Throughout our 94-year history, we've navigated many economic and housing cycles through constant reinvention. We are committed to offering relevant quality products, providing complimentary interior design service and manufacturing approximately 75% of the custom furniture in our own North American facilities. We acknowledge the ways technology is changing the furniture shopping experience and through investments in our people, our design centers, our marketing and our technology, we are creating a stronger client engagement experience while expanding into additional retail markets. We want to thank our teams across Ethan Allen for their continued dedication and execution, and our shareholders for their ongoing support as we remain focused on driving long-term shareholder value. We look forward to continuing our progress and remain cautiously optimistic," concluded Mr. Kathwari.

FISCAL 2026 FOURTH QUARTER HIGHLIGHTS*

● | Consolidated net sales of $146.8 million; prior year $160.4 million

- | Retail net sales of $132.0 million; prior year $138.5 million

- | Wholesale net sales of $79.7 million; prior year $87.2 million

● | Written orders

- | Retail segment written orders declined 10.8%

- | Wholesale segment written orders decreased 11.9%

● | Consolidated gross margin of 63.1%; adjusted gross margin of 59.7%; prior year 59.9%; included in the current year consolidated gross margin was the recovery of $5.0 million in previously paid tariffs imposed under the International Emergency Economic Protection Act ("IEEPA"); these refunds reflect claims made through the U.S. Customs and Border Protection refund system and increased both consolidated gross and operating margin by 340 basis points in the just completed fourth quarter

● | Selling, general and administrative expenses ("SG&A") decreased 4.4% from last year from reduced variable expenses, strong cost control, reduced headcount and lower marketing costs

● | Marketing spend totaled $4.7 million or 3.2% of consolidated net sales; prior year 3.4%

● | Consolidated operating margin of 9.8%; adjusted consolidated operating margin of 7.4%; adjusted prior year 9.7%; current year operating margin impacted by higher tariffs and fixed cost deleveraging from lower consolidated net sales

● | Diluted EPS of $0.46; adjusted diluted EPS of $0.36; adjusted prior year $0.49

● | Generated $22.4 million in operating cash flow; prior year $24.8 million

● | Paid cash dividends of $10.0 million or $0.39 per share, the same as a year ago

● | Repurchased 250,000 shares of Company stock for $4.8 million under the existing share repurchase program; remaining authorization to repurchase 1,757,364 shares of stock pursuant to the program

FISCAL 2026 FULL YEAR HIGHLIGHTS*

● | Consolidated net sales of $579.5 million; prior year $614.6 million

- | Retail net sales of $511.2 million; prior year $523.1 million

- | Wholesale net sales of $330.7 million; prior year $359.1 million

● | Written orders

- | Retail segment written orders 6.1% lower

- | Wholesale segment written orders decreased 11.2%

● | Consolidated gross margin of 61.2%; prior year 60.5%

● | SG&A expenses, representing 53.3% of sales, decreased 0.4%

● | Consolidated operating margin of 7.8%; adjusted operating margin of 8.1%; adjusted prior year 10.2%

● | Diluted EPS of $1.56; adjusted diluted EPS of $1.61; adjusted prior year $2.04

● | Generated $52.5 million of cash from operating activities; $61.7 million a year ago

● | Paid cash dividends totaling $46.3 million during fiscal 2026, including a special cash dividend of $0.25 per share in August 2025

● | Invested $11.0 million in capital expenditures; comparable to $11.3 million a year ago

● | Ended the fiscal year with $187.5 million in total cash and investments; no outstanding debt

● | Inventory levels rose to $148.5 million at June 30, 2026, up 5.4%

● | Headcount totaled 3,062 associates at fiscal year-end, down 4.6%

● | Four new Company-operated design centers located in Colorado Springs (CO), San Diego (CA), Vancouver (Canada) and Thornhill (Canada) were opened during fiscal 2026 that showcase Ethan Allen home furnishings while combining complimentary interior design services with technology

● | Ended the fiscal year with 171 Ethan Allen retail design centers in North America, including 141 Company-operated and 30 independently owned and operated

● | New Company-operated design centers to be opened during fiscal 2027 include locations in Victoria Gardens (CA), Aventura (FL), Burlington (VT), Brooklyn (NY) and Naples (FL)

● | New tariffs under Section 301 of the Trade Act of 1974 became effective on July 24, 2026, and range between 10% and 12.5%; these tariffs replace the previously issued 10% global tariffs imposed under Section 122, which recently expired

● | For the third year in a row Ethan Allen was named America's #1 Premium Furniture Retailer

● | The Sustainable Furnishings Council and the National Wildlife Federation awarded Ethan Allen a "High Score" on their Wood Furniture Scorecard for its commitment to the use of sustainable wood in furniture manufacturing

● | Ethan Allen's upholstery operation in Silao, Mexico was recently awarded the Great Place to Work® certification for the eighth consecutive year; in addition to this designation, the Silao operation was recognized as "Empresa Socialmente Responsible" (Environmentally and Socially Responsible) for the seventh consecutive year

● | Celebrated Ethan Allen Day in June to honor the pioneering spirit of its namesake and celebrate the 94-year history of Ethan Allen as an iconic American brand

● | Held the Company's annual convention at its headquarters and livestreamed across the world; under the theme of Always Moving Forward , the program reviewed initiatives in manufacturing, logistics, technology, marketing and retail, and celebrated interior designers both for achievement in written sales and design excellence

* See reconciliation of GAAP to adjusted key financial measures in the back of this release; comparisons are to the fourth quarter and full fiscal 2025 year

KEY FINANCIAL MEASURES*

(Unaudited) | ​
(In thousands, except per share data) | ​
​ | ​ | Three months ended June 30, | ​ | ​ | Twelve months ended June 30, | ​
​ | ​ | 2026 | ​ | ​ | 2025 | ​ | ​ | 2026 | ​ | ​ | 2025 | ​
Net sales | ​ | 146,752 | ​ | ​ | 160,357 | ​ | ​ | 579,487 | ​ | ​ | 614,649 | ​
GAAP gross profit | ​ | 92,616 | ​ | ​ | 96,059 | ​ | ​ | 354,771 | ​ | ​ | 372,121 | ​
Adjusted gross profit* | ​ | 87,661 | ​ | ​ | 96,059 | ​ | ​ | 354,771 | ​ | ​ | 372,121 | ​
GAAP operating income | ​ | 14,347 | ​ | ​ | 15,269 | ​ | ​ | 45,016 | ​ | ​ | 61,988 | ​
Adjusted operating income* | ​ | 10,823 | ​ | ​ | 15,588 | ​ | ​ | 46,651 | ​ | ​ | 62,895 | ​
GAAP operating margin | ​ | ​ | 9.8 | % | ​ | ​ | 9.5 | % | ​ | ​ | 7.8 | % | ​ | ​ | 10.1 | %
Adjusted operating margin* | ​ | ​ | 7.4 | % | ​ | ​ | 9.7 | % | ​ | ​ | 8.1 | % | ​ | ​ | 10.2 | %
GAAP net income | ​ | 11,754 | ​ | ​ | 12,268 | ​ | ​ | 39,883 | ​ | ​ | 51,596 | ​
Adjusted net income* | ​ | 9,122 | ​ | ​ | 12,505 | ​ | ​ | 41,104 | ​ | ​ | 52,271 | ​
GAAP diluted EPS | ​ | 0.46 | ​ | ​ | 0.48 | ​ | ​ | 1.56 | ​ | ​ | 2.01 | ​
Adjusted diluted EPS* | ​ | 0.36 | ​ | ​ | 0.49 | ​ | ​ | 1.61 | ​ | ​ | 2.04 | ​
Cash flows from operating activities | ​ | 22,419 | ​ | ​ | 24,817 | ​ | ​ | 52,477 | ​ | ​ | 61,696 | ​

* See reconciliation of GAAP to adjusted key financial measures in the back of this release

BALANCE SHEET and CASH FLOW

Cash and investments totaled $187.5 million at June 30, 2026 compared with $196.2 million a year ago. The decrease during fiscal 2026 was due to $46.3 million in cash dividends paid, capital expenditures of $11.0 million and share repurchases of $4.8 million partially offset by $52.5 million in cash generated by operating activities, including $5.0 million in tariff refunds.

Cash from operating activities totaled $52.5 million during fiscal 2026, a decrease from $61.7 million in the prior year primarily due to lower net income, incremental restructuring payments and changes in working capital, including an increase in inventory carrying levels and lower customer deposits.

Cash dividends paid during fiscal 2026 totaled $46.3 million, which included a special cash dividend of $6.4 million, or $0.25 per share, and regular quarterly cash dividends totaling $39.9 million.

Inventories, net totaled $148.5 million at June 30, 2026, an increase of 5.4% since last year as new product introductions combined with price increases drove higher levels of on-hand inventory but improved in-stock inventory positions.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-09-03_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

Executive Overview

Who We Are . Founded in 1932, Ethan Allen is a leading interior design company, manufacturer and retailer in the home furnishings marketplace. We are a global luxury home fashion brand that is vertically integrated from product design through home delivery, which offers clients stylish product offerings, artisanal quality and personalized service. We are known for the quality and craftsmanship of our products as well as for the exceptional personal service from design to delivery. We provide complimentary interior design service to our clients and sell a full range of home furnishings through a retail network of design centers located throughout the U.S. and internationally as well as online at ethanallen.com.

Ethan Allen design centers represent a mix of locations operated by independent licensees and Company-operated locations. At June 30, 2026, the Company operates 141 retail design centers, 136 located in the U.S. and five in Canada. Our independently operated design centers are located in the U.S., Asia, the Middle East and Europe. During fiscal 2026, we opened four new Company-operated design centers in Colorado Springs, Concord (Canada), San Diego and Vancouver.

We also own and operate eleven manufacturing facilities, including four manufacturing plants, one sawmill, one rough mill and a kiln dry lumberyard in the U.S., three upholstery manufacturing plants in Mexico and one case goods manufacturing plant in Honduras. Approximately 75% of our furniture is manufactured in our North American plants. We also contract with various suppliers located in Europe, Asia and other countries to import products.

Ethan Allen focuses on the key areas of talent, service, marketing, technology and social responsibility. Our initiatives to introduce new products, run strong marketing campaigns, invest in our North American manufacturing, and maintain our logistics network throughout North America has positioned us well for sustained profitability and returning value to shareholders.

ETHAN ALLEN INTERIORS INC. AND SUBSIDIARIES

Foundation: Ethan Allen is rooted in our core values of quality, craftsmanship and personal service—values that have enabled us to navigate many economic and housing cycles. Through constant reinvention, including the evolution from a wholesale dealer business to a retail network, we have remained profitable each year since going public in 1993 and have built a differentiated enterprise supported by strong margins, disciplined management and consistent cash dividends. Vertically integrated from retail to manufacturing to logistics, we continue to craft 75% of our furniture in eleven North American manufacturing plants, supporting jobs, strengthening our supply chain and investing in quality.

Business Model. Our vertical integration is a competitive advantage for us. Our North American manufacturing and logistics operations are an integral part of an overall strategy to maximize production efficiencies and maintain this competitive advantage. Our business model is to focus on providing relevant product offerings, capitalizing on the personal service offered to our clients by our interior design professionals, leveraging the benefits of our vertical integration including a manufacturing presence in North America, investing in new technologies across our business, maintaining a strong logistics network, communicating our messages with strong marketing campaigns, and utilizing an omni-channel approach via our website, ethanallen.com. We aim to position Ethan Allen as the premier interior design destination and a preferred brand offering products of superior style, quality, and value to clients with a comprehensive, one-stop shopping solution for their home furnishing and interior design needs. We seek to constantly reinvent our projection and product offerings through a broad selection of products, designed to complement one another, reflecting current fashion trends in home furnishing.

Talent. At June 30, 2026, our employee count totaled 3,062, with 2,137 employees in our wholesale segment and 925 in our retail segment. Our employee count decreased 4.6% or 149 associates during fiscal 2026, with 47 fewer employees in retail and 102 fewer employees in wholesale. We continually look for opportunities to strengthen our teams while at the same time optimizing headcount through operational efficiencies.

Fiscal 2026 Financial Year in Review (1) . Our financial performance during fiscal 2026 was highlighted by strong margins, positive operating cash flow and strong cash dividends supported by a robust balance sheet despite operating in a challenging macroeconomic environment. We were able to improve operating efficiency and run a leaner enterprise despite a reduction in our contract business and sluggish demand. Consolidated net sales of $579.5 million were down 5.7% compared to the prior year due to lower contract sales, a decline in delivered unit volume and fewer incoming orders which led to lower available backlog partially offset by a higher average ticket price. Our consolidated gross margin of 61.2% was higher than 60.5% in the prior year due to a change in sales mix, lower in-bound freight costs, reduced headcount and a higher average ticket price. Our operating margin was 7.8% compared to 10.1% in the prior year primarily due to deleveraging from lower consolidated net sales and higher tariffs partially offset by disciplined cost management and retail price increases. Diluted earnings per share of $1.56 was lower than $2.01 in the prior year due to fewer net sales and the impact of tariffs.

We remain debt-free with substantial liquidity and a robust balance sheet to support long-term growth. We generated $52.5 million in operating cash flow during fiscal 2026, which helped grow our total cash and investments to $187.5 million at June 30, 2026. We continued our history of returning capital to shareholders by paying four regular quarterly cash dividends of $0.39 per share and a special cash dividend of $0.25 per share, bringing the total amount of dividends paid to $46.3 million during fiscal 2026. As part of our capital allocation strategy, we also repurchased 250,000 shares of Company stock for $4.8 million during fiscal 2026. Inventory levels totaled $148.5 million at June 30, 2026, an increase of 5.4% since last year as new product introductions combined with price increases drove higher levels of on-hand inventory but improved in-stock inventory positions. Customer deposits from undelivered written orders totaled $62.7 million at June 30, 2026, down from $75.1 million a year ago as delivered sales outpaced incoming retail written orders. Our wholesale backlog was $44.3 million at June 30, 2026, a decrease of 9.3% due to a slowdown in orders and improved customer lead times.

(1) | Refer to the Regulation G Reconciliation of Non-GAAP Financial Measures section within this MD&A for the reconciliation of U.S. generally accepted accounting principles ("GAAP") to adjusted key financial metrics.

ETHAN ALLEN INTERIORS INC. AND SUBSIDIARIES

Key Operating Metrics

A summary of our key operating metrics is presented in the following table (in millions, except per share data).

Fiscal Year Ended June 30,
2026 | % of Sales | % Chg | 2025 | % of Sales | % Chg | 2024 | % of Sales | % Chg
Net sales | 579.5 | 100.0 | % | (5.7 | %) | 614.6 | 100.0 | % | (4.9 | %) | 646.2 | 100.0 | % | (18.3 | %)
Gross profit | 354.8 | 61.2 | % | (4.7 | %) | 372.1 | 60.5 | % | (5.3 | %) | 393.1 | 60.8 | % | (18.2 | %)
Operating income | 45.0 | 7.8 | % | (27.4 | %) | 62.0 | 10.1 | % | (20.5 | %) | 78.0 | 12.1 | % | (43.2 | %)
Adjusted operating income (1) | 46.7 | 8.1 | % | (25.8 | %) | 62.9 | 10.2 | % | (19.3 | %) | 77.9 | 12.1 | % | (41.6 | %)
Net income | 39.9 | 6.9 | % | (22.7 | %) | 51.6 | 8.4 | % | (19.1 | %) | 63.8 | 9.9 | % | (39.7 | %)
Adjusted net income (1) | 41.1 | 7.1 | % | (21.4 | %) | 52.3 | 8.5 | % | (18.0 | %) | 63.8 | 9.9 | % | (38.1 | %)
Diluted EPS | 1.56 | (22.4 | %) | 2.01 | (19.3 | %) | 2.49 | (39.7 | %)
Adjusted diluted EPS (1) | 1.61 | (21.1 | %) | 2.04 | (18.1 | %) | 2.49 | (38.2 | %)
Cash flow from operating activities | 52.5 | (14.9 | %) | 61.7 | (23.1 | %) | 80.2 | (20.3 | %)
Return on equity | 8.6 | % | 10.8 | % | 13.4 | %
Wholesale written orders | (11.2 | %) | (3.2 | %) | (10.9 | %)
Retail written orders | (6.1 | %) | (1.5 | %) | (8.4 | %)

(1) | Refer to the Regulation G Reconciliation of Non-GAAP Financial Measures section within this MD&A for the reconciliation of GAAP to adjusted key financial metrics.

Results of Operations

For an understanding of the significant factors that influenced our financial performance in fiscal 2026 compared with fiscal 2025, the following discussion should be read in conjunction with the consolidated financial statements and related notes presented under Item 8 in this Annual Report on Form 10-K. Refer to Results of Operations under Item 7, Management ' s Discussion and Analysis of Financial Condition and Results of Operations , contained in Part II of our Annual Report on Form 10-K for the fiscal year ended June 30, 2025, filed with the SEC on August 22, 2025, for an analysis of the fiscal 2025 results as compared to fiscal 2024.

(in thousands) | Fiscal Year Ended June 30,
2026 | 2025 | % Change
Consolidated net sales | 579,487 | 614,649 | (5.7 | %)
Wholesale net sales | 330,695 | 359,057 | (7.9 | %)
Retail net sales | 511,195 | 523,142 | (2.3 | %)
Consolidated gross profit | 354,771 | 372,121 | (4.7 | %)
Consolidated gross margin | 61.2 | % | 60.5 | %

Net Sales

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-09-03_item1_business.md)

ITEM 1. BUSINESS

Overview

Ethan Allen is a leading interior design company, manufacturer and retailer in the home furnishings marketplace. We are a global luxury home fashion brand that is vertically integrated from product design through home delivery, which offers our customers stylish product offerings, artisanal quality, and personalized service. We are known for the quality and craftsmanship of our products as well as for the exceptional personal service from design to delivery, and for our commitment to social responsibility and sustainable operations. Our strong network of entrepreneurial leaders and interior designers provide complimentary interior design service to our clients and sell a full range of home furnishing products through a retail network of design centers located throughout the United States ("U.S.") and abroad as well as online at ethanallen.com.

Ethan Allen design centers represent a mix of locations operated by independent licensees and Company-operated locations. At June 30, 2026, the Company operates 141 retail design centers with 136 located in the U.S. and five in Canada. Our 43 independently operated design centers are located in the U.S., Asia, the Middle East and Europe. We manufacture approximately 75% of our furniture in our North American manufacturing plants and have been recognized for product quality and craftsmanship since we were founded in 1932. We own and operate eleven manufacturing facilities, including four manufacturing plants, one sawmill, one rough mill and one kiln dry lumberyard in the U.S., three manufacturing plants in Mexico and one manufacturing plant in Honduras. The Company also partners with suppliers located in Europe, Asia, and other countries to produce and import various products that support the business.

We regularly update display presentations and floor plans, strengthen the qualifications of our designers through training and certifications and combine technology with personal service in our design centers. Over the past 10 years, 25% of our design centers are new or have been relocated as we continually evaluate our retail footprint. In the past five years, we have either opened or relocated 17 design centers with an average size of 7,230 square feet. These new design centers reflect our shift to lifestyle centers that better project our brand and optimize space. During fiscal 2026, four new Company-operated design centers were opened that showcase Ethan Allen home furnishings while combining complimentary interior design services with technology.

Business Strategy

Our vertical integration is a competitive advantage for us. Our North American manufacturing and logistics operations are an integral part of an overall strategy to maximize production efficiencies and maintain this competitive advantage. Being vertically integrated across retail, manufacturing and logistics gives us additional flexibility to navigate changing economic conditions while managing quality and service at a high level. We strive to deliver value to our shareholders through the execution of our strategic initiatives focused on the concept of constant reinvention. Ethan Allen has a distinct vision of classic American style with a modern perspective, which we believe differentiates us from our competitors. Our business model is to maintain continued focus on (i) providing relevant product offerings, (ii) capitalizing on the professional and personal service offered to our clients by our interior design professionals, (iii) leveraging the benefits of our vertical integration including a strong manufacturing presence in North America, (iv) regularly investing in new technologies across all aspects of our vertically integrated business, (v) maintaining a strong logistics network, (vi) communicating our messages with strong marketing campaigns, and (vii) utilizing our website, ethanallen.com, as a key marketing tool to drive traffic to our retail design centers.

We aim to position Ethan Allen as a premier interior design destination and a preferred brand offering products of superior style, quality, and value to clients with a comprehensive solution for their home furnishing and interior design needs. We operate our business with an entrepreneurial attitude, staying focused on long-term growth, and treating our employees, vendors, and clients with dignity and respect.

Product

Ethan Allen has kept a disciplined approach to core product assortment. Our focus on maximizing customization and client choice has helped us minimize unnecessary complexity. As a leading interior design destination, our strategy supports personalization and customization, allowing clients and designers to tailor products. We manufacture 75% of the furniture we offer by combining the craftsmanship of our skilled associates with technology in our North American facilities. Every product bears the distinctive quality of the Ethan Allen brand and is sold under the one Ethan Allen brand name. Meticulously hand-guided stitching dresses our upholstery frames and our case goods wood furniture is crafted from premium lumber and veneers, which are individually finished and customized. Our commitment to using leading construction techniques is evident, including using mortise and tenon joinery and four-corner glued dovetail joinery for drawers. These elements are part of Ethan Allen's identity, solidifying our reputation for quality, style and exclusive home furnishings and décor. We exclusively sell Ethan Allen products in our design centers.

ETHAN ALLEN INTERIORS INC. AND SUBSIDIARIES

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-09-03_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-09-03_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-09-03_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-29_2-02-results.md, 10-K_2026-09-03_item7_mdna.md, 10-K_2026-09-03_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
