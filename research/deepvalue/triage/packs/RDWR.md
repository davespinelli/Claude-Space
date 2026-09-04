# Triage pack — RDWR · RADWARE LTD

_Generated 2026-09-04 21:11 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** RDWR · **Name:** RADWARE LTD
- **CIK:** 0001094366
- **SIC:** 7389 — Services-Business Services, NEC
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/RDWR

**Fetcher warnings for this ticker:** 10-K 2026-03-31: heading split missed Item 1 - Business, Item 1A - Risk Factors; no 10-Q in recent filings; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** RADWARE LTD
- **CIK:** 1,094,366 · **SIC:** 7389 (Services-Business Services, NEC) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 28.53 |
| mktcap | $1.2B |
| ev | $1.1B |
| ev_ebit | 98.7x |
| fcf | $41.6M |
| fcf_yield | 3.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 3.7% |
| net_debt | -$105.1M |
| net_debt_ebit | -9.2x |
| cash | $105.1M |
| ltd | $0.00 |
| equity | $349.4M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $301.9M |
| revenue_prior | $274.9M |
| rev_growth | 9.8% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $11.4M |
| net_income | $20.3M |
| cfo | $50.1M |
| capex | $8.5M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 1.4% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 43,145,971 |
| shares_py | 42,554,602 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 14.9% |
| r6m | 14.5% |
| off_52w_high | -11.2% |
| adv20 | $5.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.40 |
| r_ev_ebit | 0.06 |
| r_roic | 0.44 |
| r_rev_growth | 0.65 |
| r_buyback | 0.40 |
| score | 0.44 |

**Data provenance and flags**

| metric | value |
|---|---|
| revenue_period | CY2025 |
| ebit_period | CY2025 |
| equity_period | CY2025Q4I |
| shares_period | CY2025Q4I |
| shares_py_period | CY2024Q4I |
| capex_missing | False |
| ltd_missing | True |

**Other screen columns**

| metric | value |
|---|---|
| rank | 297 |

**Screen rationale:** debt data missing (net cash unverified); 12-1 momentum 14.9%


## 3. Share count trend

- Shares outstanding: **43,145,971** (CY2025Q4I) vs **42,554,602** prior year (CY2024Q4I)
- Change: **1.4%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No 8-K filings fetched for this ticker._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 2,000 sh / $50,420 vs sells 18,736 sh / $559,782 -> net $-509,362 (SELLING).
Distinct insiders buying (code P): 1. Largest buy: Avidan Guy bought 2,000 sh @ $25.21 ($50,420) on 2026-07-31.

Form 4 filings parsed: 12; transaction rows: 13 (open-market buys 1, sales 5).

| code | rows |
|---|---|
| A | 6 |
| P | 1 |
| S | 5 |
| W | 1 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release

_Not available: no 8-K with a readable release exhibit was fetched. Current-quarter results are unknown from this pack._

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-03-31_item7_mdna.md)

_Extraction: started at the Overview heading._

Overview

We have in the past entered into, and in the future we may enter
into, transactions with related parties, such as our directors and senior management or their respective affiliates, which transactions
are generally subject to the prior approval of our audit or compensation committee and board of directors.

Transactions with Rad-Bynet Group

We have entered into a number of agreements with certain companies
that form part of the RAD-Bynet Group, of which either the heirs of the late Yehuda Zisapel, the heirs of his late brother, Zohar Zisapel,
and Nava Zisapel (or all of them together) were co-founders, and are directors and/or shareholders. Roy Zisapel also serves as a director
of RAD Data Communications Ltd., Bynet Electronics Ltd., AB-NET Communications Ltd. (and its wholly owned subsidiary, ABNET Cloud Services
Ltd.), Bynet Data Centers Ltd., Bynet Data Communications Ltd. (and its wholly owned subsidiary RAD Negev Ltd.), RADWIN Ltd., Packetlight
Networks Ltd. and other companies in the RAD-Bynet Group.

