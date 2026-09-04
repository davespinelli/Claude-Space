# Triage pack — MLKN · MILLERKNOLL, INC.

_Generated 2026-09-04 15:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** MLKN · **Name:** MILLERKNOLL, INC.
- **CIK:** 0000066382
- **SIC:** 2520 — Office Furniture
- **Fiscal year end (MM-DD):** 05-30
- **Exchange:** Nasdaq
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/MLKN

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** MILLERKNOLL, INC.
- **CIK:** 66,382 · **SIC:** 2520 (Office Furniture) · **Exchange:** Nasdaq

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtAndCapitalLeaseObligations

**Valuation**

| metric | value |
|---|---|
| price | 22.39 |
| mktcap | $1.5B |
| ev | $2.6B |
| ev_ebit | 13.2x |
| fcf | $77.6M |
| fcf_yield | 5.1% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | 6.4% |
| net_debt | $1.1B |
| net_debt_ebit | 5.5x |
| cash | $167.7M |
| ltd | $1.3B |
| equity | $1.3B |
| ltd_tag | LongTermDebtAndCapitalLeaseObligations |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $3.8B |
| revenue_prior | $3.7B |
| rev_growth | 4.7% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | $198.3M |
| net_income | $91.5M |
| cfo | $199.9M |
| capex | $122.3M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.5% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 68,123,238 |
| shares_py | 67,806,605 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 20.2% |
| r6m | 14.3% |
| off_52w_high | -7.8% |
| adv20 | $11.9M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.50 |
| r_ev_ebit | 0.65 |
| r_roic | 0.57 |
| r_rev_growth | 0.52 |
| r_buyback | 0.57 |
| score | 0.61 |

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
| rank | 130 |

**Screen rationale:** 12-1 momentum 20.2%


## 3. Share count trend

- Shares outstanding: **68,123,238** (CY2026Q2I) vs **67,806,605** prior year (CY2025Q2I)
- Change: **0.5%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-03** — Item 5.02 (officer / director change or comp arrangement): On June 1, 2026, MillerKnoll, Inc. (the "Company") announced that its Board of Directors (the "Board") and Andi R. Owen, the Company's President and Chief Executive Officer, have mutually agreed that Ms. Owen will retire from the Company effective June 30...

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 90 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 18 |
| F | 36 |
| M | 36 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-06-24_2-02-results.md)

_Extraction: started at the first release heading, 'MillerKnoll, Inc. Reports Fourth Quarter and Full Fiscal Year 2026 Res'; skipped 15 forward-looking-statement block(s); 3 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (mlkn8k_05302026ex991.htm)

MillerKnoll, Inc. Reports Fourth Quarter and Full Fiscal Year 2026 Results

Zeeland, Mich., June 24, 2026 – MillerKnoll Inc. (NASDAQ: MLKN), a growth-oriented small-cap value company in the industrial and consumer sectors, today reported results for the fourth quarter and full fiscal year 2026, ended May 30, 2026.

Fourth Quarter and Fiscal 2026 Financial Results

(Unaudited) | (Unaudited)
Three Months Ended | Twelve Months Ended
(Dollars in millions, except per share data) | May 30, 2026 | May 31, 2025 | % Chg. | May 30, 2026 | May 31, 2025 | % Chg.
(13 weeks) | (13 weeks) | (52 weeks) | (52 weeks)
Net sales | 1,004.2 | 961.8 | 4.4 | % | 3,841.7 | 3,669.9 | 4.7 | %
Gross margin % | 39.4 | % | 39.2 | % | 38.8 | % | 38.8 | %
Operating expenses | 344.2 | 321.9 | 6.9 | % | 1,290.5 | 1,372.1 | (5.9) | %
Adjusted operating expenses * | 327.7 | 305.0 | 7.4 | % | 1,252.0 | 1,174.4 | 6.6 | %
Operating earnings % | 5.1 | % | 5.7 | % | 5.2 | % | 1.4 | %
Adjusted operating earnings % * | 6.9 | % | 7.5 | % | 6.2 | % | 6.8 | %
Earnings (loss) per share - diluted (1) | 0.34 | (0.84) | 140.5 | % | 1.32 | (0.54) | 344.4 | %
Adjusted earnings per share - diluted * | 0.55 | 0.60 | (8.3) | % | 1.86 | 1.95 | (4.6) | %
* Items indicated represent Non-GAAP measurements; see the reconciliations of Non-GAAP financial measures and related explanations below. (1) Due to the anti-dilutive effect resulting from periods where the Company reports a net loss, the impact of potentially dilutive securities on the per share amounts has been omitted from the calculation of weighted-average common shares outstanding for diluted net loss per common share.

