# Triage pack — SPWR · SunPower Inc.

_Generated 2026-09-05 03:09 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** SPWR · **Name:** SunPower Inc.
- **CIK:** 0001838987
- **SIC:** 1700 — Construction - Special Trade Contractors
- **Fiscal year end (MM-DD):** 12-29
- **Exchange:** Nasdaq, Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/SPWR

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** SunPower Inc.
- **CIK:** 1,838,987 · **SIC:** 1700 (Construction - Special Trade Contractors) · **Exchange:** Nasdaq,Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebt

> **EARNINGS QUALITY FLAG — one-off items likely.**
> revenue growth above 50% alongside share count growth above 15% (bought, not organic).
> Reported net income is not supported by the operating engine that is supposed to produce it (typical causes: gains on sale, legal settlements, deferred-tax valuation-allowance releases, bargain-purchase gains). Reconcile net income to operating income in the earnings release (section 7) before treating any earnings-based metric here as repeatable.

**Valuation**

| metric | value |
|---|---|
| price | 0.40 |
| mktcap | $50.9M |
| ev | $226.6M |
| ev_ebit | n/a |
| fcf | -$15.3M |
| fcf_yield | -30.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -14.2% |
| net_debt | $175.7M |
| net_debt_ebit | n/a |
| cash | $4.1M |
| ltd | $179.8M |
| equity | -$26.3M |
| ltd_tag | LongTermDebt |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $300.0M |
| revenue_prior | $108.7M |
| rev_growth | 175.9% |
| rev_growth_note | share count +52.4% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | revenue growth above 50% alongside share count growth above 15% (bought, not organic) |
| ebit | -$26.9M |
| net_income | -$45.4M |
| cfo | -$15.3M |
| capex | n/a |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 52.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 126,652,769 |
| shares_py | 83,108,708 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | -82.0% |
| r6m | -68.8% |
| off_52w_high | -80.9% |
| adv20 | $7.0M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.03 |
| r_ev_ebit | 0.00 |
| r_roic | 0.08 |
| r_rev_growth | 0.99 |
| r_buyback | 0.04 |
| score | 0.13 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2026Q2I |
| shares_period | CY2026Q1I |
| shares_py_period | CY2025Q2I |
| capex_missing | True |
| ltd_missing | False |

**Other screen columns**

| metric | value |
|---|---|
| rank | 478 |

