# Triage pack — JFB · JFB Construction Holdings

_Generated 2026-09-05 03:06 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** JFB · **Name:** JFB Construction Holdings
- **CIK:** 0002024306
- **SIC:** 1540 — General Bldg Contractors - Nonresidential Bldgs
- **Fiscal year end (MM-DD):** 12-31
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/JFB

**Fetcher warnings for this ticker:** 10-K 2026-03-31: heading split missed Item 1 - Business, Item 1A - Risk Factors, Item 7 - MD&A; no proxy (DEF 14A) in recent filings

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** JFB Construction Holdings
- **CIK:** 2,024,306 · **SIC:** 1540 (General Bldg Contractors - Nonresidential Bldgs) · **Exchange:** Nasdaq

> **DEBT DATA MISSING — DO NOT SCORE THIS AS NET CASH.**
> debt data missing (net cash unverified) — no long-term-debt concept was tagged in any XBRL frame, so LTD was filled with 0: EV is understated, ROIC overstated, and any negative net debt is an artefact of that fill rather than a confirmed debt-free balance sheet. The `net_debt`, `net_debt_ebit`, `ev` and `roic` figures below are all affected.
> **Before scoring this name, read the balance sheet (total debt, current portion of long-term debt, revolver/credit-facility balance) and the MD&A liquidity and capital resources section in sections 8-9 of this pack, and use the figures you find there instead of the screen's.**

**Valuation**

| metric | value |
|---|---|
| price | 4.95 |
| mktcap | $86.6M |
| ev | $78.7M |
| ev_ebit | n/a |
| fcf | -$12.0M |
| fcf_yield | -13.9% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -11.2% |
| net_debt | -$8.0M |
| net_debt_ebit | n/a |
| cash | $8.0M |
| ltd | $0.00 |
| equity | $47.8M |
| ltd_tag | none |
| ltd_missing | True |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $30.5M |
| revenue_prior | $23.1M |
| rev_growth | 32.3% |
| rev_growth_note | share count +84.5% yoy — growth may be acquisition/issuance-driven, not organic |
| eq_flag | n/a |
| ebit | -$5.7M |
| net_income | -$5.3M |
| cfo | -$11.8M |
| capex | $227k |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 84.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 17,521,630 |
| shares_py | 9,496,900 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 24.5% |
| r6m | -43.1% |
| off_52w_high | -70.5% |
| adv20 | $2.8M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.06 |
| r_ev_ebit | 0.00 |
| r_roic | 0.12 |
| r_rev_growth | 0.90 |
| r_buyback | 0.02 |
| score | 0.17 |

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
| rank | 471 |

**Screen rationale:** revenue +32.3% BUT share count +84.5% yoy — growth may be acquisition/issuance-driven, not organic; debt data missing (net cash unverified); 12-1 momentum 24.5%; WARNING 6m return below -40%


## 3. Share count trend

- Shares outstanding: **17,521,630** (CY2026Q2I) vs **9,496,900** prior year (CY2025Q2I)
- Change: **84.5%** — dilution / growing count
- Source concept: `dei:EntityCommonStockSharesOutstanding`
- **Flag:** share count +84.5% yoy — growth may be acquisition/issuance-driven, not organic

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

_No Item 1.01 (material agreement), 1.02 (termination) or 5.02 (officer/director change) 8-K filed since 2026-03-03 among the 6 8-Ks fetched._

## 6. Insider activity (Form 4, trailing 12 months)

Net open-market activity (last 12m): buys 0 sh / $0 vs sells 4,039 sh / $59,992 -> net $-59,992 (SELLING).
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 15 (open-market buys 0, sales 2).

| code | rows |
|---|---|
| A | 13 |
| S | 2 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-05-12_7-01-reg-fd.md)

_Extraction: no Highlights/Results/quarter heading found; started at the top of the exhibit; skipped 8 forward-looking-statement block(s)._

## EX-99.1 - EX-99.1 (ex99-1.htm)

EX-99.1
ex99-1.htm
EX-99.1

Exhibit 99.1

JFB
Construction Announces 115% increase in Revenue

Q1
2026 over Q1 2025

Lantana,
Fla. – May 11, 2026 – JFB Construction Holdings (Nasdaq: JFB), a real estate development and construction company focused
on hospitality, commercial, industrial, and residential property development, announces that first quarter 2026 revenue increased 115%
as compared to the first quarter of 2025.