"We delivered a strong fourth quarter relative to the expectations we set coming into the period. These results reflect the advantages of a business purpose-built around geographic and channel diversity. It is a business anchored by exceptional talent, iconic brands, world-class manufacturing capabilities, and an incomparable network of contract dealers, retail stores, and wholesale partners. I am honored to be stepping into the interim CEO role at an important time for the Company, and I am eager to help lead this business alongside a deeply tenured and highly aligned team of senior leaders with a shared desire to elevate our performance as a company," said Jeff Stutz, Chief Operating Officer and incoming interim CEO.

Stutz continued, "As we begin a new fiscal year, I am confident in our ability to execute our strategic vision with heightened discipline, drive improved profitability, and further strengthen our balance sheet, all with an eye toward improving long-term value creation."

Fourth Quarter

• Net sales of $1.004 billion, up 4.4% as reported and up 3.7% organically * , year-over-year

• Orders of $971.5 million, down 6.3% as reported and down 6.9% organically * , year-over-year, primarily related to the prior year order pull-forward of $55 million to $60 million in the North America Contract segment

• Gross margin increased 20 basis points

• Consolidated operating expenses increased to $344.2 million

• Consolidated adjusted operating expenses * increased to $327.7 million, driven primarily by variable selling expense, new store costs, higher compensation expense and the timing of program spend

• Operating expense special charges of $16.5 million:

◦ $8.1 million of restructuring charges related to targeted workforce reductions and a facility consolidation

◦ $5.8 million of purchase accounting amortization

◦ $2.6 million of CEO transition costs

• Operating margin of 5.1%, compared to 5.7% in the prior year

• Adjusted operating margin * of 6.9%, compared to 7.5% in the prior year

Fiscal 2026

• Net sales of $3.842 billion, up 4.7% as reported and up 3.6% organically * , year-over-year

• Gross margin was flat with the prior year

• Operating margin of 5.2%, compared to 1.4% in the prior year

• Adjusted operating margin * of 6.2%, compared to 6.8% in the prior year

Fourth Quarter 2026 Cash Flow, Debt, and Liquidity

• Liquidity, as of May 30, 2026, of $571.7 million reflected cash on hand and Revolving Credit Facility availability

• Cash flow from operations of $64.9 million, compared to $70.9 million in Q4 last year

• Net debt-to-EBITDA ratio, as defined by our Credit Facility, of 2.80x

• Near term scheduled debt maturities:

◦ $25.1 million in fiscal 2027

◦ $25.8 million in fiscal 2028

◦ $76.2 million in fiscal 2029

Dividend

• On April 14, 2026, MillerKnoll's Board of Directors declared a quarterly cash dividend of $0.1875 per share. The dividend is payable on July 15, 2026, to shareholders of record on May 30, 2026.

Fourth Quarter and Fiscal 2026 Results by Segment

North America Contract

• Q4 net sales of $530.2 million, up 6.9% as reported and up 6.7% organically * , year-over-year

• Q4 orders of $510.9 million, down 10.0% as reported and down 10.1% organically * , year-over-year

• Q4 operating margin of 8.2% compared to 7.7% in the prior year