**Screen rationale:** revenue +175.9% BUT share count +52.4% yoy — growth may be acquisition/issuance-driven, not organic; EARNINGS QUALITY: revenue growth above 50% alongside share count growth above 15% (bought, not organic) — one-off items likely; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **126,652,769** (CY2026Q1I) vs **83,108,708** prior year (CY2025Q2I)
- Change: **52.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +52.4% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-09-03** — Item 1.01 (Entry into a Material Definitive Agreement): entered into securities purchase agreements (the " Purchase Agreements ") with various accredited investors (the
- **2026-08-28** — Item 1.01 (Entry into a Material Definitive Agreement): entered into a simple agreement for future equity (the " SAFE ") with the Rodgers Massey Revocable Living Trust (the
- **2026-08-10** — Item 1.01 (Entry into a Material Definitive Agreement): entered into a simple agreement for future equity (the "SAFE") with an institutional investor in connection with its investment
- **2026-07-22** — Item 1.01 (Entry into a Material Definitive Agreement): entered into OTC Equity Prepaid Forward Transaction Settlement Agreements (the " FPA Settlement Agreements ") with funds

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 7,953,086 sh / $0 vs sells 20,000 sh / $40,800 -> net $-40,800 (SELLING).
Distinct insiders buying (code P): 2. Largest buy: Rodgers Thurman J bought 7,226,186 sh @ $0.00 ($0) on 2026-07-01.

Form 4 filings parsed: 6; transaction rows: 11 (open-market buys 3, sales 2).

| code | rows |
|---|---|
| A | 1 |
| P | 5 |
| S | 2 |
| X | 3 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-28_2-02-results.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit; skipped 8 forward-looking-statement block(s)._

## EX-99.1 - PRESS RELEASE DATED JULY 28, 2026 (ea029940201ex99-1.htm)

EX-99.1
ea029940201ex99-1.htm
PRESS RELEASE DATED JULY 28, 2026

Exhibit 99.1

SunPower
Reports Q2'26 Results

Q3'26
Fcst: $10 Million Operating Income Improvement

OREM,
Utah (July 28, 2026) – SunPower Inc. (herein "SunPower," the "Company," or Nasdaq: "SPWR"),
a solar technology, services, and installation company, will present its Q2'26 results via webcast today, Tuesday, July 28, at
1:00pm ET. Register for the webcast here or by visiting our Events page: https://investors.sunpower.com/news-events/events .

Fellow
Shareholders:

The
preliminary Q2'26 quarterly report of key financial parameters is shown below, compared to the Q1'26 results.

SunPower
Q2'26 Revenue & Operating Income Statement​ 1

GAAP​ 2 | NON-GAAP 3
($1000s) | Q2 2026 | Q1 2026 | Q2 2026 | Q1 2026
Revenue | 55,956 | 72,793 | 55,956 | a | 72,793
Gross Profit | 26,159 | 45,162 | ​ 4 | 27,598 | 46,883
Gross Margin (%) | 47 | % | 62 | % | 49 | % | 64 | %
Operating Expense (Opex) | 44,273 | 64,357 | ​ 4 | 40,071 | c | 59,748
Opex (less commission) | 28,332 | 35,793 | 24,130 | d | 31,184
Stock Comp, Intangibles, M&A​ 3 | 5,642 | 6,331 | 0 | 0
Operating Income (loss) | (18,115 | (19,196 | (12,473 | b | (12,865
Cash Balance​ 5 | 4,024 | 9,488 | 4,024 | e | 9,488

Our
Q2'26 revenue was $56.0 million, $16.8 million down from the $72.8 million reported in Q1'26. That revenue decline (a, above)
flowed through the P&L to produce a Q2'26 non-GAAP operating loss of $12.5 million (b), actually slightly better than the Q1'26
loss. The good news is that while the revenue dropped $16.8 million, the operating expense dropped $19.7 million (c), of which $7.1 million
was a reduction in fixed cost (d) that will help drive recovery in subsequent quarters. Finally, our ending Q3'26 cash balance
was $4.0 million (e), below our minimum cash target of $10 million, because we chose to avoid the dilution that would have been caused
by raising money at a low share price.

1 | Non-GAAP Operating income is based on preliminary, unaudited non-GAAP results posted on the IR section of our website under "News" [us.sunpower.com].

2 | Our 2026 GAAP financial statements are found in the 10Q filing posted on our website.

3 | Our non-GAAP financials are used to run the company. Our policy allows for only three GAAP/non-GAAP differences: a) no non-cash amortization of intangibles, b) no employee stock compensation charges and c) no one-time restructuring M&A gains or losses.

4 | The filed 10Q report transfers $475,000 from opex to fixed COGS with no Opinc effect.

5 | Cash balances exclude restricted cash and include issued but uncashed checks.

1 of 9

SunPower
CEO, T.J. Rodgers, commented, "The Q2'26 $16.8 million revenue drop was factors worse than any result New SunPower has ever
posted. And was caused primarily by our SunPower Direct Division. The relevant questions are why did we fail to make our numbers; what
will we change to prevent the problem in the future; and when will we return to profitability?

Rodgers
continued, "The Direct Division revenue miss was caused in turn by a pile-up of about 1,105 jobs delayed at the end of the line
in Q2'26. The principle is simple: double the inventory of any operation and for a given effort, the inventory will move half as
fast. These delayed jobs have signed contracts, are in operation now and will clear the line this quarter, releasing about $15.3 million
in revenue (which I expected to ship in Q2, hence I made no pre-announcement). In short form, we had the orders, the designs, and the
financing, but chose not to submit the jobs for funding due to violations of our quality specifications for funding package submissions,
such as blurry photographs or a missing utility bill or – worse – re-design and re-permit. Fortunately, our Quality group
held its ground and did not allow any defective jobs to be submitted for funding. Our strong quality policy is why SunPower's New
Homes division has not suffered even one rejection of its financing submissions for over 70 weeks by its financial partner, Palmetto
LightReach – a feat that earned SunPower the LightReach Platinum Partner Award in 2026.

Rodgers
concluded, "The Q2'26 quality problems were self-induced by the SunPower Direct management team that knowingly and surreptitiously
violated our quality specifications. After that discovery, I replaced the top two and one-half tiers of that management team from Ambia,
a startup we acquired, and started over with SunPower veterans Kapil Rai and Steve Erickson. The benefit of eliminating that management
team will become visible in Q3."

Q3'26
Outlook

Despite
a poor Q2'26, we remain optimistic in our outlook for Q3'26. We have just enjoyed our three best quarters in bookings ever.
We expect to grow Q3'26 revenue to $75-plus million and reduce our operating loss by 90% from ($12.5 million) in Q2'26 to
less than ($1.0 million) in Q3'26.

2 of 9

Total
Bookings

Signed
Contract + Design Complete + Funding Approved

$13.0
Million in Permanent Cost Reductions

The
actions to stem Q1'26 losses – a RIF, the implementation of a four-day workweek (to minimize the RIF), and structured cost-cutting
– were made in May and reduced our quarterly fixed operating expenses by about $7.1 million. In Q3'26, we will further reduce
our fixed expenses by another $5.9 million with more cost cutting and "right-sizing" the combined New Homes-Cobalt management
teams.

Conclusion

Given
the structural changes mandated by two consecutive tough quarters, we will recover strongly in both revenue and profit in Q3'26.
Cost cutting to survive on thin margins can only go so far. With the state-of-the-art Monolith and Monolith II panels, as well as the
high tech, high margin installations by our New Homes/Cobalt Division, we will move into the premium segment of the solar market defined
by sustainable technology advantages and bring premium pricing to a very lean installation company.

3 of 9

Recent
Events of Note

( Press
Releases on Our Website here)

● | SunPower Appoints Tom Kowalczuk CFO (July 7, 2026). He has a CPA and a Chicago MBA.

Cobalt
Power Systems Completes 1.2MW Commercial Solar & Storage Project at

Santa Clara University (May 26, 2026)

SunPower's
Cobalt Power Systems and Wunder Power Complete Advanced Solar

System at San Francisco's Waterfront Plaza (June 15, 2026)

4 of 9

San
Francisco Waterfront Plaza: Earthquake Tolerant System

"Floats"
on Tensile Concrete Roof

SunPower
Achieves High NPS Score from Starbucks (May 29, 2026)

One of 26 "Greener Stores" Program

5 of 9

SunPower
Completes Megawatt Millenium Solar Project,

Receives
High Customer NPS Score (July 16, 2026)

Creates
A Megawatt of Power From Carport Roofs

· | SunPower receives high net promoter scores (NPS)

○ | SunPower Achieves High NPS Score from Starbucks (May 29, 2026)

○ | And from Millenium (July 16, 2026)

○ | NPS scores improving in general

SunPower
Aggregate New Promoter Score (NPS)

6 of 9

About
SunPower

SunPower
Inc. (Nasdaq: SPWR) is a leading residential solar services provider in North America. The Company's digital platform and installation
services support energy needs for customers wishing to make the transition to a more energy-efficient lifestyle. For more information
visit www.sunpower.com.

Sioban
Hickie

VP
Investor Relations

IR@sunpower.com

(801)
515-8727

8 of 9

SUNPOWER
INC.

RECONCILIATION
OF NON-GAAP FINANCIAL MEASURES (PRELIMINARY)

(In
Thousands)

As Reported Unaudited
Note | Q1 2026 | Q2 2026
GAAP operating Income(loss) from continuing operations | (19,196 | (18,115
Depreciation and amortization | A | 2,869 | 3,224
Stock based compensation | B | 1,605 | 1,705
Restructuring charges | C | 1,857 | 712
Total of Non-GAAP adjustments | 6,331 | 5,642
Non-GAAP net Income (loss) | (12,865 | (12,473

Notes:

( A) | Depreciation and amortization: Depreciation and amortization related to capital expenditures.

( B ) | Stock-based compensation: Stock-based compensation relates to our equity incentive awards and for services paid in warrants. Stock-based compensation is a non-cash expense.

( C) | Acquisition Costs: Costs primarily related to acquisition, headcount reductions (i.e. severence), legal, professional services (i.e. historical carveout audits) and due diligence.

Source:
SunPower Inc.

9 of 9

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-04-14_item7_mdna.md)

_Extraction: started at the Overview heading._

Overview

SunPower Inc. is the rebranded name of Complete Solaria, Inc. The rebranding
was effective April 22, 2025 and our legal name change became effective on October 16, 2025. We are headquartered in Orem, Utah.

Our
Company was originally incorporated in Delaware as Complete Solar, Inc. on February 22, 2010. In 2022, Complete Solar, Inc. implemented
a holding company reorganization creating Complete Solar Holding Corporation ("Complete Solar Holding") as successor to Complete
Solar, Inc. Complete Solar Holding then acquired The Solaria Corporation in November 2022 and we changed our name to Complete Solaria,
Inc. We created a technology platform to offer clean energy products to homeowners by enabling a national network of sales partners and
build partners. Our sales partners generate solar installation contracts with homeowners on our behalf. To facilitate this process, we
provide the software tools, sales support and brand identity to our sales partners, making them competitive with national providers.
This turnkey solution makes it easy for anyone to sell solar.

On
July 18, 2023, we consummated a series of merger transactions contemplated by an Amended and Restated Business Combination Agreement
entered into with wholly-owned subsidiaries of Freedom Acquisition I Corp. ("FACT") ("Mergers"), equating to
a reverse recapitalization for accounting purposes. Under the reverse recapitalization of accounting, FACT was treated as the acquired
company for financial statement reporting purposes. This determination was based on us having a majority of the voting power of the post-combination
company, our senior management comprising substantially all of the senior management of the post-combination company, and our operations
comprising the ongoing operations of the post-combination company. Accordingly, for accounting purposes, the Mergers were treated as
the equivalent of a capital transaction in which we issued stock for the net assets of FACT. The net assets of FACT were stated at historical
cost, with no goodwill or other intangible assets recorded.

In October 2023, we completed the sale of our solar panel business.
On September 30, 2024, we acquired certain assets relating to the Blue Raven Solar business, New Homes business and Non-Installing Dealer
network (collectively the "SunPower Businesses") from the SunPower Debtors, the successor entity in bankruptcy to SunPower
Corporation and its direct and indirect subsidiaries. The acquired SunPower Businesses sell products to residential customers and home
builders through a network of installing and non-installing dealers and resellers and internal sales team. On September 24, 2025, we completed
the acquisition of Sunder Energy, LLC, ("Sunder"), which contracts with customers for solar installations performed by third-party
installation companies through a dealer network. On November 21, 2025, we completed the acquisition of Ambia Energy LLC, ("Ambia")
a residential solar energy system installer.

We
fulfill our customer contracts by using in-house installation experts and by engaging with local construction specialists. We manage
the customer experience and complete all pre-construction activities prior to delivering build-ready projects including hardware, engineering
plans, and building permits to our builder partners. We manage and coordinate this process through our proprietary software system.

There
is substantial doubt about our ability to continue as a going concern within one year after the date that the consolidated financial
statements are issued. The consolidated financial statements included in this Annual Report on Form 10-K have been prepared assuming
that we will continue to operate as a going concern, which contemplates the realization of assets and settlement of liabilities in the
normal course of business. They do not include any adjustments to reflect the possible future effects on the recoverability and classification
of assets or the amounts and classifications of liabilities that may result from uncertainty related to its ability to continue as a
going concern.

Growth
Strategy and Outlook

Our
growth strategy contains the following elements:

● | Increase revenue by expanding installation capacity and developing new geographic markets – We continue to expand our network of partners who will install systems resulting from sales generated by our sales partners. By leveraging this network of skilled builders in addition to our in-house installation experts, we aim to increase our installation capacity in our traditional markets and expand our offering into new geographies throughout the U.S. This will enable greater sales growth in existing markets and create new revenue in expansion markets.

● | Increase revenue and margin by engaging national-scale sales partners – We aim to offer a turnkey solar solution to prospective sales partners with a national footprint. These include electric vehicle manufacturers, national home security providers, and real estate brokerages. We expect to create a consistent offering with a single execution process for such sales partners throughout their geographic territories. These national accounts have unique customer relationships that we believe will facilitate meaningful sales opportunities and low cost of acquisition to both increase revenue and improve margin.

● | Increase revenue and margin by executing on a battery storage opportunity – We have an opportunity to increase our revenue and margin in the battery space through our partnership with Enphase. By providing homeowners with an option to include battery storage as part of their solar system install, we believe there will be a greater need for battery storage as the demand and costs of energy will increase.

The
Mergers

We
entered into an Amended and Restated Business Combination Agreement with FACT, First Merger Sub, Second Merger Sub, and Solaria on October
3, 2022. The Merger was consummated on July 18, 2023. Upon the terms and subject to the conditions of the Merger, (i) First Merger Sub
merged with and into Complete Solaria with Complete Solaria surviving as a wholly-owned subsidiary of FACT (the " First Merger "),
(ii) immediately thereafter and as part of the same overall transaction, Complete Solaria merged with and into Second Merger Sub, with
Second Merger Sub surviving as a wholly-owned subsidiary of FACT (the " Second Merger "), and FACT changed its name
to "Complete Solaria, Inc." and Second Merger Sub changed its name to "CS, LLC" and (iii) immediately after the
consummation of the Second Merger and as part of the same overall transaction, Solaria merged with and into a newly formed Delaware limited
liability company and wholly-owned subsidiary of FACT and changed its name to "The SolarCA LLC" (" Third Merger Sub "),
with Third Merger Sub surviving as a wholly-owned subsidiary of FACT (the "Additional Merger", and together with the First
Merger and the Second Merger, the " Mergers ").

The
Mergers between Complete Solaria and FACT were accounted for as a reverse recapitalization. Under this method of accounting, FACT was
treated as the acquired company for financial statement reporting purposes. This determination was primarily based on the Company having
a majority of the voting power of the post-combination company, the Company's senior management comprising substantially all of
the senior management of the post-combination company, and the Company's operations comprising the ongoing operations of the post-combination
company. Accordingly, for accounting purposes, the Mergers were treated as the equivalent of a capital transaction in which Complete
Solaria issued stock for the net assets of FACT. The net assets of FACT were stated at historical cost, with no goodwill or other intangible
assets recorded.

Disposal
Transaction

In October 2023, we completed
the divestiture of our solar panel business to Maxeon (" Divestiture "), pursuant to the terms of the Disposal Agreement.
Under the terms of the Disposal Agreement, Maxeon agreed to acquire certain assets and employees of Complete Solaria, for an aggregate
purchase price of approximately $11.0 million consisting of 1,100,000 shares of Maxeon ordinary shares. We determined that the criteria
were met for discontinued operations classification as the divestiture represented a strategic shift in our business. In connection with
the Divestiture, we recognized a loss from discontinued operations of $1.1 million, $2.0 million and $173.4 million in the fiscal years
ended December 28, 2025, December 29, 2024 and December 31, 2023, respectively. We also sold all the Maxeon shares in the year ended
December 31, 2023, and recorded a $4.2 million loss on the sale of these shares in our consolidated statements of operations and comprehensive
loss.

Acquisitions

Certain
Assets of SunPower Debtors

On September 30, 2024, we acquired the SunPower Businesses for consideration
of $54.5 million which we financed through the issuance of $66.8 million of 7.0% senior unsecured convertible notes in September 2024.
These notes mature on July 1, 2029 and are convertible into shares of the Company's common stock at the option of the holder at
a current conversion rate of $1.71 per share. The SunPower Businesses operated as a solar technology and energy services provider that
offered fully integrated solar, storage, and home energy solutions to customers in the United States through an array of hardware, software,
and "Smart Energy" solutions. This transaction was accounted for as a business combination under Accounting Standards Codification
("ASC") 805, Business Combinations .

Sunder
Energy LLC

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-04-14_item1_business.md)

PART
I

ITEM
1. BUSINESS

Our
Mission

Our
mission is to deliver energy-efficient solutions to homeowners and small to medium-sized businesses that allow them to lower their energy
bills while reducing their carbon footprint. SunPower Inc. or SunPower, has created a unique, end-to-end offering that delivers a best-in-class
customer experience with a robust technology platform, financing solutions, and high-performance solar equipment.

Business
Overview

SunPower
Inc. (the "Company") is the rebranded name of Complete Solaria, Inc. The rebranding was effective April 22, 2025 and became
legally effective on October 16, 2025. We are headquartered in Orem, Utah.

Complete
Solaria, Inc. ("Complete Solaria") was formed in November 2022 through the merger of Complete Solar Holding Corporation,
a Delaware corporation ("Complete Solar"), and The Solaria Corporation, a Delaware corporation (such entity, "Solaria,"
and such transaction, the "Business Combination"). Complete Solaria created a technology platform to offer clean energy products
to homeowners by enabling a national network of sales partners and build partners. Our sales partners generate solar installation contracts
with homeowners on our behalf. To facilitate this process, we provide the software tools, sales support and brand identity to our sales
partners, making them competitive with national providers. We fulfill our customer contracts by engaging with local construction specialists
and using our in-house installation experts. We manage the customer experience and complete all pre-construction activities prior to
delivering build-ready projects including hardware, engineering plans, and building permits to our builder partners and in-house teams.

In
October 2023, we sold the solar panel assets of The Solaria Corporation, including intellectual property and customer contracts to Maxeon
Solar Technologies, Ltd. ("Maxeon") pursuant to the terms of an asset purchase agreement (the "Disposal Agreement").
Under the terms of the Disposal Agreement, Maxeon agreed to acquire certain assets and employees of Complete Solaria for an aggregate
purchase price of approximately $11.0 million consisting of 1,100,000 shares of Maxeon ordinary shares.

We
expect to continue making acquisitions and entering into strategic partnerships as part of our long-term business strategy. For example,
on September 24, 2025, we completed the purchase of all the membership interests of Sunder Energy, LLC ("Sunder"). Sunder
provides a third-party solar energy sales force to initiate and execute contracts with customers throughout the United States. Sunder's
sales force works with solar installation companies in which Sunder acts as the agent for each transaction entered. Sunder earns revenue
based on residential solar installation contracts for residential homeowners that are sold to installation companies in accordance with
its contracts with those installation companies. Upon entering into a sales contract, the requisite performance obligation of Sunder
is to assist the installation companies in the progress of the installation and obtain permission to operate. On November 21, 2025, we
completed the purchase of all the membership interest of Ambia Energy, LLC ("Ambia"). Ambia is a residential solar energy
system installer which operates in various markets throughout the United States. Ambia generates revenue from selling and installing
solar energy systems or orchestrating the sale of a solar energy system which will be installed by a third party. On January 30, 2026,
we completed the purchase of all of the equity interests of Cobalt Power Systems, Inc. ("Cobalt"). Cobalt is an installer
of residential and commercial solar energy systems in the San Francisco Bay area. Cobalt generates revenue from the design and installation
of solar power systems.

On
August 5, 2024, we entered into an Asset Purchase Agreement (the "APA") among us and SunPower Corporation and its direct
and indirect subsidiaries (collectively, the "SunPower Debtors") providing for the sale and purchase of certain assets relating
to the Blue Raven Solar business, New Homes Business and Non-Installing Dealer network previously operated by the SunPower Debtors (the
"Acquired SunPower Assets"). The APA was entered into in connection with a voluntary petition filed by SunPower under Chapter
11 of the United States Code, 11 U.S.C.§§ 101-1532. The sale was approved on September 23, 2024, by the United States Bankruptcy
Court for the District of Delaware. We completed the acquisition of the Acquired SunPower Assets effective September 30, 2024. The assets
and businesses acquired by us under the APA are referred to as the "SunPower Businesses." As part of the acquisition the
Company acquired Albatross, an order-to-management proprietary software to manage our orders, fulfillment and customer service all in
one central location.

The
acquisitions of Sunder, Ambia, Cobalt and SunPower Businesses are collectively referred to herein as "Acquisitions".

Revenue
Model

We
offer solar system sales and installation to residential homeowners and the new home builders' communities. The Acquisitions will
allow us to accelerate our revenue growth and expand our footprint to deliver solar system sales into regions where we might have not
previously done business.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-04-14_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-04-14_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-04-14_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-28_2-02-results.md, 10-K_2026-04-14_item7_mdna.md, 10-K_2026-04-14_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
