# Triage pack — WS · Worthington Steel, Inc.

_Generated 2026-09-04 20:36 UTC by research/deepvalue/triage_pack.py. Excerpts only: every section is truncated. Do not infer anything the text does not say._

## 1. Company identity

- **Ticker:** WS · **Name:** Worthington Steel, Inc.
- **CIK:** 0001968487
- **SIC:** 3310 — Steel Works, Blast Furnaces & Rolling & Finishing Mills
- **Fiscal year end (MM-DD):** 05-31
- **Exchange:** NYSE
- **Filings fetched:** /home/user/Claude-Space/research/deepvalue/filings/WS

## 2. Screen row (all metrics)

_Source: universe_under2b.csv (not a screen candidate)_

- **Name:** Worthington Steel, Inc.
- **CIK:** 1,968,487 · **SIC:** 3310 (Steel Works, Blast Furnaces & Rolling & Finishing Mills) · **Exchange:** NYSE

**Debt data:** OK — long-term debt from us-gaap:LongTermDebtNoncurrent

**Valuation**

| metric | value |
|---|---|
| price | 35.99 |
| mktcap | $1.8B |
| ev | $1.8B |
| ev_ebit | n/a |
| fcf | $80.0M |
| fcf_yield | 4.4% |

**Quality and balance sheet**

| metric | value |
|---|---|
| roic | -0.1% |
| net_debt | -$40.2M |
| net_debt_ebit | n/a |
| cash | $84.6M |
| ltd | $44.4M |
| equity | $1.1B |
| ltd_tag | LongTermDebtNoncurrent |
| ltd_missing | False |

**Growth and operations**

| metric | value |
|---|---|
| revenue | $3.4B |
| revenue_prior | $3.1B |
| rev_growth | 11.3% |
| rev_growth_note | n/a |
| eq_flag | n/a |
| ebit | -$1.4M |
| net_income | -$13.0M |
| cfo | $201.2M |
| capex | $121.2M |

**Capital allocation**

| metric | value |
|---|---|
| share_chg | 0.1% |
| share_chg_src | dei:EntityCommonStockSharesOutstanding |
| shares | 50,948,146 |
| shares_py | 50,872,821 |

**Price behaviour and liquidity**

| metric | value |
|---|---|
| mom_12_1 | 20.8% |
| r6m | -5.6% |
| off_52w_high | -25.4% |
| adv20 | $8.5M |

**Screen ranks (0-1, higher is better)**

| metric | value |
|---|---|
| r_fcf_yield | 0.45 |
| r_ev_ebit | 0.00 |
| r_roic | 0.30 |
| r_rev_growth | 0.69 |
| r_buyback | 0.63 |
| score | 0.46 |

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
| rank | 277 |

**Screen rationale:** 12-1 momentum 20.8%


## 3. Share count trend

- Shares outstanding: **50,948,146** (CY2026Q2I) vs **50,872,821** prior year (CY2025Q2I)
- Change: **0.1%** — roughly flat
- Source concept: `dei:EntityCommonStockSharesOutstanding`

## 4. Price range (1 year)

_Not included: skipped (TRIAGE_NO_PRICE set)._

## 5. Material 8-K events, last 6 months (Items 1.01 / 1.02 / 5.02)

- **2026-06-30** — Item 1.01 (Entry into a Material Definitive Agreement): On June 25, 2026, Worthington Steel, Inc. (the " Company ") entered into that certain Credit Agreement (the " Credit Agreement "), an asset-based revolving credit agreement, among the Company, as borrower, the lenders party thereto, and Wells Fargo Bank...
- **2026-06-30** — Item 1.02 (Termination of a Material Definitive Agreement): On June 25, 2026, upon execution of the Credit Agreement, the Company terminated the Former Credit Agreement.
- **2026-06-25** — Item 5.02 (officer / director change or comp arrangement): On June 23, 2026, Steven R. Witt announced his retirement from his position as Corporate Controller and Principal Accounting Officer of Worthington Steel, Inc. (the "Company"), effective June 23, 2026.

## 6. Insider activity (Form 4, trailing 12 months)

No open-market insider purchases or sales (codes P/S) in the last 12m — only non-market rows such as grants, option exercises, gifts or tax withholding. No observation; not a signal.
Distinct insiders buying (code P): 0. Largest buy: none.