• Q4 adjusted operating margin * of 10.4%, up 40 basis points compared to prior year, primarily from gross margin expansion driven by leverage on higher sales and pricing realization, partially offset by inflationary cost pressure

• Full year net sales of $2.061 billion, up 4.9% as reported and up 4.8% organically *

• Full year operating margin of 9.0%, up 280 basis points compared to prior year

• Full year adjusted operating margin * of 10.3%, up 60 basis points compared to prior year

International Contract

• Q4 net sales of $178.7 million, down 3.8% as reported and down 5.8% organically * , year-over-year

• Q4 orders of $173.0 million, down 8.7% as reported and down 10.6% organically * , year-over-year

• Q4 operating margin of 7.5% compared to 11.7% in the prior year

• Q4 adjusted operating margin * of 8.2%, down 470 basis points year-over-year, primarily from deleverage on lower sales, regional sales mix, foreign currency impact, and the timing of program spend

• Full year net sales of $674.0 million, up 2.1% as reported and down 1.2% organically *

• Full year operating margin of 8.1%, down 150 basis points compared to prior year

• Full year adjusted operating margin * of 8.6%, down 250 basis points compared to prior year

Global Retail

• Q4 net sales of $295.3 million, up 5.5% as reported and up 4.5% organically * , year-over-year

• Q4 orders of $287.6 million, up 2.8% as reported and up 2.0% organically * , year-over-year

◦ Q4 orders were up 8.8% in the North America region, year-over-year

• Q4 operating margin of 4.6% compared to 5.3% in the prior year

• Q4 adjusted operating margin * of 5.4%, down 110 basis points year-over-year, primarily due to the impact from opening new stores and underperformance by the Holly Hunt brand

• Full year net sales of $1,106.5 million, up 5.9% as reported and up 4.3% organically *

• Full year operating margin of 2.3%, up 860 basis points compared to prior year

• Full year adjusted operating margin * of 3.0%, down 200 basis points compared to prior year

• Q4 new retail store openings: DWR stores in Boulder, CO and Birmingham, MI, and Herman Miller stores in Ft. Lauderdale, FL and Woodbury, MN. Opened 15 total new retail stores in Fiscal 2026

First Quarter and Fiscal 2027 Outlook

The table below presents our selected expectations for the first quarter and full fiscal year 2027 financial operating results:

Q1 FY2027
Net sales | $928 million to $968 million
Gross margin % | 38.7% to 39.7%
Adjusted operating expenses * | $316 million to $326 million
Interest and other expense, net | $15 million to $16 million
Adjusted effective tax rate * | 24% to 26%
Adjusted earnings per share - diluted * | $0.33 to $0.39
Full Year FY2027
Net sales | $3.93 billion to $4.13 billion
Adjusted earnings per share - diluted * | $1.85 to $2.15
* Items indicated represent Non-GAAP measures. The Q1 FY2027 outlook excludes an expected $5.7 million in operating expense charges related to amortization of Knoll purchased intangibles and the related tax and earnings per share impact. The Company has not reconciled forward-looking non-GAAP measures because certain items that impact such measures are outside of the Company's control and/or cannot be reasonably predicted. These items are uncertain, depend on various factors, and could have a material impact on GAAP results for the guidance period. See "Non-GAAP Financial Measures and Other Supplemental Data."

The full year outlook also includes the following additional estimated full year expectations:

• Opening 14 to 18 new retail stores, including three to four new store openings in Q1

• Effective tax rate of approximately 22.5% to 24.5%

• Capital expenditures of approximately $125 million to $135 million

Webcast and Conference Call Information

The Company will host a conference call and webcast to discuss the results of the fourth quarter of fiscal 2026 on Wednesday, June 24, 2026, at 5:00 PM ET. To ensure participation, allow extra time to visit the Company's website at https://www.millerknoll.com/investor-relations/news-events/events-and-presentations to download the streaming software necessary to participate. An online archive of the webcast will also be available on the Company's investor relations website. Additional links to materials supporting the release will be available at https://www.millerknoll.com/investor-relations.

