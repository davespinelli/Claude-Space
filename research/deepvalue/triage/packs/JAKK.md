# Triage pack — JAKK · JAKKS PACIFIC INC

_Generated 2026-09-04 23:07 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** JAKK · **Name:** JAKKS PACIFIC INC
- **CIK:** 0001009829
- **SIC:** 3944 — Games, Toys & Children's Vehicles (No Dolls & Bicycles)
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/JAKK

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** JAKKS PACIFIC INC
- **CIK:** 1,009,829 · **SIC:** 3944 (Games, Toys & Children's Vehicles (No Dolls & Bicycles)) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

> **EARNINGS QUALITY FLAG — one-off items likely.**
> net income exceeds revenue; net income more than 3x operating income.
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 24.05 |
| mktcap | $275.3M |
| ev | $215.7M |
| ev_ebit | 15.2x |
| fcf | -$1.1M |
| fcf_yield | -0.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 6.0% |
| net_debt | -$59.5M |
| net_debt_ebit | -4.2x |
| cash | $59.5M |
| ltd | $0.00 |
| equity | $247.9M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $113.3M |
| revenue_prior | $691.0M |
| rev_growth | -83.6% |
| rev_growth_note | n/a |
| eq_flag | net income exceeds revenue; net income more than 3x operating income |
| ebit | $14.2M |
| net_income | $9.9B |
| cfo | $8.5M |
| capex | $9.6M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 2.7% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 11,445,012 |
| shares_py | 11,146,831 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 52.5% |
| r6m | 18.5% |
| off_52w_high | -8.8% |
| adv20 | $2.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.19 |
| r_ev_ebit | 0.58 |
| r_roic | 0.56 |
| r_rev_growth | 0.00 |
| r_buyback | 0.28 |
| score | 0.37 |

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
| rank | 350 |

**Screen rationale:** debt data missing (net cash unverified); 12-1 momentum 52.5%; EARNINGS QUALITY: net income exceeds revenue; net income more than 3x operating income — one-off items likely


## 3. Share count trend

- Shares outstanding: **11,445,012** (CY2026Q2I) vs **11,146,831** prior year (CY2025Q2I)
- Change: **2.7%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-03-27** — Item 5.02 (Departure of Directors or Principal Officers;): Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 9; transaction rows: 27 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 9 |
| F | 4 |
| M | 14 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-02_item7_mdna.md)

_Extraction: started at 'Results of Operations'._

Results of Operations

The following table sets forth, for the periods
indicated, certain statement of operations data as a percentage of net sales. A discussion of the operating results for 2024 can be found
in our Annual Report on Form 10-K for the year ended December 31, 2024, as filed with the SEC on March 6, 2025, in Item 7. Management's
Discussion and Analysis of Financial Condition and Results of Operations – Results of Operations.