Form 4 filings parsed: 12; transaction rows: 18 (open-market buys 0, sales 0).

| code | rows |
|---|---|
| A | 8 |
| F | 10 |

Codes: P=open-market purchase, S=open-market sale, A=grant/award, M=option exercise, F=tax withholding, G=gift.

Detail: form4_last12m.csv

## 7. Latest earnings press release (8-K exhibit from 8-K_2026-07-10_2-02-results.md)

_Extraction: started at the first release heading, 'Worthington Steel Reports Fourth Quarter Fiscal 2026 Results'; skipped 11 forward-looking-statement block(s); 5 block(s) of pre-heading matter dropped._

## EX-99.1 - EX-99.1 (ws-ex99_1.htm)

Worthington Steel Reports Fourth Quarter Fiscal 2026 Results

COLUMBUS, Ohio – Worthington Steel, Inc. (NYSE: WS), a market-leading, value-added metals processing company, reported updated financial results for the fiscal 2026 fourth quarter ended May 31, 2026.

Fourth Quarter Highlights (all comparisons to the fourth quarter of fiscal 2025) :

•
Net sales of $929.2 million increased 12% compared to $832.9 million.

•
Operating loss of $74.5 million compared to operating income of $66.4 million due primarily to non-cash impairments in the Electrical Steel reporting unit and acquisition related expenses in the fourth quarter of fiscal 2026.

•
Net loss attributable to controlling interest of $57.5 million compared to net earnings attributable to controlling interest of $55.7 million.

•
Net loss per diluted share attributable to controlling interest of $1.15 compared to net earnings per diluted share attributable to controlling interest of $1.10; adjusted net earnings per diluted share attributable to controlling interest of $0.75 compared to $1.05.

•
Adjusted EBIT of $54.3 million compared to $70.1 million.

•
In January 2026, the Company entered into a business combination agreement with Klöckner & Co SE ("Kloeckner") and launched a voluntary public cash takeover offer for all outstanding Kloeckner shares at €11.00 per share. During the fourth quarter, shares representing a majority of Kloeckner's outstanding share capital were tendered into the offer, satisfying the minimum acceptance threshold. On June 3, 2026, subsequent to the end of fiscal 2026, the Company completed settlement of the offer and its acquisition of a majority interest in Kloeckner, securing approximately 62% of Kloeckner's outstanding shares following settlement (the "Kloeckner Acquisition"), representing a significant milestone toward eventual operating control and value capture.

•
Recognized as a John Deere Partner-level Supplier for the 14 th consecutive year and received John Deere's inaugural Community Engagement Award.

•
Named a Top Workplace in Columbus by Columbus CEO magazine, marking the 14 th consecutive year the Company has earned this recognition.

•
Declared a quarterly dividend of $0.16 per share payable on September 29, 2026, to shareholders of record at the close of business on September 15, 2026.

"Worthington Steel closed fiscal 2026 with continued progress against our long-term strategy," said Geoff Gilmore, president and chief executive officer. "Fourth quarter results reflected solid execution in a mixed market with tighter year-over-year value-added spreads, which are beginning to normalize. Higher net sales were supported by growth in our direct business and continued focus on value-added solutions for customers. The completion of the Kloeckner transaction shortly after year-end marks the largest acquisition in our history and a defining step in building a stronger, more diversified metals processing platform. As we move forward, our priorities remain clear: safety, customer service, operational discipline, integration readiness and strong returns for shareholders."

Financial highlights for the fiscal 2026 periods and the comparative periods are as follows:

(In millions, except volume)