Financial highlights for the three and twelve months ended May 30, 2026 follow:

MillerKnoll, Inc.

Condensed Consolidated Statements of Operations

(Unaudited) (Dollars in millions, except per share and common share data) | Three Months Ended | Twelve Months Ended
May 30, 2026 | May 31, 2025 | May 30, 2026 | May 31, 2025
Net sales | 1,004.2 | 100.0 | % | 961.8 | 100.0 | % | 3,841.7 | 100.0 | % | 3,669.9 | 100.0 | %
Cost of sales | 608.6 | 60.6 | % | 584.9 | 60.8 | % | 2,352.9 | 61.2 | % | 2,247.3 | 61.2 | %
Gross margin | 395.6 | 39.4 | % | 376.9 | 39.2 | % | 1,488.8 | 38.8 | % | 1,422.6 | 38.8 | %
Operating expenses | 344.2 | 34.3 | % | 321.9 | 33.5 | % | 1,290.5 | 33.6 | % | 1,372.1 | 37.4 | %
Operating earnings | 51.4 | 5.1 | % | 55.0 | 5.7 | % | 198.3 | 5.2 | % | 50.5 | 1.4 | %
Other expenses, net | 13.6 | 1.4 | % | 19.3 | 2.0 | % | 70.1 | 1.8 | % | 72.4 | 2.0 | %
Earnings (loss) before income taxes and equity income | 37.8 | 3.8 | % | 35.7 | 3.7 | % | 128.2 | 3.3 | % | (21.9) | (0.6) | %
Income tax expense | 11.9 | 1.2 | % | 91.9 | 9.6 | % | 32.4 | 0.8 | % | 11.6 | 0.3 | %
Equity (loss) income, net of tax | (1.0) | (0.1) | % | — | — | % | (0.1) | — | % | 0.3 | — | %
Net earnings (loss) | 24.9 | 2.5 | % | (56.2) | (5.8) | % | 95.7 | 2.5 | % | (33.2) | (0.9) | %
Net earnings attributable to redeemable noncontrolling interests | 1.3 | 0.1 | % | 0.9 | 0.1 | % | 4.2 | 0.1 | % | 3.7 | 0.1 | %
Net earnings (loss) attributable to MillerKnoll, Inc. | 23.6 | 2.4 | % | (57.1) | (5.9) | % | 91.5 | 2.4 | % | (36.9) | (1.0) | %
Amounts per common share attributable to MillerKnoll, Inc.
Earnings (loss) per share - basic | $0.34 | ($0.84) | $1.33 | ($0.54)
Weighted average basic common shares | 68,798,344 | 68,091,762 | 68,736,117 | 68,977,267
Earnings (loss) per share - diluted | $0.34 | ($0.84) | $1.32 | ($0.54)
Weighted average diluted common shares | 69,416,668 | 68,091,762 | 69,321,661 | 68,977,267

MillerKnoll, Inc.

Condensed Consolidated Statements of Cash Flows

Twelve Months Ended
(Unaudited) (Dollars in millions) | May 30, 2026 | May 31, 2025
Cash provided by (used in):
Operating activities | 199.9 | 209.3
Investing activities | (115.6) | (100.9)
Financing activities | (117.0) | (150.3)
Effect of exchange rate changes | 6.7 | 5.2
Net change in cash and cash equivalents | (26.0) | (36.7)
Cash and cash equivalents, beginning of period | 193.7 | 230.4
Cash and cash equivalents, end of period | 167.7 | 193.7

MillerKnoll, Inc.

Condensed Consolidated Balance Sheets

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-07-20_item7_mdna.md)

_Extraction: started at the Overview heading._

Executive Overview

MillerKnoll is a collective of dynamic brands that comes together to design the world we live in. From the spaces we make that help us live and work better, to how we manufacture our products, to the ways we solve challenges facing our customers and global community, design is our tool for creating positive impact. Our optimism leads us as we redefine modern for the 21st century, shaping a future that's more sustainable, caring, and beautiful for all people and our planet.