"The
first quarter of 2026 was another significant quarter for JFB Construction Holdings as revenue has more than doubled, up 115% as compared
to the first quarter of 2025," said Joseph F. Basile, III, CEO of JFB Construction Holdings. "Our revenue growth in the first
quarter of 2026 represents ongoing growth.

"In
addition, during the first quarter, we have continued signing key contracts. We anticipate a great pipeline of contracts throughout 2026,"
concluded Mr. Basile.

JFB
Construction Holdings has filed a Registration Statement on Form S-4 in relation to the Company's merger with XTEND, valued at
approximately $1.5 billion. As announced on March 4, 2026, XTEND currently has over $70 million in backlog contracts and over $500 million
in the anticipated pipeline.

About
JFB Construction Holdings

JFB
Construction Holdings (Nasdaq: JFB) is a real estate development and construction company that has provided general contracting and construction
management services in 36 U.S. states. For more information, visit the company's SEC filings at www.sec.gov .

investors@jfbconstruction.net

XTEND
Contact:

Headline
Media

Sarah
Small

255 1449

sarah@headline.media

XTEND
Investor Relations:

MZ
North America

Shannon
Devine

XTEND@mzgroup.us

203-741-8811

## 8. MD&A — no 10-K Item 7 fetched, using 10-Q MD&A (10-Q_2026-08-13_mdna.md)

_Extraction: started at the Overview heading._

Overview

JFB is a commercial and residential construction company specializing in retail buildouts, multifamily developments, luxury homes and general commercial construction. We have strong relationships with franchisees and franchisors, which has been the foundation of driving steady growth, especially in the Southern Atlantic region. Our expansion plans include vertically integrated real estate development projects and securing larger, more complex construction projects that require higher bond capacity.

Revenue Sources

Our primary markets vary across our business segments.

Commercial Contracting Segments

Our commercial contracting segment has completed projects in 36 states, delivering over 2 million square feet of commercial retail and shopping center space construction and improvements. This segment's market is driven primarily by our ability to provide services to franchisees and franchisors nationwide, regardless of project location because of our operational flexibility and established relationships with franchisees and franchisors alike. While we have historically focused on the Southern Atlantic region, including Florida, Georgia, South Carolina, and North Carolina, where we have established a strong reputation and network, our growth is increasingly tied to the strength of our relationships with franchisees and the trust of franchisors who rely on us as preferred builders for multiple projects.

Real Estate Development Segment

Our real estate development segment is currently concentrated in South Florida, with plans to leverage our regional success to expand into other southern and U.S. markets by identifying market opportunities and joint venture partners that align with our objectives. Our residential construction segment is also focused on South Florida, with no current plans for expansion beyond this market.

Rental Income Segment

Our rental income segment consists primarily of revenue generated from the lease and sublease of office space within our corporate headquarters in South Florida. As part of our broader real estate strategy, we actively manage excess capacity within our facilities to optimize utilization and generate recurring, non‑construction revenue streams. This includes subleasing portions of our office space to third‑party tenants whose operational needs align with our building configuration and occupancy standards.

Rental income is recognized in accordance with the underlying lease and sublease agreements, which generally provide for fixed monthly payments and, in certain cases, reimbursement of shared operating costs. Subleasing activity allows us to offset a portion of our occupancy expenses while maintaining flexibility to scale our internal footprint as our operating segments grow. We continue to evaluate opportunities to enhance this segment by identifying additional space within our facilities that may be suitable for sublease arrangements, provided such activity remains consistent with our long‑term operational requirements.

Corporate Growth and Expansion

Management believes we will leverage our established industry relationships, experience operating in various jurisdictions and navigating complex construction regulations to meet our growth objectives of continuing to expand our market throughout more of the United States and successfully winning bids for larger construction projects. The Company intends to focus its business in states with increased population and GDP growth, such as Florida, Texas and South Carolina. However, as we expand into new territories, our reputation for excellence will be less known by new clients and we will need to compete with other construction companies that may have been operating in a given region for years and already have built up reliable networks of clients, vendors, contractors, and other market participants. We believe our ability to rely on our relationships within the franchise industry and more generally the real estate development industry, should offset some of this potential risk, however, by continuing to build on our experience and proven track record.