Under these agreements, we lease property and purchase certain
products and services from certain member entities of the RAD-Bynet Group. In addition, in February 2022, we acquired the technology and
operations of SecurityDAM (now called DC Protection Ltd.), to which we sometimes refer as the SecurityDAM Acquisition.

The RAD-Bynet Group consists of manufacturers of communications
solutions comprised of hardware and/or software and communications solution providers, distributors and integrators as well as service
providers. The RAD-Bynet Group includes companies dealing in advanced communication technology, networks, and integration. Companies within
the RAD-Bynet Group provide a variety of solutions and services to their customers, including engineering, purchasing and sub-contracting,
production and final testing, planning and control, and support for end users. The RAD-Bynet Group also includes a few companies that
provide services that support the activities of the other RAD-Bynet Group members, such as real estate leasing and administrative services.
Some of the products of members of the RAD-Bynet Group are complementary to, and may be used in connection with, our products and services.
Each company in the RAD-Bynet Group is independent from the others. The ownership and Board of Directors structure of each RAD-Bynet Group
member is different and certain of the RAD-Bynet Group members are publicly traded companies. See Item 4.C "Organizational Structure"
for additional details about the group.

Lease of Property

We lease the office space for our headquarters and principal R&D,
administrative, finance and marketing and sales operations from private companies within the RAD-Bynet Group that are owned by the heirs
of the late Zohar Zisapel, Nava Zisapel, and the heirs of the late Yehuda Zisapel:

• | One lease is a five-story building in Tel Aviv, Israel, consisting of approximately 40,000 square feet, plus storage and parking space. This lease expires in June 2030. The annual rent amounts to approximately $705,000.

• | A second lease consists of five floors in the Or Tower in Tel Aviv, Israel with approximately 68,000 square feet, plus parking spaces. This lease expires in June 2030. The annual rent amounts to approximately $2,084,000. In this annual report, we sometimes refer to this lease as well as the lease described above as the "Lease Agreements for the Company's Headquarters."

• | We also lease approximately 3,600 square feet of space in Jerusalem, Israel, for development facilities from an affiliated company owned by the heirs of the late Yehuda Zisapel and Nava Zisapel. This lease expires in August 2028. The annual rent amounts to approximately $100,000.

• | In addition, we lease approximately 8,200 square feet of space in Jerusalem, Israel, for manufacturing facilities from an affiliated company owned by the heirs of the late Yehuda Zisapel, Nava Zisapel, and the heirs of the late Zohar Zisapel. This lease expires in August 2028. The annual rent amounts to approximately $160,000.

• | We lease approximately 16,900 square feet in Mahwah, New Jersey, consisting of approximately 12,700 square feet of office space and 4,200 square feet of warehouse space, from an affiliated company owned by the heirs of the late Yehuda Zisapel, Nava Zisapel, and the heirs of the late Zohar Zisapel. The annual rent amounts to approximately $195,000. The lease expires in March 2031.

Distribution Agreement

Bynet Data Communications Ltd. (Bynet), a member of the RAD-Bynet
Group, distributes our products in Israel on a non-exclusive basis. We have a written distributor agreement with Bynet under which
we provide Bynet with discounts on our solutions similar to the discounts provided to third-party distributors in the region in the ordinary
course of business. The total sales to Bynet (and other companies in the RAD-Bynet Group) under such distributor agreement amounted to
approximately $5.3 million in 2025, compared to $5.7 million in 2024 and $3.3 million in 2023.

Additional RAD-Bynet Group Equipment and Services

We purchase the following additional equipment services from members
of the RAD-Bynet Group: network management, IT and communication services, equipment testing and repair, inventory, cloud hosting services,
electricity charges, parking and building maintenance, reception and security services, vehicles and human resource administration and
marketing services.