MillerKnoll's products are sold internationally through controlled subsidiaries or branches in various countries including the United Kingdom, Denmark, Italy, France, the Netherlands, Canada, Japan, Mexico, Australia, Singapore, China, Hong Kong, India, and Brazil. The Company's products are sold in over 100 countries primarily through independent contract furniture dealers, direct customer sales, owned and independent retailers, direct-mail catalogs, and the Company's eCommerce platforms.

The Company is globally positioned in terms of manufacturing operations. In North America, manufacturing and distribution operations are in Georgia, New York, North Carolina, Michigan, Pennsylvania, and Texas in the United States, as well as Toronto and Mexico City. In Europe, the Company's manufacturing presence is in the United Kingdom and Italy. Manufacturing operations globally also include facilities located in Brazil, China, and India. The Company manufactures products using a system of lean manufacturing techniques collectively referred to as the MillerKnoll Performance System (MKPS). For its contract furniture business, MillerKnoll strives to maintain efficiencies and cost savings by minimizing the amount of inventory on hand. Accordingly, production is order-driven with direct materials and components purchased as needed to meet demand. These factors result in a high rate of inventory turns related to our manufactured inventories.

A key element of the Company's manufacturing strategy is to limit fixed production costs by sourcing component parts from strategic suppliers. This strategy has allowed the Company to increase the variable nature of its cost structure, while retaining proprietary control over those production processes that the Company believes provide a competitive advantage. As a result of this strategy, the Company's manufacturing operations are largely assembly-based.

A key element of the Company's growth strategy is to scale the Global Retail business through the Company's Herman Miller and Design Within Reach ("DWR") retail channels. DWR provides a channel to bring MillerKnoll's iconic and design-centric products across our brands such as Knoll, Muuto, and HAY, to retail customers, along with other proprietary and third-party products, with a focus on modern design.

The Company is comprised of various operating segments as defined by generally accepted accounting principles in the United States (U.S. GAAP). The operating segments are determined on the basis of how the Company internally reports and evaluates financial information used to make operating decisions. The Company has identified the following segments:

• North America Contract — Includes the operations associated with the design, sourcing, manufacture, and sale of furniture products directly or indirectly through an independent dealership network for office, healthcare, and educational environments throughout the United States and Canada as well as the global operations of the Spinneybeck, FilzFelt, Maharam, Edelman, and Knoll Textile brands.

• International Contract — Includes the operations associated with the design, sourcing, manufacture, and sale of furniture products, directly or indirectly through an independent dealership network for office, healthcare, and educational environments in Europe, the Middle East, Africa, Asia-Pacific, and Latin America.

• Global Retail — Includes global operations associated with the sale of modern design furnishings and accessories to third party retailers, as well as direct to consumer sales through eCommerce, direct-mail catalogs, and physical retail stores, along with the global operations of the Holly Hunt brand.

The Company also reports a corporate category consisting primarily of unallocated corporate expenses related to general corporate functions, including, but not limited to, certain legal, executive, corporate finance, information technology, administrative, and acquisition-related costs.

Core Strengths

The Company relies on the following core strengths in delivering solutions to customers:

• Product Portfolio and Brand Collective - MillerKnoll is a collective of globally recognized design brands known for working with some of the most well-known and respected designers in the world. Combined, the Company represents over 100 years of design research and exploration in service of humanity. Within the industries in which the Company operates, Herman Miller and Knoll, along with Colebrook Bosson Saunders, Design Within Reach, Edelman, FilzFelt, Geiger, HAY, Holly Hunt, Maharam, Muuto, NaughtOne and Spinneybeck are acknowledged as leading brands that inspire architects and designers to create their best design solutions. This portfolio has enabled MillerKnoll to connect with new audiences, channels, geographies, and product categories. Leveraging the collective brand equity of MillerKnoll across the lines of business is an important element of the Company's business strategy.

