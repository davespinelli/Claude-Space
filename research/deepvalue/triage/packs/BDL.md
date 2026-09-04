# Triage pack — BDL · FLANIGANS ENTERPRISES INC

_Generated 2026-09-04 13:59 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** BDL · **Name:** FLANIGANS ENTERPRISES INC
- **CIK:** 0000012040
- **SIC:** 5812 — Retail-Eating  Places
- **Fiscal year end (MM-DD):** 10-03
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/BDL

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** FLANIGANS ENTERPRISES INC
- **CIK:** 12,040 · **SIC:** 5812 (Retail-Eating  Places) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 45.85 |
| mktcap | $85.2M |
| ev | $85.8M |
| ev_ebit | 9.8x |
| fcf | $4.7M |
| fcf_yield | 5.5% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 9.8% |
| net_debt | $590k |
| net_debt_ebit | 0.1x |
| cash | $28.8M |
| ltd | $29.4M |
| equity | $69.8M |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $205.2M |
| revenue_prior | $187.2M |
| rev_growth | 9.6% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $8.7M |
| net_income | $5.0M |
| cfo | $10.5M |
| capex | $5.8M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.0% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 1,858,647 |
| shares_py | 1,858,647 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 58.3% |
| r6m | 39.1% |
| off_52w_high | -11.4% |
| adv20 | $1.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.53 |
| r_ev_ebit | 0.77 |
| r_roic | 0.70 |
| r_rev_growth | 0.64 |
| r_buyback | 0.67 |
| score | 0.71 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q2I |
| shares_py_period | CY2025Q2I |
| capex_missing | False |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 53 |

**Screen rationale:** cheap at 9.8x EV/EBIT; 12-1 momentum 58.3%


## 3. Share count trend

- Shares outstanding: **1,858,647** (CY2026Q2I) vs **1,858,647** prior year (CY2025Q2I)
- Change: **0.0%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 3,866 sh / $119,312 vs sells 0 sh / $0 -> net $119,312 (BUYING).
Distinct insiders buying (code P): 1. Largest buy: FLANIGAN JAMES II bought 975 sh @ $32.00 ($31,200) on 2026-05-18.

Form 4 filings parsed: 2; transaction rows: 8 (open-market buys 8, sales 0).

| code | rows |
|---|---|
| P | 8 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2025-12-19_item7_mdna.md)

_Extraction: started at the Overview heading; window reaches 'Results of Operations'._

OVERVIEW

Financial Information Concerning Industry Segments

Our business is conducted
principally in two segments: the restaurant segment and the package liquor store segment. Financial information broken into these two
principal industry segments for the two fiscal years ended September 27, 2025 and September 28, 2024 is set forth in the Consolidated
Financial Statements which are attached hereto.

General

As of September 27, 2025,
we (i) operated 32 units, consisting of restaurants, sports bar, package liquor stores and combination restaurants/package liquor stores
that we either own or have operational control over and partial ownership in; and (ii) franchises an additional five units, consisting
of two restaurants (one of which we operate) and three combination restaurants/package liquor stores.

Franchised Units .
In exchange for our providing management and related services to our franchisees and granting them the right to use our service marks
"Flanigan's Seafood Bar and Grill" and "Big Daddy's Liquors", our franchisees (four of which are
franchised to members of the family of our Chairman of the Board, officers and/or directors), are required to (i) pay to us a royalty
equal to 1% of gross package liquor sales and 3% of gross restaurant sales; and (ii) make advertising expenditures equal to between 1.5%
to 3% of all gross sales based upon our actual advertising costs allocated between stores, pro-rata, based upon gross sales.

Affiliated Limited Partnership
Owned Units . We manage and control the operations of ten of the eleven restaurants owned by limited partnerships, except the Fort
Lauderdale, Florida restaurant which is managed and controlled by a related franchisee. Accordingly, the results of operations of all
limited partnership owned restaurants, except the Fort Lauderdale, Florida restaurant are consolidated with our results of operations
for accounting purposes. The results of operations of the Fort Lauderdale, Florida restaurant are accounted for by us utilizing the equity
method.

RESULTS OF OPERATIONS

REVENUES (in thousands):