A portion of the above services, such as electricity charges, are
"pass through" services for which we are charged on a "back-to-back" basis according to our actual usage (i.e.,
we are charged pro rata based on the actual charge of the third-party electricity company) due to the fact that we lease part of our facilities
from a number of other RAD-Bynet Group members. Other services mentioned above, such as vehicles and human resource administration, are
performed by one of the RAD-Bynet Group companies and are provided to all members of the RAD-Bynet Group, in order to achieve lower prices
for these services based on economies of scale. In addition, since the RAD-Bynet Group is comprised of a number of companies that are
engaged in our industry, the RAD-Bynet Group companies initiate marketing events from time to time, which we participate in, to promote
the RAD-Bynet Group members' products. The charges for these services are based on actual costs incurred and are allocated to the
Company according to its relative part in such services (e.g., vehicles administration – according to the number of the Company's
vehicles out of the total vehicles of the RAD-Bynet Group; marketing events – according to the number of participants who are our
customers out of the total number of participants in the events).

Transactions with Fortissimo Portfolio Companies

We have entered into a number of agreements with several Fortissimo Portfolio Companies
(as defined above). Under these agreements, we purchase certain products and services from such companies, as described below.

Summary

Following is a summary of the general purchases of products and services from the RAD-Bynet
Group companies (excluding leases, distribution and the services previously provided by SecurityDAM, which are described above) and Fortissimo
Portfolio Companies during 2025:

RAD-Bynet Group Entity | Products/Services
Bynet Data Communications Ltd. | Network management, IT and communication equipment, testing and repair, mutual marketing activities
Internet Binat Ltd. | IT and communication services
Bynet System Applications Ltd. | Communication equipment and services
Rad Data Communications Ltd. | Operating services and manpower
Cloudride Ltd. | Cloud hosting services, mutual marketing activities
Bynet Electronics Ltd. | Testing equipment and related services
Fortissimo Portfolio Company | Products/Services
Cellcom Israel Ltd. | Communication services
Accord Insurance Agency Ltd. | Insurance Agent
Sela Software Labs (Israel) Ltd | Cloud Hosting Services

The total cost of our purchases from the RAD-Bynet Group entities referenced in the
table above amounted to approximately $3.4 million in 2025, compared to $3.4 million in 2024 and $3.1 million in 2023. The total cost
of our purchases from Fortissimo Portfolio Companies referenced in the table above amounted to approximately $4.1 million in 2025, compared
to less than $1.0 million in 2024 and 2023.

We believe that our transactions and arrangements with affiliated parties, including
members of the RAD-Bynet Group or with any of the Fortissimo Portfolio Companies, are in the ordinary course of our business (other than
the SecurityDAM Acquisition) and are not unusual in their nature or conditions. However, in accordance with the Companies Law, they generally
require the approval of our Audit Committee and our Board of Directors and may, in certain circumstances, such as to the extent they relate
to compensation terms of our directors, require approval by our shareholders. In this respect, as permitted by the Companies Law, our
Audit Committee established internal policies with certain criteria and procedures designed to ensure that the terms of the transactions
to which we enter into with companies within the RAD-Bynet Group or with any of the Fortissimo Portfolio Companies, are made on market
terms and, at the same time, where such transactions are immaterial or negligible, both from a qualitative and quantitative perspective
(and/or are otherwise believed to be routine), would not require the pre-approval of our Audit Committee and Board of Directors. Our management
is required to examine whether transactions with the RAD-Bynet Group or any of the Fortissimo Portfolio Companies comply with such criteria,
and transactions that do not meet the criteria require pre-approval of our Audit Committee and such other corporate approvals prescribed
by the Companies Law.

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business

_Not available: the fetcher did not split out this section for this filing. Describe the business from the MD&A overview above instead, and say so in the note._

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | **MISSING** |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-03-31_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 10-K_2026-03-31_item7_mdna.md

**Missing:** 8-K filings, 8-K earnings press release exhibit, 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