• Design Leadership - The Company is committed to developing research-based functionality and aesthetically innovative new products and has a history of doing so, in collaboration with a global network of leading independent designers. The Company believes its skills and experience in matching problem-solving design with the workplace needs of customers provide the Company with a competitive advantage in the marketplace. An important component of the Company's business strategy is to actively pursue a program of new product research, design, and development. The Company accomplishes this through the use of an internal research and engineering staff that engages with third party design resources generally compensated on a royalty basis.

• Unique Business Model - The Company has built a multi-channel distribution capability that it considers unique. Through contract furniture dealers, direct customer sales, retail stores and studios, eCommerce, wholesalers, and independent retailers, the Company serves contract and residential customers across a range of channels and geographies. As it pertains to its operations, the Company was among the first in the industry to embrace the concept of lean manufacturing. MKPS provides the foundation for all the Company's manufacturing operations. The Company is committed to continuously improving both product quality and production and operational efficiency. The Company believes these concepts hold significant promise for further gains in reliability, quality, and efficiency.

• Global Scale and Reach - In addition to its global omni-channel distribution capability, the Company has a global network of designers, suppliers, manufacturing operations, and research and development centers that position the Company to serve contract and residential customers globally. The Company believes that leveraging this global scale will be an important enabler to executing its strategy.

• Extraordinary People - We believe that our employees are a critical success factor for our business. We strive to identify, hire, develop, motivate and retain the best employees. Our ability to attract, engage, and retain key employees has been and will remain critical to our success.

Channels of Distribution

The Company's products and services are offered to most of its customers under standard trade credit terms between 30 and 45 days. For all the items below, revenue is recognized when control transfers to the customer. The Company's products and services are sold through the following distribution channels:

• Independent Contract Furniture Dealers - Most of the Company's product sales are made to a global network of independently owned and operated contract furniture dealerships. These dealers purchase the Company's products and distribute them to end customers. Many of these dealers also offer furniture-related services, including product installation.

• Direct Contract Sales - The Company sells products and services directly to end customers without an intermediary (e.g., sales to the U.S. federal government). In most of these instances, the Company contracts separately with a dealer or third-party installation company to provide sales-related services.

• eCommerce - The Company sells products in its portfolio of brands across the globe, through localized Herman Miller, Knoll, and DWR websites. These sites complement the Company's existing methods of distribution and extend the Company's brands' reach for new and existing customers and clients.

• Wholesale - Through the Company's Global Retail segment, certain products are sold on a wholesale basis to independent retailers located in various markets around the world.

• Retail Locations - As of May 30, 2026, the Company operated 93 retail stores, including 45 DWR stores, 39 Herman Miller stores, 4 Knoll stores, 1 Muuto store, 1 HAY store, and 3 outlet stores.

Areas of Strategic Focus

Our strategy is designed to harness the full potential of MillerKnoll while driving growth across all business segments, geographies, and customer groups and creating value for all our stakeholders. We will capitalize on global trends including hybrid and flexible work, consumers' focus on investing in their homes, a focus on health and well-being, and an expectation of corporate social responsibility. Our strategy includes three key focus areas:

Drive Customer Demand and Order Growth

_[...truncated at ~10,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-07-20_item1_business.md)

Item 1 Business

Overview

MillerKnoll is a collective of dynamic brands that comes together to design the world we live in. From the spaces we make that help us live and work better, to how we manufacture our products, to the ways we solve challenges facing our customers and global community, design is our tool for creating positive impact. Our optimism leads us as we redefine modern for the 21st century, shaping a future that's more sustainable, caring, and beautiful for all people and our planet.

The Company researches, designs, manufactures and distributes interior furnishings for use in various environments including residential, office, healthcare and educational settings, and provides related services that support organizations and individuals all over the world. The Company's products are sold primarily through the following channels: independent contract furniture dealers, direct customer sales, owned and independent retailers, direct-mail catalogs, and the Company's eCommerce platforms.