For the Fiscal Year Ended
September 27, 2025 | September 28, 2024
Amount | Percent | Amount | Percent
(In thousands) | (In thousands)
Restaurant food sales | 124,501 | 61.25 | 114,795 | 61.95
Restaurant bar sales | 31,764 | 15.63 | 30,010 | 16.20
Package store sales | 46,988 | 23.12 | 40,497 | 21.85
Total Sales | 203,253 | 100.00 | 185,302 | 100.00
Franchise related revenues | 1,754 | 1,693
Other revenues | 241 | 221
Total Revenue | 205,248 | 187,216

Comparison of Fiscal Years Ended September 27, 2025 and September
28, 2024

Revenues.
Total revenue for our fiscal year 2025 increased $18,032,000 or 9.63% to $205,248,000 from $187,216,000 for our fiscal year 2024 due
primarily to increased package liquor store and restaurant sales, increased menu prices and revenue generated from our Company-owned
restaurant in Hollywood, Florida (Store #19R) for our entire fiscal year 2025 as opposed to a part of our fiscal year 2024.
Effective February 23, 2025, we increased our menu prices for our bar offerings to target an increase to our bar revenues of
approximately 0.84% annually. Effective December 4, 2024, we increased our menu prices for our bar offerings to target an increase
to our bar revenues of approximately 4.90% annually and effective November 17, 2024 we increased our menu prices for our food
offerings to target an increase to our food revenues of approximately 4.14% annually. Effective August 25, 2024, we increased menu
prices for our bar offerings to target an increase to our bar revenues of approximately 5.63% annually to offset higher food and
liquor costs and higher overall expenses (collectively the "Recent Price Increases").

Restaurant Food Sales .
Restaurant revenue generated from the sale of food, including non-alcoholic beverages, at restaurants totaled $124,501,000 for our fiscal
year 2025 as compared to $114,795,000 for our fiscal year 2024. The increase in restaurant food sales is attributable to the Recent Price
Increases and food sales generated from our Company-owned restaurant in Hollywood, Florida (Store #19R) for our entire fiscal year 2025
as opposed to a part of our fiscal year 2024. Comparable weekly restaurant food sales for restaurants open for all of our fiscal years
2025 and 2024, which consists of ten restaurants owned by us (excluding our Hollywood, Florida location Store #19R which opened for business
during the second quarter of our fiscal year 2024) and ten restaurants owned by affiliated limited partnerships was $2,245,000 and $2,122,000
for our fiscal years 2025 and 2024 respectively, an increase of 5.80%. Comparable weekly restaurant food sales for Company-owned restaurants
only (excluding our Hollywood, Florida location Store #19R which opened for business during the second quarter of our fiscal year 2024)
was $997,000 and $938,000 for our fiscal years 2025 and 2024, respectively, an increase of 6.29%. Comparable weekly restaurant food sales
for affiliated limited partnership owned restaurants only was $1,248,000 and $1,184,000 for our fiscal years 2025 and 2024 respectively,
an increase of 5.41%. We expect that restaurant food sales, including non-alcoholic beverages, for our fiscal year 2026 will increase
due to increased restaurant traffic.

Restaurant Bar Sales.
Restaurant revenue generated from the sale of alcoholic beverages at restaurants totaled $31,764,000 for our fiscal year 2025 as compared
to $30,010,000 for our fiscal year 2024. The increase in restaurant bar sales is attributable to the Recent Price Increases and bar sales
generated from our Company-owned restaurant in Hollywood, Florida (Store #19R) for our entire fiscal year 2025 as opposed to a part of
our fiscal year 2024. Comparable weekly restaurant bar sales for restaurants open for all of our fiscal years 2025 and 2024 respectively,
which consists of ten restaurants owned by us (excluding our Hollywood, Florida location Store #19R which opened for business during
the second quarter of our fiscal year 2024) and ten restaurants owned by affiliated limited partnerships was $583,000 for our fiscal
year 2025 and $562,000 for our fiscal year 2024, an increase of 3.74%. Comparable weekly restaurant bar sales for Company-owned restaurants
only (excluding our Hollywood, Florida location Store #19R which opened for business during the second quarter of our fiscal year 2024)
was $244,000 and $234,000 for our fiscal years 2025 and 2024 respectively, an increase of 4.27%. Comparable weekly restaurant bar sales
affiliated limited partnership owned restaurants only was $339,000 and $328,000 for our fiscal years 2025 and 2024 respectively, an increase
of 3.35%. We expect that restaurant bar sales for our fiscal year 2026 will increase due to increased restaurant traffic.

Package Liquor Store
Sales . Revenue generated from sales of liquor and related items at package liquor stores totaled $46,988,000 for our fiscal year
2025 as compared to $40,497,000 for our fiscal year 2024, an increase of $6,491,000. This increase was primarily due to increased package
liquor store traffic. The weekly average of same store package liquor store sales, which includes eleven (11) Company-owned package liquor
stores was $904,000 and $779,000 for our fiscal years 2025 and 2024 respectively, an increase of 16.05%. We expect that package liquor
store sales for our fiscal year 2026 will increase due to increased package liquor store traffic.

Costs and Expenses .
Costs and expenses (consisting of cost of merchandise sold, payroll and related costs, operating expenses, occupancy costs, selling,
general and administrative expenses and depreciation and amortization) for our fiscal year 2025 increased $15,128,000 or 8.34% to $196,503,000
from $181,375,000 for our fiscal year 2024. The increase was primarily due to increased payroll, an expected general increase in food
costs and overall expenses, as well as costs and expenses incurred from our Company-owned restaurant in Hollywood Florida (Store #19R)
for our entire fiscal year 2025 as opposed to a part of our fiscal year 2024, partially offset by actions taken by management to reduce
and/or control costs. We anticipate that our operating costs and expenses will continue to increase through our fiscal year 2026. Operating
costs and expenses decreased as a percentage of total revenue to approximately 95.74% in our fiscal year 2025 from 96.88% in our fiscal
year 2024.

Gross Profit .
Gross profit is calculated by subtracting the cost of merchandise sold from sales.

Restaurant Food and
Bar Sales . Gross profit for food and bar sales for our fiscal year 2025 increased to $104,091,000 from $94,943,000 for our fiscal
year 2024. Gross profit margin for the restaurant food and bar sales increased during our fiscal year 2025 when compared to our fiscal
year 2024 due to the Recent Price Increases, partially offset by higher food costs. Our gross profit margin for restaurant food and bar
sales (calculated as gross profit reflected as a percentage of restaurant food and bar sales), was 66.61% for our fiscal year 2025 and
65.57% for our fiscal year 2024.

Package Store Sales .
Gross profit for package store sales for our fiscal year 2025 increased to $11,803,000 from $10,369,000 for our fiscal year 2024. Our
gross profit margin, (calculated as gross profit reflected as a percentage of package liquor store sales), for package store sales was
25.12% for our fiscal year 2025 and 26.60% for our fiscal year 2024. We anticipate that the gross profit margin for package liquor store
merchandise will decrease for our fiscal year 2026 due to higher costs and a reduction in pricing of certain package store merchandise
to remain competitive.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2025-12-19_item1_business.md)

ITEM 1. BUSINESS

General

As of September 27, 2025,
Flanigan's Enterprises, Inc., a Florida corporation, together with its subsidiaries ("we", "our", "ours"
and "us" as the context requires), (i) operates 32 units, consisting of restaurants, package liquor stores, combination restaurant/package
liquor stores and a sports bar that we either own or have operational control over and partial ownership in; and (ii) franchises an additional
5 units, consisting of 2 restaurants (one of which we operate) and 3 combination restaurant/package liquor stores. The table below provides
information concerning the type (i.e. restaurant, sports bar, package liquor store or combination restaurant/package liquor store) and
ownership of the units (i.e. whether (i) we own 100% of the unit; (ii) the unit is owned by a limited partnership of which we are the
sole general partner and/or have invested in; or (iii) the unit is franchised by us), as of September 27, 2025 and as compared to September
28, 2024. With the exception of "The Whale's Rib," a restaurant we operate but do not own, and "Brendan's
Sports Pub" a restaurant/bar we own, all of the restaurants operate under our service marks "Flanigan's Seafood Bar
and Grill" or "Flanigan's" and all of the package liquor stores operate under our service marks "Big Daddy's
Liquors" or "Big Daddy's Wine & Liquors".

TYPES OF UNITS | September 27, 2025 | September 28, 2024
Company Owned:
Combination package liquor store and restaurant | 2 | 2
Restaurant only, including sports bar | 9 | 9
Package liquor store only | 9 | 9
Company Managed Restaurants Only:
Limited partnerships | 10 | 10
Franchise | 1 | 1
Unrelated Third Party | 1 | 1
Total Company Owned/Operated Units | 32 | 32
Franchised Units | 5 | 5 | (1)

Notes:

(1) | We operate a restaurant for one (1) franchisee. This unit is included in the table both as a franchised restaurant, as well as a restaurant operated by us.

History and Development of Our Business

We were incorporated in Florida
in 1959 and commenced operating as a chain of small cocktail lounges and package liquor stores throughout South Florida. By 1970, we
had established a chain of "Big Daddy's" lounges and package liquor stores between Vero Beach and Homestead, Florida.
From 1970 to 1979, we expanded our package liquor store and lounge operations throughout Florida and opened clubs in five other "Sun
Belt" states. In 1975, we discontinued most of our package store operations in Florida except in the South Florida areas of Miami-Dade,
Broward, Palm Beach and Monroe Counties. In 1982, we expanded our club operations into the Philadelphia, Pennsylvania area as general
partner of several limited partnerships we organized. In March 1985, we began franchising package liquor stores and lounges in the South
Florida area. (See Note 12 to the consolidated financial statements and the discussion of franchised units on pages 3 and 4).

During our fiscal year 1987,
we began renovating our lounges to provide full restaurant food service, and subsequently renovated and added food service to most of
our lounges. Food sales currently represent approximately 79.67% and bar sales approximately 20.33% of our total restaurant sales.

Our package liquor stores
emphasize high volume business by providing customers with a wide variety of brand name and private label merchandise at discount prices.
Our restaurants and our sports bar establishment offer alcoholic beverages and food service with abundant portions and reasonable prices,
served in a relaxed, friendly and casual atmosphere.

We conduct our operations
directly and through a number of limited partnerships and wholly owned subsidiaries, all of which are listed below. Our subsidiaries
and the limited partnerships, (except for the limited partnership, where we are not the general partner, which owns and operates our
franchised restaurant in Fort Lauderdale, Florida) are reported on a consolidated basis.

Entity | State Of Organization | Percentage Owned
Flanigan's Management Services, Inc. | Florida | 100
CIC Investors #13, Limited Partnership | Florida | 50
CIC Investors #25, Limited Partnership | Florida | —
CIC Investors #50, Limited Partnership | Florida | 29
CIC Investors #55, Limited Partnership | Florida | 54
CIC Investors #60, Limited Partnership | Florida | 46
CIC Investors #65, Limited Partnership | Florida | 33
CIC Investors #70, Limited Partnership | Florida | 41
CIC Investors #80, Limited Partnership | Florida | 32
CIC Investors #85, Limited Partnership | Florida | 7
CIC Investors #90, Limited Partnership | Florida | 11
Josar Investments, LLC | Florida | 100
Flanigan's Calusa Center, LLC | Florida | 100
Flanigan's Fish Company, LLC | Florida | 51

Package Liquor Store Operations

Our package liquor stores
emphasize high volume business by providing customers with a wide selection of brand name and private label liquors, beers and wines
while offering competitive pricing by meeting the published sales prices of our competitors. We provide sales training to our package
liquor store personnel. The stores are open for business seven days a week from 9:00-10:00 a.m. to 10:00-11:00 p.m., depending upon demand
and local law. Most of our units have "night windows" with extended evening hours.

Company-Owned Package
Liquor Stores . As of our fiscal year ended September 27, 2025, we own and operate eleven package liquor stores in the South Florida
area under the name "Big Daddy's Liquors" or "Big Daddy's Wine & Liquors", two of which are jointly
operated with restaurants we own.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2025-12-19_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2025-12-19_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2025-12-19_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 10-K_2025-12-19_item7_mdna.md, 10-K_2025-12-19_item1_business.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