Our expansion and growth goals, some of which will come with more capital intensive projects, may expose the Company to greater risks related to lack of performance, faltering relationships, improper investment of resources or otherwise. The Company also recognizes operations are likely to fluctuate significantly and historical results should not be considered indicative of results for any future periods. While taking into account the inherent risks, it is our intent to capitalize on our increased access to capital and credibility to fund new projects and increase our bond-ability fueling our intended growth. Our ability to obtain surety bonds is important for expanding our operations, as bonding is often required for bidding on public and large private projects. Increased bonding capacity allows us to pursue more high-value contracts, particularly in government and infrastructure sectors, enhancing revenue opportunities and market diversification. It also strengthens our credibility with clients and lenders, reflecting our financial stability. This credibility can lead to improved financial terms and mitigate risks associated with contract defaults, enabling the company to confidently take on larger projects and drive long-term growth.

We have extensive experience building and remodeling hundreds of franchise locations for corporate franchisors and franchisees for national, fast expanding brands, including Orange Theory Fitness, European Wax Center, Massage Envy, Planet Fitness, V/O Medspa, Arby's, Tropical Smoothie Cafe, Amazing Lash Studio, Starbucks and Save-A-Lot. For our franchise clients, we offer interior remodeling, space optimization, and the integration of advanced design to create functional and attractive retail environments. The Company expects consistent and reliable revenue for this division based on established relationships and clients affiliated with reputable name brands. Should such relationships be compromised or key individuals leave their positions with franchisors, our consistent revenue sources could be adversely impacted. However, the departure of key individuals may create new opportunities with the franchisors these individuals transition to. We intend to continue to utilize our commitment to quality craftsmanship, attention to detail, and customer satisfaction to set us apart in this market. Should the quality of our workmanship suffer through poor project management or quality control, our reputation may be impacted, reducing our ability to attract new clients or retain past clients. Each project with our significant franchise client, Planet Fitness, is under a separate agreement, but our standard business arrangement involves a fixed-price commercial construction contract valued between $1.5-2 million, with an anticipated completion timeline of 12-14 weeks. Payments are due within 30 days of invoice, aligning with project milestones to ensure cash flow and maintain project pace. Management believes JFB Construction's unique selling proposition lies in our ability to tailor solutions to meet the specific needs of each client, familiarity of the needs of our clients within the franchise construction niche, and delivering projects on time and within budget. Further, we attempt to offer efficient and economical solutions for our client's expanding franchisee and franchisor businesses by allowing them to utilize the same contractor for many of their franchise locations.

Presently, the Company has begun to expand its real estate development segment by being the general contractor on low rise apartment and townhome developments projects. In the future, the Company also intends to invest directly or through joint ventures in real estate development projects. While these investments present a pathway to generate additional revenues by selling completed projects at a premium, generating rental income and/or to vertically integrate by securing valuable construction contracts associated with the projects, they also involve considerable capital commitments and exposure to market volatility, project delays, and other risks associated with real estate development. The illiquid nature of these investments further amplifies the challenges, as capital is often tied up for extended periods, limiting the company's flexibility to redeploy resources. We believe the Company's integrated approach, combining investment with the potential to secure construction contracts, will offset such risks by securing additional large-scale construction projects and potential revenue generated from the investments. Presently, our focus is on apartment complexes and townhouses, with a potential shift to mixed-use buildings, hotels and commercial properties in the future as our business expands and new opportunities are presented.

Residential Construction Segment

Our residential construction segment focuses on custom home builds, in addition to certain remodeling projects primarily in the South Florida region with a focus on superior craftsmanship and attention to detail. Some of our luxury residential projects also include state of the art equestrian facilities. We have focused more on growth of this segment to continue to diversify our service offerings. Our relationships with architects, engineers and designers create opportunities for these projects and we will continue to foster these relationships to continue growth in this division.

Strategic Goals

In addition to our expansion into key states such as Florida, Texas, and South Carolina, we have set forward-looking strategic milestones—including targeted market penetration rates, phased rollouts, and revenue growth objectives over the next 12 to 24 months—to overcome regional brand recognition challenges and establish a robust presence in these markets.

Recent Developments

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
| MD&A / management commentary | 10-K Item 7 MD&A | **MISSING** |
| Risk factors | 10-K Item 1A - Risk Factors | **MISSING** |

**Present:** meta.json, form4_summary.md, 8-K_2026-05-12_7-01-reg-fd.md, 10-Q_2026-08-13_mdna.md (10-Q MD&A used in place of the 10-K)

**Missing:** 10-K Item 7 MD&A (substituted 10-Q MD&A), 10-K Item 1 - Business (business description), transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