4Q 2026 | 4Q 2025 | FY 2026 | FY 2025
Volume (tons) | 938,589 | 982,180 | 3,586,817 | 3,793,752
Net sales | 929.2 | 832.9 | 3,443.8 | 3,093.3
Operating income (loss) | (74.5 | 66.4 | (1.4 | 147.0
Net earnings (loss) attributable to controlling interest | (57.5 | 55.7 | 8.5 | 110.7
Adjusted EBIT (Non-GAAP) (1) | 54.3 | 70.1 | 161.1 | 149.1
Equity in net income of unconsolidated affiliate | 3.6 | 4.0 | 20.3 | 4.4

(Per diluted share amounts, after-tax)

4Q 2026 | 4Q 2025 | FY 2026 | FY 2025
Net earnings (loss) per diluted share attributable to controlling interest | (1.15 | 1.10 | 0.17 | 2.19
Impairment of goodwill, long-lived, and other assets | 1.47 | - | 1.50 | 0.07
Restructuring and other (income) expense, net | - | 0.01 | (0.07 | 0.02
Kloeckner purchase derivative | 0.17 | - | 0.04 | -
Kloeckner acquisition-related expenses | 0.23 | - | 0.54 | -
Kloeckner securities investment income, net | (0.24 | - | (0.24 | -
Bridge nonrevolving loan commitment costs | 0.26 | - | 0.26 | -
Pension adjustments | (0.01 | - | (0.01 | (0.04
Sitem Group acquisition completion bonus payment | - | - | 0.03 | -
Gain on Sitem Group purchase derivative | - | (0.06 | - | (0.06
Deferred tax asset adjustment | - | - | 0.02 | -
Gain on land sale | - | - | - | (0.02
Impact of dilutive shares (2) | 0.02 | - | - | -
Adjusted net earnings per diluted share attributable to controlling interest (Non-GAAP) (1) | 0.75 | 1.05 | 2.24 | 2.16

(1)
Results in both the current year period and prior year period were impacted by certain items, as further discussed and reconciled to the most directly comparable GAAP financial measure in the Non-GAAP Financial Measures / Supplemental Data section later in this release.

(2)
For the fourth quarter of fiscal 2026, net loss per diluted share attributable to controlling interest was based on weighted average diluted shares outstanding of 49.9 million, which excluded non-qualified stock options and restricted common share awards, as the effect would be anti-dilutive. The calculation of adjusted net earnings per diluted share attributable to controlling interest (Non-GAAP) was based on weighted average diluted shares outstanding of 50.9 million, as non-qualified stock options and restricted common share awards are dilutive for adjusted net earnings per diluted share attributable to controlling interest (Non-GAAP).

Quarterly Results

Net sales for the fourth quarter of fiscal 2026 were $929.2 million, an increase of $96.3 million, or 12%, compared to the prior year quarter. This increase was driven primarily by higher direct volumes, including the $47.6 million impact of the addition of Sitem Group and, to a lesser extent, higher average direct selling prices. Direct tons sold increased by 3%, with legacy business, excluding Sitem Group, increasing 1% and the remaining increase due to the addition of Sitem Group. Direct selling prices, excluding the impact of Sitem Group, increased 5% in the fourth quarter of fiscal 2026 compared to the prior year quarter. Toll processing sales decreased $1.9 million, or 6%, in the fourth quarter of fiscal 2026 compared to the prior year quarter. Toll volumes decreased 15% in the fourth quarter of fiscal 2026 compared to the prior year quarter. The decrease in toll volumes was due to a combination of closing the Cleveland-area Worthington Samuel Coil Processing ("WSCP") facility in May 2025 as well as softening demand from mill customers. Toll selling prices increased 11% in the fourth quarter of fiscal 2026 compared to the prior year quarter, primarily due to higher value-added mix within toll processing. The mix of direct tons versus toll tons processed was 65% to 35% in the fourth quarter of fiscal 2026 compared to 60% to 40% in the prior year quarter.

Gross margin in the fourth quarter of fiscal 2026 was $118.8 million, a decrease of $8.2 million compared to the prior year quarter. The decrease was primarily driven by lower direct spreads (calculated as sales less material costs) and lower toll spreads, partially offset by a $3.1 million favorable impact from Sitem Group. Direct spreads decreased by $6.6 million primarily due to a $6.1 million unfavorable change from an estimated $20.8 million inventory holding gain in the prior year quarter to an estimated $14.7 million inventory holding gain in the fourth quarter of fiscal 2026. Additionally, value-added market spread compression negatively impacted direct spreads by $2.6 million compared to the prior year. These headwinds were partially offset by $2.1 million spread impact of higher direct volumes, notably in automotive. Toll spreads, down $2.4 million, were negatively impacted by $4.0 million due to lower volumes, partially offset by $1.6 million due to a favorable change in toll price due to mix.

Operating loss in the fourth quarter of fiscal 2026 was $74.5 million, a decrease of $140.9 million compared to the prior year quarter. The decrease was driven primarily by $112.2 million of goodwill, long-lived, and other asset impairment charges, a $22.2 million increase in selling, general and administrative ("SG&A") expense, and a $8.2 million decrease in gross margin, partially offset by a $1.7 million favorable change in restructuring and other (income), expense, net. During the fourth quarter of fiscal 2026, the Company recognized $112.2 million of impairments related to goodwill and long-lived assets within the Electrical Steel reporting unit. The impairments resulted from weakened demand in certain end markets, particularly industrial motors in both Europe and the United States, due to increased foreign competition, and in automotive, some delayed program launches. The $22.2 million increase in SG&A expense,

which included $4.2 million related to Sitem Group, was primarily attributable to $15.5 million of professional fees related to the Kloeckner Acquisition, and to a lesser extent, an increase in compensation and benefits expenses of $2.5 million. During the fourth quarter of fiscal 2025, the Company recognized restructuring expenses of $1.7 million due to the previously announced plans to combine WSCP's toll processing manufacturing facility in Cleveland, Ohio into its existing manufacturing facility in Twinsburg, Ohio, as well as the severance expense associated with the TWB Company's ("TWB") voluntary retirement program.

Net loss attributable to controlling interest of $57.5 million in the fourth quarter of fiscal 2026 compares to net earnings attributable to controlling interest of $55.7 million in the prior year quarter. Net loss per diluted share attributable to controlling interest of $1.15 per diluted share for its fiscal 2026 fourth quarter compares to net earnings per diluted share attributable to controlling interest of $1.10 in the prior year quarter.

Adjusted net earnings attributable to controlling interest of $38.3 million in the fourth quarter of fiscal 2026 compares to $53.4 million in the prior year quarter. Adjusted net earnings per diluted share attributable to controlling interest of $0.75 compares to $1.05 in the prior year quarter. The fourth quarter of fiscal 2026 adjusted results exclude a $74.7 million after-tax impairment of goodwill and long-lived assets, or $1.47 per diluted share, an $8.7 million unrealized after-tax loss on a Kloeckner purchase derivative, or $0.17 per diluted share, an $11.8 million after-tax Kloeckner acquisition-related expenses adjustment, or $0.23 per diluted share, a $12.2 million after-tax gain due to net investment income on Kloeckner securities held, or $0.24 per diluted share, a $13.5 million after-tax adjustment due to the expense related to the bridge nonrevolving loan commitment costs associated with the Kloeckner Acquisition, or $0.26 per diluted share, and $0.7 million after-tax pension adjustments, or $0.01 per diluted share. In addition, the impact of $0.02 per dilutive share was excluded in calculating the Company's fourth quarter fiscal 2026 adjusted net earnings per diluted share attributable to controlling interest as this reflects the effect of these potentially dilutive shares that would otherwise be anti-dilutive on the net loss attributable to controlling interest. The prior year quarter adjusted results exclude a $3.0 million after-tax gain on the Sitem Group purchase price derivative, or $0.06 per diluted share, and $0.7 million after-tax restructuring and other expense, net, or $0.01 per diluted share. For additional information on non-GAAP financial measures, see the Non-GAAP Financial Measures / Supplemental Data section later in this release.

_[...truncated at ~12,000 chars of this document]_

## 8. 10-K Item 7 MD&A — Overview / Results of Operations (10-K_2026-07-30_item7_mdna.md)

_Extraction: split excerpt: Overview block + Results of Operations block._

Introduction

This Management's Discussion and Analysis of Financial Condition and Results of Operations ("MD&A") should be read in conjunction with our consolidated and combined financial statements and the related Notes in this Form 10-K. This MD&A is designed to provide a reader with material information relevant to an assessment of our financial condition and results of operations and to allow investors to view the Company from the perspective of management.

The MD&A included in this report discusses our fiscal 2026 and fiscal 2025 financial condition and results of operations. For a comparison and discussion of our results of operations and financial condition for fiscal 2025 and fiscal 2024, see "Part II – Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations – Results of Operations – Fiscal 2025 Compared to Fiscal 2024" of our Annual Report on Form 10-K for the fiscal year ended May 31, 2025, filed with the SEC on July 29, 2025.

Basis of Presentation

Worthington Steel was formed as an Ohio corporation on February 28, 2023, for the purpose of receiving, pursuant to a reorganization, all of the outstanding equity interests of the steel processing business of Worthington Enterprises. On December 1, 2023, the Separation was completed and Worthington Steel became an independent, publicly traded company. Our financial statements for the periods until the Separation on December 1, 2023, are combined financial statements prepared on a carve-out basis. Our financial statements for the periods beginning on and after December 1, 2023, are consolidated financial statements based on our reported results as a stand-alone company. Accordingly, the third quarter of fiscal 2024 and onward included consolidated and combined financial statements, whereas all prior periods included combined financial statements. For additional information, see "Note 1 – Description of Business, The Separation, and Basis of Presentation".

Business Overview

We are one of North America's premier value-added metals processors with the ability to provide a diversified range of products and services that span a variety of end markets. We maintain market-leading positions in the North American carbon flat-rolled steel and tailor welded blank industries and are one of the largest global producers of electrical steel laminations. For over 70 years, we have been delivering high-quality steel processing capabilities across a variety of end markets including automotive, heavy truck, agriculture, construction, and energy. With the ability to produce customized steel solutions, we aim to be the preferred value-added steel processor in the markets we serve by delivering highly technical, customer-specific solutions, while also providing advanced materials support. Our scale allows us to achieve an advantaged cost structure and service platform supported by a strategic operating footprint. We serve our customers by processing flat-rolled steel coils, which we source primarily from various North American steel mills, into the precise type, thickness, length, width, shape, and surface quality required by customer specifications. We sell steel on a direct basis, whereby we are exposed to the risks and rewards of ownership of the material while in our possession. Additionally, we toll process steel under a fee for service arrangement whereby we process customer-owned material. Our manufacturing facilities further benefit from the flexibility to scale between direct and tolling services based on demand dynamics throughout the year.

Our operations are managed principally on a products and services basis under a single group organizational structure. We own controlling interests in the following operating joint ventures: Spartan, TWB, WSCP, and Sitem Group. We also own a controlling interest in WSP, which became a nonoperating joint venture in October 2022, when we completed the divestiture of its remaining net assets. The net assets and operating results of these joint ventures are consolidated with the equity owned by the minority joint venture member shown as "Noncontrolling interests", or, in the case of Sitem Group, "Redeemable noncontrolling interest" in our consolidated balance sheets, and the noncontrolling interest in net earnings and Other Comprehensive Income ("OCI") shown as net earnings or comprehensive income attributable to noncontrolling interests in our consolidated and combined statements of earnings and consolidated and combined statements of comprehensive income, respectively. Our remaining joint venture, Serviacero Worthington, is unconsolidated and accounted for using the equity method.

AI in Transformation

During fiscal 2026, we continued integrating commercially available AI technologies into our long-term transformation strategy. Through these efforts, we use AI to generate insights, evaluate strategies, and automate routine tasks, improving productivity and strengthening internal decision-making. We are developing and refining AI solutions in areas such as predictive maintenance and intelligent reporting, which drive greater value through smarter, more connected systems. Expanding the use of AI across operations and the back-office functions enables our teams to devote more time to the highest-value aspects of their roles.

Recent Business Developments

•
On June 1, 2026, we incurred indebtedness in the form of (1) the 2033 Notes, due June 1, 2033, and (2) the seven-year Term Loans under the Term Loan Facility.

•
On June 3, 2026, we closed the Kloeckner Acquisition, at which date we owned approximately 60.86% of Kloeckner's total outstanding share capital.

•
On June 15, 2026, we settled our binding agreement to acquire one million additional Kloeckner shares at €11.00 per share (approximately $12.7 million), bringing our total ownership to approximately 61.87% of Kloeckner's total outstanding share capital.

_[...truncated at ~6,000 chars of this document]_

... [gap in Item 7 skipped] ...

Results of Operations

Fiscal 2026 Compared to Fiscal 2025

The tables throughout this section present, on a comparative basis, our results of operations for the past two fiscal years.

(In millions, except volume and per common share amounts) | 2026 | 2025 | Change
Volume (in tons) | 3,586,817 | 3,793,752 | (206,935
Net sales | 3,443.8 | 3,093.3 | 350.5
Operating income (loss) | (1.4 | 147.0 | (148.4
Equity income | 20.3 | 4.4 | 15.9
Net earnings attributable to controlling interest | 8.5 | 110.7 | (102.2
Earnings per diluted share attributable to controlling interest | 0.17 | 2.19 | (2.02

Net sales in fiscal 2026 were $3,443.8 million, an increase of $350.5 million, or 11%, compared to fiscal 2025. The increase was driven primarily by higher direct volumes, including the $165.7 million impact of the addition of Sitem Group and, to a lesser extent, higher average direct selling prices. Direct tons sold increased 6%, with legacy business increasing 5% and the remaining increase due to the addition of Sitem Group. Direct selling prices, excluding the impact of Sitem Group, increased 3% in fiscal 2026 compared to fiscal 2025. Toll processing net sales decreased 20% in fiscal 2026 compared to fiscal 2025. The decrease in toll volumes was due to a combination of closing the Cleveland-area WSCP facility in May 2025 as well as softening demand from mill customers as they required less outside processing to meet their production requirements. Toll selling prices increased 1% in fiscal 2026 compared to fiscal 2025. The mix of direct versus toll volumes was 64% to 36% in fiscal 2026, compared to 57% to 43% in fiscal 2025.

Gross Margin

Change
(In millions) | 2026 | % of Net sales | 2025 | % of Net sales | %
Gross margin | 403.3 | 11.7 | % | 388.6 | 12.6 | % | 14.7 | 3.8 | %

Gross margin in fiscal 2026 was $403.3 million, an increase of $14.7 million, compared to fiscal 2025. The increase was primarily driven by higher direct spreads, and to a lesser extent, a $2.0 million favorable impact from Sitem Group, which was partially offset by lower toll spreads. Direct spreads increased by $49.0 million, primarily due to the $32.2 million impact of higher direct volume, as well as a $25.6 million change from $10.4 million in estimated inventory holding losses in fiscal 2025 compared to estimated holding gains of $15.2 million in fiscal 2026. These gains in direct spreads were partially offset by an $8.8 million unfavorable impact due to value-added market spread compression compared to the prior year. Toll spreads, down $30.6 million, were negatively impacted by $24.9 million due to lower volumes and $5.7 million due to an unfavorable change in toll price, primarily due to mix.

Selling, General and Administrative Expense

Change
(In millions) | 2026 | % of Net sales | 2025 | % of Net sales | %
Selling, general and administrative expense | 297.4 | 8.6 | % | 231.6 | 7.5 | % | 65.8 | 28.4 | %

Selling, general and administrative expense ("SG&A") in fiscal 2026 was $297.4 million, an increase of $65.8 million compared to fiscal 2025. The increase in SG&A expense included $19.0 million related to Sitem Group, which includes a one-time bonus of €4.0 million ($4.6 million) paid to key individuals at Sitem Group as a result of the closing of the Sitem Group acquisition. Professional and other fees increased $29.4 million in fiscal 2026 compared to fiscal 2025, excluding Sitem Group expenses, primarily attributable to $35.8 million of professional and other fees related to the Kloeckner Acquisition. Additionally, compared to fiscal 2025, compensation expense increased by $10.8 million, including a $3.8 million increase in incentive compensation.

Other Operating Items

Change
(In millions) | 2026 | 2025 | %
Impairment of goodwill | 53.8 | - | 53.8 | -
Impairment of long-lived assets and other assets | 60.5 | 7.4 | 53.1 | 717.6 | %
Restructuring and other (income) expense, net | (7.0 | 2.6 | (9.6 | (369.2 | %)

_[...truncated at ~4,000 chars of this document]_

## 9. 10-K Item 1 - Business (10-K_2026-07-30_item1_business.md)

Item 1. — Business

General Overview

Worthington Steel, Inc., an Ohio corporation ("Worthington Steel" and, together with its consolidated subsidiaries and joint ventures, referred to herein as the "Company," "we," "us" or "our") is one of North America's premier value-added metals processors with the ability to provide a diversified range of products and services that span a variety of end markets. We are a value-added processor of carbon flat-rolled steel and a producer of laser welded solutions and electrical steel laminations. We are one of the largest independent intermediate processors of carbon flat-rolled steel in the U.S. We occupy a niche in the steel industry by focusing on products requiring exact specifications.

We buy coils of steel from primary steel producers and process them to the precise type, thickness, length, width, shape and surface quality required by customer specifications. Our product lines and processing capabilities include:

•
Carbon Flat-Rolled Steel Processing: We perform a variety of value-added processes based on customer requirements including pickling, specialty re-rolling, hot dip galvanizing, blanking, slitting and cutting-to-length.

•
Electrical Steel Laminations : We manufacture precision magnetic steel laminations for the automotive (including applications for electrified vehicles), industrial motor, generator and transformer industries. We deliver precision manufacturing (including stamping, heat treating, core assembly, die casting, bonding, etc.), material sourcing, metallurgical analysis, engineering, prototyping and product design, tooling, and value-added capabilities to customers via a global manufacturing footprint.

•
Tailor Welded Products : Tailor welded blanks and aluminum tailor welded blanks are used by North American automotive customers to reduce weight, lower cost, improve material utilization, and consolidate parts. Our highly engineered products allow for flexible part design and ensure the right material is used in the right place. Tailor welded blanks are made from individual sheets of steel of different thickness, strength and coating which are joined together by laser welding. Aluminum tailor welded blanks are processed using friction stir welding technology. Friction stir welding offers the widest range of formable welded properties for all automotive aluminum alloys.

We also toll process steel for steel mills, large end-users and service centers. Toll processing is different from direct sale steel processing in that the customer retains title to the steel and has the responsibility for selling the end product. Toll processing allows us to earn a fee for services without incurring inventory costs. Our manufacturing facilities further benefit from the flexibility to move between direct versus tolling services based on demand throughout the year.

We operate 34 manufacturing facilities located in the U.S. (19), Canada (2), China, India, Germany, Mexico (4), Italy (3), France, Slovakia, and Switzerland. In addition, our Serviacero joint venture operates three additional manufacturing facilities in Mexico. On June 3, 2026, subsequent to the completion of the fiscal year ended on May 31, 2026 ("fiscal 2026"), through our wholly owned indirect subsidiary Worthington Steel GmbH (the "Bidder"), we acquired a controlling equity stake in Germany-based Klöckner & Co SE ("Kloeckner"), which operates approximately 110 distribution and processing facilities primarily located in the United States, Mexico, Germany, Austria, and Switzerland.

We serviced approximately 1,500 customers during fiscal 2026 in many end markets including automotive, construction, machinery and equipment, agriculture, and heavy trucks, among others. The automotive industry is one of the largest consumers of flat-rolled steel, and the largest end market for us. During fiscal 2026, our top three customers, each of whom is in the automotive industry, represented approximately 34.5% of total net sales.

The steel processing industry is fragmented and highly competitive. There are many competitors, including other independent intermediate processors. Competition is primarily on the basis of price, product quality and the ability to meet delivery requirements. Technical service and support for material testing and customer-specific applications enhance the quality of products (see the Technical Services section below). However, the extent to which technical service and support capability has improved our competitive position has not been quantified. Our ability to meet tight delivery schedules is, in part, based on the proximity of our facilities to customers, suppliers and one another. The extent to which plant location has impacted our competitive position has not been quantified. Processed steel products are priced competitively, primarily based on market factors, including, among other things, market pricing, the cost and availability of raw materials, transportation and shipping costs, and overall economic conditions in the U.S. and abroad.

Our philosophy is rooted in the belief that people are our most important asset and is the basis for our unwavering commitment to our employees, customers, suppliers, and shareholders. Our primary goal is to create value for our shareholders. Built on the successful

foundation of the Worthington Business System, a strategic framework designed to drive continuous improvement through the use of enabling tools and technology that help drive results and inform our business decisions, we apply a disciplined approach to capital deployment and seek to grow earnings by optimizing our operations and supply chain, developing and commercializing new products and applications, and pursuing strategic investments and acquisitions.

_[...truncated at ~6,000 chars of this document]_

## 10. Earnings call material

_Not available: no transcript or prepared-remarks file was fetched. There is no management voice in this pack beyond the press release and MD&A._

## 11. Document availability

**Annual report form:** 10-K

| role | source item | file |
|---|---|---|
| Business description | 10-K Item 1 - Business | 10-K_2026-07-30_item1_business.md |
| MD&A / management commentary | 10-K Item 7 MD&A | 10-K_2026-07-30_item7_mdna.md |
| Risk factors | 10-K Item 1A - Risk Factors | 10-K_2026-07-30_item1a_risks.md |

**Present:** meta.json, form4_summary.md, 8-K_2026-07-10_2-02-results.md, 10-K_2026-07-30_item7_mdna.md, 10-K_2026-07-30_item1_business.md

**Missing:** transcript / prepared remarks

_Anything not listed as present is absent from this pack. Score conservatively and say what you could not check rather than guessing._