Year Ended December 31,
2025 | 2024
Net sales | 100.0 | % | 100.0 | %
Less: Cost of sales
Cost of goods | 49.7 | 52.3
Royalty expense | 16.2 | 15.5
Amortization of tools and molds | 1.7 | 1.4
Cost of sales | 67.6 | 69.2
Gross profit | 32.4 | 30.8
Direct selling expenses | 6.4 | 5.8
General and administrative expenses | 23.4 | 19.2
Depreciation and amortization | 0.1 | 0.1
Selling, general and administrative expenses | 29.9 | 25.1
Income from operations | 2.5 | 5.7
Other income (expense), net | 0.1 | 0.1
Loss on debt extinguishment | (0.1 | —
Interest income | 0.2 | 0.1
Interest expense | (0.1 | (0.2
Income before provision for income taxes | 2.6 | 5.7
Provision for income taxes | 0.9 | 0.8
Net income | 1.7 | 4.9
Net income attributable to JAKKS Pacific, Inc. | 1.7 | % | 4.9 | %
Net income attributable to common stockholders | 1.7 | % | 5.1 | %

The following table summarizes, for the periods
indicated, certain statement of operations data by segment (in thousands).

Year Ended December 31,
2025 | 2024
Net Sales
Toys/Consumer Products | 461,937 | 570,018
Costumes | 108,734 | 121,024
570,671 | 691,042
Cost of Sales
Toys/Consumer Products | 304,333 | 389,534
Costumes | 81,258 | 88,487
385,591 | 478,021
Gross Profit
Toys/Consumer Products | 157,604 | 180,484
Costumes | 27,476 | 32,537
185,080 | 213,021

Comparison of the Years Ended December 31, 2025 and 2024

Net Sales

Toys/Consumer Products. Net sales of our Toys/Consumer
Products segment were $461.9 million in 2025, compared to $570.0 million in 2024, representing a decrease of $108.1 million, or 19.0%.
The decrease in net sales was primarily due to lower sales North America, down 24.0%, while International sales grew 2.7%. The Dolls,
Role Play and Dress Up Division decreased 22.6% year over year, mainly due to limited theatrical releases and lower sales within the Disney
Princess and Style Collection businesses. Within the Action Play & Collectibles Division, down 15.6%, Sonic the Hedgehog 3 and the
Sonic/DC collaboration added incremental year over year sales, while lower Nintendo sales offset those gains. The Seasonal Division was
down 8.8% from 2024.

Costumes. Net sales of our Costumes segment
were $108.7 million in 2025, compared to $121.0 million in 2024, representing a decrease of $12.3 million, or 10.2%. The decrease in net
sales was primarily driven by US customers lowering their order levels based on tariffs. Despite the lower sales in the US, our International
sales grew in 2025 its highest level.

Cost of Sales

Toys/Consumer Products. Cost of sales of
our Toys/Consumer Products segment was $304.3 million, or 65.9% of related net sales in 2025 compared to $389.5 million, or 68.3% of related
net sales in 2024 representing a decrease of $85.2 million or 21.9%. Although royalty rates were higher year-over-year, the decrease in
the cost of sales percentage of net sales, year-over-year is due to lower inventory obsolescence costs.

Costumes. Cost of sales of our Costumes segment
was $81.3 million, or 74.8% of related net sales for 2025 compared to $88.5 million, or 73.1% of related net sales for 2024 representing
a decrease of $7.2 million, or 8.1%. The year-over-year decrease in dollars is directly attributable to lower volume. The increase in
percent of net sales is attributable higher royalty expense due to higher royalty guarantee shortfalls offset by improvements in product
cost of goods attributable to mix and design for improved margin.

Selling, General and Administrative Expenses

Selling, general and administrative expenses were
$170.9 million in 2025 and $173.3 million in 2024, constituting 29.9% and 25.1% of net sales, respectively. Selling, general and administrative
expenses decreased from the prior year by $2.4 million or 1.4% primarily driven by lower media costs and lower temporary labor costs.

Loss on Debt Extinguishment

In 2025, we recognized a loss on debt extinguishment
of $0.4 million in connection with the early termination our existing $67.5 million JPMorgan ABL revolving credit facility in connection
with entering into a new senior secured facility with BMO Bank, N.A.

Interest Income

Interest Income was $1.0 million for the year
ended December 31, 2025, as compared to $0.8 million in the prior year period. Interest income earned is primarily due to the Company's
money market investments.

Interest Expense

Interest expense was $0.5 million for the year
ended December 31, 2025, as compared to $1.1 million in the prior year period, both related to borrowings from our revolving credit facilities.

Provision for Income Taxes

During 2025, our income tax expense, which includes
federal, state and foreign income taxes and discrete items, was $4.9 million, or an effective tax rate of 33.1%. The 2025 tax expense
included a discrete tax benefit of $0.2 million primarily related to adjustments to uncertain tax positions and to return to provision
adjustments. Absent these discrete tax benefits, our effective tax rate for 2025 was 34.4%, primarily due to taxes on federal, state,
and foreign income.

During 2024, our income tax expense, which includes
federal, state and foreign income taxes and discrete items, was $5.5 million, or an effective tax rate of 13.9%. The 2024 tax expense
included a discrete tax benefit of $1.4 million primarily comprised of valuation allowance adjustments. Absent these discrete tax benefits,
our effective tax rate for 2024 was 17.4%, primarily due to taxes on federal, state, and foreign income.

We assess the available positive and negative evidence
to estimate if sufficient future taxable income will be generated to use the existing deferred tax assets by jurisdiction. Based on our
evaluation of all positive and negative evidence, as of December 31, 2025, a valuation allowance of $0.7 million has been recorded against
the deferred tax assets that more likely than not will not be realized. The net deferred tax asset change of $0.8 million consists of
the net deferred tax asset changes in the US and foreign jurisdictions, where we are in a cumulative income position.

Uncertainties that may have a significant impact on net sales
and income (loss) from operations

Significant outbreaks of contagious diseases,
and other adverse public health developments, could have a material impact on our business operations and operating results. The immediate
and lingering impact of the 2019 COVID-19 pandemic added additional risk and complexity to the Company's operations. In addition,
the history of smaller scale epidemics in Hong Kong/China (e.g., "bird flu") highlights an additional risk given that substantially
all of our product is sourced from China and our Hong Kong operation is foundational to our business model. We cannot quantify the extent
that any new outbreak might have on our sales, net income and cash flows, but it could be significant.

In the first quarter of 2022, Russia and Ukraine
engaged in an armed conflict that continues. We cannot predict at this time if the conflict will spread to other countries. Accordingly,
we cannot quantify at this time if, or the extent, this conflict will adversely impact our business operations.

The U.S. taking unilateral action to impose tariffs
on products imported from China and adopting an approach to deploy tariffs with no advance notice or feedback mechanism has created across
markets has created uncertainty about our ability to source products with a cost structure consistent with our recent history. It also
increased the possibility that markets outside the U.S. could institute retaliatory tariffs that would ultimately increase the cost of
our doing business in those markets where we import product. In addition, our customer base has faced increased costs in importing our
product from Hong Kong into their home markets. In the event our customers choose to raise consumer prices to offset these costs, negative
consumer reaction could substantially reduce unit demand for our product line, and by extension lower sales. Lower sales could negatively
impact our profitability and cash flows.

Quarterly Fluctuations and Seasonality

We have experienced significant quarterly fluctuations
in operating results and anticipate these fluctuations in the future. The operating results for any quarter are not necessarily indicative
of results for any future period. Our first quarter is typically expected to be the least profitable as a result of lower net sales but
substantially similar fixed operating expenses. This is consistent with the performance of many companies in the toy industry.

The following table presents our unaudited quarterly
results for the years indicated. The seasonality of our business is reflected in this quarterly presentation.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-03-02_item1_business.md)

Item 1. Business

In this report, "JAKKS," the "Company,"
"we," "us" and "our" refer to JAKKS Pacific, Inc. and its subsidiaries.

Company Overview

We are a leading multi-product line, multi-brand
toy company that designs, produces, markets, sells and distributes toys and related kid-targeted consumer products, inclusive of kids
indoor and outdoor furniture, costumes and various product lines in the sporting goods and home furnishings space. We focus our business
on acquiring or licensing well-recognized intellectual property ("IP"), trademarks and/or brand names, most with long product
histories ("evergreen brands"). We seek to acquire/license these evergreen brands because we believe they are less subject
to market fads or trends. We also develop proprietary products marketed under our own trademarks and brand names and have historically
acquired complementary businesses to further grow our portfolio. For accounting purposes, our products have been divided into two segments:
(i) Toys/Consumer Products and (ii) Costumes. Segment information with respect to revenues, assets and profits or losses attributable
to each segment is contained in Note 3 to the audited consolidated financial statements contained below in Item 8. Our products include:

● | Action figures and accessories, including licensed characters based on the Nintendo®, Sonic the Hedgehog®, and The Simpsons® franchises and our own proprietary brands including Creepy Crawlers®;
● | Toy vehicles, including Xtreme Power Dozer®, Xtreme Power Dump Truck®, XPV®, Road Champs®, Fly Wheels® and AirTitans® inflatable remote-control dinosaur;
● | Dolls and accessories, including small dolls, large dolls, fashion dolls and baby dolls based on licenses, including Disney Darlings, Disney Encanto®, Disney Moana® 2, Disney ILY 4EVER®, Disney Frozen®, Disney Princess® and Minnie Mouse®, and infant and pre-school toys based on TV shows like PBS's Daniel Tiger's Neighborhood® as well as in-house brands such as Perfectly Cute®, Charming™, and KidTopia™;
● | Private label products developed exclusively for certain retail customers in various product categories;
● | Foot-to-floor ride-on products, including those based on BBC's Bluey®, Fisher-Price®, Nickelodeon®, and Hasbro® licenses and inflatable play environments, tents and wagons;
● | Role play, dress-up, pretend play and novelty products for boys and girls based on well-known brands and entertainment properties such as Disney Frozen® , Black & Decker® , Disney Princess®, and Disney Encanto®, as well as those based on our own proprietary brands;
● | Indoor and outdoor kids' furniture, activity trays and tables and room décor, seasonal and outdoor products, including those based on Disney® characters, Nickelodeon® and Hasbro® licenses;
● | Halloween and everyday costumes for children and in some cases teens and adults based on licensed and proprietary non-licensed brands, including Super Mario Bros.®, Microsoft's Halo®, Disney-Pixar Toy Story®, Harry Potter®, Minions®, Sesame Street®, Power Rangers®¸ Pokemon®, Hasbro® brands, Universal's Wicked® and Disney Frozen®, Disney Princess® and related Halloween accessories;
● | Outdoor activity toys including ReDo Skateboard Co.® and junior sports toys including Sky Ball® hyper-charged balls, SportsZone® sport sets and Wave Hoop® toy hoops marketed under our Maui® brand; and
● | Board games under the brand JAKKS Wild Games®, including Temple Raider®, K.O. Corral® and Galactic JAXX™.

We continually review the marketplace to identify
and evaluate popular and evergreen brands and product categories that we believe have the potential for growth. We endeavor to generate
growth within these lines by:

● | creating innovative products under our established licenses and brand names;

● | adding new items to the branded product lines that we expect will enjoy greater popularity;

● | infusing innovation and technology when appropriate to make products more appealing to today's kids; and

● | expanding our international product offering either sold directly to retailers or via third-party distributors.

Our Business Strategy

In addition to developing our own proprietary brands,
properties and marks, licensing popular IP enables us to use these high-profile marks at a lower cost than we would incur if we purchased
these marks or funded the development of comparable marks on our own. Beyond the investment profile, we have an appreciation of the challenges
and expertise required to break through the noise in a world filled with high-budget, content-centric consumer choices either based on
well-known pre-existing IP or the even higher hurdle to launch new IP in the current marketplace. By licensing IP and trademarks from
world-class brand owners and content creators, we have potential access to a far greater range of marks than would be available for purchase.
Licensors ultimately are responsible for the franchise management of their IP, and we, by extension, leverage their related investment
in content and promotion, which we hope in turn will create a robust market for our related toy, consumer products and costume product
lines. Licensors often also invest resources in engaging our largest customers directly to keep them aware of new initiatives and content
to facilitate our sell-in of product. It also helps to credibly assure licensors that we will prioritize their brands, properties and
IP rather than explicitly competing with them with a broad range of self-developed content-led offerings. We also license technology developed
by unaffiliated inventors and product developers to enhance the design, innovation and functionality of our products.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-03-02_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-02_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-03-02_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-02_item7_mdna.md, 10-K_2026-03-02_item1_business.md

**Missing:** 8-K earnings press release exhibit, transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