Powering the world's most dynamic design brands, MillerKnoll includes Herman Miller® and Knoll®, as well as Colebrook Bosson Saunders, Design Within Reach®, Edelman®, FilzFelt®, Geiger®, HAY®, Holly Hunt®, KnollTextiles®, Maharam®, Muuto®, NaughtOne®, and Spinneybeck®. MillerKnoll's corporate offices are located at 855 East Main Avenue, PO Box 302, Zeeland, Michigan, 49464-0302 and its telephone number is 616 654 3000. Unless otherwise noted or indicated by the context, all references to "MillerKnoll," "we," "our," "Company" and similar references are to MillerKnoll, Inc. and its controlled subsidiaries. Further information relating to principles of consolidation is provided in Note 1 to the Consolidated Financial Statements included in Item 8 of this report.

Segments

The Company has three reportable segments: North America Contract, International Contract, and Global Retail. The Company also reports a corporate category consisting primarily of unallocated corporate expenses. For a more detailed description of the Company's segments, refer to Item 7 of this report.

Financial information relating to segments is provided in Note 13 to the Consolidated Financial Statements included in Item 8 of this report.

Description of Business

MillerKnoll is a global leader of design. Our brands have led conversations on design for over 100 years, and we continue to drive our industry forward with visionary thinking and a purposeful approach. The Company's principal business consists of the research, design, manufacture, selling and distribution of seating products, furniture systems, other freestanding furniture elements, textiles, leather, felt, home furnishings and related services.

The Company's ingenuity and design excellence create award-winning products and services, which have made the Company a leader in the design and development of furniture, furniture systems, textiles, leather, felt and related technology and acoustical solutions. This leadership is exemplified by the innovative concepts introduced by the Company in its broad array of product offerings.

The Company's furniture systems, seating, freestanding furniture, storage, casegoods, textile products, leather, felt, acoustic products and related services are used in (1) institutional environments including offices and related conference, lobby, and lounge areas and general public areas including transportation terminals; (2) health/science environments including hospitals, clinics and other healthcare facilities; (3) industrial and educational settings; and (4) residential and other environments.

The Company's products are marketed worldwide by its own sales staff, independent dealers and retailers, via its eCommerce websites, and through its owned Herman Miller, Design Within Reach ("DWR"), HAY, Knoll, and Muuto retail stores. Salespeople work with dealers, the architecture and design community, and directly with end-users. Independent dealerships concentrate on the sale of MillerKnoll products and some complementary product lines of other manufacturers. It is estimated that approximately 53.6% of the Company's sales in the fiscal year ended May 30, 2026, were made directly through independent dealers. The remaining sales were made directly to end-users, including federal, state and local governments and several business organizations by the Company's own sales staff, retail channels, or to independent retailers.

The Company is a recognized leader within its industry for the use, development, and integration of customer-centered technologies that enhance the reliability, speed, and efficiency of our customers' operations. This includes proprietary sales tools, interior design and product specification software, order entry and manufacturing scheduling and production systems, and direct connectivity to the Company's suppliers.

Raw Materials

The Company's manufacturing materials are available from a number of sources within North America, South America, Europe and Asia. The costs of certain direct materials used in the Company's manufacturing and assembly operations are sensitive to shifts in commodity market prices. In particular, the costs of steel, plastic, aluminum components and particleboard are sensitive to the market prices of commodities such as raw steel, aluminum, crude oil, lumber and resins. Increases in the market prices for these commodities can have an adverse impact on the Company's profitability. Further information regarding the impact of direct material costs on the Company's financial results is provided in Management's Discussion and Analysis in Item 7 of this report, "Management's Discussion and Analysis of Financial Condition and Results of Operations".

Patents and Trademarks

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-07-20_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-07-20_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-07-20_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-06-24_2-02-results.md, 10-K_2026-07-20_item7_mdna.md, 10-K_2026-07-20_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
